#!/usr/bin/env python3
"""Merge-time uniqueness gate for newly introduced AID work-item directories.

A new claim is a work-item directory absent at merge-base but introduced
by the candidate. It is rejected if that directory already exists on the
latest target-branch commit supplied by the caller.

Files added beneath a directory already present at merge-base are additive
changes, not new claims.

Missing refs, Git failures, unreadable objects, and subprocess failures are
INCOMPLETE, never PASS.

Exit codes: 0 PASS; 1 VIOLATION; 2 INCOMPLETE.
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
    pass


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
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


def git(*args: str) -> str:
    result = run_git(*args)
    if result.returncode:
        raise Incomplete(
            f"git {args!r} exited {result.returncode}: "
            f"{result.stderr.strip()}"
        )
    return result.stdout.strip()


def resolve_commit(ref: str, label: str) -> str:
    if not ref:
        raise Incomplete(f"{label} ref is empty")
    return git("rev-parse", "--verify", f"{ref}^{{commit}}")


def exists(commit: str, path: str) -> bool:
    result = run_git("cat-file", "-e", f"{commit}:{path}")
    if result.returncode == 0:
        return True

    # A missing path is an ordinary absence only after the commit itself
    # has been verified as readable.
    git("cat-file", "-e", f"{commit}^{{commit}}")

    listing = run_git(
        "ls-tree",
        "-r",
        "--name-only",
        commit,
        "--",
        path,
    )
    if listing.returncode:
        raise Incomplete(
            f"cannot inspect {path} on {commit}: "
            f"{listing.stderr.strip()}"
        )

    return bool(listing.stdout.strip())


def introduced_dirs(merge_base: str, candidate: str) -> list[str]:
    names = git(
        "diff",
        "--diff-filter=A",
        "--name-only",
        "--no-renames",
        merge_base,
        candidate,
        "--",
        ROOT,
    ).splitlines()

    result = set()

    for name in names:
        match = PATTERN.match(name)
        if not match:
            continue

        directory = f"{ROOT}/{match.group(1)}"

        if not exists(merge_base, directory):
            result.add(directory)

    return sorted(result)


def check(base_ref: str, head_ref: str) -> int:
    try:
        base = resolve_commit(base_ref, "base")
        head = resolve_commit(head_ref, "candidate")

        merge_base = git("merge-base", base, head)
        if not merge_base:
            raise Incomplete("Git returned an empty merge-base")

        git("cat-file", "-e", f"{merge_base}^{{commit}}")

        introduced = introduced_dirs(merge_base, head)
        occupied = [
            path for path in introduced
            if exists(base, path)
        ]

    except Incomplete as exc:
        print(f"WORK-ITEM UNIQUENESS: INCOMPLETE ({exc})")
        return 2

    if occupied:
        for path in occupied:
            print(
                f"VIOLATION: {path} already exists on target base {base}"
            )

        print(
            "WORK-ITEM UNIQUENESS: VIOLATION "
            f"(base={base} candidate={head} "
            f"introduced={len(introduced)} occupied={len(occupied)})"
        )
        return 1

    print(
        "WORK-ITEM UNIQUENESS: PASS "
        f"(base={base} candidate={head} "
        f"introduced={len(introduced)} occupied=0)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="latest target-branch commit")
    parser.add_argument("--head", help="exact candidate commit")
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

    return check(args.base, args.head)


if __name__ == "__main__":
    sys.exit(main())
