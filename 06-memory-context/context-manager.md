# Memory Context Manager

**Status:** DECIDED ownership boundaries; CANDIDATE coordinator workflow; TO_VALIDATE latency targets  
**Owner:** Session G

## 1. Responsibility

MCM owns desired state of each Brain-managed Context: membership, ordering, entry metadata, budget allocation, immutable versions, reconciliation and delivery intent. It is not an Agent Prompt Builder or Planner. It does not choose Agent actions, execute tools, mutate canonical memories or implement BMCP transport.

## 2. Components

| Component | Owns | Does not own |
|---|---|---|
| Coordinator | Workflow sequencing, transaction boundaries, idempotent orchestration | Domain policy or transport |
| Context Planner | Desired membership, tiers and coverage plan | Agent task planning or F retrieval algorithms |
| Activator Collaboration Port | Candidate intake, activation reason, completeness/uncertainty handshake | Retrieval ranking, indexes or caches |
| Context Editor | Entry operation validation and staged edits | Canonical Memory writes |
| Versioning/Committer | CAS, sequence allocation, immutable snapshot/delta, replay | Adapter applied state |
| Reconciler | Source/policy/delivery drift detection and compensating changes | Canonical fact correction |
| Budget Manager | Resource allocation, sufficiency and compaction assessment | Blind Top-K truncation |
| Delivery Coordinator | Snapshot/Delta intent and acknowledgement correlation | BMCP wire encoding or local prompt mutation |

## 3. Main workflow

1. **Resolve identity:** authenticate via I/H; resolve principal, Agent, instance, session, task, environment and exact Scope. Reject unresolved environment where required.
2. **Authorize:** check read/activate/context-write/deliver permissions and policy epoch. Scope is namespace, not authorization.
3. **Load base:** load Context head, immutable snapshot, entry revisions, tombstones and delivery metadata; verify scope and integrity.
4. **Consume signals:** accept structured telemetry (C/H) and F retrieval/activation outputs. Task/intent are signals, not organization rules. Do not require or persist full CoT.
5. **Validate canonical eligibility:** resolve exact Memory ID/version; verify lifecycle, epistemic status, temporal validity, provenance and permission. Accepted-but-not-Compiled telemetry is not Canonical Memory.
6. **Plan:** derive coverage requirements, tiers, candidates, conflicts, freshness and budget estimate. Record missing evidence and retrieval incompleteness.
7. **Edit:** produce deterministic staged operations; validate all against one base snapshot and policy epoch.
8. **Commit:** idempotency lookup + CAS/serialized writer. Atomically persist Change Set, target immutable Context Version, operation results, audit and outbox intent.
9. **Deliver:** choose Snapshot or Delta relative to Adapter's known base/capability. Reauthorize and check Forget/revocation tombstones immediately before send.
10. **Reconcile delivery:** correlate receipt/ack by Delivery ID, Context ID, target version, Adapter, Context Session, Inference Request and capability epoch. Never infer Applied from timeout or transport success.
11. **Observe:** record lag, coverage, errors and audit. Agent continues independently if Brain delivery is unavailable.

## 4. Transaction boundaries

- **T1 Context commit — atomic:** idempotency record/result, Change Set, immutable target snapshot/version, delta, audit/outbox and head CAS. All durable or none visible.
- **T2 Delivery attempt — separate:** network send may repeat; retries retain logical Delivery ID. Timeout is Unknown, not Applied.
- **T3 Adapter application — external:** Adapter validates and atomically materializes the complete managed region at a future inference boundary, then attests. Brain stores evidence, not a direct view of model internals.
- **T4 Reconciliation — resumable saga:** reauthorize each stage, block invalid data first, create compensating Change Sets, request adapter clearing/replacement and record per-target outcomes. No global atomic transaction across Brain, Adapter and model runtime is claimed.

## 5. Activator collaboration with F

G supplies exact Scope/purpose, task coverage requirements, missing dimensions, prior membership/freshness watermark, budget and blocked canonical refs. F returns candidate Memory ID/version, permitted rendering/evidence refs, activation reason, relevance signals, completeness, uncertainty, truncation and index watermark.

G revalidates authorization and canonical lifecycle. F recommendation is not authorization. Incomplete retrieval is a sufficiency limitation, not proof of absence. Index lag cannot override canonical retraction/Forget.

