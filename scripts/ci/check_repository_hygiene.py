#!/usr/bin/env python3
"""Reject prohibited generated artifacts committed to the repository tree."""

import subprocess
import sys


# Repository hygiene policy.
#
# Entries are repository-root-relative paths, written with a leading slash.
# Adding a prohibited path requires explicit evidence of the artifact and
# an intentional policy update here.
PROHIBITED_PATHS = (
    "/_dm.txt",
)


def error(message):
    print(f"::error::{message}", file=sys.stderr)


def committed_paths():
    """Return paths in the committed HEAD tree, not the working tree."""
    try:
        root_result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )
    except OSError as exc:
        raise RuntimeError(
            f"cannot execute git: {exc}"
        ) from exc

    if root_result.returncode != 0:
        raise RuntimeError(
            "cannot determine repository root: "
            "git rev-parse --show-toplevel failed"
        )

    root = root_result.stdout.strip()
    if not root:
        raise RuntimeError("git returned an empty repository root")

    try:
        tree_result = subprocess.run(
            [
                "git",
                "-C",
                root,
                "ls-tree",
                "-r",
                "-z",
                "--name-only",
                "HEAD",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(
            f"cannot inspect committed repository tree: {exc}"
        ) from exc

    if tree_result.returncode != 0:
        raise RuntimeError(
            "cannot inspect committed repository tree: "
            "git ls-tree failed for HEAD"
        )

    return set(tree_result.stdout.split(b"\0")) - {b""}


def main():
    try:
        paths = committed_paths()
    except RuntimeError as exc:
        error(f"repository hygiene cannot be determined: {exc}")
        return 2

    violations = []

    for prohibited_path in PROHIBITED_PATHS:
        git_path = prohibited_path.lstrip("/").encode("utf-8")

        if git_path in paths:
            violations.append(prohibited_path)

    if violations:
        for path in violations:
            error(
                "repository hygiene violation: "
                f"prohibited committed file '{path}'"
            )
        return 1

    print("Repository hygiene check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
