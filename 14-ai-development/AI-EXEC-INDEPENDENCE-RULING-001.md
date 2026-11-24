---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Metadata added on 2026-11-24 so that this file can be edited without tripping DM-01. No content claim in this file is verified by this block."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AI-EXEC-INDEPENDENCE-RULING-001
# Session Independence, Platform Identity and R3 Expert Review / 会话独立、平台身份与 R3 专家审查裁定

- Document ID: AI-EXEC-INDEPENDENCE-RULING-001
- Version: 1.0
- Status: PROPOSED — pending explicit Project Owner adoption; this session does not claim Owner adoption
- Ruling date: 2026-11-18 (execution date; coordinator observations also cite 2026-11-19)
- Authority: L4 governance adjudication session; Project Owner adoption remains required for repository-wide normative policy
- Tracking: Issue #130; AID-2026-005; related PRs #249/#251/#252/#253/#258 and Issue #264
- Relationship: COMPLEMENT — narrow interpretation; no source clause is amended or waived
- Review-by: 2026-12-02
- Language authority: English and Chinese provisions are intended to be semantically equivalent; independent bilingual review NOT RECORDED

## Status path / 状态路径

PROPOSED → ADOPTED only after the Project Owner, or a delegate with explicit documented authority to adopt repository-wide governance policy, records an affirmative attributable decision in an existing governance carrier. The record must identify this document/version, adopting authority, effective date, relationship, rationale, boundary and review date. An author-identity COMMENT, AI role simulation, commit, merge, silence or this session's own ruling is not adoption. Until then this remains a proposal, not an effective amendment to ADOPTED standards.

PROPOSED → ADOPTED 仅可在项目 Owner，或具有明确书面仓库级治理规范采用授权的代理人，于既有治理载体作出明确且可归属的采用决定后发生。记录须标明文件/版本、采用权威、生效日期、文档关系、理由、边界和复核日期。作者身份 COMMENT、AI 角色模拟、提交、合并、沉默或本会话自身裁定均不构成采用。在此之前，本文件仍是提案，不是对 ADOPTED 规范的有效修订。

Basis: AI-EXEC-001 v1.1 and AI-EXEC-002 v1.1 are ADOPTED via PR #256 merge 48a556491506d25e78be47957276bf3821797a0a; PR-GOVERNANCE-001 is ADOPTED via Issue #130 comment #6962523529; AI-EXEC-UNIFICATION-RULING-001 is the binding precedent. This proposal is COMPLEMENT, not SUPERSEDE.

依据：AI-EXEC-001/002 v1.1 已随 PR #256 合并 48a556491506d25e78be47957276bf3821797a0a 而 ADOPTED；PR-GOVERNANCE-001 由 Issue #130 评论 #6962523529 采用；AI-EXEC-UNIFICATION-RULING-001 为约束性先例。本提案关系为 COMPLEMENT，不是 SUPERSEDE。

---

## RULING-04 — Two non-substitutable independence dimensions / 裁定四——两种不可替代的独立性

**Conflict / 冲突点.** NR-001 / OPTION A permits a genuinely new independent ChatGPT conversation to satisfy the independent-session requirement subject to controls. PR-GOVERNANCE-001 §5 as amended 2026-11-24 makes independence a property of the reviewing session: a review through the same connected GitHub identity as the author **is** independent when the reviewing session is not the authoring session. Before that amendment §5 required a distinct GitHub actor, which NR-001 / OPTION A could not supply. AI-EXEC-001 v1.1 §6 and AI-EXEC-002 §5 preserve both requirements; the amendment removes the conflict rather than choosing a side.

NR-001 / OPTION A 允许真正新建的独立 ChatGPT 对话在满足控制条件时满足独立会话要求。PR-GOVERNANCE-001 §5 经 2026-11-24 修订后，把独立性定义为审查会话的属性：只要审查会话不是撰写会话，即使沿用作者所用的同一已连接 GitHub 身份，**仍**构成独立。修订前的 §5 要求独立的 GitHub 操作者，而 NR-001 / OPTION A 无法提供，这才是原先的冲突所在。AI-EXEC-001 v1.1 §6 和 AI-EXEC-002 §5 同时保留两项要求；本次修订是消除冲突，不是在其中选边。

