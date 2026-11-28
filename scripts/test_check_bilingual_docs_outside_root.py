
import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().with_name("check_bilingual_docs.py")
SPEC = importlib.util.spec_from_file_location(
    "check_bilingual_docs",
    SCRIPT_PATH,
)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Cannot load module from {SCRIPT_PATH}")

MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

outside_root_markdown_paths = MODULE.outside_root_markdown_paths
outside_root_additions = MODULE.outside_root_additions


class OutsideRootMarkdownTests(unittest.TestCase):
    def setUp(self):
        self.roots = {"00-governance", "14-ai-development"}

    def test_new_markdown_outside_normative_roots_is_rejected(self):
        changed = {
            "reviews/new-review.md": "A",
            "00-governance/new-policy.md": "A",
            "14-ai-development/new-standard.md": "A",
        }

        self.assertEqual(
            outside_root_additions(changed, self.roots),
            ["reviews/new-review.md"],
        )

    def test_modified_markdown_outside_roots_is_not_an_addition(self):
        changed = {
            "reviews/existing-review.md": "M",
        }

        self.assertEqual(
            outside_root_additions(changed, self.roots),
            [],
        )
        self.assertEqual(
            outside_root_markdown_paths(changed, self.roots),
            ["reviews/existing-review.md"],
        )

    def test_deleted_markdown_outside_roots_is_not_an_addition(self):
        changed = {
            "reviews/removed-review.md": "D",
        }

        self.assertEqual(
            outside_root_additions(changed, self.roots),
            [],
        )
        self.assertEqual(
            outside_root_markdown_paths(changed, self.roots),
            ["reviews/removed-review.md"],
        )

    def test_modified_and_deleted_files_preserve_skipped_note_candidates(self):
        changed = {
            "reviews/existing-review.md": "M",
            ".github/old-guidance.md": "D",
            "00-governance/policy.md": "M",
        }

        self.assertEqual(
            outside_root_additions(changed, self.roots),
            [],
        )
        self.assertEqual(
            outside_root_markdown_paths(changed, self.roots),
            [
                "reviews/existing-review.md",
                ".github/old-guidance.md",
            ],
        )

    def test_non_markdown_files_are_ignored(self):
        changed = {
            "reviews/image.png": "A",
            "reviews/data.yaml": "A",
        }

        self.assertEqual(
            outside_root_markdown_paths(changed, self.roots),
            [],
        )
        self.assertEqual(
            outside_root_additions(changed, self.roots),
            [],
        )

    def test_nested_paths_are_classified_by_top_level_root(self):
        changed = {
            "reviews/archive/new-record.MD": "A",
            "14-ai-development/reports/new-record.md": "A",
        }

        self.assertEqual(
            outside_root_additions(changed, self.roots),
            ["reviews/archive/new-record.MD"],
        )

    def test_unknown_status_is_not_treated_as_addition(self):
        changed = {
            "reviews/unknown.md": "R",
        }

        self.assertEqual(
            outside_root_additions(changed, self.roots),
            [],
        )


if __name__ == "__main__":
    unittest.main()
