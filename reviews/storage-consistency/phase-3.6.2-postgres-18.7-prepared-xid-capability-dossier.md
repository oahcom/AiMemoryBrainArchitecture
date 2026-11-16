# JF-10 Storage Gate A — PostgreSQL 18.7 Prepared-XID Capability Dossier


## Current Gate A summary — controlling status (2026-11-17)

This summary supersedes historical interim status and “next test” statements in earlier sections.

**CI capability subtests PASS for the pinned PostgreSQL 18.7 profile:**
1. Single-node prepared-XID persistence, lock retention, hard restart, same-XID commit/rollback.
2. Two-node synchronous WAL replay, primary loss, standby promotion, same-XID commit/rollback.
3. Physical pg_basebackup/restore with stale-control fail-closed fixture.
4. Coordinator process crash in the participant-success / ACK-checkpoint gap.
5. TCP CommandComplete response loss after PREPARE / COMMIT PREPARED / ROLLBACK PREPARED.
6. Required synchronous standby unavailable: PREPARE waits on SyncRep; client outcome UNKNOWN; local prepared XID and lock remain; visibility remains private.
7. WAL-archive PITR to explicit LSN; target state restored, post-target state excluded.

**Still OPEN for Gate A:** production Canonical Authority deployment and DB profile NOT DESIGNATED; production I/D control-ledger integration; production old-primary fencing/STONITH, rejoin control and split-brain prevention beyond the CI pg_rewind rejoin procedure; production host/zone/cloud-volume durability and failover routing/monitoring; backup archive retention and operational restore governance; named production operator/on-call, approved runbook, RPO/RTO and operational acceptance.

Gate A remains PARTIAL PASS / OPEN. Gate B remains BLOCKED until Gate A acceptance; Gate C remains BLOCKED until Gate B acceptance; JF-10 P0 remains OPEN; production activation is NOT AUTHORIZED.

**Owner:** Storage / Consistency  
**Decision date:** 2026-11-17  
**Status:** POSTGRESQL 18.7 CI CAPABILITY PROFILE QUALIFIED ACROSS PREPARED-XID, SYNC FAILOVER, ACK-LOSS, STANDBY-UNAVAILABLE UNKNOWN, PHYSICAL RESTORE AND WAL PITR SUBTESTS; PRODUCTION DEPLOYMENT / FENCING / OPERATIONS NOT ACCEPTED.

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

## 5. Scope limitations of the original single-node probe (historical; later evidence in §§7–18)

The probe does NOT test or prove:

- a synchronous standby, replication quorum, standby promotion, or prepared-XID recovery after primary loss;
- replication of prepared transaction state and locks under the intended production topology;
- backup/restore, point-in-time recovery, snapshot rollback protection, or reapplication of the current Forget control ledger before serving reads;
- persistent storage hardware guarantees, cloud volume semantics, zone loss, or production RPO/RTO;
- the actual Canonical Memory Authority deployment, migrations, connection pool, failover manager, or production runtime configuration;
- an identified human on-call/operator or production runbook;
- I sequencer recovery, COC consensus durability, provider idempotency, or end-to-end JF-10 conformance.

wal_level=replica is a configuration prerequisite only; it is not proof of a functioning replication topology.

## 6. Accountable role and current production boundary

**Accountable technical role:** Storage DB Platform Operator (Storage Owner responsibility for the candidate qualification profile).  
**Production Canonical Authority deployment / DB profile:** NOT DESIGNATED.  
**Production on-call identity / deployment operator:** NOT YET DESIGNATED; do not infer an individual or production service from this CI role.

The pinned PostgreSQL 18.7 CI profile has since passed the two-node sync failover, same-XID commit/rollback after promotion, physical pg_basebackup restore, coordinator ACK-gap, TCP ACK-loss, required-standby-unavailable UNKNOWN/private/lock-retention, and WAL-archive PITR subtests (§§7–18). Remaining Gate A work is production binding, old-primary fencing/rejoin and split-brain prevention, production I/D ledger integration, infrastructure durability/routing/monitoring, and approved operator/runbook/RPO/RTO evidence.

Gate B persistent COC remains BLOCKED until full Gate A acceptance. Gate C end-to-end fault injection remains BLOCKED until Gate B passes. JF-10 P0 remains OPEN; production activation is NOT AUTHORIZED; multi-PolicyDomain atomicity remains BLOCKED.


## 7. Two-node synchronous replication and primary-loss recovery — PASS (CI)

A second physical workflow now qualifies the pinned PostgreSQL 18.7 image in a two-node primary/standby topology.

Exact evidence:
- Probe: reviews/storage-consistency/postgres_probe/jf10_postgres_sync_failover_probe.py
- Probe Blob: 23d8ea8546932e592093c5c17cd2b52f8a294720
- Workflow: .github/workflows/jf10-postgres-ha-capability.yml
- Workflow Blob: f3c05f90c6065458b49879def10dce672685c850
- Image: postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc
- Run: 43908428220
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43908428220
- Run head commit: 7cd416a1f80364fe7de316f19716325b6503cbfa
- Job ID: 133443444760
- Job conclusion: SUCCESS

Exact topology/configuration:
- One primary and one physical streaming standby on a dedicated Docker network, both using the same pinned image digest.
- Primary: max_prepared_transactions=16, wal_level=replica, max_wal_senders=10, max_replication_slots=10, synchronous_commit=remote_apply, fsync=on, full_page_writes=on.
- Standby application_name: jf10_standby.
- Primary synchronous_standby_names: FIRST 1 (jf10_standby).
- The workflow waited for pg_stat_replication to report state=streaming and sync_state=sync before preparing the participant.
- Both nodes use separate named Docker volumes.

Observed PASS markers from the raw job log:
- SYNCHRONOUS_STANDBY=('jf10_standby', 'streaming', 'sync')
- SYNCHRONOUS_STANDBY_PREPARED_WAL_REPLAY=PASS
- HOT_STANDBY_PREPARED_XACT_VIEW_HIDDEN_AS_DOCUMENTED=PASS
- PRIMARY_HARD_KILL=PASS
- STANDBY_PROMOTION=PASS
- PREPARED_LOCK_RETAINED_ON_127_0_0_1=PASS
- PREPARED_XID_REPLAYED_TO_SYNC_STANDBY=PASS
- SAME_XID_COMMIT_AFTER_PRIMARY_LOSS=PASS
- ATOMIC_VISIBILITY_AFTER_PROMOTION=PASS
- JF10_POSTGRESQL_18_7_SYNC_FAILOVER_CAPABILITY=PASS

The exact XID was prepared on the primary only after the standby was confirmed synchronous with remote_apply. The standby replayed the prepared WAL while keeping the publication pointer and receipt private. PostgreSQL hot standby intentionally reports no pg_prepared_xacts rows during recovery; after primary hard-kill and standby promotion, the exact prepared XID was visible and resolvable. The promoted server retained the row lock. COMMIT PREPARED on the original XID exposed VisibilityPointer and PublicationReceipt together.

## 8. Updated Gate A disposition

**Gate A is now materially advanced: single-node crash/restart and two-node synchronous standby promotion/recovery are both physically demonstrated for the pinned PostgreSQL 18.7 CI topology. Gate A remains OPEN / PARTIAL PASS.**

Still NOT VERIFIED:
- same-XID ROLLBACK PREPARED after promotion (rollback is proven only by the single-node probe so far);
- backup/restore and point-in-time recovery, including Forget-control-ledger replay before any restored data is served;
- zone/host loss and persistent storage behavior outside ephemeral GitHub-hosted Docker volumes;
- actual production Canonical Authority DB deployment, network/security profile, connection pool, failover manager and runbook;
- named human production on-call/operator, RPO/RTO and operational ownership.

The two-node workflow uses a simple CI promotion command and does not validate a production-grade fencing/STONITH system, quorum manager, split-brain prevention, DNS/connection routing, or external I sequencer decision log. No production HA approval is implied.

Next Gate A action: add rollback-after-promotion and backup/restore recovery evidence, then identify the actual deployment and human operator. Gate B remains blocked until Gate A passes; Gate C remains blocked until Gate B passes.


## 9. Same-XID rollback after primary-loss promotion — PASS (2026-11-17)

The two-node probe was extended to prepare two independent participants on the primary before failover:
- XID jf10_pg187_sync_failover_commit_001 — resolved by COMMIT PREPARED after promotion.
- XID jf10_pg187_sync_failover_rollback_001 — resolved by ROLLBACK PREPARED after promotion.

