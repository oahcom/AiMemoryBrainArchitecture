#!/usr/bin/env python3
# scripts/ci/test_check_manifest_blob_pins.py
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
    return subprocess.run(
        ["git", *args],
        cwd=root,
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.decode().strip()


def commit_tree(root, files):
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(
            content if isinstance(content, bytes) else content.encode()
        )

    git(root, "add", ".")
    git(
        root,
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-m",
        "fixture",
    )
    return git(root, "rev-parse", "HEAD")


class BlobPinsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")

    def tearDown(self):
        self.tmp.cleanup()

    def run_gate(self, commit="HEAD"):
        p = subprocess.run(
            [
                sys.executable,
                str(GATE),
                "--root",
                str(self.root),
                "--commit",
                commit,
            ],
            text=True,
            capture_output=True,
        )
        return p.returncode, p.stdout, p.stderr

    def manifest(self, path, digest):
        return (
            "work_item_id: AID-2026-900\n"
            f"root: {path}\nroot_blob: \"{digest}\"\n"
        )

    @staticmethod
    def blob_sha(data):
        return hashlib.sha1(
            b"blob " + str(len(data)).encode() + b"\0" + data
        ).hexdigest()

    @staticmethod
    def prompt_sha(data):
        return hashlib.sha256(data).hexdigest()

    def test_valid_pin_is_silent_about_individual_pin(self):
        data = b"committed bytes\n"
        sha = self.blob_sha(data)

        commit = commit_tree(
            self.root,
            {
                "README.md": data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    self.manifest("README.md", sha),
            },
        )

        code, out, err = self.run_gate(commit)
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0",
            out,
        )
        self.assertNotIn("MISMATCH", out)

    def test_nested_authored_index_mirror_pin_is_checked(self):
        data = b"authored mirror bytes\n"
        wrong = "0" * 40

        commit_tree(
            self.root,
            {
                "docs/en/05-memory-runtime/README.md": data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "baseline_and_source_evidence:\n"
                        "  authored_indexes:\n"
                        "    - en_mirror: "
                        "docs/en/05-memory-runtime/README.md\n"
                        f"      en_mirror_blob: \"{wrong}\"\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(
            "MISMATCH authored_indexes[0].en_mirror",
            out,
        )
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)

    def test_changed_byte_is_rejected_with_declared_and_actual_digest(self):
        data = b"committed bytes\n"
        wrong = "0" * 40

        commit_tree(
            self.root,
            {
                "README.md": data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    self.manifest("README.md", wrong),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)

    def test_deleted_path_is_rejected_and_named(self):
        commit_tree(
            self.root,
            {
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    self.manifest("missing.md", "1" * 40),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("PATH_MISSING", out)
        self.assertIn("path=missing.md", out)

    def test_cross_commit_pin_reads_the_declared_source_commit(self):
        source_data = b"source revision\n"
        source = commit_tree(
            self.root,
            {"source.md": source_data},
        )
        source_sha = self.blob_sha(source_data)

        candidate = commit_tree(
            self.root,
            {
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "d_source_commit: " + source + "\n"
                        "d_source_blobs:\n"
                        f"  - 'source.md: {source_sha}'\n"
                    ),
            },
        )

        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_unavailable_cross_commit_is_incomplete_not_pass(self):
        commit_tree(
            self.root,
            {
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "d_source_commit: "
                        + "f" * 40
                        + "\n"
                        "d_source_blobs:\n"
                        "  - 'source.md: "
                        + "1" * 40
                        + "'\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        self.assertIn("INCOMPLETE", out)

    def test_prompt_sha256_and_byte_count_are_both_checked(self):
        data = b"prompt\n"

        commit_tree(
            self.root,
            {
                "prompt.md": data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "prompt:\n"
                        "  prompt_file: prompt.md\n"
                        f"  prompt_sha256: {self.prompt_sha(data)}\n"
                        f"  prompt_bytes: {len(data)}\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=2 ok=2 mismatch=0", out)

    def test_top_level_prompt_sha256_correct_digest_passes(self):
        data = b"top-level prompt\n"
        digest = self.prompt_sha(data)

        commit_tree(
            self.root,
            {
                "prompt.md": data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "work_item_id: AID-2026-900\n"
                        "prompt_file: prompt.md\n"
                        f"prompt_sha256: {digest}\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("prompt.top_level", out)
        self.assertIn("prompt_declared=1 prompt_compared=1", out)

    def test_top_level_prompt_sha256_wrong_digest_fails(self):
        data = b"top-level prompt\n"
        wrong = "0" * 64

        commit_tree(
            self.root,
            {
                "prompt.md": data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "work_item_id: AID-2026-900\n"
                        "prompt_file: prompt.md\n"
                        f"prompt_sha256: {wrong}\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH prompt.top_level", out)
        self.assertIn("path=prompt.md", out)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.prompt_sha(data)}", out)

    def test_top_level_prompt_sha256_missing_file_fails(self):
        wrong = "1" * 64

        commit_tree(
            self.root,
            {
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "work_item_id: AID-2026-900\n"
                        "prompt_file: missing-prompt.md\n"
                        f"prompt_sha256: {wrong}\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("PATH_MISSING", out)
        self.assertIn("prompt.top_level", out)
        self.assertIn("path=missing-prompt.md", out)
        self.assertIn("prompt_declared=1 prompt_compared=0", out)

    def test_nested_prompt_sha256_keeps_original_semantics(self):
        data = b"nested prompt\n"
        wrong = "0" * 64

        commit_tree(
            self.root,
            {
                "nested.md": data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "prompt:\n"
                        "  prompt_file: nested.md\n"
                        f"  prompt_sha256: {wrong}\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH prompt.nested", out)
        self.assertIn("path=nested.md", out)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.prompt_sha(data)}", out)

    def test_unknown_prompt_digest_field_fails_closed(self):
        commit_tree(
            self.root,
            {
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "work_item_id: AID-2026-900\n"
                        "prompt_digest: "
                        + "0" * 64
                        + "\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        self.assertIn("unrecognized prompt digest field", out)
        self.assertIn("prompt_digest", out)

    def test_prompt_coverage_assertion_rejects_uncompared_declaration(self):
        data = b"one comparable prompt\n"

        commit_tree(
            self.root,
            {
                "good.md": data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "work_item_id: AID-2026-900\n"
                        "prompt_file: good.md\n"
                        f"prompt_sha256: {self.prompt_sha(data)}\n"
                        "prompt:\n"
                        "  prompt_file: missing-nested.md\n"
                        f"  prompt_sha256: {'1' * 64}\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        self.assertIn(
            "PROMPT_COVERAGE declared=2 compared=1",
            out,
        )

    def test_top_level_prompt_uses_conventional_fallback_path(self):
        data = b"conventional prompt\n"
        digest = self.prompt_sha(data)

        commit_tree(
            self.root,
            {
                "14-ai-development/work-items/AID-2026-900/prompt-v1.md":
                    data,
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "work_item_id: AID-2026-900\n"
                        f"prompt_sha256: {digest}\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "prompt.top_level",
            out,
        )
        self.assertIn(
            "prompt_declared=1 prompt_compared=1",
            out,
        )

    def test_top_level_fallback_missing_file_fails(self):
        digest = "1" * 64

        commit_tree(
            self.root,
            {
                "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                    (
                        "work_item_id: AID-2026-900\n"
                        f"prompt_sha256: {digest}\n"
                    ),
            },
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("PATH_MISSING", out)
        self.assertIn(
            "14-ai-development/work-items/AID-2026-900/prompt-v1.md",
            out,
        )

    def test_empty_tree_is_incomplete(self):
        code, out, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("INCOMPLETE", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
