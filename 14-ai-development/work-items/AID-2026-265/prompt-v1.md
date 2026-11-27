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
        - "14-ai-development/work-items/AID-2026-265/manifest.yaml"
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
      - "index-table-integrity"
      - "document-management"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-265 Prompt Snapshot

Source: user-provided task in the coordination conversation that carried the
FIX-1325 repair of PR #1325.
Capture status: structured task snapshot, not a raw platform transcript.
Date: 2026-11-27.

Open a standalone pull request that repairs the split `AID-2026-190` row in
`14-ai-development/work-items/INDEX.md` on the current `main`, and register this
work item.

Required sequence:

1. Re-read the row in the current `origin/main` blob. If it is already repaired,
   stop and report `ALREADY_FIXED_ON_MAIN:<commit>` instead of opening a pull
   request.
2. Confirm the work-item number `AID-2026-265` is unoccupied in three places:
   the `14-ai-development/work-items` tree on `origin/main`, `aid-ledger.yaml` on
   `origin/aid-ledger`, and remote branch names. If any check hits, stop; do not
   renumber unilaterally.
3. Branch from `origin/main`, take only the one-line INDEX repair, and register
   the work item in the same commit.
4. The new work item's own INDEX row must be written into the same file that is
   being repaired, so the final file is its own self-check: every row complete on
   one physical line, consistent column count, no control characters.
5. Run `scripts/check_traceability.py --index-only`,
   `scripts/check_document_management.py`,
   `scripts/ci/check_repository_hygiene.py --base origin/main --head HEAD`, and
   `scripts/check_bilingual_docs.py`; record raw output.
6. One commit, one push, no force. Do not merge, do not close issues, do not
   touch the already-merged #1325 branch, do not modify the primary worktree.

Acceptance for this work item: the repaired row carries ten pipe separators, the
word `verification_status` is complete, the file contains no control characters,
the count of `^|` lines grows by exactly the number of rows added, and the row
pair is gone from `main` after merge.
