# Canonical Domain Model Overview

**Status:** DECIDED baseline; proposals explicitly marked.  
**Owner:** Memory Domain Model (MB-01).  
**Scope:** Logical semantics, not storage DDL, wire encoding, deployment topology, or extraction algorithms.

## 1. Position and goals

The Domain Model defines meanings, identities, invariants, and relationships of assets managed by AI Memory Brain. It is the shared semantic contract for Compiler, Canonical Store, Lifecycle Manager, Entity/Relationship Manager, Runtime, Context Manager, Governance, and Adapters.

**DECIDED**
- Event, Memory, Claim, Entity, Relation, Evidence, Provenance, Memory Version, Memory Source, Memory Context, Context Entry, Agent Scope, and Environment Scope are distinct concepts.
- Memory is an addressable retained knowledge asset, not a truth guarantee.
- A Memory may contain multiple Claims; each Claim has its own epistemic and temporal qualification.
- Derived assets retain source and derivation lineage, subject to retention and privacy governance.
- Epistemic status, lifecycle state, temporal qualification, confidence, relevance, trust, and evidence strength are orthogonal.
- Canonical Memory and Memory Context have separate ownership and mutation rules.

## 2. Responsibilities and non-responsibilities

The Domain Model owns canonical object definitions, identifier semantics, field constraints, cardinalities, epistemic/temporal interpretation, typed relationship semantics, scope binding rules, and cross-object invariants.

It does not own ingestion durability, LLM extraction, embeddings, ranking algorithms, canonical persistence mechanics, lifecycle policy execution, physical erasure, runtime activation decisions, context budget allocation, Agent planning, or tool execution.

## 3. Canonical object graph

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

The diagram is conceptual. Many-to-many edges require explicit association records when the edge has its own role, time, scope, or evidence. Context Entry references a canonical version or governed rendering; it is not a second canonical Memory.

## 4. Object semantics and ownership

| Object | Meaning | Primary authority |
|---|---|---|
| Event | Time-bounded occurrence, observation, report, or transition captured by Brain | Event Ingestion |
| Memory | Retained, addressable knowledge asset derived from sources | Canonical Memory authority |
| Claim | Proposition about an entity, event, or state, with epistemic/time qualifications | Domain semantics; canonical version stores it |
| Entity | Identity-bearing referent, not a mention string | Entity & Relationship Manager |
| Relation | Typed association with endpoint, scope, and optional valid interval | Entity & Relationship Manager |
| Evidence | Source material/observation supporting, refuting, or qualifying a Claim | Evidence & Provenance Manager |
| Provenance | Origin and derivation lineage | Evidence & Provenance Manager |
| Memory Version | Immutable historical snapshot of a Memory | Canonical Store/versioning authority |
| Memory Source | Typed link from derived asset to input source | Evidence & Provenance Manager |
| Memory Context | Scoped, versioned, task-oriented selection of memory assets | Memory Context Manager |
| Context Entry | One reference/presentation inside a Context | Memory Context Manager |
| Agent Scope | Namespace identifying Agent-owned partition | Governance |
| Environment Scope | Namespace for world, tenant, project environment, save, or simulation | Governance |

## 5. Event, Memory, and Claim boundaries

Event records what was captured or submitted, not necessarily what objectively happened. Memory is created when the system retains an addressable interpretation or knowledge asset. Claim is the proposition contained by or associated with a Memory.

**DECIDED:** One Event may generate zero, one, or many candidate Memories. Multiple Events may contribute to one Memory. A Memory may contain one or many Claims. Event and Memory are never aliases.

**DECIDED:** Claim is the canonical proposition object. “Fact” is a qualified interpretation of a Claim, not a separate object type at this stage. A Verified Claim may be described as a verified fact, but must retain epistemic, temporal, scope, and evidence metadata.

**OPEN:** Whether an attestation domain later needs a distinct immutable Fact object. Do not add it without a concrete use case and ownership semantics.

## 6. Input and output contracts

