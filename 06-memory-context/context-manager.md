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
