# Phase 3.8.4 — I Exact-Version Review of H Unified Manifest 1.2.11
# Phase 3.8.4 — I 对 H Unified Manifest 1.2.11 的精确版本审查

- Reviewer: I — Security, Identity and Governance Architect
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Provenance: delegated I-role simulation in the coordinating session; not an independent human I Owner signature or cryptographic attestation.
- Scope: I-signed P0 mapping, I owner snapshot/ledger proof references, artifact/wire version binding and owner release digest binding.
- Status: architecture / cryptographic profile candidate only; NOT FROZEN / NOT PRODUCTION-APPROVED.

## 1. Exact reviewed bundle / 精确审查组合

| Artifact | Exact Blob / Evidence |
|---|---|
| H Unified Schema 1.2.11, wire 1.3.0 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H I crypto wire mapping 3.8.4 | `bf160288d7529b37ad1b56924c1583748922aa25` |
| I crypto profile proposal | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` |
| I artifact-revision/digest amendment | `00e3fa5e8cfbaa99b163dc3a550167e5f71e0e4a` |
| I P0 vector set | `4657f0c81e9c8692d29ac183380f3d7e074a4e4c` |
| I Python/Node crypto test | `7658edc6f51dac203742ecc1ecf00d41bd676908` |
| H semantic reference module | `4a7c22ed15dff0a688559f79e4facbffca6527cd` |
| H semantic/schema test file | `c95bea3d7a7bee5f419bfabe914ea56be79fc8ad` |
| H RecoveryJoin schema 1.0.1 | `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c` |
| H candidate CI | Run `44048157932`, commit `05812faf5cfd4360803d660ebf5ffb8d48cba6b1`, 209 tests PASS |

## 2. I accepted findings / I 接受的设计

1. The unified common envelope distinguishes and requires `schema_artifact_revision=1.2.11` and `schema_version=1.3.0`. Both are included in the three I-signed Unified Schema P0 vectors. A receiver must reject artifact/version disagreement and downgrade.
2. `OWNER_LOCAL_GATE_RELEASE` uses `OUTAGE_ADMISSION_RELEASE_ONLY`, matching the I/D/C owner-local gate semantics.
3. The I Gate Release P0 separates `manifest_content_digest` from `manifest_record_entry_digest`, and separates `batch_digest` from `batch_entry_digest`. These are not aliases.
4. The owner snapshot requires an attestation digest and an owner-specific high-water digest. Owner admission bindings require immutable membership-proof ref and digest.
5. `signature_profile_id` may remain structurally optional for explicitly non-protected compatibility messages, but it is mandatory semantically for protected I-signed records.
6. H owns schema and wire validation; I remains sole authority for I issuer trust, profile/key status, signature verification policy, PermissionEpoch, ProducerDomainInventoryEpoch, TargetInventorySeal and I Gate Release.

## 3. I conditions / I 保留条件

1. **I membership-proof contract is still missing.** I must publish the exact I OwnerSnapshotMembershipProof schema, issuer/subject/audience/purpose, signed P0 projection, digest preimage, ledger inclusion proof format, high-water inclusion rule, key status and anti-rollback validation. H's generic ref/digest fields are necessary but do not constitute an I proof.
2. The proof must bind the exact I owner ledger ref/version, entry ref/digest, owner-local sequence namespace/value, captured admission high-water, owner snapshot ref/digest/attestation digest, ledger root, operation digest and scope binding. No cross-owner numeric comparison is permitted.
3. The 209-test H run validates schema structure, normalized semantic fixtures and cross-language TEST vectors. It does not validate a live I ledger, I signature, production trust registry, historical key verification, revocation or anti-rollback service.
4. The Python/Node Ed25519 vectors use a deterministic TEST-ONLY seed. I has not approved production Ed25519 suitability, HSM/KMS custody, trust-root ceremony, key lifecycle, algorithm agility or regulatory constraints.
5. RecoveryJoin 1.0.1 remains a separate artifact. Its nested `completeEmptyProof` and `outOfScopeProof` field projections are accepted only under the exact pinned schema and H field map; any RecoveryJoin schema revision requires a new exact review.
6. I Gate Release remains a final I-sequencer currentness CAS over PermissionEpoch, IGateGeneration, inventory epoch/registry digest, TargetInventorySeal, current signer/key status and exact Batch/Manifest roots. The schema cannot prove that the live CAS ran.
7. No I release may be inferred from a COC completion observation, Storage receipt, timeout or a D/C release.

## 4. Decision / 决议

I accepts the H 1.2.11 schema and P0 mapping as a candidate with the conditions above. This does not approve the I production cryptographic profile, close I R1/R2, establish owner-ledger conformance, close JF-10 P0, approve Multi-PolicyDomain atomicity or authorize production activation.

**ACCEPT WITH ENUMERATED AMENDMENTS** — candidate only.

I 接受 H 1.2.11 Schema 与 P0 Mapping 作为候选方案，但须满足上述条件。本决议不批准 I 生产密码学 Profile，不关闭 I R1/R2，不证明 Owner Ledger Conformance，不关闭 JF-10 P0，不批准 Multi-PolicyDomain Atomicity，也不授权生产激活。

**ACCEPT WITH ENUMERATED AMENDMENTS** — 仅限候选方案。
