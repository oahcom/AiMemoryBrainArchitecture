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


class ChangedPathTests(unittest.TestCase):
    def test_same_head_is_not_applicable_not_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            head = make_repo(root)
            output, errors = io.StringIO(), io.StringIO()
            with (
                patch.object(GATE, "REPO_ROOT", root),
                patch.object(GATE, "_require_full_git_history"),
                patch.dict(os.environ, {"BASE_SHA": head, "HEAD_SHA": head}),
                patch.object(sys, "argv", ["check_bilingual_docs.py"]),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(errors),
            ):
                code = GATE.main()
            self.assertEqual(code, 2, output.getvalue() + errors.getvalue())
            self.assertIn("NOT_APPLICABLE", errors.getvalue())
            self.assertNotIn("PASS", output.getvalue() + errors.getvalue())

    def test_invalid_base_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            head = make_repo(root)
            output, errors = io.StringIO(), io.StringIO()
            with (
                patch.object(GATE, "REPO_ROOT", root),
                patch.object(GATE, "_require_full_git_history"),
                patch.dict(os.environ, {"BASE_SHA": "deadbeef", "HEAD_SHA": head}),
                patch.object(sys, "argv", ["check_bilingual_docs.py"]),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(errors),
            ):
                code = GATE.main()
            self.assertEqual(code, 2, output.getvalue() + errors.getvalue())
            self.assertIn("Unable to determine changed paths", errors.getvalue())

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
                patch.object(GATE, "REPO_ROOT", root),
                patch.dict(os.environ, {"BASE_SHA": base, "HEAD_SHA": head}),
            ):
                self.assertEqual(GATE.changed_status(), {"src/only.rs": "A"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
