# GOV-NC-2026-11-22-ENUM-BOUNDARY-021 — Bilingual Gate Enumeration Boundary and Baseline Write Protection

- Registration ID: GOV-NC-2026-11-22-ENUM-BOUNDARY-021
- Date: 2026-11-22
- Category: Engineering Governance / CI Gate Integrity
- Status: OPEN — Awaiting implementation and independent verification
- Affected component: `scripts/check_bilingual_docs.py`
- Related registration: GOV-NC-2026-11-22-REPO-ROOT-014
- Scope: Gate enumeration boundary, frozen-baseline write protection, and repository-root consistency
- Prohibited scope: `crates/`, existing frozen-baseline entries, and existing pull requests

## 1. Overview

This registration records two independent defects in the bilingual
documentation gate that jointly affect CI trustworthiness.

First, `current_bilingual_gaps()` enumerates files recursively from the
filesystem rather than from Git's tracked-file set. Cached files, temporary
files, and untracked Markdown files, including files ignored by `.gitignore`,
may therefore be incorrectly classified as normative documentation gaps.

Second, `write_baseline()` does not validate the working-tree state before
writing. Phantom paths produced by untracked files may be permanently added
to the frozen baseline. Since the baseline policy prohibits adding entries,
such contamination cannot be automatically repaired by an ordinary run.

The two defects affect enumeration correctness and the recoverability of
governed state, respectively.

## 2. Defect One: Incorrect Enumeration Boundary

### 2.1 Original implementation

The original implementation is:

    for root_name in sorted(NORMATIVE_ROOTS):
        root = REPO_ROOT / root_name
        for path in sorted(root.rglob("*.md")):
            source = path.relative_to(REPO_ROOT).as_posix()

`Path.rglob()` enumerates files on disk without distinguishing:

- Git-tracked files;
- untracked files;
- files ignored by `.gitignore`;
- test caches;
- temporary files.

Consequently, the set actually checked by the gate is not equivalent to the
repository's version-controlled documentation set.

### 2.2 Controlled experiment — verbatim evidence

The following was executed in a clean detached checkout:

    $ printf '# probe\n' > 06-memory-context/_probe-untracked.md
    $ BASE_SHA=$HEAD_SHA=origin/main python scripts/check_bilingual_docs.py
    ::error::New bilingual gap outside frozen baseline: 06-memory-context/_probe-untracked.md
    EXIT=2

Then:

    $ git ls-files --error-unmatch 06-memory-context/_probe-untracked.md
    error: pathspec ... did not match any file(s) known to git

This demonstrates that the gate incorrectly classified a file outside the
Git-tracked set as a new bilingual gap.

### 2.3 Actual impact already observed

The following two ignored cache files:

- `08-bmcp-protocol/.pytest_cache/README.md`
- `08-bmcp-protocol/tests/conformance/.pytest_cache/README.md`

cause the main working-tree check to return `EXIT=2`.

A clean checkout of the same commit instead produces:

    PASS / 77 frozen / 0 new gaps

A single commit therefore produces a red result locally and a green result
in a clean checkout. This shows that additional working-tree files
contaminate the gate and prevent stable CI decisions.

### 2.4 Governance ruling

`current_bilingual_gaps()` MUST obtain Markdown paths exclusively from the
Git-tracked set.

`git ls-files` is the sole enumeration source, and the command MUST execute
with the repository root as its working directory.

Paths MUST use repository-relative POSIX form and MUST exactly match the
existing `source` identifier representation.

The following MUST NOT enter the gap set:

- untracked files;
- ignored files;
- pytest caches;
- temporary files;
- any other on-disk file outside the Git-tracked set.

If Git cannot be executed, the repository cannot be identified, the command
fails, or its output cannot be parsed reliably, the gate MUST fail closed.
It MUST NOT fall back to `rglob()` or interpret an execution failure as
zero gaps.

Tracked Markdown files MUST continue to undergo the existing full bilingual
checks. This repair MUST NOT weaken normative strictness.

## 3. Defect Two: Missing Frozen-Baseline Write Protection

### 3.1 Original implementation

The original implementation is:

    def write_baseline() -> int:
        gaps = sorted(current_bilingual_gaps())
        header = (...)
        BASELINE_PATH.write_text(
            header + "\n".join(gaps) + "\n",
            encoding="utf-8",
        )

