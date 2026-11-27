#!/usr/bin/env python3
"""Deterministic Git-history tests for the work-item uniqueness gate."""
from __future__ import annotations
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_work_item_uniqueness.py")
ITEM = "14-ai-development/work-items/AID-2026-279"

def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True,
                          capture_output=True, text=True).stdout.strip()

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
    return repo, commit_file(repo, "README.md", "base\n", "base")

def invoke(repo: Path, base: str | None, head: str) -> subprocess.CompletedProcess[str]:
    args = ["python3", str(SCRIPT), "--head", head]
    if base is not None:
        args += ["--base", base]
    print("$ " + " ".join(args), flush=True)
    result = subprocess.run(args, cwd=repo, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result

class WorkItemUniquenessTests(unittest.TestCase):
    def test_new_unoccupied_directory_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "new\n", "new item")
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("introduced=1 occupied=0", result.stdout)

    def test_occupied_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, ancestor = init_repo(Path(temp))
            git(repo, "checkout", "-b", "topic")
            topic = commit_file(repo, f"{ITEM}/topic.txt", "topic\n", "topic claim")
            git(repo, "checkout", "-b", "main-simulated", ancestor)
            latest = commit_file(repo, f"{ITEM}/main.txt", "main\n", "main claim")
            result = invoke(repo, latest, topic)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("VIOLATION", result.stdout)

    def test_additive_file_under_existing_directory_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            base = commit_file(repo, f"{ITEM}/manifest.yaml", "existing\n", "existing")
            head = commit_file(repo, f"{ITEM}/evidence.md", "additive\n", "add evidence")
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("introduced=0 occupied=0", result.stdout)

    def test_race_replay_rejects_second_candidate_on_fresh_base(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, old_base = init_repo(Path(temp))
            git(repo, "branch", "candidate-a", old_base)
            git(repo, "branch", "candidate-b", old_base)
            git(repo, "checkout", "candidate-a")
            head_a = commit_file(repo, f"{ITEM}/a.txt", "A\n", "candidate A")
            git(repo, "checkout", "candidate-b")
            head_b = commit_file(repo, f"{ITEM}/b.txt", "B\n", "candidate B")
            first = invoke(repo, old_base, head_a)
            stale_second = invoke(repo, old_base, head_b)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(stale_second.returncode, 0, stale_second.stdout + stale_second.stderr)
            git(repo, "checkout", "-b", "main-after-a", head_a)
            latest = git(repo, "rev-parse", "HEAD")
            fresh_second = invoke(repo, latest, head_b)
            self.assertEqual(fresh_second.returncode, 1, fresh_second.stdout + fresh_second.stderr)
            self.assertIn("VIOLATION", fresh_second.stdout)

    def test_missing_base_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            head = git(repo, "rev-parse", "HEAD")
            result = invoke(repo, None, head)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("INCOMPLETE", result.stdout)

if __name__ == "__main__":
    unittest.main(verbosity=2)
