# Mature Domain Modeling and Reference Architecture Research
# 成熟领域建模与参考架构研究

- ID: B-RESEARCH-001
- Status: RESEARCH SYNTHESIS — CANDIDATE RECOMMENDATIONS, NOT TECHNOLOGY OR ARCHITECTURE FREEZE
- Research date: 2026-11-17
- Scope: DDD, Event Sourcing, Temporal Models, Provenance, Knowledge Graph/Ontology, memory systems, workflow/runtime persistence, JSON Schema.

## 1. Executive synthesis / 研究结论

The project should adopt **selective DDD semantics**, not mechanically apply every tactical pattern. Keep one shared canonical vocabulary and explicit bounded semantic ownership, while allowing each Owner to maintain its own model and state machine. Do not require a microservice per Bounded Context or a distributed deployment: repository principles explicitly allow subsystem boundaries without process/service/crate boundaries.

本项目应采用**选择性 DDD 语义**，而不是机械套用全部战术模式。保持共享规范词汇和明确的领域权威边界，同时允许各 Owner 维护自己的局部模型和状态机。不要求每个 Bounded Context 都成为微服务，也不要求分布式部署：仓库原则明确允许子系统边界不等于进程/服务/Crate 边界。

Recommended minimum:
- Canonical domain entities and typed references for identity-bearing concepts.
- Value objects for qualifiers, scopes as typed refs, time intervals, locators and digests.
- Explicit association records only where relationship role/time/scope/evidence has independent meaning.
- Immutable versions and append-only audit evidence where history matters; state-based canonical persistence remains viable.
- Selective bitemporal semantics for time-qualified claims/relations, not every field/object.
- Provenance modeled with the small PROV-O conceptual core (Entity/Activity/Agent) where useful, without adopting RDF/OWL as a storage mandate.
- Relational/transactional canonical model first; graph projections are derived views until query/use-case evidence justifies a first-class graph store.

建议的最小模型：身份对象使用规范实体和类型化引用；限定符、Scope 引用、时间区间、Locator、Digest 使用值对象；只有当关系角色/时间/Scope/证据具有独立含义时才建立显式关联记录；对确需历史的对象使用不可变版本和追加式审计证据，同时保留状态型规范持久化的可行性；对带时间的 Claim/Relation 选择性使用双时态语义；在需要处借鉴 PROV-O 的 Entity/Activity/Agent 小型概念核心，但不强制 RDF/OWL 存储；优先关系型/事务型规范模型，图投影先作为派生视图。

## 2. DDD / bounded contexts / 聚合

### Official references
- Microsoft Learn, “Design a microservice domain model” (published in .NET architecture guidance; accessed 2026-11-17): https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model
- Microsoft Learn, “Designing a DDD-oriented microservice”: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice
- Martin Fowler, “Bounded Context” (2014-01-15): https://martinfowler.com/bliki/BoundedContext.html
- Martin Fowler, “DDD Aggregate” (2013-04-23): https://martinfowler.com/bliki/DDD_Aggregate.html

### Observed principles
- An Entity is identified by identity/continuity, not merely its attributes.
- A Value Object has no conceptual identity; equality is by value.
- A Bounded Context contains a coherent model and ubiquitous language; the same real-world referent can have different context-local representations.
- An Aggregate is selected around invariants that must be consistent together in actual transactions; the Aggregate Root is the consistency gate.
- DDD is useful where domain rules are complex and changing; simpler CRUD responsibilities do not justify the full tactical pattern set.

### Application to AI Memory Brain
- Use bounded contexts as **semantic ownership boundaries**: Canonical Memory/Lifecycle (D), Compiler (E), Runtime (F), Context (G), Protocol (H), Security/Governance (I), Storage/Consistency and system integration (A).
- B defines shared domain meaning and reference rules, but does not force all Owner-local models to share identical internal types.
- Candidate aggregates should be based on proven invariants: Memory + current version pointer may be one canonical consistency boundary; ForgetOperation + fence/barrier may be a D-owned operation boundary; Context + ContextVersion/ChangeSet are G-owned. Exact aggregate design remains D/G/Storage authority, not B unilateral design.
- Cross-aggregate references should be typed references and owner contracts, not shared mutable object graphs.
- Do not invent a generic AggregateRoot base class or force all objects into aggregates.

**Disposition:** DECIDED recommendation to use DDD's strategic bounded-context and ubiquitous-language concepts; CANDIDATE use of aggregates only after transaction/invariant analysis.

