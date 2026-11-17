# Phase 3.8.23 — G Successor Consumer Decision: H Applied Delivery Evidence 1.0.0
# Phase 3.8.23 — G 后继消费者决议：H Applied Delivery Evidence 1.0.0

- Owner domain: G — ContextVersion, Delivery, Applied State and Reconciliation.
- Mode: delegated G-role exact consumer review under user instruction; **not an independent human G Owner signature**.
- G normative source: Phase 3.8.22 Blob \`bd297873bc1e593280484a43cb44b56058d9c4ff\`.
- H branch exact Head reviewed: \`session-h-bmcp-protocol@9fb2097905ef653b3a2048ac5f6804fc94178d8d\`.
- H schema Blob: \`2ce8776ca5ee5e014b234dc3eb34a7cb7961e608\`.
- H validator Blob: \`953de9274a3d711b8337333a595f0bf04efb02ec\`.
- H tests Blob: \`e1e81af3d25766c37ef95170dae868261eb5fb3e\`.
- H hardening addenda: Phase 3.8.25 Blob \`ca5cc6030471ac8107d7aaee652c18badc65edac\`; Phase 3.8.26 Blob \`9ff4ac5b64b354f63add21a5d16d37da46835c07\`.
- C source schema Blob: \`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda\`; C vector Blob \`c447f8c2908469c52cb52a448101495a331277c5\`.
- H exact CI: run \`44180835412\` SUCCESS, 26/26 Applied Delivery Evidence tests; run \`44180835611\` SUCCESS, semantic-and-wire tests.
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

The exact H candidate CI passed 26/26 tests. This addresses the previously observed reference-validator behavior, but the production conditions remain open:
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
- H duplicate-key and replay-disclosure reference hardening: **CANDIDATE CI PASS 26/26**.
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

精确 H 候选 CI 已通过 26/26。但生产条件仍未关闭：
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
- H Duplicate Key / Replay Disclosure 参考加固：**候选 CI 26/26 PASS**。
- 生产 H Trust/Replay/C Resolver：**NOT VERIFIED**。
- G 对 H 1.0.0 的精确消费者语义：**委托 G 角色候选接受；仍需真实 Owner 接受**。
- G Durable Applied Persistence/Restore：**NOT IMPLEMENTED / NOT VERIFIED**。
- Full Applied：**NOT ACCEPTED / NOT PROVEN**。
- 全局 C/G/H Freeze 和生产激活：**NO / NOT AUTHORIZED**。
