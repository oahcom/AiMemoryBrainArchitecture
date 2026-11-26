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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "The report, the PR #1195 commit and the residual passage locations named here were read at main = 3a859ac0 on 2026-11-26. Nothing in this prompt was measured by this session; the platform values it cites are reproduced from section 7.2.2 of the report, which records their own readback."
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

# AID-2026-097 prompt v1 — F-02 residual live assertions

## Task as delegated

Correct the residual live assertions in `00-governance/reports/bilingual-baseline-remediation-report.md`
on `main` that still state, in the present tense, that F-02 Requirement 2 is `NOT_VERIFIED` and that
F-02 overall is `PARTIAL`, after PR #1195 (merge `c6b7d987`, report v2.10) reclassified Requirement 2
as `COMPLETE / VERIFIED` on the 2026-11-25 measurement.

## Inputs supplied to this session

1. `00-governance/reports/bilingual-baseline-remediation-report.md` at `main`. Section 0 is the
   boundary rule this task obeys: bound assets (HEAD/tree/blob SHAs, run ids, historical readings,
   every `## D7 v2.x Revision Note`) are not edited; live assertions (finding states, normative
   statements, outstanding blockers) are.
2. PR #1195 / commit `c6b7d987`, whose v2.10 revision note enumerates the sections it changed, and
   therefore, by subtraction, the sections it did not.
3. The list of residual passages supplied by the delegating coordinator, located by content in the
   file rather than by line number.
4. The measured platform state recorded in §7.2.2 (2026-11-25): `GET /branches/main/protection`
   returned 200 with `strict: true`, `enforce_admins.enabled: true` and 16 contexts including
   `GOV-DOC-001 structural checks`; `GET /rulesets` returned 200 `[]`; `PUT /pulls/1038/merge` at
   head `b5cf4f25` was refused 405 with `Required status check "rust-workspace-test" is failing.`
5. Issue #283, the residual tracker, now CLOSED.

## Work-item number

The delegated identifier was `AID-2026-095`. By the time this session rebased onto current `main`,
that number was already taken by a Stage 0 registration record (`AID-2026-095`, A-I + Storage
end-to-end composition review package, PR #1264) merged on `main`. Per the delegation's instruction
to use the next genuinely free number and say so, this work item is `AID-2026-097`: `AID-2026-096`
is also on `main` (normative approval for Design Principles and Architecture Invariants), and no open
pull request claims 097.

## What was asked for

- Edit only the live assertions listed, in both language columns where the report is bilingual.
- Add `## D7 v2.11 Revision Note` and `## D7 v2.11 修订说明` after the v2.10 pair, in the same shape.
- Do not edit any `## D7 v2.1`–`## D7 v2.10` note, the §6.2 review-statistics table, or the §6.3 R6
  findings table.
- Open a pull request; do not merge it and do not un-draft it.

## Prompt provenance

The prompt text is a delegated coordinator request reproduced above in substance, not a verbatim
independent artifact. `prompt_provenance` in the manifest is `USER_AUTHORIZED_DELEGATED_REQUEST; no
independent prompt-source verification claimed`, and `executed_prompt_provenance` is `NOT_VERIFIED`.
