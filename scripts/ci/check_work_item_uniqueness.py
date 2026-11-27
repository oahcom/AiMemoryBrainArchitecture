#!/usr/bin/env python3
"""Merge-time uniqueness gate for newly introduced AID work-item directories.

A claim is a work-item directory that a candidate-only commit created: the
commit added a file under that directory and its own first-parent tree did not
contain the directory yet. The claim is rejected if the directory already
exists on the latest target-branch commit supplied by the caller, or if the
candidate declares the same AID from more than one candidate-only commit.

Claims are derived from candidate-only, non-merge commits and each commit's
first-parent tree. This keeps the original claim commit visible after GitHub
"Update branch" merges the advanced target into the candidate, which moves the
merge-base past that commit.

Files added beneath a directory already present in the claim commit's
first-parent tree are additive changes, not new claims.

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


def tree_ids(commit: str) -> set[str]:
    return {
        match.group(1)
        for name in git("ls-tree", "-r", "--name-only", commit, "--", ROOT).splitlines()
        if (match := PATTERN.match(name))
    }


def first_parent(commit: str) -> str | None:
    fields = git("rev-list", "--parents", "-n", "1", commit).split()
    if not fields or fields[0] != commit:
        raise Incomplete(f"cannot read the parent list of commit {commit}")
    return fields[1] if len(fields) > 1 else None


def claim_commits(
    base: str, head: str, candidate_ids: set[str]
) -> dict[str, list[str]]:
    """Map each candidate ID to the candidate-only commits that created it.

    The range excludes every commit reachable from the supplied base. Merge
    commits are excluded, so an Update-branch merge itself can neither erase
    nor invent a claim; the original non-merge claim commit stays visible.
    """
    claims = {item_id: [] for item_id in sorted(candidate_ids)}
    commits = git(
        "rev-list", "--no-merges", "--reverse", f"{base}..{head}"
    ).splitlines()

    for commit in commits:
        parent = first_parent(commit)

        if parent is None:
            added = git(
                "diff-tree",
                "--root",
                "--no-commit-id",
                "--name-only",
                "--diff-filter=A",
                "--no-renames",
                "-r",
                commit,
                "--",
                ROOT,
            ).splitlines()
        else:
            # Verify the parent object before using its tree.
            git("cat-file", "-e", f"{parent}^{{commit}}")
            added = git(
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "--diff-filter=A",
                "--no-renames",
                "-r",
                parent,
                commit,
                "--",
                ROOT,
            ).splitlines()

        for name in added:
            match = PATTERN.match(name)
            if not match:
                continue

            item_id = match.group(1)
            if item_id not in claims:
                continue

            directory = f"{ROOT}/{item_id}"

            if parent is None or not exists(parent, directory):
                claims[item_id].append(commit)

    return claims


def check(base_ref: str, head_ref: str) -> int:
    try:
        base = resolve_commit(base_ref, "base")
        head = resolve_commit(head_ref, "candidate")

        git("cat-file", "-e", f"{base}^{{commit}}")
        git("cat-file", "-e", f"{head}^{{commit}}")

        candidate_ids = tree_ids(head)
        claims = claim_commits(base, head, candidate_ids)

        introduced = sorted(
            item_id for item_id, commits in claims.items() if commits
        )
        occupied = [
            (f"{ROOT}/{item_id}", claims[item_id])
            for item_id in introduced
            if exists(base, f"{ROOT}/{item_id}")
        ]
        duplicated = [
            (item_id, commits)
            for item_id, commits in claims.items()
            if len(commits) > 1
        ]
        unidentifiable = [
            item_id for item_id in candidate_ids
            if not claims[item_id] and not exists(base, f"{ROOT}/{item_id}")
        ]

    except Incomplete as exc:
        print(f"WORK-ITEM UNIQUENESS: INCOMPLETE ({exc})")
        return 2

    if unidentifiable:
        print(
            "WORK-ITEM UNIQUENESS: INCOMPLETE "
            f"(no candidate-only commit created {ROOT}/{unidentifiable[0]}; "
            f"the claim cannot be identified) "
            f"base={base} candidate={head}"
        )
        return 2

    if occupied or duplicated:
        for path, commits in occupied:
            print(
                f"VIOLATION: {path} already exists on target base {base} "
                f"(candidate claim commits {','.join(commits)})"
            )

        for item_id, commits in duplicated:
            print(
                f"VIOLATION: {ROOT}/{item_id} is claimed by multiple "
                f"candidate-only commits {','.join(commits)}"
            )

        print(
            "WORK-ITEM UNIQUENESS: VIOLATION "
            f"(base={base} candidate={head} "
            f"introduced={len(introduced)} occupied={len(occupied)} "
            f"duplicate_claims={len(duplicated)})"
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
