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
