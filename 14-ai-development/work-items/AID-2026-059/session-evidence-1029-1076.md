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
      last_verification_note: "Every figure in 'AI-visible output' was produced in this session by running the commands named there against this branch. The suite counts, the mutation results and the gate verdicts are transcriptions of that output, not estimates."
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

# Session evidence — AID-2026-059 / Issues #1029, #1058, #1061, #1063, #1071, #1074, #1076

## Session role / use case

IMPLEMENTER. Close seven residuals left open after the session-evidence gate
landed. Their common shape: a check that reported success over a fact it never
read.

| Issue | Check | What it never read |
|---|---|---|
| #1029 | `check_declared_check_contexts.py` | the protected set — only the declared one |
| #1058 | workflow-shape guard | `REQUIRED_JOB_IDS` membership |
| #1061 | `check_09` | an entry the PR cites but did not write |
| #1063 | every test | `AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC` |
| #1071 | `check_traceability.py` | the tree — it had no caller |
| #1074 | `Session Evidence` | the body at merge time |
| #1076 | `_run_checks` precondition | nothing: the condition was `X != X` |

The session was executed by an AI agent. This record is the agent's report about
its own work, not a third-party attestation.

## Actual AI input

The operative input is the assignment transcribed in
`14-ai-development/work-items/AID-2026-059/prompt-1029-1076-v1.md`, pinned by
digest at 9174 bytes /
`636ebb9e853c593091b293f5ea709c0936ef7bab3b7987d118c0d1847382ed94`. It names
the seven defects, the required behaviour per Issue, the three session
constraints, and the integration policy: each Issue in its own worktree, no
push, no PR, integration centralised so conflicting edits are ordered
deliberately rather than by merge order.

## AI-visible output

**What changed, by commit.** Seven commits, rebased onto `main` at
`30c7277e1fc1f08f2b11fa1d3cf4ad80793a4184`:

```
5a2fda7  fix(session-evidence): require an entry's Issue links when the PR cites it, not only when it writes it (#1061)
dc86a59  fix(session-evidence): replace the unfalsifiable fail-open precondition with one that can fire (#1076)
52b2fcc  fix(session-evidence): re-run on body edits and bind the verdict to the body it judged (#1074)
542d05c  fix(ci): detect block-form needs: and pin the verdict job as required (#1058)
fd8f319  test(session-evidence): pin the production effective-time boundary to a test (#1063)
d93108a  fix(gov-doc): compare the protected context set to the declared one, not only to the workflow tree (#1029)
714f2cc  fix(traceability): run the INDEX/manifest assertions against the tree in a required job (#1071)
```

**#1061 — the predicate becomes the union of write and cite.**
`check_09_manifest_and_evidence_entries` now builds `cited_paths` from
`pr_paths` and `issue_paths_by_number` and raises when an entry's `issue_refs`
names an unlinked Issue **and** this PR either wrote or cited that entry. The
hole closed is measurable: on `main`, a PR that names another session's evidence
document at PR level, writes nothing, and links none of the Issues that document
is attributed to returned `rc=0 AI-SESSION-EVIDENCE: PRESENT`. It now returns
`rc=1` naming the unlinked Issue. The union is necessary in both directions —
write-only admits borrowed evidence, cite-only admits rewriting a historical
entry's `issue_refs` without citing it.

**#1076 — the tautology is replaced by something that can fire.**
`set(linked) != set(ctx.issues)` compared two values derived from the identical
`pr["body"]` string. It is gone, along with the now-unused `linked` binding. The
replacement compares a fact the body carries against a fact `_load_context`
resolved: a non-blank `Related issue(s)` field with an empty `ctx.issues` map
raises. A field that is absent or blank is left to `check_01`, which already
rejects it as a declaration error rather than a resolution error, so the two do
not overlap.

