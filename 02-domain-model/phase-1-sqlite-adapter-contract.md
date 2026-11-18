# Phase 1 SQLite Adapter Contract

Status: CANDIDATE engineering implementation; not production readiness evidence.

## Scope

Implements the Phase 1 MemoryStorage trait against SQLite with:
- explicit schema initialization;
- immutable version rows;
- current-version CAS;
- idempotency receipt persistence;
- monotonic commit sequence;
- atomic version/current-pointer/commit-log/idempotency transaction;
- scope-filtered reads and change listing.

## Deliberate limits

This adapter does not implement Event Store, Lifecycle Manager, Forget erasure, distributed coordination, backup/PITR, multi-process linearizability evidence, or production deployment topology.

The serialized Memory and MemoryVersion payloads are an engineering representation only. Claim cross-version identity remains OPEN and is not resolved by this adapter.

## Transaction model

Writers use a SQLite immediate transaction. The commit boundary includes the version row, current pointer, commit-log row and idempotency receipt. A failed transaction rolls back.

## Verification ceiling

The PR includes SQLite in-memory round-trip, idempotency and stale-version tests. Repository-side Rust CI is not currently established, so no GitHub Actions test result is claimed until such a workflow exists.
