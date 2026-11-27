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

Add assessor, assessed_version and evidence_baseline metadata to SYS-RISK-001 EN/ZH-CN and architecture-complexity-assessment EN/ZH-CN. Preserve each report's historical baseline and disclose provenance limits; do not fabricate a contemporaneous session signature. Add a deterministic read-only checker and tests under scripts/ci/. Run it in the existing required Schema non-empty audit (hard gate) job, without creating a new job or required context. Do not modify Issue #262 body or close it.
