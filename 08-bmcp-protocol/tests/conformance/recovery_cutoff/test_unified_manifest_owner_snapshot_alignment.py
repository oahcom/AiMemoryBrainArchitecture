"""Regression tests for D Owner Snapshot schema/composed-validator alignment."""
from __future__ import annotations
import sys
import unittest
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
        snapshots={owner:snapshot(owner) for owner in ("I","D","C")}; self.assertEqual(validate_union(composed_manifest(snapshots),[],[],snapshots,membership_proofs={}),VALID)
    def test_07_composed_validate_union_fails_closed_for_legacy_d_snapshot(self):
        snapshots={owner:snapshot(owner) for owner in ("I","D","C")}; snapshots["D"]=snapshot("D",True)
        self.assertEqual(validate_union(composed_manifest(snapshots),[],[],snapshots,membership_proofs={}),UNKNOWN)
    def test_08_digest_mismatch_is_invalid(self):
        s=snapshot("D"); s["owner_specific_high_waters_digest"]="0"*64; self.assertEqual(validate_owner_snapshot(s,"D"),INVALID)

if __name__=="__main__": unittest.main(verbosity=2)
