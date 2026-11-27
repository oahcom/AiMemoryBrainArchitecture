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
        - "14-ai-development/work-items/AID-2026-109/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured prompt snapshot for the W5 correction session; provenance is not independently verified."
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
    canonical_scope: "AID-2026-109 W5 prompt snapshot"
    canonical_scope_id: "ai-development/aid-2026-109-w5-prompt-snapshot"
    canonical_scope_keywords:
      - "ai-development"
      - "prompt-snapshot"
      - "session-evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-109 / W5 session prompt snapshot

Prompt status: structured scope snapshot, not a verbatim transcript.
Attribution: user-authorized operator (delegated by account owner).
Date: 2026-11-27.

## Actual task input

The user assigned W5: repair PR #1334 for the existing AID-2026-109 work item, without renumbering. The user required the canonical session-evidence file to contain the sections "Session role / use case", "Actual AI input", and "AI-visible output"; the work-item manifest must contain a session_evidence entry pointing to that file. The PR body must state the real Issue #1332, "AI-assisted work: YES", and the canonical session-evidence reference. The user required synchronizing the PR branch with current main, converting the draft PR to ready, requiring all 16 required contexts to succeed, and merging with the merge method only. After merge, the user required verification of each changed path's main-branch blob and a comment on Issue #1332 explaining that PR #1334 is not content-equivalent to PR #1312, with the PR number and merge SHA.

The user supplied hard constraints: do not use reserved work-item numbers 241–259; preserve AID-2026-109; use block-style YAML for metadata; do not claim AI-assisted work without a manifest declaration; do not use squash, rebase merge, force push, branch-protection changes, or Issue closure; merge current main into the branch and require behind=0; do not fabricate SHAs or gate results; if an out-of-scope gate fails, stop and report its exact name and log; use attribution "user-authorized operator (delegated by account owner)" and date 2026-11-27.

A subsequent user instruction required using only GitHub connector/API operations, not a local work directory, and asked for execution through merge plus a report of PR number, head SHA, all 16 contexts, merge SHA, and post-merge blob verification.

## Scope boundary

This is documentation/evidence correction only under existing AID-2026-109. It does not allocate a new work-item ID, modify production code, close Issues, grant normative acceptance, or assert a natural-person Owner signature.
