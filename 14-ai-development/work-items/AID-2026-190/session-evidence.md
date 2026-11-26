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
        - "14-ai-development/work-items/AID-2026-190/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the request as received, the environment it ran in and the commands whose output is quoted in evidence.md. No platform session identifier is available, so the session identity is recorded as NOT_RECORDED rather than inferred."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session Evidence — AID-2026-190

## Session role / use case

Annotation worker inside a dispatched repair contract. The assistant was told to read two
operator-side briefs (`fix-brief-common.md` and `unit-auth02.md`), work only in the
worktree `D:\code\wt-auth02` on branch `fix/2026-11-27-dangling-09-refs`, produce a
complete list of the `09-security-governance/` documents cited but absent from main with
every referencing `file:line`, apply a minimal in-place fix at each citation, create no
referenced file, edit no normative body, and publish the result as a work item plus one
`INDEX.md` row.

The role it actually performed was: measure the defect, classify every occurrence,
annotate the ones that could be annotated without a second change, and stop at the ones
that could not — recording the gate's own rejection rather than working around it.

## Actual AI input

The dispatched contract instructed the assistant to:

- read `fix-brief-common.md` and `unit-auth02.md` and execute end to end without asking
  questions;
- work only in `D:\code\wt-auth02` on `fix/2026-11-27-dangling-09-refs`, fetch and merge
  `origin/main` first, and treat a non-empty `git status` as its own uncommitted work;
- take a work-item number only after checking the PR list for occupation, and stop rather
  than open a duplicate PR if another PR already does the same work;
- build `14-ai-development/work-items/AID-2026-<NNN>/` with `manifest.yaml`,
  `evidence.md`, `prompt-v1.md`, `session-evidence.md`, two `docs/` mirrors of the
  evidence and one appended `INDEX.md` row;
- for unit auth02 specifically: produce the full path-plus-`file:line` inventory in the
  evidence, apply the note `(not restored on main; see AID-2026-107 §10)` while keeping the
  original path text, demote any clickable link to plain text, create no referenced file,
  edit no normative body, and run `check_bilingual_docs.py` plus
  `check_document_management.py` to confirm nothing turns red;
- never change branch protection, never close an Issue, never delete a required context,
  never edit files unrelated to the unit, and never fabricate a SHA, a test output or a
  gate result.

The full contract text is captured verbatim in `prompt-v1.md`.

## AI-visible output

Visible in the branch:

- 30 annotated lines in 19 documents, each keeping its original path text and gaining the
  one parenthetical note; the complete before/after inventory is evidence sections 3 and 4.
- Six live citations in four `13-engineering-decisions/` documents left unchanged, with
  the bilingual gate's verbatim rejection quoted in evidence section 5.3 as the reason.
  Those edits were applied first, measured, and reverted.
- Local gate output in evidence section 6: bilingual gate PASS with `77 frozen, 0 new
  gaps`; document-management gate `INCOMPLETE`, identical before and after the change;
  line endings, manifest parse, repository hygiene, session-evidence shape, traceability
  and governance-traceability all PASS.
- No file was created under `09-security-governance/`, no reference was deleted, and no
  path text was reworded: `git grep -F <path>` still finds all 300 occurrences.

Visible to the assistant but not reproduced here: the operator's briefs are the only
context it had; no Issue thread, PR discussion or platform session identifier was
provided, so none is claimed.
