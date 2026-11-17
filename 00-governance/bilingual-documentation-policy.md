# Bilingual Architecture Documentation Policy / 架构双语文档规范

- Policy ID: GOV-DOC-001
- Version: 1.1
- Status: **NORMATIVE — REQUIRED FOR ALL ARCHITECTURE WORK**
- Owner: A — Principal Integration / Architecture Governance
- Applies to: All Owners (A–I), contributors, architecture reviews, ADRs, specifications, and implementation-facing contract changes

## 1. Policy statement / 规范声明

**Every architecture design or architecture change MUST be documented in both Chinese and English.** The two language versions are a single deliverable and MUST be updated in the same change set.

**每一项架构设计或架构变更都必须同时形成中文和英文文档。** 两种语言版本属于同一项交付物，必须在同一个变更集中同步更新。

This policy is a repository-wide governance requirement. It is not an optional translation guideline and is not limited to documents labelled as major specifications.

本规范是全仓库治理要求，不是可选的翻译建议，也不只适用于标记为“主要规范”的文档。

## 2. Scope / 适用范围

The requirement applies to, at minimum:
- System and subsystem architecture, component boundaries, responsibility assignments, and dependency maps.
- Domain models, schemas, data contracts, lifecycle/state machines, invariants, and transaction semantics.
- APIs, protocols, message envelopes, field definitions, compatibility rules, and error semantics.
- Security, identity, Scope, Permission, retention, Forget, audit, and threat models.
- Storage, indexes, cache, consistency, recovery, deployment, and operational design.
- Technology evaluations, ADRs, engineering decisions, resource budgets, and benchmark plans/results.
- Test strategies, conformance requirements, acceptance criteria, and architecture review findings.
- Any change that alters the meaning, constraints, status, examples, or implementation guidance of the above.

适用范围至少包括：系统和子系统架构、组件边界、职责与依赖；领域模型、Schema、数据契约、生命周期和状态机；API、协议、字段与兼容性；安全、身份、权限、遗忘与审计；存储、索引、缓存、一致性、恢复和部署；技术评估、ADR、资源预算与基准测试；测试策略、验收条件和架构审查结论，以及对上述内容产生语义影响的任何修改。

Code comments, generated API references, machine-generated schema dumps, and raw test logs may remain in their natural technical language when duplicating them would be harmful or mechanically misleading. However, their architecture meaning, usage constraints, and interpretation MUST be explained in both language versions of the owning specification.

代码注释、自动生成的 API 参考、机器生成的 Schema 转储和原始测试日志，在重复翻译会造成误导或破坏机器可读性的情况下，可以保留其技术原文；但所属规范必须用中英文解释其架构含义、使用约束和解读方式。

## 2.1 Mandatory duties for every AI developer / 所有 AI 开发者的强制职责

This policy applies to **every AI developer, AI coding agent, AI reviewer, AI architecture agent, and AI session** working in this repository—not only the A–I Owners and not only the documentation role. The accountable Owner remains responsible for ensuring that every delegated AI session receives and follows this requirement.

Every AI developer MUST, before starting a task:

1. Read this policy and the relevant bilingual portal/style/glossary guidance.
2. Locate the current Chinese and English counterparts of every architecture contract affected by the task.
3. Identify which language files are authoritative source specifications and which are reader guides or translations; never assume a translated guide overrides an approved source contract.
4. Include bilingual-documentation work explicitly in its task plan, prompt, scope and acceptance criteria.

During the task, every AI developer MUST:

1. Create or update both language versions in the same change set whenever it creates or changes architecture meaning, constraints, interfaces, state, security, failure behavior, compatibility, technology decisions, resource assumptions, tests or acceptance criteria.
2. Keep both versions aligned as the design evolves; do not defer translation until an informal later cleanup.
3. Preserve stable identifiers, decision status, open issues, evidence references and exact source revision.
4. Update reciprocal links and the documentation coverage/status register.
5. If source material is incomplete, conflicting or not approved, preserve that uncertainty in both languages and escalate to the accountable Owner. Translation is not authority to decide.

Before reporting a task complete, every AI developer MUST provide a bilingual change manifest and verify counterpart existence, semantic parity, identifier parity, status parity and links. A task that changes architecture semantics is **NOT DONE** while its counterpart is missing, stale without an approved exception, or materially inconsistent.

