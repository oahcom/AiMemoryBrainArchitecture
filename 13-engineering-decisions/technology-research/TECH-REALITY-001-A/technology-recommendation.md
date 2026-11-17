# Technology Recommendation / 技术栈建议

- Task: TECH-REALITY-001-A | Owner A | Date: 2026-11-17
- Status: **THREE CANDIDATE STACKS — NONE APPROVED / 三套候选方案，均未批准**

## 1. Decision boundary / 决策边界

This document offers system-level options. It does not approve an ADR, freeze a library, select a deployment topology or override B–I/Storage decisions. The recommendations are conditional on the current logical contracts and must be validated by prototypes and owner review.

本文件提供系统级方案，不批准 ADR、不冻结库、不选择部署拓扑，也不覆盖 B–I/Storage 的决策权。所有建议均以当前逻辑契约为前提，并必须通过原型与 Owner 审查。

## 2. Stack 1 — Minimum viable / 最小可行技术栈

**Purpose:** Profile S, single-user local-first prototype; minimum moving parts.

| Layer | Candidate choice | Why | Alternatives / conditions |
|---|---|---|---|
| Core language/runtime | Rust + Tokio | DECIDED language direction; mature async ecosystem | Tokio is RECOMMENDED, not frozen |
| Storage | SQLite + WAL via SQLx or rusqlite; choose one | One local transaction authority, simple install | PostgreSQL if single-writer/remote workload fails measured envelope |
| Blob | Content-addressed local filesystem + SQL metadata | Simple large-payload storage and digest verification | DB BLOB for small data only; object store later |
| Event | SQL transactional outbox + bounded DB-backed workers | Keeps acceptance and work intent in same DB transaction | NATS only when independent consumers/replay/scale require it |
| Workflow | Explicit durable work table, lease, fencing and retry | Sufficient for short/medium local jobs if tested | Temporal/Restate if durable timers/workflow complexity outgrows DB worker |
| Search | SQL structured filters + FTS5 | Lowest deployment complexity | Tantivy if language/ranking/index load needs it |
| Vector | None in first vertical slice; add one only after recall benchmark | Avoid index/Forget complexity before proof of need | sqlite-vec/usearch/LanceDB/Qdrant alternatives |
| Cache | Moka optional and bounded | In-process; disposable | No cache is safer until invalidation contract is proven |
| Agent integration | Brain-owned provider ports; Agent-specific Adapter SDKs | Preserve framework/model independence | Rig may be used externally by Agent, not as Brain core |
| Protocol | H-owned versioned JSON over authenticated HTTP/local IPC candidate | Debuggable and cross-language | CBOR/gRPC only after payload/streaming benchmark |
| Security | I-owned identity/policy; evaluate embedded Cedar | Avoid mandatory policy service initially | OpenFGA/SpiceDB/OPA if policy topology requires it |
| Observability | Rust tracing + structured redacted logs + basic metrics | Low-cost local diagnostics | OTel exporters and Prometheus/Grafana when operational need exists |
| Deployment | One Rust app process; optional inference process; systemd/OCI packaging | Clear single-node fault/transaction boundary | Do not require Kubernetes |
| Backup/recovery | SQLite backup API/consistent DB snapshot + blob manifest/checksum + isolated restore + Forget replay | A DB file copy alone is not a complete backup | PostgreSQL-native backup when Postgres is selected |

**Required caveat:** SQLite WAL remains one writer and same-host only. This stack is viable only if the critical D/E/Storage races can be linearized inside the same SQLite transaction/locking design and the measured Profile S workload passes.

**必要限制：** SQLite WAL 仍然是单写者且仅限同一主机。只有当 D/E/Storage 关键竞争能在同一 SQLite 事务/锁设计内线性化，且 Profile S 实测通过时，该方案才可行。

## 3. Stack 2 — Balanced / 平衡型技术栈

**Purpose:** Profile M, multiple Agent instances, remote access and heavier retrieval/workflow demands.

| Layer | Candidate choice | Why | Alternatives / conditions |
|---|---|---|---|
| Core | Rust + Tokio modular monolith | Keep canonical logic and transaction coordination cohesive | Split worker processes only with measured isolation needs |
| Storage | PostgreSQL as primary transaction authority | MVCC, row locks, concurrent writers and multi-process access | SQLite remains local/offline profile option if supported deliberately |
| Blob | Content-addressed filesystem/object storage with manifest | Large source artifacts and backups | S3-compatible service only when remote scale needs it |
| Event | PostgreSQL outbox + independent worker pool | Durable local atomic handoff | NATS JetStream if independent consumers/replay/replication justify it |
| Workflow | SQL durable jobs initially; evaluate Temporal or Restate for long-running workflows | Avoid early second state authority | Select one durable engine only after end-to-end spike |
| Search | PostgreSQL structured filters + FTS5 (SQLite profile) or Tantivy | Hybrid structured/lexical search | OpenSearch only if scale/query features justify service |
| Vector | pgvector or Qdrant as derived projection; choose one | PostgreSQL consolidation vs dedicated ANN | LanceDB if embedded/columnar and hybrid benchmark wins |
| Cache | Moka per process; Redis only if cross-process cache has measured value | Local bounded cache first | Cache never authoritative for auth/Forget |
| Agent integration | Capability-based SDK and adapters; HTTP/JSON initial candidate | Heterogeneous Agents | Rust Rig optional outside Brain |
| Protocol | BMCP versioned schema; HTTP/2/gRPC if streaming/client generation matters | Cross-language compatibility | H decides |
| Security | Cedar embedded evaluation candidate plus I-owned identity/revocation layer | Rust native and local low-latency | OpenFGA/SpiceDB if relationship tuples become first-class service requirement |
| Observability | tracing + OTel Collector; Prometheus/Grafana optional | Cross-process trace correlation | Avoid raw content in telemetry |
| Deployment | Brain core + optional compiler/index/inference workers; OCI/systemd | Separate heavy resources while preserving SQL authority | Kubernetes only with multi-node ops need |
| Backup/recovery | PostgreSQL PITR/base backup + blob snapshot manifest + index rebuild + Forget/revocation restore gate | Mature multi-writer recovery | RPO/RTO must be approved |

