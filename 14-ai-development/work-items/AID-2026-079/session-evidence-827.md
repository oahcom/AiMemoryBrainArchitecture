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
      last_verification_note: "The two runs quoted below were executed in this session against the rebased head, and their output is reproduced rather than summarised. The 318 count and the 317 counterfactual were produced by the same command on the same tree."
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

# Session evidence — AID-2026-079

**Role:** TEST_AUTHOR. **Session:** `a1078`, the author session for pull request #1078.
**Base:** `origin/main` = `1f5ba824aa8b2e350a8d70874b0a45720fa4a441`, 2026-11-26.

## Session role / use case

TEST_AUTHOR. This session rebased the existing `test/T92-fault-injection` branch onto
`1f5ba824`, registered `AID-2026-079`, corrected a false premise in the pull request body and
supplied the four required declaration fields. It did not author the four test cases: T92a–T92d
were already written and were already effective. The rebase resolved a textual conflict in
`scripts/test_check_document_management.py` between `575cf3f4` (main's restored guards,
`run_restored_guards()`, T93a–T93h) and this branch (`run_fault_injection()`, T92a–T92d). Both
sides were kept and no assertion was edited.

## Actual AI input

The instruction that produced this record, verbatim in its operative parts:

> Job: finish draft PR #1078 — rebase it, give it a work item, and correct a false claim in
> its body. The tests themselves are already written and I have independently verified they
> are effective. Do not rewrite them.

> The dirty is a one-file textual conflict: main's `575cf3f4 Restore the seven guards removed
> by #1070, with direct-call tests` rewrote the same file after `29eea143`. Resolve by
> rebasing; keep BOTH main's restored guards and the PR's `run_fault_injection()` (called from
> `main()` right after `run_single_entry_callers()`).

> PR body's `Work Item ID` is absent. AID-2026-001..078 are taken on main (highest =
> `AID-2026-078`). **Take `AID-2026-079`**

> Re-run the T92a counterfactual on the rebased tree and confirm it still produces the named
> failure. A test that stopped biting during the rebase is the failure mode this PR exists to
> avoid.

Two further constraints shaped what this record may claim: the tests were not to be
rewritten, and no claim the diff does not support was to be added. Everything below is a
measurement this session ran, not a restatement of the pull request description.

## AI-visible output

Visible to the user, in this session: the conflict resolution in
`scripts/test_check_document_management.py` (both blocks retained, conflict markers removed),
the three files in `14-ai-development/work-items/AID-2026-079/`, one appended row in
`14-ai-development/work-items/INDEX.md`, one rebased commit, and the rewritten pull request
body. The suite result and the counterfactual output below are reproduced from the runs that
produced them.

### 1. Rebase

`git rebase origin/main` from `ade0e2d8` (authored against `29eea143`) onto `1f5ba824`
conflicted once, in `scripts/test_check_document_management.py`. The conflict region held
main's `def run_restored_guards()` (T93a–T93h) against this branch's
`def run_fault_injection()` (T92a–T92d). Resolution: keep both, in that order, delete the
markers. `main()` already contained both call sites after the rebase —
`run_restored_guards()` and, after `run_single_entry_callers()`, `run_fault_injection()`.

The rebased head is `076ed20f736d1024946521a82fffe7caec40d764`. The commit message is
unchanged and the diff is +282 on that single file: the branch's 284 lines plus the two
blank-line removals the conflict resolution made when the blocks were joined.

### 2. Suite, rebased tree

```
318/318 passed
1 skipped, 1 registered of 1 allowed: T68c a real 0o000 directory is reported by path (integration)
```

Exit 0. The count rose from 295 because `575cf3f4` added T93a–T93h to the same file. The
skip set is unchanged: one registered skip, `T68c`, and no unregistered skip.

### 3. T92a counterfactual, rebased tree

The seam under test is the `except OSError: return None` in `git()`
(`scripts/check_document_management.py`). It was neutralised for one run — replaced with a
handler that cannot match, so the `FileNotFoundError` raised by the injected
`subprocess.run` escapes instead of being turned into `None` — and the suite re-run. Output,
verbatim, with the mutation in place:

```
  [FAIL] T92a git() spawn failure is refused by the caller, not raised  exit 2, matching lines [], output "::error::Unable to determine Git history completeness: [Errno 2] No such file or directory: 'git'\n"
317/318 passed
1 skipped, 1 registered of 1 allowed: T68c a real 0o000 directory is reported by path (integration)
```

Exit 1, one failure, and it is the named one. The file was restored from a byte copy taken
before the mutation and `git status` was clean afterwards.

The observed exit code is 2 rather than 1 because removing the `OSError` handler changes
which refusal the gate reaches first: `_git_history_is_shallow()` runs before the changed-path
selection, so the gate reports "Unable to determine Git history completeness" and returns 2.
The assertion still fails, which is the point — the case is bound to the caller's refusal and
not merely to the exit code, and it fails whenever that refusal stops happening.

### 4. What this record does not claim

- It does not claim the tests were written here. They were not; only the rebase and the
  registration are this session's.
- It does not claim any of the four failures occurs naturally in CI. The cases are
  controlled injections of one seam each, and the docstring in `run_fault_injection()` says
  so.
- It does not claim the suite exercises `scripts/check_document_management.py`'s production
  behaviour beyond these four error paths; the T93 guards that the rebase preserved are
  `575cf3f4`'s work, not this work item's.
- It does not claim independent review or an acceptance decision. Both are `NOT_ASSIGNED` in
  the manifest.
- `executed_prompt_provenance` is `NOT_VERIFIED`: the prompt snapshot was written after the
  session from the instruction above, and it has not been re-read line by line against the
  executed turn.
