---
document_metadata:
  domain: memory-brain
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope: {type: Full-document}
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-150/restore-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Source blob identity and body preservation are verified; exact-version Owner acceptance and normative approval remain unrecorded."
    usage_status: Active
    modification_status: Modified
    supersession: {supersedes: [], supersession_reason: null, effective_date: null}
    archival: {archived_date: null, archival_reason: null, archival_reference: null}
  authority:
    canonical_status: Canonical
    canonical_scope: "D ForgetOperation, ForgetFence, producer barrier and canonical publication eligibility"
    canonical_scope_id: "memory-brain/forget-fence-operation-publication-gate"
    canonical_scope_keywords: ["forget-operation", "forget-fence", "producer-barrier", "publication-gate"]
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
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




---

# Phase 3.6 — Forget Fence Linearization & Atomicity Semantics

**Owner:** Session D — Memory Brain Principal Architect  
**Status:** D-owned domain semantics DECIDED; E/Storage enforcement, I authorization freshness and cross-module conformance OPEN.  
**Authority:** This addendum is normative for D's Canonical Forget semantics. It does not select a database, claim a deployed transaction protocol, or assert implementation/test success.

## 1. Forget Atomicity Invariants

### 1.1 Unique safety invariant

For every derivative-capable Producer Work item W and every artifact A derived directly or transitively from W:

> **A must never enter any retrievable, deliverable, indexable, inferable, externally enumerable or otherwise consumer-visible state unless W is durably registered, W is accounted for by every applicable installed Forget barrier, the complete dependency lineage is durably registered, and the final visibility decision validates the current applicable ForgetFence and current I authorization/PermissionEpoch for the exact Principal, Scope and artifact.**

Equivalent fail-closed form:

> Any Producer Work that is not captured by an applicable Forget Barrier, or that has not passed the current Fence and Authorization checks at the final visibility boundary, MUST NOT cause a derivative to become visible.

No queue, lease, worker-local state, staged object, accepted event, dependency receipt, gate response, cached authorization result, outbox message, replay token or historical publication receipt independently grants visibility.

### 1.2 Distinct durable stages

| Stage | Meaning | Required durable evidence | Does not mean |
|---|---|---|---|
| Work Registration | D admits one stable logical ProducerWorkItemId with source/lineage/scope binding | RegistrationReceipt, request digest, ProducerRegistryVersion, ProducerRegistrationSequence, disposition | Work has been captured by a later fence |
| Barrier Capture | InstallForgetFence snapshots all accepted work ordered before its linearization point | ForgetFenceCursor, immutable BarrierSnapshotReceipt, ProducerRegistrationHighWater, registry version and target digest | Captured work is allowed to publish |
| Dependency Registration | Complete artifact identity and required direct/transitive source edges are committed to D's dependency inventory | DependencyRegistrationReceipt(s), complete-set/lineage digest and inventory position | Artifact is visible |
| Staging | E or another producer writes immutable candidate bytes/metadata into a private namespace | ArtifactRef/version, payload digest, private-stage identity and WorkItemId | Artifact is registered or visible |
| Publish Authorization | Final gate verifies work, attempt/lease, dependencies, current fence, current PermissionEpoch and Principal/Scope authorization | Immutable gate decision bound to exact IDs, digests and current authority decisions | Visibility has committed |
| Durable Commit | One externally observable commit makes the publication decision and authoritative visibility state durable together, or a proven equivalent protocol completes | PublicationReceipt, commit identity/cursor, authoritative visibility marker and recovery evidence | All consumers have refreshed their caches |
| Artifact Visibility | Consumers can discover/read/deliver the artifact through the authoritative visibility predicate | Committed PUBLISHED receipt and current fence/authorization enforcement at protected reads | Physical erasure or global Forget completion |
| Terminal Disposition | D closes the logical work item only after every output and every future publication path is accounted for | ProducerWorkTerminalReceipt, final attempt/lease epoch, output/dependency/publication inventory and no-future-publication evidence | Queue deletion, lease expiry, DLQ parking or worker exit |

Stage ordering is normative, but not every work item must reach every stage. Rejected, suppressed or cleanup-only work may terminate without staging or publication. A stage receipt is not a substitute for a later stage's receipt.

### 1.3 Barrier and visibility rules

