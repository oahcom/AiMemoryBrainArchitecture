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
