---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count and exit code below was produced by a command run against this branch, based on origin/main b978d9bb, on 2026-11-26."
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

# Session evidence — AID-2026-081

## Session role / use case

IMPLEMENTER. This session measured the contradiction reported in issue #1081,
corrected the workflow comment, and added the check that compares it to the
baseline it describes. It did not regenerate the baseline and did not touch the
unrelated `scripts/bilingual-baseline.txt`.

## Actual AI input

The assignment that produced this change, abridged only where it repeated
repository context:

> Job: fix issue #1081 — a workflow comment states a number that the artifact it
> describes contradicts, and nothing compares them.
>
> Part 1 — fix the comment. Change `81` to `77` and make the sentence carry its
> own provenance so the next reader can tell whether it is still true ...
> Do not merely swap the digit; a bare number is what rotted.
>
> Part 2 — the actual defect: make the claim checkable. ... Add the cheapest
> check that prevents recurrence. ... It must FAIL when the comment's number is
> edited to a wrong value ... It must PASS on the corrected main tree. ... If the
> ratchet is allowed to be RED on main by design ... your check must still be
> green — it compares counts, not pass/fail. `0` must never mean "could not
> check"; if the baseline cannot be read, exit 2.

## AI-visible output

The output visible to the user is: the diff to `.github/workflows/gates.yml` and
`scripts/ci/test_gate_ratchet.py`, the three files in this directory, one row
appended to `14-ai-development/work-items/INDEX.md`, and the pull request that
carries them.

## 1. What the comment said, and what the artifacts said

At `origin/main` `1f5ba824`, `.github/workflows/gates.yml` line 159 read:

```
# GOV-DOC-001 full scan: 81 normative paths lack an en/zh-CN counterpart.
```

Measured:

```
scripts/ci/baselines/bilingual-docs.txt    77 lines, 77 non-comment entries, 77 unique, no header
scripts/bilingual-baseline.txt             79 lines, 77 non-comment entries, has a header (NOT this gate's input)
python3 scripts/check_bilingual_docs_full.py    reports 001. .. 077., then "GOV-DOC-001 full scan: FAIL"
python3 scripts/ci/gate_ratchet.py ...          "baseline=77 current=77 regressions=0 fixed=0", "PASS", exit 0
```

The comment is wrong by four against both inputs. The ratchet was green because
the failure set matched the baseline exactly — it never reads the comment.

## 2. The check

`scripts/ci/test_gate_ratchet.py` already runs in CI, from the
`Self-check the ratchet wrapper` step of the `bilingual` job. One test was
added to it:

- `STATED_COUNT` matches `# GOV-DOC-001 full scan: <n> normative paths` in
  `gates.yml`, read as text (no YAML parser, matching
  `check_session_evidence_workflow_shape.py`).
- `baseline_entries()` counts `scripts/ci/baselines/bilingual-docs.txt` the way
  `gate_ratchet.py` does: non-blank, non-comment, deduplicated.
- The test asserts exactly one such comment and that its number equals that
  count.

`main()` pre-reads both artifacts and exits 2 with `INCOMPLETE` if either
cannot be read, so an unreadable file is never reported as a violation. Exit 0
and 1 come from unittest.

## 3. The mutation

With the comment edited to `81`:

```
AssertionError: 81 != 77 : gates.yml says 81 normative paths; bilingual-docs.txt has 77 entries
----------------------------------------------------------------------
Ran 7 tests in 1.489s

FAILED (failures=1)
EXIT=1
```

Restored to `77`, the same command prints `Ran 7 tests`, `OK`, exit 0. The
ratchet itself was not run by the check and its red-on-main state does not
affect the result.

## 4. Exit codes

```
corrected tree                 0   (7 tests OK)
comment edited to 81           1   (AssertionError above)
baseline path made unreadable  2   (INCOMPLETE: [Errno 2] No such file or directory: 'does-not-exist.txt')
```

## 5. What this record does not claim

- It does not claim the historical `baseline=81 current=81` rows in
  `14-ai-development/ci-gates-and-ratchets.{en,zh-CN}.md` are wrong. They record
  a 2026-11-22 measurement and were left unedited.
- It does not claim the check generalises to other prose numbers. It pins one
  comment against one file, because that is the only such claim with a
  machine-readable counterpart.
- It does not claim the ratchet is green on main. The ratchet is a ratchet.
- `executed_prompt_provenance` is `NOT_VERIFIED`: the prompt was written from
  the same measurements as this record but was not re-read line by line against
  the final diff.
