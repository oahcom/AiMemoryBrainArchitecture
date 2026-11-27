#!/usr/bin/env python3
"""Deterministic Git-history tests for the work-item uniqueness gate.

Every case builds a real temporary repository: the gate reads trees, so object
mocks would prove nothing about it. The interpreter is ``sys.executable`` so
the suite runs on Windows as well as in CI.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_work_item_uniqueness.py")
ITEM = "14-ai-development/work-items/AID-2026-279"
OTHER = "14-ai-development/work-items/AID-2026-280"
REGISTRY = "14-ai-development/work-items/registry/work-item-claims.yaml"
EMPTY_REGISTRY = "schema_version: 1\nclaims: []\n"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()


def write(repo: Path, path: str, content: str) -> None:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def commit_file(repo: Path, path: str, content: str, message: str) -> str:
    write(repo, path, content)
    return commit(repo, message)


def init_repo(root: Path, *, with_registry: bool = True) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "gate-test@example.invalid")
    git(repo, "config", "user.name", "Gate Test")
    git(repo, "config", "commit.gpgsign", "false")
    write(repo, "README.md", "base\n")
    if with_registry:
        write(repo, REGISTRY, EMPTY_REGISTRY)
    return repo, commit(repo, "base")


def claim_yaml(work_item_id: str, status: str, pull_request: int, head_sha: str) -> str:
    merge = "null" if status != "MERGED" else f"\"{'a' * 40}\""
    return (
        "schema_version: 1\n"
        "claims:\n"
        f"  - work_item_id: {work_item_id}\n"
        f"    status: {status}\n"
        f"    pull_request: {pull_request}\n"
        "    repository: example/repo\n"
        f"    head_sha: \"{head_sha}\"\n"
        f"    merge_commit_sha: {merge}\n"
        "    claimed_at: \"2026-11-27T00:00:00Z\"\n"
        "    updated_at: \"2026-11-27T00:00:00Z\"\n"
        f"    owner_work_item: {work_item_id}\n"
        "    evidence:\n"
        f"      - \"{work_item_id}/manifest.yaml\"\n"
    )


def invoke(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT), *args]
    print("$ " + " ".join(command), flush=True)
    result = subprocess.run(
        command, cwd=repo, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result


class WorkItemUniquenessTests(unittest.TestCase):
    def test_new_unoccupied_directory_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "new\n", "new item")
            result = invoke(repo, "--base", base, "--head", head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("new_ids=1", result.stdout)

    def test_additive_file_under_existing_directory_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            base = commit_file(repo, f"{ITEM}/manifest.yaml", "existing\n", "existing")
            head = commit_file(repo, f"{ITEM}/evidence.md", "additive\n", "add evidence")
            result = invoke(repo, "--base", base, "--head", head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("new_ids=0", result.stdout)
            self.assertIn("modified_under_shared=0", result.stdout)

    # Regression 1: the candidate merges the target branch, so the directory is
    # present on both sides and the old merge-base algorithm reported
    # introduced=0. The candidate still holds its own copy of the record.
    def test_merged_target_with_same_directory_still_violates(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, fork = init_repo(Path(temp))
            git(repo, "checkout", "-q", "-b", "candidate")
            branch = commit_file(repo, f"{ITEM}/manifest.yaml", "candidate\n", "candidate claim")
            git(repo, "checkout", "-q", "-b", "target", fork)
            target = commit_file(repo, f"{ITEM}/manifest.yaml", "target\n", "target claim")
            git(repo, "checkout", "-q", "candidate")
            subprocess.run(
                ["git", "merge", "--no-edit", "-X", "ours", target],
                cwd=repo, check=True, capture_output=True, text=True,
            )
            merged = git(repo, "rev-parse", "HEAD")
            self.assertNotEqual(merged, branch)
            result = invoke(repo, "--base", target, "--head", merged)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("VIOLATION", result.stdout)
            self.assertIn("already owns this work item", result.stdout)

    # Regression 2: the conflict is resolved on the target side for the
    # manifest, yet the candidate's own evidence file still overwrites the
    # target's record. Merging the target branch again does not launder it.
    def test_conflict_resolved_target_side_then_remerged_violates(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, fork = init_repo(Path(temp))
            git(repo, "checkout", "-q", "-b", "candidate")
            write(repo, f"{ITEM}/manifest.yaml", "candidate\n")
            write(repo, f"{ITEM}/evidence.md", "candidate evidence\n")
            commit(repo, "candidate claim")
            git(repo, "checkout", "-q", "-b", "target", fork)
            write(repo, f"{ITEM}/manifest.yaml", "target\n")
            write(repo, f"{ITEM}/evidence.md", "target evidence\n")
            target = commit(repo, "target claim")
            git(repo, "checkout", "-q", "candidate")
            subprocess.run(
                ["git", "merge", "--no-edit", target],
                cwd=repo, check=False, capture_output=True, text=True,
            )
            # Resolve manifest.yaml on the target side, keep the candidate's
            # evidence file, then merge the target branch again.
            write(repo, f"{ITEM}/manifest.yaml", "target\n")
            write(repo, f"{ITEM}/evidence.md", "candidate evidence\n")
            commit(repo, "resolve manifest on target side")
            subprocess.run(
                ["git", "merge", "--no-edit", target],
                cwd=repo, check=False, capture_output=True, text=True,
            )
            merged = git(repo, "rev-parse", "HEAD")
            result = invoke(repo, "--base", target, "--head", merged)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(f"{ITEM} has modified or deleted paths", result.stdout)

    # Regression 3: the pull request base is behind the latest target branch,
    # which already carries the same id.
    def test_stale_base_where_latest_target_has_the_id_violates(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, fork = init_repo(Path(temp))
            git(repo, "checkout", "-q", "-b", "candidate")
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "candidate\n", "candidate claim")
            git(repo, "checkout", "-q", "-b", "target", fork)
            latest = commit_file(repo, f"{ITEM}/manifest.yaml", "target\n", "target claim")
            result = invoke(repo, "--base", latest, "--head", head)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("VIOLATION", result.stdout)

    def test_registry_claim_by_another_pull_request_rejects_new_id(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, fork = init_repo(Path(temp))
            git(repo, "checkout", "-q", "-b", "candidate")
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "candidate\n", "candidate claim")
            git(repo, "checkout", "-q", "-b", "target", fork)
            base = commit_file(
                repo, REGISTRY,
                claim_yaml("AID-2026-279", "CLAIMED", 1, "b" * 40),
                "other pull request claims the id",
            )
            result = invoke(repo, "--base", base, "--head", head, "--pull-request", "2")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("is already CLAIMED in the registry", result.stdout)

    def test_registry_claim_by_the_same_pull_request_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, fork = init_repo(Path(temp))
            git(repo, "checkout", "-q", "-b", "candidate")
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "candidate\n", "candidate claim")
            git(repo, "checkout", "-q", "-b", "target", fork)
            base = commit_file(
                repo, REGISTRY,
                claim_yaml("AID-2026-279", "CLAIMED", 2, "b" * 40),
                "the same pull request claims the id",
            )
            result = invoke(
                repo, "--base", base, "--head", head,
                "--pull-request", "2", "--repository", "example/repo",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_race_replay_rejects_the_second_candidate_on_a_fresh_base(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, fork = init_repo(Path(temp))
            git(repo, "checkout", "-q", "-b", "candidate-a")
            head_a = commit_file(repo, f"{ITEM}/a.txt", "A\n", "candidate A")
            git(repo, "checkout", "-q", "-b", "candidate-b", fork)
            head_b = commit_file(repo, f"{ITEM}/b.txt", "B\n", "candidate B")
            first = invoke(repo, "--base", fork, "--head", head_a)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            # Merge candidate A; the second candidate must be re-checked
            # against the new target tip, not its stale base.
            git(repo, "checkout", "-q", "-b", "target", head_a)
            latest = git(repo, "rev-parse", "HEAD")
            second = invoke(repo, "--base", latest, "--head", head_b)
            self.assertEqual(second.returncode, 1, second.stdout + second.stderr)
            self.assertIn("VIOLATION", second.stdout)

    def test_registry_bootstrap_from_head_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp), with_registry=False)
            write(repo, REGISTRY, EMPTY_REGISTRY)
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "new\n", "introduce registry")
            result = invoke(repo, "--base", base, "--head", head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("bootstrap", result.stdout)

    def test_absent_registry_is_treated_as_empty(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp), with_registry=False)
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "new\n", "new item")
            result = invoke(repo, "--base", base, "--head", head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("registry=absent", result.stdout)

    def test_missing_base_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            head = git(repo, "rev-parse", "HEAD")
            result = invoke(repo, "--head", head)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("INCOMPLETE", result.stdout)

    def test_unknown_ref_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            result = invoke(repo, "--base", base, "--head", "deadbeef" * 5)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("INCOMPLETE", result.stdout)

    def test_malformed_registry_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            base = commit_file(repo, REGISTRY, "schema_version: 1\nclaims: {}\n", "bad registry")
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "new\n", "new item")
            result = invoke(repo, "--base", base, "--head", head)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("INCOMPLETE", result.stdout)

    def test_unrelated_work_item_directories_are_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_file(repo, f"{OTHER}/manifest.yaml", "other\n", "other item")
            result = invoke(repo, "--base", base, "--head", head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("new_ids=1", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
