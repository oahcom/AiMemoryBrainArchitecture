# JF-10 Storage Evidence Assessment — PostgreSQL 18.7 Candidate

- Assessment ID: P-JF10-STORAGE-EVIDENCE-001
- Prepared by: Session P coordinator (independent evidence reconciliation; not Storage/D/E/I Owner acceptance)
- Date: 2026-11-17
- Status: **EVIDENCE RECONCILED — GATE A PARTIAL PASS / OPEN**
- Scope: PostgreSQL 18.7 engine capability and isolated CI fixtures only; no production adapter or canonical deployment sign-off.

## 1. Executive disposition

The prior description of Storage evidence as merely a single-node prepared-XID probe is stale. Storage's current branch contains a materially expanded evidence dossier and a seven-workflow regression batch, all seven GitHub Actions runs reporting SUCCESS against the pinned PostgreSQL 18.7 image.

The evidence supports the following bounded statement:

> PostgreSQL 18.7 has demonstrated, in isolated CI fixtures, durable prepared-XID behavior, lock retention, same-XID resolution across tested process/primary-loss paths, synchronous-standby promotion, physical backup/restore, explicit-LSN PITR, prepared-XID PITR visibility boundaries, authoritative-reader rejection of pointer-only/receipt-only rows, and fail-closed behavior for missing/corrupt/incomplete WAL on the latest enhanced probe revision. The first enhanced run failed on an assertion-vocabulary mismatch; Storage corrected it and the complete seven-workflow batch now passes on the current probe blob.

It does **not** prove the project has selected PostgreSQL, nor that the production Canonical Authority adapter, I sequencer/COC, D fence/lineage state, E publication state, production visibility/read path, real infrastructure fencing, named operator, runbook or RPO/RTO are implemented and verified.

Therefore:
- PostgreSQL 18.7: **STRONG JF-10 TRANSACTIONAL CANDIDATE / CURRENT CI CAPABILITY BATCH 7/7 PASS**.
- Gate A: **PARTIAL PASS / OPEN**.
- Gate B: **BLOCKED pending Gate A full acceptance**.
- Gate C: **BLOCKED pending Gate B**.
- JF-10 P0: **OPEN**.
- Production activation: **NOT AUTHORIZED**.
- TEC-003 / TEC-004: **CANDIDATE / TO_VALIDATE; no final database decision**.

## 2. Exact source pins

Storage branch: `session-storage-consistency-forget-atomicity-2026-11-16`

- Current Storage branch HEAD: `e6e578766b081b6d450d6af7fc4d6d673f8afd53`.
- Current Storage dossier blob: `3d1c66e61334764013ddd253f18c07b52714fc77`.
- Current PITR probe blob: `9d2a85f9a5d53f91df247a310c38377e563d259d`; workflow blob: `a055d311c324d09eb6ebf4054247761116795eb7`.
- Current probe blob is identical to the tested probe at commit `2d476dd32ac020d329e8290ee2aaaa1f0c057c92`; current branch is three commits ahead of that test commit, with changes only to the Storage boundary acceptance, deployment readiness and dossier documents.
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

## 5. Architecture-phase acceptance boundary — implementation binding deferred

Storage's current readiness record explicitly clarifies that the project is in architecture-design phase and has no production runtime/adapter by design. Set `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`. The absence of production code in this repository remains a bounded inventory fact, but it is **not a Gate A architecture blocker** and must not be used to prevent Gate B design work.

Gate A architecture closure must instead specify:
1. engine/version/profile rationale and unresolved DB product decision;
2. isolation, D fence/lineage lock scope and linearization point;
3. prepared-XID durability, lock retention, same-XID resolution and in-doubt handling;
4. atomic VisibilityPointer + PublicationReceipt + owner outcome + receipt-consumption + outbox boundary;
5. authoritative read path and stale replica/cache exclusion;
6. PITR/WAL prefix continuity, missing/corrupt/incomplete archive fail-closed restore and control-ledger reconciliation;
7. HA/fencing/rejoin, failure-domain and topology constraints;
8. future engineering/operations acceptance criteria, including named operator, runbook, RPO/RTO and deployment profile.

