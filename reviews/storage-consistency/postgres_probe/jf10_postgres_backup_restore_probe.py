"""PostgreSQL 18.7 physical backup/restore and stale-control fail-closed probe.

This is CI evidence on ephemeral Docker volumes. It verifies that a prepared
XID survives pg_basebackup restore and that an older restored Forget-control
snapshot cannot serve reads until an external newer control epoch is replayed.
"""
from __future__ import annotations

import os
import subprocess
import time

import psycopg
from psycopg import errors


IMAGE = os.environ["PG_IMAGE"]
XID = "jf10_pg187_backup_restore_commit_001"
OPERATION_ID = "op-prepared-survives-backup"
FORGOTTEN_ID = "artifact-forgotten-after-backup"
SAFE_ID = "artifact-still-authorized"
REQUIRED_AUTHORITY_EPOCH = 1


def conn(port: int):
    return psycopg.connect(
        host="127.0.0.1",
        port=port,
        dbname="postgres",
        user="postgres",
        password="jf10-restore-ci-only",
        autocommit=True,
        connect_timeout=3,
    )


def wait_db(port: int, timeout: int = 90):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            with conn(port) as c:
                c.execute("SELECT 1")
            return
        except Exception as exc:
            last = exc
            time.sleep(1)
    raise RuntimeError(f"PostgreSQL port {port} did not become ready: {last}")


def docker(*args: str):
    subprocess.run(["docker", *args], check=True)


def setup_primary():
    with conn(5432) as c:
        version = c.execute("SHOW server_version").fetchone()[0]
        settings = {
            key: c.execute("SHOW " + key).fetchone()[0]
            for key in ("max_prepared_transactions", "fsync", "synchronous_commit", "full_page_writes")
        }
        assert version.startswith("18.7 "), version
        assert settings == {
            "max_prepared_transactions": "16",
            "fsync": "on",
            "synchronous_commit": "on",
            "full_page_writes": "on",
        }, settings
        c.execute("DROP TABLE IF EXISTS jf10_restore_receipt")
        c.execute("DROP TABLE IF EXISTS jf10_restore_visibility")
        c.execute("DROP TABLE IF EXISTS jf10_restore_control")
        c.execute("DROP TABLE IF EXISTS jf10_restore_lock")
        c.execute("CREATE TABLE jf10_restore_lock (id integer PRIMARY KEY, marker text NOT NULL)")
        c.execute("INSERT INTO jf10_restore_lock VALUES (1, 'prepared-xid-lock')")
        c.execute(
            "CREATE TABLE jf10_restore_visibility "
            "(operation_id text PRIMARY KEY, visibility_pointer text NOT NULL)"
        )
        c.execute(
            "CREATE TABLE jf10_restore_receipt "
            "(operation_id text PRIMARY KEY, receipt_digest text NOT NULL)"
        )
        c.execute(
            "CREATE TABLE jf10_restore_control "
            "(singleton boolean PRIMARY KEY DEFAULT true CHECK (singleton), "
            "ledger_epoch bigint NOT NULL, serving_enabled boolean NOT NULL)"
        )
        c.execute(
            "INSERT INTO jf10_restore_control(singleton, ledger_epoch, serving_enabled) "
            "VALUES (true, 0, true)"
        )
        c.execute(
            "INSERT INTO jf10_restore_visibility VALUES (%s, %s), (%s, %s)",
            (
                FORGOTTEN_ID, "private-staged-object:" + FORGOTTEN_ID,
                SAFE_ID, "private-staged-object:" + SAFE_ID,
            ),
        )
        c.execute(
            "INSERT INTO jf10_restore_receipt VALUES (%s, %s), (%s, %s)",
            (
                FORGOTTEN_ID, "sha256:" + FORGOTTEN_ID,
                SAFE_ID, "sha256:" + SAFE_ID,
            ),
        )
        c.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        c.execute("SELECT id FROM jf10_restore_lock WHERE id = 1 FOR UPDATE")
        c.execute(
            "INSERT INTO jf10_restore_visibility VALUES (%s, %s)",
            (OPERATION_ID, "private-staged-object:" + OPERATION_ID),
        )
        c.execute(
            "INSERT INTO jf10_restore_receipt VALUES (%s, %s)",
            (OPERATION_ID, "sha256:" + OPERATION_ID),
        )
        c.execute(f"PREPARE TRANSACTION '{XID}'")
    print(f"PRIMARY_VERSION={version}")
    print(f"PRIMARY_SETTINGS={settings}")
    print(f"PRIMARY_PREPARED_XID={XID}")


