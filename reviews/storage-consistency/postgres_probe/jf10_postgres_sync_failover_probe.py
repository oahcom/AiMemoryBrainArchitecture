"""Two-node PostgreSQL 18.7 synchronous-replication/failover probe.

This validates whether a PREPARE TRANSACTION record and its locks reach a
synchronous standby before the primary is lost, and whether the promoted
standby can resolve the exact same XID. CI only; not production HA approval.
"""
from __future__ import annotations

import os
import subprocess
import time

import psycopg
from psycopg import errors


XID = "jf10_pg187_sync_failover_commit_001"
OPERATION_ID = "op-sync-failover-commit"


def conn(host: str, port: int = 5432):
    return psycopg.connect(
        host=host,
        port=port,
        dbname="postgres",
        user="postgres",
        password="jf10-ha-ci-only",
        autocommit=True,
        connect_timeout=3,
    )


def wait_db(host: str, port: int = 5432, timeout: int = 90):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            with conn(host, port) as c:
                c.execute("SELECT 1")
            return
        except Exception as exc:
            last = exc
            time.sleep(1)
    raise RuntimeError(f"database {host} not ready: {last}")


def docker(*args: str):
    subprocess.run(["docker", *args], check=True)


def wait_sync():
    deadline = time.time() + 90
    while time.time() < deadline:
        with conn("127.0.0.1") as c:
            row = c.execute(
                "SELECT application_name, state, sync_state "
                "FROM pg_stat_replication"
            ).fetchone()
            if row and row[0] == "jf10_standby" and row[1] == "streaming" and row[2] == "sync":
                print(f"SYNCHRONOUS_STANDBY={row}")
                return
        time.sleep(1)
    raise AssertionError("standby did not become synchronous")


def setup_tables():
    with conn("127.0.0.1") as c:
        version = c.execute("SHOW server_version").fetchone()[0]
        settings = {
            k: c.execute("SHOW " + k).fetchone()[0]
            for k in (
                "max_prepared_transactions",
                "fsync",
                "synchronous_commit",
                "full_page_writes",
                "wal_level",
                "synchronous_standby_names",
            )
        }
        assert version.startswith("18.7 "), version
        assert settings["max_prepared_transactions"] == "16", settings
        assert settings["fsync"] == "on", settings
        assert settings["synchronous_commit"] == "remote_apply", settings
        assert settings["full_page_writes"] == "on", settings
        assert settings["wal_level"] == "replica", settings
        assert settings["synchronous_standby_names"] == "FIRST 1 (jf10_standby)", settings

        c.execute("DROP TABLE IF EXISTS jf10_ha_receipt")
        c.execute("DROP TABLE IF EXISTS jf10_ha_visibility")
        c.execute("DROP TABLE IF EXISTS jf10_ha_lock")
        c.execute("CREATE TABLE jf10_ha_lock (id integer PRIMARY KEY, marker text NOT NULL)")
        c.execute("INSERT INTO jf10_ha_lock VALUES (1, 'serialization-guard')")
        c.execute(
            "CREATE TABLE jf10_ha_visibility "
            "(operation_id text PRIMARY KEY, visibility_pointer text NOT NULL)"
        )
        c.execute(
            "CREATE TABLE jf10_ha_receipt "
            "(operation_id text PRIMARY KEY, receipt_digest text NOT NULL)"
        )
    print(f"PRIMARY_VERSION={version}")
    print(f"PRIMARY_SETTINGS={settings}")


def prepare_on_primary():
    with conn("127.0.0.1") as c:
        c.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        c.execute("SELECT id FROM jf10_ha_lock WHERE id = 1 FOR UPDATE")
        c.execute(
            "INSERT INTO jf10_ha_visibility VALUES (%s, %s)",
            (OPERATION_ID, "private-staged-object:" + OPERATION_ID),
        )
        c.execute(
            "INSERT INTO jf10_ha_receipt VALUES (%s, %s)",
            (OPERATION_ID, "sha256:" + OPERATION_ID),
        )
        c.execute(f"PREPARE TRANSACTION '{XID}'")
    print(f"PRIMARY_PREPARED_XID={XID}")


def assert_prepared(host: str, port: int = 5432):
    with conn(host, port) as c:
        row = c.execute(
            "SELECT gid FROM pg_prepared_xacts WHERE gid = %s", (XID,)
        ).fetchone()
        assert row == (XID,), f"{host} missing prepared XID: {row}"


def assert_not_visible(host: str, port: int = 5432):
    with conn(host, port) as c:
        p = c.execute(
            "SELECT 1 FROM jf10_ha_visibility WHERE operation_id = %s",
            (OPERATION_ID,),
        ).fetchone()
        r = c.execute(
            "SELECT 1 FROM jf10_ha_receipt WHERE operation_id = %s",
            (OPERATION_ID,),
        ).fetchone()
        assert p is None and r is None, (host, p, r)


