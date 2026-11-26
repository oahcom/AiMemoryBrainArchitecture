---
document_metadata:
  domain: architecture
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      evidence_reference: []
    evidence_verification:
      verification_status: Unverified
      last_verification_note: "Owner-authorized classification direction for AID-2026-11-26-GOV-DOC-01; not a formal approval record. Pre-metadata content blob: 62f5d490cb983289b93f83886d8a6109505c1650. Approval remains Draft; evidence verification remains Unverified."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Logical system component map"
    canonical_scope_id: architecture/logical-system-component-map
    canonical_scope_keywords:
      - subsystem
      - owner
      - capability
      - component-boundary
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: "01-system-architecture/component-map.md"
    en: "docs/en/01-system-architecture/component-map.md"
    zh-CN: null
---
# 逻辑系统组件图

- 文档 ID：SYS-COMP-001
- 版本：1.0
- 源规范：[项目规范性原文](../../../01-system-architecture/component-map.md)
- 对应英文：[Logical System Component Map](../../en/01-system-architecture/component-map.md)
- 状态：DECIDED（逻辑职责基线）；具体实现边界仍由详细设计决定

本图描述的是职责边界，不规定进程、服务或 Crate 的部署边界。

## 第 0 层：系统

**AI Memory Brain** —— 独立于模型和 Agent 的记忆基础设施。

## 第 1 层：子系统

### SYS-MEMORY-BRAIN —— 权威记忆

| ID | 逻辑子系统 | 主要职责 |
|---|---|---|
| MB-01 | Memory Domain Model | 规范对象语义、标识符、类型化关系、时间和认知元数据 |
| MB-02 | Canonical Memory Store | 持久化、版本历史、权威记忆读写 |
| MB-03 | Memory Lifecycle Manager | Candidate/Active/Superseded/Archive/Retract 状态转换及生命周期策略 |
| MB-04 | Entity & Relationship Manager | Entity 身份、解析、类型化关系和图一致性 |

### SYS-MEMORY-COMPILER —— 从经历形成记忆

| ID | 逻辑子系统 | 主要职责 |
|---|---|---|
| MC-01 | Event Ingestion Engine | 校验事件、确定 Scope、去重并可靠接收 |
| MC-02 | Extraction & Normalization Engine | 提取候选记忆/命题并规范化结构 |
| MC-03 | Evidence & Provenance Manager | 关联来源片段、证据、派生链路和信任元数据 |
| MC-04 | Consolidation & Conflict Resolver | 去重、合并、版本化、限定并保留冲突 Claim |

### SYS-MEMORY-RUNTIME —— 记忆服务与上下文控制

| ID | 逻辑子系统 | 主要职责 |
|---|---|---|
| MR-01 | Memory Retrieval Engine | 在结构化、词法、语义、时间和关系索引中路由查询并检索候选 |
| MR-02 | Memory Activation Policy Engine | 决定激活哪些记忆、何时激活以及为什么激活 |
| MR-03 | Memory Context Manager (MCM) | 规划、编辑、版本化、预算管理和协调有 Scope 的 Memory Context |
| MR-04 | Context Synchronization Engine | 交付 Snapshot/Delta，并跟踪 Adapter ACK 和已应用版本 |

### SYS-CROSS-CUTTING —— 横切基础设施

| ID | 逻辑子系统 | 主要职责 |
|---|---|---|
| XF-01 | Storage, Index & Cache Infrastructure | 持久化原语、索引维护、缓存和 Runtime 工作集支持 |
| XF-02 | Scope, Permission & Governance Engine | 授权、隔离、保留、遗忘和审计策略 |
| XF-03 | Protocol Gateway & Adapter Contracts | BMCP 校验、能力协商、遥测和上下文消息边界 |
| XF-04 | Consistency, Recovery & Observability | 幂等、重放、协调修复、健康状态、Tracing、Metrics 和审计关联 |

## Owner A–I 权威交叉映射

以下 Level-1 分组是逻辑聚合，不是 Owner 身份，也不意味着一对一归属。Owner 命名空间仅指 A–I：

