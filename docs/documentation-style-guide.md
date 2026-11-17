# Architecture Documentation Style Guide / 架构文档编写规范

- Document ID: DOC-STYLE-001
- Version: 1.0
- Status: Documentation governance baseline

## 1. Purpose / 目的

Architecture documents must be technically precise and understandable to readers who did not participate in design sessions. Readability is an engineering quality attribute, not decoration.

架构文档必须既技术准确，也能让没有参加设计讨论的人读懂。易读性是工程质量，不是装饰。

## 2. Audience layers / 读者层次

Write for three audiences:
1. **Orientation reader / 入门读者:** needs the mission, boundaries, concepts, and one coherent system picture.
2. **Subsystem engineer / 模块工程师:** needs ownership, contracts, dependencies, workflows, states, and failure behavior.
3. **Implementer / 实现与验证人员:** needs exact schemas, transaction semantics, protocol fields, test vectors, and acceptance evidence.

Start with the simplest correct explanation, then progressively disclose detail. Do not require a newcomer to understand a storage protocol before explaining why the subsystem exists.

先给出最简单但正确的解释，再逐层展开。不要在解释模块存在的目的之前，就要求读者理解底层存储协议。

## 3. Recommended structure / 推荐结构

For major architecture documents, use this order where applicable:
1. Purpose / 目的
2. One-sentence summary / 一句话概括
3. Scope and non-goals / 范围与非目标
4. Responsibilities and non-responsibilities / 负责与不负责
5. Context diagram / 上下文图
6. Concepts and data model / 概念与数据模型
7. Main workflows / 主要流程
8. State machines and invariants / 状态机与不变量
9. Interfaces and dependencies / 接口与依赖
10. Security and trust boundaries / 安全与信任边界
11. Failure and recovery / 故障与恢复
12. Performance and resource budget / 性能与资源预算
13. Acceptance criteria / 验收标准
14. Decisions, open questions, and references / 决策、未决事项与引用

Not every document needs every section. Do not add empty headings merely to satisfy a template.

## 4. Readability rules / 易读性规则

- Put the conclusion before its justification.
- Keep one main idea per paragraph.
- Explain an acronym at first use.
- Prefer concrete verbs over abstract noun chains.
- Name the owner of each action; avoid vague phrases such as “the system handles it”.
- Distinguish input, output, state change, side effect, and acknowledgement.
- Explain why a constraint exists, not only what it says.
- Use diagrams for relationships or sequences, not as a substitute for prose.
- Keep diagrams small; split large diagrams by concern.
- Use tables for comparisons and responsibilities, not long narrative.
- Give a concrete example for subtle distinctions such as Accepted vs. Applied or Context Remove vs. Forget.
- State what a mechanism does not guarantee.
- Link to detailed contracts instead of duplicating long specifications.

## 5. Normative language / 规范性措辞

Use consistently:
- **MUST / 必须:** mandatory requirement.
- **MUST NOT / 禁止:** prohibited behavior.
- **SHOULD / 应当:** strong recommendation; deviations require rationale.
- **MAY / 可以:** permitted option.
- **DECIDED / 已决议:** approved architecture baseline.
- **CANDIDATE / 候选:** not binding.
- **OPEN / 未决:** unresolved.
- **TO_VALIDATE / 待验证:** evidence required.

Never use “supports”, “secure”, “atomic”, “durable”, “real-time”, or “complete” without defining scope and evidence.

## 6. Bilingual parity / 双语一致性

- **MUST:** Maintain Chinese and English counterparts for every architecture design, specification, review finding, ADR, and semantic architecture change—not only major guides.
- **MUST:** Add and update both counterparts in the same change set. A one-language-only architecture change cannot pass documentation acceptance except under GOV-DOC-001.
- Keep the same document ID, semantic version, decision status, section numbering, diagrams, tables, examples, and normative force.
- Translate explanations, not stable identifiers: API fields, enum values, type names, crate names, paths, and ADR IDs remain unchanged.
- Any change to either language triggers a semantic parity check of the other language in the same change set.
- Record source revision, document ID/version, accountable Owner, and parity evidence.
- Do not omit caveats, failure cases, or open issues in either language.
- If a translation is not updated, mark it **STALE / 翻译待同步** and link the authoritative revision; GOV-DOC-001 requires an approved, time-bounded exception with an Owner and due date.

## 7. Diagram and table rules / 图表规范

- Every diagram needs a title or a sentence explaining what it shows.
- Label authority and direction where ambiguity is possible.
- Do not imply a process boundary from a logical component box.
- Use consistent names in diagrams and prose.
- Tables need meaningful headings and concise cells.
- If a table is too wide, split it by concern rather than shrinking its meaning.

## 8. Change control / 变更管理

For each paired-document change:
1. Identify the source specification and exact revision.
2. Update Chinese and English counterparts together.
3. Check terminology against the shared glossary.
4. Check decision status against the latest ADR/owner decision.
5. Validate links and Mermaid syntax.
6. Review whether the text introduces a new requirement or changes normative meaning.
7. Record changed document IDs and versions in the change summary.

Translations must not create architecture decisions. Semantic changes must follow the appropriate Owner/ADR process.

## 9. Review checklist / 文档审查清单

- Can a new reader explain the purpose after the first section?
- Are Brain, Agent, Adapter, and Environment responsibilities unambiguous?
- Are responsibilities and non-responsibilities explicit?
- Are the main flows understandable without reading another document?
- Are authority, state, and acknowledgement boundaries clear?
- Are terms consistent with the shared glossary?
- Are DECIDED, CANDIDATE, OPEN, and TO_VALIDATE distinguished?
- Are failure cases and non-guarantees visible?
- Do Chinese and English say the same thing?
- Are links and diagrams valid?

## 10. Mandatory project rule / 项目强制规范

Every A–I Owner MUST deliver architecture work in Chinese and English. This includes proposals, review reports, module specifications, interfaces, schemas, state machines, ADRs, technology decisions, tests/acceptance requirements, and material revisions. Bilingual parity is an acceptance gate, not optional polish. See [GOV-DOC-001](../00-governance/bilingual-documentation-policy.md).

A–I 所有 Owner 必须以中英文双语交付架构工作，包括设计提案、审查报告、模块规范、接口、Schema、状态机、ADR、技术决策、测试/验收要求和重要修订。双语一致性是验收门禁，不是可选的文字润色。详见 [GOV-DOC-001](../00-governance/bilingual-documentation-policy.md)。


## Mandatory bilingual architecture delivery / 强制双语架构交付

All new architecture designs and architecture changes MUST include Chinese and English counterparts in the same change set. This applies to Owner proposals, ADRs, protocols, schemas, reviews, integration decisions, tests, and acceptance reports—not only overview documents.

每次新架构设计和架构变更，都必须在同一变更集中提交中英文对应文档。此要求适用于 Owner 提案、ADR、协议、Schema、审查报告、集成决议、测试和验收报告，不仅限于总览文档。

The normative policy is [GOV-DOC-BILINGUAL-001](../../00-governance/bilingual-architecture-documentation-policy.md). A missing or stale counterpart blocks documentation acceptance unless an explicitly approved, time-bounded exception exists. Update docs/translation-status.md in the same change set.
