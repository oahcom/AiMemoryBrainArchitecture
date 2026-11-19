"""H semantic/structural tests for unified manifest schema artifact 1.2.9."""
import json, sys, unittest
from jsonschema import Draft202012Validator, RefResolver
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
SCHEMA_PATH=ROOT/"schemas"/"bmcp.coc-jf10-unified-1.2.12.schema.json"
sys.path.insert(0,str(ROOT/"runtime_reference"))
from unified_manifest_semantics import (VALID,INVALID,UNKNOWN,td,snapshot_root,content_digest,
    validate_union as _validate_union,validate_pair,validate_release,validate_epoch_completed,validate_profile,validate_provider_outcome)


def fixtures():
    snaps={}
    for o in ("I","D","C"):
        hexchar={"I":"1","D":"2","C":"3"}[o]
        snaps[o]={"owner":o,"owner_gate_ref":o+"/gate/1","request_set_digest":hexchar*64,"admission_set_digest":hexchar*64,"owner_snapshot_ref":o+"/snap/1","owner_snapshot_digest":hexchar*64,
          "owner_snapshot_attestation_ref":o+"/att/1","owner_snapshot_attestation_digest":hexchar*64,
          "owner_gate_generation":"7","request_high_water":"12","admission_high_water":"18","request_count":1,"admission_count":1,
          "request_ledger_root":hexchar*64,"admission_ledger_root":hexchar*64,
          "owner_ledger_root":hexchar*64,"anti_rollback_anchor_ref":o+"/anchor/7",
          "owner_specific_high_waters":{
            "I":{"receipt_issue_high_water":"I/issue/9","receipt_consume_high_water":"I/consume/7","inventory_epoch_ref":"I/inventory/3","registry_snapshot_digest":"1"*64,"relevant_entry_set_root":"1"*64},
            "D":{"producer_registration_high_water":"D/registration/9","work_item_high_water":"D/work/11","attempt_high_water":"D/attempt/12","barrier_generation":"D/barrier/4","barrier_root":"2"*64},
            "C":{"reservation_high_water":"C/reservation/5","provider_attempt_high_water":"C/attempt/8","provider_outcome_high_water":"C/outcome/8"}
          }[o],"owner_specific_high_waters_digest":None,"ledger_available":True,"pagination_complete":True}
        snaps[o]["owner_specific_high_waters_digest"]=td("OWNER-SPECIFIC-HIGH-WATERS",snaps[o]["owner_specific_high_waters"])
    def admission(owner,ref,pref):
        s=snaps[owner]
        return {"owner_kind":owner,"owner_admission_ref":owner+"/"+ref,"owner_entry_ref":owner+"/"+ref+"/row",
          "owner_entry_kind":"RESERVATION" if owner=="C" else "WORK_ITEM","owner_ledger_ref":owner+"/ledger/1",
          "owner_ledger_version":"1","owner_local_sequence":"sequence/5","owner_high_water":"18","owner_entry_digest":"a"*64,
          "owner_ledger_root":s["owner_ledger_root"],"owner_snapshot_ref":s["owner_snapshot_ref"],
          "owner_snapshot_digest":s["owner_snapshot_digest"],"owner_snapshot_attestation_ref":s["owner_snapshot_attestation_ref"],
          "owner_snapshot_attestation_digest":s["owner_snapshot_attestation_digest"],
          "owner_snapshot_membership_proof_ref":owner+"/membership-proof/"+ref,"owner_snapshot_membership_proof_digest":"e"*64,
          "operation_identity_ref":"operation/"+ref,"operation_digest":"b"*64,"request_digest":"c"*64,
          "scope_binding_digest":"d"*64,"admission_state":"PENDING" if pref else "ADMITTED_NOT_REGISTERED",
          "effect_boundary":"RESERVATION" if owner=="C" else "WORK_ADMISSION",
          "coc_participant_intent_ref":pref,"coc_absence_reason":"not_registered_at_frozen_prefix" if pref is None else None}
    a=admission("C","admit-1","participant/1");z=admission("D","work-9",None)
    p={"member_kind":"COC_PARTICIPANT","participant_intent_ref":"participant/1","transaction_ref":"transaction/1",
       "request_digest":"c"*64,"owner_boundary_ref":"boundary/C/1","policy_domain_ref":"policy/1",
       "participant_tuple_digest":"e"*64,"participant_owner":"C","owner_admission_bindings":[{
        "owner_kind":"C","owner_admission_ref":a["owner_admission_ref"],"owner_entry_ref":a["owner_entry_ref"],
        "owner_ledger_ref":a["owner_ledger_ref"],"owner_ledger_version":a["owner_ledger_version"],
        "owner_local_sequence":a["owner_local_sequence"],"owner_high_water":a["owner_high_water"],
        "owner_entry_digest":a["owner_entry_digest"],"owner_ledger_root":a["owner_ledger_root"],
        "owner_snapshot_ref":a["owner_snapshot_ref"],"owner_snapshot_digest":a["owner_snapshot_digest"],
        "owner_snapshot_attestation_ref":a["owner_snapshot_attestation_ref"],
        "owner_snapshot_attestation_digest":a["owner_snapshot_attestation_digest"],
        "owner_snapshot_membership_proof_ref":a["owner_snapshot_membership_proof_ref"],"owner_snapshot_membership_proof_digest":a["owner_snapshot_membership_proof_digest"],
        "operation_digest":a["operation_digest"],"scope_binding_digest":a["scope_binding_digest"],
        "coc_participant_intent_ref":"participant/1"}]}
    local={"member_kind":"OWNER_LOCAL_ADMISSION",**{k:v for k,v in z.items() if k!="coc_absence_reason"},
           "coc_participant_intent_ref":None,"coc_absence_reason":z["coc_absence_reason"]}
    members=sorted([p,local],key=lambda x:("0" if x["member_kind"]=="COC_PARTICIPANT" else "1",
        x.get("participant_intent_ref",x.get("owner_kind","")+":"+x.get("owner_admission_ref",""))))
    m={"schema_version":"1.3.0","message_type":"PARTICIPANT_SET_RECONCILIATION","manifest_id":"manifest/1",
       "recovery_epoch_ref":"epoch/1","prefix":{"coordinator_epoch":"term/4","coordinator_index":88,
       "entry_digest":"f"*64,"committed_configuration_epoch":"config/2"},"enumeration_high_water":"prefix/88",
       "coc_participant_count":1,"owner_local_admission_count":1,"manifest_member_count":2,
       "member_set_root":td("MANIFEST-MEMBER-SET",members),"owner_snapshot_roots":{k:snapshot_root(v) for k,v in snaps.items()},
       "manifest_members":members}
    m["manifest_content_digest"]=content_digest(m)
    proofs={}
    for row in (a,z):
        key=(row["owner_kind"],row["owner_admission_ref"])
        proofs[key]={"available":True,"valid":True,"test_signature_verified":True,"owner_ledger_root":row["owner_ledger_root"],
          "owner_entry_digest":row["owner_entry_digest"],"owner_snapshot_digest":row["owner_snapshot_digest"],
          "owner_snapshot_attestation_digest":row["owner_snapshot_attestation_digest"],
          "owner_local_sequence":row["owner_local_sequence"],"owner_high_water":row["owner_high_water"],
          "operation_digest":row["operation_digest"],"scope_binding_digest":row["scope_binding_digest"],
          "proof_ref":row["owner_snapshot_membership_proof_ref"],
          "proof_digest":row["owner_snapshot_membership_proof_digest"],"within_frozen_high_water":True}
    return m,[p],[a,z],snaps,proofs

