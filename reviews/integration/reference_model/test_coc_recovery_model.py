"""Deterministic tests for the in-memory COC outage recovery model.

These are logical reference-model tests, not production consensus or owner-service tests.
"""
import unittest

from coc_recovery_model import Blocked, CoordinatorModel, OwnerRequest, ProtocolError


class COCRecoveryModelTests(unittest.TestCase):
    def setUp(self):
        self.coc = CoordinatorModel()
        self.i_req = OwnerRequest("I", "irev-01", "domain-A", 17, "i-digest")
        self.d_req = OwnerRequest("D", "dfence-01", "domain-A", 9, "d-digest",
                                  ("memory-A", "source-A"))

    def test_i_request_during_outage_persists_local_gate_and_blocks_submit(self):
        self.coc.set_outage()
        self.assertEqual(self.coc.record_owner_request(self.i_req), "PENDING_COC_CUTOFF")
        self.assertFalse(self.coc.provider_submit_allowed("domain-A"))
        self.assertEqual(self.coc.position, 0)

    def test_d_request_during_outage_blocks_affected_lineage_only(self):
        self.coc.set_outage()
        self.coc.record_owner_request(self.d_req)
        self.assertFalse(self.coc.provider_submit_allowed("domain-A", ("memory-A",)))
        self.assertTrue(self.coc.provider_submit_allowed("domain-A", ("unrelated-memory",)))
        self.assertTrue(self.coc.provider_submit_allowed("domain-B", ("memory-A",)))

    def test_new_intent_rejected_while_owner_local_gate_closed(self):
        self.coc.set_outage()
        self.coc.record_owner_request(self.d_req)
        self.coc.available = True
        with self.assertRaises(Blocked):
            self.coc.admit_intent("intent-new", "domain-A", "req", ("memory-A",))

    def test_simultaneous_i_and_d_requests_share_one_batch_without_local_time_order(self):
        self.coc.set_outage()
        self.coc.record_owner_request(self.i_req)
        self.coc.record_owner_request(self.d_req)
        self.coc.available = True
        batch = self.coc.recover_batch(owner_complete={"I": True, "D": True})
        self.assertEqual(batch.position, 1)
        self.assertEqual(batch.i_request_refs, ("irev-01",))
        self.assertEqual(batch.d_request_refs, ("dfence-01",))
        # The batch carries two sets at one position; no comparison of 17 vs 9 occurs.
        self.assertEqual(self.coc.log[-1]["kind"], "RECOVERY_CUTOFF_BATCH")

    def test_recovery_batch_enumerates_every_pre_batch_affected_participant(self):
        p1 = self.coc.admit_intent("intent-1", "domain-A", "req-1", ("memory-A",))
        p2 = self.coc.admit_intent("intent-2", "domain-A", "req-2", ("memory-B",))
        self.coc.set_outage()
        self.coc.record_owner_request(self.i_req)
        self.coc.record_owner_request(self.d_req)
        self.coc.available = True
        batch = self.coc.recover_batch(owner_complete={"I": True, "D": True})
        self.assertEqual(set(batch.pre_batch_participant_refs), {p1.intent_ref, p2.intent_ref})
        self.assertEqual(batch.pre_batch_participant_refs, ("intent-1", "intent-2"))

    def test_unresolved_pre_batch_participant_keeps_owner_gates_closed(self):
        p = self.coc.admit_intent("intent-1", "domain-A", "req-1", ("memory-A",))
        self.coc.set_outage()
        self.coc.record_owner_request(self.i_req)
        self.coc.record_owner_request(self.d_req)
        self.coc.available = True
        self.coc.recover_batch(owner_complete={"I": True, "D": True})
        with self.assertRaises(Blocked):
            self.coc.release_owner_gate("I", owner_high_water=17)
        with self.assertRaises(Blocked):
            self.coc.release_owner_gate("D", owner_high_water=9)
        self.assertIn("irev-01", self.coc.pending_gates["I"])
        self.assertIn("dfence-01", self.coc.pending_gates["D"])

    def test_owner_gates_release_only_after_reconciliation_and_high_water(self):
        p = self.coc.admit_intent("intent-1", "domain-A", "req-1", ("memory-A",))
        self.coc.set_outage()
        self.coc.record_owner_request(self.i_req)
        self.coc.record_owner_request(self.d_req)
        self.coc.available = True
        self.coc.recover_batch(owner_complete={"I": True, "D": True})
        self.coc.reconcile_participant(p.intent_ref, i_state="COMMIT_WON",
                                       d_state="CLEARANCE_CONFIRMED",
                                       c_outcome="ACCEPTED")
        with self.assertRaises(Blocked):
            self.coc.release_owner_gate("I", owner_high_water=16)
        self.coc.release_owner_gate("I", owner_high_water=17)
        self.coc.release_owner_gate("D", owner_high_water=9)
        self.assertFalse(self.coc.pending_gates["I"])
        self.assertFalse(self.coc.pending_gates["D"])

    def test_missing_committed_prefix_enters_restore_fenced(self):
        self.coc.set_outage()
        self.coc.record_owner_request(self.i_req)
        self.coc.available = True
        with self.assertRaises(Blocked):
            self.coc.recover_batch(prefix_valid=False, owner_complete={"I": True})
        self.assertTrue(self.coc.restore_fenced)
        self.assertFalse(self.coc.provider_submit_allowed("domain-A"))

    def test_missing_owner_request_completeness_enters_restore_fenced(self):
        self.coc.set_outage()
        self.coc.record_owner_request(self.d_req)
        self.coc.available = True
        with self.assertRaises(Blocked):
            self.coc.recover_batch(owner_complete={"D": False})
        self.assertTrue(self.coc.restore_fenced)

    def test_changed_owner_request_digest_is_conflict(self):
        self.coc.set_outage()
        self.coc.record_owner_request(self.i_req)
        changed = OwnerRequest("I", "irev-01", "domain-A", 17, "changed-digest")
        with self.assertRaises(ProtocolError):
            self.coc.record_owner_request(changed)


if __name__ == "__main__":
    unittest.main()
