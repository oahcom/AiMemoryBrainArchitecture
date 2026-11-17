"""TEST-PROFILE semantic validator for the Recovery Cutoff 1.0.5 two-record protocol.

This module is executable reference logic, not production cryptography, quorum verification,
or authoritative ledger access. The digest profile is deliberately test-only until I/H
approve the canonical-byte and trust profile.
"""
from __future__ import annotations

import hashlib
import json

VALID = "VALID"
INVALID = "INVALID"
UNKNOWN = "UNKNOWN"
FENCED = "FENCED"
RECONCILIATION_ALLOWED = "RECONCILIATION_ALLOWED"


def canonical_test_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(domain, value):
    return hashlib.sha256(("BMCP-" + domain + "-TEST-v1\\0").encode("ascii")
                          + canonical_test_bytes(value)).hexdigest()


def participant_content_projection(manifest):
    fields = (
        "message_id", "recovery_epoch_ref", "prefix_term", "prefix_index",
        "prefix_root", "previous_prefix_digest", "enumeration_status",
        "participant_count", "participant_set_root", "participant_entries",
    )
    return {key: manifest[key] for key in fields}


def participant_content_digest(manifest):
    return digest("PARTICIPANT-MANIFEST-CONTENT",
                  participant_content_projection(manifest))


def recovery_batch_projection(batch):
    excluded = {"batch_digest", "quorum_commit_proof_ref", "envelope",
                "quorum_commit_proof_valid"}
    return {key: value for key, value in batch.items() if key not in excluded}


def recovery_batch_digest(batch):
    return digest("RECOVERY-CUTOFF-BATCH", recovery_batch_projection(batch))


def participant_manifest_record_projection(manifest):
    fields = (
        "schema_id", "schema_version", "message_type", "message_id",
        "recovery_epoch_ref", "prefix_term", "prefix_index", "prefix_root",
        "enumeration_status", "participant_count", "participant_set_root",
        "previous_prefix_digest", "participant_entries", "recovery_batch_ref",
        "recovery_batch_digest", "participant_manifest_content_digest",
    )
    return {key: manifest[key] for key in fields}


def participant_manifest_record_digest(manifest):
    return digest("PARTICIPANT-MANIFEST-RECORD",
                  participant_manifest_record_projection(manifest))


def _valid_digest(value):
    return isinstance(value, str) and len(value) == 64 and all(
        char in "0123456789abcdef" for char in value
    )


