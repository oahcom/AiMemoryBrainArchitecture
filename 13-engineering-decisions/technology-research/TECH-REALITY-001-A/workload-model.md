# Workload Model and Benchmark Plan / 工作负载模型与基准测试计划

- Task: TECH-REALITY-001-A | Owner A | Date: 2026-11-17
- Status: **ASSUMPTION ENVELOPES ONLY — NOT PROJECT REQUIREMENTS OR SLOs / 仅为假设区间，不是项目需求或 SLO**

## 1. Known vs unknown / 已知与未知

Known from TAB-001: local-first initial deployment direction is a planning driver; optional local inference has a 12–16 GB VRAM planning envelope. Host RAM, CPU, GPU model, disk type, corpus, number of users/Agents, write rate, retrieval QPS, retention and latency SLOs are not confirmed.

TAB-001 已知：本地优先是初始部署驱动；可选本地推理按 12–16 GB VRAM 进行规划。Host RAM、CPU、GPU 型号、磁盘类型、语料、用户/Agent 数、写入速率、检索 QPS、保留周期和延迟 SLO 均未确认。

All values below are **assumed test envelopes** to design representative experiments. They must be replaced with owner/user evidence before technology selection.

以下所有数值都是用于设计代表性实验的**假设测试区间**。正式技术选型前必须用 Owner/用户证据替换。

## 2. Profiles / 工作负载档位

| Dimension | Profile S — Personal / Single User | Profile M — Multi-Agent / Power User | Profile L — Multi-Tenant / Service |
|---|---|---|---|
| Users | 1 | 1–5 power users | 100–10,000 tenants/users |
| Agent instances | 1–5 | 5–50 | 100–10,000+ |
| Daily accepted Events | 100–1,000 | 1,000–100,000 | 100,000–10,000,000 |
| Canonical memories/claims | 10,000–100,000 | 100,000–1,000,000 | 10,000,000–1,000,000,000 |
| Average event payload | 1–8 KB text metadata; attachments separate | 1–16 KB; attachments separate | 1–32 KB; attachments separate |
| Concurrent read/write operations | 1–10 | 10–100 | 100–10,000 |
| Recall QPS | 1–10 | 10–100 | 100–10,000 |
| Vector count | 0 initially; test 10k–100k | 100k–1M | 10M–1B |
| Retention | User-configured; long-lived | Policy-defined, multi-year candidate | Tenant policy and legal retention |
| Workflow duration | milliseconds to 10 minutes | seconds to hours; occasional days | seconds to days |
| Interactive latency envelope | Measure p50/p95/p99; provisional local target 100–300 ms p95 for lexical recall only | Measure p50/p95/p99; target TBD | Service SLO TBD |
| Durability | Accepted Event must survive process restart under declared local durability | Same plus multi-process recovery | Multi-host durability and RPO/RTO required |
| RPO/RTO | Not specified; measure local restore | Not specified | Must be explicitly approved before deployment |

These ranges are not claims about the intended product. Profile L is a stress/architecture evolution envelope, not evidence that the project currently needs multi-billion-vector scale.

这些区间不是产品目标声明。Profile L 是压力测试和架构演进区间，不代表项目当前需要数十亿向量规模。

## 3. Data and storage sizing / 数据与存储估算

The benchmark harness should separately count:
- Raw Events and attachments/blobs.
- Canonical Memory revisions and Evidence references.
- Entity/Relation/Claim records and provenance edges.
- Outbox, work items, leases, receipts and audit.
- Lexical/vector index bytes and rebuild staging space.
- Cache/working-set resident memory.
- WAL growth, backups and restore staging.

A first-order disk estimate must use measured serialized row sizes and index amplification:
`DB bytes ≈ rows × measured average row bytes + indexes + WAL headroom`.
`Blob bytes ≈ retained payload bytes × retention generations`.
`Backup bytes ≈ DB snapshot + referenced blobs + restore staging + safety margin`.

Do not estimate disk solely from raw Event count; revisions, provenance, indexes and backups can dominate.

基准测试必须分别统计 Raw Event、附件 Blob、Canonical Memory 修订、Evidence 引用、Entity/Relation/Claim、Provenance Edge、Outbox/WorkItem/Lease/Receipt/Audit、索引字节、重建暂存空间、Cache、WAL、备份与恢复暂存。磁盘估算必须使用实测行大小和索引放大率，不能只按 Event 数量推算。

## 4. Required benchmark dimensions / 必测维度

