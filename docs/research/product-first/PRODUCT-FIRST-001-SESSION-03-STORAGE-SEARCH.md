# PRODUCT-FIRST-001 — Session 03: Storage, Search & Index Product Adoption
# PRODUCT-FIRST-001 — Session 03：存储、搜索与索引产品采用研究

- Task: `PRODUCT-FIRST-001 / SESSION-03`
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Research branch: `research/product-first-001-session-03-storage-search`
- Exact main baseline: `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Date: 2026-11-18
- Status: **RESEARCH DRAFT / NOT AN ADR / NO TECHNOLOGY FREEZE**
- Language: English and Chinese are normative peers in this research artifact.
- Scope note: this report evaluates product adoption against the existing logical contracts. It does not authorize implementation, alter Canonical Truth / Evidence / Forget authority, or approve a physical deployment.

---

## 0. Executive conclusion / 执行摘要

**Recommendation:** do not add an independent vector database, Tantivy, Redis, a graph database, or a distributed broker to the first storage slice. The minimum credible target is a single-authority transactional store with structured relational queries, native full-text search, a transactional outbox, rebuildable projections, and a bounded content-addressed blob layer. PostgreSQL is the strongest multi-writer/server candidate; SQLite is a credible embedded/single-host candidate. Neither is selected by this report.

The recommendation is conditional on the exact Storage ADR: L1 Option A requires one logical Serializable Transaction Domain per Canonical Memory authority. A product is acceptable only if D's authoritative admission/fence records and Storage's visibility/outcome records share that serialization domain and the required atomic commit. Merely choosing the same vendor, cluster, or SQL dialect is not sufficient.

**Vector answer:** PostgreSQL + pgvector is the default first candidate and is likely sufficient for the initial vertical slice if a labeled retrieval evaluation demonstrates acceptable recall/latency under tenant/scope filters. Qdrant has real value as a dedicated vector-search service at scale, but it is not required to preserve current semantics and introduces a second consistency, backup, restore, tenant-filter, and Forget-projection surface.

**Search answer:** begin with PostgreSQL FTS (or SQLite FTS5 for the embedded profile). Tantivy is a later embedded Rust-library option when multilingual tokenization, BM25 control, indexing throughput, or ranking requirements demonstrably exceed native FTS. It is a library, not a ready-made distributed search service.

**Canonical answer:** exactly one authoritative representation for each domain fact. Search documents, vector rows, caches, graph projections, and denormalized read models are disposable derived projections keyed by canonical IDs, version/digest, scope, and projection revision. They are never Canonical Truth or Evidence authority.

**Forget answer:** authoritative read suppression is synchronous at the D Fence / current authority boundary; secondary index/cache/blob cleanup is asynchronous but tracked, replayable, and cannot re-enable serving. Restore starts fenced and must reconcile current D/I/COC/Storage high-waters before any protected read. Physical erasure is a separate evidence-bearing obligation, not implied by deleting an index row.

**Decision status:** RECOMMENDED candidate architecture only. No L4 engine, deployment topology, schema, vector index, or search engine is approved or frozen here.

**建议：** 第一阶段不要引入独立向量数据库、Tantivy、Redis、图数据库或分布式 Broker。最小可信方案是：单一 Authority 事务存储、结构化关系查询、数据库原生全文检索、事务 Outbox、可重建投影，以及边界清晰的内容寻址 Blob 层。PostgreSQL 是多写入/服务端候选；SQLite 是嵌入式/单机候选。本报告不替 Owner 选定其中任何一个。

必须服从 Storage ADR：L1 Option A 要求每个 Canonical Memory Authority 使用一个逻辑 Serializable Transaction Domain。只有 D 的 Admission/Fence 权威记录与 Storage 的 Visibility/Outcome 权威记录确实共享该序列化域，并满足原子提交要求，产品才合格。相同厂商、集群或 SQL 方言并不等于满足要求。

**向量检索：** PostgreSQL + pgvector 是默认首选候选；若带租户/Scope 过滤的标注检索评估证明召回率和延迟达标，初期无需独立向量库。Qdrant 在规模化向量检索时有实际价值，但不是维持当前语义的必要条件，并会增加第二套一致性、备份、恢复、租户过滤和 Forget 投影面。

**全文检索：** 先用 PostgreSQL FTS（嵌入式 Profile 用 SQLite FTS5）。只有多语言分词、BM25 控制、索引吞吐或排序要求经实测超过原生 FTS 时，再评估 Tantivy。Tantivy 是 Rust 库，不是开箱即用的分布式搜索服务。

**Canonical：** 每个领域事实只能有一个权威表示。搜索文档、向量行、缓存、图投影和反规范化读模型都是可丢弃的派生投影，必须绑定 Canonical ID、Version/Digest、Scope 和 Projection Revision，不能成为 Canonical Truth 或 Evidence 权威。

---

## 1. Baseline / 当前基线

### 1.1 Exact repository snapshot / 精确仓库快照

- Current default branch: `main`.
- Exact HEAD read from the Git tree: `b3c666e67982cb3d3374e759cfb6552c7765aacb`.
- Repository README says architecture definition; implementation is “Not started by design”.
- `ARCHITECTURE_ROADMAP.md` places technology selection after logical architecture and requires prototypes, benchmarks, ADRs, and explicit gates.
- `00-governance/architecture-invariants.md` includes I-04 (distinct Event/Memory/Fact/Entity/Relation/Evidence), I-05 (provenance), I-13 (scope and permission), I-15 (event/record/valid time), I-20 (Forget covers derived and secondary representations), I-21 (subsystem boundary does not imply process/service/crate), and I-22 (performance claims require reproducible measurement).
- `02-domain-model/core-entities.md` defines immutable Memory Versions, Claim epistemic status, Event recorded/event time, Evidence availability, Relations, Provenance, Scope, and atomic current-pointer advancement. It explicitly says this is logical schema, not database DDL.
- `02-domain-model/relationships-and-provenance.md` says Relation semantics are decided while graph representation and lineage compaction are candidate/open; similarity or co-occurrence is not a typed Relation.
- `13-engineering-decisions/technology-architecture-blueprint.md` (TAB-001, v0.1) is a candidate blueprint, not a technology freeze. Its technology register records:
  - TEC-003 SQLite + WAL single-node prototype: CANDIDATE / TO_VALIDATE.
  - TEC-004 PostgreSQL multi-writer/remote evolution path: CANDIDATE.
  - TEC-005 content-addressed local filesystem + metadata: RECOMMENDED.
  - TEC-006 FTS5 first, Tantivy comparison: CANDIDATE.
  - TEC-007 embedded ANN (e.g. usearch) vs sqlite-vec: OPEN.
  - TEC-008 Moka in-process cache: RECOMMENDED.
  - TEC-017 versioned SQL migrations: RECOMMENDED.
  - TEC-018 transactional outbox + DB-backed workers: CANDIDATE.
  Required prototypes include SQLite/PostgreSQL transaction comparison, D/E Forget race tests, FTS5/Tantivy, at least two vector candidates, restore with Forget/revocation replay. These prototypes are not claimed as run by this report.

### 1.2 Storage ADR — exact decision boundary / Storage ADR 精确决策边界

Read exact Storage/D serialization topology ADR Blob:
`bb544ba2f346bdc130d524bd5c7310d86f367988`.

- **L1 is selected:** Option A, one logical serializable transaction domain per Canonical Memory authority.
- **L4 remains OPEN:** actual database product/version/configuration, deployment manifest, operator/on-call, cluster/failure-domain placement, HA/PITR, protected read-path enforcement, production key custody, and physical crash/failover/restore drills.
- D retains semantic authority over ProducerWork admission, ForgetFence, lineage/dependency completeness, PublicationParticipantRef, and D terminality.
- Storage retains semantic authority over PREPARED_HIDDEN, VisibilityPointer, Storage outcome, PublicationReceipt, and outbox durability.
- I retains identity, authentication, permission, authorization, revocation ordering, and I CommitAuthorizationReceipt.
- COC remains a separate quorum log; it is not silently included in the database transaction and is not XA.
- C and E retain their Provider and Compiler authority respectively.
- Pointer + receipt + outcome + outbox must commit atomically. A hidden participant must not become publicly visible before exact D and I proof validation.
- UNKNOWN/IN_DOUBT remains private and barriers remain held. A lost ACK is reconciled using the same immutable operation/participant tuple.
- A stale replica/cache must not bypass the authoritative pointer/fence. Restore/failover with uncertain serialization history is RESTORE_FENCED.
- Option B requires a successor ADR and equivalent durable protocol proof; Option C check-then-write/asynchronous coordination is rejected.

**Baseline limitation discovered:** the exact current-main recursive tree at the pinned HEAD contains 126 entries and no root-level `09-storage-and-index/`, `03-memory-brain/`, `04-memory-compiler/`, `05-memory-runtime/`, `06-memory-context/`, `08-protocols/`, `10-security-and-governance/`, `11-consistency-and-recovery/`, or `12-testing-and-acceptance/` source directories. The README and documentation portal still describe those directories as the detailed source-specification layout. Therefore, this report can bind the exact Storage ADR Blob and inspect the current domain/technology documents, but it cannot claim a complete current-main readback of the absent Storage/Forget source directories. This is a baseline/documentation availability finding, not proof that the blobs never existed on another branch.

### 1.3 PR and Owner-contract status / PR 与 Owner 契约状态

- **PR #45**: technology-reality research; historical base `b372b62c640a2b656e54b6db62a4ee67d7d8c001`, research head `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`. It is an earlier candidate research package, not current-main authority and not a technology approval.
- **PR #56**: independent review of #45; verdict REVISE / feasibility NOT YET PROVEN / architecture freeze NOT READY. It found currentness and Storage ADR pin issues in the original #45 package. Its review is evidence about #45, not a substitute for this session's exact current-main baseline.
- **PR #73**: open Draft remediation based on exact current main `b3c666e67982cb3d3374e759cfb6552c7765aacb`, head `7b4771b3766c616fa932b30b21c3bc0dc742f564`. It corrects the Storage ADR pin and carries current Phase 3.8/3.8.3 source deltas, but is role-simulated remediation and does not select an L4 engine or establish physical conformance.
- Related current proposal context: PR #66 D Forget closure, #68 I/D terminalization, and #71 Storage review are Draft proposals on separate Owner branches. Their bodies explicitly state they are not final Owner approval, production implementation, Forget completion, or physical erasure. Do not treat their proposed changes as mainline normative changes.
- PR #52 is a Draft A integration review on an older base; it conditionally accepts the logical Option A direction while retaining L4 and exact Owner-review gaps. It is not a current-main L4 approval.

**Baseline status:** current logical domain and Option A constraints are sufficiently clear for product evaluation. Current-main Storage implementation contracts, production DB adapter, runtime deployment, representative workload, and conformance evidence are not present/proven. Research confidence is high for product capabilities from official docs, but low for project-specific fit until workload and physical tests exist.

---

## 2. Storage product comparison / 存储产品比较

### 2.1 PostgreSQL 18 / PostgreSQL 18

**Role fit:** leading server-side canonical transactional candidate, not approved.

Strengths:
- Mature relational constraints, transactions, indexes, JSON, range/time types, recursive SQL, generated columns, and transactional outbox patterns.
- Serializable isolation is available, but applications must handle serialization failures and retry safely; retries must preserve the same immutable operation identity and must not duplicate external effects.
- PostgreSQL 18 supports WAL-based backup and point-in-time recovery; PITR is operationally powerful but requires tested base-backup/WAL retention/timeline procedures.
- Native FTS supports `tsvector`, `tsquery`, GIN/GiST. GIN is the preferred full-text index type for many workloads.
- Row-Level Security (RLS) can enforce row visibility per role, with default-deny when enabled without a matching policy.

Risks / costs:
- It is a separately operated server: upgrade, vacuum/autovacuum, WAL growth, connection pooling, backup retention, replication, monitoring, capacity, and on-call responsibilities are real costs.
- Serializable transactions can abort under contention; transaction retry behavior must be explicit and idempotent.
- RLS is defense-in-depth, not the sole authorization boundary: superusers and roles with BYPASSRLS bypass it; table owners normally bypass unless FORCE ROW LEVEL SECURITY is enabled. Referential-integrity checks also bypass row security.
- A PostgreSQL deployment does not automatically prove the Storage ADR's one-serialization-domain property. The actual D/Storage row ownership, transaction/UoW, authority anchor, commit path, and protected read path must be implemented and tested.
- Logical replication/read replicas and asynchronous replicas must not be used for fence-sensitive or currentness-sensitive decisions without a formally accepted consistency profile.

License / adoption cost:
- PostgreSQL License, permissive BSD/MIT-like. pgvector is a PostgreSQL extension and its upstream metadata identifies PostgreSQL license terms. Verify exact release, extension packaging, supported PostgreSQL major, and deployment image at adoption time.

**Disposition:** PREFERRED SERVER CANDIDATE / L4 OPEN. Use one DB transaction domain for D + Storage physical serialization rows per Canonical Memory authority. Do not split them into separate databases for organizational convenience.

### 2.2 SQLite + WAL / SQLite + WAL

**Role fit:** embedded/local-first single-host candidate.

Strengths:
- In-process embedded deployment; no database server or separate DBA service.
- ACID transactions and serializable writes by serializing writers. WAL allows readers and a writer to proceed concurrently.
- FTS5 supplies full-text query, phrase/prefix/NEAR/boolean operations, ranking helpers including BM25, and content/external-content modes.
- Online Backup API can create a consistent snapshot while allowing normal access between incremental backup steps.
- Very low operational footprint and useful for desktop, local-agent, single-user, offline deployments.

Hard limits:
- Only one writer at a time per database. High concurrent ingestion/compilation/publication can serialize and queue.
- WAL requires all participating processes to be on the same host; it does not work over a network filesystem.
- Not a multi-host HA/replication substrate. Do not place a SQLite WAL file on NFS/shared network storage or use it as a distributed transaction coordinator.
- Application must own migration, file permissions, encryption-at-rest strategy, backup rotation, disk-full behavior, corruption detection, and restore fencing.
- FTS5 availability depends on build configuration in some SQLite build modes; verify the exact library bundled by every target.

**Disposition:** CANDIDATE for embedded single-host profile only. It can be compatible with Option A if D and Storage use the same SQLite database/connection transaction domain and all authority rows/read paths obey the same serialization anchor. It cannot satisfy a multi-host authority topology by itself.

### 2.3 Other relational engines / 其他关系数据库

MySQL/InnoDB and SQL Server are mature relational products, but this research finds no project-specific advantage sufficient to offset a third SQL dialect, different serializable/locking semantics, adapter/testing matrix, and operational diversity. Revisit only if a target deployment environment or operator requirement makes them materially preferable. They are not recommended for the first vertical slice.

---

## 3. Search product comparison / 搜索产品比较

### 3.1 PostgreSQL FTS / PostgreSQL 原生全文检索

- Supports document/query tokenization, lexeme normalization, ranking, highlighting, and GIN/GiST indexes.
- Keeps canonical relational filters, authorization joins, temporal filters, and lexical query in one DB query plan.
- Transactional update with canonical version/outbox can avoid cross-system indexing lag for basic lexical search.
- Language dictionaries/tokenization quality varies. Chinese/Japanese morphology and project-specific tokenization must be evaluated; default English-centric assumptions are unsafe.
- FTS indexes are derived structures. They can be regenerated from approved canonical text fields and versioned source rows.

**Disposition:** FIRST SERVER-SIDE LEXICAL OPTION. It minimizes components and consistency boundaries. It is not a claim that PostgreSQL FTS is sufficient for every language or relevance requirement.

### 3.2 SQLite FTS5 / SQLite FTS5

- Strong match for embedded local-first search.
- Supports phrases, prefix terms, proximity/NEAR, boolean expressions, ranking/BM25 helpers, snippets/highlighting.
- External-content tables can index content stored elsewhere, but the application is responsible for keeping the FTS index synchronized with the content table.
- FTS5 shadow tables are internal; application code should not mutate them directly.
- Tokenizer quality and Chinese/Japanese segmentation need evaluation; extensions such as jieba/lindera-family tokenizers add dependency and packaging cost.

**Disposition:** FIRST EMBEDDED LEXICAL OPTION when SQLite is selected. Search rows remain rebuildable.

### 3.3 Tantivy / Tantivy

- Rust full-text search library inspired by Lucene, with BM25, phrase queries, configurable tokenizers, incremental indexing, multi-threaded indexing, mmap-backed directories, and facets/range queries.
- Third-party tokenizers exist for Chinese, Japanese, and Korean, but each adds a dependency, dictionary/data packaging, versioning, and reproducibility concern.
- Tantivy is a library, not an out-of-the-box distributed search service. Distributed search is explicitly out of scope for Tantivy itself.
- Index updates are delete-and-reindex semantics; commit and reader reload affect visibility.
- A separate Tantivy index creates a second durable artifact that needs rebuild, snapshot/versioning, scope filters, Forget suppression, and consistency watermark management.

**Disposition:** DEFER. Revisit if PostgreSQL FTS / FTS5 fails a labeled corpus evaluation on tokenizer quality, ranking control, throughput, or latency. It is not required just because the core application is Rust.

### 3.4 pgvector / pgvector

- Stores vector types and supports exact nearest-neighbor search (perfect recall) plus approximate HNSW and IVFFlat.
- HNSW generally trades higher memory/build cost for a favorable speed/recall tradeoff; IVFFlat generally uses less memory and builds faster but needs training/data-aware tuning.
- Approximate index filtering occurs after the ANN scan in common plans. Selective tenant/scope filters can therefore return fewer candidates than requested; iterative scans, partial indexes, or partitioning may be needed.
- Shared ANN indexes can let one tenant's vectors affect another tenant's recall and query speed. The project must choose partitioning/separate tables or another isolation strategy based on tenant scale and threat model.
- pgvector runs inside PostgreSQL, reducing the number of independent data services and allowing vector rows to share transaction, backup, role, and schema management with canonical records. It does not make vectors canonical facts.

**Disposition:** DEFAULT VECTOR CANDIDATE after lexical baseline, not required for initial correctness. Begin with exact search or a small HNSW prototype on a labeled dataset. Gate approximate search on recall@k, precision@k, latency, memory, filtered recall, update/delete/rebuild, and Forget tests.

### 3.5 Qdrant / Qdrant

- Dedicated vector database/search engine with payload filtering, HNSW-oriented vector search, snapshots, sharding, replication, and distributed deployment.
- Distributed mode is not equivalent to automatic replication: self-hosted operators must create shard replicas and manage shard placement/rebalancing; replication factor and transfer method matter.
- Qdrant's documentation describes distinct shard-transfer consistency trade-offs. A record-stream transfer can have weaker ordering and may require reindexing; snapshot transfer preserves index/quantization and can provide stronger ordering at extra space/operational cost.
- Multi-tenancy supports payload filters, user-defined sharding, and tiered approaches; separate collections per tenant can become resource-heavy.
- Qdrant is Apache-2.0 licensed upstream. Cloud/service terms are separate from the OSS server license.

Value:
- Independent vector scaling, purpose-built ANN, payload filtering, vector-specific operational controls, and managed Qdrant Cloud.
- Useful when vector workload, throughput, memory, index size, or isolation needs grow beyond the relational database's acceptable envelope.

Costs:
- Second write/read system, outbox consumer, delivery watermark, replay/idempotency, snapshot/restore coordination, tenant-filter correctness, and Forget tombstone/purge workflow.
- No atomic transaction across PostgreSQL canonical visibility and Qdrant index update. The safe pattern is canonical commit + outbox, then asynchronous projection; query results must be revalidated against the canonical authority before disclosure.
- Qdrant availability must never decide whether a memory exists, is visible, forgotten, or authorized.

**Disposition:** NOT IN MINIMAL STACK. Add only after measured vector-specific requirements and a failure/Forget/restore proof justify the additional system.

### 3.6 LanceDB / LanceDB

- Apache-2.0 OSS project; positioned as an embedded/serverless retrieval library/database on Lance columnar format, with vector and multimodal data use cases.
- Attractive for local/embedded vector and multimodal retrieval experiments and columnar datasets.
- It is not a replacement for the Storage ADR's transactional authority by mere adoption. Its storage/index lifecycle, transaction isolation, multi-process/multi-host guarantees, restore semantics, and integration with the exact D/Storage serialization anchor require separate verification.
- Current upstream workspace metadata may move quickly and can require a recent Rust toolchain; pin exact release and MSRV before adoption.

**Disposition:** DEFER / EXPERIMENTAL ALTERNATIVE to embedded ANN or analytical retrieval, not the canonical transactional store.

### 3.7 Cache and other search components / 缓存与其他检索组件

- **Moka:** appropriate in-process bounded cache candidate for a local modular monolith. It must be generation/fence-aware, TTL-bounded, and disposable. Cache hit must not bypass I authorization or D Forget read suppression.
- **Redis:** not required for the first local modular monolith. Add only for a demonstrated cross-process cache/coordination need. Redis must not become a durable canonical memory or Forget authority.
- **Elasticsearch/OpenSearch/Quickwit:** capable search services but add a service, index pipeline, cluster operations, backup, tenant security, and Forget propagation. No current workload evidence justifies them.
- **Tantivy vs Quickwit:** Tantivy is the Rust library; Quickwit is a distributed search engine built on Tantivy. Do not describe Tantivy itself as distributed.

---

## 4. Physical deployment topologies / 物理部署拓扑

| Topology | Components | Advantages | Main risks | Disposition |
|---|---|---|---|---|
| T0 Embedded local | Rust modular monolith + SQLite/WAL + FTS5 + local content-addressed blobs + Moka | smallest footprint, offline, single install | one writer, same-host only, single-node recovery/operator burden | candidate for single-user/local profile |
| T1 Single DB service | Rust modular monolith + PostgreSQL + FTS + optional pgvector + blob store + outbox workers | strong relational/transaction integration, simpler consistency | DB ops, serializable retries, RLS/tenant design, HA/restore complexity | preferred server candidate |
| T2 DB + vector service | PostgreSQL canonical + Qdrant derived vector projection + blob store | vector scaling/isolation options | dual-store projection lag, Forget and restore orchestration | scale-driven only |
| T3 DB + Tantivy | PostgreSQL/SQLite canonical + Tantivy embedded index | advanced BM25/tokenizers, Rust integration | custom index lifecycle, snapshot/rebuild, cross-store lag | only if native FTS fails evaluation |
| T4 distributed multi-service | PostgreSQL + Qdrant + distributed search + broker + cache cluster + object store | independent scaling and fault domains | many consistency authorities, expensive operations, high failure surface | reject for first slice |

**Option A constraint across all topologies:** the D admission/fence rows and Storage visibility/outcome rows for a Canonical Memory authority must share the exact logical serializable transaction domain. T2/T3 may add derived search stores, but they cannot move those authoritative rows outside that domain. COC remains its own quorum log; there is no claim of cross-log XA atomicity.

### 4.1 Deployment profile recommendation / 部署 Profile 建议

1. **Local embedded profile:** SQLite/WAL + FTS5, only if the deployment is explicitly one host and the expected write concurrency is modest. All D/Storage authority records must live in the same DB transaction domain. Do not use a network-mounted WAL database.
2. **Server profile:** PostgreSQL as one authority database. Prefer a modular monolith first; D and Storage may be separate Rust modules but not separate physical transaction domains for the protected commit path.
3. **Scale-out search profile:** keep PostgreSQL canonical; add Qdrant/Tantivy only as derived projections behind an outbox and canonical revalidation.
4. **Blob profile:** start with content-addressed local filesystem when one host; move to S3-compatible/object storage only when deployment requires shared durable blob capacity. Store digest, size, media type, encryption metadata, retention class, and authority reference in the canonical DB. Never make an object URL itself the authority.
5. **Cache profile:** process-local Moka initially; no Redis until there is a measured cross-process need.

---

## 5. Data authority mapping / 数据权威映射

| Data / representation | Authority | Physical candidate | Duplicate policy |
|---|---|---|---|
| Event identity, classification, recorded_at, source/idempotency | Event/Capture contract | canonical relational rows | one authoritative event record; retries same key+digest return same outcome |
| Evidence identity, source_ref, locator, availability, integrity metadata | Evidence/Provenance authority | relational metadata + immutable content ref | one Evidence identity; source payload may be retained once by content digest |
| Memory / MemoryVersion / Claim | Canonical Memory authority | relational rows and immutable version tables | immutable versions; one current pointer; no competing “search truth” |
| Entity / Relation / typed temporal edges | Domain/Entity authority | relational tables with typed refs and temporal columns | canonical typed edge, not embedding/co-occurrence |
| Provenance / source edges | Evidence & Provenance authority | relational edge tables | preserve source lineage; don't flatten away provenance |
| D admission, ForgetFence, dependency set, PublicationParticipant | D | same Option-A transaction domain | no second D authority in cache/index |
| Storage hidden participant, VisibilityPointer, Receipt, Outcome, Outbox | Storage | same Option-A transaction domain | pointer+receipt+outcome+outbox atomic |
| I auth/PermissionEpoch/revocation/CommitAuthorizationReceipt | I | I-authoritative store/sequencer | separate authority; DB colocation does not transfer semantics |
| COC quorum prefix/Batch/Manifest | COC | separate quorum log | no silent folding into SQL or XA claim |
| Lexical index | derived projection | Postgres FTS / FTS5 / Tantivy | rebuildable; source IDs+version+digest+watermark |
| Vector embeddings/ANN graph | derived projection | pgvector / Qdrant / LanceDB | rebuildable; bind model/version/dimension/input digest |
| Graph traversal acceleration | derived projection | relational indexes / optional graph engine | typed Relations remain canonical in relational authority |
| Blob bytes | blob/content retention authority | content-addressed filesystem/object store | one immutable content object per digest where retention permits |
| Cache entries | no authority | Moka / optional Redis | disposable; version/fence/permission generation keyed |
| Backup snapshots | recovery artifact | DB backup + blob snapshot + external evidence | never directly serve restored data before reconciliation |

### 5.1 Avoiding duplicate facts / 避免重复事实

Duplication is acceptable only when it is an explicitly derived, versioned projection or a content-addressed physical copy with integrity/retention metadata. It is not acceptable to maintain two independently editable canonical records of the same proposition.

Rules:
- Canonical Claim is not copied into a second “fact table” with independent lifecycle.
- Evidence metadata is not a duplicate Claim; Evidence supports/refutes/qualifies a Claim through typed links.
- A vector embedding is a derived representation of a specified source version and embedding model, not a new fact.
- A search document is a query projection, not a new MemoryVersion.
- A Relation is not inferred merely from co-occurrence or vector similarity.
- Blob metadata and blob bytes are split by storage mechanics, but the content digest binds them; no mutable URL is treated as durable evidence.
- Denormalized read models carry source IDs, versions, digests, and projection watermarks and can be discarded/rebuilt.

---

## 6. Forget, restore, and index rebuild implications / Forget、恢复与索引重建影响

### 6.1 Forget path / Forget 路径

1. D commits the authoritative ForgetFence / suppression transition at its defined linearization point. All protected read paths must consult the current authority or an equally strong, non-stale fence proof.
2. The canonical DB transaction makes the item ineligible for serving immediately. A query must not reveal content merely because an old search row, vector, cache key, blob URL, replica, or precomputed result still exists.
3. The transactional outbox records projection invalidation work in the same canonical transaction as the relevant state transition.
4. Cache invalidation uses a monotonic authority/fence/permission generation. On uncertain generation, cache is bypassed.
5. Lexical/vector/graph projections receive idempotent tombstones and purge commands. Their progress is tracked per target with exact source version, operation ID, target identity, and acknowledgement.
6. Blob retention/physical erasure is handled according to the applicable retention and evidence policy. Removing a search index entry is not proof that bytes were erased from backups, replicas, snapshots, or object-store versions.
7. UNKNOWN/IN_DOUBT projection cleanup does not release D/I barriers or permit serving. A stale projection may be ignored, but not used to prove Forget completion.
8. Audit evidence records suppression, target enumeration, projection cleanup, backup expiry/key destruction as applicable, and remaining exceptions.

### 6.2 Restore and anti-rollback / 恢复与防回滚

- Restore DB, blob storage, and derived search indexes into an isolated, non-serving environment.
- Set `RESTORE_FENCED`; do not accept writes, expose signed URLs, or serve protected search results.
- Reconcile the restored COC committed prefix, D/I/C owner-local request/admission/effect high-waters, ForgetFence generations, revocation/PermissionEpoch, and Storage visibility outcomes against independent current witnesses.
- Reject or quarantine any restored state whose high-water is behind, whose proof is missing, or whose commit/participant identity is ambiguous.
- Rebuild derived indexes from canonical state only after reconciliation; exclude Forgotten/suppressed content and bind the new index generation to the restored authority generation.
- Invalidate all process and distributed caches after restore; no cache snapshot is trusted as authority.
- Only the responsible Owners may release their own gates. A successful database restore alone is not permission to serve.

### 6.3 Index rebuild / 索引重建

A rebuildable projection needs:
- stable canonical source ID and immutable version;
- source content digest and projection schema/version;
- embedding model ID/version/dimension where applicable;
- tenant/scope metadata and policy generation;
- monotonic outbox sequence / projection watermark;
- idempotent upsert/delete semantics;
- deterministic rebuild input and tokenizer/config pin;
- shadow-index build + validation + atomic generation switch;
- reconciliation for changes that occur during build;
- Forget suppression recheck before index publication and again before result disclosure.

A rebuild may temporarily reduce search availability, but it must never increase authority or resurrect forgotten content.

---

## 7. Multi-tenancy, authorization, and isolation / 多租户、授权与隔离

**Authority boundary:**
- Domain Model owns Scope semantics and object relationships.
- I owns authentication, authorization, PermissionEpoch, revocation, and authorization proof.
- The Brain's access/read path enforces the authorization result and D Forget suppression.
- Storage owns durable persistence and visibility commit, not permission policy.
- Search engines enforce tenant/scope filters as defense-in-depth, not as the source of authorization truth.

**Required controls:**
- Tenant/Scope identity is derived from authenticated principal and authorized scope resolution, never trusted from a user-controlled query parameter alone.
- Every canonical read, evidence dereference, blob retrieval, lexical/vector candidate, graph traversal, cache hit, export, and backup restore path is scope-filtered.
- PostgreSQL RLS may provide defense-in-depth, but application roles must not be table owners/superusers/BYPASSRLS; test FORCE ROW LEVEL SECURITY and privileged maintenance paths. RLS does not replace I authorization or D suppression.
- For high-isolation tenants, evaluate separate DB/schema/collection/shard boundaries; for many small tenants, partitioning and strict filter enforcement may be more practical. Document residual noisy-neighbor and index-recall leakage risks.
- pgvector approximate filtering can happen after ANN candidate scanning. A tenant filter that is correct logically can still underfill results or leak cross-tenant influence through recall/latency. Evaluate per-tenant partition/index strategies where necessary.
- Qdrant payload filters must be applied on every query path; collection-per-tenant has resource overhead. User-defined sharding is an option for a smaller number of large tenants.
- Search result candidates must be revalidated against canonical authorization and Forget state before content is fetched or disclosed.
- Cross-tenant aggregates, uniqueness constraints, foreign-key errors, timing, counts, and debug traces must be reviewed for side channels.
- Backups and support tooling require explicit tenant-aware access and auditable privileged access.

---

## 8. Capability-by-capability disposition / 按能力的产品决策

| Capability | Minimal implementation | Product adoption trigger | Status |
|---|---|---|---|
| Canonical storage | PostgreSQL or SQLite profile, selected by deployment target | write concurrency, HA, operator, multi-host needs | L4 OPEN |
| Event/evidence storage | relational metadata + content-addressed blob reference | large immutable payload/object retention | candidate |
| Relational data | SQL tables, constraints, transactions | none; core requirement | RECOMMENDED mechanism |
| Vector search | initially omit or pgvector exact/HNSW spike | labeled recall/latency proves ANN need | OPEN / TO_VALIDATE |
| Full-text search | PostgreSQL FTS or SQLite FTS5 | tokenizer/relevance/scale test fails native option | RECOMMENDED first |
| Hybrid search | SQL lexical + vector candidate fusion, canonical revalidation | retrieval evaluation shows measurable benefit | TO_VALIDATE |
| Temporal query | valid-time + recorded-time columns, range predicates/indexes | specialized temporal workload proves need | SQL first |
| Graph/relationship | typed relational edges + recursive queries | deep path traversal/graph analytics exceed SQL | SQL first |
| Blob storage | content-addressed local FS initially | multi-host durability/size/access patterns | RECOMMENDED candidate |
| Cache | Moka in-process, bounded and disposable | measured cross-process need | RECOMMENDED candidate |
| Index rebuild | outbox + source watermark + shadow generation | mandatory before index is production-serving | REQUIRED |
| Backup/restore | SQLite Online Backup or PostgreSQL base backup/WAL PITR + blob snapshot | based on selected physical engine | REQUIRED |
| Multi-tenancy | I authorization + Scope filtering + DB/search defense-in-depth | tenant count/isolation profile | REQUIRED |
| Replication | none for local profile; PostgreSQL HA profile when required | RPO/RTO and availability objectives | L4 OPEN |
| Migration | versioned SQL migrations, expand/contract, checksum/readback | every schema evolution | REQUIRED |

---

## 9. Adoption matrix / 采用矩阵

| Product | Canonical DB | Search/index | First slice | Later trigger | Recommendation |
|---|---:|---:|---:|---|---|
| PostgreSQL 18 | Yes, candidate | FTS native | server profile | multi-writer/server/HA need | PREFERRED SERVER CANDIDATE |
| SQLite + WAL | Yes, candidate | FTS5 native | embedded profile | local/offline, one-host | CANDIDATE |
| pgvector | No separate authority | vector projection | optional evaluation only | vector benchmark passes | DEFAULT VECTOR CANDIDATE |
| Qdrant | No | vector service | No | dedicated scale/filter/sharding need | DEFER |
| Tantivy | No | lexical index library | No | native FTS fails corpus test | DEFER |
| LanceDB | Not approved as transaction authority | embedded vector/multimodal | No | embedded ANN/multimodal experiment | EXPERIMENTAL |
| Redis | No | cache/coordination only | No | cross-process cache need | DEFER |
| Neo4j / graph DB | No | graph projection | No | complex graph traversal/analytics need | DEFER |
| S3-compatible object store | No | blob bytes | local FS first | multi-host/object lifecycle | LATER |
| Elasticsearch/OpenSearch/Quickwit | No | search service | No | measured lexical/distributed search need | DEFER |

No product in this matrix is approved or frozen by this report.

---

## 10. Recommended minimal stack / 推荐最小技术栈

### Profile A — Local-first embedded candidate

- Rust modular monolith; subsystem boundaries remain modules, not mandatory services.
- SQLite + WAL as one per-authority transaction domain, with one writer queue and explicit busy/retry behavior.
- FTS5 for lexical retrieval.
- Content-addressed local filesystem for immutable blobs; metadata and digests in SQLite.
- Moka for bounded in-process cache; generation/fence-aware; no cache is authoritative.
- DB-backed transactional outbox/work queue; no Redis/NATS/Kafka in the first slice.
- Vector search omitted initially; if needed, compare exact SQL scan/pgvector server profile versus one embedded ANN library in a separately gated experiment.

### Profile B — Server-side candidate

- Rust modular monolith.
- PostgreSQL 18 as the single canonical transactional domain for the relevant Canonical Memory authority; D + Storage serialization rows and anchor must participate in the same serializable commit boundary.
- PostgreSQL FTS for initial lexical search.
- pgvector optional and co-located only after a labeled retrieval evaluation; exact search baseline before HNSW/IVFFlat.
- Content-addressed object storage (local filesystem initially; S3-compatible when multi-host operations require it).
- Moka local cache. Add Redis only if a measured multi-process need exists.
- Transactional outbox and DB-backed workers; external projections are asynchronous and rebuildable.
- Qdrant/Tantivy only behind an outbox and canonical revalidation, after independent failure/Forget/restore gates.

**Why two profiles:** the product is intended to be local-first and model/agent independent. SQLite and PostgreSQL represent different deployment profiles, not two databases that should both be active writers for the same authority. A given Canonical Memory authority has one active serialization domain. Cross-profile migration is a controlled authority migration, not live dual-write truth.

### Explicit non-goals / 明确不做

- No microservice split for D, Storage, Index, Vector, Cache, Blob, or Search merely because they are separate modules.
- No dual canonical write to PostgreSQL and Qdrant.
- No graph DB before typed Relation query workloads demonstrate need.
- No search engine as Canonical Truth.
- No Redis or broker as a substitute for DB transactions, Forget fences, or COC quorum.
- No assumption that object-store deletion or index deletion equals physical Forget completion.

---

## 11. Complexity reduction opportunities / 复杂度削减机会

1. **One canonical transaction domain:** avoid separate D and Storage databases in v1. Keep semantic owners distinct while sharing the L1 Option-A physical serialization substrate.
2. **Native lexical search first:** avoid operating both FTS and Tantivy before corpus evidence requires it.
3. **Vector as a derived capability:** store embedding metadata/version and ANN rows as projection; avoid a Qdrant cluster before vector recall and scale require it.
4. **Relational graph first:** typed edge tables and recursive SQL avoid a graph service while preserving Relation semantics.
5. **Blob indirection, not blob duplication:** content-addressed immutable objects and metadata refs avoid multiple full copies of evidence payloads.
6. **DB-backed outbox/workers:** avoid Kafka/NATS for a first modular monolith unless throughput/consumer isolation evidence demands them.
7. **Moka before Redis:** avoid distributed cache invalidation and another failure domain.
8. **One migration framework:** versioned SQL migrations with expand/contract, compatibility checks, and checksums across supported profiles.
9. **No separate temporal database:** preserve valid_time, recorded_at, event_time and transaction time in relational schema; add specialized temporal product only if measured query requirements exceed SQL.
10. **Projection generation/watermarks:** one generic projection lifecycle contract for FTS, vector, graph, and cache reduces bespoke cleanup logic without merging their semantics.
11. **Explicit profile matrix:** choose embedded SQLite or server PostgreSQL per authority/deployment; do not run both as simultaneous sources of truth.
12. **Keep owner boundaries typed:** reducing physical products must not collapse Event/Memory/Claim/Evidence/Relation, D/Storage/I/COC authority, or canonical vs derived representations.

---

## 12. Acceptance criteria / 验收标准

No product adoption or ADR approval should occur until the relevant criteria below are met. All tests are currently **NOT RUN by this research session** unless explicitly marked as source-inspected evidence.

### 12.1 Storage and transaction acceptance

- [ ] Exact database product, version, build, configuration, adapter, deployment manifest, operator/on-call, and authority identity are pinned.
- [ ] D admission, D ForgetFence, Storage PREPARED_HIDDEN, VisibilityPointer, Receipt, Outcome, and Outbox row ownership and transaction boundaries are Owner-approved.
- [ ] The exact `CanonicalAuthoritySerializationAnchor` is implemented and tied to the correct `BrainAuthorityRef` / `SerializationDomainRef` / DB incarnation.
- [ ] Serializable conflict/retry tests preserve immutable operation identity and reject same idempotency key with conflicting digest.
- [ ] Fence-first and participant-first races prove the required order.
- [ ] Pointer + receipt + outcome + outbox commit atomically; no partial visible state.
- [ ] Lost ACK, crash-before-commit, crash-after-commit-before-ACK, duplicate request, and ambiguous outcome are resolved by same operation/participant tuple.
- [ ] Stale replica/cache and protected read path tests cannot serve before pointer commit or after Forget suppression.
- [ ] Primary loss, promotion, old-primary rejoin fencing, split-brain attempt, and DB-incarnation mismatch tests pass.
- [ ] Restore/PITR is RESTORE_FENCED until COC/D/I/Storage prefixes and anti-rollback witnesses reconcile.

### 12.2 Search and index acceptance

- [ ] Labeled corpus includes Chinese, Japanese, English, multilingual queries, aliases, temporal qualifiers, negative/conflicting claims, and scope/tenant distributions.
- [ ] Baseline retrieval includes SQL structured filters and native lexical search before ANN.
- [ ] Compare PostgreSQL FTS vs FTS5 vs Tantivy on recall@k, precision@k, nDCG/MRR, latency percentiles, index build time, incremental update, delete, and rebuild.
- [ ] Compare exact vector search vs pgvector HNSW/IVFFlat; include filtered recall, memory, index build, write amplification, and deletion behavior.
- [ ] If Qdrant is proposed, prove outbox lag/replay, duplicate delivery, target restore, shard movement, filtered multi-tenant queries, canonical revalidation, and Forget cleanup.
- [ ] Every index row binds source ID/version/digest, model/tokenizer version, scope, policy/fence generation, and projection watermark.
- [ ] Shadow rebuild and generation switch cannot expose stale or forgotten content.
- [ ] Search outage or lag returns a safe degraded result; it cannot change canonical existence/visibility.

### 12.3 Forget, security, and multi-tenant acceptance

- [ ] Fence linearization blocks all protected read paths immediately, including search, cache, blob, graph, export, and replicas.
- [ ] Index/cache tombstone and purge are idempotent, observable, retryable, and cannot release owner barriers by themselves.
- [ ] Physical erasure and backup expiry/key destruction are tracked separately from logical suppression.
- [ ] Restore cannot resurrect content forgotten after the backup snapshot.
- [ ] Cross-tenant negative tests cover SQL, RLS, FTS, vector, Qdrant payload filters, blob, cache, graph traversal, exports, and privileged tools.
- [ ] Authorization is issued/verified by I; search filters and RLS are defense-in-depth, not authorization authority.
- [ ] No stale authorization/fence cache or replica is accepted for a protected decision.

### 12.4 Operations, migration, and license acceptance

- [ ] Backup/restore drills establish RPO/RTO; PostgreSQL WAL/PITR or SQLite Online Backup is exercised on the exact selected build.
- [ ] Disk-full, corrupt blob, missing object, WAL growth, failed migration, and interrupted index rebuild have deterministic safe behavior.
- [ ] Schema migrations are versioned, checksummed, idempotent where applicable, expand/contract, and restore-compatible.
- [ ] Index rebuild can run from canonical records and a defined event/outbox watermark without treating the index as source of truth.
- [ ] Exact release tags, MSRV, extensions, tokenizer dictionaries, build flags, transitive licenses, and cloud/service terms are reviewed.
- [ ] Independent review reads back the exact source Blobs and bilingual semantic parity.
- [ ] No implementation PASS, Gate closure, production activation, or technology freeze is inferred from a desk research report.

---

## 13. Open questions and closure conditions / 未解决事项与关闭条件

| ID | Open question | Why it matters | Closure condition |
|---|---|---|---|
| S03-OPEN-01 | Target deployment profile: single-user local, multi-user local, or server | determines SQLite vs PostgreSQL and operator model | explicit product/operations decision with user and workload assumptions |
| S03-OPEN-02 | Expected corpus size, writes/sec, concurrency, tenant count, blob size, retention | no defensible capacity/performance choice without it | measured workload model and representative dataset |
| S03-OPEN-03 | Exact current-main Storage source directories absent from pinned tree | full source contract currentness cannot be certified from main | restore/publish normative source paths or provide exact authoritative refs; re-read all linked specs |
| S03-OPEN-04 | Physical L4 DB engine/version/config and operator | required by ADR T1/T6/T7 | L4 ADR plus deployment manifest, on-call, HA/PITR and read-path evidence |
| S03-OPEN-05 | Exact D/Storage serialization anchor, row ownership and transaction/UoW | Option A requires more than same DB label | exact schema/transaction diagram and race/fault tests accepted by D and Storage |
| S03-OPEN-06 | I/COC bridge and Restore anti-rollback witness | cannot claim cross-log atomicity | exact Owner contract and restore/recovery drill |
| S03-OPEN-07 | Chinese/Japanese tokenizer and relevance quality | native FTS may be insufficient | labeled multilingual retrieval evaluation; decide FTS5/Postgres FTS/Tantivy |
| S03-OPEN-08 | Vector value and filtered ANN quality | no proof an independent vector service is needed | labeled evaluation with lexical-only baseline and scope-filtered vector comparison |
| S03-OPEN-09 | Blob retention, encryption, key custody, backup erasure policy | Forget and Evidence lifecycle depend on it | I/Storage-approved retention/key/backup policy and test |
| S03-OPEN-10 | Tenant isolation tiers | affects RLS, partitioning, separate DB/collections | threat model and tenant-size/isolation profile |
| S03-OPEN-11 | Replication, RPO/RTO and region requirements | determines HA product topology | operations-owned SLO and tested failover/restore plan |
| S03-OPEN-12 | Owner approval status for Phase 3.9 Forget terminalization proposals | proposals are not normative | exact D/I/Storage decisions and independent review |

### Final disposition / 最终结论

- **Adopt now:** no new external storage/search service. Preserve the current logical model, one Option-A serialization domain per authority, transactional outbox, and rebuildable derived-index contract.
- **Prototype next:** SQLite/WAL + FTS5 for embedded profile; PostgreSQL 18 + FTS + optional pgvector for server profile. Compare only on the same labeled workload and fault suite.
- **Defer:** Qdrant, Tantivy, LanceDB, Redis, Neo4j, Elasticsearch/OpenSearch/Quickwit until a measured requirement and complete operational/Forget proof justify them.
- **Do not freeze:** PostgreSQL, SQLite, pgvector, Qdrant, any schema, topology, or index engine. L4 remains OPEN.
- **No semantic changes:** Canonical Truth, Evidence, D Forget, I authorization, Storage visibility, and COC authority remain unchanged.
- **Research validation:** official product documentation inspected; exact project baseline/ADR blobs read; no prototype, benchmark, fault injection, security audit, or production deployment executed. Independent review is pending.

- **现在采用：** 不新增外部存储/搜索服务；保留当前逻辑模型、每 Authority 一个 Option A 序列化域、事务 Outbox 和可重建派生索引契约。
- **下一步原型：** 嵌入式 Profile 验证 SQLite/WAL + FTS5；服务端 Profile 验证 PostgreSQL 18 + FTS + 可选 pgvector。必须在同一标注工作负载和故障测试套件上比较。
- **暂缓：** Qdrant、Tantivy、LanceDB、Redis、Neo4j、Elasticsearch/OpenSearch/Quickwit，除非测量证明有必要且运维/Forget 证明齐备。
- **不得冻结：** PostgreSQL、SQLite、pgvector、Qdrant、任何 Schema、拓扑或索引引擎。L4 仍 OPEN。
- **不改变语义：** Canonical Truth、Evidence、D Forget、I Authorization、Storage Visibility 和 COC 权威均不变。
- **研究验证状态：** 已检查官方产品文档，已读取项目精确基线/ADR Blob；未执行原型、基准、故障注入、安全审计或生产部署；等待独立审查。

---

## Appendix A — Evidence register / 证据登记表

### A.1 Project sources / 项目源码

| Evidence ID | Source | Exact pin | Claim supported | Validation |
|---|---|---|---|---|
| P-01 | Repository main recursive tree | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | exact current-main path inventory; storage source dirs absent | READ BACK |
| P-02 | `README.md` | Blob `429e873bd5bf081e10a449b27e3495428e1046f1` | architecture repo; implementation not started by design; domain distinctions | READ BACK |
| P-03 | `ARCHITECTURE_ROADMAP.md` | Blob `29289361973ec4369f067706132190793cd57a6b` | tech decisions follow architecture; prototypes and ADR gates required | READ BACK |
| P-04 | `00-governance/architecture-invariants.md` | Blob `33b037318e459ebb73bea33b3186f31a41d5dcfe` | I-04/I-05/I-13/I-15/I-20/I-21/I-22 constraints | READ BACK |
| P-05 | `02-domain-model/core-entities.md` | Blob `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` | Event/MemoryVersion/Claim/Entity/Relation/Evidence/Scope semantics | READ BACK |
| P-06 | `02-domain-model/relationships-and-provenance.md` | Blob `e762f84c59f69de7a44baad2123aed46e1ffea16` | typed relations, provenance, graph representation remains open | READ BACK |
| P-07 | `13-engineering-decisions/technology-architecture-blueprint.md` | Blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | TAB-001 candidate register and required prototype list | READ BACK |
| P-08 | Storage/D Serialization Topology ADR | Blob `bb544ba2f346bdc130d524bd5c7310d86f367988` | L1 Option A selected; L4 engine/deployment open; semantic owner split | EXACT BLOB READ; not present in pinned main tree |
| P-09 | Storage v3.2.3 normative technical body | Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Storage/COC recovery and visibility contract context | EXACT BLOB READ; branch provenance, not current-main path |
| P-10 | Storage v3.3.2 manifest | Blob `5c614375e10698e4931d83deb57d20321445e068` | bundle binding and non-freeze status | EXACT BLOB READ; delegated-role manifest |
| P-11 | PR #45 / #56 / #73 metadata and bodies | #45 base/head; #56 review; #73 base `b3c666e...` head `7b4771b...` | prior research, independent review, current-main remediation boundaries | READ BACK |
| P-12 | PR #66 / #68 / #71 proposal metadata and bodies | D/I/Storage Phase 3.9 branches | Forget proposal status and owner boundaries | READ BACK; Draft proposals only |

### A.2 Official product sources / 官方产品来源

1. PostgreSQL 18 transaction isolation: https://www.postgresql.org/docs/18/transaction-iso.html — serializable failures require application retry. **OFFICIAL DOC READ**
2. PostgreSQL 18 RLS: https://www.postgresql.org/docs/18/ddl-rowsecurity.html — RLS behavior, owner/superuser/BYPASSRLS limitations. **OFFICIAL DOC READ**
3. PostgreSQL 18 FTS tables/indexes: https://www.postgresql.org/docs/18/textsearch-tables.html — tsvector, GIN indexing and query examples. **OFFICIAL DOC READ**
4. PostgreSQL 18 FTS index types: https://www.postgresql.org/docs/18/textsearch-indexes.html — GIN preferred; GiST lossy. **OFFICIAL DOC READ**
5. PostgreSQL 18 PITR: https://www.postgresql.org/docs/18/continuous-archiving.html — WAL archive, base backup, PITR, standby and operational caveats. **OFFICIAL DOC READ**
6. PostgreSQL license: https://www.postgresql.org/about/licence/ — PostgreSQL License. **OFFICIAL DOC READ**
7. SQLite WAL: https://www.sqlite.org/wal.html — reader/writer concurrency and same-host restriction. **OFFICIAL DOC READ**
8. SQLite isolation: https://www.sqlite.org/isolation.html — serializable writes by serialization; one writer at a time. **OFFICIAL DOC READ**
9. SQLite FTS5: https://www.sqlite.org/fts5.html — full-text capabilities, BM25 helpers, external-content and contentless tables. **OFFICIAL DOC READ**
10. SQLite Online Backup API: https://www.sqlite.org/backup.html — consistent online snapshots. **OFFICIAL DOC READ**
11. pgvector upstream: https://github.com/pgvector/pgvector — exact/approximate search, HNSW/IVFFlat, filtering and multi-tenancy considerations. **UPSTREAM README READ**
12. Qdrant distributed deployment: https://qdrant.tech/documentation/operations/distributed_deployment/ — cluster/shard/replication/transfer behavior. **OFFICIAL DOC READ**
13. Qdrant multi-tenancy: https://qdrant.tech/documentation/manage-data/multitenancy/ — payload filters, user-defined sharding, tiered multitenancy. **OFFICIAL DOC READ**
14. Qdrant license: https://github.com/qdrant/qdrant/blob/master/LICENSE — Apache-2.0. **UPSTREAM LICENSE READ**
15. Tantivy README: https://github.com/quickwit-oss/tantivy — Rust library, BM25, tokenizers, incremental indexing, distributed-search non-feature. **UPSTREAM README READ**
16. Tantivy license: https://github.com/quickwit-oss/tantivy/blob/main/LICENSE — MIT. **UPSTREAM LICENSE READ**
17. LanceDB README: https://github.com/lancedb/lancedb — embedded/serverless multimodal/vector positioning. **UPSTREAM README READ**
18. LanceDB license: https://github.com/lancedb/lancedb/blob/main/LICENSE — Apache-2.0. **UPSTREAM LICENSE READ**

**Evidence limits:** upstream READMEs and official docs prove documented product capabilities, not the Brain's conformance. Version tags, MSRV, binary packaging, extension compatibility, tokenizer dictionaries, cloud terms, and transitive dependency licenses must be pinned at implementation time. No project-specific performance number is asserted.

---

## Appendix B — Bilingual status vocabulary / 双语状态词汇

- **DECIDED / 已决议:** normative project decision; this report does not create one.
- **RECOMMENDED / 推荐:** preferred research direction, still subject to Owner review/ADR.
- **CANDIDATE / 候选:** plausible option requiring comparison.
- **TO_VALIDATE / 待验证:** requires prototype, benchmark, fault injection, or security evidence.
- **OPEN / 未决:** unresolved and not approved.
- **NOT RUN / 未运行:** no execution evidence is claimed.
- **READ BACK / 已读回:** exact source content was retrieved; this is not independent approval.
- **INDEPENDENT REVIEW PENDING / 等待独立审查:** a separate reviewer must verify the exact final commit and Blob.

