#!/usr/bin/env python3
"""Self-check for scripts/check_required_contexts_merge_group.py.

Each case builds the smallest tree the checker reads: the declaring document and
one or two workflows. A case fails if the checker returns the wrong exit code or
stops naming the evidence.
"""

from __future__ import annotations

import contextlib
import io
import tempfile
import textwrap
import unittest
from pathlib import Path

import check_required_contexts_merge_group as gate

DOC = """\
<!-- declared-check-contexts: read by scripts/check_declared_check_contexts.py -->
```text
Gate one
Gate two
```
"""

WORKFLOW = """\
name: Fixture
on:
  pull_request:
{events}
jobs:
  gate:
    name: Gate one
    runs-on: ubuntu-latest
    steps:
      - run: "true"
  second:
    name: Gate two
    runs-on: ubuntu-latest
    steps:
      - run: "true"
"""

SERIALIZED = """\
name: Architecture document management gate
concurrency:
  group: ${{{{ github.workflow }}}}-{group}
  cancel-in-progress: false
{queue}
on:
  pull_request:
  merge_group:
    types: [checks_requested]
jobs:
  document-management:
    name: Gate one
    runs-on: ubuntu-latest
    steps:
      - run: "true"
  second:
    name: Gate two
    runs-on: ubuntu-latest
    steps:
      - run: "true"
"""

MERGE_GROUP = """\
  merge_group:
    types: [checks_requested]
"""

FULL_GROUP = (
    "${{ github.event.pull_request.base.ref || "
    "github.event.merge_group.base_ref || github.ref }}"
)


class GateTest(unittest.TestCase):
    def run_gate(self, files: dict[str, str]) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "14-ai-development").mkdir()
            (root / "14-ai-development/PR-GOVERNANCE-001.md").write_text(
                DOC, encoding="utf-8"
            )
            (root / ".github/workflows").mkdir(parents=True)
            for name, text in files.items():
                (root / ".github/workflows" / name).write_text(
                    textwrap.dedent(text), encoding="utf-8"
                )
            error = io.StringIO()
            with contextlib.redirect_stderr(error):
                code = gate.main(root)
            return code, error.getvalue()

    def serialized(self, group: str = FULL_GROUP, queue: str = "  queue: max") -> str:
        return SERIALIZED.format(group=group, queue=queue)

    def test_missing_merge_group_is_a_violation(self):
        code, error = self.run_gate({"fixture.yml": WORKFLOW.format(events="")})
        self.assertEqual(code, 1, error)
        self.assertIn("no `merge_group` entry", error)
        self.assertIn("fixture.yml:", error)

    def test_wrong_merge_group_type_is_a_violation(self):
        events = "  merge_group:\n    types: [some_other_event]\n"
        code, error = self.run_gate({"fixture.yml": WORKFLOW.format(events=events)})
        self.assertEqual(code, 1, error)
        self.assertIn("does not request `checks_requested`", error)

    def test_merge_group_subscription_passes(self):
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events=MERGE_GROUP)}
        )
        self.assertEqual(code, 0, error)
        self.assertIn("PASS (2 contexts)", error)

    def test_serialization_requires_queue_max_and_base_ref(self):
        cases = {
            "no queue": self.serialized(queue=""),
            "ref_name": self.serialized(group="github.ref_name"),
            "no push selector": self.serialized(
                group="${{ github.event.pull_request.base.ref || "
                "github.event.merge_group.base_ref }}"
            ),
        }
        for label, text in cases.items():
            with self.subTest(label):
                code, error = self.run_gate({"document-management.yml": text})
                self.assertEqual(code, 1, error)

    def test_serialized_document_management_passes(self):
        code, error = self.run_gate({"document-management.yml": self.serialized()})
        self.assertEqual(code, 0, error)

    def test_wrong_context_count_comment_is_a_violation(self):
        text = "# Seven required contexts live in this file.\n" + WORKFLOW.format(
            events=MERGE_GROUP
        )
        code, error = self.run_gate({"fixture.yml": text})
        self.assertEqual(code, 1, error)
        self.assertIn("the comment claims 7 required contexts", error)

    def test_correct_context_count_comment_passes(self):
        text = "# Two required contexts live in this file.\n" + WORKFLOW.format(
            events=MERGE_GROUP
        )
        code, error = self.run_gate({"fixture.yml": text})
        self.assertEqual(code, 0, error)


if __name__ == "__main__":
    unittest.main()