**中文：** 将 Bounded Context 和统一语言作为领域划分工具；聚合只围绕真实事务不变量确定。不要建立通用 AggregateRoot 基类，也不要把所有对象都强制放入聚合。

## 2A. Chinese DDD findings / 中文 DDD 研究结论

- Entity 通过身份和连续性识别，而不只是属性相等；Value Object 没有概念身份，按值相等。
- Bounded Context 包含一致的模型和统一语言；同一个现实对象可在不同 Context 中具有不同的局部表示。
- Aggregate 应围绕必须在真实事务中共同保持的不变量选择；Aggregate Root 是一致性入口。
- DDD 适合复杂且不断变化的领域规则；简单 CRUD 不足以证明必须采用完整战术模式。
- 本项目应把 Bounded Context 用作语义权威边界，不要求每个 Context 对应一个微服务、进程或 Crate。
- 候选聚合由 D/G/Storage 根据真实事务和不变量决定；B 不得单方面冻结 Memory、Forget 或 Context 聚合。
- 跨聚合引用应使用类型化引用和 Owner 契约，不共享可变对象图；不建立通用 AggregateRoot 基类。

## 3. Event Sourcing and state-based persistence / 事件溯源与状态持久化

### Reference
- Martin Fowler, “Event Sourcing”: https://martinfowler.com/eaaDev/EventSourcing.html (accessed 2026-11-17).

The reference explains that state can be rebuilt by replaying events, but replay can be slow and snapshots/current-state storage may be added. It also highlights complexity when replay interacts with external systems, code changes and time-dependent external queries.

### Application
The project needs durable event capture, immutable Memory Versions, audit history, deterministic recovery for some owner workflows, and Forget-safe replay. These needs do **not** imply that every domain object must be event-sourced.

Recommended split:
- Event/source ingestion: preserve immutable accepted source facts and acceptance evidence where retention permits.
- Canonical Memory: state-based current aggregate + immutable version history + append-only lifecycle/audit records is a viable minimum.
- Forget/authorization/commit operations: owner-specific durable operation ledgers and receipts are required because recovery/ordering matters; these are not automatically full-system Event Sourcing.
- Derived indexes, summaries, retrieval results and Context projections should be rebuildable from canonical sources and explicit owner events/receipts.
- Replaying must not repeat provider side effects; C idempotency and same-operation reconciliation remain mandatory.

**Rejected:** universal Event Sourcing as default. It increases event schema evolution, replay determinism, external side-effect fencing, retention/Forget, migration and snapshot complexity. Adopt full event sourcing only where audit/replay requirements and measured benefits justify it.

**中文：** 不将全系统 Event Sourcing 作为默认。推荐对 Memory 使用当前状态 + 不可变版本 + 追加式生命周期/审计记录；对 Forget、授权和提交等确实需要恢复/排序的操作保留专用持久操作账本和 Receipt。只有经实际需求和复杂度论证后，才对特定边界采用完整事件溯源。

### 中文 Event Sourcing 研究结论

Event Sourcing 可以通过重放事件重建状态，但重放可能缓慢；可加入 Snapshot/Current State。与外部系统、副作用、代码升级和时间相关外部查询交互时，复杂度会显著增加。

本项目需要持久事件捕获、不可变 Memory Version、审计历史，以及部分 Owner 工作流的确定性恢复和 Forget-safe Replay；这些需求不意味着所有领域对象都必须采用 Event Sourcing。

推荐划分：
- 来源摄取：在保留策略允许时保存不可变已接受来源事实及接受证据。
- 规范 Memory：当前聚合状态 + 不可变版本历史 + 追加式生命周期/审计记录。
- Forget/Authorization/Commit：对需要恢复/排序的 Owner 工作流使用专属持久操作账本和 Receipt；这不等于全系统事件溯源。
- Index、Summary、Retrieval Result 和 Context Projection 应能从规范来源及显式 Owner 事件/Receipt 重建。
- Replay 不得重复执行 Provider 副作用；C Idempotency 和同一操作协调仍是强制要求。

拒绝将 Universal Event Sourcing 作为默认，因为它增加 Event Schema 演进、重放确定性、外部副作用 Fence、保留/Forget、迁移和 Snapshot 复杂度。只有当审计/重放要求和可测收益足以证明时，才对特定边界采用完整 Event Sourcing。

## 4. Temporal and provenance standards / 时间与溯源标准

### PROV-O
- W3C Recommendation, “PROV-O: The PROV Ontology”: https://www.w3.org/TR/prov-o/ (accessed 2026-11-17).

