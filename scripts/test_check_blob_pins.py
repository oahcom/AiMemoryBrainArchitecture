#!/usr/bin/env python3
"""Tests for check_blob_pins.py using temporary Git repositories."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_blob_pins.py").resolve()
EMPTY_BASELINE = "empty-baseline.txt"


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise AssertionError(proc.stderr)
    return proc.stdout.strip()


def blob_oid(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


class BlobPinCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "user.name", "Blob Pin Tests")

        (self.repo / "14-ai-development/work-items/AID-2026-001").mkdir(
            parents=True
        )
        (self.repo / "docs").mkdir()
        (self.repo / "docs/en.md").write_bytes(b"english\n")
        (self.repo / "docs/zh.md").write_bytes(b"chinese\n")

        self.write_manifest(
            """
work_item_id: AID-2026-001
prompt_file: docs/en.md
prompt_file_blob_sha: PLACEHOLDER
prompt_file_commit_sha: COMMIT
"""
        )
        self.commit_all()
        self.replace_manifest_values()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @property
    def manifest(self) -> Path:
        return (
            self.repo / "14-ai-development/work-items/AID-2026-001/manifest.yaml"
        )

    @property
    def empty_baseline(self) -> Path:
        return self.repo / EMPTY_BASELINE

    def write_manifest(self, content: str) -> None:
        self.manifest.write_text(content.lstrip(), encoding="utf-8")

    def commit_all(self) -> str:
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", "fixture")
        return git(self.repo, "rev-parse", "HEAD")

    def replace_manifest_values(self) -> None:
        commit = git(self.repo, "rev-parse", "HEAD")
        oid = git(self.repo, "rev-parse", "HEAD:docs/en.md")
        content = self.manifest.read_text(encoding="utf-8")
        content = content.replace("PLACEHOLDER", oid)
        content = content.replace("COMMIT", commit)
        self.manifest.write_text(content, encoding="utf-8")
        self.commit_all()

    def remove_prompt_commit_base(self) -> None:
        content = self.manifest.read_text(encoding="utf-8")
        content = "\n".join(
            line for line in content.splitlines()
            if not line.startswith("prompt_file_commit_sha:")
        ) + "\n"
        self.manifest.write_text(content, encoding="utf-8")

    def run_checker(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repo",
                str(self.repo),
                *args,
            ],
            text=True,
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_valid_pin_has_zero_path_missing_summary(self) -> None:
        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        # The declared commit is historical and contains the pinned blob.
        self.assertIn("PATH_MISSING=0", proc.stdout)
        self.assertIn("BAD=0", proc.stdout)
        self.assertNotIn("\n001. ", proc.stdout)

    def test_historical_commit_pin_is_unchanged_when_head_changes(self) -> None:
        # The fixture's prompt_file_commit_sha points to the commit before
        # the manifest was updated. Changing HEAD must not change that base.
        (self.repo / "docs/en.md").write_bytes(b"changed in later HEAD\n")
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("PINS=1", proc.stdout)
        self.assertIn("MISMATCH=0", proc.stdout)
        self.assertIn("PATH_MISSING=0", proc.stdout)

    def test_changed_file_at_head_base_produces_mismatch_with_path(self) -> None:
        self.remove_prompt_commit_base()
        (self.repo / "docs/en.md").write_bytes(b"changed\n")
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("MISMATCH", proc.stdout)
        self.assertIn("path=docs/en.md", proc.stdout)
        self.assertIn("field=prompt_file_blob_sha", proc.stdout)
        self.assertIn("declared=", proc.stdout)
        self.assertIn("actual=", proc.stdout)
        self.assertIn("base=", proc.stdout)

    def test_deleted_path_is_path_missing_and_includes_path(self) -> None:
        self.remove_prompt_commit_base()
        (self.repo / "docs/en.md").unlink()
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("PATH_MISSING", proc.stdout)
        self.assertIn("path=docs/en.md", proc.stdout)

    def test_baseline_emit_then_new_finding_fails(self) -> None:
        old_en = git(self.repo, "rev-parse", "HEAD:docs/en.md")
        (self.repo / "docs/en.md").write_bytes(b"changed english\n")
        self.write_manifest(
            f"""
files:
  - path: docs/en.md
    sha: {old_en}
