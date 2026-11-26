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
    canonical_scope: "E-domain Memory Compiler record phase-3.8-e-publication-orchestration-retry-recovery-contract.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3-8-e-publication-orchestration-retry-recovery-contract"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-8-e-publication-orchestration-retry-recovery-contract
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.8 — E Publication Orchestration, Retry and Recovery Contract

- Owner role: E — Memory Compiler
- Status: **E-role proposal; D/I/Storage exact APIs and independent Owner approval OPEN**
- Related: Issue #25; A Phase 3.8.1 contract-surface addendum
- English and Chinese are normative peers.

## 1. E authority boundary

E owns CompileIntent, compiler ingress receipt, immutable compiler input bundle, DerivationRun, Attempt/Lease lifecycle, private staging, complete output/dependency submission and compiler-side recovery orchestration.

E does not mint D ProducerClass eligibility, D RegistrationReceipt, D PublicationParticipantRef, I authorization, Storage visibility outcome or global Forget terminality. Queue ACK, E AcceptedReceipt, local Published/Completed labels and object-store existence are not cross-owner proof.

## 2. Required identity model

- CompileIntentId: stable logical intent.
- ProducerWorkItemId: stable D-governed logical work identity.
- request_digest: immutable logical admission request.
- DerivationRunId: one immutable compiler input/configuration run.
- AttemptId / LeaseId / LeaseEpoch: one execution attempt and fencing generation.
- DependencyRegistrationId / complete_dependency_set_digest: one immutable full lineage set.
- PublicationOperationId / publication_tuple_digest: one immutable publication attempt.
- D PublicationParticipantRef, I CommitAuthorizationReceiptRef, StorageVisibilityParticipantRef: three distinct owner-specific identities.

Retrying the same transport or resolving a lost ACK preserves the operation identity and digest. A new publication attempt after authoritative NO_PUBLICATION or after changing artifact/version, source revision, dependency set, Scope, compiler input or attempt/lease tuple gets a new PublicationOperationId, participant identities and tuple digest. Never reuse one operation ID with a changed digest.

## 3. Normative E lifecycle

1. Persist E ingress and stable CompileIntentId/ProducerWorkItemId.
2. Call D RegisterProducerWork and resolve durable D RegistrationReceipt by WorkItemId + request digest.
3. Only after D registration is durable may E enqueue, lease, dereference protected sources or execute.
4. Freeze an immutable compiler input bundle for one DerivationRunId: exact source refs/revisions, evidence/provenance, Scope, policy observations, compiler/model/schema versions and deterministic input digest.
5. Revalidate current I authorization and D fence/lineage at every protected source dereference and execution boundary.
6. Produce immutable output into private staging. No public locator, signed URL, index event or cache warming may expose it.
7. Link EventRef-only ingress to exact Canonical MemoryRef/MemoryVersionRef identities and revisions before dependency registration.
8. Submit the entire direct + transitive dependency set as one immutable D dependency registration operation. Do not publish partial sets.
9. Resolve complete D DependencyRegistrationReceipt.
10. Ask Storage to persist hidden StorageVisibilityParticipantRef bound to the immutable publication tuple.
11. Ask D to admit PublicationParticipantRef bound to that exact durable Storage participant.
12. Ask I to consume the single-use CommitAuthorization operation in its PolicyDomain sequencer, bound to the exact D and Storage participant refs.
13. Ask Storage to perform the final visibility transaction, validating exact D current participant/fence and the consumed I CommitAuthorizationReceipt / ICommitAuthorizationProof (not post-commit ITerminalProof).
14. Resolve authoritative Storage outcome by the same PublicationOperationId + tuple digest.
15. D and I independently close their participants only after validating the same Storage COMMITTED_VISIBLE or NO_PUBLICATION outcome.
16. E updates its local output accounting only after owner receipts are resolved. E local status does not close D ProducerWork.

Any unresolved step blocks progression. UNKNOWN keeps the artifact private and all admitted barriers open.

