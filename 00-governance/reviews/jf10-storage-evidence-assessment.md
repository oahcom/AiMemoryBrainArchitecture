# JF-10 Storage Evidence Assessment — PostgreSQL 18.7 Candidate

- Assessment ID: P-JF10-STORAGE-EVIDENCE-001
- Prepared by: Session P coordinator (independent evidence reconciliation; not Storage/D/E/I Owner acceptance)
- Date: 2026-11-17
- Status: **EVIDENCE RECONCILED — GATE A PARTIAL PASS / OPEN**
- Scope: PostgreSQL 18.7 engine capability and isolated CI fixtures only; no production adapter or canonical deployment sign-off.

## 1. Executive disposition

The prior description of Storage evidence as merely a single-node prepared-XID probe is stale. Storage's current branch contains a materially expanded evidence dossier and a seven-workflow regression batch, all seven GitHub Actions runs reporting SUCCESS against the pinned PostgreSQL 18.7 image.

The evidence supports the following bounded statement:

> PostgreSQL 18.7 has demonstrated, in isolated CI fixtures, durable prepared-XID behavior, lock retention, same-XID resolution across tested process/primary-loss paths, synchronous-standby promotion, physical backup/restore, explicit-LSN PITR, prepared-XID PITR visibility boundaries, and fail-closed behavior for missing/corrupt/incomplete WAL on the earlier successful probe revision. The current enhanced probe adds authoritative-reader negative cases and stricter exact-WAL assertions, but its latest run is FAILING at the corrupt-WAL diagnostic assertion; the incomplete-WAL case has not yet run on that revision.

It does **not** prove the project has selected PostgreSQL, nor that the production Canonical Authority adapter, I sequencer/COC, D fence/lineage state, E publication state, production visibility/read path, real infrastructure fencing, named operator, runbook or RPO/RTO are implemented and verified.

Therefore:
- PostgreSQL 18.7: **STRONG JF-10 TRANSACTIONAL CANDIDATE / PARTIAL CI CAPABILITY PASS; CURRENT DEEP-PITR PROBE REVISION FAILING**.
- Gate A: **PARTIAL PASS / OPEN**.
- Gate B: **BLOCKED pending Gate A full acceptance**.
- Gate C: **BLOCKED pending Gate B**.
- JF-10 P0: **OPEN**.
- Production activation: **NOT AUTHORIZED**.
- TEC-003 / TEC-004: **CANDIDATE / TO_VALIDATE; no final database decision**.

## 2. Exact source pins

Storage branch: `session-storage-consistency-forget-atomicity-2026-11-16`

