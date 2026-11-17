# Phase 3.8.10 — H Review of I P0 Allowlists for Unified 1.2.14 / RecoveryJoin 1.0.2
# Phase 3.8.10 — H 对 I P0 白名单（Unified 1.2.14 / RecoveryJoin 1.0.2）的复审

- Reviewer: H — BMCP Protocol and Interoperability
- Exact I successor P0 addendum: `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md`
- I successor P0 Blob: `44986f5f864bcdc1a79d34978273644d381a68c0`
- H Unified schema 1.2.14 Blob: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H RecoveryJoin schema 1.0.2 Blob: `4b664e3bce465499bcdfd93796349a4ba7074002`
- I Owner Snapshot Attestation schema 1.0.0 Blob: `ecf9971b089ca5fab9a92915663dc913c8ab1ba6`
- I Phase 3.8.13 callback semantics review: Blob `373c1d1fc38018cdc138764e67bed141143dddda`
- I Phase 3.8.14 final compatibility review: Blob `bcf4314a8b764a26b7baf5ec387ad98cf7ddf0a5`
- Prior H review for Unified 1.2.13: Blob `c16063197766a495feb98776c7516ebcbe4b7441`
- Status: **ACCEPT WITH ENUMERATED L3 OBLIGATIONS — EXACT L1 FIELD CONTRACT CANDIDATE; NOT FROZEN**
- Provenance: delegated H-role review; **not an independent human H Owner signature**.

## 1. Common-envelope P0 / Common Envelope P0

H Unified 1.2.14 preserves the exact H 1.2.13 common-envelope P0 shape, with only the schema artifact revision advanced to 1.2.14 and the D-only high-water extension described in §2. The I P0 includes `schema_artifact_revision` as a signed field and covers every common-envelope semantic field. It excludes only the expressly permitted payload digest/signature/integrity locators/channel-binding locators and COC-appended quorum/record proof fields. No common semantic field is omitted.

H Unified 1.2.14 保持 H 1.2.13 的 Common Envelope P0 结构，仅将 Schema Artifact Revision 推进到 1.2.14，并增加 §2 所述 D-only High-Water。I P0 已将 `schema_artifact_revision` 纳入签名字段，覆盖所有 Common Envelope 语义字段；只排除明确允许的 Payload Digest/Signature/Integrity Locator/Channel Binding Locator 和 COC 追加 Quorum/Record Proof。

## 2. D-only high-water delta / 仅 D High-Water 变化

H 1.2.14 adds `ownerSpecificHighWatersD.forget_fence_generation_high_water`. It is not part of the I owner-specific high-water union and is not part of I P0. The I high-water object remains exactly five fields:
`receipt_issue_high_water`, `receipt_consume_high_water`, `inventory_epoch_ref`, `registry_snapshot_digest`, `relevant_entry_set_root`.

The new D field is distinct from D `owner_gate_generation` and `barrier_generation`, and from every I PermissionEpoch/InventoryEpoch/receipt/PolicyDomain position. H MUST NOT compare or alias these domains.

H 1.2.14 新增 `ownerSpecificHighWatersD.forget_fence_generation_high_water`，该字段不属于 I High-Water Union 或 I P0。I 的五字段 High-Water Object 保持不变。D Fence High-Water 与 D GateGeneration、BarrierGeneration 及所有 I PermissionEpoch/InventoryEpoch/Receipt/PolicyDomain Position 均不同，H 不得比较或别名化。

## 3. I owner snapshot attestation / I Owner Snapshot Attestation

The H 1.2.14 `ownerSnapshot` remains a COC-carried summary, not the I signature object. The exact I attestation schema Blob `ecf9971b089ca5fab9a92915663dc913c8ab1ba6` has the same five required I high-water fields as H `ownerSpecificHighWatersI`.

- H `owner_snapshot_attestation_digest` equals I attestation `attestation_digest` and is recomputed from the exact I P0.
- H `owner_specific_high_waters_digest` is recomputed over the exact I high-water object.
- Underlying `snapshot_digest`, attestation digest and owner-specific-high-water digest are distinct digest domains.
- COC summary never substitutes for I's owner-signed attestation.

