# AI Memory Brain — Architecture Breakthrough Research Overview

- Research ID: ABR-SESSION-0-2026-11-18
- Status: **CANDIDATE / TO_VALIDATE; not an architecture approval**
- Research branch: `research/architecture-breakthrough-session-0-2026-11-18`
- Baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Date: 2026-11-18

## 1. Executive summary

The research does not propose a rewrite. It seeks the smallest changes that reduce duplicated mechanisms and cross-owner coordination without weakening safety invariants.

Three hypotheses emerge:

1. **Forget:** build a small executable cross-authority state model before adding more prose contracts. TLA+/TLC is the primary candidate for interleavings, crashes, replay, safety and liveness. Alloy is complementary for closed-world identity, target, lineage, Scope and authority relations. A passing model is not implementation proof.
2. **Runtime:** unify resource accounting, hierarchical budgets, admission, scheduling and reclaim—not domain authority. F's request scheduling, candidate/evidence budgets, cache/Working Set capacity and G's Context token/byte budgets can share one in-process Resource Manager. D canonical identity, F retrieval/activation, G ContextVersion, I authorization/Forget and H Applied evidence must remain separate.
3. **Compiler:** introduce a narrow, versioned Memory IR as a typed stage contract inside E, not a generic compiler platform. It should carry source identity/version/digest, Scope, evidence roles, temporal/epistemic qualifiers, transformation versions, uncertainty, conflicts and provenance. Model extraction produces candidates; deterministic validation and D canonical commit remain authoritative.

There is **no evidence yet that the proposed architecture outperforms the current architecture**. No controlled benchmark, formal model check, deployment, or fault campaign was run. The supported outcome is a set of testable simplification hypotheses and a minimal experiment plan.

## 2. Independence and evidence limitations

Session 0 read the live GitHub main ref, Issue #43, PR metadata, and relevant files on the current D/E/F/G/I/Storage/C/H owner branches. Public technical documentation was consulted for TLA+/Alloy, PostgreSQL, SQLite, Temporal, Kafka, Lucene, Tantivy, Qdrant, Redis, Linux cgroup v2 and OpenTelemetry.

This is not a blind organizational review: Session 0 shares the same repository and historical Issue #43 context as other owner sessions. Relevant owner artifacts were independently re-read at the current branch heads and blob SHAs listed below. Historical Issue #43 summaries were discovery aids only. No TLA+/Alloy checker was executed; no benchmark, database deployment or production fault drill was performed. Product documentation establishes mechanisms, not correctness of this project's integration.

### Live baseline and source pins

| Source | Current branch HEAD | Read artifacts / blob SHA |
|---|---|---|
| main | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | `01-system-architecture/system-overview.md` / `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256` |
| A | `session-a-integration-2026-11-16` @ `6e05831d264040e0e3b3359245b1e01ea613b46c` | responsibility matrix / `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3`; governance baseline / `a43a8f2fa3d31681d64b79d584364fdae80f8866` |
| B | `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | Fact/Claim ADR / `a1024938ff5baba069cf128c69496a44e143330c`; consumer mapping / `dd45a37199c9b69ab6b68f65e051a484a04691d4` |
| D | `session-d-memory-brain-2026-11-16` @ `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | Forget contract / `1f0391bc49d007c44ec74165bd33d37412cc7990`; publication gate / `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |
| E | `session-e-memory-compiler-2026-11-16` @ `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | producer admission / `e59f517fff161ab882aa0ddc4a5bda513964ae1a`; derived registration / `00e37ba56596e710513c8d0568acd79141d9101b`; evidence/provenance / `38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963` |
| F | `session-f-memory-runtime` @ `1908ce4d233b20f7cafd00cb679affd01bd15174` | runtime overview / `b7a948f014c3ad882a35a18bfc8ce025b26ab85a`; scheduling / `ca35d8cddd012c1ff067328ee22177f57c40ae36`; working set / `a934491950c876701e8ac592a0e6aaea983b44e3`; activation / `b7f5d85468f5262e472769a1991b812ac4a64f5b` |
| G | `session-g-memory-context` @ `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | context reconciliation / `87063aceebed1c30b7840045ada8e3f348732688`; context architecture/budget also read at this HEAD |
| I | `session-i-security-governance-2026-11-16` @ `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | global inventory / `9100061fa986fb6676656169de3fcf9fc1c72664`; retention/erasure / `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` @ `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | COC design v3.2.3 / `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` |
| C / H | C @ `71047cdb51139ca4080ac67f451e38a48698859d`; H @ `0d36324457e39bd50ad56ae902d477c4ea765b61` | live branch heads checked; Applied/recovery limitations require further exact-source review |

Issue #43 records G's prior HEAD as `3367438...`; the live GitHub branch listing now returns `763b3d...`. This report uses the live branch head, not the stale issue value.

### PR snapshot

PRs #46, #49, #55, #69, #70 and #71 were all Open / Draft / Unmerged at read time. PR #71 targets the Storage branch, not main. PR state is not an approval signal.

## 3. Workstream A — Forget model checking

### 3.1 The real question

The problem is not a shortage of Forget state names. It is whether locally owned state machines compose into a linearizable, recoverable, anti-resurrection protocol:

- D: ForgetOperation, ForgetFence, ProducerWork registration/barrier, dependency inventory and publication semantics;
- E: compiler work/attempt/lease/retry/DLQ/replay, staged derivatives and dependency-registration calls;
- I: PermissionEpoch, global Producer Domain Inventory, inventory sealing, global completion criteria and exceptions;
- Storage: physical transaction, prepared XID, visibility pointer, COC and recovery cutoff;
- F/G/H: indexes/cache/Working Sets, Context snapshots/deltas and Adapter application/reconnect.

Logical suppression, asynchronous cleanup and physical erasure remain distinct. D's CanonicalSuppressionComplete is not I's Global Forget Completed.

### 3.2 Smallest useful formal model

Start with one BrainAuthority, one target and lineage, two producers, two derived artifacts, one index, one Context, one Adapter and two concurrent operations (Forget and Publish). Model only:

- `fenceGeneration`, `permissionEpoch`;
- `producerRegistered`, `producerTerminal`;
- `dependencyRegistered`;
- `artifactPrivate/Visible`;
- `targetSuppressed`;
- `inventorySealed`, `barrierClosed`;
- `restoreGeneration`, `adapterAckGeneration`.

Safety properties:

1. **NoPostFenceVisibility:** an artifact covered by the current fence/lineage cannot become visible.
2. **RegisterBeforePublish:** every visible derivative has stable ProducerWork registration and complete dependency registration.
3. **BarrierSoundness:** a barrier closes only when every pre-fence work item has verifiable terminal disposition and no unresolved lease/DLQ/replay remains.
4. **UnknownIsNotSuccess:** timeout, lost ACK and unknown state never imply success, terminality or cleanup completion.
5. **RestoreCannotRollbackControl:** current control high-waters are applied before reads/writes after restore; an old snapshot cannot lower fence or permission generations.
6. **NoCrossEpochCompare:** PermissionEpoch, ForgetFenceGeneration, ProducerRegistrationHighWater, CanonicalCommitCursor, IndexWatermark and ContextVersion remain distinct namespaces.

Counterexample classes: producer registration racing with fence installation; partial dependency registration; lost ACK after visibility commit; expired lease with a still-running stale worker; DLQ replay; index rebuild; offline Adapter reconnect with old Context; restore rollback; and Permission revocation racing final commit.

**The current TLA+ file is only a first-stage skeleton, not the complete model above:** it currently abstracts one target set, producer registration, fence high-water capture, dependency registration, visibility suppression, terminalization and restore control-high-water overlay. It does not yet encode lost ACK, Lease/Attempt, DLQ/Replay, PermissionEpoch, I's global inventory, index/Context/Adapter state, and TLC has not been run. Those scenarios are the next extension backlog, not coverage already verified in this submission.

### 3.3 Tool selection

- **TLA+/TLC — CANDIDATE, preferred first.** Suitable for concurrent state machines and temporal properties; checks safety and liveness and produces counterexample traces. State space must be bounded.
- **Apalache — CANDIDATE, alternative.** Symbolic checking is useful for bounded safety over finite structures; its documentation still describes experimental aspects, so do not make it the sole verifier.
- **Alloy 6 — CANDIDATE, complementary.** Strong for relational constraints over producer/target/lineage/Scope/authority and bounded counterexamples. No instance within a finite scope does not establish an unbounded theorem.
- **PostgreSQL — CANDIDATE physical mechanism.** Serializable isolation detects concurrent read/write dependency patterns that cannot correspond to any serial execution and aborts a transaction. It only covers the transaction boundary of that database; it does not atomically include an external COC, Adapter, vector store or cloud service.

### 3.4 Preliminary disposition

**CANDIDATE: TLA+ as the primary model, Alloy as a relational supplement.** Do not start by adopting a generic distributed transaction framework or creating another coordinator. First determine whether D Producer Registration, Fence Install, Dependency Registration and Visibility Commit can share one physical transaction / linearization anchor. If not, compare recoverable prepare/commit with the COC protocol.

## 4. Workstream B — Memory Operating System

### 4.1 Existing overlap

F already owns retrieval routing, activation recommendations, Working Sets/cache, Runtime scheduling, admission, cancellation and per-request candidate/evidence/latency budgets. G owns Context membership, ContextVersion, ordering, expiry, token/byte budget, sufficiency, snapshots/deltas and reconciliation.

This is a real overlap in resource policy, not proof that domain ownership should merge. The best breakthrough is a single **in-process Runtime Resource Manager (logical module, not a new service)**:

- resource ledger for CPU, RAM/VRAM, candidates, evidence bytes, tokens, concurrency slots and deadlines;
- hierarchical budgets: global → principal/scope → session/context → request/stage;
- reservations before fan-out, reranking and context expansion;
- scheduling: interactive Recall priority, deferrable background refresh, cross-principal fairness;
- residency: common byte/entry accounting for Working Sets and caches;
- reclaim: evict only rebuildable projections; Context reduction must go through G's authorized operations;
- feedback from pressure, queue age, cache misses, token budget and sufficiency outcomes.

### 4.2 What must not be unified

- Canonical Memory is not an evictable cache.
- Forget and Permission are not resource policies; priority/budget can never override them.
- RetrievalResult and ActivationRecommendation remain F semantics; ContextEntry and ContextVersion remain G semantics.
- Context budget is a semantic/user-visible budget, not merely a RAM budget.
- Applied Context is Adapter evidence, not residency state.

### 4.3 Mature mechanisms

- Linux cgroup v2 distinguishes protection (`memory.low`), throttling under pressure (`memory.high`) and a hard limit (`memory.max`). Borrow hierarchical control and pressure feedback, not a literal cross-platform memory algorithm.
- Redis approximated LRU/LFU demonstrates that maintaining an exact global access order is not always worth its metadata/CPU cost. Select eviction only after hit-rate and overhead measurements.
- Qdrant's payload indexes plus HNSW show that vector retrieval and filter execution must be co-designed. A resource manager can schedule retrieval but cannot replace index filter semantics.
- OpenTelemetry context propagation can correlate reservations, cancellation, eviction and Context updates. High-cardinality IDs should not be metric labels.

### 4.4 Preliminary disposition

**CANDIDATE: one Resource Manager for resource ledger, hierarchical budgets, admission/scheduling/reclaim; preserve F/G domain authority.** No new microservice, no renaming Context Manager into an OS, and no predictive scheduler in the first iteration.

## 5. Workstream C — Memory IR / Memory Compiler

### 5.1 Existing foundation

E already has durable acceptance, recoverable work items, deterministic normalization, optional model extraction, Evidence/Provenance, candidate proposals, conflict proposals and D canonical commit coordination. Its Evidence/Provenance contract requires exact source version/digest, locator, support/refute/qualify role, method/model lineage and Forget dependency registration.

Memory IR should therefore not create another pipeline. It should replace unstable intermediate DTOs with a typed, versioned contract between existing stages.

### 5.2 Minimal IR

Top-level envelope:
- `ir_version`, `schema_digest`, `producer`, `derivation_run_id`;
- immutable `source_refs[]` (version/digest/locator);
- `scope_refs[]`, `observed_at`, `recorded_at`;
- typed candidate `nodes[]`: Fact/Claim/Event/Entity/Relation/Procedure etc.;
- `evidence_links[]`: support/refute/qualify/context-only;
- `provenance[]`: parents, transform kind, tool/model/prompt/policy version, input/output digest;
- `uncertainty[]`, `conflicts[]`, `validation_findings[]`;
- `forget_dependencies[]` referencing D receipts, not inventing D authority fields.

Fact/Claim types must respect B's ADR status. While the B ADR remains blocked, use an explicitly provisional discriminant or opaque proposal; do not freeze a wire/storage schema that depends on the unresolved choice.

### 5.3 Compiler passes

1. Parse/Normalize — deterministic; never overwrite source.
2. Extract — optional model stage; emits candidates and source spans, not truth.
3. Type/Scope Validate — deterministic hard gate; reject or quarantine failures.
4. Evidence/Provenance Attach — exact source version, digest and transform lineage.
5. Conflict/Consolidation Propose — preserve conflicts; propose rather than silently adjudicate.
6. Optimize — semantic-preserving deduplication, normalization and redundancy reduction; record input/output digest for each pass.
7. D Commit Request — commit through D authority; IR never writes canonical store directly.
8. Projection Publish — only after dependency registration, current Fence/Permission and final visibility gate.

### 5.4 Incremental recompilation

Fingerprint using `source_digest + parser_version + extraction_policy/model_version + IR_schema_version + transform_versions`. Recompile only affected lineage subgraphs when an input or pass version changes. Old authorization/Fence receipts are never reused as current publication permission. Historical derivations remain auditable; a new DerivationRun creates new provenance rather than overwriting history.

### 5.5 Preliminary disposition

**CANDIDATE: introduce Memory IR as an internal E stage contract; do not create a Compiler service or plugin framework.** The first version needs only 5–7 stable types, schema version, source/provenance, validation report and deterministic normalization.

## 6. Product adoption boundaries

| Product | Original problem / mechanism | Fit | Inappropriate use / cost |
|---|---|---|---|
| PostgreSQL | ACID, MVCC, Serializable Snapshot Isolation | Canonical transaction, idempotency, outbox, same-domain linearization candidate | Transaction boundary must be physically closed; serialization retries, connections, backup and HA operations |
| SQLite | Embedded transactions, WAL, multi-reader/single-writer | Minimal local single-host vertical slice | WAL relies on same-host shared memory; not for network filesystems or multi-host writers |
| Lucene / Tantivy | Inverted index, immutable segments, background merge | Adopt a mature lexical index library instead of writing one | Internal doc IDs/segment IDs are not canonical identity; merge/rebuild resource cost |
| Qdrant | HNSW + payload indexes + filtered vector search | Adopt when corpus/filter/vector needs justify a separate service | Extra process/deployment, data copy, filter schema and Forget/version consistency |
| Temporal | Event History, deterministic replay, Activities isolate external side effects | Reconsider if workflows become long-running, multi-service and recovery-heavy | Full service operation may be unnecessary for a local-first modular monolith |
| Kafka | Partitioned append log, offsets, consumer replay, compaction | Only when multi-consumer throughput/retention/cross-node streaming is measured | Not a default queue; broker, partition-order constraints, retention/replay and operations |
| TLA+/Alloy | Concurrent state model / relational constraints and counterexample search | Critical Forget and authorization linearization paths | Abstraction still requires refinement/conformance to implementation |
| OpenTelemetry | Trace/metric/log correlation | Adopt APIs/SDKs/conventions directly | Avoid high-cardinality labels and sensitive payload leakage |

## 7. Preliminary assessment of the current architecture

### Worth preserving (DECIDED baseline; not changed here)

- Canonical Memory / Memory Context / Applied Context separation.
- D/I/F/G/H/C authority and Scope/Permission/Forget constraints.
- Separation of Durable Accepted, Compiled, CanonicalCommitted, Indexed, Delivered and Applied.
- Evidence/Provenance, typed cursors/epochs and fail-closed unknowns.
- Brain does not own Agent planning or tool execution.

### Complexity risks (CANDIDATE; evidence required)

- Repeated race/failure contracts across Owners and repeated version-bundle/exact-adoption reconciliation.
- F request budgets and Working Set limits may duplicate accounting with G Context budgets.
- E intermediate objects may cause repeated DTO/schema/provenance conversions without a common IR.
- COC, Storage prepared XID, owner-local gates, receipts/sequencers and recovery cutoffs may create high integration overhead; document count alone does not prove overengineering. Compare against a minimal single-transaction implementation.
- Multiple cursor namespaces are not inherently bad complexity when they represent distinct authorities and ordering semantics; collapsing them could make the system less safe.

## 8. Three highest-value next experiments

1. **Forget Model + Counterexample Suite:** model ProducerRegistration / FenceInstall / DependencyRegister / Publish / LostACK / Restore / Replay in a small TLA+ spec. Produce counterexample traces and explicit model bounds; then map actions to D/E/Storage APIs and a SQL transaction prototype.
2. **Runtime Resource Manager A/B:** compare current distributed budgets with hierarchical shared budgets on the same real task set. Measure p50/p95, token waste, RAM peak, cache hit rate, partial results, fairness and Forget/revocation latency.
3. **Memory IR Vertical Slice:** use 20–50 representative experiences to compare current stage DTOs with typed IR. Measure schema/adapter count, repeated parsing, determinism, incremental recompilation scope, provenance completeness and review cost.

## 9. Status

| Conclusion | Status |
|---|---|
| TLA+ primary model, Alloy supplement | CANDIDATE |
| Resource Manager unifies accounting, not Owner authority | CANDIDATE |
| Memory IR as internal E stage contract | CANDIDATE |
| Exact PostgreSQL/SQLite/Lucene/Tantivy/Qdrant/Temporal/Kafka adoption mix | TO_VALIDATE |
| New architecture is better than current architecture | UNRESOLVED (no comparative experiment) |
| Modify A–I authority specs / approve ADR | NOT AUTHORIZED |

## 10. External references

- TLA+ tools / TLC / Apalache: https://lamport.org/tla/tools.html
- Alloy 6 model and bounded traces: https://alloytools.org/spec.html
- PostgreSQL 18 transaction isolation: https://www.postgresql.org/docs/18/transaction-iso.html
- SQLite WAL constraints: https://sqlite.org/wal.html
- Temporal Event History and replay: https://docs.temporal.io/encyclopedia/event-history
- Kafka log design: https://kafka.apache.org/design/
- Lucene segment model: https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/index/package-summary.html
- Tantivy architecture: https://docs.rs/tantivy/latest/tantivy/
- Qdrant indexing: https://qdrant.tech/documentation/manage-data/indexing/
- Linux cgroup v2 memory controller: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- Redis eviction: https://redis.io/docs/latest/develop/reference/eviction/
- OpenTelemetry context propagation: https://opentelemetry.io/docs/concepts/context-propagation/
