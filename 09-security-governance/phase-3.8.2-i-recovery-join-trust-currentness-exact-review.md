# Phase 3.8.2 — I Exact Review: RecoveryJoin Trust, Currentness and Release

- Reviewer perspective: I — Security, Identity and Governance
- Review mode: **role simulation in the integration session; not an independent I Owner signature**
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Project phase: architecture proposal only; cryptographic profile/implementation/conformance NOT VERIFIED.

## 1. Exact review targets

- D Phase 3.8 contract: Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78.
- E Phase 3.8 contract: Blob 475fee41e5eea527af4edefbfe88c58c86967d0a.
- I Phase 3.8 contract: Blob 54bab0484bd232a5a258e65e34cc7425288b39a6.
- Storage Phase 3.8 contract: Blob 175ee7b1349cfdb79a19898b311a88391ed88010.
- Storage RecoveryJoin contract: Blob 41f80b1aacfebdb1f652b16144afbf83ce950e82.
- H RecoveryJoin schema: Blob dd3234aa1c74caf6d0e335875cd96e0b2b64082f.
- H semantic contract: Blob 6f66a72a2d0aa43af338ff9e22d650d47aa2bd80.
- HRC semantic suite: Blob 60a2f4db4bd12f2131ecd147db9bbe328da6db50.

## 2. I disposition

The authority split is correct:
- I alone owns PolicyDomain authorization, PermissionEpoch, revocation order, issuer/key status and I outage-gate close/release.
- D owns ForgetFence and D barrier/lineage; C owns provider side-effect admission; Storage owns prepared/visibility outcome; COC only records and joins evidence.
- RecoveryJoin is not an ALLOW token and does not authorize receipt issuance/consumption, Storage commit, provider invocation or Forget completion.
- The pre-commit ICommitAuthorizationProof (consumed CommitAuthorizationReceipt / COMMIT_WON sequencer result) is distinct from post-commit ITerminalProof. Storage validates the former; I issues the latter only after Storage terminal outcome.

## 3. Blocking amendments

### I-RJ-01 — Signatures and trust must bind both owner identity layers

I must verify the signed OwnerAdmissionRef, exact OwnerEntryRef row digest, OwnerSnapshotRef/digest, GateGeneration, ScopeGeneration, owner authority, issuer/key version, audience and recovery epoch. The stable admission identity and owner snapshot row identity are separate bindings; neither can substitute for the other.

### I-RJ-02 — Currentness must be revalidated in I's own sequencer

Before I releases its outage gate, the I PolicyDomain sequencer must recheck:
- request and admission roots/counts/high-waters;
- receipt issue and receipt consume high-waters;
- ProducerDomainInventoryEpoch and relevant registry-entry generations;
- I GateGeneration, scope generation and independent anti-rollback anchor;
- exact RecoveryBatchDigest, ParticipantManifestRecordDigest and RecoveryJoinProofDigest;
- all applicable I receipt/terminal participant obligations.

A JoinProof that was valid when created becomes STALE if any relevant I high-water, scope, registry epoch or key status changes before release CAS.

### I-RJ-03 — Empty-set and out-of-scope proofs are security assertions

COMPLETE_EMPTY must be backed by a complete I ledger query and an I-signed canonical empty root. OUT_OF_SCOPE_WITH_PROOF requires I-signed scope-bound proof. Missing evidence, partial cursor, unavailable key status or stale replica is UNKNOWN, not empty or out-of-scope.

### I-RJ-04 — I/Storage terminal pairing is exact and typed

For JF-10, I terminal outcome must bind exact ParticipantIntentRef, PreparedParticipantRef, GID, CanonicalAuthorityDBRef, DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version and operation/tuple digest. COMMIT_WON pairs only with same-tuple Storage COMMITTED; REVOCATION_WON / INDETERMINATE_ABORTED pairs only with same-tuple ROLLED_BACK. UNKNOWN holds the gate and same participant.

### I-RJ-05 — Cryptographic profile remains a freeze blocker

H's TEST-only canonical digest is not an I-approved signing profile. I must decide signature suite, trust roots, key lifecycle, historical verification, compromise/backdating, anti-rollback anchors, nonce retention and revocation propagation. Structural schema PASS cannot imply cryptographic interoperability.

## 4. Required I tests

- I request/receipt issue/consume race with CloseIRecoveryGate.
- Inventory epoch changes after JoinProof but before release CAS.
- Key rotation/revocation/compromise between snapshot and release.
- OwnerAdmissionRef substitution and OwnerEntryRef row substitution.
- Empty-set signature with partial ledger cursor.
- OUT_OF_SCOPE proof from wrong scope or stale signer.
- COMMIT_WON + same tuple Storage COMMITTED.
- COMMIT_WON + different GID/DB incarnation or ROLLED_BACK.
- REVOCATION_WON + same tuple ROLLED_BACK.
- Any UNKNOWN/IN_DOUBT preserves held revocation and no release.
- Restore with sequencer rollback, stale registry projection or missing high-water.

