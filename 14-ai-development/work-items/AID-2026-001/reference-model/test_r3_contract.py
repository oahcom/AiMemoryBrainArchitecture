"""R3 contract-level tests.

Version: R3-FSTOR-20261118-02

Coverage:
- DFI-001..022
- I-U011-T01..T16
- STOR-01..07
- AUTH-01..14
- F-STOR-01/F-STOR-02 repair regressions
- F-OI-01 nonce projection recovery and replay rejection
- F-OI-02 independent idempotent retry audit

These tests exercise the in-memory reference model only.
DFI-013 deterministic sequential interleavings are not concurrency proof.
DFI-021 is an in-memory failure/rollback boundary, not physical durability.
Nonce projection reconstruction is an in-memory projection recovery check,
not a WAL, disk persistence, or physical crash-recovery proof.
"""

import threading
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

    def test_DFI_001(self):
        m = done()
        self.assertFalse(m.read_allowed(m.fence_generation))
        self.assertFalse(m.read_allowed(None))

    def test_DFI_002(self):
        m = done()
        m.phase = Phase.CLEANUP
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertNotEqual(m.phase, Phase.COMPLETED)

    def test_DFI_003(self):
        m = R3Model("m")
        with self.assertRaises(ContractViolation):
            m.forgotten_transition("Cancel")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

    def test_DFI_004(self):
        m = done()
        m.set_required_targets(["required", "unknown"])
        m.mark_target("required", "SUCCEEDED")
        m.mark_target("unknown", "UNKNOWN")
        self.assertFalse(m.domain_complete())
        self.assertIn("unknown", m.unknown_required_targets)

    def test_DFI_005(self):
        m = done()
        m.set_required_targets(["adapter"])
        m.mark_target("adapter", "ACKNOWLEDGED")
        self.assertFalse(m.domain_complete())

    def test_DFI_006(self):
        m = done()
        m.set_required_targets(["retained"])
        m.mark_target("retained", "POLICY_RETAINED")
        self.assertFalse(m.domain_complete())

    def test_DFI_007(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        first = m.commit_suppression(
            "op-1", "attempt-1", "key-1", "hash-A",
            auth=auth(nonce="nonce-first"),
        )

        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op-1", "attempt-2", "key-1", "hash-A",
                auth=auth(
                    signature_valid=False,
                    nonce="nonce-invalid",
                ),
            )

        m.phase = Phase.AUTHORIZED
        second = m.commit_suppression(
            "op-1", "attempt-2", "key-1", "hash-A",
            auth=auth(nonce="nonce-second"),
        )
        self.assertIs(first, second)
        self.assertIn("nonce-second", m.nonce_registry)

        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op-2", "attempt-3", "key-1", "hash-B",
                auth=auth(nonce="nonce-third"),
            )

    def test_DFI_008(self):
        m = done()
        a = m.start_attempt("a1")
        b = m.start_attempt("a2")
        with self.assertRaises(ContractViolation):
            m.commit_stage("a1", a, "cleanup")
        m.commit_stage("a2", b, "cleanup")

    def test_DFI_009(self):
        m = done()
        m.start_attempt("a1")
        self.assertEqual(m.reconcile("UNKNOWN"), Reconciliation.UNKNOWN)
        with self.assertRaises(ContractViolation):
            m.retry("a2")
        m.reconcile("APPLIED")
        m.retry("a2")

    def test_DFI_010(self):
        m = R3Model("m")
        with self.assertRaises(ContractViolation):
            m.authorize_and_suppress(
                auth(permission_epoch=6), 10, 7, "op"
            )
        self.assertEqual(m.phase, Phase.REQUESTED)
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

    def test_DFI_011(self):
        m = done()
        m.set_required_targets(["a"])
        m.mark_target("a", "SUCCEEDED")
        self.assertTrue(m.domain_complete())
        revision = m.inventory_revision
        m.set_required_targets(["a", "b"])
        self.assertGreater(m.inventory_revision, revision)
        self.assertFalse(m.domain_complete())

    def test_DFI_012(self):
        m = done()
        m.begin_restore(0)
        self.assertFalse(m.restore_query_allowed())
        with self.assertRaises(ContractViolation):
            m.reconcile_restore(0, False)
        m.reconcile_restore(m.fence_generation, True)
        self.assertTrue(m.restore_query_allowed())

    def test_DFI_013(self):
        """Sequential fence interleavings only; NOT a concurrency proof."""
        m = R3Model("m")

        old_worker_lease = m.start_attempt("worker-old")
        new_worker_lease = m.start_attempt("worker-new")
        with self.assertRaises(ContractViolation):
            m.commit_stage(
                "worker-old", old_worker_lease, "publish"
            )
        self.assertNotIn("STAGE:publish", m.audit)

        old_fence = m.fence_generation
        self.assertTrue(m.producer_admission(old_fence))

        m.authorize_and_suppress(auth(nonce="dfi013-nonce"), 10, 7, "op")

        with self.assertRaises(ContractViolation):
            m.register_dependency("late-producer", old_fence)
        self.assertNotIn("DEPENDENCY:late-producer", m.audit)

        with self.assertRaises(ContractViolation):
            m.recall_cache_fill(
                "delayed-key", "late-value", old_fence
            )
        self.assertNotIn("delayed-key", m.cache_entries)

        self.assertFalse(m.producer_admission(old_fence))
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertGreater(m.fence_generation, old_fence)

    def test_DFI_014(self):
        m = done()
        old = m.start_attempt("producer-old")
        new = m.start_attempt("producer-new")
        with self.assertRaises(ContractViolation):
            m.commit_stage("producer-old", old, "publish")
        m.commit_stage("producer-new", new, "publish")

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

    def test_DFI_016(self):
        m = done()
        with self.assertRaises(ContractViolation):
            m.rebuild_index(
                m.fence_generation - 1, {m.memory_id}
            )
        self.assertEqual(
            m.rebuild_index(m.fence_generation, {m.memory_id}), set()
        )

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

    def test_DFI_018(self):
        m = R3Model("m")
        m.context_remove()
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertIn("CONTEXT_REMOVE", m.audit)
        with self.assertRaises(ContractViolation):
            m.forgotten_transition("ContextRemove")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

    def test_DFI_019(self):
        m = done()
        m.set_required_targets(["adapter"])
        m.mark_target("adapter", "ACKNOWLEDGED")
        self.assertFalse(m.domain_complete())

    def test_DFI_020(self):
        m = R3Model("m")
        with self.assertRaises(ContractViolation):
            m.forgotten_transition("AgentTelemetry")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

    def test_DFI_021(self):
        """In-memory pre-publication abort; not WAL or crash durability."""
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

        recovered_record = m.atomic_commit
        self.assertIsNotNone(recovered_record)
        self.assertEqual(recovered_record, commit)
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)

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

    def test_T01(self):
        self._deny(issuer_known=False)

    def test_T02(self):
        for key in (
            "audience_matches", "operation_matches",
            "request_hash_matches", "purpose_matches", "scope_matches",
        ):
            with self.subTest(key=key):
                self._deny(**{key: False})

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

    def test_T04(self):
        self._deny(permission_epoch=6)

    def test_T05(self):
        m = R3Model("m")
        result = m.revoke_race(
            "REVOCATION_WON",
            auth=auth(nonce="revocation-wins-nonce"),
        )

        self.assertEqual(result, "REVOCATION_WON")

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

    def test_T06(self):
        m = R3Model("m")
        result = m.revoke_race(
            "COMMIT_WON",
            auth=auth(nonce="commit-wins-nonce"),
        )

        self.assertEqual(result, "COMMIT_WON")

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

    def test_T07(self):
        m = R3Model("m")
        result = m.revoke_race(
            "UNKNOWN",
            auth=auth(nonce="unknown-order-nonce"),
        )

        self.assertEqual(result, "UNKNOWN")

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

    def test_T08(self):
        self._deny(delegation_current=False)

    def test_T09(self):
        m = R3Model("m")
        m.legal_hold = True
        with self.assertRaises(ContractViolation):
            m.authorize_and_suppress(auth(), 10, 7, "op")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertEqual(m.fence_generation, 0)

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

    def test_T11(self):
        m = done()
        m.set_required_targets(["held"])
        m.mark_target("held", "POLICY_RETAINED")
        self.assertFalse(m.domain_complete())

    def test_T12(self):
        m = done()
        m.set_required_targets(["unknown"])
        m.mark_target("unknown", "UNKNOWN")
        self.assertFalse(m.domain_complete())

    def test_T13(self):
        m = done()
        m.set_required_targets(["a"])
        m.mark_target("a", "SUCCEEDED")
        self.assertTrue(m.domain_complete())
        m.set_required_targets(["a", "new"])
        self.assertFalse(m.domain_complete())

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

    def test_T16(self):
        m = done()
        m.phase = Phase.CLEANUP
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertNotEqual(m.phase, Phase.COMPLETED)


