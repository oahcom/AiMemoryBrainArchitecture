# H Applied Delivery Evidence 1.0.0 — C/G/I 精确消费者映射审查

- Review ID: ABR-INTEGRATION-004
- H branch: `session-h-bmcp-protocol@6608cde89d959257db612d8ff8080f631333f3f3`
- H Schema Blob: `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`
- H Validator Blob: `2f6de24eea737cf75a16ead7495bea4627bb1bb4`
- H Phase 3.8.24 candidate report Blob: `f193113f142506b0d0848c7131f780db93a83aef`
- G Phase 3.8.22 contract Blob: `bd297873bc1e593280484a43cb44b56058d9c4ff`
- C Phase 3.8.23 identity review Blob: `4860c627b4d7e84e23fb39ad83411674f3b88c7b`
- CSubmitOutcome 1.0.1 Schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- Status: **Integration consumer review only; not C/G/I Owner acceptance**

## 1. 结论

H Applied Delivery Evidence 1.0.0 已正确把 Adapter Delivery Evidence 作为独立消息族，与 Unified 1.2.15 Gateway Attestation 分离；其 HDeliveryBindingIdentity 和 HObservationRecordIdentity 的字段形状与 G Phase 3.8.22 定义基本一致，且 Schema/Validator/11 项测试均已通过候选 CI。

但当前候选尚不能据此宣称 C/G/I 已接受完整线协议。仍有三个必须由责任 Owner 精确决定的映射问题：

1. H Schema 仅携带 C Submit Outcome / Outcome Record 的 opaque refs、record sequence 和 payload digest；没有把 G 所需的完整 CProviderAttemptIdentity / COutcomeRecordIdentity 展开为一等字段。H Validator 只有 `verify_c_final_boundary` callback，没有显式的 C Owner Ledger Record / C Outcome Identity binding callback。若 opaque refs 能唯一解析到已认证、不可变的 C Owner record，这种设计可能成立，但必须有精确 C 接受和 callback 规范。
2. `integrity_proof_ref` 是 Schema required 字段，却被排除在 H P0 签名/摘要投影之外；当前 Validator 也没有单独的 integrity-proof-reference verifier。必须明确该引用是否故意不可信/仅供提示，或通过签名/独立证明绑定它。
3. H `adapter_capability_epoch` 不等于 I `PermissionEpoch`。当前 H 1.0.0 Schema 没有 I PermissionEpoch 或 CommitAuthorizationReceipt 字段；G/I 必须明确授权证据由独立 I 记录通过 final boundary join，还是 H 消息需要携带经过认证的 I epoch/reference。禁止把 capability epoch 当成权限 epoch。

因此判定：**H 1.0.0 是可运行的 conformance candidate，但 C/G/I exact consumer mapping 仍 OPEN；Global Applied 仍 NOT FROZEN / NOT PROVEN。**

## 2. 已对齐的 H identity fields

### 2.1 HDeliveryBindingIdentity

H Phase 3.8.24 定义：
`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`

H Schema 将七个字段全部列入 required 和 properties：
- `adapter_instance_ref`
- `runtime_session_ref`
- `delivery_id`
- `delivery_attempt_id`
- `inference_request_id`
- `final_request_boundary_id`
- `adapter_capability_epoch`

这与 G Phase 3.8.22 的 HDeliveryBindingIdentity 字段集合一致。G 必须对这些字段的 issuer、scope、session binding、final boundary 和 capability epoch currentness 做 exact acceptance；H 的 Schema required 只证明字段存在，不证明字段值已被可信来源认证。

### 2.2 HEvidenceIdentity

`(HDeliveryBindingIdentity, evidence_kind)`

H Schema 的 `evidence_kind` 是 required 的封闭枚举，方向正确。新增 evidence kind 应是同一 delivery binding 下新的 evidence slot/revision，不得创建新的 DeliveryAttempt 或 G Applied identity。

