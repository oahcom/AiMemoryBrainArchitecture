#!/usr/bin/env python3
"""Regression tests for AC4 Work Item manifest validation."""
from __future__ import annotations
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ci.check_work_item_manifest_schema import validate_text

REQUIRED = """work_item_id: AID-TEST
title: fixture
class: TEST
risk: R1
risk_rationale: fixture
status: DISPATCHED
id_status: PROVISIONAL
sponsor: test
accountable_owner: test
acceptance_authority: test
attribution: test
date: "2026-11-27"
repository:
  name: test/repo
base_branch: main
base_commit_sha: deadbeef
scope:
  objective: fixture
evidence: evidence.md
session_evidence:
  - role: TEST
    issue_refs:
      - "#266"
    implementing_ai_session: test
    session_evidence_ref: session-evidence.md
implementation:
  status: NOT_STARTED
  summary: fixture
  files_changed: []
  tests: []
"""

def run_cli_fixture(documentation: str, label: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        manifest = root / "14-ai-development/work-items/AID-TEST/manifest.yaml"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(REQUIRED + documentation, encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=root, check=True)
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/ci/check_work_item_manifest_schema.py"),
             "--root", str(root), "--tree", "HEAD"],
            cwd=ROOT, text=True, capture_output=True,
        )
        print(f"CHECKER FIXTURE {label}: exit={result.returncode}")
        print(result.stdout, end="")
        return result.returncode, result.stdout


def main() -> int:
    failures = 0
    empty_code, empty_output = run_cli_fixture("documentation: []\n", "documentation: []")
    if empty_code != 1 or "documentation must contain at least one reference" not in empty_output:
        failures += 1
    missing_code, missing_output = run_cli_fixture(
        "documentation:\n  - path: no/such/file.md\n    relationship: reference\n",
        "path no/such/file.md",
    )
    if missing_code != 1 or "documentation[0].path not in git tree: no/such/file.md" not in missing_output:
        failures += 1

    errors = validate_text(REQUIRED + "documentation: []\n", "empty.yaml",
                           {"session-evidence.md", "evidence.md"})
    print("FIXTURE documentation: []")
    print(f"  violations+{len(errors)}")
    for error in errors:
        print(f"  - {error}")
    if "documentation must contain at least one reference" not in errors:
        failures += 1

    missing = REQUIRED + """documentation:
  - path: no/such/file.md
    relationship: reference
"""
    errors = validate_text(missing, "missing.yaml", {"session-evidence.md", "evidence.md"})
    print("FIXTURE documentation: [{path: no/such/file.md}]")
    print(f"  violations+{len(errors)}")
    for error in errors:
        print(f"  - {error}")
    if "documentation[0].path not in git tree: no/such/file.md" not in errors:
        failures += 1

    tree = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD"],
                          cwd=ROOT, text=True, capture_output=True, check=True)
    paths = set(tree.stdout.splitlines())
    aid251 = ROOT / "14-ai-development/work-items/AID-2026-251/manifest.yaml"
    errors = validate_text(aid251.read_text(encoding="utf-8"), aid251.as_posix(), paths)
    if errors:
        print("AID-2026-251: NOT COMPLIANT")
        for error in errors:
            print(f"  - {error}")
        failures += 1
    else:
        print("AID-2026-251: COMPLIANT")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
