# Phase 3.8.23 — G Successor Consumer Decision: H Applied Delivery Evidence 1.0.0
# Phase 3.8.23 — G 后继消费者决议：H Applied Delivery Evidence 1.0.0

- Owner domain: G — ContextVersion, Delivery, Applied State and Reconciliation.
- Mode: delegated G-role exact consumer review under user instruction; **not an independent human G Owner signature**.
- G normative source: Phase 3.8.22 Blob \`bd297873bc1e593280484a43cb44b56058d9c4ff\`.
- H branch exact Head reviewed: \`session-h-bmcp-protocol@b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9\`.
- H schema Blob: \`2ce8776ca5ee5e014b234dc3eb34a7cb7961e608\`.
- H validator Blob: \`8febb915ec321cc37cf159b2f5b917a3f945726c\`.
- H tests Blob: \`77cb66b895c5293a2f4883b1d5cb69775e71d00c\`.
- H hardening addenda: Phase 3.8.25 Blob \`4c220e998fc6ba700157598b0384dc3134cf8575\`; Phase 3.8.26 Blob \`9ff4ac5b64b354f63add21a5d16d37da46835c07\`.
- C source schema Blob: \`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda\`; C vector Blob \`c447f8c2908469c52cb52a448101495a331277c5\`.
- H exact CI: run \`44181762581\` SUCCESS, 29/29 Applied Delivery Evidence tests; run \`44180835611\` SUCCESS, semantic-and-wire tests.
- Disposition: **ACCEPT AS CANDIDATE CONSUMER SHAPE WITH ENUMERATED CONDITIONS; FULL APPLIED NOT ACCEPTED; G PERSISTENCE NOT IMPLEMENTED**.

## 1. Decision scope

This decision evaluates H's separate \`APPLIED_DELIVERY_EVIDENCE_RECORDED\` 1.0.0 message family as a candidate input to G. It does not modify Unified 1.2.15 C Provider Outcome Gateway Attestation or the JF-10 Applied ACK 1.1.0 schema family. Those are separate evidence/message families.

G owns the unique durable Applied decision. H may provide authenticated delivery/Adapter/Runtime evidence; C remains sole authority for provider handoff outcome; I remains sole authority for authorization; D remains sole authority for ForgetFence; COC/Storage remain sole authorities for their transaction and same-GID outcomes.

This delegated review is a successor candidate decision only. It does not silently amend G Phase 3.8.22 or transfer production authority.

## 2. Candidate identity acceptance

G accepts the following H identity projections as distinct candidate identities:

- \`HDeliveryBindingIdentity\` = (\`adapter_instance_ref\`, \`runtime_session_ref\`, \`delivery_id\`, \`delivery_attempt_id\`, \`inference_request_id\`, \`final_request_boundary_id\`, \`adapter_capability_epoch\`).
- \`HEvidenceIdentity\` = (\`HDeliveryBindingIdentity\`, \`evidence_kind\`).
- \`HObservationRecordIdentity\` = (\`issuer_ref\`, \`sender_authority_ref\`, \`sender_subject_ref\`, \`message_id\`, \`message_nonce\`, \`signing_sequence_namespace_ref\`, \`signing_record_sequence\`).

These are not substitutes for one another and none is G's Applied idempotency key. G's Applied identity/evidence revision must additionally bind exact ContextVersion, Delivery attempt, InferenceRequestId, FinalRequestBoundaryId, COutcomeRecordIdentity, C provider attempt/request digest, COC participant/transaction, I and D proofs, Storage same-GID outcome, and the aggregate EvidenceSetDigest.

H's exact 1.0.0 schema contains all seven HDeliveryBindingIdentity fields and all seven HObservationRecordIdentity fields. The new family is correctly kept separate from Unified 1.2.15 and JF-10 Applied ACK.

## 3. Candidate CSubmitOutcome join acceptance

The Phase 3.8.26 H reference validator now:
1. resolves H \`c_submit_outcome_ref\` through an injected C record resolver;
2. requires the resolved record to expose C \`issuer_authority_ref\`, \`sequence_namespace_ref\`, \`record_ref\`, \`record_sequence\`, \`payload_digest\` and \`FinalRequestBoundaryRef\`;
3. calls a separate tri-state C record authentication/validation callback;
4. enforces exact equality of H/C record ref, record sequence, payload digest and final request boundary;
5. compares \`ActualInferenceRequestId\` when the C record supplies it;
6. fails closed when the resolver or C verifier is unavailable.

The exact H suite consumes C's CPO-01 accepted fixture and tests negative mutations for record ref, sequence, payload digest, final boundary and optional ActualInferenceRequestId. This is sufficient to accept the **field-mapping algorithm as a reference candidate**, not the live C authority.

**Conditions**
- The resolver must return the exact immutable C record named by \`c_submit_outcome_ref\`; no display-name, caller-supplied payload or arbitrary URI substitution.
- C authentication must verify the C signature/profile, issuer authority, sequence namespace, immutable record identity, append-only Owner Ledger inclusion and schema semantics. H signer identity/sequence must never substitute for C identity.
- Resolver/verifier False => INVALID; unavailable/exception/None => UNKNOWN; UNKNOWN cannot be promoted to Full Applied.
- C \`Outcome\` and \`SideEffectStatus\` remain C-owned. H does not reinterpret them. G Full Applied requires a determinate \`HANDOFF_ACCEPTED\` with \`PROVEN_OCCURRED\` and all required provider/participant evidence; UNKNOWN/IN_DOUBT/rejected/not-invoked cannot qualify.
- For Full Applied, G requires the C record to carry an exact \`ActualInferenceRequestId\` matching H \`inference_request_id\`. If absent, the evidence may remain a valid H observation but G Full Applied is UNKNOWN/INELIGIBLE.
- G must independently bind C \`RequestDigest\` and provider-attempt lineage to the exact G request, Context/Delivery and COC transaction. H 1.0.0 does not duplicate RequestDigest and does not replace this G join.

## 4. Duplicate-key and replay-disclosure conditions

The exact H head adds duplicate-member rejection using an object-pairs hook and tests top-level/nested duplicate JSON members. It also requires a tri-state current replay authorization callback before disclosing \`original_result_ref\`; denied => INVALID, unavailable/exception => UNKNOWN with no result ref.

The exact H candidate CI passed 29/29 tests. The current H code uses two independent callbacks, `verify_current_i_replay_authorization` and `verify_current_d_forget_fence`, and tests denial/UNKNOWN/exception for both. This addresses the previously observed reference-validator behavior, but the production conditions remain open:
- The callback must be wired to the real I authorization/PermissionEpoch and key-status authorities, audience/scope checks, and applicable D ForgetFence authority.
- No result reference may be disclosed before current authorization is confirmed.
- H must use the approved production raw-byte parser/canonicalization/signature profile; the local sorted-key JSON test canonicalizer is not a production cryptographic profile.
- Durable replay reservation/result persistence, crash recovery and runtime Adapter integration are not proven by callback tests.

## 5. G Full Applied predicate remains unchanged

H evidence can only be one component of G's evidence revision. It cannot itself create G Applied.

Before Full Applied, G must validate, for the same request and causal transaction:
1. C's immutable authenticated CSubmitOutcome and determinate successful provider handoff.
2. H's authenticated observation and exact delivery/request/boundary binding.
3. COC terminal proof, complete recovery batch and owner high-water evidence.
4. I authorization/receipt-consumption terminal evidence and D complete-lineage ForgetFence evidence, independently authenticated and correctly ordered.
5. Where JF-10 applies, Storage same-GID terminal resolution and exact VisibilityPointer/PublicationReceipt or non-publication outcome.
6. G ContextVersion, Delivery attempt, Scope/Environment, managed-region digest, identity/session/capability, currentness and invalidation predicates.
7. G's own durable Applied identity, evidence revision, uniqueness and commit receipt.

UNKNOWN in any required authority remains UNKNOWN; no weaker receipt combination may be promoted to Full Applied.

## 6. Remaining blockers

| ID | Owner | Required work | Status |
|---|---|---|---|
| G-ADE-01 | H/I/D | Wire replay recheck to real I/D authorities and production trust registry | OPEN |
| G-ADE-02 | H/C | Implement live immutable C resolver and C Owner Ledger/signature verification | OPEN |
| G-ADE-03 | C/G | Decide whether ActualInferenceRequestId is mandatory in C records for all Full Applied profiles; absent => no Full Applied pending decision | OPEN |
| G-ADE-04 | G | Publish machine-readable Applied schema/SDK, stable identity key, unique index and atomic durable commit contract | OPEN |
| G-ADE-05 | G | Implement crash/restart, multi-replica duplicate, stale restore and high-water regression tests | OPEN |
| G-ADE-06 | C/G/H/I/D/COC/Storage | Exact review of the same successor artifact pins and owner-specific boundaries | OPEN |
| G-ADE-07 | Independent reviewer | Re-read final heads and verify no unreviewed source drift | OPEN |

G Phase 3.8.22 §10 still lists G-AP-P01..P18 as SPECIFIED / NOT RUN. This successor consumer decision does not convert them to PASS. The two reference models published through PR #114 are in-memory models, not G persistence implementation.

## 7. Final disposition

- H Applied Delivery Evidence 1.0.0 identity shape: **ACCEPTED AS CANDIDATE**.
- H CSubmitOutcome resolver/equality algorithm: **ACCEPTED AS REFERENCE CANDIDATE WITH CONDITIONS**.
- H duplicate-key and replay-disclosure reference hardening: **CANDIDATE CI PASS 29/29**.
- Production H trust/replay/C resolver: **NOT VERIFIED**.
- G exact H 1.0.0 consumer semantics: **DELEGATED G-ROLE CANDIDATE ACCEPTANCE ONLY; REAL OWNER ACCEPTANCE REQUIRED**.
- G durable Applied persistence/restore: **NOT IMPLEMENTED / NOT VERIFIED**.
- Full Applied: **NOT ACCEPTED / NOT PROVEN**.
- Global C/G/H freeze and production activation: **NO / NOT AUTHORIZED**.

---

## 8. 中文完整决议

### 8.1 决议范围

本决议审查 H 独立的 \`APPLIED_DELIVERY_EVIDENCE_RECORDED\` 1.0.0 消息族能否作为 G 的候选输入。它不修改 Unified 1.2.15 C Provider Outcome Gateway Attestation，也不修改 JF-10 Applied ACK 1.1.0；三者属于不同消息/证据族。

G 拥有唯一、持久化的 Applied 决议。H 提供已认证 Delivery/Adapter/Runtime 证据；C 仍是 Provider Handoff Outcome 唯一权威；I 仍是 Authorization 唯一权威；D 仍是 ForgetFence 唯一权威；COC/Storage 分别拥有自己的事务和 Same-GID Outcome 权威。

这是委托 G 角色的候选消费者决议，不是独立人类 G Owner 签署，不会静默修改 G Phase 3.8.22，也不转移生产权威。

### 8.2 候选身份接受

G 将以下三个 H 身份投影接受为彼此独立的候选身份：
- \`HDeliveryBindingIdentity\`：Adapter Instance、Runtime Session、Delivery、Attempt、InferenceRequest、FinalRequestBoundary、CapabilityEpoch 七元组。
- \`HEvidenceIdentity\`：HDeliveryBindingIdentity + evidence_kind。
- \`HObservationRecordIdentity\`：H Issuer、Sender Authority/Subject、Message ID/Nonce、Signing Namespace/Sequence 七元组。

三者不能互相替代，也都不是 G Applied 幂等键。G Applied identity/evidence revision 还必须绑定精确 ContextVersion、Delivery Attempt、InferenceRequestId、FinalRequestBoundaryId、COutcomeRecordIdentity、C Provider Attempt/RequestDigest、COC Participant/Transaction、I/D Proof、Storage Same-GID Outcome 和 EvidenceSetDigest。

H 1.0.0 Schema 已包含完整的 HDeliveryBindingIdentity 和 HObservationRecordIdentity，并正确地与 Unified 1.2.15 和 JF-10 Applied ACK 分离。

### 8.3 CSubmitOutcome 候选关联接受

H Phase 3.8.26 参考 Validator 现在通过注入 Resolver 解析 CSubmitOutcome，要求解析结果包含 C Issuer Authority、Sequence Namespace、Record Ref/Sequence、Payload Digest、FinalRequestBoundaryRef，并通过独立的 C Authentication/Validation Callback。之后精确比较 H/C Record Ref、Sequence、Payload Digest、Final Boundary；若 C 提供 ActualInferenceRequestId，也必须精确匹配。Resolver/Verifier 不可用时 fail-closed。

H 测试现在读取 C 的 CPO-01 Accepted Fixture，并对 Record Ref、Sequence、Payload Digest、Final Boundary 和可选 ActualInferenceRequestId 进行负向变异测试。这足以接受**字段映射算法作为参考候选**，但不等于接入真实 C 权威。

必要条件：
- Resolver 必须返回 \`c_submit_outcome_ref\` 所指向的同一不可变 C Record；不得使用显示名、调用方自带 Payload 或任意 URI 替代。
- C Authentication 必须验证 C Signature/Profile、Issuer Authority、Sequence Namespace、Immutable Record Identity、Append-only Owner Ledger Inclusion 和 Schema Semantics。H 的签名身份/序列绝不能代替 C 身份。
- Resolver/Verifier False 为 INVALID；不可用/异常/None 为 UNKNOWN；UNKNOWN 不得晋升为 Full Applied。
- C 的 Outcome/SideEffectStatus 仍由 C 决定。H 不解释或改写。G Full Applied 仅允许确定的 \`HANDOFF_ACCEPTED\` + \`PROVEN_OCCURRED\`，并满足 Provider/Participant 证据；UNKNOWN/IN_DOUBT/Rejected/Not Invoked 均不得满足。
- Full Applied 必须有 C 的精确 ActualInferenceRequestId 与 H InferenceRequestId 匹配。缺失时可以保留为 H Observation，但 G Full Applied 必须 UNKNOWN/INELIGIBLE。
- G 必须独立把 C RequestDigest/Provider Attempt Lineage 绑定到精确 G Request、Context/Delivery 和 COC Transaction。H 1.0.0 未复制 RequestDigest，不能代替 G 的关联。

### 8.4 Duplicate Key 与 Replay Disclosure 条件

H 最新 Head 增加了 object-pairs hook，在 Schema/P0 验证前拒绝顶层和嵌套重复 JSON 键；并在披露 \`original_result_ref\` 前强制执行 Tri-state Current Replay Authorization。拒绝为 INVALID，不可用/异常为 UNKNOWN，二者都不得披露 Result Ref。

精确 H 候选 CI 已通过 29/29。但生产条件仍未关闭：
- Callback 必须接入真实 I Authorization/PermissionEpoch/Key Status、Audience/Scope 和适用 D ForgetFence 权威。
- 当前授权通过前不得披露任何 Result Ref。
- 生产 Raw-byte Parser/Canonicalization/Signature Profile 必须由 H/I 批准；本地 Sorted-key JSON 测试 Canonicalizer 不是生产密码学档案。
- Durable Replay Reservation/Result Persistence、Crash Recovery 和 Runtime Adapter Integration 尚未证明。

### 8.5 G Full Applied Predicate 不变

H Evidence 只是 G Evidence Revision 的一个组成部分，不能自己创建 G Applied。Full Applied 仍要求同一 Request/Causal Transaction 的 C Provider Outcome、H Delivery/Request Binding、COC Terminal/Recovery Batch、I/D 权威证据、Storage Same-GID Outcome，以及 G 自身 Context/Delivery/Scope/Region/Identity/Currentness 和 Durable Applied Ledger 全部通过。

任一必需权威 UNKNOWN，整体保持 UNKNOWN；不得将多个较弱 Receipt 组合晋升为 Full Applied。

### 8.6 最终状态

- H Applied Delivery Evidence 1.0.0 身份结构：**候选接受**。
- H CSubmitOutcome Resolver/Equality：**参考候选有条件接受**。
- H Duplicate Key / Replay Disclosure 参考加固：**候选 CI 29/29 PASS**。
- 生产 H Trust/Replay/C Resolver：**NOT VERIFIED**。
- G 对 H 1.0.0 的精确消费者语义：**委托 G 角色候选接受；仍需真实 Owner 接受**。
- G Durable Applied Persistence/Restore：**NOT IMPLEMENTED / NOT VERIFIED**。
- Full Applied：**NOT ACCEPTED / NOT PROVEN**。
- 全局 C/G/H Freeze 和生产激活：**NO / NOT AUTHORIZED**。


## 9. Current H-head and C/G consumer recheck — 2026-11-18

The H branch has advanced from the exact snapshot reviewed by this delegated G-role decision (`b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9`) to current H HEAD `b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9`.

Current H pins:
- Schema: `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`
- Validator: `8febb915ec321cc37cf159b2f5b917a3f945726c`
- Tests: `77cb66b895c5293a2f4883b1d5cb69775e71d00c` (29 test methods)
- C join addendum: `9ff4ac5b64b354f63add21a5d16d37da46835c07`
- Hardening addendum: `4c220e998fc6ba700157598b0384dc3134cf8575`

The current H code separates replay disclosure checks into two independent callbacks: I current authorization/PermissionEpoch/key/principal/audience/scope, and D current ForgetOperation/Fence/lineage. Each is tri-state and both must pass before returning `original_result_ref`. The H validator also contains the reference C resolver and exact field mapping.

The exact CI evidence in this decision (29/29, run `44181762581`) is for the earlier H head `9fb2097...`, not current H head `b14e388...`. The current 29-test suite has no verified exact-head run in this review. This G-role decision remains a delegated candidate consumer acceptance only; it is not a real G Owner signature, production integration acceptance or G persistence proof.

H 分支已从本委派 G 角色决议审查的精确快照 `9fb2097...` 前进至当前 Head `b14e388...`。当前 H Validator 已将 Replay Disclosure 检查拆分为两个独立 Callback：I 当前授权/PermissionEpoch/Key/Principal/Audience/Scope，以及 D 当前 ForgetOperation/Fence/Lineage。二者均为 Tri-state，必须同时通过后才能返回 `original_result_ref`。H Validator 也包含 C Resolver 和精确字段映射参考实现。

本决议引用的 29/29 CI Run `44181762581` 属于旧 H Head `9fb2097...`，不是当前 `b14e388...`。当前 29 项测试尚无本审查可核实的精确 Head Run。因此本 G 角色决议仍仅为委派候选消费者接受，不是真实 G Owner 签名、生产集成验收或 G 持久化证明。


## 10. Current H/C source refresh — 2026-11-18

This append-only refresh replaces stale source pins for the candidate consumer review. It does not broaden the decision or turn delegated G-role work into a real Owner signature.

### Exact current source pins

- G Owner branch HEAD observed: `2c53a9d872ad4d57d99bd24a860ca695b9e3a661`.
- H Owner branch HEAD observed: `4386f67a61f7968da4c3603f28cc8a5100714f9f`.
- C Owner branch HEAD observed: `9e18e9065377f291b01536c383fcf4a7aecb9971`.
- H Applied Delivery Evidence 1.0.0 schema Blob: `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`.
- H validator Blob: `43f402e4a09034da197ac24856cddbd496c9c75f`.
- H conformance tests Blob: `98242cc193a77b27d58b39353ccc031201992614`.
- H hardening addendum Blob: `4c220e998fc6ba700157598b0384dc3134cf8575`.
- H CSubmitOutcome join addendum Blob: `9ff4ac5b64b354f63add21a5d16d37da46835c07`.
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`.
- CSubmitOutcome 1.0.1 vector Blob: `c447f8c2908469c52cb52a448101495a331277c5`.
- C delegated exact review of H resolver binding / 30-test head: C Phase 3.8.29 Blob `ef90613b19b857c9436bab86b8b42c26a54bdda8`.
- Earlier C delegated join review: C Phase 3.8.28 Blob `7ae8f2609a8786c4a5a715a270faa706156ed462`.

