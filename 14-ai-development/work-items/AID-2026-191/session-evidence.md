---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-191/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the dispatched task and what the implementing session did with it; the session identifier and the verbatim model input stream were not captured."
    usage_status: Active
    modification_status: Modified
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
    canonical_scope_keywords:
      - "gate"
      - "hygiene"
      - "silent-skip"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session Evidence — AID-2026-191

## Session role / use case

Repair worker for one gate defect. The assistant was spawned by a dispatching session and given
two brief files and one worktree: fix the repository-hygiene gate reporting a pass for new-file
admission that it had silently skipped when `--base` and `--head` were absent, and ship it as a
registered work item through a pull request.

## Actual AI input

The dispatching session supplied, in order:

- two brief files, `fix-brief-common.md` (batch-wide: worktree discipline, credential handling,
  number allocation, work-item structure, block-style metadata, PR body fields, merge discipline)
  and `unit-hygiene.md` (this unit: the defect, the four things to do, two prohibitions);
- the worktree `D:\code\wt-hygiene` on branch `fix/2026-11-27-hygiene-silent-skip`, and the
  instruction to work only inside it;
- the defect as measured by the dispatcher: `check_repository_hygiene.py:968-979` skips new-file
  admission without `--base/--head` and prints the same `Repository hygiene check passed` line,
  and `.github/workflows/repository-hygiene.yml` invokes that script twice, once without the pair;
- a choice to be made with a stated reason: refuse the unqualified run in the script, or supply
  the range in CI;
- two prohibitions: do not change the decision logic taken when `--base` and `--head` are both
  present; do not add a required context.

The model serving this unit was `opencode-go/deepseek-v4.1-flash` because both 9router routes were
returning 429. That substitution changes which model produced the edits, not what was asked for.

## What the session did

1. Read the briefs, then the worktree: `git fetch origin main` and `git merge --no-ff origin/main`
   reported "Already up to date" at `4326669c`, and `git status --short` was empty. Nothing from an
   earlier attempt was present to preserve or discard.
2. Read the defect at the source rather than at the line numbers given: `main()` ran the denylist,
   INDEX-membership and manifest-consistency checks, then fell through to
   `print("Repository hygiene check passed ...")` when no range was supplied, and
   `repository-hygiene.yml` had both an unqualified step and a ranged step.
3. Counted the callers before choosing. `git grep` found one unqualified invocation in the tree
   (the workflow step) and 27 in the test module. That count is what decided the question the
   brief left open: supplying the range in CI repairs one caller and leaves 27 others able to
   print a pass for admission that never ran, so the refusal belongs in the script.
4. Implemented the refusal, kept the head-tree half behind an explicit `--head-tree-only` flag so
   the capability was not deleted to punish a message, bumped `CHECK_VERSION` so an old silent-skip
   PASS cannot be confused with a new one, collapsed the workflow's duplicated invocation to one
   step carrying the range, and updated the 27 call sites plus four new tests.
5. Ran the script both ways and the suite, then registered this work item and one INDEX row.

## AI-visible output

The assistant reported, and the head of this branch confirms:

- `python scripts/ci/check_repository_hygiene.py` with no arguments prints
  `Repository new-file admission SKIPPED (new-file admission requires --base and --head).` plus
  `::error::repository hygiene cannot be determined: new-file admission requires --base and
  --head`, and exits 2. Before the change the same invocation printed
  `Repository hygiene check passed (version=2026-11-24.8).` and exited 0.
- the same script with `--base 4326669c... --head 4326669c...` prints
  `Repository new-file admission version=2026-11-27.1 ...` and
  `Repository new-file admission passed: 0 new path(s) checked.` and exits 0;
- the same script with `--head-tree-only` prints
  `Repository hygiene head-tree checks complete (version=2026-11-27.1). New-file admission SKIPPED
  (new-file admission requires --base and --head).` and exits 0;
- `python scripts/test_check_repository_hygiene.py` ran 101 tests, `OK (skipped=1)`, exit 0, where
  the base revision ran 97;
- a YAML parse of both revisions of `repository-hygiene.yml` shows the same single job
  `repository-hygiene` with the same display name `Repository hygiene (hard gate)`, and steps
  18 → 17 with the two script invocations collapsed to one;
- no admission rule, allowlist entry, prohibited path, job name, required context or branch
  protection entry was changed.

This unit was served by `opencode-go/deepseek-v4.1-flash` after both 9router routes returned 429;
the substitution changes which model produced the text, not what was asked for.

## Attribution and independence

- Attribution: user-authorized operator, delegated by the account owner.
- Independent review: NOT_ASSIGNED. No APPROVE, acceptance or natural-person signature is
  represented by this file or by the PR.
- The session that wrote these files is the session that describes them; that is disclosure, not
  independence.
