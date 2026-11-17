# Evidence Index
# 证据索引

- Status: First-pass evidence index; access date 2026-11-17.
- Repository evidence is pinned in ../existing-domain-model-baseline.md and ../cross-owner-canonical-semantics-matrix.md.
- This index lists external official sources used for modeling research. Product documentation is evidence of documented product design, not independent correctness or performance proof.

## DDD / Domain Model
- Microsoft Learn — Design a microservice domain model: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model
- Microsoft Learn — Designing a DDD-oriented microservice: https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/ddd-oriented-microservice
- Martin Fowler — Bounded Context (2014-01-15): https://martinfowler.com/bliki/BoundedContext.html
- Martin Fowler — DDD Aggregate (2013-04-23): https://martinfowler.com/bliki/DDD_Aggregate.html

## Event Sourcing / Durable Workflows
- Martin Fowler — Event Sourcing: https://martinfowler.com/eaaDev/EventSourcing.html
- Temporal — Event History: https://docs.temporal.io/encyclopedia/event-history
- Temporal — Understanding Temporal: https://docs.temporal.io/evaluate/understanding-temporal

## Memory and Agent References
- Zep v4 — How Graph Creation Works: https://help.getzep.com/how-graph-creation-works
- Zep v2 — Understanding the Graph: https://help.getzep.com/v2/understanding-the-graph
- Graphiti official repository: https://github.com/getzep/graphiti
- Mem0 official repository: https://github.com/mem0ai/mem0
- Mem0 official Graph Memory documentation source: https://github.com/mem0ai/mem0/blob/main/docs/platform/features/graph-memory.mdx
- Mem0 official architecture reference: https://github.com/mem0ai/mem0/blob/main/skills/mem0/references/architecture.md
- Letta — Stateful agents: https://docs.letta.com/concepts/stateful-agents
- Letta — Memory & dreaming: https://docs.letta.com/configuration/memory
- LangGraph — Checkpointing: https://langchain-ai.github.io/langgraph/reference/checkpoints/
- LangGraph — Persistence: https://langchain-ai.github.io/langgraph/cloud/concepts/threads/

## Provenance / Knowledge Representation
- W3C PROV-O Recommendation: https://www.w3.org/TR/prov-o/
- W3C RDF 1.1 Concepts and Abstract Syntax: https://www.w3.org/TR/rdf-concepts/
- W3C OWL 2 Web Ontology Language Overview: https://www.w3.org/TR/owl2-overview/

## Storage / Validation
- PostgreSQL 18 — Concurrency Control: https://www.postgresql.org/docs/current/mvcc.html
- PostgreSQL 18 — Transaction Isolation: https://www.postgresql.org/docs/current/transaction-iso.html
- JSON Schema specification: https://json-schema.org/specification
- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12

## Evidence limitations
- No independent benchmark, source-code comparative experiment, deployment test or conformance run was performed.
- Mem0 findings are based on official repository documentation and are version-sensitive; distinguish current platform Graph Memory from historical external graph-store integration.
- Zep findings are explicitly version-scoped (v4 and v2 documentation).
- Temporal and PostgreSQL docs describe those products' own mechanisms; they do not prove that AI Memory Brain's cross-authority protocol is correctly implemented.
- All implementation and production claims remain NOT VERIFIED.
