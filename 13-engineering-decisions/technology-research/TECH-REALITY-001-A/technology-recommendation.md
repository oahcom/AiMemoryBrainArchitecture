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


## 8. Current Storage architecture and PostgreSQL qualification update / Storage 当前架构与 PostgreSQL 资格更新

The Storage branch now contains a 2026-11-17 ADR addendum (Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`) selecting one logical serializable transaction domain per Canonical Memory authority as the normative v1 **serialization architecture profile**. This decision preserves D, Storage, I and COC as separate semantic/consistency authorities. It does not select the deployment topology in this document and does not select a production DB.

The PostgreSQL 18.7 prepared-XID dossier (Blob `0aabf66848dc97deee028c571183c0d7204008c0`) reports PASS for bounded engine-level CI subtests: prepared-XID/lock persistence through hard restart and same-XID commit/rollback; two-node synchronous WAL replay and promotion; physical backup/restore; coordinator ACK-gap crash; TCP ACK loss; standby-unavailable UNKNOWN/private behavior; and WAL PITR. Gate A remains PARTIAL PASS / OPEN. Gate B's amended COC protocol requires focused exact-owner re-review. Gate C is deferred to engineering-phase distributed integration/fault injection. JF-10 runtime P0 remains OPEN; production activation is NOT AUTHORIZED; multi-PolicyDomain atomicity remains BLOCKED.

**Updated conditional recommendation:**
- Keep Storage-ADR Option A (one logical serializable transaction domain per Canonical Memory authority) as the current normative v1 architecture profile, subject to exact current Owner reviews.
- Treat PostgreSQL 18.7 as the leading qualified engine-capability candidate for the JF-10 prepared-XID bridge, not an approved production Canonical Authority database.
- Retain SQLite WAL only as a limited local prototype candidate for transaction groups that fit its single-writer, same-host model; do not claim it meets JF-10 prepared-XID recovery across an external I sequencer.
- Do not approve any DB product or production topology until the actual adapter, D/I/COC integration, authoritative read path, failover/fencing, backup/restore and operator/runbook evidence pass.

Storage 分支现有 2026-11-17 ADR 补充条款（Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`）选择每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain，作为 v1 规范性**序列化架构档案**。该决策保持 D、Storage、I、COC 的语义/一致性权威独立，不选择本文件中的部署拓扑，也不选择生产数据库。

PostgreSQL 18.7 Prepared-XID 档案（Blob `0aabf66848dc97deee028c571183c0d7204008c0`）报告了有限的引擎级 CI 子测试 PASS：Prepared-XID/锁跨硬重启持久化及同 XID Commit/Rollback；双节点同步 WAL Replay 与 Promotion；物理备份恢复；协调器 ACK 间隙崩溃；TCP ACK 丢失；同步备机不可用时 UNKNOWN/Private；WAL PITR。Gate A 仍 PARTIAL PASS / OPEN。Gate B 修订 COC 协议需要聚焦精确 Owner 复审。Gate C 延后到工程阶段进行分布式集成/故障注入。JF-10 runtime P0 仍 OPEN；禁止生产激活；多 PolicyDomain 原子性仍 BLOCKED。

**更新后的条件性建议：**
- 将 Storage-ADR Option A（每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain）保留为当前 v1 规范性架构档案，但需当前 Owner 精确复审。
- 将 PostgreSQL 18.7 视为 JF-10 Prepared-XID 桥接的领先引擎能力候选，不是已批准的生产 Canonical Authority 数据库。
- SQLite WAL 仅保留为适用于单写者、同主机事务组的有限本地原型候选；不得声称其满足跨外部 I Sequencer 的 JF-10 Prepared-XID 恢复。
- 在真实 Adapter、D/I/COC 集成、权威读路径、故障切换/隔离、备份恢复和 Operator/Runbook 证据通过前，不批准数据库产品或生产拓扑。

## 9. 完整中文版本 / Chinese Version

### 9.1 决策边界

本文件只给出系统级候选方案，不批准 ADR、不冻结依赖、不选择正式部署拓扑，也不覆盖 B–I/Storage 的领域决策。所有建议必须经过 Owner 审查和原型验证。

### 9.2 方案一：最小可行技术栈（Profile S）

- Core：Rust + Tokio。
- Storage：SQLite + WAL，通过 SQLx 或 rusqlite（二选一），Blob 使用内容寻址本地文件系统 + SQL Metadata。
- Event：SQL Transactional Outbox + 有界 DB Worker。
- Workflow：DB Work Table、Lease、Fence、Retry；只有 DB Worker 不足时再评估 Temporal/Restate。
- Search：结构化 SQL + FTS5；FTS5 不足再评估 Tantivy。
- Vector：首个纵向切片不引入，只有检索评估证明收益后才选一个。
- Cache：Moka 可选且有界；在失效契约证明前不缓存更安全。
- Agent：Brain 自有 Provider Port 和 Adapter；Rig 仅作为 Agent 侧可选库。
- Protocol：H 定义版本化 JSON + 认证 HTTP/本地 IPC 候选。
- Security：I 拥有身份/权限/撤销；可评估嵌入式 Cedar。
- Observability：Rust tracing、结构化脱敏日志、基础 Metrics。
- Deployment：单一 Rust 进程，可选推理进程；systemd/OCI，不要求 Kubernetes。
- Backup：SQLite Backup API/一致快照 + Blob Manifest/Checksum + 隔离恢复 + Forget Replay。

限制：SQLite WAL 只有单写者、同主机。只有 D/E/Storage 关键竞争能在同一事务/锁模型中线性化，且 Profile S 实测通过时才可行。SQLite 目前没有跨外部 I Sequencer 的 JF-10 Prepared-XID 恢复证明。

### 9.3 方案二：平衡型技术栈（Profile M）

- Rust + Tokio 模块化单体；按需要拆独立 Worker。
- PostgreSQL 作为多写者/远程访问时的事务权威。
- 内容寻址 Blob + Manifest。
- PostgreSQL Outbox + Worker；独立 Consumer/Replay/复制需求成立时再评估 NATS。
- 长任务先用 SQL Durable Jobs；只有复杂 Timer/Retry/独立 Worker 有实测价值才选择 Temporal 或 Restate。
- PostgreSQL 结构过滤 + FTS5（SQLite 本地配置）或 Tantivy。
- pgvector 或 Qdrant 作为派生投影（二选一）；LanceDB 需 Beta 风险评估。
- Moka 本地 Cache；Redis 只有跨进程共享缓存有实测价值才引入。
- BMCP 版本化协议，HTTP/JSON 初始候选；gRPC 只有流式/SDK 需要时。
- Cedar 嵌入式候选；OpenFGA/SpiceDB 只有关系授权成为独立服务需求时。
- tracing + OTel Collector，Prometheus/Grafana 可选。
- Brain Core + 可选 Compiler/Index/Inference Worker；OCI/systemd。
- PostgreSQL PITR/备份 + Blob Snapshot + Index Rebuild + Forget/Revocation Restore Gate。

限制：PostgreSQL 多写者能力不解决跨服务原子性、Blob 原子性、外部 Provider 或 Forget 目标完整性。

### 9.4 方案三：高扩展型技术栈（Profile L）

- Rust 独立服务，严格 Contract 和独立 Owner。
- PostgreSQL 按权威域持久化；需要时 Partition/Replica。
- Object Storage 保存不可变 Evidence/Blob。
- Kafka/Redpanda 或 NATS JetStream 按 Partition、Replay、Consumer 需求选择。
- Temporal 或 Restate 承担 Durable Workflow。
- Tantivy/OpenSearch/Qdrant 作为独立派生索引，避免多个系统重复承担同一检索职责。
- Qdrant Cluster 仅在语料、QPS、可用性需要时采用。
- Moka 本地 Cache；Redis 仅在共享热点有实测收益时。
- Agent Gateway + 多语言 SDK；BMCP over gRPC/HTTP2 或等效协议。
- OpenFGA/SpiceDB 用于关系授权，OPA 用于策略分发，Cedar 可用于本地 Enforcement；由 I 决定。
- OTel Collector、Prometheus、Grafana、集中式 Trace/Log。
- OCI 容器；Kubernetes 只有多节点运维确实需要时采用。
- DB PITR/复制、Object Versioning、Index Snapshot/Rebuild 和跨区域恢复演练。

限制：研发、运维和分布式一致性成本最高，当前没有工作负载证据证明必要。

### 9.5 三套方案比较

| 维度 | 最小型 | 平衡型 | 高扩展型 |
|---|---|---|---|
| 研发复杂度 | 低–中 | 中–高 | 很高 |
| 运维复杂度 | 低 | 中–高 | 很高 |
| 一致性风险 | 单 DB 边界证明后最低 | 外部服务和投影增多 | 分布式权威最多，最高 |
| 性能潜力 | 本地中等 | 高 | 大规模潜力高 |
| 部署成本 | 最低 | 中 | 最高 |
| Rust 生态成熟度 | Core/Storage 高，向量/推理各异 | 高–中 | 各服务/SDK 混合 |
| 迁移成本 | 初始最低 | 中 | 高 |
| 适用阶段 | Profile S 原型 | Profile M 演进 | Profile L 有证据后 |

### 9.6 条件性建议

Profile S 应先试验本地模块化单体，因为它最少独立故障域和事务域；这不是正式选型。若 D/E/Storage Fence/Publication 无法在 SQLite 安全实现，应评估 PostgreSQL 或调整物理事务边界，不得削弱 Forget。当前 Storage ADR 已选择每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain 作为 v1 序列化档案；PostgreSQL 18.7 是 JF-10 Prepared-XID 能力的领先资格候选，但不是生产 DB 批准。Profile M 可在多写者/远程访问被测量证明后选择 B；Profile L 无当前证据支持。

## 6. Current-source constraints on all candidate stacks / 当前源对所有候选技术栈的约束

No stack recommendation may assume that a workflow engine, broker, SQL database or crypto library implements the Brain-owned D/E/I/Storage protocol. The current Phase 3.8 sequence is a cross-owner proposal: E durable ingress; D registration and complete lineage; Storage hidden participant; D publication admission; I single-use authorization; Storage final serializable atomic visibility/outcome/receipt/outbox; D/I closeout after the same Storage outcome. UNKNOWN remains private and barrier-held.

Storage ADR selects Option A only for L1 logical serialization per Canonical Memory authority. L4 physical engine/deployment is OPEN; therefore neither SQLite nor PostgreSQL is approved by this ADR. H candidate schema CI and I crypto candidate are not production evidence. C/G/H Applied remains not frozen, not tested and not implementation-verified. Restate Server license must be evaluated as BSL 1.1 with Additional Use Grant separately from the MIT Rust SDK.

**中文：** 所有候选栈均不得假设 Workflow Engine、Broker、SQL 数据库或 Crypto 库已经实现 Brain 自有的 D/E/I/Storage 协议。当前 Phase 3.8 顺序仍是跨 Owner 提案。Storage ADR 仅为每个 Canonical Memory Authority 的 L1 逻辑序列化选择 Option A；L4 物理引擎/部署 OPEN，因此该 ADR 没有批准 SQLite 或 PostgreSQL。H Schema CI 和 I Crypto 候选不是生产证据；C/G/H Applied 仍未冻结、未测试、未验证实现。Restate Server BSL 1.1 与 MIT Rust SDK 必须分开评估。

Full status: [OWNER-REMEDIATION-001](owner-remediation/OWNER-REMEDIATION-001.md).
