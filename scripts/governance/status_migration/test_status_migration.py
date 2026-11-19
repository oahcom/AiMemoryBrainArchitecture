import tempfile
import unittest
from pathlib import Path

import yaml

from migrate_status import PHASES, run
from check_status_gates import check


class StatusMigrationTests(unittest.TestCase):
    def test_all_twelve_exact_source_states_are_mapped(self):
        self.assertEqual(
            set(PHASES),
            {
                "PROPOSED", "ANALYZED", "PROMPT_READY", "READY",
                "IN_PROGRESS", "IMPLEMENTED", "VERIFIED", "REVIEWED",
                "INTEGRATION_READY", "ACCEPTED", "MERGED", "CLOSED",
            },
        )
        self.assertEqual(len(PHASES), 12)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: PROPOSED\n", encoding="utf-8")
            original = path.read_bytes()
            result = run(path)
            self.assertEqual(result["result"], "WOULD_MIGRATE")
            self.assertEqual(path.read_bytes(), original)

    def test_decorated_status_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: 'IN_PROGRESS — active'\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                run(path, apply=True)
            self.assertFalse(
                path.with_name(path.name + ".pre-status-migration.bak").exists()
            )

    def test_blocked_and_rejected_markers_are_preserved_orthogonally(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            markers = {
                "blocked": {"reason": "dependency", "owner": "Owner A"},
                "rejected": {"reason": "superseded proposal", "owner": "Owner B"},
            }
            path.write_text(
                yaml.safe_dump({"status": "IN_PROGRESS", **markers}, sort_keys=False),
                encoding="utf-8",
            )
            run(path, apply=True)
            migrated = yaml.safe_load(path.read_bytes())
            self.assertEqual(migrated["status"], "IN_PROGRESS")
            self.assertEqual(migrated["lifecycle"]["phase"], "ACTIVE")
            self.assertEqual(migrated["lifecycle"]["markers"], markers)

    def test_unknown_status_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: ADOPTED\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                run(path, apply=True)

    def test_apply_backup_and_exact_byte_rollback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            original = b"status: VERIFIED\n"
            path.write_bytes(original)
            result = run(path, apply=True)
            self.assertEqual(result["result"], "MIGRATED")
            self.assertEqual(
                path.with_name(path.name + ".pre-status-migration.bak").read_bytes(),
                original,
            )
            migrated = yaml.safe_load(path.read_bytes())
            self.assertEqual(migrated["status"], "VERIFIED")
            self.assertEqual(migrated["lifecycle"]["phase"], "VALIDATION")
            self.assertEqual(
                migrated["lifecycle"]["gates"]["verified"]["status"],
                "NOT_RECORDED",
            )
            run(path, rollback=True)
            self.assertEqual(path.read_bytes(), original)

    def test_idempotent_apply_does_not_overwrite_existing_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text("status: READY\n", encoding="utf-8")
            run(path, apply=True)
            backup = path.with_name(path.name + ".pre-status-migration.bak")
            backup_bytes = backup.read_bytes()
            self.assertEqual(run(path, apply=True)["result"], "ALREADY_MIGRATED")
            self.assertEqual(backup.read_bytes(), backup_bytes)

    def test_gate_checker_rejects_unknown_status_and_phase_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text(
                "status: ADOPTED\nlifecycle:\n  phase: INTAKE\n"
                "  source_status: ADOPTED\n  gates: {}\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                check(path)
            path.write_text(
                "status: VERIFIED\nlifecycle:\n  phase: ACTIVE\n"
                "  source_status: VERIFIED\n  gates: {}\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                check(path)

    def test_gate_checker_requires_pass_and_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.yaml"
            path.write_text(
                "status: VERIFIED\nlifecycle:\n  phase: VALIDATION\n"
                "  source_status: VERIFIED\n  gates:\n"
                "    verified:\n      status: NOT_RECORDED\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                check(path)
            path.write_text(
                "status: VERIFIED\nlifecycle:\n  phase: VALIDATION\n"
                "  source_status: VERIFIED\n  gates:\n"
                "    verified:\n      status: PASS\n      evidence: test://exact-run\n",
                encoding="utf-8",
            )
            self.assertEqual(check(path)["result"], "PASS")


if __name__ == "__main__":
    unittest.main()
