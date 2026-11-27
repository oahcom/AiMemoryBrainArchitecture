---
document_metadata:
  steward: "AID-2026-251 delegated repair operator"
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
        - "14-ai-development/work-items/AID-2026-251/ac4-repair-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Operator-prepared compact snapshot; not a verbatim platform transcript."
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
    canonical_scope_keywords:
      - "AID-2026-251"
      - "AC4"
      - "prompt-snapshot"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-251 AC4 repair — operative prompt snapshot

This is a compact operator-prepared record of the operative R2 instruction, not a verbatim platform transcript; the manifest therefore records executed_prompt_provenance as NOT_VERIFIED.

The user ruled that this work repairs AID-2026-251 itself and must not create a new AID. Use branch fix/aid-2026-251-ac4-repair, add the incremental evidence file ac4-repair-evidence.md, and leave PR #1366 untouched.

The four measurable repairs are: documentation must contain at least one entry; each documentation path must exist in the Git tree; the contradictory .md suffix restriction must be removed so real .py/.yaml paths are accepted; and violations must produce exit 1 while the work-item-manifest-schema job runs as a blocking CI job.

Resolve the GOV-DOC YAML parser conflict using option A: support only flat sequence-of-mapping records and add regression tests; do not broaden support for nested mappings or other YAML constructs.

Migrate exactly the 83 manifest paths in tree e47dd6f0 (82 AID-2026 manifests plus FIX-2026-P1-T1). Add only documentation fields using paths already referenced by each manifest and present in the current tree. AID-2026-030 must reference its actual Python deliverable.

Record real before/after batch outputs, the 83/83 list, required-context results, and GitHub-observed verification. Do not claim unobserved results, do not modify branch protection, do not squash/rebase merge, and preserve concurrent main changes.
