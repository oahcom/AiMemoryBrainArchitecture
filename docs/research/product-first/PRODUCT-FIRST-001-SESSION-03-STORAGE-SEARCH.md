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



---

# 中文完整对应版本 / Complete Chinese Peer Version

## 1. 基线与架构边界

本研究基于 `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`。README 声明当前仓库是架构定义项目，生产实现尚未开始，这是有意安排。TAB-001 是候选技术蓝图，不是技术冻结。技术选型必须经过原型、基准测试、ADR 和明确门禁。

核心不变量包括：Event、Memory、Fact/Claim、Entity、Relation、Evidence 必须区分；派生 Memory 必须保留 Provenance；Scope 与 Permission 独立强制执行；Event Time、Recorded Time、Valid Time 不得混淆；Forget 必须覆盖派生记录和二级表示；子系统边界不意味着必须拆进程、服务或 Crate；性能结论必须来自可复现测量。

Storage ADR 的精确 Blob 为 `bb544ba2f346bdc130d524bd5c7310d86f367988`。其状态必须精确理解为：

- **L1 已决议：** 每个 Canonical Memory Authority 使用一个逻辑 Serializable Transaction Domain，即 Option A。
- **L4 未决：** 实际数据库产品/版本/配置、部署清单、Operator/On-call、集群故障域、HA/PITR、受保护读路径、生产密钥托管和物理故障恢复演练。
- D 仍负责 ProducerWork Admission、ForgetFence、Lineage/Dependency 完整性、PublicationParticipant 和 D Terminality。
- Storage 仍负责 PREPARED_HIDDEN、VisibilityPointer、Storage Outcome、PublicationReceipt 和 Outbox 持久化。
- I 仍负责身份、认证、Permission、Authorization、Revocation 顺序及 CommitAuthorizationReceipt。
- COC 仍是独立 Quorum Log；不属于数据库事务，也不构成 XA。
- C 和 E 分别保留 Provider 与 Compiler 权威。

Pointer、Receipt、Outcome、Outbox 必须原子提交。隐藏 Participant 在精确 D/I Proof 验证之前不能公开。UNKNOWN/IN_DOUBT 必须保持私有并维持 Barrier。丢失 ACK 必须通过同一个不可变 Operation/Participant Tuple 恢复。陈旧副本和缓存不能绕过权威 Pointer/Fence。恢复或故障切换的序列化历史不确定时必须进入 RESTORE_FENCED。

**当前 main 的基线缺口：** 精确递归 Git Tree 有 126 个条目，但不存在根级 `09-storage-and-index/`、`03-memory-brain/`、`04-memory-compiler/`、`05-memory-runtime/`、`06-memory-context/`、`08-protocols/`、`10-security-and-governance/`、`11-consistency-and-recovery/`、`12-testing-and-acceptance/` 目录。README/文档入口仍将这些目录描述为详细规范源。因此，本报告可以绑定 Storage ADR Blob 并审查当前 Domain/Technology 文件，但不能声称已经从当前 main 完整读回缺失的 Storage/Forget 源规范。这是当前性和文档可用性发现，不代表相关 Blob 从未存在于其他分支。

## 2. PR 与 Owner 契约状态

- **PR #45：** 技术现实性研究，历史 Base 为 `b372b62c640a2b656e54b6db62a4ee67d7d8c001`，研究 Head 为 `6c7c5919c1b50f38c4d24be679a3885ee3c15b97`。它是历史候选研究包，不是当前 main 权威，也不是技术批准。
- **PR #56：** 对 #45 的独立审查，结论为 REVISE / NOT YET PROVEN / ARCHITECTURE FREEZE NOT READY。它指出 #45 的当前性和 Storage ADR 引用问题。它证明的是 #45 的审查状态，不替代本次对当前 main 的精确核验。
- **PR #73：** 基于当前 main `b3c666e67982cb3d3374e759cfb6552c7765aacb` 的 Open Draft 修复，Head 为 `7b4771b3766c616fa932b30b21c3bc0dc742f564`。它修正 Storage ADR 引用并携带 Phase 3.8/3.8.3 当前源增量，但属于角色模拟修复，不选择 L4 引擎，也不证明物理符合性。
- **PR #66、#68、#71：** D Forget、I/D Terminalization 和 Storage 审查的 Draft 提案，位于独立 Owner 分支。其正文明确说明并非最终 Owner 批准、生产实现、Forget 完成或物理擦除。不能将其提案当作 mainline 规范变更。
- **PR #52：** 较旧 Base 上的 Draft A 集成审查。它对逻辑 Option A 方向作条件接受，同时保留 L4 和精确 Owner 复审缺口，不构成当前 main 的 L4 批准。

当前逻辑 Domain 与 Option A 约束足以开展产品评估。当前 main 中尚未证明 Storage 实现契约、生产 DB Adapter、运行时部署、代表性工作负载和物理符合性。产品能力的官方文档证据较充分，但项目适配性必须等待工作负载和物理测试。

## 3. 存储产品比较

### 3.1 PostgreSQL 18

**定位：** 服务端 Canonical Transactional Store 的首选候选，不是已批准产品。

优势：
- 成熟的关系约束、事务、索引、JSON、范围/时间类型、递归 SQL、Generated Column 和 Transactional Outbox 模式。
- 支持 Serializable Isolation，但应用必须处理 Serialization Failure 并安全重试；重试必须保持相同不可变 Operation Identity，不能重复外部副作用。
- PostgreSQL 18 支持基于 WAL 的备份和 PITR；能力强，但需要演练 Base Backup、WAL 保留和 Timeline 恢复流程。
- 原生 FTS 提供 `tsvector`、`tsquery`、GIN/GiST；很多工作负载中 GIN 是首选全文索引。
- RLS 可以按数据库角色限制行可见性；启用后没有匹配 Policy 时默认拒绝。

