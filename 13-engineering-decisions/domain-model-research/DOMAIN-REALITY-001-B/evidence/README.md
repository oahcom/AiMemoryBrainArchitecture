# Evidence Index
# 证据索引

- Status: First-pass evidence index; access date 2026-11-17. / 状态：第一轮证据索引；访问日期：2026-11-17。
- Repository evidence is pinned in ../existing-domain-model-baseline.md and ../cross-owner-canonical-semantics-matrix.md. / 仓库证据 Pin 记录于 ../existing-domain-model-baseline.md 和 ../cross-owner-canonical-semantics-matrix.md。
- This index lists external official sources used for modeling research. Product documentation is evidence of documented product design, not independent correctness or performance proof. / 本索引列出领域建模研究使用的外部官方来源。产品文档只能证明产品公开描述的设计，不能独立证明其正确性或性能。

## DDD / Domain Model / DDD 与领域模型
- Microsoft Learn — Design a microservice domain model / 设计微服务领域模型: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model
- Microsoft Learn — Designing a DDD-oriented microservice / 设计面向 DDD 的微服务: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice
- Martin Fowler — Bounded Context (2014-01-15) / 有界上下文（2014-01-15）: https://martinfowler.com/bliki/BoundedContext.html
- Martin Fowler — DDD Aggregate (2013-04-23) / DDD 聚合（2013-04-23）: https://martinfowler.com/bliki/DDD_Aggregate.html

## Event Sourcing / Durable Workflows / 事件溯源与持久工作流
- Martin Fowler — Event Sourcing / 事件溯源: https://martinfowler.com/eaaDev/EventSourcing.html
- Temporal — Event History / 事件历史: https://docs.temporal.io/encyclopedia/event-history
- Temporal — Understanding Temporal / 理解 Temporal: https://docs.temporal.io/evaluate/understanding-temporal

## Memory and Agent References / Memory 与 Agent 参考
- Zep v4 — How Graph Creation Works / 图创建机制: https://help.getzep.com/how-graph-creation-works
- Zep v2 — Understanding the Graph / 理解图模型: https://help.getzep.com/v2/understanding-the-graph
- Graphiti official repository / Graphiti 官方仓库: https://github.com/getzep/graphiti
- Mem0 official repository / Mem0 官方仓库: https://github.com/mem0ai/mem0
- Mem0 official Graph Memory documentation source / Mem0 官方 Graph Memory 文档源文件: https://github.com/mem0ai/mem0/blob/main/docs/platform/features/graph-memory.mdx
- Mem0 official architecture reference / Mem0 官方架构参考: https://github.com/mem0ai/mem0/blob/main/skills/mem0/references/architecture.md
- Letta — Stateful agents / 有状态 Agent: https://docs.letta.com/concepts/stateful-agents
- Letta — Memory & dreaming / Memory 与 Dreaming: https://docs.letta.com/configuration/memory
- LangGraph — Persistence and checkpoints / 持久化与 Checkpoint: https://docs.langchain.com/oss/python/langgraph/persistence

## Provenance / Knowledge Representation / 溯源与知识表示
- W3C PROV-O Recommendation / W3C PROV-O 建议标准: https://www.w3.org/TR/prov-o/
- W3C RDF 1.1 Concepts and Abstract Syntax / RDF 1.1 概念与抽象语法: https://www.w3.org/TR/rdf-concepts/
- W3C OWL 2 Web Ontology Language Overview / OWL 2 Web 本体语言概览: https://www.w3.org/TR/owl2-overview/

## Storage / Validation / 存储与验证
- PostgreSQL 18 — Concurrency Control / 并发控制: https://www.postgresql.org/docs/current/mvcc.html
- PostgreSQL 18 — Transaction Isolation / 事务隔离: https://www.postgresql.org/docs/current/transaction-iso.html
- JSON Schema specification / JSON Schema 规范: https://json-schema.org/specification
- JSON Schema Draft 2020-12 / JSON Schema 2020-12 草案: https://json-schema.org/draft/2020-12

## Evidence limitations / 证据局限
- No independent benchmark, source-code comparative experiment, deployment test or conformance run was performed. / 未执行独立基准测试、源码对比实验、部署测试或一致性测试。
- Mem0 findings are based on official repository documentation and are version-sensitive; distinguish current platform Graph Memory from historical external graph-store integration. / Mem0 结论基于官方仓库文档，具有版本敏感性；必须区分当前 Platform Graph Memory 与历史外部图存储集成。
- Zep findings are explicitly version-scoped (v4 and v2 documentation). / Zep 结论明确限定于对应版本（v4 与 v2 文档）。
- Temporal and PostgreSQL docs describe those products' own mechanisms; they do not prove that AI Memory Brain's cross-authority protocol is correctly implemented. / Temporal 和 PostgreSQL 文档描述各自产品机制，并不能证明 AI Memory Brain 的跨权威协议已正确实现。
- All implementation and production claims remain NOT VERIFIED. / 所有实现和生产就绪声明仍为 NOT VERIFIED。
