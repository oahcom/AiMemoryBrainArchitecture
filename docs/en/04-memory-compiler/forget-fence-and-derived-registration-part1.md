# E Forget Fence and Derived Registration — Part 1: Core Contract

- Document ID: E-FORGET-DERIVED-001-P1
- Source revision: DEREFERENCED — historical source blob `00e37ba56596e710513c8d0568acd79141d9101b` retained; no current normative source path exists.
- Source: DEREFERENCED — original normative path `04-memory-compiler/forget-fence-and-derived-registration-part1.md` is absent from the current main tree; alternative: [surviving Chinese counterpart](../../zh-CN/04-memory-compiler/forget-fence-and-derived-registration-part1.md) (blob `0d96f4e0c82763c74ab61f67e4a2869280632395`; translation only, not an authoritative substitute).
- Chinese counterpart: [第 1 部分 — 核心契约](../../zh-CN/04-memory-compiler/forget-fence-and-derived-registration-part1.md)

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
