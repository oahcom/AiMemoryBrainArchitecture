# AI Development Standard
# AI 开发规范

**Document ID:** AI-STD-001  
**Version:** 1.0  
**Status:** PROPOSED — initial governance baseline  
**Applies to:** All AI-assisted and AI-executed work in this repository  
**Normative language:** MUST / MUST NOT / SHOULD / MAY

> This standard establishes the engineering controls for a project developed by AI agents under explicit project governance. AI agents are developers, not autonomous authorities over project scope, security policy, or acceptance.

## 1. Purpose / 目的

The project is developed end-to-end by AI developers organized around named module Owners. Quality must come from explicit authority boundaries, reproducible work, independent verification, and traceable decisions—not from confidence or verbosity in an AI response.

本规范建立全 AI 开发项目的统一工程制度。质量依靠明确的职责边界、可复现的开发过程、独立验证和可追溯决策，而不是依靠 AI 的自我评价。

The standard governs architecture changes, implementation, tests, documentation, migrations, security changes, and release work. It applies equally to every Owner and cross-cutting specialist.

## 2. Governing principles / 基本原则

1. **Prompt is a controlled work instruction.** No substantive development starts from an informal chat request alone. A versioned task prompt MUST exist in the repository before execution.
2. **Owner accountability.** Every task has one accountable Owner. Multiple contributors may assist, but ownership is singular and explicit.
3. **Authority follows the contract.** An Owner may decide within its domain, but MUST NOT silently redefine another Owner's contracts.
4. **Independent verification.** The implementing AI MUST NOT be the sole reviewer or sole acceptance authority for its own work.
5. **Evidence over assertion.** “Implemented”, “tested”, “secure”, “passed” and “complete” require specific evidence.
6. **Small, reversible increments.** Prefer small vertical slices and narrow changes over broad speculative rewrites.
7. **Fail closed on uncertainty.** Unknown contract, identity, permission, data-loss, or recovery behavior blocks unsafe progression.
8. **No silent decisions.** Material changes require a decision record, rationale, alternatives, consequences, and affected owners.
9. **Traceability is mandatory.** Requirement → task → prompt version → branch/commit → changed files → tests → review → integration decision must be traceable.
10. **Tiered bilingual documentation practice.** Every AI developer/session MUST read GOV-DOC-001 and the [Bilingual Documentation Tiering Policy](bilingual-tiering-policy.md), inspect the applicable classification in the authorized tier inventory, and plan documentation work accordingly. Tier 1 files MUST have Chinese and English counterparts updated in the same change set; Tier 2 files are optional-bilingual only within the approved allowlist; Tier 3 files are Chinese-first and an English counterpart requires the responsible Owner's confirmation. UNKNOWN or unconfirmed classifications MUST be escalated for human confirmation and MUST NOT be treated as Tier 2 or Tier 3. These tiers do not waive the architecture-semantic bilingual gate in §7.1. The accountable Owner MUST enforce these requirements on delegated agents. Code comments and machine-generated artifacts may retain their natural technical language, but their architecture meaning MUST be explained bilingually where the gate applies.

## 3. AI developer roles / AI 开发角色

### 3.1 Module Owners

The project uses the A–I Owner model:

| Owner | Primary authority |
|---|---|
| A | Principal integration, cross-module contract registry, integration decisions |
| B | Domain model and canonical domain semantics |
| C | Agent integration, telemetry and inference-boundary requirements |
| D | Canonical Memory Brain, memory lifecycle and Forget semantics |
| E | Memory Compiler and derived-memory production |
| F | Memory Runtime, retrieval, activation, working sets and runtime cache |
| G | Memory Context, ContextVersion, ChangeSet and reconciliation |
| H | BMCP protocol and Adapter protocol behavior |
| I | Security, identity, authorization and governance |

Storage/Consistency, Testing/Quality, Observability/Performance and Release may operate as named cross-cutting specialist roles. They MUST have explicit task authority and MUST NOT silently take ownership of a module's domain decisions.

### 3.2 Required separation of duties

For every non-trivial task, assign:

- **Request/Task Sponsor:** clarifies intended outcome and priority.
- **Accountable Owner:** owns the domain result and branch.
- **Implementing AI:** performs the change under the approved prompt.
- **Independent Reviewer:** a separate AI session/agent that did not author the implementation.
- **Integration Architect:** checks cross-module compatibility and integration evidence.
- **Acceptance Authority:** approves scope, risk and merge according to project governance.

One AI session adopting several personas does NOT constitute independent review. A simulated panel is useful for brainstorming but is not evidence of independent approval.

