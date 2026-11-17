# Mature Technology Selection — Candidate Matrix

Status: research recommendation only. This does not supersede TAB-001, Storage ADRs or Owner decisions.

| Capability | Candidate | Recommendation | Boundary / evidence needed |
|---|---|---|---|
| Canonical transactional state | PostgreSQL | Strong candidate for the selected Storage transaction/serialization domain, subject to current Storage ADR and physical L4 proof | Validate serializable transaction behavior, COC durability, failover/old-primary fencing, restore/PITR and deployment topology. PostgreSQL WAL supports crash recovery; that alone does not prove cross-owner Forget/COC correctness. |
| Local single-user prototype | SQLite | Use for isolated local prototype or single-node MVP only if Storage authority approves semantic fit | WAL supports concurrent readers with a writer, but one writer remains serialized; test lock behavior, fsync/VFS, backup and crash restore. Do not assume SQLite satisfies cross-process/global JF-10 topology. |
| Lexical/full-text index | Tantivy or SQLite FTS5 | Start with existing simplest path; Tantivy is a strong Rust-native embedded candidate if measured scale justifies it | Index is derivative/rebuildable; enforce scope-before-candidate and per-partition watermark. SQLite FTS5 is simplest when already using SQLite. |
| Vector ANN | Qdrant | Defer until labelled retrieval evaluation shows lexical/structured gap | Verify pre-filter guarantees under strict Scope filters, stale/deleted payload suppression, partition isolation, rebuild and Forget races. Qdrant supports hybrid queries/filters; this is not an authorization authority. |
| Disposable cache | Redis / Valkey | Optional cache only; do not use as canonical memory or sole safety ledger | LRU/LFU are approximate cache policies. Cache keys include exact version/scope/epochs; every hit revalidates I/D. Prefer no-eviction or bounded local cache for correctness-critical metadata. |
| Scheduler / concurrency | Tokio primitives + small in-process policy module | Prefer library primitives (bounded channels, semaphore, cancellation, task groups) before durable external scheduler | Runtime admission is ephemeral. Use Temporal/DBOS/Restate only if durable long-running workflows become a proven requirement, not for every Recall. |
| Resource ledger | Existing transactional store | Store reservation/idempotency only if RM is adopted; otherwise local bounded counters | Never put authority tokens, Forget completion or Context lifecycle under Redis TTL semantics. |

## Product boundary decisions

- Buy/use storage engines, text indexes, vector search and cache implementations; do not reinvent B-trees, inverted indexes, ANN or LRU data structures.
- Keep Brain-owned semantics: canonical identity, authorization gates, Forget fences, provenance, task coverage/sufficiency, activation rationale, fairness policy, residency-view interpretation and explanation.
- No technology selection may convert a derivative index/cache into canonical authority.
- Do not introduce Kubernetes or a distributed scheduler for a local-first modular monolith without workload and operator evidence.

## Sources

- PostgreSQL WAL: https://www.postgresql.org/docs/18/runtime-config-wal.html
- SQLite WAL: https://www.sqlite.org/wal.html
- SQLite FTS5: https://www.sqlite.org/fts5.html
- Tantivy crate: https://docs.rs/tantivy/latest/tantivy/
- Qdrant search: https://qdrant.tech/documentation/search/search/
- Redis eviction: https://redis.io/docs/latest/develop/reference/eviction/
