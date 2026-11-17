# Phase 3.7 — G Local Lifecycle: Producer, Derivative, Queue, Recall, Context and Restore

- Owner: G — Memory Context
- Branch: `session-g-memory-context`
- Status: **G-local semantic proposal; C/G/H delivery and cross-owner interfaces remain OPEN / NOT VERIFIED**
- Scope: desired Context membership/versioning, Context-derived artifacts, delivery queue, recall-to-context assembly, Applied evidence and restore/reconnect.
- Authority boundary: D owns canonical Memory, ForgetFence and producer registry; I owns authorization/PermissionEpoch; E owns compiler production; F owns retrieval/index/cache; G owns Context and Context-side delivery/Applied records; H owns authenticated transport/Adapter capability; C owns final immutable request submission/execution evidence; Storage owns durable transaction/visibility evidence.

## 1. G's local lifecycle model

G is the authority for desired Context state and Context-side Applied records, but it is not canonical Memory authority and does not decide source truth.

| Object | G-local states | Terminal / non-terminal meaning |
|---|---|---|
| Context producer work | Planned → DRegistrationPending → Registered → Queued → Leased → Reconciling → Committed / Blocked / CancelledNoPublication | Lease expiry, timeout and DLQ remain open until durable no-publication disposition |
| Context derivative | Candidate → MembershipPlanned → PrivateMaterialized → LineageRegistered → GatePending → CurrentContextVersion / Invalidated / Quarantined | ContextVersion is immutable desired-state version; not canonical Memory revision or Applied |
| Delivery queue | Prepared → Queued → Dispatched → Delivered → Materialized → FinalRequestSubmitted → Applied / Unknown / Rejected / Superseded | Transport ACK is not Applied; Applied requires G predicate and C/H/I/D evidence |
| Recall input | Requested → CandidateRefsReceived → CanonicalValidated → ScopeAuthorized → SelectedForContext / Rejected / Incomplete | F supplies candidates; G owns membership decision, not F ranking/index truth |
| Context | Draft → Validating → Active → Stale → ReconcileRequired → Blocked / Closed | Reconciled is a run outcome, not a Context or Entry lifecycle state |
| Restore unit | Discovered → Isolated → AuthorityReconciled → ContextReconciled → DeliveryReconciled → AdapterReconciled → Serving | Restore receipt alone never enables serving or delivery |

## 2. Producer behavior

1. G is a derivative producer for Context membership/materializations, ChangeSets, immutable Snapshots/Deltas, delivery intents and any durable cache/outbox that can reproduce protected content.
2. Register stable ProducerWorkItemId and complete source/lineage/Scope with D before queue, lease, execution or canonical dereference. Bind ContextId, target ContextVersion/ChangeSet digest, source refs, D fence, I PermissionEpoch and request digest.
3. Retries preserve WorkItemId+digest; AttemptId/LeaseId change. Same identity+digest is idempotent; changed digest is conflict.
4. Every derived Context artifact registers complete direct/transitive dependencies with D before visibility or delivery. If atomic/recoverable final gate is unavailable, keep it private and create no sendable Delivery.
5. D producer barrier closes only on D-accepted durable terminal disposition. G cannot close D's barrier or claim global Forget completion.
6. Context Remove is membership change only; it is not canonical Forget and cannot substitute for D ForgetFence.

## 3. Derivative behavior

- ContextEntry membership, rendered/materialized region, immutable Snapshot/Delta, ChangeSet, delivery payload, context cache and restore image are derivatives whenever they contain or can reconstruct canonical source content.
- Each artifact binds ContextId, immutable ContextVersion, source MemoryVersionRefs, full transitive lineage digest, ScopeRefs, EnvironmentRef, I PermissionEpoch, D fence checkpoint, artifact schema, digest and producer work identity.
- Build privately; register dependencies; validate current D fence and I permission at the final visibility/delivery gate. No check-then-send.
- Forget/revocation installs a durable deny tombstone immediately. Suppress affected entries, invalidate stale ChangeSets/Snapshots/Deltas/materializations, cancel or supersede pending delivery, and prevent late ACK from promoting Applied.
- Historical immutable ContextVersion and valid historical Applied record may be retained as non-serving audit evidence under I policy. Current-use validity is a separate projection; later Forget does not rewrite a historically true submission fact.
- Context Remove is not physical erasure; G reports only Context/known Adapter action evidence and never claims F purge, C execution deletion or external physical erasure.

