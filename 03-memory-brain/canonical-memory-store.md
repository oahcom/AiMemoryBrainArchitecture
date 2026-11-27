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
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-242/evidence.md"
        - "Source branch session-d-memory-brain-2026-11-16 @ b525e1f8fee2471a131e4a38efda99804045e424"
        - "AID-2026-089 / PR #1232 — D-only logical Fence authority"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Historical source restored; §17 Fence-owner wording is explicitly superseded by AID-2026-089. Candidate only; no D Owner acceptance, cross-owner acceptance, implementation or production conformance is asserted."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Candidate
    canonical_scope: "D canonical Memory identity, immutable version, lifecycle and canonical commit/change-feed semantics (historical candidate; Fence boundary controlled by AID-2026-089)"
    canonical_scope_id: "memory-brain/canonical-memory-store"
    canonical_scope_keywords:
      - canonical-memory-store
      - memory-version
      - canonical-commit-cursor
      - index-watermark
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/03-memory-brain/canonical-memory-store.md"
    zh-CN: "docs/zh-CN/03-memory-brain/canonical-memory-store.md"
---
# Canonical Memory Store

> **RECOVERY / AUTHORITY-CONFLICT NOTICE — INFORMATIVE ONLY.** This historical source is restored byte-for-byte after this notice. Its §17 dependency sentence assigns “Forget fence” to I. That phrase conflicts with AID-2026-089, merged by PR #1232 (merge commit `d914e8a1f8a1ba24c21c41a9249489d544388185`): D is the sole logical issuer of ForgetOperation identity/state and ForgetFence generation/cursor; Storage-local fence rows are D-derived, rebuildable projections; I owns authorization, global policy and Global Forget Completion. AID-2026-089 controls that boundary. Do not interpret §17 as granting I Fence issuance or Storage independent Fence authority. This recovered document remains a Draft / Informative candidate, not an approved normative contract.


**Status:** Authority and immutability DECIDED; detailed record layouts and transaction implementation CANDIDATE pending engineering validation.  
**Related blockers:** INT-P0-01, INT-P0-02, INT-P0-03, INT-P0-04, INT-P1-02, INT-P1-06; DM-001..DM-013.

## 1. Purpose

Persist the authoritative identities and immutable versions of Memory assets and their typed links. Provide exact historical reads, atomic canonical commits, lifecycle state authority, provenance visibility, and a recoverable change feed. It is not a vector database, event-ingestion system, or mutable “latest facts” table.

## 2. Scope

Owns Memory identity, MemoryVersion, canonical Claim revision references (subject to ADR), Entity/Relation canonical references, Evidence/Provenance links, LifecycleEvent, ConflictSet and canonical Forget records. It does not own Event ingestion, extraction, ranking, Context versions, policy evaluation, physical erasure or external replicas.

## 3. Responsibilities

- Allocate stable opaque IDs and enforce uniqueness.
- Append immutable MemoryVersion snapshots; never overwrite historical content.
- Maintain a CAS-protected current-version pointer and monotonic commit sequence.
- Validate references, scope compatibility, required evidence/provenance and schema versions.
- Commit canonical data and publication intent atomically or through a recoverable transaction/outbox.
- Support exact version reads and bitemporal “valid at T, known by T2” queries.
- Expose canonical change feed and rebuildable projection checkpoints.

## 4. Non-Responsibilities

No independent truth adjudication, extraction, embedding generation, retrieval ranking, context assembly, Agent reasoning, global authorization policy, backup lifecycle, or physical deletion execution.

## 5. Domain Objects

**MemoryIdentity:** memory_id, owner_scope_ref, applicability_scope_refs, created_at, created_by_actor_ref, schema_family, identity_status. ID is stable and never reused.

**MemoryVersion:** memory_version_id, memory_id, sequence, parent_version_id, commit_sequence, content_digest, immutable_payload_ref/snapshot, claim_refs, entity_refs, relation_refs, evidence_refs, provenance_refs, lifecycle_projection, change_reason, author_actor_ref, recorded_at, schema_version. All fields describe a fixed committed snapshot. lifecycle_projection is a convenience snapshot only; authoritative transition history is LifecycleEvent.

**CanonicalCommit:** operation_id, idempotency_key, request_digest, expected_version_id, resulting_version_id, commit_sequence, outcome, committed_at. It makes retries deterministic.

**LifecycleEvent:** event_id, memory_id, from_state, to_state, actor_ref, scope_refs, reason, policy_decision_ref, related_version_id, occurred_at, sequence. Append-only and the sole authority for lifecycle transitions; current lifecycle state is a projection of this ordered stream.

**OutboxRecord:** event_id, aggregate_ref, aggregate_version, event_kind, payload_ref/digest, created_at, publication_state. A durable publication intent, not a second source of canonical truth.

