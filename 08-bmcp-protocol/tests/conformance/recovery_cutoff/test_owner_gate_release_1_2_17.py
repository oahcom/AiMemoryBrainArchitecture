from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "runtime_reference"))

from owner_gate_release_semantics_1_2_17 import (
    INVALID, UNKNOWN, VALID, _td, owner_reconciliation_root, validate_owner_gate_release,
)


def snapshot():
    values = {
        "receipt_issue_high_water": "11",
        "receipt_consume_high_water": "9",
        "permission_epoch": "I-permission-epoch:7",
        "producer_domain_inventory_epoch_ref": "I-inventory-epoch:12",
        "registry_snapshot_digest": "a" * 64,
        "relevant_entry_set_root": "b" * 64,
    }
    return {
        "owner": "I",
        "owner_gate_ref": "I:gate:1",
        "owner_gate_generation": "8",
        "scope_generation_ref": "scope-generation:4",
        "request_high_water": "19",
        "admission_high_water": "17",
        "request_set_digest": "c" * 64,
        "admission_set_digest": "d" * 64,
        "request_ledger_root": "e" * 64,
        "admission_ledger_root": "f" * 64,
        "owner_snapshot_ref": "I:snapshot:19",
        "owner_snapshot_digest": "1" * 64,
        "owner_snapshot_attestation_ref": "I:attestation:19",
        "owner_snapshot_attestation_digest": "2" * 64,
        "owner_ledger_root": "3" * 64,
        "anti_rollback_anchor_ref": "I:anchor:19",
        "owner_specific_high_waters": values,
        "owner_specific_high_waters_digest": _td("OWNER-SPECIFIC-HIGH-WATERS", values),
    }


def owner_snapshot_root(s):
    fields = (
        "owner_snapshot_ref", "owner_snapshot_digest",
        "owner_snapshot_attestation_ref", "owner_snapshot_attestation_digest",
        "owner_gate_generation", "scope_generation_ref",
        "request_high_water", "admission_high_water",
        "request_ledger_root", "admission_ledger_root", "owner_ledger_root",
        "anti_rollback_anchor_ref", "owner_specific_high_waters_digest",
    )
    return {key: s[key] for key in fields}


def batch():
    s = snapshot()
    return {
        "recovery_epoch_ref": "epoch:22",
        "coc_record_ref": "COC:batch:41",
        "payload_digest": "4" * 64,
        "coc_record_position": "41",
        "coc_entry_digest": "5" * 64,
        "prefix": {
            "coordinator_epoch": "term:4",
            "coordinator_index": 40,
            "entry_digest": "a" * 64,
            "committed_configuration_epoch": "config:2",
        },
        "owner_snapshots": {"I": s},
        "manifest_id": "manifest:stable:1",
        "manifest_content_digest": "7" * 64,
        "enumeration_high_water": "enum:40",
        "coc_participant_count": 0,
        "owner_local_admission_count": 0,
        "manifest_member_count": 0,
        "member_set_root": "9" * 64,
    }


def manifest():
    b = batch()
    s = snapshot()
    return {
        "recovery_epoch_ref": "epoch:22",
        "prefix": dict(b["prefix"]),
        "batch_record_ref": b["coc_record_ref"],
        "batch_position": 41,
        "batch_entry_digest": b["coc_entry_digest"],
        "manifest_id": b["manifest_id"],
        "enumeration_high_water": b["enumeration_high_water"],
        "coc_record_ref": "COC:manifest:42",
        "coc_record_position": "42",
        "coc_entry_digest": "6" * 64,
        "manifest_content_digest": b["manifest_content_digest"],
        "coc_participant_count": b["coc_participant_count"],
        "owner_local_admission_count": b["owner_local_admission_count"],
        "manifest_member_count": b["manifest_member_count"],
        "member_set_root": b["member_set_root"],
        "owner_snapshot_roots": {"I": owner_snapshot_root(s)},
        "manifest_members": [],
    }


