# Canonical Memory Store

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
