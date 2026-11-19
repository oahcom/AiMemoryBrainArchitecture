# AI Prompt Authoring Standard
# AI 提示词编写规范

**Document ID:** AI-PROMPT-STD-001  
**Version:** 1.0  
**Status:** PROPOSED  
**Parent:** AI-STD-001 / AI-AUTO-001

## 1. Purpose / 目的

A prompt is a controlled engineering instruction that defines what an AI session may do, what it must not do, and what evidence it must leave. Prompt quality is part of engineering quality.

提示词不是聊天建议，而是受控工程指令，必须定义 AI 可以做什么、不能做什么，以及必须留下什么证据。

## 2. Authoring principles / 编写原则

Every prompt MUST be:

1. **Traceable:** linked to Work Item, Issue, Owner, exact source refs and prompt version.
2. **Bounded:** explicit scope, non-goals, allowed paths, branch and forbidden actions.
3. **Authority-safe:** states which decisions the session owns and which require escalation.
4. **Evidence-driven:** defines observable acceptance criteria and reproducible verification.
5. **Dependency-aware:** lists exact upstream contract and branch SHAs; distinguishes DECIDED, CANDIDATE, OPEN and TO_VALIDATE.
6. **Failure-aware:** includes stop conditions for missing sources, stale base, conflicting contracts, permission errors, data-integrity risks and failed tests.
7. **Idempotent:** says how to detect prior commits, PRs, comments and repeated run effects.
8. **Reviewable:** short enough to audit, structured, with no contradictory or hidden instructions.
9. **Bilingual where normative:** architecture/contract prompts and outputs must preserve the project's Chinese/English documentation rule.
10. **Secret-safe:** no credentials, private keys, access tokens or sensitive production data.

## 3. Prompt authoring workflow / 编写流程

### Step 1 — Intake normalization

A converts the Issue into a structured work request:
- preserve user intent and constraints;
- separate requirement, assumption, proposal and decision;
- identify one accountable Owner;
- classify work class and risk;
- split cross-module work into child tasks;
- define measurable outcome and non-goals.

A MUST ask for clarification when an ambiguity changes safety, authority, data semantics or acceptance. It MUST NOT silently invent a requirement.

### Step 2 — Source and dependency pinning

The author records:
- repository and target branch;
- base commit SHA;
- source document paths and blob SHAs;
- upstream Owner branch/head SHAs;
- relevant Issue/PR numbers;
- contract/ADR status;
- expected output paths.

A prompt MUST distinguish exact approved sources from informative background. A branch name without a SHA is not a stable baseline.

### Step 3 — Authority and scope construction

The prompt MUST state:
- named Owner role and domain;
- accountable decision owner;
- allowed modifications;
- forbidden modifications;
- required consultations/approvals;
- whether the session may commit, open PRs, comment, merge or only report.

Default: an Owner may change its own domain files; cross-domain files require explicit authorization and affected Owner review. Merge/release/destructive actions are prohibited unless specifically authorized.

### Step 4 — Acceptance and verification design

Acceptance criteria MUST be testable and tied to evidence:
- exact artifact/path/schema/API/state transition;
- expected behavior and negative behavior;
- relevant tests and fixtures;
- crash/retry/replay/race cases for concurrency/persistence work;
- security/authorization/adversarial cases for security-sensitive work;
- migration/rollback and compatibility cases where applicable;
- environment/workload for performance claims.

Avoid subjective criteria such as “robust”, “best”, “complete” unless decomposed into observable checks.

### Step 5 — Stop and escalation rules

Every prompt MUST say to stop before unsafe action if:
- a required source/branch/commit is unavailable or changed;
- an authoritative decision is missing or conflicting;
- scope or permission is insufficient;
- another Owner's decision is required;
- a test reveals data loss, unauthorized access, stale Forget exposure or protocol ambiguity;
- unexpected files, migrations or generated changes appear;
- the task would require bypassing CI, review or merge protection.

The session must report exact blocker, evidence, decision owner and safe next step.

### Step 6 — Prompt review and approval

A is the default prompt author/editor for cross-owner work. The accountable Owner MUST review and approve the prompt's domain semantics, scope and acceptance criteria before READY.

