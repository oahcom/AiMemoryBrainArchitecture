#!/usr/bin/env python3
"""Regression tests for the base-anchored gate ratchet."""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).resolve().parent / "gate_ratchet.py"
REPO_ROOT = Path(__file__).resolve().parents[2]
GATES_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "gates.yml"
BILINGUAL_BASELINE = (
    REPO_ROOT / "scripts" / "ci" / "baselines" / "bilingual-docs.txt"
)
MANIFEST_BASELINE = (
    REPO_ROOT / "scripts" / "ci" / "baselines" / "manifest-blob-pins.txt"
)

BASELINES = {
    "bilingual-docs": "scripts/ci/baselines/bilingual-docs.txt",
    "manifest-blob-pins": (
        "scripts/ci/baselines/manifest-blob-pins.txt"
    ),
}

STATED_COUNT = re.compile(
    r"^[ \t]*#[ \t]*GOV-DOC-001 full scan:[ \t]*(\d+)[ \t]+normative paths",
    re.MULTILINE,
)


def baseline_entries(content: str) -> list[str]:
    return sorted({
        line.strip()
        for line in content.splitlines()
        if line.strip() and not line.strip().startswith("#")
    })


def python(*body: str) -> str:
    statements = "; ".join(body)
    return f'"{sys.executable}" -c "{statements}"'


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if proc.returncode:
        raise AssertionError(proc.stderr)
    return proc.stdout.strip()


def make_repo(
    base_text: str,
    candidate_text: str | None = None,
    *,
    baseline_id: str = "bilingual-docs",
    create_base_file: bool = True,
) -> tuple[tempfile.TemporaryDirectory, Path, str]:
    tmp = tempfile.TemporaryDirectory()
    repo = Path(tmp.name)
    git(repo, "init")
    git(repo, "config", "user.email", "ratchet-test@example.invalid")
    git(repo, "config", "user.name", "Ratchet Test")

    path = repo / BASELINES[baseline_id]
    path.parent.mkdir(parents=True, exist_ok=True)
    if create_base_file:
        path.write_text(base_text, encoding="utf-8")
        git(repo, "add", BASELINES[baseline_id])
    git(repo, "commit", "--allow-empty", "-m", "base")
    base_ref = git(repo, "rev-parse", "HEAD")

    if candidate_text is not None:
        path.write_text(candidate_text, encoding="utf-8")

    return tmp, repo, base_ref


def run_gate(
    base_text: str,
    candidate_text: str,
    command: str,
    *,
    baseline_id: str = "bilingual-docs",
    baseline_path: str | None = None,
    base_ref_override: str | None = None,
    create_base_file: bool = True,
) -> subprocess.CompletedProcess[str]:
    tmp, repo, base_ref = make_repo(
        base_text,
        candidate_text,
        baseline_id=baseline_id,
        create_base_file=create_base_file,
    )
    try:
        path = baseline_path or BASELINES[baseline_id]
        return subprocess.run(
            [
                sys.executable,
                str(GATE),
                "--baseline-ref",
                base_ref_override or base_ref,
                "--baseline-id",
                baseline_id,
                "--baseline",
                path,
                "--format",
                "paths",
                "--command",
                command,
            ],
            cwd=repo,
            capture_output=True,
            text=True,
        )
    finally:
        tmp.cleanup()


