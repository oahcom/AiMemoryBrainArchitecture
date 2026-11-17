# 架构复杂度评估
# X — 首席架构复杂度评估

- 评估 ID：X-ACA-2026-11-17
- 版本：1.0
- 状态：**独立设计级评估——不构成 Owner 批准、契约冻结或实现验收**
- 仓库：`oahcom/AiMemoryBrainArchitecture`
- Main 基线：`b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- 评估分支：`review/architecture-complexity-assessment-2026-11-17`
- 日期：2026-11-17
- 角色：X — 首席架构复杂度评估
- 英文对应版本：[English version](2026-11-17-architecture-complexity-assessment.md)

## 1. 执行结论

**当前架构的实现、验证和长期维护可行性：NOT PROVEN（尚未证明）。**

架构的问题并非简单的“规模太大”。主要成本来自多个独立 Owner 状态机和证明义务的组合：Canonical Memory、Compiler Admission/Publication、Retrieval/Index、Context Delivery、Adapter Application、身份与授权、Forget、Storage Visibility、COC 和 Restore。

设计中存在必须承担的正确性成本：来源追溯、Scope 优先授权、不可变版本、类型化因果位置、幂等持久化接收、Forget 防复活、最终推理边界证明，以及故障关闭式恢复。这些不能为了降低评分而删除。

首要复杂度放大器是：一个业务操作可能跨越多个权威，每个权威拥有自己的状态、Epoch、Cursor、证据、重试和恢复规则。第二个放大器是多个 Owner 分支和协议修订链之间的精确版本治理。第三个放大器是多个关键契约仍处于 CANDIDATE 或 OPEN，最终实现可能不得不编码尚未完全闭合的语义。

本评估衡量的是**设计系统及其必要证明负担**，不是代码量、交付工期或某个 Owner 的工作质量。分数是序数风险指标，不是可相加的项目总分。

### 决策摘要

| 问题 | 评估 |
|---|---|
| 能否不进一步简化就按当前完整组合直接实现？ | NOT PROVEN |
| 逻辑模块化单体方向是否可行？ | CANDIDATE；明显优于过早微服务化 |
| 正确性要求产生的复杂度是否都能消除？ | 不能；部分属于基础成本 |
| 是否存在过度设计？ | 存在治理/版本化与协议面扩张风险；尚无足够证据认定核心安全不变量是不必要的 |
| 当前测试负担是否已被限制且可端到端执行？ | NOT PROVEN |
| 运维拓扑是否确定？ | 否；Storage 拓扑 ADR 仍 BLOCKED |
| 小型团队能否持续并行承担全部工作流？ | 若没有严格排序和首发范围限制，风险很高 |

## 2. 证据基线与限制

### 2.1 实际读取的源版本

| 来源 | 分支 / Ref | 精确版本或 Blob | 评估用途 |
|---|---|---|---|
| Main | main | Commit `b372b62c640a2b656e54b6db62a4ee67d7d8c001` | 仓库基线和治理 |
| D | `session-d-memory-brain-2026-11-16` | HEAD `97e68fbd225bdf0ac71860c01077481afc162d50`；Forget Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`；Cursor Blob `4688a0ca487bf4d853c7f0220408abe8d743d159` | Canonical 权威、Fence、Cursor |
| E | `session-e-memory-compiler-2026-11-16` | HEAD `fdb4f67a83083d995930b88f93975b5ee36080f3`；Forget Blob `00e37ba56596e710513c8d0568acd79141d9101b`；Accepted Blob `5ca77a5b48e69afb3bc81429baf538be7dce4d46` | Ingress、Work 生命周期、Publication |
| F | `session-f-memory-runtime` | HEAD `8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3`；Retrieval Blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af`；Forget Blob `ce59252dbbdc5d10d016704797e9ba12d5a941bd` | Retrieval、Index、Cache、防复活 |
| G | `session-g-memory-context` | HEAD `f9ca0ddc36e17f74041506f17039f0202d13042e`；Version Blob `05c0739d0c22576a1fd5affc7d73c078c89049b1`；Reconciliation Blob `87063aceebed1c30b7840045ada8e3f348732688` | Context 状态与协调 |
| H | `session-h-bmcp-protocol` | HEAD `6eb1816f3a17b68422f55848cc722c76b835d9a1`；Applied Blob `ed6b43a29aa368d772c701ffc83309a5aadf3c00`；Delivery Blob `bf9732cc39d156853b507c3a3a4e573159978f49` | 协议、Adapter、Applied |
| I | `session-i-security-governance-2026-11-16` | HEAD `3f29dbc4dffb99c16ab1d3197e2f5fb8207ebe2f`；Inventory Blob `9100061fa986fb6676656169de3fcf9fc1c72664`；Identity Blob `03765efac4bb1153f303ce0030f9e277d602e81d` | 身份、策略、Global Forget |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | HEAD `17be31915b06d98d7f822e6e5270b8cde39eb0bb`；拓扑 ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`；Visibility Blob `175ee7b1349cfdb79a19898b311a88391ed88010`；v3.2.5 清单 Blob `bea90697e7a61d43bed00543d636a5cdf40cf5ca` | Storage/COC/Restore |
| C | `session-c-agent-integration-2026-11-16` | HEAD `9d4301b056fd72f683bdcfeceaa262f21e991051` | Agent 边界；本次未深入读取其完整源包 |
| A | `session-a-integration-2026-11-16` | HEAD `d72dbac6e0f739cd00ac986176b78ec5cd385d88` | 集成与协调；本次未深入读取其完整源包 |
| PR #28 | `docs/bilingual-coverage-completion` | HEAD `365726ac4ac9f16c935eb4b23f88411b4ecc0fc4` | 双语迁移范围与已知缺口 |

