# AI 大脑架构突破研究总报告（中文）

- Research ID: ABR-SESSION-0-2026-11-18
- Status: **CANDIDATE / TO_VALIDATE；非架构批准**
- Research branch: `research/architecture-breakthrough-session-0-2026-11-18`
- Baseline: `main@b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Date: 2026-11-18

## 1. 执行摘要

本轮研究不是另起炉灶，而是寻找能减少自研机制、减少 Owner 协调、同时不削弱安全不变量的最小替代路径。当前证据支持三个方向：

1. **Forget：先建立一个跨 D/E/I/Storage 的小型可执行状态模型，而不是继续扩展文字合同。** TLA+ 适合并发状态转移、崩溃/重放和安全/活性性质；Alloy 适合检查目标、来源、派生物、Owner 与 Scope 之间的关系约束。建议先 TLA+，Alloy 只在闭世界库存/血缘关系出现反例时补充。模型通过不等于实现通过。
2. **Runtime：统一资源管理，不统一领域权威。** F 的请求调度、候选预算、缓存/Working Set 容量与 G 的 Context token/byte budget 确实可共享一个分层资源账本、准入/预留/回收机制；但 D Canonical Memory、F Retrieval/Activation、G ContextVersion、I Permission/Forget 和 H Applied 不能合并成一个“万能 Memory Manager”。
3. **Compiler：引入窄的、版本化的 Memory IR，而不是再造一套通用编译器平台。** IR 应是编译阶段间稳定的类型化数据契约，承载来源、证据角色、Scope、时间/认知限定、转换版本和派生血缘。LLM 只产生候选 IR；确定性验证与 D Canonical Commit 保持独立。

**当前不能声称新架构已优于现架构。** 没有同工作负载下的复杂度、延迟、资源、正确性对照数据。当前能成立的是：有若干可验证的简化假设，以及明确的最小实验路径。

## 2. 研究独立性与证据边界

本会话作为 Session 0 协调人，直接读取 GitHub 当前 main、Issue #43、指定 PR 元数据，以及 D/E/F/G/I/Storage/C/H 当前 Owner 分支中的相关文件；同时查阅 TLA+/Alloy、PostgreSQL、SQLite、Temporal、Kafka、Lucene、Tantivy、Qdrant、Redis、Linux cgroup 和 OpenTelemetry 的公开技术资料。

本研究与 A–I Owner 研究会话共享同一仓库及 Issue #43 中记录的历史证据，因此**不是组织意义上的盲审**。但本报告对关键 Owner 工件做了当前分支 HEAD 与 Blob SHA 读回；Issue #43 中的历史摘要只用于定位，不替代实时来源。没有执行 TLA+/Alloy 模型检查，没有运行基准测试，没有部署数据库/服务，也没有做生产故障演练。外部资料只证明成熟产品机制，不证明本项目集成正确。

### 当前基线与 Owner 来源

| 来源 | 当前分支 HEAD | 本轮读取的文件 / Blob SHA |
|---|---|---|
| main | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | `01-system-architecture/system-overview.md` / `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256` |
| D | `session-d-memory-brain-2026-11-16` @ `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | Forget contract / `1f0391bc49d007c44ec74165bd33d37412cc7990`; publication gate / `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |
| E | `session-e-memory-compiler-2026-11-16` @ `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | producer admission / `e59f517fff161ab882aa0ddc4a5bda513964ae1a`; derived registration / `00e37ba56596e710513c8d0568acd79141d9101b`; evidence/provenance / `38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963` |
| F | `session-f-memory-runtime` @ `1908ce4d233b20f7cafd00cb679affd01bd15174` | runtime overview / `b7a948f014c3ad882a35a18bfc8ce025b26ab85a`; scheduling / `ca35d8cddd012c1ff067328ee22177f57c40ae36`; working set / `a934491950c876701e8ac592a0e6aaea983b44e3`; activation / `b7f5d85468f5262e472769a1991b812ac4a64f5b` |
| G | `session-g-memory-context` @ `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | context reconciliation / `87063aceebed1c30b7840045ada8e3f348732688`; context budget and architecture were also read at this HEAD |
| I | `session-i-security-governance-2026-11-16` @ `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | global inventory / `9100061fa986fb6676656169de3fcf9fc1c72664`; retention/erasure / `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` @ `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | COC design v3.2.3 / `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` |
| C / H | C @ `71047cdb51139ca4080ac67f451e38a48698859d`; H @ `0d36324457e39bd50ad56ae902d477c4ea765b61` | branch heads verified; Issue #43 records the exact Applied / recovery gaps requiring follow-up |

注意：Issue #43 中 G 的历史 HEAD 记录为 `3367438...`，但当前 GitHub branch listing 返回 `763b3d...`。本研究采用实时分支 HEAD，而不是沿用 Issue 中旧值。

### 指定 PR 快照

截至本轮读取：#46、#49、#55、#69、#70、#71 均 Open / Draft / Unmerged。#71 base 是 Storage 分支，不是 main。PR 状态只表示提交状态，不代表内容批准。

## 3. Workstream A — Forget Model Checking

### 3.1 问题重新定义

当前核心不是“缺少更多 Forget 状态名称”，而是多个权威的局部状态是否能组合成一个可线性化、可恢复、不会复活的全局过程：

- D：ForgetOperation、ForgetFence、ProducerWork registration/barrier、依赖库存与最终发布语义；
- E：编译 work/attempt/lease/retry/DLQ/replay、派生物 staging 和依赖注册调用；
- I：PermissionEpoch、全局 Producer Domain Inventory、目标库存封存、全局完成标准与例外；
- Storage：物理事务、Prepared XID、Visibility Pointer、COC、恢复 cutoff；
- F/G/H：索引/缓存/Working Set、Context 快照/Delta、Adapter 应用与离线重连。

必须保持三个不同的结果：逻辑抑制、异步清理、物理擦除。D 的 CanonicalSuppressionComplete 不等于 I 的 Global Forget Completed。

### 3.2 最小形式模型

建议先把模型缩成一个 BrainAuthority、一个目标及其 lineage、两个 producer、两个派生物、一个 index、一个 Context、一个 Adapter、两个并发操作（Forget 与 Publish）。状态只保留：

- `fenceGeneration`、`permissionEpoch`；
- `producerRegistered`、`producerTerminal`；
- `dependencyRegistered`；
- `artifactPrivate/Visible`；
- `targetSuppressed`；
- `inventorySealed`、`barrierClosed`；
- `restoreGeneration` 与 `adapterAckGeneration`。

先检查安全性质，再检查活性。核心不变量：

1. **NoPostFenceVisibility**：受当前 fence 覆盖的目标或 lineage 不得变为可见。
2. **RegisterBeforePublish**：每个可见派生物必须存在稳定 ProducerWork 注册与完整依赖注册。
3. **BarrierSoundness**：BarrierClosed 只能在 fence high-water 内所有 work 都有可验证终结结果、无未解决 lease/DLQ/replay 后成立。
4. **UnknownIsNotSuccess**：超时、丢失 ACK、状态未知不得转为成功、终结或清理完成。
5. **RestoreCannotRollbackControl**：恢复后必须先应用当前控制高水位，再开放读写；旧快照不能降低 fence/permission 控制代次。
6. **NoCrossEpochCompare**：PermissionEpoch、ForgetFenceGeneration、ProducerRegistrationHighWater、CanonicalCommitCursor、IndexWatermark、ContextVersion 不得跨命名空间比较。

反例搜索必须覆盖：注册与 fence 竞态、依赖注册部分成功、可见性提交后 ACK 丢失、旧 Worker lease 过期后继续执行、DLQ 重放、索引 rebuild、Adapter 离线后旧 Context 重连、Restore 回滚、Permission revocation 与 final commit 竞态。

**当前 TLA+ 文件只是第一阶段骨架，不是上述完整模型：** 它目前只抽象单一目标集、Producer 注册、Fence high-water 捕获、依赖登记、可见性抑制、终结和控制高水位恢复覆盖；尚未编码 ACK 丢失、Lease/Attempt、DLQ/Replay、PermissionEpoch、I 全局库存、索引/Context/Adapter 状态，也尚未运行 TLC。上述场景是下一轮扩展清单，不是本次已验证的覆盖范围。

### 3.3 工具判断

- **TLA+/TLC：CANDIDATE，优先。** 适合并发状态机与时序性质；可直接检查安全与活性，输出反例轨迹。模型需限制有限状态空间。
- **Apalache：CANDIDATE，备选。** 符号检查适合有限数据结构下的有界安全验证；其工具文档仍提示实验性质，不把它作为唯一验证器。
- **Alloy 6：CANDIDATE，补充。** 更适合 producer/target/lineage/Scope/authority 的关系完整性、身份唯一性与小范围时序反例；有界范围内无反例不代表无界证明。
- **PostgreSQL：CANDIDATE 物理实现机制。** Serializable 能检测无法对应任何串行执行的并发事务并中止其中一个；但它只覆盖同一数据库事务边界内的读写依赖，不能自动原子化外部 COC、Adapter、向量库或云服务。

### 3.4 初步结论

**CANDIDATE：TLA+ 作为主模型，Alloy 作为关系约束补充。** 暂不建议先引入通用分布式事务框架或新的全局协调服务。先回答：D 的 Producer Registration、Fence Install、Dependency Registration、Visibility Commit 能否落入一个物理事务/单一线性化锚点？若不能，才比较可恢复 Prepare/Commit 与 COC 的复杂性。

## 4. Workstream B — Memory Operating System

### 4.1 现有边界与重叠

F 当前已经拥有 Retrieval routing、Activation recommendation、Working Set/cache、Runtime scheduling、Admission、Cancellation、per-request candidate/evidence/latency budgets。G 拥有 Context membership、ContextVersion、ordering、expiry、token/byte budget、sufficiency、snapshot/delta 和 reconciliation。

这里有真实的资源策略重叠，但没有证据证明需要把两个 Owner 的语义合并。最有价值的突破是把资源控制从散落的策略实现中抽出来，形成**一个 Runtime 内部 Resource Manager（逻辑模块，不是新服务）**：

- 资源账本：CPU、RAM/VRAM、候选数、证据字节、token、并发槽、deadline；
- 分层预算：全局 → principal/scope → session/context → request/stage；
- 资源预留：fan-out、rerank、context expansion 前先 reserve；
- 调度：交互 Recall 优先、background refresh 可延期，跨 principal 公平；
- 驻留：Working Set/cache 使用统一 byte/entry accounting；
- 回收：只回收可重建的派生驻留项；Context 通过 G 的授权操作缩减，不由资源管理器直接改写；
- 反馈：压力、队列年龄、cache miss、token 预算与 sufficiency 结果驱动 admission。

### 4.2 不应统一的部分

- Canonical Memory 不是可驱逐缓存。
- Forget/Permission 不是资源策略；任何预算/优先级都不能覆盖它们。
- RetrievalResult 与 ActivationRecommendation 是 F 的语义；ContextEntry/ContextVersion 是 G 的语义。
- Context budget 是用户可感知的语义预算，不能简化成 RAM budget。
- Applied Context 是 Adapter 证据，不是驻留状态。

### 4.3 成熟机制借鉴

- Linux cgroup v2 的 `memory.low`、`memory.high`、`memory.max` 分别表达保护、节流压力和硬限制；适合借鉴层级资源控制与压力反馈，不应直接照搬为跨平台应用内部内存算法。
- Redis 的近似 LRU/LFU 说明精确维护全局访问序列并不总是值得；缓存淘汰策略应通过命中率/CPU/元数据开销实测选择。
- Qdrant 的 payload index + HNSW 说明检索过滤与向量索引必须协同设计；资源管理器只能调度检索资源，不能替代索引本身的 filter semantics。
- OpenTelemetry 的 trace context 传播适合为每次预算预留、任务取消、驱逐和 Context 更新建立因果链；高基数 ID 不应成为 metric labels。

### 4.4 初步结论

**CANDIDATE：单一 Resource Manager 统一资源账本、预算分层、准入/调度/回收；保留 F/G 的领域权威。** 不新增微服务，不把 Context Manager 改名成 OS，不在首个版本引入复杂预测型调度器。

## 5. Workstream C — Memory IR / Memory Compiler

### 5.1 当前已有基础

E 已有 durable acceptance、recoverable work item、deterministic normalization、可选模型抽取、Evidence/Provenance、candidate proposals、conflict proposals、canonical commit coordination 等阶段。其 Evidence/Provenance 合同要求 exact source version/digest、locator、support/refute/qualify role、method/model lineage 和 Forget dependency registration。

因此 Memory IR 的目标不是再创建一套新流程，而是将当前阶段间的临时对象收敛成一个稳定、可版本化、可验证的中间契约。

### 5.2 建议的最小 IR

顶层 envelope：
- `ir_version`、`schema_digest`、`producer`、`derivation_run_id`；
- `source_refs[]`（不可变版本/摘要/定位器）；
- `scope_refs[]`、`observed_at`、`recorded_at`；
- `nodes[]`：Fact/Claim/Event/Entity/Relation/Procedure 等 typed candidate；
- `evidence_links[]`：support/refute/qualify/context-only；
- `provenance[]`：父节点、transform kind、tool/model/prompt/policy version、input/output digest；
- `uncertainty[]`、`conflicts[]`、`validation_findings[]`；
- `forget_dependencies[]`（引用 D receipt，不自创 D 权威字段）。

IR 中的 Fact/Claim 类型必须遵守 B 的 ADR 状态；在 B ADR-BLOCKED 期间只能使用明确的 provisional discriminant 或 opaque proposal，不得冻结 wire/storage schema。

### 5.3 编译 pass 边界

1. Parse/Normalize：确定性，原始 source 不可覆盖。
2. Extract：模型可选，输出候选和原文 span，不拥有真值。
3. Type/Scope Validate：确定性硬门，失败即拒绝/隔离。
4. Evidence/Provenance Attach：精确引用源版本、摘要和转换 lineage。
5. Conflict/Consolidation Propose：保留冲突，提出而非擅自裁决。
6. Optimize：只做语义保持的去重、归一化、冗余压缩；每次优化记录输入/输出 digest。
7. D Commit Request：通过 D 权威提交；IR 不直接写 canonical store。
8. Projection Publish：在依赖登记、Fence、Permission 和 final visibility gate 满足后发布。

### 5.4 Incremental recompilation

以 `source_digest + parser_version + extraction_policy/model_version + IR_schema_version + transform_versions` 形成 derivation fingerprint。输入或 pass 版本改变时，仅重编受影响的 lineage 子图；不可复用旧的 authorization/fence receipt 作为当前发布许可。历史 derivation 保留可追溯性，新的 DerivationRun 创建新节点，不覆写旧 provenance。

### 5.5 初步结论

**CANDIDATE：引入 Memory IR 作为 E 内部的类型化 stage contract；不新建独立 Compiler Service，不把所有 pass 都做成插件。** 首版只需 5–7 个稳定类型、schema version、source/provenance、validation report 和 deterministic normalization。

## 6. 成熟产品采用边界

| 产品 | 原问题 / 机制 | 对 Memory Brain 的适用性 | 不适用 / 成本 |
|---|---|---|---|
| PostgreSQL | ACID、MVCC、Serializable Snapshot Isolation | canonical transaction、idempotency、outbox、同域线性化候选 | 事务范围必须物理闭合；serialization retry、连接/备份/HA运维成本 |
| SQLite | 嵌入式事务、WAL、多读单写 | 最小本地单机/单进程垂直切片候选 | WAL 依赖同主机共享内存，不适合网络文件系统/多主机 |
| Lucene / Tantivy | 倒排索引、immutable segments、后台 merge | lexical retrieval 直接采用成熟库，避免自研全文索引 | index doc IDs/segment 内部身份不可作为 canonical identity；merge 与 rebuild 资源成本 |
| Qdrant | HNSW + payload indexes + filtered vector search | 数据量/过滤/向量查询需要独立服务时采用 | 增加进程/部署、数据复制、filter schema、版本/删除/Forget 一致性成本 |
| Temporal | Event History、deterministic replay、Activity 隔离外部副作用 | 若后台流程跨长时间/多服务/多次恢复，再评估采用 | 当前 local-first modular monolith 可能不需要完整 Temporal 服务运营成本 |
| Kafka | 分区 append log、offset、consumer replay、compaction | 仅在多消费者吞吐/保留/跨节点事件流有量化需求时 | 不作为默认队列；引入 broker、partition ordering 限制、retention/replay/ops |
| TLA+/Alloy | 并发状态模型/关系约束与反例搜索 | Forget 和授权线性化关键路径 | 模型抽象与真实实现之间仍需 refinement/conformance |
| OpenTelemetry | trace/metric/log correlation | 直接采用 API/SDK/semantic conventions | 避免高基数标签和敏感内容泄漏 |

## 7. 对现架构的初步判断

### 值得保留（DECIDED 基线，不因本研究变更）

- Canonical Memory / Memory Context / Applied Context 三层区分。
- D/I/F/G/H/C 各自权威与 Scope/Permission/Forget 约束。
- Durable Accepted 与 Compiled/CanonicalCommitted/Indexed/Delivered/Applied 的分离。
- Evidence/Provenance、typed cursors/epochs、unknown fail-closed。
- Brain 不承担 Agent planning/tool execution。

### 复杂度风险（CANDIDATE，需要实证）

- 跨 Owner 重复表达同一条 race/failure contract，版本 bundle 与 exact adoption 反复核对。
- F 的 request budgets、Working Set limits 与 G 的 Context budgets 可能存在重复记账。
- E 的多个候选对象/阶段输出若没有统一 IR，可能造成 adapter/schema/provenance 转换重复。
- COC、Storage Prepared XID、Owner-local gates、receipt/sequencer、recovery cutoff 的多层协议可能形成过高的集成负担；不能仅凭文档数量断言过度设计，需比较最小单事务实现。
- 复杂状态命名和多个 cursor namespace 本身不是坏复杂度；若它们对应不同权威和不同排序语义，合并反而危险。

## 8. 下一阶段三个最值得投入的实验

1. **Forget Model + Counterexample Suite**：将 ProducerRegistration / FenceInstall / DependencyRegister / Publish / LostACK / Restore / Replay 建成最小 TLA+ 模型，输出反例轨迹和模型边界；随后映射到 D/E/Storage API 与 SQL transaction prototype。
2. **Runtime Resource Manager A/B**：以同一真实任务集比较当前分散预算与统一层级预算；测 p50/p95、token waste、RAM peak、cache hit、partial result、fairness 和 Forget/revocation latency。
3. **Memory IR Vertical Slice**：固定 20–50 条代表性原始经历，比较当前 stage DTO 与 typed IR；测 schema/adapter 数量、重复解析、determinism、增量重编范围、provenance 完整率和人工复核成本。

## 9. 当前结论状态

| 结论 | 状态 |
|---|---|
| TLA+ 主模型、Alloy 补充 | CANDIDATE |
| Resource Manager 统一资源账本、不统一 Owner 权威 | CANDIDATE |
| Memory IR 作为 E 内部 stage contract | CANDIDATE |
| PostgreSQL/SQLite/Lucene/Tantivy/Qdrant/Temporal/Kafka 具体采用组合 | TO_VALIDATE |
| 新方案已优于现架构 | UNRESOLVED（无对照实验） |
| 修改 A–I 权威规范 / ADR | NOT AUTHORIZED |

## 10. 外部资料

- TLA+ tools / TLC / Apalache: https://lamport.org/tla/tools.html
- Alloy 6 model and bounded traces: https://alloytools.org/spec.html
- PostgreSQL 18 transaction isolation: https://www.postgresql.org/docs/18/transaction-iso.html
- SQLite WAL constraints: https://sqlite.org/wal.html
- Temporal Event History and replay: https://docs.temporal.io/encyclopedia/event-history
- Kafka log design: https://kafka.apache.org/design/
- Lucene segment model: https://lucene.apache.org/core/10_2_1/core/org/apache/lucene/index/package-summary.html
- Tantivy architecture: https://docs.rs/tantivy/latest/tantivy/
- Qdrant indexing: https://qdrant.tech/documentation/manage-data/indexing/
- Linux cgroup v2 memory controller: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- Redis eviction: https://redis.io/docs/latest/develop/reference/eviction/
- OpenTelemetry context propagation: https://opentelemetry.io/docs/concepts/context-propagation/
