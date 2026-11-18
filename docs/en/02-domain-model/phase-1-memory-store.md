# Phase 1 Memory Store Facade

Status: DECIDED for the Phase 1 orchestration boundary; the storage backend remains replaceable.

## Purpose
Provide the smallest application-level facade composing the frozen Domain Model with the backend-neutral MemoryStorage port.

## Responsibilities
- validate Memory and MemoryVersion invariants before storage;
- require resolved Scope for every operation;
- preserve stable Memory identity and immutable MemoryVersion semantics;
- reject memory_id != revision.memory_id before commit;
- delegate CAS, idempotency and visibility enforcement to MemoryStorage;
- expose current/revision reads and idempotency resolution without owning persistence.

## Non-responsibilities
No SQLite DDL, distributed consensus, physical Forget, permission policy, indexing, embeddings, LLM behavior, or deployment topology.

## Revision boundary
MemoryVersion is the canonical immutable revision representation. MemoryRevision is an API alias only and is not a second persistence object.

## Scope boundary
Every facade operation requires a non-empty resolved Scope. Scope compatibility is not a permission grant.

## Idempotent write boundary
A revision write carries expected-current-version, idempotency key and request digest together. Identity mismatches are rejected before Storage; replay/conflict semantics are delegated to Storage.

## Acceptance
Create/read require valid Scope; revision identity mismatch fails before backend invocation; stale transitions are rejected; same key + same digest can resolve to the original receipt; different scopes are not implicitly visible; no backend-specific dependency enters the facade.

## Next unit
After this minimal facade is stable, continue with higher-level Memory Store behaviors and application integration. Do not add vector/graph/LLM dependencies.
