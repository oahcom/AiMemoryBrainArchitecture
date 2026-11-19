
"""Black-box tests for scripts/check_policy_inheritance.py.

Run:
    python3 -m unittest tests.test_policy_inheritance -v

The tests use temporary Git repositories and real Git objects.
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


def git(cwd: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=cwd,
        text=True,
    ).strip()


class PolicyInheritanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "Policy Test")
        git(self.repo, "config", "user.email", "policy-test@example.invalid")

        policy = self.repo / "00-governance"
        policy.mkdir()
        (policy / "bilingual-documentation-policy.md").write_text(
            "# GOV-DOC-001\nVersion: 1.1\nStatus: NORMATIVE\n",
            encoding="utf-8",
        )

        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "baseline")
        self.commit_sha = git(self.repo, "rev-parse", "HEAD")
        self.blob_sha = git(
            self.repo,
            "rev-parse",
            "HEAD:00-governance/bilingual-documentation-policy.md",
        )

        declaration = {
            "policy_id": "GOV-DOC-001",
            "inherited_version": "1.1",
            "source_commit": self.commit_sha,
            "policy_blob_sha": self.blob_sha,
            "source_path": (
                "00-governance/bilingual-documentation-policy.md"
            ),
        }
        self.declaration = self.repo / ".governance" / (
            "GOV-DOC-001-inheritance.json"
        )
        self.declaration.parent.mkdir()
        self.write_declaration(declaration)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_declaration(self, value: dict) -> None:
        self.declaration.write_text(
            json.dumps(value, indent=2) + "\n",
            encoding="utf-8",
        )

    def run_checker(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--repo",
                str(self.repo),
                "--declaration",
                str(self.declaration),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_commit_and_blob_pass(self) -> None:
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Git object verification: PASS", result.stdout)
        self.assertIn("POLICY INHERITANCE: PASS", result.stdout)

    def test_wrong_version_fails(self) -> None:
        data = json.loads(self.declaration.read_text(encoding="utf-8"))
        data["inherited_version"] = "1.2"
        self.write_declaration(data)

        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("inherited_version", result.stderr)
        self.assertIn("POLICY INHERITANCE: FAIL", result.stdout)

    def test_wrong_commit_fails(self) -> None:
        data = json.loads(self.declaration.read_text(encoding="utf-8"))
        data["source_commit"] = "0" * 40
        self.write_declaration(data)

        result = self.run_checker()
        self.assertEqual(result.returncode, 1)

    def test_wrong_blob_fails(self) -> None:
        data = json.loads(self.declaration.read_text(encoding="utf-8"))
        data["policy_blob_sha"] = "0" * 40
        self.write_declaration(data)

        result = self.run_checker()
        self.assertEqual(result.returncode, 1)

    def test_commit_sha_cannot_masquerade_as_blob_sha(self) -> None:
        data = json.loads(self.declaration.read_text(encoding="utf-8"))
        data["policy_blob_sha"] = data["source_commit"]
        self.write_declaration(data)

        result = self.run_checker()
        self.assertEqual(result.returncode, 1)

    def test_missing_declaration_fails(self) -> None:
        self.declaration.unlink()
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
