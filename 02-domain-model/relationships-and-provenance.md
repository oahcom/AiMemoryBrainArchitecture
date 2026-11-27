---
document_metadata:
  domain: domain-model
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
        - "14-ai-development/work-items/AID-2026-200/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a normative root that carried no front-matter: records domain, role and the status the document states in its own body (Status: Core semantics DECIDED). Claims no canonical authority (canonical_status stays Non-Canonical) and records no Owner approval. Pre-metadata content blob: a674e21756cdbf8c07683083bfdcb58a33f48a20."
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
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: null
    en: "docs/en/02-domain-model/relationships-and-provenance.md"
    zh-CN: "docs/zh-CN/02-domain-model/relationships-and-provenance.md"
---
# Relationships and Provenance Model

**Status:** Core semantics DECIDED; graph representation and lineage compaction CANDIDATE/OPEN.  
**Owner:** Memory Domain Model, with Evidence & Provenance and Entity/Relationship Managers executing the contracts.

## 1. Purpose and boundaries

This specification defines typed associations and explains where retained assertions came from. It enables inspection, challenge, re-derivation, correction, and governance without confusing source material with derived interpretation.

Domain Model owns semantics, cardinalities, and invariants. Entity & Relationship Manager resolves identity and maintains relation consistency. Evidence & Provenance Manager captures locators and lineage. Compiler proposes links; Canonical Store persists immutable versions; Governance controls visibility and Forget propagation.

Not owned: entity resolution algorithms, graph engine choice, trust scoring, extraction models, ranking, or physical deletion.

## 2. Relation model

A Relation is a typed edge between typed domain references. It is not textual co-occurrence, embedding similarity, or an unqualified link.

Required semantics:
- relation_type: controlled, versioned vocabulary.
- subject_ref/object_ref: typed references validated against relation definition.
- directionality: directed, symmetric, or inverse-paired.
- qualifiers: structured role, modality, environment, and source metadata.
- valid_time: optional interval during which relation holds.
- epistemic_status: how the relation is known.
- evidence_refs: support/refute/qualify references.
- scope_refs: applicability and visibility.
- lifecycle_state: proposed, active, superseded, retracted.

Each vocabulary entry defines stable type ID/version, allowed endpoint types, inverse/symmetry semantics, self-edge policy, uniqueness constraints, required qualifiers, temporal semantics, and scope compatibility.

**DECIDED:** Relations may be temporal. Missing interval does not mean timeless. Inverse edges must follow canonical relation definition.

**CANDIDATE:** Store one canonical directed edge and derive inverse traversal at query time unless explicit inverse records are required for audit/domain semantics.

## 3. Relation cardinality and lifecycle

Relations are generally many-to-many. Uniqueness depends on relation type, scope, and overlapping validity. Endpoints may be Entity, Claim, Event, Memory, or other declared object types.

- proposed: extracted/supplied but not accepted as active canonical relation.
- active: accepted within declared scope and valid time.
- superseded: replaced by successor; old relation remains historical.
- retracted: withdrawn with reason and authority; evidence/history remains.

Updates create immutable revisions or successor edges. Overlapping changes require explicit conflict handling.

## 4. Evidence model

Evidence is source material or observation used to support, refute, or qualify a Claim/Relation. It has:
- stable evidence_id and evidence_kind;
- typed source_ref;
- optional locator (message ID/span, document page, JSON path, media time range, environment tick/frame, tool-result path);
- optional retained excerpt/content reference;
- observed_at and recorded_at;
- collector identity and optional integrity digest;
- evidential_role: supports, refutes, qualifies, context_only;
- scope references and availability state.

One Evidence can support multiple Claims; one Claim can have multiple Evidence items. This is many-to-many. Where role/strength differs by Claim, use an explicit assessment/link record.

**DECIDED:** Evidence is not a truth score. A locator to mutable external URL is not guaranteed durable evidence. If source retention is prohibited or source unavailable, preserve permitted metadata and mark availability accurately.

## 5. Provenance model

Provenance is traceable origin and derivation history of a Memory, Memory Version, Claim, Relation, or Evidence. It answers:
- Which source inputs and exact versions contributed?
- Which source portions were used?
- What transformation/inference was performed?
- Which component/method/model/rule version performed it?
- When was it derived?
- Which prior derived artifacts were inputs?
- What is unavailable or redacted, and why?

~~~mermaid
flowchart TD
 E1[Source Event / Document / User Input] --> EV[Evidence + Locator]
 EV --> P1[Provenance: direct capture]
 P1 --> C1[Candidate Claim]
 C1 --> P2[Provenance: extraction / normalization]
 E2[Additional Event / Evidence] --> P2
 P2 --> M1[Memory Version 1]
 M1 --> P3[Provenance: consolidation]
 M2[Related Memory Version] --> P3
 P3 --> M3[Memory Version 2]
 M3 --> CE[Context Entry reference]
~~~

Context Entry is a presentation/reference, not a new canonical derivation. If compaction rewrites presentation text, it links to exact canonical version and lineage used.

### Memory Source
A typed provenance edge with memory_source_id, typed source_ref (versioned where possible), source_role (primary, supporting, contradicting, context), optional locator, scope, and creation time.

### Derivation record
Provenance includes target_ref, source edges, derivation_kind, method/component version, derived_at, input digests, parent provenance refs, and unavailable_reason where incomplete. Kinds include direct_capture, extraction, normalization, summarization, consolidation, inference, human_correction, verification, and migration. Method identity describes process; it is not proof of correctness.

## 5A. Claim/Fact lineage and references

ClaimRevision is the exact immutable assertion state referenced by downstream governed objects.

FactRevision MUST reference exact ClaimRevisionRef values and the relevant EvidenceRef and ProvenanceRef values.

A relationship between FactRevision and ClaimRevision is an explicit governed reference, not an implicit current-head relationship.

Forget dependency discovery MUST traverse these references and their registered derivatives.

Historical lineage does not grant authorization to read forgotten content.

## 6. Evidence strength and independence

Evidence strength is assessed relative to a Claim and role. It may depend on directness, integrity, temporal proximity, corroboration, contradiction, and source independence. It is distinct from source Trust and Claim Confidence.

Copies of one source are not independent corroboration. Provenance exposes common ancestry; duplicate derivatives must not inflate support.

**TO_VALIDATE:** evidence-strength rubric and independence assessment. No numeric formula is normative.

## 7. Input/output contracts and workflow

Inputs: typed relation proposals, source objects/locators, claim-evidence links, derivation metadata, scopes, actor/method identity.

Outputs: validated typed edges, provenance nodes, lineage traversal, integrity/unavailability states, structured errors.

Workflow:
1. Resolve source identity and version.
2. Validate source access scope.
3. Create Evidence reference and locator without changing source.
4. Attach Evidence to Claim/Relation with explicit role.
5. Record derivation method and input digests.
6. Commit candidate/canonical object with provenance edges.
7. Publish change event for index/reconciliation.
8. For every transformation, add lineage; never rewrite prior provenance.

## 8. Consistency, concurrency, recovery

Provenance edges commit atomically with target version or through transactional outbox. A target cannot be marked successfully derived while required lineage is missing. If an external source cannot be fetched during replay, keep source reference and mark unavailable; do not fabricate excerpt content.

Concurrent relation edits use expected version/parent. Stale writes reject. Entity merge/split and Relation merge/split create explicit migration records. Projections are rebuildable from canonical records and provenance events.

## 9. Forget and retention

Forget may remove/de-identify source payloads, excerpts, provenance metadata, derived Memories, Relations, indexes, caches, contexts, and backups. The graph supports dependency discovery but must not preserve forbidden personal content merely to prove deletion.

**DECIDED:** lineage metadata and deletion audit metadata are governed separately from source content. Where erasure is required, retain only permissible tombstone metadata that cannot reconstruct forgotten content.

## 10. Security, performance, acceptance

Access to Memory does not automatically grant access to Evidence source. Each source edge is independently authorized. Cross-scope lineage requires explicit sharing. Locators can expose private message IDs, paths, or environment coordinates and are protected. Evidence text is untrusted data, never instruction authority.

Measure lineage traversal latency by depth/fan-out, relation lookup by type/scope, locator resolution, duplicate ancestry, and Forget dependency completeness.

Acceptance:
- Every derived Memory/Claim traces to sources or states why unavailable.
- Evidence can support/refute distinct claims unambiguously.
- Relation endpoint/type validation is enforced.
- Relation time and scope are preserved.
- Common ancestry prevents copied sources counting as independent.
- Multi-generation consolidation remains traceable.
- Source unavailability is explicit.
- Unauthorized lineage/source references are not disclosed.
- Forget dependency discovery reaches registered derivatives/projections.

## 11. Open decisions and interfaces

- **OPEN:** relation vocabulary governance and extension compatibility.
- **CANDIDATE:** canonical edge with derived inverse traversal.
- **OPEN:** provenance DAG requirement versus limited cycles.
- **TO_VALIDATE:** evidence rubric and lineage compaction threshold.
- Entity Manager confirms merge/split reference migration.
- Compiler emits source version/locator and method/input digest.
- Store guarantees target-version and provenance visibility.
- Governance defines deletion/tombstone limits.