Implementation binding, actual runtime/DB adapter, production fencing, operator/runbook and RPO/RTO are engineering/deployment-phase gates. They remain future acceptance requirements, not prerequisites for architecture Gate A closure.

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


## 11. Current enhanced-probe retest — PASS; supersedes §10 failure state

Storage corrected the corrupt-WAL diagnostic assertion to recognize PostgreSQL's actual `invalid magic number` diagnostic while retaining exact target-segment matching and mandatory no-writable/no-authoritative checks. The enhanced probe now completes the missing, corrupt and incomplete cases.

Exact current evidence:
- Current Storage branch HEAD: `fe7debe55da71e655eecfc46f25ec49eae43404a`.
- Current dossier blob: `b011683568857c73c5bfc0cfe1d9d56278fb6578`.
- Current readiness blob: `812d33d7a64107a890191ad7fae036fde7f319df`.
- Current COC protocol specification: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`.
- Current PITR probe blob: `63506807be82b3203e7e682b0772452621c92558`; workflow blob: `a055d311c324d09eb6ebf4054247761116795eb7`.
- Current prepared-XID probe blob: `184e0507fd225ee18f321f3f1ce6a63f869b13f3`; capability workflow blob: `fbcbce...`.
- Current branch is five commits ahead of the six-workflow test commit `83bdacbafa840808dca9be7a8c76c4df83c63504`; compare shows only readiness and dossier documents changed. Both probe blobs remain identical to the tested revisions.
- PITR run: `43957910909`, job `133617253176`, SUCCESS.
- Run URL: https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/43957910909

Raw log confirms:
- `AUTHORITATIVE_READER_REJECTS_POINTER_ONLY_AND_RECEIPT_ONLY=PASS`
- `PITR_PREPARED_XID_PRIVATE_AND_LOCKED=PASS`
- `PITR_COMMIT_POINTER_AND_RECEIPT_ATOMIC=PASS`
- `PITR_ROLLBACK_NO_POINTER_NO_RECEIPT=PASS`
- `PITR_MISSING_EXACT_WAL_FAILS_CLOSED=PASS`
- `PITR_MISSING_NO_WRITABLE_OR_AUTHORITATIVE_SERVICE=PASS`
- `PITR_CORRUPT_EXACT_WAL_FAILS_CLOSED=PASS`
- `PITR_CORRUPT_NO_WRITABLE_OR_AUTHORITATIVE_SERVICE=PASS`
- `PITR_INCOMPLETE_EXACT_WAL_FAILS_CLOSED=PASS`
- `PITR_INCOMPLETE_NO_WRITABLE_OR_AUTHORITATIVE_SERVICE=PASS`
- `JF10_PITR_WAL_NEGATIVE_CASES=PASS`
- `JF10_POSTGRESQL_PITR_ATOMICITY_AND_NEGATIVES=PASS`

The six other workflows on the same tested commit also completed SUCCESS:
- Prepared-XID: run `43957910975`.
- Synchronous failover: run `43957911188`.
- Physical backup/restore: run `43957911173`.
- Explicit-LSN WAL PITR: run `43957910971`.
- Synchronous standby unavailable: run `43957911270`.
- Old-primary rewind/rejoin: run `43957911036`.

Thus the current enhanced probe revision and all six supporting workflows have a 7/7 CI PASS batch. This closes the test-harness defect recorded in §10 / UMR-018 for the pinned PostgreSQL 18.7 CI profile. It does **not** close Gate A overall: the production Canonical Authority runtime/adapter is still NOT IDENTIFIED in the inspected repository, production I/D ledger integration and COC quorum deployment are unverified, and real infrastructure fencing, operator/runbook, RPO/RTO and production operational acceptance remain open. Gate A PARTIAL PASS / OPEN; Gate B BLOCKED; Gate C BLOCKED; JF-10 P0 OPEN; production activation NOT AUTHORIZED.


## 12. Project phase and Gate B sequencing correction

The current Storage readiness blob `5da030123e76e523f681d1262b8a31483df0e6b3` clarifies:
- `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`; no production code repository/runtime is expected during architecture design.
- Gate A remains PARTIAL PASS / OPEN for remaining storage architecture specifications and cross-owner decisions.
- Gate B COC persistence/quorum log/participant registry/recovery-cutoff design is authorized to proceed now in parallel with Gate A closure.
- Gate B design acceptance remains pending; this is not implementation PASS.
- Gate C implementation fault-injection is deferred until an implementation exists.
- JF-10 P0 remains OPEN; production activation NOT AUTHORIZED.

The same readiness document still contains stale statements later in the file that Gate B/C remain BLOCKED after it authorizes Gate B design. The correct state vector is: **Gate B specification PUBLISHED / exact Owner review PENDING / Gate B design acceptance OPEN / Gate B implementation NOT RUN / Gate C implementation tests DEFERRED**. The current Phase 3.6.3 protocol Blob `4ac63...` is a proposal, not an Owner-approved or implemented protocol.

A detailed review of the newly published Storage COC design is in `00-governance/reviews/storage-coc-durable-log-recovery-design-review.md`. It is a strong candidate with blocking amendments; it does not yet close Gate B.



## 13. Phase 3.6.3 COC protocol specification published

Storage published `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`, Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25`. It is a materially stronger architecture specification: Raft crash-fault model, durable quorum commit receipts, VoterConfigurationEpoch/joint membership, immutable record envelope, participant registry/state machine, linearizable APIs, I/D owner-local outage gates, recovery batch with participant-set digest, signed RecoveryReconciliationReceipt, checkpoint/WAL/PITR/restore fencing, retention and Gate B conformance plan.

