# Context Edit Operations

**Status:** DECIDED semantic rules; CANDIDATE operation encoding  
**Owner:** Session G

## 1. Common contract

Every operation belongs to one Context and one Base Version. It carries operation_id, operation_type, target_entry_id where relevant, typed payload, preconditions, actor, reason, timestamp, policy epoch and idempotency identity. Operation order inside a Change Set is deterministic and significant. All operations are validated against a staged working copy; no partial target version is committed.

Preconditions: Context is eligible for mutation; caller and exact Scope are authenticated/authorized; Base Version matches current head; all canonical refs remain eligible and authorized; no Forget/revocation tombstone blocks them; budget and classification constraints pass.

A successful non-no-op Change Set creates exactly one immutable Context Version. A no-op may be deduplicated without a version bump (CANDIDATE). No operation mutates Canonical Memory by default.

## 2. Operations

### Add
- **Purpose/input:** add a Context Entry referencing exact Memory ID/version, rendering/projection ref, tier/priority, activation reason, source/evidence refs and validity.
- **Preconditions:** entry absent or stable ID supplied; exact canonical version readable and authorized; no duplicate membership conflict.
- **Output/version:** new entry; one new Context Version on committed non-no-op set.
- **Idempotency:** same operation ID + normalized payload returns prior result; same key/different payload is IDEMPOTENCY_KEY_REUSE. Default membership dedupe key is (context, memory, version, rendering profile).
- **Failure/audit:** reject entire set; audit actor, canonical ref/version, reason, auth epoch and result.
- **Canonical effect:** none.

### Update
- **Purpose/input:** change Context metadata or rendering profile; includes entry_id, expected_entry_revision and patch.
- **Preconditions:** entry active/deferred and revision matches; new rendering remains authorized and tied to same or explicitly changed canonical version.
- **Output/version:** new entry revision in enclosing Context Version.
- **Idempotency:** same operation ID/patch is no-op.
- **Failure/audit:** stale entry revision conflicts; invalid patch rejects entire set; audit changed fields and before/after hashes.
- **Canonical effect:** none.

### Remove
- **Purpose/input:** remove membership by entry_id, reason and optional expected revision.
- **Preconditions:** entry exists in staged view; Context mutation authorized.
- **Output/version:** membership tombstone; historical versions remain subject to retention.
- **Idempotency:** repeated same removal is no-op; otherwise absent entry returns not found.
- **Failure/audit:** stale revision conflicts; audit entry, reason, actor and prior version.
- **Canonical effect:** none; not Forget.

### Replace
- **Purpose/input:** atomically substitute old entry with new canonical ref/version and metadata; optionally inherit position.
- **Preconditions:** old entry active; replacement eligible/authorized; unresolved conflict policy permits; budget valid.
- **Output/version:** old entry removed/superseded and new entry active in one version.
- **Idempotency:** same old/new refs and operation ID returns prior result.
- **Failure/audit:** all-or-nothing; audit both refs, reason and hashes.
- **Canonical effect:** none.

### Reorder
- **Purpose/input:** ordered entry IDs or stable relative-order constraints.
- **Preconditions:** all IDs belong to this Context; no duplicates; omissions are explicit.
- **Output/version:** deterministic position assignments.
- **Idempotency:** identical order is no-op.
- **Failure/audit:** reject cross-Context/unknown IDs; audit prior/new order and rationale.
- **Canonical effect:** none.

### Expire
- **Purpose/input:** entry ID, expires_at or typed expiry predicate, reason.
- **Preconditions:** expiry semantics and clock uncertainty explicit; policy allows change.
- **Output/version:** entry becomes ineligible at effective time; materialize a Change Set/version when desired membership changes.
- **Idempotency:** same expiry condition is no-op.
- **Failure/audit:** unknown condition rejected or conservatively treated as ineligible where policy requires; audit rule/evaluator time.
- **Canonical effect:** none.

