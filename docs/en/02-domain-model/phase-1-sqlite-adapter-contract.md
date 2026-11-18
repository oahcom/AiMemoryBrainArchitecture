# Phase 1 SQLite Adapter Contract

Status: DECIDED — Phase 1 SQLite persistence boundary only. This is not production-readiness evidence.

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

## Decision: Phase 1 persistence boundary

DECIDED for the tested local file-backed SQLite profile:
- File-backed connections enable WAL, synchronous=FULL, foreign_keys=ON and a 5-second busy timeout.
- A committed MemoryVersion and its current pointer, idempotency receipt and monotonic change sequence survive connection close and database reopen.
- When a separate process is terminated while the version row, current pointer, commit-log row and idempotency receipt have been written inside one Immediate transaction but before COMMIT, reopening the database exposes none of those uncommitted effects.
- The version/current-pointer/commit-log/idempotency write set is treated as one atomic transaction boundary.

Evidence:
- PR #242 merged into main: merge commit `aa711289785395d2efa202e34def64c393ee0ac7`.
- Verification commit `4a3e06fd263e9dbd1056179dceb3cb21b17e330f` is a descendant of the PR #242 merge commit and includes the SQLite persistence tests plus independent-connection CAS/idempotency race coverage.
- Rust Workspace CI: run ID `44259233587` (run #25), job `rust-workspace-test`, `cargo test --workspace --all-targets` — SUCCESS.
- GOV-DOC-001: run ID `44259233358` (run #405), job `GOV-DOC-001 structural checks` — SUCCESS.

## Deliberate limits

This decision is limited to the Phase 1 behavior and the tested GitHub Actions local filesystem/runtime. It does not establish:
- power-loss, kernel-crash, storage-controller-cache, media-corruption or backup/restore recovery;
- cross-process or multi-host linearizability, distributed coordination or production deployment topology;
- production readiness or a production durability SLO.

The independent-connection CAS and idempotency race tests are same-process tests across separate SQLite Connection instances. Their scope and follow-up are tracked separately by PR #244; they do not expand this decision into a cross-process concurrency claim.

The serialized Memory and MemoryVersion payloads are an engineering representation only. Claim cross-version identity remains OPEN and is not resolved by this adapter.

## Transaction model

Writers use a SQLite immediate transaction. The commit boundary includes the version row, current pointer, commit-log row and idempotency receipt. A failed or uncommitted transaction rolls back.

File-backed connections enable WAL and synchronous=FULL. In-memory connections use synchronous=FULL but retain SQLite's in-memory journal behavior. Each opened connection applies foreign_keys=ON and a 5-second busy timeout.

## Verification inventory

The Rust workspace CI workflow `.github/workflows/rust-phase1.yml` runs `cargo test --workspace --all-targets`.

SQLite adapter tests cover:
- in-memory round-trip, idempotency, stale-version and scope boundaries;
- committed state surviving connection close and database reopen, including current pointer, idempotency receipt and change sequence;
- two independent SQLite connections racing to commit against the same expected current version: exactly one CAS succeeds and the other receives StaleVersion;
- two independent SQLite connections concurrently submitting the same idempotency key, digest and request: both receive the same durable receipt and only one change record is created;
- abrupt process termination while a transaction has written the version row, current pointer, commit-log row and idempotency receipt but has not committed; reopening must recover with none of those partial effects visible.

The two-connection race tests validate write serialization and idempotency replay across independent SQLite Connection instances in one process; they are not a cross-process or multi-host linearizability proof.

The abrupt-exit test validates process-termination recovery of an uncommitted SQLite transaction under the tested local filesystem/runtime. It is not a power-loss, kernel-crash, storage-controller-cache, media-corruption, backup/restore, or multi-process linearizability proof.
