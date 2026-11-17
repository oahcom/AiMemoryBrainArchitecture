# Deployment Topology Comparison / 部署拓扑比较

- Task: TECH-REALITY-001-A | Owner A | Date: 2026-11-17
- Status: **COMPARISON ONLY — NO TOPOLOGY SELECTED / 仅比较，不构成拓扑选型**

## 1. Scoring method / 评分方法

Scores are ordinal engineering estimates, not measurements. For complexity, transaction difficulty, operations, recovery, development, testing and lock-in: **1 = low/easy, 5 = high/hard**. For scale potential and Rust fit: **1 = low, 5 = high**. Scores must be revised after representative workload and prototypes. No numeric performance is inferred.

评分是工程估计，不是实测数据。复杂度、事务难度、运维、恢复、开发、测试和锁定风险维度中，**1 = 低/容易，5 = 高/困难**；扩展潜力与 Rust 适配度中，**1 = 低，5 = 高**。应在代表性工作负载和原型测试后修订，不推断任何数值性能。

## 2. Option A — Local-first modular monolith / 本地优先模块化单体

**Shape**
- One Rust application process with logical modules/crates.
- One local transactional database authority (SQLite candidate).
- Content-addressed blob directory, rebuildable lexical/vector indexes, in-process bounded cache.
- DB outbox and bounded background workers.
- Optional isolated inference process; Agent Adapter embedded in or adjacent to Agent runtime.

**Strengths**
- One process and one SQL transaction domain simplify canonical commit, event acceptance, idempotency, cursors and Forget linearization.
- Few operational dependencies; local install and offline behavior are tractable.
- Rust module interfaces and conformance tests can preserve logical separation without network hops.
- Indexes can be rebuilt from canonical data.

**Risks / limits**
- SQLite has a single-writer constraint; WAL is single-host only and can suffer checkpoint starvation.
- One process can create failure coupling unless worker pools, bounded queues, cancellation and panic boundaries are deliberate.
- CPU/GPU inference must not block Tokio executor or storage path.
- A local filesystem/blob directory must be backed up consistently with DB metadata.

## 3. Option B — Modular monolith + selected external services / 模块化单体 + 选择性外部服务

**Shape**
- Rust Brain core and transactional database (likely PostgreSQL if multi-writer/remote access is required).
- External vector service (e.g. Qdrant) only if benchmark justifies it.
- Optional external workflow/queue (Temporal/Restate/NATS) only if durable task scale and isolation justify it.
- External LLM providers or isolated inference worker.
- OTel Collector/Prometheus stack in non-minimal deployment.

**Strengths**
- Separates heavy inference, high-throughput indexing, remote access or long-lived workflows.
- PostgreSQL provides mature multi-client concurrency and operational tooling.
- Dedicated vector services offer HNSW, filtering, sharding and operational capabilities.

**Risks / limits**
- Every external service creates network failure, credentials, version compatibility, backup and upgrade work.
- Canonical SQL commit and vector/index publication are no longer one transaction; outbox, watermarks, suppression and repair become mandatory.
- Workflow history does not automatically transact with canonical DB.
- Forget completion must account for each independent store and service.

## 4. Option C — Distributed services / 分布式服务架构

**Shape**
- Independently deployed services for ingress, compiler, canonical memory, retrieval, context, protocol, authorization and orchestration.
- Multiple databases and index services, durable broker, distributed workflow coordinator, independent Agent gateway.
- Replication, sharding, service discovery, distributed tracing and rollout coordination.

**Strengths**
- Independent scaling and fault domains where there are real, sustained workloads.
- Supports multi-host and multi-tenant deployment patterns with separate operational ownership.
- Allows independently upgraded components where contracts are stable.

**Risks / limits**
- Cross-service transaction and Forget linearization become distributed protocols.
- Strongly increases the number of partial-failure, retry, duplicate, stale-cache, replay and split-brain cases.
- More deployment, security, observability, schema compatibility and operator requirements.
- Current repository has no measured scale or deployment evidence that requires this topology.

## 5. Comparative scorecard / 量化比较

| Dimension (1 low/easy, 5 high/hard unless stated) | Option A | Option B | Option C |
|---|---:|---:|---:|
| Consistency complexity | 2 | 4 | 5 |
| Transaction implementation difficulty | 2–3 | 4 | 5 |
| Deployment complexity | 1–2 | 3–4 | 5 |
| Failure recovery difficulty | 2–3 | 4 | 5 |
| Development cost | 2–3 | 4 | 5 |
| Operations cost | 1–2 | 3–4 | 5 |
| Scale potential (1 low, 5 high) | 2–3 | 4 | 5 |
| Rust ecosystem fit (1 low, 5 high) | 5 | 4 | 3–4 |
| Test difficulty | 2–3 | 4 | 5 |
| Technology lock-in risk | 2 | 3–4 | 4–5 |

The score ranges reflect unresolved details (for example, SQLite versus PostgreSQL in A; which external services in B). They are not a ranking of product quality.

## 6. Fit by workload profile / 工作负载适配