| 逻辑分组 | 主责 Owner 权威 | 协作 Owner | 权威边界 |
|---|---|---|---|
| SYS-MEMORY-BRAIN | B 负责领域语义；D 负责 Canonical Memory 身份、持久化/生命周期及 Forget Fence；I 负责全局策略 | E、F、G 按各自流程参与 | 聚合分组没有唯一 Owner。B 定义领域含义；D 拥有规范记忆机制；I 拥有授权、Retention/Legal Hold、外部副本策略及全局完成标准。 |
| SYS-MEMORY-COMPILER | E | B、D、I | E 负责接收/编译及派生物生产；B 负责语义定义；D 控制 Canonical 接纳和生命周期；I 控制授权与策略。 |
| SYS-MEMORY-RUNTIME | F 负责检索/激活；G 负责 Memory Context 权威 | B、D、C、H | F 负责检索/激活；G 负责 Context 语义/版本；D 仍是 Canonical 来源；C 在 Agent 推理边界应用；H 拥有 BMCP Wire/协议语义。 |
| SYS-CROSS-CUTTING | I 负责全局安全/治理策略；H 负责 BMCP 协议；C 负责 Agent 侧集成 | A、B、C、D、E、F、G、H、I 按具体契约参与 | Storage/Consistency 执行职责按契约共享，不虚构聚合 Owner。Owner A 保留跨系统集成/冲突协调权。 |

子系统 ID（例如 MB-01、MC-01、MR-01、XF-01）仅标识逻辑组件，不是 Owner ID。

## 外部参与者

| 参与者 | 自身职责 | 不委托给 Brain 的职责 |
|---|---|---|
| Agent | 推理、规划、行动选择、工具执行 | Brain 不成为它的规划器或执行器 |
| LLM / Inference Runtime | 模型推理和 Token 处理 | Brain 不拥有模型内部机制 |
| Agent Adapter | 映射遥测，并在推理边界应用上下文 | Adapter 不重新定义 Brain 记忆策略 |
| Environment Adapter | 环境事件和状态观察 | Brain 不直接控制或驱动环境 |
| Skill Library | 可执行技能和流程 | Memory 记录经历，不会自动成为可执行代码 |

## 主要关系

- Event Ingestion 写入可靠事件，并向 Compiler 发出已接收事件引用。
- Compiler 通过 Brain 所有的领域和生命周期契约创建候选记忆资产。
- Evidence/Provenance 将每项派生资产关联到其来源。
- Consolidation 更新权威资产，并为索引和 Runtime 协调发布变更事件。
- Retrieval 向 Activation 和 Context Planning 提供候选记忆。
- Activation Policy 评估任务/遥测信号，并请求上下文变更。
- MCM 对每个受管 Context 的版本序列拥有权威性。
- Context Synchronization 传输 Snapshot/Delta，并记录 Adapter ACK。
- Governance 约束事件接收、读取、修改、同步、保留和遗忘。
- Consistency/Recovery 在子系统边界之间协调 Replay、Idempotency、修复和可观测性。

## 架构注意事项

上述 16 个逻辑组件是职责地图，不意味着必须创建 16 个可独立部署的单元。详细设计可以合并或拆分实现模块，但必须保留职责归属和架构不变量。

## Owner 引用命名空间与引用规则

- 正式责任归属必须使用明确形式 `Owner A` 至 `Owner I`。单独字母（A–I）不构成 Owner 引用。
- 逻辑子系统必须使用其 `SYS-*` 标识（例如 `SYS-MEMORY-COMPILER`）；不得用单独字母引用子系统。
- Responsibility Matrix 的能力/组件标签及 P/S 参与标记属于独立分类，不代表负责的 Owner。
- 同一句话需要同时引用子系统和 Owner 时，必须分别明确写出（例如“SYS-MEMORY-COMPILER；负责 Owner E”），不得相互推断。
- 自动检查由 AID-2026-081 / Issue #1237 单独跟踪。在该检查合并前，本节只是人工引用规则，不代表 lint 门禁已经存在。
