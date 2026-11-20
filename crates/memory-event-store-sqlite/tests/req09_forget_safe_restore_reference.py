#!/usr/bin/env python3
"""REQ-09 Forget-safe backup/restore reference implementation.

The Forget fence is stored in a separate durable SQLite database which is
never replaced by restoring an event-store backup. Restore stages the backup,
validates both stores, removes every event whose persisted ScopeRef namespace
is fenced, and only then atomically replaces the live database.

This is an executable Python/SQLite reference implementation, NOT Rust-native
adapter integration, production deployment, cross-device atomicity, or a
certified backup system. Callers must keep the fence DB on an independently
protected durable volume and must not restore it from the event-store backup.
"""
from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

EVENT_DDL = """
PRAGMA foreign_keys = ON;
CREATE TABLE accepted_events (
  event_row INTEGER PRIMARY KEY AUTOINCREMENT,
  producer_actor_ref TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload_digest TEXT NOT NULL,
  scope_json TEXT NOT NULL,
  envelope_json TEXT NOT NULL,
  accepted_at TEXT NOT NULL,
  processing_state_json TEXT NOT NULL,
  UNIQUE(producer_actor_ref, idempotency_key)
);
CREATE TABLE event_payloads (
  event_row INTEGER PRIMARY KEY REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
  payload_bytes BLOB NOT NULL,
  verified_digest TEXT NOT NULL
);
CREATE TABLE compile_outbox (
  outbox_row INTEGER PRIMARY KEY AUTOINCREMENT,
  event_row INTEGER NOT NULL UNIQUE REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
  intent_kind TEXT NOT NULL CHECK(intent_kind = 'compile'),
  created_at TEXT NOT NULL
);
"""
FENCE_DDL = """
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
CREATE TABLE IF NOT EXISTS forget_fence (
  namespace_key TEXT PRIMARY KEY,
  fence_seq INTEGER NOT NULL UNIQUE,
  reason_digest TEXT NOT NULL,
  recorded_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fence_meta (
  singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
  next_seq INTEGER NOT NULL CHECK(next_seq > 0)
);
INSERT OR IGNORE INTO fence_meta(singleton, next_seq) VALUES(1, 1);
"""

class FenceUnavailable(RuntimeError):
    pass


def connect(path: str | Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(path), timeout=5, isolation_level=None)
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA synchronous = FULL")
    return db


def initialize_event_store(path: str | Path) -> None:
    db = connect(path)
    db.executescript(EVENT_DDL)
    db.close()


def initialize_fence(path: str | Path) -> None:
    db = connect(path)
    db.executescript(FENCE_DDL)
    db.close()


def add_event(db: sqlite3.Connection, key: str, namespace_key: str, payload: bytes) -> int:
    scope = [{"scope_id": namespace_key, "scope_kind": "User", "namespace_key": namespace_key}]
    db.execute("BEGIN IMMEDIATE")
    try:
        cur = db.execute(
            "INSERT INTO accepted_events(producer_actor_ref,idempotency_key,payload_digest,scope_json,envelope_json,accepted_at,processing_state_json) VALUES(?,?,?,?,?,?,?)",
            ("actor-1", key, "sha256:" + payload.hex(), json.dumps(scope), "{}", "t", '"Pending"'),
        )
        row = cur.lastrowid
        db.execute("INSERT INTO event_payloads VALUES(?,?,?)", (row, payload, "sha256:" + payload.hex()))
        db.execute("INSERT INTO compile_outbox(event_row,intent_kind,created_at) VALUES(?,'compile','t')", (row,))
        db.execute("COMMIT")
        return row
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise


def _load_fences(db: sqlite3.Connection) -> set[str]:
    # Missing tables, malformed metadata, or an unreadable fence fail closed.
    row = db.execute("SELECT next_seq FROM fence_meta WHERE singleton=1").fetchone()
    if row is None or row[0] < 1:
        raise FenceUnavailable("Forget fence metadata missing or invalid")
    fences = db.execute("SELECT namespace_key, fence_seq FROM forget_fence").fetchall()
    if any(not key or seq <= 0 or seq >= row[0] for key, seq in fences):
        raise FenceUnavailable("Forget fence row invalid")
    return {key for key, _ in fences}


def _read_fences(fence_path: str | Path) -> set[str]:
    db = None
    try:
        db = connect(fence_path)
        db.execute("BEGIN IMMEDIATE")
        return _load_fences(db)
    except BaseException as exc:
        if isinstance(exc, FenceUnavailable):
            raise
        raise FenceUnavailable(f"Forget fence unavailable: {exc}") from exc
    finally:
        if db is not None:
            if db.in_transaction:
                db.execute("ROLLBACK")
            db.close()


