# PR #28 — Independent Bilingual Semantic Parity Review
# PR #28 — 中英文架构文档独立语义一致性复审

- Review ID: BILINGUAL-SEMANTIC-REVIEW-PR28-001
- Review version: 1.0
- Reviewed PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/28
- Reviewed branch: `docs/bilingual-coverage-completion`
- Reviewed snapshot: `b66703cd63bcf45082bc5d544a61345567eb5249`
- Review date: 2026-11-17
- Review mode: targeted independent semantic review of high-risk contracts and status semantics
- Overall disposition: **CONDITIONAL PASS FOR THE REVIEWED HIGH-RISK PAIRS; NOT A FULL BILINGUAL PARITY SIGN-OFF; NOT APPROVED FOR MERGE**

## 1. Executive conclusion / 结论摘要

The reviewed high-risk English/Chinese pairs are substantially aligned on their core authority boundaries, state distinctions, fail-closed requirements, and non-guarantees. No critical reversal of ownership, security policy, or Forget completion semantics was found in the sampled contracts.

本轮抽查的高风险中英文文档，在核心权威边界、状态区分、Fail-closed 要求和非保证事项上总体一致。抽查范围内未发现 Owner 权限、安全策略或 Forget 完成语义被翻译反转的 Critical 级问题。

The review is **not** a blanket approval of all 124 changed files. It is a targeted pass over domain epistemic/time semantics, lifecycle, scope/permission, D Forget/cursor/publication contracts, E receipt/producer-admission/provenance contracts, and F retrieval/activation/cache/scheduling contracts, plus the associated coverage metadata.

本结论**不代表对 PR 中全部 124 个变更文件的整体批准**。本轮重点覆盖领域认知/时间语义、生命周期、Scope/Permission、D Forget/Cursor/Publication 契约、E Receipt/Producer Admission/Provenance 契约、F Retrieval/Activation/Cache/Scheduling 契约及其覆盖状态元数据。

## 2. High-risk semantic checks passed / 已通过的高风险语义核查

### 2.1 Domain model / 领域模型

- Epistemic Status remains independent from Memory Lifecycle. Observed/Reported/Inferred/Verified/Disputed/Retracted are not translated as lifecycle states or as a linear confidence ladder.
- Intent/Plan/Prediction/Pending/Attempted are not promoted into completed outcomes without outcome evidence.
- Event Time, Recorded At and Valid Time remain distinct; unknown Valid Time is not treated as “valid forever”.
- Lifecycle state remains separate from Claim epistemic status. Forgotten is terminal for the old content identity; Archive is not Forget; Context Remove is not Forget.
- Scope defines namespace/applicability while Permission defines actor/action authorization. Scope membership does not grant permission; async workers must re-check current authorization.

- Epistemic Status 与 Memory Lifecycle 保持独立；Observed/Reported/Inferred/Verified/Disputed/Retracted 未被翻译为生命周期状态或线性置信度等级。
- Intent/Plan/Prediction/Pending/Attempted 未在缺少 Outcome Evidence 时被提升为已完成结果。
- Event Time、Recorded At、Valid Time 保持区分；未知 Valid Time 不表示“永久有效”。
- Lifecycle State 与 Claim Epistemic Status 分离。Forgotten 对旧内容身份是终态；Archive 不等于 Forget；Context Remove 不等于 Forget。
- Scope 定义命名空间/适用范围，Permission 定义 Actor/Action 授权。Scope 成员身份不授予权限；异步 Worker 必须重新检查当前授权。

### 2.2 D — Forget, cursor and publication / D — Forget、Cursor 与 Publication

- Logical Suppression, Asynchronous Cleanup and Physical Erasure remain three distinct outcomes.
- D's CanonicalSuppressionComplete is not I's Global Forget Completion and is not proof of physical erasure.
- ForgetOperation state is distinct from Memory Lifecycle; “Forgetting” is not a Memory lifecycle state.
- ForgetFenceGeneration/ForgetFenceCursor, CanonicalCommitCursor, ProducerRegistrationSequence/HighWater, AggregateRevision, LifecycleEventCursor, IndexWatermark, PermissionEpoch and ContextVersion remain separate typed namespaces.
- Producer registration and fence installation require a shared linearizable ordering domain; final publication checks the latest applicable D fence and current I PermissionEpoch at the same visibility boundary. A detached check-then-write or uncoordinated token is insufficient.
- Part 4's D acceptance remains limited to D-owned fence/barrier semantics. I authorization, Storage realization, cross-owner conformance and production activation remain OPEN/NOT RUN.

