# Bilingual Governance and Documentation Policy / 双语治理与文档规范

- Policy ID: GOV-DOC-001
- Version: 1.2
- Status: DRAFT — PENDING FORMAL GOVERNANCE APPROVAL
- Previous Version: 1.1
- Previous Version Status: NORMATIVE
- Owner: A — Principal Integration / Architecture Governance
- Applies to: All Owners (A–I), contributors, AI developers, AI coding agents, AI reviewers, architecture agents, AI sessions, and all repositories formally included in the project's development governance scope.
- Supersedes: No existing normative version until v1.2 is formally approved and adopted.

> This document is a proposed extension of the existing GOV-DOC-001 policy. It does not create a new Policy ID, retroactively rewrite historical records, or become normative merely by being drafted, committed, or merged.
>
> 本文件是现有 GOV-DOC-001 的扩展草案，不创建新的 Policy ID，不追溯改写历史记录，也不因起草、提交或合并而自动成为规范性制度。

---

## 1. Policy statement / 规范声明

**EN**

Every architecture design or architecture change MUST be documented in both Chinese and English. The two language versions are a single deliverable and MUST be updated in the same change set.

Every governed Umbrella Requirement, newly created GitHub Issue, newly created Git Commit Message, and Pull Request title and body MUST provide Chinese and English content according to this policy.

The two language versions MUST preserve the same meaning, authority, scope, status, constraints, evidence, and decision boundaries.

This policy is a repository-wide governance requirement. It is not an optional translation guideline and is not limited to documents labelled as major specifications.

**中文**

每一项架构设计或架构变更都必须同时形成中文和英文文档。两种语言版本属于同一项交付物，必须在同一个变更集中同步更新。

所有纳入治理范围的 Umbrella Requirement、所有新建 GitHub Issue、所有新建 Git Commit Message，以及所有 Pull Request 标题和正文，都必须按照本规范提供中文和英文内容。

中英文版本必须保持相同的含义、权威性、范围、状态、约束、证据和决策边界。

本规范是全仓库治理要求，不是可选的翻译建议，也不只适用于标记为主要规范的文档。

## 2. Scope / 适用范围

### 2.1 Architecture documentation / 架构文档

**EN**

The bilingual requirement applies to, at minimum:

- System and subsystem architecture, component boundaries, responsibility assignments, and dependency maps.
- Domain models, schemas, data contracts, lifecycle/state machines, invariants, and transaction semantics.
- APIs, protocols, message envelopes, field definitions, compatibility rules, and error semantics.
- Security, identity, Scope, Permission, retention, Forget, audit, and threat models.
- Storage, indexes, cache, consistency, recovery, deployment, and operational design.
- Technology evaluations, ADRs, engineering decisions, resource budgets, and benchmark plans/results.
- Test strategies, conformance requirements, acceptance criteria, and architecture review findings.
- Any change that alters the meaning, constraints, status, examples, or implementation guidance of the above.

**中文**

适用范围至少包括：

- 系统和子系统架构、组件边界、职责分配及依赖关系图。
- 领域模型、Schema、数据契约、生命周期/状态机、不变式及事务语义。
- API、协议、消息封装、字段定义、兼容性规则及错误语义。
- 安全、身份、Scope、Permission、保留策略、Forget、审计及威胁模型。
- 存储、索引、缓存、一致性、恢复、部署及运维设计。
- 技术评估、ADR、工程决策、资源预算及基准测试计划/结果。
- 测试策略、一致性要求、验收标准及架构审查发现。
- 任何改变上述内容含义、约束、状态、示例或实施指导的修改。

### 2.2 Technical-language exceptions / 技术原文例外

**EN**

Code comments, generated API references, machine-generated schema dumps, and raw test logs may remain in their natural technical language when duplicating or translating them would be harmful or mechanically misleading.

However, their architecture meaning, usage constraints, and interpretation MUST be explained in both language versions of the owning specification.

**中文**

