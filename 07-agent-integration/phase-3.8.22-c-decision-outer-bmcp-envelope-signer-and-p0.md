# Phase 3.8.22 — C Decision Candidate: Outer BMCP Envelope Signer and Exact P0
# Phase 3.8.22 — C 决策候选：外层 BMCP Envelope 签署主体与精确 P0

- Owner perspective: C — Agent Integration / Provider Outcome Semantic Authority
- H gap contract: Phase 3.8.18 Blob `fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1`
- H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- Existing C object profile candidate: Phase 3.8.6 Blob `44641b4b01d721c47e08ae9380ffe645bb3ccda0`
- Existing C object projection: Phase 3.8.8 Blob `06d9264124d85896ccd44ef7789d9af245d8255b`
- Status: **C-ROLE DECISION CANDIDATE; EXACT ENVELOPE PROFILE PROPOSED; I CRYPTO GOVERNANCE / H WIRE MAPPING / STORAGE ACCEPTANCE REVIEW REQUIRED; NOT REGISTERED / NOT FROZEN**
- Provenance: delegated C-role decision candidate in the coordinating session; not an independent human C Owner signature.
- English and Chinese are normative peers.

## 1. C decision / C 决策

For `C_PROVIDER_OUTCOME_RECORDED`, **the C-owned provider adapter is the origin signer of the outer BMCP message envelope**, in addition to signing the immutable CSubmitOutcome object. These are two distinct signed objects and two distinct P0 projections.

H Gateway MUST NOT replace the C origin signature with a gateway signature. H may issue a separate gateway-ingress receipt/attestation after it authenticates the transport peer and verifies the C envelope, but that receipt has a distinct H issuer, distinct record type, distinct P0/profile and evidentiary meaning. It is additive, never a substitute for the C-origin signature.

For any non-C-originated BMCP message, this C decision does not apply; that message's owning authority decides its own signer.

对于 `C_PROVIDER_OUTCOME_RECORDED`，**C 自有 Provider Adapter 是外层 BMCP Message Envelope 的 Origin Signer**，并且还要独立签署不可变 CSubmitOutcome Object。这是两个不同的 Signed Object，具有两个不同的 P0 Projection。

H Gateway 不得用 Gateway Signature 替代 C Origin Signature。H 可以在认证 Transport Peer 并验证 C Envelope 后签发独立 Gateway-Ingress Receipt/Attestation，但其 Issuer、Record Type、P0/Profile 与证据含义均不同。该 Receipt 只能附加，不能替代 C Origin Signature。

本 C 决策不适用于非 C-originated BMCP Message；其他消息由其 Owner 决定签署主体。

## 2. Why two signatures / 为什么需要两份签名

### 2.1 CSubmitOutcome object signature

The immutable C object signature proves that the C authority signed the exact provider-outcome semantic record under the C object P0 contract. It is independent of message delivery, envelope nonce, audience and transport session.

### 2.2 Outer BMCP envelope signature

The outer C-origin signature proves that the C adapter emitted this exact message-family instance, with this message identity/nonce/audience, schema artifact revision, sender/issuer/subject, C object reference/digest, message-specific fields and proof references. It protects the delivery envelope against mutation, substitution and cross-message replay. It does not prove provider truth beyond the independently verified C object/evidence.

### 2.1 CSubmitOutcome Object Signature

不可变 C Object Signature 证明 C Authority 按 C Object P0 合同签署了精确 Provider-Outcome Semantic Record。它独立于 Message Delivery、Envelope Nonce、Audience 与 Transport Session。

### 2.2 外层 BMCP Envelope Signature

外层 C Origin Signature 证明 C Adapter 发出了这一精确 Message-Family Instance，并绑定 Message Identity/Nonce/Audience、Schema Artifact Revision、Sender/Issuer/Subject、C Object Ref/Digest、消息专属字段与 Proof Ref。它保护 Delivery Envelope，防止变异、替换与跨消息重放。但除独立验证的 C Object/Evidence 外，它不额外证明 Provider Truth。