Exact Owner review is still pending. Residual design issues recorded in `00-governance/reviews/storage-coc-durable-log-recovery-design-review.md`:
- no explicit quorum-committed recovery-epoch completion record;
- no exact COC RecordType ↔ H BMCP message/schema mapping;
- no repeated cutoff-batch loop for requests arriving during reconciliation;
- I-owned PolicyDomain/CausalOrderDomain registry authority not explicit;
- external anti-rollback anchor custody/failure domain not named;
- A Applied package companion pin remains fc3 while current A COC architecture is a3c51.

The readiness document §23.1/§23.4 says Gate B spec published / exact Owner review pending, but §29 still says Gate B blocked until Gate A and deployment evidence. UMR-023 tracks this inconsistency. Correct phase vector:
- Gate A: PARTIAL PASS / OPEN for remaining architecture specifications and exact Owner decisions.
- Gate B: specification PUBLISHED / exact Owner review PENDING / acceptance OPEN.
- Gate C: implementation fault-injection DEFERRED_TO_ENGINEERING_PHASE.
- Implementation binding: DEFERRED_TO_ENGINEERING_PHASE.
- JF-10 P0 OPEN; production activation NOT AUTHORIZED.



## 14. Current COC / JF-10 source and gate reconciliation — supersedes earlier Gate B wording

### 14.1 Current Storage source pins

