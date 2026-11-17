# Research Evidence Register / 研究证据登记表

- Task: TECH-REALITY-001-A | Owner A | Research date: 2026-11-17
- Evidence policy: official source first; exact inspected source snapshot recorded; moving branches are not release pins.
- Prototype status: **NOT RUN / 未运行**

## 1. Project source register / 项目源码登记

| Project | Repo / release observed | Inspected source snapshot (tree SHA) | License / language | Core inspected source locations | Key finding / limitation |
|---|---|---|---|---|---|
| Mem0 | https://github.com/mem0ai/mem0 — v2.2.1 | `f1791daa86d469249c9b002f62644d58a1eb96a0` | Apache-2.0 / Python | `mem0/memory/main.py`, `mem0/memory/storage.py`, `mem0/vector_stores/*` | LLM-assisted extraction/update/delete, vector adapter ecosystem, SQLite history; no cross-store canonical Forget proof |
| Graphiti | https://github.com/getzep/graphiti — v0.31.2 | `869c1b279e01a2767a464581e1cb657ce0e39271` | Apache-2.0 / Python | `graphiti_core/graphiti.py`, `nodes.py`, `edges.py`, `search/*`, `driver/*/operations/*` | Episode provenance, temporal edges, graph drivers and hybrid search; does not supply Brain full authority model |
| Letta Code | https://github.com/letta-ai/letta-code — v0.34.63 | `b622fb1bc0941981e08da5ec2b2736d897e9bde1` | Apache-2.0 / TypeScript | `src/agent/memory-filesystem.ts`, `src/agent/memory-git.ts`, agent context/memory modules | Agent-scoped memory filesystem, Git history/sync, backend capabilities; not general Brain canonical store |
| Hermes Agent | https://github.com/NousResearch/hermes-agent — v0.23.2+canary.20261117T064624Z | `7c9b019ab5620d4c64e7b0de4aa45cbc24dea963` | MIT / Python | `agent/memory_manager.py`, `agent/memory_provider.py`, `agent/memory_context.py`, `hermes_cli/backup_sqlite.py` | Provider isolation/profile binding/background drain; SQLite session backup; Agent-owned runtime, not Brain |
| LangGraph | https://github.com/langchain-ai/langgraph — 1.2.22 | `02f2c2e6c992ffccce9e9129781fdd04f015c6fa` | MIT / Python | `libs/checkpoint-postgres/langgraph/checkpoint/postgres/base.py`, checkpoint conformance tests | Checkpointer vs Store separation, versioned SQL migrations, pending writes; not Rust core or canonical memory |
| Temporal Rust SDK | https://github.com/temporalio/sdk-rust — v1.2.0 | `a5d7742e8c5b925351fff314c2662a316309583b` | MIT / Rust | `crates/client/src/worker.rs`, `workflow_handle.rs`, `crates/sdk-core/src/worker/workflow/managed_run.rs`, replay/state machines | Real Rust workflow replay/worker SDK; requires Temporal service; workflow history is not canonical DB transaction |
| Restate Server | https://github.com/restatedev/restate — v1.8.1-hotfix.2 | `f0cfcae2b935cfe6f80de9a72a180f976da1c66c`; canonical LICENSE: https://github.com/restatedev/restate/blob/main/LICENSE | BSL 1.1 + Additional Use Grant / Rust | server Bifrost/loglet/workflow modules | Durable service infrastructure; adds another state authority; review public managed-platform restriction separately |
| Restate Rust SDK | https://github.com/restatedev/sdk-rust — v0.12.1 | `9a08091654f1e6da905f71ffe09bdd4742ecc995` | MIT / Rust | `src/lib.rs`, `src/service.rs`, `Cargo.toml` | First-party Rust SDK; HEAD manifest 0.13.0, MSRV 1.90, ahead of latest tag |
| NATS Server | https://github.com/nats-io/nats-server — v2.15.3 | `99cd69546eedb8450157ff0d104ffcfb23c69ec3` | Apache-2.0 / Go | `server/jetstream.go` family and server stream/consumer code | JetStream durable streams/consumer ACK/replay; broker exactly-once boundary only |
| Qdrant | https://github.com/qdrant/qdrant — v1.20.2 | `23065a0bf6857c3e5da45f6c8939cc746cc0580e` | Apache-2.0 / Rust | `lib/collection/src/collection_manager/segments_searcher/*`, `lib/collection/src/shards/*`, `lib/segment/src/index/hnsw_index/*` | HNSW + payload filtering + segments/shards; external service not canonical truth |
| Tantivy | https://github.com/quickwit-oss/tantivy — 0.26.1 | `2ad36b4fd0c00ded047b12295423250d8d4d713b` | MIT / Rust | `src/index/*`, `src/indexer/*`, `src/query/*`, `src/directory/*` | Rust-native segmented lexical search; HEAD Cargo reports 0.27.0 |
| LanceDB | https://github.com/lancedb/lancedb — v0.42.0-beta.18 | `57b20fb11d907fd8948827370e7c4032d396c205` | Apache-2.0 / Rust + other SDKs | `rust/lancedb/src/connection.rs`, `query.rs`, `query/hybrid.rs`, `index/vector.rs` | Embedded/distributed retrieval DB and hybrid search; current inspected release beta |
| OpenFGA | https://github.com/openfga/openfga — v1.22.1 | `798149843737e264e64b8660baadb946528c02f0` | Apache-2.0 / Go | `internal/graph/*`, `pkg/server/check.go`, docs architecture | Zanzibar-like relationship authorization as a service + datastore |
| OPA | https://github.com/open-policy-agent/opa — v1.22.4 | `cb47e88514b31765d12fa774830cd6a8caa35440` | Apache-2.0 / Go | policy evaluator, server and Wasm integration docs/source | Rego policy service or Wasm; host owns data and Wasm runtime integration |
| Cedar | https://github.com/cedar-policy/cedar — CLI v4.15.0 | `6387cb449bbff5e7c7c9617c56e02b36310be733` | Apache-2.0 / Rust | Cedar SDK/core/validator source; public crate `cedar-policy` | Embedded Rust policy evaluator; identity/revocation still project-owned |
| Rig | https://github.com/0xPlaygrounds/rig — v0.46.0 | `6428714f6be50fdc8c05eece015c6adebbcb7233` | MIT / Rust | `rig-core` provider/tool abstractions | Agent/LLM library, not durable workflow or Brain store |
| OpenTelemetry Rust | https://github.com/open-telemetry/opentelemetry-rust — opentelemetry-0.33.1 | `1e29b1fe1d03bde8e48eb564a3dee8ec9efed6a7` | Apache-2.0 / Rust | `opentelemetry`, `opentelemetry-sdk`, exporters, docs/design | Metrics/logs stable in official status page; tracing components beta in inspected docs |

