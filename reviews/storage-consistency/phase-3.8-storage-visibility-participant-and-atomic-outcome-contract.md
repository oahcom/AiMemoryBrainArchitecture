# Phase 3.8 — Storage Visibility Participant and Atomic Outcome Contract

- Owner role: Storage Consistency / Forget Atomicity
- Status: **Storage-role logical transaction proposal; physical topology and implementation proof OPEN**
- Related: Issue #25; A Phase 3.8.1 contract-surface addendum
- English and Chinese are normative peers.

## 1. Storage authority boundary

Storage owns durable records, transaction isolation/serialization, idempotency enforcement, private staging boundary, authoritative visibility pointer, visibility outcome proof, outbox commit and crash/failover/restore mechanics.

Storage does not mint D ProducerClass eligibility, D RegistrationReceipt, D ForgetFence/PublicationParticipantRef, I authorization/PermissionEpoch/CommitAuthorizationReceipt, E work/attempt semantics, C ParticipantIntentRef or global Forget completion.

Storage may provide the physical transaction substrate for D semantics; it does not become the semantic D authority merely because records share a database.

## 2. Logical records

### 2.1 StorageVisibilityParticipant

Minimum immutable fields:
- storage_visibility_participant_ref
- publication_operation_id
- publication_request_digest and publication_tuple_digest
- producer_work_item_id, DerivationRunId, AttemptId, LeaseId, LeaseEpoch
- artifact_ref, artifact_version, artifact_content_digest
- dependency_registration_receipt_ref and complete_dependency_set_digest
- exact ScopeRef and lineage digest
- private_stage_ref / immutable private object version
- storage_authority_ref and database-incarnation/serialization-domain ref
- state PREPARED_HIDDEN | COMMITTED_VISIBLE | NO_PUBLICATION | UNKNOWN
- storage_transaction_ref, record_version, created_at

Prepare is durable but invisible. It creates no public pointer, signed serving URL, index event or cache-visible entry. StorageVisibilityParticipantRef is not Storage PreparedParticipantRef/GID/XID from JF-10.

### 2.2 StorageVisibilityOutcome

Minimum immutable fields:
- publication_operation_id and publication_tuple_digest
- exact StorageVisibilityParticipantRef
- exact D PublicationParticipantRef
- exact I CommitAuthorizationReceiptRef / ITerminalProofRef
- outcome COMMITTED_VISIBLE | NO_PUBLICATION | UNKNOWN
- visibility_transaction_ref and visibility_pointer_ref (pointer required only for COMMITTED_VISIBLE)
- D current participant/fence proof reference
- I terminal authorization proof reference
- outbox_event_ref and outcome_digest
- commit timestamp and storage authority/incarnation identity

Outcome is immutable. Conflicting terminal outcomes are an integrity incident and must quarantine.

## 3. PrepareVisibility operation

Input: immutable publication tuple, private stage identity, complete dependency receipt/digest, exact work/attempt/lease tuple.

Atomic durable prepare:
1. Authenticate the caller and verify it is authorized to stage this operation under the Storage API boundary.
2. Resolve PublicationOperationId idempotency. Same ID + same tuple digest returns the same participant. Same ID + changed digest returns IMMUTABLE_IDENTITY_CONFLICT.
3. Verify the private stage exists as an immutable private object/version and cannot be served through public read paths.
4. Persist StorageVisibilityParticipantRef and the complete immutable tuple/ledger row.
5. Commit durable PREPARED_HIDDEN state before returning success.

The response is a Storage durability receipt, not D admission, I authorization or visibility permission. If ACK is lost, resolve the same PublicationOperationId + tuple digest. Do not create another participant.

D admission is prohibited until Storage can authoritatively read back this exact participant as durable PREPARED_HIDDEN.

## 4. D and I participant binding

After PrepareVisibility:
- D admits PublicationParticipantRef bound to the exact StorageVisibilityParticipantRef and same publication tuple.
- I consumes CommitAuthorizationReceipt in its own PolicyDomain sequencer, bound to the exact D and Storage refs.
- Storage must persist the returned exact D/I proof references into the publication ledger before final visibility commit.

Storage must reject participant substitution, cross-operation refs, changed digest, stale attempt/lease, incomplete dependency receipt or Scope mismatch.

