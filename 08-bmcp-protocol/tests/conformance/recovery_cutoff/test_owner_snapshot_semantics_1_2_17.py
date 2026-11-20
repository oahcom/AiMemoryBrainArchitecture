"""Independent regression tests for D bounded fields in H 1.2.17 snapshots."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "runtime_reference"))

from owner_snapshot_semantics_1_2_17 import (  # noqa: E402
    INVALID, UNKNOWN, VALID, _td, validate_owner_snapshot_1_2_17,
)

NON_TYPED_BOUNDED_FIELDS = (
    "dependency_closure_cursor",
)

ALL_BOUNDED_FIELDS = (
    "producer_registration_high_water",
    "work_item_high_water",
    "attempt_high_water",
    "barrier_generation",
    "forget_fence_generation_high_water",
    "dependency_closure_cursor",
)


def d_snapshot():
    values = {
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
        "owner": "D",
        "owner_gate_ref": "D:gate:1",
        "owner_gate_generation": "4",
        "scope_generation_ref": "D:scope:1",
        "request_high_water": "19",
        "request_count": "19",
        "request_set_digest": "a" * 64,
        "request_ledger_root": "b" * 64,
        "admission_high_water": "17",
        "admission_count": "17",
        "admission_set_digest": "c" * 64,
        "admission_ledger_root": "d" * 64,
        "owner_snapshot_ref": "D:snapshot:1",
        "owner_snapshot_digest": "e" * 64,
        "owner_snapshot_attestation_ref": "D:attestation:1",
        "owner_snapshot_attestation_digest": "f" * 64,
        "owner_ledger_root": "1" * 64,
        "anti_rollback_anchor_ref": "D:anchor:1",
        "owner_specific_high_waters": values,
        "owner_specific_high_waters_digest": _td("OWNER-SPECIFIC-HIGH-WATERS", values),
    }


def true_authorities(calls):
    def callback(name):
        def verify(*_args):
            calls.append(name)
            return True
        return verify

    return {
        "verify_attestation": callback("attestation"),
        "verify_ledger_currentness": callback("ledger_currentness"),
        "verify_anti_rollback": callback("anti_rollback"),
    }


class DOwnerSnapshotBoundedFieldTests(unittest.TestCase):
    def test_513_character_values_with_recomputed_digest_are_invalid_before_authority_callbacks(self):
        for field in NON_TYPED_BOUNDED_FIELDS:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                snapshot["owner_specific_high_waters"][field] = "1" * 513
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS",
                    snapshot["owner_specific_high_waters"],
                )
                self.assertEqual(
                    snapshot["owner_specific_high_waters_digest"],
                    _td("OWNER-SPECIFIC-HIGH-WATERS", snapshot["owner_specific_high_waters"]),
                )
                calls = []
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities(calls)),
                    INVALID,
                )
                self.assertEqual(calls, [])

    def test_empty_string_is_invalid_for_each_bounded_field(self):
        for field in ALL_BOUNDED_FIELDS:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                snapshot["owner_specific_high_waters"][field] = ""
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS",
                    snapshot["owner_specific_high_waters"],
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    INVALID,
                )

    def test_length_one_is_accepted_for_each_bounded_field(self):
        for field in ALL_BOUNDED_FIELDS:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                snapshot["owner_specific_high_waters"][field] = "1"
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS",
                    snapshot["owner_specific_high_waters"],
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    VALID,
                )

    def test_length_512_is_accepted_for_each_non_typed_bounded_field(self):
        for field in NON_TYPED_BOUNDED_FIELDS:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                snapshot["owner_specific_high_waters"][field] = "1" * 512
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS",
                    snapshot["owner_specific_high_waters"],
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    VALID,
                )

    def test_length_513_is_invalid_for_each_non_typed_bounded_field(self):
        for field in NON_TYPED_BOUNDED_FIELDS:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                snapshot["owner_specific_high_waters"][field] = "1" * 513
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS",
                    snapshot["owner_specific_high_waters"],
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    INVALID,
                )



    def test_all_five_d_high_waters_accept_zero_and_signed_64_maximum(self):
        fields = (
            "producer_registration_high_water",
            "work_item_high_water",
            "attempt_high_water",
            "barrier_generation",
            "forget_fence_generation_high_water",
        )
        for field in fields:
            for value in ("0", str((1 << 63) - 1)):
                with self.subTest(field=field, value=value):
                    snapshot = d_snapshot()
                    snapshot["owner_specific_high_waters"][field] = value
                    snapshot["owner_specific_high_waters_digest"] = _td(
                        "OWNER-SPECIFIC-HIGH-WATERS", snapshot["owner_specific_high_waters"]
                    )
                    self.assertEqual(
                        validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                        VALID,
                    )

    def test_all_five_d_high_waters_reject_values_above_signed_64_maximum(self):
        fields = (
            "producer_registration_high_water",
            "work_item_high_water",
            "attempt_high_water",
            "barrier_generation",
            "forget_fence_generation_high_water",
        )
        for field in fields:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                snapshot["owner_specific_high_waters"][field] = str(1 << 63)
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS", snapshot["owner_specific_high_waters"]
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    INVALID,
                )

    def test_leading_zero_d_values_are_accepted_and_canonicalized_before_digest_projection(self):
        fields = (
            "producer_registration_high_water",
            "work_item_high_water",
            "attempt_high_water",
            "barrier_generation",
            "forget_fence_generation_high_water",
        )
        for field in fields:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                values = snapshot["owner_specific_high_waters"]
                values[field] = "000" + values[field]
                canonical_projection = dict(values)
                canonical_projection[field] = str(int(values[field]))
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS", canonical_projection
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    VALID,
                )
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS", values
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    INVALID,
                )

    def test_invalid_d_decimal_forms_are_rejected(self):
        for value in ("-1", "+8", "", " 8", "8 ", "8.0", "8e0", "١", "1_0"):
            with self.subTest(value=value):
                snapshot = d_snapshot()
                snapshot["owner_specific_high_waters"]["producer_registration_high_water"] = value
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS", snapshot["owner_specific_high_waters"]
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    INVALID,
                )

    def test_existing_legal_d_snapshot_remains_valid(self):
        self.assertEqual(
            validate_owner_snapshot_1_2_17(d_snapshot(), "D", **true_authorities([])),
            VALID,
        )

    def test_missing_authority_callback_remains_unknown(self):
        self.assertEqual(validate_owner_snapshot_1_2_17(d_snapshot(), "D"), UNKNOWN)

    def test_existing_digest_mismatch_remains_invalid(self):
        snapshot = d_snapshot()
        snapshot["owner_specific_high_waters_digest"] = "0" * 64
        self.assertEqual(
            validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
            INVALID,
        )

    def test_digest_and_root_fields_keep_their_existing_sha256_validation(self):
        snapshot = d_snapshot()
        self.assertEqual(len(snapshot["owner_specific_high_waters"]["barrier_root"]), 64)
        self.assertEqual(len(snapshot["owner_specific_high_waters"]["dependency_closure_root"]), 64)
        self.assertEqual(
            validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
            VALID,
        )


    def test_all_five_d_high_waters_accept_512_char_leading_zero_input_when_canonical_value_is_in_range(self):
        fields = (
            "producer_registration_high_water",
            "work_item_high_water",
            "attempt_high_water",
            "barrier_generation",
            "forget_fence_generation_high_water",
        )
        for field in fields:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                values = snapshot["owner_specific_high_waters"]
                values[field] = "0" * 511 + "8"
                canonical_projection = dict(values)
                canonical_projection[field] = "8"
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS", canonical_projection
                )
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities([])),
                    VALID,
                )

    def test_all_five_d_high_waters_reject_513_char_input_before_authority_callbacks(self):
        fields = (
            "producer_registration_high_water",
            "work_item_high_water",
            "attempt_high_water",
            "barrier_generation",
            "forget_fence_generation_high_water",
        )
        for field in fields:
            with self.subTest(field=field):
                snapshot = d_snapshot()
                values = snapshot["owner_specific_high_waters"]
                values[field] = "0" * 512 + "8"
                snapshot["owner_specific_high_waters_digest"] = _td(
                    "OWNER-SPECIFIC-HIGH-WATERS", values
                )
                calls = []
                self.assertEqual(
                    validate_owner_snapshot_1_2_17(snapshot, "D", **true_authorities(calls)),
                    INVALID,
                )
                self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