PROV-O's compact starting point is Entity, Activity and Agent, connected by relations such as used, wasGeneratedBy, wasAssociatedWith, wasAttributedTo and wasDerivedFrom. Qualified relations can capture roles and responsibility. This maps well to Brain's source artifacts, derivation processes and responsible actors.

**Adoption:** borrow the conceptual pattern, not necessarily the namespace or RDF serialization. Memory/Evidence/Claim are project-specific types; PROV-O Entity is a broad provenance class and must not be blindly equated to the project's Entity.

### Bitemporal history
- Existing project source already separates Valid Time from Record Time and preserves both histories.
- Recommend selective bitemporal support for Claims/Relations and Memory revisions where users need “valid at T” and “known by T2”.
- Avoid imposing bitemporal columns on every object; keep Occurred At, Observed At, Recorded At, Valid Time and Storage Transaction Time distinct.

### 中文 PROV-O 研究结论

PROV-O 的精简起点是 Entity、Activity、Agent，并通过 used、wasGeneratedBy、wasAssociatedWith、wasAttributedTo、wasDerivedFrom 等关系连接；Qualified Relation 可记录角色和责任。这与 Brain 的来源产物、派生过程和负责 Actor 对应。

采纳方式：借鉴概念模式，不强制使用其 Namespace 或 RDF 序列化。Memory/Evidence/Claim 是项目专属类型；PROV-O Entity 是宽泛溯源类，不得直接等同项目 Entity。

### 中文双时态历史结论

- 项目现有源规范已经区分 Valid Time 与 Record Time，并要求保留两者历史。
- 建议对需要回答“在 T 时有效、在 T2 时系统已知”的 Claim/Relation 和 Memory Revision 选择性支持双时态。
- 不要对每个对象强加双时态字段；Occurred At、Observed At、Recorded At、Valid Time 和 Storage Transaction Time 必须区分。

## 5. Knowledge Graph, RDF and OWL / 知识图谱、RDF 与 OWL

### Standards
- W3C, “RDF 1.1 Concepts and Abstract Syntax”: https://www.w3.org/TR/rdf-concepts/
- W3C, “OWL 2 Web Ontology Language Document Overview”: https://www.w3.org/TR/owl2-overview/

RDF models a graph as subject-predicate-object triples and datasets as named/default graphs. The RDF data model is atemporal by itself; temporal meaning requires explicit vocabulary. OWL 2 adds formally defined ontology semantics for classes, properties, individuals and data values, with inference capabilities and profiles.

### Application
- The existing project Relation model is already a typed association with endpoint constraints, directionality, Scope, Valid Time, epistemic status and Evidence.
- This is more expressive than untyped entity co-occurrence. Preserve typed Relation semantics.
- A relational model plus explicit relation records and provenance edges is sufficient as the initial canonical representation.
- Graph projection may be useful for entity-centric retrieval, multi-hop traversal and lineage exploration, but graph storage is not a domain requirement.
- RDF/OWL should be deferred until there is a concrete need for cross-system semantic interoperability, formal ontology reasoning, shared externally governed vocabulary or automated entailment.
- If introduced, define mappings from canonical types to ontology terms and preserve source IDs/authority; never let inferred triples silently become verified Claims.

**Disposition:** graph projection CANDIDATE; RDF/OWL DEFERRED; no graph database or ontology stack selected.

**中文：** 初始规范表示采用关系模型 + 显式 Relation 记录 + Provenance 边即可。图投影可用于实体检索和多跳遍历，但图数据库不是领域必需。只有出现跨系统语义互操作、正式本体推理或外部共享词汇治理需求时，才评估 RDF/OWL。

### 中文 RDF / OWL 研究结论

RDF 以 Subject-Predicate-Object 三元组表达图，Dataset 由 Default/Named Graph 组成；RDF 本身不提供时间语义，需要显式词汇。OWL 2 提供 Classes、Properties、Individuals 和 Data Values 的形式化本体语义及推理能力/Profile。

项目已有 Relation 模型包含类型化关联、端点约束、方向、Scope、Valid Time、认知状态和 Evidence，优于无类型共现边。初始规范表示采用关系模型 + 显式 Relation 记录 + Provenance Edge 已足够。

图投影可用于 Entity-centric Retrieval、多跳遍历和谱系探索，但 Graph Storage 不是领域要求。只有在跨系统语义互操作、正式本体推理、外部共享词汇治理或自动蕴含确有需求时，才评估 RDF/OWL。即使引入，也必须保留来源 ID/权威，不得让推断 Triple 静默变成 Verified Claim。

