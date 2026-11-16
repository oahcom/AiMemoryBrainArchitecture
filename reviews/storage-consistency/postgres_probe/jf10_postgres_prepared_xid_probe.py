"""Physical PostgreSQL prepared-XID capability probe for JF-10.

This is an executable single-node CI capability test, not production HA proof.
It exercises real PostgreSQL PREPARE TRANSACTION / COMMIT PREPARED /
ROLLBACK PREPARED, lock retention, atomic visibility rows, and abrupt
container-process restart using the same persistent Docker volume.
"""
from __future__ import annotations

import os
import subprocess
import time

import psycopg
from psycopg import errors


XID_COMMIT = "jf10_pg187_commit_after_restart_001"
XID_ROLLBACK = "jf10_pg187_rollback_same_xid_001"


def connect():
    return psycopg.connect(
        host=os.environ.get("PGHOST", "127.0.0.1"),
        port=int(os.environ.get("PGPORT", "5432")),
        dbname=os.environ.get("PGDATABASE", "postgres"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", "jf10-ci-only"),
        autocommit=True,
        connect_timeout=3,
    )


def wait_ready(timeout=60):
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            with connect() as conn:
                conn.execute("SELECT 1")
            return
        except Exception as exc:  # startup race only
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"PostgreSQL did not become ready: {last_error}")


def setup():
    with connect() as conn:
        version = conn.execute("SHOW server_version").fetchone()[0]
        settings = {
            key: conn.execute("SHOW " + key).fetchone()[0]
            for key in (
                "max_prepared_transactions",
                "fsync",
                "synchronous_commit",
                "full_page_writes",
                "wal_level",
            )
        }
        assert version.startswith("18.7 "), f"expected PostgreSQL 18.7 build, got {version}"
        assert int(settings["max_prepared_transactions"]) >= 8, settings
        for key in ("fsync", "synchronous_commit", "full_page_writes"):
            assert settings[key] == "on", settings
        assert settings["wal_level"] == "replica", settings

        conn.execute("DROP TABLE IF EXISTS jf10_probe_receipt")
        conn.execute("DROP TABLE IF EXISTS jf10_probe_visibility")
        conn.execute("DROP TABLE IF EXISTS jf10_probe_lock")
        conn.execute(
            "CREATE TABLE jf10_probe_lock "
            "(id integer PRIMARY KEY, marker text NOT NULL)"
        )
        conn.execute(
            "INSERT INTO jf10_probe_lock VALUES (1, 'serialization-guard')"
        )
        conn.execute(
            "CREATE TABLE jf10_probe_visibility "
            "(operation_id text PRIMARY KEY, visibility_pointer text NOT NULL)"
        )
        conn.execute(
            "CREATE TABLE jf10_probe_receipt "
            "(operation_id text PRIMARY KEY, receipt_digest text NOT NULL)"
        )
    print(f"SERVER_VERSION={version}")
    print(f"SERVER_SETTINGS={settings}")


def prepare_publication(xid: str, operation_id: str):
    with connect() as conn:
        conn.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        conn.execute("SELECT id FROM jf10_probe_lock WHERE id = 1 FOR UPDATE")
        conn.execute(
            "INSERT INTO jf10_probe_visibility VALUES (%s, %s)",
            (operation_id, "private-staged-object:" + operation_id),
        )
        conn.execute(
            "INSERT INTO jf10_probe_receipt VALUES (%s, %s)",
            (operation_id, "sha256:" + operation_id),
        )
        # XIDs are constants defined above; no caller-controlled SQL is used.
        conn.execute(f"PREPARE TRANSACTION '{xid}'")
    print(f"PREPARED_XID={xid}")


