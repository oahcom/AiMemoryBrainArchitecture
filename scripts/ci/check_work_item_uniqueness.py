#!/usr/bin/env python3
"""Merge-time uniqueness gate for AID work-item directories.

Both trees are read independently and completely:

  * ``--head`` is the candidate tree (the pull request head, the merge-group
    head, or ``github.event.after``).
  * ``--base`` is the latest target-branch tree. CI refreshes ``origin/main``
    immediately before calling this and passes the refreshed SHA; the event's
    ``pull_request.base.sha`` is not used, because a stale target is exactly the
    failure this gate exists to catch. A ref that is not a full 40-hex commit
    SHA is INCOMPLETE.

Nothing about occupancy is inferred from a merge base. The previous version
asked ``merge-base(base, head)`` what the candidate had "introduced"; once the
candidate merged the target branch, ``introduced`` was empty and a second claim
on the same ID passed silently. It also trusted a possibly stale ``base``.

Rules:

  1. ``new_ids = candidate_ids - target_ids``. Every new id must be absent from
     the target tree and must not be CLAIMED or MERGED in the registry by a
     different pull request. Otherwise VIOLATION.
  2. For ids present on both sides only ADDED paths are additive. A path the
     candidate itself modified or deleted since the fork point, under a shared
     id, is a competing claim on a record the target branch already owns.
     Otherwise VIOLATION. A candidate that is merely behind the target on that
     record has not claimed anything: that is a freshness failure, and the
     separate branch-freshness check owns it.
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


def _id_of(path: str) -> str | None:
    prefix = ROOT + "/"
    if not path.startswith(prefix):
        return None
    first = path[len(prefix):].split("/", 1)[0]
    return first if ID_RE.match(first) else None


def own_changes(fork: str, head: str) -> dict[str, str]:
    """Paths the candidate changed since the fork point, with their status."""
    output = git(
        "diff", "--name-status", "-z", "--no-renames", fork, head, "--", ROOT,
    )
    parts = [part for part in output.split("\0") if part]
    return {
        path: status
        for status, path in zip(parts[0::2], parts[1::2])
    }


def competing_claims(
    base: str, head: str, shared_ids: set[str], fork: str | None
) -> dict[str, str]:
    """Shared ids the candidate claims, with the reason.

    Two distinct situations, and only one of them is additive:

    * The id existed at the fork point, so the candidate inherited the record.
      Added files beneath it are additive; modifying or deleting a path that
      existed at the fork point is an edit to a record the target owns.
    * The id did not exist at the fork point, so the candidate introduced it
      independently while the target branch introduced the same id. Every path
      it contributes under that id is a competing claim, including additions.

    A candidate that is merely behind the target is neither: it inherited the
    record and changed nothing, which is a freshness failure owned by the
    separate branch-freshness check.
    """
    if not shared_ids:
        return {}
    if fork is None:
        # No common ancestor: attribute every difference to the candidate.
        fork_ids: set[str] = set()
        changes = own_changes(base, head)
    else:
        fork_ids = tree_ids(fork)
        changes = own_changes(fork, head)
    reasons: dict[str, str] = {}
    for path, status in sorted(changes.items()):
        work_item_id = _id_of(path)
        if work_item_id is None or work_item_id not in shared_ids:
            continue
        if work_item_id not in fork_ids:
            reasons.setdefault(
                work_item_id,
                "introduces an id the target branch already owns",
            )
        elif status in ("M", "D", "T", "R", "C"):
            reasons.setdefault(
                work_item_id,
                "modifies or deletes a record the target branch already owns",
            )
    return reasons


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
        try:
            fork = git("merge-base", base, head).strip() or None
        except Incomplete:
            # No usable common ancestor. Attribution falls back to "everything
            # the candidate differs on is the candidate's own", which can only
            # over-report, never pass.
            fork = None
        competing = competing_claims(base, head, shared_ids, fork)
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
    for work_item_id, reason in sorted(competing.items()):
        violations.append(
            f"{ROOT}/{work_item_id} {reason}; only added files beneath an "
            f"inherited record are additive"
        )

    summary = (
        f"base={base} head={head} candidate_ids={len(candidate_ids)} "
        f"target_ids={len(target_ids)} new_ids={len(new_ids)} "
        f"competing_shared={len(competing)} registry={registry_source}"
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
