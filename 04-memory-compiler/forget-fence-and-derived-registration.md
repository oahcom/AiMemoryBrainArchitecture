# Forget Fence, Producer Admission and Derived Publication Contract

**Status:** CANDIDATE E enforcement contract; D canonical semantics are DECIDED; D/E/Storage atomic registration and final publication gate are **OPEN / BLOCKING**. I/H/B contracts are candidate inputs, not frozen schemas.
**Owner:** Session E — Memory Compiler.
**Scope:** E ingress-to-compiler work, derivative lineage, dependency registration, replay and visibility.
**Authority:** D owns ForgetOperation, ForgetFenceCursor, producer-registration ledger/barrier and canonical suppression. I owns Principal/authorization, PermissionEpoch, retention and global completion policy. E owns compiler work lifecycle and enforcement. H owns authenticated transport binding/wire. B owns typed domain-reference semantics. Storage/Consistency must realize the atomic visibility boundary. F owns IndexWatermark; G owns ContextVersion.

## 1. Safety invariant

No compiler-produced artifact, provenance edge, proposal, embedding, excerpt, cache item, outbox payload or other derivative is available to Runtime, canonical readers, retrieval, Context, Adapter or any other consumer until (a) its source lineage is durably registered with D's dependency inventory, (b) a current authorization/PermissionEpoch and D ForgetFence check succeeds, and (c) the authoritative final Publication Gate durably commits.

A staged artifact is private and non-queryable. Queue membership, Accepted Receipt, Compiler Completion, local provenance persistence, D Registration Receipt, or a local precheck alone is not permission to expose it.

If any check, registration, gate result or required authority is unavailable or ambiguous, remain non-visible and fail closed. Logical suppression, asynchronous cleanup and physical erasure remain distinct; E cannot declare global Forget completion or physical deletion.

## 2. D contract consumed from current branch HEAD

Source read: `session-d-memory-brain-2026-11-16@30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6`.

| D-owned contract | D's current semantic decision | E consumption / boundary |
|---|---|---|
| ForgetOperation identity | Durable operation ID; idempotent request key + normalized digest; exact typed targets and target-set digest | E stores and propagates D-issued operation/fence references; never invents Forget IDs or target matching |
| ForgetFenceCursor | `(forget_operation_id, fence_generation, target_set_digest)`; monotonic D generation, distinct from commit cursor and permission epoch | Every worker/attempt records the observed typed fence; refresh latest applicable fence at protected reads and final visibility boundary |
| Producer registry | Closed-world producer-class/registration ledger; every work item registers before execution with stable producer/work ID, class, source refs/revisions, scopes, operation/correlation IDs, admission CanonicalCommitCursor, observed fence and lease/attempt identity | E registers before queue/lease/run; queue insertion is not admission; unknown registration outcome is resolved by stable work ID, never assumed |
| Producer barrier | Fence installation atomically captures producer-registration high-water mark; all pre-fence registered work must reach durable terminal disposition | E keeps registration open through retries, DLQ, replay and late result handling; no item disappears on lease expiry or queue deletion |
| Post-fence admission | New work referencing fenced target/lineage is rejected, quarantined or admitted only as suppression/cleanup work | Requeue/recompile cannot gain legitimacy from a new attempt or current generation; D re-evaluates source ancestry |
| Register-before-visible | Derivative record + dependency edge committed atomically or equivalent durable prepare/commit; final gate rechecks latest fence immediately before visibility | E persists private staged output, registers all dependencies, then requests final gate; no local check-then-publish |
| Target acknowledgements | Target-specific suppression/cleanup/unknown/exception evidence; unknown is not success | E reports only E producer/job/derivative scope; D/I own roll-up and global completion |
| Canonical commit cursor | One global sequence per Canonical Memory authority; independent AggregateRevision and per-Memory LifecycleEventCursor | E stores returned CanonicalCommitCursor unchanged and separately stores aggregate and lifecycle references |
| Transaction visibility | Canonical writes, aggregate head CAS, LifecycleEvent append, CanonicalCommit record and outbox intent share one atomic/recoverable D transaction; cursor visible only after durable commit | E never fabricates commit evidence or cursor; unknown outcome is queried by stable operation key |

**Important precision:** D defines these semantic obligations, not callable API names, request/response schemas or a proven Storage implementation. The E-side labels below describe required operation semantics only; they do not assert that a D API already exists.

## 3. Compiler Work Item identity and lifecycle

### 3.1 Stable identity

- `EventRef`: immutable accepted source event identity; payload corrections are new events/correction links, never mutation.
- `AcceptedReceiptId`: durable E acceptance evidence.
- `CompileIntentId`: stable logical processing intent created with acceptance.
- `ProducerWorkItemId`: stable identity registered with D for one logical derivative-capable work item. It is not an attempt ID and is not recreated by retry.
- `DerivationRunId`: one execution/run lineage; recompile creates a new run linked to the original Event/intent and prior run, subject to current policy.
- `AttemptId` and `LeaseId`: unique per execution attempt/lease. A retry preserves ProducerWorkItemId and creates a new AttemptId/LeaseId.
- `DerivedArtifactRef`: stable identity for one staged derivative; a changed derivation output is a new immutable artifact/version, not overwrite.
- `DependencyRegistrationId` and `PublicationOperationId`: stable idempotency identities for registration and publication reconciliation.

Suggested stable work identity derivation is a persisted opaque ID allocated at acceptance/compile-intent creation, not a recomputed hash of payload text. D must receive the same ProducerWorkItemId on every retry/recovery of that logical work.

### 3.2 State machine