The order is strictly Storage Prepare → D Admission → I Consumption. A crash after Storage Prepare but before D admission leaves an orphan private Storage participant. It has no visibility path and is retained for same-ID reconciliation. A crash after confirmed D admission with missing Storage participant is UNKNOWN/ledger inconsistency, never abort.

## 5. CommitVisibility operation

The final visibility transaction is the only visibility linearization point. It must execute under a D/Storage-approved serialization mechanism and atomically:
1. Resolve PublicationOperationId + tuple digest; exact replay returns the immutable original outcome.
2. Verify Storage participant is PREPARED_HIDDEN and exact.
3. Verify exact active D PublicationParticipantRef and current D fence/participant proof.
4. Verify exact I terminal authorization proof, including PolicyDomain, tuple, both participant refs, COMMIT_WON and current proof/key status at the final gate.
5. Verify artifact/version/content digest, complete dependency set, Scope and current attempt/lease fencing.
6. Atomically install authoritative visibility pointer, immutable PublicationReceipt/outcome and outbox event.
7. Persist COMMITTED_VISIBLE outcome and commit identity in the same transaction.

No read path may expose the artifact before this transaction commits. Object-store existence/listing, signed URL, cache warming, index event, queue message or outbox delivery is not visibility.

If any predicate fails authoritatively before commit, Storage may persist NO_PUBLICATION only if it proves no pointer was installed and no delayed worker/outbox/retry can later install it. If commit outcome cannot be proven, return/retain UNKNOWN and keep artifact private.

## 6. NO_PUBLICATION proof

A terminal NO_PUBLICATION proof must bind the exact publication tuple and Storage participant and prove:
- no authoritative visibility pointer was installed;
- no publication transaction remains prepared or unresolved;
- all writers, staged publishers, retries, delayed workers and outbox handlers for this operation are fenced or durably incapable of publishing;
- no conflicting COMMITTED_VISIBLE record exists;
- recovery/restore will preserve this terminal disposition.

A timeout, failed RPC, missing row, expired lease, process death or object age is not NO_PUBLICATION.

## 7. Serialization and topology decision

Candidate preferred topology: one serializable transaction domain per Canonical Memory authority covering D registration/fence high-water, complete dependency registration, D publication participant admission and final visibility pointer/outcome. This is a recommendation, not a deployed decision.

If D semantic records and Storage visibility live in separate services, D and Storage must approve a durable prepare/commit or equivalent linearizable coordinator protocol. It must prove:
- one order for RegisterProducerWork vs InstallForgetFence;
- complete-set dependency commit;
- D PublicationParticipant admission vs Fence;
- final visibility commit vs current D fence;
- response-loss recovery by stable operation ID/digest;
- failover/restore continuity and hidden-on-UNKNOWN;
- no split-brain visibility pointer or dual terminal outcome.

Process-local mutexes, queue order, eventual replicas, outbox-only coordination, check-then-write and reusable D tokens are insufficient.

I's PolicyDomain sequencer remains an independent authority. Storage must validate the exact I proof at the actual visibility commit; it must not compare PermissionEpoch numerically with D or Storage positions.

## 8. Crash/failover/restore

- Before prepare commit: no participant and no visibility.
- After prepare before D admission: durable orphan PREPARED_HIDDEN, private.
- D admission ACK unknown: resolve same D operation; do not create another participant.
- After D admission, Storage row missing: UNKNOWN/ledger inconsistency; hold D/I barriers.
- I REVOCATION_WON: no visibility; prove NO_PUBLICATION before closeout.
- I COMMIT_WON: preserve in-flight participant until Storage terminal outcome.
- Visibility commit ACK lost: same operation lookup; do not infer abort.
- Database failover/incarnation mismatch: quarantine until authoritative ledger and transaction continuity is proven.
- Restore: all pointers/artifacts non-serving until D fence/lineage and I current policy/revocation plus Storage participant/outcome reconcile.

## 9. Required Storage tests

