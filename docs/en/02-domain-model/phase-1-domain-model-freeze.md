---
document_metadata:
  domain: domain-model
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      evidence_reference: []
    evidence_verification:
      verification_status: Unverified
      last_verification_note: "Owner-authorized classification direction for AID-2026-11-26-GOV-DOC-01; this is not a formal approval record. Pre-metadata content blob: 1b70c270cb0107219e71bbdb47cd95da51907bfe. Phase 1 semantic freeze does not authorize runtime implementation or deployment. Approval remains Draft; evidence verification remains Unverified."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Phase 1 domain model freeze"
    canonical_scope_id: domain-model/phase-1-domain-model-freeze
    canonical_scope_keywords:
      - phase-1
      - domain-freeze
      - domain-semantics
      - implementation-binding
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: "02-domain-model/phase-1-domain-model-freeze.md"
    en: null
    zh-CN: "docs/zh-CN/02-domain-model/phase-1-domain-model-freeze.md"
---
# Phase 1 Domain Model Freeze

**Status:** DECIDED for Phase 1 implementation scope; global unresolved decisions remain OPEN/CANDIDATE/TO_VALIDATE.  
**Document:** DOMAIN-MODEL-001 Phase 1 implementation freeze  
**Owner:** Memory Domain Model (MB-01)

## 1. Freeze boundary

Phase 1 freezes only the minimum domain semantics required for:

`Event -> Memory -> MemoryVersion -> Claim -> ScopeRef -> Provenance reference -> Queryable canonical state`.

This document does not freeze ID-generation algorithms, BMCP wire format, SQLite DDL, vector/graph indexes, LLM/embedding providers, physical Forget semantics, permission-policy language, or distributed deployment.

## 2. Canonical objects

The canonical source defines seven Phase 1 object sections (2.1–2.7). This mirror restores those sections and their object names. Sections 2.8–2.9 below are explanatory groupings of additional Evidence, Provenance, Scope, Actor, and Temporal references mentioned by this guide; they do not add objects to or expand the canonical Phase 1 freeze. The canonical source remains authoritative.

Phase 1 uses Event, Memory, MemoryVersion, Claim, ClaimRevision, Fact, FactRevision, Entity, Relation, Evidence, Provenance, MemorySource, MemoryContext, ContextEntry, ScopeRef, ActorRef, and TemporalRef.

Claim represents proposition identity and immutable ClaimRevision history.

Fact is an independent governed Attestation object referencing exact ClaimRevision values.

Fact is not equivalent to objective truth, Confidence, or Verified Claim status.

The convergence decision supersedes conflicting semantic descriptions in earlier Phase 1 documentation.

This is a semantic direction decision only. It does not approve physical Schema, DDL, public API, wire contract, production security material, or implementation conformance.

### 2.1 OpaqueId

All domain identifiers are opaque: they carry no business semantics, are not derived from display names, and are not reused during their defined lifecycle. Their serialization form is provisionally a string. The concrete generation algorithm remains CANDIDATE. Phase 1 does not permit business meaning to be inferred from an identifier's lexical order, prefix, or string contents.

### 2.2 ScopeRef

`ScopeRef` identifies the namespace and applicability of an object.

| Field | Constraint |
|---|---|
| `scope_id` | Required; an `OpaqueId` |
| `scope_kind` | Required; a controlled enumeration |
| `namespace_key` | Required; not derived from a display name |

Phase 1 supports these scope kinds: `user`, `project`, `agent`, `agent_instance`, `task`, `session`, `environment`, and `system`.

**DECIDED:** Scope and Permission are separate. The Domain Model expresses scope ownership/applicability and does not embed permission or grants in Memory data structures.

### 2.3 Event

Event records a captured or received occurrence, observation, report, transition, or governed input. It is not proof that the represented content is true. Event acceptance does not equal Memory truth.

### 2.4 Memory

Memory is a stable addressable retained-knowledge asset. Memory identity remains stable across versions. Lifecycle is independent from Claim epistemic status. ContextEntry does not own Memory and Context Remove is not Forget.

### 2.5 MemoryVersion

MemoryVersion is an immutable semantic snapshot. Updates create successor versions. The current-version pointer and new canonical version commit must share the canonical transaction boundary. Concurrent updates require an expected current/parent version; stale writes return conflict.

### 2.6 Claim

Claim is the canonical proposition. Epistemic states are Observed, Reported, Inferred, Verified, Disputed, and Retracted. Confidence is not truth. Conflicts and retractions preserve history and evidence.

