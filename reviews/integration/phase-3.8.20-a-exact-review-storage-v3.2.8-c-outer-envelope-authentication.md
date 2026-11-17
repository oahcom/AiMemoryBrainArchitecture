# Phase 3.8.20 — A Exact Integration Review: Storage v3.2.8 / C Outer BMCP Envelope Authentication
# Phase 3.8.20 — A 精确集成复审：Storage v3.2.8 / C 外层 BMCP Envelope Authentication

- Reviewer perspective: A — Principal Integration Architect
- Exact Storage v3.2.8 manifest Blob: 3c9d84e54c745c77d9e3895b631d4e164828ea9b
- C corrected outer-signer/P0 candidate Blob: 310e7e0073d3c32f594bc151f10c249c828ce30f
- H exact JSON-Pointer mapping Blob: 4ba7e1699215d02224f805a15484b1da2e40c03f
- I exact corrected P0 review Blob: 63d7bfc4ad08bd75e8c0a16c34b3c4ca95e76d00
- H schema 1.2.14 Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- H current validator Blob: eab961a08d41e871f38543b18ee60cf024977414
- H local CI: run 44072037563, commit c6faee294e503f32a802ba51f3f3b3eb4bee2cd7, 42 tests
- Decision: **ACCEPT AS A COHERENT ARCHITECTURE CANDIDATE WITH BLOCKING IMPLEMENTATION AND GOVERNANCE CONDITIONS — DO NOT FREEZE**
- Provenance: delegated A-role exact integration review; not an independent human A Owner acceptance.

## 1. Exact integration finding / 精确集成发现

The C/H/I candidate now has a coherent two-signed-object model for `C_PROVIDER_OUTCOME_RECORDED`:
1. C immutable CSubmitOutcome object, signed under its own C object P0/profile.
2. C-originated outer BMCP envelope, signed by the C provider adapter under a distinct envelope P0/profile.

The H gateway cannot substitute for C origin signing. An H gateway receipt may be additive, with a distinct H issuer and semantics. I owns trust registration, key lifecycle/history, revocation, anti-rollback and protected principal policy. H owns exact wire mapping and verifier implementation. Storage owns durable acceptance only after authenticated ingress.

C/H/I candidate now explicitly includes `integrity_proof_ref` and `channel_binding_proof_ref` in outer P0. H mapping identifies exact JSON Pointers. This corrects the field omission discovered in H's first review.

当前 C/H/I 候选已为 `C_PROVIDER_OUTCOME_RECORDED` 建立连贯的双 Signed-Object 模型：
1. C 不可变 CSubmitOutcome Object，使用独立 C Object P0/Profile 签名。
2. C-originated Outer BMCP Envelope，由 C Provider Adapter 使用独立 Envelope P0/Profile 签名。

H Gateway 不得替代 C Origin Signing。H Gateway Receipt 可以附加，但必须具有不同 H Issuer 与语义。I 拥有 Trust Registration、Key Lifecycle/History、Revocation、Anti-rollback 与 Protected Principal Policy。H 拥有精确 Wire Mapping 与 Verifier Implementation。Storage 拥有仅在 Authenticated Ingress 后持久接受的职责。

C/H/I Candidate 现在明确将 `integrity_proof_ref` 与 `channel_binding_proof_ref` 纳入 Outer P0。H Mapping 标识精确 JSON Pointer。这修正了 H 首次审查发现的字段遗漏。

## 2. Integration strengths / 集成优点

- Signed objects and P0 projections are explicitly distinct; no silent C-object P0 reuse for the envelope.
- C signer role is explicit for the C-originated message family.
- H's JSON-Pointer mapping is pinned to exact H 1.2.14 schema and C 1.0.1 schema.
- Proof locators are signed while the referenced proof objects remain independently authenticated.
- I retains trust/key authority without taking over C message semantics.
- H gateway receipt is not conflated with C origin signature.
- Storage durable acceptance is ordered after all required authentication and evidence joins.
- Candidate preserves tri-state fail-closed semantics.

- Signed Object 与 P0 Projection 明确分离；不得将 C Object P0 静默复用到 Envelope。
- C-originated Message Family 的 C Signer Role 明确。
- H JSON-Pointer Mapping 精确绑定 H 1.2.14 与 C 1.0.1 Schema。
- Proof Locator 被签名，同时被引用 Proof Object 仍需独立认证。
- I 保留 Trust/Key 权威，不接管 C Message Semantics。
- H Gateway Receipt 不与 C Origin Signature 混淆。
- Storage Durable Acceptance 排在全部必需 Authentication/Evidence Join 之后。
- 候选保留 Tri-state Fail-closed 语义。

