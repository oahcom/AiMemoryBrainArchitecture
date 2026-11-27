from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from blob_pin_scope import (
    NoScope,
    Scope,
    ScopeUnresolvable,
    derive_scope,
    digest_of,
    resolve_bytes,
)


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode:
        raise AssertionError(proc.stderr)
    return proc.stdout.strip()


def make_repo() -> tuple[tempfile.TemporaryDirectory, Path, str]:
    temporary = tempfile.TemporaryDirectory()
    root = Path(temporary.name)

    git(root, "init")
    git(root, "config", "user.name", "Blob Pin Tests")
    git(root, "config", "user.email", "blob-pin-tests@example.invalid")

    (root / "manifest-dir").mkdir()
    (root / "manifest-dir" / "source.txt").write_bytes(b"first version\n")
    git(root, "add", ".")
    git(root, "commit", "-m", "first")
    first_commit = git(root, "rev-parse", "HEAD")

    return temporary, root, first_commit


class DeriveScopeTests(unittest.TestCase):
    def test_commit_sha_sibling_selects_commit_scope(self):
        sha = "a" * 40
        scope = derive_scope(
            {"source_blob_sha": "b" * 40, "source_commit_sha": sha},
            "source_blob_sha",
            "manifest-dir",
        )
        self.assertEqual(scope.kind, "commit")
        self.assertEqual(scope.commit_sha, sha)

    def test_commit_sibling_selects_commit_scope(self):
        sha = "c" * 40
        scope = derive_scope(
            {"source_blob_sha": "b" * 40, "source_commit": sha},
            "source_blob_sha",
            "manifest-dir",
        )
        self.assertEqual(scope.kind, "commit")
        self.assertEqual(scope.commit_sha, sha)

    def test_short_commit_sha_is_no_scope(self):
        with self.assertRaises(NoScope):
            derive_scope(
                {
                    "source_blob_sha": "b" * 40,
                    "source_commit_sha": "abcdef1",
                    "source_path": "source.txt",
                },
                "source_blob_sha",
                "manifest-dir",
            )

    def test_sibling_path_selects_candidate_scope(self):
        scope = derive_scope(
            {"source_blob_sha": "b" * 40, "source_path": "source.txt"},
            "source_blob_sha",
            "manifest-dir",
        )
        self.assertEqual(scope.kind, "candidate")
        self.assertEqual(scope.content_ref, "manifest-dir")

    def test_non_sibling_path_does_not_select_scope(self):
        with self.assertRaises(NoScope):
            derive_scope(
                {
                    "source_blob_sha": "b" * 40,
                    "translation_path": "translation.txt",
                },
                "source_blob_sha",
                "manifest-dir",
            )

    def test_no_commit_or_path_is_no_scope(self):
        with self.assertRaises(NoScope):
            derive_scope({"source_blob_sha": "b" * 40}, "source_blob_sha", ".")

    def test_empty_sibling_path_is_no_scope(self):
        with self.assertRaises(NoScope):
            derive_scope(
                {"source_blob_sha": "b" * 40, "source_path": "  "},
                "source_blob_sha",
                "manifest-dir",
            )


class ResolveBytesTests(unittest.TestCase):
    def test_commit_scope_with_missing_commit_is_unresolvable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            scope = Scope(kind="commit", commit_sha="f" * 40)
            with self.assertRaises(ScopeUnresolvable):
                resolve_bytes(root, scope, "missing.txt")

    def test_content_scope_is_unresolvable(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ScopeUnresolvable):
                resolve_bytes(
                    Path(temporary),
                    Scope(kind="content", content_ref="some-content-ref"),
                    "source.txt",
                )

    def test_candidate_reads_head_tree(self):
        temporary, root, first_commit = make_repo()
        self.addCleanup(temporary.cleanup)

        (root / "manifest-dir" / "source.txt").write_bytes(b"candidate version\n")
        git(root, "add", ".")
        git(root, "commit", "-m", "candidate")

        scope = Scope(kind="candidate", content_ref="manifest-dir")
        self.assertEqual(
            resolve_bytes(root, scope, "source.txt"),
            b"candidate version\n",
        )
        self.assertNotEqual(git(root, "rev-parse", "HEAD"), first_commit)

    def test_commit_reads_the_declared_commit_tree(self):
        temporary, root, first_commit = make_repo()
        self.addCleanup(temporary.cleanup)

        (root / "manifest-dir" / "source.txt").write_bytes(b"later version\n")
        git(root, "add", ".")
        git(root, "commit", "-m", "later")

        scope = Scope(
            kind="commit",
            commit_sha=first_commit,
            content_ref="manifest-dir",
        )
        self.assertEqual(
            resolve_bytes(root, scope, "source.txt"),
            b"first version\n",
        )

    def test_missing_path_is_unresolvable(self):
        temporary, root, _ = make_repo()
        self.addCleanup(temporary.cleanup)

        scope = Scope(kind="candidate", content_ref="manifest-dir")
        with self.assertRaises(ScopeUnresolvable):
            resolve_bytes(root, scope, "does-not-exist.txt")


class DigestTests(unittest.TestCase):
    def test_sha256_normalizes_crlf_to_lf(self):
        self.assertEqual(
            digest_of("sha256", b"a\r\nb"),
            digest_of("sha256", b"a\nb"),
        )

    def test_git_blob_sha1_matches_git_object_format(self):
        data = b"sample\n"
        expected = hashlib.sha1(
            b"blob " + str(len(data)).encode("ascii") + b"\0" + data
        ).hexdigest()
        self.assertEqual(digest_of("git-blob-sha1", data), expected)

    def test_byte_length(self):
        self.assertEqual(digest_of("byte-length", b"abc"), "3")


if __name__ == "__main__":
    unittest.main()
