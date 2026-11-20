# Compiler State Machine and D Producer Admission Interface

- Document ID: E-PRODUCER-ADMISSION-001
- Version: 1.0
- Source branch: session-e-memory-compiler-2026-11-16
- Source revision: DEREFERENCED — historical source blob `e59f517fff161ab882aa0ddc4a5bda513964ae1a` retained; no current normative source path exists.
- Source: DEREFERENCED — original normative path `04-memory-compiler/compiler-state-and-producer-admission.md` is absent from the current main tree; alternative: [surviving Chinese counterpart](../../zh-CN/04-memory-compiler/compiler-state-and-producer-admission.md) (blob `ac26ce694021aeefd1dbf0db0099903b98387be9`; translation only, not an authoritative substitute).
- Chinese counterpart: [Compiler 状态机与 D Producer Admission 接口](../../zh-CN/04-memory-compiler/compiler-state-and-producer-admission.md)
- Status: E lifecycle semantics CANDIDATE; D semantic operations DECIDED; callable API/transport and Storage atomicity OPEN

# Compiler State Machine and D Producer Admission Interface

**Status:** CANDIDATE E lifecycle/adapter contract; D semantic operation contracts and linearization are DECIDED; callable transport/API binding and Storage atomic realization remain OPEN.
**Owner:** Session E — Memory Compiler.
**Authority boundary:** E owns compiler-internal work/attempt/stage state. D owns Producer Registration ledger, Forget barrier and canonical gate semantics. I owns authorization/PermissionEpoch and global Forget policy. H owns authenticated transport binding. Storage owns physical transaction/visibility realization only when explicitly agreed.

## 1. Identity hierarchy

| Identity | Stability | Meaning |
|---|---|---|
| EventRef | Immutable | One accepted source event |
| AcceptedReceiptId | Immutable | E evidence of durable ingress |
| CompileIntentId | Stable across retries | Logical compilation intent |
| ProducerWorkItemId | Stable across retries of one logical work | D-visible producer registration/barrier identity |
| DerivationRunId | One run; new for recompile | Specific compiler/model/schema execution lineage |
| AttemptId | New for each attempt | Retry/worker execution attempt |
| LeaseId | New for each lease | Time-bounded worker ownership |
| DerivedArtifactRef/version | Immutable per output version | Private staged derivative identity |
| DependencyRegistrationId | Stable idempotency key | D dependency-registration reconciliation |
| PublicationOperationId | Stable idempotency key | Final gate/visibility reconciliation |

IDs are opaque and allocated durably. Payload-supplied IDs are never trusted as authority. A recompile creates a new DerivationRunId and fresh authorization/fence checks; whether D requires a new ProducerWorkItemId or a child registration under the original item is an OPEN D interface decision. It may never bypass the original source lineage or barrier.

## 2. State transitions

```text
Received
  -> Validating
  -> Accepted
  -> D_Registration_Pending
  -> Registered
  -> Queued
  -> Leased
  -> Running
  -> Staged
  -> Dependency_Registration_Pending
  -> DependencyRegistered
  -> Publication_Gate_Pending
  -> Published
  -> Terminal
```

Alternative exits:
- Validating -> Rejected (no Accepted receipt; unless a durable policy-safe rejection receipt is separately defined).
- Accepted / Queued / Leased / Running / Staged -> Cancelled or Suppressed, then Terminal after durable no-publication evidence.
- Running / Staged / dependency pending -> Retry, then Queued with same ProducerWorkItemId and a new AttemptId after fresh authorization/fence checks.
- Retry budget exhausted -> DeadLettered; this is **not terminal** while replay remains possible.
- D canonical write -> CanonicalCommitted is a separate result/evidence axis, not an alias for Published.
- LeaseExpired is an operational condition; it invalidates that lease but does not terminate the work item or remove it from D's barrier.

## 3. Admission and barrier mapping

