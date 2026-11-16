"""Fail-closed test when the required synchronous standby disappears.

This is a PostgreSQL 18.7 CI capability probe, not production fencing evidence.
It proves the protected PREPARE boundary does not silently downgrade to local
durability when synchronous_commit=remote_apply and the required synchronous
standby is unavailable.
"""
from __future__ import annotations

import time

import psycopg
from psycopg import errors

XID = "jf10_sync_standby_unavailable_001"
OPERATION_ID = "op-sync-standby-unavailable"


def conn():
    return psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="jf10-ha-ci-only",
        autocommit=True,
        connect_timeout=3,
        options="-c statement_timeout=5000",
    )


def wait_no_sync_standby():
    deadline = time.time() + 30
    while time.time() < deadline:
        with conn() as c:
            row = c.execute(
                "SELECT count(*) FROM pg_stat_replication WHERE sync_state = 'sync'"
            ).fetchone()
            if row == (0,):
                return
        time.sleep(0.25)
    raise AssertionError("synchronous standby still present")


def main():
    with conn() as c:
        version = c.execute("SHOW server_version").fetchone()[0]
        assert version.startswith("18.7 "), version
        settings = {
            k: c.execute("SHOW " + k).fetchone()[0]
            for k in ("synchronous_commit", "synchronous_standby_names", "fsync")
        }
        assert settings["synchronous_commit"] == "remote_apply", settings
        assert settings["synchronous_standby_names"] == "FIRST 1 (jf10_standby)", settings
        assert settings["fsync"] == "on", settings
        c.execute("CREATE TABLE IF NOT EXISTS jf10_sync_unavailable_visibility "
                  "(operation_id text PRIMARY KEY, value text NOT NULL)")
        c.execute("DELETE FROM jf10_sync_unavailable_visibility WHERE operation_id = %s",
                  (OPERATION_ID,))
    print(f"SERVER_VERSION={version}")
    print(f"PROTECTED_SYNC_SETTINGS={settings}")

    # Stop the required synchronous standby. The primary must not silently
    # convert remote_apply into local-only durability.
    import subprocess
    subprocess.run(["docker", "stop", "jf10-standby"], check=True, capture_output=True, text=True)
    wait_no_sync_standby()
    print("REQUIRED_SYNCHRONOUS_STANDBY_UNAVAILABLE=PASS")

    timed_out = False
    with conn() as c:
        c.execute("SET statement_timeout = '5000ms'")
        c.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        c.execute(
            "INSERT INTO jf10_sync_unavailable_visibility VALUES (%s, %s)",
            (OPERATION_ID, "must-remain-private"),
        )
        try:
            c.execute(f"PREPARE TRANSACTION '{XID}'")
        except errors.QueryCanceled:
            timed_out = True
            c.execute("ROLLBACK")
    assert timed_out, "PREPARE unexpectedly completed without synchronous standby"
    print("PREPARE_BLOCKED_WITHOUT_SYNC_STANDBY=PASS")
    print("PREPARE_TIMEOUT_FAIL_CLOSED=PASS")

    with conn() as c:
        prepared = c.execute(
            "SELECT gid FROM pg_prepared_xacts WHERE gid = %s", (XID,)
        ).fetchone()
        visible = c.execute(
            "SELECT value FROM jf10_sync_unavailable_visibility WHERE operation_id = %s",
            (OPERATION_ID,),
        ).fetchone()
        sync_names = c.execute("SHOW synchronous_standby_names").fetchone()[0]
    assert prepared is None, f"unexpected prepared XID: {prepared}"
    assert visible is None, f"protected data became visible: {visible}"
    assert sync_names == "FIRST 1 (jf10_standby)", sync_names
    print("NO_LOCAL_ONLY_PREPARED_XID=PASS")
    print("NO_PROTECTED_VISIBILITY=PASS")
    print("NO_SYNCHRONOUS_COMMIT_DOWNGRADE=PASS")
    print("JF10_SYNC_STANDBY_UNAVAILABLE_FAIL_CLOSED=PASS")


if __name__ == "__main__":
    main()
