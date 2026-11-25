#!/usr/bin/env python3
"""Self-check for check_session_evidence_workflow_shape.

Run from `scripts/`: this module imports its checker by bare name.

Each case builds a throwaway tree so the mutation is the only thing that can
move the verdict, and each asserts on the message text, not only the exit code
-- a guard that fails for an unrelated reason would otherwise look like a
guard that works. The incomplete cases are the point: a checker that cannot
find its input must say INCOMPLETE (2), never PASS (0).
"""

import io
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import check_session_evidence_workflow_shape as checker

REPO = Path(__file__).resolve().parent.parent

WORKFLOW_PATH = ".github/workflows/session-evidence.yml"

WORKFLOW = """\
name: Session Evidence Gate
on:
  pull_request:
jobs:
  self-test-trusted-base:
    name: Session Evidence self-test (base)
    runs-on: ubuntu-latest
    steps:
      - name: Checkout trusted base revision
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.base.sha }}
          persist-credentials: false

  self-test-pr-head:
    name: Session Evidence self-test (head)
    runs-on: ubuntu-latest
    steps:
      - name: Checkout PR head
        uses: actions/checkout@v4
        with:
          persist-credentials: false

  validate:
    name: Session Evidence
    runs-on: ubuntu-latest
    steps:
      - name: Checkout trusted base revision
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.base.sha }}
"""


class SessionEvidenceWorkflowShapeTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)

    def write(self, text):
        path = self.root / WORKFLOW_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_checker(self):
        """(exit code, stderr) for the tree built by this test."""
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            code = checker.main(self.root)
        return code, errors.getvalue()

    def test_pass_on_the_three_job_shape(self):
        self.write(WORKFLOW)
        code, message = self.run_checker()
        self.assertEqual(code, 0)
        self.assertNotIn("::error::", message)

    def test_collapse_to_one_job_is_a_violation_naming_each_missing_job(self):
        collapsed = """\
name: Session Evidence Gate
on:
  pull_request:
jobs:
  validate:
    name: Session Evidence
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 -m scripts.governance.session_evidence.validate
"""
        self.write(collapsed)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("self-test-trusted-base", message)
        self.assertIn("self-test-pr-head", message)

    def test_deleting_the_head_job_names_that_job(self):
        lines = WORKFLOW.splitlines()
        start = next(
            i for i, line in enumerate(lines) if line.startswith("  self-test-pr-head:")
        )
        end = next(i for i, line in enumerate(lines) if line.startswith("  validate:"))
        self.write("\n".join(lines[:start] + lines[end:]))
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("self-test-pr-head", message)

    def test_head_job_checkout_with_ref_is_a_violation(self):
        self.write(WORKFLOW.replace(
            "      - name: Checkout PR head\n"
            "        uses: actions/checkout@v4\n"
            "        with:\n"
            "          persist-credentials: false\n",
            "      - name: Checkout PR head\n"
            "        uses: actions/checkout@v4\n"
            "        with:\n"
            "          ref: ${{ github.event.pull_request.base.sha }}\n"
            "          persist-credentials: false\n",
        ))
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("self-test-pr-head", message)
        self.assertIn("ref:", message)

    def test_validate_needs_is_a_violation(self):
        self.write(WORKFLOW.replace(
            "  validate:\n    name: Session Evidence\n",
            "  validate:\n    name: Session Evidence\n    needs: self-test-pr-head\n",
        ))
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("validate", message)
        self.assertIn("needs:", message)

    def test_ref_in_the_base_job_is_allowed(self):
        # The base job SHALL read the base revision; only the head job may not.
        self.write(WORKFLOW)
        self.assertIn(
            "ref: ${{ github.event.pull_request.base.sha }}",
            WORKFLOW,
        )
        self.assertEqual(self.run_checker()[0], 0)

    def test_incomplete_when_the_workflow_is_absent(self):
        self.assertEqual(self.run_checker()[0], 2)

    def test_incomplete_when_there_is_no_jobs_mapping(self):
        self.write("name: Session Evidence Gate\non:\n  pull_request:\n")
        self.assertEqual(self.run_checker()[0], 2)

    def test_the_repository_itself_passes(self):
        # The shape is a claim about this tree; hold it to that.
        self.assertEqual(checker.main(REPO), 0)


if __name__ == "__main__":
    unittest.main()
