# Phase 3.8.18 — I Review: H Explicit Outer Signature-Profile Requirement
# Phase 3.8.18 — I 复审：H 外层 Signature-Profile 明确要求

- Owner perspective: I — Security, Identity and Governance
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H envelope auth validator Blob: `a863acd01abcb147db2bd23a3b8bb1985d81bc78`
- H Provider Outcome validator Blob: `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth test Blob: `3469c5268d3558c777ea9f16058e00570517ff54`
- H Provider Outcome test Blob: `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H Phase 3.8.20 closure Blob: `73543e8e7963f1442931c318542a4249d1c41790`
- H CI run `44075215559`, commit `a36c34897545316942c7cda8da5d8bea7dacec5b`, job `134011346259`: **63 tests / SUCCESS**
- Decision: **ACCEPT REQUIRED PROFILE-ID FIELD AND TRI-STATE REGISTRY SEMANTICS; DO NOT REGISTER A PROFILE OR TRUST ROOT**
- Provenance: delegated I-role review; **not an independent human I Owner signature or governance approval**.

## 1. I governance rule / I 治理规则

I accepts a non-empty `signature_profile_id` as a required semantic field for protected owner-signed envelopes. The identifier is not self-authenticating. It must resolve through an I-governed registry binding issuer, signer role, key ID/version, profile, algorithm, canonicalization and key lifecycle status.

I 接受非空 `signature_profile_id` 作为受保护 Owner-signed Envelope 的必需语义字段。该 Identifier 本身不具备认证能力，必须通过 I 治理 Registry 解析 Issuer、Signer Role、Key ID/Version、Profile、Algorithm、Canonicalization 与 Key Lifecycle Status 的绑定。

## 2. Required tri-state / 必需三态

- missing/empty identifier: INVALID;
- known, authenticated but unregistered, revoked, expired or mismatched profile/key: INVALID;
- registry unavailable, historical key status unavailable, profile unknown or anti-rollback checkpoint unavailable: UNKNOWN;
- exact profile/key/issuer/role binding verified under current I policy: TRUE for this callback only, not a global approval.

- Identifier 缺失/为空：INVALID；
- 已知且已认证但未注册、撤销、过期或不匹配的 Profile/Key：INVALID；
- Registry 不可用、历史 Key Status 不可用、Profile 未知或 Anti-Rollback Checkpoint 不可用：UNKNOWN；
- 精确 Profile/Key/Issuer/Role 绑定通过当前 I Policy：仅该 Callback 返回 TRUE，不构成全局批准。

The envelope integrity verifier must not infer signature profile from `canonicalization_profile_id`, trust a payload-selected algorithm or silently fall back to C's object profile. If `signature_profile_id` is present, it must match the I-governed registry entry.

Envelope Integrity Verifier 不得从 `canonicalization_profile_id` 推断 Signature Profile，不得信任 Payload 自选算法，也不得静默回退到 C Object Profile。若存在 `signature_profile_id`，必须与 I-governed Registry Entry 一致。

## 3. No production approval / 不批准生产部署

This review does not register a profile, select the C adapter/H gateway/separate attestor, approve a trust root, authorize KMS/HSM custody, key rotation/revocation/compromise recovery, historical verification or production transport/replay deployment. Signer-role and outer P0 decisions remain OPEN pending explicit C/H/I agreement and independent governance.

本复审不注册 Profile、不选择 C Adapter/H Gateway/独立 Attestor、不批准 Trust Root、不授权 KMS/HSM Custody、Key Rotation/Revocation/Compromise Recovery、Historical Verification 或生产 Transport/Replay 部署。Signer Role 与 Outer P0 决策仍 OPEN，等待 C/H/I 明确一致及独立治理。

## 4. I decision / I 侧决议

**Delegated I-role decision: ACCEPT the explicit profile identifier and tri-state registry semantics as a candidate fail-closed contract. Production profile registration, trust root, signer-role policy, key lifecycle, historical verification and anti-rollback remain OPEN. NOT FROZEN.**

I36-GOV-01..10 remain GOVERNANCE-BLOCKED. No Multi-PolicyDomain, Global Forget, physical erasure or production activation is authorized.

**角色模拟 I 侧决议：接受显式 Profile Identifier 与三态 Registry 语义作为候选 fail-closed 合同。Production Profile Registration、Trust Root、Signer Role Policy、Key Lifecycle、Historical Verification 与 Anti-Rollback 仍 OPEN，不冻结。**

I36-GOV-01..10 继续 GOVERNANCE-BLOCKED。不授权 Multi-PolicyDomain、Global Forget、物理擦除或生产激活。
