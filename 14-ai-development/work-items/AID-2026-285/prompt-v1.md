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
      last_verification_note: "Structured task snapshot assembled from the two dispatched prompt rounds and the supplied implementation and executor facts; prompt provenance remains NOT_VERIFIED and this snapshot is not a verbatim transcript."
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
    canonical_scope: "Structured implementation prompt snapshot for AID-2026-285, closing the residual merge-time serialization and local test invocation acceptance gaps in Issue #1341."
    canonical_scope_id: "ai-development/aid-2026-285-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-285"
      - "Issue #1341"
      - "work-item uniqueness"
      - "merge-time serialization"
      - "local test invocation"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-285 — Prompt Snapshot

## 1. Task and role

Close the two residual acceptance rows of Issue #1341, "serialized, merge-time work-item uniqueness gate."

The implementation session is the sole author of the implementation and the associated work-item records. The executor is a separate agent session that applies the implementation output byte-for-byte, runs the commands, captures their output, and reports the results.

The implementation session recorded for this work item is:

`6b092534-81b4-83ec-a4de-49c5c6ecaa8b`

Execution evidence in `evidence.md` is executor-executed. It must not be attributed to the implementation session.

The work item is AID-2026-285, reserved on the `aid-ledger` branch at commit `5592658f`. Its reservation identifies the branch `fix/aid279-merge-time-serialization` and scopes the work to:
- making `scripts/ci/test_work_item_uniqueness.py` runnable without assuming a `python3` executable is available;
- making the merge-time base the latest target branch rather than the pull-request event base.

## 2. Repository and implementation baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Issue: `#1341`
- Work item: `AID-2026-285`
- Implementation branch: `fix/aid279-merge-time-serialization`
- Base branch: `main`
- Base commit: `7ecf2a8e7d1e40a13f6af6d4335a6766a222194f`
- Planned PR title: `fix(ci): make the work-item uniqueness gate merge-time serialized and locally runnable (AID-2026-285)`

The branch was cut from `origin/main` at the base commit above.

The work item modifies the existing checker, its deterministic test suite, and the existing document-management workflow. It does not introduce a separate job or a new required context.

## 3. Defects to close

### 3.1 Test invocation assumes a `python3` executable

The existing test suite invoked the checker using a literal `python3` executable. On the executor's Windows environment, the command was not found. The subprocess return code was `9009`, and the captured output was empty.

The test suite must invoke the checker through `sys.executable`, ensuring that the child process uses the same Python interpreter that is running the test suite.

The workflow's Ubuntu runner may continue to invoke its test suite using `python3`; the local test-suite requirement is that its child checker invocation must not hard-code `python3`.

### 3.2 Pull-request enforcement can use a stale event base

The pull-request event base SHA can be stale by the time the enforcement step executes. A uniqueness decision based only on that event SHA does not establish occupancy against the latest target-branch commit at the time the enforcement step runs.

The enforcement step must fetch the target branch itself, then pass the fetched remote-tracking ref to the checker as `--base`.

The candidate must be the generated GitHub merge candidate identified by `github.sha`, not the source branch head SHA.

## 4. Required mechanism

### 4.1 Serialize decisions by target branch

Use workflow-level GitHub Actions concurrency with a group keyed by the target branch:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.base.ref || github.ref_name }}
  cancel-in-progress: false
```

The group must be shared by pull requests targeting the same branch. It must not be keyed by the candidate SHA or by the source branch.

Set `cancel-in-progress: false` so a newly arriving candidate does not cancel a running uniqueness decision.

### 4.2 Fetch the current target branch before checking

The pull-request enforcement step must fetch the target branch itself:

```bash
git fetch origin "+refs/heads/${BASE_REF}:refs/remotes/origin/${BASE_REF}"
```

It must then invoke the checker with the fetched remote-tracking branch as its base:

```bash
python3 scripts/ci/check_work_item_uniqueness.py \
  --base "refs/remotes/origin/$BASE_REF" \
  --head "$CANDIDATE_SHA"