## 4. EventRef-only ingress

E may accept EventRef-only input locally, but must not dispatch derivative-capable work until D has issued RegistrationReceipt. D admission requires authenticated producer, enabled ProducerClass/version, exact Scope, canonical request digest and D-approved opaque lineage token/digest. E's AcceptedReceipt is local ingress evidence only.

Before dependency registration/publication, E must resolve exact canonical source refs/revisions and append them to the original lineage. Incomplete or conflicting lineage stays private/quarantined. D registration is not I permission to read protected payload.

## 5. Dependency completeness

A dependency submission is one immutable complete-set operation:
- artifact identity/version/content digest;
- every direct source/parent edge;
- every transitive ancestor edge required by D policy;
- exact source MemoryRef/MemoryVersionRef and revision;
- Scope and provenance;
- complete-set digest and canonicalization profile.

E may stage bytes before D dependency commit, but staging remains private. If dependency commit response is lost, resolve the same DependencyRegistrationId + digest. A partial set, stale source revision, missing EventRef mapping or changed Scope yields INCOMPLETE/CONFLICT and no publication capability.

## 6. Attempt, lease and retry semantics

- Queue is at-least-once delivery, not authority.
- Logical retry preserves ProducerWorkItemId and request digest.
- Every attempt receives a fresh AttemptId/LeaseId/LeaseEpoch.
- Old attempts cannot register dependencies, publish, suppress a newer attempt or terminalize work.
- Same immutable publication operation transport retries and crash recovery reuse PublicationOperationId + tuple digest + all participant refs.
- After authoritative NO_PUBLICATION, a new attempt is a new immutable publication operation with new PublicationOperationId, participant refs, tuple digest and fresh D/I checks.
- A changed compiler input, source revision, model/schema/compiler config, output digest, dependency set or Scope creates a new DerivationRun/output identity and requires fresh D dependency and publication admission.
- DLQ is a queue state, never terminal proof. Replay must resolve the same logical work and current D/I policy; it cannot bypass a ForgetFence.

## 7. Terminal and output accounting

E must provide D with a durable inventory:
- every DerivationRun and Attempt;
- every staged artifact/version;
- every dependency registration;
- every publication operation and its resolved Storage outcome;
- every suppressed/quarantined output and proof that it cannot later publish;
- all retry, DLQ replay, outbox and delayed publisher paths.

Only D may issue D ProducerWork terminal receipt. E Published/Failed/Cancelled/Completed labels never imply D terminality. Any UNKNOWN participant or inventory gap keeps work open.

## 8. Restore and recovery

Restore starts in isolated non-serving mode:
1. Restore Storage participant/visibility records and DB incarnation proof.
2. Reconcile D producer ledger, RegistrationReceipt, Fence/high-water, dependency receipts and PublicationParticipantRefs.
3. Reconcile I current PolicyDomain policy/revocation/registry and in-flight authorization participants.
4. Reconcile E CompileIntent, DerivationRun, Attempt/Lease and output inventory.
5. Reconcile COC prefix and all other independently owned proofs where required by the wider restore contract.
6. Replay only idempotently by stable operation identity/digest. Unknown gaps remain quarantined.
7. Re-enable serving only after the independent D/I/Storage proofs agree.

Never infer terminality from missing queue rows, expired lease, process death, stale replica, absent receipt or age. Preserve the same immutable publication tuple across recovery of an in-flight operation.

## 9. E state transition outline

- INGRESS_ACCEPTED → D_REGISTRATION_PENDING → D_REGISTERED
- D_REGISTERED → QUEUED → LEASED → RUNNING
- RUNNING → PRIVATE_STAGED → DEPENDENCY_PENDING → DEPENDENCY_COMPLETE
- DEPENDENCY_COMPLETE → STORAGE_PREPARED_HIDDEN → D_PUBLICATION_ADMITTED
- D_PUBLICATION_ADMITTED → I_COMMIT_WON (or REVOCATION_WON / UNKNOWN)
- I_COMMIT_WON → STORAGE_COMMIT_PENDING → COMMITTED_VISIBLE (or NO_PUBLICATION / UNKNOWN)
- UNKNOWN → RECONCILIATION_REQUIRED (never auto-abort)
- local output disposition → D_TERMINAL_PENDING → D_TERMINAL_CONFIRMED

