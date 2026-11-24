---
document_metadata:
  domain: ai-development
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Approved
      approver: Integration Owner
      decision_date: "2026-11-23"
      approved_version:
        scheme: content-hash
        value: "41243e916e67c2704ab93f05f190e07f2015b3e546b50f6f778d7e5f0caa1cfe"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "Issue #130 comment #6962523529"
        - "PR #144 merge commit 3754d049db840b049728afd814faac968bf10749"
        - "PR #750 comment #7092567630 (owner-proxy ratification: §6.1 review disposition lock included in the approved scope)"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-24"
      last_verification_note: "v1.0 adoption is recorded in Issue #130 comment #6962523529. The §6.1 inclusion is recorded separately in PR #750 comment #7092567630, because the #130 comment predates §6.1 by six days and cannot carry it. This metadata does not assert that GitHub platform enforcement is enabled."
    usage_status: Active
    modification_status: Pending-Reapproval
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "Pull-request admission, exact-Head verification, independent review, merge dispositions, and integration into main in this repository."
    canonical_scope_id: ai-development/pr-governance-001
    canonical_scope_keywords:
      - pull-request-admission
      - exact-head-verification
      - independent-review
      - merge-disposition
      - main-branch-integration
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md"
    zh-CN: "docs/zh-CN/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md"
---
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

A pull request is mandatory **if and only if the merge target is `main`**, regardless of the source branch (Owner primary, child/work, research or recovery branch). Every change targeting `main` must enter through a PR and satisfy the applicable exact-Head checks and review gates.

A merge whose target is any non-`main` branch does **not** require a PR. This includes child/work → Owner primary, ordinary work → Owner primary, and Owner primary → another non-`main` branch. The responsible Owner may integrate directly after the required scope, test, evidence, safety and authority checks; record material results in the existing Work Item/Issue. Do not create a PR solely to represent an Owner-internal merge.

This exception must not be used to bypass the `main` PR gate indirectly. If the intended integration target is `main`, open a PR targeting `main` from the source branch and do not route the change through a non-`main` branch to evade review.

只有合并目标为 `main` 时才必须创建 PR，且不受来源分支类型限制（Owner 主分支、子/工作分支、研究分支或恢复分支均适用）。所有目标为 `main` 的变更都必须通过 PR 集成，并满足适用的精确 Head 检查和审查门禁。

合并目标为任何非 `main` 分支时，**不需要 PR**。包括子/工作分支 → Owner 主分支、普通工作分支 → Owner 主分支，以及 Owner 主分支 → 其他非 `main` 分支。责任 Owner 可在完成必要的范围、测试、证据、安全和权威检查后直接集成，并将重要结果记录到已有 Work Item/Issue。不得仅为表示 Owner 内部合并而创建 PR。

此例外不得用于间接绕过 `main` 的 PR 门禁。如果预期集成目标是 `main`，应从来源分支创建目标为 `main` 的 PR，不得先绕经非 `main` 分支规避审查。

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

A COMMENT review is technical commentary, not an APPROVE review. **Independence is a property of the reviewing session, not of the GitHub account that carries it.** A review is independent when it is performed by a session that did not author the change and did not implement it, and that reaches its conclusion from the artifacts rather than from the author's account of them. Separate sessions may share one GitHub identity; the identity is the carrier, and independence is decided by whether the context is shared, not by whether the account differs. Where the platform enforces required approvals, GitHub additionally forbids approving one's own pull request; that is a platform constraint on the carrier and does not raise the independence bar above the session level. **AI role simulation inside the authoring session is not independent review**, because the reviewer and the author share one context and one incentive; a separate session that does not share that context is. Record exceptions explicitly; do not silently waive the requirement.

COMMENT 是技术评论，不是 APPROVE。**独立性是审查会话的属性，不是承载它的 GitHub 账号的属性。** 当一次审查由未撰写、未实现该变更的会话执行，且其结论来自产物本身而非作者对产物的陈述时，该审查即为独立。多个会话可以共用一个 GitHub 身份；身份是载体，独立性由上下文是否共享决定，而不由账号是否相异决定。平台强制审批时，GitHub 另禁止批准自己的 PR；那是施加于载体的平台约束，不把独立性的门槛抬到会话之上。**在撰写会话内部做 AI 角色模拟不构成独立审查**，因为审查者与作者共享同一上下文与同一激励；不共享该上下文的另一会话构成独立审查。任何例外都必须显式记录，不得默默豁免。

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

### 6.1 Review disposition lock / 审查处置锁