处置：Graph Projection 为 CANDIDATE；RDF/OWL 为 DEFERRED；未选择图数据库或本体技术栈。

## 6. Mature project references / 成熟项目参考

### 6.1 Zep / Graphiti
- Zep v4 “How Graph Creation Works”: https://help.getzep.com/how-graph-creation-works
- Zep v2 “Understanding the Graph”: https://help.getzep.com/v2/understanding-the-graph
- Graphiti official repository README: https://github.com/getzep/graphiti

Observed model: raw source is stored as an Episode; extraction derives Entity nodes and temporal relationship/fact edges; derived observations/summaries are additional context artifacts. Source episodes provide provenance. Graphiti describes validity windows and temporal history.

Borrow: explicit source Episode → derived entities/edges, temporal relation history, provenance back-links.
Do not copy: automatically adopting a graph database or assuming extracted edges are verified truth. B's model requires epistemic status, explicit evidence role and owner lifecycle controls.

### 6.2 Mem0
- Official repository: https://github.com/mem0ai/mem0
- Official Graph Memory documentation source: https://github.com/mem0ai/mem0/blob/main/docs/platform/features/graph-memory.mdx
- Official “How Mem0 Works”: https://github.com/mem0ai/mem0/blob/main/docs/core-concepts/how-it-works.mdx
- Official architecture reference: https://github.com/mem0ai/mem0/blob/main/skills/mem0/references/architecture.md

Observed model: memory extraction and retrieval pipeline; user/agent/app/run scope dimensions; SQL facts/metadata, vector embeddings and entity store; platform graph connections link memory nodes through extracted entities and boost retrieval. Current Graph Memory documentation says connections are entity-to-memory/co-occurrence based, not typed semantic relations such as “manages”. The current official source validation supplement records the observed extraction/scope/graph model and its limits; no unsupported claim about all API mutation behavior is made here.

Borrow: separating scope IDs from extracted graph entities; multi-signal retrieval and entity linking as a projection/ranking aid.
Do not copy: platform-specific hidden extraction pipeline as canonical truth; untyped co-occurrence edges as substitutes for typed Relation; no evidence that this model supplies this project's strict Forget atomicity and provenance guarantees.

### 6.3 Letta
- Official docs “Stateful agents”: https://docs.letta.com/concepts/stateful-agents
- Official docs “Memory & dreaming”: https://docs.letta.com/configuration/memory

Observed model: persistent Agent identity with memory, model/tool configuration and multiple conversations; memory shared across an Agent's conversations. MemFS is a git-backed memory filesystem with inspectable/editable files; dreaming consolidates recent interactions.

Borrow: explicit separation between persistent Agent identity and conversations; inspectable memory state and versioned changes.
Do not copy: agent-owned memory filesystem as the Brain's canonical domain model; Agent identity and conversation semantics are product-specific to Letta.

### 6.4 LangGraph
- Official checkpoint reference: https://docs.langchain.com/oss/python/langgraph/persistence
- Official persistence guide: https://docs.langchain.com/oss/python/langgraph/persistence

Observed model: checkpoint is a snapshot of graph state at a point in time, identified by a unique monotonically increasing ID; thread_id groups checkpoints; pending writes enable resumption. Checkpointers support thread-scoped short-term state; Stores support long-term cross-thread data.

Borrow: distinguish Session/Thread execution state from long-term memory Store; checkpoint identity/version is not canonical Memory identity.
Do not copy: graph execution checkpoint as Brain MemoryVersion or ContextVersion. They represent different state authorities.

### 6.5 Temporal
- Official “Event History”: https://docs.temporal.io/encyclopedia/event-history
- Official “Understanding Temporal”: https://docs.temporal.io/evaluate/understanding-temporal

Observed model: Workflow Event History is a durable ordered record for one Workflow Execution. Workflow code emits Commands; service persists resulting Events; replay reconstructs execution state after failure.

Borrow: durable operation history, command-vs-event distinction, replay evidence and deterministic recovery discipline for long-running Forget/commit workflows.
Do not copy: treating every Memory mutation as a Temporal Workflow or making Temporal a required runtime dependency. Workflow history is an execution log, not the canonical memory domain.

### 6.6 PostgreSQL
- PostgreSQL 18 documentation, Chapter 13 “Concurrency Control”: https://www.postgresql.org/docs/current/mvcc.html
- PostgreSQL 18 “Transaction Isolation”: https://www.postgresql.org/docs/current/transaction-iso.html

