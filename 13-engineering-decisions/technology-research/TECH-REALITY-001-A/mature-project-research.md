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

## 10. 完整中文版本 / Chinese Version

### 10.1 研究方法

本研究直接检查外部项目 GitHub 仓库元数据、默认分支 Tree、关键实现文件、Release 元数据和官方文档。Tree SHA 标识实际检查的源码快照；Release Tag 用于可复现版本参考。滚动 main 不等于发布版本，正式选型必须固定 Tag/Commit。

### 10.2 记忆架构项目

**Mem0**（v2.2.1，Apache-2.0，Python，Tree `f1791daa86d469249c9b002f62644d58a1eb96a0`）：`Memory.add()` 支持 user/agent/run Scope；开启 inference 时先取近期对话、检索旧 Memory，再由 LLM 抽取候选事实并决定 Add/Update/Delete。Embedding 和 Vector Store 通过 Adapter Factory 接入；SQLiteManager 用 SQLite 存历史和消息，核心 Memory Retrieval 由独立 Vector Store 提供。可借鉴分阶段 Extract→Retrieve→Compare→Propose、显式 Scope、向量后端适配；不能把向量行当 Canonical Truth，也不能把 LLM Add/Update/Delete 当生命周期权威。跨 SQL/Vector/Blob/Forget 的原子性未证明。

**Zep/Graphiti**（v0.31.2，Apache-2.0，Python，Tree `869c1b279e01a2767a464581e1cb657ce0e39271`）：以 Episode 为摄入单位，抽取实体和关系，写入 Graph Node/Edge；Edge 保存 `valid_at`、`invalid_at`、`expired_at`、`reference_time` 等时间字段，并保留 Episode 来源。使用 LLM 抽取/去重，支持多个图数据库 Driver 和 Hybrid Search。可借鉴原始 Episode Provenance、Valid Time 与记录时间分离、显式 Entity Resolution；不能把 Graph Store/LLM Pipeline 当成 Brain 完整 Canonical Revision、Forget Fence、ContextVersion 或 Permission 实现。实体关系不自动意味着首版必须部署图数据库。

**Letta Code**（v0.34.63，Apache-2.0，TypeScript，Tree `b622fb1bc0941981e08da5ec2b2736d897e9bde1`）：记忆与有状态 Agent Runtime 紧密结合，采用 Agent-scoped Memory Filesystem、系统/用户目录和 Git 历史/同步，并通过 Backend Capability 处理本地/远程差异。可借鉴 Agent 记忆隔离、可读文件、版本历史和能力协商；Git 历史不能替代多记录事务、Forget 目标清单、权限和 Applied 证明。

**Hermes Agent**（v0.23.2+canary，MIT，Python，Tree `7c9b019ab5620d4c64e7b0de4aa45cbc24dea963`）：MemoryManager 管内建 Provider 和至多一个外部 Provider；Provider 按 Profile/Home 绑定，失败隔离；后台写入使用单 Worker Executor 和有界 Shutdown Drain。SQLite Session 持久化、Checkpoint、Backup/Restore 有独立代码和测试，Backup 使用 SQLite Backup API，避免只复制主 DB 而遗漏 WAL。可借鉴 Profile 隔离、有界后台任务、故障降级和真实备份测试；不能把 best-effort Provider Hook 当成 Brain Accepted Event 的持久性保证。

### 10.3 Agent Runtime 与 Durable Workflow

**LangGraph**（1.2.22，MIT，Python，Tree `02f2c2e6c992ffccce9e9129781fdd04f015c6fa`）：明确区分短期 Thread Checkpoint 与跨 Thread Store；PostgreSQL Checkpointer 有 Checkpoint、Blob、Pending Writes 表、复合键、版本迁移和 Conformance Tests。可借鉴执行状态与长期领域记忆分离、持久化行为契约；不能把 Agent Graph Checkpoint 当 Canonical Memory。

**Temporal Rust SDK**（1.2.0，MIT，Tree `a5d7742e8c5b925351fff314c2662a316309583b`）：有 Rust Client/Worker 和 Replay/Workflow State Machine；Workflow 通过持久 Event History 重放恢复，Activity 有 Retry/Heartbeat。需要独立 Temporal Service。适用于长时间 Timer、重试、取消、独立 Worker 和恢复；不替代 Canonical SQL、Forget Barrier 或 Applied。

**Restate**（Server v1.8.1-hotfix.2，Rust；Rust SDK Release v0.12.1，HEAD Manifest 0.13.0，MIT）：提供 Service、Virtual Object、Workflow；Virtual Object 按 Key 串行处理。可借鉴 Durable Handler 和按 Aggregate 串行化；但 SDK 版本较新，增加独立持久化服务，不与 Brain SQL 自动事务化。

