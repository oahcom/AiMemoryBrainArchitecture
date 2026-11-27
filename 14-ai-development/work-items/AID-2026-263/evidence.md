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
        - "14-ai-development/work-items/AID-2026-263/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local test runs and one live branch-protection read are recorded verbatim. No CI run or merge SHA is claimed; the race row stays unproven until a live two-pull-request experiment exists."
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

# AID-2026-263 — Evidence

**Attribution:** user-authorized operator (delegated by account owner)
**Date:** 2026-11-27
**Issues:** #1331 (defect, mechanism selection), #1341 (implementation issue, acceptance table)
**Branch base:** `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028` (`origin/main`, merge of PR #1372)

## 1. What this work item is, and what it deliberately is not

Option (d) has two halves. The first — a checker that decides "is this newly
introduced work-item directory already occupied on the latest target branch" —
was merged into `main` by AID-2026-279 (`feat(ci): enforce merge-time work-item
uniqueness`, commit `84790d36`, merged by PR #1372 as `386d8f57`), wired into the
required GOV-DOC-002 job (`.github/workflows/document-management.yml` lines
32-46). The second — a **serialized merge boundary** that evaluates every
candidate against the `main` it will land on and merges with the head it judged —
is not on `main`. AID-2026-279 states the gap itself:

> The branch-protection /protection endpoint returned HTTP 403 to this
> connection, so strict and enforce_admins are not asserted. Merge serialization
> through strict freshness remains unverified until those two fields can be
> independently read.
> — `14-ai-development/work-items/AID-2026-279/evidence.md`, section "Serialization mechanism"

This work item therefore adds **no second checker**. A second copy of the same
rule under a second name is the defect #1331 reports, not a fix for it. It adds
the broker that calls the merged checker, and it records which of the eight
acceptance rows are actually established.

## 2. Option (d), verbatim

Source: `https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/issues/1331/comments`
(comment id `3586480262`, author `oahcom`, created `2026-11-26T18:08:33Z`),
retrieved 2026-11-27 by this session before the REST quota was exhausted.

> ## Owner decision recorded — Option (d) selected
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
> ### Options (a), (b), (c) — not selected as standalone solutions
>
> - **(a) a shared reservation registry**: needs reservation lifecycle and concurrency semantics of its own, so it adds a second source of truth to keep consistent with the branch.
> - **(b) base-relative validation alone**: without serialization, two PRs can both pass against the same base and then race to merge — the defect survives.
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
| `14-ai-development/work-items/AID-2026-263/*` | new | Registration, prompt snapshot, session evidence, this record. |
| `14-ai-development/work-items/INDEX.md` | modified | One row. |

Not changed: `scripts/ci/check_work_item_uniqueness.py`, its tests, any
existing workflow, the required-context set, branch protection.

### 4.1 Why the broker judges the head and records the candidate tree

The broker computes the merge candidate itself:

```
tree=$(git merge-tree --write-tree --no-messages "$base_sha" "$head_sha")
```

A non-zero exit means the candidate has no tree at all (add/add conflict on the
same path), and the pull request is rejected without a uniqueness verdict —
there is nothing to judge.

When the candidate does exist, `git merge-tree` guarantees it is the union of
`main` and the head with no conflict, so the directories the candidate
*introduces* are exactly the directories the head introduces. The merged
checker is therefore called with `--base <latest main> --head <head>`; passing
it a tree object is not possible (`rev-parse <ref>^{commit}` fails on a tree) and
would be a lie about what was read. The candidate tree OID is printed in the run
log next to `base` and `head`, so the association between the verdict and the
merge that followed is auditable.

## 5. Acceptance evidence — row by row

Legend: **ACQUIRED** = demonstrated by an artifact in this repository at this
head. **NOT ACQUIRED** = not demonstrated. Nothing below is marked acquired on
the strength of a gate that merely ran.

| # | Evidence | Status | Artifact / reason |
|---|---|---|---|
| 1 | Contract | ACQUIRED | Section 2 above is the Owner decision verbatim; section 3 is the implementation issue verbatim. The two cases are implemented by `scripts/ci/check_work_item_uniqueness.py` (`introduced_dirs` filtered by `exists(merge_base, directory)`, occupancy by `exists(base, path)`) and re-stated in the broker's rejection paths. |
| 2 | Serialization | **NOT ACQUIRED** | `BROKER_SERIALIZATION_UNPROVEN`. The broker serialises its own runs and re-reads main before every merge, but nothing on the platform restricts `main` to this path. A platform mechanism does exist and was measured on 2026-11-27 (`strict: true` plus the required GOV-DOC-002 context); section 6 records what that does and does not prove. |
| 3 | Positive test | ACQUIRED | `scripts/ci/test_work_item_merge_broker.py::test_unoccupied_new_directory_is_accepted` (exit 0, `introduced=1 occupied=0`) and, from AID-2026-279, `test_new_unoccupied_directory_passes`. Raw output in section 7. |
| 4 | Negative test | ACQUIRED | `test_same_id_after_the_first_merge_is_rejected` (exit 1, `VIOLATION`) and AID-2026-279's `test_occupied_directory_is_rejected`. |
| 5 | Additive test | ACQUIRED | `test_additive_file_under_existing_directory_is_accepted` (exit 0, `introduced=0 occupied=0`) and AID-2026-279's `test_additive_file_under_existing_directory_passes`. |
| 6 | Race test | **PARTIAL** | The gate is shown to reject the second claimant once main has advanced (`test_same_id_after_the_first_merge_is_rejected`, which first shows both candidates passing against the shared base). That is the gate's half. The other half — that two broker runs cannot interleave — is not demonstrated: it needs a real run with two `merge-ready` pull requests, and no such run exists. |
| 7 | Exact-Head test | **PARTIAL** | The broker re-reads the head, aborts when the API head and the fetched head disagree, and passes `sha=<head_sha>` to the merge API so a head that moved is refused rather than merged unevaluated. That is structural: the assertion lives in `test_judges_a_fresh_merge_candidate_and_pins_the_head`, and no live merge has exercised it. |
| 8 | Regression evidence | **PARTIAL** | `check_traceability.py --index-only`, `check_repository_hygiene.py`, `check_test_reachability.py`, `check_document_management.py` and `audit_runner_admission.py` were executed locally on this head; raw output in section 7 and `session-evidence.md`. No CI run is claimed for this head. |

Rows 2, 6, 7, 8 are the reason this pull request is a draft and #1341 stays
open.

## 6. `BROKER_SERIALIZATION_UNPROVEN`

The requirement is that two concurrent pull requests cannot both validate
against the same obsolete base. Three things are needed for that, and this
change supplies only the first two:

1. **Serialised evaluation.** Supplied: one `concurrency` group with
   `cancel-in-progress: false`, and a re-read of `origin/main` at the top of
   every iteration.
2. **Evaluation against the merge that will happen.** Supplied: the candidate
   tree is computed against the `main` that exists at that moment, and the merge
   call names the exact head SHA.
3. **No other path into `main`.** **Not supplied.** Branch protection would have
   to require a context produced by this workflow — and this workflow produces
   no required context by design (adding one is out of scope for this work
   item). Any actor who can merge a pull request can merge it without the
   broker, after the required contexts pass.

### 6.1 Measured on 2026-11-27T04:47:13Z

`GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` returned
HTTP 200 to this session. The earlier 403 was quota exhaustion (`remaining: 0`
from `/rate_limit`), not a permission boundary; AID-2026-279 recorded the same
403 and reasonably read it as unreadable. The payload says:

- `required_status_checks.strict: true`
- 16 required contexts, unchanged from the 2026-11-25 document, including
  `GOV-DOC-002 metadata checks` — the job that runs the AID-2026-279 checker
- `enforce_admins: {enabled: true}`
- `GET /repos/.../rulesets` returned `[]`: no repository ruleset, so no merge
  queue and no ruleset-based required workflow

`strict: true` is a real serialisation mechanism, and it is a *different* one
from this broker. It means a pull request cannot merge unless its head contains
the current `main` tip. The merge of any other pull request moves `main`, which
marks every remaining pull request out of date; bringing one back up to date
creates a new head SHA whose required contexts have not run yet. The uniqueness
verdict is one of those required contexts, so a verdict computed against an
older base cannot be the verdict that merges.

That narrows the gap to two claims that are still unproven:

1. That the platform behaves as the flag implies under a real race — two pull
   requests introducing the same ID, merged one after the other. This needs a
   live experiment; no such run exists, so the race row stays PARTIAL.
2. That no actor can merge around it. `enforce_admins: true` is measured and no
   ruleset exists to bypass, but "no bypass exists" is an absence claim that a
   single read cannot establish.

So the correct statement is narrower than "serialization is unproven" and
broader than "serialization is proven": **the platform mechanism is present and
measured; its behaviour under a real race is not demonstrated, and this broker
is not the exclusive path into `main`.** Row 2 stays NOT ACQUIRED until a
two-pull-request race is replayed on the platform and its outcome recorded.

What would close it, in order of cost:

- Replay the race: two branches that both introduce `AID-2026-9xx`, both labelled
  `merge-ready`, one broker run; record the second merge being refused or the
  second check failing after the first merge moves `main`.
- Or require a context produced by this workflow **and** forbid direct pushes;
  then a merge that skips the broker fails the required check. That is a
  branch-protection change and needs the Owner, not this pull request.

## 7. Raw local output

Host: Windows, Python 3.12.3, git 2.56.1. `python3` is a Microsoft Store stub on
this host (exit 9009), so AID-2026-279's own tests cannot run here; this work
item's tests use `sys.executable` for that reason.

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

Ran 11 tests in 7.464s

OK
```

```
$ python scripts/check_traceability.py --index-only
PASS TRACEABILITY: 0 requirements / 119 work items / 0 errors / 110 warnings
```

```
$ python scripts/ci/check_repository_hygiene.py --base 756e1e25d735f526254fc3241b47880fef527b24 --head 9b4d45d72c14114682c23663d5cb09999aa8b241
Work-item index membership version=2026-11-27.2 directories=130 linked=130
Work-item manifest consistency version=2026-11-27.2 manifests=119 in_scope=105 excluded_by_record_type=5 unrecognized=9 violations=0
Repository new-file admission passed: 6 new path(s) checked.
```

```
$ python scripts/ci/check_test_reachability.py
Test reachability: 69 test files, 69 reachable, 0 unreachable
Gate wiring: 21 gate scripts, 3 unwired, 3 baselined
```

```
$ python scripts/check_document_management.py --require-changed 756e1e25
PASS (incremental): no GOV-DOC-002 violations; 684 classified, 370 unclassified
```

```
$ python scripts/ci/check_manifest_blob_pins.py
main=9b4d45d7 manifests=120 pins=196 ok=105 mismatch=89 path_missing=2 incomplete=0
(no AID-2026-263 line; the 89 mismatches are the pre-existing set that
 scripts/ci/baselines/manifest-blob-pins.txt records as measured on main at
 6f597e2d. The gate exits 1 on this count wherever it runs, main included.)
```

```
$ python scripts/ci/check_work_item_uniqueness.py --base HEAD --head HEAD
WORK-ITEM UNIQUENESS: PASS (base=9b4d45d72c14114682c23663d5cb09999aa8b241 candidate=9b4d45d72c14114682c23663d5cb09999aa8b241 introduced=0 occupied=0)
```

```
$ python scripts/ci/audit_runner_admission.py
GitHub-hosted runner policy: 27 job(s) audited, 0 violation(s)
```

```
$ bash -n <broker run block>            # syntax of the workflow's shell body
exit=0
$ shellcheck -S warning <broker run block>
SC2148 only: no shebang in a `run:` block, which is expected
```

## 9. Identifier history and the AIDSCAN evidence

This work item was first authored under the 262 placeholder. That number was a local,
unpublished placeholder: it existed only as a commit in a worktree, with no ref
pointing at it. AIDSCAN's five-scope scan (2829 commits of `main` history, 2349
ref tips deduplicated to 1317 unique trees, 21 ledger versions, 280 worktrees,
PR refs excluded) judged that occupation non-authoritative, and `aid-ledger`
recorded the correction in branch `ledger/2026-11-27-aid-263`, commit
`384a3057`, whose message is "chore(aid): cancel 262, reserve 263 for #1341,
record 261 conflict and 7 missing rows". The ledger entry reads:

```yaml
  - id: AID-2026-263
    state: RESERVED
    carrier: "Issue #1341 (serialized merge-time work-item uniqueness gate)"
```

Re-verified in this session, not taken on trust:

- `git grep` for `AID-2026-263` under `14-ai-development/work-items` across all
  2495 local refs: no hit.
- `git log --all -S"AID-2026-263"`: no commit.
- `git ls-remote --heads origin` filtered for branch names containing `263`: no
  hit.

### 9.1 The 262 placeholder is retired, and its content did exist

The 262 placeholder did reach the remote before the renumber, and this record
does not pretend otherwise:

| Fact | Value |
|---|---|
| Branch | `work-item/aid-2026-262-merge-broker` |
| Head SHA | `8908bb166c589acf3005a722c455ac9981715a7d` |
| Commit subject | `feat(ci): serialized merge-time work-item uniqueness broker (AID-2026-262)` |
| Commit time | `2026-11-27T12:45:11+08:00` (`2026-11-27T04:45:11Z`) |
| Local worktree commit | `2b63b8ba` (same title, different SHA) |
| Content | The broker workflow and its tests, now carried by this work item under `AID-2026-263` |

That branch is retired: its content is merged into
`work-item/aid-2026-263-merge-broker`, and the remote branch is deleted so that
262 does not become a second carrier for this work item — the same
double-carrier shape that #1341 reports for 261. Deletion output and the
verification read are recorded in `session-evidence.md`.

## 8. Not claimed

- No CI run, required-context result, merge SHA or post-merge blob digest is
  claimed for this branch.
- No live broker execution is claimed: no pull request carried `merge-ready`
  while this session ran, so the merge path has never executed.
- No independent review is claimed.
- AID-2026-279's tests were not executed on this host (see section 7); the
  merged gate's behaviour is demonstrated here only through the composition
  tests in this work item.