Observed model: MVCC snapshots provide transaction isolation; Serializable guarantees equivalence to serial execution but applications must handle serialization failures/retries. Repeatable Read can still permit serialization anomalies under PostgreSQL's documented behavior.

Borrow: understand snapshot visibility and serializable transaction semantics as physical implementation capabilities to validate against Storage contracts.
Do not copy: assuming the label SERIALIZABLE alone proves the project's JF-10 cross-authority crash/recovery protocol, same-XID resolution, D fence ordering or I authorization sequencing. Those require end-to-end fault proof and explicit contract participation.

### 6.7 JSON Schema
- Official specification: https://json-schema.org/specification
- Draft 2020-12: https://json-schema.org/draft/2020-12

Observed model: specification is split into Core and Validation; 2020-12 is the current published version identified by the official specification page at research time.

Borrow: use JSON Schema to validate stable, owner-approved serialized contracts and negative fixtures.
Do not copy: using JSON Schema as the source of domain semantics, state-transition rules, authorization, temporal ordering or cross-document invariants. Those require explicit semantic validation beyond structural schema.

## 6A. Chinese mature-project comparison / 中文成熟项目对照

| 项目/标准 | 实际模型观察 / 中文总结 | 可借鉴内容 | 不应照搬的内容 | 复杂度与采纳状态 |
|---|---|---|---|---|
| Zep / Graphiti | 原始来源以 Episode 保存；抽取派生 Entity 节点和带时间的关系/Fact Edge；来源 Episode 提供 Provenance；Graphiti 描述有效时间窗口和关系历史。 | Source Episode → Derived Entity/Edge；关系时间历史；Provenance 回链。 | 不自动采用 Graph DB；抽取 Edge 不等于 Verified Truth。 | 语义模式 CANDIDATE；图数据库未选择。 |
| Mem0 | 提取/检索流水线；User/Agent/App/Run Scope；SQL Facts/Metadata、Vector Embedding、Entity Store；Graph Memory 连接记忆节点和抽取 Entity，并辅助 Retrieval。 | Scope ID 与 Graph Entity 分离；多信号 Retrieval 和 Entity Linking 可作为投影/排序辅助。 | 不把平台内部抽取当作规范真值；无类型共现边不能替代类型化 Relation；没有证据证明其满足本项目严格 Forget Atomicity/Provenance。 | 可借鉴检索模式；规范模型不采纳其专属实现。 |
| Letta | 持久 Agent 身份、Memory、模型/工具配置和多个 Conversation；Memory 可跨 Conversation 共享；MemFS 为可检查/编辑的 Git-backed 文件系统；Dreaming 负责巩固。 | 区分持久 Agent 身份与 Conversation；Memory 状态可检查、版本化。 | 不把 Agent-owned 文件系统当作 Brain 规范领域模型；Agent/Conversation 语义具有产品特定性。 | 概念参考，不选用其产品架构。 |
| LangGraph | Checkpoint 是某时刻 Graph State Snapshot，具有唯一单调 ID；Thread ID 组织 Checkpoints；Pending Writes 支持恢复；Checkpointer 管 Thread 短期状态，Store 管跨 Thread 长期数据。 | 区分 Session/Thread 执行状态与长期 Memory Store；Checkpoint ID/Version 不等于规范 Memory ID。 | 不把 Graph Execution Checkpoint 当作 Brain MemoryVersion 或 ContextVersion。 | 执行状态参考，不作为领域实体。 |
| Temporal | Workflow Event History 是单个 Workflow Execution 的持久有序记录；Workflow Code 发出 Commands，Service 持久化 Events，Replay 可在故障后重建执行状态。 | 对长时 Forget/Commit 工作流借鉴持久操作历史、Command/Event 区分、Replay 证据和确定性恢复纪律。 | 不把每次 Memory 变更都建成 Temporal Workflow，也不把 Temporal 设为必需 Runtime 依赖。 | 操作账本参考；未选用引擎。 |
| PostgreSQL | MVCC Snapshot 提供事务隔离；Serializable 旨在等价于串行执行，但应用必须处理 Serialization Failure/Retry；Repeatable Read 仍可能出现文档所述异常。 | 把 Snapshot Visibility 和 Serializable 语义作为 Storage 物理能力验证。 | 不能仅凭 SERIALIZABLE 标签证明 JF-10 跨权威崩溃恢复、same-XID、D Fence 顺序或 I 授权顺序。 | 物理实现候选能力；Storage/A 拥有 ADR 和测试。 |
| JSON Schema | 规范分为 Core 和 Validation；2020-12 是研究时官方页面列出的已发布版本。 | 验证稳定且经 Owner 批准的序列化契约及 Negative Fixture。 | 不能用 Schema 代替领域语义、状态转换、授权、时间顺序或跨文档不变量。 | 推荐用于结构校验；不是领域语义源。 |
| W3C PROV-O | Entity/Activity/Agent 和 Qualified Relation 表达来源、过程和责任。 | 小型 Provenance 概念核心。 | 不要求 RDF Namespace/序列化，也不把 PROV Entity 等同项目 Entity。 | CANDIDATE。 |
| W3C RDF / OWL | RDF 三元组表达图；OWL 2 提供形式化本体和推理。 | 仅在互操作/正式推理需求出现时映射。 | 不因项目有 Memory 就默认部署完整 Ontology。 | DEFERRED。 |

