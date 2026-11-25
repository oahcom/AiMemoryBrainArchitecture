"""Automated acceptance and adversarial tests for the Session Evidence Gate."""

import contextlib
import hashlib
import io
import os
import re
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


TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".github",
    "PULL_REQUEST_TEMPLATE.md",
)

ISSUE_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    ".github",
    "ISSUE_TEMPLATE",
    "session-evidence.md",
)


def fill_pull_request_template(number, refs):
    """Fill the repository's own PR template, adding nothing to it.

    Every value replaces the text the template already leaves after its own
    label, and the per-Issue row replaces the template's placeholder row.
    """
    with open(TEMPLATE_PATH, encoding="utf-8") as handle:
        lines = handle.read().splitlines()

    values = {
        "Work Item ID": "AID-2026-001",
        "Related issue(s)": f"#{number}",
        "AI-assisted work": "YES",
        "Session evidence reference(s)": refs[0],
    }

    for index, line in enumerate(lines):
        match = re.match(r"- ([^:]+):", line)
        if match and match.group(1).strip() in values:
            label = match.group(1).strip()
            lines[index] = f"- {label}: {values[label]}"
            continue

        if line.strip().startswith("| #NNN |"):
            lines[index] = f"| #{number} | YES | {refs[0]} |"

    return "\n".join(lines) + "\n"


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

    def test_blob_content_wrapped_by_the_api_still_decodes(self):
        # The REST API returns base64 wrapped at 60 characters. The fixtures
        # did not, so a validator that rejected the newlines passed every test
        # and failed on the first real pull request. This test is the only one
        # that hands the validator the payload shape the API actually sends.
        world = make_valid_world()
        raw_api = world["api"]

        def wrapped(path):
            payload = raw_api(path)
            content = payload.get("content")
            if not content:
                return payload
            return {
                **payload,
                "content": "\n".join(
                    content[at:at + 60]
                    for at in range(0, len(content), 60)
                ) + "\n",
            }

        self.patch_validate("gh_api", wrapped)
        self.patch_validate("gh_tree", world["tree"])
        self.patch_validate("gh_blob_text", world["blob_text"])
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

    def test_multi_line_related_issues_are_all_parsed(self):
        body = f"""## Related issue(s)

{issue_url(101)}
{issue_url(102)}
"""
        self.assertEqual(
            validate.parse_related_issues(body, REPOSITORY),
            [101, 102],
        )

    def test_a_second_evidence_path_is_not_silently_dropped(self):
        # Every reference has to be validated one by one. While the field
        # value was its first line only, the second path never reached a
        # check, so a declared file that does not exist passed the gate.
        missing = "14-ai-development/work-items/AID-2026-099/does-not-exist.md"
        body = f"""## Work Item

AID-2026-001

## Related issue(s)

#101

## AI-assisted work

YES

## Session evidence reference(s)

{EVIDENCE_A}
{missing}

## Per-Issue AI session evidence

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| {issue_url(101)} | YES | {EVIDENCE_A} |
"""
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertEqual(result, 1, output)
        self.assertIn(missing, output)

    def test_multi_line_status_field_is_rejected(self):
        with self.assertRaises(validate.ValidationError):
            validate._parse_status(
                validate._extract_field(
                    "## AI-assisted work\n\nYES\nNO\n",
                    "AI-assisted work",
                ),
                "test",
            )

    def test_an_empty_field_does_not_absorb_the_next_bullet_field(self):
        # The template stacks its fields as consecutive bullets with no
        # heading between them. An empty field must stop at the next label,
        # or it would read an Issue URL out of a field the author filled in
        # for another purpose and link an Issue this slot never declared.
        body = "\n".join(
            [
                "- Related issue(s):",
                "- AI-assisted work: NO",
                f"- Related PR(s): {issue_url(101)}",
            ]
        )
        with self.assertRaises(validate.ValidationError):
            validate.parse_related_issues(body, REPOSITORY)

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
            # The verdict remains the first line; NOT_APPLICABLE carries no
            # additional boundary note.
            self.assertEqual(summary_file.read().splitlines()[0], expected)
        self.assertNotIn("skipped", output.lower())
        self.assertNotIn("neutral", output.lower())

    def test_entry_may_attribute_evidence_to_a_legacy_undeclared_issue(self):
        # A pre-policy Issue has no declaration by definition, so its row is
        # LEGACY_UNDECLARED. Naming it in issue_refs says which Issue this
        # session's work belongs to, not that AI was used on that Issue --
        # the specification keeps those two facts independent.
        body = f"""## Related issue(s)

#101

## AI-assisted work

YES

## Session evidence reference(s)

{EVIDENCE_A}

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| {issue_url(101)} | LEGACY_UNDECLARED | N/A |
"""
        world = make_valid_world(
            issue_created="2020-01-01T00:00:00Z",
            issue_body=ISSUE_BODY_UNDECLARED,
            pr_body=body,
        )
        self.install_world(world)
        self.assertEqual(run_validator(), 0)

    def test_pre_effective_undeclared_pr_is_not_applicable(self):
        # Issue #1026: with no declaration at all, the historical guard
        # used to be unreachable because check_01 ran first and raised.
        world = make_valid_world(
            issue_created="2020-01-01T00:00:00Z",
            issue_body=ISSUE_BODY_UNDECLARED,
            pr_body="Related issue(s): #101\n",
        )
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertEqual(result, 0)
        self.assertIn("AI-SESSION-EVIDENCE: NOT_APPLICABLE", output)

    def test_pre_effective_pr_with_post_effective_issue_requires_declaration(
        self,
    ):
        # One linked Issue postdates the effective time, so the exemption
        # does not apply and the missing declaration must still fail. This
        # is what stops the #1026 fix from becoming a blanket skip.
        entries = [make_entry(101, "a"), make_entry(102, "b")]
        world = make_valid_world(
            entries=entries,
            issue_created="2020-01-01T00:00:00Z",
            issue_body=ISSUE_BODY_UNDECLARED,
            pr_body="Related issue(s): #101, #102\n",
        )
        original_api = world["api"]

        def api(path):
            if path == f"/repos/{REPOSITORY}/issues/102":
                return {
                    "number": 102,
                    "html_url": issue_url(102),
                    "created_at": "2100-01-01T00:00:00Z",
                    "body": ISSUE_BODY_UNDECLARED,
                }
            return original_api(path)

        self.install_world(world)
        self.patch_validate("gh_api", api)
        result, output = self.capture_validator()
        self.assertEqual(result, 1)
        self.assertIn(
            "PR: missing AI-assisted work declaration",
            output,
        )

    def test_pre_effective_pr_volunteered_yes_with_missing_evidence_fails(
        self,
    ):
        # A pre-effective PR that volunteers a YES declaration is not
        # exempt: it must still prove the reference exists. Skipping the
        # body checks for every pre-effective PR would let this pass.
        # The Issue is historical and undeclared, so the guard is True and
        # an unconditional early exit would return 0 here.
        missing = (
            "14-ai-development/work-items/AID-2026-001/"
            "evidence/session-missing.md"
        )
        body = f"""## Work Item

AID-2026-001

## Related issue(s)

#101

## AI-assisted work

YES

## Session evidence reference(s)

{missing}

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| {issue_url(101)} | LEGACY_UNDECLARED | N/A |
"""
        world = make_valid_world(
            issue_created="2020-01-01T00:00:00Z",
            issue_body=ISSUE_BODY_UNDECLARED,
            pr_body=body,
        )
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertEqual(result, 1)
        self.assertIn(
            "path does not exist in PR Head Git tree",
            output,
        )

    def test_pre_effective_pr_volunteered_yes_with_valid_evidence_is_not_applicable(
        self,
    ):
        # The declared case must keep its old behaviour: the declaration is
        # still validated, then the historical verdict is returned. The
        # verdict string is pinned here; the sibling test above pins only
        # the exit code for the same world.
        body = f"""## Work Item

AID-2026-001

## Related issue(s)

#101

## AI-assisted work

YES

## Session evidence reference(s)

{EVIDENCE_A}

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| {issue_url(101)} | LEGACY_UNDECLARED | N/A |
"""
        world = make_valid_world(
            issue_created="2020-01-01T00:00:00Z",
            issue_body=ISSUE_BODY_UNDECLARED,
            pr_body=body,
        )
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertEqual(result, 0)
        self.assertIn("AI-SESSION-EVIDENCE: NOT_APPLICABLE", output)

    def test_entry_cannot_attribute_evidence_to_an_issue_that_declares_no(
        self,
    ):
        body = f"""## Related issue(s)

#101

## AI-assisted work

YES

## Session evidence reference(s)

{EVIDENCE_A}

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| {issue_url(101)} | NO | N/A |
"""
        world = make_valid_world(
            pr_body=body,
            issue_body=ISSUE_BODY_NO,
        )
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("Issue #101", output)
        self.assertIn("maps to NO", output)
        self.assertIn("declares YES", output)


    def test_post_policy_missing_declaration_is_missing_and_failed(self):
        world = make_valid_world(issue_body=ISSUE_BODY_UNDECLARED)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("MISSING:", output)
        self.assertIn("Issue #101", output)

    def test_yes_requires_refs(self):
        # The PR declaration is the only defect: with this guard removed
        # the validator reports PRESENT, so no other clause can satisfy
        # this test.
        body = make_pr_body(
            status="YES",
            refs=[],
            issue_status="YES",
            issue_refs=[EVIDENCE_A],
        )
        self.make_valid_world(pr_body=body)
        result, output = self.capture_validator()
        self.assertEqual(result, 1)
        self.assertIn("PR: YES requires evidence references", output)

    def test_missing_pr_declaration_is_reported(self):
        body = make_pr_body().replace(
            "## AI-assisted work\n\nYES\n\n", ""
        )
        self.assertNotIn("## AI-assisted work", body)
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertEqual(result, 1)
        self.assertIn(
            "PR: missing AI-assisted work declaration",
            output,
        )

    def test_invalid_pr_declaration_value_is_reported(self):
        world = make_valid_world(
            pr_body=make_pr_body(status="MAYBE"),
        )
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertEqual(result, 1)
        self.assertIn("PR: AI-assisted work must be YES or NO", output)

    def test_no_requires_na(self):
        # This world also violates the Issue-mapping rule, so a bare
        # nonzero-exit assertion stayed green when the PR-scope guard was
        # deleted. Pin the message to the guard under test.
        body = make_pr_body(
            status="NO", refs=[EVIDENCE_A],
            issue_status="NO", issue_refs=[]
        )
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertEqual(result, 1)
        self.assertIn("PR: NO requires N/A", output)

    def test_pr_mapping_cannot_rewrite_issue_declaration(self):
        # The Issue declares NO/N/A; the PR table claims YES with evidence.
        # Without this rule a PR body can overwrite its own Issue's
        # declaration and the gate still reports PRESENT.
        body = make_pr_body(
            status="YES",
            refs=[EVIDENCE_A],
            issue_status="YES",
            issue_refs=[EVIDENCE_A],
        )
        world = make_valid_world(
            pr_body=body,
            issue_body=ISSUE_BODY_NO,
        )
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn(
            "PR mapping status differs from Issue declaration",
            output,
        )

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

    def test_evidence_document_requires_session_role_section(self):
        # Everything else is legal; only the role heading is missing. The
        # gate exists to prove a session role was recorded, so this guard
        # must fail closed on its own.
        world = make_valid_world()
        _install_evidence_text(
            world,
            """# Actual AI input

The actual prompt supplied to the AI:
Review the implementation requirements and produce the requested work.

# AI-visible output

The actual output returned by the AI:
The implementation was completed and the validation results were reported.
""",
        )
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("missing Session role / use case", output)

    def test_case_mismatched_path_is_rejected_with_every_other_rule_satisfied(self):
        # Manifest, Issue declaration and both PR scopes all name the same
        # wrong-case path; the tree holds only the lowercase one. A
        # lowercase fallback in lookup would silently accept it.
        wrong = EVIDENCE_A.replace("/evidence/", "/Evidence/")
        self.assertNotEqual(wrong, EVIDENCE_A)
        entry = make_entry(101)
        entry["session_evidence_ref"] = wrong
        issue_body = f"""## AI-assisted work

YES

## Session evidence reference(s)

{wrong}
"""
        world = make_valid_world(entries=[entry], issue_body=issue_body)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn(wrong, output)

    def test_evidence_state_semantics(self):
        cases = [
            ("NOT_AVAILABLE", "", False),
            ("NOT_RECORDED", "", False),
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

    def test_each_evidence_state_requires_a_named_explanation(self):
        # The three states are three different claims -- the platform does
        # not provide the content, the author did not record it, or the copy
        # was redacted -- and silence is not one of them. A bare state word
        # must fail, and the failure must name the state it rejected.
        for state in ("NOT_AVAILABLE", "NOT_RECORDED", "REDACTED"):
            with self.subTest(state=state, case="explained"):
                text = (
                    "# Actual AI input\n"
                    f"{state}\n"
                    "Reason: not obtainable for this session.\n"
                )
                validate._parse_evidence_region(
                    text, "Actual AI input", "test.md"
                )

            with self.subTest(state=state, case="bare"):
                text = f"# Actual AI input\n{state}\n"
                with self.assertRaises(validate.ValidationError) as caught:
                    validate._parse_evidence_region(
                        text, "Actual AI input", "test.md"
                    )
                self.assertIn(state, str(caught.exception))

    def test_rejects_duplicate_related_issues(self):
        with self.assertRaises(validate.ValidationError):
            validate.parse_related_issues(
                "Related issue(s): #101, #101",
                REPOSITORY,
            )

    def test_accepts_the_owning_issue_url_spelling(self):
        # The template used to ask for "Owning Issue URL"; the gate read only
        # "Owning Issue". Both spellings name the same field.
        body = f"Owning Issue URL: {issue_url(101)}"
        self.assertEqual(
            validate._extract_field(body, "Related issue(s)"),
            issue_url(101),
        )
        self.assertEqual(
            validate.parse_related_issues(body, REPOSITORY),
            [101],
        )

    def test_missing_issue_field_names_the_field_it_wanted(self):
        with self.assertRaises(validate.ValidationError) as raised:
            validate.parse_related_issues("Work Item ID: AID-2026-001", REPOSITORY)
        self.assertEqual(
            str(raised.exception),
            "PR description: missing Related issue(s)",
        )

    def test_accepts_markdown_list_markers_on_every_read_field(self):
        # Every field in .github/PULL_REQUEST_TEMPLATE.md is a "- Label: value"
        # bullet; the list marker is presentation, not part of the label.
        body = "\n".join(
            [
                "- Related issue(s): #101",
                "- AI-assisted work: NO",
                "- Session evidence reference(s): N/A",
            ]
        )
        self.assertEqual(validate._extract_field(body, "AI-assisted work"), "NO")
        self.assertEqual(
            validate._extract_field(body, "Session evidence reference(s)"),
            "N/A",
        )
        self.assertEqual(validate.parse_related_issues(body, REPOSITORY), [101])

    def test_repository_pull_request_template_is_accepted(self):
        # The whole point: a PR body filled in exactly as the repository's own
        # template asks must pass. If the template and the gate ever drift
        # apart again, this test names the field that drifted.
        body = fill_pull_request_template(101, [EVIDENCE_A])
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertEqual(result, 0, output)
        self.assertIn("AI-SESSION-EVIDENCE: PRESENT", output)

    def test_repository_issue_template_carries_a_parseable_declaration(self):
        # The Issue side needs a distribution channel too: without one, every
        # post-policy Issue linked by a PR fails check_03 for lack of a field
        # nobody asked it to carry.
        with open(ISSUE_TEMPLATE_PATH, encoding="utf-8") as handle:
            text = handle.read()

        body = text.replace("YES | NO", "YES", 1).replace(
            "`path/to/session/evidence.md` — or `N/A` when the line above is `NO`",
            f"`{EVIDENCE_A}`",
            1,
        )

        self.assertEqual(
            validate._parse_issue_declaration(body, 101),
            ("YES", [EVIDENCE_A]),
        )
        self.assertIn("not a hard gate", body)

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

    def test_rejects_duplicate_evidence_reference_within_one_scope(self):
        # The same path twice in one Issue row is a duplicate in that
        # declaration scope. _parse_reference_lines is the only reachable
        # implementation of the rule: check_06 and check_07 are handed lists
        # this parser has already deduplicated, so they never see the pair.
        # This test fails if the parser's duplicate check is removed.
        body = make_pr_body(
            refs=[EVIDENCE_A],
            issue_refs=[EVIDENCE_A, EVIDENCE_A],
        )
        world = make_valid_world(pr_body=body)
        self.install_world(world)
        result, output = self.capture_validator()
        self.assertNotEqual(result, 0)
        self.assertIn("duplicate evidence references", output)

    def test_check_06_rejects_duplicates_if_handed_them(self):
        # In production _parse_reference_lines rejects a duplicate pair before
        # check_06 runs, so no black-box input reaches this branch. It is kept
        # as the per-scope check and is called directly here; deleting the
        # branch makes this test fail, which is the point.
        ctx = make_context(make_valid_world())
        with self.assertRaises(validate.ValidationError):
            validate.check_06_all_references_individually(
                ctx,
                [EVIDENCE_A, EVIDENCE_A],
            )

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
                summary_file.read().splitlines()[0],
                "AI-SESSION-EVIDENCE: PRESENT",
            )

    def test_job_summary_states_the_structure_only_boundary(self):
        self.make_valid_world()
        summary = os.path.join(self.temporary_directory(), "summary.md")
        with mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": summary}):
            self.assertEqual(run_validator(), 0)
        with open(summary, encoding="utf-8") as summary_file:
            lines = summary_file.read().splitlines()
        self.assertEqual(lines[0], "AI-SESSION-EVIDENCE: PRESENT")
        self.assertIn("bytes are unchanged", lines[1])
        self.assertFalse(
            any(
                line.startswith("AI-SESSION-EVIDENCE: ")
                for line in lines[1:]
            ),
            "only the first line may look like a verdict",
        )

    def test_present_summary_carries_the_structure_only_boundary(self):
        # The note is the only place a reviewer learns that PRESENT means "the
        # declared files exist and their bytes are unchanged" -- without it the
        # verdict reads as an endorsement of the evidence itself. Only the note
        # says so, and nothing but this test pins the sentence, so it could be
        # deleted with the suite staying green.
        self.make_valid_world()
        summary = os.path.join(self.temporary_directory(), "summary.md")
        with mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": summary}):
            self.assertEqual(run_validator(), 0)
        with open(summary, encoding="utf-8") as summary_file:
            lines = summary_file.read().splitlines()

        self.assertTrue(
            lines[0].startswith("AI-SESSION-EVIDENCE: PRESENT"),
            "the verdict stays the first line the workflow greps for",
        )
        self.assertIn("does not prove", lines[1])
        self.assertIn("authentic", lines[1])
        self.assertEqual(
            [
                line
                for line in lines
                if line.startswith("AI-SESSION-EVIDENCE:")
            ],
            [lines[0]],
            "exactly one line may look like a verdict",
        )
        self.assertNotEqual(lines[0], lines[1])

    def test_failure_summary_has_missing_verdict(self):
        world = make_valid_world(pr_body="incomplete")
        self.install_world(world)
        summary = os.path.join(self.temporary_directory(), "summary.md")
        with mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": summary}):
            self.assertNotEqual(run_validator(), 0)
        with open(summary, encoding="utf-8") as summary_file:
            self.assertEqual(
                summary_file.read().splitlines()[0],
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
        self.assertIn("maps to NO", output)

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
        self.assertIn("maps to NO", output)

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
