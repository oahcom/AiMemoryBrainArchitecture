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
        - "14-ai-development/work-items/AID-2026-329/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Operator-executed test outputs for the 372-case document-management count contract are recorded below; this evidence document and its metadata have not been independently validated by the implementation session."
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
    canonical_scope: "Execution evidence and verification status for AID-2026-329 document-management test count contract, including the expected aggregate of 372 executed and registered-skipped cases."
    canonical_scope_id: "ai-development/aid-2026-324-document-management-count-contract-evidence"
    canonical_scope_keywords:
      - "AID-2026-329"
      - "document-management count contract"
      - "372 aggregate"
      - "execution evidence"
      - "registered skips"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Evidence — AID-2026-329

## 1. Scope and baseline

This work item implements the count contract assigned to Issue #1268.

The current-main baseline was measured on the Windows host after the branch
was cleanly rebased onto `origin/main` at
`31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`, using:

```powershell
$env:PYTHONUTF8 = "1"
python scripts/test_check_document_management.py
$LASTEXITCODE
```

Measured result on the rebased main baseline:

- Exit code: `0`
- Executed cases: `376`
- Passed executed cases: `376`
- Registered skipped cases: `1`
- Aggregate: `377`

The final two output lines were:

```text
376/376 passed
1 skipped, 1 registered of 13 allowed: T68c a real 0o000 directory is reported by path (integration)
```

There were 376 `[ok  ]` result lines.

The single registered skip is the T68c integration case. It is not an
executed pass and must not be added to the passed count. The aggregate is
the sum of executed and skipped cases: `376 + 1 = 377`.

The baseline repository head for this measurement was:

`31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`

The earlier `371` executed, `371/371 passed`, and `372` aggregate figures
were measured before the rebase. They are pre-rebase historical values and
are superseded by the current-main measurement above.

The target test file is:

`scripts/test_check_document_management.py`

At the inspected baseline, the file contained 5256 lines. `ALLOWED_SKIPS`
was at lines 50–61, `main()` began at line 5191, and its final summary
and return block was at lines 5233–5252.

## Rebase and re-measurement

The implementation branch was cleanly rebased onto `origin/main` at
`31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`. The post-rebase `main()` structure
differs from the pre-rebase structure: runner execution is organized through
a `runners` tuple, each runner is invoked under an individual `try/except`,
and the `run_steward_baseline_ratchet` runner has been added. The count
contract was therefore integrated into the rebased structure without
replacing or reverting the runner orchestration. Its change is limited to
the finalization block beginning at `passed, executed = sum(RESULTS), len(RESULTS)`.

The re-measured current-main baseline is `376` executed cases plus `1`
registered skipped case, for an aggregate of `377`. Accordingly,
`EXPECTED_AGGREGATE = 377` is defined after `ALLOWED_SKIPS`, so the expected
total reflects the current registered skip allowance and the measured
current-main count. The registered T68c skip remains excluded from the
executed-pass count.

The post-change positive run on the same Windows host reported
`376/376;1 skipped` and exited `0`. Two negative cases were also measured:
setting `EXPECTED_AGGREGATE = 376` caused the aggregate-mismatch guard to
exit `1` with
`FAIL: expected 376 executed and skipped cases, got 377 (376 executed, 1 skipped)`;
clearing the result ledger caused the no-execution guard to exit `1` with
`FAIL: no cases executed`.

The pre-rebase baseline (`371` executed, `1` skipped, aggregate `372`) is
retained only as historical context. It is not the baseline for the rebased
branch or the current count contract.

## 2. Implementation contract

The implementation consists of three bounded edits in
`scripts/test_check_document_management.py`.

### 2.1 Add the expected aggregate

Immediately after `ALLOWED_SKIPS`, add:

```python
# Current #1268 count contract: executed cases plus registered skips.
# The additional symlink-unavailable regression case belongs to #1438.
EXPECTED_AGGREGATE = 377
```

This makes the #1268 aggregate an explicit assertion rather than an
informal expectation.

### 2.2 Replace the final summary and guards in main()

The finalization block computes:

- `passed`: the number of successful executed cases;
- `executed`: the number of recorded executed cases;
- `skipped`: the number of registered skip records;
- `total`: `executed + skipped`.

