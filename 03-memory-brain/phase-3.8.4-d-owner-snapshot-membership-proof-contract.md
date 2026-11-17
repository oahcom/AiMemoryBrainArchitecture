# Phase 3.8.4 — D Owner Snapshot Membership Proof Contract
# Phase 3.8.4 — D Owner Snapshot Membership Proof 合同

- Owner: D — Memory Brain / ForgetFence Authority
- Status: **PROPOSED / CANDIDATE ONLY — NOT APPROVED OR FROZEN**
- Applies to D-owned work, attempt, producer-registration, derivative and barrier rows in H Unified Manifest 1.2.11 / wire 1.3.0.

## 1. Authority boundary

D alone attests D producer/work admission, WorkItem/Attempt/Derivative membership, ForgetFence generation, lineage and barrier membership. H may validate typed shape and join references but cannot attest D ledger completeness. I PermissionEpoch/InventoryEpoch and C provider counters remain opaque owner-owned values.

## 2. Proof required for each D row

Every D row represented in a COC participant binding or as an unregistered owner-local admission MUST carry one immutable `DAdmissionSnapshotMembershipProof` binding:

- `proof_ref`, `owner_kind=D`, D BrainAuthorityRef;
- exact D producer/work ledger ref and version, exact row/entry ref and digest;
- exact ProducerRegistrationRef / WorkItemRef / AttemptRef / DerivativeRef / admission ref as applicable;
- D-local sequence namespace/value and captured producer-registration, WorkItem and Attempt high-waters;
- immutable D owner snapshot ref/digest, snapshot-attestation ref/digest and complete D ledger root;
- ForgetOperationRef, target/source/ancestor scope binding digest, D Gate ref/generation and ForgetFenceGeneration;
- operation identity/digest, request digest, barrier generation/root/member identity;
- independent D anti-rollback anchor, key-status generation and D signature-profile/key/version/signature references.

A proof binds the exact D-local namespace and must not compare D counters with I, C or COC positions.

## 3. Membership and completeness

The proof attests exact inclusion of the identified row in the frozen D snapshot and that its D-local sequence is at or below the relevant captured D high-water. The signed snapshot must cover all producer registration, WorkItem, Attempt, derivative and barrier rows capable of affecting the target/source/ancestor lineage, including rows lacking COC registration.

Membership is not completeness. Completeness additionally requires D's authoritative query/projection identity, pagination completion, count, ordered set root, producer registry version/digest, dependency-inventory revision/digest, high-water vector and anti-rollback checkpoint. A late-discovered pre-fence row invalidates the old snapshot and reopens the affected barrier; the successor snapshot must include it. An empty D set requires a separate D-signed COMPLETE_EMPTY proof and cannot be inferred from count=0.

## 4. D signature projection and verification

D owns the proof canonical projection, digest preimage and signing profile. The signed projection includes all fields in §2 plus issuer/subject/audience/purpose, target lineage selector, applicability decision, Gate/Fence generation, snapshot roots and anti-rollback anchor. Only signature bytes/ref and explicitly derived digest fields are excluded.

Verification checks D key status, signature, scope, target lineage, exact snapshot and high-water inclusion. H must not interpret or re-sign D's proof. I/D cross-owner joins use exact typed refs and digests; they never compare numeric counters.

## 5. Gate/recovery semantics

D Gate Release validates every D membership proof in the canonical union Manifest and reconciles it against the same frozen D snapshot. A proof does not mean WorkItem terminality, publication, cancellation or Forget completion. UNKNOWN/IN_DOUBT, late discovery, incomplete dependency closure, changed barrier root, stale FenceGeneration or anti-rollback uncertainty keeps D's barrier/gate closed.

D outage admission release remains `OUTAGE_ADMISSION_RELEASE_ONLY`; it does not clear the effective Forget Fence or authorize C provider egress.

## 6. Decision boundary

This is a D-role proposal in the coordinating session, not independent human D Owner approval. The D proof signer/key lifecycle, durable ledger query, producer/queue/worker/restore reconciliation and executable race/fault tests remain unimplemented/unverified. No physical Storage acceptance or Forget completion is claimed.


## 7. H Unified 1.2.16 D snapshot field mapping — CANDIDATE / OWNER DECISION REQUIRED