Owner 分支 HEAD 是本次评估期间读取的实时引用；Blob 用于标识实际读取的具体源文件。本次属于有范围限制的源样本审查，不声称已审查所有 Owner 分支的全部文件。

### 2.2 仓库集成事实

- Main 递归 Tree 包含 82 个文件。D/E/F/G/H/I/Storage 的详细源规范并未全部集成到 Main；Owner 分支存在不能等同于 Main 已集成。
- PR #28 仍为 Draft/Open，并明确说明其新增源对齐的双语文档，但不修改 Owner 源规范；同时明确不声称完成全部 136 个文件的语义一致性验收。
- PR #28 记录 C/G/H Applied 冻结 BLOCKED、I 治理 BLOCKED、Storage 拓扑 ADR-BLOCKED、JF-10 P0 OPEN / NOT IMPLEMENTED / NOT RUN。
- 双语覆盖登记将多项 Owner 详细规范的翻译标记为 NOT STARTED。阅读指南不是规范性 Owner 契约。
- 评估时 Main 分支保护 API 显示未启用。这属于治理/运维暴露，不代表源设计语义错误。
- Issue #43 仍为 Open，定义了架构统一与可行性审查边界。本评估保留其中的非声明和权威边界。

### 2.3 证据限制

本次未验证生产实现、完整端到端一致性活动、代表性负载基准、生产拓扑或小团队交付试验。若干分支内审查明确属于静态审查或模拟角色视角，并非独立外部签署。以下评分不能被解释为实测运行复杂度。

## 3. 评分模型

每个模块和跨模块机制分别从八个维度评分：

1. **I — 内部复杂度：** 内部职责、算法、对象模型和局部规则。
2. **D — 依赖复杂度：** 正确运行所依赖的外部契约数量与强度。
3. **S — 状态复杂度：** 状态对象、转换、Epoch、Revision 和生命周期组合。
4. **C — 并发复杂度：** 竞争、Admission、排序、锁、线性化和重复工作。
5. **R — 恢复复杂度：** 崩溃窗口、重放、恢复、协调和未决结果。
6. **V — 验证复杂度：** 测试、证据、证明谓词和独立验收。
7. **O — 运维复杂度：** 部署、数据服务、备份、监控、故障转移和人工运维。
8. **K — 认知复杂度：** 跨 Owner 理解、源版本绑定、文档和变更传播。

等级：1 低；2 中等；3 显著；4 高；5 极高。5 表示该维度的设计负担或未解决风险极高，不代表设计必然错误。

每个评分均须有证据、放大因素、简化机会、不可删除的正确性约束和置信度。禁止把分数相加或计算算术意义上的“系统总复杂度”。

## 4. 模块复杂度矩阵

维度顺序：**I / D / S / C / R / V / O / K**。

