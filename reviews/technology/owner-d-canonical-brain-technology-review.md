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
## 9. Reassessment — Storage and COC architecture evidence (2026-11-17)

The original verdict's phrase 'BLOCKED for storage selection' is superseded for architecture design by the following exact evidence:
- Storage selected PostgreSQL 18.7 as the concrete prepared-XID capability candidate for the pinned CI profile; it is not production deployment approval.
- Seven-workflow regression set is 7/7 SUCCESS: PITR run `43958775001`/job `133620265141`; prepared-XID `43959079736`/`133621314502`; synchronous promotion `43959079669`/`133621315610`; backup/restore `43959079703`/`133621314624`; WAL PITR `43959079745`/`133621314724`; sync-unavailable fail-closed `43959079760`/`133621315188`; pg_rewind/rejoin `43959079930`/`133621314973`.
- Exact COC durable protocol Blob `4ac63ac79491e79ec0c9114ef73941c73d7bbf25` has exact D acceptance in `03-memory-brain/phase-3.6.3-d-coc-durable-protocol-acceptance.md`, Blob `e2a74d138ccebfb4266d19ea0c0c03f58a815bf5`.
- Storage Gate B protocol design is exact-owner-reviewed; A records the matrix in `reviews/integration/phase-3.6.3-coc-durable-protocol-acceptance-matrix.md`.

Updated D disposition: **CONDITIONAL PASS — D semantic and architecture contract accepted; runtime implementation and end-to-end conformance deferred to engineering.** D does not certify PostgreSQL production deployment, I sequencer integration, D ledger implementation, physical erasure or Global Forget completion. JF-10 implementation P0 remains OPEN.

## 10. TAR-AI-001 refresh — current D/Storage capability evidence (2026-11-17)

This addendum supersedes any earlier statement in this report that no concrete Storage engine candidate or CI capability evidence exists. The D review was refreshed against D branch HEAD `06bce7f13bfe003d6d70b8d57c9522f5e46e2ed9`; the report's earlier semantic review baseline was D HEAD `7385e6fa45087a73ea314e8790e22903f3a3be7c`. The current Storage branch at refresh was `session-storage-consistency-forget-atomicity-2026-11-16` HEAD `7a1b733c2e83fd2427aacdd18bd30518b27fcd72`.

### 10.1 Updated candidate disposition

- PostgreSQL 18.7 is now the **selected CI capability qualification profile** for JF-10 prepared-XID testing, not an approved production Canonical Authority deployment.
- The Storage dossier records PASS for the pinned profile's single-node prepared-XID persistence/lock retention/hard restart/same-XID resolution, two-node synchronous WAL replay and promotion, physical backup/restore stale-control fail-closed fixture, coordinator crash in the participant-success/ACK gap, TCP ACK loss, synchronous-standby-unavailable UNKNOWN/private behavior, and WAL-archive PITR.
- The Storage dossier explicitly keeps Gate A PARTIAL PASS / OPEN; Gate B's exact-owner protocol acceptance is design-level with enumerated exceptions and the later amended revision requires focused exact-owner re-review; Gate C implementation/fault injection is deferred to engineering. JF-10 P0 remains OPEN and production activation is not authorized.
- Therefore D's engine disposition is updated: PostgreSQL 18.7 is the leading qualified capability candidate for the JF-10 profile; SQLite WAL remains a plausible lightweight canonical-store prototype but is not evidenced for durable prepared-XID recovery across an external I sequencer. No final database ADR or production deployment selection is approved here.

### 10.2 Revised component/dependency and interface assessment

The D/E joint decision fixes the semantic serialization order across RegisterProducerWork, InstallForgetFence, complete RegisterDerivedDependency, final visibility commit and barrier-visible terminal disposition. E's stable WorkItemId/AttemptId/LeaseEpoch/DerivationRunId mapping is aligned. I accepts JF-10 v2 only for a single PolicyDomainRef and binds its sequencer decision to the exact prepared Storage participant/XID and owner boundary. Storage alone controls VisibilityPointer and PublicationReceipt. COC records order/participant observations but cannot mint D fence effectiveness, I authorization or Storage visibility.

The remaining implementation gate is narrower than an undefined contract but still P0: bind the exact owner-final-gate and D fence/lineage predicate into one tested storage/COC/I deployment, preserve prepared XID and locks through failover/restore, prove same-XID forward commit/rollback, and demonstrate D's ledger and I sequencer integration. Multi-PolicyDomain atomicity remains blocked. D local CanonicalSuppressionComplete remains distinct from I Global Forget completion and physical erasure.

### 10.3 Updated blocking findings

