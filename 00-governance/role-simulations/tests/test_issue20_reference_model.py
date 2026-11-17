import unittest
from issue20_reference_model import (
    DAuthority, IAuthority, StorageAuthority, Publication, Protocol,
    RestoreGate, ProtocolError, UnknownOutcome, FRecallProjection,
    EDerivation, GContextVersion
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


class OwnerSnapshotCompletenessTests(unittest.TestCase):
    def snapshot(self, rows=None):
        return __import__("issue20_reference_model").OwnerSnapshot(
            "I", 4, "i:100", list(rows or []),
            pagination_complete=True, attested=True, anti_rollback=True
        )

    def test_membership_does_not_imply_complete_enumeration(self):
        snap = self.snapshot(["producer-A"])
        snap.pagination_complete = False
        snap.attested = False
        snap.anti_rollback = False
        self.assertTrue(snap.proves_membership("producer-A", 4))
        with self.assertRaises(ProtocolError):
            snap.seal_complete(1, snap.ordered_root(snap.rows))

    def test_complete_snapshot_requires_all_independent_evidence(self):
        snap = self.snapshot(["producer-A"])
        proof = snap.seal_complete(1, snap.ordered_root(snap.rows))
        self.assertEqual(proof["count"], 1)
        self.assertTrue(snap.sealed)

    def test_empty_snapshot_requires_explicit_complete_empty_proof(self):
        snap = self.snapshot([])
        with self.assertRaises(ProtocolError):
            snap.seal_complete(0, snap.ordered_root([]))
        snap.complete_empty_proof = True
        self.assertEqual(snap.seal_complete(0, snap.ordered_root([]))["count"], 0)

    def test_late_discovered_row_invalidates_previous_snapshot_seal(self):
        snap = self.snapshot(["producer-A"])
        snap.seal_complete(1, snap.ordered_root(snap.rows))
        snap.discover_late_row("producer-B")
        self.assertFalse(snap.sealed)
        with self.assertRaises(ProtocolError):
            snap.seal_complete(2, snap.ordered_root(snap.rows))

    def test_snapshot_membership_is_generation_bound(self):
        snap = self.snapshot(["producer-A"])
        self.assertTrue(snap.proves_membership("producer-A", 4))
        self.assertFalse(snap.proves_membership("producer-A", 5))


class RecoveryManifestTests(unittest.TestCase):
    def test_cutoff_must_commit_before_manifest_reconciliation(self):
        manifest = __import__("issue20_reference_model").RecoveryManifest()
        with self.assertRaises(ProtocolError):
            manifest.reconcile([], [])

    def test_union_uses_coc_prefix_and_independent_owner_high_waters(self):
        manifest = __import__("issue20_reference_model").RecoveryManifest()
        manifest.commit_cutoff("batch-1", "batch-digest-1", 10,
                               {"D": 20, "I": 35, "C": 8})
        result = manifest.reconcile(
            [{"participant_ref": "p-1", "coc_position": 10}],
            [{"owner": "D", "admission_ref": "d-1", "owner_position": 20},
             {"owner": "I", "admission_ref": "i-1", "owner_position": 35}]
        )
        self.assertNotEqual(result["member_set_root"], result["manifest_content_digest"])
        self.assertNotEqual(result["manifest_record_entry_digest"], result["batch_entry_digest"])

    def test_member_beyond_coc_prefix_is_rejected(self):
        manifest = __import__("issue20_reference_model").RecoveryManifest()
        manifest.commit_cutoff("batch-1", "digest-1", 10, {"D": 20})
        with self.assertRaises(ProtocolError):
            manifest.reconcile(
                [{"participant_ref": "p-1", "coc_position": 11}], [])

    def test_owner_admission_beyond_its_own_high_water_is_rejected(self):
        manifest = __import__("issue20_reference_model").RecoveryManifest()
        manifest.commit_cutoff("batch-1", "digest-1", 10, {"D": 20, "I": 35})
        with self.assertRaises(ProtocolError):
            manifest.reconcile([], [
                {"owner": "D", "admission_ref": "d-1", "owner_position": 21}
            ])

    def test_cutoff_and_manifest_are_idempotent_across_recovery(self):
        manifest = __import__("issue20_reference_model").RecoveryManifest()
        cutoff = manifest.commit_cutoff("batch-1", "digest-1", 10, {"D": 20})
        same = manifest.commit_cutoff("batch-1", "digest-1", 10, {"D": 20})
        self.assertEqual(cutoff, same)
        first = manifest.reconcile([], [])
        self.assertEqual(first, manifest.reconcile([], []))
        with self.assertRaises(ProtocolError):
            manifest.commit_cutoff("batch-2", "digest-2", 11, {"D": 21})
        with self.assertRaises(ProtocolError):
            manifest.reconcile(
                [{"participant_ref": "late", "coc_position": 9}], [])


class FRecallGateTests(unittest.TestCase):
    def test_candidate_is_not_returned_without_current_d_and_i_proofs(self):
        f = FRecallProjection()
        f.index("memory-1", "source-digest")
        self.assertEqual(f.return_page(["memory-1"], {"memory-1"}, set()), [])
        self.assertEqual(f.return_page(["memory-1"], set(), {"memory-1"}), [])

    def test_every_page_revalidates_and_forget_invalidates_projection(self):
        f = FRecallProjection()
        f.index("memory-1", "source-digest")
        self.assertEqual(f.return_page(["memory-1"], {"memory-1"}, {"memory-1"}),
                         ["memory-1"])
        f.invalidate("memory-1")
        self.assertEqual(f.return_page(["memory-1"], {"memory-1"}, {"memory-1"}), [])

    def test_integrity_unknown_fails_closed(self):
        f = FRecallProjection()
        f.index("memory-1", "source-digest")
        self.assertEqual(f.return_page(["memory-1"], {"memory-1"}, {"memory-1"},
                                       integrity_ok=False), [])


class EDerivationLifecycleTests(unittest.TestCase):
    def test_retry_keeps_work_identity_and_increments_attempt(self):
        e = EDerivation("work-1", "request-digest")
        self.assertEqual(e.retry("request-digest"), 1)
        first_lease = e.lease_id
        self.assertEqual(e.retry("request-digest"), 2)
        self.assertEqual(e.work_item_id, "work-1")
        self.assertNotEqual(first_lease, e.lease_id)

    def test_same_work_identity_with_changed_digest_conflicts(self):
        e = EDerivation("work-1", "request-digest")
        with self.assertRaises(ProtocolError):
            e.retry("changed-digest")

    def test_d_admission_cannot_precede_storage_prepare(self):
        e = EDerivation("work-1", "request-digest")
        e.retry("request-digest")
        e.stage_private("artifact-digest")
        with self.assertRaises(ProtocolError):
            e.admit_d("d-admission-1")

    def test_unknown_and_lease_retry_are_not_no_publication(self):
        e = EDerivation("work-1", "request-digest")
        e.retry("request-digest")
        e.stage_private("artifact-digest")
        e.prepare_storage("storage-participant-1")
        e.admit_d("d-admission-1")
        with self.assertRaises(UnknownOutcome):
            e.resolve("UNKNOWN")
        self.assertEqual(e.state, "UNKNOWN_IN_DOUBT")
        self.assertIsNone(e.terminal_outcome)

    def test_terminal_publication_requires_storage_and_d_join(self):
        e = EDerivation("work-1", "request-digest")
        e.retry("request-digest")
        e.stage_private("artifact-digest")
        e.prepare_storage("storage-participant-1")
        e.admit_d("d-admission-1")
        self.assertEqual(e.resolve("COMMITTED_VISIBLE"), "PUBLISHED")


class GContextLineageTests(unittest.TestCase):
    def test_context_derivative_requires_source_lineage(self):
        g = GContextVersion()
        with self.assertRaises(ProtocolError):
            g.materialize("fragment-1", [], 3)

    def test_delta_rejects_stale_base_version(self):
        g = GContextVersion()
        g.materialize("fragment-1", ["memory-1"], 3)
        g.version += 1
        with self.assertRaises(ProtocolError):
            g.apply_delta(1, "fragment-2", ["memory-2"], 3)

    def test_forget_of_transitive_source_invalidates_context_and_delivery(self):
        g = GContextVersion()
        g.materialize("fragment-1", ["memory-1", "memory-parent"], 3)
        g.create_delivery("delivery-1", 1, 3)
        result = g.forget({"memory-parent"}, current_d_generation=4)
        self.assertTrue(result["stale"])
        with self.assertRaises(ProtocolError):
            g.replay_delivery("delivery-1", 4)

    def test_old_delivery_cannot_cross_d_generation_change(self):
        g = GContextVersion()
        g.materialize("fragment-1", ["memory-1"], 3)
        g.create_delivery("delivery-1", 1, 3)
        with self.assertRaises(ProtocolError):
            g.replay_delivery("delivery-1", 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