**Ruling / 裁定.**
1. Session/review-behavior independence (S-independence) means a genuinely new conversation distinct from authoring/implementation, supplied with frozen inputs, independently reading repository sources, performing adversarial review and recording findings, with NR-001 disclosure that conversation isolation is not model/provider/statistical independence.
2. Platform-identity/review-event independence (P-independence) — **retired 2026-11-24.** Was defined as: the review event is attributable to a GitHub identity distinct from the author's connected GitHub identity. Item 5 records why it no longer stands as a bar; it is kept here so that rulings written against it remain readable.
3. S-independence satisfies the independence requirement of `PR-GOVERNANCE-001` §5 in full, as amended 2026-11-24 to make independence a property of the reviewing session. It does not create a second GitHub actor and does not produce Owner approval; neither is required for independence.
4. Under the repository's stated ChatGPT-native model where sessions share oahcom, a fresh session satisfies §5 independence. The shared GitHub actor is the carrier of the review event, not the measure of its independence; what §5 now asks is whether the reviewing context is the authoring context, and for a fresh session it is not.
5. AI-EXEC-001 R2 maps independent ChatGPT session to S-independence, which is now the §5 requirement itself. Affected Owner explicit contract approval is separate and still required. R3 additionally requires security/domain expert review, reproducible tests and explicit Acceptance Authority approval. Those remain non-substitutable; P-independence no longer exists as a separate bar.
6. For §5-covered changes (security, identity, authorization, Forget, lifecycle, canonical persistence, recovery, cross-owner contracts, production operations), a qualifying independent session is sufficient for the independence element of MERGE. High-risk changes additionally require the affected Owner's explicit approval, which no session supplies. Absent that approval, disposition remains HOLD, or REMEDIATE/REJECT as justified.

1. 会话/审查行为独立性（S 独立性）指真正新建、区别于作者/实现会话的对话，取得冻结输入，独立读取仓库源文件，开展对抗性审查并记录 findings，同时按 NR-001 披露对话隔离不代表模型/服务商/统计独立。
2. 平台身份/审查事件独立性（P 独立性）——**2026-11-24 退役。** 原定义为：审查事件归属于不同于作者所用连接身份的 GitHub 身份。第 5 项记录它为何不再作为门槛；保留在此是为了让针对它写下的裁定仍然可读。
3. S 独立性完整满足 `PR-GOVERNANCE-001` §5 的独立性要求——该条已于 2026-11-24 修订为「独立性是审查会话的属性」。它不创建第二个 GitHub 操作者，也不产生 Owner 批准；而这两者都不是独立性的必要条件。
4. 在本仓库所有会话共享 oahcom 的 ChatGPT-native 模式下，新会话即满足 §5 独立性。共享的 GitHub 操作者是审查事件的载体，不是其独立性的度量；§5 现在问的是「审查上下文是否为撰写上下文」，而对新会话而言它不是。
5. AI-EXEC-001 R2 的独立 ChatGPT 会话对应 S 独立性，而它现在就是 §5 的要求本身。受影响 Owner 明确批准契约是独立门禁，仍然必需。R3 另要求安全/领域专家审查、可复现测试和 Acceptance Authority 明确批准；这些仍不可替代。P 独立性不再作为独立门槛存在。
6. 对 §5 覆盖的变更，合格的独立会话足以满足 MERGE 的独立性要素。高风险变更另需受影响 Owner 的明确批准，而这不由任何会话提供。无该批准时仍须 HOLD，或按事实 REMEDIATE/REJECT。

**Boundaries / 边界.** No model independence, multi-model consensus, human expertise, platform enforcement or independent GitHub actor is claimed. Role separation is not actor separation. Role simulation inside the authoring session must never be relabeled independent; a separate session under the same identity already is independent.

