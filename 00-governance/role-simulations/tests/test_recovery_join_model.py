import unittest
from recovery_join_model import (
    OwnerSnapshot, MembershipProof, CanonicalUnion, TwoPhaseRecovery,
    verify_membership, digest, JoinError
)


def snapshot(owner, rows=("row-1",), high_water=10, complete=True,
             anti_rollback=True, empty_signed=False):
    return OwnerSnapshot(
        owner=owner, rows=tuple(rows), high_water=high_water,
        snapshot_ref=f"{owner}-snapshot", snapshot_digest=f"{owner}-snapshot-digest",
        query_id=f"{owner}-query", pagination_complete=complete,
        anti_rollback_current=anti_rollback, complete_empty_signed=empty_signed
    )


def proof(snap, row, sequence=1, signature=True, key_current=True):
    return MembershipProof(
        owner=snap.owner, row_id=row, sequence=sequence,
        snapshot_ref=snap.snapshot_ref, snapshot_digest=snap.snapshot_digest,
        proof_digest=f"proof:{snap.owner}:{row}",
        signature_valid=signature, key_status_current=key_current
    )


class MembershipCompletenessTests(unittest.TestCase):
    def test_exact_row_membership_passes(self):
        s = snapshot("D")
        self.assertTrue(verify_membership(s, proof(s, "row-1")))

    def test_row_not_in_snapshot_fails(self):
        s = snapshot("D")
        with self.assertRaises(JoinError):
            verify_membership(s, proof(s, "not-in-snapshot"))

    def test_row_above_owner_high_water_fails(self):
        s = snapshot("I", high_water=4)
        with self.assertRaises(JoinError):
            verify_membership(s, proof(s, "row-1", sequence=5))

    def test_membership_proof_does_not_replace_pagination_completeness(self):
        s = snapshot("D", complete=False)
        self.assertTrue(verify_membership(s, proof(s, "row-1")))
        with self.assertRaises(JoinError):
            s.assert_complete()

    def test_empty_set_requires_signed_complete_empty(self):
        unsigned = snapshot("I", rows=(), empty_signed=False)
        with self.assertRaises(JoinError):
            unsigned.assert_complete()
        signed = snapshot("I", rows=(), empty_signed=True)
        self.assertTrue(signed.assert_complete() is None)

    def test_stale_key_or_bad_signature_fails_membership(self):
        s = snapshot("D")
        with self.assertRaises(JoinError):
            verify_membership(s, proof(s, "row-1", signature=False))
        with self.assertRaises(JoinError):
            verify_membership(s, proof(s, "row-1", key_current=False))


class CanonicalUnionTests(unittest.TestCase):
    def test_unregistered_owner_admission_is_union_member_once(self):
        d = snapshot("D", rows=("d-row",))
        i = snapshot("I", rows=("i-row",))
        proofs = (proof(d, "d-row"), proof(i, "i-row"))
        union = CanonicalUnion(
            coc_participants=("coc-1",),
            owner_rows=({"owner": "D", "row_id": "d-row", "absence_reason": "not-in-frozen-prefix"},),
            snapshots={"D": d, "I": i},
            proofs=proofs,
            owner_bindings={"coc-1": (("I", "i-row"),)}
        ).build("epoch-1", "prefix-digest")
        self.assertEqual(union["coc_participant_count"], 1)
        self.assertEqual(union["owner_local_admission_count"], 1)
        self.assertEqual(union["manifest_member_count"], 2)

    def test_embedded_owner_binding_is_not_double_counted(self):
        d = snapshot("D", rows=("d-row",))
        union = CanonicalUnion(
            coc_participants=("coc-1",),
            owner_rows=({"owner": "D", "row_id": "d-row", "parent_intent_ref": "coc-1"},),
            snapshots={"D": d},
            proofs=(proof(d, "d-row"),),
            owner_bindings={"coc-1": (("D", "d-row"),)}
        ).build("epoch-1", "prefix")
        self.assertEqual(union["manifest_member_count"], 1)
        self.assertEqual(union["owner_local_admission_count"], 0)

    def test_owner_only_member_requires_absence_reason(self):
        d = snapshot("D", rows=("d-row",))
        with self.assertRaises(JoinError):
            CanonicalUnion(
                coc_participants=(),
                owner_rows=({"owner": "D", "row_id": "d-row"},),
                snapshots={"D": d}, proofs=(proof(d, "d-row"),)
            ).build("epoch-1", "prefix")

    def test_snapshot_row_must_be_represented_exactly_once(self):
        d = snapshot("D", rows=("d1", "d2"))
        with self.assertRaises(JoinError):
            CanonicalUnion(
                coc_participants=(),
                owner_rows=({"owner": "D", "row_id": "d1", "absence_reason": "no-coc"},),
                snapshots={"D": d}, proofs=(proof(d, "d1"),)
            ).build("epoch-1", "prefix")

    def test_duplicate_owner_admission_is_rejected(self):
        d = snapshot("D", rows=("d1",))
        row = {"owner": "D", "row_id": "d1", "absence_reason": "no-coc"}
        with self.assertRaises(JoinError):
            CanonicalUnion(
                coc_participants=(), owner_rows=(row, row),
                snapshots={"D": d}, proofs=(proof(d, "d1"),)
            ).build("epoch-1", "prefix")


class BatchManifestTests(unittest.TestCase):
    def test_batch_first_crash_remains_fenced_until_same_manifest_commits(self):
        r = TwoPhaseRecovery()
        r.commit_batch("batch-1", "batch-digest", "manifest-content")
        self.assertEqual(r.state, "BATCH_COMMITTED_MANIFEST_PENDING")
        with self.assertRaises(JoinError):
            r.complete()
        r.commit_manifest("batch-1", "manifest-content", "manifest-entry", ("m1",))
        self.assertEqual(r.state, "MANIFEST_COMMITTED_OWNER_RELEASES_PENDING")

    def test_same_batch_identity_changed_digest_conflicts(self):
        r = TwoPhaseRecovery()
        r.commit_batch("batch-1", "batch-digest", "manifest-content")
        with self.assertRaises(JoinError):
            r.commit_batch("batch-1", "changed-batch-digest", "manifest-content")

    def test_manifest_cannot_be_committed_before_batch(self):
        r = TwoPhaseRecovery()
        with self.assertRaises(JoinError):
            r.commit_manifest("batch-1", "manifest-content", "manifest-entry", ())

    def test_owner_release_requires_unchanged_high_water_and_both_digests(self):
        r = TwoPhaseRecovery()
        r.commit_batch("batch-1", "batch-digest", "manifest-content")
        r.commit_manifest("batch-1", "manifest-content", "manifest-entry", ("m1",))
        with self.assertRaises(JoinError):
            r.release_owner("I", 4, 5, "manifest-content", "manifest-entry")
        with self.assertRaises(JoinError):
            r.release_owner("I", 4, 4, "manifest-content", "wrong-entry")
        r.release_owner("I", 4, 4, "manifest-content", "manifest-entry")

    def test_recovery_epoch_needs_each_owner_release(self):
        r = TwoPhaseRecovery()
        r.commit_batch("batch-1", "batch-digest", "manifest-content")
        r.commit_manifest("batch-1", "manifest-content", "manifest-entry", ("m1",))
        r.release_owner("I", 4, 4, "manifest-content", "manifest-entry")
        r.release_owner("D", 7, 7, "manifest-content", "manifest-entry")
        with self.assertRaises(JoinError):
            r.complete()
        r.release_owner("C", 9, 9, "manifest-content", "manifest-entry")
        self.assertEqual(r.complete(), "RECOVERY_EPOCH_COMPLETED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
