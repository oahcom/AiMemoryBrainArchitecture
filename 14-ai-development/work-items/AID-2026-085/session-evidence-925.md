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
      last_verification_note: "Every count, exit code and mutation transcript below was produced by a command run in this worktree, based on origin/main 587d7ca9, on 2026-11-26."
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

# Session evidence — AID-2026-085

## Session role

IMPLEMENTER. This session re-measured the census in issue #925, extended
`scripts/ci/check_test_reachability.py` with the symmetric rule for gate-shaped
scripts, added the `scripts/ci/baselines/gate-wiring.txt` baseline, and
mutation-verified both rules. It did not wire any gate: the one the assignment
named as wireable exits 1 on main, so wiring it would have reddened a required
job. No workflow file changed and no gate was deleted.

## Actual AI input

The assignment that produced this change, abridged only where it repeated
repository context:

> A gate-shaped script (`scripts/**/{check,audit,validate,verify}_*.py`) can be
> added with no workflow invoking it, and nothing notices.
> `scripts/ci/check_test_reachability.py` enforces the symmetric rule for
> `test_*.py` files only. Issue #925 asks to extend that same gate, not to write
> a second parser.
>
> Extend `scripts/ci/check_test_reachability.py` ... reusing its existing
> machinery: it already parses workflow text, expands `-p` globs and matches two
> invocation forms. Do not write a second workflow parser. A gate counts as
> wired only when its path (or basename) appears as an argument to an executed
> command in a workflow `run:` block — a reference inside a comment must not
> count, and neither must the gate's own *test* being wired.
>
> Baseline the currently-unwired set in `scripts/ci/baselines/gate-wiring.txt`,
> one repository-relative path per line, consumed ... the same way
> `scripts/ci/baselines/bilingual-docs.txt` is. Read that baseline and its
> consumer first and copy the mechanism; do not invent a second one. A *new*
> unwired gate must fail immediately.
>
> Wire `scripts/check_source_revision_pointers.py` into `repository-hygiene.yml`
> as a new step inside the existing repository-hygiene job (so no new required
> status context is created), then remove it from the baseline. ...
>
> Do **not** wire `check_policy_inheritance.py` or `check_status_gates.py` ...
> Do not delete them either ... Leave them in the baseline and say in the PR
> exactly why each stays.
>
> Mutation verification, mandatory: for each of the two rules ... remove the
> guard and confirm the **named** test fails with an `AssertionError`, not a
> traceback. Record the verbatim output.

## AI-visible output

The diff to `scripts/ci/check_test_reachability.py`,
`scripts/ci/test_check_test_reachability.py` and
`scripts/ci/baselines/gate-wiring.txt`; the three files in this directory; one
row inserted into `14-ai-development/work-items/INDEX.md`; and the pull request
that carries them. No workflow file is in the diff.

## 1. The census, re-measured rather than repeated

At `origin/main` `587d7ca9`:

```
gate-shaped scripts under scripts/   16
unwired by any .github/workflows/*.yml   3
```

Bare invocation of each of the three, run from clean detached worktrees:

```
scripts/check_source_revision_pointers.py
  SOURCE_POINTER_SCAN
  POINTERS=52  ACCURATE=16  STALE=8  UNRESOLVED=0
  DEREFERENCED=28  BAD_DEREFERENCE=0  NON_BLOB_REFERENCE=4  BAD=8
  STALE docs/en/00-governance/design-principles.md:58 -> declared=9792e189… actual=0a67b5b2…
  exit 1
scripts/check_policy_inheritance.py
  usage: check_policy_inheritance.py [-h] [--repo REPO] --declaration DECLARATION
  check_policy_inheritance.py: error: the following arguments are required: --declaration
  exit 2
scripts/governance/status_migration/check_status_gates.py
  usage: check_status_gates.py [-h] paths [paths ...]
  check_status_gates.py: error: the following arguments are required: paths
  exit 2
```

`git ls-files | grep -i declaration` prints nothing.

### The measurement the assignment got wrong

The assignment, and issue #925's proposal item 3, both said
`check_source_revision_pointers.py` exits 0 and is "wireable today". It exits
**1**. Verified three ways: a clean detached worktree at `587d7ca9`, a clean
detached worktree at `dc826e4e` (also `BAD=8`), and by hand on one case —
`docs/en/00-governance/design-principles.md:58` declares
`9792e189d63fbbc3694ab891fc4aeba5143b3b1c` while
`git rev-parse HEAD:00-governance/design-principles.md` is
`0a67b5b2b4acb22faa0b3dec38d23c771f88b821`.