**Governance interpretation for this repository's ChatGPT-native execution model (NR-001):** A genuinely new, separate ChatGPT conversation may satisfy “a separate AI session/agent” when the reviewer did not participate in the implementation and independently reads the exact frozen artifacts and evidence from GitHub. This provides conversation/context isolation only; it does not establish model, provider, runtime/environment, or statistical independence and MUST NOT be described as multi-model consensus. The reviewer MUST disclose this limitation. All R3 requirements remain unchanged: independent security/domain specialist review and reproducible test evidence are still required before acceptance. This interpretation does not waive acceptance authority or permit self-approval.

**本仓库 ChatGPT 原生执行模型的治理解释（NR-001）：** 真正新建的独立 ChatGPT 对话，在 Reviewer 未参与实现且从 GitHub 独立读取准确冻结工件和证据时，可以满足“独立 AI 会话/Agent”的要求。这仅提供对话/上下文隔离，不构成模型、服务商、运行环境或统计意义上的独立，且**不得**描述为多模型共识。Reviewer **必须**披露这一限制。所有 R3 要求保持不变：验收前仍须进行独立安全/领域专业审查并提供可复现的测试证据。本解释不豁免验收授权，也不允许自我批准。

For low-risk documentation-only changes, one reviewer may cover several review dimensions, but author and reviewer MUST remain distinct. Security, data deletion, authorization, consistency, recovery and public protocol changes require independent specialist review.

## 4. Task classification and gates / 任务分类与门禁

Every work item MUST declare its class:

- **ARCH:** architecture or contract definition;
- **IMPL:** production implementation;
- **TEST:** test infrastructure, fixtures or conformance tests;
- **SEC:** security, identity, privacy, retention or deletion;
- **MIG:** schema/data migration or compatibility;
- **PERF:** performance/resource measurement;
- **DOC:** documentation-only;
- **OPS:** build, CI, release or operational work.

Risk levels:

- **R0:** editorial, no normative or executable behavior change;
- **R1:** isolated implementation/documentation with bounded impact;
- **R2:** cross-module contract, persistence, protocol, concurrency or compatibility impact;
- **R3:** security boundary, authorization, Forget/deletion, data integrity, recovery, migration or release-critical change.

R2/R3 require explicit impact analysis and named reviewers. R3 requires security/domain specialist review and reproducible test evidence before acceptance.

### 4.1 Work item lifecycle / 工作项生命周期

AI-STD-001 uses six operational phases to reduce status-label complexity. The original twelve checkpoints remain distinct as gate milestones and MUST be preserved in lifecycle.source_status and lifecycle.gates. This mapping becomes normative only after independent review and Owner acceptance.

| Operational phase | Source checkpoint(s) | Meaning / 含义 |
|---|---|---|
| INTAKE | PROPOSED, ANALYZED, PROMPT_READY | Proposal, analysis and prompt preparation / 提议、分析与提示词准备 |
| READY | READY | Execution prerequisites satisfied / 执行前置条件满足 |
| ACTIVE | IN_PROGRESS, IMPLEMENTED | Implementation underway or submitted / 实现进行中或已提交 |
| VALIDATION | VERIFIED, REVIEWED, INTEGRATION_READY | Verification, independent review and integration-readiness gates / 验证、独立评审和集成就绪门禁 |
| ACCEPTANCE | ACCEPTED | Explicit acceptance-authority decision / 接受权限主体明确决策 |
| COMPLETE | MERGED, CLOSED | Merge and closeout milestones / 合并与结项检查点 |

The phase is a grouping, NOT a gate result. VERIFIED, REVIEWED and INTEGRATION_READY require separate evidence. ACCEPTED, MERGED and CLOSED remain distinct decisions/milestones and MUST NOT be inferred from one another. See status-migration-map.en.md and status-migration-map.zh-CN.md.

六个操作阶段仅用于归并状态标签，不代表门禁自动通过。VERIFIED、REVIEWED、INTEGRATION_READY 必须分别保留证据。ACCEPTED、MERGED、CLOSED 仍是独立决策/里程碑，不得相互推断。映射细节见中英文迁移表。

### 4.2 Independent gate evidence / 独立门禁证据

The following gates remain mandatory and independently auditable; phase grouping does not waive, combine or auto-pass them:
- VERIFIED: exact commands, environment, tested commit SHA, expected/actual results and logs.
- REVIEWED: reviewer separate from implementer, exact reviewed Head, report and finding dispositions.
- INTEGRATION_READY: cross-module compatibility evidence and required registry updates.
- ACCEPTED: explicit decision by the authorized acceptance authority; no self-acceptance.
- MERGED: target branch and merge commit SHA, after required approval.
- CLOSED: traceability/index update and closeout evidence.

