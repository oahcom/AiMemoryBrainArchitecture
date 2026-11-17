# Mature Project Research / 成熟项目实现研究

- Task: TECH-REALITY-001-A
- Owner: A
- Research date: 2026-11-17
- Scope: Memory architectures, Agent runtimes, durable workflow, event systems, storage, retrieval, authorization, observability
- Status: **SOURCE-INSPECTED DESK RESEARCH; PROJECT PROTOTYPES NOT RUN / 已检查源码的案头研究；本项目原型未运行**

## 1. Research method / 研究方法

For each project, the research inspected the public GitHub repository metadata, current default-branch tree, selected implementation files, current release metadata where available, and official documentation. HEAD tree SHAs identify the inspected source snapshot; release tags identify the latest release observed at capture time. A moving `main` branch is not a reproducible release, so production decisions must pin an exact tag/commit and re-run the review.

本研究检查了各项目的 GitHub 仓库元数据、默认分支 Tree、关键实现文件、可获取的最新 Release 元数据和官方文档。HEAD Tree SHA 用于标识实际检查的源码快照；Release Tag 表示采集时观察到的最新发布版本。滚动的 `main` 分支不是可复现发布版本，正式选型前必须固定 Tag/Commit 并重新审查。

## 2. Memory architecture projects / 记忆架构项目

### 2.1 Mem0

- Repository: https://github.com/mem0ai/mem0
- Inspected source snapshot: `f1791daa86d469249c9b002f62644d58a1eb96a0`
- Latest release observed: `v2.2.1` (2026-09-25)
- License: Apache-2.0; primary implementation: Python
- Inspected files: `mem0/memory/main.py`, `mem0/memory/storage.py`, `mem0/vector_stores/base.py`, vector-store provider adapters.
- Official architecture: https://github.com/mem0ai/mem0/blob/main/skills/mem0/references/architecture.md

**Observed implementation**
- `Memory.add()` accepts user/agent/run scope and an `infer` flag. With inference enabled, a phased pipeline gathers recent messages, retrieves existing memories, asks an LLM to extract candidate facts, and then decides add/update/delete operations.
- Embeddings and vector-store operations are provided through factories/adapters; the current tree includes many vector backends (Qdrant, pgvector, Chroma, Pinecone, OpenSearch, etc.).
- `SQLiteManager` in `mem0/memory/storage.py` stores history and messages in SQLite, using a process-local threading lock and explicit SQL transactions. The core memory retrieval store is a separately configured vector store.
- Search is vector-centric with scope/metadata filters and optional reranking; the implementation has entity extraction and scoring helpers.
- Delete/update history and vector mutations are separate concerns; this is not a demonstrated single physical transaction spanning canonical memory, vector index, external providers, backups and Forget barriers.

**Applicable lessons**
- Keep model-assisted extraction separate from deterministic identity/scope validation.
- Make scope filters explicit and prevent caller metadata from overriding identity.
- Treat vector stores as adapters, and preserve update/delete history.
- Use a staged extract → retrieve prior candidates → compare → propose operations pipeline.

**Do not copy**
- Do not equate vector-store memory rows with canonical memory authority.
- Do not assume LLM-chosen add/update/delete is a safe lifecycle authority.
- Do not infer project-grade Forget atomicity from delete APIs or history rows.
- The current multi-backend integration surface is broader than the first Brain vertical slice needs.

### 2.2 Zep / Graphiti

- Repository: https://github.com/getzep/graphiti
- Inspected source snapshot: `869c1b279e01a2767a464581e1cb657ce0e39271`
- Latest release observed: `v0.31.2` (2026-10-20)
- License: Apache-2.0; primary implementation: Python
- Inspected files: `graphiti_core/graphiti.py`, `nodes.py`, `edges.py`, `search/search.py`, `driver/driver.py`, Neo4j/FalkorDB/Neptune operation modules.
- Official docs: https://help.getzep.com/v2/understanding-the-graph