## 3. New C envelope profile candidate / 新 C Envelope Profile 候选

This is a distinct profile; it MUST NOT reuse the C object profile or I profile by identifier or by projection.

| Item | Candidate |
|---|---|
| Profile bundle | `AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0` |
| Canonicalization | `RFC8785-JCS-1.0` constrained by RFC 7493 I-JSON |
| Digest | SHA-256 |
| Signature primitive | Ed25519 / RFC 8032 |
| Signature encoding | Canonical unpadded Base64url |
| Payload domain tag | ASCII `AIMBA-C-BMCP-ENVELOPE-PAYLOAD-v1` |
| Signature domain tag | ASCII `AIMBA-C-BMCP-ENVELOPE-SIGNATURE-v1` |
| Message family domain | Exact ASCII `C_PROVIDER_OUTCOME_RECORDED` |
| Signer authority | C Provider Adapter authority |
| Key identity | C-owned envelope-signing key reference + immutable version; exact key may equal or differ from object-signing key only if I-approved profile registration explicitly authorizes both uses |

The algorithm suite and canonicalization are **candidates only**. I must approve algorithm suitability, profile registry semantics, trust roots, key custody, revocation/history, compromise ordering and anti-rollback. C owns the message semantics and signer role. H owns the wire representation and exact implementation mapping. This document does not register a key or authorize production use.

这是独立 Profile；不得通过相同 Identifier 或 Projection 复用 C Object Profile 或 I Profile。

上述算法套件与 Canonicalization **仅为候选**。I 必须批准算法适用性、Profile Registry 语义、Trust Root、Key Custody、Revocation/History、Compromise Ordering 与 Anti-rollback。C 拥有消息语义与签署主体决策；H 拥有 Wire Representation 与精确实现 Mapping。本文件不注册 Key，也不授权生产使用。

## 4. Exact outer-envelope P0 allowlist / 外层 Envelope P0 精确白名单

The envelope P0 is built from the exact H Unified 1.2.14 `commonEnvelope` plus the `C_PROVIDER_OUTCOME_RECORDED` message-family fields. The C object remains separately dereferenced and verified.

### 4.1 Common envelope members included

Include every present member in this exact set:
- `schema_id`
- `schema_artifact_revision`
- `schema_version`
- `message_type`
- `message_id`
- `message_nonce`
- `audience`
- `sender_authority_ref`
- `sender_subject_ref`
- `issuer_ref`
- `subject_ref`
- `owner_authority`
- `owner_record_ref`
- `policy_domain_ref` when present
- `causal_order_profile_ref`
- `causal_order_coordinator_ref`
- `causal_order_domain_ref`
- `canonicalization_profile_id`
- `signature_profile_id`
- `digest_algorithm`
- `key_id_ref`
- `key_version`
- `created_at`
- `owner_signature_ref`
- `integrity_proof_ref`
- `channel_binding_proof_ref`

### 4.2 C message-family members included

Include every present member in this exact set:
- `c_submit_outcome_ref`
- `c_submit_outcome_digest`
- `provider_outcome`
- `provider_ref`
- `provider_adapter_ref`
- `provider_idempotency_key_ref`
- `provider_request_ref`
- `provider_receipt_ref`
- `actual_inference_request_id`
- `final_request_boundary_id`
- `request_digest`
- `transaction_ref`
- `participant_reservation_ref`
- `prepared_participant_ref`
- `prepare_attempt_ref`
- `prepare_attempt_generation`
- `participant_ledger_ref`
- `participant_ledger_version`
- `participant_tuple_digest`
- `i_terminal_decision_ref`
- `d_clearance_ref`
- `storage_resolution_proof_ref`
- `provider_outcome_evidence_ref`
- `provider_lookup_proof_ref`
- `provider_no_handoff_proof_ref`
- `not_invoked_proof_ref`
- `unknown_reason_ref`
- `owner_admission_ref`
- `owner_admission_digest`
- `owner_ledger_ref`
- `owner_ledger_version`
- `owner_local_sequence`
- `owner_high_water`
- `owner_ledger_root`
- `coc_participant_intent_ref` (null vs string is signed exactly)
- `coc_absence_reason` when present

