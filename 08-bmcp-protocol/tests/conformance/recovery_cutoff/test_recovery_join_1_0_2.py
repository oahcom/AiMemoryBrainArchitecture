"""RecoveryJoin 1.0.2 schema and D-binding conformance tests.

These tests validate structural constraints and deterministic local bindings only.
D signature/currentness authority is represented by injected test callbacks; no
D production key, ledger, or currentness service is available in this suite.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "validators"))

SCHEMA = json.loads(
    (ROOT / "schemas" / "bmcp.recovery-join-1.0.2.schema.json").read_text(encoding="utf-8")
)
from recovery_join_validator import (  # noqa: E402
    validate_d_producer_registration_binding,
    validate_d_fence_evidence_binding,
    validate_recovery_join,
)


def fragment_validator(name: str) -> Draft202012Validator:
    wrapper = {
        "$schema": SCHEMA["$schema"],
        "$defs": SCHEMA["$defs"],
        "$ref": f"#/$defs/{name}",
    }
    return Draft202012Validator(wrapper)


def owner_snapshot(owner: str = "D") -> dict:
    value = {
        "owner_authority_ref": f"{owner}/authority/1",
        "snapshot_ref": f"{owner}/snapshot/1",
        "snapshot_digest": "a" * 64,
        "request_count": 0,
        "request_root": "b" * 64,
        "request_highwaters": {"request": "0"},
        "admission_count": 0,
        "admission_root": "c" * 64,
        "admission_highwaters": {"admission": "0"},
        "gate_ref": f"{owner}/gate/1",
        "gate_generation": "2",
        "scope_generation": "3",
        "anti_rollback_anchor_ref": f"{owner}/anchor/1",
        "signature_ref": f"{owner}/snapshot-signature/1",
        "request_enumeration_status": "COMPLETE_EMPTY",
        "admission_enumeration_status": "COMPLETE_EMPTY",
    }
    if owner == "D":
        value.update({
            "producer_registration_sequence_namespace_ref": "D/producer-registration/namespace",
            "producer_registration_high_water": "5",
            "forget_fence_namespace_ref": "D/forget-fence/namespace",
            "forget_fence_generation_high_water": "4",
            "forget_fence_currentness_proof_ref": "D/fence-currentness-proof/1",
            "forget_fence_currentness_proof_digest": "d" * 64,
        })
    return value


def membership_proof() -> dict:
    d = "e" * 64
    return {
        "proof_ref": "D/membership-proof/1",
        "owner_kind": "D",
        "owner_authority_ref": "D/authority/1",
        "issuer_ref": "D/issuer/1",
        "subject_ref": "D/admission-entry/1",
        "audience_ref": "COC/recovery-validator",
        "purpose": "COC_RECOVERY_CUTOFF_MANIFEST_MEMBERSHIP",
        "owner_ledger_ref": "D/producer-registration-ledger/1",
        "owner_ledger_version": "v1",
        "owner_entry_ref": "D/admission-entry/1",
        "owner_entry_digest": d,
        "owner_admission_ref": "D/admission/1",
        "owner_sequence_namespace": "D/producer-registration/namespace",
        "owner_local_sequence": "4",
        "owner_high_water": "5",
        "owner_ledger_root": d,
        "owner_snapshot_ref": "D/snapshot/1",
        "owner_snapshot_digest": "a" * 64,
        "owner_snapshot_attestation_ref": "D/snapshot-attestation/1",
        "owner_snapshot_attestation_digest": d,
        "owner_gate_ref": "D/gate/1",
        "owner_gate_generation": "2",
        "scope_ref": "scope/1",
        "scope_generation": "3",
        "scope_binding_digest": d,
        "operation_identity_ref": "operation/1",
        "operation_digest": d,
        "request_digest": d,
        "anti_rollback_anchor_ref": "D/anchor/1",
        "key_status_generation": "D/key-status/1",
        "signature_profile_ref": "D/signature-profile/1",
        "key_id": "D/key/1",
        "key_version": "v1",
        "canonicalization_profile_ref": "profile/jcs",
        "digest_profile_ref": "profile/sha256",
        "proof_digest": d,
        "signature_ref": "D/signature/1",
        "producer_registration_sequence_namespace_ref": "D/producer-registration/namespace",
        "producer_registration_high_water": "5",
        "forget_fence_namespace_ref": "D/forget-fence/namespace",
        "forget_fence_generation_high_water": "4",
        "forget_fence_currentness_proof_ref": "D/fence-currentness-proof/1",
        "forget_fence_currentness_proof_digest": "d" * 64,
    }


def admission_row(proof: dict | None = None) -> dict:
    p = proof or membership_proof()
    return {
        "owner_kind": "D",
        "owner_admission_ref": p["owner_admission_ref"],
        "owner_entry_ref": p["owner_entry_ref"],
        "owner_admission_entry_digest": p["owner_entry_digest"],
        "owner_sequence_namespace": p["owner_sequence_namespace"],
        "owner_sequence": p["owner_local_sequence"],
        "gate_generation": p["owner_gate_generation"],
        "scope_ref": p["scope_ref"],
        "scope_generation": p["scope_generation"],
        "operation_identity_ref": p["operation_identity_ref"],
        "operation_digest": p["operation_digest"],
    }


def currentness_proof() -> dict:
    return {
        "proof_ref": "D/fence-currentness-proof/1",
        "proof_digest": "d" * 64,
        "owner_kind": "D",
        "forget_operation_ref": "D/forget-operation/1",
        "target_set_digest": "f" * 64,
        "forget_fence_namespace_ref": "D/forget-fence/namespace",
        "forget_fence_generation": "3",
        "forget_fence_generation_high_water": "4",
        "producer_registration_high_water": "5",
        "owner_snapshot_ref": "D/snapshot/1",
        "owner_snapshot_digest": "a" * 64,
        "owner_gate_generation": "2",
        "anti_rollback_anchor_ref": "D/anchor/1",
        "currentness_status": "CURRENT",
        "signature_ref": "D/fence-currentness-signature/1",
        "lineage_manifest_digest": "1" * 64,
    }


def forget_evidence() -> dict:
    return {
        "owner_kind": "D",
        "evidence_kind": "LINEAGE",
        "evidence_ref": "D/lineage-evidence/1",
        "evidence_digest": "2" * 64,
        "disposition": "PRESENT",
        "forget_operation_ref": "D/forget-operation/1",
        "fence_generation": "3",
        "lineage_manifest_ref": "D/lineage-manifest/1",
        "lineage_manifest_digest": "1" * 64,
        "barrier_member_ref": "D/barrier-member/1",
        "target_set_digest": "f" * 64,
        "forget_fence_namespace_ref": "D/forget-fence/namespace",
    }


class RecoveryJoin102ConformanceTests(unittest.TestCase):
    def test_01_schema_is_draft_2020_12_valid(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_02_root_schema_rejects_missing_required_envelope_members(self):
        self.assertTrue(list(Draft202012Validator(SCHEMA).iter_errors({})))

    def test_03_d_owner_snapshot_accepts_both_typed_watermarks_and_fence_binding(self):
        value = {"I": owner_snapshot("I"), "D": owner_snapshot("D"), "C": owner_snapshot("C")}
        fragment_validator("ownerSnapshots").validate(value)

    def test_04_d_owner_snapshot_requires_producer_registration_namespace(self):
        value = {"I": owner_snapshot("I"), "D": owner_snapshot("D"), "C": owner_snapshot("C")}
        value["D"].pop("producer_registration_sequence_namespace_ref")
        with self.assertRaises(ValidationError):
            fragment_validator("ownerSnapshots").validate(value)

    def test_05_d_owner_snapshot_requires_fence_currentness_reference_and_digest(self):
        value = {"I": owner_snapshot("I"), "D": owner_snapshot("D"), "C": owner_snapshot("C")}
        value["D"].pop("forget_fence_currentness_proof_digest")
        with self.assertRaises(ValidationError):
            fragment_validator("ownerSnapshots").validate(value)

    def test_06_d_membership_proof_accepts_typed_fields(self):
        fragment_validator("ownerSnapshotMembershipProof").validate(membership_proof())

    def test_07_d_membership_proof_requires_typed_producer_highwater(self):
        value = membership_proof()
        value.pop("producer_registration_high_water")
        with self.assertRaises(ValidationError):
            fragment_validator("ownerSnapshotMembershipProof").validate(value)

    def test_08_d_membership_proof_rejects_non_decimal_typed_highwater(self):
        value = membership_proof()
        value["producer_registration_high_water"] = "NOT_A_NUMBER"
        with self.assertRaises(ValidationError):
            fragment_validator("ownerSnapshotMembershipProof").validate(value)

    def test_09_currentness_proof_requires_all_fields_listed_in_contract(self):
        value = currentness_proof()
        value.pop("anti_rollback_anchor_ref")
        with self.assertRaises(ValidationError):
            fragment_validator("forgetFenceCurrentnessProof").validate(value)

    def test_10_currentness_proof_uses_contract_field_name_for_fence_generation(self):
        value = currentness_proof()
        self.assertIn("forget_fence_generation", value)
        self.assertNotIn("fence_generation", value)
        fragment_validator("forgetFenceCurrentnessProof").validate(value)

    def test_11_lineage_manifest_digest_is_admitted_but_not_required(self):
        value = currentness_proof()
        value.pop("lineage_manifest_digest")
        fragment_validator("forgetFenceCurrentnessProof").validate(value)

    def test_12_d_evidence_schema_admits_optional_target_set_and_fence_namespace(self):
        value = forget_evidence()
        value.pop("target_set_digest")
        value.pop("forget_fence_namespace_ref")
        fragment_validator("ownerEvidence").validate(value)

    def test_13_producer_binding_is_valid_only_with_d_authority_callback(self):
        result = validate_d_producer_registration_binding(
            membership_proof(), admission_row(), owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "VALID")

    def test_14_producer_binding_without_authority_callback_is_unknown(self):
        result = validate_d_producer_registration_binding(
            membership_proof(), admission_row(), owner_snapshot()
        )
        self.assertEqual(result["status"], "UNKNOWN")

    def test_15_producer_binding_rejects_generic_typed_highwater_mismatch(self):
        proof = membership_proof()
        proof["owner_high_water"] = "6"
        result = validate_d_producer_registration_binding(
            proof, admission_row(proof), owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "INVALID")

    def test_16_producer_binding_rejects_sequence_above_typed_highwater(self):
        proof = membership_proof()
        proof["owner_local_sequence"] = "6"
        row = admission_row(proof)
        result = validate_d_producer_registration_binding(proof, row, owner_snapshot(), lambda _: True)
        self.assertEqual(result["status"], "INVALID")

    def test_17_missing_d_snapshot_namespace_is_unknown_not_valid(self):
        snapshot = owner_snapshot()
        snapshot.pop("producer_registration_sequence_namespace_ref")
        result = validate_d_producer_registration_binding(
            membership_proof(), admission_row(), snapshot, lambda _: True
        )
        self.assertEqual(result["status"], "UNKNOWN")

    def test_18_fence_binding_requires_d_authoritative_currentness_callback(self):
        result = validate_d_fence_evidence_binding(forget_evidence(), currentness_proof(), owner_snapshot())
        self.assertEqual(result["status"], "UNKNOWN")

    def test_19_fence_binding_accepts_matching_current_proof_with_authority_callback(self):
        result = validate_d_fence_evidence_binding(
            forget_evidence(), currentness_proof(), owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "VALID")

    def test_20_fence_binding_rejects_generation_above_its_own_highwater(self):
        proof = currentness_proof()
        proof["forget_fence_generation"] = "5"
        result = validate_d_fence_evidence_binding(
            forget_evidence(), proof, owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "INVALID")

    def test_21_fence_binding_rejects_target_set_digest_mismatch(self):
        proof = currentness_proof()
        proof["target_set_digest"] = "9" * 64
        result = validate_d_fence_evidence_binding(
            forget_evidence(), proof, owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "INVALID")

    def test_22_stale_fence_is_invalid(self):
        proof = currentness_proof()
        proof["currentness_status"] = "STALE"
        result = validate_d_fence_evidence_binding(
            forget_evidence(), proof, owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "INVALID")

    def test_23_unknown_fence_currentness_remains_unknown(self):
        proof = currentness_proof()
        proof["currentness_status"] = "UNKNOWN"
        result = validate_d_fence_evidence_binding(
            forget_evidence(), proof, owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "UNKNOWN")

    def test_24_missing_should_level_fence_binding_remains_unknown(self):
        evidence = forget_evidence()
        evidence.pop("target_set_digest")
        result = validate_d_fence_evidence_binding(
            evidence, currentness_proof(), owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "UNKNOWN")

    def test_25_missing_lineage_digest_in_currentness_proof_remains_unknown(self):
        proof = currentness_proof()
        proof.pop("lineage_manifest_digest")
        result = validate_d_fence_evidence_binding(
            forget_evidence(), proof, owner_snapshot(), lambda _: True
        )
        self.assertEqual(result["status"], "UNKNOWN")

    def test_26_duplicate_json_members_are_rejected(self):
        result = validate_recovery_join(
            b'{"schema_id":"bmcp.recovery-join","schema_id":"attacker"}'
        )
        self.assertEqual(result["status"], "INVALID")
        self.assertIn("duplicate JSON object member", result["errors"][0])


if __name__ == "__main__":
    unittest.main()
