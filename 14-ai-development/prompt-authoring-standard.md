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

Every execution prompt MUST contain:

1. Identity: Work Item ID, Issue, prompt ID/version/hash, Owner and session role.
2. Objective: intended outcome and observable result.
3. Baseline: repo, branch, base SHA, source paths/blob SHAs, dependencies.
4. Authority: owned decisions, allowed actions, prohibited actions and approvers.
5. Scope: in-scope files/modules and explicit non-goals.
6. State of knowledge: DECIDED/CANDIDATE/OPEN/TO_VALIDATE facts.
7. Required steps: inspect → plan → change → verify → report.
8. Acceptance criteria: numbered, objective, independently checkable.
9. Verification: commands, fixtures, environment, expected/actual results.
10. Git workflow: branch, commits, PR target, review handoff and no-merge rule.
11. Stop/escalation conditions.
12. Evidence and final report schema.

For a scheduled prompt, additionally include:
- Owner key and automation ID;
- cadence and timezone;
- Issue/PR selection query and priority order;
- maximum work items/actions per run;
- duplicate-run/idempotency behavior;
- notification policy;
- behavior when no eligible work exists;
- capability/permission preflight;
- run record and escalation target.

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
- 跨 Owner 任务必须拆分责任边界；每个 Owner 只批准自己的领域。I 和 Testing/Quality 按安全风险和验证风险参与审查。
- 定时任务提示词还必须写明 Owner key、automation ID、频率、时区、Issue/PR 查询规则、每次运行的工作上限、幂等行为、无任务时的行为、权限预检和升级路径。
- SHA-256 对仓库中实际提交的提示词文件字节计算；UTF-8，不做换行、空白或 Unicode 归一化。记录文件路径、字节数、摘要、Blob SHA 和 Commit SHA。
- 任何影响目标、范围、授权、基线、验收、测试或定时行为的修改都必须产生新版本；已执行版本不可覆盖。
- 缺少来源、审批、权限、可验证条件或安全保障时，提示词不得进入 READY；AI 必须停止并报告阻塞，不能自行补造决议。
