# PR #28 — Independent Bilingual Semantic Parity Review
# PR #28 — 中英文架构文档独立语义一致性复审

- Review ID: BILINGUAL-SEMANTIC-REVIEW-PR28-001
- Review version: 1.0
- Reviewed PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/28
- Reviewed branch: `docs/bilingual-coverage-completion`
- Reviewed snapshot: `9b525f400c45e701c6888e99d3ff2b200ef46f27` (includes follow-up P2 fixes and cross-module identity/Applied/Storage review)
- Review date: 2026-11-17
- Review mode: targeted independent semantic review of high-risk contracts and status semantics
- Overall disposition: **CONDITIONAL PASS FOR THE REVIEWED HIGH-RISK PAIRS; NOT A FULL BILINGUAL PARITY SIGN-OFF; NOT APPROVED FOR MERGE**

## 1. Executive conclusion / 结论摘要

The reviewed high-risk English/Chinese pairs are substantially aligned on their core authority boundaries, state distinctions, fail-closed requirements, and non-guarantees. No critical reversal of ownership, security policy, or Forget completion semantics was found in the sampled contracts.

本轮抽查的高风险中英文文档，在核心权威边界、状态区分、Fail-closed 要求和非保证事项上总体一致。抽查范围内未发现 Owner 权限、安全策略或 Forget 完成语义被翻译反转的 Critical 级问题。

The review is **not** a blanket approval of all 125 changed files. It is a targeted pass over domain epistemic/time semantics, lifecycle, scope/permission, D Forget/cursor/publication contracts, E receipt/producer-admission/provenance contracts, and F retrieval/activation/cache/scheduling contracts, plus the associated coverage metadata.

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

## 5. Focused cross-module identity, Applied and Storage/Consistency review / 跨模块身份、Applied 与 Storage/Consistency 专项复审

### 5.1 Reviewed bilingual pairs / 已复审双语配对

The following PR #28 pairs were checked against each other at the current branch snapshot:

- `docs/en/01-system-architecture/component-interactions.md` ↔ `docs/zh-CN/01-system-architecture/component-interactions.md`
- `docs/en/01-system-architecture/data-flows.md` ↔ `docs/zh-CN/01-system-architecture/data-flows.md`
- `docs/en/01-system-architecture/integration-governance-guide.md` ↔ `docs/zh-CN/01-system-architecture/integration-governance-guide.md`
- `docs/en/12-testing-and-acceptance/cross-module-conformance-guide.md` ↔ `docs/zh-CN/12-testing-and-acceptance/cross-module-conformance-guide.md`
- `docs/en/02-domain-model/scope-and-permission-model.md` ↔ `docs/zh-CN/02-domain-model/scope-and-permission-model.md`

No material semantic divergence was found in the checked identity and Applied summaries:
- Principal/ActorRef/ScopeRef/ProducerIdentity remain distinct; identity authentication, domain reference semantics, wire binding, telemetry assertion and owner-side enforcement remain assigned to their respective authorities.
- Scope is not Permission; payload-supplied identity is not authenticated transport identity; async work rechecks current authorization.
- Applied is tied to the exact ContextVersion and Adapter boundary receipt; it is not model comprehension. The conformance guide preserves final-request attestation, offline reconnect against ContextVersion/PermissionEpoch/ForgetFenceGeneration, and fail-closed behavior for unknown Forget targets.
- Typed cursor/epoch namespaces remain distinct in the integration guide, including ForgetFenceGeneration/Cursor, PermissionEpoch, ContextVersion, IndexWatermark and AdapterCapabilityEpoch.
- Component interaction tables preserve Context version commit, asynchronous delivery, Applied acknowledgement and Sync/Adapter failure containment.

