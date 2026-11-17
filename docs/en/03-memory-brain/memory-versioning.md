# Memory Versioning and Historical Semantics

- Document ID: D-VERSIONING-001
- Version: 1.0
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: af747f339d03bdd4684b6ed60fca05957dc8e1fb
- Source branch head audited: 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- Source: [D Owner specification](../../../03-memory-brain/memory-versioning.md)
- Chinese counterpart: [Memory Versioning 与历史语义](../../zh-CN/03-memory-brain/memory-versioning.md)
- Status: Immutable version principle DECIDED; Claim revision and exact transaction/time semantics CANDIDATE/OPEN
- Related: INT-P0-01/03, INT-P1-01/02/06; DM-002/003/006/008/009/013

## 1. Purpose

Define how canonical Memory, Claim, Entity and Relation changes are represented without destructive overwrite; provide deterministic historical queries, concurrency control, idempotency, reconciliation and Forget-aware history semantics.

## 2. Scope and ownership

Covers MemoryVersion, candidate ClaimRevision, EntityVersion, RelationRevision, LifecycleEvent sequence, canonical commit receipts, time semantics, historical reference resolution and migration records. ContextVersion and ChangeSet are G-owned.

D defines immutable revision semantics and parentage; Canonical Store persists revisions and commit records; Lifecycle Manager owns lifecycle events; B owns domain/epistemic/time semantics; I owns authorization and Forget policy.

## 3. Responsibilities and non-responsibilities

Responsibilities: immutable revision identity/parent relationships; CAS and stale-write behavior; separate valid-time and record/transaction-time history; exact historical/as-of reads; idempotent retries and explicit conflicts; preserve Entity merge/split and Relation migration history; coordinate version/dependency enumeration with Forget.

Not responsible for ContextVersion state, delivery/Applied, Event ingestion sequence, BMCP version negotiation, global permission policy, storage engine choice or physical erasure.

## 4. Domain objects

- **MemoryVersion:** immutable snapshot for one Memory; per-Memory monotonic sequence, parent version, canonical commit sequence, digest, actor, reason, schema version, recorded time, references and content snapshot.
- **ClaimRevision (CANDIDATE; INT-P0-01 ADR-blocked):** immutable revision of stable Claim identity; revision ID, claim ID, sequence, parent revision, proposition, epistemic status, valid time, source/Evidence refs, Provenance refs, ScopeRefs, actor, recorded time, method and digest.
- **EntityVersion:** immutable attribute/alias profile revision for stable Entity ID.
- **RelationRevision:** immutable predicate/endpoints/validity/evidence/lifecycle revision for stable Relation ID.
- **LifecycleEvent:** authoritative append-only transition with per-aggregate sequence; current state is a fold/projection.
- **CanonicalCommitReceipt:** idempotency key, request digest, expected base, committed version, commit sequence, outcome and timestamp.
- **MigrationRecord:** explicit old/new typed refs, operation kind, mapping/partition, actor, evidence, scope, sequence and reason.

## 5. Data model and time semantics

All revisions are immutable, opaque-ID-addressed, schema-versioned and scope-bound. Each revision has one parent except genesis. A branch/fork is never silently merged: canonical aggregate head advances with CAS; competing revisions become rejected proposals or explicit reconciliation candidates.

Time axes:
- Event Time: when represented occurrence happened.
- Recorded At: when Brain accepted/recorded it.
- Valid Time: interval during which proposition/relation is asserted to hold.
- Commit/Transaction Time: when canonical version became authoritative.

Candidate TimeValue fields: lower_bound, upper_bound, precision, timezone, certainty, original_phrase, source_ref. TimeInterval includes start/end TimeValue, half-open boundary convention and explicit unknown/unbounded markers. Unknown is not infinity; missing does not mean timeless.

Historical query: “valid at T” filters Valid Time; “known by T2” filters canonical transaction/record time. Results identify exact revision/version and whether current, superseded, retracted, archived or unavailable due to Forget.

## 6. Claim identity alternatives (INT-P1-02)

| Dimension | Option A: stable Claim ID + immutable ClaimRevision | Option B: new Claim ID per correction/successor |
|---|---|---|
| Identity | Proposition thread persists; revision identifies exact assertion | Each assertion/correction is a new identity linked by successor |
| Evidence | Links to exact revision; shared evidence linked explicitly | Naturally binds to Claim but repeated links proliferate |
| Lifecycle | Epistemic status revisions append; retraction is revision/event | Old Claim retracts and successor/new Claim is created |
| Versioning | MemoryVersion pins ClaimRevision IDs | MemoryVersion pins Claim IDs; correction causes identity churn |
| Conflict | ConflictSet references exact revisions | ConflictSet references separate Claim identities |
| Query | “Claim as known then” selects revision | Easier immutable assertion query; harder grouping of evolving proposition |
| Permissions | Scope on Claim identity and every revision | Scope evaluated per new Claim; successor links separately authorized |
| Storage | Revision table + identity index | More identities and successor graph |