**PydanticAI/Rig**：PydanticAI 是 Python typed Agent/Tool 框架；Rig v0.46.0 是 Rust Agent/LLM 库。两者可用于 Agent 侧集成参考，不是 Brain Durable Workflow 或 Canonical Memory Store。Brain 应拥有自己的 Provider Port 和 Conformance。

### 10.4 Event 与 Message

**NATS JetStream**（v2.15.3，Apache-2.0，Go，Tree `99cd69546eedb8450157ff0d104ffcfb23c69ec3`）：Stream 持久化消息，Consumer 保存 ACK/Delivery 状态，未确认消息可重投，支持 Replay。所谓 Exactly Once 由 Publisher Message-ID 去重窗口和 Consumer Double ACK 组成，是 Broker 交互范围内的保证，不代表任意 SQL/外部副作用 Exactly Once。首版优先 SQL Transactional Outbox + DB Worker；只有独立 Consumer、Replay、复制或实测吞吐需求成立时才引入 JetStream。

Kafka/Redpanda 提供分区日志、Offset、Replay，但不自动解决跨 Brain SQL、Blob、Forget Barrier 的事务。Broker 内事务不能原子提交任意外部数据库业务副作用。

### 10.5 Storage 与 Retrieval

SQLite WAL 允许 Reader 与 Writer 并行，但仍只有一个 Writer；WAL Index 依赖同主机共享内存，不能放在网络文件系统；长 Reader 可能阻塞 Checkpoint。PostgreSQL 使用 MVCC，并提供显式锁和 Serializable Isolation，但序列化冲突仍需 Retry。两者都不会自动把文件系统 Blob 与 SQL 提交变成同一原子事务。

FTS5 内置于 SQLite，支持 Tokenizer 和 BM25，部署最简单；中文、混合语言和领域词必须用项目语料测试。Tantivy 是 Rust 原生 Segment Index/Searcher/IndexWriter，控制力更强，但引入 Index Writer/Reader Refresh、Delete/Merge 和 Rebuild 生命周期。建议 FTS5 起步，测量不足时再引入 Tantivy。

Qdrant v1.20.2 是 Rust Server，支持 Dense/Sparse/Named Vector、Payload Filter、HNSW、Segment、Shard 和分布式部署；适合专用向量检索，不是 Canonical Store。LanceDB v0.42.0-beta.18 支持 Lance Columnar、向量/全文/Hybrid Retrieval，但当前版本 Beta；可作为派生检索库候选，不能替代事务领域数据库。

### 10.6 Security 与 Observability

Cedar 是 Rust 原生 Policy Language/Evaluator，支持 Schema Validation；适合作为嵌入式策略评估候选，但不负责身份签发、撤销传播、Inventory 或审计。OpenFGA/SpiceDB 是服务化 Zanzibar 风格关系授权，增加 API/DB/网络一致性边界。OPA/Rego/Wasm 可做通用策略分发，但 Host 仍要提供数据和执行环境。首版不应强制部署独立授权服务，I 决定语义。

OpenTelemetry Rust 0.33.1 的 Signals 成熟度不同；当前官方状态需分别看 Metrics、Logs、Tracing。建议先用 Rust `tracing` API，Exporter 作为 Adapter，禁止默认将受保护 Memory 内容写入 Trace/Log。

### 10.7 跨项目结论

1. 成熟记忆系统以不同方式分离原始对话/Episode、抽取事实、索引和 Agent Context，没有一个项目直接提供 Brain 的完整 Canonical Authority + Temporal/Provenance + Forget + Applied 语义。
2. LLM 适合抽取、实体解析和摘要建议；身份、Scope、权限、生命周期、提交顺序和 Forget 必须由确定性代码掌控。
3. Temporal Graph 是能力，不是必须部署 Graph DB 的理由。
4. Durable Workflow 不替代 Canonical SQL Transaction。
5. At-least-once Broker 仍要求业务幂等；Exactly Once 必须明确作用边界。
6. SQL + Outbox/Worker 可能是最简单首版，但前提是事务和 Forget 竞争得到证明。
7. Search/Vector 是派生投影，必须可重建、可授权过滤、可 Forget 抑制。
8. 应借鉴机制和 Conformance，而不是整体照搬单个产品架构。

### 10.8 未验证项

本任务没有运行 Brain 原型，也没有对上述系统进行集成测试、性能基准、跨平台构建或安全审计。所有性能、模型兼容、GPU 和部署结论均需目标硬件验证。


## 11. Focused implementation-boundary verification / 实现边界重点核验

The following official-document checks sharpen the integration boundaries. They are not Brain integration evidence.

### 11.1 PostgreSQL prepared transactions are a powerful but operationally sharp primitive