风险和成本：
- 它是独立服务，需要负责升级、Vacuum/Autovacuum、WAL 增长、连接池、备份保留、复制、监控、容量和 On-call。
- Serializable 事务可能因竞争而 Abort，必须定义明确的重试策略。
- RLS 只能作为纵深防御，不能成为唯一授权边界：Superuser、BYPASSRLS 角色可绕过；表 Owner 通常也可绕过，除非启用 FORCE ROW LEVEL SECURITY；参照完整性检查也绕过 RLS。
- 采用 PostgreSQL 不会自动证明符合 Storage ADR 的单一序列化域。必须实现并测试 D/Storage 行归属、Transaction/UoW、Authority Anchor、Commit Path 和受保护读路径。
- 未经正式接受的强一致性 Profile，不得使用逻辑复制或异步副本处理 Fence/Currentness 敏感决策。

许可证和采用成本：
- PostgreSQL 使用 PostgreSQL License，属于宽松、类似 BSD/MIT 的许可证。pgvector 上游元数据也指向 PostgreSQL License 条款。采用时仍须核对精确 Release、Extension 打包、支持的 PostgreSQL Major 和部署镜像。

**结论：** PREFERRED SERVER CANDIDATE / L4 OPEN。每个 Canonical Memory Authority 的 D 与 Storage 物理序列化记录应共用一个 DB Transaction Domain，不能为组织边界方便而拆到两个数据库。

### 3.2 SQLite + WAL

**定位：** 嵌入式、本地优先、单主机候选。

优势：
- 进程内嵌入，无需独立 DB Server 或 DBA 服务。
- 支持 ACID 和 Serializable Write；通过串行化写入实现隔离。WAL 允许读者与一个写入者并行。
- FTS5 支持全文查询、短语/前缀/NEAR/布尔查询、BM25 辅助排序，以及 External-Content 模式。
- Online Backup API 可以在正常访问仍继续的情况下创建一致快照。
- 适合桌面、本地 Agent、单用户、离线部署，运维占用很低。

硬限制：
- 每个数据库同一时刻只有一个 Writer。高并发 Ingestion/Compiler/Publication 会排队。
- WAL 要求所有使用数据库的进程位于同一主机；不能运行在 Network Filesystem 上。
- 不是多主机 HA/Replication 底座，不能把 WAL 文件放在 NFS/共享网络存储上，也不能作为分布式事务协调器。
- 应用必须负责 Migration、文件权限、静态加密、备份轮换、磁盘满处理、损坏检测和 Restore Fencing。
- 某些 SQLite 构建方式需要显式启用 FTS5，必须验证所有目标平台捆绑的精确 SQLite Library。

**结论：** 仅作为嵌入式单主机 Profile 的 CANDIDATE。如果 D 与 Storage 使用同一 SQLite DB/Connection Transaction Domain，且所有权威记录与读路径服从同一 Serialization Anchor，则可能满足 Option A。它本身不能满足多主机 Authority 拓扑。

### 3.3 其他关系数据库

MySQL/InnoDB 和 SQL Server 都是成熟关系数据库，但目前没有足够的项目特定优势来抵消第三套 SQL 方言、不同 Serializable/Locking 语义、Adapter/测试矩阵和运维多样性成本。只有目标部署环境或 Operator 要求带来实质优势时才重新评估。第一阶段不建议采用。

## 4. 搜索产品比较

### 4.1 PostgreSQL FTS

- 支持文档/查询分词、词元归一化、排序、Highlight 和 GIN/GiST。
- 结构化 Canonical Filter、Authorization Join、Temporal Filter 与 Lexical Query 可以留在同一个 DB Query Plan。
- 对基础词法检索，Canonical Version/Outbox 与索引更新可以减少跨系统延迟。
- 语言词典和 Tokenizer 质量各不相同。中文、日文形态学和项目专用分词必须评估，不能默认英语能力足够。
- FTS Index 是派生结构，可以从批准的 Canonical Text Field 和 Version 重建。

**结论：** 服务端第一词法候选。它减少组件和一致性边界，但不代表能满足所有语言和相关性需求。

### 4.2 SQLite FTS5

- 非常适合嵌入式本地优先检索。
- 支持短语、前缀、NEAR、布尔表达式、BM25 辅助排序、Snippet 和 Highlight。
- External-Content Table 可以索引存储在别处的内容，但同步一致性由应用负责。
- FTS5 Shadow Table 属于内部结构，应用代码不应直接修改。
- Tokenizer 的中文/日文分词质量需要评估；jieba/lindera 系扩展会增加依赖、词典打包和版本复现成本。

**结论：** SQLite 被选为 Profile 时，FTS5 是第一嵌入式词法方案；索引行必须可重建。

### 4.3 Tantivy

- 受 Lucene 启发的 Rust 全文检索库，具备 BM25、短语查询、可配置 Tokenizer、增量索引、多线程索引、Mmap Directory、Facet 和范围查询。
- 中文、日文、韩文存在第三方 Tokenizer，但会引入依赖、词典/数据打包、版本管理和可复现性问题。
- Tantivy 是 Library，不是开箱即用的分布式搜索服务；其本身明确不提供分布式搜索。
- 索引更新采用 Delete + Reindex；Commit 和 Reader Reload 会影响可见性。
- 独立 Tantivy Index 是第二份持久化工件，必须处理 Rebuild、Snapshot/Version、Scope Filter、Forget Suppression 和 Watermark。