1. Registration is durable before enqueue, lease acquisition, protected payload dereference, execution, retry, DLQ replay or publication.
2. Registration and fence installation share one linearizable ordering domain per affected Canonical Memory authority and applicable lineage.
3. Every accepted registration ordered before fence installation is included in the immutable captured high-water. A registration ordered after the fence is rejected/quarantined or explicitly admitted as cleanup-only with no ordinary publication capability.
4. Barrier capture makes pre-fence work accountable; it does not grant permission to publish.
5. Complete dependency registration precedes visibility. Incomplete, partial or unknown dependency registration leaves the artifact private.
6. Final publication validates every source ancestor, target, ScopeRef, current fence and current I authorization at the visibility linearization point.
7. Any uncertain commit, missing receipt, unavailable authority, stale lease, stale PermissionEpoch, unknown fence, incomplete lineage or unresolved idempotency outcome is non-visible and unresolved.
8. Lease expiry, DLQ state, retry delay, process disappearance and queue deletion never close the logical work item.
9. A late derivative or newly discovered lineage edge invalidates the current barrier proof and requires suppression plus reconciliation; history is not silently rewritten.
10. No consumer may bypass the authoritative visibility predicate by reading staging storage, object paths, caches, indexes, outbox payloads, delivery queues or stale snapshots directly.

## 2. Operation Linearization Table

A linearization point is the single durable event that determines the externally observable order. The evidence below is a required contract, not a claim that the current system already emits it.

| Operation / race | Linearization point | Only legal outcomes | Minimum durable evidence |
|---|---|---|---|
| RegisterProducerWork vs InstallForgetFence | Commit of either operation under the same authority/lineage serialization domain | Registration first: accepted sequence s is included with s <= captured H. Fence first: ordinary work is rejected/quarantined or cleanup-only. No accepted-but-uncaptured work | RegistrationReceipt + sequence + digest; ForgetFence receipt + generation + immutable H + install cursor; shared ordering/commit evidence |
| RegisterDerivedDependency vs InstallForgetFence | Commit of complete dependency set under the same applicable fence serialization domain | Dependency first: complete artifact/edges are durable and included in fence reconciliation; fence first: covered lineage registration is rejected/quarantined and artifact remains private | DependencyRegistrationReceipt + complete lineage digest + inventory position; fence receipt/H; commit order |
| PublishDerivedIfFenceCurrent vs InstallForgetFence | Atomic/linearizable visibility commit ordered against fence installation | Publish first: artifact was visible before fence and is in dependency/barrier inventory for suppression/reconciliation. Fence first: publish rejects/quarantines. No third state | PublicationReceipt + visibility commit identity; authoritative fence receipt/generation; dependency receipts; serialized commit trace |
| PublishDerivedIfFenceCurrent vs Permission Revocation | Final visibility commit must consume/validate an I-authoritative current authorization decision under I-defined revocation freshness semantics | Revocation first: reject. Publication first: publication was authorized at its commit point; subsequent revocation applies prospectively under I policy. If currentness/order cannot be established, remain private | I decision reference + PermissionEpoch + Principal/Scope binding + decision freshness proof; publication commit record. Exact cross-service ordering remains I/Storage OPEN |
| CompleteProducerWork vs Crash Recovery | Commit of immutable terminal disposition in D barrier ledger | Terminal commit first: recovery returns same terminal receipt. Crash before terminal commit: work remains open and recovery reconciles same WorkItemId. Never infer terminal from disappearance | ProducerWorkTerminalReceipt + final AttemptId/LeaseEpoch + output accounting digest + terminal commit cursor |
| ResolveProducerWork after uncertain outcome | Consistent authoritative read of the original stable ID/digest | Return original receipt/state or UNKNOWN; lookup never creates a second operation | Lookup key, original digest, authoritative ledger snapshot/version and returned receipt |
| ReconcileForgetBarrier | Consistent read over immutable barrier/dependency/target checkpoints | DRAINED only for exact named checkpoints; later evidence creates a new checkpoint or reopens proof | BarrierSnapshotReceipt, registry version, high-water, dependency inventory position, reconciliation receipt and unresolved counts |

**Permission race qualification:** D does not own I's PermissionEpoch or revocation ordering. D requires I to supply an authoritative, current, commit-usable decision. A stale cached ALLOW, caller-supplied epoch or numeric comparison is never sufficient. Until I and Storage specify and prove how revocation freshness is bound to the final visibility commit, that part of CR-P1-01 remains OPEN and the implementation must fail closed.

## 3. Producer Work State Machine

### 3.1 States

| State | Meaning | Publication capability |
|---|---|---|
| Registered | Stable WorkItemId and durable D registration receipt exist | None until later checks |
| CapturedByBarrier | An installed fence's immutable barrier snapshot includes this work | None by virtue of capture |
| Staged | Candidate artifact exists only in private staging | Forbidden |
| DependencyRegistered | Complete dependency set is durably recorded | Forbidden until final gate |
| PublishEligible | All preconditions currently appear satisfied; this is a revocable evaluation, not a durable permit | No standalone capability; must revalidate at commit |
| Published | Exact artifact/version has a committed PUBLISHED receipt and authoritative visibility marker | Only while current read-time fence/authorization checks permit |
| Suppressed | Work/output is durably prevented from ordinary publication or exposure | Forbidden |
| Rejected | Admission, dependency or publication was durably denied | Forbidden |
| RetryPending | Same logical WorkItemId remains open; a new attempt may be issued after fresh checks | Forbidden for stale/currently unvalidated attempt |
| Terminal | Durable final disposition proves no unresolved or future publication path remains | Forbidden except a separately registered, authorized new work item not derived from a fenced lineage |

