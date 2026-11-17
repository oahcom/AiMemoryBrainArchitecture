# Phase 3.8.23 — H 精确消费方决议与 G Applied Persistence Delivery Evidence Mapping

- 角色：模拟 H Owner 的委托审查；不是独立人类 Owner 签署或 I 安全注册。
- 决议：身份语义 **ACCEPT WITH ENUMERATED EXCEPTIONS**；**WIRE MAPPING NOT FROZEN**。
- G 目标 EN Blob：`bd297873bc1e593280484a43cb44b56058d9c4ff`
- G 目标 zh-CN Blob：`82553a47fae2d5e796e0742b46231afe465e75b2`
- H Unified 1.2.15 Schema Blob：`860fc4cec658db7d2703cd6adf72aa31a2723f6d`
- H Gateway Validator Blob：`9cc426d4c26deb452f39daff34c1008dd535e969`
- H Gateway Validator Tests Blob：`9a5051b001a6e59d7b71e6dd175e84bb7d01d252`
- H Adapter/Applied Attestation 合同 Blob：`74be8374a67da385a5f0f8e34c7aef2b38b72bcf`
- H Phase 3.8.21 精确映射说明 Blob：`2dc30f193d9c4f4bdc05ca4c137103687db28924`

## 1. 关键边界发现

Unified 1.2.15 与 `gateway_attestation_validator.py` 认证的是 H Gateway 对 `C_PROVIDER_OUTCOME_RECORDED` Envelope 的 Attestation，包括 Origin Transport Receipt、H Signing Sequence 及重复的 C Outcome 字段。这与 Adapter/Runtime Applied Delivery Evidence 不是同一消息/证据族。

Gateway Validator 的 P0 Allowlist 是显式列表，并拒绝未列出的字段。因此，不能在没有版本化 Profile/Schema Successor 和新向量的情况下，把 Adapter Delivery 字段追加到现有 P0 Projection；也不能把 H Gateway 的 `message_id/message_nonce/signing_record_sequence` 当作 Adapter Evidence Observation 的不可变身份。

H §11.1 候选映射已经列出 Delivery 字段，但该候选表本身不是 Unified 1.2.15 Schema，也不是可执行 Validator Mapping。此前 G 对完整 Delivery Tuple 未出现在 1.2.15 C Provider Outcome Branch 的观察仍然成立，并进一步澄清：字段虽在 H 候选文档中有描述，却没有接入精确 1.2.15 Message Schema/Validator 路径。

## 2. 逐字段决议

### 2.1 HDeliveryBindingIdentity — 接受为 H 所有的语义元组

`(adapter_instance_ref, runtime_session_ref, delivery_id, delivery_attempt_id, inference_request_id, final_request_boundary_id, adapter_capability_epoch)`

H 确认：
- `adapter_instance_ref`：精确 H 注册 Adapter Instance，而不只是 Adapter 产品/Build。
- `runtime_session_ref`：经认证的 Runtime Session Binding，不能仅凭 Transport Connection 推断。
- `delivery_id` + `delivery_attempt_id`：G 签发的 Delivery 与精确未被 Supersede 的 Attempt；H 只保留，不创建 G 身份。
- `inference_request_id`：Runtime/Provider 实际分配的 Request ID，绝不从 DeliveryId 合成。
- `final_request_boundary_id`：C 观察到的精确成功 Submit Boundary；H 不能签发或替代它。
- `adapter_capability_epoch`：H 签发的 Capability Epoch，绑定精确 Adapter Instance/Session 与协商 Profile。

Tier-1 Full Observation 的必要伴随字段包括 `runtime_instance_ref`、`adapter_ref`、`context_id`、`context_version`、`materialized_context_version`、`final_request_boundary_type`、精确 Request/Managed-Region Digest Profile、Coverage 与 Integrity References。这些是证据谓词；除非 G 显式版本化身份 Key，否则它们不是稳定 Delivery Key 的额外组件。

### 2.2 HEvidenceIdentity — ACCEPT

`(HDeliveryBindingIdentity, evidence_kind)`

`evidence_kind` 是由 H Evidence Profile 控制的封闭版本化 Enum。新增 Evidence Kind 是同一 Delivery Binding 下的新 Evidence Slot/Revision，不会创建新的 DeliveryAttempt 或 G Applied Identity。未知 Critical Kind 必须 Fail Closed。

