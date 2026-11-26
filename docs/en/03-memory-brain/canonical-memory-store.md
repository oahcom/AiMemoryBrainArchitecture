---
document_metadata:
  domain: memory-brain
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "Issue #1177"
        - "source commit: b525e1f8fee2471a131e4a38efda99804045e424"
        - "original source blob: 6b37c91033fda21f072e2a3bde6f274663b1e76e"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Existing translated companion body preserved; source pin refreshed; semantic parity review pending."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/03-memory-brain/canonical-memory-store.md"
    zh-CN: "docs/zh-CN/03-memory-brain/canonical-memory-store.md"
---

# Canonical Memory Store

- Document ID: D-CANONICAL-STORE-001
- Version: 1.0
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: d47366d1ca04da37ff77f6edd31fe42efc93e0f9
- Source branch head audited: 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- Source: [canonical D source](../../../03-memory-brain/canonical-memory-store.md) (source commit `b525e1f8fee2471a131e4a38efda99804045e424`; original source blob `6b37c91033fda21f072e2a3bde6f274663b1e76e`).
- Chinese counterpart: [Canonical Memory Store](../../zh-CN/03-memory-brain/canonical-memory-store.md)
- Status: Authority and immutability DECIDED; detailed record layouts and transaction implementation CANDIDATE pending engineering validation
- Related blockers: INT-P0-01..04, INT-P1-02, INT-P1-06, DM-001..DM-013

## 1. Purpose

Persist authoritative identities and immutable versions of Memory assets and typed links. Provide exact historical reads, atomic canonical commits, lifecycle-state authority, provenance visibility, and a recoverable change feed. It is not a vector database, event-ingestion system, or mutable “latest facts” table.

## 2. Scope

Owns Memory identity, MemoryVersion, canonical Claim revision references (subject to ADR), Entity/Relation canonical references, Evidence/Provenance links, LifecycleEvent, ConflictSet, and canonical Forget records. It does not own Event ingestion, extraction, ranking, Context versions, policy evaluation, physical erasure, or external replicas.

## 3. Responsibilities

- Allocate stable opaque IDs and enforce uniqueness.
- Append immutable MemoryVersion snapshots; never overwrite historical content.
- Maintain a CAS-protected current-version pointer and monotonic commit sequence.
- Validate references, scope compatibility, required Evidence/Provenance, and schema versions.
- Commit canonical data and publication intent atomically or through a recoverable transaction/outbox.
- Support exact-version reads and bitemporal “valid at T, known by T2” queries.
- Expose canonical change feed and rebuildable projection checkpoints.

## 4. Non-responsibilities

No independent truth adjudication, extraction, embedding generation, retrieval ranking, context assembly, Agent reasoning, global authorization policy, backup lifecycle, or physical deletion execution.

## 5. Domain objects

- **MemoryIdentity:** memory_id, owner_scope_ref, applicability_scope_refs, created_at, created_by_actor_ref, schema_family, identity_status. ID is stable and never reused.
- **MemoryVersion:** memory_version_id, memory_id, sequence, parent_version_id, commit_sequence, content_digest, immutable_payload_ref/snapshot, claim_refs, entity_refs, relation_refs, evidence_refs, provenance_refs, lifecycle_projection, change_reason, author_actor_ref, recorded_at, schema_version. It is a fixed committed snapshot. lifecycle_projection is convenience only; LifecycleEvent is authoritative.
- **CanonicalCommit:** operation_id, idempotency_key, request_digest, expected_version_id, resulting_version_id, commit_sequence, outcome, committed_at. Makes retries deterministic.
- **LifecycleEvent:** event_id, memory_id, from_state, to_state, actor_ref, scope_refs, reason, policy_decision_ref, related_version_id, occurred_at, sequence. Append-only and sole authority for lifecycle transitions; current state is a projection of this ordered stream.
- **OutboxRecord:** event_id, aggregate_ref, aggregate_version, event_kind, payload_ref/digest, created_at, publication_state. Durable publication intent, not a second source of canonical truth.