- Current Storage branch HEAD: `3c8ab8ee4579a550300aa48aecab928149cf9370`.
- Current Storage dossier blob: `2f76ca8b8c19b84c37e7604cd254990dd93eb8b1`.
- Current PITR probe blob: `7fa4bb3fb07eacc3f708f5682ea4c9e2019f267d`; workflow blob: `a055d311c324d09eb6ebf4054247761116795eb7`.
- Current Storage HEAD is eight commits ahead of the successful evidence commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`; the PITR probe has materially changed and must be re-run.
- Current executable conformance plan blob: `49056cd46fd30445c0e564c99e0e234f60f065c4`.
- PITR atomicity probe blob: `8c0e281f1db4dd6190127f02ac71b1126da39903`.
- Pinned image: `postgres:18.7@sha256:2ea8630df176ad090ec92136dee850397c5af8781e4bcf2e4162593691c61bbc`.
- Evidence regression commit: `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`.
- Current Storage HEAD is six commits ahead of that evidence commit and not behind it; the latest commits update deployment-readiness and evidence-dossier documents. The test results are pinned to the earlier exact commit, not silently attributed to later source.

## 3. Seven-workflow regression evidence

All seven runs below are completed with conclusion SUCCESS. Each has one job and the relevant test/probe step completed successfully.

| Capability | Run ID | Job ID | Result |
|---|---:|---:|---|
| Prepared-XID + restart | 43955195289 | 133607790416 | SUCCESS |
| Synchronous standby promotion | 43955195323 | 133607790413 | SUCCESS |
| Physical backup/restore | 43955195219 | 133607790737 | SUCCESS |
| Explicit-LSN WAL PITR | 43955195388 | 133607790699 | SUCCESS |
| Prepared-XID PITR + archive negatives | 43955195460 | 133607791713 | SUCCESS |
| Synchronous standby unavailable / fail-closed | 43955195197 | 133607790658 | SUCCESS |
| Old-primary rewind/rejoin | 43955195256 | 133607790520 | SUCCESS |

Run URLs:
- https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195289
- https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195323
- https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195219
- https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195388
- https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195460
- https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195197
- https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43955195256

The Storage dossier records the final PASS markers and detailed scope limits. The CI run/job conclusions were independently checked against GitHub Actions metadata in this reconciliation. This assessment did not download or independently re-hash the raw log archives; raw marker descriptions are attributed to the Storage dossier.

## 4. Highest-value atomicity evidence

The dedicated PITR probe uses isolated `jf10_*` fixture tables, explicitly not production COC or I/D tables. It:
1. creates two prepared transactions, each with paired VisibilityPointer and PublicationReceipt rows;
2. takes a physical base backup while both transactions are prepared;
3. resolves one with COMMIT PREPARED and the other with ROLLBACK PREPARED;
4. restores at prepared, commit and rollback LSN boundaries;
5. checks exact prepared XIDs, lock retention and reader-visible pointer/receipt state;
6. runs missing, corrupt and incomplete WAL archive negative cases.

The Storage dossier reports these PASS markers:
- `PITR_PREPARED_XID_PRIVATE_AND_LOCKED=PASS`
- `PITR_COMMIT_POINTER_AND_RECEIPT_ATOMIC=PASS`
- `PITR_ROLLBACK_NO_POINTER_NO_RECEIPT=PASS`
- `PITR_MISSING_WAL_FAILS_CLOSED=PASS`
- `PITR_CORRUPT_WAL_FAILS_CLOSED=PASS`
- `PITR_INCOMPLETE_WAL_FAILS_CLOSED=PASS`

This is valuable engine capability evidence for the invariant that prepared work stays private, a committed fixture pointer and receipt appear together, and rollback leaves neither visible. It is not the production I/D/Storage transaction or COC implementation.

Additional dossier evidence includes a real TCP CommandComplete response-loss probe (run 43913477785), coordinator process-crash/ACK-gap recovery, synchronous standby unavailable fail-closed behavior, and a single-runner Docker old-primary fencing/rewind/rejoin simulation. Each is bounded by the dossier's explicit limitations.

## 5. Production implementation stop condition

The Storage dossier's recursive tree audit explicitly reports no production runtime source tree, service executable, Canonical Authority DB adapter, migration package or application deployment manifest in the inspected repository branch. The repository README on main also describes the repository as architecture definition with implementation not started by design.

This is the decisive remaining gap. Before Gate A can close, the accountable Owner must:
1. identify the canonical implementation repository and branch, or explicitly designate this repository as the implementation home;
2. pin the runtime entrypoint, DB adapter, schema/migration path and build SHA;
3. trace the actual authoritative write/read path for prepared XID, D/lineage locks, VisibilityPointer, PublicationReceipt, owner outcome, receipt consumption and outbox;
4. map I sequencer/COC durable decision and D fence ordering to the actual implementation;
5. run the production-equivalent crash, ACK-loss, failover, PITR, WAL-negative and restore campaign against that exact path;
6. bind real infrastructure fencing/STONITH, split-brain prevention, archive retention/immutability, human operator, runbook, RPO/RTO and deployment profile.

Until this exists, the CI fixtures cannot be promoted to production conformance.

## 6. Database decision implication: SQLite versus PostgreSQL

TAB-001 recommends SQLite + WAL only as a first single-node prototype candidate, while PostgreSQL is a comparison/evolution candidate. The current Storage evidence changes the relative evidence position but does not approve a final DB.

Relevant primary documentation:
- PostgreSQL 18 `PREPARE TRANSACTION`: https://www.postgresql.org/docs/18/sql-prepare-transaction.html
- PostgreSQL 18 two-phase transactions: https://www.postgresql.org/docs/18/two-phase.html
- PostgreSQL 18 `max_prepared_transactions`: https://www.postgresql.org/docs/18/runtime-config-resource.html
- SQLite WAL: https://www.sqlite.org/wal.html
- SQLite isolation/concurrency: https://www.sqlite.org/isolation.html

PostgreSQL documents a native SQL-level two-phase transaction lifecycle: PREPARE TRANSACTION stores prepared state on disk; later sessions can COMMIT PREPARED or ROLLBACK PREPARED; prepared transactions retain locks and must be resolved by an external transaction manager. The feature must be enabled/configured, and the PostgreSQL documentation warns against long-lived prepared transactions because they retain locks and interfere with VACUUM / transaction-ID wraparound.

SQLite WAL documentation describes atomic commit through WAL records, readers/writers concurrency, same-host shared-memory requirements and a single writer at a time. Its documented SQL transaction/WAL model is not the PostgreSQL external-transaction-manager PREPARE/COMMIT PREPARED protocol. Thus SQLite WAL cannot be treated as a drop-in implementation of the exact prepared-XID participant contract.

Decision-support conclusion:
- If JF-10 requires a durable prepared participant whose exact XID and locks survive restart and are later resolved by an external sequencer, PostgreSQL currently has direct native protocol support plus actual pinned CI capability evidence.
- SQLite may remain viable for a simpler single-node canonical store only if D/E/I/Storage define and prove a different durable participant/intent protocol that preserves the same invariants without pretending SQLite has native prepared transactions.
- Do not select SQLite for the authoritative JF-10 participant merely because it is operationally lightweight.
- Do not select PostgreSQL as production DB merely because isolated CI probes pass.
- Keep TEC-003/004 open until production adapter, deployment and operational evidence is bound.

## 7. Remaining evidence matrix

| Requirement | Current evidence | Remaining blocker |
|---|---|---|
| Native prepared-XID persistence | PostgreSQL CI probe PASS | Production adapter mapping |
| Prepared lock retention | CI restart/PITR probes PASS | Production lock scope and bounded in-doubt operations |
| Same-XID commit/rollback | CI probes PASS | Real I decision log/COC integration |
| VisibilityPointer + receipt atomicity | Isolated fixture PASS | Actual schema and canonical reader path |
| Primary-loss promotion | CI synchronous standby PASS | Production fencing/STONITH and quorum safety |
| Old-primary rejoin | Docker simulation PASS | Independent infrastructure fencing and HA manager |
| Backup/restore and PITR | CI fixture PASS | Production archive retention, immutability, off-site recovery, RPO/RTO |
| Missing/corrupt/incomplete WAL | CI negatives PASS | Production restore quarantine/control-ledger reconciliation |
| D fence/lineage ordering | Reference protocol/model and fixture design | Shared real DB transaction and D implementation |
| I sequencer/COC | Architecture/protocol only | Production durable coordinator and authorization |
| E compiler publication | Architecture/protocol only | Runtime work-item/lease/manifest integration |
| Human operations | Not identified | Named operator, runbook, alerting, drills |

## 8. Required Owner actions

- Storage: maintain the exact evidence dossier and expose raw run artifacts/log hashes; identify the runtime adapter or document its absence.
- D: confirm exact D fence/lineage lock and barrier mapping against the tested PostgreSQL transaction semantics.
- E: confirm stable WorkItemId/PublicationOperationId, lease fencing and publication receipt mapping.
- I: confirm the sequencer/COC durable decision, authorization receipt and failover/fencing integration; PostgreSQL capability cannot establish I policy correctness.
- A: record a gate vector that distinguishes engine capability PASS from production implementation NOT IDENTIFIED.
- Project governance authority: approve any final technology ADR only after Owner evidence and required ADR authority are established.

No Session P action in this assessment changes a Storage/D/E/I Owner decision, selects a production database, closes JF-10 P0, or authorizes production activation.

## 9. Final verdict

**PostgreSQL 18.7 candidate capability evidence: PASS for the tested isolated CI profile.**

**JF-10 Gate A: PARTIAL PASS / OPEN.** The key missing item is no longer a generic database capability test; it is the mapping from the capability to the actual production Canonical Authority runtime, I/D/E integration and operational deployment.

**Technology baseline: NOT FROZEN.** TEC-003 and TEC-004 remain candidate/open pending the implementation binding and Owner/ADR decisions.


## 10. Current-source regression re-run — enhanced PITR probe FAILED

The Storage branch has advanced to `3c8ab8ee4579a550300aa48aecab928149cf9370`, eight commits beyond the earlier all-green evidence commit `8b8c749017bf09d6aa01a7d858b48f910ec5b1bd`. The current PITR probe is a materially expanded revision:
- Current probe blob: `7fa4bb3fb07eacc3f708f5682ea4c9e2019f267d`.
- Workflow blob: `a055d311c324d09eb6ebf4054247761116795eb7`.
- Current run: `43957456225`, job `133615673051`, conclusion **FAILURE**.
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43957456225

### 10.1 New checks that passed before the failure

The current probe adds an authoritative publication read-path fixture and stricter exact target-WAL/timeline checks. Raw job log confirms:
- `AUTHORITATIVE_READER_REJECTS_POINTER_ONLY_AND_RECEIPT_ONLY=PASS`
- `PITR_PREPARED_XID_PRIVATE_AND_LOCKED=PASS`
- `PITR_COMMIT_POINTER_AND_RECEIPT_ATOMIC=PASS`
- `PITR_ROLLBACK_NO_POINTER_NO_RECEIPT=PASS`
- `PITR_MISSING_EXACT_WAL_FAILS_CLOSED=PASS`
- `PITR_MISSING_NO_WRITABLE_OR_AUTHORITATIVE_SERVICE=PASS`

The exact target segment/timeline mapping was emitted and the target WAL files were confirmed archived.

### 10.2 Failure is currently an assertion-vocabulary mismatch, not evidence of unsafe promotion

The corrupt-WAL case failed at the diagnostic assertion. PostgreSQL's raw log contains:
`invalid magic number D158 in WAL segment 000000010000000000000006`
followed by:
`FATAL: recovery ended before configured recovery target was reached`.

The current test assertion for the corrupt case accepts `wrong size`, `invalid record` or `incorrect checksum`, but not PostgreSQL's observed `invalid magic number`. The test therefore raises AssertionError before it reaches the subsequent query asserting `pg_is_in_recovery()=true` and `transaction_read_only=on`. The container exits during recovery and does not become a writable promoted service, but the intended negative case is not fully verified because the assertion stopped early. The incomplete-WAL case is not reached in this failed run.

### 10.3 Required Storage correction

1. Include the observed `invalid magic number` diagnostic as a recognized corrupt-WAL failure, while retaining exact required target-WAL filename matching.
2. Keep the post-failure no-writable/no-authoritative-service assertion mandatory and ensure it runs for both queryable read-only recovery and non-queryable startup failure.
3. Re-run the entire enhanced probe so missing, corrupt and incomplete cases all execute.
4. Publish the new run/job, raw log, exact target LSN/timeline/segment mapping, and current probe/workflow blobs.
5. Keep the authoritative reader negative fixture and pointer-only/receipt-only cases in the test; they are meaningful improvement.

### 10.4 Current branch batch status

On current Storage HEAD `3c8ab8ee4579a550300aa48aecab928149cf9370`:
- Prepared-XID: run `43957456300` — SUCCESS.
- Synchronous failover: run `43957456184` — SUCCESS.
- Backup/restore: run `43957456777` — SUCCESS.
- Explicit-LSN WAL PITR: run `43957456393` — SUCCESS.
- Synchronous standby unavailable: run `43957456200` — SUCCESS.
- Old-primary rewind/rejoin: run `43957456416` — SUCCESS.
- Enhanced prepared-XID PITR + exact-WAL negatives: run `43957456225` — FAILURE.

Thus the earlier seven-workflow success batch remains valid for its exact older commit, but the current branch regression batch is **6/7 PASS, 1/7 FAIL**. The overall Gate A disposition remains PARTIAL PASS / OPEN. No production adapter, real I/D control-ledger integration, COC quorum deployment, production fencing, operator/runbook or RPO/RTO is proven.