- **P0 — TAR-D-P0-001:** D/E/Storage integrated producer admission, fence installation, dependency completeness, publication visibility and terminal barrier implementation is not present or verified. Design contracts exist; runtime linearizability remains unproven.
- **P0 — TAR-D-P0-002:** JF-10 application-level I sequencer + Storage prepared-XID participant + D fence/lineage integration and same-XID recovery remain unimplemented / not end-to-end tested. PostgreSQL engine capability tests do not close this.
- **P1 — TAR-D-P1-001:** Complete exact-owner acceptance of the currently amended Storage/COC protocol revision and production topology/profile remains open.
- **P1 — TAR-D-P1-002:** Canonical commit/revision/lifecycle/outbox cursor atomicity and F/G consumer continuity require actual application transaction and consumer tests.
- **P1 — TAR-D-P1-003:** Blob staging, metadata visibility, encryption, backup/PITR and restore quarantine must be integrated with the D control ledger.
- **P1 — TAR-D-P1-004:** Callable D operations/receipts, D ledger persistence, I coordinator client and F/G consumer conformance are not implemented.

### 10.4 Required prototypes/tests and evidence boundary

Storage CI provides real engine-capability evidence for PostgreSQL 18.7 under the pinned CI configuration. It is not a benchmark of the AiMemoryBrain application, not an E/D/I/COC adapter integration test, and not production deployment evidence. Required next engineering tests:
1. Implement D ledger + producer/fence/dependency/publication transaction adapters against PostgreSQL 18.7 and a comparable SQLite prototype where SQLite remains under consideration.
2. Run the complete D36/E36/JF-10/COC crash and race suite against the real application adapters, including old-primary fencing, prepared-XID failover, coordinator restore and same-XID recovery.
3. Verify canonical cursor assignment, immutable revision, lifecycle event, visibility pointer, PublicationReceipt, receipt consumption and outbox atomicity.
4. Restore database + blobs + WAL/archive + I/D control ledgers from stale and current points; prove quarantine before serving and no resurrection.
5. Benchmark writer contention, prepared-XID lock duration, queue/reader throughput, WAL growth/checkpoint, backup/PITR/restore time, RAM/disk and operational overhead.

### 10.5 Exact additional evidence

| Source | Commit SHA | Blob SHA |
|---|---|---|
| D branch refresh | `06bce7f13bfe003d6d70b8d57c9522f5e46e2ed9` | branch tree at review refresh |
| Storage branch | `7a1b733c2e83fd2427aacdd18bd30518b27fcd72` | branch tree at review refresh |
| Storage realization review | `7a1b733c2e83fd2427aacdd18bd30518b27fcd72` | `107d21bd2c604ee0b04feff2ee5580e1de9c7fce` |
| PostgreSQL 18.7 capability dossier | `7a1b733c2e83fd2427aacdd18bd30518b27fcd72` | `0aabf66848dc97deee028c571183c0d7204008c0` |
| Storage joint durable atomicity decision | `7a1b733c2e83fd2427aacdd18bd30518b27fcd72` | `17071157152c7868d638383ec97543fe3d35e652` |
| Forget atomicity verification report | `7a1b733c2e83fd2427aacdd18bd30518b27fcd72` | `9f224722a40844686d275e44a8ab6ba72fa1ddb8` |
| D joint Forget decision | `06bce7f13bfe003d6d70b8d57c9522f5e46e2ed9` | `1b6a312ecffd3947bbb4df59f902242482c98a40` |
| D COC acceptance | `06bce7f13bfe003d6d70b8d57c9522f5e46e2ed9` | `e2a74d138ccebfb4266d19ea0c0c03f58a815bf5` |

This refresh changes only the D technology review report. It does not modify D module contracts, Storage artifacts, TAB-001, or any other Owner branch. No end-to-end D/E/Storage/I/COC implementation test or Global Forget completion is claimed.


## 11. TAR-AI-001 mandatory-section index and final D disposition

### Executive Summary

**CONDITIONAL PASS** for D semantic and technology architecture; **BLOCKED** for integrated Storage implementation and JF-10 application conformance. PostgreSQL 18.7 is a qualified CI capability candidate, not a production engine approval.

### Review Scope

TAB-001, D canonical store, cursor semantics, Forget/publication gate, D/E joint linearization, JF-10, D COC acceptance, current E producer decisions, I JF-10 disposition and Storage branch capability evidence were inspected. The latest D owner design source HEAD before report publication was `06bce7f13bfe003d6d70b8d57c9522f5e46e2ed9`; Storage source HEAD `7a1b733c2e83fd2427aacdd18bd30518b27fcd72`.

### Six-Dimension Review Conclusions

1. **Technical Requirements & Workload Fit:** CONDITIONAL — semantic operations and typed cursors are specified; production workload envelope unmeasured.
2. **Component Dependencies & Boundaries:** CONDITIONAL — D/E/I/Storage/COC authority split is coherent; application adapters absent.
3. **Candidate Technology Selection:** CONDITIONAL — PostgreSQL 18.7 is the leading prepared-XID capability candidate; SQLite remains an unqualified alternative for JF-10; no production database ADR.
4. **Resource Constraints:** NOT MEASURED — throughput, lock duration, prepared-XID backlog, WAL, blob, RAM/disk, backup/restore and operations need measurement.
5. **Failure Recovery & Operational Safety:** BLOCKED — engine capability CI passed, but application D/I/COC integration and end-to-end recovery are not run.
6. **Interface & Compatibility:** CONDITIONAL — typed cursor/fence/epoch/XID boundaries are clear; callable APIs, receipts and F/G consumers remain unimplemented.

