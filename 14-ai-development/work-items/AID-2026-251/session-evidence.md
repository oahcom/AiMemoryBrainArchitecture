---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-251/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Session artifact; provenance is recorded in the adjacent manifest."
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

# Session role / use case

Role: implementation and repository governance operator.
Use case: define a Work Item manifest schema and a read-only checker for
Issue #266 AC4, preserving all existing manifest contents.

# Actual AI input

The user instructed the assistant to create AID-2026-251, define the required
manifest key set and the documentation/session_evidence/implementation shapes,
add a read-only checker under scripts/ci, integrate it into the existing CI
workflow, quantify legacy violations without migrating them, and report the
merge and post-merge verification. The user specified that the PR body must
reference a real Issue, include AI-assisted-work disclosure and this file path.

# AI-visible output

The assistant produced the schema at
`14-ai-development/work-items/work-item-manifest.schema.yaml`, the checker at
`scripts/ci/check_work_item_manifest_schema.py`, and a workflow job invoking
the checker. Existing manifest files were left unchanged. The measured CI
result, merge SHA, and post-merge blob comparisons are recorded only after
GitHub reports them.

署名：user-authorized operator (delegated by account owner)
日期：2026-11-27