| 模块 / 权威 | 评分 | 主要证据与原因 |
|---|---:|---|
| B — Domain Model | 4/4/5/3/3/4/2/5 | Event/Memory/Fact/Claim/Entity/Relation/Evidence 的不同语义；时间和认知状态；Typed ActorRef/ScopeRef 依赖。Fact/Claim 仍 ADR-BLOCKED，身份/Schema 耦合尚未解决。 |
| C — Agent Integration | 4/5/4/4/4/5/3/5 | Telemetry、Adapter 身份、推理边界集成、Provider Outcome 和实际最终请求证据。C/G/H Applied 依赖三个权威，不能从传输 ACK 推断。置信度中低：本次未深入读取 C 分支源文件。 |
| D — Canonical Memory | 5/5/5/5/5/5/4/5 | Canonical 生命周期、身份、Aggregate Revision、每个 Authority 的全局 CanonicalCommitCursor、每个 Memory 的 Lifecycle Cursor、ForgetOperation/Fence、Producer Registry/High-water 和依赖血缘。 |
| E — Memory Compiler | 5/5/5/5/5/5/4/5 | 持久化 Accepted Receipt、Compile Intent、Work/Attempt/Lease 身份、暂存 Derivative、Dependency Registration、Publication Gate、DLQ/Replay 和多种独立 Receipt。D/Storage 原子操作仍 OPEN。 |
| F — Memory Runtime | 5/5/5/5/5/5/4/5 | Structured/Entity/Full-text/Vector/Graph/Temporal/Provenance 检索；Scope-before-candidate；分区 Watermark；最终复核；Cache/Working Set 隔离与防复活。 |
| G — Memory Context | 5/5/5/5/5/5/4/5 | 不可变 ContextVersion、CAS/串行化、ChangeSet、Delivery/Session 状态、Reconciliation 触发、Stale/Blocked 状态、按消费者记录 Applied 历史和 Forget 失效。 |
| H — BMCP / Adapter | 5/5/5/5/5/5/4/5 | 版本化 Envelope、身份绑定、Capability Epoch、Snapshot/Delta、Reconnect、Delivery ACK 分类、加密证据和最终请求 Applied 分层。多个 Schema/Recovery 修订增加兼容性和精确版本负担。 |
| I — Security & Governance | 5/5/5/5/5/5/5/5 | Principal/Issuer/Delegation、Scope Binding、PermissionEpoch、Revocation 排序、封闭世界 Producer/Recipient Inventory、Target Seal、Global Forget 证明、备份与物理擦除例外。 |
| Storage / Consistency / COC | 5/5/5/5/5/5/5/5 | Durable Hidden Participant、Prepared-XID/GID 身份、D/I/Storage Gate、Atomic Visibility/Outcome、COC Prefix/Batch/Manifest、Restore High-water 和 Split-brain Fencing。物理拓扑 ADR 仍阻塞。 |
| A — Integration / Governance coordination | 4/5/4/4/4/5/3/5 | 精确版本源登记、依赖图、Owner 验收、跨文档一致性和 Conformance 协调。协调成本高；不得成为模块语义的影子 Owner。 |

**置信度：** B/D/E/F/G/H/I/Storage 对所引用源样本为中高；A/C 为中低。以上是架构设计评分，不是实现测量结果。

### 模块结论

- **最高内部状态负担：** D、E、G、H、I。即使不考虑跨模块组合，其局部状态机也已较大。
- **最高并发/恢复负担：** D、E、Storage，其次 I 和 G。关键竞争并非普通请求并发，而是决定已遗忘或未授权数据是否重新可见。
- **最高认知负担：** I、H、Storage、A。它们的证据和协议修订要求理解多个权威命名空间及精确版本依赖。
- **检索专属负担最高：** F。混合检索本身并非唯一成本；授权必须先于候选暴露，并贯穿 Fusion、Reranking、Materialization 和返回阶段复核。
- **最高集成依赖：** C/G/H Applied 与 D/E/Storage Publication。不能把另一个模块的 ACK 当成证明来安全实现。

## 5. 跨模块复杂度矩阵

维度顺序仍为 **I / D / S / C / R / V / O / K**。

| 跨模块机制 | 评分 | 为什么超过单模块复杂度 |
|---|---:|---|
| E Admission × D Forget Fence × Storage Visibility | 5/5/5/5/5/5/4/5 | Producer Class/Work 注册、Fence 快照/High-water、Dependency Edge、Hidden Prepare、最终 Fence 复核、Visibility Pointer 和不可变 Outcome 必须共享可证明的线性化模型。 |
| D/E/F/G/H/I/Storage Global Forget | 5/5/5/5/5/5/5/5 | I Domain Inventory/Seal + D Work-item Barrier + 各 Owner Watermark/ACK + Adapter/离线状态 + Backup/Restore/外部接收方；任何局部 ACK 都不能证明全局完成。 |
| C/G/H 最终请求 Applied | 4/5/5/4/4/5/3/5 | 精确 ContextVersion、Delivery Attempt、Adapter Capability、认证身份、Scope、Permission Epoch、Forget Fence、Managed-region Digest 和实际提交的推理请求必须绑定。 |
| JF-10 / COC / Storage Prepared Participant | 5/5/5/5/5/5/5/5 | COC Quorum Prefix、不可变 Participant Tuple、GID/Native XID/DB Incarnation、I Terminal Decision、Same-XID Resolution、Owner Outcome 和 Atomic Visibility Receipt；UNKNOWN 必须保持 Barrier。 |
| Typed Causal Position 与 Freshness Vector | 4/5/5/4/5/5/3/5 | CanonicalCommitCursor、AggregateRevision、LifecycleEventCursor、IndexWatermark、ForgetFenceGeneration、PermissionEpoch、ContextVersion、AdapterCapabilityEpoch 和 Producer High-water 不可互换。 |
| Restore / Backup / Split-brain Recovery | 5/5/5/5/5/5/5/5 | Restore Quarantine、WAL/Timeline 连续性、Old-primary Fencing、COC Prefix、I/D Ledger、Inventory Seal、Prepared Participant 和 Owner-local Gate Release 必须在服务前完成协调。 |
| 双语源文件与精确版本治理 | 3/5/4/2/3/5/3/5 | 双语文件、稳定标识、Source Branch/Commit/Blob Pin、Supersession 和独立 Owner 审查。这是治理复杂度，不是运行时复杂度。 |

