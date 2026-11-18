# Phase 1 Storage Trait Contract

Status: CANDIDATE implementation seam; no backend is selected.

## Purpose

Define the backend-neutral application port between the pure memory-domain crate and future persistent implementations.

## Operations

- create_memory
- read_current
- read_version
- commit_version
- list_changes
- resolve_idempotency

## Commit boundary

A backend implementation MUST treat the immutable version, current-version CAS, idempotency record and canonical commit sequence as one recoverable commit boundary. This trait does not prescribe SQLite DDL or a distributed transaction protocol.

## Safety

Every read/write receives resolved scope. A backend MUST NOT use a stale projection as canonical state. expected_current_version is an optimistic-concurrency guard.

## Idempotency

The same idempotency key and request digest may return the original receipt. The same key with a different digest MUST return IdempotencyConflict.

## Explicit non-goals

No SQLite adapter, Event Store, Memory Store facade, network transport, vector/graph index, physical Forget implementation, or production durability claim is included.

## Verification

The crate contains pure Rust contract-shape tests only. They do not prove backend atomicity, crash recovery, serialization, concurrency across processes, or durability.
