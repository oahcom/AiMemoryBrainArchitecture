你给的 498 行阶段一检查器已落地并实跑。**13 个测试里 6 个红。** 下面是完整测试文件与逐条失败原文——这次你有了 388 行原文，请给出可落盘的完整文件（检查器 + 测试改动）。

## 一、失败原文（`python -X utf8 -m unittest scripts.ci.test_check_manifest_blob_pins`）

FAIL: test_changed_byte_is_rejected_with_declared_and_actual_digest (scripts.ci.test_check_manifest_blob_pins.BlobPinsT
est.test_changed_byte_is_rejected_with_declared_and_actual_digest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_lcs\wt-main2\scripts\ci\test_check_manifest_blob_pins.py", line 94, in test_changed_byte_is_rejected_w
ith_declared_and_actual_digest
    self.assertIn(f"declared={wrong}", out)
AssertionError: 'declared=0000000000000000000000000000000000000000' not found in "main=b24c70a1e9ed4d08433da3018d17c40b
1a81bf1f manifests=1 pins=0 ok=0 mismatch=0 path_missing=0 incomplete=0\nverified=0 mismatch=0 path_missing=0 unresolve
d=1 non_blob=0 incomplete=0\nINCOMPLETE UNRESOLVED(GIT_OBJECT_MISSING): manifest=14-ai-development/work-items/AID-2026-
900/manifest.yaml field=index.root declared='0000000000000000000000000000000000000000': Git object does not exist: 0000
000000000000000000000000000000000000\n"

FAIL: test_cross_identity_isolation_reports_only_the_wrong_pin (scripts.ci.test_check_manifest_blob_pins.BlobPinsTest.t
est_cross_identity_isolation_reports_only_the_wrong_pin)
Kills a resolver that reuses one identity's digest while checking another.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_lcs\wt-main2\scripts\ci\test_check_manifest_blob_pins.py", line 242, in test_cross_identity_isolation_
reports_only_the_wrong_pin
    self.assertIn("pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0", out)
AssertionError: 'pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0' not found in "main=d30daeeddc9620045f252b725f80bdf
1351d78cf manifests=1 pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0\nverified=1 mismatch=0 path_missing=0 unresolv
ed=1 non_blob=0 incomplete=0\nINCOMPLETE UNRESOLVED(GIT_OBJECT_MISSING): manifest=14-ai-development/work-items/AID-2026
-900/manifest.yaml field=authored_indexes[1].root declared='0000000000000000000000000000000000000000': Git object does 
not exist: 0000000000000000000000000000000000000000\n"

FAIL: test_deleted_path_is_rejected_and_named (scripts.ci.test_check_manifest_blob_pins.BlobPinsTest.test_deleted_path_
is_rejected_and_named)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_lcs\wt-main2\scripts\ci\test_check_manifest_blob_pins.py", line 105, in test_deleted_path_is_rejected_
and_named
    self.assertIn("PATH_MISSING", out)
AssertionError: 'PATH_MISSING' not found in "main=344cd3254605b854d9f0414e9036ca3f93dac3cb manifests=1 pins=0 ok=0 mism
atch=0 path_missing=0 incomplete=0\nverified=0 mismatch=0 path_missing=0 unresolved=1 non_blob=0 incomplete=0\nINCOMPLE
TE UNRESOLVED(GIT_OBJECT_MISSING): manifest=14-ai-development/work-items/AID-2026-900/manifest.yaml field=index.root de
clared='1111111111111111111111111111111111111111': Git object does not exist: 1111111111111111111111111111111111111111\
n"

FAIL: test_neighbouring_digest_key_does_not_verify_target_pair (scripts.ci.test_check_manifest_blob_pins.BlobPinsTest.t
est_neighbouring_digest_key_does_not_verify_target_pair)
Kills a resolver that reads pair A's digest from pair B's sibling key.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_lcs\wt-main2\scripts\ci\test_check_manifest_blob_pins.py", line 175, in test_neighbouring_digest_key_d
oes_not_verify_target_pair
    self.assertIn("pins=2 ok=0 mismatch=2 path_missing=0 incomplete=0", out)
AssertionError: 'pins=2 ok=0 mismatch=2 path_missing=0 incomplete=0' not found in "main=a642021ceada5f1586b606156839399
5e541b503 manifests=1 pins=1 ok=0 mismatch=1 path_missing=0 incomplete=0\nverified=0 mismatch=1 path_missing=0 unresolv
ed=1 non_blob=0 incomplete=0\nINCOMPLETE UNRESOLVED(GIT_OBJECT_MISSING): manifest=14-ai-development/work-items/AID-2026
-900/manifest.yaml field=authored_indexes[0].root declared='0000000000000000000000000000000000000000': Git object does 
not exist: 0000000000000000000000000000000000000000\nMISMATCH authored_indexes[0].en_mirror path=pair-b.md declared=f6b
5ecc7f3c53107a60423e1ab29a220cea48a35 actual=8586130aaa68bd26cfc7745413631095492ff834\n"

FAIL: test_nested_authored_index_mirror_pin_is_checked (scripts.ci.test_check_manifest_blob_pins.BlobPinsTest.test_nest
ed_authored_index_mirror_pin_is_checked)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_lcs\wt-main2\scripts\ci\test_check_manifest_blob_pins.py", line 80, in test_nested_authored_index_mirr
or_pin_is_checked
    self.assertIn("MISMATCH authored_indexes[0].en_mirror", out)
AssertionError: 'MISMATCH authored_indexes[0].en_mirror' not found in "main=c803e77794c95274cb9e5385ae585f0d4b398085 ma
nifests=1 pins=0 ok=0 mismatch=0 path_missing=0 incomplete=0\nverified=0 mismatch=0 path_missing=0 unresolved=1 non_blo
b=0 incomplete=0\nINCOMPLETE UNRESOLVED(GIT_OBJECT_MISSING): manifest=14-ai-development/work-items/AID-2026-900/manifes
t.yaml field=authored_indexes[0].en_mirror declared='0000000000000000000000000000000000000000': Git object does not exi
st: 0000000000000000000000000000000000000000\n"

FAIL: test_unavailable_cross_commit_is_incomplete_not_pass (scripts.ci.test_check_manifest_blob_pins.BlobPinsTest.test_
unavailable_cross_commit_is_incomplete_not_pass)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_lcs\wt-main2\scripts\ci\test_check_manifest_blob_pins.py", line 129, in test_unavailable_cross_commit_
is_incomplete_not_pass
    self.assertEqual(code, 2, out + err)
AssertionError: 1 != 2 : main=b08a220c1cf58b0fdfe415a7992bccdc5d112209 manifests=1 pins=0 ok=0 mismatch=0 path_missing=
0 incomplete=0
verified=0 mismatch=0 path_missing=0 unresolved=1 non_blob=0 incomplete=0
INCOMPLETE UNRESOLVED(GIT_OBJECT_MISSING): manifest=14-ai-development/work-items/AID-2026-900/manifest.yaml field=d_sou
rce_blobs[0] declared='1111111111111111111111111111111111111111': Git object does not exist: 11111111111111111111111111
11111111111111
----------------------------------------------------------------------
Ran 13 tests in 7.418s
FAILED (failures=6)

## 二、从失败里能看出的三个语义问题

1. **`pins` 计数变了**：`test_deleted_path_is_rejected_and_named` 得到 `pins=0`，而旧实现是 `pins=1` + `PATH_MISSING`。说明对象类型/声明合法性判定放在了 `pins += 1` 之前并提前返回。旧语义是「凡是进入了 check 的声明都算一个 pin」，测试断言的正是这个。
2. **合成 OID 被当成 `GIT_OBJECT_MISSING`**：多数测试用 `'0'*40`、`'a'*40` 这类对象库里不存在的值来构造 mismatch 场景。新代码先查对象类型 → 不存在 → 归 `UNRESOLVED`，于是 `MISMATCH ... declared=... actual=...` 不再出现。
3. **`declared=0000…` 丢失**：`test_changed_byte_is_rejected_with_declared_and_actual_digest` 断言问题行里必须带 `declared=<原声明值>`，新输出没有。

## 三、必须由你决定并落地的一件事

对象不存在的 40-hex 声明，到底是：

- (a) `UNRESOLVED(GIT_OBJECT_MISSING)`（契约 §6.1 第 3 条），代价是这些测试的 fixture 必须改成真实存在的 blob，且 `pins` 语义要重新定义；还是
- (b) 对象类型判定**只用于把已存在的 commit/tree/tag 分流为 `NON_BLOB`**；对象不存在时仍走原有路径（读 locator、比对声明值 → `MISMATCH` / `PATH_MISSING`），`GIT_OBJECT_MISSING` 在阶段一不产生。

选 (a) 请给出全部 6 个测试的 fixture 改法（要能直接落盘）。选 (b) 请给出检查器的修改，并说明这与契约 §6.1 的偏离如何记录（阶段一注释？契约勘误？）。

我的判断倾向：阶段一的目的是「分类语义与双台账」，不是「对象存在性判定」；(b) 的改动面小、保住 13 个测试的既有语义、且 `NON_BLOB` 仍然实现。但这是你的裁定，不是我的。

## 四、要交付的东西

1. 阶段一检查器的**完整替换文件**（最终版，直接可落盘）。
2. 测试的改动：如果只需新增，给追加块；如果需要改既有断言，逐条给出「旧行 → 新行」。
3. `manifest-blob-pins-unresolved.txt` 的初始内容（含注释头）。
4. workflow 两步 ratchet 的最终 YAML（含 `sed` 不吞 exit 2 的处理）。
5. `#1350` 正文的「0. 阶段适用范围」段落。

## 五、现有测试文件（388 行，逐字）

```python
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

```
