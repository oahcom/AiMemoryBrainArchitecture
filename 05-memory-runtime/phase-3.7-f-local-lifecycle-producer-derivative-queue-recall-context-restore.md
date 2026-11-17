# Phase 3.7 — F Local Lifecycle: Producer, Derivative, Queue, Recall, Context and Restore

- Owner: F — Memory Runtime
- Branch: `session-f-memory-runtime`
- Status: **F-local semantic proposal; cross-owner interfaces and implementation remain OPEN / NOT VERIFIED**
- Scope: runtime retrieval, indexes, caches, Working Sets, runtime-owned derived projections, and reconnect/restore.
- Authority boundary: D owns canonical Memory, ForgetFence, producer registry and lineage; I owns authorization/PermissionEpoch; E owns compiler production; G owns Context and Applied/Delivery; H owns adapter transport/capability; Storage owns durable transaction/visibility evidence.

## 1. F's local lifecycle model

F is a consumer and projection maintainer, not a canonical Producer of Memory. F may itself create runtime-local derivatives (index segments, embeddings, query caches, entity/graph projections, summaries used only as retrieval aids, Working Set entries); those remain non-authoritative and must carry exact source lineage and Scope.

| Object | F-local states | Terminal / non-terminal meaning |
|---|---|---|
| Runtime ProducerWork | Requested → AuthorityChecked → DRegistered (when derivative-capable) → Queued → Leased → Running → Completed / Suppressed / Failed | Lease expiry, timeout, worker loss and DLQ are non-terminal until durable no-more-publication disposition is established |
| Runtime Derivative | Planned → BuildingPrivate → LineageRegistered → GatePending → VisibleProjection → Invalidated / Quarantined → Retired | VisibleProjection is only an F projection; never canonical truth or Forget completion |
| Queue item | Enqueued → Leased → Running → Acked / RetryScheduled / Quarantined / Cancelled | Queue ACK means local handling only; it does not prove indexing completeness or D barrier closure |
| Recall request | Admitted → CandidateSearch → AuthorityFiltered → CanonicalRevalidated → Ranked → FinalGate → Returned / Suppressed / Unknown | Only exact, current, authorized refs can cross FinalGate |
| Working Set / F Context | Created → PopulatedByRefs → Materialized → Active → Invalidated → Cleared / Quarantined | F Working Set is not G ContextVersion and has no Applied semantics |
| Restore unit | Discovered → Isolated → AuthorityReconciled → ReplayValidated → Rebuilt → GateEnabled | Never serve restored bytes before current I/D reconciliation |

## 2. Producer behavior

1. Every F activity that can create, retain, publish or later dereference a derivative is classified and registered with D before enqueue, lease, source dereference or execution.
2. Producer identity is stable across retries: producer class, ProducerWorkItemId, request digest, source refs/revisions, transitive lineage, Scope, admission cursor, observed D fence and I PermissionEpoch. AttemptId and LeaseId are separate and rotate on retry.
3. Pure read-only recall that creates no durable derivative may use the read authorization path; prefetch, cache fill, index build, graph expansion and retained summaries are derivative-capable and require producer registration.
4. Registration timeout is UNKNOWN: resolve by stable identity/digest; never create a new identity to bypass a barrier.
5. D fence installation captures its own producer high-water. Pre-fence work remains accounted until durable terminal/no-publication evidence; post-fence work referencing covered lineage is rejected or quarantined.
6. F cannot invent D receipts, close D's barrier, or claim global Forget completion.

## 3. Derivative behavior

- Every index row/vector/segment, cache entry, graph edge, retrieval summary and persisted Working Set snippet carries exact source/version references, Scope, lineage digest, producer identity, schema/index generation and authority provenance.
- Build into a private generation. Register complete direct and transitive dependencies with D before visibility.
- Final publication/activation must be serialized with D's latest fence and current I permission. If the cross-owner gate is unavailable or ambiguous, keep the generation private/quarantined.
- A derivative is invalidated when any covered source/ancestor is forgotten, permission is revoked, scope changes, source version is superseded, or schema/generation becomes incompatible.
- Rebuild/replay from old snapshots must re-check every source and lineage against current D/I state; successful rebuild and zero search hits are not Forget evidence.
- Physical byte erasure is a separate capability/evidence; F reports logical suppression and its own cleanup evidence only.

## 4. Queue behavior

