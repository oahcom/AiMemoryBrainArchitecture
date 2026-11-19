import tempfile
import unittest
from pathlib import Path

import yaml

from migrate_status import PHASES, run
from check_status_gates import check


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

    def test_gate_missing_records_rejected_at_required_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: VERIFIED\nlifecycle:\n  phase: VALIDATION\n  source_status: VERIFIED\n  gates: {}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing"):
                check(path)

    def test_gate_rejects_empty_and_fake_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            head = "a" * 40
            content = f"""status: VERIFIED
subject_head: {head}
lifecycle:
  phase: VALIDATION
  source_status: VERIFIED
  subject_head: {head}
  gates:
    verified:
      status: PASS
      evidence:
        commands: [pytest]
        environment: Python 3.13
        tested_head: {head}
        expected_result: 10 tests pass
        actual_result: ""
        logs: fake
"""
            path.write_text(content, encoding="utf-8")
            with self.assertRaises(ValueError):
                check(path)

    def test_gate_rejects_wrong_head(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            head = "a" * 40
            other = "b" * 40
            content = f"""status: VERIFIED
subject_head: {head}
lifecycle:
  phase: VALIDATION
  source_status: VERIFIED
  subject_head: {head}
  gates:
    verified:
      status: PASS
      evidence:
        commands: [pytest]
        environment: Python 3.13
        tested_head: {other}
        expected_result: 10 tests pass
        actual_result: 10 tests pass
        logs: artifacts/test.log
"""
            path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "does not match"):
                check(path)

    def test_gate_rejects_same_person_review(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            head = "a" * 40
            content = f"""status: REVIEWED
subject_head: {head}
lifecycle:
  phase: VALIDATION
  source_status: REVIEWED
  subject_head: {head}
  gates:
    verified:
      status: PASS
      evidence:
        commands: [pytest]
        environment: Python 3.13
        tested_head: {head}
        expected_result: tests pass
        actual_result: tests pass
        logs: artifacts/test.log
    independent_review:
      status: PASS
      evidence:
        reviewer: Alice
        implementer: alice
        reviewed_head: {head}
        report: review.md
        findings_disposition: none
"""
            path.write_text(content, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "different identities"):
                check(path)

    def test_all_six_gate_records_missing_are_rejected_at_closed_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: CLOSED\nlifecycle:\n  phase: COMPLETE\n  source_status: CLOSED\n  gates: {}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                check(path)


if __name__ == "__main__":
    unittest.main()
