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
        - "14-ai-development/work-items/AID-2026-242/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-242/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Captured from the current user instruction; exact execution/session identifier is not exposed by the chat runtime."
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
    canonical_scope: "AID-2026-242 W4 renumbering and merge task prompt"
    canonical_scope_id: "ai-development/aid-2026-242-prompt-v2"
    canonical_scope_keywords:
      - prompt-snapshot
      - renumbering
      - merge-conflict
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-242 prompt snapshot v2 — W4

The user authorized work on `oahcom/AiMemoryBrainArchitecture`, default branch `main`, expected baseline `788fbc01` (verify by fetch). Continue PR #1297: rename the D work item's `AID-2026-109` directory to `AID-2026-242`, update internal references and prompt digest, and record the renumbering in evidence.

The user requires a real `git merge origin/main`, with the main-side current implementation of `scripts/check_bilingual_docs.py` and the branch-side intended change inspected before resolving. Preserve main behavior and any branch-only capability; do not replace the entire file with one side without analysis. Run `python scripts/test_check_bilingual_docs.py` if present and `python scripts/check_bilingual_docs.py`, recording exact output.

Push the updated branch. If the new PR head has zero Actions runs within three minutes, do not wait: rebuild from `origin/main` with a merge commit, open a replacement PR, comment on and close the original PR. Do not fabricate checks.

Require all 16 required contexts successful, `strict` and `enforce_admins` true, `behind_by` zero, and merge using the merge method only. Refresh status immediately before merge and verify every changed file's blob SHA on merged `origin/main`. Do not squash, rebase-merge, force-push, alter branch protection, or close Issue #1212.

PR body must contain `Related issue(s): #1212`, `AI-assisted work: YES`, and the exact `Session evidence reference(s): 14-ai-development/work-items/AID-2026-242/session-evidence.md`. Attribution: `user-authorized operator (delegated by account owner)`, date `2026-11-27`; any adjudicative wording must say `代理裁决，非自然人 Owner 签署`.

Only modify this work item's scope. Preserve main's distinct AID-2026-109 I work item. Keep block-style YAML metadata; do not use flow mappings. Report rename paths, both sides' checker diff and resolution rationale, local test outputs, exact new head, all 16 contexts, merge SHA and per-file blob verification.
