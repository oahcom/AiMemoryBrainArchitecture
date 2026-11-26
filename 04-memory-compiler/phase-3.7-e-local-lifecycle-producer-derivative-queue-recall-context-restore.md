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
    canonical_scope: "E-domain Memory Compiler record phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md; canonical placement pending Owner acceptance."
    canonical_scope_id: "memory-compiler/e-phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---



# Phase 3.7 — E Local Lifecycle: Producer, Derivative, Queue, Recall, Context and Restore

- Owner: E — Memory Compiler
- Branch: `session-e-memory-compiler-2026-11-16`
- Status: **E-local semantic proposal; D/E/Storage publication gate and cross-owner schemas remain OPEN / NOT VERIFIED**
- Scope: source-event ingestion, compiler work, derived artifact production, compiler queues/outboxes, compiler source recall, compiler input context and restore.
- Authority boundary: D owns canonical Memory, ForgetFence, producer registry and dependency inventory; I owns authorization/PermissionEpoch; E owns compilation; F owns runtime retrieval/index projections; G owns user-facing Context and Applied/Delivery; H owns wire/adapter capability; Storage owns agreed durable transaction/visibility realization.

## 1. E's local lifecycle model

E is a derivative producer, not the canonical authority. Accepted input, compiler completion and a locally stored artifact do not make an artifact visible.

| Object | E-local states | Terminal / non-terminal meaning |
|---|---|---|
| Producer intent | Received → Validating → Accepted → RegistrationPending → Registered → Queued → Leased → Running → Staged → DependencyRegistered → GatePending → Published / Suppressed / Rejected | Dead-letter, timeout, lease expiry and worker loss are non-terminal until no-publication disposition is durable |
| Derivation | Planned → Executing → CandidateProduced → Validated → PrivateStaged → LineageBound → PublicationPending → Published / Quarantined / Discarded | Every recompile is a new DerivationRun; prior outputs remain immutable |
| Queue/outbox | Enqueued → Leased → Dispatched → Acked / Retry / DLQ / Cancelled | Queue ACK is not compiler success, canonical commit, publication or D barrier closure |
| Source recall | Requested → Authorized → SourceResolved → EvidenceBound → ReturnedToCompiler / Blocked | Compiler source recall is not user Recall and never bypasses D/I checks |
| Compiler input context | Assembled → ProvenanceChecked → ScopeChecked → Budgeted → FrozenForRun → Consumed / Invalidated | E's run input bundle is not G ContextVersion or F Working Set |
| Restore unit | Discovered → Isolated → PrefixReconciled → LedgerReconciled → ReplayValidated → PrivateRebuilt → PublicationGate → Enabled | No restored staged artifact/outbox is exposed before reconciliation |

## 2. Producer behavior

1. E registers each derivative-capable logical work item with D before queue insertion, lease, source dereference or execution. Required binding: stable ProducerWorkItemId, producer class/identity, CompileIntentId, source EventRef(s)/exact Memory refs, ScopeRefs, complete known lineage, request digest, admission CanonicalCommitCursor, observed ForgetFence and I PermissionEpoch.
2. AcceptedReceiptId proves E durable ingress only; it does not prove D producer registration. Registration uncertainty is resolved by stable WorkItemId+digest.
3. Retry preserves ProducerWorkItemId and request digest; AttemptId and LeaseId change. Recompile creates a new DerivationRunId and immutable output version, with fresh authorization/fence checks and a D-governed registration relation. It cannot escape the original source lineage or Forget barrier.
4. Every terminal outcome is explicit and durable: Published, RejectedBeforeAdmission, CancelledNoPublication, SuppressedByFence, FailedNoPublication or other D-approved disposition. DLQ, timeout, retry exhaustion and process death are not terminal.
5. D's pre-fence producer high-water remains open until D accepts terminal/no-publication evidence. E cannot remove registrations or self-close the barrier.
6. Unknown D/I authority or registration outcome fails closed; do not execute derivative-capable work speculatively.