## 2. Official technical documentation / 官方技术文档

| Technology | Official source | Verified fact used |
|---|---|---|
| SQLite isolation | https://www.sqlite.org/isolation.html | SQLite serializes writers; one writer at a time |
| SQLite WAL | https://www.sqlite.org/wal.html | WAL allows readers+writer concurrency, still one writer; same-host shared memory; not network filesystem |
| PostgreSQL MVCC | https://www.postgresql.org/docs/current/mvcc.html | MVCC, transaction isolation, explicit locks and serialization failure handling |
| SQLite FTS5 | https://www.sqlite.org/fts5.html | Tokenizers and BM25; ranking semantics |
| Tantivy | https://docs.rs/tantivy/ | Index segments, schema, IndexWriter, Searcher and Directory |
| Qdrant overview | https://qdrant.tech/documentation/overview/ | Client/server, HNSW, payload filtering and segments |
| Qdrant filtering | https://qdrant.tech/course/beginners/module-2/payload-filtering/ | Payload filters can constrain HNSW traversal |
| LanceDB | https://lance.org/quickstart/ | Embedded or distributed retrieval database, Lance tables |
| NATS JetStream | https://docs.nats.io/concepts/jetstream | Durable streams, stateful consumers, ACK/redelivery/replay |
| NATS exactly-once | https://docs.nats.io/nats-concepts/jetstream/README | Message ID deduplication + double ACK; bounded broker semantics |
| Temporal | https://docs.temporal.io/evaluate/understanding-temporal | Ordered Event History and workflow replay |
| Restate Rust SDK | https://docs.rs/restate-sdk/latest/restate_sdk/ | Services, Virtual Objects and Workflows |
| LangGraph persistence | https://docs.langchain.com/oss/python/langgraph/persistence | Checkpointer for thread state vs Store for cross-thread memory |
| Graphiti/Zep | https://help.getzep.com/v2/understanding-the-graph | Episodes, entity nodes and temporal fact edges |
| Mem0 architecture | https://github.com/mem0ai/mem0/blob/main/skills/mem0/references/architecture.md | SQL facts/metadata plus vector/entity stores |
| OpenFGA architecture | https://github.com/openfga/openfga/blob/main/docs/architecture/architecture.md | API service, datastore and graph permission evaluation |
| Cedar | https://docs.cedarpolicy.com/ | Policy language, validator and embedded authorization |
| OPA Wasm | https://www.openpolicyagent.org/docs/wasm | Rego to Wasm; host provides data/imports and SDK integration |
| OpenTelemetry Rust | https://opentelemetry.io/docs/languages/rust/ | Per-signal maturity status |

## 3. Rust crate evidence / Rust Crate 证据

