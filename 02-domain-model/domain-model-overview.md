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
4. ClaimId identity policy across Memory versions remains OPEN; Phase 1 does not freeze stable-versus-version-local Claim identity.

### 2.4 Claim Identity Classification and Revision Invariants

Claim identity is determined by proposition identity, not by textual representation, evidence count, confidence score, or serialization.

A Claim has a stable logical identity (`ClaimRef`). Each immutable assertion state is identified by a separate `ClaimRevisionRef`.

The following classification is normative:

| ID | Change dimension | Classification | Lineage | Authorization |
|---|---|---|---|---|
| CI-01 | Subject/entity resolution changes the actual referent | NEW_CLAIM | New ClaimRef; record identity lineage to the prior Claim where related | Authorized identity-resolution decision |
| CI-02 | Predicate changes the asserted relationship or property | NEW_CLAIM | New ClaimRef; related-to lineage where applicable | Authorized claim creation |
| CI-03 | Object/value changes the asserted proposition | NEW_CLAIM | New ClaimRef; related-to lineage where applicable | Authorized claim creation |
| CI-04 | Polarity changes (positive/negative) | NEW_CLAIM | New ClaimRef; preserve the opposing proposition relationship | Authorized claim creation |
| CI-05 | Quantifier changes the proposition's substantive extent | NEW_CLAIM | New ClaimRef; related-to lineage | Authorized claim creation |
| CI-06 | Modality changes the asserted possibility, necessity, obligation, or ability | NEW_CLAIM | New ClaimRef; related-to lineage | Authorized claim creation |
| CI-07 | Temporal qualifier changes the proposition's substantive temporal meaning | NEW_CLAIM | New ClaimRef; related-to lineage | Authorized claim creation |
| CI-08 | Scope changes the namespace or applicability boundary | NEW_CLAIM | New ClaimRef; explicit scope lineage; never silently migrate identity | Authorization in source and target Scope as applicable |
| CI-09 | Evidence changes without changing proposition identity | NEW_REVISION | Same ClaimRef; new immutable ClaimRevisionRef | Authorized revision |
| CI-10 | Provenance or derivation lineage changes without changing proposition identity | NEW_REVISION | Same ClaimRef; new immutable ClaimRevisionRef | Authorized provenance correction |
| CI-11 | Epistemic status changes | NEW_REVISION | Same ClaimRef; new immutable ClaimRevisionRef | Authorized status transition |
| CI-12 | Confidence or evidence-strength assessment changes | NEW_REVISION | Same ClaimRef; new immutable ClaimRevisionRef | Authorized assessment update |
| CI-13 | Formatting, spelling, punctuation, or presentation-only correction | NEW_REVISION | Same ClaimRef; preserve semantic equivalence and prior revision | Authorized editorial correction |

#### Substantive qualifier rule

A qualifier is substantive if changing it changes the proposition's truth conditions, applicability, temporal meaning, modality, or scope.

A substantive qualifier change MUST create a NEW_CLAIM.

A qualifier that changes only representation, without changing proposition meaning or applicability, MUST create a NEW_REVISION.

#### Identity resolution rule

A change in the displayed entity label alone does not create a new Claim if the underlying referent is unchanged.

A change in the resolved referent does create a new Claim.

#### Scope invariant

A ClaimRef is bound to its declared Scope identity.

Changing Scope MUST NOT mutate or silently transfer an existing ClaimRef.

A new ClaimRef and explicit lineage are required.

Cross-Scope lineage MUST NOT transfer access rights. Authorization in the source and target Scope MUST be independently validated as applicable.

#### Revision invariant

A NEW_REVISION MUST preserve ClaimRef and create a new immutable ClaimRevisionRef.

Historical revisions MUST NOT be overwritten.

Every correction MUST record its parent revision and correction reason.

Evidence addition alone does not create a new Claim identity.

Evidence or Provenance reference changes do not authorize changing the Claim proposition.

#### Authorization invariant

Classification MUST be deterministic and recorded with the resulting identity/revision decision.

Implementations MUST NOT independently choose different classifications for semantically equivalent input.

When classification is ambiguous, the system MUST reject automatic identity mutation and require an explicit governed decision.

It MUST NOT silently select NEW_REVISION as a fallback.

F and G MUST consume exact ClaimRevisionRef values.

F and G MUST NOT resolve historical references through semantic similarity, current-head substitution, or an unqualified latest-version lookup.

This section defines semantic identity only. It does not freeze Schema, DDL, public API, or wire representation.

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

### 3.15 Fact, FactRevision and Attestation

Fact is an independently identifiable governed Attestation object.

FactRevision is an immutable version of that Attestation.

Every FactRevision MUST reference:

- Exact FactRef and FactRevisionRef.
- Exact ClaimRevisionRef values being attested.
- Exact EvidenceRef values.
- Exact ProvenanceRef values.
- ScopeRef and applicable visibility constraints.
- Valid-time interval and recorded/commit-time references.
- Attestor principal identity.
- Exact Attestation Method identifier and immutable Version.
- I AuthorizationDecisionRef.
- Attestation outcome, rationale and correction/revocation lineage.

FactRevision MUST NOT silently follow a Claim's latest revision.