"""
        )
        self.commit_all()

        baseline = self.repo / "generated-baseline.txt"
        emitted = self.run_checker("--emit-baseline", str(baseline))
        self.assertEqual(emitted.returncode, 0, emitted.stdout + emitted.stderr)
        lines = baseline.read_text(encoding="utf-8").splitlines()
        self.assertTrue(lines)
        self.assertTrue(all(not line.startswith("NNN. ") for line in lines))
        self.assertTrue(all(" path=" in line for line in lines))

        ratcheted = self.run_checker("--baseline", str(baseline))
        self.assertEqual(ratcheted.returncode, 0, ratcheted.stdout)
        self.assertIn("NEW_FINDINGS=0", ratcheted.stdout)
        self.assertIn("STALE_BASELINE_ITEMS=0", ratcheted.stdout)

        old_zh = git(self.repo, "rev-parse", "HEAD:docs/zh.md")
        content = self.manifest.read_text(encoding="utf-8")
        content += (
            "  - path: docs/zh.md\n"
            f"    sha: {old_zh}\n"
        )
        self.manifest.write_text(content, encoding="utf-8")
        (self.repo / "docs/zh.md").write_bytes(b"changed chinese\n")
        self.commit_all()

        added = self.run_checker("--baseline", str(baseline))
        self.assertEqual(added.returncode, 1, added.stdout + added.stderr)
        self.assertIn("NEW_FINDINGS=1", added.stdout)

    def test_removing_a_finding_makes_baseline_stale_and_fails(self) -> None:
        old_en = git(self.repo, "rev-parse", "HEAD:docs/en.md")
        old_zh = git(self.repo, "rev-parse", "HEAD:docs/zh.md")
        (self.repo / "docs/en.md").write_bytes(b"changed english\n")
        (self.repo / "docs/zh.md").write_bytes(b"changed chinese\n")
        self.write_manifest(
            f"""
files:
  - path: docs/en.md
    sha: {old_en}
  - path: docs/zh.md
    sha: {old_zh}
"""
        )
        self.commit_all()

        baseline = self.repo / "generated-baseline.txt"
        emitted = self.run_checker("--emit-baseline", str(baseline))
        self.assertEqual(emitted.returncode, 0, emitted.stdout + emitted.stderr)
        self.assertEqual(len(baseline.read_text(encoding="utf-8").splitlines()), 2)

        current_zh = git(self.repo, "rev-parse", "HEAD:docs/zh.md")
        self.write_manifest(
            f"""
files:
  - path: docs/en.md
    sha: {old_en}
  - path: docs/zh.md
    sha: {current_zh}
"""
        )
        self.commit_all()

        stale = self.run_checker("--baseline", str(baseline))
        self.assertEqual(stale.returncode, 1, stale.stdout + stale.stderr)
        self.assertIn("NEW_FINDINGS=0", stale.stdout)
        self.assertIn("STALE_BASELINE_ITEMS=1", stale.stdout)

    def test_every_repeated_blob_key_is_accounted_for(self) -> None:
        self.write_manifest(
            """
