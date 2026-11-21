"""Dependency-free integrity checks for the checked-in BMCP schema candidates."""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RECOVERY_SCHEMA = ROOT / "schemas" / "bmcp.recovery-cutoff-1.0.4.schema.json"
JOIN_SCHEMA = ROOT / "schemas" / "bmcp.recovery-join-1.0.0.schema.json"
UNIFIED_SCHEMA = ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.8.schema.json"
JOIN_SCHEMA_101 = ROOT / "schemas" / "bmcp.recovery-join-1.0.1.schema.json"


class SchemaCandidateIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recovery = json.loads(RECOVERY_SCHEMA.read_text(encoding="utf-8"))
        cls.join = json.loads(JOIN_SCHEMA.read_text(encoding="utf-8"))
        cls.unified = json.loads(UNIFIED_SCHEMA.read_text(encoding="utf-8"))
        cls.join_101 = json.loads(JOIN_SCHEMA_101.read_text(encoding="utf-8"))

    def test_SCHEMA_01_recovery_schema_is_draft_2020_12_and_closed_root(self):
        self.assertEqual(self.recovery["$schema"], "https://json-schema.org/draft/2020-12/schema")
        for name in ("ownerSnapshot", "participantManifest", "recoveryBatch", "admissionEntry", "gateRelease", "epochCompleted"):
            self.assertFalse(self.recovery["$defs"][name].get("additionalProperties", True))

    def test_SCHEMA_02_recovery_schema_contains_six_message_families(self):
        refs = {x["$ref"].split("/")[-1] for x in self.recovery["oneOf"]}
        self.assertEqual(refs, {
            "ownerSnapshot", "participantManifest", "recoveryBatch",
            "admissionEntry", "gateRelease", "epochCompleted"
        })

    def test_SCHEMA_03_join_schema_requires_both_directional_edge_sets(self):
        required = set(self.join["required"])
        self.assertIn("owner_admission_to_participant", required)
        self.assertIn("participant_to_owner_evidence", required)
        self.assertIn("difference_sets", required)
        self.assertFalse(self.join.get("additionalProperties", True))

    def test_SCHEMA_04_join_schema_carries_jf10_identity_tuple(self):
        fields = set(self.join["$defs"]["jf10Join"]["required"])
        self.assertTrue({
            "prepared_participant_ref", "prepared_transaction_gid",
            "canonical_authority_db_ref", "database_incarnation_ref",
            "participant_ledger_ref", "participant_ledger_version",
            "i_terminal_state", "storage_terminal_state"
        }.issubset(fields))

    def test_SCHEMA_05_join_schema_does_not_collapse_owner_highwaters(self):
        owner = self.join["$defs"]["ownerSnapshot"]["properties"]
        self.assertIn("request_highwaters", owner)
        self.assertIn("admission_highwaters", owner)
        self.assertIn("gate_generation", owner)
        self.assertIn("anti_rollback_anchor_ref", owner)

    def test_SCHEMA_06_owner_request_and_admission_completeness_are_independent(self):
        props = self.join["$defs"]["ownerSnapshot"]["properties"]
        self.assertIn("request_enumeration_status", props)
        self.assertIn("admission_enumeration_status", props)
        required = set(self.join["$defs"]["ownerSnapshot"]["required"])
        self.assertTrue({"request_enumeration_status", "admission_enumeration_status"}.issubset(required))

    def test_SCHEMA_07_admission_join_carries_wire_position_reference_and_resolved_position(self):
        props = self.join["$defs"]["admissionJoin"]["properties"]
        self.assertIn("participant_position_ref", props)
        self.assertIn("participant_position", props)

    def test_SCHEMA_08_join_proof_covers_owner_request_ledger_rows(self):
        self.assertIn("owner_request_dispositions", self.join["required"])
        req = self.join["$defs"]["requestDisposition"]
        self.assertIn("owner_entry_ref", req["required"])
        self.assertIn("owner_request_digest", req["required"])

    def test_SCHEMA_09_join_edges_bind_admission_ref_and_ledger_row_ref(self):
        edge = self.join["$defs"]["admissionJoin"]
        self.assertIn("owner_admission_ref", edge["required"])
        self.assertIn("owner_entry_ref", edge["required"])
        participant = self.join["$defs"]["participantEvidenceJoin"]
        self.assertIn("primary_owner_entry_ref", participant["required"])

    def test_SCHEMA_10_request_disposition_binds_snapshot_row_digest(self):
        req = self.join["$defs"]["requestDisposition"]
        self.assertIn("owner_entry_digest", req["required"])
        self.assertIn("owner_request_digest", req["required"])

    def test_SCHEMA_11_typed_d_lineage_edge_requires_fence_and_manifest(self):
        oe = self.join["$defs"]["ownerEvidence"]
        self.assertIn("forget_operation_ref", oe["properties"])
        self.assertIn("fence_generation", oe["properties"])
        self.assertIn("lineage_manifest_ref", oe["properties"])
        self.assertIn("barrier_member_ref", oe["properties"])

    def test_SCHEMA_12_not_registered_disposition_binds_operation_and_scope(self):
        no = self.join["$defs"]["noParticipantDisposition"]
        self.assertTrue({"operation_identity_ref", "operation_digest", "scope_ref", "gate_generation", "scope_generation"}.issubset(set(no["required"])))

    def test_SCHEMA_13_unified_1_2_8_artifact_and_wire_versions_are_distinct(self):
        self.assertEqual(self.unified["$id"], "https://schemas.aimemorybrainarchitecture.invalid/bmcp.coc-jf10-unified/1.2.8")
        self.assertIn("1.2.8", self.unified["title"])
        common = self.unified["$defs"]["commonEnvelope"]
        self.assertIn("1.2.8", common["description"])
        self.assertEqual(common["properties"]["schema_version"]["const"], "1.2.0")

    def test_SCHEMA_14_signature_profile_id_is_explicit_but_compatibility_optional(self):
        common = self.unified["$defs"]["commonEnvelope"]
        self.assertIn("signature_profile_id", common["properties"])
        self.assertNotIn("signature_profile_id", common["required"])
        self.assertEqual(common["properties"]["digest_algorithm"]["const"], "SHA-256")

    def test_SCHEMA_15_owner_snapshot_attestation_is_content_bound(self):
        owner = self.unified["$defs"]["ownerSnapshot"]["properties"]
        self.assertIn("owner_snapshot_attestation_ref", owner)
        self.assertEqual(owner["owner_snapshot_attestation_digest"]["pattern"], "^[0-9a-f]{64}$")

    def test_SCHEMA_16_recovery_join_101_types_complete_empty_and_out_of_scope_proofs(self):
        self.assertEqual(self.join_101["$id"], "https://schemas.aimemorybrainarchitecture.invalid/bmcp.recovery-join/1.0.1")
        empty = self.join_101["$defs"]["completeEmptyProof"]
        out = self.join_101["$defs"]["outOfScopeProof"]
        self.assertFalse(empty.get("additionalProperties", True))
        self.assertFalse(out.get("additionalProperties", True))
        self.assertTrue({"ledger_query_ref", "owner_high_water", "pagination_complete", "count", "canonical_empty_root", "key_status_generation", "anti_rollback_anchor_ref", "signature_ref"}.issubset(set(empty["required"])))
        self.assertTrue({"request_ref", "operation_identity_ref", "scope_ref", "applicability_policy_ref", "decision", "owner_high_water", "ledger_query_ref", "key_status_generation", "anti_rollback_anchor_ref", "signature_ref"}.issubset(set(out["required"])))
        snap = self.join_101["$defs"]["ownerSnapshot"]["properties"]
        self.assertIn("request_pagination_complete", snap)
        self.assertIn("admission_pagination_complete", snap)
        self.assertIn("key_status_generation", snap)


if __name__ == "__main__":
    unittest.main(verbosity=2)
