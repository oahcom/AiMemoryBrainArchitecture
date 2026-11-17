# Phase 3.8.20 — H Gateway Attestation P0 Contract Candidate for Provider Outcome
# Phase 3.8.20 — H Provider Outcome Gateway Attestation P0 合同候选

- Owner perspective: H — BMCP Protocol / Envelope / Gateway Attestation
- Status: **P0 CANDIDATE SPECIFIED; SCHEMA 1.2.15 SUCCESSOR REQUIRED; C/I EXACT REVIEW REQUIRED; NOT REGISTERED / NOT CRYPTO-FROZEN**
- Current wire baseline: H Unified 1.2.14, Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- C object baseline: CSubmitOutcome 1.0.1, Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H reference auth gate: Blob `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- C signer/attestation disposition: Blob `65aa82bac678e317325b1673121b92c04121b4f4`
- I trust-boundary acceptance: Blob `a698fb8d58181c9fc760be5a0a3901cc9817dcad`
- A integration review: Phase 3.12.2, Blob `eb3c946065aff4fbc6d76f384402fb9f75fa32dc`
- Provenance: delegated H-role contract drafting; not an independent human H Owner signature or I profile registration.
- English and Chinese are normative peers.

## 1. Purpose and non-substitution / 目的与不可替代边界

This contract defines a **separate H Gateway Attestation** for a `C_PROVIDER_OUTCOME_RECORDED` BMCP message. The C adapter continues to sign the immutable CSubmitOutcome 1.0.1 object under C's independent C-P0. The H gateway authenticates the original C adapter at ingress, then signs an H-owned envelope projection that binds the exact received message, exact C object and protected origin-transport receipt.

The H attestation means only “the identified H gateway received these exact bytes under this authenticated origin context and bound them to this exact C object.” It does not assert provider truth, provider-side-effect occurrence, C admission correctness, I authorization, D clearance, Storage resolution or COC commitment.

本合同定义 `C_PROVIDER_OUTCOME_RECORDED` BMCP Message 的**独立 H Gateway Attestation**。C Adapter 继续使用 C 独立 C-P0 对不可变 CSubmitOutcome 1.0.1 Object 签名。H Gateway 在 Ingress 认证原始 C Adapter 后，签署 H-owned Envelope Projection，将精确接收消息、精确 C Object 与受保护 Origin-Transport Receipt 绑定。

H Attestation 仅表示“指定 H Gateway 在该认证 Origin Context 下收到这些精确字节，并将其绑定到精确 C Object”。它不证明 Provider Truth、Provider Side-Effect 发生、C Admission 正确、I Authorization、D Clearance、Storage Resolution 或 COC Commitment。

The following are distinct signed/evidence domains:
1. C object P0 digest/signature — C authority.
2. H gateway envelope P0 digest/signature — H gateway attestation.
3. Origin transport authentication receipt — H transport verifier, with I-approved trust policy.
4. I authorization/key-status evidence — I authority.
5. D lineage/fence evidence — D authority.
6. Storage/COC persistence and recovery evidence — Storage/COC authority.

不得混淆六类独立证据域：C Object P0、H Gateway Envelope P0、Origin Transport Authentication Receipt、I Authorization/Key Status、D Lineage/Fence、Storage/COC Persistence/Recovery。

## 2. Proposed successor schema / 后继 Schema 候选

The current H 1.2.14 common envelope does not carry enough explicit origin-transport receipt and H signing-sequencer data to make the selected gateway-attestation model self-describing. H therefore proposes **Unified schema artifact revision 1.2.15 / wire family 1.3.0** as a successor. No 1.2.14 file is mutated.

For `C_PROVIDER_OUTCOME_RECORDED`, 1.2.15 MUST conditionally require:
- `signature_profile_id` — exact H gateway attestation profile ID; it is not `canonicalization_profile_id`;
- `origin_transport_context_ref` — immutable verifier-produced receipt ref for the original C→H ingress;
- `origin_transport_context_digest` — digest of that exact receipt;
- `origin_received_bytes_digest` — digest of the exact raw bytes received from the original C adapter before parsing/normalization;
- `origin_issuer_ref`, `origin_sender_authority_ref`, `origin_sender_subject_ref` — original C-side transport identity claims verified at ingress;
- `origin_authentication_context_ref`, `origin_channel_binding_proof_ref`, `origin_received_at` — immutable origin-auth/session evidence and time;
- `signing_sequence_namespace_ref`, `signing_record_sequence` — H gateway's durable monotonic signing sequence, linked to the authenticated H key-status registry/checkpoint.

Existing envelope fields retain distinct meanings:
- `issuer_ref`, `sender_authority_ref`, `sender_subject_ref` identify the H gateway attestor and MUST match the receiver's protected H transport context;
- `subject_ref` is the registry-authorized subject of the C-owned message and need not equal the H gateway sender subject;
- `owner_authority` remains `C`; `owner_record_ref` is the exact immutable C record;
- `channel_binding_proof_ref` binds the H gateway's authenticated downstream channel; `origin_channel_binding_proof_ref` binds the original C→H ingress channel;
- `owner_signature_ref` identifies the independent C object signature evidence;
- all existing C Provider Outcome branch fields remain exact duplicated-wire fields and MUST match the CSubmitOutcome object.

当前 H 1.2.14 Common Envelope 没有足够显式的 Origin-Transport Receipt 与 H Signing-Sequencer 数据，无法完整表达 Gateway-Attestation 模型。H 提议以 **Unified Schema Artifact Revision 1.2.15 / Wire Family 1.3.0** 作为后继版本，不修改 1.2.14 文件。

对 `C_PROVIDER_OUTCOME_RECORDED`，1.2.15 必须条件性要求：
- `signature_profile_id`：精确 H Gateway Attestation Profile ID，不等于 `canonicalization_profile_id`；
- `origin_transport_context_ref/digest`：原始 C→H Ingress 的不可变 Verifier Receipt 与 Digest；
- `origin_received_bytes_digest`：原始 C Adapter 字节在 Parse/Normalize 前的精确 Digest；
- `origin_issuer_ref`、`origin_sender_authority_ref`、`origin_sender_subject_ref`：Ingress 时验证的原始 C 侧 Transport Identity；
- `origin_authentication_context_ref`、`origin_channel_binding_proof_ref`、`origin_received_at`：不可变 Origin Auth/Session Evidence 与时间；
- `signing_sequence_namespace_ref`、`signing_record_sequence`：H Gateway 持久单调签名序列，并绑定认证 H Key Status Registry/Checkpoint。

既有 Envelope 字段含义：
- `issuer_ref`、`sender_authority_ref`、`sender_subject_ref` 标识 H Gateway Attestor，必须匹配 Receiver Protected H Transport Context；
- `subject_ref` 是 Registry 授权的 C-owned Message Subject，不要求等于 H Gateway Sender Subject；
- `owner_authority` 保持 `C`，`owner_record_ref` 指向精确不可变 C Record；
- `channel_binding_proof_ref` 绑定 H Gateway 下游认证 Channel；`origin_channel_binding_proof_ref` 绑定原始 C→H Ingress Channel；
- `owner_signature_ref` 指向独立 C Object Signature Evidence；
- 所有现有 C Provider Outcome Wire 字段仍是精确重复字段，必须与 CSubmitOutcome Object 一致。

## 3. H P0 exact field projection / H P0 精确字段投影

Candidate profile identifier: `AIMBA-H-GATEWAY-ATTEST-1.0` (unregistered candidate only).

Candidate canonicalization: `RFC8785-JCS-1.0`; digest: `SHA-256`; signature: `Ed25519`; digest/signature encoding: unpadded Base64url. These primitives and encodings are proposals only; I must approve the exact profile and H trust root before registration.

The signed P0 projection is a JSON object containing **every present field** from these groups, with no wildcard exclusions:

**A. Envelope identity and routing**
- `schema_id`, `schema_artifact_revision`, `schema_version`, `message_type`;
- `message_id`, `message_nonce`, `audience`;
- `issuer_ref`, `sender_authority_ref`, `sender_subject_ref`, `subject_ref`;
- `owner_authority`, `owner_record_ref`, `policy_domain_ref` when present;
- `causal_order_profile_ref`, `causal_order_coordinator_ref`, `causal_order_domain_ref`.

**B. H signer and signing order**
- `signature_profile_id`, `canonicalization_profile_id`, `digest_algorithm`;
- `key_id_ref`, `key_version`;
- `signing_sequence_namespace_ref`, `signing_record_sequence`;
- `created_at`.

**C. Origin transport receipt**
- `origin_transport_context_ref`, `origin_transport_context_digest`;
- `origin_received_bytes_digest`;
- `origin_issuer_ref`, `origin_sender_authority_ref`, `origin_sender_subject_ref`;
- `origin_authentication_context_ref`, `origin_channel_binding_proof_ref`, `origin_received_at`;
- `channel_binding_proof_ref` for the H gateway's authenticated downstream channel.

**D. Complete message-specific Provider Outcome branch**
- every present C Provider Outcome wire property, including `c_submit_outcome_ref`, `c_submit_outcome_digest`, outcome enum, provider/adapter/idempotency refs, request boundary/digest, transaction/evidence refs, owner admission/ledger fields, COC intent/reservation/absence fields, I/D/Storage proof refs and C signature evidence refs;
- any future message-specific property requires a successor P0 revision and vectors; no wildcard ignore list is permitted.

**Excluded derived/evidence-envelope fields (exact exclusions only)**
- `payload_digest`: derived SHA-256 digest of the canonical P0 projection;
- `signature`: Ed25519 signature over the domain-separated P0 preimage;
- `integrity_proof_ref`: immutable reference to the resulting signature/integrity evidence record; it is verified after P0/signature validation and is excluded to avoid a self-reference cycle.

No other field is excluded. Null, absent, empty string, empty array and empty object remain distinct. Optional properties are included if present; a missing required/conditional property is INVALID. Canonicalization MUST reject duplicate JSON keys, invalid UTF-8, non-finite numbers and non-canonical representations before P0 construction.

候选 Profile ID：`AIMBA-H-GATEWAY-ATTEST-1.0`（仅未注册候选）。

候选 Canonicalization：`RFC8785-JCS-1.0`；Digest：`SHA-256`；Signature：`Ed25519`；Digest/Signature Encoding：无 Padding Base64url。以上均只是提案，注册前必须由 I 批准精确 Profile 与 H Trust Root。

签名 P0 Projection 是 JSON Object，包含以下全部分组中的**每个实际存在字段**，不得使用 Wildcard Exclusion：

**A. Envelope Identity/Routing**：Schema ID/Revision/Wire Version/Message Type、Message ID/Nonce/Audience、Issuer/Sender/Subject、Owner Authority/Record、PolicyDomain（若存在）、COC Profile/Coordinator/Domain。

**B. H Signer/Signing Order**：Signature Profile、Canonicalization Profile、Digest Algorithm、Key ID/Version、Signing Sequence Namespace/Record Sequence、Created At。

**C. Origin Transport Receipt**：Origin Context Ref/Digest、Origin Received Bytes Digest、Origin Issuer/Sender Authority/Sender Subject、Origin Authentication Context、Origin Channel Binding、Origin Received At，以及 H Gateway 下游 Channel Binding。

**D. 完整 Provider Outcome Message Branch**：每个实际存在的 C Provider Outcome Wire 属性，包括 C Object Ref/Digest、Outcome、Provider/Adapter/Idempotency、Request Boundary/Digest、Transaction/Evidence、Owner Admission/Ledger、COC Intent/Reservation/Absence、I/D/Storage Proof 与 C Signature Evidence；未来新增消息字段必须升级 P0 Revision 并增加向量，不允许 Wildcard Ignore。

**仅允许以下精确排除字段：**
- `payload_digest`：Canonical P0 Projection 的派生 SHA-256 Digest；
- `signature`：Domain-Separated P0 Preimage 的 Ed25519 Signature；
- `integrity_proof_ref`：结果 Signature/Integrity Evidence Record 的不可变引用；在 P0/Signature 验证后校验，为避免自引用环而排除。

除此之外不得排除任何字段。Null、Absent、Empty String、Empty Array、Empty Object 必须区分。Optional Property 若存在就纳入；Required/Conditional Property 缺失为 INVALID。P0 构造前必须拒绝 Duplicate JSON Key、Invalid UTF-8、Non-finite Number 与 Non-canonical Representation。

## 4. Domain separation and preimage / 域分离与 Preimage

Candidate domain separator bytes:

`AIMBA-H-GATEWAY-ATTEST-P0\0v1\0`

Candidate preimage:

`UTF8(domain_separator) || JCS(P0)`

Candidate digest:

`BASE64URL_NOPAD(SHA256(JCS(P0)))`

Candidate signature:

`BASE64URL_NOPAD(Ed25519.Sign(H_gateway_private_key, preimage))`

The H gateway signature authenticates the H P0 only. The C object signature remains over C's own C-P0 and is verified independently. A valid H signature cannot upgrade an invalid/unknown C signature.

候选 Domain Separator、Preimage、Digest 与 Signature 如上。H Gateway Signature 只认证 H P0；C Object Signature 仍只覆盖 C 自己的 C-P0，并独立验证。H Signature 有效不能将无效/未知 C Signature 升级为有效。

## 5. Verification order / 验证顺序

1. Strictly parse raw bytes; reject duplicate keys/invalid UTF-8/non-finite numbers.
2. Select exact H schema revision and message family from trusted receiver configuration; validate 1.2.15 structural/conditional schema before any acceptance decision.
3. Authenticate the H gateway's protected transport/session principal; payload claims cannot mint ProtectedTransportContext.
4. Resolve H signer/profile/key through I-approved registry and verify key status at `signing_record_sequence` plus current status/anti-rollback.
5. Reconstruct exact P0, recompute `payload_digest`, verify H signature and integrity evidence.
6. Verify the origin transport receipt against H gateway's protected ingress-verifier result; bind raw received bytes digest, C adapter identity, authentication context and channel-binding proof.
7. Verify H gateway signer/issuer/subject/audience/message-family delegation in the I registry.
8. Atomically reserve replay state and persist the accepted H receipt/message under a crash-safe ingress state machine. A mere callback return is not durable acceptance.
9. Dereference and independently verify CSubmitOutcome 1.0.1, C-P0 digest/signature, sequence namespace, provider evidence and C semantics.
10. Verify separate I/D/Storage/COC joins and currentness. Return VALID only when every required verifier and durable join succeeds; missing authority state is UNKNOWN.

## 6. Replay and durable acceptance state machine / Replay 与 Durable Acceptance 状态机

The current H reference callback `check_and_reserve_replay` is insufficient as a production contract. The production state machine must bind `message_id`, `message_nonce`, H P0 digest, C object ref/digest, signer key/version, audience, origin context digest and replay expiry.

Required states:
- `AUTHENTICATED_UNRESERVED`;
- `REPLAY_RESERVED` with durable reservation ID and expiry;
- `INGRESS_COMMITTED` with immutable accepted receipt/result ref;
- `ABORTED_PRECOMMIT` only when no domain side effect/owner processing occurred;
- `UNKNOWN_RECOVERY` while commit/reservation status cannot be resolved;
- `IDEMPOTENT_REPLAY` only after the original committed result is read back and current disclosure authorization is rechecked.

Reservation and ingress commit must be one recoverable transaction or an explicit durable two-record protocol with idempotent recovery. Crash after reservation but before ingress commit MUST resolve the same reservation; it must not consume the nonce forever or allow a second independent message to proceed. Crash after ingress commit but before ACK MUST return the same immutable result. Same digest with a different message ID is still subject to C/owner-level idempotency and cannot repeat provider side effects. Same message ID/nonce with different P0 digest is INVALID.

## 7. Test matrix / 测试矩阵

Before P0 freeze, H must add:
- one positive complete 1.2.15 H gateway envelope + origin transport receipt + C object fixture;
- one mutation for every P0 field, including all common and C branch fields;
- explicit absent/null/empty vectors for every nullable COC field and origin receipt field;
- changed raw ingress bytes with unchanged normalized object;
- changed origin context digest/ref, origin sender, gateway issuer, subject, owner authority, audience, channel binding and key version;
- changed signing sequence namespace/record sequence and stale/revoked/compromised key status;
- unknown/unregistered H profile and wrong key-purpose tests;
- invalid C object signature with valid H signature and valid C signature with invalid H signature;
- duplicate nonce/message ID conflict, same-digest replay, replay after authorization revocation and replay-ledger outage;
- crash injection after replay reservation, after durable ingress commit, before result publication and before ACK;
- independent Python and Node implementations with pinned dependencies and byte-for-byte expected vectors.

## 8. Disposition / 结论

**Delegated H-role disposition: ACCEPT this H gateway-attestation P0 as a construction candidate for cross-owner review. The proposed schema 1.2.15, profile ID, algorithms, domain separator and P0 are NOT registered, NOT approved and NOT frozen. Implementation is blocked on exact C/I review and trust governance.**

**角色模拟 H 侧结论：接受该 H Gateway Attestation P0 作为交叉审查的构造候选。拟议 Schema 1.2.15、Profile ID、算法、Domain Separator 与 P0 均未注册、未批准、未冻结。实现前必须取得 C/I 精确复审与 Trust Governance 批准。**

---
**Provenance:** delegated H-role contract drafting in the coordinating session; not an independent human H Owner signature, I registration or production security approval.
