"""TEST-profile semantic reference for unified COC/JF-10 schema 1.2.9.

This module validates normalized evidence objects only. Digests are deterministic test
fixtures, not a production canonicalization, signature, quorum or trust profile.
"""
from __future__ import annotations
import hashlib
import json

VALID, INVALID, UNKNOWN = "VALID", "INVALID", "UNKNOWN"


def canonical_test_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def test_digest(domain, value):
    return hashlib.sha256(("BMCP-" + domain + "-TEST-v1|").encode("ascii")
                          + canonical_test_bytes(value)).hexdigest()


def owner_snapshot_root_projection(snapshot):
    fields = (
        "owner_snapshot_ref", "owner_snapshot_digest", "owner_snapshot_attestation_ref",
        "owner_snapshot_attestation_digest", "owner_gate_generation", "request_high_water",
        "admission_high_water", "request_ledger_root", "admission_ledger_root",
        "owner_ledger_root", "anti_rollback_anchor_ref", "owner_specific_high_waters_digest",
    )
    return {key: snapshot[key] for key in fields}


def manifest_content_projection(manifest):
    fields = (
        "manifest_id", "recovery_epoch_ref", "prefix", "enumeration_high_water",
        "coc_participant_count", "owner_local_admission_count", "manifest_member_count",
        "member_set_root", "owner_snapshot_roots", "manifest_members",
    )
    return {key: manifest[key] for key in fields}


def manifest_content_digest(manifest):
    return test_digest("MANIFEST-CONTENT", manifest_content_projection(manifest))


def member_key(member):
    kind = member.get("member_kind")
    if kind == "COC_PARTICIPANT":
        return ("0", member.get("participant_intent_ref", ""))
    if kind == "OWNER_LOCAL_ADMISSION":
        return ("1", member.get("owner_kind", "") + ":" + member.get("owner_admission_ref", ""))
    return ("9", "")