## 3. Derivative behavior

- Derivatives include normalized claims, extracted entities/relations, evidence spans, summaries, embeddings, provenance edges, compiler proposals, staged canonical candidates, and any durable outbox/cache artifact that can later expose or regenerate source-derived content.
- Each immutable DerivedArtifactRef/version binds ProducerWorkItemId, DerivationRunId, source EventRef and exact source versions, complete transitive lineage, provenance, Scope, policy epoch, schema/model/compiler versions and content digest.
- Keep candidate outputs private/non-queryable until dependencies are durably registered with D and the authoritative publication gate succeeds against the current D fence and I permission.
- A derivative whose dependency set is incomplete, ambiguous or unresolvable is quarantined, not partially published.
- Same dependency-registration key+same digest is idempotent; same key+different digest is conflict. No mutable overwrite of a published artifact; changed output creates a new immutable version.
- Forget/revocation causes immediate logical suppression of affected artifacts, blocks late publication, and initiates governed cleanup. E cannot claim F index purge, G Context removal, physical byte erasure or global completion.

## 4. Queue and outbox behavior

- Queue entries are durable references to registered work, not authorization. The payload binds WorkItemId, digest, source refs, lineage digest, Scope, schema and attempt/lease generation.
- At-least-once dispatch is expected. Stable identity+digest deduplicates; changed digest conflicts. Stale leases cannot publish.
- D registration must precede enqueue. If queue insertion succeeds but registration is uncertain, quarantine and resolve by stable identity; never run.
- Retry/DLQ preserves the open producer registration. A new attempt is not a new logical work item.
- Before execution, source reads, dependency registration and publication, revalidate current I PermissionEpoch and D fence. A final gate must serialize with visibility; local check-then-publish is forbidden.
- Restore quarantines queue/outbox records until COC prefix, D producer ledger/high-water, I policy and Storage participant/visibility records reconcile. Unknown gaps block replay.

## 5. Recall behavior

- E's Recall is narrowly defined as compiler source/evidence resolution: fetch exact authorized EventRef/MemoryVersionRef and provenance required for a specific DerivationRun.
- It is not interactive/user recall, ranking, context delivery or an authorization grant. F owns runtime retrieval; G owns Context selection.
- Every source read is bound to authenticated producer identity, purpose, Scope, I PermissionEpoch and D fence; revalidate source lifecycle and lineage before dereference.
- Resolve exact source revisions. Do not silently float a reference to a newer version or substitute a preferred claim. Superseded/retracted/forgotten/unauthorized sources are blocked or explicitly classified.
- Incomplete source coverage is recorded as incomplete; absence in a search/index result is not proof that a source does not exist.
- Evidence/provenance remains attached through extraction, normalization, consolidation and output. Compiler outputs cannot promote untrusted source text into privileged instructions.

## 6. Context behavior

- E owns only the immutable compiler input bundle for one DerivationRun: selected source refs, evidence/provenance, exact versions, Scope, policy epoch, compiler/model/schema versions, budget and deterministic input digest.
- Freeze the input bundle before execution. Any changed source, permission, fence, schema or model configuration requires a new run identity/input digest and fresh validation.
- This bundle is not G's desired Context, ContextVersion, Snapshot/Delta, Delivery or Applied record, and not F's retrieval Working Set.
- E may request source candidates from F or provide validated derived refs to G; F decides retrieval mechanics, G decides Context membership and delivery. E cannot declare a user-facing recall result or Applied state.
- No cross-Scope mixing. If source provenance or scope is uncertain, do not compile/publish.

## 7. Restore and replay

