# Phase 3.8.13 — H Exact Review of D RecoveryJoin 1.0.2 P0 Crosswalk and H 1.2.14 Fence High-Water
# Phase 3.8.13 — H 对 D RecoveryJoin 1.0.2 P0 Crosswalk 与 H 1.2.14 Fence High-Water 的精确审查

- Reviewer: H — BMCP Protocol / Schema / Interoperability
- Branch: `session-h-bmcp-protocol`
- Exact H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- Exact H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- D membership proof contract: Blob `d80dabe7210e681bc4e2290355a38f8b67be9ddd`
- D crosswalk: Blob `c4adf827dd62d44c43b8e871dec4835581508adf`
- D exact review: Blob `55ae7bc33b37f0e729949fdd2a694eb6211bbc55`
- Decision: **ACCEPT D P0/CROSSWALK AS L1/L2 CANDIDATE WITH H SEMANTIC JOIN CONDITIONS**
- English and Chinese are normative peers.

## 1. H decision / H 决议

H accepts D's RecoveryJoin 1.0.2 generic membership-proof P0 crosswalk and the H Unified 1.2.14 D-specific high-water structure. The exact D high-water field is:

`ownerSpecificHighWatersD.forget_fence_generation_high_water`

It is distinct from `owner_gate_generation` and `barrier_generation`. The D proof remains a closed generic RecoveryJoin object; D-specific semantics are bound by the exact D row/ForgetOperation digest and signed owner snapshot/attestation, not by extra untyped fields.

H 接受 D 的 RecoveryJoin 1.0.2 通用 Membership Proof P0 Crosswalk 和 H Unified 1.2.14 D 专属 High-Water 结构。精确 D High-Water 字段为 `ownerSpecificHighWatersD.forget_fence_generation_high_water`，与 Gate Generation、Barrier Generation 不同。D Proof 仍是封闭通用 RecoveryJoin 对象；D 专属语义由精确 D Row/ForgetOperation Digest 和签名 Owner Snapshot/Attestation 绑定，不通过额外未类型化字段扩展。

## 2. Required H semantic join / H 必须执行的语义 Join

For each D owner snapshot represented in the unified batch and RecoveryJoin:
1. Resolve the same D OwnerAuthorityRef and SnapshotRef.
2. Require exact equality of SnapshotDigest and SnapshotAttestationRef/Digest between the unified ownerSnapshot summary and the D membership proof.
3. Recompute `owner_specific_high_waters_digest` from the exact D-specific high-water object, including `forget_fence_generation_high_water`.
4. Verify the D snapshot attestation commits to the same D-specific high-water vector and exact D ledger root.
5. Verify every included D ForgetFence row digest and ensure its ForgetFenceGeneration is at or below the captured D high-water in the same D namespace.
6. Verify the RecoveryJoin generic proof P0 binds the same owner snapshot ref/digest, owner ledger root, owner admission/entry digest and anti-rollback anchor.
7. Do not infer D completeness from H/COC counts, COC prefix, or another owner's high-water.

对于每个进入 Unified Batch/RecoveryJoin 的 D Owner Snapshot，H 必须 Join 相同 D Authority/SnapshotRef，校验 SnapshotDigest 和 Attestation Ref/Digest 一致，重算包含 `forget_fence_generation_high_water` 的 D High-Water Digest，验证 D Attestation 与 Ledger Root，并验证每个 D Fence Row 的 Generation 不超过同 Namespace 的快照 High-Water。RecoveryJoin 通用 P0 必须绑定相同 Snapshot/Ledger/Admission/Entry Digest/Anti-rollback。H 不得从 COC Count/Prefix 或其他 Owner High-Water 推断 D 完整性。

## 3. Type and namespace constraints / 类型与 Namespace 约束

- D ForgetFenceGeneration is an opaque D-local monotonic value.
- D owner gate generation is an independent D gate generation.
- D barrier generation/root identifies the dependency/barrier snapshot.
- COC term/index, I PermissionEpoch, C record/event sequence and Storage transaction/GID identifiers are not comparable to any of the above.
- The generic RecoveryJoin schema remains closed. The D-specific high-water vector is carried only in the H 1.2.14 owner-specific summary and bound by D's signed snapshot/attestation.

## 4. L3 reference obligations / L3 参考义务

H requires reference-model tests for:
- missing/changed D high-water field;
- high-water digest mismatch;
- owner snapshot ref/digest mismatch;
- attestation ref/digest mismatch;
- D row with ForgetFenceGeneration above snapshot high-water;
- gate generation or barrier generation substituted for fence high-water;
- same snapshot ref but different D ledger root;
- incomplete D pagination or unavailable D verifier -> UNKNOWN;
- D-only field injected into closed generic RecoveryJoin proof -> INVALID.

## 5. Final H disposition / H 最终结论

**ACCEPT D P0/CROSSWALK AS L1/L2 CANDIDATE WITH H SEMANTIC JOIN CONDITIONS.**

H accepts the exact D crosswalk and H 1.2.14 schema candidate. The H semantic join rules above are normative. This is not evidence of live D ledger completeness, production semantic validator, actual owner release, physical Storage integration or production Forget completion.

**接受 D P0/Crosswalk 作为 L1/L2 候选，并附 H Semantic Join 条件。** H 接受精确 D Crosswalk 与 H 1.2.14 Schema 候选。上述 H Semantic Join 规则为规范要求；不证明实时 D Ledger 完整性、生产 Semantic Validator、真实 Owner Release、物理 Storage 集成或生产 Forget 完成。
