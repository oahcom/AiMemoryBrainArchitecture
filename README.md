# AI Memory Brain Architecture

> **Model-independent memory infrastructure for AI agents.**  
> **面向 AI Agent 的模型无关记忆基础设施。**

AI Memory Brain is being designed as a durable, governed memory layer that allows different agents, models, and runtimes to share and carry forward knowledge without making any one model or agent framework the owner of that knowledge.

AI Memory Brain 致力于构建一个持久、可治理的 AI 记忆层，让不同 Agent、模型和运行环境能够共享并延续知识，而不把记忆的所有权绑定到某个模型或 Agent 框架。

<p align="center">
  <strong>Agents may change. Models may change. Memory should remain portable, traceable, and governable.</strong><br/>
  <strong>Agent 可以更换，模型可以更换；记忆应当持续存在、可追溯、可治理、可迁移。</strong>
</p>

---

## Project status / 项目状态

| Item | Current status |
|---|---|
| Repository | Architecture specifications and system-contract design |
| Product-level runtime | **Not started** — the repository contains limited reference models, validators, and conformance tests, but no integrated product runtime |
| Architecture | System boundaries and core subsystem responsibilities are defined; detailed contracts continue to evolve |
| Protocol and technology choices | Some items remain CANDIDATE, OPEN, or TO_VALIDATE; see their source specifications |
| Performance and production validation | Not yet established through a running implementation and representative workloads |

This is an architecture-first project. A documented design, proposed contract, or review result is not evidence that the corresponding capability has been implemented, integrated, or production-validated. Status labels in the source documents remain authoritative.

本项目采用架构先行的推进方式。目前仓库承载架构规范、子系统设计和跨模块契约治理，并包含少量参考模型、验证器和符合性测试；**产品级运行时尚未开始实现**，这些参考资产不构成集成产品。文档中的设计、候选方案或局部测试结果，不代表相应能力已经完成端到端集成或通过生产验证。具体决策状态以源规范中的标记为准。

## 1. The problem we are solving / 我们要解决的问题

AI agents are becoming more capable, but their useful knowledge is still fragmented across conversations, sessions, applications, model providers, and agent frameworks. Built-in model memory and individual agent-memory libraries can help within their own boundaries, but they do not by themselves establish a durable, independently governed memory authority shared across heterogeneous agents.

As systems become long-running and multi-agent, the hard problems are not just storing summaries or retrieving similar text. They include:

- **Continuity:** preserve useful knowledge across sessions, agents, model upgrades, and runtime changes.
- **Meaning and evidence:** distinguish events, claims, entities, relationships, observations, plans, and verified outcomes.
- **Change over time:** revise stale information without erasing history or silently turning conflicting claims into one “fact.”
- **Governance:** enforce scope, permissions, retention, forgetting, audit, and recovery across derived data and connected components.
- **Reliable application:** know not only what context was sent, but which version an adapter actually applied at the inference boundary.
- **Interoperability:** avoid coupling the memory store and lifecycle to one model vendor or agent framework.

AI Agent 正在变得更强，但有价值的知识仍分散在对话、会话、应用、模型厂商和 Agent 框架之中。模型内置记忆和单个 Agent 的记忆库可以解决各自边界内的问题，却不天然等于一个能够跨异构 Agent 持续存在、独立治理的记忆权威层。

当系统变成长周期、多 Agent 系统，真正困难的就不只是保存摘要或检索相似文本，还包括跨会话连续性、事实与证据语义、信息随时间变化、跨组件治理，以及确认记忆上下文是否真正应用到推理边界。

## 2. Our positioning / 项目定位

**AI Memory Brain is being designed as an independent memory authority and governance layer—not another Agent framework, chat application, vector database, or prompt-management tool.**

Its job is to own the lifecycle of canonical memory and coordinate how task-specific memory context is prepared, delivered, applied, reconciled, and governed. Agents remain responsible for reasoning, planning, tool use, and action execution.

**AI Memory Brain 正在被设计为独立的记忆权威与治理层，而不是另一个 Agent 框架、聊天应用、向量数据库或提示词管理工具。**

其目标是管理规范记忆资产的生命周期，并协调任务所需记忆上下文的准备、交付、应用、对账和治理。推理、规划、工具调用与行动执行仍由 Agent 自身负责。

### What the architecture is designed to provide / 架构目标

