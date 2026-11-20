"""SQLite-backed bounded reference model for G Applied persistence.

This is a local single-file reference model, NOT production G persistence,
PostgreSQL/Serializable proof, a multi-replica guarantee, or Owner approval.
It exercises immutable identity, atomic ledger/outbox writes, idempotency,
crash-before-commit, lost-ACK retry, current-use invalidation and restore fencing.

Run:
  python -m unittest discover -s 06-memory-context/reference_model -p 'test_*.py' -v
"""
from __future__ import annotations

import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


REQUIRED_AUTHORITIES = ("C", "H", "COC", "I", "D", "STORAGE")


class Rejected(Exception):
    pass


class SimulatedCrash(Exception):
    pass


class LostAck(Exception):
    pass


class RestoreFenced(Exception):
    pass


def validate_full_applied_request_binding(
    h_observation: dict[str, str] | None,
    c_submit_outcome: dict[str, str] | None,
) -> tuple[str, str | None]:
    """TEST-only Full Applied request join; not a production authority adapter."""
    if not isinstance(h_observation, dict) or not isinstance(c_submit_outcome, dict):
        return "UNKNOWN", "H observation or CSubmitOutcome is unavailable"
    required = (
        ("H.inference_request_id", h_observation.get("inference_request_id")),
        ("H.final_request_boundary_type", h_observation.get("final_request_boundary_type")),
        ("C.ActualInferenceRequestId", c_submit_outcome.get("ActualInferenceRequestId")),
        ("C.FinalRequestBoundaryType", c_submit_outcome.get("FinalRequestBoundaryType")),
    )
    missing = [name for name, value in required if not isinstance(value, str) or not value]
    if missing:
        return "UNKNOWN", "Full Applied request binding incomplete: " + ", ".join(missing)
    if h_observation["inference_request_id"] != c_submit_outcome["ActualInferenceRequestId"]:
        return "INVALID", "H.inference_request_id != C.ActualInferenceRequestId"
    if h_observation["final_request_boundary_type"] != c_submit_outcome["FinalRequestBoundaryType"]:
        return "INVALID", "H.final_request_boundary_type != C.FinalRequestBoundaryType"
    return "VALID", None


