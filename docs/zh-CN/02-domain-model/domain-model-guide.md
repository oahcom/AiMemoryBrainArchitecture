# 领域模型架构指南

- 文档 ID：DOC-DOM-001
- 版本：1.0
- 源规范：02-domain-model/
- Owner：B — Domain Model
- 对应英文：[Domain Model Architecture Guide](../../en/02-domain-model/domain-model-guide.md)
- 状态：解释性指南；详细契约和未决 ADR 仍以源规范及正式决议为准

## 1. 为什么需要领域模型

领域模型为所有子系统统一定义 Brain 管理的对象，以及这些对象之间的关系。没有统一领域模型，Compiler、Store、Runtime、Context Manager 和 Governance 可能用同一个词表达不同含义，也可能对身份、时间、证据和归属作出互不兼容的假设。

领域模型定义语义和约束。它不规定 SQL 表结构、协议编码、信息提取算法、部署拓扑，也不指定某一种图数据库或索引引擎。

## 2. 最核心的概念

**Event 是系统捕获的内容；Memory 是被保留的知识资产；Claim 是该资产表达的命题；Evidence 是支持、反驳或限定 Claim 的依据。**

这些概念不能互换：
- Event 可能不完整、错误、只是计划、预测或来源报告。
- Memory 是可寻址、被保留的资产，但不自动代表真实。
- Claim 必须带有认知状态和时间限定。
- Evidence 是来源材料或观察，不是置信度分数。
- Provenance 记录资产来自哪里、经过了什么派生过程。

## 3. 概念对象关系图

