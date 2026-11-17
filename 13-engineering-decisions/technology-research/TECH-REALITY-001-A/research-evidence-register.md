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
| Restate Server | https://github.com/restatedev/restate — v1.8.1-hotfix.2 | `f0cfcae2b935cfe6f80de9a72a180f976da1c66c` | Repo license NOASSERTION in API / Rust | server Bifrost/loglet/workflow modules | Durable service infrastructure; adds another state authority |
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
