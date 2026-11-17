# Phase 3.8.19 — I Review: C Separate H-Gateway Attestation Model
# Phase 3.8.19 — I 复审：C 独立 H-Gateway Attestation 模型

- Owner perspective: I — Security, Identity, Trust and Governance
- C signer/attestation disposition: Phase 3.8.23, Blob `65aa82bac678e317325b1673121b92c04121b4f4`
- H authenticated-ingress reference gate: Blob `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- Prior I envelope trust-boundary review: Phase 3.8.18, Blob `73145f83df234ebb9e55cc07f0a82b0db9416b68`
- Status: **ACCEPT AS TRUST-BOUNDARY ARCHITECTURE CANDIDATE; NO H PROFILE REGISTRATION / NO GATEWAY KEY APPROVAL / NO DEPLOYMENT**
- Provenance: delegated I-role review; not an independent human I Owner signature or formal security registration.
- English and Chinese are normative peers.

## 1. I disposition / I 侧决议

I accepts C's separation model as an architecture candidate:
- C signs the immutable CSubmitOutcome object under C's independent C-P0 contract and C data-key lifecycle.
- H gateway may issue a separate H-owned receipt/attestation over a distinct H envelope/receipt P0 after protected transport authentication of the C adapter.
- H attestation proves gateway receipt and binding to the exact C object only; it does not prove provider side-effect truth.
- C P0, H receipt P0 and any I governance/authorization proof are separate cryptographic domains and authority facts.

I 对 C 提出的分离模型作为架构候选予以接受：
- C 使用独立 C-P0 合同与 C Data-Key Lifecycle 对不可变 CSubmitOutcome Object 签名；
- H Gateway 可在 Protected Transport 认证 C Adapter 后，对独立 H Envelope/Receipt P0 签发独立 H-owned Receipt/Attestation；
- H Attestation 仅证明 Gateway 收到消息并绑定精确 C Object，不证明 Provider Side-Effect Truth；
- C P0、H Receipt P0 与任何 I Governance/Authorization Proof 属于不同密码学域和权威事实。

## 2. Trust ownership / Trust 权属

I owns the governance decision for whether an H gateway issuer/key/profile is trusted by the system. H owns the gateway service, envelope wire, P0 construction and signing operation. C owns the source provider outcome and its C object signature. This means:
- I does not become the H envelope signer.
- H cannot self-register or self-approve its gateway key/profile.
- C cannot authorize H trust-root/key custody by virtue of owning the provider event.
- An H gateway attestation cannot substitute for C object signature or provider evidence.
- The I trust registry must explicitly map issuer → authority kind → signer identity/key version → allowed message family/audience → permitted delegation/subject relation → validity interval and revocation state.

I 拥有系统是否信任 H Gateway Issuer/Key/Profile 的 Governance 决策；H 拥有 Gateway Service、Envelope Wire、P0 构造与签名操作；C 拥有 Provider Outcome Source 及 C Object Signature。因此：
- I 不成为 H Envelope Signer；
- H 不能自行注册/批准 Gateway Key/Profile；
- C 不能因为拥有 Provider Event 就授权 H Trust Root/Key Custody；
- H Gateway Attestation 不能替代 C Object Signature 或 Provider Evidence；
- I Trust Registry 必须显式映射 Issuer → Authority Kind → Signer Identity/Key Version → Allowed Message Family/Audience → Permitted Delegation/Subject Relation → Validity Interval/Revocation State。

## 3. Conditions before any registration / 注册前条件

1. H publishes an exact versioned H receipt/envelope P0: complete field allowlist, JSON Pointers, canonical bytes, domain separator, digest/signature algorithms, profile ID, explicit null/absent treatment and signature preimage.
2. H distinguishes original ingress bytes digest, normalized/canonical envelope digest, C object payload digest and gateway receipt digest; no digest may be reused across domains without an explicit typed rule.
3. H publishes a distinct H gateway key namespace and key-status event/sequence contract. It must not reuse C or I key IDs/sequences.
4. I approves the H trust-root hierarchy, issuer registration, allowed signer/subject/owner-authority relation, audience, key purpose, key status/history, revocation/compromise precedence, rotation, custody, anti-rollback and historical verification.
5. H gateway signing key must be held by an approved KMS/HSM or equivalent protected signer boundary; no private key in repository, source fixture or CI secret echo.
6. Protected transport authentication must establish the original C adapter identity before H issues a receipt. Gateway attestation cannot retroactively authenticate an untrusted sender.
7. Replay/idempotency state must be durable, scoped and crash-safe; same-digest replay disclosure must re-check current authorization, key status, scope and Forget fence.
8. At least two independent implementations must agree on exact H P0 canonical bytes/digest/signature and every signed-field mutation must invalidate the signature.
9. Unknown/unavailable trust registry, key status, checkpoint, transport context or replay state returns UNKNOWN; proven mismatch returns INVALID. No default trust or algorithm downgrade.

任何注册前必须：
1. H 发布精确版本化 H Receipt/Envelope P0：完整 Field Allowlist、JSON Pointer、Canonical Bytes、Domain Separator、Digest/Signature Algorithm、Profile ID、Null/Absent 语义与 Signature Preimage；
2. 明确区分 Original Ingress Bytes Digest、Normalized/Canonical Envelope Digest、C Object Payload Digest 与 Gateway Receipt Digest；不同 Digest 域不得无类型规则复用；
3. H 发布独立 Gateway Key Namespace 与 Key Status Event/Sequence 合同，不得复用 C/I Key ID 或 Sequence；
4. I 批准 H Trust Root Hierarchy、Issuer Registration、Signer/Subject/Owner-Authority Relation、Audience、Key Purpose、Key Status/History、Revocation/Compromise 优先级、Rotation、Custody、Anti-Rollback 与 Historical Verification；
5. H Gateway Signing Key 必须由批准的 KMS/HSM 或等效保护边界托管；私钥不得进入 Repository、Source Fixture 或 CI Secret Echo；
6. H 签发 Receipt 前，Protected Transport 必须认证原始 C Adapter；Gateway Attestation 不能追溯认证不可信 Sender；
7. Replay/Idempotency State 必须 Durable、Scoped、Crash-Safe；Same-Digest Replay 披露前必须重新检查 Current Authorization、Key Status、Scope 与 Forget Fence；
8. 至少两种独立实现对精确 H P0 Canonical Bytes/Digest/Signature 达成一致，逐字段变异必须使 Signature 失效；
9. Trust Registry、Key Status、Checkpoint、Transport Context 或 Replay State 未知/不可用为 UNKNOWN；已证明不匹配为 INVALID。禁止默认信任或算法降级。

## 4. I approval boundary / I 批准边界

This review does **not**:
- register an H profile;
- approve a production H gateway issuer, trust root, key or KMS/HSM;
- approve AIMBA-H-ENVELOPE-CRYPTO or any other profile identifier;
- authorize a gateway signer to act for C without explicit scoped delegation;
- approve the H reference callbacks as production trust services;
- close I permission, revocation, anti-rollback or final currentness gates.

本复审不：
- 注册 H Profile；
- 批准生产 H Gateway Issuer、Trust Root、Key 或 KMS/HSM；
- 批准 AIMBA-H-ENVELOPE-CRYPTO 或其他 Profile Identifier；
- 未经明确范围 Delegation 就授权 Gateway 代表 C；
- 将 H Reference Callback 批准为生产 Trust Service；
- 关闭 I Permission、Revocation、Anti-Rollback 或 Final Currentness Gate。

## 5. Final I disposition / I 最终结论

**Delegated I-role decision: ACCEPT C's separate H-gateway receipt/attestation model as the preferred trust-boundary candidate. I retains exclusive trust-root/registry/key-governance approval. No H profile, issuer, signer, key, custody or production deployment is registered or approved. NOT FROZEN.**

**角色模拟 I 侧决议：接受 C 的独立 H-Gateway Receipt/Attestation 模型作为优先 Trust-Boundary 候选。I 保留 Trust Root/Registry/Key Governance 的独占批准权。未注册或批准任何 H Profile、Issuer、Signer、Key、Custody 或生产部署。不冻结。**

---
**Provenance:** delegated I-role review authored in the coordinating session; not an independent human I Owner signature or formal governance registration.