## 7. Consolidated recommendations / 综合建议

| Topic | Recommendation | Status |
|---|---|---|
| DDD | Strategic DDD: bounded semantic ownership + ubiquitous language | DECIDED recommendation |
| Aggregates | Derive from actual invariants and transaction boundaries; no generic aggregate framework | CANDIDATE |
| Event Sourcing | Not universal; state + immutable revisions + targeted operation ledgers | RECOMMENDED |
| Temporal | Selective bitemporal Claims/Relations/revisions | CANDIDATE |
| Provenance | PROV-O-inspired Entity/Activity/Agent pattern | CANDIDATE |
| Knowledge Graph | Typed relational canonical graph; graph projection if retrieval use case proves value | RECOMMENDED |
| RDF/OWL | Defer formal ontology and reasoning | DEFERRED |
| JSON Schema | Validate approved wire/storage interchange contracts, not domain meaning | RECOMMENDED |
| PostgreSQL | Candidate implementation capability only; Storage/A owns final ADR and tests | NOT SELECTED |
| Temporal workflow engine | Reference for durable operation patterns only; not selected | NOT SELECTED |

## 7A. 中文综合建议表

| 主题 | 建议 | 状态 |
|---|---|---|
| DDD | 采用战略 DDD：语义有界上下文 + 统一语言。 | DECIDED recommendation |
| Aggregates | 从真实不变量和事务边界推导，不建立通用聚合框架。 | CANDIDATE |
| Event Sourcing | 不全局采用；使用状态 + 不可变 Revision + 专用操作账本。 | RECOMMENDED |
| Temporal | 对 Claim/Relation/Revision 选择性双时态。 | CANDIDATE |
| Provenance | 借鉴 PROV-O Entity/Activity/Agent 模式。 | CANDIDATE |
| Knowledge Graph | 规范层采用类型化关系型图；有检索证据时再建图投影。 | RECOMMENDED |
| RDF/OWL | 延后正式本体和推理。 | DEFERRED |
| JSON Schema | 验证已批准的 Wire/Storage 交换契约，不定义领域含义。 | RECOMMENDED |
| PostgreSQL | 仅作为物理能力候选；最终 ADR/测试由 Storage/A 决定。 | NOT SELECTED |
| Temporal Workflow Engine | 仅作持久操作模式参考；未选用。 | NOT SELECTED |

## 8. Limitations and evidence discipline / 局限与证据纪律

- Product documentation describes product behavior, not independent proof of correctness or performance.
- Mem0's official repository and documentation were inspected at the current documentation level; version-specific behavior must be pinned before any implementation decision.
- Zep pages expose different documentation generations (v2 and v4); findings are version-scoped, not a claim that all versions share one model.
- No benchmark, source-level comparative experiment, deployment test or production conformance was run by this research.
- External sources accessed on 2026-11-17; version numbers are stated only where the source identifies them (PostgreSQL 18; JSON Schema 2020-12; OWL 2 Second Edition; RDF 1.1; PROV-O).
- This research does not authorize technology selection or schema freeze.

### 中文局限与证据纪律

- 产品文档描述产品行为，不构成独立正确性或性能证明。
- Mem0 结论基于其当前官方仓库/文档；任何实现决定前必须 Pin 具体版本。
- Zep 页面来自 v2 和 v4 不同文档代际；结论必须限定版本，不能声称所有版本共用同一模型。
- 本研究未执行 Benchmark、源码对比实验、部署测试或生产一致性测试。
- 外部来源访问日期为 2026-11-17；仅在来源明确标识时记录版本号（PostgreSQL 18、JSON Schema 2020-12、OWL 2 Second Edition、RDF 1.1、PROV-O）。
- 本研究不授权技术选型或 Schema 冻结。

## 9. Gate status / 门禁状态

