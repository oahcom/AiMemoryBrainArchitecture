# Phase 3.8.2 — Storage Exact Review: RecoveryJoin, Visibility and Serialization Topology

- Reviewer perspective: Storage / Consistency
- Review mode: **role simulation in the integration session; not an independent Storage Owner signature**
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS; TOPOLOGY ADR-BLOCKED**
- Project phase: architecture proposal only; no implementation/conformance PASS.

## 1. Exact review targets

- D Phase 3.8 contract: Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78.
- E Phase 3.8 contract: Blob 475fee41e5eea527af4edefbfe88c58c86967d0a.
- I Phase 3.8 contract: Blob 54bab0484bd232a5a258e65e34cc7425288b39a6.
- Storage Phase 3.8 visibility contract: Blob 175ee7b1349cfdb2e450d0fab49e0f61f20a5a5.
- Storage Phase 3.6.11 bidirectional JoinProof: Blob 41f80b1aacfebdb1f652b16144afbf83ce950e82.
- H RecoveryJoin schema 1.0.0: Blob f531c1d4b89a48457188c4988f140952759223a6.
- H semantic validator/test contract: Blob c93560fcda947aef0a611b3096fb1c1994d41cd0.
- HRC/JPF executable suite: Blob d14e66a2196303374f31a4285244a0f77a3ad328.
- A race/crash/failover matrix: Blob c0f8ae699a42de46d12d0d311892e5670014e0f1.

## 2. Storage disposition

The bidirectional join design preserves separate authorities and the acyclic digest chain:
ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest → RecoveryJoinProofDigest → owner release / RecoveryEpochCompleted.

It correctly distinguishes:
- COC ParticipantIntent set through exact prefix P;
- I/D/C request sets;
- I/D/C admission sets;
- OwnerAdmissionRef vs OwnerEntryRef;
- C primary admission anchor vs additional I/D/C/Storage evidence edges;
- NOT_REGISTERED no-effect proof vs unresolved pending obligation;
- D/I/C owner release vs COC recovery completion;
- Storage PreparedParticipantRef/GID/DatabaseIncarnationRef vs COC ParticipantIntentRef.

Storage can persist and quorum-commit JoinProof only after complete authoritative readback of the batch, manifest and owner snapshots. Storage cannot sign or issue I/D/C gate release.

## 3. Blocking amendments

### STORAGE-RJ-01 — JoinProof must include exact request-row disposition

Every I/D/C request member must map to exactly one request disposition by OwnerRequestRef + OwnerEntryRef + OwnerRequestDigest + owner-local sequence namespace/value + Scope. OUT_OF_SCOPE_WITH_PROOF requires an owner-signed proof. A missing request edge blocks JoinProof even if all admission/participant joins match.

### STORAGE-RJ-02 — Manifest enumeration must be independently re-readable

A complete ParticipantManifest must equal the authoritative COC participant set through exact prefix P, including every page/cursor and committed entry digest. Count/root equality without authoritative prefix enumeration is not sufficient. Missing page, stale follower or quorum loss is UNKNOWN.

### STORAGE-RJ-03 — Both digest phases must be crash-safe

Keep the Storage v3.1 digest order: precomputed manifest content → batch → committed manifest record → JoinProof. Crash after batch but before manifest, or after manifest before JoinProof, stays fenced and resumes the same immutable IDs/digests. Never replace a batch or manifest identity to escape an ACK gap.

### STORAGE-RJ-04 — Owner release currentness remains independent

JoinProof is not an aggregate release token. I/D/C each re-read their own authoritative roots/high-waters/generations/anti-rollback anchor and perform a local CAS. Any advance returns STALE and requires a new round. COC cannot release an owner gate.

### STORAGE-RJ-05 — Physical topology remains unselected

The Phase 3.8 Storage visibility contract's one-serializable-DB-per-Canonical-Authority idea is a recommendation, not a deployed topology. The Phase 3.8.2 ADR records Option A as conditional preference, Option B as an alternative and check-then-write as rejected. No actual Canonical Authority runtime/DB adapter or D/Storage shared serialization domain has been designated. JF-10 PostgreSQL 18.7 candidate CI is not proof of production topology.

## 4. Required Storage tests

- Batch/manifest/JoinProof digest order with crash after each commit.
- Missing/duplicate participant, request or admission row.
- OwnerAdmissionRef and OwnerEntryRef independently substituted.
- Same owner row joined to two participants.
- Same participant joined to conflicting operation/scope/digest.
- Empty COC prefix plus empty/non-empty owner request/admission combinations.
- NOT_REGISTERED with no effect vs possible effect.
- JoinProof created then I/D/C high-water advances before release CAS.
- JF-10 same GID/DatabaseIncarnationRef COMMITTED/ROLLED_BACK/UNKNOWN mapping.
- DB failover, old-primary fencing, stale replica, snapshot rollback and restore quarantine.
- Actual visibility pointer, PublicationReceipt, Storage outcome and outbox atomicity.

## 5. Topology ADR disposition

The new Storage topology ADR is **ADR-BLOCKED / NO TOPOLOGY SELECTED**. Option A is preferred only if the real Canonical Authority runtime proves D and Storage can share the approved serializable transaction domain while preserving semantic ownership. Otherwise Option B requires a named durable linearizable coordinator and independent failover proof. The actual runtime, DB adapter, D/Storage row ownership, read path, deployment topology, human operator/on-call and PITR/old-primary fencing remain open.

## 6. Storage conclusion

**ACCEPT WITH ENUMERATED AMENDMENTS** for the logical JoinProof and visibility contract. STORAGE-RJ-01..05 remain explicit blockers. No schema freeze, DB product/topology approval, implementation/conformance PASS, deployment or production activation is claimed.

## 7. 中文结论

Storage 接受双向 Join Proof 的逻辑方向：COC Prefix Participant 集合与 I/D/C Request/Admission 集合分别由各自权威完整枚举，再通过两方向 Typed Edge 建立关系。必须保留 OwnerAdmissionRef 与 OwnerEntryRef 的区分，C Primary Admission Anchor 与 I/D/C/Storage 其他证据分开，NOT_REGISTERED 必须有无副作用证明或保持 Pending。Storage 只持久化/提交 JoinProof，不能签发 Owner Gate Release。

物理拓扑 ADR 仍 ADR-BLOCKED：Option A 是有条件优先候选，Option B 是替代方案，Check-then-write 被拒绝；真实 Canonical Authority Runtime 和 D/Storage 事务域尚未指定。

本文件是本集成会话中的 Storage 角色模拟审查，不是独立 Owner 签名。