不宣称模型独立、多模型共识、真人专家身份、平台强制控制或独立 GitHub 操作者。角色分离不等于操作者分离；在撰写会话内做的角色扮演不得重新标记为独立。同一身份下的**另一个会话**本就是独立，无需重新标记。

**Effective scope / 生效范围.** Prospective interpretation after adoption. Review by 2026-12-02. / 采用后向前适用。复核期限 2026-12-02。

---

## RULING-05 — Five-disposition authorization chain / 裁定五——五态授权链

**Conflict / 冲突点.** NR-001 review + Owner comments + an exception + exact-Head checks could be misread as enough to merge despite §5, converting exception recording into waiver.

NR-001 审查 + Owner 评论 + 例外 + exact-Head 检查可能被误读为足以绕过 §5 合并，从而把例外登记变成豁免。

**Ruling / 裁定.** Preserve exactly MERGE / HOLD / REMEDIATE / SUPERSEDED / REJECT:
- MERGE only if every applicable exact-Head check passes; an independent-session §5 review exists where applicable; NR-001 review exists where required; every affected authority Owner explicitly approves the exact normative contract boundary; R3 additionally has qualified independent expert review, reproducible test evidence and Acceptance Authority approval; dependencies are satisfied; no blocking finding remains; and the PR is mergeable.
- HOLD if any required review, Owner approval, expert review, exact-Head check, reproducible evidence or dependency is missing, pending, NOT RUN, NOT VERIFIED or attributable only to the shared identity.
- REMEDIATE for a concrete defect/evidence gap repairable on the same coherent carrier; re-review the changed exact Head.
- SUPERSEDED only when an actual replacement fully supersedes the carrier; preserve unique evidence. It is not a shortcut around missing approval.
- REJECT when the proposal is invalid or conflicts with accepted authority; preserve rationale and evidence.

严格保留 MERGE / HOLD / REMEDIATE / SUPERSEDED / REJECT 五态：
- MERGE 仅在所有适用 exact-Head 检查通过；适用时有独立会话 §5 审查；需要时有 NR-001 审查；每个受影响权威 Owner 明确批准准确规范契约边界；R3 另有合格独立专家审查、可复现测试和 Acceptance Authority 批准；依赖满足；无阻断 finding；PR 可合并时成立。
- 任一必需审查、Owner 批准、专家审查、exact-Head 检查、可复现证据或依赖缺失、待定、NOT RUN、NOT VERIFIED，或仅归属于共享身份时，必须 HOLD。
- REMEDIATE 用于可在同一连贯载体修复的具体缺陷/证据缺口；变更后重新审查新 exact Head。
- SUPERSEDED 仅在真实替代项完整取代载体时使用，并保留独有证据；不得绕过批准缺失。
- REJECT 用于提案无效或与已接受权威冲突；保留理由和证据。

**Owner approval protocol / Owner 批准协议.** The actual accountable Owner (or a delegate with documented authority) must issue a direct, attributable, explicit written decision identifying PR/Work Item, exact Head or immutable contract version/blob, clauses/fields, ACCEPT / REJECT / ACCEPT WITH AMENDMENTS, conditions, identity/role and timestamp. Use an existing Issue/PR comment or link a verifiable Owner-authored artifact. If GitHub actor is shared oahcom, disclose it; do not represent it as a distinct platform identity or GitHub APPROVE. Verify attribution through an authorized Owner channel. If attribution cannot be verified, Owner gate remains OPEN.

实际 accountable Owner（或具备书面授权的代理人）必须直接作出可归属、明确的书面决定，标明 PR/Work Item、准确 Head 或不可变契约版本/Blob、条款/字段、ACCEPT / REJECT / ACCEPT WITH AMENDMENTS、条件、身份/角色和时间戳。记录放在既有 Issue/PR 评论，或链接可核验的 Owner 署名工件。若 GitHub 操作者为共享 oahcom，必须披露，不得将其描述为不同平台身份或 GitHub APPROVE。必须通过获授权的 Owner 渠道核验归属；无法核验时 Owner 门禁保持 OPEN。

