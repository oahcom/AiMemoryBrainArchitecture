# Entity and Relationship Manager

- Document ID: D-ENTITY-RELATION-001
- Version: 1.0
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: DEREFERENCED — historical source blob `14697658d4d873381ca8d4e3bed7c1170368ec29` retained; no current normative source path exists.
- Source branch head audited: 6b654d5cffaeb71b01f2b0750daa0abc14eb64b3
- Source: DEREFERENCED — original normative path `03-memory-brain/entity-and-relationship-manager.md` is absent from the current main tree; alternative: [surviving Chinese counterpart](../../zh-CN/03-memory-brain/entity-and-relationship-manager.md) (blob `3bb770efe2decf1b7178281ef8a63c584e3a0d7f`; translation only, not an authoritative substitute).
- Chinese counterpart: [Entity 与 Relationship Manager](../../zh-CN/03-memory-brain/entity-and-relationship-manager.md)
- Status: Identity and typed temporal relationship principles DECIDED; merge/split and vocabulary details CANDIDATE/OPEN
- Related: INT-P0-02/03, INT-P1-02/03/06; DM-005/006/007/009/010/013

## 1. Purpose and scope

Manage identity-bearing Entities and typed, evidence-qualified Relations without conflating identity with names, mentions, co-occurrence or graph projections. Preserve historical identity decisions and reference migration across merge/split.

Owns Entity identity/versions, alias/mention links, resolution decisions, merge/split records, Relation identity/revisions, typed predicates/values, direction, validity, evidence, scope constraints and canonical graph-reference consistency. Does not own retrieval ranking, global policy, Event ingestion or physical deletion.

## 2. Responsibilities and non-responsibilities

- Allocate stable opaque Entity IDs independent of display labels.
- Resolve references using evidence and scope; return ambiguity rather than guess.
- Maintain versioned attributes/aliases with provenance and validity.
- Enforce typed Relation endpoints, direction, temporal validity, evidence and scope.
- Record Entity merge/split and Relation migration as immutable operations.
- Expose bounded authorized graph traversal and historical queries.
- Ensure Forget dependency discovery can find Entity/Relation references and derived projections.

No name-only identity inference, unrestricted cross-scope resolution, truth adjudication, relation ranking, vector-similarity policy, Agent planning or permission granting. A display name is a label, not an identity key.

## 3. Domain objects

- **EntityIdentity:** entity_id, owner_scope_ref, applicability_scope_refs, entity_kind, created_at, created_by_actor_ref, identity_status. Stable, never reused.
- **EntityVersion:** entity_version_id, entity_id, sequence, parent_version_id, canonical_attributes, attribute_validity, content_digest, alias_refs, provenance_refs, actor_ref, recorded_at, schema_version. Immutable descriptive revision.
- **Alias:** alias_id, entity_id, normalized_label, language/locale, alias_kind, valid_time, source/evidence refs, scope refs, confidence/method metadata. Scoped, time-qualified label; never identity.
- **MentionRef:** source object/version, locator, surface form, candidate entity refs and resolution status. Mention is not automatically an Entity.
- **EntityResolutionDecision:** decision_id, mention_ref, candidate_entity_refs, selected_entity_ref or unresolved, evidence_refs, method_ref, actor_ref, scope_refs, recorded_at, status. Ambiguity remains explicit.
- **EntityMergeRecord:** merge_id, source_entity_ids, survivor_entity_id, source versions, evidence refs, relation migration refs, scopes, actor, reason, commit sequence, timestamp, correction/supersession ref. Explicit redirect map preserves historical lookups.
- **EntitySplitRecord:** split_id, source_entity_id, new_entity_ids, partition criteria, affected mention/claim/relation refs, evidence, scopes, actor, reason, commit sequence, timestamp, correction ref. Records reference partitioning without rewriting history.
- **RelationIdentity:** relation_id, canonical subject TypedObjectRef, typed predicate, canonical object TypedValue/TypedObjectRef, direction, owner/applicability scopes, created metadata.
- **RelationRevision:** relation_revision_id, relation_id, sequence, parent_revision_id, validity interval, epistemic status, lifecycle state, evidence/provenance refs, confidence assessment ref, author ActorRef, reason, recorded_at, schema version, digest. Immutable.
- **RelationMigrationRecord:** migration_id, operation kind, old/new relation refs, affected Entity refs, evidence, scope, actor, reason, sequence and timestamp.