代码注释、自动生成的 API 参考、机器生成的 Schema 转储和原始测试日志，在重复或翻译会造成误导或破坏机器可读性的情况下，可以保留其自然技术语言。

但是，所属规范必须用中英文解释这些内容的架构含义、使用约束和解读方式。

### 2.3 Umbrella Requirements / 大需求

**EN**

Every governed Umbrella Requirement MUST contain complete Chinese and English versions of its substantive content.

At minimum, this includes:

- Requirement identity and metadata.
- Background and source quotations.
- Problem statement and objectives.
- Scope, included items, and excluded items.
- Requirements and expected outcomes.
- Acceptance criteria and checklists.
- Dependencies, related artifacts, and references.
- Current status, decision authority, unresolved issues, and evidence limitations.

An Umbrella Requirement is a durable requirement record. Bilingual completion MUST NOT be interpreted as Owner approval, architecture approval, implementation completion, or normative adoption.

**中文**

每个纳入治理范围的 Umbrella Requirement 都必须具有完整的中英文实质性内容。

至少包括：

- 需求标识和元数据。
- 背景和原始引文。
- 问题陈述和目标。
- 范围、包含事项和排除事项。
- 需求及预期结果。
- 验收标准和检查清单。
- 依赖、关联工件和引用。
- 当前状态、决策权限、未解决问题及证据限制。

Umbrella Requirement 是长期保存的需求记录。完成双语化不得被解释为 Owner 批准、架构批准、实现完成或规范采纳。

### 2.4 GitHub Issues / GitHub Issue

**EN**

Every newly created GitHub Issue within the governed repository MUST have a bilingual title and bilingual substantive body.

The title SHOULD use:

`[STABLE-ID] English title / 中文标题`

The body MUST use paired English and Chinese sections for every substantive section.

Original quotations MUST be preserved verbatim. An accurate translation MUST be provided adjacent to each quotation without replacing the original.

Stable identifiers, source references, dates, evidence, unknown values, and status tokens MUST remain unchanged.

Existing historical Issues are subject to tracked migration. This policy does not authorize bulk rewriting, state changes, or invented historical content.

**中文**

治理仓库中所有新建 GitHub Issue 都必须具有双语标题和双语实质性正文。

标题应采用：

`[STABLE-ID] English title / 中文标题`

正文的每个实质性章节都必须提供成对的英文和中文内容。

原始引文必须逐字保留，并在其附近提供准确翻译，不得用译文替换原文。

稳定标识、来源引用、日期、证据、未知值和状态 Token 必须保持不变。

既有历史 Issue 必须纳入有记录的迁移。本规范不授权批量改写、状态变更或补造历史内容。

### 2.5 Commit Messages / Git 提交信息

**EN**

Every newly created Git Commit Message in a governed repository MUST contain bilingual Subject and Body content.

The recommended Subject format is:

`<type>(<scope>): <English summary> / <中文摘要>`

The Body MUST contain an English section and a Chinese section when substantive explanatory content is present.

Footer metadata, issue references, stable identifiers, trailers, and machine-consumed tokens MUST remain canonical and MUST NOT be translated.

Historical commits MUST NOT be rewritten solely to satisfy this policy.

**中文**

治理仓库中所有新建 Git Commit Message 都必须包含双语 Subject 和 Body。

推荐 Subject 格式：

`<type>(<scope>): <English summary> / <中文摘要>`

存在实质性说明内容时，Body 必须同时包含英文部分和中文部分。

Footer 元数据、Issue 引用、稳定标识、Trailer 和机器消费的 Token 必须保持规范原文，不得翻译。

不得仅为了满足本规范而重写历史 Commit。

### 2.6 Pull Requests / Pull Request

**EN**

Every newly created Pull Request MUST have a bilingual title and bilingual substantive description.

The title SHOULD use:

`[STABLE-ID] English title / 中文标题`

The body MUST include paired English and Chinese descriptions of:

