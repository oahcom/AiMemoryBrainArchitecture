# Phase 3.8.17 — I Review: H Outer Envelope Authentication and Protected Identity Boundary
# Phase 3.8.17 — I 复审：H 外层 Envelope Authentication 与 Protected Identity 边界

- I authority: Security, Identity and Governance
- H gap/decision contract Blob: fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1
- H Unified 1.2.14 schema Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- I P0 allowlist baseline Blob: 44986f5f864bcdc1a79d34978273644d381a68c0
- Status: **ACCEPT GAP IDENTIFICATION; I TRUST/PRINCIPAL/KEY POLICY REMAINS I-OWNED; NO C PROFILE REUSE**
- Provenance: delegated I-role review; not an independent human I Owner or governance approval.

## 1. Authentication must be outside the payload / Authentication 必须来自 Payload 之外

I confirms that payload sender/issuer/subject/key/audience fields are untrusted claims. H must obtain protected transport/session/workload verifier context outside the payload, and I must validate issuer trust, principal binding, audience, credential/key status, validity, revocation, delegation and authorization under I policy.

I 确认 Payload Sender/Issuer/Subject/Key/Audience 字段是不可信 Claim。H 必须从 Payload 之外取得受保护 Transport/Session/Workload Verifier Context；I 必须按 I Policy 验证 Issuer Trust、Principal Binding、Audience、Credential/Key Status、Validity、Revocation、Delegation 与 Authorization。

## 2. Profile ownership separation / Profile 权属分离

AIMBA-I-CRYPTO-1.0 is an I-owned profile for I-signed records. It must not be applied to C-originated BMCP envelope semantics merely because I owns the trust registry. I's trust registry may validate an issuer/key under an explicitly registered profile, but it does not redefine C's signed object semantics or choose C's envelope P0.

AIMBA-I-CRYPTO-1.0 是 I 自有的 I-signed Record Profile。不得仅因 I 拥有 Trust Registry，就将其应用到 C-originated BMCP Envelope 语义。I Trust Registry 可以在明确注册的 Profile 下验证 Issuer/Key，但不能重定义 C 的 Signed Object 语义，也不能替 C 选择 Envelope P0。

C must identify the signer and publish the exact C-owned envelope profile/P0 if C signs the envelope. H defines wire mapping and transport integration. I approves trust-root registration, credential/key status/history, revocation, principal/audience binding, anti-rollback and authorization policy within I's authority.

如果 C 签署 Envelope，C 必须明确 Signer 并发布精确 C-owned Envelope Profile/P0。H 定义 Wire Mapping 与 Transport Integration。I 在自身权威范围内批准 Trust Root Registration、Credential/Key Status/History、Revocation、Principal/Audience Binding、Anti-Rollback 与 Authorization Policy。

## 3. Required verifier behavior / 必需 Verifier 行为

- missing protected verifier context, unregistered profile, unavailable key status/history or unavailable replay authority → UNKNOWN;
- invalid signature, revoked/compromised key, principal/issuer/subject/audience mismatch, nonce replay or invalid channel binding → INVALID;
- payload-supplied key/profile/issuer must never override authenticated configuration;
- signature verification must bind the exact signed object and message family;
- outer-envelope authentication and C object authentication are independent required checks.

- 缺少 Protected Verifier Context、Profile 未注册、Key Status/History 不可用或 Replay Authority 不可用 → UNKNOWN；
- Signature 无效、Key 已 Revoked/Compromised、Principal/Issuer/Subject/Audience 不匹配、Nonce Replay 或 Channel Binding 无效 → INVALID；
- Payload 提供的 Key/Profile/Issuer 不得覆盖已认证配置；
- Signature Verification 必须绑定精确 Signed Object 与 Message Family；
- Outer Envelope Authentication 与 C Object Authentication 是彼此独立的必需检查。

## 4. I disposition / I 侧结论

**Delegated I-role decision: ACCEPT H's outer-envelope authentication gap and protected identity boundary. I retains sole authority for trust roots, principal binding, key lifecycle, revocation/history, anti-rollback and authorization. I does not approve reuse of AIMBA-I-CRYPTO-1.0 for C-originated envelopes.**
