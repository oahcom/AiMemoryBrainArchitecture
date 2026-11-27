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

    def test_nested_authored_index_mirror_pin_is_checked(self):
        data = b"authored mirror bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "docs/en/05-memory-runtime/README.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                ("baseline_and_source_evidence:\n"
                 "  authored_indexes:\n"
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
                self.manifest("README.md", wrong),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn(f"actual={self.blob_sha(data)}", out)
        print(out.strip())

    def test_deleted_path_is_rejected_and_named(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                self.manifest("missing.md", "1" * 40),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("PATH_MISSING", out)
        self.assertIn("path=missing.md", out)
        print(out.strip())

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
        print(out.strip())

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
        """Kills a resolver that pairs en_mirror_blob with another sibling path."""
        data_x = b"en mirror file X\n"
        data_y = b"neighbour file Y\n"
        digest_x = self.blob_sha(data_x)
        digest_y = self.blob_sha(data_y)
        manifest = (
            "work_item_id: AID-2026-900\n"
            "baseline_and_source_evidence:\n"
            "  authored_indexes:\n"
            "    - en_mirror: file-x.md\n"
            f"      en_mirror_blob: \"{digest_y}\"\n"
        )
        commit_tree(self.root, {
            "file-x.md": data_x,
            "file-y.md": data_y,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml": manifest,
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=1 ok=0 mismatch=1 path_missing=0 incomplete=0", out)
        self.assertIn(
            f"MISMATCH authored_indexes[0].en_mirror path=file-x.md "
            f"declared={digest_y} actual={digest_x}",
            out,
        )
        self.assertNotIn("path=file-y.md", out)

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
