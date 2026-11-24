"""Automated acceptance and adversarial tests for the Session Evidence Gate."""

import contextlib
import hashlib
import io
import os
import tempfile
import unittest
from unittest import mock

from scripts.governance.session_evidence import validate
from tests.session_evidence import support

from tests.session_evidence.support import (
    EFFECTIVE_AT,
    EVIDENCE_A,
    EVIDENCE_B,
    EVIDENCE_TEXT_A,
    HEAD_SHA,
    ISSUE_BODY_NO,
    ISSUE_BODY_UNDECLARED,
    ISSUE_BODY_YES,
    MANIFEST,
    PROMPT_A,
    PROMPT_B,
    PROMPT_BYTES_A,
    PROMPT_BYTES_B,
    REPOSITORY,
    issue_url,
    make_blob,
    make_entry,
    make_manifest,
    make_pr_body,
    make_valid_world,
)


def run_validator():
    return validate.main([])


def assert_missing(test_case, output):
    test_case.assertTrue(
        output.startswith("MISSING:") or "MISSING:" in output
    )


def make_context(world):
    pr = world["pr"]
    issue = world["issue"]
    tree = world["git_tree"]
    return validate.ValidationContext(
        repo=REPOSITORY,
        pr_number=101,
        pr=pr,
        body=pr["body"],
        head_sha=HEAD_SHA,
        tree=tree,
        tree_by_path=validate._tree_index(tree),
        effective_at=validate.parse_utc_timestamp(EFFECTIVE_AT),
        issues={
            issue["number"]: validate.IssueRecord(
                number=issue["number"],
                url=issue["html_url"],
                created_at=validate._parse_api_timestamp(
                    issue["created_at"], f"Issue #{issue['number']}"
                ),
                body=issue["body"],
                is_historical=(
                    validate._parse_api_timestamp(
                        issue["created_at"], f"Issue #{issue['number']}"
                    )
                    < validate.parse_utc_timestamp(EFFECTIVE_AT)
                ),
            )
        },
    )


def _install_text(world, path, text):
    blob = make_blob(path, text)
    world["git_tree"] = [
        item for item in world["git_tree"] if item["path"] != path
    ] + [
        {key: value for key, value in blob.items() if key != "_raw"}
    ]
    world["raw_by_sha"][blob["sha"]] = blob["_raw"]
    previous = world["blob_text"]
    world["blob_text"] = lambda repo, sha, p: (
        text if p == path else previous(repo, sha, p)
    )


def _install_manifest_text(world, manifest_text):
    _install_text(world, MANIFEST, manifest_text)


def _install_evidence_text(world, evidence_text):
    _install_text(world, EVIDENCE_A, evidence_text)


def _legacy_manifest_text():
    return f"""implementing_ai_session: "session-a"
executed_prompt_snapshot_file: "{PROMPT_A}"
executed_prompt_sha256: "{hashlib.sha256(PROMPT_BYTES_A).hexdigest()}"
executed_prompt_bytes: {len(PROMPT_BYTES_A)}
executed_prompt_provenance: "VERIFIED"
session_reference_status: "RECORDED"
session_evidence_ref: "{EVIDENCE_A}"
"""


