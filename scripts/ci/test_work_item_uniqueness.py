#!/usr/bin/env python3
"""Deterministic Git-history and workflow tests for the work-item uniqueness gate.

The gate's contract: a candidate merge tree is rejected when it contains
multiple canonical record paths declaring the same work-item id. A newly
introduced id is also rejected when the target tree's claim ledger contains a
blocking claim owned by another pull request. Modifying or deleting a record
the target branch already owns is not a duplicate declaration.

Two layers of evidence:

  * synthetic repositories for each accept/reject row, including the three
    duplicate/claim shapes and the supported legacy identity shapes;
  * a pinned regression over the eight most recent first-parent commits of
    main, comparing the old rule (verbatim copy of the #1413 implementation in
    ``fixtures/legacy_shared_id_rule_1413.py``) with the current rule on the
    same base/head pair.

Run: python scripts/ci/test_work_item_uniqueness.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_work_item_uniqueness.py")
LEGACY = Path(__file__).with_name("fixtures") / "legacy_shared_id_rule_1413.py"
REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "document-management.yml"

ITEM = "14-ai-development/work-items/AID-2026-279"
OTHER_ITEM = "14-ai-development/work-items/AID-2026-280"
RECORD = f"{ITEM}/manifest.yaml"
OTHER_RECORD = f"{OTHER_ITEM}/manifest.yaml"
LEDGER = "14-ai-development/work-items/registry/work-item-claims.yaml"
REPOSITORY = "oahcom/AiMemoryBrainArchitecture"

# Eight most recent first-parent commits of origin/main when this window was
# pinned, each paired with its first parent. Immutable: this is history.
FIRST_PARENT_WINDOW = (
    ("31c1e5d83e7dad326dbd4b69d4a8e19534718ff1", "159095f3cc5dca9d40ad3856aaa493b164c0ca2e"),
    ("159095f3cc5dca9d40ad3856aaa493b164c0ca2e", "56c3fe1b2e3859fdd713a6dece3a959943b8a20a"),
    ("56c3fe1b2e3859fdd713a6dece3a959943b8a20a", "561e9f2471d09828cf7a91dc5b24bbfe82b2e213"),
    ("561e9f2471d09828cf7a91dc5b24bbfe82b2e213", "981397d99b76123678382bcbdd298333a72176c9"),
    ("981397d99b76123678382bcbdd298333a72176c9", "460f437eb3496e10737b9ef20f4b816e34d155c4"),
    ("460f437eb3496e10737b9ef20f4b816e34d155c4", "6482901cbc55e98d4a53f2203e6864b34a888b26"),
    ("6482901cbc55e98d4a53f2203e6864b34a888b26", "da69e43f8be029a5d13c2e4781b7c84c64e3aa42"),
    ("da69e43f8be029a5d13c2e4781b7c84c64e3aa42", "cd1722e753a429247d91f990caa2defac565e308"),
)

# Old rule verdicts on this window, measured with base = first parent. The
# numbers are work-item ids the old rule reported as competing declarations,
# not path counts. Pinned so that a drift in the oracle or in the window fails
# loudly instead of quietly widening or narrowing the claim.
OLD_RULE_FALSE_POSITIVE_IDS = {
    "31c1e5d83e7dad326dbd4b69d4a8e19534718ff1": 45,
    "6482901cbc55e98d4a53f2203e6864b34a888b26": 1,
}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def record(work_item_id: str, title: str = "t") -> str:
    return f"work_item_id: {work_item_id}\ntitle: {title}\n"


def ledger(*claims: tuple[str, str, int, str]) -> str:
    lines = ["schema_version: 1", "claims:"]
    for work_item_id, status, number, repository in claims:
        lines += [
            f"  - work_item_id: {work_item_id}",
            f"    status: {status}",
            f"    pull_request: {number}",
            f"    repository: {repository}",
        ]
    return "\n".join(lines) + "\n"


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


def delete_path(repo: Path, path: str, message: str) -> str:
    git(repo, "rm", "-q", path)
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


def run_checker(
    script: Path,
    repo: Path,
    base: str | None,
    head: str,
    *,
    extra: list[str] | None = None,
    echo: bool = True,
) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, str(script), "--head", head]

    if base is not None:
        args += ["--base", base]

    if extra:
        args += extra

    if echo:
        print("$ " + " ".join(args), flush=True)

    result = subprocess.run(
        args,
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if echo:
        print(result.stdout.strip())

        if result.stderr.strip():
            print(result.stderr.strip())

    return result


def invoke(
    repo: Path,
    base: str | None,
    head: str,
    *,
    extra: list[str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return run_checker(SCRIPT, repo, base, head, extra=extra)


class WorkItemUniquenessTests(unittest.TestCase):

    def assertPass(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(
            result.returncode,
            0,
            result.stdout + result.stderr,
        )
        self.assertIn("PASS", result.stdout)

    def assertViolation(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(
            result.returncode,
            1,
            result.stdout + result.stderr,
        )
        self.assertIn("VIOLATION", result.stdout)

    def assertIncomplete(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(
            result.returncode,
            2,
            result.stdout + result.stderr,
        )
        self.assertIn("INCOMPLETE", result.stdout)

    def test_new_unoccupied_record_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "new item",
            )

            result = invoke(repo, base, head)

            self.assertPass(result)
            self.assertIn("introduced=1", result.stdout)

    def test_additive_file_under_existing_record_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "existing",
            )

            head = commit_file(
                repo,
                f"{ITEM}/evidence.md",
                "additive\n",
                "add evidence",
            )

            result = invoke(repo, base, head)

            self.assertPass(result)
            self.assertIn("introduced=0", result.stdout)
            self.assertIn("shared=1", result.stdout)

    # The same record path, same id, content changed, is a legal modification.
    def test_same_path_modification_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                RECORD,
                record("AID-2026-279", "before"),
                "existing",
            )

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279", "after"),
                "retitle",
            )

            result = invoke(repo, base, head)

            self.assertPass(result)
            self.assertIn("introduced=0", result.stdout)
            self.assertIn("duplicate_declarations=0", result.stdout)

    # A deletion removes a declaration. It does not create one.
    def test_deletion_of_shared_record_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "existing",
            )

            head = delete_path(repo, RECORD, "remove record")

            result = invoke(repo, base, head)

            self.assertPass(result)
            self.assertIn("candidate_ids=0", result.stdout)
            self.assertIn("shared=0", result.stdout)

    # Legacy identity shapes are supported, and are read from content.
    def test_legacy_aid_field_is_read(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                RECORD,
                "aid: AID-2026-279\ntitle: t\n",
                "legacy aid field",
            )

            result = invoke(repo, base, head)

            self.assertPass(result)
            self.assertIn("candidate_ids=1", result.stdout)

    def test_legacy_nested_work_item_id_is_read(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                RECORD,
                "manifest_version: '1.0'\nwork_item:\n  proposed_id: AID-2026-279\n",
                "legacy nested registration",
            )

            result = invoke(repo, base, head)

            self.assertPass(result)
            self.assertIn("candidate_ids=1", result.stdout)

    def test_fix_identifier_is_accepted(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                "14-ai-development/work-items/FIX-2026-P1-T1/manifest.yaml",
                record("FIX-2026-P1-T1"),
                "fix record",
            )

            result = invoke(repo, base, head)

            self.assertPass(result)
            self.assertIn("candidate_ids=1", result.stdout)

    def test_record_without_identity_is_a_violation(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                RECORD,
                "title: no identity here\n",
                "missing identity",
            )

            result = invoke(repo, base, head)

            self.assertViolation(result)
            self.assertIn("WORK_ITEM_ID_MISSING", result.stdout)

    def test_directory_identity_mismatch_is_a_violation(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-280"),
                "mislabelled directory",
            )

            result = invoke(repo, base, head)

            self.assertViolation(result)
            self.assertIn("WORK_ITEM_PATH_ID_MISMATCH", result.stdout)

    # Duplicate detection and path-identity detection are independent and are
    # both reported for one input.
    def test_duplicate_and_path_mismatch_are_both_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "correct record",
            )
            head = commit_file(
                repo,
                OTHER_RECORD,
                record("AID-2026-279"),
                "second path, wrong directory",
            )

            result = invoke(repo, base, head)

            self.assertViolation(result)
            self.assertIn("DUPLICATE_WORK_ITEM_ID", result.stdout)
            self.assertIn("WORK_ITEM_PATH_ID_MISMATCH", result.stdout)

    # Positive case: two different work-item directories declaring one id.
    def test_two_work_item_directories_declaring_one_id_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "first directory",
            )
            head = commit_file(
                repo,
                OTHER_RECORD,
                record("AID-2026-279"),
                "second directory, same id",
            )

            result = invoke(repo, base, head)

            self.assertViolation(result)
            self.assertIn("duplicate_declarations=1", result.stdout)

    # Positive case: the id is already owned by the base tip and the candidate
    # adds a second record path for it. The evaluated tree is the merge
    # candidate the workflow checks, so it contains both records.
    def test_merge_candidate_with_two_paths_for_one_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "target owns the id",
            )

            git(repo, "checkout", "-b", "topic")
            commit_file(
                repo,
                OTHER_RECORD,
                record("AID-2026-279"),
                "candidate re-declares it elsewhere",
            )

            git(repo, "checkout", "-")
            git(repo, "merge", "--no-ff", "topic", "-m", "merge candidate")

            candidate = git(repo, "rev-parse", "HEAD")

            result = invoke(repo, base, candidate)

            self.assertViolation(result)
            self.assertIn("duplicate_declarations=1", result.stdout)
            self.assertIn(RECORD, result.stdout)
            self.assertIn(OTHER_RECORD, result.stdout)

    def test_race_replay_rejects_second_candidate_on_fresh_base(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, old_base = init_repo(Path(temp))

            git(repo, "branch", "candidate-a", old_base)
            git(repo, "branch", "candidate-b", old_base)

            git(repo, "checkout", "candidate-a")
            head_a = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "candidate A",
            )

            git(repo, "checkout", "candidate-b")
            commit_file(
                repo,
                OTHER_RECORD,
                record("AID-2026-279"),
                "candidate B",
            )

            first = invoke(repo, old_base, head_a)
            self.assertPass(first)

            git(repo, "checkout", "-b", "main-after-a", head_a)
            latest = git(repo, "rev-parse", "HEAD")

            git(repo, "merge", "--no-ff", "candidate-b", "-m", "merge candidate B")
            merged = git(repo, "rev-parse", "HEAD")

            fresh_second = invoke(repo, latest, merged)

            self.assertViolation(fresh_second)
            self.assertIn("duplicate_declarations=1", fresh_second.stdout)

    # Positive case: a blocking claim owned by another pull request.
    def test_id_claimed_by_another_pull_request_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                LEDGER,
                ledger(("AID-2026-279", "CLAIMED", 9999, REPOSITORY)),
                "ledger",
            )

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "candidate declares a claimed id",
            )

            result = invoke(repo, base, head)

            self.assertViolation(result)
            self.assertIn("is already CLAIMED in the claim ledger", result.stdout)

    def test_abandoned_claim_does_not_block(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                LEDGER,
                ledger(("AID-2026-279", "ABANDONED", 9999, REPOSITORY)),
                "ledger",
            )

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "candidate",
            )

            result = invoke(repo, base, head)

            self.assertPass(result)

    def test_own_claim_is_not_a_conflict(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                LEDGER,
                ledger(("AID-2026-279", "CLAIMED", 42, REPOSITORY)),
                "ledger",
            )

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "candidate",
            )

            result = invoke(
                repo,
                base,
                head,
                extra=["--pull-request", "42", "--repository", REPOSITORY],
            )

            self.assertPass(result)

    def test_same_pull_request_number_in_another_repository_is_not_exempt(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))

            base = commit_file(
                repo,
                LEDGER,
                ledger(("AID-2026-279", "CLAIMED", 42, REPOSITORY)),
                "ledger",
            )

            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "candidate",
            )

            result = invoke(
                repo,
                base,
                head,
                extra=["--pull-request", "42", "--repository", "other/repo"],
            )

            self.assertViolation(result)

    def test_pull_request_without_repository_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))
            head = commit_file(repo, RECORD, record("AID-2026-279"), "item")

            result = invoke(repo, base, head, extra=["--pull-request", "42"])

            self.assertIncomplete(result)
            self.assertIn("requires --repository", result.stdout)

    # The candidate may not supply the ledger that decides its own occupancy.
    def test_candidate_supplied_ledger_is_not_authoritative(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            head = commit_file(
                repo,
                LEDGER,
                ledger(("AID-2026-279", "CLAIMED", 9999, REPOSITORY)),
                "candidate adds a ledger",
            )
            head = commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
                "candidate record",
            )

            result = invoke(repo, base, head)

            self.assertIncomplete(result)
            self.assertIn("bootstrap requires explicit authorization", result.stdout)

    def test_missing_base_is_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = init_repo(Path(temp))
            head = git(repo, "rev-parse", "HEAD")

            result = invoke(repo, None, head)

            self.assertIncomplete(result)
            self.assertIn("missing required ref(s): --base", result.stdout)

    # Acceptance row 2: the workflow must fetch the target branch before making
    # its decision, and serialize per candidate. Serializing by target branch
    # let one pending slot replace queued runs, so a stale verdict could
    # outlive the base it was computed against.
    def test_workflow_serializes_by_target_and_fetches_latest_base(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn(
            "group: ${{ github.workflow }}-${{ github.event_name }}-${{ "
            "github.event.pull_request.number || github.ref_name }}",
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
        # positions inside that step's target-branch branch, not against the
        # step name: the push branch legitimately has no fetch.
        branch_start = run_script.index(
            'if [ "$EVENT_NAME" = "pull_request" ]; then'
        )
        branch_end = run_script.index("\n          else", branch_start)
        branch = run_script[branch_start:branch_end]

        self.assertIn(fetch, branch)
        self.assertIn(checker, branch)
        self.assertLess(branch.index(fetch), branch.index(checker))

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

        enforcement_step = workflow.split("Enforce work-item uniqueness")[1].split(
            "- name:"
        )[0]
        # The event payload's base SHA can be stale by the time the job runs.
        # The step may export it for other steps, but the decision itself must
        # diff against the freshly fetched branch ref.
        self.assertNotIn("$PR_BASE", enforcement_step.split("run: |", 1)[-1])

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

    # The merge-group path must evaluate the queue's candidate SHA and
    # serialize on the queue's target branch, not on the candidate ref.
    def test_merge_group_uses_head_sha_and_base_ref(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn(
            "  merge_group:\n    types: [checks_requested]",
            workflow,
        )
        self.assertIn(
            "MG_BASE: ${{ github.event.merge_group.base_sha }}",
            workflow,
        )
        self.assertIn(
            "MG_HEAD: ${{ github.event.merge_group.head_sha }}",
            workflow,
        )
        self.assertIn(
            '--base "$MG_BASE" \\\n              --head "$MG_HEAD"',
            workflow,
        )
        self.assertIn(
            "EVENT_NAME: ${{ github.event_name }}",
            workflow,
        )
        self.assertNotIn(
            "group: ${{ github.workflow }}-${{ github.ref }}",
            workflow,
        )

    # Acceptance row 7: the checker must evaluate a GitHub-style merge
    # candidate whose first parent is the target base, not merely the PR head.
    def test_merge_candidate_sha_is_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, base = init_repo(Path(temp))

            git(repo, "checkout", "-b", "topic")

            commit_file(
                repo,
                RECORD,
                record("AID-2026-279"),
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

            self.assertPass(result)
            self.assertIn(f"head={candidate}", result.stdout)
            self.assertIn("introduced=1", result.stdout)


class SharedIdHistoryRegression(unittest.TestCase):
    """Old rule versus new rule on the pinned first-parent window of main.

    The old rule counted a modified or deleted path under a shared id as a
    competing declaration. The new rule must pass those commits and must still
    reject a candidate tree that declares one id twice.
    """

    @classmethod
    def setUpClass(cls):
        missing = [
            sha
            for head, base in FIRST_PARENT_WINDOW
            for sha in (head, base)
            if subprocess.run(
                ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                cwd=REPO,
                capture_output=True,
            ).returncode
        ]
        if missing:
            raise RuntimeError(
                "the pinned regression window is not present in this clone "
                f"(missing {missing[0]}); CI must fetch full history with "
                "fetch-depth: 0 rather than skip this regression"
            )

        cls.rows = []

        for head, base in FIRST_PARENT_WINDOW:
            old = run_checker(LEGACY, REPO, base, head, echo=False)
            new = run_checker(SCRIPT, REPO, base, head, echo=False)
            cls.rows.append((head, base, old, new))

        print("\ncommit     base       verdict_old  verdict_new  triggering_ids")
        for head, base, old, new in cls.rows:
            ids = [
                line.split(": ", 1)[1].split(" ", 1)[0]
                for line in old.stdout.splitlines()
                if line.startswith("VIOLATION: ")
            ]
            print(
                f"{head[:9]}  {base[:9]}  "
                f"{'VIOLATION' if old.returncode == 1 else 'PASS':<12}"
                f"{'VIOLATION' if new.returncode == 1 else 'PASS':<12}"
                f"{len(ids)} id(s)"
            )
            for work_item_id in ids:
                print(f"    {work_item_id}")

        cls.old_red = {
            head: old
            for head, _, old, _ in cls.rows
            if old.returncode != 0
        }
        cls.new_red = {
            head: new
            for head, _, _, new in cls.rows
            if new.returncode != 0
        }

        print(
            f"[regression] rows={len(cls.rows)} "
            f"old_red={len(cls.old_red)} old_pass={len(cls.rows) - len(cls.old_red)} "
            f"new_red={len(cls.new_red)} new_pass={len(cls.rows) - len(cls.new_red)}"
        )

    def test_old_rule_rejected_exactly_the_pinned_commits(self):
        self.assertEqual(
            set(self.old_red),
            set(OLD_RULE_FALSE_POSITIVE_IDS),
            "the old rule's verdicts on this window changed; re-measure before "
            "trusting the comparison",
        )

    def test_old_rule_false_positives_are_shared_id_changes(self):
        for head, output in self.old_red.items():
            self.assertEqual(
                output.returncode,
                1,
                f"{head}: expected the old rule to reject",
            )
            self.assertIn(
                "modifies or deletes a record the target branch already owns",
                output.stdout,
                f"{head}: expected a shared-id M/D verdict",
            )

    def test_new_rule_passes_every_commit_in_the_window(self):
        self.assertEqual(
            self.new_red,
            {},
            "the new rule rejected a commit: "
            + "; ".join(
                f"{head}: {output.stdout.strip()}"
                for head, output in self.new_red.items()
            ),
        )

    def test_new_rule_reports_no_duplicate_declarations(self):
        for head, _, _, new in self.rows:
            self.assertIn("duplicate_declarations=0", new.stdout)
        self.assertNotIn(
            "VIOLATION",
            "".join(new.stdout for _, _, _, new in self.rows),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
