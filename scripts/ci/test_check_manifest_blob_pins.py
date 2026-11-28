#!/usr/bin/env python3
# scripts/ci/test_check_manifest_blob_pins.py
"""Offline unit tests for check_manifest_blob_pins and blob_pin_scope."""

from __future__ import annotations

import contextlib
import hashlib
import json
import io
import subprocess
import tempfile
import unittest

import yaml
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



def git(root: Path, *args: str) -> bytes:
    """Run Git locally; never accesses a remote."""
    proc = subprocess.run(
        ["git", *args],
        cwd=Path(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        raise AssertionError(
            "git command failed: "
            f"{args!r}\n"
            f"{proc.stderr.decode('utf-8', 'replace')}"
        )
    return proc.stdout


def blob_sha(data: bytes) -> str:
    """Return the Git blob SHA-1 of raw bytes."""
    return checker.digest_of("git-blob-sha1", data)


def commit_tree(root: Path, files: dict[str, bytes | str]) -> str:
    """
    Write/update files and create a local commit.

    Calling this more than once creates successive commits, which allows
    tests to construct a historical source commit and a candidate commit.
    """
    root = Path(root)

    for relative_path, content in files.items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(content, str):
            content = content.encode("utf-8")

        target.write_bytes(content)

    git(root, "add", "--all")
    git(root, "commit", "-m", "test fixture commit")

    return git(root, "rev-parse", "HEAD").decode("ascii").strip()


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
        # Every test gets an isolated local repository.
        self._repo_tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._repo_tmp.name)

        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Manifest Pin Tests")
        git(self.root, "config", "user.email", "manifest-pin-tests@example.invalid")


    def tearDown(self):
        blob_pin_registry.FIELD_REGISTRY.clear()
        blob_pin_registry.FIELD_REGISTRY.update(self._original_registry)
        checker.FIELD_REGISTRY.clear()
        checker.FIELD_REGISTRY.update(self._original_checker_registry)

    @staticmethod
    def blob_sha(data) -> str:
        if isinstance(data, str):
            data = data.encode("utf-8")
        return checker.digest_of("git-blob-sha1", data)

    def manifest(self) -> str:
        return (
            "14-ai-development/work-items/"
            "AID-2026-900/manifest.yaml"
        )

    def run_gate(self, commit: str | None = None):
        """
        Adapter for the new verify(root, commit, explain, verbose) API.

        The old run_gate() returned (exit_code, stdout, stderr).
        This adapter preserves that test-facing shape while invoking the
        actual new checker.verify() implementation.
        """
        if commit is None:
            commit = git(self.root, "rev-parse", "HEAD").decode("ascii").strip()

        stdout = io.StringIO()
        stderr = io.StringIO()

        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = checker.verify(
                self.root,
                commit,
                explain=True,
                verbose=True,
            )

        return code, stdout.getvalue(), stderr.getvalue()

    def expected_identity(
        self,
        *,
        kind: str,
        field_path: str,
        locator: str,
    ) -> str:
        """
        Build the stable identity prefix emitted by checker.identity_line().

        The new identity format uses field= and locator= rather than the
        old gate's human-oriented path= output.
        """
        return (
            f"{kind}"
            f" manifest={self.manifest()}"
            f" pin_id={checker.pin_id_for(self.manifest(), field_path)}"
            f" field={field_path}"
            f" scope=candidate"
            f" locator={locator}"
        )

    def assert_explained_finding(
        self, output, kind, field_path, locator, declared, actual
    ):
        manifest = self.manifest()
        pin_id = checker.pin_id_for(manifest, field_path)
        identity = (
            f"{kind} manifest={manifest} pin_id={pin_id} "
            f"field={field_path} scope=candidate locator={locator}"
        )
        self.assertIn(identity, output)
        self.assertIn(
            f"declared={json.dumps(declared)} actual={json.dumps(actual)}",
            output,
        )

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
        data_a = b"pair A content\n"
        data_b = b"pair B content\n"
        digest_a = blob_sha(data_a)
        digest_b = blob_sha(data_b)
        wrong_digest = "0" * 40

        document = {
            "baseline_and_source_evidence": {
                "authored_indexes": [
                    {
                        "root": "pair-a.md",
                        "root_blob": wrong_digest,
                        "en_mirror": "pair-b.md",
                        "en_mirror_blob": digest_a,
                    }
                ]
            }
        }

        commit = commit_tree(
            self.root,
            {
                "pair-a.md": data_a,
                "pair-b.md": data_b,
                self.manifest(): yaml.safe_dump(document, sort_keys=False),
            },
        )

        code, out, err = self.run_gate(commit)

        self.assertEqual(code, 1, msg=out + err)
        self.assertIn(
            "pins=2 ok=0 mismatch=2 path_missing=0 incomplete=0",
            out,
        )

        self.assert_explained_finding(
            out,
            "MISMATCH",
            "baseline_and_source_evidence.authored_indexes[0].root_blob",
            "pair-a.md",
            wrong_digest,
            digest_a,
        )
        self.assert_explained_finding(
            out,
            "MISMATCH",
            "baseline_and_source_evidence.authored_indexes[0].en_mirror_blob",
            "pair-b.md",
            digest_a,
            digest_b,
        )

    def test_path_key_identity_uses_en_mirror_path_not_neighbour_file(self):
        data_root = b"root content\n"
        data_mirror = b"English mirror content\n"
        digest_root = blob_sha(data_root)
        digest_mirror = blob_sha(data_mirror)

        document = {
            "baseline_and_source_evidence": {
                "authored_indexes": [
                    {
                        "root": "file-root.md",
                        "root_blob": digest_root,
                        "en_mirror": "file-en.md",
                        "en_mirror_blob": digest_root,
                    }
                ]
            }
        }

        commit = commit_tree(
            self.root,
            {
                "file-root.md": data_root,
                "file-en.md": data_mirror,
                self.manifest(): yaml.safe_dump(document, sort_keys=False),
            },
        )

        code, out, err = self.run_gate(commit)

        self.assertEqual(code, 1, msg=out + err)
        self.assertIn(
            "pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0",
            out,
        )

        self.assert_explained_finding(
            out,
            "MISMATCH",
            "baseline_and_source_evidence.authored_indexes[0].en_mirror_blob",
            "file-en.md",
            digest_root,
            digest_mirror,
        )

        self.assertNotIn(
            "field=baseline_and_source_evidence.authored_indexes[0].root_blob",
            out,
        )
        self.assertNotIn("locator=file-root.md", out)

    def test_cross_identity_isolation_reports_only_the_wrong_pin(self):
        data_a = b"identity A content\n"
        data_b = b"identity B content\n"
        digest_a = blob_sha(data_a)
        digest_b = blob_sha(data_b)
        wrong_digest = "0" * 40

        document = {
            "baseline_and_source_evidence": {
                "authored_indexes": [
                    {
                        "root": "identity-a.md",
                        "root_blob": digest_a,
                    },
                    {
                        "root": "identity-b.md",
                        "root_blob": wrong_digest,
                    },
                ]
            }
        }

        commit = commit_tree(
            self.root,
            {
                "identity-a.md": data_a,
                "identity-b.md": data_b,
                self.manifest(): yaml.safe_dump(document, sort_keys=False),
            },
        )

        code, out, err = self.run_gate(commit)

        self.assertEqual(code, 1, msg=out + err)
        self.assertIn(
            "pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0",
            out,
        )

        self.assert_explained_finding(
            out,
            "MISMATCH",
            "baseline_and_source_evidence.authored_indexes[1].root_blob",
            "identity-b.md",
            wrong_digest,
            digest_b,
        )

        self.assertNotIn(
            "field=baseline_and_source_evidence.authored_indexes[0].root_blob",
            out,
        )
        self.assertNotIn("locator=identity-a.md", out)

    def test_every_enumerated_path_digest_pair_is_validated(self):
        file_contents = {
            "top-root.md": b"top root\n",
            "top-en.md": b"top English mirror\n",
            "top-zh.md": b"top Chinese mirror\n",
            "auth-root.md": b"authored root\n",
            "auth-en.md": b"authored English mirror\n",
            "auth-zh.md": b"authored Chinese mirror\n",
            "related-path.md": b"related evidence\n",
            "related-en.md": b"related English mirror\n",
            "related-zh.md": b"related Chinese mirror\n",
            "execution-evidence.md": b"execution evidence\n",
            "prompt.md": b"prompt source\n",
            "session-prompt.md": b"executed prompt snapshot\n",
        }
        digests = {
            name: blob_sha(content)
            for name, content in file_contents.items()
        }

        document = {
            "root": "top-root.md",
            "root_blob": digests["top-root.md"],
            "en_mirror": "top-en.md",
            "en_mirror_blob": digests["top-en.md"],
            "zh_cn_mirror": "top-zh.md",
            "zh_cn_mirror_blob": digests["top-zh.md"],
            "baseline_and_source_evidence": {
                "authored_indexes": [
                    {
                        "root": "auth-root.md",
                        "root_blob": digests["auth-root.md"],
                        "en_mirror": "auth-en.md",
                        "en_mirror_blob": digests["auth-en.md"],
                        "zh_cn_mirror": "auth-zh.md",
                        "zh_cn_mirror_blob": digests["auth-zh.md"],
                    }
                ]
            },
            "related_evidence": [
                {
                    "path": "related-path.md",
                    "blob": digests["related-path.md"],
                    "en_mirror": "related-en.md",
                    "en_mirror_blob": digests["related-en.md"],
                    "zh_cn_mirror": "related-zh.md",
                    "zh_cn_mirror_blob": digests["related-zh.md"],
                }
            ],
            "evidence_file": "execution-evidence.md",
            "evidence_blob": digests["execution-evidence.md"],
            "prompt_file": "prompt.md",
            "prompt_sha256": hashlib.sha256(file_contents["prompt.md"]).hexdigest(),
            "prompt_bytes": len(file_contents["prompt.md"]),
            "session_evidence": [
                {
                    "executed_prompt_snapshot_file": "session-prompt.md",
                    "executed_prompt_sha256": hashlib.sha256(
                        file_contents["session-prompt.md"]
                    ).hexdigest(),
                    "executed_prompt_bytes": len(
                        file_contents["session-prompt.md"]
                    ),
                }
            ],
        }

        # source_commit / d_source_commit 是 NON_BLOB：
        # 2 个 commit 引用不计入 pin。
        # 因此当前 checker 对本 fixture 枚举的有效 blob pins 是 14，而不是旧测试的 16。

        candidate_files = dict(file_contents)
        candidate_files[self.manifest()] = yaml.safe_dump(
            document,
            sort_keys=False,
        )

        commit = commit_tree(self.root, candidate_files)

        code, out, err = self.run_gate(commit)

        self.assertEqual(code, 0, msg=out + err)
        self.assertIn(
            "pins=14 ok=14 mismatch=0 path_missing=0 incomplete=0",
            out,
        )
        self.assertIn("findings=0 violations=0", out)
        self.assertNotIn("MISMATCH", out)
        self.assertNotIn("INCOMPLETE", out)

    def test_related_evidence_mirror_pair_substitution_is_named(self):
        data_en = b"related English mirror\n"
        data_zh = b"related Chinese mirror\n"
        digest_en = blob_sha(data_en)
        digest_zh = blob_sha(data_zh)

        document = {
            "related_evidence": [
                {
                    "en_mirror": "related-en.md",
                    "en_mirror_blob": digest_zh,
                    "zh_cn_mirror": "related-zh.md",
                    "zh_cn_mirror_blob": digest_zh,
                }
            ]
        }

        commit = commit_tree(
            self.root,
            {
                "related-en.md": data_en,
                "related-zh.md": data_zh,
                self.manifest(): yaml.safe_dump(document, sort_keys=False),
            },
        )

        code, out, err = self.run_gate(commit)

        self.assertEqual(code, 1, msg=out + err)
        self.assertIn(
            "pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0",
            out,
        )

        self.assert_explained_finding(
            out,
            "MISMATCH",
            "related_evidence[0].en_mirror_blob",
            "related-en.md",
            digest_zh,
            digest_en,
        )

        self.assertNotIn(
            "field=related_evidence[0].zh_cn_mirror_blob",
            out,
        )
        self.assertNotIn("locator=related-zh.md", out)


if __name__ == "__main__":
    unittest.main()