A pull request MUST NOT be merged while any formal review is in `REQUEST_CHANGES` state, or while any material blocking review finding remains unresolved and unverified.

当任一正式审查处于 `REQUEST_CHANGES` 状态，或任一实质阻断性审查发现仍未解决且未验证时，PR **不得**合并。

When a formal `REQUEST_CHANGES` review or an authorized blocking disposition is recorded:

1. The PR disposition MUST become `HOLD`.
2. Every blocking finding MUST have an explicit recorded disposition.
3. A finding requiring correction MUST NOT be considered resolved merely because a new commit was pushed, a comment says "fixed", or CI passes.
4. Resolution MUST identify the corrective commit and relevant verification evidence on the current exact Head.
5. The reviewer MUST re-check the corrected exact Head and confirm resolution, unless the authorized acceptance authority explicitly records a permitted risk acceptance.
6. Immediately before merging, the merge authority MUST verify the current Head, review state, unresolved findings, required checks, and dependencies.

记录到正式 `REQUEST_CHANGES` 审查或经授权的阻断处置后：

1. PR 处置状态必须改为 `HOLD`。
2. 每一项阻断性发现必须有明确记录在案的处置。
3. 需要修正的发现，不得仅因推送了新提交、评论声称"已修复"或 CI 通过就视为已解决。
4. 解决记录必须指明修正提交，以及在**当前精确 Head** 上的相关验证证据。
5. 审查方必须复核修正后的精确 Head 并确认解决；除非经授权的验收权威明确记录了允许的风险接受。
6. 合并前一刻，合并权威必须核对当前 Head、审查状态、未解决发现、必需检查与依赖。

An active `REQUEST_CHANGES` review MUST block merging. An unresolved material blocking finding MUST also block merging, even if no formal `REQUEST_CHANGES` review was submitted.

处于活动状态的 `REQUEST_CHANGES` 审查必须阻断合并。即使未提交正式 `REQUEST_CHANGES` 审查，未解决的实质阻断性发现同样必须阻断合并。

Any exception requires an explicit decision by the authorized acceptance authority, recording the finding, rationale, accepted risk, scope, and decision evidence. Such an exception MUST NOT override mandatory security, domain-owner, or release-authority approval.

任何例外均需经授权的验收权威明确裁定，并记录该发现、理由、接受的风险、范围与决策证据。此类例外不得覆盖强制性的安全、领域负责人或发布权威审批。

This is a process requirement. It MUST NOT be described as a platform-enforced merge block unless the repository's live GitHub configuration has been verified to enforce it (see §7).

本条为流程要求。除非仓库的实时 GitHub 配置经核实确实强制执行，否则不得表述为平台强制的合并阻断（见 §7）。

#### 6.1.1 What does not trigger the lock / 不触发处置锁的情形

Ordinary discussion comments, non-blocking suggestions, and review comments that do not assert a material blocking finding do not lock the PR. The lock attaches only to a formal `REQUEST_CHANGES` review, or to a material blocking finding / `HOLD` disposition explicitly recorded by a reviewer with that authority. Without this boundary, routine commentary could hold a PR open indefinitely.

普通讨论评论、非阻断性建议，以及未主张实质阻断性发现的审查评论，均不触发该锁。该锁仅附着于正式 `REQUEST_CHANGES` 审查，或由具备该权限的审查方明确记录的实质阻断性发现 / `HOLD` 处置。缺少这一边界，日常评论即可无限期锁住 PR。

#### 6.1.2 Origin / 来源

This clause exists because a review disposition and a merge happened 27 seconds apart, with the correction landing on an already-merged branch 18 minutes later and never reaching the target branch. The interval is the evidence, not the rule: the rule exists because the review disposition state and the merge permission had no enforced relationship. See `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13 for the instance record.

本条的由来：一次审查处置与一次合并相隔 27 秒，修正 18 分钟后落在已合并分支上，从未进入目标分支。时间间隔是证据而非规则本身：规则之所以存在，是因为审查处置状态与合并权限之间缺少强制关系。实例记录见 `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13。

#### 6.1.3 Re-review of Corrective Commits and the Final Head / 修正提交与最终 Head 的重新审查

When one or more corrective commits are pushed to address a blocking finding, a review disposition issued against the previous Head MUST NOT automatically be treated as review or approval of the new Head.

An authorized reviewer MUST inspect the final exact Head proposed for merge. The re-review MUST confirm all of the following:

1. Whether every previously recorded blocking finding has been resolved on that Head;
2. Whether the corrective commits, individually and in combination with the pre-existing changes, introduce any new material issue;
3. Whether the final Head continues to satisfy all applicable architecture, governance, security, testing, and other mandatory requirements.