| Crate | Version observed | Official source |
|---|---|---|
| tokio | 1.54.1 | https://docs.rs/tokio/latest/tokio/ |
| sqlx | 0.9.0 | https://docs.rs/sqlx/latest/sqlx/ |
| rusqlite | 0.43.0 | https://docs.rs/rusqlite/latest/rusqlite/ |
| tantivy | release 0.26.1; HEAD manifest 0.27.0 | https://docs.rs/tantivy/ |
| moka | 0.12.16 | https://docs.rs/moka/latest/moka/ |
| temporalio-sdk | 1.2.0 | https://docs.rs/temporalio-sdk/latest/ |
| restate-sdk | release 0.12.1; HEAD manifest 0.13.0 | https://docs.rs/restate-sdk/latest/restate_sdk/ |
| cedar-policy | docs.rs 4.14.1; repo CLI tag v4.15.0 | https://docs.rs/cedar-policy/latest/cedar_policy/ |
| ort | 2.0.0-rc.15 | https://docs.rs/ort/latest/ort/ |
| candle-core | 0.11.1 | https://docs.rs/candle-core/latest/candle_core/ |
| opentelemetry | 0.33.1 | https://docs.rs/opentelemetry/latest/opentelemetry/ |

## 4. Evidence quality labels / 证据质量标签

- **SOURCE INSPECTED:** exact public repository tree SHA and implementation paths were read.
- **OFFICIAL DOC INSPECTED:** official documentation was consulted for the cited mechanism.
- **RELEASE OBSERVED:** GitHub release or docs.rs crate version observed on 2026-11-17.
- **NOT RUN:** no build, integration, benchmark, race/fault test or security audit was executed for this Brain task.
- **NOT PROVEN:** public project behavior does not by itself prove Brain-specific contract satisfaction.

## 5. Research limitations / 研究限制

1. HEAD tree SHAs are source snapshots, not necessarily the latest release commit. Use release tags for reproducible dependency pins.
2. Some projects publish multiple packages/SDKs with independent versions (e.g. Restate server vs Rust SDK; OpenTelemetry API vs exporters; Cedar CLI vs crate).
3. License entries reflect repository or crate metadata and are not a complete transitive license opinion.
4. No SBOM, cargo-audit, cargo-deny, SLSA/provenance verification or CVE review was run.
5. No Windows/Linux/macOS build matrix was run.
6. No Brain-specific prototype or performance measurement was run.


## 6. Project Owner technology review evidence / 项目 Owner 技术审查证据

Current Owner branch heads were read from recursive Git Trees on 2026-11-17. Published TAR report blobs were fetched directly from those branches. The reports themselves record older reviewed HEADs; exact differences and interpretation are in `owner-technology-review-synthesis.md`.

| Owner | Current branch HEAD | TAR report Blob | Report disposition |
|---|---|---|---|
| B | `8f83e4b172bc6bb41df60de58c1884886b22e617` | `fd3e5723b81de10bed806896e4be71ceb7a1669b` | Conditional Pass; Fact/Claim ADR blocked |
| C | `667bbf84b89dc1a54ddc02852477a74083d2d89b` | `ee42c7192561261789a0c7b5bd16d32c0eaaf14c` | Conditional Pass; final-submit/adapter/Applied unverified |
| D | `97e68fbd225bdf0ac71860c01077481afc162d50` | `97c049050d67dd12e0c64ef49b2b05795651608c` | Conditional Pass semantic architecture; Storage/JF-10 implementation blocked |
| E | `fdb4f67a83083d995930b88f93975b5ee36080f3` | `c94f6a8e64ba3138a27e6f316f10411ef33b7ab8` | Conditional Pass local durable compiler; publication/recovery blocked |
| F | `8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3` | `124cc9300442b0e3a1e83603910e1c332b4fae48` | Conditional Pass structured + FTS5 first; ANN conditional |
| G | `f9ca0ddc36e17f74041506f17039f0202d13042e` | `8b9ea4b4a63f7bbddbefdb0b14cf99943b3e7613` | Conditional Pass; Context transaction and Applied remain open |
| H | `f809be092a6c04db7982cc1bdbdd9c88787a4286` | `cb9d1d97604bdb71bc2f5bf47f6392e03f30ba99` | Conditional Pass; encoding/transport/security schema open |
| I | `28df608b075e619563c6367a8a1c171185c1faaf` | `c24f03aae6ce7bc76eaeb1ed33bb24fb7fcac624` | Conditional Pass architecture; deployable security and Global Forget blocked |
| Storage | `17be31915b06d98d7f822e6e5270b8cde39eb0bb` | No separate TAR-AI-001 review found | Direct current Storage artifacts below |

### Storage current exact artifacts / Storage 当前精确工件

| Artifact | Current branch path | Blob SHA | Evidence class |
|---|---|---|---|
| Serialization topology ADR (includes 2026-11-17 logical Option A addendum) | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` | Storage architecture decision: logical v1 serialization profile; physical topology/DB still open |
| PostgreSQL 18.7 Prepared-XID capability dossier | `reviews/storage-consistency/phase-3.6.2-postgres-18.7-prepared-xid-capability-dossier.md` | `0aabf66848dc97deee028c571183c0d7204008c0` | Bounded engine-level CI evidence; Gate A PARTIAL PASS / OPEN |
| Atomic producer/dependency/visibility realization | `reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md` | `2ab899ee37a18ae6c8f2f64dbb82ad6499842060` | Proposed physical realization; not selected/implemented/conformance verified |
| Visibility participant and atomic outcome contract | `reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `175ee7b1349cfdb79a19898b311a88391ed88010` | Contract semantics; no implementation proof |
| Restore high-water reference model evidence | `reviews/storage-consistency/phase-3.6.5-restore-highwater-reference-model-evidence.md` | `bf991a8a098bfdacc24bace53d452b8ccf2078e6` | 25/25 in-memory tests; no real service/DB restore |

