#!/usr/bin/env python3
"""Check newly introduced work-item directories against the latest target tree.

T-04 in check_traceability.py detects duplicate INDEX entries within one tree.
This checker detects independently introduced work-item directories whose
identifiers are already occupied in a newer target tree.

The candidate/target merge-base identifies which directories the candidate
introduced. Occupancy is judged against the current target tree, not against
the candidate branch's historical base alone.

The checker is read-only and reads Git objects without consulting or modifying
the working tree.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

WORK_ITEMS_PATH = "14-ai-development/work-items"
WORK_ITEM_ID = re.compile(r"^AID-\d{4}-\d{3}$")


class IncompleteError(RuntimeError):
    """The Git objects or relationships needed for a reliable decision are absent."""


def git(
    root: Path,
    *arguments: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=root,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def resolve_commit(root: Path, ref: str) -> str:
    result = git(root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if result.returncode:
        raise IncompleteError(
            f"cannot resolve commit ref {ref!r}: "
            f"{result.stderr.strip() or 'Git object unavailable'}"
        )

    sha = result.stdout.strip()
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", sha):
        raise IncompleteError(f"ref {ref!r} did not resolve to a commit SHA")
    return sha


def tree_ids(root: Path, commit: str) -> set[str]:
    """Return immediate AID directory names beneath WORK_ITEMS_PATH."""
    treeish = f"{commit}:{WORK_ITEMS_PATH}"

    object_type = git(root, "cat-file", "-t", treeish)
    if object_type.returncode:
        raise IncompleteError(
            f"cannot resolve work-items tree at {commit}: "
            f"{object_type.stderr.strip() or 'Git object unavailable'}"
        )

    if object_type.stdout.strip() != "tree":
        raise IncompleteError(
            f"{WORK_ITEMS_PATH} is not a tree at {commit}"
        )

    result = git(root, "ls-tree", "-z", treeish)
    if result.returncode:
        raise IncompleteError(
            f"cannot list work-items tree at {commit}: "
            f"{result.stderr.strip()}"
        )

    ids: set[str] = set()

    for entry in result.stdout.split("\0"):
        if not entry:
            continue

        if "\t" not in entry:
            raise IncompleteError(
                f"unparseable ls-tree entry in work-items tree at {commit}"
            )

        metadata, name = entry.split("\t", 1)
        fields = metadata.split()

        if len(fields) != 3:
            raise IncompleteError(
                f"unparseable ls-tree metadata in work-items tree at {commit}"
            )

        mode, entry_type, _object_id = fields

        if not WORK_ITEM_ID.fullmatch(name):
            continue

        if entry_type != "tree" or mode not in {"040000", "40000"}:
            raise IncompleteError(
                f"work-item path {WORK_ITEMS_PATH}/{name} "
                f"is not a directory at {commit}"
            )

        ids.add(name)

    return ids


def find_merge_base(root: Path, candidate: str, target: str) -> str:
    result = git(root, "merge-base", "--all", candidate, target)

    if result.returncode:
        raise IncompleteError(
            "cannot determine candidate/target merge-base: "
            f"{result.stderr.strip() or 'no common ancestor'}"
        )

    bases = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    if len(bases) != 1:
        raise IncompleteError(
            "candidate and target do not have exactly one merge-base "
            f"(found {len(bases)}); refusing an ambiguous decision"
        )

    return bases[0]


def scan(
    root: Path,
    target_ref: str,
    candidate_ref: str,
) -> tuple[int, dict[str, int], list[str]]:
    totals = {
        "candidate_new_directories": 0,
        "target_occupied_new_directories": 0,
        "accepted_new_directories": 0,
        "existing_directories": 0,
    }
    details: list[str] = []

    candidate_sha = "UNRESOLVED"
    target_sha = "UNRESOLVED"

    try:
        candidate_sha = resolve_commit(root, candidate_ref)
        target_sha = resolve_commit(root, target_ref)
        base_sha = find_merge_base(root, candidate_sha, target_sha)

        base_ids = tree_ids(root, base_sha)
        target_ids = tree_ids(root, target_sha)
        candidate_ids = tree_ids(root, candidate_sha)

        introduced_ids = candidate_ids - base_ids
        conflicts = sorted(introduced_ids & target_ids)
        accepted = sorted(introduced_ids - target_ids)
        existing = sorted(candidate_ids & base_ids)

        totals["candidate_new_directories"] = len(introduced_ids)
        totals["target_occupied_new_directories"] = len(conflicts)
        totals["accepted_new_directories"] = len(accepted)
        totals["existing_directories"] = len(existing)

        print(f"candidate={candidate_sha}")
        print(f"target={target_sha}")
        print(f"merge_base={base_sha}")

        for aid in accepted:
            details.append(
                f"PASS new work-item directory {aid}: target is unoccupied"
            )

        for aid in existing:
            details.append(
                f"PASS existing work-item directory {aid}: "
                "incremental changes allowed"
            )

        for aid in conflicts:
            details.append(
                f"ERROR WU-01 duplicate work-item directory {aid}: "
                "candidate introduces this ID, but the latest target "
                "already contains it"
            )

        print("WORK_ITEM_UNIQUENESS")
        for key, value in totals.items():
            print(f"{key.upper()}={value}")

        print(f"BAD={len(conflicts)}")

        for detail in details:
            print(detail)

        if conflicts:
            return 1, totals, details

        print("PASS WORK ITEM UNIQUENESS")
        return 0, totals, details

    except IncompleteError as exc:
        print(f"candidate={candidate_sha}")
        print(f"target={target_sha}")
        print("WORK_ITEM_UNIQUENESS")
        print("INCOMPLETE=1")
        print("BAD=0")
        print(f"INCOMPLETE: {exc}")
        return 2, totals, [str(exc)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--target",
        default="origin/main",
        help="latest target branch ref (default: origin/main)",
    )
    parser.add_argument(
        "--candidate",
        default="HEAD",
        help="exact candidate commit/ref (default: HEAD)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Git repository root (default: checker repository)",
    )

    args = parser.parse_args(argv)
    root = args.root.resolve()

    check = git(root, "rev-parse", "--show-toplevel")
    if check.returncode:
        print("INCOMPLETE: --root is not a Git working repository")
        return 2

    exit_code, _totals, _details = scan(
        root,
        args.target,
        args.candidate,
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