### Component Dependency Analysis

D owns canonical identities, immutable revisions, CanonicalCommitCursor, LifecycleEventCursor, ForgetFence and producer barrier. E owns WorkItem/Attempt/Lease/manifest. I owns PermissionEpoch/CommitAuthorizationReceipt/revocation and global inventory. Storage owns physical XID, VisibilityPointer and PublicationReceipt. COC records order/participant observations only. F/G/H/C are downstream consumers and cannot infer global Forget or Applied from D-local state.

### Candidate Technology Comparison

PostgreSQL 18.7 supports tested prepared-XID and recovery capabilities under the pinned CI profile, but has server/ops overhead and remains unbound to production. SQLite WAL is low-footprint and appropriate for local transactional prototypes, but its ordinary transaction model does not demonstrate durable external prepared-XID participant recovery. RocksDB/KV adds application-level transaction/constraint burden. A database-backed outbox is suitable for local queues but is not the barrier authority. Recommendation: continue PostgreSQL 18.7 as the JF-10 integration target while retaining SQLite only as a comparative prototype; make no final engine ADR before application-level race/recovery evidence.

### Resource Budget Analysis

No application performance or capacity measurement is claimed. Benchmark concurrent canonical writers/readers, transaction and lock duration, prepared-XID/in-doubt count, D barrier latency, WAL growth/checkpoint, blob throughput, backup/PITR/restore throughput, connection/RAM/disk overhead and recovery time. Keep model inference outside D commit path.

### Failure & Recovery Matrix

- Admission wins before fence → work included in captured high-water.
- Fence wins before admission → durable reject/quarantine; no lease or source dereference.
- Dependency registration incomplete → private/no visibility.
- Publish wins before fence → durable publication included in pre-fence reconciliation.
- Fence wins before publish → reject; private artifact.
- I COMMIT_WON + Storage crash → same-XID forward recovery, private until Storage visibility commit.
- I REVOCATION_WON → same-XID rollback/no publication.
- UNKNOWN/IN_DOUBT → preserve participant, locks and barrier; no timeout/TTL release.
- Restore → quarantine and reconcile current D/I control state before serving.
- PostgreSQL capability subtests are PASS for their pinned CI profile; application-level D/E/I/COC cases remain NOT RUN.

### Interface Compatibility Findings

CanonicalCommitCursor is one global sequence per Brain authority; AggregateRevision and LifecycleEventCursor are independent. ForgetFenceGeneration, ProducerRegistrationHighWater, PermissionEpoch, ProducerDomainInventoryEpoch, IndexWatermark, ContextVersion, AdapterCapabilityEpoch, Storage XID and COC positions remain distinct. I JF-10 v2 accepts one PolicyDomainRef only. D local CanonicalSuppressionComplete is not I Global Forget completion or physical erasure.

### Blocking Findings

P0: D/E/Storage atomic admission/fence/dependency/publication/terminal integration not implemented; JF-10 same-XID I/Storage application recovery not integrated. P1: current Storage protocol exact-owner acceptance/re-review; canonical commit/cursor/outbox app tests; DB/blob/backup/restore integration; D/I ledger and F/G consumer conformance.

### Required ADRs

Database engine/profile ADR (PostgreSQL vs SQLite under app harness); Storage isolation/participant/XID recovery ADR; blob/DB visibility and backup/PITR ADR; B Fact/Claim ADR remains upstream and blocks schema freeze.

### Required Prototypes and Tests

PostgreSQL/SQLite same-fixture app harness; D36/E36 deterministic race suite; JF-10 prepare/commit/rollback/unknown crash matrix; I sequencer and D ledger integration; WAL/PITR/corruption/disk-full/restore-after-Forget; blob orphan/digest tests; F/G cursor/fence consumer tests; concurrency and resource benchmarks. Engine CI is not a substitute for these application tests.

### Verdict

**CONDITIONAL PASS** for semantic design and candidate technology direction; **BLOCKED** for implementation acceptance and global Forget completion.

### Evidence and Exact SHAs

See §10.5 for the current D/Storage exact evidence manifest and this report's publication commit. Additional controlling source blobs: D canonical store `6b37c91033fda21f072e2a3bde6f274663b1e76e`; D cursor semantics `4688a0ca487bf4d853c7f0220408abe8d743d159`; D publication gate `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`; D JF-10 `94679897e84a6f58fd8b9467b5249e1a885cb0b0`; E producer conformance `a17f065e69e809fceacb51873d6a36a8b0f5c235`; I PermissionEpoch `bae6a24fe3a374bc816993979a8fa9af52517dea`; I Global Forget inventory `9100061fa986fb6676656169de3fcf9fc1c72664`.

This appendix is part of the D review report only. No module contract, TAB-001, or other Owner report is changed.
