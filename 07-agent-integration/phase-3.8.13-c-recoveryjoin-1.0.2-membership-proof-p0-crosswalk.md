# Phase 3.8.13 — C Membership Proof P0 Crosswalk to RecoveryJoin 1.0.2
# Phase 3.8.13 — C Membership Proof P0 与 RecoveryJoin 1.0.2 精确映射

- Owner perspective: C — Agent Integration / Provider Outcome Authority
- Status: **ACCEPT GENERIC RECOVERYJOIN P0 WITH EXPLICIT C-ROW DIGEST INDIRECTION; CANDIDATE / NOT FROZEN**
- C owner membership proof contract: Blob `5e37185610869951c3b392c9ad143a72b4c702ac`
- CSubmitOutcome schema 1.0.1: Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- C Phase 3.11.1 sequence namespace amendment: Blob `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb`
- H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- H Unified schema 1.2.14: Blob `fee452efb99ab4fe0ceccb347c46eeef1521bd28`
- C Provider Outcome mapping target: H Phase 3.8.10, Unified 1.2.14 → CSubmitOutcome 1.0.1
- Provenance: delegated C-role technical decision; **not an independent human C Owner signature**.

## 1. Decision / 决议

C adopts the RecoveryJoin 1.0.2 generic `ownerSnapshotMembershipProof` as the serialized C membership-proof envelope. C-specific facts MUST NOT be silently discarded: they are committed by the exact C owner-ledger entry and immutable CSubmitOutcome object referenced by the generic envelope. The owner-specific P0 is the generic schema P0 plus its exact typed reference/digest bindings; it is not a second ad hoc object with unrepresented fields.

C 将 RecoveryJoin 1.0.2 的通用 `ownerSnapshotMembershipProof` 作为序列化 C Membership Proof Envelope。C 专属事实不得丢弃，而是由通用 Envelope 引用的精确 C Owner Ledger Entry 和不可变 CSubmitOutcome 对象承诺。Owner 专属 P0 即通用 Schema P0 加精确类型化引用/摘要绑定，不再另造一个无法由 H Schema 表达的第二对象。

## 2. Exact generic P0 / 通用 P0 精确字段

