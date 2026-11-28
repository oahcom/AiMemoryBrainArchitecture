---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# AID-2026-003-PROMPT v1 — retrospective correction addendum

- Record type: immutable-prompt companion / errata (not a replacement of prompt-v1.md)
- Applies to: `AID-2026-003-PROMPT v1` at `prompt-v1.md`
- Authority: remediation dispatch and Owner's F-2/F-4 closure conditions in PR #256
- Status: PROPOSED correction record; does not retroactively alter the executed prompt or claim this addendum was the original kickoff instruction.

## 1. Identity

- Work Item: AID-2026-003
- Issue / PR: #218 / #256
- Prompt ID/version: AID-2026-003-PROMPT v1 (historical prompt); this file is its supplemental correction record, not a new executed prompt version.
- Owner: Integration Owner
- Session role: REMEDIATE Implementer; not reviewer or acceptance authority.

## 2. Objective

Preserve the exact historical bytes of prompt-v1.md while supplying the omitted State of knowledge facts and bilingual scope/acceptance requirements identified by F-2 and F-4.

## 3. Baseline

- Repository: oahcom/AiMemoryBrainArchitecture
- Branch: ai/AID-2026-003/IO-exec-v11
- Base branch: main
- Full base commit: 6b5db2918cffc2281deb22fd9858a37dbaeec726
- Initial PR Head: ef3aa3e96271ccffe1482931069f30dfa9b1eb2a
- Historical prompt file: 14-ai-development/work-items/AID-2026-003/prompt-v1.md
- Historical prompt introduction commit: bb1ac7a59619e56769ac1e69c272a772f8c96b02

## 4. Authority

This record does not amend or replace the executed prompt. The historical prompt remains immutable under AI-EXEC-002 §2 and AI-PROMPT-STD-001 §5. Any future substantive instruction change requires a separately versioned prompt before execution. This addendum records missing archival context and the explicit remediation constraints; it does not authorize merge or acceptance.

## 5. Scope

- Repair AI-EXEC-001/002 v1.1 rule defects F-1 and F-5 through F-7.
- Preserve prompt-v1.md bytes; attach this correction record rather than editing the executed file.
- Record bilingual work for both normative Chinese sources and their English counterparts:
  - Chinese authoritative source: 14-ai-development/AI-EXEC-001.md, v1.1
  - Planned English counterpart: docs/en/14-ai-development/AI-EXEC-001.md
  - Chinese authoritative source: 14-ai-development/AI-EXEC-002.md, v1.1
  - Planned English counterpart: docs/en/14-ai-development/AI-EXEC-002.md
- Non-goals: resolve the three disclosed upstream conflicts, complete the English translations in this remediation, or change upstream standards.

## 6. State of knowledge

### DECIDED
- AI-EXEC-001/002 v1.0 remain ADOPTED until the project Owner adopts v1.1.
- PR #256 disposition is REMEDIATE; it must not be merged by this implementer.
- R3 specialist review and reproducible test evidence are non-waivable prerequisites to acceptance and merge.
- Historical prompt-v1.md is immutable; this companion record is the correction path.

### CANDIDATE
- Revised clause wording in AI-EXEC-001/002 and the bilingual exception registration in docs/translation-status.md are candidate remediation text pending exact-Head Owner review.

### OPEN
- The three upstream conflicts (15-vs-12 prompt structure, TESTED-vs-VERIFIED vocabulary, and SHA-256 mandatory-vs-NOT_VERIFIED) remain assigned to Issue #218.
- English counterparts remain outstanding under the explicitly time-bounded exception.

### TO_VALIDATE
- Exact final Head and file line references.
- Cross-file consistency of R3, grandfather, prompt-structure, interop, provenance and bilingual exception terms.
- SHA-256 of historical prompt bytes; do not infer or copy a prior reported digest as a newly verified result.

## 7. Required steps

Inspect frozen base and current PR Head; remediate F-1 first; then F-5/F-6/F-7; then F-2/F-3/F-4; preserve the prompt-v1 historical bytes; update manifest and INDEX with verified provenance; publish finding closure evidence to existing PR #256 and Issue #218 only.

## 8. Acceptance criteria

- The complete 12-item prompt structure is represented across the immutable prompt and this companion record, including all four State of knowledge categories and concrete facts.
- Bilingual work appears explicitly in scope and acceptance: both English counterparts are tracked; Chinese v1.1 is the temporary authoritative source; the exact source revision, missing counterpart paths, accountable Owner, due date, and tracking Issue are registered.
- The exception is not completion: English counterparts must be updated before the next dependent architecture baseline is accepted and no later than 2026-12-02.
- No claim of bilingual parity or acceptance is made by this implementer.

## 9. Verification

Verify exact source file revisions, the 12-item structure, four knowledge states, bilingual exception fields, and cross-reference consistency. SHA-256 is NOT_VERIFIED unless computed from exact committed bytes. Runtime and test suites are NOT RUN for this documentation-only change.

## 10. Git workflow

Use only branch ai/AID-2026-003/IO-exec-v11 and existing PR #256. Keep prompt-v1.md unchanged. Record this companion file's actual introduction commit in manifest/INDEX after creation. Do not merge.

## 11. Stop / escalation

Stop on baseline drift, upstream conflict, missing write permission, or inability to prove a closure condition. Keep the affected finding OPEN and return it to Issue #218. Never treat COMMENT as APPROVE, NOT RUN as PASS, or a missing record as proof of historical noncompliance.

## 12. Evidence and final report

Record the addendum path, its introducing commit SHA, prompt-v1 introduction commit SHA, full base SHA, exact final Head, finding ID/severity/feedback destination, and all verification states. Owner exact-Head review and merge decision remain outstanding.
