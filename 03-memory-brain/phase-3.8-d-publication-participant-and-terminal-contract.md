# Phase 3.8 — D Publication Participant and Terminal Contract

- Owner role: D — Memory Brain / ForgetFence authority
- Status: **D-role proposal; exact Owner approval, callable API and conformance OPEN**
- Related: Issue #25; A Phase 3.8.1 contract-surface addendum
- English and Chinese are normative peers.

## 1. Authority boundary

D owns ProducerClass eligibility, ProducerWork admission, RegistrationReceipt, ProducerRegistrationSequence, ForgetFence ordering, complete dependency/lineage inventory, PublicationParticipantRef and producer/publication terminality.

D does not own I authorization, Storage persistence/visibility, E queue/lease execution, H wire encoding, C ParticipantIntentRef or Storage PreparedParticipantRef/GID/XID.

A D receipt proves only the D decision it names. It is never an independent Storage write capability.

## 2. Required nominal types

The following identities MUST NOT alias:
- ProducerWorkItemId
- ProducerRegistrationSequence
- ForgetOperationRef / ForgetFenceGeneration
- DependencyRegistrationId / DependencyRegistrationReceiptRef
- PublicationOperationId
- D PublicationParticipantRef
- D PublicationReceiptRef / D TerminalReceiptRef
- StorageVisibilityParticipantRef
- I CommitAuthorizationReceiptRef
- C ParticipantIntentRef
- Storage PreparedParticipantRef / PreparedTransactionGID / XID
- AttemptId / LeaseId / LeaseEpoch

D-local positions are opaque and meaningful only in the D authority domain. They are never compared numerically with I PermissionEpoch or Storage transaction positions.

## 3. PublicationParticipantRef logical contract

D's PublicationParticipantRef is a durable in-flight barrier participant, not a PublicationReceipt and not visibility permission.

Minimum immutable binding:
- publication_participant_ref
- publication_operation_id
- canonical publication_request_digest
- publication_tuple_digest
- exact storage_visibility_participant_ref
- producer_work_item_id and exact D RegistrationReceiptRef
- producer_class_id and immutable producer_class_version
- derived_artifact_ref, immutable artifact_version and artifact_content_digest
- dependency_registration_receipt_ref and complete_dependency_set_digest
- exact ScopeRef and source/target lineage digest
- DerivationRunId, AttemptId, LeaseId and LeaseEpoch
- D-local fence_generation and admission_position
- participant_state and record_version

D MUST reject admission unless Storage has authoritatively confirmed the exact StorageVisibilityParticipantRef is durably PREPARED_HIDDEN and bound to the same PublicationOperationId and tuple digest. D does not infer Storage durability from a caller assertion or transport ACK.

## 4. AdmitPublication operation

Input:
- immutable PublicationTuple and digest
- exact StorageVisibilityParticipantRef
- D RegistrationReceiptRef
- complete DependencyRegistrationReceiptRef
- authenticated caller/workload context

Atomic D decision:
1. Authenticate caller and resolve ProducerClass/version.
2. Resolve PublicationOperationId idempotency: same ID+same tuple digest returns original result; same ID+different digest is IMMUTABLE_IDENTITY_CONFLICT.
3. Verify D RegistrationReceipt and WorkItem identity.
4. Verify complete dependency receipt, exact source revisions, transitive lineage digest and Scope.
5. Verify current AttemptId/LeaseId/LeaseEpoch; stale attempts are rejected.
6. Verify Storage's durable hidden participant evidence and exact tuple binding.
7. Linearize against InstallForgetFence in D's authoritative ordering domain.
8. If a covering Fence wins first, return FENCE_WON / REJECTED and do not create an active participant.
9. If admission wins, persist an unresolved PublicationParticipantRef in the D barrier and return it. This is an ordering hold only, not permission to publish.

The D admission commit is the D-side linearization point. It does not linearize Storage visibility.

## 5. D fence behavior

- Fence-first: publication admission is rejected/quarantined and Storage cannot commit visibility.
- Publication-participant-first: the participant is unresolved; a later Fence may be recorded but cannot become effective past the participant until Storage proves COMMITTED_VISIBLE or authoritative NO_PUBLICATION.
- UNKNOWN/IN_DOUBT: participant remains active and the affected Fence remains held.
- No timeout, lease expiry, process death, missing row, queue deletion or age-based cleanup can terminalize the participant.

## 6. Terminalization operations

D accepts exactly two terminal Storage outcomes for an admitted publication:

### COMMITTED_VISIBLE
D verifies:
- exact Storage participant and PublicationOperationId;
- exact publication tuple digest;
- exact artifact/version/content digest;
- authoritative Storage visibility transaction and pointer proof;
- exact D participant was active and accounted;
- no conflicting outcome exists.

D then records immutable D PublicationReceipt/terminal evidence and accounts the derivative in ForgetFence inventory.

### NO_PUBLICATION
D verifies positive authoritative evidence that:
- no visibility pointer was installed;
- no outbox, retry, delayed publisher, staged writer or replay can later install it;
- exact Storage participant and tuple digest match;
- no conflicting COMMITTED_VISIBLE outcome exists.

