---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The insertion point was read from main at 1ae2d07; the clause text is the one Owner accepted in Issue #262 comment 7153428650, reproduced without rewording apart from the appended non-exemption sentence, which is the answer to boundary question 5."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# WO — REQ 级风险评估的署名要求（AC2 of Issue #262）

Scope: put the four-item assessment-signature requirement into
`14-ai-development/PR-GOVERNANCE-001.md` §5, in both languages, immediately
after the paragraph that ends with "不得默默豁免", and answer the one boundary
question that blocks the change.

## What this instruction is carried out against

1. The clause text, verbatim, from Issue #262 comment `7153428650` ("记录二 AC2"):
   the four items — role, isolation constraint, signature, accountability — with
   the sentence "例外按 §5 末句显式记录，不得默默豁免。"
2. The landing point rationale: §5 is the only authority for session-level
   independence, and §9 already fixes its change path (bilingual semantic parity
   plus an exact-Head governance review). A new file would create a second
   independence authority, which the document-management policy calls a design
   error.
3. Boundary question 5, which the owner recorded as the only deferred item that
   blocks the merge: whether `EX-20261123-01` can cover this requirement.

## Acceptance asked for

1. §5 states all four items in English and in Chinese, with semantic parity —
   in particular the negative constraints, which are the ones that drift:
   the assessor "neither wrote nor implemented" the assessed object; role
   simulation inside one session "is not" an independent assessment; an
   overturned assessment "is not rewritten".
2. The non-exemption sentence appears in both languages and names *this
   paragraph* as the unit an exception record must name.
3. No existing sentence in §5 is deleted, reordered or reworded. The addition is
   an addition.
4. The approval metadata is not silently refreshed. `decision_status: Approved`
   and its `approved_version` content hash stay as they are; a merged change to a
   Canonical standard is not re-approved by the session that writes it, and
   `modification_status` already reads `Pending-Reapproval`.
5. The `-ENFORCEMENT` addendum is not claimed to be in parity beyond what it
   already is: it summarises §5 at its line 85 and is a different document, so it
   is left unchanged rather than edited to look consistent.
6. Any review recorded for this change states its independence at the session
   level and does not claim an account-level approval that does not exist.

## Excluded, and stated as excluded

- Anything in `crates/`. This is a normative document change.
- Re-approval of `PR-GOVERNANCE-001.md`. Owner acceptance of the *text* (comment
  `7153428650`) is the authority for the wording, not for the document's approval
  state.
- The other four boundary questions (assessor qualification, human signature,
  consequence of being overturned, whether the requirement reaches single-PR
  risk). They stay deferred; the owner recorded only question 5 as blocking.
