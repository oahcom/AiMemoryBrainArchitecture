"""Regression coverage for versioned owner-snapshot field sets in the composed validator."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "runtime_reference"))

from unified_manifest_semantics import (  # noqa: E402
    INVALID, UNKNOWN, VALID, content_digest, snapshot_root, td,
    validate_owner_snapshot, validate_union,
)


def values(owner, revision):
    if owner == "I" and revision == "1.2.9":
        return {
            "receipt_issue_high_water": "11",
            "receipt_consume_high_water": "9",
            "inventory_epoch_ref": "I-inventory:12",
            "registry_snapshot_digest": "a" * 64,
            "relevant_entry_set_root": "b" * 64,
        }
    if owner == "I":
        return {
            "receipt_issue_high_water": "11",
            "receipt_consume_high_water": "9",
            "permission_epoch": "I-permission:7",
            "producer_domain_inventory_epoch_ref": "I-inventory:12",
            "registry_snapshot_digest": "a" * 64,
            "relevant_entry_set_root": "b" * 64,
        }
    if owner == "C" and revision == "1.2.9":
        return {
            "reservation_high_water": "21",
            "provider_attempt_high_water": "34",
            "provider_outcome_high_water": "31",
        }
    if owner == "C":
        return {
            "reservation_high_water": "21",
            "provider_attempt_high_water": "34",
            "provider_outcome_high_water": "31",
            "provider_idempotency_namespace_ref": "C-provider-namespace:4",
            "final_request_boundary_generation": "7",
        }
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


def snapshot(owner, revision):
    high_waters = values(owner, revision)
    return {
        "owner": owner,
        "owner_gate_generation": "4",
        "request_high_water": "19",
        "admission_high_water": "17",
        "request_ledger_root": "1" * 64,
        "admission_ledger_root": "2" * 64,
        "owner_snapshot_ref": f"{owner}:snapshot:1",
        "owner_snapshot_digest": "e" * 64,
        "owner_snapshot_attestation_ref": f"{owner}:attestation:1",
        "owner_snapshot_attestation_digest": "f" * 64,
        "owner_ledger_root": "3" * 64,
        "anti_rollback_anchor_ref": f"{owner}:anchor:1",
        "owner_specific_high_waters": high_waters,
        "owner_specific_high_waters_digest": td("OWNER-SPECIFIC-HIGH-WATERS", high_waters),
        "ledger_available": True,
        "pagination_complete": True,
    }


def composed_manifest(snapshots):
    manifest = {
        "manifest_id": "manifest:1",
        "recovery_epoch_ref": "epoch:1",
        "prefix": {"coordinator_epoch": "coc:1", "coordinator_index": 1,
                   "entry_digest": "4" * 64, "committed_configuration_epoch": "q:1"},
        "enumeration_high_water": "1",
        "coc_participant_count": 0,
        "owner_local_admission_count": 0,
        "manifest_member_count": 0,
        "owner_snapshot_roots": {owner: snapshot_root(s) for owner, s in snapshots.items()},
        "manifest_members": [],
    }
    manifest["member_set_root"] = td("MANIFEST-MEMBER-SET", [])
    manifest["manifest_content_digest"] = content_digest(manifest)
    return manifest


class UnifiedManifest1217ComposedEntryTests(unittest.TestCase):
    def test_01_legacy_i_and_c_sets_remain_valid_only_in_129_mode(self):
        for owner in ("I", "C"):
            with self.subTest(owner=owner):
                self.assertEqual(
                    validate_owner_snapshot(snapshot(owner, "1.2.9"), owner),
                    VALID,
                )
                self.assertEqual(
                    validate_owner_snapshot(
                        snapshot(owner, "1.2.9"), owner,
                        schema_artifact_revision="1.2.17",
                    ),
                    INVALID,
                )

    def test_02_new_i_and_c_sets_are_valid_only_in_1217_mode(self):
        for owner in ("I", "C"):
            with self.subTest(owner=owner):
                self.assertEqual(
                    validate_owner_snapshot(snapshot(owner, "1.2.17"), owner),
                    INVALID,
                )
                self.assertEqual(
                    validate_owner_snapshot(
                        snapshot(owner, "1.2.17"), owner,
                        schema_artifact_revision="1.2.17",
                    ),
                    VALID,
                )

    def test_03_unknown_revision_fails_closed(self):
        self.assertEqual(
            validate_owner_snapshot(snapshot("I", "1.2.17"), "I",
                                     schema_artifact_revision="1.2.18"),
            INVALID,
        )

    def test_04_union_129_keeps_legacy_i_c_field_sets(self):
        snapshots = {owner: snapshot(owner, "1.2.9") for owner in ("I", "D", "C")}
        self.assertEqual(
            validate_union(
                composed_manifest(snapshots), [], [], snapshots,
                membership_proofs={}, verify_owner_snapshot=lambda *_: True,
            ),
            VALID,
        )

    def test_05_union_1217_accepts_exact_new_i_c_field_sets(self):
        snapshots = {owner: snapshot(owner, "1.2.17") for owner in ("I", "D", "C")}
        self.assertEqual(
            validate_union(
                composed_manifest(snapshots), [], [], snapshots,
                membership_proofs={}, verify_owner_snapshot=lambda *_: True,
                schema_artifact_revision="1.2.17",
            ),
            VALID,
        )

    def test_06_union_1217_rejects_legacy_i_or_c_alias_sets(self):
        for owner in ("I", "C"):
            with self.subTest(owner=owner):
                snapshots = {kind: snapshot(kind, "1.2.17") for kind in ("I", "D", "C")}
                snapshots[owner] = snapshot(owner, "1.2.9")
                self.assertEqual(
                    validate_union(
                        composed_manifest(snapshots), [], [], snapshots,
                        membership_proofs={}, verify_owner_snapshot=lambda *_: True,
                        schema_artifact_revision="1.2.17",
                    ),
                    INVALID,
                )

    def test_07_union_129_rejects_new_i_or_c_field_sets(self):
        for owner in ("I", "C"):
            with self.subTest(owner=owner):
                snapshots = {kind: snapshot(kind, "1.2.9") for kind in ("I", "D", "C")}
                snapshots[owner] = snapshot(owner, "1.2.17")
                self.assertEqual(
                    validate_union(
                        composed_manifest(snapshots), [], [], snapshots,
                        membership_proofs={}, verify_owner_snapshot=lambda *_: True,
                    ),
                    INVALID,
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
