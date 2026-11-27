# AID-2026-290 — Evidence

## 1. Issue

- Owning issue: #1268
- Repository: oahcom/AiMemoryBrainArchitecture
- Target file: scripts/test_check_document_management.py
- Scope: T36, T37, T41, T42

## 2. Initial baseline supplied by operator

Normal path, with symlink support:

```text
371/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
```

This establishes that the first patch preserved the normal-path
total on the operator's machine.

It does not establish correctness of the unavailable-symlink path.

## 3. Forced unavailable-path failure — verbatim operator output

```text
  [skip] T42 governed file reached through a symlinked parent is rejected  (symlink creation unavailable on this platform)
  [ok  ] T42 governed file reached through a symlinked parent is rejected
RESULTS: [False, True, True, True, True, True, True, True, True]
RESULTS_BY_NAME: {'T36 directory symlink is rejected as a governed root': False, 'T37 governed_files does not descend into a symlinked root': True, 'T41 symlinked governed file is rejected': True, 'T42 governed file reached through a symlinked parent is rejected': True, 'T43 hidden top-level directory must be accounted for': True, 'T44 .git is structurally exempt from the registry': True, 'T45 backlog count disagreeing with the disk is an error': True, 'T46 backlog count that is not an integer is an error': True, 'T47 backlog documents are actually scanned': True}
SKIPPED: ['T36 directory symlink is rejected as a governed root', 'T37 governed_files does not descend into a symlinked root', 'T41 symlinked governed file is rejected', 'T42 governed file reached through a symlinked parent is rejected']
UNEXPECTED_SKIPS: []
RECORDED_AS_RESULT: ['T36 directory symlink is rejected as a governed root', 'T37 governed_files does not descend into a symlinked root', 'T41 symlinked governed file is rejected', 'T42 governed file reached through a symlinked parent is rejected']
MISSING_FROM_EVERYTHING: []
VERDICT: FAIL
```

## 4. Failure analysis

The four affected cases were simultaneously present in SKIPPED
and RESULTS_BY_NAME.

Root cause: skip() records the skip but does not terminate
Python control flow.

Three structural problems were identified:

1. T36 continued into its original registry assertion and record().
2. T41 broke out of its symlink creation loop but continued into
   its original assertion and record().
3. T42 continued into its original assertion and record().

T37 shares T36's directory symlink prerequisite and must receive
its own independent skip when that prerequisite fails.

## 5. Corrective implementation

Use independent creation-success flags and mutually exclusive
branches:

- directory_symlink_created: T36 and T37
- file_symlinks_created: T41
- parent_symlink_created: T42

Every failed prerequisite takes the skip branch.
The corresponding record branch is reachable only when the
prerequisite succeeded.

The four existing ALLOWED_SKIPS entries and their exact reasons
remain unchanged.

T43-T47 retain their original behavior.

## 6. Required re-verification

Run both commands after applying the corrected function:

```bash
python scripts/test_check_document_management.py
python verify_symlink_unavailable.py
```

The first command must prove the normal symlink-capable path
still executes all four assertions.

The second command must prove all four cases are independently
skipped, with no duplicate records.

## 7. Acceptance criteria

- Exactly four symlink cases in SKIPPED on simulated failure.
- No symlink case in RESULTS_BY_NAME on simulated failure.
- UNEXPECTED_SKIPS is empty.
- No missing symlink case.
- Wrong skip reason is rejected.
- Wrong skip name is rejected.
- Normal path remains 371/371 on the same Windows baseline.
- Existing T68c behavior remains unchanged.

## 8. Execution status

Initial patch:
- Normal-path operator output: 371/371.
- Forced unavailable-path operator output: FAIL.

Corrected function:
- Authored in the implementation session.
- Not executed by the implementation session.
- Both required commands remain pending.

No claim of corrected test success, PR merge or Owner acceptance
is made by this evidence record.
