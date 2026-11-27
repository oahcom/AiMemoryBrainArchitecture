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
        - "14-ai-development/work-items/AID-2026-262/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local test runs are recorded verbatim. No CI run, merge SHA, or platform-side branch-protection read is claimed; the serialization boundary is declared unproven rather than asserted."
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
      - "merge-broker"
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

# AID-2026-262 鈥?Evidence

**Attribution:** user-authorized operator (delegated by account owner)
**Date:** 2026-11-27
**Issues:** #1331 (defect, mechanism selection), #1341 (implementation issue, acceptance table)
**Branch base:** `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028` (`origin/main`, merge of PR #1372)

## 1. What this work item is, and what it deliberately is not

Option (d) has two halves. The first 鈥?a checker that decides "is this newly
introduced work-item directory already occupied on the latest target branch" 鈥?was merged into `main` by AID-2026-279 (`feat(ci): enforce merge-time work-item
uniqueness`, PR #1372, commit `84790d36`, wiring in
`.github/workflows/document-management.yml` lines 32-46). The second 鈥?a
**serialized merge boundary** that evaluates every candidate against the main it
will land on and merges with the head it judged 鈥?is not on `main`. AID-2026-279
states the gap itself:

> The branch-protection /protection endpoint returned HTTP 403 to this
> connection, so strict and enforce_admins are not asserted. Merge serialization
> through strict freshness remains unverified until those two fields can be
> independently read.
> 鈥?`14-ai-development/work-items/AID-2026-279/evidence.md`, section "Serialization mechanism"

This work item therefore adds **no second checker**. A second copy of the same
rule under a second name is the defect #1331 reports, not a fix for it. It adds
the broker that calls the merged checker, and it records which of the eight
acceptance rows are actually established.

## 2. Option (d), verbatim

Source: `https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/issues/1331/comments`
(comment id `3586480262`, author `oahcom`, created `2026-11-26T18:08:33Z`),
retrieved 2026-11-27 by this session before the REST quota was exhausted.

> ## Owner decision recorded 鈥?Option (d) selected
>
> Owner adjudication, 2026-11-27. The mechanism chosen is a fourth option, not one of the three listed above.
>
> **Option (d): a serialized, merge-time work-item uniqueness gate.**
>
> The gate evaluates the candidate merge against the latest target-branch state, with merges serialized so that two concurrent pull requests cannot both validate against the same obsolete base. It must distinguish two cases:
>
> | Case | Required behaviour |
> |---|---|
> | New work-item directory | Reject if the ID is already occupied on the latest target branch. |
> | Existing work-item directory | Permit legitimate additive files under that directory; an added file is not a duplicate work-item claim. |
>
> This places uniqueness enforcement at the merge boundary, which is the only point that sees the real base, instead of at branch-local validation, which cannot see a sibling claim.
>
> ### Options (a), (b), (c) 鈥?not selected as standalone solutions
>
> - **(a) a shared reservation registry**: needs reservation lifecycle and concurrency semantics of its own, so it adds a second source of truth to keep consistent with the branch.
> - **(b) base-relative validation alone**: without serialization, two PRs can both pass against the same base and then race to merge 鈥?the defect survives.
> - **(c) post-collision arbitration**: decides who yields after the collision has already happened, which is the current situation and is precisely what this issue reports.
>
> ### Status of this issue
>
> **Open.** Selecting a mechanism does not close the defect. This issue closes only when an implementation exists and the acceptance evidence below is delivered, per the implementation issue raised for it.
>
> ### Why the diagnostic in the original report was incomplete
>
> The root cause is not that IDs are allocated carelessly. It is that uniqueness is enforced only within a single tree, while branches independently introduce directories, and nothing serialises the merge boundary. Five collisions in one batch is the expected output of that design, not a run of bad luck.

## 3. Issue #1341 body, verbatim

Source: `https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/issues/1341`,
retrieved 2026-11-27 by this session before the REST quota was exhausted.

> ## Task
>
> Implement Option (d) as selected in #1331 on 2026-11-27: a **serialized, merge-time work-item uniqueness gate**. #1331 stays open until this issue's acceptance evidence is delivered.
>
> This issue exists because the defect is a mechanism, not an incident. Five open pull requests collided with work items already on `main` in a single batch, and the two previous reports (#1096, #1236) were both closed by renumbering the individual claimants without changing how IDs are allocated.
>
> ## Contract to implement
>
> | Case | Required behaviour |
> |---|---|
> | New work-item directory introduced by the candidate merge | Reject if that ID is already occupied on the latest target-branch state |
> | New files under an existing work-item directory | Accept; an additive file is not a duplicate work-item claim |
>
> The gate's authority is the merge candidate evaluated against the **latest** target branch, not an earlier branch HEAD and not the branch's own base.
>
> ## Acceptance evidence
>
> | Evidence | Required proof |
> |---|---|
> | Contract | Explicit definition of new-directory uniqueness and existing-directory additive changes |
> | Serialization | Proof that concurrent PR merges cannot both validate against the same stale base |
> | Positive test | A new, unoccupied work-item ID is accepted |
> | Negative test | A new directory whose ID already exists on the latest base is rejected |
> | Additive test | New files under an existing work-item directory are accepted |
> | Race test | Two PRs independently introducing the same ID cannot both merge |
> | Exact-Head test | The uniqueness result is associated with the actual merge candidate, not an earlier branch HEAD |
> | Regression evidence | Existing traceability and repository hygiene checks continue to pass |
>
> ## Delivery constraints
>
> - Implementation, tests and independent review must come from a session **other than the coordinating session**. The coordinating session writes no implementation code.
> - Independent review must be of the exact final HEAD, not of an earlier revision.
> - Green means the eight rows above are demonstrated. A gate that merely runs is not evidence that it rejects anything.
>
> ## Out of scope
>
> Retroactively renumbering the existing collisions. Those are handled per PR in #1332.

## 4. What was built

| File | Change | Why |
|---|---|---|
| `.github/workflows/work-item-merge-broker.yml` | new | The serialized merge boundary: `labeled`/`workflow_dispatch` trigger, `concurrency: main-work-item-merge-broker`, `cancel-in-progress: false`, re-enumeration of open `merge-ready` pull requests, per-candidate re-read of main/head/checks/merge candidate, `sha=<head>` pinned merge. |
| `scripts/ci/test_work_item_merge_broker.py` | new | 11 tests: 7 structural assertions on the workflow, 4 composition tests that drive the merged AID-2026-279 checker through the exact two references the broker passes it. |
| `14-ai-development/work-items/AID-2026-262/*` | new | Registration, prompt snapshot, session evidence, this record. |
| `14-ai-development/work-items/INDEX.md` | modified | One row. |

Not changed: `scripts/ci/check_work_item_uniqueness.py`, its tests, any
existing workflow, the required-context set, branch protection.

### 4.1 Why the broker judges the head and records the candidate tree

The broker computes the merge candidate itself:

```
tree=$(git merge-tree --write-tree --no-messages "$base_sha" "$head_sha")
```

A non-zero exit means the candidate has no tree at all (add/add conflict on the
same path), and the pull request is rejected without a uniqueness verdict 鈥?there is nothing to judge.

When the candidate does exist, `git merge-tree` guarantees it is the union of
`main` and the head with no conflict, so the directories the candidate
*introduces* are exactly the directories the head introduces. The merged
checker is therefore called with `--base <latest main> --head <head>`; passing
it a tree object is not possible (`rev-parse <ref>^{commit}` fails on a tree) and
would be a lie about what was read. The candidate tree OID is printed in the run
log next to `base` and `head`, so the association between the verdict and the
merge that followed is auditable.

## 5. Acceptance evidence 鈥?row by row

Legend: **ACQUIRED** = demonstrated by an artifact in this repository at this
head. **NOT ACQUIRED** = not demonstrated. Nothing below is marked acquired on
the strength of a gate that merely ran.

| # | Evidence | Status | Artifact / reason |
|---|---|---|---|
| 1 | Contract | ACQUIRED | Section 2 above is the Owner decision verbatim; section 3 is the implementation issue verbatim. The two cases are implemented by `scripts/ci/check_work_item_uniqueness.py` (`introduced_dirs` filtered by `exists(merge_base, directory)`, occupancy by `exists(base, path)`) and re-stated in the broker's rejection paths. |
| 2 | Serialization | **NOT ACQUIRED** | `BROKER_SERIALIZATION_UNPROVEN`. The workflow serialises its own runs and re-reads main before every merge, but nothing on the platform restricts `main` to this path. Section 6 records what would close this row. |
| 3 | Positive test | ACQUIRED | `scripts/ci/test_work_item_merge_broker.py::test_unoccupied_new_directory_is_accepted` (exit 0, `introduced=1 occupied=0`) and, from AID-2026-279, `test_new_unoccupied_directory_passes`. Raw output in section 7. |
| 4 | Negative test | ACQUIRED | `test_same_id_after_the_first_merge_is_rejected` (exit 1, `VIOLATION`) and AID-2026-279's `test_occupied_directory_is_rejected`. |
| 5 | Additive test | ACQUIRED | `test_additive_file_under_existing_directory_is_accepted` (exit 0, `introduced=0 occupied=0`) and AID-2026-279's `test_additive_file_under_existing_directory_passes`. |
| 6 | Race test | **PARTIAL** | The gate is shown to reject the second claimant once main has advanced (`test_same_id_after_the_first_merge_is_rejected`, which first shows both candidates passing against the shared base). That is the gate's half. The other half 鈥?that two broker runs cannot interleave 鈥?is not demonstrated: it needs a real run with two `merge-ready` pull requests, and no such run exists. |
| 7 | Exact-Head test | **PARTIAL** | The broker re-reads the head, aborts when the API head and the fetched head disagree, and passes `sha=<head_sha>` to the merge API so a head that moved is refused rather than merged unevaluated. That is structural: the assertion lives in `test_judges_a_fresh_merge_candidate_and_pins_the_head`, and no live merge has exercised it. |
| 8 | Regression evidence | **PARTIAL** | `check_traceability.py --index-only` and `check_repository_hygiene.py` were executed locally on this head; raw output in section 7. No CI run is claimed for this head. |

Rows 2, 6, 7, 8 are the reason this pull request is a draft and #1341 stays
open.

## 6. `BROKER_SERIALIZATION_UNPROVEN`

The requirement is that two concurrent pull requests cannot both validate
against the same obsolete base. Three things are needed for that, and this
change supplies only the first:

1. **Serialised evaluation.** Supplied: one `concurrency` group with
   `cancel-in-progress: false`, and a re-read of `origin/main` at the top of
   every iteration.
2. **Evaluation against the merge that will happen.** Supplied: the candidate
   tree is computed against the `main` that exists at that moment, and the merge
   call names the exact head SHA.
3. **No other path into `main`.** **Not supplied.** Branch protection would have
   to require a context produced by this workflow 鈥?and this workflow produces
   no required context by design (adding one is out of scope for this work
   item). Any actor who can merge a pull request can merge it without the
   broker, after the required contexts pass.

The in-repository record of the protection payload is dated and partial:
`14-ai-development/PR-GOVERNANCE-001.md` records, measured 2026-11-25, sixteen
required contexts, `strict: true`, `enforce_admins: {enabled: true}`,
`allow_force_pushes: {enabled: false}`, `allow_deletions: {enabled: false}`, and
no `required_pull_request_reviews`. `strict: true` would force a pull request to
be up to date with `main` before merging, which is a real serialisation
mechanism 鈥?but it is a *different* mechanism from this broker, it was not read
by this session (the REST quota was exhausted; `GET /branches/main/protection`
returned 403), and AID-2026-279 already records that it could not read it either.
Reading a 2026-11-25 document is not a 2026-11-27 measurement.

What would close row 2, in order of cost:

- Require a context produced by this workflow on `main` **and** forbid direct
  pushes; then a merge that skips the broker fails the required check. This is a
  branch-protection change and needs the Owner, not this pull request.
- Or run the merge through a GitHub merge queue, which is serialised by the
  platform rather than by a `concurrency` group.

Until one of those exists, the correct reading of a green broker run is "this
pull request was judged against the main it merged into", not "concurrent
merges are impossible".

## 7. Raw local output

Host: Windows, Python 3.12.3, git 2.56.1. `python3` is a Microsoft Store stub on
this host (exit 9009), so AID-2026-279's own tests cannot run here; they use
`sys.executable` in this work item's tests instead.

```
$ python scripts/ci/test_work_item_merge_broker.py
test_triggers_are_the_label_and_manual_dispatch ... ok
test_runs_are_serialised_and_never_cancelled ... ok
test_permissions_are_minimal_and_write_scoped ... ok
test_runs_on_a_github_hosted_runner ... ok
test_re_enumerates_instead_of_reusing_the_event ... ok
test_judges_a_fresh_merge_candidate_and_pins_the_head ... ok
test_declares_the_unproven_serialization_boundary ... ok
test_unoccupied_new_directory_is_accepted ... ok
test_same_id_after_the_first_merge_is_rejected ... ok
test_additive_file_under_existing_directory_is_accepted ... ok
test_conflicting_candidates_yield_no_merge_candidate ... ok

Ran 11 tests in 6.926s

OK
```

```
$ python scripts/ci/check_work_item_uniqueness.py --base HEAD --head HEAD
WORK-ITEM UNIQUENESS: PASS (base=386d8f57b02d8e3c511ff0e3980b9ce0af8b3028 candidate=386d8f57b02d8e3c511ff0e3980b9ce0af8b3028 introduced=0 occupied=0)
```

```
$ bash -n <broker run block>            # syntax of the workflow's shell body
exit=0
$ shellcheck -S warning <broker run block>
SC2148 only: no shebang in a `run:` block, which is expected
```

Regression checks on this head are recorded in `session-evidence.md`.

## 8. Not claimed

- No CI run, required-context result, merge SHA or post-merge blob digest is
  claimed for this branch.
- No live broker execution is claimed: the REST quota was exhausted before any
  pull request could be created, so no `merge-ready` run exists.
- No branch-protection read on 2026-11-27 is claimed.
- No independent review is claimed.
- AID-2026-279's tests were not executed on this host (see section 7); the
  merged gate's behaviour is demonstrated here only through the composition
  tests in this work item.
