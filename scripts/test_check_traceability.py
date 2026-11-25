#!/usr/bin/env python3
"""Unit tests for check_traceability.py; no network or third-party packages."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from check_traceability import run_check


AID = "AID-2026-999"
ISSUE_URL = "https://github.com/oahcom/AiMemoryBrainArchitecture/issues/266"


class TraceabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "00-governance").mkdir()
        (self.root / "14-ai-development/work-items" / AID).mkdir(
            parents=True
        )
        (self.root / "scripts").mkdir()
        (self.root / "docs").mkdir()

        subprocess.run(
            ["git", "init", "-q"], cwd=self.root, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "traceability-test@example.invalid"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Traceability Test"],
            cwd=self.root,
            check=True,
        )
        (self.root / "seed.txt").write_text("seed\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", "seed.txt"], cwd=self.root, check=True
        )
        subprocess.run(
            ["git", "commit", "-qm", "seed"], cwd=self.root, check=True
        )
        self.base_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.root,
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.strip()

        (self.root / "docs/linked.md").write_text(
            "linked\n", encoding="utf-8"
        )
        self.write_manifest()
        self.write_index()
        self.write_registry()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def manifest_path(self, aid: str = AID) -> Path:
        return (
            self.root / "14-ai-development/work-items" / aid / "manifest.yaml"
        )

    def write_manifest(
        self,
        work_item_id: str = AID,
        tracking_issue: str = "#266 (REQ-05)",
        base_commit_sha: str | None = None,
        extra: str = "",
    ) -> None:
        sha = base_commit_sha or self.base_sha
        content = (
            "work_item_id: {}\n"
            "status: VERIFIED\n"
            'tracking_issue: "{}"\n'
            "base_commit_sha: {}\n"
            "dependency_refs: []\n"
            "{}"
        ).format(work_item_id, tracking_issue, sha, extra)
        self.manifest_path().write_text(content, encoding="utf-8")

    def write_index(self, aid: str = AID, path: str | None = None) -> None:
        manifest_path = path or "{}/manifest.yaml".format(aid)
        content = (
            "| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | "
            "Implementation | Review | Acceptance |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
            "| [{}]({}) | Example | NOT_RECORDED | NOT_RECORDED | "
            "VERIFIED | | | | |\n"
        ).format(aid, manifest_path)
        (
            self.root / "14-ai-development/work-items/INDEX.md"
        ).write_text(content, encoding="utf-8")

    def registry_item(self) -> dict:
        return {
            "requirement_id": "REQ-05",
            "title": "Example requirement",
            "authority_url": ISSUE_URL,
            "status": "NOT_RECORDED",
            "owner": "NOT_RECORDED",
            "scope_in": "NOT_RECORDED",
            "scope_out": "NOT_RECORDED",
            "linked_work_items": [AID],
            "linked_docs": ["docs/linked.md"],
            "session_acceptance": {
                "acceptance_state": "NOT_RECORDED",
                "evidence_refs": [],
            },
            "independent_review": {
                "required": False,
                "status": "NOT_REQUIRED",
                "blocker_reason": None,
                "exception_ref": None,
                "implementation_identity": None,
                "reviewer_identity": None,
                "evidence_refs": [],
            },
        }

    def write_registry(self, requirements: list | None = None) -> None:
        data = {
            "_comment": ["Test registry; GitHub Issue is authoritative."],
            "requirements": (
                requirements if requirements is not None
                else [self.registry_item()]
            ),
        }
        (
            self.root / "00-governance/requirements-registry.yaml"
        ).write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )

    def check(self) -> tuple[int, str]:
        output = io.StringIO()
        code = run_check(self.root, output)
        return code, output.getvalue()

    def check_cli(self, *args: str) -> tuple[int, str]:
        """Run the checker as a process from the tree root.

        #1071: the assertions must bite on the real path, not only when a
        test calls a function. This executes the checker the way
        `.github/workflows/repository-hygiene.yml` does against this tree,
        with the temporary repository as its working directory.
        """
        script = Path(__file__).with_name("check_traceability.py")
        result = subprocess.run(
            [sys.executable, str(script), *args],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout + result.stderr

    def add_unindexed_manifest(
        self,
        aid: str,
        content: str,
    ) -> None:
        directory = self.root / "14-ai-development/work-items" / aid
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "manifest.yaml").write_text(
            content, encoding="utf-8"
        )

    def test_t01_valid_unique_requirement_and_issue_url_passes(self) -> None:
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertIn("TRACEABILITY: 1 requirements / 1 work items", output)

    def test_t01_duplicate_requirement_id_fails(self) -> None:
        item = self.registry_item()
        self.write_registry([item, dict(item)])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR T-01 duplicate requirement_id REQ-05", output)

    def test_t01_malformed_authority_url_fails(self) -> None:
        item = self.registry_item()
        item["authority_url"] = "Issue #266"
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR T-01", output)

    def test_t02_existing_linked_document_passes(self) -> None:
        code, output = self.check()
        self.assertEqual(code, 0, output)

    def test_t02_missing_linked_document_fails(self) -> None:
        item = self.registry_item()
        item["linked_docs"] = ["docs/does-not-exist.md"]
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR T-02", output)

    def test_t03_indexed_linked_work_item_passes(self) -> None:
        code, output = self.check()
        self.assertEqual(code, 0, output)

    def test_t03_unindexed_linked_work_item_fails(self) -> None:
        item = self.registry_item()
        item["linked_work_items"] = ["AID-2026-998"]
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR T-03", output)

    def test_t04_index_row_with_manifest_and_matching_id_passes(self) -> None:
        code, output = self.check()
        self.assertEqual(code, 0, output)

    def test_t04_index_row_without_manifest_fails(self) -> None:
        self.manifest_path().unlink()
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR T-04 INDEX entry", output)

    def test_t04_manifest_id_must_match_directory(self) -> None:
        self.write_manifest(work_item_id="AID-2026-998")
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR T-04 manifest", output)

    def test_t04_historical_aid_key_is_accepted_only_for_allowlisted_id(
        self,
    ) -> None:
        legacy_id = "AID-2026-023"
        directory = self.root / "14-ai-development/work-items" / legacy_id
        directory.mkdir(parents=True)
        (directory / "manifest.yaml").write_text(
            "aid: AID-2026-023\n"
            'tracking_issue: "legacy"\n'
            "base_commit_sha: {}\n".format(self.base_sha),
            encoding="utf-8",
        )
        index = (
            self.root / "14-ai-development/work-items/INDEX.md"
        )
        # Append instead of replacing: the default AID fixture stays
        # indexed, so its registry link still resolves (T-03) and the new
        # reverse-completeness rule (T-04) sees both manifests registered.
        with index.open("a", encoding="utf-8") as handle:
            handle.write(
                "| [{}]({}/manifest.yaml) |\n".format(
                    legacy_id, legacy_id
                )
            )
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertIn("uses legacy aid identity key", output)

    def test_t04_aid_key_is_rejected_for_non_allowlisted_id(self) -> None:
        self.write_manifest()
        self.manifest_path().write_text(
            "aid: {}\n".format(AID), encoding="utf-8"
        )
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("non-normative aid key", output)

    def test_t04_both_identity_keys_are_rejected(self) -> None:
        self.manifest_path().write_text(
            "work_item_id: {}\naid: {}\n".format(AID, AID),
            encoding="utf-8",
        )
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("both work_item_id and aid", output)

    def test_t04_unknown_identity_key_is_not_guessed(self) -> None:
        self.manifest_path().write_text(
            "id: {}\n".format(AID), encoding="utf-8"
        )
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("no recognized identity key", output)

    def test_t04_stage_zero_registration_is_warning_not_identity_error(
        self,
    ) -> None:
        self.manifest_path().write_text(
            'manifest_version: "1.0"\n'
            'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n'
            'registration_stage: "STAGE_0"\n',
            encoding="utf-8",
        )
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertIn("Stage 0 registration record", output)
        self.assertNotIn("no recognized identity key", output)

    def test_t04_unindexed_ordinary_manifest_is_error(self) -> None:
        unindexed = "AID-2026-998"
        self.add_unindexed_manifest(
            unindexed,
            "work_item_id: {}\n".format(unindexed),
        )
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn(
            "14-ai-development/work-items/{}/manifest.yaml".format(unindexed),
            output,
        )
        self.assertIn("exists on disk but is not indexed", output)

    def test_t04_unindexed_stage_zero_registration_is_error(self) -> None:
        unindexed = "AID-2026-998"
        self.add_unindexed_manifest(
            unindexed,
            'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n',
        )
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("Stage 0 registration record", output)
        self.assertIn("exists on disk but is not indexed", output)

    def test_t05_issue_reference_matching_authority_is_accepted(self) -> None:
        self.write_manifest(tracking_issue="#266 (REQ-05)")
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertNotIn("WARN T-05", output)

    def test_t05_unmapped_free_text_is_warning_not_error(self) -> None:
        self.write_manifest(
            tracking_issue="#617 (REQ-08 / implementation follow-up)"
        )
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertIn("WARN T-05", output)
        self.assertNotIn("ERROR T-05", output)

    def test_t06_real_commit_is_accepted(self) -> None:
        self.write_manifest(base_commit_sha=self.base_sha)
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertNotIn("WARN T-06", output)

    def test_t06_missing_commit_in_complete_history_is_warning(self) -> None:
        missing_sha = "f" * 40
        self.write_manifest(base_commit_sha=missing_sha)
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertIn("WARN T-06", output)
        self.assertIn("complete local Git object database", output)

    def test_t06_shallow_repository_unknown_returns_two(self) -> None:
        shallow_file = self.root / ".git/shallow"
        shallow_file.write_text(self.base_sha + "\n", encoding="ascii")
        self.write_manifest(base_commit_sha="e" * 40)
        code, output = self.check()
        self.assertEqual(code, 2, output)
        self.assertIn("WARN T-06", output)
        self.assertIn("shallow object database", output)

    def test_t07_explicit_no_work_item_reason_passes(self) -> None:
        item = self.registry_item()
        item["linked_work_items"] = []
        item["no_work_item_yet"] = True
        item["no_work_item_yet_reason"] = "No verified AID mapping."
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 0, output)

    def test_t07_missing_work_item_and_reason_fails(self) -> None:
        item = self.registry_item()
        item["linked_work_items"] = []
        item["no_work_item_yet"] = True
        item.pop("no_work_item_yet_reason", None)
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR T-07", output)

    def test_required_missing_document_path_is_exit_one(self) -> None:
        item = self.registry_item()
        item["linked_docs"] = ["docs/missing-required-file.md"]
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR T-02", output)

    def acceptance_item(self) -> dict:
        item = self.registry_item()
        item["session_acceptance"] = {
            "acceptance_state": "NOT_RECORDED",
            "evidence_refs": [],
        }
        item["independent_review"] = {
            "required": True,
            "status": "BLOCKED",
            "blocker_reason": "Only one write-capable identity is available.",
            "exception_ref": "EX-20261123-01",
            "implementation_identity": None,
            "reviewer_identity": None,
            "evidence_refs": [],
        }
        return item


    def test_t08_explicit_blocked_review_is_warning(self) -> None:
        self.write_registry([self.acceptance_item()])
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertIn("independent review is explicitly BLOCKED", output)
        self.assertNotIn("ERROR T-08", output)


    def test_t08_blocked_review_requires_exception_ref(self) -> None:
        item = self.acceptance_item()
        item["independent_review"]["exception_ref"] = None
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("BLOCKED requires exception_ref", output)


    def test_t08_blocked_review_requires_reason(self) -> None:
        item = self.acceptance_item()
        item["independent_review"]["blocker_reason"] = ""
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("BLOCKED requires blocker_reason", output)


    def test_t08_pending_review_is_warning(self) -> None:
        item = self.acceptance_item()
        review = item["independent_review"]
        review["status"] = "PENDING"
        review["blocker_reason"] = None
        review["exception_ref"] = None
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertIn("independent review is pending", output)


    def test_t08_same_identity_cannot_pass_review(self) -> None:
        item = self.acceptance_item()
        review = item["independent_review"]
        review.update({
            "status": "PASSED",
            "blocker_reason": None,
            "exception_ref": None,
            "implementation_identity": "writer-1",
            "reviewer_identity": "writer-1",
            "evidence_refs": ["PR-REVIEW-REF"],
        })
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("reviewer must differ", output)


    def test_t08_distinct_reviewer_with_evidence_can_pass(self) -> None:
        item = self.acceptance_item()
        review = item["independent_review"]
        review.update({
            "status": "PASSED",
            "blocker_reason": None,
            "exception_ref": None,
            "implementation_identity": "writer-1",
            "reviewer_identity": "reviewer-2",
            "evidence_refs": ["PR-REVIEW-REF"],
        })
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 0, output)


    def test_t08_legacy_acceptance_state_is_rejected(self) -> None:
        item = self.acceptance_item()
        item["acceptance_state"] = "NOT_RECORDED"
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("retains legacy acceptance_state", output)


    def test_t08_unknown_independent_review_status_is_rejected(self) -> None:
        item = self.acceptance_item()
        item["independent_review"]["status"] = "SOME_NEW_STATE"
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertIn("status is missing or unsupported", output)


    # Issue #884: the summary word must be a function of the verdict. A run
    # that exits non-zero must never print PASS, because any consumer that
    # reads only the text would then get the opposite answer from the exit
    # code.
    def test_summary_word_is_fail_when_errors_are_present(self) -> None:
        item = self.registry_item()
        item["linked_docs"] = ["docs/does-not-exist.md"]
        self.write_registry([item])
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertNotIn("PASS", output)
        self.assertIn("FAIL TRACEABILITY: 1 requirements", output)

    def test_missing_registry_is_fail_not_zero_error_incomplete(self) -> None:
        # The fixture is self-contained: setUp writes its own minimal registry
        # into this temporary repository, and this test removes it. A required
        # input missing is a repository defect: exit 1 and an error count of 1,
        # never a summary that reads "0 errors" beside a failing exit code.
        (
            self.root / "00-governance/requirements-registry.yaml"
        ).unlink()
        code, output = self.check()
        self.assertEqual(code, 1, output)
        self.assertNotIn("PASS", output)
        self.assertNotIn("INCOMPLETE TRACEABILITY:", output)
        self.assertIn("ERROR required registry unavailable:", output)
        self.assertIn(
            "FAIL TRACEABILITY: 0 requirements / 0 work items / 1 errors",
            output,
        )

    def test_summary_word_is_pass_when_no_errors(self) -> None:
        code, output = self.check()
        self.assertEqual(code, 0, output)
        self.assertIn("PASS TRACEABILITY: 1 requirements", output)

    # Issue #1071: the checker's only execution was this file. These tests run
    # it as a process, the way the workflow does, so the four INDEX/manifest
    # properties are shown to bite on the real path rather than only when a
    # test calls a function.

    def test_1071_cli_runs_without_registry_and_reports_scope(self) -> None:
        (
            self.root / "00-governance/requirements-registry.yaml"
        ).unlink()
        code, output = self.check_cli("--index-manifest-only")
        self.assertEqual(code, 0, output)
        self.assertIn("NOT EVALUATED: requirement checks", output)
        self.assertIn(
            "PASS TRACEABILITY [INDEX/MANIFEST ONLY]: 0 requirements / "
            "1 work items",
            output,
        )

    def test_1071_cli_duplicate_index_entry_exits_nonzero(self) -> None:
        index = self.root / "14-ai-development/work-items/INDEX.md"
        with index.open("a", encoding="utf-8") as handle:
            handle.write(
                "| [{}]({}/manifest.yaml) | Example again |\n".format(AID, AID)
            )
        # Condition 3 (no registry) and condition 4 (registry supplied): the
        # assertion, not the plumbing, is what these pin down.
        for args in ((), ("--index-manifest-only",)):
            with self.subTest(args=args):
                code, output = self.check_cli(*args)
                self.assertNotEqual(code, 0, output)
                self.assertIn("duplicate INDEX entry {}".format(AID), output)

    def test_1071_cli_manifest_identity_mismatch_exits_nonzero(self) -> None:
        self.write_manifest(work_item_id="AID-2026-998")
        for args in ((), ("--index-manifest-only",)):
            with self.subTest(args=args):
                code, output = self.check_cli(*args)
                self.assertNotEqual(code, 0, output)
                self.assertIn("does not match directory", output)

    def test_1071_default_cli_still_fails_on_missing_registry(self) -> None:
        (
            self.root / "00-governance/requirements-registry.yaml"
        ).unlink()
        code, output = self.check_cli()
        self.assertEqual(code, 1, output)
        self.assertIn("ERROR required registry unavailable:", output)

    def test_1071_narrowed_cli_missing_index_is_exit_one(self) -> None:
        (
            self.root / "14-ai-development/work-items/INDEX.md"
        ).unlink()
        code, output = self.check_cli("--index-manifest-only")
        self.assertEqual(code, 1, output)
        self.assertIn("required work item INDEX unavailable:", output)


if __name__ == "__main__":
    unittest.main()
