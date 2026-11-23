#!/usr/bin/env python3
"""Tests for the repository hygiene gate."""

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
    )


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

    def run_checker(self):
        return subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=self.repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )

    def test_prohibited_file_present_fails(self):
        self.commit({
            "_dm.txt": "generated gate output\n",
        })

        result = self.run_checker()

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "::error::repository hygiene violation: "
            "prohibited committed file '/_dm.txt'",
            result.stderr,
        )

    def test_prohibited_file_absent_passes(self):
        self.commit({
            "README.md": "Repository content\n",
        })

        result = self.run_checker()

        self.assertEqual(result.returncode, 0)
        self.assertIn(
            "Repository hygiene check passed.",
            result.stdout,
        )

    def test_gitignore_does_not_excuse_committed_file(self):
        self.commit({
            ".gitignore": "/_dm.txt\n",
            "_dm.txt": "committed generated output\n",
        })

        result = self.run_checker()

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "prohibited committed file '/_dm.txt'",
            result.stderr,
        )

    def test_unrelated_repository_files_are_unaffected(self):
        self.commit({
            "README.md": "Repository documentation\n",
            "VERIFICATION.txt": "Verification evidence\n",
            "scripts/example.py": "print('hello')\n",
            "docs/architecture.md": "Architecture documentation\n",
        })

        result = self.run_checker()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