**Required caveat:** PostgreSQL solves multi-writer database concurrency better than SQLite, but it does not solve cross-service atomicity, filesystem blob atomicity, external provider delivery or Forget target completeness. Every additional index/worker remains a separate recovery target.

**必要限制：** PostgreSQL 比 SQLite 更适合多写者数据库并发，但不能解决跨服务原子性、文件系统 Blob 原子性、外部 Provider 投递或 Forget 目标完整性。每个额外索引/Worker 仍是独立恢复目标。

## 4. Stack 3 — High scalability / 高扩展型技术栈

**Purpose:** Profile L only after multi-tenant service workload, operational ownership and availability targets are demonstrated.

| Layer | Candidate choice | Why | Alternatives / conditions |
|---|---|---|---|
| Core | Rust services with strict contracts and explicit service ownership | Independent scaling/fault domains | Keep Canonical transaction authority singular |
| Storage | PostgreSQL primary per authority domain; partitioning/replicas as needed | Multi-tenant, high concurrency | FoundationDB only with a specific proven transaction/data-model need |
| Blob | Object storage with immutable version/digest manifest | Large retained evidence and backup | Encryption/retention/restore governance required |
| Event | Kafka/Redpanda or NATS JetStream selected by partition/replay/consumer requirements | Durable multi-consumer streams | No broker guarantees arbitrary SQL exactly-once effects |
| Workflow | Temporal or Restate | Durable long-running orchestration and independent workers | Must integrate with canonical DB through idempotent activities/outbox |
| Search | Tantivy/OpenSearch/Qdrant as separately operated projections | Scale and channel-specific tuning | Avoid unnecessary overlap; define one source per channel |
| Vector | Qdrant cluster or managed vector store | Sharding, replication, ANN filters | Only if corpus/QPS/availability demands it |
| Cache | Moka local + Redis/KeyDB distributed only for measured shared-cache needs | Cross-process hot data | Current policy/fence must be revalidated on protected reads |
| Agent integration | Independent gateway + SDKs across Agent languages | Tenant auth, network ingress, streaming | C/H own protocol and adapter semantics |
| Protocol | Versioned BMCP over gRPC/HTTP2 or equivalent | Streaming, typed clients, multi-language | Compatibility and downgrade policy |
| Security | OpenFGA/SpiceDB for relationship graph or OPA policy distribution; Cedar at local enforcement if needed | Centralized multi-service policy | I owns choice; consistency tokens and revocation semantics required |
| Observability | OTel Collector, Prometheus, Grafana, centralized logs/traces | Cross-service operations | Sensitive data redaction and retention |
| Deployment | OCI containers, orchestration platform (Kubernetes only if operational scale needs it) | Multi-node scheduling/rollout | Not a default for Profile S/M |
| Backup/recovery | DB PITR/replication, object-store versioning, index snapshots/rebuild, cross-region restore exercises | Service durability | Forget/revocation replay before restore becomes queryable |

**Required caveat:** This option has the highest development/operations and distributed consistency cost. It is not justified by the current repository's unquantified workload.

**必要限制：** 该方案具有最高研发、运维和分布式一致性成本。当前仓库尚无量化工作负载证明其必要性。

## 5. Comparison / 三套方案比较

| Dimension | Minimum | Balanced | High-scale |
|---|---|---|---|
| Development complexity | Low–medium | Medium–high | Very high |
| Operations complexity | Low | Medium–high | Very high |
| Consistency risk | Lowest if single DB boundary is proven | Higher due to projections/services | Highest due to distributed ownership |
| Performance potential | Moderate, local workload | High | Highest at scale, but only if operated well |
| Deployment cost | Lowest | Medium | Highest |
| Rust ecosystem maturity | High for core/storage; vector/inference vary | High–medium | Mixed across services and SDKs |
| Migration cost | Lowest starting point | Medium | High |
| Suitable phase | Profile S prototype | Profile M evolution | Profile L only |

## 6. Recommended investigation order / 建议研究顺序

1. Prove one transactional storage path and Forget race semantics.
2. Prove SQL outbox/worker recovery and idempotency.
3. Establish a lexical retrieval baseline and labeled quality dataset.
4. Add vector retrieval only if measured benefit warrants it.
5. Prove C/G/H Applied semantics and protocol conformance.
6. Complete I-owned identity/revocation/Forget mapping.
7. Run backup/restore and operational fault campaigns.
8. Only then approve ADRs and a baseline technology stack.

## 7. Conditional system recommendation / 条件性总体建议

For Profile S, Option A is the first experiment to run because it minimizes independent failure and transaction domains. This is not a formal selection. If the D/E/Storage fence/publication proof cannot be implemented safely in SQLite, the correct response is to evaluate PostgreSQL or revise the physical transaction boundary—not to weaken Forget semantics. Option B is the natural candidate if measured concurrency/remote access requires it. Option C remains unsupported absent Profile L evidence.
