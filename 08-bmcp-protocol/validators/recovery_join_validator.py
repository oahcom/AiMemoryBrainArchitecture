"""RecoveryJoin 1.0.2 structural and D-binding conformance reference.

This module does not claim production/runtime conformance. JSON Schema validation
checks message and proof structure only. The D-specific helpers check deterministic
cross-field bindings and require injected D-authoritative verification callbacks
for membership-proof authentication and ForgetFence currentness.

The H-RJ-HW-01 contract is a CANDIDATE DESIGN RECORD. In particular, D has not
supplied the authoritative namespace encoding, currentness-proof issuance format,
signature verifier, or currentness query interface. Without those callbacks the
result is UNKNOWN, never VALID.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "schemas"
    / "bmcp.recovery-join-1.0.2.schema.json"
)
SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

class DuplicateJSONMemberError(ValueError):
    """Raised when a JSON object repeats a member name."""


Verifier = Callable[[dict[str, Any]], bool | None]


def _reject_duplicate_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate member names at every JSON object depth."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONMemberError(f"duplicate JSON object member: {key}")
        result[key] = value
    return result


def _result(status: str, detail: str) -> dict[str, Any]:
    return {"status": status, "detail": detail}


def _fragment_errors(name: str, value: Any) -> list[Any]:
    wrapper = {
        "$schema": SCHEMA["$schema"],
        "$defs": SCHEMA["$defs"],
        "$ref": f"#/$defs/{name}",
    }
    return list(Draft202012Validator(wrapper).iter_errors(value))


def validate_recovery_join(raw_envelope: bytes | str) -> dict[str, Any]:
    """Validate JSON syntax and the RecoveryJoin envelope's structural schema.

    A successful result is STRUCTURALLY_VALID, not semantically VALID. D proof
    authentication and currentness are handled by the explicit D-binding helpers.
    """
    try:
        raw = raw_envelope.decode("utf-8") if isinstance(raw_envelope, bytes) else raw_envelope
        envelope = json.loads(raw, object_pairs_hook=_reject_duplicate_object_pairs)
    except DuplicateJSONMemberError as exc:
        return {"status": "INVALID", "errors": [str(exc)]}
    except Exception as exc:
        return {"status": "INVALID", "errors": [f"invalid JSON: {type(exc).__name__}"]}
    if not isinstance(envelope, dict):
        return {"status": "INVALID", "errors": ["RecoveryJoin envelope must be an object"]}

    errors = sorted(
        Draft202012Validator(SCHEMA).iter_errors(envelope),
        key=lambda error: list(error.path),
    )
    if errors:
        return {
            "status": "INVALID",
            "errors": [
                f"{'/'.join(map(str, error.path))}: {error.message}"
                for error in errors
            ],
        }
    return {"status": "STRUCTURALLY_VALID", "errors": []}


def validate_d_producer_registration_binding(
    proof: dict[str, Any],
    row: dict[str, Any],
    snapshot: dict[str, Any],
    verify_membership_proof: Verifier | None = None,
) -> dict[str, Any]:
    """Check D's typed ProducerRegistrationHighWater binding.

    The callback must authenticate the D-issued membership proof, including
    issuer/authority, signature profile, key status and ledger inclusion.
    """
    if not all(isinstance(value, dict) for value in (proof, row, snapshot)):
        return _result("INVALID", "proof, row and snapshot must be objects")
    if proof.get("owner_kind") != "D" or row.get("owner_kind") != "D":
        return _result("INVALID", "ProducerRegistrationHighWater binding is D-only")

    proof_required = (
        "owner_admission_ref", "owner_entry_ref", "owner_entry_digest",
        "owner_authority_ref", "owner_sequence_namespace", "owner_local_sequence", "owner_high_water",
        "owner_snapshot_ref", "owner_snapshot_digest", "owner_gate_ref",
        "owner_gate_generation", "scope_ref", "scope_generation",
        "operation_identity_ref", "operation_digest", "anti_rollback_anchor_ref",
        "producer_registration_sequence_namespace_ref",
        "producer_registration_high_water",
    )
    row_required = (
        "owner_admission_ref", "owner_entry_ref", "owner_admission_entry_digest",
        "owner_sequence_namespace", "owner_sequence", "gate_generation",
        "scope_ref", "scope_generation", "operation_identity_ref", "operation_digest",
    )
    missing_proof = [name for name in proof_required if name not in proof]
    missing_row = [name for name in row_required if name not in row]
    if missing_proof or missing_row:
        return _result(
            "INVALID",
            "membership proof or admission row is structurally incomplete: "
            + ", ".join(missing_proof + missing_row),
        )

    snapshot_required = (
        "owner_authority_ref", "snapshot_ref", "snapshot_digest", "gate_ref", "gate_generation",
        "scope_generation", "anti_rollback_anchor_ref", "producer_registration_sequence_namespace_ref",
        "producer_registration_high_water",
    )
    missing_snapshot = [name for name in snapshot_required if name not in snapshot]
    if missing_snapshot:
        return _result(
            "UNKNOWN",
            "D-authoritative snapshot material is unavailable: " + ", ".join(missing_snapshot),
        )

    for field, left, right in (
        ("owner_admission_ref", proof["owner_admission_ref"], row["owner_admission_ref"]),
        ("owner_entry_ref", proof["owner_entry_ref"], row["owner_entry_ref"]),
        ("owner_authority_ref", proof["owner_authority_ref"], snapshot["owner_authority_ref"]),
        ("scope_ref", proof["scope_ref"], row["scope_ref"]),
        ("scope_generation/row", proof["scope_generation"], row["scope_generation"]),
        ("scope_generation/snapshot", proof["scope_generation"], snapshot["scope_generation"]),
        ("operation_identity_ref", proof["operation_identity_ref"], row["operation_identity_ref"]),
        ("operation_digest", proof["operation_digest"], row["operation_digest"]),
        ("owner_gate_generation/row", proof["owner_gate_generation"], row["gate_generation"]),
        ("owner_entry_digest", proof["owner_entry_digest"], row["owner_admission_entry_digest"]),
        ("owner_sequence_namespace", proof["owner_sequence_namespace"], row["owner_sequence_namespace"]),
        ("owner_local_sequence", proof["owner_local_sequence"], row["owner_sequence"]),
        ("owner_snapshot_ref", proof["owner_snapshot_ref"], snapshot["snapshot_ref"]),
        ("owner_snapshot_digest", proof["owner_snapshot_digest"], snapshot["snapshot_digest"]),
        ("owner_gate_ref", proof["owner_gate_ref"], snapshot["gate_ref"]),
        ("owner_gate_generation", proof["owner_gate_generation"], snapshot["gate_generation"]),
        ("anti_rollback_anchor_ref", proof["anti_rollback_anchor_ref"], snapshot["anti_rollback_anchor_ref"]),
        (
            "producer_registration_sequence_namespace_ref",
            proof["producer_registration_sequence_namespace_ref"],
            snapshot["producer_registration_sequence_namespace_ref"],
        ),
    ):
        if left != right:
            return _result("INVALID", f"D binding mismatch: {field}")

    if proof["owner_sequence_namespace"] != proof["producer_registration_sequence_namespace_ref"]:
        return _result("INVALID", "D proof namespace differs from typed ProducerRegistration namespace")
    if proof["owner_high_water"] != proof["producer_registration_high_water"]:
        return _result("INVALID", "generic owner_high_water differs from typed ProducerRegistrationHighWater")
    if proof["producer_registration_high_water"] != snapshot["producer_registration_high_water"]:
        return _result("INVALID", "proof ProducerRegistrationHighWater differs from D snapshot")
    if not all(
        isinstance(value, str) and value.isascii() and value.isdecimal()
        and (value == "0" or not value.startswith("0"))
        for value in (
            proof["owner_local_sequence"],
            proof["owner_high_water"],
            proof["producer_registration_high_water"],
        )
    ):
        return _result("INVALID", "D ProducerRegistration counters must be canonical decimal strings")
    if int(proof["owner_local_sequence"]) > int(proof["producer_registration_high_water"]):
        return _result("INVALID", "owner_local_sequence exceeds ProducerRegistrationHighWater")

    if verify_membership_proof is None:
        return _result("UNKNOWN", "D membership-proof authority verifier was not supplied")
    try:
        verified = verify_membership_proof(proof)
    except Exception as exc:
        return _result("UNKNOWN", f"D membership-proof verifier exception: {type(exc).__name__}")
    if verified is True:
        return _result("VALID", "local typed bindings match and D membership proof was authenticated")
    if verified is False:
        return _result("INVALID", "D membership-proof authority verifier rejected the proof")
    return _result("UNKNOWN", "D membership-proof verifier returned an indeterminate result")


def validate_d_fence_evidence_binding(
    evidence: dict[str, Any],
    currentness_proof: dict[str, Any] | None,
    snapshot: dict[str, Any],
    verify_currentness_proof: Verifier | None = None,
) -> dict[str, Any]:
    """Check D ForgetFence tuple bindings and delegate authority/currentness.

    The callback must verify D issuance, proof signature, anti-rollback anchor,
    ledger currentness and the authoritative currentness query. Numeric ordering
    alone is explicitly insufficient to establish CURRENT.
    """
    if not isinstance(evidence, dict) or not isinstance(snapshot, dict):
        return _result("INVALID", "evidence and snapshot must be objects")
    if currentness_proof is None:
        return _result("UNKNOWN", "D ForgetFence currentness proof is unavailable")
    if not isinstance(currentness_proof, dict):
        return _result("INVALID", "D ForgetFence currentness proof must be an object")

    schema_errors = _fragment_errors("forgetFenceCurrentnessProof", currentness_proof)
    if schema_errors:
        return _result("INVALID", "malformed D currentness proof: " + schema_errors[0].message)

    evidence_required = (
        "forget_operation_ref", "fence_generation", "lineage_manifest_ref",
        "lineage_manifest_digest", "barrier_member_ref",
    )
    missing_evidence = [name for name in evidence_required if name not in evidence]
    if missing_evidence:
        return _result("INVALID", "D Forget evidence is structurally incomplete: " + ", ".join(missing_evidence))

    # These two fields are SHOULD-level in H-RJ-HW-01 §5.7, not MUST-level.
    # Their absence prevents a positive join but is not silently converted to INVALID.
    if "target_set_digest" not in evidence or "forget_fence_namespace_ref" not in evidence:
        return _result("UNKNOWN", "D evidence lacks SHOULD-level target-set or Fence namespace binding")

    snapshot_required = (
        "snapshot_ref", "snapshot_digest", "gate_generation",
        "anti_rollback_anchor_ref", "forget_fence_namespace_ref",
        "forget_fence_generation_high_water", "forget_fence_currentness_proof_ref",
        "forget_fence_currentness_proof_digest", "producer_registration_high_water",
    )
    missing_snapshot = [name for name in snapshot_required if name not in snapshot]
    if missing_snapshot:
        return _result("UNKNOWN", "D snapshot lacks currentness material: " + ", ".join(missing_snapshot))

    p = currentness_proof
    bindings = (
        ("proof_ref", p["proof_ref"], snapshot["forget_fence_currentness_proof_ref"]),
        ("proof_digest", p["proof_digest"], snapshot["forget_fence_currentness_proof_digest"]),
        ("owner_snapshot_ref", p["owner_snapshot_ref"], snapshot["snapshot_ref"]),
        ("owner_snapshot_digest", p["owner_snapshot_digest"], snapshot["snapshot_digest"]),
        ("owner_gate_generation", p["owner_gate_generation"], snapshot["gate_generation"]),
        ("anti_rollback_anchor_ref", p["anti_rollback_anchor_ref"], snapshot["anti_rollback_anchor_ref"]),
        ("forget_fence_namespace_ref", p["forget_fence_namespace_ref"], snapshot["forget_fence_namespace_ref"]),
        ("forget_fence_generation_high_water", p["forget_fence_generation_high_water"], snapshot["forget_fence_generation_high_water"]),
        ("producer_registration_high_water", p["producer_registration_high_water"], snapshot["producer_registration_high_water"]),
        ("forget_operation_ref", p["forget_operation_ref"], evidence["forget_operation_ref"]),
        ("target_set_digest", p["target_set_digest"], evidence["target_set_digest"]),
        ("forget_fence_namespace_ref/evidence", p["forget_fence_namespace_ref"], evidence["forget_fence_namespace_ref"]),
        ("forget_fence_generation", p["forget_fence_generation"], evidence["fence_generation"]),
    )
    for name, left, right in bindings:
        if left != right:
            return _result("INVALID", f"D ForgetFence binding mismatch: {name}")

    generation = p["forget_fence_generation"]
    high_water = p["forget_fence_generation_high_water"]
    for value in (generation, high_water):
        if not (
            isinstance(value, str) and value.isascii() and value.isdecimal()
            and (value == "0" or not value.startswith("0"))
        ):
            return _result("INVALID", "ForgetFenceGeneration values must be canonical decimal strings")
    if int(generation) > int(high_water):
        return _result("INVALID", "ForgetFenceGeneration exceeds its namespace high-water")

    # §5.8 adds this digest to the proof but does not settle requiredness.
    if "lineage_manifest_digest" not in p:
        return _result("UNKNOWN", "contract names lineage_manifest_digest but proof omitted the unresolved field")
    if p["lineage_manifest_digest"] != evidence["lineage_manifest_digest"]:
        return _result("INVALID", "lineage_manifest_digest differs between evidence and currentness proof")

    if p["currentness_status"] == "STALE":
        return _result("INVALID", "D currentness proof explicitly reports STALE")
    if p["currentness_status"] == "UNKNOWN":
        return _result("UNKNOWN", "D currentness proof explicitly reports UNKNOWN")
    if verify_currentness_proof is None:
        return _result("UNKNOWN", "D authoritative signature/currentness verifier was not supplied")
    try:
        verified = verify_currentness_proof(p)
    except Exception as exc:
        return _result("UNKNOWN", f"D currentness verifier exception: {type(exc).__name__}")
    if verified is True and p["currentness_status"] == "CURRENT":
        return _result("VALID", "D ForgetFence bindings match and authoritative verifier confirmed CURRENT")
    if verified is False:
        return _result("INVALID", "D authoritative currentness verifier rejected the proof")
    return _result("UNKNOWN", "D authoritative currentness verifier returned an indeterminate result")
