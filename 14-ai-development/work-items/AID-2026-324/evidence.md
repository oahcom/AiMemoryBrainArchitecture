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
      last_verification_note: "Before evidence is operator-supplied; after evidence placeholders are intentionally pending execution."
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
    canonical_scope: "Execution evidence skeleton for AID-2026-324 fail-closed symlink skip corrections."
    canonical_scope_id: "ai-development/aid-2026-324-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-324"
      - "execution evidence"
      - "fail-closed symlink skip"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-324 — Evidence

## 1. Scope and evidence status

This record covers F1, F2, F3, F5 and the additional harness-process-exit
finding described in Issue #1439, together with the symlink-unavailable
handling, runner exception isolation and full-suite forced-unavailability
regression for Issue #1438. It does not claim F4 is fixed.

All "before" output below was supplied verbatim by the operator. The
Issue #1439 "after" output below was supplied verbatim by the operator.
Issue #1438 after-output remains an explicit placeholder until the operator
executes the patched tree and supplies the resulting output.

## 2. F1 — OSError classification

### Before (operator-supplied, verbatim)

```text
SKIPPED: ['T36 directory symlink is rejected as a governed root', 'T37 governed_files does not descend into a symlinked root', 'T41 symlinked governed file is rejected', 'T42 governed file reached through a symlinked parent is rejected']
SKIPPED_COUNT_PER_NAME: {'T36 directory symlink is rejected as a governed root': 1, 'T37 governed_files does not descend into a symlinked root': 1, 'T41 symlinked governed file is rejected': 1, 'T42 governed file reached through a symlinked parent is rejected': 1}
UNEXPECTED_SKIPS: []
F1_VERDICT: FAIL_OPEN (ENOSPC swallowed as skip)
376/376 passed
MAIN_EXIT: 0
```

### After (operator execution pending)

```text
SKIPPED: []
CAUGHT: OSError(28, 'No space left on device')
F1_ENOSPC_PROPAGATED: True
F1_VERDICT: PASS
WINERROR_ALLOWLIST: PASS
WINERROR_SHARING_VIOLATION: REJECTED
WINERROR_AMBIGUOUS_CODES: REJECTED
```

## 3. F2 — exact skip-reason equality

### Before (operator-supplied, verbatim)

```text
  [skip] T36 directory symlink is rejected as a governed root  ( symlink creation unavailable on this platform	)
INJECTED_REASON: '\xa0symlink creation unavailable on this platform\t'
REGISTERED: 'symlink creation unavailable on this platform'
UNEXPECTED_SKIPS_DELTA: []
F2_VERDICT: FAIL_OPEN (whitespace drift admitted)
```

### After (operator execution pending)

```text
  [skip] T36 directory symlink is rejected as a governed root  ( symlink creation unavailable on this platform	)
INJECTED_REASON: '\xa0symlink creation unavailable on this platform\t'
REGISTERED: 'symlink creation unavailable on this platform'
UNEXPECTED_SKIPS_DELTA: ["T36 directory symlink is rejected as a governed root: skip reason '\\xa0symlink creation unavailable on this platform\\t' is not the registered one"]
F2_VERDICT: PASS
```

## 4. F3 — diagnostic-specific negative harness

### Before (operator-supplied, verbatim)

```text
HARNESS_EXIT: 0
TAIL: ['UNEXPECTED_SKIPS: []', 'MAIN_EXIT: 1']
F3_VERDICT: FAIL_OPEN (unrelated exit 1 reported as PASS)
```

### After (operator execution pending)

```text
unregistered-name -> PASS ['EXPECTED_DIAGNOSTIC: present', 'MAIN_EXIT: 1']
wrong-reason -> PASS ['EXPECTED_DIAGNOSTIC: present', 'MAIN_EXIT: 1']
whitespace-reason -> PASS ['EXPECTED_DIAGNOSTIC: present', 'MAIN_EXIT: 1']
EXIT=0
```

## 5. F5 — exact-once forced-unavailability assertion