H Unified 1.2.16 introduces D-specific snapshot high-waters:
- `forget_fence_generation_high_water`
- `dependency_closure_cursor`
- `dependency_closure_root`
in addition to producer-registration, WorkItem, Attempt and barrier generation/root fields.

Candidate D semantics:
1. `forget_fence_generation_high_water` is the D-authoritative ForgetFenceGeneration high-water captured at the same frozen snapshot boundary. It is distinct from OwnerGateGeneration and BarrierGeneration.
2. `dependency_closure_cursor` is an opaque D-local cursor identifying the exact completed pagination boundary for the applicable producer/work/attempt/derivative dependency-closure query.
3. `dependency_closure_root` commits the complete canonical dependency closure at that cursor, including applicable source/ancestor/target lineage and late-discovery membership. It is not merely a WorkItem count or the barrier root.
4. The three values MUST be covered by the D-signed owner snapshot attestation P0 and the canonical `owner_specific_high_waters_digest`. A cursor/root/high-water mismatch or late-discovered pre-fence dependency invalidates the old snapshot and requires a successor snapshot/barrier reconciliation.

H schema 1.2.16 exact Blob `91c4fd70cb1e1cff76d733baa180325bd2da84c1` and its concrete I/D/C snapshot-instance tests Blob `e1667b0f9526884c56c311bf1bcf8af6af0b9477` passed within H run #44192602325 (356 tests, 22 skipped). H 1.2.17 semantic reference validator/test Blobs `60cd1b686eaa9ac364c69a708353fa0e5f635197` / `24d3cf0730a138f25719cb1e29de28f833a00cdf` bind the exact D snapshot across Batch and Manifest roots; exact H code Head `f08dadd...` passed run #44193331446 (390 tests, 22 skipped).

**D candidate disposition:** these fields align with D's existing ForgetFence, barrier and complete dependency-lineage authority, but the exact cursor pagination semantics, root projection, P0 signature fields and production ledger query remain to be added/approved by D. This append is delegated D-role candidate work, not an independent human D Owner signature. It does not prove Forget completion, barrier release or physical erasure.

### 中文：H Unified 1.2.16 D Snapshot 字段映射 — 候选 / 需 Owner 决策

H Unified 1.2.16 新增 D 专属 Snapshot High-water：`forget_fence_generation_high_water`、`dependency_closure_cursor`、`dependency_closure_root)，并保留 Producer Registration、WorkItem、Attempt 和 Barrier Generation/Root。

候选 D 语义：
1. `forget_fence_generation_high_water` 是同一冻结 Snapshot 边界上的 D 权威 ForgetFenceGeneration High-water，与 OwnerGateGeneration、BarrierGeneration 独立。
2. `dependency_closure_cursor` 是 D-local 不透明 Cursor，标识适用 Producer/Work/Attempt/Derivative Dependency-closure 查询完成分页的精确边界。
3. `dependency_closure_root` 承诺该 Cursor 下完整规范化 Dependency Closure，包含适用 Source/Ancestor/Target Lineage 和 Late-discovery Membership；它不等于 WorkItem 数量或 Barrier Root。
4. 三个值必须进入 D 签名 Owner Snapshot Attestation P0 和规范化 `owner_specific_high_waters_digest`。Cursor/Root/High-water 不匹配或发现 Fence 前遗漏依赖时，旧 Snapshot 必须失效，并生成后继 Snapshot/Barrier Reconciliation。

H Schema 1.2.16 Blob `91c4fd7...` 及实例测试 Blob `e1667b0...` 在 H Run #44192602325 中通过（356 项，22 项 skipped）。H 1.2.17 Validator/Test Blob `60cd1b6...` / `24d3cf0...` 将精确 D Snapshot 绑定到 Batch/Manifest Root；精确 H Head `f08dadd...` 的 Run #44193331446 通过 390 项。

**D 候选结论：** 这些字段与 D 现有 ForgetFence、Barrier 和完整 Dependency Lineage 权威一致，但精确 Cursor 分页语义、Root Projection、P0 签名字段和生产 Ledger 查询仍需 D 自有合同补充并批准。本追加是委派 D 角色候选，不是独立人类 D Owner 签名；不证明 Forget Completion、Barrier Release 或物理擦除。
