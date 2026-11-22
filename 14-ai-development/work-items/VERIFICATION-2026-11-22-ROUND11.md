# Verification round — 2026-11-22 12:20–12:40 +08:00

Verifier measurements only. No code in this document was written by the verifier.

## 0. Read this first: the numbers move every few minutes

Main advanced three times while this round was being measured:

| time | head | passed | ignored |
|---|---|---|---|
| 12:20 | `1904c1af` | 487 | 3 |
| 12:35 | `b093b59f` | **503** | **1** |

So no figure below is a fact about "the repo". Each is a fact about a named commit at
a named minute. The findings that follow were re-confirmed at `b093b59f` before this
document was committed; the trend is recorded because the rate of change is itself
the most important measurement here.

## 1. Test baseline moved, and my earlier figures are superseded

```
$ cargo test --workspace --all-targets      # at b093b59f
PASSED=503  FAILED=0  IGNORED=1
```

The counting chain now reconciles without a residual, which the GAP-10 §6.2 note
left open:

| point | passed | ignored | delta |
|---|---|---|---|
| `b29278a8` (§6 measurement) | 385 | 10 | — |
| `444deef1` (this verifier) | 411 | 10 | +26 |
| `1904c1af` (this verifier) | 487 | 3 | +76 / −7 ignored |
| `b093b59f` (this verifier) | **503** | **1** | +16 / −2 ignored |

The nine tests that stopped being ignored across this window are the substantive
change: they were not skipped, they were implemented. §6.2's unresolved 371-vs-385
question is now moot — re-derivation was done rather than inherited, which is what
that note asked for.

One ignored test remains: `dm2_06_missing_authorization_ref_blocks_fact_publication`.
It is named, so it is a known hole rather than a silent one.

## 2. D6.2 landed, and it landed correctly

`#576` (`6500d9d4`) does what GAP-12 step 1 specified, by a session other than the
Owner I dispatched (mine was rate-limited at 429 before touching the tree).

Checked against GAP-12's own closure criteria:

| criterion | result | evidence |
|---|---|---|
| C1 no line names the cursor as confirmation | **PASS** | `lib.rs:643-647` comment states it is "NOT evidence that a canonical commit was confirmed" |
| C2 `StagingInput` field renamed | **PASS** | `lib.rs:431` `canonical_commit_cursor_recorded`; `PublicationProof` at `:287` deliberately unchanged |
| C3 test fails if a cursor alone yields `true` | **PASS** | `caller_supplied_cursor_does_not_confirm_canonical_commit`, plus `staging_accepts_a_recorded_cursor_...` and `staging_rejects_a_run_with_no_recorded_cursor` |
| C4 `pending_d()` not on a gate path | **PASS** | `grep pending_d crates/memory-compiler/` → 0 |
| C5 disposition unchanged | **PASS** | 503/0/1, `Ok(Blocked)` preserved |
| C6 steps 2/4/5 outstanding with owners | **PASS** | GAP-12 §5, GAP-13 §6 |

Note the rename kept the boundary exactly: `StagingInput` was renamed,
`PublicationProof` was not. A careless rename would have flipped the gate open.

## 3. GAP-11 closed in substance

The empty four-comment function I recorded as "passing is the defect" is now a
real test at `crates/memory-context/tests/e2e_negative_paths.rs:195`:

```
running 1 test
test forgotten_memory_is_excluded_from_context ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 7 filtered out
```

It asserts five things, including a before-state check that makes the later
assertions meaningful:

- memory visible before forget (`assert_eq!(before.memory_version_id, ...)`)
- `read_current` → `Ok(None)` after forget
- `read_revision` → `Ok(None)` after forget
- fenced write rejected with `MemoryStoreError::Storage(StorageError::Forgotten)`
- `forget_memory` is a public method on `MemoryStore` (`lib.rs:125`)

GAP-11's central finding — "the test had zero assertions, so `ok` proved nothing" —
no longer holds. It is replaced by a test that fails if forgetting stops working.

## 4. Still open, measured rather than assumed

**GAP-09 — schema non-empty audit is still red.**

```
$ cd 08-bmcp-protocol/schemas && python3 test_nonempty_audit.py
EXIT=1
5506 lines
32 *.json files present
```

Re-confirmed at `b093b59f`, byte-identical to the previous round. The attribution
stands: the audit table declares scope over "every direct-child `*.json`" and covers
2 of 32. This needs per-row human judgement on 30 schema families, not a script —
regenerating rows is the wrong repair, because #505 deliberately changed two
conditional constraints after reading schema semantics.

**GAP-11 — the two fences are still not reconciled.**

`canonical_forget_fences` in `memory-storage-sqlite` is consulted in 5 places
(`lib.rs:128,176,214,250,1062`). `forget_fence.rs` in `memory-event-store-sqlite`
holds its own fence. Neither crate references the other's. The forget *path* now
works end to end through `MemoryStore`, so the user-visible defect is closed, but
the split authority I recorded remains: two fences, two keys, no join.

This is a narrower and less urgent finding than GAP-11 originally was, and should
be re-scoped rather than carried forward as "Tier 1".

**GAP-13 — participant admission, external, unchanged.** Zero `JF10` in Rust; the
receipt schema still calls itself a candidate and disclaims key policy. Nothing in
this round moved it.

## 5. What this round did not do

- Did not re-audit the 30 schemas (needs owner judgement per family).
- Did not attempt `Published`: still requires the three external issuers named in
  GAP-12 §5 and GAP-13 §6.
- Did not touch the `Cargo.lock` untracked file present in both worktrees; whether
  it should be tracked is an owner call, not a verifier one.