- Logical Suppression、Asynchronous Cleanup、Physical Erasure 仍是三种不同结果。
- D 的 CanonicalSuppressionComplete 不等于 I 的 Global Forget Completion，也不是物理擦除证明。
- ForgetOperation 状态与 Memory Lifecycle 分离；“Forgetting”不是 Memory 生命周期状态。
- ForgetFenceGeneration/ForgetFenceCursor、CanonicalCommitCursor、ProducerRegistrationSequence/HighWater、AggregateRevision、LifecycleEventCursor、IndexWatermark、PermissionEpoch、ContextVersion 保持为不同的类型化 Namespace。
- Producer Registration 与 Fence Installation 必须在共享线性化排序域内排序；最终 Publication 必须在同一可见性边界检查最新适用 D Fence 和当前 I PermissionEpoch。分离的 Check-then-write 或未协调 Token 不足以保证安全。
- Part 4 的 D 接受仅限 D 拥有的 Fence/Barrier 语义。I Authorization、Storage 实现、跨 Owner Conformance 和 Production Activation 仍为 OPEN/NOT RUN。

### 2.3 E — Receipt, admission and provenance / E — Receipt、Admission 与 Provenance

- AcceptedReceipt, ProducerRegistrationReceipt, CompilerCompletionReceipt, CanonicalCommitReceipt, DerivedRegistrationReceipt, PublicationReceipt and IndexAppliedAcknowledgement prove different facts; neither language collapses them into one success state.
- Accepted is tied to durable ingress commit, not mere process receipt or queue enqueue.
- DLQ/LeaseExpired/Timeout/lost ACK/unknown publication outcome are not terminal success. Unknown publication keeps the artifact private.
- Retry/replay preserves stable logical work identity and source lineage while using a new AttemptId; current authorization and Forget checks are repeated.
- Source/environment identity is included in the semantic request digest in both languages.
- Evidence/Provenance remains source-lineage evidence, not a truth score; independent Evidence authorization and D dependency registration precede visibility.

- AcceptedReceipt、ProducerRegistrationReceipt、CompilerCompletionReceipt、CanonicalCommitReceipt、DerivedRegistrationReceipt、PublicationReceipt、IndexAppliedAcknowledgement 证明不同事实；两种语言均未将其合并成一个 Success 状态。
- Accepted 以持久化 Ingress Commit 为准，不是进程收到字节或 Queue Enqueue。
- DLQ/LeaseExpired/Timeout/ACK 丢失/Publication Outcome Unknown 都不是终态成功。Publication 结果未知时 Artifact 必须保持 Private。
- Retry/Replay 保留稳定逻辑 Work Identity 和 Source Lineage，同时使用新的 AttemptId；并重新检查当前 Authorization 与 Forget。
- 两种语言的 Semantic Request Digest 均包含来源/环境身份。
- Evidence/Provenance 是来源血缘证据，不是真实性评分；可见性之前必须独立授权 Evidence 并完成 D Dependency Registration。

### 2.4 F — Runtime safety and status semantics / F — Runtime 安全与状态语义

- Scope-before-Candidate is a hard invariant; unauthorized records must not enter fusion, reranking, counts, caches or activation.
- Cache hits and Working Set reuse revalidate current I permission and D fence/lifecycle; stale or unverifiable entries are dropped/quarantined, not served.
- F advances only its own invalidation generation and does not mint or advance D's ForgetFence.
- ActivationRecommendation is a proposal to G; it does not mutate ContextVersion, constitute Delivery or prove Applied.
- Conflicting Claims are not silently resolved by ranking; support/refute evidence and conflict markers are preserved.
- Partial/degraded/unavailable outcomes are distinct from complete; scheduling and cancellation do not turn partial results into complete results.

- Scope-before-Candidate 是硬性不变量；未授权记录不得进入 Fusion、Reranking、Count、Cache 或 Activation。
- Cache Hit 和 Working Set Reuse 必须重新验证当前 I Permission 与 D Fence/Lifecycle；陈旧或无法验证的条目必须丢弃/隔离，不能返回。
- F 只推进自己的 Invalidation Generation，不创建或推进 D ForgetFence。
- ActivationRecommendation 是提交给 G 的 Proposal；它不修改 ContextVersion、不构成 Delivery，也不证明 Applied。
- Ranking 不得静默裁决冲突 Claim；必须保留 Support/Refute Evidence 和 Conflict Marker。
- Partial/Degraded/Unavailable 与 Complete 状态不同；Scheduling/Cancellation 不得把部分结果变成完整结果。

## 3. Findings / 发现项

### BSR-28-001 — Recorded At wording weakens the durability qualifier
- Severity: **P2 — terminology precision**
- Files:
  - `docs/en/02-domain-model/epistemic-and-temporal-semantics.md`
  - `docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md`
