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

## Bilingual architecture documentation policy / 架构双语文档规范

**Normative requirement:** Every architecture design or semantic architecture change MUST include Chinese and English documentation in the same change set. Both versions must preserve identical meaning, constraints, decision status, stable identifiers, failure cases, and acceptance criteria. A one-language-only architecture PR cannot pass documentation acceptance unless a time-bounded, tracked **STALE** exception is approved under the policy.

**面向所有 AI 开发者的规范性要求：** 每一位 AI 开发者/会话——无论负责架构、编码、测试、安全、协议、存储、性能、迁移、运维还是审查——都 MUST 阅读并遵守 GOV-DOC-001。任何新增或改变架构含义、面向实现的契约的变更，都 MUST 在同一个变更集中同步更新中文和英文文档。两种语言必须保持相同的含义、约束、决策状态、稳定标识、故障场景和验收条件。缺少或实质不一致的对应版本意味着 NOT DONE，不得通过验收；只有正式批准且有明确期限、责任人和跟踪记录的 **STALE** 例外才可临时豁免。

See [GOV-DOC-001 Bilingual Architecture Documentation Policy](00-governance/bilingual-documentation-policy.md) and the [bilingual documentation portal](docs/README.md).

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
| `14-ai-development/` | AI development governance, iteration lifecycle, versioned prompts and evidence records |

## AI development governance

This repository is developed through named AI Module Owners under a controlled, evidence-based workflow. Every substantive task must have a versioned prompt, an accountable Owner, an isolated change, reproducible verification and independent review.

All AI developers/sessions MUST use the [canonical Prompt Library](prompts/README.md): global prompts are stored directly under `prompts/`, while A–I Owner-specific prompts are stored in their respective `prompts/A/` through `prompts/I/` directories. The exact prompt version used must be preserved in the Work Item evidence bundle. See [AI Development Standard](14-ai-development/ai-development-standard.md), [Iteration Lifecycle](14-ai-development/iteration-lifecycle.md), and [Prompt & Evidence Template](14-ai-development/prompt-and-evidence-template.md).

本仓库通过明确的 AI 模块 Owner 和可追溯证据流程进行开发。每项实质性任务都必须具有版本化提示词、责任 Owner、隔离变更、可复现验证和独立审查。

所有 AI 开发者/会话 MUST 使用[规范提示词目录](prompts/README.md)：全局提示词直接存放在 `prompts/` 根目录，A–I Owner 专属提示词分别存放在 `prompts/A/` 至 `prompts/I/`。实际执行的准确提示词版本必须保存在 Work Item 证据包中。

## How decisions are documented

Every significant design statement must be classified as one of:

- **DECIDED** — normative architecture baseline.
- **CANDIDATE** — a proposed design awaiting comparison.
- **TO_VALIDATE** — a hypothesis requiring experiments or prototypes.
- **OPEN** — an unresolved question that blocks or influences later design.

Implementation must not begin merely because a component has a name. Its responsibilities, boundaries, inputs, outputs, state transitions, failure behavior, security constraints, and acceptance criteria must first be specified.

## Current starting point

See [Architecture Roadmap](ARCHITECTURE_ROADMAP.md), [System Overview](01-system-architecture/system-overview.md), [Component Map](01-system-architecture/component-map.md), and [Responsibility Matrix](01-system-architecture/responsibility-matrix.md).