**Observed implementation**
- The primary ingest abstraction is an Episode. `add_episode()` processes an episode, extracts entities and relations, writes graph nodes/edges and can update communities; bulk ingestion is also supported.
- Entity nodes have names, embeddings, summaries and typed attributes. Entity edges contain fact text/embedding, episode references, `valid_at`, `invalid_at`, `expired_at` and `reference_time`.
- Raw episodes provide provenance anchors for extracted facts. The system uses LLM prompts for extraction and deduplication and supports multiple graph database drivers.
- Search combines text/vector-oriented retrieval and configurable hybrid recipes; graph proximity and temporal semantics can affect ranking.

**Applicable lessons**
- Preserve raw source episodes and link every extracted relation to its producing episodes.
- Model valid-time intervals separately from episode/recording time.
- Entity and edge identity resolution are explicit, expensive stages, not a simple string merge.
- A graph backend can be abstracted behind a driver while graph operations remain domain-specific.

**Do not copy**
- Graphiti's graph store and LLM extraction pipeline do not implement the Brain's full canonical revision, Evidence access, Forget fence, ContextVersion or PermissionEpoch contracts.
- Graph graph semantics are not a replacement for typed relational transaction constraints.
- Do not introduce Neo4j/graph DB solely because the domain contains Entity/Relation edges; relational adjacency tables and recursive queries may suffice for the first measured workload.

### 2.3 Letta

- Current repository: https://github.com/letta-ai/letta-code
- Inspected source snapshot: `b622fb1bc0941981e08da5ec2b2736d897e9bde1`
- Latest release observed: `v0.34.63` (2026-11-15)
- License: Apache-2.0; current repository primary language: TypeScript
- Inspected files: `src/agent/memory-filesystem.ts`, `src/agent/memory-git.ts`, agent context/memory modules and tests.
- Historical `letta-ai/letta` README says active current source is `letta-ai/letta-code`; old V1 API server is in the archive branch.

**Observed implementation**
- Memory is integrated into a stateful Agent runtime rather than exposed solely as a detached retrieval service.
- The current code has an Agent-scoped memory filesystem root, system/user memory directories, local/remote backend capability checks, and Git-based synchronization for memory repositories.
- Memory file changes can be versioned and synchronized via Git operations, including pre-commit hook installation and remote repository coordination.
- Agent context and memory lifecycle are integrated with backend capability negotiation and local/remote execution.

**Applicable lessons**
- Explicit Agent-scoped memory roots and separation of system/user-managed memory.
- Human-readable, inspectable memory artifacts and version history can improve debugging and recovery.
- Use capability negotiation instead of assuming all Agent backends support the same memory operations.
- Keep an Agent-facing memory interface independent of a specific backend implementation.

**Do not copy**
- Letta's memory filesystem and Agent state model are not a general canonical Brain contract.
- Git history is useful for inspectable file-based memory but is not a substitute for atomic multi-record transactions, typed cursors, Forget target inventory or authorization enforcement.
- Do not conflate an Agent's internal working/core memory with Brain-owned canonical assets or Applied Context evidence.

### 2.4 Hermes Agent

- Repository: https://github.com/NousResearch/hermes-agent
- Inspected source snapshot: `7c9b019ab5620d4c64e7b0de4aa45cbc24dea963`
- Latest release observed: `v0.23.2+canary.20261117T064624Z` (2026-11-17)
- License: MIT; primary implementation: Python
- Inspected files: `agent/memory_manager.py`, `agent/memory_provider.py`, `agent/memory_context.py`, `agent/checkpoints/manager.py`, `hermes_cli/backup_sqlite.py`, memory provider tests.
- Official repository: https://github.com/NousResearch/hermes-agent

