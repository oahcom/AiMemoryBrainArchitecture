# Memory Versioning and Historical Semantics

**Status:** Immutable version principle DECIDED; Claim revision and exact transaction/time semantics CANDIDATE/OPEN.  
**Related issues:** INT-P0-01, INT-P0-03, INT-P1-01, INT-P1-02, INT-P1-06; DM-002, DM-003, DM-006, DM-008, DM-009, DM-013.

## 1. Purpose

Define how canonical Memory, Claim, Entity and Relation changes are represented without destructive overwrite; provide deterministic historical queries, concurrency control, idempotency, reconciliation and Forget-aware history semantics.

## 2. Scope

Covers MemoryVersion, ClaimRevision candidate, EntityVersion, RelationRevision, LifecycleEvent sequence, canonical commit receipts, time semantics, historical reference resolution and migration records. ContextVersion and ChangeSet are explicitly G-owned, not defined here.

## 3. Responsibilities

- Define immutable revision identity and parent relationships.
- Define compare-and-swap semantics and stale-write behavior.
- Preserve valid-time and record/transaction-time history separately.
- Provide exact historical lookup and deterministic as-of queries.
- Make retries idempotent and conflicts explicit.
- Preserve Entity merge/split and Relation migration history.
- Coordinate version/dependency enumeration with Forget.

## 4. Non-Responsibilities

No ContextVersion state machine, delivery/Applied semantics, Event ingestion sequence, BMCP wire version negotiation, global permission policy, storage engine selection or physical erasure policy.

## 5. Domain Objects

MemoryVersion: immutable snapshot for one Memory identity; monotonic per-Memory sequence, parent version, canonical commit sequence, digest, actor, reason, schema version, recorded time, references and content snapshot.

ClaimRevision (CANDIDATE pending INT-P0-01 ADR): immutable revision of a stable Claim identity; revision ID, claim ID, sequence, parent revision, proposition payload, epistemic status, valid time, source/Evidence refs, Provenance refs, ScopeRefs, actor, recorded time, method and digest. Stable Claim ID + immutable revisions is recommended because it preserves identity across corrections while allowing references to exact assertions; alternative successor Claim IDs are compared below.

EntityVersion: immutable attribute/alias profile revision for stable Entity ID.

RelationRevision: immutable predicate/endpoints/validity/evidence/lifecycle revision for stable Relation ID.

LifecycleEvent: authoritative append-only state transition with per-aggregate sequence. Current state is a fold/projection, not a second mutable truth source.

CanonicalCommitReceipt: idempotency key, request digest, expected base, committed version, commit sequence, outcome and timestamp.

MigrationRecord: explicit old/new typed refs, operation kind, mapping/partition, actor, evidence, scope, sequence and reason.

## 6. Data Model

All revisions are immutable, opaque-ID-addressed, schema-versioned and scope-bound. Each revision has one parent except genesis. A branch/fork is not silently merged: canonical aggregate head is advanced with CAS; competing revisions become rejected proposals or explicit reconciliation candidates.

Time semantics:
- Event Time: when represented occurrence happened.
- Recorded At: when Brain accepted/recorded it.
- Valid Time: interval during which proposition/relation is asserted to hold.
- Commit/Transaction Time: when canonical version became authoritative.
TimeValue candidate fields: lower_bound, upper_bound, precision, timezone, certainty, original_phrase, source_ref. TimeInterval includes start/end TimeValue, half-open boundary convention and explicit unknown/unbounded markers. Unknown is not infinity and missing does not mean timeless.

Historical query contract: “valid at T” filters Valid Time; “known by T2” filters canonical transaction/record time. Results identify the exact revision/version and whether it is current, superseded, retracted, archived or unavailable due to Forget.

### Claim identity alternatives (INT-P1-02)

