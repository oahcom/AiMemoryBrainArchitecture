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

## 4. Temporal and provenance standards / 时间与溯源标准

### PROV-O
- W3C Recommendation, “PROV-O: The PROV Ontology”: https://www.w3.org/TR/prov-o/ (accessed 2026-11-17).

PROV-O's compact starting point is Entity, Activity and Agent, connected by relations such as used, wasGeneratedBy, wasAssociatedWith, wasAttributedTo and wasDerivedFrom. Qualified relations can capture roles and responsibility. This maps well to Brain's source artifacts, derivation processes and responsible actors.

**Adoption:** borrow the conceptual pattern, not necessarily the namespace or RDF serialization. Memory/Evidence/Claim are project-specific types; PROV-O Entity is a broad provenance class and must not be blindly equated to the project's Entity.

### Bitemporal history
- Existing project source already separates Valid Time from Record Time and preserves both histories.
- Recommend selective bitemporal support for Claims/Relations and Memory revisions where users need “valid at T” and “known by T2”.
- Avoid imposing bitemporal columns on every object; keep Occurred At, Observed At, Recorded At, Valid Time and Storage Transaction Time distinct.

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

Observed model: memory extraction and retrieval pipeline; user/agent/app/run scope dimensions; SQL facts/metadata, vector embeddings and entity store; platform graph connections link memory nodes through extracted entities and boost retrieval. Current Graph Memory documentation says connections are entity-to-memory/co-occurrence based, not typed semantic relations such as “manages”. Official repository docs describe ADD-only extraction for the current algorithm, with explicit update/delete operations still available at API level; do not overgeneralize “ADD-only” to every API mutation.

Borrow: separating scope IDs from extracted graph entities; multi-signal retrieval and entity linking as a projection/ranking aid.
Do not copy: platform-specific hidden extraction pipeline as canonical truth; untyped co-occurrence edges as substitutes for typed Relation; no evidence that this model supplies this project's strict Forget atomicity and provenance guarantees.

### 6.3 Letta
- Official docs “Stateful agents”: https://docs.letta.com/concepts/stateful-agents
- Official docs “Memory & dreaming”: https://docs.letta.com/configuration/memory

Observed model: persistent Agent identity with memory, model/tool configuration and multiple conversations; memory shared across an Agent's conversations. MemFS is a git-backed memory filesystem with inspectable/editable files; dreaming consolidates recent interactions.

Borrow: explicit separation between persistent Agent identity and conversations; inspectable memory state and versioned changes.
Do not copy: agent-owned memory filesystem as the Brain's canonical domain model; Agent identity and conversation semantics are product-specific to Letta.

### 6.4 LangGraph
- Official checkpoint reference: https://langchain-ai.github.io/langgraph/reference/checkpoints/
- Official persistence guide: https://langchain-ai.github.io/langgraph/cloud/concepts/threads/

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

## 8. Limitations and evidence discipline / 局限与证据纪律

- Product documentation describes product behavior, not independent proof of correctness or performance.
- Mem0's official repository and documentation were inspected at the current documentation level; version-specific behavior must be pinned before any implementation decision.
- Zep pages expose different documentation generations (v2 and v4); findings are version-scoped, not a claim that all versions share one model.
- No benchmark, source-level comparative experiment, deployment test or production conformance was run by this research.
- External sources accessed on 2026-11-17; version numbers are stated only where the source identifies them (PostgreSQL 18; JSON Schema 2020-12; OWL 2 Second Edition; RDF 1.1; PROV-O).
- This research does not authorize technology selection or schema freeze.

## 9. Gate status / 门禁状态

This report completes a first official-source research pass for DDD, Event Sourcing, PROV-O, RDF/OWL, Zep/Graphiti, Mem0, Letta, LangGraph, Temporal, PostgreSQL and JSON Schema. It does not close B2/B3, and it is not an independent review or technology ADR.

本报告完成了 DDD、Event Sourcing、PROV-O、RDF/OWL、Zep/Graphiti、Mem0、Letta、LangGraph、Temporal、PostgreSQL 和 JSON Schema 的第一轮官方来源研究。但不关闭 B2/B3，也不构成独立审查或技术 ADR。
