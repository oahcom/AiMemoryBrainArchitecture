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
        - "14-ai-development/work-items/AID-2026-285/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Executor-captured outputs are recorded below. The evidence document and its metadata have not been independently validated by the implementation session, and the GitHub Actions workflow was not executed."
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
    canonical_scope: "Executor-provided test and Git-history execution evidence for AID-2026-285, the Issue #1341 merge-time work-item uniqueness gate correction."
    canonical_scope_id: "ai-development/aid-2026-285-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-285"
      - "executor execution"
      - "work-item uniqueness"
      - "merge-time serialization"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-285 — Evidence

## 1. Scope

This evidence record covers the two residual acceptance gaps for Issue #1341:

1. The test suite must invoke the checker through the active Python interpreter rather than assuming that a `python3` executable is available.
2. Pull-request enforcement must serialize decisions by target branch, fetch the current target branch before checking, and evaluate the generated merge candidate against that fetched base.

The implementation files covered are:

- `scripts/ci/check_work_item_uniqueness.py`
- `scripts/ci/test_work_item_uniqueness.py`
- `.github/workflows/document-management.yml`

The implementation session authored the files. A separate executor applied them, ran the commands, and supplied the output recorded below.

## 2. Initial Windows failure before the test invocation correction

The executor supplied the following baseline result from before the change:

```text
PS> python -X utf8 scripts/ci/test_work_item_uniqueness.py
...
Ran 5 tests in 5.786s

FAILED (failures=5)
```

Each failure was reported as:

```text
AssertionError: 9009 != <expected> :
```

The executor identified return code `9009` as Windows' command-not-found result for `python3`. The captured child-process output was empty.

This baseline demonstrates the local invocation defect: the test suite attempted to start a `python3` executable that was not available in the executor's environment.

## 3. First expanded-suite failure and implementation correction

The executor reported the following result for the first applied revision of the expanded eight-test suite:

```text
FAIL: test_workflow_serializes_by_target_and_fetches_latest_base
  File ".../test_work_item_uniqueness.py", line 266, in test_workflow_serializes_by_target_and-fetches-latest-base
    self.assertLess(fetch_position, enforcement_position)
AssertionError: 2010 not less than 1605

Ran 8 tests in 7.295s
FAILED (failures=1)
```

The assertion compared the file position of the fetch command inside the enforcement step with the position of the enforcement step's own `- name:` marker. Since the fetch command is inside the step, its position in the file is necessarily later than the step-name marker. The assertion therefore compared different structural levels and did not test the intended command ordering.

The implementation session selected option (ii): keep the fetch and checker invocation in the same enforcement step, extract the `run:` script in the test, and compare the positions of the fetch command and checker invocation within that script.

The corrected test verifies that the fetch appears before the checker invocation that consumes the fetched remote-tracking ref. The workflow remains a single enforcement step.

## 4. Corrected Windows test-suite result

The executor supplied the following output after applying the corrected test:

```text
test_additive_file_under_existing_directory_passes ... ok
test_merge_candidate_sha_is_checked ... ok
test_missing_base_is_incomplete ... ok
test_new_unoccupied_directory_passes ... ok
test_occupied_directory_is_rejected ... ok
test_race_replay_rejects_second_candidate_on_fresh_base ... ok
test_workflow_checks_github_merge_candidate_not_pr_head ... ok
test_workflow_serializes_by_target_and-fetches-latest-base ... ok

Ran 8 tests in 17.550s

OK
```

The executor also reported:

```text
EXITCODE=0
```

The command used was:

```powershell
python -X utf8 scripts/ci/test_work_item_uniqueness.py
```

This is executor-executed Windows evidence. It is not a test run performed by the implementation session.

The eight reported tests cover:
- acceptance of a newly introduced unoccupied directory;
- rejection of an occupied directory;
- acceptance of additive content beneath an existing directory;
- rejection of a competing claim when replayed against a fresh base;
- INCOMPLETE for missing base input;
- target-branch concurrency and fetch-before-check ordering in the workflow;
- checker evaluation of a GitHub-style merge candidate;
- workflow use of `github.sha` rather than the PR source head SHA.

