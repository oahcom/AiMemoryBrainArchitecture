#!/usr/bin/env python3
"""Tests for the repository hygiene and new-file admission gates."""

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

        # -f is intentional: tests must be able to commit ignored fixtures.
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

    def assert_admission_passes(self, base, head):
        result = self.run_checker(base, head)
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def assert_admission_fails(self, base, head, path):
        result = self.run_checker(base, head)
        self.assertEqual(
            result.returncode,
            1,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        self.assertIn(path, result.stderr)

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

        self.assert_admission_fails(base, head, "_dm.txt")

    def test_gitignored_but_forced_committed_dm_txt_fails(self):
        base = self.seed_base()
        head = self.commit({
            ".gitignore": "/_dm.txt\n",
            "_dm.txt": "forced committed output\n",
        })

        self.assert_admission_fails(base, head, "_dm.txt")

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

        self.assert_admission_fails(base, head, "result.json")

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
        head = git(self.repo, "rev-parse", "HEAD")

        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=self.repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("/_dm.txt", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
