"""JF-10 PITR atomicity and WAL-corruption negative probes.

All jf10_* tables are an isolated Storage protocol fixture, not production COC
or I/D tables. The test verifies PostgreSQL prepared-XID recovery and atomic
VisibilityPointer/PublicationReceipt visibility at explicit PITR boundaries.
"""
from __future__ import annotations

import os
import subprocess
import time
import uuid

import psycopg

IMAGE = os.environ["PG_IMAGE"]
NETWORK = "jf10-pitr-atomicity-net"
PRIMARY = "jf10-pitr-atomicity-primary"
BACKUP_VOL = "jf10-pitr-atomicity-backup"
ARCHIVE_VOL = "jf10-pitr-atomicity-archive"
PASSWORD = "jf10-pitr-atomicity-ci-only"


def sh(*args: str, check: bool = True, capture: bool = True) -> str:
    p = subprocess.run(args, check=check, text=True, stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.STDOUT if capture else None)
    return (p.stdout or "").strip()


def docker(*args: str, check: bool = True) -> str:
    return sh("docker", *args, check=check)


def psql(sql: str, host: str = PRIMARY, port: int = 5432) -> str:
    with psycopg.connect(host="127.0.0.1", port=port, dbname="postgres",
                         user="postgres", password=PASSWORD, autocommit=True,
                         connect_timeout=3) as c:
        cur = c.execute(sql)
        return "\n".join(str(r) for r in cur.fetchall()) if cur.description else ""


def scalar(sql: str) -> str:
    with psycopg.connect(host="127.0.0.1", port=5432, dbname="postgres",
                         user="postgres", password=PASSWORD, autocommit=True,
                         connect_timeout=3) as c:
        return str(c.execute(sql).fetchone()[0])


def wait_primary(name: str, port: int, timeout: int = 120) -> None:
    end = time.time() + timeout
    last = ""
    while time.time() < end:
        try:
            with psycopg.connect(host="127.0.0.1", port=port, dbname="postgres",
                                 user="postgres", password=PASSWORD, connect_timeout=2) as c:
                if not c.execute("SELECT pg_is_in_recovery()").fetchone()[0]:
                    return
        except Exception as e:
            last = str(e)
        time.sleep(1)
    raise RuntimeError(f"{name} did not promote: {last}")


def clone_volume(source: str, destination: str, mount: str) -> None:
    docker("volume", "create", destination)
    docker("run", "--rm", "--user", "root", "-v", f"{source}:{mount}",
           "-v", f"{destination}:/dest", "--entrypoint", "bash", IMAGE,
           "-lc", f"cp -a {mount}/. /dest/ && chown -R postgres:postgres /dest")


def copy_archive(destination: str) -> None:
    docker("volume", "create", destination)
    docker("run", "--rm", "--user", "root", "-v", f"{ARCHIVE_VOL}:/src",
           "-v", f"{destination}:/dest", "--entrypoint", "bash", IMAGE,
           "-lc", "cp -a /src/. /dest/ && chown -R postgres:postgres /dest")


def start_restore(label: str, target_lsn: str, data_vol: str, wal_vol: str, port: int) -> str:
    name = f"jf10-pitr-atomicity-{label}"
    docker("run", "-d", "--name", name, "--network", NETWORK,
           "-e", f"POSTGRES_PASSWORD={PASSWORD}", "-p", f"{port}:5432",
           "-v", f"{data_vol}:/var/lib/postgresql", "-v", f"{wal_vol}:/archive",
           IMAGE, "-c", "max_prepared_transactions=16", "-c", "wal_level=replica",
           "-c", "fsync=on", "-c", "full_page_writes=on",
           "-c", "restore_command=cp /archive/%f %p",
           "-c", f"recovery_target_lsn={target_lsn}",
           "-c", "recovery_target_action=promote",
           "-c", "recovery_target_timeline=latest")
    return name


def wait_recovery(port: int, promoted: bool, timeout: int = 120) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with psycopg.connect(host="127.0.0.1", port=port, dbname="postgres",
                                 user="postgres", password=PASSWORD, connect_timeout=2) as c:
                in_recovery = c.execute("SELECT pg_is_in_recovery()").fetchone()[0]
                if not in_recovery:
                    return True
        except Exception:
            pass
        time.sleep(1)
    return False


def restore_query(port: int, sql: str):
    with psycopg.connect(host="127.0.0.1", port=port, dbname="postgres",
                         user="postgres", password=PASSWORD, connect_timeout=5) as c:
        return c.execute(sql).fetchall()