## 4. Queue and delivery behavior

- Delivery queue is a durable state machine keyed by DeliveryId and DeliveryAttemptId, bound to exact ContextVersion, target Adapter/session, Scope, Environment, region inventory/digest, PermissionEpoch, D fence and H capability epoch.
- Queue insertion/dispatch and H transport ACK are separate stages. Delivered does not mean Materialized; Materialized does not mean FinalRequestSubmitted; FinalRequestSubmitted does not mean Applied.
- Attempts are immutable. Retry creates a new attempt; a late ACK for an old attempt is historical evidence only and cannot roll back/supersede a newer target.
- Before dispatch, adapter apply and final request submission, revalidate current I authorization, D fence/lineage, Context head, Scope/Environment, session and H capability. Unknown means suppress/block.
- Forget/revocation cancels/supersedes all not-yet-finalized attempts and requests Adapter clear for all known sessions that may have received target. Offline/timeout/lost ACK = Unknown, never confirmed.
- Queue restore quarantines old payloads; do not replay before full identity/session, permission, fence, target version and Adapter reconciliation.

## 5. Recall behavior

- G does not own global retrieval or ranking. F provides candidate MemoryVersionRefs plus watermark/completeness/truncation and provenance evidence.
- G resolves each exact ref with D, checks lineage and lifecycle, authorizes exact Scope/purpose with I, and compares source/freshness evidence. Missing index hits are not absence.
- G selects membership based on task/Agent/Environment relevance, policy, sufficiency and budget; retain provenance and source identity. Never silently substitute a newer revision or rewrite disputed claims.
- If F reports gaps/truncation or D/I authority is unknown, mark Context incomplete/stale or block affected entries; do not convert uncertainty into a clean Context.
- G's selection is a Context decision, not a claim that a model recalled, attended to, understood or used the content.

## 6. Context behavior

- G owns ContextId, immutable ContextVersion, desired membership, ContextEntry lifecycle, ChangeSet/CAS, Snapshot/Delta, Delivery and Applied record.
- Context is a scoped, task/Agent/Environment-bound working target assembled from canonical refs; it is not a second canonical Memory store.
- Keep Context, Entry, Delivery and Applied lifecycles separate. Context Active does not imply all entries valid; Delivered does not imply Applied; Applied is per exact request/session/region.
- Context reconciliation compares desired membership with D canonical lifecycle/lineage, I authorization, E event status, F freshness/completeness and H/C delivery/request evidence. A reconciliation run's Reconciled result is scoped to its declared watermark and Scope.
- On Forget/revocation, deny tombstone takes effect before expensive cleanup. Historical snapshots become audit-only and non-sendable; create a new safe ContextVersion only after current authority checks.
- Full Applied requires exact ContextVersion, Delivery/Attempt, InferenceRequestId, FinalRequestBoundaryId, Adapter/session/capability, region digest, current PermissionEpoch, D fence and C final-request evidence. It proves exact submission under predicates, not attention, understanding or execution success.

## 7. Restore and reconnect

1. Restore Context versions, ChangeSets, Snapshots/Deltas, delivery ledger, Applied history, tombstones and adapter-session records into isolated non-serving state.
2. Reconcile COC committed prefix, current I PermissionEpoch/revocation/registry high-water, D Forget/lineage/producer barrier and Storage pointer/receipt/participant ledger. These are separate typed authorities.
3. Reapply deny tombstones before any content materialization. Revalidate each ContextEntry's exact source revision, lineage, Scope, Environment and current authorization.
4. Preserve historical Applied facts, but recompute current-use validity; do not replay an old Applied as permission to deliver.
5. Reject stale ContextVersion, ChangeSet base, Snapshot/Delta chain, DeliveryAttempt, ACK, Adapter session or capability epoch. Unknown continuity requires a new full Snapshot only after current authority checks.
6. Reconcile every known Adapter/session. Offline, failed or insufficiently observable targets remain Unknown/Blocked; never assume cleared.
7. Rebuild a new safe ContextVersion atomically via CAS; create fresh Delivery attempts only after the target is current and authorized.
8. Immediately before Adapter apply and again before final request submission, revalidate I/D/G/H state. Storage RestoreReconciliationReceipt is not Context Applied or global Forget completion.
9. Reconnect is a new trust boundary: authenticate new session, negotiate capability, fetch current I/D state, clear/quarantine old local state, reconcile G target, then send current Snapshot/Delta. Never restore old snapshot first and clean later.