本轮核对了上述五组 PR #28 中英文配对。身份和 Applied 摘要未发现实质语义偏差：
- Principal/ActorRef/ScopeRef/ProducerIdentity 保持不同类型；身份认证、领域引用语义、Wire 绑定、遥测声明和 Owner 边界执行仍由各自权威负责。
- Scope 不等于 Permission；Payload 自报身份不等于已认证 Transport Identity；异步任务必须重新检查当前授权。
- Applied 绑定准确 ContextVersion 和 Adapter 边界 Receipt，不代表模型理解。Conformance 指南保留了最终请求 Attestation、离线重连时对 ContextVersion/PermissionEpoch/ForgetFenceGeneration 的协调，以及未知 Forget 目标 Fail-closed 要求。
- Integration Guide 保留不同 Cursor/Epoch Namespace，包括 ForgetFenceGeneration/Cursor、PermissionEpoch、ContextVersion、IndexWatermark 和 AdapterCapabilityEpoch。
- Component Interaction 双语表均保留 Context Version 提交、异步 Delivery、Applied 确认以及 Sync/Adapter 故障隔离。

### 5.2 Authoritative source status checked / 权威源规范状态核验

The paired guides are not the detailed contracts. The current Owner source snapshots show:

| Source artifact | Exact source revision | Current status / limitation |
|---|---|---|
| B `principal-actor-binding-mapping.md` | `bbbef919e1e2ffe158cda8d9b2c5e718efaae969` | CANDIDATE; identity freeze INT-P0-02 / INT-X-03 remains OPEN |
| B `typed-reference-and-scope-semantics.md` | `e9a6bd21e06bc02a5208619f5a949217860b1c00` | CANDIDATE; Claim identity remains ADR-BLOCKED; typed identity/Scope/Environment semantics require dependent approvals |
| C `phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | C-owned semantic decisions recorded; C/G/H cross-owner freeze BLOCKED; implementation/execution NOT VERIFIED |
| H `adapter-capability-and-applied-attestation.md` | `ed6b43a29aa368d772c701ffc83309a5aadf3c00` | CANDIDATE; final-request proof profile OPEN with C; authorization binding OPEN with I |
| H `phase-3.6-authenticated-identity-protected-operation-binding.md` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` | JOINT-DECIDED technical baseline; governance and consumer acceptance OPEN; implementation/conformance NOT VERIFIED |
| H `phase-3.6-identity-binding-consumer-conformance-status.md` | `8afb914731a34d8ab44331f54f1f39bfd8ec37ce` | Protocol design JOINT-DECIDED; consumer acceptance OPEN; governance GOVERNANCE-BLOCKED; H36 NOT RUN |
| G `phase-3.6-applied-forget-reconciliation-contract.md` | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | G semantic decisions recorded; C/G/H Applied freeze BLOCKED; implementation/execution NOT VERIFIED |
| Storage `phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md` | `175ee7b1349cfdb79a19898b311a88391ed88010` | Logical transaction proposal; physical topology and implementation proof OPEN |
| Storage `phase-3.8.2-storage-serialization-topology-adr.md` | `080433f8e13a500522bc2754da64057edb0ae9d8` | ADR-BLOCKED; candidate options only; no deployed topology selected; T1–T8 OPEN |
| Storage exact-version review of COC/I/D bundle | `d2e804da153ae30e9c2862bf524bc89c42a5dad3` | ACCEPT on recovery batch/manifest ordering only; joint freeze remains BLOCKED |
| Storage/JF-10 `phase-3.6.2-jf10-cross-authority-recovery-protocol.md` | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` | CANDIDATE; I acceptance required; NOT IMPLEMENTED; conformance NOT RUN; JF-10 P0 OPEN |
| Storage restore `phase-3.6.5-restore-control-highwater-and-quarantine-contract.md` | `4f656163aeba532a441eaed1d293a48e2363cb4a` | CANDIDATE; exact I-D-A-Storage review required; restore remains fenced absent current control high-water proof |

The C contract requires the actual post-transformation final request to cross the observed successful submit boundary, with runtime-assigned InferenceRequestId, exact Context/Delivery identifiers, complete managed-region digest, current PermissionEpoch, D ForgetFence and H CapabilityEpoch. G alone accepts Applied. Tier 2/3 cannot claim Full Applied. Historical Applied remains an audit fact but cannot be reused after revocation/Forget invalidation. Unknown ordering fails closed.

The Storage contracts require durable hidden participant preparation, exact D participant/fence binding, consumed I authorization proof, and a single final visibility linearization transaction that atomically commits VisibilityPointer, PublicationReceipt/outcome and outbox. UNKNOWN remains private. Restore starts quarantined and requires independent COC/I/D/Storage high-water and participant reconciliation; no single cursor proves global safety.

C 契约要求实际经过全部转换的最终请求越过可观测的成功 Submit 边界，并绑定 Runtime 分配的 InferenceRequestId、准确 Context/Delivery 标识、完整 Managed Region Digest、当前 PermissionEpoch、D ForgetFence 和 H CapabilityEpoch。只有 G 可以接受 Applied。Tier 2/3 不得声称 Full Applied。历史 Applied 可以保留为审计事实，但在撤销/Forget 失效后不得再次用于后续请求。无法证明顺序时必须 Fail-closed。

Storage 契约要求先持久化隐藏 Participant，绑定准确 D Participant/Fence、已消费的 I Authorization Proof，并通过唯一最终 Visibility Linearization Transaction 原子提交 VisibilityPointer、PublicationReceipt/Outcome 和 Outbox。UNKNOWN 必须保持 Private。Restore 必须从隔离状态开始，并独立协调 COC/I/D/Storage High-water 与 Participant；任何单一 Cursor 都不能证明全局安全。

### 5.3 BSR-28-004 — High-risk detailed contracts are not part of PR #28 / 高风险详细契约未纳入 PR #28

- Severity: **P1 — high-risk coverage / acceptance gate**
- Status: **OPEN — explicitly tracked scope gap, not a translation mismatch in the reviewed guide pairs**
- Evidence: PR #28 changes bilingual reader/overview guides through F, but it does not include paired detailed specifications for B Phase 3 typed identity/Principal binding, C/G/H final-request Applied contracts, or Storage/Consistency COC/JF-10/visibility/restore contracts. The current `docs/translation-status.md` branch overlay records these detailed sets as pending.
- Risk: a reader could over-read the system guides as if they were frozen, complete cross-owner contracts. The authoritative sources are still CANDIDATE/BLOCKED/OPEN/NOT VERIFIED as listed above.
- Required action: keep PR #28's scope statement explicit; do not mark identity, Applied, Storage topology, JF-10 or restore as bilingual-complete or accepted. Create exact-source-SHA bilingual pairs in subsequent tracked batches, and preserve each source's candidate/blocking/not-run status.

- 严重级别：**P1 — 高风险覆盖/验收门禁**
- 状态：**OPEN — 已明确登记的范围缺口，不是本轮已复审指南配对中的翻译偏差**
- 证据：PR #28 包含截至 F 的双语阅读/总览指南，但未包含 B Phase 3 Typed Identity/Principal Binding、C/G/H Final-request Applied 契约或 Storage/Consistency COC/JF-10/Visibility/Restore 契约的成对详细规范。当前 `docs/translation-status.md` 分支覆盖表已将这些详细文档登记为待处理。
- 风险：读者可能误将系统指南理解为已冻结、完整的跨 Owner 契约；但上述权威源文件仍处于 CANDIDATE/BLOCKED/OPEN/NOT VERIFIED 状态。
- 要求：PR #28 必须继续明确其范围；不得将 Identity、Applied、Storage Topology、JF-10 或 Restore 标记为双语完成或已验收。后续批次必须按准确源 SHA 创建双语配对，并保留每份源文件的 Candidate/Blocking/Not-run 状态。

## 6. Findings / 发现项

### BSR-28-001 — Recorded At wording weakens the durability qualifier
- Severity: **P2 — terminology precision**
- Status: **RESOLVED** in PR #28 commit `b8295214517c2a6dbaf87a4c75dc91b53721a1b4`.
- Files:
  - `docs/en/02-domain-model/epistemic-and-temporal-semantics.md`
  - `docs/zh-CN/02-domain-model/epistemic-and-temporal-semantics.md`
- Evidence at review snapshot: English defines Recorded At as assigned by Brain “at durable acceptance”; the original Chinese used “在可靠接收时赋值”.
- Risk: the original Chinese could be read as reliable receipt/transport acceptance rather than the durable acceptance linearization point.
- Resolution: both occurrences in the Chinese document now say “在持久化接受成功提交时赋值”, matching the durable acceptance boundary without changing the source specification.

### BSR-28-002 — Coverage registers and PR summary were stale/inconsistent with the branch tree
- Severity: **P2 — governance/status accuracy**
- Status: **RESOLVED** in PR #28 commits `2e3e7a4d303cb218b485c46d8093da80ec117795` and `1ffedc673f0b50f27b31430246dd71c522adde04` (with subsequent formatting correction).
- Files:
  - `docs/translation-status.md`
  - `docs/owner-branch-translation-inventory.md`
  - PR #28 description
- Evidence:
  - The branch contains all five F detailed pairs: Runtime Overview, Retrieval Engine, Activation Policy Engine, Working Set and Cache, and Runtime Scheduling. However, `docs/translation-status.md` still says F's five detailed specs are English-only / NOT STARTED, and `docs/owner-branch-translation-inventory.md` still says F is NOT STARTED.
  - The PR description says E Evidence/Provenance is pending, but both `docs/en/04-memory-compiler/evidence-and-provenance.md` and `docs/zh-CN/04-memory-compiler/evidence-and-provenance.md` exist and carry the same source Blob reference.
  - The PR description reports E as 6/8 paired, while `docs/translation-status.md` reports 7/8. The remaining Forget/Derived Registration scope needs an exact split/source inventory before the count is changed.
  - `docs/translation-status.md` and the PR description report D as 8/8 paired, while `docs/owner-branch-translation-inventory.md` still reports 7/8 and says the operation/publication gate is pending, despite the bilingual wrapper and Parts 1–4 being present.
- Risk: reviewers and AI developers could rely on contradictory coverage statements.
- Resolution: `docs/translation-status.md` now has an explicit PR #28 branch overlay distinguishing file-pair presence from semantic review/source reconciliation; it records B 6/6, D 8/8, E 7/8 and F 5/5, with G/C/H/I detailed pairs and Storage/Consistency correctly pending. `docs/owner-branch-translation-inventory.md` now preserves historical source-branch audit SHAs while separately recording D 8/8 and F 5/5 companion presence in PR #28. The PR description has been aligned to this same scope and explicitly retains Draft status.

### BSR-28-003 — PR validation summary was stale; corrected
- Severity: **P3 — review metadata**
- Status: **RESOLVED** in the PR description after this finding was recorded.
- File: PR #28 description
- Evidence: the stale PR statement was replaced. On current PR head `d1196a1fa6bbab5d1b978c1344061a2c749e8b1b`, workflow runs `44058512458` and `44058466437` both completed successfully; job `GOV-DOC-001 structural checks` passed in both runs.
- Risk: PR readers could otherwise see an obsolete validation status.
- Resolution: PR body now records the current-head structural gate result and explicitly states that structural CI does not prove semantic parity.

## 7. Review boundaries and non-findings / 复审边界与未发现事项

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

## 8. Recommended disposition / 建议处置

1. BSR-28-001 and BSR-28-002 are resolved in the current PR branch; keep their resolution evidence traceable.
2. BSR-28-003 is resolved in the PR description and current-head CI record.
3. Continue the targeted review of identity binding, Applied proof and Storage/Consistency contracts.
4. Keep PR #28 Draft until remaining semantic review, source-branch reconciliation and required governance checks are complete.
5. Rerun structural CI after the remaining review changes; do not treat CI success as semantic approval.

1. BSR-28-001 和 BSR-28-002 已在当前 PR 分支修复，并保留对应证据。
2. BSR-28-003 已在 PR 描述和当前 HEAD 的 CI 记录中修复。
3. 继续针对身份绑定、Applied 证明和 Storage/Consistency 契约开展专项审查。
4. 在剩余语义复审、源分支基线核对和必要治理检查完成前，PR #28 保持 Draft。
5. 后续审查变更完成后重跑结构性 CI；不得把 CI 成功等同于语义批准。
