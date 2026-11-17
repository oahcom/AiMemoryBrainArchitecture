# Phase 3.8.15 — I Review of H Expanded Full-Path and Envelope Authentication Boundary
# Phase 3.8.15 — I 对 H 扩展 Full-Path 与 Envelope Authentication 边界的复审

- Owner: I — Security, Identity and Governance
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H authority-join mapping Blob: `1cbe74eba69325510d6b1019d971661f965eabf8`
- I P0 allowlist Blob: `44986f5f864bcdc1a79d34978273644d381a68c0`
- H validator core Blob: `eab961a08d41e871f38543b18ee60cf024977414`
- H expanded test Blob: `540056d7c4f290c31290b17c264c69cfd76b1cb2`
- H full fixture Blob: `f911027c848d21dd36fb87ba64a201a1455787a7`
- H expanded closure Blob: `60e5eb98a07efcf87bc3f2be6fcf7fedb2196504`
- H CI run `44070924346`, exact commit `77a9d5e2e716ba33387f0beb1195f864ed8ac54f`: **SUCCESS**
- Decision: **ACCEPT LOCAL I CALLBACK BOUNDARY AS TESTED INTERFACE ONLY; OUTER ENVELOPE AUTHENTICATION AND PRODUCTION I PROOF OPEN**
- Provenance: delegated I-role review; not independent human I Owner/governance approval.

## 1. I terminal proof boundary / I Terminal Proof 边界

I accepts that tests 29 and 24/25 exercise the callback boundary for I terminal decision: a test callback rejects REVOCATION_WON where provider invocation requires COMMIT_WON, missing callback yields UNKNOWN, and explicit contradiction yields INVALID. The fixture's I terminal ref is a synthetic locator; it is not an I-signed proof and does not authenticate PolicyDomain, operation, participant, receipt consumption, PermissionEpoch, key status or anti-rollback.

I 接受 Test 29 与 Test 24/25 对 I Terminal Callback 边界的测试：Provider Invocation 需要 COMMIT_WON 时拒绝 REVOCATION_WON；Callback 缺失为 UNKNOWN；明确矛盾为 INVALID。Fixture 的 I Terminal Ref 只是合成定位符，不是 I 签名 Proof，也不认证 PolicyDomain、Operation、Participant、Receipt Consumption、PermissionEpoch、Key Status 或 Anti-Rollback。

## 2. Outer envelope authentication is not covered / 外层 Envelope Authentication 未覆盖

The H common envelope requires payload_digest, integrity_proof_ref, channel_binding_proof_ref, key_id_ref, key_version and signature. The Provider Outcome validator full-path tests load the schema but do not authenticate the outer H envelope signature/integrity or compare payload identity assertions with the authenticated transport principal.

I requires a distinct H Gateway/Auth validation step before any durable acceptance:
- verify the canonical envelope payload digest and signature under an approved profile;
- authenticate the channel-binding proof and issuer key status;
- bind sender_authority_ref/sender_subject_ref/issuer_ref to the authenticated transport principal and registered authority;
- reject duplicate/replay, stale key, wrong audience, policy-domain mismatch and signature/digest substitution;
- preserve a clear ordering: outer envelope authentication → H/C schema and C-P0 validation → C/I/D/Storage authority joins.

H Common Envelope 要求 payload_digest、integrity_proof_ref、channel_binding_proof_ref、key_id_ref、key_version 和 signature。Provider Outcome Full-Path Test 虽加载 Schema，但未认证外层 H Envelope Signature/Integrity，也未将 Payload Identity Assertion 与 Authenticated Transport Principal 比对。

I 要求在任何 Durable Acceptance 前存在独立 H Gateway/Auth 校验步骤：验证规范 Envelope Digest/Signature、Channel Binding、Issuer Key Status；将 Sender/Issuer 身份绑定到认证 Transport Principal 和注册 Authority；拒绝 Replay、Stale Key、错误 Audience、PolicyDomain 不匹配和 Digest/Signature 替换；执行清晰顺序：外层认证 → H/C Schema 与 C-P0 校验 → C/I/D/Storage Authority Join。

## 3. I disposition / I 侧结论

**Delegated I-role decision: ACCEPT H's local I callback test boundary as L1/L2 evidence only. Outer envelope authentication, production I terminal proof verifier, trust roots, key custody, historical verification and anti-rollback remain OPEN. NOT FROZEN.**

I36-GOV-01..10 remain GOVERNANCE-BLOCKED. No Multi-PolicyDomain, Global Forget, physical erasure or production activation is authorized. This review is not an independent human I Owner signature.

**角色模拟 I 侧结论：仅接受 H 本地 I Callback 测试边界作为 L1/L2 证据。外层 Envelope Authentication、生产 I Terminal Proof Verifier、Trust Root、Key Custody、Historical Verification 和 Anti-Rollback 仍 OPEN，不冻结。** I36-GOV-01..10 继续 GOVERNANCE-BLOCKED，不授权 Multi-PolicyDomain、Global Forget、物理擦除或生产激活。