The projection uses exact field presence and exact JSON values. Absent, null, empty string, empty array and empty object are distinct. No coercion, defaulting, Unicode normalization outside JCS, omission of unknown critical members or wildcard exclusion is permitted. Because H schema uses `unevaluatedProperties:false`, any new message field requires a schema/profile revision and a new exact projection review.

### 4.3 Exact exclusions

Exclude only:
- `payload_digest`: derived from P0;
- `signature`: signature output;
- `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, `coc_previous_entry_digest`: coordinator-appended COC record/quorum evidence, independently verified and joined to this signed C message;
- any transport-session secret/material that is not serialized as an envelope member. The serialized `channel_binding_proof_ref` and `integrity_proof_ref` are included in P0 (see below).

**Correction to legacy C Phase 3.8.6 projection:** that earlier candidate included an ambiguous mixed common-envelope/C-object field inventory and excluded integrity/channel-binding locators. This Phase 3.8.22 contract supersedes that ambiguity for the *outer envelope only*. The immutable C object P0 remains governed by its own exact schema/profile contract. Do not reinterpret either P0 as the other.

### 4.4 Integrity and channel-binding references

Include both `integrity_proof_ref` and `channel_binding_proof_ref` in the outer envelope P0 so an attacker cannot replace the proof locator without invalidating the signature. The referenced evidence must still be independently verified:
- integrity proof must be resolved against the authenticated signer/profile and exact envelope digest;
- channel-binding proof must be checked against protected transport/session verifier context outside the payload.
Signing a proof reference does not prove the proof itself.

### 4.1 Common Envelope 成员

包含以下精确集合中每个实际存在的成员：
- `schema_id`
- `schema_artifact_revision`
- `schema_version`
- `message_type`
- `message_id`
- `message_nonce`
- `audience`
- `sender_authority_ref`
- `sender_subject_ref`
- `issuer_ref`
- `subject_ref`
- `owner_authority`
- `owner_record_ref`
- 存在时的 `policy_domain_ref`
- `causal_order_profile_ref`
- `causal_order_coordinator_ref`
- `causal_order_domain_ref`
- `canonicalization_profile_id`
- `signature_profile_id`
- `digest_algorithm`
- `key_id_ref`
- `key_version`
- `created_at`
- `owner_signature_ref`

### 4.2 C 消息专属成员

包含以下精确集合中每个实际存在的成员：
- `c_submit_outcome_ref`
- `c_submit_outcome_digest`
- `provider_outcome`
- `provider_ref`
- `provider_adapter_ref`
- `provider_idempotency_key_ref`
- `provider_request_ref`
- `provider_receipt_ref`
- `actual_inference_request_id`
- `final_request_boundary_id`
- `request_digest`
- `transaction_ref`
- `participant_reservation_ref`
- `prepared_participant_ref`
- `prepare_attempt_ref`
- `prepare_attempt_generation`
- `participant_ledger_ref`
- `participant_ledger_version`
- `participant_tuple_digest`
- `i_terminal_decision_ref`
- `d_clearance_ref`
- `storage_resolution_proof_ref`
- `provider_outcome_evidence_ref`
- `provider_lookup_proof_ref`
- `provider_no_handoff_proof_ref`
- `not_invoked_proof_ref`
- `unknown_reason_ref`
- `owner_admission_ref`
- `owner_admission_digest`
- `owner_ledger_ref`
- `owner_ledger_version`
- `owner_local_sequence`
- `owner_high_water`
- `owner_ledger_root`
- `coc_participant_intent_ref`（必须精确签署 null 与 string 的区别）
- 存在时的 `coc_absence_reason`

Projection 使用精确 Field Presence 与 JSON Value。Absent、Null、Empty String、Empty Array、Empty Object 均不同。禁止 Coercion、Defaulting、JCS 之外的 Unicode Normalization、遗漏 Unknown Critical Member 或 Wildcard Exclusion。由于 H Schema 使用 `unevaluatedProperties:false`，任何新增消息字段都需要 Schema/Profile Revision 与新的精确 Projection Review。

### 4.3 精确排除项

仅排除：
- `payload_digest`：从 P0 派生；
- `signature`：签名输出；
- `coc_commit_proof_ref`、`coc_record_ref`、`coc_record_position`、`coc_entry_digest`、`coc_previous_entry_digest`：由 Coordinator 追加的 COC Record/Quorum Evidence，必须独立验证并 Join 回本 Signed C Message；
- 不作为 Envelope Member 序列化的 Transport Session Secret/Material。序列化的 `channel_binding_proof_ref` 与 `integrity_proof_ref` 纳入 P0（见下文）。

**对 C Phase 3.8.6 旧 Projection 的修正：** 旧候选混合了 Common Envelope/C Object 字段清单，并排除了 Integrity/Channel-Binding Locator。Phase 3.8.22 仅对*外层 Envelope*取代该歧义。不可变 C Object P0 仍由其自身精确 Schema/Profile 合同管理。不得将两种 P0 相互解释。

### 4.4 Integrity 与 Channel-Binding Reference

将 `integrity_proof_ref` 与 `channel_binding_proof_ref` 纳入外层 Envelope P0，避免攻击者替换 Proof Locator 而不触发签名失败。被引用的 Evidence 仍须独立验证：
- Integrity Proof 必须针对已认证 Signer/Profile 与精确 Envelope Digest 解析；
- Channel-Binding Proof 必须与 Payload 之外的 Protected Transport/Session Verifier Context 核对。
签署 Proof Reference 不等于证明 Proof 本身有效。

## 5. Construction / 构造

1. Strictly parse UTF-8 JSON; reject duplicate keys, non-I-JSON values and non-finite numbers.
2. Validate exact H schema ID, artifact revision 1.2.14, wire version 1.3.0 and message family.
3. Construct P0 from §§4.1–4.2 plus the two integrity/channel-binding refs.
4. `P0Bytes = JCS(P0)`.
5. `payload_digest = SHA-256(ASCII("AIMBA-C-BMCP-ENVELOPE-PAYLOAD-v1") || 0x00 || P0Bytes)`, lowercase hex.
6. `P = P0 + { payload_digest }`; `PBytes = JCS(P)`.
7. `signature_preimage = ASCII("AIMBA-C-BMCP-ENVELOPE-SIGNATURE-v1") || 0x00 || ASCII("AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0") || 0x00 || ASCII("C_PROVIDER_OUTCOME_RECORDED") || 0x00 || PBytes`.
8. Ed25519 sign using the C envelope-signing key authorized for this exact profile, audience and message family.
9. Encode canonical unpadded Base64url.
10. H verifies this signature using authenticated I-approved C issuer/key status and protected transport identity; H does not infer trust from payload fields.

### 5. 构造

1. 严格解析 UTF-8 JSON；拒绝 Duplicate Key、非 I-JSON Value 与非有限数字。
2. 校验精确 H Schema ID、Artifact Revision 1.2.14、Wire Version 1.3.0 与 Message Family。
3. 按 §§4.1–4.2 以及两个 Integrity/Channel-Binding Ref 构造 P0。
4. `P0Bytes = JCS(P0)`。
5. `payload_digest = SHA-256(ASCII("AIMBA-C-BMCP-ENVELOPE-PAYLOAD-v1") || 0x00 || P0Bytes)`，小写 Hex。
6. `P = P0 + { payload_digest }`；`PBytes = JCS(P)`。
7. `signature_preimage = ASCII("AIMBA-C-BMCP-ENVELOPE-SIGNATURE-v1") || 0x00 || ASCII("AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0") || 0x00 || ASCII("C_PROVIDER_OUTCOME_RECORDED") || 0x00 || PBytes`。
8. 使用经授权用于该精确 Profile、Audience 与 Message Family 的 C Envelope-Signing Key 执行 Ed25519 签名。
9. 编码为 Canonical Unpadded Base64url。
10. H 使用经 I 批准的 C Issuer/Key Status 与受保护 Transport Identity 验证 Signature；H 不得从 Payload 字段推断 Trust。

## 6. Verification and acceptance order / 验证与接受顺序

1. Strict raw parse and duplicate-key rejection.
2. Exact H schema pin and message-family structural validation.
3. Obtain authenticated transport/session principal from outside the payload.
4. Resolve C signer/profile/key from trusted configuration and I-authoritative trust registry; payload key/profile/issuer claims are untrusted.
5. Recompute outer envelope P0 digest and verify C envelope signature; check key status/history/anti-rollback.
6. Verify channel binding and exact principal/issuer/sender/subject/audience binding.
7. Check nonce replay and message identity/idempotency in an authoritative replay ledger. Missing replay authority => UNKNOWN.
8. Dereference and independently verify the CSubmitOutcome object signature/digest and exact wire/object equality.
9. Verify I terminal, D clearance, Storage resolution and COC proofs through their respective authoritative verifiers.
10. Only then allow durable acceptance/dispatch to downstream consumers. Any required verifier unavailable => UNKNOWN and no positive acceptance.

### 6. 验证与接受顺序

1. Raw Parse 严格解析并拒绝 Duplicate Key。
2. 精确 H Schema Pin 与 Message-Family 结构验证。
3. 从 Payload 之外取得已认证 Transport/Session Principal。
4. 从 Trusted Configuration 与 I 权威 Trust Registry 解析 C Signer/Profile/Key；Payload Key/Profile/Issuer Claim 均不可信。
5. 重算外层 Envelope P0 Digest 并验证 C Envelope Signature；检查 Key Status/History/Anti-rollback。
6. 验证 Channel Binding 与精确 Principal/Issuer/Sender/Subject/Audience Binding。
7. 在权威 Replay Ledger 检查 Nonce Replay 与 Message Identity/Idempotency。Replay Authority 缺失时为 UNKNOWN。
8. 解引用并独立验证 CSubmitOutcome Object Signature/Digest 与精确 Wire/Object Equality。
9. 通过各自权威 Verifier 验证 I Terminal、D Clearance、Storage Resolution 与 COC Proof。
10. 只有全部完成后才允许 Durable Acceptance/下游 Dispatch。任一必需 Verifier 不可用即 UNKNOWN，不得 Positive Acceptance。

## 7. Required conformance vectors / 必需符合性向量

At minimum:
- valid C outer envelope + valid C object → VALID;
- valid C object + mutated outer message_id/nonce/audience/schema revision/C message field → INVALID;
- mutate each common-envelope P0 member independently → INVALID;
- mutate each C message-family P0 member independently → INVALID;
- mutate integrity_proof_ref or channel_binding_proof_ref → INVALID;
- payload_digest/signature mutation → INVALID;
- C object signature valid but envelope signature invalid → overall INVALID;
- envelope signature valid but C object signature/digest invalid → overall INVALID;
- unknown/unregistered profile, unavailable trust/key history or replay ledger → UNKNOWN;
- revoked/compromised key, wrong issuer/principal/audience, channel binding mismatch, nonce replay → INVALID;
- COC proof append must not change C origin P0/signature, but invalid COC proof still fails overall message acceptance;
- H gateway receipt must not be accepted as a C origin signature;
- C object signature profile and outer-envelope profile cross-substitution → INVALID.

至少覆盖：
- 有效 C Outer Envelope + 有效 C Object → VALID；
- 有效 C Object + 变异 Outer Message ID/Nonce/Audience/Schema Revision/C Message Field → INVALID；
- 每个 Common-Envelope P0 成员单独变异 → INVALID；
- 每个 C Message-Family P0 成员单独变异 → INVALID；
- Integrity Proof Ref 或 Channel-Binding Proof Ref 变异 → INVALID；
- Payload Digest/Signature 变异 → INVALID；
- C Object Signature 有效但 Envelope Signature 无效 → 总体 INVALID；
- Envelope Signature 有效但 C Object Signature/Digest 无效 → 总体 INVALID；
- Profile 未注册、Trust/Key History 或 Replay Ledger 不可用 → UNKNOWN；
- Key Revoked/Compromised、Issuer/Principal/Audience 错误、Channel Binding 不匹配、Nonce Replay → INVALID；
- 追加 COC Proof 不得改变 C Origin P0/Signature，但 COC Proof 无效仍须导致整体 Message Acceptance 失败；
- H Gateway Receipt 不得被当作 C Origin Signature 接受；
- C Object Signature Profile 与 Outer-Envelope Profile 交叉替代 → INVALID。

## 8. Ownership and open decisions / 权属与未决事项

- **C:** owns the C origin signer decision, exact C message-family semantics, P0 inventory and C envelope profile candidate; owns the independent CSubmitOutcome object P0.
- **I:** must approve crypto suite suitability, C signer trust registration, key lifecycle/history/revocation/anti-rollback and authenticated principal policy. I does not rewrite C P0.
- **H:** must derive exact JSON Pointers/requiredness from H schema, implement raw parse/P0 extraction/digest/signature/channel binding/transport principal/replay checks and publish executable conformance tests. H does not choose C signer or C semantics.
- **Storage:** must define durable ingress/replay acceptance boundary and crash/retry behavior; must not persist an accepted C event before authenticated envelope verification.
- **A:** must exact-version review the final C/H/I/Storage bundle before any freeze decision.

- **C：** 拥有 C Origin Signer 决策、精确 C Message-Family 语义、P0 Inventory 与 C Envelope Profile Candidate；并拥有独立 CSubmitOutcome Object P0。
- **I：** 必须批准 Crypto Suite 适用性、C Signer Trust Registration、Key Lifecycle/History/Revocation/Anti-rollback 与 Authenticated Principal Policy。I 不重写 C P0。
- **H：** 必须从 H Schema 推导精确 JSON Pointer/Requiredness，实现 Raw Parse/P0 Extraction/Digest/Signature/Channel Binding/Transport Principal/Replay Check 并发布可执行 Conformance Test。H 不选择 C Signer 或 C 语义。
- **Storage：** 必须定义 Durable Ingress/Replay Acceptance Boundary 与 Crash/Retry 行为；认证 Envelope 前不得持久接受 C Event。
- **A：** 必须在任何 Freeze 决策前对最终 C/H/I/Storage Bundle 做精确版本审查。

## 9. Decision and limits / 决策与限制

**C delegated-role decision candidate:** C is the origin signer of the C_PROVIDER_OUTCOME_RECORDED outer envelope and the separate immutable CSubmitOutcome object. The outer envelope has a distinct C-owned P0/profile candidate. H gateway attestation is additive only. No implicit C object P0 or I profile reuse.

This does not approve production algorithm deployment, trust roots, key custody/HSM/KMS, key registration, revocation service, anti-rollback anchor, transport implementation, replay ledger, production provider adapter or runtime conformance. C origin signature proves C emitted the message; it does not prove provider truth, I authorization, D clearance, Storage resolution or COC durability.

**C 角色委托决策候选：** C 是 C_PROVIDER_OUTCOME_RECORDED 外层 Envelope 与独立不可变 CSubmitOutcome Object 的 Origin Signer。外层 Envelope 有独立 C-owned P0/Profile Candidate。H Gateway Attestation 仅为附加证据。不得隐式复用 C Object P0 或 I Profile。

本决策不批准生产算法部署、Trust Root、Key Custody/HSM/KMS、Key Registration、Revocation Service、Anti-rollback Anchor、Transport Implementation、Replay Ledger、Production Provider Adapter 或 Runtime Conformance。C Origin Signature 证明 C 发出该消息；不证明 Provider Truth、I Authorization、D Clearance、Storage Resolution 或 COC Durability。

---
**Disposition:** ACCEPT AS A C-OWNED ENVELOPE SIGNER/P0 DECISION CANDIDATE; I/H/Storage exact review and independent C Owner acceptance remain required. NOT REGISTERED / NOT FROZEN / NOT PRODUCTION-AUTHORIZED.
