#!/usr/bin/env python3
"""Compare work-item directory contents using only the base and candidate trees.

No commit ancestry, merge-base, branch name, or commit ordering participates in
the verdict. Exit codes: 0 PASS; 1 VIOLATION/DELETION; 2 INCOMPLETE.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

ROOT = "14-ai-development/work-items"
PATTERN = re.compile(r"^14-ai-development/work-items/(AID-\d{4}-\d{3})/")
TIMEOUT = 30


class Incomplete(RuntimeError):
    """An input tree or required Git object cannot be read."""


def run_git(*args: str) -> str:
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
        raise Incomplete(f"git {args!r}: {type(exc).__name__}: {exc}") from exc
    if result.returncode:
        raise Incomplete(
            f"git {args!r} exited {result.returncode}: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def resolve_tree(ref: str, label: str) -> str:
    if not ref:
        raise Incomplete(f"{label} ref is empty")
    return run_git("rev-parse", "--verify", f"{ref}^{{tree}}")


def item_paths(tree: str) -> dict[str, set[str]]:
    """Return each AID's tracked file paths relative to its directory."""
    paths: dict[str, set[str]] = {}
    for name in run_git("ls-tree", "-r", "--name-only", tree, "--", ROOT).splitlines():
        match = PATTERN.match(name)
        if match:
            item_id = match.group(1)
            prefix = f"{ROOT}/{item_id}/"
            paths.setdefault(item_id, set()).add(name[len(prefix):])
    return paths


def check(base_ref: str, head_ref: str) -> int:
    try:
        base_tree = resolve_tree(base_ref, "base")
        candidate_tree = resolve_tree(head_ref, "candidate")
        base_items = item_paths(base_tree)
        candidate_items = item_paths(candidate_tree)
    except Incomplete as exc:
        print(f"WORK-ITEM UNIQUENESS: INCOMPLETE ({exc})")
        return 2

    violations: list[tuple[str, list[str]]] = []
    deletions: list[str] = []

    for item_id in sorted(base_items.keys() | candidate_items.keys()):
        if item_id not in candidate_items:
            deletions.append(item_id)
            continue
        if item_id not in base_items:
            # A new declaration is permitted. Merge queue serializes races.
            continue

        added_paths = sorted(candidate_items[item_id] - base_items[item_id])
        if added_paths:
            violations.append((item_id, added_paths))

    for item_id, added_paths in violations:
        print(
            f"VIOLATION: {ROOT}/{item_id} "
            f"new_paths={','.join(added_paths)}"
        )
    for item_id in deletions:
        print(f"DELETION: {ROOT}/{item_id} exists_on_base=true absent_on_candidate=true")

    if violations or deletions:
        verdict = "VIOLATION" if violations else "DELETION"
        print(
            f"WORK-ITEM UNIQUENESS: {verdict} "
            f"(base_tree={base_tree} candidate_tree={candidate_tree} "
            f"violations={len(violations)} deletions={len(deletions)})"
        )
        return 1

    print(
        "WORK-ITEM UNIQUENESS: PASS "
        f"(base_tree={base_tree} candidate_tree={candidate_tree} "
        f"violations=0 deletions=0)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="baseline commit or tree")
    parser.add_argument("--head", required=True, help="candidate commit or tree")
    args = parser.parse_args(argv)
    return check(args.base, args.head)


if __name__ == "__main__":
    sys.exit(main())
