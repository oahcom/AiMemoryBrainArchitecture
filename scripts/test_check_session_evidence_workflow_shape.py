#!/usr/bin/env python3
"""Self-check for check_session_evidence_workflow_shape.

Run with: python3 scripts/test_check_session_evidence_workflow_shape.py

Each case builds a throwaway tree so the mutation is the only thing that can
move the verdict, and each asserts on message text, not only the exit code.
The incomplete cases must say INCOMPLETE (2), never PASS (0).
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
    types: [opened, synchronize, reopened, edited]
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
      - name: Bind the verdict to the body it judged
        if: always()
        run: |
          if ! digest=$(curl example | python3 -c 'import hashlib')
          then
            exit 1
          fi
          if ! printf '%s' "$digest" | grep -Eq '^[0-9a-f]{64}$'; then
            exit 1
          fi
          echo "AI-SESSION-EVIDENCE-BODY-SHA256: $digest" >> "$GITHUB_STEP_SUMMARY"
      - name: Ensure job summary contains a verdict
        if: always()
        run: echo "AI-SESSION-EVIDENCE: PRESENT" >> "$GITHUB_STEP_SUMMARY"
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
        """Return the exit code and stderr for this test tree."""
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
            i for i, line in enumerate(lines)
            if line.startswith("  self-test-pr-head:")
        )
        end = next(
            i for i, line in enumerate(lines)
            if line.startswith("  validate:")
        )
        self.write("\n".join(lines[:start] + lines[end:]))
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("self-test-pr-head", message)

    def test_head_job_checkout_with_ref_is_a_violation(self):
        mutated = WORKFLOW.replace(
            "      - name: Checkout PR head\n"
            "        uses: actions/checkout@v4\n"
            "        with:\n"
            "          persist-credentials: false\n",
            "      - name: Checkout PR head\n"
            "        uses: actions/checkout@v4\n"
            "        with:\n"
            "          ref: ${{ github.event.pull_request.base.sha }}\n"
            "          persist-credentials: false\n",
        )
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("self-test-pr-head", message)
        self.assertIn("ref:", message)

    def test_head_job_checkout_with_ref_names_the_ref_line(self):
        mutated = WORKFLOW.replace(
            "      - name: Checkout PR head\n"
            "        uses: actions/checkout@v4\n"
            "        with:\n"
            "          persist-credentials: false\n",
            "      - name: Checkout PR head\n"
            "        uses: actions/checkout@v4\n"
            "        with:\n"
            "          ref: ${{ github.event.pull_request.base.sha }}\n"
            "          persist-credentials: false\n",
        )
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn(
            "ref: ${{ github.event.pull_request.base.sha }}", message
        )

    def test_validate_needs_is_a_violation(self):
        self.write(WORKFLOW.replace(
            "  validate:\n    name: Session Evidence\n",
            "  validate:\n    name: Session Evidence\n"
            "    needs: self-test-pr-head\n",
        ))
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("validate", message)
        self.assertIn("needs:", message)

    def test_validate_block_form_needs_is_a_violation_naming_the_needs_line(self):
        block = WORKFLOW.replace(
            "  validate:\n    name: Session Evidence\n",
            "  validate:\n    name: Session Evidence\n"
            "    needs:\n      - self-test-pr-head\n",
        )
        self.write(block)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("`needs:`", message)
        needs_line = next(
            i for i, line in enumerate(block.splitlines(), 1)
            if line.strip() == "needs:"
        )
        job_line = next(
            i for i, line in enumerate(block.splitlines(), 1)
            if line.strip() == "validate:"
        )
        self.assertIn(f"(line {needs_line}: needs:)", message)
        self.assertNotIn(f"(line {job_line}:", message)

    def test_ref_violation_quotes_the_ref_line_and_not_the_uses_line(self):
        ref = "ref: ${{ github.event.pull_request.head.sha }}"
        mutated = WORKFLOW.replace(
            "      - name: Checkout PR head\n"
            "        uses: actions/checkout@v4\n"
            "        with:\n"
            "          persist-credentials: false\n",
            "      - name: Checkout PR head\n"
            "        uses: actions/checkout@v4\n"
            "        with:\n"
            f"          {ref}\n"
            "          persist-credentials: false\n",
        )
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        ref_line = next(
            i for i, line in enumerate(mutated.splitlines(), 1)
            if line.strip() == ref
        )
        self.assertIn(f"(line {ref_line}: {ref})", message)
        self.assertNotIn("uses: actions/checkout@v4", message)

    def test_deleting_the_validate_job_names_it_as_required(self):
        lines = WORKFLOW.splitlines()
        start = next(
            i for i, line in enumerate(lines)
            if line.startswith("  validate:")
        )
        self.write("\n".join(lines[:start]))
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("job id 'validate' is missing", message)

    def test_ref_in_the_base_job_is_allowed(self):
        self.write(WORKFLOW)
        self.assertIn(
            "ref: ${{ github.event.pull_request.base.sha }}",
            WORKFLOW,
        )
        self.assertEqual(self.run_checker()[0], 0)

    def test_trigger_without_edited_is_a_violation_naming_edited_and_its_line(self):
        mutated = WORKFLOW.replace(
            "    types: [opened, synchronize, reopened, edited]\n",
            "    types: [opened, synchronize, reopened]\n",
        )
        self.assertNotEqual(mutated, WORKFLOW)
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("edited", message)
        types_line = next(
            i for i, line in enumerate(mutated.splitlines(), 1)
            if line.strip() == "types: [opened, synchronize, reopened]"
        )
        self.assertIn(f"(line {types_line}:", message)

    def test_trigger_with_edited_in_flow_form_passes(self):
        self.write(WORKFLOW)
        self.assertIn("types: [opened, synchronize, reopened, edited]", WORKFLOW)
        code, message = self.run_checker()
        self.assertEqual(code, 0)
        self.assertNotIn("::error::", message)

    def test_trigger_with_edited_in_block_form_passes(self):
        block = WORKFLOW.replace(
            "    types: [opened, synchronize, reopened, edited]\n",
            "    types:\n"
            "      - opened\n"
            "      - synchronize\n"
            "      - reopened\n"
            "      - edited\n",
        )
        self.assertNotEqual(block, WORKFLOW)
        self.write(block)
        code, message = self.run_checker()
        self.assertEqual(code, 0)
        self.assertNotIn("::error::", message)

    def test_trigger_without_a_types_key_is_a_violation(self):
        mutated = WORKFLOW.replace(
            "    types: [opened, synchronize, reopened, edited]\n", ""
        )
        self.assertNotEqual(mutated, WORKFLOW)
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("no `types:` key", message)
        self.assertIn("edited", message)

    def test_incomplete_when_the_workflow_is_absent(self):
        self.assertEqual(self.run_checker()[0], 2)

    def test_incomplete_when_there_is_no_jobs_mapping(self):
        self.write("name: Session Evidence Gate\non:\n  pull_request:\n")
        self.assertEqual(self.run_checker()[0], 2)

    def test_repository_itself_passes(self):
        self.assertEqual(checker.main(REPO), 0)

    def test_body_digest_step_is_required(self):
        mutated = WORKFLOW.replace(
            "      - name: Bind the verdict to the body it judged\n"
            "        if: always()\n"
            "        run: |\n"
            "          if ! digest=$(curl example | python3 -c 'import hashlib')\n"
            "          then\n"
            "            exit 1\n"
            "          fi\n"
            "          if ! printf '%s' \"$digest\" | grep -Eq '^[0-9a-f]{64}$'; then\n"
            "            exit 1\n"
            "          fi\n"
            "          echo \"AI-SESSION-EVIDENCE-BODY-SHA256: $digest\" >> \"$GITHUB_STEP_SUMMARY\"\n",
            "",
        )
        self.assertNotEqual(mutated, WORKFLOW)
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("mutation 1", message)
        self.assertIn("Bind the verdict to the body it judged", message)
        self.assertIn("line", message)

    def test_body_digest_always_condition_is_required(self):
        mutated = WORKFLOW.replace(
            "        if: always()\n        run: |\n",
            "        if: success()\n        run: |\n",
            1,
        )
        self.assertNotEqual(mutated, WORKFLOW)
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("mutation 2", message)
        self.assertIn("always()", message)
        self.assertIn("line", message)

    def test_body_digest_expression_always_condition_passes(self):
        mutated = WORKFLOW.replace(
            "        if: always()\n        run: |\n",
            "        if: ${{ always() }}\n        run: |\n",
            1,
        )
        self.assertNotEqual(mutated, WORKFLOW)
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 0, message)
        self.assertNotIn("mutation 2", message)

    def test_body_digest_rejects_non_always_expressions(self):
        for condition in (
            "success()",
            "failure()",
            "${{ success() }}",
            "${{ failure() }}",
        ):
            with self.subTest(condition=condition):
                mutated = WORKFLOW.replace(
                    "        if: always()\n        run: |\n",
                    f"        if: {condition}\n        run: |\n",
                    1,
                )
                self.assertNotEqual(mutated, WORKFLOW)
                self.write(mutated)
                code, message = self.run_checker()
                self.assertEqual(code, 1)
                self.assertIn("mutation 2", message)
                self.assertIn("always()", message)
                self.assertIn("line", message)

    def test_body_digest_write_is_required(self):
        mutated = WORKFLOW.replace(
            'echo "AI-SESSION-EVIDENCE-BODY-SHA256: $digest" >> "$GITHUB_STEP_SUMMARY"',
            'echo "AI-SESSION-EVIDENCE: PRESENT" >> "$GITHUB_STEP_SUMMARY"',
        )
        self.assertNotEqual(mutated, WORKFLOW)
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("mutation 3", message)
        self.assertIn("AI-SESSION-EVIDENCE-BODY-SHA256", message)
        self.assertIn("line", message)

    def test_body_digest_hex_validation_is_independent(self):
        mutated = WORKFLOW.replace(
            "          if ! printf '%s' \"$digest\" | grep -Eq '^[0-9a-f]{64}$'; then\n",
            "          if ! printf '%s' \"$digest\" | grep -Eq '^[0-9a-f]{63}$'; then\n",
        )
        self.assertNotEqual(mutated, WORKFLOW)
        self.write(mutated)
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("64 lowercase hexadecimal", message)
        self.assertIn("line", message)


if __name__ == "__main__":
    unittest.main()
