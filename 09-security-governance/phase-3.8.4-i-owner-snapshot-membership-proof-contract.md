# Phase 3.8.4 — I Owner Snapshot Membership Proof Contract
# Phase 3.8.4 — I Owner Snapshot Membership Proof 合同

- Owner: I — Security, Identity and Governance
- Status: **PROPOSED / CANDIDATE ONLY — NOT APPROVED OR FROZEN**
- Applies to: I-owned rows represented in H Unified Manifest 1.2.11 / wire 1.3.0.
- Normative language: MUST / MUST NOT / UNKNOWN.

## 1. Authority boundary

I is the sole authority for I PolicyDomain request/admission ledgers, I receipt issue/consume events, I owner snapshots, I membership proofs, I issuer/key status and I anti-rollback anchors. H transports and structurally validates the proof; H does not decide I ledger completeness or key trust. D/C proofs remain D/C-owned.

## 2. Proof identity and exact binding

Every I row represented as either an `owner_admission_binding` within a `COC_PARTICIPANT` or an `OWNER_LOCAL_ADMISSION` MUST have one immutable `IAdmissionSnapshotMembershipProof`. The proof MUST bind, without aliases:

- `proof_ref`, `owner_kind=I`, I PolicyDomain authority ref;
- exact I ledger ref/version, exact entry ref and entry digest;
- exact I OwnerAdmissionRef, owner-local sequence namespace and sequence;
- captured I admission high-water and admission ledger root;
- immutable I snapshot ref/digest and signed snapshot-attestation ref/digest;
- exact I Gate ref/generation and PolicyDomain/scope binding digest;
- operation identity ref/digest and request digest;
- independent I anti-rollback anchor ref and key-status generation;
- issuer, subject, audience, purpose, signature profile, key ID/version and signature ref.

The sequence is compared only inside its I-owned namespace. No comparison to D/C sequence or COC index is permitted.

## 3. Membership and completeness semantics

The I proof attests that the exact ledger row is included in the exact immutable signed snapshot, that the row sequence is at or below the captured I admission high-water, and that the snapshot root/count/set digest were computed over the complete applicable I admission query for the declared PolicyDomain and scope.

A valid row-membership proof does not by itself prove the entire I set is complete. Completeness additionally requires the signed snapshot attestation, exact query identity, pagination-complete evidence, count, canonical set digest/root and high-water. Empty I sets require the separate RecoveryJoin COMPLETE_EMPTY proof; zero count or empty array alone is not proof.

## 4. Signature projection

I defines and owns the canonical proof P0, digest preimage and signature profile. The P0 MUST include every identity, ledger, entry, sequence/high-water, snapshot, attestation, root, scope, operation, request, gate-generation, anti-rollback, key-status, issuer/subject/audience/purpose field listed above. It excludes only the signature bytes/ref and derived digest fields explicitly enumerated by the I profile. No H or Storage field may be silently added or removed from the I projection.

The proof digest is SHA-256 over the I-approved canonical proof payload. Signature verification checks the exact I key version and key-status generation, issuer authorization, audience, purpose, scope and anti-rollback anchor. Revoked, unknown, stale, rolled-back or unverifiable key state yields UNKNOWN and blocks I Gate Release.

## 5. Release use

I Gate Release MUST validate every I membership proof referenced by the canonical union Manifest and reconcile it against the exact frozen I snapshot. Any missing row, duplicate, unexpected row, root mismatch, high-water mismatch, incomplete page, stale key status or changed currentness CAS blocks release. I may not attest D/C rows.

## 6. Failure semantics and retention

Proofs are immutable and append-only. Late evidence creates a successor proof or reconciliation record; it never rewrites an old proof. Missing ledger, partial query, stale replica, unavailable anti-rollback checkpoint, uncertain ordering or failed signature returns UNKNOWN. No timeout, absent COC participant or zero count may be converted into an empty-set proof.

## 7. Decision boundary

This contract is an I-role proposal in the coordinating session, not independent human I Owner approval. Production algorithm/regulatory suitability, trust-root ceremony, HSM/KMS, key rotation, compromise response, external anti-rollback and durable PolicyDomain sequencer conformance remain open. I exact review of H 1.2.11 is limited to the wire fields and semantic obligations above; it does not freeze production cryptography.


## 8. Concrete I P0 projection / I P0 具体投影

The I membership proof P0 is the exact RecoveryJoin 1.0.2 `ownerSnapshotMembershipProof` payload identity excluding only the derived `proof_digest` and external `signature_ref`. The digest field is `proof_digest`; the signed projection is P0 plus that derived digest. The signature preimage is governed by the I crypto profile and domain-separated by message type `I_ADMISSION_SNAPSHOT_MEMBERSHIP_PROOF`.

The P0 includes all of:
`proof_ref`, `owner_kind`, `owner_authority_ref`, `issuer_ref`, `subject_ref`, `audience_ref`, `purpose`, `owner_ledger_ref`, `owner_ledger_version`, `owner_entry_ref`, `owner_entry_digest`, `owner_admission_ref`, `owner_sequence_namespace`, `owner_local_sequence`, `owner_high_water`, `owner_ledger_root`, `owner_snapshot_ref`, `owner_snapshot_digest`, `owner_snapshot_attestation_ref`, `owner_snapshot_attestation_digest`, `owner_gate_ref`, `owner_gate_generation`, `scope_ref`, `scope_generation`, `scope_binding_digest`, `operation_identity_ref`, `operation_digest`, `request_digest`, `anti_rollback_anchor_ref`, `key_status_generation`, `signature_profile_ref`, `key_id`, `key_version`, `canonicalization_profile_ref`, and `digest_profile_ref`.

