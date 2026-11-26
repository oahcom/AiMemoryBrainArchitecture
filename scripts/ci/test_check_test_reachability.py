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
        self.baseline()

    def tearDown(self):
        self._tmp.cleanup()

    def workflow(self, body, name="w.yml"):
        (self.root / ".github" / "workflows" / name).write_text(body, encoding="utf-8")

    def baseline(self, *entries):
        """Write the gate-wiring baseline the checker requires."""
        path = self.root / "scripts" / "ci" / "baselines" / "gate-wiring.txt"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join("%s\n" % entry for entry in entries), encoding="utf-8")

    def gate(self, relative="scripts/check_thing.py"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
        return relative

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
        # Distinct filenames: identical ones would trip the stem-collision rule
        # first, and this case is about the ambiguous root, not about stems.
        for name in ("one", "two"):
            d = self.root / name / "same"
            d.mkdir(parents=True)
            (d / ("test_%s.py" % name)).write_text("", encoding="utf-8")
        self.workflow("      - run: python3 -m unittest discover -s same\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 2)
        self.assertIn("ambiguous", err)

    def test_shared_stem_fails_closed_with_both_paths(self):
        # Rule B matches by substring, so `scripts/ci/test_check_fmt.py` is
        # reported reachable whenever `scripts/test_check_fmt.py` is wired. The
        # gate must refuse to answer rather than answer wrongly.
        for parent in ("scripts", "scripts/ci"):
            directory = self.root / parent
            directory.mkdir(parents=True, exist_ok=True)
            (directory / "test_check_fmt.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 scripts/test_check_fmt.py\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn("scripts/test_check_fmt.py", err)
        self.assertIn("scripts/ci/test_check_fmt.py", err)
        self.assertIn("shared", err)

    def test_unique_stems_still_pass(self):
        # The collision check must not fire on the ordinary case.
        for parent, name in (("scripts", "test_a.py"), ("scripts/ci", "test_b.py")):
            directory = self.root / parent
            directory.mkdir(parents=True, exist_ok=True)
            (directory / name).write_text("", encoding="utf-8")
        self.workflow(
            "      - run: python3 scripts/test_a.py\n"
            "      - run: python3 scripts/ci/test_b.py\n"
        )
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)

    def test_real_repository_has_no_duplicate_stems(self):
        """The precondition Rule B depends on, asserted against the real tree."""
        stems = {}
        for test in REPO.rglob("test_*.py"):
            if ".git" in test.parts:
                continue
            stems.setdefault(test.stem, []).append(
                test.relative_to(REPO).as_posix()
            )
        collisions = {k: v for k, v in stems.items() if len(v) > 1}
        self.assertEqual(collisions, {})

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

    # --- gate-shaped scripts (#925) -------------------------------------

    def test_gate_referenced_only_in_a_comment_is_unwired(self):
        gate = self.gate()
        self.workflow(
            "jobs:\n"
            "  a:\n"
            "    steps:\n"
            "      # TODO: wire %s one day\n"
            "      - run: |\n"
            "          set -euo pipefail\n"
            "          # python3 %s would go here\n"
            "          echo hi\n" % (gate, gate)
        )
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(gate, out)
        self.assertIn("Gate wiring", err)

    def test_gate_whose_test_is_wired_but_gate_is_not(self):
        # The #899/#925 confusion: tests/test_policy_inheritance.py runs while
        # scripts/check_policy_inheritance.py runs nowhere.
        gate = self.gate("scripts/check_policy_inheritance.py")
        (self.root / "tests").mkdir()
        (self.root / "tests" / "test_policy_inheritance.py").write_text("", encoding="utf-8")
        self.workflow("      - run: python3 -m unittest tests/test_policy_inheritance.py\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(gate, out)
        self.assertNotIn("tests/test_policy_inheritance.py", out)

    def test_gate_invoked_in_a_run_block_is_wired(self):
        gate = self.gate()
        self.workflow("      - run: python3 %s\n" % gate)
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)
        self.assertIn("0 unreachable", err)
        self.assertIn("1 gate scripts, 0 unwired", err)

    def test_gate_in_a_block_scalar_run_is_wired_by_basename(self):
        self.gate("scripts/ci/check_thing.py")
        self.workflow(
            "      - run: |\n"
            "          set -euo pipefail\n"
            "          python3 -c 'import yaml'\n"
            "          cd scripts/ci\n"
            "          python3 check_thing.py\n"
        )
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)

    def test_new_unwired_gate_fails_and_names_the_script(self):
        gate = self.gate()
        self.workflow("      - run: echo hi\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(gate, out)
        self.assertIn("not in scripts/ci/baselines/gate-wiring.txt", err)

    def test_baselined_unwired_gate_is_tolerated(self):
        gate = self.gate()
        self.baseline(gate)
        self.workflow("      - run: echo hi\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)
        self.assertIn("1 gate scripts, 1 unwired, 1 baselined", err)

    def test_baseline_entry_that_became_wired_is_stale(self):
        gate = self.gate()
        self.baseline(gate)
        self.workflow("      - run: python3 %s\n" % gate)
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn("stale", err)
        self.assertIn(gate, err)
        # ... and it goes green only when the stale line is removed, not before.
        self.baseline()
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)
        self.assertIn("1 gate scripts, 0 unwired, 0 baselined", err)

    def test_unreadable_baseline_is_incomplete_not_pass(self):
        (self.root / "scripts" / "ci" / "baselines" / "gate-wiring.txt").unlink()
        self.workflow("      - run: echo hi\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 2, out + err)
        self.assertIn("gate-wiring baseline not found", err)

    def test_gate_under_a_sibling_directory_is_still_found(self):
        # No filename-prefix exclusion: a gate anywhere under scripts/ counts.
        gate = self.gate("scripts/governance/status_migration/check_status_gates.py")
        self.workflow("      - run: echo hi\n")
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn(gate, out)

    # --- comment-blind Rule B and the .yaml suffix (#1212) ---------------

    def test_test_named_only_in_a_comment_is_unreachable(self):
        """Rule B matches substrings, so a commented name used to count."""
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_x.py").write_text("", encoding="utf-8")
        self.workflow(
            "jobs:\n"
            "  a:\n"
            "    steps:\n"
            "      - run: echo hi\n"
            "      # TODO: run pkg/test_x.py once the fixture exists\n"
        )
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn("pkg/test_x.py", out)
        self.assertIn("1 of 1", err)

    def test_discover_in_a_comment_is_not_a_discovery_root(self):
        """The same reading applies to the discovery root, not only Rule B."""
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_x.py").write_text("", encoding="utf-8")
        self.workflow(
            "jobs:\n"
            "  a:\n"
            "    steps:\n"
            "      - run: echo hi\n"
            "      # - run: python3 -m unittest discover -s pkg\n"
        )
        code, out, err = run(self.root)
        self.assertEqual(code, 1, out + err)
        self.assertIn("pkg/test_x.py", out)

    def test_yaml_workflow_suffix_is_read_for_both_branches(self):
        """A `.yaml` workflow reaches tests and wires gates like a `.yml` one."""
        gate = self.gate()
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "test_x.py").write_text("", encoding="utf-8")
        self.workflow(
            "      - run: python3 -m unittest discover -s pkg\n"
            "      - run: python3 %s\n" % gate,
            name="w.yaml",
        )
        code, out, err = run(self.root)
        self.assertEqual(code, 0, out + err)
        self.assertIn("0 unreachable", err)
        self.assertIn("1 gate scripts, 0 unwired", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
