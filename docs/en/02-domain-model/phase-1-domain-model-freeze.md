# Phase 1 Domain Model Freeze

**Status:** DECIDED for Phase 1 implementation scope; global unresolved decisions remain OPEN/CANDIDATE/TO_VALIDATE.  
**Document:** DOMAIN-MODEL-001 Phase 1 implementation freeze  
**Owner:** Memory Domain Model (MB-01)

## 1. Freeze boundary

Phase 1 freezes only the minimum domain semantics required for:

`Event -> Memory -> MemoryVersion -> Claim -> ScopeRef -> Provenance reference -> Queryable canonical state`.

This document does not freeze ID-generation algorithms, BMCP wire format, SQLite DDL, vector/graph indexes, LLM/embedding providers, physical Forget semantics, permission-policy language, or distributed deployment.

## 2. Canonical objects

Phase 1 uses Event, Memory, MemoryVersion, Claim, ClaimRevision, Fact, FactRevision, Entity, Relation, Evidence, Provenance, MemorySource, MemoryContext, ContextEntry, ScopeRef, ActorRef, and TemporalRef.

Claim represents proposition identity and immutable ClaimRevision history.

Fact is an independent governed Attestation object referencing exact ClaimRevision values.

Fact is not equivalent to objective truth, Confidence, or Verified Claim status.

The convergence decision supersedes conflicting semantic descriptions in earlier Phase 1 documentation.

This is a semantic direction decision only. It does not approve physical Schema, DDL, public API, wire contract, production security material, or implementation conformance.

### Event

Event records a captured or received occurrence, observation, report, transition, or governed input. It is not proof that the represented content is true. Event acceptance does not equal Memory truth.

### Memory

Memory is a stable addressable retained-knowledge asset. Memory identity remains stable across versions. Lifecycle is independent from Claim epistemic status. ContextEntry does not own Memory and Context Remove is not Forget.

### MemoryVersion

MemoryVersion is an immutable semantic snapshot. Updates create successor versions. The current-version pointer and new canonical version commit must share the canonical transaction boundary. Concurrent updates require an expected current/parent version; stale writes return conflict.

### Claim

Claim is the canonical proposition. Epistemic states are Observed, Reported, Inferred, Verified, Disputed, and Retracted. Confidence is not truth. Conflicts and retractions preserve history and evidence.

**Identity boundary:** Proposition identity uses a stable ClaimRef across Memory versions; immutable assertion states use exact ClaimRevisionRef values under DOMAIN-MODEL-001 §2.4. This semantic classification is DECIDED FOR CONVERGENCE. ID-generation algorithms remain CANDIDATE and are not frozen here.

### Evidence / Provenance

Evidence supports, refutes, or qualifies a Claim. Provenance records origin and derivation lineage. Missing source material is represented as unavailable rather than fabricated. Model or method identity is not proof of truth.

### Scope / Actor / Temporal references

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

## 8. Next implementation unit

Rust Workspace: Cargo workspace, `crates/memory-domain`, Rust types and deterministic DM-01..DM-10 tests, without Storage/SQLite/vector/model dependencies.

> This English document is the normative bilingual counterpart of `02-domain-model/phase-1-domain-model-freeze.md`.