The participants used distinct serialization-guard rows and distinct operation IDs. Both prepared XIDs were synchronously WAL-replayed to the standby. After primary SIGKILL and standby promotion, both exact XIDs were present in pg_prepared_xacts; both locks remained held. The promoted standby committed the first XID and rolled back the second. The first participant exposed pointer + receipt together; the second exposed neither.

Updated exact evidence:
- Probe Blob: cbe1f317479145dbf1467e426b0c0737a6ec054c
- Workflow Blob: f3c05f90c6065458b49879def10dce672685c850
- Successful run: 43908746695
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43908746695
- Run head commit: b59c0842dba86b581ded4d9519c4289b6a699fde
- Job ID: 133444572245
- Job conclusion: SUCCESS

Additional raw-log markers:
- SAME_XID_ROLLBACK_AFTER_PRIMARY_LOSS=PASS
- ROLLBACK_NON_PUBLICATION_AFTER_PROMOTION=PASS

This supersedes the prior §8 open item “same-XID ROLLBACK PREPARED after promotion”. That item is now PASS for the pinned two-node CI profile.

## 10. Gate A remaining blockers after commit + rollback failover proof

**Gate A remains PARTIAL PASS / OPEN.** The pinned CI profile now proves:
- single-node hard restart with same-XID commit and rollback;
- two-node synchronous prepared-WAL replay;
- primary hard loss and standby promotion;
- same-XID commit and rollback after promotion;
- retained prepared locks;
- atomic publication pointer + receipt visibility and rollback non-publication.

Still NOT VERIFIED:
- physical backup/restore and point-in-time recovery;
- restoration of an older snapshot while a newer Forget fence/participant decision exists, and mandatory control-ledger reconciliation before serving any read;
- real host/zone/storage failure and durability semantics beyond ephemeral Docker volumes;
- production failover fencing/STONITH, quorum manager, split-brain prevention, routing and reconnect behavior;
- actual Canonical Authority deployment profile and named human production on-call/operator, runbook, RPO/RTO.

Gate B remains blocked until the remaining Gate A conditions pass; Gate C remains blocked until Gate B.


## 11. Physical backup/restore, prepared-XID recovery and stale-control fail-closed — PASS (2026-11-17)

Storage added a physical pg_basebackup/restore probe using the same pinned PostgreSQL 18.7 image digest. It deliberately takes a physical backup while one XID is prepared and while a previously visible artifact remains in a stale snapshot. After restore, it verifies the old control-ledger epoch blocks all reads until the newer authoritative Forget-control epoch is replayed.

Exact evidence:
- Probe: reviews/storage-consistency/postgres_probe/jf10_postgres_backup_restore_probe.py
- Probe Blob: 81072ea2411af12f29c7a7a4d984df3f870321ca
- Workflow: .github/workflows/jf10-postgres-restore-capability.yml
- Workflow Blob: 38369ed197665c4ed99a9ba30602cb5e3b04ba75
- Pinned image: postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc
- Successful run: 43909138634
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43909138634
- Run head commit: 62033b9f90a28c4afdea07fafa0f575342b084e9
- Job ID: 133445937783
- Job conclusion: SUCCESS

Observed PASS markers:
- PG_BASEBACKUP_PHYSICAL_COPY=PASS
- PHYSICAL_BACKUP_RESTORE_STARTUP=PASS
- STALE_RESTORE_READ_GATE_CLOSED=PASS
- PREPARED_XID_SURVIVES_PHYSICAL_BACKUP_RESTORE=PASS
- CURRENT_FORGET_CONTROL_REPLAY_BEFORE_READS=PASS
- FORGOTTEN_ARTIFACT_SUPPRESSED_AFTER_RESTORE=PASS
- UNRELATED_ARTIFACT_REMAINS_READABLE=PASS
- SAME_XID_COMMIT_AFTER_RESTORE=PASS
- RESTORED_PREPARED_VISIBILITY_POINTER_PLUS_RECEIPT=PASS
- JF10_POSTGRESQL_18_7_BACKUP_RESTORE_CAPABILITY=PASS

The backup was taken while the exact participant XID was prepared. The restored server retained that XID; the visibility pointer and receipt remained private. The restored snapshot contained local Forget-control epoch 0 while the test fixture supplied authoritative required epoch 1. The read gate rejected reads before reconciliation. The newer control record was then replayed, the forgotten artifact was suppressed, an unrelated artifact remained readable, and only then was the original prepared XID committed by the same XID.

## 12. Updated Gate A disposition after backup/restore

**Gate A remains PARTIAL PASS / OPEN, but all four executable CI sub-gates now pass on the pinned PostgreSQL 18.7 image:**
1. Single-node prepared-XID, lock retention, hard restart, same-XID commit/rollback.
2. Two-node synchronous WAL replay, primary hard loss, standby promotion, same-XID commit/rollback and atomic visibility.
3. Physical pg_basebackup/restore while a prepared XID exists; same-XID resolution after restore.
4. Stale restored control snapshot fails closed until newer Forget-control epoch is replayed before reads.

Remaining NOT VERIFIED:
- production host/zone loss, cloud volume durability, hardware persistence guarantees and real RPO/RTO;
- production failover fencing/STONITH, quorum manager, split-brain prevention, routing, reconnect and operational recovery ownership;
- actual Canonical Memory Authority deployment and exact production DB/storage/network/security configuration;
- named human production on-call/operator and approved runbooks;
- the external I sequencer, COC quorum log, C provider, application Storage participant adapter and end-to-end JF-10 integration.

The backup/restore control epoch in this CI probe is an explicit test fixture standing in for the externally authoritative I/D Forget-control ledger; it proves the fail-closed gate behavior, not production integration with I or D services. Gate B remains blocked until the real production deployment/operator portion of Gate A is accepted. Gate C remains blocked until Gate B.


## 13. Coordinator crash-window / unrecorded-ACK recovery — PASS (2026-11-17)

Storage added an independent deterministic coordinator-crash test around three ambiguous outcome boundaries. The test uses the pinned PostgreSQL 18.7 image and a durable SQLite coordinator-ledger fixture. Each child process terminates immediately after the PostgreSQL participant command succeeds but before the coordinator writes the ACK/result to its ledger. A fresh process then reconciles the exact original XID and authoritative participant rows.

Evidence:
- Probe: reviews/storage-consistency/postgres_probe/jf10_postgres_ack_gap_probe.py
- Probe Blob: 51cf8c7a9fa169aff8b0a5fd8a7ec5f934ad35a2
- Workflow: .github/workflows/jf10-postgres-ack-gap-capability.yml
- Workflow Blob: 7b612223f309ef0b963d262a94845a083e79ec7c
- Pinned image: postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc
- Successful run: 43912857694
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43912857694
- Run head commit: 5f342adb95f95208e8f1e2cc52538cf0944aa9e3
- Job ID: 133459107145
- Job conclusion: SUCCESS

Observed raw-log PASS markers:
- PREPARE_ACK_UNRECORDED_COORDINATOR_CRASH=PASS
- RECOVERED_EXACT_PREPARED_XID_NO_NEW_XID=PASS
- PREPARED_VISIBILITY_PRIVATE_AFTER_ACK_GAP=PASS
- PREPARE_ACK_GAP_THEN_TERMINAL_COMMIT_ACK_GAP=PASS
- SAME_XID_COMMIT_OUTCOME_RECONCILED=PASS
- COMMIT_ACK_UNRECORDED_COORDINATOR_CRASH=PASS
- COMMIT_VISIBILITY_INVARIANT_AFTER_ACK_GAP=PASS
- ROLLBACK_ACK_UNRECORDED_COORDINATOR_CRASH=PASS
- SAME_XID_ROLLBACK_OUTCOME_RECONCILED=PASS
- ROLLBACK_VISIBILITY_INVARIANT_AFTER_ACK_GAP=PASS
- JF10_COORDINATOR_ACK_GAP_RECOVERY=PASS

The test proves that after a coordinator process dies between participant success and recording the outcome, recovery can inspect the same XID and participant visibility state without allocating a replacement XID. PREPARE ambiguity retains private visibility and the prepared lock; terminal COMMIT ambiguity reconciles to pointer + receipt visible together; terminal ROLLBACK ambiguity reconciles to neither visible.

**Scope limitation:** this is a deterministic process-crash / lost-coordinator-checkpoint window test. It is not a TCP packet-drop or network ACK-loss test, does not use the production I sequencer/COC quorum log, and does not prove production coordinator durability. The SQLite ledger is a CI fixture only.

## 14. Updated Gate A status — participant ACK-gap subtest passed

