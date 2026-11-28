# 系统架构规范

- 文档 ID：SYS-ARCH-001
- 版本：1.0
- 源规范：[规范性原文](../../../01-system-architecture/system-overview.md)
- 源版本：c3707831777feb14aedd7aea0eca1c162bf59fc6
- 对应英文：[System Architecture Specification](../../en/01-system-architecture/system-architecture-specification.md)
- 状态：DECIDED（已决议基线），其中明确标记的候选项和验证项除外

**范围：** 本文定义逻辑系统架构，不定义部署拓扑或代码级设计。

## 1. 产品定义

AI Memory Brain 是一套独立的记忆基础设施，负责捕获经历、编译持久化记忆资产、检索并激活相关知识，以及为跨会话、跨模型、跨环境的 Agent 管理带版本的记忆上下文。

即使 Agent 实现或底层 LLM 发生变化，系统也应保持记忆连续性。

## 2. 目标

- 建立持久化、结构化、可追溯的记忆资产。
- 在明确的 Scope 和 Permission 约束下，实现跨会话、跨 Agent 的记忆复用。
- 从事件、观察、文档和用户提供的信息中形成记忆。
- 结合结构化、词法、语义、时间和关系信号进行检索。
- 根据结构化 Agent/环境遥测主动激活记忆。
- 由 Brain 权威地、带版本地管理 Agent 推理上下文中的专属记忆区域。
- 明确生命周期、冲突、保留、遗忘、审计和恢复语义。
- 采用 Local-first 运行方式，并在需要时使用资源可控的模型辅助组件。

## 3. 非目标

Brain 不负责：

- Agent 规划、任务拆解或行动选择。
- 工具执行、浏览器/终端控制或环境操纵。
- Agent 安全策略、外部动作权限或模型 Guardrail。
- 特定 LLM、Agent 框架、Prompt 模板或专有隐藏推理格式。
- Skill 执行。Skill Library 可以是独立子系统，并引用记忆。

## 4. 逻辑架构

### 4.1 Memory Brain（记忆大脑）

负责权威记忆的身份和生命周期：

- 领域语义与规范标识符。
- 权威记忆持久化和版本历史。
- 实体与关系管理。
- 认知和时间限定。
- 来源链和证据引用。
- Canonical Forget 身份／生命周期／Fence 机制（Owner D）；全局授权、保留／法律保全、外部副本策略、全局目标清单及全局完成标准（Owner I）。

Global Forget Completion 必须由 Owner D 与每一位相关执行 Owner 根据经这些 Owner 接受的完成证据契约共同确定。Owner D 和 Owner I 均不得单方面宣布全局完成。该契约仍有待相关 Owner 接受；本方向性要求本身不构成相关 Owner 已接受该契约的证据。

### 4.2 Memory Compiler（记忆编译器）

将输入转换为候选及巩固后的记忆资产：

- 可靠的事件接收。
- 提取与规范化。
- 实体解析与关系提议。
- 证据和来源链关联。
- 重复检测、巩固与冲突处理。
- 索引更新事件生成。

事件接收确认不应依赖同步 LLM 推理。可靠接收与语义巩固是两个独立阶段。

### 4.3 Memory Runtime（记忆运行时）

在交互期间提供记忆服务：

- 检索路由与候选生成。
- 激活策略评估。
- 有界运行时工作集和缓存。
- 上下文规划与充分性评估。
- 上下文编辑、版本管理、协调与同步。

### 4.4 Agent Integration（Agent 集成）

定义由 Brain 拥有的契约及 Agent 侧执行机制：

- 将结构化遥测映射到规范 Schema。
- 上下文包投递和能力协商。
- Adapter 在推理边界进行校验和应用。
- 明确的确认、拒绝和版本协调。

### 4.5 横切基础设施

- 存储与索引基础设施。
- Scope 和 Permission 强制执行。
- 一致性、幂等性、事件重放和恢复。
- 审计、可观测性和性能测量。

## 5. 逻辑数据路径

### 5.1 从经历到记忆

Agent / Environment → Event Ingress（事件接收）→ Durable Event Log（持久化事件日志）→ Memory Compiler（记忆编译器）→ Canonical Memory Store（权威记忆存储）→ Index Updates（索引更新）→ Runtime Availability（运行时可检索）

