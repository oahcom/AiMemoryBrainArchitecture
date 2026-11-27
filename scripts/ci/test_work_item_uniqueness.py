#!/usr/bin/env python3
"""Deterministic Git-history and workflow tests for the work-item uniqueness gate."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_work_item_uniqueness.py")
WORKFLOW = (
    Path(__file__).resolve().parents[2]
    / ".github"
    / "workflows"
    / "document-management.yml"
)
ITEM = "14-ai-development/work-items/AID-2026-279"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def commit_file(
    repo: Path,
    path: str,
    content: str,
    message: str,
) -> str:
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

    base = commit_file(repo, "README.md", "base\n", "base")
    return repo, base


def invoke(
    repo: Path,
    base: str | None,
    head: str,
) -> subprocess.CompletedProcess[str]:
    args = [
        sys.executable,
        str(SCRIPT),
        "--head",
        head,
    ]

    if base is not None:
        args += ["--base", base]

    print("$ " + " ".join(args), flush=True)

    result = subprocess.run(
        args,
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    print(result.stdout.strip())

    if result.stderr.strip():
        print(result.stderr.strip())

    return result


def legacy_merge_base_counts(repo: Path, base: str, head: str) -> tuple[int, int]:
    """Reproduce the former merge-base introduction/occupancy calculation.

    Kept only to prove that the previous algorithm reports a false PASS on the
    Update-branch and merge-queue graphs asserted below.
    """
    merge_base = git(repo, "merge-base", base, head)
    added = git(
        repo,
        "diff",
        "--diff-filter=A",
        "--name-only",
        "--no-renames",
        merge_base,
        head,
        "--",
        "14-ai-development/work-items",
    ).splitlines()

    introduced = set()

    for name in added:
        parts = name.split("/")
        if len(parts) < 4 or not parts[2].startswith("AID-"):
            continue

        directory = "/".join(parts[:3])
        present = subprocess.run(
            ["git", "cat-file", "-e", f"{merge_base}:{directory}"],
            cwd=repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).returncode == 0

        if not present:
            introduced.add(directory)

    occupied = sum(
        subprocess.run(
            ["git", "cat-file", "-e", f"{base}:{directory}"],
            cwd=repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).returncode == 0
        for directory in introduced
    )

    return len(introduced), occupied


class WorkItemUniquenessTests(unittest.TestCase):

    def test_new_unoccupied_directory_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                f"{ITEM}/manifest.yaml",
                "new\n",
                "new item",
            )

            result = invoke(repo, base, head)

            self.assertEqual(
                result.returncode,
                0,
                result.stdout + result.stderr,
            )
            self.assertIn("introduced=1 occupied=0", result.stdout)

    def test_occupied_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, ancestor = init_repo(Path(temp))

            git(repo, "checkout", "-b", "topic")

            topic = commit_file(
                repo,
                f"{ITEM}/topic.txt",
                "topic\n",
                "topic claim",
            )

            git(repo, "checkout", "-b", "main-simulated", ancestor)

            latest = commit_file(
                repo,
                f"{ITEM}/main.txt",
                "main\n",
                "main claim",
            )

            result = invoke(repo, latest, topic)

            self.assertEqual(
                result.returncode,
                1,
                result.stdout + result.stderr,
            )
            self.assertIn("VIOLATION", result.stdout)

    def test_additive_file_under_existing_directory_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                f"{ITEM}/manifest.yaml",
                "existing\n",
                "existing",
            )

            head = commit_file(
                repo,
                f"{ITEM}/evidence.md",
                "additive\n",
                "add evidence",
            )

            result = invoke(repo, base, head)

            self.assertEqual(
                result.returncode,
                0,
                result.stdout + result.stderr,
            )
            self.assertIn("introduced=0 occupied=0", result.stdout)

    def test_race_replay_rejects_second_candidate_on_fresh_base(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, old_base = init_repo(Path(temp))

            git(repo, "branch", "candidate-a", old_base)
            git(repo, "branch", "candidate-b", old_base)

            git(repo, "checkout", "candidate-a")
            head_a = commit_file(
                repo,
                f"{ITEM}/a.txt",
                "A\n",
                "candidate A",
            )

            git(repo, "checkout", "candidate-b")
            head_b = commit_file(
                repo,
                f"{ITEM}/b.txt",
                "B\n",
                "candidate B",
            )

            first = invoke(repo, old_base, head_a)
            stale_second = invoke(repo, old_base, head_b)

            self.assertEqual(
                first.returncode,
                0,
                first.stdout + first.stderr,
            )
            self.assertEqual(
                stale_second.returncode,
                0,
                stale_second.stdout + stale_second.stderr,
            )

            git(repo, "checkout", "-b", "main-after-a", head_a)
            latest = git(repo, "rev-parse", "HEAD")

            fresh_second = invoke(repo, latest, head_b)

            self.assertEqual(
                fresh_second.returncode,
                1,
                fresh_second.stdout + fresh_second.stderr,
            )
            self.assertIn("VIOLATION", fresh_second.stdout)

    def test_missing_base_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            head = git(repo, "rev-parse", "HEAD")

            result = invoke(repo, None, head)

            self.assertEqual(
                result.returncode,
                2,
                result.stdout + result.stderr,
            )
            self.assertIn("INCOMPLETE", result.stdout)

    # Acceptance row 2: the workflow must serialize all candidates for the
    # same target branch and fetch that branch before making its decision.
    # Reverting to head-SHA concurrency or removing the fresh fetch makes
    # this test fail because competing PRs can again use independent stale bases.
    def test_workflow_serializes_by_target_and_fetches_latest_base(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn(
            "group: ${{ github.workflow }}-${{ "
            "github.event.pull_request.base.ref || github.ref_name }}",
            workflow,
        )
        self.assertIn("cancel-in-progress: false", workflow)

        enforcement_marker = (
            "- name: Enforce work-item uniqueness against the current target base"
        )
        enforcement_position = workflow.index(enforcement_marker)

        run_marker = "run: |"
        run_position = workflow.index(run_marker, enforcement_position)
        run_start = run_position + len(run_marker)

        next_step = workflow.find("\n      - name:", run_start)
        self.assertNotEqual(
            next_step,
            -1,
            "The enforcement step must be followed by another workflow step",
        )

        run_script = workflow[run_start:next_step]

        fetch = (
            'git fetch origin '
            '"+refs/heads/${BASE_REF}:refs/remotes/origin/${BASE_REF}"'
        )
        checker = "scripts/ci/check_work_item_uniqueness.py"

        self.assertIn(fetch, run_script)
        self.assertIn(checker, run_script)
        self.assertIn(
            '--base "refs/remotes/origin/$BASE_REF"',
            run_script,
        )

        # The fetch and decision intentionally share one step. Compare their
        # positions inside that step's run script, not against the step name.
        # Reverting the fetch to occur after the checker, or removing it,
        # makes this assertion fail.
        fetch_position = run_script.index(fetch)
        checker_position = run_script.index(checker)

        self.assertLess(fetch_position, checker_position)

    # Acceptance row 7: the checker must evaluate a GitHub-style merge
    # candidate whose first parent is the target base, not merely the PR head.
    # Reverting the workflow to pass the source HEAD would remove this exact
    # candidate from the evaluated input and leave the required check attached
    # to an earlier commit.
    def test_merge_candidate_sha_is_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            git(repo, "checkout", "-b", "topic")

            commit_file(
                repo,
                f"{ITEM}/manifest.yaml",
                "candidate\n",
                "candidate item",
            )

            git(repo, "checkout", "-")
            git(repo, "merge", "--no-ff", "topic", "-m", "merge candidate")

            candidate = git(repo, "rev-parse", "HEAD")

            self.assertEqual(
                git(repo, "rev-parse", f"{candidate}^1"),
                base,
            )

            result = invoke(repo, base, candidate)

            self.assertEqual(
                result.returncode,
                0,
                result.stdout + result.stderr,
            )
            self.assertIn(
                f"candidate={candidate}",
                result.stdout,
            )
            self.assertIn("introduced=1 occupied=0", result.stdout)

    # Acceptance row 7: the pull_request enforcement command must use
    # github.sha, which identifies the generated merge candidate. Reverting
    # to github.event.pull_request.head.sha makes this assertion fail.
    def test_workflow_checks_github_merge_candidate_not_pr_head(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn(
            "CANDIDATE_SHA: ${{ github.sha }}",
            workflow,
        )
        self.assertIn(
            '--head "$CANDIDATE_SHA"',
            workflow,
        )
        self.assertNotIn(
            "github.event.pull_request.head.sha",
            workflow,
        )

        self.assertIn(
            "github.event.pull_request.base.ref",
            workflow,
        )

        self.assertIn(
            "PR_BASE: ${{ github.event.pull_request.base.sha }}",
            workflow,
        )

        self.assertLess(
            workflow.index("- name: Self-check the gate"),
            workflow.index("- name: Self-test work-item uniqueness gate"),
        )
        self.assertLess(
            workflow.index("- name: Self-test work-item uniqueness gate"),
            workflow.index(
                "- name: Enforce work-item uniqueness against the current target base"
            ),
        )


    # Claim identity: an Update-branch merge moves the merge-base past the
    # candidate's claim commit. The legacy merge-base algorithm then reports
    # introduced=0 occupied=0 (false PASS); the first-parent claim identity
    # still sees B's original commit and rejects the duplicate ID.
    def test_update_branch_keeps_original_claim_and_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, old_base = init_repo(Path(temp))

            git(repo, "branch", "candidate-a", old_base)
            git(repo, "branch", "candidate-b", old_base)

            git(repo, "checkout", "candidate-a")
            head_a = commit_file(repo, f"{ITEM}/a.txt", "A\n", "candidate A")

            git(repo, "checkout", "candidate-b")
            head_b = commit_file(repo, f"{ITEM}/b.txt", "B\n", "candidate B")

            # A lands first; the target base now owns AID-2026-311.
            git(repo, "checkout", "-b", "main-after-a", head_a)
            latest_base = git(repo, "rev-parse", "HEAD")

            # B presses "Update branch": the advanced target is merged into B.
            git(repo, "checkout", "candidate-b")
            git(
                repo,
                "merge",
                "--no-ff",
                "-m",
                "Update branch from main-after-a",
                "main-after-a",
            )
            updated_b = git(repo, "rev-parse", "HEAD")

            self.assertEqual(
                git(repo, "merge-base", latest_base, updated_b),
                latest_base,
            )

            legacy = legacy_merge_base_counts(repo, latest_base, updated_b)
            print(
                "LEGACY MERGE-BASE RESULT: "
                f"introduced={legacy[0]} occupied={legacy[1]} (false PASS)"
            )
            self.assertEqual(legacy, (0, 0))

            self.assertIn(
                f"{ITEM}/a.txt",
                git(repo, "ls-tree", "-r", "--name-only", updated_b),
            )
            self.assertIn(
                f"{ITEM}/b.txt",
                git(repo, "ls-tree", "-r", "--name-only", updated_b),
            )

            result = invoke(repo, latest_base, updated_b)

            self.assertEqual(
                result.returncode,
                1,
                result.stdout + result.stderr,
            )
            self.assertIn("VIOLATION", result.stdout)
            self.assertIn(head_b, result.stdout)
            self.assertIn("introduced=1 occupied=1", result.stdout)

    # The same identity must hold for a merge-queue candidate: the queue
    # reconstructs the candidate as a merge of the advanced base with the
    # original head, so the original claim commit is again not the first
    # parent of anything.
    def test_merge_group_reconstruction_rejects_second_candidate(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, old_base = init_repo(Path(temp))

            git(repo, "branch", "candidate-a", old_base)
            git(repo, "branch", "candidate-b", old_base)

            git(repo, "checkout", "candidate-a")
            head_a = commit_file(repo, f"{ITEM}/a.txt", "A\n", "candidate A")

            git(repo, "checkout", "candidate-b")
            commit_file(repo, f"{ITEM}/b.txt", "B\n", "candidate B")

            git(repo, "checkout", "-b", "main-after-a", head_a)
            latest_base = git(repo, "rev-parse", "HEAD")

            git(repo, "checkout", "main-after-a")
            git(
                repo,
                "merge",
                "--no-ff",
                "-m",
                "merge_group candidate B",
                "candidate-b",
            )
            queue_candidate = git(repo, "rev-parse", "HEAD")

            self.assertEqual(
                git(repo, "merge-base", latest_base, queue_candidate),
                latest_base,
            )

            legacy = legacy_merge_base_counts(repo, latest_base, queue_candidate)
            print(
                "LEGACY MERGE-GROUP RESULT: "
                f"introduced={legacy[0]} occupied={legacy[1]} (false PASS)"
            )
            self.assertEqual(legacy, (0, 0))

            result = invoke(repo, latest_base, queue_candidate)

            self.assertEqual(
                result.returncode,
                1,
                result.stdout + result.stderr,
            )
            self.assertIn("VIOLATION", result.stdout)

    # An Update branch that does not collide must stay green: only a claim on
    # an ID the base already owns (or a duplicated claim) is a violation.
    def test_update_branch_with_unoccupied_claim_still_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, old_base = init_repo(Path(temp))

            git(repo, "checkout", "-b", "candidate-b")
            commit_file(repo, f"{ITEM}/manifest.yaml", "new\n", "claim")

            git(repo, "checkout", "-b", "main-advance", old_base)
            latest_base = commit_file(
                repo, "unrelated.txt", "advance\n", "advance base"
            )

            git(repo, "checkout", "candidate-b")
            git(repo, "merge", "--no-ff", "-m", "Update branch", "main-advance")
            updated = git(repo, "rev-parse", "HEAD")

            result = invoke(repo, latest_base, updated)

            self.assertEqual(
                result.returncode,
                0,
                result.stdout + result.stderr,
            )
            self.assertIn("introduced=1 occupied=0", result.stdout)

    # Two candidate-only commits that each create the same ID are a duplicate
    # claim even when the base does not own the directory yet.
    def test_two_candidate_only_claims_for_one_id_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            first = commit_file(repo, f"{ITEM}/first.txt", "one\n", "claim one")

            git(repo, "checkout", "-b", "side", base)
            second = commit_file(repo, f"{ITEM}/second.txt", "two\n", "claim two")

            git(repo, "checkout", "-b", "both", first)
            git(repo, "merge", "--no-ff", "-m", "merge side", "side")
            merged = git(repo, "rev-parse", "HEAD")

            self.assertIn(
                f"{ITEM}/second.txt",
                git(repo, "ls-tree", "-r", "--name-only", merged),
            )

            result = invoke(repo, base, merged)

            self.assertEqual(
                result.returncode,
                1,
                result.stdout + result.stderr,
            )
            self.assertIn("duplicate_claims=1", result.stdout)
            self.assertIn(second, result.stdout)

    def test_repeated_invocation_is_deterministic(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_file(repo, f"{ITEM}/manifest.yaml", "new\n", "claim")

            first = invoke(repo, base, head)
            retry = invoke(repo, base, head)

            self.assertEqual(first.returncode, 0)
            self.assertEqual(first.returncode, retry.returncode)
            self.assertEqual(first.stdout, retry.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
