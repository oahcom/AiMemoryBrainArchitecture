import copy
import hashlib
import json
import unittest
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "validators"))
SCHEMA = json.loads((ROOT / "schemas" / "bmcp.applied-delivery-evidence-1.0.0.schema.json").read_text())
C_VECTOR_PATH = ROOT / "tests" / "conformance" / "provider_outcome" / "fixtures" / "c_submit_outcome_1_0_1_vectors.json"
C_VECTORS = json.loads(C_VECTOR_PATH.read_text())
C_ACCEPTED_RECORD = next(v["record"] for v in C_VECTORS["vectors"] if v["id"] == "CPO-01-accepted")
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
        "inference_request_id":"R/request/1","final_request_boundary_id":"C/final-boundary/CPO-01-accepted",
        "adapter_capability_epoch":"H/capability-epoch/1","evidence_kind":"FINAL_REQUEST_SUBMITTED","evidence_tier":"TIER_1",
        "adapter_ref":"H/adapter/1","runtime_instance_ref":"R/runtime/1","context_id":"G/context/1",
        "context_version":"G/context-version/7","materialized_context_version":"G/context-version/7",
        "final_request_boundary_type":"RUNTIME_FINAL_SUBMIT_HOOK","managed_region_id":"G/managed-region/1",
        "managed_region_revision":"rev-7","managed_region_inventory_digest":"a"*64,
        "managed_region_coverage":"COMPLETE","managed_region_digest":"b"*64,"digest_profile":"TEST-ONLY-SHA256",
        "evidence_issuer_ref":"H/adapter-evidence/issuer","evidence_schema_version":"1.0.0",
        "submission_observed_at":"2026-11-18T00:00:00Z","submission_monotonic_sequence":"9",
        "correlation_ref":"G/delivery/1","causation_ref":"C/boundary/1","audit_ref":"H/audit/1",
        "c_submit_outcome_ref":"C/outcome/CPO-01-accepted","c_outcome_record_ref":"C/outcome/CPO-01-accepted",
        "c_outcome_record_sequence":"41","c_outcome_payload_digest":"1"*64,
        "payload_digest":"0"*64,"signature":"TEST-SIGNATURE","integrity_proof_ref":"H/integrity/1"
    }
    value["payload_digest"] = hashlib.sha256(canonical_p0_bytes(value)).hexdigest()
    return value


def checks(disposition="NEW", replay_i_authorization=True, replay_d_fence=True, c_record=None, c_verification=True, resolver_available=True):
    resolved_record = copy.deepcopy(C_ACCEPTED_RECORD if c_record is None else c_record)
    return AppliedDeliveryChecks(
        verify_profile_registration=lambda e: True, verify_key_status=lambda e: True,
        verify_signature=lambda e,p: True, verify_protected_identity_binding=lambda e: True,
        verify_c_final_boundary=lambda e: True, verify_g_delivery_binding=lambda e: True,
        verify_capability_epoch=lambda e: True,
        commit_observation=lambda e,d: DurableObservationDecision(disposition, "H/result/1" if disposition=="SAME_DIGEST_REPLAY" else None),
        verify_current_i_replay_authorization=lambda e,r: replay_i_authorization,
        verify_current_d_forget_fence=lambda e,r: replay_d_fence,
        resolve_c_submit_outcome=lambda ref: resolved_record if resolver_available else None,
        verify_c_submit_outcome_record=lambda record: c_verification,
    )


