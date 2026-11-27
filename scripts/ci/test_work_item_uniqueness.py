#!/usr/bin/env python3
"""Deterministic real-Git tests for the work-item uniqueness gate."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_work_item_uniqueness.py")
ROOT = "14-ai-development/work-items"
ITEM = f"{ROOT}/AID-2026-279"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def commit_files(repo: Path, files: dict[str, str], message: str) -> str:
    for relative, content in files.items():
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        git(repo, "add", relative)
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def commit_file(repo: Path, path: str, content: str, message: str) -> str:
    return commit_files(repo, {path: content}, message)


def init_repo(root: Path) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "gate-test@example.invalid")
    git(repo, "config", "user.name", "Gate Test")
    base = commit_file(repo, "README.md", "base\n", "base")
    return repo, base


def manifest(work_item_id: str | None = None, aid: str | None = None) -> str:
    lines = []
    if work_item_id is not None:
        lines.append(f"work_item_id: {work_item_id}\n")
    if aid is not None:
        lines.append(f"aid: {aid}\n")
    return "".join(lines) or "title: test item\n"


def invoke(
    repo: Path, base: str | None, head: str
) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, str(SCRIPT), "--head", head]
    if base is not None:
        args += ["--base", base]
    print("$ " + subprocess.list2cmdline(args), flush=True)
    result = subprocess.run(
        args,
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result


class WorkItemUniquenessTests(unittest.TestCase):
    def test_positive_new_unoccupied_id(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_file(
                repo,
                f"{ITEM}/manifest.yaml",
                manifest("AID-2026-279"),
                "new item",
            )
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("violations=0", result.stdout)

    def test_negative_directory_occupied_on_latest_base(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, ancestor = init_repo(Path(temp))
            git(repo, "checkout", "-b", "candidate")
            head = commit_file(
                repo, f"{ITEM}/candidate.txt", "candidate\n", "claim"
            )
            git(repo, "checkout", "-b", "target", ancestor)
            latest = commit_file(
                repo, f"{ITEM}/target.txt", "target\n", "occupy"
            )
            result = invoke(repo, latest, head)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("VIOLATION", result.stdout)
            self.assertIn("AID-2026-279", result.stdout)

    def test_additive_existing_directory_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            base = commit_file(
                repo,
                f"{ITEM}/manifest.yaml",
                manifest("AID-2026-279"),
                "existing item",
            )
            head = commit_file(
                repo, f"{ITEM}/evidence.md", "additive evidence\n", "add evidence"
            )
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("introduced_directories=0", result.stdout)

    def test_race_two_independent_claimants(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, old_base = init_repo(Path(temp))
            git(repo, "branch", "candidate-a", old_base)
            git(repo, "branch", "candidate-b", old_base)

            git(repo, "checkout", "candidate-a")
            head_a = commit_file(
                repo, f"{ITEM}/a.txt", "A\n", "candidate A"
            )
            git(repo, "checkout", "candidate-b")
            head_b = commit_file(
                repo, f"{ITEM}/b.txt", "B\n", "candidate B"
            )

            first = invoke(repo, old_base, head_a)
            stale_second = invoke(repo, old_base, head_b)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(
                stale_second.returncode, 0,
                stale_second.stdout + stale_second.stderr,
            )

            git(repo, "checkout", "-b", "target-after-a", head_a)
            advanced_target = git(repo, "rev-parse", "HEAD")
            fresh_second = invoke(repo, advanced_target, head_b)
            self.assertEqual(
                fresh_second.returncode, 1,
                fresh_second.stdout + fresh_second.stderr,
            )

    def test_exact_head_stale_vs_advanced_target(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, old_base = init_repo(Path(temp))
            git(repo, "branch", "first", old_base)
            git(repo, "branch", "second", old_base)

            git(repo, "checkout", "first")
            first_head = commit_file(
                repo, f"{ITEM}/first.txt", "first\n", "first claimant"
            )
            git(repo, "checkout", "second")
            second_head = commit_file(
                repo, f"{ITEM}/second.txt", "second\n", "second claimant"
            )

            stale_result = invoke(repo, old_base, second_head)
            self.assertEqual(
                stale_result.returncode, 0,
                stale_result.stdout + stale_result.stderr,
            )

            git(repo, "checkout", "-b", "advanced-target", first_head)
            latest_target = git(repo, "rev-parse", "HEAD")
            advanced_result = invoke(repo, latest_target, second_head)
            self.assertEqual(
                advanced_result.returncode, 1,
                advanced_result.stdout + advanced_result.stderr,
            )

    def test_free_directory_manifest_identity_collision(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            base = commit_file(
                repo,
                f"{ROOT}/AID-2026-250/manifest.yaml",
                manifest("AID-2026-250"),
                "existing item",
            )
            head = commit_file(
                repo,
                f"{ROOT}/AID-2026-279/manifest.yaml",
                manifest("AID-2026-250"),
                "manifest collision",
            )
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("AID-2026-250", result.stdout)

    def test_legacy_aid_identity_collision(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            base = commit_file(
                repo,
                f"{ROOT}/AID-2026-250/manifest.yaml",
                manifest("AID-2026-250"),
                "existing item",
            )
            head = commit_file(
                repo,
                f"{ROOT}/AID-2026-279/manifest.yaml",
                manifest("AID-2026-279", "AID-2026-250"),
                "legacy aid collision",
            )
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("AID-2026-250", result.stdout)

    def test_index_registration_without_directory_occupies_id(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            base = commit_file(
                repo,
                f"{ROOT}/INDEX.md",
                "| [AID-2026-250](AID-2026-250/manifest.yaml) | registered |\n",
                "register identity",
            )
            head = commit_file(
                repo,
                f"{ROOT}/AID-2026-279/manifest.yaml",
                manifest("AID-2026-250"),
                "claim indexed identity",
            )
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("AID-2026-250", result.stdout)

    def test_quoted_and_unquoted_manifest_variants(self):
        for scalar in ('"AID-2026-250"', "'AID-2026-250'", "AID-2026-250"):
            with self.subTest(scalar=scalar):
                with tempfile.TemporaryDirectory() as temp:
                    repo, _ = init_repo(Path(temp))
                    base = commit_file(
                        repo,
                        f"{ROOT}/AID-2026-251/manifest.yaml",
                        f"work_item_id: {scalar}\n",
                        "existing manifest identity",
                    )
                    head = commit_file(
                        repo,
                        f"{ROOT}/AID-2026-279/manifest.yaml",
                        manifest("AID-2026-250"),
                        "candidate item",
                    )
                    result = invoke(repo, base, head)
                    self.assertEqual(
                        result.returncode, 1,
                        result.stdout + result.stderr,
                    )
                    self.assertIn("AID-2026-250", result.stdout)

    def test_candidate_multiple_directories_same_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_files(
                repo,
                {
                    f"{ROOT}/AID-2026-279/manifest.yaml":
                        manifest("AID-2026-279"),
                    f"{ROOT}/AID-2026-280/manifest.yaml":
                        manifest("AID-2026-279"),
                },
                "two candidate claims",
            )
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("multiple directory claims", result.stdout)

    def test_no_work_item_directory_addition(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_file(
                repo, "docs/note.md", "unrelated\n", "unrelated"
            )
            result = invoke(repo, base, head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("introduced_directories=0", result.stdout)

    def test_unknown_sha_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            head = git(repo, "rev-parse", "HEAD")
            result = invoke(repo, "0" * 40, head)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("INCOMPLETE", result.stdout)

    def test_missing_arguments_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            result = subprocess.run(
                [sys.executable, str(SCRIPT)],
                cwd=repo,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("INCOMPLETE", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
