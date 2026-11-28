#!/usr/bin/env python3
"""Ratchet gate wrapper with declaration-identity comparison for blob-pin v2."""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

NUMBERED_PREFIX = re.compile(r"^\d{3,4}\.\s+")
SUMMARY_RE = re.compile(
    r"^(?:PASS|FAIL|OK|FAILED|NO TESTS)(?![A-Za-z0-9_])|^Ran\s|"
    r"^GOV-DOC-001 full scan:|^runner admission:"
)
ITEM_TOKEN_RE = re.compile(r"\S*/\S*|\b[\w.-]+\.(?:md|py|ya?ml|rs|toml|json|txt)\b")
BLOB_PIN_BASELINE_FORMAT = "manifest-blob-pin-v2"
BLOB_PIN_IDENTITY_FIELDS = ("kind", "manifest", "pin_id", "field", "scope", "locator")
BLOB_PIN_KINDS = {"MISMATCH", "PATH_MISSING", "UNCLASSIFIED", "NO_SCOPE", "SCOPE_UNRESOLVABLE"}


def is_summary(line: str) -> bool:
    return bool(SUMMARY_RE.match(line)) and not ITEM_TOKEN_RE.search(line)


def normalize(lines: list[str], fmt: str) -> list[str]:
    items = set()
    for raw in lines:
        line = raw.strip()
        if not line or is_summary(line):
            continue
        if fmt == "paths":
            line = NUMBERED_PREFIX.sub("", line)
        items.add(line)
    return sorted(items)


def read_baseline(path: Path) -> list[str]:
    if not path.is_file():
        raise SystemExit(f"gate_ratchet: baseline not found: {path}")
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            entries.append(value)
    return sorted(set(entries))


def compare(baseline: list[str], current: list[str]):
    unused = list(baseline)
    regressions = []
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


def parse_blob_pin_line(line: str) -> tuple[str, ...] | None:
    try:
        parts = shlex.split(line)
    except ValueError:
        return None
    if not parts or parts[0] not in BLOB_PIN_KINDS:
        return None
    values = {}
    for part in parts[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            values[key] = value
    fields = ("manifest", "pin_id", "field", "scope", "locator")
    if any(key not in values for key in fields):
        return None
    return (parts[0], *(values[key] for key in fields))


def read_blob_pin_baseline(path: Path):
    if not path.is_file():
        raise SystemExit(f"gate_ratchet: baseline not found: {path}")
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("blob-pin baseline is empty; expected manifest-blob-pin-v2 header")
    header = json.loads(lines[0])
    if header.get("format") != BLOB_PIN_BASELINE_FORMAT or tuple(header.get("identity_fields", ())) != BLOB_PIN_IDENTITY_FIELDS:
        raise ValueError("legacy blob-pin baseline rejected; explicit v1-to-v2 migration required")
    identities = []
    for line in lines[1:]:
        record = json.loads(line)
        if tuple(record.keys()) != BLOB_PIN_IDENTITY_FIELDS:
            raise ValueError("blob-pin baseline record has non-canonical identity fields")
        identities.append(tuple(str(record[key]) for key in BLOB_PIN_IDENTITY_FIELDS))
    if len(identities) != len(set(identities)):
        raise ValueError("blob-pin baseline contains duplicate identities")
    return sorted(identities)


def normalize_blob_pin_findings(lines: list[str]):
    identities = []
    for line in lines:
        if not line.strip():
            continue
        identity = parse_blob_pin_line(line.strip())
        if identity is None:
            raise ValueError(f"unparseable blob-pin finding identity: {line}")
        identities.append(identity)
    if len(identities) != len(set(identities)):
        raise ValueError("checker emitted duplicate blob-pin finding identities")
    return sorted(identities)


def compare_blob_pin_identities(baseline, current):
    baseline_set, current_set = set(baseline), set(current)
    return sorted(current_set - baseline_set), sorted(baseline_set - current_set)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--command", required=True)
    parser.add_argument("--format", choices=("schema", "paths", BLOB_PIN_BASELINE_FORMAT), default="schema")
    args = parser.parse_args(argv)

    try:
        if args.format == BLOB_PIN_BASELINE_FORMAT:
            baseline = read_blob_pin_baseline(args.baseline)
        else:
            baseline = read_baseline(args.baseline)
        proc = subprocess.run(args.command, shell=True, capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        if args.format == BLOB_PIN_BASELINE_FORMAT:
            current = normalize_blob_pin_findings(proc.stdout.splitlines())
            regressions, fixed = compare_blob_pin_identities(baseline, current)
        else:
            current = normalize(proc.stdout.splitlines(), args.format)
            regressions, fixed = compare(baseline, current)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"gate_ratchet: ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"ratchet: {args.baseline.as_posix()}")
    print(f"ratchet: baseline={len(baseline)} current={len(current)} "
          f"regressions={len(regressions)} fixed={len(fixed)}")
    if proc.returncode not in (0, 1):
        print(f"ratchet: FAIL - wrapped command exited {proc.returncode}; only 0 (clean) and 1 (red) are comparable.")
        return 1
    if proc.returncode != 0 and not current:
        print(f"ratchet: FAIL - wrapped command exited {proc.returncode} without printing any item.")
        return 1
    for item in regressions:
        print(f"::error::ratchet regression: {item}")
    for item in fixed:
        print(f"::error::ratchet stale baseline identity: {item}; lower the baseline by removing fixed items.")
    if regressions or fixed:
        return 1
    print("ratchet: PASS - failure identity set matches baseline exactly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
