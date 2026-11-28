#!/usr/bin/env python3
"""Behavioural tests for the one-time broken-base exception in the hygiene gate.

The guard lives inside a workflow shell step, so the test extracts that exact
block from `.github/workflows/repository-hygiene.yml` and runs it under bash
with each status combination. Nothing here re-implements the conditions: if the
workflow drifts, the extraction fails and these tests fail with it.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "repository-hygiene.yml"

KNOWN_BROKEN_BASE = "f0843a8f38a420883921cfda96b515204967f885"
OTHER_BASE = "0" * 40
WARNING = "WARNING: allowing known broken base"

BASH_CANDIDATES = (
    os.environ.get("BASH_BIN", ""),
    r"C:\Program Files\Git\bin\bash.exe",
    "/usr/bin/bash",
    "/bin/bash",
)


def find_bash() -> str | None:
    for candidate in BASH_CANDIDATES:
        if candidate and Path(candidate).exists():
            return candidate
    return shutil.which("bash")


def extract_guard() -> str:
    """Return the guard block, from KNOWN_BROKEN_BASE_SHA to the warning's fi."""
    lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
    start = next(
        index for index, line in enumerate(lines)
        if "KNOWN_BROKEN_BASE_SHA=" in line
    )
    warning = next(
        index for index, line in enumerate(lines)
        if WARNING in line and "echo" in line
    )
    end = next(
        index for index in range(warning, len(lines))
        if lines[index].strip() == "fi"
    )
    block = [line[10:] if line.startswith(" " * 10) else line
             for line in lines[start:end + 1]]
    return "\n".join(block) + "\n"


class BaseExceptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bash = find_bash()
        cls.guard = extract_guard()

    def run_guard(self, base_sha: str, base: int, negative: int, candidate: int) -> subprocess.CompletedProcess:
        if not self.bash:
            self.skipTest("bash is not available on this host")
        script = (
            "set -u\n"
            f'BASE_SHA="{base_sha}"\n'
            f"base_status={base}\n"
            f"negative_status={negative}\n"
            f"candidate_status={candidate}\n"
            + self.guard
            + 'echo "REACHED_END"\n'
        )
        with tempfile.TemporaryDirectory(prefix="hygiene-guard-") as tmp:
            path = Path(tmp) / "guard.sh"
            path.write_text(script, encoding="utf-8", newline="\n")
            return subprocess.run(
                [self.bash, str(path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )

    def test_known_broken_base_may_bootstrap(self) -> None:
        result = self.run_guard(KNOWN_BROKEN_BASE, 2, 0, 0)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn(WARNING, result.stdout)
        self.assertIn("REACHED_END", result.stdout)

    def test_other_base_incomplete_still_fails(self) -> None:
        result = self.run_guard(OTHER_BASE, 2, 0, 0)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("INCOMPLETE: base scan could not be completed", result.stdout)
        self.assertNotIn("REACHED_END", result.stdout)

    def test_known_base_with_incomplete_candidate_fails(self) -> None:
        result = self.run_guard(KNOWN_BROKEN_BASE, 2, 0, 2)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("INCOMPLETE: negative sample or candidate scan", result.stdout)
        self.assertNotIn("REACHED_END", result.stdout)

    def test_known_base_with_incomplete_negative_sample_fails(self) -> None:
        result = self.run_guard(KNOWN_BROKEN_BASE, 2, 2, 0)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("INCOMPLETE: negative sample or candidate scan", result.stdout)
        self.assertNotIn("REACHED_END", result.stdout)

    def test_known_base_with_clean_base_passes_silently(self) -> None:
        result = self.run_guard(KNOWN_BROKEN_BASE, 0, 0, 0)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn(WARNING, result.stdout)
        self.assertIn("REACHED_END", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
