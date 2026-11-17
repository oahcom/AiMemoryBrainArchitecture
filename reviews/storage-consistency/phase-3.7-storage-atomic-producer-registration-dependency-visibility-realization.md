# Phase 3.7 — Storage Atomic Producer Registration, Dependency and Visibility Realization

- Owner perspective: Storage / Consistency
- Status: **PROPOSED PHYSICAL REALIZATION; not selected, implemented or conformance-verified**
- Branch: session-storage-consistency-forget-atomicity-2026-11-16
- Exact semantic authorities: D Producer/Fence/Lineage; I current authorization; E compiler lifecycle
- English and Chinese are normative peers.

## 1. Decision boundary

Storage accepts D's exact semantic operation set and E's lifecycle ordering as the required input contract, subject to exact-owner review. Storage does not own or mint ProducerClass eligibility, ProducerRegistrationReceipt, ForgetFence, dependency semantics, lineage completeness, I authorization or D terminality.

- D decides and signs the semantic admission/fence/dependency/publication/terminal outcomes.
- E owns CompileIntent, ProducerWork consumption, attempts, leases, derivation runs, private staging and output accounting.
- I owns current authorization and revocation.
- Storage owns durable persistence, transaction isolation/serialization, idempotency constraints, authoritative visibility state and crash recovery.
- H transports typed evidence; transport ACK is not a commit or gate receipt.

The Storage realization must not turn a Storage row into a D decision merely because both are stored in one database. Logical authority remains D; Storage provides the physical commit substrate and exact evidence of persistence/visibility.

## 2. Required shared serialization domain

Preferred realization is one serializable transactional database/coordinator per Canonical Memory authority, covering D-authoritative control rows and the authoritative artifact visibility pointer. At minimum, the same serialization domain orders:

1. RegisterProducerWork and its ProducerRegistrationSequence/RegistrationReceipt;
2. InstallForgetFence and its immutable ProducerRegistryVersion + ProducerRegistrationHighWater + target inventory snapshot;
3. RegisterDerivedDependency as one complete immutable artifact/dependency set;
4. PublishDerivedIfFenceCurrent and the authoritative visibility transition;
5. CompleteProducerWork and barrier-visible terminal disposition.

RegisterProducerClass version/status must be durably committed before work admission and read in the same admission order. CaptureProducerRegistrationHighWater is the immutable value committed with fence installation; it is not a later queue scan or a new cutoff.

A deployment may use separate physical services only if D and Storage approve a durable prepare/commit or equivalent linearizable coordinator protocol that preserves these same ordering and recovery guarantees. A process-local mutex, queue ordering, eventual replica, outbox-only design, stale cached fence, check-then-write, or reusable D token followed by an independent Storage write is rejected.

## 3. Logical persistence records (illustrative, not frozen schema)

| Record | Required binding | Authority / use |
|---|---|---|
| AuthorityCoordinator | BrainAuthorityRef, serialization version, current D fence ref, next D registration position | Storage serialization substrate; D semantics |
| ProducerClassVersion | ProducerClassId/version, owner/workload binding, capabilities, enabled status, digest | D-owned registry projection |
| ProducerWork | stable ProducerWorkItemId, class/version, authenticated producer binding ref, EventRef/canonical refs, lineage token/digest, Scope, request digest, D registration position, observed fence, state | D-owned barrier ledger |
| WorkAttempt | WorkItemId, AttemptId, LeaseId, lease epoch, worker binding, current auth/fence observations, state | E execution / stale-worker fencing |
| ForgetFence | ForgetOperationRef, D generation, target digest, registry version, captured producer high-water, inventory snapshot ref | D-owned fence projection |
| DerivedArtifact | immutable ArtifactRef/version, WorkItemId, DerivationRunId, private locator, payload digest, visibility state | E output / Storage privacy |
| DependencySet | stable registration ID/digest, artifact/version, complete direct/transitive edges, lineage digest, Scope, D inventory position | D-owned dependency inventory |
| Publication | stable PublicationOperationId/digest, artifact, work/attempt/lease, dependency receipt digest, D fence decision ref, I decision ref, visibility transaction ID, PublicationReceipt | D decision + Storage visibility proof |
| WorkTerminal | WorkItemId, final attempt, all output dispositions, no-future-publication proof, D terminal receipt | D barrier terminality |
| Outbox | stable event ID, source transaction/commit ID, event digest, delivery state | At-least-once propagation only |