~~~mermaid
erDiagram
  EVENT ||--o{ EVIDENCE : supplies
  MEMORY ||--|{ MEMORY_VERSION : versions
  MEMORY_VERSION ||--o{ CLAIM : contains
  CLAIM }o--o{ ENTITY : concerns
  CLAIM }o--o{ EVIDENCE : supported_by
  CLAIM }o--o{ RELATION : qualified_by
  EVIDENCE }o--|| PROVENANCE : traces
  MEMORY_VERSION }o--o{ MEMORY_SOURCE : derived_from
  MEMORY_CONTEXT ||--o{ CONTEXT_ENTRY : contains
  CONTEXT_ENTRY }o--|| MEMORY_VERSION : references
  AGENT_SCOPE ||--o{ MEMORY : bounds
  ENVIRONMENT_SCOPE ||--o{ EVENT : qualifies
~~~

这是概念关系图，不是物理数据库 Schema。如果某种关系本身具有角色、时间、Scope 或 Evidence，就可能需要独立的关联记录。Context Entry 引用某个 Canonical Version 或受治理的呈现内容，它不是第二份 Canonical Memory。

## 4. 主要领域对象

| 对象 | 含义 | 主要权威 |
|---|---|---|
| Event | 被捕获的发生、观察、报告或状态转换 | Event Ingestion |
| Memory | 被保留、可寻址的知识资产 | Canonical Memory |
| Claim | 关于实体、事件或状态的命题 | Domain Semantics；存储于 Canonical Version |
| Entity | 具有身份的指代对象，不只是名称或文本提及 | Entity & Relationship Manager |
| Relation | 带类型、端点、Scope 和可选有效时间的关联 | Entity & Relationship Manager |
| Evidence | 支持、反驳或限定 Claim 的来源材料/观察 | Evidence & Provenance Manager |
| Provenance | 来源及派生链路 | Evidence & Provenance Manager |
| Memory Version | 不可变的历史快照 | Canonical Store / Versioning |
| Memory Source | 派生资产到输入来源的类型化链接 | Evidence & Provenance Manager |
| Memory Context | 面向任务、有 Scope 和版本的记忆集合 | Memory Context Manager |
| Context Entry | Context 内的一条引用或呈现 | Memory Context Manager |
| Agent Scope | Agent 所属记忆命名空间 | Governance |
| Environment Scope | 世界、租户、项目环境、存档或模拟环境的命名空间 | Governance |

## 5. 身份、版本和时间

- ID 是不表达业务语义的不透明标识。UUIDv7 只是候选，不是强制算法。
- 同一 Memory 在多个不可变版本之间保持稳定的 memory_id。
- 更新会创建后继版本，不得原地修改历史内容。
- 并发更新使用 expected-version/CAS 或等价并发控制。过期写入必须被拒绝或显式协调。
- event_time、recorded_at 和 valid_time 分别回答不同问题，不得混淆。
- 未知值必须明确表示未知，不得编造时间、来源或身份。

## 6. 认知状态不等于生命周期

Claim 的认知状态说明命题的依据和当前认知地位：

| 状态 | 含义 |
|---|---|
| Observed | 直接捕获的观察 |
| Reported | 某个来源作出陈述，尚未独立验证 |
| Inferred | 通过声明的方法从前提推导而来 |
| Verified | 通过声明的验证流程或权威证明 |
| Disputed | 存在实质冲突且尚未解决 |
| Retracted | 由授权来源/流程撤回，或已被判定无效 |

Memory 生命周期说明资产的管理阶段：

| 状态 | 含义 |
|---|---|
| Candidate | 等待校验、巩固或策略决策 |
| Consolidated | 已通过结构性巩固检查 |
| Active | 在 Scope 和策略过滤后可正常检索 |
| Superseded | 已被后继资产替代，但保留历史 |
| Archived | 仍被保留，但当前策略下不再激活 |
| Forgotten | 已提交受治理 Forget；访问被禁止，清理/去标识过程有记录 |

两组状态彼此独立。Active Memory 可以包含 Disputed Claim；Archived Memory 也可以包含 Verified Claim。

## 7. Scope 不等于 Permission

Scope 回答：**资产属于哪里、适用于哪里？** Permission 回答：**谁可以执行什么操作？**

一个对象可以包含多个类型化 Scope 引用，但组合 Scope 不得默默扩大访问范围。相同 Agent 身份不代表可以跨不同 Environment Scope 读取内容。Evidence 的访问权限可能比派生 Memory 更严格。每个相关边界都必须检查 Permission，包括异步任务实际执行时。

## 8. Relation、Evidence 和 Provenance

Relation 是带类型的关联，不是文本共现或 Embedding 相似度。Relation 定义必须约束允许的端点类型、方向性、限定信息、时间语义、Scope 兼容性和唯一性。

Evidence 可以支持、反驳或限定 Claim。一份 Evidence 可以关联多个 Claim，一个 Claim 也可以有多份 Evidence。同一来源的复制件不能被算作相互独立的佐证。

Provenance 记录来源版本、使用的来源片段、转换过程、方法/组件版本、派生时间、输入摘要、父级链路，以及不可用或脱敏的原因。方法引用只能解释内容如何产生，不能证明结果正确。

## 9. 记忆如何形成

~~~text
发生 / 报告 / 文档 / 观察
        ↓
Event 和来源登记
        ↓
Evidence 与 Provenance
        ↓
候选 Memory 和 Claim 提案
        ↓
Entity 与 Relation 解析
        ↓
认知、时间和 Scope 限定
        ↓
Lifecycle Policy 评估
        ↓
Canonical Memory Version
        ↓
检索，并可选进入 Context
~~~

Compiler 负责提出和转换候选内容，不能绕过 Canonical Lifecycle Policy。Schema 合法不代表内容真实。没有结果证据时，计划或预测不得升级为已完成结果。

## 10. 必须保留的领域不变量

1. Event 不等于 Memory；Evidence 不等于 Claim。
2. Claim 是命题，不是其来源。
3. Memory 在不可变版本之间保持稳定身份。
4. 未知时间不意味着“永远有效”。
5. 派生资产必须关联来源，或明确记录 Provenance 不可用的原因。
6. 没有结果证据时，Intent、Plan、Prediction 和 Pending Action 不得成为已完成结果。
7. Relation 必须带类型；共现不等于 Relation。
8. Scope 不等于 Permission。
9. Context Entry 不拥有也不修改 Canonical Memory。
10. Context Remove 不等于 Forget。
11. 冲突 Claim 必须保留证据和解决历史。
12. Confidence、Trust、Relevance 和 Evidence Strength 彼此不同。

## 11. 重要未决事项：Fact / Claim

当前跨模块集成记录仍将 Fact/Claim ADR 标记为 **ADR-BLOCKED**。部分较早的领域模型文本将 Claim 描述为规范命题对象，并把 Fact 视为带限定的 Claim 解释；但在治理决议解除阻塞之前，不能据此冻结下游 Schema。

正式 ADR 批准之前：
- 保留现有源文档中的表述作为已有提案/历史基线，不把它提升为新的全系统批准契约。
- 不得仅凭翻译决定增加或删除独立 Fact 对象。
- 依赖该问题的 Schema 和接口决策继续保持 OPEN/BLOCKED。
- 正式决议形成后，必须同步更新中英文指南和受影响规范。

## 12. 详细源规范

本指南是易读入口，不替代详细契约：
- [领域模型总览](../../../02-domain-model/domain-model-overview.md)
- [核心领域实体](../../../02-domain-model/core-entities.md)
- [认知与时间语义](../../../02-domain-model/epistemic-and-temporal-semantics.md)
- [记忆生命周期模型](../../../02-domain-model/lifecycle-model.md)
- [关系与来源模型](../../../02-domain-model/relationships-and-provenance.md)
- [Scope 与 Permission 模型](../../../02-domain-model/scope-and-permission-model.md)

详细源规范仍是实现参考。本指南不声称所有字段级契约已经完成翻译。