The summary format is:

```text
{passed}/{executed};{skipped} skipped
```

The count contract intentionally distinguishes the two concepts:

- `passed` counts only successful executions;
- `executed` counts all executed cases, including failures;
- `skipped` counts cases that could not execute and were registered as skips;
- `total` counts executed cases plus registered skips.

A skip is part of the aggregate inventory, but it is not a pass. Therefore
the aggregate check uses `total`, while the final executed-case success
check uses `passed == executed`.

The guards run in this order:

1. `executed == 0`: fail if no case actually ran;
2. `UNEXPECTED_SKIPS`: fail if any skip is not registered with its allowed
   reason;
3. Fail if executed plus registered skipped cases differs from `377`.
4. `passed == executed`: succeed only if every executed case passed.

### 2.3 Preserve the recording and skip boundary

`record()` is not changed.

`skip()` is not changed.

`ALLOWED_SKIPS` is not changed.

This work item does not broaden the set of cases allowed to skip and does
not change the reason registered for any existing skip.

## 3. Negative-test procedures and expected results

The following tests must be run against temporary copies of the test file.
They must not alter the committed source file.

### 3.1 Aggregate mismatch

Construct a temporary copy of
`scripts/test_check_document_management.py`.

In that copy only, change:

```python
EXPECTED_AGGREGATE = 377
```

to:

```python
EXPECTED_AGGREGATE = 376
```

Run the temporary copy from the repository root using the same Python
interpreter and environment as the baseline.

Expected result:

- Set `EXPECTED_AGGREGATE` to `377`.
- Actual counts on the rebased current-main baseline: `376` executed and
  `1` registered skipped.
- Aggregate: `377`.
- The expected aggregate check must fail if the executed-plus-skipped total
  differs from `377`.
- With the deliberate negative-test value `EXPECTED_AGGREGATE = 376`, the
  measured output is:
  `FAIL: expected 376 executed and skipped cases, got 377 (376 executed, 1 skipped)`.

### 3.2 Zero executed cases

Construct another temporary copy of
`scripts/test_check_document_management.py`.

Immediately before the finalization statement that computes `passed` and
`executed`, insert:

```python
    RESULTS.clear()
    SKIPPED.clear()
    UNEXPECTED_SKIPS.clear()
```

Run that temporary copy from the repository root using the same Python
interpreter and environment as the baseline.

Expected result:

- Exit code: `1`
- Required failure text:

```text
FAIL: no cases executed
```

This proves the zero-execution guard cannot be bypassed by an empty
execution ledger.

### 3.3 Evidence status

Both negative cases have now been executed on the Windows host. With
`EXPECTED_AGGREGATE = 376`, the count-mismatch case exited `1` and printed
`FAIL: expected 376 executed and skipped cases, got 377 (376 executed, 1 skipped)`.
With the result ledger cleared, the no-execution case exited `1` and printed
`FAIL: no cases executed`. These are measured negative-test results, not
pending measurements.

## 4. Ownership and change boundary

This work item owns only the #1268 count contract.

It does not own, implement, or modify:

- the symlink-unavailability regression test assigned to Issue #1438;
- the forced `OSError(1314, ...)` end-to-end path assigned to Issue #1438;
- production document-management validators;
- workflow definitions;
- branch-protection configuration.

The only product-code/test-suite file changed by this implementation is:

`scripts/test_check_document_management.py`

The workflow caller remains:

`.github/workflows/document-management.yml:34`

The repository-wide search supplied for this work item found no script or
workflow consumer that parses the test suite's standard output. The summary
format change therefore has no identified downstream stdout parser to
update.

## 5. What this record does not claim

This evidence record does not claim:

- that the two negative tests have already been executed;
- that the forced `OSError(1314, ...)` path is fixed by this work item;
- that the #1438 symlink-unavailability regression has been implemented;
- that production validator behavior has changed;
- that workflow or branch-protection configuration has changed;
- that an independent review or Owner acceptance has occurred;
- that the work item or its implementation PR has been merged.

Those claims require separate evidence and, where applicable, separate
ownership under Issue #1438.
