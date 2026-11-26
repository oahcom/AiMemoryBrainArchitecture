import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from migrate_status import PHASES, run
from check_status_gates import ORDER, check


HEAD = "a" * 40
EVIDENCE_ARTIFACT = "Verified evidence artifact for the attested subject work.\n"


def git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args], check=True,
        capture_output=True, text=True).stdout.strip()


def make_repo(files):
    directory = tempfile.TemporaryDirectory()
    root = Path(directory.name)
    git(root, "init", "-q")
    git(root, "config", "user.email", "tests@example.invalid")
    git(root, "config", "user.name", "Status Gate Tests")
    # Evidence must be part of the subject commit's tree, so the default
    # evidence artifact is committed with the fixture itself.
    files = {"evidence/proof.txt": EVIDENCE_ARTIFACT, **files}
    for name, content in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    (root / ".fixture").write_text("fixture\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture")
    head = git(root, "rev-parse", "HEAD")
    return directory, root, head


def evidence_for(gate, head, path):
    common = {
        "verified": {
            "commands": ["python -m unittest"],
            "environment": "Python 3.12; PyYAML",
            "tested_head": head,
            "expected_result": "all targeted tests pass",
            "actual_result": "all targeted tests pass",
            "logs": path,
        },
        "independent_review": {
            "reviewer": "reviewer-one",
            "implementer": "implementer-two",
            "reviewer_session": "session-reviewer-one",
            "implementer_session": "session-implementer-two",
            "reviewed_head": head,
            "report": path,
            "findings_disposition": "all findings dispositioned",
        },
        "integration": {
            "compatibility_result": "compatibility checks pass",
            "registry_updates": ["registry checked"],
            "integration_report": path,
        },
        "owner_acceptance": {
            "authority": "authorized owner",
            "decision": "ACCEPT",
            "decision_record": path,
        },
        "merge": {
            "target_branch": "main",
            "merge_commit": head,
            "merge_record": path,
        },
        "closeout": {
            "index_update": "work index updated",
            "closeout_record": path,
        },
    }
    return common[gate]


def manifest_for(source, head, gate_count, evidence_path="evidence/proof.txt"):
    gates = {}
    for index, name in enumerate(ORDER):
        if index < gate_count:
            gates[name] = {
                "status": "PASS",
                "evidence": evidence_for(name, head, evidence_path),
            }
        else:
            gates[name] = {"status": "NOT_RECORDED"}
    phases = {
        "PROPOSED": "INTAKE", "ANALYZED": "INTAKE", "PROMPT_READY": "INTAKE",
        "READY": "READY", "IN_PROGRESS": "ACTIVE", "IMPLEMENTED": "ACTIVE",
        "VERIFIED": "VALIDATION", "REVIEWED": "VALIDATION",
        "INTEGRATION_READY": "VALIDATION", "ACCEPTED": "ACCEPTANCE",
        "MERGED": "COMPLETE", "CLOSED": "COMPLETE",
    }
    return {
        "status": source,
        "subject_head": head,
        "review_identity_aliases": {},
        "source_authenticity": "NOT_VERIFIED",
        "lifecycle": {
            "phase": phases[source],
            "source_status": source,
            "subject_head": head,
            "gates": gates,
            "markers": {},
        },
    }