| Profile | Option A | Option B | Option C |
|---|---|---|---|
| S — Personal/single user | Plausible first prototype if single-writer envelope and local durability pass | Usually over-complex unless remote Agent or vector service is a demonstrated requirement | Not justified by present evidence |
| M — Power user/multi-Agent | Plausible with measured DB write serialization, bounded queues and isolated inference; PostgreSQL may be required | Candidate if concurrency, remote access or workflow scale exceeds A | Only if distinct services/fault domains are proven necessary |
| L — Multi-tenant/service | SQLite local topology not sufficient for multi-host; PostgreSQL plus selected services likely candidate | Strong candidate baseline | Candidate only with measured scale/independent ownership and distributed transaction plan |

## 7. Explicit topology triggers / 明确拆分触发条件

Move from A toward B only when at least one measurable condition is true:
1. Sustained concurrent writes exceed the tested SQLite single-writer envelope or create unacceptable queue age/tail latency.
2. Brain must be accessed by multiple hosts/processes over a network and local single-host SQLite semantics no longer fit.
3. GPU model loading/OOM/stalls measurably threaten core ingress/recovery despite bounded in-process isolation.
4. Index rebuild or vector workload materially degrades interactive Recall and independent scaling is justified.
5. Durable workflows require timers/retries/history across process restarts and are too complex or unreliable for DB workers.
6. Security boundary requires an independently isolated network-facing gateway.

Move from B toward C only when independent scaling/fault-domain requirements and operational ownership are measured, not merely because logical Owner modules exist.

从 A 向 B 演进，必须至少满足一项可测条件：SQLite 单写者能力被持续并发写入超过；需要多主机访问；GPU 推理故障影响核心路径；索引重建影响 Recall；长期 Workflow 需要独立持久执行；或安全边界要求独立 Gateway。由 B 向 C 演进必须有独立扩缩容、故障域和运维责任的实测证据，不能仅因为逻辑 Owner 模块存在。

## 8. Provisional disposition / 暂定意见

Option A is the lowest-cost hypothesis to prototype for Profile S, not a selected production topology. Option B is a conditional path for multi-writer, remote and heavy retrieval/workflow requirements. Option C is not supported by current workload evidence. All three remain comparison options until ADRs and prototypes close the transaction, Forget, recovery and resource gates.

Option A 是 Profile S 最低成本的原型假设，不是正式生产拓扑选型。Option B 是面向多写者、远程访问和重型检索/工作流需求的条件路径。当前没有工作负载证据支持 Option C。三者都必须等待 ADR 和原型关闭事务、Forget、恢复与资源门禁。


## 9. Terminology and current Storage architecture decision / 术语与 Storage 当前架构决策

**Do not confuse two independent Option A/B/C labels.**

- This document's Option A/B/C are *deployment topologies*: local-first modular monolith; modular monolith plus selected services; distributed services.
- Storage ADR's Option A/B/C are *serialization topologies*: one logical serializable transaction domain per Canonical Memory authority; separate D/Storage services plus durable linearizable coordinator; check-then-write (rejected).

The current Storage ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` adds a 2026-11-17 decision selecting **Storage-ADR Option A** as the normative v1 logical serialization profile. It does not select this document's deployment Option A, nor a physical DB engine. A single logical transaction domain could be deployed inside a modular monolith or as a shared transaction substrate with separately deployed processes, subject to actual engine/connection and operator proof.

The current PostgreSQL 18.7 dossier Blob `0aabf66848dc97deee028c571183c0d7204008c0` provides meaningful but bounded engine-level capability evidence. It makes PostgreSQL 18.7 the leading qualified JF-10 prepared-XID capability candidate; it does not close the D/I/COC application bridge or production deployment. SQLite remains a local prototype candidate for operations within one same-host transaction domain, but it is not qualified by the cited evidence for external I sequencer prepared-XID recovery.

**不要混淆两组独立的 Option A/B/C 命名。**

- 本文件 Option A/B/C 指**部署拓扑**：本地优先模块化单体；模块化单体 + 选择性外部服务；分布式服务。
- Storage ADR 的 Option A/B/C 指**序列化拓扑**：每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain；D/Storage 分服务 + 持久化线性协调器；Check-then-write（已拒绝）。

当前 Storage ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` 的 2026-11-17 补充条款选择 **Storage-ADR Option A** 作为 v1 规范逻辑序列化档案。它既不选择本文件的部署 Option A，也不选择物理数据库。一个逻辑事务域可部署在模块化单体中，也可能通过共享事务底座由不同进程访问，但必须有真实引擎/连接与运维证据。

PostgreSQL 18.7 档案 Blob `0aabf66848dc97deee028c571183c0d7204008c0` 提供有意义但有限的引擎能力证据，使 PostgreSQL 18.7 成为 JF-10 Prepared-XID 能力资格的领先候选；它没有关闭 D/I/COC 应用桥接或生产部署。SQLite 仍可作为同一主机事务域内操作的本地原型候选，但现有证据未证明其支持外部 I Sequencer 的 Prepared-XID 恢复。

