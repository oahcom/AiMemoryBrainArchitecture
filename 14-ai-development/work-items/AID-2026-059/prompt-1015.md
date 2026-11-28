---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      verification_status: Unverified
      last_verified_date: "2026-11-25"
      last_verification_note: "A transcription of the dispatch brief issued for Issue #1015. It was not captured from the model input channel, so the digest below pins these bytes and nothing about their fidelity."
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

# Dispatch brief for Issue #1015 — record it verbatim, do not summarise

Repo: `/d/code/AiMemoryBrainArchitecture` (Windows host, bash shell). Create your own
worktree at `/d/wt/a1015` from a freshly fetched `origin/main`. Do not touch any other
worktree under `/d/wt/`. Do not edit `/d/code/AiMemoryBrainArchitecture` in place.

## What to build

Issue **#1015**: `.github/workflows/session-evidence.yml` was rewritten into three jobs
by PR #1014 to fix a defect that had survived 18 consecutive failing runs. Nothing now
prevents someone collapsing it back, and the collapse is silent.

Current shape on `main` (verify it yourself, do not trust this):

| job id | checkout | purpose |
| --- | --- | --- |
| `self-test-trusted-base` | `ref: ${{ github.event.pull_request.base.sha }}` | the merged validator is not tampered with |
| `self-test-pr-head` | `actions/checkout@v4` with **no `ref:`** | the PR's own tests run and can fail |
| `validate` | `ref: ${{ github.event.pull_request.base.sha }}` | the verdict, independent of the head suite |

Each of the following regressions must be caught, because each was a real failure mode:

1. The three jobs are merged back into one → `validate` and the head self-test share a
   checkout.
2. `self-test-pr-head` gains `ref:` → it silently tests the base tree again, which is the
   exact defect #1014 fixed.
3. `validate` gains `needs: self-test-pr-head` → a PR can suppress its own verdict by
   deleting a test.

## Where it must live — this is the part that is easy to get wrong

Write a new script next to `scripts/check_declared_check_contexts.py` (read that file
first; reuse its parsing approach and its exit-code conventions). Suggested name:
`scripts/check_session_evidence_workflow_shape.py`. A companion test file alongside it,
in the same style as the existing `scripts/test_*.py` tests.

**It must NOT go in `tests/session_evidence/`.** That directory is checked out from the
**base** commit in CI by design, so a guard living there would itself be read from the
base tree and would never see a change to the workflow in the PR under test — it would be
unable to catch the very thing it exists to catch. The author of #1014 confirmed this
reasoning independently.

## It must actually execute, or it is worthless

Issue #925 in this repository records that four of fourteen gate scripts are never
executed by any workflow — a guard that never runs is indistinguishable from no guard. So:

- Wire the new script into an existing workflow as a step in a job that already runs on
  every PR. Prefer adding a step to the existing `Repository hygiene (hard gate)` job in
  `.github/workflows/repository-hygiene.yml` so that **no required-context name changes**
  — do not add a new job, and do not alter any existing job's `name:` field.
- Confirm from the workflow file that your step is inside a job that triggers on
  `pull_request`.

## The three assertions

1. All three job ids exist in `.github/workflows/session-evidence.yml`:
   `self-test-trusted-base`, `self-test-pr-head`, `validate`.
2. No checkout step inside the `self-test-pr-head` job carries a `ref:` key.
3. The `validate` job has no `needs:` key.

Each failure must exit non-zero and print a message naming the specific violation and the
job id — not a generic "shape check failed".

The repository has no YAML parser available (PyYAML and node `yaml` both failed to install
for a previous author), so `scripts/check_declared_check_contexts.py` uses regexes over the
raw text. Read it and follow the same approach. Do not add a dependency.

## Reverse-verification — mandatory

A guard tested only against the unmodified file proves nothing. For **each** of the three
assertions, mutate the workflow, run the script, and confirm it exits non-zero with the
expected message, then restore:

- delete the `self-test-pr-head:` block → assertion 1 must fire naming `self-test-pr-head`
- add `ref: ${{ github.event.pull_request.base.sha }}` to the head job's checkout →
  assertion 2 must fire
- add `needs: self-test-pr-head` to `validate` → assertion 3 must fire

Also confirm the **unmutated** file passes, otherwise the guard may be failing for an
unrelated reason and you would be reporting three false positives. Report each mutation,
the exit code, and the message.

## Passing the gate on your own PR

`Session Evidence`, `Session Evidence self-test (base)` and `Session Evidence self-test
(head)` are all **required** status contexts on `main` now, so your PR must satisfy them.
Follow the merged precedent of PR #1013:

- Add a non-empty session-evidence document under
  `14-ai-development/work-items/AID-2026-059/` (that work item is "Implement the AI session
  evidence gate specified by Issue #799" — the correct scope for a guard on that gate's
  workflow). Name it for issue 1015. It must record what you measured, what you changed,
  and what you could not verify.
- If `AID-2026-059/manifest.yaml` has a `session_evidence:` list, append an entry in the
  existing shape without restructuring the file.
- PR body must carry `Related issue(s): #1015`, `AI-assisted work: YES`,
  `Session evidence reference(s): <path you added>`, and `BILINGUAL-MANIFEST: COMPLETE` —
  but check `scripts/check_bilingual_docs.py` for what your specific paths actually require
  rather than assuming.

Note: `.github/` and `scripts/` are **not** normative roots, so `.py` and `.yml` files do
not trigger the bilingual requirement. The work-item `.md` you add **is** under a normative
root, so read the gate and satisfy it properly.

**Important known blocker:** the `Session Evidence` verdict step currently has an ordering
defect (issue #1026) that blocks PRs whose linked Issues all predate 2026-12-01. #1015 was
created today, so it is one of those. Do **not** work around it by forcing the declaration
to `NO`. If you cannot get the check green because of #1026 rather than your own content,
say so explicitly and stop — another worker is fixing #1026 in parallel, and your PR will
be merged after that lands.

## Deliverable

Commit, push a branch, open a **ready** (not draft) PR against `main`. Report:

- PR number and head SHA
- the new script's exact diff, and the workflow step you added (paste both)
- the three mutations, each with exit code and message
- confirmation that the unmutated file passes
- confirmation that your step sits inside a job that triggers on `pull_request`, quoting
  the surrounding YAML
- every gate you actually read and its conclusion
- anything you could not verify

Never claim a check is green without reading its conclusion.