### 5.2 从记忆到推理上下文

Agent Telemetry（Agent 遥测）→ Protocol Gateway（协议网关）→ Memory Observer（记忆观察器）→ Activation & Retrieval（激活与检索）→ Context Planner / Editor（上下文规划/编辑）→ Versioned Change Set（带版本的变更集）→ Adapter → Next Inference Boundary（下一次推理边界）→ Acknowledgement（确认）

### 5.3 治理路径

Authorized Request（已授权请求）→ Scope & Permission Check（作用域与权限检查）→ Governance Policy（治理策略）→ Canonical / Derived Data Actions（权威/派生数据操作）→ Index & Cache Reconciliation（索引与缓存协调）→ Audit Record（审计记录）

## 6. 记忆与上下文分离

- Canonical Memory 是持久化权威。
- Memory Context 是针对特定 Agent Instance、任务和环境构建的、有 Scope 和版本的视图。
- Applied Context 记录 Adapter 确认已在约定边界安装的上下文。
- 记忆可以存在，但尚未被激活到任何上下文。
- 同一条权威记忆可以通过不同的任务化呈现，出现在多个上下文中。
- 移除 Context Entry 不会删除其 Canonical Memory。
- Brain 不得假设修改受管记忆区域就能擦除模型已经处理过的内容。

## 7. 观察与激活模型

Brain 使用结构化遥测作为判断任务状态和潜在记忆需求的证据，不要求完整的隐藏思维链（Chain of Thought）。

规范遥测可以包含 Task State、Intent、Plan Summary、Active Entities、Pending Actions、Observations、Outcomes、Uncertainty、Risk Signals 和 Environment State Deltas。

Intent 和 Plan 字段描述未来或计划状态，不是结果证据。激活策略由 Brain 拥有；Adapter 将 Agent 原生信号映射到规范 Schema。

**CANDIDATE（候选）：** 在 Agent 工作期间进行异步预激活，并在高影响或不可逆动作前进行同步检查。触发阈值和评分权重仍需验证。

## 8. 上下文应用边界

Brain 是其管理记忆上下文的逻辑权威。Adapter 是实际应用上下文包或变更集的执行点。

必须明确界定受管记忆区域，不得覆盖 System/Developer 指令、用户原始输入或 Agent 安全策略。变更在下一次推理上下文组装时应用，而不是假设可以改写正在执行的推理。

## 9. 隔离模型

Scope 与 Permission 相互独立：

- Scope 定义所有权/命名空间，例如 User、Project、Agent、Agent Instance、Session 和 Environment。
- Permission 决定对该 Scope 内资源允许执行哪些操作。
- Environment 标识符必须区分可能发生状态冲突的不同世界、存档、租户或模拟环境。
- 共享 Canonical Memory 不意味着共享工作上下文，也不意味着可以不受限制地访问。

## 10. 部署与实现中立性

**DECIDED（已决议）：** 逻辑子系统不自动意味着独立进程、服务或 Rust Crate。

**CANDIDATE（候选）：** 首期采用内部契约清晰的模块化单体；只有在隔离、扩展、可靠性或部署证据足以支持时才拆分进程。

## 11. 主要质量属性

- 正确性与来源链完整性。
- Scope 和 Permission 隔离。
- Context 版本一致性与可恢复性。
- 低且可预测的检索/同步延迟。
- CPU、内存、磁盘及可选 GPU 消耗有界。
- Adapter 互操作性和协议演进能力。
- 可观察、可复现的 Agent 层面收益。

在代表性工作负载和硬件基线确定前，量化目标均为 **OPEN（未决）**。

## 12. 开放的架构问题

1. 什么样的 Canonical Memory 粒度最适合支持 Event、Claim 和 Evidence 版本管理？
2. 对每个 Adapter 能力等级，哪些遥测字段必须提供，哪些可以选填？
3. 如何跨任务衡量 Context Sufficiency，同时避免对单一 Agent 过拟合？
4. Event Log、Canonical Store 和索引之间需要什么一致性保证？
5. 在 12–16 GB VRAM 本地设备上，最小且安全、有用的模型辅助编译流水线是什么？
6. 在代表性的混合检索负载下，哪种存储/索引候选方案更合适？
7. 派生记忆、缓存和备份的保留及物理擦除保证是什么？
