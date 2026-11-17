# Phase 3.12.1 — A Exact Integration Review: Storage v3.3.1 and H Authenticated Ingress
# Phase 3.12.1 — A 精确集成复审：Storage v3.3.1 与 H Authenticated Ingress

- Owner perspective: A — Principal System Architecture / Integration Authority
- Exact Storage manifest: Phase 3.6.21 Storage v3.3.1, Blob `f6e61691ecdcfcbf1fb423cc45242868676ca925`
- Predecessor Storage manifest: v3.3.0, Blob `c8407c9f10049d65426a3598ad20b6aa70f83c32`
- Storage/D Option A topology ADR: Phase 3.8.2, Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`
- H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- CSubmitOutcome 1.0.1: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H envelope-auth validator: Blob `5c5079765f468eaf40690c0c7cbd6b03275a1ff8`
- H Provider Outcome validator: Blob `b8cd692d261df7a31a0f65c3e003693e305f73a2`
- H envelope-auth tests: Blob `ddf34e9c30edfc378a9482a30837ce04c4abcf97`
- H Provider Outcome tests: Blob `da1454ed985c84160c4cb6a0462df9d1225fab7f`
- H closure: Phase 3.8.19, Blob `860c896a388597a4378eda5aa323f276390acf34`
- H exact CI: Run `44073888935`, tested commit `0e212731073b36e4fa9ffda8467e60806da1b380`, job `134006790527`, SUCCESS, 60 tests / 0 failures
- H current branch HEAD: `10434b4df4b7c999206cbc296ffdbca4755fe3d2` (documentation-only successor; tested source Blobs unchanged)
- C exact review: Phase 3.8.22, Blob `8fd6052cabf58a78962cc2e776398b2a40604bcd`
- I exact review: Phase 3.8.18, Blob `73145f83df234ebb9e55cc07f0a82b0db9416b68`
- Status: **CONDITIONAL ACCEPTANCE OF THE BOUNDED REFERENCE BUNDLE; STORAGE MANIFEST AMENDMENT REQUIRED; NO PROFILE REGISTRATION / NO FREEZE / NO PRODUCTION AUTHORIZATION**
- Provenance: delegated A-role integration review at the user's direction; not an independent human A Owner approval.
- English and Chinese are normative peers.

## 1. A disposition / A 侧裁决

**ACCEPT WITH ENUMERATED AMENDMENTS** the H 1.2.14 / CSubmitOutcome 1.0.1 reference-ingress candidate bundle and its bounded 60-test evidence. The C and I reviews correctly preserve their authority boundaries and do not approve an outer signer/profile or production trust.

**Do not freeze. Do not register any crypto profile. Do not authorize production envelope acceptance, provider egress, JF-10 completion, Global Forget, Full Applied or production activation.**

A 对 H 1.2.14 / CSubmitOutcome 1.0.1 Reference-Ingress 候选 Bundle 及有限 60 项测试证据作出 **ACCEPT WITH ENUMERATED AMENDMENTS**。C/I 复审正确保留权威边界，未批准外层 Signer/Profile 或生产 Trust。

**不冻结、不注册任何密码学 Profile、不授权生产 Envelope Acceptance、Provider Egress、JF-10 完成、Global Forget、Full Applied 或生产激活。**

## 2. Evidence reconciliation / 证据对账

The v3.3.1 manifest pins the exact H schema, H/C validators, envelope-auth wrapper, test sources, 60-test workflow result, and new C/I reviews. The tested commit is `0e212731...`; the current H branch HEAD is `10434b4...`. The intervening H commit adds the Phase 3.8.19 closure document only; the pinned validator and test Blobs are unchanged. This is a valid source-level CI binding, but the manifest must state this tested-commit/current-head distinction exactly.

v3.3.1 Manifest 已绑定精确 H Schema、H/C Validator、Envelope Auth Wrapper、测试源码、60 项 Workflow 结果及新增 C/I 复审。测试 Commit 为 `0e212731...`；当前 H Branch HEAD 为 `10434b4...`。两者之间的 H Commit 仅增加 Phase 3.8.19 闭环文档，绑定的 Validator/Test Blob 未变化。该 CI 源码绑定可接受，但 Manifest 必须准确表达 Tested Commit 与 Current HEAD 的区别。

The 60 tests establish:
- 36 local H/C schema, C-object mapping, semantic and candidate C-P0 checks;
- 18 outer-envelope reference-gate orchestration tests;
- six Python/Node candidate C crypto interoperability tests.

They do NOT establish real outer-envelope canonicalization/digest/signature verification, production I trust registry/key lifecycle, real transport/channel binding, durable replay storage, production owner verifiers, provider issuer truth, COC quorum durability or Storage physical recovery. The envelope and owner callbacks are deterministic test doubles. The evidence ceiling in H Phase 3.8.19 and Storage v3.3.1 is correctly bounded.

60 项测试证明：
- 36 项本地 H/C Schema、C Object Mapping、Semantic 与候选 C-P0 检查；
- 18 项 Outer Envelope Reference Gate 编排测试；
- 6 项 Python/Node 候选 C Crypto Interoperability 测试。

它们不证明真实 Outer Envelope Canonicalization/Digest/Signature、生产 I Trust Registry/Key Lifecycle、真实 Transport/Channel Binding、Durable Replay Storage、生产 Owner Verifier、Provider Issuer Truth、COC Quorum Durability 或 Storage 物理恢复。Envelope 与 Owner Callback 均为确定性 Test Double。H Phase 3.8.19 和 Storage v3.3.1 对证据上限的声明正确。

## 3. Blocking manifest inconsistency — Option A status / Manifest 阻塞性不一致：Option A 状态

The v3.3.1 manifest's §2/§6 describes Option A as a “conditional L1 candidate” and says “A-01–A-05 clarifications remain open”. However, the exact pinned ADR Blob `bb544ba2...` states:
- §8 selects **Option A as the normative v1 logical architecture profile**;
- §8.7 requires one durable `CanonicalAuthoritySerializationAnchor` per `BrainAuthorityRef`, with an append-only transition record and a specific SERIALIZABLE/CAS transaction protocol;
- physical engine/deployment remains **L4 OPEN**.

The pinned ADR contains no A-01–A-05 register. The manifest's A-01–A-05 statement is unsupported by the pinned artifact and contradicts its selected-Option-A disposition.

**Required Storage correction before final manifest acceptance:**
1. Change “conditional L1 candidate” to “Option A selected as normative v1 logical architecture; L4 physical engine/deployment OPEN”.
2. Remove “A-01–A-05 clarifications remain open” unless a separate exact-versioned register is identified and pinned.
3. Preserve the L4 gates: runtime identity, row ownership, serializable/CAS behavior, I proof consumption, atomic outcome, HA/restore, read-path and accountable operator.
4. Ensure the manifest does not imply a physical DB product or deployment has been selected.

v3.3.1 Manifest §2/§6 将 Option A 描述为“conditional L1 candidate”，并称“A-01–A-05 clarifications remain open”。但精确绑定 ADR Blob `bb544ba2...` 明确：
- §8 已选择 **Option A 作为 v1 规范逻辑架构**；
- §8.7 要求每个 `BrainAuthorityRef` 一个持久化 `CanonicalAuthoritySerializationAnchor`，包含 Append-Only Transition Record 与具体 SERIALIZABLE/CAS 事务协议；
- 物理引擎/部署仍为 **L4 OPEN**。

该 ADR 不包含 A-01–A-05 登记表。Manifest 的 A-01–A-05 声明没有精确绑定依据，并与 ADR 的 Option A 已选决议矛盾。

**Storage 最终接受 Manifest 前必须修正：**
1. 将“conditional L1 candidate”改为“Option A 已选为 v1 规范逻辑架构；L4 物理引擎/部署 OPEN”；
2. 删除“A-01–A-05 clarifications remain open”，除非另有独立精确版本登记表并绑定；
3. 保留 L4 Gate：Runtime Identity、Row Ownership、Serializable/CAS、I Proof Consumption、Atomic Outcome、HA/Restore、Read Path 与明确责任 Operator；
4. 不得暗示已选择物理 DB 产品或生产部署。

## 4. Outer-envelope gate — accepted interface, not authenticated acceptance / 外层 Envelope Gate：接受接口，不代表认证完成

A accepts the H reference design's main separation:
- outer envelope authentication is independent from C object P0;
- protected transport context is distinct from payload claims;
- I-controlled key/identity/channel verifiers remain callbacks;
- replay reservation is attempted only after preceding authentication callbacks pass;
- C object semantic validation follows outer authentication;
- same-digest replay does not rerun the domain validator.

The following remain release blockers:

1. **No exact outer-envelope P0/profile.** H's `verify_envelope_integrity` callback is an interface only. No approved canonical projection, domain separator, signature preimage, algorithm/profile registration or independent cryptographic vectors exist for the outer envelope.
2. **Signer role remains unresolved.** C's Phase 3.8.22 recommends (but does not approve) a separate H gateway attestation over the received envelope/receipt while retaining C's independent C-object signature. I has not approved signer delegation, trust root or profile. A accepts this as the preferred candidate separation, not a final owner decision.
3. **Protected context provenance.** A public `ProtectedTransportContext` dataclass is constructible by arbitrary Python callers. Production ingress must only accept a context minted by the trusted transport verifier; enforce this at the API/process boundary, not by convention or type annotation.
4. **Replay durability/atomicity.** The callback reserves replay state before C object/domain validation and before durable ingress acceptance. Specify reservation lifecycle, crash recovery, lease/expiry, abort/release, commit/acceptance, prior-result publication and atomicity. No replay reservation may become a permanent consumed nonce with no recoverable message, nor permit duplicate domain processing after crash.
5. **Authorization on replay.** Before returning a prior result for SAME_DIGEST_REPLAY, re-evaluate current I authorization/PermissionEpoch, issuer/key status, audience/scope and applicable D Forget fence. Authentication of a signer at replay time is not by itself authorization to disclose a prior result.
6. **Schema/profile binding order.** The authenticated wrapper invokes envelope auth before the downstream domain validator's full JSON Schema validation. The exact H schema artifact/revision/message type must be selected from trusted receiver configuration and bound into the envelope P0/profile verifier before the message is accepted; malformed or unsupported revisions must never reach a trusted acceptance state.
7. **No production callback implementation.** All trust, channel, registry, replay and owner authority callbacks remain unconnected test seams.

A 接受 H Reference Design 的主要分离：
- Outer Envelope Authentication 独立于 C Object P0；
- Protected Transport Context 与 Payload Claim 分离；
- I 控制的 Key/Identity/Channel Verifier 保持为 Callback；
- 仅在前序认证 Callback 成功后才尝试 Replay Reservation；
- 外层认证后才执行 C Object Semantic Validation；
- Same-Digest Replay 不重新执行 Domain Validator。

以下仍是 Release Blocker：

1. **无精确 Outer Envelope P0/Profile。** H 的 `verify_envelope_integrity` 目前只是接口，没有批准的 Canonical Projection、Domain Separator、Signature Preimage、算法/Profile 注册或独立密码学向量。
2. **Signer Role 未解决。** C Phase 3.8.22 建议（但未批准）由 H Gateway 对接收 Envelope/Receipt 做独立 Attestation，同时保留 C 独立 C Object Signature。I 尚未批准 Signer Delegation、Trust Root 或 Profile。A 将其视为优先候选分离，不是最终 Owner 决策。
3. **Protected Context 来源。** 公开 `ProtectedTransportContext` Dataclass 可由任意 Python 调用方构造。生产 Ingress 只能接受可信 Transport Verifier 生成的 Context；必须在 API/进程边界强制，不能依赖约定或类型注解。
4. **Replay Durability/Atomicity。** Callback 在 C Object/Domain Validation 与 Durable Ingress Acceptance 前预留 Replay State。必须定义 Reservation 生命周期、崩溃恢复、Lease/Expiry、Abort/Release、Commit/Acceptance、Prior-Result Publication 与原子性。不得让 Replay Reservation 成为永久消耗但没有可恢复消息的 Nonce，也不得在崩溃后重复 Domain Processing。
5. **Replay 时授权。** SAME_DIGEST_REPLAY 返回旧结果前，必须重新评估当前 I Authorization/PermissionEpoch、Issuer/Key Status、Audience/Scope 与适用 D Forget Fence。Signer 在重放时通过 Authentication，不等于有权披露旧结果。
6. **Schema/Profile Binding 顺序。** Authenticated Wrapper 在下游 Domain Validator 完整 JSON Schema 校验之前先执行 Envelope Auth。可信 Receiver Configuration 必须先选定精确 H Schema Artifact/Revision/Message Type，并将其绑定进 Envelope P0/Profile Verifier；格式错误或不支持的 Revision 不得进入可信 Acceptance。
7. **生产 Callback 未实现。** Trust、Channel、Registry、Replay 与 Owner Authority Callback 仍未接通，属于测试 Seam。

## 5. Cross-owner authority decision / 跨 Owner 权威决议

| Area | Authority | Current disposition |
|---|---|---|
| C Provider Outcome object P0 and provider truth | C | Separate and retained; C production trust/provider evidence OPEN |
| Outer envelope wire/P0 contract | H | Reference gate accepted; exact P0 OPEN |
| Envelope signer delegation / trust root / key lifecycle | I, with C approval for C-origin semantics | NOT REGISTERED / NOT APPROVED |
| Protected transport/channel binding | H transport adapter + I trust policy | Interface candidate only |
| Durable replay and ingress acceptance | H protocol + Storage persistence; message-owner idempotency | Reference callback only |
| D Forget fence/lineage | D | Independent D proof and final currentness remain OPEN |
| Storage recovery/visibility | Storage | Exact manifest binding only; live COC/Storage evidence OPEN |
| Global integration/release decision | A | Conditional design acceptance only; no freeze |

## 6. Required successor work / 后续必须工作

1. Storage publishes a v3.3.2 successor manifest correcting Option A status and removing unsupported A-01–A-05 references.
2. C and I publish exact signer/attestation and trust-registry decisions; no implicit C-P0 reuse.
3. H publishes outer-envelope P0 allowlist, domain separation, canonical bytes, null/absent rules, signature profile ID and Python/Node positive + per-field negative vectors.
4. H implements a non-forgeable protected-context factory/transport ingress boundary.
5. H/Storage specify and test crash-safe replay reservation + durable acceptance state machine, including same-digest replay authorization recheck.
6. H binds trusted schema selection/revision into the envelope authentication stage.
7. Re-run exact H CI after code changes; update the exact-version manifest; then A performs another review.

## 7. Final A decision / A 最终裁决

**ACCEPT WITH ENUMERATED AMENDMENTS** for the bounded H 1.2.14 / C 1.0.1 reference-ingress design and 60-test local evidence. **REJECT the v3.3.1 manifest as a final consistent bundle manifest until the Option A status inconsistency is corrected.** No crypto profile registration, envelope signer approval, production authentication, provider egress, Storage deployment, JF-10 completion or global release is authorized.

**对 H 1.2.14 / C 1.0.1 Reference-Ingress 设计与 60 项本地证据作出 ACCEPT WITH ENUMERATED AMENDMENTS。** 在 Option A 状态不一致修正前，**不接受 v3.3.1 作为最终一致的 Bundle Manifest**。不授权 Crypto Profile 注册、Envelope Signer 批准、生产认证、Provider Egress、Storage 部署、JF-10 完成或全局发布。

---
**Provenance:** delegated A-role integration review authored in the coordinating session at the user's direction. It is not an independent human A Owner approval, formal governance signature, production security certification or deployment authorization.