- A model- and agent-framework-independent memory architecture.
- A canonical, versioned home for durable memory assets and their evidence.
- A lifecycle and governance layer for memory creation, revision, conflict, retention, and forgetting.
- A context-serving and synchronization layer between memory and agent inference boundaries.
- An interoperability architecture, including BMCP and Agent Adapters.

### What we are not / 我们不是什么

- Not an LLM, an Agent, or an Agent orchestration framework.
- Not a replacement for the Agent's planner, tools, skills, or action policy.
- Not merely a vector database, RAG pipeline, conversation summarizer, or profile store.
- Not a claim that every model's hidden internal state can be inspected, controlled, or erased.
- Not currently a production-ready implementation.

## 3. The architectural idea / 核心架构思想

The proposed architecture separates three concerns that are often collapsed into one memory feature:

1. **Canonical Memory — what the system knows and why.** Durable, versioned memory assets with identity, scope, lifecycle, evidence, and provenance.
2. **Memory Context — what a particular agent/task needs now.** A scoped and versioned working view assembled for a specific execution context.
3. **Applied Context — what the adapter attests to applying.** Evidence of the context version included at the declared inference boundary, as attested by the Adapter.

This separation matters. A memory can exist without being activated into a task. Removing an item from one task context does not automatically delete its canonical memory. Sending a context package does not prove that an agent applied it. Forgetting is a governed lifecycle operation, not merely removing text from a prompt.

架构将经常被混为一谈的三个概念明确分离：

1. **Canonical Memory（规范记忆）：系统长期保存了什么，以及依据是什么。** 具备身份、作用域、生命周期、证据和来源链的持久化、版本化记忆资产。
2. **Memory Context（记忆上下文）：某个 Agent/任务此刻需要什么。** 面向具体执行环境构建的、有作用域和版本的工作视图。
3. **Applied Context（已应用上下文）：Adapter 对应用操作作出了什么确认。** 由 Adapter 提供的证据，用于表明特定上下文版本已纳入约定的推理请求边界。

记忆存在不代表它必须进入每个任务上下文；从某个任务上下文移除内容不等于删除规范记忆；发送上下文也不等于 Agent 已经应用。遗忘必须是受治理的生命周期操作，而不只是从提示词中删掉一段文字。

### Logical architecture / 逻辑架构

| Layer | Responsibility |
|---|---|
| **Memory Brain** | Canonical identity, domain semantics, persistence, versioning, entities, relations, lifecycle, provenance |
| **Memory Compiler** | Event ingestion, extraction, normalization, evidence linking, consolidation, conflict handling |
| **Memory Runtime** | Retrieval, activation, working sets, context planning, versioning, synchronization |
| **BMCP & Agent Adapters** | Telemetry, capability negotiation, snapshots/deltas, application acknowledgements, version reconciliation |
| **Cross-cutting infrastructure** | Scope and permissions, storage and indexes, consistency, recovery, audit, security, observability |

These are logical responsibility boundaries, not a requirement to deploy each component as a separate service or process.

这些是逻辑职责边界，并不意味着每个组件都必须独立部署为服务或进程。

## 4. Where we intend to create durable value / 长期价值来自哪里

We do not expect generic summarization, embeddings, or vector search alone to be a defensible moat. Those capabilities are increasingly available as model-provider features and managed services.

The intended differentiation is in the system-level guarantees and interoperability around memory:

### 4.1 Canonical memory semantics

Represent Event, Memory, Claim, Entity, Relation, Evidence, and Provenance as distinct concepts. Preserve the difference between an observation, a claim, an intention, and a verified outcome. Make revision and conflict explicit rather than hiding them in regenerated summaries.

### 4.2 Lifecycle and provenance

The design tracks where a memory came from, how it was derived, which evidence supports it, how it changed, and which downstream artifacts depend on it. It aims to enable controlled revision, supersession, retraction, retention, and recovery. **Provenance provides traceability; by itself, it does not prove that a source is authentic, accurate, untampered, or independent of other sources.**

### 4.3 Governance that reaches derived data

Treat forgetting and access control as end-to-end system concerns—not just deletion from the primary record. The design must account for producers, derived memories, queues, indexes, caches, recall paths, contexts, and restoration paths. Forget-related fences and publication gates are intended to prevent stale asynchronous work from making withdrawn information visible again; their complete correctness still requires implementation and fault-injection evidence.