- Objective and background.
- Scope and excluded work.
- Changes and affected paths.
- Baseline and source revisions.
- Verification commands and actual results.
- Acceptance criteria and disposition.
- Risks, limitations, and unresolved items.
- Review and approval status.
- Related Issues, Work Items, and evidence.

A PR's bilingual completeness MUST NOT be interpreted as permission to merge, approve, close, or adopt a policy.

**中文**

所有新建 Pull Request 都必须具有双语标题和双语实质性描述。

标题应采用：

`[STABLE-ID] English title / 中文标题`

正文必须为以下内容提供成对的中英文描述：

- 目标和背景。
- 工作范围和排除事项。
- 修改内容和受影响路径。
- 基线和来源修订。
- 验证命令及实际结果。
- 验收标准和处置结果。
- 风险、限制和未解决事项。
- 审查和批准状态。
- 关联 Issue、Work Item 和证据。

PR 双语内容完整，不代表获得合并、批准、关闭或规范采纳授权。

### 2.7 Repository inheritance / 仓库继承

**EN**

All future development repositories, subrepositories, and supporting repositories formally included in the project's governance scope MUST inherit GOV-DOC-001.

The inheriting repository MUST:

1. Identify GOV-DOC-001 as its governing bilingual policy.
2. Preserve the same Policy ID and approved version reference.
3. Link to the authoritative policy source.
4. Provide a repository-local adoption record or inheritance declaration.
5. Include bilingual requirements in its Issue, Commit Message, PR, and documentation workflows.
6. Maintain a local migration register for historical records.
7. Preserve stable identifiers and decision authority.
8. Record any formally approved, time-bounded exception without silently weakening the inherited policy.

Repository inheritance does not automatically authorize creation, modification, migration, or activation of a future repository.

**中文**

所有未来正式纳入项目治理范围的开发仓库、子仓库和配套仓库，都必须继承 GOV-DOC-001。

继承仓库必须：

1. 明确 GOV-DOC-001 为其适用的双语治理规范。
2. 保留相同的 Policy ID 和已批准版本引用。
3. 链接至权威规范来源。
4. 提供仓库本地采纳记录或继承声明。
5. 在 Issue、Commit Message、PR 和文档工作流中落实双语要求。
6. 维护本地历史迁移登记表。
7. 保留稳定标识和决策权限。
8. 对正式批准且有期限的例外进行登记，不得静默削弱继承规范。

仓库继承机制不自动授权创建、修改、迁移或启用任何未来仓库。

## 3. Mandatory duties for every AI developer / 所有 AI 开发者的强制职责

**EN**

This policy applies to every AI developer, AI coding agent, AI reviewer, AI architecture agent, and AI session working in a governed repository—not only the A–I Owners and not only the documentation role.

The accountable Owner remains responsible for ensuring that every delegated AI session receives and follows this requirement.

Every AI developer MUST, before starting a task:

1. Read this policy and the relevant bilingual portal/style/glossary guidance.
2. Locate the current Chinese and English counterparts of every architecture contract affected by the task.
3. Identify which language files are authoritative source specifications and which are reader guides or translations; never assume a translated guide overrides an approved source contract.
4. Identify the affected Issues, Umbrella Requirements, Commit Messages, and PR deliverables.
5. Include bilingual-documentation work explicitly in its task plan, prompt, scope, and acceptance criteria.

During the task, every AI developer MUST:

1. Create or update both language versions in the same change set whenever it creates or changes architecture meaning, constraints, interfaces, state, security, failure behavior, compatibility, technology decisions, resource assumptions, tests, or acceptance criteria.
2. Keep both versions aligned as the design evolves; do not defer translation until an informal later cleanup.
3. Preserve stable identifiers, decision status, open issues, evidence references, and exact source revision.
4. Update reciprocal links and the documentation coverage/status register.
5. Keep newly created Issues, Commit Messages, and PR titles/descriptions bilingual.
6. If source material is incomplete, conflicting, or not approved, preserve that uncertainty in both languages and escalate to the accountable Owner. Translation is not authority to decide.

