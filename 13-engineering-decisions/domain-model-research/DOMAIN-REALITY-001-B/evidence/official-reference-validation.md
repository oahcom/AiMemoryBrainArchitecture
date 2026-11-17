# Official Reference Validation — Domain Modeling Research
# 官方参考资料核验 — 领域建模研究

- ID: B-EXT-REF-001
- Status: RESEARCH EVIDENCE — NOT A PROJECT CONTRACT
- Access date: 2026-11-17
- Purpose: verify the official concepts used by the mature-domain-model assessment; distinguish observed implementation patterns from recommendations for this project.

## 1. DDD and bounded contexts / DDD 与限界上下文

- Martin Fowler, **Bounded Context**: https://martinfowler.com/bliki/BoundedContext.html
- Martin Fowler, **DDD Aggregate**: https://martinfowler.com/bliki/DDD_Aggregate.html
- Microsoft Learn, **Design a microservice domain model**: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model

**Observed / 观察：** DDD strategic boundaries help keep a coherent model and language within a context. Aggregates are consistency boundaries, not a requirement to wrap every entity or create a service per context.

**中文观察：** DDD 战略边界帮助在单个 Context 内保持模型和语言一致。Aggregate 是一致性边界，并不要求将每个 Entity 都包装进聚合，也不要求每个 Context 都创建独立 Service。

**Project disposition / 本项目处理：** Adopt bounded contexts as semantic ownership boundaries. Aggregate boundaries remain with D/G/Storage and must be justified by actual invariants and transaction boundaries. Do not introduce generic AggregateRoot inheritance or mandatory microservices.

**中文处理：** 将 Bounded Context 作为语义所有权边界；Aggregate 的具体边界由 D/G/Storage 决定，必须由真实不变量和事务边界证明。不得引入通用 AggregateRoot 继承，也不得强制微服务化。

## 2. Zep / Graphiti / Zep 与 Graphiti

- Zep v4 official guide, **How Graph Creation Works**: https://help.getzep.com/how-graph-creation-works
- Zep v3 official guide, **Context Graph overview**: https://help.getzep.com/v3/graph-overview
- Graphiti official repository: https://github.com/getzep/graphiti

**Observed / 观察：** Zep documents source Episodes and LLM-derived entities, relationships and facts/edges tied back to Episodes. Its documentation explicitly distinguishes provenance (where derived material came from) from correctness of the source or derived fact. Episodes can be used to query at a point in time and trace mentions/lineage.

**中文观察：** Zep 文档描述 Source Episode，以及由 LLM 派生并回链到 Episode 的 Entity、Relation 和 Fact/Edge。文档明确区分 Provenance（派生材料来自哪里）与来源/派生 Fact 是否正确。Episode 可用于指定时间点查询，并追踪 Mention/Lineage。

**Borrow / 借鉴：** preserve source records and explicit links from derived graph artifacts back to source Episodes; maintain temporal history where supported by use cases.

**中文借鉴：** 保留来源记录，并为派生图产物建立回到 Source Episode 的显式链接；在真实用例需要时维护时间历史。

**Do not infer / 不可推断：** a temporal graph does not by itself prove epistemic truth, authorization, deletion completion or suitability as the canonical storage engine.

**中文不可推断：** 时间图本身不能证明认知真值、授权、删除完成，也不能证明其适合作为规范存储引擎。

## 3. Mem0 / Mem0

- Official repository: https://github.com/mem0ai/mem0
- Official guide, **How Mem0 Works**: https://github.com/mem0ai/mem0/blob/main/docs/core-concepts/how-it-works.mdx
- Official guide, **Graph Memory**: https://github.com/mem0ai/mem0/blob/main/docs/platform/features/graph-memory.mdx

**Observed / 观察：** Mem0 describes memory extraction and search scoped by user/agent/run dimensions. Its Graph Memory guide explicitly distinguishes graph entities extracted from memory content from user/agent/app/run IDs used to scope memories. The current documented graph links entity nodes to memory nodes; entity-to-entity relationships are based on co-occurrence rather than typed predicates such as “manages”.

**中文观察：** Mem0 描述按 User/Agent/Run 维度限定的 Memory 抽取和搜索。Graph Memory 指南明确区分从 Memory 内容抽取的 Graph Entity 与用于限定 Memory 的 User/Agent/App/Run ID。当前文档中的 Graph 将 Entity Node 链接到 Memory Node；Entity-to-Entity 关系基于共现，而不是“manages”等类型化谓词。

**Borrow / 借鉴：** separate identity/scope dimensions from extracted knowledge entities; graph-assisted retrieval may be a projection/ranking aid.

