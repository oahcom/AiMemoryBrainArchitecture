#!/usr/bin/env python3
"""Self-check for check_declared_check_contexts.

Run from `scripts/`: this module imports its checker by bare name.

Each test builds a throwaway tree so the case is the only thing that can move
the verdict. The incomplete cases are the point: a checker that cannot find its
input must say INCOMPLETE (2), never PASS (0).
"""

import io
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import check_declared_check_contexts as checker

REPO = Path(__file__).resolve().parent.parent

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
```text
Rust format (hard gate)
audit
```
"""


class DeclaredCheckContextsTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        (self.root / ".github" / "workflows").mkdir(parents=True)
        (self.root / "14-ai-development").mkdir(parents=True)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_checker(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return checker.main(self.root)

    def test_pass_when_every_declared_context_is_produced(self):
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)
        self.assertEqual(self.run_checker(), 0)

    def test_job_id_satisfies_a_declaration_without_a_display_name(self):
        # `audit` has no `name:` in WORKFLOW, so GitHub reports the job id.
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)
        self.assertIn("audit", checker.produced_contexts(WORKFLOW))

    def test_violation_names_the_unproduced_context(self):
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW.replace(
            "Rust format (hard gate)", "Rust format (renamed)"
        ))
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(checker.main(self.root), 1)
        self.assertIn("Rust format (hard gate)", errors.getvalue())
        self.assertIn(DOC, errors.getvalue())

    def test_incomplete_when_declaring_document_is_absent(self):
        self.write(".github/workflows/gates.yml", WORKFLOW)
        self.assertEqual(self.run_checker(), 2)

    def test_incomplete_when_no_workflow_can_produce_anything(self):
        self.write(DOC, DOC_TEXT)
        self.assertEqual(self.run_checker(), 2)

    def test_incomplete_when_the_declaration_block_is_absent(self):
        self.write(DOC, "# PR-GOVERNANCE-001\n\nNo declaration here.\n")
        self.write(".github/workflows/gates.yml", WORKFLOW)
        self.assertEqual(self.run_checker(), 2)

    def test_incomplete_when_the_declaration_block_is_empty(self):
        self.write(DOC, "<!-- declared-check-contexts -->\n```text\n```\n")
        self.write(".github/workflows/gates.yml", WORKFLOW)
        self.assertEqual(self.run_checker(), 2)

    def test_the_repository_itself_passes(self):
        # The declared contexts are a claim about this tree; hold it to that.
        self.assertEqual(checker.main(REPO), 0)


if __name__ == "__main__":
    unittest.main()