- Queue records are durable work references, not authority. A queue message contains stable WorkItemId/digest and references to registered source/lineage, not unguarded plaintext as its authority.
- Delivery is at-least-once safe: same identity+digest is idempotent; same identity with changed digest is conflict. Attempt/lease generation fences stale workers.
- Lease expiry, queue deletion, retry exhaustion or dead-lettering never closes a D producer registration.
- Before every lease/run and before every projection visibility transition, refresh current I permission and D fence. Cancel is best-effort; final visibility gate is mandatory.
- Queue restore first quarantines all messages, reconciles producer ledger/high-waters and tombstones, then replays only eligible work. Unknown continuity blocks replay.

## 5. Recall behavior

- Authenticate principal, exact Scope, purpose and environment; obtain current I PermissionEpoch/decision and D fence context before candidate admission.
- Push scope filters into candidate generation; indexes return refs, not trusted content. Suppress stale/cross-scope candidates before buffers, fusion, counts, traces or reranking.
- Re-resolve exact Memory version, lifecycle, lineage and permission through D/I before materialization and again immediately before final return/handoff.
- IndexWatermark is partition-local and contiguous; gaps mean stale/incomplete, never deletion. Missing hit is not proof of absence.
- If authorization/fence/currentness is unknown, suppress affected content and return an explicit incomplete/unknown outcome; never serve stale cache as fallback.
- F does not claim G Context Applied, H adapter purge, C execution, or global Forget completion.

## 6. Context behavior

- F owns only its runtime Working Set and retrieval-local context. It may retain refs and, where authorized, protected snippets; every item remains scoped, versioned and lineage-bound.
- G's ContextId/ContextVersion, desired membership, Delivery and Applied records are external typed inputs to F, never aliases for F cache generation or IndexWatermark.
- F may provide candidate refs, freshness/completeness and materialization evidence to G. G decides Context membership and Applied; F cannot promote a candidate to Context or infer delivery.
- On scope/session/environment switch, invalidate namespace and prevent cross-context cache reuse. Revalidate permission and fence on every protected read.

## 7. Restore and reconnect

1. Restore indexes, caches, queues and Working Sets into an isolated/quarantined namespace.
2. Verify Storage restore evidence and reconcile COC committed prefix plus current I PermissionEpoch/registry and D ForgetFence/lineage/producer high-water; these authorities remain distinct.
3. Replay tombstones/fences through required high-waters; invalidate stale IndexWatermarks and all unproven cache generations.
4. Reconcile each queue item against D registration and current I/D state; stale attempts cannot publish.
5. Rebuild private index generations from eligible canonical sources, register lineage, and pass the current final gate before enabling reads.
6. Reauthenticate reconnecting runtime/session; clear or quarantine old Working Set before restoring a fresh one. Never restore then clean.
7. If any authority, prefix, lineage or participant continuity is unknown, keep affected partitions/queues/contexts suppressed. RestoreReconciliationReceipt is not IndexWatermark, D clearance, I authorization or Forget completion.

## 8. Required evidence and tests

F emits per-partition watermark/coverage, producer registration references, derivative lineage digest, queue disposition, cache/Working Set invalidation generation, recall suppression counts and restore reconciliation outcome. It must not overstate byte deletion or cross-owner completion.

Required tests: fence-vs-build race; revocation-vs-final-return race; duplicate/changed-digest queue delivery; lease expiry and stale worker; lost invalidation; partition gap; pre-fence snapshot rebuild; restore with stale replica; reconnect with old Working Set; unknown D/I authority. Tests are specifications until actually executed.

## 9. Non-goals / blockers

- No canonical Memory writes or Forget decisions.
- No ownership of G ContextVersion/Applied, H ACK, C execution, I policy, or D barrier.
- D/E/Storage atomic register-before-visible interface remains a blocking dependency where a derivative can become externally visible.
- **No runtime implementation, conformance PASS, physical erasure proof or production activation is claimed.**


## 10. Phase 3.7 cross-owner reconciliation amendments (EN)

**Disposition:** F-local amendment proposal for LIF-01/04/05/07/08/09/10/11. It does not assert independent approval by another Owner, freeze a shared schema, or claim implementation conformance.

### 10.1 Producer admission and derivative boundary
- A local F ProducerClass declaration is descriptive only. Before derivative-capable work, F MUST resolve a D-issued, versioned, enabled ProducerClass registration whose owner, source-reference classes, output/derivative classes and capability (normal, replay, rebuild, cleanup-only) cover the operation.
- F MUST retain a D RegistrationReceipt bound to stable ProducerWorkItemId and canonical request digest before queue insertion, lease, protected source dereference, execution, retry/replay or publication.
- The no-registration Recall exception is limited to bounded, non-persistent, non-derivative reads. It MUST NOT retain excerpts, populate reusable caches, prefetch, embed, summarize, expand graphs, persist Working Set items, enqueue replayable work or create reusable output. Any such effect requires registration first.
- Unknown registration blocks execution and is resolved using the same identity/digest; no replacement identity may evade a fence.

