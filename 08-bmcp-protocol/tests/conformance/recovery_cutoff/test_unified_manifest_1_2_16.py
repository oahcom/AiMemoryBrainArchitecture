"""Structural checks for Unified COC/JF-10 schema artifact 1.2.16.

1.2.16 closes exact owner-snapshot/currentness fields required by Storage COC
§17. It remains a structural candidate, not semantic or production proof.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads(
    (ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.16.schema.json").read_text(encoding="utf-8")
)


class UnifiedManifest1216SchemaTests(unittest.TestCase):
    def setUp(self):
        self.defs = SCHEMA["$defs"]
        self.common = self.defs["commonEnvelope"]

    def test_01_artifact_revision_bumps_without_changing_wire_family(self):
        self.assertEqual(SCHEMA["$id"].rsplit("/", 1)[-1], "1.2.16")
        self.assertEqual(self.common["properties"]["schema_artifact_revision"]["const"], "1.2.16")
        self.assertEqual(self.common["properties"]["schema_version"]["const"], "1.3.0")

    def test_02_owner_snapshot_requires_distinct_scope_generation(self):
        snap = self.defs["ownerSnapshot"]
        root = self.defs["ownerSnapshotRoot"]
        self.assertIn("scope_generation_ref", snap["required"])
        self.assertIn("scope_generation_ref", snap["properties"])
        self.assertIn("scope_generation_ref", root["required"])
        self.assertIn("scope_generation_ref", root["properties"])
        self.assertNotEqual(
            snap["properties"]["scope_generation_ref"],
            snap["properties"]["owner_gate_generation"],
        )

    def test_03_i_snapshot_requires_permission_and_inventory_epochs(self):
        i = self.defs["ownerSpecificHighWatersI"]
        required = set(i["required"])
        self.assertTrue({
            "permission_epoch", "producer_domain_inventory_epoch_ref",
            "receipt_issue_high_water", "receipt_consume_high_water",
            "registry_snapshot_digest", "relevant_entry_set_root",
        }.issubset(required))
        self.assertNotIn("inventory_epoch_ref", i["properties"])
        self.assertEqual(i["properties"]["permission_epoch"]["type"], "string")

    def test_04_permission_epoch_is_opaque_i_local_value(self):
        prop = self.defs["ownerSpecificHighWatersI"]["properties"]["permission_epoch"]
        self.assertEqual(prop["type"], "string")
        self.assertIn("never numerically compared", prop["description"])

    def test_05_d_snapshot_requires_dependency_closure_cursor_and_root(self):
        d = self.defs["ownerSpecificHighWatersD"]
        self.assertTrue({
            "producer_registration_high_water", "work_item_high_water",
            "attempt_high_water", "barrier_generation", "barrier_root",
            "forget_fence_generation_high_water",
            "dependency_closure_cursor", "dependency_closure_root",
        }.issubset(set(d["required"])))

    def test_06_c_snapshot_requires_provider_namespace_and_boundary_generation(self):
        c = self.defs["ownerSpecificHighWatersC"]
        self.assertTrue({
            "reservation_high_water", "provider_attempt_high_water",
            "provider_outcome_high_water", "provider_idempotency_namespace_ref",
            "final_request_boundary_generation",
        }.issubset(set(c["required"])))

    def test_07_owner_snapshot_root_binds_scope_and_all_authority_highwaters(self):
        root = self.defs["ownerSnapshotRoot"]
        required = set(root["required"])
        self.assertTrue({
            "owner_snapshot_ref", "owner_snapshot_digest",
            "owner_snapshot_attestation_ref", "owner_snapshot_attestation_digest",
            "owner_gate_generation", "scope_generation_ref",
            "request_high_water", "admission_high_water",
            "request_ledger_root", "admission_ledger_root",
            "owner_specific_high_waters_digest",
        }.issubset(required))

    def test_08_owner_snapshot_still_separates_request_and_admission_ledgers(self):
        snap = self.defs["ownerSnapshot"]
        self.assertTrue({
            "request_high_water", "request_count", "request_set_digest", "request_ledger_root",
            "admission_high_water", "admission_count", "admission_set_digest", "admission_ledger_root",
        }.issubset(set(snap["required"])))

    def test_09_each_owner_highwater_shape_is_closed_world(self):
        for name in (
            "ownerSpecificHighWatersI",
            "ownerSpecificHighWatersD",
            "ownerSpecificHighWatersC",
        ):
            with self.subTest(owner_shape=name):
                self.assertFalse(self.defs[name].get("additionalProperties", True))

    def test_10_batch_and_manifest_union_contract_remains_present(self):
        message_types = {
            clause["properties"]["message_type"]["const"]
            for branch in SCHEMA["oneOf"]
            for clause in branch.get("allOf", [])
            if "message_type" in clause.get("properties", {})
        }
        self.assertIn("COC_RECOVERY_CUTOFF_BATCH", message_types)
        self.assertIn("PARTICIPANT_SET_RECONCILIATION", message_types)
        manifest = next(
            clause for branch in SCHEMA["oneOf"] for clause in branch.get("allOf", [])
            if clause.get("properties", {}).get("message_type", {}).get("const") == "PARTICIPANT_SET_RECONCILIATION"
        )
        refs = {x["$ref"] for x in manifest["properties"]["manifest_members"]["items"]["oneOf"]}
        self.assertEqual(refs, {"#/$defs/cocParticipantMember", "#/$defs/ownerLocalAdmissionMember"})

    def test_11_schema_is_valid_draft_2020_12(self):
        Draft202012Validator.check_schema(SCHEMA)



    def _owner_snapshot_fixture(self, owner):
        common = {
            "owner": owner,
            "owner_gate_ref": f"{owner}/gate/1",
            "owner_gate_generation": "1",
            "scope_generation_ref": f"{owner}/scope-generation/1",
            "request_high_water": "1",
            "request_count": 0,
            "request_set_digest": "a" * 64,
            "owner_snapshot_attestation_ref": f"{owner}/snapshot-attestation/1",
            "anti_rollback_anchor_ref": f"{owner}/anti-rollback/1",
            "owner_ledger_root": "b" * 64,
            "admission_high_water": "1",
            "admission_count": 0,
            "admission_set_digest": "c" * 64,
            "request_ledger_root": "d" * 64,
            "admission_ledger_root": "e" * 64,
            "owner_snapshot_attestation_digest": "f" * 64,
            "owner_specific_high_waters_digest": "0" * 64,
        }
        if owner == "I":
            common["owner_specific_high_waters"] = {
                "receipt_issue_high_water": "1",
                "receipt_consume_high_water": "1",
                "permission_epoch": "I/permission-epoch/1",
                "producer_domain_inventory_epoch_ref": "I/producer-domain-inventory/1",
                "registry_snapshot_digest": "1" * 64,
                "relevant_entry_set_root": "2" * 64,
            }
        elif owner == "D":
            common["owner_specific_high_waters"] = {
                "producer_registration_high_water": "1",
                "work_item_high_water": "1",
                "attempt_high_water": "1",
                "barrier_generation": "1",
                "barrier_root": "3" * 64,
                "forget_fence_generation_high_water": "1",
                "dependency_closure_cursor": "D/dependency-cursor/1",
                "dependency_closure_root": "4" * 64,
            }
        elif owner == "C":
            common["owner_specific_high_waters"] = {
                "reservation_high_water": "1",
                "provider_attempt_high_water": "1",
                "provider_outcome_high_water": "1",
                "provider_idempotency_namespace_ref": "C/provider-idempotency-namespace/1",
                "final_request_boundary_generation": "1",
            }
        return common

    def _owner_snapshot_validator(self):
        return Draft202012Validator({
            "$schema": SCHEMA["$schema"],
            "$defs": self.defs,
            "$ref": "#/$defs/ownerSnapshot",
        })

    def test_12_actual_i_d_c_owner_snapshot_instances_validate(self):
        validator = self._owner_snapshot_validator()
        for owner in ("I", "D", "C"):
            with self.subTest(owner=owner):
                validator.validate(self._owner_snapshot_fixture(owner))

    def test_13_i_snapshot_rejects_missing_producer_domain_inventory_epoch(self):
        snapshot = self._owner_snapshot_fixture("I")
        del snapshot["owner_specific_high_waters"]["producer_domain_inventory_epoch_ref"]
        with self.assertRaises(ValidationError):
            self._owner_snapshot_validator().validate(snapshot)

    def test_14_i_snapshot_rejects_legacy_inventory_epoch_alias(self):
        snapshot = self._owner_snapshot_fixture("I")
        snapshot["owner_specific_high_waters"]["inventory_epoch_ref"] = "I/legacy-epoch/1"
        with self.assertRaises(ValidationError):
            self._owner_snapshot_validator().validate(snapshot)

    def test_15_d_snapshot_rejects_missing_dependency_closure_root(self):
        snapshot = self._owner_snapshot_fixture("D")
        del snapshot["owner_specific_high_waters"]["dependency_closure_root"]
        with self.assertRaises(ValidationError):
            self._owner_snapshot_validator().validate(snapshot)

    def test_16_c_snapshot_rejects_missing_provider_idempotency_namespace(self):
        snapshot = self._owner_snapshot_fixture("C")
        del snapshot["owner_specific_high_waters"]["provider_idempotency_namespace_ref"]
        with self.assertRaises(ValidationError):
            self._owner_snapshot_validator().validate(snapshot)


if __name__ == "__main__":
    unittest.main(verbosity=2)