My first census loop was `python3 "$f" 2>&1 | tail -5; echo "exit=$?"`, which
reports `tail`'s exit code rather than the gate's. That is where the 0 came
from. Every exit code in this record was taken from a command that did not sit
at the end of a pipeline.

Consequence: wiring it as a hard step in `repository-hygiene` would redden a
required job on every pull request. It is not wired. The eight stale pointers
are a `docs/` defect and a different work item.

`check_traceability.py`, which the issue lists as unwired, is wired:
`repository-hygiene.yml:136` runs `python3 scripts/check_traceability.py
--index-only`. The live set is therefore three, not the issue's four.

## 2. What counts as wired

`run_blocks()` reads each workflow as text, finds every `run:` key (inline or
`|`/`>` block), and strips shell comments with quote awareness. `gate_wiring()`
splits each block into tokens on whitespace and shell metacharacters, strips
per-token quotes, and reports a gate wired when its repository-relative path or
its basename is one of those tokens.

That makes three things non-matches by construction:

- a gate named in a YAML or shell comment — comments are removed first;
- `tests/test_policy_inheritance.py` when the gate is
  `scripts/check_policy_inheritance.py` — the token is a different string;
- `scripts/check_policy_inheritance.py.bak` — tokens are compared whole.

And one thing a match: `--command "python3
scripts/check_bilingual_docs_full.py"` passed to `gate_ratchet.py`, because the
quotes are stripped per token.

Enumeration is the module's existing `os.walk` with the existing `.git`
exclusion; there is no filename-prefix exclusion. A gate under
`scripts/governance/status_migration/` is found, which is asserted by
`test_gate_under_a_sibling_directory_is_still_found`.

## 3. The baseline, and why it is not a green exemption

`scripts/ci/baselines/gate-wiring.txt`:

```
scripts/check_policy_inheritance.py
scripts/check_source_revision_pointers.py
scripts/governance/status_migration/check_status_gates.py
```

each preceded by a comment naming its measured exit code and the reason it
stays. The file is consumed the way `bilingual-docs.txt` is consumed by
`gate_ratchet.py`: exact set, both directions. A new unwired gate is a
regression and fails. A baselined gate that becomes wired is a stale baseline
and also fails, so the exemption cannot outlive its reason. The
`test_baseline_entry_that_became_wired_is_stale` case pins that second
direction.

The reason each one stays, as written in the file:

- `check_policy_inheritance.py` — exits 2, needs `--declaration`, and there is
  no declaration file in the tree.
- `check_source_revision_pointers.py` — exits 1 with 8 STALE pointers, so a
  hard step would redden the required job. Ratcheting it against a second
  baseline is the right shape and is a separate change.
- `check_status_gates.py` — exits 2, needs `paths`, and no path set is declared.

## 4. Why no gate was wired

The assignment's deliverable 3 was "wire `check_source_revision_pointers.py`,
remove it from the baseline; it exits 0 so this cannot redden the board". The
premise is false, so the action was not taken and the gate stays baselined with
its reason written down. The alternative — wire it under `gate_ratchet.py` with
a `scripts/ci/baselines/source-revision-pointers.txt` holding the eight STALE
items — is the repository's sanctioned shape for a red-on-main gate, but it adds
a second ratchet step and a second baseline, which is outside this work item's
file scope. It is recorded here as the follow-up rather than done silently.

Net effect on CI: no workflow file changes at all, so no required status context
moves and no job gets a new failure mode. What changes is that the next
gate-shaped script with no workflow will fail `check_test_reachability.py`.

## 5. Tests, and the mutation transcripts

Suite size after this change: 24 tests, all passing.

```
$ python3 scripts/ci/test_check_test_reachability.py
Ran 24 tests in 3.121s
OK
```

Nine cases were added: comment-only reference, test-wired-gate-not-wired,
direct `run:` invocation, block-scalar invocation by basename, new unwired gate,
baselined unwired gate, stale baseline, unreadable baseline, and a gate under a
sibling directory.

The stale-baseline case asserts both halves: a baselined gate that *is* wired
must exit 1 naming the path, and it goes green only after the baseline line is
removed. `gate_ratchet.py` documents that direction; this test confirms the
implementation rather than the docstring.

### Mutation 1 — the wiring rule

Guard replaced with `wired[relative] = True`:

