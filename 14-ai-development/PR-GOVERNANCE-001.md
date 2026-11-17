# PR-GOVERNANCE-001 — Pull Request Governance, Consolidation & Immediate Integration Standard
# PR 治理、反堆积与验证即合入规范

- Document ID: PR-GOVERNANCE-001
- Version: 1.0
- Status: ADOPTED — owner-directed adoption recorded in Issue #130 comment #6962523529 after PR #144 merged on 2026-11-18
- Owner: Integration Owner; repository configuration remains the repository administrator's responsibility
- Tracking: Issue #130
- Related P0: Issue #134
- Adoption record: Issue #130 comment #6962523529; PR #144 merge commit `3754d049db840b049728afd814faac968bf10749`

## 1. Purpose and governing rule / 目的与治理原则

A PR is an integration unit, not a work diary or a substitute for an Issue. Every material AI session must publish its actual work, findings, decisions, verification and blockers to an existing GitHub Issue/PR. Reuse the existing carrier whenever possible. Create a new PR only for a distinct, reviewable integration unit; consolidate duplicate or overlapping changes rather than accumulating PRs.

PR 是集成单元，不是工作流水账，也不能替代 Issue。每个产生实质工作的 AI 会话都必须将实际工作、发现、决策、验证和阻塞发布到现有 GitHub Issue/PR。优先复用已有载体；只有独立且可审查的集成单元才创建新 PR。重复或重叠的变更必须合并整理，禁止堆积 PR。

A merged PR proves repository integration only. It does not, by itself, prove domain-owner acceptance, security approval, production readiness, architecture freeze or deployment success.

PR 合并只证明代码/文档已集成到目标分支，本身不证明领域 Owner 验收、安全批准、生产就绪、架构冻结或部署成功。

## 2. Required session delivery record / 会话交付记录

Every session performing development, research, review, defect analysis, verification or producing a technical/architecture conclusion MUST update its owning Issue/PR during the work and publish a closeout record containing:

1. Session ID, prompt ID/version/hash, role and accountable Owner.
2. Work Item/Issue and related PR numbers; use existing carriers where possible.
3. Exact repository, branch, base SHA, Head SHA and changed paths.
4. Actual work performed; distinguish authored work from review or delegated simulation.
5. Findings and decisions classified as PROPOSED, ACCEPTED, REJECTED, OPEN or BLOCKED, with decision authority and source pins.
6. Verification commands, environment, exact tested SHA, run links and results; enumerate NOT RUN checks with reasons.
7. Independent review identity and review state; disclose same-author/delegated review.
8. Dependencies, risks, blockers, handoff Owner and closure condition.
9. Merge state; if merged, target branch, actual merge commit SHA and post-merge readback.

未产生实质变更的已分配任务也必须记录 NO-CHANGE 或 BLOCKED 结果。聊天记录不能作为唯一交付物。

Assigned sessions with no material change must still record NO-CHANGE or BLOCKED. Chat history is never the sole project artifact.

## 3. PR admission and consolidation / PR 准入与合并整理

Before creating a PR, search for an existing PR/Issue for the same Work Item and integration unit. Prefer updating that carrier. A new PR must state its unique deliverable, owner, scope, dependencies and why it cannot be folded into an existing PR.

创建 PR 前，必须搜索相同 Work Item 和集成单元的现有 PR/Issue，优先更新已有载体。新 PR 必须说明其独立交付物、Owner、范围、依赖，以及不能并入现有 PR 的原因。

Do not create a PR solely to restate an already merged conclusion. Do not split one coherent change into multiple PRs merely to obtain separate activity records. Separate PRs are justified only when ownership, release order, risk boundary or independently verifiable acceptance requires it.

不得仅为重复已合并结论而创建 PR；不得为了制造活动记录而把一个完整变更拆成多个 PR。只有 Owner、发布顺序、风险边界或可独立验收要求确实不同，才允许拆分 PR。

For PRs targeting a non-main Owner/research/recovery branch, preserve that base branch and its dependency chain. Do not silently retarget or merge such a PR to main. Mainline publication requires an explicit integration PR with exact source pins and authority boundaries.

目标为非 main Owner/研究/恢复分支的 PR，必须保留其目标分支和依赖链。不得擅自改为 main 或直接合入 main。发布到主线必须另建明确的集成 PR，并记录准确源版本和权威边界。

## 4. Exact-Head verification gate / 精确 Head 验证门禁

A PR is merge-eligible only when all applicable checks and reviews refer to its current exact Head SHA. Before merge, the Integration Owner MUST refresh and record:

- PR state, base branch and current base SHA.
- Exact current Head SHA and mergeability/conflict state.
- Every applicable required check name, conclusion and workflow/run URL for that exact Head.
- Independent review/approval required by risk and ownership; approval must apply to the current Head.
- Unresolved review conversations and material findings.
- Bilingual manifest/parity result where GOV-DOC-001 applies.
- Dependency PRs and their actual merge states.

PR 只有在所有适用检查和审查均针对当前准确 Head SHA 时才具备合并资格。合并前，集成 Owner 必须刷新并记录：PR 状态、目标分支及 Base SHA、当前 Head SHA、冲突/可合并状态、针对该 Head 的检查名称/结论/运行链接、按风险和 Owner 要求取得的独立审批、未解决讨论、双语清单/一致性结果及依赖 PR 的真实合并状态。

A check on an earlier Head, a green check on another PR, a branch-level success unrelated to the current Head, or a locally asserted result is not a substitute. A missing, pending, skipped or failed applicable check is NOT PASS. If a new commit changes the Head, the evidence must be refreshed.

