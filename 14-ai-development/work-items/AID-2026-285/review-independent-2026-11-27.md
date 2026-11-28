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
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Independent review of the exact head aac82d45193bbd3964184220f4bf11713a142ec8. The reviewer session did not implement the change; every command in the appendix was executed by it on this machine and the output is pasted, not summarized. The verdict, per-row verdicts and findings were produced by a separate review conversation that had no prior exposure to the work."
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
  steward: "independent reviewer session (no implementation role)"
---

# Independent Review — AID-2026-285

## Review identity

| Field | Value |
|---|---|
| Work item | AID-2026-285 |
| Issue / PR | #1341 / #1447 |
| Reviewed exact head | `aac82d45193bbd3964184220f4bf11713a142ec8` |
| Merge commit | `08167492c786658bbb2f0ebdfd24236157ebd169` |
| PR base at merge | `168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab` |
| Pre-fix comparison commit | `7ecf2a8e7d1e40a13f6af6d4335a6766a222194f` |
| Candidate tree / merge tree | `f43bc26c6bf0ad6b9034dd57e0a075ed85964333` (identical) |
| Review date | 2026-11-27 |
| Reviewer | separate review conversation, no implementation role |
| Overall verdict | **NEEDS REVISION** |

The reviewer session executed every command below on Windows against a detached worktree at the
reviewed head and a second detached worktree at the pre-fix commit. It wrote no implementation code and
changed no implementation file. The verdict, per-row verdicts and findings in sections 1–5 are the
output of a review conversation that was given the object, Issue #1341's acceptance rows, the workflow,
the checker and test excerpts, and the command output in section 6 — and nothing else.

> **Supersession note, added by the reviewer session (not the review conversation).** This record
> reviews the exact head named above. While the record was being committed, `main` had already
> advanced to `473f06d76`, which replaces this checker and its suite under AID-2026-311 / PR #1477
> (`fix(ci): tree-only work-item uniqueness verdict`). Everything below is a statement about
> `aac82d45`, not about current `main`.

## Verdict

**NEEDS REVISION**

PR #1447 implements a meaningful improvement: the checker supports explicit base/head references, the workflow fetches the target branch, the concurrency group is target-branch-scoped, and the candidate is evaluated using `github.sha`. Positive, negative, additive, exact-candidate, and regression evidence are demonstrated. However, the central merge-time uniqueness guarantee is not established. `cancel-in-progress: false` serializes workflow executions, not validation and merge as one atomic operation. The scratch reproduction demonstrates that two candidates can both pass against the same base, subsequently merge, and leave duplicate work-item files. More importantly, the measured branch-protection setting is `required_status_checks.strict = False`, contradicting the carrier's assertion that strict freshness closes the residual interval. The change improves detection but does not prove the acceptance requirement that competing PRs cannot both merge duplicate IDs.

## Per-row verdicts

| Issue #1341 row | Verdict | Deciding evidence and assessment |
|---|---|---|
| Contract | DEMONSTRATED | Checker excerpt: `introduced_dirs(merge_base, head)` retains directories absent from the merge-base tree; `occupied = [path for path in introduced if exists(base, path)]` checks occupancy against the supplied target base. Tests 1–3 exercise new-directory and additive-file behavior. |
| Serialization | PARTIALLY DEMONSTRATED | Workflow lines 7–9 establish a target-branch concurrency group and disable cancellation. Lines 54–57 fetch and consume the target ref. Test 6 passes its workflow-string assertions. However, concurrency does not serialize the subsequent GitHub merge operation with validation. |
| Positive test | DEMONSTRATED | Test 1, `test_new_unoccupied_directory_passes`, is `ok` in the eight-test run. Its stated assertion is exit 0 with `introduced=1 occupied=0`. |
| Negative test | DEMONSTRATED | The isolated test reports `ok` and explicitly asserts checker exit code 1 and `VIOLATION` in stdout. Its checker output confirms `introduced=1 occupied=1` for AID-2026-279 on base `205254e...`. |
| Additive test | DEMONSTRATED | Test 3, `test_additive_file_under_existing_directory_passes`, reports `ok`; its assertion requires exit 0 and `introduced=0`. This is consistent with the checker excluding directories already present at the merge base. |
| Race test | NOT DEMONSTRATED | Test 4 demonstrates rejection when the second candidate is explicitly replayed against a fresh base. However, §6.8 demonstrates that A and B both pass against B0, both are merged, and the post-merge push check also passes with `introduced=0 occupied=0`. The required guarantee that both cannot merge is contradicted by the supplied reproduction. |
| Exact-Head test | DEMONSTRATED | Workflow line 49 assigns `CANDIDATE_SHA: ${{ github.sha }}`; line 57 passes it as `--head`. Runner log §6.4 identifies the checked-out merge candidate and reports `candidate=124fd67...`, the generated merge commit containing `aac82d451...`. Tests 7 and 8 also pass. |
| Regression evidence | DEMONSTRATED | `scripts/test_check_document_management.py`: `371/371 passed`. All 16 required contexts are reported successful on the reviewed head, including Repository hygiene, Session Evidence, and GOV-DOC-002. The job name remains present and all measured required contexts resolve to existing jobs. |

