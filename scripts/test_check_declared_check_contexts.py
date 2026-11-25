#!/usr/bin/env python3
"""Self-check for check_declared_check_contexts.

Run from `scripts/`: this module imports its checker by bare name.

Each test builds a throwaway tree so the case is the only thing that can move
the verdict. The incomplete cases are the point: a checker that cannot find its
input must say INCOMPLETE (2), never PASS (0).
"""

import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

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


class ProtectedCheckContextsTest(unittest.TestCase):
    """The reverse condition: protected -> declared.

    The forward condition could not see #1029: three `Session Evidence*`
    contexts were required on the platform while the document declared twelve,
    and every declared context was still produced by a job. These cases hold
    the other direction.
    """

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, True)
        (self.root / ".github" / "workflows").mkdir(parents=True)
        (self.root / "14-ai-development").mkdir(parents=True)
        self.write(DOC, DOC_TEXT)
        self.write(".github/workflows/gates.yml", WORKFLOW)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_checker(self, payload=None, error=None, requests=None):
        def fetch(path):
            if requests is not None:
                requests.append(path)
            if error is not None:
                raise error
            return payload

        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return checker.main(self.root, check_protection=True, fetch=fetch)

    def run_capturing(self, payload):
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            code = checker.main(
                self.root,
                check_protection=True,
                fetch=lambda path: payload,
            )
        return code, errors.getvalue()

    @staticmethod
    def checks(*pairs):
        return {
            "checks": [{"context": c, "app_id": a} for c, a in pairs],
            "contexts": [c for c, _ in pairs],
        }

    def test_pass_when_protected_equals_declared(self):
        payload = self.checks(
            ("Rust format (hard gate)", 15368),
            ("audit", 15368),
        )
        self.assertEqual(self.run_checker(payload), 0)

    def test_legacy_contexts_shape_is_accepted(self):
        # Only `contexts` populated: app identity is absent and cannot be compared.
        payload = {"contexts": ["Rust format (hard gate)", "audit"]}
        self.assertEqual(self.run_checker(payload), 0)

    def test_protected_context_absent_from_the_document_is_a_violation(self):
        payload = self.checks(
            ("Rust format (hard gate)", 15368),
            ("audit", 15368),
            ("Session Evidence", 15368),
        )
        code, errors = self.run_capturing(payload)
        self.assertEqual(code, 1)
        self.assertIn("Session Evidence", errors)
        self.assertIn("does not declare it", errors)

    def test_declared_context_absent_from_protection_is_a_violation(self):
        payload = self.checks(("audit", 15368))
        code, errors = self.run_capturing(payload)
        self.assertEqual(code, 1)
        self.assertIn("Rust format (hard gate)", errors)
        self.assertIn("does not require it", errors)

    def test_equal_counts_with_different_names_is_a_violation(self):
        # Kills a count-only comparison: two on each side, one name each way.
        payload = self.checks(("Rust format (hard gate)", 15368), ("lint", 15368))
        code, errors = self.run_capturing(payload)
        self.assertEqual(code, 1)
        self.assertIn("audit", errors)
        self.assertIn("lint", errors)

    def test_the_two_sets_are_printed_so_the_difference_is_visible(self):
        payload = self.checks(("audit", 15368), ("lint", 15368))
        _, errors = self.run_capturing(payload)
        self.assertIn("declared (2)", errors)
        self.assertIn("protected (2)", errors)

    def test_transport_failure_is_incomplete_not_pass(self):
        code = self.run_checker(
            error=checker.ProtectionUnavailable("GitHub API HTTP 503")
        )
        self.assertEqual(code, 2)

    def test_transport_failure_message_says_protection_cannot_be_verified(self):
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            checker.main(
                self.root,
                check_protection=True,
                fetch=lambda path: (_ for _ in ()).throw(
                    checker.ProtectionUnavailable("GitHub API HTTP 503")
                ),
            )
        self.assertIn("INCOMPLETE", errors.getvalue())
        self.assertIn("protection cannot be verified", errors.getvalue())

    def test_unexpected_payload_shape_is_incomplete(self):
        self.assertEqual(self.run_checker({"unexpected": True}), 2)
        self.assertEqual(self.run_checker([]), 2)

    def test_missing_token_is_incomplete_when_protection_was_requested(self):
        # Uses the real fetch so the token check runs; no network is reached
        # because the token is absent before a request is built.
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("GITHUB_TOKEN", None)
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                code = checker.main(self.root, check_protection=True)
        self.assertEqual(code, 2)

    def test_request_targets_the_branch_protection_endpoint(self):
        requests = []
        payload = self.checks(("Rust format (hard gate)", 15368), ("audit", 15368))
        self.run_checker(payload, requests=requests)
        self.assertEqual(len(requests), 1)
        self.assertIn("/branches/main/protection/required_status_checks", requests[0])
        self.assertIn("oahcom/AiMemoryBrainArchitecture", requests[0])

    def test_branch_is_configurable(self):
        requests = []

        def fetch(path):
            requests.append(path)
            return self.checks(("Rust format (hard gate)", 15368), ("audit", 15368))

        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            checker.main(self.root, branch="release", check_protection=True, fetch=fetch)
        self.assertIn("/branches/release/", requests[0])

    def test_app_binding_is_reported_because_it_is_not_compared(self):
        # Name-only comparison: the document names no App, so the App that must
        # produce the context is reported rather than silently ignored.
        payload = self.checks(("Rust format (hard gate)", 4242), ("audit", 4242))
        code, errors = self.run_capturing(payload)
        self.assertEqual(code, 0)
        self.assertIn("4242", errors)

    def test_skipped_reverse_check_says_so_and_does_not_claim_protection(self):
        errors = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(errors):
            self.assertEqual(checker.main(self.root), 0)
        output = errors.getvalue()
        self.assertIn("reverse check skipped", output)
        # It must not report a protected set it never read.
        self.assertNotIn("protected checks on", output)

    def test_forward_violation_still_fails_with_protection_requested(self):
        self.write(".github/workflows/gates.yml", WORKFLOW.replace(
            "Rust format (hard gate)", "Rust format (renamed)"
        ))
        payload = self.checks(("Rust format (hard gate)", 15368), ("audit", 15368))
        self.assertEqual(self.run_checker(payload), 1)


if __name__ == "__main__":
    unittest.main()