Never issue or claim GitHub APPROVE as a workaround for the platform's self-approval prohibition. Owner written decision may satisfy only the Owner contract-approval gate when attribution and scope are verified; it is not §5 independence and cannot substitute for it. Independence is supplied by a separate reviewing session, which this repository can always open; where even that is unavailable, HOLD and escalate to Project Owner/repository administrator.

绝不得将 GitHub APPROVE 作为平台自审禁令的变通方式。Owner 书面决定只有在归属和范围可核验时才满足 Owner 契约批准门禁，它本身不是 §5 独立性，也不能替代独立性。独立性由另一个审查会话提供，而本仓库始终可以开启这样的会话；连这一步都不可得时才 HOLD 并升级给项目 Owner/仓库管理员。

**Boundaries / 边界.** No combination of same-identity COMMENT, role simulation, Owner narrative, exception entry or green CI manufactures an independent reviewer. Exception alone never changes HOLD to MERGE. / 同身份 COMMENT、角色模拟、Owner 叙述、例外登记或绿色 CI 的任何组合都不能制造独立审查者；例外本身绝不能将 HOLD 变为 MERGE。

**Effective scope / 生效范围.** All five-state decisions after adoption. Review by 2026-12-02. / 采用后适用于全部五态决策。复核期限 2026-12-02。

---

## RULING-06 — Explicit §5 exception protocol / 裁定六——§5 显式例外登记协议

**Conflict / 冲突点.** PR-GOVERNANCE-001 §5 requires explicit exception recording but does not enumerate fields/counting/carriers. AI-EXEC-001 v1.1 §6 restricts exceptions to escalation/HOLD/REMEDIATE/REJECT and caps them at two per iteration.

PR-GOVERNANCE-001 §5 要求显式登记例外，但未枚举字段/计数/载体。AI-EXEC-001 v1.1 §6 将例外限制为升级/HOLD/REMEDIATE/REJECT，并规定每迭代最多两项。

**Ruling / 裁定.** An exception is a time-bounded record of an unavailable control/resource, never a waiver. Register one per distinct blocked Work Item/PR plus missing mandatory control/resource.

例外是对控制/资源不可用情况的限时记录，绝不是豁免。每个不同的受阻 Work Item/PR 与缺失强制控制/资源组合登记一项。

| Field / 字段 | Required content / 必需内容 |
|---|---|
| Exception ID | EX-YYYYMMDD-NN, unique within iteration / 迭代内唯一 |
| Work Item/carrier | AID, Issue, PR, repository / 仓库与载体 |
| Rule/control | Exact clause and missing review/evidence / 准确条款与缺失控制 |
| Risk/scope | R0–R3 and affected boundary / 风险级与影响边界 |
| Request time | Timezone timestamp + source link / 含时区时间与来源链接 |
| Missing resource | Independent GitHub reviewer, expert, Owner decision or test / 缺失资源 |
| Attempts/source order | Recipients, requests, timestamps, responses; NR-001 first where applicable / 尝试与来源顺序 |
| Reason | Factual unavailability; distinguish not-requested from no-response / 事实原因 |
| Disposition | HOLD / REMEDIATE / REJECT only / 仅限三种处置 |
| Escalation owner/time | Named accountable Owner/admin and timestamp / 升级责任人与时间 |
| Open evidence | Exact missing items; retain NOT RUN / NOT VERIFIED / 未满足证据 |
| Next review | Timestamp / 下次复核时间 |
| Deadline | 24-hour escalation and 3-business-day disposition where §6 applies / 适用时限 |
| Decision | Continue HOLD / REMEDIATE / REJECT; authority and timestamp / 决定、权威、时间 |
| Closure evidence | Actual control obtained or remediation/rejection; exact link/SHA / 关闭证据 |
| Iteration/count | Iteration key, ordinal 1 or 2, over-quota marker / 迭代与计数 |
| Disclosure | Shared GitHub identity, AI simulation and provenance limits / 身份与出处披露 |

