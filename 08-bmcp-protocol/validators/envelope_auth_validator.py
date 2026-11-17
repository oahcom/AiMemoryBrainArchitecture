"""Fail-closed H outer-envelope authentication gate.

This is a reference integration boundary, not a production cryptographic
implementation. Trust, key status, channel binding, identity registry and
replay state are supplied by protected verifier callbacks. Missing callbacks
or unavailable authority state never become authenticated success.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import rfc8785
from enum import Enum
from typing import Any, Callable, Optional

from provider_outcome_validator import (
    AuthorityChecks,
    DuplicateJSONKey,
    parse_strict_json,
    validate_provider_outcome,
)


C_ENVELOPE_PROFILE_ID = "AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0"
C_ENVELOPE_CANONICALIZATION_PROFILE = "RFC8785-JCS-1.0"
C_ENVELOPE_PAYLOAD_DOMAIN = b"AIMBA-C-BMCP-ENVELOPE-PAYLOAD-v1" + bytes([0])
C_ENVELOPE_SIGNATURE_DOMAIN = b"AIMBA-C-BMCP-ENVELOPE-SIGNATURE-v1" + bytes([0])

OUTER_ENVELOPE_P0_FIELDS = frozenset("""
schema_id schema_artifact_revision schema_version message_type message_id
message_nonce audience sender_authority_ref sender_subject_ref issuer_ref
subject_ref owner_authority owner_record_ref policy_domain_ref
causal_order_profile_ref causal_order_coordinator_ref causal_order_domain_ref
canonicalization_profile_id signature_profile_id digest_algorithm
integrity_proof_ref channel_binding_proof_ref key_id_ref key_version
created_at owner_signature_ref
c_submit_outcome_ref c_submit_outcome_digest provider_outcome provider_ref
provider_adapter_ref provider_idempotency_key_ref provider_request_ref
provider_receipt_ref actual_inference_request_id final_request_boundary_id
request_digest transaction_ref participant_reservation_ref prepared_participant_ref
prepare_attempt_ref prepare_attempt_generation participant_ledger_ref
participant_ledger_version participant_tuple_digest i_terminal_decision_ref
d_clearance_ref storage_resolution_proof_ref provider_outcome_evidence_ref
provider_lookup_proof_ref provider_no_handoff_proof_ref not_invoked_proof_ref
unknown_reason_ref owner_admission_ref owner_admission_digest owner_ledger_ref
owner_ledger_version owner_local_sequence owner_high_water owner_ledger_root
coc_participant_intent_ref coc_absence_reason
""".split())
OUTER_ENVELOPE_COC_APPENDED_FIELDS = frozenset({
    "coc_commit_proof_ref", "coc_record_ref", "coc_record_position",
    "coc_entry_digest", "coc_previous_entry_digest",
})
OUTER_ENVELOPE_REQUIRED_FIELDS = frozenset({
    "schema_id", "schema_artifact_revision", "schema_version", "message_type",
    "message_id", "message_nonce", "audience", "sender_authority_ref",
    "sender_subject_ref", "issuer_ref", "subject_ref", "owner_authority",
    "owner_record_ref", "causal_order_profile_ref",
    "causal_order_coordinator_ref", "causal_order_domain_ref",
    "canonicalization_profile_id", "signature_profile_id", "digest_algorithm",
    "integrity_proof_ref", "channel_binding_proof_ref", "key_id_ref",
    "key_version", "created_at", "owner_signature_ref",
    "payload_digest", "signature",
})


def outer_envelope_p0(envelope: dict[str, Any]) -> dict[str, Any]:
    """Extract the exact C outer-envelope P0; reject unclassified members."""
    unknown = set(envelope) - OUTER_ENVELOPE_P0_FIELDS - OUTER_ENVELOPE_COC_APPENDED_FIELDS - {"payload_digest", "signature"}
    if unknown:
        raise ValueError("unclassified outer-envelope members: " + ", ".join(sorted(unknown)))
    missing = OUTER_ENVELOPE_REQUIRED_FIELDS - set(envelope)
    if missing:
        raise ValueError("missing outer-envelope P0/security members: " + ", ".join(sorted(missing)))
    if envelope.get("signature_profile_id") != C_ENVELOPE_PROFILE_ID:
        raise ValueError("wrong C outer-envelope signature_profile_id")
    if envelope.get("canonicalization_profile_id") != C_ENVELOPE_CANONICALIZATION_PROFILE:
        raise ValueError("wrong C outer-envelope canonicalization_profile_id")
    if envelope.get("digest_algorithm") != "SHA-256":
        raise ValueError("wrong C outer-envelope digest_algorithm")
    if envelope.get("schema_id") != "bmcp.coc-jf10-unified" or envelope.get("schema_artifact_revision") != "1.2.14" or envelope.get("schema_version") != "1.3.0":
        raise ValueError("wrong C outer-envelope schema identity/revision")
    if envelope.get("message_type") != "C_PROVIDER_OUTCOME_RECORDED":
        raise ValueError("wrong C outer-envelope message family")
    return {name: envelope[name] for name in OUTER_ENVELOPE_P0_FIELDS if name in envelope}


def outer_envelope_digest_and_preimage(envelope: dict[str, Any]) -> tuple[str, bytes]:
    """Compute the candidate C outer-envelope digest and Ed25519 preimage."""
    p0 = outer_envelope_p0(envelope)
    p0_bytes = rfc8785.dumps(p0)
    digest = hashlib.sha256(C_ENVELOPE_PAYLOAD_DOMAIN + p0_bytes).hexdigest()
    signed = dict(p0)
    signed["payload_digest"] = digest
    preimage = (
        C_ENVELOPE_SIGNATURE_DOMAIN
        + C_ENVELOPE_PROFILE_ID.encode("ascii") + bytes([0])
        + b"C_PROVIDER_OUTCOME_RECORDED" + bytes([0])
        + rfc8785.dumps(signed)
    )
    return digest, preimage


class ReplayDecision(str, Enum):
    NEW = "NEW"
    SAME_DIGEST_REPLAY = "SAME_DIGEST_REPLAY"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ReplayCheck:
    decision: ReplayDecision
    prior_result_ref: Optional[str] = None


@dataclass(frozen=True)
class ProtectedTransportContext:
    """Verifier-produced context; never construct this from envelope claims."""

    issuer_ref: str
    authority_ref: str
    authority_kind: str
    subject_ref: str
    audience: str
    runtime_session_ref: str
    authentication_context_ref: str
    channel_binding_proof_ref: str


@dataclass
class EnvelopeAuthChecks:
    # True = verified, False = authenticated contradiction, None = unavailable.
    verify_envelope_integrity: Optional[
        Callable[[bytes, dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_envelope_signature: Optional[
        Callable[[dict[str, Any], bytes, ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_key_status: Optional[
        Callable[[dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_channel_binding: Optional[
        Callable[[dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None
    verify_identity_binding: Optional[
        Callable[[dict[str, Any], ProtectedTransportContext], Optional[bool]]
    ] = None
    check_and_reserve_replay: Optional[
        Callable[[dict[str, Any], ProtectedTransportContext], ReplayCheck]
    ] = None


_REQUIRED_AUTH_FIELDS = (
    "schema_id",
    "schema_artifact_revision",
    "schema_version",
    "message_type",
    "message_id",
    "message_nonce",
    "audience",
    "issuer_ref",
    "sender_authority_ref",
    "sender_subject_ref",
    "subject_ref",
    "owner_authority",
    "canonicalization_profile_id",
    "signature_profile_id",
    "digest_algorithm",
    "payload_digest",
    "integrity_proof_ref",
    "channel_binding_proof_ref",
    "key_id_ref",
    "key_version",
    "signature",
)


def _call_bool(label: str, callback, args, invalid: list[str], unknown: list[str]) -> None:
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
        unknown.append(label + " returned an unsupported result")


def authenticate_outer_envelope(
    raw_envelope: bytes,
    protected_context: Optional[ProtectedTransportContext],
    checks: EnvelopeAuthChecks,
) -> dict[str, Any]:
    """Authenticate the outer H envelope before schema/domain acceptance."""
    try:
        envelope = parse_strict_json(raw_envelope)
    except (UnicodeDecodeError, DuplicateJSONKey, ValueError, TypeError) as exc:
        return {
            "status": "INVALID",
            "errors": [f"strict outer-envelope parse failed: {type(exc).__name__}"],
            "unknown": [],
        }

    missing = [
        name for name in _REQUIRED_AUTH_FIELDS
        if not isinstance(envelope.get(name), str) or not envelope.get(name)
    ]
    if missing:
        return {
            "status": "INVALID",
            "errors": ["missing or malformed outer-envelope security fields: " + ", ".join(missing)],
            "unknown": [],
        }

    try:
        computed_digest, signature_preimage = outer_envelope_digest_and_preimage(envelope)
    except Exception as exc:
        return {
            "status": "INVALID",
            "errors": ["outer-envelope P0/digest construction failed: " + type(exc).__name__ + ": " + str(exc)],
            "unknown": [],
        }
    if computed_digest != envelope.get("payload_digest"):
        return {
            "status": "INVALID",
            "errors": ["outer-envelope payload_digest mismatch"],
            "unknown": [],
        }

    if protected_context is None:
        return {
            "status": "UNKNOWN",
            "errors": [],
            "unknown": ["protected transport/session verifier context unavailable"],
        }

    # These are claim-to-protected-context comparisons, not authentication by
    # themselves. The protected context is supplied by the transport verifier.
    bindings = (
        ("issuer_ref", protected_context.issuer_ref),
        ("sender_authority_ref", protected_context.authority_ref),
        ("sender_subject_ref", protected_context.subject_ref),
        ("audience", protected_context.audience),
        ("channel_binding_proof_ref", protected_context.channel_binding_proof_ref),
    )
    invalid = [
        f"outer-envelope claim mismatch: {field}"
        for field, trusted_value in bindings
        if envelope.get(field) != trusted_value
    ]
    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": []}

    # C_PROVIDER_OUTCOME_RECORDED is a C-originated event. An H gateway
    # receipt may be additive, but cannot authenticate this C origin message.
    if protected_context.authority_kind != "C" or envelope.get("owner_authority") != "C":
        return {
            "status": "INVALID",
            "errors": ["C provider outcome requires an authenticated C origin principal"],
            "unknown": [],
        }

    unknown: list[str] = []
    if checks.verify_envelope_signature is not None:
        _call_bool(
            "outer envelope signature/profile",
            checks.verify_envelope_signature,
            (envelope, signature_preimage, protected_context),
            invalid,
            unknown,
        )
    else:
        _call_bool(
            "outer envelope signature/profile",
            checks.verify_envelope_integrity,
            (raw_envelope, envelope, protected_context),
            invalid,
            unknown,
        )
    _call_bool(
        "issuer key status / revocation / anti-rollback",
        checks.verify_key_status,
        (envelope, protected_context),
        invalid,
        unknown,
    )
    _call_bool(
        "protected channel binding",
        checks.verify_channel_binding,
        (envelope, protected_context),
        invalid,
        unknown,
    )
    _call_bool(
        "issuer/authority/principal registry binding",
        checks.verify_identity_binding,
        (envelope, protected_context),
        invalid,
        unknown,
    )

    # Do not reserve replay state for unauthenticated, contradictory or
    # unverifiable messages. Replay reservation is the final auth-stage step.
    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": unknown}
    if unknown:
        return {"status": "UNKNOWN", "errors": [], "unknown": unknown}

    replay_result: Optional[ReplayCheck] = None
    if checks.check_and_reserve_replay is None:
        unknown.append("durable replay/idempotency verifier not configured")
    else:
        try:
            replay_result = checks.check_and_reserve_replay(envelope, protected_context)
        except Exception:
            replay_result = ReplayCheck(ReplayDecision.UNKNOWN)
        if not isinstance(replay_result, ReplayCheck):
            replay_result = ReplayCheck(ReplayDecision.UNKNOWN)

        if replay_result.decision == ReplayDecision.CONFLICT:
            invalid.append("message identity/nonce reused with a different digest or binding")
        elif replay_result.decision == ReplayDecision.UNKNOWN:
            unknown.append("durable replay/idempotency state unavailable")
        elif replay_result.decision == ReplayDecision.SAME_DIGEST_REPLAY:
            if not replay_result.prior_result_ref:
                unknown.append("same-digest replay has no prior durable result reference")
        elif replay_result.decision != ReplayDecision.NEW:
            unknown.append("unsupported replay decision")

    if invalid:
        return {"status": "INVALID", "errors": invalid, "unknown": unknown}
    if unknown:
        return {"status": "UNKNOWN", "errors": [], "unknown": unknown}
    if replay_result and replay_result.decision == ReplayDecision.SAME_DIGEST_REPLAY:
        return {
            "status": "IDEMPOTENT_REPLAY",
            "errors": [],
            "unknown": [],
            "prior_result_ref": replay_result.prior_result_ref,
        }
    return {"status": "AUTHENTICATED_NEW", "errors": [], "unknown": [], "envelope": envelope}


def validate_authenticated_provider_outcome(
    raw_envelope: bytes,
    raw_c_object: bytes,
    protected_context: Optional[ProtectedTransportContext],
    envelope_auth_checks: EnvelopeAuthChecks,
    envelope_schema: dict,
    c_object_schema: dict,
    owner_checks: AuthorityChecks,
) -> dict[str, Any]:
    """Only the authenticated entrypoint may invoke Provider Outcome validation."""
    auth = authenticate_outer_envelope(raw_envelope, protected_context, envelope_auth_checks)
    if auth["status"] != "AUTHENTICATED_NEW":
        return auth

    try:
        c_object = parse_strict_json(raw_c_object)
    except (UnicodeDecodeError, DuplicateJSONKey, ValueError, TypeError) as exc:
        return {
            "status": "INVALID",
            "errors": [f"strict C-object parse failed: {type(exc).__name__}"],
            "unknown": [],
            "outer_envelope_authenticated": True,
        }

    result = validate_provider_outcome(
        auth["envelope"],
        c_object,
        envelope_schema,
        c_object_schema,
        owner_checks,
    )
    result["outer_envelope_authenticated"] = True
    return result
