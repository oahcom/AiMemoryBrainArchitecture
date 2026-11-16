import copy
import unittest

from restore_highwater_model import Blocked, RestoreModel, valid_proofs


class RestoreHighWaterTests(unittest.TestCase):
    def setUp(self):
        self.m = RestoreModel()
        self.coc, self.i, self.d, self.storage = valid_proofs(self.m)
        self.snapshot = {"wal_contiguous": True, "target_lsn": "0/7000000",
                         "timeline_verified": True, "old_primary_fenced": True,
                         "quarantined": True}

    def reconcile(self, **overrides):
        args = {"snapshot": self.snapshot, "coc_proof": self.coc,
                "i_proofs": self.i, "d_proofs": self.d, "storage_proof": self.storage}
        args.update(overrides)
        return self.m.reconcile(**args)

    def test_restore_starts_fenced_and_quarantined(self):
        self.assertEqual(self.m.state, "RESTORE_FENCED")
        self.assertIsNone(self.m.receipt)

    def test_complete_proof_set_issues_reconciled_but_fenced_receipt(self):
        receipt = self.reconcile()
        self.assertEqual(receipt.state, "RECONCILED_BUT_FENCED")
        self.assertEqual(self.m.state, "RECONCILED_BUT_FENCED")
        self.assertFalse(self.m.owner_service_gate)

    def test_missing_coc_proof_blocks(self):
        with self.assertRaises(Blocked):
            self.reconcile(coc_proof={})

    def test_coc_prefix_gap_or_missing_anchor_blocks(self):
        bad = dict(self.coc, contiguous=False)
        with self.assertRaises(Blocked):
            self.reconcile(coc_proof=bad)
        bad = dict(self.coc, external_anchor_verified=False)
        with self.assertRaises(Blocked):
            self.reconcile(coc_proof=bad)

    def test_stale_coc_epoch_or_index_blocks(self):
        bad = dict(self.coc, index=99)
        with self.assertRaises(Blocked):
            self.reconcile(coc_proof=bad)

    def test_missing_policy_domain_proof_blocks(self):
        with self.assertRaises(Blocked):
            self.reconcile(i_proofs={"pd-A": self.i["pd-A"]})

    def test_stale_permission_epoch_or_registry_epoch_blocks(self):
        bad = copy.deepcopy(self.i)
        bad["pd-A"]["permission_epoch"] = "pe-A-old"
        with self.assertRaises(Blocked):
            self.reconcile(i_proofs=bad)
        bad = copy.deepcopy(self.i)
        bad["pd-B"]["inventory_epoch"] = 8
        with self.assertRaises(Blocked):
            self.reconcile(i_proofs=bad)

    def test_missing_or_stale_d_operation_proof_blocks(self):
        with self.assertRaises(Blocked):
            self.reconcile(d_proofs={"forget-1": self.d["forget-1"]})
        bad = copy.deepcopy(self.d)
        bad["forget-1"]["producer_highwater"] = 11
        with self.assertRaises(Blocked):
            self.reconcile(d_proofs=bad)

    def test_open_d_barrier_blocks_restore(self):
        bad = copy.deepcopy(self.d)
        bad["forget-2"]["barrier_state"] = "OPEN"
        with self.assertRaises(Blocked):
            self.reconcile(d_proofs=bad)

    def test_incomplete_lineage_digest_blocks_restore(self):
        bad = copy.deepcopy(self.d)
        bad["forget-1"]["lineage_digest"] = "incomplete"
        with self.assertRaises(Blocked):
            self.reconcile(d_proofs=bad)

    def test_unknown_or_missing_storage_participant_blocks(self):
        bad = copy.deepcopy(self.storage)
        bad["participants"] = {}
        with self.assertRaises(Blocked):
            self.reconcile(storage_proof=bad)

    def test_same_gid_native_xid_or_terminal_outcome_mismatch_blocks(self):
        bad = copy.deepcopy(self.storage)
        bad["participants"]["participant-1"]["gid"] = "gid_other"
        with self.assertRaises(Blocked):
            self.reconcile(storage_proof=bad)
        bad = copy.deepcopy(self.storage)
        bad["participants"]["participant-1"]["native_xid"] = "native-xid:999"
        with self.assertRaises(Blocked):
            self.reconcile(storage_proof=bad)

    def test_unresolved_prepared_participant_blocks(self):
        bad = copy.deepcopy(self.storage)
        bad["participants"]["participant-1"]["state"] = "PREPARED"
        with self.assertRaises(Blocked):
            self.reconcile(storage_proof=bad)

    def test_pointer_only_or_receipt_only_visibility_blocks(self):
        bad = copy.deepcopy(self.storage)
        bad["visibility_pairs"]["artifact-1"]["receipt_tx"] = "tx-other"
        with self.assertRaises(Blocked):
            self.reconcile(storage_proof=bad)

    def test_missing_wal_or_timeline_proof_blocks(self):
        bad = dict(self.snapshot, wal_contiguous=False)
        with self.assertRaises(Blocked):
            self.reconcile(snapshot=bad)

    def test_old_primary_must_be_fenced_and_restore_quarantined(self):
        bad = dict(self.snapshot, old_primary_fenced=False)
        with self.assertRaises(Blocked):
            self.reconcile(snapshot=bad)
        bad = dict(self.snapshot, quarantined=False)
        with self.assertRaises(Blocked):
            self.reconcile(snapshot=bad)

    def test_proof_signature_key_or_audience_failure_blocks(self):
        bad = dict(self.coc, signature_valid=False)
        with self.assertRaises(Blocked):
            self.reconcile(coc_proof=bad)
        bad = dict(self.coc, key_version_active=False)
        with self.assertRaises(Blocked):
            self.reconcile(coc_proof=bad)
        bad = dict(self.coc, audience="public-read")
        with self.assertRaises(Blocked):
            self.reconcile(coc_proof=bad)

    def test_control_highwater_advance_during_restore_requires_retry(self):
        final_i = copy.deepcopy(self.m.current_i)
        final_i["pd-A"]["permission_epoch"] = "pe-A-8"
        with self.assertRaises(Blocked):
            self.reconcile(final_i=final_i)
        self.assertIsNone(self.m.receipt)
        self.assertEqual(self.m.state, "RESTORE_FENCED")

    def test_restore_receipt_alone_does_not_enable_service(self):
        self.reconcile()
        self.assertFalse(self.m.owner_service_gate)
        with self.assertRaises(Blocked):
            self.m.enable_owner_service(receipt_verified=True, owner_gate_verified=False)

    def test_service_release_requires_receipt_and_separate_owner_gate(self):
        self.reconcile()
        self.m.enable_owner_service(receipt_verified=True, owner_gate_verified=True)
        self.assertTrue(self.m.owner_service_gate)
        self.assertEqual(self.m.state, "OWNER_GATE_RELEASED")

    def test_restore_receipt_never_proves_global_forget_completion(self):
        self.reconcile()
        self.assertFalse(self.m.global_forget_complete())


if __name__ == "__main__":
    unittest.main()