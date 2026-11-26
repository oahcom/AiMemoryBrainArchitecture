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
    "01-system-architecture/component-interactions.md",
    "01-system-architecture/data-flows.md",
    "docs/en/01-system-architecture/component-interactions.md",
    "docs/en/01-system-architecture/data-flows.md",
    "docs/zh-CN/01-system-architecture/component-interactions.md",
    "docs/zh-CN/01-system-architecture/data-flows.md",
    "01-system-architecture/system-boundaries.md",
    "docs/en/01-system-architecture/system-boundaries.md",
    "docs/zh-CN/01-system-architecture/system-boundaries.md",
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
        r"(?<!Owner )\b([A-I])\s+(?:owns|is accountable for|is responsible for|has authority over)\b")),
)

def violations(text: str) -> list[tuple[int, str, str]]:
    found = []
    in_fence = False
    owner_columns: list[int] = []
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(chr(96) * 3):
            in_fence = not in_fence
            owner_columns = []
            continue
        if in_fence:
            continue
        if line.lstrip().startswith('|'):
            cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
            if any('owner' in cell.casefold() for cell in cells):
                owner_columns = [index for index, cell in enumerate(cells) if 'owner' in cell.casefold()]
                continue
            if owner_columns:
                for index in owner_columns:
                    if index >= len(cells):
                        continue
                    value = cells[index]
                    if re.search(r'\bSYS-[A-Z0-9]+(?:-[A-Z0-9]+)*\b', value):
                        found.append((number, 'SYS_ID_AS_OWNER', line.strip()))
                        break
                    if re.fullmatch(CAPABILITY, value, re.IGNORECASE):
                        found.append((number, 'CAPABILITY_AS_OWNER', line.strip()))
                        break
                continue
        else:
            owner_columns = []
        for code, pattern in PATTERNS:
            if code == 'BARE_LETTER_AS_OWNER' and '|' in line:
                continue
            if pattern.search(line):
                found.append((number, code, line.strip()))
                break
    return found

def mirror_signature(text: str) -> tuple[int, int, frozenset[str]]:
    """Language-neutral shape: table rows, formal Owner citations, SYS IDs."""
    table_rows = sum(1 for line in text.splitlines() if line.lstrip().startswith("|"))
    owner_refs = len(re.findall(r"\bOwner [A-I]\b", text))
    sys_ids = frozenset(re.findall(r"\bSYS-(?:MEMORY-BRAIN|MEMORY-COMPILER|MEMORY-RUNTIME|CROSS-CUTTING)\b", text))
    return table_rows, owner_refs, sys_ids

def check(root: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    contents: dict[str, str] = {}
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
        contents[relative] = text
        for line, code, excerpt in violations(text):
            errors.append(f"{relative}:{line}: {code}: {excerpt}")
    # Root, EN and ZH-CN versions must preserve the same structural inventory.
    for stem in ("component-map.md", "responsibility-matrix.md",
                 "component-interactions.md", "data-flows.md", "system-boundaries.md"):
        group = [
            f"01-system-architecture/{stem}",
            f"docs/en/01-system-architecture/{stem}",
            f"docs/zh-CN/01-system-architecture/{stem}",
        ]
        if all(path in contents for path in group):
            signatures = [mirror_signature(contents[path]) for path in group]
            # Table/Owner counts are stable across translations. SYS identifiers
            # are checked as a set only for the Component Map, where they are
            # the subsystem namespace itself.
            if len({(sig[0], sig[1]) for sig in signatures}) != 1:
                errors.append(f"bilingual structural drift for {stem}: table/Owner signature differs")
            if stem == "component-map.md" and len({sig[2] for sig in signatures}) != 1:
                errors.append("bilingual SYS-* subsystem inventory drift in component-map.md")
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
