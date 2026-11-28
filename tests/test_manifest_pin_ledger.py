#!/usr/bin/env python3
"""Integration tests for the manifest blob pin ledger checker.

Each test creates a temporary Git repository and invokes the real checker
as a subprocess against committed repository history.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "scripts" / "ci" / "check_manifest_blob_pins.py"

MANIFEST = "14-ai-development/work-items/AID-TEST-001/manifest.yaml"
PINNED_PATH = "docs/index.md"
BASELINE_PATH = "scripts/ci/baselines/manifest-blob-pins.txt"
LEDGER_PATH = "scripts/ci/manifest-pin-ledger.md"

OLD_CONTENT = b"old index\n"
NEW_CONTENT = b"new index\n"
UNRELATED_CONTENT = b"unrelated\n"


def blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


class LedgerRepository:
    """Small committed repository with one manifest pin and its history."""

    def __init__(self, root: Path):
        self.root = root
        self._git("init", "-q")
        self._git("config", "user.name", "Ledger Test")
        self._git("config", "user.email", "ledger-test@example.invalid")

        self.old_pin = blob_sha(OLD_CONTENT)
        self.new_pin = blob_sha(NEW_CONTENT)

        self._write(PINNED_PATH, OLD_CONTENT)
        self._write_manifest(self.old_pin)
        self.base_commit = self._commit("initial pinned content")

        self._write(
            BASELINE_PATH,
            f"Measured against main {self.base_commit}.\n".encode("ascii"),
        )
        self.baseline_commit = self._commit("add pin baseline")

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode:
            raise AssertionError(
                f"git {' '.join(args)} failed ({result.returncode}): "
                f"{result.stderr}"
            )
        return result.stdout.strip()

    def _write(self, relative_path: str, content: bytes) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def _write_manifest(self, pin: str) -> None:
        content = (
            "root: docs/index.md\n"
            f"root_blob: {pin}\n"
        ).encode("ascii")
        self._write(MANIFEST, content)

    def _commit(self, message: str) -> str:
        self._git("add", "-A")
        self._git("commit", "-q", "-m", message)
        return self._git("rev-parse", "HEAD")

    def make_unrelated_commit(self) -> str:
        self._write("docs/unrelated.txt", UNRELATED_CONTENT)
        return self._commit("unrelated change")

    def make_repin_commit(self, declared_pin: str | None = None) -> str:
        self._write(PINNED_PATH, NEW_CONTENT)
        self._write_manifest(declared_pin or self.new_pin)
        return self._commit("repin manifest blob")

    def add_ledger(self, rows: list[tuple[str, ...]]) -> str:
        """Write six-column legacy rows and seven-column mode-aware rows.

        Each row is either:
          (manifest, field, path, previous_pin, new_pin, repin_commit)
        or:
          (manifest, field, path, reference_mode, previous_pin, new_pin, repin_commit)
        """
        legacy_rows = [row for row in rows if len(row) == 6]
        mode_rows = [row for row in rows if len(row) == 7]
        if len(legacy_rows) + len(mode_rows) != len(rows):
            raise ValueError("ledger rows must contain exactly six or seven fields")

        lines = []
        if not rows or legacy_rows:
            lines.extend([
                "|manifest|field|path|previous_pin|new_pin|repin_commit|",
                "|---|---|---|---|---|---|",
            ])
            lines.extend("|" + "|".join(row) + "|" for row in legacy_rows)

        if legacy_rows and mode_rows:
            lines.append("")

        if mode_rows:
            lines.extend([
                "|manifest|field|path|reference_mode|previous_pin|new_pin|repin_commit|",
                "|---|---|---|---|---|---|---|",
            ])
            lines.extend("|" + "|".join(row) + "|" for row in mode_rows)

        self._write(LEDGER_PATH, ("\n".join(lines) + "\n").encode("ascii"))
        return self._commit("add manifest pin ledger")

    def checker(self, commit: str = "HEAD") -> tuple[int, str]:
        result = subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--root",
                str(self.root),
                "--commit",
                commit,
            ],
            cwd=REPOSITORY_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout

    def valid_row(
        self,
        repin_commit: str,
        previous_pin: str | None = None,
        new_pin: str | None = None,
    ) -> tuple[str, str, str, str, str, str]:
        return (
            MANIFEST,
            "index.root",
            PINNED_PATH,
            previous_pin or self.old_pin,
            new_pin or self.new_pin,
            repin_commit,
        )

    def valid_mode_row(
        self,
        repin_commit: str,
        reference_mode: str = "current",
        previous_pin: str | None = None,
        new_pin: str | None = None,
    ) -> tuple[str, str, str, str, str, str, str]:
        return (
            MANIFEST,
            "index.root",
            PINNED_PATH,
            reference_mode,
            previous_pin or self.old_pin,
            new_pin or self.new_pin,
            repin_commit,
        )


class ManifestPinLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="manifest-pin-ledger-")
        self.repo = LedgerRepository(Path(self.tempdir.name))

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_valid_record_authorizes_real_first_parent_transition(self) -> None:
        repin = self.repo.make_repin_commit()
        self.repo.add_ledger([self.repo.valid_row(repin)])

        status, output = self.repo.checker()

        self.assertEqual(status, 0, output)
        self.assertIn("ledger_records=1", output)
        self.assertNotIn("VIOLATION ", output)
        self.assertNotIn("INCOMPLETE ", output)

    def test_repin_without_ledger_record_is_a_violation(self) -> None:
        wrong_pin = hashlib.sha1(b"not the pinned blob").hexdigest()
        self.repo.make_repin_commit(declared_pin=wrong_pin)
        self.repo.add_ledger([])

        status, output = self.repo.checker()

        self.assertEqual(status, 1, output)
        self.assertIn("VIOLATION unledgered pin transition", output)

    def test_ledger_chain_discontinuity_is_incomplete(self) -> None:
        repin = self.repo.make_repin_commit()
        incorrect_previous = hashlib.sha1(b"not the previous pin").hexdigest()
        self.repo.add_ledger([
            self.repo.valid_row(repin, previous_pin=incorrect_previous)
        ])

        status, output = self.repo.checker()

        self.assertEqual(status, 2, output)
        self.assertIn("ledger previous_pin does not match first parent", output)

    def test_repin_commit_must_introduce_the_recorded_change(self) -> None:
        unrelated = self.repo.make_unrelated_commit()
        self.repo.make_repin_commit()
        self.repo.add_ledger([self.repo.valid_row(unrelated)])

        status, output = self.repo.checker()

        self.assertEqual(status, 2, output)
        self.assertIn("ledger new_pin does not match repin commit", output)

    def test_target_pin_must_equal_latest_ledger_record(self) -> None:
        repin = self.repo.make_repin_commit()
        self.repo.add_ledger([self.repo.valid_row(repin)])

        wrong_latest = hashlib.sha1(b"later incorrect pin").hexdigest()
        self.repo._write_manifest(wrong_latest)
        self.repo._commit("change target pin without ledger update")

        status, output = self.repo.checker()

        self.assertEqual(status, 2, output)
        self.assertIn("target pin does not equal latest ledger new_pin", output)

    def test_seven_column_current_record_authorizes_transition(self) -> None:
        repin = self.repo.make_repin_commit()
        self.repo.add_ledger([self.repo.valid_mode_row(repin, "current")])

        status, output = self.repo.checker()

        self.assertEqual(status, 0, output)
        self.assertIn("ledger_records=1", output)
        self.assertNotIn("INCOMPLETE ", output)
        self.assertNotIn("VIOLATION ", output)

    def test_six_column_legacy_record_maps_to_current_mode(self) -> None:
        repin = self.repo.make_repin_commit()
        self.repo.add_ledger([self.repo.valid_row(repin)])

        status, output = self.repo.checker()

        self.assertEqual(status, 0, output)
        self.assertIn("ledger_records=1", output)

    def test_seven_column_record_rejects_invalid_reference_mode(self) -> None:
        repin = self.repo.make_repin_commit()
        invalid_row = (
            MANIFEST,
            "index.root",
            PINNED_PATH,
            "sometimes",
            self.repo.old_pin,
            self.repo.new_pin,
            repin,
        )
        self.repo.add_ledger([invalid_row])

        status, output = self.repo.checker()

        self.assertEqual(status, 2, output)
        self.assertIn("INCOMPLETE", output)

    def test_duplicate_transition_across_legacy_and_extended_tables_is_incomplete(self) -> None:
        repin = self.repo.make_repin_commit()
        self.repo.add_ledger([
            self.repo.valid_row(repin),
            self.repo.valid_mode_row(repin, "current"),
        ])

        status, output = self.repo.checker()

        self.assertEqual(status, 2, output)
        self.assertIn("INCOMPLETE", output)
        self.assertIn("duplicate", output.lower())

    def test_reference_mode_is_part_of_ledger_transition_identity(self) -> None:
        repin = self.repo.make_repin_commit()
        self.repo.add_ledger([
            self.repo.valid_mode_row(repin, "historical"),
        ])

        status, output = self.repo.checker()

        self.assertEqual(status, 2, output)
        self.assertIn("INCOMPLETE", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