### 3.2 Allowed transitions and guards

- ABSENT -> Registered: only after durable RegisterProducerWork acceptance.
- Registered -> CapturedByBarrier: only when a committed fence snapshot includes the registration sequence.
- Registered -> Staged: only after valid receipt and current pre-execution authorization/fence checks.
- CapturedByBarrier -> Staged: may occur for already-running pre-fence work, but does not confer publish permission; the final gate still applies.
- Staged -> DependencyRegistered: only after the complete required dependency set has durable receipts.
- DependencyRegistered -> PublishEligible: only after current work/attempt/lease, source revisions, Scope, Fence and Permission checks pass.
- PublishEligible -> Published: only at the atomic/linearizable visibility commit with a committed PublicationReceipt.
- Any nonterminal state -> Suppressed: only with durable suppression/quarantine evidence and proof that no attempt can later publish.
- Any admission/gate state -> Rejected: only with a durable typed rejection receipt.
- Registered/CapturedByBarrier/Staged/DependencyRegistered -> RetryPending: only while preserving WorkItemId and lineage; old attempt/lease is invalidated.
- RetryPending -> Registered: same logical registration is resolved, then a fresh AttemptId/LeaseEpoch is established; it is not a new admission.
- Published/Suppressed/Rejected -> Terminal: only after all outputs and future publication paths are accounted for and D commits terminal evidence.
- Terminal is immutable for that work identity. Late evidence does not rewrite it; it invalidates/reopens the applicable Forget proof and creates an audited reconciliation obligation.

No transition from an unregistered, unknown, partially registered, stale-authorization, stale-fence or incomplete-dependency state may enter Published. PublishEligible is not a bearer token and expires whenever any bound precondition changes.

### 3.3 Retry, lease and replay identity

WorkItemId is the root barrier identity across retry, lease replacement, DLQ replay and worker recovery. AttemptId, LeaseId and monotonic LeaseEpoch identify executions only. A replaced or expired attempt cannot register dependencies, publish or terminalize using stale lease evidence. Recompile creates a new DerivationRunId explicitly linked to the original source lineage and requires an explicit D admission/re-admission decision; it cannot reset lineage or bypass an active fence.

## 4. Fence / Permission Dual Validation Contract

FenceGeneration and PermissionEpoch are independent typed namespaces owned by different authorities.

Before the final visibility commit, all of the following must be true:

1. **Current Fence:** D establishes the latest applicable ForgetFence for the artifact, every source ancestor and the exact target/version family. Unknown or unavailable fence means deny.
2. **Current Permission:** I establishes the current PermissionEpoch and authorization decision under its policy-domain semantics. Stale, revoked, unknown or unavailable decision means deny.
3. **Principal binding:** the authenticated Principal/ProducerIdentity is validated by I/H trust mechanisms; payload identity is not proof.
4. **Scope authorization:** every source and target ScopeRef is valid and authorized for the authenticated Principal and producer operation. Scope mismatch or missing binding means deny.
5. **Work state:** the WorkItemId is durably registered, nonterminal, in the correct Forget barrier disposition, and its producer class is enabled for the operation.
6. **Attempt/lease state:** AttemptId and LeaseId (when used) are current; the LeaseEpoch has not been superseded or expired.
7. **Dependency state:** every required direct and transitive dependency receipt is durable, complete, immutable and bound to the exact artifact/version, WorkItemId and lineage digest.
8. **Artifact binding:** the staged artifact identity/version and payload digest match the publication request and dependency receipts.
9. **Atomic visibility:** the above predicates and the transition to visible are one externally observable linearization point or a proven equivalent crash-safe protocol.

Forbidden:
- comparing, incrementing, converting or substituting PermissionEpoch and ForgetFenceGeneration;
- treating admission-time authorization or observed fence as final authorization;
- treating a D fence receipt as I permission;
- treating an I permission decision as exemption from a D fence;
- accepting an old single-use token without revalidating the current fence and permission at visibility commit;
- exposing an artifact while any required check is unknown.

## 5. Storage Semantic Requirements (implementation-neutral)

D specifies observable semantics only. Storage may choose a database transaction, linearizable conditional write/CAS, coordinator, durable prepare/commit protocol, distributed transaction or another mechanism, provided it proves the same externally observable behavior.

Storage MUST demonstrate:

