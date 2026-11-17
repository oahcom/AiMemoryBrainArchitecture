# Phase 3.8.14 — D Exact Review: H Applied Delivery Evidence Replay ForgetFence Callback
# Phase 3.8.14 — D 精确审查：H Applied Delivery Evidence Replay ForgetFence Callback

- Owner domain: D — Memory Brain / ForgetFence Authority.
- Mode: delegated D-role exact review; **not an independent human D Owner signature**.
- D branch reviewed: \`session-d-memory-brain-2026-11-16@7e6d0b133dae88f442665e7b05a54060e047647e\`.
- D publication/terminal contract: Phase 3.8 Blob \`17e53890dd6cce9bea9eacc1be2e64b0ef55ac78\`.
- Prior D/H callback review: Phase 3.8.11 Blob \`7a9ed2bcf7fd34edc576a4a1be7f4388ee551b43\`.
- H branch reviewed: \`session-h-bmcp-protocol@b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9\`.
- H validator Blob: \`8febb915ec321cc37cf159b2f5b917a3f945726c\`.
- H tests Blob: \`77cb66b895c5293a2f4883b1d5cb69775e71d00c\`.
- H hardening addendum Blob: \`4c220e998fc6ba700157598b0384dc3134cf8575\`.
- H Applied Delivery Evidence CI: run \`44181762581\`, **SUCCESS, 29/29 tests**.
- Disposition: **ACCEPT SEPARATE D FORGETFENCE CALLBACK AS REFERENCE BOUNDARY WITH CONDITIONS; D LINEAGE/RELEASE AUTHORITY NOT VERIFIED**.

## 1. D decision scope

D reviews only the ForgetOperation/Fence/lineage currentness check required before H discloses a historical replay result. I current authorization is a separate conjunctive check. A successful I result does not imply D clearance; H's callback does not create or terminalize a D participant.

D Phase 3.8 requires exact PublicationParticipant and complete dependency/lineage inventory; D-local positions remain opaque and are never compared numerically with I PermissionEpoch or Storage positions. A D receipt proves only the named D decision and is never an independent Storage write capability.

## 2. Exact H callback boundary

H now exposes a separate tri-state callback:

\`verify_current_d_forget_fence(envelope, original_result_ref)\`

It runs independently from \`verify_current_i_replay_authorization\` before SAME_DIGEST_REPLAY returns an original result reference.

D accepts this callback as a reference boundary only if the production D adapter resolves the exact Context/Delivery/Managed Region identity to authoritative G/D records and checks:
- exact ContextId/ContextVersion, DeliveryId/DeliveryAttemptId, managed-region identity/revision/digest and relevant source/target lineage;
- ForgetOperationRef and current ForgetFenceGeneration;
- target/source/ancestor Scope generation and digest;
- complete affected ProducerWork/Attempt/Derivative membership and dependency/lineage inventory;
- D barrier generation/root/terminality and unresolved PublicationParticipant/ProducerWork state;
- D owner-ledger high-water/root and snapshot/restore continuity;
- late-discovery successor snapshot and final D-local currentness CAS.

The H 1.0.0 envelope does not carry a direct D fence proof field. Therefore the D adapter must resolve lineage/currentness from authoritative G/D records using the exact context/delivery/region references; it MUST NOT trust caller-supplied or inferred fence values. If the exact lineage cannot be resolved, the result is UNKNOWN and no replay result reference is disclosed.

## 3. Fail-closed requirements

- D callback True: may proceed only if the separate I callback also returned True.
- D callback False: INVALID; no original result reference.
- D callback unavailable/exception/None: UNKNOWN; no original result reference.
- No timeout, missing row, stale snapshot, queue deletion, age-based cleanup or absence of a visible participant may imply D clearance.
- A later ForgetFence may invalidate current-use while preserving historical evidence; replay disclosure is a current-use boundary and must honor the current fence.
- D callback does not issue D PublicationReceipt, close a PublicationParticipant, release a Forget barrier or prove global Forget completion.

## 4. Remaining D gates

This review does not implement a live D ledger resolver, complete lineage pagination, late-discovery handling, barrier terminality, D currentness CAS or production Storage visibility proof. The H callback is an injected seam and tests use deterministic doubles. D Owner approval and exact integration conformance remain open.

**Final disposition:** D replay ForgetFence callback **ACCEPTED AS REFERENCE CANDIDATE WITH CONDITIONS**; production D lineage/currentness/release **OPEN / NOT VERIFIED**; no Forget completion, global Forget, physical erasure or production activation is claimed.

---

## 5. 中文完整结论

D 本次只审查 H 披露历史 Replay Result 前所需的 ForgetOperation/Fence/Lineage 当前性检查。I 当前授权是独立合取条件。I 检查成功不代表 D Clearance；H Callback 不能创建或终态化 D Participant。

H 现在提供独立的 \`verify_current_d_forget_fence(envelope, original_result_ref)\` Tri-state Callback，并与 I Callback 分开执行。D 仅在生产 Adapter 能把精确 Context/Delivery/Managed Region Identity 解析到权威 G/D Record，并检查完整 ForgetOperation/Fence/Lineage、Scope Generation、Affected Producer/Attempt/Derivative Membership、Barrier Root/Terminality、D Owner Ledger High-water/Restore Continuity、Late Discovery Successor Snapshot 和 D-local Currentness CAS 时，才接受该接口作为参考边界。

H 1.0.0 Envelope 没有直接携带 D Fence Proof 字段，因此 D Adapter 必须使用精确 Context/Delivery/Region 引用，从权威 G/D Record 解析 Lineage/Currentness；不得信任调用方自带或推断的 Fence 值。无法解析时必须 UNKNOWN，且不披露 Replay Result Ref。

D Callback False 为 INVALID；不可用/异常/None 为 UNKNOWN；二者均不得披露 Result Ref。Timeout、Missing Row、Stale Snapshot、Queue Deletion 或 Age-based Cleanup 都不能推断 D Clearance。D Callback 不签发 PublicationReceipt、不关闭 PublicationParticipant、不释放 Forget Barrier，也不证明 Global Forget 完成。

本审查不实现真实 D Ledger Resolver、完整 Lineage Pagination、Late Discovery、Barrier Terminality、D Currentness CAS 或生产 Storage Visibility Proof。H Callback 仍为注入接缝，测试使用确定性 Double。D Owner 批准与精确集成符合性仍 OPEN。

最终状态：D Replay ForgetFence Callback **参考候选有条件接受**；生产 D Lineage/Currentness/Release **OPEN / NOT VERIFIED**；不声称 Forget Completion、Global Forget、物理擦除或生产激活。

## 6. Current H code-head delta — 2026-11-18

The original 29-test snapshot above is historical. H's current Owner branch is `session-h-bmcp-protocol@4386f67a61f7968da4c3603f28cc8a5100714f9f`. The final H successor commit adds a Unified 1.2.15 structural-conformance document; the replay code and tests are unchanged at the Blob level.

Current exact H pins:
- Applied Delivery Evidence schema Blob: `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`.
- Validator Blob: `43f402e4a09034da197ac24856cddbd496c9c75f`.
- Conformance test Blob: `98242cc193a77b27d58b39353ccc031201992614`.
- Hardening addendum Blob: `4c220e998fc6ba700157598b0384dc3134cf8575`.

The exact 30-test code Head reviewed in the later H/C pass is `4c16410f8b20b8fc2bc8c7609eb7bf07d83f317e`; run [#44187702465](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187702465) is SUCCESS, 30/30. Its validator/test Blobs match the current H Owner branch pins above. This is code-blob equivalence, not a claim that CI ran on the later documentation-only branch HEAD `4386f67...`.

The current 30-test suite retains the separate D replay callback:
- `verify_current_d_forget_fence(envelope, original_result_ref)` runs independently from the I callback before SAME_DIGEST_REPLAY returns the original result reference.
- False => INVALID and no result reference; None/exception => UNKNOWN and no result reference.
- The H envelope carries no direct D Fence proof. Production D must resolve exact ContextId/ContextVersion, DeliveryId/Attempt, Managed Region identity/revision/digest and full source/target lineage from authoritative G/D records; caller-supplied or inferred fence values are not acceptable.
- The D adapter must verify current ForgetOperation/FenceGeneration, ancestor/source/target Scope generations, complete ProducerWork/Attempt/Derivative and dependency membership, barrier root/terminality, unresolved publication participants, D ledger high-water/restore continuity and late-discovery successor state.
- D must not issue a PublicationReceipt, close a participant, release a Forget barrier or infer global Forget completion merely by approving replay disclosure.

**Updated disposition:** the D callback shape remains ACCEPTED AS REFERENCE CANDIDATE WITH CONDITIONS on the current code Blob. The callback remains injected; no live D lineage/currentness resolver, late-discovery inventory, D currentness CAS, barrier-release proof or production Storage visibility proof is present. This delegated D-role review is not an independent human D Owner signature and does not establish Forget completion or production activation.

### 中文：当前 H 代码 Head 差异

上方 29 项测试快照已是历史记录。H 当前 Owner 分支为 `session-h-bmcp-protocol@4386f67a61f7968da4c3603f28cc8a5100714f9f`。最后 H 后继提交只增加 Unified 1.2.15 结构符合性文档；Replay 代码和测试 Blob 未改变。

当前 H 精确来源：Schema `2ce8776...`、Validator `43f402e...`、Tests `98242cc...`、Hardening Addendum `4c220e9...`。后续 30 项精确代码 Head `4c16410...` 的 Run #44187702465 SUCCESS，30/30；其 Validator/Tests Blob 与当前 H Owner 分支一致。这是代码 Blob 等价，不表示 CI 运行在仅增加文档的后续分支 Head 上。

当前 30 项测试保留独立 D Replay Callback：SAME_DIGEST_REPLAY 返回 Original Result Ref 前，独立执行 `verify_current_d_forget_fence`；False 为 INVALID 且不返回引用，None/异常为 UNKNOWN 且不返回引用。H Envelope 没有直接携带 D Fence Proof。生产 D 必须从权威 G/D Record 解析精确 Context/Version、Delivery/Attempt、Managed Region Identity/Revision/Digest 和完整 Source/Target Lineage；不得接受调用方自带或推断的 Fence 值。

D Adapter 还必须验证当前 ForgetOperation/FenceGeneration、祖先/Source/Target Scope Generation、完整 ProducerWork/Attempt/Derivative 与 Dependency Membership、Barrier Root/Terminality、未解决 PublicationParticipant、D Ledger High-water/Restore Continuity 和 Late-discovery Successor State。D 不得仅因允许 Replay Disclosure 就签发 PublicationReceipt、关闭 Participant、释放 Forget Barrier 或推断 Global Forget 完成。

更新结论：D Callback 结构在当前代码 Blob 上仍**有条件接受为参考候选**；Callback 仍是注入接缝，没有真实 D Lineage/Currentness Resolver、Late-discovery Inventory、D Currentness CAS、Barrier-release Proof 或生产 Storage Visibility Proof。此委派 D 角色审查不是独立人类 D Owner 签名，不证明 Forget 完成或生产激活。
