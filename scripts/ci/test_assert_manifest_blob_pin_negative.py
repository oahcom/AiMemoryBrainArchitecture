import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parent
    / "assert_manifest_blob_pin_negative.py"
)

COMMIT = "9a2063ae1fa5d905b3817cd4eddba065a06daa73"

SUMMARY = (
    "main=9a2063ae1fa5d905b3817cd4eddba065a06daa73 "
    "manifests=108 pins=169 ok=85 mismatch=80 "
    "path_missing=0 incomplete=1 unbound=4"
)

EXPECTED_INCOMPLETE = (
    "INCOMPLETE related_evidence[0]: missing or invalid "
    "reference_mode=None; expected 'historical' or 'current'"
)


class NegativeAssertionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        checker_dir = self.root / "scripts" / "ci"
        checker_dir.mkdir(parents=True)
        self.checker = checker_dir / "check_manifest_blob_pins.py"

    def tearDown(self):
        self.temp.cleanup()

    def write_checker(self, body):
        self.checker.write_text(body, encoding="utf-8")

    def run_assertion(self):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--commit",
                COMMIT,
                "--root",
                str(self.root),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def valid_negative_checker(self):
        lines = [
            "#!/usr/bin/env python3",
            "import sys",
            f"print({SUMMARY!r})",
        ]
        lines.extend(
            f"print('MISMATCH fixture-{i} path=file-{i} declared=old actual=new')"
            for i in range(80)
        )
        lines.extend(
            f"print('UNBOUND_BLOB_SHA256 manifest=m{i} pointer=/p/f field=f declared=d')"
            for i in range(4)
        )
        lines.append(f"print({EXPECTED_INCOMPLETE!r})")
        lines.append("sys.exit(2)")
        return "\n".join(lines) + "\n"

    def test_exact_negative_evidence_with_exit_two_passes(self):
        self.write_checker(self.valid_negative_checker())
        result = self.run_assertion()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NEGATIVE_ASSERTION_PASS", result.stdout)

    def test_checker_exit_zero_is_a_violation(self):
        self.write_checker(
            "import sys\n"
            f"print({SUMMARY!r})\n"
            "sys.exit(0)\n"
        )
        result = self.run_assertion()
        self.assertEqual(result.returncode, 1)
        self.assertIn("was not rejected", result.stderr)

    def test_checker_exit_one_is_a_violation(self):
        self.write_checker(
            "import sys\n"
            f"print({SUMMARY!r})\n"
            "sys.exit(1)\n"
        )
        result = self.run_assertion()
        self.assertEqual(result.returncode, 1)
        self.assertIn("负样本未被正确拒绝", result.stderr)

    def test_exit_two_without_expected_evidence_is_a_violation(self):
        self.write_checker("import sys\nsys.exit(2)\n")
        result = self.run_assertion()
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected immutable evidence", result.stderr)

    def test_wrong_summary_is_a_violation(self):
        self.write_checker(
            "import sys\n"
            "print('main=wrong manifests=108 pins=169 ok=85 mismatch=80 "
            "path_missing=0 incomplete=1 unbound=4')\n"
            f"print({EXPECTED_INCOMPLETE!r})\n"
            "sys.exit(2)\n"
        )
        result = self.run_assertion()
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected immutable evidence", result.stderr)

    def test_wrong_mismatch_count_is_a_violation(self):
        self.write_checker(
            "import sys\n"
            f"print({SUMMARY!r})\n"
            "print('MISMATCH only-one')\n"
            f"print({EXPECTED_INCOMPLETE!r})\n"
            "sys.exit(2)\n"
        )
        result = self.run_assertion()
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected immutable evidence", result.stderr)

    def test_path_missing_is_rejected_as_wrong_evidence(self):
        self.write_checker(
            "import sys\n"
            f"print({SUMMARY!r})\n"
            "print('PATH_MISSING fixture path=file declared=old')\n"
            f"print({EXPECTED_INCOMPLETE!r})\n"
            "sys.exit(2)\n"
        )
        result = self.run_assertion()
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected immutable evidence", result.stderr)

    def test_wrong_incomplete_source_is_rejected(self):
        self.write_checker(
            "import sys\n"
            f"print({SUMMARY!r})\n"
            "print('INCOMPLETE unrelated finding')\n"
            "sys.exit(2)\n"
        )
        result = self.run_assertion()
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected immutable evidence", result.stderr)

    def test_wrong_unbound_count_is_rejected(self):
        lines = [
            "import sys",
            f"print({SUMMARY!r})",
            f"print({EXPECTED_INCOMPLETE!r})",
        ]
        lines.extend(
            f"print('UNBOUND_BLOB_SHA256 manifest=m{i} pointer=/p/f field=f declared=d')"
            for i in range(3)
        )
        lines.append("sys.exit(2)")
        self.write_checker("\n".join(lines) + "\n")

        result = self.run_assertion()
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected immutable evidence", result.stderr)

    def test_wrong_commit_is_incomplete(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--commit",
                "0000000000000000000000000000000000000000",
                "--root",
                str(self.root),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("INCOMPLETE", result.stderr)


if __name__ == "__main__":
    unittest.main()
