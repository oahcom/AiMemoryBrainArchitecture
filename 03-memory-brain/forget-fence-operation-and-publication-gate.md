# Forget Fence Atomicity, Producer Admission and Publication Gate

**Owner:** Session D — Memory Brain Principal Architect  
**Status:** D operation semantics DECIDED; D/E interface schema, Storage/Consistency realization and cross-owner conformance OPEN.  
**Addresses:** CR-P1-01, D-REV-P1-003.

D owns canonical ForgetOperation, ForgetFence, producer-registration/barrier ledger, dependency inventory semantics and canonical publication eligibility. E owns compiler work/attempt/lease/retry/DLQ/replay state and invokes these contracts. I owns authenticated identity, authorization and PermissionEpoch. Storage/Consistency owns physical atomicity/serialization only when explicitly assigned and validated. H owns wire/Adapter ACK; F owns index behavior; G owns Context behavior.

> This document specifies operation-level semantics and observable evidence. It does not assert that callable D APIs, a database transaction, lock, CAS, distributed coordinator or production implementation already exists.

## 1. Normative invariants

1. No derivative-capable producer may enqueue, lease, dereference protected source payload, execute, retry, DLQ-replay or publish until a durable ProducerWork registration receipt exists.
2. A producer class must be registered and enabled under a versioned registry before work admission. Unknown, disabled, unregistered or registry-incomplete classes fail closed.
3. ProducerWork registration and Fence installation participate in one linearizable ordering domain for the affected Brain authority and source lineage.
4. A registration concurrent with fence installation is either committed before the fence snapshot and included in its barrier, or ordered after the fence and rejected/quarantined. There is no admitted-but-unaccounted work that can publish.
5. Complete dependency registration is durable before any artifact can be visible. Partial or uncertain registration leaves the artifact private.
6. The latest applicable ForgetFence is checked at the same atomic/linearizable boundary that changes the artifact from private to visible. A prior read or single-use token consumed later without a shared fence is insufficient.
7. PermissionEpoch is independently revalidated at the final gate. ForgetFenceGeneration and PermissionEpoch are different types and namespaces; numeric ordering, comparison or conversion between them is forbidden.
8. Retries and lease replacement preserve ProducerWorkItemId and lineage; AttemptId and LeaseId identify executions, not new admission authority. Recompile uses a new DerivationRunId and an explicit linked child/re-admission decision, never an unlinked work identity.
9. Timeout, lost ACK, expired lease, missing receipt, registry gap, DLQ state, or unavailable latest fence/permission is unresolved and blocks publication/barrier closure.
10. DLQ replay, restore, rebuild, backfill and re-index must reuse or explicitly link the original source lineage and re-run current fence and permission checks before visibility.

## 2. Typed identity and evidence vocabulary

| Type | Owner / scope | Semantics |
|---|---|---|
| ProducerClass | D registry; stable class identity + contract version | Registered category of derivative-capable producer |
| ProducerRegistryVersion | D | Immutable version of producer-class registry and enabled/disabled status |
| ProducerWorkItemId | D ledger | One logical derivative-capable work item across retries/lease changes |
| RegistrationReceipt | D | Durable admission result bound to work ID, request digest, class, source lineage/scope, registry version and registration sequence |
| ProducerRegistrationSequence / HighWater | D ledger | Monotonic position in producer-work ledger; not a canonical cursor, fence generation or permission epoch |
| ForgetFenceGeneration | D Forget authority | Monotonic generation in the ForgetFence namespace |
| ForgetFenceCursor | D | Typed tuple (ForgetOperationId, ForgetFenceGeneration, TargetSetDigest); installation CanonicalCommitCursor is separate audit evidence |
| PermissionEpoch | I | Opaque authorization/revocation epoch in I policy namespace |
| DerivedArtifactRef/version | E artifact identity; registered in D inventory | Immutable staged derivative identity/version |
| DependencyRegistrationId / Receipt | D inventory | Stable idempotency identity and durable artifact/source-lineage evidence |
| PublicationOperationId / Receipt | D gate semantics | Stable idempotency identity and final visibility outcome |
| CanonicalCommitCursor | D; one Brain authority | Commit ordering/audit cursor; not a fence or registration sequence |
| AttemptId / LeaseId / DerivationRunId | E | Attempt, lease and derivation execution identities; never replace WorkItemId |

