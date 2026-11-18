# Phase 1 Domain Model Freeze

**Status:** DECIDED for Phase 1 implementation scope; unresolved global decisions remain OPEN/CANDIDATE/TO_VALIDATE.  
**Purpose:** Reduce the existing Domain Model specification to the smallest implementable, testable and persistable Phase 1 contract.

## 1. Freeze boundary

Phase 1 freezes only the semantics required for:

```
Event -> Memory -> MemoryVersion -> Claim -> ScopeRef -> Provenance reference -> Queryable canonical state
```

This document does not decide concrete ID generation, BMCP wire format, SQLite DDL, vector/graph indexes, LLM/embedding providers, stable Claim identity across versions, physical Forget semantics, permission policy language, or distributed consistency. Those remain governed by the existing domain documents and later ADRs.

## 2. Canonical objects

### OpaqueId
Domain IDs carry no business meaning, are not derived from display names, are not reused within their lifetime, and are serialized as strings. The generation algorithm remains CANDIDATE.

### ScopeRef
Minimum fields are `scope_id`, `scope_kind`, and `namespace_key`. Supported kinds are user, project, agent, agent_instance, task, session, environment, and system.

**DECIDED:** Scope and Permission are separate. Scope expresses namespace/applicability; it does not grant read/write permission.

### Event
Event represents an occurrence, observation, report, transition, or other governed input. Minimum semantics include identity, kind, source, payload reference, recorded time, scope, classification, schema version, retention class, and operation-dependent idempotency key.

Classifications include observed, reported, planned, predicted, attempted, outcome, administrative, and unknown.

Acceptance of an Event does not prove truth. planned/predicted/attempted must not automatically become outcome. Reuse of an idempotency key with a different payload digest is a conflict.

### Memory
Memory is a stable, addressable retained knowledge asset. Its identity is stable across versions. Lifecycle state is independent from truth status. ContextEntry does not own Memory, and Context Remove is not Forget.

### MemoryVersion
MemoryVersion is an immutable semantic snapshot. It has a stable identity, Memory identity, monotonic version number, parent reference where applicable, author/change metadata, claims, provenance references, digest, and schema version.

Versions are never mutated in place. New state creates a successor version. The current-version pointer and canonical commit belong to the same transaction boundary. Concurrent writes must provide the expected current/parent version and stale writes must conflict rather than overwrite.

### Claim
Claim is the canonical proposition stored in Memory. It has subject, predicate, object, polarity, epistemic status, optional confidence/valid time, assertion time, scope and qualifiers.

Phase 1 statuses are observed, reported, inferred, verified, disputed and retracted.

Confidence is not truth. Verified requires appropriate method/evidence semantics. Disputed and retracted states preserve the relevant history.

**Identity boundary:** `claim_id` is unique within an immutable MemoryVersion. Stable identity across MemoryVersions remains **OPEN**.

### ProvenanceRef
Phase 1 stores immutable provenance references but does not freeze the complete Provenance DAG. Derived versions require valid lineage or an explicit unavailable reason. Missing sources must never be fabricated, and model/method identity is not itself truth proof.

## 3. Required domain invariants

1. Event and Memory remain distinct concepts.
2. Memory identity is stable across Versions.
3. MemoryVersion is immutable.
4. Version numbers are monotonic and non-reused per Memory.
5. Stale updates cannot overwrite the latest version.
6. Scope is explicit and never inferred from display names.
7. Different scopes are not implicitly merged by identical text, labels, or Agent names.
8. Permission is not inferred from Scope.
9. Planned/predicted/attempted do not become completed outcome automatically.
10. Claim epistemic status is independent from Memory lifecycle.
11. Missing provenance is explicit, never fabricated.
12. Unknown time is not timeless.
13. Context operations do not directly mutate Canonical Memory.
14. Domain validation is deterministic and LLM-independent.
15. Domain objects do not depend on SQLite, HTTP, Agent frameworks, or model implementations.

## 4. Scope isolation

Canonical reads/writes carry a resolved scope.

```
same scope      -> eligible for domain-level access
different scope -> not implicitly visible
ambiguous scope -> reject
missing scope   -> reject for scoped objects
```

This is not a complete Permission Policy. Governance decides permissions. Same Scope means semantic namespace compatibility only.

Acceptance must demonstrate: cross-environment reads are rejected; identical Agent identity with different Environment Scope is not implicitly merged; unresolved scoped objects cannot enter canonical storage; cross-scope references require explicit sharing semantics; filtering occurs before query results are formed.

## 5. Domain API boundary

The future Domain crate provides pure domain types and validation and does not directly operate storage.

Target capabilities:

```
validate_event(...)
validate_memory(...)
validate_memory_version(...)
validate_claim(...)
validate_scope(...)
check_version_transition(...)
check_scope_compatibility(...)
```

Storage, Compiler, Runtime and Governance call these capabilities through application ports.

## 6. Acceptance evidence

| ID | Acceptance | Required proof |
|---|---|---|
| DM-01 | Object separation | Event / Memory / Version / Claim independently expressible |
| DM-02 | Version immutability | updates create successor Versions |
| DM-03 | Version concurrency | stale versions are rejected |
| DM-04 | Claim semantics | epistemic status and lifecycle remain separate |
| DM-05 | Scope isolation | different scopes are not implicitly visible/merged |
| DM-06 | Provenance | lineage or explicit unavailable state |
| DM-07 | Outcome boundary | plan/prediction/attempt does not become outcome |
| DM-08 | Determinism | no model/external-service dependency |
| DM-09 | Dependency boundary | no SQLite/HTTP/LLM dependency |
| DM-10 | Open-decision hygiene | unverified decisions are not silently frozen |

## 7. Decision status

DECIDED for Phase 1: object boundaries, stable Memory identity, immutable MemoryVersion, expected-parent transition semantics, Scope/Permission separation, scope isolation baseline, Claim epistemic/lifecycle separation, and pure domain validation.

Still unchanged: ID generation CANDIDATE; Claim global identity OPEN; Relation vocabulary OPEN; Evidence strength TO_VALIDATE; Scope algebra OPEN; Permission policy language OPEN; physical Forget OPEN; Vector/Graph outside Phase 1.

## 8. Next implementation unit

**Rust Workspace**: establish Cargo workspace and `crates/memory-domain`; implement the frozen core types and domain-invariant tests; do not introduce Storage, SQLite, Vector DB, or model dependencies.