### 4.4 Applied-context accountability

Distinguish **Delivered**, **Applied**, and **Acknowledged**. A transport success is not proof of application. The design aims to make context version, adapter capability, application boundary, and reconciliation state explicit. An Applied attestation can establish the declared Adapter-boundary operation and inclusion of a context version in the submitted request; it does **not** prove that the model attended to, understood, remembered, or behaviorally used that content.

### 4.5 Cross-agent and cross-model portability

Keep canonical memory independent of a particular model's prompt format or an Agent framework's private state representation. Use protocol contracts and adapters to connect heterogeneous systems without surrendering memory authority to any one of them.

我们不认为摘要生成、Embedding 或向量检索本身能够构成长期壁垒——这些能力正逐渐成为模型厂商和托管服务的通用功能。

项目希望形成的长期差异化，在于围绕记忆建立系统级语义、治理和互操作保证：

- **规范记忆语义：** 区分 Event、Memory、Claim、Entity、Relation、Evidence、Provenance，避免把观察、主张、意图和已验证结果混为一谈。
- **生命周期与来源链：** 追踪记忆来源、派生过程、支持证据、历史修订及下游依赖。来源链提供可追溯性，但本身不能证明来源真实、准确、未被篡改，也不能证明多个来源彼此独立。
- **覆盖派生数据的治理：** 将遗忘和权限控制延伸到生产者、派生记忆、队列、索引、缓存、召回、上下文和恢复路径。Forget Fence 与 Publication Gate 的目标是防止过期异步任务让已撤回信息重新可见；其完整正确性仍需实现和故障注入证据。
- **上下文应用可问责：** 明确区分 Delivered、Applied、Acknowledged。Applied 证据最多证明约定的 Adapter 边界操作及特定上下文版本被纳入提交请求，不证明模型注意、理解、记住或实际使用了这些内容。
- **跨 Agent、跨模型迁移：** 规范记忆不依赖某个模型的提示词格式或某个 Agent 框架的私有状态表达，通过协议与 Adapter 连接异构系统。

## 5. Interoperability / 互操作方向

BMCP is currently a **candidate application-level protocol contract**. Its interoperability, wire compatibility, and independent implementations have not yet been demonstrated. It may ultimately be implemented over existing transport and serialization mechanisms; the intended value is in the memory-lifecycle semantics, not in inventing a new transport stack.

The project is designed around an explicit boundary between the Brain and external agents:

- **BMCP** is intended to define the protocol surface for memory-related telemetry and context exchange; its contract and interoperability remain candidate work.
- **Adapters** translate agent-specific signals into canonical telemetry and apply context changes at inference boundaries.
- **Capability negotiation and versioning** make differences between integrations explicit.
- **Acknowledgements and reconciliation** provide evidence about delivery and application state.

The goal is not to force every agent to adopt one runtime. The goal is to let existing and future agents use a common, governed memory layer while retaining their own reasoning and execution environments.

BMCP 目前仍是**候选的应用层协议契约**，尚未证明其互操作性、线上兼容性或独立实现能力。它最终可以建立在现有传输和序列化机制之上；预期价值在于记忆生命周期语义，而不是重新发明传输协议栈。

项目通过 Brain 与外部 Agent 之间的明确边界实现互操作：

- **BMCP** 旨在定义记忆相关遥测与上下文交换的协议边界；其契约和互操作能力仍处于候选阶段。
- **Adapter** 将各类 Agent 信号映射为规范遥测，并在推理边界应用上下文变更。
- **能力协商与版本管理** 显式表达不同集成方式的能力差异。
- **确认与对账** 为上下文交付和应用状态提供证据。

我们不要求所有 Agent 采用同一种 Runtime；目标是让现有和未来的 Agent 都能使用共同、可治理的记忆层，同时保留各自的推理和执行环境。

## 6. Roadmap / 后续方向

The intended progression is evidence-driven. Each stage depends on stable contracts and measurable acceptance criteria—not on the number of documents or components.

