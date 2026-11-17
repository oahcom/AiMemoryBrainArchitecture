"""Fail-closed H outer-envelope authentication gate.

This is a reference integration boundary, not a production cryptographic
implementation. Trust, key status, channel binding, identity registry and
replay state are supplied by protected verifier callbacks. Missing callbacks
or unavailable authority state never become authenticated success.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional

from provider_outcome_validator import (
    AuthorityChecks,
    DuplicateJSONKey,
    parse_strict_json,
    validate_provider_outcome,
)


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
    "message_id",
    "message_nonce",
    "audience",
    "issuer_ref",
    "sender_authority_ref",
    "sender_subject_ref",
    "subject_ref",
    "owner_authority",
    "canonicalization_profile_id",
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

    unknown: list[str] = []
    _call_bool(
        "outer envelope canonical digest/signature/profile",
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