## Findings

### 1. Critical — The uniqueness invariant is not protected against competing merges

**Evidence**

Section 6.8 reproduces the following sequence:

```text
--- A evaluated at B0 (merge candidate) ---
WORK-ITEM UNIQUENESS: PASS (...) introduced=1 occupied=0
exit=0

--- B evaluated at the SAME base B0 ---
WORK-ITEM UNIQUENESS: PASS (...) introduced=1 occupied=0
exit=0
```

Both candidates are then merged. The post-merge check reports:

```text
WORK-ITEM UNIQUENESS: PASS (...) introduced=0 occupied=0
exit=0
```

The merged tree contains:

```text
14-ai-development/work-items/AID-2026-999/a.txt
14-ai-development/work-items/AID-2026-999/b.txt
```

**Why it matters**

The checker detects a collision only when the candidate is evaluated against a base already containing the competing directory. It cannot reject a candidate based on a competing PR that has passed validation but has not yet merged.

The concurrency group serializes workflow runs, not the entire validation-to-merge transaction. Two sequential validations can still occur before either corresponding merge.

The post-merge push check also fails to detect the resulting duplicate because the directory already exists at its merge base.

**What would close it**

Implement a merge-time mechanism that makes uniqueness validation and admission mutually exclusive for candidates targeting the same branch. Ensure a competing candidate cannot merge based on validation performed against an obsolete target state.

Add an end-to-end race test exercising the actual admission mechanism, not merely a manually refreshed second checker invocation. Assert that exactly one competing candidate can merge.

### 2. High — The carrier's strict-freshness justification contradicts measured branch protection

**Evidence**

The carrier claims:

> The residual interval - the target advancing between the check and the merge - is closed by the repository's existing `required_status_checks.strict: true`.

Section 6.7 reports:

```text
required_status_checks.strict = False
```

It also reports:

```text
GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets
returns [] (no merge queue).
```

**Why it matters**

The stated justification for closing the interval between validation and merge is not supported by the measured configuration. In fact, the measured strict setting is explicitly false.

The required `Branch freshness vs base` context being successful does not establish that GitHub branch protection enforces strict required-status-check freshness.

Consequently, the carrier's claimed residual-interval protection cannot be accepted.

**What would close it**

Provide evidence of an enforced merge-time freshness mechanism, with the actual effective configuration and a test demonstrating rejection of a candidate whose target base advances after its uniqueness check.

Alternatively, implement an atomic admission mechanism that does not depend on strict branch freshness.

### 3. Medium — The runner evidence does not establish a different fetched base from the event base

**Evidence**

Workflow lines 46–47:

```yaml
PR_BASE: ${{ github.event.pull_request.base.sha }}
BASE_REF: ${{ github.event.pull_request.base.ref }}
```

Workflow lines 54–57:

```bash
git fetch origin "+refs/heads/${BASE_REF}:refs/remotes/origin/${BASE_REF}"
python3 scripts/ci/check_work_item_uniqueness.py \
  --base "refs/remotes/origin/$BASE_REF" \
  --head "$CANDIDATE_SHA"
```

Runner log:

```text
PR_BASE: 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab
BASE_REF: main
```

The checker reports:

```text
WORK-ITEM UNIQUENESS: PASS (base=168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab candidate=124fd67... introduced=1 occupied=0)
```

Section 6.3 separately demonstrates that the checker can resolve a supplied live remote-tracking ref:

```text
$ git rev-parse refs/remotes/origin/main
4a6cdd0e7c5dc0db53be37a2f945e02c59d5abf9
```

Its verdict prints that same base.

**Why it matters**

The workflow code correctly passes the fetched remote-tracking ref rather than `PR_BASE`. However, the runner's fetched SHA equals the event payload's base SHA.

Therefore, the runner log does not independently demonstrate that the fetched value differed from the event payload. Section 6.3 demonstrates local ref consumption, not a different fetched value during the actual workflow execution.

The carrier's acceptance-table wording that the runner used `168f66a6`, "not the event base", is inaccurate: `168f66a6` is also the event base shown in that runner log.

**What would close it**

Provide a workflow execution where the target branch advances beyond the event base before the fetch, and show that the checker reports the newer fetched SHA.

## Answers to five direct questions

**a. Can two PRs targeting the same branch still both validate against the same stale base?**

Yes. Workflow lines 7–9 serialize workflow executions by target branch, but they do not serialize validation with the corresponding merge. Lines 54–57 fetch the branch when the checker step executes. If candidate A finishes validation without merging before candidate B begins its validation, B can fetch the same unchanged base. Section 6.8 demonstrates both candidates passing against B0. Therefore, the workflow does not establish that two competing PRs cannot both validate against the same base.

**b. What does `cancel-in-progress: false` guarantee, and what does it not guarantee?**

It prevents a newly arriving workflow run in the same concurrency group from cancelling the currently running workflow. Together with lines 7–9, it provides target-branch-scoped serialization of running workflow executions. It does not guarantee that a validated candidate merges before another candidate validates, that validation and merge are atomic, that every pending candidate is retained, or that the target cannot advance between validation and merge.

**c. Does the checker receive the fetched commit rather than the event payload?**

Yes, by the workflow's actual argument construction. Line 54 fetches the target branch; line 56 supplies `refs/remotes/origin/$BASE_REF` as `--base`; line 57 supplies the candidate as `--head`. The runner executes this path with `BASE_REF=main`. However, its reported base SHA equals `PR_BASE`, so that execution does not independently prove a different fetched SHA. Section 6.3 confirms that the checker resolves a supplied remote-tracking ref rather than substituting the event payload.

**d. Is the result bound to the exact merge candidate rather than the pushed head?**

Yes. Workflow line 49 sets `CANDIDATE_SHA` from `${{ github.sha }}`, and line 57 passes it to `--head`. The runner log identifies the checked-out commit as `124fd67ddd0412fc360251773b39683dd8ad0d81`, described as the merge of `aac82d451...` into `168f66a6...`. Its verdict reports `candidate=124fd67...`, not the PR head SHA. This is evidence of checking the generated merge candidate.

**e. Is the required context `GOV-DOC-002 metadata checks` preserved, and did any required context disappear?**

Yes. The workflow still declares `name: GOV-DOC-002 metadata checks` at line 22. The supplied check-run evidence lists all 16 required contexts as successful, and the job-name check states that every required context resolves to a job still present at the reviewed head. No disappearance of a required context is demonstrated.

## Limitations

1. This review evaluates the supplied exact-head source excerpts, test descriptions, command outputs, runner log, merge identity, and measured branch-protection configuration. It does not independently execute the repository or retrieve GitHub records.
2. The eight-test output establishes that the suite passed on the reviewer's machine. The additional isolated run independently establishes the negative test's rejection assertion and removes the earlier output-interleaving ambiguity.
3. The local live-ref experiment demonstrates checker behavior with a remote-tracking ref, not that the workflow runner fetched a different commit from the event base.
4. The runner log establishes the candidate SHA checked in that execution. It does not establish atomicity between checking and merging.
5. The measured `required_status_checks.strict = False` is a review-time observation. No historical branch-protection configuration at the exact merge timestamp is supplied.
6. No merge-queue execution, `merge_group` workflow, or atomic merge-admission mechanism is demonstrated.
7. The successful regression results establish the supplied test and required-context outcomes, not the absence of all regressions.