## 8. Evidence and tests

G emits ContextVersion/ChangeSet IDs, source/lineage digest, Scope/Environment, producer registration and dependency receipts, reconciliation watermarks/gaps, DeliveryId/Attempt, Adapter/session/capability, region digest, C final-request evidence reference, Applied disposition and restore result. G never claims F index purge, H byte purge, C execution success or I global Forget completion.

Required tests: D fence vs Context publish; revocation vs dispatch/apply/final-submit; duplicate/changed-digest producer and delivery; late ACK from superseded attempt; F index gap/truncation; stale Context CAS; offline Adapter reconnect; restore with old snapshot/ACK; historical Applied vs current-use invalidation; unknown authority blocks. These are specifications until executed.

## 9. Non-goals / blockers

- G does not create canonical Memory, decide Forget, own F retrieval/index, E compiler queues, H protocol, C execution or I policy.
- C/G/H exact final-request/Applied proof contract remains a cross-owner dependency.
- **No production Context restore, Adapter delivery integration, conformance PASS or global Forget completion is claimed.**


## 10. Phase 3.7 cross-owner reconciliation amendments (EN)

**Disposition:** G-local amendment proposal for LIF-01/03/04/05/08/09/10/12. D/C/I/H boundaries remain independently owned; this amendment does not claim their approval.

### 10.1 Context derivative registration vs Delivery vs provider participant intent
- G's local ProducerClass declaration is descriptive only. Every persistent/replayable Context derivative (membership materialization, Snapshot, Delta, ChangeSet, retained region, cache or outbox payload) requires a D-issued enabled ProducerClass and D RegistrationReceipt before queue/lease/build/source dereference/publication.
- Context materialization and retained Context artifacts are G derivatives; their complete direct/transitive source dependencies MUST be registered with D before they become visible or sendable.
- DeliveryId, DeliveryAttemptId, H transport receipt/ACK, Delivered or Materialized proves only its declared delivery/disclosure boundary. It is not D ProducerRegistration, D ParticipantIntentRef, C provider-submit evidence or G Applied.
- Before C crosses provider submit, the exact request-bound ParticipantIntentRef MUST already be admitted by D into the causal participant barrier. It MUST bind the immutable request, region digest, ContextId/ContextVersion, DeliveryId/Attempt, target Adapter/session, Scope/Environment and current I authorization. C MUST reject submit if the reference/binding is absent, stale or mismatched. G cannot mint or infer it from Delivery/ACK.
- D's participant-intent contract and C enforcement remain blocking until D and C publish exact owner-owned contracts. No provider-submit permission is implied here.

### 10.2 Applied and authorization semantics
- G owns Applied for its exact predicate/evidence set. Applied is historical proof of a specific request/region/session boundary, not attention, understanding, successful execution, D barrier closure or global Forget completion.
- Historical Applied may be retained as audit evidence under I policy. After Forget, revocation, restore or scope/session change, recompute current-use eligibility; old Applied, Delivery or ACK never grants permission to resend or serve.
- I authorization and D fence/lineage are independent. Revalidate current I authorization and D eligibility before dispatch, Adapter apply, final request submission and protected materialization. Unknown means suppress/block.
- H authenticates/transports evidence but cannot upgrade Delivered to Materialized, Materialized to FinalRequestSubmitted or FinalRequestSubmitted to G Applied.

