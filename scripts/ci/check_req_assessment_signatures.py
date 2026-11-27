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
    m = re.search(rf"(?im)^\s*(?:[-*]\s*)?{re.escape(name)}\s*:\s*(.*?)\s*$", text)
    return m.group(1).strip().strip("`'\"") if m else None

def inspect(root: Path = ROOT) -> list[str]:
    out = []
    for rel in RECORDS:
        path = root / rel
        if not path.is_file():
            out.append(f"FAIL {rel}: file missing")
            continue
        body = path.read_text(encoding="utf-8")
        vals = {k: field(body, k) for k in ("Assessor", "assessed_version", "evidence_baseline")}
        bad = False
        for k, v in vals.items():
            if not v:
                out.append(f"FAIL {rel}: missing or empty {k}")
                bad = True
        version = vals["assessed_version"]
        if version and not SHA40.fullmatch(version):
            out.append(f"FAIL {rel}: assessed_version must be a full 40-character hexadecimal commit")
            bad = True
        if not bad:
            out.append(f"PASS {rel}: Assessor, assessed_version, evidence_baseline")
    return out

def main() -> int:
    results = inspect()
    print("\n".join(results))
    failures = sum(x.startswith("FAIL ") for x in results)
    print(f"SUMMARY records={len(RECORDS)} failures={failures}")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