**Final disposition: NEEDS REVISION.** The isolated negative test resolves the earlier evidence ambiguity and is now demonstrated. It does not change the overall verdict: Issue #1341's central requirement—preventing two competing work-item claims from both merging—remains unproven and is contradicted by the supplied race reproduction.

## 6. Command evidence

Every command below was executed by the reviewer session. Output is pasted, not summarized. Commands
that print a checker verdict were run from a worktree whose `HEAD` is the commit named in the heading.

### 6.1 Exact head `aac82d451...` — `python -X utf8 scripts/ci/test_work_item_uniqueness.py`

```text
test_additive_file_under_existing_directory_passes (__main__.WorkItemUniquenessTests.test_additive_file_under_existing_directory_passes) ... $ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head a6d23a17f33b8d2131a531c16b3dc0a34c8d7f72 --base 9aa3dbde06e31630d11074adb6a4326c9efad4f9
ok
test_merge_candidate_sha_is_checked (__main__.WorkItemUniquenessTests.test_merge_candidate_sha_is_checked) ... WORK-ITEM UNIQUENESS: PASS (base=9aa3dbde06e31630d11074adb6a4326c9efad4f9 candidate=a6d23a17f33b8d2131a531c16b3dc0a34c8d7f72 introduced=0 occupied=0)
$ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head 7dfb6352af24ecbaec27b4c202061c5adfa06a91 --base 29ed43f67987f78eebeb95a4ad0e6d9e637886fe
ok
test_missing_base_is_incomplete (__main__.WorkItemUniquenessTests.test_missing_base_is_incomplete) ... WORK-ITEM UNIQUENESS: PASS (base=29ed43f67987f78eebeb95a4ad0e6d9e637886fe candidate=7dfb6352af24ecbaec27b4c202061c5adfa06a91 introduced=1 occupied=0)
$ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head 34faebbba77e71ecf3656206b5be43dddaa81d88
ok
test_new_unoccupied_directory_passes (__main__.WorkItemUniquenessTests.test_new_unoccupied_directory_passes) ... WORK-ITEM UNIQUENESS: INCOMPLETE (missing required ref(s): --base)
$ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head 0dfaeafec9dc1db2c0fe2d224dbabce5b343b8e9 --base 5267de9292979d4d905888a39f52a870a13a2ddc
ok
test_occupied_directory_is_rejected (__main__.WorkItemUniquenessTests.test_occupied_directory_is_rejected) ... WORK-ITEM UNIQUENESS: PASS (base=5267de9292979d4d905888a39f52a870a13a2ddc candidate=0dfaeafec9dc1db2c0fe2d224dbabce5b343b8e9 introduced=1 occupied=0)
$ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head 2a89be8b48ef19592121ce0c7f0069bb0e321f0d --base 225dc8f7dd09f07ef8e7491682d1a957979dcd13
ok
test_race_replay_rejects_second_candidate_on_fresh_base (__main__.WorkItemUniquenessTests.test_race_replay_rejects_second_candidate_on_fresh_base) ... VIOLATION: 14-ai-development/work-items/AID-2026-279 already exists on target base 225dc8f7dd09f07ef8e7491682d1a957979dcd13
WORK-ITEM UNIQUENESS: VIOLATION (base=225dc8f7dd09f07ef8e7491682d1a957979dcd13 candidate=2a89be8b48ef19592121ce0c7f0069bb0e321f0d introduced=1 occupied=1)
$ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head f79cba15099775657fcea271e6f2d85969cc8ae5 --base 21d781d17305c57e5e26ea18d49ddb0f9a57c0dc
WORK-ITEM UNIQUENESS: PASS (base=21d781d17305c57e5e26ea18d49ddb0f9a57c0dc candidate=f79cba15099775657fcea271e6f2d85969cc8ae5 introduced=1 occupied=0)
$ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head 7616e099d51f616d00af9a46277d7961ea8c9deb --base 21d781d17305c57e5e26ea18d49ddb0f9a57c0dc
WORK-ITEM UNIQUENESS: PASS (base=21d781d17305c57e5e26ea18d49ddb0f9a57c0dc candidate=7616e099d51f616d00af9a46277d7961ea8c9deb introduced=1 occupied=0)
$ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head 7616e099d51f616d00af9a46277d7961ea8c9deb --base f79cba15099775657fcea271e6f2d85969cc8ae5
ok
test_workflow_checks_github_merge_candidate_not_pr_head (__main__.WorkItemUniquenessTests.test_workflow_checks_github_merge_candidate_not_pr_head) ... ok
test_workflow_serializes_by_target_and_fetches_latest_base (__main__.WorkItemUniquenessTests.test_workflow_serializes_by_target_and_fetches_latest_base) ... ok

----------------------------------------------------------------------
Ran 8 tests in 10.479s

OK
VIOLATION: 14-ai-development/work-items/AID-2026-279 already exists on target base f79cba15099775657fcea271e6f2d85969cc8ae5
WORK-ITEM UNIQUENESS: VIOLATION (base=f79cba15099775657fcea271e6f2d85969cc8ae5 candidate=7616e099d51f616d00af9a46277d7961ea8c9deb introduced=1 occupied=1)
```

