#!/usr/bin/env python3
"""Self-check for scripts/check_source_revision_pointers.py.

Two defects are pinned here, both invisible from the exit code alone before
the fix:

  * a document with two `Source revision` records had every record compared
    against the first `Source:` link, so the second pointer was verified
    against -- and blamed on -- the first pointer's file;
  * a pointer whose value is not a 40-character blob (`main`, `HEAD`, a tag)
    was printed as NON_BLOB_REFERENCE and left out of BAD, so the scan exited
    0 while a pointer that resolves to nothing stayed live.

Fixtures are throwaway git repositories under the system temporary directory;
no network, no third-party packages.

    python3 scripts/test_check_source_revision_pointers.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_source_revision_pointers.py").resolve()

TRACKED = ("00-governance/a.md", "00-governance/b.md")


class SourceRevisionPointerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for directory in ("docs/en", "docs/zh-CN", "00-governance"):
            (self.root / directory).mkdir(parents=True)
        self.git("init", "-q")
        self.git("config", "user.email", "source-revision-test@example.invalid")
        self.git("config", "user.name", "Source Revision Test")
        for path in TRACKED:
            (self.root / path).write_text(f"{path}\n", encoding="utf-8")
        self.git("add", "--", *TRACKED)
        self.git("commit", "-qm", "seed")
        self.blob = {path: self.blob_of(path) for path in TRACKED}

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()

    def blob_of(self, path: str) -> str:
        return self.git("rev-parse", f"HEAD:{path}")

    def write_doc(self, rel: str, text: str) -> None:
        target = self.root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def scan(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def two_pointer_doc(self, first: str, second: str) -> str:
        return (
            "---\ntitle: two pointers\n---\n\n"
            f"- Source revision: {first}\n"
            "- Source: [a](../../00-governance/a.md)\n\n"
            f"- Source revision: {second}\n"
            "- Source: [b](../../00-governance/b.md)\n"
        )

    def test_each_pointer_is_compared_to_its_own_source(self) -> None:
        """The pinned defect: `links[0]` verified b's pointer against a's blob."""
        self.write_doc(
            "docs/en/two.md",
            self.two_pointer_doc(self.blob[TRACKED[0]], self.blob[TRACKED[1]]),
        )

        proc = self.scan()

        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("ACCURATE=2", proc.stdout)
        self.assertIn("STALE=0", proc.stdout)

    def test_a_wrong_second_pointer_is_blamed_on_its_own_source(self) -> None:
        wrong = "1" * 40
        self.write_doc(
            "docs/en/two.md",
            self.two_pointer_doc(self.blob[TRACKED[0]], wrong),
        )

        proc = self.scan()

        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("STALE=1", proc.stdout)
        stale = [line for line in proc.stdout.splitlines() if line.startswith("STALE ")]
        self.assertEqual(len(stale), 1, proc.stdout)
        self.assertIn("00-governance/b.md", stale[0])
        self.assertNotIn("00-governance/a.md", stale[0])

    def test_movable_reference_fails_the_scan(self) -> None:
        """`Source revision: main` resolves to nothing; it cannot pass silently."""
        self.write_doc(
            "docs/en/movable.md",
            "---\ntitle: movable\n---\n\n"
            "- Source revision: main\n"
            "- Source: [a](../../00-governance/a.md)\n",
        )

        proc = self.scan()

        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("NON_BLOB_REFERENCE=1", proc.stdout)
        self.assertIn("BAD=1", proc.stdout)
        self.assertIn("NON_BLOB_REFERENCE docs/en/movable.md", proc.stdout)

    def test_a_second_pointer_with_no_source_line_of_its_own_is_unresolved(self) -> None:
        self.write_doc(
            "docs/en/half.md",
            "---\ntitle: half\n---\n\n"
            f"- Source revision: {self.blob[TRACKED[0]]}\n"
            "- Source: [a](../../00-governance/a.md)\n\n"
            f"- Source revision: {self.blob[TRACKED[1]]}\n",
        )

        proc = self.scan()

        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("ACCURATE=1", proc.stdout)
        self.assertIn("UNRESOLVED=1", proc.stdout)
        unresolved = [
            line for line in proc.stdout.splitlines()
            if line.startswith("UNRESOLVED ")
        ]
        self.assertEqual(len(unresolved), 1, proc.stdout)
        self.assertIn("NO_SOURCE_LINK", unresolved[0])

    def test_both_language_trees_are_scanned(self) -> None:
        self.write_doc(
            "docs/zh-CN/two.md",
            self.two_pointer_doc(self.blob[TRACKED[0]], self.blob[TRACKED[1]]),
        )

        proc = self.scan()

        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("ACCURATE=2", proc.stdout)


if __name__ == "__main__":
    unittest.main()
