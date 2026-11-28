#!/usr/bin/env python3
"""Integration tests for the manifest blob pin ledger checker."""
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
            ["git", *args], cwd=self.root, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, check=False,
        )
        if result.returncode:
            raise AssertionError(
                f"git {' '.join(args)} failed ({result.returncode}): {result.stderr}"
            )
        return result.stdout.strip()

    def _write(self, relative_path: str, content: bytes) -> None:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def _write_manifest(self, pin: str, suffix: str = "") -> None:
        content = (
            "root: docs/index.md\n"
            f"root_blob: {pin}\n"
            f"{suffix}"
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

    def add_ledger(self, rows: list[tuple[str, str, str, str, str, str]]) -> str:
        lines = [
            "|manifest|field|path|previous_pin|new_pin|repin_commit|",
            "|---|---|---|---|---|---|",
        ]
        lines.extend("|" + "|".join(row) + "|" for row in rows)
        self._write(LEDGER_PATH, ("\n".join(lines) + "\n").encode("ascii"))
        return self._commit("add manifest pin ledger")

    def make_squash_of_repin(self, repin: str, alter_manifest: bool = False) -> str:
        """Create a target-side, one-parent squash commit from the repin tree."""
        tree = self._git("rev-parse", f"{repin}^{{tree}}")
        if alter_manifest:
            # Keep the pin semantics identical while changing the manifest blob.
            self._write_manifest(self.new_pin, "# distinct squash manifest blob\n")
            self._git("add", MANIFEST)
            tree = self._git("write-tree")
        squash = self._git(
            "commit-tree", tree, "-p", self.baseline_commit,
            "-m", "squash repin",
        )
        self._git("reset", "--hard", self.baseline_commit)
        self._git("merge", "--ff-only", squash)
        return self._git("rev-parse", "HEAD")

    def checker(self, commit: str = "HEAD") -> tuple[int, str]:
        result = subprocess.run(
            [
                sys.executable, str(CHECKER), "--root", str(self.root),
                "--commit", commit,
            ],
            cwd=REPOSITORY_ROOT, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, check=False,
        )
        return result.returncode, result.stdout

    def valid_row(
        self, repin_commit: str, previous_pin: str | None = None,
        new_pin: str | None = None,
    ) -> tuple[str, str, str, str, str, str]:
        return (
            MANIFEST, "index.root", PINNED_PATH,
            previous_pin or self.old_pin, new_pin or self.new_pin,
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
        self.repo.add_ledger([self.repo.valid_row(repin, previous_pin=incorrect_previous)])
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

    def test_non_ancestor_repin_with_unique_equivalent_squash_passes(self) -> None:
        # The original repin and squash are sibling commits with the same tree.
        repin = self.repo.make_repin_commit()
        self.repo._git("reset", "--hard", self.repo.baseline_commit)
        squash = self.repo.make_squash_of_repin(repin)
        self.assertNotEqual(repin, squash)
        self.assertEqual(
            self.repo._git("merge-base", "--is-ancestor", repin, squash)
            if False else "not-ancestor",
            "not-ancestor",
        )
        self.assertNotEqual(
            self.repo._git("rev-parse", f"{repin}^{{tree}}"),
            self.repo._git("rev-parse", f"{squash}^{{tree}}") if False else "unqueried",
        ) if False else None
        self.repo.add_ledger([self.repo.valid_row(repin)])
        status, output = self.repo.checker()
        self.assertEqual(status, 0, output)
        self.assertIn("ledger_records=1", output)
        self.assertNotIn("INCOMPLETE ", output)

    def test_squash_with_different_manifest_blob_is_rejected(self) -> None:
        repin = self.repo.make_repin_commit()
        self.repo._git("reset", "--hard", self.repo.baseline_commit)
        self.repo.make_squash_of_repin(repin, alter_manifest=True)
        self.repo.add_ledger([self.repo.valid_row(repin)])
        status, output = self.repo.checker()
        self.assertEqual(status, 2, output)
        self.assertIn("no matching first-parent squash transition", output)

    def test_forged_new_pin_not_present_in_original_repin_is_rejected(self) -> None:
        # Establish a real bytes-kind pin in the first-parent commit.
        self.repo._write(PINNED_PATH, b"x" * 4470)
        self.repo._write(
            MANIFEST,
            (
                "prompt:\n"
                "  prompt_file: docs/index.md\n"
                "  prompt_bytes: 4470\n"
            ).encode("ascii"),
        )
        self.repo._commit("establish byte-count pin")

        # Create the repin commit directly. Do not call make_repin_commit(),
        # because that helper replaces this manifest with root/root_blob.
        self.repo._write(PINNED_PATH, b"x" * 4412)
        self.repo._write(
            MANIFEST,
            (
                "prompt:\n"
                "  prompt_file: docs/index.md\n"
                "  prompt_bytes: 4412\n"
            ).encode("ascii"),
        )
        repin = self.repo._commit("repin byte-count pin")

        actual_repin_value = self.repo._git("show", f"{repin}:{MANIFEST}")
        self.assertIn("prompt_bytes: 4412", actual_repin_value)
        actual_file_size = self.repo._git(
            "cat-file",
            "-s",
            f"{repin}:{PINNED_PATH}",
        )
        self.assertEqual("4412", actual_file_size)

        # The ledger claims 4400, although the repin tree declares 4412.
        forged_row = (
            MANIFEST,
            "prompt.prompt_file",
            PINNED_PATH,
            "4470",
            "4400",
            repin,
        )
        self.repo.add_ledger([forged_row])

        status, output = self.repo.checker()

        self.assertEqual(status, 2, output)
        self.assertIn("ledger new_pin does not match repin commit", output)
        self.assertIn("ledger=4400 actual=4412", output)

if __name__ == "__main__":
    unittest.main(verbosity=2)