**Observed implementation**
- `MemoryManager` owns a built-in provider plus at most one external provider; provider failures are isolated and swallowed/logged per provider.
- Provider instances are bound to profile/home scope during initialization; the contract explicitly prohibits cross-profile mutable state and rebinding a provider per call.
- Memory writes/prefetches can be scheduled in a single-worker background executor, with bounded shutdown drain and explicit abandoned-work accounting.
- The repository includes SQLite session persistence, checkpointing, recovery, backup and extensive failure/regression tests. Its SQLite backup implementation uses the SQLite backup API and fails closed rather than copying only the main database file when WAL data may be missing.
- Memory provider lifecycle hooks and session state are Agent-runtime concerns; the implementation is not a standalone Memory Brain server.

**Applicable lessons**
- Profile/tenant binding must be immutable for the lifetime of a provider instance.
- External memory failures should not corrupt or block core Agent execution; use bounded timeouts and explicit degraded status.
- Background writes need bounded queues, shutdown drain, and abandoned-work reporting.
- Backup and restore are engineering features requiring dedicated code/tests, not a README checkbox.

**Do not copy**
- A best-effort plugin hook is not sufficient for the Brain's durable Event acceptance contract.
- Provider exception swallowing must not become silent loss of a Brain-owned Accepted event.
- Hermes Agent's Agent-owned session DB is not the Brain's canonical memory transaction authority.

## 3. Agent runtime and durable workflow projects / Agent 运行时与持久工作流项目

### 3.1 LangGraph

- Repository: https://github.com/langchain-ai/langgraph
- Inspected source snapshot: `02f2c2e6c992ffccce9e9129781fdd04f015c6fa`
- Latest release observed: `1.2.22` (2026-11-14)
- License: MIT; primary implementation: Python
- Inspected files: `libs/checkpoint-postgres/langgraph/checkpoint/postgres/base.py`, checkpoint conformance suite, persistence docs.
- Official persistence docs: https://docs.langchain.com/oss/python/langgraph/persistence

**Observed implementation**
- Checkpointers persist graph/thread state; Stores persist application-defined data across threads. The project deliberately distinguishes short-term thread state from long-term store data.
- The Postgres checkpointer uses explicit tables for checkpoints, checkpoint blobs and pending writes, composite primary keys, versioned migrations and conflict-aware upserts.
- Checkpoint conformance tests define behavioral compatibility for implementations, including put/get/list, pending writes, deletion and history behavior.
- This is a graph execution/checkpoint abstraction, not a general canonical memory domain or universal distributed workflow engine.

**Applicable lessons**
- Separate execution checkpoint state from long-term domain data.
- Specify checkpointer behavior with a conformance suite rather than relying on adapter claims.
- Composite keys and durable pending writes make replay/recovery semantics explicit.

**Do not copy**
- Do not store Canonical Memory as graph checkpoint state.
- Do not let Agent graph state become the authority for Brain ContextVersion or CanonicalCommitCursor.
- The Python implementation is not a Rust runtime dependency.

### 3.2 Temporal

- Repository: https://github.com/temporalio/sdk-rust
- Inspected source snapshot: `a5d7742e8c5b925351fff314c2662a316309583b`
- Latest release observed: `v1.2.0` (2026-11-09)
- License: MIT; Rust SDK plus external Temporal Service
- Inspected files: `crates/client/src/worker.rs`, `workflow_handle.rs`, `crates/sdk-core/src/worker/workflow/managed_run.rs`, workflow state-machine modules and replay/history modules.
- Official docs: https://docs.temporal.io/evaluate/understanding-temporal

**Observed implementation**
- Temporal persists an ordered Event History for each Workflow Execution. Workflow code is replayed against that history to reconstruct workflow state after worker/process failure.
- The Rust SDK contains client/worker and a substantial workflow state-machine/replay core; it is not merely a thin HTTP client.
- Activities are separate execution units with retry/heartbeat semantics; workflow determinism and replay compatibility are architectural constraints.
- The durable service is a separately deployed infrastructure component and becomes a new stateful dependency.

**Applicable lessons**
- Durable long-running orchestration, retries, timers, task queues, cancellation and recovery are mature problems with a mature engine.
- Use Temporal if the Brain needs durable multi-hour/day orchestration with independent workers, not merely because it has background tasks.
- Workflow history is useful operational evidence for task progression.

