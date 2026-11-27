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
      last_verification_note: "GOV-DOC-002 classification of a normative root that carried no front-matter: records domain, role and the status the document states in its own body (Status: DECIDED semantics unless marked otherwise). Claims no canonical authority (canonical_status stays Non-Canonical) and records no Owner approval. Pre-metadata content blob: 06a914699813e36d8bfd69e96c46debb3c3e0cf3."
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
    en: "docs/en/02-domain-model/core-entities.md"
    zh-CN: "docs/zh-CN/02-domain-model/core-entities.md"
---
# Core Domain Entities

**Status:** DECIDED semantics unless marked otherwise.  
**Owner:** Memory Domain Model (MB-01).  
**Purpose:** Logical schema and field constraints, not database DDL or wire-format specification.

## 1. Schema conventions

IDs are opaque and non-semantic. **CANDIDATE:** UUIDv7 or another sortable opaque identifier; algorithm is not normative. Timestamps are UTC instants with source precision/timezone retained when relevant. Intervals default to half-open [start, end). Required means required for a valid persisted object. Unknown is explicit; it is not fabricated. Canonical versions are immutable. Enum evolution requires schema/version compatibility.

## 2. Event

An Event is a captured occurrence, observation, report, or state transition.

| Field | Type / nullable | Meaning and constraint |
|---|---|---|
| event_id | OpaqueId, required | Stable unique identity |
| event_kind | String/enum, required | Versioned event vocabulary |
| source_type | Enum, required | user, agent, environment_adapter, external_system, document, system |
| source_id | OpaqueId/String, required | Origin identity; not an auth credential |
| payload_ref | ContentRef, required | Retained payload or declared external source |
| event_time | TimeValue, nullable | When occurrence happened; null if unknown |
| recorded_at | Instant, required | Durable acceptance time, immutable |
| scope_refs | ScopeRef[], required | Resolved scopes |
| environment_scope_id | OpaqueId, nullable | Required if environment-dependent |
| idempotency_key | String, conditionally required | Retryable ingress uniqueness within source/operation |
| classification | Enum, required | observed, reported, planned, predicted, attempted, outcome, administrative, unknown |
| schema_version | String, required | Envelope version |
| retention_class | String, required | Governance policy selector |
| integrity_digest | String, nullable | Payload integrity reference |

Acceptance does not verify truth. Planned/predicted are not outcomes. Same idempotency key with different payload digest is a conflict.

## 3. Memory

| Field | Type / nullable | Meaning and constraint |
|---|---|---|
| memory_id | OpaqueId, required | Stable across versions; never reused |
| memory_kind | String/enum, required | preference, episodic, procedural-description, semantic, environment-state, etc. |
| label | String, nullable | Display label, not identity |
| scope_refs | ScopeRef[], required | Ownership/applicability boundary |
| primary_environment_scope_id | OpaqueId, nullable | Explicit environment anchor where relevant |
| current_version_id | OpaqueId, required after first commit | Current immutable version |
| lifecycle_state | Enum, required | Candidate, Consolidated, Active, Superseded, Archived, Forgotten |
| created_at / updated_at | Instant, required | Canonical creation/current pointer update |
| retention_class | String, required | Retention policy |
| sensitivity | Enum, required | public-within-scope, internal, sensitive, restricted |
| supersedes_memory_id | OpaqueId, nullable | Explicit predecessor |
| forget_operation_id | OpaqueId, nullable | Governance workflow reference |

A Memory may contain multiple Claims. Empty Claim sets require a declared non-propositional memory kind. Lifecycle is not truth status.

## 4. Memory Version

| Field | Type / nullable | Meaning and constraint |
|---|---|---|
| memory_version_id | OpaqueId, required | Immutable version identity |
| memory_id | OpaqueId, required | Parent Memory |
| version_number | PositiveInteger, required | Monotonic per Memory; never reused |
| parent_version_id | OpaqueId, nullable | Null only for initial version |
| created_at | Instant, required | Commit time |
| author_kind / author_ref | Enum + ActorRef, required | compiler, lifecycle_manager, authorized_user, governance, migration |
| change_reason | Enum/string, required | extraction, consolidation, correction, verification, retraction, migration |
| claims | ClaimSnapshot[], required | Immutable claim set |
| entity_refs / relation_refs | OpaqueId[], required | Explicit typed references |
| provenance_refs | OpaqueId[], required | Lineage or explicit unavailable reason |
| content_digest | String, required | Canonical semantic content digest |
| schema_version | String, required | Domain schema version |

No in-place edit. Current pointer advancement and version commit are atomic. Competing writes use expected parent/current version.

## 5. Claim

A Claim is the canonical proposition identity.

A Claim uses a stable ClaimRef and has immutable ClaimRevision records.

A ClaimRevision identifies one exact assertion state and preserves its parent, proposition, epistemic status, valid time, Evidence references, Provenance references and Scope.

Claim identity classification follows DOMAIN-MODEL-001 §2.4.

## 5A. Fact and FactRevision

Fact is an independent governed Attestation object.

FactRevision is immutable and references exact ClaimRevisionRef, Evidence, Provenance, Scope, Attestor, Method/Version and I AuthorizationDecisionRef values.

A Fact is not a Verified Claim alias or an objective-truth flag.

This logical entity definition does not approve DDL or physical Schema.
## 6. Entity

