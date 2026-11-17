# Phase 3.6.14 — I Exact Review of Storage v3.2.4 Successor Manifest
# Phase 3.6.14 — I 对 Storage v3.2.4 后继清单的精确审查

- Reviewer role: I — Security, Identity and Governance
- Exact reviewed manifest Blob: `6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7`
- Manifest path: `reviews/storage-consistency/phase-3.6.14-storage-v3.2.4-successor-exact-version-binding-manifest.md`
- Decision: **ACCEPT STORAGE ORDERING AS A CANDIDATE; OWNER-PROOF VERSION MIGRATION REQUIRED; FREEZE NOT APPROVED**
- Provenance: coordinator-authored I-role simulation at user's direction; NOT an independent human I Owner signature.

## 1. I decision / I 决议

I accepts the authority separation and the Storage S0a–S4 candidate ordering as a coherent recovery design: I remains authoritative for PermissionDomain/PolicyDomain request and authorization ledgers, receipt issue/consume, revocation order, ProducerDomain inventory, TargetInventorySeal, I membership proof P0, key status, anti-rollback and I-local release CAS. Storage/COC may preserve and join I evidence but cannot mint, reinterpret or release I authority.

I 接受 Storage S0a–S4 候选顺序及权限边界：I 继续独占 PolicyDomain 请求与授权账本、Receipt 签发/消费、撤销顺序、ProducerDomain Inventory、TargetInventorySeal、I Membership Proof P0、Key Status、Anti-Rollback 和 I 本地 Release CAS。Storage/COC 只能持久化和关联 I 证据，不能代替 I 签发或释放权限。

## 2. Exact-version findings / 精确版本发现

The manifest correctly binds:
- I R1/R2 candidate Blob `57ef6c4352d79577ae53a77895f73bce434c5fca`;
- I owner-local gate amendment Blob `0d0b4fb0f5921e63b6ebfd70b62afa31d3d5fdf7`;
- I authorization sequencer contract Blob `54bab0484bd232a5a258e65e34cc7425288b39a6`;
- I membership proof contract Blob `88209bbea0ab600880c5c630cfe83af31ee16dd7`;
- H Unified 1.2.12 Blob `a54f66914a819d77f00c6af04e76453ff9f654ee`;
- H RecoveryJoin 1.0.2 Blob `4b664e3bce465499bcdfd93796349a4ba7074002`.

Currentness readback confirmed the I source Blob IDs listed above still match the exact files on the I branch at review time.

## 3. Blocking I amendment / I 阻断修订

I membership proof contract Blob `88209bbea0ab600880c5c630cfe83af31ee16dd7` explicitly states that it applies to H Unified Manifest **1.2.11**. The successor manifest binds H Unified **1.2.12**. The I proof contract must not be silently assumed compatible with 1.2.12.

Required I action:
1. Publish an I-owned bilingual amendment that explicitly adopts or rejects the 1.2.12 RecoveryJoin/unified mapping.
2. Pin the exact H schema and RecoveryJoin fields that carry I proof ref/digest and the exact owner authority payload.
3. Preserve I's P0, digest preimage, signature profile, issuer/audience/purpose, key-status and anti-rollback semantics; H must not change I's signed projection.
4. Specify UNKNOWN behavior for missing verifier, incomplete pagination, stale key status and unavailable anti-rollback.
5. Add negative vectors for old-version payload, missing proof, mismatched proof digest, high-water overflow and scope mismatch.

Required I proof completeness remains distinct from per-row membership: query identity, complete pagination, count, canonical set digest/root and high-water are required. A valid row proof alone cannot prove the complete I set.

## 4. R1/R2 and release invariants / R1/R2 与 Release 不变量

I request acceptance, authorization admission, receipt issuance/consumption and revocation must share I's durable serialization boundary. The frozen I snapshot must bind PolicyDomain/scope, GateGeneration, ScopeVersion, request high-water, in-flight admission high-water, roots/counts, anti-rollback anchor and key-status generation. Any changed currentness value invalidates release and requires a successor cutoff round. I counters are never compared numerically with D/C/COC counters.

I release remains a fresh I-local CAS after exact Batch/Manifest readback. COC completion is not I release. No stale token or wall-clock ordering substitutes for I's authoritative terminal receipt.

## 5. Disposition / 处理结论

- Storage S0a–S4 composition: **ACCEPT AS CANDIDATE**.
- I authority boundary and I-only release: **ACCEPT**.
- I proof applicability to H 1.2.12: **NEEDS I AMENDMENT**.
- Joint freeze of manifest: **NOT APPROVED**.
- Production sequencer, key registry, anti-rollback adapter and executable race tests: **NOT VERIFIED**.

This is not an independent I Owner approval and must not be represented as one.
