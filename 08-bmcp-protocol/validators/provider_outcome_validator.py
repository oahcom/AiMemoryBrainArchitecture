"""Local H/C schema and C Provider Outcome validator for BMCP 1.2.14.

This module does NOT authenticate the outer BMCP envelope, transport principal,
channel binding or message replay. Direct calls to validate_provider_outcome()
and validate_raw_provider_outcome() are not secure ingress acceptance APIs.
Production ingress MUST call validate_authenticated_provider_outcome() from
envelope_auth_validator.py first, then supply real owner-authority verifiers.

This remains an integration seam, not a production-ready trust implementation.
All authority-dependent checks are injected callbacks and MUST be supplied by
the deployment. Missing callbacks produce UNKNOWN, never VALID.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable, Optional

import rfc8785
from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_ARTIFACT_REVISION = "1.2.14"
WIRE_SCHEMA_VERSION = "1.3.0"
BMCP_SCHEMA_ID = "bmcp.coc-jf10-unified"
BMCP_SCHEMA_URI = "https://schemas.aimemorybrainarchitecture.invalid/bmcp.coc-jf10-unified/1.2.14"
C_OBJECT_SCHEMA_ID = "CSubmitOutcome"
C_OBJECT_SCHEMA_URI = "urn:aimba:schema:c-submit-outcome:1.0.1"
C_PROFILE_ID = "AIMBA-C-CRYPTO-1.0"

# Wire field -> immutable C object field. The exact H schema remains the
# structural authority; this table only defines duplicated-value equality.
WIRE_TO_C = {
    "c_submit_outcome_ref": "record_ref",
    "c_submit_outcome_digest": "payload_digest",
    "provider_outcome": "Outcome",
    "provider_ref": "ProviderRef",
    "provider_adapter_ref": "AdapterRef",
    "provider_idempotency_key_ref": "IdempotencyKeyRef",
    "final_request_boundary_id": "FinalRequestBoundaryRef",
    "request_digest": "RequestDigest",
    "transaction_ref": "CausalOrderTransactionRef",
    "provider_outcome_evidence_ref": "OutcomeEvidenceRef",
    "provider_request_ref": "ProviderRequestRef",
    "provider_receipt_ref": "ProviderReceiptRef",
    "provider_lookup_proof_ref": "ProviderLookupProofRef",
    "provider_no_handoff_proof_ref": "ProviderNoHandoffProofRef",
    "not_invoked_proof_ref": "NotInvokedProofRef",
    "unknown_reason_ref": "UnknownReasonRef",
    "actual_inference_request_id": "ActualInferenceRequestId",
    "owner_signature_ref": "OwnerSignatureRef",
    "owner_admission_ref": "CAdmissionRef",
    "owner_admission_digest": "CAdmissionDigest",
    "owner_ledger_ref": "COwnerLedgerRef",
    "owner_ledger_version": "COwnerLedgerVersion",
    "owner_local_sequence": "COwnerLocalSequence",
    "owner_high_water": "COwnerHighWater",
    "owner_ledger_root": "COwnerLedgerRoot",
    "coc_participant_intent_ref": "COCParticipantIntentRef",
    "participant_reservation_ref": "COCParticipantReservationRef",
    "coc_absence_reason": "COCAbsenceReason",
}


class DuplicateJSONKey(ValueError):
    pass


def _reject_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _reject_non_json_constant(value):
    raise ValueError(f"non-JSON numeric constant: {value}")


def parse_strict_json(raw: bytes) -> dict[str, Any]:
    if not isinstance(raw, bytes):
        raise TypeError("raw JSON must be bytes")
    text = raw.decode("utf-8", errors="strict")
    value = json.loads(
        text,
        object_pairs_hook=_reject_duplicate_pairs,
        parse_constant=_reject_non_json_constant,
    )
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def _schema_errors(instance: dict, schema: dict) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [e.message for e in validator.iter_errors(instance)]


def _semantic_errors(record: dict) -> list[str]:
    errors = []
    if not record.get("sequence_namespace_ref"):
        errors.append("C outcome sequence namespace is required")
    if int(record["COwnerLocalSequence"]) > int(record["COwnerHighWater"]):
        errors.append("C owner local sequence exceeds high-water")
    intent = record["COCParticipantIntentRef"]
    reservation = record["COCParticipantReservationRef"]
    absence_reason = record["COCAbsenceReason"]
    if intent is None:
        if reservation is not None or not absence_reason:
            errors.append("null COC intent requires null reservation and explicit reason")
    elif not isinstance(reservation, str) or not reservation or absence_reason is not None:
        errors.append("non-null COC intent requires reservation and null absence reason")

    outcome = record["Outcome"]
    side_effect = record["SideEffectStatus"]
    if outcome == "HANDOFF_ACCEPTED":
        if not record.get("ProviderReceiptRef") or side_effect != "PROVEN_OCCURRED":
            errors.append("HANDOFF_ACCEPTED requires provider receipt and PROVEN_OCCURRED")
    elif outcome == "HANDOFF_REJECTED" and side_effect == "PROVEN_NONE":
        if not record.get("ProviderNoHandoffProofRef"):
            errors.append("rejected-as-no-side-effect requires authoritative no-handoff proof")
    elif outcome == "NOT_INVOKED":
        if side_effect != "PROVEN_NONE" or not record.get("ProviderNoHandoffProofRef") or not record.get("NotInvokedProofRef"):
            errors.append("NOT_INVOKED requires durable no-handoff proofs and PROVEN_NONE")
    elif outcome in ("UNKNOWN", "IN_DOUBT"):
        if side_effect != "POSSIBLE_OR_UNKNOWN" or not record.get("UnknownReasonRef"):
            errors.append("UNKNOWN/IN_DOUBT must remain nonterminal with a reason")
    return errors


def _p0(record: dict) -> dict:
    # C-P0 is every present schema-allowed member except the derived digest
    # and signature. additionalProperties=false prevents wildcard omissions.
    return {k: v for k, v in record.items() if k not in ("payload_digest", "signature")}


def _candidate_digest_and_preimage(record: dict) -> tuple[str, bytes]:
    p0_bytes = rfc8785.dumps(_p0(record))
    digest = hashlib.sha256(b"AIMBA-C-PAYLOAD-v1\0" + p0_bytes).hexdigest()
    signed_projection = dict(_p0(record))
    signed_projection["payload_digest"] = digest
    signed_bytes = rfc8785.dumps(signed_projection)
    preimage = (
        b"AIMBA-C-SIGNATURE-v1\0"
        + C_PROFILE_ID.encode("ascii")
        + b"\0"
        + record["message_type"].encode("ascii")
        + b"\0"
        + signed_bytes
    )
    return digest, preimage


@dataclass
class AuthorityChecks:
    # Each callback returns True (verified), False (contradiction), or None
    # (unavailable/unknown). No callback may trust a payload-supplied key.
    verify_profile_registration: Optional[Callable[[dict], Optional[bool]]] = None
    verify_key_status: Optional[Callable[[dict], Optional[bool]]] = None
    verify_c_signature: Optional[Callable[[dict, bytes], Optional[bool]]] = None
    verify_provider_evidence: Optional[Callable[[dict, dict], Optional[bool]]] = None
    verify_owner_ledger: Optional[Callable[[dict, dict], Optional[bool]]] = None
    verify_coc_join: Optional[Callable[[dict, dict], Optional[bool]]] = None
    verify_currentness: Optional[Callable[[dict, dict], Optional[bool]]] = None
    # Separate owner authorities: a COC join callback cannot impersonate I, D or Storage.
    # Each callback verifies issuer, exact proof, digest, scope, currentness and joins.
    verify_i_terminal_decision: Optional[Callable[[dict, dict], Optional[bool]]] = None
    verify_d_clearance: Optional[Callable[[dict, dict], Optional[bool]]] = None
    verify_storage_resolution_proof: Optional[Callable[[dict, dict], Optional[bool]]] = None


def validate_provider_outcome(
    envelope: dict,
    c_object: dict,
    envelope_schema: dict,
    c_object_schema: dict,
    checks: AuthorityChecks,
) -> dict:
    """Validate H/C schema and C semantics only; does not authenticate outer H.

    Production ingress must first pass envelope_auth_validator's protected
    transport, signature, key-status, channel-binding, identity and replay gate.
    """
    invalid = []
    unknown = []

    if envelope.get("schema_id") != BMCP_SCHEMA_ID:
        invalid.append("wrong BMCP schema_id")
    if envelope_schema.get("$id") != BMCP_SCHEMA_URI:
        invalid.append("wrong loaded BMCP schema artifact URI")
    if c_object_schema.get("$id") != C_OBJECT_SCHEMA_URI:
        invalid.append("wrong loaded C object schema artifact URI")
    if envelope.get("schema_artifact_revision") != SCHEMA_ARTIFACT_REVISION:
        invalid.append("wrong BMCP schema_artifact_revision")
    if envelope.get("schema_version") != WIRE_SCHEMA_VERSION:
        invalid.append("wrong BMCP schema_version")
    if envelope.get("message_type") != "C_PROVIDER_OUTCOME_RECORDED":
        invalid.append("wrong BMCP message_type")

    invalid.extend("BMCP schema: " + e for e in _schema_errors(envelope, envelope_schema))
    invalid.extend("C object schema: " + e for e in _schema_errors(c_object, c_object_schema))
    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": []}

    if (c_object.get("schema_id") != C_OBJECT_SCHEMA_ID
            or c_object.get("schema_version") != "1.0.1"
            or c_object.get("schema_artifact_revision") != "1.0.1"):
        invalid.append("wrong immutable C object schema identity/revision; require 1.0.1")
    if c_object.get("signature_profile_id") != C_PROFILE_ID:
        invalid.append("wrong C signature profile identifier")
    if c_object.get("message_type") != "C_PROVIDER_OUTCOME_RECORDED" or envelope.get("message_type") != c_object.get("message_type"):
        invalid.append("C object/envelope message_type mismatch")
    if envelope.get("c_submit_outcome_ref") != c_object.get("record_ref"):
        invalid.append("c_submit_outcome_ref does not resolve to this immutable object")
    if envelope.get("c_submit_outcome_digest") != c_object.get("payload_digest"):
        invalid.append("c_submit_outcome_digest differs from C payload_digest")

    for wire_name, object_name in WIRE_TO_C.items():
        if wire_name in envelope:
            if envelope[wire_name] != c_object.get(object_name):
                invalid.append(f"wire/object mismatch: {wire_name} != {object_name}")
        elif object_name in c_object and c_object[object_name] is not None:
            invalid.append(f"non-null C object value missing from wire: {wire_name}")

    invalid.extend(_semantic_errors(c_object))
    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": []}

    try:
        computed_digest, preimage = _candidate_digest_and_preimage(c_object)
    except Exception as exc:
        return {"status": "INVALID", "errors": [f"C canonicalization failed: {type(exc).__name__}"], "unknown": []}
    if computed_digest != c_object["payload_digest"]:
        invalid.append("C payload_digest mismatch")
    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": []}

    callbacks = (
        ("C profile registration", checks.verify_profile_registration, (c_object,)),
        ("C key status at signing sequence", checks.verify_key_status, (c_object,)),
        ("C signature/key status", checks.verify_c_signature, (c_object, preimage)),
        ("provider evidence issuer", checks.verify_provider_evidence, (envelope, c_object)),
        ("C owner ledger inclusion/currentness", checks.verify_owner_ledger, (envelope, c_object)),
        ("COC intent/reservation/quorum join", checks.verify_coc_join, (envelope, c_object)),
        ("anti-rollback/currentness", checks.verify_currentness, (envelope, c_object)),
        ("I terminal decision / COMMIT_WON authority", checks.verify_i_terminal_decision, (envelope, c_object)),
        ("D Forget clearance / fence authority", checks.verify_d_clearance, (envelope, c_object)),
        ("Storage resolution proof / same-GID authority", checks.verify_storage_resolution_proof, (envelope, c_object)),
    )
    for label, callback, args in callbacks:
        if callback is None:
            unknown.append(label + " verifier not configured")
            continue
        try:
            result = callback(*args)
        except Exception:
            result = None
        if result is False:
            invalid.append(label + " verification contradiction")
        elif result is None:
            unknown.append(label + " evidence unavailable")

    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": unknown}
    if unknown:
        return {"status": "UNKNOWN", "errors": [], "unknown": unknown}
    return {"status": "VALID", "errors": [], "unknown": []}



def validate_raw_provider_outcome(
    envelope_raw: bytes,
    c_object_raw: bytes,
    envelope_schema: dict,
    c_object_schema: dict,
    checks: AuthorityChecks,
) -> dict:
    """Strictly parse raw JSON for local tests; NOT an authenticated ingress API.

    This function does not verify outer-envelope signature, transport identity,
    channel binding or replay. Production ingress must use the authenticated
    wrapper in envelope_auth_validator.py.
    """
    try:
        envelope = parse_strict_json(envelope_raw)
        c_object = parse_strict_json(c_object_raw)
    except (UnicodeDecodeError, DuplicateJSONKey, json.JSONDecodeError, ValueError, TypeError) as exc:
        return {"status": "INVALID", "errors": [f"strict JSON parse failed: {type(exc).__name__}"], "unknown": []}
    return validate_provider_outcome(envelope, c_object, envelope_schema, c_object_schema, checks)


# BMCP 1.2.13+ removes the ambiguous participant_intent_ref alias from the C branch.
# CSubmitOutcome 1.0.1 requires sequence_namespace_ref. The verify_key_status
# authority callback must compare it with the authenticated CKeyStatusEvent
# sequence_namespace_ref and prove event_sequence and record_sequence share the
# same durable C authority sequencer. Missing callback remains UNKNOWN; this
# local core never infers namespace equivalence. I terminal, D clearance and Storage
# resolution are separate authority seams; COC join validation does not subsume them.