### 2.3 HObservationRecordIdentity

H Phase 3.8.24 定义：
`(issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`

七个字段均在 H Schema 的 required/properties 中。Validator 将其作为 observation identity，并通过 `commit_observation` callback 处理 NEW / SAME_DIGEST_REPLAY / CONFLICT；但生产 durable uniqueness ledger 尚未实现。

## 3. C 身份映射未闭合

G Phase 3.8.22 的 C 身份合同：

- `CProviderAttemptIdentity = (issuer_authority_ref, sequence_namespace_ref, ProviderAttemptRef, ProviderAttemptGeneration, ProviderRef, ProviderAccountRef, IdempotencyNamespaceRef, IdempotencyKeyRef, RequestDigest)`
- `COutcomeRecordIdentity = (issuer_authority_ref, sequence_namespace_ref, record_ref, record_sequence)`

CSubmitOutcome 1.0.1 Schema 中这些字段均为 C-owned properties，且其中 issuer/namespace/record/attempt/provider/account/idempotency/request digest 有独立字段和类型约束。

H Applied 1.0.0 当前仅提供：
- `c_submit_outcome_ref`
- `c_outcome_record_ref`
- `c_outcome_record_sequence`
- `c_outcome_payload_digest`

H Schema 没有显式包含 C 的 issuer authority、sequence namespace、ProviderAttemptRef/generation、ProviderRef/account、IdempotencyNamespace/Key 或 RequestDigest。不能把 `c_outcome_payload_digest` 当作 `RequestDigest` 或 `OutcomeEvidenceDigest`；它们是不同证据/身份域。

### 可接受的两种实现路径（需要 C/G 明确选择）

**Option A — 完整 typed tuple：** H 1.0.1 successor 显式携带完整 CProviderAttemptIdentity 与 COutcomeRecordIdentity 所需字段，并在 H P0 中签名。

**Option B — opaque authenticated reference：** 保留 H 当前 ref 结构，但 C 必须定义 `c_submit_outcome_ref` / `c_outcome_record_ref` 的唯一性、issuer/namespace scope、版本、record sequence、payload digest、Owner signature/ledger inclusion 和不可变解析语义；H 的 C verifier callback 必须验证这些内容并返回 VALID/INVALID/UNKNOWN。单纯检查字符串非空不够。

当前 H Validator 的 `verify_c_final_boundary(envelope)` callback 可以由实现方扩展来做更多事，但其接口/报告没有明确规定它必须验证 C OutcomeRecordIdentity、CProviderAttemptIdentity、C Owner Ledger inclusion 和 C outcome payload digest。不得假设 callback 名称本身证明了这些检查。

## 4. C Final Request Boundary 精确交叉映射

H fields:
- `inference_request_id`
- `final_request_boundary_id`
- `final_request_boundary_type`
- `c_submit_outcome_ref`
- `c_outcome_record_ref`
- `c_outcome_record_sequence`
- `c_outcome_payload_digest`

CSubmitOutcome 1.0.1 fields:
- `ActualInferenceRequestId`
- `FinalRequestBoundaryRef`
- `FinalRequestBoundaryType`
- `RequestDigest`
- `Outcome`
- `payload_digest`
- `OutcomeEvidenceDigest`
- C owner/attempt/record identity fields

必须由 C Owner 对以下映射逐字段确认：
1. H `inference_request_id` 是否必须与 C `ActualInferenceRequestId` 相等，缺失/不适用时如何处理。
2. H `final_request_boundary_id` 如何绑定 C `FinalRequestBoundaryRef`，且 ref 类型/authority namespace 如何规范化。
3. H `final_request_boundary_type` 是否与 C 类型值一一映射，未知值如何 fail closed。
4. H `c_outcome_payload_digest` 精确指向 C `payload_digest` 还是另一个 digest；不得与 `RequestDigest`、`OutcomeEvidenceDigest` 混用。
5. 只有 C 确定性 `HANDOFF_ACCEPTED` 且 provider/participant evidence 完整时，H evidence 才可成为 G Full Applied 评估输入；UNKNOWN/IN_DOUBT/NOT_INVOKED/REJECTED 不可提升 Full Applied。

