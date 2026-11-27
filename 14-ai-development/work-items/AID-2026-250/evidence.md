---
document_metadata:
  steward: "Architecture Governance"
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
        - "14-ai-development/work-items/AID-2026-250/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "CI and post-merge verification pending."
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
---

# Evidence — AID-2026-250

## Scope and baseline
- Base: `386d8f57b02d8e3c511ff0e3980b9ce0af8b3028`
- Branch: `w7/aid-250`
- Related Issue: #262
- Four reports: SYS-RISK-001 EN/ZH-CN and architecture-complexity-assessment EN/ZH-CN.

## Historical provenance boundary
All four reports identify historical baseline `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. The metadata preserves that source baseline. SYS-RISK-001 does not record the original assessor session identity; that limitation is disclosed. The attachment does not retroactively prove a contemporaneous signature.

## Checker evidence
- Checker and tests: `scripts/ci/check_req_assessment_signatures.py`, `scripts/ci/test_check_req_assessment_signatures.py`.
- Exact PR Head execution and output: PENDING CI; no unexecuted result is represented as PASS.

## Integration
Reuse the existing `work-item-manifest-schema` job. No new job/context, branch-protection mutation, Issue body change, or Issue closure.

## Base synchronization
- A merge commit incorporated latest observed main `a588cd9914949c2c9db7b2c5704d906fd3f05b70` into the work branch before exact-Head verification: `8a6fe56b0a2a10018a6dbda1c546d7002eb3a64a`.
- This is a normal two-parent merge commit; no rebase, squash or force update was used.

## Base synchronization and PR traceability
- Latest observed main incorporated by merge commit: `6f597e2dd8b6e879bf7539aa16b88a39504d9c49`.
- Merge commit on the work branch: `bec645a11ab7cd206d04e6bb50f8e9d078adb7b1` (two parents; no rebase, squash or force update).
- PR: #1388. The PR description now includes the required per-Issue mapping table for #262.