Opaque IDs are non-recycled. Same logical identity + same canonical digest returns original evidence; same identity + changed digest is immutable conflict. D ProducerRegistrationSequence, D ForgetFenceGeneration, D CanonicalCommitCursor, I PermissionEpoch, Storage transaction/XID/visibility pointer, E AttemptId/LeaseId and F/G positions remain distinct nominal types.

## 4. Atomic operation protocols

### 4.1 RegisterProducerWork

One transaction under the shared coordinator:
1. Authenticate the caller context and validate the D ProducerClass version/status and request digest.
2. Resolve stable WorkItemId idempotency; same digest returns the original receipt, changed digest conflicts.
3. Evaluate the latest applicable D fence and Scope/lineage eligibility.
4. If allowed, allocate the D ProducerRegistrationSequence and persist the D-owned work ledger row and durable receipt together.
5. If blocked, persist REJECTED/QUARANTINED/CLEANUP_ONLY with no executable lease/queue capability.
6. Commit before E may enqueue, lease, dereference protected source content or execute derivative-capable work.

**Linearization point:** commit of the transaction that evaluates current fence and commits accepted registration in the same serialization order as fence installation.

EventRef-only ingress is supported consistently with D §3.2: an immutable EventRef plus authenticated producer, enabled class/version, exact Scope, request digest and D-approved opaque lineage token/digest may be registered before Canonical MemoryRef exists. Such work is included in D barrier high-water. Exact canonical refs/revisions must be linked before dependency registration/publication. Incomplete identity/Scope/lineage remains quarantined. Registration is not I authorization for protected payload dereference.

### 4.2 InstallForgetFence and high-water

One transaction under the same coordinator:
1. Resolve ForgetOperation idempotency and target digest.
2. Allocate the D-owned fence generation.
3. Capture the last committed D ProducerRegistrationSequence as immutable high-water.
4. Persist effective fence, target/lineage selector digest, ProducerRegistryVersion, high-water, inventory snapshot ref and outbox intent.
5. Commit.

**Linearization point:** this commit. An admission racing the fence either commits first and is included at/below high-water, or follows the fence and is rejected/quarantined/cleanup-only. No admitted-but-unaccounted work state is legal.

### 4.3 RegisterDerivedDependency

Stage artifact bytes privately first. Then one transaction:
1. Resolve DependencyRegistrationId/digest.
2. Verify registered nonterminal WorkItemId and exact current AttemptId/LeaseId.
3. Verify exact canonical source refs/revisions have been linked to any EventRef-only ingress lineage.
4. Verify every direct and transitive source/parent edge and exact Scope.
5. Re-evaluate current D fence/lineage and persist the artifact identity plus the entire required edge set as one complete immutable registration.
6. Emit a complete D DependencyRegistrationReceipt only after commit.

Partial edge sets remain explicitly incomplete and non-publishable. If a multi-store prepare is required, no incomplete/prepared artifact or receipt may be interpreted as dependency-complete.

### 4.4 PublishDerivedIfFenceCurrent + visibility

One authoritative visibility transaction must:
1. Resolve PublicationOperationId/digest; return original result for exact replay, conflict on changed digest.
2. Verify D RegistrationReceipt, ProducerWorkItemId, class/version, exact artifact/version and request digest.
3. Verify current AttemptId/LeaseId/lease epoch and reject stale/superseded workers.
4. Verify complete D dependency receipts, transitive lineage digest, exact source revisions and Scope.
5. Validate the latest applicable D fence in the same serialization domain as InstallForgetFence.
6. Validate an I-authoritative current authorization decision at the final boundary. Storage MUST NOT compare PermissionEpoch numerically with D positions. If I cannot provide a decision whose currentness is valid at the actual visibility linearization point, visibility is blocked. The exact I proof/serialization mechanism remains an I-owned dependency, not invented by Storage.
7. Atomically commit visibility pointer/state, D PublicationReceipt outcome, Storage visibility transaction identity and outbox event.

