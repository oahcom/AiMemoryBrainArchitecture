---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Restored byte-for-byte from Owner source branch; Owner acceptance remains pending."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "E-domain Memory Compiler record phase-3.8.2-e-recovery-join-orchestration-exact-review.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3-8-2-e-recovery-join-orchestration-exact-review"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-8-2-e-recovery-join-orchestration-exact-review
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.8.2 — E Exact Review: RecoveryJoin Orchestration and Retry

- Reviewer perspective: E — Memory Compiler
- Review mode: **role simulation in the integration session; not an independent E Owner signature**
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Project phase: architecture proposal only; implementation/conformance NOT VERIFIED.

## 1. Exact review targets

- D Phase 3.8 contract: Blob 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78.
- E Phase 3.8 contract: Blob 475fee41e5eea527af4edefbfe88c58c86967d0a.
- I Phase 3.8 contract: Blob 54bab0484bd232a5a258e65e34cc7425288b39a6.
- Storage Phase 3.8 contract: Blob 175ee7b1349cfdb79a19898b311a88391ed88010.
- Storage RecoveryJoin contract: Blob 41f80b1aacfebdb1f652b16144afbf83ce950e82.
- H RecoveryJoin schema candidate: Blob dd3234aa1c74caf6d0e335875cd96e0b2b64082f.
- H semantic suite: Blob 60a2f4db4bd12f2131ecd147db9bbe328da6db50.
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


## 7. H/Storage follow-up

The latest RecoveryJoin schema adds explicit owner request dispositions, row-level identity/digest binding and typed D/I/C/Storage evidence. This improves E's ability to distinguish pending requests from admitted work and to reconcile exact recovery inventory. It does not implement E-RJ-01: E still needs a runtime gate that blocks queue dispatch, protected source dereference, lease execution, retry replay and publication until exact RecoveryJoin, current owner releases and restore reconciliation are proven.

Updated H RecoveryJoin schema Blob: dd3234aa1c74caf6d0e335875cd96e0b2b64082f.
Updated HRC suite Blob: 60a2f4db4bd12f2131ecd147db9bbe328da6db50.


## Verified H candidate CI result

GitHub Actions run 44039990464, job 133891944149, checked out H commit da94bcc1796cb350eed12845e49cbc3663faab9c and completed 66/66 candidate tests successfully (Ubuntu 26.04 / CPython 3.12.16). This is a PASS for the committed Python HRC/JPF/WIRE/SCHEMA candidate suite only. It does not prove production signatures, cross-language canonical bytes, live owner/COC adapters, physical JF-10 behavior or deployed Storage topology/HA/restore.
