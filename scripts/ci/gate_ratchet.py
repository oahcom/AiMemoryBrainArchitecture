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

An *item* is the whole line the wrapped gate printed for it, minus its
`NNN. ` prefix: the part after ` -> ` is part of the item, not decoration. A
line that only reports the run's verdict or a count is not an item, but a
verdict word in front of a path (`OK <path> has no counterpart`) does not make
one a summary.

Exit codes: 0 ratchet holds, 1 regression, stale baseline, or a wrapped
command that exited non-zero without reporting an item, 2 usage/IO error.

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

# Lines that report a verdict or a count rather than an offending item. The
# boundary keeps an item whose name merely starts with a verdict word
# ("OK_STATUS") out of the summary set.
SUMMARY_RE = re.compile(
    r"^(?:PASS|FAIL|OK|FAILED|NO TESTS)(?![A-Za-z0-9_])"
    r"|^Ran\s"
    r"|^GOV-DOC-001 full scan:"
    r"|^runner admission:"
)

# A token that names a repository object. A "summary" line that still names
# one is not a summary: it is an offending item wearing a verdict prefix.
# `OK 00-governance/a.md has no counterpart` used to be dropped whole by the
# prefix filter, so a real failure never reached the comparison.
ITEM_TOKEN_RE = re.compile(
    r"\S*/\S*|\b[\w.-]+\.(?:md|py|ya?ml|rs|toml|json|txt)\b"
)


def is_summary(line: str) -> bool:
    return bool(SUMMARY_RE.match(line)) and not ITEM_TOKEN_RE.search(line)


def normalize(lines: list[str], fmt: str) -> list[str]:
    """Reduce raw gate output to the stable set of offending items.

    The item keeps everything the gate printed for it, including what follows
    ` -> `. Truncating at the arrow merged two different failures on the same
    path into one item, which is exactly the information a ratchet exists to
    compare.
    """
    items: set[str] = set()
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if is_summary(line):
            continue
        if fmt == "paths":
            # Bilingual scanner: "042. some/path.md -> target expression"
            line = NUMBERED_PREFIX.sub("", line)
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


def compare(baseline: list[str], current: list[str]) -> tuple[list[str], list[str]]:
    """Pair items with baseline entries; return (regressions, fixed).

    A baseline entry may be a bare path -- the shape `gates.yml` documents for
    `--format paths` (`sed -E 's/ -> .*$//'`), which is what every entry in the
    shipped baseline is. Such an entry stands for one item that begins with
    `"<path> -> "`.

    One item, not all of them: two different failures on the same path now need
    two baseline entries, so the second one is a regression. Covering every
    item of a path with that path's single entry is the same silent merge the
    arrow truncation used to perform.
    """
    unused = list(baseline)
    regressions: list[str] = []
    for item in current:
        matched = item if item in unused else None
        if matched is None:
            for entry in unused:
                if item.startswith(entry + " -> "):
                    matched = entry
                    break
        if matched is None:
            regressions.append(item)
        else:
            unused.remove(matched)
    return regressions, sorted(unused)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--command", required=True)
    parser.add_argument(
        "--format",
        choices=("schema", "paths"),
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
    # Items are printed to stdout. stderr carries interpreter warnings and
    # tracebacks, which are not items. A command that exits non-zero without
    # printing an item has not reported a failure set at all; that is checked
    # below, because an empty set minus an empty baseline is otherwise a pass.
    current = normalize(proc.stdout.splitlines(), args.format)

    regressions, fixed = compare(baseline, current)
    print(f"ratchet: {args.baseline.as_posix()}")
    print(f"ratchet: baseline={len(baseline)} current={len(current)} "
          f"regressions={len(regressions)} fixed={len(fixed)}")

    if proc.returncode not in (0, 1):
        print(f"ratchet: FAIL - the wrapped command exited {proc.returncode}; "
              "only 0 (clean) and 1 (red) carry a comparable failure set.")
        return 1

    if proc.returncode != 0 and not current:
        print(f"ratchet: FAIL - the wrapped command exited {proc.returncode} "
              "without printing any item; a crash is not a clean run.")
        return 1

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
