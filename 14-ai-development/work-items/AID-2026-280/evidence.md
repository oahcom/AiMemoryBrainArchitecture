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
      last_verification_note: "Acceptance measurements are assigned to the coordinating session and must be bound to the final PR head."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Acceptance evidence for AID-2026-280"
    canonical_scope_id: "ai-development/aid-2026-280-evidence"
    canonical_scope_keywords:
      - issue-1268
      - symlink-boundary
      - test-accounting
    canonical_conflict_status: None
    normative_status: Informative
---

# Acceptance Evidence — AID-2026-280

All measurements below must be performed by the coordinating session against the final PR head. No result is claimed by this implementation session.

## Issue-text corrections

1. **Record reduction:** Eight records are lost, not two. Nine cases are expected from the three affected blocks, but early returns leave only the first record.
2. **Whole-suite behaviour:** Forced symlink failure currently causes an uncaught `OSError` at `run_scan_boundary():3022` after 201 records. The suite does not print its summary. The isolated function's false-pass behaviour must not be confused with whole-suite behaviour.
3. **Line distance:** T42 is at line 2926 and T68c at line 3648: 722 lines apart.

## Acceptance measurements

| # | Acceptance evidence | Required measurement |
|---|---|---|
| 1 | Rejection | Patch `Path.symlink_to` to raise `OSError` and `NotImplementedError` in separate runs. Run the full suite. Confirm dependent cases appear in `[skip]` output and do not appear in RESULTS. Confirm the process reaches its summary. |
| 2 | No erasure | In the same forced-failure run, assert `RESULTS_BY_NAME` contains successful executions for T43, T44, T45, T46 and T47. |
| 3 | Honest accounting | Capture `n/n passed` and the registered-skip line. Reconcile the total with the actual RESULTS length. Confirm every skipped case has exactly one registered reason and is excluded from the pass numerator and denominator. |
| 4 | Unregistered skip remains fatal | Invoke `skip()` with an unregistered name and with an incorrect reason for a registered name. Confirm `UNEXPECTED_SKIPS` is populated and `main()` exits non-zero. |
| 5 | No regression | Run `python3 scripts/test_check_document_management.py` on a symlink-capable Linux or Windows host. Compare the executed-case count against the pre-change baseline. No new skip may appear. |
| 6 | Mutation | Remove the new symlink-unavailable handling or restore the former false-pass branch. Repeat the forced-failure self-check. It must fail because the affected cases are recorded as passes or the independent cases disappear. |
| 7 | Exact head | Record the final PR head SHA before running the evidence suite. Attach the exact SHA, command, exit status, stdout/stderr and results to this evidence record. Re-run after any subsequent commit. |
| 8 | Complete suite and scan-boundary resilience | Force symlink creation to raise during the entire suite, including `run_scan_boundary()`. Confirm no unhandled `OSError`, no false-pass result, and a final summary with registered skips. Independently verify each guarded scan-boundary case. |

## Required baseline comparison

The coordinating session must record:

- Baseline commit: `a588cd99` (recheck moving main).
- Baseline target blob: `7fe44a8285f22219c8b50fdf06b4a241b45c22d2`.
- Historical measurements: 371/371 at `bc741bdc`; 368/368 at `4fa75e78`.
- The one pre-existing registered skip: T68c.
- New skip names and exact reasons.
- Total executed results on a symlink-capable host.
- Total executed results and skipped names on a forced-failure host.
- Final PR head SHA.

## Acceptance boundary

No CI, merge, independent review, Owner acceptance, or Issue closure is asserted here. A green test run is evidence of test execution, not acceptance authority.