**Linearization point:** the durable transaction commit that both validates all predicates and changes the authoritative visibility state. No prior “gate approved” message can be consumed later as an unconstrained write permit.

Before commit every read path sees PRIVATE_STAGED/absent. After commit a reader may resolve the artifact only through the authoritative visibility pointer and must still enforce current D/I eligibility on serving/rebuild paths. Object-store existence/listing, signed URLs, cache warming, index events and outbox delivery do not establish visibility.

If the commit ACK is lost, state is UNKNOWN and the artifact remains non-consumable until the same PublicationOperationId/digest resolves to the authoritative committed receipt. The implementation must make it impossible for readers to observe a visibility pointer whose transaction outcome is unresolved.

### 4.5 CompleteProducerWork

A terminal transaction verifies:
- final lease/attempt fencing;
- every output has a durable published receipt or a durable suppressed/quarantined disposition incapable of later publication;
- every dependency/publication operation is resolved;
- no retry, DLQ replay, delayed worker, outbox or staged publisher can still publish;
- no unknown ACK/participant or inventory gap remains.

Only then may D commit its terminal receipt and close the barrier item. Lease expiry, worker death, queue deletion and DLQ are not terminal. Late discovery of a publication reopens reconciliation without rewriting historical receipts.

## 5. Crash, retry and recovery rules

- Crash before registration commit: no D receipt, no queue/lease/execute.
- Crash after registration commit but before ACK: resolve same WorkItemId/digest; do not create a second registration.
- Crash after private staging: bytes remain private; resume same work or quarantine.
- Crash during dependency-set commit: authoritative transaction is either complete or incomplete; only complete committed set gets a receipt.
- Crash during final visibility commit: read authoritative transaction by same PublicationOperationId/digest. Committed returns original receipt; proven abort permits retry under fresh I/D checks; UNKNOWN remains hidden and barrier-open.
- Lease replacement: old lease epoch cannot register dependencies, publish or terminalize.
- Fence advances after work admission: work remains barrier-accounted; dependency/publication rechecks current fence and cannot publish covered lineage.
- Restore/failover: restore all records into quarantine/non-serving mode, reconcile D fence/ledger and I current policy before visibility pointers or projections are served. Unknown ledger/engine/replica state remains quarantined.

## 6. Race proof obligations

For every applicable Work W and Fence F:
- **Admission first:** W's committed registration position is at/below F's captured high-water; W is accounted. Any later covered derivative publication is rejected by the final current-fence gate.
- **Fence first:** F and its high-water commit; W's later registration is rejected/quarantined/cleanup-only and receives no execution capability.

For publication P racing F:
- **Publication first:** visibility commit is durable before F; its complete dependency/lineage inventory is available to F reconciliation.
- **Fence first:** P observes the current fence in the same serialization domain and cannot become visible.
- **Unprovable order:** UNKNOWN; artifact remains private.

No third outcome is permitted.

## 7. Owner acceptance and open dependencies

Storage's proposed physical realization is **ACCEPT WITH ENUMERATED CONDITIONS** for the D/E semantic contracts pinned below, not a claim of independent Owner approval or implementation success.

Exact sources reviewed:
- D controlling operation contract: Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5.
- D Phase 3.7 correction: to be pinned after D exact readback.
- E producer admission: Blob e59f517fff161ab882aa0ddc4a5bda513964ae1a.
- E derived registration/staging: Blob 00e37ba56596e710513c8d0568acd79141d9101b.
- Storage realization baseline: Blob 107d21bd2c604ee0b04feff2ee5580e1de9c7fce.
- Storage prepared-participant design v3.1: Blob d5bdc72f193fcdaa654e4f07f865b77c578673ca; this is a related JF-10 persistence contract, not proof that producer visibility transactions are implemented.

