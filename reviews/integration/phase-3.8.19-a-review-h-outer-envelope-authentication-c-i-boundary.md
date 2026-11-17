# Phase 3.8.19 — A Review: H Outer Envelope Authentication / C-I Authority Boundary
# Phase 3.8.19 — A 复审：H Outer Envelope Authentication / C-I Authority Boundary

- Reviewer perspective: A — Principal Integration Architect
- H gap/decision contract Blob: fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1
- C exact boundary review Blob: d9da97c25cab7d22041dd6e25acab164cde1f9c4
- I exact trust-boundary review Blob: a50fa73aa9cb5949a29e2ca39b0f4284c4a5a31b
- H Unified 1.2.14 schema Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- H current validator Blob: eab961a08d41e871f38543b18ee60cf024977414
- Decision: **ACCEPT AS A BLOCKING ARCHITECTURE GAP WITH OWNER-DEFINED FOLLOW-UP; DO NOT FREEZE**
- Provenance: delegated A-role integration assessment; not an independent human A Owner acceptance.

## 1. A finding / A 发现

The 42-test H/C local validator pass does not authenticate the outer BMCP envelope. The H commonEnvelope requires cryptographic and transport-binding fields structurally, but the current Provider Outcome validator does not recompute/verify the envelope payload_digest/signature, verify channel binding or bind payload sender/issuer/subject/key claims to protected transport verifier context. It can return VALID while the outer signature is only signature-shaped fixture bytes.

This is a distinct gap from CSubmitOutcome object signature validation and must be recorded as such. The 42-test result remains valid for its stated local H/C schema/semantic/C-P0 scope; it must not be relabelled as authenticated envelope conformance.

42 项 H/C 本地 Validator 测试没有认证外层 BMCP Envelope。H commonEnvelope 结构上要求密码学与 Transport Binding 字段，但当前 Provider Outcome Validator 不重算/验证 Envelope payload_digest/signature、不验证 Channel Binding，也不将 Payload Sender/Issuer/Subject/Key Claim 与受保护 Transport Verifier Context 绑定。即使外层 Signature 只是形态化 Fixture Bytes，它仍可能返回 VALID。

这与 CSubmitOutcome Object Signature 校验是不同缺口，必须单独登记。42 项测试在其声明的本地 H/C Schema/Semantic/C-P0 范围内仍有效，但不得改称为已认证 Envelope Conformance。

## 2. Authority composition / 权威组合

A accepts the proposed separation:
- H owns exact envelope wire representation, canonicalization mapping, transport/session integration and gateway enforcement;
- C owns CSubmitOutcome semantics and must explicitly decide whether/how a C-originated envelope is signed as a separate object;
- I owns trust roots, issuer/principal binding, key lifecycle/status/history, revocation, anti-rollback and authorization;
- Storage accepts durable messages only after the agreed authenticated-ingress predicate, and owns durable replay/acceptance persistence semantics.

A rejects implicit profile reuse:
- C's AIMBA-C-CRYPTO-1.0 signs the C immutable object and is not automatically the envelope profile;
- I's AIMBA-I-CRYPTO-1.0 is for I-signed records and cannot be applied to C-originated envelopes without explicit authority;
- H cannot choose a profile or signer on behalf of C or I.

A 接受以下权威分离：
- H 拥有 Envelope Wire Representation、Canonicalization Mapping、Transport/Session Integration 与 Gateway Enforcement；
- C 拥有 CSubmitOutcome 语义，并必须明确 C-originated Envelope 是否/如何作为独立对象签名；
- I 拥有 Trust Root、Issuer/Principal Binding、Key Lifecycle/Status/History、Revocation、Anti-Rollback 与 Authorization；
- Storage 仅在约定的 Authenticated-Ingress Predicate 满足后持久接受消息，并拥有 Durable Replay/Acceptance Persistence 语义。

A 拒绝隐式 Profile 复用：
- C AIMBA-C-CRYPTO-1.0 签署 C 不可变 Object，不自动成为 Envelope Profile；
- I AIMBA-I-CRYPTO-1.0 用于 I-signed Record，未经明确授权不得应用到 C-originated Envelope；
- H 不得代表 C 或 I 选择 Profile/Signer。

## 3. Required completion evidence / 必需完成证据

1. C exact decision: outer-envelope signer identity, C-owned envelope P0 allowlist, domain separation, signature preimage and cross-language vectors, or an explicit alternative attestation model.
2. H exact contract: strict raw parse, schema pin, envelope P0 extraction, digest/signature verification integration, channel-binding validation, authenticated transport principal mapping, audience/nonce/replay and fail-closed tri-state.
3. I exact contract: approved profile registry, issuer/key status/history, revocation/compromise ordering, principal/subject/audience validation, anti-rollback and UNKNOWN/INVALID semantics.
4. Storage exact contract: durable acceptance only after authenticated ingress, authoritative replay/idempotency ledger and crash/retry behavior.
5. H executable tests: positive valid envelope, per-field P0 mutation, digest/signature mutation, wrong key/profile, revoked key, sender/principal mismatch, wrong audience, nonce replay, channel-binding mismatch, unavailable trust/replay sources and C-object/envelope cross-independent failure cases.
6. A exact-version integration review after C/H/I/Storage decisions and tests.

## 4. Gate and authorization statement / Gate 与授权状态

- H outer-envelope authentication: **OPEN / NOT IMPLEMENTED IN THE CURRENT PROVIDER OUTCOME VALIDATOR**.
- C envelope signer/P0 decision: **OPEN**.
- I trust/principal/key/revocation policy binding: **OPEN**.
- Storage authenticated durable-ingress binding: **OPEN**.
- Gate A: PARTIAL PASS / OPEN.
- Gate B: BLOCKED.
- Gate C: DEFERRED TO ENGINEERING / NOT RUN.
- JF-10 P0, R1, R2: OPEN.
- Production activation/provider egress: NOT AUTHORIZED.

## 5. A disposition / A 结论

**ACCEPT AS A BLOCKING ARCHITECTURE GAP WITH OWNER-DEFINED FOLLOW-UP; DO NOT FREEZE.**

The H/C 42-test local validation result remains valid within its exact evidence ceiling. Authenticated outer-envelope acceptance is not proven. No C/I profile is implicitly selected, no production trust adapter is authorized and no Gate status changes.

**接受为必须由 Owner 明确后续处理的阻塞性架构缺口；不得冻结。**

H/C 42 项本地验证结果在其精确证据边界内仍有效，但外层 Envelope Authentication 未证明。不隐式选择 C/I Profile，不授权生产 Trust Adapter，不改变任何 Gate 状态。

---
**Provenance:** delegated A-role integration assessment; not an independent human A Owner acceptance.
