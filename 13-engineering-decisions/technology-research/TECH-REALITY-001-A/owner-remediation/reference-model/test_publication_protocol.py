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
from dataclasses import dataclass, field, replace


class Rejected(Exception):
    pass


@dataclass(frozen=True)
class StorageNoPublicationProof:
    """Test-seam representation of the Storage positive NO_PUBLICATION proof."""

    operation_id: str
    operation_binding: tuple
    publication_id: str
    storage_id: str
    visibility_pointer_absent: bool
    outbox_absent: bool
    unresolved_participants_absent: bool
    writers_fenced: bool
    stage_publishers_fenced: bool
    retries_fenced: bool
    delayed_publishers_fenced: bool
    outbox_handlers_fenced: bool
    conflicting_commit_absent: bool
    restore_preserves_terminal: bool

    def complete(self):
        return all((
            self.visibility_pointer_absent is True,
            self.outbox_absent is True,
            self.unresolved_participants_absent is True,
            self.writers_fenced is True,
            self.stage_publishers_fenced is True,
            self.retries_fenced is True,
            self.delayed_publishers_fenced is True,
            self.outbox_handlers_fenced is True,
            self.conflicting_commit_absent is True,
            self.restore_preserves_terminal is True,
        ))


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
    i_pending: dict = field(default_factory=dict)
    revocation_pending: set = field(default_factory=set)
    outcomes: dict = field(default_factory=dict)
    visibility: dict = field(default_factory=dict)
    receipts: dict = field(default_factory=dict)
    operation_bindings: dict = field(default_factory=dict)
    storage_no_publication_proofs: dict = field(default_factory=dict)
    outbox: dict = field(default_factory=dict)
    private_unknown: set = field(default_factory=set)
    d_closed: dict = field(default_factory=dict)
    i_closed: dict = field(default_factory=dict)
    publication_commit_winners: dict = field(default_factory=dict)
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

    def admit_publication(self, publication_id, work_id, storage_id,
                          request_digest, owner_boundary, final_visibility_gate_id):
        work = self.producer_work.get(work_id)
        if work is None:
            raise Rejected("producer work not registered")
        if self.fence_installed or work["generation"] != self.fence_generation:
            raise Rejected("D fence installed or producer registration generation stale")
        if storage_id not in self.storage_participants:
            raise Rejected("exact hidden storage participant missing")
        if self.storage_participants[storage_id][0] != work_id:
            raise Rejected("storage participant belongs to another work")
        if not request_digest or not owner_boundary or not final_visibility_gate_id:
            raise Rejected("canonical request digest, owner boundary and final visibility gate identity are required")
        binding = (
            work_id, storage_id, self.storage_participants[storage_id][1],
            request_digest, owner_boundary, final_visibility_gate_id,
        )
        prior = self.publication_participants.get(publication_id)
        if prior is not None and prior != binding:
            raise Rejected("publication participant identity rebound")
        self.publication_participants[publication_id] = binding

    def authorize_commit(self, auth_id, publication_id, storage_id,
                         request_digest, owner_boundary, final_visibility_gate_id):
        if auth_id in self.revoked:
            raise Rejected("authorization revoked")
        if publication_id not in self.publication_participants:
            raise Rejected("publication participant missing")
        if self.publication_participants[publication_id][1] != storage_id:
            raise Rejected("authorization participant binding mismatch")
        if self.publication_participants[publication_id][3:] != (request_digest, owner_boundary, final_visibility_gate_id):
            raise Rejected("authorization request digest or owner boundary mismatch")
        binding = (publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id)
        prior = self.authorizations.get(auth_id)
        if prior is not None:
            if prior != binding:
                raise Rejected("authorization identity rebound")
            return
        if publication_id in self.publication_commit_winners:
            raise Rejected("publication participant already has a COMMIT_WON operation")
        self.authorizations[auth_id] = binding

    def revoke(self, auth_id):
        self.revoked.add(auth_id)
        if any(binding[0] == auth_id for binding in self.i_pending.values()):
            self.revocation_pending.add(auth_id)

    def consume_i_commit_won(self, operation_id, auth_id, publication_id,
                             storage_id, request_digest, owner_boundary, final_visibility_gate_id, d_proof):
        i_proof = (
            "I_COMMIT_WON", auth_id, publication_id, storage_id,
            request_digest, owner_boundary, final_visibility_gate_id,
        )
        binding = (
            auth_id, publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id,
            d_proof, i_proof,
        )
        # A replay after COMMIT_WON returns the same proof even if revocation
        # arrived later; the sequencer decision already won.
        if operation_id in self.i_pending:
            if self.i_pending[operation_id] != binding:
                raise Rejected("I participant identity rebound")
            return i_proof
        if operation_id in self.i_closed:
            if self.operation_bindings.get(operation_id) != binding:
                raise Rejected("closed I participant identity rebound")
            return i_proof
        if operation_id in self.private_unknown or operation_id in self.outcomes:
            raise Rejected("operation is already UNKNOWN or terminal")
        prior_winner = self.publication_commit_winners.get(publication_id)
        if prior_winner is not None and prior_winner != operation_id:
            raise Rejected("publication participant already has a COMMIT_WON operation")
        if auth_id not in self.authorizations or auth_id in self.revoked:
            raise Rejected("authorization absent or revocation won before I consumption")
        if self.authorizations[auth_id] != (
            publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id
        ):
            raise Rejected("authorization not bound to exact participants, digest and owner boundary")
        if publication_id not in self.publication_participants:
            raise Rejected("D publication proof missing")
        publication_binding = self.publication_participants[publication_id]
        if publication_binding[1] != storage_id or publication_binding[3:] != (
            request_digest, owner_boundary, final_visibility_gate_id
        ):
            raise Rejected("D proof does not bind exact Storage participant, digest and owner boundary")
        if d_proof != (
            "D_ADMITTED", publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id
        ):
            raise Rejected("invalid D publication proof")
        prior = self.operation_bindings.get(operation_id)
        if prior is not None and prior != binding:
            raise Rejected("operation identity rebound before Storage commit")
        if auth_id in self.consumed:
            raise Rejected("single-use authorization already consumed")
        self.consumed.add(auth_id)
        self.publication_commit_winners[publication_id] = operation_id
        self.i_pending[operation_id] = binding
        self.operation_bindings[operation_id] = binding
        return i_proof

    def commit(self, operation_id, auth_id, publication_id, storage_id,
               request_digest, owner_boundary, final_visibility_gate_id, d_proof, i_commit_won_proof,
               *, fail_before_commit=False):
        binding = (
            auth_id, publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id,
            d_proof, i_commit_won_proof,
        )
        if operation_id in self.private_unknown:
            prior = self.operation_bindings.get(operation_id)
            if prior is not None and prior != binding:
                raise Rejected("UNKNOWN operation binding mismatch; reconciliation required")
            raise Rejected("operation outcome UNKNOWN; authoritative reconciliation required")
        if operation_id in self.receipts:
            if self.operation_bindings.get(operation_id) != binding:
                raise Rejected("operation identity reused with different immutable binding")
            return self.receipts[operation_id]
        if operation_id in self.outcomes:
            raise Rejected("operation already terminal as NO_PUBLICATION; use a new operation ID")
        # Storage consumes no I authorization: it validates the exact prior
        # COMMIT_WON decision made by the independent I sequencer.
        if self.i_pending.get(operation_id) != binding:
            raise Rejected("exact I COMMIT_WON participant has not been consumed")
        if auth_id not in self.authorizations or auth_id not in self.consumed:
            raise Rejected("authorization or I consumption missing")
        if self.authorizations[auth_id] != (
            publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id
        ):
            raise Rejected("authorization not bound to exact participants, digest and owner boundary")
        if publication_id not in self.publication_participants:
            raise Rejected("D publication proof missing")
        if self.publication_participants[publication_id][1] != storage_id:
            raise Rejected("D proof does not bind exact Storage participant")
        if self.publication_participants[publication_id][3:] != (request_digest, owner_boundary, final_visibility_gate_id):
            raise Rejected("D participant digest or owner boundary mismatch")
        if d_proof != (
            "D_ADMITTED", publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id
        ):
            raise Rejected("invalid D publication proof")
        if i_commit_won_proof != (
            "I_COMMIT_WON", auth_id, publication_id, storage_id,
            request_digest, owner_boundary, final_visibility_gate_id,
        ):
            raise Rejected("invalid pre-commit I COMMIT_WON proof")
        if fail_before_commit:
            raise RuntimeError("simulated crash before Storage transaction commit")

        receipt = ("RECEIPT", operation_id, publication_id, storage_id)
        outcome = ("COMMITTED", operation_id, publication_id, storage_id)
        self.visibility[publication_id] = "VISIBLE"
        self.outcomes[operation_id] = outcome
        self.receipts[operation_id] = receipt
        self.outbox[operation_id] = ("PUBLISH", receipt)
        return receipt

    def _validate_unknown_binding(self, binding):
        if not isinstance(binding, tuple) or len(binding) != 8:
            raise Rejected("UNKNOWN operation binding must be an immutable eight-tuple")
        auth_id, publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id, d_proof, i_commit_won_proof = binding
        if self.authorizations.get(auth_id) != (
            publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id
        ):
            raise Rejected("UNKNOWN operation authorization binding mismatch")
        publication = self.publication_participants.get(publication_id)
        if (
            publication is None or publication[1] != storage_id
            or publication[3:] != (request_digest, owner_boundary, final_visibility_gate_id)
        ):
            raise Rejected("UNKNOWN operation publication/Storage/digest/boundary mismatch")
        storage = self.storage_participants.get(storage_id)
        if storage is None or storage[0] != publication[0]:
            raise Rejected("UNKNOWN operation Storage participant belongs to another work")
        if d_proof != (
            "D_ADMITTED", publication_id, storage_id, request_digest, owner_boundary, final_visibility_gate_id
        ):
            raise Rejected("UNKNOWN operation D admission proof mismatch")
        if i_commit_won_proof != (
            "I_COMMIT_WON", auth_id, publication_id, storage_id,
            request_digest, owner_boundary, final_visibility_gate_id,
        ):
            raise Rejected("UNKNOWN operation I COMMIT_WON proof mismatch")
        return auth_id, publication_id, storage_id

    def mark_unknown(self, operation_id, binding=None):
        if operation_id in self.outcomes or operation_id in self.receipts:
            raise Rejected("cannot mark a terminal operation UNKNOWN")
        if operation_id not in self.i_pending:
            raise Rejected("UNKNOWN Storage outcome requires pending I COMMIT_WON")
        if binding is not None:
            self._validate_unknown_binding(binding)
            prior = self.operation_bindings.get(operation_id)
            if prior is not None and prior != binding:
                raise Rejected("UNKNOWN operation identity rebound")
        self.private_unknown.add(operation_id)

    def resolve_no_publication(self, operation_id, proof):
        if operation_id not in self.private_unknown:
            raise Rejected("NO_PUBLICATION reconciliation requires an UNKNOWN operation")
        if operation_id in self.outcomes or operation_id in self.receipts:
            raise Rejected("operation already has a terminal outcome")
        if operation_id not in self.i_pending:
            raise Rejected("NO_PUBLICATION reconciliation requires pending I COMMIT_WON")
        if not isinstance(proof, StorageNoPublicationProof):
            raise Rejected("NO_PUBLICATION proof must use the typed test-seam record")
        binding = self.operation_bindings.get(operation_id)
        if binding is None:
            raise Rejected("UNKNOWN operation has no immutable binding to reconcile")
        auth_id, publication_id, storage_id = self._validate_unknown_binding(binding)
        if proof.operation_id != operation_id or proof.operation_binding != binding:
            raise Rejected("NO_PUBLICATION proof does not bind the exact UNKNOWN operation")
        if publication_id != proof.publication_id or storage_id != proof.storage_id:
            raise Rejected("NO_PUBLICATION proof participant identity mismatch")
        if not self.fence_installed or publication_id not in self.fence_pending:
            raise Rejected("NO_PUBLICATION reconciliation requires the active ForgetFence participant barrier")
        if publication_id in self.visibility or operation_id in self.outbox or auth_id not in self.consumed:
            raise Rejected("local state contradicts NO_PUBLICATION proof or missing I COMMIT_WON consumption")
        if not proof.complete():
            raise Rejected("Storage NO_PUBLICATION proof is incomplete")
        outcome = ("NO_PUBLICATION", operation_id, publication_id, storage_id)
        self.outcomes[operation_id] = outcome
        self.storage_no_publication_proofs[operation_id] = proof
        self.private_unknown.remove(operation_id)
        return outcome

    def close_d(self, operation_id, authoritative_outcome):
        if self.outcomes.get(operation_id) != authoritative_outcome:
            raise Rejected("D closeout requires exact authoritative Storage outcome")
        self.d_closed[operation_id] = authoritative_outcome
        if isinstance(authoritative_outcome, tuple) and len(authoritative_outcome) >= 3:
            self.fence_pending.discard(authoritative_outcome[2])

    def close_i(self, operation_id, authoritative_outcome):
        if self.outcomes.get(operation_id) != authoritative_outcome:
            raise Rejected("I closeout requires exact authoritative Storage outcome")
        binding = self.i_pending.get(operation_id)
        if binding is None or authoritative_outcome[2:4] != binding[1:3]:
            raise Rejected("I closeout requires its exact unresolved participant")
        self.i_closed[operation_id] = authoritative_outcome
        del self.i_pending[operation_id]
        auth_id = binding[0]
        if auth_id in self.revocation_pending and not any(
            pending[0] == auth_id for pending in self.i_pending.values()
        ):
            self.revocation_pending.remove(auth_id)


