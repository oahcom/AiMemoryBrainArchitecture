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
    canonical_scope: "Implementation prompt snapshot for AID-2026-290 symlink-boundary test accounting correction."
    canonical_scope_id: "ai-development/aid-2026-290-prompt-snapshot"
    canonical_scope_keywords:
      - "AID-2026-290"
      - "prompt snapshot"
      - "symlink boundary"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-290 — Prompt Snapshot

## 1. Task

Correct the symlink-unavailable handling in `scripts/test_check_document_management.py` for the four affected test cases:

- T36 directory symlink is rejected as a governed root
- T37 governed_files does not descend into a symlinked root
- T41 symlinked governed file is rejected
- T42 governed file reached through a symlinked parent is rejected

The defect is test-result accounting: when symlink creation is unavailable, a test must be recorded as skipped, not also recorded as a result, and must not leave an unaccounted test case.

## 2. Required behavior

When `Path.symlink_to` raises `OSError` or `NotImplementedError`:

1. T36 is independently recorded through `skip()`.
2. T37 is independently recorded through `skip()`, even though it shares the directory-symlink prerequisite with T36.
3. T41 is recorded through `skip()` if the governed-file symlink setup cannot be completed.
4. T42 is recorded through `skip()` if the symlinked-parent setup cannot be completed.
5. None of these skipped cases may subsequently call `record()`.
6. The four cases must not appear in `RESULTS_BY_NAME`.
7. `UNEXPECTED_SKIPS` must remain empty when the registered skip reason is used.
8. Every case must be accounted for: no missing case and no duplicate accounting.

The exact registered skip reason is:

`symlink creation unavailable on this platform`

The four existing `ALLOWED_SKIPS` registrations are to remain unchanged. T68c's existing skip behavior is also unchanged.

## 3. Scope and exclusions

In scope:
- The symlink-boundary test function and its result-accounting branches.
- Evidence describing the initial failure and the corrected operator-executed verification.

Out of scope:
- Production document-management checker behavior.
- T68c and its integration behavior.
- Other test cases or test-count changes.
- Any change to the four registered skip names or their exact reason.
- Any change to the test source after the operator-executed verification recorded in the evidence.

## 4. Verification contract

The operator verification commands are:

```bash
python verify_symlink_unavailable.py
python scripts/test_check_document_management.py
```

The forced-unavailability check must demonstrate:
- the four affected cases occur in `SKIPPED`;
- they do not occur in `RESULTS_BY_NAME`;
- `RECORDED_AS_RESULT` is empty for those four cases;
- `UNEXPECTED_SKIPS` is empty;
- `MISSING_FROM_EVERYTHING` is empty;
- the verdict is `PASS`.

The normal-path suite must preserve the existing total test count and the existing T68c skip.

Negative checks must demonstrate that an unregistered skip name and a mismatched registered skip reason are rejected by the main gate with exit code 1.

## 5. Evidence discipline

Execution evidence supplied by the operator must be labeled as operator-executed. It must not be represented as a test run performed by the implementation session.

Do not claim:
- corrected code was independently executed by the implementation session;
- GOV-DOC-002 passed after the metadata correction;
- Session Evidence validation passed;
- a PR was merged;
- review or Owner acceptance occurred.

The work item remains in progress until the repository's required document and session-evidence gates have been run against the committed files.
