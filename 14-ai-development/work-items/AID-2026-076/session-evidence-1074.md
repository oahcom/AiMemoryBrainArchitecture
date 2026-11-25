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
      last_verification_note: "Every exit code, message fragment and line number quoted below was produced by running the guard in this detached worktree on 2026-11-25, not read off the source. The three reverts were applied to the guard in isolation and restored; `git diff` for that path against the last restore is empty and the suite and the guard are green."
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

IMPLEMENTER. Issue #1074 reports that `Session Evidence` — a required context —
computes its verdict from `pr.body`, which the author can rewrite after the run,
and that `.github/workflows/session-evidence.yml` did not re-run on `edited`.
This session adds the trigger, adds the shape-guard rule that holds it, and adds
the tests that make reverting either one fail.

This session did not change `scripts/governance/session_evidence/validate.py`.
Reading the body live is correct for a gate that runs on the current state; the
missing trigger is the defect. The body digest the Issue also asks for is a
second change with its own scope and is not done here.

# Actual AI input

**Committed, byte-exact.** `prompt-v1.md` in this directory is the instruction
this change was carried out against, pinned at
`06ee5615ab9fc696afa769183141d637ec5287776b60cc0b06afd117a024f6b2`, 5525 bytes.
The digest was computed from the bytes written to this branch with
`python -c "import hashlib;b=open(path,'rb').read();print(len(b),hashlib.sha256(b).hexdigest())"`,
not composed.

`executed_prompt_provenance` is `NOT_VERIFIED`: the digest proves the committed
file has not changed since it was pinned, not that it is byte-for-byte what the
session read.

**Read before writing:**

| input | what it settled |
|---|---|
| Issue #1074 body and its five comments | the mechanism (live body read, default trigger set), the measured instances (#1054 05:36:07Z success → 05:36:20Z edit → 05:37:29Z merge; 4 of 75 merges), and the fact that the digest half of the closing condition is a separate change |
| `.github/workflows/session-evidence.yml` at `origin/main 30c7277e` | the trigger block (`on:` / `pull_request:` / nothing else), three jobs, no `concurrency:` block |
| `.github/workflows/bilingual-docs.yml:5` | the precedent: `types: [opened, synchronize, reopened, edited, ready_for_review]` already in the same directory |
| `scripts/governance/session_evidence/validate.py:1853` | `body = pr.get("body") or ""` inside `_load_context()`, confirming the verdict is a function of live text |
| `scripts/check_session_evidence_workflow_shape.py` at `origin/main` | the style: `JobBlock`/`StepBlock` NamedTuples carrying `first_line`, regex-over-raw-text parsing, `::error::` lines, `FAIL (N violation(s))`, exit 1 |
| `scripts/test_check_session_evidence_workflow_shape.py` at `origin/main` | the style: throwaway tree per case, `WORKFLOW` fixture string, `run_checker()` returning `(exit code, stderr)` |
| `14-ai-development/work-items/AID-2026-073/` | the registration template: manifest fields, evidence section names, INDEX row layout |

# What was added

**1. The trigger.** `.github/workflows/session-evidence.yml`:

```yaml
on:
  pull_request:
    # The validator reads the PR body live, so an `edited` event must schedule a
    # run or a green verdict outlives the text it judged. The default set
    # (opened, synchronize, reopened) omits `edited`; list all four explicitly
    # so the behaviour is stated rather than inherited.
    types: [opened, synchronize, reopened, edited]
```

The full default set is written out rather than writing `types: [edited]` plus
relying on inherited defaults, because an explicit list is the thing the guard
can read and a future default change cannot silently alter it.

**2. The guard rule.** `scripts/check_session_evidence_workflow_shape.py` gains
a fourth property and the parsing it needs:

- `ON_KEY_RE`, `PULL_REQUEST_RE`, `TYPES_FLOW_RE`, `TYPES_BLOCK_RE`,
  `TYPES_ITEM_RE` — the trigger block is located by indentation, the same
  technique the file already uses for jobs and steps.
- `TriggerBlock(text, first_line)` — the `pull_request:` block and the line of
  its key.
- `TypesDecl(values, line)` — the parsed `types:` entries and the line of the
  `types:` key, so the message can quote it.
- `trigger_block(text)` — None when no `on:` block is readable.
- `types_decl(block)` — both spellings, one return shape.
- `_trigger_violations(text)` — three messages: no readable `pull_request:`
  trigger; no `types:` key (names the default set that omits `edited`); `types:`
  present without `edited` (names the line).
- `main()` reads the file once into `text`, keeps the `jobs:` INCOMPLETE branch
  unchanged, and returns `violations(blocks) + _trigger_violations(text)`.

The INCOMPLETE semantics are untouched: a missing `jobs:` mapping is still exit
2. A missing trigger is exit 1, because a workflow with `jobs:` but no readable
`pull_request:` trigger is a workflow the guard can read and finds wrong, not one
it cannot read.

**3. The tests.** Four added to the existing class, following its helpers:

1. `test_trigger_without_edited_is_a_violation_naming_edited_and_its_line`
2. `test_trigger_with_edited_in_flow_form_passes`
3. `test_trigger_with_edited_in_block_form_passes`
4. `test_trigger_without_a_types_key_is_a_violation`

