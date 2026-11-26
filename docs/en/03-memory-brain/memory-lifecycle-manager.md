# Memory Lifecycle Manager

- Document ID: D-LIFECYCLE-001
- Version: 1.0
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: DEREFERENCED — historical source blob `8b972035b449e1eab546aedc9cc5b30581600c65` retained; no current normative source path exists.
- Source branch head audited: 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- Source: DEREFERENCED — original normative path `03-memory-brain/memory-lifecycle-manager.md` is absent from the current main tree; alternative: [surviving Chinese counterpart](../../zh-CN/03-memory-brain/memory-lifecycle-manager.md) (blob `6710e51561da3a7d10b7937fbdd461f95d9869de`; translation only, not an authoritative substitute).
- Chinese counterpart: [Memory Lifecycle Manager](../../zh-CN/03-memory-brain/memory-lifecycle-manager.md)
- Status: State separation and canonical authority DECIDED; detailed policy thresholds and some transitions OPEN
- Related: INT-P0-02/03/04, INT-P1-02/06; DM-004/007/008/011

## 1. Purpose

Own policy-governed transitions of canonical Memory assets and maintain one auditable lifecycle history. Lifecycle describes management state, not truth, confidence, trust, relevance, or authorization.

## 2. Scope

Covers Memory lifecycle, transition commands, lifecycle history, eligibility signals, conflict-aware transitions, retention/Forget domain support and integration with Entity/Relation references. Claim epistemic status is related but separate. Physical erasure and global authorization remain I-owned.

## 3. Responsibilities

- Validate allowed Memory lifecycle transitions.
- Require evidence/provenance and scope checks appropriate to each transition.
- Keep lifecycle state history append-only and deterministically project current state.
- Prevent Compiler proposals from directly activating or overwriting canonical state.
- Coordinate supersession, archive, retract, and Forget with canonical versions and downstream invalidation.
- Expose Forget Operation records and dependency enumeration to Governance.

## 4. Non-responsibilities

No Event ingestion, extraction, retrieval ranking, context planning, global permission policy, physical deletion, backup expiry, external model deletion, or objective truth determination.

## 5. Domain objects

- **LifecyclePolicyRef:** versioned policy identifier and applicability; thresholds remain I-owned or policy-configured, not embedded in code.
- **LifecycleEvent:** immutable transition record containing event_id, target Memory ID, from/to states, actor_ref, scope_refs, reason_code, evidence_refs, policy_ref/version, expected_version/state, related successor, operation_id, timestamp, sequence, correlation_id. Records who/what/why/when without copying sensitive source text.
- **LifecycleProjection:** derived current state, last event sequence, eligibility flags and projection watermark. Rebuildable.
- **ConflictSet:** conflict_set_id, scoped Claim revision refs, conflict dimensions, evidence refs, valid-time overlap, status (open/resolved/accepted_coexistence), resolution events and authority. Candidate domain structure pending Claim ADR/revision semantics.
- **ForgetOperation:** operation_id, request idempotency, target TypedObjectRefs, requesting_actor_ref, scope_refs, purpose, authorization_decision_ref/version, policy_ref/version, state, created_at, suppression_at, dependency_snapshot_id/watermark, per-target results, retry metadata, residual_exceptions, completion_proof_ref, completed_at. Stores workflow metadata, not forgotten payload.
- **ForgetTarget:** typed target ref, target class, discovered_by, required_action, status, attempts, last_error_code, last_attempt_at, completed_at, proof_ref. Target classes include canonical versions, Claim revisions, Evidence, Provenance descendants, Entity/Relation links, index/vector/graph projections, caches, working sets, Context entries/ChangeSets, backups and external recipients.

## 6. Data model

Memory lifecycle vocabulary: Candidate, Consolidated, Active, Superseded, Archived, Forgotten. A Forget request first creates an operation and suppression fence; Forgotten is the terminal logical state after required in-scope targets meet policy completion criteria. Temporary Forgetting state belongs to ForgetOperation, not a permanent Memory lifecycle state.

Keep independent dimensions:
- Epistemic status: Observed, Reported, Inferred, Verified, Disputed, Retracted.
- Confidence: estimate with scale, method, calibration population and assessed time.
- Trust: source/principal/process trust metadata; not truth.
- Relevance: task- and time-dependent utility; owned by Runtime/activation.
- Evidence strength: claim/evidence-role assessment; not confidence or source trust.
- Lifecycle: management stage only.

## 7. State machine