The PostgreSQL 18.7 dossier's pinned CI profile records bounded PASS subtests for prepared-XID persistence/lock retention/hard restart/same-XID commit/rollback, two-node synchronous WAL replay/promotion, physical backup/restore, coordinator crash in participant-success/ACK gap, TCP ACK loss, standby-unavailable UNKNOWN/private and WAL PITR. It explicitly does not prove production Canonical Authority deployment, live D/I/COC integration, signed participant receipt trust, real read-path enforcement, production operator/runbook or RPO/RTO. Gate A remains PARTIAL PASS / OPEN; Gate B current amended protocol requires focused exact-owner re-review; Gate C is deferred to engineering; JF-10 runtime P0 remains OPEN.

PostgreSQL 18.7 档案记录了有限 CI 子测试 PASS：Prepared-XID 持久化/锁保留/硬重启/同 XID Commit/Rollback、双节点同步 WAL Replay/Promotion、物理备份恢复、参与者成功与 ACK 间隙协调器崩溃、TCP ACK 丢失、备机不可用时 UNKNOWN/Private、WAL PITR。它明确不能证明生产 Canonical Authority 部署、D/I/COC 实时集成、签名参与者 Receipt 信任、真实读路径、生产 Operator/Runbook 或 RPO/RTO。Gate A 仍 PARTIAL PASS / OPEN；Gate B 当前修订协议需要聚焦精确 Owner 复审；Gate C 延后到工程阶段；JF-10 runtime P0 仍 OPEN。


## 7. 完整中文版本 / Chinese Version

### 7.1 外部项目源码证据

| 项目 | 仓库/观察到的版本 | 源码 Tree SHA | 许可证/语言 | 检查的核心路径 | 主要发现 |
|---|---|---|---|---|---|
| Mem0 | mem0ai/mem0，v2.2.1 | `f1791daa86d469249c9b002f62644d58a1eb96a0` | Apache-2.0/Python | `mem0/memory/main.py`、`storage.py`、`vector_stores/*` | LLM 抽取/更新/删除，Vector Adapter，SQLite History；未证明跨存储 Forget 原子性 |
| Graphiti | getzep/graphiti，v0.31.2 | `869c1b279e01a2767a464581e1cb657ce0e39271` | Apache-2.0/Python | `graphiti.py`、`nodes.py`、`edges.py`、`search/*`、`driver/*` | Episode Provenance、Temporal Edge、Graph Driver、Hybrid Search |
| Letta Code | letta-ai/letta-code，v0.34.63 | `b622fb1bc0941981e08da5ec2b2736d897e9bde1` | Apache-2.0/TypeScript | `memory-filesystem.ts`、`memory-git.ts` | Agent 隔离文件系统、Git 历史/同步；不是 Brain Canonical Store |
| Hermes Agent | NousResearch/hermes-agent，v0.23.2 Canary | `7c9b019ab5620d4c64e7b0de4aa45cbc24dea963` | MIT/Python | `memory_manager.py`、`memory_provider.py`、`memory_context.py`、`backup_sqlite.py` | Provider 隔离、Profile 绑定、有界后台 Drain、SQLite 备份 |
| LangGraph | langchain-ai/langgraph，1.2.22 | `02f2c2e6c992ffccce9e9129781fdd04f015c6fa` | MIT/Python | Postgres Checkpointer、Conformance Test | Checkpoint 与长期 Store 分离；不是 Rust Canonical Memory |
| Temporal Rust SDK | temporalio/sdk-rust，v1.2.0 | `a5d7742e8c5b925351fff314c2662a316309583b` | MIT/Rust | Client Worker、Workflow Replay、State Machine | 真正 Rust Durable Workflow SDK；需外部 Temporal Service |
| Restate Server | restatedev/restate，v1.8.1-hotfix.2 | `f0cfcae2b935cfe6f80de9a72a180f976da1c66c`；规范 LICENSE：https://github.com/restatedev/restate/blob/main/LICENSE | BSL 1.1 + Additional Use Grant/Rust | Server Bifrost/Loglet/Workflow | Durable Service 基础设施，增加持久化权威；公共托管平台限制需单独审查 |
| Restate Rust SDK | restatedev/sdk-rust，v0.12.1 | `9a08091654f1e6da905f71ffe09bdd4742ecc995` | MIT/Rust | `src/lib.rs`、`src/service.rs`、`Cargo.toml` | 一方 Rust SDK；HEAD Manifest 0.13.0，MSRV 1.90 |
| NATS Server | nats-io/nats-server，v2.15.3 | `99cd69546eedb8450157ff0d104ffcfb23c69ec3` | Apache-2.0/Go | JetStream Stream/Consumer 实现 | Durable Stream、ACK/Redelivery/Replay；Exactly Once 仅 Broker 边界 |
| Qdrant | qdrant/qdrant，v1.20.2 | `23065a0bf6857c3e5da45f6c8939cc746cc0580e` | Apache-2.0/Rust | Collection/Segment/HNSW/Shard | HNSW、Payload Filter、Segment/Shard；不是 Canonical Truth |
| Tantivy | quickwit-oss/tantivy，0.26.1 | `2ad36b4fd0c00ded047b12295423250d8d4d713b` | MIT/Rust | `src/index`、`indexer`、`query`、`directory` | Rust 原生分段词法检索；HEAD Cargo 版本 0.27.0 |
| LanceDB | lancedb/lancedb，v0.42.0-beta.18 | `57b20fb11d907fd8948827370e7c4032d396c205` | Apache-2.0/Rust+其他 SDK | `rust/lancedb/src` | 嵌入/分布式检索 DB、Hybrid Search；当前版本 Beta |
| OpenFGA | openfga/openfga，v1.22.1 | `798149843737e264e64b8660baadb946528c02f0` | Apache-2.0/Go | `internal/graph`、`pkg/server/check.go` | Zanzibar 风格关系授权服务 |
| OPA | open-policy-agent/opa，v1.22.4 | `cb47e88514b31765d12fa774830cd6a8caa35440` | Apache-2.0/Go | Policy Evaluator、Server、Wasm | Rego 服务或 Wasm；Host 仍需提供数据和运行时 |
| Cedar | cedar-policy/cedar，CLI v4.15.0 | `6387cb449bbff5e7c7c9617c56e02b36310be733` | Apache-2.0/Rust | Cedar SDK/Core/Validator | 嵌入式 Rust Policy Evaluator；身份和撤销仍由项目实现 |
| Rig | 0xPlaygrounds/rig，v0.46.0 | `6428714f6be50fdc8c05eece015c6adebbcb7233` | MIT/Rust | `rig-core` Provider/Tool | Agent/LLM 库，不是 Durable Workflow 或 Brain Store |
| OpenTelemetry Rust | opentelemetry-rust，0.33.1 | `1e29b1fe1d03bde8e48eb564a3dee8ec9efed6a7` | Apache-2.0/Rust | API、SDK、Exporter | Metrics/Logs 与 Tracing 的成熟度需分信号核验 |