work_item_id: AID-2026-001
one_blob: 1111111111111111111111111111111111111111
nested:
  two_blob: 2222222222222222222222222222222222222222
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("OUT_OF_SCOPE=2", proc.stdout)
        self.assertIn("OUT_OF_SCOPE_KEY one_blob=1", proc.stdout)
        self.assertIn("OUT_OF_SCOPE_KEY two_blob=1", proc.stdout)

    def test_sha_with_path_is_a_pin(self) -> None:
        oid = git(self.repo, "rev-parse", "HEAD:docs/en.md")
        self.write_manifest(
            f"""
verification_status:
  files:
    - path: docs/en.md
      sha: {oid}
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PINS=1", proc.stdout)
        self.assertIn("BAD=0", proc.stdout)

    def test_sha_without_path_is_out_of_scope(self) -> None:
        self.write_manifest(
            """
verification_status:
  sha: 1111111111111111111111111111111111111111
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PINS=0", proc.stdout)
        self.assertIn("OUT_OF_SCOPE_KEY sha=1", proc.stdout)

    def test_frontmatter_digest_is_out_of_scope(self) -> None:
        self.write_manifest(
            """
records:
  - path: docs/en.md
    frontmatter_blob_sha: 1111111111111111111111111111111111111111
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PINS=0", proc.stdout)
        self.assertIn("OUT_OF_SCOPE_KEY frontmatter_blob_sha=1", proc.stdout)

    def test_prose_commit_sentinels_are_out_of_scope_not_invalid(self) -> None:
        sentinels = (
            "NOT_SEPARATELY_COMMITTED (same commit as registration package)",
            "NOT_VERIFIED",
            "NOT_AVAILABLE pending evidence",
            "N/A",
        )
        for sentinel in sentinels:
            with self.subTest(sentinel=sentinel):
                oid = git(self.repo, "rev-parse", "HEAD:docs/en.md")
                self.write_manifest(
                    f"""
prompt_file: docs/en.md
prompt_file_blob_sha: {oid}
prompt_file_commit_sha: "{sentinel}"
"""
                )
                self.commit_all()
                proc = self.run_checker("--baseline", str(self.empty_baseline))
                self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                self.assertIn("PINS=0", proc.stdout)
                self.assertIn("INVALID=0", proc.stdout)
                self.assertIn(
                    "OUT_OF_SCOPE_KEY prompt_file_blob_sha=1", proc.stdout
                )

    def test_relative_snapshot_file_is_posix_and_platform_independent(self) -> None:
        manifest_dir = (
            self.repo / "14-ai-development/work-items/AID-2026-001"
        )
        snapshot = manifest_dir / "snapshot.md"
        snapshot.write_bytes(b"snapshot content\n")
        old_oid = blob_oid(b"snapshot content\n")
        self.write_manifest(
            f"""
snapshot_file: snapshot.md
snapshot_git_blob_sha: {old_oid}
"""
        )
        self.commit_all()

        # Force a mismatch so the normalized path is observable in a finding.
        snapshot.write_bytes(b"changed snapshot\n")
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        expected = (
            "path=14-ai-development/work-items/AID-2026-001/snapshot.md"
        )
        self.assertIn(expected, proc.stdout)
        self.assertNotIn(
            "path=14-ai-development\\work-items\\AID-2026-001\\snapshot.md",
            proc.stdout,
        )

    def test_current_main_blobs_classifies_older_same_file_pin_as_history(self) -> None:
        current_oid = git(self.repo, "rev-parse", "HEAD:docs/en.md")
        self.write_manifest(
            f"""
current_main_blobs:
  en_md: {current_oid}
records:
  - file: docs/en.md
    git_blob_sha: 1111111111111111111111111111111111111111
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("PINS=0", proc.stdout)
        self.assertIn("OUT_OF_SCOPE_KEY git_blob_sha=1", proc.stdout)
        self.assertIn("MISMATCH=0", proc.stdout)

    def test_read_observation_classifies_blob_pin_as_history(self) -> None:
        self.write_manifest(
            """
number_allocation:
  evidence:
    - kind: main_INDEX_read
      path: docs/en.md
      blob_sha: 1111111111111111111111111111111111111111
      observation: AID-2026-001 was not present in the inspected INDEX.
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("PINS=0", proc.stdout)
        self.assertIn("OUT_OF_SCOPE_KEY blob_sha=1", proc.stdout)
        self.assertIn("MISMATCH=0", proc.stdout)

    def test_source_files_blob_uses_source_head(self) -> None:
        old_head = git(self.repo, "rev-parse", "HEAD")
        old_blob = git(self.repo, "rev-parse", "HEAD:docs/en.md")

        (self.repo / "docs/en.md").write_bytes(b"new HEAD content\n")
        new_head = self.commit_all()

        self.write_manifest(
            f"""
source:
  head: {old_head}
  files:
    - path: docs/en.md
      blob: {old_blob}
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("PINS=1", proc.stdout)
        self.assertIn("MISMATCH=0", proc.stdout)
        self.assertNotIn(f"base={new_head}", proc.stdout)

    def test_invalid_commit_is_finding_not_silently_skipped(self) -> None:
        oid = git(self.repo, "rev-parse", "HEAD:docs/en.md")
        self.write_manifest(
            f"""
prompt_file: docs/en.md
prompt_file_blob_sha: {oid}
prompt_file_commit_sha: not-a-commit
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("INVALID", proc.stdout)
        self.assertIn("path=docs/en.md", proc.stdout)

    def test_findings_have_stable_numbered_prefix(self) -> None:
        self.write_manifest(
            """
a:
  prompt_file: docs/en.md
  prompt_file_blob_sha: 1111111111111111111111111111111111111111
b:
  prompt_file: docs/zh.md
  prompt_file_blob_sha: 2222222222222222222222222222222222222222
"""
        )
        self.commit_all()

        proc = self.run_checker("--baseline", str(self.empty_baseline))
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        finding_lines = [
            line for line in proc.stdout.splitlines()
            if line[:3].isdigit() and line[3:5] == ". "
        ]
        self.assertEqual(len(finding_lines), 2)
        self.assertTrue(finding_lines[0].startswith("001. "))
        self.assertTrue(finding_lines[1].startswith("002. "))
        self.assertIn("path=docs/en.md", finding_lines[0])
        self.assertIn("path=docs/zh.md", finding_lines[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
