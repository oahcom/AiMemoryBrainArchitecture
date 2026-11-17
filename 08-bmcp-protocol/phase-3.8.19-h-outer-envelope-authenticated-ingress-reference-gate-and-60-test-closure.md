# Phase 3.8.19 — H Outer-Envelope Authenticated Ingress Gate and Exact 60-Test CI
# Phase 3.8.19 — H 外层 Envelope 认证 Ingress Gate 与精确 60 项 CI

- Owner perspective: H — BMCP Protocol / Envelope / Adapter Authentication
- Status: **REFERENCE AUTHENTICATED-INGRESS GATE + 60/60 EXACT-HEAD TESTS PASS; CRYPTO PROFILE / SIGNER ROLE / PRODUCTION TRUST OPEN; NOT PRODUCTION / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- H Unified 1.2.14 schema Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H envelope auth validator Blob: `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- H Provider Outcome validator Blob: `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth test Blob: `ddf34e9c30edfc378a9482a30837ce04c4abcf97`
- H Provider Outcome test Blob: `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H full positive fixture Blob: `f911027c848d21dd36fb87ba64a201a1455787a7`
- C crypto interop test Blobs: `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` and `a49d588ea6f840927fe21ad8c41cd8089dceac29`
- H workflow Blob: `4459d19f5b4eea058377d9819e48e81eed5c8c4b`
- Exact H Provider Outcome CI run: `44073888935`
- Exact tested commit: `0e212731073b36e4fa9ffda8467e60806da1b380`
- Exact job: `134006790527` (`provider-outcome`) — **completed / success**
- Test result: **60 tests, 0 failures** (36 H/C Provider Outcome tests + 18 outer-envelope-auth tests + 6 Python/Node crypto interop tests)
- Predecessor gap contract: H Phase 3.8.18, Blob `fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1`
- H identity-binding baseline: Phase 3.6, Blob `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- I envelope-auth boundary review: Phase 3.8.15, Blob `df869ef90e6279602b4d46128a81b2dc6ba01d71`
- Provenance: delegated H-role reference implementation and exact CI readback; **not an independent human H Owner decision**.
- English and Chinese are normative peers.

## 1. Scope and exact result / 范围与精确结果

H Phase 3.8.18 identified that the Provider Outcome validator could return local VALID without authenticating the outer BMCP envelope. This phase adds a separate reference ingress gate and an authenticated wrapper. The exact H Provider Outcome workflow ran 60 tests on commit `0e212731...`; raw job output records `Ran 60 tests in 12.250s` and `OK`.

H Phase 3.8.18 指出 Provider Outcome Validator 可能在未认证外层 BMCP Envelope 的情况下返回本地 VALID。本阶段新增独立 Reference Ingress Gate 与 Authenticated Wrapper。H Provider Outcome Workflow 在 Commit `0e212731...` 上执行 60 项测试；Raw Job Output 记录 `Ran 60 tests in 12.250s` 与 `OK`。

The exact source set contains:
- 36 H/C Provider Outcome validator unit/full-path methods;
- 18 outer-envelope authentication/transport/replay methods;
- six Python/Node candidate C crypto interoperability methods.

精确源集合包括：36 个 H/C Provider Outcome Validator Unit/Full-Path 方法、18 个 Outer Envelope Authentication/Transport/Replay 方法，以及 6 个 Python/Node 候选 C Crypto Interop 方法。

## 2. Authenticated ingress entrypoint / 认证 Ingress 入口

New source:
- `validators/envelope_auth_validator.py`
- `tests/conformance/provider_outcome/test_envelope_auth_validator.py`

The production-intended entrypoint is `validate_authenticated_provider_outcome(raw_envelope, raw_c_object, protected_context, envelope_auth_checks, envelope_schema, c_object_schema, owner_checks)`.

The legacy `validate_provider_outcome()` and `validate_raw_provider_outcome()` functions are explicitly documented as local H/C schema/semantic test interfaces, **not authenticated ingress acceptance APIs**. They do not verify outer envelope signature, protected transport principal, channel binding or replay.

新增源码为 `envelope_auth_validator.py` 及其 18 项测试。生产预期入口是 `validate_authenticated_provider_outcome(...)`。原有 `validate_provider_outcome()` 与 `validate_raw_provider_outcome()` 已明确标记为本地 H/C Schema/Semantic 测试接口，**不是认证 Ingress Acceptance API**；它们不验证外层 Envelope Signature、Protected Transport Principal、Channel Binding 或 Replay。

