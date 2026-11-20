# AI Memory Brain Architecture — Documentation Portal

> **Bilingual architecture documentation | 双语架构文档**

Chinese and English are maintained as equivalent reading versions. Normative architecture decisions remain governed by the source specifications and ADRs in this repository.

## Start here / 从这里开始

| Reader | Recommended path |
|---|---|
| New to the project / 初次了解 | [中文系统总览](zh-CN/01-system-architecture/system-overview.md) · [English System Overview](en/01-system-architecture/system-overview.md) |
| Understand architecture / 理解架构 | System overview → [System Design Guide](zh-CN/01-system-architecture/system-design-guide.md) → [Integration Governance Guide](zh-CN/01-system-architecture/integration-governance-guide.md) → component map → responsibility matrix → [Domain Model Guide](zh-CN/02-domain-model/domain-model-guide.md) |
| Implement a subsystem / 开发模块 | Owner specification → domain/protocol contracts → acceptance criteria |
| MVP pilot implementation / MVP 试点实现 | [MVP Architecture Decisions (EN)](governance/MVP-ARCHITECTURE-DECISIONS.md) · [MVP 架构决策 (中文)](zh-CN/governance/MVP-ARCHITECTURE-DECISIONS.md) |
| Evaluate technology / 技术选型 | [中文技术架构总览](zh-CN/13-engineering-decisions/technology-architecture-overview.md) · [English Technology Overview](en/13-engineering-decisions/technology-architecture-overview.md) |
| Look up terms / 查术语 | [Bilingual Glossary / 中英术语表](glossary/architecture-glossary.md) |

**Coverage and migration plan / 覆盖与迁移计划：** [Bilingual Documentation Status](translation-status.md) · [Owner Branch Migration Inventory](owner-branch-translation-inventory.md)

**Mandatory rule for every AI developer / 所有 AI 开发者强制规则：** Every AI developer/session—whether doing architecture, implementation, tests, security, storage, protocols, performance, migrations, operations or reviews—MUST read and follow [GOV-DOC-001](../00-governance/bilingual-documentation-policy.md). Any change to architecture meaning or implementation-facing contracts requires synchronized Chinese and English updates in the same change set. Missing or materially divergent counterparts mean NOT DONE unless a formally approved, time-bounded STALE exception exists. See also [AI Development Standard](../14-ai-development/ai-development-standard.md) and the [Prompt & Evidence Template](../14-ai-development/prompt-and-evidence-template.md).



**Canonical AI prompt library / AI 提示词规范目录：** Every AI session MUST start from the repository [Prompt Library](../prompts/README.md): global prompts live directly under `prompts/`, and Owner-specific prompts live under `prompts/A/` through `prompts/I/`. Each task must preserve the exact executed prompt version in its Work Item evidence bundle.

**AI 提示词规范目录：** 每个 AI 会话 MUST 从仓库的[提示词目录](../prompts/README.md)开始：全局提示词直接放在 `prompts/` 根目录，Owner 专属提示词分别放在 `prompts/A/` 至 `prompts/I/`。每项任务必须将实际执行的准确提示词版本保存在 Work Item 证据包中。

## Documentation layers / 文档层次

The [Cross-Module Conformance Guide](zh-CN/12-testing-and-acceptance/cross-module-conformance-guide.md) explains how architecture contracts are verified and what evidence is required before a PASS can be claimed.

### L1 — Understand the system / 理解系统
Mission, scope, non-goals, Brain vs. Agent, system map, main data and control flows.

### L2 — Understand subsystem architecture / 理解子系统
Start with the [Domain Model](zh-CN/02-domain-model/domain-model-guide.md), [Canonical Brain](zh-CN/03-memory-brain/memory-brain-guide.md), [Compiler](zh-CN/04-memory-compiler/memory-compiler-guide.md), [Runtime](zh-CN/05-memory-runtime/memory-runtime-guide.md), [Context](zh-CN/06-memory-context/memory-context-guide.md), [Agent Integration](zh-CN/07-agent-integration/agent-integration-guide.md), [BMCP](zh-CN/08-bmcp-protocol/bmcp-guide.md), and [Security & Governance](zh-CN/09-security-governance/security-governance-guide.md) guides before reading detailed Owner contracts.
Domain Model, Canonical Memory Brain, Compiler, Runtime, Memory Context, BMCP, Agent Integration, Security, Storage, Consistency, and Recovery.

### L3 — Build and verify / 工程实现与验证
Exact schemas, protocol fields, state machines, transaction boundaries, failure recovery, ADRs, prototypes, benchmarks, conformance tests, and acceptance gates.


## Source specifications / 原始规范

The existing root-level directories remain the detailed specification source: 00-governance, 01-system-architecture, 02-domain-model, 03-memory-brain, 04-memory-compiler, 05-memory-runtime, 06-memory-context, 07-agent-integration, 08-protocols, 09-storage-and-index, 10-security-and-governance, 11-consistency-and-recovery, 12-testing-and-acceptance, and 13-engineering-decisions.

Bilingual guides explain and navigate these specifications; they do not silently override them. If a guide conflicts with a normative specification, follow the current approved decision record and raise a documentation issue.

## Language and authority policy / 语言与权威规则

1. Chinese and English must express the same architecture meaning, constraints, status, and examples.
2. Stable identifiers, protocol fields, enum values, type names, crate names, and ADR IDs remain unchanged in both languages.
3. Translation must never turn CANDIDATE, OPEN, or TO_VALIDATE into DECIDED or APPROVED.
4. Normative decisions are governed by source specifications and the owner/ADR process—not by whichever language page was edited last.
5. Each paired document records its ID, version, source revision, status, and counterpart path.
6. Every AI developer/session must check both language counterparts before work and include bilingual parity in its task plan, prompt, review and completion evidence.
7. A contract change requires both language versions to be updated in the same change set, or the untranslated counterpart must be marked STALE under a formally approved, time-bounded exception.

## Status vocabulary / 状态词汇

| Status | 中文解释 | Meaning |
|---|---|---|
| DECIDED | 已决议 | Normative baseline; changes require an explicit decision record. |
| RECOMMENDED | 推荐方案 | Preferred direction, pending required owner review or ADR. |
| CANDIDATE | 候选方案 | Plausible option; not binding or frozen. |
| TO_VALIDATE | 待验证 | Requires prototype, benchmark, fault injection, or security evidence. |
| OPEN | 未决 | Unresolved question or dependency. |
| BLOCKED | 阻塞 | Progress or acceptance is prevented by an unresolved condition. |
| NOT REVIEWED | 尚未审查 | No review evidence is available. |

## Current documentation status / 当前文档状态

This is the initial bilingual foundation: paired system and technology overviews, a shared glossary, and authoring rules. Detailed subsystem specifications will be translated and readability-reviewed in controlled batches. This portal does not claim every source document is already bilingual.