PostgreSQL documents `PREPARE TRANSACTION` as a mechanism for external transaction managers. A prepared transaction is durable and can later be committed or rolled back from another session, but PostgreSQL warns that leaving prepared transactions open for long periods retains locks and interferes with VACUUM. Therefore a Brain JF-10 implementation would need bounded prepare-to-decision time, durable coordinator ownership, orphan detection, operator recovery and a tested UNKNOWN/private behavior. Merely enabling `max_prepared_transactions` is not a protocol.

Sources: https://www.postgresql.org/docs/18/sql-prepare-transaction.html ; https://www.postgresql.org/docs/18/two-phase.html ; https://www.postgresql.org/docs/18/sql-commit-prepared.html

### 11.2 SQLite WAL is appropriate only inside a narrow physical envelope

SQLite WAL allows readers and a writer to overlap but still serializes writers. Its wal-index uses shared memory, requiring all participating processes to be on the same host; WAL is not supported when clients on different machines access a network filesystem. SQLite remains a reasonable local prototype candidate only if Brain's selected Storage topology is single-host and the serialized writer/fence protocol is proven under crash and concurrency tests.

Source: https://www.sqlite.org/wal.html

### 11.3 Durable workflow replay requires deterministic workflow code

Temporal's Event History is the ordered record used to replay Workflow code and reconstruct state. Decisions must be replay-deterministic; time, randomness and external effects must be mediated by replay-safe APIs or Activities. This is valuable for long-running compilation/maintenance work, but the workflow engine's history does not become Brain's Canonical Memory ledger and does not atomically close the Forget/publication race.

Source: https://docs.temporal.io/workflows

### 11.4 Broker delivery semantics do not eliminate domain idempotency

JetStream adds persistence, replay and at-least-once delivery to NATS. Publish acknowledgements and consumer acknowledgements still have failure windows in which a sender may retry or a consumer may receive a message again. The application must keep idempotent operation identity and durable deduplication in the owning transaction domain; a broker's "exactly once" feature label must be scoped to its documented broker boundary.

Source: https://docs.nats.io/concepts/jetstream

### 11.5 Filtered ANN is a workload-specific retrieval capability, not an access-control boundary

Qdrant uses HNSW for dense vector search and supports filter-aware indexing through payload indexes and filterable HNSW edges. The docs emphasize indexing fields used in filters and note that strict or combined filters affect query strategy/recall. Brain must test recall under actual Scope/tenant/time/Forget filters and still enforce authorization and visibility in the authoritative read path. A vector store must remain a derived projection.

Sources: https://qdrant.tech/documentation/manage-data/indexing/ ; https://qdrant.tech/documentation/search-design/vector-search-filtering/

### 11.6 Embedded policy evaluation still depends on host-owned identity and entity data

Cedar evaluates authorization using Principal, Action, Resource and Context; default behavior is deny unless a Permit policy grants access. Evaluation errors are diagnostically visible. This makes Cedar a plausible embedded policy engine candidate, not a complete identity or revocation system: Brain still owns trusted identity binding, entity freshness, Scope mapping, revocation and audit evidence.

Source: https://docs.cedarpolicy.com/auth/authorization.html

### 11.7 Rust observability signals have different maturity levels

The official OpenTelemetry Rust status page lists Traces as Beta and Metrics/Logs as Stable. Integrations should therefore be selected per signal and exporter, with a stable instrumentation facade and explicit privacy filtering. No protected Memory payload should be emitted by default.

Source: https://opentelemetry.io/docs/languages/rust/

### 11.8 中文综合判断

1. PostgreSQL 2PC 是强能力，但同时引入 Prepared-XID 的协调器、超时、孤儿事务、人工恢复和运维责任；不能只把数据库参数打开就宣称 JF-10 完成。
2. SQLite WAL 适用于同主机、单写者约束可接受的原型；跨主机共享数据库文件不符合 WAL 物理前提。
3. Temporal 能提供可重放的 Durable Workflow，但 Workflow 代码必须确定性；它不拥有 Canonical Memory 或 Forget 线性化点。
4. NATS JetStream 的 At-least-once 意味着重复仍需业务幂等处理，Outbox/Consumer 的去重必须落在正确的事务权威中。
5. Qdrant 能做过滤向量检索，但 Scope/Forget 过滤下的 Recall 和权限仍须在 Brain 真实读取路径证明。
6. Cedar 可评估 Permit/Forbid 策略，但身份、撤销、Scope 绑定和实体数据可信度仍归 Brain/Owner。
7. OTel Rust Traces 与 Metrics/Logs 成熟度不同，Observability 不能作为统一“已成熟”依赖处理。

No benchmark, integration or fault test was run. All recommendations remain conditional candidates, not ADR decisions.
