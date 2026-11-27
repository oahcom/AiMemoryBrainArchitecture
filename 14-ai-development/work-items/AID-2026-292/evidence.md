# AID-2026-292 — Evidence

## Scope and provenance

This work item supplements AID-2026-290 for Issue #1268. AID-2026-290 corrected T36, T37, T41 and T42. This item does not replace or alter those four cases.

The implementation scope is limited to `scripts/test_check_document_management.py` and the four AID-2026-292 work-item records plus the INDEX row. The production checker, CI jobs, branch protection and 16 required contexts are outside scope.

The measurements below were executed by the coordinating operator on this machine (Windows, Python 3.12, symlink-capable) against the tree described by `base_commit_sha` plus this commit's diff. The identity of the tested file is `scripts/test_check_document_management.py` sha256 `d0754aaf23bc07997d36756ddafd7d631a5fcf47aa589b250251d06e894e83bd` (230718 bytes). Measured at 2026-11-27T08:23:59Z.

## Acceptance criteria

| # | Acceptance row | Required evidence |
|---|---|---|
| 1 | T49, T50, T51 and T51b handle unavailable symlink creation honestly. | Each dependent case is recorded exactly once in `SKIPPED`, never in `RESULTS`; the rest of `run_scan_boundary()` continues. |
| 2 | T58, T59 and T60 handle unavailable symlink creation honestly. | Each dependent case is recorded exactly once in `SKIPPED`, never in `RESULTS`; later independent cases continue. |
| 3 | T128 treats unavailable symlink creation as a registered skip. | The exception path calls `skip()` with the exact registered reason; successful creation retains the original `_bind(...)` assertion path unchanged. |
| 4 | All eight new skip names are registered exactly once. | T49, T50, T51, T51b, T58, T59, T60 and T128 are present in `ALLOWED_SKIPS` with reason `symlink creation unavailable on this platform`; T36/T37/T41/T42 are not duplicated. |
| 5 | The unavailable-symlink check is part of the test suite. | T129 is registered in `main()` and simulates symlink creation failure without relying on an external script. |
| 6 | Independent cases still execute under global symlink failure. | T43, T44, T45, T46, T47, T52 and T61 all execute and evaluate True in the forced-failure self-check. |
| 7 | Skip accounting remains fail-closed. | An unregistered T49 skip makes the suite exit 1; a mutation restoring the old T36 false-pass path makes T129 fail. |
| 8 | Symlink-capable platforms retain normal behavior. | Successful symlink paths retain their original assertions; normal platform suite remains 372/372 with only T68c skipped. |

## Measured results

### Normal run (symlink-capable platform)

```text
$ python scripts/test_check_document_management.py
372/372 passed
1 skipped, 1 registered of 13 allowed: T68c a real 0o000 directory is reported by path (integration)
exit 0
```

### Forced failure: every `Path.symlink_to` raises `OSError(1314)`

`Path.symlink_to` is patched for the whole of `main()`, so no case can create a link.

```text
rc=0
RESULTS_LEN=360  PASSED=360  FAILED=0
SKIP_COUNT=13    UNEXPECTED=[]
DOUBLE_RECORD=[]
360/360 passed
13 skipped, 13 registered of 13 allowed: T36 ...; T37 ...; T41 ...; T42 ...; T49 ...; T50 ...; T51 ...; T51b ...; T58 ...; T59 ...; T60 ...; T68c ...; T128 ...
T43=True T44=True T45=True T46=True T47=True T52=True T61=True T129=True
```

`DOUBLE_RECORD` is the intersection of `SKIPPED` with `RESULTS_BY_NAME`: empty means no skipped case was also recorded as a result.

### Unregistered skip negative control

`T49 symlinked backlog root is named in the diagnostic` popped from `ALLOWED_SKIPS`, same global forced failure.

```text
rc=1
RESULTS_LEN=360  PASSED=359
SKIP_COUNT=13    UNEXPECTED=['T49 symlinked backlog root is named in the diagnostic (symlink creation unavailable on this platform)']
T49_IN_SKIPPED=True  T49_IN_RESULTS=False
FAIL: 1 unregistered skip(s): T49 symlinked backlog root is named in the diagnostic (symlink creation unavailable on this platform)
```

### Mutation: T49's `skip(...)` replaced by `record(..., True)`

This is the false-pass shape AID-2026-290 removed. Under the same global forced failure:

```text
rc=1
RESULTS_LEN=361  PASSED=360
T129 symlink-unavailable cases skip without erasing independent cases = False
```

The mutation was reverted from a byte backup; the file sha256 returned to `d0754aaf...83bd` (`RESTORE_MATCHES_ORIGINAL=True`).

### Two defects found by operator execution and fixed before this commit

The first delivery failed measurement, so none of the numbers above applied to it:

1. `run_scan_boundary()` contained `skip = gate.governed_prefixes()`, which shadowed the module-level `skip()` for the whole function body. The four new calls in that function raised `UnboundLocalError: cannot access local variable 'skip'` the moment a link could not be created — the run aborted at T49 with 205 results and 4 skips. Fixed by renaming the local to `prefixes`.
2. The T129 independent-case list named T61 as `T61 DM-08 names the path it was given, not a same-named key elsewhere`, a string no case records; the recorded name is `T61 a same-named key elsewhere is not reported as the forbidden path`. Fixed.

Both defects are invisible on a platform where symlinks can be created, because those `except` branches never run. That is why the forced-failure run, not the normal run, is the acceptance evidence for this work item.

## Measurement boundary

Totals: 372 cases on a symlink-capable platform, 360 under forced global failure. The 12-case difference is the twelve symlink-dependent cases, which skip in the forced run; T129 itself records in both runs.

These measurements were taken on the tree identified by the file sha256 above, not on a later rebase. After rebasing onto `main`, rerun the normal suite, the forced-failure suite, the unregistered-skip negative control and the mutation, and record the new file sha256 with the results. Do not carry these numbers forward as post-rebase evidence.

No CI result, merge, independent review, Owner acceptance or Issue closure is asserted here.
