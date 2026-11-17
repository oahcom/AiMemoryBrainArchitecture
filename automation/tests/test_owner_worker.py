import unittest
from owner_worker import safe_path, validate_files, WorkerError

class BoundaryTests(unittest.TestCase):
    def test_allowlist(self):
        self.assertTrue(safe_path("automation/owner-output/a.md"))
        self.assertFalse(safe_path(".github/workflows/a.yml"))
        self.assertFalse(safe_path("src/main.rs"))
    def test_traversal(self):
        self.assertFalse(safe_path("automation/owner-output/../x.md"))
        self.assertFalse(safe_path("automation/owner-output/a/../../x"))
    def test_duplicate(self):
        with self.assertRaises(WorkerError):
            validate_files([{"path":"automation/owner-output/a.md","content":"a"},{"path":"automation/owner-output/a.md","content":"b"}])
    def test_size_limit(self):
        with self.assertRaises(WorkerError):
            validate_files([{"path":"automation/owner-output/a.md","content":"x"*24001}])
    def test_exact_schema(self):
        with self.assertRaises(WorkerError):
            validate_files([{"path":"automation/owner-output/a.md","content":"ok","mode":"100755"}])

if __name__=="__main__": unittest.main()