class SessionEvidenceValidatorTests(unittest.TestCase):
    def setUp(self):
        self.environment = mock.patch.dict(
            os.environ,
            {
                "AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC": EFFECTIVE_AT,
                "GITHUB_TOKEN": "offline-test-token",
                "GITHUB_REPOSITORY": REPOSITORY,
                "PR_NUMBER": "101",
            },
            clear=False,
        )
        self.environment.start()
        self.addCleanup(self.environment.stop)
        os.environ.pop("GITHUB_STEP_SUMMARY", None)

    def patch_validate(self, name, value):
        patcher = mock.patch.object(validate, name, value)
        patcher.start()
        self.addCleanup(patcher.stop)

    def install_world(self, world):
        self.patch_validate("gh_api", world["api"])
        self.patch_validate("gh_tree", world["tree"])
        self.patch_validate("gh_blob_text", world["blob_text"])
        return world

    def make_valid_world(self, **kwargs):
        world = make_valid_world(**kwargs)
        self.install_world(world)
        return world

    def capture_validator(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = run_validator()
        return result, output.getvalue()

    def temporary_directory(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return directory.name

    def test_valid_single_issue_single_session(self):
        self.make_valid_world()
        self.assertEqual(run_validator(), 0)

    def test_multiple_sessions_same_issue(self):
        entries = [make_entry(101, "a"), make_entry(101, "b")]
        refs = [EVIDENCE_A, EVIDENCE_B]
        body = make_pr_body(refs=refs, issue_refs=refs)
        world = make_valid_world(entries=entries, pr_body=body)
        self.install_world(world)
        self.assertEqual(run_validator(), 0)

    def test_multiple_issues_and_multiple_sessions(self):
        entries = [make_entry(101, "a"), make_entry(102, "b")]
        body = f"""## Related issue(s)

#101, #102

## AI-assisted work

YES

## Session evidence reference(s)

{EVIDENCE_A}
{EVIDENCE_B}

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| {issue_url(101)} | YES | {EVIDENCE_A} |
| {issue_url(102)} | YES | {EVIDENCE_B} |
"""
        world = make_valid_world(entries=entries, pr_body=body)
        original_api = world["api"]

        def api(path):
            if path == f"/repos/{REPOSITORY}/issues/102":
                return {
                    "number": 102,
                    "html_url": issue_url(102),
                    "created_at": "2031-01-02T00:00:00Z",
                    "body": f"""AI-assisted work: YES

Session evidence reference(s):
{EVIDENCE_B}
""",
                }
            return original_api(path)

        self.install_world(world)
        self.patch_validate("gh_api", api)
        self.assertEqual(run_validator(), 0)

    def test_rejects_noncanonical_paths(self):
        # Retain the original traversal and malformed-path coverage.
        paths = [
            "../escape.md",
            "14-ai-development/../escape.md",
            "14-ai-development//evidence.md",
            "14-ai-development/./evidence.md",
            "14-ai-development//work-items/a.md",
            "javascript:alert(1)",
        ]
        for path in paths:
            with self.subTest(path=path):
                with self.assertRaises(validate.ValidationError):
                    validate.validate_canonical_evidence_path(
                        path, "test path"
                    )

        # Assert the specific guard responsible for each of these cases.
        cases = [
            ("/absolute/evidence.md", "absolute path is forbidden"),
            ("//absolute/evidence.md", "absolute path is forbidden"),
            (
                r"14-ai-development\work-items\evidence.md",
                "backslash is forbidden",
            ),
            (
                "https://example.com/evidence.md",
                "URL scheme is forbidden",
            ),
            ("%2e%2e/escape.md", "percent encoding is forbidden"),
            ("  leading-space.md", "surrounding whitespace"),
        ]
        for path, reason in cases:
            with self.subTest(path=path, expected_reason=reason):
                with self.assertRaises(validate.ValidationError) as caught:
                    validate.validate_canonical_evidence_path(
                        path, "test path"
                    )
                self.assertIn(reason, str(caught.exception))

    def test_rejects_case_mismatched_path(self):
        world = make_valid_world()
        body = make_pr_body(
            refs=[
                "14-ai-development/work-items/AID-2026-001/"
                "evidence/SESSION-A.md"
            ]
        )
        world["pr"]["body"] = body
        world["issue"]["body"] = ISSUE_BODY_YES
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_rejects_directory_symlink_and_submodule(self):
        for mode, kind, reason in (
            ("040000", "tree", "target is not a Git blob"),
            ("120000", "blob", "target is not a regular file"),
            ("160000", "commit", "target is not a Git blob"),
        ):
            with self.subTest(mode=mode, kind=kind):
                world = make_valid_world()
                item = next(
                    item for item in world["git_tree"]
                    if item["path"] == EVIDENCE_A
                )
                item["mode"] = mode
                item["type"] = kind
                self.install_world(world)
                result, output = self.capture_validator()
                self.assertNotEqual(result, 0)
                self.assertIn(reason, output)

    def test_rejects_empty_file(self):
        world = make_valid_world()
        item = next(
            item for item in world["git_tree"]
            if item["path"] == EVIDENCE_A
        )
        item["size"] = 0
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_rejects_nonexistent_issue(self):
        world = make_valid_world()
        original_api = world["api"]

        def api(path):
            if path == f"/repos/{REPOSITORY}/issues/101":
                raise validate.ValidationError("HTTP 404 Not Found")
            return original_api(path)

        self.install_world(world)
        self.patch_validate("gh_api", api)
        self.assertNotEqual(run_validator(), 0)

    def test_rejects_missing_pr_fields(self):
        world = make_valid_world(pr_body="Related issue(s): #101")
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_rejects_missing_post_policy_issue_declaration(self):
        world = make_valid_world(issue_body=ISSUE_BODY_UNDECLARED)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("MISSING:", output)
        self.assertIn("Issue #101", output)

    def test_historical_issue_outputs_not_applicable_and_success(self):
        world = make_valid_world(
            issue_created="2020-01-01T00:00:00Z",
            issue_body=ISSUE_BODY_UNDECLARED,
            pr_body="""## Related issue(s)

#101

## AI-assisted work

NO

## Session evidence reference(s)

N/A

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| https://github.com/oahcom/AiMemoryBrainArchitecture/issues/101 | LEGACY_UNDECLARED | N/A |
""",
        )
        self.install_world(world)
        summary = os.path.join(self.temporary_directory(), "summary.md")
        with mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": summary}):
            result, output = self.capture_validator()
        expected = (
            f"AI-SESSION-EVIDENCE: NOT_APPLICABLE "
            f"(linked issue #101 predates {EFFECTIVE_AT})"
        )
        self.assertEqual(result, 0)
        self.assertIn(expected, output)
        with open(summary, encoding="utf-8") as summary_file:
            self.assertEqual(summary_file.read().strip(), expected)
        self.assertNotIn("skipped", output.lower())
        self.assertNotIn("neutral", output.lower())

    def test_post_policy_missing_declaration_is_missing_and_failed(self):
        world = make_valid_world(issue_body=ISSUE_BODY_UNDECLARED)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("MISSING:", output)
        self.assertIn("Issue #101", output)

    def test_yes_requires_refs(self):
        body = make_pr_body(status="YES", refs=[], issue_refs=[])
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_no_requires_na(self):
        body = make_pr_body(
            status="NO", refs=[EVIDENCE_A],
            issue_status="NO", issue_refs=[]
        )
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_issue_no_requires_na(self):
        body = make_pr_body(
            status="YES",
            refs=[EVIDENCE_A],
            issue_status="NO",
            issue_refs=[],
        )
        world = make_valid_world(
            pr_body=body,
            issue_body=ISSUE_BODY_NO,
        )
        _install_manifest_text(world, _legacy_manifest_text())
        world["pr"]["base"] = {"sha": "b" * 40}
        self.install_world(world)
        self.patch_validate(
            "gh_compare_paths",
            lambda repo, base_sha, head_sha: set(),
        )
        self.assertEqual(run_validator(), 0)

    def test_legacy_undeclared_is_only_for_historical_issue(self):
        body = make_pr_body(
            status="NO",
            refs=[],
            issue_status="LEGACY_UNDECLARED",
            issue_refs=[],
        )
        world = make_valid_world(
            issue_created="2020-01-01T00:00:00Z",
            issue_body=ISSUE_BODY_UNDECLARED,
            pr_body=body,
        )
        self.install_world(world)
        self.assertEqual(run_validator(), 0)

    def test_rejects_legacy_undeclared_for_post_policy_issue(self):
        body = make_pr_body(
            status="NO",
            refs=[],
            issue_status="LEGACY_UNDECLARED",
            issue_refs=[],
        )
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_single_value_fields_reject_joined_values(self):
        values = [
            "session-a,session-b",
            "session-a;session-b",
            "session-a+session-b",
            "session-a session-b",
            "session-a\nsession-b",
        ]
        for value in values:
            with self.subTest(value=value):
                self.assertTrue(validate._contains_joined_values(value))

    def test_single_value_fields_accept_single_values(self):
        values = [
            "session-a",
            "14-ai-development/evidence/prompt.md",
            "a" * 64,
            "VERIFIED",
        ]
        for value in values:
            with self.subTest(value=value):
                self.assertFalse(validate._contains_joined_values(value))

    def test_joined_session_identifier_is_not_split(self):
        world = make_valid_world()
        manifest = world["manifest"].replace(
            'implementing_ai_session: "session-a"',
            'implementing_ai_session: "session-a,session-b"',
        )
        _install_manifest_text(world, manifest)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("joined multi-value", output)
        self.assertNotIn("session-a,session-b", output)

    def test_prompt_sha256_matches_original_bytes(self):
        self.make_valid_world()
        self.assertEqual(run_validator(), 0)

    def test_prompt_sha256_mismatch_fails(self):
        world = make_valid_world()
        manifest = world["manifest"].replace(
            hashlib.sha256(PROMPT_BYTES_A).hexdigest(),
            "0" * 64,
        )
        _install_manifest_text(world, manifest)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("executed_prompt_sha256 mismatch", output)

    def test_prompt_byte_count_mismatch_fails(self):
        world = make_valid_world()
        manifest = world["manifest"].replace(
            f"executed_prompt_bytes: {len(PROMPT_BYTES_A)}",
            "executed_prompt_bytes: 999",
        )
        _install_manifest_text(world, manifest)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("executed_prompt_bytes mismatch", output)

    def test_manifest_requires_all_seven_legacy_fields(self):
        manifest = """session_evidence:
  - role: IMPLEMENTER
    issue_refs:
      - "#101"
    implementing_ai_session: "session-a"
"""
        with self.assertRaises(validate.ValidationError):
            validate.parse_manifest_session_entries(manifest, MANIFEST)

    def test_manifest_rejects_simultaneous_legacy_and_entries(self):
        manifest = """implementing_ai_session: "legacy-session"
executed_prompt_snapshot_file: "prompt.md"
executed_prompt_sha256: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
executed_prompt_bytes: 1
executed_prompt_provenance: "VERIFIED"
session_reference_status: "RECORDED"
session_evidence_ref: "evidence.md"
session_evidence:
  - role: IMPLEMENTER
"""
        with self.assertRaises(validate.ValidationError):
            validate.parse_manifest_session_entries(manifest, MANIFEST)

    def test_manifest_rejects_invalid_provenance(self):
        world = make_valid_world()
        manifest = world["manifest"].replace(
            'executed_prompt_provenance: "VERIFIED"',
            'executed_prompt_provenance: "UNKNOWN"',
        )
        _install_manifest_text(world, manifest)
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_manifest_rejects_unlinked_issue_reference(self):
        world = make_valid_world()
        manifest = world["manifest"].replace(
            issue_url(101),
            issue_url(999),
        )
        _install_manifest_text(world, manifest)
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_evidence_requires_actual_input_and_output_sections(self):
        with self.assertRaises(validate.ValidationError):
            validate._parse_evidence_region(
                "# Summary\nOnly a retrospective summary.",
                "Actual AI input",
                "test.md",
            )
        with self.assertRaises(validate.ValidationError):
            validate._parse_evidence_region(
                "# Actual AI-visible output\n",
                "AI-visible output",
                "test.md",
            )

    def test_evidence_state_semantics(self):
        cases = [
            ("NOT_AVAILABLE", "", True),
            ("NOT_RECORDED", "", True),
            ("REDACTED", "Reason: credentials removed.", True),
            ("REDACTED", "", False),
        ]
        for state, explanation, valid in cases:
            with self.subTest(state=state, explanation=explanation):
                text = f"# Actual AI input\n{state}\n{explanation}\n"
                if valid:
                    validate._parse_evidence_region(
                        text, "Actual AI input", "test.md"
                    )
                else:
                    with self.assertRaises(validate.ValidationError):
                        validate._parse_evidence_region(
                            text, "Actual AI input", "test.md"
                        )

    def test_rejects_duplicate_related_issues(self):
        with self.assertRaises(validate.ValidationError):
            validate.parse_related_issues(
                "Related issue(s): #101, #101",
                REPOSITORY,
            )

    def test_rejects_external_issue_url(self):
        with self.assertRaises(validate.ValidationError):
            validate._normalise_issue_reference(
                "https://example.com/issues/101",
                REPOSITORY,
            )

    def test_rejects_wrong_repository_issue_url(self):
        with self.assertRaises(validate.ValidationError):
            validate._normalise_issue_reference(
                "https://github.com/another/repository/issues/101",
                REPOSITORY,
            )

    def test_effective_time_must_be_utc(self):
        with self.assertRaises(validate.ValidationError):
            validate.parse_utc_timestamp("2099-01-01T00:00:00+08:00")

    def test_effective_time_must_be_valid(self):
        with self.assertRaises(validate.ValidationError):
            validate.parse_utc_timestamp("2099-99-99T00:00:00Z")

    def test_issue_and_pr_declarations_are_independent(self):
        body = make_pr_body(
            status="NO",
            refs=[],
            issue_status="YES",
            issue_refs=[EVIDENCE_A],
        )
        world = make_valid_world(
            pr_body=body,
            issue_body=ISSUE_BODY_YES,
        )
        self.install_world(world)
        self.assertEqual(run_validator(), 0)

    def test_issue_yes_without_matching_manifest_mapping_fails(self):
        body = make_pr_body(
            status="YES",
            refs=[EVIDENCE_A],
            issue_status="YES",
            issue_refs=[EVIDENCE_A],
        )
        world = make_valid_world(pr_body=body)
        manifest = world["manifest"].replace(
            issue_url(101),
            issue_url(999),
        )
        _install_manifest_text(world, manifest)
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_pr_evidence_path_must_be_in_head_tree(self):
        path = (
            "14-ai-development/work-items/AID-2026-001/"
            "evidence/not-in-tree.md"
        )
        body = make_pr_body(refs=[path], issue_refs=[path])
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        self.assertNotEqual(run_validator(), 0)

    def test_declared_path_missing_from_head_tree(self):
        world = make_valid_world()
        absent_path = (
            "14-ai-development/work-items/AID-2026-001/"
            "evidence/absent.md"
        )
        world["pr"]["body"] = make_pr_body(refs=[absent_path])
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn(
            "does not exist in PR Head Git tree",
            output,
        )

    def test_manifest_and_evidence_are_read_from_head_sha(self):
        world = make_valid_world()
        calls = []
        original_tree = world["tree"]

        def tree(repo, sha):
            calls.append((repo, sha))
            return original_tree(repo, sha)

        world["tree"] = tree
        self.install_world(world)
        self.assertEqual(run_validator(), 0)
        self.assertEqual(calls, [(REPOSITORY, HEAD_SHA)])

    def test_pr_issue_table_must_have_one_row_per_related_issue(self):
        body = """| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| https://github.com/oahcom/AiMemoryBrainArchitecture/issues/101 | YES | evidence.md |
"""
        parsed = validate.parse_pr_issue_table(body, REPOSITORY)
        self.assertEqual(parsed[101][0], "YES")

    def test_missing_issue_table_is_rejected(self):
        with self.assertRaises(validate.ValidationError):
            validate.parse_pr_issue_table("No mapping table", REPOSITORY)

    def test_no_evidence_refs_cannot_be_implicitly_assigned_to_no_issue(self):
        body = """## Related issue(s)

#101

## AI-assisted work

YES

## Session evidence reference(s)

evidence.md

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| https://github.com/oahcom/AiMemoryBrainArchitecture/issues/101 | NO | N/A |
"""
        parsed = validate.parse_pr_issue_table(body, REPOSITORY)
        self.assertEqual(parsed[101], ("NO", []))

    def test_tree_index_is_case_sensitive(self):
        tree = [
            {
                "path": "Evidence/Session.md",
                "mode": "100644",
                "type": "blob",
                "sha": "a" * 40,
                "size": 10,
            }
        ]
        index = validate._tree_index(tree)
        self.assertIn("Evidence/Session.md", index)
        self.assertNotIn("evidence/session.md", index)

    def test_tree_index_rejects_duplicate_paths(self):
        item = {
            "path": "evidence.md",
            "mode": "100644",
            "type": "blob",
            "sha": "a" * 40,
            "size": 10,
        }
        with self.assertRaises(validate.ValidationError):
            validate._tree_index([item, dict(item)])

    def test_missing_api_token_fails(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("GITHUB_TOKEN", None)
            with self.assertRaises(validate.ValidationError):
                validate._request_json("/repos/example/repo/issues/1")

    def test_job_summary_has_present_verdict(self):
        self.make_valid_world()
        summary = os.path.join(self.temporary_directory(), "summary.md")
        with mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": summary}):
            self.assertEqual(run_validator(), 0)
        with open(summary, encoding="utf-8") as summary_file:
            self.assertEqual(
                summary_file.read().strip(),
                "AI-SESSION-EVIDENCE: PRESENT",
            )

    def test_failure_summary_has_missing_verdict(self):
        world = make_valid_world(pr_body="incomplete")
        self.install_world(world)
        summary = os.path.join(self.temporary_directory(), "summary.md")
        with mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": summary}):
            self.assertNotEqual(run_validator(), 0)
        with open(summary, encoding="utf-8") as summary_file:
            self.assertEqual(
                summary_file.read().strip(),
                "AI-SESSION-EVIDENCE: MISSING",
            )

    def test_main_accepts_argv(self):
        self.make_valid_world()
        self.assertEqual(validate.main([]), 0)

    # -----------------------------------------------------------------------
    # Direct tests of GitHub API response handling
    # -----------------------------------------------------------------------

    def test_gh_compare_paths_rejects_truncated_response(self):
        self.patch_validate(
            "gh_api",
            lambda path: {
                "truncated": True,
                "files": [{"filename": "a.md"}],
            },
        )
        with self.assertRaises(validate.ValidationError) as caught:
            validate.gh_compare_paths(
                REPOSITORY, "b" * 40, "a" * 40
            )
        self.assertIn("truncated", str(caught.exception))

    def test_gh_compare_paths_rejects_file_limit(self):
        files = [
            {"filename": f"f{i}.md"}
            for i in range(300)
        ]
        self.patch_validate(
            "gh_api",
            lambda path: {"files": files},
        )
        with self.assertRaises(validate.ValidationError) as caught:
            validate.gh_compare_paths(
                REPOSITORY, "b" * 40, "a" * 40
            )
        self.assertIn("300", str(caught.exception))

    def test_gh_compare_paths_returns_changed_paths(self):
        self.patch_validate(
            "gh_api",
            lambda path: {
                "files": [
                    {"filename": "14-ai-development/x.md"},
                    {"filename": "scripts/y.py"},
                ]
            },
        )
        self.assertEqual(
            validate.gh_compare_paths(
                REPOSITORY, "b" * 40, "a" * 40
            ),
            {
                "14-ai-development/x.md",
                "scripts/y.py",
            },
        )

    def test_gh_tree_rejects_truncated_tree(self):
        self.patch_validate(
            "gh_api",
            lambda path: {
                "truncated": True,
                "tree": [],
            },
        )
        with self.assertRaises(validate.ValidationError) as caught:
            validate.gh_tree(REPOSITORY, "a" * 40)
        self.assertIn("truncated", str(caught.exception))

    # -----------------------------------------------------------------------
    # OD-A3-r5 regression tests
    # -----------------------------------------------------------------------

    def test_changed_manifest_rejects_issue_refs_to_no_issue(self):
        body = make_pr_body(
            status="YES",
            refs=[EVIDENCE_A],
            issue_status="NO",
            issue_refs=[],
        )
        world = make_valid_world(
            pr_body=body,
            issue_body=ISSUE_BODY_NO,
        )
        self.install_world(world)
        self.patch_validate(
            "gh_compare_paths",
            lambda repo, base_sha, head_sha: {MANIFEST},
        )
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("MISSING:", output)
        self.assertIn("Issue #101", output)
        self.assertIn("YES", output)

    def test_unchanged_manifest_still_requires_issue_refs_mapping(self):
        body = make_pr_body(
            status="YES",
            refs=[EVIDENCE_A],
            issue_status="NO",
            issue_refs=[],
        )
        world = make_valid_world(
            pr_body=body,
            issue_body=ISSUE_BODY_NO,
        )
        self.install_world(world)
        self.patch_validate(
            "gh_compare_paths",
            lambda repo, base_sha, head_sha: set(),
        )
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("MISSING:", output)
        self.assertIn("Issue #101", output)
        self.assertIn("YES", output)

    def test_changed_legacy_manifest_must_migrate(self):
        world = make_valid_world()
        _install_manifest_text(world, _legacy_manifest_text())
        self.install_world(world)
        self.patch_validate(
            "gh_compare_paths",
            lambda repo, base_sha, head_sha: {MANIFEST},
        )
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("MISSING:", output)
        self.assertIn(
            f"{MANIFEST}: updated manifest must use the canonical "
            "session_evidence entries",
            output,
        )

    def test_unchanged_legacy_manifest_is_exempt_from_issue_mapping(self):
        world = make_valid_world()
        _install_manifest_text(world, _legacy_manifest_text())
        _install_evidence_text(world, EVIDENCE_TEXT_A)
        world["pr"]["base"] = {"sha": "b" * 40}
        self.install_world(world)
        self.patch_validate(
            "gh_compare_paths",
            lambda repo, base_sha, head_sha: set(),
        )
        self.assertEqual(run_validator(), 0)

    def test_truncated_compare_fails_closed(self):
        world = make_valid_world()
        world["pr"]["base"] = {"sha": "b" * 40}
        self.install_world(world)

        def truncated_compare(repo, base_sha, head_sha):
            raise validate.ValidationError(
                "unable to determine changed paths: "
                "GitHub compare result is truncated"
            )

        self.patch_validate("gh_compare_paths", truncated_compare)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("MISSING:", output)
        self.assertIn("unable to determine changed paths", output)


if __name__ == "__main__":
    unittest.main()
