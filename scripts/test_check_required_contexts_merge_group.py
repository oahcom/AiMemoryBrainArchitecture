#!/usr/bin/env python3
"""Self-check for scripts/check_required_contexts_merge_group.py.

Each case builds the smallest tree the checker reads: the declaring document and
one or two workflows, plus an injected platform-required set. No case reaches the
network: `protection=` is the injection point `main()` already provides.
"""

from __future__ import annotations

import contextlib
import io
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

import check_required_contexts_merge_group as gate

DOC = """\
<!-- declared-check-contexts: read by scripts/check_declared_check_contexts.py -->
```text
Gate one
Gate two
Gate three
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
  third:
    name: Gate three
    runs-on: ubuntu-latest
    steps:
      - run: "true"
"""

# The concurrency shape AID-2026-013 put on main (0962fbdc5): workflow, event
# and PR number, with github.ref_name as the non-PR fallback.
ISOLATED = """\
name: Architecture document management gate
concurrency:
  group: {group}
  cancel-in-progress: {cancel}
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

MAIN_GROUP = (
    "${{ github.workflow }}-${{ github.event_name }}-"
    "${{ github.event.pull_request.number || github.ref_name }}"
)

MERGE_GROUP = """\
  merge_group:
    types: [checks_requested]
"""


class GateTest(unittest.TestCase):
    def run_gate(
        self,
        files: dict[str, str],
        protection: list[str] | None = None,
        fetch_error: Exception | None = None,
    ) -> tuple[int, str]:
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
                if fetch_error is not None:
                    with mock.patch.object(
                        gate, "fetch_protected_contexts", side_effect=fetch_error
                    ):
                        code = gate.main(root)
                else:
                    code = gate.main(root, protection=protection)
            return code, error.getvalue()

    def isolated(self, group: str = MAIN_GROUP, cancel: str = "false",
                 queue: str = "") -> str:
        return ISOLATED.format(group=group, cancel=cancel, queue=queue)

    def test_required_context_without_merge_group_is_a_violation(self):
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events="")},
            protection=["Gate one"],
        )
        self.assertEqual(code, 1, error)
        self.assertIn("no `merge_group` entry", error)
        self.assertIn("fixture.yml:", error)

    def test_wrong_merge_group_type_is_a_violation(self):
        events = "  merge_group:\n    types: [some_other_event]\n"
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events=events)},
            protection=["Gate one"],
        )
        self.assertEqual(code, 1, error)
        self.assertIn("does not request `checks_requested`", error)

    def test_declared_but_not_required_context_is_exempt(self):
        """The 17/16 regression: an extra declared context needs no wiring."""
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events=MERGE_GROUP)},
            protection=["Gate one"],
        )
        self.assertEqual(code, 0, error)
        self.assertIn("DECLARED BUT NOT PLATFORM-REQUIRED: 2", error)
        self.assertIn("PASS (1 platform-required contexts)", error)

    def test_required_context_without_producer_is_a_violation(self):
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events=MERGE_GROUP)},
            protection=["Gate one", "Not produced"],
        )
        self.assertEqual(code, 1, error)
        self.assertIn("no job under", error)

    def test_second_producer_can_satisfy_the_requirement(self):
        other = """\
        name: Other
        on:
          merge_group:
            types: [checks_requested]
        jobs:
          alias:
            name: Gate one
            runs-on: ubuntu-latest
            steps:
              - run: "true"
        """
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events=""), "other.yml": other},
            protection=["Gate one"],
        )
        self.assertEqual(code, 0, error)

    def test_empty_platform_set_is_incomplete(self):
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events=MERGE_GROUP)},
            protection=[],
        )
        self.assertEqual(code, 2, error)
        self.assertIn("missing, empty, or malformed", error)

    def test_duplicate_platform_contexts_are_incomplete(self):
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events=MERGE_GROUP)},
            protection=["Gate one", "Gate one"],
        )
        self.assertEqual(code, 2, error)
        self.assertIn("duplicates", error)

    def test_unreadable_platform_set_is_incomplete(self):
        code, error = self.run_gate(
            {"fixture.yml": WORKFLOW.format(events=MERGE_GROUP)},
            fetch_error=OSError("connection refused"),
        )
        self.assertEqual(code, 2, error)
        self.assertIn("could not be read", error)

    def test_main_concurrency_isolation_passes(self):
        code, error = self.run_gate(
            {"document-management.yml": self.isolated()},
            protection=["Gate one"],
        )
        self.assertEqual(code, 0, error)

    def test_isolation_tokens_are_required(self):
        cases = {
            "no event_name": self.isolated(
                group="${{ github.workflow }}-${{ github.event.pull_request.number || github.ref_name }}"
            ),
            "no pr number": self.isolated(
                group="${{ github.workflow }}-${{ github.event_name }}-${{ github.ref_name }}"
            ),
            "no ref_name fallback": self.isolated(
                group="${{ github.workflow }}-${{ github.event_name }}-${{ github.event.pull_request.number }}"
            ),
        }
        for label, text in cases.items():
            with self.subTest(label):
                code, error = self.run_gate(
                    {"document-management.yml": text}, protection=["Gate one"]
                )
                self.assertEqual(code, 1, error)

    def test_queue_and_target_branch_are_rejected(self):
        cases = {
            "queue max": self.isolated(queue="  queue: max"),
            "base_ref": self.isolated(
                group="${{ github.workflow }}-${{ github.event_name }}-"
                "${{ github.event.pull_request.number || github.ref_name }}-"
                "${{ github.event.merge_group.base_ref }}"
            ),
            "pull_request base": self.isolated(
                group="${{ github.workflow }}-${{ github.event_name }}-"
                "${{ github.event.pull_request.number || github.ref_name }}-"
                "${{ github.event.pull_request.base.ref }}"
            ),
            "github.ref": self.isolated(
                group="${{ github.workflow }}-${{ github.event_name }}-"
                "${{ github.event.pull_request.number || github.ref }}"
            ),
            "cancel in progress": self.isolated(cancel="true"),
        }
        for label, text in cases.items():
            with self.subTest(label):
                code, error = self.run_gate(
                    {"document-management.yml": text}, protection=["Gate one"]
                )
                self.assertEqual(code, 1, error)

    def test_wrong_context_count_comment_is_a_violation(self):
        text = "# Seven required contexts live in this file.\n" + WORKFLOW.format(
            events=MERGE_GROUP
        )
        code, error = self.run_gate({"fixture.yml": text}, protection=["Gate one"])
        self.assertEqual(code, 1, error)
        self.assertIn("the comment claims 7 required contexts", error)

    def test_correct_context_count_comment_passes(self):
        text = "# Three required contexts live in this file.\n" + WORKFLOW.format(
            events=MERGE_GROUP
        )
        code, error = self.run_gate({"fixture.yml": text}, protection=["Gate one"])
        self.assertEqual(code, 0, error)


if __name__ == "__main__":
    unittest.main()
