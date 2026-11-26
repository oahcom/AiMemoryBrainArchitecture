#!/usr/bin/env python3
"""Read-only lint for confusing Owner A-I, SYS-* and capability namespaces.

The scan is deliberately limited to the registered architecture entry-point
documents. It reports suspicious accountability constructions; it does not
infer ownership or rewrite documentation.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FILES = (
    "01-system-architecture/component-map.md",
    "01-system-architecture/responsibility-matrix.md",
    "docs/en/01-system-architecture/component-map.md",
    "docs/en/01-system-architecture/responsibility-matrix.md",
    "docs/zh-CN/01-system-architecture/component-map.md",
    "docs/zh-CN/01-system-architecture/responsibility-matrix.md",
)
CAPABILITIES = (
    "Domain Model", "Canonical Store", "Lifecycle", "Entity/Relation",
    "Ingestion", "Extraction", "Evidence", "Consolidation", "Retrieval",
    "Activation", "MCM", "Sync", "Governance", "Consistency",
)
CAPABILITY = r"(?:" + "|".join(re.escape(x) for x in CAPABILITIES) + r")"
SYS = r"SYS-[A-Z0-9]+(?:-[A-Z0-9]+)*"
PATTERNS = (
    ("SYS_ID_AS_OWNER", re.compile(
        rf"\bOwner\s+(?:ID\s+)?{SYS}\b|"
        rf"\b(?:primary|accountable|responsible)\s+Owner\s*[:=]\s*{SYS}\b|"
        rf"\b{SYS}\s+(?:is|acts? as)\s+(?:the\s+)?(?:Owner|primary owner|accountable owner)\b",
        re.IGNORECASE)),
    ("CAPABILITY_AS_OWNER", re.compile(
        rf"\bOwner\s+(?:ID\s+)?{CAPABILITY}\b|"
        rf"\b(?:primary|accountable|responsible)\s+Owner\s*[:=]\s*{CAPABILITY}\b|"
        rf"\b{CAPABILITY}\s+(?:is|acts? as)\s+(?:the\s+)?Owner\b",
        re.IGNORECASE)),
    ("BARE_LETTER_AS_OWNER", re.compile(
        r"\b([A-I])\s+(?:owns|is accountable for|is responsible for|has authority over)\b",
        re.IGNORECASE)),
)

def violations(text: str) -> list[tuple[int, str, str]]:
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        # Markdown code fences are examples, not live accountability claims.
        if line.lstrip().startswith("```"):
            continue
        for code, pattern in PATTERNS:
            match = pattern.search(line)
            if match:
                found.append((number, code, line.strip()))
                break
    return found

def check(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    for relative in FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"INCOMPLETE missing registered scan target: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"INCOMPLETE cannot read {relative}: {exc}")
            continue
        for line, code, excerpt in violations(text):
            errors.append(f"{relative}:{line}: {code}: {excerpt}")
    return (2 if any(x.startswith("INCOMPLETE") for x in errors) else 1 if errors else 0, errors)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="scan without modifying files")
    parser.add_argument("--root", type=Path, default=Path("."), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    code, errors = check(args.root.resolve())
    if errors:
        for item in errors:
            print(f"ERROR {item}", file=sys.stderr)
    else:
        print(f"OWNER NAMESPACE: PASS ({len(FILES)} registered documents scanned)")
    return code

if __name__ == "__main__":
    raise SystemExit(main())
