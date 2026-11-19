#!/usr/bin/env python3
"""Tests for the evidence tiering checker v2 (FIX-2026-P1-T4).

Every case runs against a real temporary Git repository so that commit
objects, subject-tree containment, blob equality and the sidecar anchor are
verified for real (R1 B-01, H-04). Each assertion checks the VERDICT and the
specific REASON code, never the exit code alone.

Run: python test_evidence_tiering.py -v
"""
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check-evidence-tiering.py"


def git(repo, *args, check=True):
    result = subprocess.run(["git", "-C", str(repo)] + list(args),
                            capture_output=True, text=True, encoding="utf-8",
                            errors="replace")
    if check and result.returncode:
        raise AssertionError("git %s failed: %s%s" % (args, result.stdout, result.stderr))
    return result


class Fixture:
    """A real Git repository holding evidence files and a sidecar anchor."""

    def __init__(self, root, sidecar_anchored=True):
        self.root = Path(root)
        self.sidecar_anchored = sidecar_anchored
        self.root.mkdir(parents=True, exist_ok=True)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "test@example.invalid")
        git(self.root, "config", "user.name", "Test")
        (self.root / "README.md").write_text("# repo\n", encoding="utf-8", newline="\n")
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", "initial")
        self.base = git(self.root, "rev-parse", "HEAD").stdout.strip()

        files = {
            "design.md": "# design\n",
            "impact.md": "# impact\n",
            "test.log": "ran 3 tests, ok\n",
            "review.md": "# review\n",
            "rollback.md": "# rollback\n",
            "review-note.md": "# editorial review\n",
            "classify.md": "# classification basis\n",
            "downgrade.md": "# downgrade confirmation\n",
            "evidence.sha256": "design.md aaaa\n",
        }
        for name, content in files.items():
            (self.root / name).write_text(content, encoding="utf-8", newline="\n")
        sidecar_text = (self.root / "evidence.sha256").read_text(encoding="utf-8")
        self.digest = hashlib.sha256(sidecar_text.encode("utf-8")).hexdigest()
        message = "subject commit"
        if self.sidecar_anchored:
            message += "\n\nsidecar-sha256: %s" % self.digest
        git(self.root, "add", ".")
        git(self.root, "commit", "-qm", message)
        self.subject = git(self.root, "rev-parse", "HEAD").stdout.strip()

    def declaration(self, **overrides):
        fields = {
            "work_item": "FIX-TEST-002",
            "change_class": "ARCHITECTURE",
            "review_level": "R3",
            "evidence_level": "1",
            "subject_head": self.subject,
            "base_head": self.base,
            "change_summary": "harden evidence binding",
            "classification_basis": "architecture contract changed",
            "assessed_by": "owner-g",
            "assessed_at": "2026-11-20T00:00:00+08:00",
            "rationale": "architecture semantics changed, Level 1 required",
            "source_authenticity": "NOT_VERIFIED",
            "evidence.design_doc": "design.md",
            "evidence.impact_analysis": "impact.md",
            "evidence.test_log": "test.log",
            "evidence.review_record": "review.md",
            "evidence.rollback_plan": "rollback.md",
            "binding.protocol": "v3",
            "binding.sidecar_path": "evidence.sha256",
            "binding.sidecar_anchor": "sha256:%s" % self.digest,
            "authenticity.acknowledged": "true",
        }
        for key, value in overrides.items():
            if value is None:
                fields.pop(key, None)
            else:
                fields[key] = value
        return render(fields)

    def write_declaration(self, text, name="declaration.yaml"):
        path = self.root / name
        path.write_text(text, encoding="utf-8", newline="\n")
        return path