### 跨模块评估

系统的主要复杂度是**协议组合**，不是模块数量。只有当相关权威对相同不可变操作/Participant 身份、精确 Scope、当前 Epoch、因果截止点、终态处置和证据达成一致，工作流才安全。如果某个组件已前进，而另一个组件仍旧或未知，正确结果通常是阻塞、隔离或协调，而不是猜测。

## 6. 状态空间复杂度分析

### 6.1 组合状态轴

关键工作流至少会组合以下相互独立的状态维度：

- 身份：Issuer、Principal、ActorRef、Producer/Recipient Instance 和 Trust/Key 状态。
- Scope：Tenant/User/Project/Agent/Instance/Task/Session/Environment 和 Purpose。
- Canonical 状态：Object Identity、Aggregate Revision、Lifecycle State 和 CanonicalCommitCursor。
- Compiler 状态：Accepted、Registered、Queued、Leased、Running、Staged、DependencyRegistered、Published、CanonicalCommitted、Retry、DeadLettered、Terminal。
- Forget 状态：Operation、Target Inventory、Fence Generation、Producer High-water、Dependency Coverage、Suppression、Cleanup 和 Residual Exception。
- Runtime 状态：Index/Channel/Partition Watermark、Coverage/Schema Version、Cache/Working Set Generation 和 In-flight Query/Rerank。
- Context 状态：ContextVersion、ChangeSet、Reconciliation State、Delivery Attempt 和 Consumer/Session Applied Version。
- Storage/COC 状态：Private Prepare、Participant Identity、Prepared Transaction、Quorum Prefix、I Decision、Storage Outcome、Visibility Pointer 和 Restore Gate。
- 时间/故障状态：Crash Point、Lost ACK、Duplicate Delivery、Stale Lease、Delayed Event、Offline Recipient、Replay、Rollback 和 Unknown Outcome。

这些维度并非一个全局状态机。它们是独立 Owner 局部状态机，在集成边界处形成组合。当前资料尚未闭合全部有限状态域、合法转换和等价状态约简，因此无法负责任地计算可能状态总数。**精确状态空间基数：NOT PROVEN。**

### 6.2 最高风险组合

1. Producer Registration 获胜或 Forget Fence 获胜，随后在 Dependency Registration 或 Publication 前发生崩溃。
2. Storage Hidden Prepare 成功但 ACK 丢失；D Admission 和 Retry 必须解析到同一个不可变 Participant。
3. I Authorization/Revocation 在初始检查与最终 Visibility Commit 之间发生变化。
4. Index Watermark 落后，而 Canonical Forget Fence 已前进；候选不能通过 Fusion、Cache 或 Graph Expansion 泄露。
5. Context Delivery 已在本地应用，但最终 Inference Submission 尚未证明；不得 Full Applied。
6. Adapter 在 Forget 期间离线，稍后带着过期队列/缓存重连并尝试 Replay。
7. Restore 将数据回滚到 Control-ledger High-water 或 Inventory Seal 之后；系统必须保持 RESTORE_FENCED。
8. COC Quorum 丢失且 Prepared Participant 未决；UNKNOWN/IN_DOUBT 必须保留锁和 Barrier，不能通过 TTL 解决。

### 6.3 必须保留的正确性约束

- 身份、权限、Fence、Lineage、Cursor Gap、Participant Outcome 或 Restore Proof 未知时必须 Fail Closed。
- 绝不能从一个权威的 ACK 推断另一个权威的状态。
- 不得跨命名空间比较或强制转换 Typed Cursor/Epoch。
- 最终 Visibility Commit 前不得暴露暂存数据。
- DLQ、Lease Expiry、Timeout 或缺失 ACK 不得视为终态成功。
- 不得从 Delivered、单纯 Materialization 或 Adapter Capability 声明推断 Applied。
- 不得从 Canonical Suppression 或局部 Cleanup 声称 Global/Physical Forget 完成。
- Restore 数据必须等独立 Control Ledger 和 Owner Gate 协调完成后才可服务。

### 6.4 不削弱正确性的简化方式

每个状态机只保留一个权威 Owner；定义最小不可变跨模块 Tuple；暴露少量类型化边界操作；让派生 Index 和 Cache 可丢弃；并在有限的首发部署中集中物理线性化点。不要在每个消费者重复实现策略逻辑。消费者应执行权威方签发的决策，而不是重新实现权威方的决策规则。

## 7. 复杂度热点登记表

