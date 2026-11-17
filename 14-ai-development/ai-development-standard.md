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
10. **Mandatory bilingual practice for every AI developer.** Every AI developer/session MUST read GOV-DOC-001 before work, inspect both language counterparts, include bilingual deliverables in its prompt and plan, and keep Chinese/English architecture meaning synchronized in the same change set. The accountable Owner MUST enforce this on delegated agents. Missing or materially divergent counterparts make the architecture task NOT DONE, except for a formally approved, time-bounded STALE exception. Code comments and machine-generated artifacts may retain their natural technical language, but their architecture meaning MUST be explained bilingually.

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

### 4.1 Work item lifecycle

| State | Meaning | Exit evidence |
|---|---|---|
| PROPOSED | Outcome and motivation recorded | Sponsor and candidate Owner identified |
| ANALYZED | Scope, dependencies, risks and alternatives analyzed | Impact map and acceptance criteria |
| PROMPT_READY | Prompt reviewed and frozen for execution | Prompt ID/version/hash and base refs |
| READY | Dependencies and contracts sufficient to start | Owner accepts task; blockers explicit |
| IN_PROGRESS | AI implementation underway | Branch and progress record |
| IMPLEMENTED | Change submitted by Owner | Commit SHA, changed-file list, self-check |
| VERIFIED | Automated/manual checks executed | Commands, environment, logs/results |
| REVIEWED | Independent review completed | Review report and finding disposition |
| INTEGRATION_READY | Cross-module contracts compatible | Integration evidence and updated registry |
| ACCEPTED | Acceptance authority approves | Explicit acceptance record |
| MERGED | Approved change integrated | Merge commit and target branch |
| CLOSED | Traceability and follow-up complete | Work item index updated |

A task MUST NOT skip a required gate. “Implemented” is not “Verified”; “Verified” is not “Reviewed”; “Reviewed” is not “Accepted”; “Accepted” is not “Merged”.

### 4.2 Blocked and rejected states

Use **BLOCKED** when a required contract, decision, permission, dependency or environment is unavailable. Record the blocker owner and resolution condition.

Use **REJECTED** when the proposed approach is invalid or unacceptable. Preserve the prompt and review record; do not erase failed attempts.

## 5. Prompt engineering as controlled engineering / 提示词工程化

A task prompt is a versioned engineering artifact, not disposable chat text.

**Canonical storage location:** all reusable prompts MUST be stored in the repository-root `prompts/` directory before execution. Global prompts MUST be placed directly under `prompts/`; Owner-specific prompts MUST be placed only under `prompts/A/` through `prompts/I/`. Do not place Owner prompts at the root or duplicate global rules in Owner files. Cross-owner tasks combine the global prompts with the relevant Owner prompts. The exact prompt actually executed MUST be copied into its Work Item evidence bundle with Prompt ID, version and SHA-256. Executed prompt versions are immutable.

**规范存储位置：** 所有可复用提示词 MUST 在执行前存入仓库根目录的 `prompts/`。全局提示词 MUST 直接放在 `prompts/` 根目录；Owner 专属提示词 MUST 仅放在 `prompts/A/` 至 `prompts/I/` 对应目录中。不得将 Owner 提示词放在根目录，也不得在 Owner 文件中重复复制全局规则。跨 Owner 任务组合全局提示词和相关 Owner 提示词。实际执行的准确提示词 MUST 连同 Prompt ID、版本和 SHA-256 复制到 Work Item 证据包。已执行提示词版本不可修改。

Start from the [canonical Prompt Library](../prompts/README.md). Every AI session MUST read `prompts/global-project-developer.md` and `prompts/global-bilingual-documentation.md`, plus its assigned Owner prompt. Review sessions MUST also read `prompts/global-architecture-reviewer.md`.

Every prompt MUST include:

1. Work Item ID, prompt ID, version, status and task class/risk.
2. Objective and observable outcome.
3. Accountable Owner, implementer role and independent reviewer role.
4. Repository, branch, base commit SHA and relevant dependency SHAs.
5. Required source documents and exact paths.
6. Scope: allowed files/modules and explicit non-goals.
7. Normative constraints, invariants and authority boundaries.
8. Required design/implementation steps.
9. Acceptance criteria stated as observable conditions.
10. Test plan, exact commands where known, fixtures and expected results.
11. Security, failure, concurrency, recovery and compatibility considerations as applicable.
12. Required deliverables and report format.
13. Commit, read-back, branch-head and evidence requirements.
14. Stop conditions and escalation path for ambiguity or conflicting contracts.\n15. **Bilingual documentation manifest:** affected Chinese/English paths, source revision, counterpart status, stable identifier/status parity checks, cross-links, and the reviewer responsible for semantic parity.

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
- the prompt is stored, versioned and reviewed;\n- the prompt explicitly requires GOV-DOC-001 compliance and identifies the Chinese/English source/counterpart documents;
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
- both Chinese and English normative documentation are created/updated in the same change set whenever architecture/contract behavior changes;\n- a bilingual change manifest records exact paths/source revision and verifies semantic, identifier, decision-status and link parity;\n- the reviewer explicitly checks bilingual parity; missing or materially divergent counterparts block DONE/ACCEPTED unless a formally approved time-bounded exception exists;
- commit SHA, test evidence, review report and final status are recorded;
- integration and acceptance authority have explicitly accepted the result.

If a check cannot run, record **NOT RUN** with reason. Never report it as PASS.

### 7.1 Mandatory bilingual-documentation gate / 强制双语文档门禁\n\nEvery task that may affect architecture meaning MUST include this gate, including architecture-only, implementation, test, security, storage, protocol, performance, migration and operations tasks. The implementer MUST check whether code or tests reveal a contract change; if so, it MUST stop treating the work as implementation-only and update the owning specification in both languages. A translation-only change MUST NOT silently change a decision. The independent reviewer MUST compare both language versions against the same source revision and record PASS/FAIL for meaning, stable identifiers, status, examples and links. If either counterpart is missing or materially inconsistent, record BLOCKED/NOT DONE and identify the accountable Owner and closure condition.\n\n每项可能影响架构含义的任务都必须执行本门禁，包括架构、实现、测试、安全、存储、协议、性能、迁移和运维任务。实现者必须检查代码或测试是否揭示了契约变化；若是，就不得再把工作视为纯实现任务，而必须同步更新所属规范的中英文版本。纯翻译变更不得暗中改变决议。独立审查者必须基于同一源版本比较两种语言，并记录含义、稳定标识、状态、示例和链接的 PASS/FAIL。任何一方缺失或存在实质不一致时，必须记录 BLOCKED/NOT DONE，并明确责任 Owner 和关闭条件。\n\n## 8. Verification model / 验证模型

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
- documentation and traceability;\n- mandatory Chinese/English semantic parity under GOV-DOC-001.

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