def validate_manifest_union(manifest, prefix_participants, owner_admissions,
                            owner_snapshots, pagination_complete=True):
    if not pagination_complete:
        return UNKNOWN
    if not isinstance(owner_snapshots, dict) or set(owner_snapshots) != {"I", "D", "C"}:
        return UNKNOWN
    for owner, snap in owner_snapshots.items():
        if not isinstance(snap, dict) or snap.get("owner") != owner:
            return INVALID
        if not snap.get("ledger_available") or not snap.get("pagination_complete"):
            return UNKNOWN
        for field in ("owner_snapshot_digest", "owner_snapshot_attestation_digest",
                      "request_ledger_root", "admission_ledger_root", "owner_ledger_root",
                      "owner_specific_high_waters_digest"):
            if not snap.get(field):
                return UNKNOWN

    members = manifest.get("manifest_members")
    if not isinstance(members, list):
        return INVALID
    if members != sorted(members, key=member_key):
        return INVALID
    if len({member_key(x) for x in members}) != len(members):
        return INVALID

    prefix_by_ref = {}
    for participant in prefix_participants:
        ref = participant.get("participant_intent_ref")
        if not ref or ref in prefix_by_ref:
            return INVALID
        prefix_by_ref[ref] = participant

    admissions_by_key = {}
    for admission in owner_admissions:
        owner = admission.get("owner_kind")
        ref = admission.get("owner_admission_ref")
        if owner not in {"I", "D", "C"} or not ref:
            return INVALID
        key = (owner, ref)
        if key in admissions_by_key:
            return INVALID
        snap = owner_snapshots[owner]
        try:
            seq, high = int(admission["owner_local_sequence"]), int(admission["owner_high_water"])
        except (KeyError, TypeError, ValueError):
            return INVALID
        if seq < 0 or seq > high:
            return INVALID
        if high > int(snap["admission_high_water"]):
            return UNKNOWN
        for f in ("owner_snapshot_ref", "owner_snapshot_digest",
                  "owner_snapshot_attestation_ref", "owner_snapshot_attestation_digest",
                  "owner_ledger_root"):
            expected = snap.get(f)
            if admission.get(f) != expected:
                return INVALID
        admissions_by_key[key] = admission

    coc_members = {}
    local_members = {}
    for member in members:
        kind = member.get("member_kind")
        if kind == "COC_PARTICIPANT":
            ref = member.get("participant_intent_ref")
            if not ref or ref in coc_members:
                return INVALID
            coc_members[ref] = member
        elif kind == "OWNER_LOCAL_ADMISSION":
            if member.get("coc_participant_intent_ref", "MISSING") is not None:
                return INVALID
            if not member.get("coc_absence_reason"):
                return INVALID
            key = (member.get("owner_kind"), member.get("owner_admission_ref"))
            if key in local_members:
                return INVALID
            local_members[key] = member
        else:
            return INVALID

    if set(coc_members) != set(prefix_by_ref):
        return INVALID

    for pref, participant in prefix_by_ref.items():
        member = coc_members[pref]
        for field in ("transaction_ref", "request_digest", "owner_boundary_ref",
                      "policy_domain_ref", "participant_tuple_digest", "participant_owner"):
            if member.get(field) != participant.get(field):
                return INVALID
        bindings = member.get("owner_admission_bindings")
        if not isinstance(bindings, list) or not bindings:
            return INVALID
        binding_keys = []
        for binding in bindings:
            key = (binding.get("owner_kind"), binding.get("owner_admission_ref"))
            admission = admissions_by_key.get(key)
            if admission is None or admission.get("coc_participant_intent_ref") != pref:
                return INVALID
            for field in ("owner_entry_ref", "owner_ledger_ref", "owner_ledger_version",
                          "owner_local_sequence", "owner_high_water", "owner_entry_digest",
                          "owner_ledger_root", "owner_snapshot_ref", "owner_snapshot_digest",
                          "owner_snapshot_attestation_ref", "owner_snapshot_attestation_digest",
                          "operation_digest", "scope_binding_digest"):
                if binding.get(field) != admission.get(field):
                    return INVALID
            if binding.get("coc_participant_intent_ref") != pref:
                return INVALID
            binding_keys.append(key)
        expected_keys = {key for key, value in admissions_by_key.items()
                         if value.get("coc_participant_intent_ref") == pref}
        if set(binding_keys) != expected_keys or len(binding_keys) != len(set(binding_keys)):
            return INVALID

    expected_local = {key for key, value in admissions_by_key.items()
                      if value.get("coc_participant_intent_ref") is None}
    if set(local_members) != expected_local:
        return INVALID
    for key, member in local_members.items():
        admission = admissions_by_key[key]
        for field in ("owner_kind", "owner_admission_ref", "owner_entry_ref",
                      "owner_ledger_ref", "owner_ledger_version", "owner_local_sequence",
                      "owner_high_water", "owner_entry_digest", "owner_ledger_root",
                      "owner_snapshot_ref", "owner_snapshot_digest",
                      "owner_snapshot_attestation_ref", "owner_snapshot_attestation_digest",
                      "operation_identity_ref", "operation_digest", "request_digest",
                      "scope_binding_digest", "admission_state", "effect_boundary",
                      "owner_entry_kind"):
            if member.get(field) != admission.get(field):
                return INVALID
    roots = manifest.get("owner_snapshot_roots")
    if not isinstance(roots, dict) or set(roots) != {"I", "D", "C"}:
        return INVALID
    for owner, snap in owner_snapshots.items():
        if roots.get(owner) != owner_snapshot_root_projection(snap):
            return INVALID

    coc_count = len(coc_members)
    local_count = len(local_members)
    if manifest.get("coc_participant_count") != coc_count:
        return INVALID
    if manifest.get("owner_local_admission_count") != local_count:
        return INVALID
    if manifest.get("manifest_member_count") != len(members) or len(members) != coc_count + local_count:
        return INVALID
    root = test_digest("MANIFEST-MEMBER-SET", members)
    if manifest.get("member_set_root") != root:
        return INVALID
    if manifest.get("manifest_content_digest") != manifest_content_digest(manifest):
        return INVALID
    return VALID


