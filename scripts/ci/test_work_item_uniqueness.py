#!/usr/bin/env python3
"""Tree-only invariance tests for work-item uniqueness."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_work_item_uniqueness.py")
ROOT = "14-ai-development/work-items"
ITEM_ID = "AID-2026-311"
ITEM = f"{ROOT}/{ITEM_ID}"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def commit_file(repo: Path, path: str, content: str, message: str) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    git(repo, "add", path)
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def init_repo(root: Path) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "gate-test@example.invalid")
    git(repo, "config", "user.name", "Gate Test")
    base = commit_file(repo, f"{ITEM}/manifest.yaml", "id: existing\n", "baseline")
    commit_file(repo, f"{ITEM}/existing-evidence.md", "old\n", "existing evidence")
    return repo, git(repo, "rev-parse", "HEAD")


def invoke(repo: Path, base: str, head: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [os.environ.get("PYTHON", "python3"), str(SCRIPT),
         "--base", base, "--head", head],
        cwd=repo, capture_output=True, text=True,
    )


def assert_verdict(test: unittest.TestCase, result, code: int, marker: str):
    test.assertEqual(result.returncode, code, result.stdout + result.stderr)
    test.assertIn(marker, result.stdout)


def build_pair(root: Path, construction: str) -> tuple[Path, str, str]:
    repo, old_base = init_repo(root)
    if construction == "update_branch":
        git(repo, "checkout", "-b", "pr-b", old_base)
        commit_file(repo, f"{ITEM}/evidence.md", "new\n", "PR B claim")
        git(repo, "checkout", "-b", "advanced-main", old_base)
        base = commit_file(repo, "base-advance.txt", "advance\n", "advance base")
        git(repo, "checkout", "pr-b")
        git(repo, "merge", "--no-ff", "-m", "Update branch", "advanced-main")
        head = git(repo, "rev-parse", "HEAD")
        if git(repo, "merge-base", base, head) != base:
            raise AssertionError("Update-branch merge-base did not advance to base")
    else:
        base = commit_file(repo, "base-advance.txt", "advance\n", "advance base")
        if construction == "ordinary_pr":
            git(repo, "checkout", "-b", "ordinary-pr", base)
            head = commit_file(repo, f"{ITEM}/evidence.md", "new\n", "ordinary PR")
        elif construction == "squash":
            git(repo, "checkout", "-b", "squash-topic", base)
            commit_file(repo, f"{ITEM}/evidence.md", "intermediate\n", "PR commit 1")
            commit_file(repo, f"{ITEM}/evidence.md", "new\n", "PR commit 2")
            git(repo, "checkout", "--detach", base)
            git(repo, "merge", "--squash", "squash-topic")
            git(repo, "commit", "-m", "squash PR")
            head = git(repo, "rev-parse", "HEAD")
        elif construction == "merge_group":
            git(repo, "checkout", "-b", "second-pr", base)
            git(repo, "commit", "--allow-empty", "-m", "second queued PR")
            second_parent = git(repo, "rev-parse", "HEAD")
            git(repo, "checkout", "-b", "merge-group-first-pr", base)
            first_parent = commit_file(repo, f"{ITEM}/evidence.md", "new\n", "first queued PR")
            candidate_tree = git(repo, "rev-parse", f"{first_parent}^{{tree}}")
            head = git(repo, "commit-tree", candidate_tree, "-p", base, "-p", second_parent, "-m", "merge group candidate")
            if len(git(repo, "rev-list", "--parents", "-n", "1", head).split()) != 3:
                raise AssertionError("synthetic merge-group commit must have two parents")
        else:
            raise AssertionError(f"unknown construction: {construction}")
    return repo, base, head


class WorkItemUniquenessTreeTests(unittest.TestCase):
    def test_ordinary_pr_ahead_tree_is_violation(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base, head = build_pair(Path(temp), "ordinary_pr")
            assert_verdict(self, invoke(repo, base, head), 1, "WORK-ITEM UNIQUENESS: VIOLATION")

    def test_update_branch_rewritten_merge_base_tree_is_violation(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base, head = build_pair(Path(temp), "update_branch")
            assert_verdict(self, invoke(repo, base, head), 1, "WORK-ITEM UNIQUENESS: VIOLATION")

    def test_squash_merge_equivalent_tree_is_violation(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base, head = build_pair(Path(temp), "squash")
            assert_verdict(self, invoke(repo, base, head), 1, "WORK-ITEM UNIQUENESS: VIOLATION")

    def test_merge_group_two_parent_tree_is_violation(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base, head = build_pair(Path(temp), "merge_group")
            assert_verdict(self, invoke(repo, base, head), 1, "WORK-ITEM UNIQUENESS: VIOLATION")

    def test_all_four_constructions_have_identical_tree_pair_and_verdict(self):
        observed = []
        for construction in ("ordinary_pr", "update_branch", "squash", "merge_group"):
            with tempfile.TemporaryDirectory() as temp:
                repo, base, head = build_pair(Path(temp), construction)
                base_tree = git(repo, "rev-parse", f"{base}^{{tree}}")
                head_tree = git(repo, "rev-parse", f"{head}^{{tree}}")
                result = invoke(repo, base, head)
                summary = next(
                    line for line in result.stdout.splitlines()
                    if line.startswith("WORK-ITEM UNIQUENESS:")
                )
                verdict = summary.split()[2]
                observed.append((base_tree, head_tree, result.returncode, verdict))
                assert_verdict(self, result, 1, "WORK-ITEM UNIQUENESS: VIOLATION")
        self.assertEqual(len(set(observed)), 1, observed)

    def test_new_declaration_is_allowed(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_file(repo, f"{ROOT}/AID-2026-312/manifest.yaml", "id: new\n", "new declaration")
            assert_verdict(self, invoke(repo, base, head), 0, "WORK-ITEM UNIQUENESS: PASS")

    def test_deleting_existing_work_item_is_reported_separately(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            git(repo, "rm", "-r", ITEM)
            git(repo, "commit", "-m", "delete work item")
            head = git(repo, "rev-parse", "HEAD")
            result = invoke(repo, base, head)
            assert_verdict(self, result, 1, "DELETION:")
            self.assertIn("WORK-ITEM UNIQUENESS: DELETION", result.stdout)

    def test_deletion_only_within_existing_work_item_is_allowed(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            git(repo, "rm", f"{ITEM}/existing-evidence.md")
            git(repo, "commit", "-m", "remove old evidence")
            head = git(repo, "rev-parse", "HEAD")
            assert_verdict(self, invoke(repo, base, head), 0, "WORK-ITEM UNIQUENESS: PASS")

    def test_checker_executes_only_rev_parse_and_ls_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo, base = init_repo(root)
            head = commit_file(repo, f"{ITEM}/evidence.md", "new\n", "add evidence")
            log = root / "git-commands.log"
            wrapper_dir = root / "bin"
            wrapper_dir.mkdir()
            real_git = subprocess.check_output(["which", "git"], text=True).strip()
            wrapper = wrapper_dir / "git"
            wrapper.write_text(
                "#!/bin/sh\nprintf '%s\\n' \"$*\" >> \"$GIT_COMMAND_LOG\"\n"
                f"exec {real_git} \"$@\"\n",
                encoding="utf-8",
            )
            wrapper.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{wrapper_dir}{os.pathsep}{env['PATH']}"
            env["GIT_COMMAND_LOG"] = str(log)
            result = subprocess.run(
                ["python3", str(SCRIPT), "--base", base, "--head", head],
                cwd=repo, env=env, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            commands = log.read_text(encoding="utf-8").splitlines()
            self.assertTrue(commands)
            self.assertTrue(
                all(command.startswith("rev-parse ") or command.startswith("ls-tree ") for command in commands),
                commands,
            )

    def test_missing_base_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            head = git(repo, "rev-parse", "HEAD")
            assert_verdict(self, invoke(repo, "", head), 2, "WORK-ITEM UNIQUENESS: INCOMPLETE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
