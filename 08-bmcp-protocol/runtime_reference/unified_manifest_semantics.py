"""TEST-profile reference validators for unified BMCP manifest 1.2.9."""
import hashlib
import json
import re

VALID, INVALID, UNKNOWN = "VALID", "INVALID", "UNKNOWN"


def td(domain, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(("BMCP-" + domain + "-TEST-v1|").encode("ascii") + raw).hexdigest()


def snapshot_root(s):
    keys = ("owner_snapshot_ref","owner_snapshot_digest","owner_snapshot_attestation_ref",
            "owner_snapshot_attestation_digest","owner_gate_generation","request_high_water",
            "admission_high_water","request_ledger_root","admission_ledger_root","owner_ledger_root",
            "anti_rollback_anchor_ref","owner_specific_high_waters_digest")
    return {k:s[k] for k in keys}


def content_projection(m):
    keys = ("manifest_id","recovery_epoch_ref","prefix","enumeration_high_water",
            "coc_participant_count","owner_local_admission_count","manifest_member_count",
            "member_set_root","owner_snapshot_roots","manifest_members")
    return {k:m[k] for k in keys}


def content_digest(m):
    return td("MANIFEST-CONTENT", content_projection(m))


def member_key(m):
    if m.get("member_kind") == "COC_PARTICIPANT":
        return ("0", m.get("participant_intent_ref",""))
    if m.get("member_kind") == "OWNER_LOCAL_ADMISSION":
        return ("1", m.get("owner_kind","")+":"+m.get("owner_admission_ref",""))
    return ("9","")


def validate_owner_snapshot(
    snapshot, owner, allow_legacy_d_snapshot=False, schema_artifact_revision="1.2.9"
):
    # Keep the 1.2.9 wire contract closed-world by default. 1.2.17 callers
    # must opt into its distinct I/C field sets explicitly.
    if schema_artifact_revision == "1.2.9":
        i_fields = {
            "receipt_issue_high_water", "receipt_consume_high_water", "inventory_epoch_ref",
            "registry_snapshot_digest", "relevant_entry_set_root",
        }
        c_fields = {
            "reservation_high_water", "provider_attempt_high_water", "provider_outcome_high_water",
        }
    elif schema_artifact_revision == "1.2.17":
        i_fields = {
            "receipt_issue_high_water", "receipt_consume_high_water", "permission_epoch",
            "producer_domain_inventory_epoch_ref", "registry_snapshot_digest", "relevant_entry_set_root",
        }
        c_fields = {
            "reservation_high_water", "provider_attempt_high_water", "provider_outcome_high_water",
            "provider_idempotency_namespace_ref", "final_request_boundary_generation",
        }
    else:
        return INVALID
    fields={
      "I": i_fields,
      "D":{"producer_registration_high_water","work_item_high_water","attempt_high_water",
           "barrier_generation","barrier_root","forget_fence_generation_high_water",
           "dependency_closure_cursor","dependency_closure_root"},
      "C": c_fields,
    }
    if owner not in fields or snapshot.get("owner")!=owner:
        return INVALID
    values=snapshot.get("owner_specific_high_waters")
    if not isinstance(values,dict):
        return INVALID
    if owner == "D":
        # Apply the D string-length contract before either the legacy opt-in
        # return or the normal eight-field validation path.
        bounded_string_fields = {
            "producer_registration_high_water",
            "work_item_high_water",
            "attempt_high_water",
            "barrier_generation",
            "forget_fence_generation_high_water",
            "dependency_closure_cursor",
        }
        for name in bounded_string_fields.intersection(values):
            value = values[name]
            if not isinstance(value, str) or not 1 <= len(value) <= 512:
                return INVALID
    if owner=="D" and set(values)=={
        "producer_registration_high_water","work_item_high_water","attempt_high_water",
        "barrier_generation","barrier_root",
    }:
        # Explicit legacy policy: the former five-field D snapshot is recognizable,
        # but lacks the separately-authoritative ForgetFence and dependency-closure
        # evidence required by Schema 1.2.17. It must never become VALID.
        if any(not isinstance(v,str) or not v for v in values.values()):
            return INVALID
        legacy_digest=td("OWNER-SPECIFIC-HIGH-WATERS",values)
        if snapshot.get("owner_specific_high_waters_digest")!=legacy_digest:
            return INVALID
        return VALID if allow_legacy_d_snapshot else UNKNOWN
    if set(values)!=fields[owner]:
        return INVALID
    if any(not isinstance(v,str) or not v for v in values.values()):
        return INVALID
    for name,value in values.items():
        if name.endswith("digest") or name.endswith("_root"):
            if not re.fullmatch(r"[0-9a-f]{64}",value):
                return INVALID
    expected=td("OWNER-SPECIFIC-HIGH-WATERS",values)
    if snapshot.get("owner_specific_high_waters_digest")!=expected:
        return INVALID
    return VALID



def validate_owner_snapshot_membership_proof_payload(proof, row, snapshot, verify_owner_signature=None):
    """Validate one exact owner proof payload; signature verification is delegated to that owner."""
    if not isinstance(proof,dict) or not isinstance(row,dict) or not isinstance(snapshot,dict):
        return UNKNOWN
    if not callable(verify_owner_signature):
        return UNKNOWN
    required=("proof_ref","owner_kind","owner_authority_ref","issuer_ref","subject_ref","audience_ref","purpose",
      "owner_ledger_ref","owner_ledger_version","owner_entry_ref","owner_entry_digest","owner_admission_ref",
      "owner_sequence_namespace","owner_local_sequence","owner_high_water","owner_ledger_root",
      "owner_snapshot_ref","owner_snapshot_digest","owner_snapshot_attestation_ref",
      "owner_snapshot_attestation_digest","owner_gate_ref","owner_gate_generation","scope_ref",
      "scope_generation","scope_binding_digest","operation_identity_ref","operation_digest","request_digest",
      "anti_rollback_anchor_ref","key_status_generation","signature_profile_ref","key_id","key_version",
      "canonicalization_profile_ref","digest_profile_ref","proof_digest","signature_ref")
    if any(not proof.get(k) for k in required):
        return UNKNOWN
    if proof.get("purpose")!="COC_RECOVERY_CUTOFF_MANIFEST_MEMBERSHIP":
        return INVALID
    if proof.get("owner_kind") not in {"I","D","C"} or proof.get("owner_kind")!=row.get("owner_kind"):
        return INVALID
    row_fields=("owner_ledger_ref","owner_ledger_version","owner_entry_ref","owner_entry_digest",
      "owner_admission_ref","owner_sequence_namespace","owner_local_sequence","owner_high_water",
      "owner_ledger_root","owner_snapshot_ref","owner_snapshot_digest","owner_snapshot_attestation_ref",
      "owner_snapshot_attestation_digest","operation_identity_ref","operation_digest","request_digest",
      "scope_binding_digest")
    for field in row_fields:
        if proof.get(field)!=row.get(field):
            return INVALID
    if proof.get("proof_ref")!=row.get("owner_snapshot_membership_proof_ref"):
        return INVALID
    if proof.get("proof_digest")!=row.get("owner_snapshot_membership_proof_digest"):
        return INVALID
    snapshot_fields=("owner_snapshot_ref","owner_snapshot_digest","owner_snapshot_attestation_ref",
      "owner_snapshot_attestation_digest","owner_ledger_root","owner_gate_ref","owner_gate_generation",
      "anti_rollback_anchor_ref")
    for field in snapshot_fields:
        target="owner_gate_generation" if field=="owner_gate_generation" else field
        if field not in snapshot:
            return UNKNOWN
        if proof.get(field)!=snapshot.get(target):
            return INVALID
    seq=proof.get("owner_local_sequence")
    high=proof.get("owner_high_water")
    if not isinstance(seq,str) or not re.fullmatch(r"(0|[1-9][0-9]*)",seq):
        return INVALID
    if not isinstance(high,str) or not re.fullmatch(r"(0|[1-9][0-9]*)",high):
        return INVALID
    if int(seq)>int(high):
        return INVALID
    verified=verify_owner_signature(proof,proof["owner_kind"],snapshot)
    if verified is None or verified==UNKNOWN:
        return UNKNOWN
    if verified is not True:
        return INVALID
    return VALID

def validate_union(
    m, prefix_rows, admission_rows, snapshots, membership_proofs=None, complete=True,
    verify_membership_proof=None, verify_owner_snapshot=None, allow_legacy_d_snapshot=False,
    schema_artifact_revision="1.2.9",
):
    if not complete:
        return UNKNOWN
    if membership_proofs is None:
        return UNKNOWN
    if admission_rows and not callable(verify_membership_proof):
        return UNKNOWN
    if not isinstance(snapshots,dict) or set(snapshots)!={"I","D","C"}:
        return UNKNOWN
    for owner,s in snapshots.items():
        if s.get("owner") != owner:
            return INVALID
        if not s.get("ledger_available") or not s.get("pagination_complete"):
            return UNKNOWN
        snapshot_result=validate_owner_snapshot(
            s, owner, allow_legacy_d_snapshot=allow_legacy_d_snapshot,
            schema_artifact_revision=schema_artifact_revision,
        )
        if snapshot_result!=VALID:
            return snapshot_result
        # Local cache flags are not authority. Attestation, anti-rollback and
        # currentness must be established by the owner-authoritative verifier.
        if not callable(verify_owner_snapshot):
            return UNKNOWN
        try:
            owner_verified=verify_owner_snapshot(s,owner)
        except Exception:
            return UNKNOWN
        if owner_verified is None or owner_verified==UNKNOWN:
            return UNKNOWN
        if owner_verified is not True:
            return INVALID
    members=m.get("manifest_members")
    if not isinstance(members,list) or members != sorted(members,key=member_key):
        return INVALID
    if len({member_key(x) for x in members}) != len(members):
        return INVALID
    pmap={}
    for p in prefix_rows:
        ref=p.get("participant_intent_ref")
        if not ref or ref in pmap:
            return INVALID
        pmap[ref]=p
    amap={}
    for a in admission_rows:
        key=(a.get("owner_kind"),a.get("owner_admission_ref"))
        if key[0] not in {"I","D","C"} or not key[1] or key in amap:
            return INVALID
        s=snapshots[key[0]]
        if a.get("owner_high_water") != s.get("admission_high_water"):
            return UNKNOWN
        proof=membership_proofs.get(key)
        if proof is None or proof.get("available") is not True:
            return UNKNOWN
        verification=verify_membership_proof(proof,key[0],s)
        if verification is None or verification == UNKNOWN:
            return UNKNOWN
        if verification is not True:
            return INVALID
        if proof.get("owner_ledger_root") != a.get("owner_ledger_root"):
            return INVALID
        if proof.get("owner_entry_digest") != a.get("owner_entry_digest"):
            return INVALID
        if proof.get("owner_snapshot_digest") != a.get("owner_snapshot_digest"):
            return INVALID
        if proof.get("proof_ref") != a.get("owner_snapshot_membership_proof_ref"):
            return INVALID
        if proof.get("proof_digest") != a.get("owner_snapshot_membership_proof_digest"):
            return INVALID
        if proof.get("owner_snapshot_attestation_digest") != a.get("owner_snapshot_attestation_digest"):
            return INVALID
        if proof.get("owner_local_sequence") != a.get("owner_local_sequence") or proof.get("owner_high_water") != a.get("owner_high_water"):
            return INVALID
        if proof.get("operation_digest") != a.get("operation_digest") or proof.get("scope_binding_digest") != a.get("scope_binding_digest"):
            return INVALID
        if proof.get("within_frozen_high_water") is not True:
            return INVALID
        for field in ("owner_snapshot_ref","owner_snapshot_digest","owner_snapshot_attestation_ref",
                      "owner_snapshot_attestation_digest","owner_ledger_root"):
            if a.get(field)!=s.get(field):
                return INVALID
        if not a.get("owner_snapshot_membership_proof_ref"):
            return INVALID
        amap[key]=a
    cm={}
    lm={}
    for x in members:
        if x.get("member_kind")=="COC_PARTICIPANT":
            ref=x.get("participant_intent_ref")
            if not ref or ref in cm:
                return INVALID
            cm[ref]=x
        elif x.get("member_kind")=="OWNER_LOCAL_ADMISSION":
            if x.get("coc_participant_intent_ref","MISSING") is not None or not x.get("coc_absence_reason"):
                return INVALID
            key=(x.get("owner_kind"),x.get("owner_admission_ref"))
            if key in lm:
                return INVALID
            lm[key]=x
        else:
            return INVALID
    if set(cm)!=set(pmap):
        return INVALID
    for ref,p in pmap.items():
        x=cm[ref]
        for field in ("transaction_ref","request_digest","owner_boundary_ref","policy_domain_ref",
                      "participant_tuple_digest","participant_owner"):
            if x.get(field)!=p.get(field):
                return INVALID
        bindings=x.get("owner_admission_bindings")
        if not isinstance(bindings,list):
            return INVALID
        seen=[]
        for b in bindings:
            key=(b.get("owner_kind"),b.get("owner_admission_ref"))
            a=amap.get(key)
            if a is None or a.get("coc_participant_intent_ref")!=ref:
                return INVALID
            for field in ("owner_entry_ref","owner_ledger_ref","owner_ledger_version","owner_local_sequence",
                          "owner_high_water","owner_entry_digest","owner_ledger_root","owner_snapshot_ref",
                          "owner_snapshot_digest","owner_snapshot_attestation_ref","owner_snapshot_attestation_digest",
                          "owner_snapshot_membership_proof_ref","operation_digest","scope_binding_digest"):
                if b.get(field)!=a.get(field):
                    return INVALID
            if b.get("coc_participant_intent_ref")!=ref:
                return INVALID
            seen.append(key)
        expected={k for k,a in amap.items() if a.get("coc_participant_intent_ref")==ref}
        if set(seen)!=expected or len(seen)!=len(set(seen)):
            return INVALID
    expected_local={k for k,a in amap.items() if a.get("coc_participant_intent_ref") is None}
    if set(lm)!=expected_local:
        return INVALID
    for key,x in lm.items():
        a=amap[key]
        for field in ("owner_kind","owner_admission_ref","owner_entry_ref","owner_entry_kind","owner_ledger_ref",
                      "owner_ledger_version","owner_local_sequence","owner_high_water","owner_entry_digest",
                      "owner_ledger_root","owner_snapshot_ref","owner_snapshot_digest","owner_snapshot_attestation_ref",
                      "owner_snapshot_attestation_digest","owner_snapshot_membership_proof_ref",
                      "operation_identity_ref","operation_digest","request_digest","scope_binding_digest",
                      "admission_state","effect_boundary"):
            if x.get(field)!=a.get(field):
                return INVALID
    roots=m.get("owner_snapshot_roots")
    if not isinstance(roots,dict) or set(roots)!={"I","D","C"}:
        return INVALID
    for owner,s in snapshots.items():
        if roots.get(owner)!=snapshot_root(s):
            return INVALID
    coc,local=len(cm),len(lm)
    if m.get("coc_participant_count")!=coc or m.get("owner_local_admission_count")!=local:
        return INVALID
    if m.get("manifest_member_count")!=len(members) or len(members)!=coc+local:
        return INVALID
    if m.get("member_set_root")!=td("MANIFEST-MEMBER-SET",members):
        return INVALID
    if m.get("manifest_content_digest")!=content_digest(m):
        return INVALID
    return VALID

def validate_pair(batch, manifest, batch_position, manifest_position, linearizable=True):
    if not linearizable:return UNKNOWN
    if batch.get("quorum_committed") is not True or manifest.get("quorum_committed") is not True:return UNKNOWN
    if tuple(manifest_position)<=tuple(batch_position):return INVALID
    if batch.get("message_type")!="COC_RECOVERY_CUTOFF_BATCH" or manifest.get("message_type")!="PARTICIPANT_SET_RECONCILIATION":return INVALID
    if batch.get("schema_version")!="1.3.0" or manifest.get("schema_version")!="1.3.0":return INVALID
    for f in ("recovery_epoch_ref","manifest_id","manifest_content_digest","coc_participant_count",
              "owner_local_admission_count","manifest_member_count","member_set_root","prefix"):
        if batch.get(f)!=manifest.get(f):return INVALID
    if manifest.get("batch_record_ref")!=batch.get("coc_record_ref"):return INVALID
    if manifest.get("batch_position")!=batch_position[1] or manifest.get("batch_entry_digest")!=batch.get("coc_entry_digest"):return INVALID
    if batch.get("coc_record_position")!=str(batch_position[1]) or manifest.get("coc_record_position")!=str(manifest_position[1]):return INVALID
    if manifest.get("manifest_content_digest")!=content_digest(manifest):return INVALID
    owner_snaps=batch.get("owner_snapshots")
    roots=manifest.get("owner_snapshot_roots")
    if not isinstance(owner_snaps,dict) or set(owner_snaps)!={"I","D","C"}:return UNKNOWN
    if not isinstance(roots,dict) or set(roots)!={"I","D","C"}:return INVALID
    for owner,snap in owner_snaps.items():
        if roots.get(owner)!=snapshot_root(snap):return INVALID
    if manifest.get("coc_entry_digest")!=manifest.get("envelope_payload_digest"):return INVALID
    return VALID


def owner_reconciliation_root(manifest, owner):
    projected=[]
    for member in manifest.get("manifest_members",[]):
        if member.get("member_kind")=="COC_PARTICIPANT":
            bindings=[x for x in member.get("owner_admission_bindings",[]) if x.get("owner_kind")==owner]
            if bindings:
                projected.append({"participant_intent_ref":member.get("participant_intent_ref"),
                                  "owner_admission_bindings":bindings})
        elif member.get("member_kind")=="OWNER_LOCAL_ADMISSION" and member.get("owner_kind")==owner:
            projected.append(member)
    return td("OWNER-RECONCILIATION", projected)


def validate_release(r,b,m):
    owner=r.get("owner_kind")
    if owner not in {"I","D","C"} or r.get("release_type")!="OUTAGE_ADMISSION_RELEASE_ONLY":
        return INVALID
    snapshots=b.get("owner_snapshots")
    if not isinstance(snapshots,dict) or owner not in snapshots:
        return UNKNOWN
    s=snapshots[owner]
    expected={
      "batch_record_ref":b.get("coc_record_ref"),"batch_digest":b.get("payload_digest"),
      "batch_position":b.get("coc_record_position"),"batch_entry_digest":b.get("coc_entry_digest"),
      "manifest_record_ref":m.get("coc_record_ref"),"manifest_record_position":m.get("coc_record_position"),
      "manifest_content_digest":m.get("manifest_content_digest"),
      "manifest_record_entry_digest":m.get("coc_entry_digest"),
      "owner_gate_ref":s.get("owner_gate_ref"),"owner_gate_generation":s.get("owner_gate_generation"),
      "owner_request_high_water":s.get("request_high_water"),
      "owner_admission_high_water":s.get("admission_high_water"),
      "request_set_digest":s.get("request_set_digest"),"admission_set_digest":s.get("admission_set_digest"),
      "request_ledger_root":s.get("request_ledger_root"),"admission_ledger_root":s.get("admission_ledger_root"),
      "reconciliation_root":owner_reconciliation_root(m,owner),
    }
    if any(r.get(k)!=v for k,v in expected.items()):
        return INVALID
    return VALID if r.get("final_currentness_cas_valid") is True else UNKNOWN


def validate_epoch_completed(completed, batch, manifest, releases):
    if not isinstance(releases,dict) or set(releases)!={"I","D","C"}:
        return INVALID
    for owner,release in releases.items():
        if release.get("owner_kind")!=owner:
            return INVALID
        result=validate_release(release,batch,manifest)
        if result!=VALID:
            return result
    expected={
      "recovery_epoch_ref":batch.get("recovery_epoch_ref"),
      "batch_record_ref":batch.get("coc_record_ref"),
      "batch_digest":batch.get("payload_digest"),
      "batch_position":batch.get("coc_record_position"),
      "batch_entry_digest":batch.get("coc_entry_digest"),
      "manifest_record_ref":manifest.get("coc_record_ref"),
      "manifest_content_digest":manifest.get("manifest_content_digest"),
      "manifest_record_position":manifest.get("coc_record_position"),
      "manifest_record_entry_digest":manifest.get("coc_entry_digest"),
    }
    if any(completed.get(k)!=v for k,v in expected.items()):
        return INVALID
    refs=completed.get("owner_release_refs")
    if not isinstance(refs,list) or len(refs)!=3 or len(set(refs))!=3:
        return INVALID
    if set(refs)!={r.get("coc_record_ref") for r in releases.values()}:
        return INVALID
    return VALID if completed.get("quorum_committed") is True else UNKNOWN


def validate_profile(message, protected, registry, owner, audience, purpose):
    if not protected:return VALID
    pid=message.get("signature_profile_id")
    if not pid:return INVALID
    if registry is None:return UNKNOWN
    profile=registry.get(pid)
    if not profile or profile.get("status")!="ACTIVE":return INVALID
    if any(profile.get(k)!=v for k,v in {"owner_authority":owner,"audience":audience,
                                         "purpose":purpose,"wire_schema_version":"1.3.0"}.items()):return INVALID
    if message.get("owner_authority")!=owner or message.get("audience")!=audience:return INVALID
    return VALID


def validate_provider_outcome(m):
    if m.get("message_type")!="C_PROVIDER_OUTCOME_RECORDED" or m.get("owner_authority")!="C":return INVALID
    required=("c_submit_outcome_ref","c_submit_outcome_digest","owner_admission_ref","owner_ledger_ref",
              "owner_ledger_version","owner_local_sequence","owner_high_water","owner_ledger_root",
              "provider_ref","provider_adapter_ref","provider_idempotency_key_ref","request_digest",
              "final_request_boundary_id","provider_outcome_evidence_ref")
    if any(not m.get(k) for k in required):return UNKNOWN
    outcome=m.get("provider_outcome")
    if outcome=="HANDOFF_ACCEPTED":
        return VALID if all(m.get(k) for k in ("provider_request_ref","provider_receipt_ref","participant_reservation_ref")) else INVALID
    if outcome=="HANDOFF_REJECTED":
        return VALID if all(m.get(k) for k in ("provider_no_handoff_proof_ref","participant_reservation_ref")) else INVALID
    if outcome=="NOT_INVOKED":
        return INVALID if m.get("provider_receipt_ref") or not m.get("not_invoked_proof_ref") else VALID
    if outcome in {"UNKNOWN","IN_DOUBT"}:return UNKNOWN if m.get("unknown_reason_ref") else INVALID
    return INVALID
