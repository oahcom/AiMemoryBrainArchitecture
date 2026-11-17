from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "runtime_reference"))

from owner_snapshot_semantics_1_2_17 import (
    INVALID, UNKNOWN, VALID, OWNER_FIELDS, _td, validate_owner_snapshot_1_2_17,
)


def owner_values(owner):
    if owner == "I":
        return {
            "receipt_issue_high_water": "11",
            "receipt_consume_high_water": "9",
            "permission_epoch": "I-permission-epoch:7",
            "producer_domain_inventory_epoch_ref": "I-inventory-epoch:12",
            "registry_snapshot_digest": "a" * 64,
            "relevant_entry_set_root": "b" * 64,
        }
    if owner == "D":
        return {
            "producer_registration_high_water": "8",
            "work_item_high_water": "12",
            "attempt_high_water": "17",
            "barrier_generation": "4",
            "barrier_root": "c" * 64,
            "forget_fence_generation_high_water": "5",
            "dependency_closure_cursor": "D-cursor:12",
            "dependency_closure_root": "d" * 64,
        }
    return {
        "reservation_high_water": "21",
        "provider_attempt_high_water": "34",
        "provider_outcome_high_water": "31",
        "provider_idempotency_namespace_ref": "C-provider-namespace:4",
        "final_request_boundary_generation": "7",
    }


def snapshot(owner="I"):
    values = owner_values(owner)
    return {
        "owner": owner,
        "owner_gate_ref": f"{owner}:gate:1",
        "owner_gate_generation": "8",
        "scope_generation_ref": f"{owner}:scope-generation:4",
        "request_high_water": "19",
        "request_count": "19",
        "request_set_digest": "e" * 64,
        "request_ledger_root": "f" * 64,
        "admission_high_water": "17",
        "admission_count": "17",
        "admission_set_digest": "1" * 64,
        "admission_ledger_root": "2" * 64,
        "owner_snapshot_ref": f"{owner}:snapshot:19",
        "owner_snapshot_digest": "3" * 64,
        "owner_snapshot_attestation_ref": f"{owner}:attestation:19",
        "owner_snapshot_attestation_digest": "4" * 64,
        "owner_ledger_root": "5" * 64,
        "anti_rollback_anchor_ref": f"{owner}:anchor:19",
        "owner_specific_high_waters": values,
        "owner_specific_high_waters_digest": _td("OWNER-SPECIFIC-HIGH-WATERS", values),
    }


def validate(s=None, owner="I", attestation=True, current=True, anchor=True):
    return validate_owner_snapshot_1_2_17(
        s or snapshot(owner), owner,
        verify_attestation=(lambda *_: attestation),
        verify_ledger_currentness=(lambda *_: current),
        verify_anti_rollback=(lambda *_: anchor),
    )


class OwnerSnapshot1217SemanticTests(unittest.TestCase):
    def test_01_exact_i_snapshot_is_valid(self):
        self.assertEqual(validate(), VALID)

    def test_02_exact_d_snapshot_is_valid(self):
        self.assertEqual(validate(snapshot("D"), "D"), VALID)

    def test_03_exact_c_snapshot_is_valid(self):
        self.assertEqual(validate(snapshot("C"), "C"), VALID)

    def test_04_missing_authority_callbacks_returns_unknown(self):
        self.assertEqual(validate_owner_snapshot_1_2_17(snapshot(), "I"), UNKNOWN)

    def test_05_wrong_owner_is_invalid(self):
        self.assertEqual(validate(snapshot("I"), "D"), INVALID)

    def test_06_missing_scope_generation_is_unknown(self):
        s = snapshot(); s.pop("scope_generation_ref")
        self.assertEqual(validate(s), UNKNOWN)

    def test_07_missing_permission_epoch_is_invalid(self):
        s = snapshot(); s["owner_specific_high_waters"].pop("permission_epoch")
        s["owner_specific_high_waters_digest"] = _td("OWNER-SPECIFIC-HIGH-WATERS", s["owner_specific_high_waters"])
        self.assertEqual(validate(s), INVALID)

    def test_08_missing_dependency_closure_root_is_invalid(self):
        s = snapshot("D"); s["owner_specific_high_waters"].pop("dependency_closure_root")
        s["owner_specific_high_waters_digest"] = _td("OWNER-SPECIFIC-HIGH-WATERS", s["owner_specific_high_waters"])
        self.assertEqual(validate(s, "D"), INVALID)

    def test_09_missing_provider_namespace_is_invalid(self):
        s = snapshot("C"); s["owner_specific_high_waters"].pop("provider_idempotency_namespace_ref")
        s["owner_specific_high_waters_digest"] = _td("OWNER-SPECIFIC-HIGH-WATERS", s["owner_specific_high_waters"])
        self.assertEqual(validate(s, "C"), INVALID)

    def test_10_extra_owner_specific_field_is_invalid(self):
        s = snapshot(); s["owner_specific_high_waters"]["extra"] = "unexpected"
        s["owner_specific_high_waters_digest"] = _td("OWNER-SPECIFIC-HIGH-WATERS", s["owner_specific_high_waters"])
        self.assertEqual(validate(s), INVALID)

    def test_11_owner_specific_digest_mismatch_is_invalid(self):
        s = snapshot(); s["owner_specific_high_waters_digest"] = "a" * 64
        self.assertEqual(validate(s), INVALID)

    def test_12_malformed_snapshot_digest_is_invalid(self):
        s = snapshot(); s["owner_snapshot_digest"] = "not-a-digest"
        self.assertEqual(validate(s), INVALID)

    def test_13_non_decimal_request_highwater_is_invalid(self):
        s = snapshot(); s["request_high_water"] = "19x"
        self.assertEqual(validate(s), INVALID)

    def test_14_non_decimal_owner_gate_generation_is_invalid(self):
        s = snapshot(); s["owner_gate_generation"] = "generation-eight"
        self.assertEqual(validate(s), INVALID)

    def test_15_owner_attestation_unknown_stays_unknown(self):
        self.assertEqual(validate(attestation=None), UNKNOWN)

    def test_16_owner_attestation_denial_is_invalid(self):
        self.assertEqual(validate(attestation=False), INVALID)

    def test_17_anti_rollback_unavailable_stays_unknown(self):
        self.assertEqual(validate(anchor=None), UNKNOWN)

    def test_18_anti_rollback_denial_is_invalid(self):
        self.assertEqual(validate(anchor=False), INVALID)

    def test_19_owner_ledger_currentness_unavailable_stays_unknown(self):
        self.assertEqual(validate(current=None), UNKNOWN)

    def test_20_stale_owner_ledger_currentness_stays_unknown(self):
        self.assertEqual(validate(current=False), UNKNOWN)

    def test_21_i_permission_epoch_is_not_numeric(self):
        s = snapshot()
        s["owner_specific_high_waters"]["permission_epoch"] = "I-epoch:alpha"
        s["owner_specific_high_waters_digest"] = _td("OWNER-SPECIFIC-HIGH-WATERS", s["owner_specific_high_waters"])
        self.assertEqual(validate(s), VALID)

    def test_22_d_dependency_cursor_is_opaque_not_numeric(self):
        s = snapshot("D")
        s["owner_specific_high_waters"]["dependency_closure_cursor"] = "cursor:opaque/alpha"
        s["owner_specific_high_waters_digest"] = _td("OWNER-SPECIFIC-HIGH-WATERS", s["owner_specific_high_waters"])
        self.assertEqual(validate(s, "D"), VALID)


if __name__ == "__main__":
    unittest.main(verbosity=2)
