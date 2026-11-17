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