### 2.3 HObservationRecordIdentity — 有条件 ACCEPT

`(issuer_ref, sender_authority_ref, sender_subject_ref, message_id, message_nonce, signing_sequence_namespace_ref, signing_record_sequence)`

它标识一条不可变、经认证的 H Observation，而非逻辑 Delivery。Issuer/Sender 字段必须是精确经验证解析的身份。Message ID + Nonce 提供 Envelope Replay Identity；Signing Sequence 仅在其 Namespace 和 Anti-Rollback Checkpoint 内有序。Timestamp 仅作描述。

相同 Observation Identity + 相同 Canonical H P0 Digest + 相同不可变 Receipt/Result Ref = 精确重放。相同 Observation Identity 但 Digest 或不可变元组变化 = Conflict/Quarantine。合法 Successor 必须使用新的 Observation Identity，并由经认证的 H Owner Ledger 明确链接到同一 HDeliveryBindingIdentity。

### 2.4 Digest 与 Replay 分离 — ACCEPT

H P0 Digest 是单条已签名 H Envelope 的内容完整性值，不属于 HDeliveryBindingIdentity、HEvidenceIdentity 或 GAppliedIdentity。Gateway Message Replay Ledger、Adapter Evidence Observation Ledger 与 G Applied Uniqueness Ledger 是不同幂等域。任何一层不得拿自己的 Replay Key 替代其他层的逻辑身份。

## 3. 精确 Schema/Validator 映射决议

H 不会修改不可变 Unified 1.2.15 Artifact，也不会原地扩大现有 C Provider Outcome P0 Allowlist。

正确的后继方案是独立版本化的 H Applied Delivery Evidence Message Family（候选 Schema ID：`bmcp.applied-delivery-evidence`，Artifact Revision：`1.0.0`），包含：
- 对每个 HDeliveryBindingIdentity 组件的必需类型化属性；
- 必需的 `evidence_kind` 与不可变 Observation Identity 字段；
- Authenticated Issuer/Sender、Signature Profile、Signing Sequence Namespace/Sequence、Message ID/Nonce、Audience 与 H P0 Digest/Signature；
- H 文档 §11.1–11.6 候选字段的精确映射；
- Strict Unknown-Critical-Field Rejection 与明确 Absent/Null 语义；
- 覆盖所有实际存在字段的 P0 Allowlist，唯一排除精确派生 Digest/Signature/Integrity Reference；
- 对 Schema Revision、Protected Identity Binding、Capability Epoch、C Final-Boundary Equality、G Delivery/Attempt Equality、Digest Integrity、Replay Conflict 与 Successor Lineage 的 Validator 检查。

这是一项规范性映射决议，不代表后继 Schema、Validator、SDK 或测试已经实现。H 必须在后续实现提交中提供精确 Artifact 路径、Blob SHA、P0 向量与 CI Run，才能将 Wire Mapping 标记为完成。

## 4. 明确例外与 Gate

1. H Unified 1.2.15 Gateway Validator 仅对当前 C Provider Outcome Gateway-Attestation 用途有效；不能推断它已接受 Adapter Delivery Evidence。
2. 独立 H Applied Delivery Evidence Schema/Validator 已完成设计说明，但**尚未实现/验证**。
3. C 必须审查重复字段及其与 CSubmitOutcome 1.0.1 的 Final-Boundary Equality；G 必须审查 Delivery/Context Binding；I 必须批准 Signer/Profile/Key Registry 与 Trust Roots。
4. H Gateway Message Replay、H Adapter Observation Replay 与 G Applied Idempotency 仍是三个不同的 Durable Ledger。
5. 本委托 H 角色审查不是独立人类 H Owner 批准、I 密码学注册、生产信任或部署 Durable Replay 证据。

## 5. 结论

**针对精确 G Phase 3.8.22 Blob，H 身份语义：ACCEPT WITH ENUMERATED EXCEPTIONS。H Delivery Evidence Wire Mapping：NOT FROZEN；后继 Schema/Validator 实现仍待完成。H 1.2.15 Gateway Attestation 保持独立范围。全局 Applied Freeze：NO。Production Activation：NOT AUTHORIZED。**
