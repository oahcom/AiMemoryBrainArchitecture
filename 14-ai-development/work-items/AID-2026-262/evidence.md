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
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "The supplied repository and platform measurements were checked for this authoring record. The landed checker and harness sizes, harness failure result, main SHA, ledger correction, required-context count and strict freshness setting are recorded. The proposed extension and its tests have not been run; no CI, merge, review or Owner acceptance is claimed."
    usage_status: Active
    modification_status: Active-Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "The design, implementation contract and supplied measurements for extending the already-required GOV-DOC-002 job with serialized merge-time uniqueness checks for work-item directory, manifest and INDEX identities under issue #1341."
    canonical_scope_id: ai-development/aid-2026-262-work-item-uniqueness-gate
    canonical_scope_keywords:
      - work-item uniqueness
      - merge-time gate
      - directory identity
      - manifest work_item_id
      - legacy aid
      - INDEX registration
      - latest target branch
      - job concurrency
      - strict branch freshness
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-262 — Implementation contract and measured evidence

## 1. Record scope

This record covers the extension of the landed work-item uniqueness checker for GitHub issue #1341. The implementation target is the existing `scripts/ci/check_work_item_uniqueness.py`, its test harness, and the already-required `GOV-DOC-002 metadata checks` job in `.github/workflows/document-management.yml`.

The authoritative decision is to extend the existing required gate in place. This work does not create a second independent uniqueness workflow or a new branch-protection context.

The intended checker recognizes four identity sources:

1. A directory name directly beneath `14-ai-development/work-items/`.
2. A top-level `work_item_id` scalar in that directory's `manifest.yaml`.
3. A top-level historical `aid` scalar in that directory's `manifest.yaml`.
4. An identity registration in `14-ai-development/work-items/INDEX.md`.

The checker compares identities introduced by the candidate against identities occupied on the latest target commit. It preserves additive changes beneath a directory already present at the merge-base.

## 2. Reconciliation and identifier history

### 2.1 AID-2026-242 was invalidated

AID-2026-242 was initially reserved for issue #1341. It was later occupied on main by the unrelated D canonical store root restoration, merged through PR #1297 at `044dee41`.

The aid-ledger correction at commit `79c622cc`, titled `correct 241/242 carriers and reserve 260/262`, invalidated the earlier reservation and reserved AID-2026-262 for issue #1341.

The supplied current-main measurement is:

`386d8f57b02d8e3c511ff0e3980b9ce0af8b3028`

The supplied allocation measurements report 114 AID directories on main, highest ID AID-2026-279, and AID-2026-262 free on main and the known branches at allocation time. The open-PR claims supplied for the allocation check are AID-2026-253, AID-2026-256, AID-2026-261, AID-2026-267, AID-2026-268 and AID-2026-280.

### 2.2 AID-2026-279 remains historical

AID-2026-279 is the competing implementation that landed through PR #1372. Its record and evidence are not to be rewritten.

The implementation in `scripts/ci/check_work_item_uniqueness.py` and `scripts/ci/test_work_item_uniqueness.py` is the existing carrier being extended. The separate checker, test and workflow from the earlier branch are removed so that the repository does not retain two independent uniqueness gates.

The earlier branch's 13/13 local test result and its real-tree PASS are evidence for that earlier checker only. They are not evidence that the landed `scripts/ci/` checker extension or its corrected harness passes.

## 3. Supplied measurements

The supplied measurements report:

| Item | Supplied result |
|---|---|
| Current `origin/main` | `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028` |
| Landed checker | `scripts/ci/check_work_item_uniqueness.py`, 4318 bytes |
| Landed harness | `scripts/ci/test_work_item_uniqueness.py`, 4796 bytes |
| Existing harness invocation | `python -X utf8 scripts/ci/test_work_item_uniqueness.py` |
| Existing harness outcome | 5/5 fail; subprocess return code 9009 |
| Reported harness defect | `invoke()` hardcodes the `python3` executable |
| Earlier checker | `scripts/check_work_item_uniqueness.py`, 11366 bytes |
| Earlier test file | `scripts/test_check_work_item_uniqueness.py`, 15514 bytes |
| Earlier workflow | `.github/workflows/work-item-uniqueness.yml`, 2406 bytes |
| Earlier checker tests | 13/13 passed, for the earlier checker only |
| Earlier real-tree run | PASS; introduced directories 0; occupied identities 121; violations 0 |
| Required status contexts | 16 |
| Strict up-to-date protection | true |
| Merge queue | absent (reported API response 404) |
| Auto-merge | false |

