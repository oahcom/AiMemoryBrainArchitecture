#!/usr/bin/env python3
"""Tests for the work-item claim registry validator."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_work_item_registry.py")
HEAD = "b" * 40
MERGE = "c" * 40


def claim(work_item_id="AID-2026-279", status="CLAIMED", pull_request=1, **overrides):
    row = {
        "work_item_id": work_item_id,
        "status": status,
        "pull_request": pull_request,
        "repository": "example/repo",
        "head_sha": HEAD,
        "merge_commit_sha": MERGE if status == "MERGED" else None,
        "claimed_at": "2026-11-27T00:00:00Z",
        "updated_at": "2026-11-27T00:10:00Z",
        "owner_work_item": work_item_id,
        "evidence": [f"{work_item_id}/manifest.yaml"],
    }
    row.update(overrides)
    return row


def render(claims, schema_version=1):
    if not claims:
        return f"schema_version: {schema_version}\nclaims: []\n"
    lines = [f"schema_version: {schema_version}", "claims:"]
    for row in claims:
        first = True
        for key, value in row.items():
            prefix = "  - " if first else "    "
            first = False
            if value is None:
                lines.append(f"{prefix}{key}: null")
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                lines.extend(f"      - \"{item}\"" for item in value)
            elif isinstance(value, str):
                lines.append(f'{prefix}{key}: "{value}"')
            else:
                lines.append(f"{prefix}{key}: {value}")
    return "\n".join(lines) + "\n"


def invoke(*args, env=None):
    command = [sys.executable, str(SCRIPT), *args]
    print("$ " + " ".join(command), flush=True)
    result = subprocess.run(
        command, capture_output=True, text=True, encoding="utf-8",
        errors="replace", env=env,
    )
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return result


class RegistryValidatorTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.root = Path(self._temp.name)

    def tearDown(self):
        self._temp.cleanup()

    def ledger(self, name, text):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_valid_claimed_ledger_passes(self):
        path = self.ledger("claims.yaml", render([claim()]))
        result = invoke("--registry", path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WORK-ITEM REGISTRY: PASS", result.stdout)

    def test_valid_merged_ledger_passes(self):
        path = self.ledger("claims.yaml", render([claim(status="MERGED")]))
        result = invoke("--registry", path)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unknown_status_is_a_violation(self):
        path = self.ledger("claims.yaml", render([claim(status="OPEN")]))
        result = invoke("--registry", path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("status must be one of", result.stdout)

    def test_merged_without_merge_commit_sha_is_a_violation(self):
        path = self.ledger(
            "claims.yaml",
            render([claim(status="MERGED", merge_commit_sha=None)]),
        )
        result = invoke("--registry", path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("merge_commit_sha is required", result.stdout)

    def test_missing_field_is_a_violation(self):
        row = claim()
        row.pop("evidence")
        path = self.ledger("claims.yaml", render([row]))
        result = invoke("--registry", path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("is missing evidence", result.stdout)

    def test_two_pull_requests_claiming_one_id_are_a_violation(self):
        path = self.ledger(
            "claims.yaml",
            render([claim(pull_request=1), claim(pull_request=2)]),
        )
        result = invoke("--registry", path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("is CLAIMED by more than one pull request", result.stdout)

    def test_merged_id_cannot_be_reclaimed(self):
        merged = claim(status="MERGED", pull_request=1)
        merged["updated_at"] = "2026-11-27T01:00:00Z"
        later = claim(pull_request=2)
        later["claimed_at"] = "2026-11-27T02:00:00Z"
        later["updated_at"] = "2026-11-27T02:10:00Z"
        path = self.ledger("claims.yaml", render([merged, later]))
        result = invoke("--registry", path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("may not be re-claimed", result.stdout)

    def test_claimed_to_merged_transition_passes(self):
        before = self.ledger("before.yaml", render([claim()]))
        after = self.ledger("after.yaml", render([claim(status="MERGED")]))
        result = invoke("--registry", after, "--previous", before)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_claimed_to_abandoned_transition_passes(self):
        before = self.ledger("before.yaml", render([claim()]))
        after = self.ledger("after.yaml", render([claim(status="ABANDONED")]))
        result = invoke("--registry", after, "--previous", before)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_merged_is_terminal(self):
        before = self.ledger("before.yaml", render([claim(status="MERGED")]))
        after = self.ledger("after.yaml", render([claim(status="ABANDONED")]))
        result = invoke("--registry", after, "--previous", before)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("was MERGED and cannot move", result.stdout)

    def test_claim_may_not_be_deleted(self):
        before = self.ledger("before.yaml", render([claim()]))
        after = self.ledger("after.yaml", render([]))
        result = invoke("--registry", after, "--previous", before)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("claims are never deleted", result.stdout)

    def test_new_row_must_start_claimed(self):
        before = self.ledger("before.yaml", render([]))
        after = self.ledger("after.yaml", render([claim(status="MERGED")]))
        result = invoke("--registry", after, "--previous", before)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("new rows must start CLAIMED", result.stdout)

    def test_missing_registry_is_incomplete(self):
        result = invoke("--registry", str(self.root / "absent.yaml"))
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("INCOMPLETE", result.stdout)

    def test_live_check_without_token_is_incomplete(self):
        path = self.ledger("claims.yaml", render([claim()]))
        env = {key: value for key, value in os.environ.items()
               if key not in ("GITHUB_TOKEN", "GH_TOKEN")}
        result = invoke("--registry", path, "--check-live-prs", env=env)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("INCOMPLETE", result.stdout)

    def test_schema_version_must_be_one(self):
        path = self.ledger("claims.yaml", render([claim()], schema_version=2))
        result = invoke("--registry", path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("schema_version must be the integer 1", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
