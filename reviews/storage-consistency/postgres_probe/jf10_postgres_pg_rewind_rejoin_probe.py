"""Verify a fenced old primary is rewound and rejoins only as a standby.

This is a PostgreSQL 18.7 CI rejoin-procedure test. The stopped container is a
test-harness fence, not production STONITH or an HA-manager certification.
"""
from __future__ import annotations

import time

import psycopg
from psycopg import errors


def connect(port: int):
    return psycopg.connect(
        host="127.0.0.1",
        port=port,
        dbname="postgres",
        user="postgres",
        password="jf10-ha-ci-only",
        autocommit=True,
        connect_timeout=3,
    )


def wait_for_rejoin(timeout: int = 120):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            with connect(5432) as c:
                recovery = c.execute("SELECT pg_is_in_recovery()").fetchone()[0]
                if recovery is True:
                    return
                last = f"old primary is not in recovery: {recovery}"
        except Exception as exc:
            last = exc
        time.sleep(1)
    raise RuntimeError(f"rewound old primary did not rejoin as standby: {last}")


def main():
    wait_for_rejoin()
    with connect(5433) as new_primary, connect(5432) as rejoined:
        assert new_primary.execute("SELECT pg_is_in_recovery()").fetchone() == (False,)
        assert rejoined.execute("SELECT pg_is_in_recovery()").fetchone() == (True,)

        expected = (
            ("after-promotion", "new-primary-write"),
            ("before-failover", "pre-failover-write"),
        )
        for marker, value in expected:
            p = new_primary.execute(
                "SELECT value FROM jf10_rejoin_marker WHERE marker = %s", (marker,)
            ).fetchone()
            s = rejoined.execute(
                "SELECT value FROM jf10_rejoin_marker WHERE marker = %s", (marker,)
            ).fetchone()
            assert p == (value,), (marker, p)
            assert s == (value,), (marker, s)

        primary_timeline = new_primary.execute(
            "SELECT timeline_id FROM pg_control_checkpoint()"
        ).fetchone()[0]
        standby_timeline = rejoined.execute(
            "SELECT timeline_id FROM pg_control_checkpoint()"
        ).fetchone()[0]
        assert primary_timeline == standby_timeline == 2, (
            primary_timeline, standby_timeline
        )

        try:
            rejoined.execute(
                "INSERT INTO jf10_rejoin_marker VALUES ('forbidden-standby-write', 'must-fail')"
            )
        except errors.ReadOnlySqlTransaction:
            print("REJOINED_OLD_PRIMARY_REJECTS_WRITES=PASS")
        else:
            raise AssertionError("rewound old primary accepted a write")

        replication = new_primary.execute(
            "SELECT state FROM pg_stat_replication"
        ).fetchone()
        assert replication == ("streaming",), replication

    print(f"NEW_PRIMARY_TIMELINE={primary_timeline}")
    print(f"REJOINED_STANDBY_TIMELINE={standby_timeline}")
    print("OLD_PRIMARY_REWOUND_TO_NEW_TIMELINE=PASS")
    print("OLD_PRIMARY_REJOINED_AS_STANDBY=PASS")
    print("PRE_FAILOVER_AND_POST_PROMOTION_DATA_REPLICATED=PASS")
    print("NO_DUAL_WRITER_AFTER_REJOIN=PASS")
    print("JF10_POSTGRESQL_PG_REWIND_REJOIN=PASS")


if __name__ == "__main__":
    main()
