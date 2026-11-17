# Phase 3.8.9 — H Review of I P0 Allowlists for Unified 1.2.13 / RecoveryJoin 1.0.2
# Phase 3.8.9 — H 对 I P0 白名单（Unified 1.2.13 / RecoveryJoin 1.0.2）的复审

- Reviewer: H — BMCP Protocol and Interoperability
- Exact I successor P0 addendum: `09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md`
- I successor P0 Blob: `5c0e2049513d391dfc118f4f629a5ec95de456d6`
- H Unified schema 1.2.13 Blob: `8e7f6a6c9663388863db88548f9c37d0fdb1bd97`
- H RecoveryJoin schema 1.0.2 Blob: `4b664e3bce465499bcdfd93796349a4ba7074002`
- I Owner Snapshot Attestation schema 1.0.0 Blob: `ecf9971b089ca5fab9a92915663dc913c8ab1ba6`
- Historical I P0 addendum 3.8.7 Blob: `739dc15e3cca33aef3f012f713b988e5528d4ad9`
- Status: **ACCEPT WITH ENUMERATED L3 OBLIGATIONS — EXACT L1 FIELD CONTRACT CANDIDATE; NOT FROZEN**
- Provenance: delegated H-role review in the coordinating session; **not an independent human H Owner signature**.

## 1. Common-envelope P0 exactness / Common Envelope P0 精确性

H 1.2.13 adds required `schema_artifact_revision` to the common envelope and explicitly declares it part of protected owner signature projections. The historical I Phase 3.8.7 allowlist did not include this field; its generic "no other common field may be excluded" sentence therefore conflicted with the current schema.

The I Phase 3.8.9 successor corrects the omission. H compared the exact H 1.2.13 common-envelope property set with the I allowlist. The allowlist now covers every signed semantic field, including `schema_artifact_revision`. It excludes only the explicitly permitted non-P0 fields: `payload_digest`, `signature`, integrity/channel-binding locators, and the COC-appended quorum/record proof fields. No other common field is omitted.

H 1.2.13 在 Common Envelope 中新增必需 `schema_artifact_revision`，并明确该字段属于受保护 Owner Signature Projection。历史 I Phase 3.8.7 白名单未包含该字段，因此其“不得排除其他 Common Field”与当前 Schema 存在冲突。I Phase 3.8.9 已补齐。H 已比较 H 1.2.13 Common Envelope 属性集合与 I 白名单：现已覆盖所有签名语义字段，只排除明确允许的 Payload Digest、Signature、Integrity/Channel Binding Locator 及 COC 追加 Quorum/Record 证明字段。

## 2. I owner snapshot attestation / I Owner Snapshot Attestation

The H 1.2.13 `ownerSnapshot` is a COC-carried summary, not the I signature object. H verifies the exact I-signed `IOwnerSnapshotAttestation/1.0` by dereferencing `owner_snapshot_attestation_ref`.

Exact I high-water mapping:
- H `ownerSpecificHighWatersI` requires exactly `receipt_issue_high_water`, `receipt_consume_high_water`, `inventory_epoch_ref`, `registry_snapshot_digest`, `relevant_entry_set_root`.
- I attestation schema 1.0.0 requires exactly the same five fields in `owner_specific_high_waters`; no D/C fields are permitted.
- H summary `owner_snapshot_attestation_digest` equals I attestation `attestation_digest` and must be recomputed from the exact I signed P0.
- H summary `owner_specific_high_waters_digest` is recomputed over the exact I high-water object under the approved canonical profile.
- Underlying `snapshot_digest`, attestation digest and owner-specific-high-water digest are three distinct digest values/domains and must not be substituted.

H 1.2.13 的 I High-Water Union 与 I Attestation Schema 的五个必需字段完全一致，不允许混入 D/C 字段。H Summary 的 Attestation Digest 必须等于 I Attestation Digest 并从精确签名 P0 重算；High-Water Digest 则对精确 I High-Water Object 独立重算。底层 Snapshot Digest、Attestation Digest 和 High-Water Digest 是三个不同摘要域，不得互相替代。

## 3. RecoveryJoin 1.0.2 membership proof / RecoveryJoin 1.0.2 Membership Proof

RecoveryJoin 1.0.2 requires `owner_snapshot_membership_proofs`. H confirms the I successor defines a distinct I-signed P0 for this proof payload. It is not the snapshot attestation, ICompleteEmptyProof or IOutOfScopeProof.