C Phase 3.8.23 只接受 G Phase 3.8.22 中 C-owned identity semantics，并明确 C/H wire interoperability NOT ACCEPTED / NOT VERIFIED；不能把该决议扩张解释为已接受 H 1.0.0。

## 5. H P0 Projection 的 Integrity Proof Reference 问题

H Validator：
- P0 excludes `payload_digest`、`signature`、`integrity_proof_ref`；
- `verify_signature` 接收 `envelope` 与 P0 bytes；
- 没有 `verify_integrity_proof_ref` callback；
- Schema 将 `integrity_proof_ref` 列为 required string。

这产生明确的规范问题：若该引用影响证据解释、完整性验证或后续取证，而它又不在签名 P0 中，则攻击者/中间层替换该引用不会改变 P0 digest。若它只是非权威提示，必须在规范中明确消费者不得信任它；若它是权威证据定位符，则应被签名绑定或由独立签名/不可变 ledger proof 绑定。

当前 11 项测试没有单独证明改变 `integrity_proof_ref` 会被拒绝或不会改变语义。要求 H 增加 mutation test 与 exact decision。

## 6. I PermissionEpoch 与 H CapabilityEpoch

- H `adapter_capability_epoch`：H/Adapter capability state namespace。
- I `PermissionEpoch`：I policy-domain authorization currentness namespace。
- 两者不可比较、转换或互相替代。

I Phase 3.6 确认要求受保护操作在不可逆 commit/disclosure 边界重新验证 PermissionEpoch；I Phase 3.8 receipt proposal 进一步要求单次消费的 CommitAuthorizationReceipt 与 D PublicationParticipantRef、StorageVisibilityParticipantRef 绑定。

H Applied 1.0.0 没有显式 PermissionEpoch / CommitAuthorizationReceipt field。G/I 必须确定：
- H evidence 是否只通过 authenticated final boundary reference 关联 I 的独立权威记录；
- 若是，H/G 验证器如何证明该 join 是 exact、current、同一 Scope/Actor/Audience/operation；
- 若需要 H 原样携带 PermissionEpoch，必须使用独立 typed field/ref，不能复用 `adapter_capability_epoch`。

## 7. 必须完成的精确消费者决议

| 责任方 | 必须确认 | 当前状态 |
|---|---|---|
| H | C opaque refs 的语义、C callback 完整检查、integrity_proof_ref 认证、生产 canonicalization/profile | OPEN |
| C | H 1.0.0 到 CSubmitOutcome 1.0.1 的 identity/final-boundary/digest 精确映射 | OPEN；3.8.23 只审了 G 的 C-owned tuple |
| G | HDeliveryBindingIdentity/HEvidenceIdentity/HObservationRecordIdentity 到 GAppliedIdentity 的 exact mapping、Full Applied predicate 与 durable evidence join | OPEN；3.8.22 是 design draft |
| I | PermissionEpoch/CommitAuthorizationReceipt 与 H delivery/final boundary 的关联及 trust profile | OPEN；3.8 技术合同仍 proposal |
| Storage/COC | H/C evidence references 如何与同一 GID/participant/terminal outcome 绑定 | OPEN |

## 8. 判定

- H schema shape：**CANDIDATE IMPLEMENTED**。
- H local validator/test suite：**BOUNDED CI PASS**。
- HDeliveryBindingIdentity / HEvidenceIdentity / HObservationRecordIdentity 字段形状：**STRUCTURALLY ALIGNED WITH G**。
- CProviderAttemptIdentity / COutcomeRecordIdentity 通过 opaque refs 的认证绑定：**UNRESOLVED**。
- `integrity_proof_ref` P0 排除语义：**UNRESOLVED / SECURITY REVIEW REQUIRED**。
- I PermissionEpoch join：**UNRESOLVED**。
- C/G/I exact consumer acceptance：**NOT FOUND**。
- Global Applied / Production activation：**NOT FROZEN / NOT AUTHORIZED**。

