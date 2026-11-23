#!/usr/bin/env python3
"""Regression tests for the hosted-only GitHub Actions runner policy."""

import tempfile
import unittest
from pathlib import Path

from audit_runner_admission import audit_workflow


class HostedRunnerPolicyTests(unittest.TestCase):
    def audit(self, workflow: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "workflow.yml"
            path.write_text(workflow, encoding="utf-8")
            return audit_workflow(path)

    def test_accepts_github_hosted_ubuntu_runner(self):
        count, violations = self.audit("""name: test
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo ok
""")
        self.assertEqual(count, 1)
        self.assertEqual(violations, [])

    def test_rejects_self_hosted_runner(self):
        count, violations = self.audit("""name: test
on: push
jobs:
  test:
    runs-on: [self-hosted, linux, x64]
    steps:
      - run: echo no
""")
        self.assertEqual(count, 1)
        self.assertEqual(len(violations), 1)
        self.assertIn("ubuntu-latest", violations[0])

    def test_rejects_dynamic_runner(self):
        count, violations = self.audit("""name: test
on: push
jobs:
  test:
    runs-on: ${{ matrix.runner }}
    steps:
      - run: echo no
""")
        self.assertEqual(count, 1)
        self.assertEqual(len(violations), 1)
        self.assertIn("matrix.runner", violations[0])

    def test_rejects_block_list_with_self_hosted_label(self):
        count, violations = self.audit("""name: test
on: push
jobs:
  test:
    runs-on:
      - self-hosted
      - linux
    steps:
      - run: echo no
""")
        self.assertEqual(count, 1)
        self.assertEqual(len(violations), 1)

    def test_checks_every_job(self):
        count, violations = self.audit("""name: test
on: push
jobs:
  hosted:
    runs-on: ubuntu-latest
  local:
    runs-on: [self-hosted, linux]
""")
        self.assertEqual(count, 2)
        self.assertEqual(len(violations), 1)


if __name__ == "__main__":
    unittest.main()