Exit code 0. The `$ ...python.exe ...check_work_item_uniqueness.py` lines are echoed by the test
harness itself, not by the reviewer. Test names go to stderr and each test's own output to stdout, so
this capture interleaves the two streams and a verdict line can appear under a neighbouring test name;
6.10 gives the isolated run of the negative test.

### 6.2 Pre-fix `7ecf2a8e7` — the same command

```text
test_additive_file_under_existing_directory_passes (__main__.WorkItemUniquenessTests.test_additive_file_under_existing_directory_passes) ... $ python3 D:\code\_scratch\rev285\base285\scripts\ci\check_work_item_uniqueness.py --head b73ed0adf34726520140acf1a65fa9c858fb3362 --base cd514fce993308224085425a31877a17b44f40ab
FAIL
test_missing_base_is_incomplete (__main__.WorkItemUniquenessTests.test_missing_base_is_incomplete) ... 
$ python3 D:\code\_scratch\rev285\base285\scripts\ci\check_work_item_uniqueness.py --head 66886daee43155fc795020d49abb6058347354f6
FAIL
test_new_unoccupied_directory_passes (__main__.WorkItemUniquenessTests.test_new_unoccupied_directory_passes) ... 
$ python3 D:\code\_scratch\rev285\base285\scripts\ci\check_work_item_uniqueness.py --head 0a38950f5ef60d9f9ec762e7164733627640b812 --base 66886daee43155fc795020d49abb6058347354f6
FAIL
test_occupied_directory_is_rejected (__main__.WorkItemUniquenessTests.test_occupied_directory_is_rejected) ... 
$ python3 D:\code\_scratch\rev285\base285\scripts\ci\check_work_item_uniqueness.py --head 6e681f977b26a3340d93b447939448deb5cf0c31 --base 112d48bb05e1b27e75b38c805f01f9098699e891
FAIL
test_race_replay_rejects_second_candidate_on_fresh_base (__main__.WorkItemUniquenessTests.test_race_replay_rejects_second_candidate_on_fresh_base) ... 
$ python3 D:\code\_scratch\rev285\base285\scripts\ci\check_work_item_uniqueness.py --head a997b527bd62d7e3fbf39bbcfa42c66808e64865 --base affcdf3f5332f163589cec1cf4a650f4db19f339

$ python3 D:\code\_scratch\rev285\base285\scripts\ci\check_work_item_uniqueness.py --head 6953a200f9fbbe0575800570b31c8744ab4af3ce --base affcdf3f5332f163589cec1cf4a650f4db19f339
FAIL

======================================================================
FAIL: test_additive_file_under_existing_directory_passes (__main__.WorkItemUniquenessTests.test_additive_file_under_existing_directory_passes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_scratch\rev285\base285\scripts\ci\test_work_item_uniqueness.py", line 69, in test_additive_file_under_existing_directory_passes
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
AssertionError: 9009 != 0 : 

======================================================================
FAIL: test_missing_base_is_incomplete (__main__.WorkItemUniquenessTests.test_missing_base_is_incomplete)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_scratch\rev285\base285\scripts\ci\test_work_item_uniqueness.py", line 96, in test_missing_base_is_incomplete
    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
AssertionError: 9009 != 2 : 

======================================================================
FAIL: test_new_unoccupied_directory_passes (__main__.WorkItemUniquenessTests.test_new_unoccupied_directory_passes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_scratch\rev285\base285\scripts\ci\test_work_item_uniqueness.py", line 49, in test_new_unoccupied_directory_passes
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
AssertionError: 9009 != 0 : 

======================================================================
FAIL: test_occupied_directory_is_rejected (__main__.WorkItemUniquenessTests.test_occupied_directory_is_rejected)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_scratch\rev285\base285\scripts\ci\test_work_item_uniqueness.py", line 60, in test_occupied_directory_is_rejected
    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
AssertionError: 9009 != 1 : 

======================================================================
FAIL: test_race_replay_rejects_second_candidate_on_fresh_base (__main__.WorkItemUniquenessTests.test_race_replay_rejects_second_candidate_on_fresh_base)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\code\_scratch\rev285\base285\scripts\ci\test_work_item_uniqueness.py", line 83, in test_race_replay_rejects_second_candidate_on_fresh_base
    self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
AssertionError: 9009 != 0 : 

----------------------------------------------------------------------
Ran 5 tests in 6.027s

FAILED (failures=5)
```

