#!/usr/bin/env python3
"""REQ-09 SQLite fault-injection reference harness.

This stdlib-only executable reference model mirrors the current
memory-event-store-sqlite write set:
accepted_events -> event_payloads -> compile_outbox.

It is NOT a Rust-native test and does not prove the Rust adapter itself.
FI-04/FI-05 are structural checks: the current adapter schema has no
current-pointer or independent commit-log table to inject into. FI-01 and
FI-09 exercise interrupted uncommitted work and committed reopen behavior;
they are not power-loss or hardware durability certification.
"""
from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

DDL = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
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

def connect(path: str) -> sqlite3.Connection:
    db = sqlite3.connect(path, timeout=5, isolation_level=None)
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA synchronous = FULL")
    return db

def initialize(path: str) -> None:
    db = connect(path)
    db.executescript(DDL)
    db.close()

def counts(db: sqlite3.Connection) -> tuple[int, int, int]:
    return tuple(
        db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in ("accepted_events", "event_payloads", "compile_outbox")
    )

def append_event(db: sqlite3.Connection, key: str, payload: bytes) -> int:
    digest = "sha256-test:" + payload.hex()
    db.execute("BEGIN IMMEDIATE")
    try:
        old = db.execute(
            "SELECT event_row, payload_digest FROM accepted_events "
            "WHERE producer_actor_ref=? AND idempotency_key=?",
            ("actor-1", key),
        ).fetchone()
        if old:
            if old[1] != digest:
                raise ValueError("idempotency conflict")
            db.execute("COMMIT")
            return old[0]
        cur = db.execute(
            "INSERT INTO accepted_events "
            "(producer_actor_ref,idempotency_key,payload_digest,scope_json,envelope_json,accepted_at,processing_state_json) "
            "VALUES (?,?,?,?,?,?,?)",
            ("actor-1", key, digest, '["scope-1"]', "{}", "test-time", '"Pending"'),
        )
        row = cur.lastrowid
        db.execute(
            "INSERT INTO event_payloads(event_row,payload_bytes,verified_digest) VALUES(?,?,?)",
            (row, payload, digest),
        )
        db.execute(
            "INSERT INTO compile_outbox(event_row,intent_kind,created_at) VALUES(?,'compile','test-time')",
            (row,),
        )
        db.execute("COMMIT")
        return row
    except BaseException:
        if db.in_transaction:
            db.execute("ROLLBACK")
        raise

class FaultInjectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name) / "event-store.sqlite")
        initialize(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def db(self):
        return connect(self.path)

    def test_FI01_interrupted_writer_before_commit_rolls_back_all_rows(self):
        db = self.db()
        db.execute("BEGIN IMMEDIATE")
        cur = db.execute(
            "INSERT INTO accepted_events "
            "(producer_actor_ref,idempotency_key,payload_digest,scope_json,envelope_json,accepted_at,processing_state_json) "
            "VALUES ('actor-1','precommit','d','[]','{}','t','Pending')"
        )
        row = cur.lastrowid
        db.execute("INSERT INTO event_payloads VALUES(?,?,?)", (row, b"p", "d"))
        db.execute(
            "INSERT INTO compile_outbox(event_row,intent_kind,created_at) VALUES(?,'compile','t')",
            (row,),
        )
        db.close()  # Abandon the uncommitted transaction.
        db = self.db()
        self.assertEqual(counts(db), (0, 0, 0))
        db.close()

    def test_FI02_commit_then_close_reopen_preserves_atomic_write_set(self):
        db = self.db()
        append_event(db, "normal-commit", b"payload")
        db.close()
        db = self.db()
        self.assertEqual(counts(db), (1, 1, 1))
        db.close()

    def test_FI03_lost_ack_retry_returns_original_idempotent_row(self):
        db = self.db()
        first = append_event(db, "lost-ack", b"payload")
        retry = append_event(db, "lost-ack", b"payload")
        self.assertEqual(first, retry)
        self.assertEqual(counts(db), (1, 1, 1))
        db.close()

    def test_FI04_current_pointer_failure_is_not_in_current_schema(self):
        db = self.db()
        names = {
            row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        self.assertNotIn("current_pointer", names)
        db.close()

    def test_FI05_commit_log_failure_is_not_in_current_schema(self):
        db = self.db()
        names = {
            row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        self.assertNotIn("commit_log", names)
        db.close()

    def test_FI06_idempotency_insert_failure_is_atomic(self):
        db = self.db()
        db.execute(
            """CREATE TRIGGER fail_idempotency BEFORE INSERT ON accepted_events
               BEGIN SELECT RAISE(ABORT, 'FI06 injected idempotency insert failure'); END"""
        )
        with self.assertRaises(sqlite3.IntegrityError):
            append_event(db, "idempotency-fail", b"payload")
        self.assertEqual(counts(db), (0, 0, 0))
        db.close()

    def test_FI07_event_payload_insert_failure_rolls_back_acceptance(self):
        db = self.db()
        db.execute(
            """CREATE TRIGGER fail_payload BEFORE INSERT ON event_payloads
               BEGIN SELECT RAISE(ABORT, 'FI07 injected payload insert failure'); END"""
        )
        with self.assertRaises(sqlite3.IntegrityError):
            append_event(db, "payload-fail", b"payload")
        self.assertEqual(counts(db), (0, 0, 0))
        db.close()

    def test_FI08_outbox_insert_failure_rolls_back_entire_acceptance(self):
        db = self.db()
        db.execute(
            """CREATE TRIGGER fail_outbox BEFORE INSERT ON compile_outbox
               BEGIN SELECT RAISE(ABORT, 'FI08 injected outbox insert failure'); END"""
        )
        with self.assertRaises(sqlite3.IntegrityError):
            append_event(db, "outbox-fail", b"payload")
        self.assertEqual(counts(db), (0, 0, 0))
        db.close()

    def test_FI09_commit_survives_writer_close_and_reopen(self):
        db = self.db()
        append_event(db, "postcommit", b"payload")
        db.close()
        db = self.db()
        self.assertEqual(counts(db), (1, 1, 1))
        db.close()

if __name__ == "__main__":
    unittest.main(verbosity=2)