## 6. Data model and ADR boundary

All records have typed IDs, schema_version, ownership ScopeRef, applicable ScopeRefs, actor/time metadata and content digest where content-bearing. Version snapshots store canonical object references as typed refs, not free-form IDs. Sensitive Evidence content may be stored separately behind stricter authorization; MemoryVersion stores only authorized ContentRefs and integrity digests.

Claim and Fact persistence is explicitly **ADR-BLOCKED** under INT-P0-01. Until approved, only a neutral PropositionRef/opaque proposal envelope is permitted in non-frozen interfaces. Do not generate DDL, public schema, stable cross-module wire fields, or immutable Fact/Claim identities from either alternative. Candidate revision model: stable Claim identity plus immutable ClaimRevision IDs, each tied to one or more MemoryVersions; still CANDIDATE under INT-P1-02.

## 7. Commit state machine

Draft proposal → Validated → Committed or Rejected/Deferred. Only Committed creates a MemoryVersion and advances current pointer. Same idempotency key/same request digest returns original commit; same key/different digest is IDEMPOTENCY_CONFLICT.

Lifecycle is not a mutable-column authority: the append-only LifecycleEvent stream is authoritative; current state is a deterministic fold/materialized projection. MemoryVersion may snapshot lifecycle state observed at commit for efficient reads but cannot independently change it.

## 8. Operations and commit sequence

Operations: CreateMemoryIdentity; CommitVersion(expected_current_version); ReadCurrent; ReadVersion; ReadAsOf(valid_time, known_by_time); ListChanges(after_sequence, scope_filter); ReadLifecycleHistory; RebuildProjection; ResolveIdempotency; AppendLifecycleEvent.

Commit sequence:
1. Authenticate/resolve ActorRef and ScopeRefs.
2. I authorizes operation/resource; Brain validates scope semantics.
3. Validate schema, expected version, references, content digest and provenance completeness.
4. Verify each referenced object is visible and scope-compatible.
5. Atomically persist immutable version, pointer update, idempotency record and outbox event, or equivalent recoverable commit protocol.
6. Return commit receipt and canonical sequence.
7. Projections/indexes consume outbox asynchronously and publish watermarks.

## 9. Invariants

- Memory ID is stable across versions and never reused.
- MemoryVersion is immutable and has at most one parent.
- Current pointer references a committed version of the same Memory.
- Commit sequence is monotonic within the canonical authority.
- Stale expected version never overwrites a newer version.
- Required provenance is committed with target version or explicitly marked unavailable.
- No cross-scope reference without explicit authorized sharing.
- Projection lag never changes canonical truth.
- LifecycleEvent is the unique transition authority (resolves DM-008 candidate).
- Forget does not silently rewrite history; governed erasure may make payload unavailable while retaining only permissible non-reconstructive tombstone metadata.

## 10. Interfaces

- **E:** submits candidate objects and proposed parent/base reference; Store returns canonical Memory ID, MemoryVersion ID, commit sequence, lifecycle decision and outbox event ID. E cannot write Store internals or bypass Lifecycle Manager.
- **F:** reads current/exact historical versions with mandatory scope filters and explicit expansion limits. Store returns canonical records and projection watermark only where relevant; F must not treat stale projection as canonical.
- **G:** references immutable Memory ID + MemoryVersion ID. G owns ContextVersion/ChangeSet; Store does not track Context lifecycle. If G reads current-at-read, it pins resolved version in committed Context Entry.
- **H:** receives opaque typed refs only; H owns wire representation.
- **I:** supplies authorization decision/policy version and Forget/Retention obligations.

Every call carries actor, scope, idempotency and correlation metadata.

## 11. Errors