- Evidence: English defines Recorded At as assigned by Brain “at durable acceptance”; Chinese currently says “在可靠接收时赋值” and repeats “在可靠接收时赋值 Recorded At” in the workflow.
- Risk: “可靠接收” can be read as reliable receipt/transport acceptance rather than the durable acceptance linearization point. That ambiguity could move the meaning of Recorded At earlier than the committed durable receipt.
- Required correction: use an explicit equivalent such as “在持久化接受提交时赋值” or “在持久化接收成功提交时赋值”, and keep the same wording in §8.
- This is a wording-precision finding, not evidence that the underlying English/Chinese temporal model is otherwise inconsistent.

### BSR-28-002 — Coverage registers and PR summary are stale/inconsistent with the branch tree
- Severity: **P2 — governance/status accuracy**
- Files:
  - `docs/translation-status.md`
  - `docs/owner-branch-translation-inventory.md`
  - PR #28 description
- Evidence:
  - The branch contains all five F detailed pairs: Runtime Overview, Retrieval Engine, Activation Policy Engine, Working Set and Cache, and Runtime Scheduling. However, `docs/translation-status.md` still says F's five detailed specs are English-only / NOT STARTED, and `docs/owner-branch-translation-inventory.md` still says F is NOT STARTED.
  - The PR description says E Evidence/Provenance is pending, but both `docs/en/04-memory-compiler/evidence-and-provenance.md` and `docs/zh-CN/04-memory-compiler/evidence-and-provenance.md` exist and carry the same source Blob reference.
  - The PR description reports E as 6/8 paired, while `docs/translation-status.md` reports 7/8. The remaining Forget/Derived Registration scope needs an exact split/source inventory before the count is changed.
  - `docs/translation-status.md` and the PR description report D as 8/8 paired, while `docs/owner-branch-translation-inventory.md` still reports 7/8 and says the operation/publication gate is pending, despite the bilingual wrapper and Parts 1–4 being present.
- Risk: reviewers and AI developers may rely on contradictory coverage statements and either duplicate work or incorrectly assume untranslated material is complete.
- Required correction: reconcile the exact source-spec count and split inventory; mark F as “paired in PR #28; semantic review pending” rather than NOT STARTED; align D's 8/8 state across both registers; correct the PR E summary after confirming the remaining Forget/Derived Registration scope.

### BSR-28-003 — PR validation summary is stale
- Severity: **P3 — review metadata**
- File: PR #28 description
- Evidence: PR body says the current-head CI result is “pending after the prompt-library gate update”; the recorded workflow run `44050762889` completed successfully for the structural bilingual/prompt-library gate.
- Risk: PR readers see an obsolete validation status.
- Required correction: update the PR body with the actual run result and retain the qualification that structural CI does not prove semantic parity.

## 4. Review boundaries and non-findings / 复审边界与未发现事项

- No Critical/P0 semantic reversal was found in the targeted high-risk pairs reviewed above.
- The source/environment identity digest requirement is present in both languages; no finding is raised for it.
- D Part 4's ordering cases (submit-before-fence, fence-before-submit, and unknown/incomparable ordering) align in the English and Chinese text reviewed.
- The review did not execute Rust tests, fault-injection tests, Storage crash/recovery tests, or cross-owner conformance suites. All source documents that label these tests NOT RUN remain NOT RUN.
- This review does not approve architecture freeze, implementation sign-off, branch protection, or merge.

- 在上述抽查的高风险双语文档中，未发现 Critical/P0 级语义反转。
- 两种语言均包含 Source/Environment Identity Digest 要求；不对此项登记缺陷。
- 已核对的 D Part 4 中 Submit-before-Fence、Fence-before-Submit、Unknown/不可比较顺序三种情况，中英文一致。
- 本复审没有执行 Rust 测试、故障注入测试、Storage 崩溃/恢复测试或跨 Owner Conformance Suite。源文档标记为 NOT RUN 的测试仍然是 NOT RUN。
- 本复审不批准架构冻结、实现签收、分支保护或合并。

## 5. Recommended disposition / 建议处置

1. Fix BSR-28-001 in the Chinese temporal-semantics document.
2. Reconcile BSR-28-002 across the bilingual coverage register, Owner inventory and PR description without prematurely marking semantic review complete.
3. Update BSR-28-003's PR validation statement.
4. Keep PR #28 Draft until the findings are corrected and the remaining changed architecture pairs receive the planned semantic review.
5. After fixes, rerun structural CI and perform a final diff review; do not treat CI success as semantic approval.

1. 修正 BSR-28-001 的中文时间语义措辞。
2. 对齐 BSR-28-002 涉及的双语覆盖清单、Owner Inventory 和 PR 描述，但不得提前将语义复审标记为完成。
3. 更新 BSR-28-003 的 PR 验证状态。
4. 在缺陷修复、剩余架构双语文件完成计划中的语义复审之前，PR #28 保持 Draft。
5. 修复后重跑结构性 CI 并复核最终 Diff；不得把 CI 成功等同于语义批准。