**结论：** 暂缓。只有 PostgreSQL FTS/FTS5 在标注语料评估中无法满足 Tokenizer、排序控制、吞吐或延迟时才重新评估。不能仅因为主应用是 Rust 就引入 Tantivy。

### 4.4 pgvector

- 在 PostgreSQL 中存储 Vector Type，支持 Exact Nearest Neighbor（完美召回）以及 HNSW、IVFFlat Approximate Search。
- HNSW 通常以更高内存/构建成本换取较好的速度与召回折中；IVFFlat 通常内存更低、构建更快，但需要数据感知调优。
- 常见执行计划中，Approximate Index Filter 在 ANN Scan 之后执行。选择性 Tenant/Scope Filter 可能使结果数量不足，需要 Iterative Scan、Partial Index 或 Partition。
- 共享 ANN Index 可能使一个 Tenant 的 Vector 影响另一个 Tenant 的 Recall 和 Query Speed。需根据规模和威胁模型选择 Partition 或独立 Table。
- pgvector 在 PostgreSQL 内运行，减少独立服务数量，并能与 Canonical Row 共用事务、备份、Role 和 Schema 管理；但 Vector 不因此成为 Canonical Fact。

**结论：** Lexical Baseline 之后的默认向量候选，非第一阶段正确性的必需品。先用标注语料比较 Exact Search 与小规模 HNSW。Approximate Search 的准入必须考察 Recall@k、Precision@k、Latency、Memory、Filtered Recall、Update/Delete/Rebuild 和 Forget 测试。

### 4.5 Qdrant

- 专用 Vector Database/Search Engine，具备 Payload Filter、HNSW、Snapshot、Sharding、Replication 和 Distributed Deployment。
- Distributed Mode 不等于自动 Replication：Self-hosted Operator 必须创建 Shard Replica 并管理 Shard Placement/Rebalancing；Replication Factor 和 Transfer Method 都重要。
- Qdrant 文档明确描述了 Shard Transfer 的一致性折中。Stream Records 可能具有较弱顺序且需要重新索引；Snapshot Transfer 可保留 Index/Quantization，但有额外空间和运维成本，并能提供更强顺序保证。
- Multi-tenancy 支持 Payload Filter、User-defined Sharding、Tiered Multitenancy；每 Tenant 独立 Collection 在 Tenant 数量大时会产生资源负担。
- Qdrant 上游使用 Apache-2.0；Cloud/托管服务条款与 OSS Server 许可证应分开审查。

价值：
- 独立 Vector 扩展、专用 ANN、Payload Filter、向量运维控制和托管 Cloud。
- 当向量负载、吞吐、内存、Index Size 或隔离需求超过关系数据库可接受范围时有价值。

成本：
- 第二套读写系统、Outbox Consumer、投递 Watermark、Replay/Idempotency、Snapshot/Restore 协调、Tenant Filter 正确性及 Forget Tombstone/Purge。
- PostgreSQL Canonical Visibility 与 Qdrant Index 更新之间没有原子事务。安全模式是 Canonical Commit + Outbox + 异步 Projection；查询结果必须在披露前重新由 Canonical Authority 校验。
- Qdrant 可用性不能决定 Memory 是否存在、可见、Forgotten 或已授权。

**结论：** 不纳入最小技术栈。只有向量专属需求的测量结果和 Failure/Forget/Restore 证明足以支持额外系统时才引入。

### 4.6 LanceDB

- Apache-2.0 OSS 项目，定位为基于 Lance 列式格式的 Embedded/Serverless Retrieval Database/Library，面向 Vector 与多模态数据。
- 适合本地/嵌入式向量与多模态检索实验及列式数据集。
- 不能仅因采用它就替代 Storage ADR 的事务权威。其存储/索引生命周期、事务隔离、多进程/多主机保证、恢复语义，以及与 D/Storage Serialization Anchor 的集成仍需单独核验。
- 上游 Workspace Metadata 变化较快，可能要求较新的 Rust Toolchain；采用前应固定精确 Release 和 MSRV。

**结论：** 暂缓/实验性替代方案，不作为 Canonical Transactional Store。

### 4.7 Cache 与其他组件

- **Moka：** 适合本地模块化单体中的进程内有界缓存。必须识别 Generation/Fence，设置 TTL，且可随时丢弃。Cache Hit 不能绕过 I Authorization 或 D Forget Read Suppression。
- **Redis：** 第一阶段本地模块化单体不需要。只有确有跨进程缓存/协调需求时再引入，不能成为 Durable Canonical Memory 或 Forget Authority。
- **Elasticsearch/OpenSearch/Quickwit：** 能力强，但会增加服务、索引管线、集群运维、备份、Tenant Security 和 Forget Propagation。当前没有工作负载证据证明需要。
- **Tantivy 与 Quickwit：** Tantivy 是 Rust Library；Quickwit 是基于 Tantivy 的分布式搜索引擎，不能把 Tantivy 本身称为分布式服务。

## 5. 物理部署拓扑

