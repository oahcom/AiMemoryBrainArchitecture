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
- H semantic contract: Blob b3218298f58cff9b92cb1c38e453af6fd4d0dd50.
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
Updated H semantic contract Blob: b3218298f58cff9b92cb1c38e453af6fd4d0dd50.
Updated HRC suite Blob: 60a2f4db4bd12f2131ecd147db9bbe328da6db50.