| State | Owner / meaning | D barrier visibility |
|---|---|---|
| Accepted | E: Event + payload reference + idempotency receipt + CompileIntent durably committed | Not yet admitted; no execution allowed |
| Registered | D has durably accepted ProducerWorkItem registration and returned/queryable Registration Receipt | **Yes**; included in D registration ledger/high-water |
| Queued | E: registered intent waiting for dispatch | D registration remains open |
| Leased | E: attempt/lease acquired; includes observed PermissionEpoch and ForgetFenceCursor | D must be able to correlate lease/attempt identity to registered work |
| Running | E: protected reads/extraction/consolidation executing | D registration remains open |
| Staged | E/Storage: immutable output persisted in private staging; not queryable or publishable | D registration remains open |
| DependencyRegistered | Every required source/transitive dependency has a durable D Registration Receipt; no partial set is publishable | D dependency inventory reflects all dependencies |
| Published | Final Publication Gate succeeded; publication receipt is durable and artifact visibility switched atomically | D sees successful terminal disposition only after gate evidence |
| CanonicalCommitted | Separate D evidence confirms canonical write; contains CanonicalCommitCursor + exact aggregate revision refs | D canonical transaction is authoritative; not implied by Published |
| Retry | E: retry scheduled against same work/lineage, new AttemptId; current auth/fence rechecked | Registration remains open; retry is not a new admission bypass |
| DeadLettered | E: parked after retry budget/permanent error; replay may still occur | **Not terminal** while replay/publication remains possible; barrier stays open |
| Cancelled / Rejected | Durable terminal disposition; no publication possible; cancellation/suppression reason recorded | D receives terminal evidence |
| Terminal | E declares work unable to publish again; all outputs are published, canonical-committed, or suppressed/rejected and reconciled | D may count it toward barrier only after durable terminal acknowledgement |

`Published` and `CanonicalCommitted` are separate evidence dimensions: a derivative may be published without being a canonical Memory, and a canonical commit does not imply a derived projection/index has been published. A work item may carry both outcomes where applicable. `DeadLettered` is a parked state, not automatic barrier completion. Lease expiry is not Terminal.

### 3.3 D-observed versus E-internal states

D must observe: producer class; stable ProducerWorkItemId; source refs and exact versions/revisions where applicable; ScopeRefs; operation/correlation/causation refs; admission CanonicalCommitCursor; observed ForgetFenceCursor; attempt/lease identity; durable registration receipt/high-water position; dependency-registration evidence; terminal disposition and evidence.

E internally manages: Accepted, Queued, Running, Staged, Retry schedule, DLQ residence, worker health and stage checkpoints. E may expose these as progress telemetry, but they do not replace D's barrier ledger. D need not mirror every internal substate if its ledger reliably retains the admitted work as open until an explicit terminal acknowledgement.

A pre-fence registration remains in the barrier even if its queue row, worker process or lease disappears. D's barrier may close only after every pre-barrier registration is terminal and every derivative produced by it is registered before visibility.

## 4. Register-before-visible protocol

The following is the required semantic sequence. Names in monospace are E-side operation intents, not existing D API declarations.

1. **Durable ingress:** persist immutable EventRef/payload reference/digest, AcceptedReceipt, idempotency row and CompileIntent/outbox atomically or via proven recoverable WAL. Return Accepted only after durable commit.
2. **Stable work identity:** allocate ProducerWorkItemId and persist it with CompileIntent, source EventRef, source lineage and idempotency context.
3. **D Producer Admission:** submit the work registration to D before enqueue, lease, protected payload dereference or execution. Required fields are listed in §7. Await durable Registration Receipt. If response is lost, query/retry with the same work ID and digest. No receipt/no execution.
4. **Queue and execute:** only a Registered item may be Queued/Leased/Running. Every attempt revalidates authenticated ProducerIdentity, current authorization/PermissionEpoch, Scope binding and latest applicable ForgetFence before payload/source access and at each protected boundary.
5. **Private staging:** write immutable DerivedArtifactRef and provenance in a private staging namespace. Runtime, search, canonical readers and downstream consumers must not enumerate/read staged rows. Staging object-store ACL and metadata state must deny consumers by default.
6. **Dependency registration:** persist complete direct and transitive lineage; submit every dependency to D's dependency inventory. Wait for durable D Registration Receipt(s). Partial registration, timeout or unknown receipt leaves the artifact invisible.
7. **Final authorization/fence check:** refresh current I PermissionEpoch and latest D ForgetFenceCursor against all source ancestors, target refs and ScopeRefs. Cached admission-time values are not sufficient.
8. **Final Publication Gate:** submit the exact artifact/version, work/run/attempt/lease IDs, all dependency receipt IDs, request digest, current PermissionEpoch, observed ForgetFenceCursor and publication operation key. D must atomically/linearly serialize gate acceptance against fence installation and prove registrations are durable.
9. **Atomic visibility:** only after a durable successful Publication Receipt may Storage switch the artifact from private staged to visible. The gate and storage visibility transition must share one transaction/linearizable commit protocol; otherwise a durable prepare/commit protocol must guarantee that crashes and uncertain outcomes leave the artifact hidden until reconciliation.
10. **Terminal acknowledgement:** E records Published/CanonicalCommitted outcomes and sends D a durable terminal disposition only when no further publication from this work item is possible.

A local fence read followed by an independent Storage write is explicitly unsafe. If the final gate cannot be bound to the visibility transition, E must not publish.

## 5. Failure, idempotency and crash recovery

