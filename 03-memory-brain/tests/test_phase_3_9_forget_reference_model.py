"""Phase 3.9 logical reference model tests.

These tests exercise the proposed state-machine semantics only. They do not
implement or prove production D/Storage/I transaction, crypto, HA, or read-path
conformance.
"""
import unittest
from dataclasses import dataclass, field


class Blocked(Exception):
    pass


class Conflict(Exception):
    pass


@dataclass(frozen=True)
class IReceipt:
    operation_id: str
    memory_id: str
    memory_version: int
    scope_digest: str
    fence_generation: int
    d_proof_digest: str
    event_digest: str
    permission_epoch: str
    nonce: str
    outcome: str


@dataclass
class ForgetReferenceModel:
    operation_id: str = "op-1"
    memory_id: str = "mem-1"
    memory_version: int = 7
    scope_digest: str = "scope-digest-A"
    phase: str = "REQUESTED"
    lifecycle_state: str = "Active"
    fence_generation: int = 0
    fence_active: bool = False
    read_suppressed: bool = False
    proof_digest: str | None = None
    barrier_members: dict = field(default_factory=dict)
    visible_artifacts: set = field(default_factory=set)
    inventoried_artifacts: set = field(default_factory=set)
    i_receipts: dict = field(default_factory=dict)
    i_unresolved: set = field(default_factory=set)
    i_closeouts: dict = field(default_factory=dict)
    i_revoked: bool = False
    i_revocation_pending: bool = False
    i_sequencer_unknown: bool = False
    global_forget_completed: bool = False
    physical_erasure_confirmed: bool = False

    def admit_publication(self, participant_id):
        if self.fence_active:
            raise Blocked("fence rejects new publication admission")
        self.barrier_members[participant_id] = "OPEN"

    def commit_visibility(self, participant_id, artifact_id):
        if participant_id not in self.barrier_members:
            raise Blocked("publication participant missing")
        if self.fence_active:
            raise Blocked("fence wins before visibility commit")
        self.barrier_members[participant_id] = "COMMITTED_VISIBLE"
        self.visible_artifacts.add(artifact_id)

    def install_fence(self):
        if self.fence_active:
            return self.fence_generation
        self.fence_generation += 1
        self.fence_active = True
        self.read_suppressed = True
        self.phase = "FENCE_INSTALLED"
        self.inventoried_artifacts.update(self.visible_artifacts)
        return self.fence_generation

    def read(self, artifact_id, fence_state_known=True):
        if not fence_state_known:
            return False
        if self.fence_active and artifact_id in self.visible_artifacts:
            return False
        return artifact_id in self.visible_artifacts

    def resolve_participant(self, participant_id, outcome, artifact_id=None,
                            visibility_linearized_before_fence=False):
        if participant_id not in self.barrier_members:
            raise Blocked("unknown barrier member")
        if outcome == "COMMITTED_VISIBLE":
            if self.fence_active and not visibility_linearized_before_fence:
                raise Blocked("post-fence visibility cannot be accepted")
            self.visible_artifacts.add(artifact_id)
            if self.fence_active:
                self.inventoried_artifacts.add(artifact_id)
            self.barrier_members[participant_id] = "COMMITTED_VISIBLE"
        elif outcome == "NO_PUBLICATION":
            self.barrier_members[participant_id] = "NO_PUBLICATION"
        elif outcome == "UNKNOWN":
            self.barrier_members[participant_id] = "UNKNOWN"
        else:
            raise ValueError("invalid outcome")

    def close_barrier(self):
        if not self.fence_active:
            raise Blocked("fence not installed")
        if any(v in {"OPEN", "UNKNOWN"} for v in self.barrier_members.values()):
            raise Blocked("unresolved barrier member")
        self.phase = "BARRIER_DRAINED"
        self.proof_digest = f"proof:{self.operation_id}:{self.fence_generation}"
        self.phase = "CANONICAL_SUPPRESSION_COMPLETE"
        return self.proof_digest

    def revoke_authorization(self):
        if self.i_unresolved:
            self.i_revocation_pending = True
        else:
            self.i_revoked = True

    def issue_i_receipt(self, *, event_digest, permission_epoch="i-epoch-9",
                        nonce="nonce-1"):
        if self.i_sequencer_unknown:
            outcome = "UNKNOWN"
        elif self.i_revoked:
            outcome = "REVOCATION_WON"
        else:
            outcome = "COMMIT_WON"
        receipt = IReceipt(
            self.operation_id, self.memory_id, self.memory_version,
            self.scope_digest, self.fence_generation, self.proof_digest or "",
            event_digest, permission_epoch, nonce, outcome
        )
        prior = self.i_receipts.get(nonce)
        if prior and prior != receipt:
            raise Conflict("nonce reused with changed tuple")
        self.i_receipts[nonce] = receipt
        if outcome == "COMMIT_WON":
            self.i_unresolved.add(nonce)
        return receipt

    def terminalize(self, receipt, *, event_digest, current_d_proof=True):
        if self.phase != "CANONICAL_SUPPRESSION_COMPLETE" or not self.proof_digest:
            raise Blocked("canonical suppression proof missing")
        if not current_d_proof or receipt.d_proof_digest != self.proof_digest:
            raise Blocked("D proof is stale")
        if receipt.outcome != "COMMIT_WON":
            raise Blocked("I did not authorize this exact terminalization")
        expected = (
            self.operation_id, self.memory_id, self.memory_version,
            self.scope_digest, self.fence_generation, self.proof_digest,
            event_digest
        )
        actual = (
            receipt.operation_id, receipt.memory_id, receipt.memory_version,
            receipt.scope_digest, receipt.fence_generation,
            receipt.d_proof_digest, receipt.event_digest
        )
        if actual != expected:
            raise Conflict("receipt tuple mismatch")
        if self.lifecycle_state == "Forgotten":
            result = "ALREADY_TERMINALIZED"
        else:
            self.lifecycle_state = "Forgotten"
            result = "D_TERMINALIZED"
        self.i_unresolved.discard(receipt.nonce)
        self.i_closeouts[receipt.nonce] = result
        if self.i_revocation_pending and not self.i_unresolved:
            self.i_revocation_pending = False
            self.i_revoked = True
        return result