| E event/state | Required D ledger meaning |
|---|---|
| Accepted | No D admission implied |
| D_Registration_Pending | Request may have committed; E must resolve by stable ProducerWorkItemId/digest |
| Registered | D Registration Receipt exists; barrier high-water/registration identity is durable |
| Queued / Retry / DeadLettered | Same D registration remains open; retry/DLQ does not disappear from barrier |
| Leased / LeaseExpired | D can correlate active/expired LeaseId + AttemptId; expiration is not terminal |
| Running / Staged | D registration remains open; E progress is telemetry, not barrier completion |
| DependencyRegistered | D dependency inventory has every required direct/transitive edge receipt |
| Published / CanonicalCommitted | Durable gate and/or canonical commit evidence recorded independently |
| Cancelled / Rejected / Terminal | E sends durable terminal disposition; D closes barrier item only after validating evidence and no further publication is possible |

D's Forget contract requires every work item admitted before the fence's producer-registration high-water mark to reach a durable terminal disposition. E must never delete a registration, hide a DLQ item or treat a lost worker as completed.

## 4. Required D operation semantics (not API names)

### 4.1 Producer registration

E needs a D operation that durably registers the logical producer work before enqueue or execution. Minimum semantic request fields:

- ProducerWorkItemId, producer class and authenticated ProducerIdentity binding;
- source EventRef(s), and canonical source refs/exact versions when available;
- source/transitive lineage digest or approved opaque dependency token;
- ScopeRefs and security-domain binding;
- operation, correlation and causation IDs;
- admission CanonicalCommitCursor (D-issued current authority position, or an explicit D-defined genesis/empty value if no canonical commit has occurred);
- observed ForgetFenceCursor and I PermissionEpoch;
- request digest, initial AttemptId/LeaseId if applicable, and producer schema/version.

Minimum result: durable ProducerRegistrationReceipt, registration ledger sequence/high-water token and accepted/rejected disposition. Receipt lookup by ProducerWorkItemId + digest must be idempotent.

**OPEN:** D must define how EventRef-only ingress registers before any canonical MemoryRef exists, and whether one logical work item or each attempt/recompile is a separate ledger entry.

### 4.2 Dependency registration

E needs a D operation to durably register each DerivedArtifactRef/version and complete source ancestry before visibility. Minimum request: artifact ref/version, ProducerWorkItemId, DerivationRunId, direct and transitive source refs or I-approved opaque tokens, exact source versions, ProvenanceRef, ScopeRefs, lineage digest, observed fence and idempotency identity. Result: durable DerivedRegistrationReceipt and inventory position.

Duplicate same-key/same-digest registration returns the original receipt. Same key/different digest conflicts. Partial registration remains non-visible. D must define source-reference classes and whether D or a D-designated inventory service is authoritative.

### 4.3 Final Publication Gate

E needs a final D-authoritative gate that checks the latest ForgetFenceCursor and registration inventory, and serializes the result against concurrent fence installation. Minimum request: PublicationOperationId, artifact/version, ProducerWorkItemId, DerivationRunId, AttemptId/LeaseId, all dependency receipt IDs, current PermissionEpoch/authorization decision ref, observed ForgetFenceCursor, ScopeRefs and request digest.

The result must be a durable PublicationReceipt bound to exact artifact/version, dependency receipts, fence generation, permission epoch and visibility outcome. Storage must not expose the artifact until the gate's committed success is proven.

**OPEN:** D must define whether the gate itself performs the visibility transition, or issues a single-use fencing token consumed by Storage under a shared transaction/CAS. A token followed by an uncoordinated write is not sufficient.

## 5. Failure semantics

- Admission ACK loss: query same work ID; never enqueue while unknown.
- Worker crash/lease expiry: D registration stays open; new attempt must refresh permission/fence.
- Dependency ACK loss: query stable dependency key; artifact stays private.
- Partial dependency writes: resume idempotently; no partial publication.
- Publication ACK loss: artifact stays private until lookup proves commit.
- Fence or PermissionEpoch advances: stale lease/attempt rejected; no generation refresh can legitimize the same stale result.
- DLQ: barrier-open until explicit terminal acknowledgement or authorized replay.
- Late result: discard/quarantine; cannot overwrite a newer or terminal state.
- Restore: apply current fence before any staging or derived object is made queryable.

## 6. Observability

Required telemetry: EventRef, AcceptedReceiptId, CompileIntentId, ProducerWorkItemId, DerivationRunId, AttemptId, LeaseId, D registration receipt/high-water, DependencyRegistrationIds, PublicationOperationId/Receipt, observed CanonicalCommitCursor, AggregateRevision refs, LifecycleEventCursor, ForgetFenceCursor, PermissionEpoch, state transition, retry count, terminal disposition, correlation/causation IDs and structured failure class. Never log forgotten content or sensitive locators.