class StorageFaults(unittest.TestCase):

    def test_STOR_01_concurrent_suppression_race(self):
        """Real two-thread shared-boundary race, not sequential duplicate.

        Both callers cross a synchronization barrier before entering the
        same model commit boundary. They use distinct valid authorization
        nonces and the same idempotency identity. Exactly one authoritative
        commit must be published; the other caller must reuse that record.
        """
        m = R3Model("mem")
        m.phase = Phase.AUTHORIZED

        barrier = threading.Barrier(2)
        results = []
        errors = []
        result_lock = threading.Lock()

        def contender(index):
            try:
                supplied = auth(nonce=f"concurrent-nonce-{index}")
                barrier.wait(timeout=5)
                result = m.commit_suppression(
                    "concurrent-op",
                    attempt_id=f"attempt-{index}",
                    idempotency_key="concurrent-key",
                    request_hash="concurrent-hash",
                    auth=supplied,
                )
                with result_lock:
                    results.append((index, result, supplied.nonce))
            except Exception as exc:
                with result_lock:
                    errors.append(exc)

        workers = [
            threading.Thread(target=contender, args=(0,)),
            threading.Thread(target=contender, args=(1,)),
        ]

        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join(timeout=10)

        self.assertTrue(all(not worker.is_alive() for worker in workers))
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 2)

        authoritative = m.atomic_commit
        self.assertIsNotNone(authoritative)
        self.assertIs(results[0][1], authoritative)
        self.assertIs(results[1][1], authoritative)

        self.assertEqual(m.commit_counter, 1)
        self.assertEqual(m.fence_generation, 1)
        self.assertEqual(m.inventory_revision, 1)
        self.assertEqual(m.phase, Phase.SUPPRESSION_COMMITTED)
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)

        self.assertEqual(
            m.outbox,
            {"concurrent-op": "SUPPRESSION_COMMITTED"},
        )
        self.assertEqual(len(m.operation_registry), 1)
        self.assertEqual(
            m.operation_registry["concurrent-key"]["commit"],
            authoritative,
        )
        self.assertEqual(
            m.operation_registry["concurrent-key"]["request_hash"],
            "concurrent-hash",
        )

        self.assertEqual(
            m.nonce_registry,
            {"concurrent-nonce-0", "concurrent-nonce-1"},
        )
        self.assertEqual(
            sum(
                item == "SUPPRESSION_COMMITTED"
                for item in m.audit
            ),
            1,
        )
        self.assertEqual(
            sum(
                item == "IDEMPOTENT_COMMIT_REUSED"
                for item in m.audit
            ),
            1,
        )

        m._validate_atomic_commit(
            authoritative,
            published=True,
            expected_revision=authoritative.suppression_proof.inventory_revision,
            expected_fence=authoritative.fence_tombstone.fence_generation,
        )

    def test_STOR_02_replica_lag_failover(self):
        m = done()
        with self.assertRaises(ContractViolation):
            m.promote_replica("lag", m.fence_generation - 1)
        self.assertFalse(m.read_allowed(None, False))

    def test_STOR_03_stale_worker_old_lease(self):
        m = done()
        old = m.start_attempt("old")
        new = m.start_attempt("new")
        with self.assertRaises(ContractViolation):
            m.commit_stage("old", old, "erase")
        m.commit_stage("new", new, "erase")

    def test_STOR_04_duplicate_events_outbox_replay(self):
        m = done()
        self.assertFalse(m.replay_outbox("op"))
        self.assertTrue(m.replay_outbox("event"))
        self.assertFalse(m.replay_outbox("event"))

    def test_STOR_05_timeout_retry_reconciliation(self):
        m = done()
        m.start_attempt("a1")
        self.assertEqual(m.reconcile("UNKNOWN"), Reconciliation.UNKNOWN)
        with self.assertRaises(ContractViolation):
            m.retry("a2")
        m.reconcile("NOT_APPLIED")
        m.retry("a2")

    def test_STOR_06_restore_isolation_reconciliation(self):
        m = done()
        m.begin_restore(0)
        self.assertFalse(m.restore_query_allowed())
        m.reconcile_restore(m.fence_generation, True)
        self.assertTrue(m.restore_query_allowed())

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

    def test_AUTH_01_missing_authorization(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression("op")
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.fence_generation, 0)

    def test_AUTH_02_invalid_signature(self):
        self._direct_commit(
            auth(signature_valid=False, nonce="bad-signature")
        )

    def test_AUTH_03_unknown_issuer(self):
        self._direct_commit(
            auth(issuer_known=False, nonce="unknown-issuer")
        )

    def test_AUTH_04_expired_authorization(self):
        self._direct_commit(
            auth(expires_at=10, nonce="expired"),
            now=10,
        )

    def test_AUTH_05_stale_permission_epoch(self):
        self._direct_commit(
            auth(permission_epoch=6, nonce="stale-epoch")
        )

    def test_AUTH_06_phase_mutation_is_not_authority(self):
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression("phase-only")
        self.assertEqual(m.phase, Phase.AUTHORIZED)
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.fence_generation, 0)

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

    def test_AUTH_12_not_before(self):
        self._direct_commit(
            auth(not_before=11, nonce="not-yet-valid"),
            now=10,
        )

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

    def test_AUTH_14_stale_delegation(self):
        self._direct_commit(
            auth(
                delegation_current=False,
                nonce="stale-delegation",
            )
        )


