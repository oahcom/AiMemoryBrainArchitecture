import unittest
from issue20_reference_model import (
    DAuthority, IAuthority, StorageAuthority, Publication, Protocol,
    RestoreGate, ProtocolError, UnknownOutcome
)


def publication():
    return Publication("pub-001", "sha256:" + "a" * 64,
                       "sp-001", "scope-A", "artifact-1")


class DAdmissionFenceTests(unittest.TestCase):
    def test_admission_before_fence_is_in_captured_prefix(self):
        d = DAuthority()
        d.admit("w1", "digest-1")
        snap = d.install_fence()
        self.assertEqual(snap["high_water"], 1)
        self.assertEqual(snap["member_ids"], ("w1",))

    def test_fence_before_admission_rejects_work(self):
        d = DAuthority()
        d.install_fence()
        with self.assertRaises(ProtocolError):
            d.admit("w1", "digest-1")

    def test_same_identity_same_digest_is_idempotent(self):
        d = DAuthority()
        first = d.admit("w1", "digest-1")
        self.assertEqual(first, d.admit("w1", "digest-1"))
        self.assertEqual(d.registration_high_water, 1)

    def test_same_identity_changed_digest_conflicts(self):
        d = DAuthority()
        d.admit("w1", "digest-1")
        with self.assertRaises(ProtocolError):
            d.admit("w1", "digest-2")

    def test_unknown_is_not_terminal_and_blocks_release(self):
        d = DAuthority()
        d.admit("w1", "digest-1")
        snap = d.install_fence()
        with self.assertRaises(ProtocolError):
            d.terminalize("w1", "UNKNOWN")
        with self.assertRaises(ProtocolError):
            d.release_fence(snap["generation"], snap["high_water"])

    def test_release_rejects_stale_generation(self):
        d = DAuthority()
        d.admit("w1", "digest-1")
        snap = d.install_fence()
        d.terminalize("w1", "NO_PUBLICATION")
        with self.assertRaises(ProtocolError):
            d.release_fence(snap["generation"] - 1, snap["high_water"])


class PublicationHandshakeTests(unittest.TestCase):
    def test_valid_publication(self):
        p = Protocol()
        self.assertEqual(p.publish(publication()), "COMMITTED_VISIBLE")

    def test_unknown_i_decision_keeps_artifact_private_and_gates_open(self):
        p = Protocol()
        with self.assertRaises(UnknownOutcome):
            p.publish(publication(), i_decision="UNKNOWN")
        self.assertEqual(p.storage.participants["sp-001"]["state"], "PRIVATE_PREPARED")
        self.assertIn("pub-001", p.d.unresolved)
        self.assertIn("pub-001", p.i.unresolved)

    def test_revocation_won_never_publishes(self):
        p = Protocol()
        self.assertEqual(p.publish(publication(), i_decision="REVOCATION_WON"),
                         "NO_PUBLICATION")
        self.assertNotEqual(p.storage.participants["sp-001"]["state"],
                            "COMMITTED_VISIBLE")

    def test_storage_unknown_keeps_private_bytes_and_d_barrier_open(self):
        p = Protocol()
        with self.assertRaises(UnknownOutcome):
            p.publish(publication(), storage_outcome="UNKNOWN")
        self.assertEqual(p.storage.participants["sp-001"]["state"], "PRIVATE_PREPARED")
        self.assertIn("pub-001", p.d.unresolved)

    def test_i_receipt_changed_digest_replay_conflicts(self):
        i = IAuthority()
        pub = publication()
        i.consume(pub, "COMMIT_WON")
        changed = Publication(pub.operation_id, "sha256:" + "b" * 64,
                              pub.participant_ref, pub.scope, pub.artifact_id)
        with self.assertRaises(ProtocolError):
            i.consume(changed, "COMMIT_WON")

    def test_storage_rejects_stale_permission_epoch(self):
        s = StorageAuthority()
        pub = publication()
        s.prepare(pub)
        d_receipt = {"work_id": pub.operation_id, "digest": pub.digest,
                     "generation": 1}
        i_receipt = {"outcome": "COMMIT_WON", "digest": pub.digest,
                     "participant_ref": pub.participant_ref,
                     "permission_epoch": "perm-old"}
        with self.assertRaises(ProtocolError):
            s.resolve(pub, d_receipt, i_receipt, 1, "perm-new",
                      "COMMITTED_VISIBLE")

    def test_missing_storage_participant_is_unknown_not_abort(self):
        s = StorageAuthority()
        pub = publication()
        d_receipt = {"work_id": pub.operation_id, "digest": pub.digest,
                     "generation": 1}
        i_receipt = {"outcome": "COMMIT_WON", "digest": pub.digest,
                     "participant_ref": pub.participant_ref,
                     "permission_epoch": "perm-1"}
        with self.assertRaises(UnknownOutcome):
            s.resolve(pub, d_receipt, i_receipt, 1, "perm-1",
                      "COMMITTED_VISIBLE")

    def test_d_fence_generation_change_invalidates_admission(self):
        p = Protocol()
        pub = publication()
        p.storage.prepare(pub)
        d_receipt = p.d.admit(pub.operation_id, pub.digest)
        p.d.install_fence()
        i_receipt = p.i.consume(pub, "COMMIT_WON")
        with self.assertRaises(ProtocolError):
            p.storage.resolve(pub, d_receipt, i_receipt, p.d.generation,
                              p.i.permission_epoch, "COMMITTED_VISIBLE")

    def test_revocation_after_commit_won_waits_for_storage_terminal(self):
        i = IAuthority()
        pub = publication()
        i.consume(pub, "COMMIT_WON")
        self.assertEqual(i.revoke(), "PENDING")
        self.assertIn(pub.operation_id, i.unresolved)
        self.assertEqual(i.close_participant(pub, "NO_PUBLICATION"),
                         "REVOCATION_EFFECTIVE")
        self.assertFalse(i.unresolved)

    def test_revocation_before_receipt_consumption_wins(self):
        i = IAuthority()
        self.assertEqual(i.revoke(), "EFFECTIVE")
        receipt = i.consume(publication(), "COMMIT_WON")
        self.assertEqual(receipt["outcome"], "REVOCATION_WON")


class RestoreGateTests(unittest.TestCase):
    def test_restore_requires_all_independent_owner_proofs(self):
        gate = RestoreGate()
        for owner in ("storage", "coc", "i", "d", "f", "e", "g"):
            gate.attest(owner, "digest-" + owner)
        with self.assertRaises(ProtocolError):
            gate.release()

    def test_stale_owner_proof_blocks_restore(self):
        gate = RestoreGate()
        for owner in gate.required:
            gate.attest(owner, "digest-" + owner, current=(owner != "i"))
        with self.assertRaises(ProtocolError):
            gate.release()
        self.assertEqual(gate.state, "RESTORE_FENCED")

    def test_complete_current_proof_conjunction_releases(self):
        gate = RestoreGate()
        for owner in gate.required:
            gate.attest(owner, "digest-" + owner)
        self.assertEqual(gate.release(), "SERVING")


if __name__ == "__main__":
    unittest.main(verbosity=2)