| Stage | Focus | Evidence required to progress |
|---|---|---|
| **1. Architecture and domain contracts** | Freeze core semantics, ownership boundaries, lifecycle, scope, permissions, and critical invariants | Approved decisions, consistent bilingual specifications, explicit open issues |
| **2. Canonical memory vertical slice** | Implement durable event ingress, canonical memory, evidence/provenance, versioning, and lifecycle | Reproducible tests for identity, idempotency, revisions, conflicts, and persistence |
| **3. Runtime and context application** | Retrieval, activation, context planning, versioned snapshots/deltas, adapter application | Agent-task evaluations, context-version evidence, latency and resource measurements |
| **4. Governance and recovery** | Forgetting, retention, derived-data reconciliation, recovery, audit, and failure handling | Concurrency, retry, crash, replay, offline-reconnect, and non-resurrection tests |
| **5. Interoperability and adoption** | BMCP compatibility, multiple adapters, integrations, operational deployment | Independent conformance evidence, cross-agent portability, real workload and user validation |

### Near-term engineering priorities / 近期工程优先级

1. Resolve blocking domain-model and cross-module semantic decisions before treating them as frozen contracts.
2. Close the end-to-end producer, derivative, storage, publication, and forgetting transaction semantics.
3. Define executable conformance tests for idempotency, recovery, context application, and lifecycle invariants.
4. Build a narrow vertical slice before expanding subsystem breadth.
5. Benchmark representative workloads and publish the environment, dataset, latency, recall, resource use, and failure conditions.
6. Validate the architecture against multiple agent/model integrations rather than optimizing for one vendor.

路线图以可验证证据推进，而不是以文档数量或组件数量衡量进度。近期优先解决领域模型与跨模块语义阻塞、遗忘端到端事务语义、可执行一致性测试，并尽早构建窄而完整的纵向切片。性能结论必须绑定真实工作负载、测试环境和可复现数据。

## 7. What success should look like / 如何衡量成功

A successful Memory Brain should demonstrate measurable system properties:

- **Continuity:** useful memories remain available across sessions and supported agent/model changes.
- **Traceability:** each derived memory can be traced to its source evidence and transformation history.
- **Correctness:** conflicting, stale, superseded, or withdrawn information is handled according to explicit policy.
- **Forgetting correctness:** withdrawn information does not reappear through retries, delayed producers, indexes, caches, reconnects, or recovery.
- **Application evidence:** the system can distinguish a context being generated, delivered, and actually applied.
- **Interoperability:** more than one independently implemented Agent Adapter can use the same canonical memory authority.
- **Efficiency:** retrieval and synchronization meet measured latency and resource budgets on declared workloads.

这些指标目前是验收目标，不是已取得的性能或生产成果。具体阈值应在代表性工作负载和实现基线建立后确定。

## 8. Who this project is for / 面向谁

- **Agent and AI application builders** who need memory continuity beyond a single conversation or vendor.
- **Infrastructure engineers** building long-running, multi-agent, or stateful AI systems.
- **Platform and enterprise architects** who need memory ownership, isolation, provenance, retention, audit, and deletion guarantees.
- **Researchers and contributors** interested in memory semantics, agent interoperability, context synchronization, and reliable forgetting.

## 9. Explore the repository / 如何阅读仓库

Start with the [Documentation Portal](docs/README.md). It provides bilingual reading paths, terminology, documentation status, and links to subsystem guides.

Recommended entry points:

- [System Architecture Overview](01-system-architecture/system-overview.md) — mission, boundaries, logical architecture, and data flows.
- [Component Map](01-system-architecture/component-map.md) — subsystem responsibilities and external participants.
- [Responsibility Matrix](01-system-architecture/responsibility-matrix.md) — ownership and boundaries.
- [Architecture Roadmap](ARCHITECTURE_ROADMAP.md) — staged design and implementation progression.
- [Bilingual Documentation Policy](00-governance/bilingual-documentation-policy.md) — requirements for Chinese/English architecture changes.
- [Prompt Library](prompts/README.md) — canonical AI development prompts and Owner-specific workflows.

建议从[双语文档入口](docs/README.md)开始，了解阅读路径、术语、文档状态和各子系统指南。之后阅读[系统架构总览](01-system-architecture/system-overview.md)、[组件地图](01-system-architecture/component-map.md)、[职责矩阵](01-system-architecture/responsibility-matrix.md)和[架构路线图](ARCHITECTURE_ROADMAP.md)。

### Documentation and decision discipline / 文档与决策纪律

