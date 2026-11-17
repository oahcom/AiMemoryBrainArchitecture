# Phase 3.8.14 — H Exact Review of I P0 3.8.9 under Unified 1.2.14 / RecoveryJoin 1.0.2
# Phase 3.8.14 — H 对 I P0 3.8.9 在 Unified 1.2.14 / RecoveryJoin 1.0.2 下的精确审查

- Reviewer: H — BMCP Protocol / Schema / Interoperability
- Branch: `session-h-bmcp-protocol`
- Exact H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- Exact H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- Exact I P0 allowlists: Blob `5c0e2049513d391dfc118f4f629a5ec95de456d6`
- Exact I owner snapshot membership proof contract: Blob `88209bbea0ab600880c5c630cfe83af31ee16dd7`
- Exact I compatibility review: Blob `c400b66639b810a9437c1b52993a2015473622d6`
- Exact D high-water review: Blob `6d45398885a842b0e5effc860bc97d7ecd3a8435`
- Decision: **ACCEPT I P0 / RECOVERYJOIN 1.0.2 COMPATIBILITY FOR H 1.2.14; L3 VECTORS OPEN**
- English and Chinese are normative peers.

## 1. H decision / H 决议

H accepts I's Phase 3.8.9 exact P0 allowlists and owner snapshot membership proof under H Unified 1.2.14 and RecoveryJoin 1.0.2.

The exact H common-envelope field `schema_artifact_revision` is signed and MUST equal 1.2.14. I's P0 allowlist already includes this field; this review confirms its value binding. H 1.2.14's additional D `forget_fence_generation_high_water` is D-owned and does not enter I's owner-specific P0.

H 接受 I Phase 3.8.9 精确 P0 白名单和 Owner Snapshot Membership Proof 在 H Unified 1.2.14 / RecoveryJoin 1.0.2 下兼容。

H Common Envelope 的 `schema_artifact_revision` 是签名字段，必须等于 1.2.14。I P0 白名单已包含该字段；本审查确认其精确值绑定。H 1.2.14 新增的 D `forget_fence_generation_high_water` 属于 D，不进入 I Owner-Specific P0。

## 2. Required semantic verification / 必须执行的语义验证

- Verify exact I P0 family projection and profile IDs; the H structural schema alone is insufficient.
- Resolve I owner authority, issuer, key ID/version, historical status and anti-rollback through I's authoritative trust boundary.
- Verify I owner snapshot attestation and each RecoveryJoin membership proof as distinct signed objects.
- Join I owner snapshot ref/digest, attestation ref/digest, owner ledger root, request/admission counts/roots/high-waters, I-specific high-water digest, gate/scope generation and anti-rollback anchor.
- Enforce exact `schema_artifact_revision=1.2.14`; wire `schema_version=1.3.0` does not replace it.
- Do not map D's ForgetFenceGeneration into I receipt/consume high-waters, PermissionEpoch or InventoryEpoch.
- Keep COC quorum evidence independent from I owner signature projection.

## 3. H/RecoveryJoin owner proof cross-schema join / H/RecoveryJoin 跨 Schema Owner Proof Join

H Unified ownerSnapshot and RecoveryJoin 1.0.2 ownerSnapshot are distinct carrier objects. H must join them by exact owner authority and snapshot ref/digest; the RecoveryJoin ownerSnapshotMembershipProof then binds the exact owner entry/admission, sequence, ledger root, snapshot digest, attestation ref/digest and anti-rollback. No count-only or root-only inference is accepted.

H Unified ownerSnapshot 与 RecoveryJoin 1.0.2 ownerSnapshot 是不同载体对象。H 必须通过精确 Owner Authority 和 Snapshot Ref/Digest 将它们 Join；RecoveryJoin Membership Proof 再绑定精确 Owner Entry/Admission、Sequence、Ledger Root、Snapshot Digest、Attestation Ref/Digest 和 Anti-rollback。禁止仅凭 Count 或 Root 推断。

## 4. L3 obligations / L3 义务

H requires exact independent vectors for each I BMCP message family and standalone proof object, including H 1.2.14 artifact revision, P0 digest/preimage, snapshot/attestation mismatch, owner-entry mismatch, incomplete pagination, empty proof/count mismatch, stale key status, historical checkpoint absence and anti-rollback failure.

The previous 101/101 I-profile run is bounded and does not close these per-family vectors. Missing I authority callback remains UNKNOWN/fail-closed.

## 5. Final H disposition / H 最终结论

**ACCEPT I P0 / RECOVERYJOIN 1.0.2 COMPATIBILITY FOR H 1.2.14; L3 VECTORS OPEN.**

This is an architecture/contract compatibility decision only. It does not approve production trust root/profile registration, HSM/KMS, live key registry, owner ledger implementation, physical restore, or production Global Forget.

**接受 I P0 / RecoveryJoin 1.0.2 与 H 1.2.14 兼容；L3 向量仍 OPEN。** 这只是架构/合同兼容决策，不批准生产 Trust Root/Profile 注册、HSM/KMS、实时 Key Registry、Owner Ledger 实现、物理 Restore 或生产 Global Forget。
