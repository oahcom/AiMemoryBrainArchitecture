#!/usr/bin/env python3
"""Tests for the repository hygiene and new-file admission gates."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


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
        text=True,
    ).stdout.strip()


class RepositoryHygieneTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)

        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "Hygiene Test")
        git(self.repo, "config", "user.email", "hygiene@example.invalid")

    def tearDown(self):
        self.tempdir.cleanup()

    def commit(self, files):
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

    def assert_admission_fails(self, base, head, path):
        result = self.run_checker(base, head)
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        expected = (
            "::error::new-file admission violation: "
            f"no allowlist rule for '{path}'"
        )
        self.assertIn(expected, result.stderr)

    def test_new_allowed_source_file_passes(self):
        base = self.seed_base()
        head = self.commit({
            "scripts/new_gate.py": "print('hello')\n",
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

        result = self.run_checker_args()

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

        result = self.run_checker_args()

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

        result = self.run_checker_args()
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

        result = self.run_checker_args()
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertIn("directories=3 linked=2", result.stdout)
        self.assertNotIn("directories=3 linked=3", result.stdout)

    def test_index_membership_fails_on_a_directory_with_no_entry(self):
        self.index_fixture(
            "| [AID-2026-001](AID-2026-001/manifest.yaml) |\n",
            ["AID-2026-001", "AID-2026-002"],
        )

        result = self.run_checker_args()
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

        result = self.run_checker_args()
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertIn(
            "::error::index membership violation: index entry present, "
            "no directory: 14-ai-development/work-items/AID-2026-009",
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
