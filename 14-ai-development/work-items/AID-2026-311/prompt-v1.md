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
        - "14-ai-development/work-items/AID-2026-311/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Implementation and CI verification are pending independent review."
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
      - "merge-queue"
      - "claim-identity"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# Prompt Snapshot — AID-2026-311

## Task

Repair Issue #1341's work-item uniqueness mechanism after independent acceptance found that Update branch can move merge-base past the original claim. Two PRs from one old base may create different files beneath the same AID directory; after A merges and B updates its branch, the previous checker can see no introduced directory and pass.

## Required design

- Preserve the original claim identity across merge-based Update branch.
- Serialize actual candidate evaluation through GitHub Merge Queue `merge_group`.
- Compare the candidate's claim against the event's latest base.
- Bind the decision to the exact candidate SHA and fail closed on missing or unreadable inputs.
- Keep positive, negative, additive and race-reproduction regression coverage.
- Do not change branch protection or enable merge queue; report those as administrator prerequisites.
- Do not merge the PR, force-push, squash, or close Issue #1341.

## Execution constraints

Use only GitHub REST/Contents API through the GitHub connector. Do not use shell, local worktrees, or local test execution. Use the reserved AID-2026-311 through AID-2026-318 range after checking the work-items directory and all-state pull requests.

## Acceptance boundary

CI must execute the new Update-branch regression on the exact PR head. A real GitHub race test remains pending until merge queue is enabled and a controlled A/B candidate sequence can be observed.
