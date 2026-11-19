"""Regression tests for D Owner Snapshot schema/composed-validator alignment."""
from __future__ import annotations
import json
import sys
import unittest
from jsonschema import Draft202012Validator, ValidationError
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "runtime_reference"))
from unified_manifest_semantics import (
    INVALID, UNKNOWN, VALID, content_digest, snapshot_root, td,
    validate_owner_snapshot, validate_union,
)

def owner_values(owner):
    return {
        "I": {"receipt_issue_high_water":"11","receipt_consume_high_water":"9","inventory_epoch_ref":"I-inventory:12","registry_snapshot_digest":"a"*64,"relevant_entry_set_root":"b"*64},
        "D": {"producer_registration_high_water":"8","work_item_high_water":"12","attempt_high_water":"17","barrier_generation":"4","barrier_root":"c"*64,"forget_fence_generation_high_water":"5","dependency_closure_cursor":"D-cursor:12","dependency_closure_root":"d"*64},
        "C": {"reservation_high_water":"21","provider_attempt_high_water":"34","provider_outcome_high_water":"31"},
    }[owner]

def snapshot(owner, legacy_d=False):
    values=owner_values(owner)
    if legacy_d and owner=="D":
        values={k:v for k,v in values.items() if k not in {"forget_fence_generation_high_water","dependency_closure_cursor","dependency_closure_root"}}
    return {"owner":owner,"owner_specific_high_waters":values,"owner_specific_high_waters_digest":td("OWNER-SPECIFIC-HIGH-WATERS",values),
      "owner_snapshot_ref":owner+":snapshot:1","owner_snapshot_digest":"e"*64,"owner_snapshot_attestation_ref":owner+":attestation:1",
      "owner_snapshot_attestation_digest":"f"*64,"owner_gate_generation":"4","request_high_water":"19","admission_high_water":"17",
      "request_ledger_root":"1"*64,"admission_ledger_root":"2"*64,"owner_ledger_root":"3"*64,"anti_rollback_anchor_ref":owner+":anchor:1",
      "ledger_available":True,"pagination_complete":True}

def schema_d_snapshot():
    values=owner_values("D")
    return {
        "owner":"D", "owner_gate_ref":"D:gate:1", "owner_gate_generation":"4",
        "scope_generation_ref":"D:scope:1", "request_high_water":"19", "request_count":19,
        "request_set_digest":"a"*64, "owner_snapshot_attestation_ref":"D:attestation:1",
        "anti_rollback_anchor_ref":"D:anchor:1", "owner_ledger_root":"b"*64,
        "admission_high_water":"17", "admission_count":17, "admission_set_digest":"c"*64,
        "request_ledger_root":"d"*64, "admission_ledger_root":"e"*64,
        "owner_snapshot_attestation_digest":"f"*64,
        "owner_specific_high_waters":values,
        "owner_specific_high_waters_digest":td("OWNER-SPECIFIC-HIGH-WATERS",values),
    }

def composed_manifest(snapshots):
    roots={owner:snapshot_root(s) for owner,s in snapshots.items()}
    m={"manifest_id":"manifest:1","recovery_epoch_ref":"epoch:1","prefix":{"coordinator_epoch":"coc:1","coordinator_index":1,"entry_digest":"4"*64,"committed_configuration_epoch":"q:1"},
       "enumeration_high_water":"1","coc_participant_count":0,"owner_local_admission_count":0,"manifest_member_count":0,
       "owner_snapshot_roots":roots,"manifest_members":[]}
    m["member_set_root"]=td("MANIFEST-MEMBER-SET",[])
    m["manifest_content_digest"]=content_digest(m)
    return m

