#!/usr/bin/env python3
"""Check the BMCP message index against schema message_type constraints.

Only const/enum constraints attached to a property named message_type are
counted. Other enums (Outcome, SideEffectStatus, status values, event names,
and prose/test strings) are intentionally ignored.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


TABLE_COLUMNS = 6
SCHEMA_REF_RE = re.compile(r"`(schemas/[^\`]+\.schema\.json)`")
LOCAL_PATH_RE = re.compile(r"\x60([^\x60]+)\x60")


def _pointer(parent: str, token: str | int) -> str:
    escaped = str(token).replace("~", "~0").replace("/", "~1")
    return f"{parent}/{escaped}"


def _message_type_values(node: Any, pointer: str):
    """Yield finite string values constrained by a message_type property."""
    if isinstance(node, dict):
        if "const" in node:
            value = node["const"]
            if isinstance(value, str):
                yield value, _pointer(pointer, "const")
        enum_values = node.get("enum")
        if isinstance(enum_values, list):
            for index, value in enumerate(enum_values):
                if isinstance(value, str):
                    yield value, _pointer(_pointer(pointer, "enum"), index)
        for key, child in node.items():
            if key in {"const", "enum"}:
                continue
            yield from _message_type_values(child, _pointer(pointer, key))
    elif isinstance(node, list):
        for index, child in enumerate(node):
            yield from _message_type_values(child, _pointer(pointer, index))


def extract_message_type_definitions(schema: Any) -> dict[str, set[str]]:
    """Return message type -> JSON Pointers of its const/enum constraints."""
    definitions: dict[str, set[str]] = defaultdict(set)

    def walk(node: Any, pointer: str = "") -> None:
        if isinstance(node, dict):
            for key, child in node.items():
                child_pointer = _pointer(pointer, key)
                if key == "message_type":
                    for value, constraint_pointer in _message_type_values(
                        child, child_pointer
                    ):
                        definitions[value].add(constraint_pointer)
                walk(child, child_pointer)
        elif isinstance(node, list):
            for index, child in enumerate(node):
                walk(child, _pointer(pointer, index))

    walk(schema)
    return dict(definitions)


def _index_rows(index_text: str):
    lines = index_text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == "## Message types")
    except StopIteration:
        return [], ["missing '## Message types' section"]

    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    rows = []
    errors = []
    for line_number, line in enumerate(lines[start + 1 : end], start + 2):
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and set(cells[0]) <= {"-", ":", " "}:
            continue
        if cells and cells[0].lower() in {"message type", "消息类型"}:
            continue
        if len(cells) != TABLE_COLUMNS:
            errors.append(
                f"line {line_number}: expected {TABLE_COLUMNS} table cells, got {len(cells)}"
            )
            continue
        match = re.fullmatch(r"`([^\`]+)`", cells[0])
        if not match:
            errors.append(f"line {line_number}: message type must be one backtick code span")
            continue
        rows.append(
            {
                "line": line_number,
                "message_type": match.group(1),
                "definition_source": cells[1],
                "schema_cell": cells[2],
                "schema_refs": SCHEMA_REF_RE.findall(cells[2]),
                "validator_cell": cells[3],
                "test_cell": cells[4],
            }
        )
    return rows, errors


def audit_repository(repository_root: Path) -> dict[str, Any]:
    protocol_root = repository_root / "08-bmcp-protocol"
    schema_dir = protocol_root / "schemas"
    index_path = protocol_root / "protocol-index.md"
    errors: list[str] = []
    definitions: dict[str, list[tuple[str, str]]] = defaultdict(list)
    schema_files = sorted(schema_dir.glob("*.json"))

    for schema_path in schema_files:
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"schema {schema_path.relative_to(repository_root).as_posix()}: {exc}")
            continue
        extracted = extract_message_type_definitions(schema)
        for message_type, pointers in extracted.items():
            for pointer in sorted(pointers):
                definitions[message_type].append(
                    (schema_path.relative_to(protocol_root).as_posix(), pointer)
                )

    try:
        index_text = index_path.read_text(encoding="utf-8")
    except OSError as exc:
        index_text = ""
        errors.append(f"cannot read index: {exc}")

    rows, row_errors = _index_rows(index_text)
    errors.extend(row_errors)
    row_by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    invalid_rows: list[str] = []

    for row in rows:
        message_type = row["message_type"]
        row_by_type[message_type].append(row)
        if not row["definition_source"]:
            invalid_rows.append(
                f"line {row['line']}: empty definition source for {message_type}"
            )
        for label, cell in (
            ("definition source", row["definition_source"]),
            ("validator", row["validator_cell"]),
            ("conformance test", row["test_cell"]),
        ):
            for artifact_ref in LOCAL_PATH_RE.findall(cell):
                if not artifact_ref.endswith((".md", ".py", ".json")):
                    continue
                if artifact_ref.startswith(("docs/", "08-bmcp-protocol/")):
                    artifact_path = repository_root / artifact_ref
                else:
                    artifact_path = protocol_root / artifact_ref
                if not artifact_path.is_file():
                    invalid_rows.append(
                        f"line {row['line']}: {label} path does not exist: {artifact_ref}"
                    )
        if not row["schema_refs"]:
            invalid_rows.append(
                f"line {row['line']}: no schemas/ path in Schema cell for {message_type}"
            )
            continue
        for schema_ref in row["schema_refs"]:
            if schema_ref.startswith("/") or ".." in Path(schema_ref).parts:
                invalid_rows.append(
                    f"line {row['line']}: unsafe schema path {schema_ref}"
                )
                continue
            schema_path = protocol_root / schema_ref
            if not schema_path.is_file():
                invalid_rows.append(
                    f"line {row['line']}: schema path does not exist: {schema_ref}"
                )
                continue
            try:
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                invalid_rows.append(
                    f"line {row['line']}: cannot parse {schema_ref}: {exc}"
                )
                continue
            if message_type not in extract_message_type_definitions(schema):
                invalid_rows.append(
                    f"line {row['line']}: {schema_ref} does not define message_type {message_type}"
                )

    duplicate_rows = {
        message_type: [row["line"] for row in matching]
        for message_type, matching in row_by_type.items()
        if len(matching) > 1
    }
    missing = sorted(set(definitions) - set(row_by_type))
    extra = sorted(set(row_by_type) - set(definitions))
    for message_type, line_numbers in duplicate_rows.items():
        errors.append(
            f"duplicate index row for {message_type} at lines {line_numbers}"
        )
    for message_type in missing:
        errors.append(f"schema message type missing from index: {message_type}")
    for message_type in extra:
        errors.append(f"index message type absent from schemas: {message_type}")
    errors.extend(invalid_rows)

    return {
        "schema_files": len(schema_files),
        "schemas_with_message_type": sum(
            1
            for schema_path in schema_files
            if _schema_has_message_type(schema_path)
        ),
        "unique_message_types": len(definitions),
        "index_rows": len(rows),
        "indexed_unique": len(row_by_type),
        "missing": missing,
        "extra": extra,
        "duplicate_rows": duplicate_rows,
        "invalid_rows": invalid_rows,
        "definitions": dict(definitions),
        "errors": errors,
    }


def _schema_has_message_type(schema_path: Path) -> bool:
    try:
        return bool(
            extract_message_type_definitions(
                json.loads(schema_path.read_text(encoding="utf-8"))
            )
        )
    except (OSError, json.JSONDecodeError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="repository root (defaults to this script's repository)",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="print every extracted message type and its schema JSON Pointers",
    )
    args = parser.parse_args()

    result = audit_repository(args.root.resolve())
    print(f"schema_files={result['schema_files']}")
    print(f"schemas_with_message_type={result['schemas_with_message_type']}")
    print(f"unique_message_types={result['unique_message_types']}")
    print(f"index_rows={result['index_rows']}")
    print(f"indexed_unique={result['indexed_unique']}")
    print(f"missing={len(result['missing'])}")
    print(f"extra={len(result['extra'])}")
    print(f"duplicate_types={len(result['duplicate_rows'])}")
    print(f"invalid_rows={len(result['invalid_rows'])}")

    if args.details:
        for message_type in sorted(result["definitions"]):
            refs = result["definitions"][message_type]
            print(f"TYPE {message_type}")
            for schema_path, pointer in refs:
                print(f"  {schema_path}#{pointer}")

    if result["errors"]:
        for error in result["errors"]:
            print(f"ERROR: {error}")
        print("FAIL")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