## 7. Conformance cases (NOT RUN)

- D registration precedes queue/lease; admission timeout blocks execution.
- Fence install races registration and exactly one serialized outcome wins.
- D barrier includes queue pending, leased, expired, retry, DLQ and replay.
- Lease expiry cannot be counted terminal.
- Dependency registration must be complete before final gate.
- Fence/permission changes between staging and gate reject publication.
- ACK loss at each boundary resolves to the same receipt.
- Recompile creates new provenance/run identity and cannot bypass source fence.
- Late result cannot publish after terminal/cancel.
- D and E state transitions reconcile after crash/restore.

**No runtime interface or implementation is claimed by this document.**



---
## Phase 3.5 — Producer Work Lifecycle and Admission Refinement

**Status:** E-owned lifecycle semantics are CANDIDATE; D operation schemas and D/E/Storage linearization remain OPEN. No runtime implementation is claimed.

### A. Producer-class registration versus work-item registration

Producer-class registration and per-work-item admission are distinct:

- **ProducerClass** identifies a derivative-capable producer boundary: compiler ingress, extraction/consolidation, retry scheduler, DLQ replay worker, operator replay/recompile worker, and any E-owned outbox dispatcher that can cause derivative work.
- **ProducerClassRegistration** is a D-owned closed-world inventory declaration. It binds a stable class ID/version, owning module, authenticated ProducerIdentity class, source/derivative capabilities, Scope coverage, enabled/disabled state and registration schema. E must not execute a derivative-capable path until D confirms the class is registered and active.
- **ProducerWorkItem** is one logical, durable unit admitted under a registered class. Its stable ProducerWorkItemId is persisted before queue insertion, lease acquisition or execution.
- D's contract names RegisterProducerWork for per-work registration. Whether class registration has a separate D operation, and its exact request/response and version-transition semantics, is **OPEN-D-CLASS-01**. E does not invent that API.

### B. Required E lifecycle and identity rules

| Lifecycle concern | E rule | D barrier consequence |
|---|---|---|
| Initial admission | Persist CompileIntent + stable ProducerWorkItemId, then obtain durable D registration receipt before enqueue | D ledger contains work before execution |
| Lease acquisition | New LeaseId + AttemptId; bind worker identity, expiry, observed PermissionEpoch and ForgetFenceCursor | Existing work remains open; lease is evidence, not a new admission |
| Lease renewal | Same LeaseId/AttemptId; renew only after current authorization and fence revalidation; persist renewal result | Renewal cannot move admission beyond a fence or erase barrier membership |
| Lease expiry | Mark lease expired; preserve work item and attempt history; reconcile owner/heartbeat before takeover | Expiry is never terminal and cannot close barrier |
| Retry | Same ProducerWorkItemId and CompileIntentId; new AttemptId and LeaseId; fresh authorization/fence check | Same barrier member remains open |
| DLQ | Durable parked record with reason, source lineage and replay policy; D registration remains open | DLQ is not terminal while replay remains possible |
| DLQ replay | New AttemptId/LeaseId, same ProducerWorkItemId; resolve D registration by same ID/digest before dispatch | Replay cannot escape original barrier |
| Operator replay | Authenticated, authorized action; preserve source lineage and work ID; audit operator/reason | No unregistered side channel |
| Recompile | New DerivationRunId and immutable output identity; current policy/fence checks; link to original intent/run. Whether child attempt or separately registered child work is OPEN-D-RECOMPILE-01 | Never bypass source ancestry or prior fence |
| Terminal disposition | Durable no-further-publication assertion plus reconciliation of all outputs/dependencies/publication outcomes | D closes barrier item only after accepting terminal evidence |

Attempt identity is immutable and append-only. A retry/recovery never reuses AttemptId; a lease renewal never creates a new logical work item. WorkItem identity is not recomputed from payload text and is never deleted to hide a stuck item.

### C. Terminal disposition vocabulary

E may submit these explicit terminal dispositions to D, with evidence:

- PUBLISHED_ALL_OUTPUTS: every output has a durable dependency receipt and PublicationReceipt; no unaccounted staged output remains.
- CANONICAL_COMMITTED: D CanonicalCommitReceipt is durably resolved for the named canonical operation; this does not imply derived projection publication.
- CANCELLED_NO_OUTPUT: cancellation is durable and no output was produced or can still be produced.
- SUPPRESSED_NO_PUBLICATION: fence/authorization denial is durable; staged outputs are quarantined/invisible and all publication attempts are disabled.
- REJECTED_PERMANENT: policy/schema/source rejection is final, with no replay path left enabled.
- FAILED_PARKED: not terminal while replay or recovery remains possible; use only as a nonterminal DLQ status.

A terminal assertion must include ProducerWorkItemId, registration receipt, terminal disposition, all DerivationRunIds/AttemptIds, output inventory digest, dependency/publication/canonical receipt references, latest observed fence and permission decision refs, timestamp, reason and evidence digest. D owns acceptance of terminal evidence. E must not mark a D barrier item closed based only on its local state.

### D. Crash/recovery invariants

1. Recover Accepted/CompileIntent/outbox before dispatch; do not infer successful D registration from a local queue row.
2. On lost RegisterProducerWork ACK, query by ProducerWorkItemId + request digest; while outcome is unknown, do not lease or execute.
3. On lost dependency-registration ACK, query the same DependencyRegistrationId + digest; staged artifact remains private.
4. On lost publication ACK, query the same PublicationOperationId; do not expose until committed success is proven.
5. On process crash after D registration, reconstruct work from durable intent + D receipt; keep the same work identity.
6. On worker crash, expire/revoke the lease and create a new AttemptId only after current authorization/fence checks.
7. On restore, reconcile current D fence and I PermissionEpoch before any staged artifact or replay is queryable.
8. Outbox and DLQ replay are at-least-once; stable identities and idempotency, not queue exactly-once assumptions, prevent duplicate effects.

### E. OPEN items owned outside E

- OPEN-D-CLASS-01: D operation/schema and ordering for ProducerClass registration, class disable/revocation and class-registry version.
- OPEN-D-REG-02: exact RegisterProducerWork request/response, high-water token, duplicate/conflict errors, and serialization with InstallForgetFence.
- OPEN-D-RECOMPILE-01: whether recompile is a child work registration or a new ProducerWorkItemId linked to original lineage.
- OPEN-D-TERMINAL-01: D's accepted terminal-disposition schema and evidence validation rules.
- OPEN-I-AUTH-01: exact authenticated ProducerIdentity/ActorRef/ScopeRef binding remains subject to B/I/H agreement; B Fact/Claim remains ADR-BLOCKED.
- OPEN-STORAGE-01: durable lease, staging, outbox, dependency and visibility transaction implementation is not selected or tested.



---
## Phase 3.5 Addendum — D Registry and Barrier Snapshot Consumption

E's ProducerClass registration is not merely local configuration. Before derivative-capable work is admitted, E must hold a D ProducerClassRegistrationReceipt proving the class is ENABLED under a committed ProducerRegistryVersion. A local allow-list cannot substitute for D's closed-world registry. Disabling a class blocks new work but does not erase or terminalize existing work.

D's ProducerWork RegistrationReceipt includes ProducerRegistrationSequence and ProducerRegistryVersion. The sequence/high-water is a producer-ledger namespace, not CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor or ForgetFenceGeneration. E stores it unchanged and uses it only as D directs.

D InstallForgetFence captures ProducerRegistryVersion and ProducerRegistrationHighWater in the same durable linearization point that makes the fence effective. CaptureProducerRegistrationHighWater returns an immutable BarrierSnapshotReceipt tied to that installation; it is a verification/read operation, not a second or movable cutoff.

E recovery uses D ResolveProducerWork with the original ProducerWorkItemId and registration digest. D ReconcileForgetBarrier is the authoritative D-local roll-up over immutable barrier/dependency/target checkpoints. E supplies its receipts and terminal evidence; it cannot independently assert DRAINED or global completion.