## 3. Reference authentication sequence / Reference Authentication 顺序

The reference gate implements the following fail-closed order:

1. Strictly parse exact raw UTF-8 bytes; reject duplicate JSON members, invalid UTF-8, non-finite numbers and non-object roots.
2. Require the minimum security envelope fields and a verifier-produced protected transport/session context. Missing protected context is UNKNOWN; malformed/missing required security fields are INVALID.
3. Compare the claims that must directly match the protected context: `issuer_ref`, `sender_authority_ref`, `sender_subject_ref`, `audience` and `channel_binding_proof_ref`.
4. Invoke the envelope-integrity verifier for exact raw bytes, canonical digest, signature preimage and approved signature profile.
5. Invoke key-status/revocation/history/anti-rollback verification.
6. Verify channel binding against the protected session context.
7. Verify issuer/authority/principal/subject/owner-authority registry binding.
8. Only after steps 4–7 are all verified, atomically check/reserve message replay/idempotency state:
   - NEW → continue;
   - SAME_DIGEST_REPLAY with a prior durable result ref → return IDEMPOTENT_REPLAY and do not re-run the domain validator;
   - CONFLICT → INVALID;
   - unavailable replay state or missing prior result ref → UNKNOWN.
9. Only AUTHENTICATED_NEW continues to H/C schema validation, immutable C object dereference/equality, C semantic predicates, C-P0 digest recomputation and separate C/I/D/Storage authority joins.

Reference Gate 执行 fail-closed 顺序：严格解析原始 UTF-8；检查安全字段与受保护 Transport/Session Context；将 Issuer/Sender/Audience/Channel Claim 与保护性 Context 比较；验证外层 Digest/Signature/Profile；验证 Key Status/Revocation/History/Anti-Rollback；验证 Channel Binding；验证 Identity Registry；仅在前述认证成功后原子检查/预留 Replay/Idempotency；最后才进入 H/C Schema、C Object、C Semantic、C-P0 与独立 Owner Join。

The direct claim checks do not authenticate the claims by themselves. They only reject a payload/context mismatch. The verifier callbacks are the trust boundary and must use authenticated registries and protected context, never a payload-selected key or profile.

直接 Claim 比较本身不认证 Claim，只负责拒绝 Payload/Context 不一致。真正 Trust Boundary 是 Verifier Callback，必须使用认证 Registry 和 Protected Context，不能使用 Payload 自选 Key/Profile。

## 4. Explicit unresolved signer and owner-role separation / 未决 Signer 与 Owner 角色分离

This implementation deliberately does **not** equate `owner_authority` with the authenticated transport sender authority. A C-owned Provider Outcome record may be transported/signed by a C adapter, H gateway or separately authorized attestor only if the C/I-approved registry policy explicitly permits that relationship. Test 17 proves only that the reference callback can represent such a policy; it does not decide which signer is approved.

本实现刻意**不将 `owner_authority` 与认证 Transport Sender Authority 等同**。C-owned Provider Outcome 可以由 C Adapter、H Gateway 或独立 Attestor 传输/签名，但仅在 C/I 批准的 Registry Policy 明确允许该关系时成立。Test 17 只证明 Reference Callback 能表达这种策略，不决定哪种 Signer 已获批准。

`subject_ref` and `owner_authority` are resolved by the identity/authority registry callback; they are not forced to equal the sender subject string or sender authority kind. The sender's `issuer_ref`, `sender_authority_ref` and `sender_subject_ref` must still match the protected transport context.

`subject_ref` 与 `owner_authority` 由 Identity/Authority Registry Callback 解析，不强制等于 Sender Subject 字符串或 Sender Authority Kind。Sender 的 `issuer_ref`、`sender_authority_ref` 与 `sender_subject_ref` 仍必须匹配 Protected Transport Context。

The H schema exposes `signature_profile_id` as an optional property, while the envelope requires `canonicalization_profile_id`, `key_id_ref`, `key_version` and `signature`. The integrity callback MUST resolve the exact approved signature profile from authenticated key/issuer configuration. It MUST NOT treat `canonicalization_profile_id` as a signature profile or select a trusted profile solely from payload fields. If `signature_profile_id` is present, it must match the authenticated registry result.

