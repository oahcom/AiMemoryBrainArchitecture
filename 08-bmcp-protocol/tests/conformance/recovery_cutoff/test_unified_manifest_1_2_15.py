"""Structural conformance checks for Unified COC/JF-10 schema artifact 1.2.15.

These tests verify the exact schema's declared wire surface only. They do not
implement semantic signature verification, owner-ledger resolution, COC quorum
proof verification, or production canonicalization.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.15.schema.json").read_text(encoding="utf-8")
)


def message_branch(message_type: str) -> dict:
    for branch in SCHEMA["oneOf"]:
        for clause in branch.get("allOf", []):
            value = clause.get("properties", {}).get("message_type", {}).get("const")
            if value == message_type:
                return clause
    raise AssertionError(f"message type not found: {message_type}")


class UnifiedManifest1215SchemaTests(unittest.TestCase):
    def setUp(self):
        self.defs = SCHEMA["$defs"]
        self.common = self.defs["commonEnvelope"]

    def test_01_schema_artifact_revision_and_wire_version_are_distinct(self):
        self.assertEqual(self.common["properties"]["schema_artifact_revision"]["const"], "1.2.15")
        self.assertEqual(self.common["properties"]["schema_version"]["const"], "1.3.0")
        self.assertNotEqual(
            self.common["properties"]["schema_artifact_revision"]["const"],
            self.common["properties"]["schema_version"]["const"],
        )

    def test_02_exact_eleven_message_families_are_declared(self):
        expected = {
            "COC_RECOVERY_CUTOFF_BATCH",
            "PARTICIPANT_SET_RECONCILIATION",
            "OWNER_LOCAL_PENDING_GATE",
            "OWNER_LOCAL_GATE_RELEASE",
            "RECOVERY_EPOCH_COMPLETED",
            "JF10_PREPARE_INTENT_REGISTERED",
            "JF10_PREPARED_PARTICIPANT_REGISTERED",
            "JF10_I_TERMINAL_DECISION_OBSERVED",
            "JF10_STORAGE_PARTICIPANT_RESOLVED",
            "JF10_BRIDGE_RECONCILIATION_RECORDED",
            "C_PROVIDER_OUTCOME_RECORDED",
        }
        actual = {
            clause["properties"]["message_type"]["const"]
            for branch in SCHEMA["oneOf"]
            for clause in branch.get("allOf", [])
            if "message_type" in clause.get("properties", {})
        }
        self.assertEqual(actual, expected)

    def test_03_recovery_batch_binds_owner_snapshots_and_union_manifest(self):
        branch = message_branch("COC_RECOVERY_CUTOFF_BATCH")
        required = set(branch["required"])
        self.assertTrue({
            "owner_snapshots", "manifest_id", "manifest_content_digest",
            "coc_participant_count", "owner_local_admission_count",
            "manifest_member_count", "member_set_root",
        }.issubset(required))
        snapshots = branch["properties"]["owner_snapshots"]
        self.assertEqual(set(snapshots["required"]), {"I", "D", "C"})

    def test_04_manifest_member_array_is_typed_union_and_unique(self):
        branch = message_branch("PARTICIPANT_SET_RECONCILIATION")
        members = branch["properties"]["manifest_members"]
        self.assertEqual(members["type"], "array")
        self.assertTrue(members["uniqueItems"])
        refs = {item["$ref"] for item in members["items"]["oneOf"]}
        self.assertEqual(refs, {"#/$defs/cocParticipantMember", "#/$defs/ownerLocalAdmissionMember"})

    def test_05_coc_member_requires_explicit_owner_admission_bindings(self):
        member = self.defs["cocParticipantMember"]
        self.assertIn("COC_PARTICIPANT", member["properties"]["member_kind"]["const"])
        self.assertIn("owner_admission_bindings", member["required"])
        self.assertEqual(member["properties"]["owner_admission_bindings"]["type"], "array")
        self.assertTrue(member["properties"]["owner_admission_bindings"]["uniqueItems"])

    def test_06_unregistered_owner_admission_requires_explicit_null_and_reason(self):
        member = self.defs["ownerLocalAdmissionMember"]
        self.assertIn("OWNER_LOCAL_ADMISSION", member["properties"]["member_kind"]["const"])
        self.assertIn("coc_participant_intent_ref", member["required"])
        self.assertEqual(member["properties"]["coc_participant_intent_ref"]["type"], "null")
        self.assertIn("coc_absence_reason", member["required"])
        self.assertIn("owner_snapshot_membership_proof_ref", member["required"])
        self.assertIn("owner_snapshot_membership_proof_digest", member["required"])

    def test_07_owner_snapshot_separates_request_and_admission_ledgers(self):
        snap = self.defs["ownerSnapshot"]
        required = set(snap["required"])
        self.assertTrue({
            "request_high_water", "request_count", "request_set_digest", "request_ledger_root",
            "admission_high_water", "admission_count", "admission_set_digest", "admission_ledger_root",
            "owner_snapshot_attestation_digest", "owner_specific_high_waters_digest",
        }.issubset(required))
        self.assertNotEqual(
            snap["properties"]["request_high_water"],
            snap["properties"]["admission_high_water"],
        )

    def test_08_i_owner_specific_highwaters_are_complete(self):
        required = set(self.defs["ownerSpecificHighWatersI"]["required"])
        self.assertEqual(required, {
            "receipt_issue_high_water", "receipt_consume_high_water",
            "inventory_epoch_ref", "registry_snapshot_digest", "relevant_entry_set_root",
        })

    def test_09_d_owner_specific_highwaters_are_complete(self):
        required = set(self.defs["ownerSpecificHighWatersD"]["required"])
        self.assertEqual(required, {
            "producer_registration_high_water", "work_item_high_water",
            "attempt_high_water", "barrier_generation", "barrier_root",
            "forget_fence_generation_high_water",
        })

    def test_10_c_owner_specific_highwaters_are_complete(self):
        required = set(self.defs["ownerSpecificHighWatersC"]["required"])
        self.assertEqual(required, {
            "reservation_high_water", "provider_attempt_high_water", "provider_outcome_high_water",
        })

    def test_11_owner_snapshot_root_set_requires_i_d_c(self):
        roots = self.defs["ownerSnapshotRoots"]
        self.assertEqual(set(roots["required"]), {"I", "D", "C"})
        self.assertEqual(set(roots["properties"]), {"I", "D", "C"})

    def test_12_owner_admission_binding_is_snapshot_membership_proof_bound(self):
        binding = self.defs["ownerAdmissionBinding"]
        required = set(binding["required"])
        self.assertTrue({
            "owner_admission_ref", "owner_entry_ref", "owner_entry_digest",
            "owner_snapshot_ref", "owner_snapshot_digest",
            "owner_snapshot_attestation_ref", "owner_snapshot_attestation_digest",
            "owner_snapshot_membership_proof_ref", "owner_snapshot_membership_proof_digest",
        }.issubset(required))

    def test_13_recovery_epoch_completion_binds_exact_batch_manifest_pair(self):
        branch = message_branch("RECOVERY_EPOCH_COMPLETED")
        required = set(branch["required"])
        self.assertTrue({
            "batch_record_ref", "batch_digest", "batch_position", "batch_entry_digest",
            "manifest_record_ref", "manifest_record_position", "manifest_record_entry_digest",
            "manifest_content_digest", "owner_release_refs", "reconciliation_root",
            "quorum_commit_proof_ref",
        }.issubset(required))

    def test_14_c_provider_outcome_requires_final_request_boundary(self):
        branch = message_branch("C_PROVIDER_OUTCOME_RECORDED")
        required = set(branch["required"])
        self.assertTrue({
            "c_submit_outcome_ref", "c_submit_outcome_digest", "provider_outcome",
            "provider_idempotency_key_ref", "final_request_boundary_id", "request_digest",
            "provider_outcome_evidence_ref",
        }.issubset(required))

    def test_15_jf10_prepared_participant_binds_typed_gid_and_database_incarnation(self):
        branch = message_branch("JF10_PREPARED_PARTICIPANT_REGISTERED")
        required = set(branch["required"])
        self.assertTrue({
            "storage_prepared_participant_ref", "prepared_transaction_gid",
            "canonical_authority_db_ref", "database_incarnation_ref",
            "prepare_attempt_ref", "prepare_attempt_generation",
            "participant_ledger_ref", "participant_ledger_version",
            "publication_operation_id", "request_digest", "participant_tuple_digest",
            "prepared_participant_receipt_ref",
        }.issubset(required))
        self.assertNotIn("postgresql_native_xid", required)

    def test_16_common_envelope_declares_origin_and_signing_sequence_metadata(self):
        required = set(self.common["required"])
        properties = set(self.common["properties"])
        self.assertTrue({
            "schema_artifact_revision", "schema_version", "issuer_ref",
            "sender_authority_ref", "sender_subject_ref", "audience",
        }.issubset(required))
        self.assertTrue({
            "signing_sequence_namespace_ref", "signing_record_sequence",
            "origin_transport_context_ref", "origin_received_bytes_digest",
        }.issubset(properties))

    def test_17_every_message_branch_rejects_unevaluated_properties(self):
        for branch in SCHEMA["oneOf"]:
            self.assertFalse(branch.get("unevaluatedProperties", True))

    def test_18_schema_is_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(SCHEMA)


if __name__ == "__main__":
    unittest.main(verbosity=2)