def create_physical_backup_and_restore():
    docker("volume", "create", "jf10-restore-data")
    docker(
        "run", "--rm", "--user", "root",
        "-v", "jf10-restore-data:/var/lib/postgresql",
        "--entrypoint", "bash", IMAGE, "-lc",
        "chown -R postgres:postgres /var/lib/postgresql",
    )
    docker(
        "run", "--rm", "--user", "postgres", "--network", "jf10-restore-net",
        "-v", "jf10-restore-data:/var/lib/postgresql",
        "--entrypoint", "bash", IMAGE, "-lc",
        "mkdir -p /var/lib/postgresql/18/docker && "
        "pg_basebackup -d 'host=jf10-primary user=postgres' "
        "-D /var/lib/postgresql/18/docker -Fp -Xs -P",
    )
    print("PG_BASEBACKUP_PHYSICAL_COPY=PASS")
    docker(
        "run", "-d", "--name", "jf10-restore", "--network", "jf10-restore-net",
        "-e", "POSTGRES_PASSWORD=jf10-restore-ci-only",
        "-e", "POSTGRES_HOST_AUTH_METHOD=trust",
        "-p", "5434:5432",
        "-v", "jf10-restore-data:/var/lib/postgresql",
        IMAGE,
        "-c", "max_prepared_transactions=16",
        "-c", "fsync=on",
        "-c", "synchronous_commit=on",
        "-c", "full_page_writes=on",
    )
    wait_db(5434)
    print("PHYSICAL_BACKUP_RESTORE_STARTUP=PASS")


def read_artifact(operation_id: str):
    with conn(5434) as c:
        gate = c.execute(
            "SELECT ledger_epoch, serving_enabled FROM jf10_restore_control WHERE singleton=true"
        ).fetchone()
        if not gate[1] or gate[0] < REQUIRED_AUTHORITY_EPOCH:
            raise PermissionError(
                f"restore gate closed: local_epoch={gate[0]}, required_epoch={REQUIRED_AUTHORITY_EPOCH}"
            )
        return c.execute(
            "SELECT visibility_pointer FROM jf10_restore_visibility WHERE operation_id=%s",
            (operation_id,),
        ).fetchone()


def assert_stale_restore_fails_closed():
    with conn(5434) as c:
        local_epoch, serving_enabled = c.execute(
            "SELECT ledger_epoch, serving_enabled FROM jf10_restore_control WHERE singleton=true"
        ).fetchone()
    assert local_epoch == 0 and serving_enabled is True, (local_epoch, serving_enabled)
    try:
        read_artifact(FORGOTTEN_ID)
    except PermissionError:
        print("STALE_RESTORE_READ_GATE_CLOSED=PASS")
    else:
        raise AssertionError("stale restored snapshot served data before authority reconciliation")
    with conn(5434) as c:
        prepared = c.execute(
            "SELECT gid FROM pg_prepared_xacts WHERE gid=%s", (XID,)
        ).fetchone()
        assert prepared == (XID,), f"prepared XID missing after restore: {prepared}"
        assert c.execute(
            "SELECT 1 FROM jf10_restore_visibility WHERE operation_id=%s",
            (OPERATION_ID,),
        ).fetchone() is None
    print("PREPARED_XID_SURVIVES_PHYSICAL_BACKUP_RESTORE=PASS")


def apply_current_authoritative_control_and_resolve():
    # This row represents the current authoritative Forget-control ledger
    # fetched from outside the restored DB; it is deliberately newer than
    # the snapshot's local ledger epoch.
    with conn(5434) as c:
        c.execute("BEGIN")
        c.execute(
            "DELETE FROM jf10_restore_visibility WHERE operation_id=%s",
            (FORGOTTEN_ID,),
        )
        c.execute(
            "DELETE FROM jf10_restore_receipt WHERE operation_id=%s",
            (FORGOTTEN_ID,),
        )
        c.execute(
            "UPDATE jf10_restore_control SET ledger_epoch=%s, serving_enabled=true "
            "WHERE singleton=true",
            (REQUIRED_AUTHORITY_EPOCH,),
        )
        c.execute("COMMIT")
    assert read_artifact(FORGOTTEN_ID) is None
    safe = read_artifact(SAFE_ID)
    assert safe == ("private-staged-object:" + SAFE_ID,), safe
    print("CURRENT_FORGET_CONTROL_REPLAY_BEFORE_READS=PASS")
    print("FORGOTTEN_ARTIFACT_SUPPRESSED_AFTER_RESTORE=PASS")
    print("UNRELATED_ARTIFACT_REMAINS_READABLE=PASS")

    with conn(5434) as c:
        c.execute(f"COMMIT PREPARED '{XID}'")
    with conn(5434) as c:
        pointer = c.execute(
            "SELECT visibility_pointer FROM jf10_restore_visibility WHERE operation_id=%s",
            (OPERATION_ID,),
        ).fetchone()
        receipt = c.execute(
            "SELECT receipt_digest FROM jf10_restore_receipt WHERE operation_id=%s",
            (OPERATION_ID,),
        ).fetchone()
    assert pointer == ("private-staged-object:" + OPERATION_ID,), pointer
    assert receipt == ("sha256:" + OPERATION_ID,), receipt
    print("SAME_XID_COMMIT_AFTER_RESTORE=PASS")
    print("RESTORED_PREPARED_VISIBILITY_POINTER_PLUS_RECEIPT=PASS")


if __name__ == "__main__":
    setup_primary()
    create_physical_backup_and_restore()
    assert_stale_restore_fails_closed()
    apply_current_authoritative_control_and_resolve()
    print("JF10_POSTGRESQL_18_7_BACKUP_RESTORE_CAPABILITY=PASS")
    print("LIMITATION=CI_VOLUMES_AND_TEST_FIXTURE_CONTROL_LEDGER_NOT_PRODUCTION_BACKUP_SERVICE")