D closes the participant without a derivative publication.

### UNKNOWN / IN_DOUBT
No terminal receipt. Keep D participant and Fence held. Missing Storage state after confirmed D admission is ledger inconsistency, not abort.

D terminalization is idempotent by PublicationParticipantRef + Storage outcome digest. A conflicting terminal outcome is an immutable integrity incident and must quarantine.

## 7. Producer terminality remains separate

CompleteProducerWork is not implied by one publication terminal result. D may close a ProducerWork barrier only after all attempts, outputs, dependencies, publications, retries, DLQ replays, outbox deliveries and delayed publishers are accounted, with no UNKNOWN participant or inventory gap.

## 8. Error vocabulary

- FENCE_WON
- PRODUCER_NOT_REGISTERED
- PRODUCER_CLASS_DISABLED_OR_UNKNOWN
- INCOMPLETE_DEPENDENCY_SET
- LINEAGE_OR_SCOPE_MISMATCH
- STORAGE_PARTICIPANT_NOT_DURABLE
- STORAGE_PARTICIPANT_BINDING_MISMATCH
- STALE_ATTEMPT
- IMMUTABLE_IDENTITY_CONFLICT
- REPLAY_OF_TERMINAL_OPERATION
- UNKNOWN / IN_DOUBT

Errors must be typed and stable. Unknown must never be translated into retryable abort.

## 9. Required D proof obligations

D must publish deterministic tests for:
1. RegisterProducerWork vs InstallForgetFence both commit orders.
2. EventRef-only valid and invalid admission.
3. Dependency complete-set atomicity and source revision mismatch.
4. Storage participant missing/non-durable at D admission.
5. D admission ACK loss and same-ID resolution.
6. Fence after active PublicationParticipantRef.
7. Storage COMMITTED_VISIBLE / NO_PUBLICATION / UNKNOWN closeout.
8. Stale AttemptId/LeaseId/LeaseEpoch.
9. Conflicting Storage outcome and restore ledger gap.

Each test asserts D ledger rows, fence high-water/state, participant state and exact receipt digests.

## 10. Open D decisions

- Exact canonical serialization and digest profile: H + D.
- Exact D receipt signature/issuer and key lifecycle: D + H + I boundary.
- Callable API/transport error mapping: D + H.
- D/Storage physical serialization authority and failover proof: D + Storage.
- Independent D Owner approval and conformance evidence: OPEN.

## 11. 中文规范

### 11.1 权威边界
D 拥有 ProducerClass 资格、ProducerWork 准入、RegistrationReceipt、ProducerRegistrationSequence、ForgetFence 顺序、完整依赖/Lineage Inventory、PublicationParticipantRef 及 Producer/Publication 终态。D 不拥有 I 授权、Storage 持久化/可见性、E Queue/Lease 执行、H Wire 编码、C ParticipantIntentRef 或 Storage PreparedParticipantRef/GID/XID。

### 11.2 PublicationParticipantRef
D PublicationParticipantRef 是持久化的进行中 Barrier Participant，不是 PublicationReceipt，也不是 Visibility Permission。它必须绑定 PublicationOperationId、规范 Request Digest、Tuple Digest、精确 StorageVisibilityParticipantRef、ProducerWorkItemId、D RegistrationReceipt、ProducerClass/Version、Artifact/Version/Digest、完整 Dependency Receipt/Digest、Scope、Source/Target Lineage、DerivationRunId、AttemptId、LeaseId/LeaseEpoch，以及 D-local FenceGeneration/AdmissionPosition。

D 只有在 Storage 权威确认精确 Storage Participant 已持久化为 PREPARED_HIDDEN 且 Tuple 一致后，才可准入。调用者声明或 Transport ACK 不能证明 Storage 持久化。

### 11.3 准入与 Fence
D 在自己的权威顺序域中原子验证 Registration、完整依赖、Lineage、Scope、当前 Attempt/Lease、Storage Durable Participant，并与 InstallForgetFence 线性化。Fence-first 必须拒绝。PublicationParticipant-first 则保持未解决并阻止后续 Fence 越过，直到 Storage 提供 COMMITTED_VISIBLE 或权威 NO_PUBLICATION。UNKNOWN/IN_DOUBT 永远保持 Barrier 开放。

### 11.4 终态
COMMITTED_VISIBLE 必须验证精确 Storage Participant、Operation/Tuple Digest、Artifact/Version、Visibility Pointer 和当前 D Participant；随后签发不可变 D PublicationReceipt 并纳入 ForgetFence Inventory。NO_PUBLICATION 必须正向证明无 Pointer、无 Outbox/Retry/Delayed Publisher/Replay 能在之后发布。UNKNOWN 不得终态化。D ProducerWork Terminal 仍需核清所有 Attempt、Output、Dependency、Publication、Retry、DLQ、Outbox 和延迟 Publisher。

### 11.5 未决事项
规范序列化/摘要、签名与 Key Lifecycle、Callable API/Wire Error Mapping、D/Storage 物理事务域及独立 D Owner 批准和符合性证据仍 OPEN。本提案不构成 Schema Freeze 或实现通过。
