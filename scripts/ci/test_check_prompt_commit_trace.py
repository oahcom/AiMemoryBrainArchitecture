"""Regression tests for the prompt-to-commit trace checker."""
import os
import subprocess
import unittest
from pathlib import Path

from scripts.ci.check_prompt_commit_trace import (
    ROOT, audit, classify_primary, resolve_commit, summarize,
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


class RepositoryRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ref = resolve_commit(ROOT, os.environ.get("GITHUB_BASE_SHA", "origin/main"))
        if not cls.ref:
            raise unittest.SkipTest("origin/main unavailable; CI must checkout full history")
        cls.rows = audit(ROOT, cls.ref, cls.ref)
        cls.by_id = {r["work_item_id"]: r for r in cls.rows}

    def test_nested_implementation_commit_field_is_read(self):
        # These five commits resolve but are not ancestors of main.
        for item in ("AID-2026-041", "AID-2026-042", "AID-2026-043",
                     "AID-2026-048", "AID-2026-049"):
            with self.subTest(item=item):
                row = self.by_id[item]
                self.assertEqual(row["commit_dimension"], "UNREACHABLE")
                self.assertEqual(row["primary_status"], "COMMIT_UNREACHABLE")
                self.assertNotIn("commit_absent", row["findings"])

    def test_prompt_pinned_but_implementation_commit_absent(self):
        for item in ("AID-2026-011", "AID-2026-040", "AID-2026-044",
                     "AID-2026-045", "AID-2026-046"):
            with self.subTest(item=item):
                row = self.by_id[item]
                self.assertEqual(row["prompt_dimension"], "PINNED_OK")
                self.assertEqual(row["commit_dimension"], "ABSENT")
                self.assertIn("commit_absent", row["findings"])

    def test_047_unpinned_head_match_is_not_execution_time_trace(self):
        # AID-2026-047 currently has no blob or commit pin in its manifest.
        # Its HEAD bytes match, but the R3 state contract classifies this
        # HEAD_MATCH/no-pin case as DIGEST_UNPINNED, not TRACEABLE.
        row = self.by_id["AID-2026-047"]
        self.assertEqual(row["prompt_dimension"], "HEAD_MATCH")
        self.assertEqual(row["commit_dimension"], "REACHABLE")
        self.assertEqual(row["primary_status"], "DIGEST_UNPINNED")
        self.assertIn("digest_unpinned", row["findings"])
        self.assertNotIn("digest_head_mismatch", row["findings"])


if __name__ == "__main__":
    unittest.main()
