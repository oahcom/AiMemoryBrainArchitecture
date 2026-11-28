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
                f"root: README.md\nroot_blob: \"{sha}\"\n",
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
                 f"      en_mirror_blob: \"{wrong}\"\n"),
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
                f"root: README.md\nroot_blob: \"{wrong}\"\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)
        print(out.strip())

    def test_deleted_path_is_rejected_and_named(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"root: missing.md\nroot_blob: \"{'1' * 40}\"\n",
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
                f"source_blobs:\n  - path: source.md\n    sha: \"{self.blob_sha(data)}\"\nbase_commit: {source}\n",
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_unavailable_cross_commit_is_incomplete_not_pass(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                f"source_blobs:\n  - path: source.md\n    sha: \"{'1' * 40}\"\nbase_commit: {'f' * 40}\n",
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
                f"prompt_version: v2\nprompt_sha256: \"{good}\"\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        manifest = self.root / "14-ai-development/work-items/AID-2026-900/manifest.yaml"
        manifest.write_text(f"prompt_version: v2\nprompt_sha256: \"{'0' * 64}\"\n")
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
                 f"    source_blob_sha: \"{self.blob_sha(src)}\"\n"
                 f"    source_commit_sha: \"{source_commit}\"\n"
                 "    translation_path: en.md\n"
                 f"    translation_blob_sha: \"{self.blob_sha(trans)}\"\n"
                 f"    translation_commit_sha: \"{translation_commit}\"\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_source_selected_files_without_frontmatter_locator_are_unresolved(self):
        data = b"restored file\n"
        source_commit = commit_tree(self.root, {"file.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source:\n"
                 f"  head_sha: \"{source_commit}\"\n"
                 "  selected_source_files:\n"
                 "    - path: file.md\n"
                 f"      source_blob_sha: \"{self.blob_sha(data)}\"\n"
                 f"      restored_blob_sha: \"{self.blob_sha(data)}\"\n"
                 f"      frontmatter_blob_sha: \"{self.blob_sha(b'frontmatter')}\"\n"),
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
                f"unregistered_evidence_blob_sha: \"{'a' * 40}\"\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("UNRESOLVED(missing field locator)", out)

    def test_missing_source_translation_commit_is_incomplete(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source_translation_pairs:\n"
                 "  - source_path: source.md\n"
                 f"    source_blob_sha: \"{'a' * 40}\"\n"
                 "    source_commit_sha: NOT_RECORDED\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("UNRESOLVED(commit locator)", out)

    def test_generic_blob_field_uses_sibling_path_and_source_commit(self):
        data = b"generic pinned bytes\n"
        source = commit_tree(self.root, {"generic.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("generic_evidence:\n"
                 "  path: generic.md\n"
                 f"  evidence_blob_sha: \"{self.blob_sha(data)}\"\n"
                 f"  source_commit_sha: \"{source}\"\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)

    def test_nested_gate_a_reconstruction_mirror_pins_are_checked(self):
        data = b"nested mirror\n"
        source = commit_tree(self.root, {"mirror.md": data})
        wrong = "0" * 40
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("baseline_and_source_evidence:\n"
                 "  gate_a_reconstruction:\n"
                 "    - source_commit: " + source + "\n"
                 "      en_mirror: mirror.md\n"
                 f"      en_mirror_blob: \"{wrong}\"\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH gate_a_reconstruction[0].en_mirror", out)

    def test_empty_declared_digest_is_not_dropped(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                "root: README.md\nroot_blob: ''\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=1", out)
        self.assertIn("invalid Git blob SHA-1 declaration", out)

    def test_nested_d_source_blobs_use_nested_source_commit(self):
        data = b"nested D source\n"
        source = commit_tree(self.root, {"nested.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("baseline_and_source_evidence:\n"
                 f"  d_source_commit: {source}\n"
                 "  d_source_blobs:\n"
                 f"    - 'nested.md: {self.blob_sha(data)}'\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)

    def test_owner_ruling_pointer_pins_use_artifact_not_pointer_document(self):
        old = b"superseded artifact\n"
        current = b"current artifact\n"
        old_sha, current_sha = self.blob_sha(old), self.blob_sha(current)
        commit_tree(self.root, {
            "old.md": old,
            "current.md": current,
            "pointer.md": b"pointer metadata\n",
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("owner_ruling:\n"
                 "  superseded_artifact: old.md\n"
                 f"  superseded_blob: {old_sha}\n"
                 "  current_artifact: current.md\n"
                 f"  current_blob: {current_sha}\n"
                 "reconciliation:\n"
                 "  pointers_changed:\n"
                 "    - document: pointer.md\n"
                 f"      before_blob: {old_sha}\n"
                 f"      after_blob: {current_sha}\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=4 ok=4 mismatch=0", out)

    def test_source_baseline_digest_only_pin_resolves_unique_blob_oid_in_commit_tree(self):
        data = b"source baseline artifact\n"
        source = commit_tree(self.root, {"baseline.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source_baseline:\n"
                 f"  main: {source}\n"
                 f"  artifact_blob: {self.blob_sha(data)}\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)

    def test_prompt_snapshot_relative_file_locator_is_resolved_from_manifest_directory(self):
        data = b"prompt snapshot\n"
        sha256 = hashlib.sha256(data).hexdigest()
        manifest_path = "14-ai-development/work-items/AID-2026-900/manifest.yaml"
        prompt_path = "14-ai-development/work-items/AID-2026-900/prompt-v1.md"
        commit_tree(self.root, {
            prompt_path: data,
            manifest_path:
                ("prompt:\n"
                 "  snapshot_file: prompt-v1.md\n"
                 f"  snapshot_git_blob_sha: \"{self.blob_sha(data)}\"\n"
                 f"  snapshot_sha256: {sha256}\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=2 ok=2", out)

    def test_session_prompt_pin_uses_explicit_historical_commit_not_candidate_tree(self):
        historical = b"historical prompt bytes\n"
        current = b"edited prompt bytes\n"
        historical_commit = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/prompt-v1.md": historical,
        })
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/prompt-v1.md": current,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("session_evidence:\n"
                 "  - executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-900/prompt-v1.md\n"
                 f"    executed_prompt_sha256: \"{hashlib.sha256(historical).hexdigest()}\"\n"
                 f"    executed_prompt_commit_sha: \"{historical_commit}\"\n"
                 f"    executed_prompt_bytes: {len(historical)}\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=2 ok=2 mismatch=0", out)

    def test_session_prompt_pin_without_commit_uses_candidate_tree_and_rejects_historical_digest(self):
        historical = b"historical prompt bytes\n"
        current = b"edited prompt bytes\n"
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/prompt-v1.md": historical,
        })
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/prompt-v1.md": current,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("session_evidence:\n"
                 "  - executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-900/prompt-v1.md\n"
                 f"    executed_prompt_sha256: \"{hashlib.sha256(historical).hexdigest()}\"\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH session_evidence[0].executed_prompt_snapshot_file", out)
    def test_source_path_branch_head_blob_sha_shape(self):
        data = b"source path pin\n"
        source = commit_tree(self.root, {"source.md": data})
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("source:\n"
                 f"  branch_head: {source}\n"
                 "  source_path: source.md\n"
                 f"  source_blob_sha: \"{self.blob_sha(data)}\"\n"),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)

    def test_prompt_original_payload_without_dedicated_file_is_unresolved(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/prompt-v2.md": b"ordinary prompt file\n",
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("prompt_file: 14-ai-development/work-items/AID-2026-900/prompt-v2.md\n"
                 f"prompt_original_payload_sha256: {'a' * 64}\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("no dedicated prompt_original_payload_file locator", out)

    def test_identical_incomplete_fields_in_two_manifests_keep_distinct_provenance(self):
        candidate = commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                "prompt_sha256: NOT_VERIFIED\n",
            "14-ai-development/work-items/AID-2026-901/manifest.yaml":
                "prompt_sha256: NOT_VERIFIED\n",
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 1, out + err)
        self.assertIn("manifest=14-ai-development/work-items/AID-2026-900/manifest.yaml", out)
        self.assertIn("manifest=14-ai-development/work-items/AID-2026-901/manifest.yaml", out)

    def test_empty_tree_is_incomplete(self):
        code, out, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertIn("INCOMPLETE", err)

    def test_unlocated_blob_cannot_borrow_same_digest_from_another_field(self):
        data = b"shared digest must not confer a locator\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {
            "file.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("root: file.md\n"
                 f"root_blob: \"{digest}\"\n"
                 f"unregistered_source_blob: \"{digest}\"\n"),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=2", out)
        self.assertIn("ok=1", out)
        self.assertIn("INCOMPLETE UNRESOLVED(missing field locator)", out)
        self.assertIn("field=manifest.unregistered_source_blob", out)
    def test_neighbouring_digest_key_does_not_verify_target_pair(self):
        """Kills a resolver that reads pair A's digest from pair B's sibling key."""
        data_a = b"pair A committed bytes\n"
        data_b = b"pair B committed bytes\n"
        digest_a = self.blob_sha(data_a)
        digest_b = self.blob_sha(data_b)
        wrong = "0" * 40
        manifest = (
            "work_item_id: AID-2026-900\n"
            "baseline_and_source_evidence:\n"
            "  authored_indexes:\n"
            "    - root: pair-a.md\n"
            f"      root_blob: \"{wrong}\"\n"
            "      en_mirror: pair-b.md\n"
            f"      en_mirror_blob: \"{digest_a}\"\n"
        )
        commit_tree(self.root, {
            "pair-a.md": data_a,
            "pair-b.md": data_b,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml": manifest,
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=2 ok=0 mismatch=2 path_missing=0 incomplete=0", out)
        self.assertIn(
            f"MISMATCH authored_indexes[0].root path=pair-a.md "
            f"declared={wrong} actual={digest_a}",
            out,
        )
        self.assertIn(
            f"MISMATCH authored_indexes[0].en_mirror path=pair-b.md "
            f"declared={digest_a} actual={digest_b}",
            out,
        )

    def test_path_key_identity_uses_en_mirror_path_not_neighbour_file(self):
        """Kills a resolver that prefers root when resolving en_mirror."""
        data_root = b"root file bytes\n"
        data_mirror = b"en mirror file bytes\n"
        digest_root = self.blob_sha(data_root)
        digest_mirror = self.blob_sha(data_mirror)
        manifest = (
            "work_item_id: AID-2026-900\n"
            "baseline_and_source_evidence:\n"
            "  authored_indexes:\n"
            "    - root: file-root.md\n"
            f"      root_blob: \"{digest_root}\"\n"
            "      en_mirror: file-en.md\n"
            f"      en_mirror_blob: \"{digest_root}\"\n"
        )
        commit_tree(self.root, {
            "file-root.md": data_root,
            "file-en.md": data_mirror,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml": manifest,
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0", out)
        self.assertIn(
            f"MISMATCH authored_indexes[0].en_mirror path=file-en.md "
            f"declared={digest_root} actual={self.blob_sha(data_mirror)}",
            out,
        )
        self.assertNotIn("MISMATCH authored_indexes[0].root", out)
        self.assertNotIn("path=file-root.md declared=", out)

    def test_cross_identity_isolation_reports_only_the_wrong_pin(self):
        """Kills a resolver that reuses one identity's digest while checking another."""
        data_a = b"correct identity A\n"
        data_b = b"wrong identity B\n"
        digest_a = self.blob_sha(data_a)
        wrong = "0" * 40
        manifest = (
            "work_item_id: AID-2026-900\n"
            "baseline_and_source_evidence:\n"
            "  authored_indexes:\n"
            "    - root: identity-a.md\n"
            f"      root_blob: \"{digest_a}\"\n"
            "    - root: identity-b.md\n"
            f"      root_blob: \"{wrong}\"\n"
        )
        commit_tree(self.root, {
            "identity-a.md": data_a,
            "identity-b.md": data_b,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml": manifest,
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0", out)
        self.assertIn(
            f"MISMATCH authored_indexes[1].root path=identity-b.md "
            f"declared={wrong} actual={self.blob_sha(data_b)}",
            out,
        )
        self.assertNotIn("MISMATCH authored_indexes[0].root", out)

    def test_every_enumerated_path_digest_pair_is_validated(self):
        """Kills omissions or path/digest mis-associations in the checker's enumerated families."""
        reconstructed_data = b"historical reconstructed bytes\n"
        source_data = b"historical D source bytes\n"
        source_commit = commit_tree(self.root, {
            "historical/reconstructed.md": reconstructed_data,
            "historical/source.md": source_data,
        })

        files = {
            "top-root.md": b"top root\n",
            "top-en.md": b"top english mirror\n",
            "top-zh.md": b"top chinese mirror\n",
            "auth-root.md": b"authored root\n",
            "auth-en.md": b"authored english mirror\n",
            "auth-zh.md": b"authored chinese mirror\n",
            "related-path.md": b"related evidence\n",
            "related-en.md": b"related english mirror\n",
            "related-zh.md": b"related chinese mirror\n",
            "execution-evidence.md": b"execution evidence\n",
            "prompt.md": b"prompt snapshot\n",
            "session-prompt.md": b"session prompt snapshot\n",
        }

        def sha(name):
            return self.blob_sha(files[name])

        prompt_data = files["prompt.md"]
        session_data = files["session-prompt.md"]
        document = {
            "work_item_id": "AID-2026-900",
            "root": "top-root.md",
            "root_blob": sha("top-root.md"),
            "en_mirror": "top-en.md",
            "en_mirror_blob": sha("top-en.md"),
            "zh_cn_mirror": "top-zh.md",
            "zh_cn_mirror_blob": sha("top-zh.md"),
            "baseline_and_source_evidence": {
                "authored_indexes": [
                    {
                        "root": "auth-root.md",
                        "root_blob": sha("auth-root.md"),
                        "en_mirror": "auth-en.md",
                        "en_mirror_blob": sha("auth-en.md"),
                        "zh_cn_mirror": "auth-zh.md",
                        "zh_cn_mirror_blob": sha("auth-zh.md"),
                    }
                ]
            },
            "related_evidence": [
                {
                    "path": "related-path.md",
                    "blob": sha("related-path.md"),
                    "en_mirror": "related-en.md",
                    "en_mirror_blob": sha("related-en.md"),
                    "zh_cn_mirror": "related-zh.md",
                    "zh_cn_mirror_blob": sha("related-zh.md"),
                }
            ],
            "gate_a_reconstruction": [
                {
                    "root": "historical/reconstructed.md",
                    "reconstructed_root_blob": self.blob_sha(reconstructed_data),
                    "source_commit": source_commit,
                }
            ],
            "evidence_file": "execution-evidence.md",
            "evidence_blob": sha("execution-evidence.md"),
            "d_source_commit": source_commit,
            "d_source_blobs": [
                "historical/source.md: " + self.blob_sha(source_data)
            ],
            "prompt": {
                "prompt_file": "prompt.md",
                "prompt_sha256": hashlib.sha256(prompt_data).hexdigest(),
                "prompt_bytes": len(prompt_data),
            },
            "session_evidence": [
                {
                    "executed_prompt_snapshot_file": "session-prompt.md",
                    "executed_prompt_sha256": hashlib.sha256(session_data).hexdigest(),
                    "executed_prompt_bytes": len(session_data),
                }
            ],
        }
        candidate_files = dict(files)
        candidate_files[
            "14-ai-development/work-items/AID-2026-900/manifest.yaml"
        ] = yaml.safe_dump(document, sort_keys=False)
        commit_tree(self.root, candidate_files)

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=16 ok=16 mismatch=0 path_missing=0 incomplete=0",
            out,
        )
        self.assertNotIn("MISMATCH", out)
        self.assertNotIn("INCOMPLETE", out)

    def test_related_evidence_mirror_pair_substitution_is_named(self):
        """Kills a resolver that swaps both related-evidence mirror identities."""
        data_en = b"related English mirror bytes\n"
        data_zh = b"related Chinese mirror bytes\n"
        digest_en = self.blob_sha(data_en)
        digest_zh = self.blob_sha(data_zh)
        document = {
            "work_item_id": "AID-2026-900",
            "related_evidence": [
                {
                    "en_mirror": "related-en.md",
                    "en_mirror_blob": digest_zh,
                    "zh_cn_mirror": "related-zh.md",
                    "zh_cn_mirror_blob": digest_zh,
                }
            ],
        }
        commit_tree(self.root, {
            "related-en.md": data_en,
            "related-zh.md": data_zh,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump(document, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0", out)
        self.assertIn(
            f"MISMATCH related_evidence[0].en_mirror path=related-en.md "
            f"declared={digest_zh} actual={digest_en}",
            out,
        )
        self.assertNotIn("MISMATCH related_evidence[0].zh_cn_mirror", out)
        self.assertNotIn("MISMATCH related_evidence[0].en_mirror path=related-zh.md", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