No arithmetic, numeric comparison, casting or substitution is permitted between ProducerRegistrationSequence, CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, ForgetFenceGeneration, PermissionEpoch, IndexWatermark or ContextVersion. D evaluates typed fence coverage/freshness for exact target lineage. I evaluates current permission validity.

## 3. Operation contracts

The names below are normative semantic operations, not assertions that public API names or wire schemas exist. Every operation returns a durable receipt or typed non-success result. Request digests are computed over canonicalized typed fields.

### 3.1 RegisterProducerClass

- **Input:** authenticated producer-owner binding; ProducerClassId; owner/module; contract/schema version; permitted source-reference classes; declared derivative/output classes; Scope/security-domain constraints; capabilities (production, replay, rebuild, cleanup-only); idempotency key and canonical request digest.
- **Output:** ProducerClassRegistrationReceipt; ProducerRegistryVersion; status ENABLED, DISABLED or QUARANTINED; effective registry sequence.
- **Idempotency:** same owner + class ID + version + digest returns original receipt. Same identity with different digest returns IDEMPOTENCY_CONFLICT. Rebinding a class to a different owner/capability set requires explicit new version and supersession.
- **Errors:** UNKNOWN_OWNER, AUTHENTICATION_REQUIRED, CLASS_CONFLICT, UNSUPPORTED_SCHEMA, REGISTRY_INCOMPLETE, POLICY_DENIED.
- **Linearization point:** durable commit of registry version/status in authoritative D registry. Work admission must observe a committed enabled version.
- **Rules:** unknown class is never implicitly admitted. Disabling a class blocks new work but does not erase existing registrations; existing work remains in barrier until terminal. If registry completeness is unknown, Forget proof remains open.

### 3.2 RegisterProducerWork

- **Input:** ProducerWorkItemId; ProducerClassId + registry version; authenticated ProducerIdentity binding reference (validated by H/I, not payload claim); source EventRef and/or canonical TypedObjectRefs with exact revisions; source/transitive lineage digest or approved opaque token; ScopeRefs; ForgetOperation/correlation/causation refs; admission CanonicalCommitCursor or D-defined genesis; observed ForgetFenceCursor; current PermissionEpoch/authorization-decision reference; schema version; canonical request digest; optional initial AttemptId/LeaseId.
- **Output:** RegistrationReceipt binding identity fields, ProducerRegistrationSequence, ProducerRegistryVersion, admission fence observation, disposition ACCEPTED, REJECTED, QUARANTINED or CLEANUP_ONLY, and durable lookup key.
- **Idempotency:** same WorkItemId + same canonical digest returns same receipt/sequence. Same ID + different digest returns IDEMPOTENCY_CONFLICT and cannot mutate original registration. Retry does not create a second logical registration.
- **Errors:** UNKNOWN_PRODUCER_CLASS, CLASS_DISABLED, FENCE_CLOSED, FENCE_UNKNOWN, PERMISSION_STALE_OR_DENIED, SCOPE_INVALID, SOURCE_LINEAGE_INVALID, REGISTRY_INCOMPLETE, IDEMPOTENCY_CONFLICT.
- **Linearization point:** durable insertion/acceptance of work ledger row in the same serialization domain used by InstallForgetFence. Sequence is assigned only at this point.
- **Admission rule:** if an active fence covers any source ancestor, ordinary derivative work is rejected or quarantined. A caller-supplied current generation does not make a forgotten ancestor eligible. Only suppression/cleanup work may be admitted post-fence, and it cannot publish ordinary derivatives.
- **EventRef-only ingress:** registration may precede canonical MemoryRef creation. D records EventRef/opaque lineage token, producer, scope and security binding. When canonical refs become available, E must append/link exact refs/revisions before dependency registration/publication. Missing MemoryRef does not permit omitted lineage.