## 6. Data Model

All records have typed IDs, schema_version, ownership ScopeRef, applicable ScopeRefs, actor/time metadata and content digest where content-bearing. A version snapshot stores canonical object references as typed references, not free-form IDs. Sensitive Evidence content may be stored separately behind stricter authorization; the MemoryVersion stores only authorized ContentRefs and integrity digests.

Claim and Fact persistence is explicitly **ADR-BLOCKED** under INT-P0-01. Until approved, this document permits only a neutral PropositionRef/opaque proposal envelope in non-frozen interfaces; do not generate DDL, public schema, stable cross-module wire fields, or immutable Fact/Claim object identities from either alternative. Candidate revision model: stable Claim identity plus immutable ClaimRevision IDs, each revision tied to one or more MemoryVersions; this remains CANDIDATE under INT-P1-02.

## 7. State Machine

Commit: Draft proposal → Validated → Committed or Rejected/Deferred. Only Committed creates a MemoryVersion and advances current pointer. Retry with same idempotency key and same request digest returns original commit; same key with different digest is IDEMPOTENCY_CONFLICT.

Lifecycle is not a mutable column authority: LifecycleEvent append-only stream is authoritative; current state is deterministic fold/materialized projection. MemoryVersion may snapshot the lifecycle state observed at commit for efficient reads but cannot independently change it.

## 8. Operations

CreateMemoryIdentity; CommitVersion(expected_current_version); ReadCurrent; ReadVersion; ReadAsOf(valid_time, known_by_time); ListChanges(after_sequence, scope_filter); ReadLifecycleHistory; RebuildProjection; ResolveIdempotency; AppendLifecycleEvent.

Commit sequence:
1. Authenticate/resolve ActorRef and ScopeRefs.
2. I authorizes operation/resource; Brain validates scope semantics.
3. Validate schema, expected version, references, content digest and provenance completeness.
4. Verify each referenced object is visible and scope-compatible.
5. Atomically persist immutable version, pointer update, idempotency record and outbox event (or equivalent recoverable commit protocol).
6. Return commit receipt and canonical sequence.
7. Projections/indexes consume outbox asynchronously and publish watermarks.

## 9. Invariants

- A Memory ID is stable across versions and never reused.
- A MemoryVersion is immutable and has at most one parent.
- Current pointer references a committed version of the same Memory.
- Commit sequence is monotonic within the canonical authority.
- A stale expected version never overwrites a newer version.
- Required provenance is committed with the target version or is explicitly marked unavailable.
- No cross-scope reference is accepted without explicit authorized sharing.
- Projection lag never changes canonical truth.
- LifecycleEvent is the unique transition authority (resolves DM-008 candidate).
- Forget does not silently rewrite history; governed erasure may make payload unavailable while retaining only permissible non-reconstructive tombstone metadata.

## 10. Interfaces

E submits candidate objects and a proposed parent/base reference; Store returns canonical Memory ID, MemoryVersion ID, commit sequence, lifecycle decision and outbox event ID. E cannot write Store internals or bypass Lifecycle Manager.

F reads current or exact historical versions, with mandatory scope filters and explicit expansion limits. Store returns canonical records plus projection watermark only where relevant; F must not treat a stale projection as canonical.

G references immutable Memory ID + MemoryVersion ID. G owns ContextVersion and ChangeSet; Store does not track Context lifecycle. If G chooses current-at-read, it must pin the resolved version in its committed Context entry.

H receives opaque typed references only; wire representation belongs to H. I supplies authorization decision/policy version and Forget/Retention obligations. Every call has actor, scope, idempotency and correlation metadata.

## 11. Error Handling

NOT_FOUND_OR_NOT_VISIBLE; STALE_VERSION; IDEMPOTENCY_CONFLICT; INVALID_REFERENCE; SCOPE_MISMATCH; PERMISSION_DENIED; INVALID_SCHEMA; PROVENANCE_INCOMPLETE; CONTENT_DIGEST_MISMATCH; LIFECYCLE_EVENT_ORDER_ERROR; OUTBOX_LAG; HISTORY_UNAVAILABLE_DUE_TO_FORGET. Errors are structured and disclosure-safe.

## 12. Consistency

Canonical transaction boundary includes identity/version rows, current pointer, commit receipt, lifecycle event if part of the operation, and outbox intent. If the selected storage cannot atomically commit all, use a durable prepare/commit protocol with recovery markers; do not expose a partially committed version as canonical. Outbox consumers are at-least-once; event IDs and aggregate version make processing idempotent. Indexes and graph projections are rebuildable from canonical records plus retained event/provenance history.

## 13. Security / Scope