**Counting / 计数.**
- Count each distinct blocked Work Item/PR plus missing mandatory control/resource once per iteration. Same control and continuous blocked interval for one PR counts once; separate controls (for example §5 reviewer and R3 expert) count separately.
- New iteration, renewed request after recorded deadline, materially different missing control or new PR/Work Item is a new exception. Do not split one event to inflate counts or merge distinct controls to hide counts.
- Limit remains no more than two per iteration. A third is over-quota, must be recorded and escalated to daily governance window; omission does not make it compliant.
- Keep the countable register in the existing owning Issue/PR thread and link it from manifest/Closeout. Issue #130 is cross-PR index; details remain on each affected existing PR/Issue. If no PR exists, use existing Issue or Closeout. Never create an Issue solely for an exception.
- Close only when missing control is actually obtained or an authorized REMEDIATE/REJECT decision is recorded. Expiry, silence or elapsed time does not close it.

- 每个不同的受阻 Work Item/PR 与缺失强制控制/资源组合，每迭代计一次。同一 PR、同一控制、同一连续受阻区间计一次；不同控制（如 §5 审查者与 R3 专家）分别计数。
- 新迭代、超过已记录期限后的重新请求、实质不同的缺失控制或新 PR/Work Item 均构成新例外。不得拆分事件虚增数量，也不得合并不同控制隐匿数量。
- 配额仍为每迭代不超过两项。第三项属于超额，必须登记并升级至日度治理窗口；不登记不代表合规。
- 可计数登记册放在既有归属 Issue/PR 线程，并由 manifest/Closeout 链接。Issue #130 作为跨 PR 索引；详细记录仍留在各受影响 PR/Issue。无 PR 时使用既有 Issue 或 Closeout。不得仅为例外新建 Issue。
- 仅当实际取得缺失控制，或有授权的 REMEDIATE/REJECT 决定时才能关闭。到期、沉默或时间流逝不能关闭例外。

**Boundaries / 边界.** Exceptions do not satisfy missing review/approval/expert/test, turn NOT RUN into PASS, authorize downgrade or permit MERGE. Clock triggers escalation/disposition only. / 例外不满足缺失审查/批准/专家/测试，不把 NOT RUN 变为 PASS，不授权降级或 MERGE；时钟只触发升级/处置。

**Effective scope / 生效范围.** New exception records after adoption; no fabricated historical evidence. Review by 2026-12-02. / 采用后适用于新例外；不得补造历史证据。复核期限 2026-12-02。

---

## RULING-07 — R3 expert source and escalation clock / 裁定七——R3 专家来源与升级时钟

**Conflict / 冲突点.** AI-EXEC-001 v1.1 requires R3 independent security/domain expert review, reproducible tests and explicit Acceptance Authority approval. NR-001 does not waive these gates.

AI-EXEC-001 v1.1 要求 R3 独立安全/领域专家审查、可复现测试和 Acceptance Authority 明确批准；NR-001 不豁免这些门禁。

**Ruling / 裁定.** A qualifying expert must be a real, identifiable human with competence relevant to the particular risk, evidenced by professional role/experience, relevant work, qualification or a documented accountable-Owner assessment. The person must be independent of author/implementation, disclose conflicts, and review exact Head or immutable artifact. The report must identify reviewer, expertise/basis, independence/conflict disclosure, exact SHA, scope, methods/evidence, findings/severity, conclusion, limitations and timestamp. A platform expert resource may qualify only if it is a verifiable human expert and all independence requirements are met; no such resource is asserted to exist here. ChatGPT conversations, model personas, prompt roles, AI panels or vendor/model labels never qualify.

合格专家必须是真实、可识别的人类，具备与具体风险相关的能力，并由专业职责/经验、相关工作、资格或 accountable Owner 书面评估证明。该人员必须独立于作者/实现者、披露利益冲突，并审查准确 Head 或不可变工件。报告须标明审查者、专业领域/依据、独立性/冲突披露、准确 SHA、范围、方法/证据、findings/严重级、结论、限制和时间戳。平台专家资源只有在其为可核验的人类专家且满足全部独立性要求时才可能合格；本裁定不宣称存在此类资源。ChatGPT 对话、模型人格、提示词角色、AI 面板或供应商/模型标签永远不能充当专家。

