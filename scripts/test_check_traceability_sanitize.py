"""Regression tests for INDEX.md sanitization in check_traceability."""

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_traceability.py")
SPEC = importlib.util.spec_from_file_location(
    "check_traceability_sanitize_target",
    MODULE_PATH,
)
if SPEC is None or SPEC.loader is None:
    raise ImportError("Cannot load scripts/check_traceability.py")

MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

sanitize_index_text = MODULE.sanitize_index_text
AID_LINK_RE = MODULE.AID_LINK_RE


class SanitizeIndexTextTests(unittest.TestCase):
    def find_aids(self, text):
        return [
            match.group(1)
            for match in AID_LINK_RE.finditer(sanitize_index_text(text))
        ]

    def test_single_line_html_comment_is_not_recognized(self):
        text = (
            "<!-- [AID-2026-001](AID-2026-001/manifest.yaml) -->\n"
        )
        self.assertEqual(self.find_aids(text), [])

    def test_multiline_html_comment_is_not_recognized(self):
        text = (
            "<!--\n"
            "[AID-2026-002](AID-2026-002/manifest.yaml)\n"
            "-->\n"
        )
        self.assertEqual(self.find_aids(text), [])

    def test_fenced_code_link_is_not_recognized(self):
        text = (
            "```markdown\n"
            "[AID-2026-003](AID-2026-003/manifest.yaml)\n"
            "```\n"
        )
        self.assertEqual(self.find_aids(text), [])

    def test_link_outside_comments_and_fences_is_recognized(self):
        text = (
            "<!-- [AID-2026-001](AID-2026-001/manifest.yaml) -->\n"
            "```markdown\n"
            "[AID-2026-002](AID-2026-002/manifest.yaml)\n"
            "```\n"
            "[AID-2026-004](AID-2026-004/manifest.yaml)\n"
        )
        self.assertEqual(
            self.find_aids(text),
            ["AID-2026-004"],
        )

    def test_line_count_is_preserved(self):
        text = (
            "before\n"
            "<!-- comment starts\n"
            "[AID-2026-001](AID-2026-001/manifest.yaml)\n"
            "comment ends --> after\n"
            "```markdown\n"
            "[AID-2026-002](AID-2026-002/manifest.yaml)\n"
            "```\n"
            "after\n"
        )
        cleaned = sanitize_index_text(text)
        self.assertEqual(
            len(cleaned.splitlines()),
            len(text.splitlines()),
        )

    def test_sanitization_is_idempotent(self):
        text = (
            "before\n"
            "<!-- hidden\n"
            "[AID-2026-001](AID-2026-001/manifest.yaml)\n"
            "-->\n"
            "```markdown\n"
            "[AID-2026-002](AID-2026-002/manifest.yaml)\n"
            "```\n"
            "[AID-2026-003](AID-2026-003/manifest.yaml)\n"
        )
        once = sanitize_index_text(text)
        twice = sanitize_index_text(once)
        self.assertEqual(twice, once)


if __name__ == "__main__":
    unittest.main()
