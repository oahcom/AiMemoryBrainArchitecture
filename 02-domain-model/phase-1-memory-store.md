# Phase 1 Memory Store Facade

Status: DECIDED for the Phase 1 orchestration boundary; storage backend remains replaceable.

## Purpose

Provide the smallest application-level facade that composes the frozen Domain Model with the backend-neutral MemoryStorage port.

## Responsibilities

- validate Memory and MemoryVersion domain invariants before storage;
- require resolved Scope on every operation;
- preserve Memory identity and immutable MemoryVersion/revision semantics;
- enforce memory_id == revision.memory_id before commit;
- delegate CAS, idempotency and visibility enforcement to MemoryStorage;
- expose read-current, read-revision and idempotency resolution without owning persistence.

## Non-responsibilities

The facade does not define SQLite DDL, transactions, distributed consensus, physical Forget, permissions, indexing, embeddings, LLM behavior, or deployment topology.

## Revision boundary

Phase 1 treats MemoryVersion as the canonical immutable revision representation. `MemoryRevision` is an API alias only; it does not create a second persistence object.

## Scope boundary

Every facade operation requires a non-empty resolved Scope. Scope compatibility is necessary but is not permission grant; Storage/Governance remain authoritative for visibility and authorization.

## Idempotent write boundary

A revision write carries expected-current-version, idempotency key and request digest together. The facade rejects identity mismatches before Storage and delegates replay/conflict semantics to the Storage port.

## Acceptance

- create/read operations require valid Scope;
- revision identity mismatch is rejected before backend invocation;
- stale revision transitions are rejected by the domain/storage boundary;
- same idempotency key + same digest can resolve to the original receipt;
- different scopes do not become implicitly visible;
- no backend-specific dependency enters the facade.

## Next unit

After this minimal facade is stable, continue with higher-level Memory Store behaviors and application integration; do not add vector/graph/LLM dependencies.
