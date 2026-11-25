#!/usr/bin/env python3
"""Regression tests for GOV-DOC-001 changed-path fail-closed behavior."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).with_name("check_bilingual_docs.py")
SPEC = importlib.util.spec_from_file_location("check_bilingual_docs_under_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def make_repo(root: Path) -> str:
    git(root, "init", "-q")
    git(root, "config", "user.email", "gate@example.invalid")
    git(root, "config", "user.name", "gate-test")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "seed")
    return git(root, "rev-parse", "HEAD")


def commit_file(root: Path, rel: str) -> str:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# fixture\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", f"add {rel}")
    return git(root, "rev-parse", "HEAD")


def run_gate(
    root: Path, base: str, head: str, body: str = "", baseline: tuple[str, ...] = ()
) -> tuple[int, str]:
    """Run main() over a fixture repo with real-repository checks stubbed out."""
    baseline_path = root / "scripts" / "bilingual-baseline.txt"
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_path.write_text(
        "".join(f"{entry}\n" for entry in baseline), encoding="utf-8"
    )
    output, errors = io.StringIO(), io.StringIO()
    with (
        patch.object(GATE, "ROOT", root),
        patch.object(GATE, "BASELINE_PATH", baseline_path),
        patch.object(GATE, "_require_full_git_history"),
        patch.object(GATE, "check_prompt_library", return_value=[]),
        patch.object(GATE, "check_embedded_registration_history", return_value=[]),
        patch.dict(os.environ, {"BASE_SHA": base, "HEAD_SHA": head, "PR_BODY": body}),
        patch.object(sys, "argv", ["check_bilingual_docs.py"]),
        contextlib.redirect_stdout(output),
        contextlib.redirect_stderr(errors),
    ):
        code = GATE.main()
    return code, output.getvalue() + errors.getvalue()


class ChangedPathTests(unittest.TestCase):
    def test_same_head_is_not_applicable_not_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            head = make_repo(root)
            output, errors = io.StringIO(), io.StringIO()
            with (
                patch.object(GATE, "ROOT", root),
                patch.object(GATE, "_require_full_git_history"),
                patch.dict(os.environ, {"BASE_SHA": head, "HEAD_SHA": head}),
                patch.object(sys, "argv", ["check_bilingual_docs.py"]),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(errors),
            ):
                code = GATE.main()
            combined = output.getvalue() + errors.getvalue()
            self.assertEqual(code, 2, combined)
            self.assertIn("NOT_APPLICABLE", combined)
            self.assertNotIn("PASS", combined)

    def test_invalid_base_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            head = make_repo(root)
            output, errors = io.StringIO(), io.StringIO()
            with (
                patch.object(GATE, "ROOT", root),
                patch.object(GATE, "_require_full_git_history"),
                patch.dict(os.environ, {"BASE_SHA": "deadbeef", "HEAD_SHA": head}),
                patch.object(sys, "argv", ["check_bilingual_docs.py"]),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(errors),
            ):
                code = GATE.main()
            combined = output.getvalue() + errors.getvalue()
            self.assertEqual(code, 2, combined)
            self.assertIn("Unable to determine changed paths", combined)

    def test_nonempty_code_only_change_is_not_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = make_repo(root)
            (root / "src").mkdir()
            (root / "src" / "only.rs").write_text("// code-only\n", encoding="utf-8")
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "code-only")
            head = git(root, "rev-parse", "HEAD")
            with (
                patch.object(GATE, "ROOT", root),
                patch.dict(os.environ, {"BASE_SHA": base, "HEAD_SHA": head}),
            ):
                self.assertEqual(GATE.changed_status(), {"src/only.rs": "A"})

    def test_pair_exempt_work_item_doc_needs_no_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = make_repo(root)
            head = commit_file(root, "14-ai-development/work-items/INDEX.md")
            code, combined = run_gate(root, base, head)
            self.assertEqual(code, 0, combined)
            self.assertNotIn("BILINGUAL-MANIFEST", combined)

    def test_pair_exempt_adr_needs_no_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = make_repo(root)
            head = commit_file(root, "14-ai-development/adr/ADR-001-fixture.md")
            code, combined = run_gate(root, base, head)
            self.assertEqual(code, 0, combined)

    def test_non_exempt_14_doc_still_needs_manifest(self) -> None:
        rel = "14-ai-development/spec-fixture.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = make_repo(root)
            head = commit_file(root, rel)
            code, combined = run_gate(root, base, head, baseline=(rel,))
            self.assertEqual(code, 1, combined)
            self.assertIn(rel, combined)

    def test_pair_checked_normative_doc_still_needs_manifest(self) -> None:
        rel = "06-memory-context/context-implementation-coverage.md"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = make_repo(root)
            head = commit_file(root, rel)
            code, combined = run_gate(root, base, head, baseline=(rel,))
            self.assertEqual(code, 1, combined)
            self.assertIn(rel, combined)
            self.assertIn("BILINGUAL-MANIFEST: COMPLETE", combined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
