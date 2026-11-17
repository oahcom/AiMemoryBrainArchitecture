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

### A. Memory Brain —— 权威记忆

| ID | 逻辑子系统 | 主要职责 |
|---|---|---|
| MB-01 | Memory Domain Model | 规范对象语义、标识符、类型化关系、时间和认知元数据 |
| MB-02 | Canonical Memory Store | 持久化、版本历史、权威记忆读写 |
| MB-03 | Memory Lifecycle Manager | Candidate/Active/Superseded/Archive/Retract 状态转换及生命周期策略 |
| MB-04 | Entity & Relationship Manager | Entity 身份、解析、类型化关系和图一致性 |

### B. Memory Compiler —— 从经历形成记忆

| ID | 逻辑子系统 | 主要职责 |
|---|---|---|
| MC-01 | Event Ingestion Engine | 校验事件、确定 Scope、去重并可靠接收 |
| MC-02 | Extraction & Normalization Engine | 提取候选记忆/命题并规范化结构 |
| MC-03 | Evidence & Provenance Manager | 关联来源片段、证据、派生链路和信任元数据 |
| MC-04 | Consolidation & Conflict Resolver | 去重、合并、版本化、限定并保留冲突 Claim |

### C. Memory Runtime —— 记忆服务与上下文控制

| ID | 逻辑子系统 | 主要职责 |
|---|---|---|
| MR-01 | Memory Retrieval Engine | 在结构化、词法、语义、时间和关系索引中路由查询并检索候选 |
| MR-02 | Memory Activation Policy Engine | 决定激活哪些记忆、何时激活以及为什么激活 |
| MR-03 | Memory Context Manager (MCM) | 规划、编辑、版本化、预算管理和协调有 Scope 的 Memory Context |
| MR-04 | Context Synchronization Engine | 交付 Snapshot/Delta，并跟踪 Adapter ACK 和已应用版本 |

### D. 横切基础设施

| ID | 逻辑子系统 | 主要职责 |
|---|---|---|
| XF-01 | Storage, Index & Cache Infrastructure | 持久化原语、索引维护、缓存和 Runtime 工作集支持 |
| XF-02 | Scope, Permission & Governance Engine | 授权、隔离、保留、遗忘和审计策略 |
| XF-03 | Protocol Gateway & Adapter Contracts | BMCP 校验、能力协商、遥测和上下文消息边界 |
| XF-04 | Consistency, Recovery & Observability | 幂等、重放、协调修复、健康状态、Tracing、Metrics 和审计关联 |

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