H Schema 将 `signature_profile_id` 定义为可选属性，同时 Envelope 要求 `canonicalization_profile_id`、`key_id_ref`、`key_version` 与 `signature`。Integrity Callback 必须从认证 Key/Issuer 配置解析精确批准的 Signature Profile；不得把 `canonicalization_profile_id` 当作 Signature Profile，也不得仅凭 Payload 字段选择可信 Profile。若存在 `signature_profile_id`，必须与认证 Registry 结果一致。

C's `AIMBA-C-CRYPTO-1.0` currently applies to the immutable CSubmitOutcome object P0/signature. It is not automatically the outer BMCP envelope profile. I's profile is I-owned and cannot be applied to C-originated envelope semantics without explicit authority. The exact outer-envelope P0 field allowlist, signing principal, profile, algorithm, key custody and revocation policy remain **OPEN pending C/I decisions**.

C 的 `AIMBA-C-CRYPTO-1.0` 当前适用于不可变 CSubmitOutcome Object P0/Signature，不自动成为外层 BMCP Envelope Profile。I Profile 属于 I，未经明确授权不得用于 C-originated Envelope 语义。外层 Envelope P0 字段 Allowlist、Signer Principal、Profile、算法、Key Custody 与 Revocation Policy 仍 **OPEN，等待 C/I 决策**。

## 5. Callback contract and tri-state / Callback 合同与三态

The reference callback set is:
- `verify_envelope_integrity(raw_bytes, envelope, protected_context)`;
- `verify_key_status(envelope, protected_context)`;
- `verify_channel_binding(envelope, protected_context)`;
- `verify_identity_binding(envelope, protected_context)`;
- `check_and_reserve_replay(envelope, protected_context)`.

For Boolean verifiers: True = verified; False = authenticated contradiction (INVALID); None, exception or missing callback = UNKNOWN. The replay callback returns NEW, SAME_DIGEST_REPLAY, CONFLICT or UNKNOWN. No missing verifier, unknown profile, key-status outage, channel-binding outage or replay-ledger outage can produce AUTHENTICATED_NEW.

Reference Callback 包括 Envelope Integrity、Key Status、Channel Binding、Identity Binding 与 Replay/Idempotency。Boolean Verifier 中 True=验证成功；False=已证明矛盾（INVALID）；None/异常/缺失 Callback=UNKNOWN。Replay Callback 返回 NEW、SAME_DIGEST_REPLAY、CONFLICT 或 UNKNOWN。Verifier 缺失、Profile 未知、Key Status/Channel Binding/Replay Ledger 不可用均不能产生 AUTHENTICATED_NEW。

## 6. Exact test coverage / 精确测试覆盖

The 18 outer-envelope tests establish only local reference behavior:
1. new envelope proceeds only with protected context and all callbacks;
2. duplicate JSON members are rejected before callbacks;
3. missing protected context returns UNKNOWN;
4. issuer/sender/audience/channel claim mismatch returns INVALID;
5. signature/digest contradiction returns INVALID;
6. unavailable key status returns UNKNOWN;
7. channel-binding contradiction returns INVALID;
8. identity registry contradiction returns INVALID;
9. missing required verifier returns UNKNOWN;
10. same-digest replay returns prior result without reprocessing;
11. changed-digest replay conflict returns INVALID;
12. unavailable replay ledger returns UNKNOWN;
13. authenticated entrypoint does not call domain validator before authentication;
14. authenticated entrypoint invokes domain validator only after auth;
15–16. replay reservation is not attempted if signature/authentication fails or key status is UNKNOWN;
17. gateway signer versus C-owned record remains registry-authorized, not hardcoded;
18. subject/owner-authority claim is rejected when registry binding contradicts.

18 项 Outer Envelope 测试只证明本地 Reference 行为：Protected Context 与全部 Callback 成功才继续；Duplicate Key 在 Callback 前拒绝；Context 缺失 UNKNOWN；Issuer/Sender/Audience/Channel Claim 不匹配 INVALID；Signature/Digest 矛盾 INVALID；Key Status 不可用 UNKNOWN；Channel/Identity 矛盾 INVALID；Callback 缺失 UNKNOWN；Same-Digest Replay 返回既有结果；Changed-Digest Conflict INVALID；Replay Ledger 不可用 UNKNOWN；Domain Validator 不得在 Auth 前调用；Replay Reservation 不得在认证失败/Key Status UNKNOWN 时执行；Gateway Signer 与 C Owner 关系由 Registry 决定；Subject/Owner Authority 由 Registry 验证。

## 7. Evidence ceiling / 证据上限

