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
        - "14-ai-development/work-items/AID-2026-279/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured task capture; it is not a byte-for-byte platform transcript."
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
    canonical_scope_keywords:
      - "prompt-snapshot"
      - "work-item-uniqueness"
      - "merge-time-gate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-279 Prompt Snapshot

Source: user-provided task in the S6-A implementation conversation.
Capture status: structured task snapshot, not a raw platform transcript.
Date: 2026-11-27.

Implement Issue #1341 as a serialized merge-time work-item uniqueness gate in
oahcom/AiMemoryBrainArchitecture using GitHub API only. A candidate newly
introducing an AID-YYYY-NNN directory must be rejected when the identifier
is already present on the latest target branch. New files beneath a directory
already present at merge-base must be accepted. Exit codes: 0 PASS, 1
VIOLATION, 2 INCOMPLETE; missing refs or unreadable Git state never pass.

Create scripts/ci/check_work_item_uniqueness.py and
scripts/ci/test_work_item_uniqueness.py. Wire both explicitly into the existing
GOV-DOC-002 metadata checks job, which is already a required context; do not add
a job or alter the 16 required contexts. Use PR_BASE / PUSH_BEFORE selection,
with push base github.event.before. Do not modify branch protection,
check_manifest_blob_pins.py, or repository-hygiene.yml. Use a unique
work-item number in 260-279, preserve block-style YAML metadata, include
required PR evidence declarations, and provide actual execution, open-PR,
serialization, and post-merge evidence.