本审查是集成技术发现，不是 C/G/I Owner 决议，不修改 H/C/G/I Owner 分支，不授权 schema freeze、merge 或生产激活。


## 9. A-H-ADE-006 精确审查补充：三个 P0 阻断条件

A 的 PR #98 精确审查（Blob `44f79fc037a3aa15d171781fecf5a924e10a0388`）将 H Applied Delivery Evidence 1.0.0 判为 **DEFERRED — CANDIDATE IMPLEMENTATION WITH OPEN P0 CONDITIONS**，并登记：

### H-ADE-001 — Duplicate JSON object keys

当前 Validator 直接调用 `json.loads(raw_envelope.decode("utf-8"))`。Python 标准 decoder 会在 JSON Schema/P0 计算前折叠重复 object keys。必须在对象物化前拒绝顶层和嵌套重复 key，覆盖 identity、digest、signature、authority 字段，并增加负向向量。该项阻断认证生产使用。

### H-ADE-002 — CSubmitOutcome semantic join

H 当前只有 opaque C refs/sequence/digest 和 `verify_c_final_boundary` seam；没有明确规定如何解析并验证不可变 CSubmitOutcome 1.0.1 record 的：
- issuer / sequence namespace / COutcomeRecordIdentity；
- CProviderAttemptIdentity 与 successor lineage；
- `Outcome` / `SideEffectStatus`；
- `RequestDigest` / `ActualInferenceRequestId` / `FinalRequestBoundaryRef`；
- immutable record payload digest 与 Owner-ledger inclusion。

必须有 tri-state resolver/verifier，且由 C/G exact review。H 不得 mint C provider truth，G 不得仅凭 H evidence 产生 Full Applied。

### H-ADE-003 — Replay result disclosure 的 current authorization recheck

I Phase 3.8.23 要求 SAME_DIGEST_REPLAY 在返回原始 durable result 前重新检查当前 I Authorization/PermissionEpoch、key status、audience/scope 和适用 D Forget fence。H Validator 当前没有显式 current-authorization callback；`commit_observation` seam 未规定该回查。未完成前不得向已撤权或 stale caller 返回 `original_result_ref`。

### 额外集成问题：H-ADE-004 candidate — Integrity Proof Reference binding

本审查另发现 `integrity_proof_ref` 是 required field，却被排除在 P0 projection 外，且没有独立 verifier callback。该项是待 H Owner 决定的额外安全问题，不应冒充 A 已登记的 H-ADE-001..003。必须明确它是非权威 hint，还是需要签名/不可变 ledger proof 绑定；增加替换 mutation test。

## 10. C/I Gateway order reviews 的适用范围

- C Phase 3.8.27 Blob `3ca06dbfd7d59483e9604b7a68df924c719f60aa` 接受 C object schema/digest/signature/sequence namespace/provider evidence/semantics 先于 H Unified Gateway Attestation 签名，再进行 replay reservation 和 durable ingress acceptance 的顺序。
- I Phase 3.8.23 Blob `85cdbad04ae4b688338cdf2b667c21d2f02d8b96` 接受同一 gateway replay/durable ingress 顺序，并明确 SAME_DIGEST_REPLAY 必须重新检查当前授权、PermissionEpoch、key status、audience/scope 和 D Forget fence。
- 两项均是 delegated role review，且针对 H Unified 1.2.15 Gateway Attestation path。**它们不是 H Applied Delivery Evidence 1.0.0 的 C/G/I exact consumer acceptance**，但其 replay disclosure 约束对任何返回 prior result reference 的实现具有直接安全相关性。

