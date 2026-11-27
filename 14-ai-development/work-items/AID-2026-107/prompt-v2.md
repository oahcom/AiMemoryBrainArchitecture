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
        - "14-ai-development/work-items/AID-2026-107/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Supplemental prompt snapshot recorded from the user-authorized IMPL2 scope-adjudication request; original platform payload bytes are not independently exposed."
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

AID-2026-107 supplemental prompt v2: Append the user-requested IMPL2 file-by-file scope adjudication to the existing AID-2026-107 work item. Compare the exact main tree with Owner branches session-d-memory-brain-2026-11-16, session-e-memory-compiler-2026-11-16, session-f-memory-runtime, and session-i-security-governance-2026-11-16. Classify every missing path as NORMATIVE_ROOT, HISTORICAL_PHASE_RECORD, or UNDECIDED with an evidence-based reason; count by directory; do not restore historical or undecided files without Owner ruling; put normative-root restoration in a separate PR; update Gate A item 5, keep Gate A/B PARTIAL / OPEN, keep #1212 open, update Canonical/EN/ZH-CN and manifest/index, create a Draft PR and merge only after 16 exact-Head checks pass.
