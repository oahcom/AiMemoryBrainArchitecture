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
import re
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

    def test_head_job_checkout_with_ref_names_the_ref_line(self):
        # The bare `ref:` token also appears in the prose of the message, so the
        # assertion above held even when the parenthetical quoted the correct
        # `uses:` line. Pin the value, not the token.
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
        self.assertIn(
            "ref: ${{ github.event.pull_request.base.sha }}", message
        )

    def test_validate_needs_is_a_violation(self):
        self.write(WORKFLOW.replace(
            "  validate:\n    name: Session Evidence\n",
            "  validate:\n    name: Session Evidence\n    needs: self-test-pr-head\n",
        ))
        code, message = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("validate", message)
        self.assertIn("needs:", message)

    def test_validate_block_form_needs_is_a_violation_naming_the_needs_line(self):
        # #1058. YAML block form puts the value on the following lines, so the
        # key line ends at the colon. A regex that requires a token after the
        # colon matches only the flow form and lets the block form through,
        # silently -- the dependency it forbids is exactly as present.
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
        # The line number, not the job name, is what locates the offending key.
        self.assertIn(f"(line {needs_line}: needs:)", message)
        self.assertNotIn(f"(line {job_line}:", message)

    def test_ref_violation_quotes_the_ref_line_and_not_the_uses_line(self):
        # #1045. The step's `uses:` line is the one line in a checkout step that
        # is already correct, so quoting it sends the reader to look for a
        # `ref:` that is not there. The negative assertion is the direction:
        # naming `ref:` in the prose of the message is not enough.
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

    def test_ref_in_the_base_job_is_allowed(self):
        # The base job SHALL read the base revision; only the head job may not.
        self.write(WORKFLOW)
        self.assertIn(
            "ref: ${{ github.event.pull_request.base.sha }}",
            WORKFLOW,
        )
        self.assertEqual(self.run_checker()[0], 0)

    def test_trigger_without_edited_is_a_violation_naming_edited_and_its_line(self):
        # #1074. The validator reads the PR body live, so a trigger that does not
        # re-run on `edited` leaves a verdict describing text that no longer
        # exists. The default set omits `edited`, so the key must say so.
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
        # The anti-regression case for #1045's bug class. A guard that reads only
        # the flow form would reject this correct file, which is the failure the
        # `needs:` regex already had once in this same script.
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

    def test_the_repository_itself_passes(self):
        # The shape is a claim about this tree; hold it to that.
        self.assertEqual(checker.main(REPO), 0)

    def test_the_types_trigger_does_not_break_the_three_job_invariants(self):
        # #1074 added `types:` under `pull_request:`. That is a nested mapping
        # inside the `on:` block, so it must not be read as a job, and it must
        # not smuggle a `ref:` or `needs:` into a job. The other cases in this
        # class run against the same fixture, so they now also prove the
        # invariants still hold with the trigger present; this one names it.
        self.assertIn("    types: [opened, synchronize, reopened, edited]\n", WORKFLOW)
        self.write(WORKFLOW)
        code, message = self.run_checker()
        self.assertEqual(code, 0)
        self.assertNotIn("::error::", message)
        self.assertIn("three independent jobs", message)

    def test_the_repository_trigger_includes_edited(self):
        # #1074: `edited` is not a GitHub default activity type, so without it
        # a body edit after a run schedules nothing and the verdict keeps
        # describing text that no longer exists. Removing it from the real
        # workflow must fail here, not pass silently.
        text = (REPO / WORKFLOW_PATH).read_text(encoding="utf-8")
        self.assertIn("edited", self.pull_request_types(text))

    @staticmethod
    def pull_request_types(text):
        """The activity types declared for the `pull_request` trigger.

        Comment lines between the trigger key and `types:` are skipped, so the
        pin still reads the real workflow where the rationale sits inline.
        """
        match = re.search(
            r"^  pull_request:\s*$((?:\n[ \t]*(?:#[^\n]*)?)*?)\n[ \t]*types:\s*\[([^\]]*)\]",
            text,
            re.MULTILINE,
        )
        return [item.strip() for item in match.group(2).split(",")] if match else []


if __name__ == "__main__":
    unittest.main()