## 6. Failure behavior

| Failure | Behavior |
|---|---|
| Authorization unavailable/denied | Fail closed; no materialization/delivery |
| Environment ID absent/ambiguous | Reject environment-bound planning |
| F index stale/incomplete | Mark plan incomplete; preserve uncertainty |
| Canonical version changes during planning | Abort or replan against fresh revision |
| CAS conflict | Reload and re-evaluate; never blind overwrite |
| Budget exceeded | Replan/compact/defer/reject; never silently truncate P0 |
| Commit succeeds, publish fails | Outbox retries; committed Context remains queryable |
| Delivery timeout | Unknown; query/reconcile by stable IDs |
| Adapter rejects/partial applies | No full Applied; request Snapshot/repair |
| Forget races with delivery | Tombstone wins; block send/apply |
| Brain unavailable | Agent proceeds under its own policy; no new Applied claim |

## 7. State ownership

Context Lifecycle belongs to MCM; Entry Lifecycle to Context domain/editor; Delivery Lifecycle to Delivery Coordinator/H contract. A Context may be Active while one delivery is Rejected; a delivery may be Applied for v7 while desired head is v9.

## 8. Error categories

IDENTITY_UNRESOLVED, ENVIRONMENT_REQUIRED, SCOPE_MISMATCH, PERMISSION_DENIED, PERMISSION_EPOCH_STALE, FORGET_BLOCKED, CANONICAL_REF_NOT_FOUND, CANONICAL_VERSION_STALE, CANONICAL_NOT_ELIGIBLE, BASE_VERSION_MISMATCH, IDEMPOTENCY_KEY_REUSE, CHANGE_SET_INVALID, BUDGET_EXCEEDED, SUFFICIENCY_INCOMPLETE, RETRIEVAL_INCOMPLETE, DELIVERY_GAP, DELIVERY_EXPIRED, APPLIED_PROOF_INSUFFICIENT, RECONCILE_REQUIRED, CONTEXT_BLOCKED, INTEGRITY_FAILURE. Errors must not reveal unauthorized IDs/content or cross-Scope existence.

## 9. Observability and decisions

Measure planning/commit/delivery latency separately; CAS conflicts; outbox age; stale Context age; reconcile queue age; tombstone propagation lag; budget utilization; sufficiency dimensions; Applied coverage; unknown deliveries; Adapter capability. High-cardinality IDs belong in traces, not metric labels.

- **DECIDED:** atomic T1; external T2/T3; resumable T4 saga; F owns retrieval, G revalidates.
- **CANDIDATE:** single writer per Context with CAS guard and deterministic operation order.
- **TO_VALIDATE:** throughput/contention under multi-Agent updates.
- **OPEN:** physical outbox transaction (engineering), wire schema (H), authorization schema (I).


## 10. Phase 3.5 coordinator and producer-gate workflow

The coordinator must preserve the owner-specific linearization points; a sequence of successful local checks is not a substitute for an atomic visibility gate.

### 10.1 Producer admission and work identity

Before G enables a producer class for Context snapshot/delta, compaction, reconciliation materialization or delivery-intent production, it registers the class/version with D. Before a derivative-capable work item is enqueued, leased, dereferences protected canonical source data or starts execution, G durably registers it through D's semantic RegisterProducerWork contract. The registration binds stable ProducerWorkItemId, canonical request digest, ProducerClass/registry version, exact source refs/revisions and transitive lineage, ScopeRefs, Context/artifact target, admission CanonicalCommitCursor, observed ForgetFenceCursor, current I PermissionEpoch/authorization decision and correlation refs.

Retry retains ProducerWorkItemId/digest; AttemptId and LeaseId change per execution. Unknown registration receipt, D registry gap, stale permission or unavailable current fence means no work admission. G does not assume that a queue entry or lease is a durable D registration.

### 10.2 Context artifact publication

A staged ContextVersion/ChangeSet may be computed privately. Before it is visible as the current Context head or can be included in a sendable Snapshot/Delta, G registers complete dependency lineage with D (including exact canonical refs, source/transitive lineage and G artifact/version identity) and obtains a durable dependency receipt. The final visibility decision must use D PublishDerivedIfFenceCurrent semantics and current I authorization at the same linearizable decision that makes the G artifact visible. If G and D storage cannot implement a shared transaction or proven recoverable prepare/commit protocol, the staged artifact remains private; G must not advance the public Context head or deliver it. A local check followed by an independent write is forbidden.

