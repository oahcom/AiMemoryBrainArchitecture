#!/usr/bin/env python3
"""Tests for the committed-HEAD CRLF line-ending gate."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CHECKER = (
    Path(__file__).resolve().parent
    / "ci"
    / "check_line_endings.py"
)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
    )


class LineEndingTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)

        git(self.repo, "init", "-q")

    def tearDown(self):
        self.tempdir.cleanup()

    def write_files(self, files):
        """Write fixture files as exact bytes."""
        for name, content in files.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)

    def commit(self, files):
        self.write_files(files)

        git(
            self.repo,
            "-c", "core.autocrlf=false",
            "add", "-A",
        )
        git(
            self.repo,
            "-c", "user.email=line-endings@example.invalid",
            "-c", "user.name=Line Ending Test",
            "commit", "-q", "-m", "test fixture",
        )

    def run_checker(self, cwd=None):
        return subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=cwd or self.repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True,
        )

    @staticmethod
    def output(result):
        return result.stdout + result.stderr

    def assert_result(self, result, expected_code):
        self.assertEqual(
            result.returncode,
            expected_code,
            msg=self.output(result),
        )

    def assert_output_contains(self, result, expected):
        self.assertIn(
            expected,
            self.output(result),
            msg=self.output(result),
        )

    def assert_no_error_annotation(self, result):
        self.assertNotIn(
            "::error::",
            self.output(result),
            msg=self.output(result),
        )

    def test_lf_only_file_passes(self):
        self.commit({
            "docs/readme.md": b"first line\nsecond line\n",
        })

        result = self.run_checker()

        self.assert_result(result, 0)
        self.assert_no_error_annotation(result)

    def test_crlf_file_fails_and_names_path(self):
        self.commit({
            "docs/crlf.md": b"first line\r\nsecond line\r\n",
        })

        result = self.run_checker()

        self.assert_result(result, 1)
        self.assert_output_contains(
            result,
            "::error::CRLF line endings in committed file 'docs/crlf.md'",
        )
        self.assert_output_contains(
            result,
            "2 CRLF sequences, 2 total lines",
        )

    def test_text_unset_exempts_frozen_prompt(self):
        self.commit({
            ".gitattributes": (
                b"frozen-prompt.md -text\n"
            ),
            "frozen-prompt.md": (
                b"first line\r\nsecond line\r\n"
            ),
        })

        result = self.run_checker()

        self.assert_result(result, 0)
        self.assert_no_error_annotation(result)

    def test_unlisted_extension_is_inspected(self):
        self.commit({
            "evidence.txt": b"first line\r\nsecond line\r\n",
        })

        result = self.run_checker()

        self.assert_result(result, 1)
        self.assert_output_contains(
            result,
            "::error::CRLF line endings in committed file 'evidence.txt'",
        )
        self.assert_output_contains(
            result,
            "2 CRLF sequences, 2 total lines",
        )

    def test_extensionless_text_blob_is_inspected(self):
        self.commit({
            "extensionless": b"first line\r\nsecond line\r\n",
        })

        result = self.run_checker()

        self.assert_result(result, 1)
        self.assert_output_contains(
            result,
            "::error::CRLF line endings in committed file 'extensionless'",
        )
        self.assert_output_contains(
            result,
            "2 CRLF sequences, 2 total lines",
        )


    def test_untracked_crlf_file_is_ignored(self):
        self.commit({
            "README.md": b"clean committed content\n",
        })

        untracked = self.repo / "untracked.md"
        untracked.write_bytes(b"untracked\r\ncontent\r\n")

        result = self.run_checker()

        self.assert_result(result, 0)
        self.assert_no_error_annotation(result)

    def test_mixed_line_endings_fail(self):
        self.commit({
            "docs/mixed.md": (
                b"first line\n"
                b"second line\r\n"
                b"third line\n"
            ),
        })

        result = self.run_checker()

        self.assert_result(result, 1)
        self.assert_output_contains(
            result,
            "::error::CRLF line endings in committed file 'docs/mixed.md'",
        )
        self.assert_output_contains(
            result,
            "1 CRLF sequences, 3 total lines",
        )

    def test_empty_file_passes(self):
        self.commit({
            "docs/empty.md": b"",
        })

        result = self.run_checker()

        self.assert_result(result, 0)
        self.assert_no_error_annotation(result)

    def test_non_git_directory_returns_inspection_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_checker(cwd=Path(directory))

        self.assert_result(result, 2)
        self.assert_output_contains(
            result,
            "::error::line-ending inspection incomplete:",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
