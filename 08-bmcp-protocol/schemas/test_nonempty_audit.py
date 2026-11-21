#!/usr/bin/env python3
"""Guard schema non-empty constraints against the bilingual audit inventory.

Run from any working directory:
    python3 08-bmcp-protocol/schemas/test_nonempty_audit.py

The guard is intentionally conservative: every JSON Schema pattern is registered,
not only patterns that a small heuristic recognizes as non-empty.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parent
AUDIT = SCHEMA_DIR.parent / "schema-nonempty-audit.md"
CONSTRAINT_KEYS = ("minProperties", "minItems", "minLength")


def pointer(parts: list[str]) -> str:
    return "/" + "/".join(
        str(part).replace("~", "~0").replace("/", "~1") for part in parts
    )


def walk(node, parts=None):
    parts = [] if parts is None else parts
    if isinstance(node, dict):
        for key in CONSTRAINT_KEYS:
            if key in node:
                yield pointer(parts), f"{key}={node[key]}"
        if "pattern" in node:
            yield pointer(parts), f"pattern={node['pattern']}"
        for key, value in node.items():
            yield from walk(value, parts + [key])
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, parts + [str(index)])


def split_table_cells(line: str) -> list[str]:
    """Split a Markdown table row without treating pipes inside code spans as separators."""
    cells = []
    current = []
    in_code = False
    escaped = False
    for char in line.strip():
        if char == "`" and not escaped:
            in_code = not in_code
            current.append(char)
        elif char == "|" and not in_code and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == "\\\\" and not escaped
        if char != "\\\\":
            escaped = False
    cells.append("".join(current).strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "":
        cells.pop()
    return cells


def audit_entries():
    entries = set()
    if not AUDIT.is_file():
        raise FileNotFoundError(f"audit table not found: {AUDIT}")
    for line in AUDIT.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.replace("\\|", "|") for cell in split_table_cells(line)]
        if len(cells) < 3:
            continue
        schema_name = cells[0].strip("`")
        location = cells[1].strip("`")
        constraint = cells[2].strip("`")
        disposition = cells[4].strip("`") if len(cells) > 4 else ""
        if constraint.startswith(CONSTRAINT_KEYS) or constraint.startswith("pattern="):
            entries.add((schema_name, location, constraint))
    return entries


def main() -> int:
    import json

    registered = audit_entries()
    discovered = set()
    errors = []
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.name}:/:invalid JSON ({type(exc).__name__})")
            continue
        for location, constraint in walk(schema):
            item = (path.name, location, constraint)
            discovered.add(item)
            if item not in registered:
                errors.append(f"{path.name}:{location}:{constraint}")
    stale = sorted(registered - discovered)
    for schema_name, location, constraint in stale:
        errors.append(f"AUDIT_STALE:{schema_name}:{location}:{constraint}")
    if errors:
        print("\n".join(sorted(errors)))
        return 1
    print(
        f"OK: {len(list(SCHEMA_DIR.glob('*.json')))} schemas; "
        f"{len(discovered)} registered constraints; no unregistered or stale entries."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