| Failure/race | Required E behavior |
|---|---|
| D admission unavailable/unknown | Do not enqueue or execute. Resolve by ProducerWorkItemId + request digest; never assume admitted |
| Admission ACK lost after D commit | Query same work ID; accept the same D Registration Receipt; no second logical registration |
| Crash after registration, before queue | D ledger remains open; recovery scans registered nonterminal work and re-enqueues same work ID |
| Duplicate Event/message | Same authenticated idempotency namespace + same digest returns original Event/Receipt/CompileIntent/WorkItem; no second effect |
| Same idempotency key, different digest | Conflict; preserve original receipt; do not create work |
| Worker crash / lease expiry | Lease expires but work remains D-registered/open; recover with new AttemptId and recheck current auth/fence before any protected read |
| Crash after staging | Staged output remains private; reconcile dependency receipts and current fence before any further action |
| Partial dependency registration | Remain invisible; retry missing registrations idempotently; do not publish a partial dependency set |
| Registration ACK lost | Query by stable DependencyRegistrationId/derived ref + digest; no duplicate edge or assumed success |
| Gate rejects due to advanced fence/permission epoch | Suppress/quarantine staged output; do not refresh generation and retry as if same work were newly authorized |
| Gate ACK lost | Keep output hidden; query PublicationOperationId. Reveal only on authoritative committed success |
| Crash after gate commit but before E records receipt | Query same PublicationOperationId; record original Publication Receipt; never issue a different publication key |
| DLQ/replay | DLQ preserves EventRef, CompileIntentId, ProducerWorkItemId, lineage and last safe checkpoint. Replay creates a new attempt, not a new authority; reauthorize and recheck fence |
| Recompile | New DerivationRunId and provenance version, linked to original source lineage; new D admission/registration as required by D; forbidden if any ancestor is fenced or retention denies |
| Late result after lease loss/cancel/fence | Discard or retain only private, policy-permitted diagnostic metadata; never publish; D terminal state remains authoritative |
| Permission revoked | Stop protected reads/writes; invalidate lease; no new stage commit, dependency registration or publication unless I authorizes the exact operation |
| ForgetFence advanced | Any old lease/attempt is stale; suppress output and terminally acknowledge; do not rebase old work onto latest fence |
| Restore/rebuild | Reapply current ForgetFence and authorization before making restored staging/derivatives queryable; old queue snapshots are not authority |

Every retry, replay, DLQ requeue and recompile reuses or links to the original source identity and must pass fresh authorization and fence checks. A queue transition never creates permission. A later fence generation is not a substitute for source eligibility.

## 6. Cursor and receipt separation

| Type | Owner / namespace | E use | Never substitute for |
|---|---|---|---|
| SourceEventCursor | E; one declared ingress partition | Durable source acceptance position; replay/resume | CanonicalCommitCursor, AggregateRevision, IndexWatermark |
| CanonicalCommitCursor | D; one globally ordered sequence per Brain authority | Store exact D-returned cursor for canonical commit and as-of reference | Source offset, AggregateRevision, LifecycleEventCursor, IndexWatermark |
| AggregateRevision | D; one aggregate | Store exact immutable Memory/Entity/Relation revision identity/sequence | Global canonical cursor |
| LifecycleEventCursor | D; one Memory lifecycle stream | Store exact lifecycle event position, including enclosing canonical cursor separately | CanonicalCommitCursor or AggregateRevision |
| IndexWatermark | F; index/channel/partition, applied-through CanonicalCommitCursor | Consume only as F's typed acknowledgement | D cursor itself or Forget proof |
| ForgetFenceCursor | D; ForgetOperation + target-set digest + generation | Observe as a fence, compare only within D-defined fence namespace | Any cursor, PermissionEpoch |
| PermissionEpoch | I; defined principal/security-policy namespace | Revalidate current authorization at protected boundaries | ForgetFenceCursor or commit cursor |
| ContextVersion | G; one Context | Treat only as downstream context version | Any E/D cursor |
| Delivery/Adapter identifiers | G/H | Carry opaquely when correlated | Canonical or source cursor |

E's receipts/provenance may carry typed fields only when the corresponding event occurred. A CandidateProposition/ExtractionIR does not carry a fabricated CanonicalCommitCursor. A canonical commit receipt is recorded only after D confirms commit. E does not define or advance F's IndexWatermark.

## 7. D/E/Storage atomic boundary — explicit OPEN interface

D's current contract defines semantic requirements but does **not** publish callable API names, complete request/response schemas, transaction ownership or failure/recovery semantics for the following. The E-side names here are requirements, not claims of existing implementation.

| Required operation semantic | Required input/output evidence | Atomic / linearization requirement | Current state |
|---|---|---|---|
| Producer Work Registration | Input: ProducerWorkItemId, producer class/identity binding, source EventRef + canonical refs/revisions where present, ScopeRefs, operation/correlation IDs, admission CanonicalCommitCursor, observed ForgetFenceCursor, permission/policy epoch, request digest, attempt/lease identity. Output: durable Registration Receipt + D registration high-water/epoch + accepted/rejected disposition | Registration ledger commit must linearize before E queue/lease/execution and be ordered against fence installation | **OPEN — D schema/API + Storage transaction** |
| Dependency Registration | Input: DerivedArtifactRef/version, ProducerWorkItemId/DerivationRunId, complete source/transitive source refs or approved opaque tokens, exact source versions, ProvenanceRef, ScopeRefs, lineage digest, observed fence. Output: durable Derived Registration Receipt(s), registration IDs and inventory position | Dependency edge and derivative registration must be durable before any visibility; duplicate registration idempotent | **OPEN — D ledger API + E/Storage atomicity** |
| Final Publication Gate | Input: PublicationOperationId, artifact/version, work/run/attempt/lease IDs, all dependency receipt IDs, current PermissionEpoch, current ForgetFenceCursor, request digest. Output: committed/rejected result, durable Publication Receipt and authoritative fence/registration evidence | Gate decision must serialize with fence installation and atomically control Storage visibility, or use a proven recoverable prepare/commit protocol that keeps artifact hidden on uncertainty | **OPEN / BLOCKING — D/E/Storage** |
| Producer terminal acknowledgement | Input: ProducerWorkItemId, final attempt/lease, terminal disposition, all output/registration/publication refs, reason and digest. Output: durable terminal receipt / barrier ledger update | D barrier counts item terminal only after durable acknowledgement; no lease expiry/queue deletion implies terminal | **OPEN — D response schema + reconciliation semantics** |
| Current Fence/Permission lookup | Input: exact target/source ancestry and Scope; output: latest applicable ForgetFenceCursor and current I PermissionEpoch/decision | Freshness and consistency guarantee must cover final gate; stale cached values cannot authorize publication | **OPEN — D/I API consistency and epoch lookup semantics** |

