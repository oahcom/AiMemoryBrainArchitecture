# Domain Model — Architecture Guide

- Document ID: DOC-DOM-001
- Version: 1.0
- Source specifications: 02-domain-model/
- Owner: B — Domain Model
- Chinese counterpart: [领域模型架构指南](../../zh-CN/02-domain-model/domain-model-guide.md)
- Status: Explanatory guide; source contracts and unresolved ADRs remain authoritative

## 1. Why the Domain Model exists

The Domain Model gives every subsystem a shared definition of the things the Brain stores and the relationships among them. Without it, the Compiler, Store, Runtime, Context Manager, and Governance layer could use the same word to mean different things—or make incompatible assumptions about identity, time, evidence, and ownership.

It defines meaning and constraints. It does not prescribe SQL tables, wire encoding, extraction algorithms, deployment topology, or a particular graph/index engine.

## 2. The core idea

**An Event is something captured. A Memory is a retained knowledge asset. A Claim is a proposition represented by that asset. Evidence is what supports, refutes, or qualifies a Claim.**

These are not interchangeable:
- An Event may be incomplete, mistaken, planned, predicted, or merely reported.
- A Memory is retained and addressable; it is not automatically true.
- A Claim carries epistemic and temporal qualifications.
- Evidence is source material or an observation, not a confidence score.
- Provenance records where an asset came from and how it was derived.

## 3. Conceptual object map

