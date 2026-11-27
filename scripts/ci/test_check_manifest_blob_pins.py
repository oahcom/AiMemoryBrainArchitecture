#!/usr/bin/env python3
"""Tests for committed-byte manifest blob-pin verification."""
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
GATE = HERE / "check_manifest_blob_pins.py"


def git(root, *args, data=None):
    return subprocess.run(["git", *args], cwd=root, input=data, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout.decode().strip()


def commit_tree(root, files):
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
    git(root, "add", ".")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "commit", "-m", "fixture")
    return git(root, "rev-parse", "HEAD")


class BlobPinsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")

    def tearDown(self):
        self.tmp.cleanup()

    def run_gate(self, commit="HEAD"):
        p = subprocess.run([sys.executable, str(GATE), "--root", str(self.root),
                            "--commit", commit], text=True, capture_output=True)
        return p.returncode, p.stdout, p.stderr

    def manifest(self, path, digest):
        return ("work_item_id: AID-2026-900\n"
                f"root: {path}\nroot_blob: \"{digest}\"\n")

    @staticmethod
    def blob_sha(data):
        return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

    def test_valid_pin_is_silent_about_individual_pin(self):
        data = b"committed bytes\n"
        sha = self.blob_sha(data)
        commit = commit_tree(self.root, {
            "README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                self.manifest("README.md", sha),
        })
        code, out, err = self.run_gate(commit)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)
        self.assertNotIn("MISMATCH", out)

    def test_changed_byte_is_rejected_with_declared_and_actual_digest(self):
        data = b"committed bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                self.manifest("README.md", wrong),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)

    def test_deleted_path_is_rejected_and_named(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                self.manifest("missing.md", "1" * 40),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("PATH_MISSING", out)
        self.assertIn("path=missing.md", out)

    def test_cross_commit_pin_reads_the_declared_source_commit(self):
        source_data = b"source revision\n"
        source = commit_tree(self.root, {"source.md": source_data})
        source_sha = self.blob_sha(source_data)
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("d_source_commit: " + source + "\n"
                 "d_source_blobs:\n"
                 f"  - 'source.md: {source_sha}'\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_unavailable_cross_commit_is_incomplete_not_pass(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("d_source_commit: " + "f" * 40 + "\n"
                 "d_source_blobs:\n  - 'source.md: " + "1" * 40 + "'\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        self.assertIn("INCOMPLETE", out)

    def test_prompt_sha256_and_byte_count_are_both_checked(self):
        data = b"prompt\n"
        commit_tree(self.root, {
            "prompt.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("prompt:\n  prompt_file: prompt.md\n"
                 f"  prompt_sha256: {hashlib.sha256(data).hexdigest()}\n"
                 f"  prompt_bytes: {len(data)}\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=2 ok=2 mismatch=0", out)

    def test_empty_tree_is_incomplete(self):
        code, out, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("INCOMPLETE", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
