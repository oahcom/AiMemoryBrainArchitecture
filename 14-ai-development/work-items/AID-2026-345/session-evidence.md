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
      last_verification_note: "Local suite passes; independent review is pending."
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
      - "merge-group"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session evidence — AID-2026-345

## Session

- role: `IMPLEMENTATION_SESSION`
- orchestrator session: `CLAIM-LEDGER` subagent of the governance orchestration
  session, isolated worktree `D:\code\_aimb\wt-ledger3`
- model family: `9router` / `hermes` routed through the host adapter
- platform: Windows, PowerShell 5.1, no WSL
- base: `origin/main` `daa935f7a7ecc808f1775be8cf153cf715961b08`, merged forward
  to `bf7fd91cbb3ccad4d2dba5662b14b849e446d706` before the ledger bootstrap

## Adjudication input

The design was not authored in this session. The evidence in `evidence.md`
sections 1–3 was submitted to the adjudication conversation
`6b0a52f1-afe4-83ec-992c-ff404f45cbb7` (prompt `ledger-1b.md`, reply
`reply-6b0a52f1-120720.md`, copied to `ledger-reply-1.md`) and its text was
transcribed mechanically. The adjudication's own summary:

> The root cause is not that the checker lacks a duplicate-id test, it is that
> there is no authoritative write point that can produce a single winner between
> concurrent claims. `CLAIMED`/`MERGED` in the existing checker is only a static
> validation. Pull-request concurrency, required contexts and strict protection
> cannot replace a claim transaction.

Two of the adjudication's proposals were dropped in the final transcription and
the reason is recorded rather than hidden:

- the per-id `refs/heads/work-item-claims/<ID>` design was superseded by the
  adjudication's own final section (one ref, one file), so no per-id ref exists;
- a ref-versus-YAML consistency check has no subject when the YAML *is* the ref
  content.

## Executed work

1. Read-only evidence pass: the checker, `aid-ledger.yaml`, `PR-GOVERNANCE-001.md`,
   the workflow wiring, live branch protection, merge-queue state and the
   `concurrency` blocks of all 12 workflows.
2. Adjudication round trip; the reply is stored verbatim in
   `D:\code\_aimb\round\ledger-reply-1.md`.
3. Transcription: `claim_work_item.py`, `migrate_work_item_claims.py`,
   `test_work_item_claims.py`, the checker patch and the workflow wiring.
4. Migration and bootstrap of `refs/heads/work-item-claims` at
   `0a3fc6e476f89e66ff3bcdaf3b6a10a2d6903ece`.
5. Three experiments: same-id race, different-id race, gate rejection of the
   losing record. Outputs are quoted in `evidence.md` section 7.
6. Pull request opened; the id is claimed on the authoritative ref with that
   pull request number before the checks are re-run.

## Limits

No merge, no rebase of published work, no force push, no change to branch
protection or the merge queue, no change to another pull request.