**Do not copy**
- Temporal workflow history does not replace the Brain's canonical transactional database or its Forget publication gate.
- Do not move domain state into workflow history or treat an Activity completion as CanonicalCommit proof.
- Rust SDK support must be validated against the exact required Temporal server version, features, operational model and replay compatibility.

### 3.3 Restate

- Server repository: https://github.com/restatedev/restate
- Server latest release observed: `v1.8.1-hotfix.2` (2026-11-02); server source is Rust.
- Rust SDK repository: https://github.com/restatedev/sdk-rust
- SDK inspected source snapshot: `HEAD` tree; Cargo manifest version `0.13.0`, Rust edition 2024, MSRV 1.90, MIT.
- Inspected files: SDK `src/lib.rs`, service/handler APIs, server Bifrost loglet and workflow-related modules.
- Official SDK docs: https://docs.rs/restate-sdk/latest/restate_sdk/

**Observed implementation**
- Restate models durable handlers as Services, Virtual Objects and Workflows. Virtual Objects provide keyed state and serialized handler execution per object; workflows coordinate durable steps.
- The Rust SDK is a first-party SDK, but the observed crate version is still 0.13.0 and should be treated as a younger ecosystem surface than Tokio/SQLx.
- The server introduces its own durable execution and state-management infrastructure.

**Applicable lessons**
- Durable handlers and keyed serialization can replace some bespoke worker lease/state-machine machinery.
- A Virtual Object is a useful comparison for per-authority or per-aggregate serialization.
- Durable RPC can simplify retry and idempotency handling for external operations.

**Do not copy**
- Restate's workflow/object state does not automatically share a transaction with the Brain's chosen canonical SQL database.
- A Restate service boundary creates distributed consistency and operational obligations; it cannot make cross-database Forget atomic.
- Do not adopt before a narrow integration spike verifies failure semantics and SDK/server compatibility.

### 3.4 PydanticAI and Rig (Rust Agent libraries)

- PydanticAI: https://github.com/pydantic/pydantic-ai (MIT, Python; current repo inspected at HEAD).
- Rig: https://github.com/0xPlaygrounds/rig (MIT, Rust; current repo inspected at HEAD).
- Rig is an LLM application/Agent library with provider, tool and structured-output abstractions; it is not a durable workflow engine or canonical memory store.
- PydanticAI provides typed Agent/tool/output/dependency patterns in Python; it is useful as a comparison for model-provider boundaries, not a Rust runtime dependency.

**Conclusion**
The Brain should own its model-provider ports and conformance tests. It should not adopt a general Agent framework as its internal runtime merely to gain tool calling or planning. Rig may be evaluated as an optional Rust Agent-side integration library, but Agent orchestration remains outside the Brain's core responsibility.

## 4. Event and message infrastructure / 事件与消息基础设施

### 4.1 NATS JetStream

- Repository: https://github.com/nats-io/nats-server
- Inspected source snapshot: `99cd69546eedb8450157ff0d104ffcfb23c69ec3`
- Latest release observed: `v2.15.3` (2026-11-11)
- License: Apache-2.0; server implementation: Go
- Official docs: https://docs.nats.io/concepts/jetstream

**Observed semantics**
- Streams persist messages; consumers maintain independent delivery/acknowledgement state and can replay from sequence/time.
- Unacknowledged messages are redelivered, providing at-least-once delivery.
- JetStream's "exactly once" feature combines publisher message-ID deduplication over a configured window and double acknowledgement for consumer ACK receipt. This is a broker-level message protocol guarantee, not a transaction across application side effects or an external SQL database.
- Pull consumers provide application-controlled flow control and are recommended by the docs for new projects where scalability/error handling matter.

**Recommendation**
Start with transactional SQL outbox + DB-backed workers for local single-node use. Introduce JetStream only when independent consumers, replay retention, cross-process flow control, replication or measured queue throughput justify another durable system.

