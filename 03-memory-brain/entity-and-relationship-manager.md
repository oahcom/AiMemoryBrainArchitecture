# Entity and Relationship Manager

**Status:** Identity and typed temporal relationship principles DECIDED; merge/split and vocabulary details CANDIDATE/OPEN.  
**Related issues:** INT-P0-02, INT-P0-03, INT-P1-02, INT-P1-03, INT-P1-06; DM-005, DM-006, DM-007, DM-009, DM-010, DM-013.

## 1. Purpose

Manage identity-bearing Entities and typed, evidence-qualified Relations without conflating identity with names, mentions, co-occurrence, or graph projections. Preserve historical identity decisions and reference migration across merge/split operations.

## 2. Scope

Own Entity identity, EntityVersion, alias/mention links, resolution decisions, merge/split records, Relation identity/revisions, typed predicates/values, direction, validity, evidence, scope constraints and canonical graph-reference consistency. Does not own retrieval graph ranking, global policy, event ingestion or physical deletion.

## 3. Responsibilities

- Allocate stable opaque Entity IDs and preserve identity independently of display labels.
- Resolve references using evidence and scope constraints; return ambiguity rather than guess.
- Maintain versioned attributes and aliases with provenance and validity.
- Enforce typed Relation endpoints, directionality, temporal validity, evidence and scope.
- Record Entity merge/split and Relation migration as immutable operations.
- Expose bounded, authorized graph traversal and historical queries.
- Ensure Forget dependency discovery can find Entity/Relation references and derived projections.

## 4. Non-Responsibilities

No name-only identity inference, unrestricted cross-scope entity resolution, truth adjudication, relation ranking, vector similarity policy, Agent planning, or permission granting. A display name is a label, not an identity key.

## 5. Domain Objects

**EntityIdentity:** entity_id, owner_scope_ref, applicability_scope_refs, entity_kind, created_at, created_by_actor_ref, identity_status. Stable and never reused.

**EntityVersion:** entity_version_id, entity_id, sequence, parent_version_id, canonical_attributes, attribute_validity, content_digest, alias_refs, provenance_refs, actor_ref, recorded_at, schema_version. Immutable descriptive revision.

**Alias:** alias_id, entity_id, normalized_label, language/locale, alias_kind, valid_time, source/evidence refs, scope refs, confidence/method metadata. Alias is a scoped, time-qualified label; it is never identity.

**MentionRef:** source object/version, locator, surface form, candidate entity refs and resolution status. A mention is not automatically an Entity.

**EntityResolutionDecision:** decision_id, mention_ref, candidate_entity_refs, selected_entity_ref or unresolved, evidence_refs, method_ref, actor_ref, scope_refs, recorded_at, decision status. Ambiguous results remain ambiguous.

**EntityMergeRecord:** merge_id, source_entity_ids, survivor_entity_id, source versions, evidence refs, relation migration refs, scope refs, actor, reason, commit sequence, timestamp, correction/supersession ref. Explicit redirect map preserves historical lookups.

**EntitySplitRecord:** split_id, source_entity_id, new_entity_ids, partition criteria, affected mention/claim/relation refs, evidence refs, scope refs, actor, reason, commit sequence, timestamp, correction ref. It records how references were partitioned; it never rewrites old history.

**RelationIdentity:** relation_id, canonical subject TypedObjectRef, typed predicate, canonical object TypedValue or TypedObjectRef, direction, owner/applicability scopes, created metadata.

**RelationRevision:** relation_revision_id, relation_id, sequence, parent_revision_id, validity interval, epistemic status, lifecycle state, evidence refs, provenance refs, confidence assessment ref, author ActorRef, reason, recorded_at, schema version, digest. Immutable.

**RelationMigrationRecord:** migration_id, operation kind, old/new relation refs, affected Entity refs, evidence, scope, actor, reason, sequence and timestamp.

## 6. Data Model

