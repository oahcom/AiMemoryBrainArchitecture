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
        - "14-ai-development/work-items/AID-2026-345/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Local test suite passes; independent review is pending."
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
      - "work-item-uniqueness"
      - "shared-id"
      - "duplicate-declaration"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Executed prompt — AID-2026-345

Subagent CLAIM-LEDGER. Windows PowerShell 5.1, no WSL, isolated worktree
`D:\code\_aimb\wt-ledger3` on `origin/main` `daa935f7a7ecc808f1775be8cf153cf715961b08`.

## Problem statement (given, with two recorded incidents)

AID allocation has no atomicity, so two pull requests can claim one id inside
the same scan window. Two incidents prove it:

- `AID-2026-327`: free at start; taken by PR #1495 (`79b38c944`) while PR #1506
  was open; four add/add conflicts; #1506 renumbered to `AID-2026-341`.
- `AID-2026-292`: absent from `work-items/` and `INDEX.md`, yet held by the
  closed, unmerged PR #1467 and cited by Issue #264 and Issue #1332.

Both were caught by Git file-level conflicts, not by a uniqueness gate. The
adjudication forbids recording either as a checker success.

## Standing facts at the start

- `strict = false`; merge queue not enabled; no claim ledger on `main`.
- 17 required contexts; `enforce_admins = true`; force pushes disallowed.
- `scripts/ci/check_work_item_uniqueness.py` already implements a claim-ledger
  rule (`CLAIMED`/`MERGED` blocking, fail-closed on a candidate-supplied
  ledger), but `14-ai-development/work-items/registry/work-item-claims.yaml`
  does not exist on `main`, so the rule never fires.

## Ordered task

1. `git fetch origin --prune`; record the full `origin/main` SHA.
2. Read-only evidence: the existing uniqueness checker, any ledger
   implementation, the numbering clauses of `PR-GOVERNANCE-001.md`, whether CI
   reads the ledger and fails closed, `strict`, merge-queue state, the
   `concurrency` configuration of every workflow, and the two incidents.
3. Submit that evidence to the adjudication conversation and require an
   implementable design: which operation is actually atomic under Git and
   GitHub; ledger structure and location; the `CLAIMED` / `MERGED` /
   `ABANDONED` / `EXPIRED` state machine; coexistence with `strict=false` and
   no merge queue; fail-closed validator rules and the difference between
   "never registered" and "registered then released"; the relationship to the
   existing checker; and a migration for the historical work items that does
   not fabricate conflicts.
4. Transcribe the design mechanically, run the tests, quote real output.
5. Run a real concurrent claim: two branches declaring one id, showing that
   only one succeeds, and quote both outputs.
6. Push without force and open a pull request whose body carries
   `AI-assisted work: YES`, `Work Item ID:`, `Related issues:` and the session
   evidence reference. The id must be re-scanned immediately before use;
   `implementing_ai_session` must be a single token; `Related issue(s)` must
   name an Issue, never a pull request.
7. Poll the 16 declared contexts (60 s x 30). Do not merge.
8. Deliver `CLAIM-LEDGER.md` with the evidence, the adjudication text, the
   file list, the test output, the two race outputs, the pull request number
   and head, and the 16-context verdict.

## Hard constraints

No force push, no rebase, no merge, no change to another pull request, no
touch of the main worktree, no enabling of the merge queue, no change to
branch protection.
