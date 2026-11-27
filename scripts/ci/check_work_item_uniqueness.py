#!/usr/bin/env python3
"""Merge-time uniqueness gate for AID work-item directories.

Both trees are read independently and completely:

  * ``--head`` is the candidate tree (the pull request head, the merge-group
    head, or ``github.event.after``).
  * ``--base`` is the latest target-branch tree (the pull request base, the
    merge-group base, or ``github.event.before``).

Nothing about occupancy is inferred from a merge base. The previous version
asked ``merge-base(base, head)`` what the candidate had "introduced"; once the
candidate merged the target branch, ``introduced`` was empty and a second claim
on the same ID passed silently. It also trusted a possibly stale ``base``.

Rules:

  1. ``new_ids = candidate_ids - target_ids``. Every new id must be absent from
     the target tree and must not be CLAIMED or MERGED in the registry by a
     different pull request. Otherwise VIOLATION.
  2. For ids present on both sides only ADDED paths are additive. A modified or
     deleted path under a shared id is a competing claim on a record the target
     branch already owns. Otherwise VIOLATION.
  3. Unreadable refs, unreadable trees, or an unreadable registry are
     INCOMPLETE (exit 2), never PASS.

Exit codes: 0 PASS; 1 VIOLATION; 2 INCOMPLETE.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

ROOT = "14-ai-development/work-items"
DEFAULT_REGISTRY = ROOT + "/registry/work-item-claims.yaml"
ID_RE = re.compile(r"AID-\d{4}-\d{3}\Z")
BLOCKING_STATUSES = frozenset({"CLAIMED", "MERGED"})
KNOWN_STATUSES = frozenset({"CLAIMED", "MERGED", "ABANDONED"})
TIMEOUT = 30


class Incomplete(RuntimeError):
    """The gate cannot reach a verdict; never a PASS."""


def git(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
        raise Incomplete(f"git {' '.join(args)}: {type(exc).__name__}: {exc}") from exc
    if result.returncode:
        raise Incomplete(
            f"git {' '.join(args)} exited {result.returncode}: {result.stderr.strip()}"
        )
    return result.stdout


def resolve_commit(ref: str, label: str) -> str:
    if not ref:
        raise Incomplete(f"{label} ref is empty")
    return git("rev-parse", "--verify", f"{ref}^{{commit}}").strip()


def _ids_in(output: str) -> set[str]:
    """Extract first-level AID-YYYY-NNN directory names from tree paths."""
    prefix = ROOT + "/"
    found: set[str] = set()
    for entry in output.split("\0"):
        if not entry.startswith(prefix):
            continue
        first = entry[len(prefix):].split("/", 1)[0]
        if ID_RE.match(first):
            found.add(first)
    return found


def tree_ids(commit: str) -> set[str]:
    """Every work-item id present anywhere in the commit's tree."""
    return _ids_in(git("ls-tree", "-r", "-z", "--name-only", "--full-tree", commit, "--", ROOT))


def competing_ids(base: str, head: str) -> set[str]:
    """Ids with at least one modified or deleted path between base and head."""
    output = git(
        "diff", "--name-only", "-z", "--no-renames", "--diff-filter=MD",
        base, head, "--", ROOT,
    )
    return _ids_in(output)


def _blob_at(commit: str, path: str) -> str | None:
    probe = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}:{path}"],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    if probe.returncode == 0:
        return git("show", f"{commit}:{path}")
    # The commit itself must be readable; a missing path is a normal absence.
    git("cat-file", "-e", f"{commit}^{{commit}}")
    return None