### 7.2 官方技术文档

- SQLite Isolation：确认 SQLite 写入串行化，同一时间只有一个 Writer。
- SQLite WAL：Reader/Writer 可并行，但仍只有一个 Writer；依赖同主机共享内存，不支持网络文件系统。
- PostgreSQL MVCC：使用 MVCC、事务隔离和显式锁；Serializable 冲突需要应用 Retry。
- SQLite FTS5：Tokenizer 与 BM25 排序机制。
- Tantivy：Segment、Schema、IndexWriter、Searcher 和 Directory。
- Qdrant：Client/Server、HNSW、Payload Filtering、Segment。
- LanceDB：嵌入式/分布式检索库与 Lance Table。
- NATS JetStream：Durable Stream、Consumer、ACK/Redelivery/Replay。
- Temporal：持久 Event History 和 Workflow Replay。
- Restate：Service、Virtual Object、Workflow。
- LangGraph：Thread Checkpointer 与跨 Thread Store 分离。
- Graphiti：Episode、Entity Node、Temporal Fact Edge。
- Cedar：Policy Language、Validator 和嵌入式授权。
- OPA Wasm：Rego 编译为 Wasm，Host 提供数据/Imports。
- OpenTelemetry Rust：各 Signal 独立成熟度状态。

### 7.3 Rust Crate 证据

Tokio 1.54.1、SQLx 0.9.0、rusqlite 0.43.0、Tantivy Release 0.26.1（HEAD 0.27.0）、Moka 0.12.16、Temporalio SDK 1.2.0、Restate SDK Release 0.12.1（HEAD 0.13.0）、Cedar Crate docs.rs 4.14.1（CLI Tag v4.15.0）、ort 2.0.0-rc.15、Candle Core 0.11.1、OpenTelemetry 0.33.1。具体 Crate 版本必须与 Server/CLI/Exporter 版本分别核对。

### 7.4 证据标签和限制

- **SOURCE INSPECTED：** 已检查精确公开仓库 Tree SHA 和实现路径。
- **OFFICIAL DOC INSPECTED：** 已读取官方文档。
- **RELEASE OBSERVED：** 2026-11-17 观察到 GitHub Release 或 docs.rs 版本。
- **NOT RUN：** 本任务没有运行 Brain Build、集成、基准、竞争/故障测试或安全审计。
- **NOT PROVEN：** 外部项目功能本身不能证明 Brain 特有契约满足。