```

The workflow environment must bind:

```yaml
PR_BASE: ${{ github.event.pull_request.base.sha }}
BASE_REF: ${{ github.event.pull_request.base.ref }}
PUSH_BEFORE: ${{ github.event.before }}
CANDIDATE_SHA: ${{ github.sha }}
```

The PR path is selected when both `BASE_REF` and `PR_BASE` are non-empty. `PR_BASE` identifies the pull-request event context; it is not the base passed to the checker. The fetched remote-tracking ref is the checker base.

### 4.3 Evaluate the generated merge candidate

For pull-request enforcement, use:

```yaml
CANDIDATE_SHA: ${{ github.sha }}
```

and pass:

```bash
--head "$CANDIDATE_SHA"
```

Do not pass `github.event.pull_request.head.sha`. The required check must evaluate the generated merge candidate rather than only the source branch head.

### 4.4 Preserve the push path

For push events, retain the existing `PUSH_BEFORE` path. When `PUSH_BEFORE` is non-empty and is not the all-zero SHA, invoke the checker with that before-SHA as `--base` and the candidate SHA as `--head`.

For a first push with no usable before-SHA, retain the no-argument checker invocation. The checker reports missing required refs as INCOMPLETE rather than PASS.

### 4.5 Repository merge-queue fact

The repository's rulesets query returned an empty list:

```text
GET /repos/.../rulesets
[]
```

There is no merge queue on this repository in the supplied facts. Therefore `merge_group` is deliberately not introduced as the enforcing path.

### 4.6 Branch-protection relationship

The supplied mechanism relies on strict branch protection to require the pull request to be up to date and to require a fresh check after the target branch advances. This is the stated mechanism for closing the interval between the check and a later merge.

This work item does not claim that it independently changed or revalidated branch protection settings.

## 5. Checker behavior to preserve

The checker remains a standard-library Python program that compares:
- candidate-side work-item directories newly introduced since the merge-base; and
- occupancy of those directories on the base commit supplied by the caller.

A directory is a new claim only when it is absent at merge-base and introduced by the candidate. Files added beneath a directory already present at merge-base are additive changes, not new claims.

The checker outcomes remain:
- exit code `0`: PASS;
- exit code `1`: VIOLATION;
- exit code `2`: INCOMPLETE.

Missing refs, Git failures, unreadable objects, and subprocess failures are INCOMPLETE, never PASS.

The checker must not treat a directory already present on the supplied latest target base as an available new claim.

## 6. Eight acceptance rows

1. **Interpreter portability.** The test suite invokes the checker with `sys.executable`, not a literal `python3` command. The suite must be runnable with the Python interpreter selected by the executor, including on Windows.

2. **Target-branch serialization and fresh fetch.** The workflow concurrency group is keyed by `github.event.pull_request.base.ref || github.ref_name`, uses `cancel-in-progress: false`, and fetches the target branch before the checker invocation that consumes the fetched remote-tracking ref.

3. **New unoccupied directory.** A candidate that introduces a work-item directory absent from the supplied base is accepted when that directory is not occupied on the supplied target base.

4. **Occupied directory rejection.** A candidate that introduces a new work-item directory is rejected with VIOLATION when that directory is already occupied on the supplied target base.

5. **Additive change acceptance.** A candidate that adds a file beneath a work-item directory already present at merge-base is accepted as additive content and does not count as a newly introduced directory.

6. **Incomplete-state handling and race replay.** Missing base input is INCOMPLETE. A deterministic replay must show that two candidates evaluated against the same stale base can each initially pass, while reevaluating the second candidate against a fresh base containing the first candidate's claim rejects it.

7. **Exact merge-candidate input.** A GitHub-style merge candidate is checked, and the pull-request workflow passes `github.sha` as `--head`. It must not use `github.event.pull_request.head.sha`.

8. **Workflow integration and scope.** The existing GOV-DOC-002 job remains the enforcing job, with the self-check and uniqueness self-test before enforcement. The PR enforcement path fetches the target branch and uses the fetched ref as `--base`; the existing push-before path remains. No merge_group enforcing path is added because the repository has no merge queue. No new job or required context is introduced.

## 7. Prompt dispatch and revision history

Two prompt rounds were dispatched to the implementation session:

| Round | Snapshot name | Bytes | SHA-256 |
|---|---|---:|---|
| 1 | `p1.md` | 26281 | `14c4f9145c4691c02586cff447b90c5ebe7a693d6580c541f32779a19fcfed3e` |
| 2 | `p1b.md` | 3476 | `79c3c60adb180b2cdd780aa35bf227052aea908e2414b2048ebdf6c1ecdcb768` |

These identifiers and digests are the supplied dispatch facts. This structured snapshot is not a verbatim copy of either prompt round.

### Round 1

The first round specified the Issue #1341 residual acceptance work, the repository and branch baseline, the distinction between implementation author and executor, the checker/test/workflow scope, and the required deliverables.

The implementation direction was to retain the existing gate and required job while closing the local interpreter invocation defect and the stale event-base gap.

### Round 2

The second round addressed the workflow test assertion that compared the fetch command's position with the enforcement step's own name marker. It required a correction that measured ordering within the enforcement step's `run:` script.

The implementation session selected option (ii): retain the single enforcement step and assert that the fetch command appears before the checker invocation inside that step. The corrected test extracts the run script and compares the two positions within that extracted script.

## 8. Failed assertion and correction record

The executor reported that the first applied revision of the expanded test suite had one failure:

```text
FAIL: test_workflow_serializes_by_target_and_fetches_latest_base
  File ".../test_work_item_uniqueness.py", line 266, in test_workflow_serializes_by_target_and_fetches_latest_base
    self.assertLess(fetch_position, enforcement_position)
AssertionError: 2010 not less than 1605

Ran 8 tests in 7.295s
FAILED (failures=1)
```

The failure was in the test's position comparison. The fetch command was inside the enforcement step, so its file offset was necessarily greater than the offset of that step's `- name:` line. That comparison did not test the intended ordering.

The implementation session chose option (ii):
- keep the fetch and checker invocation in the same enforcement step;
- extract that step's `run:` script in the test;
- locate the fetch command within that script;
- locate the checker invocation within that script;
- assert that the fetch precedes the checker invocation.

The corrected assertion is scoped to the run script. It fails if the fetch is removed or moved after the checker invocation.

## 9. Provenance and execution discipline

The implementation session authored the checker, test suite, workflow, and this structured record.

The executor separately applied the implementation output, ran the commands on Windows, and supplied the captured output recorded in `evidence.md`.

The prompt snapshot provenance is `NOT_VERIFIED`. The prompt-round digests are recorded as supplied facts; they do not establish that this structured snapshot is a byte-identical copy of either dispatched prompt.

No test execution is attributed to the implementation session unless explicitly identified as such. No GitHub Actions run, merge, independent review, or Owner acceptance is claimed.
