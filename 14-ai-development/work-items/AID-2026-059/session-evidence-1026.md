---
document_metadata:
  domain: ai-development
  steward: "Architecture Governance"
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

**What was measured before changing anything.**

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

**What changed.**

- `scripts/governance/session_evidence/validate.py`: the linked Issues are
  parsed at the top of `_run_checks`; an agreement check fails closed if that
  set and `ctx.issues` disagree; the historical guard now runs before
  `check_01`, but only an undeclared body is returned early. A body that
  declares either field falls through to the unchanged order.
- `tests/session_evidence/test_validate.py`: six test methods added.

**Verification actually run on this branch.**

The branch is based on `ee4f81d9`, the merge base of the implementation
commits with the merge commit `940a4cb3` (`git merge-base 0b7b9ba2^ 940a4cb3`).
An earlier draft recorded `0bbb35f1`, which is `Merge pull request #1046` — an
ancestor of the merge, but not this branch's base. That is why this note and
the `AID-2026-064` record disagree about the base: `AID-2026-064` records
`7a69f32b` (`Merge pull request #1039`), which is the base of *its* branch.
Both values are real commits; they answer the question for different branches,
and neither is a typo.

The code change is two files, plus three work-record files (`manifest.yaml`,
this document, `prompt-1026-v1.md`).

```
python3 -m unittest tests.session_evidence.test_validate
    Ran 85 tests ... OK
```

```
mutation 1: _historical_not_applicable -> return False unconditionally
    killed by test_pre_effective_undeclared_pr_is_not_applicable
        AssertionError: 1 != 0   (assertEqual(result, 0))
    also killed: test_pr_opened_before_the_effective_time_without_a_declaration_is_not_applicable,
                 test_pre_effective_pr_volunteered_yes_with_valid_evidence_is_not_applicable,
                 test_historical_issue_outputs_not_applicable_and_success

mutation 2: early exit unconditional (declaration-presence check removed,
            PR opening date still required)
    killed by test_pre_effective_pr_volunteered_yes_with_missing_evidence_fails
        AssertionError: 0 != 1   (assertEqual(result, 1))
    also killed: test_post_policy_missing_declaration_is_missing_and_failed,
                 test_rejects_missing_post_policy_issue_declaration

mutation 3: PR opening-date bound removed, rest of the condition intact
    killed by test_pr_opened_after_the_effective_time_without_a_declaration_fails
        AssertionError: 0 != 1   (assertEqual(result, 1))
```

The three mutants are not tight: mutants 1 and 2 each take down sibling tests as
well, because every one of those tests needs the guard or the declaration check
to exist. Each mutant was restored before the next was applied, and the full
suite was re-run green after the last restoration.

Gate conclusions read, not assumed:

```
python3 scripts/ci/check_line_endings.py
    Line-ending check: 1339 files inspected, 0 binary skipped, 0 violations.

python3 scripts/ci/check_repository_hygiene.py --base 69cb05c9573f204821b25ee4bd199bc4c3b5dad6 --head ff8a33b2e0bcb68cfe4491d532eeea93790b411a
    Work-item index membership version=2026-11-24.7 directories=55 linked=55
    Work-item manifest consistency version=2026-11-24.7 manifests=44 in_scope=42 excluded_by_record_type=2 unrecognized=0 violations=0
    Repository new-file admission version=2026-11-24.7 base=69cb05c9573f204821b25ee4bd199bc4c3b5dad6 head=ff8a33b2e0bcb68cfe4491d532eeea93790b411a merge_base=69cb05c9573f204821b25ee4bd199bc4c3b5dad6
    Repository new-file admission passed: 0 new path(s) checked.
    exit code 0

  The head named above is the parent of the commit that carries this quotation;
  quoting a commit inside itself is impossible, and the two differ only by this
  block. The earlier draft quoted `--base 0bbb35f1 --head 17f155e1`, neither of
  which is a base or head of the merged work.

python3 scripts/check_document_management.py --require-changed 0bbb35f1
    PASS (incremental): no GOV-DOC-002 violations; 219 classified, 493 unclassified

BASE_SHA=... HEAD_SHA=... PR_BODY=... python3 scripts/check_bilingual_docs.py
    bilingual baseline: 77 frozen, 0 new gaps
    Bilingual documentation and prompt-library gate: PASS (6 changed paths inspected)
```

The first draft of assertion 3 used an Issue that declared YES, which made the
historical guard `False` on its own; mutation 2 survived it. The test was
rewritten so the guard is `True` and only the declaration-presence check stands
between the mutant and a false `NOT_APPLICABLE`.

While this branch was open, `main` advanced twice and gained the rule that a
canonical manifest entry may name a `LEGACY_UNDECLARED` row. The branch was
rebased; the manifest entry for this session now names Issue #1026 rather than
attributing its evidence at PR scope, because that attribution became legal.

A later review added one more bound to the same guard: the exemption now also
requires the pull request itself to have been opened before the effective time.
Checking only the Issues was not enough, because every Issue here predates the
policy and declares nothing, so a silent pull request was exempted and "link an
old Issue and say nothing" would have been a permanent way out from the
effective time onwards. The condition is now date-bounded at both ends.

**What could not be verified.**

- The workflow job reads the validator from the **base** revision, so the first
  run of this pull request cannot exercise the repaired logic; it exercises the
  base copy, which still contains the defect. This is recorded rather than
  worked around: the pull request carries a full declaration, so the base
  validator has nothing to complain about, and the fix lands for later pull
  requests.
- No independent review exists for this change. `independent_reviewer` stays
  `NOT_ASSIGNED` in the work item.
- The six new tests exercise the validator through its offline fixtures:
  `test_pre_effective_undeclared_pr_is_not_applicable`,
  `test_pre_effective_pr_with_post_effective_issue_requires_declaration`,
  `test_pre_effective_pr_volunteered_yes_with_missing_evidence_fails`,
  `test_pre_effective_pr_volunteered_yes_with_valid_evidence_is_not_applicable`,
  `test_pr_opened_before_the_effective_time_without_a_declaration_is_not_applicable`
  and `test_pr_opened_after_the_effective_time_without_a_declaration_fails`.
  They do not exercise the GitHub API, the workflow file, or branch protection.