## 4. Typed data model

TypedPredicate includes vocabulary namespace, predicate code/version, arity, endpoint type constraints, symmetry/inverse declaration, temporal behavior and deprecation metadata. TypedValue includes value kind, canonical encoding, optional unit/locale, schema/vocabulary version and explicit unknown/null semantics. Free-form predicates are never silently treated as canonical vocabulary.

TypedObjectRef = object_type + opaque object_id + optional immutable version/revision ID + optional scope_ref + reference purpose. ScopeRef = scope_id + registered scope_kind + owner_ref + optional parent_scope_id + status/version. ActorRef = actor_kind + stable subject ID + issuer/authentication ref + optional delegation chain; display_name is descriptive only. TimeValue = normalized bounds, precision, timezone, certainty, source phrase and source ref. TimeInterval = start/end TimeValue, boundary convention and explicit unbounded/unknown markers. ContentRef = content_id, media/content kind, immutable version/digest, locator/access class, availability state and source identity. These are minimum candidate structures; H/I finalize identity/auth fields.

Relation direction is explicit. Directed predicate subject/object positions are normative. Symmetric relations declare symmetry in vocabulary; inverse traversal may be derived. **CANDIDATE default:** persist one canonical directed edge and derive inverse traversal; do not duplicate inverse records unless audit/domain semantics require it.

## 5. State machines

Entity identity: Provisional → Resolved → Merged or Split; Resolved may become Retired under explicit policy. Merged/Split identities remain addressable as historical identities with redirect/partition metadata; IDs are never reused.

Relation lifecycle: Proposed → Active → Superseded or Retracted. A new revision supersedes the prior revision without mutation. Retraction preserves history and reason. Valid Time is independent of record lifecycle; an Active relation can have a bounded validity interval.

## 6. Operations

CreateEntity; AddAlias; ResolveMention; UpdateEntityVersion(expected_version); MergeEntities; SplitEntity; CreateRelation; ReviseRelation(expected_revision); RetractRelation; SupersedeRelation; TraverseRelations(scope, depth, fanout, as_of); ResolveHistoricalReference; RebuildGraphProjection.

**Merge workflow:** authorize source/survivor scopes; verify same permitted ownership domain or explicit sharing; assess identity evidence; create immutable merge record and survivor version; create redirects; migrate current refs through explicit mapping; retain historical refs unchanged; emit change events for F/G and projection rebuild. Matching names alone never authorize cross-user/project/environment merge.

**Split workflow:** authorize; define evidence-backed partition; create new Entity identities; explicitly assign affected current refs; record unresolved/ambiguous refs; preserve old historical versions and source Entity identity; emit migration and downstream reconciliation event. Do not automatically split every old historical reference.

## 7. Invariants

- Entity ID is opaque, stable and never reused.
- Alias/display name/mention never establishes identity alone.
- Resolution is scope-bounded; no implicit cross-user/project/Agent/environment merge.
- Every Entity/Relation has explicit ownership/applicability ScopeRefs.
- Every Relation has typed predicate, direction, endpoint types, lifecycle and validity semantics.
- Evidence/Provenance are independently referenced and authorized.
- Merge/split are append-only, auditable, scope-checked and historically reversible only by a new correction record, not destructive rollback.
- Graph projections are rebuildable; canonical Relation revisions are authoritative.
- Forget dependency discovery can enumerate references and derivatives.

## 8. Interfaces