The earlier real-tree run used base `f18adc9fa1d06837433a09498f5297bf13b35756` and head `d674e67e2483378dfb03d11bd6859792a86763fb`. It is retained as historical evidence and is not a current-main or current-checker result.

## 4. Implementation contract

### 4.1 Candidate and target semantics

The checker accepts `--base` and `--head`, each a full 40-hex commit SHA. Abbreviated SHAs, branch names, malformed SHAs and unresolved commits must produce INCOMPLETE, not PASS.

The checker computes the merge-base of the target commit and candidate commit. Candidate-introduced work-item directories are determined from paths added after that merge-base. A directory already present at the merge-base is not a new claim merely because the candidate adds another file beneath it.

The occupied identity set is read from the target commit's Git tree and blobs, not from the working copy. It includes directory names, top-level manifest `work_item_id`, top-level legacy `aid`, and INDEX registrations.

For every introduced directory, the checker collects the directory identity and any valid top-level manifest identity fields. New INDEX registrations are also candidate claims. An identity already present in the target occupied set is a violation. Two introduced directories making the same identity claim are also a violation.

### 4.2 Result contract

| Exit code | Meaning |
|---|---|
| 0 | PASS |
| 1 | VIOLATION |
| 2 | INCOMPLETE |

Every violation emits a GitHub `::error::` annotation identifying the duplicate identity and its source. Git failures, unreadable objects, missing arguments, invalid SHAs or indeterminate comparisons must not be accepted as PASS.

### 4.3 Test harness repair

The landed test harness currently invokes the checker through the literal executable name `python3`. The supplied execution result is five failures with return code 9009 on the reported machine.

The harness must use `sys.executable` so that it launches the checker with the interpreter running the harness. The proposed real-Git suite includes named cases for positive, negative, additive, race, exact-head, manifest identity, legacy `aid`, INDEX registration, quoted scalar variants, duplicate candidate claims, no-directory changes, unknown SHAs and missing arguments.

The proposed checker and corrected harness have not been run in this authoring turn. No pass count is asserted for them.

## 5. Required workflow integration and serialization

### 5.1 Required context

The uniqueness check runs as a step in the existing job named `GOV-DOC-002 metadata checks`. The supplied branch-protection measurement reports 16 required contexts. This design adds no separate status context and requires no branch-protection write.

The required job therefore carries the uniqueness verdict as part of its existing required context, subject to the workflow change landing and the job succeeding on the current PR head.

### 5.2 Target refresh

For pull requests, the workflow fetches `origin/main` in the step named:

`Refresh target branch immediately before uniqueness decision`

The step resolves `refs/remotes/origin/main` to a full commit SHA and passes it to the checker as `--base`. It passes the exact `github.event.pull_request.head.sha` as `--head`. The event's `pull_request.base.sha` is not used as the authoritative occupancy snapshot because it may be stale when the job executes.

For a push to main, the workflow uses the push event's `before` SHA as the base and `github.sha` as the candidate.

### 5.3 Job-level serialization

The job has a static concurrency group:

`document-management-gov-doc-002-serialized`

and sets:

`cancel-in-progress: false`

The group is job-level and shared across all runs of this job, rather than including a PR head SHA. This prevents two executions of this required job from running simultaneously.

GitHub concurrency does not promise FIFO ordering. A newer pending run may replace an older pending run. A superseded run has no successful required result; it must not be interpreted as a passing verdict.