The `WORKFLOW` fixture gained the `types:` line, because the fixture is a claim
about this tree and the guard now holds this tree to that line. Two pre-existing
tests (`test_pass_on_the_three_job_shape`,
`test_ref_in_the_base_job_is_allowed`) asserted exit 0 on the fixture and would
otherwise have failed for a reason unrelated to what they test; their assertions
are unchanged.

# Reverse-verification

Each rule was reverted in isolation in this worktree, the suite run, the result
captured, and the guard restored. The guard was copied to
`C:/tmp/opencode/_w1088_guard.bak` before the first revert and restored from it
after the last.

**Revert 1 — the rule disabled: `_trigger_violations` returns `[]`.**

```
def _trigger_violations(text: str) -> list[str]:
    """MUTANT: rule disabled."""
    return []
    block = trigger_block(text)
```

```
$ cd scripts && python -m unittest discover -s . -p "test_check_session_evidence_workflow_shape.py"
...FF..
FAIL: test_trigger_without_a_types_key_is_a_violation
    self.assertEqual(code, 1)
AssertionError: 0 != 1
FAIL: test_trigger_without_edited_is_a_violation_naming_edited_and_its_line
    self.assertEqual(code, 1)
AssertionError: 0 != 1
Ran 16 tests in 0.026s
FAILED (failures=2)
```

**Revert 2 — block form disabled: `if False and TYPES_BLOCK_RE.match(line)`.**

```
$ cd scripts && python -m unittest discover -s . -p "test_check_session_evidence_workflow_shape.py"
.F.....
FAIL: test_trigger_with_edited_in_block_form_passes
    self.assertEqual(code, 0)
AssertionError: 1 != 0
Ran 16 tests in 0.023s
FAILED (failures=1)
```

This is the anti-regression case for #1045's bug class: a guard that reads only
the flow form rejects a correct file, and this test is what says so.

**Revert 3 — flow form disabled: `if False and flow`.**

```
$ cd scripts && python -m unittest discover -s . -p "test_check_session_evidence_workflow_shape.py"
FAIL: test_the_repository_itself_passes
    self.assertEqual(checker.main(REPO), 0)
AssertionError: 1 != 0
FAIL: test_trigger_with_edited_in_flow_form_passes
    self.assertEqual(code, 0)
AssertionError: 1 != 0
FAIL: test_trigger_without_edited_is_a_violation_naming_edited_and_its_line
    self.assertIn(f"(line {types_line}:", message)
AssertionError: '(line 4:' not found in "::error::the `pull_request:` trigger declares no `types:` key in .github/workflows/session-evidence.yml (trigger at line 3); ..."
Ran 16 tests in 0.030s
FAILED (failures=5)
```

All failures above are `AssertionError`. None is a traceback and none is an
`ImportError`.

**Restored:**

```
$ cd scripts && python -m unittest discover -s . -p "test_check_session_evidence_workflow_shape.py"
Ran 16 tests in 0.032s
OK
$ cd .. && python scripts/check_session_evidence_workflow_shape.py
::notice::.github/workflows/session-evidence.yml has the three independent jobs self-test-trusted-base, self-test-pr-head, validate; the head job carries no `ref:`, the verdict job carries no `needs:`, and the `pull_request:` trigger declares `edited`
SESSION EVIDENCE WORKFLOW SHAPE: PASS
GUARD_EXIT=0
```

# AI-visible output

```
.github/workflows/session-evidence.yml              +5 lines: the types: list and its comment
scripts/check_session_evidence_workflow_shape.py    +4th property: trigger parsing, three messages
scripts/test_check_session_evidence_workflow_shape.py  +4 tests, 12 existing untouched
14-ai-development/work-items/AID-2026-076/          manifest, prompt, this record
14-ai-development/work-items/INDEX.md               one row
```

Guard exit code on the unmutated repository: **0** (`GUARD_EXIT=0`).
Suite: **16 tests, OK** (12 pre-existing + 4 new).

# Limitations

1. **This narrows the race; it does not close it.** `edited` guarantees that a
   body edit schedules a run, so a green verdict no longer survives an edit
   *without* a re-run. An edit that lands after the last run completes and
   before the merge still races the merge, and a `success` computed on the
   earlier text can still be the required context that authorises it. Closing
   that needs a merge queue, a verdict bound to something immutable (the
   commit), or an `if:` guard comparing the body hash. Issue #1074 asks for a
   body digest as the second, independent half; that is not done here, so #1074
   stays open.
2. **No `concurrency:` block exists and none was added.** Two runs on the same
   PR therefore serialise rather than cancel each other. Whether `edited`
   should join a cancellation group is a real decision — a stale run cancelled
   by a newer one is the correct outcome, but it changes what "the required
   context" means — and it is not taken here.
3. **The guard reads indentation, not YAML.** A `types:` key written inside a
   block scalar at exactly four spaces would be read as the trigger's. The
   trigger block is the first thing in this file and contains no scalars, so
   this tree is safe; the same limitation, with the same upgrade path, is
   already documented at the top of the guard for `ref:` and `needs:`.
4. **The message says `edited` and quotes the line; it does not check the order
   or completeness of the list.** `types: [edited]` alone would pass, dropping
   `opened`/`synchronize`/`reopened` and thereby *reducing* coverage. That is a
   real gap in the rule, stated rather than implied: the guard enforces presence
   of `edited`, not the full default set.
5. **No independent review is claimed.** The three reverts are reproducible from
   the commands and output above, which is why they are written out rather than
   summarised.
