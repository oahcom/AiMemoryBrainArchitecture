# Phase 3.8.17 — I Review: H Outer-Envelope Authenticated Ingress Gate
# Phase 3.8.17 — I 复审：H 外层 Envelope 认证 Ingress Gate

- Owner perspective: I — Security, Identity and Governance
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H identity-binding baseline Blob: `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- I trust/identity governance authority: I-owned; no production trust root registered by this review
- H envelope auth validator Blob: `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- H Provider Outcome validator Blob: `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth test Blob: `ddf34e9c30edfc378a9482a30837ce04c4abcf97`
- H Provider Outcome test Blob: `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H exact closure Blob: `860c896a388597a4378eda5aa323f276390acf34`
- H CI run `44073888935`, commit `0e212731073b36e4fa9ffda8467e60806da1b380`, job `134006790527`: **60 tests / SUCCESS**
- Decision: **ACCEPT TRI-STATE TRUST/IDENTITY CALLBACK BOUNDARY AS TESTED INTERFACE ONLY; TRUST PROFILE / SIGNER / PRODUCTION VERIFICATION OPEN**
- Provenance: delegated I-role review; **not an independent human I Owner signature or governance approval**.

## 1. I security authority / I 安全权威

I owns issuer trust, Principal resolution, credential/key status, audience policy, validity, revocation, delegation, authorization and approved trust/key lifecycle. H obtains protected transport/session verifier context and binds it to the envelope; H must not mint or independently approve trust decisions.

I 独占 Issuer Trust、Principal Resolution、Credential/Key Status、Audience Policy、Validity、Revocation、Delegation、Authorization 与批准的 Trust/Key Lifecycle。H 获取 Protected Transport/Session Verifier Context 并绑定 Envelope，但不得自行签发或批准 Trust Decision。

## 2. Review of H callback contract / H Callback 合同复审

I accepts the candidate separation:
- `verify_envelope_integrity` must verify the exact outer envelope digest/signature/preimage under an I-approved and signer-authorized profile; the profile must be resolved from authenticated key/issuer configuration, never payload-selected.
- `verify_key_status` must check signing-time and current key status, revocation/compromise/retirement history, and anti-rollback.
- `verify_channel_binding` must authenticate the exact protected session/channel proof.
- `verify_identity_binding` must resolve issuer, sender authority, sender subject, subject_ref, owner_authority and the allowed signer-to-owner relationship through trusted registries.
- `check_and_reserve_replay` must use durable replay state bound to message ID, nonce, digest, audience, authenticated principal/session and signer; missing state is UNKNOWN.
- A verifier False is INVALID; missing/unavailable/unknown profile or trust state is UNKNOWN; no payload mirror may become authentication fallback.

I 接受候选职责分离：
- `verify_envelope_integrity` 必须在 I 批准且 Signer 获授权的 Profile 下验证精确 Outer Envelope Digest/Signature/Preimage；Profile 必须从认证 Key/Issuer 配置解析，不能由 Payload 自选；
- `verify_key_status` 必须检查签名时与当前 Key Status、Revocation/Compromise/Retirement 历史和 Anti-Rollback；
- `verify_channel_binding` 必须认证精确 Protected Session/Channel Proof；
- `verify_identity_binding` 必须通过可信 Registry 解析 Issuer、Sender Authority、Sender Subject、subject_ref、owner_authority 及允许的 Signer-to-Owner 关系；
- `check_and_reserve_replay` 必须使用绑定 Message ID/Nonce/Digest/Audience/Authenticated Principal/Session/Signer 的持久 Replay State；状态缺失为 UNKNOWN；
- Verifier False=INVALID；Verifier 缺失/不可用/Profile 或 Trust 未知=UNKNOWN；禁止 Payload Mirror 作为 Authentication Fallback。

I confirms the code no longer hardcodes `owner_authority == authenticated sender authority kind`. This is required because a C-owned record and its transport signer/attestor are different roles; only I-approved registry policy may authorize the relationship. Test 17 is not an I authorization decision.

I 确认代码不再硬编码 `owner_authority == authenticated sender authority kind`。这是必要的，因为 C-owned Record 与 Transport Signer/Attestor 是不同角色；仅 I 批准的 Registry Policy 可授权其关系。Test 17 不是 I 授权决策。

## 3. Ordering and replay / 顺序与 Replay

I accepts the fail-closed sequence as an interface candidate: strict parse → protected context → direct issuer/sender/audience/channel claim comparison → integrity/profile → key status → channel binding → identity registry → durable replay check/reservation → H/C schema/C-P0 and owner-authority joins. Replay reservation MUST NOT occur when signature/key/identity/channel verification is INVALID or UNKNOWN. Same-digest replay returns prior durable result; it must not repeat provider side effects.

I 接受该 fail-closed 顺序作为接口候选：Strict Parse → Protected Context → Issuer/Sender/Audience/Channel Claim 比较 → Integrity/Profile → Key Status → Channel Binding → Identity Registry → Durable Replay Check/Reservation → H/C Schema/C-P0 与 Owner Authority Join。Signature/Key/Identity/Channel Verification 为 INVALID 或 UNKNOWN 时不得预留 Replay。Same-Digest Replay 返回既有 Durable Result，不得重复 Provider Side Effect。

## 4. Explicit non-approvals / 明确不批准事项

This review does NOT:
- register or approve a production trust root, signature profile or algorithm;
- choose whether C adapter, H gateway or a separate attestor signs the outer envelope;
- approve C profile reuse for the outer envelope;
- approve KMS/HSM custody, key rotation/revocation/compromise recovery or historical verification implementation;
- certify the transport verifier, channel-binding service or durable replay ledger;
- approve outer-envelope P0 field projection or signature preimage;
- authorize production durable acceptance, Gate A/B/C transition or activation.

本复审不注册/批准生产 Trust Root、Signature Profile 或算法；不选择 C Adapter/H Gateway/独立 Attestor 作为 Outer Signer；不批准 C Profile 复用；不批准 KMS/HSM Custody、Key Rotation/Revocation/Compromise Recovery 或 Historical Verification 实现；不认证 Transport Verifier、Channel Binding Service 或 Durable Replay Ledger；不批准 Outer Envelope P0 Projection/Signature Preimage；不授权生产 Durable Acceptance、Gate A/B/C 迁移或激活。

## 5. I disposition / I 侧决议

**Delegated I-role decision: ACCEPT H's tri-state outer-envelope authentication and replay callback separation as a candidate interface and local L1/L2 test evidence only. Production trust root, signer-role policy, profile registration, key lifecycle, historical verification, anti-rollback and durable replay authority remain OPEN. NOT FROZEN.**

I36-GOV-01..10 remain GOVERNANCE-BLOCKED. No Multi-PolicyDomain, Global Forget, physical erasure or production activation is authorized.

**角色模拟 I 侧决议：仅接受 H 三态 Outer Envelope Authentication/Replay Callback 分离作为候选接口与本地 L1/L2 测试证据。Production Trust Root、Signer Role Policy、Profile Registration、Key Lifecycle、Historical Verification、Anti-Rollback 与 Durable Replay Authority 仍 OPEN，不冻结。**

I36-GOV-01..10 继续 GOVERNANCE-BLOCKED。不授权 Multi-PolicyDomain、Global Forget、物理擦除或生产激活。