**Clock / 时钟**
- Start at the evidenced request timestamp. If no qualifying resource/evidence is obtained within 24 hours, escalate to accountable Owner and keep HOLD/BLOCKED; record request, attempts, missing resource, escalation recipient and next review.
- If still unavailable at 3 business days, accountable Owner records continue HOLD, REMEDIATE with concrete acquisition plan, or REJECT. Timeout never authorizes MERGE, ACCEPTED, risk downgrade or waiver.
- If historical request time is absent, mark NOT RECORDED and start a new prospective clock from a newly evidenced request; never invent/backdate.
- PR #249: RV-249-2 is BLOCKER and says NR-001 session review cannot satisfy the R3 expert gate. Keep BLOCKED/HOLD until qualified expert report and reproducible exact-Head evidence exist, in addition to §5 and Owner gates. Apply clock from verifiable request time; if unavailable, mark NOT RECORDED and initiate a fresh request.
- PR #258: F-PR258-REVIEW-02 is BLOCKER; F-PR258-RESILIENCE-01 is P1. Exact-Head Rust/GOV-DOC checks are recorded SUCCESS, but subprocess crash/recovery, concurrent append, restart receipt stability, payload-tamper detection and WAL recovery remain NOT VERIFIED/NOT RUN; independent persistence/security-domain review remains required. Keep HOLD/BLOCKED. Green CI does not close missing tests or expert review. Apply same request-clock rule.
- Reproducible evidence identifies exact source SHA, command, environment/dependencies, fixtures, expected/actual results, logs/artifact links and independent reproduction instructions. Any required test not run remains NOT RUN.

- 从可核验请求时间启动。24 小时内未取得合格资源/证据，升级至 accountable Owner 并保持 HOLD/BLOCKED；记录请求、尝试、缺失资源、升级对象和下次复核。
- 3 个工作日仍不可用时，accountable Owner 记录继续 HOLD、带具体获取计划的 REMEDIATE 或 REJECT。超时绝不授权 MERGE、ACCEPTED、风险降级或豁免。
- 历史请求时间缺失时标记 NOT RECORDED，并从新取得证据的请求启动前瞻时钟；不得虚构/倒签。
- PR #249：RV-249-2 为 BLOCKER，指出 NR-001 会话审查不能满足 R3 专家门禁。除 §5 和 Owner 门禁外，必须取得合格专家报告和 exact-Head 可复现证据后才能解除 HOLD/BLOCKED。按可核验请求时间计算时钟；若缺失，标记 NOT RECORDED 并重新请求。
- PR #258：F-PR258-REVIEW-02 为 BLOCKER；F-PR258-RESILIENCE-01 为 P1。记录显示 exact-Head Rust/GOV-DOC 检查 SUCCESS，但子进程崩溃/恢复、并发追加、重启回执稳定性、payload 篡改检测和 WAL 恢复仍为 NOT VERIFIED/NOT RUN；独立持久化/安全领域审查仍缺失。必须保持 HOLD/BLOCKED。绿色 CI 不能关闭缺失测试或专家审查。适用同一请求时钟。
- 可复现证据须标明准确源 SHA、命令、环境/依赖、fixture、预期/实际结果、日志/产物链接及独立复现说明。任何必需测试未运行仍为 NOT RUN。

**Boundaries / 边界.** This ChatGPT session is not a security/domain expert. No R3 evidence is waived. / 本会话不是安全/领域专家；不豁免任何 R3 证据。

**Effective scope / 生效范围.** R3 qualification and clock records after adoption. Review by 2026-12-02. / 采用后适用于 R3 专家资格和时钟记录。复核期限 2026-12-02。

---

## RULING-08 — Phase B application to PRs #251/#252/#253 / 裁定八——Phase B 三个 PR 的规则适用

Rules-only application. No PR state, branch or metadata is changed. / 仅作规则适用判断，不改变 PR 状态、分支或元数据。

