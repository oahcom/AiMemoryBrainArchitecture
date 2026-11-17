"""Fail-closed H gateway-attested ingress validator for BMCP 1.2.15.

This is a reference integration implementation. All trust, signer, origin
transport, key-status, integrity-evidence and durable replay callbacks are
deployment seams. Missing/unavailable authority evidence returns UNKNOWN.
It is not production cryptography or a deployed trust service.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any, Callable, Optional

import rfc8785

from envelope_auth_validator import ProtectedTransportContext
from provider_outcome_validator_1_2_15 import (
    AuthorityChecks,
    DuplicateJSONKey,
    parse_strict_json,
    validate_provider_outcome,
    _schema_errors,
)

H_SCHEMA_ID = "bmcp.coc-jf10-unified"
H_SCHEMA_URI = "https://schemas.aimemorybrainarchitecture.invalid/bmcp.coc-jf10-unified/1.2.15"
H_SCHEMA_REVISION = "1.2.15"
H_WIRE_VERSION = "1.3.0"
H_PROFILE_ID = "AIMBA-H-GATEWAY-ATTEST-1.0"
H_DOMAIN_SEPARATOR = b"AIMBA-H-GATEWAY-ATTEST-P0\x00v1\x00"

# Explicit signed P0 allowlist. No wildcard exclusion is permitted.
# The only excluded fields are payload_digest, signature and integrity_proof_ref.
P0_FIELDS = (
    "schema_id", "schema_artifact_revision", "schema_version", "message_type",
    "message_id", "message_nonce", "audience", "issuer_ref",
    "sender_authority_ref", "sender_subject_ref", "subject_ref",
    "owner_authority", "owner_record_ref", "policy_domain_ref",
    "causal_order_profile_ref", "causal_order_coordinator_ref",
    "causal_order_domain_ref", "canonicalization_profile_id", "digest_algorithm",
    "key_id_ref", "key_version", "signature_profile_id", "created_at",
    "channel_binding_proof_ref", "owner_signature_ref", "coc_commit_proof_ref",
    "coc_record_ref", "coc_record_position", "coc_entry_digest",
    "coc_previous_entry_digest", "origin_transport_context_ref",
    "origin_transport_context_digest", "origin_received_bytes_digest",
    "origin_issuer_ref", "origin_sender_authority_ref",
    "origin_sender_subject_ref", "origin_authentication_context_ref",
    "origin_channel_binding_proof_ref", "origin_received_at",
    "signing_sequence_namespace_ref", "signing_record_sequence",
    "c_submit_outcome_ref", "c_submit_outcome_digest", "provider_outcome",
    "provider_ref", "provider_adapter_ref", "provider_idempotency_key_ref",
    "provider_request_ref", "provider_receipt_ref", "actual_inference_request_id",
    "final_request_boundary_id", "request_digest", "transaction_ref",
    "participant_reservation_ref", "prepared_participant_ref",
    "prepare_attempt_ref", "prepare_attempt_generation", "participant_ledger_ref",
    "participant_ledger_version", "participant_tuple_digest",
    "i_terminal_decision_ref", "d_clearance_ref", "storage_resolution_proof_ref",
    "provider_outcome_evidence_ref", "provider_lookup_proof_ref",
    "provider_no_handoff_proof_ref", "not_invoked_proof_ref", "unknown_reason_ref",
    "owner_admission_ref", "owner_admission_digest", "owner_ledger_ref",
    "owner_ledger_version", "owner_local_sequence", "owner_high_water",
    "owner_ledger_root", "coc_participant_intent_ref", "coc_absence_reason",
)

_EXCLUDED_P0_FIELDS = {"payload_digest", "signature", "integrity_proof_ref"}


@dataclass(frozen=True)
class DurableIngressDecision:
    # NEW means an immutable accepted receipt/result was durably committed.
    # SAME_DIGEST_REPLAY must include the original durable result reference.
    decision: str
    prior_result_ref: Optional[str] = None


@dataclass
class GatewayAttestationChecks:
    # True = verified, False = authenticated contradiction, None = unavailable.
    verify_profile_registration: Optional[
        Callable[[dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_key_status: Optional[
        Callable[[dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_h_signature: Optional[
        Callable[[dict[str, Any], bytes, ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_integrity_evidence: Optional[
        Callable[[dict[str, Any], str, ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_identity_binding: Optional[
        Callable[[dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_origin_transport_receipt: Optional[
        Callable[[dict[str, Any], bytes, dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None
    # Atomically reserve replay identity and durably commit the accepted ingress.
    # This callback must be crash-safe; an in-memory dedupe cache is not sufficient.
    commit_authenticated_ingress: Optional[
        Callable[[dict[str, Any], str, ProtectedTransportContext], DurableIngressDecision]
    ] = None
    # Re-check current I authorization/PermissionEpoch, key status, audience/scope
    # and applicable D Forget fence before disclosing a prior result on replay.
    verify_replay_disclosure_authorization: Optional[
        Callable[[dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None


def _collect_check(
    label: str,
    callback,
    args: tuple,
    invalid: list[str],
    unknown: list[str],
) -> None:
    if callback is None:
        unknown.append(label + " verifier not configured")
        return
    try:
        result = callback(*args)
    except Exception:
        result = None
    if result is False:
        invalid.append(label + " verification contradiction")
    elif result is None:
        unknown.append(label + " evidence unavailable")
    elif result is not True:
        unknown.append(label + " returned unsupported result")


def build_h_p0(envelope: dict[str, Any]) -> dict[str, Any]:
    unexpected = set(envelope) - set(P0_FIELDS) - _EXCLUDED_P0_FIELDS
    if unexpected:
        raise ValueError("unrecognized envelope members outside H P0 allowlist: " + ", ".join(sorted(unexpected)))
    return {name: envelope[name] for name in P0_FIELDS if name in envelope}


def h_p0_digest_and_preimage(envelope: dict[str, Any]) -> tuple[str, bytes]:
    p0 = build_h_p0(envelope)
    canonical = rfc8785.dumps(p0)
    digest = hashlib.sha256(canonical).hexdigest()
    preimage = H_DOMAIN_SEPARATOR + canonical
    return digest, preimage


def validate_gateway_attested_provider_outcome(
    raw_envelope: bytes,
    raw_c_object: bytes,
    raw_origin_bytes: Optional[bytes],
    protected_context: Optional[ProtectedTransportContext],
    gateway_checks: GatewayAttestationChecks,
    envelope_schema: dict,
    c_object_schema: dict,
    c_checks: AuthorityChecks,
) -> dict[str, Any]:
    """Validate H 1.2.15 gateway attestation, then independent C object semantics."""
    try:
        envelope = parse_strict_json(raw_envelope)
        c_object = parse_strict_json(raw_c_object)
    except (UnicodeDecodeError, DuplicateJSONKey, ValueError, TypeError) as exc:
        return {"status": "INVALID", "errors": [f"strict JSON parse failed: {type(exc).__name__}"], "unknown": []}

    invalid: list[str] = []
    unknown: list[str] = []

    if envelope_schema.get("$id") != H_SCHEMA_URI:
        invalid.append("wrong loaded H 1.2.15 schema artifact URI")
    if envelope.get("schema_id") != H_SCHEMA_ID:
        invalid.append("wrong H schema_id")
    if envelope.get("schema_artifact_revision") != H_SCHEMA_REVISION:
        invalid.append("wrong H schema artifact revision")
    if envelope.get("schema_version") != H_WIRE_VERSION:
        invalid.append("wrong H wire schema version")
    if envelope.get("message_type") != "C_PROVIDER_OUTCOME_RECORDED":
        invalid.append("wrong message_type")
    invalid.extend("H schema: " + err for err in _schema_errors(envelope, envelope_schema))
    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": []}

    if protected_context is None:
        return {
            "status": "UNKNOWN", "errors": [],
            "unknown": ["protected H gateway transport/session context unavailable"],
        }

    # These sender fields identify the H gateway attestor, not the C owner.
    for field, trusted in (
        ("issuer_ref", protected_context.issuer_ref),
        ("sender_authority_ref", protected_context.authority_ref),
        ("sender_subject_ref", protected_context.subject_ref),
        ("audience", protected_context.audience),
        ("channel_binding_proof_ref", protected_context.channel_binding_proof_ref),
    ):
        if envelope.get(field) != trusted:
            invalid.append(f"H gateway protected-context mismatch: {field}")

    if envelope.get("owner_authority") != "C":
        invalid.append("gateway-attested Provider Outcome must retain owner_authority=C")
    if envelope.get("owner_record_ref") != envelope.get("c_submit_outcome_ref"):
        invalid.append("owner_record_ref must equal c_submit_outcome_ref")
    if envelope.get("signature_profile_id") != H_PROFILE_ID:
        invalid.append("wrong H gateway attestation profile identifier")
    if envelope.get("canonicalization_profile_id") != "RFC8785-JCS-1.0":
        invalid.append("wrong H gateway canonicalization profile identifier")
    if not isinstance(envelope.get("signature"), str) or not re.fullmatch(r"[A-Za-z0-9_-]{86}", envelope["signature"]):
        invalid.append("H Ed25519 signature must be 86-character unpadded Base64url")

    if raw_origin_bytes is None or not isinstance(raw_origin_bytes, bytes):
        unknown.append("original C-to-H ingress bytes unavailable")
    elif hashlib.sha256(raw_origin_bytes).hexdigest() != envelope.get("origin_received_bytes_digest"):
        invalid.append("origin_received_bytes_digest mismatch")

    try:
        computed_digest, h_preimage = h_p0_digest_and_preimage(envelope)
    except Exception as exc:
        return {"status": "INVALID", "errors": [f"H P0 construction failed: {type(exc).__name__}"], "unknown": []}
    if computed_digest != envelope.get("payload_digest"):
        invalid.append("H gateway payload_digest mismatch")

    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": unknown}

    checks = (
        ("H profile registration", gateway_checks.verify_profile_registration, (envelope, protected_context)),
        ("H key status at signing sequence/current head", gateway_checks.verify_key_status, (envelope, protected_context)),
        ("H gateway signature", gateway_checks.verify_h_signature, (envelope, h_preimage, protected_context)),
        ("H integrity evidence reference", gateway_checks.verify_integrity_evidence, (envelope, computed_digest, protected_context)),
        ("H gateway identity/delegation", gateway_checks.verify_identity_binding, (envelope, protected_context)),
    )
    for label, callback, args in checks:
        _collect_check(label, callback, args, invalid, unknown)

    if raw_origin_bytes is not None:
        _collect_check(
            "original C ingress transport receipt/AdapterRef binding",
            gateway_checks.verify_origin_transport_receipt,
            (envelope, raw_origin_bytes, c_object, protected_context),
            invalid,
            unknown,
        )
    else:
        unknown.append("origin transport receipt cannot be checked without original ingress bytes")

    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": unknown}
    if unknown:
        return {"status": "UNKNOWN", "errors": [], "unknown": unknown}

    # Independently validate the C immutable object, C-P0 and all C/I/D/Storage joins.
    c_result = validate_provider_outcome(envelope, c_object, envelope_schema, c_object_schema, c_checks)
    if c_result["status"] != "VALID":
        c_result["h_gateway_attestation_authenticated"] = True
        return c_result

    if gateway_checks.commit_authenticated_ingress is None:
        return {
            "status": "UNKNOWN", "errors": [],
            "unknown": ["durable replay reservation/ingress commit not configured"],
            "h_gateway_attestation_authenticated": True,
        }

    try:
        durable = gateway_checks.commit_authenticated_ingress(
            envelope, computed_digest, protected_context
        )
    except Exception:
        durable = DurableIngressDecision("UNKNOWN")

    if not isinstance(durable, DurableIngressDecision):
        durable = DurableIngressDecision("UNKNOWN")
    if durable.decision == "CONFLICT":
        return {
            "status": "INVALID", "errors": ["message identity/nonce reused with a different H P0 digest"],
            "unknown": [], "h_gateway_attestation_authenticated": True,
        }
    if durable.decision == "UNKNOWN":
        return {
            "status": "UNKNOWN", "errors": [],
            "unknown": ["durable replay/ingress state unavailable"],
            "h_gateway_attestation_authenticated": True,
        }
    if durable.decision == "SAME_DIGEST_REPLAY":
        if not durable.prior_result_ref:
            return {
                "status": "UNKNOWN", "errors": [],
                "unknown": ["same-digest replay has no prior durable result reference"],
                "h_gateway_attestation_authenticated": True,
            }
        replay_invalid: list[str] = []
        replay_unknown: list[str] = []
        _collect_check(
            "current authorization to disclose prior replay result",
            gateway_checks.verify_replay_disclosure_authorization,
            (envelope, protected_context),
            replay_invalid,
            replay_unknown,
        )
        if replay_invalid:
            return {"status": "INVALID", "errors": replay_invalid, "unknown": replay_unknown}
        if replay_unknown:
            return {"status": "UNKNOWN", "errors": [], "unknown": replay_unknown}
        return {
            "status": "IDEMPOTENT_REPLAY", "errors": [], "unknown": [],
            "prior_result_ref": durable.prior_result_ref,
            "h_gateway_attestation_authenticated": True,
        }
    if durable.decision != "NEW":
        return {
            "status": "UNKNOWN", "errors": [],
            "unknown": ["unsupported durable ingress decision"],
            "h_gateway_attestation_authenticated": True,
        }

    c_result["h_gateway_attestation_authenticated"] = True
    c_result["durable_ingress_committed"] = True
    c_result["h_p0_digest"] = computed_digest
    return c_result
