# AID-2026-292 — Evidence

## 1. Scope

This evidence record covers only the in-suite regression self-check
T129 in:

`scripts/test_check_document_management.py`

Objective:

Prove that symlink-unavailable skips do not erase independent test
cases executed by the same runner functions.

The eight symlink-dependent call sites and their shared helper belong
to AID-2026-324 and are outside this work item's implementation scope.

## 2. Implementation evidence

Implementation branch:

`fix/2026-11-27-aid-292-in-suite-skip-selfcheck`

Reported fork point:

`origin/main` at `561e9f24`

Changed file:

`scripts/test_check_document_management.py`

The implementation contains two edits:

1. Add `run_symlink_unavailable_self_check()`.
2. Register `run_symlink_unavailable_self_check` in the existing
   `main()` runners tuple.

The self-check:

- Patches `Path.symlink_to` to raise `OSError(1314)`.
- Exercises `run_symlink_boundary()`.
- Exercises `run_scan_boundary()`.
- Exercises `run_unified_scan()`.
- Exercises `run_unbound_emissions()`.
- Checks the exact expected twelve-name SKIPPED slice.
- Checks that those twelve names do not appear in the newly recorded
  RESULTS_BY_NAME entries.
- Checks that no unexpected skip was introduced.
- Checks that independent cases T43, T44, T45, T46, T47, T52,
  and T61 each recorded True.
- Restores RESULTS, SKIPPED, UNEXPECTED_SKIPS, and RESULTS_BY_NAME
  before recording T129 itself.

## 3. Acceptance evidence

| ID | Acceptance requirement | Reported evidence | Status |
|---|---|---|---|
| A1 | Add an in-suite regression self-check | T129 implemented in the existing test runner | MEASURED |
| A2 | Exercise the symlink-unavailable condition | Path.symlink_to patched to raise OSError(1314) | MEASURED |
| A3 | Verify all twelve expected skips | Exact expected-name comparison against the new SKIPPED slice | MEASURED |
| A4 | Ensure skipped names are not recorded as passed | RESULTS_BY_NAME checked for absence of all twelve names | MEASURED |
| A5 | Ensure independent cases survive | T43/T44/T45/T46/T47/T52/T61 each recorded True | MEASURED |
| A6 | Detect unexpected skip behavior | UNEXPECTED_SKIPS checked for emptiness | MEASURED |
| A7 | Preserve result-accounting state | Existing accounting collections restored before T129 records itself | MEASURED |
| A8 | Register the self-check in the suite | T129 added to the main() runners tuple | MEASURED |
| A9 | Ensure regression sensitivity | Erasure mutation executed: `run_scan_boundary()` made to return immediately after the T49 skip; T129 was the single failing case (exit 1, 358 results, 10 skips) | MEASURED |
| A11 | Ensure an unregistered skip still fails the run | T49 popped from `ALLOWED_SKIPS` under forced failure: exit 1, `FAIL: 1 unregistered skip(s): T49 ...`, T129 False | MEASURED |
| A10 | Keep implementation scope limited | T129 is the only added case | REPORTED; REVIEW PENDING |

## 4. Reported measurements

Tested source state: `scripts/test_check_document_management.py`
SHA-256 `0d64f7114447020dc354623884d659e2888403aa52c4ee0aefd82350d49a9879`,
234166 bytes, measured 2026-11-28 by the coordinating operator.

Environment:

- Native Windows
- Python 3.12
- Implementation branch:
  `fix/2026-11-27-aid-292-in-suite-skip-selfcheck`

### Normal execution

Command:

`python scripts/test_check_document_management.py`

Reported outcome:

- 377/377 passed
- 1 skipped
- T68c was the skipped case
- Exit code 0

### Forced symlink-unavailable execution

Execution condition:

`Path.symlink_to` globally forced to raise `OSError(1314)`.

Reported outcome:

- Exit code 0
- 365/365 passed
- 13 skipped
- 13 registered of 13 allowed
- UNEXPECTED_SKIPS empty
- DOUBLE_RECORD empty
- T129 True

### Mutation sensitivity

Mutation executed: `run_scan_boundary()` was made to return immediately after
the T49 skip, so the skip aborts its enclosing function — the defect class this
case exists to catch.

Observed outcome:

- Exit code 1
- 363 results, 362 passed, 1 failed
- 10 skips (T50, T51 and T51b never ran)
- The single failing case was
  `T129 symlink-unavailable cases skip without erasing independent cases`

The source was restored from a byte backup afterwards and its SHA-256 verified
identical to the tested value above.

## 5. Measurement boundary

All numerical results are measurements of a particular tested source
state.

The results must be associated with the SHA-256 of the exact tested
`scripts/test_check_document_management.py` file.

The implementation branch's reported measurements do not automatically
apply to a rebased branch, a modified file, or a later commit.

After any rebase or modification:

1. Recompute the tested file SHA-256.
2. Repeat the normal execution.
3. Repeat the forced global OSError(1314) execution.
4. Execute the mutation sensitivity check.
5. Verify that T129 remains the only added test case.
6. Record the new outputs against the new file SHA-256.

## 6. Explicit non-claims

This evidence does not claim:

- That the standalone `verify_full_suite_symlink_unavailable.py`
  has been wired into CI.
- That any CI workflow was changed.
- That branch protection or required status contexts were changed.
- That AID-2026-324's helper or eight call sites were implemented
  by AID-2026-292.
- That a PR has been merged.
- That an independent reviewer has approved the implementation.
- That Owner acceptance has been recorded.
- That the reported measurements remain valid after rebase.
