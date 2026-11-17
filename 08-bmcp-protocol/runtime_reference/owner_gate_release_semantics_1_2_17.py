"""TEST-profile semantic validator for H Unified 1.2.17 Owner Gate Release.

This reference function checks exact owner-snapshot, Batch/Manifest and
currentness bindings. Signature, COC quorum and owner-currentness verification
are injected callbacks. It is not production crypto or a live-ledger adapter.
"""
from __future__ import annotations

import hashlib
import json
from typing import Callable, Mapping

VALID, INVALID, UNKNOWN = "VALID", "INVALID", "UNKNOWN"


def _td(domain: str, value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(("BMCP-" + domain + "-TEST-v1|").encode("ascii") + raw).hexdigest()


def owner_reconciliation_root(manifest: Mapping, owner: str) -> str:
    projected = []
    for member in manifest.get("manifest_members", []):
        if member.get("member_kind") == "COC_PARTICIPANT":
            bindings = [
                binding for binding in member.get("owner_admission_bindings", [])
                if binding.get("owner_kind") == owner
            ]
            if bindings:
                projected.append({
                    "participant_intent_ref": member.get("participant_intent_ref"),
                    "owner_admission_bindings": bindings,
                })
        elif member.get("member_kind") == "OWNER_LOCAL_ADMISSION" and member.get("owner_kind") == owner:
            projected.append(member)
    return _td("OWNER-RECONCILIATION", projected)



def owner_snapshot_root_projection(snapshot: Mapping) -> dict:
    fields = (
        "owner_snapshot_ref", "owner_snapshot_digest",
        "owner_snapshot_attestation_ref", "owner_snapshot_attestation_digest",
        "owner_gate_generation", "scope_generation_ref",
        "request_high_water", "admission_high_water",
        "request_ledger_root", "admission_ledger_root", "owner_ledger_root",
        "anti_rollback_anchor_ref", "owner_specific_high_waters_digest",
    )
    return {field: snapshot.get(field) for field in fields}


def validate_owner_gate_release(
    release: Mapping,
    batch: Mapping,
    manifest: Mapping,
    owner_snapshot: Mapping,
    *,
    verify_owner_signature: Callable | None = None,
    verify_coc_commit_proof: Callable | None = None,
    currentness_cas: Callable | None = None,
) -> str:
    """Validate one release against exact source records and live owner currentness.

    Missing authoritative verifiers/currentness sources return UNKNOWN.
    Explicit immutable binding mismatch or verifier denial returns INVALID.
    """
    if not all(isinstance(x, Mapping) for x in (release, batch, manifest, owner_snapshot)):
        return UNKNOWN

    required = (
        "message_type", "owner_kind", "release_type", "owner_gate_ref", "owner_gate_generation",
        "recovery_epoch_ref", "batch_record_ref", "batch_digest", "manifest_record_ref",
        "owner_request_high_water", "owner_admission_high_water", "request_set_digest",
        "admission_set_digest", "request_ledger_root", "admission_ledger_root",
        "reconciliation_root", "owner_signature_ref", "coc_commit_proof_ref",
        "batch_position", "batch_entry_digest", "manifest_record_position",
        "manifest_record_entry_digest", "manifest_content_digest",
        "owner_snapshot_ref", "owner_snapshot_digest", "owner_snapshot_attestation_ref",
        "owner_snapshot_attestation_digest", "owner_ledger_root", "scope_generation_ref",
        "anti_rollback_anchor_ref", "owner_specific_high_waters",
        "owner_specific_high_waters_digest",
    )
    if any(k not in release or release[k] is None or release[k] == "" for k in required):
        return UNKNOWN
    if release.get("message_type") != "OWNER_LOCAL_GATE_RELEASE":
        return INVALID
    owner = release.get("owner_kind")
    if owner not in {"I", "D", "C"} or owner_snapshot.get("owner") != owner:
        return INVALID
    if release.get("release_type") != "OUTAGE_ADMISSION_RELEASE_ONLY":
        return INVALID

    # Exact owner snapshot binding.
    pairs = {
        "owner_gate_ref": "owner_gate_ref",
        "owner_gate_generation": "owner_gate_generation",
        "owner_request_high_water": "request_high_water",
        "owner_admission_high_water": "admission_high_water",
        "request_set_digest": "request_set_digest",
        "admission_set_digest": "admission_set_digest",
        "request_ledger_root": "request_ledger_root",
        "admission_ledger_root": "admission_ledger_root",
        "owner_snapshot_ref": "owner_snapshot_ref",
        "owner_snapshot_digest": "owner_snapshot_digest",
        "owner_snapshot_attestation_ref": "owner_snapshot_attestation_ref",
        "owner_snapshot_attestation_digest": "owner_snapshot_attestation_digest",
        "owner_ledger_root": "owner_ledger_root",
        "scope_generation_ref": "scope_generation_ref",
        "anti_rollback_anchor_ref": "anti_rollback_anchor_ref",
        "owner_specific_high_waters_digest": "owner_specific_high_waters_digest",
    }
    if any(release.get(out_key) != owner_snapshot.get(snapshot_key) for out_key, snapshot_key in pairs.items()):
        return INVALID
    if release.get("owner_specific_high_waters") != owner_snapshot.get("owner_specific_high_waters"):
        return INVALID
    if not isinstance(release.get("owner_specific_high_waters"), Mapping):
        return INVALID

    # The Batch and Manifest must carry this exact same frozen owner snapshot.
    batch_snapshots = batch.get("owner_snapshots")
    if not isinstance(batch_snapshots, Mapping) or owner not in batch_snapshots:
        return UNKNOWN
    if not isinstance(batch_snapshots[owner], Mapping):
        return INVALID
    if dict(batch_snapshots[owner]) != dict(owner_snapshot):
        return INVALID

    manifest_roots = manifest.get("owner_snapshot_roots")
    if not isinstance(manifest_roots, Mapping) or owner not in manifest_roots:
        return UNKNOWN
    if not isinstance(manifest_roots[owner], Mapping):
        return INVALID
    if dict(manifest_roots[owner]) != owner_snapshot_root_projection(owner_snapshot):
        return INVALID

    # Exact Recovery Cutoff Batch / Manifest pair binding.
    if release.get("recovery_epoch_ref") != batch.get("recovery_epoch_ref"):
        return INVALID
    if release.get("recovery_epoch_ref") != manifest.get("recovery_epoch_ref"):
        return INVALID
    pair_fields = (
        "batch_record_ref", "batch_position", "batch_entry_digest",
        "manifest_id", "manifest_content_digest", "enumeration_high_water",
        "coc_participant_count", "owner_local_admission_count",
        "manifest_member_count", "member_set_root", "prefix",
    )
    batch_to_manifest = {
        "batch_record_ref": batch.get("coc_record_ref"),
        "batch_position": batch.get("coc_record_position"),
        "batch_entry_digest": batch.get("coc_entry_digest"),
        "manifest_id": batch.get("manifest_id"),
        "manifest_content_digest": batch.get("manifest_content_digest"),
        "enumeration_high_water": batch.get("enumeration_high_water"),
        "coc_participant_count": batch.get("coc_participant_count"),
        "owner_local_admission_count": batch.get("owner_local_admission_count"),
        "manifest_member_count": batch.get("manifest_member_count"),
        "member_set_root": batch.get("member_set_root"),
        "prefix": batch.get("prefix"),
    }
    if any(field not in manifest or manifest.get(field) is None for field in pair_fields):
        return UNKNOWN
    for field, expected in batch_to_manifest.items():
        if expected is None:
            return UNKNOWN
        actual = manifest.get(field)
        if field == "batch_position":
            if str(actual) != str(expected):
                return INVALID
        elif actual != expected:
            return INVALID
    try:
        batch_position = int(batch.get("coc_record_position"))
        manifest_position = int(manifest.get("coc_record_position"))
    except (TypeError, ValueError):
        return UNKNOWN
    if batch_position >= manifest_position:
        return INVALID
    if release.get("batch_record_ref") != batch.get("coc_record_ref"):
        return INVALID
    if release.get("batch_digest") != batch.get("payload_digest"):
        return INVALID
    if str(release.get("batch_position")) != str(batch.get("coc_record_position")):
        return INVALID
    if release.get("batch_entry_digest") != batch.get("coc_entry_digest"):
        return INVALID
    if release.get("manifest_record_ref") != manifest.get("coc_record_ref"):
        return INVALID
    if str(release.get("manifest_record_position")) != str(manifest.get("coc_record_position")):
        return INVALID
    if release.get("manifest_record_entry_digest") != manifest.get("coc_entry_digest"):
        return INVALID
    if release.get("manifest_content_digest") != manifest.get("manifest_content_digest"):
        return INVALID

    try:
        expected_root = owner_reconciliation_root(manifest, owner)
    except Exception:
        return UNKNOWN
    if release.get("reconciliation_root") != expected_root:
        return INVALID

    # All authority checks are independent; absence/uncertainty is UNKNOWN.
    if not callable(verify_owner_signature) or not callable(verify_coc_commit_proof) or not callable(currentness_cas):
        return UNKNOWN
    try:
        owner_sig = verify_owner_signature(release, owner_snapshot)
    except Exception:
        return UNKNOWN
    if owner_sig is None or owner_sig == UNKNOWN:
        return UNKNOWN
    if owner_sig is not True:
        return INVALID
    try:
        coc_proof = verify_coc_commit_proof(release, batch, manifest)
    except Exception:
        return UNKNOWN
    if coc_proof is None or coc_proof == UNKNOWN:
        return UNKNOWN
    if coc_proof is not True:
        return INVALID
    try:
        current = currentness_cas(owner, owner_snapshot)
    except Exception:
        return UNKNOWN
    if current is None or current == UNKNOWN:
        return UNKNOWN
    if current is not True:
        return INVALID
    return VALID
