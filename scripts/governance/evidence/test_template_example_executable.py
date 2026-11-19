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

Each case asserts VERDICT and the specific REASON code; an exit code alone is not
evidence (AI-STD-001 acceptance rule).

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


def load_checker():
    """Import the shipped checker so the test uses the shipped parser, not a copy."""
    spec = importlib.util.spec_from_file_location("evidence_tiering_checker", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
        """A bundle-relative evidence path is the FU1 defect; it must still be blocked."""
        with tempfile.TemporaryDirectory() as tmp:
            root, head = self.materialise(tmp)
            text = self.fill_heads(self.example, head)
            decl = self.checker.parse_declaration(text)
            design = decl["evidence"]["design_doc"]
            flattened = text.replace('"%s"' % design, '"%s"' % Path(design).name)
            self.assertNotEqual(flattened, text, "design_doc path did not occur as declared")

            result = self.run_declaration(root, flattened)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("VERDICT\tBLOCKED", result.stdout)
            self.assertIn("REASON\tCE_EVIDENCE_NOT_IN_SUBJECT", result.stdout,
                          "resolving evidence paths against the declaration directory instead of "
                          "the repository root is no longer rejected:\n" + result.stdout)

    def test_level3_review_note_must_still_be_a_path(self):
        """Level 3 verifies review_note, so free text there must be blocked, not accepted."""
        with tempfile.TemporaryDirectory() as tmp:
            root, head = self.materialise(tmp)
            text = self.fill_heads(self.example, head)
            self.assertIn("evidence_level: 2", text, "the example is expected to declare Level 2")
            text = text.replace("evidence_level: 2", "evidence_level: 3", 1)

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
            self.assertIn("REASON\tCE_EVIDENCE_NOT_IN_SUBJECT", result.stdout,
                          "review_note is documented as a path but is not verified as one:\n"
                          + result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
