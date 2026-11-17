# Phase 3.8.6 — D Membership Proof P0 Crosswalk to RecoveryJoin 1.0.2
# Phase 3.8.6 — D Membership Proof P0 与 RecoveryJoin 1.0.2 精确映射

- Owner perspective: D — Memory Brain / ForgetFence Authority
- Status: **ACCEPT GENERIC RECOVERYJOIN P0 WITH EXPLICIT D-ROW DIGEST INDIRECTION; CANDIDATE / NOT FROZEN**
- D owner membership proof contract: Blob `d80dabe7210e681bc4e2290355a38f8b67be9ddd`
- D Forget Fence contract: Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`
- D Gate Release currentness contract: Blob `7f2861d9441b9be6c8e69f41fd0276636be483a8`
- H Unified schema 1.2.14: Blob `fee452efb99ab4fe0ceccb347c46eeef1521bd28`
- H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- Provenance: delegated D-role technical decision; **not an independent human D Owner signature**.

## 1. Decision / 决议

D adopts the closed generic RecoveryJoin 1.0.2 `ownerSnapshotMembershipProof` as the serialized D membership-proof envelope. D-specific Forget/lineage/barrier semantics remain fully bound by the exact D owner-ledger entry, ForgetOperation record, scope binding and signed owner snapshot. They are not silently omitted; they are committed by the generic proof's exact reference/digest fields and H 1.2.14 D high-water summary.

D 将 RecoveryJoin 1.0.2 封闭通用 `ownerSnapshotMembershipProof` 作为序列化 D Membership Proof Envelope。D 专属 Forget/Lineage/Barrier 语义仍由精确 D Owner Ledger Entry、ForgetOperation Record、Scope Binding 和签名 Owner Snapshot 完整绑定。它们不是被静默省略，而是由通用 Proof 的精确引用/摘要字段与 H 1.2.14 D High-Water Summary 承诺。

## 2. Exact generic P0 / 通用 P0

The serialized D proof P0 contains exactly the RecoveryJoin 1.0.2 generic fields:
`proof_ref`, `owner_kind=D`, `owner_authority_ref`, `issuer_ref`, `subject_ref`, `audience_ref`, `purpose`, `owner_ledger_ref`, `owner_ledger_version`, `owner_entry_ref`, `owner_entry_digest`, `owner_admission_ref`, `owner_sequence_namespace`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root`, `owner_snapshot_ref`, `owner_snapshot_digest`, `owner_snapshot_attestation_ref`, `owner_snapshot_attestation_digest`, `owner_gate_ref`, `owner_gate_generation`, `scope_ref`, `scope_generation`, `scope_binding_digest`, `operation_identity_ref`, `operation_digest`, `request_digest`, `anti_rollback_anchor_ref`, `key_status_generation`, `signature_profile_ref`, `key_id`, `key_version`, `canonicalization_profile_ref`, `digest_profile_ref`.

Exclude derived `proof_digest` and external `signature_ref` from P0. Compute `proof_digest` over D domain-separated JCS(P0); signature projection is P0 plus the digest. No D-only field is appended as an untyped extra property to H's closed generic object.

## 3. D-specific no-loss dereference map / D 专属字段无损解引用映射

