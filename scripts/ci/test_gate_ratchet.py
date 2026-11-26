#!/usr/bin/env python3
"""Self-check for scripts/ci/gate_ratchet.py.

Runs the real wrapper against real baseline files. The defect pinned here: a
wrapped command that exits non-zero and prints nothing used to produce
`regressions=0 fixed=0` and PASS with exit 0 when the baseline was empty, so a
crashed gate read as a clean run. Only stdout was ever inspected.

    python3 scripts/ci/test_gate_ratchet.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).resolve().parent / "gate_ratchet.py"

# Relative to this file: scripts/ci/ -> repository root.
REPO_ROOT = Path(__file__).resolve().parents[2]
GATES_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "gates.yml"
BILINGUAL_BASELINE = REPO_ROOT / "scripts" / "ci" / "baselines" / "bilingual-docs.txt"

# The prose claim being pinned: "# GOV-DOC-001 full scan: <n> normative paths".
STATED_COUNT = re.compile(
    r"^[ \t]*#[ \t]*GOV-DOC-001 full scan:[ \t]*(\d+)[ \t]+normative paths",
    re.MULTILINE,
)


def baseline_entries(text: str) -> list[str]:
    """The set gate_ratchet.py builds: non-blank, non-comment, deduplicated."""
    return sorted(
        {
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        }
    )


def python(*body: str) -> str:
    """A --command that runs this interpreter, quoted for both sh and cmd."""
    statements = "; ".join(body)
    return f'"{sys.executable}" -c "{statements}"'


def run_gate(baseline_text: str, command: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        baseline = Path(tmp) / "baseline.txt"
        baseline.write_text(baseline_text, encoding="utf-8")
        return subprocess.run(
            [
                sys.executable,
                str(GATE),
                "--baseline",
                str(baseline),
                "--format",
                "paths",
                "--command",
                command,
            ],
            capture_output=True,
            text=True,
        )


class GateRatchetTests(unittest.TestCase):
    def test_empty_baseline_with_nonzero_exit_and_no_output_fails(self):
        proc = run_gate("# no entries\n", python("import sys", "sys.exit(1)"))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("exited 1 without printing any item", proc.stdout)
        self.assertNotIn("PASS", proc.stdout)

    def test_empty_baseline_with_clean_exit_and_no_output_passes(self):
        proc = run_gate("# no entries\n", python("import sys", "sys.exit(0)"))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS", proc.stdout)

    def test_reported_failure_outside_the_baseline_is_a_regression(self):
        proc = run_gate(
            "a.md\n",
            python("print('b.md')", "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("ratchet regression", proc.stdout)

    def test_exact_match_with_nonzero_exit_still_passes(self):
        proc = run_gate(
            "a.md\n",
            python("print('a.md')", "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS", proc.stdout)

    def test_baseline_item_that_no_longer_fails_is_stale(self):
        proc = run_gate("a.md\n", python("import sys", "sys.exit(0)"))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("lower the baseline", proc.stdout)

    def test_exit_status_outside_zero_one_is_not_comparable(self):
        proc = run_gate(
            "a.md\n",
            python("print('a.md')", "import sys", "sys.exit(2)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("only 0 (clean) and 1 (red)", proc.stdout)


class CommentedCountTests(unittest.TestCase):
    """gates.yml states a count that nothing else compared (issue #1081).

    The comment said 81 while the baseline it describes held 77 entries. This
    compares the two numbers only: the ratchet is allowed to be red on main, so
    the wrapped gate is never run here and no pass/fail is asserted about it.
    """

    def test_stated_count_matches_baseline_entries(self):
        workflow = GATES_WORKFLOW.read_text(encoding="utf-8")
        baseline = BILINGUAL_BASELINE.read_text(encoding="utf-8")

        stated = STATED_COUNT.findall(workflow)
        self.assertEqual(
            len(stated),
            1,
            "gates.yml must state the GOV-DOC-001 count exactly once",
        )

        entries = baseline_entries(baseline)
        self.assertEqual(
            int(stated[0]),
            len(entries),
            f"gates.yml says {stated[0]} normative paths; "
            f"{BILINGUAL_BASELINE.name} has {len(entries)} entries",
        )


def main() -> None:
    # 0 = pass, 1 = violation, 2 = incomplete. unittest owns 0 and 1; an
    # artifact that cannot be read must not be reported as a violation.
    for path in (GATES_WORKFLOW, BILINGUAL_BASELINE):
        try:
            path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"INCOMPLETE: {exc}", file=sys.stderr)
            sys.exit(2)
    unittest.main()


if __name__ == "__main__":
    main()
