#!/usr/bin/env python3
"""Check three-way governance-operation authority traceability and mirror shape.

This is a read-only structural check. It does not approve policy or decide
whether a named authority is substantively correct.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from gov_doc_fail_closed import validate_group

FILES = (
    "01-system-architecture/system-boundaries.md",
    "docs/en/01-system-architecture/system-boundaries.md",
    "docs/zh-CN/01-system-architecture/system-boundaries.md",
)
HEADERS = {
    FILES[0]: ("Operation", "Policy / authorization authority", "Canonical-state authority", "Physical executor", "Minimum completion evidence / boundary"),
    FILES[1]: ("Operation", "Policy / authorization authority", "Canonical-state authority", "Physical executor", "Minimum completion evidence / boundary"),
    FILES[2]: ("操作", "策略/授权权威", "规范状态权威", "物理执行者", "最低完成证据/边界"),
}
EXPECTED_OPERATIONS = 7
EXPECTED_OPERATION_MARKERS = {
    FILES[0]: ("Authorization and revocation", "Retention and legal hold",
               "Logical Forget suppression / fence", "Physical erasure",
               "Backup expiry / deletion", "External-recipient deletion",
               "Global Forget Completion assessment"),
    FILES[1]: ("Authorization and revocation", "Retention and legal hold",
               "Logical Forget suppression / fence", "Physical erasure",
               "Backup expiry / deletion", "External-recipient deletion",
               "Global Forget Completion assessment"),
    FILES[2]: ("授权与撤销", "Retention 与 Legal Hold", "逻辑 Forget 抑制/围栏",
               "物理擦除", "备份到期/删除", "外部接收方删除",
               "Global Forget Completion 判定"),
}
FALSE_COMPLETION = (
    re.compile(r"\b(?:Forgotten state|D fence|canonical fence)\b.{0,100}\b(?:proves|means|confirms)\b.{0,40}\b(?:physical erasure|global completion)\b", re.I),
    re.compile(r"\bOwner\s+[DI]\b.{0,60}\b(?:may|can)\b.{0,30}\b(?:declare|claim)\b.{0,30}\bcompletion\b.{0,20}\balone\b", re.I),
    re.compile(r"Forgotten 状态.{0,40}(?:证明|意味着).{0,30}(?:物理擦除|全局完成)"),
    re.compile(r"Owner\s*[DI].{0,30}(?:可以|有权).{0,20}(?:单方面|独自).{0,20}(?:宣称|判定).{0,20}完成"),
)

UNASSIGNED_DECLARATION = re.compile(
    r"(?:^|[;；])\s*[`*_]*\s*(?:NOT_ASSIGNED\b|未分配|尚未分配)", re.I)

def is_unassigned(value: str) -> bool:
    """True only for an explicit unassigned declaration, not incidental prose.

    The register's traceability rule is "Where a role is not assigned, record
    `NOT_ASSIGNED` and keep the operation open". The declaration is the token
    standing on its own at the start of the cell or of a `;`-separated slot;
    prose that merely explains why this high-level document does not name the
    Owner (e.g. "... catalog Owner is not assigned by this high-level
    document", "本高层文档尚未分配负责该 Catalog 的 Owner") is a statement
    about the document, not a declaration, and must not trip the gate.
    """
    return bool(UNASSIGNED_DECLARATION.search(value))

def table_rows(text: str, expected_header: tuple[str, ...]) -> list[list[str]] | None:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if tuple(cells) != expected_header:
            continue
        rows = []
        for candidate in lines[index + 1:]:
            if not candidate.strip().startswith("|"):
                if rows:
                    break
                continue
            values = [part.strip() for part in candidate.strip().strip("|").split("|")]
            if values and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in values):
                continue
            if len(values) != 5:
                rows.append(values)
            else:
                rows.append(values)
        return rows
    return None

def check(
    root: Path,
    *,
    require_group_closure: bool = False,
) -> tuple[int, list[str]]:
    errors: list[str] = []
    row_counts: list[int] = []
    for relative in FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"INCOMPLETE missing registered mirror: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"INCOMPLETE cannot read {relative}: {exc}")
            continue
        rows = table_rows(text, HEADERS[relative])
        if rows is None:
            errors.append(f"{relative}: missing five-column governance authority register")
            row_counts.append(0)
            continue
        row_counts.append(len(rows))
        if len(rows) != EXPECTED_OPERATIONS:
            errors.append(f"{relative}: expected {EXPECTED_OPERATIONS} operations, found {len(rows)}")
        operation_names = [row[0] for row in rows if len(row) == 5]
        for marker in EXPECTED_OPERATION_MARKERS[relative]:
            if not any(marker.casefold() in name.casefold() for name in operation_names):
                errors.append(f"{relative}: missing expected governance operation: {marker}")
        for number, cells in enumerate(rows, 1):
            if len(cells) != 5:
                errors.append(f"{relative}: row {number} has {len(cells)} columns, expected 5")
                continue
            operation, policy, canonical, executor, evidence = cells
            for label, value in (
                ("operation", operation), ("policy authority", policy),
                ("canonical-state authority", canonical),
                ("physical executor", executor), ("completion evidence", evidence),
            ):
                if not value:
                    errors.append(f"{relative}: row {number} {label} is empty")
                elif is_unassigned(value):
                    errors.append(f"{relative}: row {number} {label} is unassigned; operation remains open")
            if policy and canonical and policy.casefold() == canonical.casefold():
                errors.append(f"{relative}: row {number} collapses policy and canonical-state authority into one entry")
            if executor and executor.casefold() in {policy.casefold(), canonical.casefold()}:
                errors.append(f"{relative}: row {number} collapses an authority role into the physical executor entry")
        for pattern in FALSE_COMPLETION:
            match = pattern.search(text)
            if match:
                errors.append(f"{relative}: false/unilateral completion assertion: {match.group(0)}")
    if len(row_counts) == len(FILES) and len(set(row_counts)) != 1:
        errors.append(f"bilingual mirror row-count mismatch: {row_counts}")
    # AC3 is mandatory for CI, but optional for legacy content-only fixtures.
    # The CI entry point enables it explicitly with --require-group-closure.
    if require_group_closure:
        errors.extend(validate_group(root, FILES))
    if errors:
        return (2 if any(x.startswith("INCOMPLETE") for x in errors) else 1, errors)
    return 0, []

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="scan without modifying files")
    parser.add_argument("--root", type=Path, default=Path("."), help=argparse.SUPPRESS)
    parser.add_argument(
        "--require-group-closure",
        action="store_true",
        help="fail closed unless all registered documents are classified and DM-12 closed",
    )
    args = parser.parse_args(argv)
    code, errors = check(
        args.root.resolve(),
        require_group_closure=args.require_group_closure,
    )
    if errors:
        for item in errors:
            print(f"ERROR {item}", file=sys.stderr)
    else:
        print(f"GOVERNANCE OPERATION TRACEABILITY: PASS ({EXPECTED_OPERATIONS} operations x 3 mirrors)")
    return code

if __name__ == "__main__":
    raise SystemExit(main())
