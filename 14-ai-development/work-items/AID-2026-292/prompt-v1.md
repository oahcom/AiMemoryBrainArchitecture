# AID-2026-292 — Prompt v1

## Task

Complete the residual symlink-unavailable accounting work for Issue #1268 in `oahcom/AiMemoryBrainArchitecture`.

This work supplements AID-2026-290. AID-2026-290 already changed T36, T37, T41 and T42 to registered skips. Do not alter their semantics or duplicate their `ALLOWED_SKIPS` entries.

## Baseline

Target the `origin/main` version of:

`scripts/test_check_document_management.py`

Baseline blob supplied for this task: `e1e30e735805d678f4bf04b70134f3348259e5d7`.

The following seven symlink creation sites remain unprotected:

- T49: `(root / "docs").symlink_to(outside, target_is_directory=True)`
- T50: `(root / "docs" / "linked").symlink_to(...)`
- T51: `(root / "docs" / "linked.md").symlink_to(outside)`
- T51b: `(root / "docs" / "en").symlink_to(...)`
- T58: `(root / "00-governance" / "linked").symlink_to(...)`
- T59: `(root / "ghost").symlink_to(...)`
- T60: `(root / "tools").symlink_to(...)`

T128 in `run_unbound_emissions()` currently records a failed test when symlink creation raises `OSError` or `NotImplementedError`.

## Required implementation

1. Add exactly these eight entries to `ALLOWED_SKIPS`:
   - `T49 symlinked backlog root is named in the diagnostic`
   - `T50 symlinked directory inside a backlog root is reported`
   - `T51 symlinked markdown file inside a backlog root is reported`
   - `T51b symlinked bilingual mirror directory is refused by name`
   - `T58 symlinked subdirectory in a normative root is reported`
   - `T59 top-level symlink is reported and does not satisfy the registry`
   - `T60 declared directory that is only a symlink is reported`
   - `T128 DM-14 a symlinked mirror directory is named`

2. Use the same bounded skip shape as AID-2026-290:
   `try/except (OSError, NotImplementedError)` and `skip(name, "symlink creation unavailable on this platform")`.

3. A failed creation must record the dependent case only in `SKIPPED`. It must not call `record(..., True)`, `record(..., False)`, or `_bind(...)` for that case.

4. A failed creation must not return from the enclosing test function. Independent cases later in the same function must still execute.

5. Preserve successful symlink-capable execution. In particular, T128's successful `_bind(...)` path must remain byte-for-byte unchanged.

6. Add a suite-registered T129 self-check. It must force `Path.symlink_to` to raise `OSError(1314)`, exercise the relevant test functions, assert all dependent symlink cases are skipped and not recorded as results, and assert independent T43–T47, T52 and T61 cases still execute and pass. Restore all global result/skip state before recording T129 itself.

7. Register T129 in `main()`.

## Hard scope boundaries

- Do not change `check_document_management.py`.
- Do not change CI jobs, branch protection or the 16 required contexts.
- Do not add dependencies.
- Do not alter AID-2026-290's T36, T37, T41 or T42 semantics.
- Do not claim CI, merge, independent review, Owner acceptance or Issue closure.

## Required coordinator measurements

Run the suite normally on a symlink-capable platform.

Run the suite with every `Path.symlink_to` call forced to raise `OSError(1314)`.

Verify:
- 360/360 passed, 13 skipped, 13 registered of 13 allowed, exit 0 under forced failure.
- T43/T44/T45/T46/T47/T52/T61/T129 execute and are True under forced failure.
- Removing the T49 skip registration causes exit 1 with an unregistered-skip diagnostic naming T49.
- The normal capability-platform result is 372/372 passed, one registered skip (T68c), exit 0.
- Reverting T36 to `except -> record(..., True) -> return` makes T129 false, with T36 in RESULTS and not SKIPPED; expected mutation result 355/356.
- Reverting T49 to an unprotected symlink creation under forced failure raises OSError(1314), aborts the suite and exits 1.

Record exact commands, branch head, output and exit codes in `evidence.md`. These supplied measurements are a reference expectation, not permission to claim a new run. After rebase, rerun the measurements against the new exact head.
