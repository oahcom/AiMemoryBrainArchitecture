#!/usr/bin/env python3
"""Generate a manifest blob-pin v2 identity baseline from a legacy v1 baseline.

The generator is intentionally fail-closed: it never writes a baseline when the
measurement introduces an identity absent from v1, or when the checker reports
an incomplete/internal error.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

IDENTITY_FIELDS = ("kind", "manifest", "pin_id", "field", "scope", "locator")
CURRENT_KINDS = {"MISMATCH", "PATH_MISSING", "INCOMPLETE", "NO_SCOPE", "UNCLASSIFIED"}
UNRESOLVED = "UNRESOLVED"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _identity(kind: str, values: dict[str, str]) -> tuple[str, ...]:
    return (kind, *(values.get(key) or UNRESOLVED for key in IDENTITY_FIELDS[1:]))


def _key_values(parts: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            values[key] = value
    return values


def _regex_values(line: str) -> dict[str, str]:
    return dict(re.findall(r"(?:^|\s)(manifest|pin_id|field|scope|locator)=([^\s]+)", line))


def parse_current_line(line: str) -> tuple[str, ...] | None:
    line = line.strip()
    if not line or " detail " in f" {line} " or "actual=" in line or "declared=" in line:
        return None
    if line.startswith("INTERNAL_ERROR"):
        raise RuntimeError(line)
    if line.startswith("INCOMPLETE"):
        values = _regex_values(line)
        hint = re.match(r"^INCOMPLETE\s+UNRESOLVED\((.*?)\)", line)
        if hint and "field" not in values:
            values["field"] = hint.group(1).split(" blob locator", 1)[0]
        return _identity("INCOMPLETE", values)
    try:
        parts = shlex.split(line)
    except ValueError:
        return None
    if not parts or parts[0] not in CURRENT_KINDS:
        return None
    return _identity(parts[0], _key_values(parts[1:]))


def parse_v1_line(line: str) -> tuple[str, ...] | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("INCOMPLETE"):
        values = _regex_values(line)
        hint = re.match(r"^INCOMPLETE\s+UNRESOLVED\((.*?)\)", line)
        if hint and "field" not in values:
            values["field"] = hint.group(1).split(" blob locator", 1)[0]
        return _identity("INCOMPLETE", values)
    try:
        parts = shlex.split(line)
    except ValueError:
        return None
    if not parts or parts[0] not in {"MISMATCH", "PATH_MISSING", "NO_SCOPE", "UNCLASSIFIED"}:
        return None
    values = _key_values(parts[1:])
    # v1 rows used: KIND <field> path=<locator> [declared=...] [actual=...].
    if len(parts) > 1 and "=" not in parts[1]:
        values.setdefault("field", parts[1])
    if "path" in values:
        values.setdefault("locator", values["path"])
    return _identity(parts[0], values)


def read_v1(path: Path) -> list[tuple[str, ...]]:
    identities = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        identity = parse_v1_line(line)
        if identity is None:
            raise ValueError(f"cannot parse v1 baseline line {number}: {line}")
        identities.append(identity)
    return identities


def read_current(stdout: str, stderr: str) -> list[tuple[str, ...]]:
    combined = stdout + "\n" + stderr
    if re.search(r"(^|\n)INTERNAL_ERROR\b", combined):
        raise RuntimeError("checker emitted INTERNAL_ERROR")
    identities = []
    for line in stdout.splitlines():
        identity = parse_current_line(line)
        if identity is not None:
            identities.append(identity)
    if any(item[0] == "INCOMPLETE" for item in identities):
        raise RuntimeError("checker emitted INCOMPLETE identity")
    return identities


def resolve_v1_against_current(
    v1: list[tuple[str, ...]], current: list[tuple[str, ...]]
) -> list[tuple[str, ...]]:
    """Resolve legacy partial rows only when stable fields identify one current row."""
    resolved = []
    used: set[tuple[str, ...]] = set()
    for old in v1:
        kind, _manifest, _pin_id, field, _scope, locator = old
        if kind in {"MISMATCH", "PATH_MISSING", "NO_SCOPE", "UNCLASSIFIED"}:
            matches = [
                item for item in current
                if item[0] == kind and item[3] == field and item[5] == locator
                and item not in used
            ]
            if len(matches) == 1:
                resolved.append(matches[0])
                used.add(matches[0])
                continue
        resolved.append(old)
    return resolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--measurement-commit", required=True)
    parser.add_argument("--v1", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)

    if not HEX40.fullmatch(args.measurement_commit):
        parser.error("--measurement-commit must be a full lowercase 40-character SHA")
    root = Path(__file__).resolve().parents[2]
    checker = root / "scripts" / "ci" / "check_manifest_blob_pins.py"
    try:
        v1 = read_v1(args.v1)
        proc = subprocess.run(
            [sys.executable, str(checker), "--root", str(root),
             "--commit", args.measurement_commit],
            cwd=root, text=True, encoding="utf-8", errors="replace",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        current = read_current(proc.stdout, proc.stderr)
        if proc.returncode not in (0, 1):
            raise RuntimeError(f"checker exited {proc.returncode}")
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        print(f"baseline migration aborted: {exc}", file=sys.stderr)
        return 4

    v1_resolved = resolve_v1_against_current(v1, current)
    v1_set, current_set = set(v1_resolved), set(current)
    kept = sorted(v1_set & current_set)
    fixed = sorted(v1_set - current_set)
    added = sorted(current_set - v1_set)
    print(f"kept={len(kept)} fixed={len(fixed)} added={len(added)}")
    if added:
        print("added identities (not admitted to baseline):", file=sys.stderr)
        for identity in added:
            print(json.dumps(dict(zip(IDENTITY_FIELDS, identity)),
                             ensure_ascii=False, separators=(",", ":")), file=sys.stderr)
        return 3

    records = [dict(zip(IDENTITY_FIELDS, identity)) for identity in sorted(current_set)]
    statistics = {
        "v1_records": len(v1_set),
        "current_records": len(current_set),
        "kept": len(kept),
        "fixed": len(fixed),
        "added": len(added),
        "by_kind": {
            kind: sum(1 for record in records if record["kind"] == kind)
            for kind in sorted(CURRENT_KINDS)
        },
    }
    header = {
        "format": "manifest-blob-pin-v2",
        "identity_fields": list(IDENTITY_FIELDS),
        "measurement_commit": args.measurement_commit,
        "statistics": statistics,
    }
    output = [json.dumps(header, ensure_ascii=False, separators=(",", ":"))]
    output.extend(json.dumps(record, ensure_ascii=False, separators=(",", ":"))
                  for record in records)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(output) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
