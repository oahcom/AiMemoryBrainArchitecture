"""Structural checks for Unified COC/JF-10 schema artifact 1.2.17.

1.2.17 closes the owner-local gate release binding required by Storage §17.4.
It is a structural candidate only, not signature/semantic production proof.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.17.schema.json").read_text(encoding="utf-8")
)


def branch_for(message_type: str) -> dict:
    for branch in SCHEMA["oneOf"]:
        for clause in branch.get("allOf", []):
            if clause.get("properties", {}).get("message_type", {}).get("const") == message_type:
                return clause
    raise AssertionError(message_type)


class UnifiedManifest1217SchemaTests(unittest.TestCase):
    def test_01_artifact_revision_is_1_2_17_and_wire_family_remains_1_3_0(self):
        common = SCHEMA["$defs"]["commonEnvelope"]["properties"]
        self.assertEqual(SCHEMA["$id"].rsplit("/", 1)[-1], "1.2.17")
        self.assertEqual(common["schema_artifact_revision"]["const"], "1.2.17")
        self.assertEqual(common["schema_version"]["const"], "1.3.0")

    def test_02_owner_gate_release_binds_exact_owner_snapshot(self):
        release = branch_for("OWNER_LOCAL_GATE_RELEASE")
        required = set(release["required"])
        self.assertTrue({
            "owner_snapshot_ref", "owner_snapshot_digest",
            "owner_snapshot_attestation_ref", "owner_snapshot_attestation_digest",
            "owner_ledger_root",
        }.issubset(required))

    def test_03_owner_gate_release_binds_scope_and_anti_rollback(self):
        release = branch_for("OWNER_LOCAL_GATE_RELEASE")
        required = set(release["required"])
        self.assertTrue({
            "scope_generation_ref", "anti_rollback_anchor_ref",
            "owner_gate_ref", "owner_gate_generation",
        }.issubset(required))

    def test_04_owner_gate_release_binds_complete_owner_specific_currentness(self):
        release = branch_for("OWNER_LOCAL_GATE_RELEASE")
        required = set(release["required"])
        self.assertIn("owner_specific_high_waters", required)
        self.assertIn("owner_specific_high_waters_digest", required)
        refs = {x["$ref"] for x in release["properties"]["owner_specific_high_waters"]["oneOf"]}
        self.assertEqual(refs, {
            "#/$defs/ownerSpecificHighWatersI",
            "#/$defs/ownerSpecificHighWatersD",
            "#/$defs/ownerSpecificHighWatersC",
        })

    def test_05_release_still_binds_both_batch_and_manifest_records(self):
        release = branch_for("OWNER_LOCAL_GATE_RELEASE")
        required = set(release["required"])
        self.assertTrue({
            "batch_record_ref", "batch_position", "batch_entry_digest", "batch_digest",
            "manifest_record_ref", "manifest_record_position", "manifest_record_entry_digest",
            "manifest_content_digest", "reconciliation_root",
        }.issubset(required))

    def test_06_release_still_binds_both_request_and_admission_ledgers(self):
        release = branch_for("OWNER_LOCAL_GATE_RELEASE")
        required = set(release["required"])
        self.assertTrue({
            "owner_request_high_water", "owner_admission_high_water",
            "request_set_digest", "admission_set_digest",
            "request_ledger_root", "admission_ledger_root",
        }.issubset(required))

    def test_07_i_release_can_carry_permission_epoch(self):
        values = SCHEMA["$defs"]["ownerSpecificHighWatersI"]
        self.assertIn("permission_epoch", values["required"])
        self.assertIn("producer_domain_inventory_epoch_ref", values["required"])

    def test_08_d_release_can_carry_dependency_closure(self):
        values = SCHEMA["$defs"]["ownerSpecificHighWatersD"]
        self.assertIn("dependency_closure_cursor", values["required"])
        self.assertIn("dependency_closure_root", values["required"])

    def test_09_c_release_can_carry_provider_namespace_and_boundary_generation(self):
        values = SCHEMA["$defs"]["ownerSpecificHighWatersC"]
        self.assertIn("provider_idempotency_namespace_ref", values["required"])
        self.assertIn("final_request_boundary_generation", values["required"])

    def test_10_owner_release_requires_owner_signature_and_coc_commit_proof(self):
        required = set(branch_for("OWNER_LOCAL_GATE_RELEASE")["required"])
        self.assertTrue({"owner_signature_ref", "coc_commit_proof_ref", "coc_record_ref"}.issubset(required))

    def test_11_owner_release_branch_is_closed_world(self):
        branch = next(x for x in SCHEMA["oneOf"] if any(
            a.get("properties", {}).get("message_type", {}).get("const") == "OWNER_LOCAL_GATE_RELEASE"
            for a in x.get("allOf", [])
        ))
        self.assertFalse(branch.get("unevaluatedProperties", True))

    def test_12_schema_is_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(SCHEMA)


if __name__ == "__main__":
    unittest.main(verbosity=2)