The PostgreSQL 18.7 CI qualification now includes the four physical capability groups previously listed plus the coordinator ACK-gap recovery subtest. Gate A remains PARTIAL PASS / OPEN because the production deployment binding, real I/D control-ledger integration, production fencing/STONITH and split-brain prevention, host/zone/cloud storage durability, named human operator, approved runbook and RPO/RTO remain unverified. Gate B remains blocked pending full Gate A acceptance; Gate C remains blocked pending Gate B.


## 15. Real TCP CommandComplete ACK-loss and same-XID reconciliation — PASS (2026-11-17)

Storage added a one-shot TCP proxy that deliberately drops the PostgreSQL backend CommandComplete response frame after the server has executed the target command. The client therefore receives a broken connection / UNKNOWN result while the participant may already have changed durable state. Recovery reconnects directly and reconciles the exact original XID and visibility rows.

Evidence:
- Probe: reviews/storage-consistency/postgres_probe/jf10_postgres_tcp_ack_loss_probe.py
- Probe Blob: db843927fb3fd2f37b15b7a56dee5ca4c9b4274c
- Workflow: .github/workflows/jf10-postgres-tcp-ack-loss.yml
- Workflow Blob: ae9cea590721630f3ebad6d9566de79ac188fd23
- Pinned image: postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc
- Successful run: 43913477785
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43913477785
- Run head commit: 9f3f9595fa5fec6003ece53bb289a5ff499f87ee
- Job ID: 133461308120
- Job conclusion: SUCCESS

Observed raw-log PASS markers:
- CLIENT_OBSERVED_UNKNOWN_AFTER_PREPARE_TRANSACTION=PASS
- TCP_ACK_LOST_AFTER_PREPARE_SAME_XID_RECOVERED=PASS
- PREPARE_LOST_ACK_NO_PUBLICATION=PASS
- CLIENT_OBSERVED_UNKNOWN_AFTER_COMMIT_PREPARED=PASS
- TCP_ACK_LOST_AFTER_COMMIT_SAME_XID_RECONCILED=PASS
- COMMIT_POINTER_RECEIPT_ATOMIC_VISIBILITY=PASS
- CLIENT_OBSERVED_UNKNOWN_AFTER_ROLLBACK_PREPARED=PASS
- TCP_ACK_LOST_AFTER_ROLLBACK_SAME_XID_RECONCILED=PASS
- ROLLBACK_NON_PUBLICATION=PASS
- JF10_POSTGRESQL_TCP_ACK_LOSS_RECOVERY=PASS

This is an actual TCP response-loss injection at the PostgreSQL protocol CommandComplete boundary, not merely a suppressed application result. After PREPARE ACK loss, the exact prepared XID remained discoverable, its lock remained held, and pointer/receipt remained private. After COMMIT ACK loss, the exact XID was absent and pointer + receipt were visible together. After ROLLBACK ACK loss, the exact XID was absent and neither row was visible.

Scope limitation: this is a single-node PostgreSQL 18.7 CI proxy test. It does not establish production I sequencer/COC integration, coordinator quorum durability, real network partitions across production zones, production failover fencing or deployment readiness.

## 16. Gate A updated disposition

The PostgreSQL 18.7 candidate now has passing CI evidence for:
1. single-node prepared-XID, lock retention, hard restart and same-XID commit/rollback;
2. two-node synchronous WAL replay, primary hard loss, standby promotion and same-XID commit/rollback;
3. physical pg_basebackup/restore with prepared-XID survival and stale-control fail-closed behavior;
4. coordinator process crash after participant success but before ACK/checkpoint persistence;
5. real TCP CommandComplete response loss after PREPARE, COMMIT PREPARED and ROLLBACK PREPARED, followed by exact same-XID reconciliation.

Gate A remains PARTIAL PASS / OPEN because the actual Canonical Authority deployment, production I/D ledger integration, production failover fencing/STONITH and split-brain prevention, host/zone/cloud-storage durability, named human operator, runbook and RPO/RTO are not bound or verified. Gate B remains blocked until full Gate A acceptance; Gate C remains blocked until Gate B.


## 17. Required synchronous standby unavailable — PREPARE remains UNKNOWN/private — PASS (2026-11-17)

Storage added a negative-path PostgreSQL 18.7 CI probe. It establishes a required synchronous standby with `synchronous_commit=remote_apply`, stops that standby, starts a protected transaction and attempts `PREPARE TRANSACTION`.

Evidence:
- Probe: `reviews/storage-consistency/postgres_probe/jf10_postgres_sync_unavailable_probe.py`
- Probe Blob: `b6de4e4f461405107464ff8ad179520f9b028749`
- Workflow: `.github/workflows/jf10-postgres-sync-unavailable.yml`
- Workflow Blob: `32ed78aa702dfb6f45c73f94c81bd617b970976b`
- Successful run: `43927416496`
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43927416496
- Run commit: `4e4cf967d97254f1f6e8dea03f1afd1402ff0802`
- Job ID: `133510446871`
- Conclusion: SUCCESS

Observed raw log markers:
- `REQUIRED_SYNCHRONOUS_STANDBY_UNAVAILABLE=PASS`
- `PREPARE_WAIT_EVENT=('IPC', 'SyncRep')`
- `PREPARE_BLOCKED_ON_SYNCHRONOUS_REPLICATION=PASS`
- `CLIENT_PREPARE_OUTCOME_UNKNOWN_AFTER_CONNECTION_LOSS=PASS`
- `LOCAL_PREPARED_XID_REMAINS_IN_DOUBT=PASS`
- `NO_PROTECTED_VISIBILITY=PASS`
- `PREPARED_LOCK_RETAINED_DURING_UNKNOWN=PASS`
- `SAME_XID_ROLLBACK_AFTER_TEST=PASS`
- `NO_PUBLICATION_AFTER_ROLLBACK=PASS`
- `JF10_SYNC_STANDBY_UNAVAILABLE_FAIL_CLOSED=PASS`

**Important interpretation:** the PREPARE backend had already persisted the prepared XID locally when it entered the synchronous-replication wait. Terminating the backend while it waited produced client UNKNOWN, while the exact XID remained locally prepared and its lock remained held; the visibility row remained absent. This is not evidence that the prepared XID was absent or replicated. It proves the client cannot treat a lost PREPARE ACK as success and must preserve UNKNOWN / IN_DOUBT, keep publication private and prevent the I coordinator from advancing until the exact XID is reconciled against the authoritative recovery path. The test's final ROLLBACK PREPARED uses `synchronous_commit=local` solely for cleanup after all safety assertions; that cleanup override is not a production configuration.

An earlier draft of this probe incorrectly expected the local prepared XID to be absent and failed. The final probe corrects that assertion to the actual PostgreSQL behavior above; the failed run is not counted as passing evidence.

Gate A remains PARTIAL PASS / OPEN. This CI test does not prove production standby recovery, fencing, or safe promotion while the PREPARE ACK is outstanding. A production failover policy must not promote a standby that may lack the locally prepared XID and then claim a terminal participant outcome.


## 18. WAL-archive point-in-time recovery to explicit LSN — PASS (2026-11-17)

Storage added and executed a PostgreSQL 18.7 WAL-archive PITR campaign. The workflow creates a physical base backup, commits a target marker, captures its post-commit LSN, commits a later marker, archives the WAL segment, restores the base backup with archive recovery, and promotes at the explicit target LSN.

Evidence:
- Probe: `reviews/storage-consistency/postgres_probe/jf10_postgres_pitr_probe.py`
- Probe Blob: `6e7721ee8f8708357610e0bc564e015872b8263c`
- Workflow: `.github/workflows/jf10-postgres-pitr.yml`
- Workflow Blob: `4c2175055ae43ccebb95f219952ec0480121e62d`
- Successful run: `43927783471`
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43927783471
- Run commit: `91117532adb25914bcaa49b0007f7c34ef49c787`
- Job ID: `133511748345`
- Conclusion: SUCCESS
- Engine: PostgreSQL 18.7 (Debian 18.7-1.pgdg13+2)
- Explicit recovery target LSN: `0/6000190`
- Observed replay LSN: `0/7000000`
- Promoted recovery timeline: `2`

Raw log PASS markers:
- `PITR_BASE_BACKUP_CREATED=PASS`
- `PITR_TARGET_WAL_ARCHIVED=PASS`
- `PITR_BASE_STATE_PRESENT=PASS`
- `PITR_TARGET_STATE_PRESENT=PASS`
- `PITR_POST_TARGET_STATE_ABSENT=PASS`
- `PITR_EXACT_LSN_RECOVERY=PASS`
- `JF10_POSTGRESQL_WAL_ARCHIVE_PITR=PASS`

The test proves that the base state and target transaction are present after recovery while the transaction committed after the target LSN is absent. The restored server was promoted on timeline 2. The recovery image was configured with the same `max_prepared_transactions=16`, `wal_level=replica`, `fsync=on` and `full_page_writes=on` profile as the source; the restore explicitly removed any standby.signal and used recovery.signal plus the archived WAL.

