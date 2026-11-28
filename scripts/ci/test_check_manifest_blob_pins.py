# scripts/ci/test_check_manifest_blob_pins.py
#!/usr/bin/env python3
"""Tests for committed-byte and historical manifest blob-pin verification."""

import hashlib
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
GATE = HERE / "check_manifest_blob_pins.py"

# Finding format:
# CODE manifest=... pin_id=... field=... scope=... locator=...
#      declared="..." actual="..." reason="..."
#      classification="..." basis="..."
_FIELD_RE = re.compile(r'(\w+)=(?:"((?:\\.|[^"])*)"|(\S+))')


def git(root, *args, data=None, check=True):
    process = subprocess.run(
        ["git", *args],
        cwd=root,
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )
    return process.stdout.decode().strip()


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
        "-c", "user.name=Test",
        "-c", "user.email=test@example.invalid",
        "commit", "-m", "fixture",
    )
    return git(root, "rev-parse", "HEAD")


def parse_findings(output):
    """Parse checker finding lines into independent code and field values."""
    findings = []
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        parts = stripped.split(None, 1)
        code = parts[0]
        if code not in {
            "HISTORICAL_REFERENCE_NOT_FOUND",
            "REFERENCE_MODE_MISSING_OR_INVALID",
            "CURRENT_REFERENCE_MISMATCH",
            "INCOMPLETE",
        }:
            continue

        fields = {}
        if code == "INCOMPLETE" and len(parts) == 2:
            if stripped.startswith("INCOMPLETE manifest="):
                prefix, separator, message = stripped.partition(": ")
                if separator:
                    fields["manifest"] = prefix[len("INCOMPLETE manifest="):]
                    fields["reason"] = message
            else:
                prefix, separator, message = stripped.partition(": ")
                if separator:
                    fields["locator"] = prefix[len("INCOMPLETE "):]
                    fields["reason"] = message
        elif len(parts) == 2:
            for match in _FIELD_RE.finditer(parts[1]):
                key, quoted, unquoted = match.groups()
                value = quoted if quoted is not None else unquoted
                if quoted is not None:
                    value = (
                        value.replace(r"\"", '"')
                        .replace(r"\\", "\\")
                    )
                fields[key] = value

        findings.append({
            "code": code,
            **fields,
            "line": stripped,
        })

    return findings


class BlobPinsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Test")
        git(self.root, "config", "user.email", "test@example.invalid")

    def tearDown(self):
        self.tmp.cleanup()

    def run_gate(self, commit="HEAD"):
        process = subprocess.run(
            [
                sys.executable,
                str(GATE),
                "--root", str(self.root),
                "--commit", commit,
            ],
            text=True,
            capture_output=True,
        )
        return process.returncode, process.stdout, process.stderr

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

    def manifest_path(self):
        return "14-ai-development/work-items/AID-2026-900/manifest.yaml"

    def findings(self, out, err=""):
        return parse_findings(out + "\n" + err)

    def assert_finding(self, out, code, **expected):
        matches = [
            finding
            for finding in self.findings(out)
            if finding["code"] == code
            and all(finding.get(key) == value for key, value in expected.items())
        ]
        self.assertTrue(
            matches,
            "No finding matched "
            f"code={code!r}, expected={expected!r}.\n"
            f"Parsed findings: {self.findings(out)!r}\n"
            f"Output:\n{out}",
        )
        return matches[0]

    def assert_no_finding(self, out, code, **expected):
        matches = [
            finding
            for finding in self.findings(out)
            if finding["code"] == code
            and all(finding.get(key) == value for key, value in expected.items())
        ]
        self.assertFalse(
            matches,
            f"Unexpected finding(s): {matches!r}\nOutput:\n{out}",
        )

    def test_valid_pin_is_silent_about_individual_pin(self):
        data = b"committed bytes\n"
        sha = self.blob_sha(data)
        commit_tree(self.root, {
            "README.md": data,
            self.manifest_path(): self.manifest("README.md", sha),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out
        )
        self.assert_no_finding(out, "CURRENT_REFERENCE_MISMATCH")

    def test_nested_authored_index_mirror_pin_is_checked_historically(self):
        data = b"authored mirror bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "docs/en/05-memory-runtime/README.md": data,
            self.manifest_path(): (
                "baseline_and_source_evidence:\n"
                "  authored_indexes:\n"
                "    - en_mirror: docs/en/05-memory-runtime/README.md\n"
                f"      en_mirror_blob: \"{wrong}\"\n"
            ),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        finding = self.assert_finding(
            out,
            "HISTORICAL_REFERENCE_NOT_FOUND",
            field="authored_indexes[0].en_mirror",
            pin_id="authored_indexes[0].en_mirror",
            locator="docs/en/05-memory-runtime/README.md",
            classification="historical",
        )
        self.assertEqual(finding.get("declared"), wrong)
        self.assert_no_finding(out, "CURRENT_REFERENCE_MISMATCH")

    def test_changed_current_byte_is_rejected_with_declared_and_actual_digest(self):
        data = b"committed bytes\n"
        wrong = "0" * 40
        commit_tree(self.root, {
            "README.md": data,
            self.manifest_path(): self.manifest("README.md", wrong),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        finding = self.assert_finding(
            out,
            "CURRENT_REFERENCE_MISMATCH",
            field="index.root",
            pin_id="index.root",
            locator="README.md",
        )
        self.assertEqual(finding.get("declared"), wrong)
        self.assertEqual(finding.get("actual"), self.blob_sha(data))

    def test_deleted_path_is_rejected_with_current_diagnostic(self):
        commit_tree(self.root, {
            self.manifest_path(): self.manifest("missing.md", "1" * 40),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        finding = self.assert_finding(
            out,
            "CURRENT_REFERENCE_MISMATCH",
            locator="missing.md",
        )
        self.assertIn(
            "absent from candidate commit tree",
            finding.get("reason", ""),
        )

    def test_prompt_snapshot_fields_are_not_asserted_by_this_checker(self):
        wrong_sha = "0" * 64
        commit_tree(self.root, {
            self.manifest_path(): (
                "prompt_sha256: " + wrong_sha + "\n"
                "prompt_bytes: 999\n"
                "prompt_original_payload_sha256: " + wrong_sha + "\n"
                "prompt_original_payload_bytes: 998\n"
                "prompt:\n"
                "  prompt_file: absent-prompt.md\n"
                "  prompt_sha256: " + wrong_sha + "\n"
                "  prompt_bytes: 999\n"
                "session_evidence:\n"
                "  - executed_prompt_snapshot_file: absent-session-prompt.md\n"
                "    executed_prompt_sha256: " + wrong_sha + "\n"
                "    executed_prompt_bytes: 999\n"
            ),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=0 ok=0 mismatch=0 path_missing=0 incomplete=0", out
        )
        self.assertNotIn("prompt_file", out)
        self.assertNotIn("executed_prompt_snapshot_file", out)
        self.assertEqual(self.findings(out), [])

    def test_empty_tree_is_incomplete(self):
        code, out, err = self.run_gate()
        self.assertEqual(code, 2)
        self.assertEqual(out.strip(), "")
        self.assertIn(
            "INCOMPLETE: invalid or absent source commit: 'HEAD'", err
        )

    def test_neighbouring_digest_key_does_not_verify_target_pair(self):
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
            self.manifest_path(): manifest,
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn(
            "pins=2 ok=0 mismatch=2 path_missing=0 incomplete=0", out
        )
        self.assert_finding(
            out,
            "HISTORICAL_REFERENCE_NOT_FOUND",
            field="authored_indexes[0].root",
            pin_id="authored_indexes[0].root",
            locator="pair-a.md",
        )
        self.assert_finding(
            out,
            "HISTORICAL_REFERENCE_NOT_FOUND",
            field="authored_indexes[0].en_mirror",
            pin_id="authored_indexes[0].en_mirror",
            locator="pair-b.md",
        )

    def test_path_key_identity_uses_en_mirror_path_not_neighbour_file(self):
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
            self.manifest_path(): manifest,
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0", out)
        self.assert_finding(
            out,
            "HISTORICAL_REFERENCE_NOT_FOUND",
            field="authored_indexes[0].en_mirror",
            pin_id="authored_indexes[0].en_mirror",
            locator="file-en.md",
        )
        self.assert_no_finding(
            out,
            "HISTORICAL_REFERENCE_NOT_FOUND",
            field="authored_indexes[0].root",
            locator="file-root.md",
        )

    def test_cross_identity_isolation_reports_only_the_wrong_pin(self):
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
            self.manifest_path(): manifest,
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0", out)
        self.assert_finding(
            out,
            "HISTORICAL_REFERENCE_NOT_FOUND",
            field="authored_indexes[1].root",
            pin_id="authored_indexes[1].root",
            locator="identity-b.md",
        )
        self.assert_no_finding(
            out,
            "HISTORICAL_REFERENCE_NOT_FOUND",
            field="authored_indexes[0].root",
            locator="identity-a.md",
        )

    def test_every_in_scope_pair_is_validated_and_out_of_scope_families_excluded(self):
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
        }

        def sha(name):
            return self.blob_sha(files[name])

        document = {
            "work_item_id": "AID-2026-900",
            "root": "top-root.md",
            "root_blob": sha("top-root.md"),
            "en_mirror": "top-en.md",
            "en_mirror_blob": sha("top-en.md"),
            "zh_cn_mirror": "top-zh.md",
            "zh_cn_mirror_blob": sha("top-zh.md"),
            "baseline_and_source_evidence": {
                "authored_indexes": [{
                    "root": "auth-root.md",
                    "root_blob": sha("auth-root.md"),
                    "en_mirror": "auth-en.md",
                    "en_mirror_blob": sha("auth-en.md"),
                    "zh_cn_mirror": "auth-zh.md",
                    "zh_cn_mirror_blob": sha("auth-zh.md"),
                }]
            },
            "related_evidence": [{
                "reference_mode": "current",
                "path": "related-path.md",
                "blob": sha("related-path.md"),
                "en_mirror": "related-en.md",
                "en_mirror_blob": sha("related-en.md"),
                "zh_cn_mirror": "related-zh.md",
                "zh_cn_mirror_blob": sha("related-zh.md"),
            }],
            "gate_a_reconstruction": [{
                "root": "historical/reconstructed.md",
                "reconstructed_root_blob": self.blob_sha(reconstructed_data),
                "source_commit": source_commit,
            }],
            "evidence_file": "execution-evidence.md",
            "evidence_blob": sha("execution-evidence.md"),
            "d_source_commit": source_commit,
            "d_source_blobs": [
                "historical/source.md: " + self.blob_sha(source_data)
            ],
        }
        candidate_files = dict(files)
        candidate_files[self.manifest_path()] = yaml.safe_dump(
            document, sort_keys=False
        )
        commit_tree(self.root, candidate_files)

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=10 ok=10 mismatch=0 path_missing=0 incomplete=0 excluded=2",
            out,
        )
        self.assertNotIn("MISMATCH", out)
        self.assertNotIn("INCOMPLETE", out)

    def test_related_evidence_mirror_pair_substitution_is_named(self):
        data_en = b"related English mirror bytes\n"
        data_zh = b"related Chinese mirror bytes\n"
        digest_zh = self.blob_sha(data_zh)
        document = {
            "work_item_id": "AID-2026-900",
            "related_evidence": [{
                "reference_mode": "current",
                "en_mirror": "related-en.md",
                "en_mirror_blob": digest_zh,
                "zh_cn_mirror": "related-zh.md",
                "zh_cn_mirror_blob": digest_zh,
            }],
        }
        commit_tree(self.root, {
            "related-en.md": data_en,
            "related-zh.md": data_zh,
            self.manifest_path(): yaml.safe_dump(document, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assertIn("pins=2 ok=1 mismatch=1 path_missing=0 incomplete=0", out)
        self.assert_finding(
            out,
            "CURRENT_REFERENCE_MISMATCH",
            field="related_evidence[0].en_mirror",
            pin_id="related_evidence[0].en_mirror",
            locator="related-en.md",
        )
        self.assert_no_finding(
            out,
            "CURRENT_REFERENCE_MISMATCH",
            field="related_evidence[0].zh_cn_mirror",
            locator="related-zh.md",
        )

    def test_later_independent_edit_does_not_invalidate_historical_reference(self):
        original = b"declared historical bytes\n"
        original_sha = self.blob_sha(original)
        first = commit_tree(self.root, {
            "evidence.md": original,
            self.manifest_path(): (
                "related_evidence:\n"
                "  - reference_mode: historical\n"
                "    path: evidence.md\n"
                f"    blob: {original_sha}\n"
            ),
        })

        (self.root / "evidence.md").write_bytes(b"later independent edit\n")
        git(self.root, "add", "evidence.md")
        git(self.root, "commit", "-m", "independent edit")
        candidate = git(self.root, "rev-parse", "HEAD")
        self.assertNotEqual(first, candidate)

        code, out, err = self.run_gate(candidate)
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)
        self.assertEqual(self.findings(out), [])

    def test_current_reference_fails_after_path_edit_without_digest_update(self):
        original = b"current evidence before edit\n"
        original_sha = self.blob_sha(original)
        commit_tree(self.root, {
            "evidence.md": original,
            self.manifest_path(): (
                "related_evidence:\n"
                "  - reference_mode: current\n"
                "    path: evidence.md\n"
                f"    blob: {original_sha}\n"
            ),
        })

        (self.root / "evidence.md").write_bytes(b"current evidence after edit\n")
        git(self.root, "add", "evidence.md")
        git(self.root, "commit", "-m", "edit current evidence")

        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        self.assert_finding(
            out,
            "CURRENT_REFERENCE_MISMATCH",
            field="related_evidence[0].path",
            pin_id="related_evidence[0].path",
            locator="evidence.md",
        )

    def test_missing_and_invalid_reference_modes_fail_closed(self):
        data = b"related evidence\n"
        sha = self.blob_sha(data)
        document = {
            "related_evidence": [
                {"path": "a.md", "blob": sha},
                {
                    "reference_mode": "candidate-ish",
                    "path": "a.md",
                    "blob": sha,
                },
            ]
        }
        commit_tree(self.root, {
            "a.md": data,
            self.manifest_path(): yaml.safe_dump(document, sort_keys=False),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 1, out + err)
        first = self.assert_finding(
            out,
            "REFERENCE_MODE_MISSING_OR_INVALID",
            field="related_evidence[0]",
            pin_id="related_evidence[0]",
            classification="policy",
        )
        second = self.assert_finding(
            out,
            "REFERENCE_MODE_MISSING_OR_INVALID",
            field="related_evidence[1]",
            pin_id="related_evidence[1]",
            classification="policy",
        )
        self.assertEqual(first.get("scope"), "related_evidence")
        self.assertEqual(second.get("scope"), "related_evidence")
        self.assertIn("pins=2", out)
        self.assertIn("incomplete=0", out)

    def test_digest_without_its_path_is_incomplete(self):
        document = {
            "authored_indexes": [{
                "root_blob": "1" * 40,
            }]
        }
        commit_tree(self.root, {
            self.manifest_path(): yaml.safe_dump(document, sort_keys=False),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        finding = self.assert_finding(
            out,
            "INCOMPLETE",
            locator="authored_indexes[0].root",
        )
        self.assertIn(
            "corresponding exact path is absent",
            finding.get("reason", ""),
        )

    def test_malformed_declaration_record_is_incomplete(self):
        commit_tree(self.root, {
            self.manifest_path(): "authored_indexes:\n  - not-a-mapping\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        finding = self.assert_finding(
            out,
            "INCOMPLETE",
            locator="authored_indexes[0]",
        )
        self.assertIn(
            "declaration record is not a mapping",
            finding.get("reason", ""),
        )

    def test_unrecognized_declaration_bearing_shape_is_incomplete(self):
        commit_tree(self.root, {
            self.manifest_path(): (
                "authored_indexes:\n"
                "  - root: file.md\n"
                "    custom_blob: " + "1" * 40 + "\n"
            ),
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        finding = self.assert_finding(
            out,
            "INCOMPLETE",
            locator="authored_indexes[0]",
        )
        self.assertIn(
            "unrecognized declaration-bearing key 'custom_blob'",
            finding.get("reason", ""),
        )

    def test_related_evidence_non_mapping_record_is_incomplete(self):
        commit_tree(self.root, {
            self.manifest_path(): "related_evidence:\n  - unexpected-scalar\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        finding = self.assert_finding(
            out,
            "INCOMPLETE",
            locator="related_evidence[0]",
        )
        self.assertIn(
            "declaration record is not a mapping",
            finding.get("reason", ""),
        )

    def test_nested_evidence_blob_is_checked_but_undefined_families_are_excluded(self):
        evidence = b"nested execution evidence\n"
        manifest = {
            "work_item_id": "AID-2026-900",
            "baseline_and_source_evidence": {
                "gate_a_reconstruction": [{
                    "root": "missing-reconstruction.md",
                    "reconstructed_root_blob": "1" * 40,
                }],
                "d_source_commit": "f" * 40,
                "d_source_blobs": [
                    "missing-source-a.md: " + "2" * 40,
                    "missing-source-b.md: " + "3" * 40,
                ],
                "evidence_file": "execution-evidence.md",
                "evidence_blob": self.blob_sha(evidence),
            },
        }
        commit_tree(self.root, {
            "execution-evidence.md": evidence,
            self.manifest_path(): yaml.safe_dump(manifest, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0 excluded=3",
            out,
        )
        self.assertEqual(self.findings(out), [])

    def test_conflicting_top_level_and_nested_family_fails_closed(self):
        top_data = b"top-level authored index\n"
        nested_data = b"nested authored index\n"
        top_sha = self.blob_sha(top_data)
        nested_sha = self.blob_sha(nested_data)
        manifest = {
            "work_item_id": "AID-2026-900",
            "authored_indexes": [{
                "root": "top.md",
                "root_blob": top_sha,
            }],
            "baseline_and_source_evidence": {
                "authored_indexes": [{
                    "root": "nested.md",
                    "root_blob": nested_sha,
                }],
            },
        }
        commit_tree(self.root, {
            "top.md": top_data,
            "nested.md": nested_data,
            self.manifest_path(): yaml.safe_dump(manifest, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        finding = self.assert_finding(
            out,
            "INCOMPLETE",
            manifest=self.manifest_path(),
        )
        self.assertIn("conflicting authored_indexes", finding.get("reason", ""))
        self.assertNotIn("pins=1 ok=1", out)

    def test_equal_top_level_and_nested_family_is_checked_once(self):
        data = b"one historical index\n"
        digest = self.blob_sha(data)
        family = [{
            "root": "same.md",
            "root_blob": digest,
        }]
        manifest = {
            "work_item_id": "AID-2026-900",
            "authored_indexes": family,
            "baseline_and_source_evidence": {
                "authored_indexes": family,
            },
        }
        commit_tree(self.root, {
            "same.md": data,
            self.manifest_path(): yaml.safe_dump(manifest, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1", out)
        self.assertEqual(self.findings(out), [])

    def test_exact_prompt_and_undefined_blob_keys_are_excluded(self):
        manifest = {
            "prompt_sha256": "0" * 64,
            "prompt_bytes": 12,
            "prompt_original_payload_sha256": "1" * 64,
            "prompt_original_payload_bytes": 13,
            "latest_invariant_source_blob": "2" * 40,
            "prior_invariant_source_blob": "3" * 40,
            "latest_forget_fence_contract_blob": "4" * 40,
            "latest_system_boundaries_blob": "5" * 40,
            "latest_context_version_blob": "6" * 40,
            "latest_applied_evidence_blob": "7" * 40,
        }
        commit_tree(self.root, {
            self.manifest_path(): yaml.safe_dump(manifest, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=0 ok=0 mismatch=0 path_missing=0 incomplete=0 excluded=10",
            out,
        )
        self.assertEqual(self.findings(out), [])

    def test_unknown_top_level_blob_key_still_fails_closed(self):
        commit_tree(self.root, {
            self.manifest_path(): "custom_blob: " + "1" * 40 + "\n",
        })
        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        finding = self.assert_finding(
            out,
            "INCOMPLETE",
            manifest=self.manifest_path(),
        )
        self.assertIn(
            "unrecognized declaration-bearing key",
            finding.get("reason", ""),
        )

    def test_out_of_scope_gate_and_d_source_families_do_not_create_findings(self):
        manifest = {
            "gate_a_reconstruction": [{
                "root": "missing.md",
                "reconstructed_root_blob": "1" * 40,
                "note": "commit " + "a" * 40,
            }],
            "d_source_commit": "f" * 40,
            "d_source_blobs": [
                "missing-a.md: " + "2" * 40,
                "missing-b.md: " + "3" * 40,
            ],
        }
        commit_tree(self.root, {
            self.manifest_path(): yaml.safe_dump(manifest, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=0 ok=0 mismatch=0 path_missing=0 incomplete=0 excluded=3",
            out,
        )
        self.assertNotIn("PATH_MISSING", out)
        self.assertNotIn("CURRENT_REFERENCE_MISMATCH", out)
        self.assertEqual(self.findings(out), [])

    def test_commit_argument_accepts_full_sha_head_remote_branch_and_local_branch(self):
        data = b"commit selector bytes\n"
        digest = self.blob_sha(data)
        commit = commit_tree(self.root, {
            "README.md": data,
            self.manifest_path(): self.manifest("README.md", digest),
        })
        git(self.root, "branch", "feature/test")
        git(self.root, "update-ref", "refs/remotes/origin/main", commit)

        for revision in (commit, "HEAD", "origin/main", "feature/test"):
            with self.subTest(revision=revision):
                code, out, err = self.run_gate(revision)
                self.assertEqual(code, 0, out + err)
                self.assertIn("pins=1 ok=1", out)

    def test_invalid_commit_argument_is_incomplete(self):
        data = b"commit selector bytes\n"
        digest = self.blob_sha(data)
        commit_tree(self.root, {
            "README.md": data,
            self.manifest_path(): self.manifest("README.md", digest),
        })
        code, out, err = self.run_gate("not-a-real-ref")
        self.assertEqual(code, 2)
        self.assertIn("INCOMPLETE:", err)

    def test_working_tree_changes_are_not_visible_to_commit_checker(self):
        data = b"committed bytes\n"
        digest = self.blob_sha(data)
        commit = commit_tree(self.root, {
            "README.md": data,
            self.manifest_path(): self.manifest("README.md", digest),
        })

        (self.root / "README.md").write_bytes(b"uncommitted replacement\n")
        code, out, err = self.run_gate(commit)
        self.assertEqual(code, 0, out + err)
        self.assertIn(f"main={commit}", out)
        self.assertEqual(self.findings(out), [])

    def test_related_evidence_counts_all_three_pairs(self):
        contents = {
            "primary.md": b"primary\n",
            "en.md": b"english\n",
            "zh.md": b"chinese\n",
        }
        document = {
            "related_evidence": [{
                "reference_mode": "current",
                "path": "primary.md",
                "blob": self.blob_sha(contents["primary.md"]),
                "en_mirror": "en.md",
                "en_mirror_blob": self.blob_sha(contents["en.md"]),
                "zh_cn_mirror": "zh.md",
                "zh_cn_mirror_blob": self.blob_sha(contents["zh.md"]),
            }]
        }
        commit_tree(self.root, {
            **contents,
            self.manifest_path(): yaml.safe_dump(document, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=3 ok=3 mismatch=0 path_missing=0 incomplete=0", out)
        self.assertEqual(self.findings(out), [])

    def test_evidence_blob_family_conflict_fails_closed(self):
        data_a = b"evidence A\n"
        data_b = b"evidence B\n"
        document = {
            "evidence_file": "a.md",
            "evidence_blob": self.blob_sha(data_a),
            "baseline_and_source_evidence": {
                "evidence_file": "b.md",
                "evidence_blob": self.blob_sha(data_b),
            },
        }
        commit_tree(self.root, {
            "a.md": data_a,
            "b.md": data_b,
            self.manifest_path(): yaml.safe_dump(document, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 2, out + err)
        finding = self.assert_finding(
            out,
            "INCOMPLETE",
            manifest=self.manifest_path(),
        )
        self.assertIn(
            "conflicting evidence_file/evidence_blob",
            finding.get("reason", ""),
        )

    def test_related_evidence_nested_family_is_resolved(self):
        data = b"nested related evidence\n"
        document = {
            "baseline_and_source_evidence": {
                "related_evidence": [{
                    "reference_mode": "current",
                    "path": "related.md",
                    "blob": self.blob_sha(data),
                }],
            }
        }
        commit_tree(self.root, {
            "related.md": data,
            self.manifest_path(): yaml.safe_dump(document, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0", out)
        self.assertEqual(self.findings(out), [])

    def test_historical_reference_in_second_merge_parent_is_found(self):
        """A historical blob reachable only through a merge's second parent counts."""
        base = commit_tree(self.root, {
            "README.md": b"base\n",
        })
        first_parent_branch = git(
            self.root, "symbolic-ref", "--short", "HEAD"
        )

        # The second parent introduces the target historical blob.
        git(self.root, "checkout", "-b", "side-history")
        historical_bytes = b"blob introduced on second parent\n"
        (self.root / "merge-only.md").write_bytes(historical_bytes)
        git(self.root, "add", "merge-only.md")
        git(self.root, "commit", "-m", "add second-parent historical blob")
        second_parent = git(self.root, "rev-parse", "HEAD")

        # The first-parent branch adds a conflicting version of the same path.
        git(self.root, "checkout", first_parent_branch)
        (self.root / "merge-only.md").write_bytes(b"first-parent version\n")
        git(self.root, "add", "merge-only.md")
        git(self.root, "commit", "-m", "add first-parent competing blob")

        # Resolve the merge by deleting the path from the merge result. The
        # target bytes therefore exist only in the second parent's history.
        merge = subprocess.run(
            ["git", "merge", "--no-commit", "--no-ff", "side-history"],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertNotEqual(merge.returncode, 0, merge.stdout + merge.stderr)
        git(self.root, "rm", "-f", "merge-only.md")
        git(self.root, "commit", "-m", "merge side history and resolve by deletion")
        merge_commit = git(self.root, "rev-parse", "HEAD")

        parents = git(self.root, "rev-list", "--parents", "-n", "1", merge_commit)
        self.assertEqual(len(parents.split()), 3, parents)
        self.assertIn(second_parent, parents.split()[1:])
        self.assertNotEqual(base, merge_commit)

        # Add the historical declaration after the merge. The candidate tree
        # has no merge-only.md; only the second-parent history has its blob.
        manifest = {
            "related_evidence": [{
                "reference_mode": "historical",
                "path": "merge-only.md",
                "blob": self.blob_sha(historical_bytes),
            }]
        }
        commit_tree(self.root, {
            self.manifest_path(): yaml.safe_dump(manifest, sort_keys=False),
        })

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn("pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0", out)
        self.assertEqual(self.findings(out), [])


class UnboundBlobSha256Test(unittest.TestCase):
    """PR #1417 comment 7212343821: an unbound blob_sha256 is a violation."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        git(self.root, "init", "-q")

    def tearDown(self):
        self.tmp.cleanup()

    def run_gate(self):
        p = subprocess.run([sys.executable, str(GATE), "--root", str(self.root),
                            "--commit", "HEAD"], text=True, capture_output=True)
        return p.returncode, p.stdout, p.stderr

    def commit_manifest(self, manifest, extra=None):
        files = {"14-ai-development/work-items/AID-2026-900/manifest.yaml": manifest}
        files.update(extra or {})
        return commit_tree(self.root, files)

    def test_bound_blob_sha256_with_matching_digest_passes(self):
        data = b"bound artifact bytes\n"
        manifest = ("work_item_id: AID-2026-900\n"
                    "artifact_pins:\n"
                    "  model_path: model.md\n"
                    f"  model_blob_sha256: \"{hashlib.sha256(data).hexdigest()}\"\n")
        self.commit_manifest(manifest, {"model.md": data})

        code, out, err = self.run_gate()
        self.assertEqual(code, 0, out + err)
        self.assertIn(
            "pins=1 ok=1 mismatch=0 path_missing=0 incomplete=0 "
            "excluded=0 unbound=0",
            out,
        )
        self.assertNotIn("UNBOUND_BLOB_SHA256", out)

    def test_bound_blob_sha256_with_wrong_digest_is_mismatch(self):
        data = b"bound artifact bytes\n"
        wrong = "0" * 64
        manifest = ("work_item_id: AID-2026-900\n"
                    "artifact_pins:\n"
                    "  model_path: model.md\n"
                    f"  model_blob_sha256: \"{wrong}\"\n")
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
        manifest = ("work_item_id: AID-2026-900\n"
                    "artifact_pins:\n"
                    "  model_path: absent.md\n"
                    f"  model_blob_sha256: \"{digest}\"\n")
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
        manifest = ("work_item_id: AID-2026-900\n"
                    "measurement_basis:\n"
                    f"  model_blob_sha256_lf: \"{digest}\"\n")
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