以下门禁仍然强制且必须独立审计；阶段归并不得豁免、合并或自动通过：
- VERIFIED：准确命令、环境、测试 Commit SHA、预期/实际结果及日志。
- REVIEWED：与实现者分离的 Reviewer、准确审查 Head、报告及发现处置。
- INTEGRATION_READY：跨模块兼容证据及必要的注册表更新。
- ACCEPTED：获授权接受主体的明确决定，不允许自我接受。
- MERGED：在所需批准后记录目标分支和 Merge Commit SHA。
- CLOSED：可追溯性/索引更新和结项证据。

### 4.3 Orthogonal markers and independent lifecycles / 正交标记与独立生命周期

BLOCKED and REJECTED remain orthogonal markers, not operational phases. They may accompany any phase and MUST retain reason, responsible party, known timestamp and resolution/disposition evidence. They MUST NOT be silently converted into a normal phase.

BLOCKED 和 REJECTED 保留为正交标记，而非操作阶段。它们可伴随任一阶段，并 MUST 保留原因、责任方、已知时间及解决/处置证据，不得静默转换为正常阶段。

Architecture decision records retain their own independent lifecycle and status vocabulary. This work item MUST NOT migrate, rename or collapse architecture-decision states. Owner role definitions, including Owner G's charter, are unchanged.

架构决策记录继续使用独立生命周期和状态词汇。本工作项 MUST NOT 迁移、重命名或合并架构决策状态。包括 Owner G Charter 在内的 Owner 角色定义均不变。

### 4.4 Migration safety / 迁移安全

Migration MUST be dry-run by default, additive, idempotent, backup-first and reversible. Preserve exact source status and all historical evidence; only the exact twelve source values listed in §4.1 are eligible. Decorated, unknown, missing or ambiguous values fail closed and remain unchanged for review. Never infer missing review, acceptance, integration, merge or closeout evidence. The original status field remains intact during compatibility migration; the six-phase value is added under lifecycle.phase. A later canonical-field cutover requires separate authorization and an inventory of all readers, writers and historical records.

迁移 MUST 默认 dry-run、增量、幂等、先备份且可回滚。必须保留精确源状态及全部历史证据；只有 §4.1 列出的十二个精确源状态可迁移。带说明后缀、未知、缺失或有歧义的值必须 fail closed，保持不变并等待审查。不得推断缺失的评审、接受、集成、合并或结项证据。兼容阶段保留原始 status 字段，六阶段值新增于 lifecycle.phase。后续规范字段切换必须另行授权，并先盘点所有读写方及历史记录。

## 5. Prompt engineering as controlled engineering / 提示词工程化

A task prompt is a versioned engineering artifact, not disposable chat text.

**Canonical storage location:** all reusable prompts MUST be stored in the repository-root `prompts/` directory before execution. Global prompts MUST be placed directly under `prompts/`; Owner-specific prompts MUST be placed only under `prompts/A/` through `prompts/I/`. Do not place Owner prompts at the root or duplicate global rules in Owner files. Cross-owner tasks combine the global prompts with the relevant Owner prompts. The exact prompt actually executed MUST be copied into its Work Item evidence bundle with Prompt ID, version and SHA-256. Executed prompt versions are immutable.

**规范存储位置：** 所有可复用提示词 MUST 在执行前存入仓库根目录的 `prompts/`。全局提示词 MUST 直接放在 `prompts/` 根目录；Owner 专属提示词 MUST 仅放在 `prompts/A/` 至 `prompts/I/` 对应目录中。不得将 Owner 提示词放在根目录，也不得在 Owner 文件中重复复制全局规则。跨 Owner 任务组合全局提示词和相关 Owner 提示词。实际执行的准确提示词 MUST 连同 Prompt ID、版本和 SHA-256 复制到 Work Item 证据包。已执行提示词版本不可修改。

Start from the [canonical Prompt Library](../prompts/README.md). Every AI session MUST read `prompts/global-project-developer.md` and `prompts/global-bilingual-documentation.md`, plus its assigned Owner prompt. Review sessions MUST also read `prompts/global-architecture-reviewer.md`.

### 5.1 Seven core elements / 七项核心要素

Every new task prompt MUST use the following seven core sections. Seven means seven structural sections, not seven fields. Required detail belongs inside the relevant section; the prompt MUST remain concise and MUST NOT duplicate global policy text. AI-PROMPT-STD-001 §4 retains twelve mandatory content requirements, mapped into these seven sections; those requirements are content obligations, not additional headings. AI-STD-001 §5.1 governs section count/names, while AI-PROMPT-STD-001 §4 governs the twelve content obligations. Both MUST be satisfied. If any requirement cannot be represented without loss, the prompt is NOT READY and the conflict MUST be escalated; authors MUST NOT add extra mandatory top-level headings as a workaround.