| Dimension | Option A: stable Claim ID + immutable ClaimRevision | Option B: new Claim ID for every correction/successor |
|---|---|---|
| Identity | Proposition thread persists across revisions; revision ID identifies exact assertion | Each assertion/correction is a new identity linked by successor |
| Evidence | Evidence links to exact revision; shared evidence can be linked explicitly | Evidence naturally binds to each Claim, but repeated links proliferate |
| Lifecycle | Epistemic status revisions append; retraction is a revision/event | Old Claim retracts and successor/new Claim is created |
| Versioning | MemoryVersion pins ClaimRevision IDs | MemoryVersion pins Claim IDs; identity churn on correction |
| Conflict | ConflictSet references exact revisions | ConflictSet references separate Claim identities |
| Query | “Claim as known then” requires revision selection | Easier immutable assertion query; harder to group evolving proposition |
| Permissions | Scope on Claim identity and every revision; revisions inherit no broader permission | Scope evaluated per new Claim; successor links separately authorized |
| Storage | Revision table + identity index | More identities and successor graph |

**Recommendation CANDIDATE:** Option A, stable Claim ID plus immutable ClaimRevision. It offers durable referential identity while keeping exact historical assertion immutable. A correction creates a new revision and explicit correction/supersession relation; retraction creates a new epistemic revision/event and does not erase earlier assertions. If the ADR chooses an independent Fact object, FactRecord gets its own immutable revision stream and links to the exact ClaimRevision(s) it attests to. No Claim/Fact schema is frozen before ADR approval.

## 7. State Machine

A revision is Draft → Validated → Committed; committed revisions are immutable. A subsequent revision points to the prior committed revision. Retraction is a new revision/status event; it does not mutate the previous revision. Lifecycle state remains separate and is managed by Lifecycle Manager.

Entity/Relation versions follow the same append-only parent/CAS pattern. Merge/split creates migration records; it never rewrites old refs. ContextVersion and ChangeSet are separate G-owned objects that pin MemoryVersion IDs.

## 8. Operations

ReadHead; ReadRevision; ReadAsOf(valid_at, known_by); CommitRevision(expected_parent); RetractClaim(expected_revision); SupersedeRelation; MergeEntity; SplitEntity; ReconcileConflict; ResolveHistoricalRef; EnumerateVersionDependenciesForForget.

Concurrent update:
1. Client reads head revision/version.
2. Client submits mutation with expected parent and idempotency key.
3. Brain validates schema, scope, permission result, references and evidence.
4. CAS advances head once.
5. A loser receives STALE_VERSION with current visible head ref if authorized.
6. Caller rereads and submits a new reconciled operation; no automatic last-write-wins.

Idempotency: key scoped by ActorRef + operation + resource + relevant ScopeRef; request digest binds canonical payload. Same key/same digest returns original receipt; same key/different digest is conflict. Retention of idempotency receipts must be coordinated with Forget/retention and must not retain forgotten content.

## 9. Invariants

- No committed revision is updated in place.
- Every revision has stable identity and parent lineage.
- One authoritative head per aggregate at a time; concurrent forks require explicit reconciliation.
- Historical query returns exact revision identity and time basis.
- Event, valid, recorded and transaction time are not conflated.
- A correction does not silently rewrite past validity or epistemic status.
- Merge/split and relation migration preserve historical references.
- Context references pin exact MemoryVersion, not a moving current pointer.
- Forget can make content unavailable without falsifying historical sequence metadata.

## 10. Interfaces

E submits candidate revision with expected base, source event/evidence refs, provenance, actor/scope/time and idempotency. Brain returns accepted canonical revision and MemoryVersion refs or structured conflict/defer. F reads exact revision or as-of state and must surface stale/partial projections. G stores Memory ID + MemoryVersion ID in Context Entry; G independently versions Context and ChangeSet (INT-P1-01). H serializes opaque version refs; protocol negotiation belongs to H. I authorizes revisions and Forget, and defines which historical metadata may survive. Every cross-module operation carries schema version, ActorRef, ScopeRefs, correlation/causation and idempotency as applicable.

## 11. Error Handling

STALE_VERSION; REVISION_PARENT_MISMATCH; IDEMPOTENCY_CONFLICT; INVALID_TIME_INTERVAL; TIME_PRECISION_LOSS; SCOPE_MISMATCH; PERMISSION_DENIED; REVISION_NOT_FOUND_OR_NOT_VISIBLE; HISTORY_UNAVAILABLE_DUE_TO_FORGET; MIGRATION_MAPPING_INCOMPLETE; SCHEMA_VERSION_UNSUPPORTED.