## 3. Blocking conditions / 阻断条件

### A1 — C Owner acceptance and cryptographic profile

The C Phase 3.8.22 artifact is a delegated role decision candidate, not independent C Owner approval. The profile ID, JCS/SHA-256/Ed25519 suite, exact P0 and signer key usage remain unregistered/unfrozen. C must formally accept the exact corrected Blob and clarify whether envelope and object keys are distinct or the same key under separately authorized profile usages.

### A2 — I formal security governance

I's review accepts the separation but expressly does not approve algorithm suitability, trust roots, key custody, profile registration, revocation/history, anti-rollback or production signer authorization. Formal I approval and executable trust adapter are missing.

### A3 — H executable outer-envelope verifier

H Phase 3.8.20 is an architecture mapping, not implementation. The current H Provider Outcome validator does not recompute/verify outer envelope payload_digest/signature, verify integrity/channel-binding proof, bind claims to protected transport principal or enforce authoritative nonce replay. Full raw parser and P0 extraction tests are not present.

### A4 — Storage durable authenticated ingress

Storage v3.2.8 states the correct ordering, but no deployed durable ingress/replay/idempotency boundary or crash/retry semantics are implemented or tested. COC quorum and same-GID persistence remain separate blockers.

### A5 — Independent conformance and fault injection

The H 42-test CI is still bounded to local H/C object validation and C crypto vectors. It does not test outer-envelope signature, protected transport, channel binding, replay authority or durable acceptance. Required positive/negative tests and crash/failover fault injection remain open.

## 4. Exact required acceptance tests / 精确必需验收测试

1. Valid C envelope + valid C object → VALID.
2. Mutate every common-envelope and C message-family P0 field independently → INVALID.
3. Mutate `integrity_proof_ref` or `channel_binding_proof_ref` → INVALID.
4. Valid envelope signature + invalid C object signature/digest → INVALID.
5. Valid C object signature + invalid envelope signature → INVALID.
6. Wrong issuer/principal/subject/audience/key/profile, revoked/compromised key → INVALID.
7. Missing/unavailable I trust registry, key history, protected transport context, channel binding or replay ledger → UNKNOWN.
8. Nonce replay, message identity collision or downgrade → INVALID.
9. H gateway receipt without C origin signature → INVALID as C-origin message.
10. COC append does not alter C origin P0/signature but invalid COC proof rejects overall acceptance.
11. Storage crash after verification but before durable acceptance; crash after durable write but before ACK; replay after restart; duplicate retry; key revocation during recovery.
12. No downstream dispatch before authenticated durable acceptance is committed.

## 5. Gate status / Gate 状态

- Storage Gate A: PARTIAL PASS / OPEN.
- Gate B COC persistence: BLOCKED.
- Gate C end-to-end fault injection: DEFERRED TO ENGINEERING / NOT RUN.
- JF-10 P0: OPEN.
- R1/R2: OPEN.
- Multi-PolicyDomain atomicity: BLOCKED.
- C outer-envelope authentication: ARCHITECTURE CANDIDATE / NOT IMPLEMENTED / NOT VERIFIED.
- I trust/profile registration: OPEN / NOT APPROVED.
- Storage durable authenticated ingress: OPEN / NOT IMPLEMENTED.
- Production activation/provider egress: NOT AUTHORIZED.

## 6. A disposition / A 结论

**ACCEPT AS A COHERENT ARCHITECTURE CANDIDATE WITH BLOCKING IMPLEMENTATION AND GOVERNANCE CONDITIONS — DO NOT FREEZE.**

The architecture authority boundaries are now coherent at design level. The evidence does not justify protocol freeze, production authentication, Gate promotion or release. C/H/I/Storage documents are delegated role artifacts in this coordinated workflow, not independent human Owner signatures.

**接受为具有阻断性实现与治理条件的连贯架构候选——不得冻结。**

架构层面的权威边界目前已连贯，但证据不足以支持协议冻结、生产认证、Gate 晋级或发布。C/H/I/Storage 文档均为本协调工作流中的角色委托工件，不是独立人类 Owner 签署。

---
**Provenance:** delegated A-role exact integration review; not an independent human A Owner acceptance.