Scope: this is a single-node CI PITR capability test using a local Docker named volume and archive volume. It does not prove production archive retention, off-site immutability, backup catalog integrity, cross-zone recovery, RPO/RTO, key custody, or replay of the production I/D Forget-control ledger. Gate A remains PARTIAL PASS / OPEN.


## 19. Fenced old-primary pg_rewind and safe standby rejoin — PASS (2026-11-17)

Storage added and executed a PostgreSQL 18.7 two-node rejoin-procedure test. It hard-fences the old primary container, promotes the synchronous standby, recovers the old data directory offline, rewinds it to the promoted source timeline with `pg_rewind`, and starts it only as a standby.

Evidence:
- Probe: `reviews/storage-consistency/postgres_probe/jf10_postgres_pg_rewind_rejoin_probe.py`
- Probe Blob: `0fe6af4a8c9ef350ef9cbf0694a8f975e8f142f5`
- Workflow: `.github/workflows/jf10-postgres-pg-rewind-rejoin.yml`
- Workflow Blob: `7670ff9537054df1c1303d4eda4d46bffdfa3c4c`
- Successful run: `43930047054`
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43930047054
- Run commit: `1eb9c9c08e3ae658fcbcfa568d1c2e1ab0e1999a`
- Job ID: `133519705454`
- Conclusion: SUCCESS

Observed raw log PASS markers:
- `OLD_PRIMARY_HARD_FENCED=PASS`
- `OLD_PRIMARY_OFFLINE_CRASH_RECOVERY=PASS`
- `PG_REWIND_TO_PROMOTED_TIMELINE=PASS`
- `NEW_PRIMARY_POST_REJOIN_WRITE_REPLICATED=PASS`
- `REJOINED_OLD_PRIMARY_REJECTS_WRITES=PASS`
- `OLD_PRIMARY_REJOINED_AS_STANDBY=PASS`
- `PRE_FAILOVER_AND_POST_PROMOTION_DATA_REPLICATED=PASS`
- `NO_DUAL_WRITER_AFTER_REJOIN=PASS`
- `JF10_POSTGRESQL_PG_REWIND_REJOIN=PASS`

The CI procedure kept the old primary stopped and unreachable after hard kill, performed crash recovery with networking disabled, retained required WAL for `pg_rewind`, rewound the data directory to the promoted primary, then rejoined the old node as a read-only standby. A new write made after rejoin was observed on the rejoined standby; a direct write attempt on that standby was rejected.

**Scope limitation:** the “fence” is a stopped Docker container under a single GitHub Actions runner, not production STONITH, cloud instance fencing, storage fencing, independent failure-domain control, HA-manager arbitration, DNS/connection routing or split-brain monitoring. The checkpoint timeline fields returned by `pg_control_checkpoint()` remained at the prior checkpoint timeline in this short test; the authoritative evidence of the new timeline is `pg_rewind` plus the standby WAL receiver streaming from timeline 2 and successful post-rejoin replication. Do not cite the checkpoint timeline fields as proof of timeline 2.

This closes only the pg_rewind/rejoin procedure subtest for the pinned CI profile. Production fencing and split-brain prevention remain OPEN. Gate A remains PARTIAL PASS / OPEN.


## 20. Prepared-XID / visibility / receipt PITR boundaries and WAL archive negatives — PASS (2026-11-17)

Storage executed the dedicated PostgreSQL 18.7 PITR atomicity campaign on the pinned image digest. The probe creates two prepared transactions, takes a physical backup while both are prepared, then resolves one by COMMIT PREPARED and the other by ROLLBACK PREPARED. Separate restores target the prepared, commit and rollback LSN boundaries. The same workflow also runs missing, corrupt and incomplete WAL archive negative cases.

Evidence:
- Probe: `reviews/storage-consistency/postgres_probe/jf10_postgres_pitr_atomicity_probe.py`
- Probe Blob: `8c0e281f1db4dd6190127f02ac71b1126da39903`
- Workflow: `.github/workflows/jf10-postgres-pitr-atomicity.yml`
- Successful run: `43955195460`
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195460
- Run head commit: `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`
- Job ID: `133607791713`
- Job conclusion: SUCCESS
- Pinned image: `postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc`
- Observed boundary LSNs: prepared `0/5004420`; commit `0/6000000`; rollback `0/6000110`.

Observed raw-log PASS markers:
- `PREPARED_XIDS_CREATED=PASS`
- `PREPARED_BOUNDARY_WAL_ARCHIVED=PASS`
- `PITR_PREPARED_XID_PRIVATE_AND_LOCKED=PASS`
- `PITR_COMMIT_POINTER_AND_RECEIPT_ATOMIC=PASS`
- `PITR_ROLLBACK_NO_POINTER_NO_RECEIPT=PASS`
- `JF10_PITR_PREPARED_XID_VISIBILITY_RECEIPT_BOUNDARIES=PASS`
- `PITR_MISSING_WAL_FAILS_CLOSED=PASS`
- `PITR_CORRUPT_WAL_FAILS_CLOSED=PASS`
- `PITR_INCOMPLETE_WAL_FAILS_CLOSED=PASS`
- `JF10_PITR_WAL_NEGATIVE_CASES=PASS`
- `JF10_POSTGRESQL_PITR_ATOMICITY_AND_NEGATIVES=PASS`

The prepared-boundary restore retained both exact prepared XIDs and their locks while exposing neither VisibilityPointer nor PublicationReceipt. The commit-boundary restore exposed the commit participant's pointer and receipt together while retaining the other prepared participant. The rollback-boundary restore showed no pointer and no receipt for the rolled-back participant. Each malformed or unavailable archive case failed recovery closed rather than allowing a writable, incorrectly promoted recovery instance.

The first attempt exposed a test-harness target-LSN defect: the rollback target was sampled after `pg_switch_wal()`, which moved the target to the next WAL segment boundary. The corrected probe captures `pg_current_wal_flush_lsn()` after the rollback marker and before switching WAL. The successful run above is on the corrected commit; the earlier failed run is not counted as passing evidence.

**Scope limitation:** this is an isolated Storage fixture using local Docker volumes and a local archive. It proves PostgreSQL capability behavior for the pinned CI profile, not production COC quorum durability, production I/D Forget-control ledger replay, archive immutability/off-site retention, cross-zone recovery, production operator procedures, or RPO/RTO. Gate A remains PARTIAL PASS / OPEN. Gate B remains blocked pending full Gate A acceptance; Gate C remains blocked pending Gate B; JF-10 P0 remains OPEN and production activation remains NOT AUTHORIZED.

## 21. Repeated physical backup/restore and explicit-LSN PITR workflow confirmation — PASS (2026-11-17)

The same corrected commit also reran the previously established physical backup/restore and explicit-LSN PITR workflows successfully:
- Physical backup/restore run: `43955195219`; job `133607790737`; final marker `JF10_POSTGRESQL_18_7_BACKUP_RESTORE_CAPABILITY=PASS`.
- Explicit-LSN archive PITR run: `43955195388`; job `133607790699`; final markers `PITR_BASE_STATE_PRESENT=PASS`, `PITR_TARGET_STATE_PRESENT=PASS`, `PITR_POST_TARGET_STATE_ABSENT=PASS`, `PITR_EXACT_LSN_RECOVERY=PASS`, `JF10_POSTGRESQL_WAL_ARCHIVE_PITR=PASS`.
- Explicit target LSN: `0/5000190`; observed replay LSN: `0/6000000`; promoted timeline: `2`.

These are rerun confirmations of the respective isolated CI probes, not production restore qualification. All three workflows ran against commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`.


## 22. Repository runtime / authoritative DB adapter boundary audit — NOT IDENTIFIED (2026-11-17)

Storage inspected the complete recursive Git tree for the exact branch head after the PITR evidence updates:
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`
- Tree head: `e803f7d79d4ec747272299113d8222c60c3be8e9`
- Recursive tree entries: 86; GitHub reported `truncated=false`.
- Executable/source-like files: 21 total. All 21 are GitHub Actions workflows, isolated PostgreSQL probe scripts, or the JF-10 reference model and its tests.
- No production runtime source tree, service executable, Canonical Authority DB adapter, migration package, or application deployment manifest is present in this branch snapshot.

This is a repository-content observation, not a claim that no implementation exists in any external repository or deployment. The project-designated Canonical Authority runtime executable and its authoritative database access path therefore cannot be identified or inspected from this repository branch. The PostgreSQL 18.7 CI probes remain engine-capability fixtures and must not be described as exercising the production adapter.

