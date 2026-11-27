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

# AID-2026-251 dispatched task snapshot

Repository: oahcom/AiMemoryBrainArchitecture
Base branch: main
Assigned work item: AID-2026-251
Related issue: #266

Define a block-style YAML schema for Work Item manifests under
14-ai-development/work-items/. The schema must define the required top-level
key set and the documentation, session_evidence, and implementation shapes.
Add a read-only checker under scripts/ci/, integrate it into the existing
workflow job pattern without adding dependencies, and report all current
manifest compliance and violations without migrating existing manifests.
Preserve issue #266 as open. PR metadata must include the Related issue(s),
AI-assisted work declaration, and session evidence reference. Use the
delegated operator attribution and date 2026-11-27.

The operator must report only GitHub-observed CI, merge, and blob verification
results; do not fabricate check results or SHAs.