The serialized proof P0 contains the exact RecoveryJoin 1.0.2 fields:
`proof_ref`, `owner_kind=C`, `owner_authority_ref`, `issuer_ref`, `subject_ref`, `audience_ref`, `purpose`, `owner_ledger_ref`, `owner_ledger_version`, `owner_entry_ref`, `owner_entry_digest`, `owner_admission_ref`, `owner_sequence_namespace`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root`, `owner_snapshot_ref`, `owner_snapshot_digest`, `owner_snapshot_attestation_ref`, `owner_snapshot_attestation_digest`, `owner_gate_ref`, `owner_gate_generation`, `scope_ref`, `scope_generation`, `scope_binding_digest`, `operation_identity_ref`, `operation_digest`, `request_digest`, `anti_rollback_anchor_ref`, `key_status_generation`, `signature_profile_ref`, `key_id`, `key_version`, `canonicalization_profile_ref`, `digest_profile_ref`.

Exclude derived `proof_digest` and external `signature_ref` from P0. Compute `proof_digest` over the C domain-separated JCS(P0); the signature projection is P0 plus that digest. This is aligned with the generic H schema and C's prior signature contract.

## 3. C-specific no-loss dereference map / C 专属字段无损解引用映射

| C semantic fact | Generic RecoveryJoin binding | Required C-side verification |
|---|---|---|
| Adapter / ProviderAccount / Provider / Endpoint / Region / API operation | `owner_authority_ref`, `owner_entry_ref`, `owner_entry_digest` | The exact C owner row digest commits to all typed identities; H/C dereference and verify the C row |
| C ledger/version/entry | `owner_ledger_ref`, `owner_ledger_version`, `owner_entry_ref`, `owner_entry_digest` | Exact immutable row membership; for a Provider Outcome row, CSubmitOutcome 1.0.1 `record_ref` and `payload_digest` are the canonical row reference/digest |
| C admission | `owner_admission_ref` | Must equal CSubmitOutcome 1.0.1 `CAdmissionRef`; `CAdmissionDigest` is verified from the immutable admission record |
| C sequence namespace/local sequence/high-water | `owner_sequence_namespace`, `owner_local_sequence`, `owner_high_water` | `owner_sequence_namespace` equals C `sequence_namespace_ref`; `owner_local_sequence` equals `COwnerLocalSequence`; C ledger high-water is C-owned |
| C snapshot and attestation | `owner_snapshot_ref/digest`, `owner_snapshot_attestation_ref/digest`, `owner_ledger_root` | C verifies full query projection, pagination, set root and anti-rollback |
| C gate/generation | `owner_gate_ref`, `owner_gate_generation` | Must equal C `CGateRef/CGateGeneration` in the referenced immutable row |
| scope and operation | `scope_ref/generation/binding_digest`, `operation_identity_ref/digest`, `request_digest` | Exact C gate/scope/final request boundary and operation tuple are committed by the referenced row |
| idempotency namespace/key | `owner_entry_ref/digest`, `operation_digest`, `request_digest` | Exact C row / CSubmitOutcome 1.0.1 dereference must verify `IdempotencyNamespaceRef` and `IdempotencyKeyRef` |
| ProviderAttempt / Outcome / receipt / lookup | `owner_entry_ref/digest` | CSubmitOutcome 1.0.1 immutable object must verify ProviderAttemptRef/Generation, Outcome, SideEffectStatus, ProviderReceiptRef / ProviderLookupProofRef and evidence digest/issuer/type |
| COC intent/reservation or absence | `owner_entry_ref/digest` | CSubmitOutcome 1.0.1 P0 carries `COCParticipantIntentRef`, `COCParticipantReservationRef`, `COCAbsenceReason`; H exact mapping validates the COC pair/absence semantics |
| C anti-rollback/key/signature | `anti_rollback_anchor_ref`, `key_status_generation`, signature profile/key/canonicalization/digest fields | C verifies issuer trust, key status and historical validity; H cannot mint C truth |

The CSubmitOutcome 1.0.1 schema requires the complete provider-boundary tuple and signed `sequence_namespace_ref`. The generic membership proof does not duplicate these fields; `owner_entry_digest` commits to the exact C row and H separately dereferences the CSubmitOutcome object. A missing row, digest mismatch, namespace mismatch or stale key status is INVALID/UNKNOWN as appropriate, never VALID.

## 4. High-water mapping / High-Water 映射

H Unified 1.2.14 `ownerSnapshot` maps C high-waters as:
- top-level `request_high_water` and `admission_high_water`;
- `ownerSpecificHighWatersC.reservation_high_water`;
- `ownerSpecificHighWatersC.provider_attempt_high_water`;
- `ownerSpecificHighWatersC.provider_outcome_high_water`.

The exact five values remain C-owned and nominally incomparable to I, D, COC and Storage positions. The `owner_specific_high_waters_digest` must be recomputed over the exact C object.

## 5. C disposition / C 侧结论

**C ACCEPTS THE GENERIC RECOVERYJOIN 1.0.2 P0 WITH THE ABOVE NO-LOSS DEREFERENCE MAP AS AN L1/L2 CANDIDATE.** This resolves the apparent C-specific field mismatch without adding untyped fields to H's closed generic object. The C owner-entry digest and CSubmitOutcome 1.0.1 object are mandatory; the H envelope alone is never provider truth.

**C 接受上述 RecoveryJoin 1.0.2 通用 P0 与 C 专属无损解引用映射作为 L1/L2 候选。** 通过 C Owner Entry Digest 和 CSubmitOutcome 1.0.1 不可变对象承诺 C 专属事实，不向 H 封闭通用对象添加未定义字段。H Envelope 本身永远不能代替 Provider Truth。

Remaining L3: exact Python/Node P0 vectors for every C row kind, complete pagination/currentness proof, production C sequencer/key status, C/I profile registration, same-key provider lookup, real adapter race/fault tests and independent human C Owner approval remain OPEN.