**中文借鉴：** 将身份/Scope 维度与抽取出的知识 Entity 分离；Graph-assisted Retrieval 可作为投影或 Ranking 辅助。

**Do not copy / 不照搬：** untyped co-occurrence links are not a replacement for this project's typed Relation with endpoint, time, scope and evidence semantics.

**中文不照搬：** 无类型共现链接不能替代本项目具有端点、时间、Scope 和 Evidence 语义的类型化 Relation。

## 4. Letta / Letta

- Official docs, **Stateful agents**: https://docs.letta.com/concepts/stateful-agents
- Official docs, **Memory & dreaming**: https://docs.letta.com/configuration/memory

**Observed / 观察：** Letta describes a persistent Agent identity with its own memory, model/tool configuration and one or more conversations; memory can be shared across conversations. Its documented MemFS is a git-backed memory filesystem that can be inspected and edited.

**中文观察：** Letta 描述具有自身 Memory、Model/Tool 配置和一个或多个 Conversation 的持久 Agent 身份；Memory 可跨 Conversation 共享。其文档中的 MemFS 是可检查和编辑的 Git-backed Memory 文件系统。

**Borrow / 借鉴：** explicitly distinguish persistent Agent identity from conversation/thread identity; inspectable revision history can aid auditability.

**中文借鉴：** 明确区分持久 Agent 身份与 Conversation/Thread 身份；可检查的 Revision History 有助于审计。

**Do not infer / 不可推断：** this is not a substitute for B's canonical Memory identity, I's authenticated Principal, or D's Forget lifecycle guarantees.

**中文不可推断：** 该模型不能替代 B 的规范 Memory 身份、I 的已认证 Principal 或 D 的 Forget 生命周期保证。

## 5. LangGraph / LangGraph

- Official docs, **Persistence**: https://docs.langchain.com/oss/python/langgraph/persistence

**Observed / 观察：** LangGraph documents two persistence concepts: checkpointers for thread-scoped graph state/checkpoints and stores for application-defined long-term data across threads.

**中文观察：** LangGraph 文档区分两类持久化概念：用于 Thread Scope Graph State/Checkpoint 的 Checkpointer，以及用于跨 Thread 应用长期数据的 Store。

**Borrow / 借鉴：** keep short-lived execution/thread state distinct from cross-thread durable memory assets. A Context or Working Set should not be collapsed into canonical Memory merely because it is persisted.

**中文借鉴：** 将短期执行/Thread State 与跨 Thread 的持久 Memory 资产分开。不能仅因为 Context 或 Working Set 被持久化，就把它们合并为规范 Memory。

## 6. Temporal / Temporal

- Official docs, **Workflows**: https://docs.temporal.io/workflows
- Official docs, **Event History**: https://docs.temporal.io/encyclopedia/event-history
- Official docs, **Understanding Temporal**: https://docs.temporal.io/evaluate/understanding-temporal

**Observed / 观察：** Temporal's Workflow Execution is an instance of a Workflow Definition; execution progress is represented by a durable ordered Event History. Replay rebuilds workflow state from history, while previously completed Activities are not re-executed as new side effects during deterministic replay.

**中文观察：** Temporal 的 Workflow Execution 是 Workflow Definition 的一个实例；执行进度由持久、有序的 Event History 表示。Replay 从 History 重建 Workflow State；确定性 Replay 不会把已完成 Activity 作为新副作用再次执行。

**Borrow / 借鉴：** operation/workflow history can support deterministic recovery for selected high-risk processes.

**中文借鉴：** 对选定的高风险流程，可借鉴 Operation/Workflow History 以支持确定性恢复。

**Do not infer / 不可推断：** a durable workflow engine does not imply the whole Memory domain should be Event Sourced. External side effects, version evolution, retention and Forget still need explicit design.

**中文不可推断：** 使用持久 Workflow Engine 不意味着整个 Memory 领域都应采用 Event Sourcing。外部副作用、版本演进、保留和 Forget 仍需要显式设计。

## 7. PostgreSQL / PostgreSQL

- PostgreSQL 18 official documentation, **Transaction Isolation**: https://www.postgresql.org/docs/current/transaction-iso.html

**Observed / 观察：** PostgreSQL documents Serializable isolation and serialization failures that applications must be prepared to retry. Repeatable Read is snapshot isolation and does not provide the same serial execution guarantee for all concurrent transactions.

**中文观察：** PostgreSQL 文档说明 Serializable 隔离可能发生 Serialization Failure，应用必须准备重试。Repeatable Read 属于 Snapshot Isolation，并不对所有并发事务提供相同的串行执行保证。

**Borrow / 借鉴：** if Storage uses a serializable transaction domain, retry semantics and idempotent whole-transaction retry must be specified and tested.