Before reporting a task complete, every AI developer MUST provide a bilingual change manifest and verify counterpart existence, semantic parity, identifier parity, status parity, and links.

A task that changes architecture semantics is NOT DONE while its counterpart is missing, stale without an approved exception, or materially inconsistent.

AI reviewers and integration agents MUST check this requirement as an explicit review dimension. They MUST raise a finding and block documentation acceptance when the requirement is not met.

A task prompt that omits this requirement is incomplete and MUST be corrected before execution or acceptance.

**中文**

本规范适用于在治理仓库工作的每一位 AI 开发者、AI 编码 Agent、AI 审查者、AI 架构 Agent 和每一个 AI 会话，而不只是 A–I Owner 或文档岗位。

委派任务的责任 Owner 必须确保每个 AI 会话收到并遵守本要求。

每位 AI 开发者在开始任务前 MUST：

1. 阅读本规范以及相关双语入口、写作规范和术语表。
2. 找到任务涉及的每份架构契约当前的中文和英文对应版本。
3. 确认哪些文件是权威源规范，哪些是阅读指南或翻译；不得假设翻译版指南可以覆盖已批准的源契约。
4. 识别受影响的 Issue、Umbrella Requirement、Commit Message 和 PR 交付物。
5. 在任务计划、提示词、工作范围和验收标准中明确列入双语文档工作。

执行任务期间，每位 AI 开发者 MUST：

1. 只要新增或改变架构含义、约束、接口、状态、安全、故障行为、兼容性、技术决策、资源假设、测试或验收条件，就必须在同一个变更集中创建或更新中英文两个版本。
2. 随设计演进同步维护两种语言，不得把翻译推迟到非正式的后续清理阶段。
3. 保留稳定标识、决策状态、未决事项、证据引用和准确源版本。
4. 更新双向链接和文档覆盖/状态登记表。
5. 确保新建 Issue、Commit Message 和 PR 标题/描述符合双语要求。
6. 如果源材料不完整、存在冲突或尚未批准，必须在两种语言中保留其不确定性并升级给责任 Owner。翻译不构成决策授权。

在报告任务完成前，每位 AI 开发者 MUST 提供双语变更清单，并验证对应文件存在、语义一致、标识一致、状态一致且链接有效。

凡改变架构语义的任务，只要另一语言版本缺失、未经批准的例外而过期，或存在实质不一致，就属于 NOT DONE。

AI 审查者和集成 Agent MUST 将本要求作为明确的审查维度。未满足时 MUST 提出 Finding 并阻止文档验收。

遗漏本要求的任务提示词属于不完整提示词，必须在执行或验收前修正。

## 4. Required parity / 双语一致性要求

**EN**

Chinese and English counterparts MUST preserve:

1. The same document/policy/requirement identity and compatible version.
2. The same scope, authority, ownership, and normative force.
3. The same requirements, constraints, caveats, failure modes, security boundaries, and non-guarantees.
4. The same state machines, examples, diagrams, tables, and acceptance criteria where applicable.
5. The same decision status, including DECIDED, RECOMMENDED, CANDIDATE, OPEN, BLOCKED, TO_VALIDATE, RECORDED, and other applicable canonical tokens.
6. Reciprocal links and traceability to the exact source revision.
7. The same unknown or unavailable information, without filling gaps through inference.

Stable identifiers MUST NOT be translated or renamed, including:

- REQ-01 through REQ-05.
- Policy IDs and Work Item IDs.
- Issue and PR numbers.
- Commit SHAs and Blob SHAs.
- File paths.
- API fields and names.
- JSON keys, enum values, type names, and protocol constants.
- State tokens and evidence references.
- ADR IDs and repository identifiers.

Explanatory prose SHOULD translate the meaning while retaining canonical identifiers.

**中文**

中英文版本 MUST 保持：