**#1074 — the verdict is bound to the text it judged.**
The workflow gains `types: [opened, synchronize, reopened, edited]`, and a step
after the validator writes `AI-SESSION-EVIDENCE-BODY-SHA256: <64 hex>` into the
job summary under `if: always()`, because a MISSING verdict must be bound to its
text too. The digest is computed by the workflow from the API's `body` field via
`python3 -c` JSON parsing — not by the validator, because the validator runs
from the base revision and a PR must not be able to change its own judging
rules. `jq -r` appends a newline and `jq -j` plus shell substitution strips
trailing newlines, so any `jq`-based one-liner can digest different bytes; the
parsing approach avoids that class of error and the recomputation one-liner is
in a comment. A `null` body digests as
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` — the empty
string, a defined value, because an empty body is a legitimate input that must be
judged. If the body cannot be fetched the step exits non-zero and the job fails;
it never writes a digest it could not compute. The new key deliberately does not
start with `AI-SESSION-EVIDENCE: `, which would be parsed as a verdict.

**#1058 — `REQUIRED_JOB_IDS` membership is pinned.** Only this half was kept:
`main` had already fixed the block-form matcher independently in `a316ff69`
(merged as #1085) with an equivalent pattern, so the incoming block-form code and
its three tests were dropped at the conflict rather than re-landed. The surviving
test deletes the `validate:` block from the workflow text and requires the
checker to name `job id 'validate' is missing`; with `"validate"` removed from
the constant it goes red.

**#1063 — the effective-time literal has a reader.**
`ProductionEffectiveTimeBoundaryTests` parses the literal out of
`.github/workflows/session-evidence.yml` with a regex — the same bare-text
approach the shape guard uses, no YAML dependency — and asserts it equals a
named constant; a second test drives the boundary in both directions and asserts
the verdict flips. `support.py`'s `2099-01-01T00:00:00Z` gains a comment saying
it exists only to construct the "not yet effective" world.

**#1029 — the reverse direction is compared.**
`check_declared_check_contexts.py` gains `--protection` and `--branch`
(defaulting to `main`, so no caller breaks): it reads
`/repos/{repo}/branches/{branch}/protection/required_status_checks`, accepts both
the legacy `contexts` array and the newer `checks: [{context, app_id}]`, and
requires set equality. The comparison is on names, because the Normative
document lists names and no App — the code does not invent an `app_id` for the
declared side, and it reports the payload's `(context, app_id)` pairs so the App
constraint is visible rather than silently ignored. Exit `2` INCOMPLETE on a
transport failure or unreadable payload; `0` never means "could not check".
Without `--protection` the reverse half prints that it was skipped and does not
claim to have verified protection. The stale "§7 declares twelve" claim in
`AID-2026-061/session-evidence-wo01.md` is replaced with a pointer to §7.

**#1071 — the checker runs against the tree.**
`check_traceability.py` gains `--index-manifest-only`, which evaluates the four
INDEX/manifest properties without the registry and reports the requirement checks
as `NOT EVALUATED` in a scoped summary line. The bare run still fails loudly on
the missing registry, so #926 is not regressed. `.github/workflows/repository-hygiene.yml`
gains one step, `python3 scripts/check_traceability.py --index-manifest-only`,
inside the existing `repository-hygiene` job — the one that produces the required
`Repository hygiene (hard gate)` context — with no `|| true`, no
`continue-on-error`, and not inside an `if: always()` block. The registry itself
is not created (#266/OD-23's scope).

**Verification actually run on this branch, at the rebased head `714f2cc`.**

```
python -m unittest discover -s tests/session_evidence -p "test_*.py"
    Ran 98 tests in 0.443s
    OK
```

```
cd scripts && python -m unittest test_check_session_evidence_workflow_shape
    Ran 15 tests in 0.023s
    OK
cd scripts && python -m unittest test_check_declared_check_contexts
    Ran 23 tests in 0.066s
    OK
cd scripts && python -m unittest test_check_traceability
    Ran 41 tests in 7.312s
    OK
```

```
python scripts/ci/check_repository_hygiene.py \
    --base 30c7277e1fc1f08f2b11fa1d3cf4ad80793a4184 --head 714f2cc...
    Work-item index membership version=2026-11-24.8 directories=58 linked=58
    Work-item manifest consistency version=2026-11-24.8 manifests=49 in_scope=47 excluded_by_record_type=2 unrecognized=0 violations=0
    Repository new-file admission passed: 0 new path(s) checked.
```

```
python scripts/ci/check_line_endings.py
    Line-ending check: 1376 files inspected, 0 binary skipped, 0 violations.
python scripts/check_session_evidence_workflow_shape.py
    SESSION EVIDENCE WORKFLOW SHAPE: PASS
python scripts/check_declared_check_contexts.py
    DECLARED CHECK CONTEXTS: PASS
python scripts/check_traceability.py --index-manifest-only
    PASS TRACEABILITY [INDEX/MANIFEST ONLY]: 0 requirements / 49 work items / 0 errors / 58 warnings
```

**Mutations run, one per code fix.**

```
#1061  predicate reverted to `... and entry_written_here`
    FAIL: test_cited_preexisting_entry_still_requires_linking_its_issue
    AssertionError: 0 != 1 : AI-SESSION-EVIDENCE: PRESENT

#1076  new precondition deleted
    Ran 94 tests ... FAILED (failures=1)
    only test_related_field_with_unresolved_issues_raises_the_precondition

#1074  `edited` removed from types:
    FAIL: test_the_repository_trigger_includes_edited
    AssertionError: 'edited' not found in ['opened', 'synchronize', 'reopened']

