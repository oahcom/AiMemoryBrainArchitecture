#!/usr/bin/env python3
"""Emit standalone raw rc/stderr transcripts for the three contract probes."""

import io
import tempfile
from contextlib import redirect_stderr
from pathlib import Path

import check_declared_check_contexts as checker

DOC = "14-ai-development/PR-GOVERNANCE-001.md"
WORKFLOW = """\
name: Example gates
on: pull_request
jobs:
  fmt:
    name: Rust format (hard gate)
    runs-on: ubuntu-latest
    steps:
      - run: true
  audit:
    runs-on: ubuntu-latest
    steps:
      - run: true
"""
DOC_TEXT = """\
# PR-GOVERNANCE-001

<!-- declared-check-contexts: read by scripts/check_declared_check_contexts.py -->
\x60\x60\x60text
Rust format (hard gate)
audit
\x60\x60\x60
"""


def fixture():
    root = Path(tempfile.mkdtemp())
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / "14-ai-development").mkdir(parents=True)
    (root / DOC).write_text(DOC_TEXT, encoding="utf-8")
    (root / ".github" / "workflows" / "gates.yml").write_text(WORKFLOW, encoding="utf-8")
    return root


def probe(label, expected, callback):
    errors = io.StringIO()
    with redirect_stderr(errors):
        rc = callback()
    raw = errors.getvalue()
    print(f"PROBE {label}: rc={rc}")
    print("stderr:")
    print(raw, end="" if raw.endswith("\n") else "\n")
    if rc != expected:
        raise SystemExit(f"probe {label}: expected rc={expected}, got {rc}")


root = fixture()
probe(
    "required-only injected payload",
    1,
    lambda: checker.main(root, ["Rust format (hard gate)", "audit", "Session Evidence"]),
)

root = fixture()
original = checker.fetch_protected_contexts
def unavailable(**_kwargs):
    raise OSError("connection refused")
checker.fetch_protected_contexts = unavailable
try:
    probe("fetch exception", 2, lambda: checker.main(root))
finally:
    checker.fetch_protected_contexts = original

root = fixture()
checker.fetch_protected_contexts = lambda **_kwargs: None
try:
    probe("fetch returns None", 2, lambda: checker.main(root))
finally:
    checker.fetch_protected_contexts = original
