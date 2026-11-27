import tempfile
import unittest
from pathlib import Path
from scripts.ci.check_req_assessment_signatures import RECORDS, inspect

class SignatureCheckerTests(unittest.TestCase):
    def populate(self, root, overrides=None):
        overrides = overrides or {}
        for rel in RECORDS:
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(overrides.get(rel, "assessor: R\nassessed_version: " + "a"*40 + "\nevidence_baseline: main@abc\n"), encoding="utf-8")

    def test_valid_four_reports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); self.populate(root)
            self.assertFalse(any(x.startswith("FAIL ") for x in inspect(root)))

    def test_missing_fields(self):
        samples = {
            "assessor": "assessed_version: " + "a"*40 + "\nevidence_baseline: base\n",
            "assessed_version": "assessor: R\nevidence_baseline: base\n",
            "evidence_baseline": "assessor: R\nassessed_version: " + "a"*40 + "\n",
        }
        for name, body in samples.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); self.populate(root, {RECORDS[0]: body})
                self.assertTrue(any(f"missing or empty {name}" in x for x in inspect(root)))

    def test_invalid_sha(self):
        for sha in ("abc", "g"*40):
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp); self.populate(root, {RECORDS[0]: f"assessor: R\nassessed_version: {sha}\nevidence_baseline: base\n"})
                self.assertTrue(any("full 40-character hexadecimal" in x for x in inspect(root)))

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); self.populate(root); (root/RECORDS[0]).unlink()
            self.assertTrue(any("file missing" in x for x in inspect(root)))

    def test_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); self.populate(root)
            self.assertEqual(inspect(root), inspect(root))

if __name__ == "__main__":
    unittest.main()
