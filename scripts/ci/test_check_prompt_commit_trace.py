#!/usr/bin/env python3
"""Regression tests for the prompt-to-commit trace checker."""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from scripts.ci.check_prompt_commit_trace import (
    classify_primary,
    initial_registration_eligible,
    ratchet_violations,
    summarize,
)


class PrimaryDecisionOrderTests(unittest.TestCase):
    def test_decision_precedence_is_fixed(self):
        self.assertEqual(
            classify_primary(False, False, False, False, False), "NO_TRACE"
        )
        self.assertEqual(
            classify_primary(True, True, False, False, False),
            "DIGEST_UNPINNED",
        )
        self.assertEqual(
            classify_primary(True, True, True, False, False),
            "DIGEST_MISMATCH",
        )
        self.assertEqual(
            classify_primary(True, True, True, True, False),
            "COMMIT_UNREACHABLE",
        )
        self.assertEqual(
            classify_primary(True, True, True, True, True), "TRACEABLE"
        )


class RatchetTests(unittest.TestCase):
    def test_regression_is_reported_when_primary_status_degrades(self):
        result = {"manifests": [{
            "work_item_id": "AID-2026-999",
            "primary_status": "DIGEST_MISMATCH",
            "findings": ["digest_pinned_mismatch"],
        }]}
        baseline = {"manifests": {"AID-2026-999": {
            "primary_status": "TRACEABLE", "findings": [],
        }}}
        self.assertEqual(
            ratchet_violations(result, baseline, {"AID-2026-999"}),
            ["REGRESSION:AID-2026-999:TRACEABLE->DIGEST_MISMATCH",
             "NEW_FINDINGS:AID-2026-999:digest_pinned_mismatch"],
        )

    def test_new_findings_is_reported_for_new_nontraceable_manifest(self):
        result = {"manifests": [{
            "work_item_id": "AID-2026-999",
            "primary_status": "NO_TRACE",
            "findings": ["digest_absent"],
        }]}
        self.assertEqual(
            ratchet_violations(result, {"manifests": {}}, set()),
            ["NEW_FINDINGS:AID-2026-999:NO_TRACE"],
        )

    def test_new_findings_is_reported_for_added_finding_on_existing_item(self):
        result = {"manifests": [{
            "work_item_id": "AID-2026-999",
            "primary_status": "TRACEABLE",
            "findings": ["commit_unreachable"],
        }]}
        baseline = {"manifests": {"AID-2026-999": {
            "primary_status": "TRACEABLE", "findings": [],
        }}}
        self.assertEqual(
            ratchet_violations(result, baseline, {"AID-2026-999"}),
            ["NEW_FINDINGS:AID-2026-999:commit_unreachable"],
        )

    def test_manifest_present_at_base_but_absent_from_baseline_is_not_new(self):
        result = {"manifests": [{
            "work_item_id": "AID-2026-265",
            "primary_status": "NO_TRACE",
            "findings": ["digest_absent"],
        }]}
        self.assertEqual(
            ratchet_violations(result, {"manifests": {}}, {"AID-2026-265"}),
            [],
        )

    def test_removed_manifest_is_not_a_ratchet_violation(self):
        baseline = {"manifests": {"AID-2026-265": {
            "primary_status": "NO_TRACE", "findings": ["digest_absent"],
        }}}
        self.assertEqual(
            ratchet_violations({"manifests": []}, baseline, set()), []
        )

    def test_new_work_item_with_pinned_initial_registration_passes(self):
        row = {
            "work_item_id": "AID-2026-999",
            "primary_status": "NO_TRACE",
            "findings": ["commit_absent"],
            "initial_registration_eligible": True,
        }

        self.assertEqual(
            ratchet_violations(
                {"manifests": [row]},
                {"manifests": {}},
                set(),
            ),
            [],
        )

    def test_new_work_item_without_registration_evidence_still_fails(self):
        row = {
            "work_item_id": "AID-2026-999",
            "primary_status": "NO_TRACE",
            "findings": ["digest_absent", "commit_absent"],
            "initial_registration_eligible": False,
        }

        self.assertEqual(
            ratchet_violations(
                {"manifests": [row]},
                {"manifests": {}},
                set(),
            ),
            [
                "NEW_FINDINGS:AID-2026-999:NO_TRACE"
            ],
        )

    def test_initial_registration_requires_exact_immutable_prompt_blob(self):
        manifest_path = (
            "14-ai-development/work-items/AID-2026-999/manifest.yaml"
        )
        prompt_path = (
            "14-ai-development/work-items/AID-2026-999/prompt-v1.md"
        )
        prompt_bytes = b"immutable prompt fixture\n"
        blob_sha = "a" * 40

        doc = {
            "prompt_commit_trace_initial_registration": True,
        }

        valid = initial_registration_eligible(
            manifest_path=manifest_path,
            doc=doc,
            prompt_path=prompt_path,
            prompt_blob_sha=blob_sha,
            prompt_commit_sha=None,
            prompt_blob_bytes=prompt_bytes,
            head_prompt_bytes=prompt_bytes,
            implementation_commit=None,
            merge_commit=None,
            primary_status="NO_TRACE",
            findings=["commit_absent"],
        )

        self.assertTrue(valid)

        # Same declaration, but the prompt at HEAD has different bytes.
        mismatched = initial_registration_eligible(
            manifest_path=manifest_path,
            doc=doc,
            prompt_path=prompt_path,
            prompt_blob_sha=blob_sha,
            prompt_commit_sha=None,
            prompt_blob_bytes=prompt_bytes,
            head_prompt_bytes=b"modified prompt\n",
            implementation_commit=None,
            merge_commit=None,
            primary_status="NO_TRACE",
            findings=["commit_absent"],
        )

        self.assertFalse(mismatched)

        # A declaration without the explicit registration marker is invalid.
        unregistered_doc = {}

        unregistered = initial_registration_eligible(
            manifest_path=manifest_path,
            doc=unregistered_doc,
            prompt_path=prompt_path,
            prompt_blob_sha=blob_sha,
            prompt_commit_sha=None,
            prompt_blob_bytes=prompt_bytes,
            head_prompt_bytes=prompt_bytes,
            implementation_commit=None,
            merge_commit=None,
            primary_status="NO_TRACE",
            findings=["commit_absent"],
        )

        self.assertFalse(unregistered)

        # A missing digest must never qualify.
        missing_digest = initial_registration_eligible(
            manifest_path=manifest_path,
            doc=doc,
            prompt_path=prompt_path,
            prompt_blob_sha=blob_sha,
            prompt_commit_sha=None,
            prompt_blob_bytes=prompt_bytes,
            head_prompt_bytes=prompt_bytes,
            implementation_commit=None,
            merge_commit=None,
            primary_status="NO_TRACE",
            findings=["digest_absent", "commit_absent"],
        )
        self.assertFalse(missing_digest)

        # A pinned digest mismatch must never qualify.
        mismatched_digest = initial_registration_eligible(
            manifest_path=manifest_path,
            doc=doc,
            prompt_path=prompt_path,
            prompt_blob_sha=blob_sha,
            prompt_commit_sha=None,
            prompt_blob_bytes=prompt_bytes,
            head_prompt_bytes=prompt_bytes,
            implementation_commit=None,
            merge_commit=None,
            primary_status="NO_TRACE",
            findings=["digest_pinned_mismatch", "commit_absent"],
        )
        self.assertFalse(mismatched_digest)


