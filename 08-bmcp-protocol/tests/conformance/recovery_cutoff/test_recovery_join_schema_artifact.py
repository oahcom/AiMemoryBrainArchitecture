"""Executable artifact checks for the RecoveryJoin 1.0.2 JSON Schema.

Run from the repository root:
    python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance/recovery_cutoff -p 'test_recovery_join*.py' -v

The unittest runner prints the collected test count and pass/fail summary.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "schemas" / "bmcp.recovery-join-1.0.2.schema.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)


def fragment_validator(name: str) -> Draft202012Validator:
    return Draft202012Validator({
        "$schema": SCHEMA["$schema"],
        "$defs": SCHEMA["$defs"],
        "$ref": f"#/$defs/{name}",
    })


class RecoveryJoinSchemaArtifactTests(unittest.TestCase):
    def test_01_schema_identity_and_index_are_consistent(self):
        self.assertEqual(SCHEMA_PATH.name, "bmcp.recovery-join-1.0.2.schema.json")
        match = re.search(r"-(\\d+\\.\\d+\\.\\d+)\\.schema\\.json$", SCHEMA_PATH.name)
        self.assertIsNotNone(match, "schema filename must end in a semantic version")
        filename_version = match.group(1)
        id_match = re.search(r"/(\\d+\\.\\d+\\.\\d+)$", SCHEMA["$id"])
        self.assertIsNotNone(id_match, "$id must end in a semantic version")
        self.assertEqual(id_match.group(1), filename_version)
        self.assertEqual(SCHEMA["properties"]["schema_version"]["const"], filename_version)
        message_type = SCHEMA["properties"]["message_type"]["const"]
        self.assertEqual(message_type, "RECOVERY_JOIN_PROOF")

        index = (ROOT / "protocol-index.md").read_text(encoding="utf-8")
        row = next((line for line in index.splitlines() if "| `RECOVERY_JOIN_PROOF` |" in line), None)
        self.assertIsNotNone(row, "protocol index must use the schema's exact message_type")
        self.assertIn("schemas/bmcp.recovery-join-1.0.2.schema.json", row)
        self.assertIn("tests/conformance/recovery_cutoff/test_recovery_join_schema_artifact.py", row)

    def test_02_valid_full_message_fixture_is_accepted(self):
        instance = json.loads((FIXTURES / "valid_recovery_join_1_0_2.json").read_text(encoding="utf-8"))
        errors = list(VALIDATOR.iter_errors(instance))
        self.assertEqual(errors, [], "\\n".join(error.message for error in errors))

    def test_03_invalid_forget_fence_generation_fixture_is_rejected(self):
        instance = json.loads((FIXTURES / "invalid_forget_fence_generation.json").read_text(encoding="utf-8"))
        self.assertTrue(list(fragment_validator("forgetFenceGeneration").iter_errors(instance)))

    def test_04_invalid_owner_snapshot_membership_proof_fixture_is_rejected(self):
        instance = json.loads((FIXTURES / "invalid_owner_snapshot_membership_proof.json").read_text(encoding="utf-8"))
        self.assertTrue(list(fragment_validator("ownerSnapshotMembershipProof").iter_errors(instance)))

    def test_05_invalid_complete_empty_proof_fixture_is_rejected(self):
        instance = json.loads((FIXTURES / "invalid_complete_empty_proof.json").read_text(encoding="utf-8"))
        self.assertTrue(list(fragment_validator("completeEmptyProof").iter_errors(instance)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