class ForgetPhase39Tests(unittest.TestCase):
    def test_participant_first_fence_suppresses_reads_before_barrier_closes(self):
        m = ForgetReferenceModel()
        m.admit_publication("p1")
        m.install_fence()
        self.assertTrue(m.read_suppressed)
        self.assertFalse(m.read("artifact-1"))
        with self.assertRaises(Blocked):
            m.close_barrier()

    def test_fence_first_rejects_new_publication(self):
        m = ForgetReferenceModel()
        m.install_fence()
        with self.assertRaises(Blocked):
            m.admit_publication("p1")

    def test_fence_first_rejects_visibility_commit(self):
        m = ForgetReferenceModel()
        m.admit_publication("p1")
        m.install_fence()
        with self.assertRaises(Blocked):
            m.commit_visibility("p1", "artifact-1")

    def test_visibility_first_artifact_is_inventoried_and_suppressed(self):
        m = ForgetReferenceModel()
        m.admit_publication("p1")
        m.commit_visibility("p1", "artifact-1")
        self.assertTrue(m.read("artifact-1"))
        m.install_fence()
        self.assertIn("artifact-1", m.inventoried_artifacts)
        self.assertFalse(m.read("artifact-1"))

    def test_unresolved_participant_may_resolve_as_pre_fence_commit(self):
        m = ForgetReferenceModel()
        m.admit_publication("p1")
        m.install_fence()
        m.resolve_participant("p1", "COMMITTED_VISIBLE", "artifact-1",
                              visibility_linearized_before_fence=True)
        self.assertIn("artifact-1", m.inventoried_artifacts)
        self.assertFalse(m.read("artifact-1"))
        self.assertEqual(m.close_barrier(), "proof:op-1:1")

    def test_post_fence_visibility_cannot_be_accepted(self):
        m = ForgetReferenceModel()
        m.admit_publication("p1")
        m.install_fence()
        with self.assertRaises(Blocked):
            m.resolve_participant("p1", "COMMITTED_VISIBLE", "artifact-1")

    def test_unknown_participant_keeps_barrier_open_but_reads_suppressed(self):
        m = ForgetReferenceModel()
        m.admit_publication("p1")
        m.install_fence()
        m.resolve_participant("p1", "UNKNOWN")
        self.assertFalse(m.read("artifact-1"))
        with self.assertRaises(Blocked):
            m.close_barrier()

    def test_no_publication_terminalizes_barrier_member(self):
        m = ForgetReferenceModel()
        m.admit_publication("p1")
        m.install_fence()
        m.resolve_participant("p1", "NO_PUBLICATION")
        self.assertEqual(m.close_barrier(), "proof:op-1:1")
        self.assertEqual(m.phase, "CANONICAL_SUPPRESSION_COMPLETE")

    def test_unknown_fence_state_fails_closed(self):
        m = ForgetReferenceModel()
        m.admit_publication("p1")
        m.commit_visibility("p1", "artifact-1")
        self.assertFalse(m.read("artifact-1", fence_state_known=False))

    def test_requester_revocation_does_not_rollback_fence(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.revoke_authorization()
        self.assertTrue(m.fence_active)
        self.assertEqual(m.fence_generation, 1)
        self.assertTrue(m.read_suppressed)

    def test_forgotten_requires_current_d_proof_and_i_commit_won_receipt(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.close_barrier()
        receipt = m.issue_i_receipt(event_digest="event-1")
        self.assertEqual(m.terminalize(receipt, event_digest="event-1"), "D_TERMINALIZED")
        self.assertEqual(m.lifecycle_state, "Forgotten")

    def test_revocation_before_i_consumption_wins(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.close_barrier()
        m.revoke_authorization()
        receipt = m.issue_i_receipt(event_digest="event-1")
        self.assertEqual(receipt.outcome, "REVOCATION_WON")
        with self.assertRaises(Blocked):
            m.terminalize(receipt, event_digest="event-1")

    def test_revocation_after_commit_won_waits_for_exact_d_outcome(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.close_barrier()
        receipt = m.issue_i_receipt(event_digest="event-1")
        m.revoke_authorization()
        self.assertTrue(m.i_revocation_pending)
        self.assertFalse(m.i_revoked)
        m.terminalize(receipt, event_digest="event-1")
        self.assertFalse(m.i_revocation_pending)
        self.assertTrue(m.i_revoked)

    def test_unknown_i_sequencer_cannot_terminalize(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.close_barrier()
        m.i_sequencer_unknown = True
        receipt = m.issue_i_receipt(event_digest="event-1")
        self.assertEqual(receipt.outcome, "UNKNOWN")
        with self.assertRaises(Blocked):
            m.terminalize(receipt, event_digest="event-1")

    def test_stale_d_proof_cannot_terminalize(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.close_barrier()
        receipt = m.issue_i_receipt(event_digest="event-1")
        with self.assertRaises(Blocked):
            m.terminalize(receipt, event_digest="event-1", current_d_proof=False)

    def test_wrong_event_digest_is_rejected(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.close_barrier()
        receipt = m.issue_i_receipt(event_digest="event-1")
        with self.assertRaises(Conflict):
            m.terminalize(receipt, event_digest="event-2")

    def test_same_nonce_changed_tuple_conflicts(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.close_barrier()
        m.issue_i_receipt(event_digest="event-1", nonce="same")
        with self.assertRaises(Conflict):
            m.issue_i_receipt(event_digest="event-2", nonce="same")

    def test_d_forgotten_does_not_claim_global_or_physical_erasure(self):
        m = ForgetReferenceModel()
        m.install_fence()
        m.close_barrier()
        receipt = m.issue_i_receipt(event_digest="event-1")
        m.terminalize(receipt, event_digest="event-1")
        self.assertFalse(m.global_forget_completed)
        self.assertFalse(m.physical_erasure_confirmed)

    def test_fence_generation_is_idempotent_and_monotonic(self):
        m = ForgetReferenceModel()
        self.assertEqual(m.install_fence(), 1)
        self.assertEqual(m.install_fence(), 1)
        self.assertEqual(m.fence_generation, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