1. Restore event log, compiler state, staged artifacts, queue/outbox and dependency manifests into quarantine/private storage.
2. Verify Storage restore/participant evidence and reconcile the COC committed prefix, D producer registration/dependency high-waters and I PermissionEpoch/revocation/registry state. These are separate typed authorities.
3. Preserve the same CompileIntentId, ProducerWorkItemId, request digest, PublicationOperationId, PreparedParticipantRef and PreparedTransactionGID where a prepared publication exists. AttemptId/LeaseId may change; immutable transaction tuple may not.
4. Resolve every in-flight item by stable identity. Never infer completion from missing queue message, expired lease, absent receipt or stale replica.
5. Revalidate source revisions, complete lineage, Scope, policy, ForgetFence and model/schema compatibility. Rebuild only private artifacts.
6. Re-register/reconcile dependencies idempotently; final publication must pass the current D/I gate. If pointer/receipt/GID/authority disagree, remain quarantined.
7. Reconcile post-restore events before opening queue consumers or exposing artifacts. Unknown continuity means no replay/no publication.
8. A RestoreReconciliationReceipt is not a PublicationReceipt, D clearance, I authorization, COC terminal decision or global Forget completion.

## 8. Evidence and tests

E emits AcceptedReceipt, producer registration receipt reference, immutable run/attempt identities, source/input digest, dependency receipts, publication operation/result, terminal no-publication disposition, queue state and restore reconciliation outcome. D alone closes its barrier; Storage alone supplies its agreed transaction evidence.

Required tests: register-before-enqueue crash; enqueue-before-ACK; duplicate delivery and changed digest; stale lease publication; retry/DLQ across Forget fence; incomplete transitive lineage; revocation during compilation; gate-vs-fence race; restore with stale prefix/participant ledger; recompile after source supersession; unknown GID resolution. These are required specifications, not claims of executed tests.

## 9. Non-goals / blockers

- E does not own canonical truth, Forget decisions, user-facing Recall, F indexes, G Context/Applied, H ACK or I authorization.
- D/E/Storage atomic registration/dependency/final publication gate remains **BLOCKING** until callable schemas and crash-safe linearization are agreed and verified.
- **No compiler implementation, conformance PASS, production restore or publication activation is claimed.**


## 10. Phase 3.7 cross-owner reconciliation amendments (EN)

**Disposition:** E-local amendment proposal for LIF-01/02/04/05/08/09/10. D's §8 EventRef-only registration rule is the controlling D decision for this proposal set; E consumes that rule but does not mint D admission.

### 10.1 ProducerClass and EventRef-only ingress
- E's local producer taxonomy is not an admission grant. Every derivative-capable CompileIntent MUST be covered by a D-issued, versioned, enabled ProducerClass registration specifying owner, accepted source-reference classes, output/derivative classes and permitted capabilities (normal, replay, rebuild, cleanup-only).
- E ingress acceptance (AcceptedReceipt) and D producer admission (RegistrationReceipt) are distinct and neither substitutes for the other.
- **EventRef-only ingress follows D §8 and is eligible for D registration before Canonical MemoryRef exists** only when authenticated producer, enabled ProducerClass/version, exact Scope, canonical request digest and D-approved opaque lineage token/digest are complete. E MUST obtain the durable D RegistrationReceipt before queue/lease/execute. E MUST NOT treat the receipt as protected-payload authorization; current I authorization is separately required. Before dependency registration/publication, E MUST link exact Canonical MemoryRef/MemoryVersionRef identities and revisions to the original EventRef lineage. Missing/invalid bindings remain quarantined with no execution capability.

### 10.2 Derivation, retries and terminal disposition
- Retry preserves logical ProducerWorkItemId and request digest; AttemptId/LeaseId rotate. Recompile creates a new immutable DerivationRun/output version linked to predecessor/source lineage through a D-governed relation; it cannot shed prior dependencies or fences.
- E-local Published, Rejected, Cancelled, Failed, DLQ or Completed labels do not close a D producer barrier. E supplies durable no-later-publication evidence; D alone accepts terminal disposition and closes its barrier.
- Every source dereference, execution boundary, dependency registration and publication gate revalidates current I authorization and D fence/lineage. Historical permission or cached ALLOW is insufficient.