def assert_not_visible(operation_id: str):
    with connect() as conn:
        pointer = conn.execute(
            "SELECT 1 FROM jf10_probe_visibility WHERE operation_id = %s",
            (operation_id,),
        ).fetchone()
        receipt = conn.execute(
            "SELECT 1 FROM jf10_probe_receipt WHERE operation_id = %s",
            (operation_id,),
        ).fetchone()
        assert pointer is None and receipt is None, (
            f"prepared transaction leaked visibility: {operation_id}"
        )


def assert_prepared(xid: str):
    with connect() as conn:
        row = conn.execute(
            "SELECT gid FROM pg_prepared_xacts WHERE gid = %s", (xid,)
        ).fetchone()
        assert row == (xid,), f"prepared XID missing: {xid}; got {row}"


def assert_lock_retained():
    with connect() as conn:
        conn.execute("BEGIN")
        conn.execute("SET LOCAL lock_timeout = '500ms'")
        try:
            conn.execute(
                "UPDATE jf10_probe_lock SET marker = 'must-not-pass' WHERE id = 1"
            )
        except errors.LockNotAvailable:
            conn.execute("ROLLBACK")
            print("PREPARED_LOCK_RETENTION=PASS")
            return
        conn.execute("ROLLBACK")
    raise AssertionError("prepared participant did not retain its row lock")


def assert_visible_pair(operation_id: str, expected: bool):
    with connect() as conn:
        pointer = conn.execute(
            "SELECT visibility_pointer FROM jf10_probe_visibility "
            "WHERE operation_id = %s",
            (operation_id,),
        ).fetchone()
        receipt = conn.execute(
            "SELECT receipt_digest FROM jf10_probe_receipt WHERE operation_id = %s",
            (operation_id,),
        ).fetchone()
    if expected:
        assert pointer == ("private-staged-object:" + operation_id,), pointer
        assert receipt == ("sha256:" + operation_id,), receipt
    else:
        assert pointer is None and receipt is None, (pointer, receipt)


def abrupt_restart_same_container():
    subprocess.run(["docker", "kill", "--signal=KILL", "jf10-postgres"], check=True)
    subprocess.run(["docker", "start", "jf10-postgres"], check=True)
    wait_ready()
    print("POSTMASTER_KILL_RESTART=PASS")


def commit_case():
    operation_id = "op-commit-after-restart"
    prepare_publication(XID_COMMIT, operation_id)
    assert_prepared(XID_COMMIT)
    assert_not_visible(operation_id)
    assert_lock_retained()
    abrupt_restart_same_container()
    assert_prepared(XID_COMMIT)
    assert_not_visible(operation_id)
    assert_lock_retained()
    with connect() as conn:
        conn.execute(f"COMMIT PREPARED '{XID_COMMIT}'")
    assert_visible_pair(operation_id, True)
    print("SAME_XID_COMMIT_AFTER_RESTART=PASS")
    print("ATOMIC_VISIBILITY_POINTER_PLUS_RECEIPT=PASS")


def rollback_case():
    operation_id = "op-rollback-same-xid"
    prepare_publication(XID_ROLLBACK, operation_id)
    assert_prepared(XID_ROLLBACK)
    assert_not_visible(operation_id)
    assert_lock_retained()
    with connect() as conn:
        conn.execute(f"ROLLBACK PREPARED '{XID_ROLLBACK}'")
    assert_visible_pair(operation_id, False)
    with connect() as conn:
        remaining = conn.execute(
            "SELECT 1 FROM pg_prepared_xacts WHERE gid = %s", (XID_ROLLBACK,)
        ).fetchone()
    assert remaining is None
    print("SAME_XID_ROLLBACK=PASS")
    print("ROLLBACK_NON_PUBLICATION=PASS")


if __name__ == "__main__":
    wait_ready()
    setup()
    commit_case()
    rollback_case()
    print("JF10_POSTGRESQL_18_7_SINGLE_NODE_CAPABILITY=PASS")
    print("LIMITATION=NO_REPLICATION_FAILOVER_OR_PRODUCTION_RESTORE_CLAIM")
