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
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Metadata classification only. Prompt provenance and current ChatGPT session identity are not independently verified; see the explicit evidence limitation below."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
work_item_id: AID-2026-089
authorization:
  authorized_by: "user-authorized operator (delegated by account owner)"
  decision_date: "2026-11-26"
external_evidence_reference:
  workflow: "AID-2026-11-26-FORGET-FENCE-01"
  issues: ["#1125", "#1211"]
repository:
  base_branch: main
  base_commit_sha: 8d90843aec4583c3282a3b45da31c7d6fd734cf2
  branch: docs/forget-fence-authority-2026-11-26
  pull_request: 1232
decision:
  logical_authority: D
  storage_role: "physical durability/recovery and derived rebuildable projections only"
  owner_acceptance: PENDING
  normative_approval: NOT_CLAIMED
  implementation_authorization: NOT_GRANTED
verification:
  criteria:
    FF-01: "D sole logical issuer"
    FF-02: "Storage rows projection-only"
    FF-03: "Typed target + source + Scope + lineage"
    FF-04: "Fail closed on stale/missing/corrupt/underscoped authority"
    FF-05: "D-domain and I-global completion separated"
    FF-06: "EN/ZH-CN semantic parity"
    FF-07: "Issue comments posted; Issues remain OPEN"
  ci_status: PENDING
  owner_review: PENDING
session:
  implementing_ai_session: NOT_RECORDED
  provenance: NOT_VERIFIED
  session_reference_status: NOT_RECORDED
  session_reference_reason: "The exact current ChatGPT session identifier is not exposed in the available execution context. Historical session identifiers belong to other sessions and were not substituted."
prompt:
  file: 14-ai-development/work-items/AID-2026-089/prompt-v1.md
  sha256: 58dd684c5eb6e5d727bf232aed00f1c34620fc27567396cff192fe1479e0329d
  bytes: 4258
  provenance: NOT_VERIFIED
  provenance_reason: "The committed prompt text is available, but no immutable raw-source capture proves byte-for-byte origin."
