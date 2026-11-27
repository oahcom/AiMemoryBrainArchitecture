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
      last_verification_note: "The four tree scenarios were executed locally against real temporary Git repositories. The merge-queue race case is BLOCKED: the repository has no merge queue enabled, so no merge_group run exists to observe."
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
      - "race-test"
      - "regression-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-279 — Race and regression test report

**Attribution:** user-authorized operator (delegated by account owner)
**Date:** 2026-11-27
**Issue:** #1341
**Local interpreter:** Python 3.12.3 (Windows)
**Suite:** `scripts/ci/test_work_item_uniqueness.py` — 14 tests, all passing;
`scripts/ci/test_work_item_registry.py` — 15 tests, all passing.

Every case builds a real temporary Git repository. The gate reads trees, so
object mocks would prove nothing about it.

## Before and after

| # | Scenario | Old algorithm | New algorithm |
|---|---|---|---|
| 1 | Target branch already has the id; candidate merged the target branch and keeps its own copy of the record | `introduced=0` → PASS (wrong) | VIOLATION (exit 1) |
| 2 | Same id, conflict resolved on the target side, target branch merged again | `introduced=0` → PASS (wrong) | VIOLATION (exit 1) |
| 3 | Pull-request base behind the latest target branch, which already has the id | `introduced=1 occupied=0` → PASS (wrong) | VIOLATION (exit 1) |
| 4 | New file added beneath an id that already exists on the target branch | PASS | PASS (exit 0) |

The old algorithm asked `merge-base(base, head)` what the candidate had
introduced. Cases 1 and 2 collapse that set to empty; case 3 compares against a
stale base. The new algorithm reads both trees independently and never consults
a merge base.

## Scenario 1 — merged target, same directory

```
$ python scripts/ci/check_work_item_uniqueness.py --base <target> --head <merge commit>
VIOLATION: 14-ai-development/work-items/AID-2026-279 has modified or deleted paths; the target branch already owns this work item, so only added files are additive
WORK-ITEM UNIQUENESS: VIOLATION (base=... candidate_ids=1 target_ids=1 new_ids=0 modified_under_shared=1 registry=base ...)
```

## Scenario 2 — conflict resolved on the target side, merged again

```
$ python scripts/ci/check_work_item_uniqueness.py --base <target> --head <re-merged commit>
VIOLATION: 14-ai-development/work-items/AID-2026-279 has modified or deleted paths; the target branch already owns this work item, so only added files are additive
WORK-ITEM UNIQUENESS: VIOLATION (... new_ids=0 modified_under_shared=1 ...)
```

Resolving `manifest.yaml` on the target side does not launder the claim: the
candidate's own evidence file still overwrites the target's record, and merging
the target branch again does not remove it.

## Scenario 3 — stale pull-request base

```
$ python scripts/ci/check_work_item_uniqueness.py --base <latest target> --head <candidate>
VIOLATION: 14-ai-development/work-items/AID-2026-279 has modified or deleted paths; the target branch already owns this work item, so only added files are additive
WORK-ITEM UNIQUENESS: VIOLATION (... new_ids=0 modified_under_shared=1 ...)
```

## Scenario 4 — additive file under an existing id

```
$ python scripts/ci/check_work_item_uniqueness.py --base <target> --head <candidate>
WORK-ITEM UNIQUENESS: PASS (... new_ids=0 modified_under_shared=0 ...)
```

## Registry cases

| Case | Expected | Result |
|---|---|---|
| CLAIMED created, schema valid | exit 0 | exit 0 |
| CLAIMED → MERGED (`--previous`) | exit 0 | exit 0 |
| CLAIMED → ABANDONED (`--previous`) | exit 0 | exit 0 |
| MERGED → ABANDONED | exit 1 | exit 1 |
| MERGED id re-claimed by a second pull request | exit 1 | exit 1 |
| Two pull requests CLAIMED for one id | exit 1 | exit 1 |
| Row deleted between revisions | exit 1 | exit 1 |
| New row entering as MERGED | exit 1 | exit 1 |
| Missing ledger | exit 2 | exit 2 |
| `--check-live-prs` with no token | exit 2 | exit 2 |

## Race at merge time — BLOCKED

**Status: BLOCKED. The merge queue is not enabled on
`oahcom/AiMemoryBrainArchitecture`, so no `merge_group` run can be produced and
no real two-candidate race can be observed end to end.**

What is verified instead:

1. The `merge_group` event is wired (`on: merge_group: types:
   [checks_requested]`) and maps `--base` to
   `github.event.merge_group.base_sha` and `--head` to
   `github.event.merge_group.head_sha`. The step exits 2 on an empty or
   all-zero ref, so an inert queue cannot silently pass.
2. The race is reproduced locally with two branches off one base, the first
   merged, and the second re-checked against the new target tip:

```
$ python scripts/ci/check_work_item_uniqueness.py --base <fork> --head <candidate A>
WORK-ITEM UNIQUENESS: PASS (new_ids=1 ...)
$ python scripts/ci/check_work_item_uniqueness.py --base <tip after A> --head <candidate B>
VIOLATION: 14-ai-development/work-items/AID-2026-279 has modified or deleted paths; ...
WORK-ITEM UNIQUENESS: VIOLATION (...)
```

The second candidate fails because the target tree now owns the id. This is the
same evaluation the queue performs; what is missing is only the queue's
scheduling, not the decision.

Unblocking requires a repository setting (Settings → Rules → Merge queue), which
is outside this work item's boundary. No branch-protection change is made here.
