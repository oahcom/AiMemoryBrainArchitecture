#![recursion_limit = "512"]
//! Cross-implementation conformance: the Rust P0 digest must equal the value
//! produced by the BMCP Python reference validator for the same envelope.
//!
//! Expected value computed by `state/_p0_py.py`, which is a byte-for-byte
//! transcription of `canonical_p0_bytes()` in
//! `08-bmcp-protocol/validators/applied_delivery_evidence_validator.py`:
//!     json.dumps(build_h_p0(env), ensure_ascii=False, sort_keys=True,
//!                separators=(",", ":"))
//!
//! If this test fails, the Rust canonicalization diverged from the reference
//! implementation and every recorded digest becomes unverifiable.

use bmcp_protocol::digest::p0_digest_of_value;
use serde_json::{json, Value};

const EXPECTED_P0: &str = "1554fe033d057e297281fee1f748b70cd20d2e2bdee7e92d52621bfe7d79a478";

fn reference_envelope() -> Value {
    json!({
        "schema_artifact_revision": "1.0.0",
        "message_type": "APPLIED_DELIVERY_EVIDENCE_RECORDED",
        "issuer_ref": "issuer",
        "sender_authority_ref": "authority",
        "sender_subject_ref": "subject",
        "audience": "audience",
        "message_id": "message",
        "message_nonce": "nonce",
        "signing_sequence_namespace_ref": "namespace",
        "signing_record_sequence": "1",
        "signature_profile_id": "profile",
        "key_id_ref": "key",
        "key_version": "1",
        "adapter_instance_ref": "adapter-instance",
        "runtime_session_ref": "runtime-session",
        "delivery_id": "delivery",
        "delivery_attempt_id": "attempt",
        "inference_request_id": "inference",
        "final_request_boundary_id": "boundary",
        "adapter_capability_epoch": "1",
        "evidence_kind": "APPLIED_CONTEXT_OBSERVED",
        "evidence_tier": "TIER_2",
        "adapter_ref": "adapter",
        "runtime_instance_ref": "runtime",
        "context_id": "context",
        "context_version": "v1",
        "materialized_context_version": "v1",
        "final_request_boundary_type": "final",
        "managed_region_id": "region",
        "managed_region_revision": "1",
        "managed_region_inventory_digest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "managed_region_coverage": "PARTIAL",
        "managed_region_digest": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "digest_profile": "p0",
        "evidence_issuer_ref": "evidence-issuer",
        "evidence_schema_version": "1.0.0",
        "submission_observed_at": "2026-01-01T12:30:45Z",
        "correlation_ref": "correlation",
        "causation_ref": "causation",
        "audit_ref": "audit",
        "c_submit_outcome_ref": "submit",
        "c_outcome_record_ref": "record",
        "c_outcome_record_sequence": "2",
        "c_outcome_payload_digest": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "payload_digest": "0000000000000000000000000000000000000000000000000000000000000000",
        "signature": "signature",
        "integrity_proof_ref": "proof"
    })
}

#[test]
fn p0_digest_matches_python_reference_validator() {
    let actual = p0_digest_of_value(&reference_envelope()).expect("digest");
    assert_eq!(actual, EXPECTED_P0);
}

#[test]
fn p0_digest_ignores_excluded_fields() {
    let mut value = reference_envelope();
    let baseline = p0_digest_of_value(&value).expect("digest");

    // payload_digest / signature / integrity_proof_ref are outside P0.
    value["payload_digest"] = json!("ff".repeat(32));
    value["signature"] = json!("totally-different-signature");
    value["integrity_proof_ref"] = json!("another-proof");
    assert_eq!(p0_digest_of_value(&value).expect("digest"), baseline);
}

#[test]
fn p0_digest_changes_when_a_covered_field_changes() {
    let mut value = reference_envelope();
    let baseline = p0_digest_of_value(&value).expect("digest");

    value["delivery_attempt_id"] = json!("attempt-2");
    assert_ne!(p0_digest_of_value(&value).expect("digest"), baseline);
}

#[test]
fn p0_digest_rejects_unknown_member() {
    let mut value = reference_envelope();
    value["not_a_protocol_field"] = json!("x");
    assert!(p0_digest_of_value(&value).is_err());
}
