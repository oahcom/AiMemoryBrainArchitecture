#!/usr/bin/env python3
"""Regression tests for legacy and schema-driven Work Item manifest validation."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.ci.check_work_item_manifest_schema import (
    SCHEMA_PATH,
    GitOutputDecodeError,
    git_show,
    run_git_utf8,
    validate_text,
    finding_id,
    finding_identity,
    validate_ledger,
    generate_ledger,
    LEDGER_PLACEHOLDERS,
)


CHECKER = ROOT / "scripts/ci/check_work_item_manifest_schema.py"
SCHEMA_FILE = ROOT / SCHEMA_PATH

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
documentation:
  - path: evidence.md
    relationship: evidence
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

SCHEMA_TEXT = SCHEMA_FILE.read_text(encoding="utf-8")


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"git {' '.join(args)} failed ({result.returncode}): {result.stderr}"
        )
    return result.stdout.strip()


def init_repo(root: Path) -> None:
    git(root, "init", "-q")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "user.name", "Fixture")


def write_fixture(
    root: Path,
    *,
    manifest: str = REQUIRED,
    schema: str = SCHEMA_TEXT,
) -> None:
    manifest_path = root / "14-ai-development/work-items/AID-TEST/manifest.yaml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(manifest, encoding="utf-8")
    schema_path = root / SCHEMA_PATH
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path.write_text(schema, encoding="utf-8")
    (root / "evidence.md").write_text("fixture evidence\n", encoding="utf-8")
    (root / "session-evidence.md").write_text("fixture session evidence\n", encoding="utf-8")


def commit_all(root: Path, message: str = "fixture") -> str:
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD")


def run_checker(root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root), "--tree", "HEAD", *extra],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        check=False,
    )


class LegacyCompatibilityTests(unittest.TestCase):
    def test_empty_documentation_legacy_fixture(self):
        errors = validate_text(
            REQUIRED.replace(
                "documentation:\n  - path: evidence.md\n    relationship: evidence\n",
                "documentation: []\n",
            ),
            "empty.yaml",
            {"evidence.md", "session-evidence.md"},
        )
        self.assertIn("documentation must contain at least one reference", errors)

    def test_missing_documentation_path_legacy_fixture(self):
        content = REQUIRED.replace("path: evidence.md", "path: no/such/file.md")
        errors = validate_text(
            content, "missing.yaml", {"evidence.md", "session-evidence.md"},
        )
        self.assertIn("documentation[0].path not in git tree: no/such/file.md", errors)

    def test_existing_ci_invocation_remains_available(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root)
            init_repo(root)
            commit_all(root)
            baseline_path = root / "baseline.json"
            baseline_path.write_text(
                json.dumps({"baseline_tree": "HEAD", "cohort_tree": "HEAD"}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable, str(CHECKER), "--root", str(root),
                    "--tree", "HEAD", "--baseline", str(baseline_path),
                ],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                errors="strict", check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Manifest schema v2:", result.stdout)

    def test_batch_report_remains_available_for_83_manifest_cohort(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            for index in range(83):
                rel = (
                    root / "14-ai-development/work-items"
                    / f"AID-TEST-{index:03d}" / "manifest.yaml"
                )
                rel.parent.mkdir(parents=True, exist_ok=True)
                rel.write_text(REQUIRED, encoding="utf-8")
            (root / "evidence.md").write_text("evidence\n", encoding="utf-8")
            (root / "session-evidence.md").write_text("session\n", encoding="utf-8")
            commit_all(root)
            baseline_path = root / "baseline.json"
            baseline_path.write_text(
                json.dumps({"baseline_tree": "HEAD", "cohort_tree": "HEAD"}),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable, str(CHECKER), "--root", str(root),
                    "--tree", "HEAD", "--baseline", str(baseline_path),
                    "--batch-report",
                ],
                cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                errors="strict", check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("batch 1/4", result.stdout)
            self.assertIn("batch 4/4", result.stdout)


class FullTreeValidationTests(unittest.TestCase):
    def make_repo(self, root: Path, *, manifest: str = REQUIRED, schema: str = SCHEMA_TEXT):
        init_repo(root)
        write_fixture(root, manifest=manifest, schema=schema)
        commit_all(root)

    def test_full_tree_valid_manifest_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            result = run_checker(root, "--all-manifests", "--schema-driven", "--strict", "--report")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["population"], "ALL_DISCOVERED_MANIFESTS")
            self.assertEqual(report["discovered"], 1)
            self.assertEqual(report["validated"], 1)
            self.assertEqual(report["incomplete"], 0)
            self.assertEqual(report["ac4_violations"], 0)
            self.assertEqual(report["other_schema_violations"], 0)
            self.assertEqual(report["manifests"][0]["status"], "PASS")

    def test_full_tree_finds_manifest_outside_legacy_cohort(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = REQUIRED.replace("relationship: evidence", "relationship: invalid-relationship")
            self.make_repo(root, manifest=manifest)
            result = run_checker(root, "--all-manifests", "--schema-driven", "--strict", "--report")
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["discovered"], 1)
            self.assertEqual(report["validated"], 1)
            self.assertGreater(report["ac4_violations"], 0)
            self.assertEqual(report["manifests"][0]["status"], "VIOLATION")
            self.assertTrue(any(
                f["rule_id"] == "documentation.relationship.enum"
                for f in report["manifests"][0]["findings"]
            ))

    def test_schema_enum_mutation_changes_validation_without_checker_edit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mutated_schema = SCHEMA_TEXT.replace("      - NOT_STARTED\n", "")
            self.assertNotEqual(mutated_schema, SCHEMA_TEXT)
            self.make_repo(root, schema=mutated_schema)
            result = run_checker(root, "--all-manifests", "--schema-driven", "--strict", "--report")
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            rule_ids = {f["rule_id"] for f in report["manifests"][0]["findings"]}
            self.assertIn("implementation.status.enum", rule_ids)

    def test_unknown_schema_keyword_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mutated_schema = SCHEMA_TEXT.replace(
                'schema_version: "2"',
                'schema_version: "2"\nunsupported_future_keyword: true',
            )
            self.make_repo(root, schema=mutated_schema)
            result = run_checker(root, "--all-manifests", "--schema-driven", "--strict", "--report")
            self.assertEqual(result.returncode, 2)
            self.assertIn("schema configuration invalid", result.stderr)
            self.assertIn("unsupported schema root keyword", result.stderr)

    def test_malformed_yaml_is_reported_as_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, manifest=REQUIRED + "documentation: [\n")
            result = run_checker(root, "--all-manifests", "--schema-driven", "--strict", "--report")
            self.assertEqual(result.returncode, 2, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["parse_errors"], 1)
            self.assertEqual(report["incomplete"], 1)
            self.assertEqual(report["manifests"][0]["status"], "PARSE_ERROR")

    def test_duplicate_yaml_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root, manifest=REQUIRED + "title: duplicate\n")
            result = run_checker(root, "--all-manifests", "--schema-driven", "--strict", "--report")
            self.assertEqual(result.returncode, 2, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["parse_errors"], 1)
            self.assertIn("duplicate key", report["manifests"][0]["error"])

    def test_git_tree_is_used_instead_of_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_repo(root)
            manifest_path = root / "14-ai-development/work-items/AID-TEST/manifest.yaml"
            manifest_path.write_text(
                REQUIRED.replace("relationship: evidence", "relationship: invalid-worktree-only"),
                encoding="utf-8",
            )
            untracked = root / "14-ai-development/work-items/AID-UNTRACKED/manifest.yaml"
            untracked.parent.mkdir(parents=True)
            untracked.write_text(REQUIRED, encoding="utf-8")
            result = run_checker(root, "--all-manifests", "--schema-driven", "--strict", "--report")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["discovered"], 1)
            self.assertEqual(report["validated"], 1)
            self.assertEqual(report["manifests"][0]["status"], "PASS")

    def test_baseline_cannot_suppress_strict_full_tree_violations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = REQUIRED.replace("relationship: evidence", "relationship: invalid")
            self.make_repo(root, manifest=invalid)
            result = run_checker(
                root, "--all-manifests", "--schema-driven", "--strict", "--report",
                "--baseline", "some-baseline.json",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--baseline is not accepted", result.stderr)

    def test_report_has_one_result_for_every_discovered_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            schema_path = root / SCHEMA_PATH
            schema_path.parent.mkdir(parents=True, exist_ok=True)
            schema_path.write_bytes(SCHEMA_FILE.read_bytes())
            for index in range(3):
                manifest_path = (
                    root / "14-ai-development/work-items"
                    / f"AID-TEST-{index}" / "manifest.yaml"
                )
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                content = REQUIRED
                if index == 1:
                    content = content.replace("relationship: evidence", "relationship: invalid")
                if index == 2:
                    content = content.replace("status: NOT_STARTED", "status: UNKNOWN")
                manifest_path.write_text(content, encoding="utf-8")
            (root / "evidence.md").write_text("evidence\n", encoding="utf-8")
            (root / "session-evidence.md").write_text("session\n", encoding="utf-8")
            commit_all(root)
            result = run_checker(root, "--all-manifests", "--schema-driven", "--report")
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["discovered"], 3)
            self.assertEqual(len(report["manifests"]), 3)
            self.assertEqual(report["validated"] + report["incomplete"], report["discovered"])
            self.assertEqual(
                sum(len(item["findings"]) for item in report["manifests"]),
                report["ac4_violations"] + report["other_schema_violations"],
            )

    def test_combined_ac4_and_other_schema_findings_are_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = REQUIRED.replace(
                "relationship: evidence", "relationship: invalid",
            ).replace("status: NOT_STARTED", "status: INVALID_STATUS")
            self.make_repo(root, manifest=invalid)
            result = run_checker(root, "--all-manifests", "--schema-driven", "--strict", "--report")
            self.assertEqual(result.returncode, 1, result.stderr)
            report = json.loads(result.stdout)
            self.assertGreater(report["ac4_violations"], 0)
            self.assertGreater(report["other_schema_violations"], 0)
            categories = {f["category"] for f in report["manifests"][0]["findings"]}
            self.assertEqual(categories, {"AC4", "OTHER_SCHEMA"})

    def test_schema_driven_options_require_all_manifests(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_checker(Path(directory), "--schema-driven")
            self.assertEqual(result.returncode, 2)
            self.assertIn("require --all-manifests", result.stderr)


class GitEncodingTests(unittest.TestCase):
    def test_git_output_uses_strict_utf8(self):
        with mock.patch("scripts.ci.check_work_item_manifest_schema.subprocess.run") as mocked:
            mocked.return_value = subprocess.CompletedProcess(
                args=["git", "show"], returncode=0,
                stdout=b"valid utf-8 \xe2\x9c\x93", stderr=b"",
            )
            self.assertEqual(run_git_utf8(["git", "show"], ROOT), "valid utf-8 \u2713")

    def test_invalid_git_stdout_raises_decode_error(self):
        with mock.patch("scripts.ci.check_work_item_manifest_schema.subprocess.run") as mocked:
            mocked.return_value = subprocess.CompletedProcess(
                args=["git", "show"], returncode=0, stdout=b"\xff\xfe", stderr=b"",
            )
            with self.assertRaises(GitOutputDecodeError):
                run_git_utf8(["git", "show"], ROOT)

    def test_git_stderr_is_decoded_for_diagnostics(self):
        with mock.patch("scripts.ci.check_work_item_manifest_schema.subprocess.run") as mocked:
            mocked.return_value = subprocess.CompletedProcess(
                args=["git", "show"], returncode=1, stdout=b"",
                stderr=b"failure \xff",
            )
            with self.assertRaises(Exception) as raised:
                run_git_utf8(["git", "show"], ROOT)
            self.assertIn("failure", str(raised.exception))

    def test_git_show_invalid_utf8_blob_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            init_repo(root)
            path = root / "14-ai-development/work-items/AID-TEST/manifest.yaml"
            path.parent.mkdir(parents=True)
            path.write_bytes(b"title: \xff\n")
            commit_all(root)
            with self.assertRaises(GitOutputDecodeError):
                git_show(root, "HEAD", "14-ai-development/work-items/AID-TEST/manifest.yaml")


class LegacyLedgerTests(unittest.TestCase):
    def _identity(self, path="14-ai-development/work-items/AID-TEST/manifest.yaml"):
        return (path, "documentation.required", "/documentation")

    def _finding(self, path="14-ai-development/work-items/AID-TEST/manifest.yaml"):
        return {
            "manifest_path": path,
            "rule_id": "documentation.required",
            "pointer": "/documentation",
            "category": "AC4",
            "message": "documentation is required",
        }

    def _entry(self, disposition="OPEN", **changes):
        identity = self._identity()
        entry = {
            "finding_id": finding_id(identity),
            "manifest_path": identity[0],
            "rule_id": identity[1],
            "pointer": identity[2],
            "disposition": disposition,
            "rationale": "The historical record is being remediated.",
            "accountable_owner": "Work Item governance owner",
            "migration_plan": "Add valid documentation and verify the schema gate.",
            "resolution_commit": None,
            "resolution_evidence": None,
        }
        entry.update(changes)
        return entry

    def _ledger(self, entries):
        return {
            "schema_version": 1,
            "baseline_commit": "a" * 40,
            "cohort": "14-ai-development/reports/work-item-legacy-cohort.json",
            "generated_by": "scripts/ci/check_work_item_manifest_schema.py --generate-ledger",
            "entries": entries,
        }

    def _validate(self, entries, baseline=None, current=None):
        baseline = baseline if baseline is not None else {self._identity(): self._finding()}
        current = current if current is not None else baseline
        return validate_ledger(
            self._ledger(entries), baseline, current, "a" * 40,
            "14-ai-development/reports/work-item-legacy-cohort.json",
        )

    def test_finding_identity_hash_is_stable_and_uses_json_tuple(self):
        identity = self._identity()
        self.assertEqual(len(finding_id(identity)), 64)
        self.assertEqual(finding_identity(self._finding()), identity)

    def test_cohort_finding_new_identity_is_regression(self):
        baseline = {self._identity(): self._finding()}
        new_identity = (
            "14-ai-development/work-items/AID-TEST/manifest.yaml",
            "documentation.relationship.enum",
            "/documentation/0/relationship",
        )
        current = dict(baseline)
        current[new_identity] = {
            "manifest_path": new_identity[0],
            "rule_id": new_identity[1],
            "pointer": new_identity[2],
            "category": "AC4",
            "message": "invalid relationship",
        }
        self.assertIn(new_identity, set(current) - set(baseline))

    def test_manifest_outside_cohort_is_new_population(self):
        outside = "14-ai-development/work-items/AID-NEW/manifest.yaml"
        self.assertNotEqual(outside, self._identity()[0])
        self.assertTrue(outside.endswith("/manifest.yaml"))

    def test_missing_ledger_entry_is_reported(self):
        errors, _ = self._validate([])
        self.assertIn("MISSING_LEDGER_ENTRY", {e["code"] for e in errors})

    def test_orphan_ledger_entry_is_reported(self):
        entry = self._entry()
        entry["manifest_path"] = "14-ai-development/work-items/AID-ORPHAN/manifest.yaml"
        identity = (entry["manifest_path"], entry["rule_id"], entry["pointer"])
        entry["finding_id"] = finding_id(identity)
        errors, _ = self._validate([entry])
        self.assertIn("ORPHAN_LEDGER_ENTRY", {e["code"] for e in errors})

    def test_duplicate_ledger_entry_is_reported(self):
        entry = self._entry()
        errors, _ = self._validate([entry, dict(entry)])
        self.assertIn("DUPLICATE_LEDGER_ENTRY", {e["code"] for e in errors})

    def test_incomplete_ledger_entry_is_reported(self):
        entry = self._entry()
        entry["accountable_owner"] = ""
        errors, _ = self._validate([entry])
        self.assertIn("INCOMPLETE_LEDGER_ENTRY", {e["code"] for e in errors})

    def test_draft_placeholders_are_incomplete_but_not_missing_or_orphan(self):
        entry = self._entry()
        for key, placeholder in LEDGER_PLACEHOLDERS.items():
            entry[key] = placeholder
        errors, _ = self._validate([entry])
        self.assertEqual({e["code"] for e in errors}, {"INCOMPLETE_LEDGER_ENTRY"})

    def test_migrated_finding_still_present_is_rejected(self):
        entry = self._entry(
            disposition="MIGRATED",
            resolution_commit="b" * 40,
            resolution_evidence="PR #1 and merged commit bbbbbbbb",
        )
        errors, _ = self._validate([entry])
        self.assertIn("INCOMPLETE_LEDGER_ENTRY", {e["code"] for e in errors})

    def test_open_finding_that_disappeared_is_rejected(self):
        entry = self._entry()
        errors, _ = self._validate([entry], current={})
        self.assertIn("INCOMPLETE_LEDGER_ENTRY", {e["code"] for e in errors})

    def test_accepted_risk_requires_present_finding_and_complete_fields(self):
        entry = self._entry(disposition="ACCEPTED_RISK")
        errors, _ = self._validate([entry])
        self.assertEqual(errors, [])

    def test_generated_ledger_is_open_draft_with_all_required_fields(self):
        finding = self._finding()
        baseline = {finding_identity(finding): finding}
        cohort = {
            "baseline_commit": "a" * 40,
        }
        generated = generate_ledger(
            baseline,
            cohort,
            Path("14-ai-development/reports/work-item-legacy-cohort.json"),
        )
        self.assertEqual(generated["schema_version"], 1)
        self.assertEqual(generated["entries"][0]["disposition"], "OPEN")
        self.assertEqual(
            generated["entries"][0]["rationale"],
            LEDGER_PLACEHOLDERS["rationale"],
        )
        self.assertIsNone(generated["entries"][0]["resolution_commit"])

    def test_ledger_top_level_must_match_p1_contract(self):
        ledger = self._ledger([self._entry()])
        ledger["entry_count"] = 1
        baseline = {self._identity(): self._finding()}
        errors, _ = validate_ledger(
            ledger, baseline, baseline, "a" * 40,
            "14-ai-development/reports/work-item-legacy-cohort.json",
        )
        self.assertIn("INCOMPLETE_LEDGER_ENTRY", {e["code"] for e in errors})


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