def release():
    s, b, m = snapshot(), batch(), manifest()
    return {
        "message_type": "OWNER_LOCAL_GATE_RELEASE",
        "owner_kind": "I",
        "release_type": "OUTAGE_ADMISSION_RELEASE_ONLY",
        "owner_gate_ref": s["owner_gate_ref"],
        "owner_gate_generation": s["owner_gate_generation"],
        "recovery_epoch_ref": b["recovery_epoch_ref"],
        "batch_record_ref": b["coc_record_ref"],
        "batch_digest": b["payload_digest"],
        "batch_position": 41,
        "batch_entry_digest": b["coc_entry_digest"],
        "manifest_record_ref": m["coc_record_ref"],
        "manifest_record_position": 42,
        "manifest_record_entry_digest": m["coc_entry_digest"],
        "manifest_content_digest": m["manifest_content_digest"],
        "owner_request_high_water": s["request_high_water"],
        "owner_admission_high_water": s["admission_high_water"],
        "request_set_digest": s["request_set_digest"],
        "admission_set_digest": s["admission_set_digest"],
        "request_ledger_root": s["request_ledger_root"],
        "admission_ledger_root": s["admission_ledger_root"],
        "reconciliation_root": owner_reconciliation_root(m, "I"),
        "owner_signature_ref": "I:sig:release:1",
        "coc_commit_proof_ref": "COC:proof:42",
        "coc_record_ref": "COC:release:43",
        "coc_record_position": "43",
        "coc_entry_digest": "8" * 64,
        "owner_snapshot_ref": s["owner_snapshot_ref"],
        "owner_snapshot_digest": s["owner_snapshot_digest"],
        "owner_snapshot_attestation_ref": s["owner_snapshot_attestation_ref"],
        "owner_snapshot_attestation_digest": s["owner_snapshot_attestation_digest"],
        "owner_ledger_root": s["owner_ledger_root"],
        "scope_generation_ref": s["scope_generation_ref"],
        "anti_rollback_anchor_ref": s["anti_rollback_anchor_ref"],
        "owner_specific_high_waters": dict(s["owner_specific_high_waters"]),
        "owner_specific_high_waters_digest": s["owner_specific_high_waters_digest"],
    }


def validate(r=None, s=None, b=None, m=None, sig=True, coc=True, current=True):
    return validate_owner_gate_release(
        r or release(), b or batch(), m or manifest(), s or snapshot(),
        verify_owner_signature=(lambda *_: sig),
        verify_coc_commit_proof=(lambda *_: coc),
        currentness_cas=(lambda *_: current),
    )