For multi-owner work, each affected Owner approves only its own boundary. I reviews prompts for SEC/R3, identity, authorization, privacy, Forget, retention and threat-model impact. Testing/Quality reviews testability and required evidence for R2/R3. A records unresolved dissent; it does not manufacture consensus.

For A-owned work, A MUST NOT be sole author and approver. The Sponsor or a delegated independent author drafts; a separate reviewer checks it; affected Owners approve their domain boundaries.

Prompt approval is not implementation approval, review approval or merge approval.

## 4. Mandatory prompt structure / 强制结构

Every execution prompt MUST use exactly the seven mandatory top-level sections defined by AI-STD-001 §5.1. This is a structural rule only: all twelve mandatory content elements below remain mandatory and MUST be placed inside the seven sections. Do not create twelve additional top-level headings.

每份执行提示词 MUST 使用 AI-STD-001 §5.1 规定的七个强制顶层章节。这只是结构规则：以下十二项强制内容要素全部保留，且 MUST 放入七个章节中。不得另行创建十二个顶层章节。

| # | Mandatory content element / 强制内容要素 | Placement / 放置章节 |
|---|---|---|
| 1 | Identity: Work Item ID, Issue, Prompt ID/version/hash, Owner and session role / 身份标识 | 1. Task identity / 任务标识 |
| 2 | Objective: intended outcome and observable result / 目标与可观测结果 | 2. Goal and boundaries / 目标与边界 |
| 3 | Baseline: repo, branch, base SHA, source paths/blob SHAs, dependencies / 基线与来源 | 3. Context and dependencies / 上下文与依赖 |
| 4 | Authority: owned decisions, allowed/prohibited actions and approvers / 权限与审批 | 4. Constraints and execution guidance / 约束与执行指导 |
| 5 | Scope: in-scope files/modules and explicit non-goals / 范围与非目标 | 2. Goal and boundaries; 4. Constraints / 目标与边界；约束与执行指导 |
| 6 | State of knowledge: DECIDED/CANDIDATE/OPEN/TO_VALIDATE / 知识状态 | 3. Context and dependencies / 上下文与依赖 |
| 7 | Required steps: inspect → plan → change → verify → report / 必需步骤 | 4. Constraints and execution guidance / 约束与执行指导 |
| 8 | Acceptance criteria: numbered, objective, independently checkable / 验收标准 | 5. Acceptance and deliverables / 验收与交付物 |
| 9 | Verification: commands, fixtures, environment, expected/actual results / 验证方法与结果 | 6. Evidence and review / 证据与审查 |
| 10 | Git workflow: branch, commits, PR target, review handoff and no-merge rule / Git 工作流 | 1. Task identity; 6. Evidence and review; 7. Stop conditions and coordination / 任务标识；证据与审查；停止条件与协调 |
| 11 | Stop/escalation conditions / 停止与升级条件 | 7. Stop conditions and coordination / 停止条件与协调 |
| 12 | Evidence and final report schema / 证据与最终报告格式 | 6. Evidence and review / 证据与审查 |

For scheduled prompts, these additional fields remain mandatory in the relevant seven-section locations: Owner key and automation ID; cadence and timezone; Issue/PR selection query and priority order; maximum work items/actions per run; duplicate-run/idempotency behavior; notification policy; behavior when no eligible work exists; capability/permission preflight; and run record/escalation target.

定时提示词还必须在七章节相应位置保留以下附加字段：Owner key 和 automation ID、频率及时区、Issue/PR 选择查询与优先级、每次运行最大工作项/操作数、重复运行/幂等行为、通知策略、无符合条件任务时的行为、能力/权限预检，以及运行记录和升级目标。

## 5. Versioning and hashing / 版本与哈希

- Store exact approved prompt bytes in a versioned repository file.
- SHA-256 is calculated over the exact committed file bytes, with UTF-8 encoding and no implicit newline, whitespace, Unicode or line-ending normalization.
- Record path, byte length, digest, blob SHA, commit SHA and execution reference.
- Any change to objective, scope, authority, source baseline, acceptance, verification, stop conditions or scheduled behavior creates a new prompt version.
- Run-specific clarifications/addenda are separately stored and hashed; if they materially alter instructions, create a new prompt version before proceeding.
- Executed prompt versions are immutable.
- Do not hash rendered chat text and claim it is the repository prompt digest.
- If the digest cannot be computed or verified, record NOT_VERIFIED and do not claim prompt integrity.