class Schema1212Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.schema=json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    def setUp(self):self.m,self.prefix,self.admissions,self.snaps,self.proofs=fixtures()
    def validate_union(self,*args,**kwargs):
        kwargs["verify_membership_proof"]=lambda proof,owner,snapshot: proof.get("test_signature_verified") is True
        kwargs["verify_owner_snapshot"]=lambda snapshot,owner: True
        kwargs["allow_legacy_d_snapshot"]=True  # Historical 1.2.12 fixtures intentionally use the old five-field D shape.
        return _validate_union(*args,**kwargs)
    def msg(self,t):
        return next(x["allOf"][1] for x in self.schema["oneOf"] if x["allOf"][1]["properties"]["message_type"]["const"]==t)
    def test_SCHEMA1212_01_artifact_vs_wire_version(self):
        self.assertTrue(self.schema["$id"].endswith("/1.2.12"))
        env=self.schema["$defs"]["commonEnvelope"]
        self.assertEqual(env["properties"]["schema_artifact_revision"]["const"],"1.2.12")
        self.assertIn("schema_artifact_revision",env["required"])
        self.assertEqual(env["properties"]["schema_version"]["const"],"1.3.0")
    def test_SCHEMA1212_02_typed_union_members(self):
        refs={x["$ref"] for x in self.msg("PARTICIPANT_SET_RECONCILIATION")["properties"]["manifest_members"]["items"]["oneOf"]}
        self.assertEqual(refs,{"#/$defs/cocParticipantMember","#/$defs/ownerLocalAdmissionMember"})
    def test_SCHEMA1212_03_local_admission_requires_null_and_reason(self):
        d=self.schema["$defs"]["ownerLocalAdmissionMember"]
        self.assertEqual(d["properties"]["coc_participant_intent_ref"]["type"],"null")
        self.assertTrue({"coc_participant_intent_ref","coc_absence_reason","owner_snapshot_attestation_digest"}.issubset(d["required"]))
    def test_SCHEMA1212_04_coc_member_binds_owner_rows(self):
        self.assertIn("owner_admission_bindings",self.schema["$defs"]["cocParticipantMember"]["required"])
    def test_SCHEMA1212_05_batch_has_distinct_counts_and_root(self):
        p=self.msg("COC_RECOVERY_CUTOFF_BATCH")["properties"]
        self.assertTrue({"manifest_content_digest","coc_participant_count","owner_local_admission_count","manifest_member_count","member_set_root"}.issubset(p))
    def test_SCHEMA1212_06_manifest_binds_owner_snapshot_roots(self):
        p=self.msg("PARTICIPANT_SET_RECONCILIATION")["properties"]
        self.assertIn("owner_snapshot_roots",p)
        self.assertEqual(self.schema["$defs"]["ownerSnapshotRoots"]["required"],["I","D","C"])
    def test_SCHEMA1212_07_snapshot_requires_both_attestation_and_highwater_digests(self):
        r=set(self.schema["$defs"]["ownerSnapshot"]["required"])
        self.assertTrue({"owner_snapshot_attestation_digest","owner_specific_high_waters_digest"}.issubset(r))
    def test_SCHEMA1212_08_release_completion_bind_content_and_record(self):
        for t in ("OWNER_LOCAL_GATE_RELEASE","RECOVERY_EPOCH_COMPLETED"):
            r=set(self.msg(t)["required"])
            self.assertTrue({"manifest_content_digest","manifest_record_entry_digest"}.issubset(r))
    def test_SCHEMA1212_09_signature_profile_structural_optional(self):
        d=self.schema["$defs"]["commonEnvelope"]
        self.assertIn("signature_profile_id",d["properties"])
        self.assertNotIn("signature_profile_id",d["required"])
    def test_SCHEMA1212_10_ambiguous_manifest_digest_removed(self):
        for t in ("COC_RECOVERY_CUTOFF_BATCH","PARTICIPANT_SET_RECONCILIATION","OWNER_LOCAL_GATE_RELEASE","RECOVERY_EPOCH_COMPLETED"):
            self.assertNotIn("manifest_digest",self.msg(t)["properties"])
    def test_SCHEMA1212_11_membership_proof_ref_and_digest_are_required(self):
        for name in ("ownerAdmissionBinding","ownerLocalAdmissionMember"):
            required=set(self.schema["$defs"][name]["required"])
            self.assertTrue({"owner_snapshot_membership_proof_ref","owner_snapshot_membership_proof_digest"}.issubset(required))
    def test_SCHEMA1212_12_owner_release_enum_matches_I_D_contract(self):
        self.assertEqual(self.msg("OWNER_LOCAL_GATE_RELEASE")["properties"]["release_type"]["const"],"OUTAGE_ADMISSION_RELEASE_ONLY")

    def test_SCHEMA1212_13_json_schema_draft_2020_12_meta_validation(self):
        Draft202012Validator.check_schema(self.schema)

    def test_SCHEMA1212_14_owner_local_admission_member_validates_against_schema(self):
        resolver=RefResolver.from_schema(self.schema)
        member=next(x for x in self.m["manifest_members"] if x["member_kind"]=="OWNER_LOCAL_ADMISSION")
        Draft202012Validator(self.schema["$defs"]["ownerLocalAdmissionMember"],resolver=resolver).validate(member)

    def test_SCHEMA1212_15_coc_participant_and_owner_binding_validate_against_schema(self):
        resolver=RefResolver.from_schema(self.schema)
        member=next(x for x in self.m["manifest_members"] if x["member_kind"]=="COC_PARTICIPANT")
        Draft202012Validator(self.schema["$defs"]["cocParticipantMember"],resolver=resolver).validate(member)
        Draft202012Validator(self.schema["$defs"]["ownerAdmissionBinding"],resolver=resolver).validate(member["owner_admission_bindings"][0])

    def test_SCHEMA1212_16_owner_snapshot_roots_validate_against_schema(self):
        resolver=RefResolver.from_schema(self.schema)
        Draft202012Validator(self.schema["$defs"]["ownerSnapshotRoots"],resolver=resolver).validate(self.m["owner_snapshot_roots"])

    def test_SCHEMA1212_13_owner_highwater_object_is_discriminated(self):
        refs={x["$ref"] for x in self.schema["$defs"]["ownerSnapshot"]["properties"]["owner_specific_high_waters"]["oneOf"]}
        self.assertEqual(refs,{"#/$defs/ownerSpecificHighWatersI","#/$defs/ownerSpecificHighWatersD","#/$defs/ownerSpecificHighWatersC"})
    def test_SCHEMA1212_14_each_owner_highwater_shape_is_closed_and_complete(self):
        for name in ("ownerSpecificHighWatersI","ownerSpecificHighWatersD","ownerSpecificHighWatersC"):
            d=self.schema["$defs"][name]
            self.assertFalse(d["additionalProperties"])
            self.assertEqual(set(d["required"]),set(d["properties"]))
    def test_SCHEMA1212_15_owner_specific_highwater_fixtures_validate(self):
        resolver=RefResolver.from_schema(self.schema)
        for owner,name in (("I","ownerSpecificHighWatersI"),("D","ownerSpecificHighWatersD"),("C","ownerSpecificHighWatersC")):
            Draft202012Validator(self.schema["$defs"][name],resolver=resolver).validate(self.snaps[owner]["owner_specific_high_waters"])


