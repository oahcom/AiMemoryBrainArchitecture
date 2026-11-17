# Phase 3.8.4 — C Owner Snapshot Membership Proof Contract
# Phase 3.8.4 — C Owner Snapshot Membership Proof 合同

- Owner: C — Agent Integration / Provider Outcome Authority
- Status: **PROPOSED / CANDIDATE ONLY — NOT APPROVED OR FROZEN**
- Applies to C admissions, reservations, provider attempts and outcomes in H Unified Manifest 1.2.11 / wire 1.3.0.

## 1. Authority boundary

C alone attests C request/admission/reservation/provider-attempt/provider-outcome ledger rows and provider-boundary observations. A COC ParticipantIntent, Storage receipt, I authorization, D fence proof or H transport ACK cannot synthesize C Provider Outcome.

## 2. Proof required for each C row

Every C row represented in a COC participant binding or as an unregistered owner-local admission MUST carry one immutable `CAdmissionSnapshotMembershipProof` binding:

- `proof_ref`, `owner_kind=C`, C Adapter/ProviderAccount authority ref;
- exact C ledger ref/version, row/entry ref and entry digest;
- exact C admission/reservation/provider-attempt/outcome refs and row kind;
- C-local sequence namespace/value and captured request, admission, reservation, provider-attempt and provider-outcome high-waters as applicable;
- immutable C snapshot ref/digest, snapshot-attestation ref/digest and complete C ledger root;
- C Gate ref/generation, adapter/provider-account/egress-gate identity and scope binding digest;
- operation identity/digest, immutable final request digest, provider idempotency namespace/key ref;
- COC ParticipantIntentRef/reservation ref or explicit null plus absence reason;
- provider receipt/lookup evidence ref/digest when the row is an outcome;
- independent C anti-rollback anchor, key-status generation and C signature-profile/key/version/signature refs.

All C counters remain within their C-owned namespace. No comparison to I/D counters or COC indexes is permitted.

## 3. Membership and completeness

The proof attests that the exact row is included in the frozen signed C snapshot and at/below its applicable C-local high-water. Completeness additionally requires the exact provider/account/adapter query projection, pagination completion, counts, ordered set root, request/admission/reservation/provider-attempt/provider-outcome high-waters and anti-rollback checkpoint.

A membership proof does not prove provider success. Provider truth remains a separate immutable CSubmitOutcome derived from actual provider receipt or authoritative same-key lookup. UNKNOWN/IN_DOUBT stays blocking. A missing COC ParticipantIntent is represented as explicit null plus reason; it is not repaired by fabricating a participant. Empty C sets require a separate signed COMPLETE_EMPTY proof.

## 4. C signature projection and verification

C owns the proof P0, canonical digest preimage and signature profile. It binds every field in §2 plus issuer/subject/audience/purpose, adapter/provider-account/egress-gate identity, gate generation, immutable request boundary, idempotency namespace/key and snapshot roots. Only signature bytes/ref and explicitly derived digest fields are excluded.

The verifier checks C key status, signature, exact adapter/provider-account scope, snapshot membership, high-water inclusion and anti-rollback anchor. H cannot infer provider outcome from the membership proof.

## 5. Gate/recovery semantics

C Gate Release validates all C membership proofs and reconciles every reservation, attempt and outcome in the frozen C snapshot. The final provider send-vs-close linearization remains owned by the transport-owning C Adapter. Recovery must keep provider invocation/retry closed until Batch and Manifest S4 readback and semantic join complete. Ambiguous handoff is reconciled only using the same immutable request/attempt and provider idempotency key; if the provider lacks authoritative same-key lookup, IN_DOUBT may persist indefinitely.

A membership proof is not an egress permit, provider outcome, successful delivery or exactly-once guarantee.

## 6. Decision boundary

This is a C-role proposal in the coordinating session, not independent human C Owner approval. Provider-specific key custody, same-key lookup authority, receipt authenticity, durable C ledger/adapter serialization and real provider fault-injection remain unimplemented/unverified. No production provider acceptance or production activation is claimed.


## 7. H Unified 1.2.16 C snapshot field mapping — CANDIDATE / OWNER DECISION REQUIRED

H Unified 1.2.16 introduces C-specific snapshot high-waters:
- `provider_idempotency_namespace_ref`
- `final_request_boundary_generation`
in addition to reservation, provider-attempt and provider-outcome high-waters.