### 7.1 Minimum interface questions to D

1. What exact API/command durably registers one ProducerWorkItem, and what fields/typed refs are required for EventRef-only ingress before a canonical object exists?
2. Does D registration cover a logical work item or each attempt separately? How are retry, DLQ, lease replacement and recompile linked without creating an untracked barrier gap?
3. What is the exact receipt identity, registration high-water field/type, producer registry version and lookup-by-idempotency operation?
4. What exact API durably registers a DerivedArtifactRef and every source dependency? Does D require a prepare token before E persists the final artifact row?
5. What operation atomically installs/advances ForgetFence against ProducerWork Registration? What is the linearization order when admission races with fence installation?
6. What exact final gate operation accepts dependency receipts and PermissionEpoch/ForgetFenceCursor, and does it own the visibility flip or return a token Storage must consume?
7. If Storage owns the visibility flip, what shared transaction, lock/CAS, fencing token or transactional outbox protocol makes gate acceptance and visibility one linearizable event?
8. How are ACK loss, timeout-after-commit, duplicate receipt, partial dependency registration, conflicting digest, lease expiry and late result queried/reconciled?
9. What is the durable terminal disposition enum and which DLQ states remain barrier-open?
10. Which source references are valid for D's inventory (EventRef, MemoryRef, MemoryVersionRef, EvidenceRef, opaque token), and how are transitive ancestry and Scope matching validated?

### 7.2 E fail-closed stop conditions

E MUST stop before the affected action when:
- no durable D Producer Registration Receipt can be established;
- D cannot establish the latest applicable ForgetFenceCursor;
- I cannot establish authenticated Principal/ProducerIdentity and current PermissionEpoch;
- ScopeRef semantics or security-domain binding is unresolved for the operation;
- any required dependency registration is missing/partial/unknown;
- final gate and Storage visibility cannot be shown to share an atomic/linearizable boundary;
- a lease/attempt is stale, revoked, expired or fenced;
- a source or ancestor is forgotten, retention-ineligible or not authorized;
- D's barrier ledger reports a gap, unknown producer class or unresolved prior attempt.

No availability fallback, manual queue replay or operator override may bypass these conditions. Only an explicit I-owned policy exception can alter I policy; it cannot invent a D API or erase the need for an auditable D barrier.

## 8. Security and typed identity alignment

- ProducerIdentity is bound to authenticated transport context: authenticated Principal/issuer, registered producer/application identity, instance/workload identity, credential/key validity, permitted event families, tenant/security domain and revocation/credential epoch.
- Payload `producer_id`, `ProducerId`, `ActorRef`, `agent_id` or `scope_ref` is a claim/selector, never authentication. H binds transport principal; I validates trust/policy. Mismatch rejects or quarantines.
- ActorRef is a B/I typed reference to the Principal and authority chain, not a bearer credential. E never accepts caller-constructed ActorRef as proof.
- ScopeRef uses B's typed domain reference semantics. Scope membership/applicability is not a grant; I separately authorizes each source and operation.
- Current PermissionEpoch is rechecked at ingress, before protected dereference, before each sensitive stage commit, before D registration where required, before canonical write submission and at final publication. Admission-time epoch is an observation, not a perpetual capability.
- Idempotency namespace is bound to authenticated Principal + ProducerIdentity + validated Scope binding + tenant/security domain + operation/event family + caller key. Exact field encoding and whether multiple ScopeRefs form a canonical set remain **CANDIDATE / H-I-B approval required**. ScopeRef must not be treated as authorization.
- If authentication, principal binding, Scope resolution, policy epoch, retention or revocation status is unknown, fail closed.

H's message-envelope document and I's Principal/ActorRef contract are CANDIDATE inputs, not frozen wire/policy schemas.

## 9. Conformance scenarios (NOT RUN)

1. A work item cannot be leased before D registration receipt is durable.
2. Forget racing admission is serialized: either registration is in the captured barrier or rejected/quarantined.
3. Every pre-fence work item remains visible to D through worker crash, lease expiry, retry and DLQ.
4. A DLQ item does not count terminal while replay is possible.
5. Derived artifact cannot be read by Runtime/consumer before all dependency receipts and Publication Receipt exist.
6. Forget between dependency registration and final gate rejects stale publication.
7. PermissionEpoch advances between lease and gate; old attempt cannot publish.
8. Duplicate event and lost Accepted ACK return same receipt/work identity.
9. Lost D registration ACK returns same receipt without duplicate registration.
10. Lost Publication ACK leaves artifact hidden until lookup proves committed gate.
11. Late worker result after cancellation/fence cannot become visible.
12. Transitive ancestor Forget suppresses derivative-of-derivative.
13. Cross-scope lineage cannot broaden authorization.
14. Restore/replay reapplies current fence before queryability.
15. Canonical cursor is globally ordered per Brain authority; aggregate revision/lifecycle cursor remain independent; F IndexWatermark is never rewritten by E.