class PublicationProtocolTests(unittest.TestCase):
    def prepared(self):
        p = Protocol()
        p.register_producer("work-1", 0)
        p.register_dependencies("work-1", ["root", "child-a", "child-b"])
        p.create_hidden_storage_participant("storage-1", "work-1")
        p.admit_publication("publication-1", "work-1", "storage-1", "request-digest-1", "owner-boundary-1", "visibility-gate-1")
        p.authorize_commit("auth-1", "publication-1", "storage-1", "request-digest-1", "owner-boundary-1", "visibility-gate-1")
        return p

    def commit_args(self):
        return dict(
            operation_id="op-1", auth_id="auth-1",
            publication_id="publication-1", storage_id="storage-1",
            request_digest="request-digest-1", owner_boundary="owner-boundary-1", final_visibility_gate_id="visibility-gate-1",
            d_proof=("D_ADMITTED", "publication-1", "storage-1", "request-digest-1", "owner-boundary-1", "visibility-gate-1"),
            i_commit_won_proof=("I_COMMIT_WON", "auth-1", "publication-1", "storage-1", "request-digest-1", "owner-boundary-1", "visibility-gate-1"),
        )

    def consume_i(self, p, args=None):
        args = dict(args or self.commit_args())
        args["i_commit_won_proof"] = p.consume_i_commit_won(
            args["operation_id"], args["auth_id"], args["publication_id"],
            args["storage_id"], args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"], args["d_proof"],
        )
        return args

    def no_publication_proof(self, *, operation_binding=None, **overrides):
        args = self.commit_args()
        binding = operation_binding or (
            args["auth_id"], args["publication_id"], args["storage_id"],
            args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
            args["d_proof"], args["i_commit_won_proof"],
        )
        values = dict(
            operation_id="op-1",
            operation_binding=binding,
            publication_id="publication-1",
            storage_id="storage-1",
            visibility_pointer_absent=True,
            outbox_absent=True,
            unresolved_participants_absent=True,
            writers_fenced=True,
            stage_publishers_fenced=True,
            retries_fenced=True,
            delayed_publishers_fenced=True,
            outbox_handlers_fenced=True,
            conflicting_commit_absent=True,
            restore_preserves_terminal=True,
        )
        values.update(overrides)
        return StorageNoPublicationProof(**values)

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
            p.admit_publication("publication-1", "work-1", "storage-1", "request-digest-1", "owner-boundary-1", "visibility-gate-1")

    def test_publication_already_closed_by_d_before_fence_is_not_pending(self):
        p = self.prepared()
        args = self.consume_i(p)
        p.commit(**args)
        outcome = p.outcomes["op-1"]
        p.close_i("op-1", outcome)
        p.close_d("op-1", outcome)
        p.install_forget_fence()
        self.assertNotIn("publication-1", p.fence_pending)

    def test_publication_first_remains_fence_barrier_until_d_closeout(self):
        p = self.prepared()
        p.install_forget_fence()
        self.assertIn("publication-1", p.fence_pending)
        args = self.consume_i(p)
        receipt = p.commit(**args)
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

    def test_admission_requires_nonempty_final_visibility_gate(self):
        p = self.prepared()
        with self.assertRaisesRegex(Rejected, "final visibility gate identity"):
            p.admit_publication(
                "publication-without-gate", "work-1", "storage-1",
                "request-digest-1", "owner-boundary-1", "",
            )

    def test_publication_must_bind_exact_storage_participant(self):
        p = self.prepared()
        with self.assertRaises(Rejected):
            p.admit_publication("p2", "work-1", "storage-does-not-exist", "request-digest-1", "owner-boundary-1", "visibility-gate-1")
        with self.assertRaises(Rejected):
            p.admit_publication("p3", "other-work", "storage-1", "request-digest-1", "owner-boundary-1", "visibility-gate-1")

    def test_authorization_is_bound_to_exact_participants(self):
        p = self.prepared()
        with self.assertRaises(Rejected):
            p.authorize_commit("wrong-auth", "publication-1", "other-storage", "request-digest-1", "owner-boundary-1", "visibility-gate-1")

    def test_authorization_replay_remains_idempotent_after_commit_won(self):
        p = self.prepared()
        args = self.consume_i(p)
        p.authorize_commit(
            args["auth_id"], args["publication_id"], args["storage_id"],
            args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
        )
        self.assertEqual(p.publication_commit_winners["publication-1"], "op-1")

    def test_new_authorization_is_rejected_after_commit_won(self):
        p = self.prepared()
        self.consume_i(p)
        with self.assertRaisesRegex(Rejected, "already has a COMMIT_WON operation"):
            p.authorize_commit(
                "auth-2", "publication-1", "storage-1",
                "request-digest-1", "owner-boundary-1", "visibility-gate-1",
            )

    def test_publication_participant_has_one_i_commit_winner_across_operation_ids(self):
        p = self.prepared()
        p.authorize_commit(
            "auth-2", "publication-1", "storage-1",
            "request-digest-1", "owner-boundary-1", "visibility-gate-1",
        )
        d_proof = (
            "D_ADMITTED", "publication-1", "storage-1",
            "request-digest-1", "owner-boundary-1", "visibility-gate-1",
        )
        p.consume_i_commit_won(
            "op-1", "auth-1", "publication-1", "storage-1",
            "request-digest-1", "owner-boundary-1", "visibility-gate-1", d_proof,
        )
        with self.assertRaisesRegex(Rejected, "already has a COMMIT_WON operation"):
            p.consume_i_commit_won(
                "op-2", "auth-2", "publication-1", "storage-1",
                "request-digest-1", "owner-boundary-1", "visibility-gate-1", d_proof,
            )
        self.assertEqual(set(p.i_pending), {"op-1"})
        self.assertIn("auth-1", p.consumed)
        self.assertNotIn("auth-2", p.consumed)

    def test_pre_winner_revocation_allows_new_authorization_for_same_participant(self):
        p = self.prepared()
        p.authorize_commit(
            "auth-2", "publication-1", "storage-1",
            "request-digest-1", "owner-boundary-1", "visibility-gate-1",
        )
        p.revoke("auth-1")
        d_proof = (
            "D_ADMITTED", "publication-1", "storage-1",
            "request-digest-1", "owner-boundary-1", "visibility-gate-1",
        )
        with self.assertRaises(Rejected):
            p.consume_i_commit_won(
                "op-1", "auth-1", "publication-1", "storage-1",
                "request-digest-1", "owner-boundary-1", "visibility-gate-1", d_proof,
            )
        proof = p.consume_i_commit_won(
            "op-2", "auth-2", "publication-1", "storage-1",
            "request-digest-1", "owner-boundary-1", "visibility-gate-1", d_proof,
        )
        self.assertEqual(
            proof,
            ("I_COMMIT_WON", "auth-2", "publication-1", "storage-1",
             "request-digest-1", "owner-boundary-1", "visibility-gate-1"),
        )
        self.assertEqual(p.publication_commit_winners["publication-1"], "op-2")

    def test_revocation_wins_before_commit(self):
        p = self.prepared()
        p.revoke("auth-1")
        with self.assertRaisesRegex(Rejected, "revocation won"):
            self.consume_i(p)

    def test_commit_wins_before_later_revocation(self):
        p = self.prepared()
        args = self.consume_i(p)
        p.revoke("auth-1")
        self.assertIn("auth-1", p.revocation_pending)
        self.assertEqual(self.consume_i(p, args)["i_commit_won_proof"], args["i_commit_won_proof"])
        receipt = p.commit(**args)
        outcome = p.outcomes["op-1"]
        self.assertEqual(p.receipts["op-1"], receipt)
        self.assertEqual(p.outcomes["op-1"], outcome)
        args2 = self.commit_args()
        args2["operation_id"] = "op-2"
        with self.assertRaisesRegex(Rejected, "revocation won|single-use|publication participant already has a COMMIT_WON operation"):
            self.consume_i(p, args2)
        p.close_i("op-1", outcome)
        self.assertNotIn("auth-1", p.revocation_pending)

    def test_authorization_is_single_use_across_distinct_operations(self):
        p = self.prepared()
        args = self.consume_i(p)
        p.commit(**args)
        args2 = self.commit_args()
        args2["operation_id"] = "op-2"
        with self.assertRaisesRegex(Rejected, "single-use|publication participant already has a COMMIT_WON operation"):
            self.consume_i(p, args2)

    def test_final_storage_commit_requires_both_exact_proofs(self):
        p = self.prepared()
        args = self.commit_args()
        args["d_proof"] = ("D_ADMITTED", "publication-1", "wrong-storage", args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"])
        with self.assertRaises(Rejected):
            self.consume_i(p, args)
        p = self.prepared()
        args = self.consume_i(p)
        args["i_commit_won_proof"] = ("I_TERMINAL", "auth-1")
        with self.assertRaises(Rejected):
            p.commit(**args)

    def test_crash_before_commit_leaves_no_partial_visibility_or_receipt(self):
        p = self.prepared()
        args = self.consume_i(p)
        args["fail_before_commit"] = True
        with self.assertRaises(RuntimeError):
            p.commit(**args)
        self.assertEqual(p.visibility, {})
        self.assertEqual(p.outcomes, {})
        self.assertEqual(p.receipts, {})
        self.assertEqual(p.outbox, {})
        self.assertEqual(p.consumed, {"auth-1"})
        self.assertIn("op-1", p.i_pending)
        args.pop("fail_before_commit")
        receipt = p.commit(**args)
        self.assertEqual(p.receipts["op-1"], receipt)

    def test_storage_commit_records_visibility_outcome_receipt_and_outbox_after_i_consumption(self):
        p = self.prepared()
        args = self.consume_i(p)
        receipt = p.commit(**args)
        self.assertEqual(p.consumed, {"auth-1"})
        self.assertIn("op-1", p.i_pending)
        self.assertEqual(p.visibility["publication-1"], "VISIBLE")
        self.assertEqual(p.outcomes["op-1"][0], "COMMITTED")
        self.assertEqual(p.receipts["op-1"], receipt)
        self.assertEqual(p.outbox["op-1"], ("PUBLISH", receipt))

    def test_lost_ack_retry_is_idempotent(self):
        p = self.prepared()
        args = self.consume_i(p)
        first = p.commit(**args)
        second = p.commit(**args)
        self.assertEqual(first, second)
        self.assertEqual(len(p.receipts), 1)
        self.assertEqual(len(p.outbox), 1)

    def test_operation_id_reuse_with_changed_participant_binding_conflicts(self):
        p = self.prepared()
        args = self.consume_i(p)
        p.commit(**args)
        changed = dict(args)
        changed["storage_id"] = "storage-substituted"
        changed["d_proof"] = ("D_ADMITTED", "publication-1", "storage-substituted", changed["request_digest"], changed["owner_boundary"], changed["final_visibility_gate_id"])
        changed["i_commit_won_proof"] = ("I_COMMIT_WON", "auth-1", "publication-1", "storage-substituted", changed["request_digest"], changed["owner_boundary"], changed["final_visibility_gate_id"])
        with self.assertRaises(Rejected):
            p.commit(**changed)
        self.assertEqual(len(p.receipts), 1)
        self.assertEqual(len(p.outbox), 1)


    def test_unknown_operation_id_cannot_be_recommitted(self):
        p = self.prepared()
        args = self.consume_i(p)
        p.mark_unknown("op-1")
        with self.assertRaisesRegex(Rejected, "UNKNOWN"):
            p.commit(**args)
        self.assertIn("op-1", p.private_unknown)
        self.assertEqual(p.visibility, {})
        self.assertEqual(p.outcomes, {})
        self.assertEqual(p.receipts, {})
        self.assertEqual(p.outbox, {})
        self.assertEqual(p.consumed, {"auth-1"})
        self.assertIn("op-1", p.i_pending)

    def test_unknown_stays_private_and_cannot_close_out(self):
        p = self.prepared()
        args = self.commit_args()
        args["operation_id"] = "op-unknown"
        self.consume_i(p, args)
        p.mark_unknown("op-unknown")
        self.assertIn("op-unknown", p.private_unknown)
        self.assertNotIn("publication-1", p.visibility)
        with self.assertRaises(Rejected):
            p.close_d("op-unknown", ("UNKNOWN",))
        with self.assertRaises(Rejected):
            p.close_i("op-unknown", ("UNKNOWN",))

    def test_no_publication_requires_every_storage_absence_and_fence_fact(self):
        p = self.prepared()
        p.install_forget_fence()
        args = self.consume_i(p)
        binding = (args["auth_id"], args["publication_id"], args["storage_id"],
                   args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
                   args["d_proof"], args["i_commit_won_proof"])
        p.mark_unknown("op-1", binding)
        p.install_forget_fence()
        required_facts = (
            "visibility_pointer_absent",
            "outbox_absent",
            "unresolved_participants_absent",
            "writers_fenced",
            "stage_publishers_fenced",
            "retries_fenced",
            "delayed_publishers_fenced",
            "outbox_handlers_fenced",
            "conflicting_commit_absent",
            "restore_preserves_terminal",
        )
        for fact in required_facts:
            with self.subTest(missing_fact=fact):
                proof = self.no_publication_proof(**{fact: False})
                with self.assertRaisesRegex(Rejected, "incomplete"):
                    p.resolve_no_publication("op-1", proof)
                self.assertIn("op-1", p.private_unknown)
                self.assertNotIn("op-1", p.outcomes)
                self.assertEqual(p.visibility, {})
                self.assertEqual(p.receipts, {})
                self.assertEqual(p.outbox, {})
                self.assertEqual(p.consumed, {"auth-1"})

    def test_no_publication_proof_must_bind_exact_unknown_operation(self):
        p = self.prepared()
        p.install_forget_fence()
        args = self.consume_i(p)
        binding = (args["auth_id"], args["publication_id"], args["storage_id"],
                   args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
                   args["d_proof"], args["i_commit_won_proof"])
        p.mark_unknown("op-1", binding)
        wrong_binding = ("other-auth",) + binding[1:]
        valid = self.no_publication_proof()
        invalid_proofs = (
            replace(valid, operation_id="other-operation"),
            replace(valid, operation_binding=wrong_binding),
            replace(valid, publication_id="other-publication"),
            replace(valid, storage_id="other-storage"),
        )
        for proof in invalid_proofs:
            with self.subTest(proof=proof):
                with self.assertRaises(Rejected):
                    p.resolve_no_publication("op-1", proof)
                self.assertIn("op-1", p.private_unknown)
                self.assertNotIn("op-1", p.outcomes)

    def test_no_publication_unknown_binding_must_match_registered_participants(self):
        p = self.prepared()
        args = self.consume_i(p)
        binding = (args["auth_id"], args["publication_id"], args["storage_id"],
                   args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
                   args["d_proof"], args["i_commit_won_proof"])
        invalid_bindings = (
            (args["auth_id"], args["publication_id"], "storage-substituted",
             args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
             args["d_proof"], args["i_commit_won_proof"]),
            (args["auth_id"], args["publication_id"], args["storage_id"],
             args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
             ("D_ADMITTED", args["publication_id"], "storage-substituted", args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"]),
             args["i_commit_won_proof"]),
            (args["auth_id"], args["publication_id"], args["storage_id"],
             args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
             args["d_proof"],
             ("I_COMMIT_WON", "other-auth", args["publication_id"], args["storage_id"], args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"])),
        )
        for invalid in invalid_bindings:
            with self.subTest(binding=invalid):
                with self.assertRaises(Rejected):
                    p.mark_unknown("op-1", invalid)
                self.assertNotIn("op-1", p.private_unknown)
        p.mark_unknown("op-1", binding)
        self.assertIn("op-1", p.private_unknown)

    def test_no_publication_rejects_local_state_contradicting_absence_proof(self):
        for state_name in ("visibility", "outbox", "missing_i_consumption"):
            with self.subTest(state=state_name):
                p = self.prepared()
                p.install_forget_fence()
                args = self.consume_i(p)
                binding = (args["auth_id"], args["publication_id"], args["storage_id"],
                           args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
                           args["d_proof"], args["i_commit_won_proof"])
                p.mark_unknown("op-1", binding)
                p.install_forget_fence()
                if state_name == "visibility":
                    p.visibility["publication-1"] = "VISIBLE"
                elif state_name == "outbox":
                    p.outbox["op-1"] = ("PUBLISH", ("RECEIPT", "op-1"))
                else:
                    p.consumed.remove("auth-1")
                with self.assertRaisesRegex(Rejected, "local state contradicts"):
                    p.resolve_no_publication("op-1", self.no_publication_proof())
                self.assertIn("op-1", p.private_unknown)
                self.assertNotIn("op-1", p.outcomes)

    def test_no_publication_reconciliation_requires_active_fence_barrier(self):
        p = self.prepared()
        args = self.consume_i(p)
        binding = (args["auth_id"], args["publication_id"], args["storage_id"],
                   args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
                   args["d_proof"], args["i_commit_won_proof"])
        p.mark_unknown("op-1", binding)
        proof = self.no_publication_proof()
        with self.assertRaisesRegex(Rejected, "active ForgetFence participant barrier"):
            p.resolve_no_publication("op-1", proof)
        self.assertIn("op-1", p.private_unknown)
        self.assertNotIn("op-1", p.outcomes)
        p.install_forget_fence()
        outcome = p.resolve_no_publication("op-1", proof)
        self.assertEqual(outcome, ("NO_PUBLICATION", "op-1", "publication-1", "storage-1"))

    def test_no_publication_reconciles_unknown_and_allows_exact_d_i_closeout(self):
        p = self.prepared()
        args = self.consume_i(p)
        binding = (args["auth_id"], args["publication_id"], args["storage_id"],
                   args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
                   args["d_proof"], args["i_commit_won_proof"])
        p.install_forget_fence()
        p.mark_unknown("op-1", binding)
        proof = self.no_publication_proof()
        outcome = p.resolve_no_publication("op-1", proof)
        self.assertEqual(outcome, ("NO_PUBLICATION", "op-1", "publication-1", "storage-1"))
        self.assertNotIn("op-1", p.private_unknown)
        self.assertEqual(p.storage_no_publication_proofs["op-1"], proof)
        self.assertEqual(p.visibility, {})
        self.assertEqual(p.receipts, {})
        self.assertEqual(p.outbox, {})
        self.assertEqual(p.consumed, {"auth-1"})
        self.assertIn("op-1", p.i_pending)
        self.assertIn("publication-1", p.fence_pending)
        p.close_i("op-1", outcome)
        self.assertNotIn("op-1", p.i_pending)
        self.assertIn("publication-1", p.fence_pending)
        p.close_d("op-1", outcome)
        self.assertNotIn("publication-1", p.fence_pending)

    def test_no_publication_is_terminal_and_requires_new_operation_id(self):
        p = self.prepared()
        p.install_forget_fence()
        args = self.consume_i(p)
        binding = (args["auth_id"], args["publication_id"], args["storage_id"],
                   args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
                   args["d_proof"], args["i_commit_won_proof"])
        p.mark_unknown("op-1", binding)
        p.install_forget_fence()
        p.resolve_no_publication("op-1", self.no_publication_proof())
        with self.assertRaisesRegex(Rejected, "already terminal"):
            p.commit(**args)
        self.assertEqual(p.visibility, {})
        self.assertEqual(p.receipts, {})
        self.assertEqual(p.outbox, {})

    def test_d_and_i_close_only_on_same_authoritative_storage_outcome(self):
        p = self.prepared()
        args = self.consume_i(p)
        p.commit(**args)
        outcome = p.outcomes["op-1"]
        p.close_d("op-1", outcome)
        p.close_i("op-1", outcome)
        self.assertEqual(p.d_closed["op-1"], p.i_closed["op-1"])
        with self.assertRaises(Rejected):
            p.close_i("op-1", ("COMMITTED", "different", "publication-1", "storage-1"))

    def test_commit_binding_rejects_request_digest_substitution(self):
        p = self.prepared()
        args = self.consume_i(p)
        args["request_digest"] = "request-digest-substituted"
        with self.assertRaises(Rejected):
            p.commit(**args)

    def test_commit_binding_rejects_owner_boundary_substitution(self):
        p = self.prepared()
        args = self.consume_i(p)
        args["owner_boundary"] = "owner-boundary-substituted"
        with self.assertRaises(Rejected):
            p.commit(**args)

    def test_commit_binding_rejects_final_visibility_gate_substitution(self):
        p = self.prepared()
        args = self.consume_i(p)
        args["final_visibility_gate_id"] = "visibility-gate-substituted"
        with self.assertRaises(Rejected):
            p.commit(**args)

    def test_i_commit_won_replay_rejects_request_digest_substitution(self):
        p = self.prepared()
        args = self.consume_i(p)
        changed = dict(args)
        changed["request_digest"] = "request-digest-substituted"
        with self.assertRaises(Rejected):
            self.consume_i(p, changed)

    def test_i_commit_won_replay_rejects_owner_boundary_substitution(self):
        p = self.prepared()
        args = self.consume_i(p)
        changed = dict(args)
        changed["owner_boundary"] = "owner-boundary-substituted"
        with self.assertRaises(Rejected):
            self.consume_i(p, changed)

    def test_i_commit_won_replay_rejects_final_visibility_gate_substitution(self):
        p = self.prepared()
        args = self.consume_i(p)
        changed = dict(args)
        changed["final_visibility_gate_id"] = "visibility-gate-substituted"
        with self.assertRaises(Rejected):
            self.consume_i(p, changed)

    def test_unknown_binding_rejects_request_digest_substitution(self):
        p = self.prepared()
        args = self.consume_i(p)
        wrong = (
            args["auth_id"], args["publication_id"], args["storage_id"],
            "request-digest-substituted", args["owner_boundary"], args["final_visibility_gate_id"],
            args["d_proof"], args["i_commit_won_proof"],
        )
        with self.assertRaises(Rejected):
            p.mark_unknown("op-1", wrong)
        self.assertNotIn("op-1", p.private_unknown)

    def test_unknown_binding_rejects_final_visibility_gate_substitution(self):
        p = self.prepared()
        args = self.consume_i(p)
        wrong = (
            args["auth_id"], args["publication_id"], args["storage_id"],
            args["request_digest"], args["owner_boundary"], "visibility-gate-substituted",
            args["d_proof"], args["i_commit_won_proof"],
        )
        with self.assertRaises(Rejected):
            p.mark_unknown("op-1", wrong)
        self.assertNotIn("op-1", p.private_unknown)

    def test_no_publication_proof_rejects_request_digest_substitution(self):
        p = self.prepared()
        p.install_forget_fence()
        args = self.consume_i(p)
        binding = (
            args["auth_id"], args["publication_id"], args["storage_id"],
            args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
            args["d_proof"], args["i_commit_won_proof"],
        )
        p.mark_unknown("op-1", binding)
        p.install_forget_fence()
        wrong = list(binding)
        wrong[3] = "request-digest-substituted"
        proof = self.no_publication_proof(operation_binding=tuple(wrong))
        with self.assertRaises(Rejected):
            p.resolve_no_publication("op-1", proof)
        self.assertIn("op-1", p.private_unknown)

    def test_no_publication_proof_rejects_final_visibility_gate_substitution(self):
        p = self.prepared()
        p.install_forget_fence()
        args = self.consume_i(p)
        binding = (
            args["auth_id"], args["publication_id"], args["storage_id"],
            args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
            args["d_proof"], args["i_commit_won_proof"],
        )
        p.mark_unknown("op-1", binding)
        p.install_forget_fence()
        wrong = list(binding)
        wrong[5] = "visibility-gate-substituted"
        proof = self.no_publication_proof(operation_binding=tuple(wrong))
        with self.assertRaises(Rejected):
            p.resolve_no_publication("op-1", proof)
        self.assertIn("op-1", p.private_unknown)

    def test_no_publication_proof_rejects_owner_boundary_substitution(self):
        p = self.prepared()
        p.install_forget_fence()
        args = self.consume_i(p)
        binding = (
            args["auth_id"], args["publication_id"], args["storage_id"],
            args["request_digest"], args["owner_boundary"], args["final_visibility_gate_id"],
            args["d_proof"], args["i_commit_won_proof"],
        )
        p.mark_unknown("op-1", binding)
        p.install_forget_fence()
        wrong = list(binding)
        wrong[4] = "owner-boundary-substituted"
        proof = self.no_publication_proof(operation_binding=tuple(wrong))
        with self.assertRaises(Rejected):
            p.resolve_no_publication("op-1", proof)
        self.assertIn("op-1", p.private_unknown)


if __name__ == "__main__":
    unittest.main(verbosity=2)