1. 相同的文档/规范/需求标识和兼容版本。
2. 相同的适用范围、权威性、责任归属和规范效力。
3. 相同的需求、约束、注意事项、失败模式、安全边界和非保证事项。
4. 在适用情况下保持相同的状态机、示例、图表、表格和验收标准。
5. 相同的决策状态，包括 DECIDED、RECOMMENDED、CANDIDATE、OPEN、BLOCKED、TO_VALIDATE、RECORDED 及其他适用的规范 Token。
6. 双向链接以及对准确源修订的追溯能力。
7. 相同的未知或不可用信息，不得通过推断填补空白。

以下稳定标识 MUST NOT 翻译或改名：

- REQ-01 至 REQ-05。
- Policy ID 和 Work Item ID。
- Issue 和 PR 编号。
- Commit SHA 和 Blob SHA。
- 文件路径。
- API 字段及名称。
- JSON Key、枚举值、类型名和协议常量。
- 状态 Token 和证据引用。
- ADR ID 和仓库标识。

说明性文字应翻译其含义，同时保留规范标识。

## 5. Change and review gates / 变更与审查门禁

### 5.1 Architecture changes / 架构变更

**EN**

An architecture PR MUST include:

- Both Chinese and English files for every new or changed architecture document.
- A paired-document change list, source revision, and version information.
- A terminology and decision-status parity check.
- Link and diagram validation.
- An explicit statement when a change is explanatory only and does not alter normative semantics.

A PR that changes architecture semantics in only one language MUST NOT pass architecture documentation acceptance. Reviewers MUST request the missing counterpart or a documented exception.

**中文**

架构 PR MUST 包含：

- 每份新增或修改架构文档的中英文文件。
- 双语文件变更清单、源修订和版本信息。
- 术语和决策状态一致性检查。
- 链接和图表验证。
- 如果变更仅为解释性改写、不改变规范语义，必须明确声明。

只修改一种语言且改变架构语义的 PR MUST NOT 通过架构文档验收。审查者 MUST 要求补齐另一语言版本，或提供正式例外记录。

### 5.2 Issue, Commit, and PR review / Issue、Commit 和 PR 审查

**EN**

Reviewers MUST check bilingual completeness for:

- Issue titles and substantive bodies.
- Umbrella Requirement content.
- Commit Subjects and Bodies.
- PR titles and substantive descriptions.

The review MUST also check stable identifiers, quotations, source references, evidence, unknown fields, and status preservation.

A bilingual format check does not replace semantic review or authorization checks.

**中文**

审查者 MUST 检查以下内容的双语完整性：

- Issue 标题和实质性正文。
- Umbrella Requirement 内容。
- Commit Subject 和 Body。
- PR 标题和实质性描述。

审查还 MUST 检查稳定标识、原始引文、来源引用、证据、未知字段和状态保留情况。

双语格式检查不能替代语义审查或授权检查。

### 5.3 Temporary exception / 临时例外

**EN**

An emergency or time-critical change MAY temporarily land with one counterpart marked STALE / 翻译待同步, but only if the same PR records:

- Why simultaneous bilingual completion is not practical.
- Which language/version is currently authoritative for the immediate change.
- The missing counterpart path and exact source revision.
- A named accountable Owner.
- A due date and tracking Issue/PR.
- The authorized exception decision and its evidence reference.

The exception MUST NOT be used to hide unresolved design semantics or to bypass Owner/ADR approval.

The stale counterpart MUST be updated before the next dependent architecture baseline is accepted and no later than the recorded due date.

The exception is visible technical debt, not completion.

**中文**

紧急或有时限要求的变更 MAY 临时只提交一种语言，但同一 PR 必须将另一版本标记为 STALE / 翻译待同步，并记录：

- 无法同时完成双语版本的原因。
- 当前变更临时采用的权威语言/版本。
- 缺失的对应文件路径和准确源修订。
- 明确的责任 Owner。
- 截止日期和跟踪 Issue/PR。
- 正式批准的例外决议及其证据引用。

该例外 MUST NOT 用于掩盖未决设计语义或绕过 Owner/ADR 审批。