| 拓扑 | 组件 | 优点 | 主要风险 | 结论 |
|---|---|---|---|---|
| T0 嵌入式本地 | Rust 模块化单体 + SQLite/WAL + FTS5 + 本地内容寻址 Blob + Moka | 最小部署、离线可用、单次安装 | 单写者、同主机、单节点恢复责任 | 单用户本地 Profile 候选 |
| T1 单数据库服务 | Rust 模块化单体 + PostgreSQL + FTS + 可选 pgvector + Blob + Outbox Worker | 事务与关系集成强，一致性边界较少 | DB 运维、Serializable Retry、RLS/Tenant 设计、HA/Restore | 服务端首选候选 |
| T2 DB + Vector Service | PostgreSQL Canonical + Qdrant 派生向量投影 + Blob | 向量独立扩展/隔离 | 双存储投影延迟、Forget/Restore 编排 | 仅规模驱动 |
| T3 DB + Tantivy | PostgreSQL/SQLite Canonical + Tantivy 嵌入式索引 | BM25/Tokenizer 控制强、Rust 集成 | 自定义索引生命周期、Snapshot/Rebuild、跨存储延迟 | 原生 FTS 评估失败时 |
| T4 多服务分布式 | PostgreSQL + Qdrant + 分布式搜索 + Broker + Cache Cluster + Object Store | 独立扩展和故障域 | 一致性权威过多，运维昂贵，故障面扩大 | 第一阶段拒绝 |

所有拓扑都必须满足 Option A：一个 Canonical Memory Authority 的 D Admission/Fence 与 Storage Visibility/Outcome 权威行必须共享精确逻辑 Serializable Transaction Domain。T2/T3 可以增加派生搜索存储，但不能把这些权威行移出该域。COC 仍是独立 Quorum Log，不声称跨日志 XA 原子性。

### 5.1 Profile 建议

1. **Local Embedded：** SQLite/WAL + FTS5，仅用于明确单主机、写入并发适中的部署。所有 D/Storage Authority Record 必须位于同一 DB Transaction Domain；禁止 Network-mounted WAL。
2. **Server：** PostgreSQL 作为单一 Authority DB。先用模块化单体；D 与 Storage 可以是独立 Rust Module，但受保护提交路径不能分属独立物理事务域。
3. **Search Scale-out：** PostgreSQL 保持 Canonical；仅在规模需要时通过 Outbox 增加 Qdrant/Tantivy 等派生投影。
4. **Blob：** 单机先用内容寻址本地文件系统；多主机共享耐久容量确有需要时再用 S3-compatible/Object Storage。Canonical DB 保存 Digest、Size、Media Type、Encryption Metadata、Retention Class 和 Authority Ref。Object URL 不是权威。
5. **Cache：** 初期进程内 Moka；没有测量证据不引入 Redis。

## 6. 数据权威映射

| 数据/表示 | 权威 | 物理候选 | 重复策略 |
|---|---|---|---|
| Event Identity、分类、Recorded Time、Source/Idempotency | Event/Capture 契约 | Canonical 关系表 | 一个权威 Event；相同 Key+Digest 返回同一结果 |
| Evidence Identity、Source Ref、Locator、Availability、Integrity | Evidence/Provenance 权威 | 关系元数据 + 不可变内容引用 | 一个 Evidence Identity；允许按 Digest 保留一份源内容 |
| Memory/MemoryVersion/Claim | Canonical Memory 权威 | 关系表和不可变版本表 | 不可变版本；一个 Current Pointer |
| Entity/Relation/Typed Temporal Edge | Domain/Entity 权威 | 带类型引用和时间列的关系表 | Canonical Typed Edge，不是 Embedding/共现 |
| Provenance/Source Edge | Evidence & Provenance 权威 | 关系边表 | 保留 Source Lineage，不得抹平来源 |
| D Admission、ForgetFence、Dependency Set、PublicationParticipant | D | 同一 Option-A 事务域 | Cache/Index 不得建立第二个 D 权威 |
| Storage Hidden Participant、VisibilityPointer、Receipt、Outcome、Outbox | Storage | 同一 Option-A 事务域 | Pointer+Receipt+Outcome+Outbox 原子提交 |
| I Auth/PermissionEpoch/Revocation/CommitAuthorizationReceipt | I | I 权威 Store/Sequencer | 独立权威；数据库共置不转移语义 |
| COC Quorum Prefix/Batch/Manifest | COC | 独立 Quorum Log | 不得静默并入 SQL 或声称 XA |
| Lexical Index | 派生投影 | Postgres FTS / FTS5 / Tantivy | 可重建；绑定 Source ID/Version/Digest/Watermark |
| Vector Embedding/ANN Graph | 派生投影 | pgvector / Qdrant / LanceDB | 可重建；绑定 Model/Version/Dimension/Input Digest |
| Graph Traversal 加速 | 派生投影 | 关系索引/可选图引擎 | Typed Relation 仍由关系权威保存 |
| Blob Bytes | Blob/Content Retention 权威 | 内容寻址文件系统/Object Store | 保留策略允许时每 Digest 一份不可变内容 |
| Cache Entry | 无权威 | Moka / 可选 Redis | 可丢弃；按 Version/Fence/Permission Generation 标识 |
| Backup Snapshot | Recovery Artifact | DB Backup + Blob Snapshot + 外部证据 | 恢复对账前不得直接服务 |

### 6.1 避免重复事实

只有明确声明为派生、版本化投影，或带完整性/保留元数据的内容寻址物理副本，才允许重复。不能存在两份可独立编辑的 Canonical Proposition。

