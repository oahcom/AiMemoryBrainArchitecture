#!/usr/bin/env python3
"""Merge-time uniqueness gate for AID work-item registry records.

A duplicate declaration is one work-item id declared by two different
registry record paths inside the *same* tree. Modifying or deleting a record
that the target branch already owns is not a duplicate declaration: the
target branch still owns that record, and no second path declares the id.

Both trees are read independently and completely:

  * ``--head`` is the candidate tree (the pull request head, the merge-group
    head, or ``github.event.after``).
  * ``--base`` is the latest target-branch tree. CI refreshes ``origin/main``
    immediately before calling this and passes the refreshed SHA; the event's
    ``pull_request.base.sha`` is not used, because a stale target is exactly
    the failure this gate exists to catch.

Occupancy is decided by scanning the target tree, never by a merge base: a
merge base says what the candidate branch introduced, not what the target
branch currently owns.

Rules:

  1. Records are enumerated by canonical manifest path (``ROOT/<AID|FIX>/manifest.yaml``)
     and identified by their content: top-level ``work_item_id``, legacy
     ``aid``, or nested ``work_item.proposed_id``. An unreadable or unparseable
     blob is INCOMPLETE. A record that parses but declares no usable id, or
     declares one its own directory does not match, is a VIOLATION
     (``WORK_ITEM_ID_MISSING`` / ``WORK_ITEM_PATH_ID_MISMATCH``).
  2. A candidate merge tree is rejected when it contains multiple record paths
     declaring the same work-item id. Otherwise VIOLATION.
  3. A newly introduced id is rejected when the target tree's claim ledger
     contains a blocking ``CLAIMED`` or ``MERGED`` claim owned by another pull
     request. The candidate may not supply that ledger.
  4. An id present in both trees is shared, not duplicated: the candidate may
     modify or delete its record as long as it does not add a second path.

Authoritative ledger mode (``--registry-ref``): the ledger is read from that
ref instead of the base tree, and a newly introduced id must also carry a
blocking claim. When the pull request identity is supplied, that claim must
belong to the candidate's own pull request; ``MERGED`` is never exempted, and
a claim that was released (``ABANDONED``/``EXPIRED``) is reported separately
from an id that was never registered. Without the flag the base-tree rule
above is unchanged.

Exit codes: 0 PASS; 1 VIOLATION; 2 INCOMPLETE.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

ROOT = "14-ai-development/work-items"
DEFAULT_REGISTRY = ROOT + "/registry/work-item-claims.yaml"
AID_ID_RE = re.compile(r"AID-[0-9]{4}-[0-9]{3}\Z")
FIX_ID_RE = re.compile(r"FIX-[0-9]{4}-[A-Z0-9]+(?:-[A-Z0-9]+)*\Z")
RECORD_RE = re.compile(
    rf"^{ROOT}/(?P<dir>AID-[0-9]{{4}}-[0-9]{{3}}|FIX-[0-9]{{4}}-[A-Z0-9-]+)/manifest\.ya?ml\Z"
)
BLOCKING_STATUSES = frozenset({"CLAIMED", "MERGED"})
RELEASED_STATUSES = frozenset({"ABANDONED", "EXPIRED"})
KNOWN_STATUSES = frozenset({"CLAIMED", "MERGED", "ABANDONED", "EXPIRED"})
TIMEOUT = 60


def valid_work_item_id(value: object) -> bool:
    return isinstance(value, str) and bool(
        AID_ID_RE.match(value) or FIX_ID_RE.match(value)
    )


class Incomplete(RuntimeError):
    """The gate cannot reach a verdict; never a PASS."""


def run_git(
    *args: str, input_bytes: bytes | None = None
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", *args],
            input=input_bytes,
            capture_output=True,
            timeout=TIMEOUT,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise Incomplete(
            f"git {' '.join(args)}: {type(exc).__name__}: {exc}"
        ) from exc


def git(*args: str) -> str:
    result = run_git(*args)
    if result.returncode:
        raise Incomplete(
            f"git {' '.join(args)} exited {result.returncode}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result.stdout.decode("utf-8", "strict")


def resolve_commit(ref: str, label: str) -> str:
    if not ref:
        raise Incomplete(f"{label} ref is empty")
    return git("rev-parse", "--verify", f"{ref}^{{commit}}").strip()


def registry_paths(tree: str) -> list[str]:
    """Every canonical work-item manifest path under ROOT.

    A record is a manifest at ``ROOT/<AID-or-FIX-id>/manifest.yaml``. The path
    is how records are *found*; the id is how they are *identified*, and that
    is always read from the content (see ``record_id``). Discovering records by
    looking for a ``work_item_id:`` line would silently drop every manifest
    that carries its identity in a supported legacy shape.
    """
    result = run_git(
        "ls-tree", "-r", "-z", "--name-only", "--full-tree", tree, "--", ROOT
    )
    if result.returncode:
        raise Incomplete(
            f"cannot list {ROOT} on {tree}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    paths = []
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        path = entry.decode("utf-8", "strict")
        if RECORD_RE.match(path):
            paths.append(path)
    return sorted(paths)


def record_identity(data: dict) -> tuple[str | None, str | None]:
    """Read the declared work-item id from a manifest, across known shapes.

    Supported shapes, in priority order:
      * top-level ``work_item_id`` (current format);
      * top-level ``aid`` (legacy AID manifests);
      * ``work_item.proposed_id`` / ``work_item.work_item_id`` / ``work_item.id``
        (legacy nested registration manifests).

    Returns ``(id, None)`` or ``(None, reason)``. A missing, wrongly typed, or
    malformed identity is a violation of the identity constraint, not an
    unreadable input: the record was read and parsed successfully.
    """
    candidates = [
        ("work_item_id", data.get("work_item_id")),
        ("aid", data.get("aid")),
    ]
    nested = data.get("work_item")
    if isinstance(nested, dict):
        candidates.extend(
            (f"work_item.{key}", nested.get(key))
            for key in ("proposed_id", "work_item_id", "id")
        )
    for field, value in candidates:
        if value is None:
            continue
        if valid_work_item_id(value):
            return value, None
        return None, f"{field} is not a valid work-item id: {value!r}"
    return None, (
        "no supported work-item identity field "
        "(work_item_id, aid, or work_item.proposed_id)"
    )


def read_blobs(tree: str, paths: list[str]) -> dict[str, bytes]:
    """Read every blob in one ``git cat-file --batch`` call."""
    if not paths:
        return {}
    payload = "".join(f"{tree}:{path}\n" for path in paths).encode("utf-8")
    result = run_git("cat-file", "--batch", input_bytes=payload)
    if result.returncode:
        raise Incomplete(
            f"git cat-file --batch exited {result.returncode}: "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    data = result.stdout
    blobs: dict[str, bytes] = {}
    position = 0
    for path in paths:
        newline = data.find(b"\n", position)
        if newline < 0:
            raise Incomplete(f"truncated cat-file output for {path}")
        header = data[position:newline].split()
        position = newline + 1
        if len(header) != 3 or header[1] != b"blob":
            raise Incomplete(f"cannot read {path} on {tree}")
        size = int(header[2])
        blobs[path] = data[position:position + size]
        position += size + 1
    return blobs


def build_id_map(
    tree: str,
) -> tuple[dict[str, set[str]], list[tuple[str, str, str]]]:
    """Map each declared work-item id to the manifest paths declaring it.

    The id is read from the manifest content. The directory name is only used
    to check that the record's own location agrees with the id it declares; it
    can neither supply a missing id nor hide a duplicate.

    Returns ``(id_map, problems)`` where each problem is
    ``(path, code, detail)``. Unreadable or unparseable blobs raise
    ``Incomplete``; a record that was read but declares no usable identity, or
    declares one that disagrees with its own directory, is a problem the caller
    reports as a violation.
    """
    paths = registry_paths(tree)
    blobs = read_blobs(tree, paths)
    result: dict[str, set[str]] = {}
    problems: list[tuple[str, str, str]] = []
    for path in paths:
        try:
            data = load_yaml(blobs[path])
        except Exception as exc:  # noqa: BLE001 - any parse failure is INCOMPLETE
            raise Incomplete(
                f"{path} on {tree} is unreadable: {type(exc).__name__}: {exc}"
            ) from exc
        if not isinstance(data, dict):
            raise Incomplete(f"{path} on {tree} is not a mapping")
        work_item_id, reason = record_identity(data)
        if work_item_id is None:
            problems.append((path, "WORK_ITEM_ID_MISSING", reason or "unknown"))
            continue
        result.setdefault(work_item_id, set()).add(path)
        match = RECORD_RE.match(path)
        if match is not None and match.group("dir") != work_item_id:
            problems.append(
                (
                    path,
                    "WORK_ITEM_PATH_ID_MISMATCH",
                    f"declares {work_item_id} under directory {match.group('dir')}",
                )
            )
    return result, problems


def load_yaml(blob: bytes) -> object:
    import yaml

    return yaml.safe_load(blob.decode("utf-8"))


def blob_at(commit: str, path: str) -> str | None:
    result = run_git("cat-file", "-e", f"{commit}:{path}")
    if result.returncode == 0:
        return git("show", f"{commit}:{path}")
    # The commit itself must be readable; a missing path is a normal absence.
    git("cat-file", "-e", f"{commit}^{{commit}}")
    return None


def load_claims(base: str, head: str, registry: str) -> tuple[list[dict], str]:
    """Read the claim ledger from the target tree.

    The target tree is the only authoritative source. A candidate may not
    supply the ledger that decides its own occupancy: if the ledger is absent
    from the target tree and present in the candidate, the gate is INCOMPLETE
    and the ledger must be introduced by an explicitly authorized bootstrap
    before it can block anything. When neither tree has it, the ledger is
    empty. An unreadable or malformed ledger is INCOMPLETE.
    """
    text = blob_at(base, registry)
    source = f"base {base}"
    if text is None:
        if blob_at(head, registry) is not None:
            raise Incomplete(
                f"registry {registry} is absent from the target tree {base} "
                "but present in the candidate; a candidate-supplied ledger is "
                "not authoritative and bootstrap requires explicit authorization"
            )
        return [], "absent (no ledger in either tree)"
    try:
        data = load_yaml(text.encode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - any parse failure is INCOMPLETE
        raise Incomplete(
            f"registry {registry} unreadable: {type(exc).__name__}: {exc}"
        ) from exc
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
        if not valid_work_item_id(work_item_id):
            raise Incomplete(
                f"registry {registry} claims[{index}] has no valid work_item_id"
            )
        if status not in KNOWN_STATUSES:
            raise Incomplete(
                f"registry {registry} claims[{index}] has unknown status {status!r}"
            )
        parsed.append(claim)
    return parsed, source


def load_authoritative_registry(
    ref: str, registry: str
) -> tuple[list[dict], str]:
    """Read the claim ledger from its dedicated ref.

    The ref is the single authoritative source: a candidate pull request cannot
    supply or edit it. A missing or unreadable ref, a missing file, an
    unsupported schema, or a claim that is missing required fields is
    ``Incomplete`` — never a PASS. Two current claims for one id are a data
    corruption the loader reports as a violation, not as a priority contest.
    """
    probe = run_git("rev-parse", "--verify", f"{ref}^{{commit}}")
    if probe.returncode:
        raise Incomplete(
            f"authoritative ledger ref {ref} cannot be resolved: "
            f"{probe.stderr.decode('utf-8', 'replace').strip()}"
        )
    commit = probe.stdout.decode("utf-8", "strict").strip()
    text = blob_at(commit, registry)
    if text is None:
        raise Incomplete(f"registry {registry} is absent from {ref} ({commit})")
    try:
        data = load_yaml(text.encode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - any parse failure is INCOMPLETE
        raise Incomplete(
            f"registry {registry} on {ref} is unreadable: {type(exc).__name__}: {exc}"
        ) from exc
    if not isinstance(data, dict):
        raise Incomplete(f"registry {registry} on {ref} is not a mapping")
    schema_version = data.get("schema_version")
    if schema_version not in (1, 2):
        raise Incomplete(
            f"registry {registry} on {ref} declares unsupported "
            f"schema_version {schema_version!r}"
        )
    claims = data.get("claims")
    if not isinstance(claims, list):
        raise Incomplete(f"registry {registry} on {ref} declares no claims list")

    parsed: list[dict] = []
    seen: dict[str, int] = {}
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise Incomplete(f"registry claims[{index}] on {ref} is not a mapping")
        work_item_id = claim.get("work_item_id")
        status = claim.get("status")
        if not valid_work_item_id(work_item_id):
            raise Incomplete(
                f"registry claims[{index}] on {ref} has no valid work_item_id"
            )
        if status not in KNOWN_STATUSES:
            raise Incomplete(
                f"registry claims[{index}] on {ref} has unknown status {status!r}"
            )
        if schema_version == 2:
            missing = [
                key
                for key in ("repository", "owner_work_item", "claimed_at", "updated_at")
                if not claim.get(key)
            ]
            if status in BLOCKING_STATUSES and not claim.get("repository"):
                missing.append("repository")
            if missing:
                raise Incomplete(
                    f"registry claim {work_item_id} on {ref} is missing "
                    f"{', '.join(sorted(set(missing)))}"
                )
        seen[work_item_id] = seen.get(work_item_id, 0) + 1
        parsed.append(claim)
    duplicates = sorted(key for key, count in seen.items() if count > 1)
    if duplicates:
        raise DuplicateClaims(
            "registry holds more than one current claim for "
            + ", ".join(duplicates)
        )
    return parsed, f"{ref} ({commit})"


class DuplicateClaims(Incomplete):
    """Two current claims for one id: a violation, not an unreadable input."""


def is_own_claim(claim: dict, pull_request: int | None, repository: str | None) -> bool:
    """Only a CLAIMED record owned by this exact pull request is exempt.

    ``MERGED`` is permanent ownership and is never exempted; a released claim
    cannot be revived by the identity that released it; and a missing identity
    never defaults to ownership.
    """
    return (
        claim.get("status") == "CLAIMED"
        and pull_request is not None
        and repository is not None
        and claim.get("pull_request") == pull_request
        and claim.get("repository") == repository
    )


def check(
    base_ref: str,
    head_ref: str,
    registry: str = DEFAULT_REGISTRY,
    pull_request: int | None = None,
    repository: str | None = None,
    registry_ref: str | None = None,
) -> int:
    try:
        if pull_request is not None and not repository:
            raise Incomplete(
                "--pull-request requires --repository: a pull request number "
                "alone cannot identify the claiming repository"
            )

        base = resolve_commit(base_ref, "base")
        head = resolve_commit(head_ref, "candidate")

        git("cat-file", "-e", f"{base}^{{commit}}")
        git("cat-file", "-e", f"{head}^{{commit}}")

        base_map, base_problems = build_id_map(base)
        head_map, head_problems = build_id_map(head)
        if registry_ref:
            claims, registry_source = load_authoritative_registry(
                registry_ref, registry
            )
        else:
            claims, registry_source = load_claims(base, head, registry)
    except DuplicateClaims as exc:
        print(f"VIOLATION: DUPLICATE_CURRENT_CLAIM {exc}")
        print("WORK-ITEM UNIQUENESS: VIOLATION (authoritative ledger)")
        return 1
    except Incomplete as exc:
        print(f"WORK-ITEM UNIQUENESS: INCOMPLETE ({exc})")
        return 2

    # 1. Duplicate declarations inside the candidate tree.
    duplicates = {
        work_item_id: sorted(paths)
        for work_item_id, paths in head_map.items()
        if len(paths) > 1
    }

    # 2. Ids the candidate introduces, and ids both trees declare.
    introduced = set(head_map) - set(base_map)
    shared = set(head_map) & set(base_map)

    summary = (
        f"base={base} head={head} candidate_ids={len(head_map)} "
        f"target_ids={len(base_map)} introduced={len(introduced)} "
        f"shared={len(shared)} "
        f"duplicate_declarations={len(duplicates)} registry={registry_source}"
    )

    # Duplicate declarations and identity constraints are independent checks;
    # both are reported in one run, and neither classification depends on the
    # other.
    violations: list[str] = []
    for work_item_id, paths in sorted(duplicates.items()):
        violations.append(
            f"DUPLICATE_WORK_ITEM_ID {work_item_id} is declared by "
            f"{len(paths)} record paths in the candidate tree: "
            f"{', '.join(paths)}"
        )
    for tree, problems in ((base, base_problems), (head, head_problems)):
        for path, code, detail in problems:
            violations.append(f"{code} {path} on {tree}: {detail}")

    if violations:
        for violation in violations:
            print(f"VIOLATION: {violation}")
        print(f"WORK-ITEM UNIQUENESS: VIOLATION ({summary})")
        return 1

    # A shared id is a single record, not a competing claim: the duplicate
    # check above already rejected a second path, so every shared id now has
    # exactly one declaration in the candidate tree.
    for work_item_id in shared:
        assert len(head_map[work_item_id]) == 1

    blocked: dict[str, dict] = {}
    for claim in claims:
        if claim["status"] not in BLOCKING_STATUSES:
            continue
        if is_own_claim(claim, pull_request, repository):
            continue
        blocked.setdefault(claim["work_item_id"], claim)

    violations: list[str] = []
    for work_item_id in sorted(introduced):
        claim = blocked.get(work_item_id)
        if claim is not None:
            violations.append(
                f"{work_item_id} is already {claim['status']} in the claim "
                f"ledger by pull request {claim.get('pull_request')} "
                f"({claim.get('repository')})"
            )

    if registry_ref:
        registered = {claim["work_item_id"]: claim for claim in claims}
        for work_item_id in sorted(introduced):
            claim = registered.get(work_item_id)
            if claim is None:
                violations.append(
                    f"WORK_ITEM_ID_UNREGISTERED {work_item_id} is introduced by "
                    f"the candidate but has no claim in {registry_source}; claim "
                    "the id on the authoritative ledger before adding the record"
                )
            elif claim["status"] in RELEASED_STATUSES:
                violations.append(
                    f"WORK_ITEM_ID_RELEASED {work_item_id} was released as "
                    f"{claim['status']} (pull request {claim.get('pull_request')}); "
                    "claim it again instead of reusing the released record"
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
    parser.add_argument(
        "--registry", default=DEFAULT_REGISTRY, help="claim ledger path"
    )
    parser.add_argument(
        "--registry-ref",
        default=None,
        help=(
            "authoritative ledger ref (for example origin/work-item-claims); "
            "when set, the ledger is read from this ref and a newly introduced "
            "id must carry a blocking claim"
        ),
    )
    parser.add_argument(
        "--pull-request",
        type=int,
        default=None,
        help="candidate pull request number; its own claim is not a conflict",
    )
    parser.add_argument(
        "--repository",
        default=None,
        help="owner/name; only used with --pull-request",
    )
    args = parser.parse_args(argv)

    if not args.base or not args.head:
        missing = [
            name
            for name, value in (
                ("--base", args.base),
                ("--head", args.head),
            )
            if not value
        ]
        print(
            "WORK-ITEM UNIQUENESS: INCOMPLETE "
            f"(missing required ref(s): {', '.join(missing)})"
        )
        return 2

    return check(
        args.base,
        args.head,
        args.registry,
        args.pull_request,
        args.repository,
        args.registry_ref,
    )


if __name__ == "__main__":
    sys.exit(main())