E submits Entity/Relation proposals, mentions, alias evidence, typed predicates/values, time and scope; Manager returns provisional/resolved IDs, ambiguity or validation errors. E cannot merge identities from display-name similarity alone.

F requests scoped Relation traversal with explicit depth/fanout/deadline and exact version/as-of semantics. Every edge and target node is scope-filtered and authorized before ranking, aggregation or result count (INT-P0-02). Truncation is explicit.

G may store Entity/Relation refs as explanatory references, but ContextVersion/ChangeSet remain G-owned (INT-P1-01). H carries typed opaque refs and owns protocol schema. I authorizes merge/split, relation mutation, cross-scope sharing, Forget and retention. E/F/G/H/I must not interpret aliases as stable identity.

## 9. Errors

ENTITY_NOT_FOUND_OR_NOT_VISIBLE; AMBIGUOUS_ENTITY; ALIAS_SCOPE_MISMATCH; ENTITY_MERGE_CONFLICT; ENTITY_SPLIT_PARTITION_INCOMPLETE; STALE_ENTITY_VERSION; INVALID_PREDICATE; ENDPOINT_TYPE_MISMATCH; RELATION_SCOPE_MISMATCH; INVALID_VALID_TIME; RELATION_RETRACTED; GRAPH_TRAVERSAL_LIMIT; PERMISSION_DENIED; IDEMPOTENCY_CONFLICT. Errors disclose only authorized metadata.

## 10. Consistency

Entity/Relation canonical records and migration events commit with outbox/change-feed intent. Projection rebuild uses immutable revisions and migration records. Historical refs resolve to original identity/revision; “current canonical identity” may follow redirects only when caller is authorized and explicitly requests current mapping. Relation endpoints resolve to compatible Entity/Memory/Event types at referenced versions. Merge/split migration never implicitly mutates history.

## 11. Security / Scope

Identity resolution and graph traversal begin with resolved ScopeRefs and authorization. Cross-scope identity equivalence requires explicit grant and source-owner approval. Evidence access is separate. Scope filters precede candidate generation/graph expansion; each edge and destination is rechecked. Do not leak protected entity existence via alias match counts, ambiguity messages, graph degree, ranking or error detail. Environment identity is mandatory for environment-dependent Entities/Relations.

## 12. Performance and observability

Bound relation fanout, depth, page size and time budget. Provide cursor and explicit partial/truncated state. Batch endpoint validation/authorization while preserving per-edge checks. Measure alias collision, resolution ambiguity, merge/split migration size, relation traversal, temporal filtering and projection rebuild.

Track resolution decisions/ambiguity, merge/split counts, redirected-reference count, unresolved historical refs, relation revision conflicts, graph projection lag, traversal truncation and scope denials. Carry actor, scope, correlation/causation, operation, object/revision IDs and timestamps; redact alias/source payload where needed.

## 13. Failure scenarios

- Alias collision: return ambiguity; do not merge.
- Cross-scope candidate match: exclude unless explicit sharing grant authorizes it.
- Merge commit succeeds but projection migration fails: canonical merge record is authoritative; replay migration.
- Split has unresolved historical mentions: preserve unresolved mapping; do not guess.
- Relation endpoint becomes unavailable after Forget: retain only policy-permitted tombstone/reference state and mark graph edge unavailable.
- Traversal limit reached: return partial result with truncation marker, not false completeness.
- Unknown vocabulary version: reject unsafe interpretation or preserve opaque extension only where compatibility policy explicitly permits.

## 14. Dependencies and open questions

Dependencies: B type/temporal semantics; Canonical Store immutable revisions/outbox; E mentions/proposals/evidence; F graph retrieval; G pinned refs; H ActorRef/wire refs; I scope grants/permission/Forget/retention; vocabulary registry.

