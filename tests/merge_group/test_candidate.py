"""Offline tests for merge-group candidate resolution."""

from __future__ import annotations

import os
import shlex
import sys
import tempfile
import unittest
from unittest import mock

from scripts.governance.merge_group import candidate
from tests.merge_group import fixtures as fx


class CandidatePrefixTests(unittest.TestCase):
    def setUp(self):
        self.base = fx.BASE_SHA
        self.candidate_sha = fx.CANDIDATE_SHA

    def _ancestry(self, relations):
        def check(ancestor, descendant, repository=None):
            key = (ancestor, descendant)
            if key not in relations:
                self.fail(f"unexpected ancestry query: {key!r}")
            return relations[key]
        return check

    def _valid_relations(self):
        return {
            (self.base, self.candidate_sha): True,
            (fx.HEAD_1, self.base): False,
            (fx.HEAD_1, self.candidate_sha): True,
            (fx.HEAD_2, self.base): False,
            (fx.HEAD_2, self.candidate_sha): True,
            (fx.HEAD_3, self.base): False,
            (fx.HEAD_3, self.candidate_sha): True,
        }

    def test_base_is_ancestor_of_candidate(self):
        """B ≼ C.

        Input: Compare API establishes B ≼ C; H1/H2 are not in B and
        both are ancestors of C.
        Expected error: none.
        Expected exit: 0 at resolver layer.
        Assertion: both prefix members are returned in queue order.
        """
        with mock.patch.object(
            candidate,
            "_git_is_ancestor",
            side_effect=self._ancestry(self._valid_relations()),
        ):
            result = candidate._resolve_members(
                fx.valid_prefix(),
                102,
                self.base,
                self.candidate_sha,
            )

        self.assertEqual([101, 102], [item["number"] for item in result])

    def test_base_not_ancestor_of_candidate_is_violation(self):
        """B ⋠ C.

        Input: Compare API says B is not an ancestor of C.
        Expected error: BASE_NOT_IN_CANDIDATE.
        Expected exit: 1.
        Assertion: CandidateViolation is raised, not incomplete.
        """
        relations = {(self.base, self.candidate_sha): False}
        with mock.patch.object(
            candidate,
            "_git_is_ancestor",
            side_effect=self._ancestry(relations),
        ):
            with self.assertRaisesRegex(
                candidate.CandidateViolation,
                "BASE_NOT_IN_CANDIDATE",
            ):
                candidate._resolve_members(
                    fx.valid_prefix(),
                    102,
                    self.base,
                    self.candidate_sha,
                )

    def test_member_head_is_ancestor_of_candidate(self):
        """H_i ≼ C.

        Input: B ≼ C, H_i ⋠ B, and H_i ≼ C.
        Expected error: none.
        Expected exit: 0 at resolver layer.
        Assertion: the member is accepted into the candidate prefix.
        """
        relations = {
            (self.base, self.candidate_sha): True,
            (fx.HEAD_1, self.base): False,
            (fx.HEAD_1, self.candidate_sha): True,
        }
        with mock.patch.object(
            candidate,
            "_git_is_ancestor",
            side_effect=self._ancestry(relations),
        ):
            result = candidate._resolve_members(
                [fx.entry(1, 101, fx.HEAD_1)],
                101,
                self.base,
                self.candidate_sha,
            )
        self.assertEqual([101], [item["number"] for item in result])

    def test_member_head_not_ancestor_of_candidate_is_violation(self):
        """H_i ⋠ C.

        Input: B ≼ C; H_i is not in B and not an ancestor of C.
        Expected error: PR_HEAD_NOT_IN_CANDIDATE.
        Expected exit: 1.
        Assertion: offending PR number appears in the error.
        """
        relations = {
            (self.base, self.candidate_sha): True,
            (fx.HEAD_1, self.base): False,
            (fx.HEAD_1, self.candidate_sha): False,
        }
        with mock.patch.object(
            candidate,
            "_git_is_ancestor",
            side_effect=self._ancestry(relations),
        ):
            with self.assertRaisesRegex(
                candidate.CandidateViolation,
                "PR_HEAD_NOT_IN_CANDIDATE.*#101",
            ):
                candidate._resolve_members(
                    [fx.entry(1, 101, fx.HEAD_1)],
                    101,
                    self.base,
                    self.candidate_sha,
                )

    def test_head_already_in_base_is_violation(self):
        """H_i ≼ B is a confirmed no-increment violation.

        Input: B ≼ C and H_i is already an ancestor of B.
        Expected error: PR_HEAD_ALREADY_IN_BASE.
        Expected exit: 1.
        Assertion: CandidateViolation, not QueueMembershipIncomplete.
        """
        relations = {
            (self.base, self.candidate_sha): True,
            (fx.HEAD_1, self.base): True,
        }
        with mock.patch.object(
            candidate,
            "_git_is_ancestor",
            side_effect=self._ancestry(relations),
        ):
            with self.assertRaisesRegex(
                candidate.CandidateViolation,
                "PR_HEAD_ALREADY_IN_BASE.*#101",
            ):
                candidate._resolve_members(
                    [fx.entry(1, 101, fx.HEAD_1)],
                    101,
                    self.base,
                    self.candidate_sha,
                )

    def test_missing_pull_request_in_prefix_is_incomplete(self):
        """A non-tail prefix entry has no pullRequest.

        Input: position 1 has pullRequest=null; tail #102 is at position 2.
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: malformed prefix member is not silently skipped.
        """
        nodes = [
            {
                "position": 1,
                "pullRequest": None,
                "headCommit": {"oid": fx.HEAD_1},
            },
            fx.entry(2, 102, fx.HEAD_2),
        ]
        with self.assertRaisesRegex(
            candidate.QueueMembershipIncomplete,
            "prefix entry has no pullRequest",
        ):
            candidate._resolve_members(
                nodes, 102, self.base, self.candidate_sha
            )

    def test_head_commit_must_match_head_ref_oid(self):
        """headCommit.oid must equal pullRequest.headRefOid.

        Input: queue headCommit differs from PR headRefOid.
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: identity mismatch is not treated as an ancestry violation.
        """
        nodes = [
            fx.entry(1, 101, fx.HEAD_1, candidate_sha=fx.HEAD_2)
        ]
        with self.assertRaisesRegex(
            candidate.QueueMembershipIncomplete,
            "identity changed",
        ):
            candidate._resolve_members(
                nodes, 101, self.base, self.candidate_sha
            )

    def test_empty_queue_is_incomplete(self):
        """Queue entries are empty.

        Input: nodes=[].
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: empty queue is not accepted as an empty candidate.
        """
        with self.assertRaisesRegex(
            candidate.QueueMembershipIncomplete,
            "entries are empty",
        ):
            candidate._resolve_members(
                [], 101, self.base, self.candidate_sha
            )

    def test_tail_pr_absent_is_incomplete(self):
        """Tail PR does not appear in the queue.

        Input: queue has #101, tail marker identifies #102.
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: tail lookup fails closed.
        """
        with self.assertRaisesRegex(
            candidate.QueueMembershipIncomplete,
            "tail PR #102 matched 0",
        ):
            candidate._resolve_members(
                [fx.entry(1, 101, fx.HEAD_1)],
                102,
                self.base,
                self.candidate_sha,
            )

    def test_duplicate_tail_pr_is_incomplete(self):
        """Tail PR must match exactly one entry.

        Input: two entries both identify tail PR #101.
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: ambiguous tail mapping is rejected.
        """
        nodes = [
            fx.entry(1, 101, fx.HEAD_1),
            fx.entry(2, 101, fx.HEAD_2),
        ]
        with self.assertRaisesRegex(
            candidate.QueueMembershipIncomplete,
            "tail PR #101 matched 2",
        ):
            candidate._resolve_members(
                nodes, 101, self.base, self.candidate_sha
            )

    def test_duplicate_pr_inside_prefix_is_incomplete(self):
        """PR numbers must be unique across the entire prefix.

        Input: positions 1 and 2 both identify #100; position 3 is tail #101.
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: duplicate PR number is reported after unique tail mapping.
        """
        nodes = [
            fx.entry(1, 100, fx.HEAD_1),
            fx.entry(2, 100, fx.HEAD_2),
            fx.entry(3, 101, fx.HEAD_3),
        ]
        with self.assertRaisesRegex(
            candidate.QueueMembershipIncomplete,
            "duplicate PR number",
        ):
            candidate._resolve_members(
                nodes, 101, self.base, self.candidate_sha
            )

    def test_only_positions_at_or_before_tail_are_members(self):
        """The tail position defines the candidate prefix boundary.

        Input: positions 1, 2, 3; tail #102 is at position 2.
        Expected error: none.
        Expected exit: 0 at resolver layer.
        Assertion: position 3 is excluded; members are #101 and #102.
        """
        relations = self._valid_relations()
        with mock.patch.object(
            candidate,
            "_git_is_ancestor",
            side_effect=self._ancestry(relations),
        ):
            result = candidate._resolve_members(
                fx.valid_prefix(),
                102,
                self.base,
                self.candidate_sha,
            )
        self.assertEqual([101, 102], [item["number"] for item in result])

    def test_graphql_pagination_reads_second_page_and_repeats_snapshot(self):
        """Both complete snapshots must read every page.

        Input: each snapshot has page 1 (hasNextPage=true) and page 2.
        Expected error: none.
        Expected exit: 0 at snapshot layer.
        Assertion: four GraphQL calls; second page contributes tail #102.
        """
        responses = fx.two_page_graphql_sequence()
        with mock.patch.object(
            candidate,
            "_graphql",
            side_effect=responses,
        ) as graphql:
            entries = candidate._stable_queue_snapshot(
                "token", "owner", "repo"
            )

        self.assertEqual(4, graphql.call_count)
        self.assertEqual(
            [101, 102],
            [item["pullRequest"]["number"] for item in entries],
        )

    def test_first_page_only_cannot_find_tail(self):
        """A response limited to page one cannot establish the tail.

        Input: one complete page containing only #101; tail is #102.
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: resolver refuses the partial membership.
        """
        responses = fx.one_page_graphql_sequence(
            [fx.entry(1, 101, fx.HEAD_1)]
        )
        with mock.patch.object(
            candidate,
            "_graphql",
            side_effect=responses,
        ):
            entries = candidate._stable_queue_snapshot(
                "token", "owner", "repo"
            )

        with self.assertRaisesRegex(
            candidate.QueueMembershipIncomplete,
            "tail PR #102 matched 0",
        ):
            candidate._resolve_members(
                entries, 102, self.base, self.candidate_sha
            )

    def test_pagination_without_end_cursor_is_incomplete(self):
        """hasNextPage=true requires a usable endCursor.

        Input: first page says hasNextPage=true but endCursor is null.
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: pagination is not treated as complete.
        """
        page = fx.graphql_page(
            [fx.entry(1, 101, fx.HEAD_1)],
            has_next=True,
            cursor=None,
        )
        with mock.patch.object(
            candidate, "_graphql", return_value=page
        ):
            with self.assertRaisesRegex(
                candidate.QueueMembershipIncomplete,
                "without endCursor",
            ):
                candidate._queue_snapshot("token", "owner", "repo")

    def test_changed_queue_snapshot_is_incomplete(self):
        """Queue changes between the two complete snapshots.

        Input: same position/PR number, but head identity changes.
        Expected error: QUEUE_MEMBERSHIP_INCOMPLETE.
        Expected exit: 2.
        Assertion: a snapshot race is not reported as member violation.
        """
        first = [fx.entry(1, 101, fx.HEAD_1)]
        second = [fx.entry(1, 101, fx.HEAD_2)]
        with mock.patch.object(
            candidate,
            "_queue_snapshot",
            side_effect=[first, second],
        ):
            with self.assertRaisesRegex(
                candidate.QueueMembershipIncomplete,
                "changed between snapshots",
            ):
                candidate._stable_queue_snapshot(
                    "token", "owner", "repo"
                )

    def test_compare_api_reports_ancestor(self):
        """Compare API proves ancestor relation.

        Input: behind_by=0 and merge_base_commit.sha equals ancestor.
        Expected error: none.
        Expected exit: boolean True.
        Assertion: both Compare API fields are consumed.
        """
        response = fx.compare_response(fx.HEAD_1, behind_by=0)
        with mock.patch.dict(
            os.environ,
            {"GITHUB_REPOSITORY": "owner/repo", "GITHUB_TOKEN": "token"},
        ):
            with mock.patch.object(
                candidate, "_request_json", return_value=response
            ) as request:
                result = candidate._git_is_ancestor(
                    fx.HEAD_1, fx.CANDIDATE_SHA
                )

        self.assertTrue(result)
        self.assertIn(
            f"/repos/owner/repo/compare/{fx.HEAD_1}...{fx.CANDIDATE_SHA}",
            request.call_args.args[0],
        )

    def test_compare_api_reports_non_ancestor(self):
        """Compare API proves a is not an ancestor of b.

        Input: behind_by is positive.
        Expected error: none.
        Expected exit: boolean False.
        Assertion: no local git command is invoked.
        """
        response = fx.compare_response(
            fx.HEAD_1,
            behind_by=2,
            merge_base_sha=fx.HEAD_2,
        )
        with mock.patch.dict(
            os.environ,
            {"GITHUB_REPOSITORY": "owner/repo", "GITHUB_TOKEN": "token"},
        ):
            with mock.patch.object(
                candidate, "_request_json", return_value=response
            ):
                with mock.patch.object(candidate.subprocess, "run") as run:
                    result = candidate._git_is_ancestor(
                        fx.HEAD_1, fx.CANDIDATE_SHA
                    )

        self.assertFalse(result)
        run.assert_not_called()

    def test_compare_api_incomplete_response_is_git_graph_incomplete(self):
        """Compare response missing merge base is incomplete.

        Input: behind_by exists but merge_base_commit.sha is absent.
        Expected error: GIT_GRAPH_INCOMPLETE.
        Expected exit: 2.
        Assertion: missing ancestry evidence does not become False.
        """
        with mock.patch.dict(
            os.environ,
            {"GITHUB_REPOSITORY": "owner/repo", "GITHUB_TOKEN": "token"},
        ):
            with mock.patch.object(
                candidate,
                "_request_json",
                return_value={"behind_by": 0},
            ):
                with self.assertRaisesRegex(
                    candidate.GitGraphIncomplete,
                    "GIT_GRAPH_INCOMPLETE",
                ):
                    candidate._git_is_ancestor(
                        fx.HEAD_1, fx.CANDIDATE_SHA
                    )

    def test_compare_api_failure_is_git_graph_incomplete(self):
        """Compare API transport failure is incomplete.

        Input: _request_json raises an API error.
        Expected error: GIT_GRAPH_INCOMPLETE.
        Expected exit: 2.
        Assertion: API failure is not a candidate violation.
        """
        with mock.patch.dict(
            os.environ,
            {"GITHUB_REPOSITORY": "owner/repo", "GITHUB_TOKEN": "token"},
        ):
            with mock.patch.object(
                candidate,
                "_request_json",
                side_effect=OSError("network unavailable"),
            ):
                with self.assertRaisesRegex(
                    candidate.GitGraphIncomplete,
                    "GIT_GRAPH_INCOMPLETE",
                ):
                    candidate._git_is_ancestor(
                        fx.HEAD_1, fx.CANDIDATE_SHA
                    )