## 4. RecoveryJoin 1.0.2 I membership proof / I Membership Proof

H confirms the I successor defines the exact generic RecoveryJoin 1.0.2 proof P0 for `owner_kind=I`. It includes the I owner ledger/entry/admission, I namespace/local sequence/high-water/root, snapshot/attestation, gate/scope/operation/request, anti-rollback/key-status and signature profile/key/canonicalization/digest fields.

The I-specific proof contract excludes both derived `proof_digest` and external `signature_ref` from P0. The final signature projection is P0 plus `proof_digest`; `signature_ref` is an external locator and is not signed into its own P0. This matches the earlier I owner membership proof contract and the RecoveryJoin schema.

H 确认 I 后继文件为 `owner_kind=I` 定义了 RecoveryJoin 1.0.2 通用 P0。I P0 同时排除派生 `proof_digest` 和外部 `signature_ref`；签名投影为 P0 加 `proof_digest`，`signature_ref` 仅定位外部签名，不进入自身 P0。这与 I 原始 Owner Membership Proof 合同及 RecoveryJoin Schema 一致。

## 5. L3 proof vectors / L3 证明向量

1. Mutate or omit `schema_artifact_revision=1.2.14` → schema/signature INVALID.
2. Substitute I `owner_specific_high_waters_digest` or the underlying snapshot digest → INVALID.
3. Add D/C high-water fields to I's owner-specific union → INVALID.
4. Change I owner namespace, admission row, gate/scope/operation, key-status generation or anti-rollback anchor → INVALID.
5. Mutate external `signature_ref`: P0 remains byte-identical, but wrong resolved signature is INVALID and unavailable signature is UNKNOWN.
6. Missing I ledger pagination/currentness or trust root → UNKNOWN, never COMPLETE_EMPTY.
7. D `forget_fence_generation_high_water` must not enter I P0 or be compared with I counters.

No complete differential P0 suite is claimed by this review.

## 6. H disposition / H 侧结论

**ACCEPT WITH ENUMERATED L3 OBLIGATIONS — EXACT L1 FIELD CONTRACT CANDIDATE; NOT FROZEN.**

The I common-envelope P0 now binds H 1.2.14's artifact revision; I's owner-specific high-water and RecoveryJoin membership proof shapes remain exact. The D-only fence high-water is correctly kept outside I's namespace. L3 differential vectors, I profile registration, trust root, key lifecycle/custody, historical verification and anti-rollback deployment remain OPEN.

**有条件接受：** I Common Envelope P0 已绑定 H 1.2.14 Artifact Revision；I 专属 High-Water 和 RecoveryJoin Membership Proof 结构精确；D-only Fence High-Water 未混入 I Namespace。L3 差分向量、I Profile 注册、Trust Root、密钥生命周期/托管、历史验证及 Anti-Rollback 部署仍 OPEN。

This is a delegated H-role technical review, not an independent human H Owner signature. It does not close JF-10, Global Forget or authorize production.


## 7. I callback authority review / I Callback Authority 复审

I Phase 3.8.13 accepts H's verify_i_terminal_decision callback only as a fail-closed interface. The callback must independently resolve and verify I's exact COMMIT_WON/REVOCATION_WON/UNKNOWN terminal evidence, PolicyDomain/XID/request scope, key status and anti-rollback. H cannot issue I authorization, and C/D/Storage/COC evidence cannot substitute. The I review does not register or deploy production I trust services.

I Phase 3.8.13 接受 H 的 verify_i_terminal_decision 回调，但仅作为 Fail-Closed 接口。回调必须独立解析并验证 I 的 COMMIT_WON/REVOCATION_WON/UNKNOWN 终态、PolicyDomain/XID/Request 范围、Key Status 和 Anti-Rollback。H 不能签发 I 授权，C/D/Storage/COC 证据不能替代 I。I 复审不代表生产 I Trust Service 已注册或部署。