**Gate A stop condition:** the responsible Owner must provide the canonical implementation repository/branch and exact runtime entrypoint, DB adapter and schema/migration path, or explicitly designate this repository as the implementation home and deliver those artifacts. Storage must then trace the actual authoritative write/read path for prepared XID, D/lineage locks, VisibilityPointer, PublicationReceipt, owner outcome, receipt-consumption evidence and outbox, and run the conformance/fault suite against that path. Until then, production database binding and implementation conformance remain NOT IDENTIFIED / NOT VERIFIED; Gate A remains PARTIAL PASS / OPEN.


## 23. Full seven-workflow PostgreSQL 18.7 regression batch — PASS (2026-11-17)

The corrected PITR commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd` triggered the complete seven-workflow Storage regression batch. All seven runs completed with conclusion SUCCESS; the following raw job markers were independently re-read:

| Capability | Run / Job | Observed final marker |
|---|---|---|
| Prepared-XID + restart | `43955195289` / `133607790416` | `JF10_POSTGRESQL_18_7_SINGLE_NODE_CAPABILITY=PASS` |
| Synchronous standby promotion | `43955195323` / `133607790413` | `JF10_POSTGRESQL_18_7_SYNC_FAILOVER_CAPABILITY=PASS` |
| Physical backup/restore | `43955195219` / `133607790737` | `JF10_POSTGRESQL_18_7_BACKUP_RESTORE_CAPABILITY=PASS` |
| Explicit-LSN WAL PITR | `43955195388` / `133607790699` | `JF10_POSTGRESQL_WAL_ARCHIVE_PITR=PASS` |
| Prepared-XID PITR + archive negatives | `43955195460` / `133607791713` | `JF10_POSTGRESQL_PITR_ATOMICITY_AND_NEGATIVES=PASS` |
| Synchronous standby unavailable | `43955195197` / `133607790658` | `JF10_SYNC_STANDBY_UNAVAILABLE_FAIL_CLOSED=PASS` |
| Old-primary rewind/rejoin | `43955195256` / `133607790520` | `JF10_POSTGRESQL_PG_REWIND_REJOIN=PASS` |

The raw logs also show same-XID COMMIT/ROLLBACK after promotion, prepared lock retention, private visibility during synchronous-replication UNKNOWN, and the rewound old primary rejecting writes after rejoining as a standby. The rejoin evidence remains a single-runner Docker fencing simulation, not production STONITH or split-brain prevention.

This batch provides regression confidence for the pinned PostgreSQL 18.7 CI profile. It does not change Gate A's overall disposition: production runtime/adapter binding, I/D ledger integration, real infrastructure durability/fencing, named operator/runbook and RPO/RTO remain open. Gate A PARTIAL PASS / OPEN; Gate B BLOCKED; Gate C BLOCKED; production activation NOT AUTHORIZED.

## 24. Project phase correction — architecture design, not production implementation (2026-11-17)

**Authoritative phase clarification:** AiMemoryBrainArchitecture is currently an architecture-design project. There is no production code repository or production runtime implementation at this stage, and none is expected as a prerequisite for architecture-phase acceptance. The absence of an application runtime, DB adapter, migration package or deployment manifest in this architecture repository is therefore NOT a Gate A defect and must not be treated as a blocker. Section 22's observation about repository contents remains factually valid, but its proposed stop condition requiring a production implementation repository is superseded by this phase clarification.

Correct interpretation of evidence:
- The PostgreSQL 18.7 pinned-image CI probes prove selected database-engine capabilities and the behavior of the isolated Storage reference fixtures.
- They do not claim production application integration, deployed topology, cloud fencing, or operational qualification.
- Those are engineering/deployment-phase verification items, to be bound to an implementation after the architecture is accepted and an implementation repository exists.

Architecture-phase Gate A must instead close its design deliverables: selected engine/version/profile and rationale; transaction/isolation and lock/visibility contract; durable prepared-XID and same-XID recovery semantics; atomic VisibilityPointer + PublicationReceipt + owner outcome/receipt-consumption/outbox boundary; authoritative-read and stale-replica exclusion rules; backup/PITR/archive continuity and fail-closed recovery rules; HA/fencing/rejoin architecture; failure-domain/topology requirements; and explicit future implementation/operations acceptance criteria including RPO/RTO and accountable deployment ownership. Any item not yet specified remains an architecture design gap, not a missing-code blocker.

**Disposition:** remove “production runtime/DB adapter not identified” as a Gate A architecture blocker. Keep it as DEFERRED_TO_ENGINEERING_PHASE. PostgreSQL 18.7 CI capability evidence remains PASS within its stated isolated-fixture scope. Gate A overall remains PARTIAL PASS / OPEN only for outstanding architecture specifications and cross-owner design decisions. Gate B COC persistence and recovery protocol design is now authorized to proceed as the next architecture workstream; this does not authorize implementation or production activation. Gate C end-to-end implementation fault injection remains deferred until the relevant protocols and a runnable implementation exist. JF-10 P0 remains OPEN until its architecture and later engineering acceptance criteria are met; production activation NOT AUTHORIZED.


## 24. Exact target-WAL PITR evidence and authoritative-reader negative fixtures — PASS (2026-11-17)

Storage strengthened the prepared-XID PITR probe after reviewing the prior passing campaign. The updated probe now derives and waits for the exact WAL segment containing each recovery target (prepared, COMMIT and ROLLBACK), emits each target LSN/timeline/required segment, checks a paired VisibilityPointer + PublicationReceipt authoritative-reader view, and binds each negative archive failure to the exact deliberately damaged required segment.

Evidence:
- Probe: `reviews/storage-consistency/postgres_probe/jf10_postgres_pitr_atomicity_probe.py`
- Probe Blob: `9d2a85f9a5d53f91df247a310c38377e563d259d`
- Workflow: `.github/workflows/jf10-postgres-pitr-atomicity.yml`; Blob `a055d311c324d09eb6ebf4054247761116795eb7`
- Successful run: `43957910909`; job `133617253176`; conclusion SUCCESS
- Run commit: `2d476dd32ac020d329e8290ee2aaaa1f0c057c92`
- Pinned image: `postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc`

Raw job log target markers:
- Prepared target: LSN `0/5004710`, timeline `1`, required WAL `000000010000000000000005`, archived PASS.
- COMMIT target: LSN `0/6000000`, timeline `1`, required WAL `000000010000000000000006`, archived PASS.
- ROLLBACK target: LSN `0/6000110`, timeline `1`, required WAL `000000010000000000000006`, archived PASS.

Observed PASS markers:
- `AUTHORITATIVE_READER_REJECTS_POINTER_ONLY_AND_RECEIPT_ONLY=PASS`
- `PITR_PREPARED_XID_PRIVATE_AND_LOCKED=PASS`
- `PITR_COMMIT_POINTER_AND_RECEIPT_ATOMIC=PASS`
- `PITR_ROLLBACK_NO_POINTER_NO_RECEIPT=PASS`
- `PITR_MISSING_EXACT_WAL_FAILS_CLOSED=PASS`
- `PITR_CORRUPT_EXACT_WAL_FAILS_CLOSED=PASS`
- `PITR_INCOMPLETE_EXACT_WAL_FAILS_CLOSED=PASS`
- `PITR_MISSING_NO_WRITABLE_OR_AUTHORITATIVE_SERVICE=PASS`
- `PITR_CORRUPT_NO_WRITABLE_OR_AUTHORITATIVE_SERVICE=PASS`
- `PITR_INCOMPLETE_NO_WRITABLE_OR_AUTHORITATIVE_SERVICE=PASS`
- `JF10_POSTGRESQL_PITR_ATOMICITY_AND_NEGATIVES=PASS`

The missing/corrupt/incomplete cases each target the exact segment required to reach the rollback LSN. The raw logs identify the affected segment; the corruption case reports PostgreSQL's invalid WAL magic number, and the incomplete case reports the 8192-byte archive segment where 16777216 bytes are required. The failed restores do not promote to writable primary or expose an authoritative service.

**Scope limitation:** the authoritative-reader check is an isolated SQL-view fixture that joins the pointer and receipt by XID and artifact identity; it rejects pointer-only and receipt-only rows in that fixture. It is not the project's production authoritative read adapter, which remains unidentified in this repository. The CI uses local Docker volumes and local archive storage; it does not prove production I/D control-ledger integration, archive immutability/off-site retention, cross-zone durability, production fencing, operator/runbook or RPO/RTO. Two earlier runs on intermediate commits failed because the corrupt-WAL assertion did not recognize PostgreSQL's exact `invalid magic number` diagnostic; those failures are not counted. The corrected run above is the passing evidence.

Gate A remains PARTIAL PASS / OPEN. Gate B remains BLOCKED pending full Gate A acceptance; Gate C remains BLOCKED pending Gate B; JF-10 P0 remains OPEN; production activation remains NOT AUTHORIZED.

## 25. Enhanced PITR exact-WAL regression re-pass — 7/7 SUCCESS (2026-11-17)

The enhanced probe now checks exact target WAL segments for prepared, COMMIT and ROLLBACK recovery cuts; the fixture authoritative-reader view rejects pointer-only and receipt-only rows; and each missing/corrupt/incomplete archive case asserts the exact target segment and absence of a writable/authoritative service.

The first enhanced run on commit `3c8ab8e` failed only because the harness did not recognize PostgreSQL's observed `invalid magic number D158` diagnostic. The assertion was corrected to recognize that diagnostic without weakening exact target-segment matching or the no-writable/no-authoritative-service check.

Corrected evidence:
- Source commit: `2d476dd32ac020d329e8290ee2aaaa1f0c057c92`.
- Probe Blob: `9d2a85f9a5d53f91df247a310c38377e563d259d`.
- Workflow Blob: `a055d311c324d09eb6ebf4054247761116795eb7`.
- Run: `43957910909`; job: `133617253176`; SUCCESS.
- Exact target LSN / timeline / WAL: prepared `0/5004710` / `1` / `000000010000000000000005`; COMMIT `0/6000000` / `1` / `000000010000000000000006`; ROLLBACK `0/6000110` / `1` / `000000010000000000000006`.

Raw logs confirm pointer-only/receipt-only rejection; prepared XID privacy and lock retention; atomic pointer+receipt at COMMIT; neither at ROLLBACK; and all three exact-WAL negative cases fail closed without a writable or authoritative service.

The six companion workflows on the same source commit also concluded SUCCESS: prepared-XID/restart `43957910975`; synchronous failover `43957911188`; backup/restore `43957911173`; explicit-LSN PITR `43957910971`; synchronous standby unavailable `43957911270`; old-primary rewind/rejoin `43957911036`. Enhanced current batch = **7/7 SUCCESS**. The intermediate failed harness run is not counted.

Scope remains the pinned PostgreSQL CI/reference fixture only. The reader is a synthetic SQL view, not a production adapter. This is not production COC/I/D integration or deployment qualification.

## 26. Gate B design sequencing after project-phase clarification

The project is in architecture design; no production code repository/runtime is expected. Production implementation binding is `DEFERRED_TO_ENGINEERING_PHASE`, not a Gate A blocker. Gate B's persistent COC/quorum log/participant registry/recovery-cutoff protocol design may proceed now, in parallel with closure of remaining Gate A storage design specifications. This is design authorization only; Gate B is not implementation-PASS. Gate C executable fault injection remains deferred until implementation exists. JF-10 P0 remains OPEN; production activation NOT AUTHORIZED.


## 25. Exact prepared-XID lock binding and same-XID resolution after PITR — PASS (2026-11-17)

Storage extended the PITR prepared-boundary restore to correlate each exact prepared GID with its transaction-ID lock in `pg_locks`, rather than relying only on a global lock count. After recording the in-doubt/private state, the probe resolves the restored transactions using the original exact GIDs: COMMIT PREPARED for the commit participant and ROLLBACK PREPARED for the rollback participant.

Evidence:
- Probe Blob: `63506807be82b3203e7e682b0772452621c92558`
- Commit: `d026add5cfaec0d395537e8763317cdbd8255398`
- Workflow run/job: `43958775001` / `133620265141`, SUCCESS.
- Pinned image: `postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc`.

Raw-log PASS markers:
- `PITR_EXACT_PREPARED_XID_LOCKS_RETAINED=PASS`
- `PITR_PREPARED_XID_PRIVATE_AND_LOCKED=PASS`
- `PITR_SAME_XID_COMMIT_ROLLBACK_AFTER_RESTORE=PASS`
- `PITR_COMMIT_POINTER_AND_RECEIPT_ATOMIC=PASS`
- `PITR_ROLLBACK_NO_POINTER_NO_RECEIPT=PASS`
- `JF10_POSTGRESQL_PITR_ATOMICITY_AND_NEGATIVES=PASS`

This establishes exact prepared-GID/transaction-lock correlation and same-GID forward/rollback resolution in the isolated PostgreSQL PITR fixture. It does not turn the fixture into the production Storage adapter or prove I/D/COC control-plane integration.


## 26. PostgreSQL initdb readiness race correction and seven-workflow regression — PASS (2026-11-17)

A full regression batch after the PITR changes exposed one unrelated single-node capability workflow startup race: the initial `pg_isready` could observe the temporary PostgreSQL server used by the official image's initdb sequence, immediately before that server shut down and the durable server started. The Python probe then received a closed connection. This was not a prepared-XID invariant failure.

Storage corrected the workflow to wait until the initdb temporary and final server readiness log events have both occurred before accepting `pg_isready`, and made the probe itself call its bounded `wait_ready()` before setup.
- Workflow Blob: `fbcbce03d4525f7a0fb9dd3673a580a3a4c00134`
- Probe Blob: `184e0507fd225ee18f321f3f1ce6a63f869b13f3`
- Fix commit: `83bdacbafa840808dca9be7a8c76c4df83c63504`
- Prepared-XID workflow after fix: run `43959079736`, job `133621314502`, SUCCESS; markers include `SAME_XID_COMMIT_AFTER_RESTART=PASS`, `SAME_XID_ROLLBACK=PASS`, and `JF10_POSTGRESQL_18_7_SINGLE_NODE_CAPABILITY=PASS`.

The seven-workflow regression evidence is:

| Capability | Run / Job | Source commit | Conclusion |
|---|---|---|---|
| Prepared-XID PITR + exact locks + same-XID resolution + archive negatives | `43958775001` / `133620265141` | `d026add5cfaec0d395537e8763317cdbd8255398` | SUCCESS |
| Prepared-XID + restart | `43959079736` / `133621314502` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Synchronous standby promotion | `43959079669` / `133621315610` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Physical backup/restore | `43959079703` / `133621314624` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Explicit-LSN WAL PITR | `43959079745` / `133621314724` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Synchronous standby unavailable | `43959079760` / `133621315188` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Old-primary pg_rewind/rejoin | `43959079930` / `133621314973` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |

All seven jobs' final raw-log markers were independently inspected. The first prepared-XID workflow attempt on commit `d026add5...` failed only at the transient initdb readiness race; it is superseded by the successful run `43959079736` after the readiness fix and is not counted as passing evidence.

This is a regression result for pinned PostgreSQL 18.7 CI fixtures, not production deployment acceptance. Gate A remains PARTIAL PASS / OPEN; Gate B and Gate C remain BLOCKED; JF-10 P0 remains OPEN; production activation NOT AUTHORIZED.


## 25. Exact prepared-XID lock binding and same-XID resolution after PITR — PASS (2026-11-17)

Storage extended the PITR prepared-boundary restore to correlate each exact prepared GID with its transaction-ID lock in `pg_locks`, rather than relying only on a global lock count. After recording the in-doubt/private state, the probe resolves the restored transactions using the original exact GIDs: COMMIT PREPARED for the commit participant and ROLLBACK PREPARED for the rollback participant.

Evidence:
- Probe Blob: `63506807be82b3203e7e682b0772452621c92558`
- Commit: `d026add5cfaec0d395537e8763317cdbd8255398`
- Workflow run/job: `43958775001` / `133620265141`, SUCCESS.
- Pinned image: `postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc`.

Raw-log PASS markers:
- `PITR_EXACT_PREPARED_XID_LOCKS_RETAINED=PASS`
- `PITR_PREPARED_XID_PRIVATE_AND_LOCKED=PASS`
- `PITR_SAME_XID_COMMIT_ROLLBACK_AFTER_RESTORE=PASS`
- `PITR_COMMIT_POINTER_AND_RECEIPT_ATOMIC=PASS`
- `PITR_ROLLBACK_NO_POINTER_NO_RECEIPT=PASS`
- `JF10_POSTGRESQL_PITR_ATOMICITY_AND_NEGATIVES=PASS`

This establishes exact prepared-GID/transaction-lock correlation and same-GID forward/rollback resolution in the isolated PostgreSQL PITR fixture. It does not turn the fixture into the production Storage adapter or prove I/D/COC control-plane integration.

## 26. PostgreSQL initdb readiness race correction and seven-workflow regression — PASS (2026-11-17)

A full regression batch after the PITR changes exposed one unrelated single-node capability workflow startup race: the initial `pg_isready` could observe the temporary PostgreSQL server used by the official image's initdb sequence, immediately before that server shut down and the durable server started. The Python probe then received a closed connection. This was not a prepared-XID invariant failure.

Storage corrected the workflow to wait until the initdb temporary and final server readiness log events have both occurred before accepting `pg_isready`, and made the probe itself call its bounded `wait_ready()` before setup.
- Workflow Blob: `fbcbce03d4525f7a0fb9dd3673a580a3a4c00134`
- Probe Blob: `184e0507fd225ee18f321f3f1ce6a63f869b13f3`
- Fix commit: `83bdacbafa840808dca9be7a8c76c4df83c63504`
- Prepared-XID workflow after fix: run `43959079736`, job `133621314502`, SUCCESS; markers include `SAME_XID_COMMIT_AFTER_RESTART=PASS`, `SAME_XID_ROLLBACK=PASS`, and `JF10_POSTGRESQL_18_7_SINGLE_NODE_CAPABILITY=PASS`.

The seven-workflow regression evidence is:

| Capability | Run / Job | Source commit | Conclusion |
|---|---|---|---|
| Prepared-XID PITR + exact locks + same-XID resolution + archive negatives | `43958775001` / `133620265141` | `d026add5cfaec0d395537e8763317cdbd8255398` | SUCCESS |
| Prepared-XID + restart | `43959079736` / `133621314502` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Synchronous standby promotion | `43959079669` / `133621315610` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Physical backup/restore | `43959079703` / `133621314624` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Explicit-LSN WAL PITR | `43959079745` / `133621314724` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Synchronous standby unavailable | `43959079760` / `133621315188` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |
| Old-primary pg_rewind/rejoin | `43959079930` / `133621314973` | `83bdacbafa840808dca9be7a8c76c4df83c63504` | SUCCESS |

All seven jobs' final raw-log markers were independently inspected. The first prepared-XID workflow attempt on commit `d026add5...` failed only at the transient initdb readiness race; it is superseded by the successful run `43959079736` after the readiness fix and is not counted as passing evidence.

This is a regression result for pinned PostgreSQL 18.7 CI fixtures, not production deployment acceptance. Gate A remains PARTIAL PASS / OPEN; Gate B and Gate C remain BLOCKED; JF-10 P0 remains OPEN; production activation NOT AUTHORIZED.


## 27. Default-branch and linked-repository audit for production runtime designation — NOT IDENTIFIED (2026-11-17)

Storage rechecked the repository's default branch, not only the Storage feature branch:
- Default branch: `main`
- Commit: `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`
- Recursive tree: `748613c916ca795cb5b1af65f6fcdda81b928a9d`; 52 entries; `truncated=false`.
- The tree contains architecture/governance/review Markdown only; zero executable/source-like files matching `.py/.go/.rs/.ts/.tsx/.js/.java/.sql/.yaml/.yml/.toml/.json`.

Storage also searched the linked GitHub repository catalog for `AiMemoryBrain`, `Canonical Authority`, and `memory runtime`. Only `oahcom/AiMemoryBrainArchitecture` matched the project-specific query; no separate Canonical Authority or memory-runtime repository was identified by those searches. This is a bounded account/repository search, not proof that no external or unlinked repository exists.

**Disposition:** the canonical production runtime, authoritative DB adapter, schema/migration path and deployment manifest remain NOT IDENTIFIED. Storage cannot truthfully claim production adapter conformance or bind the PostgreSQL 18.7 capability fixtures to an application path until A/C/designated implementation owner supplies the immutable implementation repository/commit and runtime entrypoint, or explicitly designates this repository as the implementation home and delivers the missing code.

Gate A remains PARTIAL PASS / OPEN; Gate B remains BLOCKED; Gate C remains BLOCKED; JF-10 P0 remains OPEN; production activation NOT AUTHORIZED.


## 28. I-accepted JF-10 v2 Storage bridge — contract-to-evidence gap (2026-11-17)

Storage re-read the exact D/Storage common v2 protocol and I's formal disposition before defining the next implementation boundary:
- D/Storage common v2 protocol: Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0`.
- I JF-10 v2 disposition: Blob `8069ff86988396442c8d9dc3fd58653683abe2f3`.
- A COC architecture proposal: Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`.

I accepts the single-PolicyDomain owner-gate-participating durable 2PC architecture with binding clarifications. I's policy-domain sequencer remains the sole durable COMMIT/ABORT decision authority; COC is the quorum-ordered intent/participant-observation and reconciliation service; Storage alone resolves the exact prepared XID and commits/rolls back local visibility. COC positions and I sequencer positions are distinct typed orders and MUST NOT be numerically compared or synthesized.

### Storage bridge requirements versus current evidence

| Normative requirement | Current evidence | Status / missing implementation |
|---|---|---|
| Preallocated XID + stable PublicationOperationId/RequestDigest + exact owner_boundary + participant digest + Canonical Authority DB identity | Local PostgreSQL probes use stable or generated GIDs and exercise same-XID recovery | **PARTIAL** — no production DB identity, COC ParticipantIntentRef or immutable cross-service tuple binding |
| COC `JF10_PREPARE_INTENT_REGISTERED` before Storage PREPARE | No COC integration in the probes | **NOT IMPLEMENTED** |
| Storage-authenticated `PreparedParticipantReceipt` binding exact XID/digest/operation/DB identity/prepare state | Local pg_prepared_xacts and lock observations only | **NOT IMPLEMENTED** — no signing/verifying identity or receipt wire contract in the Storage runtime |
| COC `JF10_PREPARED_PARTICIPANT_REGISTERED` before I owner-final-gate | No COC participant registry or linearizable prefix API in the repository | **NOT IMPLEMENTED** |
| I owner-final-gate consumes the exact COC-registered participant and atomically consumes CommitAuthorizationReceipt | No live I sequencer or authenticated I API used by the probes | **NOT IMPLEMENTED** |
| I COMMIT_WON => forward-commit exact XID; I ABORT => rollback exact XID; UNKNOWN => retain XID/locks/private bytes | PostgreSQL same-XID restart/failover/PITR commit/rollback capability is covered locally | **PARTIAL** — no terminal decision source, coordinator outage, or COC/I recovery bridge |
| Atomic VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption evidence + outbox | Isolated prepared transaction proves pointer+receipt atomicity; local authoritative SQL-view fixture rejects pointer-only/receipt-only | **PARTIAL** — no production owner outcome, receipt-consumption record, outbox or application authoritative reader |
| COC `STORAGE_JF10_PARTICIPANT_RESOLVED` and `JF10_BRIDGE_RECONCILIATION_RECORDED` with authoritative readback | Not present | **NOT IMPLEMENTED** |
| D fence/lineage serialization shares the Canonical Authority DB lock domain; barrier cannot close before exact participant resolution | No live D fence/lineage tables or D API used in the probes | **NOT IMPLEMENTED** |
| Restore reconciles COC prefix, I terminal decision, D fence/high-water and Storage XID before serving | Physical restore and WAL PITR fixtures exist; stale-control fixture uses synthetic local epoch | **PARTIAL** — no authenticated external I/D high-water or RecoveryQuarantined integration |

### Required Storage implementation sequence

1. Obtain the exact canonical runtime repository/branch/commit, runtime entrypoint, DB adapter and schema/migration path. The default branch of this architecture repository contains no executable runtime; see §27.
2. Bind the production Canonical Authority DB identity and a durable preallocated-XID allocator to the owner PublicationIntent and exact immutable operation tuple.
3. Implement the Storage-side PreparedParticipantReceipt signer/verifier and idempotent same-XID lookup/recovery. Do not create a replacement XID after lost ACK.
4. Integrate the COC API/schema for pre-prepare intent registration, prepared-receipt registration, unresolved-participant enumeration, authoritative prefix read and participant-resolution/reconciliation records.
5. Integrate I's authenticated owner-final-gate API and authoritative decision lookup. Storage must execute only the exact I terminal outcome and must not infer terminality from COC.
6. Bind D's target/source/ancestor fence rows, producer/attempt/lease rows, dependency/manifest versions and fence barrier to the same Canonical Authority DB serialization transaction.
7. Run the I-accepted JF10-COC-01..10 campaign plus D fence race cases against the actual application read/write path, including I COMMIT while COC is unavailable, I ABORT while COC is unavailable, and restore behind external control-ledger high-water.

No Storage fixture in this dossier is evidence that these bridge integrations exist. Until the production runtime and owner APIs are supplied, the current PostgreSQL 18.7 work remains bounded engine-capability qualification.

Gate A remains PARTIAL PASS / OPEN; Gate B remains BLOCKED; Gate C remains BLOCKED; JF-10 P0 remains OPEN; production activation NOT AUTHORIZED; Multi-PolicyDomain BLOCKED.

## Current architecture-phase gate correction and latest regression (2026-11-17)

The project owner confirmed this is the architecture-design phase; no production code repository/runtime is expected yet. Set `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. Production runtime/adapter absence is not a Gate A architecture blocker. The earlier statement that Gate B is blocked until production implementation/runtime binding is available is superseded for architecture design.