class GateRatchetTests(unittest.TestCase):
    def test_empty_baseline_with_nonzero_exit_and_no_output_fails(self):
        proc = run_gate(
            "# no entries\n",
            "# no entries\n",
            python("import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("without printing any item", proc.stdout)
        self.assertNotIn("PASS", proc.stdout)

    def test_empty_baseline_with_clean_exit_and_no_output_passes(self):
        proc = run_gate(
            "# no entries\n",
            "# no entries\n",
            python("import sys", "sys.exit(0)"),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS", proc.stdout)

    def test_reported_failure_outside_the_baseline_is_a_regression(self):
        proc = run_gate(
            "a.md\n",
            "a.md\n",
            python("print('b.md')", "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("ratchet regression", proc.stdout)

    def test_exact_match_with_nonzero_exit_still_passes(self):
        proc = run_gate(
            "a.md\n",
            "a.md\n",
            python("print('a.md')", "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS", proc.stdout)

    def test_baseline_item_that_no_longer_fails_is_stale(self):
        proc = run_gate(
            "a.md\n",
            "a.md\n",
            python("import sys", "sys.exit(0)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("lower the candidate baseline", proc.stdout)

    def test_exit_status_outside_zero_one_is_not_comparable(self):
        proc = run_gate(
            "a.md\n",
            "a.md\n",
            python("print('a.md')", "import sys", "sys.exit(2)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("only exit 0 and 1", proc.stdout)


class ItemFidelityTests(unittest.TestCase):
    def test_two_failures_on_one_path_stay_two_items(self):
        proc = run_gate(
            "a.md\n",
            "a.md\n",
            python(
                "print('a.md -> missing docs/en/a.md')",
                "print('a.md -> missing docs/zh-CN/a.md')",
                "import sys",
                "sys.exit(1)",
            ),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertEqual(
            proc.stdout.count("::error::ratchet regression"), 1, proc.stdout
        )
        self.assertIn("a.md -> missing docs/zh-CN/a.md", proc.stdout)

    def test_a_detail_change_is_a_regression_not_a_match(self):
        proc = run_gate(
            "a.md -> missing docs/en/a.md\n",
            "a.md -> missing docs/en/a.md\n",
            python(
                "print('a.md -> missing docs/zh-CN/a.md')",
                "import sys",
                "sys.exit(1)",
            ),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("ratchet regression", proc.stdout)
        self.assertIn("a.md -> missing docs/zh-CN/a.md", proc.stdout)

    def test_both_details_recorded_in_the_baseline_pass(self):
        entries = "a.md -> x\na.md -> y\n"
        proc = run_gate(
            entries,
            entries,
            python(
                "print('a.md -> x')",
                "print('a.md -> y')",
                "import sys",
                "sys.exit(1)",
            ),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("current=2 regressions=0 remaining_fixed=0", proc.stdout)

    def test_item_wearing_a_verdict_prefix_is_not_dropped(self):
        item = "OK 00-governance/a.md has no counterpart"
        proc = run_gate(
            "# nothing baselined\n",
            "# nothing baselined\n",
            python("print(" + repr(item) + ")", "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("ratchet regression", proc.stdout)
        self.assertIn(item, proc.stdout)

    def test_baselined_item_wearing_a_verdict_prefix_is_matched(self):
        item = "OK 00-governance/a.md has no counterpart\n"
        proc = run_gate(
            item,
            item,
            python("print(" + repr(item.strip()) + ")",
                   "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS", proc.stdout)

    def test_verdict_and_count_lines_are_still_not_items(self):
        proc = run_gate(
            "# nothing baselined\n",
            "# nothing baselined\n",
            python(
                "print('PASS')",
                "print('OK')",
                "print('FAILED (failures=2)')",
                "print('Ran 12 tests in 0.031s')",
                "print('GOV-DOC-001 full scan: 914 in-scope Markdown files; "
                "377 exempt; 77 violations.')",
                "import sys",
                "sys.exit(1)",
            ),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("current=0", proc.stdout)
        self.assertIn("without printing any item", proc.stdout)

    def test_a_name_that_starts_with_a_verdict_word_is_still_an_item(self):
        proc = run_gate(
            "# nothing baselined\n",
            "# nothing baselined\n",
            python("print('OK_STATUS')", "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("ratchet regression", proc.stdout)
        self.assertIn("OK_STATUS", proc.stdout)


class BaseAnchoringTests(unittest.TestCase):
    """Issue #1462: a candidate must not author its own exemptions."""

    def test_t_a_identical_base_and_candidate_baseline_passes(self):
        proc = run_gate(
            "existing.md\n",
            "existing.md\n",
            python("print('existing.md')", "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS", proc.stdout)

    def test_t_b_removing_a_fixed_entry_is_legal_debt_repayment(self):
        proc = run_gate(
            "existing.md\n",
            "",
            python("import sys", "sys.exit(0)"),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("removed=1", proc.stdout)
        self.assertIn("baseline debt retired: existing.md", proc.stdout)

    def test_t_c_adding_an_entry_fails_and_names_the_original_line(self):
        added = "forged-exemption.md -> accepted"
        proc = run_gate(
            "existing.md\n",
            "existing.md\n" + added + "\n",
            python("import sys", "sys.exit(0)"),
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("unauthorized baseline addition", proc.stdout)
        self.assertIn(added, proc.stdout)

    def test_t_d_added_failure_and_added_baseline_still_fails(self):
        added = "MISMATCH forged/path.yaml declared=bad actual=good"
        proc = run_gate(
            "MISMATCH existing/path.yaml declared=bad actual=good\n",
            "MISMATCH existing/path.yaml declared=bad actual=good\n"
            + added + "\n",
            python(
                "print(" + repr(added) + ")",
                "import sys",
                "sys.exit(1)",
            ),
            baseline_id="manifest-blob-pins",
        )
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("unauthorized baseline addition", proc.stdout)
        self.assertIn(added, proc.stdout)
        self.assertNotIn("ratchet: PASS", proc.stdout)
        self.assertIn("wrapped-command-exit=1", proc.stdout)
        self.assertIn("wrapped-command-item: " + added, proc.stdout)

    def test_t_e_missing_base_ref_is_incomplete_exit_two(self):
        proc = run_gate(
            "existing.md\n",
            "existing.md\n",
            python("print('existing.md')", "import sys", "sys.exit(1)"),
            base_ref_override="does-not-exist",
        )
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("base ref is not an available commit", proc.stderr)

    def test_t_e_missing_path_in_base_is_incomplete_exit_two(self):
        tmp = tempfile.TemporaryDirectory()
        repo = Path(tmp.name)
        try:
            git(repo, "init")
            git(repo, "config", "user.email", "ratchet-test@example.invalid")
            git(repo, "config", "user.name", "Ratchet Test")
            git(repo, "commit", "--allow-empty", "-m", "base without baseline")
            base = git(repo, "rev-parse", "HEAD")
            candidate = repo / BASELINES["bilingual-docs"]
            candidate.parent.mkdir(parents=True)
            candidate.write_text("forged.md\n", encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable, str(GATE),
                    "--baseline-ref", base,
                    "--baseline-id", "bilingual-docs",
                    "--baseline", BASELINES["bilingual-docs"],
                    "--command", python("print('forged.md')"),
                ],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 2, proc.stderr)
            self.assertIn("baseline path does not exist", proc.stderr)
        finally:
            tmp.cleanup()

    def test_t_f_candidate_cannot_switch_the_registered_baseline_path(self):
        proc = run_gate(
            "existing.md\n",
            "existing.md\n",
            python("print('existing.md')", "import sys", "sys.exit(1)"),
            baseline_path=BASELINES["manifest-blob-pins"],
        )
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertIn("baseline path does not match registered", proc.stderr)

    def test_candidate_baseline_symlink_is_incomplete(self):
        tmp, repo, base = make_repo("existing.md\n", "existing.md\n")
        try:
            path = repo / BASELINES["bilingual-docs"]
            path.unlink()
            outside = repo / "outside.txt"
            outside.write_text("existing.md\n", encoding="utf-8")
            path.symlink_to(outside)
            proc = subprocess.run(
                [
                    sys.executable, str(GATE),
                    "--baseline-ref", base,
                    "--baseline-id", "bilingual-docs",
                    "--baseline", BASELINES["bilingual-docs"],
                    "--command", python("print('existing.md')"),
                ],
                cwd=repo,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 2, proc.stderr)
            self.assertIn("must not be a symlink", proc.stderr)
        finally:
            tmp.cleanup()

    def test_comments_and_blank_lines_do_not_create_entries(self):
        proc = run_gate(
            "# header\n\nexisting.md\n",
            "# candidate header\n\nexisting.md\n\n",
            python("print('existing.md')", "import sys", "sys.exit(1)"),
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)


class CommentedCountTests(unittest.TestCase):
    def test_stated_count_matches_baseline_entries(self):
        workflow = GATES_WORKFLOW.read_text(encoding="utf-8")
        baseline = BILINGUAL_BASELINE.read_text(encoding="utf-8")
        stated = STATED_COUNT.findall(workflow)
        self.assertEqual(len(stated), 1)
        self.assertEqual(
            int(stated[0]),
            len(baseline_entries(baseline)),
            "workflow count differs from bilingual baseline entry count",
        )


def main() -> None:
    for path in (
        GATES_WORKFLOW,
        BILINGUAL_BASELINE,
        MANIFEST_BASELINE,
        GATE,
    ):
        try:
            path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"INCOMPLETE: {exc}", file=sys.stderr)
            sys.exit(2)
    unittest.main()


if __name__ == "__main__":
    main()
