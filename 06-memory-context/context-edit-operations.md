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
