---
document_metadata:
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-193/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：Status: DECIDED quality priorities and measurement principles）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：1c7ea192fa653f789aafa5e04559ad259b05884d。"
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: "01-system-architecture/system-quality-attributes.md"
    en: "docs/en/01-system-architecture/system-quality-attributes.md"
    zh-CN: null
---
# 系统质量属性

- 文档 ID：SYS-QA-001
- 版本：1.0
- 源规范：[规范性原文](../../../01-system-architecture/system-quality-attributes.md)
- 源版本： c939ee0f6c7b29a6b51421fbfe3fe89d68ae9f6f
- 对应英文：[System Quality Attributes](../../en/01-system-architecture/system-quality-attributes.md)
- 状态：质量优先级和测量原则为 DECIDED；架构策略为 CANDIDATE；量化目标为 TO_VALIDATE

**范围：** 定义系统级质量模型和验证计划。本文不宣称任何未经测量的性能，也不规定部署拓扑。

## 1. 质量模型

必须在真实 Agent 工作流中评估本系统作为记忆基础设施的质量，而不只是运行向量搜索基准。质量属性之间存在相互影响：更强的来源链和授权检查可能增加延迟；激进缓存可以降低延迟，却可能增加陈旧数据风险；更大的上下文可以提升覆盖率，却会消耗 Token 并分散 Agent 注意力。

优先级属性：
1. 正确性与认知完整性。
2. Scope 隔离、授权与隐私。
3. Canonical/Context 一致性和可恢复性。
4. 来源链完整性与受治理遗忘。
5. 延迟可预测性和资源有界性。
6. Adapter 互操作性与可演进性。
7. 可用性与故障隔离。
8. 有用的记忆激活和可测量的 Agent 层面收益。
9. 可运维性、可观测性和可测试性。

## 2. 质量属性场景

| 属性 | 触发条件 | 必须的响应 | 测量/证据 |
|---|---|---|---|
| 语义正确性 | Agent 提交计划、预测、观察或结果 | 保留认知区别；不能仅凭计划生成已完成事实 | 对抗测试/属性测试；错误结果率 |
| 来源链完整性 | Compiler 派生或压缩记忆 | 每条派生命题都能追溯到来源证据，或明确记录来源链缺口 | 来源链覆盖率；血缘遍历测试 |
| 隔离 | Principal 查询其他 User/Agent/Environment Scope | 在受保护数据影响结果或上下文之前拒绝 | 跨租户/Agent/Environment 渗透测试 |
| Context 一致性 | 并发编辑或增量丢失 | 只有一条权威版本序列；拒绝/协调过期 Base；通过 Snapshot 修复缺口 | 版本不变量测试；协调成功率 |
| Applied 正确性 | 推理进行期间 Adapter 收到上下文变更 | 仅在后续组装边界应用；确认准确版本 | Instrumented Adapter 边界测试 |
| Forget | 已授权 Forget 指向权威记忆和派生物 | 先抑制访问，再分阶段清理；不得过早声称完成 | 抑制耗时、派生物覆盖率、备份策略审计 |
| 接收持久性 | 提交 Event 时 Storage/Compiler/模型故障 | Accepted 必须代表已持久化；下游故障不能丢失已接收 Event | 崩溃注入和重放 |
| Recall 响应性 | Agent 在负载下发起有界 Recall | 在声明预算内返回已授权候选，或明确超时/部分结果 | p50/p95/p99 延迟、超时率和部分结果率 |
| 资源有界性 | 大语料或遥测突发 | 强制执行接收、候选数量、图深度、缓存和队列限制 | CPU/RAM/VRAM/磁盘、队列深度、过载测试 |
| 互操作性 | 新 Agent/LLM 实现接入 | 通过 Adapter 能力等级使用稳定的 Brain 契约 | 多个独立 Adapter 的一致性测试 |
| 可演进性 | Protocol/Schema 增加可选能力 | 版本协商并保持向后兼容，或明确拒绝 | 兼容性矩阵测试 |
| 可用性 | 一个逻辑子系统不可用 | 故障被隔离；其他无关持久数据和权威保持完整 | 故障注入和依赖隔离测试 |
| 实用价值 | 记忆激活改变 Agent 任务表现 | 必须对照基线测量收益或退化，不能假设 | 受控 Agent 任务评估 |

