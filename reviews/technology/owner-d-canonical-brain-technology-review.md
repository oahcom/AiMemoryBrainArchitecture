# D — Canonical Memory Brain Technology Architecture Review

- Document: TAR-D-001
- Owner perspective: D — Canonical Memory Brain Architect
- Execution mode: centralized delegated review by the project integration assistant; not an independent human-owner attestation.
- Branch: `session-d-memory-brain-2026-11-16`
- Reviewed branch HEAD: `9dd48eddb3c8f91d15dfa6981a7f53cc70bd4bf8`
- TAB-001 blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- D Forget fence contract blob: `1f0391bc49d007c44ec74165bd33d37412cc7990`
- D publication gate blob: `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`
- D/E/Storage joint linearization decision blob: `1b6a312ecffd3947bbb4df59f902242482c98a40`
- Date: 2026-11-17
- Verdict: **CONDITIONAL PASS for semantic architecture; BLOCKED for storage selection and implementation acceptance.**

## 1. Executive verdict

TAB-001 correctly recommends a local-first transactional store as a prototype and explicitly refuses to equate SQLite WAL with proof of Forget atomicity. D's semantic contracts now specify the required ordering and publication predicate. The remaining gap is substantial: a physical Storage implementation must realize one authoritative serialization domain spanning producer admission, fence installation, complete dependency registration, final visibility commit and terminal barrier disposition, with recoverable receipts.

SQLite WAL is a viable prototype candidate, not an accepted implementation. PostgreSQL may provide a more suitable transaction/concurrency substrate if the required serialization and recovery properties cannot be demonstrated in SQLite. An ordinary Storage interface that decomposes the predicate into read-then-write calls is invalid.

## 2. R1–R6 assessment

| Dimension | Verdict | Evidence and gap | Impact |
|---|---|---|---|
| R1 Requirements/workload | CONDITIONAL | D contracts specify canonical revisions, global per-authority CanonicalCommitCursor, lifecycle cursor and Forget semantics. Throughput/concurrency/latency envelope is not measured. | Cannot choose DB from feature checklist alone. |
| R2 Boundaries/dependencies | CONDITIONAL | D owns semantic authority; E producer lifecycle, I authorization, Storage physical atomicity, F/G derived consumers. | Requires one shared commit/visibility boundary. |
| R3 Technology selection | BLOCKED for selection | SQLite WAL recommended as prototype; PostgreSQL and KV alternatives not compared by executable tests. | No database freeze. |
| R4 Resources | NOT MEASURED | Writer contention, WAL growth/checkpoint, blob IO, backup throughput, concurrent sessions and disk-full behavior unknown. | Local deployment sizing not proven. |
| R5 Recovery | BLOCKED | Joint decision is recorded but explicitly not implementation verified; race/fault fixtures not run. | Forget barrier and late-publication safety unproven. |
| R6 Compatibility | CONDITIONAL | Cursor/generation/epoch namespaces are explicit; callable APIs, receipt schema and Storage consistency semantics remain open. | No cross-owner integration acceptance. |

## 3. Findings

### TAR-D-P0-001 — Shared linearization boundary for Forget and derived visibility not implemented/proven