These are E orchestration labels. They do not replace owner receipts or owner authority states.

## 10. Required E tests

- D registration ACK loss before enqueue: no dispatch until same ID resolves.
- EventRef-only with complete/incomplete lineage.
- At-least-once duplicate queue delivery.
- Stale lease attempts attempting dependency registration/publication.
- Crash during complete dependency-set registration.
- Crash after Storage prepare before D admission.
- D admission ACK loss.
- I revocation-first and COMMIT_WON-first.
- Storage visibility ACK loss.
- NO_PUBLICATION followed by new publication attempt with new operation identity.
- Restore with missing/contradictory D/I/Storage records.
- DLQ replay and delayed publisher after terminalization attempt.

## 11. Open E decisions

Exact D/I/Storage callable API schemas, H wire encoding/signatures, lease epoch authority, source lineage canonicalization, retention horizons and conformance implementation remain OPEN.

## 12. 中文规范

### 12.1 E 权威边界
E 管理 CompileIntent、入口 Receipt、不可变 Compiler Input Bundle、DerivationRun、Attempt/Lease 生命周期、Private Staging、完整 Output/Dependency 提交和 Compiler Recovery Orchestration。E 不签发 D ProducerClass、D RegistrationReceipt、D PublicationParticipantRef、I Authorization、Storage Visibility Outcome 或 Global Forget Terminality。Queue ACK、E AcceptedReceipt、本地 Published/Completed 和对象存储存在性均不是跨 Owner 证明。

### 12.2 生命周期
E 先持久化入口和稳定 WorkItem 身份，再取得 D RegistrationReceipt；之后才能 Queue/Lease/Protected Source Dereference/Execute。冻结单次 DerivationRun 的精确输入包。输出先进入 Private Stage。EventRef-only 必须在 Dependency Registration/Publish 前关联精确 Canonical MemoryRef/MemoryVersionRef 与 Revision。完整 Direct/Transitive Dependency Set 作为单一不可变操作登记。之后严格按 Storage Prepare → D Publication Admission → I 单次 Sequencer Consumption → Storage Final Visibility Commit → D/I 独立 Closeout 执行。

### 12.3 重试与身份
同一操作的 Transport Retry、Lost ACK Resolution、Crash Recovery 必须复用 Operation ID、Tuple Digest 和 Participant Refs。逻辑 Work Retry 保持 ProducerWorkItemId/Request Digest，但 AttemptId/LeaseId/LeaseEpoch 更新。权威 NO_PUBLICATION 后的新发布尝试必须分配新的 PublicationOperationId、Participant Refs 和 Tuple Digest。任何 Source Revision、Dependency Set、Scope、Compiler Input/Config 或 Artifact Digest 变化都需要新的不可变 Run/Output Identity 与新 Gate。

### 12.4 终态与恢复
E 必须提交所有 Run、Attempt、Stage、Dependency、Publication、Suppressed/Quarantined Output、Retry、DLQ、Outbox 和 Delayed Publisher 的完整 Inventory。仅 D 可签发 ProducerWork Terminal Receipt。Restore 先隔离，再独立核对 Storage、D、I、E 及所需 COC Proof；未知状态保持 Quarantine。不得由队列缺行、Lease 过期、进程死亡或陈旧副本推断终态。

### 12.5 未决事项
D/I/Storage Callable API、H Wire Encoding/Signature、Lease Epoch 权威、Lineage Canonicalization、Retention 和 Conformance 实现仍 OPEN。本提案不构成 Schema Freeze 或实现通过。