TypedPredicate includes vocabulary namespace, predicate code, vocabulary version, arity, endpoint type constraints, symmetry/inverse declaration, temporal behavior and deprecation metadata. TypedValue includes value kind, canonical encoding, optional unit/locale, schema/vocabulary version and explicit unknown/null semantics. No free-form predicate is silently treated as canonical vocabulary.

TypedObjectRef = object_type + opaque object_id + optional immutable version/revision ID + optional scope_ref + reference purpose. ScopeRef = scope_id + registered scope_kind + owner_ref + optional parent_scope_id + scope status/version. ActorRef = actor_kind + stable subject ID + issuer/authentication reference + optional delegation chain; display_name is descriptive only. TimeValue = normalized bounds, precision, timezone, certainty, source phrase and source ref. TimeInterval = start/end TimeValue, boundary convention, and explicit unbounded/unknown markers. ContentRef = content_id, media/content kind, immutable version or digest, locator/access class, availability state and source identity. These are minimum candidate structures; H/I must finalize identity/auth fields.

Relation direction is explicit. For a directed predicate, subject and object positions are normative. Symmetric relations declare symmetry in the vocabulary; inverse traversal may be derived. Candidate default: persist one canonical directed edge and derive inverse traversal; do not duplicate inverse records unless audit/domain semantics require them.

## 7. State Machine

Entity identity: Provisional → Resolved → Merged or Split; Resolved may become Retired under explicit policy. Merged/Split identities remain addressable as historical identities with redirect/partition metadata; never reuse IDs.

Relation lifecycle: Proposed → Active → Superseded or Retracted. A new revision supersedes the prior revision without mutating it. Retraction preserves history and reason. Valid Time is independent of record lifecycle; an active relation can have a bounded validity interval.

## 8. Operations

CreateEntity; AddAlias; ResolveMention; UpdateEntityVersion(expected_version); MergeEntities; SplitEntity; CreateRelation; ReviseRelation(expected_revision); RetractRelation; SupersedeRelation; TraverseRelations(scope, depth, fanout, as_of); ResolveHistoricalReference; RebuildGraphProjection.

Merge workflow: authorize all source/survivor scopes; verify same permitted ownership domain or explicit sharing; assess identity evidence; create immutable merge record and survivor version; create redirects; migrate current references through explicit mapping; retain historical references unchanged; emit change events for F/G and projection rebuild. A merge cannot cross user/project/environment isolation merely because names match.

Split workflow: authorize; define evidence-backed partition; create new Entity identities; assign affected current references explicitly; record unresolved/ambiguous refs; preserve old historical versions and source Entity identity; emit migration record and downstream reconciliation event. Do not automatically split every old historical reference.

## 9. Invariants

- Entity ID is opaque, stable and never reused.
- Alias/display name/mention never establishes identity by itself.
- Resolution is scope-bounded; no implicit cross-user/project/Agent/environment merge.
- Every Entity/Relation has explicit ownership and applicability ScopeRefs.
- Every Relation has typed predicate, direction, endpoint types, lifecycle and validity semantics.
- Evidence and Provenance are independently referenced and independently authorized.
- Merge/split are append-only, auditable, scope-checked and historically reversible by a new correction record, not destructive rollback.
- Relation graph projections are rebuildable; canonical relation revisions are authoritative.
- Forget dependency discovery can enumerate references and derivatives.

## 10. Interfaces

E submits Entity/Relation proposals, mentions, alias evidence, typed predicates/values, time and scope; Manager returns provisional/resolved IDs, ambiguity, or validation errors. E cannot merge identities based on display-name similarity alone.

F requests scoped relation traversal with explicit depth/fan-out/deadline and exact version/as-of semantics. Every edge and target node is scope-filtered and authorized before it can affect ranking, aggregation or result count (INT-P0-02). Truncation is explicit.

G may store Entity/Relation refs as explanatory references, but ContextVersion semantics and change sets remain G-owned (INT-P1-01). H carries typed opaque refs; protocol schema is H-owned. I authorizes merge/split/relation mutation, cross-scope sharing, Forget and retention. E/F/G/H/I must not interpret aliases as stable identity.