| D semantic fact | Generic RecoveryJoin binding | Required D-side verification |
|---|---|---|
| D BrainAuthority / owner kind | `owner_authority_ref`, `owner_kind=D` | Resolve to the unique D Canonical Brain authority |
| D producer/work/attempt/derivative/barrier ledger row | `owner_ledger_ref/version`, `owner_entry_ref/digest`, `owner_admission_ref` | The canonical D row digest commits to row kind, producer registration, WorkItem/Attempt/Derivative/Barrier identity and all typed owner fields |
| D local namespace/sequence/high-water | `owner_sequence_namespace`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root` | All counters remain D-local; no comparison with I/C/COC/Storage |
| ForgetOperationRef and operation semantics | `operation_identity_ref`, `operation_digest` | Exact D ForgetOperation canonical record; digest commits to operation identity, target selector and immutable request semantics |
| Target/source/ancestor lineage | `scope_ref`, `scope_generation`, `scope_binding_digest` | Exact D lineage selector and ancestor closure are included in the D operation/entry canonical bytes and digest |
| Per-row ForgetFenceGeneration | `owner_entry_ref/digest`, `operation_identity_ref/digest` | Exact D fence row contains its own ForgetFenceGeneration and ForgetFenceCursor; row digest commits to the exact value |
| Current D ForgetFenceGeneration high-water | H 1.2.14 `ownerSpecificHighWatersD.forget_fence_generation_high_water` | D snapshot attestation binds the captured high-water; every included fence row is at/below it |
| D Gate ref/generation | `owner_gate_ref`, `owner_gate_generation` | D Gate identity/revision only; never aliases ForgetFenceGeneration or barrier generation |
| Barrier generation/root | H 1.2.14 `ownerSpecificHighWatersD.barrier_generation/barrier_root` plus `owner_specific_high_waters_digest` | Exact barrier snapshot and ordered member root; member identity/dependency closure committed by D entry and barrier row digests |
| Snapshot/attestation/ledger root | `owner_snapshot_ref/digest`, `owner_snapshot_attestation_ref/digest`, `owner_ledger_root` | D verifies complete producer/work/attempt/derivative/barrier query, pagination, counts, ordered set root and anti-rollback |
| Request and authorization context | `request_digest`, `operation_digest`, scope binding | D verifies exact request, scope and I authorization reference; H cannot mint D/I decision |
| D anti-rollback/key/signature | `anti_rollback_anchor_ref`, `key_status_generation`, signature profile/key/canonicalization/digest fields | D verifies its signer and I-governed trust/currentness |

The H 1.2.14 D high-water object is exactly:
- `producer_registration_high_water`;
- `work_item_high_water`;
- `attempt_high_water`;
- `barrier_generation`;
- `barrier_root`;
- `forget_fence_generation_high_water`.

The final field is distinct from both `owner_gate_generation` and `barrier_generation`. The exact per-row ForgetFenceGeneration is committed by the D row digest; the snapshot high-water proves the captured current fence range. H verifies the summary digest and exact typed joins; D alone verifies fence semantics and completeness.

## 4. Required negative vectors / 必需负向向量

1. D entry digest omits or mutates ForgetFenceGeneration → INVALID.
2. D snapshot `forget_fence_generation_high_water` is stale or lower than an included fence row → INVALID.
3. Substitute `owner_gate_generation` or `barrier_generation` for ForgetFenceGeneration → INVALID.
4. Change target/source/ancestor scope while retaining operation ref → scope-binding digest mismatch, INVALID.
5. Omit a barrier member or dependency row while retaining old barrier root → INVALID.
6. Incomplete D ledger pagination or unavailable anti-rollback/key status → UNKNOWN, not COMPLETE_EMPTY.
7. Use I/C/COC/Storage counters as D local sequence → INVALID.
8. Add D-only properties directly to the generic RecoveryJoin proof object → schema INVALID; D-specific facts belong in the referenced canonical D row and D high-water summary.

## 5. D disposition / D 侧结论

**D ACCEPTS THE GENERIC RECOVERYJOIN 1.0.2 P0 WITH THE ABOVE D-ROW DIGEST INDIRECTION AND H 1.2.14 FENCE HIGH-WATER AS AN L1/L2 CANDIDATE.** This preserves the closed generic proof schema while keeping all D semantics committed and independently D-verifiable. H cannot attest D ledger completeness or issue D release.

**D 接受 RecoveryJoin 1.0.2 通用 P0、上述 D Row Digest 解引用映射及 H 1.2.14 Fence High-Water 作为 L1/L2 候选。** 该方案保留封闭通用 Proof Schema，同时确保 D 语义被完整承诺并由 D 独立验证。H 不得认证 D Ledger 完整性或签发 D Release。

Remaining L3: exact D canonical-row schema/vectors, full producer/dependency pagination, late-discovery and stale-fence fault campaigns, D key lifecycle, I trust integration, independent human D Owner approval and physical Storage realization remain OPEN.
