# Phase 3.8.3 — I Exact Review R3: H Crypto Mapping, Snapshot Digest and Signed Completeness Proofs
# Phase 3.8.3 — I 精确复审 R3：H Crypto Mapping、Snapshot Digest 与签名完整性证明

- Reviewer: I — Security, Identity and Governance
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Provenance: delegated I-role simulation at the user's direction; not an independent human Owner signature.
- Status: **CANDIDATE ONLY — NOT CRYPTOGRAPHICALLY FROZEN / NOT DEPLOYED**
- English and Chinese are normative peers.

## 1. Exact reviewed bundle / 精确审查版本

| Artifact | Exact Blob |
|---|---|
| I `AIMBA-I-CRYPTO-1.0` profile proposal | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` |
| H crypto wire mapping R3 | `b132e6a01bcfe13f92020b9778ee3f7ddbf65753` |
| H unified COC/JF-10 schema 1.2.8 | `70b892797d07489936300a26c0dedfafe1d6e746` |
| H RecoveryJoin schema 1.0.1 | `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c` |
| H schema candidate test file | `ff2b735ccdbf5d45f3c6b2ee9a25d14db2e3c7ad` |

## 2. I disposition / I 审查结论

I accepts the revised composition for the following candidate-level properties:

1. Unified schema 1.2.8 carries an explicit `owner_snapshot_attestation_digest` alongside the locator. H semantic validation requires dereference, signature verification, digest equality and owner/gate/scope/high-water/root comparison.
2. RecoveryJoin 1.0.1 defines typed `completeEmptyProof` and `outOfScopeProof` objects. They bind ledger query, high-water, complete pagination, scope, key-status generation, anti-rollback anchor, signature profile/reference and proof digest.
3. H's mapping defines a separate proof digest and signature preimage for each proof type and preserves I authority.
4. The COC outer record, I owner signature and H transport binding remain independent proofs.
5. The optional structural `signature_profile_id` does not permit semantic downgrade: protected I records must resolve exact I profile identifiers or be rejected.

I 接受修订版在候选层面实现了 Snapshot Locator + Digest 绑定、CompleteEmpty/OutOfScope 类型化证明、独立 Digest/Signature Preimage、三类 Proof Authority 分离，以及结构可选但语义强制的 I Profile ID。

## 3. Remaining amendments / 剩余修订

### I-H-CRYPTO-03 — Stable signature-reference construction

H states that `owner_signature_ref` / `signature_ref` is preallocated and immutable, but the exact deterministic allocation and resolver contract is not yet defined. H must pin:
- reference namespace and owner authority;
- uniqueness scope and collision handling;
- allocation-before-signing transaction boundary;
- immutable ref-to-signature-envelope digest mapping;
- restore/replay behavior if the ref exists but signature bytes are unavailable.

A signature reference must never be derived from the signature bytes if it is itself included in the signed P0 projection.

### I-H-CRYPTO-04 — Independent JCS and Ed25519 implementations

The schema candidate CI does not yet prove the I profile. H must provide at least two independent implementations of:
- duplicate-key rejection before object materialization;
- RFC 8785 JCS for every exact I P0 projection;
- payload digest and domain-separated signature preimage;
- Ed25519 sign/verify and Base64url canonical encoding;
- nested snapshot/empty/out-of-scope proof verification.

Python/Node fixed UTF-8 digest fixtures are useful but are not a complete JCS/Ed25519 profile test.

### I-H-CRYPTO-05 — I operational trust approval

The I profile's algorithm/regulatory suitability, trust-root ceremony, HSM/KMS controls, key rotation/overlap, compromise response, nonce/receipt retention, revocation propagation and external anti-rollback checkpoint remain separate I/governance approvals. No operational values are inferred from this review.

### I-H-CRYPTO-06 — Storage acceptance at final visibility

Storage must accept and implement verification of the exact I proof at its actual final visibility linearization point. A schema/parser or preflight check is insufficient.

## 4. Exact schema CI interpretation / Schema CI 解释

The H branch has a schema candidate test failure on the first 1.2.8 test commit caused by two stale expected strings still saying 1.2.7. The failure was in the test assertion, not in schema parsing or proof validation. A correction was committed afterward; this review does not claim the corrected CI rerun has passed until the exact run is read back.

H 分支首次 1.2.8 Schema 测试失败是测试断言仍写着旧版本号 1.2.7，属于测试夹具错误，不是 Schema/Proof Validator 失败。修正已提交，但在读取精确后续 CI 前，本审查不宣称修正后的 CI 已通过。

## 5. Final I decision / I 最终决议

**ACCEPT WITH ENUMERATED AMENDMENTS** for the exact bundle in §1.

I accepts the candidate schema shape and authority separation. I does not approve production Ed25519 activation, trust roots, key custody, key lifecycle operations, historical trust, anti-rollback deployment, PolicyDomain sequencer, Storage integration or TAB-001 freeze.

**有条件接受**第 1 节精确版本组合的候选 Schema 形状与 Authority 分离。不批准生产 Ed25519 启用、Trust Root、Key Custody/Lifecycle、历史信任、Anti-rollback 部署、PolicyDomain Sequencer、Storage 集成或 TAB-001 冻结。