- Duplicate PrepareVisibility same/different digest.
- Prepare ACK loss and recovery.
- Orphan private participant before D admission.
- D admission attempted without durable Storage participant.
- Exact D/I participant substitution and cross-operation mismatch.
- D fence-first / participant-first.
- I revocation-first / COMMIT_WON-first.
- CommitVisibility atomic pointer + receipt + outbox.
- Visibility ACK loss and same-operation resolution.
- NO_PUBLICATION delayed worker/outbox exclusion.
- Split-brain/failover and DB incarnation mismatch.
- Restore with missing or contradictory D/I/Storage proof.
- Duplicate outbox delivery and terminal immutability.

Every test asserts actual pointer visibility, durable participant/outcome rows, D barrier and I revocation state.

## 10. Open Storage decisions

Actual DB/coordinator product, transaction isolation mode, serialization authority ownership, multi-service protocol, commit proof format, read-path enforcement, outbox guarantees, failover/restore topology and conformance results remain OPEN.

## 11. 中文规范

### 11.1 Storage 权威边界
Storage 拥有持久化记录、事务隔离/序列化、幂等约束、Private Staging 边界、权威 Visibility Pointer、Visibility Outcome Proof、Outbox Commit 和 Crash/Failover/Restore 机制。Storage 不签发 D ProducerClass/RegistrationReceipt/ForgetFence/PublicationParticipantRef，也不签发 I Authorization/PermissionEpoch/CommitAuthorizationReceipt。共享数据库不会让 Storage 自动成为 D 语义权威。

### 11.2 PrepareVisibility
Storage 必须先验证不可变 Private Stage，再按 PublicationOperationId + Tuple Digest 幂等创建持久化 PREPARED_HIDDEN StorageVisibilityParticipantRef。相同 ID/摘要返回原 Participant；相同 ID 不同摘要返回 IMMUTABLE_IDENTITY_CONFLICT。Prepare 成功只证明 Storage 持久化，不是 D Admission、I Authorization 或 Visibility Permission。ACK 丢失时使用同 ID/摘要解析。D 只能在 Storage 权威回读确认 Participant 已持久化后准入。

### 11.3 D/I 绑定
Storage Prepare 后，D 准入绑定精确 Storage Participant 的 PublicationParticipantRef；I 在 PolicyDomain Sequencer 消费绑定精确 D/Storage Participant 的 CommitAuthorizationReceipt。Storage 最终提交前必须持久化精确 D/I Proof Ref。任何 Participant 替换、跨 Operation 引用、Digest 变化、Stale Attempt/Lease、Dependency 不完整或 Scope 不一致均拒绝。

### 11.4 CommitVisibility
最终 Visibility Transaction 是唯一 Visibility Linearization Point，必须原子验证 Storage PREPARED_HIDDEN、D 当前 PublicationParticipant/Fence、I Terminal Authorization Proof、Artifact/Version/Digest、完整 Dependency、Scope 和当前 Attempt/Lease，并提交 Visibility Pointer、PublicationReceipt/Outcome、Outbox。提交前所有 Read Path 必须 Private。对象存在、Signed URL、Cache、Index Event、Queue 或 Outbox Delivery 都不是 Visibility。无法证明提交结果时为 UNKNOWN，Artifact 保持 Private。

### 11.5 NO_PUBLICATION
NO_PUBLICATION 必须正向证明没有 Pointer、没有 Prepared/Unresolved Publication、所有 Writer/Stage Publisher/Retry/Delayed Worker/Outbox Handler 已被 Fence 或永久不能发布、没有冲突 COMMITTED_VISIBLE，且 Restore 保留该终态。超时、RPC 失败、行缺失、Lease 过期、进程死亡或对象年龄都不是 NO_PUBLICATION。

### 11.6 拓扑与恢复
每个 Canonical Memory Authority 一个 Serializable Transaction Domain 是候选建议，不是部署决定。若 D/Storage 分服务，必须批准 Durable Prepare/Commit 或等效 Linearizable Coordinator，并证明 Registration/Fence、Dependency、D Participant/Fence、Final Visibility、ACK Loss、Failover/Restore 顺序一致。I PolicyDomain Sequencer 仍独立，Storage 必须在实际 Commit 验证精确 I Proof，禁止跨域比较 PermissionEpoch。

### 11.7 未决事项
数据库/Coordinator 产品、隔离级别、序列化权威归属、跨服务协议、Commit Proof 格式、Read Path Enforcement、Outbox、Failover/Restore 拓扑和 Conformance 结果仍 OPEN。本提案不构成部署或实现通过。
