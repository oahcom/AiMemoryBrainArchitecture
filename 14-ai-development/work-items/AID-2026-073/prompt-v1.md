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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The two defects were re-read on 2026-11-25 from the committed guard at a316ff69 and from Issue #1045 and Issue #1058 as they stand; every exit code and message quoted here was reproduced by running the guard, not inferred from its source."
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

# WO — Test the two workflow-shape guard defects (#1045, #1058)

Scope: add tests to `scripts/test_check_session_evidence_workflow_shape.py` that
fail when either behavioural fix in `a316ff69` is reverted. The fixes themselves
are done and are not changed by this work item.

## What the guard is, and why the tests are the work

`scripts/check_session_evidence_workflow_shape.py` asserts three properties of
`.github/workflows/session-evidence.yml`: the three job ids exist, the PR-head
job's checkout carries no `ref:`, and the verdict job carries no `needs:`. The
workflow was split into three jobs by PR #1014 after a single-job workflow had
produced 18 consecutive failing runs (#1008), and the guard exists so the split
cannot be undone silently.

A guard whose message is wrong, or which passes a shape it forbids, is the
failure mode it was built to prevent. Both defects are of that kind, and neither
was reachable by the suite as it stood: the flow-form `needs:` test was the only
`needs:` test, and no test asserted which line the `ref:` message quotes.

## Defect 1 — block-form `needs:` passed (#1058)

The regex was `^    needs:\s*\S`, which requires a value on the same line. YAML's
preferred spelling puts the value on the following lines, and that is the form a
person writes by hand:

```yaml
  validate:
    needs:
      - self-test-pr-head
```

Measured against the unmutated guard, that mutation returned exit 0 and printed
`PASS`, for a dependency the guard exists to forbid.

The fix is `NEEDS_KEY_RE = re.compile(r"^    needs:(\s*\S|\s*$)")`, which admits
both spellings.

## Defect 2 — the wrong line was quoted (#1045)

`_checkout_refs` appended the step's `uses:` line while the violation is on the
`ref:` line, producing:

```
::error::the 'self-test-pr-head' job's checkout step declares a `ref:` key
(uses: actions/checkout@v4); ...
```

`uses: actions/checkout@v4` is the one line in such a step that is already
correct. The fix carries `first_line` through `JobBlock`/`StepBlock` and emits
`line {offset}: {line.strip()}`, so the message reads
`(line 44: ref: ${{ github.event.pull_request.head.sha }})`.

## Acceptance asked for

1. A test that fails with `AssertionError` when `NEEDS_KEY_RE` is reverted to
   `^    needs:\s*\S`. It asserts exit 1, that the output names the `needs:` key,
   and that it carries the line number of the `needs:` line — not the job name
   alone, and not the line of the job id.
2. A test that fails with `AssertionError` when `_checkout_refs` is reverted to
   quoting the `uses:` line. It asserts the message contains the `ref:` text and
   does not contain the `uses:` text. The negative assertion is the direction:
   the token `ref:` already appears in the message's prose, so a positive
   assertion alone would hold under the defect.
3. Neither test fails with a traceback or an `ImportError` under either revert.
   A test that dies on a missing attribute proves nothing about behaviour.
4. The nine tests already in the file still pass, unmodified. The suite runs all
   of them plus the new ones.

## Excluded, and stated as excluded

- `scripts/check_session_evidence_workflow_shape.py`. The behaviour is fixed and
  verified; this work item tests it. If the fix is wrong, that is reported, not
  edited here.
- `.github/workflows/session-evidence.yml`. The guard is held to the real
  workflow; mutating the workflow to make a test pass would invert the relation.
- The second hole in Issue #1058 — that `REQUIRED_JOB_IDS` membership is not
  bound by any test. Issue #1058 records it as a separate property; it is not
  one of the two fixes at `a316ff69` and is not covered here.