### 10.3 Restore and Context type safety
- Restore uses a conjunctive manifest of independent Storage, COC, I, D and G/Adapter proofs. Validate each against its issuer, audience, signature, schema, lineage and opaque authority-local position. No merged scalar high-water or cross-authority numeric comparison.
- Old Context payloads, delivery attempts, ACKs and Adapter sessions restore audit-only/quarantined. Reconnect requires a new authenticated session/current capability; only after current I/D checks and a new safe ContextVersion may G create a fresh Delivery attempt.
- G ContextVersion, F Working Set and E frozen compiler input bundle are distinct nominal types. ContextVersion is not canonical Memory version, index watermark, permission epoch or D fence generation.

## 10. Phase 3.7 跨 Owner 对齐修订（中文）

**处置：** 本节将 LIF-01/03/04/05/08/09/10/12 纳入 G 本地合同。D/C/I/H 权威边界仍由各自 Owner 决定；本节不代表其已批准。

### 10.1 Context Derivative 注册、Delivery 与 Provider Participant Intent
- G 本地 ProducerClass 声明仅用于描述。所有持久化或可重放的 Context Derivative（成员物化、Snapshot、Delta、ChangeSet、保留区域、缓存或 Outbox Payload）都必须由 D 的启用 ProducerClass 覆盖，并在入队/分配租约/构建/源读取/发布前取得 D RegistrationReceipt。
- Context 物化及保留的 Context Artifact 均属于 G Derivative；可见或可发送前，必须向 D 注册完整直接和传递源依赖。
- DeliveryId、DeliveryAttemptId、H Transport Receipt/ACK、Delivered 或 Materialized 状态仅证明对应 Delivery/Disclosure 边界，不是 D ProducerRegistration、D ParticipantIntentRef、C Provider Submit 证据或 G Applied。
- C 跨越 Provider Submit 边界前，精确绑定请求的 ParticipantIntentRef 必须已由 D 纳入因果 Participant Barrier，并绑定不可变请求、Region Digest、ContextId/ContextVersion、DeliveryId/Attempt、目标 Adapter/Session、Scope/Environment 和当前 I 授权。引用或绑定缺失、陈旧或不匹配时，C 必须拒绝 Submit。G 不得自行制造该引用，也不得从 Delivery/ACK 推断其存在。
- D Participant Intent 合同及 C 侧强制执行仍是阻塞项，直至 D 和 C 分别发布精确 Owner 合同。本 G 提案不授予 Provider Submit 权限。

### 10.2 Applied 与授权语义
- G 仅对其精确定义的 Predicate 和证据集合签发 Applied。Applied 是特定 Request/Region/Session 边界的历史证明，不证明注意、理解、执行成功、D Barrier 关闭或 Global Forget 完成。
- 历史 Applied 可按 I 策略作为审计证据保留。Forget、撤权、Restore 或 Scope/Session 变化后，必须重新计算当前使用资格；旧 Applied、Delivery 或 ACK 永远不能授权重新发送或 Serving。
- I 授权与 D Fence/Lineage 相互独立。Dispatch、Adapter Apply、Final Request Submit 及受保护物化之前，必须重新验证 I 当前授权和 D 当前资格。未知即抑制/阻断。
- H 负责认证/传输证据，但不能把 Delivered 升级为 Materialized、Materialized 升级为 FinalRequestSubmitted，或把 FinalRequestSubmitted 升级为 G Applied。

### 10.3 Restore 与 Context 类型安全
- Restore 使用 Storage、COC、I、D 和 G/Adapter 独立证明的合取清单。每份证明都按自己的签发者、受众、签名、Schema、Lineage 和权威域内不透明位置验证。禁止合并标量 High-water 或跨权威数值比较。
- 旧 Context Payload、Delivery Attempt、ACK 和 Adapter Session 恢复后只能处于审计/隔离状态。Reconnect 必须建立新的认证 Session 和当前 Capability；只有通过当前 I/D 检查并生成新的安全 ContextVersion 后，G 才能创建新的 Delivery Attempt。
- G ContextVersion、F Working Set、E 冻结编译输入包是不同名义类型。ContextVersion 不是 Canonical Memory Version、Index Watermark、PermissionEpoch 或 D Fence Generation。
