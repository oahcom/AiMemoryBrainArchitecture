# AI Memory Brain Architecture — Documentation Portal

> **Bilingual architecture documentation | 双语架构文档**

Chinese and English are maintained as equivalent reading versions. Normative architecture decisions remain governed by the source specifications and ADRs in this repository.

## Start here / 从这里开始

| Reader | Recommended path |
|---|---|
| New to the project / 初次了解 | [中文系统总览](zh-CN/01-system-architecture/system-overview.md) · [English System Overview](en/01-system-architecture/system-overview.md) |
| Understand architecture / 理解架构 | System overview → component map → responsibility matrix |
| Implement a subsystem / 开发模块 | Owner specification → domain/protocol contracts → acceptance criteria |
| Evaluate technology / 技术选型 | [中文技术架构总览](zh-CN/13-engineering-decisions/technology-architecture-overview.md) · [English Technology Overview](en/13-engineering-decisions/technology-architecture-overview.md) |
| Look up terms / 查术语 | [Bilingual Glossary / 中英术语表](glossary/architecture-glossary.md) |

**Coverage and migration plan / 覆盖与迁移计划：** [Bilingual Documentation Status](translation-status.md)

**Mandatory project rule / 项目强制规范：** Every architecture design and semantic change must be documented in Chinese and English in the same change set. See [GOV-DOC-001](../00-governance/bilingual-documentation-policy.md).

## Documentation layers / 文档层次

### L1 — Understand the system / 理解系统
Mission, scope, non-goals, Brain vs. Agent, system map, main data and control flows.

### L2 — Understand subsystem architecture / 理解子系统
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
6. A contract change requires both language versions to be updated in the same change set, or the untranslated counterpart must be marked STALE.

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