### 4.2 Kafka / Redpanda

Kafka-class brokers provide durable partitioned logs, consumer offsets and replay at scale. They do not remove application-level idempotency or cross-store transaction problems. A broker transaction can coordinate broker records/offsets within its own semantics, but cannot atomically commit arbitrary Brain SQL state, blob references, canonical cursors and Forget barriers without an additional protocol. No project-specific throughput evidence currently justifies Kafka/Redpanda.

## 5. Storage and retrieval components / 存储与检索组件

### 5.1 SQLite WAL and PostgreSQL

- SQLite official WAL documentation: https://www.sqlite.org/wal.html
- SQLite isolation documentation: https://www.sqlite.org/isolation.html
- PostgreSQL 18 concurrency control: https://www.postgresql.org/docs/current/mvcc.html

**Verified constraints**
- SQLite WAL permits concurrent readers and a writer, but still only one writer at a time. Its shared-memory wal-index requires processes to be on the same host; WAL does not work over a network filesystem. Long-lived readers can prevent checkpoint completion and cause WAL growth.
- SQLite serializes writes and can provide ACID transaction semantics on one database file. It is not a multi-host distributed transaction system.
- PostgreSQL uses MVCC and supports explicit locking and Serializable isolation, but serialization failures must be retried and application invariants still need a correct transaction design.
- Neither database automatically solves a filesystem blob write plus SQL commit as one atomic transaction; use staged content-addressed writes, durable metadata registration, integrity verification and orphan recovery.

### 5.2 FTS5 and Tantivy

- SQLite FTS5 docs: https://www.sqlite.org/fts5.html
- Tantivy repository: https://github.com/quickwit-oss/tantivy
- Inspected source snapshot: `2ad36b4fd0c00ded047b12295423250d8d4d713b`; latest release observed `0.26.1`; HEAD Cargo manifest reports `0.27.0`, so release and unreleased main must not be conflated.
- License: MIT; Rust-native.

**Observed mechanisms**
- FTS5 is colocated with SQLite, supports Unicode61/ascii/porter/trigram tokenizers and BM25 scoring. Tokenization quality for Chinese, mixed-language and domain terms must be tested; default Unicode tokenization is not automatically equivalent to a production Chinese analyzer.
- Tantivy uses immutable-ish segments, schema-defined fields, IndexWriter, segment merges and query/collector abstractions inspired by Lucene. It provides Rust-native control and ranking flexibility, but adds a separate index lifecycle, writer/reader refresh, delete/merge and rebuild concerns.
- FTS5 is the simpler first baseline; Tantivy is the Rust-native candidate if corpus/index workload or analyzer control proves insufficient.

### 5.3 Qdrant

- Repository: https://github.com/qdrant/qdrant
- Inspected source snapshot: `23065a0bf6857c3e5da45f6c8939cc746cc0580e`
- Latest release observed: `v1.20.2` (2026-11-16)
- License: Apache-2.0; Rust server, official Rust client
- Official docs: https://qdrant.tech/documentation/overview/

**Observed mechanisms**
- Client/server architecture; collections contain points with dense/sparse/named vectors and payload metadata.
- HNSW search can use payload indexes for filtering during traversal; segments are storage/index units and optimizers operate in background.
- Distributed mode adds shards, replication, transfer and recovery semantics.
- Qdrant is a strong dedicated vector retrieval service, not a canonical transaction authority for Brain Memory/Evidence/Forget.

**Recommendation**
Do not introduce Qdrant in the first vertical slice unless measured retrieval quality/latency/corpus needs require it. If adopted, keep vector records as derived projections with authoritative Brain-side scope/fence filtering and rebuild paths.

### 5.4 LanceDB

- Repository: https://github.com/lancedb/lancedb
- Inspected source snapshot: `57b20fb11d907fd8948827370e7c4032d396c205`
- Latest release observed: `v0.42.0-beta.18` (2026-11-17)
- License: Apache-2.0; Rust SDK and multi-language ecosystem.
- Official docs: https://lance.org/quickstart/