## 12. Consistency

Aggregate head update and immutable revision append commit atomically with receipt and outbox. Historical reads use committed transaction sequence, not projection arrival order. LifecycleEvent sequence is unique per Memory aggregate and deterministically folded. Projection rebuild records watermark and schema compatibility. Entity/Relation migration and successor refs commit with the canonical version and outbox intent.

## 13. Security / Scope

Each revision carries or inherits an explicitly resolved ownership/applicability ScopeRef under a documented inheritance rule; it must not broaden scope. Authorization is checked for identity and exact revision access. Evidence refs are independently authorized. Historical queries cannot bypass current policy or Forget suppression. A forgotten payload cannot be reconstructed from revision snapshots, logs, hashes with reversible side data, caches or provenance excerpts.

## 14. Performance Considerations

Candidate optimization: immutable snapshots with periodic compacted read projections and delta chains; canonical authority remains revision history. Bound historical scan, parent-chain depth, relation migration fan-out and conflict query windows. Benchmark snapshot frequency, write amplification, temporal index selectivity, CAS contention and historical read latency. Compaction must preserve required lineage and retention obligations.

## 15. Observability

Record aggregate ID, version/revision ID, parent ID, commit sequence, actor/scope IDs, request digest, idempotency outcome, CAS conflicts, schema version, transaction/recorded/valid times and projection watermark. Metrics include history depth, conflict rate, stale-write rate, reconciliation latency and historical-query partial rate.

## 16. Failure Scenarios

- Concurrent updates: one CAS wins; loser reconciles.
- Duplicate retry after lost response: return original receipt.
- Same idempotency key with altered payload: reject.
- Projection lags: exact canonical read remains available or returns explicit degraded result.
- Unknown schema version: fail safely; never reinterpret fields silently.
- Merge/split projection failure: replay migration records.
- Forget removes payload: preserve only I-approved non-reconstructive audit state; historical content reads return unavailable.
- Clock skew: preserve source time/precision and separate commit time; do not order solely by client timestamp.

## 17. Dependencies

Domain Model time/epistemic semantics; Canonical Store; Lifecycle Manager; E proposal/replay contract; F historical retrieval; G ContextVersion references; H ActorRef and wire compatibility; I retention/Forget policy; consistency/recovery subsystem.

## 18. Open Questions

- OPEN: INT-P0-01 Fact/Claim ADR and resulting revision model.
- OPEN: whether claim corrections are stable-ID revisions or successor identities if ADR chooses different semantics.
- OPEN: ContextVersion/ChangeSet canonical schema is G-owned (INT-P1-01); Brain supplies pinned refs only.
- OPEN: uncertain TimeValue normalization and timezone policy (DM-006).
- OPEN: sequence scope (per aggregate vs global commit stream).
- OPEN: schema/vocabulary registry and migration compatibility (DM-013).
- TO_VALIDATE: immutable snapshot vs delta storage, history query and migration performance.


## Phase 3 remediation — normative cursor boundary (2026-11-16)

This section supersedes any earlier untyped use of “sequence”, “watermark” or “generation”. The following are distinct types and MUST NOT be compared, added, substituted or serialized as one generic integer:

| Type | Authority / scope | Meaning and ordering |
|---|---|---|
| `CanonicalCommitCursor` | D Canonical Store; one Brain authority | Globally ordered committed transaction position. Assigned only at successful atomic commit. It orders canonical transactions, not aggregate revisions or downstream application. |
| `AggregateRevision` | D; one aggregate identity (Memory, Entity, Relation, etc.) | Monotonic revision number within that aggregate. It is not globally comparable and does not imply a commit-stream position. A committed revision also carries its `CanonicalCommitCursor`. |
| `LifecycleEventCursor` | D; one Memory lifecycle stream | Tuple `(memory_id, lifecycle_event_sequence, event_id)`; sequence is contiguous within that Memory's append-only lifecycle stream. Each event also records its enclosing `CanonicalCommitCursor`. |
| `IndexWatermark` | F; one index/channel/partition | Tuple `(index_id, partition_id, applied_through: CanonicalCommitCursor, coverage/schema metadata)`. It means the partition has accounted for every canonical commit through the stated prefix; it is not a D commit cursor and never proves Forget completion. |
| `ForgetFenceCursor` | D canonical Forget authority; operation + affected target set | Tuple `(forget_operation_id, fence_generation, target_set_digest)`; generation is monotonically allocated by D. It establishes a suppression epoch, not a commit position or index watermark. |