- OPEN: generic Scope parent/child and multi-owner algebra (DM-005).
- OPEN: ActorRef issuer/delegation and workload identity (INT-P1-03).
- OPEN: vocabulary registry, extension/deprecation rules (DM-013).
- OPEN: merge/split policy for historical Claim refs after Claim ADR (DM-009).
- OPEN: whether inverse Relation records are needed beyond derived traversal.
- OPEN: DAG/cycle rule for provenance links across relation/entity derivations (DM-007).
- TO_VALIDATE: relation fanout/depth and merge/split migration benchmarks.

## Phase 3 remediation — historical-safe Merge/Split and Relation migration

**DECIDED at D domain-contract level:** Entity IDs, EntityVersion IDs, Relation IDs and RelationRevision IDs are immutable and never reused. Merge/Split never rewrites historical object payloads, old MemoryVersions, Claim/Evidence/Provenance refs or prior RelationRevisions. It appends immutable migration records and emits canonical change/outbox events.

### Entity Merge

EntityMergeRecord MUST include operation ID, ordered source Entity IDs and exact source EntityVersion refs, survivor Entity ID and exact survivor version before/after, evidence/provenance refs, scope refs, actor ref, reason, canonical commit cursor, redirect mapping, affected current-reference inventory digest, RelationMigrationRecord refs and correction/supersession pointer. Source identities remain resolvable as historical identities. Historical lookup returns original ID/version; only explicitly authorized “resolve current identity” may follow redirect. Redirect traversal is cycle-checked and bounded.

Merge is not destructive alias rewrite. Current refs migrate only through explicit per-reference mapping committed with merge. Ambiguous refs remain unresolved. Relation edges are not deduplicated merely because endpoints redirect to same survivor; semantic equivalence, scope, validity and evidence must be evaluated and recorded.

### Entity Split

EntitySplitRecord MUST include source Entity ID/version, new Entity IDs/genesis versions, evidence-backed partition criteria, exact affected current-reference set, per-reference destination mapping or explicit unresolved outcome, affected relation migration refs, actor/scope/reason, canonical commit cursor and correction pointer. Source Entity and historical versions remain addressable. Split partitions current refs only where evidence is sufficient; ambiguous refs remain attached to historical source or unresolved per explicit mapping. No automatic rewrite of historical refs.

### Relation migration

RelationMigrationRecord maps exact old RelationRevision (including endpoint refs) to zero/one/multiple successor Relation IDs/Revisions, or explicit retired/unresolved outcome. Each successor is a new immutable revision (or new Relation identity when predicate/endpoint semantics materially change), with new subject/object refs, evidence/provenance, validity, scope and reason. Old revision remains historically queryable. Migration commits atomically with canonical migration record/outbox; projection failure is repaired by replay, not history mutation.

For merge, an edge whose endpoint redirects may get a successor revision with survivor endpoint only after scope/predicate constraints are revalidated. For split, an edge is assigned to a successor only when endpoint partition evidence identifies the correct new Entity; otherwise mark unresolved/retired for current traversal while retaining old revision for authorized history. Symmetric/inverse traversal remains vocabulary-derived; migration does not create duplicate inverse records by default.

### Query semantics and audit

- Historical query returns exact originally stored Entity/Relation identity and revision; never silently follows redirects.
- Current-identity query may follow authorized redirect/partition map and returns migration chain and mapping confidence/status.
- Graph traversal uses current successor revisions only; stale projections are invalidated/rebuilt from canonical migration records and cannot resurrect retired edges.
- Forget dependency discovery includes original/successor identities, migration records and all current/historical refs subject to I retention policy; redirect is not deletion.

### Acceptance cases

1. Merge then historical lookup returns original source IDs/revisions; current lookup follows recorded redirect with audit chain.
2. Split after merge creates new IDs and explicit correction chain; does not rewrite prior merge or old refs.
3. Ambiguous split refs remain unresolved; no guessed assignment.
4. Relation endpoint migration creates new revision/record; prior edge remains historically intact.
5. Projection rebuild after merge/split yields same current graph and preserves historical lookup.
6. Cross-scope merge/split fails closed without I-authorized grant evidence.
