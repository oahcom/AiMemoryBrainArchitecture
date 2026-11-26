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
      last_verification_note: "Every count and SHA in this prompt was measured in the session that executed it: the rebase onto main 1f5ba824, the 318/318 suite result, and the T92a counterfactual at 317/318. None is copied from the pull request body."
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

# AID-2026-079 — Pin the gate's own error paths with controlled fault injection

## The assignment

This work item carries one change: `scripts/test_check_document_management.py` gains
`run_fault_injection()`, called from `main()` after `run_single_entry_callers()`, holding
four cases T92a–T92d. Each patches exactly one seam for one call, delegates every other
input to the real implementation, restores the attribute in a `finally`, and asserts that
the inputs it did not target still reached the real code. A patch that swallowed every
call would produce the same diagnostic while proving nothing, and those positive
assertions exist to make that failure visible.

The assignment, as executed, was:

1. Rebase `test/T92-fault-injection` (head `ade0e2d8`, authored against `29eea143`) onto
   `main` at `1f5ba824`, resolving the one-file conflict produced by `575cf3f4`
   ("Restore the seven guards removed by #1070, with direct-call tests"), which rewrote
   the same test file after `29eea143`. Both sides were kept: main's `run_restored_guards()`
   and this branch's `run_fault_injection()`.
2. Register this work item, because the pull request had none.
3. Correct a false premise in the pull request description. An earlier revision argued that
   a Work Item ID could not be supplied because no failure was fabricated. That argument is
   wrong: `Work Item ID: NONE` is accepted by the validator only alongside
   `AI-assisted work: NO`, and this pull request is AI-assisted. `AID-2026-079` is
   registered here.
4. Declare the four body fields and the per-issue table, with Issue #827 declared
   `LEGACY_UNDECLARED` and `N/A`, because #827 predates `2026-12-01T00:00:00Z` and carries
   no declaration of its own.

The tests were not rewritten. The rebase resolved a textual conflict; it did not change a
single assertion, and the counterfactual below was re-run on the rebased tree to show they
still bite.

## What the four cases pin

- **T92a** — `git()` cannot start the process at all. The caller must refuse with its own
  diagnostic (`ERROR: incremental changed-path selection failed: …`) rather than let the
  `OSError` escape as a traceback. The case also asserts that `git log` still reaches the
  real implementation while the seam is patched.
- **T92b** — one governed path cannot be resolved while the target set is built. It must
  leave a `DM-01` problem and stay out of the target list; either assertion alone is
  satisfiable by a wrong implementation.
- **T92c** — a governed document cannot be read while the verdict is being decided. The
  failure must be reported against the path, not raised.
- **T92d** — `Path.is_file` fails for one governed path during collection. The walk must
  survive it, `collect_governed()` must be unchanged by the injection, every other path must
  still reach the real `Path.is_file`, and the attribute must be restored afterwards.

## Measurement, this session

At the rebased head, `python3 scripts/test_check_document_management.py` prints
**318/318 passed** with **1 skipped** (`T68c a real 0o000 directory is reported by path
(integration)`, registered). The count is higher than the pre-rebase 295 because `575cf3f4`
added `run_restored_guards()` — T93a–T93h — to the same file.

Neutralising T92a's seam (the `except OSError: return None` in `git()` changed so the error
escapes) turns the suite into **317/318 passed** with exactly one failure:

```
  [FAIL] T92a git() spawn failure is refused by the caller, not raised  exit 2, matching lines [], output "::error::Unable to determine Git history completeness: [Errno 2] No such file or directory: 'git'\n"
```

The suite is green with the case and red without the guard. That is the property this work
item exists to hold, and re-running it after the rebase is what makes the rebase part of the
evidence rather than a step taken on trust.

## What this does not authorise

- No production behaviour change: `scripts/check_document_management.py` is not modified by
  this branch.
- No schema change, no required status context, no workflow step, no protection payload.
- No claim that any of these four failures happens naturally in CI. The cases are
  controlled injections and the docstring says so; that sentence is the boundary of what
  they prove.
- No claim of independent review or of an acceptance decision. Both are `NOT_ASSIGNED`.
