# Phase 3.8.2 — E Exact Review: RecoveryJoin Orchestration and Retry

- Reviewer perspective: E — Memory Compiler
- Review mode: **role simulation in the integration session; not an independent E Owner signature**
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Project phase: architecture proposal only; implementation/conformance NOT VERIFIED.

## 1. Exact review targets

- D Phase 3.8 contract: Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78.
- E Phase 3.8 contract: Blob 475fee41e5eea527af4edefbfe88c58c86967d0a.
- I Phase 3.8 contract: Blob 54bab0484bd232a5a258e65e34cc7425288b39a6.
- Storage Phase 3.8 contract: Blob 175ee7b1349cfdb2e450d0fab49e0f61f20a5a5.
- Storage RecoveryJoin contract: Blob 41f80b1aacfebdb1f652b16144afbf83ce950e82.
- H RecoveryJoin schema candidate: Blob f531c1d4b89a48457188c4988f140952759223a6.
- H semantic suite: Blob d14e66a2196303374f31a4285244a0f77a3ad328.
- A deterministic conformance matrix: Blob c0f8ae699a42de46d12d0d311892e5670014e0f1.

## 2. E disposition

The Phase 3.8 orchestration order is coherent:
Storage durable hidden prepare → D publication admission → I single-use sequencer consumption → Storage final visibility commit → D/I independent closeout.

E correctly distinguishes:
- logical ProducerWorkItemId from DerivationRunId and AttemptId/LeaseId/LeaseEpoch;
- same-operation transport retry/recovery from a new publication attempt after authoritative NO_PUBLICATION;
- private staged artifact from publicly visible artifact;
- local compiler outcome from D/I/Storage owner terminal evidence.

The RecoveryJoin does not create a new compiler identity and cannot be used to infer a missing D/I/Storage receipt.

## 3. Blocking amendments

### E-RJ-01 — Recovery Join must gate restore and protected dispatch

E's Phase 3.8 visibility flow does not explicitly state that a restored compiler runtime remains non-serving until the exact RecoveryCutoffBatch, ParticipantManifest, RecoveryJoinProof, current I/D/C owner releases and D/I/Storage restore proofs reconcile. E must add an explicit recovery gate before queue dispatch, protected source dereference, lease execution, retry replay, or publication after restore.

### E-RJ-02 — Request and admission rows must remain separate

E must not collapse owner requests into admissions or treat a COC ParticipantIntent as proof that the compiler's D RegistrationReceipt exists. The JoinProof request-disposition set and admission-to-participant edges are separate. A NOT_REGISTERED request with possible side effect remains quarantined and cannot be replayed into a new identity.

### E-RJ-03 — Retry identity after JoinProof

Same immutable publication recovery preserves PublicationOperationId, tuple digest and all owner participant refs. A new attempt after authoritative NO_PUBLICATION gets new publication/participant identities while preserving the logical ProducerWorkItemId. A changed compiler input/source revision/dependency set creates a new DerivationRun/output identity and fresh D/I gates.

### E-RJ-04 — Compiler local state is not JoinProof evidence

Queue ACK, E AcceptedReceipt, private object existence, local Published/Completed label or expired Lease cannot fill I/D/C owner evidence edges or close D ProducerWork. E must expose exact inventory refs/digests for every Run, Attempt, stage, dependency, publication and replay path.

## 4. Required E tests

- Restore while JoinProof missing or stale: no queue dispatch or protected dereference.
- Duplicate queue delivery and stale lease cannot change participant identities.
- COC participant present but D RegistrationReceipt missing: block.
- Owner request NOT_REGISTERED with possible effect: remain quarantined.
- Same publication operation lost ACK: same IDs/digest resolve.
- NO_PUBLICATION followed by new attempt: new PublicationOperationId/participants.
- Changed compiler input/dependency/source revision: new DerivationRun and fresh gates.
- RecoveryJoin complete but D/I/Storage terminal UNKNOWN: compiler remains non-serving/private.
- Outbox/DLQ/delayed publisher replay cannot bypass a closed owner gate.

## 5. E conclusion

**ACCEPT WITH ENUMERATED AMENDMENTS**. E-RJ-01..04 must be reflected in the E restore/dispatch lifecycle and deterministic conformance matrix. No E Owner independent approval, compiler implementation PASS or production activation is claimed.

## 6. 中文结论

E 接受 Storage→D→I→Storage 的可见性编排，但要求 Restore 后先完成精确 RecoveryJoin 和 I/D/C Owner Release，再允许 Queue Dispatch、Protected Source Dereference、Lease Execution、Retry Replay 或 Publication。Request 与 Admission 必须分离；同一操作恢复沿用原 ID，NO_PUBLICATION 后新尝试使用新 PublicationOperationId。E 本地状态不能替代 Owner Proof。

本文件是本集成会话中的 E 角色模拟审查，不是独立 Owner 签名。
