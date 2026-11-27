#!/usr/bin/env python3
"""Validate REQ-01 signature fields in the four assessment documents."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ASSESSED_VERSION = "b372b62c640a2b656e54b6db62a4ee67d7d8c001"
FILES = (
    ("reviews/architecture/SYS-RISK-001.en.md", "R — Principal System-wide Architecture Risk Assessment"),
    ("reviews/architecture/SYS-RISK-001.zh-CN.md", "R — 首席全系统架构风险评估"),
    ("reviews/complexity/architecture-complexity-assessment.en.md", "X — Principal Architecture Complexity Assessment"),
    ("reviews/complexity/architecture-complexity-assessment.zh-CN.md", "X — 首席架构复杂度评估负责人"),
)
FIELDS = ("assessor", "assessed_version", "evidence_baseline")
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def _values(content: str, field: str) -> list[str]:
    pattern = re.compile(rf"^\s*-\s*{re.escape(field)}\s*:\s*(.*?)\s*$", re.MULTILINE)
    return [match.group(1).strip() for match in pattern.finditer(content)]


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        return value[1:-1]
    return value


def inspect(root: Path) -> list[str]:
    findings: list[str] = []
    for relative, expected_assessor in FILES:
        path = root / relative
        if not path.is_file():
            findings.append(f"FAIL {relative}: file missing")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            findings.append(f"FAIL {relative}: unable to read file ({type(exc).__name__})")
            continue
        if not content.strip():
            findings.append(f"FAIL {relative}: file is empty")
            continue
        expected_values = {
            "assessor": expected_assessor,
            "assessed_version": ASSESSED_VERSION,
            "evidence_baseline": f"main@{ASSESSED_VERSION}:{relative}",
        }
        failed = False
        for field in FIELDS:
            values = _values(content, field)
            if not values or not _unquote(values[0]):
                findings.append(f"FAIL {relative}: missing or empty {field}")
                failed = True
                continue
            if len(values) != 1:
                findings.append(f"FAIL {relative}: expected exactly one {field} field")
                failed = True
                continue
            actual = _unquote(values[0])
            if field == "assessed_version" and not SHA40.fullmatch(actual):
                findings.append(f"FAIL {relative}: assessed_version must be 40 lowercase hexadecimal characters")
                failed = True
            elif actual != expected_values[field]:
                findings.append(f"FAIL {relative}: {field} value does not match the required value")
                failed = True
        if not failed:
            findings.append(f"PASS {relative}: assessor, assessed_version, evidence_baseline")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    results = inspect(args.root)
    for result in results:
        print(result)
    failures = sum(result.startswith("FAIL ") for result in results)
    print(f"SUMMARY files={len(FILES)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
