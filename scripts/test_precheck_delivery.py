#!/usr/bin/env python3
"""unittest coverage for scripts/precheck_delivery.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("precheck_delivery.py").resolve()


class PrecheckDeliveryTests(unittest.TestCase):
    def run_precheck(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root)],
            check=False,
            capture_output=True,
            text=True,
        )

    def make_repo(self, source: str) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(dir="/dev/shm")
        root = Path(temporary.name)
        rust_file = root / "crates" / "sample" / "src" / "lib.rs"
        rust_file.parent.mkdir(parents=True)
        rust_file.write_text(source, encoding="utf-8")
        return temporary, rust_file

    def test_trailing_tool_annotation_fails_and_reports_line(self) -> None:
        temporary, rust_file = self.make_repo(
            "pub fn healthy() {\n    let answer = 42;\n}\n"
            "[executed on device: X]\n"
        )
        with temporary:
            result = self.run_precheck(rust_file.parents[3])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(f"{rust_file}:4:", result.stdout)
            self.assertIn("[executed on device: X]", result.stdout)

    def test_clean_rust_file_passes(self) -> None:
        temporary, rust_file = self.make_repo(
            "pub fn healthy() {\n"
            '    let text = "{ not syntax }";\n'
            "    /* [ comment ] */\n"
            "}\n"
        )
        with temporary:
            result = self.run_precheck(rust_file.parents[3])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("precheck_delivery: OK", result.stdout)

    def test_unbalanced_delimiter_fails(self) -> None:
        temporary, rust_file = self.make_repo("pub fn unfinished() {\n")
        with temporary:
            result = self.run_precheck(rust_file.parents[3])
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn(f"{rust_file}: delimiter imbalance", result.stdout)
            self.assertIn("braces: +1", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
