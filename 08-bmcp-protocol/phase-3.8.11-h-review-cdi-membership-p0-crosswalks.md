# Phase 3.8.11 — H Cross-Review of C/D/I Membership P0 Crosswalks
# Phase 3.8.11 — H 对 C/D/I Membership P0 Crosswalk 的交叉复审

- Reviewer: H — BMCP Protocol and Interoperability
- H Unified schema 1.2.14 Blob: `fee452efb99ab4fe0ceccb347c46eeef1521bd28`
- H RecoveryJoin schema 1.0.2 Blob: `4b664e3bce465499bcdfd93796349a4ba7074002`
- C Phase 3.8.13 membership P0 crosswalk Blob: `df12af95e6859a389ba71eb1b7dba512b9feb8f6`
- D Phase 3.8.6 membership P0 crosswalk Blob: `c4adf827dd62d44c43b8e871dec4835581508adf`
- I Phase 3.8.10 P0 successor Blob: `35e6843da8becbf3b152512a561b05cf5486819b`
- CSubmitOutcome 1.0.1 schema Blob: `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`
- H Provider Outcome mapping Phase 3.8.10 Blob: `7739d8159b32702024583669f40974a80801782b`
- Status: **ACCEPT AS L1/L2 GENERIC-ENVELOPE + OWNER-DIGEST MAPPING CANDIDATE; L3 PROOFS OPEN**
- Provenance: delegated H-role cross-review; **not independent human C/D/H/I Owner signatures**.

## 1. Exact schema shape / 精确 Schema 形状

H RecoveryJoin 1.0.2 `ownerSnapshotMembershipProof` is a closed generic object with `additionalProperties=false`. It is not a union of arbitrary owner-specific inline properties. The accepted C/D/I mapping therefore keeps one exact generic P0 and requires owner-specific facts to be committed by the referenced owner entry, operation, scope and snapshot digests. No untyped extra property is allowed.

H RecoveryJoin 1.0.2 的 `ownerSnapshotMembershipProof` 是 `additionalProperties=false` 的封闭通用对象，不是任意 Owner 专属字段的 Union。因此本次接受 C/D/I 映射统一使用一个精确通用 P0，由 Owner Entry、Operation、Scope 和 Snapshot Digest 承诺 Owner 专属事实；不允许增加未定义字段。

## 2. C mapping / C 映射

H accepts C's generic envelope mapping with the following exact joins:
- `owner_kind=C`, C authority and owner ledger/version;
- `owner_entry_ref/digest` resolves the exact C row; for a Provider Outcome row it resolves CSubmitOutcome 1.0.1 `record_ref/payload_digest`;
- `owner_admission_ref` equals C `CAdmissionRef`;
- `owner_sequence_namespace` equals signed C `sequence_namespace_ref`; owner-local sequence and high-water remain C-owned;
- `owner_gate_ref/generation` equals C `CGateRef/CGateGeneration`;
- C Adapter/ProviderAccount/Endpoint/Region/ApiOperation/Idempotency/ProviderAttempt/Outcome/Receipt/Lookup/COC intent-reservation semantics are dereferenced from the exact C row and CSubmitOutcome 1.0.1 P0, whose digest is committed by `owner_entry_digest`;
- C high-water summary is the top-level request/admission high-water plus the C reservation/provider-attempt/provider-outcome high-water union.

H accepts C's mapping only if every dereference is exact and immutable. A valid generic proof does not prove provider success; CSubmitOutcome and provider issuer evidence remain independently required.

## 3. D mapping / D 映射

H accepts D's generic envelope mapping with the following exact joins:
- `owner_kind=D`, D BrainAuthority, D ledger/version/entry/admission;
- `operation_identity_ref/digest` resolves the exact D ForgetOperation record;
- `scope_ref/generation/scope_binding_digest` commits target/source/ancestor lineage selector and scope;
- `owner_gate_ref/generation` is D Gate only;
- exact per-row ForgetFenceGeneration and barrier member/dependency data are committed by the D owner entry digest and operation digest;
- H 1.2.14 `ownerSpecificHighWatersD` includes producer-registration, WorkItem, Attempt, Barrier generation/root and `forget_fence_generation_high_water`;
- the D owner snapshot attestation and `owner_specific_high_waters_digest` bind the exact six-field D high-water object.

H expressly confirms three non-aliasing D values: `owner_gate_generation`, `barrier_generation`, and `forget_fence_generation_high_water`. Substitution or cross-domain comparison is INVALID.

## 4. I mapping / I 映射

H accepts I's generic proof P0 as directly matching RecoveryJoin 1.0.2. I's owner-specific high-water object remains its exact five-field shape. I P0 excludes derived `proof_digest` and external `signature_ref`; the signature projection is P0 plus proof_digest. H 1.2.14's common `schema_artifact_revision` is included in I signed common-envelope P0.

## 5. L3 obligations / L3 证明义务

The following are required before L3 closure:
1. C, D and I independent canonical P0 vectors and at least two independent implementations per owner family.
2. Exact owner-entry dereference tests proving every owner-specific semantic field is included in the canonical entry digest; mutation of any field must invalidate the digest/join.
3. C Provider Outcome 1.0.1 digest/sequence namespace/COC reservation/receipt negative vectors.
4. D ForgetFenceGeneration stale-high-water, barrier-generation substitution, late discovery, dependency-closure and target/source/ancestor scope mutation vectors.
5. I attestation/high-water/owner membership, key-status, anti-rollback and signature_ref resolution vectors.
6. Missing owner ledger, snapshot, pagination, verifier, key status or anti-rollback evidence returns UNKNOWN, never VALID/COMPLETE.
7. Independent human Owner signatures and exact currentness re-read before any freeze.

## 6. Current exact review set / 当前精确复审集合

The D crosswalk pin in this review is the current D Phase 3.8.6 Blob `c4adf827dd62d44c43b8e871dec4835581508adf`; D's current exact H 1.2.14 review is separately pinned by the system manifest. H Provider Outcome mapping is current Blob `7739d8159b32702024583669f40974a80801782b`.

## 7. H disposition / H 侧结论

**ACCEPT AS L1/L2 GENERIC-ENVELOPE + OWNER-DIGEST MAPPING CANDIDATE; L3 PROOFS OPEN.**

This closes ARC-11 at the design-contract level by defining the no-loss dereference mapping for C/D/I. It does not claim executable P0 vectors, real owner-ledger completeness, provider truth, D Forget completion, I authorization victory, COC quorum durability, JF-10 closure or production readiness. H does not mint or replace C/D/I owner facts.

**ACCEPT 作为 L1/L2 通用 Envelope + Owner Digest 映射候选；L3 证明仍 OPEN。** 本复审在设计合同层关闭 ARC-11，明确 C/D/I 专属字段的无损解引用映射；不代表 P0 可执行向量、真实 Owner Ledger 完整性、Provider Truth、D Forget Completion、I Authorization Victory、COC Quorum 持久性、JF-10 关闭或生产就绪。H 不签发或替代 C/D/I Owner 事实。

This is a delegated H-role technical cross-review, not an independent human Owner signature or system-level approval.
