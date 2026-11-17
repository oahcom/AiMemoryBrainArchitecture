# Phase 3.8.18 — I Review: C Outer BMCP Envelope Signer/P0 and Trust Registration
# Phase 3.8.18 — I 复审：C 外层 BMCP Envelope Signer/P0 与 Trust Registration

- I authority: Security, Identity, Cryptographic Governance
- C decision candidate Blob: 6347c9aa80bb48adb2e2e4f318960e14ba16f33e
- H Unified 1.2.14 schema Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- C object profile candidate Blob: 44641b4b01d721c47e08ae9380ffe645bb3ccda0
- Status: **ACCEPT SEPARATION / SIGNER OWNERSHIP AS CANDIDATE; CRYPTO SUITE AND TRUST REGISTRATION NOT APPROVED**
- Provenance: delegated I-role review; not an independent human I Owner or security-governance approval.

## 1. I decision / I 决策

I accepts the architecture separation that C is the origin signer for C_PROVIDER_OUTCOME_RECORDED and that the outer BMCP envelope and immutable CSubmitOutcome object are two distinct signed objects with two distinct P0 projections. I does not object to C owning the message-family semantics and envelope signer role.

I accepts the *candidate shape* of a separately named C envelope profile only as a proposal for cryptographic governance review. The proposed RFC8785 JCS / SHA-256 / Ed25519 primitives are not approved for production by this review. I makes no determination here that the suite is suitable for all deployment threat models.

I 接受以下架构分离：C 是 C_PROVIDER_OUTCOME_RECORDED 的 Origin Signer；外层 BMCP Envelope 与不可变 CSubmitOutcome Object 是两个不同 Signed Object，具有两个不同 P0 Projection。I 不反对 C 拥有 Message-Family 语义与 Envelope Signer 角色。

I 仅将独立命名的 C Envelope Profile 候选形态作为待密码学治理审查的提案。拟议 RFC8785 JCS / SHA-256 / Ed25519 Primitive 不因本复审而获得生产批准。本复审不判定该套件适用于所有部署威胁模型。

## 2. I-owned approval boundary / I 自有批准边界

Before a C envelope profile can be registered or used, I requires:
1. exact profile identifier/version, allowed message family, purpose, audience and signer authority;
2. approved algorithm suite and parameter constraints, canonicalization implementation profile and signature encoding;
3. trusted C issuer identity and workload/adapter principal binding;
4. key generation, custody, access control, HSM/KMS policy, rotation and destruction controls;
5. key status/history model, effective-time semantics, revocation/compromise ordering, historical verification and archive retention;
6. anti-rollback checkpoint/anchor and restore/failover behavior;
7. cross-profile and cross-message replay protections, key-purpose separation and downgrade rejection;
8. independent Python/Node (or equivalent) byte-identical P0/digest/preimage/signature vectors and negative tests;
9. incident response and emergency key revocation procedure.

C owns the signed message semantics and exact P0. I's registry authenticates which C principal/key may sign the profile at a given time; I must not silently alter C's field projection. H implements wire extraction and verification but does not become the C signer.

在 C Envelope Profile 注册或使用前，I 要求：
1. 精确 Profile Identifier/Version、允许的 Message Family、Purpose、Audience 与 Signer Authority；
2. 已批准算法套件与参数约束、Canonicalization Implementation Profile、Signature Encoding；
3. 可信 C Issuer Identity 与 Workload/Adapter Principal Binding；
4. Key Generation、Custody、Access Control、HSM/KMS Policy、Rotation 与 Destruction Controls；
5. Key Status/History Model、Effective-Time Semantics、Revocation/Compromise Ordering、Historical Verification 与 Archive Retention；
6. Anti-rollback Checkpoint/Anchor 与 Restore/Failover 行为；
7. Cross-Profile/Cross-Message Replay Protection、Key-Purpose Separation 与 Downgrade Rejection；
8. 独立 Python/Node（或等价）逐字节一致 P0/Digest/Preimage/Signature 向量与 Negative Test；
9. Incident Response 与 Emergency Key Revocation Procedure。

C 拥有 Signed Message 语义与精确 P0。I Registry 认证某一时点允许哪个 C Principal/Key 签署该 Profile；I 不得静默改变 C Field Projection。H 实现 Wire Extraction/Verification，但不成为 C Signer。

## 3. Required security semantics / 必需安全语义

- payload key/profile/issuer claims are never trust roots; resolve them through authenticated configuration and I-authoritative registry.
- missing/unavailable trust profile, key history, anti-rollback anchor or authenticated principal => UNKNOWN, never VALID.
- invalid signature, wrong issuer/principal/audience/purpose, revoked/compromised key, profile downgrade or replay => INVALID.
- channel binding must compare against protected session context outside the payload.
- C object signature and C envelope signature are both independently required; one cannot substitute for the other.
- H gateway attestation is a distinct H-originated receipt and cannot be treated as C origin signature.
- I does not vouch for provider truth; C-owned evidence must independently prove provider outcome.

- Payload Key/Profile/Issuer Claim 永远不是 Trust Root；必须通过已认证配置与 I 权威 Registry 解析。
- Trust Profile、Key History、Anti-rollback Anchor 或 Authenticated Principal 缺失/不可用 → UNKNOWN，绝不 VALID。
- Signature 无效、Issuer/Principal/Audience/Purpose 错误、Key Revoked/Compromised、Profile Downgrade 或 Replay → INVALID。
- Channel Binding 必须与 Payload 之外的 Protected Session Context 比较。
- C Object Signature 与 C Envelope Signature 均需独立验证，不能互相替代。
- H Gateway Attestation 是独立 H-originated Receipt，不得当作 C Origin Signature。
- I 不为 Provider Truth 背书；必须由 C-owned Evidence 独立证明 Provider Outcome。

## 4. I disposition / I 侧结论

**ACCEPT C's separate origin-signer/P0 architecture as a candidate. I DOES NOT APPROVE the proposed crypto suite for production, register the profile, register keys, approve key custody, or authorize deployment.** A formal I security-governance decision and profile registration are still required.
