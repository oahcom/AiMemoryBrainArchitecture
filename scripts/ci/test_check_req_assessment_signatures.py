import tempfile
import unittest
from pathlib import Path

from scripts.ci.check_req_assessment_signatures import ASSESSED_VERSION, FILES, FIELDS, inspect


def valid_content(path, assessor):
    return (
        f"- assessor: {assessor}\n"
        f"- assessed_version: `{ASSESSED_VERSION}`\n"
        f"- evidence_baseline: `main@{ASSESSED_VERSION}:{path}`\n"
    )


class AssessmentDocumentSignatureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative, assessor in FILES:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(valid_content(relative, assessor), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_all_four_documents_pass(self):
        results = inspect(self.root)
        self.assertEqual(4, len(results))
        self.assertTrue(all(item.startswith("PASS ") for item in results))

    def test_each_field_deletion_fails(self):
        for field in FIELDS:
            with self.subTest(field=field):
                relative, assessor = FILES[0]
                target = self.root / relative
                content = "\n".join(
                    line for line in valid_content(relative, assessor).splitlines()
                    if not line.startswith(f"- {field}:")
                ) + "\n"
                target.write_text(content, encoding="utf-8")
                findings = inspect(self.root)
                self.assertTrue(any(item.startswith("FAIL ") and relative in item and field in item for item in findings))
                target.write_text(valid_content(relative, assessor), encoding="utf-8")

    def test_wrong_assessor_fails(self):
        relative, _ = FILES[0]
        target = self.root / relative
        target.write_text(valid_content(relative, "Wrong Principal"), encoding="utf-8")
        self.assertTrue(any("assessor value" in item for item in inspect(self.root)))

    def test_short_and_non_hex_assessed_version_fail(self):
        relative, assessor = FILES[0]
        target = self.root / relative
        for value in ("abc", "g" * 40):
            with self.subTest(value=value):
                target.write_text(
                    f"- assessor: {assessor}\n- assessed_version: `{value}`\n"
                    f"- evidence_baseline: `main@{ASSESSED_VERSION}:{relative}`\n",
                    encoding="utf-8",
                )
                self.assertTrue(any("assessed_version" in item for item in inspect(self.root)))

    def test_wrong_baseline_fails(self):
        relative, assessor = FILES[0]
        target = self.root / relative
        target.write_text(
            f"- assessor: {assessor}\n- assessed_version: `{ASSESSED_VERSION}`\n"
            f"- evidence_baseline: `main@{ASSESSED_VERSION}:wrong/path.md`\n",
            encoding="utf-8",
        )
        self.assertTrue(any("evidence_baseline value" in item for item in inspect(self.root)))

    def test_missing_file_fails(self):
        relative, _ = FILES[0]
        (self.root / relative).unlink()
        self.assertTrue(any(item.startswith(f"FAIL {relative}: file missing") for item in inspect(self.root)))

    def test_empty_file_fails(self):
        relative, _ = FILES[0]
        (self.root / relative).write_text("  \n", encoding="utf-8")
        self.assertTrue(any(item.startswith(f"FAIL {relative}: file is empty") for item in inspect(self.root)))

    def test_output_is_deterministic(self):
        self.assertEqual(inspect(self.root), inspect(self.root))


if __name__ == "__main__":
    unittest.main()