### Compact
- **Purpose/input:** selected entries, target budget, compaction profile, retained source refs and declared omissions/loss.
- **Preconditions:** all inputs authorized; provenance/evidence refs retained; risk-critical fields validated; no Forget block.
- **Output/version:** compacted projection/group with source membership and expansion refs; this is a Context artifact, not Canonical Memory.
- **Idempotency:** keyed by source entry/version set + profile + algorithm/model version.
- **Failure/audit:** reject if facts are invented, uncertainty/conflict erased, provenance dropped or authorization fails; audit algorithm, source/output hashes, cost and omissions.
- **Canonical effect:** none; no Compiler consolidation.

### Reconcile
- **Purpose/input:** trigger/watermark, affected refs, current auth epoch, canonical resolution and index completeness.
- **Preconditions:** reauthorize Context and each affected ref; D/governance authoritative status required, not stale F index alone.
- **Output/version:** Change Set of invalidations, updates, replacements, ordering/compaction where justified, unresolved blockers and coverage gaps.
- **Idempotency:** same trigger/watermark/state returns prior run; new watermark creates a new run.
- **Failure/audit:** failed/incomplete run leaves tombstones and marks Stale/ReconcileRequired/Blocked; never restores invalid entries; audit trigger, watermarks, refs, decisions and gaps.
- **Canonical effect:** none; Reconcile cannot rewrite facts or decide truth.

## 3. Atomicity and error categories

A Change Set is all-or-nothing for desired Context state. Per-operation diagnostics may be returned, but they do not imply partial commit. Default Adapter behavior is atomic full-region apply or reject; partial coverage is never silently promoted to full Applied.

Errors: ENTRY_NOT_FOUND, ENTRY_REVISION_CONFLICT, DUPLICATE_MEMBERSHIP, CANONICAL_REF_INVALID, CANONICAL_VERSION_STALE, OPERATION_PRECONDITION_FAILED, CHANGE_SET_ATOMIC_REJECT, IDEMPOTENCY_KEY_REUSE, FORGET_BLOCKED, BUDGET_EXCEEDED, COMPACTION_VALIDATION_FAILED, ORDER_INVALID.

- **DECIDED:** operations do not mutate canonical assets; Change Set commit atomic; Remove != Forget; Compact != canonical consolidation.
- **CANDIDATE:** duplicate Add dedupes by canonical ref/version/render profile; no-op sets do not advance version.
- **TO_VALIDATE:** compaction fidelity under uncertainty/conflict/temporal qualifiers.
- **OPEN:** canonical rendering/evidence refs (D/I), per-entry delivery support and wire encoding (H).


## 4. Phase 3.5 producer, fence and authorization preconditions

The common operation contract is extended with the following owner-typed evidence for any operation that reads, derives, materializes, retains or republishes canonical Memory content:

- authenticated producer/ActorRef binding resolved by I/H; typed ScopeRefs resolved under B/I;
- exact source MemoryRef and MemoryVersionRef, plus complete transitive lineage/provenance references;
- current I PermissionEpoch and action-specific authorization-decision reference;
- current D ForgetFenceCursor and applicable target/lineage decision;
- D ProducerClass/registry version, ProducerWorkItemId, RegistrationReceipt and attempt/lease references where derivative work is admitted;
- D DependencyRegistrationReceipt for every derivative artifact before visibility;
- D final publication-gate receipt/decision for the visibility transition;
- F source completeness and per-index/per-partition IndexWatermark vector when the operation consumes Runtime candidates;
- I TargetId/TargetInventorySeal references only when supplied by I for a registered G-owned Forget target.

These are not interchangeable cursors. A valid Base Version or previously accepted operation does not authorize a later derivative publication. Every retry and final visibility/apply boundary rechecks current permission and ForgetFence.

### 4.1 Operation-specific producer/fence behavior

