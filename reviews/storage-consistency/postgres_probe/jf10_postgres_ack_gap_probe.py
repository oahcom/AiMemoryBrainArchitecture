"""JF-10 coordinator crash-window / unrecorded-ACK recovery probe.

The harness uses a durable SQLite coordinator-ledger fixture and PostgreSQL
18.7 as the prepared participant. Child processes deliberately terminate
after the SQL command succeeds but before the coordinator records its ACK.
This is a deterministic coordinator-crash window test, NOT a TCP packet-loss
or production COC durability test.
"""
from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import time

import psycopg

PG = {
    "host": os.environ.get("PGHOST", "127.0.0.1"),
    "port": int(os.environ.get("PGPORT", "5432")),
    "dbname": os.environ.get("PGDATABASE", "postgres"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", "jf10-ci-only"),
    "autocommit": True,
    "connect_timeout": 3,
}
LEDGER = os.environ.get("JF10_LEDGER", "/tmp/jf10-coordinator-ledger.sqlite")
CASES = {
    "prepare": ("jf10_lost_ack_prepare_001", "op-lost-prepare-ack"),
    "commit": ("jf10_lost_ack_commit_001", "op-lost-commit-ack"),
    "rollback": ("jf10_lost_ack_rollback_001", "op-lost-rollback-ack"),
}
CRASH_EXIT = 86


def db():
    return psycopg.connect(**PG)


def ledger():
    c = sqlite3.connect(LEDGER)
    c.execute(
        "CREATE TABLE IF NOT EXISTS coordinator_operation "
        "(operation_id TEXT PRIMARY KEY, xid TEXT NOT NULL UNIQUE, "
        "phase TEXT NOT NULL, decision TEXT NOT NULL)"
    )
    c.commit()
    return c


def initialize():
    if os.path.exists(LEDGER):
        os.remove(LEDGER)
    with ledger() as l:
        for kind, (xid, op) in CASES.items():
            decision = "COMMIT" if kind == "commit" else "ROLLBACK"
            l.execute(
                "INSERT INTO coordinator_operation VALUES (?, ?, 'NEW', ?)",
                (op, xid, decision),
            )
    with db() as c:
        version = c.execute("SHOW server_version").fetchone()[0]
        assert version.startswith("18.7 "), version
        settings = {
            k: c.execute("SHOW " + k).fetchone()[0]
            for k in ("max_prepared_transactions", "fsync", "synchronous_commit", "full_page_writes")
        }
        assert int(settings["max_prepared_transactions"]) >= 8, settings
        assert all(settings[k] == "on" for k in ("fsync", "synchronous_commit", "full_page_writes")), settings
        c.execute("DROP TABLE IF EXISTS jf10_ack_receipt")
        c.execute("DROP TABLE IF EXISTS jf10_ack_visibility")
        c.execute("DROP TABLE IF EXISTS jf10_ack_lock")
        c.execute("CREATE TABLE jf10_ack_lock (id integer PRIMARY KEY, marker text NOT NULL)")
        c.execute("INSERT INTO jf10_ack_lock VALUES (1, 'coordinator-crash-guard')")
        c.execute("CREATE TABLE jf10_ack_visibility (operation_id text PRIMARY KEY, pointer text NOT NULL)")
        c.execute("CREATE TABLE jf10_ack_receipt (operation_id text PRIMARY KEY, digest text NOT NULL)")
    print(f"SERVER_VERSION={version}")
    print(f"SERVER_SETTINGS={settings}")
    print("COORDINATOR_LEDGER=SQLITE_DURABLE_TEST_FIXTURE")


def child_prepare(kind: str):
    xid, op = CASES[kind]
    with ledger() as l:
        l.execute(
            "UPDATE coordinator_operation SET phase='PREPARE_SENT' WHERE operation_id=?",
            (op,),
        )
    with db() as c:
        c.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        c.execute("SELECT id FROM jf10_ack_lock WHERE id=1 FOR UPDATE")
        c.execute("INSERT INTO jf10_ack_visibility VALUES (%s, %s)", (op, "private:" + op))
        c.execute("INSERT INTO jf10_ack_receipt VALUES (%s, %s)", (op, "sha256:" + op))
        c.execute(f"PREPARE TRANSACTION '{xid}'")
    # Simulate coordinator death after participant prepared, before ACK is
    # durably recorded in the coordinator ledger.
    os._exit(CRASH_EXIT)


def child_terminal(kind: str):
    xid, op = CASES[kind]
    decision = "COMMIT" if kind == "commit" else "ROLLBACK"
    with ledger() as l:
        l.execute(
            "UPDATE coordinator_operation SET phase=?, decision=? WHERE operation_id=?",
            (decision + "_SENT", decision, op),
        )
    with db() as c:
        c.execute(f"{decision} PREPARED '{xid}'")
    # Participant has resolved the XID; coordinator dies before recording ACK.
    os._exit(CRASH_EXIT)


def run_crashed_child(*args: str):
    p = subprocess.run([sys.executable, __file__, *args], check=False)
    assert p.returncode == CRASH_EXIT, (
        f"expected simulated coordinator crash {CRASH_EXIT}, got {p.returncode}"
    )


def participant_state(xid: str):
    with db() as c:
        return c.execute("SELECT gid FROM pg_prepared_xacts WHERE gid=%s", (xid,)).fetchone()


def visibility_state(op: str):
    with db() as c:
        pointer = c.execute("SELECT pointer FROM jf10_ack_visibility WHERE operation_id=%s", (op,)).fetchone()
        receipt = c.execute("SELECT digest FROM jf10_ack_receipt WHERE operation_id=%s", (op,)).fetchone()
    return pointer, receipt


def assert_lock_retained():
    with db() as c:
        c.execute("BEGIN")
        c.execute("SET LOCAL lock_timeout='500ms'")
        try:
            c.execute("UPDATE jf10_ack_lock SET marker='must-not-pass' WHERE id=1")
        except psycopg.errors.LockNotAvailable:
            c.execute("ROLLBACK")
            return
        c.execute("ROLLBACK")
    raise AssertionError("prepared participant lock was not retained")


def recover_prepare():
    xid, op = CASES["prepare"]
    with ledger() as l:
        phase = l.execute(
            "SELECT phase FROM coordinator_operation WHERE operation_id=?", (op,)
        ).fetchone()[0]
        assert phase == "PREPARE_SENT", phase
    assert participant_state(xid) == (xid,), "same prepared XID not found during recovery"
    assert visibility_state(op) == (None, None), "prepared data leaked before terminal decision"
    assert_lock_retained()
    with ledger() as l:
        l.execute(
            "UPDATE coordinator_operation SET phase='PREPARED_RECOVERED' WHERE operation_id=?",
            (op,),
        )
    print("PREPARE_ACK_UNRECORDED_COORDINATOR_CRASH=PASS")
    print("RECOVERED_EXACT_PREPARED_XID_NO_NEW_XID=PASS")
    print("PREPARED_VISIBILITY_PRIVATE_AFTER_ACK_GAP=PASS")


def prepare_case_direct(kind: str):
    xid, op = CASES[kind]
    with db() as c:
        c.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        c.execute("SELECT id FROM jf10_ack_lock WHERE id=1 FOR UPDATE")
        c.execute("INSERT INTO jf10_ack_visibility VALUES (%s, %s)", (op, "private:" + op))
        c.execute("INSERT INTO jf10_ack_receipt VALUES (%s, %s)", (op, "sha256:" + op))
        c.execute(f"PREPARE TRANSACTION '{xid}'")
    with ledger() as l:
        l.execute(
            "UPDATE coordinator_operation SET phase='PREPARED_RECOVERED' WHERE operation_id=?",
            (op,),
        )
    assert participant_state(xid) == (xid,)
    assert visibility_state(op) == (None, None)


def recover_prepare_case_terminal_commit():
    xid, op = CASES["prepare"]
    with ledger() as l:
        phase, decision = l.execute(
            "SELECT phase, decision FROM coordinator_operation WHERE operation_id=?", (op,)
        ).fetchone()
        assert (phase, decision) == ("COMMIT_SENT", "COMMIT"), (phase, decision)
    assert participant_state(xid) is None
    assert visibility_state(op) == (("private:" + op,), ("sha256:" + op,))
    with ledger() as l:
        l.execute(
            "UPDATE coordinator_operation SET phase='COMMITTED_RECOVERED' WHERE operation_id=?",
            (op,),
        )
    print("PREPARE_ACK_GAP_THEN_TERMINAL_COMMIT_ACK_GAP=PASS")
    print("SAME_XID_COMMIT_OUTCOME_RECONCILED=PASS")


def recover_terminal(kind: str):
    xid, op = CASES[kind]
    decision = "COMMIT" if kind == "commit" else "ROLLBACK"
    with ledger() as l:
        phase, recorded = l.execute(
            "SELECT phase, decision FROM coordinator_operation WHERE operation_id=?", (op,)
        ).fetchone()
        assert phase == decision + "_SENT", (phase, decision)
        assert recorded == decision, (recorded, decision)
    assert participant_state(xid) is None, "resolved XID unexpectedly remains prepared"
    pointer, receipt = visibility_state(op)
    if decision == "COMMIT":
        assert pointer == ("private:" + op,), pointer
        assert receipt == ("sha256:" + op,), receipt
        final = "COMMITTED_RECOVERED"
    else:
        assert pointer is None and receipt is None, (pointer, receipt)
        final = "ROLLED_BACK_RECOVERED"
    with ledger() as l:
        l.execute(
            "UPDATE coordinator_operation SET phase=? WHERE operation_id=?",
            (final, op),
        )
    print(f"{decision}_ACK_UNRECORDED_COORDINATOR_CRASH=PASS")
    print(f"SAME_XID_{decision}_OUTCOME_RECONCILED=PASS")
    print(f"{decision}_VISIBILITY_INVARIANT_AFTER_ACK_GAP=PASS")


def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "prepare-send":
            child_prepare("prepare")
        elif mode == "commit-send":
            child_terminal("commit")
        elif mode == "rollback-send":
            child_terminal("rollback")
        else:
            raise SystemExit(f"unknown mode: {mode}")
        return

    initialize()
    run_crashed_child("prepare-send")
    recover_prepare()
    # A prepared participant is now durably known to the test coordinator.
    with ledger() as l:
        l.execute(
            "UPDATE coordinator_operation SET phase='COMMIT_DECIDED' WHERE operation_id=?",
            (CASES["prepare"][1],),
        )
    # Resolve the first participant by the exact original XID; simulate the
    # terminal ACK gap by marking intent before the command and crashing after.
    with ledger() as l:
        l.execute(
            "UPDATE coordinator_operation SET phase='COMMIT_SENT', decision='COMMIT' WHERE operation_id=?",
            (CASES["prepare"][1],),
        )
    with db() as c:
        c.execute(f"COMMIT PREPARED '{CASES['prepare'][0]}'")
    # Intentionally leave the coordinator ledger at COMMIT_SENT.
    recover_prepare_case_terminal_commit()
    # Independent explicit commit and rollback cases are prepared first,
    # then the coordinator records the terminal intent before the child dies.
    for kind in ("commit", "rollback"):
        prepare_case_direct(kind)
        run_crashed_child(kind + "-send")
        recover_terminal(kind)
    print("JF10_COORDINATOR_ACK_GAP_RECOVERY=PASS")
    print("LIMITATION=COORDINATOR_PROCESS_CRASH_WINDOW_NOT_TCP_PACKET_LOSS_OR_PRODUCTION_COC")


if __name__ == "__main__":
    main()
