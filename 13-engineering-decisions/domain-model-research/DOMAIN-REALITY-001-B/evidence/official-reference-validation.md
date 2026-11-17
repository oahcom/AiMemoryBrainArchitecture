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

**Project disposition / 本项目处理：** Adopt bounded contexts as semantic ownership boundaries. Aggregate boundaries remain with D/G/Storage and must be justified by actual invariants and transaction boundaries. Do not introduce generic AggregateRoot inheritance or mandatory microservices.

## 2. Zep / Graphiti / Zep 与 Graphiti

- Zep v4 official guide, **How Graph Creation Works**: https://help.getzep.com/how-graph-creation-works
- Zep v3 official guide, **Context Graph overview**: https://help.getzep.com/v3/graph-overview
- Graphiti official repository: https://github.com/getzep/graphiti

**Observed / 观察：** Zep documents source Episodes and LLM-derived entities, relationships and facts/edges tied back to Episodes. Its documentation explicitly distinguishes provenance (where derived material came from) from correctness of the source or derived fact. Episodes can be used to query at a point in time and trace mentions/lineage.

**Borrow / 借鉴：** preserve source records and explicit links from derived graph artifacts back to source Episodes; maintain temporal history where supported by use cases.

**Do not infer / 不可推断：** a temporal graph does not by itself prove epistemic truth, authorization, deletion completion or suitability as the canonical storage engine.

## 3. Mem0 / Mem0

- Official repository: https://github.com/mem0ai/mem0
- Official guide, **How Mem0 Works**: https://github.com/mem0ai/mem0/blob/main/docs/core-concepts/how-it-works.mdx
- Official guide, **Graph Memory**: https://github.com/mem0ai/mem0/blob/main/docs/platform/features/graph-memory.mdx

**Observed / 观察：** Mem0 describes memory extraction and search scoped by user/agent/run dimensions. Its Graph Memory guide explicitly distinguishes graph entities extracted from memory content from user/agent/app/run IDs used to scope memories. The current documented graph links entity nodes to memory nodes; entity-to-entity relationships are based on co-occurrence rather than typed predicates such as “manages”.

**Borrow / 借鉴：** separate identity/scope dimensions from extracted knowledge entities; graph-assisted retrieval may be a projection/ranking aid.

**Do not copy / 不照搬：** untyped co-occurrence links are not a replacement for this project's typed Relation with endpoint, time, scope and evidence semantics.

## 4. Letta / Letta

- Official docs, **Stateful agents**: https://docs.letta.com/concepts/stateful-agents
- Official docs, **Memory & dreaming**: https://docs.letta.com/configuration/memory

**Observed / 观察：** Letta describes a persistent Agent identity with its own memory, model/tool configuration and one or more conversations; memory can be shared across conversations. Its documented MemFS is a git-backed memory filesystem that can be inspected and edited.

**Borrow / 借鉴：** explicitly distinguish persistent Agent identity from conversation/thread identity; inspectable revision history can aid auditability.

**Do not infer / 不可推断：** this is not a substitute for B's canonical Memory identity, I's authenticated Principal, or D's Forget lifecycle guarantees.

## 5. LangGraph / LangGraph

- Official docs, **Persistence**: https://docs.langchain.com/oss/python/langgraph/persistence

**Observed / 观察：** LangGraph documents two persistence concepts: checkpointers for thread-scoped graph state/checkpoints and stores for application-defined long-term data across threads.

**Borrow / 借鉴：** keep short-lived execution/thread state distinct from cross-thread durable memory assets. A Context or Working Set should not be collapsed into canonical Memory merely because it is persisted.

## 6. Temporal / Temporal

- Official docs, **Workflows**: https://docs.temporal.io/workflows
- Official docs, **Event History**: https://docs.temporal.io/encyclopedia/event-history
- Official docs, **Understanding Temporal**: https://docs.temporal.io/evaluate/understanding-temporal

