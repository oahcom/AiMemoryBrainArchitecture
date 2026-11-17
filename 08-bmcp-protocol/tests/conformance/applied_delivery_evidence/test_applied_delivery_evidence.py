import copy
import hashlib
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads((ROOT / "schemas" / "bmcp.applied-delivery-evidence-1.0.0.schema.json").read_text())
from applied_delivery_evidence_validator import (  # noqa: E402
    AppliedDeliveryChecks, DurableObservationDecision, P0_EXCLUDED,
    build_h_p0, canonical_p0_bytes, delivery_binding_identity,
    observation_identity, validate_applied_delivery_evidence,
)


def fixture():
    value = {
        "schema_artifact_revision":"1.0.0","message_type":"APPLIED_DELIVERY_EVIDENCE_RECORDED",
        "issuer_ref":"H/issuer/1","sender_authority_ref":"H/adapter-authority/1","sender_subject_ref":"H/adapter-instance/1",
        "audience":"G/applied-evidence-validator","message_id":"H/message/1","message_nonce":"nonce-1",
        "signing_sequence_namespace_ref":"H/sequence/1","signing_record_sequence":"1",
        "signature_profile_id":"TEST-ONLY","key_id_ref":"H/key/1","key_version":"test-key-v1",
        "adapter_instance_ref":"H/adapter-instance/1","runtime_session_ref":"R/session/1",
        "delivery_id":"G/delivery/1","delivery_attempt_id":"G/delivery-attempt/1",
        "inference_request_id":"R/request/1","final_request_boundary_id":"C/boundary/1",
        "adapter_capability_epoch":"H/capability-epoch/1","evidence_kind":"FINAL_REQUEST_SUBMITTED","evidence_tier":"TIER_1",
        "adapter_ref":"H/adapter/1","runtime_instance_ref":"R/runtime/1","context_id":"G/context/1",
        "context_version":"G/context-version/7","materialized_context_version":"G/context-version/7",
        "final_request_boundary_type":"RUNTIME_FINAL_SUBMIT_HOOK","managed_region_id":"G/managed-region/1",
        "managed_region_revision":"rev-7","managed_region_inventory_digest":"a"*64,
        "managed_region_coverage":"COMPLETE","managed_region_digest":"b"*64,"digest_profile":"TEST-ONLY-SHA256",
        "evidence_issuer_ref":"H/adapter-evidence/issuer","evidence_schema_version":"1.0.0",
        "submission_observed_at":"2026-11-18T00:00:00Z","submission_monotonic_sequence":"9",
        "correlation_ref":"G/delivery/1","causation_ref":"C/boundary/1","audit_ref":"H/audit/1",
        "c_submit_outcome_ref":"C/submit-outcome/1","c_outcome_record_ref":"C/outcome-record/1",
        "c_outcome_record_sequence":"17","c_outcome_payload_digest":"c"*64,
        "payload_digest":"0"*64,"signature":"TEST-SIGNATURE","integrity_proof_ref":"H/integrity/1"
    }
    value["payload_digest"] = hashlib.sha256(canonical_p0_bytes(value)).hexdigest()
    return value


def checks(disposition="NEW"):
    return AppliedDeliveryChecks(
        verify_profile_registration=lambda e: True, verify_key_status=lambda e: True,
        verify_signature=lambda e,p: True, verify_protected_identity_binding=lambda e: True,
        verify_c_final_boundary=lambda e: True, verify_g_delivery_binding=lambda e: True,
        verify_capability_epoch=lambda e: True,
        commit_observation=lambda e,d: DurableObservationDecision(disposition, "H/result/1" if disposition=="SAME_DIGEST_REPLAY" else None)
    )


class AppliedDeliveryEvidenceTests(unittest.TestCase):
    def validate(self, value, callbacks=None):
        raw=json.dumps(value,separators=(",",":"),sort_keys=True).encode()
        return validate_applied_delivery_evidence(raw, SCHEMA, callbacks or checks())

    def test_01_schema_and_positive_tier1(self):
        value=fixture()
        Draft202012Validator(SCHEMA).validate(value)
        self.assertEqual(self.validate(value)["status"],"VALID_NEW")

    def test_02_unknown_member_rejected(self):
        value=fixture(); value["unregistered_field"]="x"
        self.assertEqual(self.validate(value)["status"],"INVALID")

    def test_03_each_delivery_identity_field_required(self):
        for field in ("adapter_instance_ref","runtime_session_ref","delivery_id","delivery_attempt_id","inference_request_id","final_request_boundary_id","adapter_capability_epoch"):
            value=fixture(); value.pop(field)
            with self.subTest(field=field): self.assertEqual(self.validate(value)["status"],"INVALID")

    def test_04_tier1_requires_complete_coverage(self):
        value=fixture(); value["managed_region_coverage"]="PARTIAL"
        value["payload_digest"]=hashlib.sha256(canonical_p0_bytes(value)).hexdigest()
        self.assertEqual(self.validate(value)["status"],"INVALID")

    def test_05_tier1_requires_exact_materialized_context_version(self):
        value=fixture(); value["materialized_context_version"]="G/context-version/6"
        value["payload_digest"]=hashlib.sha256(canonical_p0_bytes(value)).hexdigest()
        self.assertEqual(self.validate(value)["status"],"INVALID")

    def test_06_digest_mutation_rejected(self):
        value=fixture(); value["delivery_attempt_id"]="G/attempt/attacker"
        self.assertEqual(self.validate(value)["status"],"INVALID")

    def test_07_identity_domains_are_separate(self):
        value=fixture()
        self.assertEqual(len(observation_identity(value)),7)
        self.assertEqual(len(delivery_binding_identity(value)),7)
        self.assertNotIn("payload_digest",P0_EXCLUDED)
        self.assertNotIn("payload_digest",build_h_p0(value))

    def test_08_unknown_trust_result_fails_closed(self):
        c=checks(); c.verify_key_status=lambda e: None
        self.assertEqual(self.validate(fixture(),c)["status"],"UNKNOWN")

    def test_09_invalid_signature_rejected(self):
        c=checks(); c.verify_signature=lambda e,p: False
        self.assertEqual(self.validate(fixture(),c)["status"],"INVALID")

    def test_10_same_digest_replay_returns_original_result(self):
        self.assertEqual(self.validate(fixture(),checks("SAME_DIGEST_REPLAY"))["status"],"VALID_REPLAY")

    def test_11_changed_digest_same_identity_conflicts(self):
        c=checks("CONFLICT")
        self.assertEqual(self.validate(fixture(),c)["status"],"INVALID")


if __name__ == "__main__":
    unittest.main()
