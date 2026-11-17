# Phase 3.8.2 — D Exact Review: RecoveryJoin and Derivative Visibility

- Reviewer perspective: D — Memory Brain / ForgetFence authority
- Review mode: **role simulation in the integration session; not an independent D Owner signature**
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Project phase: architecture proposal only; implementation/conformance NOT VERIFIED.

## 1. Exact review targets

- D Phase 3.8 Publication Participant and Terminal Contract: Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78.
- E Phase 3.8 Publication Orchestration contract: Blob 475fee41e5eea527af4edefbfe88c58c86967d0a.
- I Phase 3.8 Authorization Receipt and Sequencer contract: Blob 54bab0484bd232a5a258e65e34cc7425288b39a6.
- Storage Phase 3.8 Visibility Participant and Atomic Outcome contract: Blob 175ee7b1349cfdb2e450d0fab49e0f61f20a5a5.
- Storage Phase 3.6.11 Bidirectional COC/Owner Admission Join Proof: Blob 41f80b1aacfebdb1f652b16144afbf83ce950e82.
- H RecoveryJoin schema 1.0.0 candidate: Blob f531c1d4b89a48457188c4988f140952759223a6.
- H semantic validator contract: Blob c93560fcda947aef0a611b3096fb1c1994d41cd0.
- HRC semantic suite: Blob d14e66a2196303374f31a4285244a0f77a3ad328.
- A race/crash/failover matrix: Blob c0f8ae699a42de46d12d0d311892e5670014e0f1.

## 2. D disposition

The logical composition is compatible with D authority boundaries:

1. D ProducerWork RegistrationReceipt and ForgetFence order remain D-owned.
2. D PublicationParticipantRef is a D barrier participant, not COC ParticipantIntentRef, StorageVisibilityParticipantRef or Storage PreparedParticipantRef/GID/XID.
3. Storage durable PREPARED_HIDDEN precedes D PublicationParticipant admission.
4. D admission is linearized against D ForgetFence. Fence-first rejects; participant-first holds the affected Fence until authoritative Storage terminal outcome.
5. D closes only after validating the same immutable Storage COMMITTED_VISIBLE or positive NO_PUBLICATION proof.
6. RecoveryJoin is evidence accounting only. It does not clear D's effective ForgetFence or producer-work barrier.
7. COC RecoveryEpochCompleted and outage-gate release cannot be treated as D Forget completion.

## 3. Blocking amendments

### D-RJ-01 — Per-Fence lineage evidence must be explicit

The JoinProof currently carries generic typed owner-evidence refs. For D evidence, the normative edge must resolve and verify:
- ForgetOperationRef and exact selector/scope digest;
- D FenceGeneration and D gate/scope generation;
- D affected-lineage membership/completeness manifest ref + digest;
- exact ProducerWorkItemId / AttemptId / barrier-member identity;
- terminalization or explicit not-affected proof;
- D-local high-water and anti-rollback anchor.

A generic evidence ref is acceptable only if H defines an immutable dereference contract that fetches the signed D proof and verifies every field above. A count/root alone is not sufficient. Unknown lineage remains blocking.

### D-RJ-02 — C primary admission anchor is not D membership

The COC ParticipantManifest owner_admission_ref is the primary C admission anchor. It cannot stand in for D barrier membership. Every participant in D's affected lineage requires a separate D evidence edge; every D registered admission must reverse-join to its exact ParticipantIntentRef, COC position and entry digest.

### D-RJ-03 — NOT_REGISTERED / OUT_OF_SCOPE is not an implicit D clearance

A D request marked OUT_OF_SCOPE_WITH_PROOF requires a D-signed proof bound to the exact ForgetOperationRef, scope and request digest. If lineage is unknown or a protected effect may have occurred, the disposition remains PENDING/UNKNOWN and the D gate stays closed.

### D-RJ-04 — Owner Gate release remains separate from Forget effectiveness

The JoinProof may support D's own currentness CAS, but only D may issue D outage-gate release. That release does not advance ForgetFenceGeneration, close the producer-work barrier or declare Forget effective. Those require D's separate terminalization proof.

## 4. Required D tests

- D fence-first vs RegistrationReceipt and PublicationParticipant admission.
- D participant-first vs later Fence; verify no Fence passes unresolved work.
- Late producer/derivative discovery invalidates D lineage completeness and requires a new round.
- Per-Fence affected/not-affected lineage proof exactness and scope mismatch.
- Same D OwnerAdmissionRef mapped to two participants.
- D high-water / FenceGeneration advances between JoinProof and release CAS.
- Restore with missing D barrier member or stale D projection remains fenced.
- Storage UNKNOWN/IN_DOUBT retains D participant and Fence.
- COMMITTED_VISIBLE and NO_PUBLICATION close only the exact D participant.

## 5. D conclusion

**ACCEPT WITH ENUMERATED AMENDMENTS** as a coherent candidate composition. D-RJ-01..04 must be incorporated into H's typed D evidence mapping and the Storage JoinProof verification contract before D semantic freeze. No D Owner independent approval, implementation PASS, Forget completion or production activation is claimed.

## 6. 中文结论

D 接受逻辑组合方向，但要求 RecoveryJoin 明确绑定每个 ForgetOperation 的 FenceGeneration、Affected-Lineage Manifest、Barrier Member、Work/Attempt 和 Terminal Proof。COC ParticipantManifest 的 C Primary Admission 不能替代 D 的 Barrier Membership。NOT_REGISTERED 或 OUT_OF_SCOPE 必须有 D 签署的精确证明；未知 Lineage 必须保持 Gate/Barrier 开放。D Outage Gate Release 不等于 Forget 生效或 Producer Barrier 完成。

本文件是本集成会话中的 D 角色模拟审查，不是独立 Owner 签名。