| PR | Present rule conclusion | Required gates before MERGE |
|---|---|---|
| #251 RFC-IDE-001 | Cross-owner identity/Scope/idempotency contract; §5 applies. Exact Head/CI not recorded in INDEX; required Owner decisions not evidenced complete. **HOLD.** | Fresh NR-001 review; independent-session §5 review; attributable Domain Model/Producer Identity, Scope/Security and Event Store Owner decisions against exact contract version; exact-Head checks; resolve or explicitly exclude TTL, cleanup, ProducerIdentity composition and digest CANDIDATE/TO_VALIDATE items; no BLOCKER. |
| #252 D/E/I/Storage convergence | Cross-owner normative interfaces and security/authorization/recovery boundaries; §5 applies. Successor pins recorded, but exact-Head checks and all D/E/I/Storage Owner decisions not evidenced complete. **HOLD.** | Fresh NR-001 review; independent-session §5 review; D, E, I and Storage decisions against exact successor Blobs; close D-HW-01/H-RJ-HW-01 or keep outside accepted scope; applicable exact-Head checks; physical conformance and production authorization remain separate. |
| #253 acceptance matrix | Cross-owner acceptance authority/evidence boundary; §5 applies. Exact Head/CI and Owner adoption/approval not recorded complete. **HOLD.** | Fresh NR-001 review; independent-session §5 review; Project Owner/authorized governance adoption and affected Owner approvals for normative responsibility boundaries; exact-Head GOV-DOC/bilingual checks; no logical acceptance represented as physical conformance or production approval. |

| PR | 当前规则结论 | MERGE 前门禁 |
|---|---|---|
| #251 RFC-IDE-001 | 跨 Owner 身份/Scope/幂等契约，适用 §5。INDEX 未记录准确 Head/CI；必需 Owner 决定未证明齐全。**HOLD。** | 新 NR-001 审查；独立会话 §5 审查；Domain Model/Producer Identity、Scope/Security、Event Store Owner 对准确契约版本作可归属决定；exact-Head 检查；解决或明确排除 TTL、清理、ProducerIdentity 组合和 digest 的 CANDIDATE/TO_VALIDATE 项；无 BLOCKER。 |
| #252 D/E/I/Storage 收敛 | 跨 Owner 规范接口及安全/授权/恢复边界，适用 §5。已记录 successor pins，但未证明准确 Head 检查和 D/E/I/Storage 全部 Owner 决定完成。**HOLD。** | 新 NR-001 审查；独立会话 §5 审查；D、E、I、Storage 对准确 successor Blobs 作决定；关闭 D-HW-01/H-RJ-HW-01 或明确保留在验收范围外；适用 exact-Head 检查；物理符合性和生产授权仍为独立门禁。 |
| #253 验收矩阵 | 跨 Owner 验收权威/证据边界，适用 §5。准确 Head/CI 和 Owner 采用/批准未记录为完成。**HOLD。** | 新 NR-001 审查；独立会话 §5 审查；Project Owner/授权治理者采用及受影响 Owner 对规范责任边界批准；exact-Head GOV-DOC/双语检查；不得把逻辑验收表述为物理符合性或生产批准。 |

All three retain their existing platform state; no GitHub APPROVE is issued or inferred. New findings must be recorded in existing Issue/PR comments with ID + severity + return destination. No new Issue is opened.

三个 PR 保留现有平台状态；不发出或推断 GitHub APPROVE。新 finding 必须在既有 Issue/PR 评论中按 ID + 严重级 + 回流去向登记。不新建 Issue。

**Boundaries / 边界.** Not an implementation review or fresh CI run; refresh exact Head, checks and Owner decisions at any later merge decision. / 本节不是实现审查或新 CI 运行；未来合并决策时重新核实准确 Head、检查和 Owner 决定。

**Effective scope / 生效范围.** Rules-only application to #251/#252/#253. Review by 2026-12-02. / 仅对 #251/#252/#253 作规则适用判断。复核期限 2026-12-02。

---

## Terminology / 术语表

