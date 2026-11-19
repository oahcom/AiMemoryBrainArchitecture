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
    ReceiptCredential,
    Reconciliation,
    R3Model,
    RejectingReceiptVerifier,
    TrustAllReceiptVerifier,
    EXPECTED_RECEIPT_AUDIENCE,
    EXPECTED_RECEIPT_ISSUER,
    EXPECTED_RECEIPT_PURPOSE,
)


def receipt_credential(
    operation_id="",
    request_hash="",
    nonce="auth-nonce-default",
    receipt_id=None,
    **overrides,
):
    if receipt_id is None:
        receipt_id = "receipt-%s" % nonce
    values = dict(
        receipt_id=receipt_id,
        issuer=EXPECTED_RECEIPT_ISSUER,
        audience=EXPECTED_RECEIPT_AUDIENCE,
        operation=operation_id,
        request_hash=request_hash,
        purpose=EXPECTED_RECEIPT_PURPOSE,
        scope=frozenset({"suppression:commit"}),
        permission_epoch=7,
        nonce=nonce,
        not_before=0,
        expires_at=100,
        signature="test-signature-%s" % receipt_id,
    )
    values.update(overrides)
    return ReceiptCredential(**values)


def authorized_attempt(operation_id, request_hash, nonce, receipt_id, **credential_overrides):
    cred = receipt_credential(
        operation_id=operation_id,
        request_hash=request_hash,
        nonce=nonce,
        receipt_id=receipt_id,
        **credential_overrides,
    )
    return Authorization(
        permission_epoch=cred.permission_epoch,
        nonce=nonce,
        receipt=cred,
    )


def auth(**kw):
    nonce = kw.pop("nonce", "auth-nonce-default")
    receipt_id = kw.pop("receipt_id", None)
    # F-OI-04 strict binding: the credential must name its operation and
    # request hash. Defaults mirror commit_suppression()'s own defaults so
    # a test only has to pass them when it commits under another identity.
    operation_id = kw.pop("operation_id", "op")
    request_hash = kw.pop("request_hash", "default-hash")
    receipt_overrides = {}
    for k in list(kw):
        if k in ("issuer", "audience", "purpose", "scope",
                 "permission_epoch", "not_before", "expires_at", "signature",
                 "operation", "request_hash"):
            receipt_overrides[k] = kw.pop(k)
    cred = receipt_credential(
        operation_id=operation_id,
        request_hash=request_hash,
        nonce=nonce,
        receipt_id=receipt_id,
        **receipt_overrides,
    )
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
        nonce=nonce,
        receipt=cred,
    )
    values.update(kw)
    return Authorization(**values)


