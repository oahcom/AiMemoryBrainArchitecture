#!/usr/bin/env python3
"""Regression tests for check_fmt.py's commit/worktree identity boundary."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "scripts" / "check_fmt.py"


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


class CheckFmtWorktreeTests(unittest.TestCase):
    def make_repo(self, root: Path) -> tuple[Path, str, dict[str, str], Path]:
        scripts = root / "scripts"
        scripts.mkdir(parents=True)
        shutil.copy2(CHECKER, scripts / "check_fmt.py")
        source = root / "src" / "lib.rs"
        source.parent.mkdir(parents=True)
        source.write_text("pub fn stable() {}\n", encoding="utf-8")

        git(root, "init", "-q")
        git(root, "config", "user.email", "check-fmt@example.invalid")
        git(root, "config", "user.name", "check-fmt-test")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "seed")
        head = git(root, "rev-parse", "HEAD")

        bin_dir = root.parent / "bin"
        bin_dir.mkdir()
        cargo = bin_dir / "cargo"
        cargo.write_text(
            "#!/bin/sh\nprintf 'invoked\\n' >> \"$CARGO_LOG\"\nexit 0\n",
            encoding="utf-8",
        )
        cargo.chmod(0o755)
        log = root.parent / "cargo.log"
        env = os.environ.copy()
        env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
        env["CARGO_LOG"] = str(log)
        return root, head, env, log

    def run_checker(
        self, root: Path, head: str, env: dict[str, str]
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(root / "scripts" / "check_fmt.py"), "--expect", head],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

    def test_clean_tree_runs_fmt_and_reports_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, head, env, log = self.make_repo(Path(tmp) / "repo")
            result = self.run_checker(root, head, env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("WORKTREE_RESULT=CLEAN", result.stdout)
            self.assertIn(f"CHECKED_HEAD_SHA={head}", result.stdout)
            self.assertIn("CHECK_RESULT=PASS", result.stdout)
            self.assertTrue(log.is_file(), "cargo must run on a clean tree")

    def assert_dirty_refused(self, mutation: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, head, env, log = self.make_repo(Path(tmp) / "repo")
            if mutation == "modified":
                (root / "src" / "lib.rs").write_text("pub fn changed() {}\n", encoding="utf-8")
            elif mutation == "staged":
                (root / "src" / "lib.rs").write_text("pub fn staged() {}\n", encoding="utf-8")
                git(root, "add", "src/lib.rs")
            elif mutation == "untracked":
                untracked = root / "src" / "nested" / "new.rs"
                untracked.parent.mkdir(parents=True)
                untracked.write_text("pub fn untracked() {}\n", encoding="utf-8")
            else:
                self.fail(f"unknown mutation: {mutation}")

            result = self.run_checker(root, head, env)
            self.assertEqual(result.returncode, 7, result.stdout + result.stderr)
            self.assertIn("WORKTREE_RESULT=DIRTY", result.stdout)
            self.assertNotIn("CHECKED_HEAD_SHA=", result.stdout)
            self.assertNotIn("CHECK_RESULT=PASS", result.stdout)
            self.assertFalse(log.exists(), "cargo must not run on a dirty tree")

    def test_modified_tracked_file_is_refused(self) -> None:
        self.assert_dirty_refused("modified")

    def test_staged_file_is_refused(self) -> None:
        self.assert_dirty_refused("staged")

    def test_nested_untracked_file_is_refused(self) -> None:
        self.assert_dirty_refused("untracked")


if __name__ == "__main__":
    unittest.main()