每个新任务提示词 MUST 使用以下七个核心章节。七项指七个结构章节，而非七个字段。必要细节应放入对应章节；提示词应保持简洁，不得重复粘贴全局规范全文。 AI-PROMPT-STD-001 §4 的十二项强制要求继续有效，并映射到这七个章节中；这些要求属于内容义务，不是额外标题。AI-STD-001 §5.1 决定章节数量和名称，AI-PROMPT-STD-001 §4 决定十二项内容义务，两者必须同时满足。若任何要求无法在不丢失含义的情况下映射，提示词即为 NOT READY，必须升级处理；不得通过增加额外强制顶层标题规避冲突。

1. **Task identity / 任务标识:** Work Item ID; Prompt ID/version; accountable Owner; implementer and independent reviewer roles; repository and branch; task class/risk; owning Issue/PR carrier.
2. **Goal and boundaries / 目标与边界:** What, Why, observable objective, and explicit Out of Scope.
3. **Context and dependencies / 上下文与依赖:** base branch/full Base SHA; required source paths with version/status and blob/commit SHA; dependency Owner/contracts and exact revisions; applicable global/Owner prompts.
4. **Constraints and execution guidance / 约束与执行指导:** mandatory normative constraints, invariants, trust and authority boundaries; distinguish mandatory controls from adaptable recommended steps. Risk analysis is performed at the appropriate lifecycle gate.
5. **Acceptance and deliverables / 验收与交付物:** objective, observable acceptance criteria; required artifacts and report paths; applicable bilingual paths/manifest under GOV-DOC-001.
6. **Evidence and review / 证据与审查:** P0 traceability and acceptance evidence; applicable P1 verification evidence; review level and required independent/specialist review.
7. **Stop conditions and coordination / 停止条件与协调:** blockers, stop/escalation triggers, decision Owner, Issue/PR coordination route, and objective resume condition.

1. **任务标识：** Work Item ID、Prompt ID/版本、责任 Owner、实现者与独立审查者角色、仓库与分支、任务类别/风险等级、归属 Issue/PR 载体。
2. **目标与边界：** 做什么、为什么、可观测目标，以及明确的不在范围内事项。
3. **上下文与依赖：** 基线分支/完整 Base SHA、必读源文件路径及版本/状态和 Blob/Commit SHA、依赖 Owner/契约及准确版本、适用的全局/Owner 提示词。
4. **约束与执行指导：** 强制规范约束、不变式、信任边界和权限边界；区分强制控制与可调整的推荐步骤。风险分析在适当生命周期门禁执行。
5. **验收与交付物：** 客观可观测的验收条件、必需工件和报告路径，以及 GOV-DOC-001 要求适用时的双语路径/清单。
6. **证据与审查：** P0 可追溯性和验收证据、适用的 P1 验证证据、审查级别及必需的独立/专业审查。
7. **停止条件与协调：** 阻塞和停止/升级触发条件、决策 Owner、Issue/PR 协调路径，以及客观恢复条件。

### 5.2 Evidence and lifecycle rules / 证据与生命周期规则

- **P0 is mandatory:** the exact executed Prompt ID/version and SHA-256 MUST be recorded in the immutable Work Item evidence bundle/manifest; record Base SHA, implementation Commit SHA(s), final branch Head SHA, changed-file list, read-back, acceptance disposition and carrier closeout. Never invent an unavailable digest or identifier.
- **P1 applies when relevant:** record exact commands, environment, tested commit SHA, expected/actual results and evidence links. Checks not run MUST be marked NOT RUN with reason; inapplicable checks MUST be marked NOT APPLICABLE with reason.
- P0/P1 classification MUST NOT waive any test, security, specialist review, bilingual, R2/R3, acceptance or release gate required by this standard, GOV-DOC-001, Owner contracts or other governing policies. In particular, R3 still requires independent security/domain specialist review and reproducible test evidence before acceptance.
- Security, failure, concurrency, recovery, privacy and compatibility analysis need not be exhaustively pre-written before the task is understood. They MUST be identified and addressed at the lifecycle gate appropriate to task class/risk; they are not removed from governance.
- Recommended steps MAY be adjusted. Normative constraints, authority boundaries, required reviews and acceptance gates MUST NOT be weakened by a prompt.
- Prompt SHA-256 is the digest of the exact immutable executed prompt snapshot. Store it in the Work Item manifest/evidence bundle; do not create a self-referential hash field inside the bytes being hashed.