AI reviewers and integration agents MUST check this requirement as an explicit review dimension. They MUST raise a finding and block documentation acceptance when the requirement is not met. A task prompt that omits this requirement is incomplete and MUST be corrected before execution or acceptance.

本规范适用于在本仓库工作的**每一位 AI 开发者、AI 编码 Agent、AI 审查者、AI 架构 Agent 和每一个 AI 会话**，而不只是 A–I Owner 或文档岗位。委派任务的责任 Owner 必须确保每个 AI 会话收到并遵守本要求。

每位 AI 开发者在开始任务前 MUST：

1. 阅读本规范以及相关双语入口、写作规范和术语表。
2. 找到任务涉及的每份架构契约当前的中文和英文对应版本。
3. 确认哪些文件是权威源规范，哪些是阅读指南或翻译；不得假设翻译版指南可以覆盖已批准的源契约。
4. 在任务计划、提示词、工作范围和验收标准中明确列入双语文档工作。

执行任务期间，每位 AI 开发者 MUST：

1. 只要新增或改变架构含义、约束、接口、状态、安全、故障行为、兼容性、技术决策、资源假设、测试或验收条件，就必须在同一个变更集中创建或更新中英文两个版本。
2. 随设计演进同步维护两种语言，不得把翻译推迟到某个非正式的后续清理阶段。
3. 保留稳定标识、决策状态、未决事项、证据引用和准确源版本。
4. 更新双向链接和文档覆盖/状态登记表。
5. 如果源材料不完整、存在冲突或尚未批准，必须在两种语言中保留其不确定性并升级给责任 Owner。翻译不构成决策授权。

在报告任务完成前，每位 AI 开发者 MUST 提供双语变更清单，并验证对应文件存在、语义一致、标识一致、状态一致且链接有效。凡改变架构语义的任务，只要另一语言版本缺失、未经批准的例外而过期，或存在实质不一致，就属于 **NOT DONE**。

AI 审查者和集成 Agent MUST 将本要求作为明确的审查维度。未满足时 MUST 提出 Finding 并阻止文档验收。遗漏本要求的任务提示词属于不完整提示词，必须在执行或验收前修正。

## 3. Required parity / 双语一致性要求

Chinese and English counterparts MUST preserve:
1. The same document/policy ID and compatible version.
2. The same scope, authority, ownership, and normative force.
3. The same requirements, constraints, caveats, failure modes, security boundaries, and non-guarantees.
4. The same state machines, examples, diagrams, tables, and acceptance criteria where applicable.
5. The same decision status: DECIDED, RECOMMENDED, CANDIDATE, OPEN, BLOCKED, or TO_VALIDATE.
6. Reciprocal links and traceability to the exact source revision.

中英文版本必须保持相同的文档 ID 和兼容版本，并具有相同的适用范围、权威性、职责归属、规范效力、约束、失败场景、安全边界、状态机、示例和验收标准；决策状态必须一致，并且必须互相链接、能够追溯到准确的源版本。

Stable technical identifiers MUST NOT be translated or renamed, including API fields, JSON keys, enum values, type names, Rust crate names, protocol constants, cursor namespaces, state tokens, file paths, and ADR IDs. Explanatory prose should translate the meaning while retaining canonical identifiers.

API 字段、JSON Key、枚举值、类型名、Rust Crate 名、协议常量、游标命名空间、状态 Token、文件路径和 ADR ID 等稳定技术标识禁止翻译或改名。说明文字应翻译其含义，同时保留规范标识。

## 4. Change and review gates / 变更与审查门禁

An architecture PR MUST include:
- Both Chinese and English files for every new or changed architecture document.
- A paired-document change list, source revision, and version information.
- A terminology and decision-status parity check.
- Link and diagram validation.
- An explicit statement when a change is explanatory only and does not alter normative semantics.

架构 PR 必须包含每份新增或修改文档的中英文版本、双语文件清单、源版本与文档版本、术语和决策状态一致性检查，以及链接和图表验证；如果变更仅为解释性改写、不改变规范语义，也必须明确说明。

**A PR that changes architecture semantics in only one language MUST NOT pass architecture documentation acceptance.** Reviewers MUST request the missing counterpart or a documented exception.

**只修改一种语言且改变架构语义的 PR，不得通过架构文档验收。** 审查者必须要求补齐另一语言版本，或要求提交正式例外记录。