### Storage and transaction
- Single-writer throughput and queue wait; concurrent readers under WAL.
- Transaction latency p50/p95/p99 and lock/busy rate.
- Event + outbox atomicity; canonical row + CanonicalCommitCursor atomicity.
- Producer admission vs Forget fence race in both serial orders.
- Dependency registration vs publication visibility race.
- Crash before/after commit, disk full, process kill, WAL checkpoint and restore.
- SQLite vs PostgreSQL on the same schema, hardware, concurrency and test data.

### Workflow and event processing
- Queue depth/age, lease acquisition, expiry, fencing, retries and DLQ.
- At-least-once duplicate delivery and idempotent business effects.
- Worker crash at every durable boundary.
- Replay after ForgetFenceGeneration advances.
- Backpressure and bounded memory under model/provider outage.

### Retrieval
- Labeled query set by language, scope, temporal status, epistemic status and entity.
- Recall@k, precision@k, MRR/nDCG, provenance correctness and unauthorized/forgotten leakage (target zero).
- FTS5 vs Tantivy indexing throughput, update/delete, query latency, disk and rebuild.
- Vector candidate recall/latency/memory/filter selectivity/update/delete/rebuild.
- Hybrid retrieval and reranking incremental quality gain vs latency/cost.

### Context and Agent integration
- Context plan/edit/commit latency and version conflict rate.
- Delivery-to-Applied lag, stale delivery rejection, offline reconnect and full snapshot fallback.
- Exact final inference request evidence and duplicate/lost ACK behavior.
- Token budget and context-window compatibility across at least two model/tokenizer profiles.

### Inference and resource use
- Model load time, warm/cold latency, tokens/sec, embedding throughput, peak/steady VRAM.
- KV cache by context length and concurrent sessions.
- CPU fallback, GPU OOM and restart behavior.
- GPU admission fairness between interactive and background compilation.

### Backup, restore and operations
- Backup duration, consistency, size and CPU/IO overhead.
- Restore duration, data integrity and cursor continuity.
- Restore with current Forget/revocation replay before serving.
- Index rebuild time and correctness after restore.
- Upgrade/migration from previous schema version and rollback/recovery.

## 5. Minimal benchmark plan / 最小基准计划

| Spike | Candidate | Minimum evidence | Owner |
|---|---|---|---|
| T1 Storage | SQLite WAL vs PostgreSQL | ACID/race/fault tests, contention and recovery | Storage + D/E |
| T1 Outbox | DB-backed worker vs NATS/Temporal/Restate | lease, replay, duplicate, backpressure, crash | E + Storage |
| T2 Lexical | FTS5 vs Tantivy | multilingual labeled corpus and update/delete/rebuild | F |
| T2 Vector | sqlite-vec/usearch/LanceDB/Qdrant (select at least two) | recall/latency/memory/filter/rebuild | F + Storage |
| T3 Protocol | JSON/HTTP vs CBOR/gRPC/local IPC | payload, compatibility, auth, reconnect and Applied conformance | H/C/G |
| T3 Authorization | embedded Cedar vs policy-service alternative | I-owned policy vectors, revocation and fail-closed tests | I |
| T4 Inference | ort/Candle/llama.cpp process | target GPU, exact model, VRAM/context and OOM behavior | C/E/A |
| T4 Recovery | chosen storage + blob + indexes | backup/restore, Forget suppression and migration | Storage/I/Release |

## 6. Benchmark reporting contract / 基准报告要求

Every result must record: exact source commit, Rust toolchain, OS/kernel, CPU, RAM, GPU/driver, storage device/filesystem, database settings, corpus generator and checksum, model/tokenizer/quantization, query mix, scope distribution, concurrency, cache state, warm-up, sample count, percentiles, confidence interval where applicable, correctness oracle, test logs and command line.

A vendor benchmark or published benchmark from another hardware profile is background evidence only. It is not a Brain performance result.

每份结果必须记录精确源码提交、Rust Toolchain、OS/Kernel、CPU/RAM/GPU/Driver、存储设备/文件系统、数据库配置、语料生成器和校验和、模型/Tokenizer/量化、查询分布、Scope 分布、并发、Cache 状态、预热、样本数、分位数、适用时的置信区间、正确性判定、测试日志和命令行。厂商或其他硬件上的公开基准只能作为背景证据，不是 Brain 性能结果。

## 7. Not yet measurable / 当前不可得出的结论