1. A durable total order between RegisterProducerWork and InstallForgetFence for each applicable authority/lineage.
2. Fence installation and captured ProducerRegistrationHighWater are one indivisible observable decision; retries return the same generation and H.
3. Complete dependency registration is durable before visibility; partial/unknown sets are not publishable.
4. Final fence + permission + work/lease + dependency validation is bound to the visibility commit. A prior check followed by an unrelated write is insufficient.
5. The successful PublicationReceipt and authoritative visibility marker cannot disagree after crash, failover, retry or restore.
6. Stable IDs and canonical request digests make all operations idempotent; same ID/digest returns the original result; same ID/different digest conflicts.
7. Unknown commit outcomes are queryable by the original ID and remain hidden until resolved.
8. Lease replacement has a monotonic fencing epoch or equivalent condition that rejects stale workers.
9. Outbox delivery is replayable/idempotent but is not itself the safety serialization mechanism.
10. Every consumer path uses the authoritative visibility predicate; staging bytes, object URLs, indexes, caches, delivery queues and rebuilds cannot bypass it.
11. Restore/rebuild begins quarantined and reapplies the current independent Forget and revocation control state before serving.
12. Durability, replication, failover, isolation, read consistency, retention and backup behavior are evidenced for the actual deployed configuration.

D does not mandate a particular database, SQL isolation level, lock type, vendor feature or physical topology. A proposed mechanism is not accepted merely because its description sounds serializable.

### 5.1 Explicit rejection criteria

D rejects any proposed realization that permits:
- local fence read followed by independent visibility write;
- queue ordering or process-local mutex as the sole registration/fence order;
- accepted work omitted from captured H;
- partial dependency set followed by visible artifact;
- gate ACK followed by a separately exposed artifact without a commit-bound protocol;
- replayable/stale publication token after fence advancement or permission revocation;
- lease expiry or DLQ parking to close the barrier;
- direct object-store/index/cache/delivery reads that bypass committed visibility;
- recovery from an older snapshot that serves before current control-ledger replay;
- unknown outcome interpreted as success.

The current Storage proposal's shared transactional coordinator is directionally compatible with these requirements, but remains PROPOSED / NOT IMPLEMENTED / NOT VERIFIED. D does not certify it.

## 6. Fault / Race Proof Matrix

All rows below are required conformance scenarios. Evidence names are required artifacts to retain; they are not claims that such evidence currently exists.

| # | Scenario and operation sequence | Required linearized result | Required durable evidence | Forbidden result |
|---:|---|---|---|---|
| 1 | Registration and fence installation start concurrently; both contend for the same authority/lineage order | Registration first => accepted sequence <= captured H and work remains barrier-open. Fence first => reject/quarantine or cleanup-only. Exactly one order | RegistrationReceipt/digest/sequence; FenceReceipt/generation/H/snapshot; authoritative ordering trace | Accepted work outside H but able to execute/publish |
| 2 | Fence commit succeeds; response/ACK is lost; caller retries InstallForgetFence | Same ForgetOperationId/digest resolves to the same generation, H and snapshot; no recapture | Durable fence row/receipt, operation digest, original H, lookup result, outbox event ID | New generation or later H allocated on retry; caller assumes failure and forks operation |
| 3 | Complete dependency registration commits; process crashes before receiving ACK or before publish | Dependency receipt/edges remain durable; artifact remains private; recovery resolves same DependencyRegistrationId/digest and rechecks fence/permission | DependencyRegistrationReceipt, complete edge-set digest, inventory position, private visibility state, recovery lookup | Crash causes partial visible artifact or duplicate dependency identity |
| 4 | Publish visibility commit succeeds; response/ACK is lost | Same PublicationOperationId/digest returns original PublicationReceipt; visibility matches that committed result exactly once | PublicationReceipt, visibility commit ID/cursor, authoritative reader result, idempotency lookup | Second publication effect, missing receipt for visible artifact, or blind new operation ID |
| 5 | Artifact staged and dependencies registered under fence G; G+1 commits before final publish | Final gate sees latest applicable fence and rejects/quarantines; no visibility commit | G/G+1 fence receipts, dependency receipt, final rejection receipt, private marker and reader denial | Admission-time G or stale cache authorizes publication after G+1 |
| 6 | PermissionEpoch P observed; I revokes/advances to P+1 before final publish | If I confirms revocation first, final gate rejects. If ordering/currentness cannot be established, remain private. Publish-first is valid only if I's commit-bound decision proves it was current at the visibility point | I decision reference, policy domain/epoch, revocation event/order evidence, Principal/Scope binding, gate result and visibility record | Stale ALLOW, numeric comparison to FenceGeneration, or unproven cross-service freshness |
| 7 | Worker lease expires while work remains open; old worker resumes | Lease expires only the attempt. Work remains barrier-open; stale LeaseEpoch cannot register/publish/terminalize; new attempt must revalidate | WorkItemId, old/new AttemptId, LeaseId/LeaseEpoch, expiry/claim receipts, stale-gate rejection | Expiry treated as terminal or old worker commits |
| 8 | Two workers retry the same logical work concurrently | Both retain the same WorkItemId/lineage; one current lease epoch controls publication; duplicate compute may occur but only valid attempt may commit | RegistrationReceipt, attempt/lease history, monotonic lease epochs, publication idempotency receipt and loser rejection | Two independent work identities or both attempts publish |
| 9 | DLQ item is replayed after fence or permission changes | DLQ is nonterminal; replay uses same WorkItemId, new AttemptId, fresh fence/permission checks; covered lineage is suppressed/rejected | DLQ/replay audit, stable WorkItemId, new attempt/lease epoch, current gate receipt | DLQ parking treated terminal; replay bypasses barrier |
| 10 | Index rebuild/backfill replays historical staged/published records | Rebuild work is registered; only committed PUBLISHED records are candidates; current fence/permission and source ancestry are rechecked before index commit; covered/unknown records excluded | Rebuild WorkItemId/receipt, PublicationReceipt lookup, fence/permission decisions, index batch/partition watermark and exclusion evidence | Historical publication receipt alone authorizes current exposure |
| 11 | Adapter reconnect replays an old queued Delivery after a Forget fence or PermissionEpoch change | Old delivery is suppressed/cancelled or rebuilt from current authorized Context; current fence/permission and delivery identity are revalidated before handoff | DeliveryId/attempt, authenticated Adapter/session, current fence and PermissionEpoch decision, cancellation/reconciliation ACK | Reconnect replays stale payload because old delivery was previously accepted |
| 12 | Late derivative arrives after barrier checkpoint or apparent completion | Immediately quarantine/suppress; record lineage and producer-class defect; invalidate/reopen prior barrier proof; reconcile D and I inventories; no visibility | Late artifact/lineage digest, discovery time, prior/new checkpoint refs, suppression receipt, registry/inventory update and reopen event | Prior completion remains current or late derivative becomes visible |

