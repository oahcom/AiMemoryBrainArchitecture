"""R3 contract-level tests.

DFI-001..022, I-U011-T01..T16, STOR-01..07.
These tests exercise the in-memory reference model only.
"""
import unittest

from r3_contract_model import (
    Authorization,
    ContractViolation,
    Lifecycle,
    Phase,
    Reconciliation,
    R3Model,
)


def auth(**kw):
    values = dict(
        issuer_known=True,
        signature_valid=True,
        audience_matches=True,
        operation_matches=True,
        request_hash_matches=True,
        purpose_matches=True,
        scope_matches=True,
        not_before=0,
        expires_at=100,
        permission_epoch=7,
        nonce_unused=True,
        delegation_current=True,
    )
    values.update(kw)
    return Authorization(**values)


def done():
    model = R3Model("mem")
    model.authorize_and_suppress(auth(), 10, 7, "op")
    return model


class DFI(unittest.TestCase):

    # DFI-001: Forgotten identity must not be readable.
    def test_DFI_001(self):
        m = done()
        self.assertFalse(m.read_allowed(m.fence_generation))
        self.assertFalse(m.read_allowed(None))

    # DFI-002: SuppressionCommitted triggers Forgotten before cleanup.
    def test_DFI_002(self):
        m = done()
        m.phase = Phase.CLEANUP
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertNotEqual(m.phase, Phase.COMPLETED)

    # DFI-003: Arbitrary lifecycle strings cannot trigger Forgotten.
    def test_DFI_003(self):
        m = R3Model("m")
        with self.assertRaises(ContractViolation):
            m.forgotten_transition("Cancel")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

    # DFI-004: Unknown required targets prevent D completion.
    def test_DFI_004(self):
        m = done()
        m.set_required_targets(["required", "unknown"])
        m.mark_target("required", "SUCCEEDED")
        m.mark_target("unknown", "UNKNOWN")
        self.assertFalse(m.domain_complete())
        self.assertIn("unknown", m.unknown_required_targets)

    # DFI-005: ACKNOWLEDGED is not proof of erasure.
    def test_DFI_005(self):
        m = done()
        m.set_required_targets(["adapter"])
        m.mark_target("adapter", "ACKNOWLEDGED")
        self.assertFalse(m.domain_complete())

    # DFI-006: Policy retention is not successful deletion.
    def test_DFI_006(self):
        m = done()
        m.set_required_targets(["retained"])
        m.mark_target("retained", "POLICY_RETAINED")
        self.assertFalse(m.domain_complete())

    # DFI-007: Same idempotency Key/Hash reuses operation;
    # different Hash under the same Key is rejected.
    def test_DFI_007(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        first = m.commit_suppression(
            "op-1", "attempt-1", "key-1", "hash-A", auth=auth()
        )
        m.phase = Phase.AUTHORIZED
        second = m.commit_suppression(
            "op-1", "attempt-2", "key-1", "hash-A", auth=auth()
        )
        self.assertIs(first, second)
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op-2", "attempt-3", "key-1", "hash-B", auth=auth()
            )

    # DFI-008: Stale attempt cannot publish a stage.
    def test_DFI_008(self):
        m = done()
        a = m.start_attempt("a1")
        b = m.start_attempt("a2")
        with self.assertRaises(ContractViolation):
            m.commit_stage("a1", a, "cleanup")
        m.commit_stage("a2", b, "cleanup")

    # DFI-009: UNKNOWN outcome requires reconciliation before retry.
    def test_DFI_009(self):
        m = done()
        m.start_attempt("a1")
        self.assertEqual(m.reconcile("UNKNOWN"), Reconciliation.UNKNOWN)
        with self.assertRaises(ContractViolation):
            m.retry("a2")
        m.reconcile("APPLIED")
        m.retry("a2")

    # DFI-010: PermissionEpoch mismatch fails closed.
    def test_DFI_010(self):
        m = R3Model("m")
        with self.assertRaises(ContractViolation):
            m.authorize_and_suppress(
                auth(permission_epoch=6), 10, 7, "op"
            )
        self.assertEqual(m.phase, Phase.FAILED)

    # DFI-011: Inventory revision changes invalidate previous completion.
    def test_DFI_011(self):
        m = done()
        m.set_required_targets(["a"])
        m.mark_target("a", "SUCCEEDED")
        self.assertTrue(m.domain_complete())
        revision = m.inventory_revision
        m.set_required_targets(["a", "b"])
        self.assertGreater(m.inventory_revision, revision)
        self.assertFalse(m.domain_complete())

    # DFI-012: Restore remains quarantined until Fence reconciliation.
    def test_DFI_012(self):
        m = done()
        m.begin_restore(0)
        self.assertFalse(m.restore_query_allowed())
        with self.assertRaises(ContractViolation):
            m.reconcile_restore(0, False)
        m.reconcile_restore(m.fence_generation, True)
        self.assertTrue(m.restore_query_allowed())

    # DFI-013: Producer admission/dependency registration races with Fence.
    def test_DFI_013(self):
        m = R3Model("m")
        old_fence = m.fence_generation
        self.assertTrue(m.producer_admission(old_fence))
        m.authorize_and_suppress(auth(), 10, 7, "op")
        with self.assertRaises(ContractViolation):
            m.register_dependency("late-producer", old_fence)
        self.assertFalse(m.producer_admission(old_fence))

    # DFI-014: Old producer lease cannot publish after a new attempt.
    def test_DFI_014(self):
        m = done()
        old = m.start_attempt("producer-old")
        new = m.start_attempt("producer-new")
        with self.assertRaises(ContractViolation):
            m.commit_stage("producer-old", old, "publish")
        m.commit_stage("producer-new", new, "publish")

    # DFI-015: Recall/delayed Cache Fill must recheck Fence before return.
    def test_DFI_015(self):
        m = R3Model("m")
        old_fence = m.fence_generation
        m.recall_cache_fill("k", "stale-value", old_fence)
        m.authorize_and_suppress(auth(), 10, 7, "op")
        with self.assertRaises(ContractViolation):
            m.recall_cache_fill("k", "late-value", old_fence)
        with self.assertRaises(ContractViolation):
            m.recall_return("k", old_fence)
        self.assertNotEqual(m.lifecycle, Lifecycle.ACTIVE)

    # DFI-016: Index rebuild cannot resurrect identity from stale snapshot.
    def test_DFI_016(self):
        m = done()
        with self.assertRaises(ContractViolation):
            m.rebuild_index(
                m.fence_generation - 1, {m.memory_id}
            )
        self.assertEqual(
            m.rebuild_index(m.fence_generation, {m.memory_id}), set()
        )

    # DFI-017: Offline Snapshot/Delta reconnect checks ContextVersion.
    def test_DFI_017(self):
        m = R3Model("m")
        snapshot = m.offline_snapshot(4)
        with self.assertRaises(ContractViolation):
            m.reconnect(snapshot, [
                {"context_version": 4, "operation": "Update"}
            ])
        self.assertEqual(m.context_version, 0)
        self.assertEqual(
            m.reconnect(snapshot, [
                {"context_version": 5, "operation": "Update"}
            ]),
            5,
        )

    # DFI-018: Context Remove is distinct from canonical Forget.
    def test_DFI_018(self):
        m = R3Model("m")
        m.context_remove()
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertIn("CONTEXT_REMOVE", m.audit)
        with self.assertRaises(ContractViolation):
            m.forgotten_transition("ContextRemove")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

    # DFI-019: ACKNOWLEDGED target cannot satisfy D completion.
    def test_DFI_019(self):
        m = done()
        m.set_required_targets(["adapter"])
        m.mark_target("adapter", "ACKNOWLEDGED")
        self.assertFalse(m.domain_complete())

    # DFI-020: Agent telemetry cannot trigger canonical Forget.
    def test_DFI_020(self):
        m = R3Model("m")
        with self.assertRaises(ContractViolation):
            m.forgotten_transition("AgentTelemetry")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

    # DFI-021: Atomic tuple abort and model-level recovery boundary.
    # This is NOT a physical Crash, WAL, or Failover durability test.
    def test_DFI_021(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        before = (
            m.lifecycle,
            m.fence_generation,
            m.phase,
            m.inventory_revision,
            dict(m.outbox),
            m.atomic_commit,
        )
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op", fail_before_commit=True, auth=auth()
            )
        after = (
            m.lifecycle,
            m.fence_generation,
            m.phase,
            m.inventory_revision,
            dict(m.outbox),
            m.atomic_commit,
        )
        self.assertEqual(before, after)

        commit = m.commit_suppression("op", auth=auth())
        self.assertEqual(set(m.atomic_tuple), set(R3Model.ATOMIC_FIELDS))
        self.assertEqual(commit.suppression_proof.commit_id, commit.commit_id)
        self.assertEqual(
            commit.authorization_reference,
            m.atomic_commit.authorization_reference,
        )
        self.assertEqual(
            commit.fence_tombstone.fence_generation,
            m.fence_generation,
        )

        # In-memory record inspection only; no physical WAL claim.
        recovered_record = m.atomic_commit
        self.assertIsNotNone(recovered_record)
        self.assertEqual(recovered_record, commit)
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)

    # DFI-022: Missing backup coverage is UNKNOWN; Restore stays quarantined.
    def test_DFI_022(self):
        m = done()
        m.set_backup_manifest(None)
        self.assertEqual(m.backup_coverage(), "UNKNOWN")
        m.begin_restore(0)
        self.assertTrue(m.restore_quarantined)
        self.assertFalse(m.restore_query_allowed())


