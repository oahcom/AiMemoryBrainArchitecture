#!/usr/bin/env python3
"""Assert that the immutable manifest blob-pin negative sample is rejected."""

import argparse
import subprocess
import sys
from pathlib import Path


EXPECTED_COMMIT = "9a2063ae1fa5d905b3817cd4eddba065a06daa73"
EXPECTED_SUMMARY = (
    "main=9a2063ae1fa5d905b3817cd4eddba065a06daa73 "
    "manifests=108 pins=169 ok=85 mismatch=80 "
    "path_missing=0 incomplete=1 unbound=4"
)
EXPECTED_MISMATCH = 80
EXPECTED_PATH_MISSING = 0
EXPECTED_UNBOUND = 4
EXPECTED_INCOMPLETE = (
    "INCOMPLETE related_evidence[0]: missing or invalid "
    "reference_mode=None; expected 'historical' or 'current'"
)


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
        print(
            result.stderr,
            file=sys.stderr,
            end="" if result.stderr.endswith("\n") else "\n",
        )

    lines = result.stdout.splitlines()
    summaries = [line for line in lines if line.startswith("main=")]
    mismatches = [line for line in lines if line.startswith("MISMATCH ")]
    missing = [line for line in lines if line.startswith("PATH_MISSING ")]
    incomplete = [line for line in lines if line.startswith("INCOMPLETE ")]
    unbound = [
        line for line in lines
        if line.startswith("UNBOUND_BLOB_SHA256 ")
    ]

    evidence_matches = (
        summaries == [EXPECTED_SUMMARY]
        and len(mismatches) == EXPECTED_MISMATCH
        and len(missing) == EXPECTED_PATH_MISSING
        and incomplete == [EXPECTED_INCOMPLETE]
        and len(unbound) == EXPECTED_UNBOUND
    )

    if result.returncode == 1:
        print(
            "VIOLATION: 负样本未被正确拒绝；"
            "checker returned exit 1, expected exit 2",
            file=sys.stderr,
        )
        return 1

    if result.returncode != 2:
        print(
            "VIOLATION: negative sample was not rejected with the "
            f"expected classification; checker exit={result.returncode}, "
            "expected=2",
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
        "immutable sample rejected with the expected INCOMPLETE classification; "
        "manifests=108 pins=169 ok=85 mismatch=80 "
        "path_missing=0 incomplete=1 unbound=4"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