### 3.3 InstallForgetFence

- **Input:** durable ForgetOperationId; I authorization-decision reference; exact target TypedObjectRefs/version families; ScopeRefs; target-set digest; idempotency key + request digest; expected fence state where applicable.
- **Output:** durable ForgetFenceCursor; installation CanonicalCommitCursor; captured ProducerRegistryVersion; captured ProducerRegistrationHighWater; target inventory snapshot/watermark; fence receipt and recoverable outbox intent.
- **Idempotency:** same operation + same target/request digest returns same receipt/generation. Same operation ID with changed target digest returns IDEMPOTENCY_CONFLICT. Re-delivery does not allocate a new generation.
- **Errors:** AUTHORIZATION_REQUIRED, TARGET_SET_INVALID, IDEMPOTENCY_CONFLICT, FENCE_STATE_CONFLICT, REGISTRY_INCOMPLETE, SERIALIZATION_RETRY_EXHAUSTED.
- **Linearization point:** one durable canonical transaction/serializable commit that makes the fence effective and captures producer-registration high-water under the same admission/fence serialization order. The installation CanonicalCommitCursor is audit order, not fence generation.
- **Atomic effects:** suppress target lineage for ordinary reads/publication; allocate next D FenceGeneration; persist target digest and exact refs; capture ProducerRegistrationHighWater and ProducerRegistryVersion; persist inventory snapshot/watermark and outbox intent.
- **Rule:** if registry completeness cannot be shown, known targets may be suppressed but barrier status is BLOCKED_REGISTRY_INCOMPLETE; no canonical suppression completion claim is allowed.

### 3.4 CaptureProducerRegistrationHighWater

- **Input:** ForgetOperationId + ForgetFenceCursor; expected registry version; optional reconciliation checkpoint.
- **Output:** immutable BarrierSnapshotReceipt with captured high-water, registry version, target digest, fence generation and ledger consistency proof/reference.
- **Idempotency:** same fence + snapshot key returns same receipt. Repeated capture cannot advance the barrier for that fence. Later reconciliation checkpoints are explicitly versioned and cannot erase unresolved entries.
- **Errors:** FENCE_NOT_INSTALLED, FENCE_MISMATCH, REGISTRY_INCOMPLETE, LEDGER_GAP, SNAPSHOT_UNAVAILABLE.
- **Linearization point:** consistent snapshot read tied to fence installation transaction/version. If correspondence to installation serialization point cannot be proven, return unavailable, not an approximate high-water.
- **Rule:** this is not a second admission cutoff. InstallForgetFence establishes the immutable cutoff; capture retrieves/verifies it.

### 3.5 RegisterDerivedDependency

- **Input:** DependencyRegistrationId; DerivedArtifactRef/version; ProducerWorkItemId; DerivationRunId; AttemptId/LeaseId; ProducerClass; exact source refs/revisions and EventRefs; direct parent artifact refs + dependency receipt refs; complete lineage digest; ProvenanceRef; ScopeRefs; observed ForgetFenceCursor; current PermissionEpoch/authorization reference; schema version and canonical digest.
- **Output:** DependencyRegistrationReceipt with inventory position, artifact/version, work/run/attempt, source/parent refs and digests, scope, fence observation, permission evidence reference and status REGISTERED, REJECTED or QUARANTINED.
- **Idempotency:** same DependencyRegistrationId + same digest returns original receipt. Same ID + different digest returns IDEMPOTENCY_CONFLICT. Same immutable artifact/version and lineage returns same receipt; changed lineage requires a new immutable artifact version and registration identity.
- **Errors:** WORK_NOT_REGISTERED, WORK_TERMINAL, SOURCE_FENCED, FENCE_UNKNOWN, PERMISSION_STALE_OR_DENIED, LINEAGE_INCOMPLETE, SCOPE_MISMATCH, ARTIFACT_ID_CONFLICT, IDEMPOTENCY_CONFLICT.
- **Linearization point:** durable commit of artifact dependency record and all required edges in D inventory. If inventory spans stores, a proven durable prepare/commit protocol is required; partial edge set is not successful registration.
- **Visibility rule:** receipt is necessary but not sufficient for visibility. Artifact remains private until PublishDerivedIfFenceCurrent commits visibility.

