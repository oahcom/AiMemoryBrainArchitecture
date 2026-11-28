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


if __name__ == "__main__":
    unittest.main()
