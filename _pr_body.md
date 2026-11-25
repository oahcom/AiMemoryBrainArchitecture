BILINGUAL-MANIFEST: COMPLETE

## Work Item ID

AID-2026-059

## Related issue(s)

#1026

## AI-assisted work

YES

## Session evidence reference(s)

14-ai-development/work-items/AID-2026-059/session-evidence-1026.md

## Per-Issue AI session evidence

| Related Issue | Issue AI-assisted work | Evidence refs for this Issue |
| --- | --- | --- |
| https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1026 | LEGACY_UNDECLARED | N/A |

Issue #1026 was opened on `2026-11-25T02:12:29Z`, before `AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC`, and carries no declaration of its own. Its row is `LEGACY_UNDECLARED` / `N/A` rather than `YES`: `YES` would claim the Issue declared AI-assisted work, and it does not.

## The defect

`_run_checks` called `check_01_pr_fields_and_issue_references` as its first statement, and `check_01` raises on a missing `AI-assisted work` declaration. The historical guard ran near the end. So a pull request whose linked Issues all predate the effective time still had to fill a form the policy says does not apply to it — and PRs that complied were then told `NOT_APPLICABLE`. `#1013` passed for exactly that reason.

## The fix, and why the obvious version is wrong

`_historical_not_applicable` returns `False` on an empty `ctx.issues`. Moving the guard to the top of `_run_checks` without first resolving the Issue set would therefore make the gate validate nothing — the #1003 fail-open.

The linked Issues are parsed before any enforcement, and the two resolutions are compared:

```python
linked = parse_related_issues(ctx.body, ctx.repo)

if set(linked) != set(ctx.issues):
    raise ValidationError(
        "Internal error: linked Issues were not resolved "
        "before validation"
    )
```

Then only an **undeclared** body is exempted:

```python
if (
    _historical_not_applicable(ctx)
    and _extract_field(ctx.body, "AI-assisted work") is None
    and _extract_field(
        ctx.body, "Session evidence reference(s)"
    ) is None
):
    return _not_applicable_verdict(ctx)
```

Everything after that line is unchanged. Issue #1026 step 3 asked for the body checks to be skipped for every pre-effective PR; that is deliberately **not** implemented, because a PR that volunteers `AI-assisted work: YES` with a reference that does not exist would then pass. The ceiling is named in a code comment.

## Tests

```
python3 -m unittest tests.session_evidence.test_validate
    Ran 83 tests in 0.367s
    OK
```

Four assertions added:

| test | what it pins |
|---|---|
| `test_pre_effective_undeclared_pr_is_not_applicable` | the bug: body is only `Related issue(s): #101`, exits 0 with `NOT_APPLICABLE` |
| `test_pre_effective_pr_with_post_effective_issue_requires_declaration` | one linked Issue postdates the policy, so the missing declaration still fails |
| `test_pre_effective_pr_volunteered_yes_with_missing_evidence_fails` | a volunteered `YES` with a nonexistent path still fails |
| `test_pre_effective_pr_volunteered_yes_with_valid_evidence_is_not_applicable` | a volunteered `YES` with an existing non-empty path exits 0 with `NOT_APPLICABLE` |

## Reverse-verification

A passing test that cannot fail is not evidence.

```
mutation 1: _historical_not_applicable -> return False unconditionally
  test_pre_effective_undeclared_pr_is_not_applicable
  AssertionError: 1 != 0   (self.assertEqual(result, 0))

mutation 2: early exit unconditional (declaration-presence check removed)
  test_pre_effective_pr_volunteered_yes_with_missing_evidence_fails
  AssertionError: 0 != 1   (self.assertEqual(result, 1))
```

Both mutants were restored and the full suite re-run green after each.

The first draft of assertion 3 used an Issue that declared `YES`, which made the historical guard `False` on its own. Mutation 2 survived that draft. The test was rewritten so the guard is `True` and only the declaration-presence check stands between the mutant and a false `NOT_APPLICABLE`.

## Gates read, not assumed

```
python3 scripts/ci/check_line_endings.py
    1328 files inspected, 0 binary skipped, 0 violations.

python3 scripts/ci/check_repository_hygiene.py --base <main> --head <branch>
    Work-item index membership version=2026-11-24.7 directories=50 linked=50
    Work-item manifest consistency manifests=39 in_scope=37 violations=0
    Repository new-file admission passed: 2 new path(s) checked.

python3 scripts/check_document_management.py --require-changed origin/main
    PASS (incremental): no GOV-DOC-002 violations; 216 classified, 493 unclassified

BASE_SHA=... HEAD_SHA=... PR_BODY=... python3 scripts/check_bilingual_docs.py
    bilingual baseline: 77 frozen, 0 new gaps
    PASS (5 changed paths inspected)
```

The bilingual gate needs `BASE_SHA`/`HEAD_SHA`/`PR_BODY`; with all three set it passes on the five changed paths. `AID-2026-059/` is under `PAIR_EXEMPT_PREFIXES`, so the two new Markdown files are not required to have counterparts, and the PR body declares `BILINGUAL-MANIFEST: COMPLETE` because the work-item tree is a normative root.

## What this PR cannot do

The workflow runs the validator from the **base** revision. This pull request therefore exercises the base copy, which still contains the defect — a validator fix can never certify the pull request that carries it (recorded as F8 in `AID-2026-059`). It carries a full declaration, so the base validator has nothing to object to, and the repair takes effect for the pull requests opened after it merges.

Nothing here changes the policy effective time, the workflow file, or branch protection.

## What was measured and contradicted the issue text

Issue #1026 states that `ctx.issues` is populated as a side effect of `parse_related_issues` inside `check_01`. In this revision it is populated in `_load_context` (`validate.py:1833-1862`) from the same call, so a guard moved to the top of `_run_checks` would have seen a populated map. The fix is still written against the stated risk rather than against the observation: it re-parses and fails closed if the two resolutions disagree, so it is correct whichever of the two is true.
