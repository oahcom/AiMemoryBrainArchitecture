# GAP-11 — Merge of #541 created a second forget fence and closed nothing

**Status:** Open — new divergence introduced by a merged change
**Measured at:** `main @ b29278a8`, 2026-11-22 02:05 +08:00, WSL2 Ubuntu 24.04
**Supersedes nothing.** Complements GAP-06, which stays open.

## Why this exists

PR #541 merged at 2026-11-21T18:00:32Z as `b29278a8`. It adds a real, tested
forget authority to `crates/memory-storage-sqlite`. It does not close GAP-06,
and it introduces a second fence that GAP-06 never specified.

Both statements are measured below. Neither is an opinion about the PR's quality:
the code does what its commit message says. The problem is what "forget" now
means in this repository, which is no longer one thing.

## 1. What #541 actually built

A new table, independent of the pre-existing `forget_fence`:

```sql
CREATE TABLE IF NOT EXISTS canonical_forget_fences (
  target_kind TEXT NOT NULL CHECK (target_kind IN ('Memory', 'Version')),
  target_id   TEXT NOT NULL,
  fence_sequence INTEGER NOT NULL UNIQUE CHECK (fence_sequence > 0),
  reason_digest TEXT NOT NULL,
  recorded_at TEXT NOT NULL,
  PRIMARY KEY (target_kind, target_id)
);
```

`crates/memory-storage-sqlite/src/lib.rs:117`.

The pre-existing event-store fence is keyed differently:

```sql
CREATE TABLE IF NOT EXISTS forget_fence(
  namespace_key TEXT PRIMARY KEY,
  fence_seq INTEGER NOT NULL UNIQUE CHECK(fence_seq > 0),
  reason_digest TEXT NOT NULL,
  recorded_at TEXT NOT NULL
);
```

`crates/memory-event-store-sqlite/src/forget_fence.rs:56`.

GAP-06's contract is the second one: "a fenced **namespace** cannot yield a Memory
revision" (GAP-06, Recommendation). #541 implements the first one: "a fenced
**memory or version** cannot yield a Memory revision". Different granularity,
different table, different API, no reconciliation path.

## 2. The two fences do not know about each other

```
$ grep -rn "forget_fence" crates/memory-storage-sqlite/src/lib.rs crates/memory-store/src/lib.rs
(zero matches — the storage layer never consults the namespace fence)

$ grep -rn "canonical_forget" crates/memory-event-store-sqlite/src/forget_fence.rs
(zero matches — the event store never records a target fence)
```

Consequences, each independently checkable:

- A forget recorded through `ForgetFence::record_forget(namespace_key, digest)`
  still does not stop `MemoryStore::read_current`. Proved by a test that still
  passes on main, below.
- A forget recorded through `MemoryStorage::forget_memory(memory_id, digest)` does
  not cause `ForgetFence::restore_backup` to purge that memory's event rows. The
  restore path filters `accepted_events.scope_json` by namespace only.
  `forget_fence.rs:176`.
- The two mechanisms have separate reason-digest namespaces, so an auditor cannot
  join them to answer "was this memory ever forgotten".

## 3. Evidence that GAP-06 remains open

GAP-06 closure criterion 4 is explicit:

> The reverse test `forget_api_absence_is_detectable` is changed to assert the
> enforced behavior or removed with an explicit replacement regression test, and
> the ignored desired E2E `forgotten_memory_is_excluded_from_context` is enabled
> and passes.

Measured on `main @ b29278a8`:

```
$ cargo test -p memory-context --test e2e_negative_paths -- --include-ignored
test forgotten_memory_is_excluded_from_context ... ok
test forget_api_absence_is_detectable ... ok
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

`forget_api_absence_is_detectable` **passing is the defect**, not the good news.
That test records a namespace fence and then asserts the revision is *still*
readable. It is documented as such at `e2e_negative_paths.rs:209-211`:

> This test is expected to FAIL the moment forget is wired into the read gate.

It has not failed. The namespace fence is still not wired into any read gate.

## 4. `forgotten_memory_is_excluded_from_context` is a green with no assertions

This is the more serious finding, and it is independent of #541.

```rust
#[test]
#[ignore = "unreachable: no public forget API; see GAP-06-FORGET-PATH-UNREACHABLE"]
fn forgotten_memory_is_excluded_from_context() {
    // Intended public flow once the boundary exists:
    // create + write -> MemoryStore::forget_memory(memory_id, scope)
    // -> read_current returns no eligible revision -> build_context is empty.
    // Do not emulate this by editing ContextCandidate.lifecycle.
}
```

`crates/memory-context/tests/e2e_negative_paths.rs:199-207`. The body contains
four comment lines. There is no `assert`, no call, no fixture.

Therefore `--include-ignored` reports `ok`, and any future harness that runs
ignored tests to measure progress will count this as a passing forget test. It is
not a test. It is a TODO that reports success.

Contrast with the phase-2 acceptance tests, which handle the same "not yet
possible" situation honestly:

```
$ cargo test -p memory-domain --test phase2_acceptance -- --include-ignored
dm2_01_claim_revision_ref_uniqueness_enforced ... FAILED
dm2_02_accepted_revision_is_append_only ... FAILED
dm2_03_ci_classification_vectors ... FAILED
dm2_04_resolution_rejects_claim_head_substitution ... FAILED
dm2_06_missing_authorization_ref_blocks_fact_publication ... FAILED
dm2_08_unregistered_relation_type_rejected ... FAILED
dm2_09_relation_time_scope_lifecycle_independent ... FAILED
dm2_11_provenance_lineage_or_unavailable_reason_mandatory ... FAILED
dm2_12_shared_ancestry_not_independent_evidence ... FAILED
```

Nine failures, each an `unimplemented!()` at a named line, each with an `#[ignore]`
reason naming the missing API. That is a blocked test. The forget E2E is an empty
function. The difference is the whole point: one fails loudly when forced, the
other cannot fail.

## 5. The new forget path is still unreachable from production

Same shape as GAP-07. Every caller of the new API is inside `#[cfg(test)]`:

```
$ grep -rn "\.forget_memory(\|\.forget_version(" crates/ --include=*.rs
crates/memory-store/src/lib.rs:832,876                    (mod tests, cfg(test) at 120)
crates/memory-storage-sqlite/src/lib.rs:2948..3205        (mod tests, cfg(test) at 1182)
```

- `MemoryStore` exposes 8 public methods, none of them forget (`lib.rs:33-98`).
- `brain-cli` contains zero occurrences of `forget`.
- The only caller-capable surface is the `MemoryStorage` trait, i.e. an adapter
  consumer that does not exist yet.

So: three forget mechanisms now exist in the tree — event-store namespace fence,
storage target fence, and `MemoryLifecycle::Forgotten` — and no executable path
reaches any of them.

## 6. CI did not evaluate any of this

All four check runs on the #541 head commit and on `main` report the same
non-verdict. Annotation text, verbatim:

> The job was not started because recent account payments have failed or your
> spending limit needs to be increased.

`GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` returns
`403 — Upgrade to GitHub Pro or make this repository public to enable this
feature.`

So #541 was merged on a green mergeability flag, with zero executed checks and no
branch protection. Every finding in this document was produced by running the
code locally; none of it could have been caught by CI in its current state.

## Closure criteria

Close GAP-11 only when all hold:

1. One forget authority is designated as canonical, in a spec file, by name.
   The other is either removed or explicitly defined as a derived index of it.
2. The namespace fence and the target fence are reconciled: either a namespace
   forget also blocks reads of the memories in it, or the namespace fence is
   deleted and GAP-06 is re-scoped to target granularity deliberately.
3. `forgotten_memory_is_excluded_from_context` either contains assertions that
   fail today and pass after the fix, or is deleted. An empty ignored function
   must not survive as a progress signal.
4. `forget_api_absence_is_detectable` fails, and is then replaced by a
   regression test asserting the enforced behavior.
5. A non-test caller exists: either `MemoryStore::forget_*` or a CLI verb, with
   a test that goes through it.
6. `cargo test --workspace --all-targets` on the merged result reports 0 failed
   and, critically, the ignore count is re-derived rather than inherited.

## What this document does not claim

- That #541 is wrong. Its fences are enforced on 7 write/read paths (verified:
  `create_memory`, `commit_version`, `prepare_version`, `publish_prepared`,
  `read_version_row`, `list_changes`, `resolve_idempotency`), it has 19 new tests,
  and it removes none.
- That the forget feature is 0% done. At target granularity it is real and tested.
- That a namespace fence is the right design. It may well be the wrong one. That
  is exactly the decision Closure criteria 1-2 requires someone to make and
  record, instead of two mechanisms coexisting by accident.