Tree SHA 不一定等于最新 Release Commit；许可证信息不是完整传递依赖法律审查；本任务没有执行 SBOM、cargo-audit、cargo-deny、CVE 审查或 Windows/Linux/macOS 构建矩阵。


## 8. Focused official-document verification / 官方文档重点核验补充

This follow-up records narrow claims verified against official documentation on 2026-11-17. It supplements, but does not replace, the source-tree inspection and does not upgrade any Brain capability to PROVEN.

| Topic | Official evidence | Verified boundary / engineering implication |
|---|---|---|
| PostgreSQL prepared transactions | PostgreSQL 18 `PREPARE TRANSACTION`, two-phase transactions, and `COMMIT PREPARED`: https://www.postgresql.org/docs/18/sql-prepare-transaction.html ; https://www.postgresql.org/docs/18/two-phase.html ; https://www.postgresql.org/docs/18/sql-commit-prepared.html | Prepared state is durable and can be resolved from another session; PostgreSQL explicitly intends this for external transaction managers, warns against long-lived prepared transactions because locks remain and VACUUM is impeded. Engine support does not supply Brain's coordinator, GID mapping, receipt trust, or recovery proof. |
| SQLite WAL | https://www.sqlite.org/wal.html | Readers and one writer can overlap, but there is only one writer; WAL requires same-host shared memory and is not supported for clients on different hosts over a network filesystem. This narrows the local prototype envelope. |
| Temporal replay | https://docs.temporal.io/workflows | Workflow state is reconstructed by replaying ordered Event History; workflow code must be deterministic and external effects belong in Activities. This is durable workflow execution, not a replacement for Canonical SQL commit or Forget fencing. |
| NATS JetStream | https://docs.nats.io/concepts/jetstream | JetStream provides at-least-once delivery and replay. Duplicate publication/consumption scenarios remain possible; business idempotency is still required. |
| Qdrant filtered vector search | https://qdrant.tech/documentation/manage-data/indexing/ ; https://qdrant.tech/documentation/search-design/vector-search-filtering/ | Qdrant uses HNSW for dense vector indexing and adds payload-index-aware filtering mechanisms. Filter fields/indexes and strict-filter recall need explicit evaluation; vector ranking does not establish authorization or canonical visibility. |
| Cedar authorization | https://docs.cedarpolicy.com/auth/authorization.html | Cedar evaluates principal/action/resource/context and defaults to deny when no permit applies; policy evaluation errors are surfaced in diagnostics. Identity issuance, entity freshness, revocation and Brain-specific scope semantics remain host responsibilities. |
| OpenTelemetry Rust | https://opentelemetry.io/docs/languages/rust/ | Official Rust status currently lists Traces as Beta, Metrics and Logs as Stable. Signal maturity must not be represented as uniform; exporter and privacy policy remain deployment choices. |

### 8.1 中文核验结论

- PostgreSQL Prepared Transaction 是外部事务管理器可用的引擎原语，但长时间停留在 Prepared 状态会持续持锁并妨碍 VACUUM；必须有可靠协调器及时 Commit/Rollback。它不自动证明 Brain 的 GID、Receipt、COC/JF-10 桥接和恢复协议。
- SQLite WAL 允许 Reader 与单个 Writer 并行，但仍然只有一个 Writer，且所有连接必须位于同一主机；不能将 WAL 放在跨主机网络文件系统上。
- Temporal 通过重放有序 Event History 恢复 Workflow 状态，因此 Workflow 代码必须确定性；外部副作用应由 Activity 执行。它不是 Canonical SQL Transaction 或 Forget Fence 的替代品。
- NATS JetStream 提供 At-least-once 和 Replay，不意味着业务端天然 Exactly-once；仍需幂等键和重复处理测试。
- Qdrant 的 HNSW 与 Payload Index 能支持过滤向量检索，但严格过滤下的 Recall、索引创建时序和租户隔离必须实测；它不承担 Canonical Truth 或授权权威。
- Cedar 默认拒绝未被 Permit 明确允许的请求，但身份签发、实体数据新鲜度、撤销传播和 Brain Scope 语义仍由 Host/Owner 实现。
- OpenTelemetry Rust 的 Traces 为 Beta，Metrics/Logs 为 Stable；不得笼统声称所有 Signal 同等成熟。

These official-document checks are desk verification only. No Brain prototype, integration, benchmark, concurrency/fault test, production runbook or security audit was run.


## 7. Late Storage / JF-10 evidence refresh — 2026-11-17 / Storage 与 JF-10 最新证据

Directly fetched from Storage branch `session-storage-consistency-forget-atomicity-2026-11-16`; the v3.2.3 body Blob is recorded as a manifest pin, not claimed as an independently fetched file:

