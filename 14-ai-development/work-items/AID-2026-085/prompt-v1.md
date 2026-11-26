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
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count below was re-measured in this session against main 587d7ca9, not copied from issue #925 or from another record."
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

# AID-2026-085 — Make an unwired gate fail instead of merging green

## The brief

Issue #925: a gate-shaped script (`scripts/**/{check,audit,validate,verify}_*.py`)
can be added with no workflow invoking it, and nothing notices.
`scripts/ci/check_test_reachability.py` enforces the symmetric rule for
`test_*.py` files only. The issue asks to extend that same gate, not to write a
second parser.

## The census, re-measured at `main` `587d7ca9`

Gate-shaped scripts: **16**. Unwired by any `.github/workflows/*.yml`: **3**.

| script | bare invocation on main | note |
| --- | --- | --- |
| `scripts/check_source_revision_pointers.py` | **exit 1** — 8 `STALE` pointers | runs and reports; red on main |
| `scripts/check_policy_inheritance.py` | **exit 2** — argparse: `the following arguments are required: --declaration` | cannot be invoked as-is |
| `scripts/governance/status_migration/check_status_gates.py` | **exit 2** — argparse: `the following arguments are required: paths` | cannot be invoked as-is |

**Correction to the assignment and to issue #925.** Both said
`check_source_revision_pointers.py` exits 0 and is "wireable today". It does
not. Measured from a clean detached worktree at `587d7ca9`:

```
SOURCE_POINTER_SCAN
POINTERS=52  ACCURATE=16  STALE=8  UNRESOLVED=0
DEREFERENCED=28  BAD_DEREFERENCE=0  NON_BLOB_REFERENCE=4  BAD=8
STALE docs/en/00-governance/design-principles.md:58 -> declared=9792e189… actual=0a67b5b2…
```

and the same at `dc826e4e` (`BAD=8`). Wiring it as a hard step would redden the
required `repository-hygiene` job on every pull request, so it is **not**
wired. The eight pointers are a `docs/` defect and a different work item.

There is **no** declaration file anywhere in the tree:
`git ls-files | grep -i declaration` is empty.

`check_traceability.py`, which the issue lists as unwired, is now wired:
`repository-hygiene.yml:136` runs `python3 scripts/check_traceability.py
--index-only`. The census above is therefore three, not four.

Measured in the same session: `python3 scripts/ci/check_test_reachability.py`
exits 0 and reports 63 reachable test files (the module's own docstring said 57,
the count at `dc826e4e`; six test files have landed since, and the docstring is
corrected by this change).

## What this work item changes

1. `scripts/ci/check_test_reachability.py` gains the symmetric rule for
   gate-shaped scripts, reusing its existing `os.walk` and its existing reading
   of workflow text. No second parser is written: the module now additionally
   extracts the shell text of every `run:` block, strips shell comments, and
   matches whole tokens.
2. `scripts/ci/baselines/gate-wiring.txt` records the gates that are unwired
   today, with the same doctrine as `scripts/ci/gate_ratchet.py`: a new unwired
   gate fails, and a baselined gate that becomes wired fails until its line is
   removed.
3. All three stay baselined, each with its own stated reason in the file:
   - `check_policy_inheritance.py` and `check_status_gates.py` exit 2 for want
     of an argument, and neither argument exists as an artifact in the tree;
   - `check_source_revision_pointers.py` runs, but exits 1 on main with eight
     `STALE` pointers, so wiring it as a hard step would redden the required job.
     Ratcheting it against a second baseline is the correct shape for a
     red-on-main gate, but it is a separate change: it adds a second ratchet
     step and a second baseline, outside the file scope of this work item.
4. No workflow step is added, removed or edited. The existing
   `repository-hygiene` job is unchanged, so no required status context moves.

## Why extend the existing gate rather than add a second one

The defect and the existing rule are the same question — "is this file executed
by a workflow?" — asked of two filename shapes. A second script would have had
to re-implement `walk()`, `read_workflows()`, the comment handling and the
exit-code vocabulary, and the two answers would drift the first time one of them
learned a new invocation form. The existing module already owns that answer.

## What counts as wired, and what does not

A gate counts as wired only when its repository-relative path or its basename
appears as an argument of a command inside a workflow `run:` block, after shell
comments are stripped. Therefore:

- a reference in a YAML or shell comment does **not** count;
- the gate's own *test* being wired does **not** count — that is precisely the
  #899/#925 confusion, where `tests/test_policy_inheritance.py` runs while
  `scripts/check_policy_inheritance.py` runs nowhere;
- a gate handed to a wrapper as one quoted argument **does** count, because
  quotes are stripped per token (`gate_ratchet.py --command "python3
  scripts/check_bilingual_docs_full.py"`).

Enumeration is the module's existing `os.walk`, not a filename-prefix
exclusion, so a gate under any subdirectory of `scripts/` is found.

## Acceptance criteria

- AC1: a gate referenced only in a comment in a workflow is reported unwired.
- AC2: a gate whose test is wired but whose gate is not is reported unwired.
- AC3: a gate invoked directly in a `run:` block is reported wired.
- AC4: a gate not in the baseline and not wired fails the checker (exit 1) and
  the message names the script.
- AC5: a gate in the baseline and not wired is tolerated (exit 0).
- AC6: an unreadable baseline exits 2, never 0 — `0` must never mean "could not
  check".
- AC7: each of the two rules is mutation-verified: removing the guard makes the
  named test fail with an `AssertionError`, not a traceback.
- AC8: every baselined gate carries its own stated reason in the baseline file,
  and none is deleted.
- AC9: the existing `repository-hygiene` job is byte-identical to `587d7ca9`.

## What this work item does not claim

- It does not claim the three gates measured on main are the final set; it
  claims the census at `587d7ca9`.
- It does not claim the three baselined gates are broken as gates.
  `check_policy_inheritance.py` and `check_status_gates.py` take arguments and
  have no argument artifact; `check_source_revision_pointers.py` runs and
  correctly reports eight stale pointers.
- It does not claim the eight stale pointers were fixed. They were not: that is
  a `docs/` change and a different work item.
- It does not create a new required status context; no workflow file changes.
