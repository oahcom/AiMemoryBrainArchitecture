
"""R3 contract-level tests.

DFI-001..022, I-U011-T01..T16, STOR-01..07,
plus authorization-entry rejection tests.
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
        nonce="auth-nonce-default",
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

    # DFI-007: Same idempotency Key/Hash reuses operation only after
    # independent validation of the new authorization.
    def test_DFI_007(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        first = m.commit_suppression(
            "op-1", "attempt-1", "key-1", "hash-A",
            auth=auth(nonce="nonce-first"),
        )

        # Same Key/Hash does not bypass invalid authorization.
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op-1", "attempt-2", "key-1", "hash-A",
                auth=auth(
                    signature_valid=False,
                    nonce="nonce-invalid",
                ),
            )

        # Same Key/Hash with a fresh valid authorization reuses the commit.
        m.phase = Phase.AUTHORIZED
        second = m.commit_suppression(
            "op-1", "attempt-2", "key-1", "hash-A",
            auth=auth(nonce="nonce-second"),
        )
        self.assertIs(first, second)
        self.assertIn("nonce-second", m.nonce_registry)

        # Same Key but different Hash is rejected.
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op-2", "attempt-3", "key-1", "hash-B",
                auth=auth(nonce="nonce-third"),
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
        self.assertEqual(m.phase, Phase.REQUESTED)
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

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

    # DFI-013: Three independent stale-publication races.
    #
    # Evidence boundary: these are deterministic sequential interleavings.
    # They demonstrate the rejection conditions for old Fence, old Worker,
    # and delayed Cache Fill. They are NOT proof of true concurrent
    # execution or concurrent linearizability.
    def test_DFI_013(self):
        m = R3Model("m")

        # Race A: worker captures an old lease; a newer worker supersedes it.
        old_worker_lease = m.start_attempt("worker-old")
        new_worker_lease = m.start_attempt("worker-new")
        with self.assertRaises(ContractViolation):
            m.commit_stage(
                "worker-old", old_worker_lease, "publish"
            )
        self.assertNotIn("STAGE:publish", m.audit)

        # Capture the pre-Forget Fence for producer and cache operations.
        old_fence = m.fence_generation
        self.assertTrue(m.producer_admission(old_fence))

        # The canonical suppression commit advances Fence and Forget state.
        m.authorize_and_suppress(auth(nonce="dfi013-nonce"), 10, 7, "op")

        # Race B: producer with an old Fence cannot register a dependency.
        with self.assertRaises(ContractViolation):
            m.register_dependency("late-producer", old_fence)
        self.assertNotIn("DEPENDENCY:late-producer", m.audit)

        # Race C: delayed Cache Fill must recheck Fence at publication.
        with self.assertRaises(ContractViolation):
            m.recall_cache_fill(
                "delayed-key", "late-value", old_fence
            )
        self.assertNotIn("delayed-key", m.cache_entries)

        self.assertFalse(m.producer_admission(old_fence))
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertGreater(m.fence_generation, old_fence)

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

    # I-U011-T03: A successfully consumed Nonce cannot be replayed.
    # Expiry and not-before boundaries are also checked.
    def test_T03(self):
        m = R3Model("m")
        original = auth(nonce="real-authorization-nonce")
        first = m.authorize_and_suppress(
            original, 10, 7, "op-first"
        )

        self.assertIsNotNone(first)
        self.assertIn("real-authorization-nonce", m.nonce_registry)
        self.assertEqual(
            first.authorization_reference.nonce,
            "real-authorization-nonce",
        )

        # Replay the same Authorization Nonce through the actual commit API.
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op-replay",
                "attempt-replay",
                "key-replay",
                "hash-replay",
                auth=original,
            )

        self.assertEqual(m.atomic_commit, first)
        self.assertEqual(m.fence_generation, 1)
        self.assertNotIn("op-replay", m.outbox)

        self._deny(expires_at=10)
        self._deny(not_before=11)

    # I-U011-T04: Stale PermissionEpoch is denied.
    def test_T04(self):
        self._deny(permission_epoch=6)

    # I-U011-T05: Revocation wins when it precedes commit.
    def test_T05(self):
        m = R3Model("m")
        result = m.revoke_race(
            "REVOCATION_WON",
            auth=auth(nonce="revocation-wins-nonce"),
        )

        self.assertEqual(result, "REVOCATION_WON")

        # Assert actual state and side effects, not just the result label.
        self.assertEqual(m.permission_epoch, 8)
        self.assertEqual(m.revocation_state, "REVOKED")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.atomic_tuple, {})
        self.assertEqual(m.fence_generation, 0)
        self.assertEqual(m.inventory_revision, 0)
        self.assertEqual(m.outbox, {})
        self.assertEqual(m.operation_registry, {})
        self.assertNotIn("revocation-wins-nonce", m.nonce_registry)
        self.assertIn("AUTHORIZATION_REVOKED", m.audit)

    # I-U011-T06: Commit wins when commit precedes revocation.
    def test_T06(self):
        m = R3Model("m")
        result = m.revoke_race(
            "COMMIT_WON",
            auth=auth(nonce="commit-wins-nonce"),
        )

        self.assertEqual(result, "COMMIT_WON")

        # Commit's actual effects remain committed after later revocation.
        self.assertEqual(m.permission_epoch, 8)
        self.assertEqual(m.revocation_state, "REVOKED")
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertEqual(m.phase, Phase.SUPPRESSION_COMMITTED)
        self.assertIsNotNone(m.atomic_commit)
        self.assertEqual(m.fence_generation, 1)
        self.assertEqual(m.inventory_revision, 1)
        self.assertEqual(
            m.outbox["race-op"], "SUPPRESSION_COMMITTED"
        )
        self.assertIn("race-op", m.operation_registry)
        self.assertIn("commit-wins-nonce", m.nonce_registry)
        self.assertIn("AUTHORIZATION_REVOKED", m.audit)

    # I-U011-T07: Unprovable ordering/currentness is UNKNOWN.
    def test_T07(self):
        m = R3Model("m")
        result = m.revoke_race(
            "UNKNOWN",
            auth=auth(nonce="unknown-order-nonce"),
        )

        self.assertEqual(result, "UNKNOWN")

        # UNKNOWN is an explicit fail-closed state, not a successful commit.
        self.assertEqual(m.revocation_state, "UNKNOWN")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertEqual(m.phase, Phase.AUTHORIZED)
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.atomic_tuple, {})
        self.assertEqual(m.fence_generation, 0)
        self.assertEqual(m.inventory_revision, 0)
        self.assertEqual(m.outbox, {})
        self.assertEqual(m.operation_registry, {})
        self.assertNotIn("unknown-order-nonce", m.nonce_registry)
        self.assertIn(
            "AUTHORIZATION_CURRENTNESS_UNKNOWN", m.audit
        )

        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "unknown-followup",
                auth=auth(nonce="unknown-followup-nonce"),
            )

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


class AuthorizationCommitEntry(unittest.TestCase):

    def _direct_commit(self, authorization, **kwargs):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "direct-op", auth=authorization, **kwargs
            )
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertEqual(m.fence_generation, 0)
        return m

    # AUTH-01: Direct commit without Authorization is rejected.
    def test_AUTH_01_missing_authorization(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression("op")
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.fence_generation, 0)

    # AUTH-02: Invalid signature is rejected at commit entry.
    def test_AUTH_02_invalid_signature(self):
        self._direct_commit(
            auth(signature_valid=False, nonce="bad-signature")
        )

    # AUTH-03: Unknown issuer is rejected at commit entry.
    def test_AUTH_03_unknown_issuer(self):
        self._direct_commit(
            auth(issuer_known=False, nonce="unknown-issuer")
        )

    # AUTH-04: Expired authorization is rejected at commit entry.
    def test_AUTH_04_expired_authorization(self):
        self._direct_commit(
            auth(expires_at=10, nonce="expired"),
            now=10,
        )

    # AUTH-05: Stale PermissionEpoch is rejected at commit entry.
    def test_AUTH_05_stale_permission_epoch(self):
        self._direct_commit(
            auth(permission_epoch=6, nonce="stale-epoch")
        )

    # AUTH-06: Changing phase alone cannot grant commit authority.
    def test_AUTH_06_phase_mutation_is_not_authority(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression("phase-only")
        self.assertEqual(m.phase, Phase.AUTHORIZED)
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.fence_generation, 0)

    # AUTH-07: AuthorizationReference carries the actual authorization nonce.
    def test_AUTH_07_real_nonce_binding(self):
        m = R3Model("m")
        supplied = auth(nonce="issuer-generated-real-nonce")
        commit = m.authorize_and_suppress(supplied, 10, 7, "op")
        self.assertEqual(
            commit.authorization_reference.nonce,
            "issuer-generated-real-nonce",
        )
        self.assertIn("issuer-generated-real-nonce", m.nonce_registry)
        self.assertNotIn(
            f"nonce-{commit.commit_id}", m.nonce_registry
        )

    # AUTH-08: Aborted commit does not consume nonce; successful retry does.
    def test_AUTH_08_abort_does_not_consume_nonce(self):
        m = R3Model("m")
        supplied = auth(nonce="retry-after-abort")
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op", auth=supplied, fail_before_commit=True
            )
        self.assertNotIn(supplied.nonce, m.nonce_registry)
        self.assertIsNone(m.atomic_commit)

        commit = m.commit_suppression("op", auth=supplied)
        self.assertIsNotNone(commit)
        self.assertIn(supplied.nonce, m.nonce_registry)

    # AUTH-09: A consumed nonce cannot authorize a different operation.
    def test_AUTH_09_nonce_replay_different_key(self):
        m = R3Model("m")
        supplied = auth(nonce="one-time-nonce")
        m.authorize_and_suppress(supplied, 10, 7, "first-op")
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "second-op",
                idempotency_key="second-key",
                auth=supplied,
            )
        self.assertNotIn("second-op", m.outbox)
        self.assertEqual(m.fence_generation, 1)

    # AUTH-10: Fresh valid nonce permits same Key/Hash idempotent reuse.
    def test_AUTH_10_fresh_nonce_idempotent_reuse(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        first = m.commit_suppression(
            "op", "a1", "same-key", "same-hash",
            auth=auth(nonce="first-valid-nonce"),
        )
        m.phase = Phase.AUTHORIZED
        second = m.commit_suppression(
            "op", "a2", "same-key", "same-hash",
            auth=auth(nonce="fresh-valid-nonce"),
        )
        self.assertIs(first, second)
        self.assertIn("fresh-valid-nonce", m.nonce_registry)
        self.assertEqual(m.fence_generation, 1)

    # AUTH-11: Invalid authorization cannot use an existing idempotency result.
    def test_AUTH_11_invalid_auth_idempotent_bypass(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        first = m.commit_suppression(
            "op", "a1", "key", "hash",
            auth=auth(nonce="initial-valid"),
        )
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op", "a2", "key", "hash",
                auth=auth(
                    issuer_known=False,
                    nonce="invalid-retry",
                ),
            )
        self.assertIs(m.atomic_commit, first)
        self.assertNotIn("invalid-retry", m.nonce_registry)

    # AUTH-12: Not-before boundary is checked at commit entry.
    def test_AUTH_12_not_before(self):
        self._direct_commit(
            auth(not_before=11, nonce="not-yet-valid"),
            now=10,
        )

    # AUTH-13: Caller cannot pass an obsolete epoch to bypass model state.
    def test_AUTH_13_caller_epoch_spoof(self):
        m = R3Model("m")
        m.permission_epoch = 8
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op",
                auth=auth(permission_epoch=7, nonce="epoch-spoof"),
                current_epoch=7,
            )
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.fence_generation, 0)

    # AUTH-14: Stale delegation is rejected at the commit boundary.
    def test_AUTH_14_stale_delegation(self):
        self._direct_commit(
            auth(
                delegation_current=False,
                nonce="stale-delegation",
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
