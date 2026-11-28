from __future__ import annotations

import contextlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.governance.session_evidence import validate
from tests.session_evidence import support

from tests.merge_group.fixtures import (
    BASE_SHA,
    CANDIDATE_SHA,
    HEAD_1,
    HEAD_2,
)


REPOSITORY = support.REPOSITORY
EFFECTIVE_AT = support.EFFECTIVE_AT


class MergeGroupValidateIntegrationTests(unittest.TestCase):
    def _member(self, position, number, head_sha, body):
        return {
            "position": position,
            "number": number,
            "head_sha": head_sha,
            "body": body,
        }

    def _write_members_file(self, directory, members):
        path = Path(directory) / "merge-group-members.json"
        path.write_text(
            json.dumps(
                {
                    "repository": REPOSITORY,
                    "tail_pr": members[-1]["number"],
                    "base_sha": BASE_SHA,
                    "candidate_sha": CANDIDATE_SHA,
                    "members": members,
                }
            ),
            encoding="utf-8",
        )
        return str(path)

    def _merge_group_environment(self, members_path):
        return {
            "GITHUB_EVENT_NAME": "merge_group",
            "GITHUB_REPOSITORY": REPOSITORY,
            "AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC": EFFECTIVE_AT,
            "MERGE_GROUP_MEMBERS_JSON": members_path,
            "GITHUB_STEP_SUMMARY": "",
        }

    def _single_pr_environment(self):
        return {
            "GITHUB_EVENT_NAME": "pull_request",
            "GITHUB_REPOSITORY": REPOSITORY,
            "AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC": EFFECTIVE_AT,
            "PR_NUMBER": "101",
            "GITHUB_STEP_SUMMARY": "",
        }

    def _make_cumulative_world(self, invalid_first_body=False):
        entry_101 = support.make_entry(101, suffix="a")
        entry_102 = support.make_entry(102, suffix="b")
        entries = [entry_101, entry_102]

        body_101_refs = (
            ["docs/session-evidence/does-not-exist.md"]
            if invalid_first_body
            else [entry_101["session_evidence_ref"]]
        )
        body_102_refs = [entry_102["session_evidence_ref"]]

        body_101 = support.make_pr_body(
            number=101,
            refs=body_101_refs,
            issue_refs=[entry_101["session_evidence_ref"]],
        )
        body_102 = support.make_pr_body(
            number=102,
            refs=body_102_refs,
            issue_refs=[entry_102["session_evidence_ref"]],
        )

        world = support.make_valid_world(
            number=101,
            entries=entries,
            pr_body=body_101,
        )

        blobs = world["blobs"]
        tree = world["git_tree"]
        raw_by_sha = world["raw_by_sha"]

        text_by_sha = {
            item["sha"]: item["_raw"].decode("utf-8", errors="strict")
            for item in blobs
            if item["path"] not in (
                support.PROMPT_A,
                support.PROMPT_B,
            )
        }

        pr_responses = {
            101: {
                "number": 101,
                "body": body_101,
                "created_at": "2030-01-01T00:00:00Z",
                "head": {
                    "sha": HEAD_1,
                    "repo": {"full_name": REPOSITORY},
                },
            },
            102: {
                "number": 102,
                "body": body_102,
                "created_at": "2030-01-01T00:00:00Z",
                "head": {
                    "sha": HEAD_2,
                    "repo": {"full_name": REPOSITORY},
                },
            },
        }

        issue_responses = {
            101: {
                "number": 101,
                "html_url": support.issue_url(101),
                "created_at": "2031-01-01T00:00:00Z",
                "body": support.ISSUE_BODY_YES,
            },
            102: {
                "number": 102,
                "html_url": support.issue_url(102),
                "created_at": "2031-01-01T00:00:00Z",
                "body": support.ISSUE_BODY_YES,
            },
        }

        api_paths = []
        tree_calls = []

        def fake_api(path):
            api_paths.append(path)

            for number, response in pr_responses.items():
                if path == f"/repos/{REPOSITORY}/pulls/{number}":
                    return response

            for number, response in issue_responses.items():
                if path == f"/repos/{REPOSITORY}/issues/{number}":
                    return response

            if path == (
                f"/repos/{REPOSITORY}/compare/"
                f"{BASE_SHA}...{CANDIDATE_SHA}"
            ):
                return {
                    "files": [
                        {
                            "filename": (
                                "14-ai-development/work-items/"
                                "AID-2026-001/manifest.yaml"
                            )
                        }
                    ],
                    "truncated": False,
                }

            raise validate.ValidationError(
                f"Unexpected fake API path: {path}"
            )

        def fake_tree(repo, sha):
            tree_calls.append((repo, sha))
            if repo != REPOSITORY:
                raise AssertionError(f"Unexpected repository: {repo}")
            if sha != CANDIDATE_SHA:
                raise AssertionError(f"Unexpected tree SHA: {sha}")
            return tree

        def fake_blob_bytes(repo, sha, path):
            if repo != REPOSITORY:
                raise AssertionError(f"Unexpected repository: {repo}")
            if sha not in raw_by_sha:
                raise validate.ValidationError(
                    f"Unknown fake blob for {path}: {sha}"
                )
            return raw_by_sha[sha]

        def fake_blob_text(repo, sha, path):
            if repo != REPOSITORY:
                raise AssertionError(f"Unexpected repository: {repo}")
            if sha not in text_by_sha:
                raise validate.ValidationError(
                    f"Text blob unavailable: {path}"
                )
            return text_by_sha[sha]

        return {
            "api": fake_api,
            "fake_tree": fake_tree,
            "blob_bytes": fake_blob_bytes,
            "blob_text": fake_blob_text,
            "api_paths": api_paths,
            "tree_calls": tree_calls,
            "pr_responses": pr_responses,
            "body_101": body_101,
            "body_102": body_102,
            "candidate_tree": tree,
        }

    def _run_merge_group(self, members, world):
        with tempfile.TemporaryDirectory() as directory:
            members_path = self._write_members_file(directory, members)
            summary_path = Path(directory) / "step-summary.txt"

            environment = self._merge_group_environment(members_path)
            environment["GITHUB_STEP_SUMMARY"] = str(summary_path)

            output = []
            with (
                mock.patch.dict(os.environ, environment, clear=False),
                mock.patch.object(validate, "gh_api", side_effect=world["api"]),
                mock.patch.object(
                    validate, "gh_tree", side_effect=world["fake_tree"]
                ),
                mock.patch.object(
                    validate,
                    "gh_blob_bytes",
                    side_effect=world["blob_bytes"],
                ),
                mock.patch.object(
                    validate,
                    "gh_blob_text",
                    side_effect=world["blob_text"],
                ),
                mock.patch.object(
                    validate,
                    "_run_checks",
                    wraps=validate._run_checks,
                ) as run_checks,
                contextlib.redirect_stdout(_StringIO(output)),
            ):
                exit_code = validate.main([])

            summary = summary_path.read_text(encoding="utf-8")
            return exit_code, "".join(output), summary, run_checks

    def test_cumulative_candidate_checks_both_member_bodies(self):
        """输入：#101 与 #102 均合法，候选 tree 累计包含两者证据。
        期望错误码：无；期望退出码：0。
        断言点：两个 PR API 均被读取；两个 body 均进入真实 _run_checks；
        两个 context 均使用 CANDIDATE_SHA；tree 从未使用成员 head SHA；
        总 verdict 为 PRESENT，summary 只有一条 AI-SESSION-EVIDENCE 行。
        """
        world = self._make_cumulative_world()
        members = [
            self._member(1, 101, HEAD_1, world["body_101"]),
            self._member(2, 102, HEAD_2, world["body_102"]),
        ]

        exit_code, stdout, summary, run_checks = self._run_merge_group(
            members,
            world,
        )

        self.assertEqual(exit_code, 0)
        self.assertIn("AI-SESSION-EVIDENCE: PRESENT", stdout)

        self.assertIn(
            f"/repos/{REPOSITORY}/pulls/101",
            world["api_paths"],
        )
        self.assertIn(
            f"/repos/{REPOSITORY}/pulls/102",
            world["api_paths"],
        )

        checked_contexts = [
            call.args[0]
            for call in run_checks.call_args_list
        ]
        self.assertEqual(len(checked_contexts), 2)
        self.assertEqual(
            [ctx.pr_number for ctx in checked_contexts],
            [101, 102],
        )
        self.assertEqual(
            [ctx.body for ctx in checked_contexts],
            [world["body_101"], world["body_102"]],
        )
        self.assertEqual(
            [ctx.head_sha for ctx in checked_contexts],
            [CANDIDATE_SHA, CANDIDATE_SHA],
        )

        self.assertEqual(
            world["tree_calls"],
            [
                (REPOSITORY, CANDIDATE_SHA),
                (REPOSITORY, CANDIDATE_SHA),
            ],
        )
        self.assertNotIn(
            (REPOSITORY, HEAD_1),
            world["tree_calls"],
        )
        self.assertNotIn(
            (REPOSITORY, HEAD_2),
            world["tree_calls"],
        )

        summary_lines = summary.splitlines()
        verdict_lines = [
            line
            for line in summary_lines
            if line.startswith("AI-SESSION-EVIDENCE: ")
        ]
        self.assertEqual(
            verdict_lines,
            ["AI-SESSION-EVIDENCE: PRESENT"],
        )
        self.assertIn("PR #101: PRESENT:", summary)
        self.assertIn("PR #102: PRESENT:", summary)

    def test_one_invalid_member_makes_entire_candidate_violation(self):
        """输入：#101 的 body 声明 YES 但引用候选 tree 中不存在的证据路径，
        #102 合法。期望错误码：VIOLATION；期望退出码：1。
        断言点：两个 PR 都被检查；#101 为 VIOLATION、#102 为 PRESENT；
        总 verdict 为 VIOLATION，summary 不出现 PRESENT 总 verdict，
        证明不能只检查 tail PR 后部分通过。
        """
        world = self._make_cumulative_world(invalid_first_body=True)
        members = [
            self._member(1, 101, HEAD_1, world["body_101"]),
            self._member(2, 102, HEAD_2, world["body_102"]),
        ]

        exit_code, stdout, summary, run_checks = self._run_merge_group(
            members,
            world,
        )

        self.assertEqual(exit_code, 1)
        self.assertIn("AI-SESSION-EVIDENCE: VIOLATION", stdout)

        checked_contexts = [
            call.args[0]
            for call in run_checks.call_args_list
        ]
        self.assertEqual(
            [ctx.pr_number for ctx in checked_contexts],
            [101, 102],
        )
        self.assertEqual(
            [ctx.body for ctx in checked_contexts],
            [world["body_101"], world["body_102"]],
        )

        summary_lines = summary.splitlines()
        verdict_lines = [
            line
            for line in summary_lines
            if line.startswith("AI-SESSION-EVIDENCE: ")
        ]
        self.assertEqual(
            verdict_lines,
            ["AI-SESSION-EVIDENCE: VIOLATION"],
        )
        self.assertIn("PR #101: VIOLATION:", summary)
        self.assertIn("PR #102: PRESENT:", summary)
        self.assertNotIn(
            "AI-SESSION-EVIDENCE: PRESENT",
            summary,
        )

    def test_missing_members_file_is_incomplete_exit_two(self):
        """输入：merge-group members 文件路径不存在。
        期望错误码：INCOMPLETE；期望退出码：2。
        断言点：main 输出 INCOMPLETE；step summary 仅含 INCOMPLETE 总 verdict；
        不伪装成内容违规或成功。
        """
        with tempfile.TemporaryDirectory() as directory:
            missing_path = str(
                Path(directory) / "does-not-exist-members.json"
            )
            summary_path = Path(directory) / "step-summary.txt"
            environment = self._merge_group_environment(missing_path)
            environment["GITHUB_STEP_SUMMARY"] = str(summary_path)

            output = []
            with (
                mock.patch.dict(os.environ, environment, clear=False),
                contextlib.redirect_stdout(_StringIO(output)),
            ):
                exit_code = validate.main([])

            summary = summary_path.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 2)
        self.assertIn("AI-SESSION-EVIDENCE: INCOMPLETE", "".join(output))

        verdict_lines = [
            line
            for line in summary.splitlines()
            if line.startswith("AI-SESSION-EVIDENCE: ")
        ]
        self.assertEqual(verdict_lines, ["AI-SESSION-EVIDENCE: INCOMPLETE"])
        self.assertIn(
            "PR #unknown: INCOMPLETE: QUEUE_MEMBERSHIP_INCOMPLETE",
            summary,
        )

    def test_single_pull_request_path_remains_present(self):
        """输入：普通 pull_request 事件，使用既有 make_valid_world fixture。
        期望错误码：无；期望退出码：0。
        断言点：单 PR main 路径仍读取 PR head tree，返回 PRESENT；
        step summary 保持单 PR PRESENT verdict。
        """
        world = support.make_valid_world(number=101)
        raw_by_sha = world["raw_by_sha"]
        text_by_sha = {
            item["sha"]: item["_raw"].decode("utf-8", errors="strict")
            for item in world["blobs"]
            if item["path"] not in (
                support.PROMPT_A,
                support.PROMPT_B,
            )
        }

        def fake_blob_bytes(repo, sha, path):
            self.assertEqual(repo, REPOSITORY)
            if sha not in raw_by_sha:
                raise validate.ValidationError(
                    f"Unknown fake blob for {path}: {sha}"
                )
            return raw_by_sha[sha]

        def fake_blob_text(repo, sha, path):
            self.assertEqual(repo, REPOSITORY)
            if sha not in text_by_sha:
                raise validate.ValidationError(
                    f"Text blob unavailable: {path}"
                )
            return text_by_sha[sha]

        with tempfile.TemporaryDirectory() as directory:
            summary_path = Path(directory) / "step-summary.txt"
            environment = self._single_pr_environment()
            environment["GITHUB_STEP_SUMMARY"] = str(summary_path)

            output = []
            with (
                mock.patch.dict(os.environ, environment, clear=False),
                mock.patch.object(validate, "gh_api", side_effect=world["api"]),
                mock.patch.object(validate, "gh_tree", side_effect=world["tree"]),
                mock.patch.object(
                    validate,
                    "gh_blob_bytes",
                    side_effect=fake_blob_bytes,
                ),
                mock.patch.object(
                    validate,
                    "gh_blob_text",
                    side_effect=fake_blob_text,
                ),
                contextlib.redirect_stdout(_StringIO(output)),
            ):
                exit_code = validate.main([])

            summary = summary_path.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertIn("AI-SESSION-EVIDENCE: PRESENT", "".join(output))
        self.assertIn("AI-SESSION-EVIDENCE: PRESENT", summary)


class _StringIO:
    """Minimal write-only stdout collector."""

    def __init__(self, chunks):
        self.chunks = chunks

    def write(self, value):
        self.chunks.append(value)
        return len(value)

    def flush(self):
        return None


if __name__ == "__main__":
    unittest.main()