def load_claims(base: str, head: str, registry: str) -> tuple[list[dict], str]:
    """Read the claim ledger from the target tree, bootstrapping from the head.

    The target branch is authoritative. When the registry does not exist there
    yet (the change that introduces it), the candidate copy is used so that the
    introducing pull request is not blocked by its own bootstrap. When neither
    tree has it, the ledger is empty: the Owner ruling requires this gate not to
    depend on registry completeness, because ids that already exist on the
    target tree are rejected independently. An unreadable or malformed ledger
    is still INCOMPLETE.
    """
    text = _blob_at(base, registry)
    source = f"base {base}"
    if text is None:
        text = _blob_at(head, registry)
        source = f"head {head} (bootstrap: registry absent from base)"
    if text is None:
        return [], "absent (no ledger in either tree)"
    try:
        import yaml

        data = yaml.safe_load(text)
    except Exception as exc:  # noqa: BLE001 - any parse failure is INCOMPLETE
        raise Incomplete(f"registry {registry} unreadable: {type(exc).__name__}: {exc}") from exc
    if not isinstance(data, dict):
        raise Incomplete(f"registry {registry} is not a mapping")
    if data.get("schema_version") != 1:
        raise Incomplete(f"registry {registry} does not declare schema_version: 1")
    claims = data.get("claims")
    if not isinstance(claims, list):
        raise Incomplete(f"registry {registry} does not declare a claims list")
    parsed: list[dict] = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise Incomplete(f"registry {registry} claims[{index}] is not a mapping")
        work_item_id = claim.get("work_item_id")
        status = claim.get("status")
        if not isinstance(work_item_id, str) or not ID_RE.match(work_item_id):
            raise Incomplete(f"registry {registry} claims[{index}] has no valid work_item_id")
        if status not in KNOWN_STATUSES:
            raise Incomplete(f"registry {registry} claims[{index}] has unknown status {status!r}")
        parsed.append(claim)
    return parsed, source


def check(
    base_ref: str,
    head_ref: str,
    registry: str,
    pull_request: int | None,
    repository: str | None,
) -> int:
    try:
        base = resolve_commit(base_ref, "base")
        head = resolve_commit(head_ref, "head")
        target_ids = tree_ids(base)
        candidate_ids = tree_ids(head)
        new_ids = sorted(candidate_ids - target_ids)
        shared_ids = candidate_ids & target_ids
        competing = competing_ids(base, head) & shared_ids
        claims, registry_source = load_claims(base, head, registry)
    except Incomplete as exc:
        print(f"WORK-ITEM UNIQUENESS: INCOMPLETE ({exc})")
        return 2

    blocked: dict[str, dict] = {}
    for claim in claims:
        if claim["status"] not in BLOCKING_STATUSES:
            continue
        same_pr = pull_request is not None and claim.get("pull_request") == pull_request
        same_repo = repository is None or claim.get("repository") == repository
        if same_pr and same_repo:
            continue
        blocked.setdefault(claim["work_item_id"], claim)

    violations: list[str] = []
    for work_item_id in new_ids:
        path = f"{ROOT}/{work_item_id}"
        if work_item_id in target_ids:
            violations.append(f"{path} already exists on the target tree {base}")
            continue
        claim = blocked.get(work_item_id)
        if claim is not None:
            violations.append(
                f"{path} is already {claim['status']} in the registry by pull request "
                f"{claim.get('pull_request')} ({claim.get('repository')})"
            )
    for work_item_id in sorted(competing):
        violations.append(
            f"{ROOT}/{work_item_id} has modified or deleted paths; the target branch "
            f"already owns this work item, so only added files are additive"
        )

    summary = (
        f"base={base} head={head} candidate_ids={len(candidate_ids)} "
        f"target_ids={len(target_ids)} new_ids={len(new_ids)} "
        f"modified_under_shared={len(competing)} registry={registry_source}"
    )
    if violations:
        for violation in violations:
            print(f"VIOLATION: {violation}")
        print(f"WORK-ITEM UNIQUENESS: VIOLATION ({summary})")
        return 1
    print(f"WORK-ITEM UNIQUENESS: PASS ({summary})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="latest target-branch commit")
    parser.add_argument("--head", help="candidate commit")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY, help="claim ledger path")
    parser.add_argument("--pull-request", type=int, default=None,
                        help="candidate pull request number; its own claim is not a conflict")
    parser.add_argument("--repository", default=None,
                        help="owner/name; only used with --pull-request")
    args = parser.parse_args(argv)
    if not args.base or not args.head:
        missing = [name for name, value in (("--base", args.base), ("--head", args.head)) if not value]
        print(f"WORK-ITEM UNIQUENESS: INCOMPLETE (missing required ref(s): {', '.join(missing)})")
        return 2
    return check(args.base, args.head, args.registry, args.pull_request, args.repository)


if __name__ == "__main__":
    sys.exit(main())