**CANDIDATE recommendation:** Option A, stable Claim ID plus immutable ClaimRevision. It provides durable referential identity while keeping each historical assertion immutable. Correction creates a new revision and explicit correction/supersession relation; retraction creates a new epistemic revision/event and does not erase prior assertions. If ADR approves independent Fact object, FactRecord gets its own immutable revision stream linked to exact ClaimRevision(s). No Claim/Fact schema is frozen before ADR.

## 7. State machine

Revision: Draft → Validated → Committed. Committed revisions are immutable; successor points to prior committed revision. Retraction is a new revision/status event, not mutation of prior revision. Lifecycle remains separate and is owned by Lifecycle Manager.

Entity/Relation versions use the same append-only parent/CAS pattern. Merge/split creates migration records and never rewrites old refs. ContextVersion/ChangeSet are G-owned and pin MemoryVersion IDs.

## 8. Operations and concurrency

Operations: ReadHead; ReadRevision; ReadAsOf(valid_at, known_by); CommitRevision(expected_parent); RetractClaim(expected_revision); SupersedeRelation; MergeEntity; SplitEntity; ReconcileConflict; ResolveHistoricalRef; EnumerateVersionDependenciesForForget.

Concurrent update:
1. Read head revision/version.
2. Submit mutation with expected parent and idempotency key.
3. Brain validates schema, scope, permission result, references and evidence.
4. CAS advances head once.
5. Loser receives STALE_VERSION with current visible head ref if authorized.
6. Caller rereads and submits a reconciled operation; no automatic last-write-wins.

Idempotency key is scoped by ActorRef + operation + resource + relevant ScopeRef; request digest binds canonical payload. Same key/same digest returns original receipt; same key/different digest conflicts. Receipt retention must coordinate with Forget and must not retain forgotten content.

## 9. Invariants

- No committed revision is updated in place.
- Every revision has stable identity and parent lineage.
- One authoritative head per aggregate; concurrent forks require explicit reconciliation.
- Historical query returns exact revision identity and time basis.
- Event, valid, recorded and transaction time are not conflated.
- Correction does not silently rewrite past validity or epistemic status.
- Merge/split and relation migration preserve historical refs.
- Context references pin exact MemoryVersion, not moving current pointer.
- Forget can make content unavailable without falsifying historical sequence metadata.

## 10. Interfaces

E submits candidate revision with expected base, source Event/Evidence refs, Provenance, actor/scope/time and idempotency. Brain returns accepted canonical revision/MemoryVersion refs or structured conflict/defer. F reads exact revision/as-of state and surfaces stale/partial projections. G stores Memory ID + MemoryVersion ID in Context Entry and independently versions Context/ChangeSet (INT-P1-01). H serializes opaque version refs. I authorizes revisions/Forget and defines which historical metadata may survive. Cross-module operations carry schema version, ActorRef, ScopeRefs, correlation/causation and idempotency as applicable.

## 11. Errors

STALE_VERSION; REVISION_PARENT_MISMATCH; IDEMPOTENCY_CONFLICT; INVALID_TIME_INTERVAL; TIME_PRECISION_LOSS; SCOPE_MISMATCH; PERMISSION_DENIED; REVISION_NOT_FOUND_OR_NOT_VISIBLE; HISTORY_UNAVAILABLE_DUE_TO_FORGET; MIGRATION_MAPPING_INCOMPLETE; SCHEMA_VERSION_UNSUPPORTED.

## 12. Consistency

Aggregate head update and immutable revision append commit atomically with receipt and outbox. Historical reads use committed transaction sequence, not projection arrival order. LifecycleEvent sequence is unique per Memory aggregate and deterministically folded. Projection rebuild records watermark/schema compatibility. Entity/Relation migration and successor refs commit with canonical version and outbox intent.

## 13. Security / Scope

Each revision carries or inherits an explicitly resolved ownership/applicability ScopeRef under documented inheritance; it must not broaden scope. Authorization checks identity and exact revision. Evidence refs are independently authorized. Historical queries cannot bypass current policy or Forget suppression. Forgotten payload cannot be reconstructed from snapshots, logs, reversible side data, caches or Provenance excerpts.

## 14. Performance

Candidate optimization: immutable snapshots plus compact current projections and periodic derived snapshots. Bound historical scans, parent-chain depth, relation migration fan-out and conflict windows. Benchmark snapshot frequency, write amplification, temporal-index selectivity, CAS contention and historical-read latency. Compaction preserves required lineage/retention.

## 15. Observability

Record aggregate ID, version/revision ID, parent ID, commit sequence, actor/scope IDs, request digest, idempotency outcome, CAS conflicts, schema version, transaction/recorded/valid times and projection watermark. Metrics: history depth, conflict rate, stale-write rate, reconciliation latency and historical-query partial rate.

## 16. Failure scenarios

- Concurrent updates: one CAS wins; loser reconciles.
- Duplicate retry after lost response: return original receipt.
- Same idempotency key with altered payload: reject.
- Projection lag: exact canonical read remains available or explicit degraded result.
- Unknown schema: fail safely; never silently reinterpret fields.
- Merge/split projection failure: replay migration records.
- Forget removes payload: retain only I-approved non-reconstructive audit state; historical content read returns unavailable.
- Clock skew: preserve source time/precision and separate commit time; do not order solely by client timestamp.

