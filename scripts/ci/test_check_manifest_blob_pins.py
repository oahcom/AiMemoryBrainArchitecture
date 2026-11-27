#!/usr/bin/env python3
"""Tests for committed-byte manifest blob-pin verification and discovery."""
import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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
        "commit", "--allow-empty", "-m", "fixture")
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

    @staticmethod
    def blob_sha(data):
        return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

    def test_valid_root_pin(self):
        data = b"committed bytes\n"
        sha = self.blob_sha(data)
        commit = commit_tree(self.root, {
            "README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"root: README.md\nroot_blob: {sha}\n",
        })
        code, out, err = self.run_gate(commit)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_nested_authored_index_mirror_pin_is_checked(self):
        data = b"authored mirror bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "docs/en/05-memory-runtime/README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("baseline_and_source_evidence:\n  authored_indexes:\n"
                 "    - en_mirror: docs/en/05-memory-runtime/README.md\n"
                 f"      en_mirror_blob: {wrong}\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH authored_indexes[0].en_mirror", out)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)

    def test_changed_byte_is_rejected_with_declared_and_actual_digest(self):
        data = b"committed bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"root: README.md\nroot_blob: {wrong}\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)
        print(out.strip())

    def test_deleted_path_is_rejected_and_named(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"root: missing.md\nroot_blob: {'1' * 40}\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("PATH_MISSING", out)
        self.assertIn("path=missing.md", out)
        print(out.strip())

    def test_cross_commit_pin_reads_declared_source_commit(self):
        data = b"source revision\n"
        source = commit_tree(self.root, {"source.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"source_blobs:\n  - path: source.md\n    sha: {self.blob_sha(data)}\nbase_commit: {source}\n",
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_unavailable_cross_commit_is_incomplete_not_pass(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"source_blobs:\n  - path: source.md\n    sha: {'1' * 40}\nbase_commit: {'f' * 40}\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("UNRESOLVED(commit unavailable)", out)
        print(out.strip())

    def test_top_level_prompt_sha256_is_checked_and_mutation_fails(self):
        data = b"prompt version two\n"
        good = hashlib.sha256(data).hexdigest()
        path = "14-ai-development/work-items/AID-2026-900/prompt-v2.md"
        commit_tree(self.root, {
            path: data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"prompt_version: v2\nprompt_sha256: {good}\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        manifest = self.root / "14-ai-development/work-items/AID-2026-900/manifest.yaml"
        manifest.write_text(f"prompt_version: v2\nprompt_sha256: {'0' * 64}\n")
        git(self.root, "add", ".")
        git(self.root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
            "commit", "-m", "mutate top-level prompt pin")
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH prompt_sha256(top-level)", out)
        self.assertIn(f"declared={'0' * 64}", out)
        print(out.strip())

    def test_source_translation_pairs_use_each_declared_commit(self):
        src = b"source bytes\n"
        source_commit = commit_tree(self.root, {"src.md": src})
        trans = b"translation bytes\n"
        translation_commit = commit_tree(self.root, {"en.md": trans})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source_translation_pairs:\n"
                 "  - source_path: src.md\n"
                 f"    source_blob_sha: {self.blob_sha(src)}\n"
                 f"    source_commit_sha: {source_commit}\n"
                 "    translation_path: en.md\n"
                 f"    translation_blob_sha: {self.blob_sha(trans)}\n"
                 f"    translation_commit_sha: {translation_commit}\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_source_selected_files_without_frontmatter_locator_are_unresolved(self):
        data = b"restored file\n"
        source_commit = commit_tree(self.root, {"file.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source:\n"
                 f"  head_sha: {source_commit}\n"
                 "  selected_source_files:\n"
                 "    - path: file.md\n"
                 f"      source_blob_sha: {self.blob_sha(data)}\n"
                 f"      restored_blob_sha: {self.blob_sha(data)}\n"
                 f"      frontmatter_blob_sha: {self.blob_sha(b'frontmatter')}\n"),
            "file.md": data,
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 1, out + err)
        self.assertIn("UNRESOLVED(source.selected_source_files[0].frontmatter_blob_sha blob locator)", out)

    def test_source_files_blob_shape_is_checked(self):
        data = b"source file\n"
        source = commit_tree(self.root, {"source.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source:\n"
                 f"  head: {source}\n"
                 "  files:\n"
                 "    - path: source.md\n"
                 f"      blob: {self.blob_sha(data)}\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_unregistered_digest_field_fails_closed(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"unregistered_evidence_blob_sha: {'a' * 40}\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("UNRESOLVED(unregistered digest field)", out)

    def test_missing_source_translation_commit_is_incomplete(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source_translation_pairs:\n"
                 "  - source_path: source.md\n"
                 f"    source_blob_sha: {'a' * 40}\n"
                 "    source_commit_sha: NOT_RECORDED\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("UNRESOLVED(commit locator)", out)

    def test_generic_blob_field_uses_sibling_path_and_source_commit(self):
        data = b"generic pinned bytes\\n"
        source = commit_tree(self.root, {"generic.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("generic_evidence:\\n"
                 "  path: generic.md\\n"
                 f"  evidence_blob_sha: {self.blob_sha(data)}\\n"
                 f"  source_commit_sha: {source}\\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)

    def test_nested_gate_a_reconstruction_mirror_pins_are_checked(self):
        data = b"nested mirror\\n"
        source = commit_tree(self.root, {"mirror.md": data})
        wrong = "0" * 40
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("baseline_and_source_evidence:\\n"
                 "  gate_a_reconstruction:\\n"
                 "    - source_commit: " + source + "\\n"
                 "      en_mirror: mirror.md\\n"
                 f"      en_mirror_blob: {wrong}\\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH gate_a_reconstruction[0].en_mirror", out)

    def test_empty_declared_digest_is_not_dropped(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                "root: README.md\\nroot_blob: ''\\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=1", out)
        self.assertIn("invalid Git blob SHA-1 declaration", out)

    def test_nested_d_source_blobs_use_nested_source_commit(self):
        data = b"nested D source\\n"
        source = commit_tree(self.root, {"nested.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("baseline_and_source_evidence:\\n"
                 f"  d_source_commit: {source}\\n"
                 "  d_source_blobs:\\n"
                 f"    - 'nested.md: {self.blob_sha(data)}'\\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)

    def test_owner_ruling_pointer_pins_use_artifact_not_pointer_document(self):
        old = b"superseded artifact\\n"
        current = b"current artifact\\n"
        old_sha, current_sha = self.blob_sha(old), self.blob_sha(current)
        commit_tree(self.root, {
            "old.md": old,
            "current.md": current,
            "pointer.md": b"pointer metadata\\n",
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("owner_ruling:\\n"
                 "  superseded_artifact: old.md\\n"
                 f"  superseded_blob: {old_sha}\\n"
                 "  current_artifact: current.md\\n"
                 f"  current_blob: {current_sha}\\n"
                 "reconciliation:\\n"
                 "  pointers_changed:\\n"
                 "    - document: pointer.md\\n"
                 f"      before_blob: {old_sha}\\n"
                 f"      after_blob: {current_sha}\\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=4 ok=4 mismatch=0", out)

    def test_source_baseline_digest_only_pin_resolves_unique_blob_oid_in_commit_tree(self):
        data = b"source baseline artifact\\n"
        source = commit_tree(self.root, {"baseline.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source_baseline:\\n"
                 f"  main: {source}\\n"
                 f"  artifact_blob: {self.blob_sha(data)}\\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)

    def test_prompt_snapshot_relative_file_locator_is_resolved_from_manifest_directory(self):
        data = b"prompt snapshot\\n"
        sha256 = hashlib.sha256(data).hexdigest()
        manifest_path = "14-ai-development/work-items/AID-2026-900/manifest.yaml"
        prompt_path = "14-ai-development/work-items/AID-2026-900/prompt-v1.md"
        commit_tree(self.root, {
            prompt_path: data,
            manifest_path:
                ("prompt:\\n"
                 "  snapshot_file: prompt-v1.md\\n"
                 f"  snapshot_git_blob_sha: {self.blob_sha(data)}\\n"
                 f"  snapshot_sha256: {sha256}\\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=2 ok=2", out)

    def test_source_path_branch_head_blob_sha_shape(self):
        data = b"source path pin\\n"
        source = commit_tree(self.root, {"source.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source:\\n"
                 f"  branch_head: {source}\\n"
                 "  source_path: source.md\\n"
                 f"  source_blob_sha: {self.blob_sha(data)}\\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)

    def test_prompt_original_payload_without_dedicated_file_is_unresolved(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/prompt-v2.md": b"ordinary prompt file\\n",
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("prompt_file: 14-ai-development/work-items/AID-2026-900/prompt-v2.md\\n"
                 f"prompt_original_payload_sha256: {'a' * 64}\\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("no dedicated prompt_original_payload_file locator", out)

    def test_empty_tree_is_incomplete(self):
        code, out, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("INCOMPLETE", err)

if __name__ == "__main__":
    unittest.main(verbosity=2)
