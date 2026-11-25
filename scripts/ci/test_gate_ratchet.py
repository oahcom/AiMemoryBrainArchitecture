#!/usr/bin/env python3
"""Self-check for scripts/ci/gate_ratchet.py.

Runs the real wrapper against real baseline files. The defect pinned here: a
wrapped command that exits non-zero and prints nothing used to produce
`regressions=0 fixed=0` and PASS with exit 0 when the baseline was empty, so a
crashed gate read as a clean run. Only stdout was ever inspected.

    python3 scripts/ci/test_gate_ratchet.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).resolve().parent / "gate_ratchet.py"


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


if __name__ == "__main__":
    unittest.main()
