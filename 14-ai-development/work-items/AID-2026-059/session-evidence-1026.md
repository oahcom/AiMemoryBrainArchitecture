---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Every figure in 'AI-visible output' was produced in this session by running the commands named there against this branch. The suite count, the two mutation results and the gate verdicts are transcriptions of that output, not estimates."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session evidence — AID-2026-059 / Issue #1026

## Session role

IMPLEMENTER. Repair the ordering defect reported in Issue #1026: the session
evidence validator enforced the PR-body declaration before its own historical
exemption could run, so a pull request whose linked Issues all predate the
policy effective time was required to fill a declaration that the policy says
does not yet apply to it.

The session was executed by an AI agent. This record is the agent's report
about its own work, not a third-party attestation.

## Actual AI input

The operative input is the assignment transcribed in
`14-ai-development/work-items/AID-2026-059/prompt-1026-v1.md`, pinned by
digest at 4811 bytes / `2505838934...e4bd9`. It contains the measured facts to
re-verify, the Owner ruling on the shape of the fix, the four required
assertions, and the reverse-verification requirement.

Two directives governed the session and are quoted because the acceptance
criteria are stated against them:

> The repository's standing rule is "测试通过 ≠ 测试有效". A passing test must be shown to fail when the thing it guards is broken.

> Step 3 is deliberately stricter than issue #1026's step 3 ... A PR that *volunteers* `AI-assisted work: YES` with a reference that does not exist must still fail.

## AI-visible output

### What was measured before changing anything

- `_run_checks` at `validate.py:1946` begins with
  `check_01_pr_fields_and_issue_references`, which is where
  `_parse_status(_extract_field(ctx.body, "AI-assisted work"), "PR")` raises
  `PR: missing AI-assisted work declaration`.
- `ctx.issues` is **not** populated by `check_01`. It is built in
  `_load_context` (`validate.py:1833-1862`) from the same
  `parse_related_issues(ctx.body, ctx.repo)` call. The issue's premise that the
  guard depends on `check_01` having run does not hold in this revision: a
  naive move of the guard to the top of `_run_checks` would still see a
  populated map. The fix is written to be correct either way — it re-parses and
  then asserts that the two resolutions agree, so an empty map can never reach
  the guard.
- Baseline suite on `origin/main` at `83c78647`: `Ran 68 tests ... OK`.

### What changed

- `scripts/governance/session_evidence/validate.py`: the linked Issues are
  parsed at the top of `_run_checks`; an agreement check fails closed if that
  set and `ctx.issues` disagree; the historical guard now runs before
  `check_01`, but only an undeclared body is returned early. A body that
  declares either field falls through to the unchanged order.
- `tests/session_evidence/test_validate.py`: four assertions added.

### Verification actually run on this branch

The branch is based on `22c44b37`; four files changed.

```
python3 -m unittest tests.session_evidence.test_validate
    Ran 83 tests ... OK
```

```
mutation 1: _historical_not_applicable -> return False unconditionally
    killed by test_pre_effective_undeclared_pr_is_not_applicable
    AssertionError: 1 != 0   (assertEqual(result, 0))

mutation 2: early exit unconditional (declaration-presence check removed)
    killed by test_pre_effective_pr_volunteered_yes_with_missing_evidence_fails
    AssertionError: 0 != 1   (assertEqual(result, 1))
```

Both mutants were restored before the full suite was re-run, which reported
`Ran 83 tests ... OK` again.

Gate conclusions read, not assumed:

```
python3 scripts/ci/check_line_endings.py
    1328 files inspected, 0 violations

python3 scripts/ci/check_repository_hygiene.py --base <main> --head <branch>
    Work-item index membership directories=50 linked=50
    Work-item manifest consistency manifests=39 in_scope=37 violations=0
    Repository new-file admission passed: 2 new path(s) checked

python3 scripts/check_document_management.py --require-changed origin/main
    PASS (incremental): no GOV-DOC-002 violations; 216 classified, 493 unclassified

BILINGUAL-MANIFEST: COMPLETE BASE_SHA..HEAD_SHA python3 scripts/check_bilingual_docs.py
    bilingual baseline: 77 frozen, 0 new gaps
    PASS (5 changed paths inspected)
```

The first draft of assertion 3 used an Issue that declared YES, which made the
historical guard `False` on its own; mutation 2 survived it. The test was
rewritten so the guard is `True` and only the declaration-presence check stands
between the mutant and a false `NOT_APPLICABLE`.

While this branch was open, `main` advanced twice and gained the rule that a
canonical manifest entry may name a `LEGACY_UNDECLARED` row. The branch was
rebased; the manifest entry for this session now names Issue #1026 rather than
attributing its evidence at PR scope, because that attribution became legal.

### What could not be verified

- The workflow job reads the validator from the **base** revision, so the first
  run of this pull request cannot exercise the repaired logic; it exercises the
  base copy, which still contains the defect. This is recorded rather than
  worked around: the pull request carries a full declaration, so the base
  validator has nothing to complain about, and the fix lands for later pull
  requests.
- No independent review exists for this change. `independent_reviewer` stays
  `NOT_ASSIGNED` in the work item.
- The four new tests exercise the validator through its offline fixtures. They
  do not exercise the GitHub API, the workflow file, or branch protection.
