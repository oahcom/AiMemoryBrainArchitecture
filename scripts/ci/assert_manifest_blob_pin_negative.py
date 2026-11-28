#!/usr/bin/env python3
"""Assert that the immutable manifest blob-pin negative sample is rejected."""

import argparse
import subprocess
import sys
from pathlib import Path


EXPECTED_COMMIT = "9a2063ae1fa5d905b3817cd4eddba065a06daa73"
EXPECTED_SUMMARY = (
    "main=9a2063ae1fa5d905b3817cd4eddba065a06daa73 "
    "manifests=108 pins=172 ok=82 mismatch=86 "
    "path_missing=0 incomplete=0 unbound=4"
)
# The sample also carries four unbound blob_sha256 declarations. They are
# counted exactly, not tolerated: an extra or missing one is a changed sample.
EXPECTED_UNBOUND = 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", default=EXPECTED_COMMIT)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    if args.commit != EXPECTED_COMMIT:
        print(
            "INCOMPLETE: negative assertion is restricted to its immutable fixture",
            file=sys.stderr,
        )
        return 2

    root = Path(args.root).resolve()
    checker = root / "scripts" / "ci" / "check_manifest_blob_pins.py"

    if not checker.is_file():
        print(f"INCOMPLETE: checker not found: {checker}", file=sys.stderr)
        return 2

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(checker),
                "--commit",
                EXPECTED_COMMIT,
            ],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        print(f"INCOMPLETE: checker could not execute: {exc}", file=sys.stderr)
        return 2

    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")

    if result.returncode == 2:
        print("INCOMPLETE: negative-sample checker returned exit 2", file=sys.stderr)
        return 2

    lines = result.stdout.splitlines()
    summaries = [line for line in lines if line.startswith("main=")]
    mismatches = [line for line in lines if line.startswith("MISMATCH ")]
    missing = [line for line in lines if line.startswith("PATH_MISSING ")]
    incomplete = [line for line in lines if line.startswith("INCOMPLETE ")]
    unbound = [line for line in lines if line.startswith("UNBOUND_BLOB_SHA256 ")]

    evidence_matches = (
        summaries == [EXPECTED_SUMMARY]
        and len(mismatches) == 86
        and len(missing) == 0
        and len(incomplete) == 0
        and len(unbound) == EXPECTED_UNBOUND
    )

    if result.returncode != 1:
        print(
            "VIOLATION: negative sample was not rejected; "
            f"checker exit={result.returncode}, expected=1",
            file=sys.stderr,
        )
        return 1

    if not evidence_matches:
        print(
            "VIOLATION: negative sample rejection did not produce the "
            "expected immutable evidence",
            file=sys.stderr,
        )
        return 1

    print(
        "NEGATIVE_ASSERTION_PASS: "
        "immutable sample rejected; "
        "manifests=108 pins=172 ok=82 mismatch=86 "
        "path_missing=0 incomplete=0 unbound=4"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