另一语言版本 MUST 在下一个依赖该设计的架构基线验收前补齐，且不得晚于登记期限。

例外属于可见技术债，不代表交付完成。

### 5.4 Historical migration / 历史迁移

**EN**

Existing historical architecture documents, Issues, Umbrella Requirements, and Commit Messages MUST be inventoried and migrated through tracked batches.

Historical migration MUST:

1. Preserve the original source and original stable identifiers.
2. Preserve original quotations and add accurate translations.
3. Preserve original state, decision status, authorship, dates, and evidence.
4. Mark unavailable historical information as NOT_RECORDED or the applicable canonical unknown token.
5. Record migration responsibility, tracking Work Item, and completion evidence.
6. Distinguish MIGRATION_DEBT from formally authorized EXEMPTION.
7. Never rewrite historical commits or alter historical Commit SHAs.
8. Never classify an item as exempt without an explicit authorization record.

Historical single-language artifacts are migration debt by default, not automatically exempt.

**中文**

既有历史架构文档、Issue、Umbrella Requirement 和 Commit Message MUST 纳入清点，并通过有记录的批次进行迁移。

历史迁移 MUST：

1. 保留原始来源和原始稳定标识。
2. 保留原始引文，并增加准确翻译。
3. 保留原始状态、决策状态、作者、日期和证据。
4. 将不可获得的历史信息标记为 NOT_RECORDED 或适用的规范未知 Token。
5. 记录迁移责任、跟踪 Work Item 和完成证据。
6. 区分 MIGRATION_DEBT 与正式授权的 EXEMPTION。
7. 永不重写历史 Commit 或修改历史 Commit SHA。
8. 未有明确授权记录时，永不将遗留项分类为豁免。

历史单语工件默认属于迁移技术债，不自动属于豁免。

## 6. Authority and decision control / 权威与决策控制

**EN**

This policy governs documentation completeness and parity; it does not transfer architecture decision authority.

The relevant Owner remains responsible for its domain contract. Cross-owner decisions follow the established integration governance and ADR process.

Translation MUST NOT:

- Turn CANDIDATE, OPEN, BLOCKED, or TO_VALIDATE into DECIDED.
- Turn RECORDED into APPROVED or ADOPTED.
- Resolve a disagreement between Owner specifications by choosing one language's wording.
- Invent missing fields, behavior, guarantees, or implementation evidence.
- Describe a design as implemented, tested, atomic, secure, or production-ready without evidence.
- Change Issue, PR, or Work Item state.
- Grant merge, approval, release, or repository creation authority.

No AI developer may approve this policy or waive it on its own.

Only the authorized project governance authority may approve GOV-DOC-001 v1.2 and may approve a time-bounded exception under this policy.

**中文**

本规范只管理文档完整性和双语一致性，不转移架构决策权。

各领域契约仍由相应 Owner 负责；跨 Owner 决策仍遵循既有集成治理和 ADR 流程。

翻译 MUST NOT：

- 将 CANDIDATE、OPEN、BLOCKED 或 TO_VALIDATE 改写为 DECIDED。
- 将 RECORDED 改写为 APPROVED 或 ADOPTED。
- 通过选择某种语言的措辞来裁决 Owner 规范冲突。
- 补造缺失字段、行为、保证或实现证据。
- 在没有证据时声称设计已经实现、测试、具备原子性、安全性或生产就绪。
- 改变 Issue、PR 或 Work Item 状态。
- 授予合并、批准、发布或创建仓库的权限。

任何 AI 开发者均不得自行批准本规范或自行豁免本规范。

只有获授权的项目治理机构可以批准 GOV-DOC-001 v1.2，并可以依照本规范批准有期限的例外。

## 7. Definition of done / 完成定义

**EN**

A bilingual architecture or governance deliverable is complete only when:

1. Both language versions exist and are linked.
2. A bilingual reviewer confirms semantic and normative parity.
3. Stable identifiers match exactly.
4. All open items and status labels match.
5. Original quotations and translations are preserved.
6. Links, tables, diagrams, and examples have been checked.
7. The source revision and review evidence are recorded.
8. Required Issue, Commit, and PR metadata is bilingual.
9. Any migration debt or exception is registered.
10. Required Owner and governance approvals are recorded separately.

**中文**

双语架构或治理交付物只有满足以下条件才算完成：

1. 两种语言版本均存在并互相链接。
2. 双语审查者确认语义和规范效力一致。
3. 稳定标识完全一致。
4. 所有未决事项和状态标签一致。
5. 原始引文及其翻译均得到保留。
6. 链接、表格、图表和示例已经检查。
7. 源修订和审查证据已经记录。
8. 必需的 Issue、Commit 和 PR 元数据符合双语要求。
9. 所有迁移技术债或例外均已登记。
10. 必需的 Owner 和治理批准分别得到记录。

## 8. Enforcement / 执行

**EN**

This policy is effective for new governed work only after its adoption into the repository's approved governance baseline.

Until formal approval and adoption of v1.2, v1.1 remains the existing normative version.

After adoption, all A–I Owners and all AI developers/sessions MUST apply the expanded requirements to future design proposals, review reports, specifications, ADRs, implementation-facing contract changes, technology decisions, test/acceptance changes, Issues, Umbrella Requirements, Commit Messages, PRs, and material revisions.

The task Owner MUST put this requirement into every delegated prompt and verify the returned bilingual manifest.

Reviewers MUST treat missing or materially divergent counterparts as a blocking documentation finding.

Existing records MUST be migrated in tracked batches. Unmigrated items MUST be listed as MIGRATION_DEBT, NOT STARTED, or STALE as applicable, rather than represented as bilingual-complete.

No AI developer may waive this policy on its own.

**中文**

本规范只有在正式纳入仓库已批准治理基线后，才对新的治理工作生效。

在 v1.2 正式批准和采纳之前，v1.1 继续保持现有规范效力。

v1.2 采纳后，A–I 所有 Owner 以及所有 AI 开发者/会话 MUST 在后续设计提案、审查报告、规范、ADR、面向实现的契约变更、技术决策、测试/验收变更、Issue、Umbrella Requirement、Commit Message、PR 和重要修订中执行扩展要求。

任务 Owner MUST 将本要求写入每一份委派提示词，并核验 AI 返回的双语变更清单。

审查者 MUST 将缺失或实质不一致的对应版本视为阻断性文档 Finding。

既有记录 MUST 按有记录的批次迁移。尚未迁移的项目 MUST 根据实际情况标记为 MIGRATION_DEBT、NOT STARTED 或 STALE，不得宣称已经完成双语化。

任何 AI 开发者均不得自行豁免本规范。

## 9. Repository inheritance procedure / 仓库继承程序

**EN**

A future repository becomes subject to this policy when it is formally included in the project's governance scope by an authorized project decision.

Before governed development begins, the repository MUST:

1. Record its repository identity and accountable Owner.
2. Link the authoritative GOV-DOC-001 source.
3. Record the inherited version and effective adoption reference.
4. Include the bilingual Issue, Commit Message, PR, and documentation templates or equivalent controls.
5. Establish a migration register.
6. Record local deviations as proposals pending approval, not unilateral exceptions.

The central governance repository maintains the authoritative policy. A child repository MUST NOT silently fork, weaken, or redefine the policy.

**中文**

未来仓库只有在经授权的项目决议正式纳入项目治理范围后，才受本规范约束。

在开始治理范围内的开发之前，该仓库 MUST：

1. 登记仓库身份和责任 Owner。
2. 链接权威 GOV-DOC-001 来源。
3. 记录继承版本和正式采纳依据。
4. 纳入双语 Issue、Commit Message、PR 和文档模板或等效控制措施。
5. 建立历史迁移登记表。
6. 将本地偏离记录为待批准提案，不得自行认定为例外。