旧 Head 的检查、其他 PR 的绿色检查、与当前 Head 无关的分支成功状态或本地口头声明均不可替代。缺失、待定、跳过或失败的适用检查均不算 PASS。Head 一旦变化，必须重新取得证据。

## 5. Independent review and Owner authority / 独立审查与 Owner 权威

For changes affecting security, identity, authorization, Forget, lifecycle, canonical persistence, recovery, cross-owner contracts or production operations, require a reviewer independent of the author and the implementing session. Obtain explicit approval from each affected authority Owner when the change modifies or accepts that Owner's normative contract.

涉及安全、身份、授权、Forget、生命周期、规范持久化、恢复、跨 Owner 契约或生产运维的变更，必须由独立于作者和实现会话的审查者审查。若变更修改或验收某 Owner 的规范契约，必须取得对应 Owner 的明确批准。

A COMMENT review is technical commentary, not an APPROVE review. A review performed through the same connected GitHub identity as the author is not independent, even if the session adopts a different role. AI role simulation is not Owner approval. Record exceptions explicitly; do not silently waive the requirement.

COMMENT 是技术评论，不是 APPROVE。作者与审查者使用同一 GitHub 身份时，不构成独立审查，即使会话扮演不同角色也一样。AI 角色模拟不构成 Owner 批准。任何例外都必须显式记录，不得默默豁免。

## 6. Merge decision and immediate integration / 合并决策与及时集成

Use exactly one of these dispositions:

- MERGE: exact-Head checks passed, required independent approvals exist, no unresolved blocking finding, dependencies are satisfied, and the PR is mergeable.
- HOLD: evidence/check/review/dependency is missing or pending; identify the exact missing item and owner.
- REMEDIATE: a concrete defect exists; update the same PR where scope remains coherent, otherwise create one linked follow-up Work Item.
- SUPERSEDED: another merged artifact fully replaces this PR; cite the replacement and preserve unique evidence before closing unmerged.
- REJECT: the proposal is invalid or conflicts with accepted authority; record the rationale.

只允许使用以下处置状态：

- MERGE：精确 Head 检查通过、必需独立审批齐全、无未解决阻断发现、依赖满足且 PR 可合并。
- HOLD：证据/检查/审查/依赖缺失或待定；必须指出具体缺项和责任人。
- REMEDIATE：存在明确缺陷；范围一致时在原 PR 修复，否则创建一个关联的后续 Work Item。
- SUPERSEDED：另一已合并产物完整替代本 PR；关闭未合并 PR 前必须引用替代项并保留独有证据。
- REJECT：提案无效或与已接受权威冲突；记录理由。

Once a PR meets MERGE criteria, integrate it promptly; do not leave verified, independent, conflict-free work idle merely to accumulate more review cycles. Use the repository's permitted merge method and an expected Head SHA. After merge, read back the target branch and record the actual merge commit SHA.

PR 满足 MERGE 条件后应及时合入，不得为了堆积审查轮次而搁置已验证、独立且无冲突的工作。使用仓库允许的合并方式并传入预期 Head SHA。合并后必须从目标分支回读，并记录真实 merge commit SHA。

## 7. Platform enforcement is separate from process policy / 平台强制执行与流程规范分离

This document defines the required process. It does NOT claim that GitHub enforces the process. Required status checks, required independent approvals, stale-review dismissal, conversation resolution, force-push/deletion restrictions and bypass controls are effective only when the repository has actually configured supported branch protection or rulesets and the live API confirms enforcement.

本文定义流程要求，但**不声称 GitHub 已经强制执行这些要求**。必需状态检查、独立审批、过期审批撤销、讨论解决、禁止强推/删除和绕过控制，只有在仓库实际配置了受支持的分支保护或 Rulesets，且实时 API 确认已启用时才有效。

If the current GitHub plan/visibility does not support required controls for this private repository, record the limitation as BLOCKED and escalate to the repository administrator to select a genuinely enforceable plan/configuration. Do not treat PR templates, workflow annotations, labels, comments or AI self-review as a hard merge gate. Do not make the repository public as a workaround without an explicit security/privacy decision.

如果当前 GitHub 套餐/可见性不支持该私有仓库所需的控制，必须记录为 BLOCKED，并升级给仓库管理员选择真正可强制执行的套餐/配置。PR 模板、Workflow 注释、Label、评论或 AI 自审均不得冒充硬合并门禁。未经明确安全/隐私决策，不得通过公开仓库来规避限制。

Issue #134 remains OPEN until the platform confirms enforcement and a deliberately failing required check is proven unable to merge through the normal path.

在平台确认强制执行、且故意失败的必需检查被证明无法通过正常路径合并之前，Issue #134 必须保持 OPEN。

## 8. Closeout and traceability / 结项与可追溯性

Every merged PR MUST leave a closeout record in its PR/Issue carrier and update the Work Items index when applicable. Closeout must distinguish repository merge from Owner acceptance, conformance, deployment and production readiness. Preserve failed historical checks and corrected claims; never rewrite history or relabel a failed run as passed.

每个已合并 PR 都必须在其 PR/Issue 载体中留下结项记录，并在适用时更新 Work Items 索引。结项必须区分仓库合并、Owner 验收、符合性、部署和生产就绪。保留历史失败检查和纠正记录；不得改写历史或将失败运行重新标记为通过。

## 9. Adoption and change control / 采用与变更控制

This standard remains PROPOSED until merged and Issue #130 explicitly records adoption. Platform enforcement remains separately tracked by Issue #134. Changes to this standard require a bilingual semantic-parity update and an exact-Head governance review.

本规范在合并且 Issue #130 明确记录采用之前保持 PROPOSED。平台强制执行由 Issue #134 单独跟踪。本规范的修改必须同步更新双语语义版本，并进行精确 Head 治理审查。
