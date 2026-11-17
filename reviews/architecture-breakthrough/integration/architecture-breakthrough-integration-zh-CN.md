# 架构突破研究统一集成与交叉审查决议（中文）

- Review ID: ABR-INTEGRATION-001
- 状态：**研究集成结论；非 Owner 批准、非 ADR、非架构冻结**
- 基线：`main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- 集成分支：`review/architecture-breakthrough-integration-2026-11-18`
- 输入研究：PR #84（Session 0）、#88（A / Forget）、#86（B / Memory OS）、#85（C / Memory IR）
- 治理依据：Issue #43
- 范围：只审查 A/B/C 四份研究之间的基线、证据、架构边界与组合影响；不替代 Issue #43 的全系统 A–I + Storage 集成验收。

## 1. 执行结论

本轮研究**没有证明新架构优于当前架构**，也没有证明 Forget 已达到生产安全要求。可支持的集成结论如下：

| 主题 | 集成判定 | 可执行结论 |
|---|---|---|
| Forget formal verification | **P0 / NOT READY** | 继续以跨 D/E/I/Storage 的原子发布与恢复安全为首要验证目标；扩展模型并将逻辑模型映射到 Owner 合同和物理测试 |
| Memory Resource Manager | **CANDIDATE / SHADOW ONLY** | 只允许研究一个 Runtime 内部资源控制平面；不得合并 F Retrieval/Activation 与 G Context 语义，不得成为权限或 Forget 权威 |
| Memory IR | **CANDIDATE / SHADOW ONLY** | 只允许研究 E 内部的版本化类型化 Stage Contract；不得替代 D Canonical Commit，不得决定 B Fact/Claim |
| 完整架构优越性 | **UNRESOLVED** | 当前无同工作负载、同安全条件下的端到端对照数据 |
| 架构冻结 | **NOT READY（本研究范围）** | 本集成研究不构成 Issue #43 G1–G8 通过，也不关闭任何既有 P0 / ADR blocker |

推荐顺序：**先补强 Forget 模型与跨模块契约证据；并行准备 B/C 的影子实验设计；只有实验显示净收益且 Owner 接受后，才考虑进入架构决策。**

## 2. 精确基线与版本关系

### 2.1 当前 main

实时比较 `e52594f... ↔ main` 的结果为 `identical`，因此当前 main HEAD 确认为：

`e52594f181d2edb77448adcfed64a0fbdffaf3aa`

`b3c666e67982cb3d3374e759cfb6552c7765aacb → e52594f...` 显示 2 commits ahead、0 behind、0 changed files。它是历史提交差异，不构成已证实的树内容差异。

### 2.2 四个研究 PR

| PR | 角色 | Head SHA | PR 记录的 base SHA | 相对当前 main 的比较 |
|---|---|---|---|---|
| #84 | Session 0 总协调 | `c6e76b34cbf099d36631b284c9b8a75d778d707f` | `28fb37e21fa4ba2b871f7816fe669128618c063e` | diverged；merge-base 为 28fb37e；main 比报告基线多一个历史提交 |
| #85 | C / Memory IR | `c5013d3585d54457f38bef37984645e2055ff7cf` | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | diverged；merge-base 为 b3c666e |
| #86 | B / Memory OS | `3892916ce2379f807a0ddcd0039816f6e88ecee1` | `b3c666e67982cb3d3374e759cfb6552c7765aacb` | diverged；merge-base 为 b3c666e |
| #88 | A / Forget | `bf35b32295d0d3f337c80c3dc406db0a41de6830` | `e52594f181d2edb77448adcfed64a0fbdffaf3aa` | diverged；merge-base 为 b3c666e |

重要解释：
- 四个 PR 均保持 Open / Draft / Unmerged；PR 可合并状态不是架构批准。
- #84 报告正文仍将 `28fb37e...` 写作基线；#85/#86/#88 的报告或 PR 正文主要引用 `b3c666e...`。本集成报告以当前 main 的 `e52594f...` 为统一审查锚点。
- #88 与当前 main 的历史 diverged 是真实的。不能直接合并、不能通过改 base 字段伪装成同一历史。
- 但 `b3c666e...` 与 `e52594f...` 的文件比较为零差异，因此可以把研究结论作内容层面的共同基线审查；仍须保留历史分叉披露。
- 不重定向、不更新、不合并四个研究 PR；不修改 main 或 Owner 分支。

## 3. 证据等级与独立性

本报告区分：
1. **规范/Owner 合同**：只有对应 Owner 的精确版本和明确决议才有规范效力。
2. **研究报告**：可供集成判断，不自动成为规范。
3. **模型/原型结果**：只证明其抽象、输入和范围内的行为。
4. **物理/生产证据**：真实数据库、HA、崩溃、恢复、服务和 Adapter 验证；本轮没有新增此类证据。
5. **Owner 接受**：必须由对应权限主体对精确版本明确确认，不能由本会话角色模拟代替。

本次交叉审查由同一个助手会话承担多视角检查，**不是组织意义上的独立 Owner 审批或第三方独立审查**。本报告不得被用作 B/D/E/F/G/H/I/Storage 的签字。

## 4. A — Forget：证据与跨工作流交叉审查

### 4.1 已支持的结论

PR #88 的 Python explicit-state BFS 报告：安全规则抽象在深度 10 内探索 606 个状态/深度组合，没有发现模型内不变量违反。五种削弱关键 guard 的变体产生最短反例：
- 旧 Worker：admit → install_fence → publish
- Admission 竞态：install_fence → admit
- Index rebuild：admit → publish → install_fence → rebuild_index
- Cache refill：admit → publish → install_fence → repopulate_cache
- Stale restore：install_fence → restore

这些反例来自 mutant / weakened-guard 模型，不是生产故障日志，也不是安全模型本身发现五个漏洞。

A 报告明确将生产结论判为 **NOT READY**。F1/F2/F5/F7 仅在有限抽象模型内有条件成立；F3 跨模块证明不完整；F4/F8 未证明；F6 仅局部闭合。

### 4.2 与 B Resource Manager 的交叉约束

Resource Manager 不得：
- 将公平调度、任务优先级、预算预留解释为授权；
- 绕过 I Permission、D ForgetFence、Scope、Security 或 Freshness hard gate；
- 让旧 Reservation 跨 PermissionEpoch / ForgetFenceGeneration 继续有效；
- 以回收、重试、重新调度为由重新暴露已抑制的内容。

必须满足：
- 资源决策只回答容量/排队/预算，不产生访问权；
- F/G 在受保护读取、Context Commit、Delivery 的既有边界重新验证授权与 Fence；
- 资源管理器不可用或控制状态未知时，对受保护任务 fail closed；
- Reservation 携带类型化控制版本引用，但不得跨 epoch namespace 比较。

### 4.3 与 C Memory IR 的交叉约束

IR/Compiler 不得：
- 将模型抽取或 IR validation 结果视为 Canonical Truth；
- 在 Derived Dependency Registration 未持久完成、Fence/Permission 未最终验证前发布派生物；
- 复用历史 Forget receipt / Permission outcome 作为新 DerivationRun 的发布授权；
- 通过增量编译缓存恢复已被 Forget 抑制的派生物。

必须满足：
- source version/digest、transform version、provenance 与 lineage 完整；
- 每次新 DerivationRun 都重新满足当前 admission、dependency registration、Forget/Permission 和 publication gate；
- 旧 Worker、旧 IR、旧 cache 只能作为不可见候选或审计材料，不能越过最终披露门。

### 4.4 A 的 P0 关闭项

1. D + Storage：ProducerWork registration、Fence high-water capture、最终 lineage/Fence validation、VisibilityPointer + PublicationReceipt 的原子排序域。
2. I：Producer/Recipient/Backup/External-copy inventory 的权威来源、epoch/seal、join/leave/change 失效规则和 Global Forget completion。
3. E：Derived Registration 与 publication 的精确 Owner 合同；完整依赖集必须在可见前持久化。
4. Storage + I：JF-10 跨权威崩溃原子耦合和恢复语义。
5. F/G/H：检索最终披露、Context/Applied、Adapter reconnect 的 Fence 端到端验证。
6. Storage/I/D：Restore control high-water 不可随旧备份回滚的物理证明。

**A 决议：优先级 P0；模型结果只能作为 bounded logical evidence。生产实现不得以本模型结果为放行依据。**

## 5. B — Memory Resource Manager：交叉审查

### 5.1 保留的候选价值

PR #86 提出的 Option B 比完整 Memory OS 内核更克制：一个 Runtime 内部的共享资源控制平面，统一资源账本、层级预算、reservation、fair scheduling 和 reclaim，同时保留 F/G 领域语义。

合成实验（30 tasks、720 candidates、9,000-token budget）：
- Direct Top-K：Recall 0.5333；Precision 0.4741；Jain fairness 0.8325；1 task starvation。
- Rerank + Budget：Recall 0.5417；Precision 0.2863；Jain 0.8141；无 starvation。
- Unified RM：Recall 0.5083；Precision 0.2699；Jain 0.8554；无 starvation。
- Unified RM local selection latency median 0.324 ms，Direct Top-K 为 0.099 ms。

因此该实验显示公平性与无饥饿改善，但 Recall/Precision 下降、局部选择延迟增加。它**不能**支持“Unified RM 全面优于现状”的结论。

### 5.2 集成约束

- Retrieval 与 Activation 继续分离。
- F Working Set / Cache 是可丢弃 Runtime View；G Context 是版本化、受治理的推理区域。
- Context token/byte budget 是语义约束，不等同于 RAM/cache 容量。
- Applied Context 是 Adapter 侧证据，不是 Residency。
- Canonical Memory 绝不能进入 eviction。
- 不建立全局持久化 Residency lifecycle。
- Resource Manager 是调度与容量协调者，不是新服务，不是新的 Security/Forget/Canonical Authority。

### 5.3 建议实验门槛

先做 Shadow Mode，不改变任何线上/规范行为；使用同一真实任务集与同一硬安全过滤器，对比分散预算与统一账本：
- Recall / Precision / nDCG / Sufficiency；
- p50/p95/p99 latency；
- token waste、RAM/VRAM peak、cache hit/miss；
- task starvation、Jain fairness、跨 Principal 公平性；
- cancellation、deadline miss、partial result；
- Forget / Permission revocation 后旧 Reservation 被拒绝的延迟与比例。

实验必须预先定义 workload、随机种子、统计方法、基线、停止条件和失败回滚。合成数据仅作为算法 sanity check。

**B 决议：Option B 保持 CANDIDATE；Option C（完整 Memory OS 内核）不推荐。没有 Shadow Mode 和 Owner 接受前不进入架构规范。**

## 6. C — Memory IR：交叉审查

### 6.1 保留的候选价值

PR #85 提议在 E 现有 Compiler 内引入 Shadow Typed IR，而不是重写 Compiler 或新建 Compiler Service。它试图稳定阶段间类型、来源、证据角色、Scope、时间/认知限定、转换版本和 Provenance。

现有 E 已有 durable acceptance、work item、deterministic normalization、optional model extraction、Evidence/Provenance、candidate/conflict proposals 和 D-owned canonical commit。IR 应减少阶段 DTO 的转换歧义，不应复制这些已有职责。

### 6.2 关键交叉约束

- **B Fact/Claim ADR 保持 ADR-BLOCKED。** 使用中性候选词汇（如 AssertionCandidate / opaque proposal）；不得冻结 Fact/Claim canonical identity、storage schema 或 wire discriminant。
- **D 继续拥有 Canonical Commit。** IR 只产生候选和验证报告，不能直接写 canonical store。
- **E 继续拥有 Compiler orchestration。** Shadow IR 是内部 stage contract，不是独立服务/平台。
- **Forget/Permission 先于发布。** 新 derivation 必须有新的 admission、dependency registration 与最终 publication gate；不得复用旧授权。
- **Provenance 不可被优化丢弃。** Semantic-preserving optimization 必须记录输入/输出 digest、transform version 和父 lineage。
- **版本兼容必须显式。** ir_version/schema_digest/parser/extractor/model/policy/transform versions 共同影响 derivation fingerprint；未知版本 fail closed 或 quarantine。
- **增量重编必须确定。** 输入或 pass 版本变化时，只重编受影响 lineage；不得把旧 cache 命中视为当前有效性证明。

### 6.3 证据限制

PR #85 的原型是标准库 Python 与合成 fixture；报告指出 5 input rows、4 valid candidates、1 conflict proposal、deterministic replay、incremental fixture 中 3/3 unchanged source-node IDs。它没有验证 LLM 行为、实体解析、并发、崩溃恢复、Forget、授权、canonical commit 或生产缓存。

Direct-vs-IR 的有限原型结果不能证明生产系统复杂度下降，也不能证明类型系统在真实数据上更准确。

**C 决议：Shadow Typed IR 保持 CANDIDATE；只允许在 E 内部做非权威影子试验。不得修改 B ADR、D Canonical Commit 或生产 Pipeline。**

## 7. Session 0 总协调结论复核

Session 0 的三项研究方向与 A/B/C 原始报告基本一致，但应按以下方式修订其证据标签：

1. TLA+ / Alloy：工具选择为 CANDIDATE；Session 0 的 TLA+ skeleton 未运行 TLC。A 的 Python BFS 是另一份 bounded model evidence，不能混称为 TLC 结果。
2. Resource Manager Option B：候选，且实验结果有质量/延迟 trade-off；不应表述为已证实的复杂度减少。
3. Shadow Typed IR：候选，尚未达到正式采用门槛；Fact/Claim ADR 仍阻断。
4. “新架构是否优于现有架构”：UNRESOLVED。
5. L1 Storage topology：Session 0 报告引用 Storage topology ADR 中已 DECIDED 的单一 Serializable Transaction Domain / CanonicalAuthoritySerializationAnchor；本研究不重开该决定，也不将研究建议视为对其物理实现的证明。L4 数据库/HA/恢复能力仍需独立证据。

## 8. 冲突与风险登记

| ID | 严重度 | 风险 / 歧义 | 责任权威 | 状态 |
|---|---|---|---|---|
| INT-01 | P0 | Producer Registration / Fence / Dependency Registration / Visibility Commit 原子顺序未证明 | D/E/Storage | OPEN |
| INT-02 | P0 | Producer/Recipient/Backup/External copy inventory 完整性及 Global Forget completion 未证明 | I | OPEN |
| INT-03 | P0 | JF-10 跨 I sequencer 与 Storage visibility 的 crash atomicity 未证明 | I/Storage | OPEN |
| INT-04 | P0 | Restore 后控制高水位不回滚的物理证据缺失 | Storage/I/D | OPEN |
| INT-05 | P1 | F/G/H 最终披露、Applied、Adapter reconnect 对 Fence 的一致执行未验证 | F/G/H | OPEN |
| INT-06 | P1 | Resource Manager 可能把调度决策误用为授权或使旧 Reservation 跨 epoch 生效 | F/G + I/D | MITIGATION REQUIRED |
| INT-07 | P1 | IR 可能提前固化 B Fact/Claim 语义或绕过 D Commit / Forget registration | E + B/D | MITIGATION REQUIRED |
| INT-08 | P1 | 研究报告使用不同历史 base；source pins 需在每个 Owner 当前 HEAD 再刷新 | Integration / A | PARTIALLY RESOLVED |
| INT-09 | P1 | B 实验显示公平性收益但 Recall/Precision/latency 退化 | B + F/G | TO_VALIDATE |
| INT-10 | P1 | C 原型范围小，无法证明生产增益、并发/恢复正确性 | C + E | TO_VALIDATE |
| INT-11 | P2 | Session 0 TLA+ skeleton 与 A Python BFS 的验证对象/覆盖不同，易被混称 | Integration | CLARIFIED |

## 9. 研究决策与禁止推断

### DECIDED（仅本集成报告的审查结论）
- 当前 main 审查锚点为 `e52594f...`。
- 四份研究均为 Draft/非规范提案，不自动产生架构批准。
- Forget 的跨模块生产安全尚未证明。
- B/C 不得改变现有 Owner 权威边界。
- B/C 均须先进行影子实验并获得对应 Owner 接受。
- 本研究不关闭 Issue #43 任一 gate 或 P0 blocker。

### CANDIDATE
- TLA+ 作为 Forget 并发状态模型主工具；Alloy 作为关系约束补充。
- Runtime 内部 Resource Manager Option B。
- E 内部 Shadow Typed IR。

### UNRESOLVED / ADR-BLOCKED
- 新架构相对当前架构的整体优越性。
- B Resource Manager 在真实工作负载下的净收益。
- C IR 在真实数据/完整 E Pipeline 下的净收益。
- B Fact/Claim ADR。
- Forget P0 与 JF-10/物理恢复证明。

### 明确禁止的推断
- 不得将 bounded model pass 等同于无界形式证明或生产安全。
- 不得将合成 benchmark 等同于真实用户收益。
- 不得将原型可运行等同于生产实现可行。
- 不得将本会话模拟多 Owner 视角等同于独立 Owner 签字。
- 不得将 PR Draft、mergeable 或报告存在等同于批准。

## 10. 下一步执行顺序

1. **A / P0：** 扩展 Forget 模型：Producer/Recipient inventory epoch、Admission/Fence/Dependency/Publish、Lease/Attempt、DLQ/Replay、lost ACK、PermissionEpoch、Index/Context/Adapter、Restore high-water。明确每个变量归属的 authority namespace。
2. **D/E/Storage/I：** 对 INT-01 至 INT-04 提供精确合同和物理验证计划；未获得 Owner 接受前保持 BLOCKED。
3. **F/G/H：** 给出受保护读取、Context Commit、Delivery、Applied、Reconnect 的 Fence 检查矩阵和未知状态行为。
4. **B：** 准备 Shadow Mode workload、metric、实验预注册和回滚方案；不写规范、不改 Runtime。
5. **C：** 准备 20–50 条代表性经历的 IR shadow corpus、schema evolution 和 deterministic replay 测试；Fact/Claim 继续使用中性候选词汇。
6. **集成复审：** 逐 Owner 当前 HEAD 重新 pin exact branch/commit/path/blob，并收集明确的 Consumer Acceptance；再决定是否形成正式 ADR。

## 11. 结论

**整体判定：READY FOR FOCUSED RESEARCH / NOT READY FOR ARCHITECTURE FREEZE OR PRODUCTION IMPLEMENTATION。**

当前最值得做的不是把 Memory OS、Compiler、Forget 再抽象出更大的统一概念，而是用最小、可执行、可反驳的证据解决跨权威的关键安全顺序。B/C 的潜在简化必须服从这条安全主线，而不是增加新的权威层。

本报告是集成审查交付，不是 Owner 签字，不是架构 ADR，不是生产验收。