- **P0 为必需最低证据：** 准确执行的 Prompt ID/版本及其 SHA-256 MUST 记录在不可变 Work Item 证据包/Manifest 中；同时记录 Base SHA、实现 Commit SHA、最终分支 Head SHA、变更文件清单、读回结果、验收结论和载体 Closeout。不得伪造缺失的摘要或标识。
- **P1 在适用时提供：** 记录准确命令、环境、测试 Commit SHA、预期/实际结果和证据链接。未运行的检查 MUST 标记 NOT RUN 并说明原因；不适用的检查 MUST 标记 NOT APPLICABLE 并说明原因。
- P0/P1 分类 MUST NOT 豁免本规范、GOV-DOC-001、Owner 契约或其他治理规范要求的测试、安全、专业审查、双语、R2/R3、验收或发布门禁。尤其是 R3，在验收前仍须完成独立安全/领域专业审查和可复现测试证据。
- 安全、故障、并发、恢复、隐私和兼容性分析不必在任务尚未明确时提前穷尽，但 MUST 在任务类别/风险等级对应的生命周期门禁识别并处理；这些要求没有从治理中删除。
- 推荐步骤 MAY 根据实际情况调整。规范约束、权限边界、必需审查和验收门禁 MUST NOT 因提示词简化而弱化。
- Prompt SHA-256 是对准确、不可变的已执行提示词快照计算的摘要，应存入 Work Item Manifest/证据包；不得在被哈希的字节内容中放入自引用摘要字段。

### 5.3 Backward compatibility and migration / 向后兼容与迁移

Existing v1 prompts remain valid and MUST remain immutable after execution. They do not need retroactive rewriting. New prompts SHOULD use the seven-section template. Migrate an existing prompt only for a new authorized execution/version, preserve the old artifact and digest, and follow the mapping in `prompts/00-setup/MIGRATION-GUIDE.md`. A v2 prompt does not supersede an executed v1 prompt unless the accountable Owner explicitly authorizes the new version.

现有 v1 提示词继续有效，执行后 MUST 保持不可变，无须追溯重写。新提示词 SHOULD 使用七章节模板。只有在获准的新执行/新版本中才迁移旧提示词，并保留旧工件及摘要，遵循 `prompts/00-setup/MIGRATION-GUIDE.md` 的映射。除非责任 Owner 明确授权新版本，否则 v2 不取代已执行的 v1。

The seven-section layout does not replace mandatory preflight. Every AI session MUST continue to read `prompts/global-project-developer.md`, `prompts/global-bilingual-documentation.md`, GOV-DOC-001, this standard, and the applicable Owner prompt. Architecture-significant changes MUST retain Chinese/English counterparts, reciprocal links and parity evidence in the same change set, subject only to a formally approved, time-bounded STALE exception.

七章节结构不替代强制前置载入。每个 AI 会话 MUST 继续阅读 `prompts/global-project-developer.md`、`prompts/global-bilingual-documentation.md`、GOV-DOC-001、本规范和适用的 Owner 提示词。架构语义变更 MUST 在同一变更集中保留中英文对应版本、双向链接和一致性证据，除非正式批准有期限的 STALE 例外。

### 5.4 Simplification principles / 简化原则

- **Metadata consolidation:** group task identity and repository context; keep exact source/dependency revisions in the context section.
- **Tiered evidence:** distinguish mandatory P0 traceability from applicable P1 verification without weakening required tests.
- **Mandatory vs recommended:** normative constraints remain mandatory; suggested implementation sequence is adaptable.
- **Lifecycle-appropriate analysis:** avoid speculative upfront detail while retaining all applicable security, failure, compatibility and recovery gates.
- **Separation of concerns:** bilingual execution is governed by GOV-DOC-001/GLB-DOC-001; it is referenced by the prompt and remains an acceptance obligation, not a redundant fifteenth heading.

- **元数据合并：** 集中记录任务身份和仓库上下文；源文件/依赖的准确版本仍记录在上下文章节。
- **证据分级：** 区分必需的 P0 可追溯性和适用的 P1 验证，不弱化任何必需测试。
- **强制与推荐分离：** 规范约束保持强制；建议实现顺序可按实际调整。
- **按生命周期分析：** 避免推测性前置细节，同时保留所有适用的安全、故障、兼容性和恢复门禁。
- **关注点分离：** 双语执行由 GOV-DOC-001/GLB-DOC-001 管理；提示词仍须引用并履行双语验收义务，但不再重复设置冗余的第十五个标题。

Prompts MUST be reviewed before execution. Prompt changes after execution starts MUST create a new version and record the reason and impact. The previous prompt version remains immutable and retrievable.

AI MUST NOT invent missing approvals, dependencies, test results, file paths, commits, or Owner decisions. If inputs conflict, stop at the affected boundary, document the conflict and request an authorized decision.

## 6. Branching and change discipline / 分支与变更纪律

- One work item SHOULD map to one dedicated branch or a clearly isolated branch segment.
- Suggested branch format: `ai/<work-item-id>/<owner>-<short-topic>`.
- Do not combine unrelated work items in one commit series.
- Module Owners modify only files within their ownership unless an explicit integration task authorizes a cross-cutting change.
- Cross-owner edits require notification, impact analysis and approval from the affected Owner.
- No direct push to protected integration branches unless repository policy explicitly permits it.
- No merge based only on an AI self-review.
- Each implementation commit SHOULD be small, reviewable and use a meaningful message.
- Generated code, schemas, migrations and lockfiles MUST be reviewed as source artifacts, not treated as harmless generated output.

