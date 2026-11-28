#!/usr/bin/env python3
"""Tests for the repository hygiene and new-file admission gates."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


EMPTY_SCHEMA_REGISTRY = (
    'schema_registry_version: "1"\n'
    "excluded_records:\n"
)


CHECKER = (
    Path(__file__).resolve().parent
    / "ci"
    / "check_repository_hygiene.py"
)


def git(repo, *args):
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def work_item_names(files):
    """Work-item directory names a fixture carries, from its own file paths."""
    names = set()
    for path in files:
        if not path.startswith("14-ai-development/work-items/"):
            continue
        remainder = path[len("14-ai-development/work-items/"):]
        name, separator, _ = remainder.partition("/")
        if separator and name:
            names.add(name)
    return names


class RepositoryHygieneTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)

        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "Hygiene Test")
        git(self.repo, "config", "user.email", "hygiene@example.invalid")

    def tearDown(self):
        self.tempdir.cleanup()

    def commit(self, files, *, with_registry=True, with_index=True):
        files = dict(files)
        # The schema registry is a policy input the checker requires, so every
        # fixture tree carries one unless a test is specifically about its
        # absence. A test that wants a different registry passes its own value.
        if with_registry:
            files.setdefault(
                "14-ai-development/work-items/manifest-schema-registry.yaml",
                EMPTY_SCHEMA_REGISTRY,
            )
        # Index membership fails closed on either absent side (#1212), so a
        # fixture tree has to carry both sides the way the real tree does: at
        # least one work-item directory and an INDEX.md row for every directory
        # it contains. A case that is about either side passes its own content
        # and `setdefault` leaves it alone; a case about something else gets a
        # self-consistent registry instead of a red on an unrelated check.
        #
        # The placeholders live in the same commit as whatever the case adds,
        # and both fixture commits go through here, so they are never reported
        # as new paths by the admission check. `with_index=False` is for the
        # cases that are about the absent sides themselves.
        if with_index:
            files.setdefault(
                "14-ai-development/work-items/AID-2026-001/manifest.yaml",
                "work_item_id: AID-2026-001\n",
            )
            files.setdefault(
                "14-ai-development/work-items/INDEX.md",
                "".join(
                    f"| [{name}]({name}/manifest.yaml) |\n"
                    for name in sorted(work_item_names(files))
                ),
            )
        for name, content in files.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        git(self.repo, "add", "-f", "-A")
        git(self.repo, "commit", "-q", "-m", "test fixture")
        return git(self.repo, "rev-parse", "HEAD")

    def seed_base(self):
        return self.commit({
            "README.md": "Base repository content\n",
        })

    def run_checker(self, base, head):
        return subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--base",
                base,
                "--head",
                head,
            ],
            cwd=self.repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )

    def run_checker_args(self, *args):
        return subprocess.run(
            [sys.executable, str(CHECKER), *args],
            cwd=self.repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )

    def run_checker_unqualified(self):
        """Run the CLI exactly as a caller that forgot the range would."""
        return subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=self.repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )

    def assert_admission_passes(self, base, head):
        result = self.run_checker(base, head)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "Repository new-file admission passed:",
            result.stdout,
        )

    def assert_admission_fails(self, base, head, path, *, reason=None):
        result = self.run_checker(base, head)
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        expected = (
            "::error::new-file admission violation: "
            + (reason or f"no allowlist rule for '{path}'")
        )
        self.assertIn(expected, result.stderr)

    def test_new_work_item_registry_schema_assets_are_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "00-governance/schemas/work-item-registry.schema.json": (
                '{"type":"object"}\n'
            ),
            "00-governance/schemas/fixtures/valid.yaml": (
                "work_item_id: AID-2026-001\n"
            ),
            "00-governance/schemas/fixtures/valid.expected.json": (
                '{"valid":true}\n'
            ),
        })

        self.assert_admission_passes(base, head)

    def test_new_unapproved_work_item_registry_schema_suffix_is_rejected(self):
        base = self.seed_base()
        head = self.commit({
            "00-governance/schemas/fixtures/notes.txt": (
                "not an admitted schema asset\n"
            ),
            "00-governance/schemas/fixtures/nested/fixture.yaml": (
                "status: ACTIVE\n"
            ),
            "00-governance/schemas/nested/deeper/fixture.yaml": (
                "status: ACTIVE\n"
            ),
            "00-governance/schemas/fixtures/unexpected.json": (
                '{"unexpected":true}\n'
            ),
            "00-governance/schemas/other.schema.json": (
                '{"type":"object"}\n'
            ),
            "somewhere/else/fixture.yaml": (
                "status: ACTIVE\n"
            ),
        })

        for path in (
            "00-governance/schemas/fixtures/notes.txt",
            "00-governance/schemas/fixtures/nested/fixture.yaml",
            "00-governance/schemas/nested/deeper/fixture.yaml",
            "00-governance/schemas/fixtures/unexpected.json",
            "00-governance/schemas/other.schema.json",
            "somewhere/else/fixture.yaml",
        ):
            with self.subTest(path=path):
                self.assert_admission_fails(base, head, path)

    def test_new_allowed_source_file_passes(self):
        base = self.seed_base()
        head = self.commit({
            "scripts/new_gate.py": "print('hello')\n",
        })

        self.assert_admission_passes(base, head)

    def test_work_item_manifest_ac4_baseline_report_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/reports/work-item-manifest-ac4-baseline.json": (
                '{"baseline_tree":"0000000000000000000000000000000000000000"}\\n'
            ),
        })

        self.assert_admission_passes(base, head)

    def test_work_item_legacy_cohort_report_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/reports/work-item-legacy-cohort.json": (
                '{"schema_version":1,"baseline_commit":"'
                '0000000000000000000000000000000000000000",'
                '"cohort":[]}\\n'
            ),
        })

        self.assert_admission_passes(base, head)

    def test_work_item_legacy_disposition_ledger_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/reports/work-item-legacy-disposition.json": (
                '{"schema_version":1,"baseline_commit":"'
                '0000000000000000000000000000000000000000",'
                '"cohort":[],"generated_by":"test","entries":[]}\\n'
            ),
        })

        self.assert_admission_passes(base, head)

    def test_steward_adoption_baseline_report_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/reports/steward-adoption-baseline.json": (
                '{"pin":"0000000000000000000000000000000000000000",'
                '"governed":1,"classified":1,"present":0,"missing":["a.md"]}\\n'
            ),
        })

        self.assert_admission_passes(base, head)

    def test_prompt_commit_trace_baseline_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/work-items/AID-2026-291/baseline.json": (
                '{"schema_version":1,"commit":"0000000000000000000000000000000000000000"}\\n'
            ),
        })

        self.assert_admission_passes(base, head)

    def test_new_allowed_configuration_file_passes(self):
        base = self.seed_base()
        head = self.commit({
            ".github/workflows/new-check.yml": (
                "name: New check\n"
                "on: pull_request\n"
            ),
        })

        self.assert_admission_passes(base, head)

    def test_new_root_dm_txt_fails(self):
        base = self.seed_base()
        head = self.commit({
            "_dm.txt": "generated output\n",
        })

        result = self.run_checker(base, head)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "::error::repository hygiene violation: "
            "prohibited committed file '/_dm.txt'",
            result.stderr,
        )

    def test_gitignored_but_forced_committed_dm_txt_fails(self):
        base = self.seed_base()
        head = self.commit({
            ".gitignore": "/_dm.txt\n",
            "_dm.txt": "forced committed output\n",
        })

        result = self.run_checker(base, head)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "prohibited committed file '/_dm.txt'",
            result.stderr,
        )

    def test_new_gate_output_log_fails(self):
        base = self.seed_base()
        head = self.commit({
            "gate-output.log": "captured output\n",
        })

        self.assert_admission_fails(base, head, "gate-output.log")

    def test_new_unapproved_json_snapshot_fails(self):
        base = self.seed_base()
        head = self.commit({
            "tests/snapshots/result.json": '{"snapshot": true}\n',
        })

        self.assert_admission_fails(
            base, head, "tests/snapshots/result.json"
        )

    def test_modifying_existing_unapproved_extension_is_not_new_file(self):
        base = self.commit({
            "legacy-output.log": "old output\n",
        })

        path = self.repo / "legacy-output.log"
        path.write_text("updated existing file\n", encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "modify existing log")
        head = git(self.repo, "rev-parse", "HEAD")

        self.assert_admission_passes(base, head)

    def test_deleting_existing_file_is_not_new_file(self):
        base = self.commit({
            "docs/old-document.md": "old document\n",
        })

        (self.repo / "docs" / "old-document.md").unlink()
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "delete existing document")
        head = git(self.repo, "rev-parse", "HEAD")

        self.assert_admission_passes(base, head)

    def test_rename_to_unapproved_new_path_fails(self):
        base = self.commit({
            "old-name.py": "print('old')\n",
        })

        git(self.repo, "mv", "old-name.py", "renamed-output.log")
        git(self.repo, "commit", "-q", "-m", "rename to unapproved path")
        head = git(self.repo, "rev-parse", "HEAD")

        self.assert_admission_fails(base, head, "renamed-output.log")

    def test_original_head_denylist_still_rejects_existing_prohibited_path(self):
        self.commit({
            "_dm.txt": "prohibited\n",
        })

        result = self.run_checker_args("--head-tree-only")

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "prohibited committed file '/_dm.txt'",
            result.stderr,
        )

    # M11: denylist must remain active in admission mode.
    def test_admission_mode_still_checks_prohibited_head_paths(self):
        base = self.seed_base()
        head = self.commit({
            "_dm.txt": "prohibited\n",
            "allowed.py": "print('hello')\n",
        })

        result = self.run_checker(base, head)

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "::error::repository hygiene violation: "
            "prohibited committed file '/_dm.txt'",
            result.stderr,
        )

    # #1048: a root-level underscore file is scratch, not repository content.
    # `.md` is an admitted document suffix, so only the root rule can refuse
    # this, and the message has to name that rule -- "a new file was rejected"
    # cannot be told apart from a generic allowlist miss.
    def test_new_root_underscore_file_is_rejected(self):
        base = self.seed_base()
        head = self.commit({
            "_pr_body.md": "PR description draft\n",
        })

        result = self.run_checker(base, head)
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "::error::new-file admission violation: '_pr_body.md' is a "
            "root-level underscore/dot file; scratch files do not belong at "
            "the repository root",
            result.stderr,
        )
        self.assertNotIn("no allowlist rule", result.stderr)

    # #1048: the dot half of the rule. `.py` is an admitted source suffix, so
    # this too is refused only by the root shape.
    def test_new_root_dot_file_is_rejected(self):
        base = self.seed_base()
        head = self.commit({
            ".scratch.py": "print('scratch')\n",
        })

        result = self.run_checker(base, head)
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "::error::new-file admission violation: '.scratch.py' is a "
            "root-level underscore/dot file; scratch files do not belong at "
            "the repository root",
            result.stderr,
        )

    # #1048: the rule must not swallow legitimate root documents. A root
    # .md without the underscore prefix stays admitted.
    def test_new_root_markdown_file_is_admitted(self):
        base = self.commit({})
        head = self.commit({
            "README.md": "Repository entry point\n",
        })

        self.assert_admission_passes(base, head)

    # #1048: the rule is root-scoped. A leading underscore in a subdirectory
    # is ordinary, and asserting it here stops a later edit from widening the
    # rule to the whole tree without a red test.
    def test_new_underscore_file_in_subdirectory_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "scripts/_helper.py": "print('internal helper')\n",
        })

        self.assert_admission_passes(base, head)

    # #1048: /_dm.txt stays prohibited for its own reason. If the root rule
    # were the only thing rejecting it, deleting the denylist entry would look
    # harmless; this asserts the denylist still fires first.
    def test_root_dm_txt_is_rejected_by_the_denylist(self):
        base = self.seed_base()
        head = self.commit({
            "_dm.txt": "generated output\n",
        })

        result = self.run_checker(base, head)
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "::error::repository hygiene violation: "
            "prohibited committed file '/_dm.txt'",
            result.stderr,
        )
        self.assertNotIn("root-level underscore/dot file", result.stderr)

    # M01: committed tree contents, not ignore rules, determine admission.
    def test_gitignored_forced_committed_unapproved_file_fails_admission(self):
        base = self.seed_base()
        head = self.commit({
            ".gitignore": "*.bin\n",
            "artifacts/build-output.bin": "binary fixture\n",
        })

        self.assertIn(
            "artifacts/build-output.bin",
            git(self.repo, "ls-files"),
        )
        self.assert_admission_fails(
            base, head, "artifacts/build-output.bin"
        )

    # M08: the supplied --head, not the checkout's HEAD, is authoritative.
    def test_admission_uses_supplied_head_not_checkout_head(self):
        base = self.seed_base()
        head = self.commit({
            "artifacts/build-output.bin": "binary fixture\n",
        })

        git(self.repo, "checkout", "--detach", base)
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), base)

        self.assert_admission_fails(
            base, head, "artifacts/build-output.bin"
        )

    # M16: a Git failure must never be converted into a successful result.
    def test_unresolvable_base_returns_error_not_success(self):
        base = self.seed_base()
        head = self.commit({
            "allowed.py": "print('hello')\n",
        })

        missing = "0" * 40
        result = self.run_checker(missing, head)

        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "::error::repository hygiene cannot be determined:",
            result.stderr,
        )
        self.assertIn("rev-parse", result.stderr)

    # M18: the CLI requires both range arguments together.
    def test_base_without_head_is_rejected(self):
        self.seed_base()

        result = self.run_checker_args(
            "--base", "0" * 40
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "--base and --head must be supplied together",
            result.stderr,
        )

    def test_head_without_base_is_rejected(self):
        self.seed_base()

        result = self.run_checker_args(
            "--head", "0" * 40
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "--base and --head must be supplied together",
            result.stderr,
        )

    # #1212: an unqualified run must not be able to read as a pass. The old
    # behaviour skipped new-file admission silently and printed the same line a
    # full run prints, so a CI step that had lost its range stayed green while
    # the gate name claimed a check it had not performed.
    def test_unqualified_run_is_refused_not_reported_as_passed(self):
        self.seed_base()

        result = self.run_checker_unqualified()

        self.assertEqual(
            result.returncode,
            2,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "Repository new-file admission SKIPPED "
            "(new-file admission requires --base and --head).",
            result.stdout,
        )
        self.assertIn(
            "::error::repository hygiene cannot be determined: "
            "new-file admission requires --base and --head",
            result.stderr,
        )
        self.assertNotIn("Repository hygiene check passed", result.stdout)

    # #1212: the head-tree half is still a check, so it stays reachable -- but
    # only by name, and its summary has to say which half did not run. Without
    # this, "refuse the unqualified run" would be indistinguishable from
    # "delete the denylist, INDEX and manifest checks".
    def test_head_tree_only_reports_the_skipped_half(self):
        self.seed_base()

        result = self.run_checker_args("--head-tree-only")

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "New-file admission SKIPPED "
            "(new-file admission requires --base and --head).",
            result.stdout,
        )
        self.assertNotIn("Repository hygiene check passed", result.stdout)

    def test_head_tree_only_still_rejects_a_prohibited_path(self):
        self.commit({"_dm.txt": "prohibited\n"})

        result = self.run_checker_args("--head-tree-only")

        self.assertEqual(result.returncode, 1)
        self.assertIn("prohibited committed file '/_dm.txt'", result.stderr)

    def test_head_tree_only_cannot_be_combined_with_a_range(self):
        base = self.seed_base()
        head = self.commit({"allowed.py": "print('hello')\n"})

        result = self.run_checker_args(
            "--head-tree-only", "--base", base, "--head", head
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "--head-tree-only cannot be combined with --base and --head",
            result.stderr,
        )

    # M12: source suffix matching is intentionally case-insensitive.
    def test_uppercase_source_suffix_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "scripts/new_gate.PY": "print('hello')\n",
        })

        self.assert_admission_passes(base, head)

    # M13: configuration paths are intentionally exact and case-sensitive.
    def test_case_changed_configuration_filename_is_rejected(self):
        base = self.seed_base()
        head = self.commit({
            "PyProject.toml": "[tool.example]\n",
        })

        self.assert_admission_fails(
            base, head, "PyProject.toml"
        )

    # M14: workflow metadata is admitted only beneath root .github.
    def test_nested_github_workflow_directory_is_rejected(self):
        base = self.seed_base()
        head = self.commit({
            "nested/.github/workflows/check.yml": (
                "name: Nested workflow\n"
            ),
        })

        self.assert_admission_fails(
            base,
            head,
            "nested/.github/workflows/check.yml",
        )

    # M17: requirements files are admitted only at repository root.
    def test_nested_requirements_file_is_rejected(self):
        base = self.seed_base()
        head = self.commit({
            "nested/requirements-dev.txt": "example==1.0\n",
        })

        self.assert_admission_fails(
            base, head, "nested/requirements-dev.txt"
        )

    # M19: the prohibited path is exact, not a suffix-based denylist.
    def test_nested_dm_txt_does_not_match_root_denylist(self):
        self.commit({
            "nested/_dm.txt": "nested fixture\n",
        })

        result = self.run_checker_args("--head-tree-only")

        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    # M09: Git tree paths are NUL-delimited, not newline-delimited.
    @unittest.skipUnless(
        os.name == "posix",
        "requires newline-capable filenames",
    )
    def test_newline_in_allowed_filename_is_handled_as_one_path(self):
        base = self.seed_base()
        path = "scripts/strange\nname.py"
        head = self.commit({
            path: "print('hello')\n",
        })

        self.assert_admission_passes(base, head)

    # M20: a work-item manifest is the one YAML shape the registry needs.
    # Every other YAML shape stays rejected, so this rule cannot be widened
    # into a general .yaml admission by a later edit that nobody notices.
    def test_work_item_manifest_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/work-items/AID-2026-055/manifest.yaml":
                "work_item_id: AID-2026-055\n",
        })

        self.assert_admission_passes(base, head)

    # D7: the specifically approved provider-outcome conformance pin is
    # admitted. This does not widen the root-only requirements rule.
    def test_provider_outcome_requirements_file_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt":
                "jsonschema>=4.23,<5\n",
        })

        self.assert_admission_passes(base, head)

    # D17: both exact conformance harness package files are admitted.
    # This is deliberately not a general nested package.json rule.
    def test_conformance_package_files_are_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "08-bmcp-protocol/tests/conformance/package.json":
                '{"private": true}\n',
            "08-bmcp-protocol/tests/conformance/package-lock.json":
                '{"lockfileVersion": 3}\n',
        })

        self.assert_admission_passes(base, head)

    # D19: an immutable source snapshot directly inside an AID work item
    # is admitted. Nested snapshots are not covered by this rule.
    def test_aid_source_snapshot_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/work-items/AID-2026-003/"
            "t2-snapshot-fix-prompt.source.txt":
                "source snapshot\n",
        })

        self.assert_admission_passes(base, head)

    # D20: the reference-model .gitignore directly under an AID work item
    # is admitted. Other nested .gitignore paths remain outside the rule.
    def test_aid_reference_model_gitignore_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/work-items/AID-2026-001/"
            "reference-model/.gitignore":
                "__pycache__/\n*.pyc\n",
        })

        self.assert_admission_passes(base, head)

    # D7: requirements.txt in a sibling conformance suite is not the
    # specifically approved provider_outcome path.
    def test_recovery_cutoff_requirements_file_is_rejected(self):
        base = self.seed_base()
        path = (
            "08-bmcp-protocol/tests/conformance/"
            "recovery_cutoff/requirements.txt"
        )
        head = self.commit({
            path: "example==1.0\n",
        })

        self.assert_admission_fails(base, head, path)

    # D17: package.json under a child suite is not the conformance
    # directory's own package manifest.
    def test_nested_conformance_package_file_is_rejected(self):
        base = self.seed_base()
        path = (
            "08-bmcp-protocol/tests/conformance/"
            "provider_outcome/package.json"
        )
        head = self.commit({
            path: '{"private": true}\n',
        })

        self.assert_admission_fails(base, head, path)

    # D19: the source snapshot rule admits one filename directly under the
    # AID directory, not a snapshot nested one additional directory deep.
    def test_nested_aid_source_snapshot_is_rejected(self):
        base = self.seed_base()
        path = (
            "14-ai-development/work-items/AID-2026-003/"
            "nested/x.source.txt"
        )
        head = self.commit({
            path: "source snapshot\n",
        })

        self.assert_admission_fails(base, head, path)

    # D20: only reference-model/.gitignore at the exact approved depth is
    # admitted; a child directory's .gitignore is not.
    def test_nested_reference_model_gitignore_is_rejected(self):
        base = self.seed_base()
        path = (
            "14-ai-development/work-items/AID-2026-001/"
            "reference-model/sub/.gitignore"
        )
        head = self.commit({
            path: "*.pyc\n",
        })

        self.assert_admission_fails(base, head, path)

    # A1: protocol schemas live flat under schemas/. Positive.
    def test_protocol_schema_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "08-bmcp-protocol/schemas/1.2.18.schema.json":
                '{"$schema": "https://json-schema.org/draft/2020-12/schema"}\n',
        })

        self.assert_admission_passes(base, head)

    # A1: a schema one directory deeper is not the flat shape.
    def test_nested_protocol_schema_is_rejected(self):
        base = self.seed_base()
        path = "08-bmcp-protocol/schemas/sub/1.2.18.schema.json"
        head = self.commit({
            path: '{"$schema": "https://json-schema.org/draft/2020-12/schema"}\n',
        })

        self.assert_admission_fails(base, head, path)

    # A2: conformance vectors are admitted at any depth below the conformance
    # root. This covers both the zero-level family root and a nested fixture.
    def test_conformance_vectors_are_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "08-bmcp-protocol/tests/conformance/new-vector.json":
                '{"vector": "family-root"}\n',
            "08-bmcp-protocol/tests/conformance/provider_outcome/fixtures/"
            "new-vector.json":
                '{"vector": "nested"}\n',
        })

        self.assert_admission_passes(base, head)

    # A2: the negative lookahead is what keeps a child suite's package.json
    # out. Without it this path would be admitted as a plain vector.
    def test_a2_does_not_admit_child_suite_package_json(self):
        base = self.seed_base()
        path = (
            "08-bmcp-protocol/tests/conformance/"
            "provider_outcome/package.json"
        )
        head = self.commit({
            path: '{"private": true}\n',
        })

        self.assert_admission_fails(base, head, path)

    # A2: the same carve-out covers the -lock spelling, so a nested lockfile
    # is not smuggled in through the vector rule.
    def test_a2_does_not_admit_child_suite_package_lock(self):
        base = self.seed_base()
        path = (
            "08-bmcp-protocol/tests/conformance/"
            "recovery_cutoff/package-lock.json"
        )
        head = self.commit({
            path: '{"lockfileVersion": 3}\n',
        })

        self.assert_admission_fails(base, head, path)

    # A4: each crate owns one manifest directly under crates/<name>/.
    def test_crate_manifest_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "crates/new-crate/Cargo.toml":
                '[package]\nname = "new-crate"\nversion = "0.1.0"\n',
        })

        self.assert_admission_passes(base, head)

    # A4: workspace members are flat, so a nested manifest is not admitted.
    def test_nested_crate_manifest_is_rejected(self):
        base = self.seed_base()
        path = "crates/new-crate/sub/Cargo.toml"
        head = self.commit({
            path: '[package]\nname = "sub"\n',
        })

        self.assert_admission_fails(base, head, path)

    # A5: evidence captures are flat under governance-register/evidence/.
    def test_governance_evidence_capture_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/governance-register/evidence/"
            "new-capture.json":
                '{"captured_at": "2026-11-24T00:00:00Z"}\n',
        })

        self.assert_admission_passes(base, head)

    # A5: a nested capture directory is outside the flat evidence shape.
    def test_nested_governance_evidence_capture_is_rejected(self):
        base = self.seed_base()
        path = (
            "14-ai-development/governance-register/evidence/"
            "sub/new-capture.json"
        )
        head = self.commit({
            path: '{"captured_at": "2026-11-24T00:00:00Z"}\n',
        })

        self.assert_admission_fails(base, head, path)

    # A6: each crate's verification note sits beside its manifest.
    def test_crate_verification_note_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "crates/new-crate/VERIFICATION.txt":
                "cargo test: 12 passed\n",
        })

        self.assert_admission_passes(base, head)

    # A6: a verification note one level deeper is not the crate-level shape.
    def test_nested_crate_verification_note_is_rejected(self):
        base = self.seed_base()
        path = "crates/new-crate/sub/VERIFICATION.txt"
        head = self.commit({
            path: "cargo test: 3 passed\n",
        })

        self.assert_admission_fails(base, head, path)

    # A8: both alternation branches are exercised. The baselines directory
    # branch and the root bilingual baseline branch are separate shapes.
    def test_baseline_files_are_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "scripts/ci/baselines/new-baseline.txt": "frozen\n",
            "scripts/bilingual-baseline.txt": "frozen\n",
        })

        self.assert_admission_passes(base, head)

    # A8: a baseline nested under the baselines directory is not the shape;
    # that directory is flat by design.
    def test_nested_baseline_file_is_rejected(self):
        base = self.seed_base()
        path = "scripts/ci/baselines/sub/new-baseline.txt"
        head = self.commit({
            path: "frozen\n",
        })

        self.assert_admission_fails(base, head, path)

    # B9: the GOV-DOC-001 inheritance file is a singleton exact path.
    def test_gov_doc_001_inheritance_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            ".governance/GOV-DOC-001-inheritance.json":
                '{"inherits": []}\n',
        })

        self.assert_admission_passes(base, head)

    # B9: a sibling inheritance file with a different check ID is a different
    # document and was not ruled in. A prefix rule would admit this.
    def test_gov_doc_002_inheritance_is_rejected(self):
        base = self.seed_base()
        path = ".governance/GOV-DOC-002-inheritance.json"
        head = self.commit({
            path: '{"inherits": []}\n',
        })

        self.assert_admission_fails(base, head, path)

    # B10: the architecture document-metadata schema is a singleton path.
    def test_architecture_metadata_schema_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "00-governance/architecture-document-metadata.schema.yaml":
                "type: object\n",
        })

        self.assert_admission_passes(base, head)

    # B10: another schema in the same directory is not this document.
    def test_other_governance_schema_is_rejected(self):
        base = self.seed_base()
        path = "00-governance/other-metadata.schema.yaml"
        head = self.commit({
            path: "type: object\n",
        })

        self.assert_admission_fails(base, head, path)

    # B11: the document scope registry is a singleton path.
    def test_document_scope_registry_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "00-governance/document-scope-registry.yaml":
                "scopes: []\n",
        })

        self.assert_admission_passes(base, head)

    # B11: a differently named registry is not the registered document.
    def test_other_scope_registry_is_rejected(self):
        base = self.seed_base()
        path = "00-governance/other-scope-registry.yaml"
        head = self.commit({
            path: "scopes: []\n",
        })

        self.assert_admission_fails(base, head, path)

    # B13: the canonical work-item registry schema is a singleton path.
    def test_work_item_registry_schema_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "00-governance/schemas/work-item-registry.schema.json":
                '{"$schema": "https://json-schema.org/draft/2020-12/schema"}\n',
        })

        self.assert_admission_passes(base, head)

    # B13: a sibling schema under the same directory is a different document.
    def test_other_registry_schema_is_rejected(self):
        base = self.seed_base()
        path = "00-governance/schemas/other-registry.schema.json"
        head = self.commit({
            path: '{"type": "object"}\n',
        })

        self.assert_admission_fails(base, head, path)

    # B12: the remote worker inventory is a singleton path.
    def test_remote_worker_inventory_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/remote-worker-inventory.yaml":
                "workers: []\n",
        })

        self.assert_admission_passes(base, head)

    # B12: a sibling inventory file is not the registered document.
    def test_other_worker_inventory_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/other-worker-inventory.yaml"
        head = self.commit({
            path: "workers: []\n",
        })

        self.assert_admission_fails(base, head, path)

    # M21: the same directory, a different YAML filename, is not the registry
    # file. A prefix rule would admit this; the anchored shape does not.
    def test_other_yaml_in_work_item_directory_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/work-items/AID-2026-055/notes.yaml"
        head = self.commit({path: "note: value\n"})

        self.assert_admission_fails(base, head, path)

    # M22: nesting is not the registry shape. work-items/<ID>/nested/ is one
    # directory deeper than a manifest may live.
    def test_nested_work_item_manifest_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/work-items/AID-2026-055/nested/manifest.yaml"
        head = self.commit({path: "work_item_id: AID-2026-055\n"})

        self.assert_admission_fails(base, head, path)

    # M23: the AID- segment is required, so an arbitrary directory under
    # work-items/ cannot carry a manifest through this rule.
    def test_non_aid_directory_manifest_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/work-items/not-AID/manifest.yaml"
        head = self.commit({path: "work_item_id: not-AID\n"})

        self.assert_admission_fails(base, head, path)

    # M24: the rule is rooted at 14-ai-development/work-items/, not at any
    # path that happens to end in manifest.yaml.
    def test_manifest_outside_work_items_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/other/manifest.yaml"
        head = self.commit({path: "work_item_id: other\n"})

        self.assert_admission_fails(base, head, path)

    # M25: the anchored shape is case-sensitive, like the configuration
    # filenames. Manifest.YAML is not manifest.yaml.
    def test_case_changed_manifest_filename_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/work-items/AID-2026-055/Manifest.YAML"
        head = self.commit({path: "work_item_id: AID-2026-055\n"})

        self.assert_admission_fails(base, head, path)

    # M26: a bare manifest.yaml at the repository root is not the registry
    # file and must not be admitted by a loose suffix-shaped rule.
    def test_root_manifest_is_rejected(self):
        base = self.seed_base()
        path = "manifest.yaml"
        head = self.commit({path: "work_item_id: root\n"})

        self.assert_admission_fails(base, head, path)

    # M27: admitting the work-item manifest must not have opened .yaml
    # anywhere else. This is the regression that matters most, because a
    # future edit widening the rule would otherwise pass silently.
    def test_yaml_outside_the_registry_shape_is_still_rejected(self):
        base = self.seed_base()
        path = "00-governance/unreviewed-policy.yaml"
        head = self.commit({path: "policy: value\n"})

        self.assert_admission_fails(base, head, path)

    # AID-2026-251: the schema is admitted at one exact path; the rule
    # must not admit arbitrary YAML alongside the manifest registry.
    def test_work_item_manifest_schema_exact_path_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/work-items/work-item-manifest.schema.yaml":
                "schema_version: \"1\"\\n",
        })
        self.assert_admission_passes(base, head)

    # M28: the ID segment is not an arbitrary alnum run. A directory the
    # registry cannot allocate must not carry a manifest through this rule,
    # or the index step gets an entry it cannot resolve.
    def test_non_numeric_work_item_id_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/work-items/AID-foo/manifest.yaml"
        head = self.commit({path: "work_item_id: AID-foo\n"})

        self.assert_admission_fails(base, head, path)

    # M29: the sequence is three digits. Two digits is a different ID.
    def test_two_digit_sequence_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/work-items/AID-2026-55/manifest.yaml"
        head = self.commit({path: "work_item_id: AID-2026-55\n"})

        self.assert_admission_fails(base, head, path)

    # M30: the year is four digits. A two-digit year is a different ID.
    def test_two_digit_year_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/work-items/AID-26-055/manifest.yaml"
        head = self.commit({path: "work_item_id: AID-26-055\n"})

        self.assert_admission_fails(base, head, path)

    # M31: the sequence is exactly three digits. Four is a different ID.
    def test_four_digit_sequence_is_rejected(self):
        base = self.seed_base()
        path = "14-ai-development/work-items/AID-2026-0555/manifest.yaml"
        head = self.commit({path: "work_item_id: AID-2026-0555\n"})

        self.assert_admission_fails(base, head, path)

    # M32: the year is a shape, not a constant. Pinning it to the year the
    # rule was written would reject next year's first work item, and nobody
    # would remember to edit the rule. A different four-digit year must pass.
    def test_next_year_work_item_id_is_admitted(self):
        base = self.seed_base()
        head = self.commit({
            "14-ai-development/work-items/AID-2027-001/manifest.yaml":
                "work_item_id: AID-2027-001\n",
        })

        self.assert_admission_passes(base, head)

    # #891: the index is Canonical, so its membership must be falsifiable.
    # Every directory under work-items/ needs an entry, and every entry that
    # names a directory needs that directory. These three cases pin both
    # directions plus the clean state.
    def index_fixture(self, index_text, directories):
        files = {
            "14-ai-development/work-items/INDEX.md": index_text,
        }
        for name in directories:
            files[f"14-ai-development/work-items/{name}/manifest.yaml"] = (
                f"work_item_id: {name}\n"
            )
        return self.commit(files)

    def test_index_membership_passes_when_every_directory_is_listed(self):
        self.index_fixture(
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n"
            "| [AID-2026-002](AID-2026-002/manifest.yaml) |\n",
            ["AID-2026-001", "AID-2026-002"],
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        # A pass that compared nothing would look identical to a real pass, so
        # the counts are asserted: two directories on disk, two linked paths.
        # A zero here means the sets were empty and the check bound nothing.
        self.assertIn("directories=2 linked=2", result.stdout)

    # A summary line with equal counts cannot distinguish two counters from one
    # counter printed twice: `directories={n} linked={n}` passes either way. The
    # counts must therefore be asserted somewhere they differ, or the assertion
    # proves only that some number was printed. Three directories, two linked.
    def test_membership_summary_counts_the_two_sets_separately(self):
        self.index_fixture(
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n"
            "| [AID-2026-002](AID-2026-002/manifest.yaml) |\n",
            ["AID-2026-001", "AID-2026-002", "AID-2026-003"],
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertIn("directories=3 linked=2", result.stdout)
        self.assertNotIn("directories=3 linked=3", result.stdout)

    def test_index_membership_fails_on_a_directory_with_no_entry(self):
        self.index_fixture(
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n",
            ["AID-2026-001", "AID-2026-002"],
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertIn(
            "::error::index membership violation: directory present, "
            "no index entry: 14-ai-development/work-items/AID-2026-002",
            result.stderr,
        )

    def test_index_membership_fails_on_an_entry_with_no_directory(self):
        self.index_fixture(
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n"
            "| [AID-2026-009](AID-2026-009/manifest.yaml) |\n",
            ["AID-2026-001"],
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertIn(
            "::error::index membership violation: index entry present, "
            "no directory: 14-ai-development/work-items/AID-2026-009",
            result.stderr,
        )

    # #1212: with either side absent the old code returned [] -- no violations
    # over an empty set -- which is a pass that compared nothing. Deleting the
    # Canonical index, or renaming work-items/ so no directory is found, must
    # not be the cheapest way to silence this check, so both cases exit 2.
    def test_index_membership_fails_closed_without_work_item_directories(self):
        self.commit({"README.md": "no work items here\n"}, with_index=False)

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            2,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "no work-item directories under '14-ai-development/work-items'",
            result.stderr,
        )

    def test_index_membership_fails_closed_without_the_index(self):
        self.commit(
            {
                "14-ai-development/work-items/AID-2026-001/manifest.yaml":
                    "work_item_id: AID-2026-001\n",
            },
            with_index=False,
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            2,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "the work-item index '14-ai-development/work-items/INDEX.md' is "
            "absent from the tree",
            result.stderr,
        )

    # #944: a link anywhere in the file used to register a directory, so a row
    # could be commented out -- invisible to every reader -- and the check
    # stayed green. Registration now requires a table row. Each of the three
    # non-row carriers below is the only reference to its directory, so the
    # directory must be reported missing; if the old whole-file rule returns,
    # the link counts and the check passes, which is what makes these tests
    # evidence rather than decoration.
    def assert_membership_fails_for(self, index_text, directory):
        self.index_fixture(index_text, ["AID-2026-001", directory])

        result = self.run_checker_args("--head-tree-only")
        # The named violation is asserted before the exit code: a mutation that
        # restores the whole-file rule has to fail on this line, so the failure
        # says which directory went unregistered instead of only that some
        # count moved.
        self.assertIn(
            "::error::index membership violation: directory present, "
            f"no index entry: 14-ai-development/work-items/{directory}",
            result.stderr,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_index_membership_ignores_a_link_inside_an_html_comment(self):
        self.assert_membership_fails_for(
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n"
            "<!-- | [AID-2026-002](AID-2026-002/manifest.yaml) | -->\n",
            "AID-2026-002",
        )

    def test_index_membership_ignores_a_link_in_prose(self):
        self.assert_membership_fails_for(
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n"
            "\n"
            "The registry row for AID-2026-002 lives at "
            "[AID-2026-002](AID-2026-002/manifest.yaml) once it is due.\n",
            "AID-2026-002",
        )

    def test_index_membership_ignores_a_link_inside_a_fenced_code_block(self):
        self.assert_membership_fails_for(
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n"
            "\n"
            "```\n"
            "| [AID-2026-002](AID-2026-002/manifest.yaml) |\n"
            "```\n",
            "AID-2026-002",
        )

    # The control for the three above: prose, a comment and a fence around a
    # row must not suppress the row itself. Without this, a rule that rejected
    # every line would pass all three tests.
    def test_index_membership_counts_a_row_among_prose_and_a_comment(self):
        self.index_fixture(
            "Prose before the table.\n"
            "<!-- a comment mentioning [AID-2026-009](AID-2026-009/x.md) -->\n"
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n"
            "| [AID-2026-002](AID-2026-002/manifest.yaml) |\n",
            ["AID-2026-001", "AID-2026-002"],
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn("directories=2 linked=2", result.stdout)

    def manifest_consistency_fixture(self, manifest_text):
        return self.commit({
            "14-ai-development/work-items/INDEX.md":
                "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n",
            "14-ai-development/work-items/AID-2026-001/manifest.yaml":
                manifest_text,
        })

    # R20-01 positive: implementation.status PR_OPEN without a valid
    # positive integer implementation.pull_request must fail.
    def test_manifest_pr_open_requires_positive_pull_request(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            "status: DISPATCHED\n"
            "implementation:\n"
            "  status: PR_OPEN\n"
            "  pull_request: PENDING\n"
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertIn(
            "::error::manifest consistency violation: "
            "'14-ai-development/work-items/AID-2026-001/manifest.yaml': "
            "PR_OPEN requires pull_request to be a positive integer",
            result.stderr,
        )

    # R20-01 negative: PR_OPEN with a positive integer PR number passes.
    # The number lives under `implementation:`, which is where the real
    # manifests put it; a top-level pull_request is a different field.
    def test_manifest_pr_open_with_positive_pull_request_passes(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            "status: PR_OPEN\n"
            "implementation:\n"
            "  status: PR_OPEN\n"
            "  pull_request: 567\n"
            "  merge_commit_sha: NOT_MERGED\n"
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn(
            "Work-item manifest consistency version=2026-11-28.3 "
            "manifests=1 in_scope=1 excluded_by_record_type=0 "
            "unrecognized=0 violations=0",
            result.stdout,
        )

    # R20-02 positive: VERIFIED is a completed lifecycle assertion and
    # cannot coexist with implementation.merge_commit_sha NOT_MERGED.
    def test_manifest_not_merged_conflicts_with_verified_status(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            "status: VERIFIED\n"
            "implementation:\n"
            "  status: MERGED\n"
            "  pull_request: 521\n"
            "  merge_commit_sha: NOT_MERGED\n"
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertIn(
            "::error::manifest consistency violation: "
            "'14-ai-development/work-items/AID-2026-001/manifest.yaml': "
            "merge_commit_sha is NOT_MERGED while the lifecycle status "
            "asserts merged implementation",
            result.stderr,
        )

    # R20-02 negative: NOT_MERGED is consistent with a dispatched,
    # not-yet-implemented work item.
    def test_manifest_not_merged_with_not_started_passes(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            "status: DISPATCHED\n"
            "implementation:\n"
            "  status: NOT_STARTED\n"
            "  pull_request: PENDING\n"
            "  merge_commit_sha: NOT_MERGED\n"
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn(
            "Work-item manifest consistency version=2026-11-28.3 "
            "manifests=1 in_scope=1 excluded_by_record_type=0 "
            "unrecognized=0 violations=0",
            result.stdout,
        )

    # Reverse regression: a full SHA under implementation.merge_commit_sha
    # is not by itself evidence that implementation.status must be MERGED.
    # The checker must not read NOT_STARTED + full SHA as a contradiction;
    # see the docstring for why the rule was withdrawn rather than narrowed.
    def test_manifest_not_started_with_full_merge_sha_is_not_a_violation(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            "status: REGISTERED\n"
            "implementation:\n"
            "  status: NOT_STARTED\n"
            "  pull_request: 737\n"
            "  merge_commit_sha: "
            "776f04fb694140f8663a87d593be1da2957673a4\n"
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "manifests=1 in_scope=1 excluded_by_record_type=0 "
            "unrecognized=0 violations=0",
            result.stdout,
        )

    # R20-03 negative: NOT_STARTED with NOT_MERGED is the dispatched shape.
    def test_manifest_not_started_with_not_merged_passes(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            "status: DISPATCHED\n"
            "implementation:\n"
            "  status: NOT_STARTED\n"
            "  pull_request: PENDING\n"
            "  merge_commit_sha: NOT_MERGED\n"
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn(
            "Work-item manifest consistency version=2026-11-28.3 "
            "manifests=1 in_scope=1 excluded_by_record_type=0 "
            "unrecognized=0 violations=0",
            result.stdout,
        )

    # Scope: a nested `status:` cell must not stand in for the top-level
    # lifecycle status. A first-match-wins scan over the whole file would
    # read "MERGED" here and red on R20-02; the top-level value is
    # DISPATCHED, and the item is legitimately not merged.
    def test_nested_status_does_not_impersonate_top_level_status(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            "evidence:\n"
            "  table:\n"
            '    status: "MERGED"\n'
            "status: DISPATCHED\n"
            "implementation:\n"
            "  status: NOT_STARTED\n"
            "  pull_request: PENDING\n"
            "  merge_commit_sha: NOT_MERGED\n"
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "manifests=1 in_scope=1 excluded_by_record_type=0 "
            "unrecognized=0 violations=0",
            result.stdout,
        )

    # Scope: the mirror case. implementation.merge_commit_sha must come from
    # the implementation mapping, not from a same-named key elsewhere. A
    # top-level merge_commit_sha of NOT_MERGED must not satisfy R20-03's
    # negative side nor fire R20-02 for a VERIFIED item, because that field
    # is outside the implementation mapping.
    def test_same_named_key_outside_implementation_is_not_read(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            "status: VERIFIED\n"
            "merge_commit_sha: NOT_MERGED\n"
            "implementation:\n"
            "  status: MERGED\n"
            "  pull_request: 521\n"
            "  merge_commit_sha: 1a5342421a9d8314dc1ecc2d050a8f75452c3fc3\n"
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    # A manifest whose lifecycle fields this rule set cannot locate is
    # counted, not silently passed. Two real manifests use flat keys
    # (`registration_status`, `implementation_status`) instead of a
    # top-level `status` plus an `implementation:` mapping.
    def test_manifest_without_lifecycle_fields_is_counted_unrecognized(self):
        self.manifest_consistency_fixture(
            "work_item_id: AID-2026-001\n"
            'registration_status: "PENDING_FORMAL_REGISTRATION"\n'
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "manifests=1 in_scope=0 excluded_by_record_type=0 "
            "unrecognized=1 violations=0",
            result.stdout,
        )
    # S1: a record that declares a different record_type is a different kind
    # of record living at a manifest path, not a manifest with missing fields.
    # Exclusion needs the exact path+record_type pair, and once excluded the
    # gate must not read its fields at all.
    def registry_fixture(self, entries, manifests):
        index = "".join(
            f"| [{name}]({name}/manifest.yaml) |\n"
            for name in sorted(manifests)
        )
        registry = 'schema_registry_version: "1"\nexcluded_records:\n'
        for path, record_type in entries:
            registry += (
                f'  - path: "{path}"\n'
                f'    record_type: "{record_type}"\n'
                '    disposition: "EXCLUDED_FROM_MANIFEST_CONSISTENCY_GATE"\n'
                '    rationale: "test fixture"\n'
            )
        files = {
            "14-ai-development/work-items/INDEX.md": index,
            "14-ai-development/work-items/manifest-schema-registry.yaml":
                registry,
        }
        for name, text in manifests.items():
            files[f"14-ai-development/work-items/{name}/manifest.yaml"] = text
        return self.commit(files)

    def test_registry_exact_pair_excludes_record(self):
        self.registry_fixture(
            [(
                "14-ai-development/work-items/AID-2026-001/manifest.yaml",
                "STAGE_0_WORK_ITEM_REGISTRATION",
            )],
            {"AID-2026-001":
                'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n'},
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "manifests=1 in_scope=0 excluded_by_record_type=1 "
            "unrecognized=0 violations=0",
            result.stdout,
        )
        self.assertNotIn("unrecognized shape", result.stderr)

    # The path alone is not a decision. When the registry names the path but
    # the file declares a different record_type, the record stays in
    # unrecognized: a registry that no longer matches the file must not
    # silently keep excluding it.
    def test_registry_path_with_wrong_record_type_does_not_exclude(self):
        self.registry_fixture(
            [(
                "14-ai-development/work-items/AID-2026-001/manifest.yaml",
                "STAGE_0_WORK_ITEM_REGISTRATION",
            )],
            {"AID-2026-001": 'record_type: "SOMETHING_ELSE"\n'},
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn(
            "manifests=1 in_scope=0 excluded_by_record_type=0 "
            "unrecognized=1 violations=0",
            result.stdout,
        )
        self.assertIn("unrecognized shape", result.stderr)

    # And the record_type alone is not a decision either: a second file with
    # the same type at a path nobody registered does not inherit the first
    # file's exclusion.
    def test_registry_record_type_does_not_exclude_another_path(self):
        self.registry_fixture(
            [(
                "14-ai-development/work-items/AID-2026-001/manifest.yaml",
                "STAGE_0_WORK_ITEM_REGISTRATION",
            )],
            {
                "AID-2026-001":
                    'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n',
                "AID-2026-002":
                    'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n',
            },
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn(
            "manifests=2 in_scope=0 excluded_by_record_type=1 "
            "unrecognized=1 violations=0",
            result.stdout,
        )
        self.assertIn("AID-2026-002/manifest.yaml", result.stderr)

    # The three buckets must add up. One in_scope item, one excluded, one
    # unrecognized: if any bucket double-counts, the totals stop matching.
    def test_registry_buckets_sum_to_the_manifest_count(self):
        self.registry_fixture(
            [(
                "14-ai-development/work-items/AID-2026-002/manifest.yaml",
                "STAGE_0_WORK_ITEM_REGISTRATION",
            )],
            {
                "AID-2026-001": (
                    "work_item_id: AID-2026-001\n"
                    "status: DISPATCHED\n"
                    "implementation:\n"
                    "  status: NOT_STARTED\n"
                    "  merge_commit_sha: NOT_MERGED\n"
                ),
                "AID-2026-002":
                    'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n',
                "AID-2026-003": 'record_type: "UNREGISTERED_TYPE"\n',
            },
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn(
            "manifests=3 in_scope=1 excluded_by_record_type=1 "
            "unrecognized=1 violations=0",
            result.stdout,
        )

    # A registry naming the same path twice is a contradiction about one
    # record, so it fails rather than picking one.
    def test_registry_duplicate_path_fails(self):
        self.registry_fixture(
            [
                (
                    "14-ai-development/work-items/AID-2026-001/manifest.yaml",
                    "STAGE_0_WORK_ITEM_REGISTRATION",
                ),
                (
                    "14-ai-development/work-items/AID-2026-001/manifest.yaml",
                    "STAGE_0_WORK_ITEM_REGISTRATION",
                ),
            ],
            {"AID-2026-001":
                'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n'},
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 2, msg=result.stdout)
        self.assertIn("registered twice", result.stderr)

    # The same path registered with two different types is a conflict, not a
    # duplicate: one of the two entries is simply wrong.
    def test_registry_conflicting_record_types_fail(self):
        self.registry_fixture(
            [
                (
                    "14-ai-development/work-items/AID-2026-001/manifest.yaml",
                    "STAGE_0_WORK_ITEM_REGISTRATION",
                ),
                (
                    "14-ai-development/work-items/AID-2026-001/manifest.yaml",
                    "SOMETHING_ELSE",
                ),
            ],
            {"AID-2026-001":
                'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n'},
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 2, msg=result.stdout)
        self.assertIn("two different record_type values", result.stderr)

    # A registry that excludes a path this commit does not contain is stale.
    # Silently excluding nothing would hide an entry that stopped applying.
    def test_registry_entry_for_absent_path_fails(self):
        self.registry_fixture(
            [(
                "14-ai-development/work-items/AID-2026-009/manifest.yaml",
                "STAGE_0_WORK_ITEM_REGISTRATION",
            )],
            {"AID-2026-001": "work_item_id: AID-2026-001\nstatus: DISPATCHED\n"},
        )

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 2, msg=result.stdout)
        self.assertIn("absent from this commit", result.stderr)

    # A disposition this gate does not implement must fail rather than be
    # ignored: otherwise a typo turns an exclusion into a no-op.
    def test_registry_unknown_disposition_fails(self):
        registry = (
            'schema_registry_version: "1"\n'
            "excluded_records:\n"
            '  - path: "14-ai-development/work-items/AID-2026-001/manifest.yaml"\n'
            '    record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n'
            '    disposition: "WAIVED_FOREVER"\n'
        )
        self.commit({
            "14-ai-development/work-items/INDEX.md":
                "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n",
            "14-ai-development/work-items/manifest-schema-registry.yaml":
                registry,
            "14-ai-development/work-items/AID-2026-001/manifest.yaml":
                'record_type: "STAGE_0_WORK_ITEM_REGISTRATION"\n',
        })

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 2, msg=result.stdout)
        self.assertIn("does not implement", result.stderr)

    # A missing registry is an error, not an empty registry. "No policy
    # declared" and "policy unreadable" must not print the same thing.
    def test_missing_registry_fails_instead_of_excluding_nothing(self):
        self.commit({
            "14-ai-development/work-items/INDEX.md":
                "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n",
            "14-ai-development/work-items/AID-2026-001/manifest.yaml":
                "work_item_id: AID-2026-001\nstatus: DISPATCHED\n",
        }, with_registry=False)

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(result.returncode, 2, msg=result.stdout)
        self.assertIn("manifest-schema-registry.yaml", result.stderr)
    # The registry rule is an exact path, and "exact" has to hold in the
    # calling form, not just in the pattern. A suffix after the name must not
    # ride in on the prefix, and neither must a directory prefix.
    def test_schema_registry_filename_variant_is_rejected(self):
        base = self.seed_base()
        for path in (
            "14-ai-development/work-items/manifest-schema-registry.yaml.bak",
            "14-ai-development/work-items/manifest-schema-registry.yml",
            "nested/14-ai-development/work-items/"
            "manifest-schema-registry.yaml",
        ):
            head = self.commit({path: 'schema_registry_version: "1"\n'})
            self.assert_admission_fails(base, head, path)

    # An empty registry is a policy: it declares that nothing is excluded.
    # A missing registry is not a policy. These two states must be
    # distinguishable, so the empty one gets its own passing case rather than
    # only appearing as the default no test looks at.
    def test_explicit_empty_registry_is_a_valid_policy(self):
        self.commit({
            "14-ai-development/work-items/INDEX.md":
                "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n",
            "14-ai-development/work-items/manifest-schema-registry.yaml":
                EMPTY_SCHEMA_REGISTRY,
            "14-ai-development/work-items/AID-2026-001/manifest.yaml":
                "work_item_id: AID-2026-001\nstatus: DISPATCHED\n"
                "implementation:\n"
                "  status: NOT_STARTED\n"
                "  merge_commit_sha: NOT_MERGED\n",
        })

        result = self.run_checker_args("--head-tree-only")
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(
            "manifests=1 in_scope=1 excluded_by_record_type=0 "
            "unrecognized=0 violations=0",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