class StatusMigrationTests(unittest.TestCase):
    def test_all_twelve_exact_source_states_are_mapped(self):
        self.assertEqual(len(PHASES), 12)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: PROPOSED\n", encoding="utf-8")
            original = path.read_bytes()
            self.assertEqual(run(path)["result"], "WOULD_MIGRATE")
            self.assertEqual(path.read_bytes(), original)

    def test_duplicate_status_key_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: PROPOSED\nstatus: CLOSED\n", encoding="utf-8")
            with self.assertRaises(yaml.constructor.ConstructorError):
                run(path, apply=True)

    def test_duplicate_lifecycle_key_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: PROPOSED\nlifecycle: {}\nlifecycle: {}\n", encoding="utf-8")
            with self.assertRaises(yaml.constructor.ConstructorError):
                run(path, apply=True)

    def test_comment_preservation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("# historical header\nstatus: PROPOSED # historical status note\n# trailing historical note\n", encoding="utf-8")
            run(path, apply=True)
            migrated = path.read_text(encoding="utf-8")
            self.assertIn("# historical header", migrated)
            self.assertIn("# historical status note", migrated)
            self.assertIn("# trailing historical note", migrated)
            self.assertEqual(yaml.safe_load(migrated)["lifecycle"]["phase"], "INTAKE")

    def test_rollback_refuses_modified_migrated_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            original = b"status: VERIFIED\n"
            path.write_bytes(original)
            run(path, apply=True)
            path.write_bytes(path.read_bytes() + b"# post-migration edit\n")
            with self.assertRaisesRegex(ValueError, "changed"):
                run(path, rollback=True)
            self.assertNotEqual(path.read_bytes(), original)

    def test_apply_backup_and_hash_guarded_rollback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            original = b"status: VERIFIED\n"
            path.write_bytes(original)
            run(path, apply=True)
            backup = path.with_name(path.name + ".pre-status-migration.bak")
            self.assertEqual(backup.read_bytes(), original)
            run(path, rollback=True)
            self.assertEqual(path.read_bytes(), original)

    def test_idempotent_apply_does_not_overwrite_existing_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: READY\n", encoding="utf-8")
            run(path, apply=True)
            backup = path.with_name(path.name + ".pre-status-migration.bak")
            original_backup = backup.read_bytes()
            self.assertEqual(run(path, apply=True)["result"], "ALREADY_MIGRATED")
            self.assertEqual(backup.read_bytes(), original_backup)

    def test_six_gate_boundaries_pass_only_through_current_checkpoint(self):
        checkpoints = [
            ("VERIFIED", 1), ("REVIEWED", 2), ("INTEGRATION_READY", 3),
            ("ACCEPTED", 4), ("MERGED", 5), ("CLOSED", 6),
        ]
        for source, count in checkpoints:
            with self.subTest(source=source):
                directory, root, head = make_repo({})
                try:
                    path = root / "manifest.yaml"
                    data = manifest_for(source, head, count)
                    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                    git(root, "add", ".")
                    git(root, "commit", "-qm", "manifest fixture")
                    self.assertEqual(check(path)["result"], "PASS")
                finally:
                    directory.cleanup()

    def test_future_gate_cannot_be_pre_passed(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("VERIFIED", head, 1)
            data["lifecycle"]["gates"]["independent_review"] = {
                "status": "PASS", "evidence": evidence_for("independent_review", head, "evidence/proof.txt")
            }
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "future gate fixture")
            with self.assertRaisesRegex(ValueError, "future gate"):
                check(path)
        finally:
            directory.cleanup()

    def test_cross_identity_review_is_independent(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("REVIEWED", head, 2)
            data["review_identity_aliases"] = {"@reviewer_alias": "Reviewer-One"}
            data["lifecycle"]["gates"]["independent_review"]["evidence"]["reviewer"] = "@reviewer_alias"
            data["lifecycle"]["gates"]["independent_review"]["evidence"]["implementer"] = "implementer-two"
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "independent reviewer fixture")
            self.assertEqual(check(path)["result"], "PASS")
        finally:
            directory.cleanup()

    def test_identity_alias_normalization_does_not_decide_independence(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("REVIEWED", head, 2)
            data["review_identity_aliases"] = {"@alice_dev": "Alice"}
            review = data["lifecycle"]["gates"]["independent_review"]["evidence"]
            review["reviewer"] = "https://github.com/alice_dev"
            review["implementer"] = "ＡＬＩＣＥ"
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "alias collision fixture")
            # One account carrying two sessions is the expected case: the
            # account comparison is diagnostic and must not fail the gate.
            self.assertEqual(check(path)["result"], "PASS")
        finally:
            directory.cleanup()

    def test_one_account_with_two_sessions_is_independent(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("REVIEWED", head, 2)
            review = data["lifecycle"]["gates"]["independent_review"]["evidence"]
            review["reviewer"] = "req05-session-a"
            review["implementer"] = "req05-session-a"
            review["reviewer_session"] = "req05-review"
            review["implementer_session"] = "req05-impl"
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "same account, two sessions")
            self.assertEqual(check(path)["result"], "PASS")
        finally:
            directory.cleanup()

    def test_two_accounts_sharing_one_session_is_not_independent(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("REVIEWED", head, 2)
            review = data["lifecycle"]["gates"]["independent_review"]["evidence"]
            review["reviewer"] = "reviewer-alice"
            review["implementer"] = "implementer-bob"
            review["reviewer_session"] = "req05-shared"
            review["implementer_session"] = "req05-shared"
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "two accounts, one session")
            with self.assertRaisesRegex(ValueError, "reviewer_session and implementer_session"):
                check(path)
        finally:
            directory.cleanup()

    def test_identical_account_and_session_is_not_independent(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("REVIEWED", head, 2)
            review = data["lifecycle"]["gates"]["independent_review"]["evidence"]
            review["reviewer"] = "req05-session-a"
            review["implementer"] = "req05-session-a"
            review["reviewer_session"] = "req05-one"
            review["implementer_session"] = "req05-one"
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "identical account and session")
            with self.assertRaisesRegex(ValueError, "different sessions"):
                check(path)
        finally:
            directory.cleanup()

    def test_missing_session_field_is_rejected(self):
        for field in ("reviewer_session", "implementer_session"):
            with self.subTest(field=field):
                directory, root, head = make_repo({})
                try:
                    data = manifest_for("REVIEWED", head, 2)
                    review = data["lifecycle"]["gates"]["independent_review"]["evidence"]
                    del review[field]
                    path = root / "manifest.yaml"
                    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                    git(root, "add", ".")
                    git(root, "commit", "-qm", f"missing {field}")
                    with self.assertRaisesRegex(
                            ValueError, f"independent_review.{field}"):
                        check(path)
                finally:
                    directory.cleanup()

    def test_untrusted_external_and_traversal_references_are_rejected(self):
        directory, root, head = make_repo({})
        try:
            for reference in ("https://attacker.invalid/proof.txt", "../../outside.txt"):
                with self.subTest(reference=reference):
                    data = manifest_for("VERIFIED", head, 1, reference)
                    path = root / "manifest.yaml"
                    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                    git(root, "add", ".")
                    git(root, "commit", "-qm", "untrusted reference fixture")
                    with self.assertRaises(ValueError):
                        check(path)
        finally:
            directory.cleanup()

    def test_untracked_evidence_file_is_not_in_subject_commit_tree(self):
        directory, root, head = make_repo({})
        try:
            evidence = root / "evidence" / "untracked.txt"
            evidence.parent.mkdir(exist_ok=True)
            evidence.write_text(f"subject_head {head}\n", encoding="utf-8", newline="\n")
            data = manifest_for("VERIFIED", head, 1, "evidence/untracked.txt")
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", "manifest.yaml")
            git(root, "commit", "-qm", "manifest without evidence")
            with self.assertRaisesRegex(ValueError, "Git tree"):
                check(path)
        finally:
            directory.cleanup()

    def test_evidence_committed_after_subject_head_is_rejected(self):
        directory, root, head = make_repo({})
        try:
            # Commit a fresh evidence file after the subject commit: the
            # subject tree does not carry it, so the gate must fail closed.
            late = root / "evidence" / "late.txt"
            late.parent.mkdir(exist_ok=True)
            late.write_text("evidence recorded in a later commit\n",
                            encoding="utf-8", newline="\n")
            data = manifest_for("VERIFIED", head, 1, "evidence/late.txt")
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "evidence after subject")
            with self.assertRaisesRegex(ValueError, "Git tree"):
                check(path)
        finally:
            directory.cleanup()

    def test_double_tampering_of_evidence_and_head_is_rejected(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("VERIFIED", head, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "double tamper baseline")
            evidence = root / "evidence" / "proof.txt"
            evidence.write_text("tampered evidence without original subject head\n", encoding="utf-8")
            data["subject_head"] = "b" * 40
            data["lifecycle"]["subject_head"] = "b" * 40
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                check(path)
        finally:
            directory.cleanup()

    def test_gate_rejects_missing_required_records(self):
        directory, root, head = make_repo({})
        try:
            path = root / "manifest.yaml"
            path.write_text("status: VERIFIED\nlifecycle:\n  phase: VALIDATION\n  source_status: VERIFIED\n  subject_head: " + head + "\n  gates: {}\n", encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "missing gates")
            with self.assertRaisesRegex(ValueError, "required gate record missing"):
                check(path)
        finally:
            directory.cleanup()


    def test_future_gate_missing_record_is_rejected(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("VERIFIED", head, 1)
            del data["lifecycle"]["gates"]["independent_review"]
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "future gate record dropped")
            with self.assertRaisesRegex(ValueError, "future gate record missing"):
                check(path)
        finally:
            directory.cleanup()

    def test_evidence_validated_against_subject_tree_not_head(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("VERIFIED", head, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "subject commit")
            # Advance HEAD far past the subject commit.
            (root / "unrelated.txt").write_text("later work\n", encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "later commit")
            self.assertNotEqual(git(root, "rev-parse", "HEAD"), head)
            # Working tree still matches the subject blob: must pass.
            check(path)
        finally:
            directory.cleanup()

    def test_working_tree_drift_from_subject_blob_is_rejected(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("VERIFIED", head, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "subject commit")
            # Move both HEAD and the working tree away from the subject blob.
            (root / "evidence" / "proof.txt").write_text(
                f"rewritten for a different head {head} with new content\n", encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "evidence rewritten")
            with self.assertRaisesRegex(ValueError, "differs from subject_head blob"):
                check(path)
        finally:
            directory.cleanup()

    def test_symlinked_evidence_outside_repo_is_rejected(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("VERIFIED", head, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            outside = root.parent / "outside-secret.txt"
            outside.write_text(f"out-of-repo evidence {head}\n", encoding="utf-8")
            link = root / "evidence" / "proof.txt"
            link.unlink()
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unsupported on this platform")
                return
            git(root, "add", ".")
            git(root, "commit", "-qm", "symlink evidence")
            with self.assertRaises(ValueError):
                check(path)
        finally:
            directory.cleanup()

    def test_sidecar_anchor_detects_silent_tampering(self):
        directory, root, _ = make_repo({})
        try:
            protected = root / "scripts" / "governance" / "protected.py"
            protected.parent.mkdir(parents=True, exist_ok=True)
            protected.write_text("original protected source\n", encoding="utf-8")
            sidecar_rel = "scripts/governance/anchor.sha256"
            sidecar = root / sidecar_rel

            def commit_sidecar():
                blob = git(root, "hash-object", str(protected))
                sidecar.write_text(
                    f"git-blob-sha1 {blob}  scripts/governance/protected.py\n",
                    encoding="utf-8", newline="\n")
                digest = hashlib.sha256(sidecar.read_bytes()).hexdigest()
                git(root, "add", ".")
                git(root, "commit", "-qm", f"anchor {digest}")

            commit_sidecar()
            from check_status_gates import _verify_sidecar_anchor
            self.assertTrue(_verify_sidecar_anchor(root, sidecar_rel))
            # Tamper the protected file only.
            protected.write_text("tampered source\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "does not match sidecar blob"):
                _verify_sidecar_anchor(root, sidecar_rel)
            # Tamper both source and sidecar: anchor still fails.
            protected.write_text("tampered source again\n", encoding="utf-8")
            blob = git(root, "hash-object", str(protected))
            sidecar.write_text(
                f"git-blob-sha1 {blob}  scripts/governance/protected.py\n",
                encoding="utf-8", newline="\n")
            with self.assertRaisesRegex(ValueError, "does not match its commit anchor"):
                _verify_sidecar_anchor(root, sidecar_rel)
            # Only a fresh commit carrying the new anchor restores validity.
            digest = hashlib.sha256(sidecar.read_bytes()).hexdigest()
            git(root, "add", ".")
            git(root, "commit", "-qm", f"anchor {digest}")
            self.assertTrue(_verify_sidecar_anchor(root, sidecar_rel))
        finally:
            directory.cleanup()


    def test_placeholder_evidence_content_is_rejected(self):
        # The placeholder artifact is part of the subject commit itself, so
        # tree membership and blob equality pass; the content check must
        # still reject it.
        directory, root, head = make_repo({
            "evidence/proof.txt": "placeholder evidence content for testing gates\n"})
        try:
            data = manifest_for("VERIFIED", head, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "placeholder manifest")
            with self.assertRaisesRegex(ValueError, "placeholder"):
                check(path)
        finally:
            directory.cleanup()

    def test_tree_sha_as_subject_head_is_rejected(self):
        directory, root, head = make_repo({})
        try:
            tree_sha = git(root, "rev-parse", head + "^{tree}")
            data = manifest_for("VERIFIED", tree_sha, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "tree sha fixture")
            with self.assertRaisesRegex(ValueError, "commit object"):
                check(path)
        finally:
            directory.cleanup()

    def test_optional_sha256_digest_binding(self):
        directory, root, head = make_repo({})
        try:
            import hashlib as _hashlib
            digest = _hashlib.sha256(
                (root / "evidence" / "proof.txt").read_bytes()).hexdigest()
            data = manifest_for("VERIFIED", head, 1)
            # Matching digest passes.
            data["lifecycle"]["gates"]["verified"]["evidence"]["logs_sha256"] = digest
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "digest binding fixture")
            self.assertEqual(check(path)["result"], "PASS")
            # Mismatching digest is rejected.
            data["lifecycle"]["gates"]["verified"]["evidence"]["logs_sha256"] = "0" * 64
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "digest mismatch fixture")
            with self.assertRaisesRegex(ValueError, "does not match evidence content"):
                check(path)
        finally:
            directory.cleanup()


    def test_source_authenticity_boundary(self):
        for variant, pattern in (
            ("missing", "source_authenticity is required"),
            ("illegal", "must be NOT_VERIFIED"),
            ("VERIFIED", "cannot be self-certified"),
        ):
            with self.subTest(variant=variant):
                directory, root, head = make_repo({})
                try:
                    data = manifest_for("VERIFIED", head, 1)
                    if variant == "missing":
                        del data["source_authenticity"]
                    else:
                        data["source_authenticity"] = (
                            "VERIFIED" if variant == "VERIFIED" else "TRUSTED")
                    path = root / "manifest.yaml"
                    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                    git(root, "add", ".")
                    git(root, "commit", "-qm", f"authenticity {variant} fixture")
                    with self.assertRaisesRegex(ValueError, pattern):
                        check(path)
                finally:
                    directory.cleanup()
        # Explicit NOT_VERIFIED passes and is echoed in the report.
        directory, root, head = make_repo({})
        try:
            data = manifest_for("VERIFIED", head, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "authenticity declared fixture")
            report = check(path)
            self.assertEqual(report["source_authenticity"], "NOT_VERIFIED")
            self.assertEqual(report["content_integrity"], "PASS")
        finally:
            directory.cleanup()

    def test_no_pass_gate_does_not_require_authenticity_field(self):
        directory, root, head = make_repo({})
        try:
            data = manifest_for("PROPOSED", head, 0)
            del data["source_authenticity"]
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "no pass gates fixture")
            self.assertEqual(check(path)["result"], "PASS")
        finally:
            directory.cleanup()


if __name__ == "__main__":
    unittest.main()
