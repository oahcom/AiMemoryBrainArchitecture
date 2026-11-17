# Phase 3.6.6 — D Forget Semantic Authority Addendum

- Owner: D — Memory Brain
- Branch: `session-d-memory-brain-2026-11-16`
- Status: **D semantic contract proposal; owner implementation/conformance OPEN**
- Supersedes: none. This addendum sharpens, and must be read with, `forget-fence-and-completion-contract.md`.
- Base D contract Blob: `1f0391bc49d007c44ec74165bd33d37412cc7990`
- Authority boundary: D defines canonical Forget semantics and per-operation producer/dependency barrier. I alone defines Global Inventory governance, external-recipient/backup policy, exceptions and Global Forget completion.

## 1. Normative semantic model

Forget is a monotonic, fail-closed operation over a precisely identified canonical target set and its derivation closure. It has three non-substitutable outcomes:

1. **Coverage established** — the operation's requested scope and canonical targets are resolved, and the relevant producer/dependency domain is known sufficiently to install a meaningful fence. Coverage is not proof that every global recipient or backup is inventoried; that is I's separate responsibility.
2. **Canonical suppression established** — the D fence is durable, all covered pre-fence work is terminalized, the dependency closure is reconciled, and all D-owned canonical targets are suppressed.
3. **Global Forget completed** — an I-owned decision over the sealed global target inventory and required owner evidence. D cannot assert this state.

No timeout, lease expiry, missing row, queue deletion, process restart, successful API response or absence from a local index is terminal evidence.

## 2. Coverage

A Forget operation MUST bind:
- stable `ForgetOperationId`, requester/authorization decision reference and normalized request digest;
- exact `ScopeRef` set, canonical target TypedObjectRefs and version-family semantics;
- immutable initial target-set digest and the resolution policy/version used to expand aliases, descendants and lineage;
- a coverage snapshot/cursor, dependency-inventory version and producer-class registry version;
- explicit unresolved/ambiguous identities, inaccessible scopes and unknown producer classes.

Coverage is **COVERED** only when every requested identity is either resolved to a canonical target or explicitly rejected before fence installation. Ambiguous aliases, unresolved target identity, unknown scope, registry gap or incomplete lineage discovery yields **COVERAGE_BLOCKED**. A caller cannot narrow the requested scope silently to obtain coverage.

Coverage is a point-in-time resolution input, not a promise that no later derivative exists. Later discoveries are handled by dependency closure and barrier reopening.

## 3. Registration

D owns the canonical producer-class registry and concrete per-operation work-registration ledger for work that can create, transform, replay or publish derivatives of D canonical targets.

The registration rule is **register before execute; register before visible**:
- A producer class is registered with stable class identity, accountable owner, source/target domain, admission boundary and contract version before protected work is enabled.
- Each concrete work item is durably registered before execution/lease acquisition. The record binds stable WorkItemRef, ProducerClassRef, source refs and revisions, lineage, target ScopeRefs, operation/correlation IDs, admission cursor, observed fence generation, attempt/lease and retry/replay ancestry.
- Each derivative target and dependency edge is durably registered before that derivative becomes visible. The derivative and edge are committed atomically or visibility remains withheld until durable registration is confirmed.
- Retry, DLQ, replay, rebuild, reconnect and redrive are new registered attempts linked to the original source lineage; they do not inherit publication permission from an earlier attempt.

An unregistered producer or work item is a barrier-integrity defect, not an implicit non-member.

## 4. Fence

Fence installation is one canonical durable transaction. It atomically:
1. allocates a strictly increasing, never-reused `ForgetFenceGeneration`;
2. records the immutable ForgetOperation and target-set digest;
3. captures the producer-registration high-water and dependency-inventory snapshot/cursor;
4. records the exact pre-fence work-item barrier membership;
5. publishes a recoverable fence-installation event/outbox intent.

The fence covers exact target identities, their version families, known descendants and all derivatives whose source lineage intersects the covered set. A new Memory ID, rewritten payload, changed partition, replayed job or alternate producer is not a lineage escape.

Every canonical read, reference resolution, mutation and publication boundary MUST check the latest applicable fence. A stale or unavailable fence authority fails closed for affected targets. Final publication MUST recheck after computation and immediately before visibility.

## 5. High-water and barrier membership

`ProducerRegistrationHighWater` is a D-owned monotonic cursor in the D registration-ledger namespace. The fence transaction captures value H and the barrier contains every registration committed at or before H that can affect the operation's target/lineage closure.

The barrier is not:
- I's `ProducerDomainInventoryEpoch`;
- I's `PermissionEpoch`;
- an index watermark, Context version, COC log index or Storage LSN;
- a count inferred from queue depth.