class AtomicPublicationFaultInjection(unittest.TestCase):
    """F-STOR-01: every intermediate projection failure must roll back."""

    def _snapshot(self, m):
        return (
            m.atomic_commit,
            dict(m.atomic_tuple),
            m.fence_generation,
            m.inventory_revision,
            dict(m.outbox),
            dict(m.operation_registry),
            set(m.nonce_registry),
            m.phase,
            m.lifecycle,
            m.commit_counter,
        )

    def test_FSTOR_01_all_projection_faults_rollback(self):
        failure_points = (
            "atomic_tuple",
            "fence_generation",
            "inventory_revision",
            "outbox",
            "operation_registry",
            "nonce_registry",
            "phase",
            "lifecycle",
            "atomic_commit",
        )

        for point in failure_points:
            with self.subTest(failure_point=point):
                m = R3Model("m")
                m.phase = Phase.AUTHORIZED
                before = self._snapshot(m)

                with self.assertRaises(ContractViolation):
                    m.commit_suppression(
                        "op",
                        auth=auth(nonce=f"fault-{point}"),
                        fail_at=point,
                    )

                self.assertEqual(self._snapshot(m), before)
                self.assertEqual(m.audit, ["ATOMIC_TUPLE_ABORTED"])
                self.assertNotIn(f"fault-{point}", m.nonce_registry)

    def test_FSTOR_02_retry_after_each_injected_abort(self):
        for point in R3Model.COMMIT_PROJECTION_STEPS:
            with self.subTest(failure_point=point):
                m = R3Model("m")
                m.phase = Phase.AUTHORIZED

                with self.assertRaises(ContractViolation):
                    m.commit_suppression(
                        "op",
                        auth=auth(nonce=f"aborted-{point}"),
                        fail_at=point,
                    )

                commit = m.commit_suppression(
                    "op",
                    auth=auth(nonce=f"retry-{point}"),
                )

                self.assertIs(m.atomic_commit, commit)
                self.assertEqual(m.commit_counter, 1)
                self.assertEqual(m.fence_generation, 1)
                self.assertEqual(m.inventory_revision, 1)
                self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
                self.assertEqual(
                    m.outbox["op"], "SUPPRESSION_COMMITTED"
                )
                self.assertIn(f"retry-{point}", m.nonce_registry)
                self.assertNotIn(f"aborted-{point}", m.nonce_registry)

    def test_FSTOR_03_six_member_projection_exactness(self):
        m = R3Model("m")
        commit = m.authorize_and_suppress(
            auth(nonce="six-member-nonce"),
            10,
            7,
            "op",
        )

        self.assertEqual(set(m.atomic_tuple), set(R3Model.ATOMIC_FIELDS))

        for name in R3Model.ATOMIC_FIELDS:
            self.assertEqual(
                m.atomic_tuple[name],
                getattr(commit, name),
            )

        self.assertEqual(
            commit.lifecycle_event.operation_id,
            commit.idempotency_identity.operation_id,
        )
        self.assertEqual(
            commit.lifecycle_event.attempt_id,
            commit.idempotency_identity.attempt_id,
        )
        self.assertEqual(
            commit.authorization_reference.permission_epoch,
            m.permission_epoch,
        )
        self.assertEqual(
            commit.authorization_reference.nonce,
            "six-member-nonce",
        )
        self.assertEqual(
            commit.suppression_proof.inventory_revision,
            m.inventory_revision,
        )
        self.assertEqual(
            commit.fence_tombstone.fence_generation,
            m.fence_generation,
        )
        self.assertEqual(
            m.operation_registry[
                commit.idempotency_identity.idempotency_key
            ]["commit"],
            commit,
        )
        self.assertEqual(
            m.outbox[commit.lifecycle_event.operation_id],
            "SUPPRESSION_COMMITTED",
        )

    def test_FSTOR_04_corrupt_six_member_cross_reference_rejected(self):
        m = R3Model("m")
        commit = m.authorize_and_suppress(
            auth(nonce="cross-reference-nonce"),
            10,
            7,
            "op",
        )

        from dataclasses import replace

        invalid_commits = (
            replace(
                commit,
                authorization_reference=replace(
                    commit.authorization_reference,
                    permission_epoch=commit.authorization_reference.permission_epoch + 1,
                ),
            ),
            replace(
                commit,
                suppression_proof=replace(
                    commit.suppression_proof,
                    inventory_revision=commit.suppression_proof.inventory_revision + 1,
                ),
            ),
            replace(
                commit,
                fence_tombstone=replace(
                    commit.fence_tombstone,
                    fence_generation=commit.fence_tombstone.fence_generation + 1,
                ),
            ),
            replace(
                commit,
                lifecycle_event=replace(
                    commit.lifecycle_event,
                    attempt_id="unrelated-attempt",
                ),
            ),
            replace(
                commit,
                idempotency_identity=replace(
                    commit.idempotency_identity,
                    request_hash="unrelated-hash",
                ),
            ),
        )

        for invalid in invalid_commits:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ContractViolation):
                    m._validate_atomic_commit(
                        invalid,
                        published=True,
                        expected_revision=commit.suppression_proof.inventory_revision,
                        expected_fence=commit.fence_tombstone.fence_generation,
                    )

    def test_FSTOR_05_completion_projection_has_no_domain_side_effect(self):
        m = done()
        m.set_required_targets(["a"])
        m.mark_target("a", "SUCCEEDED")
        m.d_completion = True

        before = (
            m.d_completion,
            set(m.unknown_required_targets),
            dict(m.target_results),
            m.inventory_revision,
        )

        self.assertTrue(m.completion_projection_allowed())

        after = (
            m.d_completion,
            set(m.unknown_required_targets),
            dict(m.target_results),
            m.inventory_revision,
        )
        self.assertEqual(before, after)

    def test_FSTOR_06_nonce_projection_rebuild_and_replay_rejection(self):
        """F-OI-01: reconstruct nonce projection from authoritative records.

        This is an in-memory projection-recovery test. It does not claim
        persistence across process or machine crashes.
        """
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED

        first_nonce = "foi01-committed-nonce"
        retry_nonce = "foi01-retry-nonce"

        commit = m.commit_suppression(
            "foi01-op",
            "foi01-attempt-1",
            "foi01-key",
            "foi01-hash",
            auth=auth(nonce=first_nonce),
        )

        m.phase = Phase.AUTHORIZED
        reused = m.commit_suppression(
            "foi01-op",
            "foi01-attempt-2",
            "foi01-key",
            "foi01-hash",
            auth=auth(nonce=retry_nonce),
        )

        self.assertIs(reused, commit)
        self.assertIn(first_nonce, m.nonce_registry)
        self.assertIn(retry_nonce, m.nonce_registry)

        # Simulate loss/corruption of the derived in-memory projection.
        m.nonce_registry.clear()
        self.assertEqual(m.nonce_registry, set())

        rebuilt = m.recover_nonce_registry()
        self.assertEqual(rebuilt, {first_nonce, retry_nonce})
        self.assertEqual(m.nonce_registry, {first_nonce, retry_nonce})

        # A committed nonce remains consumed after projection reconstruction.
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "foi01-replay-op",
                "foi01-attempt-replay",
                "foi01-other-key",
                "foi01-other-hash",
                auth=auth(nonce=first_nonce),
            )

        self.assertEqual(m.atomic_commit, commit)
        self.assertEqual(m.fence_generation, 1)
        self.assertNotIn("foi01-replay-op", m.outbox)

    def test_FSTOR_07_idempotent_retry_has_complete_independent_audit(self):
        """F-OI-02: retry authorization is audited without a second commit."""
        m = R3Model("m")
        m.phase = Phase.AUTHORIZED

        original_operation_id = "foi02-original-operation"
        original_attempt_id = "foi02-original-attempt"
        idempotency_key = "foi02-idempotency-key"
        request_hash = "foi02-request-hash"
        original_nonce = "foi02-original-nonce"
        retry_nonce = "foi02-fresh-retry-nonce"

        first = m.commit_suppression(
            original_operation_id,
            original_attempt_id,
            idempotency_key,
            request_hash,
            auth=auth(nonce=original_nonce),
        )

        original_commit_id = first.commit_id
        original_fence = m.fence_generation
        original_revision = m.inventory_revision
        original_counter = m.commit_counter
        original_outbox = dict(m.outbox)
        original_audit_count = sum(
            entry == "SUPPRESSION_COMMITTED" for entry in m.audit
        )

        m.phase = Phase.AUTHORIZED
        second = m.commit_suppression(
            original_operation_id,
            "foi02-retry-attempt",
            idempotency_key,
            request_hash,
            auth=auth(nonce=retry_nonce),
        )

        self.assertIs(first, second)
        self.assertEqual(m.atomic_commit, first)
        self.assertEqual(m.fence_generation, original_fence)
        self.assertEqual(m.inventory_revision, original_revision)
        self.assertEqual(m.commit_counter, original_counter)
        self.assertEqual(m.outbox, original_outbox)

        self.assertEqual(
            sum(
                entry == "SUPPRESSION_COMMITTED"
                for entry in m.audit
            ),
            original_audit_count,
        )
        self.assertEqual(
            sum(
                entry == "IDEMPOTENT_COMMIT_REUSED"
                for entry in m.audit
            ),
            1,
        )

        self.assertEqual(len(m.retry_audit), 1)
        retry_record = m.retry_audit[0]

        self.assertEqual(
            retry_record["operation_id"],
            original_operation_id,
        )
        self.assertEqual(
            retry_record["commit_id"],
            original_commit_id,
        )
        self.assertTrue(retry_record["authorization_receipt"])
        self.assertNotEqual(
            retry_record["authorization_receipt"],
            first.authorization_reference,
        )
        self.assertEqual(retry_record["nonce"], retry_nonce)
        self.assertEqual(
            retry_record["permission_epoch"],
            first.authorization_reference.permission_epoch,
        )
        self.assertEqual(retry_record["request_hash"], request_hash)
        self.assertEqual(
            retry_record["retry_result"],
            "REUSED_EXISTING_COMMIT",
        )

        self.assertIn(original_nonce, m.nonce_registry)
        self.assertIn(retry_nonce, m.nonce_registry)

        # The retry is separately auditable but does not emit another
        # authoritative lifecycle event or create another commit.
        self.assertEqual(len(m.operation_registry), 1)
        self.assertEqual(
            m.operation_registry[idempotency_key]["commit"],
            first,
        )
        self.assertEqual(
            m.outbox[original_operation_id],
            "SUPPRESSION_COMMITTED",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)


# Static test-method inventory:
#   DFI:                         22
#   OwnerIU011 (T01..T16):       16
#   StorageFaults (STOR-01..07):  7
#   AuthorizationCommitEntry:   14
#   AtomicPublicationFaultInjection:
#                                7 (FSTOR-01..07)
#   Total:                       66 test methods
#
# Newly added tests:
#   - test_FSTOR_06_nonce_projection_rebuild_and_replay_rejection
#       F-OI-01: reconstruct nonce_registry from authoritative commit and
#       retry audit records, then reject replay of a consumed nonce.
#   - test_FSTOR_07_idempotent_retry_has_complete_independent_audit
#       F-OI-02: assert independent retry audit fields and ensure no second
#       commit, fence advance, revision advance, or duplicate committed event.
#
# Execution status:
#   NOT RUN in this delivery.
#   No test-pass claim is made. Run against the exact delivered
#   r3_contract_model.py revision before treating this suite as verified.
#   These tests cover an in-memory reference model only; they do not prove
#   WAL durability, physical crash recovery, or distributed linearizability.