D's normative operation set also includes RegisterProducerClass, CaptureProducerRegistrationHighWater, ResolveProducerWork and ReconcileForgetBarrier in addition to RegisterProducerWork, InstallForgetFence, RegisterDerivedDependency, PublishDerivedIfFenceCurrent and CompleteProducerWork. Exact D semantic operation contracts are consumed from D's operation-level specification; API transport schemas remain OPEN.



---
## Phase 3.5 Addendum — Producer Admission OPEN Item Correction

D's current operation-level specification already defines ProducerClass and ProducerWork registration inputs, outputs, idempotency, semantic errors and linearization. It also defines InstallForgetFence's captured ProducerRegistryVersion + ProducerRegistrationHighWater, CaptureProducerRegistrationHighWater's immutable snapshot receipt, ResolveProducerWork and ReconcileForgetBarrier. Accordingly, any earlier OPEN wording suggesting these D semantic elements are absent is SUPERSEDED.

The remaining OPEN work is limited to:
- callable API/transport schema and authenticated B/I/H identity serialization;
- global completeness reconciliation between D's local ProducerClass registry and I/A producer/recipient inventories;
- E's explicit recompile child/re-admission identity rule;
- assignment and validation of the Storage/Consistency implementation owner and shared serialization/visibility boundary;
- executable crash/race/fault tests and retained evidence.

E must consume D's semantic fields unchanged. In particular, ProducerRegistrationSequence is the ordering position used for barrier inclusion; ProducerRegistryVersion identifies the class registry snapshot. Neither is a CanonicalCommitCursor or ForgetFenceGeneration.


---

## Phase 3.5 Revalidation — Producer Lifecycle and D Semantic Consumption

This section supersedes earlier wording that could imply D has not defined semantic operation inputs, outputs, idempotency, errors or linearization. D's authoritative semantic source is `03-memory-brain/forget-fence-operation-and-publication-gate.md`; cursor authority is `commit-cursor-semantics.md`. E consumes those semantics without inventing callable API or wire schemas.

| Lifecycle element | Identity / state | Required E behavior and D barrier effect |
|---|---|---|
| ProducerClass registration | Stable ProducerClassId + contract version; D registry status | Separate from WorkItem registration. Only D-confirmed ENABLED class admits work. Unknown/disabled/incomplete registry fails closed. |
| WorkItem registration | Stable ProducerWorkItemId + request digest + D RegistrationReceipt | Durable registration before enqueue, lease, protected dereference or execution. Same ID/digest returns same receipt; changed digest conflicts. |
| Lease acquire/renew | LeaseId + monotonic lease epoch/expiry | Conditional current-owner lease; revalidate identity, PermissionEpoch and ForgetFence. A lease is not new admission authority. |
| Lease expiry | Attempt/lease expired; WorkItem remains open | Invalidates that attempt only. Never terminal or barrier closure. |
| Attempt identity | New AttemptId per execution attempt | Append-only audit identity; never replaces WorkItemId. |
| Retry | Same WorkItemId; new AttemptId | Reuse D registration; recheck current authorization/fence. Never create a second logical registration for retry. |
| DLQ | Same WorkItemId and lineage, durable failure reason | Remains barrier-open while replay/publication is possible. Parking/deleting queue entry is not terminal. |
| Replay | Same WorkItemId, new AttemptId, original source/receipt refs | Reauthenticate and reauthorize; recheck fence before dereference, staging, dependency registration and publication. |
| Recompile | New DerivationRunId linked to original source/intent | D requires explicit linked child/re-admission decision. Whether a distinct child ProducerWorkItemId is required remains OPEN-RECOMPILE-01. |
| Terminal disposition | D ProducerWorkTerminalReceipt + all output/attempt evidence | CompleteProducerWork only after every output is published with receipts or suppressed/quarantined and no attempt can later publish. |

Normal path: `REGISTERED → QUEUED → LEASED → RUNNING → STAGED → DEPENDENCY_REGISTERED → PUBLISH_PENDING → PUBLISHED`. Retry returns to QUEUED under the same WorkItemId and a new AttemptId. DLQ/lease expiry are non-terminal. A suppression/quarantine terminal path requires durable proof that no future publication is possible.

