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
- scope-filtered reads and change listing;
- file-backed WAL journal mode with per-connection synchronous=FULL and a bounded 5-second busy timeout.

## Deliberate limits

This adapter does not implement Event Store, Lifecycle Manager, Forget erasure, distributed coordination, backup/PITR, multi-process linearizability evidence, power-loss/media-corruption proof, or production deployment topology.

The serialized Memory and MemoryVersion payloads are an engineering representation only. Claim cross-version identity remains OPEN and is not resolved by this adapter.

## Transaction model

Writers use a SQLite immediate transaction. The commit boundary includes the version row, current pointer, commit-log row and idempotency receipt. A failed transaction rolls back.

File-backed connections enable WAL and synchronous=FULL. In-memory connections use synchronous=FULL but retain SQLite's in-memory journal behavior. Each opened connection applies foreign_keys=ON and a 5-second busy timeout.

## Verification

The Rust workspace CI workflow `.github/workflows/rust-phase1.yml` runs `cargo test --workspace --all-targets`.

SQLite adapter tests cover:
- in-memory round-trip, idempotency, stale-version and scope boundaries;
- committed state surviving connection close and database reopen, including current pointer, idempotency receipt and change sequence;
- abrupt process termination while a transaction has written the version row, current pointer, commit-log row and idempotency receipt but has not committed; reopening must recover with none of those partial effects visible.

The abrupt-exit test validates process-termination recovery of an uncommitted SQLite transaction under the tested local filesystem/runtime. It is not a power-loss, kernel-crash, storage-controller-cache, media-corruption, backup/restore, or multi-process linearizability proof.