## 3. 系统质量预算

在工作负载和硬件基线确定之前，数值预算保持 **OPEN**。下表是必须纳入的预算维度，不是已经确定的目标值。

| 维度 | 指标 | 分层方式 |
|---|---|---|
| Ingestion | 接收延迟、持久化提交延迟、拒绝/背压率 | Payload 大小、来源、并发写入者 |
| Compilation | 队列等待时间、阶段耗时、重试次数、达到 Canonical 的耗时 | 确定性阶段与模型辅助阶段；模型可用性 |
| Recall | 端到端/各阶段延迟、超时/部分结果率、候选数量 | 热/冷缓存、语料规模、查询类型、Scope 数量 |
| Activation | 从遥测到决策的延迟、误激活、漏掉相关记忆 | 任务类别、风险类别、Adapter 等级 |
| Context | 规划/编辑/提交延迟、版本冲突率、Token/字节预算使用率 | Context 大小、编辑类型、并发 Session |
| Synchronization | Delivery 延迟、Applied 滞后、重试次数、Snapshot 频率、版本缺口率 | Adapter 在线/离线、Delta 大小、网络条件 |
| Governance | 授权延迟、Forget 到访问抑制耗时、策略完成耗时 | 派生物数量、备份策略、Scope 大小 |
| Resources | CPU、RAM、磁盘 IO/容量、GPU/VRAM、网络 | 本地硬件配置、并发、模型启用/禁用 |
| Quality | 有用记忆 Precision/Recall、不受支持命题率、来源链覆盖率、冲突保留情况 | 已标注工作负载和评估集 |
| Agent outcome | 任务成功率、工具/行动错误、恢复时间、重复提问率、上下文 Token 开销 | 任务/环境/Agent/LLM 分组 |

## 4. 性能与评估方法

### 4.1 可复现基准测试声明

每项测试结果必须包含：
- 硬件：CPU、物理内存、GPU 型号/VRAM、存储类型、操作系统/运行时。
- 软件版本、配置，以及使用时的模型和量化方式。
- 语料规模和 Event/Memory/Claim/Entity 数量；Payload 平均大小和尾部大小。
- Scope 分布、Agent Instance 数量和并发 Session 数。
- 查询组合：结构化、词法、语义、时间、关系、混合。
- 缓存状态和预热流程。
- 并发数、到达速率、突发模式和持续时间。
- 正确性数据集和 Ground Truth 标注方法。
- 百分位计算方式、样本量，以及适用时的置信区间。

除非在相同工作负载和正确性标准下完成可复现比较，否则不得接受任何性能倍数或性能优势声明。

### 4.2 必需对照基线

比较以下方案：
1. 无记忆 / Agent 原生基线。
2. 简单检索基线（例如词法或仅 Embedding），在适用时使用。
3. 不包含激活的 Brain Retrieval。
4. 加入 Activation/Context 管理的 Brain Retrieval。
5. 模型辅助 Compilation 与纯确定性流水线的对比。

这些是评估基线，不是技术选型承诺。比较时必须考虑新增 Prompt Token、检索延迟和误激活。

### 4.3 质量指标

建议定义：
- **有用记忆 Precision：** 在已标注的任务上下文判断下，相关激活条目数 / 全部激活条目数。
- **有用记忆 Recall：** 相关激活条目数 / 所有被判断为相关且符合条件的条目数。
- **无依据命题率：** 激活的命题缺少所需 Evidence/Provenance，或超出了来源认知状态。
- **Scope 泄漏率：** 未授权 Scope 中泄露的受保护记录；安全测试目标为零。
- **版本正确率：** 确认与目标 Context/Version 完全一致的比例；无效 Applied 声明目标为零。
- **陈旧数据暴露：** 返回候选的来源代数早于所需一致性 Fence。
- **Forget 抑制延迟：** 从 Forget Fence 持久化到拒绝目标数据读取/激活的时间。
- **Agent 层面实用价值：** 相对于声明基线的成对任务成功率/错误指标，附带置信区间和任务分层。

