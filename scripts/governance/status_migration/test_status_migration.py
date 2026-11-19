import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from migrate_status import PHASES, run
from check_status_gates import ORDER, check


HEAD = "a" * 40


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
    for name, content in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    (root / ".fixture").write_text("fixture\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", "fixture")
    head = git(root, "rev-parse", "HEAD")
    return directory, root, head


def bind_evidence(root, head, path="evidence/proof.txt"):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"Evidence bound to subject_head {head}\n", encoding="utf-8")


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
                directory, root, head = make_repo({"evidence/proof.txt": "placeholder\n"})
                try:
                    bind_evidence(root, head)
                    path = root / "manifest.yaml"
                    data = manifest_for(source, head, count)
                    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                    git(root, "add", ".")
                    git(root, "commit", "-qm", "manifest fixture")
                    self.assertEqual(check(path)["result"], "PASS")
                finally:
                    directory.cleanup()

    def test_future_gate_cannot_be_pre_passed(self):
        directory, root, head = make_repo({"evidence/proof.txt": "placeholder\n"})
        try:
            bind_evidence(root, head)
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
        directory, root, head = make_repo({"evidence/proof.txt": "placeholder\n"})
        try:
            bind_evidence(root, head)
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

    def test_identity_alias_normalization_rejects_same_person(self):
        directory, root, head = make_repo({"evidence/proof.txt": "placeholder\n"})
        try:
            bind_evidence(root, head)
            data = manifest_for("REVIEWED", head, 2)
            data["review_identity_aliases"] = {"@alice_dev": "Alice"}
            review = data["lifecycle"]["gates"]["independent_review"]["evidence"]
            review["reviewer"] = "https://github.com/alice_dev"
            review["implementer"] = "ＡＬＩＣＥ"
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "alias collision fixture")
            with self.assertRaisesRegex(ValueError, "different identities"):
                check(path)
        finally:
            directory.cleanup()

    def test_untrusted_external_and_traversal_references_are_rejected(self):
        directory, root, head = make_repo({"evidence/proof.txt": "placeholder\n"})
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
            evidence = root / "evidence" / "proof.txt"
            evidence.parent.mkdir()
            evidence.write_text(f"subject_head {head}\n", encoding="utf-8")
            data = manifest_for("VERIFIED", head, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", "manifest.yaml")
            git(root, "commit", "-qm", "manifest without evidence")
            with self.assertRaisesRegex(ValueError, "Git tree"):
                check(path)
        finally:
            directory.cleanup()

    def test_evidence_must_be_bound_to_subject_head(self):
        directory, root, head = make_repo({"evidence/proof.txt": "evidence for a different commit\n"})
        try:
            data = manifest_for("VERIFIED", head, 1)
            path = root / "manifest.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            git(root, "add", ".")
            git(root, "commit", "-qm", "head binding fixture")
            with self.assertRaisesRegex(ValueError, "not bound to subject_head"):
                check(path)
        finally:
            directory.cleanup()

    def test_double_tampering_of_evidence_and_head_is_rejected(self):
        directory, root, head = make_repo({"evidence/proof.txt": "placeholder\n"})
        try:
            bind_evidence(root, head)
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


if __name__ == "__main__":
    unittest.main()