Exit code 1. `9009` is the Windows `cmd` "command not found" status returned because the pre-fix suite
spawned `python3` (`scripts/ci/test_work_item_uniqueness.py:33`,
`args = ["python3", str(SCRIPT), "--head", head]`). At the reviewed head that line is
`sys.executable` (line 66).

### 6.3 Does the checker consume the fetched ref or the event payload?

```text
$ git rev-parse refs/remotes/origin/main
4a6cdd0e7c5dc0db53be37a2f945e02c59d5abf9

$ python -X utf8 scripts/ci/check_work_item_uniqueness.py --base refs/remotes/origin/main --head aac82d45193bbd3964184220f4bf11713a142ec8
WORK-ITEM UNIQUENESS: PASS (base=4a6cdd0e7c5dc0db53be37a2f945e02c59d5abf9 candidate=aac82d45193bbd3964184220f4bf11713a142ec8 introduced=0 occupied=0)
```

The printed base is the live remote-tracking ref, not the PR's event base `168f66a6`.

### 6.4 Runner log — GOV-DOC-002 on the exact head (run 45959185789, job 140372677080)

```text
2026-11-27T07:32:56.9536786Z ##[group]Checking out the ref
2026-11-27T07:32:57.0510099Z HEAD is now at 124fd67d Merge aac82d45193bbd3964184220f4bf11713a142ec8 into 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab
2026-11-27T07:32:59.2939545Z WORK-ITEM UNIQUENESS: PASS (base=e29ea17357c56ca9d41a004560a5775bca853314 candidate=1f9efd93ff31c56c0d46ac31e6a4831afa738e8f introduced=0 occupied=0)
2026-11-27T07:32:59.3490655Z WORK-ITEM UNIQUENESS: PASS (base=dab4d92e6fec145f684c4197a1f78e9c9d58884e candidate=2ea4ae786d97f1412138b4e25f3833a67903ac12 introduced=1 occupied=0)
2026-11-27T07:32:59.3991631Z WORK-ITEM UNIQUENESS: INCOMPLETE (missing required ref(s): --base)
2026-11-27T07:32:59.4669962Z WORK-ITEM UNIQUENESS: PASS (base=dab4d92e6fec145f684c4197a1f78e9c9d58884e candidate=9c18deb2a6c43351635d2b2a3690e45b39bd0f21 introduced=1 occupied=0)
2026-11-27T07:32:59.5353672Z WORK-ITEM UNIQUENESS: VIOLATION (base=09f12928cb3e7d7368008aeeeee7a3443f4e76c6 candidate=92aa46113f8c39980c6805f8c3485dd4071a8322 introduced=1 occupied=1)
2026-11-27T07:32:59.5828834Z WORK-ITEM UNIQUENESS: PASS (base=dab4d92e6fec145f684c4197a1f78e9c9d58884e candidate=d9fb605d763cd7d57dc58a513279694476158329 introduced=1 occupied=0)
2026-11-27T07:32:59.6337178Z WORK-ITEM UNIQUENESS: PASS (base=dab4d92e6fec145f684c4197a1f78e9c9d58884e candidate=c0f0559006252edcc1feec45982232509665d280 introduced=1 occupied=0)
2026-11-27T07:32:59.6787870Z WORK-ITEM UNIQUENESS: VIOLATION (base=d9fb605d763cd7d57dc58a513279694476158329 candidate=c0f0559006252edcc1feec45982232509665d280 introduced=1 occupied=1)
2026-11-27T07:32:59.6912953Z ##[group]Run set -euo pipefail
2026-11-27T07:32:59.6914063Z   git fetch origin "+refs/heads/${BASE_REF}:refs/remotes/origin/${BASE_REF}"
2026-11-27T07:32:59.6935045Z   PR_BASE: 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab
2026-11-27T07:32:59.6935265Z   BASE_REF: main
2026-11-27T07:32:59.6935716Z   CANDIDATE_SHA: 124fd67ddd0412fc360251773b39683dd8ad0d81
2026-11-27T07:32:59.9011356Z WORK-ITEM UNIQUENESS: PASS (base=168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab candidate=124fd67ddd0412fc360251773b39683dd8ad0d81 introduced=1 occupied=0)
2026-11-27T07:32:59.9165441Z   PR_BASE: 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab
```