| ID | 热点 / 放大器 | 严重性 | 证据 / 影响 | 必须采取的行动 |
|---|---|---|---|---|
| XH-01 | D/E/Storage Producer-Fence-Publication 线性化 | P0 | D 语义已定义；E 明确指出 Atomic Registration/Final Gate OPEN；Storage 拓扑 ADR 尚未选择方案 | 实现前闭合精确操作、事务边界、Retry/Unknown 语义和竞争/崩溃证明 |
| XH-02 | Global Forget 封闭世界 Inventory | P0 | I Inventory Epoch/Seal 与 D Work-item Barrier 不同；涉及 F/G/H/Storage/Backup/External Targets | 首发限定一个 PolicyDomain 和明确有限的 Producer/Recipient 集合；Unknown 必须阻塞 |
| XH-03 | JF-10 + Persistent COC + Prepared-XID | P0 | Storage v3.2.5 清单已发布但未共同接受/冻结；拓扑 ADR 阻塞；Gate A 部分通过；Gate B/C 实现延期/未运行 | 保持单域范围；精确 Owner 验收和工程证明完成前不得激活分布式拓扑 |
| XH-04 | C/G/H Applied Proof | P1 | Full Applied 要求最终请求提交证据及完整身份/Scope/Epoch/Fence 绑定；H Tier 2/3 不能发出 Full | 首发选择一种 Adapter Profile；否则只能报告 Delivered/Unknown，不能 Full Applied |
| XH-05 | Typed Cursor/Epoch 数量扩张 | P1 | 源契约至少存在九种不同命名空间 | 维护一个 Registry 和 Typed Wrapper；禁止通用整数/版本字段及跨域算术 |
| XH-06 | Schema 和精确版本变更 | P1 | H 存在 Unified COC/JF-10 Schema 1.2.0–1.2.13，RecoveryCutoff 1.0.0–1.0.5 / RecoveryJoin 1.0.0–1.0.2；Storage v3.2.3 及后继绑定清单 | 建立唯一规范当前版本清单；明确废止旧 Pin；从 Schema 生成兼容性测试 |
| XH-07 | Restore 与 Rollback 证明 | P0 | Storage Reference Tests 是逻辑模型；生产 Control-ledger、Old-primary Fencing、部署和运维证据仍独立缺失 | WAL、COC、I、D、Inventory、Participant 和 Owner-release 证据协调前保持 Restore 隔离 |
| XH-08 | Retrieval Channel × Authorization × Cache | P1 | F 支持 Structured/Entity/Lexical/Vector/Graph/Temporal/Provenance 路径；每条路径都有暴露前策略要求 | 首先使用 Structured + Lexical；Vector/Graph 扩展须有语料和 Scope 隔离测试依据 |
| XH-09 | 双语 + Owner Source 集成漂移 | P1 | Main 有阅读指南但并非所有详细 Owner 契约；PR #28 仍 Draft，且不声称完成全部语义一致性 | 将 Source Integration、Translation Parity 和 Semantic Approval 作为不同门禁 |
| XH-10 | Branch Protection / Review Enforcement | P1 | Main 分支 API 报告未启用保护 | 由项目治理 Owner 决定并验证保护规则；X 只记录运维风险 |

## 8. 复杂度预算与阈值

以下阈值是架构演进的建议控制线，不改变 Owner 决策。

### 8.1 评分阈值

| 分数 | 含义 | 门禁 |
|---:|---|---|
| 1–2 | 低 / 有界 | 常规模块审查 |
| 3 | 显著 | 明确 Owner、输入/输出和回归测试 |
| 4 | 高 | 必须有明确依赖图、故障模型、验收证据和指定维护者 |
| 5 | 极高 | 必须证明其属于正确性成本，或明确批准为有界风险；禁止静默引入；需要架构门禁 |

附加控制：
- 任意 P0 跨模块机制在并发、恢复或验证维度为 5 时，在其操作契约和证明义务闭合前保持 BLOCKED。
- 首发组件若运维复杂度为 5，必须缩减到单节点/单权威有界配置，或明确延期。
- 只有移除/合并机制或可证明地缩小证明面，才能接受评分下降；改名或隐藏状态不算降低复杂度。
- 不使用平均分。门禁由最高维度及其证据决定。

### 8.2 首发范围建议

| 领域 | 预算 / 限制 | 延期或排除 |
|---|---|---|
| Canonical Authority | 一个 Brain Authority | 多 Authority Global Ordering |
| Security Domain | 一个 I PolicyDomain | 跨 PolicyDomain 原子 Forget/Publication |
| Runtime Topology | 模块化单体；正确性关键状态转换先在一个进程内 | 微服务和跨服务分布式事务 |
| Storage Serialization | 每个 Canonical Memory Authority 一个权威事务域 | 除非另行证明，不引入 Option B 分布式协调器；Option C Check-then-write 已拒绝 |
| Queue | 一个持久化 Outbox/Queue 抽象和有界 Worker | 多队列产品及独立 Replay Fabric |
| Retrieval | 首先 Structured + Lexical | 在基准测试前不引入 Vector ANN、Graph Expansion 和多个独立 Index Engine |
| Cache | 初始关闭，或一个有界进程内可丢弃 Cache | 分布式 Cache 和跨节点失效 |
| Adapter | 一种明确声明的 Adapter Capability Profile | 首发不支持广泛多框架兼容矩阵 |
| Forget Inventory | 明确有限的 Producer/Recipient Class；Unknown 阻塞 | 任意插件生态和无界外部接收方 |
| Backup/Restore | 一条明确 Backup/Restore 路径，带 Quarantine 和 Owner-ledger Reconciliation | 多 Region Active-active 和多 PolicyDomain Restore |
| Model Inference | 独立、可选的资源边界 | 将模型推理作为持久化接收或恢复的前置条件 |