LanceDB is a retrieval database built on the Lance columnar format, with embedded and distributed modes, vector and full-text/hybrid retrieval, filtering and versioned datasets. The Rust crate manifest observed on HEAD is a beta release. It may reduce the number of retrieval-specific components, but it is not a drop-in replacement for a transactional canonical domain database, nor does dataset versioning imply Forget/authorization semantics. Evaluate it as a derived retrieval store, not as the Brain's source of truth.

## 6. Authorization and policy / 授权与策略

### 6.1 Cedar

- Repository: https://github.com/cedar-policy/cedar
- License: Apache-2.0; Rust-native policy language and evaluator.
- Official docs: https://docs.cedarpolicy.com/
- Rust crate observed on docs.rs: `cedar-policy 4.14.1`.

Cedar supports application-embedded fine-grained RBAC/ABAC-style decisions, typed entity schemas, validation and policy analysis. It is a promising Rust-native policy evaluation candidate if I's contract maps cleanly to principal/action/resource/context. It does not provide the Brain's identity issuance, target inventory, revocation propagation, distributed consistency or audit workflow by itself.

### 6.2 OpenFGA / SpiceDB

OpenFGA is a Go service implementing relationship-based authorization; its architecture requires an API service and datastore and supports PostgreSQL/MySQL/SQLite, with SQLite not intended for multiple OpenFGA instances. It is suitable when relationship tuple evaluation and a separate authorization service are needed. It introduces an external service and consistency/latency boundary. SpiceDB is a comparable Zanzibar-inspired option; it must be evaluated against consistency tokens, schema migration and revocation semantics.

### 6.3 OPA

OPA is a Go policy engine with Rego, service/sidecar and Wasm integration options. Compiled Wasm can be evaluated in another runtime, but the host still owns input/data provisioning and SDK/integration responsibilities. OPA is more suitable for general policy distribution and heterogeneous policy enforcement than a small local embedded Brain unless policy centralization or multiple enforcement points require it.

**Recommendation**
Do not introduce OpenFGA, SpiceDB or OPA as a mandatory first-deployment service. Evaluate Cedar as an embedded policy engine, while I retains the semantic authority and the Brain implements authenticated identity binding, policy epoch, revocation and fail-closed enforcement. The choice remains I-owned and OPEN.

## 7. Observability / 可观测性

- OpenTelemetry Rust repository: https://github.com/open-telemetry/opentelemetry-rust
- Inspected source snapshot: `1e29b1fe1d03bde8e48eb564a3dee8ec9efed6a7`
- Latest release observed: `opentelemetry-0.33.1` (2026-10-09)
- License: Apache-2.0.
- Official Rust status page: https://opentelemetry.io/docs/languages/rust/

OpenTelemetry Rust supports metrics, logs and traces, but the official status page reports different maturity per signal (metrics/logs stable; tracing components beta in the inspected docs). Use the Rust `tracing` ecosystem as the immediate instrumentation API, with exporters behind an adapter. Do not make all OTel signals or a full Prometheus/Grafana deployment mandatory for local development. Ensure traces and logs never include raw protected memory by default.

## 8. Cross-project conclusions / 跨项目结论

1. Mature memory systems separate raw conversation/episode, extracted facts, indexes and Agent context in different ways; none directly supplies the Brain's complete canonical authority + typed temporal/provenance + cross-owner Forget + Context Applied semantics.
2. LLMs are useful for extraction, entity resolution and summarization proposals; deterministic code must retain authority over identity, scope, permissions, lifecycle transitions, commit ordering and Forget.
3. Temporal graph memory is a capability, not an automatic requirement for a graph database in the first release.
4. Durable workflow engines are valuable for long-running orchestration, but they do not replace canonical SQL transactions or cross-system publication barriers.
5. At-least-once brokers still require idempotent business operations; "exactly once" must always name its boundary.
6. A relational database plus outbox/worker can be a simpler first deployment if the critical transaction and Forget races are proved.
7. Search indexes and vector stores are projections. They must be rebuildable, scope-filtered and fenced from stale/forgotten data.
8. The most reusable project lessons are patterns and conformance tests, not wholesale adoption of one product's architecture.

