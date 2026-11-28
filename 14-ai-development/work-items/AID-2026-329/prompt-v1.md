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
      last_verification_note: "Prompt snapshot recorded for traceability; its digest and Git blob and commit pins must be measured from the committed file and populated in the work-item manifest before trace validation."
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
    canonical_scope: "Versioned implementation prompt snapshot for AID-2026-329, defining the document-management test count contract with an expected aggregate of 372."
    canonical_scope_id: "ai-development/aid-2026-324-document-management-count-contract-prompt"
    canonical_scope_keywords:
      - "AID-2026-329"
      - "implementation prompt"
      - "document-management count contract"
      - "372 aggregate"
      - "prompt traceability"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-329 — Implementation Prompt v1

## Objective

Implement the #1268 document-management test count contract in:

`scripts/test_check_document_management.py`

The expected aggregate is exactly 377, defined as:

`executed cases + registered skipped cases = 377`

This value is based on the current main-branch baseline of 376 executed
cases plus 1 registered skipped case.

This work item covers count accounting only. The additional symlink-unavailability regression case and its forced `OSError(1314, ...)` end-to-end path belong to Issue #1438 and must not be implemented here.

## Base

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`
- Base commit: `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`

## Required edits

Make exactly these three edits.

### 1. Add the aggregate constant

Immediately after `ALLOWED_SKIPS`, add:

```python
# Current document-management count contract: executed cases plus registered skips.
# The additional symlink-unavailable regression case belongs to #1438.
EXPECTED_AGGREGATE = 377
```

### 2. Integrate the count contract into the existing finalization block in main()

The current `main()` executes its sections through a `runners` tuple, invokes
each runner under an individual `try/except`, and already includes the
`run_steward_baseline_ratchet` runner. Preserve that structure. Do not revert,
replace, or reorder the runner orchestration; integrate the count contract
into the existing finalization block only, starting at
`passed, executed = sum(RESULTS), len(RESULTS)`, and replace the rest of that
block with:

```python
    passed, executed = sum(RESULTS), len(RESULTS)
    skipped = len(SKIPPED)
    total = executed + skipped
    print(f"{passed}/{executed};{skipped} skipped")
    # The aggregate counts executed cases and registered skips. A skip is
    # still not a pass: `passed` and `executed` describe executed cases only.
    # The #1438 symlink-unavailability regression case is not part of this
    # baseline; #1438 must raise the aggregate from 377 to 378 when it adds
    # that case.
    if executed == 0:
        print("FAIL: no cases executed")
        return 1
    if UNEXPECTED_SKIPS:
        print(f"FAIL: {len(UNEXPECTED_SKIPS)} unregistered skip(s): "
              + "; ".join(UNEXPECTED_SKIPS))
        return 1
    if total != EXPECTED_AGGREGATE:
        print(f"FAIL: expected {EXPECTED_AGGREGATE} executed and skipped "
              f"cases, got {total} ({executed} executed, {skipped} skipped)")
        return 1
    return 0 if passed == executed else 1
```

### 3. Preserve the existing recording boundary

Do not modify:

- `record()`
- `skip()`
- `ALLOWED_SKIPS`

Do not add or remove any allowed skip.

## Required verification

Run the suite on the Windows host:

```powershell
$env:PYTHONUTF8 = "1"
python scripts/test_check_document_management.py
$LASTEXITCODE
```

Expected current-host result:

- Exit code 0
- 376 executed cases
- 376 passed executed cases
- 1 registered skipped case
- Aggregate 377
- Summary: `376/376;1 skipped`

Run the aggregate-mismatch negative test against a temporary copy only:

1. Copy the test file to a temporary location.
2. Change `EXPECTED_AGGREGATE = 377` to `EXPECTED_AGGREGATE = 376` in that copy only.
3. Run the copy from the repository root.

Expected result:

- Exit code 1
- Output includes:
  `FAIL: expected 376 executed and skipped cases, got 377 (376 executed, 1 skipped)`

Run the zero-execution negative test against a separate temporary copy only:

1. Copy the test file to a temporary location.
2. Immediately before the finalization statement computing `passed` and `executed`, insert:

   ```python
       RESULTS.clear()
       SKIPPED.clear()
       UNEXPECTED_SKIPS.clear()
   ```

3. Run the copy from the repository root.

Expected result:

- Exit code 1
- Output includes:
  `FAIL: no cases executed`

Do not represent expected negative-test output as measured output. Record the actual output and exit code after running each test.

## Scope boundary

- Do not modify production validators.
- Do not modify workflow definitions.
- Do not modify branch protection.
- Do not implement the symlink-unavailability regression assigned to #1438.
- Do not modify the forced `OSError(1314, ...)` end-to-end path assigned to #1438.
- Do not add dependencies.

## Completion evidence

Record:

- the actual suite output and exit code;
- both negative-test outputs and exit codes;
- `git diff --check`;
- the final changed-file list;
- the final commit SHA and working-tree status.

Do not claim independent review or Owner acceptance until separately recorded.