| Operation | Canonical/derivative behavior under Phase 3.5 |
|---|---|
| Add | Pin exact MemoryVersion and full source lineage. Register the resulting ContextEntry/projection dependency before it can appear in a visible ContextVersion or delivery. |
| Update | Revalidate the new rendering/source version and lineage; register changed derived projection. A metadata-only update still creates a new ContextVersion if semantically changed. |
| Remove | Remove membership only. Do not mutate or Forget Canonical Memory. A replayed older Snapshot/Delta containing the removed or fenced entry must be rejected/superseded. |
| Replace | Validate both old and replacement refs; new lineage must be registered before the replacement becomes visible. The old ref remains historical/audit data under I retention, not active membership. |
| Reorder | Does not change canonical truth, but the ChangeSet/version remains a G-owned derivative record subject to G producer admission and publication controls. |
| Expire | Expiry makes the entry ineligible at its effective time. Any persisted removal/snapshot/delivery is a G derivative and must pass current fence/permission publication checks. |
| Compact | Register every source entry, canonical version and transitive lineage; preserve expansion refs and epistemic/conflict/temporal qualifiers. Compacted output stays private until dependency registration and final publication gate succeed. |
| Reconcile | Consume D/I authoritative triggers and current F completeness. Tombstone first for Forget/revocation; never rebuild a target from a stale snapshot or F-only result. A new safe ContextVersion must pass the same producer/dependency/publication gate. |

### 4.2 Forget precedence over staged or replayed edits

A ForgetFence or permission revocation that wins before the G artifact visibility/apply boundary invalidates any staged ChangeSet, ContextVersion, Snapshot, Delta or Delivery containing the affected lineage. G must reject, quarantine or recompute a new ChangeSet from the current safe head; it must not rebase by silently dropping the fence check, replay a historical operation, or mint a new artifact ID to escape lineage. Tombstones remain effective until D/I authoritative reconciliation says the affected reference is no longer blocked.

A ChangeSet already committed before the fence remains immutable history, but its snapshot/delta/delivery is not eligible for new use after the fence. Historical audit retention follows I policy and must not retain reconstructive forgotten plaintext.

### 4.3 No partial visibility

Operation-level diagnostics may identify which precondition failed, but the desired Context head changes only if the complete ordered operation set, D dependency registration and D final publication gate all succeed. A failed or unknown cross-owner gate leaves the target artifact private and the current head unchanged. Adapter partial coverage is an application outcome, not a partial ChangeSet commit.


## 5. Phase 3.5 — ChangeSet concurrency and replay hardening

### 5.1 Duplicate and concurrent mutation handling

1. Resolve the idempotency namespace only after authenticating the caller and resolving the exact Context/Scope. The namespace includes Principal, Context, operation family and key retention window.
2. Normalize the complete ordered operation list and compute a canonical payload hash before execution.
3. Existing key + same hash returns the original immutable result, including the original TargetVersion. Do not execute operations again.
4. Existing key + different hash rejects with IDEMPOTENCY_KEY_REUSE and emits a consistency/security audit event.
5. Verify BaseVersion equals the authoritative Context head at the commit linearization point. A mismatch rejects with BASE_VERSION_MISMATCH; caller must reload and create a new ChangeSet.
6. Validate every operation against one staged working copy. Commit ChangeSet, immutable ContextVersion, audit and outbox atomically as one G-owned logical transition.
7. Concurrent writers serialize per Context or use equivalent CAS. Exactly one writer may commit against a given BaseVersion; losers re-read and re-plan. No implicit merge or BaseVersion+1 prediction.
8. A committed ChangeSet is immutable. A retry after Forget/revocation does not regain authority from the earlier ALLOW: current permission and fence are rechecked at every protected read, derivation, publication and delivery boundary.

### 5.2 Remove, Forget and replay distinction

Remove creates a G membership tombstone in a new ContextVersion. It does not create a canonical ForgetOperation and does not advance D's ForgetFence. An older Snapshot/Delta/ChangeSet replay that would restore the removed membership is rejected or superseded by the current Context head. A canonical Forget event independently tombstones all matching G entries by exact source lineage and Scope, even if no Remove ChangeSet has yet committed.

### 5.3 Cross-owner visibility gate

A G ChangeSet may be logically validated and staged while D/Storage publication evidence is pending, but the staged artifact is private. It is not a public Context head, a sendable Snapshot/Delta or a Prepared Delivery until:
- D has durably registered every source/dependency edge;
- the current D ForgetFence and I PermissionEpoch have been revalidated at the visibility linearization point;
- D's final publication-gate decision/receipt is available and bound to this exact artifact/digest;
- G's own Context BaseVersion CAS succeeds without a competing head advance.

If any condition is Unknown, failed or stale, do not expose the target or send. This is an explicit cross-owner implementation gate; no callable D API or Storage transaction is implied by this prose.
