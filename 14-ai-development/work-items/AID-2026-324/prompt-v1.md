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
        - "14-ai-development/work-items/AID-2026-324/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Prompt snapshot recorded for traceability; this metadata does not assert approval or independent verification."
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
    canonical_scope: "Implementation prompt snapshot for AID-2026-324 symlink skip fail-closed corrections."
    canonical_scope_id: "ai-development/aid-2026-324-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-324"
      - "prompt snapshot"
      - "symlink skip"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-324 — Prompt Snapshot

## Task

Implement Issue #1439 in `oahcom/AiMemoryBrainArchitecture`, on branch
`fix/2026-11-27-symlink-skip-fail-closed`, based on
`cd1722e753a429247d91f990caa2defac565e308`.

Make symlink skip eligibility fail-closed in
`scripts/test_check_document_management.py`; strengthen
`verify_skip_registry.py` and `verify_symlink_unavailable.py`.

## Required findings

- **F1:** Replace blanket `OSError` skip handling with an explicit error
  classifier. On Windows, inspect `winerror` first and treat it as
  authoritative when present; do not fall back to errno. Permit only
  recognized capability/policy errors. Propagate all other errors,
  including ENOSPC, EIO, EEXIST, ENOENT and Windows sharing violation 32.
- **F2:** Compare skip reasons exactly; do not strip or normalize whitespace.
- **F3:** Negative subprocess harnesses must assert the expected
  `UNEXPECTED_SKIPS` diagnostic and then assert `main() == 1`.
- **F5:** Forced-unavailability verification must require each expected
  name exactly once in `SKIPPED`, and absent from `RESULTS_BY_NAME`.
- **Harness exit:** `verify_skip_registry.py` must itself return nonzero
  when any negative harness fails.

## Error classification

Use `NotImplementedError` as an unavailable capability result.
For Windows exceptions with `winerror`, permit only:
- 5 (`ERROR_ACCESS_DENIED`);
- 50 (`ERROR_NOT_SUPPORTED`);
- 1314 (`ERROR_PRIVILEGE_NOT_HELD`).

For non-Windows or exceptions without Windows `winerror`, permit only
`EPERM`, `EACCES`, `ENOTSUP`, and `EOPNOTSUPP` where defined.
Windows `winerror` takes precedence over errno because CPython's mapping
is lossy. In particular, winerror 32 maps to EACCES but is a sharing
violation, not a capability limitation. Do not include ambiguous
`ERROR_INVALID_FUNCTION` 1 in the Windows allowlist.

## Scope and exclusions

Do not modify `scripts/check_document_management.py`.
Do not reopen or alter the already-merged Issue #1268 invariant.
Do not claim F4 cross-invocation duplicate accounting is fixed.
Do not add third-party dependencies or unrelated refactoring.
Preserve existing skip names, exact registered reason, T68c behavior,
and successful symlink-capable test behavior.

## Required evidence

Provide before/after executable evidence for F1, F2, F3, F5 and the
skip-registry harness's own exit behavior. Before evidence is the
operator-provided red output. After evidence must be captured by the
operator and must not be fabricated or represented as implementation-
session execution.

The normal symlink-capable suite is expected to remain 371/371 passed
with the existing one T68c skip, unless the operator measures a
different count after applying the patch.

## Follow-up: Issue #1438

Integrate Issue #1438 into the same AID-2026-324 work item and PR carrier.

In `scripts/test_check_document_management.py`:

- Add the narrowly scoped positional errno value 1314 to the fallback
  symlink-unavailable errno allowlist. A present Windows `winerror`
  remains authoritative; Windows `winerror=32` must remain rejected.
- Apply the same symlink-unavailable classifier and exact registered skip
  reason to T49, T50, T51, T51b, T58, T59, T60 and T128.
- Register those eight case names in `ALLOWED_SKIPS` with the exact reason
  `symlink creation unavailable on this platform`.
- Give every runner called by `main()` a section-level exception boundary.
  On an exception, print `[FAIL] <runner> raised <Type>: <msg>`, record one
  failed result for that section, continue with later runners, print the
  final passed/total summary, and return a nonzero exit status.

Add `verify_full_suite_symlink_unavailable.py` at the repository root.
It must launch the full self-check in a child process while forcing both
`os.symlink` and `pathlib.Path.symlink_to` to raise `OSError(1314, ...)`.
It must verify the expected final summary, exact skip accounting and
successful process exit when all runnable assertions pass.

Expected injected-unavailability accounting is 359/359 passed and
13 skips: the twelve symlink-dependent cases (T36, T37, T41, T42,
T49, T50, T51, T51b, T58, T59, T60 and T128) plus T68c.
The expected skip summary is 13 skipped, 13 registered of 13 allowed.

Coverage limitation: a skipped T49/T50/T51/T51b/T58/T59/T60/T128 case
does not prove its original symlink-specific assertion. The forced-
unavailability regression proves skip accounting and suite completion,
not the skipped symlink behavior. Those assertions remain exercised on
symlink-capable environments.

Keep the Issue #1439 requirements and exclusions unchanged: do not modify
the production checker, do not reopen Issue #1268, do not claim F4 is fixed,
and do not add third-party dependencies or unrelated refactoring.