## 9. Unverified items / 未验证事项

- No project-specific benchmark was run.
- No Brain integration prototype with Mem0, Graphiti, Letta, Hermes, LangGraph, Temporal, Restate, NATS, Qdrant, Tantivy, LanceDB, Cedar or OTel was run.
- Windows/macOS/Linux packaging and runtime compatibility have not been exhaustively tested for every Rust dependency.
- Security advisories, transitive dependency audit and full license compatibility review remain required before pinning dependencies.
- Release tag and HEAD may differ; the evidence register records which was inspected. Exact dependency pinning is deferred to ADRs.


## 9. Project Owner technology-review cross-check / 项目 Owner 技术审查交叉核对

The current B–I Owner branches contain TAR-AI-001 technology review reports. Their recommendations are consistent with the external project research at a high level: typed relational domain core (B), capability-tiered Agent integration and HTTP/local IPC (C), local transactional prototype with strict fence/publication ordering (D), DB outbox/workers rather than Kafka by default (E), structured + FTS5 first and ANN later (F), SQL tables/outbox for Context prototype (G), JSON/JCS + HTTP/IPC as interoperability candidates (H), and I-owned authorization/revocation/key/Forget governance (I).

These Owner reports are **CONDITIONAL PASS** design reviews, not independent human Owner signatures. Their recorded reviewed HEADs are older than the current branch HEADs read in this task. See `owner-technology-review-synthesis.md` for exact current branch heads, report Blobs and stale-baseline comparisons.

Storage's current branch adds an important update: its serialization ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` contains a 2026-11-17 addendum selecting one logical serializable transaction domain per Canonical Memory authority as the normative v1 profile. Its scope is logical serialization only; it does not choose a database product or deployed topology. The same branch's PostgreSQL 18.7 dossier Blob `0aabf66848dc97deee028c571183c0d7204008c0` records bounded CI PASS subtests for prepared-XID persistence/lock retention/restart, synchronous failover, physical restore, ACK-loss and WAL PITR. Gate A remains PARTIAL PASS / OPEN; Gate B's amended protocol requires focused exact-owner re-review; Gate C is deferred; JF-10 runtime P0 remains OPEN and production activation is NOT AUTHORIZED.

本项目 B–I 当前分支包含 TAR-AI-001 技术审查报告。其建议与外部成熟项目研究总体一致：B 的强类型关系型领域核心；C 的分层 Agent 集成与 HTTP/本地 IPC；D 的本地事务原型和严格 Fence/Publication 顺序；E 默认采用 DB Outbox/Worker 而不是 Kafka；F 先结构化 + FTS5，再按需引入 ANN；G 的 Context SQL/Outbox 原型；H 的 JSON/JCS + HTTP/IPC 候选；I 保留授权、撤销、密钥和 Forget 治理权。

这些 Owner 报告均为 **CONDITIONAL PASS** 设计审查，不是独立人工 Owner 签署；其记录的审查 HEAD 早于本任务读取的当前分支 HEAD。精确对比见 `owner-technology-review-synthesis.md`。

Storage 当前分支有重要更新：序列化 ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` 的 2026-11-17 补充条款选择每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain 作为 v1 规范档案，但范围仅限逻辑序列化，不选择数据库产品或实际部署。相同分支的 PostgreSQL 18.7 档案 Blob `0aabf66848dc97deee028c571183c0d7204008c0` 记录了 Prepared-XID 持久化/锁保留/重启、同步故障切换、物理恢复、ACK 丢失和 WAL PITR 的有限 CI PASS 子测试。Gate A 仍 PARTIAL PASS / OPEN；Gate B 修订协议需要聚焦精确 Owner 复审；Gate C 延后；JF-10 runtime P0 仍 OPEN，禁止生产激活。
