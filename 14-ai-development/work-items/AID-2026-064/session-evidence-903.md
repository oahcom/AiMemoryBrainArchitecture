---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every tally below was produced on this branch, on this host, by the session that wrote the change. The pre-fix tallies were taken on the unmodified tree at origin/main 7a69f32b before either edit existed; the post-fix and negative-control tallies were taken on the tree that is the commit under review."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session role / use case

IMPLEMENTER. Fix Issue #903: a test-isolation defect in `memory-event-store-sqlite`
whose fixture directory name is unique only if the wall clock moves between two
callers. Scope was fixed by the Issue (option 1, a per-process atomic counter) and
by the ruling that came with the assignment: no new dependency, no assertion
changes, and the same treatment for any other helper with the same defect.

# Actual AI input

One prompt, recorded verbatim as `prompt-v1.md` in this directory and pinned by
digest in `manifest.yaml`:

| file | bytes | sha256 |
|---|---:|---|
| `14-ai-development/work-items/AID-2026-064/prompt-v1.md` | 8623 | `88d1eae165f7535fa608f847f2998930df3236ee77d596be440d3fc190054477` |

It fixed the remedy (option 1), forbade two of the Issue's other options, named
the three files to inspect, and required the measurements below. No follow-up
instruction changed the scope. Provenance is `NOT_VERIFIED`: the digest proves
this file has not changed since it was pinned, not that it is byte-for-byte what
the model received.

Repository state read rather than assumed: Issue #903 body (`2026-11-24T07:42Z`),
`origin/main` at `7a69f32b`, and the gate it names (#134, `cargo test --workspace
--all-targets` as a merge gate).

# AI-visible output

Two source files, both test-only:

```
crates/memory-event-store-sqlite/src/forget_fence.rs     | 11 ++++++++++-
crates/memory-event-store-sqlite/tests/forget_fence.rs   | 12 +++++++++++-
```

`temp()` in each now appends a `static COUNTER: AtomicU64` incremented with
`fetch_add(1, Ordering::Relaxed)` to the generated name. The clock value is kept
so a reader can still see when the fixture was made; it is no longer load-bearing.

**A third file has the same helper and is deliberately unchanged.**
`crates/memory-event-store-sqlite/tests/forget_fence_real_schema.rs` defines a
`temp()` with the identical name+pid+nanos shape, but it is already collision-free:
its eight call sites pass seven distinct names (`live`, `backup`, `fence`,
`wal-live`, `wal-backup`, `wal-backup-checkpointed`, `wal-fence`), each used once in
the binary, so no two concurrent calls can produce the same path even in the same
clock tick. Applying the counter there would be symmetry, not a fix. The ceiling is
recorded here instead: a future test that reuses one of those names would need the
same treatment.

# What was measured, and on what

Host: Windows 11, `rustc 1.100.0` (`x86_64-pc-windows-gnu`). The host's default
`gcc` shim is broken (`cc1` missing), so `libsqlite3-sys` was built with the
complete winlibs mingw-w64 16.2.0 that WinGet had already installed. That is a
local build-toolchain fact, not a change in this branch.

Clock granularity, measured because the whole defect depends on it: 2,000,000
consecutive `SystemTime::now().duration_since(UNIX_EPOCH).as_nanos()` reads
returned **1,547,333 adjacent duplicates**, smallest observed delta **100 ns**.
Ticks are coarse enough here for two threads to collide, which is what the Issue
predicted.

## 1. The defect, before any change

`cargo test -p memory-event-store-sqlite --lib`, default parallelism:

```
80 runs   -> 80 pass, 0 fail
```

That is not enough to see it: cargo's own startup staggers the five `fixture()`
callers most of the time. The same binary run directly, 200 times, does see it:

```
200 runs  -> 197 pass, 3 fail  (runs 16, 156, 191)
```

Every failure is the Issue's exact signature, at the same line:

```
thread 'forget_fence::tests::concurrent_forget_serializes_behind_restore_fence_lock' panicked at
crates\memory-event-store-sqlite\src\forget_fence.rs:329:11:
called `Result::unwrap()` on an `Err` value: SqliteFailure(Error { code: Unknown,
  extended_code: 1 }, Some("table accepted_events already exists"))
```

and one of the three hit `crash_after_fence_commit_is_retried_safely_on_restore`
instead, which is the same collision from the other side. The failure rate is
1.5%, lower than the Issue's ~1-in-6 on the reporting host; the mechanism is
identical and reproducible on demand, which is what matters.

## 2. After the change

```
200 direct runs -> 200 pass, 0 fail
```

## 3. Negative control

The counter line was replaced with `let seq = 0;`, the binary rebuilt, and the
same 200 runs repeated. It was then restored:

```
200 direct runs -> 195 pass, 5 fail  (runs 1, 6, 13, 15, 120)
```

Same message, same line. The counter is the cause of the difference, not the
rebuild.

## 4. Nothing else broken

```
cargo test -p memory-event-store-sqlite
  5 targets, 39 tests, 39 pass, 0 fail

cargo test --workspace --all-targets --no-fail-fast
  exit 0; 53 targets, 787 tests, 787 pass, 0 fail, 0 ignored
```

# What this record does not claim

- It does not claim the collision is gone across *processes*. Two processes
  sharing a temp directory can still collide on name+pid+nanos; the counter is
  per process. `tempfile::TempDir` is the upgrade path and was ruled out of scope.
- It does not claim Issue #903's `--test-threads=1` observation was re-measured
  here; the serial count (26/26) was already recorded in the Issue and is not the
  thing this branch changes.
- It does not claim independent review. `review.status` is `NOT_ASSIGNED` in the
  manifest.