This refines, rather than removes, G's T1 atomicity requirement: the G transaction still atomically persists idempotency, ChangeSet, immutable version, audit and outbox/head decision; the cross-owner fence gate must be part of that visibility decision. The exact storage realization remains OPEN with Storage/Consistency and D.

### 10.3 Updated coordinator sequence

1. Authenticate protected transport context; resolve B typed ActorRef/ScopeRef and I Principal/Producer/Adapter bindings. Never trust payload identity claims.
2. Resolve Context's complete required identity tuple, including EnvironmentRef where relevant; reject ambiguity.
3. Obtain current I PermissionEpoch and action-specific authorization. Obtain current D ForgetFenceCursor for every referenced Memory lineage. These tokens are independent.
4. Load the exact Context head and immutable snapshot; validate integrity, scope fingerprint, policy epoch and existing tombstones.
5. Consume F RetrievalResult/ActivationRecommendation only as immutable proposals. Require exact MemoryRef/MemoryVersionRef, activation rationale, source/evidence refs, uncertainty, completeness/truncation and per-index/per-partition IndexWatermark vector.
6. Reauthorize and resolve each candidate against D canonical state. F ranking, watermark or cache hit is not canonical authority and cannot override Forget/retraction/supersession.
7. Plan task-specific coverage and budget; stage ordered operations against one Base Version.
8. Register G producer work with D before derivative work admission/execution; preserve stable work identity across retries.
9. Register every derivative artifact and complete dependency lineage with D before visibility.
10. Atomically decide the G Context commit with D's final publication/fence gate and current I permission. On missing callable gate or unproven cross-store atomicity, quarantine; do not publish or advance visible head.
11. Create a Delivery intent only for a committed, current, non-expired target. Bind stable DeliveryId and separate AttemptId; reauthorize and recheck fence immediately before each send.
12. H validates delivery and applies only at the next inference boundary; G accepts Applied only from valid C/H Full final-request evidence.
13. Reconcile all timeouts, lost receipts, stale cursors, late ACKs, revocation and Forget using stable IDs; never infer success from elapsed time.

### 10.4 I Forget inventory evidence produced by G

G reports its own registered target slices only. It binds I's TargetId/TargetInventorySeal, ForgetOperationId, exact Context/snapshot/delta/ChangeSet/delivery target, ScopeRef coverage, D fence, I PermissionEpoch, operation/action, pre/postcondition, producer work/attempt, timestamp and integrity evidence. I owns Target State aggregation. G must not mark a target Confirmed merely because it sent a clear request; H action-specific Adapter evidence is separate. Unknown/offline remains unresolved.

### 10.5 Failure and degraded behavior

| Condition | Required G outcome |
|---|---|
| D producer class/work registration unavailable or unknown | Do not enqueue/lease/execute derivative work; retain private pending intent |
| D dependency registration incomplete | Keep artifact private; no Context head advance or delivery |
| D final publication gate unavailable/unproven | Quarantine; no visible Context Version or sendable Snapshot/Delta |
| D ForgetFence unavailable/stale | Block affected Context references and fail closed |
| I PermissionEpoch/current decision unavailable | Block protected read, mutation, publication and delivery |
| F per-partition watermark gap/truncation | Mark plan incomplete; no false completeness or absence inference |
| H final request evidence absent | Delivery remains Delivered/Unknown, never Full Applied |
| H Forget ACK missing/unsupported | G target evidence remains Pending/Unknown; I decides exception/completion |
| Late derivative or invalidated I inventory seal | Reopen G reconciliation and emit updated target evidence; do not silently preserve completion |

### 10.6 Owner boundary

D owns producer registration/fence/publication semantics; Storage/Consistency owns any physical atomicity realization; I owns identity, PermissionEpoch and global target/completion policy; F owns retrieval/index/caches; H owns BMCP and Adapter-local evidence; C owns final-request proof predicates; G owns desired Context state, membership/version and its own reconciliation/delivery intent. This workflow does not create a cross-module transaction or wire schema by assertion.
