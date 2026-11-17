"""Dependency-free integrity checks for the checked-in BMCP schema candidates."""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RECOVERY_SCHEMA = ROOT / "schemas" / "bmcp.recovery-cutoff-1.0.4.schema.json"
JOIN_SCHEMA = ROOT / "schemas" / "bmcp.recovery-join-1.0.0.schema.json"


class SchemaCandidateIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recovery = json.loads(RECOVERY_SCHEMA.read_text(encoding="utf-8"))
        cls.join = json.loads(JOIN_SCHEMA.read_text(encoding="utf-8"))

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
