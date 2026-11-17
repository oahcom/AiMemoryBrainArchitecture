"""Executable TEST-PROFILE vectors for Recovery Cutoff 1.0.5 Batch/Manifest pair."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "runtime_reference"))

from recovery_cutoff_semantics import (
    VALID, INVALID, UNKNOWN, FENCED, RECONCILIATION_ALLOWED,
    digest, participant_content_digest, recovery_batch_digest,
    participant_manifest_record_digest, validate_batch_manifest_pair,
    validate_owner_gate_release, validate_recovery_epoch_completed,
    recovery_state,
)


def fixture_pair(entries=None):
    entries = [] if entries is None else deepcopy(entries)
    prefix_term, prefix_index, prefix_root = 4, 88, "a" * 64
    manifest = {
        "schema_id": "bmcp.recovery-cutoff",
        "schema_version": "1.0.5",
        "message_type": "COC_PARTICIPANT_MANIFEST",
        "message_id": "manifest/epoch-1/round-1",
        "recovery_epoch_ref": "epoch/1",
        "prefix_term": prefix_term,
        "prefix_index": prefix_index,
        "prefix_root": prefix_root,
        "enumeration_status": "COMPLETE_EMPTY" if not entries else "COMPLETE_NON_EMPTY",
        "participant_count": len(entries),
        "participant_set_root": digest("PARTICIPANT-SET", entries),
        "previous_prefix_digest": "0" * 64,
        "participant_entries": entries,
        "recovery_batch_ref": "batch/epoch-1/round-1",
        "recovery_batch_digest": "0" * 64,
        "participant_manifest_content_digest": "0" * 64,
        "quorum_commit_proof_ref": "proof/manifest/1",
        "quorum_commit_proof_valid": True,
        "envelope": {},
    }
    manifest["participant_manifest_content_digest"] = participant_content_digest(manifest)
    batch = {
        "schema_id": "bmcp.recovery-cutoff",
        "schema_version": "1.0.5",
        "message_type": "RECOVERY_CUTOFF_BATCH",
        "message_id": "batch/epoch-1/round-1",
        "recovery_epoch_ref": "epoch/1",
        "recovery_round_ref": "round/1",
        "prefix_term": prefix_term,
        "prefix_index": prefix_index,
        "prefix_root": prefix_root,
        "participant_manifest_ref": manifest["message_id"],
        "participant_manifest_content_digest": manifest["participant_manifest_content_digest"],
        "owner_snapshot_refs": {"I": "i/snap/1", "D": "d/snap/1", "C": "c/snap/1"},
        "owner_snapshot_digests": {"I": "1" * 64, "D": "2" * 64, "C": "3" * 64},
        "scope_binding_digest": "4" * 64,
        "reconciliation_attempt_generation": "1",
        "previous_batch_digest": "0" * 64,
        "quorum_commit_proof_ref": "proof/batch/1",
        "quorum_commit_proof_valid": True,
        "envelope": {},
    }
    batch["batch_digest"] = recovery_batch_digest(batch)
    manifest["recovery_batch_digest"] = batch["batch_digest"]
    manifest["envelope"]["payload_digest"] = participant_manifest_record_digest(manifest)
    return batch, manifest


def release(owner, batch, manifest):
    return {
        "owner_kind": owner,
        "release_kind": "OUTAGE_ADMISSION_RELEASE_ONLY",
        "recovery_batch_ref": batch["message_id"],
        "recovery_batch_digest": batch["batch_digest"],
        "participant_manifest_content_digest": manifest["participant_manifest_content_digest"],
        "participant_manifest_record_digest": participant_manifest_record_digest(manifest),
        "final_currentness_cas_valid": True,
    }


class TwoPhaseRecoveryVectors(unittest.TestCase):
    def setUp(self):
        self.batch, self.manifest = fixture_pair()

    def validate(self, batch=None, manifest=None, batch_pos=(8, 100),
                 manifest_pos=(8, 101), **kwargs):
        return validate_batch_manifest_pair(
            self.batch if batch is None else batch,
            self.manifest if manifest is None else manifest,
            batch_pos, manifest_pos, **kwargs
        )

    def test_TPH_01_valid_empty_manifest_pair(self):
        self.assertEqual(self.validate(), VALID)

    def test_TPH_02_content_digest_is_stable_when_batch_backlink_is_added(self):
        before = participant_content_digest(self.manifest)
        changed = deepcopy(self.manifest)
        changed["recovery_batch_ref"] = "another/batch"
        changed["recovery_batch_digest"] = "f" * 64
        self.assertEqual(before, participant_content_digest(changed))

    def test_TPH_03_record_digest_changes_when_batch_backlink_changes(self):
        before = participant_manifest_record_digest(self.manifest)
        changed = deepcopy(self.manifest)
        changed["recovery_batch_ref"] = "another/batch"
        self.assertNotEqual(before, participant_manifest_record_digest(changed))

    def test_TPH_04_batch_must_reference_manifest_content_not_record_digest(self):
        changed = deepcopy(self.batch)
        changed["participant_manifest_content_digest"] = participant_manifest_record_digest(self.manifest)
        changed["batch_digest"] = recovery_batch_digest(changed)
        self.assertEqual(self.validate(batch=changed), INVALID)

    def test_TPH_05_manifest_must_reference_exact_batch_id(self):
        changed = deepcopy(self.manifest)
        changed["recovery_batch_ref"] = "batch/wrong"
        changed["envelope"]["payload_digest"] = participant_manifest_record_digest(changed)
        self.assertEqual(self.validate(manifest=changed), INVALID)

    def test_TPH_06_manifest_must_reference_exact_batch_digest(self):
        changed = deepcopy(self.manifest)
        changed["recovery_batch_digest"] = "f" * 64
        changed["envelope"]["payload_digest"] = participant_manifest_record_digest(changed)
        self.assertEqual(self.validate(manifest=changed), INVALID)

    def test_TPH_07_batch_record_must_precede_manifest_record(self):
        self.assertEqual(self.validate(batch_pos=(8, 102), manifest_pos=(8, 101)), INVALID)

    def test_TPH_08_manifest_and_batch_prefix_must_match(self):
        changed = deepcopy(self.manifest)
        changed["prefix_index"] += 1
        self.assertEqual(self.validate(manifest=changed), INVALID)

    def test_TPH_09_count_must_equal_entry_array_length(self):
        changed = deepcopy(self.manifest)
        changed["participant_count"] = 1
        self.assertEqual(self.validate(manifest=changed), INVALID)

    def test_TPH_10_content_digest_must_recompute(self):
        changed = deepcopy(self.manifest)
        changed["participant_manifest_content_digest"] = "f" * 64
        self.assertEqual(self.validate(manifest=changed), INVALID)

    def test_TPH_11_batch_digest_must_recompute(self):
        changed = deepcopy(self.batch)
        changed["scope_binding_digest"] = "f" * 64
        self.assertEqual(self.validate(batch=changed), INVALID)

    def test_TPH_12_manifest_record_digest_must_match_envelope(self):
        changed = deepcopy(self.manifest)
        changed["envelope"]["payload_digest"] = "f" * 64
        self.assertEqual(self.validate(manifest=changed), INVALID)

    def test_TPH_13_incomplete_prefix_enumeration_is_unknown(self):
        self.assertEqual(self.validate(prefix_enumeration_complete=False), UNKNOWN)

    def test_TPH_14_non_linearizable_pair_readback_is_unknown(self):
        self.assertEqual(self.validate(linearizable_readback=False), UNKNOWN)

    def test_TPH_15_missing_batch_quorum_proof_is_unknown(self):
        changed = deepcopy(self.batch)
        changed["quorum_commit_proof_valid"] = False
        self.assertEqual(self.validate(batch=changed), UNKNOWN)

    def test_TPH_16_missing_manifest_quorum_proof_is_unknown(self):
        changed = deepcopy(self.manifest)
        changed["quorum_commit_proof_valid"] = False
        self.assertEqual(self.validate(manifest=changed), UNKNOWN)

    def test_TPH_17_wrong_schema_version_is_invalid(self):
        changed = deepcopy(self.manifest)
        changed["schema_version"] = "1.0.4"
        self.assertEqual(self.validate(manifest=changed), INVALID)

    def test_TPH_18_duplicate_participant_identity_is_invalid(self):
        entry = {
            "participant_intent_ref": "participant/1",
            "owner_kind": "C",
            "operation_identity_ref": "operation/1",
            "participant_digest": "a" * 64,
            "prefix_term": 4,
            "prefix_index": 20,
            "entry_digest": "b" * 64,
            "owner_admission_ref": "c/admission/1",
        }
        batch, manifest = fixture_pair([entry, deepcopy(entry)])
        self.assertEqual(self.validate(batch=batch, manifest=manifest), INVALID)

    def test_TPH_19_release_requires_both_manifest_digests(self):
        r = release("I", self.batch, self.manifest)
        del r["participant_manifest_record_digest"]
        self.assertEqual(validate_owner_gate_release(r, self.batch, self.manifest), INVALID)

    def test_TPH_20_release_requires_currentness_cas(self):
        r = release("D", self.batch, self.manifest)
        r["final_currentness_cas_valid"] = False
        self.assertEqual(validate_owner_gate_release(r, self.batch, self.manifest), UNKNOWN)

    def test_TPH_21_epoch_completion_requires_all_three_owner_releases(self):
        releases = {o: release(o, self.batch, self.manifest) for o in ("I", "D")}
        completed = {
            "final_batch_ref": self.batch["message_id"],
            "final_batch_digest": self.batch["batch_digest"],
            "participant_manifest_content_digest": self.manifest["participant_manifest_content_digest"],
            "participant_manifest_record_digest": participant_manifest_record_digest(self.manifest),
            "required_owner_release_refs": ["i/release", "d/release"],
            "all_rounds_root": "a" * 64,
            "quorum_commit_proof_valid": True,
        }
        self.assertEqual(validate_recovery_epoch_completed(completed, self.batch, self.manifest, releases), INVALID)

    def test_TPH_22_epoch_completion_binds_both_manifest_digests(self):
        releases = {o: release(o, self.batch, self.manifest) for o in ("I", "D", "C")}
        completed = {
            "final_batch_ref": self.batch["message_id"],
            "final_batch_digest": self.batch["batch_digest"],
            "participant_manifest_content_digest": self.manifest["participant_manifest_content_digest"],
            "participant_manifest_record_digest": "f" * 64,
            "required_owner_release_refs": ["i/release", "d/release", "c/release"],
            "all_rounds_root": "a" * 64,
            "quorum_commit_proof_valid": True,
        }
        self.assertEqual(validate_recovery_epoch_completed(completed, self.batch, self.manifest, releases), INVALID)

    def test_TPH_23_batch_without_manifest_keeps_system_fenced(self):
        self.assertEqual(recovery_state(True, False, True, False), FENCED)

    def test_TPH_24_missing_staged_manifest_after_batch_keeps_restore_fenced(self):
        self.assertEqual(recovery_state(True, True, False, False), FENCED)

    def test_TPH_25_pair_must_be_read_back_before_reconciliation(self):
        self.assertEqual(recovery_state(True, True, True, False), FENCED)

    def test_TPH_26_reconciliation_allowed_only_after_verified_pair(self):
        self.assertEqual(recovery_state(True, True, True, True), RECONCILIATION_ALLOWED)


if __name__ == "__main__":
    unittest.main(verbosity=2)