For an I proof, the required binding includes:
- `owner_kind=I` and the unique I `owner_authority_ref`;
- exact issuer/subject/audience/purpose;
- I owner ledger/version, owner entry/digest and admission reference;
- I `owner_sequence_namespace`, owner-local sequence, high-water and ledger root;
- exact owner snapshot/digest and I snapshot attestation ref/digest;
- owner gate/generation, scope/generation/binding digest;
- operation identity/digest and request digest;
- anti-rollback anchor and key-status generation;
- signature profile, key ID/version, canonicalization/digest profile; `signature_ref` is an external signature locator, not a P0 field.

Both derived `proof_digest` and external `signature_ref` are excluded from P0. `proof_digest` is computed from domain-separated JCS(P0), and the signature projection includes P0 plus that digest. `signature_ref` only locates the signature bytes; it is not signed into its own P0. H rejects a wrong owner, purpose, unknown field or tuple mismatch as INVALID. Missing I ledger/snapshot/key-status/anti-rollback evidence remains UNKNOWN.

Namespace separation is mandatory: I `owner_sequence_namespace` is not C `sequence_namespace_ref`, COC quorum position, D local sequence, Storage attempt identity or the database serialization anchor. No cross-domain counter comparison is allowed.

RecoveryJoin 1.0.2 要求 `owner_snapshot_membership_proofs`。I 已定义独立 I 签名 P0；它不同于 Snapshot Attestation、ICompleteEmptyProof 和 IOutOfScopeProof。H 必须核验 I Owner、Ledger/Admission、I Namespace、Snapshot/Attestation、Gate/Scope、Operation/Request、Anti-Rollback/Key Status 及签名配置的完整绑定。仅 `proof_digest` 从 P0 排除并按 Domain-separated JCS 重算。错误 Owner/Purpose/未知字段/Join 不匹配为 INVALID；权威证据缺失为 UNKNOWN。I Namespace 与 C、COC、D、Storage 和数据库序列化锚点严格隔离。

## 4. L3 proof vectors / L3 证明向量

The following exact vectors are required before L3 closure:
1. mutate `schema_artifact_revision` while retaining all other common P0 fields → signature verification INVALID;
2. omit `schema_artifact_revision` from an H 1.2.13 message → schema INVALID;
3. omit `owner_snapshot_attestation_digest` or substitute the underlying snapshot digest → INVALID;
4. mutate one I owner-specific high-water field or add a D/C field to the I union → INVALID;
5. mismatch `owner_specific_high_waters_digest` against recomputed exact object → INVALID;
6. omit a required RecoveryJoin 1.0.2 membership proof when an admission row requires it → incomplete/INVALID, never silently complete;
7. mismatch membership proof owner ledger row, sequence namespace, admission ref, snapshot digest, attestation digest, gate/scope or operation tuple → INVALID;
8. unavailable key-status, I trust root, ledger pagination or anti-rollback checkpoint → UNKNOWN;
9. use C `sequence_namespace_ref` in an I proof or compare I/C/D/COC counters → INVALID;
10. mutate external `signature_ref` → P0 remains byte-identical, but the resolved signature must verify against the exact signed P0; wrong ref is INVALID and unavailable ref is UNKNOWN.\n11. mutate COC-appended quorum proof without changing I P0 → I P0 remains byte-identical, but independent COC proof verification rejects the envelope.

No full differential P0 vector run is claimed by this review. At least two independent implementations must produce byte-identical P0, digest and signature preimage for every I message family and standalone proof type.

## 5. H disposition / H 侧结论

**ACCEPT WITH ENUMERATED L3 OBLIGATIONS — EXACT L1 FIELD CONTRACT CANDIDATE; NOT FROZEN.**

The prior schema-version omission is corrected, I ownerSnapshot high-water mapping is structurally consistent, and the RecoveryJoin 1.0.2 I membership proof P0 is now explicitly defined. Remaining open items:
- independent P0 differential vectors and full semantic validator execution;
- I profile registration, trust root, key lifecycle/custody and historical verification;
- external anti-rollback deployment and key-status service;
- complete pagination and snapshot/member-set proofs for real I ledgers;
- independent Owner signatures and system-level A integration.

**有条件接受并保留 L3 义务：** Common Envelope P0 遗漏已修正；I Snapshot High-Water 映射结构一致；RecoveryJoin 1.0.2 的 I Membership Proof P0 已明确。仍需独立 P0 差分向量、完整 Semantic Validator、I Profile/Trust Root/密钥治理、Anti-Rollback、真实 Ledger Pagination/Snapshot Proof、独立 Owner 签署及 A 系统集成审查。

This is a delegated H-role technical review, not an independent human H Owner signature. It does not register or deploy I trust, close JF-10, prove Global Forget, or authorize production.
