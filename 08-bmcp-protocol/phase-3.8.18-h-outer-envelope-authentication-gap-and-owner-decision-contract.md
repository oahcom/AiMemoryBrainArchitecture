# Phase 3.8.18 — H Outer Envelope Authentication Gap and Owner Decision Contract
# Phase 3.8.18 — H 外层 Envelope Authentication 缺口与 Owner 决策合同

- Owner perspective: H — BMCP Protocol / Envelope / Adapter Authentication
- Status: **GAP CONFIRMED; CONTRACT CANDIDATE ONLY; P0 / SIGNER PROFILE NOT FROZEN; C/I OWNER DECISIONS REQUIRED**
- Baseline H Unified schema 1.2.14 Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- Baseline H validator Blob: eab961a08d41e871f38543b18ee60cf024977414
- Baseline H 42-test source Blob: da1454ed985c84160c4cb6a0462df9d1225fab7f
- Baseline H 42-test CI run: 44072037563, exact commit c6faee294e503f32a802ba51f3f3b3eb4bee2cd7
- Provenance: delegated H-role architecture analysis; not an independent human H Owner decision.
- English and Chinese are normative peers.

## 1. Confirmed gap / 已确认缺口

The H Unified 1.2.14 commonEnvelope structurally requires schema identity/revision, wire version, message identity/nonce, audience, sender/issuer/subject claims, owner authority/record, canonicalization profile, digest algorithm, payload_digest, integrity_proof_ref, channel_binding_proof_ref, key_id_ref, key_version, signature and created_at. Structural requiredness does not authenticate any of these values.

The current H provider_outcome_validator.py:
- validates the loaded H schema URI and schema artifact revision/wire version;
- validates the envelope JSON Schema;
- dereferences/compares the immutable CSubmitOutcome 1.0.1 object;
- validates C semantic predicates and recomputes C-P0 digest;
- calls injected I/D/Storage authority callbacks.

It does **not** recompute the outer H envelope payload_digest, reconstruct/verify the outer H envelope signature, verify integrity_proof_ref or channel_binding_proof_ref, receive an authenticated transport principal, bind sender/issuer/subject claims to protected verifier context, or enforce nonce replay state. AuthorityChecks has no outer-envelope signature, transport identity, channel binding or replay callbacks. validate_raw_provider_outcome performs strict JSON parsing only, then delegates to this same validator.

The full-path fixture uses signature-shaped synthetic bytes and test callbacks. It can return VALID without authenticating the outer H envelope. Therefore the 42-test pass proves the local H/C object path, **not authenticated H envelope acceptance**.

H Unified 1.2.14 CommonEnvelope 结构上要求 Schema Identity/Revision、Wire Version、Message Identity/Nonce、Audience、Sender/Issuer/Subject Claim、Owner Authority/Record、Canonicalization Profile、Digest Algorithm、Payload Digest、Integrity Proof Ref、Channel Binding Proof Ref、Key ID/Version、Signature 与 Created At。但结构必填不等于这些值已被认证。

当前 H provider_outcome_validator.py 会校验 H Schema URI 与 Revision/Wire Version、JSON Schema、CSubmitOutcome 1.0.1 对象引用/一致性、C Semantic Predicate、C-P0 Digest，并调用注入的 I/D/Storage Callback。

它**不会**重算外层 H Envelope payload_digest、重建/验证外层 Envelope Signature、验证 integrity_proof_ref 或 channel_binding_proof_ref、接收受保护 Transport Principal、将 Sender/Issuer/Subject Claim 与保护性 Verifier Context 绑定，也不执行 Nonce Replay 状态检查。AuthorityChecks 没有 Outer Envelope Signature、Transport Identity、Channel Binding 或 Replay Callback。validate_raw_provider_outcome 仅执行严格 JSON 解析，再委托同一 Validator。

Full-Path Fixture 使用合成 Signature 形态字节与 Test Callback。因此它可以在未认证外层 H Envelope 的情况下返回 VALID。42 项测试证明的是本地 H/C Object 路径，**不是经过认证的 H Envelope Acceptance**。