**Identity boundary:** Proposition identity uses a stable ClaimRef across Memory versions; immutable assertion states use exact ClaimRevisionRef values under DOMAIN-MODEL-001 §2.4. This semantic classification is DECIDED FOR CONVERGENCE. ID-generation algorithms remain CANDIDATE and are not frozen here.

### 2.7 ProvenanceRef

Phase 1 does not redefine the complete Provenance DAG. MemoryVersion stores immutable provenance references.

Each derived MemoryVersion must:

- reference at least one valid source/provenance; or
- explicitly record why provenance is unavailable;
- never fabricate a missing source;
- never treat model/method identity as proof of truth.

The complete Provenance graph is deferred to later Compiler / Governance work.

### 2.8 Evidence and Provenance concepts

Evidence supports, refutes, or qualifies a Claim. Provenance records origin and derivation lineage. Missing source material is represented as unavailable rather than fabricated. Model or method identity is not proof of truth.

### 2.9 Scope / Actor / Temporal references

Scope identifies the namespace/applicability of an object and is distinct from Permission. Actor identifies the principal responsible for an operation/source and is not a permission grant. TemporalRef preserves event/recorded/valid-time distinctions; unknown time is not timeless.

## 3. Required invariants

1. Event and Memory are distinct concepts.
2. Memory identity is stable across versions.
3. MemoryVersion is immutable.
4. Version numbers are monotonic and stale writes cannot overwrite newer versions.
5. Scope is explicit and not inferred from display names.
6. Different scopes are not implicitly merged.
7. Permission is not derived from ScopeRef.
8. Planned/predicted/attempted states do not automatically become completed outcomes.
9. Claim epistemic status and Memory lifecycle are independent.
10. Missing provenance is explicit, never fabricated.
11. Context operations do not directly mutate Canonical Memory.
12. Domain validation is deterministic and has no LLM/network/storage dependency.

## 4. Scope isolation

Canonical reads/writes carry resolved Scope. Different scopes are not implicitly visible. Ambiguous or missing scope for scoped objects is rejected. Cross-scope references require explicit sharing authorization.

Same Scope is not a Permission grant; Governance remains authoritative for authorization.

## 5. Domain API boundary

The future domain crate provides pure domain types and validation, including Event, Memory, MemoryVersion, Claim, ScopeRef and ProvenanceRef plus deterministic validation and version/scope compatibility checks. It does not directly operate Storage, HTTP, LLMs, or external frameworks.

## 6. Acceptance criteria

DM-01 Object separation; DM-02 Version immutability; DM-03 Version concurrency; DM-04 Claim semantics; DM-05 Scope isolation; DM-06 Provenance; DM-07 Outcome boundary; DM-08 Deterministic validation; DM-09 Dependency boundary; DM-10 Open-decision hygiene.

## 7. Decision status

**DECIDED for Phase 1:** Event/Memory/MemoryVersion/Claim boundaries, stable Memory identity, immutable MemoryVersion, expected-parent version transition, Scope/Permission separation, Phase 1 scope isolation, Claim epistemic/lifecycle separation, and deterministic dependency-free domain validation.

**DECIDED FOR CONVERGENCE:** Stable ClaimRef proposition identity across Memory versions and the CI-01..CI-13 classification in DOMAIN-MODEL-001 §2.4.

**Unchanged:** ID generation CANDIDATE; Relation vocabulary OPEN; Evidence strength TO_VALIDATE; Scope algebra OPEN; Permission policy language OPEN; physical Forget semantics OPEN; Vector/Graph technology outside Phase 1.

## 8. Engineering handoff — deferred, not authorized

This section records a possible future engineering handoff. It is not a current implementation instruction or authorization.

- `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE` is controlling (see Issues #7 and #1197).
- Phase 1 DECIDED means only that the domain semantics listed here are frozen as an architecture baseline. It does not authorize creating or extending a Rust workspace/crate now, nor Brain runtime, storage integration, production implementation, or deployment.
- The bounded Phase 1 Rust types/tests already present in the repository are historical work (see the bounded work recorded in Issue #200); they do not authorize new or expanded work.
- A future engineering phase may reassess a Cargo workspace, `crates/memory-domain`, Rust types, and DM-01..DM-10 tests. Work may start only after engineering-entry prerequisites are met and a separate explicit Owner implementation authorization is recorded.
- This Freeze does not freeze crate, process, service, or deployment boundaries, and does not authorize Storage, SQLite, Vector DB, or model integration.

> This English document is the normative bilingual counterpart of `02-domain-model/phase-1-domain-model-freeze.md`.