该范围不决定最终使用 SQLite 还是 PostgreSQL。PostgreSQL 18.7 已有有界 CI 能力证据；但 Storage Serialization Topology ADR 仍 BLOCKED，实际 Canonical Authority 部署不能由该证据推定。

### 8.3 测试复杂度预算

测试应围绕契约和持久化边界组织，而不是堆成一个巨大端到端套件。

| 测试层 | 必须覆盖的预算 | 退出证据 |
|---|---|---|
| Domain/State-machine Unit | 每个 Owner 局部转换、不变量、非法转换和幂等重放 | 确定性测试及状态转换覆盖 |
| Module Contract | Owner 边界输入/输出、授权、版本/Cursor 和错误语义 | Provider/Consumer 契约套件 |
| Concurrency | 每个安全关键竞争的两种串行顺序；Stale Lease/Epoch 和重复 Admission | 带不变量断言的确定性竞争 Harness |
| Crash/Recovery | 每个持久化边界前后崩溃、Lost ACK、进程重启、Unknown Outcome | 可复现故障轨迹和同身份协调 |
| Cross-module Conformance | D/E/Storage、D/E/F/G/H/I Forget、C/G/H Applied、Storage/COC/JF-10 | 精确版本向量套件和 Owner 专属证据 |
| Restore/DR | 缺失 WAL/Prefix、Stale Inventory、Old-primary Rejoin、Partial Restore、Participant Mismatch | 完整证明前持续 Fenced/Quarantined |
| Security | 身份伪造、Scope 混淆、Revocation Race、Replay、Key Rotation/Revocation、未授权存在性泄露 | 负向测试和可审计拒绝 |
| Performance | 代表性语料、Scope 分布、并发、模型/资源配置 | 可复现基准；不预设 SLO |
| Regression | 每个已修复 P0/P1 成为永久回归案例 | 与契约 ID 绑定的版本化测试集 |

Reference Model 测试通过不代表测试套件完成。逻辑模型、数据库能力探测、部署实现一致性和生产验收是不同证据类别。

### 8.4 运维复杂度预算

首发应只有一个 Canonical Database Authority、一份 Backup/Restore Runbook、一条 Monitoring/Audit Pipeline、一个明确运维责任人、有界 Worker 并发，以及明确的磁盘/队列/索引限制。生产上线前必须有 RPO/RTO、Failover Fencing、Restore 演练、备份完整性、告警责任和恢复操作人员证据。

### 8.5 认知复杂度预算

- 一个规范术语表和一个 Typed Cursor/Epoch Registry。
- 每个跨模块 Bundle 只有一个权威当前版本清单。
- 每份契约明确一个 Owner、Consumers、源版本、状态和精确验收证据。
- 阅读指南必须明确标注为非规范性，并链接 Owner 源契约。
- 避免在多个指南重复相同规范性状态机。适当使用生成索引或简明 Consumer Map。
- 每新增 State、Epoch、Cursor、Receipt 或 Protocol Version，必须说明其不能替代哪个现有概念以及原因。

## 9. 简化建议

### 必须保留 — 正确性成本

1. Canonical Memory 权威及不可变 Revision/Provenance。
2. Scope-first Authorization 和受保护边界的当前授权复核。
3. Accepted、Compiled、CanonicalCommitted、Indexed、Delivered、Applied 证据分离。
4. Typed Cursor/Epoch 命名空间及权威归属。
5. 持久化 Idempotency、稳定 Work Identity 和可安全重放的状态转换。
6. Forget Fence、封闭世界 Producer Inventory、Dependency Registration 和防复活。
7. 最终 Visibility Linearization 及 Fail-closed UNKNOWN/IN_DOUBT。
8. Adapter 最终请求证明边界；不得虚报 Full Applied。
9. Restore Quarantine、Old-primary Fencing 和独立 Owner-ledger Reconciliation。
10. 规范契约的双语语义一致性和精确源版本绑定。

### 可以简化 — 保留语义、减少机制

1. 将逻辑子系统实现为一个 Rust 模块化单体；默认不让每个 Owner 成为独立进程、Crate 或可部署服务。
2. Compiler 和有界后台任务复用一个持久化 Outbox/Worker 执行底座，同时保留各 Owner 自己的状态和授权。
3. 维护一个规范 Typed-ID/Cursor/Epoch Registry；使用 Nominal Rust Newtype 和生成式序列化，避免重复定制 Wrapper。
4. 使用一个共享 Conformance Harness 和 Owner 专属 Adapter/Fixture；避免每个模块另造一套故障 Harness。
5. 同一 Publication/Participant Identity 在各模块之间尽可能复用一个不可变 Operation Tuple 和 Digest Profile，避免每一跳独立编码身份。
6. Working Set、Context 和 Cache 优先保存 Canonical Reference，而不是复制 Payload。
7. 使用一份带稳定 Manifest 的双语评估报告，避免在多个指南重复规范性文字。