class UnionSemanticsTests(unittest.TestCase):
    def setUp(self):self.m,self.prefix,self.admissions,self.snaps,self.proofs=fixtures()
    def validate_union(self,*args,**kwargs):
        kwargs["verify_membership_proof"]=lambda proof,owner,snapshot: proof.get("test_signature_verified") is True
        kwargs["verify_owner_snapshot"]=lambda snapshot,owner: True
        kwargs["allow_legacy_d_snapshot"]=True  # Historical 1.2.12 fixtures intentionally use the old five-field D shape.
        return _validate_union(*args,**kwargs)
    def test_UNION_01_exact_union_passes(self):self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,self.snaps,self.proofs),VALID)
    def test_UNION_02_omitted_prefix_participant_fails(self):self.assertEqual(self.validate_union(self.m,[],self.admissions,self.snaps,self.proofs),INVALID)
    def test_UNION_03_omitted_unregistered_admission_fails(self):self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions[:1],self.snaps,self.proofs),INVALID)
    def test_UNION_04_duplicate_admission_fails(self):self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions+[deepcopy(self.admissions[0])],self.snaps,self.proofs),INVALID)
    def test_UNION_05_fabricated_coc_ref_on_local_member_fails(self):
        m=deepcopy(self.m);m["manifest_members"][1]["coc_participant_intent_ref"]="fake"
        self.assertEqual(self.validate_union(m,self.prefix,self.admissions,self.snaps,self.proofs),INVALID)
    def test_UNION_06_missing_absence_reason_fails(self):
        m=deepcopy(self.m);m["manifest_members"][1]["coc_absence_reason"]=""
        self.assertEqual(self.validate_union(m,self.prefix,self.admissions,self.snaps,self.proofs),INVALID)
    def test_UNION_07_wrong_owner_row_binding_fails(self):
        m=deepcopy(self.m);m["manifest_members"][0]["owner_admission_bindings"][0]["owner_entry_ref"]="wrong"
        self.assertEqual(self.validate_union(m,self.prefix,self.admissions,self.snaps,self.proofs),INVALID)
    def test_UNION_08_missing_owner_snapshot_is_unknown(self):
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,{"I":self.snaps["I"],"D":self.snaps["D"]},self.proofs),UNKNOWN)
    def test_UNION_09_partial_owner_pagination_is_unknown(self):
        s=deepcopy(self.snaps);s["D"]["pagination_complete"]=False
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,s,self.proofs),UNKNOWN)
    def test_UNION_10_owner_highwater_advance_is_unknown(self):
        a=deepcopy(self.admissions);a[1]["owner_high_water"]="19"
        self.assertEqual(self.validate_union(self.m,self.prefix,a,self.snaps,self.proofs),UNKNOWN)
    def test_UNION_11_owner_snapshot_root_mismatch_fails(self):
        m=deepcopy(self.m);m["owner_snapshot_roots"]["I"]["request_ledger_root"]="0"*64
        self.assertEqual(self.validate_union(m,self.prefix,self.admissions,self.snaps,self.proofs),INVALID)
    def test_UNION_12_member_count_mismatch_fails(self):
        m=deepcopy(self.m);m["manifest_member_count"]=9
        self.assertEqual(self.validate_union(m,self.prefix,self.admissions,self.snaps,self.proofs),INVALID)
    def test_UNION_13_member_root_mismatch_fails(self):
        m=deepcopy(self.m);m["member_set_root"]="0"*64
        self.assertEqual(self.validate_union(m,self.prefix,self.admissions,self.snaps,self.proofs),INVALID)
    def test_UNION_14_content_digest_mismatch_fails(self):
        m=deepcopy(self.m);m["manifest_content_digest"]="0"*64
        self.assertEqual(self.validate_union(m,self.prefix,self.admissions,self.snaps,self.proofs),INVALID)
    def test_UNION_15_incomplete_prefix_is_unknown(self):
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,self.snaps,self.proofs,False),UNKNOWN)

    def test_UNION_16_missing_membership_proof_is_unknown(self):
        proofs=deepcopy(self.proofs);proofs.pop(("D","D/work-9"))
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,self.snaps,proofs),UNKNOWN)
    def test_UNION_17_invalid_membership_proof_is_invalid(self):
        proofs=deepcopy(self.proofs);proofs[("C","C/admit-1")]["test_signature_verified"]=False
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,self.snaps,proofs),INVALID)
    def test_UNION_18_non_numeric_owner_sequences_are_not_arithmetically_compared(self):
        snaps=deepcopy(self.snaps);rows=deepcopy(self.admissions);proofs=deepcopy(self.proofs)
        snaps["D"]["admission_high_water"]="opaque/cursor/18";rows[1]["owner_high_water"]="opaque/cursor/18"
        proofs[("D","D/work-9")]["owner_high_water"]="opaque/cursor/18"
        m=deepcopy(self.m);m["owner_snapshot_roots"]["D"]["admission_high_water"]="opaque/cursor/18"
        m["manifest_members"][1]["owner_high_water"]="opaque/cursor/18"
        m["member_set_root"]=td("MANIFEST-MEMBER-SET",m["manifest_members"])
        m["manifest_content_digest"]=content_digest(m)
        self.assertEqual(self.validate_union(m,self.prefix,rows,snaps,proofs),VALID)
    def test_UNION_19_empty_owner_binding_is_valid_when_no_owner_admission_applies(self):
        m=deepcopy(self.m);m["manifest_members"]=[m["manifest_members"][0]]
        m["manifest_members"][0]["owner_admission_bindings"]=[]
        m["owner_local_admission_count"]=0;m["manifest_member_count"]=1
        m["member_set_root"]=td("MANIFEST-MEMBER-SET",m["manifest_members"])
        m["manifest_content_digest"]=content_digest(m)
        self.assertEqual(self.validate_union(m,self.prefix,[],self.snaps,{}),VALID)
    def test_UNION_20_applicable_owner_admission_cannot_be_omitted_from_binding(self):
        m=deepcopy(self.m);m["manifest_members"][0]["owner_admission_bindings"]=[]
        self.assertEqual(self.validate_union(m,self.prefix,self.admissions[:1],self.snaps,self.proofs),INVALID)


    def test_UNION_21_membership_proof_ref_mismatch_fails(self):
        proofs=deepcopy(self.proofs);proofs[("C","C/admit-1")]["proof_ref"]="wrong/ref"
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,self.snaps,proofs),INVALID)
    def test_UNION_22_membership_proof_outside_highwater_fails(self):
        proofs=deepcopy(self.proofs);proofs[("D","D/work-9")]["within_frozen_high_water"]=False
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,self.snaps,proofs),INVALID)

    def test_UNION_23_owner_specific_highwaters_digest_is_verified(self):
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,self.snaps,self.proofs),VALID)
    def test_UNION_24_missing_owner_specific_highwater_is_invalid(self):
        snaps=deepcopy(self.snaps);del snaps["D"]["owner_specific_high_waters"]["barrier_root"]
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,snaps,self.proofs),INVALID)
    def test_UNION_25_cross_owner_highwater_field_is_invalid(self):
        snaps=deepcopy(self.snaps);snaps["D"]["owner_specific_high_waters"]["receipt_issue_high_water"]="I/issue/1"
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,snaps,self.proofs),INVALID)
    def test_UNION_26_owner_specific_highwater_digest_mismatch_is_invalid(self):
        snaps=deepcopy(self.snaps);snaps["I"]["owner_specific_high_waters_digest"]="0"*64
        self.assertEqual(self.validate_union(self.m,self.prefix,self.admissions,snaps,self.proofs),INVALID)