## 7. Definition of Ready / Definition of Done

### Definition of Ready (DoR)

A task is READY only when:

- the outcome and non-goals are explicit;
- one accountable Owner is assigned;
- relevant architecture/contracts and base SHAs are identified;
- dependencies are available or explicitly accepted as assumptions;
- acceptance criteria are testable;
- security/data/compatibility impact is classified;
- the prompt is stored, versioned and reviewed;
- the prompt explicitly requires GOV-DOC-001 compliance and identifies the Chinese/English source/counterpart documents;
- no unresolved blocker makes safe work impossible.

### Definition of Done (DoD)

A task is DONE only when applicable conditions are satisfied:

- code/docs match the approved prompt and scope;
- formatting, lint, build and type checks pass where applicable;
- unit, integration, contract and regression tests pass at the required level;
- negative/failure-path tests cover critical invariants;
- security and permission checks are tested for relevant changes;
- migration/rollback/compatibility behavior is documented and tested where relevant;
- independent review findings are resolved or explicitly accepted as residual risk;
- Tier 1 Chinese and English normative counterparts are created/updated in the same change set; Tier 2 remains optional only within its approved allowlist, and Tier 3 remains Chinese-first subject to Owner confirmation;
- whenever architecture/contract behavior changes, the owning authoritative documentation MUST be updated in both languages regardless of a Tier 2/Tier 3 label, with a bilingual change manifest recording exact paths/source revision and semantic, identifier, decision-status and link parity;
- the reviewer explicitly checks bilingual parity wherever Tier 1 or the architecture-semantic gate applies; missing or materially divergent counterparts block DONE/ACCEPTED unless a formally approved time-bounded exception exists;
- commit SHA, test evidence, review report and final status are recorded;
- integration and acceptance authority have explicitly accepted the result.

If a check cannot run, record **NOT RUN** with reason. Never report it as PASS.

### 7.1 Tiered bilingual-documentation gate / 分层双语文档门禁

This gate is governed by bilingual-tiering-policy.md and its authorized per-file inventory (tier-mapping-proposal remains PROPOSAL until formally adopted). Classification MUST come from that inventory, not directory/name heuristics:

1. **Tier 1 — mandatory bilingual:** Chinese and English counterparts MUST be created or updated in the same change set. Tier 1 MUST NOT be downgraded by a script, ordinary Owner confirmation, or one-off task approval.
2. **Tier 2 — optional bilingual:** optionality applies only to explicitly allowlisted files. It NEVER waives the architecture-semantic gate below.
3. **Tier 3 — Chinese-first:** Chinese remains the default authoritative version. Creating or maintaining an English counterpart requires explicit confirmation from the responsible Owner; this does not waive the architecture-semantic gate.
4. **UNKNOWN / pending confirmation:** the implementer MUST stop classification-dependent disposition, report the path as UNKNOWN / NEEDS_CONFIRMATION, and obtain an authorized human decision. UNKNOWN MUST NOT be silently assigned to Tier 2 or Tier 3 and MUST NOT be reported as PASS.

**Architecture-semantic gate (applies regardless of tier):** Every task that may affect architecture meaning MUST include this gate, including architecture-only, implementation, test, security, storage, protocol, performance, migration and operations tasks. The implementer MUST check whether code or tests reveal a contract change; if so, it MUST stop treating the work as implementation-only and update the owning authoritative specification in both languages. A Tier 2 or Tier 3 label MUST NOT be used to avoid that update. A translation-only change MUST NOT silently change a decision. The independent reviewer MUST compare both language versions against the same source revision and record PASS/FAIL for meaning, stable identifiers, status, examples and links. If either required counterpart is missing, its source revision cannot be established, or the versions are materially inconsistent, record BLOCKED/NOT DONE and identify the accountable Owner and closure condition.

本门禁由 bilingual-tiering-policy.md 及其获授权的逐文件清单管理（tier-mapping-proposal 仍为正式采纳前的 PROPOSAL）。分类 MUST 来自该清单，不得依靠目录或文件名启发式推断：

1. **Tier 1 — 强制双语：** 中英文对应文件 MUST 在同一变更集中创建或更新。不得通过脚本、普通 Owner 确认或单次任务批准降低 Tier 1。
2. **Tier 2 — 可选双语：** 可选属性仅适用于明确列入白名单的文件，绝不豁免下述架构语义门禁。
3. **Tier 3 — 中文优先：** 中文仍是默认权威版本。创建或维护英文对应版本须由责任 Owner 明确确认；该确认不豁免架构语义门禁。
4. **UNKNOWN / 待确认：** 实施者 MUST 暂停依赖分类的处置，报告路径为 UNKNOWN / NEEDS_CONFIRMATION，并取得有权人员的人工决定。不得静默将 UNKNOWN 归入 Tier 2 或 Tier 3，也不得报告为 PASS。

