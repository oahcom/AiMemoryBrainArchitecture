#!/usr/bin/env python3
"""Ratchet gate wrapper: compare the exact set of failing gate items.

For --format schema, the wrapped command emits one finding per line.
The current set includes every non-PASS finding kind:

    MISMATCH
    PATH_MISSING
    UNCLASSIFIED
    NO_SCOPE
    UNRESOLVED
    SCOPE_UNRESOLVABLE
    INCOMPLETE

UNRESOLVED and INCOMPLETE are observable current findings, but they are
never permitted in an ordinary baseline. A wrapped command returning 2
represents an incomplete verification and is propagated as exit 2.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

NUMBERED_PREFIX = re.compile(r"^\d{3,4}\.\s+")

SCHEMA_KINDS = frozenset({
    "MISMATCH",
    "PATH_MISSING",
    "UNCLASSIFIED",
    "NO_SCOPE",
    "UNRESOLVED",
    "SCOPE_UNRESOLVABLE",
    "INCOMPLETE",
})

INCOMPLETE_KINDS = frozenset({
    "UNRESOLVED",
    "INCOMPLETE",
})

SUMMARY_RE = re.compile(
    r"^(?:PASS|FAIL|OK|FAILED|NO TESTS)(?![A-Za-z0-9_])"
    r"|^Ran\s"
    r"|^GOV-DOC-001 full scan:"
    r"|^runner admission:"
)

ITEM_TOKEN_RE = re.compile(
    r"\S*/\S*|\b[\w.-]+\.(?:md|py|ya?ml|rs|toml|json|txt)\b"
)


def is_summary(line: str) -> bool:
    return bool(SUMMARY_RE.match(line)) and not ITEM_TOKEN_RE.search(line)


def normalize(lines: list[str], fmt: str) -> list[str]:
    """Normalize command output into a sorted, deduplicated item set.

    Schema mode validates every non-summary line. An unknown kind or a
    malformed line is a format error, not an item to silently ratchet.
    """
    items: set[str] = set()

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        if fmt == "schema":
            # The checker prints one aggregate statistics line before
            # its finding lines. It is not part of the finding set.
            if line.startswith("main="):
                continue

            kind, separator, _remainder = line.partition(" ")
            if not separator or kind not in SCHEMA_KINDS:
                raise ValueError(
                    f"invalid schema output line (unknown or malformed kind): "
                    f"{line!r}"
                )
            items.add(line)
            continue

        if is_summary(line):
            continue

        if fmt == "paths":
            line = NUMBERED_PREFIX.sub("", line)

        items.add(line)

    return sorted(items)


def read_baseline(path: Path, fmt: str = "schema") -> list[str]:
    """Read and validate a baseline.

    An ordinary schema baseline must never contain UNRESOLVED or INCOMPLETE:
    those statuses require separate remediation/audit handling.
    """
    if not path.is_file():
        raise SystemExit(f"gate_ratchet: baseline not found: {path}")

    entries: list[str] = []

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if fmt == "schema":
            kind, separator, _remainder = stripped.partition(" ")
            if not separator or kind not in SCHEMA_KINDS:
                raise ValueError(
                    f"invalid schema baseline entry at "
                    f"{path}:{line_number}: {stripped!r}"
                )
            if kind in INCOMPLETE_KINDS:
                raise ValueError(
                    f"{kind} may not be stored in an ordinary baseline: "
                    f"{path}:{line_number}"
                )

        entries.append(stripped)

    return sorted(set(entries))


def compare(
    baseline: list[str],
    current: list[str],
) -> tuple[list[str], list[str]]:
    """Return (regressions, fixed) using one-to-one baseline matching.

    A baseline entry may be a bare path for --format paths. Such an entry
    matches one current item beginning with "<path> -> ". It cannot absorb
    multiple distinct failures on that path.
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

    try:
        baseline = read_baseline(args.baseline, args.format)
    except (OSError, UnicodeError, ValueError, SystemExit) as exc:
        print(f"gate_ratchet: baseline/format error: {exc}", file=sys.stderr)
        return 2

    try:
        proc = subprocess.run(
            args.command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        print(f"gate_ratchet: cannot run wrapped command: {exc}", file=sys.stderr)
        return 2

    try:
        current = normalize(proc.stdout.splitlines(), args.format)
    except ValueError as exc:
        print(f"gate_ratchet: output format error: {exc}", file=sys.stderr)
        return 2

    print(f"ratchet: {args.baseline.as_posix()}")
    print(
        f"ratchet: baseline={len(baseline)} current={len(current)} "
        f"regressions=pending fixed=pending"
    )

    # Exit 2 is reserved for incomplete/unresolvable verification and
    # internal/usage failures. Do not compare an incomplete result as if it
    # were a complete, stable failure set.
    if proc.returncode == 2:
        print(
            "ratchet: INCOMPLETE - wrapped command exited 2; "
            "current findings were collected but are not baseline-comparable."
        )
        return 2

    if proc.returncode not in (0, 1):
        print(
            f"ratchet: ERROR - wrapped command exited {proc.returncode}; "
            "only 0 and 1 carry a comparable failure set."
        )
        return 2

    if proc.returncode != 0 and not current:
        print(
            f"ratchet: ERROR - wrapped command exited {proc.returncode} "
            "without printing any item; a crash is not a clean run."
        )
        return 2

    regressions, fixed = compare(baseline, current)

    print(
        f"ratchet: baseline={len(baseline)} current={len(current)} "
        f"regressions={len(regressions)} fixed={len(fixed)}"
    )

    for item in regressions:
        print(
            "::error::ratchet regression "
            f"(new failure not in baseline): {item}"
        )

    for item in fixed:
        print(
            "::error::ratchet baseline is stale "
            f"(no longer failing): {item}"
        )

    if regressions or fixed:
        if regressions:
            print(
                f"ratchet: FAIL - {len(regressions)} new failure(s) "
                "above baseline."
            )
        if fixed:
            print(
                f"ratchet: FAIL - lower the baseline by "
                f"{len(fixed)} fixed item(s)."
            )
        return 1

    print("ratchet: PASS - failure set matches the baseline exactly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