### 3.6 PublishDerivedIfFenceCurrent

- **Input:** PublicationOperationId; DerivedArtifactRef/version; ProducerWorkItemId; DerivationRunId; AttemptId/LeaseId; ProducerClass; all DependencyRegistrationReceipt IDs and lineage digest; ScopeRefs; observed ForgetFenceCursor; current I PermissionEpoch + authorization-decision reference; RegistrationReceipt; request digest; private staging object/version reference.
- **Output:** durable PublicationReceipt binding WorkItem/Attempt, class, source MemoryVersion/Revision refs, ScopeRefs, RegistrationReceipt, observed and authoritative fence decision, PermissionEpoch decision reference, artifact identity, complete dependency evidence, visibility commit ID/cursor and disposition PUBLISHED, REJECTED_FENCED, REJECTED_PERMISSION, REJECTED_INCOMPLETE or QUARANTINED.
- **Idempotency:** same PublicationOperationId + same digest returns original receipt/outcome. Same key + changed digest returns IDEMPOTENCY_CONFLICT. Lost ACK is resolved by lookup of same operation ID; never issue a new key for uncertain commit.
- **Errors:** DEPENDENCY_NOT_DURABLE, REGISTRATION_NOT_DURABLE, WORK_NOT_ACTIVE, ATTEMPT_STALE, LEASE_STALE, FENCE_ADVANCED_OR_COVERS_ANCESTOR, FENCE_UNKNOWN, PERMISSION_EPOCH_STALE_OR_REVOKED, SCOPE_MISMATCH, ARTIFACT_ALREADY_PUBLISHED, IDEMPOTENCY_CONFLICT, STORAGE_ATOMICITY_UNAVAILABLE.
- **Linearization point:** single durable visibility commit at which current D fence and dependency/registration state are validated, I authorization is current/valid, and artifact becomes visible. Fence installation and this commit must serialize in the same consistency domain. If Publish wins, artifact is visible before fence and must be in dependency/barrier inventory. If Fence wins, publication is rejected. No successful gate receipt may precede an independent visibility write.
- **Storage requirement:** preferred semantics are one atomic transaction/CAS spanning gate validation and visibility marker. If stores are separate, Storage/Consistency must specify and prove equivalent protocol: durable hidden prepare; fence/permission validation bound to prepare; commit token/record atomically consumed with visibility CAS; recovery keeps ambiguous artifacts hidden; fence installation serializes against same commit decision. A token replayable after fence advancement, or uncoordinated check-then-write, is invalid.
- **Permission rule:** PermissionEpoch is checked for current validity/equality under I's authoritative semantics, never numerically compared with FenceGeneration. If I cannot provide a current decision at visibility boundary, fail closed.
- **Lineage rule:** check every source ancestor and target scope, not merely immediate parent/artifact ID. New artifact ID or recompile cannot reset lineage eligibility.

### 3.7 CompleteProducerWork

