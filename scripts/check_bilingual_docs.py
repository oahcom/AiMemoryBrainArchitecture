#!/usr/bin/env python3
"""Conservative bilingual documentation gate for pull requests.

This checks changed-file pairing and explicit PR declarations. It does not
claim semantic translation parity; that remains a reviewer responsibility.
"""
from __future__ import annotations

import os
from datetime import date
import subprocess
import sys
from pathlib import Path

NORMATIVE_ROOTS = {
    "00-governance", "01-system-architecture", "02-domain-model",
    "03-memory-brain", "04-memory-compiler", "05-memory-runtime",
    "06-memory-context", "07-agent-integration", "08-protocols",
    "09-storage-and-index", "10-security-and-governance",
    "11-consistency-and-recovery", "12-testing-and-acceptance",
    "13-engineering-decisions",
}
EXEMPT_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".drawio"}
# This normative policy intentionally contains both languages in one source file.
EMBEDDED_BILINGUAL_SOURCES = {"00-governance/bilingual-documentation-policy.md"}
ROOT = Path.cwd()


def changed_paths() -> set[str]:
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "")
    if not base or not head:
        raise RuntimeError("BASE_SHA and HEAD_SHA are required")
    raw = subprocess.check_output(
        ["git", "diff", "--name-only", f"{base}...{head}"],
        text=True,
    )
    return {line.strip() for line in raw.splitlines() if line.strip()}


def approved_exception(body: str) -> bool:
    if "BILINGUAL-EXCEPTION: APPROVED" not in body:
        return False
    labels = (
        "Exception Owner:", "Authoritative language/version:",
        "Missing counterpart path:", "Exact source revision:",
        "Due date (YYYY-MM-DD", "Tracking Issue/PR:",
        "Approval evidence",
    )
    values: dict[str, str] = {}
    lines = body.splitlines()
    for label in labels:
        value = ""
        for line in lines:
            if line.strip().startswith("- " + label):
                value = line.split(":", 1)[1].strip() if ":" in line else ""
                break
        values[label] = value
    if not all(values.values()):
        return False
    if any(value.upper() in {"TBD", "TODO", "N/A", "PENDING"} for value in values.values()):
        return False
    due = values["Due date (YYYY-MM-DD"][:10]
    try:
        date.fromisoformat(due)
    except ValueError:
        return False
    return True


def main() -> int:
    try:
        changed = changed_paths()
    except Exception as exc:
        print(f"::error::Unable to determine changed paths: {exc}")
        return 2

    body = os.environ.get("PR_BODY", "")
    errors: list[str] = []
    exception = approved_exception(body)
    complete = "BILINGUAL-MANIFEST: COMPLETE" in body

    # A language-pair change must update both sides in the same PR.
    for path in sorted(changed):
        if path.startswith("docs/en/"):
            counterpart = "docs/zh-CN/" + path[len("docs/en/"):]
            if counterpart not in changed and not exception:
                errors.append(f"{path} changed without paired change {counterpart}")
            if not (ROOT / counterpart).is_file() and not exception:
                errors.append(f"Chinese counterpart does not exist: {counterpart}")
        elif path.startswith("docs/zh-CN/"):
            counterpart = "docs/en/" + path[len("docs/zh-CN/"):]
            if counterpart not in changed and not exception:
                errors.append(f"{path} changed without paired change {counterpart}")
            if not (ROOT / counterpart).is_file() and not exception:
                errors.append(f"English counterpart does not exist: {counterpart}")

    bilingual_doc_changes = any(
        path.startswith("docs/en/") or path.startswith("docs/zh-CN/")
        or path in {"docs/README.md", "docs/translation-status.md"}
        for path in changed
    )
    if bilingual_doc_changes and not complete and not exception:
        errors.append(
            "Bilingual guide/spec files changed but PR body lacks the explicit "
            "COMPLETE manifest status or a fully documented approved exception."
        )

    # A normative source-spec change requires paired reader/spec documents
    # or a formally approved, time-bounded exception.
    normative_changes = []
    for path in sorted(changed):
        parts = Path(path).parts
        if len(parts) >= 2 and parts[0] in NORMATIVE_ROOTS:
            if Path(path).suffix.lower() in EXEMPT_SUFFIXES:
                continue
            if Path(path).suffix.lower() in {".md", ".yaml", ".yml", ".json", ".toml", ".proto"}:
                normative_changes.append(path)

    if normative_changes and not complete and not exception:
        errors.append(
            "Normative source files changed but PR body lacks "
            "'BILINGUAL-MANIFEST: COMPLETE' or a fully documented "
            "'BILINGUAL-EXCEPTION: APPROVED'."
        )

    if normative_changes and complete:
        for source in normative_changes:
            if source in EMBEDDED_BILINGUAL_SOURCES:
                continue
            en = f"docs/en/{source}"
            zh = f"docs/zh-CN/{source}"
            if en not in changed or zh not in changed:
                errors.append(
                    f"{source} requires both counterparts changed in this PR: {en}, {zh}"
                )
            if not (ROOT / en).is_file() or not (ROOT / zh).is_file():
                errors.append(
                    f"Both counterpart files must exist for {source}: {en}, {zh}"
                )

    if exception:
        print("Approved bilingual exception declaration detected; human governance approval remains mandatory.")
    if errors:
        for error in errors:
            print(f"::error::{error}")
        print("Bilingual documentation gate: FAIL")
        return 1

    print(f"Bilingual documentation gate: PASS ({len(changed)} changed paths inspected).")
    print("This is a structural gate only; semantic parity requires independent review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