**Acceptance:** design requirements documented only. No runtime implementation, Storage atomicity, conformance test or production safety claim is made.



---
## Phase 3.5 — D-to-E Operation Mapping and Publish Gate Evidence

**Normative boundary:** operation names below are the D operation contract names supplied for this workstream. This section states E's consumption requirements only. It does not declare callable APIs, fill D-owned schema gaps, or prove Storage atomicity.

### 1. D-to-E Operation Mapping

| D operation | E invocation point | Required E inputs/evidence | Required D result consumed by E | E failure behavior / OPEN |
|---|---|---|---|---|
| RegisterProducerWork | After durable Accepted/CompileIntent identity creation and before queue/lease/run; repeat lookup on recovery | Stable ProducerWorkItemId; ProducerClass ID/version; authenticated ProducerIdentity binding; EventRef + canonical source refs/exact revisions where available; lineage digest; ScopeRefs; operation/correlation/causation IDs; admission CanonicalCommitCursor; observed ForgetFenceCursor; PermissionEpoch/decision ref; request digest | Durable ProducerRegistrationReceipt and registration high-water/ledger position; explicit accepted/rejected result | Unknown ACK => lookup same ID/digest, no dispatch. OPEN: exact fields, errors, producer-class registration API, EventRef-only source semantics, high-water type and fence race linearization |
| InstallForgetFence | D-owned Forget workflow; E is a consumer/participant, not the installer | E retains registered work IDs, attempt/lease inventory, lineage, output inventory and latest known registration receipt; consume fence/target/barrier snapshot | Durable fence identity/generation, producer-registration barrier high-water, affected target digest, install commit position and recoverable notification | E stops or quarantines affected work, reconciles pre-barrier items. OPEN: notification/query schema, whether D returns complete per-item barrier snapshot, ordering/consistency SLA |
| RegisterDerivedDependency | After immutable output is staged privately and before any visibility transition | DerivedArtifactRef/version; ProducerWorkItemId; DerivationRunId/AttemptId; direct + transitive source refs/exact versions or approved opaque tokens; ProvenanceRef; ScopeRefs; lineage digest; observed fence; idempotency key/digest | Durable DerivedRegistrationReceipt for every required edge/artifact, plus inventory position and explicit duplicate/conflict result | Partial/unknown registration => artifact remains private; resolve same key/digest. OPEN: authoritative source-ref classes, D vs designated inventory service ownership, atomic batch/partial semantics, exact receipt fields/errors |
| PublishDerivedIfFenceCurrent | Immediately before publication, after all dependency receipts and current authorization are established | PublicationOperationId; artifact/version; ProducerWorkItemId; DerivationRunId; AttemptId/LeaseId; all dependency receipt IDs; source lineage digest; ScopeRefs; current I authorization decision + PermissionEpoch; observed ForgetFenceCursor; request digest | Durable PublicationReceipt bound to artifact/version, exact dependencies, checked fence, permission epoch, visibility result and commit identity | Any stale/unknown fence, auth failure, missing receipt or ambiguous outcome => no visibility; query same operation ID. OPEN: whether D performs visibility commit or issues a single-use token consumed atomically by Storage; cross-store linearization and error taxonomy |
| CompleteProducerWork | Only after all output, dependency, publication/canonical-commit and no-future-publication outcomes are durably reconciled | ProducerWorkItemId + RegistrationReceipt; terminal disposition; all Attempt/DerivationRun IDs; output inventory digest; dependency/publication/canonical receipt refs; observed final fence + auth evidence; terminal request digest | Durable terminal acknowledgement and barrier-ledger state; idempotent same-evidence result or conflict | Lost ACK => lookup same work ID/digest; never locally assume barrier closure. OPEN: terminal enum/schema, required proof completeness, reopen/invalidation behavior for late derivative |

InstallForgetFence is not an E API call. E consumes its durable outcome and ensures every E work item in the captured barrier remains discoverable until terminal acknowledgement. E does not claim authority to install or advance D's fence.

### 2. Required operation ordering

1. Persist AcceptedReceipt + CompileIntent + stable ProducerWorkItemId/outbox.
2. Confirm ProducerClass registration is active (class-registration API remains D OPEN).
3. Call/resolve RegisterProducerWork; do not queue, lease or execute until its durable receipt is known.
4. Acquire LeaseId/AttemptId; revalidate current I authorization/PermissionEpoch and D fence before protected source reads.
5. Execute compile stages and write immutable Candidate/Staged artifacts to private storage only.
6. Build complete direct/transitive dependency set and call/resolve RegisterDerivedDependency for every artifact/version/edge.
7. Reauthorize and fetch/validate the latest applicable fence immediately before gate request.
8. Call/resolve PublishDerivedIfFenceCurrent; visibility transition must share D's specified atomic boundary. If no such proven boundary exists, remain staged/private.
9. Record PublicationReceipt separately from CanonicalCommitReceipt and IndexAppliedAcknowledgement.
10. Call/resolve CompleteProducerWork only when terminal disposition is durable and no retry/replay/publication path remains unaccounted.

### 3. Staging, dependency durability and visibility