- **Input:** ProducerWorkItemId; final AttemptId/LeaseId; disposition; all output artifact refs and dependency/publication receipts; canonical commit refs where applicable; terminal reason/error class; proof no further attempt can publish; producer owner binding; request digest.
- **Output:** ProducerWorkTerminalReceipt; barrier ledger state; unresolved-output count; reconciliation cursor.
- **Idempotency:** same work ID + same terminal digest returns same receipt. Conflicting terminal digest returns TERMINAL_CONFLICT; no silent overwrite/downgrade.
- **Errors:** WORK_UNKNOWN, WORK_NOT_REGISTERED, OUTPUT_UNRECONCILED, PUBLICATION_UNKNOWN, LEASE_STILL_VALID, REPLAY_STILL_POSSIBLE, TERMINAL_CONFLICT, EVIDENCE_INCOMPLETE.
- **Linearization point:** durable terminal disposition commit in D barrier ledger after evidence validation. Lease expiry, queue deletion, worker shutdown and DLQ parking are not terminal evidence.
- **Rule:** terminal disposition is monotonic. A later-discovered derivative/publication invalidates current barrier proof and reopens reconciliation without rewriting history.

### 3.8 ResolveProducerWork

- **Input:** ProducerWorkItemId + original registration digest; optional AttemptId/LeaseId; DependencyRegistrationId and/or PublicationOperationId; caller correlation ID.
- **Output:** authoritative RegistrationReceipt, dependency receipts, PublicationReceipt, terminal receipt, current lease/attempt status and barrier membership.
- **Idempotency:** read-only and repeatable; lookup never creates work or advances a fence.
- **Errors:** WORK_UNKNOWN, DIGEST_MISMATCH, RECEIPT_NOT_RETAINED, AUTHORIZATION_REQUIRED, LEDGER_UNAVAILABLE.
- **Linearization point:** consistent read from authoritative ledger/receipt store at defined snapshot. If current state cannot be established, return UNKNOWN; caller remains fail-closed.
- **Rule:** recovery reuses original IDs/digests. Timeout alone implies neither success nor failure.

### 3.9 ReconcileForgetBarrier

- **Input:** ForgetOperationId + ForgetFenceCursor; BarrierSnapshotReceipt; registry version; dependency inventory snapshot/cursor; reconciliation checkpoint; target inventory/watermark; terminal and publication receipts.
- **Output:** BarrierReconciliationReceipt with exact high-water, included work count, terminal count, open/expired/DLQ/unknown count, dependency inventory watermark, late derivative count, unresolved registry gaps and disposition DRAINED, OPEN_WORK, OPEN_DEPENDENCY, REGISTRY_GAP, LATE_DERIVATIVE or UNKNOWN.
- **Idempotency:** same snapshot/checkpoint returns same deterministic receipt. New evidence creates append-only reconciliation receipt; prior receipts remain auditable.
- **Errors:** FENCE_UNKNOWN, SNAPSHOT_MISMATCH, LEDGER_GAP, DEPENDENCY_INVENTORY_GAP, REGISTRY_INCOMPLETE, RECONCILIATION_UNAVAILABLE.
- **Linearization point:** consistent read/snapshot over barrier ledger, dependency inventory and target inventory at explicit versioned checkpoints. DRAINED is valid only for those immutable checkpoints; later-discovered pre-fence work or late derivative invalidates current completion and forces reconciliation.
- **Rule:** only D asserts D-local canonical barrier result. I decides whether it suffices for global Forget; it is not physical-erasure evidence.

## 4. Registration/Fence/Publish state transitions

ProducerClass: UNREGISTERED -> ENABLED -> DISABLED or QUARANTINED. New admission requires ENABLED; existing work remains tracked.

ProducerWork: ABSENT -> REGISTERED -> QUEUED -> LEASED -> RUNNING -> STAGED -> DEPENDENCY_REGISTERED -> PUBLISH_PENDING -> PUBLISHED -> TERMINAL. Retry returns to QUEUED with same WorkItemId and new AttemptId. DLQ remains barrier-open. Lease expiry is an attempt condition, not terminal. Suppression/quarantine can terminate only after durable no-publication evidence. Recompile creates a new DerivationRunId explicitly linked to original lineage.