**架构语义门禁（不受层级标签影响）：** 每项可能影响架构含义的任务都 MUST 执行本门禁，包括架构、实现、测试、安全、存储、协议、性能、迁移和运维任务。实现者 MUST 检查代码或测试是否揭示契约变化；若是，就 MUST 停止将工作视为纯实现，并同步更新所属权威规范的中英文版本。不得利用 Tier 2 或 Tier 3 标签规避该更新。纯翻译变更 MUST NOT 暗中改变决议。独立审查者 MUST 基于同一源版本比较两种语言，并记录含义、稳定标识、状态、示例和链接的 PASS/FAIL。任何必需对应版本缺失、无法确认源版本或存在实质不一致时，均须记录 BLOCKED/NOT DONE，并明确责任 Owner 和关闭条件。

## 8. Verification model / 验证模型

Use layered evidence:

1. Static checks: formatting, lint, type checks, schema validation, dependency/license checks.
2. Unit tests: local invariants and state transitions.
3. Component integration tests: persistence, queues, indexes, protocol adapters.
4. Contract/conformance tests: cross-owner compatibility and wire semantics.
5. Fault-injection tests: crashes, retries, duplicate messages, lost ACKs, reordering, stale epochs and recovery.
6. Security tests: authorization boundaries, scope isolation, untrusted memory and prompt injection.
7. Workload benchmarks: representative data, hardware, warm/cold conditions, latency, throughput and resource use.
8. End-to-end acceptance: user-visible system behavior and operational recovery.

A test result is valid only with test identity, code commit, environment, command/configuration, input fixture, expected result, actual result and outcome. A bilingual-documentation check is also evidence: record both file paths, source revision, parity dimensions checked, reviewer and outcome. Performance claims MUST include workload and hardware context. Security claims MUST identify tested threat model and coverage; passing tests do not prove absence of vulnerabilities.

## 9. Review and acceptance / 审查与验收

Independent review MUST evaluate at least:

- requirement coverage and scope discipline;
- domain correctness and ownership boundaries;
- API/schema/protocol compatibility;
- data integrity, transaction and concurrency behavior;
- failure handling, idempotency, replay and recovery;
- security, identity, authorization and isolation;
- tests, observability and maintainability;
- documentation and traceability;
- mandatory Chinese/English semantic parity under GOV-DOC-001.

Findings use:

- **BLOCKER:** unsafe, incorrect, or prevents integration;
- **P0:** critical invariant/security/data-integrity defect;
- **P1:** major contract or correctness gap;
- **P2:** important quality or maintainability issue;
- **P3:** minor improvement.

Review disposition: PASS, CONDITIONAL PASS, FAIL, or NOT REVIEWABLE. Every finding has an ID, evidence, owner, severity, status and closure condition. Conditional Pass MUST list restrictions and MUST NOT be presented as full acceptance.

## 10. Architecture and implementation status vocabulary

Use separate statuses; do not collapse them:

- **DECIDED:** approved normative contract.
- **CANDIDATE:** proposal awaiting approval.
- **OPEN:** unresolved question.
- **TO_VALIDATE:** requires experiment or implementation evidence.
- **IMPLEMENTED:** code exists at a named commit.
- **TESTED:** named checks executed with recorded results.
- **REVIEWED:** independent review completed.
- **ACCEPTED:** authorized acceptance recorded.
- **MERGED:** integrated into the named target branch.

A document existing does not mean a decision is approved. A passing unit test does not prove system-level correctness. A commit does not prove deployment or runtime behavior.

## 11. Change management and learning loop / 变更与反馈

When implementation reveals a contract defect:

1. stop or isolate the unsafe part;
2. open a finding/change request;
3. identify authoritative Owner(s);
4. revise the contract through a decision record;
5. version affected prompts;
6. update dependent tasks and compatibility tests;
7. resume only after required approvals.

At the end of each iteration, record: expected vs actual, escaped defects, prompt ambiguity, rework causes, test gaps, review effectiveness, cycle time and next process improvement. Improve templates and automation based on evidence; do not weaken gates merely to increase throughput.

## 12. Initial governance status / 初始治理状态

This document is a proposed baseline until explicitly approved by the project's governance authority. Existing A–I module authority remains unchanged. Adoption does not retroactively convert previous work into compliant work; prior artifacts may be mapped to this standard with clearly marked evidence gaps.

---

# Appendix A — Minimum task record

