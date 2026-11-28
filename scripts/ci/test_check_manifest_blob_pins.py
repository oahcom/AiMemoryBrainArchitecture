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
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
    git(root, "add", ".")
    git(
        root,
        "-c", "user.name=Test",
        "-c", "user.email=test@example.invalid",
        "commit", "-m", "fixture",
    )
    return git(root, "rev-parse", "HEAD")


class BlobPinsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")

    def tearDown(self):
        self.tmp.cleanup()

    def run_gate(self, commit="HEAD", *extra_args):
        p = subprocess.run(
            [
                sys.executable,
                str(GATE),
                "--root",
                str(self.root),
                "--commit",
                commit,
                *extra_args,
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

    def write_manifest(self, document):
        path = self.root / "14-ai-development/work-items/AID-2026-900/manifest.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

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
                (
                    "baseline_and_source_evidence:\n"
                    "  authored_indexes:\n"
                    "    - en_mirror: docs/en/05-memory-runtime/README.md\n"
                    f"      en_mirror_blob: \"{wrong}\"\n"
                ),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("MISMATCH authored_indexes[0].en_mirror", out)
        self.assertIn(f"declared={wrong}", out)
        self.assertIn("actual=not-found-in-reachable-history", out)

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
                (
                    "d_source_commit: " + source + "\n"
                    "d_source_blobs:\n"
                    f"  - 'source.md: {source_sha}'\n"
                ),
        })
        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)

    def test_unavailable_cross_commit_is_incomplete_not_pass(self):
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                (
                    "d_source_commit: " + "f" * 40 + "\n"
                    "d_source_blobs:\n  - 'source.md: " + "1" * 40 + "'\n"
                ),
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
                (
                    "prompt:\n  prompt_file: prompt.md\n"
                    f"  prompt_sha256: {hashlib.sha256(data).hexdigest()}\n"
                    f"  prompt_bytes: {len(data)}\n"
                ),
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
            f"declared={wrong} actual=not-found-in-reachable-history",
            out,
        )
        self.assertIn(
            f"MISMATCH authored_indexes[0].en_mirror path=pair-b.md "
            f"declared={digest_a} actual=not-found-in-reachable-history",
            out,
        )

    def test_path_key_identity_uses_en_mirror_path_not_neighbour_file(self):
        """Kills a resolver that prefers root when resolving en_mirror."""
        data_root = b"root file bytes\n"
        data_mirror = b"en mirror file bytes\n"
        digest_root = self.blob_sha(data_root)
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
            f"declared={digest_root} actual=not-found-in-reachable-history",
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
            f"declared={wrong} actual=not-found-in-reachable-history",
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
                    "reference_mode": "current",
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
                    "reference_mode": "current",
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

    def test_authored_index_historical_pin_survives_current_rewrite(self):
        original = b"authored index original bytes\n"
        original_sha = self.blob_sha(original)
        commit_tree(self.root, {"authored.md": original})
        self.write_manifest({
            "work_item_id": "AID-2026-900",
            "baseline_and_source_evidence": {
                "authored_indexes": [
                    {"root": "authored.md", "root_blob": original_sha}
                ]
            },
        })
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                (self.root / "14-ai-development/work-items/AID-2026-900/manifest.yaml").read_text(
                    encoding="utf-8"
                )
        })
        commit_tree(self.root, {"authored.md": b"rewritten authored index\n"})

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_authored_index_historical_pin_survives_path_deletion(self):
        original = b"authored index retained in history\n"
        original_sha = self.blob_sha(original)
        commit_tree(self.root, {"authored.md": original})
        manifest_path = self.root / "14-ai-development/work-items/AID-2026-900/manifest.yaml"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            yaml.safe_dump({
                "work_item_id": "AID-2026-900",
                "baseline_and_source_evidence": {
                    "authored_indexes": [
                        {"root": "authored.md", "root_blob": original_sha}
                    ]
                },
            }, sort_keys=False),
            encoding="utf-8",
        )
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                manifest_path.read_text(encoding="utf-8")
        })
        git(self.root, "rm", "authored.md")
        git(
            self.root,
            "-c", "user.name=Test",
            "-c", "user.email=test@example.invalid",
            "commit", "-m", "delete authored index",
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_authored_index_historical_pin_not_found_in_reachable_history_fails(self):
        data = b"authored index bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "authored.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "baseline_and_source_evidence": {
                        "authored_indexes": [
                            {"root": "authored.md", "root_blob": wrong}
                        ]
                    },
                }, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=1 ok=0 mismatch=1 path_missing=0 incomplete=0", out)
        self.assertIn("actual=not-found-in-reachable-history", out)

    def test_related_evidence_current_mode_checks_candidate_bytes(self):
        original = b"related evidence current bytes\n"
        digest = self.blob_sha(original)
        commit_tree(self.root, {
            "related.md": original,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "related_evidence": [
                        {
                            "reference_mode": "current",
                            "path": "related.md",
                            "blob": digest,
                        }
                    ],
                }, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_related_evidence_historical_mode_survives_later_rewrite(self):
        original = b"historical related evidence\n"
        digest = self.blob_sha(original)
        commit_tree(self.root, {"related.md": original})
        manifest = {
            "work_item_id": "AID-2026-900",
            "related_evidence": [
                {
                    "reference_mode": "historical",
                    "path": "related.md",
                    "blob": digest,
                }
            ],
        }
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump(manifest, sort_keys=False),
        })
        commit_tree(self.root, {"related.md": b"new related evidence bytes\n"})

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_related_evidence_historical_mode_survives_later_deletion(self):
        original = b"historical related evidence before deletion\n"
        digest = self.blob_sha(original)
        commit_tree(self.root, {"related.md": original})
        manifest = {
            "work_item_id": "AID-2026-900",
            "related_evidence": [
                {
                    "reference_mode": "historical",
                    "path": "related.md",
                    "blob": digest,
                }
            ],
        }
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump(manifest, sort_keys=False),
        })
        git(self.root, "rm", "related.md")
        git(
            self.root,
            "-c", "user.name=Test",
            "-c", "user.email=test@example.invalid",
            "commit", "-m", "delete related evidence",
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_related_evidence_missing_mode_is_candidate_incomplete(self):
        data = b"legacy related evidence bytes\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {
            "related.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "related_evidence": [
                        {"path": "related.md", "blob": digest}
                    ],
                }, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=1", out)
        self.assertIn("INCOMPLETE", out)

    def test_related_evidence_invalid_mode_is_incomplete(self):
        data = b"related evidence bytes\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {
            "related.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "related_evidence": [
                        {
                            "reference_mode": "sometimes",
                            "path": "related.md",
                            "blob": digest,
                        }
                    ],
                }, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=1", out)
        self.assertIn("INCOMPLETE", out)

    def test_related_evidence_explicit_current_mode_is_required_and_passes(self):
        data = b"explicit current evidence\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {
            "related.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "related_evidence": [
                        {
                            "reference_mode": "current",
                            "path": "related.md",
                            "blob": digest,
                        }
                    ],
                }, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_base_flag_allows_only_absent_mode_as_legacy_current(self):
        data = b"legacy current evidence\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {
            "related.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "related_evidence": [
                        {"path": "related.md", "blob": digest}
                    ],
                }, sort_keys=False),
        })

        code, out, err = self.run_gate(
            "HEAD", "--allow-missing-reference-mode"
        )
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_base_flag_does_not_hide_legacy_current_mismatch(self):
        data = b"actual legacy current evidence\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "related.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "related_evidence": [
                        {"path": "related.md", "blob": wrong}
                    ],
                }, sort_keys=False),
        })

        code, out, err = self.run_gate(
            "HEAD", "--allow-missing-reference-mode"
        )
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=1 ok=0 mismatch=1 path_missing=0 incomplete=0", out)
        self.assertIn(f"declared={wrong}", out)

    def test_base_flag_does_not_allow_invalid_mode(self):
        data = b"invalid mode evidence\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {
            "related.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "related_evidence": [
                        {
                            "reference_mode": "unknown",
                            "path": "related.md",
                            "blob": digest,
                        }
                    ],
                }, sort_keys=False),
        })

        code, out, err = self.run_gate(
            "HEAD", "--allow-missing-reference-mode"
        )
        self.assertEqual(code, 2, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=1", out)
        self.assertIn("INCOMPLETE", out)

    def test_missing_mode_without_base_flag_is_incomplete(self):
        data = b"missing mode evidence\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {
            "related.md": data,
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump({
                    "work_item_id": "AID-2026-900",
                    "related_evidence": [
                        {"path": "related.md", "blob": digest}
                    ],
                }, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=1", out)

    def test_historical_lookup_includes_reachable_merge_side_branch(self):
        git(
            self.root,
            "-c", "user.name=Test",
            "-c", "user.email=test@example.invalid",
            "commit", "--allow-empty", "-m", "common ancestor",
        )
        main_branch = git(self.root, "branch", "--show-current")
        git(self.root, "checkout", "-b", "historical-side")
        historical_data = b"blob introduced on merge side branch\n"
        historical_sha = self.blob_sha(historical_data)
        commit_tree(self.root, {"side-history.md": historical_data})
        git(self.root, "checkout", main_branch)

        manifest = {
            "work_item_id": "AID-2026-900",
            "related_evidence": [
                {
                    "reference_mode": "historical",
                    "path": "side-history.md",
                    "blob": historical_sha,
                }
            ],
        }
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump(manifest, sort_keys=False),
        })

        git(
            self.root,
            "-c", "user.name=Test",
            "-c", "user.email=test@example.invalid",
            "merge", "--no-ff", "historical-side",
            "-m", "merge historical side branch",
        )

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)

    def test_historical_lookup_cache_reuses_real_git_result(self):
        data = b"one historical blob used by two declarations\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {"related.md": data})
        manifest = {
            "work_item_id": "AID-2026-900",
            "related_evidence": [
                {
                    "reference_mode": "historical",
                    "path": "related.md",
                    "blob": digest,
                },
                {
                    "reference_mode": "historical",
                    "path": "related.md",
                    "blob": digest,
                },
            ],
        }
        commit_tree(self.root, {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml":
                yaml.safe_dump(manifest, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=2 ok=2 mismatch=0 path_missing=0 incomplete=0", out)


class UnboundBlobSha256Test(unittest.TestCase):
    """PR #1417 comment 7212343821: an unbound blob_sha256 is a violation."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")

    def tearDown(self):
        self.tmp.cleanup()

    def run_gate(self):
        p = subprocess.run(
            [
                sys.executable,
                str(GATE),
                "--root",
                str(self.root),
                "--commit",
                "HEAD",
            ],
            text=True,
            capture_output=True,
        )
        return p.returncode, p.stdout, p.stderr

    def commit_manifest(self, manifest, extra=None):
        files = {
            "14-ai-development/work-items/AID-2026-900/manifest.yaml": manifest
        }
        files.update(extra or {})
        return commit_tree(self.root, files)

    def test_bound_blob_sha256_with_matching_digest_passes(self):
        data = b"bound artifact bytes\n"
        manifest = (
            "work_item_id: AID-2026-900\n"
            "artifact_pins:\n"
            "  model_path: model.md\n"
            f"  model_blob_sha256: \"{hashlib.sha256(data).hexdigest()}\"\n"
        )
        self.commit_manifest(manifest, {"model.md": data})

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0 unbound=0", out)
        self.assertNotIn("UNBOUND_BLOB_SHA256", out)

    def test_bound_blob_sha256_with_wrong_digest_is_mismatch(self):
        data = b"bound artifact bytes\n"
        wrong = "0" * 64
        manifest = (
            "work_item_id: AID-2026-900\n"
            "artifact_pins:\n"
            "  model_path: model.md\n"
            f"  model_blob_sha256: \"{wrong}\"\n"
        )
        self.commit_manifest(manifest, {"model.md": data})

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(
            f"MISMATCH blob_sha256 manifest=14-ai-development/work-items/AID-2026-900/"
            f"manifest.yaml pointer=/artifact_pins/model_blob_sha256 path=model.md "
            f"declared={wrong} actual={hashlib.sha256(data).hexdigest()}",
            out,
        )
        self.assertNotIn("UNBOUND_BLOB_SHA256", out)

    def test_bound_blob_sha256_with_missing_target_is_path_missing(self):
        digest = "1" * 64
        manifest = (
            "work_item_id: AID-2026-900\n"
            "artifact_pins:\n"
            "  model_path: absent.md\n"
            f"  model_blob_sha256: \"{digest}\"\n"
        )
        self.commit_manifest(manifest)

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(
            "PATH_MISSING blob_sha256 manifest=14-ai-development/work-items/AID-2026-900/"
            f"manifest.yaml pointer=/artifact_pins/model_blob_sha256 path=absent.md "
            f"declared={digest}",
            out,
        )
        self.assertNotIn("UNBOUND_BLOB_SHA256", out)

    def test_digest_without_path_is_unbound_and_fails(self):
        digest = "8324ec551749c2d50067967e4a445b26a6683008a4fa52e02da02a9976417a15"
        manifest = (
            "work_item_id: AID-2026-900\n"
            "measurement_basis:\n"
            f"  model_blob_sha256_lf: \"{digest}\"\n"
        )
        self.commit_manifest(manifest)

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(
            "UNBOUND_BLOB_SHA256 manifest=14-ai-development/work-items/AID-2026-900/"
            "manifest.yaml pointer=/measurement_basis/model_blob_sha256_lf "
            f"field=model_blob_sha256_lf declared={digest}",
            out,
        )
        self.assertIn("unbound=1", out)
        self.assertNotIn("PATH_MISSING", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
