# Research Comparison Matrix — Architecture Breakthrough

- Baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Research branch: `research/architecture-breakthrough-session-0-2026-11-18`
- Status: candidate comparison, not decisions

## 1. Workstream comparison

| Dimension | A — Forget Model Checking | B — Memory Operating System | C — Memory IR / Compiler |
|---|---|---|---|
| Root problem | Cross-owner state machines lack one executable composition proof | Resource limits, admission and eviction are spread across F/G | Stage-to-stage representations and lineage can drift |
| Existing authority | D fence/barrier; E work; I policy/inventory; Storage visibility; F/G/H local effects | F scheduling/retrieval/cache/activation; G Context and semantic budget | E compiler stages; D canonical commit; I governance |
| Candidate breakthrough | TLA+ model + Alloy relation constraints; single physical visibility boundary | In-process hierarchical Resource Manager | Versioned typed IR between existing stages |
| Primary invariant | No visible derivative after fence without registered lineage/current authorization | Resource use is bounded and fair; hard safety gates cannot be bypassed | Every output is typed, source-bound, reproducible and traceable |
| Build vs buy | Buy/use TLA+/TLC, Alloy; PostgreSQL for physical transaction candidate | Reuse OS limits/telemetry; implement thin application resource ledger | Implement domain-specific IR; reuse Serde/schema validation/index libraries |
| Not to build | New universal coordinator before proof | New microservice, new Agent runtime, universal Memory manager | General-purpose compiler framework/plugin ecosystem |
| Main evidence | Model counterexamples + implementation refinement + crash/fault tests | Same-workload A/B and pressure tests | Deterministic fixture replay, schema/lineage checks, migration comparison |
| Main risk | False confidence from bounded abstraction | Coupling resource scheduling to domain semantics | IR freezes unresolved Fact/Claim or over-models all memory types |
| Current disposition | CANDIDATE | CANDIDATE | CANDIDATE |

## 2. Product and mechanism matrix

| Product / system | Problem solved and mechanism | Adopt directly | Borrow selectively | Avoid / operational cost |
|---|---|---|---|---|
| PostgreSQL 18 | MVCC; SERIALIZABLE uses SSI/predicate dependency tracking and aborts non-serializable concurrent transactions | Canonical durable transaction candidate if the project selects PostgreSQL | Single transaction for fence + registration + dependency + visibility when physically co-located | Does not coordinate external COC/Adapter/Qdrant; retries and HA/backup operational burden |
| SQLite WAL | Embedded ACID store; readers and writer can proceed concurrently via WAL | First local single-host prototype candidate | WAL/checkpoint behavior and crash tests | WAL same-host shared-memory constraint; long readers can starve checkpoints and grow WAL |
| Lucene | Inverted index and immutable searchable segments, merge compaction | Mature lexical index if JVM ecosystem acceptable | Segment immutability, delete/update semantics and merge policy | Do not expose internal doc IDs as domain IDs; separate index lifecycle |
| Tantivy | Rust-native schema, tokenizer, IndexWriter, segments and searcher | Preferred Rust lexical prototype candidate | Commit/segment/merge architecture | Needs corpus-specific relevance and concurrency benchmarks |
| Qdrant | HNSW vector index plus payload indexes for filter-aware search | Adopt only if vector workload/scale justifies process boundary | Index only fields used by mandatory filters; filtered vector retrieval | Extra service, replicated derivative state, index rebuild, filter schema and Forget invalidation |
| Temporal | Durable Event History and deterministic workflow replay; Activities record external effects | Adopt if workflow durability needs outweigh operations cost | Stable work identity, replay-safe deterministic orchestration, external effects isolated as activities | Not a drop-in transaction manager; service/history/worker operations and deterministic code constraints |
| Kafka | Partitioned append log, offsets, consumer pull/replay, compaction | Adopt only for measured multi-consumer/stream requirements | Immutable offsets, partition ownership, replay, tombstone retention caveats | Broker/cluster, partition-order constraints, retention and compaction operational costs |
| TLA+/TLC | Explicit-state model checker for safety/liveness of executable TLA+ specs | Use for critical Forget/authorization protocol | Model bounded identities and interleavings; preserve trace artifacts in CI | State explosion; model correctness and implementation refinement still need review |
| Alloy 6 | Relational model finder with temporal state support and bounded scopes | Use for identity/lineage/Scope consistency models | Check structural constraints and small traces | Bounded absence of counterexample is not an unbounded proof |
| Linux cgroup v2 | Hierarchical memory protection, throttling and hard limits | Use platform facilities where available | low/high/max semantics and pressure-based control | OS-specific; app-level semantic token budget differs from process memory |
| Redis | Approximate LRU/LFU eviction under maxmemory | Consider only if a shared external cache is justified | Approximate eviction, admission/eviction telemetry | New stateful service; cache must remain disposable and authorization-aware |
| OpenTelemetry | Correlated traces, metrics, logs and context propagation | Adopt standard APIs/SDKs | Propagate trace/causation IDs across jobs and adapters | High-cardinality labels and payload logging can cause cost/privacy problems |

## 3. Decision rules

1. Prefer a library embedded in the modular monolith before adopting a new service.
2. Adopt a service only when a measurable non-functional requirement needs its operational boundary.
3. Do not let an index/cache/workflow engine become a second canonical authority.
4. Do not infer Forget correctness from a database's ACID label; identify the exact transaction boundary and all external effects.
5. Do not equate durable workflow replay with idempotent provider side effects; external activities still need stable idempotency and reconciliation.
6. Keep each cursor/epoch namespace typed; a single generic sequence is not simplification when ordering domains differ.
7. Every product adoption needs a migration plan, failure-mode review, local deployment cost, restore strategy and rollback criterion.

## 4. External sources

- PostgreSQL SSI: https://www.postgresql.org/docs/18/transaction-iso.html
- SQLite WAL: https://sqlite.org/wal.html
- Lucene segments: https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/index/package-summary.html
- Tantivy: https://docs.rs/tantivy/latest/tantivy/
- Qdrant filterable indexing: https://qdrant.tech/documentation/manage-data/indexing/
- Temporal replay: https://docs.temporal.io/workflows
- Kafka design: https://kafka.apache.org/design/
- TLC and Apalache: https://lamport.org/tla/tools.html
- Alloy: https://alloytools.org/spec.html
- Linux cgroup v2: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- Redis eviction: https://redis.io/docs/latest/develop/reference/eviction/
- OpenTelemetry: https://opentelemetry.io/docs/concepts/context-propagation/