- Evidence: D gate blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`; joint decision blob `1b6a312ecffd3947bbb4df59f902242482c98a40`.
- Required order includes RegisterProducerWork, InstallForgetFence, complete RegisterDerivedDependency, final publication visibility commit and barrier-visible terminal disposition.
- Consequence: separate “check fence” then “write artifact” allows a fence to win between check and visibility; stale workers can resurrect suppressed derivatives.
- Recommendation: prototype a single durable transaction/serializable coordinator per Canonical Memory authority. The final visible marker and PublicationReceipt must commit atomically with current fence, current I authorization, active lease/attempt and complete dependency receipt checks. Any ambiguous outcome remains private/UNKNOWN.
- Owners: Storage/Consistency with D/E/I.
- Closure: deterministic interleaving tests for admission/fence, dependency/fence, publication/fence; crash/ACK-loss/failover/restore evidence; D/E/Storage sign-off.

### TAR-D-P0-002 — Canonical commit/cursor/revision atomicity must be demonstrated on chosen engine

Canonical record/head mutation, immutable revision, lifecycle event, CanonicalCommitCursor record and outbox intent must be atomic or governed by a proven recoverable protocol. Cursor visibility cannot precede durable commit; gaps, duplicate cursor assignment and stale head CAS must be tested.

### TAR-D-P1-001 — SQLite WAL is not sufficient evidence

Validate BEGIN IMMEDIATE/transaction mode, busy timeout, writer serialization, WAL checkpointing, process crash, disk full, backup API/snapshot coordination and multi-process writer behavior. Test real transaction operations, not a mocked Storage trait. Compare PostgreSQL serializable/locking behavior under the same contract and workload. KV engines remain deferred unless SQL approaches fail measured needs.

### TAR-D-P1-002 — Blob/database publication boundary is underspecified

Content-addressed blob writes can precede DB registration and create orphaned bytes; DB references cannot become visible before durable blob integrity verification. Define digest/length verification, staging ACL, atomic metadata registration, orphan reconciliation and backup consistency. A DB-only backup is incomplete when referenced blobs are absent.

### TAR-D-P1-003 — Receipt and unknown-outcome recovery need callable schemas

Stable operation IDs and request digests must resolve original registration/fence/dependency/publication/terminal receipts after ACK loss. Unknown is not success or permission to mint a new semantic operation. Define read-after-commit consistency and replica/failover guarantees.

## 4. Technology disposition

| Technology | Disposition | Conditions |
|---|---|---|
| SQLite + WAL | ACCEPT AS FIRST PROTOTYPE | Not production-approved; pass race, crash, concurrency, restore and backup tests. |
| PostgreSQL | REQUIRED COMPARISON CANDIDATE | Same workload and correctness harness; assess operational burden versus transaction guarantees. |
| RocksDB / embedded KV | DEFER | Revisit only if measured workload proves SQL unsuitable and application-level atomicity remains demonstrable. |
| Rust Storage port | RECOMMEND | Port must expose atomic domain operations, not generic read/check/write sequences. |
| Content-addressed filesystem blobs | ACCEPT AS CANDIDATE | Staging, integrity, atomic visibility, encryption and backup contract required. |
| Outbox | RECOMMEND | Durable intent in same transaction as authoritative state transition. |
| Distributed coordinator | DEFER | No evidence justifies it for first local deployment; any later use needs explicit linearizability proof. |

## 5. Failure/recovery matrix

| Failure/race | Required behavior | Test |
|---|---|---|
| Admission wins before fence | Registration sequence included in immutable fence high-water | D-RACE-01 |
| Fence wins before admission | Reject/quarantine; no lease or source dereference | D-RACE-02 |
| Dependency registration races fence | Exactly one legal ordering; incomplete set private | D-RACE-03 |
| Publication races fence | Publish-first inventoried OR fence-first rejected; no third state | D-RACE-04 |
| Commit succeeds, ACK lost | Same receipt returned by same operation ID/digest | D-FAULT-05/06/16 |
| Worker lease expires | Old lease cannot publish or terminalize | D-FAULT-07 |
| Queue/DLQ loss | D ledger remains barrier authority; no implicit terminal | D-FAULT-08 |
| Late derivative after drain | Suppress/quarantine and reopen reconciliation | D-FAULT-09 |
| Visibility commit crash | Reader sees absent/private or fully committed visible state | D-FAULT-10 |
| WAL/archive corrupt or missing | Refuse unsafe recovery; quarantine and report data-loss/restore failure | D-RECOVERY-01 |
| Blob missing on restore | Do not serve dangling canonical references | D-RECOVERY-02 |

## 6. Resource and compatibility

Measure write rate, simultaneous producer count, transaction duration, lock wait, WAL size/checkpoint time, canonical history growth, blob size distribution, backup window, restore throughput and maximum concurrent readers. Model 1-writer contention under SQLite separately from read concurrency. No measured SLO is available.

Keep CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, ForgetFenceGeneration, ProducerRegistrationSequence/HighWater, PermissionEpoch, IndexWatermark and ContextVersion as distinct typed namespaces. D's semantic operation names are not yet callable APIs or wire schemas; H/I/B must confirm their respective mappings.

## 7. Required sequence

1. Storage owner publishes a concrete transaction/locking/CAS design and named engine/configuration.
2. Implement one authoritative transaction boundary for all D ordering operations.
3. Add deterministic race, crash, ACK-loss, disk-full, corruption, failover and restore tests.
4. Run SQLite and PostgreSQL comparison against identical fixtures.
5. D verifies receipts, cursor monotonicity, barrier completion and no-resurrection invariants.
6. Only then make a database ADR.

## 8. Final recommendation and non-claims

Conditionally accept TAB-001's local transactional-store direction. Do not freeze SQLite, PostgreSQL, a KV engine, or a split-store coordinator. The joint D/E/Storage semantic decision is recorded, but no storage implementation, race test, crash-recovery test, benchmark, backup/restore drill or production deployment was validated by this review.