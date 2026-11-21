"""Strict semantic reference validator for BMCP Applied Delivery Evidence 1.0.0.

This module is a TEST/CONFORMANCE reference. It does not implement durable storage,
production key discovery, cryptographic trust, or an owner ledger. Those authorities
are injected and must return True/False/None (VALID/INVALID/UNKNOWN).
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "bmcp.applied-delivery-evidence-1.0.0.schema.json"
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
P0_EXCLUDED = frozenset({"payload_digest", "signature", "integrity_proof_ref"})
P0_FIELDS = tuple(name for name in SCHEMA["properties"] if name not in P0_EXCLUDED)
IDENTITY_FIELDS = (
    "issuer_ref", "sender_authority_ref", "sender_subject_ref", "message_id",
    "message_nonce", "signing_sequence_namespace_ref", "signing_record_sequence",
)
DELIVERY_BINDING_FIELDS = (
    "adapter_instance_ref", "runtime_session_ref", "delivery_id",
    "delivery_attempt_id", "inference_request_id", "final_request_boundary_id",
    "adapter_capability_epoch",
)


@dataclass(frozen=True)
class DurableObservationDecision:
    disposition: str
    original_result_ref: str | None = None


@dataclass
class AppliedDeliveryChecks:
    verify_profile_registration: Callable[[dict[str, Any]], bool | None]
    verify_key_status: Callable[[dict[str, Any]], bool | None]
    verify_signature: Callable[[dict[str, Any], bytes], bool | None]
    verify_protected_identity_binding: Callable[[dict[str, Any]], bool | None]
    verify_c_final_boundary: Callable[[dict[str, Any]], bool | None]
    verify_g_delivery_binding: Callable[[dict[str, Any]], bool | None]
    verify_capability_epoch: Callable[[dict[str, Any]], bool | None]
    commit_observation: Callable[[dict[str, Any], str], DurableObservationDecision]
    verify_current_i_replay_authorization: Callable[[dict[str, Any], str], bool | None]
    verify_current_d_forget_fence: Callable[[dict[str, Any], str], bool | None]
    resolve_c_submit_outcome: Callable[[str], dict[str, Any] | None]
    verify_c_submit_outcome_record: Callable[[dict[str, Any]], bool | None]


def _reject_duplicate_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build every JSON object while rejecting duplicate member names."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object member: {key}")
        result[key] = value
    return result


_RFC3339_DATETIME = re.compile(
    r"(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
    r"[Tt](?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
    r"(?:\.[0-9]+)?(?P<offset>[Zz]|[+-][0-9]{2}:[0-9]{2})"
)


def _valid_rfc3339_datetime(value: str) -> bool:
    """Validate RFC 3339 syntax and calendar ranges, not just its regex shape."""
    match = _RFC3339_DATETIME.fullmatch(value)
    if match is None:
        return False

    parts = {name: int(match.group(name)) for name in ("year", "month", "day", "hour", "minute", "second")}
    year, month, day = parts["year"], parts["month"], parts["day"]
    if not 1 <= month <= 12 or not 0 <= parts["hour"] <= 23:
        return False
    if parts["minute"] > 59 or parts["second"] > 60:
        return False

    leap_year = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days_in_month = (31, 29 if leap_year else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if not 1 <= day <= days_in_month[month - 1]:
        return False

    offset = match.group("offset")
    if offset not in ("Z", "z"):
        offset_hour, offset_minute = int(offset[1:3]), int(offset[4:6])
        if offset_hour > 23 or offset_minute > 59:
            return False
    return True


def build_h_p0(envelope: dict[str, Any]) -> dict[str, Any]:
    unknown = set(envelope) - set(P0_FIELDS) - P0_EXCLUDED
    if unknown:
        raise ValueError("unrecognized Applied Delivery Evidence members: " + ", ".join(sorted(unknown)))
    return {key: envelope[key] for key in P0_FIELDS if key in envelope}


def validate_c_submit_outcome_join(
    envelope: dict[str, Any],
    c_record: dict[str, Any],
) -> tuple[str | None, str | None]:
    """Check H's duplicated C identity fields against one resolved immutable C record.

    The resolver must resolve envelope.c_submit_outcome_ref to this exact record;
    the separate verifier authenticates C issuer/namespace, schema, signature and
    append-only ledger inclusion. C outcome semantics remain C-owned and are not
    reinterpreted here as a G Applied decision.
    """
    # Bind the resolver result to the exact opaque reference carried by H.
    # A resolver adapter must not be able to return a different valid C record.
    requested_ref = envelope.get("c_submit_outcome_ref")
    if not isinstance(requested_ref, str) or not requested_ref:
        return "INVALID", "H c_submit_outcome_ref must be a non-empty immutable C record reference"
    if c_record.get("record_ref") != requested_ref:
        return "INVALID", "resolved CSubmitOutcome record_ref does not equal H c_submit_outcome_ref"

    required = (
        "issuer_authority_ref", "sequence_namespace_ref", "record_ref",
        "record_sequence", "payload_digest", "FinalRequestBoundaryRef",
    )
    missing = [name for name in required if not isinstance(c_record.get(name), str) or not c_record[name]]
    if missing:
        return "INVALID", "resolved CSubmitOutcome missing immutable identity fields: " + ", ".join(missing)
    equalities = (
        ("c_outcome_record_ref", "record_ref"),
        ("c_outcome_record_sequence", "record_sequence"),
        ("c_outcome_payload_digest", "payload_digest"),
        ("final_request_boundary_id", "FinalRequestBoundaryRef"),
    )
    for h_field, c_field in equalities:
        if envelope[h_field] != c_record[c_field]:
            return "INVALID", f"H/C exact field mismatch: {h_field} != C.{c_field}"
    actual_request_id = c_record.get("ActualInferenceRequestId")
    if actual_request_id is not None and actual_request_id != envelope["inference_request_id"]:
        return "INVALID", "H/C exact field mismatch: inference_request_id != C.ActualInferenceRequestId"
    return None, None


def canonical_p0_bytes(envelope: dict[str, Any]) -> bytes:
    # Deterministic test reference only. Production must use the H-approved canonicalization profile.
    return json.dumps(build_h_p0(envelope), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _tri_state(name: str, callback: Callable[..., bool | None], *args: Any) -> tuple[str | None, str | None]:
    try:
        value = callback(*args)
    except Exception as exc:  # callback failure cannot become acceptance
        return "UNKNOWN", f"{name} verifier exception: {type(exc).__name__}"
    if value is True:
        return None, None
    if value is False:
        return "INVALID", f"{name} verifier rejected evidence"
    return "UNKNOWN", f"{name} verifier result is indeterminate"


def validate_applied_delivery_evidence(
    raw_envelope: bytes,
    schema: dict[str, Any],
    checks: AppliedDeliveryChecks,
) -> dict[str, Any]:
    try:
        envelope = json.loads(
            raw_envelope.decode("utf-8"),
            object_pairs_hook=_reject_duplicate_object_pairs,
        )
    except Exception as exc:
        return {"status": "INVALID", "errors": [f"invalid JSON: {type(exc).__name__}"], "unknown": []}
    if not isinstance(envelope, dict):
        return {"status": "INVALID", "errors": ["envelope must be an object"], "unknown": []}

    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(envelope), key=lambda e: list(e.path))
    if errors:
        return {"status": "INVALID", "errors": [f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors], "unknown": []}
    if not _valid_rfc3339_datetime(envelope["submission_observed_at"]):
        return {"status": "INVALID", "errors": ["submission_observed_at: invalid RFC3339 calendar/time value"], "unknown": []}

    if envelope["evidence_tier"] == "TIER_1":
        if envelope["managed_region_coverage"] != "COMPLETE":
            return {"status": "INVALID", "errors": ["Tier 1 requires COMPLETE managed-region coverage"], "unknown": []}
        if envelope["materialized_context_version"] != envelope["context_version"]:
            return {"status": "INVALID", "errors": ["materialized_context_version differs from G context_version"], "unknown": []}
    if envelope["evidence_kind"] == "FINAL_REQUEST_SUBMITTED":
        if envelope.get("submission_monotonic_sequence") is None:
            return {"status": "INVALID", "errors": ["final-request evidence requires submission_monotonic_sequence"], "unknown": []}

    try:
        p0 = canonical_p0_bytes(envelope)
        digest = hashlib.sha256(p0).hexdigest()
    except Exception as exc:
        return {"status": "INVALID", "errors": [f"P0 construction failed: {type(exc).__name__}"], "unknown": []}
    if digest != envelope["payload_digest"]:
        return {"status": "INVALID", "errors": ["payload_digest mismatch"], "unknown": []}

    unknown = []
    for name, callback in (
        ("profile registration", checks.verify_profile_registration),
        ("key status", checks.verify_key_status),
        ("signature", checks.verify_signature),
        ("protected identity binding", checks.verify_protected_identity_binding),
        ("C final boundary", checks.verify_c_final_boundary),
        ("G delivery binding", checks.verify_g_delivery_binding),
        ("Adapter capability epoch", checks.verify_capability_epoch),
    ):
        status, detail = _tri_state(name, callback, envelope, p0) if name == "signature" else _tri_state(name, callback, envelope)
        if status == "INVALID":
            return {"status": "INVALID", "errors": [detail], "unknown": unknown}
        if status == "UNKNOWN":
            unknown.append(detail)

    if unknown:
        return {"status": "UNKNOWN", "errors": [], "unknown": unknown, "h_p0_digest": digest}

    # Resolve and authenticate the immutable C-owned outcome before H observation
    # acceptance. H verifies the join; it never mints or reinterprets C provider truth.
    try:
        c_record = checks.resolve_c_submit_outcome(envelope["c_submit_outcome_ref"])
    except Exception as exc:
        return {"status": "UNKNOWN", "errors": [], "unknown": [f"CSubmitOutcome resolver exception: {type(exc).__name__}"]}
    if c_record is None:
        return {"status": "UNKNOWN", "errors": [], "unknown": ["CSubmitOutcome resolver unavailable or record not yet visible"]}
    if not isinstance(c_record, dict):
        return {"status": "INVALID", "errors": ["CSubmitOutcome resolver returned a non-object record"], "unknown": []}
    status, detail = _tri_state("CSubmitOutcome authentication", checks.verify_c_submit_outcome_record, c_record)
    if status == "INVALID":
        return {"status": "INVALID", "errors": [detail], "unknown": []}
    if status == "UNKNOWN":
        return {"status": "UNKNOWN", "errors": [], "unknown": [detail], "h_p0_digest": digest}
    status, detail = validate_c_submit_outcome_join(envelope, c_record)
    if status == "INVALID":
        return {"status": "INVALID", "errors": [detail], "unknown": []}

    try:
        decision = checks.commit_observation(envelope, digest)
    except Exception as exc:
        return {"status": "UNKNOWN", "errors": [], "unknown": [f"durable observation commit indeterminate: {type(exc).__name__}"]}
    if decision.disposition == "CONFLICT":
        return {"status": "INVALID", "errors": ["observation identity reused with changed digest or immutable tuple"], "unknown": []}
    if decision.disposition == "SAME_DIGEST_REPLAY":
        if not decision.original_result_ref:
            return {"status": "UNKNOWN", "errors": [], "unknown": ["same-digest replay lacks original durable result reference"]}
        # A historical replay result is not perpetual authorization to disclose it.
        # Recheck current I authorization/epoch, key status, audience/scope and the
        # applicable D fence through the owner-authority adapter before disclosure.
        currentness_results = (
            ("current I replay authorization", checks.verify_current_i_replay_authorization),
            ("current D ForgetFence", checks.verify_current_d_forget_fence),
        )
        replay_unknown = []
        for name, callback in currentness_results:
            status, detail = _tri_state(name, callback, envelope, decision.original_result_ref)
            if status == "INVALID":
                return {"status": "INVALID", "errors": [detail], "unknown": []}
            if status == "UNKNOWN":
                replay_unknown.append(detail)
        if replay_unknown:
            return {"status": "UNKNOWN", "errors": [], "unknown": replay_unknown, "h_p0_digest": digest}
        return {"status": "VALID_REPLAY", "errors": [], "unknown": [], "original_result_ref": decision.original_result_ref, "h_p0_digest": digest}
    if decision.disposition != "NEW":
        return {"status": "UNKNOWN", "errors": [], "unknown": [f"unsupported durable disposition: {decision.disposition}"]}
    return {"status": "VALID_NEW", "errors": [], "unknown": [], "h_p0_digest": digest}


def observation_identity(envelope: dict[str, Any]) -> tuple[str, ...]:
    return tuple(envelope[field] for field in IDENTITY_FIELDS)


def delivery_binding_identity(envelope: dict[str, Any]) -> tuple[str, ...]:
    return tuple(envelope[field] for field in DELIVERY_BINDING_FIELDS)