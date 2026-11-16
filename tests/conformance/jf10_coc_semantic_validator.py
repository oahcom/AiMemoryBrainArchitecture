"""Reference semantic validator for the JF-10 ↔ COC bridge.

This module validates cross-message invariants that JSON Schema cannot express.
It is deliberately dependency-free and does not verify cryptographic signatures,
COC quorum proofs, or owner-authoritative database lookups.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

MESSAGE_TYPES = (
    "JF10_PREPARE_INTENT_REGISTERED",
    "JF10_PREPARED_PARTICIPANT_REGISTERED",
    "I_JF10_TERMINAL_DECISION_OBSERVED",
    "STORAGE_JF10_PARTICIPANT_RESOLVED",
    "JF10_BRIDGE_RECONCILIATION_RECORDED",
)
COMMON = (
    "publication_operation_id", "request_digest", "owner_boundary",
    "participant_intent_ref", "policy_domain_ref", "storage_participant_ref",
    "storage_xid_ref", "participant_digest", "storage_authority_db_ref",
    "causal_order_coordinator_ref", "causal_order_domain_ref",
    "causal_order_transaction_ref",
)
IMMUTABLE = COMMON
TERMINAL_I = {"COMMIT_WON", "REVOCATION_WON", "INDETERMINATE_ABORTED"}
TERMINAL_STORAGE = {"COMMITTED", "ROLLED_BACK"}


class BridgeValidationError(ValueError):
    """Raised when a bridge message set violates a normative invariant."""


def _require(record: Mapping[str, Any], fields: Iterable[str], label: str) -> None:
    missing = [field for field in fields if field not in record or record[field] in (None, "")]
    if missing:
        raise BridgeValidationError(f"{label}: missing/empty fields: {', '.join(missing)}")


def _same_tuple(records: list[Mapping[str, Any]]) -> None:
    first = records[0]
    _require(first, IMMUTABLE, "immutable tuple")
    for index, record in enumerate(records[1:], 2):
        _require(record, IMMUTABLE, f"message {index} immutable tuple")
        changed = [key for key in IMMUTABLE if record[key] != first[key]]
        if changed:
            raise BridgeValidationError(
                f"message {index}: immutable tuple conflict: {', '.join(changed)}"
            )


def _one_policy_domain(record: Mapping[str, Any]) -> None:
    domains = record.get("policy_domain_refs")
    if domains is not None and (not isinstance(domains, list) or len(domains) != 1):
        raise BridgeValidationError("multi-policy-domain atomicity is unsupported")


def validate_bridge(messages: Iterable[Mapping[str, Any]]) -> dict[str, str]:
    """Validate one ordered bridge lifecycle and return its terminal summary.

    Input order is the COC lifecycle order, not a comparison of COC/I/D/Storage
    position values. Each authority's position remains opaque and independent.
    """
    records = list(messages)
    if len(records) != 5:
        raise BridgeValidationError("exactly five lifecycle observations are required")
    actual = [record.get("message_type") for record in records]
    if tuple(actual) != MESSAGE_TYPES:
        raise BridgeValidationError("lifecycle messages are missing, duplicated, or out of COC order")

    for index, record in enumerate(records, 1):
        _require(record, ("message_type", "message_id", "payload_digest"), f"message {index}")
        _one_policy_domain(record)
    _same_tuple(records)

    intent, prepared, i_decision, storage, reconciliation = records
    _require(intent, (
        "prepare_intent_state", "preallocated_storage_xid_ref",
        "prepare_intent_coc_position", "prepare_intent_entry_digest",
        "registration_commit_proof_ref",
    ), "prepare intent")
    if intent["prepare_intent_state"] != "REGISTERED":
        raise BridgeValidationError("prepare intent is not durably registered")
    if intent["preallocated_storage_xid_ref"] != intent["storage_xid_ref"]:
        raise BridgeValidationError("preallocated XID differs from immutable Storage XID")

    _require(prepared, (
        "prepared_participant_receipt_ref", "prepared_participant_receipt_digest",
        "storage_prepare_state", "storage_prepare_transaction_ref",
        "prepared_coc_position", "prepare_intent_coc_position",
        "prepare_intent_entry_digest", "storage_private_visibility_state",
        "storage_lock_retention_state", "registration_commit_proof_ref",
    ), "prepared participant")
    if prepared["storage_prepare_state"] != "PREPARED_DURABLE":
        raise BridgeValidationError("Storage participant is not durably prepared")
    if prepared["storage_prepare_transaction_ref"] != prepared["storage_xid_ref"]:
        raise BridgeValidationError("Storage prepared transaction is not the exact XID")
    if prepared["prepare_intent_coc_position"] != intent["prepare_intent_coc_position"] or prepared["prepare_intent_entry_digest"] != intent["prepare_intent_entry_digest"]:
        raise BridgeValidationError("prepared registration does not reference the exact prior intent")
    if prepared["storage_private_visibility_state"] != "NOT_VISIBLE" or prepared["storage_lock_retention_state"] != "RETAINED":
        raise BridgeValidationError("prepared participant must remain private and locked")

    _require(i_decision, (
        "i_authorization_terminal_ref", "i_receipt_consumption_proof_ref",
        "i_sequencer_ref", "i_sequencer_position", "i_decision_digest",
        "i_terminal_outcome", "i_revocation_request_state", "i_owner_signature_ref",
        "observed_coc_prepare_intent_position", "observed_coc_prepared_position",
    ), "I terminal decision observation")
    if i_decision["i_terminal_outcome"] not in TERMINAL_I:
        raise BridgeValidationError("I outcome is not terminal")
    if i_decision["i_revocation_request_state"] == "PRESENT":
        _require(i_decision, ("i_revocation_request_ref", "i_revocation_cutoff_proof_ref"), "I revocation evidence")
    elif i_decision["i_revocation_request_state"] == "NONE_AT_TERMINALIZATION":
        if "i_revocation_request_ref" in i_decision or "i_revocation_cutoff_proof_ref" in i_decision:
            raise BridgeValidationError("revocation references forbidden when state is NONE_AT_TERMINALIZATION")
    else:
        raise BridgeValidationError("invalid I revocation request state")
    if i_decision["observed_coc_prepare_intent_position"] != intent["prepare_intent_coc_position"] or i_decision["observed_coc_prepared_position"] != prepared["prepared_coc_position"]:
        raise BridgeValidationError("I observation does not bind both prior COC registrations")

    _require(storage, (
        "storage_resolution_outcome", "storage_resolution_transaction_ref",
        "storage_resolution_digest", "storage_owner_outcome_ref",
        "storage_owner_signature_ref", "storage_same_xid_proof_ref",
        "storage_visibility_state", "storage_lock_release_state",
    ), "Storage resolution")
    if storage["storage_resolution_outcome"] not in TERMINAL_STORAGE:
        raise BridgeValidationError("Storage outcome is not terminal")
    if storage["storage_resolution_transaction_ref"] != storage["storage_xid_ref"]:
        raise BridgeValidationError("Storage resolved a different XID")
    if storage["storage_lock_release_state"] != "RELEASED_AFTER_TERMINAL":
        raise BridgeValidationError("Storage locks released outside terminal resolution")
    if storage["storage_resolution_outcome"] == "COMMITTED":
        _require(storage, ("storage_publication_receipt_ref", "visibility_pointer_transaction_ref"), "Storage commit proof")
        if storage["visibility_pointer_transaction_ref"] != storage["storage_xid_ref"] or storage["storage_visibility_state"] != "VISIBLE":
            raise BridgeValidationError("COMMITTED lacks same-XID visibility publication")
        if "storage_nonpublication_proof_ref" in storage:
            raise BridgeValidationError("COMMITTED must not carry rollback non-publication proof")
    else:
        _require(storage, ("storage_nonpublication_proof_ref",), "Storage rollback proof")
        if storage["storage_visibility_state"] != "NOT_VISIBLE":
            raise BridgeValidationError("ROLLED_BACK must remain not visible")
        if "storage_publication_receipt_ref" in storage or "visibility_pointer_transaction_ref" in storage:
            raise BridgeValidationError("ROLLED_BACK must not carry publication evidence")

    _require(reconciliation, (
        "reconciliation_state", "i_lookup_state", "storage_lookup_state",
        "d_barrier_state", "reconciled_coc_prefix_position",
        "reconciliation_observation_ref",
    ), "reconciliation")
    if reconciliation["i_lookup_state"] != i_decision["i_terminal_outcome"]:
        raise BridgeValidationError("reconciliation I lookup conflicts with observed I terminal decision")
    if reconciliation["storage_lookup_state"] != storage["storage_resolution_outcome"]:
        raise BridgeValidationError("reconciliation Storage lookup conflicts with Storage resolution")
    if reconciliation["reconciliation_state"] == "RECONCILED_TERMINAL":
        if reconciliation["d_barrier_state"] != "SATISFIED":
            raise BridgeValidationError("terminal reconciliation requires authoritative satisfied D barrier")
    elif reconciliation["reconciliation_state"] in {"PENDING", "UNKNOWN"}:
        if reconciliation["d_barrier_state"] == "SATISFIED":
            raise BridgeValidationError("pending/unknown reconciliation cannot claim barrier satisfaction")
    else:
        raise BridgeValidationError("invalid reconciliation state")

    return {
        "i_outcome": str(i_decision["i_terminal_outcome"]),
        "storage_outcome": str(storage["storage_resolution_outcome"]),
        "reconciliation_state": str(reconciliation["reconciliation_state"]),
    }