class PairAndReleaseTests(unittest.TestCase):
    def setUp(self):
        self.m,self.prefix,self.admissions,self.snaps,self.proofs=fixtures()
        self.batch={"schema_version":"1.3.0","message_type":"COC_RECOVERY_CUTOFF_BATCH",
          "recovery_epoch_ref":self.m["recovery_epoch_ref"],"manifest_id":self.m["manifest_id"],
          "manifest_content_digest":self.m["manifest_content_digest"],
          "coc_participant_count":self.m["coc_participant_count"],
          "owner_local_admission_count":self.m["owner_local_admission_count"],
          "manifest_member_count":self.m["manifest_member_count"],"member_set_root":self.m["member_set_root"],
          "prefix":self.m["prefix"],"owner_snapshots":self.snaps,"coc_record_ref":"coc/batch/1",
          "coc_record_position":"100","payload_digest":"a"*64,"coc_entry_digest":"f"*64,"quorum_committed":True}
        self.manifest=deepcopy(self.m)
        self.manifest.update({"batch_record_ref":"coc/batch/1","batch_position":100,
          "batch_entry_digest":"f"*64,"coc_record_ref":"coc/manifest/1","coc_record_position":"101",
          "coc_entry_digest":"e"*64,"envelope_payload_digest":"e"*64,"quorum_committed":True})
    def test_PAIR_01_exact_batch_manifest_pair_passes(self):
        from unified_manifest_semantics import validate_pair
        self.assertEqual(validate_pair(self.batch,self.manifest,(4,100),(4,101)),VALID)
    def test_PAIR_02_manifest_must_follow_batch(self):
        from unified_manifest_semantics import validate_pair
        self.assertEqual(validate_pair(self.batch,self.manifest,(4,101),(4,100)),INVALID)
    def test_PAIR_03_wrong_batch_backlink_fails(self):
        from unified_manifest_semantics import validate_pair
        m=deepcopy(self.manifest);m["batch_record_ref"]="wrong"
        self.assertEqual(validate_pair(self.batch,m,(4,100),(4,101)),INVALID)
    def test_PAIR_04_wrong_owner_snapshot_roots_fail(self):
        from unified_manifest_semantics import validate_pair
        m=deepcopy(self.manifest);m["owner_snapshot_roots"]["I"]["request_ledger_root"]="0"*64
        self.assertEqual(validate_pair(self.batch,m,(4,100),(4,101)),INVALID)
    def test_PAIR_05_non_linearizable_readback_is_unknown(self):
        from unified_manifest_semantics import validate_pair
        self.assertEqual(validate_pair(self.batch,self.manifest,(4,100),(4,101),False),UNKNOWN)
    def test_RELEASE_01_exact_content_and_record_digest_binding_passes(self):
        from unified_manifest_semantics import owner_reconciliation_root
        s=self.snaps["I"]
        r={"owner_kind":"I","release_type":"OUTAGE_ADMISSION_RELEASE_ONLY",
           "batch_record_ref":"coc/batch/1","batch_digest":"a"*64,"batch_position":"100","batch_entry_digest":"f"*64,
           "manifest_record_ref":"coc/manifest/1","manifest_record_position":"101",
           "manifest_content_digest":self.manifest["manifest_content_digest"],"manifest_record_entry_digest":"e"*64,
           "owner_gate_ref":s["owner_gate_ref"],"owner_gate_generation":s["owner_gate_generation"],
           "owner_request_high_water":s["request_high_water"],"owner_admission_high_water":s["admission_high_water"],
           "request_set_digest":s["request_set_digest"],"admission_set_digest":s["admission_set_digest"],
           "request_ledger_root":s["request_ledger_root"],"admission_ledger_root":s["admission_ledger_root"],
           "reconciliation_root":owner_reconciliation_root(self.manifest,"I"),"final_currentness_cas_valid":True}
        self.assertEqual(validate_release(r,self.batch,self.manifest),VALID)
    def test_RELEASE_02_missing_record_digest_fails(self):
        r={"owner_kind":"D","release_type":"OUTAGE_ADMISSION_RELEASE_ONLY",
           "batch_record_ref":"coc/batch/1","batch_digest":"a"*64,"batch_position":"100","batch_entry_digest":"f"*64,
           "manifest_record_ref":"coc/manifest/1","manifest_record_position":"101",
           "manifest_content_digest":self.manifest["manifest_content_digest"],
           "owner_gate_ref":self.snaps["D"]["owner_gate_ref"],"owner_gate_generation":"7",
           "owner_request_high_water":"12","owner_admission_high_water":"18",
           "request_set_digest":"d"*64,"admission_set_digest":"d"*64,
           "request_ledger_root":"d"*64,"admission_ledger_root":"d"*64,
           "reconciliation_root":"d"*64,"final_currentness_cas_valid":True}
        self.assertEqual(validate_release(r,self.batch,self.manifest),INVALID)
    def test_RELEASE_03_currentness_cas_not_proven_is_unknown(self):
        from unified_manifest_semantics import owner_reconciliation_root
        s=self.snaps["C"]
        r={"owner_kind":"C","release_type":"OUTAGE_ADMISSION_RELEASE_ONLY",
           "batch_record_ref":"coc/batch/1","batch_digest":"a"*64,"batch_position":"100","batch_entry_digest":"f"*64,
           "manifest_record_ref":"coc/manifest/1","manifest_record_position":"101",
           "manifest_content_digest":self.manifest["manifest_content_digest"],"manifest_record_entry_digest":"e"*64,
           "owner_gate_ref":s["owner_gate_ref"],"owner_gate_generation":s["owner_gate_generation"],
           "owner_request_high_water":s["request_high_water"],"owner_admission_high_water":s["admission_high_water"],
           "request_set_digest":s["request_set_digest"],"admission_set_digest":s["admission_set_digest"],
           "request_ledger_root":s["request_ledger_root"],"admission_ledger_root":s["admission_ledger_root"],
           "reconciliation_root":owner_reconciliation_root(self.manifest,"C"),"final_currentness_cas_valid":False}
        self.assertEqual(validate_release(r,self.batch,self.manifest),UNKNOWN)


    def test_EPOCH_01_exact_three_owner_releases_pass(self):
        from unified_manifest_semantics import owner_reconciliation_root
        releases={}
        for owner in ("I","D","C"):
            s=self.snaps[owner]
            releases[owner]={"owner_kind":owner,"release_type":"OUTAGE_ADMISSION_RELEASE_ONLY",
              "batch_record_ref":"coc/batch/1","batch_digest":"a"*64,"batch_position":"100","batch_entry_digest":"f"*64,
              "manifest_record_ref":"coc/manifest/1","manifest_record_position":"101",
              "manifest_content_digest":self.manifest["manifest_content_digest"],"manifest_record_entry_digest":"e"*64,
              "owner_gate_ref":s["owner_gate_ref"],"owner_gate_generation":s["owner_gate_generation"],
              "owner_request_high_water":s["request_high_water"],"owner_admission_high_water":s["admission_high_water"],
              "request_set_digest":s["request_set_digest"],"admission_set_digest":s["admission_set_digest"],
              "request_ledger_root":s["request_ledger_root"],"admission_ledger_root":s["admission_ledger_root"],
              "reconciliation_root":owner_reconciliation_root(self.manifest,owner),"final_currentness_cas_valid":True,
              "coc_record_ref":"release/"+owner}
        completed={"recovery_epoch_ref":"epoch/1","batch_record_ref":"coc/batch/1","batch_digest":"a"*64,
          "batch_position":"100","batch_entry_digest":"f"*64,"manifest_record_ref":"coc/manifest/1",
          "manifest_content_digest":self.manifest["manifest_content_digest"],"manifest_record_position":"101",
          "manifest_record_entry_digest":"e"*64,"owner_release_refs":["release/I","release/D","release/C"],
          "quorum_committed":True}
        self.assertEqual(validate_epoch_completed(completed,self.batch,self.manifest,releases),VALID)
    def test_EPOCH_02_missing_owner_release_fails(self):
        self.assertEqual(validate_epoch_completed({},self.batch,self.manifest,{"I":{},"D":{}}),INVALID)
    def test_EPOCH_03_owner_release_without_currentness_is_unknown(self):
        from unified_manifest_semantics import owner_reconciliation_root
        s=self.snaps["I"]
        r={"owner_kind":"I","release_type":"OUTAGE_ADMISSION_RELEASE_ONLY",
           "batch_record_ref":"coc/batch/1","batch_digest":"a"*64,"batch_position":"100","batch_entry_digest":"f"*64,
           "manifest_record_ref":"coc/manifest/1","manifest_record_position":"101",
           "manifest_content_digest":self.manifest["manifest_content_digest"],"manifest_record_entry_digest":"e"*64,
           "owner_gate_ref":s["owner_gate_ref"],"owner_gate_generation":s["owner_gate_generation"],
           "owner_request_high_water":s["request_high_water"],"owner_admission_high_water":s["admission_high_water"],
           "request_set_digest":s["request_set_digest"],"admission_set_digest":s["admission_set_digest"],
           "request_ledger_root":s["request_ledger_root"],"admission_ledger_root":s["admission_ledger_root"],
           "reconciliation_root":owner_reconciliation_root(self.manifest,"I"),"final_currentness_cas_valid":False}
        self.assertEqual(validate_release(r,self.batch,self.manifest),UNKNOWN)


