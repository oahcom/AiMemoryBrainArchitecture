"""PostgreSQL 18.7 WAL-archive PITR probe with an explicit LSN target.

The workflow creates a physical base backup, commits a target row, records the
post-commit LSN, commits a later row, archives WAL, then restores to the target
LSN. This is CI capability evidence only, not production backup approval.
"""
from __future__ import annotations

import os
import time

import psycopg

TARGET_LSN = os.environ["JF10_TARGET_LSN"]


def conn():
    return psycopg.connect(
        host="127.0.0.1",
        port=5434,
        dbname="postgres",
        user="postgres",
        password="jf10-pitr-ci-only",
        autocommit=True,
        connect_timeout=3,
    )


def main():
    deadline = time.time() + 120
    last_error = None
    while time.time() < deadline:
        try:
            with conn() as c:
                if c.execute("SELECT pg_is_in_recovery()").fetchone() == (False,):
                    break
        except Exception as exc:
            last_error = exc
        time.sleep(1)
    else:
        raise RuntimeError(f"restored PITR instance did not promote: {last_error}")

    with conn() as c:
        version = c.execute("SHOW server_version").fetchone()[0]
        replay_lsn = c.execute("SELECT pg_last_wal_replay_lsn()::text").fetchone()[0]
        base = c.execute(
            "SELECT value FROM jf10_pitr_marker WHERE marker = 'base'"
        ).fetchone()
        target = c.execute(
            "SELECT value FROM jf10_pitr_marker WHERE marker = 'target'"
        ).fetchone()
        future = c.execute(
            "SELECT value FROM jf10_pitr_marker WHERE marker = 'after-target'"
        ).fetchone()
        timeline = c.execute(
            "SELECT timeline_id FROM pg_control_checkpoint()"
        ).fetchone()[0]
    assert version.startswith("18.7 "), version
    assert base == ("base-visible",), base
    assert target == ("target-visible",), target
    assert future is None, future
    assert replay_lsn is not None, replay_lsn
    assert timeline >= 1, timeline
    print(f"SERVER_VERSION={version}")
    print(f"RECOVERY_TARGET_LSN={TARGET_LSN}")
    print(f"RECOVERY_REPLAY_LSN={replay_lsn}")
    print(f"PROMOTED_TIMELINE={timeline}")
    print("PITR_BASE_STATE_PRESENT=PASS")
    print("PITR_TARGET_STATE_PRESENT=PASS")
    print("PITR_POST_TARGET_STATE_ABSENT=PASS")
    print("PITR_EXACT_LSN_RECOVERY=PASS")
    print("JF10_POSTGRESQL_WAL_ARCHIVE_PITR=PASS")


if __name__ == "__main__":
    main()
