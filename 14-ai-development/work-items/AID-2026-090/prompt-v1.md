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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Metadata classification only. Prompt provenance and current ChatGPT session identity are not independently verified; see the evidence limitations below."
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
# AID-2026-090 — ContextVersion immutability
Authority: user-authorized operator (delegated by account owner)
Date: 2026-11-26
Issues: #1144, #1151
Apply the document-only decision in the canonical and EN/ZH-CN contract files. Define immutable fields, external mutable projections, append-only successor ChangeSet and expected-base semantics, digest binding, legal corrections and violation tests. Preserve G authority and cross-owner boundaries. Do not modify code, tests, schemas, validators, workflows, deployment or production. Open a separate Draft PR, post issue decision comments, leave both Issues OPEN. Repository Work Item ID AID-2026-090; any external workflow number is evidence only.
