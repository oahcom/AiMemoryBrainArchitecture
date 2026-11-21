#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-07 and Issue #412 regression tests for bilingual pairing and root moves.

The shared counterpart helper intentionally emits one diagnostic for every
missing member of a required pair: "requires all counterparts changed in this PR".
The original per-test assertions below are aligned to that shared diagnostic;
this keeps the implementation centralized and still tells CI users that the
pair is incomplete (rather than that a file is absent or a root move is illegal).

Tests drive the extracted pairing functions directly against a temporary
directory acting as the repository root, so the prompt-library checks and git
state are out of the loop. Each case states which F-07 exit-condition branch
it evidences.
"""
from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

GATE = Path(__file__).resolve().parents[2] / "check_bilingual_docs.py"


def load_gate(root: Path):
    spec = importlib.util.spec_from_file_location("check_bilingual_docs", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = root
    return mod


class GateRootsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.gate = load_gate(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel: str, text: str = "x\n"):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def _run_real_git_gate_for_change(self, rel: str):
        """Run main's production normative-file selection against a real git diff."""
        import contextlib
        import io
        import subprocess

        run = lambda *args: subprocess.run(
            args, cwd=self.root, check=True, capture_output=True, text=True
        )
        run("git", "init", "-q")
        run("git", "config", "user.email", "tests@example.invalid")
        run("git", "config", "user.name", "Bilingual gate regression")
        run("git", "commit", "--allow-empty", "-qm", "baseline")
        base = run("git", "rev-parse", "HEAD").stdout.strip()
        self.write(rel, "single-sided change\n")
        run("git", "add", "--", rel)
        run("git", "commit", "-qm", "single-sided change")
        head = run("git", "rev-parse", "HEAD").stdout.strip()

        previous_cwd = os.getcwd()
        output = io.StringIO()
        try:
            os.chdir(self.root)
            with patch.dict(
                os.environ,
                {"BASE_SHA": base, "HEAD_SHA": head, "PR_BODY": "BILINGUAL-MANIFEST: COMPLETE"},
            ):
                self.assertIn(rel, self.gate.changed_paths())
                with contextlib.ExitStack() as stack:
                    stack.enter_context(patch.object(self.gate, "read_baseline", return_value=set()))
                    stack.enter_context(patch.object(self.gate, "current_bilingual_gaps", return_value=set()))
                    stack.enter_context(patch.object(self.gate, "check_prompt_library", return_value=[]))
                    stack.enter_context(patch.object(self.gate, "check_embedded_registration_history", return_value=[]))
                    stack.enter_context(patch.object(self.gate, "parse_catch_up_declarations", return_value=({}, [])))
                    stack.enter_context(patch.object(self.gate, "check_policy_inheritance", return_value=[]))
                    stack.enter_context(patch.object(self.gate, "approved_exception", return_value=False))
                    stack.enter_context(patch.object(self.gate, "check_mirror_pairing", return_value=[]))
                    stack.enter_context(patch.object(self.gate, "check_normative_root_departures", return_value=[]))
                    stack.enter_context(contextlib.redirect_stdout(output))
                    stack.enter_context(contextlib.redirect_stderr(output))
                    exit_code = self.gate.main()
            return exit_code, output.getvalue()
        finally:
            os.chdir(previous_cwd)

    def normative(self, changed: set[str], complete: bool = True, exception: bool = False):
        changes = sorted(
            p for p in changed
            if p.split("/")[0] in self.gate.NORMATIVE_ROOTS
            and Path(p).suffix.lower() in {".md", ".yaml", ".yml", ".json", ".toml", ".proto"}
        )
        statuses = {path: "M" for path in changed}
        return self.gate.check_normative_pairing(changes, changed, statuses, complete, exception)

    # --- F-07 exit condition: undeclared change must fail ---

    def test_undeclared_change_fails_before_pairing(self):
        self.write("14-ai-development/foo.md")
        changed = {"14-ai-development/foo.md"}
        changes = ["14-ai-development/foo.md"]
        errors = self.gate.check_normative_pairing(changes, changed, {p: "M" for p in changed}, complete=False, exception=False)
        # With no declaration the pairing function is not the failing point;
        # the declaration check in main() is. Here we assert the pairing
        # function stays silent so the declaration error is the single gate.
        self.assertEqual(errors, [])
        self.assertIn("14-ai-development", self.gate.NORMATIVE_ROOTS)

    def test_declared_but_unpaired_source_fails(self):
        # Exit-condition evidence: changing a 14-ai-development root .md that
        # has no counterpart must fail even with BILINGUAL-MANIFEST: COMPLETE.
        self.write("14-ai-development/debt-only.md")
        changed = {"14-ai-development/debt-only.md"}
        errors = self.normative(changed)
        self.assertTrue(any("no resolvable bilingual counterpart" in e for e in errors), errors)

    def test_unpaired_source_requires_partner_changed(self):
        self.write("14-ai-development/zh-primary.md")
        self.write("14-ai-development/zh-primary.en.md")
        errors = self.normative({"14-ai-development/zh-primary.md"})
        self.assertTrue(any("requires all counterparts changed in this PR" in e for e in errors), errors)

    # --- convention: side-by-side .en.md ---

    def test_side_by_side_en_pair_passes(self):
        self.write("14-ai-development/zh-primary.md")
        self.write("14-ai-development/zh-primary.en.md")
        changed = {"14-ai-development/zh-primary.md", "14-ai-development/zh-primary.en.md"}
        self.assertEqual(self.normative(changed), [])

    def test_side_by_side_zh_cn_pair_passes(self):
        self.write("14-ai-development/en-primary.en.md")
        self.write("14-ai-development/en-primary.zh-CN.md")
        changed = {"14-ai-development/en-primary.en.md", "14-ai-development/en-primary.zh-CN.md"}
        self.assertEqual(self.normative(changed), [])

    # --- convention: docs/en mirror ---

    def test_docs_en_mirror_pair_passes(self):
        # Shape 3 is valid only when the root source is genuinely Chinese.
        chinese = "这是中文原文。" * 20
        self.write("14-ai-development/AI-EXEC-002.md", chinese)
        self.write("docs/en/14-ai-development/AI-EXEC-002.md", "English translation.\n")
        changed = {"14-ai-development/AI-EXEC-002.md", "docs/en/14-ai-development/AI-EXEC-002.md"}
        self.assertEqual(self.normative(changed), [])
        self.assertTrue(self.gate._carries_chinese("14-ai-development/AI-EXEC-002.md"))
        self.assertEqual(self.gate.check_mirror_pairing(changed, {p: "M" for p in changed}, False), [])

        # A pair of English-only files must not satisfy the root-Chinese shape.
        self.write("14-ai-development/english-only-probe.md", "English only.\n")
        self.write("docs/en/14-ai-development/english-only-probe.md", "English only.\n")
        self.gate.REPO_ROOT = self.root
        self.assertIn("14-ai-development/english-only-probe.md", self.gate.current_bilingual_gaps())

        # The two other legal shapes remain accepted by the structural inventory.
        self.write("14-ai-development/side-by-side.en.md", "English only.\n")
        self.write("14-ai-development/side-by-side.zh-CN.md", chinese)
        self.write("14-ai-development/triple.md", chinese)
        self.write("docs/en/14-ai-development/triple.md", "English translation.\n")
        self.write("docs/zh-CN/14-ai-development/triple.md", chinese)
        self.write("14-ai-development/no-pair.md", "English only.\n")
        gaps = self.gate.current_bilingual_gaps()
        self.assertNotIn("14-ai-development/side-by-side.en.md", gaps)
        self.assertNotIn("14-ai-development/side-by-side.zh-CN.md", gaps)
        self.assertNotIn("14-ai-development/triple.md", gaps)
        self.assertIn("14-ai-development/no-pair.md", gaps)

    def test_docs_en_mirror_change_alone_fails(self):
        self.write("14-ai-development/AI-EXEC-002.md")
        self.write("docs/en/14-ai-development/AI-EXEC-002.md")
        changed = {"docs/en/14-ai-development/AI-EXEC-002.md"}
        errors = self.gate.check_mirror_pairing(changed, {p: "M" for p in changed}, False)
        self.assertTrue(any("requires all counterparts changed in this PR" in e for e in errors), errors)

    # --- explicit embedded registration (F-07 exit-condition option 2) ---

    def test_embedded_registration_skips_pairing(self):
        # The gate's own registered embedded set must contain the real files.
        self.assertIn("14-ai-development/AI-EXEC-UNIFICATION-RULING-001.md", self.gate.EMBEDDED_BILINGUAL_SOURCES)
        self.write("14-ai-development/AI-EXEC-UNIFICATION-RULING-001.md")
        changed = {"14-ai-development/AI-EXEC-UNIFICATION-RULING-001.md"}
        self.assertEqual(self.normative(changed), [])

    def test_every_registered_embedded_file_is_under_normative_root(self):
        for src in self.gate.EMBEDDED_BILINGUAL_SOURCES:
            self.assertEqual(src.split("/")[0] in self.gate.NORMATIVE_ROOTS, True, src)

    # --- Issue #420: exemption registration must follow file creation ---

    def make_registration_repo(self, register_in_creation_commit: bool):
        repo = self.root / ("registration-same-commit" if register_in_creation_commit else "registration-later-commit")
        repo.mkdir()
        self.git(repo, "init", "-q")
        self.git(repo, "config", "user.email", "tests@example.invalid")
        self.git(repo, "config", "user.name", "Issue 420 tests")
        source = "00-governance/new-embedded-source.md"
        target = repo / source
        target.parent.mkdir(parents=True)
        target.write_text("embedded bilingual source\n", encoding="utf-8")
        gate_file = repo / "scripts/check_bilingual_docs.py"
        gate_file.parent.mkdir(parents=True)
        if register_in_creation_commit:
            gate_file.write_text(
                f'EMBEDDED_BILINGUAL_SOURCES = {{\n    "{source}": "independent reason",\n}}\n',
                encoding="utf-8",
            )
        self.commit_tree(repo, "add source" if register_in_creation_commit else "add source before registration")
        if not register_in_creation_commit:
            gate_file.write_text(
                f'EMBEDDED_BILINGUAL_SOURCES = {{\n    "{source}": "independent reason",\n}}\n',
                encoding="utf-8",
            )
            self.commit_tree(repo, "register existing source")
        self.gate.ROOT = repo
        self.gate.EMBEDDED_BILINGUAL_SOURCES = {source: "independent reason"}
        self.gate.SELF_REGISTERED_AT_CREATION = {}
        return repo, source

    def test_issue_420_same_commit_file_add_and_exemption_registration_rejected(self):
        self.make_registration_repo(register_in_creation_commit=True)
        errors = self.gate.check_embedded_registration_history()
        self.assertTrue(any("same commit that added the file" in error for error in errors), errors)

    def test_issue_420_registration_in_later_commit_is_accepted(self):
        self.make_registration_repo(register_in_creation_commit=False)
        self.assertEqual(self.gate.check_embedded_registration_history(), [])

    # --- operational-record subtrees: declaration only, no pairing ---

    def test_work_items_change_is_pairing_exempt(self):
        self.write("14-ai-development/work-items/INDEX.md")
        changed = {"14-ai-development/work-items/INDEX.md"}
        self.assertEqual(self.normative(changed), [])

    def test_prompts_subtree_is_pairing_exempt(self):
        self.write("14-ai-development/prompts/owners/A/owner-session-v1.md")
        changed = {"14-ai-development/prompts/owners/A/owner-session-v1.md"}
        self.assertEqual(self.normative(changed), [])

    def test_root_yaml_is_declaration_only(self):
        self.write("14-ai-development/remote-worker-inventory.yaml")
        changed = {"14-ai-development/remote-worker-inventory.yaml"}
        self.assertEqual(self.normative(changed), [])

    # --- regression: 00-governance behaviour unchanged ---

    def test_00_governance_pairing_unchanged(self):
        self.write("00-governance/policy.md")
        changed = {"00-governance/policy.md"}
        errors = self.normative(changed)
        self.assertTrue(any("requires all counterparts changed in this PR" in e for e in errors), errors)

    def test_legacy_docs_en_pairing_unchanged(self):
        self.write("docs/en/00-governance/policy.md")
        self.write("docs/zh-CN/00-governance/policy.md")
        changed = {"docs/en/00-governance/policy.md"}
        errors = self.gate.check_mirror_pairing(changed, {p: "M" for p in changed}, False)
        self.assertTrue(any("requires all counterparts changed in this PR" in e for e in errors), errors)

    # --- regression: a moved-away side must not demand a partner at the old path ---

    def test_moved_away_side_does_not_require_old_counterpart(self):
        """A real paired move is D+D at old paths and A+A at new paths.

        Build two committed trees and ask changed_status() for Git's actual
        --no-renames output. The gate must accept the complete paired move
        without demanding that either old path still exists at HEAD.
        """
        import os
        import subprocess

        repo = Path(self._tmp.name) / "paired-move-repo"
        repo.mkdir()
        run = lambda *a: subprocess.run(
            a, cwd=repo, check=True, capture_output=True, text=True
        )
        run("git", "init", "-q")
        run("git", "config", "user.email", "t@example.invalid")
        run("git", "config", "user.name", "t")
        old_en = "docs/en/00-governance/policy.md"
        old_zh = "docs/zh-CN/00-governance/policy.md"
        new_en = "docs/en/00-governance/sub/policy.md"
        new_zh = "docs/zh-CN/00-governance/sub/policy.md"
        for rel in (old_en, old_zh):
            target = repo / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("paired policy\\n", encoding="utf-8")
        run("git", "add", "-A")
        self.assertTrue(run("git", "status", "--porcelain").stdout.strip())
        run("git", "commit", "-qm", "base pair")
        base = run("git", "rev-parse", "HEAD").stdout.strip()

        for src, dst in ((old_en, new_en), (old_zh, new_zh)):
            (repo / dst).parent.mkdir(parents=True, exist_ok=True)
            run("git", "mv", src, dst)
        self.assertTrue(run("git", "status", "--porcelain").stdout.strip())
        run("git", "commit", "-qm", "move pair")
        head = run("git", "rev-parse", "HEAD").stdout.strip()

        prev = os.getcwd()
        old_base, old_head = os.environ.get("BASE_SHA"), os.environ.get("HEAD_SHA")
        try:
            os.chdir(repo)
            os.environ["BASE_SHA"], os.environ["HEAD_SHA"] = base, head
            self.gate.ROOT = repo
            statuses = self.gate.changed_status()
            self.assertEqual(statuses.get(old_en), "D", statuses)
            self.assertEqual(statuses.get(old_zh), "D", statuses)
            self.assertEqual(statuses.get(new_en), "A", statuses)
            self.assertEqual(statuses.get(new_zh), "A", statuses)
            self.assertEqual(
                self.gate.check_mirror_pairing(set(statuses), statuses, False), []
            )
        finally:
            os.chdir(prev)
            if old_base is None:
                os.environ.pop("BASE_SHA", None)
            else:
                os.environ["BASE_SHA"] = old_base
            if old_head is None:
                os.environ.pop("HEAD_SHA", None)
            else:
                os.environ["HEAD_SHA"] = old_head

    def test_moved_away_side_still_requires_paired_change(self):
        """A one-sided move remains an error: the pair was split."""
        self.write("docs/en/00-governance/sub/policy.md")
        self.write("docs/zh-CN/00-governance/policy.md")
        changed = {
            "docs/en/00-governance/policy.md",
            "docs/en/00-governance/sub/policy.md",
        }
        errors = self.gate.check_mirror_pairing(changed, {p: "M" for p in changed}, False)
        self.assertTrue(any("requires all counterparts changed in this PR" in e for e in errors), errors)

    # --- root cause: a move must expose its deleted side to changed_paths() ---

    def test_changed_paths_reports_both_sides_of_a_move(self):
        """Rename detection would hide the deleted side; --no-renames must not.

        This is the root cause of the split-pair blind spot: with rename
        detection a `git mv docs/zh-CN/x.md docs/governance/x.md` yields only
        the destination, so the pairing check never sees the removal.
        """
        import os
        import subprocess

        repo = Path(self._tmp.name) / "repo"
        repo.mkdir()
        run = lambda *a: subprocess.run(a, cwd=repo, check=True,
                                        capture_output=True, text=True)
        run("git", "init", "-q")
        run("git", "config", "user.email", "t@example.invalid")
        run("git", "config", "user.name", "t")
        src = Path("docs/zh-CN/00-governance/policy.md")
        (repo / src).parent.mkdir(parents=True)
        (repo / src).write_text("x\n", encoding="utf-8")
        run("git", "add", "-A")
        self.assertTrue(run("git", "status", "--porcelain").stdout.strip())
        run("git", "commit", "-qm", "a")
        base = run("git", "rev-parse", "HEAD").stdout.strip()
        (repo / "docs/governance").mkdir(parents=True)
        run("git", "mv", str(src), "docs/governance/policy.md")
        self.assertTrue(run("git", "status", "--porcelain").stdout.strip())
        run("git", "commit", "-qm", "move")
        head = run("git", "rev-parse", "HEAD").stdout.strip()

        os.environ["BASE_SHA"], os.environ["HEAD_SHA"] = base, head
        prev = os.getcwd()
        try:
            os.chdir(repo)
            mod = load_gate(repo)
            mod.ROOT = repo
            seen = mod.changed_paths()
        finally:
            os.chdir(prev)
            os.environ.pop("BASE_SHA", None)
            os.environ.pop("HEAD_SHA", None)

        self.assertIn("docs/zh-CN/00-governance/policy.md", seen,
                      "--no-renames must report the moved-away side")
        self.assertIn("docs/governance/policy.md", seen)


    # --- Issue #412: normative-root departures and mirror-only moves ---

    def git(self, repo: Path, *args: str) -> str:
        import subprocess
        result = subprocess.run(
            ["git", *args], cwd=repo, check=True,
            capture_output=True, text=True,
        )
        return result.stdout.strip()

    def commit_tree(self, repo: Path, message: str) -> str:
        # A failed git mv/unlink must never silently re-test the previous tree.
        status = self.git(repo, "status", "--porcelain")
        self.assertTrue(status, "refusing to commit an unchanged fixture tree")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-qm", message)
        return self.git(repo, "rev-parse", "HEAD")

    def make_git_history(self) -> tuple[Path, str]:
        repo = self.root / "issue-412-repo"
        repo.mkdir()
        self.git(repo, "init", "-q")
        self.git(repo, "config", "user.email", "tests@example.invalid")
        self.git(repo, "config", "user.name", "Issue 412 tests")
        for rel, body in (
            ("00-governance/policy.md", "normative policy body\\n"),
            ("docs/en/00-governance/policy.md", "English mirror body\\n"),
            ("docs/zh-CN/00-governance/policy.md", "Chinese mirror body\\n"),
        ):
            target = repo / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        base = self.commit_tree(repo, "base")
        self.gate.ROOT = repo
        return repo, base

    def root_departures(self, repo: Path, base: str) -> list[str]:
        import os
        os.environ["BASE_SHA"] = base
        os.environ["HEAD_SHA"] = self.git(repo, "rev-parse", "HEAD")
        return self.gate.check_normative_root_departures(exception=False)

    def git_move(self, repo: Path, src: str, dst: str) -> None:
        import os
        (repo / dst).parent.mkdir(parents=True, exist_ok=True)
        self.git(repo, "mv", src, dst)

    def test_issue_412_p2_normative_triple_move_within_same_root_is_allowed(self):
        repo, base = self.make_git_history()
        for src, dst in (
            ("00-governance/policy.md", "00-governance/renamed-policy.md"),
            ("docs/en/00-governance/policy.md", "docs/en/00-governance/renamed-policy.md"),
            ("docs/zh-CN/00-governance/policy.md", "docs/zh-CN/00-governance/renamed-policy.md"),
        ):
            self.git_move(repo, src, dst)
        self.commit_tree(repo, "move triple within docs")
        self.assertEqual(self.root_departures(repo, base), [])

    def test_issue_412_p3_mirror_only_pair_move_out_to_archive_is_allowed(self):
        repo, _ = self.make_git_history()
        (repo / "00-governance/policy.md").unlink()
        base = self.commit_tree(repo, "fixture becomes mirror-only")
        old_en = "docs/en/00-governance/policy.md"
        old_zh = "docs/zh-CN/00-governance/policy.md"
        self.git_move(repo, old_en, "docs/en/governance/archive/policy.md")
        self.git_move(repo, old_zh, "docs/zh-CN/governance/archive/policy.md")
        self.commit_tree(repo, "move mirror-only pair to archive")
        self.assertEqual(self.root_departures(repo, base), [])
        raw = self.git(repo, "diff", "--name-status", "--no-renames", f"{base}...HEAD")
        statuses = {line.split("\t", 1)[1]: line.split("\t", 1)[0]
                    for line in raw.splitlines()}
        changed = set(statuses)
        self.assertEqual(
            self.gate.check_counterpart_requirement(old_en, [old_zh], changed, statuses, False),
            [],
        )

    def test_issue_412_p5_mirror_only_pair_deleted_together_is_allowed(self):
        repo, _ = self.make_git_history()
        (repo / "00-governance/policy.md").unlink()
        base = self.commit_tree(repo, "fixture becomes mirror-only")
        old_en = repo / "docs/en/00-governance/policy.md"
        old_zh = repo / "docs/zh-CN/00-governance/policy.md"
        old_en.unlink()
        old_zh.unlink()
        self.commit_tree(repo, "delete mirror-only pair")
        self.assertEqual(self.root_departures(repo, base), [])
        raw = self.git(repo, "diff", "--name-status", "--no-renames", f"{base}...HEAD")
        statuses = {line.split("\t", 1)[1]: line.split("\t", 1)[0]
                    for line in raw.splitlines()}
        self.assertEqual(
            self.gate.check_counterpart_requirement(
                "docs/en/00-governance/policy.md",
                ["docs/zh-CN/00-governance/policy.md"],
                set(statuses), statuses, False,
            ),
            [],
        )

    def test_issue_412_d7_normative_triple_move_outside_covered_set_is_rejected(self):
        repo, base = self.make_git_history()
        for src, dst in (
            ("00-governance/policy.md", "docs/governance/archive/policy.md"),
            ("docs/en/00-governance/policy.md", "docs/en/governance/archive/policy.md"),
            ("docs/zh-CN/00-governance/policy.md", "docs/zh-CN/governance/archive/policy.md"),
        ):
            self.git_move(repo, src, dst)
        self.commit_tree(repo, "move triple outside normative roots")
        errors = self.root_departures(repo, base)
        self.assertTrue(any("moved outside NORMATIVE_ROOTS" in e for e in errors), errors)

    def test_issue_412_d8_normative_triple_deletion_is_rejected(self):
        repo, base = self.make_git_history()
        for rel in (
            "00-governance/policy.md",
            "docs/en/00-governance/policy.md",
            "docs/zh-CN/00-governance/policy.md",
        ):
            (repo / rel).unlink()
        self.commit_tree(repo, "delete normative triple")
        errors = self.root_departures(repo, base)
        self.assertTrue(any("by deletion" in e for e in errors), errors)

    def test_issue_412_d9_normative_triple_move_to_another_normative_root_is_allowed(self):
        repo, base = self.make_git_history()
        for src, dst in (
            ("00-governance/policy.md", "13-engineering-decisions/policy.md"),
            ("docs/en/00-governance/policy.md", "docs/en/13-engineering-decisions/policy.md"),
            ("docs/zh-CN/00-governance/policy.md", "docs/zh-CN/13-engineering-decisions/policy.md"),
        ):
            self.git_move(repo, src, dst)
        self.commit_tree(repo, "move triple across normative roots")
        self.assertEqual(self.root_departures(repo, base), [])


    # --- Issue #461: X.md <-> X.zh-CN.md pairs in every normative root ---

    def inventory_02(self):
        self.gate.ROOT = self.root
        self.gate.REPO_ROOT = self.root
        self.gate.NORMATIVE_ROOTS = {"02-domain-model"}
        (self.root / "02-domain-model").mkdir(parents=True, exist_ok=True)
        return self.gate.current_bilingual_gaps()

    def test_issue_461_n1_md_without_zh_cn_is_rejected(self):
        self.write("02-domain-model/zz-probe-alone.md", "English only.\\n")
        self.assertIn("02-domain-model/zz-probe-alone.md", self.inventory_02())

    def test_issue_461_n2_zh_cn_without_md_is_rejected(self):
        self.write("02-domain-model/zz-probe-alone.zh-CN.md", "中文内容。\\n")
        self.assertIn("02-domain-model/zz-probe-alone.zh-CN.md", self.inventory_02())

    def test_issue_461_n3_md_and_zh_cn_pair_is_accepted(self):
        self.write("02-domain-model/zz-probe-pair.md", "English source.\\n")
        self.write("02-domain-model/zz-probe-pair.zh-CN.md", "中文翻译。\n")
        gaps = self.inventory_02()
        self.assertNotIn("02-domain-model/zz-probe-pair.md", gaps)
        self.assertNotIn("02-domain-model/zz-probe-pair.zh-CN.md", gaps)

    def test_issue_461_n4_en_and_zh_cn_pair_is_accepted(self):
        self.write("02-domain-model/zz-probe-en.en.md", "English source.\\n")
        self.write("02-domain-model/zz-probe-en.zh-CN.md", "中文翻译。\n")
        gaps = self.inventory_02()
        self.assertNotIn("02-domain-model/zz-probe-en.en.md", gaps)
        self.assertNotIn("02-domain-model/zz-probe-en.zh-CN.md", gaps)

    def test_issue_461_n5_deleting_zh_cn_side_rejects_pair(self):
        english = "02-domain-model/phase-2-domain-extension.md"
        chinese = "02-domain-model/phase-2-domain-extension.zh-CN.md"
        self.write(english, "English source.\\n")
        self.write(chinese, "中文翻译。\n")
        self.assertNotIn(english, self.inventory_02())
        (self.root / chinese).unlink()
        self.assertIn(english, self.inventory_02())

    def test_issue_469_short_translation_is_accepted(self):
        self.write("02-domain-model/zz-probe-short.md", "English source.\n")
        self.write("02-domain-model/zz-probe-short.zh-CN.md", "中文翻译。\n")
        gaps = self.inventory_02()
        self.assertNotIn("02-domain-model/zz-probe-short.md", gaps)
        self.assertNotIn("02-domain-model/zz-probe-short.zh-CN.md", gaps)

    def test_issue_461_n6_pair_without_chinese_is_rejected(self):
        self.write("02-domain-model/zz-probe-fake.md", "English source.\n")
        self.write("02-domain-model/zz-probe-fake.zh-CN.md", "English too.\n")
        gaps = self.inventory_02()
        self.assertIn("02-domain-model/zz-probe-fake.md", gaps)
        self.assertIn("02-domain-model/zz-probe-fake.zh-CN.md", gaps)


    # --- regression: exact partial side-by-side pairs fail closed ---

    def test_partial_side_by_side_pair_rejects_both_sides(self):
        english = "02-domain-model/zz-partial-probe.md"
        chinese = "02-domain-model/zz-partial-probe.zh-CN.md"
        self.write(english, "Complete English specification.\n")
        self.write(chinese, "这是局部中文翻译内容。" * 20 + "\n")

        # Reproduce the former false-positive condition: Chinese content
        # exceeds the existing CJK character threshold but covers only part.
        self.assertTrue(self.gate._carries_chinese(chinese))
        self.gate.PARTIAL_SIDE_BY_SIDE_PAIRS.add(
            frozenset((english, chinese))
        )

        gaps = self.inventory_02()
        self.assertIn(english, gaps)
        self.assertIn(chinese, gaps)

    def test_partial_side_by_side_registration_does_not_block_mirrors(self):
        english = "02-domain-model/zz-partial-mirror-probe.md"
        chinese = "02-domain-model/zz-partial-mirror-probe.zh-CN.md"
        self.write(english, "Complete English specification.\n")
        self.write(chinese, "这是局部中文翻译内容。" * 20 + "\n")
        self.gate.PARTIAL_SIDE_BY_SIDE_PAIRS.add(
            frozenset((english, chinese))
        )

        # A complete docs/en + docs/zh-CN mirror shape remains independently
        # acceptable, even while the side-by-side relationship is rejected.
        for source in (english, chinese):
            self.write(f"docs/en/{source}", "English mirror.\n")
            self.write(f"docs/zh-CN/{source}", "中文镜像内容。\n")

        gaps = self.inventory_02()
        self.assertNotIn(english, gaps)
        self.assertNotIn(chinese, gaps)

    def test_partial_side_by_side_production_registry_is_empty(self):
        self.assertEqual(self.gate.PARTIAL_SIDE_BY_SIDE_PAIRS, set())

    # --- regression: one-sided translation catch-up is explicit and verifiable ---

    def test_catch_up_declaration_parses(self):
        body = (
            "BILINGUAL-MANIFEST: COMPLETE\n"
            "BILINGUAL-CATCH-UP: "
            "source=02-domain-model/probe.zh-CN.md "
            "counterpart=02-domain-model/probe.md\n"
        )
        declarations, errors = self.gate.parse_catch_up_declarations(body)
        self.assertEqual(errors, [])
        self.assertEqual(
            declarations,
            {"02-domain-model/probe.zh-CN.md": "02-domain-model/probe.md"},
        )

    def test_catch_up_declaration_rejects_duplicate_source(self):
        line = (
            "BILINGUAL-CATCH-UP: "
            "source=02-domain-model/probe.zh-CN.md "
            "counterpart=02-domain-model/probe.md"
        )
        _, errors = self.gate.parse_catch_up_declarations(line + "\n" + line + "\n")
        self.assertEqual(len(errors), 1)
        self.assertIn("Duplicate", errors[0])

    def test_catch_up_declaration_rejects_malformed_declaration(self):
        # Missing counterpart, missing source, a stray base-blob field, and an
        # empty path are all malformed: the declaration carries intent only.
        for bad in (
            "BILINGUAL-CATCH-UP: source=02-domain-model/probe.zh-CN.md\n",
            "BILINGUAL-CATCH-UP: counterpart=02-domain-model/probe.md\n",
            "BILINGUAL-CATCH-UP: source=02-domain-model/probe.zh-CN.md "
            "counterpart=02-domain-model/probe.md base-blob=" + "a" * 40 + "\n",
            "BILINGUAL-CATCH-UP: source= counterpart=02-domain-model/probe.md\n",
        ):
            _, errors = self.gate.parse_catch_up_declarations(bad)
            self.assertEqual(len(errors), 1, bad)
            self.assertIn("Malformed", errors[0])

    def test_catch_up_passes_with_verified_unchanged_partner(self):
        source = "02-domain-model/zz-catchup-probe.zh-CN.md"
        counterpart = "02-domain-model/zz-catchup-probe.md"
        blob = "a" * 40
        self.write(source, "\u4e2d\u6587\u7ffb\u8bd1\n")
        self.write(counterpart, "English source\n")

        with patch.dict(os.environ, {"BASE_SHA": "base", "HEAD_SHA": "head"}):
            with patch.object(
                self.gate.subprocess,
                "check_output",
                side_effect=[blob + "\n", blob + "\n"],
            ):
                errors = self.gate.check_counterpart_requirement(
                    source,
                    [counterpart],
                    {source},
                    {source: "M"},
                    False,
                    catch_up_declaration=counterpart,
                )

        self.assertEqual(errors, [])

    def test_catch_up_without_declaration_still_fails(self):
        source = "02-domain-model/zz-catchup-probe.zh-CN.md"
        counterpart = "02-domain-model/zz-catchup-probe.md"
        self.write(source, "\u4e2d\u6587\n")
        self.write(counterpart, "English\n")

        errors = self.gate.check_counterpart_requirement(
            source, [counterpart], {source}, {source: "M"}, False
        )
        self.assertTrue(
            any("requires all counterparts changed in this PR" in e for e in errors),
            errors,
        )

    def test_catch_up_rejects_changed_partner_blob(self):
        source = "02-domain-model/zz-catchup-probe.zh-CN.md"
        counterpart = "02-domain-model/zz-catchup-probe.md"
        self.write(source, "\u4e2d\u6587\n")
        self.write(counterpart, "English\n")

        with patch.dict(os.environ, {"BASE_SHA": "base", "HEAD_SHA": "head"}):
            with patch.object(
                self.gate.subprocess,
                "check_output",
                side_effect=["a" * 40 + "\n", "b" * 40 + "\n"],
            ):
                errors = self.gate.check_counterpart_requirement(
                    source,
                    [counterpart],
                    {source},
                    {source: "M"},
                    False,
                    catch_up_declaration=counterpart,
                )

        self.assertEqual(len(errors), 1)
        self.assertIn("invalid BILINGUAL-CATCH-UP declaration", errors[0])
        self.assertIn("blob changed between PR base and HEAD", errors[0])

    def test_catch_up_rejects_missing_counterpart_at_base(self):
        source = "02-domain-model/zz-catchup-probe.zh-CN.md"
        counterpart = "02-domain-model/zz-catchup-probe.md"
        self.write(source, "\u4e2d\u6587\n")
        self.write(counterpart, "English\n")

        with patch.dict(os.environ, {"BASE_SHA": "base", "HEAD_SHA": "head"}):
            with patch.object(
                self.gate.subprocess,
                "check_output",
                side_effect=self.gate.subprocess.CalledProcessError(1, "git"),
            ):
                errors = self.gate.check_counterpart_requirement(
                    source,
                    [counterpart],
                    {source},
                    {source: "M"},
                    False,
                    catch_up_declaration=counterpart,
                )

        self.assertEqual(len(errors), 1)
        self.assertIn("does not exist at PR base", errors[0])

    def test_catch_up_rejects_missing_counterpart_at_head(self):
        source = "02-domain-model/zz-catchup-probe.zh-CN.md"
        counterpart = "02-domain-model/zz-catchup-probe.md"
        self.write(source, "\u4e2d\u6587\n")
        self.write(counterpart, "English\n")

        with patch.dict(os.environ, {"BASE_SHA": "base", "HEAD_SHA": "head"}):
            with patch.object(
                self.gate.subprocess,
                "check_output",
                side_effect=[
                    "a" * 40 + "\n",
                    self.gate.subprocess.CalledProcessError(1, "git"),
                ],
            ):
                errors = self.gate.check_counterpart_requirement(
                    source,
                    [counterpart],
                    {source},
                    {source: "M"},
                    False,
                    catch_up_declaration=counterpart,
                )

        self.assertEqual(len(errors), 1)
        self.assertIn("does not exist at PR HEAD", errors[0])

    def test_catch_up_rejects_mismatched_counterpart(self):
        source = "02-domain-model/zz-catchup-probe.zh-CN.md"
        counterpart = "02-domain-model/zz-catchup-probe.md"
        self.write(source, "\u4e2d\u6587\n")
        self.write(counterpart, "English\n")

        errors = self.gate.check_counterpart_requirement(
            source,
            [counterpart],
            {source},
            {source: "M"},
            False,
            catch_up_declaration="02-domain-model/other.md",
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("does not match side-by-side partner", errors[0])

    def test_catch_up_rejects_partner_that_changed_in_pr(self):
        source = "02-domain-model/zz-catchup-probe.zh-CN.md"
        counterpart = "02-domain-model/zz-catchup-probe.md"
        self.write(source, "\u4e2d\u6587\n")
        self.write(counterpart, "English\n")

        errors = self.gate.check_counterpart_requirement(
            source,
            [counterpart],
            {source, counterpart},
            {source: "M", counterpart: "M"},
            False,
            catch_up_declaration=counterpart,
        )
        self.assertEqual(errors, [])

    def test_catch_up_rejects_non_side_by_side_source(self):
        source = "02-domain-model/zz-catchup-probe.md"
        counterpart = "02-domain-model/zz-catchup-probe.zh-CN.md"
        self.write(source, "English\n")
        self.write(counterpart, "\u4e2d\u6587\n")

        # The English side is the source: a one-sided catch-up is only allowed
        # for a translation file (.zh-CN.md / .en.md).
        reason = self.gate.check_side_by_side_catch_up(
            source, counterpart, {source}, {source: "M"}
        )
        self.assertEqual(reason, "source is not a translation file (.zh-CN.md or .en.md)")

    def test_catch_up_declaration_does_not_relax_mirror_pairing(self):
        # A catch-up declaration is a side-by-side concept. A docs/en mirror
        # change must still require both sides, declaration or not.
        source = "02-domain-model/zz-mirror-probe.md"
        mirror = f"docs/en/{source}"
        self.write(source, "English source.\n")
        self.write(mirror, "English mirror.\n")

        errors = self.gate.check_mirror_pairing({mirror}, {mirror: "M"}, False)
        self.assertTrue(errors, "mirror pairing must still require both sides")
        self.assertIn("requires all counterparts changed", errors[0])

    # --- Issue #522: data formats are not bilingual document roots ---

    def test_schema_json_change_does_not_require_counterpart(self):
        exit_code, output = self._run_real_git_gate_for_change(
            "08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json"
        )
        self.assertEqual(exit_code, 0, output)
        self.assertIn("Bilingual documentation and prompt-library gate: PASS", output)

    def test_markdown_still_requires_counterpart(self):
        exit_code, output = self._run_real_git_gate_for_change(
            "08-bmcp-protocol/gate-single-sided-probe.md"
        )
        self.assertEqual(exit_code, 1, output)
        self.assertIn("requires all counterparts changed in this PR", output)

    def test_governance_markdown_still_requires_counterpart(self):
        exit_code, output = self._run_real_git_gate_for_change(
            "00-governance/gate-single-sided-probe.md"
        )
        self.assertEqual(exit_code, 1, output)
        self.assertIn("requires all counterparts changed in this PR", output)


if __name__ == "__main__":
    unittest.main()
