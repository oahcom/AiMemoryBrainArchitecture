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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The trigger block, the live body read and the guard's silence on `types:` were each re-read on 2026-11-25 from origin/main at 30c7277e; every exit code quoted below was produced by running the guard, not inferred from its source."
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

# WO — Make a PR body edit re-run the Session Evidence gate (#1074)

Scope: add `edited` to the trigger of `.github/workflows/session-evidence.yml`,
add a shape-guard rule that the trigger declares it, and add the tests that make
a revert of either one fail the suite.

## The defect

`Session Evidence` is one of the 16 required contexts on `main`. Its verdict
authorises the merge. It is computed from `pr.body`, fetched live from the API:

```
scripts/governance/session_evidence/validate.py:1853
    body = pr.get("body") or ""
```

inside `_load_context()`, which fetches `/repos/{repo}/pulls/{n}`. Nothing pins
the text: there is no digest of the body anywhere in the validator.

The workflow declares `on: pull_request:` with no `types:`. GitHub's default
`pull_request` activity types are `opened`, `synchronize`, `reopened`.
**`edited` is not among them.** So:

1. a green run judges body revision A;
2. the body is edited to revision B, which the gate would refuse;
3. no run is scheduled;
4. the PR merges carrying a `success` that describes text the repository no
   longer contains.

`.github/workflows/bilingual-docs.yml:5` already declares
`types: [opened, synchronize, reopened, edited, ready_for_review]`, so this is
not a platform limitation anyone has to accept — the required gate is the one
workflow in the directory that omits it.

## Scope of the fix, stated precisely

`edited` closes one half: **a stale verdict no longer survives an edit without a
re-run.** It does not close the other half: **an edit that lands after the last
run and before the merge still races the merge.** Closing that needs a merge
queue, a verdict that depends on something immutable (the commit), or an `if:`
guard comparing the body hash. This work item does not claim to close it.

No `concurrency:` block exists in the workflow and none is added: with
`cancel-in-progress` absent, two runs on the same PR serialise rather than
cancel, and adding a group is a separate decision with its own review.
`git grep -n concurrency .github/workflows/session-evidence.yml` returns
nothing.

## The guard

`scripts/check_session_evidence_workflow_shape.py` checks the job graph and, as
of this work item, the trigger block. It previously contained **zero** references
to `on:`, `pull_request`, `types` or `trigger` — the trigger was unconstrained,
so adding `edited` once would have been revertible in silence.

The new rule must read both YAML spellings, because the file may be written
either way and rejecting a correct one is the bug class #1045 fixed in this same
script for `needs:`:

```yaml
    types: [opened, synchronize, reopened, edited]      # flow form
```

```yaml
    types:                                            # block form
      - opened
      - synchronize
      - reopened
      - edited
```

A missing `types:` key is a violation, not a pass: the default set omits
`edited`, which is the defect.

## Acceptance asked for

1. `.github/workflows/session-evidence.yml` declares
   `types: [opened, synchronize, reopened, edited]` — the full default set
   written out, so the behaviour is stated rather than inherited.
2. Flow-form `types:` without `edited` → exit 1, message names `edited` and the
   `types:` line number.
3. Flow-form `types:` with `edited` → exit 0.
4. Block-form `types:` with `edited` → exit 0. This is the anti-regression test.
5. `types:` absent → exit 1, message names the missing key and `edited`.
6. Each new test fails with `AssertionError` under a revert of the rule, not a
   traceback and not an `ImportError`.
7. The 12 tests already in the file pass unmodified; the suite runs 16.
8. `python scripts/check_session_evidence_workflow_shape.py` → exit 0 on the
   unmutated repository.

## Excluded, and stated as excluded

- `scripts/governance/session_evidence/validate.py`. Reading the body live is
  correct for a gate that runs on the current state; the missing trigger is the
  defect. The body digest the Issue also asks for is a second change with its own
  scope and is not done here.
- `crates/`.
- Any `concurrency:` setting. See above.