class ExecCommandTests(unittest.TestCase):
    def test_shlex_preserves_quoted_argument_cross_platform(self):
        """A quoted command argument works with the active Python executable.

        Input: sys.executable plus a quoted -c program and output path.
        Expected error: none.
        Expected exit: 0.
        Assertion: shlex preserves the executable path and one code argument.
        """
        with tempfile.TemporaryDirectory() as directory:
            output_path = os.path.join(directory, "value.txt")
            code = (
                "import os; "
                "open(os.environ['OUT'], 'w', encoding='utf-8').write('two words')"
            )
            command = (
                shlex.quote(sys.executable)
                + " -c "
                + shlex.quote(code)
            )
            member = {"number": 101, "body": "body one"}

            with mock.patch.dict(os.environ, {"OUT": output_path}):
                result = candidate._exec_members(command, [member])

            self.assertEqual(0, result)
            with open(output_path, encoding="utf-8") as stream:
                self.assertEqual("two words", stream.read())

    def test_empty_command_returns_two(self):
        """Whitespace-only command is incomplete.

        Input: --exec command contains only spaces.
        Expected error: empty command.
        Expected exit: 2.
        Assertion: subprocess is never called.
        """
        with mock.patch.object(candidate.subprocess, "run") as run:
            result = candidate._exec_members("   ", [])
        self.assertEqual(2, result)
        run.assert_not_called()

    def test_exit_zero_is_success(self):
        """Member command returns zero.

        Input: one member; subprocess returncode=0.
        Expected error: none.
        Expected exit: 0.
        Assertion: aggregate exit code is zero.
        """
        with mock.patch.object(
            candidate.subprocess,
            "run",
            return_value=mock.Mock(returncode=0),
        ):
            result = candidate._exec_members(
                "python -c pass",
                [{"number": 101, "body": "body"}],
            )
        self.assertEqual(0, result)

    def test_exit_one_is_violation(self):
        """Member command returns one.

        Input: one member; subprocess returncode=1.
        Expected error: member violation.
        Expected exit: 1.
        Assertion: aggregate exit code is one.
        """
        with mock.patch.object(
            candidate.subprocess,
            "run",
            return_value=mock.Mock(returncode=1),
        ):
            result = candidate._exec_members(
                "python -c pass",
                [{"number": 101, "body": "body"}],
            )
        self.assertEqual(1, result)

    def test_other_exit_code_is_incomplete(self):
        """Member command returns an unexpected code.

        Input: one member; subprocess returncode=7.
        Expected error: incomplete execution.
        Expected exit: 2.
        Assertion: unexpected exit code is not normalized to success.
        """
        with mock.patch.object(
            candidate.subprocess,
            "run",
            return_value=mock.Mock(returncode=7),
        ):
            result = candidate._exec_members(
                "python -c pass",
                [{"number": 101, "body": "body"}],
            )
        self.assertEqual(2, result)

    def test_member_body_is_bound_per_invocation(self):
        """Every member receives its own PR_NUMBER and PR_BODY.

        Input: two distinct member numbers and bodies.
        Expected error: none.
        Expected exit: 0.
        Assertion: subprocess environments preserve each exact body.
        """
        calls = []

        def record(argv, env, check):
            calls.append((env["PR_NUMBER"], env["PR_BODY"]))
            return mock.Mock(returncode=0)

        members = [
            {"number": 101, "body": "body for one"},
            {"number": 102, "body": "body for two"},
        ]
        with mock.patch.object(
            candidate.subprocess,
            "run",
            side_effect=record,
        ):
            result = candidate._exec_members(
                "python -c pass",
                members,
            )

        self.assertEqual(0, result)
        self.assertEqual(
            [
                ("101", "body for one"),
                ("102", "body for two"),
            ],
            calls,
        )


if __name__ == "__main__":
    unittest.main()
