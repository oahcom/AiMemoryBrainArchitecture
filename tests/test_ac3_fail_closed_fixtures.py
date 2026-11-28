#!/usr/bin/env python3
"""AC3 fail-closed fixtures for both governance checkers."""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_governance_operation_traceability import FILES as GOVERNANCE_FILES  # noqa: E402
from check_owner_namespace_references import FILES as OWNER_FILES  # noqa: E402
from gov_doc_fail_closed import validate_group  # noqa: E402


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = "00-governance/architecture-document-metadata.schema.yaml"


class FailClosedFixtureTests(unittest.TestCase):
    def make_fixture(self, registered_files: tuple[str, ...]) -> Path:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)

        paths = (SCHEMA_PATH, *registered_files)
        for relative in paths:
            source = REPOSITORY_ROOT / relative
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        self.addCleanup(self.temp.cleanup)
        return root

    def assert_fail_closed(self, root: Path, files: tuple[str, ...]) -> None:
        errors = validate_group(root, files)
        self.assertTrue(errors, "negative fixture unexpectedly passed")
        self.assertTrue(
            all(item.startswith("FAIL_CLOSED:") for item in errors),
            errors,
        )

    def test_owner_namespace_complete_group_passes(self):
        root = self.make_fixture(OWNER_FILES)
        self.assertEqual(validate_group(root, OWNER_FILES), [])

    def test_owner_namespace_missing_member_fails_closed(self):
        root = self.make_fixture(OWNER_FILES)
        (root / OWNER_FILES[0]).unlink()
        self.assert_fail_closed(root, OWNER_FILES)

    def test_owner_namespace_unclassified_member_fails_closed(self):
        root = self.make_fixture(OWNER_FILES)
        target = root / OWNER_FILES[0]
        content = target.read_text(encoding="utf-8")
        closing = content.find("---", 4)
        self.assertGreater(closing, 0)
        target.write_text(
            content[closing + 3:].lstrip("\r\n"),
            encoding="utf-8",
            newline="\n",
        )
        self.assert_fail_closed(root, OWNER_FILES)

    def test_governance_complete_group_passes(self):
        root = self.make_fixture(GOVERNANCE_FILES)
        self.assertEqual(validate_group(root, GOVERNANCE_FILES), [])

    def test_governance_missing_member_fails_closed(self):
        root = self.make_fixture(GOVERNANCE_FILES)
        (root / GOVERNANCE_FILES[0]).unlink()
        self.assert_fail_closed(root, GOVERNANCE_FILES)

    def test_governance_unclassified_member_fails_closed(self):
        root = self.make_fixture(GOVERNANCE_FILES)
        target = root / GOVERNANCE_FILES[0]
        content = target.read_text(encoding="utf-8")
        closing = content.find("---", 4)
        self.assertGreater(closing, 0)
        target.write_text(
            content[closing + 3:].lstrip("\r\n"),
            encoding="utf-8",
            newline="\n",
        )
        self.assert_fail_closed(root, GOVERNANCE_FILES)

    def test_unreadable_registered_document_fails_closed(self):
        root = self.make_fixture(OWNER_FILES)
        target = (root / "01-system-architecture" / "component-map.md").resolve()
        original_read_text = Path.read_text

        def read_text_with_permission_error(path, *args, **kwargs):
            if path.resolve() == target:
                raise PermissionError("fixture: simulated unreadable document")
            return original_read_text(path, *args, **kwargs)

        with patch.object(
            Path,
            "read_text",
            autospec=True,
            side_effect=read_text_with_permission_error,
        ):
            errors = validate_group(root, OWNER_FILES)

        self.assertTrue(errors, "unreadable fixture unexpectedly passed")
        self.assertTrue(
            any(item.startswith("FAIL_CLOSED:") for item in errors),
            errors,
        )

    def test_source_mirror_counterpart_mismatch_fails_closed(self):
        root = self.make_fixture(OWNER_FILES)
        mirror = root / "docs" / "en" / "01-system-architecture" / "component-map.md"
        original_text = mirror.read_text(encoding="utf-8")

        pattern = re.compile(
            r"(?m)^([ \t]*source:[ \t]*)(?:[\'\"])?[^\'\"\r\n]*(?:[\'\"])?$"
        )
        modified_text, replacements = pattern.subn(
            r"\g<1>01-system-architecture/system-boundaries.md",
            original_text,
            count=1,
        )
        self.assertEqual(
            replacements,
            1,
            "expected exactly one bilingual_counterpart.source line",
        )
        mirror.write_text(modified_text, encoding="utf-8", newline="")

        errors = validate_group(root, OWNER_FILES)

        self.assertTrue(errors, "source/mirror mismatch unexpectedly passed")
        self.assertTrue(
            any(item.startswith("FAIL_CLOSED:") for item in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
