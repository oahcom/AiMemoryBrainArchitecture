# AID-2026-292 — Prompt v1

## Role

You are the implementation agent for a narrowly scoped test-suite
regression change in:

`oahcom/AiMemoryBrainArchitecture`

Tracking issue: #1268

## Objective

Add one in-suite regression case, T129, proving that symlink-unavailable
skips do not erase independent test cases executed by the same runner
functions.

The eight symlink-dependent sites were already implemented and landed
by AID-2026-324. They are not part of this task.

## Starting context

Implementation branch:

`fix/2026-11-27-aid-292-in-suite-skip-selfcheck`

Reported fork point:

`561e9f24`

Target file:

`scripts/test_check_document_management.py`

The existing test runner uses a `main()` runners tuple.

## Required implementation

Add:

`run_symlink_unavailable_self_check()`

The case must:

1. Patch `Path.symlink_to` to raise `OSError(1314)`.
2. Exercise:
   - `run_symlink_boundary()`
   - `run_scan_boundary()`
   - `run_unified_scan()`
   - `run_unbound_emissions()`
3. Assert that the twelve expected skipped names exactly match
   the newly added SKIPPED slice.
4. Assert that none of those twelve names appears in the new
   RESULTS_BY_NAME entries.
5. Assert that UNEXPECTED_SKIPS remains empty.
6. Assert that all of the following independent cases recorded True:
   - T43
   - T44
   - T45
   - T46
   - T47
   - T52
   - T61
7. Restore RESULTS, SKIPPED, UNEXPECTED_SKIPS, and RESULTS_BY_NAME
   before recording T129 itself.

Register:

`run_symlink_unavailable_self_check`

in the existing `main()` runners tuple.

## Acceptance tests

### Normal run

Command:

`python scripts/test_check_document_management.py`

Expected:

- 372/372 passed.
- One skipped case: T68c.
- Exit code 0.

### Forced symlink-unavailable run

Run the same test file while globally forcing
`Path.symlink_to` to raise `OSError(1314)`.

Expected:

- Exit code 0.
- 360/360 passed.
- 13 skipped.
- 13 registered of 13 allowed.
- UNEXPECTED_SKIPS empty.
- DOUBLE_RECORD empty.
- T129 True.

### Mutation sensitivity

Mutate one dependent case so that its symlink-unavailable skip
is incorrectly replaced by:

`record(..., True)`

Expected:

- T129 becomes False.

This test must demonstrate that T129 detects the regression it
is intended to prevent.

### Scope check

Inspect the final diff and runner tuple.

Expected:

- T129 is the only case added.
- No unrelated test cases are added.
- No unrelated behavior is changed.

## Hard constraints

Do not modify:

- AID-2026-324's `_create_symlink_or_skip` helper.
- AID-2026-324's eight registered sites:
  T49, T50, T51, T51b, T58, T59, T60, T128.
- `skip()`.
- `ALLOWED_SKIPS`.
- CI jobs or workflow files.
- Branch protection.
- The 16 required status contexts.
- Production code.

Do not add dependencies.

Do not weaken existing test or skip semantics.

Do not wire the standalone
`verify_full_suite_symlink_unavailable.py` into CI.

## Evidence requirements

Record:

- Exact tested file SHA-256.
- Normal test output and exit code.
- Forced OSError(1314) test output and exit code.
- Mutation sensitivity result.
- Final changed-file list.
- Verification that T129 is the only added case.

All measurements must be repeated after any rebase or modification.

## Authority boundaries

Implementation does not constitute review approval or Owner acceptance.

Do not claim:

- PR merge.
- CI integration.
- CI success.
- Independent review approval.
- Owner acceptance.
- Completion of AID-2026-324's work.

Stop after delivering the narrowly scoped implementation and its
reproducible evidence.
