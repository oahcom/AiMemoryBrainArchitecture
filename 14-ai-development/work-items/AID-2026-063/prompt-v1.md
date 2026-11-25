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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every value in the observation table was read from the check-run and merge endpoints for pull request #1038 on 2026-11-25, and the two quotations were taken from those responses rather than from a rendered page."
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

# WO-01 stage C — executed instruction

Scope: run the deliberately-failing-head experiment that `PR-GOVERNANCE-001`
section 7 records as not run, then replace that sentence with the dated result.

Protocol as executed:

1. Branch from the current `main` so the probe head is up to date with the base
   the protection payload applies to.
2. Add one always-failing `#[test]` to an existing test module. Not a formatting
   error: a formatting error would fail the format gate first and would not show
   that the workspace test can fail independently.
3. Confirm the repository still formats (`cargo fmt --all -- --check` exits 0), so
   the only intended failure is the probe.
4. Open a pull request and wait for `rust-workspace-test` to report.
5. Attempt the merge through `PUT /pulls/{n}/merge` and record the status code
   and message. Do not read `mergeable`: it is a cache and this experiment exists
   to test that assumption.
6. Record the result, close the pull request unmerged, keep the branch so the
   failing run stays reachable.
7. Replace section 7's "not run" sentence with a dated result, stating what the
   experiment does not prove.

Recorded, not committed: the probe branch is `governance/wo01c-failing-head` at
`b5cf4f25`; pull request #1038; check run `138943464904`.
