# Technical Selection Recommendations

- Status: candidate recommendations only; no ADR approval
- Baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`

## 1. Recommended first-implementation posture

Preserve the existing logical authority model and prefer a modular Rust monolith with one durable transactional authority for the first vertical slice, subject to Storage/D/I approval. Use embedded libraries for indexes before separate services. Isolate optional model inference from durable acceptance and canonical recovery.

### Candidate stack profile

| Layer | Candidate | Recommendation |
|---|---|---|
| Canonical metadata + event/receipt ledger | PostgreSQL or SQLite | Choose one for the first vertical slice after transaction/fault tests; do not run both as competing authorities |
| Full text | Tantivy | Strong first Rust-native lexical candidate; compare against Lucene if JVM ecosystem or shared deployment matters |
| Vector | none initially / Qdrant later | Defer until workload proves vector search is necessary and structured+lexical baseline is inadequate |
| Workflow | in-process durable job table first | Evaluate Temporal only if long-running multi-service orchestration and recovery exceed local job-table capability |
| Event streaming | transactional outbox + in-process workers initially | Kafka only with measured multi-consumer, retention and cross-node throughput need |
| Formal verification | TLA+/TLC first; Alloy supplemental | Model Forget publication races and recovery before implementation claims |
| Telemetry | OpenTelemetry | Adopt trace context and standard metrics/log correlation early |
| Resource manager | small internal Rust module | Hierarchical accounting, reservations, fairness and bounded reclaim; no separate service |
| Memory IR | Rust typed structs + versioned serialization/schema | E-owned internal contract; no general plugin compiler |

## 2. PostgreSQL vs SQLite

**SQLite candidate profile:** simplest local-first embedded store, low operational burden, WAL allows readers and a writer to proceed concurrently. However WAL depends on same-host shared memory and is unsuitable for network filesystem/multi-host coordination. A single-writer model may be a benefit for a desktop/local brain, but write concurrency and checkpoint starvation must be tested.

**PostgreSQL candidate profile:** plausible fit for the Storage L1-selected per-authority SERIALIZABLE transaction domain, concurrent workers and physical HA/failover. SSI can reject non-serializable schedules. It increases deployment/backup/monitoring complexity and still cannot atomically include systems outside its transaction. Storage's L1 Option A is DECIDED; PostgreSQL itself is not selected, and actual engine/deployment conformance remains L4 OPEN.

**Selection gate:** choose SQLite if the product target is single-host/single-writer and the entire D visibility boundary can be implemented in one SQLite transaction with acceptable concurrency and durability. Choose PostgreSQL if multiple concurrent workers and HA are required and the D/I/Storage authority can share its physical transaction boundary. Do not select based on feature lists alone.

## 3. Search and index selection

- Structured filters and canonical reads should remain in the authoritative database.
- Tantivy is the first candidate for local Rust lexical search; its IndexWriter commits searchable segments and background merges optimize them.
- Lucene is a mature alternative with immutable segments and merge compaction.
- Qdrant should be a later optional service, not a default dependency. Its payload indexes are essential for filter-aware vector search; fields used in filters must be indexed and Forget/version state must be reconciled.
- All index document identifiers are implementation details; canonical typed refs remain stable identities.
- Indexes are rebuildable projections and must never decide Forget completion.

## 4. Workflow and messaging

**Start with durable work rows + outbox + idempotent in-process workers** if the first deployment is a local modular monolith. Persist stable work identity, attempt/lease identity, stage outcomes, retry schedule and terminal evidence.

Temporal is worth adopting when a workflow has long waits, external signals, multi-service activities, durable timers, human intervention or frequent worker replacement. Its replay model requires deterministic workflow code; network calls, model calls and file IO belong in Activities whose results are recorded. Temporal does not remove the need for idempotent external effects.

Kafka is not a substitute for a transaction manager or Forget inventory. Partition offsets provide replay positions, but ordering is partition-scoped and compaction/delete-marker retention has semantics that must be understood. Use only if throughput and independent consumers justify broker operations.

## 5. Formal methods

- Use TLA+/TLC for transition-system safety/liveness and race ordering.
- Use Alloy for structural constraints: no orphan derivatives, no unregistered producer, complete scope binding, no invalid cross-authority reference.
- Keep model inputs finite and explicit; enumerate assumptions and fairness.
- Preserve counterexample traces as regression fixtures.
- Every formal claim must identify model version, state bounds, properties checked, tool version, result and known abstraction gaps.
- A model PASS is logical evidence only; require refinement mapping to SQL/API and physical crash/fault evidence.

## 6. Resource manager selection

Implement only a thin in-process component:
- typed ResourceClass and BudgetScope;
- reserve/release with idempotent reservation ID;
- hierarchical limits and fair queues;
- deadline-aware admission and cooperative cancellation;
- per-cache-family byte/entry accounting;
- pressure and usage telemetry.

Do not make eviction policy a correctness mechanism. Cache entries remain disposable; every cache hit must re-check current Scope, permission and Forget state. Context edits still go through G.

## 7. Memory IR selection

Use versioned Rust types and explicit validation passes. Keep raw source immutable and preserve exact span/digest. Separate:
- Candidate object type (domain semantics delegated to B/D),
- Evidence role,
- Provenance transformation,
- Authorization/Scope,
- epistemic/temporal qualification,
- conflict and uncertainty,
- compiler policy/model versions.

Avoid a full language grammar, arbitrary user-defined pass plugins, bytecode/VM or a universal ontology in v1. B's Fact/Claim ADR remains a hard gate for canonical type finalization.

## 8. Rejected or deferred options

| Option | Status | Reason |
|---|---|---|
| Kafka as default local queue | REJECTED for v1 candidate profile | Unjustified broker/partition/retention operations before measured need |
| Qdrant as mandatory first store | REJECTED for v1 candidate profile | Adds distributed derived state before vector workload evidence |
| Temporal as mandatory workflow engine | DEFERRED | Durable local job table may suffice initially |
| One universal Memory Manager owning all semantics | REJECTED | Violates existing authority distinctions and conflates canonical/context/applied state |
| General compiler plugin framework | DEFERRED | More extension surface than the first IR needs |
| One generic cursor/epoch integer | REJECTED | Destroys authority-local ordering semantics |
| Replace COC/Storage topology immediately | UNRESOLVED | Requires same-case transaction vs protocol experiment and Owner decisions |