class AppliedStore:
    def __init__(self, path: str | Path):
        self.path = str(path)
        self._initialize()

    def _connect(self):
        conn = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        conn.execute("PRAGMA busy_timeout=15000")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA synchronous=FULL")
        return conn

    def _initialize(self):
        conn = self._connect()
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS g_meta (
                    key TEXT PRIMARY KEY,
                    value INTEGER NOT NULL
                );
                INSERT OR IGNORE INTO g_meta(key, value) VALUES
                    ('ledger_highwater', 0),
                    ('restore_epoch', 1),
                    ('serving_enabled', 1);

                CREATE TABLE IF NOT EXISTS g_applied_ledger (
                    g_applied_identity_key TEXT PRIMARY KEY,
                    evidence_revision INTEGER NOT NULL,
                    evidence_set_digest TEXT NOT NULL,
                    disposition TEXT NOT NULL CHECK(disposition = 'FULL_APPLIED'),
                    receipt_ref TEXT NOT NULL UNIQUE,
                    ledger_sequence INTEGER NOT NULL UNIQUE,
                    restore_epoch INTEGER NOT NULL,
                    current_use_valid INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS g_applied_outbox (
                    event_id TEXT PRIMARY KEY,
                    g_applied_identity_key TEXT NOT NULL UNIQUE
                        REFERENCES g_applied_ledger(g_applied_identity_key),
                    receipt_ref TEXT NOT NULL,
                    event_type TEXT NOT NULL CHECK(event_type = 'G_APPLIED_COMMITTED')
                );

                CREATE TABLE IF NOT EXISTS g_invalidation_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    g_applied_identity_key TEXT NOT NULL
                        REFERENCES g_applied_ledger(g_applied_identity_key),
                    reason TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        finally:
            conn.close()

    @staticmethod
    def _validate_proofs(proofs: dict[str, str]):
        missing = [name for name in REQUIRED_AUTHORITIES if name not in proofs]
        if missing:
            raise Rejected("missing owner proofs: " + ",".join(missing))
        invalid = [name for name in REQUIRED_AUTHORITIES if proofs[name] != "VALID"]
        if invalid:
            raise Rejected("required owner proof not VALID: " + ",".join(invalid))

    def commit_full_applied(
        self,
        identity_key: str,
        evidence_revision: int,
        evidence_set_digest: str,
        proofs: dict[str, str],
        *,
        c_outcome: str = "HANDOFF_ACCEPTED",
        side_effect_status: str = "PROVEN_OCCURRED",
        h_observation: dict[str, str] | None = None,
        c_submit_outcome: dict[str, str] | None = None,
        crash_before_commit: bool = False,
        lose_ack_after_commit: bool = False,
    ) -> str:
        if not identity_key or not evidence_set_digest or evidence_revision < 1:
            raise Rejected("invalid immutable Applied identity/revision/digest")
        self._validate_proofs(proofs)
        binding_status, binding_reason = validate_full_applied_request_binding(h_observation, c_submit_outcome)
        if binding_status != "VALID":
            raise Rejected(f"{binding_status}: {binding_reason}")
        if c_outcome != "HANDOFF_ACCEPTED" or side_effect_status != "PROVEN_OCCURRED":
            raise Rejected("C outcome is not eligible for G Full Applied")

        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                """SELECT evidence_revision, evidence_set_digest, receipt_ref
                   FROM g_applied_ledger WHERE g_applied_identity_key = ?""",
                (identity_key,),
            ).fetchone()
            if row is not None:
                if row[0] != evidence_revision or row[1] != evidence_set_digest:
                    raise Rejected("same Applied identity with changed evidence revision/digest")
                receipt = row[2]
                conn.commit()
                return receipt

            serving_enabled = conn.execute(
                "SELECT value FROM g_meta WHERE key='serving_enabled'"
            ).fetchone()[0]
            if serving_enabled != 1:
                raise Rejected("restore fence active: new Full Applied commit is blocked")

            seq = conn.execute(
                "SELECT value FROM g_meta WHERE key='ledger_highwater'"
            ).fetchone()[0] + 1
            restore_epoch = conn.execute(
                "SELECT value FROM g_meta WHERE key='restore_epoch'"
            ).fetchone()[0]
            receipt = f"g-applied-receipt:{seq}"
            event_id = f"g-applied-outbox:{seq}"

            conn.execute(
                """INSERT INTO g_applied_ledger(
                    g_applied_identity_key, evidence_revision, evidence_set_digest,
                    disposition, receipt_ref, ledger_sequence, restore_epoch
                ) VALUES (?, ?, ?, 'FULL_APPLIED', ?, ?, ?)""",
                (identity_key, evidence_revision, evidence_set_digest, receipt, seq, restore_epoch),
            )
            conn.execute(
                """INSERT INTO g_applied_outbox(
                    event_id, g_applied_identity_key, receipt_ref, event_type
                ) VALUES (?, ?, ?, 'G_APPLIED_COMMITTED')""",
                (event_id, identity_key, receipt),
            )
            conn.execute(
                "UPDATE g_meta SET value=? WHERE key='ledger_highwater'", (seq,)
            )

            if crash_before_commit:
                raise SimulatedCrash("crash injected before SQLite transaction commit")

            conn.commit()
            if lose_ack_after_commit:
                raise LostAck(receipt)
            return receipt
        except Exception:
            if conn.in_transaction:
                conn.rollback()
            raise
        finally:
            conn.close()

    def invalidate_current_use(self, identity_key: str, reason: str):
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            changed = conn.execute(
                """UPDATE g_applied_ledger SET current_use_valid=0
                   WHERE g_applied_identity_key=?""",
                (identity_key,),
            ).rowcount
            if changed != 1:
                raise Rejected("Applied identity not found")
            conn.execute(
                "INSERT INTO g_invalidation_events(g_applied_identity_key, reason) VALUES (?, ?)",
                (identity_key, reason),
            )
            conn.commit()
        except Exception:
            if conn.in_transaction:
                conn.rollback()
            raise
        finally:
            conn.close()

    def reconcile_restore(
        self,
        *,
        snapshot_epoch: int,
        snapshot_highwater: int,
        trusted_epoch: int,
        trusted_highwater: int,
        owner_currentness: dict[str, bool],
    ) -> str:
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            complete = all(owner_currentness.get(name) is True for name in REQUIRED_AUTHORITIES)
            # A snapshot ahead of the trusted external anchor is not proof of
            # newer state; it may be an unanchored fork or rollback-manipulated image.
            # This reference model requires exact epoch/high-water equality before
            # serving can be re-enabled. A production protocol may advance only with
            # a separately authenticated contiguous-prefix proof.
            anchor_mismatch = snapshot_epoch != trusted_epoch or snapshot_highwater != trusted_highwater
            if anchor_mismatch or not complete:
                conn.execute("UPDATE g_meta SET value=0 WHERE key='serving_enabled'")
                conn.commit()
                return "FENCED"
            conn.execute("UPDATE g_meta SET value=? WHERE key='restore_epoch'", (trusted_epoch,))
            conn.execute("UPDATE g_meta SET value=1 WHERE key='serving_enabled'")
            conn.commit()
            return "RECONCILED"
        except Exception:
            if conn.in_transaction:
                conn.rollback()
            raise
        finally:
            conn.close()

    def current_use_allowed(self, identity_key: str) -> bool:
        conn = self._connect()
        try:
            serving = conn.execute(
                "SELECT value FROM g_meta WHERE key='serving_enabled'"
            ).fetchone()[0]
            row = conn.execute(
                "SELECT current_use_valid FROM g_applied_ledger WHERE g_applied_identity_key=?",
                (identity_key,),
            ).fetchone()
            return bool(serving and row and row[0] == 1)
        finally:
            conn.close()

    def snapshot(self):
        conn = self._connect()
        try:
            ledger = conn.execute("SELECT * FROM g_applied_ledger ORDER BY ledger_sequence").fetchall()
            outbox = conn.execute("SELECT * FROM g_applied_outbox ORDER BY event_id").fetchall()
            meta = dict(conn.execute("SELECT key, value FROM g_meta").fetchall())
            invalidations = conn.execute("SELECT * FROM g_invalidation_events").fetchall()
            return {"ledger": ledger, "outbox": outbox, "meta": meta, "invalidations": invalidations}
        finally:
            conn.close()


class GAppliedPersistenceReferenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = AppliedStore(Path(self.tmp.name) / "g-applied.sqlite3")
        self.proofs = {name: "VALID" for name in REQUIRED_AUTHORITIES}

    def tearDown(self):
        self.tmp.cleanup()

    def commit(self, **kwargs):
        defaults = dict(
            identity_key="g-applied:context-1:delivery-4:request-9",
            evidence_revision=1,
            evidence_set_digest="a" * 64,
            proofs=self.proofs,
            h_observation={
                "inference_request_id": "request-9",
                "final_request_boundary_type": "provider_sdk_send",
            },
            c_submit_outcome={
                "ActualInferenceRequestId": "request-9",
                "FinalRequestBoundaryType": "provider_sdk_send",
            },
        )
        defaults.update(kwargs)
        return self.store.commit_full_applied(**defaults)

    def test_01_same_identity_and_digest_returns_original_receipt(self):
        first = self.commit()
        second = self.commit()
        self.assertEqual(first, second)
        snap = self.store.snapshot()
        self.assertEqual(len(snap["ledger"]), 1)
        self.assertEqual(len(snap["outbox"]), 1)

    def test_02_same_identity_changed_digest_is_conflict(self):
        self.commit()
        with self.assertRaises(Rejected):
            self.commit(evidence_set_digest="b" * 64)
        self.assertEqual(len(self.store.snapshot()["ledger"]), 1)

    def test_03_same_identity_changed_revision_is_conflict(self):
        self.commit()
        with self.assertRaises(Rejected):
            self.commit(evidence_revision=2)
        self.assertEqual(len(self.store.snapshot()["ledger"]), 1)

    def test_04_missing_or_unknown_owner_proof_blocks_full_applied(self):
        with self.assertRaises(Rejected):
            self.commit(proofs={"C": "VALID", "H": "VALID"})
        proofs = dict(self.proofs)
        proofs["D"] = "UNKNOWN"
        with self.assertRaises(Rejected):
            self.commit(proofs=proofs)
        self.assertEqual(self.store.snapshot()["ledger"], [])

    def test_05_crash_before_commit_leaves_no_partial_ledger_or_outbox(self):
        with self.assertRaises(SimulatedCrash):
            self.commit(crash_before_commit=True)
        snap = self.store.snapshot()
        self.assertEqual(snap["ledger"], [])
        self.assertEqual(snap["outbox"], [])
        self.assertEqual(snap["meta"]["ledger_highwater"], 0)

    def test_06_lost_ack_after_commit_retry_returns_same_receipt(self):
        with self.assertRaises(LostAck) as caught:
            self.commit(lose_ack_after_commit=True)
        original = str(caught.exception)
        retry = self.commit()
        self.assertEqual(original, retry)
        snap = self.store.snapshot()
        self.assertEqual(len(snap["ledger"]), 1)
        self.assertEqual(len(snap["outbox"]), 1)

    def test_07_ledger_receipt_and_outbox_commit_atomically(self):
        receipt = self.commit()
        snap = self.store.snapshot()
        self.assertEqual(snap["ledger"][0][4], receipt)
        self.assertEqual(snap["outbox"][0][2], receipt)
        self.assertEqual(snap["meta"]["ledger_highwater"], 1)

    def test_08_concurrent_duplicate_submissions_create_one_fact(self):
        barrier = threading.Barrier(6)

        def submit(_):
            barrier.wait()
            return self.commit()

        with ThreadPoolExecutor(max_workers=6) as pool:
            receipts = list(pool.map(submit, range(6)))
        self.assertEqual(len(set(receipts)), 1)
        snap = self.store.snapshot()
        self.assertEqual(len(snap["ledger"]), 1)
        self.assertEqual(len(snap["outbox"]), 1)

    def test_09_later_forget_invalidates_current_use_but_preserves_history(self):
        receipt = self.commit()
        self.assertTrue(self.store.current_use_allowed("g-applied:context-1:delivery-4:request-9"))
        self.store.invalidate_current_use(
            "g-applied:context-1:delivery-4:request-9", "D_FORGET_FENCE_ADVANCED"
        )
        snap = self.store.snapshot()
        self.assertEqual(len(snap["ledger"]), 1)
        self.assertEqual(snap["ledger"][0][4], receipt)
        self.assertEqual(len(snap["invalidations"]), 1)
        self.assertFalse(self.store.current_use_allowed("g-applied:context-1:delivery-4:request-9"))

    def test_10_stale_restore_highwater_keeps_serving_fenced(self):
        self.commit()
        result = self.store.reconcile_restore(
            snapshot_epoch=1, snapshot_highwater=0,
            trusted_epoch=2, trusted_highwater=1,
            owner_currentness={name: True for name in REQUIRED_AUTHORITIES},
        )
        self.assertEqual(result, "FENCED")
        self.assertFalse(self.store.current_use_allowed("g-applied:context-1:delivery-4:request-9"))

    def test_11_missing_owner_currentness_keeps_restore_fenced(self):
        self.commit()
        currentness = {name: True for name in REQUIRED_AUTHORITIES}
        currentness.pop("D")
        result = self.store.reconcile_restore(
            snapshot_epoch=2, snapshot_highwater=1,
            trusted_epoch=2, trusted_highwater=1,
            owner_currentness=currentness,
        )
        self.assertEqual(result, "FENCED")
        self.assertFalse(self.store.current_use_allowed("g-applied:context-1:delivery-4:request-9"))

    def test_12_exact_restore_currentness_allows_serving(self):
        self.commit()
        result = self.store.reconcile_restore(
            snapshot_epoch=2, snapshot_highwater=1,
            trusted_epoch=2, trusted_highwater=1,
            owner_currentness={name: True for name in REQUIRED_AUTHORITIES},
        )
        self.assertEqual(result, "RECONCILED")
        self.assertTrue(self.store.current_use_allowed("g-applied:context-1:delivery-4:request-9"))

    def test_13_unknown_or_in_doubt_c_outcome_blocks_full_applied(self):
        for outcome in ("UNKNOWN", "IN_DOUBT"):
            with self.subTest(outcome=outcome):
                with self.assertRaises(Rejected):
                    self.commit(c_outcome=outcome, side_effect_status="POSSIBLE_OR_UNKNOWN")
        self.assertEqual(self.store.snapshot()["ledger"], [])

    def test_14_rejected_or_not_invoked_c_outcome_blocks_full_applied(self):
        for outcome, side_effect in (("HANDOFF_REJECTED", "PROVEN_NONE"), ("NOT_INVOKED", "PROVEN_NONE")):
            with self.subTest(outcome=outcome):
                with self.assertRaises(Rejected):
                    self.commit(c_outcome=outcome, side_effect_status=side_effect)
        self.assertEqual(self.store.snapshot()["ledger"], [])


    def test_18_exact_request_id_and_boundary_type_match_allows_full_applied(self):
        status, reason = validate_full_applied_request_binding(
            {"inference_request_id": "request-9", "final_request_boundary_type": "provider_sdk_send"},
            {"ActualInferenceRequestId": "request-9", "FinalRequestBoundaryType": "provider_sdk_send"},
        )
        self.assertEqual((status, reason), ("VALID", None))
        self.assertTrue(self.commit())

    def test_19_request_id_mismatch_blocks_full_applied(self):
        with self.assertRaisesRegex(Rejected, "INVALID: H.inference_request_id"):
            self.commit(c_submit_outcome={"ActualInferenceRequestId": "request-other", "FinalRequestBoundaryType": "provider_sdk_send"})
        self.assertEqual(self.store.snapshot()["ledger"], [])

    def test_20_boundary_type_mismatch_blocks_full_applied(self):
        with self.assertRaisesRegex(Rejected, "INVALID: H.final_request_boundary_type"):
            self.commit(c_submit_outcome={"ActualInferenceRequestId": "request-9", "FinalRequestBoundaryType": "runtime_final_submit_hook"})
        self.assertEqual(self.store.snapshot()["ledger"], [])

    def test_21_missing_actual_request_id_is_unknown_and_ineligible(self):
        with self.assertRaisesRegex(Rejected, "UNKNOWN:.*C.ActualInferenceRequestId"):
            self.commit(c_submit_outcome={"FinalRequestBoundaryType": "provider_sdk_send"})
        self.assertEqual(self.store.snapshot()["ledger"], [])

    def test_22_missing_boundary_type_is_unknown_and_ineligible(self):
        with self.assertRaisesRegex(Rejected, "UNKNOWN:.*C.FinalRequestBoundaryType"):
            self.commit(c_submit_outcome={"ActualInferenceRequestId": "request-9"})
        self.assertEqual(self.store.snapshot()["ledger"], [])

    def test_23_missing_h_request_identity_is_unknown_and_ineligible(self):
        with self.assertRaisesRegex(Rejected, "UNKNOWN:.*H.inference_request_id"):
            self.commit(h_observation={"final_request_boundary_type": "provider_sdk_send"})
        self.assertEqual(self.store.snapshot()["ledger"], [])

    def test_15_snapshot_epoch_ahead_of_trusted_anchor_keeps_serving_fenced(self):
        self.commit()
        result = self.store.reconcile_restore(
            snapshot_epoch=3, snapshot_highwater=1,
            trusted_epoch=2, trusted_highwater=1,
            owner_currentness={name: True for name in REQUIRED_AUTHORITIES},
        )
        self.assertEqual(result, "FENCED")
        self.assertFalse(self.store.current_use_allowed("g-applied:context-1:delivery-4:request-9"))

    def test_16_snapshot_highwater_ahead_of_trusted_anchor_keeps_restore_fenced(self):
        self.commit()
        result = self.store.reconcile_restore(
            snapshot_epoch=2, snapshot_highwater=2,
            trusted_epoch=2, trusted_highwater=1,
            owner_currentness={name: True for name in REQUIRED_AUTHORITIES},
        )
        self.assertEqual(result, "FENCED")
        self.assertFalse(self.store.current_use_allowed("g-applied:context-1:delivery-4:request-9"))

    def test_17_restore_fence_blocks_new_full_applied_commit(self):
        self.commit()
        result = self.store.reconcile_restore(
            snapshot_epoch=1, snapshot_highwater=0,
            trusted_epoch=2, trusted_highwater=1,
            owner_currentness={name: True for name in REQUIRED_AUTHORITIES},
        )
        self.assertEqual(result, "FENCED")
        with self.assertRaisesRegex(Rejected, "restore fence active"):
            self.commit(identity_key="g-applied:new-context:new-delivery:new-request")
        snap = self.store.snapshot()
        self.assertEqual(len(snap["ledger"]), 1)
        self.assertEqual(len(snap["outbox"]), 1)
        self.assertFalse(self.store.current_use_allowed("g-applied:context-1:delivery-4:request-9"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
