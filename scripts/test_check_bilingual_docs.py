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
        encoding="utf-8",
        errors="replace",
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
    root: Path,
    base: str,
    head: str,
    body: str = "",
    baseline: tuple[str, ...] = (),
    ratchet_baseline: tuple[str, ...] | None = None,
) -> tuple[int, str]:
    """Run main() over a fixture repo with real-repository checks stubbed out."""
    baseline_path = root / "scripts" / "bilingual-baseline.txt"
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_path.write_text(
        "".join(f"{entry}\n" for entry in baseline), encoding="utf-8"
    )
    # The ratchet copy defaults to the same entries; pass ratchet_baseline to
    # exercise the cross-copy comparison.
    ratchet_path = root / "scripts" / "ci" / "baselines" / "bilingual-docs.txt"
    ratchet_path.parent.mkdir(parents=True, exist_ok=True)
    ratchet_entries = baseline if ratchet_baseline is None else ratchet_baseline
    ratchet_path.write_text(
        "".join(f"{entry}\n" for entry in ratchet_entries), encoding="utf-8"
    )
    output, errors = io.StringIO(), io.StringIO()
    with (
        patch.object(GATE, "ROOT", root),
        patch.object(GATE, "BASELINE_PATH", baseline_path),
        patch.object(GATE, "CI_BASELINE_PATH", ratchet_path),
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


BASELINE_HEADER = (
    "# Frozen inventory of pre-existing bilingual documentation gaps.\n"
    "# This baseline may only shrink; entries must never be added.\n"
    "# Regenerate only when explicitly adopting a new baseline.\n"
)


def run_write_baseline(
    root: Path, gaps: tuple[str, ...], baseline: tuple[str, ...]
) -> tuple[int, str, Path]:
    """Run write_baseline() over a committed fixture baseline."""
    baseline_path = root / "scripts" / "bilingual-baseline.txt"
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_path.write_text(
        BASELINE_HEADER + "".join(f"{entry}\n" for entry in baseline),
        encoding="utf-8",
    )
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "baseline")
    output, errors = io.StringIO(), io.StringIO()
    with (
        patch.object(GATE, "ROOT", root),
        patch.object(GATE, "BASELINE_PATH", baseline_path),
        patch.object(GATE, "current_bilingual_gaps", return_value=set(gaps)),
        contextlib.redirect_stdout(output),
        contextlib.redirect_stderr(errors),
    ):
        code = GATE.write_baseline()
    return code, output.getvalue() + errors.getvalue(), baseline_path



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


class BaselineCopyConsistencyTests(unittest.TestCase):
    """The two frozen inventories must hold the same entry set."""

    def test_identical_copies_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_repo(root)
            gap = "06-memory-context/context-gap-fixture.md"
            base = commit_file(root, gap)
            head = commit_file(root, "14-ai-development/work-items/INDEX.md")
            code, combined = run_gate(root, base, head, baseline=(gap,))
            self.assertEqual(code, 0, combined)
            self.assertNotIn("baseline copies disagree", combined)

    def test_entry_only_in_frozen_copy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = make_repo(root)
            head = commit_file(root, "14-ai-development/work-items/INDEX.md")
            code, combined = run_gate(
                root,
                base,
                head,
                baseline=("a/x.md", "b/y.md"),
                ratchet_baseline=("a/x.md",),
            )
            self.assertEqual(code, 2, combined)
            self.assertIn("::error::", combined)
            self.assertIn(
                "present only in scripts/bilingual-baseline.txt: b/y.md", combined
            )

    def test_entry_only_in_ratchet_copy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = make_repo(root)
            head = commit_file(root, "14-ai-development/work-items/INDEX.md")
            code, combined = run_gate(
                root,
                base,
                head,
                baseline=("a/x.md",),
                ratchet_baseline=("a/x.md", "b/y.md"),
            )
            self.assertEqual(code, 2, combined)
            self.assertIn(
                "present only in scripts/ci/baselines/bilingual-docs.txt: b/y.md",
                combined,
            )

    def test_comments_and_blanks_are_not_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frozen = root / "scripts" / "bilingual-baseline.txt"
            ratchet = root / "scripts" / "ci" / "baselines" / "bilingual-docs.txt"
            ratchet.parent.mkdir(parents=True)
            frozen.parent.mkdir(parents=True, exist_ok=True)
            frozen.write_text("# header\n\na/x.md\n", encoding="utf-8")
            ratchet.write_text("a/x.md\n\n# other header\n", encoding="utf-8")
            with (
                patch.object(GATE, "ROOT", root),
                patch.object(GATE, "BASELINE_PATH", frozen),
                patch.object(GATE, "CI_BASELINE_PATH", ratchet),
            ):
                self.assertEqual(GATE.check_baseline_copies_agree(), [])

    def test_missing_ratchet_copy_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frozen = root / "scripts" / "bilingual-baseline.txt"
            frozen.parent.mkdir(parents=True, exist_ok=True)
            frozen.write_text("a/x.md\n", encoding="utf-8")
            with (
                patch.object(GATE, "ROOT", root),
                patch.object(GATE, "BASELINE_PATH", frozen),
                patch.object(GATE, "CI_BASELINE_PATH", root / "scripts" / "ci" / "baselines" / "bilingual-docs.txt"),
            ):
                errors = GATE.check_baseline_copies_agree()
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("ratchet baseline is missing", errors[0])


