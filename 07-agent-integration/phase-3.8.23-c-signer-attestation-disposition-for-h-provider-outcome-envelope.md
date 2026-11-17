# Phase 3.8.23 — C Signer/Attestation Disposition for Provider Outcome Outer Envelope
# Phase 3.8.23 — C 对 Provider Outcome 外层 Envelope 的 Signer/Attestation 决议

- Owner perspective: C — Provider Outcome Semantic Authority
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C object signature projection Blob: `06d9264124d85896ccd44ef7789d9af245d8255b`
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H reference auth gate Blob: `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- C Phase 3.8.22 review Blob: `8fd6052cabf58a78962cc2e776398b2a40604bcd`
- I trust-boundary review Blob: `73145f83df234ebb9e55cc07f0a82b0db9416b68`
- Status: **C SEMANTIC ACCEPTANCE OF SEPARATE GATEWAY ATTESTATION MODEL AS CANDIDATE; I/H APPROVAL AND EXACT H P0 REQUIRED; NOT REGISTERED / NOT FROZEN**
- Provenance: delegated C-role decision; not an independent human C Owner signature.
- English and Chinese are normative peers.

## 1. Decision / 决策

C selects the following architecture candidate for `C_PROVIDER_OUTCOME_RECORDED`:

1. The C adapter/owner signs the immutable CSubmitOutcome 1.0.1 object under the C-owned C-P0 projection and C profile. This signature authenticates the C-owned provider outcome record and its C semantic fields.
2. The H gateway, after authenticating the incoming C adapter through protected transport/session context and validating the C object reference/digest, may issue a **separate H-owned gateway receipt/attestation** over a distinct H envelope/receipt P0.
3. The H gateway attestation means only: “this H gateway received this exact message under this authenticated ingress context and bound it to this exact immutable C object.” It does **not** mean the gateway independently observed the provider side effect or certifies C's provider-outcome truth.
4. The H attestation has its own issuer, authority, subject, profile ID, key namespace/lifecycle, domain separator, canonical projection and signature evidence. It MUST NOT reuse C's P0, C signature, C key or C profile.
5. If the gateway forwards an envelope without issuing a durable attestation, the receiver must still authenticate the original C adapter through the protected transport/session mechanism and validate C's object signature. A payload claim alone is never origin authentication.

C 为 `C_PROVIDER_OUTCOME_RECORDED` 选择以下架构候选：

1. C Adapter/Owner 使用 C 自有 C-P0 Projection 与 C Profile 对不可变 CSubmitOutcome 1.0.1 Object 签名。该签名认证 C-owned Provider Outcome Record 及其 C 语义字段。
2. H Gateway 在通过 Protected Transport/Session Context 认证入站 C Adapter，并验证 C Object Ref/Digest 后，可以对独立 H Envelope/Receipt P0 生成**独立 H-owned Gateway Receipt/Attestation**。
3. H Gateway Attestation 仅表示：“该 H Gateway 在此认证 Ingress Context 下收到精确消息，并将其绑定到精确不可变 C Object。”它**不**表示 Gateway 独立观察了 Provider Side Effect，也不认证 C 的 Provider Outcome Truth。
4. H Attestation 必须具有独立 Issuer、Authority、Subject、Profile ID、Key Namespace/Lifecycle、Domain Separator、Canonical Projection 与 Signature Evidence。不得复用 C P0、C Signature、C Key 或 C Profile。
5. 若 Gateway 仅转发 Envelope 而不签发持久 Attestation，接收方仍必须通过 Protected Transport/Session 机制认证原始 C Adapter，并验证 C Object Signature。Payload Claim 永远不能单独作为 Origin Authentication。

## 2. C authority invariants / C 权威不变量

- C remains sole authority for ProviderAttempt, C Gate/Generation, provider/account/adapter/endpoint/region/API operation, idempotency namespace/key, final request boundary/digest, SideEffectStatus, provider evidence, CSubmitOutcome identity and C-P0 digest/signature.
- H gateway receipt is not a C Provider Outcome and cannot amend, replace or reinterpret the immutable C object.
- A valid H gateway attestation plus invalid/unavailable C object signature is not a valid provider outcome.
- A valid C object signature plus invalid H envelope attestation is not an authenticated H ingress message.
- Storage/COC commit, I authorization, D clearance and H ACK cannot mint C provider truth.
- UNKNOWN/IN_DOUBT remains nonterminal; no retry-as-new is authorized.

- C 仍独占 ProviderAttempt、C Gate/Generation、Provider/Account/Adapter/Endpoint/Region/API、Idempotency Namespace/Key、Final Request Boundary/Digest、SideEffectStatus、Provider Evidence、CSubmitOutcome Identity 与 C-P0 Digest/Signature。
- H Gateway Receipt 不是 C Provider Outcome，不能修改、替换或重新解释不可变 C Object。
- H Gateway Attestation 有效但 C Object Signature 无效/不可用，不构成有效 Provider Outcome。
- C Object Signature 有效但 H Envelope Attestation 无效，不构成已认证 H Ingress Message。
- Storage/COC Commit、I Authorization、D Clearance 与 H ACK 均不能签发 C Provider Truth。
- UNKNOWN/IN_DOUBT 保持非终态，不授权 retry-as-new。

## 3. Required H contract / H 必需合同

H must publish a separate H-owned envelope/receipt P0 contract with:
- exact signed field allowlist and JSON Pointers;
- explicit absent/null/empty semantics;
- domain separator and canonical byte/preimage rules;
- digest and signature algorithm identifiers;
- H gateway issuer/authority/subject identity and key namespace;
- exact binding to raw ingress message digest, CSubmitOutcome record_ref, C payload_digest, C signature evidence ref and authenticated transport-context receipt;
- key-status event/sequence and anti-rollback references;
- replay/idempotency key and durable receipt lifecycle;
- distinct positive and per-field negative mutation vectors.

The H P0 must not silently include mutable receiver-local state or conflate a transport receipt with the C origin signature. If H signs a receipt rather than the original C envelope, the exact distinction among received-bytes digest, canonical envelope digest and C object digest must be explicit.

H 必须发布独立 H-owned Envelope/Receipt P0 合同，明确精确签名字段 Allowlist/JSON Pointer、Absent/Null/Empty 语义、Domain Separator/Canonical Bytes/Preimage、Digest/Signature Algorithm、H Gateway Identity/Key Namespace、Raw Ingress Digest/C Object Ref/C Payload Digest/C Signature Ref/Authenticated Transport Receipt 的精确绑定、Key Status/Sequence/Anti-Rollback、Replay/Idempotency 与 Durable Receipt Lifecycle，以及逐字段 Positive/Negative Vector。

H P0 不得静默纳入可变 Receiver-Local State，也不得混淆 Transport Receipt 与 C Origin Signature。若 H 签署的是 Receipt 而非原始 C Envelope，必须明确区分 Received-Bytes Digest、Canonical Envelope Digest 与 C Object Digest。

## 4. I/H conditions / I/H 条件

- I must approve the H gateway trust root, issuer-to-authority registry, key-status lifecycle, revocation/compromise precedence, custody, historical verification and anti-rollback policy before any H signer is trusted.
- H owns the envelope wire and P0 implementation but cannot self-approve its gateway key or profile.
- The H profile must be distinct from both AIMBA-C-CRYPTO-1.0 and AIMBA-I-CRYPTO-1.0.
- Production protected transport context must authenticate the C adapter before the gateway issues an attestation.
- Replay reservation and durable receipt publication require a crash-safe state machine and exact prior-result semantics.

- I 必须先批准 H Gateway Trust Root、Issuer-to-Authority Registry、Key Status Lifecycle、Revocation/Compromise 优先级、Custody、Historical Verification 与 Anti-Rollback，才能信任 H Signer。
- H 拥有 Envelope Wire 与 P0 实现，但不能自行批准 Gateway Key/Profile。
- H Profile 必须与 AIMBA-C-CRYPTO-1.0、AIMBA-I-CRYPTO-1.0 均不同。
- Gateway 签发 Attestation 前，Production Protected Transport Context 必须认证 C Adapter。
- Replay Reservation 与 Durable Receipt Publication 必须具备 Crash-Safe State Machine 和精确 Prior-Result 语义。

## 5. C disposition / C 侧结论

**Delegated C-role decision: ACCEPT the separate H gateway receipt/attestation model as the preferred architecture candidate while preserving the independent C-signed immutable CSubmitOutcome object. This is a C semantic boundary decision only. It does not register or approve an H profile, gateway key, trust root, signer deployment or production ingress. H exact P0 and I trust approval remain mandatory. NOT FROZEN.**

**角色模拟 C 侧决议：接受“独立 H Gateway Receipt/Attestation + 独立 C-signed 不可变 CSubmitOutcome Object”作为优先架构候选。该决议仅属于 C 语义边界，不注册/批准 H Profile、Gateway Key、Trust Root、Signer Deployment 或生产 Ingress。仍必须取得 H 精确 P0 与 I Trust 批准，不冻结。**

---
**Provenance:** delegated C-role decision authored in the coordinating session; not an independent human C Owner signature or I security approval.