### 10.3 Restore and typed context
- Restore is gated by independent Storage participant/visibility and DB-incarnation proof, COC committed-prefix proof, I current policy/revocation/registry proof, D fence/lineage/producer/dependency proof and E compiler ledger/run/dependency proof. Preserve issuer-specific signatures and opaque positions; never synthesize a scalar restore high-water.
- Unknown prefix, prepared-publication tuple, GID, participant receipt, registration or dependency continuity leaves the affected run/artifact/outbox quarantined. Never infer completion from a missing queue row or stale replica.
- E's frozen compiler input bundle is a nominal type bound to one DerivationRun/digest, not F Working Set or G ContextVersion/Delivery/Applied.

## 10. Phase 3.7 跨 Owner 对齐修订（中文）

**处置：** 本节将 LIF-01/02/04/05/08/09/10 纳入 E 本地合同。EventRef-only ingress 仍由 D 决定并属于阻塞项；本节不虚构或预先批准 D 的决定。

### 10.1 ProducerClass 与仅含 EventRef 的入口
- E 本地 Producer 分类不构成准入授权。每个可产生 Derivative 的 CompileIntent 都必须由 D 的版本化、启用状态 ProducerClass 注册覆盖，并明确 Owner、允许的 SourceRef 类型、输出/Derivative 类型和能力（normal、replay、rebuild、cleanup-only）。
- E 持久化入口接收证明（AcceptedReceipt）与 D Producer 准入证明（RegistrationReceipt）必须区分，彼此不能替代。
- **仅含 EventRef 的入口遵循 D §8，可在 Canonical MemoryRef 形成前由 D 注册**，但前提是经认证 Producer、启用 ProducerClass/Version、精确 Scope、规范请求摘要及 D 批准的不透明 Lineage Token/Digest 完整。E 必须在 Queue/Lease/Execute 前取得持久化 D RegistrationReceipt。该 Receipt 不构成受保护 Payload 授权；仍须独立验证 I 当前授权。Dependency Registration/Publish 前，E 必须将精确 Canonical MemoryRef/MemoryVersionRef 身份和 Revision 关联到原 EventRef Lineage。缺失/无效绑定仍须隔离且不授予执行能力。

### 10.2 Derivation、重试与终态处置
- 重试保留逻辑 ProducerWorkItemId 和请求摘要，AttemptId/LeaseId 每次轮换。重新编译创建新的不可变 DerivationRun/输出版本，并通过 D 管理的关系关联前序运行/源 Lineage；不得丢弃旧依赖或 Fence。
- E 本地 Published、Rejected、Cancelled、Failed、DLQ 或 Completed 标签均不能关闭 D Producer Barrier。E 提供持久化的“不会再发布”证据；仅 D 有权接受终态处置并关闭 Barrier。
- 每次源解引用、执行边界、依赖注册和发布门都必须重新验证 I 当前授权及 D Fence/Lineage。历史权限或缓存 ALLOW 不足以授权。

### 10.3 Restore 与类型边界
- Restore 的 Serving/Publication 必须由独立证明共同满足：Storage participant/visibility 与 DB incarnation、COC committed prefix、I 当前 policy/revocation/registry、D fence/lineage/producer/dependency，以及 E compiler ledger/run/dependency。保留各签发者签名和不透明位置，禁止合成单一 Restore High-water。
- Prefix、prepared publication tuple、GID、participant receipt、registration 或 dependency 连续性任何一项未知，相关 Run/Artifact/Outbox 必须隔离。不得根据队列行缺失或陈旧副本推断完成。
- E 冻结编译输入包是绑定单一 DerivationRun 和摘要的独立名义类型，不是 F Working Set，也不是 G ContextVersion/Delivery/Applied。


## 8. Normative correction — EventRef-only work and D admission

This section supersedes the earlier §3.7 wording that EventRef-only ingress must remain outside D admission. D's controlling §3.2 permits registration before Canonical MemoryRef creation.

