#!/usr/bin/env python3
"""Self-check for check_declared_check_contexts.

Run from `scripts/`: this module imports its checker by bare name.

Each test builds a throwaway tree so the case is the only thing that can move
the verdict. The protected side is injected in every case except the last, so
only one test touches the network.

The incomplete cases are the point: a checker that cannot find its input must
say INCOMPLETE (2), never PASS (0).
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

DECLARED = ["Rust format (hard gate)", "audit"]


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

    def run_checker(self, protection=None):
        """Default to the declared set: the tree alone cannot satisfy equality."""
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return checker.main(self.root, DECLARED if protection is None else protection)

    def test_pass_when_every_declared_context_is_produced(self):
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(checker.main(self.root, DECLARED), 0)
        output = errors.getvalue()
        self.assertIn("CONTEXT COUNTS: declared=2 required=2 produced=3", output)
        self.assertIn("required_not_declared=[]", output)
        self.assertIn("declared_not_produced=[]", output)
        self.assertIn("::notice::2 declared, 2 required, all produced", output)

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
            self.assertEqual(checker.main(self.root, DECLARED), 1)
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

    # --- declared vs protected -------------------------------------------------

    def test_violation_when_the_platform_requires_more_than_the_document(self):
        """The 12-vs-15 shape: protected is a strict superset of declared."""
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(checker.main(self.root, DECLARED + ["Session Evidence"]), 1)
        self.assertIn("Session Evidence", errors.getvalue())
        self.assertIn("does not declare it", errors.getvalue())
        self.assertIn("required_not_declared=['Session Evidence']", errors.getvalue())

    def test_violation_when_the_document_declares_what_is_not_protected(self):
        """Dropping a line from protection while the document keeps it must fail."""
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(checker.main(self.root, ["audit"]), 1)
        self.assertIn("Rust format (hard gate)", errors.getvalue())
        self.assertIn("declares required check context", errors.getvalue())

    def test_violation_when_a_context_is_declared_twice(self):
        """A duplicated line collapses into the set, so the sets still match."""
        self.write(DOC, DOC_TEXT.replace("audit\n", "audit\naudit\n"))
        self.write(".github/workflows/gates.yml", WORKFLOW)
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(checker.main(self.root, DECLARED), 1)
        self.assertIn("audit", errors.getvalue())
        self.assertIn("more than once", errors.getvalue())

    def test_incomplete_when_the_payload_cannot_be_read(self):
        """An unreadable platform is INCOMPLETE, never PASS and never skipped."""
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)

        def unreachable(**_kwargs):
            raise OSError("connection refused")

        original = checker.fetch_protected_contexts
        checker.fetch_protected_contexts = unreachable
        self.addCleanup(setattr, checker, "fetch_protected_contexts", original)
        with redirect_stdout(io.StringIO()), redirect_stderr(errors := io.StringIO()):
            self.assertEqual(checker.main(self.root), 2)
        self.assertIn("branches/main.protection.required_status_checks.contexts", errors.getvalue())
        self.assertIn("OSError: connection refused", errors.getvalue())

    def test_incomplete_when_the_payload_returns_none(self):
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)
        original = checker.fetch_protected_contexts
        checker.fetch_protected_contexts = lambda **_kwargs: None
        self.addCleanup(setattr, checker, "fetch_protected_contexts", original)
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(checker.main(self.root), 2)
        self.assertIn("branches/main.protection.required_status_checks.contexts", errors.getvalue())
        self.assertIn("returned None", errors.getvalue())

    def test_incomplete_when_the_payload_has_no_contexts(self):
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)
        self.assertEqual(self.run_checker(protection=[]), 2)

    # #1212: `jobs:  # comment` is not the string `jobs:`, and it is not a
    # column-0 key either, so the old reader never entered the jobs mapping and
    # the file produced an empty set. The subset test then could not fail. The
    # header is read through its comment now: both contexts must still be found.
    def test_jobs_header_with_a_trailing_comment_still_produces_contexts(self):
        commented = WORKFLOW.replace(
            "jobs:\n", "jobs:  # the required gate jobs\n"
        )
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", commented)
        self.assertIn("Rust format (hard gate)", checker.produced_contexts(commented))
        self.assertIn("audit", checker.produced_contexts(commented))
        self.assertEqual(self.run_checker(), 0)

    # The converse: a job that exists only in a comment is not produced, so a
    # declaration that leans on it must fail. Comment stripping must not turn
    # commented text into structure.
    def test_a_job_named_only_in_a_comment_is_not_produced(self):
        commented = WORKFLOW.replace("  audit:\n", "  # audit:\n")
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", commented)
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(checker.main(self.root, DECLARED), 1)
        self.assertIn("'audit'", errors.getvalue())
        self.assertIn("no job in", errors.getvalue())

    # #1212: only `*.yml` was globbed, so a `.yaml` workflow's jobs were
    # invisible and the produced side read as empty for that file. GitHub
    # honours both suffixes, and so must the checker.
    def test_yaml_workflow_suffix_is_read(self):
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yaml", WORKFLOW)
        self.assertEqual(self.run_checker(), 0)

    def test_the_repository_itself_passes(self):
        """The real tree, against its own declaration. No network.

        The live half is the checker's own CI step, not this suite: a unit test
        that needs the network fails on a rate limit and passes on a stale
        payload, and neither says anything about this tree.
        """
        real = checker.declared_contexts((REPO / DOC).read_text(encoding="utf-8"))
        self.assertTrue(real)
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(checker.main(REPO, real), 0)


if __name__ == "__main__":
    unittest.main()
