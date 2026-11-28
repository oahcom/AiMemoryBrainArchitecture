#!/usr/bin/env python3
"""Fail-closed validation for registered GOV-DOC source/mirror groups.

This module deliberately delegates metadata parsing and DM-12 semantics to
check_document_management.py. It does not implement a second YAML parser.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_document_management import (  # noqa: E402
    check_document,
    check_scope_and_relations,
    read_metadata,
)


def validate_group(root: Path, registered_files: tuple[str, ...]) -> list[str]:
    """Return FAIL_CLOSED diagnostics for any incomplete or invalid group."""
    root = root.resolve()
    errors: list[str] = []
    docs: dict[str, dict] = {}

    for relative in registered_files:
        path = root / relative

        if path.is_symlink():
            errors.append(
                f"FAIL_CLOSED: {relative}: registered document is a symlink"
            )
            continue

        if not path.is_file():
            errors.append(
                f"FAIL_CLOSED: {relative}: registered document is missing "
                "or is not a regular file"
            )
            continue

        parent = path.parent
        unsafe_parent = False
        while parent != root and root in parent.parents:
            if parent.is_symlink():
                unsafe_parent = True
                break
            parent = parent.parent

        if unsafe_parent:
            errors.append(
                f"FAIL_CLOSED: {relative}: document is reached through "
                "a symlinked parent"
            )
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(
                f"FAIL_CLOSED: {relative}: cannot read registered document: {exc}"
            )
            continue

        try:
            metadata = read_metadata(content)
        except Exception as exc:
            errors.append(
                f"FAIL_CLOSED: {relative}: metadata cannot be parsed: {exc}"
            )
            continue

        if metadata is None:
            errors.append(
                f"FAIL_CLOSED: {relative}: document exists but has no "
                "document_metadata classification"
            )
            continue

        document_errors, checked_metadata = check_document(
            path, content, root
        )
        if document_errors:
            for item in document_errors:
                errors.append(
                    f"FAIL_CLOSED: {relative}: document metadata invalid: {item}"
                )
            continue

        if checked_metadata is None:
            errors.append(
                f"FAIL_CLOSED: {relative}: document_metadata classification "
                "could not be established"
            )
            continue

        docs[relative] = checked_metadata

    # Do not run the graph check against an incomplete subset. Doing so could
    # hide a missing member by making its source relationship invisible.
    if len(docs) != len(registered_files):
        return errors

    # Existing DM-12 is the authority for source/mirror closure. Other DM
    # relationship rules are outside this helper's narrow AC3 contract.
    relation_errors = check_scope_and_relations(root, docs)
    for item in relation_errors:
        if item.startswith("DM-12 "):
            errors.append(f"FAIL_CLOSED: {item}")

    return errors


def report_group(root: Path, registered_files: tuple[str, ...]) -> int:
    """Print fail-closed diagnostics and return a process-compatible status."""
    errors = validate_group(root, registered_files)
    if errors:
        for item in errors:
            print(item, file=sys.stderr)
        return 1
    return 0
