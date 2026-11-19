#!/usr/bin/env python3
"""Tests for the evidence tiering checker (FIX-2026-P1-T4).

The GO decision requires that each acceptance gate be proven by the actual
VERDICT/REASON records, not merely by a process exit code, so every case
asserts both.

Run: python test_evidence_tiering.py -v
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check-evidence-tiering.py"
SHA = "a" * 40
SHA2 = "b" * 40


def declaration(**overrides):
    """Build a complete Level 1 declaration; overrides replace/remove fields."""
    fields = {
        "work_item": "FIX-TEST-001",
        "change_class": "ARCHITECTURE",
        "review_level": "R3",
        "evidence_level": "1",
        "subject_head": SHA,
        "change_summary": "tighten evidence binding for the checker",
        "source_authenticity": "NOT_VERIFIED",
        "evidence.design_doc": "design.md",
        "evidence.impact_analysis": "impact.md",
        "evidence.test_log": "test.log",
        "evidence.review_record": "review.md",
        "evidence.rollback_plan": "rollback.md",
        "binding.protocol": "v3",
        "binding.subject_tree_contains_evidence": "true",
        "binding.sidecar_anchor": SHA2,
        "authenticity.acknowledged": "true",
    }
    for key, value in overrides.items():
        if value is None:
            fields.pop(key, None)
        else:
            fields[key] = value
    top, nested = [], {}
    for key, value in fields.items():
        if "." in key:
            block, sub = key.split(".", 1)
            nested.setdefault(block, []).append((sub, value))
        else:
            top.append((key, value))
    lines = ["%s: %s" % (k, '"%s"' % v if " " in v else v) for k, v in top]
    for block, items in nested.items():
        lines.append("%s:" % block)
        lines.extend("  %s: %s" % (k, v) for k, v in items)
    return "\n".join(lines) + "\n"


class EvidenceTieringTests(unittest.TestCase):
    def run_checker(self, text, name="declaration.yaml"):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / name
            path.write_text(text, encoding="utf-8", newline="\n")
            return subprocess.run(
                [sys.executable, CHECKER.as_posix(), path.as_posix()],
                capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)

    def assert_blocked(self, result, code):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("VERDICT\tBLOCKED", result.stdout)
        self.assertIn("REASON\t%s" % code, result.stdout)

    # ---- the eight GO acceptance gates -------------------------------------
    def test_gate1_missing_level_declaration(self):
        self.assert_blocked(self.run_checker(declaration(evidence_level=None)), "CE_NO_LEVEL")

    def test_gate2_level_conflicts_with_risk_class(self):
        result = self.run_checker(declaration(change_class="SECURITY", evidence_level="3"))
        self.assert_blocked(result, "CE_LEVEL_CLASS_CONFLICT")

    def test_gate3_level1_required_field_missing(self):
        self.assert_blocked(self.run_checker(declaration(**{"evidence.rollback_plan": None})),
                            "CE_L1_MISSING_FIELD")

    def test_gate4_unknown_class_assigned_level(self):
        self.assert_blocked(self.run_checker(declaration(change_class="UNKNOWN", evidence_level="2")),
                            "CE_UNKNOWN_CLASS")

    def test_gate5_v3_binding_fields_missing(self):
        result = self.run_checker(declaration(**{"binding.protocol": None}))
        self.assert_blocked(result, "CE_NO_BINDING_PROTOCOL")

    def test_gate6_sha_format_invalid(self):
        self.assert_blocked(self.run_checker(declaration(subject_head="abc123")), "CE_BAD_SHA")

    def test_gate7_not_verified_cannot_pass_silently(self):
        result = self.run_checker(declaration(**{"authenticity.acknowledged": None}))
        self.assert_blocked(result, "CE_AUTH_NOT_ACK")

    def test_gate8_unparseable_input_fails_closed(self):
        self.assert_blocked(self.run_checker("this is not yaml at all\n"), "CE_UNPARSABLE")

    # ---- additional fail-closed rules -------------------------------------
    def test_r3_cannot_be_downgraded(self):
        result = self.run_checker(declaration(review_level="R3", evidence_level="2",
                                              change_class="FEATURE"))
        self.assert_blocked(result, "CE_R3_DOWNGRADE")

    def test_r2_auto_downgrade_blocked_without_justification(self):
        self.assert_blocked(self.run_checker(declaration(review_level="R2", evidence_level="3",
                                                         change_class="DOC_EDITORIAL",
                                                         **{"evidence.review_note": "note"})),
                            "CE_R2_AUTO_DOWNGRADE")

    def test_unfounded_verified_claim_blocked(self):
        self.assert_blocked(self.run_checker(declaration(source_authenticity="VERIFIED")),
                            "CE_UNFOUNDED_VERIFIED")

    def test_missing_declaration_file_blocked(self):
        result = subprocess.run([sys.executable, CHECKER.as_posix(), "no-such-file.yaml"],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(result.returncode, 2)
        self.assertIn("VERDICT\tBLOCKED", result.stdout)

    # ---- passing declarations ---------------------------------------------
    def test_level1_complete_passes(self):
        result = self.run_checker(declaration())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VERDICT\tPASS", result.stdout)
        self.assertIn("LEVEL\t1", result.stdout)
        self.assertNotIn("REASON", result.stdout)

    def test_level2_standard_passes(self):
        text = declaration(
            change_class="FEATURE", review_level="R2", evidence_level="2",
            **{"evidence.design_doc": None, "evidence.impact_analysis": None,
               "evidence.rollback_plan": None, "binding.sidecar_anchor": None})
        result = self.run_checker(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VERDICT\tPASS", result.stdout)
        self.assertIn("LEVEL\t2", result.stdout)

    def test_level3_lightweight_docs_pass(self):
        text = declaration(
            change_class="DOC_EDITORIAL", review_level="R1", evidence_level="3",
            **{k: None for k in ("evidence.design_doc", "evidence.impact_analysis",
                                 "evidence.test_log", "evidence.review_record",
                                 "evidence.rollback_plan", "binding.protocol",
                                 "binding.subject_tree_contains_evidence",
                                 "binding.sidecar_anchor")},
            **{"evidence.review_note": "typo fixes only"})
        result = self.run_checker(text)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VERDICT\tPASS", result.stdout)
        self.assertIn("LEVEL\t3", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
