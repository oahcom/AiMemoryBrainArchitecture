# AI Memory Brain Architecture

> Architecture specifications for an independent, model-agnostic memory infrastructure for AI agents.

**Repository status:** Architecture definition  
**Current phase:** System architecture baseline  
**Implementation status:** Not started by design

## Mission

Design a durable, reusable Memory Brain that owns the lifecycle and organization of memory assets and manages task-specific memory context across agents, models, sessions, and environments.

The Brain is not an Agent framework. It does not own planning, tool execution, or action policy. Agents remain responsible for reasoning and acting; the Brain owns memory assets, memory lifecycle, retrieval, activation, and the logical authority of its managed memory context.

## Architectural principles

1. The Brain defines its own memory model and policies; Agents adapt to the Brain's contracts.
2. The Brain is independent of any specific Agent framework, model vendor, or inference API.
3. Events, memories, facts, entities, relations, and evidence are distinct domain objects.
4. Derived memories retain provenance and links to supporting evidence.
5. Plans and intentions are not automatically treated as completed events or verified facts.
6. Canonical memory and task-specific memory context are separate.
7. Context removal is not memory deletion; forgetting is an explicit governance operation.
8. Context changes are versioned and applied at inference boundaries through an Adapter.
9. Memory content is data, never elevated to system/developer instruction authority.
10. Scope isolation, permission checks, auditability, and conflict preservation are foundational.

## Architecture at a glance

- **Memory Brain:** canonical memory assets, identity, relationships, lifecycle, provenance, governance.
- **Memory Compiler:** event ingestion, extraction, normalization, evidence linking, consolidation, conflict handling, indexing inputs.
- **Memory Runtime:** retrieval, activation, working sets, context planning, context synchronization.
- **Agent Integration:** a stable telemetry and context protocol plus adapters at inference boundaries.
- **Cross-cutting infrastructure:** storage, indexes, cache, consistency, recovery, security, observability.

## Bilingual documentation / 双语架构文档

The project maintains a reader-oriented Chinese/English documentation set. Start with the [Documentation Portal](docs/README.md), then read the paired [System Architecture Overview (中文)](docs/zh-CN/01-system-architecture/system-overview.md) / [System Architecture Overview (English)](docs/en/01-system-architecture/system-overview.md). The portal explains reading paths, terminology, decision-status labels, and bilingual parity rules.

项目提供中英双语、分层阅读的架构文档。建议从[双语文档入口](docs/README.md)开始，再阅读[中文系统架构总览](docs/zh-CN/01-system-architecture/system-overview.md)或[英文系统架构总览](docs/en/01-system-architecture/system-overview.md)。入口页说明阅读顺序、术语、决策状态和双语一致性规则。

## Documentation map

| Path | Purpose |
|---|---|
| `00-governance/` | Principles, invariants, terminology, architecture decisions |
| `01-system-architecture/` | System overview, component map, responsibilities, boundaries, data flows |
| `02-domain-model/` | Canonical domain objects and semantics |
| `03-memory-brain/` | Canonical memory authority and lifecycle |
| `04-memory-compiler/` | Event-to-memory compilation pipeline |
| `05-memory-runtime/` | Retrieval and runtime execution model |
| `06-memory-context/` | Context planning, editing, versioning, reconciliation |
| `07-agent-integration/` | Telemetry contracts and Adapter integration |
| `08-protocols/` | BMCP protocol specifications |
| `09-storage-and-index/` | Persistence, indexes, cache, data layout |
| `10-security-and-governance/` | Scope, permissions, retention, audit, forgetting |
| `11-consistency-and-recovery/` | Versioning, idempotency, replay, recovery |
| `12-testing-and-acceptance/` | System-level verification and acceptance criteria |
| `13-engineering-decisions/` | Technology evaluation and Rust engineering architecture |

## How decisions are documented

Every significant design statement must be classified as one of:

- **DECIDED** — normative architecture baseline.
- **CANDIDATE** — a proposed design awaiting comparison.
- **TO_VALIDATE** — a hypothesis requiring experiments or prototypes.
- **OPEN** — an unresolved question that blocks or influences later design.

Implementation must not begin merely because a component has a name. Its responsibilities, boundaries, inputs, outputs, state transitions, failure behavior, security constraints, and acceptance criteria must first be specified.

## Current starting point

See [Architecture Roadmap](ARCHITECTURE_ROADMAP.md), [System Overview](01-system-architecture/system-overview.md), [Component Map](01-system-architecture/component-map.md), and [Responsibility Matrix](01-system-architecture/responsibility-matrix.md).
