# JF-10 Storage Gate A — PostgreSQL 18.7 Prepared-XID Capability Dossier

**Owner:** Storage / Consistency  
**Decision date:** 2026-11-17  
**Status:** CANDIDATE ENGINE PROFILE SELECTED FOR PHYSICAL CAPABILITY QUALIFICATION; SINGLE-NODE PREPARED-XID PROBE PASSED; PRODUCTION DEPLOYMENT / HA GATE NOT PASSED.

## 1. Candidate profile

Storage selects PostgreSQL **18.7** as the concrete candidate engine for the JF-10 Canonical Authority DB capability qualification. This is a test-profile selection, not a claim that an existing production Canonical Memory Authority deployment has already been migrated or identified.

| Dimension | Exact qualified CI profile |
|---|---|
| Engine/image | postgres:18.7 |
| Server build observed | 18.7 (Debian 18.7-1.pgdg13+2) |
| Image digest observed in CI pull log | sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc |
| Runtime | GitHub Actions ubuntu-latest, Docker container |
| Client | Python 3.12 + psycopg 3.x (psycopg[binary]>=3.2,<4) |
| max_prepared_transactions | 16 |
| fsync | on |
| synchronous_commit | on |
| full_page_writes | on |
| wal_level | replica |
| Persistence used by test | Named Docker volume mounted at /var/lib/postgresql; same container/volume restarted after SIGKILL |
| Isolation exercised | SERIALIZABLE |
| Replication topology | NONE in this probe; single node only |

The PostgreSQL 18.7 release was published on 2026-11-12. The selected minor version is pinned to avoid a floating latest tag during this capability run.

## 2. Executable probe

- Probe: reviews/storage-consistency/postgres_probe/jf10_postgres_prepared_xid_probe.py
- Probe Blob SHA: c15ea6e66a15be2fb96f737769f58b7b6c224b7e
- Workflow: .github/workflows/jf10-postgres-capability.yml
- Workflow Blob SHA: 4eef5b24f6da1d596c34e0d072dc39d5008a1a25
- Workflow run: 43907296027
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43907296027
- Run head commit: 8c9ef00364d93c383aba515923565f8dc04bf1b6
- Job ID: 133439447210
- Job conclusion: SUCCESS

The first attempt failed only because the probe compared SHOW server_version to the bare string 18.7; PostgreSQL correctly returned 18.7 (Debian 18.7-1.pgdg13+2). The assertion was corrected to require the exact 18.7 version prefix, and the rerun above passed.

## 3. Physical observations — PASS for this profile

The successful job log records:

- SERVER_VERSION=18.7 (Debian 18.7-1.pgdg13+2)
- max_prepared_transactions=16, fsync=on, synchronous_commit=on, full_page_writes=on, wal_level=replica
- A SERIALIZABLE transaction acquired a row lock, inserted both a visibility pointer and its publication receipt, and executed PREPARE TRANSACTION under one XID.
- Both rows remained invisible while the XID was prepared.
- A separate session attempting to update the locked row received lock_timeout; the prepared participant retained its row lock.
- The PostgreSQL container was killed with SIGKILL, restarted against the same named data volume, and completed crash recovery.
- pg_prepared_xacts still contained the exact original XID after restart.
- COMMIT PREPARED on that same XID made both the visibility pointer and receipt visible together.
- A second prepared XID was resolved with ROLLBACK PREPARED; neither visibility nor receipt appeared.
- The lock-retention assertion passed both before and after restart.

Machine-readable success markers:
- PREPARED_LOCK_RETENTION=PASS
- POSTMASTER_KILL_RESTART=PASS
- SAME_XID_COMMIT_AFTER_RESTART=PASS
- ATOMIC_VISIBILITY_POINTER_PLUS_RECEIPT=PASS
- SAME_XID_ROLLBACK=PASS
- ROLLBACK_NON_PUBLICATION=PASS
- JF10_POSTGRESQL_18_7_SINGLE_NODE_CAPABILITY=PASS

## 4. Storage interpretation

Storage accepts PostgreSQL 18.7 as a viable candidate for the JF-10 prepared-XID participant contract at the tested single-node engine/profile boundary:

1. PostgreSQL persists a prepared transaction so it can be resolved by a later session using the same XID.
2. The tested prepared transaction retained its row lock across a hard postmaster/container kill and restart using the same persistent volume.
3. The tested transaction kept the publication pointer and publication receipt private until the same-XID commit; both became visible after the commit.
4. Same-XID rollback produced no publication.

This is evidence of the PostgreSQL engine behavior under the exact CI profile, not evidence that the application participant adapter, I sequencer, D shared serialization domain, C provider, or COC has been implemented.

## 5. Remaining Gate A blockers — NOT PASSED

The probe does NOT test or prove:

- a synchronous standby, replication quorum, standby promotion, or prepared-XID recovery after primary loss;
- replication of prepared transaction state and locks under the intended production topology;
- backup/restore, point-in-time recovery, snapshot rollback protection, or reapplication of the current Forget control ledger before serving reads;
- persistent storage hardware guarantees, cloud volume semantics, zone loss, or production RPO/RTO;
- the actual Canonical Memory Authority deployment, migrations, connection pool, failover manager, or production runtime configuration;
- an identified human on-call/operator or production runbook;
- I sequencer recovery, COC consensus durability, provider idempotency, or end-to-end JF-10 conformance.

wal_level=replica is a configuration prerequisite only; it is not proof of a functioning replication topology.

## 6. Accountable role and next test

**Accountable technical role:** Storage DB Platform Operator (Storage Owner responsibility for the candidate profile).  
**Production on-call identity / deployment operator:** NOT YET DESIGNATED; do not infer an individual or production service from this CI role.

Next Gate A work is a two-node synchronous-replication and promotion campaign on the same pinned PostgreSQL 18.7 image, followed by backup/restore and prepared-XID recovery validation. Gate A remains OPEN until those production-relevant topology and operator conditions are satisfied.

Gate B persistent COC remains BLOCKED until Gate A passes. Gate C end-to-end fault injection remains BLOCKED until Gate B passes. JF-10 P0 remains OPEN; production activation is NOT AUTHORIZED; multi-PolicyDomain atomicity remains BLOCKED.