class WriteBaselineShrinkOnlyTests(unittest.TestCase):
    """`--write-baseline` must refuse to raise the frozen inventory."""

    def test_added_entry_refuses_and_leaves_file_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_repo(root)
            code, combined, baseline_path = run_write_baseline(
                root, gaps=("a/x.md", "b/new.md"), baseline=("a/x.md",)
            )
            self.assertEqual(code, 2, combined)
            self.assertIn("may only shrink", combined)
            self.assertIn("b/new.md", combined)
            self.assertNotIn("baseline written", combined)
            self.assertEqual(
                baseline_path.read_text(encoding="utf-8"),
                BASELINE_HEADER + "a/x.md\n",
            )

    def test_shrinking_set_is_written(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_repo(root)
            code, combined, baseline_path = run_write_baseline(
                root, gaps=("a/x.md",), baseline=("a/x.md", "b/y.md")
            )
            self.assertEqual(code, 0, combined)
            self.assertIn("baseline written: 1 entries", combined)
            self.assertEqual(
                baseline_path.read_text(encoding="utf-8"),
                BASELINE_HEADER + "a/x.md\n",
            )

    def test_missing_current_baseline_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_repo(root)
            baseline_path = root / "scripts" / "bilingual-baseline.txt"
            output, errors = io.StringIO(), io.StringIO()
            with (
                patch.object(GATE, "ROOT", root),
                patch.object(GATE, "BASELINE_PATH", baseline_path),
                patch.object(GATE, "current_bilingual_gaps", return_value={"a/x.md"}),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(errors),
            ):
                code = GATE.write_baseline()
            combined = output.getvalue() + errors.getvalue()
            self.assertEqual(code, 2, combined)
            self.assertIn("cannot prove the new baseline only shrinks", combined)
            self.assertFalse(baseline_path.exists())


class GitOutputDecodingTests(unittest.TestCase):
    """Git output is decoded as UTF-8, never with the console's locale codec."""

    def test_undecodable_blob_names_the_decode_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_repo(root)
            # A blob Git stores happily and no UTF-8 reader can decode. On a
            # GBK console `text=True` raised UnicodeDecodeError and `git show`
            # returned None; the caller then crashed (AID-173) or, in DM-10,
            # reported a file absent that it had never read.
            stored = subprocess.run(
                ["git", "-C", str(root), "hash-object", "-w", "--stdin"],
                input=b"---\ndocument_metadata:\n\xff\xfe not utf-8\n---\n",
                capture_output=True,
                check=True,
            ).stdout.decode("ascii").strip()
            with patch.object(GATE, "ROOT", root):
                with self.assertRaises(GATE.GitOutputDecodeError) as caught:
                    GATE._git_log_output("show", stored)
            message = str(caught.exception)
            self.assertIn("decode", message)
            self.assertNotIn("not exist", message)

    def test_main_reports_decode_failure_as_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = make_repo(root)
            head = commit_file(root, "docs/zh-CN/00-governance/x.md")
            baseline_path = root / "scripts" / "bilingual-baseline.txt"
            baseline_path.parent.mkdir(parents=True, exist_ok=True)
            baseline_path.write_text("", encoding="utf-8")
            ratchet_path = root / "scripts" / "ci" / "baselines" / "bilingual-docs.txt"
            ratchet_path.parent.mkdir(parents=True, exist_ok=True)
            ratchet_path.write_text("", encoding="utf-8")
            output, errors = io.StringIO(), io.StringIO()
            with (
                patch.object(GATE, "ROOT", root),
                patch.object(GATE, "BASELINE_PATH", baseline_path),
                patch.object(GATE, "CI_BASELINE_PATH", ratchet_path),
                patch.object(GATE, "_require_full_git_history"),
                patch.object(GATE, "check_prompt_library", return_value=[]),
                patch.object(
                    GATE,
                    "check_embedded_registration_history",
                    side_effect=GATE.GitOutputDecodeError(
                        "git output decode failed (utf-8) while reading git show"
                    ),
                ),
                patch.dict(os.environ, {"BASE_SHA": base, "HEAD_SHA": head}),
                patch.object(sys, "argv", ["check_bilingual_docs.py"]),
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(errors),
            ):
                code = GATE.main()
            combined = output.getvalue() + errors.getvalue()
            # Incomplete (2), not a content verdict (1), and not a traceback.
            self.assertEqual(code, 2, combined)
            self.assertIn("decode", combined)


if __name__ == "__main__":
    unittest.main(verbosity=2)