def validate_batch_manifest_pair(batch, manifest, batch_position,
                                 manifest_position, readback_linearizable=True):
    if not readback_linearizable:
        return UNKNOWN
    if batch.get("quorum_committed") is not True or manifest.get("quorum_committed") is not True:
        return UNKNOWN
    if tuple(manifest_position) <= tuple(batch_position):
        return INVALID
    if batch.get("message_type") != "COC_RECOVERY_CUTOFF_BATCH":
        return INVALID
    if manifest.get("message_type") != "PARTICIPANT_SET_RECONCILIATION":
        return INVALID
    if batch.get("schema_version") != "1.3.0" or manifest.get("schema_version") != "1.3.0":
        return INVALID
    for field in ("recovery_epoch_ref", "manifest_id", "manifest_content_digest",
                  "coc_participant_count", "owner_local_admission_count",
                  "manifest_member_count", "member_set_root", "prefix"):
        if batch.get(field) != manifest.get(field):
            return INVALID
    if manifest.get("batch_record_ref") != batch.get("coc_record_ref"):
        return INVALID
    if manifest.get("batch_position") != batch_position[1]:
        return INVALID
    if manifest.get("batch_entry_digest") != batch.get("coc_entry_digest"):
        return INVALID
    if manifest.get("manifest_content_digest") != manifest_content_digest(manifest):
        return INVALID
    if manifest.get("coc_entry_digest") != manifest.get("envelope_payload_digest"):
        return INVALID
    return VALID


def validate_owner_release(release, batch, manifest):
    if release.get("owner_kind") not in {"I", "D", "C"}:
        return INVALID
    if release.get("release_type") != "OUTAGE_ADMISSION_GATE_ONLY":
        return INVALID
    expected = {
        "batch_record_ref": batch.get("coc_record_ref"),
        "batch_entry_digest": batch.get("coc_entry_digest"),
        "manifest_record_ref": manifest.get("coc_record_ref"),
        "manifest_content_digest": manifest.get("manifest_content_digest"),
        "manifest_record_entry_digest": manifest.get("coc_entry_digest"),
    }
    for key, value in expected.items():
        if release.get(key) != value:
            return INVALID
    if release.get("final_currentness_cas_valid") is not True:
        return UNKNOWN
    return VALID


def validate_signature_profile(message, protected, trust_registry,
                               expected_owner, expected_audience, expected_purpose):
    if not protected:
        return VALID
    profile_id = message.get("signature_profile_id")
    if not profile_id:
        return INVALID
    if trust_registry is None:
        return UNKNOWN
    profile = trust_registry.get(profile_id)
    if profile is None or profile.get("status") != "ACTIVE":
        return INVALID
    expected = {
        "owner_authority": expected_owner,
        "audience": expected_audience,
        "purpose": expected_purpose,
        "wire_schema_version": "1.3.0",
    }
    if any(profile.get(k) != v for k, v in expected.items()):
        return INVALID
    if message.get("owner_authority") != expected_owner or message.get("audience") != expected_audience:
        return INVALID
    return VALID


def validate_provider_outcome(message):
    if message.get("message_type") != "C_PROVIDER_OUTCOME_RECORDED":
        return INVALID
    if message.get("owner_authority") != "C":
        return INVALID
    if not all(message.get(k) for k in ("c_submit_outcome_ref", "c_submit_outcome_digest",
                                        "owner_admission_ref", "owner_ledger_ref",
                                        "owner_ledger_version", "owner_local_sequence",
                                        "owner_high_water", "owner_ledger_root",
                                        "provider_ref", "provider_adapter_ref",
                                        "provider_idempotency_key_ref", "request_digest",
                                        "final_request_boundary_id", "provider_outcome_evidence_ref")):
        return UNKNOWN
    outcome = message.get("provider_outcome")
    if outcome == "HANDOFF_ACCEPTED":
        return VALID if all(message.get(k) for k in ("provider_request_ref", "provider_receipt_ref",
                                                     "participant_reservation_ref")) else INVALID
    if outcome == "HANDOFF_REJECTED":
        return VALID if all(message.get(k) for k in ("provider_no_handoff_proof_ref",
                                                     "participant_reservation_ref")) else INVALID
    if outcome == "NOT_INVOKED":
        if message.get("provider_receipt_ref") or not message.get("not_invoked_proof_ref"):
            return INVALID
        return VALID
    if outcome in {"UNKNOWN", "IN_DOUBT"}:
        return UNKNOWN if message.get("unknown_reason_ref") else INVALID
    return INVALID