- Canonical Claim 不得复制到第二张具有独立生命周期的“Fact Table”。
- Evidence Metadata 不是重复 Claim；Evidence 通过 Typed Link 支持、反驳或限定 Claim。
- Vector Embedding 是指定 Source Version 和 Embedding Model 的派生表示，不是新事实。
- Search Document 是查询投影，不是新的 MemoryVersion。
- 不能仅凭共现或向量相似度创建 Relation。
- Blob Metadata 和 Blob Bytes 可以物理分离，但必须由 Content Digest 绑定；可变 URL 不构成 Durable Evidence。
- 反规范化读模型必须携带 Source ID、Version、Digest 和 Projection Watermark，并能丢弃重建。

## 7. Forget、Restore 与索引重建

### 7.1 Forget 流程

1. D 在定义的线性化点提交权威 ForgetFence/Suppression Transition。所有受保护读路径必须检查当前 Authority 或等价的非陈旧 Fence Proof。
2. Canonical DB Transaction 立即使对象失去服务资格。不能因为旧 Search Row、Vector、Cache Key、Blob URL、副本或预计算结果仍存在而披露内容。
3. Transactional Outbox 与相关状态变更在同一 Canonical Transaction 中记录投影失效工作。
4. Cache Invalidation 使用单调 Authority/Fence/Permission Generation；Generation 不确定时绕过缓存。
5. Lexical/Vector/Graph Projection 接收幂等 Tombstone/Purge 命令。进度按 Target、精确 Source Version、Operation ID、Target Identity 和 ACK 跟踪。
6. Blob Retention/Physical Erasure 按适用 Retention 和 Evidence Policy 单独处理。删除索引行不能证明备份、副本、Snapshot 或 Object Version 中的字节已擦除。
7. Projection Cleanup 的 UNKNOWN/IN_DOUBT 不能释放 D/I Barrier，也不能允许服务。陈旧投影可以被忽略，但不能作为 Forget 完成证明。
8. Audit Evidence 记录 Suppression、Target Enumeration、Projection Cleanup、Backup Expiry/Key Destruction 及剩余例外。

### 7.2 Restore 与 Anti-rollback

- 将 DB、Blob Storage 和派生 Search Index 恢复到隔离、不可服务环境。
- 设置 `RESTORE_FENCED`；不得接受写入、暴露 Signed URL 或提供受保护搜索结果。
- 对照独立当前 Witness，对账 COC Committed Prefix、D/I/C Owner-local Request/Admission/Effect High-water、ForgetFence Generation、Revocation/PermissionEpoch 和 Storage Visibility Outcome。
- High-water 落后、Proof 缺失或 Commit/Participant Identity 模糊的恢复状态必须拒绝或隔离。
- 只有完成对账后，才能从 Canonical State 重建派生索引；排除 Forgotten/Suppressed 内容，并绑定新 Index Generation 与恢复后的 Authority Generation。
- Restore 后使所有进程内和分布式 Cache 失效；任何 Cache Snapshot 都不能被视为权威。
- 只有相应 Owner 可以释放自己的 Gate。数据库 Restore 成功不等于获准服务。

### 7.3 索引重建要求

可重建投影必须具备：
- 稳定 Canonical Source ID 和不可变 Version；
- Source Content Digest 和 Projection Schema/Version；
- 对应的 Embedding Model ID/Version/Dimension；
- Tenant/Scope Metadata 和 Policy Generation；
- 单调 Outbox Sequence / Projection Watermark；
- 幂等 Upsert/Delete；
- 确定性的重建输入和 Tokenizer/Config Pin；
- Shadow Index Build + Validation + Atomic Generation Switch；
- 构建期间变更的 Reconciliation；
- Index Publication 前以及结果披露前的 Forget Suppression 复核。

重建可以暂时降低搜索可用性，但不能提升权威，也不能复活已 Forget 内容。

## 8. 多租户、授权和隔离

**权威边界：**
- Domain Model 拥有 Scope 语义与对象关系。
- I 拥有认证、授权、PermissionEpoch、Revocation 和 Authorization Proof。
- Brain Access/Read Path 执行授权结果与 D Forget Suppression。
- Storage 拥有持久化和 Visibility Commit，不拥有 Permission Policy。
- Search Engine 执行 Tenant/Scope Filter 作为纵深防御，不是 Authorization Truth。

**必需控制：**
- Tenant/Scope Identity 必须来自已认证 Principal 和授权 Scope Resolution，不能只信任用户可控 Query Parameter。
- 每个 Canonical Read、Evidence Dereference、Blob Retrieval、Lexical/Vector Candidate、Graph Traversal、Cache Hit、Export 和 Backup Restore Path 都必须 Scope-filter。
- PostgreSQL RLS 可以纵深防御，但 Application Role 不应是 Table Owner/Superuser/BYPASSRLS；必须测试 FORCE ROW LEVEL SECURITY 和特权维护路径。RLS 不替代 I Authorization 或 D Suppression。
- 高隔离 Tenant 应评估独立 DB/Schema/Collection/Shard；大量小 Tenant 可考虑 Partition 和严格 Filter。必须记录 Noisy Neighbor 和 Index Recall Leakage 风险。
- pgvector 的 Approximate Filter 可能发生在 ANN Candidate Scan 之后。Tenant Filter 在逻辑上正确，不代表结果数量和隔离影响都合格；必要时采用 Per-tenant Partition/Index。
- Qdrant Payload Filter 必须用于每条 Query；Collection-per-tenant 有资源开销；少量大型 Tenant 可以评估 User-defined Sharding。
- Search Candidate 在取内容或披露前，必须由 Canonical Authorization 和 Forget 状态重新验证。
- 跨租户聚合、唯一性约束、外键错误、时间、计数和 Debug Trace 都应检查 Side-channel。
- Backup 和 Support Tool 必须有明确的 Tenant-aware Access 与特权审计。

