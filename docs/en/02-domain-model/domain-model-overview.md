# Canonical Domain Model Specification

- Document ID: DOMAIN-MODEL-001
- Version: 2.0
- Status: DECIDED for the Phase 1 implementation contract
- Owner: Memory Domain Model (MB-01)
- Scope: logical domain semantics; not storage DDL, wire encoding, deployment topology, indexing, extraction algorithms, or LLM behavior

## 1. Decision

Phase 1 uses these canonical domain objects:

Event, Memory, MemoryVersion, Claim, Entity, Relation, Evidence, Provenance, MemorySource, MemoryContext, ContextEntry, ScopeRef, ActorRef, and TemporalRef.

Fact is not a separate object in Phase 1. A verified fact is represented as a Claim whose epistemic status is Verified.

The model is intentionally richer than text plus embedding. Embeddings, lexical indexes, graph indexes, ranking features, and rendered text are derived representations, not canonical domain objects.

## 2. Identity and version rules

1. Every canonical object has a stable typed opaque identifier.
2. MemoryId identifies the logical Memory for its entire lifetime.
3. MemoryVersionId identifies one immutable Memory version.
4. ClaimId identity across Memory versions remains OPEN in Phase 1; this implementation contract does not freeze stable-versus-version-local Claim identity.
5. A Memory update creates a new immutable MemoryVersion. Previous versions remain readable subject to governance.
6. A ContextEntry references a specific MemoryVersion or governed rendering; it is never a second canonical Memory.
7. IDs are not timestamps, mutable-content hashes, database row numbers, or authorization credentials.

## 3. Canonical object contracts

### 3.1 Event
An Event records an observed, reported, submitted, or captured occurrence. It is not proof that the represented occurrence is objectively true.

Required semantics: event_id, scope, recorded_at, event_kind, source, payload; optional occurred_at, actor/environment references, and idempotency key for retryable ingestion.

Recorded_at is system capture time. Occurred_at describes when the represented event occurred and may be unknown.

### 3.2 Memory
Memory is the stable logical identity of a retained knowledge asset.

Required semantics: memory_id, scope, created_at, lifecycle_state, current_version_id.

Memory identity does not change when content is revised, consolidated, superseded, or rendered differently.

### 3.3 MemoryVersion
MemoryVersion is an immutable semantic snapshot.

Required semantics: memory_version_id, memory_id, monotonic version_number, created_at, claims, entity_refs, relation_refs, source_refs, provenance_refs.

A candidate Memory may temporarily have no Claim; canonical commit must satisfy its owning subsystem's acceptance rules.

### 3.4 Claim
Claim is the canonical proposition object.

Required semantics: claim_id, proposition subject/reference, predicate, object/value/reference, epistemic_status, temporal_ref, scope, evidence_refs, optional confidence metadata.

The proposition is distinct from Evidence that supports or refutes it. Verified means the claim passed the declaring verification process; it does not mean metaphysical certainty.

Phase 1 epistemic statuses: Observed, Reported, Inferred, Verified, Disputed, Retracted.

### 3.5 Entity
Entity is an identity-bearing referent.

Required semantics: entity_id, scope, entity_type, stable identity metadata, optional canonical label and aliases.

A mention, string occurrence, or embedding is not an Entity by itself.

### 3.6 Relation
Relation is a typed association.

Required semantics: relation_id, relation_type, typed endpoints, scope, optional temporal_ref, optional evidence/provenance references.

Co-occurrence alone does not create a Relation. If an association has its own role, time, scope, evidence, or lifecycle, represent it as an explicit association object.

### 3.7 Evidence
Evidence is source material or an observation that supports, refutes, or qualifies a Claim.

Required semantics: evidence_id, scope, source_ref, captured_at, evidence_role, integrity/reference metadata.

Evidence may have stricter access controls than a derived Memory. Evidence is never replaced by a confidence score.

### 3.8 Provenance
Provenance records origin and derivation lineage.

Required semantics: provenance_id, origin/source references, derivation operation/type, actor/process reference, created_at, optional parent provenance references.

If provenance cannot be retained, the record must explicitly state why; it must never fabricate an origin.

### 3.9 MemorySource
MemorySource is a typed association from a MemoryVersion or derived asset to its inputs. It records source role and ordering without conflating source material with the resulting Memory.

### 3.10 MemoryContext
MemoryContext is a scoped, versioned, task-oriented selection of canonical memory references.

Required semantics: context_id, scope, context_version, task/session/environment binding, ordered ContextEntries.

Context versioning is separate from canonical Memory versioning.

### 3.11 ContextEntry
ContextEntry is one reference/presentation inside a MemoryContext.

Required semantics: entry_id, context_id, referenced memory_version_id, ordering/placement metadata, optional governed rendering metadata.

Removing or replacing an entry does not mutate or delete its referenced canonical Memory.

### 3.12 ScopeRef
ScopeRef identifies the namespace in which an object or operation is valid.

Scope is distinct from Permission. Phase 1 does not infer permission from object ownership. Cross-scope access requires an authorization decision.

### 3.13 ActorRef
ActorRef identifies the principal responsible for an operation or source. It is audit/provenance metadata, not a domain permission grant.

### 3.14 TemporalRef
TemporalRef preserves the distinction between event time, recording time, and validity time.