The function does not check whether the working tree is clean.

### 3.2 Risk

The frozen baseline carries the following governance constraint:

    # This baseline may only shrink; entries must never be added.

If an untracked Markdown file exists in a dirty working tree, the original
filesystem enumeration may write it into the frozen baseline.

Once written, the phantom path becomes a permanently frozen entry and will
not be automatically removed by ordinary checks.

This converts temporary working-tree state into long-lived governance state.

### 3.3 Governance ruling

Before any baseline write operation, `write_baseline()` MUST execute:

    git status --porcelain --untracked-files=all

Writing MUST be rejected in any of the following cases:

- a tracked file has been modified;
- a tracked file has been deleted;
- an untracked file exists;
- the Git status command fails.

On rejection, the function MUST:

1. Return a non-zero status.
2. Emit an explicit error message.
3. Leave every byte of the original baseline unchanged.
4. Leave no partially written file.

Normal writes MUST use a temporary file in the same directory and an atomic
replacement through `os.replace()`.

The status check MUST complete before content generation, and replacement
MUST occur only after the complete new content has been written. On failure,
the temporary file MUST be cleaned up and the original file preserved.

## 4. Relationship to GOV-NC-2026-11-22-REPO-ROOT-014

This registration is related to 014, but the problem definitions remain
distinct.

### 014: Repository-root resolution

014 addresses:

    REPO_ROOT versus Path.cwd()

That is, when the script is invoked from outside the repository, the
caller's current working directory MUST NOT be mistaken for the repository
root.

Its core issue is an incorrect path-resolution anchor.

### 021: Enumeration boundary and baseline write protection

021 addresses:

1. `Path.rglob()` enumerating the filesystem rather than the Git-tracked set;
2. `write_baseline()` lacking a dirty-tree rejection mechanism.

Its core issues are an incorrect definition of the file set and missing
preconditions for writing frozen governance state.

This repair MUST also ensure that relevant Git operations, file resolution,
and baseline operations consistently use `REPO_ROOT` as their anchor,
including an integration regression test with 014.

021 does not replace 014 and does not reclassify the historical 014 issue
as completed.

## 5. Implementation Requirements

### 5.1 Repair commit

Implementation MUST use a new, independent branch and a new pull request.

The implementation commit MUST contain only:

- `scripts/check_bilingual_docs.py`;
- the Chinese source of this registration;
- its byte-identical Chinese mirror;
- its English translation mirror.

Neither `crates/` nor the frozen baseline may be modified.

The final PR head SHA and merge SHA MUST be recorded in the acceptance
evidence. They MUST NOT be fabricated in advance.

### 5.2 Enumeration implementation

- Use `git ls-files`.
- Accept only tracked `.md` paths under normative roots.
- Use repository-relative POSIX paths for comparisons.
- Fail closed when Git commands fail.
- Do not fall back to filesystem recursion.

### 5.3 Baseline write protection

- First check `git status --porcelain --untracked-files=all`.
- Reject any non-empty output.
- Reject command failures.
- Use a temporary file in the same directory.
- Use `os.replace()` for atomic replacement.
- Clean up the temporary file on failure.

### 5.4 Invariants

The following existing semantics MUST remain unchanged:

- `_require_full_git_history()` remains before baseline/path checks in the normal entry point;
- `check_normative_pairing()` is unchanged;
- `check_side_by_side_catch_up()` is unchanged;
- `BILINGUAL-MANIFEST: COMPLETE` evaluation is unchanged;
- `PARTIAL_SIDE_BY_SIDE_PAIRS` is unchanged;
- `PR_BODY` continues to be read through `os.environ.get("PR_BODY", "")`;
- bilingual requirements for tracked documents are not weakened;
- `scripts/bilingual-baseline.txt` is not modified.

## 6. Mandatory Test Checklist

### T01: Untracked Markdown

Create an untracked `.md` file under a normative directory.

Expected:

- It does not enter `current_bilingual_gaps()`.
- It does not produce a New bilingual gap.
- The working tree is clean again after the experimental file is removed.

### T02: pytest caches

Create or retain:

    08-bmcp-protocol/.pytest_cache/README.md
    08-bmcp-protocol/tests/conformance/.pytest_cache/README.md