### 5.4 Why stale validation cannot authorize a merge

A run acquires the shared job concurrency slot before executing the job, then refreshes main immediately before the uniqueness decision. Consequently, a later run of this job does not execute its decision concurrently with an earlier run, and it obtains a fresh target snapshot when it begins that decision. If another PR merges after a candidate's target refresh, strict up-to-date branch protection (`required_status_checks.strict: true`, as measured) prevents the now-behind candidate branch from merging until it is updated. The updated PR triggers another required-job run, which refreshes main and evaluates the exact new head against the advanced target. A superseded pending run cannot supply a successful required result. This is a combined workflow-serialization and branch-freshness mechanism, not an atomic transaction around the GitHub merge operation; it does not promise FIFO scheduling or prevent privileged administrative bypass.

### 5.5 Residual boundary

The supplied measurements establish strict freshness but do not establish an atomic transaction between a status check and the merge operation. The protection depends on the required `GOV-DOC-002 metadata checks` context remaining enforced and strict freshness remaining enabled. An administrator with bypass authority may bypass ordinary merge requirements. The design does not claim protection against such a bypass.

## 6. Acceptance mapping

The eight issue acceptance rows are mapped to these named tests or commands:

| Acceptance row | Test or command | Result at authoring time |
|---|---|---|
| Contract | `test_free_directory_manifest_identity_collision`, `test_legacy_aid_identity_collision`, `test_index_registration_without_directory_occupies_id`, `test_candidate_multiple_directories_same_identity`, `test_additive_existing_directory_accepted` | Proposed tests; NOT RUN |
| Serialization | `test_race_two_independent_claimants` | Proposed real-Git test; NOT RUN |
| Positive test | `test_positive_new_unoccupied_id` | Proposed real-Git test; NOT RUN |
| Negative test | `test_negative_directory_occupied_on_latest_base` | Proposed real-Git test; NOT RUN |
| Additive test | `test_additive_existing_directory_accepted` | Proposed real-Git test; NOT RUN |
| Race test | `test_race_two_independent_claimants` | Proposed real-Git test; NOT RUN |
| Exact-Head test | `test_exact_head_stale_vs_advanced_target` | Proposed real-Git test; NOT RUN |
| Regression evidence | `python3 scripts/test_check_document_management.py`; `python3 scripts/ci/check_test_reachability.py`; `python3 scripts/check_traceability.py --index-only`; `python3 scripts/ci/check_line_endings.py` | Not run after this proposed change |

The previously supplied 13/13 result belongs to the earlier standalone checker and is not substituted for the unrun landed-checker tests. The existing harness's five failures with return code 9009 are the only supplied execution result for the landed harness.

## 7. Files in the selected change

The intended modified files are:

- `scripts/ci/check_work_item_uniqueness.py`
- `scripts/ci/test_work_item_uniqueness.py`
- `.github/workflows/document-management.yml`

The intended new record files are:

- `14-ai-development/work-items/AID-2026-262/manifest.yaml`
- `14-ai-development/work-items/AID-2026-262/evidence.md`
- `14-ai-development/work-items/AID-2026-262/prompt-v1.md`
- `14-ai-development/work-items/AID-2026-262/session-evidence.md`

The intended INDEX change is one registration row for AID-2026-262.

The following earlier-branch files are deleted to avoid a second independent gate:

- `scripts/check_work_item_uniqueness.py`
- `scripts/test_check_work_item_uniqueness.py`
- `.github/workflows/work-item-uniqueness.yml`

AID-2026-279 and its record are not modified.

## 8. What is not claimed

- The proposed extended checker has not been executed.
- The corrected `sys.executable` harness has not been executed.
- No updated regression counts are known.
- No GitHub Actions run or successful required-context result is claimed.
- No pull request number or merge SHA is claimed.
- No post-merge blob digest is claimed.
- No independent review is claimed.
- No natural-person Owner acceptance is claimed.
- No branch-protection setting was changed.
- No historical work-item collision was repaired or renumbered.