class DOwnerSnapshotAlignmentTests(unittest.TestCase):
    def test_01_eight_field_d_snapshot_is_valid(self): self.assertEqual(validate_owner_snapshot(snapshot("D"),"D"),VALID)
    def test_02_legacy_five_field_d_snapshot_is_unknown_not_valid(self): self.assertEqual(validate_owner_snapshot(snapshot("D",True),"D"),UNKNOWN)
    def test_03_each_missing_new_d_field_is_invalid(self):
        for field in ("forget_fence_generation_high_water","dependency_closure_cursor","dependency_closure_root"):
            with self.subTest(field=field):
                s=snapshot("D"); s["owner_specific_high_waters"].pop(field); s["owner_specific_high_waters_digest"]=td("OWNER-SPECIFIC-HIGH-WATERS",s["owner_specific_high_waters"])
                self.assertEqual(validate_owner_snapshot(s,"D"),INVALID)
    def test_04_extra_d_field_is_invalid(self):
        s=snapshot("D"); s["owner_specific_high_waters"]["unexpected"]="1"; s["owner_specific_high_waters_digest"]=td("OWNER-SPECIFIC-HIGH-WATERS",s["owner_specific_high_waters"])
        self.assertEqual(validate_owner_snapshot(s,"D"),INVALID)
    def test_05_d_highwater_values_are_not_cross_compared_or_coerced(self):
        s=snapshot("D"); s["owner_specific_high_waters"]["producer_registration_high_water"]="8"; s["owner_specific_high_waters"]["forget_fence_generation_high_water"]="8"
        s["owner_specific_high_waters_digest"]=td("OWNER-SPECIFIC-HIGH-WATERS",s["owner_specific_high_waters"]); self.assertEqual(validate_owner_snapshot(s,"D"),VALID)
        s["owner_specific_high_waters"]["forget_fence_generation_high_water"]="9"; s["owner_specific_high_waters_digest"]=td("OWNER-SPECIFIC-HIGH-WATERS",s["owner_specific_high_waters"])
        self.assertEqual(validate_owner_snapshot(s,"D"),VALID)
    def test_06_composed_validate_union_accepts_eight_field_d_snapshot(self):
        snapshots={owner:snapshot(owner) for owner in ("I","D","C")}; self.assertEqual(validate_union(composed_manifest(snapshots),[],[],snapshots,membership_proofs={},verify_owner_snapshot=lambda *_: True),VALID)
    def test_07_composed_validate_union_fails_closed_for_legacy_d_snapshot(self):
        snapshots={owner:snapshot(owner) for owner in ("I","D","C")}; snapshots["D"]=snapshot("D",True)
        self.assertEqual(validate_union(composed_manifest(snapshots),[],[],snapshots,membership_proofs={}),UNKNOWN)
    def test_08_missing_owner_authority_callback_is_unknown(self):
        snapshots={owner:snapshot(owner) for owner in ("I","D","C")}
        self.assertEqual(validate_union(composed_manifest(snapshots),[],[],snapshots,membership_proofs={}),UNKNOWN)

    def test_09_owner_currentness_unavailable_or_exception_is_unknown(self):
        snapshots={owner:snapshot(owner) for owner in ("I","D","C")}
        for callback in (lambda *_: UNKNOWN, lambda *_: (_ for _ in ()).throw(RuntimeError("authority unavailable"))):
            self.assertEqual(validate_union(composed_manifest(snapshots),[],[],snapshots,membership_proofs={},verify_owner_snapshot=callback),UNKNOWN)

    def test_10_owner_authority_denial_is_invalid(self):
        snapshots={owner:snapshot(owner) for owner in ("I","D","C")}
        self.assertEqual(validate_union(composed_manifest(snapshots),[],[],snapshots,membership_proofs={},verify_owner_snapshot=lambda *_: False),INVALID)

    def test_11_legacy_five_field_snapshot_requires_explicit_legacy_opt_in(self):
        self.assertEqual(validate_owner_snapshot(snapshot("D",True),"D",allow_legacy_d_snapshot=True),VALID)

    def test_legacy_opt_in_rejects_513_character_values_in_both_validation_paths(self):
        bounded_legacy_fields = (
            "producer_registration_high_water",
            "work_item_high_water",
            "attempt_high_water",
            "barrier_generation",
        )
        for field in bounded_legacy_fields:
            with self.subTest(field=field):
                direct = snapshot("D", True)
                direct["owner_specific_high_waters"][field] = "x" * 513
                direct["owner_specific_high_waters_digest"] = td(
                    "OWNER-SPECIFIC-HIGH-WATERS", direct["owner_specific_high_waters"]
                )
                self.assertEqual(
                    validate_owner_snapshot(direct, "D", allow_legacy_d_snapshot=True),
                    INVALID,
                )

                snapshots = {owner: snapshot(owner) for owner in ("I", "D", "C")}
                snapshots["D"] = snapshot("D", True)
                snapshots["D"]["owner_specific_high_waters"][field] = "x" * 513
                snapshots["D"]["owner_specific_high_waters_digest"] = td(
                    "OWNER-SPECIFIC-HIGH-WATERS", snapshots["D"]["owner_specific_high_waters"]
                )
                self.assertEqual(
                    validate_union(
                        composed_manifest(snapshots), [], [], snapshots,
                        membership_proofs={}, verify_owner_snapshot=lambda *_: True,
                        allow_legacy_d_snapshot=True,
                    ),
                    INVALID,
                )

    def test_13_schema_accepts_exact_eight_field_d_snapshot(self):
        schema_path=ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.17.schema.json"
        schema=json.loads(schema_path.read_text(encoding="utf-8"))
        validator=Draft202012Validator({"$schema":schema["$schema"],"$defs":schema["$defs"],"$ref":"#/$defs/ownerSnapshot"})
        validator.validate(schema_d_snapshot())

    def test_14_schema_rejects_legacy_five_field_d_snapshot(self):
        schema_path=ROOT / "schemas" / "bmcp.coc-jf10-unified-1.2.17.schema.json"
        schema=json.loads(schema_path.read_text(encoding="utf-8"))
        validator=Draft202012Validator({"$schema":schema["$schema"],"$defs":schema["$defs"],"$ref":"#/$defs/ownerSnapshot"})
        wire=schema_d_snapshot()
        wire["owner_specific_high_waters"]={k:v for k,v in wire["owner_specific_high_waters"].items() if k not in {
            "forget_fence_generation_high_water","dependency_closure_cursor","dependency_closure_root"}}
        wire["owner_specific_high_waters_digest"]=td("OWNER-SPECIFIC-HIGH-WATERS",wire["owner_specific_high_waters"])
        with self.assertRaises(ValidationError): validator.validate(wire)

    def assert_d_bounded_field_rejected_by_both_paths(self, field):
        direct = snapshot("D")
        direct["owner_specific_high_waters"][field] = "x" * 513
        direct["owner_specific_high_waters_digest"] = td("OWNER-SPECIFIC-HIGH-WATERS", direct["owner_specific_high_waters"])
        self.assertEqual(validate_owner_snapshot(direct, "D"), INVALID)

        snapshots = {owner: snapshot(owner) for owner in ("I", "D", "C")}
        snapshots["D"]["owner_specific_high_waters"][field] = "x" * 513
        snapshots["D"]["owner_specific_high_waters_digest"] = td(
            "OWNER-SPECIFIC-HIGH-WATERS", snapshots["D"]["owner_specific_high_waters"]
        )
        manifest = composed_manifest(snapshots)
        self.assertEqual(
            validate_union(
                manifest, [], [], snapshots, membership_proofs={},
                verify_owner_snapshot=lambda *_: True,
            ),
            INVALID,
        )

    def test_rejects_513_producer_registration_high_water_in_owner_snapshot_and_union(self):
        self.assert_d_bounded_field_rejected_by_both_paths("producer_registration_high_water")

    def test_rejects_513_work_item_high_water_in_owner_snapshot_and_union(self):
        self.assert_d_bounded_field_rejected_by_both_paths("work_item_high_water")

    def test_rejects_513_attempt_high_water_in_owner_snapshot_and_union(self):
        self.assert_d_bounded_field_rejected_by_both_paths("attempt_high_water")

    def test_rejects_513_barrier_generation_in_owner_snapshot_and_union(self):
        self.assert_d_bounded_field_rejected_by_both_paths("barrier_generation")

    def test_rejects_513_forget_fence_generation_high_water_in_owner_snapshot_and_union(self):
        self.assert_d_bounded_field_rejected_by_both_paths("forget_fence_generation_high_water")

    def test_rejects_513_dependency_closure_cursor_in_owner_snapshot_and_union(self):
        self.assert_d_bounded_field_rejected_by_both_paths("dependency_closure_cursor")

    def test_15_malformed_dependency_closure_root_is_invalid(self):
        s=snapshot("D")
        s["owner_specific_high_waters"]["dependency_closure_root"]="not-a-sha256"
        s["owner_specific_high_waters_digest"]=td("OWNER-SPECIFIC-HIGH-WATERS",s["owner_specific_high_waters"])
        self.assertEqual(validate_owner_snapshot(s,"D"),INVALID)

    def test_12_digest_mismatch_is_invalid(self):
        s=snapshot("D"); s["owner_specific_high_waters_digest"]="0"*64; self.assertEqual(validate_owner_snapshot(s,"D"),INVALID)

if __name__=="__main__": unittest.main(verbosity=2)