| Artifact | Path | Blob SHA | Current recorded boundary |
|---|---|---|---|
| Storage v3.2.6 successor bundle manifest | `reviews/storage-consistency/phase-3.6.16-storage-v3.2.6-successor-exact-version-bundle-manifest.md` | `dbfa37617d109d5891a067769e858085e2ce547a` | Bundle bound; H 1.2.13 exact CI open; not jointly frozen; delegated Storage-role artifact, not independent human signature |
| Normative Storage technical body v3.2.3 | Path not separately surfaced in the v3.2.6 manifest readback | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Exact Blob is pinned by the manifest; body itself was not independently fetched in this refresh |
| COC companion §§15–17 | `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md` (companion content pinned by manifest) | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest and recovery join ordering |
| PostgreSQL 18.7 capability dossier | `reviews/storage-consistency/phase-3.6.2-postgres-18.7-prepared-xid-capability-dossier.md` | `0aabf66848dc97deee028c571183c0d7204008c0` | Seven bounded CI subtests PASS; Gate A PARTIAL PASS / OPEN; production integration deferred |
| Storage deployment readiness | `reviews/storage-consistency/phase-3.6-deployment-selection-and-verification-readiness.md` | `ef4eff1708e4bd6072b86cc234340dd848bb5fbc` | Logical deployment profile selected; production Canonical Authority deployment not designated |

The seven dossier subtests cover: single-node prepared-XID/hard restart; synchronous standby replay/promotion; physical pg_basebackup restore with stale-control fail-closed fixture; coordinator crash in participant-success/ACK-checkpoint gap; TCP CommandComplete response loss; synchronous-standby-unavailable fail-closed PREPARE; WAL-archive PITR to explicit LSN. These are pinned CI fixture capabilities, not live Brain D/I/COC application conformance or production deployment proof.

