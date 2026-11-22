#!/usr/bin/env python3
"""Ratchet gate wrapper: fail only when a known-red gate gets worse.

A ratchet is not a green exemption. The baseline records the *exact set* of
currently-failing items. The gate fails when:

  * a new item appears that is not in the baseline (regression), or
  * a baseline item no longer fails (the baseline is stale and must be lowered).

Failing on the second case is deliberate: it stops the baseline from silently
absorbing fixed items and drifting into a permanent blanket exemption.

Usage:
    python3 scripts/ci/gate_ratchet.py \
        --baseline scripts/ci/baselines/bilingual-docs.txt \
        --format paths \
        --command "python3 scripts/check_bilingual_docs_full.py"

Exit codes: 0 ratchet holds, 1 regression or stale baseline, 2 usage/IO error.

ponytail: `--format schema` is now uncalled -- the only gate that used it
(`schema-nonempty`) went green and became a hard gate, and its baseline was
deleted. The branch costs three lines; delete it, and the `--format` flag with
it, whenever this file is next touched for another reason.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

NUMBERED_PREFIX = re.compile(r"^\d{3,4}\.\s+")
ARROW_SUFFIX = re.compile(r"\s+->\s+.*$")

# Lines that report a verdict or a count rather than an offending item.
SUMMARY_PREFIXES = (
    "PASS",
    "FAIL",
    "OK",
    "Ran ",
    "FAILED",
    "NO TESTS",
    "GOV-DOC-001 full scan:",
    "runner admission:",
)

# Which stream each format's offending items are printed to. Anything not
# listed defaults to stdout. `dm` reads stderr because the document-management
# gate reports its verdict and statistics on stdout and its errors on stderr;
# see the module docstring.
ITEM_STREAM = {
    "dm": "stderr",
}


def normalize(lines: list[str], fmt: str) -> list[str]:
    """Reduce raw gate output to the stable set of offending items."""
    items: set[str] = set()
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith(SUMMARY_PREFIXES):
            continue
        if fmt == "paths":
            # Bilingual scanner: "042. some/path.md -> target expression"
            line = NUMBERED_PREFIX.sub("", line)
            line = ARROW_SUFFIX.sub("", line)
        elif fmt == "dm":
            # Document-management gate: "DM-01 <rule text>: some/path.md".
            # The path after the last ": " is the stable identifier; the rule
            # text in front of it changes whenever a rule is reworded.
            line = line.rsplit(": ", 1)[-1]
        # fmt == "schema": already one item per line, keep verbatim.
        items.add(line)
    return sorted(items)


def read_baseline(path: Path) -> list[str]:
    if not path.is_file():
        raise SystemExit(f"gate_ratchet: baseline not found: {path}")
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.append(stripped)
    return sorted(set(entries))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--command", required=True)
    parser.add_argument(
        "--format",
        choices=("schema", "paths", "dm"),
        default="schema",
        help="output shape of the wrapped gate",
    )
    args = parser.parse_args(argv)

    baseline = read_baseline(args.baseline)

    proc = subprocess.run(
        args.command,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    # Items are printed to the stream `ITEM_STREAM` names for this format
    # (stdout unless the gate reports errors on stderr). The other stream
    # carries interpreter warnings and tracebacks, which are not items; a crash
    # there yields zero items and is caught below as a stale baseline
    # (fail-closed), never as a pass.
    stream = proc.stderr if ITEM_STREAM.get(args.format) == "stderr" else proc.stdout
    current = normalize(stream.splitlines(), args.format)

    current_set, baseline_set = set(current), set(baseline)
    regressions = sorted(current_set - baseline_set)
    fixed = sorted(baseline_set - current_set)

    print(f"ratchet: {args.baseline.as_posix()}")
    print(f"ratchet: baseline={len(baseline)} current={len(current)} "
          f"regressions={len(regressions)} fixed={len(fixed)}")

    for item in regressions:
        print(f"::error::ratchet regression (new failure not in baseline): {item}")
    for item in fixed:
        print(f"::error::ratchet baseline is stale (no longer failing): {item}")

    if regressions or fixed:
        if regressions:
            print(f"ratchet: FAIL - {len(regressions)} new failure(s) above baseline.")
        if fixed:
            print(f"ratchet: FAIL - lower the baseline by {len(fixed)} fixed item(s).")
        return 1

    print("ratchet: PASS - failure set matches the baseline exactly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
