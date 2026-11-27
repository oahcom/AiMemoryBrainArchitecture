---
document_metadata:
  steward: "Architecture Governance"
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
        - "14-ai-development/work-items/AID-2026-250/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Session prompt snapshot; provenance is recorded in the adjacent manifest."
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
# AID-2026-250 — implementation prompt

Repository: oahcom/AiMemoryBrainArchitecture
Base: main@386d8f57b02d8e3c511ff0e3980b9ce0af8b3028
Branch: w7/aid-250
Issue: #262

The four in-scope assessment records are the primary REQ-01 risk assessment comments on Issue #262:
- comment 7011312621 — initial architecture internal technical risk assessment
- comment 7014315135 — supplemental clarification to that assessment
- comment 7143927480 — Round 26 consolidated assessment
- comment 7149369280 — Round 29 final investigation assessment

Append three metadata fields to each existing comment body without rewriting its historical assessment content:
- assessor: the original authoring session/principal recorded by that comment
- assessed_version: the full 40-character commit the assessment evaluated
- evidence_baseline: the full main@commit snapshot from which the assessment evidence was taken

Preserve the historical nature of the records and explicitly disclose that the metadata attachment is retrospective; do not claim a contemporaneous signature, risk acceptance, or approval.

Add a deterministic, read-only checker under scripts/ci/ that retrieves exactly those four GitHub Issue comments through GET API calls and fails closed if any record or field is missing, if the assessed_version is not a full SHA, or if the values differ from the historical source baseline. Add unit tests with a mocked API reader.

Run the checker and tests inside the existing required Schema non-empty audit (hard gate) job. Add only the minimum issues:read permission needed for GET; do not create a new job or required context. Do not change Issue #262 body or close the Issue.
