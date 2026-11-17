# Phase 3.8.20 — I Exact Review: H Gateway Attestation P0 Candidate
# Phase 3.8.20 — I 精确复审：H Gateway Attestation P0 候选

- Owner perspective: I — Security, Identity, Trust and Governance
- H Phase 3.8.20 P0 candidate: Blob `05313c60c757cd736cb3ab127b330a5dce674dd1`
- C signer/attestation decision: Phase 3.8.23, Blob `65aa82bac678e317325b1673121b92c04121b4f4`
- C exact review: Phase 3.8.24, Blob `721bca2ad734284a87e1056ef4c2d9ff1f049170`
- H Unified schema 1.2.14 baseline: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H reference ingress gate: Blob `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- Status: **ACCEPT AS SECURITY ARCHITECTURE CANDIDATE WITH I-OWNED REGISTRATION BLOCKERS; NOT REGISTERED / NOT APPROVED / NOT FROZEN**
- Provenance: delegated I-role exact review; not an independent human I Owner signature or formal security registration.
- English and Chinese are normative peers.

## 1. I disposition / I 侧结论

I accepts the H gateway-attestation P0 architecture candidate subject to the C conditions and the I trust requirements below:
- C signs CSubmitOutcome under its own C-P0 and C data-key lifecycle.
- H gateway signs a distinct H envelope P0 and attests only receipt/binding.
- I governs whether the H gateway issuer/key/profile and its delegation are trusted; I is not the H signer.
- H P0, C P0 and I authorization/key-status proof remain distinct cryptographic domains.

I 在满足 C 条件与以下 I Trust 要求的前提下，接受 H Gateway-Attestation P0 架构候选：
- C 使用自己的 C-P0 与 C Data-Key Lifecycle 签署 CSubmitOutcome；
- H Gateway 签署独立 H Envelope P0，仅 Attest Receipt/Binding；
- I 决定是否信任 H Gateway Issuer/Key/Profile 与 Delegation；I 不充当 H Signer；
- H P0、C P0 与 I Authorization/Key-Status Proof 保持不同密码学域。

## 2. I-owned registry contract / I 自有 Registry 合同

The H profile candidate `AIMBA-H-GATEWAY-ATTEST-1.0` is not registered. Before registration, H and I must define an immutable registry record binding:
- exact profile ID/version, canonicalization profile, digest and signature algorithms, encoding;
- H gateway issuer/authority/subject and allowed key IDs/versions;
- key purpose = gateway-attestation only; prohibit C provider-outcome origin signing and I governance signing;
- allowed message family `C_PROVIDER_OUTCOME_RECORDED`, exact audience(s), subject/owner-authority relation and delegation scope;
- signing sequence namespace and relation to the H key-status event/registry stream;
- validity interval, activation sequence, retirement/revocation/compromise sequence and historical verification policy;
- trust-root ref/digest, custody boundary, rotation and emergency compromise procedure;
- anti-rollback checkpoint ref, monotonic head and restore/failover behavior.

H Profile 候选 `AIMBA-H-GATEWAY-ATTEST-1.0` 尚未注册。注册前，H/I 必须定义不可变 Registry Record，绑定：
- 精确 Profile ID/Version、Canonicalization Profile、Digest/Signature Algorithm 与 Encoding；
- H Gateway Issuer/Authority/Subject 及允许 Key ID/Version；
- Key Purpose 仅限 Gateway-Attestation，禁止用于 C Provider Outcome Origin Signing 或 I Governance Signing；
- 允许 Message Family `C_PROVIDER_OUTCOME_RECORDED`、精确 Audience、Subject/Owner-Authority Relation 与 Delegation Scope；
- Signing Sequence Namespace 及其与 H Key Status Event/Registry Stream 的关系；
- Validity Interval、Activation Sequence、Retirement/Revocation/Compromise Sequence 与历史验证策略；
- Trust-Root Ref/Digest、Custody Boundary、Rotation 与紧急 Compromise 流程；
- Anti-Rollback Checkpoint Ref、Monotonic Head 与 Restore/Failover 行为。

## 3. P0 and key-status requirements / P0 与 Key Status 要求

1. I conditionally accepts the candidate P0 inventory, but requires the H successor schema to make `signature_profile_id` conditionally required for gateway-attested Provider Outcome messages.
2. `signing_sequence_namespace_ref` and `signing_record_sequence` must be authenticated against the exact H gateway key-status registry stream. Timestamp alone cannot establish signing-time key validity.
3. The H integrity-proof evidence record must be immutable and bind the exact P0 digest, signature, profile ID, key ID/version, signing sequence, issuer and trust-registry snapshot. A mutable `integrity_proof_ref` is insufficient.
4. The H profile's P0 must bind the H gateway signer identity and origin C adapter transport receipt, while keeping the C object's own signature and C key-status chain separately verified.
5. The `origin_transport_context_ref/digest` must be verifier-issued, complete and non-replayable for the ingress session. The H gateway cannot attest an origin identity it did not authenticate.
6. I requires explicit null/absent semantics, full-field mutation vectors, independent Python/Node implementations and exact build/CI pins before any registration review.
7. Profile/key registry unavailability, stale checkpoint, unknown key status or incomplete history returns UNKNOWN. Proven wrong issuer/purpose/audience/key/profile is INVALID. No fallback or downgrade.

1. I 有条件接受候选 P0 Inventory，但要求后继 H Schema 对 Gateway-Attested Provider Outcome Message 将 `signature_profile_id` 条件性设为 REQUIRED。
2. `signing_sequence_namespace_ref` 与 `signing_record_sequence` 必须通过精确 H Gateway Key Status Registry Stream 认证。Timestamp 不能证明签名时 Key Validity。
3. H Integrity-Proof Evidence Record 必须不可变，并绑定精确 P0 Digest、Signature、Profile ID、Key ID/Version、Signing Sequence、Issuer 与 Trust-Registry Snapshot。可变 `integrity_proof_ref` 不足。
4. H Profile P0 必须绑定 H Gateway Signer Identity 与 Origin C Adapter Transport Receipt，同时独立验证 C Object Signature 和 C Key Status Chain。
5. `origin_transport_context_ref/digest` 必须由 Verifier 生成、完整且对 Ingress Session 不可重放。H Gateway 不得 Attest 自己未认证的 Origin Identity。
6. 注册复审前，I 要求明确 Null/Absent、全字段 Mutation Vector、独立 Python/Node 实现与精确 Build/CI Pin。
7. Profile/Key Registry 不可用、Checkpoint 过期、Key Status 未知或 History 不完整返回 UNKNOWN。已证明 Issuer/Purpose/Audience/Key/Profile 错误返回 INVALID。禁止回退或降级。

## 4. No registration or deployment approval / 不注册、不批准部署

This review does not register `AIMBA-H-GATEWAY-ATTEST-1.0`, approve Ed25519/JCS/SHA-256 for production H signing, approve an H gateway trust root, approve a production key/KMS/HSM, approve signer delegation, or authorize production ingress. The primitives in H's document remain candidate choices.

本复审不注册 `AIMBA-H-GATEWAY-ATTEST-1.0`，不批准 Ed25519/JCS/SHA-256 用于生产 H Signing，不批准 H Gateway Trust Root、生产 Key/KMS/HSM、Signer Delegation，也不授权生产 Ingress。H 文档中的 Primitive 仍为候选选择。

## 5. I disposition / I 侧最终结论

**Delegated I-role decision: ACCEPT H Phase 3.8.20 as a security architecture candidate with enumerated registration conditions. The H profile, trust root, issuer registry, gateway key, key lifecycle and production verifier remain NOT REGISTERED / NOT APPROVED. Exact successor schema and vectors must return to I before registration. NOT FROZEN.**

**角色模拟 I 侧决议：接受 H Phase 3.8.20 作为带明确注册条件的安全架构候选。H Profile、Trust Root、Issuer Registry、Gateway Key、Key Lifecycle 与生产 Verifier 均未注册/未批准。后继精确 Schema 与向量必须返回 I 注册复审。不冻结。**

---
**Provenance:** delegated I-role exact review authored in the coordinating session; not an independent human I Owner signature or formal governance registration.