def render(fields):
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
    def run_checker(self, fixture, text, repo=True):
        path = fixture.write_declaration(text)
        args = [sys.executable, CHECKER.as_posix(), path.as_posix()]
        if repo:
            args += ["--repo", fixture.root.as_posix()]
        return subprocess.run(args, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", check=False)

    def check(self, text):
        """Run against a fresh fixture whose declaration is the given text."""
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            return self.run_checker(fixture, text)

    def assert_blocked(self, result, code):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("VERDICT\tBLOCKED", result.stdout)
        self.assertIn("REASON\t%s" % code, result.stdout)

    def passed(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VERDICT\tPASS", result.stdout)
        self.assertNotIn("REASON", result.stdout)

    # ---- GO acceptance gates 1-8 -------------------------------------------
    def test_gate1_missing_level_declaration(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(evidence_level=None)),
                                "CE_NO_LEVEL")

    def test_gate2_level_conflicts_with_risk_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(change_class="SECURITY", evidence_level="3",
                                       review_level="R2",
                                       **{"evidence.review_note": "note",
                                          "classification_confirmed_by": "reviewer-x",
                                          "classification_record": "classify.md"})
            self.assert_blocked(self.run_checker(fixture, text), "CE_LEVEL_CLASS_CONFLICT")

    def test_gate3_level1_required_field_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(
                self.run_checker(fixture, fixture.declaration(**{"evidence.rollback_plan": None})),
                "CE_L1_MISSING_FIELD")

    def test_gate4_unknown_class_assigned_level(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(change_class="UNKNOWN")),
                                "CE_UNKNOWN_CLASS")

    def test_gate5_v3_binding_protocol_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(**{"binding.protocol": None})),
                                "CE_NO_BINDING_PROTOCOL")

    def test_gate6_sha_format_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(subject_head="abc123")),
                                "CE_BAD_SHA")

    def test_gate7_not_verified_cannot_pass_silently(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(
                self.run_checker(fixture, fixture.declaration(**{"authenticity.acknowledged": None})),
                "CE_AUTH_NOT_ACK")

    def test_gate8_unparseable_input_fails_closed(self):
        self.assert_blocked(self.check("this is not yaml at all\n"), "CE_UNPARSABLE")

    # ---- B-01: real v3 binding --------------------------------------------
    def test_subject_head_must_be_commit_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            tree = git(fixture.root, "rev-parse", "HEAD^{tree}").stdout.strip()
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(subject_head=tree)),
                                "CE_BAD_SUBJECT")

    def test_evidence_absent_from_subject_tree_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(**{"evidence.design_doc": "missing.md"})
            self.assert_blocked(self.run_checker(fixture, text), "CE_EVIDENCE_NOT_IN_SUBJECT")

    def test_worktree_blob_mismatch_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            fixture = Fixture(root)
            (root / "design.md").write_text("# edited after commit\n",
                                            encoding="utf-8", newline="\n")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration()), "CE_BLOB_MISMATCH")

    def test_sidecar_anchor_digest_mismatch_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(**{"binding.sidecar_anchor": "sha256:%s" % ("0" * 64)})
            self.assert_blocked(self.run_checker(fixture, text), "CE_SIDECAR_MISMATCH")

    def test_sidecar_not_anchored_in_commit_message_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo", sidecar_anchored=False)
            self.assert_blocked(self.run_checker(fixture, fixture.declaration()), "CE_SIDECAR_UNANCHORED")

    def test_missing_sidecar_path_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(
                self.run_checker(fixture, fixture.declaration(**{"binding.sidecar_path": None})),
                "CE_NO_SIDECAR_PATH")

    def test_no_repository_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "declaration.yaml"
            path.write_text("work_item: X\n", encoding="utf-8", newline="\n")
            result = subprocess.run([sys.executable, CHECKER.as_posix(), path.as_posix()],
                                    capture_output=True, text=True, encoding="utf-8",
                                    errors="replace")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("REASON\tCE_NO_REPO", result.stdout)

    # ---- B-02: R2 downgrade confirmation ----------------------------------
    def test_r2_downgrade_requires_confirmer(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(
                change_class="DOC_EDITORIAL", review_level="R2", evidence_level="3",
                **{"evidence.review_note": "editorial", "classification_confirmed_by": "reviewer-y",
                   "classification_record": "classify.md",
                   "downgrade_justification": "typo fixes",
                   "downgrade_confirmation_record": "downgrade.md"})
            self.assert_blocked(self.run_checker(fixture, text), "CE_R2_DOWNGRADE_UNCONFIRMED")

    def test_r2_downgrade_self_confirmation_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(
                change_class="DOC_EDITORIAL", review_level="R2", evidence_level="3",
                **{"evidence.review_note": "editorial", "classification_confirmed_by": "reviewer-y",
                   "classification_record": "classify.md",
                   "downgrade_justification": "typo fixes",
                   "downgrade_confirmed_by": "owner-g",
                   "downgrade_confirmation_record": "downgrade.md"})
            self.assert_blocked(self.run_checker(fixture, text), "CE_R2_DOWNGRADE_SELF_CONFIRMED")

    def test_r2_downgrade_without_justification_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(
                change_class="DOC_EDITORIAL", review_level="R2", evidence_level="3",
                **{"evidence.review_note": "editorial", "classification_confirmed_by": "reviewer-y",
                   "classification_record": "classify.md",
                   "downgrade_confirmed_by": "reviewer-y",
                   "downgrade_confirmation_record": "downgrade.md"})
            self.assert_blocked(self.run_checker(fixture, text), "CE_R2_AUTO_DOWNGRADE")

    # ---- B-03: classification trust boundary ------------------------------
    def test_lower_class_requires_independent_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(change_class="FEATURE", review_level="R2",
                                       evidence_level="2",
                                       **{"classification_record": "classify.md"})
            self.assert_blocked(self.run_checker(fixture, text), "CE_CLASS_UNCONFIRMED")

    def test_classification_self_confirmation_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(change_class="FEATURE", review_level="R2",
                                       evidence_level="2",
                                       **{"classification_confirmed_by": "owner-g",
                                          "classification_record": "classify.md"})
            self.assert_blocked(self.run_checker(fixture, text), "CE_CLASS_SELF_CONFIRMED")

    def test_classification_basis_always_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(classification_basis=None)),
                                "CE_NO_CLASSIFICATION_BASIS")

    # ---- H-01 / H-02: audit fields and review level ------------------------
    def test_audit_fields_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(assessed_by=None)),
                                "CE_NO_AUDIT_FIELD")

    def test_base_head_must_be_ancestor(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            # A commit on another branch is not an ancestor of the subject.
            git(fixture.root, "checkout", "-q", "-b", "side", fixture.base)
            (fixture.root / "side.md").write_text("side\n", encoding="utf-8", newline="\n")
            git(fixture.root, "add", ".")
            git(fixture.root, "commit", "-qm", "side")
            side = git(fixture.root, "rev-parse", "HEAD").stdout.strip()
            text = fixture.declaration(base_head=side)
            self.assert_blocked(self.run_checker(fixture, text), "CE_BASE_NOT_ANCESTOR")

    def test_review_level_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(review_level=None)),
                                "CE_NO_REVIEW_LEVEL")

    def test_review_level_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            self.assert_blocked(self.run_checker(fixture, fixture.declaration(review_level="R9")),
                                "CE_BAD_REVIEW_LEVEL")

    # ---- H-03: strict parser ---------------------------------------------
    def test_tab_indentation_rejected(self):
        self.assert_blocked(self.check("work_item: X\nevidence:\n\tdesign_doc: a.md\n"),
                            "CE_UNPARSABLE")

    def test_four_space_indent_rejected(self):
        self.assert_blocked(self.check("work_item: X\nevidence:\n    design_doc: a.md\n"),
                            "CE_UNPARSABLE")

    def test_duplicate_key_rejected(self):
        self.assert_blocked(self.check("work_item: X\nwork_item: Y\n"), "CE_UNPARSABLE")

    def test_nested_block_header_rejected(self):
        self.assert_blocked(self.check("work_item: X\nevidence:\n  inner:\n"), "CE_UNPARSABLE")

    # ---- passing declarations --------------------------------------------
    def test_level1_complete_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            result = self.run_checker(fixture, fixture.declaration())
            self.passed(result)
            self.assertIn("LEVEL\t1", result.stdout)

    def test_level2_standard_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(
                change_class="FEATURE", review_level="R2", evidence_level="2",
                **{"evidence.design_doc": None, "evidence.impact_analysis": None,
                   "evidence.rollback_plan": None,
                   "binding.sidecar_path": None, "binding.sidecar_anchor": None,
                   "classification_confirmed_by": "reviewer-z",
                   "classification_record": "classify.md"})
            result = self.run_checker(fixture, text)
            self.passed(result)
            self.assertIn("LEVEL\t2", result.stdout)

    def test_level3_lightweight_docs_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Fixture(Path(tmp) / "repo")
            text = fixture.declaration(
                change_class="DOC_EDITORIAL", review_level="R1", evidence_level="3",
                **{"evidence.design_doc": None, "evidence.impact_analysis": None,
                   "evidence.test_log": None, "evidence.review_record": None,
                   "evidence.rollback_plan": None, "evidence.review_note": "review-note.md",
                   "binding.sidecar_path": None, "binding.sidecar_anchor": None,
                   "classification_confirmed_by": "reviewer-z",
                   "classification_record": "classify.md"})
            result = self.run_checker(fixture, text)
            self.passed(result)
            self.assertIn("LEVEL\t3", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
