#!/usr/bin/env python3
"""Read-only, fail-closed REQ-01 assessment signature attachment checker."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECORDS = (
    "reviews/architecture/SYS-RISK-001.en.md",
    "reviews/architecture/SYS-RISK-001.zh-CN.md",
    "reviews/complexity/architecture-complexity-assessment.en.md",
    "reviews/complexity/architecture-complexity-assessment.zh-CN.md",
)
SHA40 = re.compile(r"^[0-9a-fA-F]{40}$")


def field(text: str, name: str) -> str | None:
    match = re.search(
        rf"(?im)^\s*(?:[-*]\s*)?{re.escape(name)}\s*:\s*(.*?)\s*$",
        text,
    )
    return match.group(1).strip().strip(chr(96) + "'\"") if match else None


def inspect(root: Path = ROOT) -> list[str]:
    findings: list[str] = []
    for relative in RECORDS:
        path = root / relative
        if not path.is_file():
            findings.append(f"FAIL {relative}: file missing")
            continue

        body = path.read_text(encoding="utf-8")
        values = {
            name: field(body, name)
            for name in ("assessor", "assessed_version", "evidence_baseline")
        }
        failed = False
        for name, value in values.items():
            if not value:
                findings.append(f"FAIL {relative}: missing or empty {name}")
                failed = True

        version = values["assessed_version"]
        if version and not SHA40.fullmatch(version):
            findings.append(
                f"FAIL {relative}: assessed_version must be a full 40-character hexadecimal commit"
            )
            failed = True

        if not failed:
            findings.append(
                f"PASS {relative}: assessor, assessed_version, evidence_baseline"
            )

    return findings


def main() -> int:
    results = inspect()
    for result in results:
        print(result)
    failures = sum(result.startswith("FAIL ") for result in results)
    print(f"SUMMARY records={len(RECORDS)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