This report completes a first official-source research pass for DDD, Event Sourcing, PROV-O, RDF/OWL, Zep/Graphiti, Mem0, Letta, LangGraph, Temporal, PostgreSQL and JSON Schema. It does not close B2/B3, and it is not an independent review or technology ADR.

本报告完成了 DDD、Event Sourcing、PROV-O、RDF/OWL、Zep/Graphiti、Mem0、Letta、LangGraph、Temporal、PostgreSQL 和 JSON Schema 的第一轮官方来源研究。但不关闭 B2/B3，也不构成独立审查或技术 ADR。


## 10. Full Chinese peer for mature-project evidence / 成熟项目证据完整中文对照

### 10.1 Zep / Graphiti

**官方来源：**
- Zep v4《How Graph Creation Works》：https://help.getzep.com/how-graph-creation-works
- Zep v2《Understanding the Graph》：https://help.getzep.com/v2/understanding-the-graph
- Graphiti 官方仓库 README：https://github.com/getzep/graphiti

**观察到的模型：** 原始来源以 Episode 保存；抽取流程据此派生 Entity 节点以及带时间语义的 Relation/Fact Edge；其他派生观察或摘要可作为额外上下文产物。来源 Episode 提供溯源入口。Graphiti 文档描述关系有效时间窗口和时间历史。

**可借鉴：** 显式保留 Source Episode → Derived Entity/Edge 的来源链；保留关系时间历史；让派生关系可以回链到原始来源。

**不得照搬：** 不因 Graphiti 使用图模型就自动选择图数据库；不把抽取出的 Edge 当作已验证真值。B 的模型还必须保留认知状态、明确 Evidence 角色和 Owner 生命周期控制。

**适用边界：** 这些结论受所引用 Zep v2/v4 文档版本约束。不同文档代际不能被合并成“所有版本行为一致”的结论。

### 10.2 Mem0

**官方来源：**
- 官方仓库：https://github.com/mem0ai/mem0
- Graph Memory 官方文档源码：https://github.com/mem0ai/mem0/blob/main/docs/platform/features/graph-memory.mdx
-《How Mem0 Works》官方文档：https://github.com/mem0ai/mem0/blob/main/docs/core-concepts/how-it-works.mdx
- 官方架构参考：https://github.com/mem0ai/mem0/blob/main/skills/mem0/references/architecture.md

**观察到的模型：** 系统具有 Memory Extraction 和 Retrieval 流水线；Scope 维度包括 user、agent、app、run；存储组件包括 SQL Facts/Metadata、Vector Embeddings 和 Entity Store。平台 Graph Connections 将 Memory Nodes 与抽取出的 Entity 关联，用于辅助检索。当前 Graph Memory 文档描述的是 Entity 与 Memory 的连接/共现关系，不等于“管理”等类型化语义关系。当前官方来源验证补充记录了已观察到的抽取、Scope 和 Graph 模型及其限制；本研究不对所有 API Mutation 行为作无证据推断。

**可借鉴：** 将 Scope ID 与抽取出的 Graph Entity 分离；把多信号 Retrieval 和 Entity Linking 作为派生投影/排序辅助。

**不得照搬：** 不把平台内部、不可见的抽取流水线直接视为规范真值；无类型共现边不能替代类型化 Relation；没有证据证明该模型提供本项目要求的严格 Forget Atomicity 和 Provenance 保证。

**适用边界：** 观察结论来自研究时可访问的官方仓库和文档。实施决策前必须固定具体版本，并重新核验版本行为。

### 10.3 Letta

**官方来源：**
- Stateful Agents：https://docs.letta.com/concepts/stateful-agents
- Memory & dreaming：https://docs.letta.com/configuration/memory

**观察到的模型：** Agent 身份具有持久性，并关联 Memory、模型/工具配置及多个 Conversation；同一 Agent 的 Memory 可跨 Conversation 共享。MemFS 是基于 Git 的 Memory 文件系统，文件可检查和编辑；Dreaming 用于巩固近期交互。

**可借鉴：** 明确区分持久 Agent 身份和 Conversation；让 Memory 状态可检查，并能观察版本化变化。

**不得照搬：** 不把 Agent 自有 Memory 文件系统直接当作 Brain 的规范领域模型；Letta 的 Agent 身份与 Conversation 语义属于其产品模型，不能未经映射就成为本项目规范。

### 10.4 LangGraph

**官方来源：**
- Checkpoint/Persistence：https://docs.langchain.com/oss/python/langgraph/persistence