NOT_FOUND_OR_NOT_VISIBLE; STALE_VERSION; IDEMPOTENCY_CONFLICT; INVALID_REFERENCE; SCOPE_MISMATCH; PERMISSION_DENIED; INVALID_SCHEMA; PROVENANCE_INCOMPLETE; CONTENT_DIGEST_MISMATCH; LIFECYCLE_EVENT_ORDER_ERROR; OUTBOX_LAG; HISTORY_UNAVAILABLE_DUE_TO_FORGET. Errors are structured and disclosure-safe.

## 12. Consistency

Canonical transaction boundary includes identity/version rows, current pointer, commit receipt, lifecycle event if part of operation, and outbox intent. If storage cannot atomically commit all, use durable prepare/commit with recovery markers; never expose a partially committed version as canonical. Outbox consumers are at-least-once; event IDs and aggregate version make processing idempotent. Indexes and graph projections are rebuildable from canonical records plus retained event/provenance history.

## 13. Security / Scope

Scope filtering occurs before materializing query candidates. Evidence ContentRef dereference requires independent authorization. Name-based lookup cannot return identity without scope and permission checks. Forget fence/suppression is consulted by reads and projection consumers. Cache/index namespaces include principal/scope/environment and policy/grant revision; stale grants invalidate or bypass cache. Memory text is untrusted data (INT-P0-04).

## 14. Performance and observability

Candidate: append-only versions plus compact current projections; periodic snapshots may accelerate historical folds but remain derived. Measure write amplification, snapshot size, CAS contention, outbox lag, historical query cost, scope-filter overhead and rebuild throughput. Bound history pagination and avoid loading Evidence payloads unless requested.

Record commit sequence, parent/result version, request digest, actor/scope IDs, correlation/causation, idempotency-key hash, transaction duration, CAS conflicts, outbox age, consumer watermark and projection rebuild status. Never log raw forgotten content or protected Evidence.

## 15. Failure scenarios

- Crash before commit: no visible version; retry may proceed.
- Crash after commit before response: idempotency record returns original receipt.
- Outbox publish failure: durable record is replayed.
- Stale writer: reject and require reread/reconciliation.
- Projection corruption: rebuild from canonical source; never repair canonical records from projection.
- Missing historical payload after governed Forget: return explicit forgotten/unavailable result, not fabricated content.
- Authorization outage: fail closed for protected reads/writes.

## 16. Dependencies and open questions

Depends on B typed semantics; Lifecycle Manager transitions; E proposal contract; F read/projection semantics; G pinned MemoryVersion refs; H ActorRef/wire identity; I authorization, Forget fence, retention and erasure policy; Storage/Consistency transaction, backup and recovery.

- OPEN: INT-P0-01 ADR must resolve Fact/Claim before schema freeze.
- CANDIDATE: stable Claim ID + immutable ClaimRevision; confirm with E/F/G.
- OPEN: transaction/outbox implementation and atomicity guarantees.
- OPEN: canonical sequence partitioning and multi-tenant ordering.
- OPEN: legal retention/tombstone fields after Forget; coordinate with I.
- TO_VALIDATE: storage engines, snapshot cadence, read/write and recovery benchmarks.

## Phase 3 remediation — normative cursor boundary

The following are distinct types and MUST NOT be compared, added, substituted, or serialized as one generic integer:

| Type | Authority / scope | Meaning and ordering |
|---|---|---|
| CanonicalCommitCursor | D Canonical Store; one Brain authority | Globally ordered committed transaction position, assigned only at successful atomic commit; orders canonical transactions, not aggregate revisions or downstream application |
| AggregateRevision | D; one aggregate identity | Monotonic revision within one aggregate; not globally comparable; committed revision also carries CanonicalCommitCursor |
| LifecycleEventCursor | D; one Memory lifecycle stream | (memory_id, lifecycle_event_sequence, event_id); contiguous within one Memory stream; each event also records enclosing CanonicalCommitCursor |
| IndexWatermark | F; one index/channel/partition | (index_id, partition_id, applied_through: CanonicalCommitCursor, coverage/schema metadata); partition coverage only, never Forget proof |
| ForgetFenceCursor | D; operation + affected target set | (forget_operation_id, fence_generation, target_set_digest); monotonic suppression epoch, not commit position or index watermark |