**PROVEN:** strict raw parser integration; protected-context claim comparison; tri-state callback orchestration; replay/idempotency result handling; replay reservation ordering; authenticated wrapper ordering; 60 exact-head tests passing.

**NOT PROVEN:** actual envelope P0 canonicalization/digest recomputation; production signature verification; approved signer/profile choice; production I trust/key registry; key lifecycle/rotation/revocation/history; real protected transport/channel binding; durable replay ledger; authenticated gateway deployment; provider truth; production owner-authority adapters; COC/Storage durability.

**已证明：** Raw Parser 集成、Protected Context Claim 比较、三态 Callback 编排、Replay/Idempotency 结果处理、Replay Reservation 顺序、Authenticated Wrapper 顺序、60 项精确 HEAD 测试通过。

**未证明：** 真实 Envelope P0 Canonicalization/Digest 重算、生产 Signature Verification、批准的 Signer/Profile 选择、生产 I Trust/Key Registry、Key Lifecycle/Rotation/Revocation/History、真实 Protected Transport/Channel Binding、持久 Replay Ledger、认证 Gateway 部署、Provider Truth、生产 Owner Authority Adapter、COC/Storage Durability。

All 18 outer-envelope callbacks in CI are deterministic test doubles. The 60-test PASS is **reference-interface conformance only**, not authenticated production envelope acceptance. No production profile is registered and no signer role is approved by this H artifact.

CI 中所有 Outer Envelope Callback 均为确定性 Test Double。60 项 PASS **仅代表 Reference Interface 符合性**，不是生产环境已认证 Envelope Acceptance。本 H 工件没有注册生产 Profile，也没有批准 Signer Role。

## 8. Required C/I decisions and next steps / 必需 C/I 决策与下一步

1. C decides whether the C Provider Outcome origin signature is sufficient for the outer envelope or whether a separate H gateway/attestor signature is required; distinguish origin signature from gateway receipt/attestation.
2. I approves the trust binding, exact signer-to-authority registry policy, signature profile/key lifecycle, historical key-status verification and anti-rollback policy.
3. H publishes the exact outer-envelope P0 field allowlist and signature preimage only after C/I decisions; include every field and explicit null/absent treatment.
4. Add real cryptographic vectors and independent Python/Node verification for the outer envelope profile; retain separate C object P0 and outer-envelope P0 digest domains.
5. Integrate the production protected transport verifier and durable replay ledger; fault-test crash between authentication, replay reservation and durable ingress.
6. Re-review with C/I/A and update Storage exact-version manifest. Until then, durable acceptance and production activation remain blocked.

1. C 决定 C Provider Outcome Origin Signature 是否足以覆盖外层 Envelope，还是需要独立 H Gateway/Attestor Signature；区分 Origin Signature 与 Gateway Receipt/Attestation。
2. I 批准 Trust Binding、Signer-to-Authority Registry Policy、Signature Profile/Key Lifecycle、Historical Key Status Verification 与 Anti-Rollback Policy。
3. H 仅在 C/I 决策后发布精确 Outer Envelope P0 Field Allowlist 与 Signature Preimage，逐字段定义并明确 Null/Absent 处理。
4. 为外层 Envelope Profile 增加真实 Crypto Vector 与独立 Python/Node 验证；C Object P0 与 Outer Envelope P0 Digest 域必须保持分离。
5. 集成生产 Protected Transport Verifier 与 Durable Replay Ledger；对 Authentication、Replay Reservation、Durable Ingress 之间的崩溃窗口进行 Fault Test。
6. 由 C/I/A 重新审查并更新 Storage 精确版本清单。在此之前，Durable Acceptance 与 Production Activation 仍阻断。

## 9. H disposition / H 侧结论

**Delegated H-role decision: ACCEPT the reference authenticated-ingress gate and 60-test local interface evidence as an architecture candidate. Do not claim authenticated production envelopes. Outer P0, signer role/profile, production trust, replay durability and gateway deployment remain OPEN. NOT FROZEN.**

**角色模拟 H 侧决议：接受 Reference Authenticated-Ingress Gate 与 60 项本地接口证据作为架构候选。不得声称生产 Envelope 已认证。Outer P0、Signer Role/Profile、Production Trust、Replay Durability 与 Gateway Deployment 仍 OPEN，不冻结。**

---
**Provenance:** delegated H-role source implementation and CI review in the coordinating session; not an independent human H Owner signature or C/I security approval.