### 可以延期 — 首个正确性切片不必实现

1. Vector ANN、Graph Retrieval 和 Reranking，直到 Lexical/Structured 基线完成测量。
2. Distributed Cache、Multi-region Active-active 和 Multi-authority Causal Ordering。
3. Multi-PolicyDomain Atomicity；它仍 BLOCKED，不得隐式支持。
4. 首发之外的广泛 Adapter 生态及 Capability Tier。
5. 若确定性/人工工作流足以先验证核心契约，则延期复杂自动记忆巩固和多模型路由。
6. 在单 Authority Publication/Forget 契约和物理拓扑选定前，延期完整生产 COC 部署。
7. 在正确性和工作负载基线建立前，延期高级优化、推测式预取和 Cache Warming。

### 需要重新评估 — 本报告不擅自决定

1. D 与 Storage 能否共享一个 Serializable Transaction Domain（Storage ADR Option A），还是必须使用持久化分布式协调器（Option B）。只有真实部署能证明时，A 才是优先候选。Option C Check-then-write 已拒绝。
2. 首发 Closed-world Producer/Recipient Inventory 的精确范围。
3. Full Applied 是否属于首发范围；或首发诚实地止于 Delivered/Unknown。
4. 实际语料和延迟要求能够证明多少 Retrieval Channel 和 Index Partition 有必要。
5. H Schema/Recovery Versioning Policy，以及历史 Schema 是否都需要保留为活跃兼容目标。
6. 运维验收范围、人工 On-call 责任和部署边界。

### 不应引入

1. 没有实测隔离/扩展需求就按逻辑子系统或 Owner 拆微服务。
2. 用通用 Version、Sequence、Epoch 或 Cursor 字段抹掉权威/类型边界。
3. 为 Context、Forget、Authorization 或 Publication 增加第二个独立事实源。
4. 用本地 Check-then-write 替代 D/Storage Linearization Gate。
5. 将 Cache/Index/Queue/Adapter ACK 当成 Canonical Proof。
6. 在明确设计和故障证明前引入 Multi-PolicyDomain 或 Multi-region 语义。
7. 仅为掩盖 Owner 不清或源版本过期而新增 Protocol State/Receipt/Version。

## 10. 小型工程团队失控预测

小团队最可能在以下位置失控：

1. **试图同时实现所有 Owner 套件。** 跨 Owner 契约尚未冻结，团队会把猜测写进接口。
2. **把 Forget 实现为后台删除任务。** 真正困难的是 Producer Admission 和 Visibility Linearization，而不是删除数据行。
3. **把不同 Receipt 混为一谈。** AcceptedReceipt、RegistrationReceipt、PublicationReceipt、IndexApplied、Adapter ACK 和 Global Forget Evidence 证明不同事实。
4. **立即构建完整检索栈。** Vector/Graph/Cache 复杂度会早于语料、质量和负载对其的证明。
5. **只测试 Happy Path 或 Reference Model。** 关键缺陷位于崩溃窗口、重复/Lost ACK、Revocation Race 和 Restore Rollback。
6. **多个活动源分支没有单一 Current Manifest。** 精确 Blob Pin 和过期决议会消耗审查能力并造成契约漂移。
7. **低估运维工作。** COC、Prepared Transaction、Backup、Restore Fencing、Key Lifecycle、Monitoring 和人工响应不是附带实现细节。
8. **允许 AI Session 独立扩张架构。** 缺少严格 Owner Prompt、Change Manifest、Source Pin 和 Review Gate 时，文档与协议版本会以团队无法验证的速度增长。

## 11. 本评估建议形成的架构约束

以下为 X 向治理提出的建议，不是单方面修改 Owner 契约：

- **X-AC-01：** 首个实现切片 SHOULD 采用模块化单体、一个 Canonical Memory Authority 和一个事务串行化域。
- **X-AC-02：** 首发 MUST 明确仅一个 I PolicyDomain，除非存在另行验收的多域协议。
- **X-AC-03：** 任意 P0 机制在并发/恢复/验证维度评分为 5 时，在其操作契约和可执行证明计划经权威 Owner 接受前 MUST 保持阻塞。
- **X-AC-04：** 模块不得仅凭另一个模块的传输或局部 ACK 声称跨模块终态。
- **X-AC-05：** Typed Cursor/Epoch 在 Schema、代码和测试中 MUST 保持名义类型区分。
- **X-AC-06：** 首个检索切片 SHOULD 使用 Structured + Lexical；新增通道必须有实测质量/延迟依据。
- **X-AC-07：** 只有 C/G/H 最终请求证明谓词满足时 MUST 才能提供 Full Applied；否则报告实际较窄的 Delivery State。
- **X-AC-08：** Restore MUST 从 Fenced/Quarantined 开始，且仅在当前 Control-ledger 和 Owner Proof 协调后才能服务。
- **X-AC-09：** 每个新增 Protocol Version、State、Epoch、Cursor 或 Receipt MUST 说明精确兼容需求和 Supersession 路径。
- **X-AC-10：** 复杂度评分变化 MUST 引用被删除/合并的机制或缩小的证明面；不接受只改评分的优化。