class ProfileAndProviderTests(unittest.TestCase):
    def setUp(self):self.registry={"I/profile/1":{"status":"ACTIVE","owner_authority":"I","audience":"coc/validator","purpose":"OWNER_LOCAL_GATE_RELEASE","wire_schema_version":"1.3.0"}}
    def test_PROFILE_01_missing_protected_profile_fails(self):
        self.assertEqual(validate_profile({"owner_authority":"I","audience":"coc/validator"},True,self.registry,"I","coc/validator","OWNER_LOCAL_GATE_RELEASE"),INVALID)
    def test_PROFILE_02_unavailable_trust_registry_unknown(self):
        self.assertEqual(validate_profile({"signature_profile_id":"I/profile/1"},True,None,"I","coc/validator","OWNER_LOCAL_GATE_RELEASE"),UNKNOWN)
    def test_PROFILE_03_exact_profile_passes(self):
        m={"signature_profile_id":"I/profile/1","owner_authority":"I","audience":"coc/validator"}
        self.assertEqual(validate_profile(m,True,self.registry,"I","coc/validator","OWNER_LOCAL_GATE_RELEASE"),VALID)
    def test_PROFILE_04_wrong_owner_audience_profile_fails(self):
        m={"signature_profile_id":"I/profile/1","owner_authority":"C","audience":"other"}
        self.assertEqual(validate_profile(m,True,self.registry,"I","coc/validator","OWNER_LOCAL_GATE_RELEASE"),INVALID)
    def test_PROVIDER_01_handoff_accepted_requires_receipt(self):
        m={"message_type":"C_PROVIDER_OUTCOME_RECORDED","owner_authority":"C","c_submit_outcome_ref":"out/1","c_submit_outcome_digest":"a"*64,
           "owner_admission_ref":"C/admit/1","owner_ledger_ref":"C/ledger","owner_ledger_version":"1","owner_local_sequence":"2","owner_high_water":"3",
           "owner_ledger_root":"b"*64,"provider_ref":"p/1","provider_adapter_ref":"a/1","provider_idempotency_key_ref":"key/1",
           "request_digest":"c"*64,"final_request_boundary_id":"boundary/1","provider_outcome_evidence_ref":"e/1",
           "provider_outcome":"HANDOFF_ACCEPTED","provider_request_ref":"req/1","provider_receipt_ref":"receipt/1","participant_reservation_ref":"reservation/1"}
        self.assertEqual(validate_provider_outcome(m),VALID)
    def test_PROVIDER_02_in_doubt_stays_unknown(self):
        m={"message_type":"C_PROVIDER_OUTCOME_RECORDED","owner_authority":"C","c_submit_outcome_ref":"out/1","c_submit_outcome_digest":"a"*64,
           "owner_admission_ref":"C/admit/1","owner_ledger_ref":"C/ledger","owner_ledger_version":"1","owner_local_sequence":"2","owner_high_water":"3",
           "owner_ledger_root":"b"*64,"provider_ref":"p/1","provider_adapter_ref":"a/1","provider_idempotency_key_ref":"key/1",
           "request_digest":"c"*64,"final_request_boundary_id":"boundary/1","provider_outcome_evidence_ref":"e/1",
           "provider_outcome":"IN_DOUBT","unknown_reason_ref":"lookup_unavailable"}
        self.assertEqual(validate_provider_outcome(m),UNKNOWN)


if __name__=="__main__":unittest.main(verbosity=2)