Blocking conditions:
1. D must confirm the EventRef-only correction and exact registration/dependency/publication receipts on the amended D Blob.
2. E must confirm the corrected EventRef mapping, stable work/attempt semantics and exact consumption sequence on the amended E Blob.
3. I must define how current authorization is linearized at a Storage visibility commit, including revocation racing that commit; a stale signed snapshot is insufficient.
4. D and Storage must identify the actual shared transaction/serialization authority and its ownership/deployment boundary.
5. H must define the exact wire schemas and canonicalization/signature profile for D/E/Storage receipts; no wire freeze is implied.
6. Engineering must implement and run deterministic admission/fence, dependency completeness, visibility, stale-lease, ACK-loss, crash, failover and restore tests.

This proposal does not select a database product, claim a D/E API exists, assert a shared transaction domain is deployed, or claim tests passed. No schema freeze, branch merge, implementation conformance PASS, production activation or global Forget completion is authorized.

## 8. 中文规范

### 8.1 权威边界
Storage 接受 D 的精确语义操作集和 E 的生命周期顺序作为必需输入合同，但仍须精确 Owner 复审。Storage 不拥有或签发 ProducerClass 资格、ProducerRegistrationReceipt、ForgetFence、Dependency Semantics、Lineage Completeness、I Authorization 或 D Terminality。

- D 决定并签发 Admission/Fence/Dependency/Publication/Terminal 语义结果。
- E 管理 CompileIntent、ProducerWork 消费、Attempt、Lease、DerivationRun、Private Staging 和 Output Accounting。
- I 管理当前授权与撤权。
- Storage 管理持久化、事务隔离/序列化、幂等约束、权威 Visibility State 和崩溃恢复。
- H 传输类型化证据；Transport ACK 不是 Commit 或 Gate Receipt。

即使 D 权威记录与 Storage 可见性指针存放在同一个数据库，Storage 记录也不会自动变成 D 决策。逻辑权威仍是 D；Storage 只提供物理提交基座及持久化/可见性证据。

### 8.2 共享序列化域
首选方案是每个 Canonical Memory Authority 使用一个可串行化事务数据库/Coordinator，覆盖 D 权威控制记录和权威 Artifact Visibility Pointer。同一序列化域至少排序 RegisterProducerWork、InstallForgetFence 与不可变 Registry/Work High-water、完整 RegisterDerivedDependency、PublishDerivedIfFenceCurrent 与 Visibility Transition、CompleteProducerWork。

ProducerClass Version/Status 必须先持久化，并由同一 Admission Order 读取。CaptureProducerRegistrationHighWater 是与 Fence Installation 一起提交的不可变值，不是之后扫描 Queue 或重新生成 Cutoff。

若采用分离物理服务，只有 D 和 Storage 批准的持久化 Prepare/Commit 或等效线性一致 Coordinator 协议才可接受，并须保留相同排序与恢复保证。进程内 Mutex、Queue 顺序、最终一致副本、仅 Outbox、陈旧 Fence Cache、Check-then-write，以及可重放 D Token 后独立 Storage 写入均不合格。

### 8.3 持久化记录
记录模型见上表。所有 ID 不透明且不可复用。同身份同规范摘要返回原证据；同身份不同摘要为不可变冲突。D ProducerRegistrationSequence、D ForgetFenceGeneration、D CanonicalCommitCursor、I PermissionEpoch、Storage Transaction/XID/Visibility Pointer、E AttemptId/LeaseId 和 F/G 位置必须保持不同名义类型。

### 8.4 原子操作
**ProducerWork 注册：** 在共享 Coordinator 事务中验证认证上下文、ProducerClass、摘要和当前 Fence；同一事务分配 D RegistrationSequence 并写入 D Work Ledger/Receipt。Commit 前 E 不得入队、租约、读取受保护内容或执行。

**Fence 安装：** 同一 Coordinator 事务分配 D FenceGeneration，捕获最后已提交 ProducerRegistrationSequence，并一起持久化 Fence、Target Digest、Registry Version、Inventory Snapshot 和 Outbox。注册先提交则进入 High-water；Fence 先提交则后续工作拒绝/隔离/仅清理。