Storage published the COC durable protocol specification at `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`. It defines the durable quorum log, membership epoch, immutable participant registry, linearizable read/write APIs, outage recovery batch, snapshot/restore fencing, compaction and crash matrix. Gate B is now **SPECIFICATION PUBLISHED / EXACT OWNER REVIEW PENDING / NOT PASSED**. Gate C remains deferred to engineering-phase executable integration and fault injection.

The latest complete PostgreSQL 18.7 capability regression is 7/7 SUCCESS:

| Capability | Run | Job |
|---|---:|---:|
| Prepared-XID PITR / visibility / receipt / exact WAL negatives | `43958775001` | `133620265141` |
| Prepared-XID persistence/restart | `43959079736` | `133621314502` |
| Synchronous standby promotion | `43959079669` | `133621315610` |
| Physical backup/restore | `43959079703` | `133621314624` |
| Explicit-LSN WAL PITR | `43959079745` | `133621314724` |
| Synchronous standby unavailable fail-closed | `43959079760` | `133621315188` |
| Old-primary pg_rewind/rejoin | `43959079930` | `133621314973` |

These are pinned PostgreSQL 18.7 CI capability results and isolated fixtures, not production application-path or real I/D/COC service integration. Gate A remains PARTIAL PASS / OPEN pending architecture specification and exact owner acceptance; JF-10 P0 remains OPEN; production activation is NOT AUTHORIZED.