## 9. 按能力的产品决策

| 能力 | 最小实现 | 产品引入触发条件 | 状态 |
|---|---|---|---|
| Canonical Storage | PostgreSQL 或 SQLite Profile | 写入并发、HA、Operator、多主机需求 | L4 OPEN |
| Event/Evidence Storage | 关系元数据 + 内容寻址 Blob 引用 | 大型不可变 Payload/对象保留 | 候选 |
| Relational Data | SQL 表、约束、事务 | 核心必需 | RECOMMENDED |
| Vector Search | 初期省略或 pgvector Exact/HNSW Spike | 标注 Recall/Latency 证明 ANN 价值 | OPEN/TO_VALIDATE |
| Full-text Search | PostgreSQL FTS 或 SQLite FTS5 | Tokenizer/相关性/规模测试未达标 | 首选 |
| Hybrid Search | SQL Lexical + Vector Candidate Fusion + Canonical Revalidation | 检索评估证明收益 | TO_VALIDATE |
| Temporal Query | Valid Time + Recorded Time + Range Predicate/Index | 专门时序负载证明必要 | 先 SQL |
| Graph/Relationship | Typed Relational Edge + Recursive Query | 深路径遍历/图分析超出 SQL | 先 SQL |
| Blob Storage | 初期内容寻址本地 FS | 多主机耐久/容量需求 | 候选 |
| Cache | Moka 进程内、有界、可丢弃 | 测量证明跨进程需求 | 候选 |
| Index Rebuild | Outbox + Source Watermark + Shadow Generation | 生产服务索引前必须具备 | REQUIRED |
| Backup/Restore | SQLite Online Backup 或 PostgreSQL Base Backup/WAL PITR + Blob Snapshot | 随物理引擎确定 | REQUIRED |
| Multi-tenancy | I Authorization + Scope Filter + DB/Search 纵深防御 | Tenant 数量/隔离 Profile | REQUIRED |
| Replication | 本地 Profile 不复制；按需采用 PostgreSQL HA | RPO/RTO 与可用性目标 | L4 OPEN |
| Migration | 版本化 SQL Migration、Expand/Contract | 每次 Schema 演进 | REQUIRED |

## 10. 采用矩阵

| 产品 | Canonical DB | Search/Index | 第一阶段 | 后续触发 | 建议 |
|---|---:|---:|---:|---|---|
| PostgreSQL 18 | 是，候选 | 原生 FTS | 服务端 Profile | 多写入/服务端/HA | PREFERRED SERVER CANDIDATE |
| SQLite + WAL | 是，候选 | 原生 FTS5 | 嵌入式 Profile | 本地/离线/单主机 | CANDIDATE |
| pgvector | 否 | Vector Projection | 仅可选评估 | Vector Benchmark 通过 | DEFAULT VECTOR CANDIDATE |
| Qdrant | 否 | Vector Service | 否 | 专用扩展/过滤/Sharding | DEFER |
| Tantivy | 否 | Lexical Index Library | 否 | Native FTS 评估失败 | DEFER |
| LanceDB | 未批准为事务权威 | Embedded Vector/Multimodal | 否 | 嵌入式 ANN 实验 | EXPERIMENTAL |
| Redis | 否 | Cache/Coordination | 否 | 跨进程 Cache 需求 | DEFER |
| Neo4j/Graph DB | 否 | Graph Projection | 否 | 复杂图遍历/分析需求 | DEFER |
| S3-compatible Object Store | 否 | Blob Bytes | 先本地 FS | 多主机/Object Lifecycle | LATER |
| Elasticsearch/OpenSearch/Quickwit | 否 | Search Service | 否 | 实测分布式检索需求 | DEFER |

本矩阵不批准或冻结任何产品。

## 11. 推荐最小技术栈

### Profile A：本地优先嵌入式候选

- Rust 模块化单体；子系统边界保持 Module，不强制成为 Service。
- SQLite + WAL 作为每 Authority 一个事务域，使用单写者队列和明确 Busy/Retry 行为。
- FTS5 负责词法检索。
- 内容寻址本地文件系统保存不可变 Blob；SQLite 保存 Metadata 和 Digest。
- Moka 提供有界进程内 Cache，识别 Generation/Fence；Cache 不具权威。
- DB-backed Transactional Outbox/Work Queue；第一阶段不使用 Redis/NATS/Kafka。
- 初期省略 Vector Search；若确有需要，单独受控评估 Exact SQL Scan/pgvector Server Profile 与一个嵌入式 ANN Library。

### Profile B：服务端候选

- Rust 模块化单体。
- PostgreSQL 18 作为相关 Canonical Memory Authority 的单一事务域；D + Storage Serialization Row 和 Anchor 必须参与同一个 Serializable Commit Boundary。
- PostgreSQL FTS 提供初始词法检索。
- pgvector 仅在标注检索评估后可选共置；先 Exact Search，再考虑 HNSW/IVFFlat。
- 内容寻址 Object Storage（初期本地 FS；多主机运维需要时 S3-compatible）。
- Moka 本地 Cache。只有跨进程需求有测量依据才加 Redis。
- Transactional Outbox + DB-backed Worker；外部 Projection 异步且可重建。
- Qdrant/Tantivy 只能在 Outbox 和 Canonical Revalidation 后引入，并经过独立 Failure/Forget/Restore Gate。

