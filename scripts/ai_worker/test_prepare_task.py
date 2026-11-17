import json
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).with_name("prepare_task.py")
SPEC = importlib.util.spec_from_file_location("prepare_task", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class PrepareTaskTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.issue = {
            "number": 42,
            "title": "Bilingual docs correction",
            "html_url": "https://github.com/oahcom/AiMemoryBrainArchitecture/issues/42",
            "state": "open",
            "labels": [
                {"name": "ai:ready"}, {"name": "owner:a"},
                {"name": "risk:r0"}, {"name": "work:doc"}
            ],
            "body": "## Objective\nClarify docs.\n## Acceptance Criteria\nBilingual.\n## Non-goals\nNo code."
        }

    def invoke(self, issue):
        src = self.root / "issue.json"
        dst = self.root / "out" / "task.json"
        src.write_text(json.dumps(issue), encoding="utf-8")
        # Run as a subprocess to exercise the command-line contract.
        import subprocess, sys
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(src), str(dst)],
            capture_output=True, text=True
        ), dst

    def test_accepts_exactly_one_owner_risk_and_work_class(self):
        result, dst = self.invoke(self.issue)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(dst.read_text(encoding="utf-8"))
        self.assertEqual(data["owner"], "A")
        self.assertEqual(data["risk"], "R0")
        self.assertEqual(data["work_class"], "DOC")

    def test_rejects_unlabeled_issue(self):
        issue = dict(self.issue)
        issue["labels"] = [{"name": "owner:a"}, {"name": "risk:r0"}, {"name": "work:doc"}]
        result, _ = self.invoke(issue)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ai:ready", result.stderr)

    def test_rejects_multiple_owners(self):
        issue = dict(self.issue)
        issue["labels"] = self.issue["labels"] + [{"name": "owner:b"}]
        result, _ = self.invoke(issue)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly one owner", result.stderr)

    def test_rejects_risk_above_pilot_limit(self):
        issue = dict(self.issue)
        issue["labels"] = [x for x in self.issue["labels"] if not x["name"].startswith("risk:")]
        issue["labels"].append({"name": "risk:r2"})
        result, _ = self.invoke(issue)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("risk:R0 or risk:R1", result.stderr)

    def test_rejects_pull_request(self):
        issue = dict(self.issue)
        issue["pull_request"] = {"url": "https://api.github.com/pulls/42"}
        result, _ = self.invoke(issue)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pull requests", result.stderr)

    def test_rejects_missing_acceptance_headings(self):
        issue = dict(self.issue)
        issue["body"] = "## Objective\nDo work."
        result, _ = self.invoke(issue)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Acceptance Criteria", result.stderr)

if __name__ == "__main__":
    unittest.main()
