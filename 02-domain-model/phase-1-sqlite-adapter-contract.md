---
document_metadata:
  domain: domain-model
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-200/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "GOV-DOC-002 classification of a normative root that carried no front-matter: records domain, role and the status the document states in its own body (Status: DECIDED, Phase 1 SQLite persistence boundary only). Claims no canonical authority (canonical_status stays Non-Canonical) and records no Owner approval. Pre-metadata content blob: c472e00f2ef4d00bb71806efc7db72062f4efb58."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Normative
  bilingual_counterpart:
    source: null
    en: "docs/en/02-domain-model/phase-1-sqlite-adapter-contract.md"
    zh-CN: "docs/zh-CN/02-domain-model/phase-1-sqlite-adapter-contract.md"
---
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

## Decision: same-process independent-connection CAS correctness

DECIDED for the tested SQLite profile, limited to two independently opened SQLite Connection instances racing within one process against the same expected-current version:
- Exactly one competing CAS write commits.
- The losing writer receives `StaleVersion`.
- Reopening the database shows one current version and exactly one change-log record.
- Concurrent identical idempotency requests replay the same durable receipt and create only one change-log record.

Evidence:
- Implementation merged by PR #243; merge commit `4a3e06fd263e9dbd1056179dceb3cb21b17e330f` (PR head `179059a5be1973e2e188fd648ee57d1db7b004fe`).
- Exact PR #243 head Rust Workspace CI run #24 / Run ID `44259219033`: `cargo test --workspace --all-targets` — SUCCESS (34 passed, 0 failed).
- Exact PR #243 head bilingual documentation gate run #404 / Run ID `44259218907` — SUCCESS.
- Duplicate tracking PR #244 was closed without merging; its exact-head verification also passed (Rust Run ID `44259233587`, docs Run ID `44259233358`). No duplicate implementation is retained.

This decision is not evidence of cross-process or multi-host linearizability, distributed coordination, failover safety, or production topology suitability.

## Deliberate limits

This decision is limited to the Phase 1 behavior and the tested GitHub Actions local filesystem/runtime. It does not establish:
- power-loss, kernel-crash, storage-controller-cache, media-corruption or backup/restore recovery;
- cross-process or multi-host linearizability, distributed coordination or production deployment topology;
- production readiness or a production durability SLO.

The independent-connection CAS and idempotency race tests are same-process tests across separate SQLite Connection instances. Their bounded correctness is decided above; they do not expand this decision into a cross-process concurrency claim. PR #244 was a duplicate tracking carrier and was closed after PR #243 merged.

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