## 17. Dependencies and open questions

Dependencies: Domain Model time/epistemic semantics; Canonical Store; Lifecycle Manager; E proposal/replay; F historical retrieval; G ContextVersion refs; H ActorRef/wire compatibility; I retention/Forget policy; consistency/recovery.

- OPEN: INT-P0-01 Fact/Claim ADR and resulting revision model.
- OPEN: stable-ID revisions vs successor identities if ADR chooses different semantics.
- OPEN: ContextVersion/ChangeSet schema is G-owned; Brain supplies pinned refs only.
- OPEN: uncertain TimeValue normalization/timezone policy (DM-006).
- OPEN: sequence scope (per aggregate vs global commit stream).
- OPEN: schema/vocabulary registry and migration compatibility (DM-013).
- TO_VALIDATE: immutable snapshot vs delta storage, history query and migration performance.

## Phase 3 remediation — normative cursor boundary

The following are distinct types and MUST NOT be compared, added, substituted or serialized as one generic integer:

| Type | Authority / scope | Meaning |
|---|---|---|
| CanonicalCommitCursor | D; one Brain authority | Globally ordered committed transaction position, assigned only at successful atomic commit |
| AggregateRevision | D; one aggregate | Monotonic revision within aggregate; not globally comparable; committed revision also carries CanonicalCommitCursor |
| LifecycleEventCursor | D; one Memory lifecycle stream | (memory_id, lifecycle_event_sequence, event_id); contiguous per Memory; also records enclosing CanonicalCommitCursor |
| IndexWatermark | F; one index/channel/partition | (index_id, partition_id, applied_through: CanonicalCommitCursor, coverage/schema metadata); coverage only, never Forget proof |
| ForgetFenceCursor | D; operation + target set | (forget_operation_id, fence_generation, target_set_digest); monotonic suppression epoch, not commit position or index watermark |

ContextVersion remains G-owned; BMCP delivery/request IDs remain H-owned; I permission/revocation epoch remains I-owned. D does not define their wire encoding.

### Canonical transaction visibility and replay

A successful canonical transaction atomically exposes object/revision writes, aggregate-head CAS updates, LifecycleEvent append, CanonicalCommit record and recoverable outbox intent. It receives one globally ordered CanonicalCommitCursor at commit serialization. Aborted/rejected transactions receive none; committed stream has no holes from rolled-back allocation. As-of readers see whole transaction or none. Cursor is visible only after durable commit.

Consumers resume after last durably applied cursor. Redelivery is allowed and idempotent. No consumer advances past missing commit, failed application or unknown schema. Out-of-order work may be staged but watermark stays at last contiguous prefix. If history expired, bootstrap from consistent snapshot with base cursor, then resume; never jump to latest. Outbox lag/retry cannot change canonical order. Projection watermark reports coverage only.

### Lifecycle event cursor

LifecycleEvent sequence is local to one Memory stream and allocated only when event and enclosing transaction commit. A gap requires replay/reconciliation. Commit cursor orders cross-aggregate transactions; lifecycle cursor orders per-Memory events. Neither substitutes for the other.

## Phase 3 remediation — version and cursor semantics

**DECIDED:** MemoryVersion sequence is a per-Memory AggregateRevision, not global CanonicalCommitCursor. Every committed MemoryVersion records both. EntityVersion and RelationRevision likewise carry their own revision and the commit cursor. Aggregate revision advances only on successful commit; rejected proposals/CAS failures consume none.

**DECIDED:** LifecycleEventCursor is per Memory lifecycle stream and independent of MemoryVersion AggregateRevision and CanonicalCommitCursor. An event may commit in the same transaction as a MemoryVersion, but all three retain separate names/meanings. Lifecycle event records enclosing canonical commit cursor.

**DECIDED:** IndexWatermark is F-owned and scoped to an index/channel partition. It describes a contiguous applied prefix plus coverage/schema metadata. Rebuild starts from consistent canonical snapshot cursor and replays; it checks latest ForgetFence before any candidate becomes visible. Rebuild progress cannot use MemoryVersion sequence or LifecycleEventCursor.

### Historical reads and replay

Historical reads use committed CanonicalCommitCursor/as-of snapshot and exact aggregate revision refs, never projection arrival order. Replay cursor is exclusive: resume after last committed-and-applied cursor. Duplicate replay is idempotent; missing cursor blocks contiguous advancement. If replay window expired, use consistent snapshot with base cursor. Per-aggregate history may be sparse in global commit stream because unrelated aggregates commit between revisions; this is not a gap in that aggregate's revision sequence.

### Claim / ConflictSet freeze gate

Claim identity, ClaimRevision schema, ConflictSet schema and field-level refs remain **ADR-BLOCKED** until Architecture Governance + B approve INT-P0-01. Existing ClaimRevision table is an option sketch, not a D decision. D maps approved ADR into immutable revision mechanics after approval; no schema, DDL, public API or wire contract may be frozen in advance.
