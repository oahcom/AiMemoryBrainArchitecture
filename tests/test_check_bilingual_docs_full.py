import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_bilingual_docs_full as checker


class FullRepositoryCheckerTests(unittest.TestCase):
    def test_root_architecture_requires_both_mirrors(self):
        files = {
            "01-system-architecture/spec.md",
            "docs/en/01-system-architecture/spec.md",
            "docs/zh-CN/01-system-architecture/spec.md",
        }
        self.assertEqual(
            checker.counterpart("01-system-architecture/spec.md", files),
            "docs/en/01-system-architecture/spec.md + docs/zh-CN/01-system-architecture/spec.md",
        )

    def test_missing_mirror_is_reportable(self):
        files = {
            "01-system-architecture/spec.md",
            "docs/en/01-system-architecture/spec.md",
        }
        self.assertIsNone(
            checker.counterpart("01-system-architecture/spec.md", files)
        )

    def test_ai_development_side_by_side_pair(self):
        files = {
            "14-ai-development/example.md",
            "14-ai-development/example.en.md",
        }
        self.assertEqual(
            checker.counterpart("14-ai-development/example.md", files),
            "14-ai-development/example.en.md",
        )

    def test_side_by_side_pair_outside_ai_development(self):
        # The incremental gate accepts a side-by-side pair in every normative
        # root; the full scan only accepted it under 14-ai-development, so the
        # two required contexts called the same two files clean and dirty at once.
        files = {
            "08-bmcp-protocol/protocol-index.md",
            "08-bmcp-protocol/protocol-index.zh-CN.md",
        }
        self.assertEqual(
            checker.counterpart("08-bmcp-protocol/protocol-index.md", files),
            "08-bmcp-protocol/protocol-index.zh-CN.md",
        )
        self.assertEqual(
            checker.counterpart("08-bmcp-protocol/protocol-index.zh-CN.md", files),
            "08-bmcp-protocol/protocol-index.md",
        )

    def test_root_set_matches_the_authority(self):
        # One authority for "what is normative": the required incremental gate.
        # A second literal is how seven phantom roots came to be listed.
        import check_bilingual_docs

        self.assertEqual(checker.NORMATIVE_ROOTS, check_bilingual_docs.NORMATIVE_ROOTS)
        self.assertEqual(checker.ROOT, check_bilingual_docs.ROOT)

    def test_operational_subtrees_are_explicitly_exempt(self):
        files = {"14-ai-development/work-items/AID-1/prompt.md"}
        self.assertIn(
            "operational",
            checker.counterpart("14-ai-development/work-items/AID-1/prompt.md", files),
        )

    def test_scope_is_markdown_only(self):
        self.assertTrue(checker.in_scope("docs/en/00-governance/guide.md"))
        self.assertFalse(checker.in_scope("src/lib.rs"))
        self.assertFalse(checker.in_scope("docs/en/00-governance/logo.png"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
