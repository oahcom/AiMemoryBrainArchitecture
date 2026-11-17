# Phase 3.8.21 — H Outer Envelope P0/Digest Reference Implementation
# Phase 3.8.21 — H 外层 Envelope P0/Digest Reference Implementation

- H authority: BMCP wire protocol / envelope verifier integration
- C corrected outer signer/P0 candidate: Blob `310e7e0073d3c32f594bc151f10c249c828ce30f`
- H exact JSON-Pointer mapping: Blob `4ba7e1699215d02224f805a15484b1da2e40c03f`
- H schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H envelope auth validator current Blob: `571f69d326be51fd80acfe0c5a3f5f2dddce61f4`
- H envelope auth tests current Blob: `babe51825d6aa13693e9cf844740104c74f598d8`
- H exact branch HEAD: `39dce3db0375bec6af4804c2403e1248fee2171f`
- Test methods in the updated envelope-auth test file: 28
- CI: **NOT YET OBSERVED FOR THIS HEAD / NO PASS CLAIM**
- Status: **REFERENCE P0/DIGEST IMPLEMENTATION CANDIDATE; CRYPTOGRAPHIC SIGNATURE AND TRUST STILL CALLBACK-BASED; NOT PRODUCTION**
- Provenance: delegated H-role source implementation; not an independent human H Owner acceptance.

## 1. Changes / 变更

The H envelope-auth reference gate now derives the C outer-envelope P0 from an explicit allowlist aligned to H Unified 1.2.14 `commonEnvelope` plus the `C_PROVIDER_OUTCOME_RECORDED` message branch.

It computes:
- JCS canonical bytes for the exact P0;
- SHA-256 over the C envelope-specific payload domain tag and P0 bytes;
- the exact candidate Ed25519 signature preimage over the profile ID, message-family domain and signed projection.

The computed digest must equal the transmitted outer `payload_digest` before signature verification is called. The signature callback receives the exact computed preimage through the preferred `verify_envelope_signature(envelope, preimage, protected_context)` seam. A legacy integrity callback remains as a compatibility seam but is invoked only after the local P0 digest has been recomputed and matched.

H Envelope-Auth Reference Gate 现在根据显式 Allowlist 派生 C Outer-Envelope P0，该 Allowlist 与 H Unified 1.2.14 `commonEnvelope` 及 `C_PROVIDER_OUTCOME_RECORDED` Message Branch 对齐。

它计算：
- 精确 P0 的 JCS Canonical Bytes；
- 对 C Envelope 专属 Payload Domain Tag 与 P0 Bytes 执行 SHA-256；
- 对 Profile ID、Message-Family Domain 与 Signed Projection 构造精确候选 Ed25519 Signature Preimage。

在调用 Signature Verification 前，计算出的 Digest 必须等于传入 Outer `payload_digest`。Signature Callback 通过优先接口 `verify_envelope_signature(envelope, preimage, protected_context)` 接收精确计算的 Preimage。保留 Legacy Integrity Callback 兼容接口，但只在本地 P0 Digest 重算并匹配后调用。

## 2. P0 rules implemented / 已实现的 P0 规则

- Exact C outer-envelope profile ID: `AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0`.
- Exact canonicalization candidate: `RFC8785-JCS-1.0`.
- Exact message family: `C_PROVIDER_OUTCOME_RECORDED`.
- Both `integrity_proof_ref` and `channel_binding_proof_ref` are signed P0 members.
- Coordinator-appended `coc_commit_proof_ref`, `coc_record_ref`, `coc_record_position`, `coc_entry_digest`, and `coc_previous_entry_digest` are excluded from C-origin P0 and must be independently verified.
- Unknown/unclassified outer-envelope members are rejected rather than silently omitted.
- Required common envelope identity, profile, digest, key, proof and signature fields are checked.
- C origin principal is mandatory for this C message family. An H gateway receipt cannot be accepted as the C origin signature.

- 精确 C Outer-Envelope Profile ID：`AIMBA-C-BMCP-ENVELOPE-CRYPTO-1.0`。
- 精确 Canonicalization Candidate：`RFC8785-JCS-1.0`。
- 精确 Message Family：`C_PROVIDER_OUTCOME_RECORDED`。
- `integrity_proof_ref` 与 `channel_binding_proof_ref` 均为 Signed P0 成员。
- Coordinator 后续追加的 `coc_commit_proof_ref`、`coc_record_ref`、`coc_record_position`、`coc_entry_digest`、`coc_previous_entry_digest` 从 C-origin P0 排除，必须独立验证。
- 未知/未分类 Outer-Envelope Member 被拒绝，不会静默遗漏。
- 检查必需 Common Envelope Identity、Profile、Digest、Key、Proof 与 Signature Field。
- 此 C Message Family 必须使用 C Origin Principal；H Gateway Receipt 不得被当作 C Origin Signature。