### 10.2 Partition evidence and terminality
- IndexWatermark is an F partition-local contiguous coverage statement, not a D producer high-water, D barrier disposition, global cursor, proof of source absence or Forget completion.
- Gaps, truncation, stale replicas and unknown coverage mean INCOMPLETE/UNKNOWN. Zero hits are not deletion evidence.
- ACK, DLQ, lease expiry, retry exhaustion, worker death, cancel request, missing queue row and F-local Completed do not close D's barrier. F supplies durable no-later-publication evidence; D alone accepts terminal disposition.

### 10.3 Current authorization and restore
- I authorization and D fence/lineage are independent authority decisions. F MUST revalidate current I authorization and D eligibility at each protected source read, materialization, cache/Working Set access, derivative registration and final visibility/return boundary. Historical receipts or cached ALLOW are not perpetual authority.
- Restore requires a conjunctive gate over independent Storage/DB-incarnation, COC-prefix, I-policy/revocation/registry, D-fence/lineage/producer-ledger and F partition/invalidation proofs. Preserve each issuer, audience, signature, schema and opaque authority-local position. No scalar aggregate high-water or cross-authority numeric comparison is permitted.
- Restored bytes, queues, caches, indexes and Working Sets remain quarantined until required proofs are current and complete, tombstones replayed, dependencies reconciled and the F final gate succeeds. Unknown coverage remains non-serving.
- F Working Set, E frozen compiler input bundle and G ContextVersion are distinct nominal types.

## 10. Phase 3.7 跨 Owner 对齐修订（中文）

**处置：** 本节将 LIF-01/04/05/07/08/09/10/11 纳入 F 本地合同。它不代表其他 Owner 已独立批准，不冻结共享 Schema，也不声称实现符合性。

### 10.1 Producer 准入与 Derivative 边界
- F 本地 ProducerClass 声明仅用于描述，不能授予生产权限。Derivative-capable 工作开始前，必须取得 D 签发、具备版本且启用的 ProducerClass 注册；其 Owner、SourceRef 类型、输出/Derivative 类型及能力（normal、replay、rebuild、cleanup-only）必须覆盖该操作。
- F 必须在入队、租约分配、受保护源读取、执行、重试/重放或发布前，取得并保存绑定稳定 ProducerWorkItemId 与规范请求摘要的 D RegistrationReceipt。
- 免注册 Recall 例外仅限有界、非持久、非 Derivative 的只读操作。不得保留摘录、填充可复用缓存、预取、生成 Embedding/Summary、扩展图、持久化 Working Set、入队可重放任务或产生可复用输出。存在任一此类效果即必须先注册。
- 注册结果未知必须阻断执行，并使用相同身份/摘要解析；不得更换身份绕过 Fence。

### 10.2 分区证据与终态
- IndexWatermark 仅表示 F 单个分区的连续覆盖情况，不是 D Producer High-water、D Barrier 处置、全局游标、源不存在证明或 Forget 完成证明。
- Gap、截断、陈旧副本及未知覆盖均表示 INCOMPLETE/UNKNOWN。零命中不能作为删除证据。
- ACK、DLQ、租约过期、重试耗尽、Worker 死亡、取消请求、队列行缺失及 F 本地 Completed 均不能关闭 D Barrier。F 只能提供持久化的“不会再发布”证据；仅 D 有权接受终态处置。

### 10.3 当前授权与 Restore
- I 授权与 D Fence/Lineage 是两个独立权威决策。F 必须在每次受保护源读取、物化、缓存/Working Set 访问、Derivative 注册及最终可见/返回边界重新验证 I 当前授权和 D 当前资格。历史 Receipt 或缓存 ALLOW 不是永久授权。
- Restore 必须采用独立证明的合取门：Storage/DB incarnation、COC prefix、I policy/revocation/registry、D fence/lineage/producer ledger，以及 F 分区/失效覆盖证明。每份证明保留自己的签发者、受众、签名、Schema 和权威域内不透明位置；禁止合成单一 High-water 或跨权威数值比较。
- 恢复字节、队列、缓存、索引和 Working Set 在必要证明完整且当前、Tombstone 已重放、依赖已核对、F 最终门通过前必须保持隔离。覆盖未知时不得 Serving。
- F Working Set、E 冻结编译输入包和 G ContextVersion 是不同名义类型。
