#!/usr/bin/env python3
"""Tests for the serialized merge broker (AID-2026-262, issue #1341).

Two halves, because the broker has two halves.

The shape tests read `.github/workflows/work-item-merge-broker.yml` as text --
no YAML dependency, and the same "small structural reader" doctrine the other
gate audits use. They assert the properties that make the broker a *broker*:
it is serialised, it re-enumerates instead of trusting the triggering event,
it judges against the merge candidate it computed, and it pins the head SHA in
the merge call.

The composition tests drive the merged gate
(`scripts/ci/check_work_item_uniqueness.py`, AID-2026-279) through the same
two references the broker passes it, on real throwaway repositories. The broker
adds no second checker: a second copy of the same rule is the defect this issue
reports, not a fix for it.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "work-item-merge-broker.yml"
GATE = REPO / "scripts" / "ci" / "check_work_item_uniqueness.py"
ITEM = "14-ai-development/work-items/AID-2026-262"
ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "broker-test",
    "GIT_AUTHOR_EMAIL": "broker-test@example.invalid",
    "GIT_COMMITTER_NAME": "broker-test",
    "GIT_COMMITTER_EMAIL": "broker-test@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True,
                          capture_output=True, text=True, env=ENV).stdout.strip()


def commit(repo: Path, path: str, content: str, message: str) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    git(repo, "add", path)
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def init_repo(root: Path) -> tuple[Path, str]:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    return repo, commit(repo, "README.md", "base\n", "base")


def gate(repo: Path, base: str, head: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(GATE), "--base", base, "--head", head],
                          cwd=repo, capture_output=True, text=True, env=ENV)


def merge_candidate(repo: Path, base: str, head: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "merge-tree", "--write-tree", "--no-messages",
                           base, head], cwd=repo, capture_output=True, text=True, env=ENV)


class WorkflowShapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_triggers_are_the_label_and_manual_dispatch(self) -> None:
        lines = self.text.splitlines()
        start = lines.index("on:")
        block = []
        for line in lines[start + 1:]:
            if line and not line.startswith((" ", "#")):
                break
            if not line.lstrip().startswith("#"):
                block.append(line)
        body = "\n".join(block)
        self.assertIn("pull_request:\n    types: [labeled]", body)
        self.assertIn("workflow_dispatch:", body)
        self.assertNotIn("pull_request_target:", body)

    def test_runs_are_serialised_and_never_cancelled(self) -> None:
        self.assertIn("concurrency:\n  group: main-work-item-merge-broker\n"
                      "  cancel-in-progress: false", self.text)

    def test_permissions_are_minimal_and_write_scoped(self) -> None:
        self.assertIn("permissions:\n  contents: write\n  pull-requests: write",
                      self.text)
        self.assertNotIn("contents: write\n  packages:", self.text)

    def test_runs_on_a_github_hosted_runner(self) -> None:
        self.assertIn("runs-on: ubuntu-latest", self.text)

    def test_re_enumerates_instead_of_reusing_the_event(self) -> None:
        self.assertIn("gh pr list --repo \"$REPO\" --state open --label \"$label\"",
                      self.text)
        self.assertIn("--json number", self.text)
        # The triggering event decides only whether to run.
        self.assertNotIn("github.event.pull_request.head.sha", self.text)
        self.assertNotIn("github.event.pull_request.base.sha", self.text)

    def test_judges_a_fresh_merge_candidate_and_pins_the_head(self) -> None:
        self.assertIn("git merge-tree --write-tree --no-messages \"${base_sha}\" \"${head_sha}\"",
                      self.text)
        self.assertIn('git fetch --quiet origin "+refs/pull/${pr}/head:', self.text)
        self.assertIn('--base "${base_sha}" --head "${head_sha}"', self.text)
        self.assertIn('-f sha="${head_sha}" -f merge_method=merge', self.text)

    def test_declares_the_unproven_serialization_boundary(self) -> None:
        self.assertIn("BROKER_SERIALIZATION_UNPROVEN", self.text)


class GateCompositionTests(unittest.TestCase):
    """The exact two references the broker passes, against a real object graph."""

    def test_unoccupied_new_directory_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit(repo, f"{ITEM}/manifest.yaml", "new\n", "claim 262")
            result = gate(repo, base, head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("introduced=1 occupied=0", result.stdout)

    def test_same_id_after_the_first_merge_is_rejected(self) -> None:
        """The race the broker exists for, replayed on the updated main."""
        with tempfile.TemporaryDirectory() as temp:
            repo, fork = init_repo(Path(temp))
            git(repo, "branch", "pr-a", fork)
            git(repo, "branch", "pr-b", fork)
            git(repo, "checkout", "-q", "pr-a")
            head_a = commit(repo, f"{ITEM}/a.txt", "A\n", "PR A")
            git(repo, "checkout", "-q", "pr-b")
            head_b = commit(repo, f"{ITEM}/b.txt", "B\n", "PR B")

            self.assertEqual(gate(repo, fork, head_a).returncode, 0)
            self.assertEqual(gate(repo, fork, head_b).returncode, 0,
                             "both pass against the stale base; that is the defect")

            git(repo, "checkout", "-q", "-B", "main-after-a", head_a)
            fresh = git(repo, "rev-parse", "HEAD")
            result = gate(repo, fresh, head_b)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("VIOLATION", result.stdout)

    def test_additive_file_under_existing_directory_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            base = commit(repo, f"{ITEM}/manifest.yaml", "existing\n", "existing")
            head = commit(repo, f"{ITEM}/scope-correction.md", "note\n", "additive")
            result = gate(repo, base, head)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("introduced=0 occupied=0", result.stdout)

    def test_conflicting_candidates_yield_no_merge_candidate(self) -> None:
        """Same directory, same filename: there is no tree to judge, so no merge."""
        with tempfile.TemporaryDirectory() as temp:
            repo, fork = init_repo(Path(temp))
            git(repo, "branch", "pr-a", fork)
            git(repo, "branch", "pr-b", fork)
            git(repo, "checkout", "-q", "pr-a")
            head_a = commit(repo, f"{ITEM}/manifest.yaml", "claimant A\n", "PR A")
            git(repo, "checkout", "-q", "pr-b")
            commit(repo, f"{ITEM}/manifest.yaml", "claimant B\n", "PR B")
            git(repo, "checkout", "-q", "-B", "main", head_a)

            result = merge_candidate(repo, "main", "pr-b")
            self.assertEqual(result.returncode, 1,
                             "expected an add/add conflict, got: " + result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
