# Context Versioning and Change Sets

**Status:** DECIDED invariants; CANDIDATE object encoding and serialization policy  
**Owner:** Session G  
**Related:** INT-P1-01, INT-P1-05, C review P2-05/P2-06

## 1. Guarantees

A Context Version is immutable and identifies one complete desired managed-region state. Each Context has one authoritative monotonically increasing sequence. Every committed Change Set identifies Base Version and Target Version. Concurrent mutations cannot silently overwrite; commit uses CAS or equivalent per-Context serialization. Snapshot and Delta represent the same target state; Delta is not independently authoritative. Adapter Applied is separate from Context head.

## 2. Context Version Object

| Field | Meaning |
|---|---|
| context_version_id | Globally unique opaque immutable version ID |
| context_id | Owning Context |
| sequence | Monotonic per-Context integer; never reused |
| parent_version_id | Immediate prior version; null only for genesis |
| snapshot_ref / snapshot_hash | Immutable complete entry snapshot and canonical digest |
| schema_version | Context domain schema |
| scope_fingerprint | Non-reversible binding to resolved Scope/identity/policy epoch |
| canonical_watermarks | Per-source/partition canonical revision watermark |
| policy_epoch | Authorization/policy epoch used at commit |
| committed_change_set_id | Change Set that created this version |
| committed_at | Brain commit time |
| actor_ref / reason | Authenticated principal/service and rationale |
| entry_count / budget_summary | Reproducible aggregate metadata |

Snapshot contains complete ordered Entry state and required membership tombstones. Payloads remain immutable refs or governed projections; permissions are rechecked at every use.

## 3. ContextEntry Version

An Entry is versioned inside each immutable Context Version. Stable identity is scoped to Context; each appearance has an entry revision:
- entry_id, context_id;
- memory_id and exact memory_version (never implicit latest);
- rendering_ref/projection_schema_version;
- tier, priority, position;
- activation_reason and activation_correlation_refs;
- epistemic_status, lifecycle_state, trust and classification;
- source_refs/evidence_refs (typed and permission-checked);
- content_hash, token_estimate, byte_size;
- activated_at, expires_at, valid_time;
- entry_revision, created_by_change_set_id, last_changed_by_change_set_id;
- entry_state and invalidation_reason.

A version pin prevents silent content drift but does not override retraction, Forget or permission revocation.

## 4. ContextChangeSet Object

| Field | Meaning |
|---|---|
| change_set_id | Unique immutable mutation request ID |
| context_id | Target Context |
| base_version | Exact expected Context Version |
| target_version | Allocated only after successful commit |
| operations | Ordered typed operations with stable operation IDs |
| reason | Trigger/business rationale, not arbitrary instruction |
| actor_ref | Authenticated caller/service |
| created_at | Request creation time |
| idempotency_key | Scoped retry identity |
| payload_hash | Hash of normalized request |
| policy_epoch | Authorization epoch checked |
| status | Prepared, Committed, Rejected, Conflict or Aborted |
| correlation_id / causation_id | Cross-system trace linkage |
| result_ref | Immutable operation result/diagnostics |

Target Version is absent before commit; callers cannot guess it from Base+1.

## 5. MemoryContext required object

Required fields: context_id, scope, agent_instance_id, task_id, environment_id, context_version, applied_version, status, budget, created_at, updated_at, expires_at.

Required semantic extensions: agent_id, session_id, principal_scope_ref, project_scope_ref, purpose/profile, schema_version, policy_epoch, canonical_watermarks, last_reconciled_at.

The applied_version field is only a convenience projection. Authoritative application history is per ContextDelivery/Adapter/Context Session/Inference Request; one Context may have multiple consumers at different versions.

## 6. ContextDelivery required object

Required fields: delivery_id, context_id, change_set_id, base_version, target_version, status, timestamps and error.