Forget: REQUESTED -> FENCE_INSTALLED + immutable BarrierSnapshot -> BARRIER_OPEN -> BARRIER_DRAINED -> TARGET_RECONCILIATION -> D_CANONICAL_SUPPRESSION_PROVEN. Registry gap, late derivative, unknown lease/publication or missing dependency blocks/reopens proof.

Publish: PRIVATE_STAGED -> DEPENDENCIES_DURABLE -> FINAL_GATE_PENDING -> (atomic fence + permission + visibility commit) -> VISIBLE. Any rejection remains private/quarantined. There is no intermediate "gate approved, artifact visible later" permission state.

## 5. Registration/Fence race: only two legal outcomes

Registration and fence installation MUST serialize on a shared D consistency boundary or formally proven equivalent.

| Serialization winner | Required result | Barrier membership | Publication eligibility |
|---|---|---|---|
| RegisterProducerWork commits first | Durable receipt with sequence s; fence captures high-water H >= s | Included in immutable pre-fence barrier | May continue only subject to final gate; if fence covers source, suppress before publication |
| InstallForgetFence commits first | Fence effective and captures H; later registration observes fence | Not admitted as ordinary derivative work; reject/quarantine or cleanup-only | No ordinary publication |
| Concurrent/ambiguous commit | Resolve by stable ID/digest; authoritative order selects one of above | Included iff registration commit precedes fence point | Unknown remains private and cannot publish |

There is no valid result in which accepted registration is absent from captured high-water. There is no valid result in which post-fence ordinary work for a covered source is accepted. If implementation cannot prove which operation linearized first, return/retain UNKNOWN and block execution/publication until reconciliation.

## 6. Derivative visibility atomic boundary

Artifact consumer-visible state and final fence/permission decision must have one externally observable linearization point. D owns the semantic rule; Storage/Consistency must nominate and validate the realization.

1. Staged artifact is private by default; no consumer-facing index, outbox, cache, canonical read or Context input can enumerate it.
2. D dependency registration durably commits artifact identity and every direct/transitive source edge before publication.
3. Final gate validates RegistrationReceipt, all DependencyRegistrationReceipts, work/attempt/lease liveness, exact ScopeRefs, every source ancestor's current fence status, and I current PermissionEpoch/authorization decision.
4. Same atomic/linearizable commit records successful PublicationReceipt and flips authoritative visibility marker. If commit aborts, neither success receipt nor visible state exists.
5. Cross-store prepare/commit is permitted only if prepare remains hidden; commit is one-time CAS/transaction bound to exact fence and permission decision; fence installation serializes with commit; recovery never exposes prepared/unknown artifact without committed proof.
6. After crash, replay, rebuild or restore, visibility is reconstructed only from committed publication records and revalidated against latest fence before exposure. Replayed dependency record alone cannot make artifact visible.

Lost ACK is resolved with ResolveProducerWork using same stable operation ID/digest. If committed, return original receipt; otherwise retry same idempotency key. Never create a new artifact identity or publication key to bypass uncertainty.

## 7. Publish Gate Evidence — minimum immutable binding

Every PublicationReceipt binds:
- WorkItemId and AttemptId; LeaseId when used;
- ProducerClassId and ProducerRegistryVersion;
- DerivationRunId;
- source MemoryVersionRef(s), exact SourceRevision(s), complete transitive lineage digest;
- ScopeRef set and scope/tenant/security-domain binding;
- Producer RegistrationReceipt ID + request digest + ProducerRegistrationSequence;
- observed ForgetFenceCursor and authoritative fence decision at commit (typed separately);
- I PermissionEpoch + authorization-decision reference/result;
- DerivedArtifactRef/version and private staging object/version identity;
- every DependencyRegistrationReceipt ID, inventory position and lineage digest;
- PublicationOperationId, request digest, visibility commit ID/CanonicalCommitCursor where applicable, final disposition.

