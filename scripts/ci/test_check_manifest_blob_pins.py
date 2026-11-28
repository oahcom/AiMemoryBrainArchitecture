#!/usr/bin/env python3
# scripts/ci/test_check_manifest_blob_pins.py
"""Offline unit tests for check_manifest_blob_pins and blob_pin_scope."""

from __future__ import annotations

import contextlib
import hashlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import blob_pin_registry
import check_manifest_blob_pins as checker
from blob_pin_scope import (
    NoScope,
    PathMissing,
    Scope,
    Unresolved,
    derive_scope,
    digest_of,
    resolve_bytes,
)


class DuplicateItemsMapping(dict):
    """Mapping test double that deliberately yields duplicate key occurrences."""

    def items(self):
        return [
            ("prompt_file", "payload.bin"),
            ("prompt_sha256", self["prompt_sha256"]),
            ("prompt_sha256", self["prompt_sha256"]),
        ]


class ManifestBlobPinTests(unittest.TestCase):
    def setUp(self):
        self._original_registry = dict(blob_pin_registry.FIELD_REGISTRY)
        self._original_checker_registry = dict(checker.FIELD_REGISTRY)

        self._set_spec(
            "prompt_sha256",
            algorithm="sha256",
            locator_keys=("prompt_file",),
        )
        self._set_spec(
            "prompt_blob_sha",
            algorithm="git-blob-sha1",
            locator_keys=("prompt_file",),
        )
        self._set_spec(
            "prompt_bytes",
            algorithm="byte-length",
            locator_keys=("prompt_file",),
        )
        self._set_spec(
            "implementation_commits",
            algorithm="NON_BLOB",
            locator_keys=(),
        )

    def tearDown(self):
        blob_pin_registry.FIELD_REGISTRY.clear()
        blob_pin_registry.FIELD_REGISTRY.update(self._original_registry)
        checker.FIELD_REGISTRY.clear()
        checker.FIELD_REGISTRY.update(self._original_checker_registry)

    def _set_spec(self, name, *, algorithm, locator_keys):
        spec = SimpleNamespace(
            algorithm=algorithm,
            locator_keys=tuple(locator_keys),
            scope_source="test",
        )
        blob_pin_registry.FIELD_REGISTRY[name] = spec
        checker.FIELD_REGISTRY[name] = spec

    @staticmethod
    def _git(root: Path, *args: str) -> str:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if proc.returncode:
            raise AssertionError(
                f"git {args!r} failed: {proc.stderr.strip()}"
            )
        return proc.stdout.strip()

    def _make_repo(self, *, payload: bytes = b"payload\n"):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)

        self._git(root, "init", "-q")
        self._git(root, "config", "user.email", "tests@example.invalid")
        self._git(root, "config", "user.name", "Unit Tests")

        manifest_dir = root / "14-ai-development" / "work-items" / "AID-TEST"
        manifest_dir.mkdir(parents=True)
        (manifest_dir / "manifest.yaml").write_text(
            "test: true\n",
            encoding="utf-8",
        )
        (root / "payload.bin").write_bytes(payload)

        self._git(root, "add", ".")
        self._git(root, "commit", "-qm", "test fixture")
        commit = self._git(root, "rev-parse", "HEAD")

        self.addCleanup(temporary.cleanup)
        return root, commit, payload

    def test_registry_field_name_strips_array_indices(self):
        self.assertEqual(
            checker.registry_field_name("implementation_commits[0]"),
            "implementation_commits",
        )
        self.assertEqual(
            checker.registry_field_name("a.b[0].c[2]"),
            "c",
        )

    def test_field_paths_have_no_synthetic_manifest_root(self):
        root, _commit, payload = self._make_repo()
        node = {
            "prompt_file": "payload.bin",
            "prompt_sha256": hashlib.sha256(payload).hexdigest(),
        }

        finding = checker.check_pin(
            root=root,
            manifest="14-ai-development/work-items/AID-TEST/manifest.yaml",
            manifest_dir="14-ai-development/work-items/AID-TEST",
            field_path="a.b[0].prompt_sha256",
            node=node,
            key="prompt_sha256",
        )

        self.assertIsNone(finding)
        self.assertFalse(
            checker.registry_field_name("manifest.a.b[0].prompt_sha256")
            == "manifest"
        )

    def test_pin_id_is_never_none(self):
        finding = checker._finding(
            kind="UNCLASSIFIED",
            manifest="14-ai-development/work-items/AID-TEST/manifest.yaml",
            field_path="a.b[0].prompt_sha256",
        )
        self.assertTrue(finding.pin_id)
        self.assertNotEqual(finding.pin_id.lower(), "none")
        self.assertIn("pin_id=", checker.identity_line(finding))

    def test_identity_and_explain_prefix_and_newline_are_consistent(self):
        finding = checker._finding(
            kind="MISMATCH",
            manifest="work-items/AID-TEST/manifest.yaml",
            field_path="a.b[0].prompt_sha256",
            scope=Scope(kind="candidate"),
            locator="payload.bin",
            declared='bad"value',
            actual="actual",
            reason="DIGEST_MISMATCH",
            classification="sha256",
            basis="FIELD_REGISTRY:prompt_file",
        )

        identity = checker.identity_line(finding)
        explained = checker.explain_line(finding)

        self.assertTrue(explained.startswith(identity))
        self.assertEqual(explained[:len(identity)], identity)
        self.assertNotIn("\n", identity)
        self.assertNotIn("\n", explained)

        plain_output = io.StringIO()
        explain_output = io.StringIO()
        with contextlib.redirect_stdout(plain_output):
            print(identity)
        with contextlib.redirect_stdout(explain_output):
            print(explained)

        self.assertEqual(plain_output.getvalue().count("\n"), 1)
        self.assertEqual(explain_output.getvalue().count("\n"), 1)

    # 失败 1：测试错。该测试应明确使用临时仓库中已验证存在的 commit scope，
    # 避免把摘要算法测试与 candidate/HEAD scope 解析耦合在一起。

    def test_registered_sha256_is_compared_using_registry_algorithm(self):
        root, commit, payload = self._make_repo()

        # 先证明 fixture 中的 commit 和 blob 确实可由 Git 读取。
        self._git(root, "cat-file", "-e", f"{commit}:payload.bin")

        expected = hashlib.sha256(payload).hexdigest()
        node = {
            "prompt_file": "payload.bin",
            "prompt_commit_sha": commit,
            "prompt_sha256": expected,
        }

        finding = checker.check_pin(
            root=root,
            manifest="manifest.yaml",
            manifest_dir="14-ai-development/work-items/AID-TEST",
            field_path="prompt_sha256",
            node=node,
            key="prompt_sha256",
        )

        self.assertIsNone(finding)

        node["prompt_sha256"] = "0" * 64
        finding = checker.check_pin(
            root=root,
            manifest="manifest.yaml",
            manifest_dir="14-ai-development/work-items/AID-TEST",
            field_path="prompt_sha256",
            node=node,
            key="prompt_sha256",
        )

        self.assertIsNotNone(finding)
        self.assertEqual(finding.kind, "MISMATCH")
        self.assertEqual(finding.actual, expected)

    def test_unregistered_digest_is_unclassified(self):
        finding = checker.check_pin(
            root=Path("."),
            manifest="manifest.yaml",
            manifest_dir=".",
            field_path="unregistered_digest",
            node={"unregistered_digest": "a" * 64},
            key="unregistered_digest",
        )

        self.assertIsNotNone(finding)
        self.assertEqual(finding.kind, "UNCLASSIFIED")
        self.assertEqual(finding.reason, "UNREGISTERED_FIELD")
        self.assertEqual(finding.basis, "UNREGISTERED_FIELD")

    def test_sentinel_is_unresolved_before_scope_lookup(self):
        finding = checker.check_pin(
            root=Path("."),
            manifest="manifest.yaml",
            manifest_dir=".",
            field_path="prompt_sha256",
            node={"prompt_sha256": "NOT_VERIFIED"},
            key="prompt_sha256",
        )

        self.assertIsNotNone(finding)
        self.assertEqual(finding.kind, "UNRESOLVED")
        self.assertEqual(finding.reason, "SENTINEL_DECLARATION")

    def test_digest_algorithms_use_raw_bytes(self):
        data = b"line one\r\nline two\n"

        self.assertEqual(
            digest_of("sha256", data),
            hashlib.sha256(data).hexdigest(),
        )

        git_blob_payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
        self.assertEqual(
            digest_of("git-blob-sha1", data),
            hashlib.sha1(git_blob_payload).hexdigest(),
        )
        self.assertEqual(digest_of("byte-length", data), str(len(data)))

        normalized = data.replace(b"\r\n", b"\n")
        self.assertNotEqual(
            digest_of("sha256", data),
            digest_of("sha256", normalized),
        )

    def test_digest_of_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            digest_of("sha256", "not bytes")

    def test_derive_scope_prefers_sibling_commit(self):
        scope = derive_scope(
            {
                "prompt_commit_sha": "a" * 40,
                "prompt_file": "payload.bin",
            },
            "prompt_sha256",
            "work-items/AID-TEST",
            locator_keys=("prompt_file",),
        )

        self.assertEqual(scope.kind, "commit")
        self.assertEqual(scope.commit_sha, "a" * 40)

    def test_derive_scope_uses_registered_sibling_path(self):
        scope = derive_scope(
            {"prompt_file": "payload.bin"},
            "prompt_sha256",
            "work-items/AID-TEST",
            locator_keys=("prompt_file",),
        )

        self.assertEqual(scope.kind, "candidate")
        self.assertEqual(scope.content_ref, "work-items/AID-TEST")

    def test_derive_scope_without_commit_or_path_raises_no_scope(self):
        with self.assertRaises(NoScope):
            derive_scope(
                {},
                "prompt_sha256",
                "work-items/AID-TEST",
                locator_keys=("prompt_file",),
            )

    def test_resolve_bytes_missing_path_is_path_missing(self):
        root, _commit, _payload = self._make_repo()

        with self.assertRaises(PathMissing):
            resolve_bytes(
                root,
                Scope(kind="candidate"),
                "does-not-exist.bin",
            )

    def test_resolve_bytes_unresolvable_commit_is_unresolved(self):
        root, _commit, _payload = self._make_repo()

        with self.assertRaises(Unresolved):
            resolve_bytes(
                root,
                Scope(kind="commit", commit_sha="f" * 40),
                "payload.bin",
            )

    # 失败 2：测试错。DuplicateItemsMapping 的底层 dict 没有 prompt_file，
    # 但 checker 使用 `name in node` 判断 locator 是否存在。
    # 将 prompt_file 放入真实 mapping，同时保留 items() 的重复字段行为。

    def test_verify_counts_duplicate_manifest_field_occurrence_once(self):
        root, commit, payload = self._make_repo()
        document = DuplicateItemsMapping({
            "prompt_file": "payload.bin",
            "prompt_sha256": hashlib.sha256(payload).hexdigest(),
        })

        with mock.patch.object(checker.yaml, "safe_load", return_value=document):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = checker.verify(root, commit, verbose=True)

        self.assertEqual(exit_code, 0)
        summary = output.getvalue().splitlines()[0]
        self.assertIn("pins=1", summary)
        self.assertIn("ok=1", summary)
        self.assertIn("findings=0", summary)

    # 失败 3：测试错。与失败 2 是同一个 fixture 缺陷；
    # 修复底层 mapping 的 prompt_file 后，失败声明才会走到摘要比较并产生 MISMATCH。

    def test_verify_counts_failed_duplicate_occurrence_once(self):
        root, commit, _payload = self._make_repo()
        document = DuplicateItemsMapping({
            "prompt_file": "payload.bin",
            "prompt_sha256": "0" * 64,
        })

        with mock.patch.object(checker.yaml, "safe_load", return_value=document):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exit_code = checker.verify(root, commit, verbose=True)

        self.assertEqual(exit_code, 1)
        lines = output.getvalue().splitlines()
        self.assertIn("pins=1", lines[0])
        self.assertIn("findings=1", lines[0])
        self.assertEqual(
            sum(line.startswith("MISMATCH ") for line in lines),
            1,
        )

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
    unittest.main()
