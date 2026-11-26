---
document_metadata:
  domain: architecture
  role: guide
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      evidence_reference: []
    evidence_verification:
      verification_status: Unverified
      last_verification_note: "Classified Informative because the existing EN/ZH guides explicitly state they are explanatory and do not replace Owner specifications or ADRs. Owner-authorized source/mirror topology for AID-2026-11-26-GOV-DOC-01; not a formal approval record. Pre-metadata content blob: ed071263a18962ecc1d6265f2b10e883815f829d. Approval remains Draft; evidence verification remains Unverified."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "System architecture overview guide"
    canonical_scope_id: architecture/system-overview-guide
    canonical_scope_keywords:
      - system-overview
      - architecture-guide
      - logical-components
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "01-system-architecture/system-overview.md"
    en: "docs/en/01-system-architecture/system-overview.md"
    zh-CN: null
---
# AI Memory Brain 系统架构总览

- 文档 ID：DOC-SYS-001
- 版本：1.0
- 对应英文：[System Architecture Overview](../../en/01-system-architecture/system-overview.md)
- 状态：架构解释文档；不替代 Owner 规范和 ADR

## 规范原文结构映射（解释性镜像）

本文件是解释性指南，并非规范原文 `01-system-architecture/system-overview.md` 的逐节替代。本指南为便于阅读，有意将原文十二个章节重新组织为九个章节。下表记录这一编辑结构差异；完整措辞和语义仍以规范原文为准。

| 规范原文章节 | 本解释性指南中的对应内容 |
|---|---|
| 1. Product definition（产品定义） | 1. 一句话理解项目 |
| 2. Goals（目标） | 1. 一句话理解项目；5. 三条主要工作流 |
| 3. Non-goals（非目标） | 2. Brain 负责什么？不负责什么？ |
| 4. Logical architecture（逻辑架构） | 3. 系统全景；4. 六个关键部分；7. A–I 架构责任 |
| 5. Logical data paths（逻辑数据路径） | 3. 系统全景；5. 三条主要工作流 |
| 6. Memory and context separation（Memory 与 Context 分离） | 6. 五组必须区分的概念 |
| 7. Observation and activation model（观察与激活模型） | 4.3. Memory Runtime；5.2. 从记忆到推理上下文 |
| 8. Context application boundary（Context 应用边界） | 4.4. Memory Context；4.5. BMCP 与 Agent Adapter |
| 9. Isolation model（隔离模型） | 2. Brain 负责什么？不负责什么？；4.6. Security & Governance |
| 10. Deployment and implementation neutrality（部署与实现中立性） | 3. 系统全景；8. 当前架构状态 |
| 11. Primary quality attributes（主要质量属性） | 8. 当前架构状态 |
| 12. Open architecture questions（开放架构问题） | 8. 当前架构状态 |

这种重新组织仅属于编辑结构差异，不会删除、缩小或替代规范原文中的任何决策、候选项、待验证事项或开放问题。本指南内容较简略之处，请以规范原文为准。

## 1. 一句话理解项目

**AI Memory Brain 是独立于 Agent 和大语言模型的长期记忆基础设施。它把经历整理成可追溯、可管理的记忆资产，并在需要时组织成上下文，交给 Agent 在推理边界使用。**

核心目标是保持记忆连续性：Agent、模型、会话和运行环境可以变化，但有价值的记忆不应随之丢失，也不应被锁在某个 Agent 的 Prompt 或私有数据库中。

## 2. Brain 负责什么？不负责什么？

### Brain 负责
- 接收对话、观察、文档和事件等记忆来源。
- 将来源整理成结构化记忆，保留证据和来源关系。
- 管理记忆身份、版本、关系、冲突、生命周期和遗忘。
- 根据任务和环境检索、筛选并激活相关记忆。
- 管理专属 Memory Context：添加、更新、移除、排序、压缩和版本同步。
- 记录 Adapter 是否在约定推理边界应用了某个上下文版本。
- 执行 Scope、Permission、安全、审计和恢复约束。

### Brain 不负责
- 不替 Agent 推理、规划、拆解任务或选择行动。
- 不执行工具、浏览器、终端或环境操作。
- 不决定 Agent 是否有权执行外部动作。
- 不依赖特定 LLM、模型供应商或 Agent 框架。
- 不把模型生成的内容自动当作事实。