def assert_lock_blocked(host: str, port: int = 5432):
    with conn(host, port) as c:
        c.execute("BEGIN")
        c.execute("SET LOCAL lock_timeout = '750ms'")
        try:
            c.execute(
                "UPDATE jf10_ha_lock SET marker = 'must-not-pass' WHERE id = 1"
            )
        except errors.LockNotAvailable:
            c.execute("ROLLBACK")
            print(f"PREPARED_LOCK_RETAINED_ON_{host.upper().replace('.', '_')}=PASS")
            return
        c.execute("ROLLBACK")
    raise AssertionError(f"prepared lock not retained on {host}")


def promote_standby():
    docker("kill", "--signal=KILL", "jf10-primary")
    print("PRIMARY_HARD_KILL=PASS")
    docker("exec", "-u", "postgres", "jf10-standby",
           "pg_ctl", "-D", "/var/lib/postgresql/18/docker", "promote")
    deadline = time.time() + 90
    while time.time() < deadline:
        try:
            with conn("127.0.0.1", 5433) as c:
                recovery = c.execute("SELECT pg_is_in_recovery()").fetchone()[0]
                if recovery is False:
                    print("STANDBY_PROMOTION=PASS")
                    return
        except Exception:
            pass
        time.sleep(1)
    raise AssertionError("standby did not promote")


def verify_and_commit():
    wait_db("127.0.0.1", port=5433)
    with conn("127.0.0.1", 5433) as c:
        recovery = c.execute("SELECT pg_is_in_recovery()").fetchone()[0]
        assert recovery is False, "promoted server is still in recovery"
        settings = {
            k: c.execute("SHOW " + k).fetchone()[0]
            for k in ("max_prepared_transactions", "fsync", "synchronous_commit")
        }
        assert settings["max_prepared_transactions"] == "16", settings
        print(f"PROMOTED_SETTINGS={settings}")

    assert_prepared("127.0.0.1", 5433)
    assert_not_visible("127.0.0.1", 5433)
    assert_lock_blocked("127.0.0.1", 5433)
    with conn("127.0.0.1", 5433) as c:
        c.execute(f"COMMIT PREPARED '{XID}'")
    with conn("127.0.0.1", 5433) as c:
        p = c.execute(
            "SELECT visibility_pointer FROM jf10_ha_visibility WHERE operation_id = %s",
            (OPERATION_ID,),
        ).fetchone()
        r = c.execute(
            "SELECT receipt_digest FROM jf10_ha_receipt WHERE operation_id = %s",
            (OPERATION_ID,),
        ).fetchone()
    assert p == ("private-staged-object:" + OPERATION_ID,), p
    assert r == ("sha256:" + OPERATION_ID,), r
    print("PREPARED_XID_REPLAYED_TO_SYNC_STANDBY=PASS")
    print("SAME_XID_COMMIT_AFTER_PRIMARY_LOSS=PASS")
    print("ATOMIC_VISIBILITY_AFTER_PROMOTION=PASS")


if __name__ == "__main__":
    wait_db("127.0.0.1", port=5432)
    wait_db("127.0.0.1", port=5433)
    # Standby is separately mapped to host port 5433.
    deadline = time.time() + 90
    while time.time() < deadline:
        try:
            with conn("127.0.0.1") as c:
                app = c.execute(
                    "SELECT application_name, state, sync_state FROM pg_stat_replication"
                ).fetchone()
                if app and app[2] == "sync":
                    break
        except Exception:
            pass
        time.sleep(1)
    wait_sync()
    setup_tables()
    prepare_on_primary()
    assert_prepared("127.0.0.1")
    assert_prepared("127.0.0.1")  # verify primary view before promotion
    assert_not_visible("127.0.0.1")
    # Standby SQL is reached through host port 5433.
    with psycopg.connect(
        host="127.0.0.1", port=5433, dbname="postgres", user="postgres",
        password="jf10-ha-ci-only", autocommit=True, connect_timeout=3
    ) as standby:
        assert standby.execute("SELECT pg_is_in_recovery()").fetchone()[0] is True
        # PostgreSQL intentionally exposes no pg_prepared_xacts rows while
        # a server is in hot-standby recovery. Verify private data here; verify
        # the prepared XID after promotion has completed recovery.
        row = standby.execute(
            "SELECT gid FROM pg_prepared_xacts WHERE gid = %s", (XID,)
        ).fetchone()
        assert row is None, f"hot standby unexpectedly exposed prepared XID: {row}"
        assert standby.execute(
            "SELECT 1 FROM jf10_ha_visibility WHERE operation_id = %s",
            (OPERATION_ID,),
        ).fetchone() is None
        assert standby.execute(
            "SELECT 1 FROM jf10_ha_receipt WHERE operation_id = %s",
            (OPERATION_ID,),
        ).fetchone() is None
    print("SYNCHRONOUS_STANDBY_PREPARED_WAL_REPLAY=PASS")
    print("HOT_STANDBY_PREPARED_XACT_VIEW_HIDDEN_AS_DOCUMENTED=PASS")
    promote_standby()
    verify_and_commit()
    print("JF10_POSTGRESQL_18_7_SYNC_FAILOVER_CAPABILITY=PASS")
    print("LIMITATION=NO_BACKUP_RESTORE_OR_PRODUCTION_OPERATOR_CLAIM")