- Work Item ID:
- Title / Class / Risk:
- Sponsor:
- Accountable Owner:
- Implementing AI session:
- Independent Reviewer:
- Prompt ID / Version / SHA-256:
- Base branch / SHA:
- Dependency SHAs:
- Scope / Non-goals:
- Acceptance criteria:
- Test plan:
- Security and compatibility impact:
- Implementation commit(s):
- Verification evidence:
- Review report:
- Acceptance record:
- Final state:


## 13. Session delivery traceability / 会话交付可追溯性

Every substantive AI session MUST use a durable GitHub Issue or Pull Request as its work carrier. A chat transcript, local note, or unlinked commit is not a project delivery record. Prefer the existing owning Issue/PR; create a new carrier only for an independently reviewable work item. Do not create duplicate PRs for the same integration unit.

Before work starts, record the Work Item ID, owning Issue/PR, accountable Owner, intended branch/base, scope, dependencies, prompt ID/version/hash, risk class, and acceptance criteria. During multi-step work, update the carrier when a material decision, changed file/commit, verification result, blocker, dependency, or handoff occurs. Do not defer all evidence until closeout.

Every completed or blocked session MUST publish a closeout comment or linked report containing:
1. Session/prompt identifier, prompt version/hash, role and accountable Owner.
2. Work Item ID and links to the owning Issue and related PRs.
3. Exact repository, branch, base SHA, final Head SHA and changed paths.
4. Actual work performed and decisions, each labeled PROPOSED, ACCEPTED, REJECTED or UNRESOLVED with the decision authority.
5. Verification commands, environment, exact tested SHA, results and evidence links; list every required check not run and why.
6. Independent review and integration status; identify when a review is a same-author/delegated simulation rather than independent approval.
7. Dependencies, blockers, risks, follow-up Owner and objective closure condition.
8. Merge state; if merged, target branch, merge commit SHA and post-merge verification. Never infer merge or approval from PR closure alone.

The Integration Owner MUST maintain `14-ai-development/work-items/INDEX.md` as a session → Work Item → Issue/PR traceability index. Each active or completed substantive session has one row; related sessions and PRs link bidirectionally where practical. Missing carriers, missing closeouts, stale source pins, and unrecorded outcomes are delivery defects and remain OPEN until corrected. For blocked/no-change assigned work, record a concise BLOCKED or NO_CHANGE closeout rather than fabricating implementation.

Architecture decisions remain subject to their existing Owner/ADR authority. A session record, PR merge, delegated role simulation, or AI-generated conclusion does not itself approve another Owner's domain decision or close a technical gate.

每个产生实质工作的 AI 会话 MUST 使用 GitHub Issue 或 Pull Request 作为持久工作载体。聊天记录、本地笔记或未关联的 Commit 均不构成项目交付记录。优先复用现有归属 Issue/PR；只有形成独立可审查工作单元时才新建载体。同一集成单元不得重复创建 PR。

工作开始前，记录 Work Item ID、归属 Issue/PR、责任 Owner、目标分支与基线、范围、依赖、Prompt ID/版本/哈希、风险等级和验收标准。多步骤工作期间，一旦出现重要决策、文件/Commit 变化、验证结果、阻塞、依赖或交接，必须及时更新载体，不得把全部证据拖到最后。

每个完成或受阻的会话 MUST 发布 Closeout 评论或链接报告，包含：
1. 会话/提示词标识、提示词版本/哈希、角色和责任 Owner。
2. Work Item ID，以及归属 Issue 和相关 PR 链接。
3. 准确的仓库、分支、Base SHA、最终 Head SHA 和变更路径。
4. 实际工作和决策；每项标记 PROPOSED、ACCEPTED、REJECTED 或 UNRESOLVED，并注明决策权威。
5. 验证命令、环境、准确测试 SHA、结果和证据链接；逐项列出未运行的必需检查及原因。
6. 独立审查和集成状态；若审查属于同一作者或委派角色模拟，必须明确披露，不得冒充独立批准。
7. 依赖、阻塞、风险、后续 Owner 和客观关闭条件。
8. 合并状态；若已合并，记录目标分支、Merge Commit SHA 和合并后验证。不得仅凭 PR 关闭状态推断已合并或已批准。

Integration Owner MUST 维护 `14-ai-development/work-items/INDEX.md`，建立会话 → Work Item → Issue/PR 可追溯索引。每个进行中或已完成的实质会话均应有一行记录；相关会话和 PR 应尽可能双向链接。缺少载体、缺少 Closeout、来源 Pin 过期或结果未记录均属于交付缺陷，必须保持 OPEN 直至修复。对于受阻或无变更的已分配任务，应记录简明 BLOCKED 或 NO_CHANGE Closeout，不得伪造实现。

架构决策仍受既有 Owner/ADR 权限约束。会话记录、PR 合并、委派角色模拟或 AI 生成的结论，均不能自行批准其他 Owner 的领域决策或关闭技术 Gate。