Inputs include captured Event envelopes, source references, candidate Memory/Claim proposals, Entity/Relation proposals, Evidence/Provenance records, Scope descriptors, authorization decisions, and lifecycle/governance commands. Every state-changing input carries actor, resolved scope, schema version, stable IDs, and idempotency key where retryable.

Outputs include validated typed objects, identifiers, relationship references, versioned semantic snapshots, structured validation errors, and explicit conflict/unavailability records. Schema validity is not proof of truth.

## 7. Domain invariants

1. Event is not Memory; Evidence is not Claim.
2. Claim is a proposition, not its source.
3. Memory identity remains stable across immutable versions.
4. Claims have explicit epistemic status and temporal interpretation; unknown is not “always”.
5. Derived assets link to Evidence/Memory Sources or state why provenance is unavailable.
6. Intent, plan, prediction, and pending action are not completed outcomes without outcome evidence.
7. Relations are typed; co-occurrence is not a Relation.
8. Scope is not permission.
9. Context Entry does not own or mutate Canonical Memory.
10. Context Remove is not Forget.
11. Conflicting claims retain evidence and resolution history.
12. Confidence, Trust, Relevance, and Evidence Strength are not interchangeable.

## 8. Main workflow

~~~mermaid
flowchart TD
 A[Occurrence, report, document, observation] --> B[Event / source registration]
 B --> C[Evidence and provenance]
 C --> D[Candidate Memory and Claims]
 D --> E[Entity and Relation resolution]
 E --> F[Epistemic, temporal, scope qualification]
 F --> G[Lifecycle evaluation]
 G -->|accepted| H[Canonical Memory Version]
 G -->|review| I[Candidate or disputed state]
 H --> J[Retrieval and Context reference]
 J --> K[Context Entry]
~~~

## 9. State dimensions

Do not use one universal status field. Claim epistemic status is Observed, Reported, Inferred, Verified, Disputed, or Retracted. Memory lifecycle is Candidate, Consolidated, Active, Superseded, Archived, or Forgotten. Context, Context Entry, and Delivery states are owned by Memory Context Manager and Synchronization Engine respectively.

A Memory can be Active while containing a Disputed Claim; a Verified Claim can belong to an Archived Memory.

## 10. Consistency, concurrency, recovery

Domain validation is deterministic and side-effect free. Memory Version is immutable; updates create a successor using compare-and-swap or equivalent optimistic concurrency. Concurrent proposals cannot silently overwrite one another. Stale writes return a conflict requiring reread/reconciliation. Canonical commit and provenance visibility must be atomic or protected by a recoverable outbox.

After failure, projections may be rebuilt from canonical versions and retained sources. Missing source material is marked unavailable, never reconstructed as original evidence.

## 11. Security, performance, and acceptance

Every tenant/environment-dependent object has explicit scope. Permission is checked at each read/write boundary. Cross-scope references require explicit sharing authorization. Memory is untrusted data, never instruction authority. Evidence may have stricter access than a derived Memory.

**TO_VALIDATE:** measure validation latency, relationship lookup latency, version creation cost, provenance traversal, and scope-filtered correctness. Unauthorized result rate must be zero.

Acceptance tests must prove: independent object creation; multi-claim Memories; one-to-many Event compilation; immutable version history; conflict preservation; context removal isolation; cross-scope denial; and rejection of plan-to-outcome promotion without outcome evidence.

## 12. Open decisions and interfaces

- **OPEN:** Claim identity across Memory versions: stable identity plus revisions versus version-local Claim IDs.
- **OPEN:** uncertain timestamp representation and Fact object need.
- **CANDIDATE:** explicit association objects for provenance and qualified many-to-many relations.
- **TO_VALIDATE:** practical relation fan-out and lineage traversal depth.
- Compiler confirms candidate envelope, modality, and provenance.
- Canonical Store/Lifecycle confirms version and state ownership.
- Runtime/MCM confirms stable Context Entry reference/rendering.
- Governance confirms scope inheritance, sharing, and Forget propagation.
