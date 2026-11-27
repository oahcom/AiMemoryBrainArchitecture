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
        - "14-ai-development/work-items/AID-2026-290/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Operator-executed test outputs are recorded below; this evidence document and its metadata have not been independently validated by the implementation session."
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
    canonical_scope: "Execution evidence and verification status for AID-2026-290 symlink-boundary test skip accounting."
    canonical_scope_id: "ai-development/aid-2026-290-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-290"
      - "execution evidence"
      - "symlink skip accounting"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-290 — Evidence

## 1. Scope

This evidence record covers the symlink-unavailable accounting correction for T36, T37, T41, and T42 in `scripts/test_check_document_management.py`.

The required unavailable-platform skip reason is exactly:

`symlink creation unavailable on this platform`

The four cases must be accounted for as skips only when symlink creation is unavailable. They must not also be entered into `RESULTS_BY_NAME`. The existing T68c behavior and total test count on a symlink-capable platform must remain unchanged.

## 2. Initial forced-unavailability failure

The following output was supplied by the operator as the initial failure evidence. It is retained as the baseline failure record:

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

The reported failure showed that skip registration did not stop subsequent result recording:
- T36 continued into its original registry assertion and was recorded as `False`.
- T37 was registered as skipped but also remained in result accounting.
- T41 continued after the symlink-creation loop stopped and was recorded as a result.
- T42 was registered as skipped but continued to its original `record()` call.

## 3. Corrected implementation behavior

The correction uses explicit setup-success flags and mutually exclusive skip/result branches.

For T36 and T37, the directory-symlink prerequisite is shared, but each test case is independently skipped when that prerequisite cannot be created.

For T41, failure to create the governed-file symlink setup prevents the assertion and result recording.

For T42, failure to create the symlinked parent prevents the assertion and result recording.

No production checker behavior is changed.

## 4. Operator-executed forced-unavailability verification

The following output was supplied by the operator. The operator forced `Path.symlink_to` to raise `OSError` using `mock.patch.object(Path, "symlink_to", side_effect=OSError(...))` and invoked `run_symlink_boundary()`.

**This is operator-executed evidence, not a test run performed by the implementation session.**

```text
RESULTS: [True, True, True, True, True]
RESULTS_BY_NAME: {'T43 hidden top-level directory must be accounted for': True, 'T44 .git is structurally exempt from the registry': True, 'T45 backlog count disagreeing with the disk is an error': True, 'T46 backlog count that is not an integer is an error': True, 'T47 backlog documents are actually scanned': True}
SKIPPED: ['T36 directory symlink is rejected as a governed root', 'T37 governed_files does not descend into a symlinked root', 'T41 symlinked governed file is rejected', 'T42 governed file reached through a symlinked parent is rejected']
UNEXPECTED_SKIPS: []
RECORDED_AS_RESULT: []
MISSING_FROM_EVERYTHING: []
VERDICT: PASS
```

Observed accounting:
- All four affected cases occur in `SKIPPED`.
- None of the four affected cases occurs in `RESULTS_BY_NAME`.
- `RECORDED_AS_RESULT` is empty.
- `UNEXPECTED_SKIPS` is empty.
- `MISSING_FROM_EVERYTHING` is empty.
- The operator-reported verdict is `PASS`.

## 5. Operator-executed normal-path verification

The following output was supplied by the operator for the normal path on a machine where symlink creation is available:

```text
371/371 passed
1 skipped, 1 registered of 5 allowed: T68c a real 0o000 directory is reported by path (integration)
```

This preserves the existing test total and the existing T68c skip.

## 6. Operator-executed negative skip-registry checks

The operator supplied the following negative-check results. These checks establish that an unregistered skip name and a mismatched reason for a registered skip are rejected by the main gate.

Unregistered name:

```text
unregistered-name -> PASS ["UNEXPECTED_SKIPS: ['T99 a case nobody registered (some reason)']", 'MAIN_EXIT: 1']
```

Incorrect reason for a registered name:

```text
wrong-reason      -> PASS ["UNEXPECTED_SKIPS: [\"T36 directory symlink is rejected as a governed root: skip reason 'a different reason' is not the registered one\"]", 'MAIN_EXIT: 1']
```

Both negative cases were reported as `PASS` because the main gate rejected the invalid skip registration with exit code 1.

## 7. Reproduction commands

Run from the repository root:

```bash
python verify_symlink_unavailable.py
python scripts/test_check_document_management.py
```

The first command exercises the forced symlink-unavailable path and its accounting checks. The second command runs the normal test suite.

The operator-provided outputs above are evidence of execution. They are not represented as execution by the implementation session.

## 8. Execution status

**Code paths verified by operator; document metadata pending completion and repository-gate revalidation.**

The operator supplied successful results for:
- forced symlink-unavailable accounting;
- normal-path test suite (`371/371 passed`, with the existing T68c skip);
- rejection of an unregistered skip name;
- rejection of a mismatched registered skip reason.

The three work-record documents required `document_metadata` front matter. `session-evidence.md` also required the validator-recognized role, input, and output sections. Those documentation changes are included in this revision.

The GOV-DOC-002 command and Session Evidence validator have not yet been reported as rerun against the revised documents. Their status therefore remains pending.

## 9. Non-claims

- The operator-executed outputs are not claimed as implementation-session self-tests.
- No claim is made that GOV-DOC-002 passed after the document metadata changes.
- No claim is made that the Session Evidence validator passed after the required sections were added.
- No claim is made that a pull request was merged.
- No claim is made that review or Owner acceptance occurred.