## 7. D / E / Storage OPEN Decision Register

| Decision | D disposition | E disposition | Storage disposition | Overall |
|---|---|---|---|---|
| Work registration vs fence total order | Semantics DECIDED | Consumer mapping exists; exact callable interface remains OPEN | Shared coordinator proposed, not implemented | OPEN for CR-P1-01 |
| Immutable barrier high-water | Semantics DECIDED | Must consume fence snapshot and preserve work identity | Same transaction proposed | OPEN for implementation |
| Dependency registration completeness | Semantics DECIDED | Complete lineage/receipt required; API details OPEN | Atomic complete-set write proposed | OPEN for implementation |
| Publish/fence linearization | Semantics DECIDED | Final gate and hidden staging required; cross-boundary gate OPEN | One commit/visibility pointer proposed; not proven | P0 OPEN |
| PermissionEpoch at final commit | D requires I-authoritative current decision | I decision mapping requested/not confirmed | Must bind decision freshness to visibility commit | OPEN / I + Storage |
| Lease/retry/DLQ/recovery | D terminal/barrier semantics DECIDED | Work/attempt lifecycle specified | Durable lease epoch/recovery proposed | NOT VERIFIED |
| Index rebuild / Adapter replay / Context consumers | D requires same fence/lineage checks at boundary | F/G/H own execution and evidence | Visibility predicate must prevent bypass | OPEN / F-G-H |
| Global inventory and completion | D provides canonical barrier result only | E supplies producer evidence | Storage supplies backup/restore evidence | OPEN / I |
| Physical erasure / external copies | Not D-owned | Not E-owned | Execution evidence required where applicable | OPEN / I + target owners |

**CR-P1-01 MUST remain OPEN.** D's semantic definition does not prove the database transaction, deployed storage behavior, permission freshness protocol, or cross-module conformance. It cannot be closed until E and Storage jointly confirm the implementable interface and the required conformance evidence exists. I's authorization decision and global inventory remain separately owned.

## 8. Baseline and evidence boundary

This Phase 3.6 addendum consumes the branch-aware sources recorded in the Phase 3.6 baseline manifest:
- A Phase 3.5 review: A branch, exact review artifact.
- D Forget completion and operation contracts: D branch.
- E Producer Admission, Derived Registration and Phase 3.6 Conformance: E branch.
- Storage atomicity proposal: Storage branch.
- I Global Forget inventory/completion contract: I branch.

Source branch HEADs must be re-queried before any later integration sign-off. Historical SHAs embedded in older reports are not current branch evidence.

**Non-claim:** this document is a D-owned semantic contract and static design artifact. It does not assert executable implementation, a deployed linearizable database, successful race/fault tests, global Forget completion, backup erasure or physical deletion.


## 9. Exact source baseline manifest (pre-edit discovery snapshot)

The following branch HEADs were queried before this D-owned Phase 3.6 edit. Blob SHAs identify the exact source artifacts read. These values are historical source snapshots for this work, not assertions that the other branches remain at these tips after this discovery.