## 29. Storage Owner decision — COC infrastructure custody accepted at architecture level only (2026-11-17)

Storage has reviewed A's COC architecture proposal Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, including its three-voter quorum, linearizable append/read, durable checkpoints, restore fencing, owner-local outage gates and JF-10 participant bridge.

**Decision: ACCEPT WITH CONDITIONS at the architecture/infrastructure-custody level. PRODUCTION DEPLOYMENT AND OPERATIONAL ACCEPTANCE NOT GRANTED.**

### Accepted architecture profile

1. One logical COC service backed by a crash-fault-tolerant replicated state machine, initially three voters across three genuinely independent failure domains with a two-voter quorum.
2. Raft or an equivalently proven consensus protocol; no multi-leader, last-write-wins, async-replica acknowledgement or node-local commit semantics.
3. A quorum-durable append-only log with immutable `CoordinatorEpoch`, `CoordinatorIndex`, `EntryDigest`, `PreviousEntryDigest` and `CausalOrderDomainRef`.
4. Linearizable append and read. A committed position is returned only after quorum durable commit. Stale follower reads cannot authorize admission, finalization, barrier release or owner completion.
5. Quorum-certified snapshots/checkpoints, full-prefix continuity verification, rollback protection and `RESTORE_FENCED` on missing/stale checkpoint, digest gap or owner high-water mismatch.
6. Unresolved/IN_DOUBT participants, request cutoffs and owner high-water evidence are retained; no TTL, heuristic cleanup or operator force-clear.
7. COC remains a neutral causal-order and participant-accounting/observation service. It is not I's policy-domain sequencer, does not decide JF-10 COMMIT/ABORT, does not mint owner proofs, and does not override C/I/D authority. Storage's Canonical Authority DB participant remains the sole executor of the exact XID and local atomic visibility transaction.

