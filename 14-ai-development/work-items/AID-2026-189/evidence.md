---
document_metadata:
  domain: ai-development
  role: work-record
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
        - "14-ai-development/work-items/AID-2026-189/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Workflow edits read back from the committed blobs at the stated head; job ids and job display names compared before and after with a YAML parse of both sides. The two deferred defects are recorded from the dispatcher's measurements plus the repository's own checker sources; neither is claimed as fixed."
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
    canonical_scope: "Evidence for the AID-2026-189 CI leftover repair: fmt-job cache removal, head-SHA concurrency for two topic workflows, and two deferred CI dispatch defects"
    canonical_scope_id: "ai-development/aid-2026-189-ci-leftovers-evidence"
    canonical_scope_keywords:
      - "ci"
      - "cache"
      - "concurrency"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-189 — CI leftovers: dead fmt cache, two missing concurrency blocks, two recorded defects

## Scope and attribution

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`; base commit read at branch creation and again before merge (see manifest)
- Predecessor: AID-2026-115, PR #1322, merge commit `ac301e09799bcc094e015db4e12d2e6ff53d5010`
- Attribution: user-authorized operator (delegated by account owner). No natural-person Owner
  signature, acceptance or approval is asserted.
- This work item changes two workflow files and adds this registration record plus one INDEX
  row. It changes no job name, no job count, no required context, no checker semantics and no
  branch protection.

The predecessor added `concurrency` to eight required workflows and `Swatinem/rust-cache@v2`
to four Rust jobs. Two defects followed it: one job received a cache it can never use, and two
topic workflows that also carry a real branch trigger were left without `concurrency`. This
record fixes those two and records two further defects that must not be fixed by a worker.

## A. The fmt job's Rust cache could never hit

`gates.yml` job `fmt` ("Rust format (hard gate)") runs exactly one command:
`python3 scripts/check_fmt.py --expect "$GITHUB_SHA"`, which shells out to
`cargo fmt --all -- --check`. `cargo fmt` parses sources and rewrites or compares them; it
builds nothing. `Swatinem/rust-cache@v2` caches `~/.cargo/{registry,git}` and the `target/`
directory, neither of which this job populates, so every run restores nothing and saves
nothing — and pays a cache-service round trip plus the extra toolchain-probe step on every
pull request.

Step list, read from both sides with a YAML parse of `jobs.fmt.steps`:

| # | Before (`origin/main`, after AID-2026-115) | After (this change) |
|---|---|---|
| 1 | `actions/checkout@v4` | `actions/checkout@v4` |
| 2 | `dtolnay/rust-toolchain@stable` (`components: rustfmt`) | `dtolnay/rust-toolchain@stable` (`components: rustfmt`) |
| 3 | `Record resolved Rust toolchain version` (`id: rust-toolchain-version`) | — removed |
| 4 | `Cache Rust dependencies and build artifacts` (`Swatinem/rust-cache@v2`, `shared-key: gates-fmt`) | — removed |
| 5 | `Verify repository formatting at this commit` | `Verify repository formatting at this commit` |

A three-line comment takes the place of the two removed steps, stating that the cache is
absent on purpose and why, so the next session does not restore it as an "omission".

Deliberately unchanged, because those jobs do compile and their caches do hit:

- `clippy` — keeps `Record resolved Rust toolchain version`, `Swatinem/rust-cache@v2`,
  `Report the toolchain source`, then `cargo clippy --workspace --all-targets -- -D warnings`.
- `doctest` — keeps both steps, then `cargo test --workspace --doc --no-fail-fast`.
- `rust-phase1.yml` job `rust-workspace-test` — keeps both steps; it builds and tests.

Timing: the dispatcher measured the `fmt` job at 8s before AID-2026-115 and observed 21s after
it on at least one run. That pair is dispatcher-measured, not re-measured here; what this
change verifies locally is the step list, not a wall-clock delta. A post-merge timing is
whatever the platform reports, and is not claimed.

## B. Two workflows were missed by the concurrency sweep

`h-applied-delivery-evidence-conformance.yml` and `publication-protocol-reference-model.yml`
are both `push` on a real topic branch **and** `pull_request` on `main`. The AID-2026-115 sweep
covered the eight required contexts and did not reach these two, so a rapid push sequence on
either topic branch queued a run per push.

Both files now carry, as the first top-level key after the `name:` line:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
  cancel-in-progress: true
```

