---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured scope snapshot of the user-provided AID-2026-280 work order, not a byte-for-byte chat export."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Task prompt snapshot for AID-2026-280"
    canonical_scope_id: "ai-development/aid-2026-280-prompt"
    canonical_scope_keywords:
      - issue-1268
      - symlink-boundary
      - registered-skips
    canonical_conflict_status: None
    normative_status: Informative
---

# Work Order Snapshot — AID-2026-280

## Objective

Implement Issue #1268 in `oahcom/AiMemoryBrainArchitecture`.

Correct the symlink boundary self-check so that inability to create a symbolic link is represented by the existing bounded `skip()` mechanism, never by `record(..., True)`.

## Baseline

- Target: `scripts/test_check_document_management.py`.
- Baseline blob: `7fe44a8285f22219c8b50fdf06b4a241b45c22d2`.
- Measured `origin/main`: `a588cd99`, subject to recheck.
- Runner: `python3 scripts/test_check_document_management.py`.
- Self-contained `main()` runner, not unittest.
- Historical totals: 371/371 at `bc741bdc` and 368/368 at `4fa75e78`.
- Existing registered skip: T68c, for execution as root.

## Required behaviour

1. The three symlink-creation blocks in `run_symlink_boundary()` must use registered skips when creation raises `OSError` or `NotImplementedError`.
2. The directory-link prerequisite covers both T36 and T37; both cases must be skipped if that shared prerequisite cannot be created.
3. T41 and T42 must be independently skipped when their respective links cannot be created.
4. No early return may erase T43-T47.
5. Other symlink creation that can abort the complete suite, particularly `run_scan_boundary():3022`, must be guarded.
6. A platform without symlink support must reach the normal summary and exit with honest skip accounting.
7. A symlink-capable platform must retain its existing nine-case execution and must not acquire a new skip.
8. Every new skip must have an exact name and reason in `ALLOWED_SKIPS`.
9. An unregistered skip or a mismatched reason must remain fatal.

## Required self-check

Add a self-check in the same test file, using the existing T-number convention, that:

- Patches symlink creation to raise.
- Runs `run_symlink_boundary()`.
- Asserts the exact skipped case names.
- Asserts T43-T47 execute.
- Asserts the five independent cases contribute actual results.
- Asserts skipped cases contribute neither a pass nor a denominator entry.
- Restores all global result and skip state before recording its own result.
- Is registered in `main()`.

## Issue-text corrections to preserve

- The drop is eight records, not two: nine expected cases are downstream of the three early returns, while only one is recorded.
- The whole suite does not stay green when symlink creation is forced to fail. It crashes at `run_scan_boundary():3022` after 201 records, with no summary. The isolated function is where the false-pass claim applies.
- T42 at line 2926 and T68c at line 3648 are 722 lines apart.

## Scope restrictions

- Do not modify `scripts/check_document_management.py`.
- Do not change gate decision logic.
- Do not add, rename or remove CI jobs.
- Do not modify branch protection or the sixteen required contexts.
- Use Python 3.12-compatible standard-library functionality only.
- Do not modify existing work-item directories or INDEX entries.
- Do not claim tests, CI, merge, review or acceptance without measurement.

## Deliverables

1. Unified diff with three lines of context for the changed test-file regions.
2. AID-2026-280 manifest.
3. Evidence record with all eight acceptance measurements.
4. This prompt snapshot.
5. Session evidence with non-empty actual input and output.
6. One appended INDEX row.

## Identifier allocation

Assigned identifier: AID-2026-280.

The coordinating session measured 131 occupied identifiers across remote refs, maximum 279, and confirmed 280 absent from main INDEX and open PR bodies. Immediately before PR creation, recheck remote refs and INDEX. If 280 is occupied, use the lowest free number in 281-290 and update all paths and references consistently.

## Attribution and authority

Attribution: user-authorized operator (delegated by account owner).

Date: 2026-11-27.

A delegated proxy record is not a natural-person Owner signature.