def validate_batch_manifest_pair(batch, manifest, batch_position,
                                 manifest_position, linearizable_readback=True,
                                 prefix_enumeration_complete=True):
    """Validate the ordered two-record pair using an explicitly TEST-only digest profile."""
    if not isinstance(batch, dict) or not isinstance(manifest, dict):
        return UNKNOWN
    if not linearizable_readback or not prefix_enumeration_complete:
        return UNKNOWN
    if batch.get("quorum_commit_proof_valid") is not True:
        return UNKNOWN
    if manifest.get("quorum_commit_proof_valid") is not True:
        return UNKNOWN

    if batch.get("schema_version") != "1.0.5" or manifest.get("schema_version") != "1.0.5":
        return INVALID
    if batch.get("message_type") != "RECOVERY_CUTOFF_BATCH":
        return INVALID
    if manifest.get("message_type") != "COC_PARTICIPANT_MANIFEST":
        return INVALID
    if not isinstance(batch_position, (tuple, list)) or not isinstance(manifest_position, (tuple, list)):
        return INVALID
    if len(batch_position) != 2 or len(manifest_position) != 2:
        return INVALID
    if tuple(manifest_position) <= tuple(batch_position):
        return INVALID

    if batch.get("participant_manifest_ref") != manifest.get("message_id"):
        return INVALID
    if batch.get("participant_manifest_content_digest") != manifest.get("participant_manifest_content_digest"):
        return INVALID
    if manifest.get("recovery_batch_ref") != batch.get("message_id"):
        return INVALID
    if manifest.get("recovery_batch_digest") != batch.get("batch_digest"):
        return INVALID

    for key in ("recovery_epoch_ref", "prefix_term", "prefix_index", "prefix_root"):
        if batch.get(key) != manifest.get(key):
            return INVALID

    entries = manifest.get("participant_entries")
    if not isinstance(entries, list):
        return INVALID
    if manifest.get("participant_count") != len(entries):
        return INVALID
    expected_status = "COMPLETE_EMPTY" if not entries else "COMPLETE_NON_EMPTY"
    if manifest.get("enumeration_status") != expected_status:
        return INVALID
    if manifest.get("participant_set_root") != digest("PARTICIPANT-SET", entries):
        return INVALID

    refs = [entry.get("participant_intent_ref") for entry in entries if isinstance(entry, dict)]
    if len(refs) != len(entries) or any(not ref for ref in refs) or len(refs) != len(set(refs)):
        return INVALID
    for entry in entries:
        if entry.get("prefix_term") != manifest.get("prefix_term"):
            return INVALID
        if entry.get("prefix_index", 0) > manifest.get("prefix_index", -1):
            return INVALID
        if not entry.get("owner_admission_ref") or not _valid_digest(entry.get("entry_digest")):
            return INVALID

    content_digest = participant_content_digest(manifest)
    if not _valid_digest(content_digest) or content_digest != manifest.get("participant_manifest_content_digest"):
        return INVALID
    if content_digest != batch.get("participant_manifest_content_digest"):
        return INVALID

    if not _valid_digest(batch.get("batch_digest")):
        return INVALID
    if recovery_batch_digest(batch) != batch.get("batch_digest"):
        return INVALID

    record_digest = participant_manifest_record_digest(manifest)
    if not _valid_digest(record_digest):
        return INVALID
    envelope = manifest.get("envelope")
    if not isinstance(envelope, dict) or envelope.get("payload_digest") != record_digest:
        return INVALID
    return VALID


def validate_owner_gate_release(release, batch, manifest):
    if not all(isinstance(x, dict) for x in (release, batch, manifest)):
        return UNKNOWN
    if release.get("owner_kind") not in {"I", "D", "C"}:
        return INVALID
    if release.get("release_kind") != "OUTAGE_ADMISSION_RELEASE_ONLY":
        return INVALID
    expected = {
        "recovery_batch_ref": batch.get("message_id"),
        "recovery_batch_digest": batch.get("batch_digest"),
        "participant_manifest_content_digest": manifest.get("participant_manifest_content_digest"),
        "participant_manifest_record_digest": participant_manifest_record_digest(manifest),
    }
    for key, value in expected.items():
        if release.get(key) != value:
            return INVALID
    if release.get("final_currentness_cas_valid") is not True:
        return UNKNOWN
    return VALID


def validate_recovery_epoch_completed(completed, batch, manifest, releases):
    if not all(isinstance(x, dict) for x in (completed, batch, manifest)):
        return UNKNOWN
    if not isinstance(releases, dict) or set(releases) != {"I", "D", "C"}:
        return INVALID
    for owner, release in releases.items():
        if release.get("owner_kind") != owner:
            return INVALID
        if validate_owner_gate_release(release, batch, manifest) != VALID:
            return UNKNOWN
    expected = {
        "final_batch_ref": batch.get("message_id"),
        "final_batch_digest": batch.get("batch_digest"),
        "participant_manifest_content_digest": manifest.get("participant_manifest_content_digest"),
        "participant_manifest_record_digest": participant_manifest_record_digest(manifest),
    }
    for key, value in expected.items():
        if completed.get(key) != value:
            return INVALID
    refs = completed.get("required_owner_release_refs")
    if not isinstance(refs, list) or len(refs) != 3 or len(set(refs)) != 3:
        return INVALID
    if completed.get("all_rounds_root") is None or completed.get("quorum_commit_proof_valid") is not True:
        return UNKNOWN
    return VALID


def recovery_state(batch_committed, manifest_committed, staged_content_available,
                   pair_readback_verified):
    """Return the only safe recovery phase for the two-record commit sequence."""
    if not batch_committed:
        return FENCED
    if not manifest_committed:
        return FENCED
    if not staged_content_available:
        return FENCED
    if not pair_readback_verified:
        return FENCED
    return RECONCILIATION_ALLOWED