## 5. I conclusion

**ACCEPT WITH ENUMERATED AMENDMENTS**. I-RJ-01..05 must be incorporated into the H/I proof-verification and currentness contract. No I cryptographic profile approval, independent Owner signature, implementation PASS or production activation is claimed.

## 6. 中文结论

I 接受 JoinProof 作为跨权威完整性账本，但它不是授权 Token。I 必须分别验证 OwnerAdmissionRef 与 OwnerEntryRef、Owner Snapshot、Gate/Scope Generation、Inventory Epoch、Receipt Issue/Consume High-water、Key Status 和 Anti-rollback Anchor，并在自己的 PolicyDomain Sequencer 中执行最终 Release CAS。空集合和 OUT_OF_SCOPE 都是必须由 I 签署的安全断言。ICommitAuthorizationProof 与 ITerminalProof 仍是提交前/提交后两个不同阶段。

本文件是本集成会话中的 I 角色模拟审查，不是独立 Owner 签名。


## 7. H schema follow-up — I-RJ-01/02 partially addressed

The latest H RecoveryJoin schema separates OwnerAdmissionRef and OwnerEntryRef, binds request/admission row digests, and requires typed I receipt/terminal evidence to carry PolicyDomainRef, PermissionEpoch, ProducerDomainInventoryEpoch, issuer key and authorization receipt. This addresses schema-shape requirements only. I still must verify signature/key status, historical trust, issuer/audience, policy/registry continuity and currentness inside the I PolicyDomain sequencer at the release CAS. H's test digest profile is not an approved I signature profile. I-RJ-03..05 and runtime trust/currentness remain OPEN.

Updated H RecoveryJoin schema Blob: dd3234aa1c74caf6d0e335875cd96e0b2b64082f.
Updated H semantic contract Blob: 6f66a72a2d0aa43af338ff9e22d650d47aa2bd80.
Updated HRC suite Blob: 60a2f4db4bd12f2131ecd147db9bbe328da6db50.


## 8. Exact H RecoveryJoin candidate re-review / H RecoveryJoin 精确版本复核补充

The H branch now pins this exact candidate set:

- RecoveryJoin schema 1.0.0: `dd3234aa1c74caf6d0e335875cd96e0b2b64082f`
- H semantic validator contract: `6f66a72a2d0aa43af338ff9e22d650d47aa2bd80`
- HRC/JPF suite after JPF-08 fixture correction: `60a2f4db4bd12f2131ecd147db9bbe328da6db50`
- Wire suite: `1a4e754ba9bfa57eb973c6d39731e9f89443b323`
- Schema integrity suite: `67aba74c120f2916d768e7b01c45408ee2624f3a`
- H CI run: [44039990464](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44039990464), 66/66 candidate tests PASS.

I accepts the schema shape only as a proposed typed evidence envelope. The CI pass does not validate production signatures, issuer/key status, historical trust, PermissionEpoch/ProducerDomainInventoryEpoch continuity, owner-signed empty/out-of-scope proofs, or I's actual PolicyDomain sequencer. HRC TEST-only digest remains non-normative. I-RJ-01/02 schema-shape coverage improves; I-RJ-03/04/05 and all runtime currentness/crypto obligations remain OPEN.

This exact-version re-review does not approve I cryptographic profile, does not issue an I gate-release decision and is not an independent human Owner signature.

H 分支当前 RecoveryJoin Schema 及候选验证套件已精确绑定，66/66 逻辑/结构候选测试通过。I 仅接受其类型化证据字段形状作为提案；不接受其 TEST-only 摘要作为生产签名规范。真实签名、Key Status、历史信任、PermissionEpoch 与 Inventory Epoch 连续性、空集合签名及 I PolicyDomain Sequencer 的 Currentness CAS 仍未闭环。


## 9. Signature profile registry boundary / Signature Profile 注册表边界

H exact schema 1.2.7 review Blob: `8bed0b05cd631014bf5af7cb5a8dafdd932940e9`; schema Blob: `e9748a5b904d2b975e47a32a0cbb31de31636854`.

I disposition: `signature_profile_id` is a typed reference only. I owns the trusted issuer/key/profile registry and must resolve the identifier from an authenticated current registry; no profile definition, algorithm or key material supplied in the message payload is authoritative. For protected owner-signed records I requires semantic validation to enforce presence, owner/issuer binding, audience/purpose/scope, key version/status, canonicalization profile separation, anti-rollback and historical verification. Missing/unknown/downgraded/wrong-audience/wrong-owner profiles yield UNKNOWN/REJECT and keep the gate closed according to the relevant verification state. I does not approve a production signature suite or registry implementation in this review.

The H schema field is structurally optional; H's own review states semantic validation must require it for protected owner-signed records. I accepts that layering only if the executable semantic validator and negative vectors are added. I cryptographic profile and runtime trust remain OPEN.