Do not place FenceGeneration and PermissionEpoch in a shared integer field or compare them numerically. Do not omit AttemptId when delayed workers may return after lease replacement. Receipt is immutable and non-reconstructive: identifiers, digests and outcomes only, no forgotten plaintext.

## 8. E / Storage / I interface mapping

| Boundary | D provides / decides | E consumes / emits | Other owner / OPEN |
|---|---|---|---|
| Producer class | Registry identity/version/status/receipt and closed-world completeness | Register compiler/replay/rebuild classes before accepting work | I/A reconcile registry inventory across producer domains; owner mapping OPEN |
| Work admission | RegistrationReceipt, high-water sequence, disposition and barrier membership | Stable WorkItemId across retries; no queue/lease/run before receipt; ACK-loss lookup | H/I authenticated ProducerIdentity and Scope/Permission validation OPEN |
| Fence install | ForgetFenceCursor, install commit cursor, captured registry version + work high-water + target snapshot | Stop/park covered work and propagate typed fence | Storage/Consistency proves registration/fence serialization |
| Dependency inventory | Durable dependency receipt and inventory position | Register all direct/transitive lineage before visibility; staged output private | E owns lineage production; B typed-ref vocabulary may remain ADR-blocked |
| Publish gate | Final authoritative fence/registration decision and PublicationReceipt semantics | Submit evidence; expose only after successful committed receipt | Storage/Consistency atomically couples gate/visibility; I supplies current permission decision |
| Terminal work | Validated terminal receipt and barrier update | Preserve DLQ/retry/lease identity; submit terminal only when no publish path remains | E owns terminal truth; D validates barrier evidence |
| Reconciliation | D barrier receipt with exact high-water and unresolved counts | Supply registration/dependency/publication/terminal evidence | I consumes D result but decides global completion |
| Global Forget | D-local canonical suppression proof only | No global completion assertion | I owns policy, exceptions, backup/external-copy and physical erasure |

### 8.1 Storage/Consistency acceptance requirements — owner OPEN

A Storage/Consistency owner must be explicitly assigned before implementation approval. That owner must select and validate one of:
- a single ACID transaction covering fence state, registration ledger/dependency records and artifact visibility marker;
- serializable transactions or conditional writes/CAS sharing a linearizable fence version and publication decision;
- durable transactional outbox plus hidden prepare/commit protocol whose recovery preserves no-visible-before-commit;
- another formally specified equivalent with explicit serialization point and crash-recovery proof.

Evidence required: isolation/consistency model; transaction participants; linearization point; idempotency/uniqueness constraints; failure injection before/after each durable write; crash recovery; concurrent register/fence/publish tests; replica/read consistency; backup/restore fence reapplication; proof stale tokens cannot publish after newer fence. D does not select or certify a specific database, lock manager or distributed transaction product.

**OPEN: no formally named Storage/Consistency Owner or implementation evidence was found in the reviewed contract set.**

## 9. Fault/Race Conformance Matrix — design expectations, NOT RUN