Candidate C semantics:
1. `provider_idempotency_namespace_ref` identifies the exact C-owned provider/account/adapter idempotency namespace frozen by this snapshot. It is an opaque namespace reference, never the secret idempotency key.
2. `final_request_boundary_generation` is a proposed C-local monotonic generation for the exact final-request-boundary registry/snapshot. It must be bound to the final request boundary identity/digest and the C provider idempotency namespace. It is not CSubmitOutcome record_sequence, C key-status event_sequence, H signing sequence, or COC index.
3. The generation must not silently reset or be reused after adapter/provider-account reconfiguration, boundary replacement or restore. The owner must specify whether such changes advance the same namespace generation or create a new namespace identity.
4. Both fields MUST be included in the C-signed owner snapshot attestation P0 and canonical `owner_specific_high_waters_digest`. A missing or ambiguous namespace/generation keeps C provider reconciliation and owner-gate release blocked.

C Phase 3.11.1 defines CSubmitOutcome 1.0.1 required `sequence_namespace_ref` for the C signing/key-status event sequence; that field is distinct from the proposed snapshot-only `final_request_boundary_generation`. CSubmitOutcome 1.0.1 schema Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` does not define final_request_boundary_generation. Therefore H 1.2.16 does not establish that C has already accepted this new generation field or that it is part of CSubmitOutcome wire semantics.

H schema 1.2.16 exact Blob `91c4fd70cb1e1cff76d733baa180325bd2da84c1` and concrete I/D/C instance tests Blob `e1667b0f9526884c56c311bf1bcf8af6af0b9477` passed within H run #44192602325 (356 tests, 22 skipped). H 1.2.17 semantic reference validator/test Blobs `60cd1b686eaa9ac364c69a708353fa0e5f635197` / `24d3cf0730a138f25719cb1e29de28f833a00cdf` bind the exact C snapshot across Batch and Manifest roots; exact H code Head `f08dadd...` passed run #44193331446 (390 tests, 22 skipped).

**C candidate disposition:** provider idempotency namespace aligns with existing C authority. FinalRequestBoundaryGeneration is a new C-owned snapshot concept and remains PROPOSED until C defines scope, monotonicity, reset/restore semantics, digest projection and exact relation to FinalRequestBoundaryRef/RequestDigest. This append is delegated C-role candidate work, not independent human C Owner approval and not production C profile registration.

### 中文：H Unified 1.2.16 C Snapshot 字段映射 — 候选 / 需 Owner 决策

H Unified 1.2.16 新增 C 专属 Snapshot High-water：`provider_idempotency_namespace_ref`、`final_request_boundary_generation)，并保留 Reservation、Provider Attempt 和 Provider Outcome High-water。

候选 C 语义：
1. `provider_idempotency_namespace_ref` 标识该 Snapshot 冻结的精确 C-owned Provider/Account/Adapter Idempotency Namespace；它是不透明 Namespace Ref，不是秘密 Idempotency Key。
2. `final_request_boundary_generation` 是提议中的 C-local 单调 Generation，用于精确 Final Request Boundary Registry/Snapshot；必须绑定 Final Request Boundary Identity/Digest 和 C Provider Idempotency Namespace。它不等于 CSubmitOutcome record_sequence、C Key-status event_sequence、H Signing Sequence 或 COC Index。
3. Adapter/Provider Account 重配置、Boundary 替换或 Restore 后不得静默重置/复用该 Generation。C Owner 必须明确此类变更是推进同一 Namespace Generation，还是创建新的 Namespace Identity。
4. 两个字段都必须进入 C 签名 Owner Snapshot Attestation P0 和规范化 `owner_specific_high_waters_digest`。Namespace/Generation 缺失或歧义时，C Provider Reconciliation 与 Owner Gate Release 必须阻塞。

C Phase 3.11.1 为 CSubmitOutcome 1.0.1 定义必需的 `sequence_namespace_ref`，用于 C Signing/Key-status Event Sequence；它与提议的 Snapshot-only `final_request_boundary_generation` 不同。CSubmitOutcome 1.0.1 Schema Blob `a631bc7...` 并未定义 final_request_boundary_generation。因此 H 1.2.16 不代表 C 已接受该新 Generation 字段，也不代表它属于 CSubmitOutcome Wire Semantics。

H Schema 1.2.16 Blob `91c4fd7...` 和 I/D/C 实例测试 Blob `e1667b0...` 在 H Run #44192602325 中通过（356 项，22 项 skipped）。H 1.2.17 Validator/Test Blob `60cd1b6...` / `24d3cf0...` 将精确 C Snapshot 绑定到 Batch/Manifest Root；精确 H Head `f08dadd...` 的 Run #44193331446 通过 390 项。

**C 候选结论：** Provider Idempotency Namespace 与现有 C 权威一致；FinalRequestBoundaryGeneration 是新的 C-owned Snapshot 概念，在 C 明确 Scope、Monotonicity、Reset/Restore Semantics、Digest Projection 以及与 FinalRequestBoundaryRef/RequestDigest 的关系之前保持 PROPOSED。本追加是委派 C 角色候选，不是独立人类 C Owner 批准，也不是生产 C Profile 注册。