## 2. Non-substitution rule / 不可替代规则

The following are separate cryptographic/authority objects and must not be conflated:

1. Outer BMCP envelope integrity/signature and protected transport/session principal binding.
2. CSubmitOutcome 1.0.1 immutable C object P0 digest/signature and C key-status/sequence namespace.
3. I terminal proof / authorization receipt.
4. D Forget clearance / Fence / lineage proof.
5. Storage same-GID resolution proof.
6. COC quorum/committed-prefix proof.

A valid C object signature does not authenticate the outer envelope. An outer envelope signature does not prove C provider outcome truth. TLS/channel binding does not replace durable message-level signature for queued/replayed/cross-boundary messages. H schema references do not prove the referenced Owner evidence.

以下是彼此独立的密码学/权威对象，不得混为一谈：

1. 外层 BMCP Envelope 完整性/签名与受保护 Transport/Session Principal Binding。
2. CSubmitOutcome 1.0.1 不可变 C Object P0 Digest/Signature 与 C Key Status/Sequence Namespace。
3. I Terminal Proof / Authorization Receipt。
4. D Forget Clearance / Fence / Lineage Proof。
5. Storage Same-GID Resolution Proof。
6. COC Quorum / Committed-Prefix Proof。

C Object Signature 有效不等于外层 Envelope 已认证；外层 Envelope Signature 有效不等于 C Provider Outcome 事实真实；TLS/Channel Binding 不替代跨队列/重放/跨边界消息的持久消息级签名；H Schema 中存在 Proof Ref 不等于已证明其引用的 Owner 证据。

## 3. Proposed validation stages — candidate only / 候选验证阶段

The following ordering is proposed for Owner review; no P0 projection, signer profile or algorithm is frozen here.

1. Strict parse raw bytes: UTF-8, duplicate-key rejection, non-finite-number rejection and top-level object shape.
2. Load the exact H schema artifact selected by trusted receiver configuration; validate schema ID, artifact revision, wire version, message type and structural schema.
3. Obtain protected transport/session/workload verifier context **outside the payload**. Payload-supplied sender/issuer/subject/key/audience values are untrusted claims.
4. Resolve the sender authority and exact envelope signature profile through authenticated configuration and the relevant Owner's approved profile registry. Never select a trusted key/profile solely from payload fields.
5. Reconstruct the exact envelope-specific P0 projection and signed preimage under an Owner-approved versioned profile; recompute payload_digest; verify signature and key status/history. The envelope P0 must explicitly define treatment of schema_artifact_revision, schema_version, message_nonce, audience, sender/issuer/subject, owner_authority, owner_record_ref, message-specific fields, integrity_proof_ref and channel_binding_proof_ref.
6. Verify channel-binding proof against the protected session; bind issuer/principal/subject/audience to the authenticated verifier result; reject claim mismatch.
7. Enforce nonce uniqueness/replay window and exact message identity/idempotency rules using an authoritative replay ledger. Unavailable replay authority is UNKNOWN, not success.
8. Only after envelope authentication, perform C object dereference/equality/C-P0 validation, then independent I/D/Storage/COC joins and currentness checks.
9. Return tri-state: INVALID for proven contradiction; UNKNOWN for missing/unavailable profile, trust, key status, transport context, channel binding, replay ledger or authority evidence; VALID only when every required check is verified.

上述顺序仅作为 Owner 审查候选；本文件不冻结 P0 Projection、Signer Profile 或算法。

