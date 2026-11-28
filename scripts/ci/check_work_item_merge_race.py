#!/usr/bin/env python3
"""Detect duplicate work-item claims merged through a two-parent Git merge.

This is a post-merge alarm, not a merge-prevention mechanism.
The prevention mechanism is strict required-status-check branch protection.
Exit codes: 0 no duplicate merge detected; 1 duplicate merge detected;
2 incomplete evidence.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

ROOT = "14-ai-development/work-items"
PATTERN = re.compile(
    r"^14-ai-development/work-items/(AID-\d{4}-\d{3})/"
)
TIMEOUT = 30


class Incomplete(RuntimeError):
    """A required Git object or tree could not be inspected."""


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
        raise Incomplete(
            f"git {args!r}: {type(exc).__name__}: {exc}"
        ) from exc

    if result.returncode:
        raise Incomplete(
            f"git {args!r} exited {result.returncode}: "
            f"{result.stderr.strip()}"
        )

    return result.stdout.strip()


def resolve_commit(ref: str, label: str) -> str:
    if not ref:
        raise Incomplete(f"{label} ref is empty")
    return run_git("rev-parse", "--verify", f"{ref}^{{commit}}")


def item_ids(commit: str) -> set[str]:
    tree = run_git("rev-parse", "--verify", f"{commit}^{{tree}}")
    names = run_git(
        "ls-tree", "-r", "--name-only", tree, "--", ROOT
    ).splitlines()

    return {
        match.group(1)
        for name in names
        if (match := PATTERN.match(name))
    }


def commit_subject(commit: str) -> str:
    return run_git("show", "-s", "--format=%s", commit)


def parents(commit: str) -> list[str]:
    fields = run_git(
        "rev-list", "--parents", "-n", "1", commit
    ).split()

    if not fields or fields[0] != commit:
        raise Incomplete(
            f"unexpected parent record for {commit}: {fields!r}"
        )

    return fields[1:]


def inspect_merge(commit: str) -> list[str]:
    merge_parents = parents(commit)

    if len(merge_parents) != 2:
        return []

    first, second = merge_parents

    merge_base = run_git(
        "merge-base", first, second
    )

    base_ids = item_ids(merge_base)
    first_ids = item_ids(first)
    second_ids = item_ids(second)

    duplicate_ids = sorted(
        (first_ids & second_ids) - base_ids
    )

    if not duplicate_ids:
        return []

    first_subject = commit_subject(first)
    second_subject = commit_subject(second)

    findings = []

    for item_id in duplicate_ids:
        findings.append(
            "DUPLICATE MERGE CLAIM: "
            f"{ROOT}/{item_id} "
            f"merge_commit={commit} "
            f"first_parent={first} "
            f"first_subject={first_subject!r} "
            f"second_parent={second} "
            f"second_subject={second_subject!r} "
            f"merge_base={merge_base}"
        )

    return findings


def check(before_ref: str, head_ref: str) -> int:
    try:
        before = resolve_commit(before_ref, "before")
        head = resolve_commit(head_ref, "head")

        commits = run_git(
            "rev-list", "--reverse", f"{before}..{head}"
        ).splitlines()

        findings: list[str] = []

        for commit in commits:
            findings.extend(inspect_merge(commit))

    except Incomplete as exc:
        print(f"WORK-ITEM MERGE RACE: INCOMPLETE ({exc})")
        return 2

    for finding in findings:
        print(f"VIOLATION: {finding}")

    if findings:
        print(
            "WORK-ITEM MERGE RACE: VIOLATION "
            f"(before={before} head={head} "
            f"findings={len(findings)})"
        )
        return 1

    print(
        "WORK-ITEM MERGE RACE: PASS "
        f"(before={before} head={head} findings=0)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args(argv)
    return check(args.before, args.head)


if __name__ == "__main__":
    sys.exit(main())