The TEST-ONLY cross-language vector is in H vector Blob `9210219a85afe1f48da0ea253a073aba8b2e138c`; the Python/Node test source is Blob `01239e06e8f4464f49acd34241dc00899befe424`. This vector proves only Python/Node agreement for this fixed test proof. Production I signing, key trust, ledger membership and completeness remain unimplemented.


## 9. H Unified 1.2.16 I snapshot field mapping — CANDIDATE / OWNER DECISION REQUIRED

H Unified 1.2.16 introduces I-specific snapshot high-waters:
- `permission_epoch`
- `producer_domain_inventory_epoch_ref`
- `receipt_issue_high_water`
- `receipt_consume_high_water`
- `registry_snapshot_digest`
- `relevant_entry_set_root`

The first two fields map to distinct I authorities:
1. `permission_epoch` is the opaque I-local PermissionEpoch for the exact PolicyDomainRef; it is not the producer inventory epoch, request high-water, admission high-water or a COC/D/Storage position.
2. `producer_domain_inventory_epoch_ref` identifies the exact I-issued ProducerDomainInventoryEpoch for the frozen PolicyDomain and declared scope/environment/jurisdiction inventory boundary. It is not inferred from I request/admission sequence.

Both fields MUST be included in the I-signed owner snapshot attestation P0 and in the canonical `owner_specific_high_waters_digest`. The snapshot attestation must bind the exact ScopeGeneration separately from OwnerGateGeneration. The I owner-specific high-water object remains closed-world.

H schema 1.2.16 exact Blob `91c4fd70cb1e1cff76d733baa180325bd2da84c1` corrected an initial conditional alias defect: the Owner=I condition now requires `producer_domain_inventory_epoch_ref`, not legacy `inventory_epoch_ref`. Its concrete I/D/C snapshot-instance tests are in Blob `e1667b0f9526884c56c311bf1bcf8af6af0b9477`; exact H Recovery Cutoff run #44192602325 passed 356 tests (22 skipped).

H Unified 1.2.17 semantic reference validator/test Blobs are `60cd1b686eaa9ac364c69a708353fa0e5f635197` / `24d3cf0730a138f25719cb1e29de28f833a00cdf`; exact code Head `f08dadd27b743b2a31fce859d6ed2c438438d1e1` passed H suite run #44193331446 (390 tests, 22 skipped). It binds the exact I snapshot across Batch and Manifest roots but uses injected signature/COC/currentness callbacks.

**I candidate disposition:** the field meanings are consistent with I's existing PermissionEpoch and ProducerDomainInventoryEpoch authority contracts. The exact 1.2.16 P0 projection, signature preimage, source-ledger adapter and currentness/anti-rollback semantics still require an I-owned amendment and explicit authorized I Owner approval. This append is a delegated I-role candidate, not an independent human I Owner signature; no I36 governance gate is passed.

### 中文：H Unified 1.2.16 I Snapshot 字段映射 — 候选 / 需 Owner 决策

H Unified 1.2.16 新增 I 专属 Snapshot High-water：`permission_epoch`、`producer_domain_inventory_epoch_ref`、`receipt_issue_high_water`、`receipt_consume_high_water`、`registry_snapshot_digest`、`relevant_entry_set_root`。

其中：
1. `permission_epoch` 是精确 PolicyDomainRef 内的不透明 I-local PermissionEpoch，不等于 Producer Inventory Epoch、Request/Admission High-water 或 COC/D/Storage 位置。
2. `producer_domain_inventory_epoch_ref` 指向 I 签发的精确 ProducerDomainInventoryEpoch，并绑定冻结的 PolicyDomain 与声明的 Scope/Environment/Jurisdiction Inventory Boundary；不得从 I Request/Admission Sequence 推断。

两个字段都必须进入 I 签名 Owner Snapshot Attestation P0 和规范化的 `owner_specific_high_waters_digest`。Snapshot Attestation 还必须将 ScopeGeneration 与 OwnerGateGeneration 分开绑定；I 专属 High-water 对象保持封闭字段集。

H Schema 1.2.16 Blob `91c4fd7...` 已修正最初的条件别名缺陷：Owner=I 条件现要求 `producer_domain_inventory_epoch_ref`，不再要求旧别名 `inventory_epoch_ref`。实例测试 Blob `e1667b0...`；精确 H Run #44192602325 通过 356 项（22 项 skipped）。

H Unified 1.2.17 语义参考 Validator/Test Blob 为 `60cd1b6...` / `24d3cf0...`；精确代码 Head `f08dadd...` 的 H Run #44193331446 通过 390 项（22 项 skipped）。它把同一 I Snapshot 绑定到 Batch 和 Manifest Root，但签名/COC/Currentness 仍是注入 Callback。

**I 候选结论：** 字段语义与 I 既有 PermissionEpoch 和 ProducerDomainInventoryEpoch 权威合同一致；但 1.2.16 精确 P0 Projection、Signature Preimage、Source Ledger Adapter 和 Currentness/Anti-rollback 语义仍需 I 自有修订及授权 I Owner 明确批准。本追加是委派 I 角色候选，不是独立人类 I Owner 签名，也不代表 I36 Governance Gate 通过。