- Current Storage branch HEAD: `337fe8bffa178e64ad8e4750f1ede1d561424edc`.
- Phase 3.6.3 COC protocol with §14 PreparedTransactionGID clarification: Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`.
- Current Storage Design v2 proposal: Blob `4ed4234ce548a814a9496adf7a14c4459ea9f7ce`.
- Current Storage readiness document Blob: `b9e664dfbed1c0f268b2b8b0d9c2ddcd29221bf1`.
- Current Storage prepared-XID dossier Blob: `0aabf66848dc97deee028c571183c0d7204008c0`.
- Storage COC self-review Blob `332de9192ccab6f18fc2a0d18700cc9585a98983` still pins prior COC protocol Blob `4ac63...`; it is historical/stale against the newer Storage acceptance in the dossier.

### 14.2 Exact gate vector

The earlier statements in §§1/12/13 that Gate B is simply “blocked pending Gate A” are superseded by the current Storage readiness vector:
- Gate A: **PARTIAL PASS / OPEN**.
- Gate B prior COC protocol Blob `4ac63...`: **DESIGN-LEVEL ACCEPTANCE WITH EXCEPTIONS**.
- Gate B amended COC protocol Blob `86ff3...`: **PUBLISHED / FOCUSED EXACT-OWNER REVIEW PENDING**. Storage accepts with conditions; A/H/I role-simulated reviews exist, but A has enumerated amendments and H/I have no approval. Independent exact-version decisions remain pending.
- Storage Design v2 Blob `4ed423...`: **FRESH PROPOSAL / EXACT OWNER REVIEW PENDING**. It is not accepted by the old `4ac63...` matrix.
- Gate B implementation/conformance: **NOT RUN / DEFERRED_TO_ENGINEERING_PHASE**.
- Gate C distributed fault-injection: **DEFERRED_TO_ENGINEERING_PHASE**.
- JF-10 P0: **OPEN**; Multi-PolicyDomain: **BLOCKED**; production activation: **NOT AUTHORIZED**.

### 14.3 Storage Design v2 advances

The current v2 Blob `4ed423...` materially addresses the earlier design gaps and contains a Storage proposal disposition for A's R1–R6 findings:
- immutable participant manifest and two-stage recovery-batch commit;
- explicit repeated cutoff-batch behavior for requests arriving after a snapshot;
- per-owner signed local gate release and explicit RECOVERY_EPOCH_COMPLETED;
- exact C/I/D/Storage participant and provider-invocation gates;
- PreparedParticipantRef / PreparedTransactionGID / NativeXidObserved separation and DB identity evidence.

It remains a proposal requiring fresh exact Owner review. Issue #16 is open; A/I/H reviews are role-simulated, D/C decisions are still required, and B/E/G should provide targeted type/producer/Applied-consumption review.

### 14.4 Prepared participant trust / wire blockers

A's Prepared GID review Blob `c869cf594e8d5b6fcd6343992836da178227ebf5` is ACCEPT WITH ENUMERATED AMENDMENTS, including:
1. non-reusable DatabaseIncarnationRef;
2. immutable PrepareAttempt identity/generation;
3. authoritative PREPARED readback before a signed receipt;
4. original prepare coordinates separated from recovery observations;
5. atomic I terminal proof consumption of the exact Storage receipt/participant/DB incarnation/operation digest.

H's strict wire review Blob `db0379c3a0ab598c7d2e47229309d2a075ccd3cb` and I's signature/trust review Blob `7545dc1f74e6cfda17701b9c053fe342a8b01d44` both conclude CANDIDATE / NO APPROVAL. All three reviews disclose coordinating-session role simulation, not independent signatures.

Remaining cross-artifact gaps:
- Common JF-10 protocol Blob `94679897e84a6f58fd8b9467b5249e1a885cb0b0` still uses generic preallocated-XID / same-XID language.
- Storage readiness §26.2 still says “preallocate the exact XID” without the GID/native-XID distinction.
- H schema Blob `a8a945cc3623c2907003b93625e3c79742150944` has opaque `preallocated_storage_xid_ref` and `storage_xid_ref`; H must explicitly map or replace these with nominal types and receipt fields.
- B typed-reference model has not yet added PreparedParticipantRef, PreparedTransactionGID, NativeXidObserved, DatabaseIncarnationRef and PrepareAttempt types.
- v2 record names and commit-proof envelope must be mapped to protocol `86ff3...` and H BMCP RecordTypes, including VoterConfigurationEpoch / COCCommitReceipt semantics.

### 14.5 Current model/test evidence — bounded claims

- PostgreSQL 18.7 capability suite: **7/7 PASS** for the pinned isolated fixture/code set. This remains strong capability evidence, not production selection/deployment.
- F anti-resurrection reference model: **19/19 PASS**; logical model only.
- H schema + strict parser reference tests: **23/23 PASS**; candidate schema/parser only.
- I Global Forget reference model: **30/30 PASS**; logical model only.
- COC in-memory outage model and JF-10 semantic validator are separate reference suites (11 and 18 tests), not a distributed COC/Raft service.

I36-GOV-01..10 remain proposal-only; no external governance approval, production target inventory seal, recipient/backup evidence or physical-erasure proof is established.

### 14.6 Current issue state

- Issue #14: A R1–R6 remains open; Storage v2's disposition is not independent Owner acceptance.
- Issue #15: exact review of amended protocol Blob `86ff3...` remains open.
- Issue #16: exact review of Storage Design v2 Blob `4ed423...` remains open.
- Issue #17: Prepared GID / signed wire / trust review remains open; A conditional, H/I no approval in role-simulated artifacts.