**为什么有两个 Profile：** 产品定位本地优先且 Agent/Model 无关。SQLite 与 PostgreSQL 是不同部署 Profile，不是同一 Authority 的双活写入数据库。一个 Canonical Memory Authority 只有一个活动 Serialization Domain。跨 Profile 迁移属于受控 Authority Migration，不是实时双写真相。

**明确不做：**
- 不因 D、Storage、Index、Vector、Cache、Blob、Search 是独立 Module 就拆微服务。
- 不对 PostgreSQL 与 Qdrant 进行双重 Canonical Write。
- 未有 Typed Relation Query 工作负载证据前不加 Graph DB。
- 不把 Search Engine 作为 Canonical Truth。
- 不用 Redis/Broker 替代 DB Transaction、Forget Fence 或 COC Quorum。
- 不假设 Object Store/Index 删除等于 Physical Forget 完成。

## 12. 复杂度削减机会

1. **一个 Canonical Transaction Domain：** v1 避免 D 与 Storage 使用不同数据库；保留语义 Owner 区分，共享 L1 Option A 物理序列化底座。
2. **先原生词法检索：** 在语料证据要求前，不同时运维 FTS 和 Tantivy。
3. **Vector 作为派生能力：** Embedding Metadata/ANN Row 是 Projection；没有规模和 Recall 证据前不建 Qdrant Cluster。
4. **先用关系模型表达图：** Typed Edge Table + Recursive SQL 可以避免图服务，同时保留 Relation 语义。
5. **Blob 间接引用而非复制：** 内容寻址不可变对象 + Metadata Ref，避免 Evidence Payload 多份完整复制。
6. **DB-backed Outbox/Worker：** 第一阶段模块化单体不需要 Kafka/NATS，除非吞吐或消费者隔离证据要求。
7. **先 Moka 后 Redis：** 避免分布式 Cache Invalidation 和额外故障域。
8. **统一 Migration Framework：** 所有 Profile 使用版本化 SQL Migration、Expand/Contract、Compatibility Check 和 Checksum。
9. **不单独引入 Temporal DB：** 在关系 Schema 中保留 Valid Time、Recorded Time、Event Time 和 Transaction Time；只有测量证明 SQL 不够时再评估专门产品。
10. **统一 Projection Generation/Watermark：** 为 FTS、Vector、Graph、Cache 使用通用 Projection Lifecycle Contract，减少定制清理逻辑，但不合并语义。
11. **明确 Profile 矩阵：** 每个 Authority 选择嵌入式 SQLite 或服务端 PostgreSQL，不同时运行两套 Source of Truth。
12. **保留类型化 Owner 边界：** 削减物理产品不能合并 Event/Memory/Claim/Evidence/Relation、D/Storage/I/COC 权威，或 Canonical/Derived 表示。

## 13. 验收标准

任何产品采用或 ADR 批准前，必须满足对应标准。除明确标记为源码核验的内容外，以下测试均为本研究会话 **NOT RUN**。

### 13.1 Storage 与 Transaction

- [ ] 固定精确 DB 产品、版本、构建、配置、Adapter、部署清单、Operator/On-call 和 Authority Identity。
- [ ] D Admission、D ForgetFence、Storage PREPARED_HIDDEN、VisibilityPointer、Receipt、Outcome、Outbox 的行归属和事务边界经 Owner 批准。
- [ ] 实现精确 `CanonicalAuthoritySerializationAnchor`，绑定正确的 `BrainAuthorityRef`、`SerializationDomainRef` 和 DB Incarnation。
- [ ] Serializable Conflict/Retry 测试保持不可变 Operation Identity，并拒绝相同 Idempotency Key 携带冲突 Digest。
- [ ] Fence-first 与 Participant-first Race 证明正确顺序。
- [ ] Pointer + Receipt + Outcome + Outbox 原子提交，无部分可见状态。
- [ ] Lost ACK、Commit 前崩溃、Commit 后 ACK 前崩溃、重复请求和模糊结果都通过相同 Operation/Participant Tuple 解决。
- [ ] Stale Replica/Cache 和 Protected Read Path 测试不能在 Pointer Commit 前或 Forget Suppression 后服务。
- [ ] Primary Loss、Promotion、Old-primary Rejoin Fencing、Split-brain Attempt 和 DB-incarnation Mismatch 测试通过。
- [ ] Restore/PITR 在 COC/D/I/Storage Prefix 与 Anti-rollback Witness 对账前保持 RESTORE_FENCED。

### 13.2 Search 与 Index

- [ ] 标注语料包括中文、日文、英文、多语言查询、别名、时间限定、否定/冲突 Claim 和 Scope/Tenant 分布。
- [ ] ANN 之前先有 SQL Structured Filter 和 Native Lexical Search 基线。
- [ ] 对 PostgreSQL FTS、FTS5、Tantivy 比较 Recall@k、Precision@k、nDCG/MRR、延迟百分位、索引构建时间、增量更新、删除和重建。
- [ ] 比较 Exact Vector Search 与 pgvector HNSW/IVFFlat，包含 Filtered Recall、内存、构建、写放大和删除行为。
- [ ] 若提议 Qdrant，必须证明 Outbox Lag/Replay、重复投递、Target Restore、Shard Move、Filtered Multi-tenant Query、Canonical Revalidation 和 Forget Cleanup。
- [ ] 每条 Index Row 绑定 Source ID/Version/Digest、Model/Tokenizer Version、Scope、Policy/Fence Generation 和 Projection Watermark。
- [ ] Shadow Rebuild/Generation Switch 不得暴露陈旧或 Forgotten 内容。
- [ ] Search Outage/Lag 只能返回安全降级结果，不能改变 Canonical Existence/Visibility。

