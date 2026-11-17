# Phase 3.8.19 — I Exact Review: Corrected C Outer Envelope P0
# Phase 3.8.19 — I 精确复审：修正后的 C Outer Envelope P0

- C exact corrected decision Blob: 310e7e0073d3c32f594bc151f10c249c828ce30f
- H exact P0 mapping Blob: 4ba7e1699215d02224f805a15484b1da2e40c03f
- H Unified schema 1.2.14 Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- Prior I review Blob: b6d1ea45825a1c2090abfba42474814f02f073a3
- Disposition: **ACCEPT CORRECTED TWO-SIGNED-OBJECT SEPARATION AS CANDIDATE; I CRYPTO REGISTRATION / TRUST POLICY NOT APPROVED**
- Provenance: delegated I-role exact review; not an independent human I Owner or governance approval.

## 1. Exact correction reviewed / 精确修正复审

The corrected C candidate now explicitly includes both `integrity_proof_ref` and `channel_binding_proof_ref` in the outer-envelope P0 allowlist. H's exact JSON-Pointer mapping binds these as `/integrity_proof_ref` and `/channel_binding_proof_ref`. This closes the prior field-inventory omission at the architecture-document level.

I confirms the intended separation:
- C envelope signature authenticates the C-originated BMCP message projection.
- C object signature authenticates the immutable CSubmitOutcome semantic object.
- I trust registry authenticates the C issuer/key/profile and current/historical key status.
- H verifies exact wire projection and protected channel/session binding.
- Storage persists accepted ingress only after all required verification succeeds.

修正后的 C Candidate 已将 `integrity_proof_ref` 与 `channel_binding_proof_ref` 明确纳入 Outer-Envelope P0 Allowlist。H 的精确 JSON-Pointer Mapping 将其绑定为 `/integrity_proof_ref` 与 `/channel_binding_proof_ref`。这在架构文档层面关闭了此前的字段清单遗漏。

I 确认以下分离：
- C Envelope Signature 认证 C-originated BMCP Message Projection。
- C Object Signature 认证不可变 CSubmitOutcome Semantic Object。
- I Trust Registry 认证 C Issuer/Key/Profile 与当前/历史 Key Status。
- H 验证精确 Wire Projection 与 Protected Channel/Session Binding。
- Storage 仅在所有必需验证成功后持久化接受 Ingress。

## 2. Security conditions remain / 安全条件仍未关闭

This review does not approve:
- RFC8785/SHA-256/Ed25519 production suitability;
- profile registration or production signer authorization;
- trust roots, C workload principal registration or key custody;
- HSM/KMS, rotation, revocation, compromise-time and historical verification policy;
- anti-rollback checkpoint or replay-ledger implementation;
- authenticated transport adapter, gateway verifier or Storage durable ingress;
- executable signature, channel-binding, replay or failure-injection tests.

本复审不批准：
- RFC8785/SHA-256/Ed25519 的生产适用性；
- Profile Registration 或生产 Signer Authorization；
- Trust Root、C Workload Principal Registration 或 Key Custody；
- HSM/KMS、Rotation、Revocation、Compromise-Time 与 Historical Verification Policy；
- Anti-rollback Checkpoint 或 Replay-Ledger Implementation；
- Authenticated Transport Adapter、Gateway Verifier 或 Storage Durable Ingress；
- 可执行 Signature、Channel-Binding、Replay 或 Failure-Injection Test。

## 3. Required fail-closed outcomes / 必须 Fail-Closed 的结果

- missing/unavailable trust profile, principal context, key history, anti-rollback or replay authority → UNKNOWN;
- invalid signature/digest, wrong issuer/principal/audience/purpose, revoked/compromised key, channel-binding mismatch or replay → INVALID;
- C object signature and outer envelope signature are both independently required;
- an H gateway receipt cannot substitute for C origin signature;
- C origin signature does not prove provider truth or any I/D/Storage/COC fact.

- Trust Profile、Principal Context、Key History、Anti-rollback 或 Replay Authority 缺失/不可用 → UNKNOWN；
- Signature/Digest 无效、Issuer/Principal/Audience/Purpose 错误、Key Revoked/Compromised、Channel-Binding 不匹配或 Replay → INVALID；
- C Object Signature 与 Outer Envelope Signature 必须独立验证；
- H Gateway Receipt 不得替代 C Origin Signature；
- C Origin Signature 不证明 Provider Truth 或任何 I/D/Storage/COC 事实。

## 4. I disposition / I 结论

**ACCEPT the corrected C two-signed-object architecture and corrected proof-reference P0 inventory as candidates. I retains all cryptographic governance and trust-registration authority. No profile is registered, no production key is authorized, and no production Gate is advanced.**