Semantic extensions: adapter_id, agent_instance_id, agent_context_session_id, inference_request_id, capability_epoch/tier, applied_coverage, managed_region_hash, final_request_hash or privacy-safe attestation ref, boundary_id/timestamp, correlation_id, forget_clear_state and application authorization epoch.

Applied requires explicit Adapter confirmation that the exact target version is completely materialized in the controlled managed region and that this region belongs to the final request submitted to inference runtime. If Adapter cannot observe that final request boundary, it MUST report Unknown or lower capability; it MUST NOT claim Tier 1. A digest is insufficient unless H/C define canonicalization, capture and correlation.

## 7. Snapshot and Delta

- **Snapshot:** complete desired state at Target Version. Required for genesis, gap recovery, unknown base, capability change or unsafe Delta reconciliation. Every canonical reference still requires current authorization.
- **Delta:** ordered operations from exact Base to Target, with base/target hashes, operation IDs and schema version. Apply atomically; duplicate Delivery ID returns prior outcome. Base mismatch rejects and requests Snapshot.
- Delta is not best effort: unknown operation, missing entry, hash mismatch or authorization failure rejects the whole update by default.
- Replaying a Change Set into a different head requires re-planning and a new Change Set, not blind replay.

## 8. CAS, concurrency and idempotency

Recommended initial policy: serialize commits per Context, with CAS on Base Version as a defensive check.

1. Normalize request and compute payload hash.
2. Resolve idempotency key within principal + context + operation family/retention window.
3. Existing key + same hash returns original result/Target Version.
4. Existing key + different hash returns IDEMPOTENCY_KEY_REUSE.
5. Verify current head equals Base Version; else BASE_VERSION_MISMATCH and re-read/replan.
6. Validate all operations against one staged snapshot.
7. Atomically commit Change Set, immutable Version, audit and outbox.
8. Advance head once; no partial commit.

No automatic merge is assumed. Safe rebase is a new Change Set after re-reading canonical and policy state.

## 9. Delivery lifecycle and late acknowledgements

Prepared → Delivered → Applied; alternatives: Rejected, Expired, Superseded.
- Prepared: package materialized/authorized, not confirmed sent.
- Delivered: transport/receiver receipt only.
- Applied: explicit proof satisfies §6.
- Rejected: Adapter refused/validation failed.
- Expired: TTL elapsed before valid application.
- Superseded: newer target replaces it before application.

Timeout is Unknown, not Rejected or Applied. Query by Delivery ID. Late Applied for a superseded version is historical evidence but cannot roll desired head backward; latest Snapshot may be required before next inference.

## 10. Rollback, supersede and replay

Committed versions are never mutated/deleted to roll back. Rollback is a new compensating Change Set after reauthorization/current canonical validation. Supersede creates a new version and marks obsolete undelivered deliveries Superseded. Replay rebuilds the chain from snapshots/Change Sets/audit/outbox; it never reuses stale authorization or bypasses Forget tombstones.

## 11. Applied coverage

- **Full:** complete target version in managed region; exact final request boundary observed; request/session/capability correlation valid.
- **Partial:** identified subset applied; never equivalent to full-version Applied.
- **Bypassed:** inference proceeded without Brain-managed region or used unmanaged fallback.
- **Unknown:** insufficient visibility, timeout, lost evidence, offline Adapter or ambiguous boundary.

Only Full may set Delivery status Applied under strict semantics. Partial/Bypassed/Unknown are non-Applied coverage outcomes. Applied does not establish model attention or use.

## 12. Decision register

- **DECIDED:** immutable versions, monotonic sequence, one authoritative head, explicit base/target, CAS/serialization, atomic Change Set, replayable audit.
- **DECIDED:** Applied ties delivery + session + request + capability epoch + final boundary proof.
- **CANDIDATE:** serialized writer per Context plus CAS.
- **TO_VALIDATE:** snapshot/delta size, hash canonicalization, retry retention and contention.
- **OPEN:** proof/digest fields (C/H); canonical revision watermark schema (D/E/F).
