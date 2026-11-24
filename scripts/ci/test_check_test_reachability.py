#!/usr/bin/env python3
"""Self-check for check_test_reachability.py.

Each case builds a throwaway tree, so the cases state what the gate promises
rather than what today's repository happens to contain. The last case runs the
gate against the real repository and asserts it is green, which is the property
the required gate depends on.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).with_name("check_test_reachability.py")
REPO = GATE.parent.parent.parent


def run(root):
    result = subprocess.run(
        [sys.executable, str(GATE), str(root)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


class ReachabilityTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".github" / "workflows").mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def workflow(self, body, name="w.yml"):
        (self.root / ".github" / "workflows" / name).write_text(body, encoding="utf-8")

    def test_unreachable_test_fails(self):
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_x.py").write_text("", encoding="utf-8")
        self.workflow("jobs:\n  a:\n    steps:\n      - run: echo hi\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("pkg/test_x.py", out)
        self.assertIn("1 of 1", err)

    def test_discover_root_reaches_test(self):
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_x.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 -m unittest discover -s pkg\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)
        self.assertIn("0 unreachable", err)

    def test_discover_pattern_excludes_and_includes(self):
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_keep.py").write_text("", encoding="utf-8")
        (self.root / "pkg" / "test_skip.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 -m unittest discover -s pkg -p 'test_keep*.py'\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn("pkg/test_skip.py", out)
        self.assertNotIn("pkg/test_keep.py", out)

    def test_quoted_pattern_is_unquoted(self):
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_a.py").write_text("", encoding="utf-8")
        self.workflow('      - run: python -m unittest discover -s pkg -p "test_*.py" -v\n')
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)

    def test_explicit_module_path_reaches_test(self):
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_x.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 -m unittest pkg.test_x\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)

    def test_explicit_script_path_reaches_test(self):
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_x.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 pkg/test_x.py\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)

    def test_root_relative_to_working_directory_is_resolved_by_suffix(self):
        # The real case: `-s provider_outcome` while the step runs inside
        # 08-bmcp-protocol/tests/conformance/.
        deep = self.root / "a" / "b" / "conformance" / "provider_outcome"
        deep.mkdir(parents=True)
        (deep / "test_p.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 -m unittest discover -s provider_outcome\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)

    def test_ambiguous_discovery_root_fails_closed(self):
        for name in ("one", "two"):
            d = self.root / name / "same"
            d.mkdir(parents=True)
            (d / "test_p.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 -m unittest discover -s same\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 2)
        self.assertIn("ambiguous", err)

    def test_escaping_discovery_root_fails_closed(self):
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_x.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 -m unittest discover -s ../elsewhere\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 2)
        self.assertIn("escapes repository", err)

    def test_missing_workflows_directory_fails_closed(self):
        empty = self.root / "bare"
        empty.mkdir()
        (empty / "test_x.py").write_text("", encoding="utf-8")
        code, out, err = run(empty)
        self.assertEqual(code, 2)
        self.assertIn("no .github/workflows", err)

    def test_too_many_arguments_is_usage_error(self):
        result = subprocess.run(
            [sys.executable, str(GATE), "a", "b"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 2)

    def test_real_repository_is_fully_reachable(self):
        """The property the required gate relies on: nothing is orphaned today."""
        code, out, err = run(REPO)
        self.assertEqual(code, 0, out + err)
        self.assertIn("0 unreachable", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