1. E creates stable CompileIntentId/ProducerWorkItemId and E AcceptedReceipt as local ingress evidence.
2. Before enqueue, lease, protected source dereference or derivative-capable execution, E invokes D RegisterProducerWork. D may accept an EventRef-only source when authenticated ProducerClass, Scope, request digest and D-approved opaque lineage token/digest are complete.
3. D acceptance yields durable RegistrationReceipt and ProducerRegistrationSequence. ACK-unknown is resolved by the same WorkItemId+digest; E does not dispatch while unresolved.
4. EventRef-only registration is included in D ForgetFence high-water and obeys D's two-outcome admission/fence linearization.
5. Before RegisterDerivedDependency or publication, E appends/links exact Canonical MemoryRef/MemoryVersionRef revisions to the original EventRef lineage. Incomplete/conflicting lineage remains private/quarantined and cannot publish.
6. D registration is not protected-payload authorization. E checks current I permission before each protected dereference and at final publication.
7. Missing identity, Scope, lineage token, registry or current authority means no queue/lease/execute capability.

### 中文规范

本节替代此前“EventRef-only 入口必须始终留在 D Admission 之外”的表述。D 既有权威 §3.2 允许 Canonical MemoryRef 形成前完成注册。

1. E 创建稳定 CompileIntentId/ProducerWorkItemId，并产生 E AcceptedReceipt 作为本地入口证据。
2. E 必须在入队、租约、受保护源读取或 Derivative-capable 执行前调用 D RegisterProducerWork。经认证 ProducerClass、Scope、请求摘要和 D 批准的不透明 Lineage Token/Digest 完整时，D 可以接受 EventRef-only Source。
3. D 接受后返回持久化 RegistrationReceipt 和 ProducerRegistrationSequence。ACK 未知时，E 必须用同一 WorkItemId+Digest 查询；未解决前不得 Dispatch。
4. EventRef-only Registration 同样纳入 D ForgetFence High-water，并遵循 D 的 Admission/Fence 两结果线性化规则。
5. RegisterDerivedDependency 或 Publish 前，E 必须把精确 Canonical MemoryRef/MemoryVersionRef Revision 追加关联到原 EventRef Lineage。Lineage 不完整或冲突时保持 Private/Quarantined，不得发布。
6. D Registration 不等于受保护 Payload 授权。E 必须在每次受保护源读取及最终 Publish Boundary 单独检查 I 当前授权。
7. 身份、Scope、Lineage Token、Registry 或当前权威状态缺失时，不得授予 Queue/Lease/Execute 能力。

## 9. D/E/Storage atomic registration-to-visibility consumption

E adopts D's nine-operation semantic contract and Storage's per-Canonical-Memory-authority shared serialization recommendation, subject to Storage proof. Required order:

E AcceptedReceipt → durable D RegistrationReceipt → Queue/Lease/Run → private immutable Stage → complete D DependencyRegistrationReceipt → D PublishDerivedIfFenceCurrent + Storage authoritative Visibility Commit → D CompleteProducerWork.

No queue/lease/execution before durable D registration. Retry preserves ProducerWorkItemId and request digest while AttemptId/LeaseId rotate. Recompile uses a new DerivationRunId and explicit D-linked child/re-admission decision, never resets lineage. Staged bytes remain private. Dependency set and lineage digest commit as one complete immutable unit. Visibility changes only at the authoritative atomic commit checking current D fence, I authorization, D registration, complete dependencies, active attempt/lease, Scope and exact artifact digest. ACK loss resolves by the same stable operation ID+digest; UNKNOWN keeps the artifact private and barrier open. Terminal closure requires D terminal receipt after all output/attempt/replay paths are accounted.

E rejects a D-approved message followed by unconstrained object-store write. If no shared ACID domain exists, E requires D+Storage-approved durable prepare/commit, one-time final visibility CAS, current-fence validation at commit, crash recovery and hidden-on-UNKNOWN behavior.

### 中文规范

E 采用 D 九项语义操作合同及 Storage 提出的每个 Canonical Memory Authority 一个共享序列化域作为目标实现，但以 Storage 物理证明为前提。强制顺序：