## 3. C origin binding / C Origin Binding

The reference gate now rejects the C_PROVIDER_OUTCOME_RECORDED message if the protected transport context is not a C authority principal or the envelope owner_authority is not C. This closes the prior reference-test ambiguity that allowed an H gateway transport identity to be treated as an origin signer. H gateway attestation remains a separate additive message and requires its own H-owned profile and record.

Reference Gate 现在会拒绝 Protected Transport Context 不是 C Authority Principal 或 Envelope `owner_authority` 不为 C 的 C_PROVIDER_OUTCOME_RECORDED Message。这关闭了此前 Reference Test 中 H Gateway Transport Identity 可能被当作 Origin Signer 的歧义。H Gateway Attestation 仍是独立附加 Message，需要自身 H-owned Profile 与 Record。

## 4. Updated test coverage / 更新测试覆盖

The envelope-auth test file now contains 28 methods, including:
- existing strict parse, protected-context, key-status, channel-binding, identity and replay tri-state behavior;
- replay reservation ordering and authenticated wrapper ordering;
- C origin principal enforcement; gateway identity is rejected as C origin;
- outer P0 digest mismatch rejected before signature callback;
- integrity/channel-binding proof locator mutation changes P0 digest;
- coordinator-appended COC fields do not change the C-origin P0 digest;
- unclassified outer-envelope member rejected;
- wrong C outer-envelope profile ID rejected;
- signature callback receives the exact computed candidate preimage.

Envelope-Auth Test File 当前包含 28 个方法，覆盖既有 Strict Parse、Protected Context、Key Status、Channel Binding、Identity、Replay 三态行为；Replay Reservation/Authenticated Wrapper 顺序；C Origin Principal 强制；H Gateway Identity 不得作为 C Origin；P0 Digest Mismatch 在 Signature Callback 前拒绝；Integrity/Channel-Binding Locator 变异会改变 P0 Digest；Coordinator 追加 COC Field 不改变 C-origin P0 Digest；Unclassified Member 与错误 Profile ID 拒绝；Signature Callback 收到精确候选 Preimage。

## 5. Important limits / 重要限制

This is a reference P0/digest construction and callback orchestration. It does **not** implement or prove:
- Ed25519 cryptographic verification;
- I-approved profile registration, trust roots or C key registry;
- key lifecycle, revocation, compromise-time/historical verification or anti-rollback;
- real protected transport/session identity or channel-binding proof verification;
- durable replay/idempotency ledger;
- schema validation at this early authentication gate (downstream authenticated wrapper still runs the H/C schema/domain validator);
- Storage durable authenticated ingress, COC quorum or same-GID resolution;
- production runtime or distributed failure behavior.

这是 Reference P0/Digest Construction 与 Callback Orchestration，**没有**实现或证明：
- Ed25519 密码学验证；
- I-approved Profile Registration、Trust Root 或 C Key Registry；
- Key Lifecycle、Revocation、Compromise-Time/Historical Verification 或 Anti-rollback；
- 真实 Protected Transport/Session Identity 或 Channel-Binding Proof Verification；
- Durable Replay/Idempotency Ledger；
- 此早期 Authentication Gate 的 Schema Validation（下游 Authenticated Wrapper 仍会运行 H/C Schema/Domain Validator）；
- Storage Durable Authenticated Ingress、COC Quorum 或 Same-GID Resolution；
- Production Runtime 或 Distributed Failure 行为。

## 6. CI and acceptance / CI 与验收

The workflow path filters include the modified validator and test directory. The exact current H branch commit is `7a666e93c08424e21342bea5f6f291a59f93f34e`. At the time of this record, the GitHub combined commit status returned no status entries and the commit-workflow lookup returned no workflow runs. Therefore **CI for this updated source has not been observed and no test pass is claimed**. The previous 60-test run `44073888935` applies only to its older exact source Blobs, not this P0/digest change.

Workflow Path Filter 包含已修改的 Validator 与 Test Directory。H 当前精确 Branch Commit 为 `7a666e93c08424e21342bea5f6f291a59f93f34e`。本记录时 GitHub Combined Commit Status 没有 Status Entry，Commit Workflow Lookup 也没有返回 Workflow Run。因此**尚未观察到此更新源码的 CI，不声明测试通过**。此前 60 项 Run `44073888935` 仅适用于其旧精确 Source Blob，不适用于本次 P0/Digest 变更。

## 7. H disposition / H 结论

**Accept as a bounded reference P0/digest implementation candidate. Exact current-source CI, C independent Owner acceptance, I formal profile registration, real cryptographic verifier, protected transport and durable replay/Storage integration remain OPEN. No production authentication or Gate promotion is claimed.**
