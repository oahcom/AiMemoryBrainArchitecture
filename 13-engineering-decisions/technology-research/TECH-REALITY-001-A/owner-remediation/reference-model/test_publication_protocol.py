"""Bounded reference model for the proposed D/E/Storage/I publication protocol.

This is an executable specification aid, NOT production code, a database adapter,
a concurrency proof, or evidence of owner approval. It deliberately models the
proposed cross-owner contract as deterministic state transitions.
Run: python -m unittest discover -s <this-directory> -p 'test_*.py' -v
"""
from __future__ import annotations

import hashlib
import json
import unittest
from dataclasses import dataclass, field


class Rejected(Exception):
    pass


@dataclass
class Protocol:
    """Small in-memory model; each method represents one durable transition."""
    fence_generation: int = 0
    fence_installed: bool = False
    producer_work: dict = field(default_factory=dict)
    dependencies: dict = field(default_factory=dict)
    storage_participants: dict = field(default_factory=dict)
    publication_participants: dict = field(default_factory=dict)
    authorizations: dict = field(default_factory=dict)
    revoked: set = field(default_factory=set)
    consumed: set = field(default_factory=set)
    outcomes: dict = field(default_factory=dict)
    visibility: dict = field(default_factory=dict)
    receipts: dict = field(default_factory=dict)
    operation_bindings: dict = field(default_factory=dict)
    outbox: dict = field(default_factory=dict)
    private_unknown: set = field(default_factory=set)
    d_closed: dict = field(default_factory=dict)
    i_closed: dict = field(default_factory=dict)
    fence_pending: set = field(default_factory=set)

    @staticmethod
    def digest(items):
        encoded = json.dumps(sorted(items), separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    def register_producer(self, work_id, generation):
        if self.fence_installed or generation != self.fence_generation:
            raise Rejected("producer admission fenced or stale")
        prior = self.producer_work.get(work_id)
        value = {"generation": generation, "state": "REGISTERED"}
        if prior is not None and prior != value:
            raise Rejected("work identity reused with different binding")
        self.producer_work[work_id] = value

    def install_forget_fence(self):
        self.fence_generation += 1
        self.fence_installed = True
        # Publications admitted before the fence remain barrier-counted until
        # D observes the exact authoritative Storage terminal outcome.
        already_d_closed = {
            outcome[2]
            for outcome in self.d_closed.values()
            if isinstance(outcome, tuple) and len(outcome) >= 3
        }
        self.fence_pending = set(self.publication_participants) - already_d_closed
        return self.fence_generation

    def register_dependencies(self, work_id, dependencies):
        if work_id not in self.producer_work:
            raise Rejected("producer work not registered")
        if not dependencies or len(set(dependencies)) != len(dependencies):
            raise Rejected("dependency set must be non-empty and unique")
        candidate = frozenset(dependencies)
        prior = self.dependencies.get(work_id)
        if prior is not None and prior != candidate:
            raise Rejected("dependency set is immutable")
        self.dependencies[work_id] = candidate

    def create_hidden_storage_participant(self, storage_id, work_id):
        if work_id not in self.dependencies:
            raise Rejected("complete dependency set missing")
        binding = (work_id, self.digest(self.dependencies[work_id]))
        prior = self.storage_participants.get(storage_id)
        if prior is not None and prior != binding:
            raise Rejected("storage participant identity rebound")
        self.storage_participants[storage_id] = binding

    def admit_publication(self, publication_id, work_id, storage_id):
        work = self.producer_work.get(work_id)
        if work is None:
            raise Rejected("producer work not registered")
        if self.fence_installed or work["generation"] != self.fence_generation:
            raise Rejected("D fence installed or producer registration generation stale")
        if storage_id not in self.storage_participants:
            raise Rejected("exact hidden storage participant missing")
        if self.storage_participants[storage_id][0] != work_id:
            raise Rejected("storage participant belongs to another work")
        binding = (work_id, storage_id, self.storage_participants[storage_id][1])
        prior = self.publication_participants.get(publication_id)
        if prior is not None and prior != binding:
            raise Rejected("publication participant identity rebound")
        self.publication_participants[publication_id] = binding

    def authorize_commit(self, auth_id, publication_id, storage_id):
        if auth_id in self.revoked:
            raise Rejected("authorization revoked")
        if publication_id not in self.publication_participants:
            raise Rejected("publication participant missing")
        if self.publication_participants[publication_id][1] != storage_id:
            raise Rejected("authorization participant binding mismatch")
        binding = (publication_id, storage_id)
        prior = self.authorizations.get(auth_id)
        if prior is not None and prior != binding:
            raise Rejected("authorization identity rebound")
        self.authorizations[auth_id] = binding

    def revoke(self, auth_id):
        self.revoked.add(auth_id)

    def commit(self, operation_id, auth_id, publication_id, storage_id,
               d_proof, i_commit_won_proof, *, fail_before_commit=False):
        # Idempotent retry is valid only for the exact immutable operation tuple.
        # Reusing an operation ID with different participants/proofs is a conflict.
        binding = (auth_id, publication_id, storage_id, d_proof, i_commit_won_proof)
        if operation_id in self.receipts:
            if self.operation_bindings.get(operation_id) != binding:
                raise Rejected("operation identity reused with different immutable binding")
            return self.receipts[operation_id]
        if auth_id not in self.authorizations or auth_id in self.revoked:
            raise Rejected("authorization absent or revoked")
        if auth_id in self.consumed:
            raise Rejected("single-use authorization already consumed")
        if self.authorizations[auth_id] != (publication_id, storage_id):
            raise Rejected("authorization not bound to exact participants")
        if publication_id not in self.publication_participants:
            raise Rejected("D publication proof missing")
        if self.publication_participants[publication_id][1] != storage_id:
            raise Rejected("D proof does not bind exact Storage participant")
        if d_proof != ("D_ADMITTED", publication_id, storage_id):
            raise Rejected("invalid D publication proof")
        if i_commit_won_proof != ("I_COMMIT_WON", auth_id, publication_id, storage_id):
            raise Rejected("invalid pre-commit I COMMIT_WON proof")
        if fail_before_commit:
            raise RuntimeError("simulated crash before atomic transaction commit")

        # One indivisible modeled Storage transaction boundary.
        receipt = ("RECEIPT", operation_id, publication_id, storage_id)
        outcome = ("COMMITTED", operation_id, publication_id, storage_id)
        self.consumed.add(auth_id)
        self.visibility[publication_id] = "VISIBLE"
        self.outcomes[operation_id] = outcome
        self.receipts[operation_id] = receipt
        self.operation_bindings[operation_id] = binding
        self.outbox[operation_id] = ("PUBLISH", receipt)
        self.private_unknown.discard(operation_id)
        return receipt

    def mark_unknown(self, operation_id):
        if operation_id not in self.outcomes:
            self.private_unknown.add(operation_id)

    def close_d(self, operation_id, authoritative_outcome):
        if self.outcomes.get(operation_id) != authoritative_outcome:
            raise Rejected("D closeout requires exact authoritative Storage outcome")
        self.d_closed[operation_id] = authoritative_outcome
        if isinstance(authoritative_outcome, tuple) and len(authoritative_outcome) >= 3:
            self.fence_pending.discard(authoritative_outcome[2])

    def close_i(self, operation_id, authoritative_outcome):
        if self.outcomes.get(operation_id) != authoritative_outcome:
            raise Rejected("I closeout requires exact authoritative Storage outcome")
        self.i_closed[operation_id] = authoritative_outcome


class PublicationProtocolTests(unittest.TestCase):
    def prepared(self):
        p = Protocol()
        p.register_producer("work-1", 0)
        p.register_dependencies("work-1", ["root", "child-a", "child-b"])
        p.create_hidden_storage_participant("storage-1", "work-1")
        p.admit_publication("publication-1", "work-1", "storage-1")
        p.authorize_commit("auth-1", "publication-1", "storage-1")
        return p

    def commit_args(self):
        return dict(
            operation_id="op-1", auth_id="auth-1",
            publication_id="publication-1", storage_id="storage-1",
            d_proof=("D_ADMITTED", "publication-1", "storage-1"),
            i_commit_won_proof=("I_COMMIT_WON", "auth-1", "publication-1", "storage-1"),
        )

    def test_admission_then_fence_blocks_new_work(self):
        p = Protocol()
        p.register_producer("before", 0)
        p.install_forget_fence()
        with self.assertRaises(Rejected):
            p.register_producer("after", 1)

    def test_fence_then_admission_rejects(self):
        p = Protocol()
        p.install_forget_fence()
        with self.assertRaises(Rejected):
            p.register_producer("after", p.fence_generation)

    def test_fence_first_rejects_publication_after_work_and_storage_registration(self):
        p = Protocol()
        p.register_producer("work-1", 0)
        p.register_dependencies("work-1", ["root", "child-a"])
        p.create_hidden_storage_participant("storage-1", "work-1")
        p.install_forget_fence()
        with self.assertRaises(Rejected):
            p.admit_publication("publication-1", "work-1", "storage-1")

    def test_publication_already_closed_by_d_before_fence_is_not_pending(self):
        p = self.prepared()
        p.commit(**self.commit_args())
        outcome = p.outcomes["op-1"]
        p.close_d("op-1", outcome)
        p.install_forget_fence()
        self.assertNotIn("publication-1", p.fence_pending)

    def test_publication_first_remains_fence_barrier_until_d_closeout(self):
        p = self.prepared()
        p.install_forget_fence()
        self.assertIn("publication-1", p.fence_pending)
        receipt = p.commit(**self.commit_args())
        outcome = p.outcomes["op-1"]
        p.close_i("op-1", outcome)
        self.assertIn("publication-1", p.fence_pending)
        p.close_d("op-1", outcome)
        self.assertNotIn("publication-1", p.fence_pending)
        self.assertEqual(p.receipts["op-1"], receipt)

    def test_stale_generation_rejected(self):
        p = Protocol()
        p.fence_generation = 4
        with self.assertRaises(Rejected):
            p.register_producer("stale", 3)

    def test_dependency_set_is_complete_and_immutable(self):
        p = Protocol()
        p.register_producer("w", 0)
        p.register_dependencies("w", ["root", "transitive-a", "transitive-b"])
        with self.assertRaises(Rejected):
            p.register_dependencies("w", ["root", "transitive-a"])
        with self.assertRaises(Rejected):
            p.register_dependencies("w", ["root", "root"])

    def test_storage_participant_requires_dependencies(self):
        p = Protocol()
        p.register_producer("w", 0)
        with self.assertRaises(Rejected):
            p.create_hidden_storage_participant("s", "w")

    def test_publication_must_bind_exact_storage_participant(self):
        p = self.prepared()
        with self.assertRaises(Rejected):
            p.admit_publication("p2", "work-1", "storage-does-not-exist")
        with self.assertRaises(Rejected):
            p.admit_publication("p3", "other-work", "storage-1")

    def test_authorization_is_bound_to_exact_participants(self):
        p = self.prepared()
        with self.assertRaises(Rejected):
            p.authorize_commit("wrong-auth", "publication-1", "other-storage")

    def test_revocation_wins_before_commit(self):
        p = self.prepared()
        p.revoke("auth-1")
        with self.assertRaises(Rejected):
            p.commit(**self.commit_args())

    def test_commit_wins_before_later_revocation(self):
        p = self.prepared()
        receipt = p.commit(**self.commit_args())
        outcome = p.outcomes["op-1"]
        p.revoke("auth-1")
        self.assertEqual(p.receipts["op-1"], receipt)
        self.assertEqual(p.outcomes["op-1"], outcome)
        args = self.commit_args()
        args["operation_id"] = "op-2"
        with self.assertRaises(Rejected):
            p.commit(**args)

    def test_authorization_is_single_use_across_distinct_operations(self):
        p = self.prepared()
        args = self.commit_args()
        p.commit(**args)
        args["operation_id"] = "op-2"
        with self.assertRaises(Rejected):
            p.commit(**args)

    def test_final_storage_commit_requires_both_exact_proofs(self):
        p = self.prepared()
        args = self.commit_args()
        args["d_proof"] = ("D_ADMITTED", "publication-1", "wrong-storage")
        with self.assertRaises(Rejected):
            p.commit(**args)
        p = self.prepared()
        args = self.commit_args()
        args["i_commit_won_proof"] = ("I_TERMINAL", "auth-1")
        with self.assertRaises(Rejected):
            p.commit(**args)

    def test_crash_before_commit_leaves_no_partial_visibility_or_receipt(self):
        p = self.prepared()
        args = self.commit_args()
        args["fail_before_commit"] = True
        with self.assertRaises(RuntimeError):
            p.commit(**args)
        self.assertEqual(p.visibility, {})
        self.assertEqual(p.outcomes, {})
        self.assertEqual(p.receipts, {})
        self.assertEqual(p.outbox, {})
        self.assertEqual(p.consumed, set())

    def test_commit_atomically_records_visibility_outcome_receipt_and_outbox(self):
        p = self.prepared()
        receipt = p.commit(**self.commit_args())
        self.assertEqual(p.visibility["publication-1"], "VISIBLE")
        self.assertEqual(p.outcomes["op-1"][0], "COMMITTED")
        self.assertEqual(p.receipts["op-1"], receipt)
        self.assertEqual(p.outbox["op-1"], ("PUBLISH", receipt))

    def test_lost_ack_retry_is_idempotent(self):
        p = self.prepared()
        first = p.commit(**self.commit_args())
        second = p.commit(**self.commit_args())
        self.assertEqual(first, second)
        self.assertEqual(len(p.receipts), 1)
        self.assertEqual(len(p.outbox), 1)

    def test_operation_id_reuse_with_changed_participant_binding_conflicts(self):
        p = self.prepared()
        p.commit(**self.commit_args())
        args = self.commit_args()
        args["storage_id"] = "storage-substituted"
        args["d_proof"] = ("D_ADMITTED", "publication-1", "storage-substituted")
        args["i_commit_won_proof"] = ("I_COMMIT_WON", "auth-1", "publication-1", "storage-substituted")
        with self.assertRaises(Rejected):
            p.commit(**args)
        self.assertEqual(len(p.receipts), 1)
        self.assertEqual(len(p.outbox), 1)

    def test_unknown_stays_private_and_cannot_close_out(self):
        p = self.prepared()
        p.mark_unknown("op-unknown")
        self.assertIn("op-unknown", p.private_unknown)
        self.assertNotIn("publication-1", p.visibility)
        with self.assertRaises(Rejected):
            p.close_d("op-unknown", ("UNKNOWN",))
        with self.assertRaises(Rejected):
            p.close_i("op-unknown", ("UNKNOWN",))

    def test_d_and_i_close_only_on_same_authoritative_storage_outcome(self):
        p = self.prepared()
        p.commit(**self.commit_args())
        outcome = p.outcomes["op-1"]
        p.close_d("op-1", outcome)
        p.close_i("op-1", outcome)
        self.assertEqual(p.d_closed["op-1"], p.i_closed["op-1"])
        with self.assertRaises(Rejected):
            p.close_i("op-1", ("COMMITTED", "different", "publication-1", "storage-1"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