def main() -> None:
    docker("network", "create", NETWORK)
    docker("volume", "create", BACKUP_VOL)
    docker("volume", "create", ARCHIVE_VOL)
    docker("run", "--rm", "--user", "root", "-v", f"{BACKUP_VOL}:/var/lib/postgresql",
           "--entrypoint", "bash", IMAGE, "-lc", "chown -R postgres:postgres /var/lib/postgresql")
    docker("run", "--rm", "--user", "root", "-v", f"{ARCHIVE_VOL}:/archive",
           "--entrypoint", "bash", IMAGE, "-lc", "chown -R postgres:postgres /archive")
    docker("run", "-d", "--name", PRIMARY, "--network", NETWORK, "-p", "5432:5432",
           "-e", f"POSTGRES_PASSWORD={PASSWORD}", "-e", "POSTGRES_HOST_AUTH_METHOD=trust",
           "-v", f"{ARCHIVE_VOL}:/archive", IMAGE,
           "-c", "max_prepared_transactions=16", "-c", "wal_level=replica",
           "-c", "max_wal_senders=10", "-c", "fsync=on", "-c", "full_page_writes=on",
           "-c", "archive_mode=on", "-c", "archive_timeout=1s",
           "-c", "archive_command=test ! -f /archive/%f && cp %p /archive/%f")
    end = time.time() + 90
    while time.time() < end:
        try:
            psql("SELECT 1")
            break
        except Exception:
            time.sleep(1)
    else:
        raise RuntimeError(docker("logs", PRIMARY, check=False))

    psql("""CREATE TABLE jf10_visibility_pointer (
        xid_name text PRIMARY KEY, artifact_id text NOT NULL, state text NOT NULL
    )""")
    psql("""CREATE TABLE jf10_publication_receipt (
        xid_name text PRIMARY KEY, artifact_id text NOT NULL, receipt text NOT NULL
    )""")

    xid_commit = "jf10-pitr-commit-" + uuid.uuid4().hex[:12]
    xid_rollback = "jf10-pitr-rollback-" + uuid.uuid4().hex[:12]
    for xid in (xid_commit, xid_rollback):
        with psycopg.connect(host="127.0.0.1", port=5432, dbname="postgres",
                             user="postgres", password=PASSWORD, autocommit=True) as c:
            c.execute("BEGIN")
            c.execute("INSERT INTO jf10_visibility_pointer VALUES (%s, %s, 'VISIBLE')",
                      (xid, f"artifact-{xid}"))
            c.execute("INSERT INTO jf10_publication_receipt VALUES (%s, %s, %s)",
                      (xid, f"artifact-{xid}", f"receipt-{xid}"))
            c.execute("PREPARE TRANSACTION %s", (xid,))
    prepared = psql("SELECT gid FROM pg_prepared_xacts ORDER BY gid")
    assert xid_commit in prepared and xid_rollback in prepared, prepared
    print("PREPARED_XIDS_CREATED=PASS")

    # Base backup captures both prepared XIDs before either terminal decision.
    docker("run", "--rm", "--user", "postgres", "--network", NETWORK,
           "-v", f"{BACKUP_VOL}:/var/lib/postgresql", "--entrypoint", "bash", IMAGE,
           "-lc", "mkdir -p /var/lib/postgresql/18/docker && pg_basebackup "
                 f"-h {PRIMARY} -U postgres -D /var/lib/postgresql/18/docker -Fp -Xs -P",
           check=True)
    psql("SELECT pg_switch_wal()")
    prepared_lsn = scalar("SELECT pg_current_wal_lsn()")
    prepared_wal = scalar(f"SELECT pg_walfile_name('{prepared_lsn}'::pg_lsn)")
    psql(f"COMMIT PREPARED '{xid_commit}'")
    psql("SELECT pg_switch_wal()")
    commit_lsn = scalar("SELECT pg_current_wal_lsn()")
    psql(f"ROLLBACK PREPARED '{xid_rollback}'")
    psql("SELECT pg_switch_wal()")
    rollback_lsn = scalar("SELECT pg_current_wal_lsn()")
    for _ in range(120):
        try:
            docker("exec", PRIMARY, "bash", "-lc", f"test -f /archive/{prepared_wal}")
            break
        except subprocess.CalledProcessError:
            time.sleep(1)
    else:
        raise RuntimeError("prepared-boundary WAL segment was not archived")
    print(f"PREPARED_BOUNDARY_LSN={prepared_lsn}")
    print(f"COMMIT_BOUNDARY_LSN={commit_lsn}")
    print(f"ROLLBACK_BOUNDARY_LSN={rollback_lsn}")
    print("PREPARED_BOUNDARY_WAL_ARCHIVED=PASS")

    docker("stop", PRIMARY)
    cases = [
        ("prepared", prepared_lsn, 5541),
        ("committed", commit_lsn, 5542),
        ("rolledback", rollback_lsn, 5543),
    ]
    results = {}
    for label, target, port in cases:
        data = f"jf10-pitr-atomicity-{label}-data"
        wal = f"jf10-pitr-atomicity-{label}-wal"
        clone_volume(BACKUP_VOL, data, "/backup")
        copy_archive(wal)
        start_restore(label, target, data, wal, port)
        if not wait_recovery(port, True):
            raise RuntimeError(docker("logs", f"jf10-pitr-atomicity-{label}", check=False)[-5000:])
        results[label] = restore_query(port, """
            SELECT (SELECT count(*) FROM pg_prepared_xacts),
                   (SELECT count(*) FROM jf10_visibility_pointer),
                   (SELECT count(*) FROM jf10_publication_receipt)
        """)[0]
        if label == "prepared":
            gids = restore_query(port, "SELECT gid FROM pg_prepared_xacts")
            assert xid_commit in str(gids) and xid_rollback in str(gids), gids
            assert results[label][1:] == (0, 0), results[label]
            locks = restore_query(port, "SELECT count(*) FROM pg_locks WHERE locktype='transactionid'")
            assert locks[0][0] >= 2, locks
            print("PITR_PREPARED_XID_PRIVATE_AND_LOCKED=PASS")
        elif label == "committed":
            assert restore_query(port, f"SELECT count(*) FROM jf10_visibility_pointer WHERE xid_name='{xid_commit}'")[0][0] == 1
            assert restore_query(port, f"SELECT count(*) FROM jf10_publication_receipt WHERE xid_name='{xid_commit}'")[0][0] == 1
            assert xid_rollback in str(restore_query(port, "SELECT gid FROM pg_prepared_xacts"))
            assert results[label][1:] == (1, 1), results[label]
            print("PITR_COMMIT_POINTER_AND_RECEIPT_ATOMIC=PASS")
        else:
            assert results[label][0] == 0, results[label]
            assert restore_query(port, f"SELECT count(*) FROM jf10_visibility_pointer WHERE xid_name='{xid_rollback}'")[0][0] == 0
            assert restore_query(port, f"SELECT count(*) FROM jf10_publication_receipt WHERE xid_name='{xid_rollback}'")[0][0] == 0
            assert results[label][1:] == (1, 1), results[label]
            print("PITR_ROLLBACK_NO_POINTER_NO_RECEIPT=PASS")
    print("JF10_PITR_PREPARED_XID_VISIBILITY_RECEIPT_BOUNDARIES=PASS")

    # Negative archive probes: remove, corrupt, or truncate the segment needed
    # to cross the prepared boundary. Recovery must never promote to writable.
    for idx, mode in enumerate(("missing", "corrupt", "incomplete"), start=1):
        label = f"negative-{mode}"
        data = f"jf10-pitr-atomicity-{label}-data"
        wal = f"jf10-pitr-atomicity-{label}-wal"
        clone_volume(BACKUP_VOL, data, "/backup")
        copy_archive(wal)
        target_wal = prepared_wal
        # Remove the target segment from both backup pg_wal and archive for all
        # modes, ensuring restore cannot silently use a copy in the base backup.
        docker("run", "--rm", "--user", "root", "-v", f"{data}:/data", "-v", f"{wal}:/archive",
               "--entrypoint", "bash", IMAGE, "-lc",
               f"rm -f /data/18/docker/pg_wal/{target_wal}")
        if mode == "missing":
            docker("run", "--rm", "--user", "root", "-v", f"{wal}:/archive",
                   "--entrypoint", "bash", IMAGE, "-lc", f"rm -f /archive/{target_wal}")
        elif mode == "corrupt":
            docker("run", "--rm", "--user", "root", "-v", f"{wal}:/archive",
                   "--entrypoint", "bash", IMAGE, "-lc",
                   f"test -f /archive/{target_wal} && printf X | dd of=/archive/{target_wal} bs=1 seek=0 conv=notrunc")
        else:
            docker("run", "--rm", "--user", "root", "-v", f"{wal}:/archive",
                   "--entrypoint", "bash", IMAGE, "-lc",
                   f"test -f /archive/{target_wal} && truncate -s 8192 /archive/{target_wal}")
        port = 5550 + idx
        name = start_restore(label, rollback_lsn, data, wal, port)
        promoted = wait_recovery(port, True, timeout=35)
        if promoted:
            raise AssertionError(f"{mode} WAL archive unexpectedly promoted to writable")
        logs = docker("logs", name, check=False)
        assert any(s in logs.lower() for s in ("restore", "wal", "invalid", "could not", "failed")), logs[-4000:]
        print(f"PITR_{mode.upper()}_WAL_FAILS_CLOSED=PASS")
    print("JF10_PITR_WAL_NEGATIVE_CASES=PASS")
    print("SCOPE=ISOLATED_STORAGE_FIXTURE_NOT_PRODUCTION_COC_OR_ID_LEDGER")
    print("JF10_POSTGRESQL_PITR_ATOMICITY_AND_NEGATIVES=PASS")


if __name__ == "__main__":
    main()
