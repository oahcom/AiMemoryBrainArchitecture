#!/usr/bin/env python3
"""Validate work-item registry record fixtures against the canonical schema.

Layout: fixtures/<case>.yaml is one candidate record, fixtures/<case>.expected.json
is {"valid": bool, "reason": str}. Exit code 1 when any case disagrees.

Usage: python 00-governance/schemas/fixtures/run_fixtures.py
"""
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE.parent / "work-item-registry.schema.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

# Compiling the schema here doubles as the meta-schema check.
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)


def main() -> int:
    passed = failed = 0
    for record_path in sorted(HERE.glob("*.yaml")):
        case = record_path.stem
        expected = json.loads((HERE / f"{case}.expected.json").read_text(encoding="utf-8"))
        record = yaml.safe_load(record_path.read_text(encoding="utf-8"))
        errors = sorted(VALIDATOR.iter_errors(record), key=lambda e: list(e.path))
        actual = not errors
        if actual == expected["valid"]:
            passed += 1
            print(f"PASS {case}: valid={actual} - {expected['reason']}")
        else:
            failed += 1
            print(f"FAIL {case}: expected valid={expected['valid']}, got valid={actual} - {expected['reason']}")
            for err in errors[:3]:
                where = "/".join(map(str, err.absolute_path)) or "<root>"
                print(f"     {where}: {err.message}")
    print(f"\nPASS={passed} FAIL={failed} TOTAL={passed + failed}")
    print("ALL PASS" if failed == 0 else "FAILURES PRESENT")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
