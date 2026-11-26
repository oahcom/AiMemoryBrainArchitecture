---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every exit code, message fragment and test name quoted below was produced by running the code on 2026-11-25 in a detached worktree at a316ff69 rebased onto main c7e87f8f, not read off the source. The three reverts were applied to the guard in isolation and restored; the guard is byte-identical to a316ff69 at this branch's head."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session role / use case

IMPLEMENTER for the tests. Issues #1045 and #1058 report two defects in
`scripts/check_session_evidence_workflow_shape.py`; commit `a316ff69` fixes both
and states in its own message that the tests are not yet written. This session
wrote those tests and the registration that makes them accountable.

This session did not change the fix. The guard is byte-identical to `a316ff69`
at this branch's head, and the reason is stated rather than implied: a test
written against a fix its author can also edit proves less than one that cannot.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the instruction
this change was carried out against, pinned at
`08eb2369f7f6228adbbb4dfc4df88b6ceaf9381be1a5d4bf90ad61ec32145c1a`, 5089 bytes.

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
session read.

**Read before writing:**

| input | what it settled |
|---|---|
| `scripts/test_check_session_evidence_workflow_shape.py` at `a316ff69` | the style: a throwaway tree per case, `WORKFLOW` as a fixture string, `run_checker()` returning `(exit code, stderr)`, assertions on message text and not only on the code |
| `scripts/check_session_evidence_workflow_shape.py` at `a316ff69` | `NEEDS_KEY_RE`, `_checkout_refs`, `JobBlock.first_line` / `StepBlock.first_line`, and the exact message shape `line {offset}: {line.strip()}` |
| the same file's pre-fix body (`a316ff69^`) | the revert targets: `^    needs:\s*\S`, and `offenders.append(next(line.strip() ... if CHECKOUT_RE.match(line)))` |
| Issue #1045 body | the acceptance the message must meet: quote the `ref:` line, with the action reference only if there is no `ref:` line |
| Issue #1058 body | the measured mutation table, and the note that `test_validate_needs_is_a_violation` uses the flow form only |

# What was added

Two tests, in the existing class, following its existing helpers.

1. `test_validate_block_form_needs_is_a_violation_naming_the_needs_line` — builds
   the block form, asserts exit 1, asserts the message names `` `needs:` ``,
   computes the 1-based line of the `needs:` line and the line of the `validate:`
   job id from the fixture it just wrote, then asserts the message contains
   `(line {needs_line}: needs:)` and does **not** contain `(line {job_line}:`.
   The negative half is what makes "named the job instead" fail.
2. `test_ref_violation_quotes_the_ref_line_and_not_the_uses_line` — mutates the
   head job to carry `ref: ${{ github.event.pull_request.head.sha }}`, asserts
   exit 1, computes that line's number, asserts
   `(line {ref_line}: {ref})` is present and `uses: actions/checkout@v4` is
   absent. The negative assertion is the direction: the token `ref:` already
   appears in the message's prose, so a positive assertion alone held under the
   defect.

# Reverse-verification

Each fix was reverted in isolation in this worktree, the single test run, the
result captured, and the guard restored. The guard was copied to
`C:/tmp/opencode/_w1081_guard.bak` before the first revert and restored from it
after the last; `git diff` against `a316ff69` for that path is empty.

**Revert 1 — `NEEDS_KEY_RE` back to flow-form only.**

```
NEEDS_KEY_RE = re.compile(r"^    needs:\s*\S")
```

```
$ cd scripts && python -m unittest test_check_session_evidence_workflow_shape.SessionEvidenceWorkflowShapeTest.test_validate_block_form_needs_is_a_violation_naming_the_needs_line
F
======================================================================
FAIL: test_validate_block_form_needs_is_a_violation_naming_the_needs_line
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\tmp\opencode\w1081\scripts\test_check_session_evidence_workflow_shape.py", line 174, in test_validate_block_form_needs_is_a_violation_naming_the_needs_line
    self.assertEqual(code, 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^
AssertionError: 0 != 1

Ran 1 test in 0.003s
FAILED (failures=1)
```

**Revert 2 — `_checkout_refs` back to quoting the `uses:` line.**

```
if any(REF_KEY_RE.match(line) for line in step_lines):
    offenders.append(next(
        line.strip() for line in step_lines if CHECKOUT_RE.match(line)
    ))
```

```
$ cd scripts && python -m unittest test_check_session_evidence_workflow_shape.SessionEvidenceWorkflowShapeTest.test_ref_violation_quotes_the_ref_line_and_not_the_uses_line
F
======================================================================
FAIL: test_ref_violation_quotes_the_ref_line_and_not_the_uses_line
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\tmp\opencode\w1081\scripts\test_check_session_evidence_workflow_shape.py", line 214, in test_ref_violation_quotes_the_ref_line_and_not_the_uses_line
    self.assertIn(f"(line {ref_line}: {ref})", message)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '(line 22: ref: ${{ github.event.pull_request.head.sha }})' not found in "::error::the 'self-test-pr-head' job's checkout step declares a `ref:` key (uses: actions/checkout@v4); ..."
```

**Revert 3 — a partial fix: the right line, no line number.** This is the shape
`origin/main` carried after #1077, and the test is required to reject it.

```
offenders.append(line.strip())          # was: f"line {offset}: {line.strip()}"
```

```
AssertionError: '(line 22: ref: ${{ github.event.pull_request.head.sha }})' not found in "::error::the 'self-test-pr-head' job's checkout step declares a `ref:` key (ref: ${{ github.event.pull_request.head.sha }}); ..."
```

**Revert 4 — a partial fix for #1058: block form caught, line number dropped.**

```
f"the {VERDICT_JOB!r} job declares `needs:`; the verdict must not "
```

```
AssertionError: '(line 26: needs:)' not found in "::error::the 'validate' job declares `needs:`; the verdict must not depend on another job, or a PR can suppress it by breaking that job (job: validate)"
```

All four are `AssertionError`. None is a traceback and none is an `ImportError`.

# AI-visible output

```
scripts/test_check_session_evidence_workflow_shape.py   +2 tests, 10 existing untouched
14-ai-development/work-items/AID-2026-073/              manifest, prompt, this record
14-ai-development/work-items/INDEX.md                   one row
scripts/check_session_evidence_workflow_shape.py        unchanged, byte-identical to a316ff69
```

# Limitations

1. **The tests bind behaviour, not the wording of the message.** They pin that
   the `needs:` line and the `ref:` line are quoted with their numbers, and that
   the `uses:` line is not. A rewrite of the surrounding sentence that keeps
   those four facts would still pass. That is deliberate: the sentence is prose
   and the line reference is the contract.
2. **The second hole in Issue #1058 is not covered.** `REQUIRED_JOB_IDS`
   membership is bound by no test — deleting `"validate"` from that tuple leaves
   the suite green, because the guard would then never look at the verdict job.
   It is a third property, not one of the two fixes at `a316ff69`, and this work
   item says so rather than letting a green suite imply otherwise.
3. **No independent review is claimed.** The reverse-verification is reproducible
   by anyone with the branch, which is the reason it is written out as commands
   and output rather than summarised as "verified".
4. **#1045 is closed and #1058 is open.** This record names both Issues and does
   not claim that either one's acceptance is met by it.
