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


class BaselineCopyRegistryTests(unittest.TestCase):
    """Every copy of the frozen inventory is declared, marked, or red."""

    COPIES = {relative: role for relative, role, _why in GATE.BASELINE_COPIES}
    BMCP_EN = "reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md"
    BMCP_ZH = "reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md"
    REGISTER = "14-ai-development/governance-register/evidence/main-paths.json"
    SNAPSHOT = "00-governance/reports/gov-doc-001-full-scan-2026-11-20.md"

    def _write(self, root: Path, relative: str, text: str) -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _tree(
        self,
        root: Path,
        authority: tuple[str, ...],
        live: tuple[str, ...] | None = None,
    ) -> None:
        """Write the two baselines plus every declared copy that a test needs."""
        frozen = root / "scripts" / "bilingual-baseline.txt"
        frozen.parent.mkdir(parents=True, exist_ok=True)
        entries = authority if live is None else live
        frozen.write_text("".join(f"{entry}\n" for entry in entries), encoding="utf-8")
        ratchet = root / "scripts" / "ci" / "baselines" / "bilingual-docs.txt"
        ratchet.parent.mkdir(parents=True, exist_ok=True)
        ratchet.write_text("".join(f"{entry}\n" for entry in authority), encoding="utf-8")

    def _check(self, root: Path) -> tuple[list[str], str]:
        output = io.StringIO()
        with (
            patch.object(GATE, "ROOT", root),
            patch.object(GATE, "BASELINE_PATH", root / "scripts" / "bilingual-baseline.txt"),
            patch.object(
                GATE,
                "CI_BASELINE_PATH",
                root / "scripts" / "ci" / "baselines" / "bilingual-docs.txt",
            ),
            contextlib.redirect_stdout(output),
        ):
            errors = GATE.check_baseline_copies_agree()
        return errors, output.getvalue()

    def test_registry_declares_every_role(self) -> None:
        """The registry names one authority, one live copy, and the rest."""
        roles = [role for _relative, role, _why in GATE.BASELINE_COPIES]
        self.assertEqual(roles.count("authority"), 1, roles)
        self.assertEqual(
            [relative for relative, role, _w in GATE.BASELINE_COPIES if role == "authority"],
            ["scripts/ci/baselines/bilingual-docs.txt"],
        )
        self.assertIn("live", roles)
        self.assertEqual(len(set(self.COPIES)), len(GATE.BASELINE_COPIES))

    def test_all_declared_copies_agreeing_passes(self) -> None:
        entries = ("a/x.md", "b/y.md")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._tree(root, entries)
            self._write(
                root,
                self.BMCP_EN,
                "| 01 | `a/x.md` |\n"
                f"> {GATE.BASELINE_COPY_MARKER}\n",
            )
            self._write(
                root,
                self.BMCP_ZH,
                "| 01 | `a/x.md` |\n"
                f"> {GATE.BASELINE_COPY_MARKER}\n",
            )
            self._write(root, self.REGISTER, '[\n"a/x.md",\n"b/y.md",\n"c/z.md"\n]\n')
            self._write(
                root,
                self.SNAPSHOT,
                "- Source revision / 扫描源 Commit: "
                "`568b847ce39f30071f35355ee0fb6f2300e00708`\n"
                "| 1 | `a/x.md` |\n",
            )
            errors, output = self._check(root)
            self.assertEqual(errors, [])
            self.assertNotIn("::error::", output)

    def test_historical_snapshot_without_marker_fails(self) -> None:
        """The drifted 81-entry snapshot must carry the marker, not just exist."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._tree(root, ("a/x.md",))
            self._write(root, self.BMCP_EN, "| 01 | `a/x.md` |\n")
            errors, _output = self._check(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn(self.BMCP_EN, errors[0])
            self.assertIn(GATE.BASELINE_COPY_MARKER, errors[0])

    def test_historical_snapshot_drift_is_a_notice_not_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._tree(root, ("a/x.md", "b/y.md"))
            self._write(
                root,
                self.BMCP_EN,
                f"> {GATE.BASELINE_COPY_MARKER}\n"
                "| 01 | `a/x.md` |\n| 02 | `c/z.md` |\n",
            )
            errors, output = self._check(root)
            self.assertEqual(errors, [])
            self.assertIn("::notice::", output)
            self.assertIn("informational only", output)
            self.assertIn(self.BMCP_EN, output)

    def test_register_missing_a_frozen_entry_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._tree(root, ("a/x.md", "b/y.md"))
            self._write(root, self.REGISTER, '[\n"a/x.md"\n]\n')
            errors, _output = self._check(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("b/y.md", errors[0])
            self.assertIn(self.REGISTER, errors[0])

    def test_snapshot_without_revision_declaration_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._tree(root, ("a/x.md",))
            self._write(root, self.SNAPSHOT, "| 1 | `a/x.md` |\n")
            errors, _output = self._check(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn(self.SNAPSHOT, errors[0])
            self.assertIn("source revision", errors[0])

    def test_undeclared_copy_of_the_inventory_fails(self) -> None:
        """A new copy that nobody declared is red even when it mostly agrees."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_repo(root)
            self._tree(root, ("a/x.md",))
            self._write(root, "notes/inventory.md", "- `a/x.md`\n- `b/drift.md`\n")
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "undeclared copy")
            errors, _output = self._check(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("notes/inventory.md", errors[0])
            self.assertIn("not a declared copy", errors[0])

    def test_marked_undeclared_snapshot_is_a_notice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make_repo(root)
            self._tree(root, ("a/x.md",))
            self._write(
                root,
                "notes/inventory.md",
                f"> {GATE.BASELINE_COPY_MARKER}\n- `a/x.md`\n- `b/drift.md`\n",
            )
            git(root, "add", "-A")
            git(root, "commit", "-q", "-m", "marked snapshot")
            errors, output = self._check(root)
            self.assertEqual(errors, [])
            self.assertIn("notes/inventory.md", output)

    def test_this_repository_has_no_undeclared_inventory_copy(self) -> None:
        """The real tree keeps exactly the copies the registry declares."""
        authority = GATE.read_baseline_entries(GATE.CI_BASELINE_PATH)
        self.assertIsNotNone(authority)
        declared = {relative for relative, _role, _why in GATE.BASELINE_COPIES}
        self.assertEqual(GATE._undeclared_copies(authority, declared), [])

    def test_entry_shapes_are_read_from_every_copy_format(self) -> None:
        text = (
            "00-governance/a.md\n"
            "| 07 | `06-memory-context/b.md` | note |\n"
            '  "13-engineering-decisions/c.md",\n'
            "- `13-engineering-decisions/d.md`\n"
        )
        self.assertEqual(
            GATE.inventory_entries_in(text),
            {
                "00-governance/a.md",
                "06-memory-context/b.md",
                "13-engineering-decisions/c.md",
                "13-engineering-decisions/d.md",
            },
        )


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
