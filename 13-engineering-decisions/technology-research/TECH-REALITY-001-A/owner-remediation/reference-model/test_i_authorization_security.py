"""Bounded I authorization/revocation sequencer reference model.

This is a deterministic state-machine model, NOT production cryptography,
a distributed sequencer, a key-management implementation, or a conformance
claim. It models the Phase 3.8 I contract's ordering and closeout semantics.
Run: python -m unittest discover -s <this-directory> -p 'test_*.py' -v
"""
from __future__ import annotations

import unittest
from dataclasses import dataclass, field


class Rejected(Exception):
    pass


@dataclass
class ISequencer:
    policy_epoch: int = 1
    high_water_epoch: int = 1
    position: int = 0
    key_status: dict = field(default_factory=lambda: {("issuer-A", 1): "ACTIVE"})
    revoked_subjects: set = field(default_factory=set)
    receipts_by_nonce: dict = field(default_factory=dict)
    pending: dict = field(default_factory=dict)
    pending_revocations: set = field(default_factory=set)
    terminal_proofs: dict = field(default_factory=dict)

    def consume(self, *, nonce, tuple_digest, subject, key_id, key_version,
                policy_epoch, operation_id, d_participant, storage_participant,
                now, accept_before):
        prior = self.receipts_by_nonce.get(nonce)
        if prior is not None:
            if prior["tuple_digest"] != tuple_digest or prior["operation_id"] != operation_id:
                raise Rejected("nonce replayed with changed immutable publication tuple")
            return prior  # Lost response retry: return the original sequencer result.

        if policy_epoch < self.high_water_epoch or policy_epoch != self.policy_epoch:
            raise Rejected("PolicyDomain epoch stale or rolled back")
        if self.key_status.get((key_id, key_version)) != "ACTIVE":
            raise Rejected("issuer key is not currently active")
        if now > accept_before:
            raise Rejected("accept-before expired before first consumption")

        self.position += 1
        result = "REVOCATION_WON" if subject in self.revoked_subjects else "COMMIT_WON"
        receipt = {
            "nonce": nonce, "tuple_digest": tuple_digest, "subject": subject,
            "operation_id": operation_id, "d_participant": d_participant,
            "storage_participant": storage_participant, "policy_epoch": policy_epoch,
            "sequencer_position": self.position, "result": result,
        }
        self.receipts_by_nonce[nonce] = receipt
        if result == "COMMIT_WON":
            self.pending[operation_id] = receipt
        return receipt

    def revoke(self, subject):
        if any(item["subject"] == subject for item in self.pending.values()):
            self.pending_revocations.add(subject)
            return "PENDING"
        self.revoked_subjects.add(subject)
        self.policy_epoch += 1
        self.high_water_epoch = max(self.high_water_epoch, self.policy_epoch)
        return "APPLIED"

    def closeout(self, *, operation_id, tuple_digest, d_participant,
                 storage_participant, storage_outcome):
        receipt = self.pending.get(operation_id)
        if receipt is None:
            raise Rejected("no unresolved COMMIT_WON participant")
        exact = (
            receipt["tuple_digest"] == tuple_digest
            and receipt["d_participant"] == d_participant
            and receipt["storage_participant"] == storage_participant
        )
        if not exact:
            raise Rejected("Storage outcome does not bind exact I participant tuple")
        if storage_outcome == "UNKNOWN":
            return None
        if storage_outcome not in ("COMMITTED_VISIBLE", "NO_PUBLICATION"):
            raise Rejected("unsupported or contradictory Storage outcome")

        proof = {
            "operation_id": operation_id, "tuple_digest": tuple_digest,
            "d_participant": d_participant, "storage_participant": storage_participant,
            "storage_outcome": storage_outcome,
            "sequencer_position": receipt["sequencer_position"],
        }
        self.terminal_proofs[operation_id] = proof
        del self.pending[operation_id]
        subject = receipt["subject"]
        if subject in self.pending_revocations:
            self.pending_revocations.remove(subject)
            self.revoked_subjects.add(subject)
            self.policy_epoch += 1
            self.high_water_epoch = max(self.high_water_epoch, self.policy_epoch)
        return proof

    def restore_reconcile(self, storage_outcomes):
        """Only exact authoritative outcomes can close; absent/UNKNOWN stay pending."""
        results = {}
        for operation_id, receipt in list(self.pending.items()):
            observed = storage_outcomes.get(operation_id)
            if observed is None or observed == "UNKNOWN":
                results[operation_id] = "IN_DOUBT"
                continue
            results[operation_id] = self.closeout(
                operation_id=operation_id,
                tuple_digest=receipt["tuple_digest"],
                d_participant=receipt["d_participant"],
                storage_participant=receipt["storage_participant"],
                storage_outcome=observed,
            )["storage_outcome"]
        return results

    def rollback_epoch(self, restored_epoch):
        if restored_epoch < self.high_water_epoch:
            raise Rejected("PolicyDomain anti-rollback high-water violation")
        self.policy_epoch = restored_epoch
        self.high_water_epoch = max(self.high_water_epoch, restored_epoch)


