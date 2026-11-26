#!/usr/bin/env python3
"""Self-check for check_manifest_parse.py.

Each case builds a throwaway tree, so the cases state what the gate promises
rather than what today's repository happens to contain. The last case runs the
gate over the real repository, which is the property the required gate relies
on: every committed manifest parses, and the printed count is the file count.

The four AID-2026-023/-029/-040/-055 cases reproduce the original defects that
b34c8e37 repaired. Naming the ids here means reintroducing one is a visible
regression of this work item, not a silent re-acquisition of the old state.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

GATE = Path(__file__).with_name("check_manifest_parse.py")
REPO = GATE.parents[2]
MANIFESTS = "14-ai-development/work-items"


def run(root):
    result = subprocess.run(
        [sys.executable, str(GATE), str(root)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


class ManifestParseTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        # Resolve once: the gate resolves its root argument, and on Windows the
        # unresolved temp path carries an 8.3 short name (ADMINI~1) that would
        # not be a substring of the reported path.
        self.root = Path(self._tmp.name).resolve()

    def tearDown(self):
        self._tmp.cleanup()

    def manifest(self, text, work_item_id="AID-2026-900"):
        path = self.root / MANIFESTS / work_item_id / "manifest.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    # AC1 -- parse every manifest and print the count.
    def test_counts_every_manifest_file(self):
        self.manifest("work_item_id: AID-2026-901\n", "AID-2026-901")
        self.manifest("work_item_id: AID-2026-902\n", "AID-2026-902")
        # A committed manifest that is not an AID id must be counted too: the
        # check globs, so no name-based exclusion rule can creep in.
        self.manifest("work_item_id: FIX-2026-P1-T1\n", "FIX-2026-P1-T1")
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)
        self.assertIn("3 manifests found", out)

    def test_no_manifest_found_fails_closed(self):
        self.root.mkdir(parents=True, exist_ok=True)
        code, out, err = run(self.root)
        self.assertEqual(code, 2)
        self.assertIn("nothing was verified", err)

    def test_too_many_arguments_is_usage_error(self):
        result = subprocess.run(
            [sys.executable, str(GATE), "a", "b"], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 2)

    # AC2 -- a duplicate key fails even where the default loader accepts it.
    def test_duplicate_top_level_key_rejected_where_safe_load_accepts(self):
        text = "work_item_id: AID-2026-901\nwork_item_id: AID-2026-902\n"
        self.assertIsInstance(yaml.safe_load(text), dict)
        path = self.manifest(text)
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(str(path), err)
        self.assertIn("duplicate key", err)

    def test_duplicate_nested_key_rejected_where_safe_load_accepts(self):
        text = "review:\n  status: PASS\n  status: FAIL\n"
        self.assertIsInstance(yaml.safe_load(text), dict)
        path = self.manifest(text)
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(str(path), err)
        self.assertIn("duplicate key", err)

    # AC3 -- a syntax error fails and the offending path is named.
    def test_unquoted_colon_scalar_fails_and_names_path(self):
        text = (
            "work_item_id: AID-2026-901\n"
            "implementing_ai_session: CURRENT (session identity: NOT_RECORDED)\n"
        )
        path = self.manifest(text)
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(str(path), err)

    def test_every_failing_path_is_reported_not_just_the_first(self):
        first = self.manifest("bad: a: b\n", "AID-2026-901")
        second = self.manifest("bad: c: d\n", "AID-2026-902")
        code, out, err = run(self.root)
        self.assertEqual(code, 1)
        self.assertIn(str(first), err)
        self.assertIn(str(second), err)

    # AC5 -- the passing run states what it did not verify.
    def test_passing_run_states_scope_limit(self):
        self.manifest("work_item_id: AID-2026-901\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)
        self.assertIn("parseability and duplicate keys only", out)
        self.assertIn("does not validate field values", out)

    # AC6 -- the four defects b34c8e37 repaired, one fixture each.
    def test_aid_2026_023_unquoted_colon_scalar_is_rejected(self):
        """L18 was: implementing_ai_session: CURRENT_DESIGN_SESSION (session identity: NOT_RECORDED)"""
        path = self.manifest(
            "work_item_id: AID-2026-023\n"
            "implementing_ai_session: CURRENT_DESIGN_SESSION "
            "(session identity: NOT_RECORDED)\n",
            "AID-2026-023",
        )
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(str(path), err)

    def test_aid_2026_040_unquoted_colon_scalar_is_rejected(self):
        """L15/L16 had two unquoted scalars, each containing a quoted sentence."""
        path = self.manifest(
            "work_item_id: AID-2026-040\n"
            'sponsor: USER-PRINCIPAL-DELEGATED (per the instruction: "OK")\n',
            "AID-2026-040",
        )
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(str(path), err)

    def test_aid_2026_029_duplicate_related_prs_is_rejected(self):
        text = (
            "work_item_id: AID-2026-029\n"
            "related_prs: [356]\n"
            "related_prs: []\n"
        )
        self.assertIsInstance(yaml.safe_load(text), dict)
        path = self.manifest(text, "AID-2026-029")
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(str(path), err)
        self.assertIn("duplicate key", err)

    def test_aid_2026_055_unescaped_nested_quote_is_rejected(self):
        text = (
            "work_item_id: AID-2026-055\n"
            "deliverables:\n"
            '  - "withdrawn: "Branch protection on main updated"."\n'
        )
        path = self.manifest(text, "AID-2026-055")
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(str(path), err)

    # AC1/AC6 -- the real tree.
    def test_real_repository_parses_and_count_matches_file_count(self):
        # The exact number is deliberately not pinned: a test that fails when
        # someone registers a work item is a test people delete. Assert the
        # relationship instead -- the printed count is the number of manifest
        # files actually present, and that number is a real corpus.
        expected = sorted((REPO / MANIFESTS).glob("*/manifest.yaml"))
        self.assertGreaterEqual(len(expected), 50, "manifest corpus is suspiciously small")
        code, out, err = run(REPO)
        self.assertEqual(code, 0, out + err)
        self.assertIn(f"{len(expected)} manifests found", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