Expected: neither file enters the gap set.

### T03: Ignored Markdown

Create a Markdown file matching `.gitignore`.

Expected: it does not enter the gap set.

### T04: Tracked Markdown

Create:

    06-memory-context/_probe-tracked.md

Run `git add` so that it becomes tracked, then run the gate.

Expected:

- The file enters the gap set.
- The gate still reports a new gap when bilingual mirrors are missing.
- The exit code is 2.

This is the mandatory regression lock preventing accidental relaxation
of the gate.

### T05: Dirty-tree baseline rejection

Save the original baseline bytes and its SHA-256.

Create an untracked file and run:

    python scripts/check_bilingual_docs.py --write-baseline

Expected:

- Non-zero exit status.
- Explicit rejection reason.
- Original baseline bytes remain exactly unchanged.
- No temporary file is left behind.

### T06: Clean-tree baseline write

Run in a clean detached worktree:

    python scripts/check_bilingual_docs.py --write-baseline

Expected: successful completion, with generated content matching the
current gap set derived from tracked files.

### T07: External working directory

Invoke the script from a directory outside the repository.

Expected:

- `REPO_ROOT` is used to locate the repository.
- Git commands execute successfully.
- The baseline is resolved under the correct repository.
- The result is independent of the external `Path.cwd()`.

### T08: Frozen-baseline invariance

In a clean detached checkout, set:

    BASE_SHA=HEAD_SHA=origin/main

The result MUST remain exactly:

    bilingual baseline: 77 frozen, 0 new gaps
    exemptions: 21
    Bilingual documentation and prompt-library gate: PASS
    EXIT=0

None of the 77 existing entries may be added or removed.

### T09: Changed-path semantics

Verify:

- The changed-path set is unchanged.
- Side-by-side catch-up behavior is unchanged.
- COMPLETE manifest behavior is unchanged.
- The PR_BODY reading channel is unchanged.
- Shallow-history interception still precedes baseline/path checks.

## 7. Minimal Reproduction Procedure

1. Obtain a clean detached worktree.
2. Create an untracked Markdown file under a normative directory.
3. Run the bilingual gate and verify that it produces no new gap.
4. Run `git add` on the experimental file.
5. Run the gate again and verify that it now produces a new gap.
6. Save the original baseline bytes.
7. Run `--write-baseline` in the dirty tree.
8. Compare the baseline bytes and verify that they are identical.
9. Remove the experimental files and restore a clean working tree.
10. Run `--write-baseline` again and verify successful completion.
11. Invoke the gate from outside the repository and verify correct root resolution.

## 8. Closure Conditions

This registration may be closed only when all of the following are true:

1. A new PR has been created without modifying existing PRs.
2. The repair scope complies with this registration's file restrictions.
3. The Git-tracked set is the sole source for gap enumeration.
4. Git failure paths have been tested and fail closed.
5. All seven new behavioral tests pass.
6. The frozen baseline remains exactly 77 entries.
7. The exemption count remains exactly 21.
8. A tracked document missing bilingual coverage still triggers EXIT=2.
9. Dirty-tree baseline writes are rejected and the original bytes remain unchanged.
10. Clean-tree baseline writing succeeds.
11. The external-cwd test passes.
12. Changed-path and shallow-history behavior have no regressions.
13. The Chinese source and `docs/zh-CN` mirror are byte-identical.
14. The `docs/en` mirror is semantically equivalent to the Chinese source.
15. The PR body contains:

    BILINGUAL-MANIFEST: COMPLETE

16. The coordinator provides real command output, final commit SHAs,
    and independent acceptance evidence.

The registration MUST remain OPEN until every closure condition is met.

## 9. Governance Conclusion

The input set of a bilingual gate MUST be defined by version-control
facts, not by whichever files happen to exist in a particular working tree.

A frozen baseline is governed state, not an arbitrary snapshot of a
filesystem scan.

Therefore:

- enumeration MUST be reproducible;
- tracking status MUST be explicit;
- baseline writes MUST have preconditions;
- file replacement MUST be atomic;
- every failure MUST remain visible and MUST NOT silently permit passage.

This registration repairs only the boundaries described above and does
not authorize weakening any existing bilingual compliance requirement.