```
$ python3 scripts/ci/test_check_test_reachability.py ReachabilityTest.test_gate_referenced_only_in_a_comment_is_unwired
test_gate_referenced_only_in_a_comment_is_unwired (__main__.ReachabilityTest.test_gate_referenced_only_in_a_comment_is_unwired) ... FAIL

======================================================================
FAIL: test_gate_referenced_only_in_a_comment_is_unwired (__main__.ReachabilityTest.test_gate_referenced_only_in_a_comment_is_unwired)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\tmp\opencode\w925\scripts\ci\test_check_test_reachability.py", line 207, in test_gate_referenced_only_in_a_comment_is_unwired
    self.assertEqual(code, 1, out + err)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : Test reachability: 0 test files, 0 reachable, 0 unreachable
Gate wiring: 1 gate scripts, 0 unwired, 0 baselined

----------------------------------------------------------------------
Ran 1 test in 0.146s

FAILED (failures=1)
```

### Mutation 1b — the comment stripping inside the wiring rule

Guard replaced with `blocks.append(rest)` (comments no longer stripped):

```
$ python3 scripts/ci/test_check_test_reachability.py ReachabilityTest.test_gate_referenced_only_in_a_comment_is_unwired
FAIL: test_gate_referenced_only_in_a_comment_is_unwired (__main__.ReachabilityTest.test_gate_referenced_only_in_a_comment_is_unwired)
  File "C:\tmp\opencode\w925\scripts\ci\test_check_test_reachability.py", line 207, in test_gate_referenced_only_in_a_comment_is_unwired
    self.assertEqual(code, 1, out + err)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : Test reachability: 0 test files, 0 reachable, 0 unreachable
Gate wiring: 1 gate scripts, 0 unwired, 0 baselined

Ran 1 test in 0.146s

FAILED (failures=1)
```

### Mutation 2 — the baseline exemption

Guard replaced with `new_unwired = list(unwired)`:

```
$ python3 scripts/ci/test_check_test_reachability.py ReachabilityTest.test_baselined_unwired_gate_is_tolerated
FAIL: test_baselined_unwired_gate_is_tolerated (__main__.ReachabilityTest.test_baselined_unwired_gate_is_tolerated)
  File "C:\tmp\opencode\w925\scripts\ci\test_check_test_reachability.py", line 256, in test_baselined_unwired_gate_is_tolerated
    self.assertEqual(code, 0, out + err)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : scripts/check_thing.py
::error::Gate wiring: 1 gate-shaped script(s) are executed by no workflow and are not in scripts/ci/baselines/gate-wiring.txt. Wire them, or the next one arrives silently (#925).

Ran 1 test in 0.115s

FAILED (failures=1)
```

All four mutations fail with `AssertionError`, not a traceback. Restoring each
guard returns `Ran 24 tests`, `OK`, exit 0.

### Mutation 3 — the stale-baseline direction

`stale = sorted(baseline - set(unwired))` replaced with `stale = []`:

```
$ python3 scripts/ci/test_check_test_reachability.py ReachabilityTest.test_baseline_entry_that_became_wired_is_stale
test_baseline_entry_that_became_wired_is_stale (__main__.ReachabilityTest.test_baseline_entry_that_became_wired_is_stale) ... FAIL

======================================================================
FAIL: test_baseline_entry_that_became_wired_is_stale (__main__.ReachabilityTest.test_baseline_entry_that_became_wired_is_stale)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\tmp\opencode\w925\scripts\ci\test_check_test_reachability.py", line 264, in test_baseline_entry_that_became_wired_is_stale
    self.assertEqual(code, 1, out + err)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : Test reachability: 0 test files, 0 reachable, 0 unreachable
Gate wiring: 1 gate scripts, 0 unwired, 1 baselined

----------------------------------------------------------------------
Ran 1 test in 0.160s

FAILED (failures=1)
```

Restored, `Ran 24 tests`, `OK`, exit 0.

## 6. Gate exit codes on the committed tree

```
python3 scripts/ci/test_check_test_reachability.py   0   24 tests OK
python3 scripts/ci/check_test_reachability.py        0   "63 test files, 63 reachable, 0 unreachable"
                                                         "16 gate scripts, 3 unwired, 3 baselined"
python3 scripts/ci/check_repository_hygiene.py       0
python3 scripts/check_traceability.py --index-only   0
python3 scripts/ci/check_manifest_parse.py           0   68 manifests found, 68 parsed
```

`git diff 587d7ca9 --stat -- .github/` is empty: no workflow file changed.

## 7. What this record does not claim

- It does not claim the three baselined gates are broken. Two take arguments and
  have no argument artifact; the third runs and correctly reports eight stale
  pointers.
- It does not claim the eight stale pointers were fixed. They were not.
- It does not claim the census is stable. It is the measurement at `587d7ca9`.
- It does not claim independent review. This record was written by the session
  that made the change.
- `executed_prompt_provenance` is `NOT_VERIFIED`: the prompt was written from
  the same measurements as this record but was not re-read line by line against
  the final diff.
