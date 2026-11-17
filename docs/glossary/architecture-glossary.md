# AI Memory Brain — Bilingual Architecture Glossary / 中英架构术语表

- Document ID: DOC-GLOSSARY-001
- Version: 1.0
- Status: Shared terminology baseline

Terms are listed English-first because identifiers and protocol contracts use stable English names. Chinese equivalents explain the concepts; they do not replace field names, enum values, type names, or ADR identifiers.

| Canonical term | 中文术语 | Definition / 定义 |
|---|---|---|
| AI Memory Brain / Brain | AI 记忆大脑 / Brain | Agent- and model-independent authority for memory assets and managed context. / 独立于 Agent 和模型的记忆资产及受管上下文权威。 |
| Agent | 智能体 | System that reasons, plans, selects actions, and invokes tools. / 负责推理、规划、选择行动和调用工具的系统。 |
| Agent Adapter | Agent 适配器 | Maps Agent telemetry and applies Brain-managed context at an inference boundary. / 映射 Agent 遥测，并在推理边界应用 Brain 管理的上下文。 |
| Event | 事件 | Captured occurrence, observation, report, or transition. / 被记录的发生、观察、报告或状态变化。 |
| Memory | 记忆资产 | Retained, addressable knowledge asset; not a guarantee of truth. / 被保留且可寻址的知识资产，不等于事实保证。 |
| Claim | 命题 / 主张 | Proposition about an entity, event, or state, with epistemic and temporal qualifications. / 关于实体、事件或状态的命题，具有认知和时间限定。 |
| Fact | 事实 | Its canonical relationship to Claim is governed by the approved domain decision. / 与 Claim 的规范关系以正式领域决议为准。 |
| Entity | 实体 | Identity-bearing referent about which memories and claims are organized. / 具有身份的指代对象，记忆和命题围绕其组织。 |
| Relation | 关系 | Typed association between domain objects, potentially scoped and temporal. / 领域对象之间有类型的关联，可带范围和时间属性。 |
| Evidence | 证据 | Source material or observation supporting, refuting, or qualifying a Claim. / 支持、反驳或限定命题的来源材料或观察。 |
| Provenance | 来源链 / 溯源 | Traceable origin and derivation history. / 可追踪的来源与派生历史。 |
| Canonical Memory | 权威记忆 | Authoritative persisted memory asset and its version history. / 权威持久化记忆资产及其版本历史。 |
| Memory Context | 记忆上下文 | Scoped, versioned, task-oriented view of selected memory assets. / 对选定记忆资产形成的、有范围和版本的任务化视图。 |
| Context Entry | 上下文条目 | Reference or presentation of a memory within one Context. / 某个上下文中的记忆引用或呈现。 |
| Applied Context | 已应用上下文 | Context version the Adapter confirms was applied at the agreed inference boundary. / Adapter 确认已在约定推理边界应用的上下文版本。 |
| Working Set | 工作集 | Bounded runtime-local set of active memory references or data. / 运行时本地、有容量上限的活跃记忆引用或数据集合。 |
| Telemetry | 遥测信号 | Structured Agent/task/environment signals; not hidden chain-of-thought. / 结构化 Agent、任务和环境信号，不是隐藏思维链。 |
| BMCP | Brain Memory Context Protocol（大脑记忆上下文协议） | Brain-defined contracts for telemetry, context delivery, acknowledgement, and governance. / Brain 定义的遥测、上下文交付、确认和治理契约。 |
| Scope | 作用域 / 数据范围 | Namespace or ownership context to which an asset or operation belongs. / 资产或操作所属的命名空间或归属范围。 |
| Permission | 权限 | Authorization to perform an operation on a scoped resource. / 对特定范围资源执行操作的授权。 |
| Principal | 安全主体 | Authenticated identity to which authorization decisions are bound. / 授权决策所绑定的已认证身份。 |
| PermissionEpoch | 权限纪元 | Version token for a policy domain's permission state; not interchangeable with ForgetFenceGeneration. / 某策略域权限状态的版本标识，不可与 ForgetFenceGeneration 互换。 |
| Forget | 遗忘 / 受治理删除 | Governed revocation/removal workflow covering canonical memory and applicable derivatives. / 覆盖权威记忆及适用派生物的受治理撤销与清理流程。 |
| Forget Fence | 遗忘栅栏 | Durable barrier preventing stale or late work from publishing or exposing forgotten content. / 阻止过期或迟到任务发布、暴露已遗忘内容的持久化屏障。 |
| Producer Barrier | 生产者屏障 | Boundary defining which producer work a Forget operation must account for. / 确定某次 Forget 必须处置哪些生产者任务的边界。 |
| CanonicalCommitCursor | 权威提交游标 | Ordered cursor for commits within one Canonical Memory Authority. / 单个 Canonical Memory Authority 内有序提交的游标。 |
| IndexWatermark | 索引水位 | Progress marker for a specific index/channel partition. / 特定索引或通道分区的处理进度标识。 |
| ContextVersion | 上下文版本 | Authoritative version in a Context's own version sequence. / 某个 Context 自身权威版本序列中的版本。 |
| Delivery | 投递 | Transfer of a Context snapshot or change to an Adapter. / 向 Adapter 传送 Context 快照或变更。 |
| Acknowledgement / ACK | 确认 | Protocol response with a defined meaning; receipt is not automatically application. / 具有明确语义的协议响应；收到不自动等于已应用。 |
| Idempotency | 幂等性 | Repeating an operation within its defined key scope does not create a second logical effect. / 在规定幂等键范围内重复操作不会产生第二次逻辑效果。 |
| Outbox | 发件箱 | Durable record of work/messages committed with the state that requires them. / 与触发它的状态一起持久化的工作或消息记录。 |
| Replay | 重放 | Reprocessing durable work under current authorization and version rules. / 在当前授权和版本规则下重新处理持久化任务。 |
| Anti-resurrection | 防复活 | Preventing stale derivatives, indexes, caches, or restores from reintroducing revoked memory. / 防止过期派生物、索引、缓存或恢复过程重新引入已撤销记忆。 |
| ADR | 架构决策记录 | Explicit record of a decision, alternatives, rationale, and consequences. / 记录决策、备选方案、理由和影响的正式文档。 |

## Required conceptual distinctions / 必须保持的概念区分

- **Epistemic Status（认知状态）** describes the basis on which a Claim is known or supported.
- **Lifecycle State（生命周期状态）** describes the management stage of a Memory asset.
- **Confidence（置信度）** describes support strength under a declared method.
- **Relevance（相关性）** describes usefulness for a task at a particular time.
- **Scope（作用域）** describes where an asset belongs.
- **Permission（权限）** describes who may perform which operation.
- **ForgetFenceGeneration（遗忘栅栏代数）** and **PermissionEpoch（权限纪元）** are separate typed tokens.
- **Context Remove（上下文移除）** is not **Forget（遗忘）**.
- **Adapter Applied（适配器已应用）** is not proof of model comprehension or behavioral compliance.

## Translation rule / 翻译规则

Do not translate stable identifiers in code, schemas, APIs, logs, or protocol payloads. In prose, introduce a Chinese explanation on first use and retain the canonical English term in parentheses where ambiguity is possible. Do not create multiple Chinese translations for one canonical term without an explicit glossary decision.