def _purge_fenced_rows(db: sqlite3.Connection, fences: set[str]) -> int:
    doomed: list[int] = []
    for (row_id, scope_json) in db.execute("SELECT event_row, scope_json FROM accepted_events"):
        try:
            scopes = json.loads(scope_json)
            if not isinstance(scopes, list) or not scopes:
                raise ValueError("invalid scope list")
            keys = {item["namespace_key"] for item in scopes if isinstance(item, dict) and item.get("namespace_key")}
            if len(keys) != len(scopes):
                raise ValueError("invalid ScopeRef namespace")
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            raise FenceUnavailable(f"event {row_id} has invalid scope metadata; restore refused") from exc
        if keys & fences:
            doomed.append(row_id)
    if doomed:
        marks = ",".join("?" for _ in doomed)
        db.execute(f"DELETE FROM compile_outbox WHERE event_row IN ({marks})", doomed)
        db.execute(f"DELETE FROM event_payloads WHERE event_row IN ({marks})", doomed)
        db.execute(f"DELETE FROM accepted_events WHERE event_row IN ({marks})", doomed)
    return len(doomed)


def record_forget(fence_path: str | Path, namespace_key: str, reason_digest: str) -> int:
    """Durably append a monotonic fence before attempting live-data purge."""
    if not namespace_key or not reason_digest:
        raise ValueError("namespace_key and reason_digest are required")
    db = connect(fence_path)
    db.execute("BEGIN IMMEDIATE")
    try:
        existing = db.execute("SELECT fence_seq FROM forget_fence WHERE namespace_key=?", (namespace_key,)).fetchone()
        if existing:
            db.execute("COMMIT")
            return existing[0]
        seq = db.execute("SELECT next_seq FROM fence_meta WHERE singleton=1").fetchone()[0]
        db.execute("INSERT INTO forget_fence VALUES(?,?,?,?)", (namespace_key, seq, reason_digest, "test-time"))
        db.execute("UPDATE fence_meta SET next_seq=? WHERE singleton=1", (seq + 1,))
        db.execute("COMMIT")
        return seq
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    finally:
        db.close()


def forget_live(event_store_path: str | Path, fence_path: str | Path, namespace_key: str, reason_digest: str) -> int:
    """Fence first; then purge. A crash between steps remains read/restore safe."""
    seq = record_forget(fence_path, namespace_key, reason_digest)
    db = connect(event_store_path)
    try:
        db.execute("BEGIN IMMEDIATE")
        _purge_fenced_rows(db, {namespace_key})
        db.execute("COMMIT")
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise
    finally:
        db.close()
    return seq


def visible_event_keys(event_store_path: str | Path, fence_path: str | Path) -> set[str]:
    fences = _read_fences(fence_path)
    db = connect(event_store_path)
    try:
        visible = set()
        for key, scope_json in db.execute("SELECT idempotency_key, scope_json FROM accepted_events"):
            scopes = json.loads(scope_json)
            if not isinstance(scopes, list) or not scopes:
                raise FenceUnavailable("invalid persisted scope; reads fail closed")
            namespace_keys = {item.get("namespace_key") for item in scopes if isinstance(item, dict)}
            if not namespace_keys or None in namespace_keys:
                raise FenceUnavailable("invalid persisted ScopeRef; reads fail closed")
            if not (namespace_keys & fences):
                visible.add(key)
        return visible
    finally:
        db.close()


def restore_backup_with_fence(backup_path: str | Path, live_path: str | Path, fence_path: str | Path) -> int:
    """Stage, fence-filter, validate, then atomically replace the live DB file.

    An IMMEDIATE transaction on the separate fence DB is held until after
    os.replace. Concurrent Forget writes therefore serialize after restore;
    they cannot land between the fence snapshot and live-file replacement.
    """
    try:
        fence_db = connect(fence_path)
        fence_db.execute("BEGIN IMMEDIATE")
        fences = _load_fences(fence_db)
    except BaseException as exc:
        try:
            fence_db.close()
        except (UnboundLocalError, sqlite3.Error):
            pass
        if isinstance(exc, FenceUnavailable):
            raise
        raise FenceUnavailable(f"Forget fence unavailable: {exc}") from exc

    live = Path(live_path)
    live.parent.mkdir(parents=True, exist_ok=True)
    fd, staged_name = tempfile.mkstemp(prefix=live.name + ".restore-", suffix=".sqlite", dir=live.parent)
    os.close(fd)
    staged = Path(staged_name)
    try:
        source = sqlite3.connect(str(backup_path))
        destination = sqlite3.connect(str(staged))
        try:
            source.backup(destination)
        finally:
            destination.close()
            source.close()
        db = connect(staged)
        try:
            required = {"accepted_events", "event_payloads", "compile_outbox"}
            present = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if not required.issubset(present):
                raise FenceUnavailable("backup schema incomplete; restore refused")
            db.execute("BEGIN IMMEDIATE")
            purged = _purge_fenced_rows(db, fences)
            db.execute("COMMIT")
            check = db.execute("PRAGMA integrity_check").fetchone()[0]
            if check != "ok":
                raise FenceUnavailable(f"staged backup integrity_check={check}")
        except BaseException:
            if db.in_transaction:
                db.execute("ROLLBACK")
            raise
        finally:
            db.close()
        # No live connection may remain open across this atomic replacement.
        for suffix in ("-wal", "-shm"):
            sidecar = Path(str(live) + suffix)
            if sidecar.exists():
                sidecar.unlink()
        os.replace(staged, live)
        return purged
    except BaseException:
        if staged.exists():
            staged.unlink()
        raise
    finally:
        if fence_db.in_transaction:
            fence_db.execute("ROLLBACK")
        fence_db.close()


class ForgetSafeRestoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.live = root / "live.sqlite"
        self.backup = root / "backup.sqlite"
        self.fence = root / "forget-fence.sqlite"
        initialize_event_store(self.live)
        initialize_fence(self.fence)
        db = connect(self.live)
        add_event(db, "alice-event", "user:alice", b"secret")
        add_event(db, "bob-event", "user:bob", b"retained")
        db.close()
        src = sqlite3.connect(str(self.live))
        dst = sqlite3.connect(str(self.backup))
        src.backup(dst)
        dst.close(); src.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_restore_uses_external_fence_and_does_not_resurrect_forgotten_scope(self):
        forget_live(self.live, self.fence, "user:alice", "sha256:forget-request")
        self.assertEqual(visible_event_keys(self.live, self.fence), {"bob-event"})
        purged = restore_backup_with_fence(self.backup, self.live, self.fence)
        self.assertEqual(purged, 1)
        self.assertEqual(visible_event_keys(self.live, self.fence), {"bob-event"})
        db = connect(self.live)
        self.assertEqual(tuple(db.execute("SELECT COUNT(*) FROM " + t).fetchone()[0] for t in ("accepted_events", "event_payloads", "compile_outbox")), (1, 1, 1))
        db.close()

    def test_fence_is_idempotent_and_monotonic(self):
        first = record_forget(self.fence, "user:alice", "sha256:request")
        again = record_forget(self.fence, "user:alice", "sha256:request")
        second = record_forget(self.fence, "user:bob", "sha256:request-2")
        self.assertEqual(first, again)
        self.assertLess(first, second)

    def test_missing_fence_fails_closed_without_replacing_live_database(self):
        before = visible_event_keys(self.live, self.fence)
        missing = Path(self.tmp.name) / "missing-fence.sqlite"
        with self.assertRaises(FenceUnavailable):
            restore_backup_with_fence(self.backup, self.live, missing)
        self.assertEqual(visible_event_keys(self.live, self.fence), before)

    def test_corrupt_scope_metadata_fails_closed_without_partial_restore(self):
        db = sqlite3.connect(str(self.backup))
        db.execute("UPDATE accepted_events SET scope_json='not-json' WHERE idempotency_key='alice-event'")
        db.commit(); db.close()
        before = visible_event_keys(self.live, self.fence)
        with self.assertRaises(FenceUnavailable):
            restore_backup_with_fence(self.backup, self.live, self.fence)
        self.assertEqual(visible_event_keys(self.live, self.fence), before)

    def test_fence_survives_reopening_and_backup_restore(self):
        record_forget(self.fence, "user:alice", "sha256:forget-request")
        self.assertEqual(restore_backup_with_fence(self.backup, self.live, self.fence), 1)
        self.assertEqual(_read_fences(self.fence), {"user:alice"})

    def test_durable_fence_hides_data_even_if_live_purge_was_interrupted(self):
        # Simulate a crash after the external fence commit but before live purge.
        record_forget(self.fence, "user:alice", "sha256:forget-request")
        self.assertEqual(visible_event_keys(self.live, self.fence), {"bob-event"})
        self.assertEqual(restore_backup_with_fence(self.backup, self.live, self.fence), 1)
        self.assertEqual(visible_event_keys(self.live, self.fence), {"bob-event"})

    def test_invalid_fence_schema_fails_closed(self):
        bad_fence = Path(self.tmp.name) / "bad-fence.sqlite"
        sqlite3.connect(str(bad_fence)).close()
        before = visible_event_keys(self.live, self.fence)
        with self.assertRaises(FenceUnavailable):
            restore_backup_with_fence(self.backup, self.live, bad_fence)
        self.assertEqual(visible_event_keys(self.live, self.fence), before)

    def test_backup_restore_keeps_unforgotten_scope_and_all_write_set_tables_consistent(self):
        record_forget(self.fence, "user:alice", "sha256:forget-request")
        restore_backup_with_fence(self.backup, self.live, self.fence)
        db = connect(self.live)
        self.assertEqual(db.execute("SELECT idempotency_key FROM accepted_events").fetchall(), [("bob-event",)])
        self.assertEqual(db.execute("SELECT COUNT(*) FROM event_payloads").fetchone()[0], 1)
        self.assertEqual(db.execute("SELECT COUNT(*) FROM compile_outbox").fetchone()[0], 1)
        db.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