1. 对 Raw Bytes 严格解析：UTF-8、重复 Key 拒绝、非有限数字拒绝、顶层 Object 结构。
2. 从可信 Receiver 配置加载精确 H Schema Artifact；校验 Schema ID、Artifact Revision、Wire Version、Message Type 与结构 Schema。
3. 从 Payload **之外**取得受保护 Transport/Session/Workload Verifier Context。Payload Sender/Issuer/Subject/Key/Audience 仅是不可信 Claim。
4. 通过已认证配置与相关 Owner 批准的 Profile Registry，解析 Sender Authority 与精确 Envelope Signature Profile。不得仅凭 Payload 字段选择可信 Key/Profile。
5. 在 Owner 批准的版本化 Profile 下重建精确 Envelope P0 与 Signed Preimage；重算 payload_digest；验证 Signature 与 Key Status/History。Envelope P0 必须明确规定 schema_artifact_revision、schema_version、message_nonce、audience、sender/issuer/subject、owner_authority、owner_record_ref、消息专属字段、integrity_proof_ref 与 channel_binding_proof_ref 的处理方式。
6. 将 Channel-Binding Proof 与受保护 Session 核对；将 Issuer/Principal/Subject/Audience 绑定到已认证 Verifier Result；Claim 不一致则拒绝。
7. 通过权威 Replay Ledger 执行 Nonce 唯一性/Replay Window 与 Message Identity/Idempotency 检查。Replay Authority 不可用时为 UNKNOWN，不得视为成功。
8. 只有外层 Envelope 认证通过后，才执行 C Object 解引用/等值/C-P0 验证，再执行独立 I/D/Storage/COC Join 与 Currentness 检查。
9. 三态结果：已证明矛盾为 INVALID；Profile/Trust/Key Status/Transport Context/Channel Binding/Replay Ledger/Authority Evidence 缺失或不可用为 UNKNOWN；全部必需检查验证后才可 VALID。

## 4. Ownership decisions required / 必需 Owner 决策

| Question | Owner authority | Required decision |
|---|---|---|
| Exact envelope P0 allowlist, canonical bytes, domain separation and signature preimage | H owns wire contract; signing Owner must accept its own semantic projection | Publish exact field-by-field P0 and negative vectors; do not reuse C object P0 implicitly |
| Which principal signs the outer envelope for C_PROVIDER_OUTCOME_RECORDED: C adapter, H gateway, or separate attestor? | C owns provider semantic event and adapter identity; H owns gateway transport; I owns trust binding | Explicitly distinguish origin signature from gateway receipt/attestation; no signature-role ambiguity |
| Signature profile ID, algorithm approval, key registry, revocation/history and anti-rollback | I owns trust/security governance; C owns C profile semantics | I approves trust/key lifecycle; C approves any C-owned envelope signer/profile; H only maps wire |
| Protected transport/session identity and channel binding | H obtains verifier context; I validates trust and Principal/authorization | Define exact authenticated verifier output and claim-comparison rules |
| Nonce/replay ledger, expiry and idempotency semantics | H transport contract + message owner; I security policy | Identify authoritative ledger, retention window, failover behavior and UNKNOWN conditions |
| Durable acceptance boundary | Storage owns persistence semantics; H owns ingress acceptance sequence | Persist only after authenticated envelope acceptance; define crash/replay/retry semantics |

Critical separation: C's AIMBA-C-CRYPTO-1.0 currently signs the immutable CSubmitOutcome object. It is not automatically an approved signature profile for the distinct outer BMCP envelope. I's AIMBA-I-CRYPTO-1.0 is I-owned and must not be applied to C-originated envelope semantics without explicit authority. H cannot choose or silently reuse either profile.

关键分离：C 的 AIMBA-C-CRYPTO-1.0 当前签署的是不可变 CSubmitOutcome Object，不自动成为独立外层 BMCP Envelope 的批准签名 Profile。I 的 AIMBA-I-CRYPTO-1.0 属于 I，不得未经明确授权应用到 C-originated Envelope 语义。H 不能自行选择或静默复用任一 Profile。

## 5. Required conformance matrix / 必需符合性矩阵

