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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every command and every count in this record came from the session that ran it. What it cannot support - that the change was independently reviewed - is stated as not supported rather than argued."
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

# Session role / use case

IMPLEMENTER -- close the fail-open hole in the Session Evidence gate, where a pull request body that
declares nothing passed as `NOT_APPLICABLE`.

# Actual AI input

The actual prompt supplied to the AI:
Make a pull request body that omits `AI-assisted work` fail the Session Evidence gate. Keep a declared
`NO` with `N/A` references passing. Keep a declared `YES` requiring a reference that exists in the PR
head tree. Add a test for each case. Relax no existing refusal.

# AI-visible output

The actual output returned by the AI:

- Located the hole at `scripts/governance/session_evidence/validate.py:2195-2203` -- an early return to
  `_not_applicable_verdict` guarded by `pr_created < ctx.effective_at`, `_historical_not_applicable(ctx)`
  and both declaration fields being absent. `_parse_status` already raised on a missing field, so the
  brief's named location was wrong and the fix is at the early return.
- Removed that early return. `check_01_pr_fields_and_issue_references` now runs for every PR.
- Inverted the two tests that pinned the exemption
  (`test_pre_effective_undeclared_pr_is_not_applicable` and
  `test_pr_opened_before_the_effective_time_without_a_declaration_is_not_applicable`) and renamed them
  to assert failure. Inverted the production-boundary test the same way.
- Added `test_declared_no_with_na_references_passes` and `test_declared_yes_with_a_real_path_passes`.
- Ran `python -m unittest discover -s tests/session_evidence -p "test_*.py"`: `Ran 100 tests`, `OK`.

# Unavailable / not recorded

The session transcript was not captured to a file while it ran, so the prompt above is a reconstruction
of the instruction rather than a live capture. No platform-internal payload is retained.