## 6. Prompt quality review checklist / 质量检查清单

A prompt is PROMPT_READY only if all applicable checks pass:

- [ ] One accountable Owner is named.
- [ ] The target outcome is observable.
- [ ] Exact base/source SHAs are recorded.
- [ ] DECIDED and unresolved contracts are separated.
- [ ] Allowed paths/actions and non-goals are explicit.
- [ ] Domain authority and required approvals are explicit.
- [ ] Acceptance criteria are objectively verifiable.
- [ ] Required positive, negative and failure-path tests are specified.
- [ ] Security/privacy/data impact is addressed.
- [ ] Stop conditions and escalation owner are named.
- [ ] Git branch/commit/PR/evidence steps are explicit.
- [ ] Idempotency and repeated execution behavior are defined.
- [ ] Hash and immutable version record are present.
- [ ] Required Owner/specialist approvals are recorded.

Any failed mandatory item keeps the Work Item out of READY.

## 7. Anti-patterns / 禁止模式

MUST NOT:
- use “do everything necessary” without scope and action limits;
- ask an AI to approve its own implementation or prompt;
- treat a role-played panel as independent reviewers;
- direct an Owner to override another Owner's domain decision;
- rely on a floating branch name or “latest” without pinning SHA;
- mix multiple unrelated Work Items in one prompt;
- bury critical constraints in long background context;
- use vague acceptance criteria;
- permit unreviewed changes to prompt instructions mid-run;
- ask scheduled tasks to repeatedly re-open completed or rejected work;
- instruct a scheduled task to merge, release or perform destructive action by default;
- claim that a prompt hash proves the AI followed the prompt.

## 8. Status model / 状态模型

`DRAFT → REVIEWED → APPROVED_FOR_EXECUTION → EXECUTED → SUPERSEDED`

A prompt may be REJECTED or BLOCKED at any stage. Prompt approval is scoped to a specific Work Item, Owner, baseline and prompt version. A changed baseline or material requirement may invalidate the approval.

## 9. Initial status / 初始状态

This document is PROPOSED and becomes normative only after the project's governance approval process. It does not retroactively validate earlier prompts or scheduled runs.

## 10. 中文规范要点 / Chinese normative summary

- 提示词是受控工程指令，不是临时聊天内容。每份提示词必须关联 Work Item、Issue、Owner、版本、哈希、基线 SHA 和验收标准。
- A 默认负责跨模块任务提示词的起草和维护，但不因此获得其他 Owner 的领域决策权。领域 Owner 必须在任务进入 READY 前批准本领域语义、范围和验收条件。
- A 自己负责实现的任务，提示词必须由 Sponsor 或独立受托者起草，并由独立审查者审核；A 不能自编自批。
- 每个提示词必须明确目标、输入源、授权边界、允许/禁止修改路径、依赖状态、可验证验收条件、测试要求、停止条件、Git/PR 流程和证据格式。
- 执行提示词的强制顶层结构为七章节（与 AI-STD-001 §5.1 一致）；十二项强制内容要素全部保留，并按本规范 §4 映射到七章节，不得另建十二个顶层章节。定时提示词的附加调度字段仍然强制。
- 跨 Owner 任务必须拆分责任边界；每个 Owner 只批准自己的领域。I 和 Testing/Quality 按安全风险和验证风险参与审查。
- 定时任务提示词还必须写明 Owner key、automation ID、频率、时区、Issue/PR 查询规则、每次运行的工作上限、幂等行为、无任务时的行为、权限预检和升级路径。
- SHA-256 对仓库中实际提交的提示词文件字节计算；UTF-8，不做换行、空白或 Unicode 归一化。记录文件路径、字节数、摘要、Blob SHA 和 Commit SHA。
- 任何影响目标、范围、授权、基线、验收、测试或定时行为的修改都必须产生新版本；已执行版本不可覆盖。
- 缺少来源、审批、权限、可验证条件或安全保障时，提示词不得进入 READY；AI 必须停止并报告阻塞，不能自行补造决议。
