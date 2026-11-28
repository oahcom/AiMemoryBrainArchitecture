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