| Artifact | Owner | Source branch | Source branch HEAD (full SHA) | Path | Source blob SHA | Evidence status |
|---|---|---|---|---|---|---|
| Phase 3.5 Cross-Module Closure Review | A | `session-a-integration-2026-11-16` | `5ce61e0982ce8e22b29f1267ca67c9a085a96a06` | `reviews/integration/phase-3.5-cross-module-closure-review.md` | `a05f1d817514bbed7bddec1729d6598d0835ef3e` | Artifact Exists; A review conclusion BLOCKED |
| D Forget Completion Contract (source before this edit) | D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | `03-memory-brain/forget-fence-and-completion-contract.md` | `cce2108899525c9ce6808716224641baa11faf4f` | Artifact Exists; D semantic decision DECIDED |
| D Operation / Publication Gate (source before this edit) | D | `session-d-memory-brain-2026-11-16` | `da8e5882d0b238d765d00b2225b79eea45a483b1` | `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `2c5b1358ff58f99af838b741a75966ccd07ad088` | Artifact Exists; D operation semantics DECIDED |
| E Producer Admission | E | `session-e-memory-compiler-2026-11-16` | `a19feb57c85819cc0e49ab39abfd945b268aa51e` | `04-memory-compiler/compiler-state-and-producer-admission.md` | `e59f517fff161ab882aa0ddc4a5bda513964ae1a` | Artifact Exists; E-owned design, implementation OPEN |
| E Derived Registration | E | `session-e-memory-compiler-2026-11-16` | `a19feb57c85819cc0e49ab39abfd945b268aa51e` | `04-memory-compiler/forget-fence-and-derived-registration.md` | `00e37ba56596e710513c8d0568acd79141d9101b` | Artifact Exists; interface/atomicity OPEN |
| E Phase 3.6 Producer Publication Conformance | E | `session-e-memory-compiler-2026-11-16` | `a19feb57c85819cc0e49ab39abfd945b268aa51e` | `04-memory-compiler/phase-3.6-producer-publication-conformance.md` | `a21f81dfe53ae6998818d2cc59e865f5dd1b839d` | Artifact Exists; DESIGN COMPLETE / IMPLEMENTATION NOT VERIFIED |
| Storage Forget Atomicity Realization Review | Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `3a14550648f21c0bc2725dac38b29e099c2f3196` | `reviews/storage-consistency/forget-atomicity-storage-realization-review.md` | `5e2d55c8b210997693a7f83d35a5a03588e4ae6b` | Artifact Exists; PROPOSED / NOT IMPLEMENTED / NOT VERIFIED |
| I Global Forget Inventory and Completion Evidence | I | `session-i-security-governance-2026-11-16` | `d52cd47972bd9d1d17f0fe6f2ab09646d084a80b` | `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` | `9100061fa986fb6676656169de3fcf9fc1c72664` | Artifact Exists; CANDIDATE; cross-owner conformance OPEN |

Related branch tips also freshly discovered: B `66adf6bdcf5ec69a146fe75afe20ce3b85af8448`; C `a585307222b0169c007915c25ff8ed0da517f3e4`; F `f86f9b536ea69d8e0fbb4bf290c7023ef0eada76`; G `557c68fd863f73dd09f6fccb3b9e920740db2e9c`; H `1ee65928f123d92a4758b0de09bc8d6df1e46253`; main `8a6414158c9c056c1638222534e1993d1bbc99d2`. These are dependency context, not cross-module approval.

 
## Phase 3.6.2 — D owner acceptance of revised JF-10 v2

**Status: D ACCEPTS THE D-OWNED SERIALIZATION AND FENCE PREDICATES IN THE DE-S v2 PROPOSAL; I ACCEPTANCE AND IMPLEMENTATION REMAIN OPEN.**

D confirms the following as normative D-side requirements for the proposed owner-gate-participating 2PC protocol:

1. D's ForgetOperation, ForgetFence, ProducerClass/ProducerWork ledger, Dependency inventory, BarrierSnapshotReceipt and canonical suppression proof remain D-owned.
2. For each Canonical Memory Authority, RegisterProducerWork, RegisterDerivedDependency, InstallForgetFence and the Storage publication participant serialize on the same durable authority/target-lineage ordering rows. The fence transaction atomically persists its strictly increasing FenceGeneration, immutable target digest, ProducerRegistryVersion, ProducerRegistrationHighWater, BarrierSnapshotReceipt and installation CanonicalCommitCursor.
3. ProducerRegistrationHighWater is scoped to the ProducerWork registration ledger for that Canonical Memory Authority. CanonicalCommitCursor is a separate per-Brain-authority commit-order/audit cursor. Neither is interchangeable with FenceGeneration, PermissionEpoch or I ProducerDomainInventoryEpoch.
4. A prepared Storage participant retains the D fence/lineage serialization locks until I's durable coordinator decision is recovered and the Storage participant commits or aborts. Fence-first means publication prepare rejects; participant-first means fence installation cannot pass the unresolved participant. A timeout is UNKNOWN, not permission to publish or close a barrier.
5. The D final predicate rechecks every source ancestor and target, exact dependency completeness, WorkItem/Attempt/Lease fencing and the latest applicable fence at the participant boundary. I COMMIT_WON never overrides a D fence.
6. ForgetOperation phases remain Requested, FenceEstablished, InventoryOpen, BarrierDraining, TargetReconciliation, CanonicalSuppressionComplete, Blocked and Failed. D may declare CanonicalSuppressionComplete only when its own captured barrier is terminal, all required D-domain targets have suppression proof or an exact I-approved residual exception, and no D-owned unknown/gap/late derivative remains. This is not I Global Forget Completion or physical erasure.
7. A late derivative, newly discovered producer, registry gap or restored stale task invalidates/reopens the relevant D proof and creates an audited reconciliation obligation; it never silently reuses a prior completion checkpoint.

D accepts the v2 protocol only as a proposed cross-authority design subject to I's exact owner-gate review. D does not define I's sequencer implementation, approve I inventory/authorization/exception policy, select a concrete database engine, or claim runtime conformance.


### D36 §9 rows 11–13 — offline rejoin, inventory epoch change and stale task recovery

| Source ID | Test name | Required result | Status |
|---|---|---|---|
| D36 §9 row 11 | Offline producer rejoin after fence | Rejoining worker resolves its original registered WorkItemId and current fence before source access; stale task is rejected/quarantined; offline/unknown producer evidence does not close I global inventory | NOT RUN |
| D36 §9 row 12 | I inventory epoch changes during Forget | D's local ProducerRegistrationHighWater remains unchanged; I seal becomes stale/reopened; no global completion until I issues a replacement seal and all newly applicable targets are reconciled | NOT RUN |
| D36 §9 row 13 | Old Compiler task resumes after CanonicalSuppressionComplete | Current D fence suppresses it before publication; stable WorkItemId/lineage is preserved; any late derivative invalidates/reopens prior D proof and is audited | NOT RUN |

These cases extend the original D36 §9 matrix; they do not renumber or weaken rows 1–10.


## Phase 3.6.2 — D confirmation of Forget ordering at the Applied submission boundary

D reviewed A's pinned C/G/H Applied Contract package (Blob SHA `61d961c32138fd875069e8cbac4696bb031447c0`) and confirms the following D-owned semantics:

1. D issues and validates the authoritative ForgetOperation/Fence identity, generation/cursor, target digest and lineage coverage. A consumer must resolve the latest applicable fence for every relevant source ancestor and target; an observed token without complete lineage/currentness proof is insufficient.
2. The final request submission boundary is a protected disclosure boundary. The applicable D fence must be checked in a causal/linearizable ordering with the actual submit event, not inferred by comparing opaque token values or independent wall-clock timestamps.
3. If the successful submit is ordered before the applicable fence installation, D's later fence does not rewrite that historical submit fact; G may retain a historically valid Applied fact only if C's immutable submit evidence and I's authorization ordering are independently proven. Current-use eligibility is immediately invalidated by the fence.
4. If fence installation is ordered before submit, the request is stale/ineligible and must not be promoted to Full Applied; the managed region remains suppressed.
5. If submit/fence ordering, lineage coverage or fence currentness is unknown or incomparable, the result is Unknown and suppressed. No Full Applied promotion is permitted.
6. A D fence receipt proves only D-owned fence/lineage facts. It does not prove I authorization, H Adapter purge, G Applied, global Forget completion, backup deletion or physical erasure.
7. A committed fence/suppression obligation is not rolled back by later requester revocation; subsequent cleanup must proceed under a currently authorized I service/continuity principal. D does not define or approve that I principal policy.

**D disposition:** **APPROVE D-OWNED FENCE/LINEAGE SEMANTICS WITH AUTHORITY RESERVATIONS** for the exact A package. I authorization and D/E/Storage executable linearization remain separate blockers. D36 and DE-S fault/race suites remain **SPECIFIED / NOT RUN**; no implementation or end-to-end completion is claimed.

## Phase 3.6.2 — D exact-version acceptance of JF-10 prepared participant ↔ COC bridge

**Reviewed exact A artifact:** `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`, A branch `session-a-integration-2026-11-16`, Blob `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`, §12.1–12.8.

**D DECISION: ACCEPT — D-OWNED FENCE/BARRIER SEMANTICS FOR THIS EXACT A BLOB, WITH AUTHORITY RESERVATIONS.**

D accepts the bridge's prospective-participant ordering and barrier requirements as consistent with D's existing fence contract, subject to these binding D interpretations:

1. A quorum-committed `JF10_PREPARE_INTENT_REGISTERED` before a D fence cutoff makes the prospective participant a member of the affected target/source/ancestor barrier, even if Storage PREPARE or the signed prepared receipt has not yet been registered.
2. A D fence cutoff ordered before prepare-intent registration rejects the affected prepare; no Storage XID may be prepared for that lineage.
3. D retains exclusive authority over ForgetOperation, ForgetFence, target/lineage registration, ProducerRegistrationHighWater, BarrierSnapshotReceipt, D fence generation and effective-fence/suppression completion. COC records and positions are evidence of cross-owner ordering; they do not mint D state or clear D obligations.
4. A pre-cutoff participant remains in the D barrier until the I sequencer's exact terminal decision and Storage's same-XID commit/rollback resolution are authoritatively proven and all D lineage obligations are satisfied.
5. An unresolved or ambiguous participant keeps the barrier open. COC/I/Storage outage, timeout, missing row, stale replica or lost ACK cannot release the participant or permit effective fence completion.
6. D and COC positions are typed, separate orders. D does not compare opaque values or infer order from wall-clock time; D consumes the authenticated bridge tuple and its own canonical fence/lineage evidence.

This is D's exact-version architecture acceptance for D-owned fence/barrier semantics only. It does not approve I's sequencer implementation, Storage's database/XA capability, COC deployment/operator, H schema, implementation, conformance or production activation. D36 and JF10-COC-01..10 remain NOT RUN. JF-10 remains P0 OPEN; multi-policy-domain atomicity remains BLOCKED.


## Phase 3.6.2 — D exact acceptance of complete JF-10 ↔ COC decision bundle

**Decision:** **ACCEPT WITH ENUMERATED EXCEPTIONS**, limited strictly to D-owned ForgetFence, producer registration, dependency inventory, lineage and barrier semantics for the single-I-PolicyDomain JF-10 v2 profile. This decision is not I authorization approval, Storage capability certification, C provider approval, H production schema freeze, or production implementation acceptance.

### Exact bundle reviewed
- A COC architecture: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- I JF-10 v2 Owner disposition: `8069ff86988396442c8d9dc3fd58653683abe2f3`
- D/E/Storage common JF-10 v2 recovery protocol: `94679897e84a6f58fd8b9467b5249e1a885cb0b0`
- C bridge Owner contract: `45a48249717c8cddb07ab96197730ef93d406c22`
- D fence/barrier Owner contract: `5a56c406578fdf257509315eb3f6f3f75456116c`
- Storage realization / participant contract: `55c01f4512f2e3d8aac767dd004e768ae073178e`
- H bridge wire mapping Owner contract (current branch readback): `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- H JSON Schema candidate: `a8a945cc3623c2907003b93625e3c79742150944`