Verbatim from `h-applied-delivery-evidence-conformance.yml` (lines 1-9):

```yaml
name: H Applied Delivery Evidence Conformance
# revision: Applied Delivery Evidence message family 1.0.0; separate from Unified 1.2.15 Gateway C Provider Outcome

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
  cancel-in-progress: true

on:
```

Verbatim from `publication-protocol-reference-model.yml` (lines 1-8):

```yaml
name: Publication Protocol Reference Model

concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.head.sha || github.sha }}
  cancel-in-progress: true

on:
```

`head.sha` and not `sha`: on a `pull_request` event `github.sha` is the synthetic merge commit,
which changes whenever the base moves, so a `sha`-keyed group would let a base update create a
second group for the same pull-request head and defeat the cancellation. `head.sha` is stable
across base updates and identical for the `push` shape of the same commit, which is why the
`|| github.sha` fallback is used for events with no pull request.

Job sets compared with a YAML parse of both revisions — identical, no rename, no merge, no
addition, no removal:

| Workflow | Jobs before | Jobs after |
|---|---|---|
| `h-applied-delivery-evidence-conformance.yml` | `applied-delivery-evidence` | `applied-delivery-evidence` |
| `publication-protocol-reference-model.yml` | `publication-protocol-reference-model` | `publication-protocol-reference-model` |
| `gates.yml` (control) | `protocol-index`, `conformance`, `schema-nonempty`, `bilingual`, `clippy`, `doctest`, `fmt` | same seven |

Neither of these two workflows produces one of the sixteen declared required contexts, so this
block cannot move a required check. `gates.yml` already carried the block from AID-2026-115 and
is unchanged here.

## C. Two defects recorded, not repaired — `DEFERRED_TO_OWNER`

Both items below would require changing what a **required context** produces, or how branch
protection and `PR-GOVERNANCE-001` §7 describe it. A worker that edits workflows may not do
that, so both are recorded with their root cause and at least two candidate fixes.

### C1 `DEFERRED_TO_OWNER` — `ready_for_review` dispatches a second run that nothing can cancel

**Observed.** Four workflows subscribe to `ready_for_review` in `pull_request.types`:

| Workflow | `types:` line | Required context(s) it produces |
|---|---|---|
| `bilingual-docs.yml` | 9 | `Bilingual docs coverage (ratchet)` |
| `branch-freshness.yml` | 19 | `Branch freshness vs base` |
| `document-management.yml` | 9 | `GOV-DOC-001 structural checks`, `GOV-DOC-002 metadata checks` |
| `repository-hygiene.yml` | 9 | `Repository hygiene (hard gate)` |

The dispatcher measured 4/4 of them double-dispatching on a draft-to-ready transition: one
completed run from `opened`/`synchronize` and a second, complete run from `ready_for_review`,
for the same head SHA, producing two sets of check runs per context.

**Root cause.** `ready_for_review` is a new event for an unchanged head SHA. By the time it
arrives, the earlier run for that SHA is already **completed**, and `cancel-in-progress` only
cancels runs that are `queued` or `in_progress` in the same concurrency group. A completed run
is immutable and is not a cancellation candidate, so the concurrency block added by
AID-2026-115 cannot suppress this duplicate — the group is right and the mechanism is
insufficient. The duplicate is therefore structural, not a concurrency misconfiguration.

**Candidate fixes (not applied).**

1. **Drop the trigger.** Remove `ready_for_review` from `pull_request.types` in the four
   workflows, leaving `opened`, `synchronize`, `reopened` (and `edited` where it is already
   there). A draft PR still gets a run from `opened`; every later push is covered by
   `synchronize`; the ready transition adds no new commit, so it adds no new fact to check.
   Cost: a PR opened as a draft whose gate failed, then marked ready with no push, relies on
   the `opened` run's conclusion — which is the correct conclusion for that head anyway.
