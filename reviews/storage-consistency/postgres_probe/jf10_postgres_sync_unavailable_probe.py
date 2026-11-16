"""Fail-closed test when the required synchronous standby disappears.

The protected PREPARE is issued in a separate backend. The probe verifies that
the backend is blocked specifically on SyncRep, then terminates that backend
and proves no prepared XID or visibility escaped. PostgreSQL 18.7 CI only.
"""
from __future__ import annotations

import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import psycopg

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
    )


def prepare_in_backend(ready: threading.Event, pid_box: list[int]):
    with conn() as c:
        c.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        c.execute(
            "INSERT INTO jf10_sync_unavailable_visibility VALUES (%s, %s)",
            (OPERATION_ID, "must-remain-private"),
        )
        pid_box.append(c.execute("SELECT pg_backend_pid()").fetchone()[0])
        ready.set()
        c.execute(f"PREPARE TRANSACTION '{XID}'")


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

    subprocess.run(["docker", "stop", "jf10-standby"], check=True, capture_output=True, text=True)
    deadline = time.time() + 30
    while time.time() < deadline:
        with conn() as c:
            count = c.execute(
                "SELECT count(*) FROM pg_stat_replication WHERE sync_state = 'sync'"
            ).fetchone()[0]
        if count == 0:
            break
        time.sleep(0.25)
    else:
        raise AssertionError("required synchronous standby remained connected")
    print("REQUIRED_SYNCHRONOUS_STANDBY_UNAVAILABLE=PASS")

    ready = threading.Event()
    pid_box: list[int] = []
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(prepare_in_backend, ready, pid_box)
        assert ready.wait(timeout=10), "PREPARE backend did not start"
        pid = pid_box[0]
        wait_event = None
        deadline = time.time() + 15
        while time.time() < deadline:
            with conn() as c:
                row = c.execute(
                    "SELECT wait_event_type, wait_event FROM pg_stat_activity WHERE pid = %s",
                    (pid,),
                ).fetchone()
            if future.done():
                raise AssertionError(
                    "PREPARE completed or failed before SyncRep wait was observed"
                )
            if row and row[1] == "SyncRep":
                wait_event = row
                break
            time.sleep(0.2)
        assert wait_event == ("IPC", "SyncRep"), wait_event
        print(f"PREPARE_WAIT_EVENT={wait_event}")
        print("PREPARE_BLOCKED_ON_SYNCHRONOUS_REPLICATION=PASS")

        with conn() as c:
            terminated = c.execute(
                "SELECT pg_terminate_backend(%s)", (pid,)
            ).fetchone()[0]
        assert terminated is True, "could not terminate blocked PREPARE backend"
        try:
            future.result(timeout=10)
        except psycopg.Error:
            print("BLOCKED_PREPARE_BACKEND_TERMINATED=PASS")
        else:
            raise AssertionError("terminated PREPARE backend returned successfully")

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
