# Phase 3.8.12 — I Exact Compatibility Review: H Unified 1.2.14 / RecoveryJoin 1.0.2
# Phase 3.8.12 — I 精确兼容性审查：H Unified 1.2.14 / RecoveryJoin 1.0.2

- Owner: I — Security, Identity and Governance
- Branch: `session-i-security-governance-2026-11-16`
- Exact I P0 allowlists: Phase 3.8.9, Blob `5c0e2049513d391dfc118f4f629a5ec95de456d6`
- Exact I owner snapshot membership proof contract: Blob `88209bbea0ab600880c5c630cfe83af31ee16dd7`
- Exact H Unified schema 1.2.14: Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- Exact H RecoveryJoin schema 1.0.2: Blob `4b664e3bce465499bcdfd93796349a4ba7074002`
- H D high-water review: Phase 3.8.13 (pending H readback)
- Decision: **ACCEPT AS I P0 / RECOVERYJOIN 1.0.2 COMPATIBLE SUCCESSOR; I AUTHORITY UNCHANGED**
- Provenance: delegated I-role technical review; not independent human I Owner or governance approval.
- English and Chinese are normative peers.

## 1. Exact compatibility decision / 精确兼容性决议

I accepts H Unified 1.2.14 and RecoveryJoin 1.0.2 as compatible successor carriers for I's Phase 3.8.9 exact P0 and owner snapshot membership proof contract.

H 1.2.14 changes the common-envelope artifact revision to 1.2.14 and adds the D-owned `forget_fence_generation_high_water` to the D-specific high-water object. The I common P0 already includes `schema_artifact_revision`; the exact value for this schema is 1.2.14. The D-only field is not an I field and does not enter I's owner-specific P0.

I 接受 H Unified 1.2.14 / RecoveryJoin 1.0.2 与 I Phase 3.8.9 精确 P0 和 Owner Snapshot Membership Proof 合同兼容。H 1.2.14 将 Common Envelope Artifact Revision 更新为 1.2.14，并在 D 专属 High-Water 中增加 `forget_fence_generation_high_water`。I Common P0 已包含 `schema_artifact_revision`，本 Schema 的精确值为 1.2.14。D-only 字段不是 I 字段，不进入 I 的 Owner-Specific P0。

## 2. I proof fields unchanged / I Proof 字段保持不变

The following I-owned values and proof families remain unchanged:
- I PolicyDomain and PermissionEpoch;
- I owner request/admission ledgers, high-waters and roots;
- I owner-specific high-water vector (receipt issue/consume, inventory epoch, registry snapshot and relevant-entry root);
- I OwnerSnapshotRef/Digest and I-signed snapshot attestation ref/digest;
- I OwnerSnapshotMembershipProof generic RecoveryJoin 1.0.2 P0;
- ICompleteEmptyProof and IOutOfScopeProof;
- ICommitAuthorizationReceipt and ITerminalProof;
- I key-status generation, historical checkpoint and anti-rollback anchor.

H's generic RecoveryJoin membership proof remains closed. I proof P0 uses the exact I owner row/snapshot/attestation and profile/key fields; it does not append D-specific fields to the generic proof object.

## 3. Required cross-owner join / 必需跨 Owner Join

1. H Unified I `owner_specific_high_waters_digest` must equal the digest of the exact I-signed owner-specific high-water vector.
2. I owner snapshot attestation ref/digest must resolve to the same snapshot ref/digest and exact I owner ledger root.
3. I RecoveryJoin membership proof must bind the same I owner authority, owner entry/admission digest, local sequence namespace/value, high-water/root, snapshot/attestation, scope/generation and anti-rollback anchor.
4. H must not substitute D `forget_fence_generation_high_water` for I receipt/consume high-waters, PermissionEpoch or InventoryEpoch.
5. If the H common envelope schema artifact revision is not exactly 1.2.14, reject; schema_version 1.3.0 alone is not sufficient.
6. Missing I verifier, incomplete I pagination, stale key status, missing historical checkpoint or unavailable anti-rollback remains UNKNOWN and blocks dependent completion.

## 4. L3 reference obligations / L3 参考义务

- I P0 reconstruction with `schema_artifact_revision=1.2.14`;
- H owner-specific high-water digest mismatch;
- I snapshot/attestation ref/digest mismatch;
- D high-water substituted into I high-water vector;
- I RecoveryJoin proof row/entry/sequence mismatch;
- incomplete pagination or stale I high-water;
- I key status/history/anti-rollback unavailable;
- cross-namespace numeric comparison attempt.

The earlier 101/101 generic I-profile candidate run does not prove all Phase 3.8.9 per-family P0 vectors. L3 remains OPEN.

## 5. Final I disposition / I 最终结论

**ACCEPT AS I P0 / RECOVERYJOIN 1.0.2 COMPATIBLE SUCCESSOR; I AUTHORITY UNCHANGED.**

I accepts H Unified 1.2.14 and RecoveryJoin 1.0.2 as compatible carriers for the I proof contract. This does not approve production trust root, profile registration, key custody, HSM/KMS, live key-status ledger, external anti-rollback service, runtime owner enumeration or production Global Forget.

**接受为 I P0 / RecoveryJoin 1.0.2 兼容后继；I 权威不变。** 不代表生产 Trust Root、Profile 注册、Key Custody、HSM/KMS、实时 Key Status Ledger、外部 Anti-rollback、Runtime Owner Enumeration 或生产 Global Forget 已批准。