class IAuthorizationSecurityTests(unittest.TestCase):
    def request(self, **overrides):
        values = dict(
            nonce="nonce-1", tuple_digest="tuple-digest-1", subject="alice",
            key_id="issuer-A", key_version=1, policy_epoch=1,
            operation_id="op-1", d_participant="D-participant-1",
            storage_participant="Storage-participant-1", now=100,
            accept_before=110,
        )
        values.update(overrides)
        return values

    def consumed(self):
        i = ISequencer()
        receipt = i.consume(**self.request())
        self.assertEqual(receipt["result"], "COMMIT_WON")
        return i, receipt

    def test_revocation_first_blocks_consumption(self):
        i = ISequencer()
        self.assertEqual(i.revoke("alice"), "APPLIED")
        receipt = i.consume(**self.request(policy_epoch=i.policy_epoch))
        self.assertEqual(receipt["result"], "REVOCATION_WON")
        self.assertNotIn("op-1", i.pending)

    def test_commit_won_first_holds_later_revocation(self):
        i, _ = self.consumed()
        self.assertEqual(i.revoke("alice"), "PENDING")
        self.assertIn("alice", i.pending_revocations)
        self.assertNotIn("alice", i.revoked_subjects)

    def test_duplicate_nonce_same_request_returns_original_receipt(self):
        i, receipt = self.consumed()
        before = i.position
        replay = i.consume(**self.request())
        self.assertEqual(replay, receipt)
        self.assertEqual(i.position, before)

    def test_duplicate_nonce_changed_tuple_is_rejected(self):
        i, _ = self.consumed()
        with self.assertRaises(Rejected):
            i.consume(**self.request(tuple_digest="different-tuple"))

    def test_artifact_scope_attempt_or_storage_change_changes_tuple(self):
        i, _ = self.consumed()
        for changed in ("artifact-version", "scope", "attempt", "storage-participant"):
            with self.subTest(changed=changed):
                with self.assertRaises(Rejected):
                    i.consume(**self.request(tuple_digest="changed-" + changed))

    def test_revoked_issuer_key_rejected(self):
        i = ISequencer()
        i.key_status[("issuer-A", 1)] = "REVOKED"
        with self.assertRaises(Rejected):
            i.consume(**self.request())

    def test_policy_epoch_rollback_rejected(self):
        i = ISequencer()
        i.policy_epoch = 5
        i.high_water_epoch = 5
        with self.assertRaises(Rejected):
            i.rollback_epoch(4)
        with self.assertRaises(Rejected):
            i.consume(**self.request(policy_epoch=4))

    def test_lost_response_after_commit_won_returns_same_receipt(self):
        i, first = self.consumed()
        retry = i.consume(**self.request())
        self.assertEqual(retry, first)
        self.assertEqual(i.position, 1)
        self.assertEqual(len(i.pending), 1)

    def test_committed_visible_closes_exact_participant(self):
        i, receipt = self.consumed()
        proof = i.closeout(
            operation_id="op-1", tuple_digest="tuple-digest-1",
            d_participant="D-participant-1",
            storage_participant="Storage-participant-1",
            storage_outcome="COMMITTED_VISIBLE",
        )
        self.assertEqual(proof["storage_outcome"], "COMMITTED_VISIBLE")
        self.assertNotIn("op-1", i.pending)
        self.assertEqual(i.terminal_proofs["op-1"]["sequencer_position"],
                         receipt["sequencer_position"])

    def test_no_publication_closes_exact_participant(self):
        i, _ = self.consumed()
        proof = i.closeout(
            operation_id="op-1", tuple_digest="tuple-digest-1",
            d_participant="D-participant-1",
            storage_participant="Storage-participant-1",
            storage_outcome="NO_PUBLICATION",
        )
        self.assertEqual(proof["storage_outcome"], "NO_PUBLICATION")

    def test_unknown_keeps_gate_and_pending_revocation_held(self):
        i, _ = self.consumed()
        i.revoke("alice")
        proof = i.closeout(
            operation_id="op-1", tuple_digest="tuple-digest-1",
            d_participant="D-participant-1",
            storage_participant="Storage-participant-1",
            storage_outcome="UNKNOWN",
        )
        self.assertIsNone(proof)
        self.assertIn("op-1", i.pending)
        self.assertIn("alice", i.pending_revocations)
        self.assertNotIn("op-1", i.terminal_proofs)

    def test_missing_or_contradictory_restore_outcome_does_not_close(self):
        i, _ = self.consumed()
        self.assertEqual(i.restore_reconcile({}), {"op-1": "IN_DOUBT"})
        with self.assertRaises(Rejected):
            i.closeout(
                operation_id="op-1", tuple_digest="wrong-tuple",
                d_participant="D-participant-1",
                storage_participant="Storage-participant-1",
                storage_outcome="COMMITTED_VISIBLE",
            )
        self.assertIn("op-1", i.pending)

    def test_restore_with_exact_storage_outcome_closes(self):
        i, _ = self.consumed()
        result = i.restore_reconcile({"op-1": "COMMITTED_VISIBLE"})
        self.assertEqual(result, {"op-1": "COMMITTED_VISIBLE"})
        self.assertNotIn("op-1", i.pending)

    def test_revocation_released_only_after_storage_terminal_outcome(self):
        i, _ = self.consumed()
        self.assertEqual(i.revoke("alice"), "PENDING")
        i.closeout(
            operation_id="op-1", tuple_digest="tuple-digest-1",
            d_participant="D-participant-1",
            storage_participant="Storage-participant-1",
            storage_outcome="NO_PUBLICATION",
        )
        self.assertIn("alice", i.revoked_subjects)
        self.assertNotIn("alice", i.pending_revocations)

    def test_expired_token_blocks_first_consumption(self):
        i = ISequencer()
        with self.assertRaises(Rejected):
            i.consume(**self.request(now=111, accept_before=110))

    def test_expiry_does_not_erase_already_consumed_commit_won(self):
        i, receipt = self.consumed()
        retry = i.consume(**self.request(now=999, accept_before=110))
        self.assertEqual(retry, receipt)
        self.assertIn("op-1", i.pending)


if __name__ == "__main__":
    unittest.main(verbosity=2)
