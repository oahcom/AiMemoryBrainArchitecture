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
        - "14-ai-development/work-items/AID-2026-254/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Structured task capture; source provenance is recorded as NOT_VERIFIED in the adjacent manifest."
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

# Executed prompt snapshot - AID-2026-254

Source: user-provided W11 task brief in the originating ChatGPT session.
Provenance: structured capture of the dispatched requirements, not a byte-for-byte platform transcript; source provenance is therefore NOT_VERIFIED.

## Required outcome

Create Work Item AID-2026-254 for W11 / Issue #265 AC8. Add a read-only, dependency-free measurement script under scripts/ that computes a reproducible attention/context-switching cost proxy from committed Work Item scope. Include at least one real repository measurement with exact source and output, define a budget and thresholds, and specify how to handle overruns.

Use only GitHub connector/API operations for repository changes. Do not change Issue #265 body or close the Issue. PR description must declare Related issue(s): #265, AI-assisted work: YES, and the resolvable session-evidence path. Merge only after all sixteen required contexts succeed on the exact head and the branch is current with main. Use a merge commit, then read back every changed file blob from main. After merge, leave a comment on Issue #265 with the metric definition, measured values, thresholds, and proposed AC8 wording.

Fixed attribution: user-authorized operator (delegated by account owner). Date: 2026-11-27. Work-item identifier: AID-2026-254.