#1058  "validate" removed from REQUIRED_JOB_IDS
    FAIL: test_deleting_the_validate_job_names_it_as_required
    AssertionError: 0 != 1

#1063  literal changed to 1999-01-01T00:00:00Z
    FAIL: test_workflow_effective_time_matches_the_pinned_policy_boundary
    FAIL: test_verdict_flips_at_the_production_effective_time
    both AssertionError

#1029  reverse comparison reduced to a count comparison
    FAILED (failures=3)   including test_equal_counts_with_different_names_is_a_violation
#1029  whole reverse half skipped (`if False:`)
    FAILED (failures=10, errors=1)

#1071  duplicate-INDEX assertion removed
    FAIL: test_1071_cli_duplicate_index_entry_exits_nonzero (args=()) and (args=('--index-manifest-only',))
    AssertionError: 0 == 0 : PASS TRACEABILITY ...
#1071  manifest identity check replaced with `return True`
    FAIL: test_1071_cli_manifest_identity_mismatch_exits_nonzero (both subTests)
```

Each mutant was restored immediately after it was measured; `git status` was
clean before each commit and at the rebased head.

**Integration conflicts and how they were resolved.**

The seven branches were rebased onto `main` at `30c7277e`. One conflict
occurred, in `check_session_evidence_workflow_shape.py` and its test, because
`main` had independently fixed the block-form half of #1058 in `a316ff69`. It
was resolved by **deletion**: the incoming matcher and its three tests were
dropped, `main`'s line-numbered implementation was kept, and only the
`REQUIRED_JOB_IDS` test survived from the incoming side. Re-landing equivalent
code would have produced two implementations of one rule.

That `main` fixed one half while leaving the other open is itself the finding:
#1058's own Owner ruling at `main = 5bbdc13d84` records four criteria, of which
(a) block form and (d) `ref:` were closed while (b) `REQUIRED_JOB_IDS` and (c)
the effective time were not. Criterion (b) is what this PR pins; (c) is #1063.

**What could not be verified.**

- The reverse protected-context check needs a token that can read branch
  protection, which is admin-scoped. CI runs with `permissions: contents: read`,
  so the workflow invokes the check without `--protection` and the reverse half
  reports itself skipped. It was run once by hand against the live payload and
  returned 16 declared / 16 protected, all `app_id 15368` — recorded, but not
  enforced in CI. Making CI enforce it needs a credential decision that is not
  this Issue's.
- Three workflow steps cannot go green on the Windows host used here and fail
  identically with the changes stashed: `test_bilingual_scripts.py` (9 failures,
  all `/bin/bash: ...check-bilingual-sync.sh: No such file or directory`),
  `test_precheck_delivery.py` (3 errors, `/dev/shm` paths), and
  `status_migration` (needs PyYAML; with it present, 1 pre-existing error in
  `test_sidecar_anchor_detects_silent_tampering`). None touch the changed files.
- The `edited` re-run cannot be observed until this PR exists: the new trigger
  fires on the next body edit of the PR that introduces it, not during its own
  first run.
- Two of the seven Issues (#1058, #1061) were closed by another session before
  this branch was rebased. Both closing rulings state in their own text that a
  criterion remained open or that a measurable difference remained; the commits
  here address exactly those remainders. They are cited as references rather
  than re-closed.

## Amended 2026-11-26 (owner ruling): seven became five, and the record says which

This record was written for a branch carrying seven Issues. By the time that
branch was rebased onto `main dcf9a634`, two of the seven had landed
independently under different commit names, so re-landing them would have
created a second implementation of one rule. They are dropped from the branch
and **this record keeps their analysis** rather than deleting it — the
measurements below were taken and are still true of the commits they describe.

| Issue | Status at the rebase | Where it actually landed |
| --- | --- | --- |
| #1029 | already on `main` | `20adc016` (#1088), plus `a64d1e6b` (#864) |
| #1071 | already on `main` | `8f694edf` (#1090) |
| #1074 (trigger half) | already on `main` | `2733283b` (#1155) |
| #1058 | kept, matcher half dropped | #1085 (`a316ff69`) had fixed the matcher independently |
| #1061, #1063, #1076, #1074 (digest half) | kept | this branch |

So the branch delivers **five** Issues' worth of change, not seven, and the
sections above that describe #1029 and #1071 are a record of work that is
already merged elsewhere — not a claim that this branch contains it. Anyone
checking this PR against the sections above should expect the `#1029` and
`#1071` diffs to be **absent** and should find them on the SHAs named here.

The prompt snapshot this record pins (`9174` bytes, `636ebb9e…`) is unchanged by
the rebase and still matches the manifest's `executed_prompt_sha256`.

