# Phase 3.8.18 — I Exact Review: H Authenticated Ingress Gate and Envelope Trust Boundary
# Phase 3.8.18 — I 精确复审：H Authenticated Ingress Gate 与 Envelope Trust 边界

- Owner perspective: I — Security, Identity, Trust and Governance
- H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H envelope-auth validator: Blob `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- H C Provider Outcome validator: Blob `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth test source: Blob `ddf34e9c30edfc378a9482a30837ce04c4abcf97`
- H Provider Outcome test source: Blob `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H Phase 3.8.19 exact closure: Blob `860c896a388597a4378eda5aa323f276390acf34`
- H exact CI Run `44073888935`, tested commit `0e212731073b36e4fa9ffda8467e60806da1b380`, Job `134006790527`, SUCCESS, 60 tests / 0 failures
- C exact review of H gate: Blob `2e8414f361b0b5d7de959be8a971aadc9e62d6a9`
- Status: **ACCEPT REFERENCE TRUST-BOUNDARY INTERFACE; PRODUCTION TRUST / PROFILE / SIGNER AUTHORIZATION NOT APPROVED**
- Provenance: delegated I-role review; not an independent human I Owner signature or governance registration.
- English and Chinese are normative peers.

## 1. Exact review scope / 精确复审范围

I reviewed the exact H outer-envelope reference gate, its 18 tests, the H/C domain validator and the 60-test CI record. The gate's separation between payload claims and verifier-produced `ProtectedTransportContext`, fail-closed tri-state callbacks, and replay-after-authentication ordering are accepted as an appropriate interface candidate.

The implementation deliberately leaves signature-profile resolution, key status, identity registry, channel binding and durable replay to injected callbacks. That is correct as an architecture seam, but it is not evidence that I's production trust services exist or are connected.

I 已复审精确 H Outer Envelope Reference Gate、18 项测试、H/C Domain Validator 与 60 项 CI 记录。将 Payload Claim 与 Verifier 生成的 `ProtectedTransportContext` 分离、Fail-Closed 三态 Callback、以及 Authentication 之后才执行 Replay 的顺序，可作为适当的接口候选接受。

实现将 Signature Profile Resolution、Key Status、Identity Registry、Channel Binding 与 Durable Replay 留给注入 Callback。这是合理的架构 Seam，但不证明 I 生产 Trust 服务已存在或接通。

## 2. I-owned trust decisions / I 自有 Trust 决策

I retains exclusive authority for:
- registration/approval of the envelope signature profile and algorithm suite;
- trust-root selection, issuer-to-authority registry policy and signer delegation;
- key identity, key status/history, revocation/compromise ordering and historical verification policy;
- key custody/KMS/HSM requirements and rotation/retirement/destruction controls;
- anti-rollback checkpoint authority and currentness policy;
- authorization/PermissionEpoch binding where the message operation requires it.

H may consume authenticated I verifier results and map them into BMCP status. H cannot register a profile, mint trust, infer key ACTIVE, approve a gateway signer, or treat an unknown issuer as trusted.

I 对以下事项保留独占权威：
- Envelope Signature Profile 与算法套件的注册/批准；
- Trust Root、Issuer-to-Authority Registry Policy 与 Signer Delegation；
- Key Identity、Key Status/History、Revocation/Compromise Ordering 与历史验证策略；
- KMS/HSM Custody、Rotation/Retirement/Destruction；
- Anti-Rollback Checkpoint Authority 与 Currentness Policy；
- 消息操作需要时的 Authorization/PermissionEpoch Binding。

H 可消费经认证的 I Verifier Result 并映射 BMCP 状态，但不能注册 Profile、签发 Trust、推断 Key 为 ACTIVE、批准 Gateway Signer，或将未知 Issuer 视为可信。

## 3. Exact interface conditions / 精确接口条件

1. `verify_envelope_integrity` MUST resolve an exact registered profile using protected issuer/key configuration. Payload-supplied `canonicalization_profile_id`, optional `signature_profile_id`, `key_id_ref` or `key_version` are selectors/claims, not trust anchors.
2. The verifier MUST recompute the envelope-specific canonical digest and verify the signature over the exact versioned P0. It must bind every signed field, including message ID/nonce, audience, issuer/sender/subject, owner authority/record, message-specific fields, integrity proof and channel-binding reference, with explicit null/absent rules.
3. `verify_key_status` MUST verify status at signing sequence/time and current status, including revocation/compromise precedence, historical verification policy, sequence namespace and external anti-rollback checkpoint. Missing status/checkpoint is UNKNOWN.
4. `verify_identity_binding` MUST independently authorize the relation among authenticated sender, issuer, sender subject, target `subject_ref`, `owner_authority`, message type and operation. It must not assume sender authority equals owner authority; any gateway/attestor delegation must be explicit and revocable.
5. `ProtectedTransportContext` must be minted by a trusted transport verifier and carry authenticated provenance. Its public dataclass shape is not a security boundary; production API access must prevent caller-supplied or payload-derived construction.
6. `verify_channel_binding` must bind the exact live session/channel and proof to the protected runtime/authentication context, with expiry and session lifecycle checks.
7. `check_and_reserve_replay` must be backed by an authoritative durable ledger. Reservation, durable ingress acceptance, crash recovery and prior-result publication need an atomic/recoverable state machine; replay state outage returns UNKNOWN. Same-digest replay must recheck current authorization/key/fence policy before returning a prior result if policy requires it.
8. A profile/key/registry mismatch proven by authenticated registry data is INVALID; unavailable registry/trust/checkpoint state is UNKNOWN. No permissive fallback or profile downgrade.

1. `verify_envelope_integrity` 必须通过 Protected Issuer/Key 配置解析精确注册 Profile。Payload 的 `canonicalization_profile_id`、可选 `signature_profile_id`、`key_id_ref`、`key_version` 只是 Selector/Claim，不是 Trust Anchor。
2. Verifier 必须对版本化 P0 重算 Envelope 专属 Canonical Digest，并验证精确签名；绑定 Message ID/Nonce、Audience、Issuer/Sender/Subject、Owner Authority/Record、消息专属字段、Integrity Proof、Channel-Binding Ref，明确 Null/Absent。
3. `verify_key_status` 必须验证签名时与当前 Key Status、Revocation/Compromise 优先级、历史验证策略、Sequence Namespace 与外部 Anti-Rollback Checkpoint。状态/Checkpoint 缺失为 UNKNOWN。
4. `verify_identity_binding` 必须独立授权 Authenticated Sender、Issuer、Sender Subject、目标 `subject_ref`、`owner_authority`、Message Type 与 Operation 的关系。不得假设 Sender Authority 等于 Owner Authority；Gateway/Attestor Delegation 必须明确且可撤销。
5. `ProtectedTransportContext` 必须由可信 Transport Verifier 生成并携带认证来源。公开 Dataclass 形态不是安全边界；生产 API 必须防止调用者自行构造或从 Payload 派生。
6. `verify_channel_binding` 必须绑定精确 Live Session/Channel 与 Protected Runtime/Auth Context，并验证过期和 Session Lifecycle。
7. `check_and_reserve_replay` 必须由权威 Durable Ledger 支持。Reservation、Durable Ingress Acceptance、Crash Recovery、Prior Result Publication 必须具备原子/可恢复状态机；Replay 状态不可用为 UNKNOWN。若策略要求，同 Digest Replay 返回旧结果前仍须重验当前 Authorization/Key/Fence。
8. 经认证 Registry 证明的 Profile/Key/Registry 矛盾为 INVALID；Registry/Trust/Checkpoint 不可用为 UNKNOWN。禁止宽松回退或 Profile Downgrade。

## 4. Evidence assessment / 证据评估

The 60-test CI is accepted as bounded local reference-interface evidence. The test callbacks are deterministic test doubles. The tests do not prove:
- I-approved production trust root or envelope profile registration;
- production issuer/key registry, key custody or historical revocation service;
- actual cryptographic P0/digest/signature verification;
- production transport identity or channel-binding verifier;
- durable replay/idempotency store or crash-consistent ingress acceptance;
- C origin signer or H gateway/attestor signer authorization.

60 项 CI 仅作为有限本地 Reference Interface 证据接受。测试 Callback 均为确定性 Test Double。测试不证明生产 I Trust Root/Envelope Profile 注册、生产 Issuer/Key Registry、Key Custody/历史 Revocation Service、真实密码学 P0/Digest/Signature 验证、生产 Transport Identity/Channel Binding、Durable Replay Store/Crash-Consistent Ingress Acceptance，或 C Origin Signer/H Gateway/Attestor Signer 授权。

## 5. I disposition / I 侧结论

**Delegated I-role disposition: ACCEPT H Phase 3.8.19 as a fail-closed reference trust-boundary interface and accept the exact 60-test result for local orchestration only. DO NOT REGISTER OR APPROVE any envelope profile, trust root, signer delegation or production key lifecycle. Production trust integration remains OPEN; NOT FROZEN.**

**角色模拟 I 侧结论：接受 H Phase 3.8.19 作为 Fail-Closed Reference Trust-Boundary Interface，60 项测试仅认可为本地编排证据。不得据此注册或批准任何 Envelope Profile、Trust Root、Signer Delegation 或生产 Key Lifecycle。生产 Trust 集成仍 OPEN，不冻结。**

---
**Provenance:** delegated I-role technical review authored in the coordinating session; not an independent human I Owner signature or formal governance registration.