Scope filter occurs before materializing query candidates. Evidence ContentRef dereference requires independent authorization. No name-based lookup can return identity without scope and permission checks. Forget fence/suppression must be consulted by reads and projection consumers. Cache and index namespaces include principal/scope/environment and policy/grant revision; stale grants invalidate or bypass cache. Memory text is untrusted data (INT-P0-04).

## 14. Performance Considerations

Candidate only: append-only versions plus compact current projections; periodic snapshots may accelerate historical folds but remain derived. Measure write amplification, snapshot size, CAS contention, outbox lag, historical query cost, scope filtering overhead and rebuild throughput. Bound history pagination and avoid loading Evidence payloads unless explicitly requested.

## 15. Observability

Record commit sequence, parent/result version, request digest, actor/scope IDs, correlation/causation, idempotency key hash, transaction duration, CAS conflicts, outbox age, consumer watermark and projection rebuild status. Never log raw forgotten content or protected Evidence.

## 16. Failure Scenarios

- Crash before commit: no visible version; retry may proceed.
- Crash after commit before response: idempotency record returns original receipt.
- Outbox publish failure: durable record is replayed.
- Stale writer: reject and require reread/reconciliation.
- Projection corruption: rebuild from canonical source; do not repair canonical records from projection.
- Missing historical payload after governed Forget: return explicit forgotten/unavailable result, not fabricated content.
- Authorization outage: fail closed for protected reads and writes.

## 17. Dependencies

Domain Model (B) for typed semantics; Lifecycle Manager for transitions; E for proposal contract; F for read/projection semantics; G for pinned MemoryVersion references; H for ActorRef/wire identity; I for authorization, Forget fence, retention and erasure policy; Storage/Consistency for transaction, backup and recovery implementation.

## 18. Open Questions

- OPEN: INT-P0-01 ADR must resolve Fact/Claim before schema freeze.
- CANDIDATE: stable Claim ID + immutable ClaimRevision; confirm with E/F/G.
- OPEN: transaction/outbox implementation and atomicity guarantees.
- OPEN: canonical sequence partitioning and multi-tenant ordering.
- OPEN: legal retention/tombstone fields after Forget; coordinate with I.
- TO_VALIDATE: storage engines, snapshot cadence, read/write and recovery benchmarks.


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


## Phase 3 remediation — canonical commit contract

### Commit cursor decision

**DECIDED (D domain contract):** `CanonicalCommitCursor` is a globally ordered cursor within one Canonical Memory authority, not a per-aggregate revision. The per-aggregate revision remains a separate `AggregateRevision`. The canonical transaction record is the join point: it records the commit cursor and the exact aggregate revision(s) created by that transaction. A transaction may advance multiple aggregate heads while receiving one commit cursor.

The cursor is allocated in the serialized commit path only after all validation/CAS checks succeed and the transaction is durably committed. The commit record, immutable writes, head changes, LifecycleEvent appends and outbox intent become visible atomically. A rejected CAS or aborted transaction consumes no cursor. Readers never observe a partially committed transaction.

### Gap, replay and outbox

The canonical committed stream is contiguous by definition. A consumer-observed gap is an operational gap (missing publication, failed application or unavailable history), not permission to skip. Consumers persist the last contiguous applied cursor, replay after it with idempotent event IDs, and repair a gap before advancing. If history has expired, a consistent snapshot plus its base cursor is required. Outbox delivery can be delayed, duplicated or retried; it cannot renumber commits. IndexWatermark is F-owned and reports the contiguous canonical prefix applied by one index partition. It is not the outbox's private offset and not a ForgetFenceCursor.

### Transaction visibility tests

1. Commit of a MemoryVersion + aggregate head + LifecycleEvent + outbox intent yields one cursor and all become visible together.
2. CAS failure yields no new revision, event, outbox intent or commit cursor.
3. A crash after durable commit but before outbox publish is recovered by replaying the same committed event IDs and cursor.
4. Duplicate/out-of-order delivery does not duplicate effects or advance a contiguous watermark across a missing commit.
5. A snapshot at cursor N plus replay after N yields the same canonical state as a full replay.
6. Two aggregates committed in one transaction share the transaction cursor but retain independent aggregate revisions.

### Interfaces

- E publishes/consumes its own durable ingress and compile cursors; E receives CanonicalCommitCursor only as D's commit result and registers derived dependencies before visibility.
- F consumes CanonicalCommitCursor and publishes its own per-index IndexWatermark; it revalidates canonical state and ForgetFence before exposure.
- G consumes D lifecycle/change signals and exact MemoryVersion refs; G's ContextVersion is independent.
- H transports opaque typed refs and acknowledgements; D defines no wire encoding.
- I supplies authorization/revocation policy; D defines no policy epoch or global completion rule.