class OwnerGateRelease1217SemanticTests(unittest.TestCase):
    def test_01_exact_owner_release_is_valid(self):
        self.assertEqual(validate(), VALID)

    def test_02_missing_authority_callbacks_returns_unknown(self):
        self.assertEqual(
            validate_owner_gate_release(release(), batch(), manifest(), snapshot()),
            UNKNOWN,
        )

    def test_03_owner_signature_unknown_stays_unknown(self):
        self.assertEqual(validate(sig=None), UNKNOWN)

    def test_04_owner_signature_denial_is_invalid(self):
        self.assertEqual(validate(sig=False), INVALID)

    def test_05_coc_commit_proof_unknown_stays_unknown(self):
        self.assertEqual(validate(coc=None), UNKNOWN)

    def test_06_coc_commit_proof_denial_is_invalid(self):
        self.assertEqual(validate(coc=False), INVALID)

    def test_07_currentness_cas_unavailable_stays_unknown(self):
        self.assertEqual(validate(current=None), UNKNOWN)

    def test_08_stale_currentness_cas_is_invalid(self):
        self.assertEqual(validate(current=False), INVALID)

    def test_09_owner_snapshot_ref_substitution_is_invalid(self):
        r = release(); r["owner_snapshot_ref"] = "I:snapshot:other"
        self.assertEqual(validate(r=r), INVALID)

    def test_10_owner_snapshot_attestation_digest_substitution_is_invalid(self):
        r = release(); r["owner_snapshot_attestation_digest"] = "9" * 64
        self.assertEqual(validate(r=r), INVALID)

    def test_11_scope_generation_substitution_is_invalid(self):
        r = release(); r["scope_generation_ref"] = "scope-generation:other"
        self.assertEqual(validate(r=r), INVALID)

    def test_12_anti_rollback_anchor_substitution_is_invalid(self):
        r = release(); r["anti_rollback_anchor_ref"] = "I:anchor:other"
        self.assertEqual(validate(r=r), INVALID)

    def test_13_permission_epoch_substitution_is_invalid(self):
        r = release(); r["owner_specific_high_waters"]["permission_epoch"] = "I-permission-epoch:other"
        self.assertEqual(validate(r=r), INVALID)

    def test_14_owner_specific_highwaters_digest_substitution_is_invalid(self):
        r = release(); r["owner_specific_high_waters_digest"] = "a" * 64
        self.assertEqual(validate(r=r), INVALID)

    def test_15_batch_record_ref_substitution_is_invalid(self):
        r = release(); r["batch_record_ref"] = "COC:batch:other"
        self.assertEqual(validate(r=r), INVALID)

    def test_16_batch_position_substitution_is_invalid(self):
        r = release(); r["batch_position"] = 99
        self.assertEqual(validate(r=r), INVALID)

    def test_17_manifest_entry_digest_substitution_is_invalid(self):
        r = release(); r["manifest_record_entry_digest"] = "b" * 64
        self.assertEqual(validate(r=r), INVALID)

    def test_18_reconciliation_root_substitution_is_invalid(self):
        r = release(); r["reconciliation_root"] = "c" * 64
        self.assertEqual(validate(r=r), INVALID)

    def test_19_wrong_owner_is_invalid(self):
        r = release(); r["owner_kind"] = "D"
        self.assertEqual(validate(r=r), INVALID)

    def test_20_wrong_release_type_is_invalid(self):
        r = release(); r["release_type"] = "GLOBAL_FORGET_CLEARANCE"
        self.assertEqual(validate(r=r), INVALID)

    def test_21_missing_required_release_binding_stays_unknown(self):
        r = release(); r.pop("scope_generation_ref")
        self.assertEqual(validate(r=r), UNKNOWN)

    def test_22_wrong_manifest_record_position_is_invalid(self):
        m = manifest(); m["coc_record_position"] = "44"
        self.assertEqual(validate(m=m), INVALID)

    def test_23_manifest_must_backlink_to_exact_batch_record(self):
        m = manifest(); m["batch_record_ref"] = "COC:batch:other"
        self.assertEqual(validate(m=m), INVALID)

    def test_24_manifest_must_bind_exact_batch_position(self):
        m = manifest(); m["batch_position"] = 39
        self.assertEqual(validate(m=m), INVALID)

    def test_25_manifest_must_bind_exact_batch_entry_digest(self):
        m = manifest(); m["batch_entry_digest"] = "a" * 64
        self.assertEqual(validate(m=m), INVALID)

    def test_26_manifest_and_batch_must_share_manifest_id(self):
        m = manifest(); m["manifest_id"] = "manifest:other"
        self.assertEqual(validate(m=m), INVALID)

    def test_27_manifest_and_batch_must_share_content_digest(self):
        m = manifest(); m["manifest_content_digest"] = "b" * 64
        self.assertEqual(validate(m=m), INVALID)

    def test_28_manifest_and_batch_must_share_exact_prefix(self):
        m = manifest(); m["prefix"]["coordinator_index"] = 39
        self.assertEqual(validate(m=m), INVALID)

    def test_29_manifest_must_commit_after_batch(self):
        m = manifest(); m["coc_record_position"] = "40"
        self.assertEqual(validate(m=m), INVALID)

    def test_30_batch_must_contain_exact_owner_snapshot(self):
        b = batch(); b["owner_snapshots"]["I"]["scope_generation_ref"] = "scope:other"
        self.assertEqual(validate(b=b), INVALID)

    def test_31_manifest_owner_snapshot_root_must_match_snapshot(self):
        m = manifest(); m["owner_snapshot_roots"]["I"]["owner_snapshot_digest"] = "9" * 64
        self.assertEqual(validate(m=m), INVALID)

    def test_32_owner_signature_callback_exception_is_unknown(self):
        self.assertEqual(validate_owner_gate_release(
            release(), batch(), manifest(), snapshot(),
            verify_owner_signature=lambda *_: (_ for _ in ()).throw(RuntimeError("I unavailable")),
            verify_coc_commit_proof=lambda *_: True,
            currentness_cas=lambda *_: True,
        ), UNKNOWN)

    def test_33_coc_proof_callback_exception_is_unknown(self):
        self.assertEqual(validate_owner_gate_release(
            release(), batch(), manifest(), snapshot(),
            verify_owner_signature=lambda *_: True,
            verify_coc_commit_proof=lambda *_: (_ for _ in ()).throw(RuntimeError("COC unavailable")),
            currentness_cas=lambda *_: True,
        ), UNKNOWN)

    def test_34_currentness_callback_exception_is_unknown(self):
        self.assertEqual(validate_owner_gate_release(
            release(), batch(), manifest(), snapshot(),
            verify_owner_signature=lambda *_: True,
            verify_coc_commit_proof=lambda *_: True,
            currentness_cas=lambda *_: (_ for _ in ()).throw(RuntimeError("owner currentness unavailable")),
        ), UNKNOWN)


if __name__ == "__main__":
    unittest.main(verbosity=2)
