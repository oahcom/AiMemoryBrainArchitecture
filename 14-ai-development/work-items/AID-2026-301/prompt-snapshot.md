---
document_metadata:
  domain: ai-development
  role: work-record
  steward: user-authorized operator (delegated by account owner)
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
        - "AID-2026-301/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Provisional implementation evidence; exact-Head CI and independent review control acceptance."
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
    canonical_scope: "Structured task-input snapshot for AID-2026-301"
    canonical_scope_id: "ai-development/aid-2026-301-prompt"
    canonical_scope_keywords:
      - "issue-1350"
      - "implementation-scope"
      - "manifest-blob-pins"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-301 implementation input snapshot

Source: user-provided implementation task in this ChatGPT conversation.
Capture status: RECORDED_NOT_FROZEN — this file is a faithful task-scope summary, not a byte-for-byte export of the complete conversation input.

Objective: close the independent-review FAIL row for applicable-field discovery in Issue #1350. Enumerate all applicable manifest blob identity shapes and their locators/algorithms/definition locations; resolve every declaration against committed bytes; report missing paths and unresolved commits/locators as failures; never silently skip an applicable field or allow pins=0/rc=0.

Known missed shapes:
- AID-001 top-level prompt_sha256 with prompt_version v2 => prompt-v2.md, SHA-256.
- AID-004 source_translation_pairs[].source_path/source_blob_sha and translation_path/translation_blob_sha, with their own commit locators.
- AID-023 source_blobs[].path/sha.
- AID-109 source.selected_source_files[].path with source_blob_sha, restored_blob_sha and frontmatter_blob_sha.
- AID-150 source.files[].path/blob.

Acceptance: explicit registry; fail-closed parser; changed-byte, deleted-path and unavailable-commit negative controls; exact-line baseline disposition; all tests and existing traceability/hygiene/bilingual regression checks; open PR only, no merge before independent review.
