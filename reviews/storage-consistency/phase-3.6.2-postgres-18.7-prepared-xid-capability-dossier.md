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