**简单区分：Agent 负责“想什么、做什么”；Brain 负责“记住什么、依据是什么、何时提供、如何管理和遗忘”。**

## 3. 系统全景

~~~mermaid
flowchart TB
    Agent[Agent：推理、规划、行动]
    Adapter[Agent Adapter：遥测映射与推理边界应用]
    Protocol[BMCP：记忆上下文协议]
    Compiler[Memory Compiler：经历编译为记忆]
    Brain[Memory Brain：权威记忆与生命周期]
    Runtime[Memory Runtime：检索与激活]
    Context[Memory Context：任务化上下文]
    Governance[Security & Governance：身份、权限、遗忘、审计]
    Storage[Storage / Index / Cache：持久化与派生索引]
    Agent <--> Adapter
    Adapter <--> Protocol
    Protocol <--> Compiler
    Protocol <--> Runtime
    Compiler --> Brain
    Brain --> Storage
    Storage --> Runtime
    Runtime --> Context
    Context --> Protocol
    Governance -. governs .-> Compiler
    Governance -. governs .-> Brain
    Governance -. governs .-> Runtime
    Governance -. governs .-> Context
~~~

图中表示逻辑关系，不代表每个方框都必须部署成独立进程、服务或 Rust Crate。

## 4. 六个关键部分

### 4.1 Memory Brain：权威记忆
保存系统管理的记忆资产及其版本、身份、证据、来源、关系和生命周期。Owner D 负责 Canonical Memory 身份/生命周期、Forget Fence 与 Canonical Forget 机制及 D 域完成判定；Owner I 负责全局授权、Retention/Legal Hold、外部副本策略、全局目标清单和全局完成标准。它回答：这条记忆是什么、来自哪里、当前版本是什么、有什么证据、是否冲突、是否仍有效、是否应归档或遗忘？

Global Forget Completion 必须由 Owner D 与每一位相关执行 Owner 基于这些 Owner 共同接受的完成证据契约联合判定。D 或 I 均不得单方面宣称全局完成。该契约仍待相关 Owner 接受；本方向决策不构成接受证据。

### 4.2 Memory Compiler：把经历整理成记忆
接收原始事件和内容，执行校验、提取、规范化、实体解析、证据关联、冲突处理和巩固。

以下状态不可混为一谈：
- **Accepted**：来源已被可靠接收。
- **Compiled**：编译流程已处理。
- **Canonical Committed**：正式写入权威记忆。
- **Indexed**：检索索引已更新。

接收成功不等于记忆已经形成；编译完成也不等于索引已更新。

### 4.3 Memory Runtime：运行时记忆服务
在交互过程中检索候选记忆、评估激活价值、维护有界工作集，并向 Context Manager 提供建议。Runtime 不拥有 Canonical Memory 或 Context Version 的最终权威。

### 4.4 Memory Context：当前任务需要的记忆视图
它不是整个记忆数据库，也不是完整 Prompt，而是 Brain 根据 Agent、任务、环境、权限和预算构建的、可版本化的记忆集合。Brain 对自己管理的区域执行 Add、Update、Remove、Replace、Reorder、Compact 等操作；变更在约定的下一次推理上下文组装边界生效。

### 4.5 BMCP 与 Agent Adapter：连接 Brain 和 Agent
BMCP 定义消息、上下文交付、能力协商和确认语义。Adapter 将 Agent 的结构化遥测映射给 Brain，并在推理边界应用 Brain 管理的上下文。Adapter 不得改写 Agent 的 System、Developer 或用户原始内容，也不得绕过 Agent 自己的安全策略。

### 4.6 Security & Governance：贯穿全系统的治理
身份、Scope、Permission、保留策略、Forget、审计和恢复，贯穿接收、编译、存储、检索、上下文交付和备份恢复。

## 5. 三条主要工作流

### 5.1 从经历形成记忆

~~~text
Agent / Environment / User
        ↓
Event Ingress（事件接收）
        ↓
Durable Acceptance（可靠接收）
        ↓
Memory Compiler（提取、规范化、证据关联）
        ↓
Canonical Memory（权威提交）
        ↓
Index Updates（索引更新）
        ↓
Memory Runtime 可检索
~~~

### 5.2 从记忆到推理上下文

~~~text
Agent Telemetry（任务与环境信号）
        ↓
BMCP
        ↓
Retrieval & Activation（检索与激活）
        ↓