**Observed / 观察：** Temporal's Workflow Execution is an instance of a Workflow Definition; execution progress is represented by a durable ordered Event History. Replay rebuilds workflow state from history, while previously completed Activities are not re-executed as new side effects during deterministic replay.

**Borrow / 借鉴：** operation/workflow history can support deterministic recovery for selected high-risk processes.

**Do not infer / 不可推断：** a durable workflow engine does not imply the whole Memory domain should be Event Sourced. External side effects, version evolution, retention and Forget still need explicit design.

## 7. PostgreSQL / PostgreSQL

- PostgreSQL 18 official documentation, **Transaction Isolation**: https://www.postgresql.org/docs/current/transaction-iso.html

**Observed / 观察：** PostgreSQL documents Serializable isolation and serialization failures that applications must be prepared to retry. Repeatable Read is snapshot isolation and does not provide the same serial execution guarantee for all concurrent transactions.

**Borrow / 借鉴：** if Storage uses a serializable transaction domain, retry semantics and idempotent whole-transaction retry must be specified and tested.

**Limit / 限制：** this documentation is not evidence that the project's actual deployed database, adapter, D fence ledger and Storage visibility pointer share one transaction domain. Issue #10 and the Storage L4 gate remain authoritative blockers.

## 8. W3C PROV-O / W3C PROV-O

- W3C Recommendation, **PROV-O: The PROV Ontology**: https://www.w3.org/TR/prov-o/

**Observed / 观察：** PROV-O's starting-point model uses Entity, Activity and Agent, with relations describing use, generation, attribution, association and derivation.

**Borrow / 借鉴：** use the compact Entity/Activity/Agent provenance pattern to explain inputs, derivation activity and responsible actors.

**Do not equate / 不可等同：** PROV-O's broad `prov:Entity` is not this project's domain `Entity`; PROV-O does not determine project-specific Claim truth, authorization, retention or Forget policy.

## 9. RDF and OWL / RDF 与 OWL

- W3C Recommendation, **RDF 1.1 Concepts and Abstract Syntax**: https://www.w3.org/TR/rdf-concepts/
- W3C Recommendation, **OWL 2 Web Ontology Language Document Overview**: https://www.w3.org/TR/owl2-overview/

**Observed / 观察：** RDF represents graph statements as subject-predicate-object triples and supports datasets with named graphs. RDF's data model is atemporal by itself; temporal interpretation requires explicit vocabulary. OWL 2 adds formally defined ontology semantics for classes, properties and individuals and supports reasoning under defined semantics.

**Project disposition / 本项目处理：** typed Relation records plus explicit provenance edges are sufficient for the initial canonical model. Graph projection is a candidate for measured multi-hop retrieval. RDF/OWL are deferred until interoperability, formal ontology reasoning or externally governed shared vocabularies are demonstrated requirements.

## 10. JSON Schema / JSON Schema

- Official specification, **Draft 2020-12**: https://json-schema.org/draft/2020-12
- Official specification index: https://json-schema.org/specification

**Observed / 观察：** Draft 2020-12 separates Core and Validation specifications and includes updated array/tuple handling, dynamic references and vocabularies including format annotation/assertion.

**Project disposition / 本项目处理：** JSON Schema is a candidate validation artifact only after domain semantics and ownership decisions stabilize. Schema validity cannot prove truth, authorization, currentness, lineage completeness or physical deletion.

## 11. Evidence ceiling / 证据上限

These references were searched/read as official documentation or standards on 2026-11-17. The summary records only claims supported by those sources. It is not a benchmark, production compatibility test, endorsement, or evidence that any product should be adopted. Product versions and mutable documentation pages must be re-pinned at any later decision date.

以上资料于 2026-11-17 从官方文档或标准页面检索/读取。本文件只记录来源能够支持的结论，不构成性能基准、生产兼容性测试、产品背书或采用建议。产品版本和可变文档页面必须在后续决策时重新 Pin。