### 13.3 Forget、安全和多租户

- [ ] Fence Linearization 立即阻断 Search、Cache、Blob、Graph、Export 和 Replica 等所有受保护读路径。
- [ ] Index/Cache Tombstone/Purge 幂等、可观测、可重试，不能单独释放 Owner Barrier。
- [ ] Physical Erasure 与 Backup Expiry/Key Destruction 和 Logical Suppression 分开跟踪。
- [ ] Restore 不能复活备份快照之后已 Forget 的内容。
- [ ] 跨租户负向测试覆盖 SQL、RLS、FTS、Vector、Qdrant Payload Filter、Blob、Cache、Graph Traversal、Export 和 Privileged Tool。
- [ ] Authorization 由 I 签发/验证；Search Filter/RLS 仅为纵深防御。
- [ ] 不接受陈旧 Authorization/Fence Cache 或 Replica 作受保护决策依据。

### 13.4 运维、迁移和许可证

- [ ] Backup/Restore Drill 确立 RPO/RTO；在精确选定构建上演练 PostgreSQL WAL/PITR 或 SQLite Online Backup。
- [ ] Disk Full、Blob Corrupt、Object Missing、WAL Growth、Migration Failure 和 Index Rebuild 中断都有确定安全行为。
- [ ] Schema Migration 版本化、有 Checksum、适当幂等、Expand/Contract，并兼容 Restore。
- [ ] Index 能从 Canonical Record 和明确 Event/Outbox Watermark 重建，不把 Index 当 Source of Truth。
- [ ] 核对精确 Release Tag、MSRV、Extension、Tokenizer Dictionary、Build Flag、传递依赖许可证及 Cloud/Service 条款。
- [ ] 独立审查读回精确 Source Blob 和双语语义对等。
- [ ] 不从案头研究报告推导 Implementation PASS、Gate Closure、Production Activation 或 Technology Freeze。

## 14. 未解决事项与关闭条件

| ID | 未解决问题 | 影响 | 关闭条件 |
|---|---|---|---|
| S03-OPEN-01 | 目标部署是单用户本地、多用户本地还是服务端 | 决定 SQLite/PostgreSQL 和 Operator 模型 | 明确产品/运维决策与用户/负载假设 |
| S03-OPEN-02 | Corpus、写入速率、并发、Tenant 数、Blob 大小、Retention | 没有数据无法可靠选容量/性能 | 实测工作负载模型和代表性数据集 |
| S03-OPEN-03 | 当前 main 缺少 Storage 源目录 | 无法认证完整规范当前性 | 恢复/发布规范源路径或提供精确权威引用，并重新读取相关规范 |
| S03-OPEN-04 | L4 DB Engine/Version/Config/Operator | Storage ADR T1/T6/T7 要求 | L4 ADR、部署清单、On-call、HA/PITR 和读路径证据 |
| S03-OPEN-05 | D/Storage Serialization Anchor、行归属和 Transaction/UoW | Option A 不等于同 DB 名称 | 精确 Schema/事务图及经 D/Storage 接受的 Race/Fault 测试 |
| S03-OPEN-06 | I/COC Bridge 与 Restore Anti-rollback Witness | 不能声称跨日志原子性 | 精确 Owner 契约及 Restore/Recovery Drill |
| S03-OPEN-07 | 中文/日文 Tokenizer 和相关性质量 | 原生 FTS 可能不足 | 标注多语言检索评估并选择 FTS5/Postgres FTS/Tantivy |
| S03-OPEN-08 | Vector 价值与 Filtered ANN 质量 | 无证据证明需要独立 Vector Service | Lexical-only 基线与 Scope-filtered Vector 对比 |
| S03-OPEN-09 | Blob Retention、Encryption、Key Custody、Backup Erasure | Forget/Evidence 生命周期依赖 | I/Storage 批准的 Retention/Key/Backup Policy 和测试 |
| S03-OPEN-10 | Tenant 隔离等级 | 影响 RLS/Partition/独立 DB/Collection | Threat Model 和 Tenant Size/Isolation Profile |
| S03-OPEN-11 | Replication、RPO/RTO、Region 要求 | 决定 HA 产品拓扑 | Ops 负责的 SLO 和故障切换/恢复方案 |
| S03-OPEN-12 | Phase 3.9 Forget Terminalization 提案的 Owner 批准状态 | 提案不是规范 | 精确 D/I/Storage 决策和独立审查 |

### 最终处置

- **现在采用：** 不新增外部存储/搜索服务；保留当前逻辑模型、每 Authority 一个 Option A 序列化域、Transactional Outbox 和可重建派生索引契约。
- **下一步原型：** 嵌入式 Profile 验证 SQLite/WAL + FTS5；服务端 Profile 验证 PostgreSQL 18 + FTS + 可选 pgvector。必须在同一标注工作负载和故障测试套件上比较。
- **暂缓：** Qdrant、Tantivy、LanceDB、Redis、Neo4j、Elasticsearch/OpenSearch/Quickwit，除非测量证明有必要且运维/Forget 证明齐备。
- **不得冻结：** PostgreSQL、SQLite、pgvector、Qdrant、任何 Schema、拓扑或索引引擎。L4 仍 OPEN。
- **不改变语义：** Canonical Truth、Evidence、D Forget、I Authorization、Storage Visibility 和 COC 权威均不变。
- **研究验证：** 已检查官方产品文档，已读取项目精确基线/ADR Blob；未执行原型、基准、故障注入、安全审计或生产部署；等待独立审查。