2. **Skip the duplicate at job level.** Keep the type and add
   `if: github.event.action != 'ready_for_review'` to each job. Cost: a skipped job still
   reports a check run with conclusion `skipped`, and a **required** context that reports
   `skipped` does not satisfy branch protection — so this variant is only usable for the
   non-required contexts, and for the four above it converts a duplicate run into a blocking
   one. It is listed because it is the obvious first idea and it is wrong for these four.
3. **Gate the dispatch on the API.** Keep the type and let the workflow's first step query
   whether a completed run already exists for the same head SHA, exiting early if so. Cost: a
   token-scoped API call on every ready transition, and a second failure mode (rate limit or
   unreadable payload) that must fail closed rather than green.

Recommendation for the Owner: (1). It is the only one that removes work without adding a new
state to reason about, and it changes no required context name.

### C2 `DEFERRED_TO_OWNER` — two required contexts execute byte-identical commands

**Observed.** Two required contexts duplicate another required context's command verbatim:

| Command | Context A (workflow / job) | Context B (workflow / job) |
|---|---|---|
| `cargo test --workspace --doc --no-fail-fast` | `Rust doctests (hard gate)` — `gates.yml` job `doctest` | `rust-workspace-test` — `rust-phase1.yml` job `rust-workspace-test` |
| `python3 scripts/check_fmt.py --expect "$GITHUB_SHA"` | `Rust format (hard gate)` — `gates.yml` job `fmt` | `rust-workspace-test` — `rust-phase1.yml` job `rust-workspace-test` |

Both commands are also the ones this change removed the cache around (the first is cached
legitimately, the second has no cache to use).

**Root cause.** The duplication is cheap to see and expensive to remove, because
`scripts/check_declared_check_contexts.py` enforces a **one-job-one-context** relation in both
directions: every declared context must be produced by some job, and every protected context
must be declared. Folding `fmt` and `doctest` into `rust-workspace-test` — the obvious
de-duplication — deletes the jobs that produce `Rust format (hard gate)` and
`Rust doctests (hard gate)`. The declared→produced half then fails, `repository-hygiene` goes
red, and branch protection still requires two contexts that no job emits, so every merge is
blocked until the declaration, the protection payload and the document are changed together.
A green merge is not available to a worker here; only the Owner can move that trio at once.

**Candidate fixes (not applied).**

1. **Delete the duplicate steps, keep both contexts.** Remove the two duplicated steps from
   `rust-phase1.yml` job `rust-workspace-test` (they are redundant with `gates.yml`), leaving
   the job to do `cargo test --workspace --all-targets` and its self-test. Every context keeps
   its name and keeps reporting; the duplicate work disappears. Cost: `rust-workspace-test`
   would no longer independently reproduce formatting and doctests, so a `gates.yml` outage
   would no longer be covered by a second producer.
2. **Retire the redundant contexts.** Remove `Rust format (hard gate)` and
   `Rust doctests (hard gate)` from the declaration in `PR-GOVERNANCE-001` §7 **and** from the
   branch-protection payload **and** from the producing jobs in one Owner-authorized change.
   Cost: three coordinated edits, and the protection payload is only writable with an
   administration-scoped credential the CI token vocabulary cannot express.
3. **Make the second producer non-identical.** Have `rust-workspace-test` run
   `cargo test --workspace --doc` (no `--no-fail-fast`) or scope it to a subset. Cost: the two
   contexts then differ in behaviour for the same name-adjacent intent, and the divergence is
   invisible unless someone diffs the workflow files.

Recommendation for the Owner: (1) if the duplication is judged a real cost; otherwise record
the duplication as accepted and say so here, so a future session stops re-finding it.

## What this record does not claim

- No timing improvement is claimed for the `fmt` job. The step list is verified; the wall-clock
  effect is whatever the platform reports after merge.
- No required context was added, removed, renamed or merged, and no checker semantics changed.
- The two deferred items are **not fixed**. Neither `ready_for_review` dispatch nor the
  duplicated required contexts changed in this branch.
- Nothing here is Owner acceptance, review independence or normative approval.