class OwnerIU011(unittest.TestCase):

    def _deny(self, **kw):
        m = R3Model("m")
        with self.assertRaises(ContractViolation):
            m.authorize_and_suppress(auth(**kw), 10, 7, "op")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertEqual(m.fence_generation, 0)

    # I-U011-T01: Unknown issuer is denied.
    def test_T01(self):
        self._deny(issuer_known=False)

    # I-U011-T02: Audience, operation, hash, purpose and scope binding.
    def test_T02(self):
        for key in (
            "audience_matches", "operation_matches",
            "request_hash_matches", "purpose_matches", "scope_matches",
        ):
            with self.subTest(key=key):
                self._deny(**{key: False})

    # I-U011-T03: Nonce replay and temporal validity are denied.
    def test_T03(self):
        self._deny(nonce_unused=False)
        self._deny(expires_at=10)
        self._deny(not_before=11)

    # I-U011-T04: Stale PermissionEpoch is denied.
    def test_T04(self):
        self._deny(permission_epoch=6)

    # I-U011-T05: Revocation wins when it precedes commit.
    def test_T05(self):
        m = R3Model("m")
        self.assertEqual(m.revoke_race("REVOCATION_WON"), "REVOCATION_WON")
        self._deny(permission_epoch=6)

    # I-U011-T06: Commit wins when commit precedes revocation.
    def test_T06(self):
        m = done()
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertEqual(m.phase, Phase.SUPPRESSION_COMMITTED)
        self.assertEqual(m.revoke_race("COMMIT_WON"), "COMMIT_WON")

    # I-U011-T07: Unprovable ordering/currentness is UNKNOWN.
    def test_T07(self):
        m = R3Model("m")
        self.assertEqual(m.revoke_race("UNKNOWN"), "UNKNOWN")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        with self.assertRaises(ContractViolation):
            m.revoke_race("UNVERIFIABLE")

    # I-U011-T08: Stale delegation is denied.
    def test_T08(self):
        self._deny(delegation_current=False)

    # I-U011-T09: Legal Hold/Retention prevents suppression.
    def test_T09(self):
        m = R3Model("m")
        m.legal_hold = True
        with self.assertRaises(ContractViolation):
            m.authorize_and_suppress(auth(), 10, 7, "op")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertEqual(m.fence_generation, 0)

    # I-U011-T10: Exception approval, scope, basis, expiry and controls.
    def test_T10(self):
        m = R3Model("m")
        with self.assertRaises(ContractViolation):
            m.set_exception({"approver": "A", "scope": "S"})
        m.set_exception({
            "approver": "A",
            "scope": ["memory:m"],
            "basis": "documented-basis",
            "expires_at": 50,
            "controls": ["audit", "limited-access"],
        })
        self.assertTrue(m.exception_valid(49))
        self.assertFalse(m.exception_valid(50))

    # I-U011-T11: Policy-retained targets are not erased.
    def test_T11(self):
        m = done()
        m.set_required_targets(["held"])
        m.mark_target("held", "POLICY_RETAINED")
        self.assertFalse(m.domain_complete())

    # I-U011-T12: Unknown required target prevents completion.
    def test_T12(self):
        m = done()
        m.set_required_targets(["unknown"])
        m.mark_target("unknown", "UNKNOWN")
        self.assertFalse(m.domain_complete())

    # I-U011-T13: Inventory expansion invalidates prior completion.
    def test_T13(self):
        m = done()
        m.set_required_targets(["a"])
        m.mark_target("a", "SUCCEEDED")
        self.assertTrue(m.domain_complete())
        m.set_required_targets(["a", "new"])
        self.assertFalse(m.domain_complete())

    # I-U011-T14: Expired/revoked exception is no longer valid.
    def test_T14(self):
        m = R3Model("m")
        m.set_exception({
            "approver": "A",
            "scope": ["memory:m"],
            "basis": "approved-basis",
            "expires_at": 20,
            "controls": ["audit"],
        })
        self.assertTrue(m.exception_valid(19))
        m.apply_expired_exception(20)
        self.assertIsNone(m.exception)
        self.assertIn("EXCEPTION_EXPIRED_OR_REVOKED", m.audit)

    # I-U011-T15: Complete target evidence without D completion is rejected.
    # I governance projection cannot substitute for D completion.
    def test_T15(self):
        m = done()
        m.set_required_targets(["a", "b"])
        m.mark_target("a", "SUCCEEDED")
        m.mark_target("b", "ERASED")
        m.set_governance_projection(True)
        m.d_completion = False
        self.assertFalse(m.completion_projection_allowed())
        self.assertTrue(m.governance_projection_complete)
        self.assertFalse(m.d_completion)
        self.assertEqual(m.required_targets, {"a", "b"})

    # I-U011-T16: Forgotten is independent of cleanup completion.
    def test_T16(self):
        m = done()
        m.phase = Phase.CLEANUP
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertNotEqual(m.phase, Phase.COMPLETED)