Exact successor bundle members recorded by the manifest include H Unified 1.2.13 / wire 1.3.0 Blob `8e7f6a6c9663388863db88548f9c37d0fdb1bd97`, H RecoveryJoin 1.0.2 Blob `4b664e3bce465499bcdfd93796349a4ba7074002`, H RecoveryCutoff 1.0.5 Blob `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7`, H C mapping Blob `32bf9b0fd42abe8b58749b858b1d5c9aef39c5fd`, CSubmitOutcome 1.0.1 Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`, I exact review Blob `367a6002327134840b1d03d426bb4bcd864db4c9`, and D exact review Blob `1f03f3a83dda3fc1cc364ae9d2d18a3f1b96b590`. The manifest itself states C candidate CI run 44059935858 (19 tests) SUCCESS; exact H 1.2.13 15-test source has not run; prior H 1.2.12 run does not transfer.

### 7.1 Source verification corrections / 源码核验补充

- Qdrant source path should be cited as `lib/collection/src/collection_manager/segments_searcher/mod.rs` (not a standalone `segments_searcher.rs`); fetched at the pinned source snapshot `23065a0bf6857c3e5da45f6c8939cc746cc0580e`, file Blob `c2108ce6ff1465e4172401e96369e5d84e65f915`.
- Mem0 `mem0/memory/main.py`, Graphiti `graphiti_core/graphiti.py`, Letta Code `src/agent/memory-filesystem.ts`, LangGraph PostgreSQL checkpointer, Temporal Rust worker, NATS JetStream and Tantivy IndexWriter paths were fetched at the exact source snapshot commits listed in §1. Hermes source re-fetch hit GitHub API rate limiting in this refresh; the prior pinned source claim remains **NOT RE-READ IN THIS REFRESH**, not newly re-verified.
- PydanticAI durable-execution official documentation was added to `mature-project-research.md`; its Python engine integrations are comparison evidence, not a Rust dependency.

本次直接从 Storage 分支读取：

| 工件 | 路径 | Blob SHA | 当前记录边界 |
|---|---|---|---|
| Storage v3.2.6 后继 Bundle | `reviews/storage-consistency/phase-3.6.16-storage-v3.2.6-successor-exact-version-bundle-manifest.md` | `dbfa37617d109d5891a067769e858085e2ce547a` | Bundle 已绑定；H 1.2.13 精确 CI OPEN；未联合冻结；属于委派 Storage 角色工件，不是独立人工签名 |
| Storage v3.2.3 规范正文 | `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md` | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | 规范 S0a–S4 与 same-GID recovery |
| COC companion §§15–17 | 同一协议文档的独立内容 Pin | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Batch-before-Manifest 与 Recovery Join 顺序 |
| PostgreSQL 18.7 能力档案 | `reviews/storage-consistency/phase-3.6.2-postgres-18.7-prepared-xid-capability-dossier.md` | `0aabf66848dc97deee028c571183c0d7204008c0` | 七项限定 CI 子测试 PASS；Gate A PARTIAL PASS / OPEN；生产集成延后 |
| Storage 部署准备 | `reviews/storage-consistency/phase-3.6-deployment-selection-and-verification-readiness.md` | `ef4eff1708e4bd6072b86cc234340dd848bb5fbc` | 逻辑部署档案已选；生产 Canonical Authority 部署未指定 |

七项档案测试包括：单节点 Prepared-XID/硬重启；同步 Standby 重放/提升；物理 pg_basebackup 恢复与 stale-control fail-closed fixture；参与者成功/ACK 检查点间 Coordinator 崩溃；TCP CommandComplete 响应丢失；同步 Standby 不可用时 PREPARE fail-closed；显式 LSN 的 WAL Archive PITR。这些仅是固定 CI Fixture 能力，不是 Brain 实时 D/I/COC 应用一致性或生产部署证明。

Manifest 记录的后继 Bundle 还包括 H Unified 1.2.13 / wire 1.3.0、H RecoveryJoin 1.0.2、H RecoveryCutoff 1.0.5、H C 映射、CSubmitOutcome 1.0.1、I 精确审查和 D 精确审查等 Blob，详见上方表格。Manifest 记录 C 候选 CI Run 44059935858（19 项测试）SUCCESS；H 1.2.13 的 15 项测试源码尚未运行；此前 H 1.2.12 的结果不能转移。

源码核验更正：Qdrant 的准确源码路径是 `segments_searcher/mod.rs`；Mem0、Graphiti、Letta Code、LangGraph PostgreSQL Checkpointer、Temporal Rust Worker、NATS JetStream 和 Tantivy IndexWriter 已按 §1 所列精确提交读回。此次重新读取 Hermes 源码时触发 GitHub API Rate Limit，因此本轮未重新验证，不将旧 Pin 记为本轮新核验。新增 PydanticAI 持久执行官方文档，但其 Python 集成仅作为比较证据，不是 Rust 依赖。

## 6. Phase 3.8 / 3.8.3 current owner evidence pins / 当前 Owner 证据 Pin

| Owner | Artifact | Branch / Blob | Status and scope |
|---|---|---|---|
| D | Phase 3.8 publication participant and terminal contract | `session-d-memory-brain-2026-11-16` / `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` | Role proposal; approval/API/conformance OPEN |
| E | Phase 3.8 publication orchestration/retry/recovery | `session-e-memory-compiler-2026-11-16` / `475fee41e5eea527af4edefbfe88c58c86967d0a` | Role proposal; D/I/Storage APIs and approval OPEN |
| I | Phase 3.8 commit authorization/revocation sequencer | `session-i-security-governance-2026-11-16` / `54bab0484bd232a5a258e65e34cc7425288b39a6` | Role proposal; approval/crypto/conformance OPEN |
| Storage | Phase 3.8 visibility participant and atomic outcome | `session-storage-consistency-forget-atomicity-2026-11-16` / `175ee7b1349cfdb79a19898b311a88391ed88010` | Logical transaction proposal; physical topology OPEN |
| Storage ADR | Phase 3.8.2 serialization topology ADR | same Storage branch / `bb544ba2f346bdc130d524bd5c7310d86f367988` | L1 Option A selected; L4 physical engine/deployment OPEN |
| A | Phase 3.8.1 contract surface and exact-pin refresh | `session-a-integration-2026-11-16` / `89f81b16e398653ece127709346baa64baf078ab` | Proposed; not Owner-approved/frozen |
| I crypto | `AIMBA-I-CRYPTO-1.0` | Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2` | Candidate only; no production key custody proof |
| H wire/schema | wire mapping `b132e6a01bcfe13f92020b9778ee3f7ddbf65753`; Unified 1.2.8 `70b892797d07489936300a26c0dedfafe1d6e746`; RecoveryJoin 1.0.1 `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c` | Issue #25 evidence | Candidate schemas only; exact H 1.2.13 CI OPEN |
| C | provider-side-effect review `a7b57bd5531222559666f0f1d9df59a259cde61a` | Issue #25 evidence | Review only; live Owner Ledger adapter/fault/race proof OPEN |

H CI run `44043259259` (97/97) is structural/reference-model scope; run `44044062849` (101 tests) is candidate differential/structural scope. Neither proves production wire/crypto or Brain end-to-end conformance. Issue #3 Applied status remains Frozen NO / Test NO-NO / Implementation Verified NO.

Restate Server canonical LICENSE is BSL 1.1 with Additional Use Grant; API metadata `NOASSERTION` is not a sufficient license conclusion. Record Server and Rust SDK MIT as separate components. See [OWNER-REMEDIATION-001](owner-remediation/OWNER-REMEDIATION-001.md).

**中文：** 上表记录当前 Phase 3.8/3.8.3 Owner 工件的精确 Blob 与证据范围。D/E/I/Storage 均为角色提案，A 为未批准提案；H CI 仅候选结构/参考模型或差分测试，不是生产 Wire/Crypto 或 Brain 端到端证明。Issue #3 Applied 仍为未冻结、未测试、未验证实现。Restate Server 规范许可证为 BSL 1.1 + Additional Use Grant；不能只记 API 元数据 NOASSERTION，且必须与 Rust SDK MIT 分开登记。
