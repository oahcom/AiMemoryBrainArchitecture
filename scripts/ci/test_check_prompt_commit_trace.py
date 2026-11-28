"""Regression tests for the prompt-to-commit trace checker."""
import os
import subprocess
import unittest
from pathlib import Path

from scripts.ci.check_prompt_commit_trace import (
    ROOT,
    audit,
    classify_primary,
    initial_registration_eligible,
    is_ancestor,
    ratchet_violations,
    resolve_commit,
    summarize,
)


class PrimaryDecisionOrderTests(unittest.TestCase):
    def test_decision_precedence_is_fixed(self):
        # Missing identity wins over every later defect.
        self.assertEqual(classify_primary(False, False, False, False, False), "NO_TRACE")
        # Unpinned wins over a broken commit; a digest mismatch wins over it too.
        self.assertEqual(classify_primary(True, True, False, False, False), "DIGEST_UNPINNED")
        self.assertEqual(classify_primary(True, True, True, False, False), "DIGEST_MISMATCH")
        self.assertEqual(classify_primary(True, True, True, True, False), "COMMIT_UNREACHABLE")
        self.assertEqual(classify_primary(True, True, True, True, True), "TRACEABLE")


class BaselinePinAncestryTests(unittest.TestCase):
    def test_baseline_pin_must_be_an_ancestor_of_comparison_base(self):
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
        parent = subprocess.check_output(
            ["git", "rev-parse", "HEAD^"], cwd=ROOT, text=True
        ).strip()
        self.assertTrue(is_ancestor(ROOT, parent, head))
        self.assertFalse(is_ancestor(ROOT, head, parent))
        self.assertFalse(is_ancestor(ROOT, "", head))


class RatchetBaseInventoryTests(unittest.TestCase):
    def test_manifest_present_at_base_but_absent_from_committed_baseline_is_not_new(self):
        row = {"work_item_id": "AID-2026-265", "primary_status": "NO_TRACE",
               "findings": ["digest_absent", "commit_absent"]}
        self.assertEqual(
            ratchet_violations({"manifests": [row]}, {"manifests": {}}, {"AID-2026-265"}),
            [],
        )

    def test_manifest_removed_from_main_is_not_a_ratchet_violation(self):
        baseline = {"manifests": {"AID-2026-265": {
            "primary_status": "NO_TRACE", "findings": ["digest_absent"]}}}
        self.assertEqual(
            ratchet_violations({"manifests": []}, baseline, {"AID-2026-265"}),
            [],
        )

    def test_genuinely_new_non_traceable_manifest_still_fails(self):
        row = {"work_item_id": "AID-2026-999", "primary_status": "NO_TRACE", "findings": []}
        self.assertEqual(
            ratchet_violations({"manifests": [row]}, {"manifests": {}}, set()),
            ["NEW_NON_TRACEABLE AID-2026-999 NO_TRACE"],
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
                "NEW_NON_TRACEABLE AID-2026-999 NO_TRACE"
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


class RepositoryRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref = resolve_commit(ROOT, os.environ.get("GITHUB_BASE_SHA", "origin/main"))
        if not cls.ref:
            raise unittest.SkipTest("origin/main unavailable; CI must checkout full history")
        cls.rows = audit(ROOT, cls.ref, cls.ref)
        cls.by_id = {r["work_item_id"]: r for r in cls.rows}

    def test_five_nested_commit_manifest_cases_follow_precedence(self):
        # AID-041 has a pinned digest mismatch, so it wins over unreachable.
        row = self.by_id["AID-2026-041"]
        self.assertEqual(row["primary_status"], "DIGEST_MISMATCH")
        self.assertEqual(row["commit_dimension"], "UNREACHABLE")
        self.assertIn("digest_pinned_mismatch", row["findings"])
        self.assertIn("commit_unreachable", row["findings"])
        self.assertNotIn("commit_absent", row["findings"])

        for item in ("AID-2026-042", "AID-2026-043"):
            with self.subTest(item=item):
                row = self.by_id[item]
                self.assertEqual(row["commit_dimension"], "UNREACHABLE")
                self.assertEqual(row["primary_status"], "COMMIT_UNREACHABLE")
                self.assertIn("commit_unreachable", row["findings"])
                self.assertNotIn("commit_absent", row["findings"])

        for item in ("AID-2026-048", "AID-2026-049"):
            with self.subTest(item=item):
                row = self.by_id[item]
                self.assertEqual(row["commit_dimension"], "UNREACHABLE")
                self.assertEqual(row["primary_status"], "DIGEST_UNPINNED")
                self.assertIn("digest_unpinned", row["findings"])
                self.assertIn("commit_unreachable", row["findings"])

    def test_five_pinned_prompt_manifests_have_no_implementation_commit(self):
        for item in ("AID-2026-011", "AID-2026-040", "AID-2026-044",
                     "AID-2026-045", "AID-2026-046"):
            with self.subTest(item=item):
                row = self.by_id[item]
                self.assertEqual(row["prompt_dimension"], "PINNED_OK")
                self.assertEqual(row["commit_dimension"], "ABSENT")
                self.assertEqual(row["primary_status"], "NO_TRACE")
                self.assertTrue(
                    {"commit_absent", "commit_pending"} & set(row["findings"])
                )

    def test_047_unpinned_head_match_is_not_execution_time_trace(self):
        row = self.by_id["AID-2026-047"]
        self.assertEqual(row["prompt_dimension"], "HEAD_MATCH")
        self.assertEqual(row["commit_dimension"], "REACHABLE")
        self.assertEqual(row["primary_status"], "DIGEST_UNPINNED")
        self.assertIn("digest_unpinned", row["findings"])
        self.assertNotIn("digest_head_mismatch", row["findings"])


if __name__ == "__main__":
    unittest.main()
