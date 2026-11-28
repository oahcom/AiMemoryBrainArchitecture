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
        - "14-ai-development/work-items/AID-2026-325/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "This reference records the operative task and supplied inputs; byte-for-byte prompt provenance remains NOT_VERIFIED."
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
    canonical_scope: "Reference record of the decision-authoring task and its required boundaries for AID-2026-325."
    canonical_scope_id: "ai-development/aid-2026-325-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-325"
      - "prompt"
      - "decision-authoring"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Prompt v1 — AID-2026-325

## Purpose

Author a documentation-only decision record closing the adjudication of
Issue #1247 in `oahcom/AiMemoryBrainArchitecture`.

The code correction is already merged through PR #1325. The remaining work
is to record the decision, its evidence, its limitations, and the disposition
of the considered alternatives. This task does not authorize another code
change.

## Operative decision question

The original independent-review gate compared normalized GitHub account
identities. PR-GOVERNANCE-001 §5 now defines independence by reviewing
session, not by GitHub account.

The decision record must explain why the retired identity criterion fails
in a repository with one measured direct write-capable account, why it
remained invisible, and why the session-declaration implementation is the
selected path.

## Required dispositions

1. Session declaration plus explicit NOT_ASSIGNED accounting:
   TAKEN. Record the merged implementation and its verification, including
   the fact that session strings are declarations and not proof of distinct
   execution contexts.

2. Keep identity comparison and mark the gate unsatisfiable:
   REJECTED. It contradicts the amended session-level clause and would
   permanently prevent lawful same-account, separate-session reviews.

3. Cancel the gate and demote §5 to process prose:
   REJECTED. It removes the executable visibility of a mandatory invariant.

## Required carrier boundary

This work item is documentation only.

It does not modify:

- `14-ai-development/PR-GOVERNANCE-001.md`
- `scripts/governance/status_migration/check_status_gates.py`
- `scripts/governance/status_migration/test_status_migration.py`

The dead `_same_account` diagnostic and the absence of CI wiring are
separate unresolved residuals. Neither is fixed here. Each requires its
own work-item carrier and acceptance criteria.

## Required deliverables

- `manifest.yaml`
- `decision.md`
- `evidence.md`
- `session-evidence.md`
- `prompt-v1.md`
- Exactly one row in `14-ai-development/work-items/INDEX.md`

The decision record is primary. The evidence record must distinguish the
independent verification measurements from the later 130-manifest corpus
measurements.

## Required provenance limitation

The authoring session must not claim to be an independent reviewer of its
own record. It must not assert Owner acceptance. Session identity and
prompt provenance remain NOT_VERIFIED unless independently corroborated.

The manifest must retain the supplied placeholders for session ID, prompt
SHA-256, prompt byte count, and PR number until mechanical substitution.

## Input authority

The operative factual inputs are the Issue #1247 body and comments, the
current implementation excerpts, the PR-GOVERNANCE-001 §5 excerpts, and
the measurements supplied in the task dated 2026-11-27.

Measurements must not be silently changed, conflated, or supplemented
with invented values.