class StorageFaults(unittest.TestCase):

    # STOR-01: Concurrent suppression cannot create a second commit.
    def test_STOR_01_concurrent_suppression_race(self):
        m = done()
        with self.assertRaises(ContractViolation):
            m.commit_suppression("duplicate")
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)

    # STOR-02: Replica lag cannot lower the committed Fence.
    def test_STOR_02_replica_lag_failover(self):
        m = done()
        with self.assertRaises(ContractViolation):
            m.promote_replica("lag", m.fence_generation - 1)
        self.assertFalse(m.read_allowed(None, False))

    # STOR-03: Old worker lease cannot commit after new attempt.
    def test_STOR_03_stale_worker_old_lease(self):
        m = done()
        old = m.start_attempt("old")
        new = m.start_attempt("new")
        with self.assertRaises(ContractViolation):
            m.commit_stage("old", old, "erase")
        m.commit_stage("new", new, "erase")

    # STOR-04: Outbox replay is idempotent.
    def test_STOR_04_duplicate_events_outbox_replay(self):
        m = done()
        self.assertFalse(m.replay_outbox("op"))
        self.assertTrue(m.replay_outbox("event"))
        self.assertFalse(m.replay_outbox("event"))

    # STOR-05: Timeout UNKNOWN requires reconciliation before retry.
    def test_STOR_05_timeout_retry_reconciliation(self):
        m = done()
        m.start_attempt("a1")
        self.assertEqual(m.reconcile("UNKNOWN"), Reconciliation.UNKNOWN)
        with self.assertRaises(ContractViolation):
            m.retry("a2")
        m.reconcile("NOT_APPLIED")
        m.retry("a2")

    # STOR-06: Restore isolation until Fence and later Forget reconciliation.
    def test_STOR_06_restore_isolation_reconciliation(self):
        m = done()
        m.begin_restore(0)
        self.assertFalse(m.restore_query_allowed())
        m.reconcile_restore(m.fence_generation, True)
        self.assertTrue(m.restore_query_allowed())

    # STOR-07: Missing, unauthenticated or empty backup manifest is UNKNOWN.
    def test_STOR_07_missing_manifest_unknown(self):
        m = done()
        m.set_backup_manifest(None)
        self.assertEqual(m.backup_coverage(), "UNKNOWN")
        m.set_backup_manifest({"authenticated": False, "copies": ["c1"]})
        self.assertEqual(m.backup_coverage(), "UNKNOWN")
        m.set_backup_manifest({"authenticated": True, "copies": []})
        self.assertEqual(m.backup_coverage(), "UNKNOWN")


if __name__ == "__main__":
    unittest.main(verbosity=2)