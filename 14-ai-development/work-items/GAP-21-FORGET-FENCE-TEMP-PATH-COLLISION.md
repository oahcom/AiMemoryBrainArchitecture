# GAP-21 — The forget_fence test harness generates colliding temp paths under parallel load

**Status:** OPEN — not fixed, deliberately not fixed inside PR #678
**Discovered:** 2026-11-22, while verifying AID-2026-049
**Severity:** P2 — produces a false red on any full-workspace run; does not affect production code
**Owner:** NOT_ASSIGNED

## What happened

A full-workspace run on `feat/context-sufficiency-report-fields-2026-11-22` exited `101`:

```
running 5 tests
test restore_anti_resurrection_and_preserves_other_scope ... FAILED
test missing_or_corrupt_fence_fails_closed ... ok
test malformed_scope_refuses_activation_without_partial_change ... ok
test crash_after_fence_commit_is_retried_without_resurrection ... ok
test concurrent_forget_waits_for_restore_snapshot_lock ... ok

thread 'restore_anti_resurrection_and_preserves_other_scope' panicked at
crates\memory-event-store-sqlite\tests\forget_fence.rs:23:7:
called `Result::unwrap()` on an `Err` value:
SqliteFailure(Error { code: Unknown, extended_code: 1 }, Some("table accepted_events already exists"))

test result: FAILED. 4 passed; 1 failed; 0 ignored
error: test failed, to rerun pass `-p memory-event-store-sqlite --test forget_fence`
```

## The cause

`crates/memory-event-store-sqlite/tests/forget_fence.rs:10`:

```rust
fn temp(name: &str) -> PathBuf {
    let n = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    std::env::temp_dir().join(format!("forget-fence-it-{name}-{}-{n}", std::process::id()))
}
```

The path is `name + pid + nanos`. Two test functions running as **concurrent threads
in one process** share the pid, so uniqueness rests entirely on `as_nanos()`. The
clock resolution available to `SystemTime::now()` is not guaranteed to be
nanosecond-granular, and under load it is not: two threads can read the same
value, land on the same path, and the second `schema()` call hits
`CREATE TABLE accepted_events` on a file the first one already initialised.

Note the failure is *not* a data race in the store — it is a collision in the
test's own scaffolding. `schema()` opens the colliding file and re-runs its
`CREATE TABLE` batch.

## Why it is not a regression from PR #678

Evidence that the failure is pre-existing and load-dependent rather than caused
by the change under review:

| Run | Result |
|---|---|
| `main` at `550bb864`, `--test forget_fence` alone | 5 passed, EXIT 0 |
| `main` at `550bb864`, full workspace | 666 passed, 0 failed, EXIT 0 |
| PR branch, `--test forget_fence` alone, 12 consecutive runs | 12/12 passed |
| PR branch, `--test forget_fence -- --test-threads=1`, 6 runs | 6/6 passed |
| PR branch, full workspace, run 1 | **1 failed**, EXIT 101 |
| PR branch, full workspace, run 2 | 687 passed, 0 failed, EXIT 0 |

`memory-context` has no dependency on `memory-event-store-sqlite` in either
direction; the two crates share no types. What changed is *timing*: adding 21
tests to the workspace changes how much CPU contention the `forget_fence` tests
see when `cargo test` schedules crates in parallel, which is exactly the
condition the nanos assumption does not survive.

A defect that only appears when the machine is busy is still a defect. It will
appear in CI, at random, on unrelated PRs, and it will be attributed to whoever
happens to be shipping at the time.

## Why it was not fixed here

Fixing it means changing a test harness in a crate this PR does not otherwise
touch. Two reasons to keep it separate:

1. **Scope.** AID-2026-049 authorises `crates/memory-context` and two coverage
   rows. `crates/memory-event-store-sqlite/tests/` is outside that.
2. **Evidence.** A fix should come with a reproduction that fails reliably
   before and passes reliably after. This report records the observation; it does
   not establish a deterministic reproduction.

## What a fix has to do

The path must be unique **without relying on clock resolution**. Any of these
suffices; the first is the smallest:

- a per-call atomic counter appended to the name:
  `static NEXT: AtomicU64 = AtomicU64::new(0);` then
  `format!("forget-fence-it-{name}-{}-{}", process::id(), NEXT.fetch_add(1, Ordering::Relaxed))`;
- a process-wide `Mutex` around the path generation, which is correct but leaves
  the clock assumption in place for the next reader;
- `tempfile::TempDir`, which is a new dependency and therefore a separate
  decision.

The counter is preferable: it makes uniqueness a property of the code rather
than of the platform's timer.

A test that pins the behaviour is worth having — spawn N threads that each call
`temp("x")` and assert N distinct paths — because the current failure mode is
silent until load is high.

## Acceptance for closing this

- `cargo test -p memory-event-store-sqlite --test forget_fence` passes with
  `--test-threads` at the default, repeatedly, on a loaded machine.
- The new uniqueness test fails against the current implementation and passes
  against the fixed one.
- No production code in `memory-event-store-sqlite` changes.