class LifecycleAndPinTests(unittest.TestCase):
    def test_dispatched_implementation_sha_is_not_counted_as_reachable(self):
        # The lifecycle rule is exercised through audit's parsed manifest path
        # in the repository integration suite; this fixture guards the
        # decision function against treating an absent implementation as trace.
        self.assertEqual(
            classify_primary(True, False, True, True, True), "NO_TRACE"
        )

    def test_head_match_without_immutable_pin_is_not_traceable(self):
        self.assertEqual(
            classify_primary(True, True, False, False, True),
            "DIGEST_UNPINNED",
        )

    def test_pinned_digest_mismatch_precedes_unreachable_commit(self):
        self.assertEqual(
            classify_primary(True, True, True, False, False),
            "DIGEST_MISMATCH",
        )


class SummaryTests(unittest.TestCase):
    def test_summary_counts_primary_matrix_and_findings(self):
        rows = [
            {
                "primary_status": "TRACEABLE",
                "prompt_dimension": "PINNED_OK",
                "commit_dimension": "REACHABLE",
                "findings": [],
            },
            {
                "primary_status": "NO_TRACE",
                "prompt_dimension": "ABSENT",
                "commit_dimension": "ABSENT",
                "findings": ["digest_absent", "commit_absent"],
            },
        ]
        result = summarize(rows)
        self.assertEqual(result["manifest_count"], 2)
        self.assertEqual(result["primary_status"]["TRACEABLE"], 1)
        self.assertEqual(result["primary_status"]["NO_TRACE"], 1)
        self.assertEqual(
            result["matrix"]["PINNED_OK"]["REACHABLE"], 1
        )
        self.assertEqual(result["findings"]["digest_absent"], 1)


class InlineManifestFixtureTests(unittest.TestCase):
    def test_manifest_fixture_keeps_repo_relative_prompt_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt = root / "14-ai-development/work-items/AID-2026-999/prompt-v1.md"
            prompt.parent.mkdir(parents=True)
            prompt.write_bytes(b"fixture prompt\n")
            manifest = {
                "work_item_id": "AID-2026-999",
                "prompt_file": (
                    "14-ai-development/work-items/AID-2026-999/prompt-v1.md"
                ),
                "prompt_sha256": hashlib.sha256(
                    prompt.read_bytes()
                ).hexdigest(),
                "implementation": {
                    "status": "DISPATCHED",
                    "implementation_commit_sha": None,
                },
            }
            loaded = yaml.safe_load(yaml.safe_dump(manifest))
            self.assertEqual(
                loaded["prompt_file"],
                "14-ai-development/work-items/AID-2026-999/prompt-v1.md",
            )
            self.assertTrue(prompt.is_file())


if __name__ == "__main__":
    unittest.main()