**中文借鉴：** 如果 Storage 使用 Serializable Transaction Domain，必须明确并测试 Retry 语义和整个事务的幂等重试。

**Limit / 限制：** this documentation is not evidence that the project's actual deployed database, adapter, D fence ledger and Storage visibility pointer share one transaction domain. Issue #10 and the Storage L4 gate remain authoritative blockers.

**中文限制：** 该文档不能证明本项目实际部署的数据库、Adapter、D Fence Ledger 和 Storage Visibility Pointer 共享同一个事务域。Issue #10 和 Storage L4 Gate 仍是权威阻塞项。

## 8. W3C PROV-O / W3C PROV-O

- W3C Recommendation, **PROV-O: The PROV Ontology**: https://www.w3.org/TR/prov-o/

**Observed / 观察：** PROV-O's starting-point model uses Entity, Activity and Agent, with relations describing use, generation, attribution, association and derivation.

**中文观察：** PROV-O 的起点模型使用 Entity、Activity 和 Agent，并通过关系描述使用、生成、归因、关联和派生。

**Borrow / 借鉴：** use the compact Entity/Activity/Agent provenance pattern to explain inputs, derivation activity and responsible actors.

**中文借鉴：** 使用精简 Entity/Activity/Agent Provenance 模式描述输入、派生活动和负责 Actor。

**Do not equate / 不可等同：** PROV-O's broad `prov:Entity` is not this project's domain `Entity`; PROV-O does not determine project-specific Claim truth, authorization, retention or Forget policy.

**中文不可等同：** PROV-O 的广义 `prov:Entity` 不等于本项目的领域 `Entity`；PROV-O 不决定本项目 Claim 真值、授权、保留或 Forget 策略。

## 9. RDF and OWL / RDF 与 OWL

- W3C Recommendation, **RDF 1.1 Concepts and Abstract Syntax**: https://www.w3.org/TR/rdf-concepts/
- W3C Recommendation, **OWL 2 Web Ontology Language Document Overview**: https://www.w3.org/TR/owl2-overview/

**Observed / 观察：** RDF represents graph statements as subject-predicate-object triples and supports datasets with named graphs. RDF's data model is atemporal by itself; temporal interpretation requires explicit vocabulary. OWL 2 adds formally defined ontology semantics for classes, properties and individuals and supports reasoning under defined semantics.

**中文观察：** RDF 使用 Subject-Predicate-Object 三元组表示图声明，并支持 Named Graph Dataset。RDF 数据模型本身没有时间语义；时间解释需要显式词汇。OWL 2 为 Class、Property 和 Individual 提供形式化本体语义，并在定义的语义下支持推理。

**Project disposition / 本项目处理：** typed Relation records plus explicit provenance edges are sufficient for the initial canonical model. Graph projection is a candidate for measured multi-hop retrieval. RDF/OWL are deferred until interoperability, formal ontology reasoning or externally governed shared vocabularies are demonstrated requirements.

**中文处理：** 初始规范模型使用类型化 Relation 记录和显式 Provenance Edge 已足够。Graph Projection 是经测量的多跳检索候选。只有证明存在互操作、正式本体推理或外部治理共享词汇需求后，才考虑 RDF/OWL。

## 10. JSON Schema / JSON Schema

- Official specification, **Draft 2020-12**: https://json-schema.org/draft/2020-12
- Official specification index: https://json-schema.org/specification

**Observed / 观察：** Draft 2020-12 separates Core and Validation specifications and includes updated array/tuple handling, dynamic references and vocabularies including format annotation/assertion.

**中文观察：** Draft 2020-12 将 Core 与 Validation 规范分离，并更新 Array/Tuple 处理、Dynamic Reference，以及 Format Annotation/Assertion 等 Vocabulary。

**Project disposition / 本项目处理：** JSON Schema is a candidate validation artifact only after domain semantics and ownership decisions stabilize. Schema validity cannot prove truth, authorization, currentness, lineage completeness or physical deletion.

**中文处理：** 只有领域语义和 Owner 决策稳定后，JSON Schema 才能作为候选验证工件。Schema 有效不能证明真值、授权、当前性、谱系完整性或物理删除。

## 11. Evidence ceiling / 证据上限

These references were searched/read as official documentation or standards on 2026-11-17. The summary records only claims supported by those sources. It is not a benchmark, production compatibility test, endorsement, or evidence that any product should be adopted. Product versions and mutable documentation pages must be re-pinned at any later decision date.

以上资料于 2026-11-17 从官方文档或标准页面检索/读取。本文件只记录来源能够支持的结论，不构成性能基准、生产兼容性测试、产品背书或采用建议。产品版本和可变文档页面必须在后续决策时重新 Pin。
