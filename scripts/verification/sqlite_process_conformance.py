#!/usr/bin/env python3
"""Process-level SQLite transaction checks for the REQ-01 F-REQ01-09 risk.

This is a Python stdlib SQLite engine/path probe, NOT execution of the Rust
SqliteMemoryStorage adapter. It checks one local file-backed SQLite profile:
WAL + synchronous=FULL + busy_timeout, separate OS processes, and abrupt
process exit before COMMIT.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import multiprocessing as mp
import os
import sqlite3
import tempfile
import time
from pathlib import Path


def connect(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path, timeout=5.0, isolation_level=None)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=FULL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def initialize(path: str) -> None:
    with closing(connect(path)) as conn:
        conn.executescript("""
            CREATE TABLE memories(memory_id TEXT PRIMARY KEY, current_version_id TEXT);
            CREATE TABLE versions(version_id TEXT PRIMARY KEY, memory_id TEXT NOT NULL REFERENCES memories(memory_id));
            CREATE TABLE commit_log(commit_sequence INTEGER PRIMARY KEY, memory_id TEXT NOT NULL REFERENCES memories(memory_id), version_id TEXT NOT NULL UNIQUE REFERENCES versions(version_id));
            CREATE TABLE idempotency(idempotency_key TEXT PRIMARY KEY, memory_id TEXT NOT NULL REFERENCES memories(memory_id), receipt TEXT NOT NULL);
            INSERT INTO memories(memory_id, current_version_id) VALUES ('m1', 'v0');
            INSERT INTO versions(version_id, memory_id) VALUES ('v0', 'm1');
            INSERT INTO commit_log(commit_sequence, memory_id, version_id) VALUES (0, 'm1', 'v0');
        """)


def cas_worker(path: str, version_id: str, start: mp.synchronize.Event, out: mp.queues.Queue) -> None:
    conn = connect(path)
    try:
        start.wait(10)
        conn.execute("BEGIN IMMEDIATE")
        current = conn.execute("SELECT current_version_id FROM memories WHERE memory_id='m1'").fetchone()[0]
        if current != "v0":
            conn.rollback()
            out.put((version_id, "STALE", current))
            return
        conn.execute("INSERT INTO versions(version_id, memory_id) VALUES (?, 'm1')", (version_id,))
        conn.execute("UPDATE memories SET current_version_id=? WHERE memory_id='m1'", (version_id,))
        conn.execute("INSERT INTO commit_log(commit_sequence, memory_id, version_id) VALUES (1, 'm1', ?)", (version_id,))
        conn.execute("INSERT INTO idempotency(idempotency_key, memory_id, receipt) VALUES (?, 'm1', ?)", (f'key-{version_id}', version_id))
        conn.commit()
        out.put((version_id, "COMMITTED", version_id))
    except Exception as exc:  # surfaced to parent as a failed outcome
        try:
            conn.rollback()
        except sqlite3.Error:
            pass
        out.put((version_id, "ERROR", repr(exc)))
    finally:
        conn.close()


def abrupt_exit_worker(path: str, ready_path: str) -> None:
    conn = connect(path)
    conn.execute("BEGIN IMMEDIATE")
    conn.execute("INSERT INTO versions(version_id, memory_id) VALUES ('v-crash', 'm1')")
    conn.execute("UPDATE memories SET current_version_id='v-crash' WHERE memory_id='m1'")
    conn.execute("INSERT INTO commit_log(commit_sequence, memory_id, version_id) VALUES (2, 'm1', 'v-crash')")
    conn.execute("INSERT INTO idempotency(idempotency_key, memory_id, receipt) VALUES ('key-crash', 'm1', 'v-crash')")
    Path(ready_path).write_text("transaction writes issued; COMMIT not issued\n", encoding="utf-8")
    os._exit(23)  # deliberately bypass connection close / Python cleanup


def run() -> None:
    with tempfile.TemporaryDirectory(prefix="req01-sqlite-process-") as tmp:
        db = str(Path(tmp) / "conformance.sqlite")
        initialize(db)

        # Two distinct OS processes, each opening its own SQLite connection.
        ctx = mp.get_context("spawn")
        start = ctx.Event()
        out = ctx.Queue()
        workers = [
            ctx.Process(target=cas_worker, args=(db, "v-a", start, out)),
            ctx.Process(target=cas_worker, args=(db, "v-b", start, out)),
        ]
        for process in workers:
            process.start()
        start.set()
        outcomes = [out.get(timeout=15) for _ in workers]
        for process in workers:
            process.join(15)
            assert process.exitcode == 0, f"CAS worker exit={process.exitcode}"
        states = sorted(item[1] for item in outcomes)
        assert states == ["COMMITTED", "STALE"], f"unexpected CAS outcomes: {outcomes}"
        with closing(connect(db)) as conn:
            current = conn.execute("SELECT current_version_id FROM memories WHERE memory_id='m1'").fetchone()[0]
            version_count = conn.execute("SELECT COUNT(*) FROM versions WHERE version_id IN ('v-a','v-b')").fetchone()[0]
            commit_count = conn.execute("SELECT COUNT(*) FROM commit_log WHERE commit_sequence=1").fetchone()[0]
            idem_count = conn.execute("SELECT COUNT(*) FROM idempotency WHERE idempotency_key IN ('key-v-a','key-v-b')").fetchone()[0]
        assert current in {"v-a", "v-b"}
        assert (version_count, commit_count, idem_count) == (1, 1, 1)
        print("PROCESS_CAS: PASS (2 OS processes; 1 COMMITTED, 1 STALE)")
        print(f"PROCESS_CAS_STATE: current={current} versions={version_count} commit_rows={commit_count} idempotency_rows={idem_count}")

        # Separate process writes the whole logical set but exits before COMMIT.
        ready = str(Path(tmp) / "crash-ready")
        crash = ctx.Process(target=abrupt_exit_worker, args=(db, ready))
        crash.start()
        deadline = time.monotonic() + 10
        while not Path(ready).exists() and crash.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert Path(ready).exists(), "crash worker did not reach pre-COMMIT point"
        crash.join(10)
        assert crash.exitcode == 23, f"expected deliberate abrupt exit 23, got {crash.exitcode}"
        with closing(connect(db)) as conn:
            current_after = conn.execute("SELECT current_version_id FROM memories WHERE memory_id='m1'").fetchone()[0]
            version_after = conn.execute("SELECT COUNT(*) FROM versions WHERE version_id='v-crash'").fetchone()[0]
            commit_after = conn.execute("SELECT COUNT(*) FROM commit_log WHERE version_id='v-crash'").fetchone()[0]
            idem_after = conn.execute("SELECT COUNT(*) FROM idempotency WHERE idempotency_key='key-crash'").fetchone()[0]
        assert current_after == current
        assert (version_after, commit_after, idem_after) == (0, 0, 0)
        print("PRE_COMMIT_PROCESS_EXIT: PASS (worker exit=23; reopened DB exposes no partial write set)")
        print(f"PRE_COMMIT_RECOVERY: current_unchanged={current_after == current} version_rows={version_after} commit_rows={commit_after} idempotency_rows={idem_after}")

        # A committed write set must remain visible after connection close/reopen.
        with closing(connect(db)) as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute("INSERT INTO versions(version_id, memory_id) VALUES ('v-durable', 'm1')")
            conn.execute("UPDATE memories SET current_version_id='v-durable' WHERE memory_id='m1'")
            conn.execute("INSERT INTO commit_log(commit_sequence, memory_id, version_id) VALUES (2, 'm1', 'v-durable')")
            conn.execute("INSERT INTO idempotency(idempotency_key, memory_id, receipt) VALUES ('key-durable', 'm1', 'v-durable')")
            conn.commit()
        with closing(connect(db)) as conn:
            durable = (
                conn.execute("SELECT current_version_id FROM memories WHERE memory_id='m1'").fetchone()[0],
                conn.execute("SELECT COUNT(*) FROM versions WHERE version_id='v-durable'").fetchone()[0],
                conn.execute("SELECT COUNT(*) FROM commit_log WHERE version_id='v-durable'").fetchone()[0],
                conn.execute("SELECT COUNT(*) FROM idempotency WHERE idempotency_key='key-durable'").fetchone()[0],
            )
        assert durable == ("v-durable", 1, 1, 1), f"durable state mismatch: {durable}"
        print("COMMITTED_REOPEN: PASS (current pointer + version + commit log + idempotency all survive reopen)")
        print("RESULT: 3/3 checks passed; Python stdlib SQLite path only, not Rust adapter execution")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    run()