The H schema/validator/test/addendum Blobs on current H Owner branch `4386f67...` are byte-identical to the current-main Blobs read in the same refresh. H's code files did not change in the final H branch successor commit; that commit adds the Chinese Unified 1.2.15 structural-conformance document.

### Exact CI scope

- H exact code Head reviewed by C Phase 3.8.29: `4c16410f8b20b8fc2bc8c7609eb7bf07d83f317e`.
- H exact CI run [#44187702465](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187702465): SUCCESS, 30/30.
- The exact schema, validator and test Blobs from that 30-test Head match the current H Owner branch Blobs listed above.
- This is code-blob equivalence plus exact-Head CI on `4c16410...`; it is not a claim that CI ran on the later documentation-only H branch HEAD `4386f67...`.
- C Phase 3.8.29 is a delegated C-role review, not an independent human C Owner signature. It accepts the immutable C record field-mapping algorithm as a reference candidate with conditions only.

### C 1.0.1 semantics that G must preserve

The current C 1.0.1 schema requires `sequence_namespace_ref` and carries `ActualInferenceRequestId` as an optional property (it is not in the schema's required array). The C Phase 3.11.1 sequence-namespace amendment is PROPOSED, not a production trust/ledger registration.

For G Full Applied:
1. The H resolver result must be the exact C record named by H `c_submit_outcome_ref`; H exact reference, sequence, payload digest and FinalRequestBoundary equality checks are reference-code candidate behavior only.
2. C's `Outcome` and `SideEffectStatus` remain C-owned. G may consider Full Applied only for determinate `HANDOFF_ACCEPTED` + `PROVEN_OCCURRED` with all required ProviderRequest/Receipt and participant evidence.
3. Because C schema 1.0.1 does not require `ActualInferenceRequestId`, absence cannot be silently treated as an exact C/H request join. Under this G candidate predicate, absent ActualInferenceRequestId means H observation may be retained but Full Applied remains UNKNOWN / INELIGIBLE until an authorized C/G profile decision provides an independently proven exact request binding.
4. G must join C `RequestDigest`, ProviderAttempt identity/generation and C causal/COC participant lineage to the exact G request and Applied evidence revision. H's 1.0.0 message does not replace those joins.

### Updated disposition

- H/C field-mapping algorithm: ACCEPTED AS REFERENCE CANDIDATE WITH CONDITIONS (delegated C/G role reviews only).
- H 30/30 exact-code-head reference conformance: PASS on run #44187702465; current H code Blobs match.
- Live C resolver, C Owner Ledger inclusion/high-water, real C signer/profile trust and production sequence namespace: NOT IMPLEMENTED / NOT VERIFIED.
- I PermissionEpoch/key/audience/scope and D ForgetFence callbacks: not live authority integrations.
- G durable Applied schema/SDK/unique index/atomic commit/crash-restore/multi-replica behavior: NOT IMPLEMENTED / NOT VERIFIED; G-AP-P01..P18 remain SPECIFIED / NOT RUN.
- Full Applied: NOT ACCEPTED / NOT PROVEN.
- Global C/G/H freeze and production activation: NO / NOT AUTHORIZED.

---

## 11. 中文：H/C 当前来源刷新 — 2026-11-18

本追加记录刷新候选消费者审查的过期来源 Pin，不扩大原决议范围，也不把委派 G 角色工作转化为真实 Owner 签名。

### 精确当前来源

- G Owner 分支 HEAD：`2c53a9d872ad4d57d99bd24a860ca695b9e3a661`。
- H Owner 分支 HEAD：`4386f67a61f7968da4c3603f28cc8a5100714f9f`。
- C Owner 分支 HEAD：`9e18e9065377f291b01536c383fcf4a7aecb9971`。
- H Applied Delivery Evidence 1.0.0 Schema Blob：`2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`。
- H Validator Blob：`43f402e4a09034da197ac24856cddbd496c9c75f`。
- H Conformance Tests Blob：`98242cc193a77b27d58b39353ccc031201992614`。
- H Hardening Addendum Blob：`4c220e998fc6ba700157598b0384dc3134cf8575`。
- H CSubmitOutcome Join Addendum Blob：`9ff4ac5b64b354f63add21a5d16d37da46835c07`。
- CSubmitOutcome 1.0.1 Schema Blob：`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`。
- CSubmitOutcome 1.0.1 Vector Blob：`c447f8c2908469c52cb52a448101495a331277c5`。
- C 对 H Resolver Binding / 30 项测试 Head 的委派精确审查：C Phase 3.8.29 Blob `ef90613b19b857c9436bab86b8b42c26a54bdda8`。
- C 较早的 Join 委派审查：C Phase 3.8.28 Blob `7ae8f2609a8786c4a5a715a270faa706156ed462`。

同一轮读取确认，当前 H Owner 分支 `4386f67...` 上的 Schema/Validator/Tests/Addendum Blob 与当前 main 的对应 Blob 完全相同。H 分支最后的后继提交仅增加 Unified 1.2.15 结构符合性中文文档，未改变上述代码文件。

### 精确 CI 范围

- C Phase 3.8.29 审查的 H 精确代码 Head：`4c16410f8b20b8fc2bc8c7609eb7bf07d83f317e`。
- H 精确 CI Run [#44187702465](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187702465)：SUCCESS，30/30。
- 该 30 项测试 Head 的 Schema、Validator、Tests Blob 与当前 H Owner 分支列出的 Blob 一致。
- 这证明代码 Blob 等价且该精确代码 Head 的 CI 通过；不能声称 CI 直接运行在后续仅修改文档的 H 分支 HEAD `4386f67...` 上。
- C Phase 3.8.29 是委派 C 角色审查，不是独立人类 C Owner 签名。它仅有条件地接受不可变 C Record 字段映射算法作为参考候选。

### G 必须保留的 C 1.0.1 语义

当前 C 1.0.1 Schema 将 `sequence_namespace_ref` 设为必需字段；`ActualInferenceRequestId` 虽有属性定义，但不在 Schema 的 required 数组中。C Phase 3.11.1 Sequence Namespace 修订仍为 PROPOSED，不等于生产 Trust/Ledger 注册。

对于 G Full Applied：
1. H Resolver 返回的必须是 H `c_submit_outcome_ref` 所指向的同一 C Record；H 的精确引用、Sequence、Payload Digest 和 FinalRequestBoundary 相等检查目前仅是参考代码候选行为。
2. C 的 `Outcome` 和 `SideEffectStatus` 仍归 C 所有。G 只有在确定的 `HANDOFF_ACCEPTED` + `PROVEN_OCCURRED`，并具备全部必要 ProviderRequest/Receipt 和 Participant Evidence 时才可评估 Full Applied。
3. 因 C 1.0.1 Schema 并未要求 `ActualInferenceRequestId`，缺失时不得静默视为 C/H Request 精确关联。按当前 G 候选 Predicate，缺失时可保留 H Observation，但 Full Applied 必须保持 UNKNOWN / INELIGIBLE，直至经授权的 C/G Profile 决议提供独立证明的精确 Request 绑定。
4. G 必须把 C `RequestDigest`、ProviderAttempt Identity/Generation 和 C Causal/COC Participant Lineage 关联到精确 G Request 与 Applied Evidence Revision。H 1.0.0 消息不能替代这些 Join。

### 更新后的结论

- H/C 字段映射算法：有条件接受为参考候选（仅委派 C/G 角色审查）。
- H 30/30 精确代码 Head 参考符合性：Run #44187702465 PASS；当前 H 代码 Blob 一致。
- 真实 C Resolver、C Owner Ledger Inclusion/High-water、真实 C Signer/Profile Trust 和生产 Sequence Namespace：NOT IMPLEMENTED / NOT VERIFIED。
- I PermissionEpoch/Key/Audience/Scope 与 D ForgetFence Callback：尚未接入真实权威服务。
- G Durable Applied Schema/SDK/Unique Index/Atomic Commit/Crash-Restore/Multi-replica：NOT IMPLEMENTED / NOT VERIFIED；G-AP-P01..P18 仍 SPECIFIED / NOT RUN。
- Full Applied：NOT ACCEPTED / NOT PROVEN。
- 全局 C/G/H Freeze 和生产激活：NO / NOT AUTHORIZED。


## 12. H Unified 1.2.16 / 1.2.17 recovery-owner snapshot successor — separate from Applied Evidence 1.0.0

H has added a separate COC/JF-10 Unified schema family successor. Do not conflate it with H Applied Delivery Evidence 1.0.0:
- Unified 1.2.16 schema Blob: `91c4fd70cb1e1cff76d733baa180325bd2da84c1`.
- Unified 1.2.17 schema Blob: `1b8f44675f30919764481d33755c566ef5cf1ea8`.
- H 1.2.17 owner-gate semantic reference validator Blob: `60cd1b686eaa9ac364c69a708353fa0e5f635197`.
- H 1.2.17 semantic tests Blob: `24d3cf0730a138f25719cb1e29de28f833a00cdf`.
- Exact H code Head `f08dadd27b743b2a31fce859d6ed2c438438d1e1`; Recovery Cutoff run #44193331446 SUCCESS, 390 tests, 22 skipped.

H 1.2.16 adds distinct I/D/C owner-specific snapshot high-waters:
- I: `permission_epoch`, `producer_domain_inventory_epoch_ref`, receipt issue/consume high-waters, registry snapshot digest and relevant entry-set root.
- D: `forget_fence_generation_high_water`, `dependency_closure_cursor`, `dependency_closure_root`, plus producer/work/attempt and barrier high-waters.
- C: `provider_idempotency_namespace_ref`, `final_request_boundary_generation`, plus reservation/provider-attempt/provider-outcome high-waters.
- Common: `scope_generation_ref`, separate from OwnerGateGeneration.

The original I conditional alias defect (`inventory_epoch_ref` vs `producer_domain_inventory_epoch_ref`) was corrected and actual I/D/C Owner Snapshot instances are now tested. This proves H schema structure only.

### G consumer constraints

1. G must preserve the authority split: I PermissionEpoch and ProducerDomainInventoryEpoch are I-owned; D ForgetFenceGeneration and dependency closure are D-owned; C provider idempotency namespace and final-request-boundary generation are C-owned. G may not mint, compare across domains or infer these values.
2. A G recovery/Applied consumer must bind the exact owner snapshot reference/digest/attestation/root and ScopeGeneration to the same Batch/Manifest pair before using any owner release.
3. The C final-request-boundary generation is a new C snapshot field. C's current CSubmitOutcome 1.0.1 schema does not define it; do not treat it as already C-approved or as a substitute for FinalRequestBoundaryRef, RequestDigest, ActualInferenceRequestId or C ProviderAttempt lineage.
4. H 1.2.17 semantic validator now checks exact Batch↔Manifest backlink, ManifestId/content digest/prefix/count/root equality, Batch-before-Manifest order, and exact owner snapshot equality across Batch and Manifest roots. It remains a test-profile reference with injected signature, COC proof and currentness callbacks.
5. G's own SQLite Applied model remains a separate 17-test local reference model (run #44188852578). Neither H's 390-test suite nor G's 17-test suite proves production Owner Ledger, COC quorum, PostgreSQL/Storage, multi-replica or physical JF-10 behavior.

**G disposition:** H Unified 1.2.16/1.2.17 is a separate candidate consumer dependency. G's owner-specific field semantics require exact C/D/I owner acceptance and Storage successor-manifest binding before G can consume them as normative recovery evidence. No G Applied or current-use acceptance is implied.

---

## 13. 中文：H Unified 1.2.16 / 1.2.17 Recovery Owner Snapshot 后继 — 与 Applied Evidence 1.0.0 分离

H 新增了独立的 COC/JF-10 Unified Schema Family 后继，不得与 H Applied Delivery Evidence 1.0.0 混淆：
- Unified 1.2.16 Schema Blob：`91c4fd70cb1e1cff76d733baa180325bd2da84c1`。
- Unified 1.2.17 Schema Blob：`1b8f44675f30919764481d33755c566ef5cf1ea8`。
- H 1.2.17 Owner Gate Semantic Reference Validator Blob：`60cd1b686eaa9ac364c69a708353fa0e5f635197`。
- H 1.2.17 Semantic Tests Blob：`24d3cf0730a138f25719cb1e29de28f833a00cdf`。
- H 精确代码 Head `f08dadd...`；Recovery Cutoff Run #44193331446 SUCCESS，390 项，22 项 skipped。

H 1.2.16 新增不同 Owner 的专属 Snapshot High-water：
- I：`permission_epoch`、`producer_domain_inventory_epoch_ref`、Receipt Issue/Consume High-water、Registry Snapshot Digest、Relevant Entry-set Root。
- D：`forget_fence_generation_high_water`、`dependency_closure_cursor`、`dependency_closure_root`，以及 Producer/Work/Attempt 与 Barrier High-water。
- C：`provider_idempotency_namespace_ref`、`final_request_boundary_generation`，以及 Reservation/Provider Attempt/Provider Outcome High-water。
- 通用字段：`scope_generation_ref`，与 OwnerGateGeneration 分离。

原 I 条件别名缺陷（`inventory_epoch_ref` 与 `producer_domain_inventory_epoch_ref` 不一致）已修正，并新增真实 I/D/C Owner Snapshot 实例验证。但这只证明 H Schema 结构。

### G 消费约束

1. G 必须保留权威分离：I PermissionEpoch/ProducerDomainInventoryEpoch 归 I；D ForgetFenceGeneration/Dependency Closure 归 D；C Provider Idempotency Namespace/Final-request-boundary Generation 归 C。G 不得签发、跨域比较或推断这些值。
2. G Recovery/Applied Consumer 在使用 Owner Release 前，必须把精确 Owner Snapshot Ref/Digest/Attestation/Root 与 ScopeGeneration 绑定到同一 Batch/Manifest Pair。
3. C Final-request-boundary Generation 是新的 C Snapshot 字段。C 当前 CSubmitOutcome 1.0.1 Schema 未定义该字段；不得视为 C 已批准，也不得替代 FinalRequestBoundaryRef、RequestDigest、ActualInferenceRequestId 或 C ProviderAttempt Lineage。
4. H 1.2.17 Semantic Validator 现检查精确 Batch↔Manifest Backlink、ManifestId/Content Digest/Prefix/Count/Root 一致性、Batch 先于 Manifest，以及 Batch/Manifest 中 Owner Snapshot 精确一致。它仍是使用注入 Signature/COC Proof/Currentness Callback 的测试 Profile 参考实现。
5. G 自身 SQLite Applied Model 仍是独立的 17 项本地参考模型（Run #44188852578）。H 390 项测试和 G 17 项测试均不证明生产 Owner Ledger、COC Quorum、PostgreSQL/Storage、多副本或物理 JF-10。

**G 处置：** H Unified 1.2.16/1.2.17 是独立候选消费者依赖。G 要将这些字段作为规范 Recovery Evidence 消费，必须先获得精确 C/D/I Owner 接受，并由 Storage Successor Manifest 绑定。此更新不代表 G Applied 或 Current-use 接受。