- exact valid outer envelope P0/signature/profile → continue to C object validation;
- mutate each signed envelope field, payload_digest or signature → INVALID;
- unknown/unregistered signature profile or key → UNKNOWN or INVALID according to authenticated registry result; never downgrade;
- revoked/compromised/retired key at signing time or now → apply I historical/current key-status policy; no local H inference;
- wrong issuer/principal/subject/audience or transport binding → INVALID;
- missing protected transport context or channel-binding evidence → UNKNOWN/INVALID per explicit policy; never trust payload mirror;
- duplicate nonce/replayed message/expired message → reject under exact replay policy;
- duplicate JSON keys/invalid UTF-8/non-finite numbers → INVALID at raw parser;
- C object signature valid but outer envelope signature invalid → overall INVALID;
- outer envelope valid but C object digest/signature invalid → overall INVALID;
- unavailable outer auth or C object verifier → UNKNOWN; never VALID.

- 精确有效 Outer Envelope P0/Signature/Profile → 才继续 C Object 校验；
- 任一签名 Envelope 字段、Payload Digest 或 Signature 变异 → INVALID；
- 未知/未注册 Signature Profile 或 Key → 按已认证 Registry Result 返回 UNKNOWN/INVALID，禁止降级；
- 签名时或当前 Key 已 Revoked/Compromised/Retired → 执行 I 历史/当前 Key Status Policy，不由 H 本地推断；
- Issuer/Principal/Subject/Audience 或 Transport Binding 不匹配 → INVALID；
- 缺少 Protected Transport Context/Channel-Binding Evidence → 按明确策略 UNKNOWN/INVALID，绝不信任 Payload Mirror；
- Nonce 重复、Message Replay、过期 → 按精确 Replay Policy 拒绝；
- Duplicate JSON Key/Invalid UTF-8/Non-finite Number → Raw Parser 阶段 INVALID；
- C Object Signature 有效但 Outer Envelope Signature 无效 → 总体 INVALID；
- Outer Envelope 有效但 C Object Digest/Signature 无效 → 总体 INVALID；
- Outer Auth 或 C Object Verifier 不可用 → UNKNOWN，绝不 VALID。

## 6. Gate impact / Gate 影响

This gap does not invalidate the bounded 42-test local H/C object conformance result. It narrows its claim: authenticated outer-envelope acceptance is NOT TESTED / NOT PROVEN. No current Gate status is upgraded or downgraded by this analysis.

- H outer-envelope authentication: **OPEN**.
- C envelope signer/profile ownership decision: **OPEN**.
- I trust/key/transport identity binding decision: **OPEN**.
- Production H gateway integration: **NOT IMPLEMENTED / NOT VERIFIED**.
- Gate A: PARTIAL PASS / OPEN.
- Gate B: BLOCKED.
- Gate C: DEFERRED TO ENGINEERING / NOT RUN.
- JF-10 P0, R1/R2: OPEN.
- Production activation: NOT AUTHORIZED.

本缺口不推翻有限的 42 项本地 H/C Object 符合性结果，但必须收窄其声明：外层 Envelope Authentication **未测试/未证明**。本分析不提升或降低任何现有 Gate。

- H Outer Envelope Authentication：OPEN。
- C Envelope Signer/Profile 权属决策：OPEN。
- I Trust/Key/Transport Identity Binding 决策：OPEN。
- Production H Gateway Integration：NOT IMPLEMENTED / NOT VERIFIED。
- Gate A：PARTIAL PASS / OPEN。
- Gate B：BLOCKED。
- Gate C：DEFERRED TO ENGINEERING / NOT RUN。
- JF-10 P0、R1/R2：OPEN。
- Production Activation：NOT AUTHORIZED。

## 7. Final H disposition / H 最终结论

**ACCEPT the outer-envelope authentication gap as a blocking architecture contract item. Do not claim authenticated BMCP envelope acceptance from C object validation. Do not freeze the envelope P0, signer profile or key/identity policy until H/C/I decisions are exact-versioned and cross-reviewed.**

**将外层 Envelope Authentication 缺口列为阻塞性架构合同事项。不得从 C Object 校验推导出 BMCP Envelope 已认证。在 H/C/I 完成精确版本化决策与交叉审查前，不冻结 Envelope P0、Signer Profile 或 Key/Identity Policy。**

---
**Provenance:** delegated H-role architecture analysis in the coordinating session; not an independent human H Owner decision.