| From | To | Conditions |
|---|---|---|
| Candidate | Consolidated | Schema/scope valid; provenance complete or explicit gap; Entity/Relation refs valid; duplicate/conflict assessment recorded; lifecycle policy accepts |
| Consolidated | Active | Explicit activation eligibility and authorization; no unresolved blocking governance fence |
| Active | Superseded | Explicit successor/replacement relation; preserve old validity/history and reason |
| Candidate/Consolidated/Active/Superseded | Archived | Retention or policy reason; archive is not deletion |
| Archived | Active | Explicit restore permission; revalidate scope, Evidence availability, currentness and conflicts; append event and new version if content changes |
| Any non-Forgotten lifecycle state | Forgotten | Distinct I-authorized canonical lifecycle transition after I supplies applicable governance completion criterion; in-progress ForgetOperation is not a lifecycle state |
| Forgotten | Any | Forbidden for same identity. New later information creates a new Memory ID |

Rejected candidate is not silently invented as a new lifecycle state: OPEN whether it remains Candidate with terminal decision metadata or is archived. Consolidated may be durable or a transient policy checkpoint (OPEN).

Claim epistemic changes are independent. Retraction records withdrawal; it does not delete evidence or rewrite prior assertion. Correction creates a new Claim revision/successor according to INT-P1-02. A Memory can contain Claims with different epistemic statuses.

## 8. Operations

EvaluateCandidate; AcceptCandidate; Consolidate; Activate; Supersede(successor); Archive; Restore; RetractClaim; OpenConflictSet; ResolveConflict; StartForget; EstablishForgetFence; RegisterForgetProducerWork; DiscoverDependencies; RecordTargetProgress; CloseProducerBarrier; RecordCanonicalSuppressionProof.

All transitions require expected state/version and idempotency key. Compiler may request/evidence a transition but cannot self-authorize it. For async Forget stages, I reauthorizes before each protected or irreversible step.

## 9. Invariants

- Lifecycle and epistemic status never share one status field.
- LifecycleEvent stream is the only authoritative transition history; projection is rebuildable (DM-008).
- No silent transition/overwrite; every change has actor, time, reason, scope and policy reference.
- Superseded content remains historically queryable subject to scope/retention.
- Archived does not mean forgotten.
- Forget fence suppresses ordinary reads/activation before asynchronous cleanup.
- D records CanonicalSuppressionComplete only when producer barrier is closed and every required canonical-domain target has suppression confirmation or explicit I-approved residual exception. This is not global Forget completion, cleanup completion or physical-erasure proof.
- Forget does not guarantee deletion from third-party model/provider data already received.
- No memory text can instruct or authorize tools (INT-P0-04).

## 10. Interfaces

- **E:** submits candidate and transition proposal with evidence, provenance, source epistemic status, scope and idempotency; Lifecycle returns accept/defer/reject and canonical lifecycle event/version reference.
- **F:** consumes current lifecycle projection and excludes/qualifies assets before ranking; respects suppression fences.
- **G:** receives invalidation/reconciliation events for Context Entries referencing superseded/archived/forgotten versions; G owns Context state.
- **H:** transports typed operation refs and status only; H owns protocol acknowledgement.
- **I:** owns permission, retention policy, physical erasure, backup and external-boundary decisions; Brain provides dependency graph and target status.

Interfaces carry ActorRef, ScopeRef, policy version, exact MemoryVersion and correlation IDs.

## 11. Errors

INVALID_TRANSITION; STALE_STATE; STALE_VERSION; MISSING_SUCCESSOR; PROVENANCE_INCOMPLETE; CONFLICT_REQUIRES_RECONCILIATION; SCOPE_MISMATCH; PERMISSION_DENIED; FORGET_IN_PROGRESS; FORGET_PARTIAL; TARGET_UNAVAILABLE; POLICY_CHANGED; ALREADY_FORGOTTEN; IDEMPOTENCY_CONFLICT. Partial Forget remains resumable and visible as partial, never success.

## 12. Consistency

LifecycleEvent append and its canonical sequence are atomic or recoverably committed with outbox. Projection fold is deterministic and replayable. ForgetOperation and per-target progress are durable, monotonic records; retries cannot revert completed targets. Suppression fence must be visible to canonical reads and all downstream projections before cleanup completion is claimed. Dependency discovery uses a snapshot/watermark and records late-arriving derivatives for follow-up suppression/cleanup.

## 13. Security / Scope

Every operation is evaluated against authenticated ActorRef, action, target resource, owner and applicability ScopeRefs, purpose, policy version and grants. Scope does not imply permission. Graph traversal checks every edge and target. Do not expose existence of unauthorized dependencies. Async workers reauthorize. Forget audits must not retain payload being forgotten; tombstone fields must be non-reconstructive and approved by I.

## 14. Performance

Forget dependency discovery and graph traversal may be long-running; use paged cursors, watermarks, bounded fan-out, progress checkpoints and backpressure. Measure suppression latency separately from policy-completion time. Lifecycle reads use rebuildable projection, with canonical event stream as source. Do not sacrifice evidence, scope checks or history to meet latency targets.