Its ClaimRevision references are exact and immutable.

Corrections, withdrawal or reassessment MUST create new governed history. They MUST NOT overwrite prior FactRevision records.

Fact does not represent absolute objective truth.

Confidence alone MUST NOT create Fact.

Verified Claim status alone MUST NOT create Fact.

I is the sole authority responsible for Attestor authorization.

D validates and persists I's exact authorization decision reference. D MUST NOT independently determine Attestor governance authority.

Attestation Method identity proves which declared procedure was invoked. It does not prove that the procedure is correct.

This section defines semantic and governance contracts only. It does not approve physical Schema, DDL, public API, production keys, Trust Root or cryptographic profile.

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

### 8.1 Shared-reference Forget Contract

Forget applies to governed content and its complete dependency closure, not merely to the object through which a request was initiated.

#### 1. Forget target granularity

The Forget target MUST identify the exact governed subject/content and applicable Scope.

Supported dependency targets include:

- ClaimRef and exact ClaimRevisionRef.
- FactRef and exact FactRevisionRef.
- EvidenceRef and protected source payload.
- ProvenanceRef and reconstructive lineage content.
- Derived MemoryVersion and ContextVersion references.
- Indexes, caches, snapshots, staging and replay artifacts.

A shared FactRef MUST NOT be treated as proof that all linked ClaimRevisions share one Forget disposition.

#### 2. FactRevision dependency enumeration

For each FactRevision, enumerate:

- Exact ClaimRevisionRef dependencies.
- EvidenceRef dependencies.
- ProvenanceRef dependencies.
- Scope and visibility dependencies.
- Derived artifacts and transitive descendants.
- Other authorization or retention dependencies.

Dependency enumeration MUST be complete before declaring the relevant Forget operation complete.

Unknown or incomplete dependency sets remain blocked.

#### 3. Shared Fact visibility

A FactRevision linked to multiple ClaimRevisions may remain visible only if every disclosed dependency is independently authorized and not suppressed by an applicable Forget decision.

If a linked ClaimRevision is forgotten:

- The forgotten ClaimRevision MUST NOT be disclosed through the shared Fact.
- Its Evidence/Provenance content MUST be suppressed according to the Forget policy.
- The shared Fact may remain visible only if its remaining content can be independently authorized and does not reveal forgotten information.
- If safe separation cannot be established, suppress the entire affected FactRevision.

#### 4. Evidence and Provenance handling

Evidence and Provenance are independently governed objects and MUST be included in dependency enumeration.

When the forgotten ClaimRevision is the only lawful basis for retaining an Evidence/Provenance payload, that payload MUST be removed or rendered unavailable under the applicable retention policy.

Shared source material may remain only where an independent lawful dependency exists and the remaining content does not reconstruct forgotten information.

#### 5. Other legal ClaimRevisions

A different ClaimRevision may remain historically available if:

- It is not itself forgotten.
- Its own Scope and authorization remain valid.
- Its Evidence and Provenance dependencies remain lawful.
- It does not expose forgotten content through shared references, excerpts, summaries or derived artifacts.

A shared Fact object MUST NOT cause unrelated legal ClaimRevisions to be erased automatically.

#### 6. Universal read-path enforcement

The same current authorization and Forget checks MUST be applied to all read paths, including:

- FR-01: Direct Claim and ClaimRevision reads.
- FR-02: Claim reads through Fact and FactRevision.
- FR-03: Evidence-to-source traversal.
- FR-04: Provenance lineage traversal.
- FR-05: F indexes, caches and retrieval projections.
- FR-06: G existing ContextVersion and historical snapshots.
- FR-07: Historical version lookup, replay, retry and recovery.
- Export: authorized content export and sharing.
- Backup: backup creation and retained copies.
- Restore: restoration and reconstruction before data becomes queryable or deliverable.

No alternative reference, cache key, old version, replay cursor, export, backup, restore process or retained object identifier bypasses the authorization and Forget decision.

#### 7. Physical erasure and audit separation

Three states MUST remain distinct:

1. Physical content erasure: governed payload and reconstructive derivatives are removed where required.
2. Audit retention: only policy-permitted, non-reconstructive metadata may remain.
3. Historical reference unavailability: old identifiers may remain in audit/history, but resolving them MUST return an explicit unavailable/suppressed result.

The existence of an identifier, digest, lineage edge, or historical pointer does not authorize disclosure.

Forget suppression is evaluated before returning content, not after a successful read.

#### 8. Completion invariant

Forget is complete for the declared scope only when all required dependency paths and alternate read paths enforce the same decision.

All required dependencies MUST have a known and reconciled disposition.

If any required dependency, export path, backup copy, restore path, or read path remains unresolved, the outcome MUST remain incomplete or unknown.

It MUST NOT be represented as successful Forget.

#### 9. Test coverage contract

The seven FR identifiers above are stable test identifiers.

Each FR test MUST identify its target, fixture, applicable Forget decision, expected suppression result, actual result, and failure classification.

A test for one FR identifier MUST NOT be treated as evidence that another FR identifier passed.

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
5. Claim identity policy is explicitly tracked as OPEN and must not be frozen by implementation;
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
| Claim identity across Memory versions | OPEN |
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