中央治理仓库维护权威规范。子仓库 MUST NOT 静默分叉、削弱或重新定义本规范。

## 10. Version and transition control / 版本与过渡控制

**EN**

GOV-DOC-001 v1.2 is DRAFT until formally approved by the authorized governance authority.

Drafting, review, Git commit, pull request creation, PR merge, or file presence alone does not constitute normative approval.

Upon approval, the approval record MUST identify:

- Policy ID and approved version.
- Approving authority.
- Decision date.
- Exact approved Commit SHA.
- Exact policy Blob SHA.
- Effective date or adoption condition.
- Superseded version and transition rule.

Until that evidence exists, v1.1 remains the normative baseline and v1.2 remains a proposal.

**中文**

GOV-DOC-001 v1.2 在获授权治理机构正式批准之前始终为 DRAFT。

起草、审查、Git Commit、创建 Pull Request、PR 合并或文件存在本身均不构成规范批准。

正式批准时，批准记录 MUST 明确：

- Policy ID 和批准版本。
- 批准机构。
- 决议日期。
- 准确的批准 Commit SHA。
- 准确的 Policy Blob SHA。
- 生效日期或采纳条件。
- 被替代版本和过渡规则。

在上述证据存在之前，v1.1 继续作为规范基线，v1.2 继续作为提案。

---

## Appendix A. Stable identifier and status preservation / 附录 A：稳定标识和状态保留

**EN**

The following values MUST remain unchanged during translation and migration:

- REQ-01, REQ-02, REQ-03, REQ-04, REQ-05.
- GOV-DOC-001.
- Work Item IDs.
- Issue and PR numbers.
- Commit SHAs and Blob SHAs.
- Repository names and file paths.
- API names, field names, and machine-readable keys.
- OPEN, RECORDED, NOT_ASSIGNED, NOT_RECORDED, NOT_CONFIRMED.
- DECIDED, RECOMMENDED, CANDIDATE, BLOCKED, TO_VALIDATE.
- MIGRATION_DEBT, EXEMPTION, STALE, NOT STARTED, NOT RUN, NOT APPLICABLE.

No status may be upgraded, downgraded, or replaced through translation alone.

**中文**

翻译和迁移过程中，下列值 MUST 保持不变：

- REQ-01、REQ-02、REQ-03、REQ-04、REQ-05。
- GOV-DOC-001。
- Work Item ID。
- Issue 和 PR 编号。
- Commit SHA 和 Blob SHA。
- 仓库名称和文件路径。
- API 名称、字段名称和机器可读 Key。
- OPEN、RECORDED、NOT_ASSIGNED、NOT_RECORDED、NOT_CONFIRMED。
- DECIDED、RECOMMENDED、CANDIDATE、BLOCKED、TO_VALIDATE。
- MIGRATION_DEBT、EXEMPTION、STALE、NOT STARTED、NOT RUN、NOT APPLICABLE。

不得仅通过翻译升级、降级或替换任何状态。

## Appendix B. Migration evidence / 附录 B：迁移证据

**EN**

Every historical migration entry MUST identify the original object, language state, migration status, historical reason when known, authorized exception when applicable, accountable Owner, tracking Work Item, and completion evidence.

Unknown values MUST remain NOT_RECORDED.

**中文**

每项历史迁移登记 MUST 识别原始对象、语言状态、迁移状态、已知的历史原因、适用时的正式例外、责任 Owner、跟踪 Work Item 和完成证据。

未知值 MUST 保持 NOT_RECORDED。

## Appendix C. Non-retroactivity / 附录 C：非追溯性

**EN**

This policy does not rewrite historical Commit objects, historical authorship, historical decision authority, or historical evidence.

Historical single-language records are inventoried and migrated through new traceable changes. Their original SHA and source remain unchanged.

**中文**

本规范不重写历史 Commit 对象、历史作者信息、历史决策权限或历史证据。

历史单语记录通过新的可追溯变更进行清点和迁移。原始 SHA 和原始来源保持不变。