## 15. Observability

Metrics: transition counts/rejections, stale-state conflicts, age by lifecycle state, conflict backlog, Forget suppression latency, dependency count, per-target completion latency, retries, unresolved exceptions, policy reauthorization failures. Events carry operation_id, target_ref, actor/scope, stage, attempt, correlation/causation and timestamps; no raw forgotten payload.

## 16. Failure scenarios

- Policy service unavailable: fail closed; no protected transition.
- Concurrent lifecycle transitions: expected state/sequence permits one; others reconcile.
- Dependency graph partially unavailable: Forget remains in progress; record unknown coverage.
- Worker crash: resume per-target checkpoint; do not repeat destructive action unsafely.
- Offline Adapter/cache: suppression event remains durable; policy must define whether completion waits for acknowledgement or uses expiry/key revocation; OPEN with I/G/H.
- External model received memory: record recipient/boundary and residual exception; Brain cannot claim remote deletion.
- Projection lag: canonical lifecycle stream governs; Runtime must not activate stale state.

## 17. Dependencies

Canonical Store for lifecycle event durability and versions; Domain Model for epistemic/time/scope semantics; E for candidate proposals; F for pre-ranking filtering; G for Context invalidation; H for authenticated operation transport and Adapter status; I for permission, retention, backup and erasure policies; Provenance graph for dependency discovery.

## 18. Open questions

- OPEN: Consolidated durable state vs transient checkpoint.
- OPEN: rejected Candidate terminal semantics.
- OPEN: Archived restore rules and Evidence expiry.
- OPEN: Forget completion policy for offline replicas, immutable backups and external model providers (INT-P0-03 / DM-011).
- OPEN: Provenance DAG vs constrained cycles; DAG is recommended candidate pending domain validation (DM-007).
- OPEN: ConflictSet semantics and Claim identity/revision after ADR (DM-003/004).
- TO_VALIDATE: suppression propagation and dependency traversal capacity.

## Phase 3 remediation — separate operation state and canonical lifecycle

### Normative distinction

Memory lifecycle is exactly Candidate, Consolidated, Active, Superseded, Archived, Forgotten. There is no Memory state named Forgetting. The Memory lifecycle field MUST NOT be set to an operation phase, fence state, visibility state or cleanup state.

ForgetOperation has its own durable state machine, independent of Memory lifecycle:

| ForgetOperation state | Meaning |
|---|---|
| Requested | Durable operation ID and idempotency identity exist; I authorization decision is pending/being recorded |
| FenceEstablished | Monotonic fence generation and affected target-set digest are durably committed; canonical reads fail closed for covered targets |
| InventoryOpen | Dependency inventory and producer work registrations are being reconciled |
| BarrierDraining | All pre-fence registered work must reach a terminal fenced outcome; no unregistered producer may bypass admission |
| TargetReconciliation | Per-target suppression/cleanup acknowledgements are collected; unknown/failed targets remain explicit |
| CanonicalSuppressionComplete | D's closed producer barrier and canonical-domain suppression proof are durable; does not assert global policy completion or physical erasure |
| Blocked / Failed | Coverage, authorization, dependency or target evidence is insufficient; resumable where safe |

There is no generic D-owned Complete state meaning the whole system has forgotten data. I may attach a separate governance completion attestation. D records its reference but does not manufacture it.

### Fence and lifecycle ordering

1. I authorizes and supplies policy/identity context; D creates durable operation record and atomically installs fence generation.
2. Canonical reads, writes, dependency registration and publication gates evaluate active fence before returning or exposing a covered target.
3. D enumerates canonical dependencies and closes producer barrier only after every pre-fence registered work item is terminal and every target inventoried.
4. D records per-target outcomes and canonical suppression proof.
5. Only when I supplies required governance completion criterion may D append LifecycleEvent transitioning Memory to Forgotten. This event is not remote physical-erasure evidence.

### Failure and retry

Fence installation is monotonic and idempotent by ForgetOperation ID. Worker crash cannot lower fence or regress a confirmed target. Unknown inventory, expired producer lease without recovery evidence, unreachable required target, cursor gap or missing acknowledgement leaves operation in progress/blocked. Retry resumes from durable registrations and target checkpoints; it does not restart with a weaker inventory snapshot.

### Cursor references

LifecycleEventCursor is (memory_id, lifecycle_event_sequence, event_id), with each committed event also carrying CanonicalCommitCursor. LifecycleEvent sequence is contiguous per Memory; CanonicalCommitCursor orders enclosing transaction globally. LifecycleProjection.last_event_cursor is a LifecycleEventCursor, never an IndexWatermark. F's IndexWatermark and D's ForgetFenceCursor remain separate types.
