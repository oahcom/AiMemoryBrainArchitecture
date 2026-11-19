#!/usr/bin/env python3
"""Cross-artifact regression: the documented declaration example must pass the shipped checker.

FIX-2026-P1-T4-FU1 closed two defects that were invisible to the existing 67 tests,
because those build their declarations by hand and never read the documentation:

  1. the template example wrote evidence paths bundle-relative ("design.md") while
     verify_path() resolves every declared value against the repository root of
     subject_head, so a work item copying the example verbatim was blocked on files
     that did exist;
  2. evidence.review_note was shown as free text while LEVEL3_FIELDS feeds it through
     the same path verifier.

Both are documentation defects, so a test over the checker alone cannot catch them
returning. This module reads the example out of the shipped template and runs it, which
is the only mechanism that ties the documented shape to the executable one.

Each case asserts VERDICT and the exact set of REASON codes; an exit code alone is not
evidence (AI-STD-001 acceptance rule). Asserting the exact set rather than membership is
deliberate: a case is only causal when the control passes and the treatment changes one
field, so any second reason would mean the case is accusing the wrong thing.

This module reads the template, so a legitimate change to the example (a new field, say)
will make these cases fail until the fixture and the expectation are updated to match.
That is the intended cost: the example is what adopters copy, so it is a contract, and a
contract change should stop the build rather than pass silently. What must NOT happen in
that situation is relaxing an assertion to get green again - if the example stops being
executable, the fix belongs in the template or the checker.

Run: python test_template_example_executable.py -v
"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check-evidence-tiering.py"
REPO = HERE.parents[2]
TEMPLATE = REPO / "14-ai-development" / "prompt-and-evidence-template.md"
SECTION = "## 4.1 Evidence depth declaration"
SUBJECT_PLACEHOLDER = 'subject_head: "<40-hex commit>"'
BASE_PLACEHOLDER = 'base_head: "<40-hex ancestor commit>"'
BUNDLE_PREFIX = "14-ai-development/work-items/"


def load_checker():
    """Import the shipped checker so the test uses the shipped parser, not a copy."""
    spec = importlib.util.spec_from_file_location("evidence_tiering_checker", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reason_codes(result):
    """The exact set of REASON codes the checker emitted."""
    return {line.split("\t")[1] for line in result.stdout.splitlines()
            if line.startswith("REASON\t")}


def extract_example():
    """Return the YAML example exactly as the template prints it."""
    text = TEMPLATE.read_text(encoding="utf-8")
    if SECTION not in text:
        raise AssertionError("template section not found: %s" % SECTION)
    after = text.split(SECTION, 1)[1]
    if "```yaml" not in after:
        raise AssertionError("no yaml block after %s" % SECTION)
    body = after.split("```yaml", 1)[1]
    if "```" not in body:
        raise AssertionError("unterminated yaml block in the template section")
    return body.split("```", 1)[0]


class TemplateExampleExecutableTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.checker = load_checker()
        cls.example = extract_example()

    def materialise(self, tmp):
        """Build a real repo whose tree contains every path the example declares."""
        root = Path(tmp) / "repo"
        root.mkdir(parents=True)
        self.git(root, "init", "-q")
        self.git(root, "config", "user.email", "test@example.invalid")
        self.git(root, "config", "user.name", "test")
        # The example declares repository: oahcom/AiMemoryBrainArchitecture, and the
        # checker verifies that claim against the origin remote, so a fixture without
        # the matching origin is rejected for a reason that has nothing to do with the
        # example. Each case must fail for its own reason, not for the fixture's.
        decl = self.checker.parse_declaration(self.example)
        self.git(root, "remote", "add", "origin",
                 "https://github.com/%s.git" % decl["repository"])

        paths = list(decl["evidence"].values())
        if decl.get("classification_record"):
            paths.append(decl["classification_record"])

        for rel in paths:
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("evidence body for %s\n" % rel, encoding="utf-8")

        self.git(root, "add", "-A")
        self.git(root, "commit", "-q", "-m", "evidence")
        head = self.git(root, "rev-parse", "HEAD").stdout.strip()
        return root, head

    def git(self, root, *args):
        result = subprocess.run(["git", "-C", str(root)] + list(args),
                                capture_output=True, text=True, encoding="utf-8",
                                errors="replace")
        if result.returncode:
            raise AssertionError("git %s failed: %s%s" % (args, result.stdout, result.stderr))
        return result

    def run_declaration(self, root, text):
        decl_path = root / "evidence-declaration.yaml"
        decl_path.write_text(text, encoding="utf-8", newline="\n")
        return subprocess.run(
            [sys.executable, CHECKER.as_posix(), decl_path.as_posix(),
             "--repo", root.as_posix()],
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)

    def fill_heads(self, text, head):
        self.assertIn(SUBJECT_PLACEHOLDER, text,
                      "the example must keep its subject_head placeholder, otherwise this test "
                      "is no longer exercising what a reader copies")
        self.assertIn(BASE_PLACEHOLDER, text, "the example must keep its base_head placeholder")
        return (text.replace(SUBJECT_PLACEHOLDER, 'subject_head: "%s"' % head)
                    .replace(BASE_PLACEHOLDER, 'base_head: "%s"' % head))

    # ---- the example as printed must pass ----------------------------------
    def test_documented_example_passes_verbatim(self):
        """The example executes as printed.

        Known limit, measured rather than assumed: this case is self-consistent, not
        correct. The fixture creates whatever the declaration names, so an example that
        writes "design.md" also passes here - it just gets a design.md at the repository
        root. That limit is why test_example_evidence_paths_are_root_relative_bundle_paths
        states the expected path base independently of the template.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root, head = self.materialise(tmp)
            result = self.run_declaration(root, self.fill_heads(self.example, head))
            self.assertEqual(result.returncode, 0,
                             "the template example does not pass the shipped checker:\n"
                             + result.stdout + result.stderr)
            self.assertIn("VERDICT\tPASS", result.stdout)
            self.assertNotIn("REASON", result.stdout,
                             "the example produced reasons:\n" + result.stdout)

    def test_example_keeps_evidence_paths_root_relative(self):
        """A bundle-relative evidence path is the FU1 defect; it must still be blocked.

        The control for this case is the test above: the example passes verbatim, so every
        other condition is already satisfied and the only thing this case changes is one
        evidence path. That is why the reason set is asserted exactly rather than as a
        membership test - a membership test would also pass if the flat path were blocked
        for some unrelated reason that happened to emit the same code.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root, head = self.materialise(tmp)
            text = self.fill_heads(self.example, head)
            decl = self.checker.parse_declaration(text)
            design = decl["evidence"]["design_doc"]
            flattened = text.replace('"%s"' % design, '"%s"' % Path(design).name)
            self.assertNotEqual(flattened, text, "design_doc path did not occur as declared")

            result = self.run_declaration(root, flattened)
            self.assertIn("VERDICT\tBLOCKED", result.stdout, result.stdout + result.stderr)
            self.assertEqual(reason_codes(result), {"CE_EVIDENCE_NOT_IN_SUBJECT"},
                             "resolving evidence paths against the declaration directory instead "
                             "of the repository root must be the only reason:\n" + result.stdout)

    def test_example_evidence_paths_are_root_relative_bundle_paths(self):
        """The example must show the path base, not rely on a lucky layout.

        This case exists because the verbatim case cannot catch the FU1 path defect on its
        own: the fixture materialises whatever the declaration names, so an example writing
        "design.md" also passes once the fixture drops a design.md at the repository root.
        Self-consistency is not correctness. The expectation below is stated independently
        of the template - every evidence path is written from the repository root into the
        work item bundle - so a bare filename is caught here even though it would execute.
        """
        decl = self.checker.parse_declaration(self.example)
        values = list(decl["evidence"].values())
        if decl.get("classification_record"):
            values.append(decl["classification_record"])
        self.assertTrue(values, "the example declares no evidence paths")
        for value in values:
            self.assertTrue(value.startswith(BUNDLE_PREFIX),
                            "the example declares %r, which does not show that evidence paths "
                            "are written from the repository root; a bare filename only "
                            "executes when the file happens to sit at the root" % value)

    def level3_variant(self):
        """The example reshaped so Level 3 is legal, leaving one field to isolate.

        FEATURE cannot be Level 3 (CE_LEVEL_CLASS_CONFLICT) and R2 to Level 3 is a downgrade
        that needs its own justification, so a control built on the example as printed would
        fail for reasons unrelated to review_note. DOC_EDITORIAL at R1 reaches Level 3 with no
        extra fields, which is what makes the pair below a controlled comparison.
        """
        text = self.example.replace("evidence_level: 2", "evidence_level: 3", 1)
        text = text.replace('change_class: "FEATURE"', 'change_class: "DOC_EDITORIAL"', 1)
        text = text.replace('review_level: "R2"', 'review_level: "R1"', 1)
        self.assertIn("evidence_level: 3", text)
        self.assertIn('change_class: "DOC_EDITORIAL"', text)
        self.assertIn('review_level: "R1"', text)
        return text

    def test_level3_control_passes(self):
        """Control: a Level 3 declaration that differs from the treatment only in review_note.

        Without this case the treatment below cannot be read as causal: BLOCKED at Level 3
        could otherwise come from any other Level 3 condition, and the test would be
        asserting a coincidence.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root, head = self.materialise(tmp)
            result = self.run_declaration(root, self.fill_heads(self.level3_variant(), head))
            self.assertEqual(result.returncode, 0,
                             "the Level 3 control does not pass, so the review_note case cannot "
                             "isolate its cause:\n" + result.stdout + result.stderr)
            self.assertIn("VERDICT\tPASS", result.stdout)
            self.assertNotIn("REASON", result.stdout, result.stdout)

    def test_level3_review_note_must_still_be_a_path(self):
        """Level 3 verifies review_note, so free text there must be blocked, not accepted."""
        with tempfile.TemporaryDirectory() as tmp:
            root, head = self.materialise(tmp)
            text = self.fill_heads(self.level3_variant(), head)

            decl = self.checker.parse_declaration(text)
            note = decl["evidence"]["review_note"]
            with_text = text.replace('"%s"' % note, '"reviewer acknowledgement"')
            self.assertNotEqual(with_text, text,
                                "the example no longer declares review_note as a path, so this "
                                "case cannot be constructed; the defect it guards against has "
                                "returned to the template itself")

            result = self.run_declaration(root, with_text)
            self.assertIn("VERDICT\tBLOCKED", result.stdout,
                          "free text in review_note was accepted at Level 3:\n" + result.stdout)
            self.assertEqual(reason_codes(result), {"CE_EVIDENCE_NOT_IN_SUBJECT"},
                             "with the Level 3 control passing, review_note must be the only "
                             "reason; anything else means the case is not isolating its "
                             "cause:\n" + result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