### 6.5 Check runs on `aac82d451...` (16 required contexts, latest per name)

```text
GOV-DOC-001 structural checks            success @2026-11-27T07:32:48Z
Branch freshness vs base                 success @2026-11-27T07:32:56Z
audit                                    success @2026-11-27T07:32:48Z
GOV-DOC-002 metadata checks              success @2026-11-27T07:32:48Z
BMCP protocol index (hard gate)          success @2026-11-27T07:32:48Z
BMCP conformance suite (hard gate)       success @2026-11-27T07:32:47Z
Schema non-empty audit (hard gate)       success @2026-11-27T07:32:48Z
Bilingual docs coverage (ratchet)        success @2026-11-27T07:32:48Z
Rust clippy (hard gate)                  success @2026-11-27T07:32:48Z
Repository hygiene (hard gate)           success @2026-11-27T07:32:48Z
Rust format (hard gate)                  success @2026-11-27T07:32:49Z
Rust doctests (hard gate)                success @2026-11-27T07:32:48Z
Session Evidence                         success @2026-11-27T07:32:48Z
Session Evidence self-test (base)        success @2026-11-27T07:32:48Z
Session Evidence self-test (head)        success @2026-11-27T07:32:48Z
rust-workspace-test                      success @2026-11-27T07:32:55Z

total check runs on sha: 25
```

### 6.6 Merge identity

```text
head_tree = f43bc26c6bf0ad6b9034dd57e0a075ed85964333
merge_tree = f43bc26c6bf0ad6b9034dd57e0a075ed85964333
merge_commit_parents = 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab aac82d45193bbd3964184220f4bf11713a142ec8
head_commit_parents  = 23d8b42b746179b3e0153149d433e1139acc3794 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab
pr_base_from_api     = 168f66a6fb2f7eb19a87af6159d3b6a19db1f9ab
```

### 6.7 Branch protection, measured live at review time

```text
required_status_checks.strict = False
contexts(16): GOV-DOC-001 structural checks, Branch freshness vs base, audit, GOV-DOC-002 metadata checks, BMCP protocol index (hard gate), BMCP conformance suite (hard gate), Schema non-empty audit (hard gate), Bilingual docs coverage (ratchet), Rust clippy (hard gate), Repository hygiene (hard gate), Rust format (hard gate), Rust doctests (hard gate), Session Evidence, Session Evidence self-test (base), Session Evidence self-test (head), rust-workspace-test
org rulesets: {"message": "Not Found", "documentation_url": "https://docs.github.com/rest/orgs/rules#get-all-organization-repository-rulesets", "status": "404"}
enforce_admins=True
required_pull_request_reviews=null
required_conversation_resolution=False
```

No workflow declares a `merge_group` trigger, and `GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets`
returns `[]`.

### 6.8 Race reproduction with the head checker, on a scratch repository