| Field | Type / nullable | Meaning and constraint |
|---|---|---|
| entity_id | OpaqueId, required | Stable, never reused |
| entity_type | String/enum, required | person, organization, project, agent, device, place, artifact, environment, concept |
| canonical_label | String, required | Preferred display label |
| aliases | AliasRecord[], required | Time- and scope-qualified names |
| identity_status | Enum, required | provisional, resolved, merged, split, retired |
| scope_refs | ScopeRef[], required | Namespace |
| external_identifiers | ExternalId[], required | Namespaced identifiers; uniqueness is scoped |
| created_at | Instant, required | Creation time |
| current_version_id | OpaqueId, required | Current identity/profile version |
| merged_into_entity_id | OpaqueId, nullable | Required when merged |
| identity_evidence_refs | OpaqueId[], required | Resolution evidence or provisional reason |

Same label does not prove same identity. Merge/split preserves redirects, history, and auditable reference migration.

## 7. Relation

| Field | Type / nullable | Meaning and constraint |
|---|---|---|
| relation_id | OpaqueId, required | Stable relation identity |
| relation_type | String, required | Controlled typed vocabulary |
| subject_ref / object_ref | TypedObjectRef, required | Typed endpoints |
| directionality | Enum, required | directed, symmetric, inverse-paired |
| qualifiers | TypedMap, required | Role, modality, environment, source |
| valid_time | TimeInterval, nullable | Asserted validity interval |
| epistemic_status | Enum, required | Epistemic vocabulary |
| evidence_refs | OpaqueId[], required | Support/refutation references |
| scope_refs | ScopeRef[], required | Applicability/visibility |
| lifecycle_state | Enum, required | proposed, active, superseded, retracted |
| created_at | Instant, required | Record creation |

Relation type declares allowed endpoint kinds, inverse/symmetry semantics, and uniqueness constraints. Co-occurrence is not a Relation.

## 8. Evidence

| Field | Type / nullable | Meaning and constraint |
|---|---|---|
| evidence_id | OpaqueId, required | Stable identity |
| evidence_kind | Enum, required | source_span, user_statement, document, observation, tool_result, attestation, derived_excerpt |
| source_ref | TypedObjectRef, required | Event/document/external source |
| locator | Locator, nullable | Message span, page, JSON path, time range, environment tick |
| excerpt_ref | ContentRef, nullable | Retained excerpt if permitted |
| observed_at | Instant, nullable | Observation time |
| recorded_at | Instant, required | Brain record time |
| collector_ref | ActorRef, required | Capturing actor/component |
| integrity_digest | String, nullable | Source integrity reference |
| evidential_role | Enum, required | supports, refutes, qualifies, context_only |
| source_reliability_ref | OpaqueId, nullable | Separate source assessment |
| scope_refs | ScopeRef[], required | Evidence access scope |
| availability_state | Enum, required | available, restricted, expired, forgotten, external_unavailable |

Evidence is not a confidence score. A mutable URL alone is not guaranteed durable evidence.

## 9. Provenance and Memory Source

Provenance fields: provenance_id (required), target_ref (required), source_edges (required), derivation_kind (required: direct_capture, extraction, normalization, summarization, consolidation, inference, human_correction, migration), method_ref (required), derived_at (required), input_digest_refs (required), parent_provenance_refs (required), unavailable_reason (nullable but required when incomplete).

Memory Source fields: memory_source_id, source_ref (typed and versioned where possible), source_role (primary, supporting, contradicting, context), locator, scope_refs, created_at. All except locator are required.

A method reference describes process; it does not prove correctness.

## 10. Memory Context and Context Entry

Memory Context fields: context_id, agent_scope_id, current_context_version, lifecycle_state, created_at, updated_at (required); task_scope_id, session_scope_id, environment_scope_id (nullable).

Context Entry fields: context_entry_id, context_id, canonical_memory_id, memory_version_id, rendering_ref, position, entry_state, added_at, source_refs (required); expires_at (nullable). MCM owns Context versions and Entry state. Entry changes do not mutate canonical objects.

## 11. Agent Scope and Environment Scope

Agent Scope fields: agent_scope_id, agent_id, owner_scope_id, scope_policy_ref, created_at, status (required); agent_instance_id nullable.

Environment Scope fields: environment_scope_id, environment_kind, environment_identity, tenant_or_project_scope_id, created_at, status (required); parent_environment_scope_id and environment_version_ref nullable. It must distinguish worlds, save files, simulation runs, tenants, and incompatible state domains.

## 12. Inputs, outputs, workflow, and consistency

State-changing proposals carry actor, scope, schema version, idempotency key where retryable, and provenance. Validation returns either a typed object or structured error: code, object_type, object_id, field_path, invariant_id, retryable.

Workflow: resolve scope → authorize → validate semantics → verify references → commit immutable record/version → publish change event. A pre-commit failure leaves no partial canonical mutation. Post-commit projection failure is repaired by outbox/replay. Stale version writes are rejected; duplicate idempotency with same digest returns prior result; same key with different digest is rejected.

## 13. Security, performance, acceptance

Scope-filter objects and references before disclosure. Evidence access may be stricter than Memory access. No untrusted content is executable or instruction-authoritative.

**TO_VALIDATE:** validation and serialization cost, reference fan-out, provenance traversal. Tests cover missing fields, unknown enums, duplicate IDs, stale versions, cross-scope references, invalid relation endpoints, Verified without evidence, and Context Entry mutation isolation.

## 14. Open decisions

- **OPEN:** ID strategy, timestamp precision, Claim identity across versions.
- **OPEN:** exact extensible vocabulary registry.
- **CANDIDATE:** typed references shaped as object_type + object_id + optional version_id.
- **TO_VALIDATE:** schema and provenance performance at high fan-out.