**DECIDED by D:** ProducerClass/WorkItem distinction; RegisterProducerWork/InstallForgetFence shared ordering; immutable ProducerRegistryVersion + ProducerRegistrationHighWater; dependency durability before visibility; final publish linearization; terminal/reconciliation receipts. **OPEN:** callable transport/API and wire errors; H/B/I identity serialization; I PermissionEpoch current-decision binding; I global inventory reconciliation; exact recompile child identity; named Storage owner and validated atomic realization; executable conformance. No endpoint or implementation is claimed to exist or pass.


---

## Phase 3.6 — Fence-Enforced Producer Work Protocol

**Status:** E producer execution contract defined; D semantic operations consumed; Storage serialization/visibility realization and D/Storage owner confirmation OPEN. **Implementation NOT VERIFIED.**

### 1. Stable work identity and attempt model

The logical producer work identity is immutable across the entire recovery/reprocessing lifetime:

- **ProducerClass**: D-registered, versioned, enabled producer capability class. E's compiler ingress, extraction/normalization, consolidation, retry scheduler, DLQ replay, worker recovery, outbox dispatcher, rebuild/recompile initiators are separately declared capabilities as required by D/I inventory policy. A local E allow-list is not admission authority.
- **WorkItemId / ProducerWorkItemId**: one stable identity for the logical source-to-derived work obligation. It is created and persisted before dispatch. It remains unchanged through retry, DLQ, replay, recompile, outbox replay, lease expiry, worker recovery and process restart. A changed semantic request under the same ID conflicts; a new AttemptId or DerivationRunId never creates a new WorkItemId.
- **AttemptId**: immutable identity for one execution attempt; new for every retry/replay/recovery attempt.
- **DerivationRunId**: immutable identity for one extraction/normalization/consolidation run; a recompile creates a new run linked to the original WorkItemId, accepted source and lineage. It does not mint a replacement WorkItemId. Any D-required child/re-admission operation must preserve the root WorkItemId as the barrier identity and be explicitly confirmed by D before dispatch.
- **RegistrationReceipt**: E stores the D-issued ProducerClassRegistrationReceipt and ProducerRegistrationReceipt separately. The latter binds WorkItemId, canonical request digest, ProducerClass/registry version, source lineage, ScopeRefs, admission disposition and ProducerRegistrationSequence. It is not an AcceptedReceipt, a lease, or a publish permit.
- **Lease**: a time-bounded worker claim bound to WorkItemId, AttemptId, worker identity, LeaseId, lease epoch/expiry, observed ForgetFenceCursor and PermissionEpoch. Lease acquire/renewal is conditional and durable. A lease is never admission authority; expiry invalidates that attempt only.
- **Source MemoryVersion**: exact immutable source MemoryRef + MemoryVersionRef/revision when canonical memory exists; EventRef + immutable payload digest is retained for Event-only ingress. Every recompile/derivative-of-derivative preserves complete source ancestry and lineage digest.
- **ScopeRef**: typed, validated scope binding and security-domain reference. ScopeRef is not permission and payload claims are not credentials.
- **FenceGeneration / ForgetFenceCursor**: D-issued typed fence generation and cursor tuple. E stores them unchanged; it never compares them numerically with PermissionEpoch or other cursors.
- **PermissionEpoch**: I-issued opaque authorization freshness value with an authorization-decision reference. E revalidates through I; it never treats the value as a grant.
- **Dependency Registration**: stable DependencyRegistrationId + canonical digest and D-issued DependencyRegistrationReceipt for the complete artifact/version and all direct/transitive source/parent edges. Same ID/digest resolves to the original receipt; changed digest conflicts.
- **Terminal Disposition**: durable, append-only final work outcome submitted through D CompleteProducerWork and accepted only when D returns ProducerWorkTerminalReceipt. E local completion is not D barrier closure.

### 2. Admission and execution ordering

The required ordering is:

1. Persist immutable ingress/CompileIntent and stable WorkItemId in E's durable acceptance/outbox boundary.
2. Resolve the enabled D ProducerClass registration and current authenticated producer/Scope binding.
3. Call D RegisterProducerWork using WorkItemId + canonical request digest and exact source lineage; resolve any timeout using the same key.
4. Dispatch/queue only after a durable ACCEPTED RegistrationReceipt is confirmed. REJECTED, QUARANTINED, CLEANUP_ONLY, UNKNOWN, missing receipt or registry gap cannot enter ordinary compile execution.
5. Acquire a fresh LeaseId/AttemptId under current I authorization and D fence state. Only then may protected source/evidence/provenance be dereferenced.
6. Execute extraction, normalization and consolidation into private staging. Record source MemoryVersion(s), ScopeRef(s), FenceGeneration observation, PermissionEpoch observation and provenance digest.
7. Register the complete derived dependency set with D. Partial/unknown dependency registration remains private.
8. Invoke the final PublishDerivedIfFenceCurrent operation; the final visibility commit, not a prior check, decides publication.
9. Resolve the authoritative PublicationReceipt, then submit terminal evidence to D. Work is terminal only after every output/attempt/replay path is reconciled.

No E queue insertion, lease, source dereference, execution, retry, DLQ replay, recompile, rebuild-triggered compiler work or publication may bypass D registration and current authorization/fence checks.

### 3. Lease, retry and terminal rules

- Lease renewal retains WorkItemId, AttemptId and LeaseId; it advances only the lease epoch/expiry under a current authorization/fence check.
- Lease expiry revokes the old lease/attempt's ability to publish. Recovery preserves WorkItemId and lineage, creates a new AttemptId/LeaseId, and re-resolves D work state plus current I PermissionEpoch and D ForgetFence before source access.
- Retry and DLQ parking do not close D barrier membership. DLQ is nonterminal while replay or publication remains possible.
- DLQ replay/outbox replay uses the same WorkItemId, CompileIntentId, source EventRef/MemoryVersion and request digest; it creates a new AttemptId and lease, then rechecks all current controls.
- Recompile uses the same WorkItemId and original source lineage, a new DerivationRunId and immutable output artifact/version IDs. It must not mint a new AcceptedReceipt or use a new WorkItemId to evade an old fence. D must explicitly confirm any child-registration representation while preserving root barrier identity.
- Terminal disposition is allowed only after all attempts are revoked/expired, all outputs are either published with receipts or suppressed/quarantined, no dependency/publication outcome is UNKNOWN, no outbox/DLQ/replay path can dispatch, and D accepts CompleteProducerWork. FAILED_PARKED is nonterminal.
- A stale worker may not publish or terminalize after a newer attempt/lease takes ownership. D's final gate validates the active attempt/lease and Storage must serialize that validation with visibility.

### 4. Typed state transitions

`RECEIVED -> DURABLE_INGESTION -> ACCEPTED -> D_REGISTRATION_PENDING -> REGISTERED -> QUEUED -> LEASED -> RUNNING -> CANDIDATE_PRIVATE -> STAGED_PRIVATE -> DEPENDENCY_REGISTRATION_PENDING -> DEPENDENCY_REGISTERED -> PUBLISH_PENDING -> PUBLISHED -> TERMINAL`

Alternative transitions:

- Any ambiguous D operation result: `*_PENDING -> UNKNOWN_RECONCILIATION`; do not advance, dispatch or expose until same operation identity resolves.
- Retry/worker recovery: `RUNNING/STAGED/UNKNOWN -> RETRY_QUEUED`; same WorkItemId, new AttemptId/LeaseId, fresh authorization/fence.
- DLQ: `RETRY_QUEUED -> DLQ_PARKED`; still registered and barrier-open.
- Recompile: new DerivationRunId under same WorkItemId; old run/output evidence remains immutable and linked.
- Fence/permission denial: `*_PRIVATE -> SUPPRESSED_QUARANTINED`; publication disabled; terminal only after durable no-future-publication proof and D acceptance.
- Any partial dependency registration or ambiguous publication: remain private and unresolved.

### 5. E/D evidence separation

E's local states (queued, leased, running, candidate, staged, retry, DLQ) are execution telemetry. D's RegistrationReceipt, DependencyRegistrationReceipt, PublicationReceipt and ProducerWorkTerminalReceipt are authoritative ledger evidence. A local row, queue ACK, object-store presence, lease heartbeat or worker success log cannot substitute for a D receipt.

The D producer-registration sequence/high-water, D ForgetFenceGeneration, D CanonicalCommitCursor and I PermissionEpoch are distinct typed namespaces. E stores each in its own typed field and delegates currentness/coverage evaluation to the issuing authority.
