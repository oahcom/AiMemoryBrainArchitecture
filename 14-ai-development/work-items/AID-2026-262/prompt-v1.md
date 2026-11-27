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
      last_verification_note: "Structured snapshot of the dispatched extension contract. This is not a verbatim transcript, platform-signed artifact or independent authentication of the executing AI session."
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
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-262 — Structured scope snapshot

## 1. Task identity

Repository: `oahcom/AiMemoryBrainArchitecture`

Issue: #1341

Related design issue: #1331

Assigned work-item identity: `AID-2026-262`

The earlier AID-2026-242 reservation was invalidated because that identifier became occupied on main through unrelated PR #1297 at `044dee41`. The aid-ledger correction at `79c622cc` records the correction and reserves AID-2026-262 for issue #1341.

The target main SHA supplied for this work is:

`386d8f57b02d8e3c511ff0e3980b9ce0af8b3028`

## 2. Authoritative implementation decision

Extend the already-landed checker at:

`scripts/ci/check_work_item_uniqueness.py`

Run it from the already-required job:

`GOV-DOC-002 metadata checks`

Do not create a second independent uniqueness workflow. Do not rewrite AID-2026-279 or its historical evidence.

The earlier-branch files below are removed from the final design:

- `scripts/check_work_item_uniqueness.py`
- `scripts/test_check_work_item_uniqueness.py`
- `.github/workflows/work-item-uniqueness.yml`

## 3. Identity contract

A target identity is occupied if it appears in any of these sources:

1. A directory name directly beneath `14-ai-development/work-items/`.
2. A top-level `work_item_id` scalar in that directory's `manifest.yaml`.
3. A top-level legacy `aid` scalar in that directory's `manifest.yaml`.
4. A registration in `14-ai-development/work-items/INDEX.md`.

The checker must compare candidate-introduced identity claims with the occupied identity set on the latest target commit.

A new file under a work-item directory already present at merge-base is additive maintenance, not a new directory claim.

A candidate introducing two directories that claim the same identity must be rejected.

The checker must read tracked trees and blobs from Git objects, not from working-copy files.

## 4. SHA and result contract

The checker accepts:

- `--base`: full 40-hex SHA of the latest target commit.
- `--head`: full 40-hex SHA of the exact candidate commit.

Branch names, abbreviated SHAs, malformed SHAs, unknown commits, Git failures and unreadable objects must not silently become PASS.

Exit codes:

- `0`: PASS.
- `1`: VIOLATION.
- `2`: INCOMPLETE.

Each violation must emit a GitHub `::error::` annotation identifying the duplicate identity and the source claim.

## 5. Test harness

The landed test harness currently invokes the checker using the literal executable `python3`. The supplied run of `python -X utf8 scripts/ci/test_work_item_uniqueness.py` reports five failures with return code 9009.

Change the harness to invoke the checker using `sys.executable`.

Use deterministic tests built from real temporary Git repositories and real commits. Do not mock Git or substitute a simulated commit graph.

The named tests must cover:

- `test_positive_new_unoccupied_id`
- `test_negative_directory_occupied_on_latest_base`
- `test_additive_existing_directory_accepted`
- `test_race_two_independent_claimants`
- `test_exact_head_stale_vs_advanced_target`
- `test_free_directory_manifest_identity_collision`
- `test_legacy_aid_identity_collision`
- `test_index_registration_without_directory_occupies_id`
- `test_quoted_and_unquoted_manifest_variants`
- `test_candidate_multiple_directories_same_identity`
- `test_no_work_item_directory_addition`
- `test_unknown_sha_is_incomplete`
- `test_missing_arguments_is_incomplete`

The test harness must exit nonzero when any test fails.

## 6. Workflow and serialization

Modify `.github/workflows/document-management.yml`.

The uniqueness test and decision remain inside the existing `GOV-DOC-002 metadata checks` job. The uniqueness verdict therefore uses the existing required status context; do not add a new context or change branch protection.

Add job-level concurrency with one static group shared by all runs of the job:

`document-management-gov-doc-002-serialized`

Set `cancel-in-progress: false`.

Immediately before the uniqueness decision, add a step named:

`Refresh target branch immediately before uniqueness decision`

For pull requests, this step must:

1. Fetch `origin/main`.
2. Resolve `refs/remotes/origin/main` to a full commit SHA.
3. Pass that SHA as `--base`.
4. Pass the exact `github.event.pull_request.head.sha` as `--head`.

Do not use the event's `pull_request.base.sha` as the authoritative target snapshot.

For direct pushes to main, use the push event's `before` SHA as base and `github.sha` as candidate.

The supplied platform measurements establish `required_status_checks.strict: true`, 16 required contexts, no merge queue, and auto-merge disabled.

The shared job concurrency group prevents two executions of this job from running simultaneously. GitHub concurrency is not FIFO; a superseded pending run has no successful required result.

Strict up-to-date protection is the merge freshness dependency. If another PR advances main after a candidate's check, the stale candidate branch must update before merge. That update causes a new required-job run, which refreshes main and checks the exact new head.

This is not an atomic transaction around the merge API and does not claim protection against privileged administrative bypass.

## 7. Eight acceptance rows

The implementation evidence must map each of the eight issue acceptance rows to a named test or command:

1. Contract — manifest identity, legacy `aid`, INDEX-only occupancy, multiple candidate claims and additive-directory tests.
2. Serialization — `test_race_two_independent_claimants`.
3. Positive — `test_positive_new_unoccupied_id`.
4. Negative — `test_negative_directory_occupied_on_latest_base`.
5. Additive — `test_additive_existing_directory_accepted`.
6. Race — `test_race_two_independent_claimants`.
7. Exact-Head — `test_exact_head_stale_vs_advanced_target`.
8. Regression — document-management self-check, traceability, test reachability and line-ending checks.

Do not claim any of these proposed tests passed until they have actually been run after the extension.

## 8. Scope restrictions

Do not:

- Rewrite AID-2026-279 or its evidence.
- Rename or renumber existing work-item directories.
- Retroactively repair historical collisions handled by #1332.
- Modify existing manifests other than the new AID-2026-262 record.
- Modify `PR-GOVERNANCE-001.md`.
- Modify `.gitattributes`.
- Modify `scripts/check_traceability.py`.
- Modify `scripts/ci/check_repository_hygiene.py`.
- Modify `.github/workflows/gates.yml`.
- Modify `.github/workflows/repository-hygiene.yml`.
- Change branch protection.
- Claim CI, merge, independent review or Owner acceptance without evidence.

## 9. Evidence and provenance

Keep separate:

- Supplied measurements of the landed checker and harness.
- The observed five harness failures with return code 9009.
- Historical results from the earlier standalone checker.
- New results from the extended landed checker, which are not yet measured.

The earlier branch's 13/13 tests and real-tree PASS must not be attributed to the landed `scripts/ci/` implementation.

The prompt snapshot is a structured scope record, not a signed transcript or proof of platform-authenticated AI identity.
