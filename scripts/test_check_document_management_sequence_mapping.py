#!/usr/bin/env python3
"""Regression: GOV-DOC YAML subset accepts flat sequence-of-mapping records."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from check_document_management import ParseError, parse_yaml_subset, read_metadata

YAML = """documentation:
  - path: docs/architecture.md
    relationship: normative
  - path: scripts/check.py
    relationship: code
"""
FRONTMATTER = """---
document_metadata:
  domain: ai-development
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
      evidence_reference:
        - "AID-2026-251/evidence.md"
        - "Issue #266"
    usage_status: Active
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
---
# Test
"""

def main() -> int:
    expected = [
        {"path": "docs/architecture.md", "relationship": "normative"},
        {"path": "scripts/check.py", "relationship": "code"},
    ]
    assert parse_yaml_subset(YAML)["documentation"] == expected
    metadata = read_metadata(FRONTMATTER)
    assert metadata is not None
    assert metadata["lifecycle"]["approval"]["evidence_reference"] == [
        "AID-2026-251/evidence.md", "Issue #266"
    ]
    print("PASS: parse_yaml_subset sequence-of-mapping fixture -> 2 mappings")
    print("PASS: read_metadata nested sequence-of-mapping remains parseable")
    try:
        parse_yaml_subset("items:\n  - name: nested\n    child:\n      value: rejected\n")
    except ParseError:
        print("PASS: nested mappings inside sequence items remain rejected")
    else:
        print("FAIL: nested mapping unexpectedly accepted")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
