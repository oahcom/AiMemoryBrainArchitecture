#!/usr/bin/env python3
"""Guard the bilingual inventory of schema constraints that reject empty values."""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

SCHEMA_DIR = Path(__file__).resolve().parent
AUDIT = SCHEMA_DIR.parent / "schema-nonempty-audit.md"
CONSTRAINT_KEYS = ("minProperties", "minItems", "minLength")


def pointer(parts: list[str]) -> str:
    return "/" + "/".join(
        str(part).replace("~", "~0").replace("/", "~1") for part in parts
    )


def is_nonempty_constraint(key: str, value) -> bool:
    if key in ("minLength", "minItems", "minProperties"):
        return isinstance(value, (int, float)) and value > 0
    if key == "pattern":
        try:
            # JSON Schema pattern uses search semantics. If the expression
            # cannot match the empty string, it also excludes an empty value.
            return re.search(value, "") is None
        except re.error:
            # Stay conservative: an unparseable pattern must still be audited.
            return True
    return False


def walk(node, parts=None):
    parts = [] if parts is None else parts
    if isinstance(node, dict):
        for key in CONSTRAINT_KEYS:
            if key in node and is_nonempty_constraint(key, node[key]):
                yield pointer(parts), f"{key}={node[key]}"
        if "pattern" in node and is_nonempty_constraint("pattern", node["pattern"]):
            yield pointer(parts), f"pattern={node['pattern']}"
        for key, value in node.items():
            yield from walk(value, parts + [key])
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, parts + [str(index)])


def split_table_cells(line: str) -> list[str]:
    """Split a Markdown table row without splitting escaped pipes or code spans."""
    cells = []
    current = []
    in_code = False
    escaped = False
    for char in line.strip():
        if char == chr(96) and not escaped:
            in_code = not in_code
            current.append(char)
        elif char == "|" and not in_code and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    cells.append("".join(current).strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "":
        cells.pop()
    return cells


def audit_entries(audit_path: Path):
    entries = set()
    if not audit_path.is_file():
        raise FileNotFoundError(f"audit table not found: {audit_path}")
    for line in audit_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.replace("\\|", "|") for cell in split_table_cells(line)]
        if len(cells) < 3:
            continue
        schema_name = cells[0].strip(chr(96))
        location = cells[1].strip(chr(96))
        constraint = cells[2].strip(chr(96))
        if constraint.startswith(CONSTRAINT_KEYS) or constraint.startswith("pattern="):
            entries.add((schema_name, location, constraint))
    return entries


def validate_inventory(schema_dir: Path, audit_path: Path):
    registered = audit_entries(audit_path)
    discovered = set()
    errors = []
    schema_files = sorted(schema_dir.glob("*.json"))
    for path in schema_files:
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
    for schema_name, location, constraint in sorted(registered - discovered):
        errors.append(f"AUDIT_STALE:{schema_name}:{location}:{constraint}")
    return errors, discovered, registered, schema_files


class AuditInventoryTests(unittest.TestCase):
    def _fixture(self, schema_text: str, audit_text: str):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        schema_dir = root / "schemas"
        schema_dir.mkdir()
        (schema_dir / "sample.schema.json").write_text(schema_text, encoding="utf-8")
        audit = root / "audit.md"
        audit.write_text(audit_text, encoding="utf-8")
        return tmp, schema_dir, audit

    def test_detects_unregistered_constraint_added(self):
        tmp, schema_dir, audit = self._fixture(
            '{"type":"string","minLength":1}',
            "| schema | location | constraint | status | rationale |\n",
        )
        with tmp:
            errors, _, _, _ = validate_inventory(schema_dir, audit)
        self.assertTrue(any("minLength=1" in error for error in errors))

    def test_detects_stale_registration_after_schema_constraint_removed(self):
        # The schema no longer has minLength=1, but the audit still registers it.
        # This is the reverse direction: stale audit data must fail the guard.
        tmp, schema_dir, audit = self._fixture(
            '{"type":"string"}',
            "| sample.schema.json | / | minLength=1 | Retain | A string ID cannot be empty. |\n",
        )
        with tmp:
            errors, _, _, _ = validate_inventory(schema_dir, audit)
        self.assertIn(
            "AUDIT_STALE:sample.schema.json:/:minLength=1",
            errors,
        )

    def test_zero_min_items_is_not_a_nonempty_constraint(self):
        tmp, schema_dir, audit = self._fixture(
            '{"type":"array","minItems":0}',
            "| schema | location | constraint | status | rationale |\n",
        )
        with tmp:
            errors, discovered, _, _ = validate_inventory(schema_dir, audit)
        self.assertEqual(errors, [])
        self.assertEqual(discovered, set())


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AuditInventoryTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    errors, discovered, registered, schema_files = validate_inventory(SCHEMA_DIR, AUDIT)
    if errors:
        print("\n".join(sorted(errors)))
    else:
        print(
            f"OK: {len(schema_files)} schemas; {len(discovered)} non-empty constraints "
            "registered; no unregistered or stale entries."
        )
    return 0 if result.wasSuccessful() and not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
