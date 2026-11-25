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
      last_verification_note: "The prompt text below is the instruction set this session executed, reproduced without edits. The front-matter block was added afterwards because the document-management gate requires document_metadata on every governed document, including prompt snapshots; the recorded digest pins this file, front-matter included."
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

# AID-2026-069 — executed prompt snapshot

Recorded verbatim as received by this session. It is the whole instruction set
for the change: no other prompt was issued, and nothing in it was supplied later
by a follow-up message. Provenance is `NOT_VERIFIED` because a committed file
cannot prove what any model actually received; the digest in the manifest only
proves this file has not changed since it was pinned.

---

Repo: `/d/code/AiMemoryBrainArchitecture` (Windows host, bash shell, Rust 1.100
available via `~/.cargo/bin`). Create your own worktree at `/d/wt/a903` from a
freshly fetched `origin/main`. Do not touch any other worktree under `/d/wt/`.
Do not edit `/d/code/AiMemoryBrainArchitecture` in place.

# What to fix

Issue **#903**: a test-isolation defect in `memory-event-store-sqlite` that makes
`cargo test --workspace` fail intermittently. It is the one thing standing
between the current state and a working workspace-test merge gate (#134).

The defect, already diagnosed in the issue and which you must verify yourself
before changing anything:

`crates/memory-event-store-sqlite/src/forget_fence.rs`, the `temp()` helper
around lines 318-322, builds a directory name from `std::env::temp_dir()` + a
caller-supplied `name` + `std::process::id()` + `SystemTime::now()` nanoseconds.
`fixture()` calls `temp("fixture")` — fixed name, fixed pid, wall-clock nanos as
the only uniqueness source. Two tests entering `fixture()` within the same clock
tick get the same directory. That is invisible at `fs::create_dir_all(&root)`
(succeeds on an existing directory) and fatal at `schema()`, which executes
`CREATE TABLE accepted_events(...)` with no `IF NOT EXISTS`, so the second caller
panics with:

```
SqliteFailure(Error { code: Unknown, extended_code: 1 }, Some("table accepted_events already exists"))
```

Observed only on Windows hosts, whose clock tick is coarse enough for concurrent
tests to collide; `ubuntu-latest` has a finer tick, which is why CI has stayed
green. A platform-dependent intermittent defect is the worst shape, so the fix
must remove the possibility rather than narrow it.

# The fix I am ruling for

Use the issue's **option 1**: append a `static COUNTER: AtomicU64` (or equivalent
`AtomicUsize`) to the generated name, incremented with
`fetch_add(1, Ordering::Relaxed)`. Rationale: smallest change, no new dependency,
no behavioural change to what the tests assert, and it makes the name unique
per-process regardless of clock granularity. Do **not** add a `tempfile`
dev-dependency (option 3) — that is a new dependency for something three lines
solve. Do **not** settle for option 2 (`create_dir` instead of `create_dir_all`)
on its own: it converts a silent collision into a loud panic, which is better
than silent but still leaves the suite flaky.

If the same `temp()` pattern exists in more than one place — check
`crates/memory-event-store-sqlite/src/forget_fence.rs` and also
`crates/memory-event-store-sqlite/tests/forget_fence.rs` and
`crates/memory-event-store-sqlite/tests/forget_fence_real_schema.rs`, which both
define a `temp()` of their own — apply the same counter treatment wherever the
uniqueness source is only name+pid+nanos. Report exactly which files you changed
and why each one needed it. If a given file's helper is already collision-free,
say so and leave it alone rather than changing it for symmetry.

Keep the change minimal and in the existing style. Leave a brief comment naming
the ceiling (the name is unique per process only, not across processes sharing a
temp dir) and the upgrade path.

# Verification — this is the whole point of the task, so do not skip it

1. **Prove the defect exists before you fix it.** On the unmodified tree, run the
   library tests repeatedly with default parallelism until you observe the
   failure, or state plainly that you could not reproduce it and give the number
   of attempts. The issue records roughly one failure in six runs on a Windows
   host. Use `cargo test -p memory-event-store-sqlite --lib` (the issue's evidence
   is that `--test-threads=1` passes 26/26 while default parallelism fails
   intermittently). Run it at least 10 times and report the pass/fail tally.
2. **Prove the fix removes it.** After the change, run the same command the same
   number of times and report the tally. A fix that cannot be shown to reduce the
   failure rate is not a fix.
3. **Prove you did not break the tests.** `cargo test -p memory-event-store-sqlite`
   must pass in full, and `cargo test --workspace --all-targets --no-fail-fast`
   must pass (this is the command the issue cares about). Report the exact totals,
   e.g. `53 targets, 793 tests, 793 pass, 0 fail`.
4. **A negative control for the fix itself.** Temporarily revert your counter
   line, confirm the failure rate returns (or that the same command reproduces a
   collision), then restore. If the collision is too infrequent to reproduce on
   demand, say so — do not fake a control.
5. `cargo fmt --check` and `cargo clippy --workspace --all-targets -- -D warnings`
   if clippy is installed; report the result. If clippy is unavailable, say so
   rather than claiming a pass.

Report raw numbers, not adjectives. "Green" without a count is not a result.

# Passing the gate on your own PR

`Session Evidence`, `Session Evidence self-test (base)` and
`Session Evidence self-test (head)` are all **required** status contexts on
`main`. Follow the merged precedent of PR #1013: add a non-empty session-evidence
document recording what you measured and what you changed, cited from the PR body
as `Session evidence reference(s): <path>`, alongside `Related issue(s): #903` and
`AI-assisted work: YES`. Read
`14-ai-development/work-items/AID-2026-059/session-evidence-799.md` and
`AID-2026-055/session-evidence-966.md` for the established shape, and check
whether `AID-2026-059/manifest.yaml`'s `session_evidence:` list needs an entry.

**Known blocker, do not work around it dishonestly:** the `Session Evidence`
verdict currently has an ordering defect (issue #1026) that blocks PRs whose
linked Issues all predate 2026-12-01; #903 was opened 2026-11-2x, so it may be
affected. Do **not** force the declaration to `NO` to get a green tick. If the
only remaining red is #1026 rather than your own content, say so explicitly —
another worker is fixing #1026 in parallel and your PR merges after that lands.

Also check whether your change trips the bilingual gate (`.md` files under
normative roots need `BILINGUAL-MANIFEST: COMPLETE`; `.rs` files do not) — read
`scripts/check_bilingual_docs.py` rather than guessing.

# Deliverable

Commit, push a branch, open a **ready** (not draft) PR against `main`. Report:

- PR number and head SHA
- the exact diff of every file you changed
- the pre-fix failure tally out of your attempts, the post-fix tally, and the
  workspace totals
- the negative control result
- fmt/clippy results
- every gate you read and its conclusion
- anything you could not reproduce or verify, stated plainly rather than
  smoothed over

Never claim a check is green without reading its conclusion.