Context Planner / Editor（上下文规划与编辑）
        ↓
Context Version / ChangeSet
        ↓
Adapter Delivery
        ↓
下一次推理上下文组装边界
        ↓
Applied Acknowledgement（应用确认）
~~~

Applied 只能证明 Adapter 在约定边界应用了对应版本，不能证明模型一定注意到、理解或遵循这些记忆。

### 5.3 遗忘与撤销

~~~text
Authorized Forget Request
        ↓
Governance Authorization
        ↓
Forget Fence + Producer Barrier
        ↓
阻止旧任务和迟到派生物重新发布
        ↓
清理或抑制 Canonical / Index / Cache / Context / Adapter / Backup
        ↓
收集每个目标的完成证据
        ↓
Global Forget Completion Decision
~~~

**Context Remove 不等于 Forget。** 从当前任务上下文移除一条记忆，不代表权威记忆已被删除。Forget 还必须阻止旧任务、索引重建、缓存回填或离线 Adapter 重新带回已遗忘内容。

## 6. 五组必须区分的概念

| 容易混淆 | 正确区别 |
|---|---|
| Event / Memory / Claim | Event 是被记录的经历或输入；Memory 是保留的知识资产；Claim 是其中表达的命题。 |
| Canonical Memory / Memory Context | 前者是权威记忆资产；后者是任务化、可版本化的记忆视图。 |
| Context Remove / Forget | 前者改变当前上下文；后者是受治理的记忆撤销与清理流程。 |
| Accepted / Applied | Accepted 表示可靠接收；Applied 表示 Adapter 在约定推理边界应用。 |
| Confidence / Relevance | Confidence 表示支持程度；Relevance 表示对当前任务的有用程度。 |

## 7. A–I 架构责任

| Owner | 权威责任 |
|---|---|
| A — Principal Integration | 全系统集成、跨模块冲突协调和最终架构裁决 |
| B — Domain Model | 领域对象、身份语义和规范模型 |
| C — Agent Integration | Agent Adapter、推理边界和最终请求证据 |
| D — Memory Brain | Canonical Memory 身份、版本、生命周期、Canonical Forget 机制与 Forget Fence；D 域完成判定 |
| E — Memory Compiler | 接收、提取、规范化、证据和派生物生产 |
| F — Memory Runtime | 检索、激活、工作集和缓存 |
| G — Memory Context | Context Version、ChangeSet、Delivery 意图 |
| H — BMCP Protocol | 协议 Envelope、消息、版本和 ACK 语义 |
| I — Security & Governance | 全局授权、Retention/Legal Hold、外部副本策略、全局目标清单和全局完成标准；组织联合完成所需的策略/证据要求 |

跨模块协作不改变领域 Owner 的权威。Storage/Consistency 提供真实持久化和事务执行能力，也不能替代领域 Owner 对语义的决定。

## 8. 当前架构状态

- **DECIDED**：Brain 独立于 Agent/模型；Canonical Memory 与 Context 分离；记忆内容是数据而非指令；Scope 与 Permission 分离；Forget 必须覆盖派生表示。
- **CANDIDATE**：模块化 Rust 单体作为首期部署形态；SQLite WAL 作为首轮存储原型；具体索引、向量检索、推理后端和传输技术。
- **OPEN / BLOCKED**：Fact/Claim ADR；D/E/Storage 的 Producer Admission、Forget Fence、Dependency Registration 和 Publication 原子边界；JF-10 与 COC 的应用级恢复；端到端 Applied 证明；Global Forget 全目标闭环。
- **TO_VALIDATE**：真实并发、崩溃、恢复、索引防复活、缓存失效、资源预算和 P95/P99 性能。

本文描述架构基线和候选实现方向，不表示系统已经实现或通过生产验收。

## 9. 推荐阅读顺序

1. [架构不变量](../../../00-governance/architecture-invariants.md)
2. [规范术语表](../../../00-governance/terminology.md)
3. [系统组件图](../../../01-system-architecture/component-map.md)
4. [子系统职责矩阵](../../../01-system-architecture/responsibility-matrix.md)
5. [领域模型总览](../../../02-domain-model/domain-model-overview.md)
6. 各模块 Owner 的详细规范
7. [技术架构总览](../13-engineering-decisions/technology-architecture-overview.md)

---
**English counterpart:** [System Architecture Overview](../../en/01-system-architecture/system-overview.md)