在解释质量分数之前，评估标签和裁定流程仍为 **OPEN**，必须先行定义。

## 5. 可用性与故障隔离

**DECIDED：** 逻辑组件故障不得静默破坏其他组件的权威状态。

必须满足：
- Event 接收不依赖模型推理服务可用。
- Compiler Backlog 必须持久化且有界；过载时执行接收控制。
- Canonical Store 故障时，不得声称 Canonical 写入成功。
- Index/cache 故障必须表现为可检测的降级或安全回退；次级结构可重建。
- Retrieval 超时不得修改 Context。
- MCM 故障必须保留最后一次提交的 Context Version。
- Sync/Adapter 故障只会延迟应用，不得改变 Applied 状态。
- Forget 必须具有持久化任务/Fence 和可恢复的逐目标进度。
- Governance 授权失败时，受保护读写必须 Fail-closed。
- 可观测性故障不得违反强制审计义务；具体 Fail-open/Fail-closed 类别仍为 OPEN。

可用性 SLO 和恢复目标（RTO/RPO）依赖工作负载及部署假设；架构阶段不得虚构数值。

## 6. 安全与隐私质量

必须具备以下控制：
- 对来源 Principal 和 Adapter 进行认证。
- 每项操作都独立于 Scope，依据 Permission 进行授权。
- 在查询和修改边界执行 Tenant/User/Agent/Session/Environment 分区。
- 将来源文本、遥测、观察和检索记忆视为不可信数据。
- 明确分隔记忆区域，并使其从属于 System/Developer 指令、用户输入和 Agent 安全策略。
- 最小化遥测采集；不要求完整隐藏 CoT。
- 从日志和指标中脱敏敏感 Payload。
- 按声明策略将 Forget 传播到权威数据和适用派生物。
- 审计管理操作和高影响操作，同时避免不必要地保留已擦除内容。

验证包括威胁建模、负向授权测试、Prompt Injection 测试样例、数据流审查、保留/擦除审计，以及 Secret/Log 扫描。

## 7. 互操作性与可演进性

**DECIDED：** Brain 契约独立于 Agent 和模型；集成差异由 Adapter 映射和能力协商处理。

测试应覆盖：
- 一个 Tier 1 推理边界 Adapter。
- 一个 Tier 2 Middleware Adapter。
- 一个 Tier 3 Event/Recall 集成。
- 在可行时，至少一个 Adapter 后接入多个 LLM Provider。
- 未知可选字段、不支持的操作、版本不匹配和降级路径。

Adapter 必须声明自身限制；Brain 不得暗示超出该能力等级的保证。具体等级定义由 Agent Integration/BMCP 规范负责。

## 8. 资源效率与 Local-first 运行

分别测量 CPU、RAM、磁盘 IO、存储增长、GPU/VRAM 和网络。每次实验都必须声明本地目标硬件配置。可选的模型辅助处理必须与确定性接收和检索路径隔离。

**CANDIDATE：** 在接收控制、Compiler 调度、Retrieval 候选扩展、Context Token/字节规划和缓存大小等边界实施资源预算。

**TO_VALIDATE：** 在目标 12–16 GB VRAM 系统上，模型辅助 Compilation 的可行性和吞吐能力。基准测试前不作任何性能声明。

## 9. 可观测性要求

每个跨组件操作都应通过 Correlation/Causation ID 追踪，并暴露：
- Request/Event/Context/Delivery 标识符（适当脱敏）。
- 组件和阶段、结果/错误类别、尝试次数。
- 队列等待时间和阶段耗时。
- Canonical/Index 代数以及 Context Base/Target/Applied Version。
- 不泄露敏感标识符的 Scope 类别。
- 资源使用和饱和情况。
- 在安全前提下的策略决策和拒绝原因代码。

