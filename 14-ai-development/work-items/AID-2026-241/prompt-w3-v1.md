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
      evidence_reference:
        - "AID-2026-241/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "This is a concise W3 task-input summary, not a verbatim transcript of the chat prompt."
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
    canonical_scope_keywords:
      - "independent-review"
      - "session-identity"
      - "governance-gate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# W3 execution input summary

Repository: `oahcom/AiMemoryBrainArchitecture`, default branch `main`. Continue PR #1325, which changes the independent-review gate to compare sessions rather than GitHub identities for Issue #1247. Rename the colliding work-item directory `AID-2026-082` to the reserved `AID-2026-241`, updating all self-references, prompt paths, session evidence, evidence, and INDEX. Recompute the SHA-256 over the renamed prompt file bytes and record the old and new values. Merge the current `origin/main` into the PR branch, preserving both sides of any concurrent edits. Push the updated existing PR branch. Require all 16 required contexts to succeed on the exact PR head, with strict branch protection and zero behind count; use a merge commit only. After merge, verify each changed path's blob against `origin/main` and leave a comment on Issue #1247 naming the PR and merge SHA without closing the Issue.

Repository-operation prohibitions: no squash, no rebase merge, no force push, no branch-protection changes, no fabricated SHAs or check results, and no closing Issue #1247. If a red check is outside this work item's scope, stop and report its exact name and log output.

Attribution: user-authorized operator (delegated by account owner), 2026-11-27.
