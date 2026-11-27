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
`NNN. ` prefix: the part after ` -> ` is part of the item, not decoration.

Exit codes: 0 ratchet holds, 1 regression or stale baseline, 2 usage,
IO, or malformed-baseline/output error.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

NUMBERED_PREFIX = re.compile(r"^\d{3,4}\.\s+")

SUMMARY_RE = re.compile(
    r"^(?:PASS|FAIL|OK|FAILED|NO TESTS)(?![A-Za-z0-9_])"
    r"|^Ran\s"
    r"|^GOV-DOC-001 full scan:"
    r"|^runner admission:"
)

ITEM_TOKEN_RE = re.compile(
    r"\S*/\S*|\b[\w.-]+\.(?:md|py|ya?ml|rs|toml|json|txt)\b"
)

BLOB_PIN_FORMAT = "manifest-blob-pin-v2"
BLOB_PIN_FIELDS = (
    "kind",
    "manifest",
    "pin_id",
    "field",
    "scope",
    "locator",
)
BLOB_PIN_FORBIDDEN_KINDS = {"SCOPE_UNRESOLVABLE", "UNRESOLVED", "INCOMPLETE"}

# The optional suffix is deliberately discarded. It may contain declared
# values, actual values, or human-readable diagnostics; none is identity.
BLOB_PIN_LINE_RE = re.compile(
    r"^(?P<kind>MISMATCH|PATH_MISSING|UNCLASSIFIED|NO_SCOPE)"
    r" manifest=(?P<manifest>\S+)"
    r" pin_id=(?P<pin_id>\S+)"
    r" field=(?P<field>\S+)"
    r" scope=(?P<scope>\S+)"
    r" locator=(?P<locator>\S+)"
    r"(?:\s+.*)?$"
)


class RatchetFormatError(ValueError):
    """The baseline or wrapped output violates its selected format."""


def is_summary(line: str) -> bool:
    return bool(SUMMARY_RE.match(line)) and not ITEM_TOKEN_RE.search(line)


def normalize(lines: list[str], fmt: str) -> list[str]:
    """Reduce raw gate output to the stable set of offending items."""
    items: set[str] = set()
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if fmt == BLOB_PIN_FORMAT:
            if line.startswith("::error::"):
                line = line[len("::error::"):]

            if is_blob_pin_identity_line(line):
                match = BLOB_PIN_LINE_RE.fullmatch(line)
                if not match:
                    raise RatchetFormatError(
                        f"malformed manifest blob pin identity line: {raw!r}"
                    )
                items.add("\0".join(
                    match.group(field) for field in BLOB_PIN_FIELDS
                ))
            continue
        if fmt == "schema" and is_blob_pin_identity_line(line):
            raise RatchetFormatError(
                "--format schema rejects manifest blob pin identity lines; "
                "use --format manifest-blob-pin-v2"
            )
        if is_summary(line):
            continue
        if fmt == "paths":
            line = NUMBERED_PREFIX.sub("", line)
        # fmt == "schema": one item per line, kept verbatim.
        items.add(line)
    return sorted(items)


def is_blob_pin_identity_line(line: str) -> bool:
    if line.startswith("::error::"):
        line = line[len("::error::"):]
    return bool(re.match(
        r"^(?:MISMATCH|PATH_MISSING|UNCLASSIFIED|NO_SCOPE)(?:\s|$)",
        line,
    ))


def _json_object_no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RatchetFormatError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def read_baseline(path: Path) -> list[str]:
    if not path.is_file():
        raise SystemExit(f"gate_ratchet: baseline not found: {path}")
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if is_blob_pin_identity_line(stripped):
            raise RatchetFormatError(
                "blob pin identity baseline cannot be read with --format schema"
            )
        entries.append(stripped)
    return sorted(set(entries))


def read_blob_pin_baseline(path: Path) -> list[str]:
    if not path.is_file():
        raise SystemExit(f"gate_ratchet: baseline not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        raise RatchetFormatError("manifest blob pin baseline is empty")

    parsed = []
    for line_number, line in enumerate(lines, 1):
        try:
            value = json.loads(
                line,
                object_pairs_hook=_json_object_no_duplicate_keys,
            )
        except (json.JSONDecodeError, RatchetFormatError) as exc:
            raise RatchetFormatError(
                f"invalid JSONL baseline line {line_number}: {exc}"
            ) from exc

        if not isinstance(value, dict):
            raise RatchetFormatError(
                f"baseline line {line_number} must be a JSON object"
            )

        if line_number == 1:
            if list(value.keys()) != ["format", "identity_fields"]:
                raise RatchetFormatError(
                    "baseline header keys/order must be "
                    '["format", "identity_fields"]'
                )
            if value != {
                "format": BLOB_PIN_FORMAT,
                "identity_fields": list(BLOB_PIN_FIELDS),
            }:
                raise RatchetFormatError(
                    "baseline header does not declare the required "
                    "manifest-blob-pin-v2 identity fields"
                )
            continue

        if list(value.keys()) != list(BLOB_PIN_FIELDS):
            raise RatchetFormatError(
                f"baseline line {line_number} keys/order must be "
                f"{list(BLOB_PIN_FIELDS)!r}"
            )
        if any(not isinstance(value[field], str) or not value[field]
               for field in BLOB_PIN_FIELDS):
            raise RatchetFormatError(
                f"baseline line {line_number} has a missing or invalid identity field"
            )
        if value["kind"] in BLOB_PIN_FORBIDDEN_KINDS:
            raise RatchetFormatError(
                f"baseline line {line_number} has non-ratchetable kind "
                f"{value['kind']!r}"
            )

        parsed.append(tuple(value[field] for field in BLOB_PIN_FIELDS))

    if not parsed:
        return []

    if len(parsed) != len(set(parsed)):
        raise RatchetFormatError("manifest blob pin baseline contains duplicate identities")
    if parsed != sorted(parsed):
        raise RatchetFormatError(
            "manifest blob pin baseline identities are not lexicographically sorted"
        )

    return [identity_key(identity) for identity in parsed]


def identity_key(identity: tuple[str, ...]) -> str:
    return "\0".join(identity)


def identity_display(key: str) -> str:
    values = key.split("\0")
    return "MISMATCH " + " ".join(
        f"{field}={value}" for field, value in zip(BLOB_PIN_FIELDS, values)
    )


def compare(baseline: list[str], current: list[str]) -> tuple[list[str], list[str]]:
    """Pair items with baseline entries; return (regressions, fixed).

    A paths baseline entry may be a bare path. It stands for one item that
    begins with "<path> -> ". Only one item is covered by one such entry.
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
        choices=("schema", "paths", BLOB_PIN_FORMAT),
        default="schema",
        help="output shape of the wrapped gate",
    )
    args = parser.parse_args(argv)

    try:
        baseline = (
            read_blob_pin_baseline(args.baseline)
            if args.format == BLOB_PIN_FORMAT
            else read_baseline(args.baseline)
        )
    except (OSError, UnicodeError, RatchetFormatError) as exc:
        print(f"::error::gate_ratchet: {exc}")
        return 2

    proc = subprocess.run(
        args.command,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        current = normalize(proc.stdout.splitlines(), args.format)
    except RatchetFormatError as exc:
        print(f"::error::gate_ratchet: {exc}")
        return 2

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
        shown = identity_display(item) if args.format == BLOB_PIN_FORMAT else item
        print(f"::error::ratchet regression (new failure not in baseline): {shown}")
    for item in fixed:
        shown = identity_display(item) if args.format == BLOB_PIN_FORMAT else item
        print(f"::error::ratchet baseline is stale (no longer failing): {shown}")

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
