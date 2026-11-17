# Phase 3.8.7 — D Exact Review: H Unified 1.2.14 Fence High-Water and RecoveryJoin Membership
# Phase 3.8.7 — D 精确复审：H Unified 1.2.14 Fence High-Water 与 RecoveryJoin Membership

- Owner perspective: D — Memory Brain / ForgetFence Authority
- H Unified schema 1.2.14 Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H RecoveryJoin schema 1.0.2 Blob: `4b664e3bce465499bcdfd93796349a4ba7074002`
- D membership P0 crosswalk Blob: `c4adf827dd62d44c43b8e871dec4835581508adf`
- D original membership proof contract Blob: `d80dabe7210e681bc4e2290355a38f8b67be9ddd`
- D Forget Fence contract Blob: `1f0391bc49d007c44ec74165bd33d37412cc7990`
- D Gate Release currentness contract Blob: `7f2861d9441b9be6c8e69f41fd0276636be483a8`
- H C/D/I membership P0 cross-review Blob: `1c0ee56a96d8b2195eaa7ed4baf69d5dc27f8149`
- Status: **ACCEPT AS D-PROOF L1/L2 CANDIDATE; L3 CURRENTNESS/FAULT VECTORS OPEN**
- Provenance: delegated D-role technical review; **not an independent human D Owner signature**.

## 1. Exact H 1.2.14 delta / H 1.2.14 精确变化

H 1.2.14 adds required `ownerSpecificHighWatersD.forget_fence_generation_high_water`. D confirms this is the D-authoritative maximum captured ForgetFenceGeneration, not an alias for:
- `owner_gate_generation` (D Gate revision);
- `barrier_generation` (D barrier snapshot generation).

D 的 FenceGeneration、GateGeneration 和 BarrierGeneration 是三个不同的 D 名义类型。H 1.2.14 的新增字段准确表示 D Snapshot 捕获的 ForgetFenceGeneration High-Water，不得与另外两个字段混用。

## 2. Exact D membership binding / D Membership 精确绑定

D accepts the generic RecoveryJoin 1.0.2 P0 with the D-specific no-loss mapping in the D Phase 3.8.6 crosswalk:

- Exact D owner row (producer registration, WorkItem, Attempt, Derivative or barrier member) is committed by `owner_entry_ref/digest`.
- Exact ForgetOperation is committed by `operation_identity_ref/digest`.
- Target/source/ancestor lineage is committed by `scope_ref/generation/scope_binding_digest`.
- Per-row ForgetFenceGeneration, barrier member identity and dependency-closure evidence are inside the canonical D row and committed by `owner_entry_digest`.
- The D snapshot attestation binds `forget_fence_generation_high_water`, producer-registration/work/attempt high-waters and barrier generation/root.
- The generic proof's snapshot/attestation digests and `owner_specific_high_waters_digest` bind the exact D snapshot/high-water object.

D 接受 D Phase 3.8.6 Crosswalk 中定义的 RecoveryJoin 1.0.2 通用 P0 与无损映射：精确 D Owner Row 由 Owner Entry Ref/Digest 承诺；ForgetOperation 由 Operation Identity/Digest 承诺；Target/Source/Ancestor Lineage 由 Scope Binding Digest 承诺；逐行 FenceGeneration、Barrier Member 和 Dependency Closure 由 D Row Digest 承诺；D Snapshot Attestation 绑定 Fence 高水位及 Producer/Work/Attempt/Barrier 高水位。

## 3. D safety predicates / D 安全谓词

- Every included D fence row's generation MUST be at or below the attested `forget_fence_generation_high_water`.
- A snapshot high-water lower than an included fence row is INVALID.
- A stale snapshot or incomplete fence/producer/work/attempt/dependency pagination is UNKNOWN and cannot release the D barrier.
- A late-discovered pre-fence row invalidates the affected snapshot/barrier proof and requires a successor D snapshot; the active Forget Fence is not rolled back.
- H verifies exact shape and digest joins only. D alone verifies D ledger completeness, lineage, fence terminality and D Gate Release CAS.

## 4. Required L3 vectors / 必需 L3 向量

1. ForgetFenceGeneration row value greater than attested high-water → INVALID.
2. Substitute D GateGeneration or BarrierGeneration for ForgetFenceGeneration → INVALID.
3. Stale fence high-water after a new fence commit → UNKNOWN/INVALID and D release blocked.
4. Late-discovered pre-fence producer/work row → snapshot invalidated and barrier reopened.
5. Mutate target/source/ancestor scope, barrier member or dependency closure while retaining old D entry digest → INVALID.
6. Missing D ledger page, key status or anti-rollback anchor → UNKNOWN, never COMPLETE_EMPTY.
7. Cross-compare D counters with I/C/COC/Storage counters → INVALID.

No deterministic fault campaign or real D ledger pagination run is claimed by this review.

## 5. D disposition / D 侧结论

**D ACCEPTS H UNIFIED 1.2.14 + RECOVERYJOIN 1.0.2 AS A D-PROOF L1/L2 CANDIDATE WITH THE EXACT FENCE HIGH-WATER AND DIGEST MAPPING ABOVE.** The L1 missing-field issue is corrected. D implementation, full lineage completeness, independent owner signatures, JF-10, Global Forget and physical Storage realization remain OPEN.

**D 接受 H Unified 1.2.14 + RecoveryJoin 1.0.2 作为 D Proof L1/L2 候选，并接受上述精确 Fence High-Water 与 Digest 映射。** L1 字段缺失已修正；D 实现、完整 Lineage、独立 Owner 签署、JF-10、Global Forget 和物理 Storage 实现仍 OPEN。

This is a delegated D-role review, not independent human D Owner approval or Forget completion.