## 12. 优先级简化与闭合顺序

| 优先级 | 工作 | 责任权威 | 排序原因 |
|---|---|---|---|
| P0-1 | 闭合 D/E/Storage Register-Fence-Dependency-Final Publication 操作和竞争语义 | D、E、Storage；A 协调 | 核心安全/可见性路径 |
| P0-2 | 限定 I Producer/Recipient Inventory 和单 PolicyDomain 首发范围 | I 与 D/E/F/G/H/Storage | 使 Forget 范围有限且可测试 |
| P0-3 | 选择 Storage Serialization Topology 并定义精确部署边界 | Storage、D、I；A 协调 | 没有它就无法实现原子性 |
| P0-4 | 闭合 JF-10/COC Same-participant、Same-XID 和 Restore 门禁，或明确延期 COC | Storage、A、I、D、C、H | 防止意外进入分布式部署 |
| P1-1 | 冻结 Typed Cursor/Epoch Registry 并完成消费者一致性验证 | D 负责权威；E/F/G/H/I 消费 | 防止语义类型漂移 |
| P1-2 | 决定 C/G/H Applied 首发范围及精确证明边界 | C、G、H、I | 避免虚假应用声明 |
| P1-3 | 集成精确 Owner Source Manifest 和双语详细契约 | A + 各 Owner | 使审查/实现基线可复现 |
| P1-4 | 建立共享 Contract/Race/Crash/Restore Test Harness | A 协调；各 Owner 提供 Oracle | 减少重复验证基础设施 |
| P2-1 | 基准测试检索通道扩展和模型资源需求 | F、Engineering | 只增加有依据的通道 |
| P2-2 | 验证生产运维、Backup/Restore、Monitoring 和 On-call | Storage、I、Engineering/Operator | 部署前需要，不是逻辑架构闭合前的前置条件 |

## 13. 最终回答

**当前架构复杂度是否处于可实现、可验证、可维护的范围内？**

**NOT PROVEN（尚未证明）。**

逻辑模块化单体方向是控制复杂度的可信方式。但当前完整设计包含多个极高复杂度的跨模块协议，尚未证明可执行的端到端证明路径、已选定的 Storage 拓扑、有界的运维责任和可持续的小团队验证能力。

只有刻意缩小首发范围、在编码前闭合正确性关键的跨模块线性化/恢复契约，并延期可选的检索/分布式/自动化能力，架构才可能变得可控。减少模块数量或删除正确性状态不是可接受的简化方式。

---

## 附录 A — 源文件解释说明

- Main 缺少详细 Owner 源文件，是集成可见性事实，不是对 Owner 分支设计质量的判决。
- 分支内 Conditional Pass 和模拟审查视角不等于独立批准。
- PostgreSQL 18.7 能力 CI 是有界引擎/配置证据，不会选择生产拓扑，也不能证明完整 D/I/Storage/COC 应用路径。
- 逻辑 Reference Model 测试不是物理实现或生产恢复证明。
- PR #28 双语结构检查不是完整语义一致性或架构验收。
- 本评估不根据复杂度分数推算实现工时。

## 附录 B — 关键源链接

- [Issue #43 — 全系统架构统一收敛与可行性审查](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)
- [PR #28 — 双语架构覆盖迁移](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/28)
- [D — Forget Fence 与完成契约](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/forget-fence-and-completion-contract.md)
- [E — Forget Fence 与 Derived Registration](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-e-memory-compiler-2026-11-16/04-memory-compiler/forget-fence-and-derived-registration.md)
- [F — Runtime Forget Suppression](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-f-memory-runtime/05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md)
- [G — Context Versioning](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-g-memory-context/06-memory-context/context-versioning.md)
- [H — Adapter Applied Attestation](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-h-bmcp-protocol/08-bmcp-protocol/adapter-capability-and-applied-attestation.md)
- [I — Global Forget Inventory](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-i-security-governance-2026-11-16/09-security-governance/global-forget-target-inventory-and-completion-evidence.md)
- [Storage — Serialization Topology ADR](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-storage-consistency-forget-atomicity-2026-11-16/reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md)
- [Storage — v3.2.5 精确版本绑定清单](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-storage-consistency-forget-atomicity-2026-11-16/reviews/storage-consistency/phase-3.6.15-storage-v3.2.5-protocol-bundle-exact-version-manifest.md)