def done():
    model = R3Model("mem", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED
        first = m.commit_suppression(
            "op-1", "attempt-1", "key-1", "hash-A",
            auth=auth(nonce="nonce-first", operation_id="op-1",
                      request_hash="hash-A"),
        )

        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op-1", "attempt-2", "key-1", "hash-A",
                auth=auth(
                    signature_valid=False,
                    nonce="nonce-invalid",
                    operation_id="op-1",
                    request_hash="hash-A",
                ),
            )

        m.phase = Phase.AUTHORIZED
        second = m.commit_suppression(
            "op-1", "attempt-2", "key-1", "hash-A",
            auth=auth(nonce="nonce-second", operation_id="op-1",
                      request_hash="hash-A"),
        )
        self.assertIs(first, second)
        self.assertIn("nonce-second", m.nonce_registry)

        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "op-2", "attempt-3", "key-1", "hash-B",
                auth=auth(nonce="nonce-third", operation_id="op-2",
                          request_hash="hash-B"),
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())

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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        with self.assertRaises(ContractViolation):
            m.forgotten_transition("AgentTelemetry")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)

    def test_DFI_021(self):
        """In-memory pre-publication abort; not WAL or crash durability."""
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        original = auth(nonce="real-authorization-nonce",
                        operation_id="op-first")
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
        with self.assertRaises(ContractViolation) as ctx:
            m.commit_suppression(
                "op-first",
                "attempt-replay",
                "key-replay",
                "default-hash",
                auth=original,
            )
        self.assertIn("replay", str(ctx.exception))

        self.assertEqual(m.atomic_commit, first)
        self.assertEqual(m.fence_generation, 1)
        self.assertNotIn("op-replay", m.outbox)

        self._deny(expires_at=10)
        self._deny(not_before=11)

    def test_T04(self):
        self._deny(permission_epoch=6)

    def test_T05(self):
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        result = m.revoke_race(
            "REVOCATION_WON",
            auth=auth(nonce="revocation-wins-nonce", operation_id="race-op"),
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        result = m.revoke_race(
            "COMMIT_WON",
            auth=auth(nonce="commit-wins-nonce", operation_id="race-op"),
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.legal_hold = True
        with self.assertRaises(ContractViolation):
            m.authorize_and_suppress(auth(), 10, 7, "op")
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertEqual(m.fence_generation, 0)

    def test_T10(self):
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("mem", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED

        barrier = threading.Barrier(2)
        results = []
        errors = []
        result_lock = threading.Lock()

        def contender(index):
            try:
                supplied = auth(nonce=f"concurrent-nonce-{index}",
                                operation_id="concurrent-op",
                                request_hash="concurrent-hash")
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation):
            m.commit_suppression("phase-only")
        self.assertEqual(m.phase, Phase.AUTHORIZED)
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.fence_generation, 0)

    def test_AUTH_07_real_nonce_binding(self):
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        supplied = auth(nonce="one-time-nonce", operation_id="first-op")
        m.authorize_and_suppress(supplied, 10, 7, "first-op")
        m.phase = Phase.AUTHORIZED
        with self.assertRaises(ContractViolation) as ctx:
            m.commit_suppression(
                "first-op",
                idempotency_key="second-key",
                auth=supplied,
            )
        # Same credential, same binding: the rejection is nonce replay.
        self.assertIn("replay", str(ctx.exception))
        self.assertEqual(m.fence_generation, 1)

    def test_AUTH_10_fresh_nonce_idempotent_reuse(self):
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED
        first = m.commit_suppression(
            "op", "a1", "same-key", "same-hash",
            auth=auth(nonce="first-valid-nonce", request_hash="same-hash"),
        )
        m.phase = Phase.AUTHORIZED
        second = m.commit_suppression(
            "op", "a2", "same-key", "same-hash",
            auth=auth(nonce="fresh-valid-nonce", request_hash="same-hash"),
        )
        self.assertIs(first, second)
        self.assertIn("fresh-valid-nonce", m.nonce_registry)
        self.assertEqual(m.fence_generation, 1)

    def test_AUTH_11_invalid_auth_idempotent_bypass(self):
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED
        first = m.commit_suppression(
            "op", "a1", "key", "hash",
            auth=auth(nonce="initial-valid", request_hash="hash"),
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
                m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
                m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED

        first_nonce = "foi01-committed-nonce"
        retry_nonce = "foi01-retry-nonce"

        commit = m.commit_suppression(
            "foi01-op",
            "foi01-attempt-1",
            "foi01-key",
            "foi01-hash",
            auth=auth(nonce=first_nonce, operation_id="foi01-op",
                      request_hash="foi01-hash"),
        )

        m.phase = Phase.AUTHORIZED
        reused = m.commit_suppression(
            "foi01-op",
            "foi01-attempt-2",
            "foi01-key",
            "foi01-hash",
            auth=auth(nonce=retry_nonce, operation_id="foi01-op",
                      request_hash="foi01-hash"),
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
                auth=auth(nonce=first_nonce,
                          operation_id="foi01-replay-op",
                          request_hash="foi01-other-hash"),
            )

        self.assertEqual(m.atomic_commit, commit)
        self.assertEqual(m.fence_generation, 1)
        self.assertNotIn("foi01-replay-op", m.outbox)

    def test_FSTOR_07_idempotent_retry_has_complete_independent_audit(self):
        """F-OI-02: retry authorization is audited without a second commit."""
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
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
            auth=auth(nonce=original_nonce, operation_id=original_operation_id,
                      request_hash=request_hash),
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
            auth=auth(nonce=retry_nonce, operation_id=original_operation_id,
                      request_hash=request_hash),
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
            first.authorization_reference.receipt_id,
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

    def test_FSTOR_08_lifecycle_terminal_invariant_survives_idempotent_retry(self):
        """F-OI-03: idempotent retry must never restore Forgotten lifecycle."""
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED

        operation_id = "foi03-original-operation"
        attempt_id = "foi03-original-attempt"
        idempotency_key = "foi03-idempotency-key"
        request_hash = "foi03-request-hash"

        first = m.commit_suppression(
            operation_id,
            attempt_id,
            idempotency_key,
            request_hash,
            auth=auth(nonce="foi03-original-nonce", operation_id=operation_id,
                      request_hash=request_hash),
        )

        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertEqual(m.phase, Phase.SUPPRESSION_COMMITTED)

        original_lifecycle = m.lifecycle
        original_phase = m.phase
        original_retry_audit = list(m.retry_audit)
        original_nonce_registry = set(m.nonce_registry)
        original_fence = m.fence_generation
        original_counter = m.commit_counter
        original_outbox = dict(m.outbox)
        original_commit = m.atomic_commit

        # Reproduce the reported regression: lifecycle and phase both regress.
        m.lifecycle = Lifecycle.ACTIVE
        m.phase = Phase.AUTHORIZED

        retry_authorization = auth(
            nonce="foi03-fresh-retry-nonce",
            operation_id=operation_id,
            request_hash=request_hash,
        )

        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                operation_id,
                "foi03-retry-attempt",
                idempotency_key,
                request_hash,
                auth=retry_authorization,
            )

        # Rejection must not consume the retry authorization or mutate commit state.
        self.assertEqual(m.retry_audit, original_retry_audit)
        self.assertEqual(m.nonce_registry, original_nonce_registry)
        self.assertNotIn(
            retry_authorization.nonce,
            m.nonce_registry,
        )
        self.assertEqual(m.fence_generation, original_fence)
        self.assertEqual(m.commit_counter, original_counter)
        self.assertEqual(m.outbox, original_outbox)
        self.assertIs(m.atomic_commit, original_commit)

        # Restore the valid committed state and retry with the same,
        # previously rejected authorization.
        m.lifecycle = original_lifecycle
        m.phase = original_phase

        reused = m.commit_suppression(
            operation_id,
            "foi03-retry-attempt",
            idempotency_key,
            request_hash,
            auth=retry_authorization,
        )

        self.assertIs(reused, first)
        self.assertIs(m.atomic_commit, first)
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)
        self.assertEqual(m.phase, Phase.SUPPRESSION_COMMITTED)
        self.assertEqual(len(m.retry_audit), len(original_retry_audit) + 1)
        self.assertIn(
            retry_authorization.nonce,
            m.nonce_registry,
        )
        self.assertEqual(m.fence_generation, original_fence)
        self.assertEqual(m.commit_counter, original_counter)
        self.assertEqual(m.outbox, original_outbox)

    def test_FSTOR_09_authorization_receipt_is_required_and_single_use(self):
        """F-OI-04: missing or reused receipts are rejected; fresh retry receipt is audited."""
        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED

        operation_id = "foi04-original-operation"
        attempt_id = "foi04-original-attempt"
        idempotency_key = "foi04-idempotency-key"
        request_hash = "foi04-request-hash"

        original_authorization = auth(
            nonce="foi04-original-nonce",
            receipt_id="foi04-original-receipt",
            operation_id=operation_id,
            request_hash=request_hash,
        )

        first = m.commit_suppression(
            operation_id,
            attempt_id,
            idempotency_key,
            request_hash,
            auth=original_authorization,
        )

        original_receipt = first.authorization_reference.receipt_id
        self.assertEqual(original_receipt, original_authorization.receipt.receipt_id)

        original_retry_audit = list(m.retry_audit)
        original_nonce_registry = set(m.nonce_registry)
        original_fence = m.fence_generation
        original_counter = m.commit_counter
        original_outbox = dict(m.outbox)
        original_commit = m.atomic_commit

        # Missing receipt must be rejected without consuming its nonce.
        missing_receipt_authorization = auth(
            nonce="foi04-missing-receipt-nonce",
            receipt_id="",
            operation_id=operation_id,
            request_hash=request_hash,
        )

        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                operation_id,
                "foi04-missing-receipt-attempt",
                idempotency_key,
                request_hash,
                auth=missing_receipt_authorization,
            )

        self.assertEqual(m.retry_audit, original_retry_audit)
        self.assertEqual(m.nonce_registry, original_nonce_registry)
        self.assertNotIn(
            missing_receipt_authorization.nonce,
            m.nonce_registry,
        )
        self.assertEqual(m.fence_generation, original_fence)
        self.assertEqual(m.commit_counter, original_counter)
        self.assertEqual(m.outbox, original_outbox)
        self.assertIs(m.atomic_commit, original_commit)

        # A fresh nonce cannot make an already-consumed receipt reusable.
        reused_receipt_authorization = auth(
            nonce="foi04-reused-receipt-nonce",
            receipt_id=original_receipt,
            operation_id=operation_id,
            request_hash=request_hash,
        )

        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                operation_id,
                "foi04-reused-receipt-attempt",
                idempotency_key,
                request_hash,
                auth=reused_receipt_authorization,
            )

        self.assertEqual(m.retry_audit, original_retry_audit)
        self.assertEqual(m.nonce_registry, original_nonce_registry)
        self.assertNotIn(
            reused_receipt_authorization.nonce,
            m.nonce_registry,
        )
        self.assertEqual(m.fence_generation, original_fence)
        self.assertEqual(m.commit_counter, original_counter)
        self.assertEqual(m.outbox, original_outbox)
        self.assertIs(m.atomic_commit, original_commit)

        # A fresh nonce and fresh receipt permit legitimate idempotent reuse.
        retry_authorization = auth(
            nonce="foi04-fresh-retry-nonce",
            receipt_id="foi04-fresh-retry-receipt",
            operation_id=operation_id,
            request_hash=request_hash,
        )

        reused = m.commit_suppression(
            operation_id,
            "foi04-valid-retry-attempt",
            idempotency_key,
            request_hash,
            auth=retry_authorization,
        )

        self.assertIs(reused, first)
        self.assertIs(m.atomic_commit, first)
        self.assertEqual(len(m.retry_audit), 1)

        retry_record = m.retry_audit[0]
        self.assertEqual(
            retry_record["authorization_receipt"],
            retry_authorization.receipt.receipt_id,
        )
        self.assertNotEqual(
            retry_record["authorization_receipt"],
            original_receipt,
        )
        self.assertEqual(
            retry_record["nonce"],
            retry_authorization.nonce,
        )

        self.assertIn(retry_authorization.nonce, m.nonce_registry)
        self.assertEqual(m.fence_generation, original_fence)
        self.assertEqual(m.commit_counter, original_counter)
        self.assertEqual(m.outbox, original_outbox)
        self.assertEqual(m.atomic_commit, first)

    def test_FSTOR_10_cleanup_allows_existing_retry_but_rejects_first_commit(self):
        """F-D-NEW-01: CLEANUP permits a fresh-authorized retry only."""
        operation_id = "foi-cleanup-operation"
        attempt_id = "foi-cleanup-first-attempt"
        idempotency_key = "foi-cleanup-idempotency-key"
        request_hash = "foi-cleanup-request-hash"

        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED

        first = m.commit_suppression(
            operation_id,
            attempt_id,
            idempotency_key,
            request_hash,
            auth=auth(nonce="foi-cleanup-first-nonce", operation_id=operation_id,
                      request_hash=request_hash),
        )

        original_fence = m.fence_generation
        original_counter = m.commit_counter
        original_outbox = dict(m.outbox)
        original_commit = m.atomic_commit

        self.assertIs(first, original_commit)
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)

        m.phase = Phase.CLEANUP

        reused = m.commit_suppression(
            operation_id,
            "foi-cleanup-retry-attempt",
            idempotency_key,
            request_hash,
            auth=auth(nonce="foi-cleanup-retry-nonce", operation_id=operation_id,
                      request_hash=request_hash),
        )

        self.assertIs(reused, first)
        self.assertIs(m.atomic_commit, first)
        self.assertEqual(m.phase, Phase.CLEANUP)
        self.assertEqual(m.lifecycle, Lifecycle.FORGOTTEN)

        self.assertEqual(len(m.retry_audit), 1)
        retry_record = m.retry_audit[0]
        self.assertEqual(
            retry_record["retry_result"],
            "REUSED_EXISTING_COMMIT",
        )
        self.assertNotEqual(
            retry_record["authorization_receipt"],
            first.authorization_reference.receipt_id,
        )

        self.assertEqual(m.fence_generation, original_fence)
        self.assertEqual(m.commit_counter, original_counter)
        self.assertEqual(m.outbox, original_outbox)

        self.assertEqual(
            sum(x == "SUPPRESSION_COMMITTED" for x in m.audit), 1,
        )
        self.assertEqual(
            sum(x == "IDEMPOTENT_COMMIT_REUSED" for x in m.audit), 1,
        )

        fresh = R3Model("fresh-memory",
                         receipt_verifier=TrustAllReceiptVerifier())
        fresh.phase = Phase.CLEANUP

        before_commit = fresh.atomic_commit
        before_fence = fresh.fence_generation

        with self.assertRaises(ContractViolation):
            fresh.commit_suppression(
                "foi-cleanup-new-operation",
                "foi-cleanup-new-attempt",
                "foi-cleanup-new-key",
                "foi-cleanup-new-hash",
                auth=auth(nonce="foi-cleanup-new-nonce",
                          operation_id="foi-cleanup-new-operation",
                          request_hash="foi-cleanup-new-hash"),
            )

        self.assertIs(fresh.atomic_commit, before_commit)
        self.assertEqual(fresh.fence_generation, before_fence)

    def test_FSTOR_11_receipt_credential_verification_and_retry_binding(self):
        """F-OI-04: reject forged/mismatched credentials and bind valid retry."""
        operation_id = "foi-cred-operation"
        idempotency_key = "foi-cred-key"
        request_hash = "foi-cred-hash"

        m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
        m.phase = Phase.AUTHORIZED

        first = m.commit_suppression(
            operation_id,
            "foi-cred-first-attempt",
            idempotency_key,
            request_hash,
            auth=auth(nonce="foi-cred-original-nonce", operation_id=operation_id,
                      request_hash=request_hash),
        )

        original_commit = m.atomic_commit
        original_fence = m.fence_generation
        original_counter = m.commit_counter
        original_outbox = dict(m.outbox)
        original_nonce_registry = set(m.nonce_registry)
        original_retry_audit = list(m.retry_audit)

        def assert_no_retry_side_effect(auth_to_try, verifier=None):
            prev = m.receipt_verifier
            if verifier is not None:
                m.receipt_verifier = verifier
            try:
                with self.assertRaises(ContractViolation):
                    m.commit_suppression(
                        operation_id,
                        "foi-cred-invalid-retry",
                        idempotency_key,
                        request_hash,
                        auth=auth_to_try,
                    )
            finally:
                m.receipt_verifier = prev
            self.assertIs(m.atomic_commit, original_commit)
            self.assertEqual(m.fence_generation, original_fence)
            self.assertEqual(m.commit_counter, original_counter)
            self.assertEqual(m.outbox, original_outbox)
            self.assertEqual(m.nonce_registry, original_nonce_registry)
            self.assertEqual(m.retry_audit, original_retry_audit)

        # Context construction rule (author spec): start from the correct
        # operation_id / request_hash, then override exactly one credential
        # field per case, so a rejection proves that field's binding.
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-forged", operation_id=operation_id,
                 request_hash=request_hash),
            verifier=RejectingReceiptVerifier(),
        )
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-wrong-issuer", operation_id=operation_id,
                 request_hash=request_hash,
                 issuer="untrusted-issuer"),
        )
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-wrong-audience", operation_id=operation_id,
                 request_hash=request_hash,
                 audience="other-service"),
        )
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-wrong-operation", operation_id="other-operation",
                 request_hash=request_hash),
        )
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-wrong-hash", operation_id=operation_id,
                 request_hash="different-request-hash"),
        )
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-wrong-epoch", operation_id=operation_id,
                 request_hash=request_hash,
                 permission_epoch=6),
        )

        # F-OI-04 strict binding direct proofs: empty operation, empty
        # request hash and empty scope are not "unbound, therefore free" —
        # they are rejected outright. No default-hash exemption.
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-empty-operation",
                 operation_id=operation_id,
                 request_hash=request_hash,
                 operation=""),
        )
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-empty-request-hash",
                 operation_id=operation_id,
                 request_hash=""),
        )
        assert_no_retry_side_effect(
            auth(nonce="foi-cred-empty-scope",
                 operation_id=operation_id,
                 request_hash=request_hash,
                 scope=frozenset()),
        )


        # Nonce mismatch: credential nonce differs from Authorization nonce.
        mismatch_cred = receipt_credential(
            nonce="foi-cred-inner-nonce",
            request_hash=request_hash,
            receipt_id="foi-cred-nonce-mismatch-receipt",
        )
        mismatch_auth = Authorization(
            permission_epoch=7,
            nonce="foi-cred-outer-nonce",
            receipt=mismatch_cred,
        )
        assert_no_retry_side_effect(mismatch_auth)

        valid_retry = auth(
            nonce="foi-cred-valid-retry-nonce",
            operation_id=operation_id,
            request_hash=request_hash,
        )
        reused = m.commit_suppression(
            operation_id,
            "foi-cred-valid-retry-attempt",
            idempotency_key,
            request_hash,
            auth=valid_retry,
        )

        self.assertIs(reused, first)
        self.assertEqual(len(m.retry_audit), 1)
        record = m.retry_audit[0]
        cred = valid_retry.receipt

        self.assertEqual(record["authorization_receipt"], cred.receipt_id)
        self.assertEqual(record["authorization_credential"], cred)
        self.assertEqual(record["issuer"], cred.issuer)
        self.assertEqual(record["nonce"], cred.nonce)
        self.assertEqual(record["retry_result"], "REUSED_EXISTING_COMMIT")
        self.assertNotEqual(
            cred.receipt_id,
            first.authorization_reference.receipt_id,
        )
        self.assertIn(cred.nonce, m.nonce_registry)
        self.assertEqual(m.fence_generation, original_fence)
        self.assertEqual(m.commit_counter, original_counter)

    def test_FSTOR_12_default_verifier_fails_closed(self):
        """A production-default model must reject every credential.

        FSTOR_10/11 inject TrustAllReceiptVerifier to isolate context
        binding. This test proves that convenience is not the shipped
        default: an unconfigured model has no commit authority at all.
        """
        m = R3Model("m")
        self.assertIsInstance(m.receipt_verifier, RejectingReceiptVerifier)
        m.phase = Phase.AUTHORIZED

        supplied = auth(
            nonce="foi-default-verifier-nonce",
            operation_id="foi-default-verifier-op",
            request_hash="foi-default-hash",
        )

        with self.assertRaises(ContractViolation):
            m.commit_suppression(
                "foi-default-verifier-op",
                "foi-default-attempt",
                "foi-default-key",
                "foi-default-hash",
                auth=supplied,
            )

        self.assertIsNone(m.atomic_commit)
        self.assertEqual(m.lifecycle, Lifecycle.ACTIVE)
        self.assertEqual(m.fence_generation, 0)
        self.assertEqual(m.retry_audit, [])
        self.assertNotIn(supplied.nonce, m.nonce_registry)

    def test_FSTOR_13_credential_context_binding_is_mandatory(self):
        """F-OI-04: no empty or placeholder value may bypass a binding check.

        Covers the bypasses left open before strict binding:
        empty operation, operation mismatch, empty request hash, the
        "default-hash" placeholder for a different request, and a scope
        that omits suppression:commit (including the empty scope).
        """
        operation_id = "foi-bind-operation"
        request_hash = "foi-bind-request-hash"

        def fresh_model():
            m = R3Model("m", receipt_verifier=TrustAllReceiptVerifier())
            m.phase = Phase.AUTHORIZED
            return m

        # Baseline: a correctly bound credential does commit once.
        baseline = fresh_model()
        good = authorized_attempt(
            operation_id, request_hash, "foi-bind-good", "foi-bind-good-r"
        )
        baseline.commit_suppression(
            operation_id, "foi-bind-a1", "foi-bind-key", request_hash,
            auth=good,
        )
        self.assertIsNotNone(baseline.atomic_commit)

        def assert_rejected(label, auth_to_try):
            m = fresh_model()
            with self.subTest(case=label):
                with self.assertRaises(ContractViolation):
                    m.commit_suppression(
                        operation_id,
                        "foi-bind-a1",
                        "foi-bind-key",
                        request_hash,
                        auth=auth_to_try,
                    )
                self.assertIsNone(m.atomic_commit)
                self.assertEqual(m.fence_generation, 0)
                self.assertEqual(m.retry_audit, [])
                self.assertNotIn(auth_to_try.receipt.nonce, m.nonce_registry)

        assert_rejected(
            "empty operation",
            authorized_attempt(
                "", request_hash, "foi-bind-no-op", "foi-bind-no-op-r"
            ),
        )
        assert_rejected(
            "operation mismatch",
            authorized_attempt(
                "other-operation",
                request_hash,
                "foi-bind-wrong-op",
                "foi-bind-wrong-op-r",
            ),
        )
        assert_rejected(
            "empty request hash",
            authorized_attempt(
                operation_id, "", "foi-bind-no-hash", "foi-bind-no-hash-r"
            ),
        )
        assert_rejected(
            "default-hash placeholder",
            authorized_attempt(
                operation_id,
                "default-hash",
                "foi-bind-placeholder",
                "foi-bind-placeholder-r",
            ),
        )
        assert_rejected(
            "scope missing suppression:commit",
            authorized_attempt(
                operation_id,
                request_hash,
                "foi-bind-scope",
                "foi-bind-scope-r",
                scope=frozenset({"suppression:read"}),
            ),
        )
        assert_rejected(
            "empty scope",
            authorized_attempt(
                operation_id,
                request_hash,
                "foi-bind-empty-scope",
                "foi-bind-empty-scope-r",
                scope=frozenset(),
            ),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)


# Static test-method inventory:
#   DFI:                         22
#   OwnerIU011 (T01..T16):       16
#   StorageFaults (STOR-01..07):  7
#   AuthorizationCommitEntry:   14
#   AtomicPublicationFaultInjection:
#                               13 (FSTOR-01..13)
#   Total:                       72 test methods
#
# U-056 additions:
#   - test_FSTOR_10_cleanup_allows_existing_retry_but_rejects_first_commit
#       F-D-NEW-01: phase gate separated from idempotent retry path.
#   - test_FSTOR_11_receipt_credential_verification_and_retry_binding
#       F-OI-04: ReceiptCredential verification with context binding.
#   - test_FSTOR_12_default_verifier_fails_closed
#       F-OI-04: the shipped default verifier rejects every credential.
#   - test_FSTOR_13_credential_context_binding_is_mandatory
#       F-OI-04: empty operation/request hash/scope and the "default-hash"
#       placeholder cannot bypass a binding check.
#
# Execution status:
#   72/72 contract tests PASS (local unittest, Python 3.13).
#   14/14 forget_model tests PASS.
#   These tests cover an in-memory reference model only; they do not prove
#   WAL durability, physical crash recovery, or distributed linearizability.
