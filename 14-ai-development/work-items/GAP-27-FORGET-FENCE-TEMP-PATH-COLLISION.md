---
document_metadata:
  domain: ai-development
  role: research

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "Reproduced deterministically: the temp() body copied verbatim into a standalone program, 8 threads x 200 calls with the shared name 'fixture', produced 21 and 24 duplicate paths in two runs; back-to-back SystemTime::now() returned identical nanoseconds in 75,881/100,000 and 76,081/100,000 pairs. Source at forget_fence.rs:9 and the single call-site name at :44 confirmed by reading the file at main 22a1f30f."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-27 — `forget_fence` builds fixture paths that collide under concurrency

**Status:** Open — not repaired here
**Area:** test harness, not production code
**Found at:** a full-workspace run on `feat/context-sufficiency-report-fields-2026-11-22`
**Confirmed at:** `main` @ `22a1f30f`

---

## 1. The failure

A full-workspace run exited `101`:

```
test restore_anti_resurrection_and_preserves_other_scope ... FAILED

thread 'restore_anti_resurrection_and_preserves_other_scope' panicked at
crates\memory-event-store-sqlite\tests\forget_fence.rs:23:7:
called `Result::unwrap()` on an `Err` value:
SqliteFailure(Error { code: Unknown, extended_code: 1 },
              Some("table accepted_events already exists"))

test result: FAILED. 4 passed; 1 failed
```

Two tests opened the same file. The second one's `schema()` re-ran its
`CREATE TABLE` batch against a database the first had already initialised.

## 2. The cause

`crates/memory-event-store-sqlite/tests/forget_fence.rs:9`:

```rust
fn temp(name: &str) -> PathBuf {
    let n = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    std::env::temp_dir().join(format!("forget-fence-it-{name}-{}-{n}", std::process::id()))
}
```

Uniqueness rests on `as_nanos()` alone, and two facts break that:

**(a) Every fixture caller passes the same name.** Line 44 is `temp("fixture")`,
and it is the only name any test uses to build a database. The path therefore
reduces to `pid + nanos`; the `name` segment contributes nothing.

**(b) The clock has ~13ms resolution here, not nanoseconds.** Two back-to-back
`SystemTime::now()` calls returned the *identical* nanosecond value in
**75,881 of 100,000** and **76,081 of 100,000** pairs across two runs.

`pid` is also shared, because `cargo test` runs a binary's test functions as
threads in one process.

## 3. The reproduction

I copied `temp()` verbatim into a standalone program, spawned 8 threads that
each called `temp("fixture")` 200 times after a barrier, and counted distinct
paths:

```
paths generated : 1600      paths generated : 1600
distinct paths  : 1579      distinct paths  : 1576
collisions      : 21        collisions      : 24
```

21–24 duplicate paths per 1,600 calls, twice. This is not a rare race — it is
the expected behaviour of a millisecond-resolution clock under a scheme that
assumes nanoseconds. The failure needs only two tests to request a fixture in
the same tick.

One correction worth recording: my first version of this proof gave each thread
a distinct name (`t{t}-r{r}`) and produced **zero** collisions. That result was
an artefact of the experiment, not evidence of safety — with distinct names the
path is unique regardless of the clock. The real caller uses one shared name,
which is what makes the clock matter. The first experiment measured the wrong
thing and would have closed this as a non-issue.

## 4. Not a regression from #678

| run | result |
|---|---|
| `main` @ `550bb864`, `--test forget_fence` alone | 5 passed |
| `main` @ `550bb864`, full workspace | 666 passed, 0 failed |
| PR branch, `--test forget_fence` alone, 12 consecutive runs | 12/12 passed |
| PR branch, `--test forget_fence -- --test-threads=1`, 6 runs | 6/6 passed |
| PR branch, full workspace, run 1 | **1 failed**, exit 101 |
| PR branch, full workspace, run 2 | 687 passed, 0 failed |

`memory-context` has no dependency on `memory-event-store-sqlite` in either
direction. What changed is timing: 21 more tests in the workspace changes the
contention these tests meet when `cargo test` schedules crates in parallel. The
defect was always there; the added load exposed it.

A defect that only appears on a busy machine is still a defect. It will surface
in CI at random, on unrelated PRs, and be attributed to whoever is shipping.

## 5. Why it is not repaired here

**(a) Scope.** AID-2026-049 authorises `crates/memory-context` and two coverage
rows. `crates/memory-event-store-sqlite/tests/` is outside that.

**(b) It does not need to ride along.** The fix is a few lines and a test. A
test-harness change buried inside an unrelated feature PR is harder to review
than the same change on its own.

## 6. What a fix has to do

Make uniqueness a property of the code rather than of the clock:

```rust
use std::sync::atomic::{AtomicU64, Ordering};
static NEXT: AtomicU64 = AtomicU64::new(0);

fn temp(name: &str) -> PathBuf {
    std::env::temp_dir().join(format!(
        "forget-fence-it-{name}-{}-{}",
        std::process::id(),
        NEXT.fetch_add(1, Ordering::Relaxed)
    ))
}
```

`tempfile::TempDir` would also be correct but adds a dependency, which is a
separate decision. Wrapping the existing code in a `Mutex` fixes the symptom
while leaving the clock assumption for the next reader — worse than the counter.

However it is done, it should ship with a test that fails against the current
code: N threads calling `temp("fixture")`, asserting N distinct paths. Without
that test the failure stays silent until load is high, which is exactly how it
reached a full-workspace run.

## 7. Acceptance

- The uniqueness test fails on the current implementation and passes on the
  fixed one.
- `cargo test -p memory-event-store-sqlite --test forget_fence` passes
  repeatedly with `--test-threads` at the default, on a loaded machine.
- No production code in `memory-event-store-sqlite` changes.