## 5. Temporary exception / 临时例外

An emergency or time-critical change MAY temporarily land with one counterpart marked **STALE / 翻译待同步**, but only if the same PR records:
- Why simultaneous bilingual completion is not practical.
- Which language/version is currently authoritative for the immediate change.
- The missing counterpart path and exact source revision.
- A named accountable Owner.
- A due date and tracking issue/PR.

The exception MUST NOT be used to hide unresolved design semantics or to bypass Owner/ADR approval. The stale counterpart MUST be updated before the next dependent architecture baseline is accepted and no later than the recorded due date. The exception is visible technical debt, not completion.

紧急或有时限要求的变更可以临时只提交一种语言，但同一 PR 必须将另一版本标记为 **STALE / 翻译待同步**，并记录原因、当前临时权威版本、待补文件路径和源版本、明确责任 Owner、截止日期及跟踪 Issue/PR。该例外不得用于掩盖未决设计语义或绕过 Owner/ADR 审批。另一语言版本必须在下一个依赖该设计的架构基线验收前补齐，且不得晚于登记期限。例外属于可见技术债，不代表交付完成。

## 6. Authority and decision control / 权威与决策控制

This policy governs documentation completeness and parity; it does not transfer architecture decision authority. The relevant Owner remains responsible for its domain contract. Cross-owner decisions follow the established integration governance and ADR process.

本规范只管理文档完整性和双语一致性，不转移架构决策权。各领域契约仍由相应 Owner 负责；跨 Owner 决策仍遵循既有集成治理和 ADR 流程。

Translation MUST NOT:
- Turn CANDIDATE, OPEN, BLOCKED, or TO_VALIDATE into DECIDED.
- Resolve a disagreement between Owner specifications by choosing one language's wording.
- Invent missing fields, behavior, guarantees, or implementation evidence.
- Describe a design as implemented, tested, atomic, secure, or production-ready without evidence.

翻译禁止将候选、未决、阻塞或待验证状态改写为已决议；禁止通过选择某种语言的措辞来裁决 Owner 冲突；禁止补造字段、行为、保证或实现证据；没有证据时禁止声称设计已经实现、测试、具备原子性、安全性或生产就绪。

## 7. Definition of done / 完成定义

A bilingual architecture deliverable is complete only when:
1. Both language versions exist and are linked.
2. A bilingual reviewer confirms semantic and normative parity.
3. Stable identifiers match exactly.
4. All open items and status labels match.
5. Links, tables, diagrams, and examples have been checked.
6. The source revision and review evidence are recorded.

只有在两种语言版本均存在并互相链接、语义和规范效力通过双语审查、稳定标识完全一致、未决事项和状态标签一致、链接表格图表及示例完成检查、源版本和审查证据均已记录后，双语架构交付才算完成。

## 8. Enforcement / 执行

This policy is effective for new architecture work from its adoption into the repository's approved governance baseline. All A–I Owners and **all AI developers/sessions** MUST apply it to future design proposals, review reports, specifications, ADRs, implementation-facing contract changes, technology decisions, test/acceptance changes, and material revisions. The task Owner MUST put this requirement into every delegated prompt and verify the returned bilingual manifest. Reviewers MUST treat missing or materially divergent counterparts as a blocking documentation finding. No AI developer may waive this policy on its own; only the authorized project governance authority may approve a time-bounded exception under Section 5. Existing documents will be migrated in tracked batches; unmigrated items MUST be listed as NOT STARTED or STALE rather than represented as bilingual-complete.

本规范自正式纳入仓库已批准治理基线后，对新的架构工作生效。A–I 所有 Owner 以及**所有 AI 开发者/会话**必须在后续设计提案、审查报告、规范、ADR、面向实现的契约变更、技术决策、测试/验收变更和重要修订中执行。任务 Owner 必须把本要求写入每一份委派提示词，并核验 AI 返回的双语变更清单。审查者必须把缺失或实质不一致的对应版本视为阻断性文档 Finding。任何 AI 开发者不得自行豁免本规范；只有获授权的项目治理机构可以依照第 5 节批准有期限的例外。既有文档按登记批次迁移；尚未迁移的文档必须标记为 NOT STARTED 或 STALE，不得宣称已经完成双语化。