**EventRef-only：** 与 D §3.2 一致，EventRef、认证 Producer、启用 Class/Version、精确 Scope、请求摘要及 D 批准 Lineage Token/Digest 完整时，可在 Canonical MemoryRef 前注册并进入 Barrier。Canonical Refs/Revisions 必须在 Dependency Registration/Publish 前补齐。Registration 本身不等于 I 对受保护 Payload 的授权。

**Dependency Registration：** 私有暂存后，以一个事务提交完整 Artifact Identity 和所有直接/传递 Edge。部分集合始终不可发布。

**最终 Publish：** 一个权威 Visibility Transaction 必须同时检查 D Registration、Work/Attempt/Lease、完整 Dependency/Lineage、Scope、最新 D Fence 和 I 当前授权，并提交 Visibility Pointer、D PublicationReceipt、Storage Commit Identity 与 Outbox。没有“先批准、后无约束写入”的中间授权。

**Terminal：** 只有所有输出、Attempt、Retry、DLQ Replay、Outbox 和延迟 Publisher 均已核清，且无 UNKNOWN，D 才能提交 Terminal Receipt 并关闭 Barrier。

### 8.5 崩溃与恢复
注册 Commit 前崩溃：无 Receipt、无执行。Commit 后 ACK 丢失：用同 WorkItemId/Digest 查询。Stage 后崩溃：仍 Private。Dependency Commit 崩溃：只有完整原子提交才能产生 Complete Receipt。Visibility ACK 丢失：按同 PublicationOperationId/Digest 查询；UNKNOWN 保持隐藏。旧 Lease Epoch 不得注册依赖、发布或终态化。Restore 必须先隔离，再重放/核验 D Fence/Ledger 和 I 当前策略，未知状态继续隔离。

### 8.6 接受条件与未决事项
Storage 对 D/E 语义合同给出 **附条件接受**，不是独立 Owner 批准或实现成功声明。仍须 D 确认 EventRef 修正，E 确认生命周期映射，I 定义 Visibility Commit 处授权当前性的线性化及撤权竞态，D/Storage 指定实际共享事务域，H 冻结精确 Wire Schema，并由工程团队执行确定性 Race/Crash/Failover/Restore 测试。

本提案不选择数据库产品，不声称 D/E API 已存在，不声称共享事务域已部署，也不声称测试通过。不授权 Schema Freeze、合并、实现符合性 PASS、生产启用或 Global Forget 完成。

## 9. Joint D/I in-flight gate composition — mandatory before visibility commit

The D/Storage serialization domain alone does not resolve the independent I revocation race. The following composition is mandatory and supersedes any reading of §4.4 that treats a detached I current-ALLOW snapshot as sufficient.

1. D admits an exact PublicationParticipantRef into its own fence/barrier order. A later D fence cannot become effective past it until terminal Storage outcome.
2. Storage creates a durable hidden StorageVisibilityParticipantRef bound to the same PublicationOperationId/digest and D participant.
3. I consumes a single-use CommitAuthorizationReceipt in its own PolicyDomain sequencer, bound to that exact Storage participant and D participant. Revocation-first rejects; COMMIT_WON holds later revocation until Storage terminal outcome.
4. Storage final visibility transaction validates both the active D publication participant/current D fence and the exact I terminal proof. The D/Storage transaction is the physical visibility linearization point; the I sequencer establishes the independent authorization/revocation order.
5. On commit, Storage emits immutable COMMITTED_VISIBLE proof. On proven abort, it emits NO_PUBLICATION proof. D and I close their respective in-flight participants only after verifying the same Storage outcome. UNKNOWN leaves both gates open and artifact private.

The authority barriers are conjunctive, not numerically merged. D fence-first or I revocation-first means no visibility. A D publication participant or I COMMIT_WON alone is never visibility permission. Exact D/I/Storage owner acceptance and deterministic crash/race tests remain required; this protocol is not implemented or verified.

### 中文规范

