# ADR-RUN-005 — Prompt Approval and Runtime Authorization
# ADR-RUN-005 — Prompt 批准与 Runtime 授权

- Status / 状态: PROPOSED — decision pending / 提案中——待决议
- Owners / 责任: A (cross-owner coordination), each Accountable Owner (domain approval), I (security), Project Governance Authority (policy approval)
- Risk / 风险: R2 read-only pilot; R3 code execution, write-back, security, migration, recovery or destructive work
- Related: AI-STD-001; AI-PROC-001; AI-TPL-001; AI-PROMPT-STD-001; AI-AUTO-001; ADR-RUN-002/003

## 1. Principle / 原则

A prompt is a versioned engineering instruction, not an authorization credential. A valid prompt digest proves which bytes were selected; it does not prove that the author was entitled to approve those bytes or that the runtime may perform every requested action.

Prompt 是版本化工程指令，不是授权凭据。Prompt Digest 只能证明选中了哪些字节，不能证明作者有权批准这些字节，也不能证明 Runtime 可执行其中所有动作。

Runtime authorization is a separate, machine-enforced decision bound to repository, work item, Owner, risk, prompt digest, base revision, allowed paths/tools, budget and approval evidence.

Runtime 授权是独立、由机器强制执行的决策，绑定仓库、Work Item、Owner、风险、Prompt Digest、Base Revision、允许路径/工具、预算和批准证据。

## 2. Required approval roles / 必需批准角色

| Work class / 工作类型 | Prompt author / 起草 | Domain approval / 领域批准 | Security approval / 安全批准 | Final acceptance / 最终验收 |
|---|---|---|---|---|
| Single-owner ARCH/DOC | A or delegated author | Accountable Owner | I if R2/R3 security impact | Independent reviewer + integration acceptance as applicable |
| Cross-owner contract | A | Every affected Owner for own semantics | I for identity/security/Forget | A integration decision after independent review |
| IMPL/TEST | A or delegated author | Implementing Owner | I for R2/R3 | Independent reviewer + test evidence |
| SEC/Forget/MIG/recovery | Independent author; A coordinates | Relevant Owners | I + specialist review | Explicit governance authority for residual R3 risk |
| A-owned implementation | Sponsor/independent delegate | A domain Owner cannot self-approve | I as risk requires | Independent reviewer and designated acceptance authority |
| Project governance policy | A drafts | A–I affected Owners review | I mandatory | Project Governance Authority |

Prompt 作者与批准者必须按表分离。A 不能替代领域 Owner 批准；A 负责的实现任务不得由 A 自编自批；R3 残余风险必须由明确治理权威接受。

## 3. Immutable prompt binding / 不可变 Prompt 绑定

Each approved prompt record contains:
- work item ID, prompt ID and semantic version;
- repository path and exact UTF-8 byte length;
- SHA-256 over exact committed file bytes (no newline, whitespace, Unicode or line-ending normalization);
- Git blob SHA and source commit SHA;
- Owner approval identity, approval timestamp and approved digest;
- risk class, scope, non-goals, allowed paths/tools, acceptance criteria and stop conditions;
- required reviewers and dependency SHAs;
- expiry/review trigger (e.g. base SHA change, policy epoch change, permission change or material scope edit).

每个批准 Prompt 记录 Work Item ID、Prompt ID/语义版本、路径、精确 UTF-8 字节长度、原始 Commit 文件字节 SHA-256（不做任何规范化）、Git Blob SHA/来源 Commit SHA、Owner 批准身份/时间/摘要、风险、范围、非目标、允许路径/工具、验收、停止条件、审查者/依赖 SHA 和失效条件。

Any byte change creates a new prompt digest and requires approval again. Runtime must fetch the exact blob/commit, recompute digest and compare against the approved record before execution.

任意字节变化都会生成新 Prompt Digest，必须重新批准。Runtime 执行前必须获取精确 Blob/Commit，重新计算 Digest 并与批准记录比较。

## 4. Runtime capability envelope / Runtime 能力信封

An execution authorization is a short-lived capability envelope containing:

`authorization_id, repository_id, work_item_id, owner_id, risk_class, prompt_digest, base_sha, policy_epoch, allowed_paths, allowed_commands, network_policy, resource_budget, expires_at, approval_refs`

It is issued by the trusted Coordinator after eligibility checks and consumed by the isolated worker launcher. It is not a bearer secret that grants unrestricted GitHub API access.

执行授权是短期 Capability Envelope，包含上述字段，由可信 Coordinator 在资格检查后签发，并由隔离 Worker Launcher 消费。它不是可授予无限制 GitHub API 访问的 Bearer Secret。

