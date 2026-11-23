#!/usr/bin/env python3
"""Check Rust formatting without modifying the working tree.

This checker runs:

    cargo fmt --all -- --check

It never runs cargo fmt without --check and never modifies Rust files.

Commit identity and --expect semantics:
    pull_request:
        GitHub Actions checks out the synthetic PR merge commit. --expect
        must be GITHUB_SHA, which identifies that checked-out merge commit.
        The event payload supplies pull_request.head.sha and
        pull_request.base.sha. When all three identities are established,
        the checker reports CHECKED_MERGE_SHA, CHECKED_PR_HEAD_SHA, and
        CHECKED_BASE_SHA.

    push:
        GITHUB_SHA identifies the pushed commit checked out by the workflow.
        --expect must be GITHUB_SHA. The checker reports CHECKED_COMMIT_SHA.

    local or any other non-pull_request event:
        --expect, when supplied, is compared with the checked-out Git HEAD.
        The checker reports that single identity as CHECKED_COMMIT_SHA.
        No PR-specific fields are reported.

Exit codes:
    0  Formatting check passed.
    1  Formatting violations found.
    2  Unable to establish the checked tree's commit identity.
    3  cargo executable not found.
    4  Formatting check timed out.
    5  Invalid arguments or expected SHA mismatch.
    6  Other execution or internal error.
    7  Refused because the Git working tree is dirty.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn


EXIT_OK = 0
EXIT_FORMAT_FAILED = 1
EXIT_UNKNOWN_COMMIT = 2
EXIT_CARGO_NOT_FOUND = 3
EXIT_TIMEOUT = 4
EXIT_EXPECTATION_FAILED = 5
EXIT_ERROR = 6
EXIT_DIRTY_WORKTREE = 7

DEFAULT_TIMEOUT_SECONDS = 300

FULL_SHA_RE = re.compile(r"^[0-9a-fA-F]{40}$")


def fail(message: str, exit_code: int) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Rust formatting without modifying source files."
    )
    parser.add_argument(
        "--expect",
        metavar="SHA",
        help=(
            "Require the checked Git HEAD to equal this full 40-character SHA. "
            "In pull_request Actions runs use GITHUB_SHA (the synthetic merge "
            "commit); in push runs use GITHUB_SHA (the pushed commit). "
            "For local and other non-PR runs, this is compared with HEAD."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        metavar="SECONDS",
        help=f"Maximum cargo execution time (default: {DEFAULT_TIMEOUT_SECONDS}).",
    )

    args = parser.parse_args()

    if args.expect is not None and not FULL_SHA_RE.fullmatch(args.expect):
        parser.error("--expect requires exactly 40 hexadecimal characters")

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    return args


def find_repository_root() -> Path:
    """Find the repository containing this script, not the caller's cwd.

    Resolve the script path first. Walk upward from scripts/check_fmt.py
    and require a .git entry at the candidate root.

    A .git directory or .git file is accepted. A .git file supports
    Git worktrees. Merely finding a parent repository from cwd is
    deliberately insufficient.
    """

    script_path = Path(__file__).resolve()

    if script_path.parent.name != "scripts":
        fail(
            f"Expected check_fmt.py inside a scripts directory: {script_path}",
            EXIT_UNKNOWN_COMMIT,
        )

    root = script_path.parent.parent

    if not (root / ".git").exists():
        fail(
            f"No Git metadata found at the script's expected repository root: "
            f"{root}. Cannot establish checked commit identity.",
            EXIT_UNKNOWN_COMMIT,
        )

    return root


def get_head_sha(root: Path) -> str:
    """Read HEAD strictly within the expected repository root."""

    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "rev-parse",
                "--verify",
                "HEAD^{commit}",
            ],
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=15,
        )
    except FileNotFoundError:
        fail("git executable not found; cannot establish commit identity.", EXIT_UNKNOWN_COMMIT)
    except subprocess.TimeoutExpired:
        fail("Timed out while resolving Git HEAD.", EXIT_UNKNOWN_COMMIT)
    except OSError as exc:
        fail(f"Unable to execute git: {exc}", EXIT_UNKNOWN_COMMIT)

    if result.returncode != 0:
        detail = result.stderr.strip()
        fail(
            "Unable to resolve HEAD in the expected repository"
            + (f": {detail}" if detail else "."),
            EXIT_UNKNOWN_COMMIT,
        )

    sha = result.stdout.strip()

    if not FULL_SHA_RE.fullmatch(sha):
        fail(
            f"Git returned an invalid or unexpected HEAD SHA: {sha!r}",
            EXIT_UNKNOWN_COMMIT,
        )

    return sha.lower()


def get_pull_request_shas() -> tuple[str, str] | None:
    """Read and validate PR head/base SHAs only for pull_request events.

    Returns None for every non-pull_request event. For pull_request events,
    failure to read or validate either SHA makes commit identity unknown.
    """

    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return None

    event_path = os.environ.get("GITHUB_EVENT_PATH")

    if not event_path:
        fail(
            "GITHUB_EVENT_PATH is required for pull_request commit identity.",
            EXIT_UNKNOWN_COMMIT,
        )

    try:
        with Path(event_path).open("r", encoding="utf-8") as event_file:
            event = json.load(event_file)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(
            f"Unable to read GitHub pull_request event payload: {exc}",
            EXIT_UNKNOWN_COMMIT,
        )

    try:
        pull_request = event["pull_request"]
        head_sha = pull_request["head"]["sha"]
        base_sha = pull_request["base"]["sha"]
    except (KeyError, TypeError):
        fail(
            "GitHub pull_request event payload is missing pull_request.head.sha "
            "or pull_request.base.sha.",
            EXIT_UNKNOWN_COMMIT,
        )

    if not isinstance(head_sha, str) or not FULL_SHA_RE.fullmatch(head_sha):
        fail(
            f"GitHub event contains an invalid pull_request.head.sha: {head_sha!r}",
            EXIT_UNKNOWN_COMMIT,
        )

    if not isinstance(base_sha, str) or not FULL_SHA_RE.fullmatch(base_sha):
        fail(
            f"GitHub event contains an invalid pull_request.base.sha: {base_sha!r}",
            EXIT_UNKNOWN_COMMIT,
        )

    return head_sha.lower(), base_sha.lower()


def check_expected_sha(actual_sha: str, expected_sha: str | None) -> None:
    if expected_sha is None:
        return

    expected = expected_sha.lower()

    if actual_sha != expected:
        fail(
            "HEAD SHA mismatch: "
            f"expected {expected}, actual {actual_sha}. "
            "The checked tree is not the requested commit.",
            EXIT_EXPECTATION_FAILED,
        )


def require_clean_worktree(root: Path) -> None:
    """Refuse to attribute a formatting result to HEAD when the tree is dirty."""

    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "status",
                "--porcelain",
                "--untracked-files=all",
            ],
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=15,
        )
    except FileNotFoundError:
        fail("git executable not found; cannot establish working-tree cleanliness.", EXIT_UNKNOWN_COMMIT)
    except subprocess.TimeoutExpired:
        fail("Timed out while checking working-tree cleanliness.", EXIT_UNKNOWN_COMMIT)
    except OSError as exc:
        fail(f"Unable to check working-tree cleanliness: {exc}", EXIT_UNKNOWN_COMMIT)

    if result.returncode != 0:
        detail = result.stderr.strip()
        fail(
            "Unable to establish working-tree cleanliness"
            + (f": {detail}" if detail else "."),
            EXIT_UNKNOWN_COMMIT,
        )

    if result.stdout:
        print("WORKTREE_RESULT=DIRTY")
        print("Uncommitted paths:")
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
        fail(
            "Working tree is not clean; refusing to attribute a formatting verdict to HEAD.",
            EXIT_DIRTY_WORKTREE,
        )

    print("WORKTREE_RESULT=CLEAN")


def run_fmt(root: Path, timeout: float) -> int:
    cargo = shutil.which("cargo")

    if cargo is None:
        fail(
            "cargo executable not found in PATH.",
            EXIT_CARGO_NOT_FOUND,
        )

    command = [
        cargo,
        "fmt",
        "--all",
        "--",
        "--check",
    ]

    print(f"Repository root: {root}")
    print("Command: cargo fmt --all -- --check")
    print()

    try:
        result = subprocess.run(
            command,
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout

        if output:
            if isinstance(output, bytes):
                output = output.decode("utf-8", errors="replace")
            print(output, end="" if output.endswith("\n") else "\n")

        fail(
            f"cargo fmt timed out after {timeout} seconds.",
            EXIT_TIMEOUT,
        )
    except OSError as exc:
        fail(
            f"Unable to execute cargo fmt: {exc}",
            EXIT_ERROR,
        )

    if result.stdout:
        print(
            result.stdout,
            end="" if result.stdout.endswith("\n") else "\n",
        )

    print()

    if result.returncode == 0:
        print("FMT_RESULT=PASS")
        return EXIT_OK

    print(f"FMT_RESULT=FAIL (cargo exit code {result.returncode})")

    return EXIT_FORMAT_FAILED


def main() -> int:
    args = parse_args()

    root = find_repository_root()

    # Establish the checked-out commit identity before checking formatting.
    # Never use a parent repository's HEAD as a fallback.
    head_sha = get_head_sha(root)

    # This function is deliberately a no-op outside pull_request events.
    pull_request_shas = get_pull_request_shas()

    check_expected_sha(head_sha, args.expect)
    require_clean_worktree(root)

    if pull_request_shas is None:
        print(f"CHECKED_COMMIT_SHA={head_sha}")
    else:
        pr_head_sha, base_sha = pull_request_shas
        print(f"CHECKED_MERGE_SHA={head_sha}")
        print(f"CHECKED_PR_HEAD_SHA={pr_head_sha}")
        print(f"CHECKED_BASE_SHA={base_sha}")

    result = run_fmt(root, args.timeout)

    if result == EXIT_OK:
        print("CHECK_RESULT=PASS")
    else:
        print("CHECK_RESULT=FAIL")

    return result


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("ERROR: interrupted by user.", file=sys.stderr)
        raise SystemExit(EXIT_ERROR)
    except SystemExit:
        raise
    except Exception as exc:
        print(
            f"ERROR: unexpected checker failure: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_ERROR)
