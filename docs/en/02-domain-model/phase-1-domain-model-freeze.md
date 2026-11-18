# Phase 1 Domain Model Freeze

**Status:** DECIDED for the Phase 1 implementation scope; unresolved global decisions remain OPEN/CANDIDATE/TO_VALIDATE.  
**Repository:** `oahcom/AiMemoryBrainArchitecture`

## Purpose

Freeze the minimum domain contract required to implement and test Phase 1 without silently deciding later architecture questions.

## Freeze boundary

Phase 1 covers Event, Memory, MemoryVersion, Claim, ScopeRef, Provenance references and queryable canonical state.

It does not freeze ID-generation algorithms, BMCP wire format, SQLite DDL, vector/graph indexes, LLM or embedding providers, cross-version Claim identity, physical Forget semantics, permission-policy language, or distributed deployment semantics.

## Canonical objects

Phase 1 canonical objects are Event, Memory, MemoryVersion, Claim, Entity, Relation, Evidence, Provenance, MemorySource, MemoryContext, ContextEntry, ScopeRef, ActorRef and TemporalRef.

Fact is not a separate Phase 1 object. A verified fact is represented as a Claim with Verified epistemic status and the required evidence, temporal and scope metadata.

## Core invariants

- Event and Memory are distinct concepts.
- Memory identity remains stable across immutable versions.
- MemoryVersion is immutable; updates create successor versions.
- Concurrent updates require an expected current/parent version and stale writes are rejected.
- Scope is explicit and is not permission.
- Different scopes are not implicitly visible or merged.
- Claim epistemic status is independent from Memory lifecycle.
- Provenance must be present or explicitly unavailable; it must never be fabricated.
- Intent, plan, prediction and attempt do not become completed outcomes without outcome evidence.
- Domain validation is deterministic, side-effect free and independent of SQLite, HTTP, LLMs or agent frameworks.

## Scope isolation

Canonical scoped reads and writes require a resolved Scope. Ambiguous or missing Scope is rejected for scoped objects. Cross-Scope references require explicit sharing semantics.

## Domain API boundary

The future domain crate provides pure types and validation operations such as event, memory, version, claim and scope validation and version/scope transition checks. Storage, Compiler, Runtime and Governance call these capabilities through application ports.

## Acceptance

DM-01 through DM-10 cover object separation, version immutability, concurrency, Claim semantics, Scope isolation, Provenance, outcome boundaries, determinism, dependency boundaries and open-decision hygiene.

## Decision status

This freeze decides only the Phase 1 implementation semantics listed above. ID generation, global Claim identity, Relation vocabulary, Evidence-strength formulas, Scope algebra, permission policy language and physical Forget remain unresolved where the source domain documents mark them OPEN/CANDIDATE/TO_VALIDATE.

## Next unit

The next implementation unit is the Rust Workspace: establish the Cargo workspace, implement the frozen domain types and pure domain tests, and do not introduce Storage, SQLite, vector databases or model dependencies.