### D-owned accepted semantics
1. A quorum-committed COC prepare-intent registered before the D fence cutoff is a prospective D barrier participant, even before Storage's prepared receipt is registered. A D cutoff before prepare-intent rejects the affected prepare.
2. The same preallocated XID/participant identity remains bound through Storage PREPARE, I terminal decision and same-XID commit/rollback resolution. A changed XID, digest, owner boundary or lineage binding is a conflict.
3. Participant-first retains D target/lineage serialization and keeps the D barrier open until I terminal evidence, Storage same-XID resolution, C provider outcome where required, and D lineage obligations are authoritative. Fence-first rejects. There is no third order.
4. UNKNOWN/IN_DOUBT, COC outage, missing log prefix, stale replica, lost ACK, missing participant row or incomplete owner proof cannot release the barrier or establish CanonicalSuppressionComplete.
5. D retains sole authority over ForgetOperation, ForgetFence, ProducerRegistrationHighWater, BarrierSnapshotReceipt, target/ancestor coverage and D completion. COC/I/Storage positions are distinct typed evidence; D does not compare them or infer order from wall-clock time.
6. The outage recovery batch and owner-local pending-gate rules are accepted only as fail-closed coordination evidence. D may reopen its local gate only after durable cutoff, complete pre-batch participant reconciliation and D owner high-water verification.
7. Acceptance is limited to one I PolicyDomain. Multi-PolicyDomain atomicity remains BLOCKED / NOT ACCEPTED.

### Enumerated exceptions / closure conditions
- This is architecture/interface acceptance only. D APIs, durable ledger, locks, participant recovery, COC deployment and production conformance are NOT VERIFIED.
- Storage must prove the selected DB's actual prepared-XID/lock retention, same-XID restart/failover recovery and atomic visibility transaction. D does not select or certify a DB engine.
- I owns the sequencer, receipt consumption, PermissionEpoch and revocation effective point; D's acceptance does not certify I implementation or external governance.
- C provider idempotency/outcome, H generated schema/parser/SDK interoperability, and COC consensus/quorum durability remain separately owned and unverified.
- D36, JF10-01..13, Storage crash/fault and cross-owner conformance remain NOT RUN. JF-10 P0 remains OPEN; no production activation or merge is authorized.