日志、指标和 Trace 不能替代领域 Evidence 或 Provenance。

## 10. 验证策略

| 测试层级 | 关注点 | 示例 |
|---|---|---|
| Contract | Schema、状态、所有权、兼容性 | Adapter 一致性测试和无效 Payload 拒绝 |
| Invariant/property | 不可妥协的语义 | 无 ACK 不得 Applied；不得把 Plan 提升为 Outcome |
| Integration | 跨组件顺序 | Event Accepted → Compiled → Canonical → Indexed |
| Concurrency | 竞争和版本安全 | Canonical/Context 并发编辑 |
| Fault injection | 恢复与隔离 | 在每个提交边界终止 Compiler/Index/Sync |
| Security | 隔离、授权、注入 | 跨 Scope Recall 和恶意记忆 Payload |
| Performance | 延迟、吞吐、资源边界 | 混合负载 p50/p95/p99 |
| Agent task | 端到端实用价值 | 有记忆与无记忆的多会话任务 |
| Governance | Forget/Retention | 派生物清理和备份过期 |

## 11. 验收标准

1. 上述所有质量场景都有可执行测试或有记录的人工验证流程。
2. 定义的对抗测试集中不得发生跨 Scope 信息泄露。
3. Event 尚未可靠提交时不得生成虚假的 Accepted Receipt。
4. 已标注的 Plan/Outcome 测试样例中不得提升无依据命题。
5. Adapter 一致性测试中不得出现无效 Applied ACK。
6. 不得静默推进存在缺口的 Context Version。
7. Index/cache 丢失并重建后，Canonical 状态仍然正确。
8. 在所需目标尚未完成，或未被明确记录为策略豁免残余项之前，Forget 不得报告策略完成。
9. 所有性能数字都必须包含 §4.1 的基准声明。
10. Agent 实用价值报告必须包含基线、任务分层、Token 开销和不确定性。
11. 资源过载必须产生有界行为，并明确执行背压/降级。
12. Protocol 演进测试必须验证支持和不支持的能力路径。

## 12. 开放问题与验证待办

| ID | 状态 | 优先级 | 问题 |
|---|---|---|---|
| QA-01 | OPEN | 高 | 定义具有代表性的 Agent 工作负载和基准语料。 |
| QA-02 | TO_VALIDATE | 高 | 在声明的硬件上建立 Recall 和 Context 应用的 p50/p95/p99 目标。 |
| QA-03 | OPEN | 高 | 为目标部署模式定义 RTO/RPO 和审计可用性要求。 |
| QA-04 | TO_VALIDATE | 高 | 相比简单检索基线，测量有用记忆 Precision/Recall 和 Agent 层面收益。 |
| QA-05 | TO_VALIDATE | 中 | 确定本地 GPU 配置下模型辅助 Compilation 的资源范围。 |
| QA-06 | OPEN | 中 | 定义评估标签裁定和置信区间方法。 |
| QA-07 | OPEN | 中 | 定义 Forget 完成和备份/副本残余项报告。 |
| QA-08 | OPEN | 中 | 定义 Adapter 等级的一致性覆盖范围和兼容性支持周期。 |

## 13. 决策摘要

- **DECIDED：** 正确性、来源链、隔离、上下文一致性、受治理遗忘和可测量的 Agent 实用价值都是一等质量属性。
- **DECIDED：** 性能声明必须基于可复现工作负载和硬件声明；不预设任何性能倍数。
- **DECIDED：** 故障隔离必须保护 Canonical 权威并明确暴露降级状态。
- **CANDIDATE：** 在 Ingress、Compiler、Retrieval、Context 和 Cache 边界执行预算。
- **TO_VALIDATE：** 延迟/吞吐/资源量化目标、模型辅助 Compilation 可行性和 Agent 层面收益。
- **OPEN：** 工作负载语料、SLO/RTO/RPO、评估标签和备份擦除语义。
