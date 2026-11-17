# ADR-RUN-006 — Branch Protection and Review Gates for Automation
# ADR-RUN-006 — 自动化分支保护与审查 Gate

- Status / 状态: PROPOSED — repository administrator action required / 提案中——需要仓库管理员操作
- Owners / 责任: A (integration), I (governance/security), repository administrator (settings), Testing/Quality (required checks)
- Risk / 风险: R3 for autonomous write-back or merge
- Related: Issue #26/#30; PR #27/#31–#33; AI-STD-001; AI-AUTO-001; ADR-RUN-002/005

## 1. Context / 背景

Automation must not bypass the same review, test and governance controls required of human contributors. A previous repository inspection reported main branch protection disabled; a later administrative read returned HTTP 403, so the current configuration is unverified. This ADR specifies the desired policy; it does not claim that settings have been changed.

自动化不得绕过人类贡献者同样需要遵守的审查、测试和治理控制。早期仓库检查报告 main 分支保护未启用；后续管理接口读取返回 HTTP 403，因此当前配置未核验。本 ADR 规定目标策略，不声称设置已修改。

## 2. Proposed default-branch rules / 默认分支规则提议

Repository administrator should configure a ruleset (preferred) or branch protection with:

- Require pull requests before merging.
- Require at least one approval from a reviewer other than the PR author; require two for R3/security/Forget/migration/recovery changes where feasible.
- Require CODEOWNER/domain Owner review for affected governed paths; I review for security/governance-sensitive paths.
- Dismiss stale approvals when new commits are pushed.
- Require approval of the most recent reviewable push by someone other than the pusher.
- Require all conversations resolved.
- Require selected CI checks on the latest head SHA (exact check names to be established by Testing/Quality).
- Require branch to be up to date before merge, or use merge queue with equivalent guarantees.
- Block force pushes and branch deletion.
- Restrict direct pushes to default branch; automation identities cannot bypass.
- Disable administrator bypass where feasible; any emergency bypass must be separately audited and approved.
- Restrict who can dismiss reviews and bypass rules.
- Use linear history if compatible with the repository workflow.

仓库管理员应配置 Ruleset（优先）或 Branch Protection：PR 合并、非作者审查批准、R3 尽可能双人审查、CODEOWNER/领域 Owner 和 I 审查、推送新 Commit 后撤销旧批准、最新 Push 需他人批准、所有讨论解决、最新 Head SHA 必需 CI、分支最新或 Merge Queue、禁止 Force Push/删除、禁止直接推默认分支、自动化身份不可绕过、限制管理员绕过和 Review Dismiss 权限，并在兼容时启用线性历史。

## 3. Required status checks / 必需状态检查

Testing/Quality must define stable, deterministic check names, at minimum:
- Markdown/link/language consistency and required bilingual documentation checks.
- Schema/contract validation for protocol and runtime artifacts.
- Unit/integration tests for affected components.
- Secret scanning and dependency/security scanning.
- Workflow policy validation (no untrusted PR execution on persistent self-hosted runner).
- Build/test evidence for implementation PRs.

Testing/Quality 负责定义稳定、确定的 Check Name，至少包括双语文档/链接一致性、Schema/Contract 校验、受影响组件测试、秘密/依赖安全扫描、Workflow 策略校验（不可信 PR 不得运行在持久 Self-hosted Runner）和实现 PR 构建/测试证据。

Checks must be bound to the exact PR head SHA. A successful check on a previous SHA does not satisfy the current PR head.

Check 必须绑定 PR 精确 Head SHA。旧 SHA 的成功 Check 不能满足当前 Head。

## 4. Automation identity restrictions / 自动化身份限制

- GitHub App bot may create branches and PRs only through the Publication Broker after authorization gates.
- Bot cannot approve its own PR, dismiss required reviews, change rulesets, modify workflow files or merge by default.
- Separate credentials/identities for read-only reconciliation and write publication where feasible.
- No administrator permission for runtime identities.
- No bypass permission for the persistent runner host account.
- Workflow dispatch and runner administration remain manual/admin-only until a separate ADR approves them.

- GitHub App Bot 只能在授权 Gate 后经 Publication Broker 创建分支/PR。
- Bot 默认不得批准自己的 PR、Dismiss 必需 Review、修改 Ruleset、修改 Workflow 文件或合并。
- 尽可能分离只读对账和写发布凭据/身份。
- Runtime 身份不授予管理员权限。
- 持久 Runner 主机账号不得拥有 Bypass 权限。
- 在单独 ADR 批准前，Workflow Dispatch 和 Runner 管理仍限人工/管理员。

## 5. Required evidence and verification / 必需证据与核验

Repository administrator must provide:
- ruleset/branch protection screenshot or API export with repository and branch identity;
- timestamp and administrator identity;
- required review count, CODEOWNER policy, stale approval policy and bypass list;
- exact required status-check contexts;
- test PR proving an unapproved change cannot merge;
- test PR proving a new commit invalidates stale approval as configured;
- test proving bot identity cannot bypass or merge;
- test proving force-push/direct push is rejected.

仓库管理员必须提供 Ruleset/Branch Protection 截图或 API 导出、仓库/分支身份、时间/管理员身份、Review 数、CODEOWNER、旧批准失效策略、Bypass 列表、精确 Check Context，并通过测试 PR 证明未批准不可合并、新 Commit 会按配置撤销旧批准、Bot 无法绕过/合并、Force Push/直接 Push 被拒绝。

## 6. Emergency procedure / 紧急程序

Emergency bypass is not a routine automation path. It requires named human authority, incident/ticket reference, reason, time limit, exact commit SHA and post-event independent review. The runtime itself cannot invoke or grant emergency bypass.

紧急绕过不是常规自动化路径。必须有具名人类授权、事件/工单编号、理由、时限、精确 Commit SHA 和事后独立审查。Runtime 自身不得调用或授予紧急绕过。

## 7. Acceptance tests / 验收测试

- BR-01 unapproved PR cannot merge.
- BR-02 PR author cannot satisfy own approval.
- BR-03 stale approval invalidated after new head commit.
- BR-04 required checks must pass on exact head SHA.
- BR-05 unresolved review conversations block merge.
- BR-06 automation identity cannot bypass.
- BR-07 force push and direct push are rejected.
- BR-08 CODEOWNER/I review requirements enforced on protected paths.
- BR-09 emergency bypass leaves auditable evidence.
- BR-10 administrator configuration is independently read back and verified.

## 8. Decision / 决议

**OPEN — administrator action required.** No autonomous write-back or merge is permitted until the active ruleset is independently verified and BR-01..BR-10 pass. The repository integration currently lacks permission to verify administrative ruleset state; the administrator must provide evidence.

**OPEN——需要管理员操作。** 当前 Ruleset 经独立核验且 BR-01..BR-10 通过前，不允许自主写回或合并。当前仓库集成无权核验管理级 Ruleset，必须由管理员提供证据。