## 5. Executor-executed real repository history check A

The executor ran:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base 6306a858 --head 7ecf2a8e
```

The captured output was:

```text
WORK-ITEM UNIQUENESS: PASS (base=6306a858afc378f27448f8796c6b6604dfa240bb candidate=7ecf2a8e7d1e40a13f6af6d4335a6766a222194f introduced=1 occupied=0)
```

The executor reported exit code `0`.

The supplied interpretation is that `7ecf2a8e` is the current `main` commit and that this history introduces `AID-2026-290`. The checker found one introduced directory and no occupied directory on the supplied base.

## 6. Executor-executed real repository history check B

The executor ran:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base 7ecf2a8e --head ece472aa
```

The captured output was:

```text
WORK-ITEM UNIQUENESS: PASS (base=7ecf2a8e7d1e40a13f6af6d4335a6766a222194f candidate=ece472aa8d4139fa0d3d441b199a1251549f7eb1 introduced=0 occupied=0)
```

The executor reported exit code `0`.

The supplied interpretation is that `ece472aa` is the head of open PR #1413, which adds files beneath `AID-2026-279`. The target `main` already contains that directory, so the checker reports `introduced=0` and accepts the additive change.

## 7. Workflow mechanism recorded by the implementation

The final workflow supplied by the implementation session uses workflow-level concurrency keyed by the target branch:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.base.ref || github.ref_name }}
  cancel-in-progress: false
```

The PR enforcement step fetches the target branch:

```bash
git fetch origin "+refs/heads/${BASE_REF}:refs/remotes/origin/${BASE_REF}"
```

It then invokes the checker with the fetched remote-tracking ref as `--base` and `CANDIDATE_SHA` as `--head`. The environment sets:

```yaml
CANDIDATE_SHA: ${{ github.sha }}
```

The PR path therefore uses the generated merge candidate rather than `github.event.pull_request.head.sha`.

The existing push-before path is retained. The workflow continues to use the existing `GOV-DOC-002 metadata checks` job, with the self-check and uniqueness self-test before enforcement.

The supplied repository fact is that `GET /repos/.../rulesets` returned an empty list (`[]`), and there is no merge queue. The workflow deliberately does not introduce `merge_group` as an enforcing path.

The workflow itself was not executed on GitHub Actions. This section records the authored mechanism; it is not evidence of a successful workflow run.

## 8. Verification status

<text>**Executor-reported local and history checks: PASS. GitHub Actions workflow execution: NOT RUN.**</text>

The executor supplied successful results for:
- the corrected eight-test Windows suite;
- a real repository history check introducing one new work-item directory;
- a real repository history check adding content beneath an existing work-item directory.

The executor also supplied the initial Windows failure and the first expanded-suite assertion failure, both retained above as part of the correction history.

The following have not been established by the supplied execution evidence:
- a GitHub Actions run of `.github/workflows/document-management.yml`;
- a green GOV-DOC-002 result on GitHub;
- merge of the implementation branch or a pull request;
- independent review;
- Owner acceptance.

## 9. Reproduction commands

Run from the repository root.

Windows local test suite:

```powershell
python -X utf8 scripts/ci/test_work_item_uniqueness.py
```

Real-history check A:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base 6306a858 --head 7ecf2a8e
```

Real-history check B:

```powershell
python -X utf8 scripts/ci/check_work_item_uniqueness.py --base 7ecf2a8e --head ece472aa
```

The output recorded in this document was supplied by the executor. These commands are reproduction instructions; they do not imply that the implementation session ran them.

## 10. Non-claims

- The executor's test output is not claimed as execution by the implementation session.
- The authored workflow is not claimed to have run successfully on GitHub Actions.
- No green CI result is claimed.
- No pull request is claimed to have been merged.
- No independent review is claimed.
- No Owner acceptance is claimed.
- The work item remains `IN_PROGRESS` pending the applicable repository document and session-evidence gates and subsequent review and acceptance.
