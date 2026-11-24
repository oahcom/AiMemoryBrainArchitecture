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

    def replace_blob(self, name, content):
        """Store raw bytes as the HEAD blob for ``name``.

        ``git add`` normalises a path whose ``text`` attribute is set, so a
        CRLF blob under a text path can only be produced by writing the
        object directly — which is how the real defect via #855 landed.
        """
        object_id = subprocess.run(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=self.repo,
            input=content,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.decode().strip()

        git(
            self.repo,
            "update-index",
            "--add",
            "--cacheinfo",
            f"100644,{object_id},{name}",
        )
        git(
            self.repo,
            "-c", "user.email=line-endings@example.invalid",
            "-c", "user.name=Line Ending Test",
            "commit", "-q", "-m", "replace blob",
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

    def test_crlf_gitattributes_is_reported(self):
        """The policy file itself is gated; a suffix list can never see it."""
        self.commit({
            ".gitattributes": b"* text=auto\n",
            "docs/readme.md": b"clean\n",
        })

        self.replace_blob(
            ".gitattributes",
            b"* text=auto\r\n*.md text eol=lf\r\n",
        )

        result = self.run_checker()

        # Assert the annotation before the exit code so a suffix-list
        # regression fails naming the path, not just the exit status.
        self.assert_output_contains(
            result,
            "::error::CRLF line endings in committed file '.gitattributes'",
        )
        self.assert_result(result, 1)
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
        # Only .gitattributes is left to inspect; the exempt path is skipped
        # instead of the gate going blind.
        self.assert_output_contains(result, "1 files inspected")

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

    def test_extensionless_text_attribute_with_lf_passes(self):
        self.commit({
            ".gitattributes": b"policy-file text\n",
            "policy-file": b"first line\nsecond line\n",
        })

        result = self.run_checker()

        self.assert_result(result, 0)
        self.assert_no_error_annotation(result)
        self.assert_output_contains(result, "2 files inspected")

    def test_extensionless_text_attribute_with_crlf_fails(self):
        self.commit({
            ".gitattributes": b"policy-file text\n",
            "policy-file": b"first line\nsecond line\n",
        })

        self.replace_blob(
            "policy-file",
            b"first line\r\nsecond line\r\n",
        )

        result = self.run_checker()

        self.assert_result(result, 1)
        self.assert_output_contains(
            result,
            "::error::CRLF line endings in committed file 'policy-file'",
        )

    def test_inspected_count_is_reported(self):
        """A gate that inspects nothing must not report success."""
        self.commit({
            "docs/readme.md": b"clean\n",
        })

        result = self.run_checker()

        self.assert_result(result, 0)
        self.assert_output_contains(
            result,
            "Line-ending check: 1 files inspected, "
            "0 binary skipped, 0 violations.",
        )

    def test_binary_content_is_skipped_and_counted(self):
        self.commit({
            "docs/readme.md": b"clean\n",
            "assets/payload.bin": b"\x00\x01\r\n\x02",
        })

        result = self.run_checker()

        self.assert_result(result, 0)
        self.assert_no_error_annotation(result)
        self.assert_output_contains(
            result,
            "1 files inspected, 1 binary skipped",
        )

    def test_binary_attribute_exempts_crlf_file(self):
        """The ``binary`` attribute is consulted alongside ``text``.

        ``binary`` sets ``-diff -merge -text``, so a later ``text=auto`` can
        leave ``text`` non-unset while ``binary`` is still ``set``. Only
        reading ``text`` would then flag a path Git calls binary.
        """
        self.commit({
            ".gitattributes": b"payload.dat binary\npayload.dat text=auto\n",
            "docs/readme.md": b"clean\n",
            "payload.dat": b"first line\nsecond line\n",
        })

        self.replace_blob(
            "payload.dat",
            b"first line\r\nsecond line\r\n",
        )

        result = self.run_checker()

        self.assert_result(result, 0)
        self.assert_no_error_annotation(result)
        # Exempt like -text: it never reaches the CRLF scan, so it is not
        # counted as content-sniffed binary either.
        self.assert_output_contains(result, "2 files inspected")

    def test_all_paths_exempt_is_an_inspection_error(self):
        """Every path opting out must not read as a clean run."""
        self.commit({
            ".gitattributes": b"* -text\n",
            "docs/readme.md": b"first line\r\nsecond line\r\n",
        })

        result = self.run_checker()

        self.assert_output_contains(
            result,
            "::error::line-ending inspection incomplete: "
            "no text blobs were inspected",
        )
        self.assert_result(result, 2)

    def test_empty_tree_is_an_inspection_error(self):
        git(
            self.repo,
            "-c", "user.email=line-endings@example.invalid",
            "-c", "user.name=Line Ending Test",
            "commit", "-q", "--allow-empty", "-m", "empty tree",
        )

        result = self.run_checker()

        self.assert_output_contains(
            result,
            "::error::line-ending inspection incomplete: "
            "HEAD tree contains no blobs to inspect",
        )
        self.assert_result(result, 2)

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