| # | Initial state | Interleaving / fault | Required result | Forbidden result |
|---:|---|---|---|---|
| 1 | Class enabled; Work absent; Fence absent | RegisterProducerWork races InstallForgetFence | Shared serialization yields accepted + sequence <= captured H, or rejected/quarantined after fence | Accepted work omitted from H yet allowed to run/publish |
| 2 | Fence installed; registration committed but response lost | E retries same WorkItemId/digest or resolves | Same receipt/sequence returned; if fence won, authoritative rejection | New work ID, duplicate ledger row, assumed acceptance |
| 3 | Work registered; artifact staged privately; dependency receipt durable | Crash before Publish | Artifact stays private; recovery resolves same IDs and rechecks fence/permission | Staged artifact visible on restart/replay |
| 4 | Publish committed; response lost | E retries same PublicationOperationId | Same PublicationReceipt returned; visibility matches committed receipt | Duplicate publication or visible artifact without receipt |
| 5 | Work leased under Attempt A / Lease L1 | Lease expires; Worker B retries with Attempt B / Lease L2 | Same WorkItemId/lineage; old attempt fenced; new attempt refreshes permission/fence | Expiry closes barrier or old attempt publishes |
| 6 | Work in DLQ; registration open | Operator/system replays item | Same WorkItemId/lineage, new AttemptId; reauthorize/recheck fence; barrier stays open | New untracked admission or DLQ treated terminal |
| 7 | Dependency inventory contains artifact lineage | Index/backfill/rebuild replays old staged/visible data | Rebuild uses committed publication state and current fence; covered artifact suppressed before index visibility | Replay makes artifact visible without fresh fence check |
| 8 | Artifact staged and dependency registered at fence G | Fence advances to G+1 before final Publish | Final gate sees latest fence and rejects/quarantines; no visibility commit | Staging-time G authorizes publication |
| 9 | PermissionEpoch P observed at admission | I revokes/advances policy before final Publish | I decision at final gate denies/stales; artifact remains private | Numeric comparison with FenceGeneration or admission epoch treated as permanent |
| 10 | ProducerClass absent/disabled/unknown | Producer attempts registration/submit | Reject/quarantine; audit; barrier cannot be certified closed if inventory incomplete | Auto-register on first work or allow side-channel publish |

Additional mandatory variants: partial dependency receipts; same key/different digest; fence lookup unavailable; terminal ACK lost; late derivative after prior proof; overlapping Forget fences; restore from backup; publication CAS conflict; permission lookup timeout. All remain fail-closed and require deterministic reconciliation.

## 10. Decision status and unresolved owners

| Item | Decision | Owner / next action |
|---|---|---|
| Operation semantics and idempotency | DECIDED — D semantic contract | D maintains normative operation meanings |
| Register/Fence total order and two-outcome race | DECIDED — D semantic contract | Storage/Consistency implements/proves shared serialization |
| Dependency-before-visible rule | DECIDED — D semantic contract | E produces lineage; Storage/Consistency proves visibility boundary |
| Publish gate evidence | DECIDED — D semantic contract | I supplies permission decision; E supplies work/attempt evidence |
| PermissionEpoch/revocation policy | OPEN / I-owned | I defines current decision semantics and lookup |
| Authenticated ProducerIdentity / ActorRef / ScopeRef | OPEN / I-H-B-owned | I/H/B align identity and typed refs; D consumes verified refs |
| Producer class global completeness | OPEN / I + A + module owners | Reconcile D local registry with I global producer/recipient inventory |
| Storage transaction/CAS/lock/consistency | OPEN — OWNER UNASSIGNED | Architecture/Engineering names accountable owner; no D self-approval |
| E operation/API mapping and terminal evidence | OPEN / E + D | E maps compiler states to semantics; D defines receipt semantics |
| H/F/G producer/consumer enforcement | OPEN / H/F/G | Each owner supplies its own conformance; D does not edit their files |
| Global Forget, exceptions, backup/external copies, physical erasure | OPEN / I-owned | I decides policy and global proof |
| Runtime/fault-injection tests | NOT RUN | Storage + E + D + relevant consumers attach evidence |

## 11. D-local acceptance and non-claims

D-local documentation acceptance requires unambiguous operation contracts and two-outcome registration/fence order, minimum PublishReceipt evidence, and deterministic expected outcomes for all ten fault/race scenarios. This document meets the documentation/design specification criterion only.

It does not establish D APIs exist, E consumes a final approved schema, Storage atomicity is implemented, any fault test passed, H/F/G conform, I approved global policy, or Forget is end-to-end/physically complete. D-REV-P1-003 remains integration-open until owner implementation and conformance evidence are reviewed.