This README contains Chinese and English in a single file; there is no separate Chinese README. **Translation status: PARTIAL.** Chinese coverage includes the project introduction, status explanation, problem summary, positioning, core three-layer model, strategic-value summary, interoperability summary, roadmap priorities summary, repository navigation, and long-term thesis. The following detailed material remains English-only in this revision and is explicitly **NOT_TRANSLATED**: the project-status table; the “What the architecture is designed to provide” and “What we are not” lists; the logical-architecture table; detailed subsections 4.1–4.5; the five-stage roadmap table and six-item near-term priority list; the success-metric list; the target-audience list; and the detailed repository entry-point list.

The repository's normative architecture documents are maintained in Chinese and English. Both versions must preserve the same meaning, constraints, stable identifiers, decision status, failure cases, and acceptance criteria. A translation must never promote a CANDIDATE, OPEN, or TO_VALIDATE item into a decided requirement.

Significant design statements use explicit status labels such as **DECIDED**, **CANDIDATE**, **TO_VALIDATE**, and **OPEN**. A component name alone is not sufficient to authorize implementation: responsibilities, boundaries, inputs, outputs, state transitions, failure behavior, security constraints, and acceptance criteria must first be specified. Implementation and acceptance claims must be backed by reproducible evidence.

Substantive development follows the repository's AI development governance: named accountable Owners, versioned prompts, isolated changes, reproducible verification, independent review, and preservation of the exact prompt version in the Work Item evidence bundle. Every AI session must use the [canonical Prompt Library](prompts/README.md). See [GOV-DOC-001](00-governance/bilingual-documentation-policy.md), the [AI Development Standard](14-ai-development/ai-development-standard.md), and the [Iteration Lifecycle](14-ai-development/iteration-lifecycle.md).

本 README 在同一个文件中包含中英文内容；仓库没有单独的中文 README 文件。**翻译状态：PARTIAL（部分翻译）。** 已有中文内容覆盖项目介绍、状态说明、问题摘要、项目定位、三层核心模型、战略价值摘要、互操作摘要、路线图优先级摘要、仓库导航和长期判断。以下详细内容在本修订中仍仅提供英文，明确标记为 **NOT_TRANSLATED（尚未翻译）**：项目状态表；“架构目标”和“我们不是什么”列表；逻辑架构表；第 4.1–4.5 节详细说明；五阶段路线图表及六项近期优先级清单；成功指标清单；目标读者清单；仓库详细入口清单。

仓库规范性架构文档采用中英双语维护，两种语言必须保持相同的含义、约束、稳定标识、决策状态、故障场景和验收标准。翻译不得把 CANDIDATE、OPEN 或 TO_VALIDATE 提升为已决议要求。

重要设计结论使用明确状态标记。仅仅为组件命名并不足以授权开始实现；必须先明确职责、边界、输入、输出、状态转换、故障行为、安全约束和验收标准。实现和验收结论必须有可复现证据。

实质性开发遵循仓库 AI 开发治理要求：具名责任 Owner、版本化提示词、隔离变更、可复现验证、独立审查，并在 Work Item 证据包中保留准确执行的提示词版本。每个 AI 会话都必须使用[规范提示词目录](prompts/README.md)。参见 [GOV-DOC-001](00-governance/bilingual-documentation-policy.md)、[AI Development Standard](14-ai-development/ai-development-standard.md) 和 [Iteration Lifecycle](14-ai-development/iteration-lifecycle.md)。

---

## 10. Long-term thesis / 长期判断

As model providers absorb more generic memory features, the value of a standalone project will not come from rebuilding those features one by one. It will come from solving the problems that remain across providers: independent memory ownership, portable semantics, provenance, lifecycle governance, reliable forgetting, applied-context evidence, and cross-agent interoperability.

Our strategic test is simple:

> **If an agent or model is replaced tomorrow, can its useful memory remain correct, governed, auditable, and usable by the next one?**

That is the problem AI Memory Brain is being designed to solve.

随着模型厂商不断吸收通用记忆能力，独立项目的价值不会来自重复实现每一种记忆功能，而应来自跨厂商仍然存在的问题：独立记忆所有权、可迁移语义、来源追溯、生命周期治理、可靠遗忘、上下文应用证据，以及跨 Agent 互操作。

我们的长期检验标准是：

> **如果明天更换一个 Agent 或模型，它积累的有价值记忆能否仍然正确、受治理、可审计，并被下一个系统继续使用？**

AI Memory Brain 正是围绕这个问题而设计。
