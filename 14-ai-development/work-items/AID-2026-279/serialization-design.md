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
        - "14-ai-development/work-items/AID-2026-279/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "The event-to-ref mapping is wired in .github/workflows/document-management.yml; merge_group behaviour is not yet exercised because the merge queue is not enabled on this repository."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "work-item-uniqueness"
      - "merge-group"
      - "serialization"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-279 — Merge-time serialization design

**Attribution:** user-authorized operator (delegated by account owner)
**Date:** 2026-11-27
**Issue:** #1341

## The failure being serialized away

A required check that runs only on `pull_request` evaluates each candidate
against the base commit recorded when that pull request was opened, or against
whatever the base branch looked like at that moment. Two candidates that both
introduce `AID-2026-NNN/` therefore each see a base without it, each pass, and
the second merge creates a duplicate record. Nothing in a `pull_request` run can
prevent this: the event is per-branch, and the branches do not see each other.

Serialization needs a place where candidates are evaluated **one at a time
against the tree the previous candidate produced**. That is the merge queue.

## Wiring

`.github/workflows/document-management.yml` now listens to three event kinds and
maps each to the tree pair it actually means:

| Event | `--base` | `--head` |
|---|---|---|
| `pull_request` | refreshed `origin/main` SHA (not `event.pull_request.base.sha`) | `github.event.pull_request.head.sha` |
| `merge_group` (`checks_requested`) | refreshed `origin/main` SHA | `github.event.merge_group.head_sha` |
| `push` (main) | `github.event.before` | `github.event.after` |

The target branch is refreshed with
`git fetch --no-tags origin +refs/heads/main:refs/remotes/origin/main` in a step
immediately before the decision step, and the SHA that fetch resolved is the
only value the checker ever receives as `--base`. The step writes `base_sha` and
`head_sha` to `$GITHUB_OUTPUT` so the pair used for the verdict is auditable
from the run log. A failed fetch, an unresolvable `origin/main`, or a value that
is not 40 hex characters exits 2 (INCOMPLETE) — there is no fallback to
`github.event.pull_request.base.sha`, because a stale target is exactly the
failure the gate exists to catch. (Semantics absorbed from #1422 / AID-2026-262,
per the Owner ruling that #1413 is the single carrier of work-item uniqueness.)

An empty ref, the all-zero `before` of a first push, or an unknown event also
exits 2 before the checker runs. There is no fallback to `github.sha`, because
`github.sha` on a `pull_request` event is the synthetic merge commit, which would
hide exactly the conflict the gate exists to find.

Both events call the same checker with the same semantics. The checker does not
know which event produced its arguments, so a `merge_group` run and a
`pull_request` run cannot drift apart.

## What the checker does with the pair

```
candidate_ids = ls-tree --head  -- 14-ai-development/work-items
target_ids    = ls-tree --base  -- 14-ai-development/work-items
new_ids       = candidate_ids - target_ids
```

* `new_ids` must be unoccupied on the target tree and unclaimed in the registry.
* For an id present on both sides, the fork point decides only *who moved a
  path*, never occupancy:
  * the id existed at the fork point — the candidate inherited the record, so
    added files are additive and a modified or deleted path is an edit to a
    record the target owns;
  * the id did not exist at the fork point — the candidate introduced it
    independently, so every path it contributes under that id is a competing
    claim, additions included;
  * the candidate is behind the target on an inherited record and changed
    nothing there — not a claim. That is a freshness failure, reported by the
    separate branch-freshness check.

The old algorithm asked `merge-base(base, head)` what the candidate had
introduced. After the candidate merged the target branch, that set was empty and
the duplicate claim passed silently. Reading the two trees independently removes
the merge base from the decision entirely.

## Invariants preserved

* Job display name is unchanged (`GOV-DOC-002 metadata checks`), so the required
  status context still matches. Only steps inside the job were added.
* No `paths:` filter on the workflow or the job: a required context that is
  skipped reports "expected" forever and blocks the merge.
* No `continue-on-error`: a violation must fail the merge group.
* `fetch-depth: 0` already present, so `--base`/`--head` are always resolvable
  locally; an unresolvable ref is exit 2, never a pass.
* The refresh contract itself is asserted by
  `scripts/ci/test_work_item_uniqueness.py` (`WorkflowRefreshContractTests`):
  step order, the exact fetch refspec, `exit 2` on failure, the `$GITHUB_OUTPUT`
  keys, and the absence of `pull_request.base.sha` in the decision step. A later
  edit cannot quietly re-point `--base` at the stale event SHA.

## Why the merge queue is the serialization point

A `merge_group` run is created when the queue assembles a batch on top of the
current target tip. The queue re-runs required checks on that assembled head
before merging. A candidate that passed on its own branch is therefore
re-evaluated against a target tree that includes whatever merged in front of it,
and the second claimant is rejected at that point — before the merge, not after.

Enabling the merge queue is a repository setting, not a workflow change. Until
it is enabled, the `merge_group` wiring is inert and the `pull_request` run is
still the only enforcement point; that is recorded as BLOCKED in
`race-test-report.md`.