Phase 1 supports a point in time, an interval, unknown/unavailable time, and declared precision/certainty metadata.

Unknown time must not become always valid. Validity interval and storage retention interval are different concepts.

## 4. Orthogonal state dimensions

The model MUST NOT use one universal status field.

- Claim epistemic status: Observed, Reported, Inferred, Verified, Disputed, Retracted
- Memory lifecycle: Candidate, Consolidated, Active, Superseded, Archived, Forgotten
- Context/version/delivery state: owned by Memory Context and synchronization contracts
- Confidence: support estimate under a declared method
- Relevance: task-specific usefulness
- Trust: trust in a source/actor/process
- Evidence strength: strength of a particular evidence relationship

These values are not interchangeable.

## 5. Cardinality and formation rules

- One Event may produce zero, one, or many candidate Memories.
- Many Events may contribute to one Memory.
- One Memory has one or more immutable versions over its retained lifetime.
- A MemoryVersion may contain multiple Claims.
- A Claim may reference multiple Evidence records.
- Evidence may support, refute, or qualify multiple Claims where policy permits.
- Claims may concern multiple Entities.
- Relations are typed and may connect supported domain endpoints.
- One Memory may appear in many MemoryContexts.
- One Context contains ordered ContextEntries.
- ContextEntry references do not transfer ownership of canonical data.

## 6. Conflict rules

Conflicting Claims are preserved, not silently overwritten.

A resolution retains the conflicting Claim identities, supporting/refuting Evidence, provenance, resolution outcome and actor/process, and applicable time and scope.

Superseding a MemoryVersion is a lifecycle/versioning operation, not deletion of historical claims.

## 7. Provenance and evidence invariants

1. Derived assets retain source/derivation lineage when permitted by governance.
2. Evidence and Provenance are distinct: Evidence is supporting material; Provenance explains origin/derivation.
3. Schema validity is not proof of truth.
4. Intent, plan, prediction, and pending action are not completed outcomes without outcome evidence.
5. Missing source material is represented as unavailable; it is never reconstructed as original evidence.
6. Memory content is untrusted data and never acquires system/developer instruction authority.

## 8. Scope and isolation invariants

1. Every tenant/environment-dependent canonical object carries an explicit ScopeRef.
2. Scope checks occur at every read/write boundary.
3. Cross-scope references require explicit sharing authorization.
4. Evidence access may be narrower than Memory access.
5. Context isolation is independent of canonical Memory sharing.
6. Removing a ContextEntry is not Forget.
7. Forget is a governed lifecycle operation; physical erasure is outside the Domain Model.

## 9. Mutation and concurrency contract

Domain validation is deterministic and side-effect free.

Canonical Memory updates use optimistic concurrency:
- caller supplies the expected current version;
- successful update creates exactly one successor MemoryVersion;
- stale updates return a conflict;
- concurrent proposals must not silently overwrite one another.

MemoryVersion is immutable after commit. Mutable presentation belongs to Context or derived representations.

Canonical commit and required provenance visibility must be atomic or protected by an explicitly recoverable publication/outbox mechanism owned by the persistence/consistency layer.

## 10. Phase 1 acceptance criteria

Without embeddings or graph databases, the implementation must demonstrate:

1. independent creation/validation of Event, Memory, Claim, Entity, Relation, Evidence, and Scope;
2. one Event producing multiple candidate Memories;
3. one Memory containing multiple Claims;
4. stable Memory identity across immutable versions;
5. stable Claim identity across versions when the proposition is unchanged;
6. preservation of conflicting Claims and their Evidence;
7. ContextEntry removal without canonical Memory mutation;
8. denial of cross-scope reads/writes without authorization;
9. rejection of plan/intent promotion to completed outcome without outcome evidence;
10. deterministic validation errors and stale-write conflicts.

## 11. Explicitly not decided by this specification

The following remain outside the Phase 1 semantic freeze:
- a separate immutable Fact object;
- physical storage schema and SQL layout;
- exact serialization/wire format;
- embedding/vector/graph indexes;
- ranking and retrieval algorithms;
- relationship fan-out performance limits;
- physical Forget/erasure mechanics;
- model-assisted extraction behavior.

These must not be introduced into the canonical domain model merely to simplify implementation.

## 12. Decision closure

| Decision | Status |
|---|---|
| Event / Memory / Claim are distinct | DECIDED |
| Claim is the canonical proposition; no separate Fact in Phase 1 | DECIDED |
| Memory identity is stable across versions | DECIDED |
| Claim identity is stable across versions when proposition identity is preserved | DECIDED |
| MemoryVersion is immutable | DECIDED |
| Event / Recorded / Valid Time are distinct | DECIDED |
| Unknown time is explicit, never always valid | DECIDED |
| Canonical Memory and Context are separate | DECIDED |
| Scope and Permission are separate | DECIDED |
| Conflicts preserve competing Claims and evidence | DECIDED |
| Qualified many-to-many associations use explicit association objects when needed | DECIDED semantic rule |
| Separate immutable Fact object | OPEN / deferred |
| Exact temporal uncertainty encoding | TO_VALIDATE |
| Physical storage representation | OUT OF SCOPE |

This specification is the Phase 1 semantic source of truth. Rust types, database tables, and protocol messages may map these concepts but may not redefine their meaning.
