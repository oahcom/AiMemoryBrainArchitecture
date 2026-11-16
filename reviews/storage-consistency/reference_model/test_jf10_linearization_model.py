"""Deterministic logical conformance tests for the JF-10 reference model.

These tests do not exercise a real DB, prepared transaction, I service, or HA stack.
Run: python -m unittest discover -s reviews/storage-consistency/reference_model -v
"""
import unittest

from jf10_linearization_model import (
    AuthorizationReceipt, Blocked, CoordinatorModel, Decision, DPublicationGate,
    ParticipantState, ProducerManifest, ProtocolError, SimulatedCrash,
    StorageParticipantModel, make_operation,
)


class JF10LinearizationModelTests(unittest.TestCase):
    def setUp(self):
        self.gate = DPublicationGate()
        self.storage = StorageParticipantModel(self.gate)
        self.coordinator = CoordinatorModel()
        self.op = make_operation()
        self.receipt = AuthorizationReceipt(
            "receipt-001", self.op.operation_id, self.op.request_digest,
            self.op.policy_domain,
        )

    def prepare_and_decide(self):
        self.op.receipt = self.receipt
        self.storage.prepare(self.op)
        self.coordinator.decide(
            self.op.operation_id, self.op.request_digest,
            frozenset({self.op.policy_domain}), self.receipt,
        )

    def test_prepared_operation_is_not_reader_visible(self):
        self.storage.prepare(self.op)
        self.assertFalse(self.storage.reader_can_see(self.op.operation_id))
        self.assertNotIn(self.op.operation_id, self.storage.publication_receipts)

    def test_commit_won_before_storage_commit_is_in_doubt_and_locked(self):
        self.prepare_and_decide()
        # Crash window: I decision is terminal; Storage local commit has not run.
        self.op.state = ParticipantState.IN_DOUBT
        self.assertFalse(self.storage.reader_can_see(self.op.operation_id))
        self.assertIn(self.op.operation_id, self.gate.prepared_operations)
        self.assertNotIn(self.receipt.receipt_id, self.storage.consumed_receipts)

    def test_recovery_uses_same_xid_and_publishes_atomically(self):
        self.prepare_and_decide()
        xid_before = self.op.xid
        self.op.state = ParticipantState.IN_DOUBT
        self.assertEqual(self.storage.recover(self.op.operation_id, self.coordinator),
                         ParticipantState.COMMITTED)
        self.assertEqual(self.op.xid, xid_before)
        self.assertTrue(self.storage.reader_can_see(self.op.operation_id))
        self.assertEqual(self.storage.publication_receipts[self.op.operation_id],
                         self.receipt.receipt_id)
        self.assertEqual(self.storage.owner_outcomes[self.op.operation_id], "COMMITTED")
        self.assertIn(self.receipt.receipt_id, self.storage.consumed_receipts)
        self.assertIn(self.op.operation_id, self.storage.outbox)
        self.assertNotIn(self.op.operation_id, self.gate.prepared_operations)

    def test_unknown_decision_fails_closed_and_retains_prepared_lock(self):
        self.storage.prepare(self.op)
        self.assertEqual(self.storage.recover(self.op.operation_id, self.coordinator),
                         ParticipantState.IN_DOUBT)
        self.assertIn(self.op.operation_id, self.gate.prepared_operations)
        self.assertFalse(self.storage.reader_can_see(self.op.operation_id))

    def test_crash_before_local_commit_keeps_operation_in_doubt_and_invisible(self):
        self.prepare_and_decide()
        with self.assertRaises(SimulatedCrash):
            self.storage.recover(self.op.operation_id, self.coordinator,
                                 fault_at="before_local_commit")
        self.assertEqual(self.op.state, ParticipantState.IN_DOUBT)
        self.assertNotIn(self.op.operation_id, self.storage.publication_records)
        self.assertFalse(self.storage.reader_can_see(self.op.operation_id))
        self.assertIn(self.op.operation_id, self.gate.prepared_operations)
        self.assertNotIn(self.receipt.receipt_id, self.storage.consumed_receipts)

    def test_crash_after_local_commit_recovers_atomic_record_projection(self):
        self.prepare_and_decide()
        with self.assertRaises(SimulatedCrash):
            self.storage.recover(self.op.operation_id, self.coordinator,
                                 fault_at="after_local_commit")
        # The commit point has happened; reader visibility follows the record.
        self.assertTrue(self.storage.reader_can_see(self.op.operation_id))
        self.assertIn(self.op.operation_id, self.storage.publication_records)
        # Simulate loss of volatile/readback projections after process restart.
        self.storage.visibility_pointers.clear()
        self.storage.publication_receipts.clear()
        self.storage.owner_outcomes.clear()
        self.storage.consumed_receipts.clear()
        self.storage.outbox.clear()
        self.assertEqual(self.storage.recover(self.op.operation_id, self.coordinator),
                         ParticipantState.COMMITTED)
        self.assertEqual(self.storage.visibility_pointers[self.op.operation_id],
                         self.op.manifest_digest)
        self.assertEqual(self.storage.publication_receipts[self.op.operation_id],
                         self.receipt.receipt_id)
        self.assertEqual(self.storage.owner_outcomes[self.op.operation_id], "COMMITTED")
        self.assertIn(self.receipt.receipt_id, self.storage.consumed_receipts)
        self.assertIn(self.op.operation_id, self.storage.outbox)
        self.assertNotIn(self.op.operation_id, self.gate.prepared_operations)

    def test_recovery_rejects_receipt_not_bound_by_coordinator(self):
        self.op.receipt = self.receipt
        self.storage.prepare(self.op)
        self.coordinator.decide(
            self.op.operation_id, self.op.request_digest,
            frozenset({self.op.policy_domain}), self.receipt,
        )
        self.op.receipt = AuthorizationReceipt(
            "forged-receipt", self.op.operation_id, self.op.request_digest,
            self.op.policy_domain,
        )
        with self.assertRaises(ProtocolError):
            self.storage.recover(self.op.operation_id, self.coordinator)
        self.assertFalse(self.storage.reader_can_see(self.op.operation_id))
        self.assertIn(self.op.operation_id, self.gate.prepared_operations)

    def test_committed_publication_readback_is_idempotent(self):
        self.prepare_and_decide()
        self.assertEqual(self.storage.recover(self.op.operation_id, self.coordinator),
                         ParticipantState.COMMITTED)
        record = self.storage.publication_records[self.op.operation_id]
        self.assertEqual(self.storage.recover(self.op.operation_id, self.coordinator),
                         ParticipantState.COMMITTED)
        self.assertEqual(self.storage.publication_records[self.op.operation_id], record)

    def test_abort_releases_lock_without_publication(self):
        self.op.receipt = self.receipt
        self.storage.prepare(self.op)
        self.coordinator.decide(
            self.op.operation_id, self.op.request_digest,
            frozenset({self.op.policy_domain}), self.receipt, Decision.ABORT,
        )
        self.assertEqual(self.storage.recover(self.op.operation_id, self.coordinator),
                         ParticipantState.ABORTED)
        self.assertFalse(self.storage.reader_can_see(self.op.operation_id))
        self.assertNotIn(self.op.operation_id, self.gate.prepared_operations)

    def test_fence_first_rejects_new_prepare(self):
        self.gate.begin_forget()
        stale = make_operation(fence_generation=1)
        with self.assertRaises(Blocked):
            self.storage.prepare(stale)

    def test_participant_first_blocks_fence_until_terminal(self):
        self.storage.prepare(self.op)
        with self.assertRaises(Blocked):
            self.gate.begin_forget()
        self.op.receipt = self.receipt
        self.coordinator.decide(
            self.op.operation_id, self.op.request_digest,
            frozenset({self.op.policy_domain}), self.receipt, Decision.ABORT,
        )
        self.storage.recover(self.op.operation_id, self.coordinator)
        self.assertEqual(self.gate.begin_forget(), 2)

    def test_multi_domain_atomicity_is_rejected(self):
        with self.assertRaises(Blocked):
            self.coordinator.decide(
                self.op.operation_id, self.op.request_digest,
                frozenset({"domain-001", "domain-002"}), self.receipt,
            )

    def test_stable_operation_identity_rejects_digest_rebinding(self):
        self.storage.prepare(self.op)
        changed = make_operation(manifest_digest="different-manifest")
        with self.assertRaises(ProtocolError):
            self.storage.prepare(changed)

    def test_e_retry_attempt_does_not_change_stable_publication_identity(self):
        producer = ProducerManifest()
        producer.freeze("work-001", "pub-001", "manifest-sha256")
        self.assertEqual(producer.assert_retry(
            "work-001", "pub-001", "manifest-sha256", "attempt-01"), "pub-001")
        self.assertEqual(producer.assert_retry(
            "work-001", "pub-001", "manifest-sha256", "attempt-99"), "pub-001")
        with self.assertRaises(ProtocolError):
            producer.assert_retry("work-001", "pub-001", "changed", "attempt-100")

    def test_terminal_decision_is_immutable(self):
        self.coordinator.decide(
            self.op.operation_id, self.op.request_digest,
            frozenset({self.op.policy_domain}), self.receipt, Decision.COMMIT,
        )
        with self.assertRaises(ProtocolError):
            self.coordinator.decide(
                self.op.operation_id, self.op.request_digest,
                frozenset({self.op.policy_domain}), self.receipt, Decision.ABORT,
            )


if __name__ == "__main__":
    unittest.main()