class AppliedDeliveryEvidenceTests(unittest.TestCase):
    def validate_raw(self, raw, callbacks=None):
        return validate_applied_delivery_evidence(raw, SCHEMA, callbacks or checks())

    def validate(self, value, callbacks=None):
        raw=json.dumps(value,separators=(",",":"),sort_keys=True).encode()
        return self.validate_raw(raw, callbacks)

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
        self.assertIn("payload_digest",P0_EXCLUDED)
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

    def test_12_duplicate_top_level_json_member_rejected(self):
        raw=b'{"message_type":"APPLIED_DELIVERY_EVIDENCE_RECORDED","message_type":"ATTACKER"}'
        result=self.validate_raw(raw)
        self.assertEqual(result["status"],"INVALID")
        self.assertEqual(result["errors"], ["invalid JSON: ValueError"])

    def test_13_duplicate_nested_json_member_rejected(self):
        raw=b'{"outer":{"identity":"trusted","identity":"attacker"}}'
        result=self.validate_raw(raw)
        self.assertEqual(result["status"],"INVALID")
        self.assertEqual(result["errors"], ["invalid JSON: ValueError"])

    def test_14_replay_result_not_disclosed_after_authorization_denial(self):
        result=self.validate(fixture(),checks("SAME_DIGEST_REPLAY",replay_i_authorization=False))
        self.assertEqual(result["status"],"INVALID")
        self.assertNotIn("original_result_ref",result)

    def test_15_replay_result_not_disclosed_when_current_authority_unknown(self):
        result=self.validate(fixture(),checks("SAME_DIGEST_REPLAY",replay_i_authorization=None))
        self.assertEqual(result["status"],"UNKNOWN")
        self.assertNotIn("original_result_ref",result)

    def test_16_replay_result_not_disclosed_when_authority_callback_raises(self):
        c=checks("SAME_DIGEST_REPLAY")
        c.verify_current_i_replay_authorization=lambda e,r: (_ for _ in ()).throw(RuntimeError("I unavailable"))
        result=self.validate(fixture(),c)
        self.assertEqual(result["status"],"UNKNOWN")
        self.assertNotIn("original_result_ref",result)

    def test_17_exact_c_submit_outcome_1_0_1_fixture_is_joined(self):
        self.assertEqual(self.validate(fixture())["status"],"VALID_NEW")

    def test_18_c_record_ref_mismatch_rejected(self):
        record=copy.deepcopy(C_ACCEPTED_RECORD); record["record_ref"]="C/outcome/attacker"
        self.assertEqual(self.validate(fixture(),checks(c_record=record))["status"],"INVALID")

    def test_19_c_record_sequence_mismatch_rejected(self):
        record=copy.deepcopy(C_ACCEPTED_RECORD); record["record_sequence"]="42"
        self.assertEqual(self.validate(fixture(),checks(c_record=record))["status"],"INVALID")

    def test_20_c_payload_digest_mismatch_rejected(self):
        record=copy.deepcopy(C_ACCEPTED_RECORD); record["payload_digest"]="2"*64
        self.assertEqual(self.validate(fixture(),checks(c_record=record))["status"],"INVALID")

    def test_21_c_final_request_boundary_mismatch_rejected(self):
        record=copy.deepcopy(C_ACCEPTED_RECORD); record["FinalRequestBoundaryRef"]="C/final-boundary/attacker"
        self.assertEqual(self.validate(fixture(),checks(c_record=record))["status"],"INVALID")

    def test_22_actual_inference_request_id_mismatch_rejected_when_c_supplies_it(self):
        record=copy.deepcopy(C_ACCEPTED_RECORD); record["ActualInferenceRequestId"]="R/request/other"
        self.assertEqual(self.validate(fixture(),checks(c_record=record))["status"],"INVALID")

    def test_23_c_record_resolver_unavailable_fails_closed(self):
        result=self.validate(fixture(),checks(resolver_available=False))
        self.assertEqual(result["status"],"UNKNOWN")

    def test_24_c_record_authentication_denial_rejected(self):
        self.assertEqual(self.validate(fixture(),checks(c_verification=False))["status"],"INVALID")

    def test_25_c_record_authentication_unknown_fails_closed(self):
        self.assertEqual(self.validate(fixture(),checks(c_verification=None))["status"],"UNKNOWN")

    def test_26_c_record_missing_issuer_identity_rejected(self):
        record=copy.deepcopy(C_ACCEPTED_RECORD); record.pop("issuer_authority_ref")
        self.assertEqual(self.validate(fixture(),checks(c_record=record))["status"],"INVALID")

    def test_27_resolver_record_ref_must_equal_h_c_submit_outcome_ref(self):
        record=copy.deepcopy(C_ACCEPTED_RECORD)
        record["record_ref"]="C/outcome/other-valid-record"
        result=self.validate(fixture(),checks(c_record=record))
        self.assertEqual(result["status"],"INVALID")
        self.assertIn("does not equal H c_submit_outcome_ref", result["errors"][0])

    def test_28_replay_result_not_disclosed_after_d_fence_denial(self):
        result=self.validate(fixture(),checks("SAME_DIGEST_REPLAY",replay_d_fence=False))
        self.assertEqual(result["status"],"INVALID")
        self.assertNotIn("original_result_ref",result)

    def test_29_replay_result_not_disclosed_when_d_fence_unknown(self):
        result=self.validate(fixture(),checks("SAME_DIGEST_REPLAY",replay_d_fence=None))
        self.assertEqual(result["status"],"UNKNOWN")
        self.assertNotIn("original_result_ref",result)

    def test_30_replay_result_not_disclosed_when_d_fence_callback_raises(self):
        c=checks("SAME_DIGEST_REPLAY")
        c.verify_current_d_forget_fence=lambda e,r: (_ for _ in ()).throw(RuntimeError("D unavailable"))
        result=self.validate(fixture(),c)
        self.assertEqual(result["status"],"UNKNOWN")
        self.assertNotIn("original_result_ref",result)


    def test_31_rfc3339_accepts_lowercase_and_leap_second_forms(self):
        for observed_at in ("2024-01-01t00:00:00z", "2016-12-31T23:59:60Z"):
            value = fixture()
            value["submission_observed_at"] = observed_at
            value["payload_digest"] = hashlib.sha256(canonical_p0_bytes(value)).hexdigest()
            with self.subTest(observed_at=observed_at):
                self.assertEqual(self.validate(value)["status"], "VALID_NEW")

    def test_32_rfc3339_rejects_impossible_calendar_date(self):
        value = fixture()
        value["submission_observed_at"] = "2024-02-30T00:00:00Z"
        value["payload_digest"] = hashlib.sha256(canonical_p0_bytes(value)).hexdigest()
        result = self.validate(value)
        self.assertEqual(result["status"], "INVALID")
        self.assertIn("invalid RFC3339", result["errors"][0])


    def test_33_profile_registration_rejection(self):
        c=checks(); c.verify_profile_registration=lambda e: False
        result=self.validate(fixture(),c)
        self.assertEqual(result["status"],"INVALID")
        self.assertIn("profile registration verifier rejected evidence",result["errors"])

    def test_34_protected_identity_binding_rejection(self):
        c=checks(); c.verify_protected_identity_binding=lambda e: False
        result=self.validate(fixture(),c)
        self.assertEqual(result["status"],"INVALID")
        self.assertIn("protected identity binding verifier rejected evidence",result["errors"])

    def test_35_c_final_boundary_rejection(self):
        c=checks(); c.verify_c_final_boundary=lambda e: False
        result=self.validate(fixture(),c)
        self.assertEqual(result["status"],"INVALID")
        self.assertIn("C final boundary verifier rejected evidence",result["errors"])

    def test_36_g_delivery_binding_rejection(self):
        c=checks(); c.verify_g_delivery_binding=lambda e: False
        result=self.validate(fixture(),c)
        self.assertEqual(result["status"],"INVALID")
        self.assertIn("G delivery binding verifier rejected evidence",result["errors"])

    def test_37_capability_epoch_rejection(self):
        c=checks(); c.verify_capability_epoch=lambda e: False
        result=self.validate(fixture(),c)
        self.assertEqual(result["status"],"INVALID")
        self.assertIn("Adapter capability epoch verifier rejected evidence",result["errors"])

    def test_38_profile_registration_unknown_is_not_rejection(self):
        c=checks(); c.verify_profile_registration=lambda e: None
        result=self.validate(fixture(),c)
        self.assertEqual(result["status"],"UNKNOWN")
        self.assertIn("profile registration verifier result is indeterminate",result["unknown"])

if __name__ == "__main__":
    unittest.main()