A ContextVersion remains G-owned and is not any of the above. BMCP delivery/request identifiers remain H-owned. I's permission/revocation epoch remains I-owned. No D contract defines their wire encoding.

### Canonical transaction visibility and replay

A successful canonical transaction atomically makes visible its canonical object/revision writes, aggregate-head CAS updates, any LifecycleEvent append, a durable CanonicalCommit record, and recoverable outbox intent. The transaction receives exactly one globally ordered `CanonicalCommitCursor` at commit serialization. Aborted/rejected transactions receive no cursor; therefore the committed canonical stream has no holes caused by rolled-back sequence allocation. Readers at an `as_of` cursor observe the whole transaction or none of it. A cursor is visible only after durable commit.

Consumers resume strictly after the last durably applied cursor. Re-delivery is allowed and must be idempotent by stable event/operation ID. A consumer may not advance its contiguous applied prefix past a missing commit, failed transaction application, or unknown schema. Out-of-order work may be staged, but the watermark remains at the last contiguous prefix until the gap is repaired. If retained history no longer covers a requested cursor, the consumer must bootstrap from a consistent snapshot carrying its base cursor and then resume; it must not silently jump to “latest”. Outbox publication may lag or retry, but it cannot change canonical commit order or authority. A projection watermark reports applied coverage only; it never changes canonical truth.

### Lifecycle event cursor

LifecycleEvent sequence is local to a Memory lifecycle stream, allocated only when the event and enclosing canonical transaction commit. Gaps in a consumer's observed sequence mean missing/unapplied lifecycle events and require replay/reconciliation. The event's commit cursor provides cross-aggregate transaction ordering; its lifecycle cursor provides per-Memory lifecycle order. Neither substitutes for the other.


## Phase 3 remediation — version and cursor semantics

**DECIDED:** MemoryVersion sequence is a per-Memory AggregateRevision. It is not the global CanonicalCommitCursor. Every committed MemoryVersion records both. EntityVersion and RelationRevision likewise carry their own aggregate revision and the CanonicalCommitCursor of their commit. Aggregate revision advances only on successful commit; rejected proposals and failed CAS attempts do not consume a revision.

**DECIDED:** LifecycleEventCursor is per Memory lifecycle stream and is independent from both MemoryVersion AggregateRevision and CanonicalCommitCursor. A lifecycle event may be committed in the same transaction as a MemoryVersion, but the three values retain separate names and meanings. The event records the enclosing canonical commit cursor for cross-aggregate ordering.

**DECIDED:** IndexWatermark is owned by F and is scoped to an index/channel partition. It describes a contiguous applied prefix of the canonical commit stream, plus coverage/schema metadata. An index rebuild starts from a consistent canonical snapshot cursor and catches up by replay; it must check the latest ForgetFence before making any candidate visible. Rebuild progress cannot be represented by MemoryVersion sequence or LifecycleEventCursor.

### Historical reads and replay

Historical reads use a committed CanonicalCommitCursor/as-of snapshot and exact aggregate revision refs, never projection arrival order. A consumer's replay cursor is exclusive: resume after the last committed-and-applied cursor. Duplicate replay is idempotent; a missing cursor blocks contiguous advancement. If the replay window has expired, use a consistent snapshot with a base cursor. A per-aggregate history can be sparse in the global commit stream because unrelated aggregates commit between its revisions; this is not a gap in that aggregate's revision sequence.

### Claim / ConflictSet freeze gate

Claim identity, ClaimRevision schema, ConflictSet schema and any field-level references remain **ADR-BLOCKED** until Architecture Governance + B approve INT-P0-01. The present document's existing ClaimRevision table is an option sketch only, not a D decision. D will map the approved ADR into immutable revision mechanics after approval; no schema, DDL, public API or wire contract may be frozen in advance.
