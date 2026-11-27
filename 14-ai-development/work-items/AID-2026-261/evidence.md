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
        - "14-ai-development/work-items/AID-2026-261/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "The recorded local results are supplied by the operator. They are not CI results, merge results, or post-merge verification. The unit-test suite had four failures caused by inconsistent output-key casing before this correction; corrected tests must be rerun before claiming the suite passes."
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
    canonical_status: Canonical
    canonical_scope: "AID-2026-261 implementation and verification record for cross-tree work-item directory uniqueness at merge time"
    canonical_scope_id: "ai-development/aid-2026-261-merge-time-work-item-uniqueness"
    canonical_scope_keywords:
      - "work-item-uniqueness"
      - "merge-time"
      - "serialization"
      - "issue-1341"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
# AID-2026-261 — Merge-time work-item directory uniqueness

## 1. Contract

The protected object is the work-item directory:

`14-ai-development/work-items/AID-YYYY-NNN/`

The rule is based on candidate-introduced directories and the latest target
branch:

1. A directory absent at the candidate/target merge-base but present in the
   candidate is a candidate-introduced work-item directory.
2. If that identifier already exists as a directory in the latest target tree,
   the candidate fails with `WU-01`.
3. If the identifier is absent from the latest target tree, the new directory
   is accepted.
4. A directory already present at the candidate's merge-base is an existing
   work item. Adding files beneath it is allowed and is not a duplicate
   registration.

The checker does not replace T-04. T-04 checks duplicate INDEX records within
one tree. This checker checks whether a candidate-introduced directory is
already occupied in another, newer tree.

## 2. Implementation

Files:

- `scripts/check_work_item_uniqueness.py`
- `tests/test_check_work_item_uniqueness.py`
- `.github/workflows/work-item-uniqueness.yml`

The checker resolves both refs to commit SHAs, identifies their unique
merge-base, and reads work-item directory entries directly from Git trees.
It does not inspect or modify the working tree.

Exit codes:

- `0`: PASS — no candidate-introduced ID is occupied by the target.
- `1`: FAIL — at least one candidate-introduced ID is occupied by the target.
- `2`: INCOMPLETE — a ref, Git object, tree, or unambiguous merge-base cannot
  be established.

A missing target is never interpreted as an empty target.

## 3. Serialization and platform boundary

The workflow uses a single workflow-wide concurrency group:

`work-item-uniqueness-repository-global`

The group is shared by different PRs and main-push audits. This differs from
the repository's existing per-head-SHA concurrency convention. The setting
`cancel-in-progress: false` prevents a new execution from canceling an
execution already checking the target.

The checker always resolves the target ref at execution time. It does not
trust the PR's historical base SHA as the occupancy authority.

A push to main starts an additional audit of open PR heads because a main
advance does not itself generate a `pull_request.synchronize` event.

This is not a claim of complete platform serialization. GitHub Actions
concurrency permits a pending run to be replaced by a newer pending run.
Furthermore, the measured branch-protection payload did not enable strict
up-to-date protection, no merge queue was present, and this new context was
not a required status check.

The remaining check-to-merge race must be closed by repository platform
administration: require this status context and enable strict up-to-date
protection or a merge queue that evaluates the actual merge candidate.
Until that is independently verified, an unconditional merge-time guarantee
must not be claimed.

## 4. Verification evidence