**观察到的模型：** Checkpoint 是某个时点 Graph State 的快照，具有唯一且单调递增的 ID；Thread ID 用于组织同一 Thread 的 Checkpoints；Pending Writes 支持从中断处恢复。Checkpointer 支持 Thread 范围的短期状态，Store 支持跨 Thread 的长期数据。

**可借鉴：** 区分 Session/Thread 执行状态与长期 Memory Store；Checkpoint 身份/版本不等于规范 Memory 身份。

**不得照搬：** 不把 Graph Execution Checkpoint 当作 Brain MemoryVersion 或 ContextVersion；三者属于不同状态权威和生命周期。

### 10.5 Temporal

**官方来源：**
- Event History：https://docs.temporal.io/encyclopedia/event-history
- Understanding Temporal：https://docs.temporal.io/evaluate/understanding-temporal

**观察到的模型：** Workflow Event History 是单个 Workflow Execution 的持久、有序记录。Workflow Code 发出 Command；Temporal Service 持久化执行产生的 Event；发生故障后通过 Replay 重建 Workflow 执行状态。

**可借鉴：** 对长时间运行的 Forget/Commit 工作流，借鉴持久操作历史、Command 与 Event 区分、Replay 证据和确定性恢复纪律。

**不得照搬：** 不把每次 Memory Mutation 都变成 Temporal Workflow；不把 Temporal 设为项目必需 Runtime 依赖。Workflow History 是执行历史，不是规范 Memory 领域模型。

### 10.6 PostgreSQL

**官方来源：**
- PostgreSQL 18《Concurrency Control》：https://www.postgresql.org/docs/current/mvcc.html
- PostgreSQL 18《Transaction Isolation》：https://www.postgresql.org/docs/current/transaction-iso.html

**观察到的模型：** MVCC Snapshot 提供事务隔离；Serializable 旨在保证结果等价于某种串行执行，但应用必须处理 Serialization Failure 并按规则重试。根据 PostgreSQL 文档，Repeatable Read 仍可能出现其定义的 Serialization Anomaly。

**可借鉴：** 将 Snapshot Visibility 和 Serializable Transaction 语义作为 Storage 物理实现能力，针对 Storage 契约验证。

**不得照搬：** 不能仅凭数据库隔离级别标签为 SERIALIZABLE，就声称已经证明项目的 JF-10 跨权威崩溃/恢复协议、Same-XID 决议、D Fence 顺序或 I Authorization Sequencing。这些要求必须由端到端故障证据和明确 Owner 契约参与来证明。

### 10.7 JSON Schema

**官方来源：**
- JSON Schema Specification：https://json-schema.org/specification
- Draft 2020-12：https://json-schema.org/draft/2020-12

**观察到的模型：** 规范分为 Core 与 Validation 两部分；研究时官方规格页面列出的已发布版本为 Draft 2020-12。

**可借鉴：** 使用 JSON Schema 验证稳定、已获 Owner 批准的序列化契约，并为 Negative Fixture 提供结构验证。

**不得照搬：** 不把 JSON Schema 当作领域语义来源。它不能单独定义状态转换、授权、时间排序或跨文档不变量；这些必须通过 Schema 以外的显式语义验证完成。

### 10.8 跨项目综合结论 / Cross-project synthesis

- 成熟项目普遍区分长期身份、短期执行状态、来源材料和派生投影；本项目应保持相同的类型边界，而不是把 Memory、Context、Checkpoint、Session 和 Graph Node 统一成一个通用对象。
- 图结构、向量索引、Checkpoint、Event History 和 JSON Schema 分别解决不同问题，不能互相替代，也不能因技术组件存在就推导出规范领域身份。
- 外部项目可提供模式和实现参考，但其产品文档不能证明本项目的 Forget、授权、Applied、Storage Publication 或生产恢复不变量。
- 所有借鉴均为候选设计输入；Owner 规范权威、精确版本 Pin、实现测试和独立验收仍然优先。

- 成熟项目普遍区分长期身份、短期执行状态、来源材料和派生投影；本项目必须保留相同类型边界，不能把 Memory、Context、Checkpoint、Session 和 Graph Node 统一为通用对象。
- Graph、Vector Index、Checkpoint、Event History 与 JSON Schema 解决不同问题，不能互相替代；不能因为存在某个技术组件，就推导出规范领域身份。
- 外部项目只提供模式和实现参考，其产品文档不能证明本项目的 Forget、授权、Applied、Storage Publication 或生产恢复不变量。
- 所有借鉴均是候选设计输入；Owner 规范权威、精确版本 Pin、实现测试和独立验收优先。