Two branches A and B each add a file under `14-ai-development/work-items/AID-2026-999/` on top of the
same base B0. Both are evaluated at B0, both are merged in sequence, then the post-merge push-style
check is run:

```text
B0=ac87b78 HA=f5f5f631be8e8990a2a8994f7311739f44c758ee HB=76bfb43a416be5faf75a558ef95ebe551c293b42
--- A evaluated at B0 (merge candidate) ---
WORK-ITEM UNIQUENESS: PASS (base=ac87b78259a8623705712ab5f5cdf2541b1965d2 candidate=f5f5f631be8e8990a2a8994f7311739f44c758ee introduced=1 occupied=0)
exit=0
--- B evaluated at the SAME base B0 ---
WORK-ITEM UNIQUENESS: PASS (base=ac87b78259a8623705712ab5f5cdf2541b1965d2 candidate=76bfb43a416be5faf75a558ef95ebe551c293b42 introduced=1 occupied=0)
exit=0
--- merged main M2=3d24aa557ce250cc44f79b7850c139d5c11f9382 (first parent M1=f5f5f631be8e8990a2a8994f7311739f44c758ee) ---
--- post-merge push check: --base M1 --head M2 ---
WORK-ITEM UNIQUENESS: PASS (base=f5f5f631be8e8990a2a8994f7311739f44c758ee candidate=3d24aa557ce250cc44f79b7850c139d5c11f9382 introduced=0 occupied=0)
exit=0
--- duplicate work item on merged tree ---
14-ai-development/work-items/AID-2026-999/a.txt
14-ai-development/work-items/AID-2026-999/b.txt
```

### 6.9 Regression

`python -X utf8 scripts/test_check_document_management.py` at the exact head:

```text
  [ok  ] T19 required leaves come from the schema, not a second list
  [ok  ] T19 every required declaration is a leaf the gate checks
  [ok  ] T19 forbidden list names superseded_by
  [ok  ] T19 copy-paste template exists
  [ok  ] T19 template carries metadata
  [ok  ] T19 template satisfies the gate
371/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
```

The workflow still declares `name: GOV-DOC-002 metadata checks` at line 22, untouched by the diff. All
16 required contexts on `main` resolve to a job name that still exists at the reviewed head; none
disappeared.

### 6.10 Isolated run of the negative test

The eight-test transcript in 6.1 merges the suite's stderr (test names) with each test's stdout; the
capture interleaved the two streams. Running the single test in isolation:

```text
test_occupied_directory_is_rejected (scripts.ci.test_work_item_uniqueness.WorkItemUniquenessTests.test_occupied_directory_is_rejected) ... $ C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe D:\code\_scratch\rev285\head285\scripts\ci\check_work_item_uniqueness.py --head 41394365a87d05574e25d19311f53346713451fe --base 205254e2546aebab33df9b135d1aa97b49da5365
ok

----------------------------------------------------------------------
Ran 1 test in 1.221s

OK
VIOLATION: 14-ai-development/work-items/AID-2026-279 already exists on target base 205254e2546aebab33df9b135d1aa97b49da5365
WORK-ITEM UNIQUENESS: VIOLATION (base=205254e2546aebab33df9b135d1aa97b49da5365 candidate=41394365a87d05574e25d19311f53346713451fe introduced=1 occupied=1)
```

## 7. Review provenance

| Item | Value |
|---|---|
| Review conversation | `6b0a2773-9f1c-83ec-b557-66087429e99f` (fresh session; no prior exposure to this work) |
| Turn 1 prompt | `p1.md`, 32,525 bytes, sha256 `6d14aaa2df375e34817f3202789b2d0181ae14b9d7211489cb2ae068948021fd` |
| Turn 1 reply | `reply-6b0a2773-090044.md`, 14,531 bytes |
| Turn 2 prompt | `p2.md`, 2,613 bytes, sha256 `2fce5b3e662b1c4dba24db0c5a9d7123a1af0e6929e8b050975b098f2e210335` |
| Turn 2 reply (committed verbatim as sections 1–5) | `reply-6b0a2773-090337.md`, 12,333 bytes |
| Reviewer session role | no implementation role; executed commands only |