- CandidateProposition, ExtractionIR, normalization output, consolidation candidates, embeddings, summaries, provenance edges, outbox payloads and all other derivatives are private until publication succeeds.
- Staging storage MUST be excluded from Runtime retrieval, canonical reads, F indexers, G context builders, H delivery, exports and general-purpose search. “Not linked from UI” is not an access-control boundary.
- Dependency registration is durable and idempotent. A derivative is not eligible for publication until the full required dependency set is acknowledged. Partial success is a private incomplete state, never partial visibility.
- The final gate checks the latest D fence and current I authorization at its linearization point. A precheck, worker lease, earlier generation, cached permission decision or local E database read is insufficient.
- Fence installation and final publication must serialize so that either publication linearizes before fence installation and is included in the barrier/inventory, or fence installation wins and publication is rejected/quarantined. There is no third outcome in which a late derivative becomes visible outside the barrier.
- If dependency registration and visibility cannot be one atomic transaction, only a D-approved durable prepare/commit protocol with recovery and no-visible-before-commit semantics is acceptable. An uncoordinated “D token then Storage write” is not sufficient.
- Any fence/authorization/lineage/receipt failure leaves the artifact private and marks the work blocked/suppressed. E must not silently drop it or report success.

### 4. Publish Gate Evidence bundle

| Evidence | Required binding |
|---|---|
| Work identity | ProducerClass ID/version, ProducerWorkItemId, ProducerRegistrationReceipt, DerivationRunId, AttemptId, LeaseId |
| Source lineage | EventRef, source canonical refs + exact revisions, complete direct/transitive lineage digest, ProvenanceRef, ScopeRefs |
| Authorization | authenticated ProducerIdentity reference, I PolicyDecision reference, PermissionEpoch, action/resource/audience/scope binding, decision validity at gate |
| Forget state | latest D ForgetFenceCursor/generation observed at gate, target-set/lineage applicability result, D gate decision reference |
| Dependency proof | complete list/digest of DerivedRegistrationReceipt IDs and inventory position |
| Publication proof | PublicationOperationId, PublicationReceipt, artifact/version, visibility commit identity/time and result |
| Recovery proof | idempotency request digests, ACK lookup/recovery outcome, correlation/causation IDs |

The evidence bundle proves only the named publication boundary. It is not a global Forget completion proof, physical-erasure proof, F index watermark or G context delivery proof.

### 5. Explicit OPEN contract gaps (do not promote to DECIDED)

- OPEN-E/D-01 RegisterProducerWork: ProducerClass registration/version, EventRef-only ingress, source-revision availability, authenticated producer binding, registration high-water type, exact receipt and duplicate/conflict/error codes.
- OPEN-E/D-02 RegisterProducerWork vs InstallForgetFence: transaction/linearization rule and exact serialization outcomes for concurrent admission and fence install.
- OPEN-E/D-03 RegisterDerivedDependency: authoritative inventory owner, full source-reference type set, transitive closure rule, batch/partial behavior, receipt and retry/error semantics.
- OPEN-E/D-04 PublishDerivedIfFenceCurrent: exact latest-fence read/serialization and authorization check, output/evidence schema, whether gate commits visibility or coordinates a D/Storage CAS/transaction.
- OPEN-E/D-05 CompleteProducerWork: terminal dispositions, terminal evidence schema, late derivative invalidation/reopen behavior, ACK lookup and conflict rules.
- OPEN-E/ST-06 Storage atomicity: atomic dependency registration + visibility, durable prepare/commit alternative, crash recovery, isolation and read-path enforcement are not selected or tested.
- OPEN-E/I/B/H-07 Identity binding: exact ActorRef/ScopeRef/ProducerIdentity schema remains joint B/I/H work; Fact/Claim ADR remains ADR-BLOCKED.
- OPEN-E/I-08 Retention: idempotency/tombstone and replay evidence retention horizon remains I-owned and numerically OPEN.

### 6. Fault and race conformance matrix (design only; NOT EXECUTED)

| ID | Race/fault | Required safe outcome | Evidence required |
|---|---|---|---|
| D-RACE-01 | RegisterProducerWork races InstallForgetFence | Exactly one serialized outcome: included at/below captured barrier, or rejected/quarantined; never untracked admitted work | D registration receipt/high-water, fence barrier snapshot, transaction ordering result |
| D-RACE-02 | Queued work exists when fence installs | Queue item remains in D barrier; cancel/quarantine or drain to durable terminal disposition | Work ID, queue/outbox state, terminal ACK |
| D-RACE-03 | Leased/in-flight compile completes after fence | Final gate rejects; staged output stays private and is suppressed/quarantined | Attempt/Lease IDs, observed/current fence, gate denial, private-stage proof |
| D-RACE-04 | Retry scheduler fires after fence | Same work ID remains barrier-open; new attempt rechecks current fence/auth and cannot publish stale lineage | Retry event, new AttemptId, registration lookup, denial/terminal evidence |
| D-RACE-05 | DLQ replay after fence | Replay is registered/reconciled under original lineage and rejected/quarantined for forgotten source | DLQ item, replay AttemptId, fence result |
| D-RACE-06 | Lease expires during fence drain | Expiry does not close barrier; recovery creates new attempt or explicit terminal evidence | Lease history, unresolved work ledger, recovery/terminal ACK |
| D-RACE-07 | Partial dependency registration | Artifact remains private; resume same idempotency keys or quarantine | Per-edge receipts, missing-edge set, no-visible assertion |
| D-RACE-08 | Fence advances after staging but before final gate | Latest fence wins; publication denied | staged artifact, fence generations, gate result |
| D-RACE-09 | PermissionEpoch revoked/advanced before gate | Authorization fails closed; no visibility even if Forget fence unchanged | PolicyDecision, old/current epoch, gate denial |
| D-RACE-10 | Late derivative discovered after barrier/proof | Immediately suppress; register target, invalidate/reopen proof and alert D/I; no silent completion | lineage, discovery time, new dependency entry, invalidation event |
| E-FAULT-11 | Compiler process crashes after D registration | Recover same ProducerWorkItemId and intent; never create untracked duplicate | registration receipt lookup, recovery log, attempt sequence |
| E-FAULT-12 | Outbox replay duplicates dispatch | At-least-once replay resolves same work/receipt; no duplicate logical work or side effect | outbox event ID, work ID, idempotency digest, duplicate result |
| E-FAULT-13 | DLQ replay repeated or concurrent | Same work ID; distinct attempts; one terminal/publish result, duplicates reconcile idempotently | DLQ ID, AttemptIds, gate/publication receipts |
| E-FAULT-14 | Recompile after Forget | New DerivationRunId cannot bypass original source lineage; D rejects/quarantines forgotten ancestry | original EventRef/work ID, prior run, new run, current fence decision |
| E-FAULT-15 | Duplicate AcceptedReceipt submission | Same authenticated namespace + same semantic digest returns original receipt/intent; no duplicate admission | receipt ID, idempotency key/digest, existing work identity |
| E-FAULT-16 | Lost RegisterProducerWork ACK | No enqueue/lease until lookup by same ID/digest proves durable registration or rejection | request digest, lookup response, dispatch hold |