D/Storage 序列化域本身不能解决独立 I Revocation 竞态，因此强制采用上述组合：D 将精确 PublicationParticipantRef 纳入自身 Fence/Barrier；Storage 创建隐藏 Visibility Participant；I 在自己的 PolicyDomain Sequencer 单次消费绑定 D/Storage Participant 的 CommitAuthorizationReceipt；Storage 最终 Visibility Transaction 同时验证 D 当前参与状态/Fence 和精确 I Terminal Proof。Storage 提交后产生不可变 COMMITTED_VISIBLE 证明；安全中止产生 NO_PUBLICATION 证明；D/I 只有验证同一 Storage Outcome 后才能分别关闭自己的 Participant。UNKNOWN 时两个 Gate 均保持开放且 Artifact Private。

两个权威 Barrier 必须合取满足，不得合并成数值序列。D Fence-first 或 I Revocation-first 均不得 Visibility。D Publication Participant 或 I COMMIT_WON 单独存在都不是 Visibility Permission。本协议仍须 D/I/Storage 精确 Owner 接受和确定性 Crash/Race 测试；尚未实现或验证。


## 11. Exact source pins and nominal identity separation

The following Phase 3.7 owner-role amendments are the exact current proposal bundle consumed by this Storage design:
- D Phase 3.7 Blob: `62d8eaf3501e20ecaceba5cd6f3298d5f6b03ac4`.
- E Phase 3.7 Blob: `2e80b66b2c6612bc67a5dec69c74e3c6cb2ba734`.
- I Phase 3.7 Blob: `a09a2ecc37601c25bfa7a6a235350730cac2855b`.
- D controlling operation contract Blob: `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`.
- E producer admission Blob: `e59f517fff161ab882aa0ddc4a5bda513964ae1a`.
- E staging/derived registration Blob: `00e37ba56596e710513c8d0568acd79141d9101b`.
- I PermissionEpoch/final-boundary contract Blob: `bae6a24fe3a374bc816993979a8fa9af52517dea`.
- I CommitAuthorizationReceipt/sequencer contract Blob: `5a5304d48aa912dcf6f817099bd5659371d8cdc8`.
- C final-submit contract Blob: `45a48249717c8cddb07ab96197730ef93d406c22`.
- G Applied/Context contract Blob: `aa3afa73d8a76cc6f025839c52bfbff6a983046a`.

Nominal identity separation is mandatory:
- D PublicationParticipantRef is the in-flight barrier identity for one derivative visibility attempt; it is not C's ParticipantIntentRef.
- C ParticipantIntentRef is the pre-provider-side-effect participant; it is not D PublicationParticipantRef.
- StorageVisibilityParticipantRef is the hidden Storage visibility transaction participant; it is not PreparedParticipantRef or PreparedTransactionGID from the separate JF-10 prepared-transaction protocol.
- PublicationOperationId, CausalOrderTransactionRef, PreparedParticipantRef, ProducerWorkItemId, DerivationRunId, AttemptId and LeaseId remain distinct types and idempotency scopes.

The D/I/Storage composition in §§9–10 is a candidate joint protocol. It does not inherit C/G Applied acceptance or JF-10 prepared-participant acceptance by analogy. Each exact interface and wire mapping requires its own review.


## 12. Crash-window correction — durable Storage participant must precede D barrier admission

This section supersedes the D-first order in §9.

The physical order is now:
1. Persist a hidden StorageVisibilityParticipantRef and its complete immutable tuple/ledger row first.
2. D admits PublicationParticipantRef bound to that exact Storage participant. D admission is impossible if the Storage participant is not authoritatively durable.
3. I consumes a single-use receipt bound to both refs.
4. Storage final visibility commit validates the D participant/current fence and I terminal proof.
5. Storage writes COMMITTED_VISIBLE or authoritative NO_PUBLICATION; D/I close their respective participants only after verifying the same outcome.

A crash between steps 1 and 2 leaves an orphan private Storage participant, which has no D admission and no path to visibility. It can remain quarantined for later same-ID reconciliation; it must not be garbage-collected based only on age. A crash after D admission cannot be resolved by a missing Storage row: it is UNKNOWN/ledger inconsistency, and D/I gates remain held.

The D PublicationParticipantRef must include the exact StorageVisibilityParticipantRef. The Storage ledger row is the recovery anchor that prevents an admitted D barrier participant from existing without a recoverable Storage operation identity.

This order does not weaken D fence-first or I revocation-first behavior. It only closes the prepare/admission crash window.