The envelope must be integrity-protected, audience-bound to one worker/run, time-bounded, revocable and single-use or replay-safe. Worker cannot expand paths, commands, network destinations, budgets or expiry. The Publication Broker independently rechecks authorization and fencing before side effects.

Envelope 必须具备完整性保护、绑定单一 Worker/Run Audience、有时限、可撤销且单次使用或具备重放安全。Worker 不得扩大路径、命令、网络目标、预算或有效期。Publication Broker 在副作用前独立复核授权与 fencing。

## 5. Eligibility gates / 资格 Gate

Before execution, coordinator verifies:
1. Issue/PR remains open and matches the work objective.
2. Repository ID and allowed branch match the approved repository scope.
3. Target revision equals the pinned expected SHA.
4. Dependencies are satisfied by evidence bound to exact revisions.
5. Prompt digest and Owner approvals are current.
6. Required I/security and independent reviews exist for the risk class.
7. No blocking finding, stop flag, emergency stop or expired authorization exists.
8. Work class, paths, commands, network and resource budget are within policy.
9. Concurrency/lease constraints allow a new run.
10. Current branch protection/ruleset evidence meets policy for any write-capable task.

执行前必须验证 Issue/PR 状态、仓库/分支范围、目标 SHA、精确修订依赖证据、Prompt Digest/Owner 批准、风险要求的 I/独立审查、阻塞 Finding/停止标志、Work Class/路径/命令/网络/预算、并发租约及写任务的分支保护证据。

## 6. Revocation and invalidation / 撤销与失效

Revoke or invalidate authorization on:
- prompt byte change or approval withdrawal;
- Owner assignment/authority change;
- target SHA change or PR closed/merged;
- permission/ruleset/policy epoch change;
- lease expiry, reassignment or fencing-token increment;
- emergency stop, security incident or budget exhaustion;
- dependency evidence withdrawn or superseded.

Prompt 字节变化/撤回批准、Owner 权限变化、目标 SHA 变化/PR 关闭或合并、权限/Ruleset/Policy Epoch 变化、租约过期/重新分配/fencing 递增、紧急停止/安全事件/预算耗尽、依赖证据撤回或过期时，必须撤销或使授权失效。

## 7. Audit / 审计

Record authorization decision ID, policy version, prompt digest, approver identities, source SHAs, allowed capability summary, issue/reason codes, worker/run ID, lease/fencing token and expiry. Never log bearer tokens, private keys, full secret-bearing environment or unnecessary user content.

记录授权决策 ID、策略版本、Prompt Digest、批准身份、源 SHA、能力摘要、理由码、Worker/Run ID、Lease/Fencing Token 和过期时间。不得记录 Bearer Token、私钥、含秘密的完整环境或无关用户内容。

## 8. Acceptance tests / 验收测试

- AUTH-01 prompt byte change invalidates approval.
- AUTH-02 wrong blob/commit SHA is rejected.
- AUTH-03 missing domain Owner approval blocks execution.
- AUTH-04 A cannot self-approve A-owned implementation.
- AUTH-05 R3 work without I/security approval is blocked.
- AUTH-06 base SHA change invalidates capability.
- AUTH-07 policy epoch change invalidates capability.
- AUTH-08 expired/revoked capability is rejected.
- AUTH-09 worker cannot expand allowed paths/commands/network/budget.
- AUTH-10 worker cannot use authorization for another run/repository.
- AUTH-11 stale fencing token blocks publication.
- AUTH-12 missing branch protection evidence blocks write-capable task.
- AUTH-13 approval withdrawal stops queued work and cancels active work safely.
- AUTH-14 audit record contains evidence references but no secret values.

测试覆盖 Prompt 字节变化、Blob/Commit SHA、Owner/I 批准、A 自批限制、R3 安全审批、Base SHA/Policy Epoch、授权过期撤销、能力扩张、跨 Run/仓库重用、旧 fencing、分支保护证据、批准撤回和审计脱敏。

## 9. Decision / 决议

**OPEN.** This ADR operationalizes AI-PROMPT-STD-001 and AI-AUTO-001 but does not supersede them. A, I and affected Owners must approve the capability schema and enforcement points before code implementation. Until then, the runtime may only perform manually authorized read-only diagnostics.

**OPEN。** 本 ADR 将 AI-PROMPT-STD-001 与 AI-AUTO-001 操作化，但不取代它们。实现前 A、I 和相关 Owner 必须批准 Capability Schema 与强制点。在此之前 Runtime 只能执行人工授权的只读诊断。
