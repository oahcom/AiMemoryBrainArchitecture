# H Gateway/Auth Contract Proposal v0.1.0 — Outer Envelope Authentication
# H Gateway/Auth 合同提案 v0.1.0 — 外层 Envelope 身份认证

- Status: **P COORDINATOR PROPOSAL / H-I JOINT REVIEW REQUIRED / NOT NORMATIVE / NOT IMPLEMENTED**
- H Unified schema: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`.
- H envelope/versioning contract: Blob `5547ecd78d118bd63e571e5daad87194d9b694e4`.
- H expanded Provider Outcome closure: Blob `60e5eb98a07efcf87bc3f2be6fcf7fedb2196504`.
- I security review identifying the gap: Blob `df869ef90e6279602b4d46128a81b2dc6ba01d71`.
- Provenance: Session P proposal, simulating H/I coordination. Not an H Owner or I Owner decision.

## 1. Problem statement / 问题定义

The current Provider Outcome full-path validator verifies the inner CSubmitOutcome object and its H wire mapping, including local schema validation, object/wire equality, C semantic predicates and C-P0 digest recomputation. It does **not** authenticate the outer H envelope's own `payload_digest`, `signature`, `integrity_proof_ref`, `channel_binding_proof_ref`, issuer/key status, or sender identity against the authenticated transport principal.

The H Unified 1.2.14 common envelope contains the relevant fields, and the H envelope/versioning contract already states that `source` and payload identity fields are assertions, not authentication. A separate Gateway/Auth acceptance boundary is therefore required before any durable acceptance.

当前 Provider Outcome Full-Path Validator 验证内层 CSubmitOutcome 对象及 H Wire Mapping，包括本地 Schema、Object/Wire 一致性、C Semantic Predicate 和 C-P0 Digest 重算。但它**没有认证外层 H Envelope 自身的** `payload_digest`、`signature`、`integrity_proof_ref`、`channel_binding_proof_ref`、Issuer/Key Status，也没有将 Sender Identity 与 Authenticated Transport Principal 绑定。

H Unified 1.2.14 Common Envelope 已包含相关字段；H Envelope/Versioning 合同也已明确 `source` 与 Payload Identity 是声明而非认证。因此必须建立独立 Gateway/Auth Durable-Acceptance 边界。

## 2. Authority separation / 权威边界

| Concern | Authority | H Gateway responsibility |
|---|---|---|
| Envelope wire schema, canonicalization profile application, digest recomputation, signature envelope parsing | H | Implement strict validation and reject unsupported/ambiguous profiles; never invent profile semantics |
| Trust root, issuer registration, key ownership/status, revocation/compromise ordering, historical verification, anti-rollback | I | Call I-authoritative verifier; never mint trust or cache a permissive result |
| Authenticated transport principal and channel binding | I-approved transport/security mechanism; H integrates | Obtain principal from trusted transport/session context, not from payload |
| Sender/subject/issuer/policy-domain binding | I policy and registered authority; H enforces returned exact binding | Compare all payload identity claims against authenticated principal and authorized registration |
| Envelope message replay (message_id/message_nonce) | H Gateway replay ledger under I-approved identity scope | Atomic dedupe/nonce enforcement; separate from C provider idempotency and COC participant identity |
| C Provider Outcome object | C | Validate inner object using C-owned schema/profile/evidence; never infer outer envelope authenticity |
| D Forget clearance | D | Verify through D-owned adapter after outer auth |
| Storage resolution / COC | Storage / COC | Verify through Storage-owned adapter after outer auth |

## 3. Required validation pipeline / 必需验证流水线

The following is a proposed ordering. H and I must jointly approve the exact profile/projection details before it becomes normative.

1. **Transport principal acquisition:** obtain the authenticated principal and session/channel identity from the trusted transport/security layer. No payload field may supply or override this identity.
2. **Strict envelope parsing:** reject duplicate JSON members, invalid UTF-8, non-finite numbers, ambiguous encodings and unsupported schema/message types. Parsing/schema preflight is not durable acceptance.
3. **Profile resolution:** resolve the exact `signature_profile_id`, `canonicalization_profile_id`, digest/signature algorithms, issuer, `key_id_ref` and immutable `key_version` through I-authoritative registration/status. Missing or stale registry state is UNKNOWN.
4. **Canonical envelope digest:** construct the exact versioned signing/digest projection. Recompute SHA-256 over the canonical envelope projection. The profile must explicitly define whether integrity/signature metadata is excluded; implementation must not guess or silently self-exclude fields.
5. **Signature verification:** verify the exact signature over the profile-defined preimage using the exact registered issuer/key version. Verify key validity at the relevant signed time and current revocation/compromise/anti-rollback state.
6. **Channel binding:** verify `channel_binding_proof_ref` against the live authenticated session/channel, nonce, audience and message identity. A reference string alone is not proof.
7. **Identity/audience binding:** bind `sender_authority_ref`, `sender_subject_ref`, `issuer_ref`, `subject_ref`, `owner_authority` and `policy_domain_ref` to the authenticated principal and I-approved registration/policy. Reject principal, audience or PolicyDomain mismatch.
8. **Replay and expiry:** verify `message_nonce`, `message_id`, `expires_at` and the owner-approved replay horizon. Same immutable message identity/digest returns the prior accepted result; same identity/nonce with a different digest is INVALID. Replay state must be durably recorded atomically with the accepted envelope or its durable inbox receipt.
9. **Inner payload validation:** only after outer authentication, validate H message-family schema, CSubmitOutcome 1.0.1 schema/object dereference, C semantics and C-P0 digest; then run independent C/I/D/Storage authority joins.
10. **Durable acceptance:** atomically persist the authenticated envelope identity/digest, replay/dedupe receipt and accepted inbox/COC record according to the selected Storage transaction profile. No VALID/durable-accepted result may be emitted while any required authority is UNKNOWN.

## 4. Result semantics / 结果语义

| Result | Meaning | Durable acceptance |
|---|---|---|
| `VALID` | Envelope digest/signature, key status, channel binding, principal/issuer/audience/scope, replay and expiry all verified against exact current authority evidence | Allowed to proceed to inner payload and owner joins; not yet proof of business application |
| `INVALID` | Cryptographic mismatch, malformed canonical form, unsupported required profile, wrong key/issuer/principal/audience/PolicyDomain, replay conflict, expired message or proven revocation | Forbidden; reject and emit security telemetry without disclosing protected payload |
| `UNKNOWN` | I registry/key-status unavailable, stale checkpoint, channel verifier unavailable, principal binding unavailable, replay ledger unavailable or anti-rollback/currentness cannot be established | Forbidden; quarantine/retry only under bounded policy, never downgrade to VALID |

The outer-envelope `VALID` result does not mean C Provider Outcome is valid, I has authorized an operation, D has cleared Forget, Storage has committed visibility, or the business operation is Applied. Each remains a separate proof.

外层 Envelope 的 `VALID` 不意味着 C Provider Outcome 有效、I 已授权、D 已解除 Forget、Storage 已提交可见性或业务操作已 Applied。它们仍是独立证明。

## 5. Required negative and race vectors / 必需负向与竞态向量

1. Flip one payload byte while retaining old digest/signature → INVALID.
2. Change canonicalization profile ID without re-signing → INVALID.
3. Unknown or unsupported signature profile/algorithm → INVALID; unavailable authoritative profile registry → UNKNOWN.
4. Substitute `key_id_ref` or `key_version` → INVALID.
5. Revoked/compromised key at signed time or current time → INVALID according to I ordering; unavailable key-status checkpoint → UNKNOWN.
6. Signature valid under an unregistered issuer → INVALID.
7. `sender_authority_ref` or `sender_subject_ref` differs from authenticated transport principal → INVALID.
8. `issuer_ref` / `subject_ref` mismatch registered key owner → INVALID.
9. Wrong `audience` or PolicyDomain → INVALID.
10. Channel-binding proof belongs to another TLS/session/channel → INVALID.
11. Channel-binding verifier unavailable or session binding cannot be proven → UNKNOWN.
12. Replay same message_id/nonce with identical digest → return prior receipt; do not repeat side effects.
13. Replay same message_id/nonce with different digest → INVALID and security event.
14. Concurrent duplicate delivery across two gateway replicas → exactly one durable inbox acceptance; the other returns the same receipt.
15. Replay ledger unavailable or split-brain currentness uncertain → UNKNOWN; no durable acceptance.
16. Expired envelope → INVALID/EXPIRED; clock source uncertainty beyond the approved bound → UNKNOWN.
17. Duplicate JSON members, invalid UTF-8, non-finite numbers or ambiguous canonical form → INVALID.
18. Attempt algorithm downgrade or fallback to an unauthenticated transport → INVALID.
19. Outer envelope digest differs from inner C `payload_digest` or C-P0 digest but each is independently valid → preserve distinct digest domains; never compare as if they were the same digest.
20. Inner C object is valid but outer H signature/principal is invalid → reject before owner joins and durable acceptance.
21. Outer envelope is valid but C/I/D/Storage evidence is missing → envelope may be authenticated, but complete message acceptance remains UNKNOWN.
22. I trust/currentness evidence is stale between verification and durable acceptance → final I currentness check/CAS must fail closed; do not commit using a stale authorization snapshot.

## 6. Profile and contract questions that must not be guessed / 不得猜测的 Profile/合同问题

H/I must resolve explicitly:
- the exact JCS/canonicalization profile identifier and signed projection;
- whether `integrity_proof_ref`, `signature`, timestamps, and transport/channel proof references are included or excluded from the signed preimage;
- the precise signature algorithm and profile registry version;
- key validity-time semantics, revocation/compromise retroactivity and historical verification rules;
- exact transport principal representation and channel-binding exporter/evidence contract;
- nonce uniqueness scope, replay retention horizon and cross-replica atomicity;
- whether outer envelope authentication is performed at ingress gateway, durable inbox, or both, and the exact revalidation boundary for queued/replayed messages.

The current schema fields and the older envelope document do not, by themselves, resolve these normative choices. No algorithm, signature projection, principal type or replay window is selected by this P proposal.

H/I 必须明确解决：JCS/Canonicalization Profile 与签名投影；Integrity/Signature/时间戳/Channel Proof 是否纳入 Preimage；签名算法与 Profile Registry；Key Validity/Revocation/Historical Verification；Transport Principal 与 Channel Binding；Nonce 唯一性范围、Replay Retention 与跨副本原子性；Ingress Gateway、Durable Inbox 和 Queued/Replay 的认证时点。

当前 Schema 字段和旧 Envelope 文档本身不足以解决这些规范选择。本 P 提案没有擅自选择算法、签名投影、Principal 类型或 Replay 窗口。

## 7. Gate and implementation boundary / Gate 与实现边界

- **P0 security gate:** outer H envelope authentication and transport-principal binding must be specified, independently reviewed and tested before durable acceptance is authorized.
- H owns gateway parsing/canonicalization/signature-validation orchestration and exact wire behavior.
- I owns trust, issuer/key registration, revocation, authorization and anti-rollback authority.
- Storage owns atomic replay receipt + durable inbox acceptance semantics and physical serialization proof.
- C/D/I/Storage business proofs remain separate; no H callback may self-assert their truth.
- Current 38-test Provider Outcome suite does not close this gate.
- This proposal is design-only; no H/I production adapter or Gateway/Auth implementation is claimed.

## 8. Proposed next sequence / 后续顺序

1. H Owner publishes a normative Gateway/Auth contract with exact profile and projection references.
2. I Owner approves the trust/principal/key-status/revocation/anti-rollback boundary.
3. Storage Owner defines the atomic replay/durable-inbox persistence boundary against the selected L1/L4 topology.
4. H adds real envelope-level positive and negative conformance fixtures, including multi-replica replay races.
5. C/I/D review the ordering boundary to ensure no inner owner join or provider egress occurs before outer authentication.
6. A performs exact integration review; only then may the P0 security gate be reconsidered.

**Disposition: PROPOSAL FOR H/I/STORAGE REVIEW; NOT NORMATIVE / NOT IMPLEMENTED / NOT FROZEN.**