Until the target hardware and a representative Brain prototype exist, the project cannot responsibly select a database based on throughput, choose a vector engine based on recall/latency, claim a 12–16 GB GPU can host a specific model/concurrency, set SLO/RTO/RPO, or approve Profile L distributed deployment.

## 8. 完整中文版本 / Chinese Version

### 8.1 已知与未知

TAB-001 只给出本地优先初始方向，以及可选本地推理 12–16 GB VRAM 的规划区间。Host RAM、CPU、GPU 型号、磁盘、语料、用户/Agent 数、写入速率、Recall QPS、保留周期、延迟 SLO、RPO/RTO 均未确认。下列区间都是测试假设，不是产品要求。

### 8.2 三种测试档位

| 维度 | S 个人单用户 | M 多 Agent/Power User | L 多租户服务 |
|---|---|---|---|
| 用户 | 1 | 1–5 | 100–10,000 |
| Agent 实例 | 1–5 | 5–50 | 100–10,000+ |
| 每日 Accepted Event | 100–1,000 | 1,000–100,000 | 100,000–10,000,000 |
| Canonical Memory/Claim | 10,000–100,000 | 100,000–1,000,000 | 10,000,000–1,000,000,000 |
| 平均 Event Payload | 1–8 KB，附件另计 | 1–16 KB | 1–32 KB |
| 并发读写 | 1–10 | 10–100 | 100–10,000 |
| Recall QPS | 1–10 | 10–100 | 100–10,000 |
| 向量数 | 初期 0；测试 10k–100k | 100k–1M | 10M–1B |
| Workflow 时长 | 毫秒至 10 分钟 | 秒至小时，偶尔数天 | 秒至数天 |
| 延迟 | 测量 p50/p95/p99；词法 Recall 暂定本地 100–300ms p95 试验目标 | 测量，目标待定 | 服务 SLO 待定 |
| RPO/RTO | 未规定 | 未规定 | 部署前必须批准 |

这些数据是测试边界，不是产品承诺。Profile L 仅用于压力/演进测试，不代表当前需要十亿向量。

### 8.3 数据与容量测量

必须分别统计 Raw Event/附件、Canonical Revision/Evidence、Entity/Relation/Claim、Outbox/Lease/Receipt/Audit、词法/向量索引、重建暂存空间、Cache、WAL、备份和恢复暂存。磁盘估算应使用实测行大小、索引放大率和保留代数，不得只按 Event 数量推算。

### 8.4 必测项目

- Storage：单写者吞吐、读并发、事务 p50/p95/p99、锁等待、SQLite vs PostgreSQL、Event+Outbox 原子性、Canonical Cursor 原子性、Admission/Fence 双向竞争、Dependency/Publication 竞争、崩溃、磁盘满、WAL Checkpoint、恢复。
- Workflow：Queue Age、Lease、Fence、Retry、DLQ、At-least-once 重复、Worker 崩溃、Forget Generation 更新后的 Replay、Backpressure。
- Retrieval：多语言标注语料；Recall@k、Precision@k、MRR/nDCG、Provenance 正确性、未授权/已 Forget 泄露必须为零；FTS5/Tantivy 更新删除与重建；ANN 过滤与重建。
- Context/Agent：ContextVersion 冲突、Delivery 到 Applied 延迟、旧 Delivery 拒绝、离线重连、Final Request 证据。
- Inference：模型加载、冷/热延迟、Tokens/s、Embedding 吞吐、VRAM、KV Cache、CPU fallback、OOM。
- Backup/Recovery：备份/恢复耗时、完整性、Cursor 连续性、Forget/Revocation Replay、Index 重建和 Schema Upgrade。

### 8.5 最小基准计划

T1 比较 SQLite/PostgreSQL 和 DB Worker/NATS/Temporal/Restate；T2 比较 FTS5/Tantivy，再按需比较 Vector；T3 比较 JSON/HTTP、IPC、CBOR/gRPC 和 Cedar；T4 比较 ort/Candle/llama.cpp 及完整 DB+Blob+Index 恢复。每项必须记录精确 Commit、Rust Toolchain、硬件、OS、DB 配置、语料校验、模型、并发、Cache 状态、样本数、分位数、正确性 Oracle 和日志。

没有目标硬件与 Brain 原型前，不能负责任地选择数据库吞吐、向量引擎 Recall、特定模型 VRAM、生产 SLO/RTO/RPO 或 Profile L 分布式部署。
