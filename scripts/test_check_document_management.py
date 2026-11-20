#!/usr/bin/env python3
"""Self-check for scripts/check_document_management.py.

Runs the gate against inline fixtures. No framework, no files on disk.

    python scripts/test_check_document_management.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_document_management import check_document  # noqa: E402


def doc(body: str) -> str:
    return f"---\ndocument_metadata:\n{body}\n---\n\n# Title\n"


BASE = """
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
"""

APPROVED_NO_BINDING = BASE.replace("decision_status: Draft", "decision_status: Approved")

REVOKED_NO_ID = BASE.replace(
    "decision_status: Draft", "decision_status: Revoked"
).replace("      decision_status: Revoked", "      decision_status: Revoked\n      revocation: null")

CANONICAL_OK = BASE.replace(
    "canonical_status: Non-Canonical",
    "canonical_status: Canonical\n"
    "    canonical_scope: \"Architecture: Data Model Design\"\n"
    "    canonical_scope_id: architecture/data-model-design\n"
    "    canonical_scope_keywords:\n      - data-model",
)

CANONICAL_BAD_SCOPE_ID = CANONICAL_OK.replace(
    "architecture/data-model-design", "Architecture Data Model"
)

CANONICAL_NO_KEYWORDS = CANONICAL_OK.replace(
    "    canonical_scope_keywords:\n      - data-model", ""
)

HAND_WRITTEN_REVERSE = BASE.replace(
    "  lifecycle:\n    approval:",
    "  lifecycle:\n    supersession:\n      superseded_by:\n        - docs/x.md\n    approval:",
)

ARCHIVED_NO_REASON = BASE.replace(
    "usage_status: Active",
    "usage_status: Archived\n    archival:\n      archived_date: \"2026-01-01\"",
)

BAD_DOMAIN = BASE.replace("domain: architecture", "domain: misc")

NO_METADATA = "---\ntitle: something\n---\n\n# Title\n"

FILE = Path("synthetic.md")


def run(name: str, text: str, expect_error: bool, needle: str = ""):
    errors, _ = check_document(FILE, text)
    hit = any(needle in e for e in errors) if needle else bool(errors)
    ok = hit == expect_error
    status = "ok  " if ok else "FAIL"
    detail = ""
    if not ok:
        detail = f"  expected={'error' if expect_error else 'clean'} got={errors}"
    print(f"  [{status}] {name}{detail}")
    return ok


def main() -> int:
    print("check_document_management self-check")
    results = [
        run("baseline conforms", doc(BASE), False),
        run("missing metadata is adoption gap, not error", NO_METADATA, False),
        run("bad domain rejected", doc(BAD_DOMAIN), True, "DM-02 domain"),
        run("Approved without version rejected", doc(APPROVED_NO_BINDING), True, "DM-03"),
        run("Revoked without decision id rejected", doc(REVOKED_NO_ID), True, "DM-04"),
        run("Canonical with scope conforms", doc(CANONICAL_OK), False),
        run("Canonical with unnormalized scope id rejected",
            doc(CANONICAL_BAD_SCOPE_ID), True, "DM-06"),
        run("Canonical without keywords rejected",
            doc(CANONICAL_NO_KEYWORDS), True, "DM-06"),
        run("hand-written superseded_by rejected",
            doc(HAND_WRITTEN_REVERSE), True, "DM-08"),
        run("Archived without reason rejected", doc(ARCHIVED_NO_REASON), True, "DM-05"),
    ]
    passed = sum(results)
    total = len(results)
    passed += run_scope_conflict()
    total += 1
    print(f"{passed}/{total} passed")
    return 0 if passed == total else 1


def run_scope_conflict() -> int:
    """DM-07: two Canonical documents claiming one scope must be rejected."""
    import tempfile

    from check_document_management import main as gate_main

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        gov = root / "00-governance"
        gov.mkdir()
        for name in ("a.md", "b.md"):
            (gov / name).write_text(doc(CANONICAL_OK), encoding="utf-8")
        import sys as _sys

        argv = _sys.argv
        _sys.argv = ["gate", "--root", tmp]
        try:
            code = gate_main()
        finally:
            _sys.argv = argv
        ok = code == 1
        print(f"  [{'ok  ' if ok else 'FAIL'}] duplicate Canonical scope rejected (DM-07)"
              + ("" if ok else f"  gate returned {code}, expected 1"))
        return 1 if ok else 0


if __name__ == "__main__":
    sys.exit(main())