These cases are specification acceptance criteria only. No runtime test, fault injection, race execution or implementation conformance is claimed.



---
## Phase 3.5 Addendum — Exact D Operation Set Alignment

This addendum supersedes the abbreviated five-row operation inventory in §1 above where D's newer normative operation contract defines additional operations and more precise semantics. D operation source: 03-memory-brain/forget-fence-operation-and-publication-gate.md on session-d-memory-brain-2026-11-16 (blob 2c5b1358ff58f99af838b741a75966ccd07ad088). D's decision log records D35-01 through D35-10. These are D semantic decisions, not proof of a callable API or Storage implementation.

| D normative operation | E consumption / production | D durable result / key semantics | E error/recovery handling |
|---|---|---|---|
| RegisterProducerClass | E registers compiler, extraction/consolidation, replay, recompile and other derivative-capable producer classes before accepting derivative work | ProducerClassRegistrationReceipt, ProducerRegistryVersion, ENABLED/DISABLED/QUARANTINED status and effective registry sequence; key class ID + version + digest | Unknown/disabled/incomplete class fails closed; existing work remains tracked after disable. OPEN: global inventory reconciliation with I/A and exact H/B identity binding |
| RegisterProducerWork | E registers stable logical work before queue, lease, source dereference or execution | RegistrationReceipt with ProducerRegistrationSequence, ProducerRegistryVersion, admission fence observation and ACCEPTED/REJECTED/QUARANTINED/CLEANUP_ONLY disposition; key WorkItemId + canonical digest | Same ID/digest resolves same receipt; changed digest conflicts. Registration/fence race follows D's single linearizable order. EventRef-only ingress is supported, but E must link exact canonical refs/revisions once available |
| InstallForgetFence | D installs; E consumes and reacts | ForgetFenceCursor + installation CanonicalCommitCursor + captured ProducerRegistryVersion + ProducerRegistrationHighWater + target snapshot/watermark + outbox intent; key ForgetOperationId + target/request digest | E must stop/reconcile covered work. Fence installation and registration are one D serialization domain. E does not install or advance fences |
| CaptureProducerRegistrationHighWater | E consumes the immutable snapshot receipt during reconciliation | BarrierSnapshotReceipt with the exact high-water, registry version, target digest, fence generation and ledger consistency proof; key fence + snapshot key | Repeated capture cannot advance cutoff. Missing/gapped snapshot => UNKNOWN/blocked; never approximate the high-water |
| RegisterDerivedDependency | E registers every staged artifact and complete lineage before visibility | DependencyRegistrationReceipt + inventory position; key DependencyRegistrationId + canonical digest; complete direct/transitive refs, parent artifact receipts, provenance, scope, fence and permission evidence | Partial/unknown edge set remains private; same key/digest lookup; different digest conflicts; immutable changed lineage requires new artifact version |
| PublishDerivedIfFenceCurrent | E submits complete gate evidence immediately before visibility | PublicationReceipt binds registration, class/version, work/attempt/lease/run, source revisions, scope, observed + authoritative fence, I PermissionEpoch decision, every dependency receipt, artifact and visibility commit identity; key PublicationOperationId + digest | Gate linearizes with visibility and latest fence + current permission. Fenced/stale/incomplete/permission/storage-unavailable outcomes remain private. No independent check-then-write or delayed unbound token |
| CompleteProducerWork | E submits terminal disposition only when no publish/replay path remains | ProducerWorkTerminalReceipt, barrier state, unresolved-output count and reconciliation cursor; key WorkItemId + terminal digest | Terminal is monotonic; same digest idempotent; conflict returns terminal conflict. Lease expiry, queue deletion, worker shutdown and DLQ parking are not terminal |
| ResolveProducerWork | E uses after lost ACK, timeout, crash or restore | Authoritative registration/dependency/publication/terminal receipts, current lease/attempt and barrier membership; read-only key WorkItemId + original registration digest and optional operation IDs | UNKNOWN/ledger unavailable remains fail-closed; lookup never creates work or advances fence; reuse original IDs/digests |
| ReconcileForgetBarrier | E supplies evidence and consumes D barrier disposition | BarrierReconciliationReceipt with exact high-water, included/terminal/open/expired/DLQ/unknown counts, dependency watermark, late-derivative count, registry gaps and DRAINED/OPEN_WORK/OPEN_DEPENDENCY/REGISTRY_GAP/LATE_DERIVATIVE/UNKNOWN; key fence + snapshot/checkpoint | Append-only checkpoints; any late derivative/gap reopens reconciliation. D asserts D-local barrier only; I decides global completion |

### D operation error semantics consumed by E

E must preserve typed non-success outcomes rather than flattening them into generic retry success:

- Producer class/admission: UNKNOWN_PRODUCER_CLASS, CLASS_DISABLED, REGISTRY_INCOMPLETE, FENCE_CLOSED, FENCE_UNKNOWN, PERMISSION_STALE_OR_DENIED, SCOPE_INVALID, SOURCE_LINEAGE_INVALID, IDEMPOTENCY_CONFLICT.
- Fence/snapshot: FENCE_STATE_CONFLICT, SERIALIZATION_RETRY_EXHAUSTED, FENCE_NOT_INSTALLED, FENCE_MISMATCH, LEDGER_GAP, SNAPSHOT_UNAVAILABLE.
- Dependency: WORK_NOT_REGISTERED, WORK_TERMINAL, SOURCE_FENCED, LINEAGE_INCOMPLETE, SCOPE_MISMATCH, ARTIFACT_ID_CONFLICT, DEPENDENCY_NOT_DURABLE.
- Publication: REGISTRATION_NOT_DURABLE, WORK_NOT_ACTIVE, ATTEMPT_STALE, LEASE_STALE, FENCE_ADVANCED_OR_COVERS_ANCESTOR, FENCE_UNKNOWN, PERMISSION_EPOCH_STALE_OR_REVOKED, DEPENDENCY_NOT_DURABLE, STORAGE_ATOMICITY_UNAVAILABLE.
- Completion/recovery: OUTPUT_UNRECONCILED, PUBLICATION_UNKNOWN, LEASE_STILL_VALID, REPLAY_STILL_POSSIBLE, TERMINAL_CONFLICT, EVIDENCE_INCOMPLETE, DIGEST_MISMATCH, RECEIPT_NOT_RETAINED, LEDGER_UNAVAILABLE, DEPENDENCY_INVENTORY_GAP, RECONCILIATION_UNAVAILABLE.

The above error names are D's semantic vocabulary; exact transport/wire encoding and API exposure remain OPEN. E may map them internally only while preserving the original typed reason and retryability.

### Additional exact linearization rules

- RegisterProducerClass linearizes at durable registry-version/status commit; work admission must observe an enabled committed version.
- RegisterProducerWork linearizes at durable work-ledger insertion in the same ordering domain as InstallForgetFence; ProducerRegistrationSequence is assigned only there.
- InstallForgetFence linearizes at one durable canonical transaction that makes the fence effective and captures registry version + work high-water.
- CaptureProducerRegistrationHighWater is a consistent snapshot read tied to the install transaction/version; it verifies but never changes the immutable cutoff.
- RegisterDerivedDependency linearizes at durable commit of the artifact record and all required dependency edges; partial edge persistence is not success.
- PublishDerivedIfFenceCurrent linearizes at the single durable visibility commit, with current fence, dependency/registration state and I authorization validated at that point.
- CompleteProducerWork linearizes at durable D terminal-disposition commit after evidence validation.
- ResolveProducerWork is a consistent read and must return UNKNOWN if authoritative current state cannot be established.
- ReconcileForgetBarrier is a consistent, versioned snapshot across barrier ledger, dependency inventory and target inventory; a DRAINED result applies only to those checkpoints.

### Typed sequence namespace correction

ProducerRegistrationSequence / ProducerRegistrationHighWater and ProducerRegistryVersion are D-owned, distinct from CanonicalCommitCursor. They must be stored as typed values and never substituted for or numerically compared with CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, ForgetFenceGeneration, PermissionEpoch, IndexWatermark or ContextVersion.



---
## Phase 3.5 Addendum — OPEN Item Precision Correction

This section supersedes the earlier OPEN-E/D-01 through OPEN-E/D-05 wording in §5 where it could be read as claiming that D has not specified operation-level inputs, outputs, idempotency, error outcomes or linearization. D's normative operation contract now specifies those semantic elements for all nine operations. The remaining gaps are narrower:

| OPEN ID | Exact unresolved item | Owner / why still open |
|---|---|---|
| OPEN-API-01 | Callable API/transport schemas, serialization, authentication binding, compatibility/version negotiation and error-to-wire mapping for D semantic operations | D + H + B/I; D explicitly states semantic operation contracts do not assert public APIs or wire schemas |
| OPEN-STORAGE-01 | Named accountable Storage/Consistency owner; chosen transaction/CAS/serializable protocol; durable hidden prepare/commit; replica/read consistency; crash/restore behavior; proof that fence installation serializes with visibility commit | Storage/Consistency owner unassigned in D review; semantic contract is not implementation evidence |
| OPEN-I-AUTH-01 | I authoritative PermissionEpoch freshness/equality/decision lookup at final gate, decision validity and revocation propagation | I-owned; E cannot define policy semantics |
| OPEN-REGISTRY-GLOBAL-01 | Reconcile D-local ProducerRegistryVersion/ProducerRegistrationHighWater with I's global producer/recipient inventory and A/module ownership registry; prove closed-world completeness | I/A + module owners; local D ledger alone does not prove global inventory completeness |
| OPEN-RECOMPILE-01 | Exact linked child/re-admission identity rule for recompile and whether a distinct ProducerWorkItemId is required | D/E; D requires explicit linked child/re-admission decision but does not freeze E's run model |
| OPEN-TEST-01 | Executable race/fault fixtures, storage fault injection, actual expected/observed outputs and owner sign-off | D/E/Storage + affected consumers; all matrices here remain design-only |

The earlier phrases “exact fields”, “exact receipt/error schema”, “high-water type” and “serialization with InstallForgetFence” are no longer valid as statements that D's semantic contract is unspecified. D has specified the semantic fields and one-order race. What remains open is their callable transport/API realization, global inventory reconciliation and tested storage linearization. Do not invent D decisions to fill those implementation gaps.
