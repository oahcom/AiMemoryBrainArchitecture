#!/usr/bin/env python3
"""Fail-closed validator for exact work-item status and independent gate evidence."""
import argparse
import json
import sys
from pathlib import Path

import yaml

PHASES = {
    "PROPOSED": "INTAKE",
    "ANALYZED": "INTAKE",
    "PROMPT_READY": "INTAKE",
    "READY": "READY",
    "IN_PROGRESS": "ACTIVE",
    "IMPLEMENTED": "ACTIVE",
    "VERIFIED": "VALIDATION",
    "REVIEWED": "VALIDATION",
    "INTEGRATION_READY": "VALIDATION",
    "ACCEPTED": "ACCEPTANCE",
    "MERGED": "COMPLETE",
    "CLOSED": "COMPLETE",
}
ORDER = (
    "verified",
    "independent_review",
    "integration",
    "owner_acceptance",
    "merge",
    "closeout",
)
REQUIRED = {
    "VERIFIED": 1,
    "REVIEWED": 2,
    "INTEGRATION_READY": 3,
    "ACCEPTED": 4,
    "MERGED": 5,
    "CLOSED": 6,
}


def check(path):
    data = yaml.safe_load(Path(path).read_bytes())
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a mapping")

    source = data.get("status")
    if not isinstance(source, str) or source not in PHASES:
        raise ValueError("status is not an exact canonical state")

    lifecycle = data.get("lifecycle")
    if not isinstance(lifecycle, dict):
        raise ValueError("missing/invalid lifecycle")
    if lifecycle.get("source_status") != source:
        raise ValueError("source_status mismatch; original status must remain exact")
    if lifecycle.get("phase") != PHASES[source]:
        raise ValueError("phase/status mapping mismatch")

    gates = lifecycle.get("gates")
    if not isinstance(gates, dict):
        raise ValueError("lifecycle.gates must be a mapping")

    required_count = REQUIRED.get(source, 0)
    for index, name in enumerate(ORDER):
        record = gates.get(name)
        if record is None:
            if index < required_count:
                raise ValueError("required gate record missing: " + name)
            continue
        if not isinstance(record, dict):
            raise ValueError("gate record must be a mapping: " + name)
        disposition = record.get("status")
        if disposition not in {"PASS", "NOT_RECORDED"}:
            raise ValueError("invalid gate disposition: " + name)
        if disposition == "PASS" and not record.get("evidence"):
            raise ValueError("PASS gate evidence reference missing: " + name)
        if index < required_count and disposition != "PASS":
            raise ValueError("gate not proven PASS: " + name)

    markers = lifecycle.get("markers", {})
    if not isinstance(markers, dict):
        raise ValueError("lifecycle.markers must be a mapping")

    return {"result": "PASS", "path": str(path), "phase": lifecycle["phase"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()

    failed = 0
    for name in args.paths:
        try:
            print(json.dumps(check(name), ensure_ascii=False))
        except Exception as error:
            failed += 1
            print(
                json.dumps(
                    {"result": "FAIL", "path": name, "error": str(error)},
                    ensure_ascii=False,
                )
            )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