~~~mermaid
erDiagram
  EVENT ||--o{ EVIDENCE : supplies
  MEMORY ||--|{ MEMORY_VERSION : versions
  MEMORY_VERSION ||--o{ CLAIM : contains
  CLAIM }o--o{ ENTITY : concerns
  CLAIM }o--o{ EVIDENCE : supported_by
  CLAIM }o--o{ RELATION : qualified_by
  EVIDENCE }o--|| PROVENANCE : traces
  MEMORY_VERSION }o--o{ MEMORY_SOURCE : derived_from
  MEMORY_CONTEXT ||--o{ CONTEXT_ENTRY : contains
  CONTEXT_ENTRY }o--|| MEMORY_VERSION : references
  AGENT_SCOPE ||--o{ MEMORY : bounds
  ENVIRONMENT_SCOPE ||--o{ EVENT : qualifies
~~~

This is a conceptual map, not a physical schema. Where a relationship has its own role, time, scope, or evidence, it may require an explicit association record. A Context Entry references a canonical version or governed rendering; it is not another Canonical Memory.

## 4. The main objects

| Object | What it means | Main authority |
|---|---|---|
| Event | Captured occurrence, observation, report, or transition | Event Ingestion |
| Memory | Retained, addressable knowledge asset | Canonical Memory authority |
| Claim | Proposition about an entity, event, or state | Domain semantics; stored in canonical versions |
| Entity | Identity-bearing referent, not just a name or mention | Entity & Relationship Manager |
| Relation | Typed association with endpoints, scope, and optional valid time | Entity & Relationship Manager |
| Evidence | Source material/observation that supports, refutes, or qualifies a Claim | Evidence & Provenance Manager |
| Provenance | Origin and derivation lineage | Evidence & Provenance Manager |
| Memory Version | Immutable historical snapshot | Canonical Store/versioning authority |
| Memory Source | Typed link from a derived asset to its input | Evidence & Provenance Manager |
| Memory Context | Scoped, versioned selection for a task | Memory Context Manager |
| Context Entry | One reference/presentation inside a Context | Memory Context Manager |
| Agent Scope | Namespace for Agent-owned memory | Governance |
| Environment Scope | Namespace for a world, tenant, project environment, save, or simulation | Governance |

## 5. Identity, versions, and time

- IDs are opaque and non-semantic. UUIDv7 is a candidate, not a mandated identifier algorithm.
- A Memory keeps a stable memory_id across immutable versions.
- A new version is a successor; it does not edit historical content in place.
- Competing updates use expected-version/CAS or equivalent concurrency control. A stale write must be rejected or explicitly reconciled.
- event_time, recorded_at, and valid_time answer different questions and must not be conflated.
- Unknown values remain explicitly unknown; the system must not fabricate a timestamp, source, or identity.

## 6. Epistemic status is not lifecycle

A Claim's epistemic status describes the basis and standing of the proposition:

| Status | Meaning |
|---|---|
| Observed | Directly captured observation |
| Reported | A source asserted it; independent verification has not occurred |
| Inferred | Derived through a declared method from premises |
| Verified | Passed a declared verification procedure or authoritative attestation |
| Disputed | Materially incompatible positions remain unresolved |
| Retracted | Withdrawn by an authorized source/process or invalidated |

Memory lifecycle describes the management stage:

| State | Meaning |
|---|---|
| Candidate | Awaiting validation/consolidation/policy decision |
| Consolidated | Passed structural consolidation checks |
| Active | Eligible for normal retrieval, subject to scope and policy |
| Superseded | Replaced for current use but retained as history |
| Archived | Retained but inactive under current policy |
| Forgotten | Governed Forget committed; access denied and deletion/de-identification tracked |

These dimensions are independent. An Active Memory can contain a Disputed Claim; an Archived Memory can contain a Verified Claim.

## 7. Scope is not Permission

Scope answers **where the asset belongs and applies**. Permission answers **who may perform which operation**.

An object can carry multiple typed scope references, but combining scopes must never silently broaden access. A matching Agent identity does not authorize access across different Environment Scopes. Evidence access may be stricter than access to a derived Memory. Permission must be checked at each relevant boundary, including asynchronous execution.

## 8. Relationships, Evidence, and Provenance

A Relation is a typed association, not text co-occurrence or embedding similarity. Its definition controls allowed endpoint types, directionality, qualifiers, temporal semantics, scope compatibility, and uniqueness.

Evidence may support, refute, or qualify a Claim. One Evidence item may be linked to multiple Claims; one Claim may have multiple Evidence items. Copies of the same source do not count as independent corroboration.

Provenance records source versions, source portions, transformations, method/component versions, derivation time, input digests, parent lineage, and any unavailable/redacted reason. A method reference explains how something was produced; it does not prove that the result is correct.

## 9. How a memory is formed

~~~text
Occurrence / report / document / observation
        ↓
Event and source registration
        ↓
Evidence and provenance
        ↓
Candidate Memory and Claim proposals
        ↓
Entity and Relation resolution
        ↓
Epistemic, temporal, and Scope qualification
        ↓
Lifecycle policy evaluation
        ↓
Canonical Memory Version
        ↓
Retrieval and optional Context reference
~~~

The Compiler proposes and transforms. It cannot bypass canonical lifecycle policy. Schema validity is not proof of truth. A planned or predicted item must not be promoted to a completed outcome without outcome evidence.

## 10. Domain invariants to preserve

1. Event is not Memory; Evidence is not Claim.
2. Claim is a proposition, not its source.
3. Memory identity remains stable across immutable versions.
4. Unknown time is not interpreted as “always”.
5. Derived assets link to sources or explicitly state why provenance is unavailable.
6. Intent, plan, prediction, and pending action are not completed outcomes without evidence.
7. Relations are typed; co-occurrence is not a Relation.
8. Scope is not Permission.
9. Context Entry does not own or mutate Canonical Memory.
10. Context Remove is not Forget.
11. Conflicting Claims retain evidence and resolution history.
12. Confidence, Trust, Relevance, and Evidence Strength are distinct.

## 11. Important unresolved decision: Fact / Claim

The current cross-module integration record continues to identify the Fact/Claim ADR as **ADR-BLOCKED**. Some earlier domain text describes Claim as the canonical proposition object and treats “Fact” as a qualified interpretation, but that wording must not be used to freeze downstream schemas while the governance decision remains blocked.

Until the authorized ADR is approved:
- Preserve the current source wording as a documented proposal/legacy baseline, not as a newly approved cross-system contract.
- Do not introduce or remove a separate Fact object based only on translation.
- Keep dependent schema and interface decisions OPEN/BLOCKED.
- Update both language guides and affected specifications when the formal decision is recorded.

## 12. Detailed source specifications

This guide is the readable entry point, not a replacement for detailed contracts:
- [Domain Model Overview](../../../02-domain-model/domain-model-overview.md)
- [Core Domain Entities](../../../02-domain-model/core-entities.md)
- [Epistemic and Temporal Semantics](../../../02-domain-model/epistemic-and-temporal-semantics.md)
- [Memory Lifecycle Model](../../../02-domain-model/lifecycle-model.md)
- [Relationships and Provenance](../../../02-domain-model/relationships-and-provenance.md)
- [Scope and Permission Model](../../../02-domain-model/scope-and-permission-model.md)

Detailed source specifications remain the implementation reference. This guide does not claim that every field-level contract has already been translated.