ContextVersion remains G-owned. BMCP delivery/request identifiers remain H-owned. I permission/revocation epoch remains I-owned. D does not define their wire encoding.

### Canonical transaction visibility and replay

A successful canonical transaction atomically exposes canonical writes/revisions, aggregate-head CAS updates, LifecycleEvent append, CanonicalCommit record, and recoverable outbox intent. It receives exactly one globally ordered CanonicalCommitCursor at commit serialization. Aborted/rejected transactions receive no cursor; committed stream has no holes caused by rolled-back sequence allocation. Readers at an as-of cursor observe the whole transaction or none. Cursor is visible only after durable commit.

Consumers resume strictly after last durably applied cursor. Redelivery is allowed and idempotent by stable event/operation ID. A consumer cannot advance contiguous prefix past a missing commit, failed application, or unknown schema. Out-of-order work may be staged, but watermark remains at last contiguous prefix until repaired. If history no longer covers requested cursor, load a consistent snapshot with base cursor, then resume; never silently jump to latest. Outbox publication may lag/retry but cannot change canonical order. Projection watermark reports applied coverage only, never canonical truth.

### Lifecycle event cursor

LifecycleEvent sequence is local to one Memory stream, allocated only when event and enclosing canonical transaction commit. A consumer-observed gap means missing/unapplied lifecycle events and requires replay/reconciliation. Commit cursor provides cross-aggregate transaction order; lifecycle cursor provides per-Memory order. Neither substitutes for the other.

## Phase 3 remediation — canonical commit contract

**DECIDED (D domain contract):** CanonicalCommitCursor is globally ordered within one Canonical Memory authority, not a per-aggregate revision. AggregateRevision remains separate. Canonical transaction record joins the commit cursor to exact aggregate revisions created by the transaction. One transaction may advance multiple aggregate heads while receiving one commit cursor.

Cursor is allocated in serialized commit path only after validation/CAS succeeds and transaction is durably committed. Commit record, immutable writes, head changes, LifecycleEvent appends and outbox intent become visible atomically. Rejected CAS/aborted transaction consumes no cursor. Readers never observe partial commit.

### Gap, replay and outbox

Canonical committed stream is contiguous by definition. Consumer-observed gap is an operational gap, not permission to skip. Consumers persist last contiguous applied cursor, replay after it with idempotent event IDs, and repair gap before advancing. If history expired, consistent snapshot plus base cursor is required. Outbox delivery may be delayed, duplicated or retried; it cannot renumber commits. IndexWatermark is F-owned and reports contiguous canonical prefix applied by one index partition. It is neither outbox private offset nor ForgetFenceCursor.

### Transaction visibility tests

1. MemoryVersion + aggregate head + LifecycleEvent + outbox intent commit yields one cursor and all become visible together.
2. CAS failure yields no new revision, event, outbox intent or commit cursor.
3. Crash after durable commit but before outbox publish is recovered by replaying same committed event IDs and cursor.
4. Duplicate/out-of-order delivery does not duplicate effects or advance contiguous watermark across missing commit.
5. Snapshot at cursor N plus replay after N yields same canonical state as full replay.
6. Two aggregates in one transaction share transaction cursor but retain independent revisions.

### Interfaces

- E publishes/consumes its own durable ingress/compile cursors; receives CanonicalCommitCursor only as D commit result and registers derived dependencies before visibility.
- F consumes CanonicalCommitCursor and publishes per-index IndexWatermark; revalidates canonical state and ForgetFence before exposure.
- G consumes D lifecycle/change signals and exact MemoryVersion refs; G ContextVersion is independent.
- H transports opaque typed refs and acknowledgements; D defines no wire encoding.
- I supplies authorization/revocation policy; D defines no policy epoch or global completion rule.
