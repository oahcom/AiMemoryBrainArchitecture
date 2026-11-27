import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parent
    / "resolve_manifest_blob_pin_base.py"
)


class ResolveManifestBlobPinBaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")

        (self.root / "file.txt").write_text("base\n", encoding="utf-8")
        self.git("add", "file.txt")
        self.git("commit", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD")

        self.git("checkout", "-qb", "feature")
        (self.root / "file.txt").write_text("feature\n", encoding="utf-8")
        self.git("commit", "-qam", "feature")
        self.head = self.git("rev-parse", "HEAD")

        self.git("checkout", "-q", "main")
        self.git("merge", "--no-ff", "-qm", "synthetic merge", "feature")
        self.merge = self.git("rev-parse", "HEAD")

        self.git("update-ref", "refs/pull/7/merge", self.merge)

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        return result.stdout.strip()

    def resolve(self, **overrides):
        env = os.environ.copy()
        env.update(
            {
                "GITHUB_EVENT_NAME": "pull_request",
                "GITHUB_SHA": self.merge,
                "GITHUB_REF": "refs/pull/7/merge",
                "GITHUB_EVENT_BEFORE": "0" * 40,
            }
        )
        env.update(overrides)
        return subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=self.root,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_pull_request_uses_merge_candidate_first_parent(self):
        result = self.resolve()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), self.base)

    def test_pull_request_ignores_stale_event_time_base(self):
        result = self.resolve(
            GITHUB_EVENT_PULL_REQUEST_BASE_SHA=self.head,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), self.base)
        self.assertNotEqual(result.stdout.strip(), self.head)

    def test_pull_request_rejects_non_merge_candidate(self):
        result = self.resolve(GITHUB_SHA=self.head)
        self.assertEqual(result.returncode, 2)
        self.assertIn("two-parent synthetic merge", result.stderr)

    def test_pull_request_requires_merge_ref_shape(self):
        result = self.resolve(GITHUB_REF="refs/heads/feature")
        self.assertEqual(result.returncode, 2)
        self.assertIn("GITHUB_REF", result.stderr)

    def test_push_uses_pre_push_tip(self):
        result = self.resolve(
            GITHUB_EVENT_NAME="push",
            GITHUB_EVENT_BEFORE=self.base,
            GITHUB_SHA=self.merge,
            GITHUB_REF="refs/heads/main",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), self.base)

    def test_push_rejects_zero_before_sha(self):
        result = self.resolve(
            GITHUB_EVENT_NAME="push",
            GITHUB_EVENT_BEFORE="0" * 40,
            GITHUB_REF="refs/heads/main",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("all-zero", result.stderr)

    def test_unknown_event_fails_closed(self):
        result = self.resolve(GITHUB_EVENT_NAME="workflow_dispatch")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported GitHub event", result.stderr)


if __name__ == "__main__":
    unittest.main()