Even when a corrective commit addresses only one known finding, the reviewer MUST NOT limit the re-review to that finding's local diff while ignoring the complete change set of the final Head.

Any subsequent commit that changes the Head after the re-review invalidates the re-review conclusion for the previous Head; the final Head MUST be checked again before merge. Passing CI, an author statement that the issue has been fixed, or approval of an earlier Head cannot substitute for this re-review.

每当为解决阻断性发现而推送一个或多个修正提交时，先前针对旧 Head 的审查结论不得自动视为对新 Head 的审查或批准。

有权审查者 MUST 检查合并候选的最终精确 Head。该复核 MUST 同时确认：

1. 此前记录的每一项阻断性发现是否已在该 Head 上得到解决；
2. 修正提交及其与原有变更的组合是否引入新的实质性问题；
3. 最终 Head 是否仍满足适用的架构、治理、安全、测试及其他强制要求。

即使修正提交只针对一个已知 finding，审查方也不得将复核范围限制为该 finding 的局部差异，而忽略最终 Head 的完整变更集合。

任何在复核后再次改变 Head 的提交，均使此前针对旧 Head 的复核结论失效；合并前必须重新核对最终 Head。CI 通过、作者声明修复完成或旧 Head 已获批准，均不能替代该复核。

A review and its associated CI results apply only to the exact merge candidate that was checked. If the base branch advances after review or validation, the resulting base-and-Head combination MUST be revalidated against all applicable required checks before merge. A passing result for the PR Head against an earlier base, and a passing result for the earlier base by itself, do not establish that their later combination is valid. If the merge candidate changes after this revalidation, the affected checks MUST be rerun before merge. Where the changed candidate affects the reviewed content or its material context, the independent review MUST also be renewed.

审查及其关联 CI 结果仅适用于实际接受检查的精确合并候选版本。若审查或验证后 base 分支前进，则在合并前 MUST 针对由更新后的 base 与 PR Head 组成的合并候选版本，重新运行所有适用的必需检查。PR Head 相对于较早 base 的通过结果，以及较早 base 自身的通过结果，均不能证明两者之后的组合仍然有效。若该次重新验证后合并候选版本再次发生变化，则合并前 MUST 重新运行受影响的检查。若候选版本变化影响已审查的内容或其重要上下文，还 MUST 重新进行独立审查。

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

This standard is **ADOPTED** as a process policy, as recorded by Issue #130 comment #6962523529 after PR #144 merged. This adoption does not claim platform enforcement. Platform enforcement remains separately tracked by Issue #134.

Changes to this standard require a bilingual semantic-parity update and an exact-Head governance review. If the repository platform cannot enforce a required control, the limitation remains BLOCKED until an administrator establishes a genuinely enforceable configuration.

本规范已被采用为**流程治理规范**；Issue #130 comment #6962523529 在 PR #144 合并后记录了采用决定。该采用不代表 GitHub 平台已经强制执行。平台强制执行仍由 Issue #134 单独跟踪。

本规范的修改必须同步更新双语语义版本，并进行精确 Head 治理审查。如果仓库平台无法强制执行某项必需控制，则该控制继续保持 BLOCKED，直到管理员建立真正可强制执行的配置。


## 10. Enforcement and evidence addendum / 强制执行与证据补充

Version 1.1 implementation details are maintained in the paired [English enforcement and evidence addendum](../docs/en/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md) and [Chinese enforcement and evidence addendum](../docs/zh-CN/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md). The addendum specifies exact-Head CI and bilingual gates, independent approval, prompt-hash/session audit evidence, CANDIDATE-to-DECIDED evidence, administrator-only branch protection actions for Issue #134, Issue #130 operational coverage audit, and rollback/emergency correction. The addendum remains PROPOSED until its PR is reviewed and merged; this link does not imply platform enforcement.

Version 1.1 的执行细节见[英文强制执行与证据补充规范](../docs/en/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md)和[中文强制执行与证据补充规范](../docs/zh-CN/14-ai-development/PR-GOVERNANCE-001-ENFORCEMENT.md)。补充规范定义精确 Head CI 与双语门禁、独立审批、提示词哈希/会话审计证据、CANDIDATE 升级 DECIDED 的证据标准、Issue #134 仅管理员可执行的平台分支保护操作、Issue #130 运营覆盖审计以及回退/紧急纠正策略。补充规范在其 PR 经审查并合并前保持 PROPOSED；该链接不代表平台强制控制已经启用。