Membership is derived from the authoritative registration ledger and its cursor, not from a producer-supplied list. Every member must have a durable terminal disposition. A work item registered after fence installation that references a covered lineage MUST be rejected or admitted solely as a non-publishing suppression/cleanup task; it cannot extend publication rights.

If the registration high-water, ledger generation, lineage inventory or barrier membership changes during proof construction, the proof attempt is stale and MUST be recomputed against the new authoritative snapshot.

## 6. Dependency closure

Dependency closure is the least fixed point of the following relation, evaluated against canonical lineage and dependency records:
- requested target → canonical descendants and version families;
- source target → every registered derived artifact;
- derived artifact → its own descendants, copies and further derivatives;
- each producer/work item → all outputs it created or attempted to create;
- each target → all canonical references and publication surfaces controlled by D.

Closure MUST preserve source-to-derived edges and exact revisions. It is not enough to search by current payload text, display name, or latest object ID.

Closure is **CLOSED** only if:
- every discovered derivative has an owner and durable target record;
- every relevant producer/work registration up to the captured high-water is accounted for;
- all required lineage edges are present and reconciled to a stable cursor;
- no unresolved producer, work item, output, lease, retry, DLQ/replay, publication intent or target remains;
- post-fence discovery has been incorporated and prior proof invalidated.

Unknown lineage, missing edge, inaccessible partition, unexplained target, ownerless derivative or a non-reconcilable cursor yields **CLOSURE_OPEN**.

## 7. Terminalization

Each pre-fence barrier member MUST reach exactly one durable terminal disposition, bound to operation, work item, attempt, producer, source lineage and fence generation:

- `PUBLISHED_BEFORE_FENCE`: publication is proven to have committed before the fence; all outputs are in dependency closure and independently suppressed.
- `CANCELLED_NO_OUTPUT`: cancellation is proven and no output became visible.
- `SUPPRESSED_QUARANTINED`: output/attempt is durably prevented from becoming visible and any extant derivative is in closure.
- `FAILED_PARKED_NO_PUBLISH`: failure is durably recorded, publication remains disabled and recovery ownership is explicit.

`UNKNOWN`, timeout, expired lease, missing worker, absent queue message, unacknowledged cancellation or ambiguous commit is nonterminal. A terminal receipt MUST identify the evidence authority and exact attempt; aggregate counts without member-level reconciliation are insufficient.

## 8. Barrier reopen and proof invalidation

A previously closed barrier MUST reopen (and any derived `CanonicalSuppressionComplete` proof MUST be marked stale/invalid for current evaluation) on any of:
- a newly discovered producer class, instance, work item or derivative that belongs to the operation's closure;
- a post-fence derivative or publication attempt whose source lineage intersects the forgotten set;
- a changed producer registry version, registration high-water, ledger generation or lineage reconciliation cursor that is relevant to the proof;
- missing, revoked, unauthenticated, contradictory or rolled-back terminal evidence;
- restore/recovery that cannot prove the D control ledger and fence high-water are at least as current as the pre-restore authority;
- a previously hidden queue, retry, DLQ, offline producer or externalized canonical derivative becoming visible.

Reopen is monotonic evidence invalidation, not fence rollback. The ForgetFence remains active. Reopen creates a new reconciliation generation/attempt, preserves the old proof for audit, records the triggering evidence and owner, and requires a fresh closure/terminalization pass. No owner may manually close the barrier by deleting the triggering record.

## 9. D terminal state machine and proof

D operation state is monotonic:
`REQUESTED → COVERAGE_BLOCKED | COVERED → FENCE_INSTALLED → CLOSURE_OPEN → BARRIER_DRAINING → CANONICAL_SUPPRESSION_COMPLETE`.
The middle reconciliation states may repeat after reopen; the fence generation never decreases. `CANCELLED` is permitted only before fence installation and only with durable proof that no fence or protected work was admitted. After fence installation, cancellation cannot remove suppression.

The immutable D proof binds request/target digests, coverage resolution, fence generation and installation cursor, producer registry version, registration high-water, exact barrier membership digest, dependency-closure digest/cursor, per-member terminal receipts, per-target suppression acknowledgements, reopen generation and final reconciliation cursor. It contains no forgotten plaintext.

D proof establishes only canonical-domain suppression and the exact D-owned closure it enumerates. It does not prove external recipient deletion, backup expiry, physical erasure, I governance approval or Global Forget completion.

## 10. Conformance boundary

This is a semantic architecture contract. Durable ledger implementation, concurrent admission/fence linearization, crash recovery, full lineage enumeration, producer integration, restore high-water verification, barrier reopen execution and cross-module negative conformance remain **NOT IMPLEMENTED / NOT VERIFIED** unless separately evidenced by exact build/run artifacts.