### Before (operator-supplied, verbatim)

```text
SKIPPED_COUNT_PER_NAME: {'T36 directory symlink is rejected as a governed root': 2, 'T37 governed_files does not descend into a symlinked root': 2, 'T41 symlinked governed file is rejected': 2, 'T42 governed file reached through a symlinked parent is rejected': 2}
RESULTS_BY_NAME: {'T43 ...': True, 'T44 ...': True, 'T45 ...': True, 'T46 ...': True, 'T47 ...': True}
CURRENT_VERDICT_PREDICATE: PASS
F5_VERDICT: FAIL_OPEN (duplicates pass the presence-only predicate)
```

### After (operator execution pending)

```text
SKIPPED_COUNT_PER_NAME: {'T36 directory symlink is rejected as a governed root': 1, 'T37 governed_files does not descend into a symlinked root': 1, 'T41 symlinked governed file is rejected': 1, 'T42 governed file reached through a symlinked parent is rejected': 1}
RECORDED_AS_RESULT: []
MISSING_FROM_EVERYTHING: []
DUPLICATE_SKIPS: []
VERDICT: PASS
EXIT=0
```

## 6. Fifth finding — harness process exit

### Before (operator-supplied, verbatim)

```text
unregistered-name -> PASS [...]
wrong-reason -> PASS [...]
EXIT=0
```

### After (operator execution pending)

```text
unregistered-name -> PASS ['EXPECTED_DIAGNOSTIC: present', 'MAIN_EXIT: 1']
wrong-reason -> PASS ['EXPECTED_DIAGNOSTIC: present', 'MAIN_EXIT: 1']
whitespace-reason -> PASS ['EXPECTED_DIAGNOSTIC: present', 'MAIN_EXIT: 1']
EXIT=0
```

## 7. Normal-path verification

### Before (operator-supplied baseline)

```text
371/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
```

### After

```text
371/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
EXIT=0
```

## 8. Non-claims

- F4 cross-invocation duplicate accounting is not claimed as fixed.
- Issue #1268 is not reopened.
- `scripts/check_document_management.py` is unchanged.
- No operator output is represented as execution by the implementation session.
- No PR merge, independent review, or Owner acceptance is claimed.

## 9. Issue #1438 — full-suite symlink-unavailable handling

### Before (operator-supplied, verbatim)

```text
EXIT=1
--- summary lines ---
（空：没有任何 n/n passed 行）
--- tail ---
  [ok  ] T34 schema missing the four dimensions stops the gate
  [ok  ] T35 absent required leaf is an error naming its path
symlink boundary
    sys.exit(main())
             ^^^^^^
  File "D:\code\_lcs\fix-1439\scripts\test_check_document_management.py", line 5259, in main
    run_symlink_boundary()
  File "D:\code\_lcs\fix-1439\scripts\test_check_document_management.py", line 2911, in run_symlink_boundary
    link.symlink_to(Path(outside), target_is_directory=True)
  File "D:\code\_lcs\repro1439\site1438\sitecustomize.py", line 6, in _deny
    raise OSError(1314, "A required privilege is not held by the client")
OSError: [Errno 1314] A required privilege is not held by the client
--- counts ---
200  [ok  ]
0    [FAIL]
0    [skip]
```

### After (operator-supplied, verbatim)

```text
FULL_SUITE_EXIT: 0
FULL_SUITE_SUMMARIES: ['359/359 passed']
FULL_SUITE_SKIP_SUMMARY_COUNT: 1
FULL_SUITE_ALL_12_SYMLINK_SKIPS: True
FULL_SUITE_VERDICT: PASS

```

### Coverage limitation

When symlink creation is unavailable, T49/T50/T51/T51b/T58/T59/T60/T128
are recorded as skips. Those skipped cases do not prove their original
symlink-specific assertions. Their symlink-specific behavior remains
exercised only on environments where the required symlinks can be created.
The full-suite forced-unavailability regression checks skip accounting and
suite completion; it is not a substitute for those symlink-specific tests.