E AcceptedReceipt → 持久化 D RegistrationReceipt → Queue/Lease/Run → Private Immutable Stage → 完整 D DependencyRegistrationReceipt → D PublishDerivedIfFenceCurrent + Storage 权威 Visibility Commit → D CompleteProducerWork。

D Registration 持久化前不得 Queue/Lease/Execution。Retry 保持 ProducerWorkItemId 和请求摘要不变，AttemptId/LeaseId 轮换。Recompile 使用新 DerivationRunId 和明确的 D-linked Child/Re-admission 决策，不得重置 Lineage。Staged Bytes 必须保持 Private。Dependency Set 与 Lineage Digest 必须作为完整不可变单元提交。只有在权威原子提交中检查当前 D Fence、I 授权、D Registration、完整依赖、活动 Attempt/Lease、Scope 和精确 Artifact Digest 后，Visibility 才能改变。ACK 丢失必须用同一稳定 Operation ID+Digest 查询；UNKNOWN 时 Artifact 保持 Private、Barrier 保持开放。所有 Output/Attempt/Replay Path 核清并取得 D Terminal Receipt 后才能关闭终态。

E 不接受 D Approved 消息后接无约束 Object Store 写入。若无共享 ACID 域，E 要求 D+Storage 批准持久化 Prepare/Commit、一次性 Final Visibility CAS、提交时当前 Fence 验证、崩溃恢复和 UNKNOWN 时隐藏。

## 10. D/I/Storage final publication sequence — no detached gate token

E adopts two independent in-flight barriers for protected derivative publication:

1. E completes private staging and the complete dependency set.
2. D admits a D-owned PublicationParticipantRef against the current ForgetFence and records it as unresolved in the D barrier.
3. Storage durably creates a hidden StorageVisibilityParticipantRef bound to PublicationOperationId/digest, artifact/version, WorkItemId, attempt/lease, dependency digest and D PublicationParticipantRef.
4. I consumes a single-use CommitAuthorizationReceipt in its own PolicyDomain sequencer, bound to that exact publication and Storage participant. REVOCATION_WON/UNKNOWN blocks visibility. COMMIT_WON is not visibility; I holds later revocation behind the unresolved participant.
5. Storage commits visibility only after validating exact D participant currentness and I terminal proof at the final boundary, in the D/Storage serialization domain. The commit records immutable PublicationReceipt and participant outcome.
6. D and I independently consume the authoritative Storage outcome: COMMITTED_VISIBLE or proven NO_PUBLICATION closes their respective participant; UNKNOWN keeps both barriers open and artifact private.

D Fence and I revocation are independent gates. D publication intent first means a later D fence waits for this participant; I receipt consumption first means a later revocation waits for this participant. If either authority wins first, publication is rejected or safely aborted. No cross-authority numeric epoch comparison is permitted.

### 中文规范

E 采用受保护 Derivative 发布所需的两个独立进行中 Barrier：

1. E 完成 Private Staging 和完整 Dependency Set。
2. D 根据当前 ForgetFence 准入 D-owned PublicationParticipantRef，并将其记为未解决 Barrier Participant。
3. Storage 持久化创建隐藏的 StorageVisibilityParticipantRef，绑定精确 PublicationOperationId/Digest、Artifact/Version、WorkItemId、Attempt/Lease、Dependency Digest 和 D PublicationParticipantRef。
4. I 在自己的 PolicyDomain Sequencer 中单次消费 CommitAuthorizationReceipt，绑定精确 Publication 与 Storage Participant。REVOCATION_WON/UNKNOWN 阻断 Visibility；COMMIT_WON 仍不等于 Visibility，I 必须让后续 Revocation 等待该未解决 Participant。
5. Storage 仅在最终边界验证精确 D Participant 当前性和 I Terminal Proof 后，才在 D/Storage 序列化域提交 Visibility，同时记录不可变 PublicationReceipt 和 Participant 结果。
6. D 与 I 分别消费权威 Storage Outcome：COMMITTED_VISIBLE 或已证明的 NO_PUBLICATION 关闭各自 Participant；UNKNOWN 保持两个 Barrier 开放且 Artifact Private。