## 11. Error Handling

ENTITY_NOT_FOUND_OR_NOT_VISIBLE; AMBIGUOUS_ENTITY; ALIAS_SCOPE_MISMATCH; ENTITY_MERGE_CONFLICT; ENTITY_SPLIT_PARTITION_INCOMPLETE; STALE_ENTITY_VERSION; INVALID_PREDICATE; ENDPOINT_TYPE_MISMATCH; RELATION_SCOPE_MISMATCH; INVALID_VALID_TIME; RELATION_RETRACTED; GRAPH_TRAVERSAL_LIMIT; PERMISSION_DENIED; IDEMPOTENCY_CONFLICT. Errors disclose only authorized metadata.

## 12. Consistency

Entity/Relation canonical records and migration events commit with outbox/change-feed intent. Projection rebuild uses immutable revisions and migration records. Historical refs resolve to original identity/revision; “current canonical identity” resolution may follow redirects only when caller is authorized and explicitly requests current mapping. Relation endpoint refs must resolve to compatible Entity/Memory/Event types at the referenced versions. Merge/split migration is never an implicit mutation of history.

## 13. Security / Scope

All identity resolution and graph traversal begins with resolved ScopeRefs and authorization. Cross-scope identity equivalence requires explicit grant and source-owner approval. Evidence access is separate. Scope filters precede candidate generation and graph expansion; each edge and destination is rechecked. Do not leak protected entity existence via alias match counts, ambiguity messages, graph degree, ranking, or error detail. Environment identity is mandatory for environment-dependent Entities/Relations.

## 14. Performance Considerations

Bound relation fan-out, depth, page size, and time budget. Provide cursor and explicit partial/truncated state. Batch endpoint validation and authorization while preserving per-edge checks. Measure alias collision rates, resolution ambiguity, merge/split migration size, relation traversal cost, temporal filtering and projection rebuild time. Never optimize by merging uncertain identities.

## 15. Observability

Track resolution decisions and ambiguity rate, merge/split counts, redirected-reference count, unresolved historical refs, relation revision conflicts, graph projection lag, traversal truncation and scope denials. Carry actor, scope, correlation/causation, operation, object/revision IDs and timestamps; redact alias/source payload where needed.

## 16. Failure Scenarios

- Alias collision: return ambiguity; do not merge.
- Cross-scope candidate match: exclude unless explicit sharing grant authorizes the operation.
- Merge commit succeeds but projection migration fails: canonical merge record is authoritative; replay migration.
- Split has unresolved historical mentions: preserve unresolved mapping; do not guess.
- Relation endpoint becomes unavailable after Forget: retain only policy-permitted tombstone/reference state and mark graph edge unavailable.
- Traversal limit reached: return partial result with truncation marker, not false completeness.
- Vocabulary version unknown: reject unsafe interpretation or preserve opaque extension only where compatibility policy explicitly permits.

## 17. Dependencies

Domain Model B for type/temporal semantics; Canonical Store for immutable revisions and outbox; E for mentions/proposals/evidence; F for graph retrieval; G for pinned refs; H for ActorRef and wire refs; I for scope grants, permission, Forget and retention; vocabulary registry for predicate compatibility.

## 18. Open Questions

- OPEN: Generic Scope parent/child and multi-owner algebra (DM-005).
- OPEN: ActorRef issuer/delegation and workload identity (INT-P1-03).
- OPEN: vocabulary registry, extension and deprecation rules (DM-013).
- OPEN: merge/split policy for historical Claim references after Claim ADR (DM-009).
- OPEN: whether inverse relation records are ever required beyond derived traversal.
- OPEN: DAG/cycle rule for provenance links crossing relation/entity derivations (DM-007).
- TO_VALIDATE: relation fan-out/depth and merge/split migration benchmarks.
