"""Black-box tests for scripts/check_policy_inheritance.py.

Run:
    python3 -m unittest tests.test_policy_inheritance -v

Trust model: the checker pins the authoritative GOV-DOC-001 v1.1 source
identity (commit, path, blob) as production constants. The positive case runs
the checker against the real repository root and the committed declaration
`.governance/GOV-DOC-001-inheritance.json`. Negative cases tamper the
declaration only; `--repo` stays pointed at the real repository so field
rejection and object verification remain against the real Git object database.

Shallow-clone note: the CI checkout must provide the pinned source commit
object (c33a1bcd36f767c96f641d2a154f34d102ce2645) and its tree (full history,
or a fetch that includes it). Tests must never override the production pinned
values with test-only parameters.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "check_policy_inheritance.py"
DECLARATION = REPO_ROOT / ".governance" / "GOV-DOC-001-inheritance.json"


class PolicyInheritanceTests(unittest.TestCase):
    def run_checker(
        self,
        declaration_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--repo",
                str(REPO_ROOT),
                "--declaration",
                str(declaration_path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def tampered(self, **changes: str) -> Path:
        data = json.loads(DECLARATION.read_text(encoding="utf-8"))
        data.update(changes)
        handle = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            encoding="utf-8",
        )
        with handle as f:
            f.write(json.dumps(data, indent=2) + "\n")
        path = Path(handle.name)
        self.addCleanup(path.unlink)
        return path

    def test_real_source_commit_and_blob_pass(self) -> None:
        result = self.run_checker(DECLARATION)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Source Commit SHA: PASS", result.stdout)
        self.assertIn("Source Blob SHA: PASS", result.stdout)
        self.assertIn("Git object verification: PASS", result.stdout)
        self.assertIn("POLICY INHERITANCE: PASS", result.stdout)

    def test_wrong_version_fails(self) -> None:
        result = self.run_checker(self.tampered(inherited_version="1.2"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("inherited_version", result.stderr)
        self.assertIn("POLICY INHERITANCE: FAIL", result.stdout)

    def test_wrong_commit_fails(self) -> None:
        result = self.run_checker(self.tampered(source_commit="0" * 40))
        self.assertEqual(result.returncode, 1)
        self.assertIn("source_commit", result.stderr)

    def test_wrong_blob_fails(self) -> None:
        result = self.run_checker(self.tampered(policy_blob_sha="0" * 40))
        self.assertEqual(result.returncode, 1)
        self.assertIn("policy_blob_sha", result.stderr)

    def test_commit_sha_cannot_masquerade_as_blob_sha(self) -> None:
        data = json.loads(DECLARATION.read_text(encoding="utf-8"))
        result = self.run_checker(
            self.tampered(policy_blob_sha=data["source_commit"])
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("policy_blob_sha", result.stderr)

    def test_missing_declaration_fails(self) -> None:
        missing = (
            REPO_ROOT / ".governance" / "definitely-missing-declaration.json"
        )
        result = self.run_checker(missing)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing", result.stderr)


if __name__ == "__main__":
    unittest.main()
