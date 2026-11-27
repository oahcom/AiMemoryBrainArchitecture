#!/usr/bin/env python3
"""Regression tests for check_fmt.py's commit/worktree identity boundary."""

from __future__ import annotations

import json
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
        encoding="utf-8",
        errors="replace",
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
        env.pop("GITHUB_EVENT_NAME", None)
        env.pop("GITHUB_EVENT_PATH", None)
        return root, head, env, log

    def run_checker(
        self,
        root: Path,
        expected: str | None,
        env: dict[str, str],
    ) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(root / "scripts" / "check_fmt.py")]
        if expected is not None:
            command.extend(["--expect", expected])

        return subprocess.run(
            command,
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )

    def test_clean_tree_runs_fmt_and_reports_single_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, head, env, log = self.make_repo(Path(tmp) / "repo")
            result = self.run_checker(root, head, env)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("WORKTREE_RESULT=CLEAN", result.stdout)
            self.assertIn(f"CHECKED_COMMIT_SHA={head}", result.stdout)
            self.assertNotIn("CHECKED_MERGE_SHA=", result.stdout)
            self.assertNotIn("CHECKED_PR_HEAD_SHA=", result.stdout)
            self.assertNotIn("CHECKED_BASE_SHA=", result.stdout)
            self.assertNotIn("CHECKED_HEAD_SHA=", result.stdout)
            self.assertIn("CHECK_RESULT=PASS", result.stdout)
            self.assertTrue(log.is_file(), "cargo must run on a clean tree")

    def test_pull_request_head_sha_is_not_accepted_as_merge_head(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, merge_sha, env, log = self.make_repo(Path(tmp) / "repo")
            pr_head_sha = "1" * 40
            base_sha = "2" * 40
            event_path = root.parent / "event.json"
            event_path.write_text(
                json.dumps(
                    {
                        "pull_request": {
                            "head": {"sha": pr_head_sha},
                            "base": {"sha": base_sha},
                        }
                    }
                ),
                encoding="utf-8",
            )
            env["GITHUB_EVENT_NAME"] = "pull_request"
            env["GITHUB_EVENT_PATH"] = str(event_path)

            self.assertNotEqual(pr_head_sha, merge_sha)
            result = self.run_checker(root, pr_head_sha, env)

            self.assertEqual(result.returncode, 5, result.stdout + result.stderr)
            self.assertIn(
                f"expected {pr_head_sha.lower()}, actual {merge_sha.lower()}",
                result.stderr,
            )
            self.assertNotIn("CHECKED_MERGE_SHA=", result.stdout)
            self.assertNotIn("CHECKED_PR_HEAD_SHA=", result.stdout)
            self.assertNotIn("CHECKED_BASE_SHA=", result.stdout)
            self.assertFalse(log.exists(), "cargo must not run after an SHA mismatch")

    def test_pull_request_reports_merge_head_and_event_shas(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, merge_sha, env, log = self.make_repo(Path(tmp) / "repo")
            pr_head_sha = "1" * 40
            base_sha = "2" * 40
            event_path = root.parent / "event.json"
            event_path.write_text(
                json.dumps(
                    {
                        "pull_request": {
                            "head": {"sha": pr_head_sha},
                            "base": {"sha": base_sha},
                        }
                    }
                ),
                encoding="utf-8",
            )
            env["GITHUB_EVENT_NAME"] = "pull_request"
            env["GITHUB_EVENT_PATH"] = str(event_path)

            result = self.run_checker(root, merge_sha, env)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(f"CHECKED_MERGE_SHA={merge_sha}", result.stdout)
            self.assertIn(f"CHECKED_PR_HEAD_SHA={pr_head_sha}", result.stdout)
            self.assertIn(f"CHECKED_BASE_SHA={base_sha}", result.stdout)
            self.assertNotIn("CHECKED_COMMIT_SHA=", result.stdout)
            self.assertNotIn("CHECKED_HEAD_SHA=", result.stdout)
            self.assertTrue(log.is_file(), "cargo must run after valid PR identity")

    def test_format_failure_on_clean_tree_remains_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, head, env, log = self.make_repo(Path(tmp) / "repo")
            cargo = Path(env["PATH"].split(os.pathsep, 1)[0]) / "cargo"
            cargo.write_text(
                "#!/bin/sh\nprintf 'invoked\\n' >> \"$CARGO_LOG\"\nexit 1\n",
                encoding="utf-8",
            )
            cargo.chmod(0o755)
            result = self.run_checker(root, head, env)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("WORKTREE_RESULT=CLEAN", result.stdout)
            self.assertIn("FMT_RESULT=FAIL", result.stdout)
            self.assertIn("CHECK_RESULT=FAIL", result.stdout)
            self.assertNotIn("WORKTREE_RESULT=DIRTY", result.stdout)
            self.assertTrue(log.is_file(), "cargo must run on a clean tree even when fmt fails")

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
            self.assertNotIn("CHECKED_COMMIT_SHA=", result.stdout)
            self.assertNotIn("CHECKED_MERGE_SHA=", result.stdout)
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