D Fence 与 I Revocation 是独立 Gate。D Publication Intent 先发生，则后来的 D Fence 等待该 Participant；I Receipt Consumption 先发生，则后来的 Revocation 等待该 Participant。任一权威先赢，都必须拒绝或安全中止发布。禁止跨权威 Epoch 数值比较。


## 11. Crash-window correction — Storage prepare before D PublicationParticipant admission

This section supersedes the ordering in §10 where D admission preceded Storage prepare.

The required sequence is:
1. Storage first persists a hidden StorageVisibilityParticipantRef bound to the immutable PublicationOperationId/digest, WorkItemId, artifact/version, AttemptId/LeaseId, complete dependency digest and private stage identity.
2. D then admits PublicationParticipantRef bound to that exact already-durable StorageVisibilityParticipantRef and records it as unresolved in the D fence/barrier.
3. I consumes the single-use CommitAuthorizationReceipt bound to both exact refs and the complete immutable publication tuple.
4. Storage commits visibility only after exact D and I proofs validate at the final boundary.
5. D and I close their own participants only after authoritative Storage COMMITTED_VISIBLE or NO_PUBLICATION evidence.

Crash semantics:
- Storage prepare exists, D admission not yet accepted: remain private; no D barrier participant and no publication capability. D rejection is resolved by the same D operation ID/digest.
- D admission ACK unknown: resolve the same PublicationParticipantRef + digest; do not create another Storage participant.
- D admission accepted: its exact Storage participant must already exist. Missing participant state is UNKNOWN/ledger inconsistency, not safe abort.
- I receipt consumed COMMIT_WON: later revocation remains pending until Storage terminal outcome.
- Any unknown outcome keeps artifact private and all already-admitted barriers open.

D PublicationParticipantRef and I CommitAuthorizationReceipt both bind the exact StorageVisibilityParticipantRef. This participant is not C ParticipantIntentRef or Storage PreparedParticipantRef/GID.

### 中文规范

本节替代 §10 中 D Admission 先于 Storage Prepare 的顺序。

强制顺序：
1. Storage 首先持久化隐藏的 StorageVisibilityParticipantRef，绑定不可变 PublicationOperationId/Digest、WorkItemId、Artifact/Version、AttemptId/LeaseId、完整 Dependency Digest 和 Private Stage 身份。
2. D 随后接受 PublicationParticipantRef，并绑定该精确且已持久化的 StorageVisibilityParticipantRef，将其记录为 Fence/Barrier 内未解决操作。
3. I 单次消费绑定两个精确 Ref 和完整不可变 Publication Tuple 的 CommitAuthorizationReceipt。
4. 只有在最终边界验证精确 D/I 证明后，Storage 才提交 Visibility。
5. D/I 只有取得权威 Storage COMMITTED_VISIBLE 或 NO_PUBLICATION 证据后，才关闭各自 Participant。

崩溃语义：
- Storage Prepare 已存在但 D Admission 尚未接受：保持 Private；尚无 D Barrier Participant，也无发布能力。D 拒绝通过同一 D Operation ID/Digest 解析。
- D Admission ACK 未知：查询同一 PublicationParticipantRef+Digest，不得创建第二个 Storage Participant。
- D Admission 已接受：其精确 Storage Participant 必须已存在。Participant 状态缺失是 UNKNOWN/Ledger Inconsistency，不是安全 Abort。
- I Receipt 已消费为 COMMIT_WON：后续 Revocation 必须等待 Storage 终态。
- 任一结果未知，Artifact 保持 Private，所有已准入 Barrier 保持开放。

D PublicationParticipantRef 和 I CommitAuthorizationReceipt 均绑定精确 StorageVisibilityParticipantRef。该 Participant 不等于 C ParticipantIntentRef 或 Storage PreparedParticipantRef/GID。
