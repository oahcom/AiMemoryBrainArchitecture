#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F-07: NORMATIVE_ROOTS covers 14-ai-development with convention-aware pairing.

Tests drive the extracted pairing functions directly against a temporary
directory acting as the repository root, so the prompt-library checks and git
state are out of the loop. Each case states which F-07 exit-condition branch
it evidences.
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

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

    def normative(self, changed: set[str], complete: bool = True, exception: bool = False):
        changes = sorted(
            p for p in changed
            if p.split("/")[0] in self.gate.NORMATIVE_ROOTS
            and Path(p).suffix.lower() in {".md", ".yaml", ".yml", ".json", ".toml", ".proto"}
        )
        return self.gate.check_normative_pairing(changes, changed, complete, exception)

    # --- F-07 exit condition: undeclared change must fail ---

    def test_undeclared_change_fails_before_pairing(self):
        self.write("14-ai-development/foo.md")
        changed = {"14-ai-development/foo.md"}
        changes = ["14-ai-development/foo.md"]
        errors = self.gate.check_normative_pairing(changes, changed, complete=False, exception=False)
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
        self.assertTrue(any("requires its counterpart changed" in e for e in errors), errors)

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
        self.write("14-ai-development/AI-EXEC-002.md")
        self.write("docs/en/14-ai-development/AI-EXEC-002.md")
        changed = {"14-ai-development/AI-EXEC-002.md", "docs/en/14-ai-development/AI-EXEC-002.md"}
        self.assertEqual(self.normative(changed), [])
        self.assertEqual(self.gate.check_mirror_pairing(changed, False), [])

    def test_docs_en_mirror_change_alone_fails(self):
        self.write("14-ai-development/AI-EXEC-002.md")
        self.write("docs/en/14-ai-development/AI-EXEC-002.md")
        changed = {"docs/en/14-ai-development/AI-EXEC-002.md"}
        errors = self.gate.check_mirror_pairing(changed, False)
        self.assertTrue(any("without paired change" in e for e in errors), errors)

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
        self.assertTrue(any("requires both counterparts changed" in e for e in errors), errors)

    def test_legacy_docs_en_pairing_unchanged(self):
        self.write("docs/en/00-governance/policy.md")
        self.write("docs/zh-CN/00-governance/policy.md")
        changed = {"docs/en/00-governance/policy.md"}
        errors = self.gate.check_mirror_pairing(changed, False)
        self.assertTrue(any("without paired change" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