## 10. 完整中文版本 / Chinese Version

### 10.1 评分说明

本文件评分是序数工程估计，不是性能实测。复杂度、事务难度、运维、恢复、研发、测试和技术锁定风险：1 低/容易，5 高/困难；扩展潜力与 Rust 适配度：1 低，5 高。所有评分必须在代表性负载和原型后修订。

### 10.2 方案 A：本地优先模块化单体

- 单一 Rust 主进程和逻辑模块/Crate。
- 一个本地事务权威数据库（SQLite 是候选）。
- 内容寻址 Blob 目录、可重建词法/向量索引、进程内有界 Cache。
- DB Outbox 和后台 Worker。
- 可选隔离推理进程，Agent Adapter 与 Agent Runtime 相邻或嵌入。

优势：Canonical Commit、Event Acceptance、幂等、Cursor 和 Forget 线性化更容易落在一个事务域；部署依赖少；离线安装简单；可通过模块 API 保留逻辑隔离。

风险：SQLite 只有一个写者，WAL 仅同一主机；进程内故障可能耦合；推理不得阻塞 Tokio 或 Storage；DB 与 Blob 必须一致备份。

### 10.3 方案 B：模块化单体 + 选择性外部服务

- Rust Brain Core + PostgreSQL（需要多写者/远程访问时）。
- 按基准引入 Qdrant 等向量服务。
- 仅在 Durable Workflow/Queue 有真实需要时引入 Temporal、Restate 或 NATS。
- 外部 LLM Provider 或隔离推理 Worker。
- 非最小部署可增加 OTel Collector/Prometheus。

优势：可隔离重推理、高吞吐索引、远程访问和长任务；PostgreSQL 有成熟多客户端并发与运维工具；专用向量服务提供 HNSW、过滤、分片能力。

风险：每个服务增加网络故障、凭证、版本、备份、升级成本；Canonical SQL 与索引发布不再一个事务；Forget 必须覆盖独立存储；Workflow History 不与 Canonical DB 自动事务化。

### 10.4 方案 C：分布式服务

把 Ingress、Compiler、Canonical Memory、Retrieval、Context、Protocol、Authorization 和 Orchestration 拆成独立服务，使用多个数据库/索引、Broker、Durable Coordinator、复制/分片和分布式追踪。

优势：有真实持续负载时可独立扩缩容和故障隔离，支持多租户、多节点和独立团队升级。

风险：跨服务事务和 Forget 变成分布式协议；部分失败、重试、重复、缓存过期、Replay、Split-brain 数量显著增加；部署、密钥、Schema 兼容、监控与运维成本最高。当前没有实测规模证明需要此方案。

### 10.5 比较评分

| 维度（除注明外 1 低/容易，5 高/困难） | A | B | C |
|---|---:|---:|---:|
| 一致性复杂度 | 2 | 4 | 5 |
| 事务实现难度 | 2–3 | 4 | 5 |
| 部署复杂度 | 1–2 | 3–4 | 5 |
| 故障恢复难度 | 2–3 | 4 | 5 |
| 研发成本 | 2–3 | 4 | 5 |
| 运维成本 | 1–2 | 3–4 | 5 |
| 扩展潜力（1 低，5 高） | 2–3 | 4 | 5 |
| Rust 生态适配（1 低，5 高） | 5 | 4 | 3–4 |
| 测试难度 | 2–3 | 4 | 5 |
| 技术锁定风险 | 2 | 3–4 | 4–5 |

### 10.6 负载档位适配

- Profile S：A 是合理原型假设；只有 SQLite 单写者和本地持久性通过测试时才成立。B 通常过度复杂，除非确实需要远程 Agent 或向量服务。C 无证据支持。
- Profile M：A 仍可能成立，但必须测量 DB 写入串行化、队列和推理隔离；多写者/远程访问可能推动 B。C 需要明确故障域证据。
- Profile L：SQLite 本地拓扑不足以支持多主机；PostgreSQL + 选择性服务是候选。C 只有在独立扩缩容、运维所有权和规模证据成立时才考虑。

### 10.7 拆分触发条件

从部署 A 走向 B，必须出现可测条件：SQLite 写入排队/尾延迟超过目标；多主机网络访问；GPU 故障影响核心路径；索引重建影响 Recall；长任务需要持久 Timer/Retry；或安全边界要求独立 Gateway。从 B 走向 C，必须证明独立扩缩容、故障域和运维责任的必要性。

### 10.8 术语特别说明

Storage ADR 的 Option A/B/C 是**序列化拓扑**，本文件 Option A/B/C 是**部署拓扑**，不能混淆。Storage ADR 当前补充条款选择“每个 Canonical Memory Authority 一个逻辑 Serializable Transaction Domain”作为 v1 规范性序列化档案；这不等于选择本文件的部署方案 A，也不等于选定 SQLite 或 PostgreSQL。PostgreSQL 18.7 是 JF-10 Prepared-XID 能力的领先资格候选；SQLite 只保留为单写者、同主机事务组的本地原型候选。