### Storage custody accepted

At the architecture level, Storage accepts responsibility to design and technically steward the COC persistence/replication substrate, checkpoint/snapshot lifecycle, restore-fencing mechanism, retention controls, observability and SLO proposal. This does not transfer ownership of COC record semantics, C/I/D decisions, H wire contracts, or G Applied semantics to Storage.

### Conditions before concrete product selection or deployment

No consensus product/vendor, cloud, region/AZ, disk durability class, KMS/HSM, network topology, backup medium, retention period, data residency, RPO/RTO, SLO, budget or named human operator/on-call is designated by this acceptance. These cannot be invented from a CI container or architecture diagram.

Before production activation, Storage requires:
- named three independent failure domains and a tested quorum-loss/leader-election/fencing profile;
- concrete consensus implementation/version/build, config and durable-media profile;
- workload identity, owner signing-key verification, encryption/key custody, key rotation and compromise response approved by Security/I;
- two-person admin controls for restore, checkpoint rollback exception, key compromise and conflict reconciliation;
- independently retained quorum-certified checkpoints plus complete log archive, freshness proof and rollback protection;
- executable node/leader loss, minority partition, lost append/read ACK, duplicate append, stale follower, node replacement, snapshot restore, missing-prefix, corruption and total-cluster restore tests;
- COC outage local pending gates and atomic recovery-cutoff batch conformance (COC-13..16) plus JF-10 bridge cases (JF10-COC-01..10);
- signed retention, data residency, RPO/RTO, SLO, runbook, monitoring, escalation and named operator/on-call acceptance.

**No production custodian/on-call commitment is implied.** The current repository contains no deployed COC service, no selected consensus implementation, no actual failure-domain map and no operational owner designation. The architecture-level Storage acceptance must not be read as deployment readiness.

Gate A remains PARTIAL PASS / OPEN; Gate B remains BLOCKED until Gate A and COC deployment evidence pass; Gate C remains BLOCKED; JF-10 P0 remains OPEN; production activation NOT AUTHORIZED; Multi-PolicyDomain BLOCKED.


The COC protocol reference has been updated to Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25` (commit `1b70f164e4a5834d36dc4b3dd1644c57309312c2`); §13 clarifies the COC commit receipt and crash-fault/RPO boundary. This is architecture protocol evidence, not an implementation claim.


## 30. Prepared-XID / visibility / receipt PITR — successful bounded campaign (2026-11-17)

**Result: PASS for the pinned PostgreSQL 18.7 CI fixture only.** Workflow run `43958775001` / job `133620265141` completed SUCCESS on tested source commit `d026add5cfaec0c395537e8763317cdbd8255398`. Current branch source blobs are identical to the tested blobs: probe `63506807be82b3203e7e682b0772452621c92558`; workflow `a055d311c324d09eb6ebf4054247761116795eb7`. [Run and logs](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43958775001).

### Exact target capture

| Recovery point | Target LSN | Timeline | Required archived WAL |
|---|---|---:|---|
| Prepared / in-doubt | `0/5004710` | 1 | `000000010000000000000005` |
| After COMMIT | `0/6000000` | 1 | `000000010000000000000006` |
| After ROLLBACK | `0/6000110` | 1 | `000000010000000000000006` |

The probe emits and checks the exact target WAL archive file for each target before restore. The previous rollback target sampling/archive defect is therefore fixed for this tested fixture revision.

### Verified invariants

- The authoritative-reader fixture rejects pointer-only and receipt-only rows.
- At the prepared target, both exact GIDs remain in `pg_prepared_xacts`, each retains its transaction-ID lock, and pointer/receipt rows remain private.
- Resolving the restored exact GIDs by same-XID COMMIT and ROLLBACK produces the expected visible/absent states.
- At the committed target, VisibilityPointer + PublicationReceipt + authoritative-reader row are all present together, while the rollback GID remains prepared.
- At the rollback target, the rollback GID is resolved and neither pointer nor receipt exists.
- Removing, corrupting or truncating the exact target WAL segment causes recovery to fail before reaching the configured target; no writable primary or authoritative service is exposed. Logs include exact missing-file, wrong-size/truncated-segment and invalid-WAL-magic/recovery-target failures.

### Limits and disposition

This probe uses synthetic local tables, a synthetic authoritative-reader view, isolated prepared transactions and disposable Docker volumes. It does not test the real production read path or any live COC, I or D service. It does not prove signed participant receipts, I's owner-final-gate/authorization consumption, COC participant registry/reconciliation, D fence/lineage serialization, authenticated owner high-water quarantine, production archive durability, independent failure-domain fencing or deployment operations.

This PASS supersedes prior FAILURE results for this exact probe revision, not the wider JF-10 gate. Gate A remains PARTIAL PASS / OPEN; Gate B DESIGN-LEVEL ACCEPTANCE COMPLETE WITH ENUMERATED EXCEPTIONS (not implementation/conformance PASS); Gate C deferred to engineering-phase executable integration/fault campaign; JF-10 runtime P0 OPEN; production activation NOT AUTHORIZED; Multi-PolicyDomain BLOCKED.
