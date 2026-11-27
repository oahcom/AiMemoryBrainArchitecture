import tempfile
import unittest
from pathlib import Path

from scripts.ci.check_req_assessment_signatures import RECORDS, inspect


class SignatureCheckerTests(unittest.TestCase):
    def populate(self, root: Path, overrides=None):
        overrides = overrides or {}
        valid = (
            "assessor: R — historical assessor; session identity not recorded\n"
            + "assessed_version: " + "a" * 40 + "\n"
            + "evidence_baseline: main@" + "a" * 40 + "\n"
        )
        for relative in RECORDS:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(overrides.get(relative, valid), encoding="utf-8")

    def test_valid_four_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.populate(Path(temporary))
            findings = inspect(Path(temporary))
            self.assertEqual(4, sum(item.startswith("PASS ") for item in findings))
            self.assertFalse(any(item.startswith("FAIL ") for item in findings))

    def test_each_missing_field_fails(self):
        samples = {
            "assessor": "assessed_version: " + "a" * 40 + "\nevidence_baseline: base\n",
            "assessed_version": "assessor: R\nevidence_baseline: base\n",
            "evidence_baseline": "assessor: R\nassessed_version: " + "a" * 40 + "\n",
        }
        for name, body in samples.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.populate(root, {RECORDS[0]: body})
                self.assertTrue(
                    any(f"missing or empty {name}" in item for item in inspect(root))
                )

    def test_invalid_sha_fails(self):
        for value in ("abc", "g" * 40):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                body = (
                    "assessor: R\n"
                    f"assessed_version: {value}\n"
                    "evidence_baseline: main@base\n"
                )
                self.populate(root, {RECORDS[0]: body})
                self.assertTrue(
                    any("full 40-character hexadecimal" in item for item in inspect(root))
                )

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.populate(root)
            (root / RECORDS[0]).unlink()
            self.assertTrue(
                any("file missing" in item for item in inspect(root))
            )

    def test_deterministic_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.populate(root)
            self.assertEqual(inspect(root), inspect(root))


if __name__ == "__main__":
    unittest.main()
