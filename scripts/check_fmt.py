#!/usr/bin/env python3
"""Check Rust formatting without modifying the working tree.

This checker runs:

    cargo fmt --all -- --check

It never runs cargo fmt without --check and never modifies Rust files.

Exit codes:
    0  Formatting check passed.
    1  Formatting violations found.
    2  Unable to establish the checked tree's commit identity.
    3  cargo executable not found.
    4  Formatting check timed out.
    5  Invalid arguments or expected SHA mismatch.
    6  Other execution or internal error.
"""

from __future__ import annotations

import argparse
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
        help="Require the checked Git HEAD to equal this full 40-character SHA.",
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
    print(f"Command: cargo fmt --all -- --check")
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

    # Establish the identity before checking formatting.
    # Never use a parent repository's HEAD as a fallback.
    head_sha = get_head_sha(root)

    check_expected_sha(head_sha, args.expect)

    print(f"CHECKED_HEAD_SHA={head_sha}")

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