| Term | Definition |
|---|---|
| S-independence | NR-001 fresh-session review; not model/provider/statistical independence. |
| P-independence | **Retired 2026-11-24.** Was: review event attributed to a GitHub identity different from the author's. No longer an independence bar; see `INDEPENDENCE-IS-SESSION-LEVEL-036`. |
| Owner approval | Explicit attributable approval by actual accountable authority for its normative boundary. |
| Expert review | Additional review by verifiable competent independent human; never a ChatGPT role. |
| Exception | Time-bounded unavailability record for escalation/HOLD/REMEDIATE/REJECT; never waiver. |
| Exact-Head | Evidence tied to precise current commit SHA. |
| NOT RUN | Required check not executed; never PASS. |
| Five dispositions | MERGE, HOLD, REMEDIATE, SUPERSEDED, REJECT. |

## Bilingual semantic parity self-check / 双语语义对等自检声明

The authoring session checked both languages for the same independence axes, non-substitution rules, five dispositions, Owner attribution protocol, exception fields/counting, R3 qualification/clock and Phase B HOLD conclusions. Author self-check only; independent bilingual semantic review NOT RECORDED. GOV-DOC-001 PASS is not claimed.

起草会话自检确认中英文均包含相同的独立性维度、不可替代规则、五态处置、Owner 归属协议、例外字段/计数、R3 专家资格/时钟和 Phase B HOLD 结论。仅为作者自检；独立双语语义审查 NOT RECORDED。不宣称 GOV-DOC-001 PASS。

## Evidence and provenance / 证据与出处

- Readback Blob SHAs: AI-EXEC-001 cb95815627f895e2cf46c4e801b91153b2713f0b; AI-EXEC-002 64a85bc8763ba22a88dc791daddae548b93e4f5d; PR-GOVERNANCE-001 4a28fa8181af0da06f52d31a6dca5d30fbf6458a; UNIFICATION-RULING 94939179ce592cd82e1a34ab8c5bd9fb6bad0283; INDEX 981bd6d3720fc8fb8d8de0a6942b85f1d4022eed.
- Prompt provenance: T2 chat instruction; coordinator session + 本会话任务提示词（独立性口径裁定）. Stable conversation ID/permalink, raw bytes and SHA-256 unavailable; SHA-256 NOT_VERIFIED. No fictional repository prompt file/hash.
- Baseline: main@6b5db2918cffc2281deb22fd9858a37dbaeec726 as stated in PR #258 quota-closeout evidence; direct branch-ref HEAD query unavailable, not represented as a fresh HEAD response.
- Verification: policy/documentation only; runtime tests NOT RUN / NOT APPLICABLE; independent GOV-DOC-001 check NOT RUN.
- Findings: F-AID005-01 [BLOCKER] → Issue #130; F-AID005-02 [P1] → Issue #130.
---

## Amendment record / 修订记录（2026-11-24）

**本文件的 RULING-04 第 3、4、5、6 项已按所有者基线修改**，术语表的 P-independence 条目标记为退役。

原因：`PR-GOVERNANCE-001` §5 于 2026-11-24 修订，独立性改为**会话级**属性。RULING-04 原判定
「S 独立性不能替代 P 独立性、§5 要求 P 独立性」因此失去依据——它所解释的那条文本已不存在。

**保留不变**：S 独立性仍然不是模型/服务商/统计独立；同会话内角色模拟仍然不构成独立审查；
受影响 Owner 的明确批准仍然独立必需；五态处置、例外字段、R3 专家审查要求均不变。

**这不是本文件自我采用。** 本文件状态仍为 `PROPOSED`。本次修改的是它与现行 §5 不一致的部分，
若不改，它会持续引用一条已被替换的条款。采用与否仍由所有者决定。

Revision of this file's RULING-04 items 3–6 follows the owner baseline and the §5 amendment of
2026-11-24. What is preserved: S-independence is still not model/provider/statistical independence;
role simulation within the authoring session still does not count; affected Owner approval is still
separately required; the five dispositions, exception fields and R3 expert-review requirements are
untouched. This file remains `PROPOSED`; the change only removes its reference to a clause that no
longer exists.