| Evidence | Proof method | Reproduction command | Expected output / acceptance condition |
|---|---|---|---|
| Contract | Checker distinguishes candidate-introduced directories from directories already present at merge-base. | `python -m unittest discover -s tests -p "test_check_work_item_uniqueness.py" -v` | New-directory uniqueness and existing-directory incremental acceptance; `Ran 7 tests in 13.697s; OK (exit 0)` |
| Serialization | Workflow-wide concurrency group serializes workflow executions; each execution resolves latest target. Platform merge enforcement remains an explicit dependency. | Inspect `.github/workflows/work-item-uniqueness.yml`; `git show HEAD:.github/workflows/work-item-uniqueness.yml` | Shared concurrency group; `cancel-in-progress: false`; platform merge barrier separately verified |
| Positive | Candidate introduces an identifier absent from target and passes. | `python scripts/check_work_item_uniqueness.py --target origin/main --candidate HEAD` | Exit 0; `PASS new work-item directory AID-2026-261`; `candidate=331faf31d115014097c1dc669061724284b5ca3c target=a588cd9914949c2c9db7b2c5704d906fd3f05b70 merge_base=a7a252eb670b31066a0ffea35dc28cbe6ef5b836; CANDIDATE_NEW_DIRECTORIES=1 TARGET_OCCUPIED_NEW_DIRECTORIES=0 ACCEPTED_NEW_DIRECTORIES=1 EXISTING_DIRECTORIES=109 BAD=0; PASS new work-item directory AID-2026-261: target is unoccupied; PASS WORK ITEM UNIQUENESS; exit 0` |
| Negative | Candidate introduces an identifier already present in latest target and fails in the checker itself. | `python -m unittest discover -s tests -p "test_check_work_item_uniqueness.py" -v` | Negative fixture exits 1; explicit `ERROR WU-01 duplicate work-item directory AID-2026-261`; `temp repo neg261: candidate=1407392f276e1c2cafde40cdb73885fc6bf97d0c target=8b6bfdc7694d518b9e69fe48f82f11dfddc76c14 merge_base=a36dc1b80e4715498cb976fedf3a68c3a782a274; CANDIDATE_NEW_DIRECTORIES=1 TARGET_OCCUPIED_NEW_DIRECTORIES=1 ACCEPTED_NEW_DIRECTORIES=0 EXISTING_DIRECTORIES=1 BAD=1; ERROR WU-01 duplicate work-item directory AID-2026-261: candidate introduces this ID, but the latest target already contains it; exit 1` |
| Incremental | Candidate adds a file beneath an identifier already present at merge-base. | `python -m unittest discover -s tests -p "test_check_work_item_uniqueness.py" -v` | Exit 0; `PASS existing work-item directory AID-2026-100`; no duplicate error |
| Race | Two candidate refs independently introduce the same identifier from the same target; first passes, then target advances, second fails. | `python -m unittest discover -s tests -p "test_check_work_item_uniqueness.py" -v` | First decision exit 0; second exit 1; `ERROR WU-01 duplicate work-item directory AID-2026-262`; `temp repo race261: step 1 (PR A against unoccupied main) TARGET_OCCUPIED_NEW_DIRECTORIES=0 BAD=0 PASS WORK ITEM UNIQUENESS exit 0; after main was advanced to PR A head, step 2 (PR B) TARGET_OCCUPIED_NEW_DIRECTORIES=1 BAD=1 ERROR WU-01 duplicate work-item directory AID-2026-262: candidate introduces this ID, but the latest target already contains it; exit 1` |
| Exact head | Same candidate ref is checked against two target states; first is unoccupied, second is occupied. | `python -m unittest discover -s tests -p "test_check_work_item_uniqueness.py" -v` | Candidate SHA remains identical; target SHA changes; result changes from exit 0 to exit 1 |
| Regression | Existing traceability, document management, runner admission, repository hygiene and uniqueness checks are run independently. | `python scripts/check_work_item_uniqueness.py --target origin/main --candidate HEAD`<br>`python scripts/check_traceability.py --index-only`<br>`python scripts/check_document_management.py --require-changed origin/main`<br>`python scripts/ci/audit_runner_admission.py`<br>`python scripts/ci/check_repository_hygiene.py --base <base_sha> --head <head_sha>` | Supplied local results: uniqueness exit 0; traceability PASS; document management PASS; runner admission 29 jobs audited, 0 violations. Repository hygiene must be run with actual base/head SHAs; no pass is claimed until its output and exit code are recorded. |

## 5. Actual local verification supplied by the operator

The following results were reported as actual local executions, not CI:

| Command | Reported result |
|---|---|
| `python scripts/check_work_item_uniqueness.py --target origin/main --candidate HEAD` | Exit 0 |
| `python scripts/check_traceability.py --index-only` | `PASS TRACEABILITY: 0 requirements / 110 work items / 0 errors / 108 warnings`, exit 0 |
| `python scripts/check_document_management.py --require-changed origin/main` | `PASS (incremental): no GOV-DOC-002 violations; 647 classified, 371 unclassified`, exit 0 |
| `python scripts/ci/audit_runner_admission.py` | `29 job(s) audited, 0 violation(s)`, exit 0 |

The reported uniqueness checker output included:

