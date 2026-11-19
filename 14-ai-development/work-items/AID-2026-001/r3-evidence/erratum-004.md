# Erratum for execution-record-010

- Raised: 2026-11-19 19:58 (UTC+8), by coordinator
- Applies to: `14-ai-development/work-items/AID-2026-001/r3-evidence/execution-record-010.md` (commit `81e51b7`, target `b87a7ea`)
- Raised on: Owner D `OD-D-FORGET-DELTA-20261119-007`

## Defects

Record 010 claims three things that its own target commit does not support.
The test counts and the `OK` result for `b87a7ea` are accurate; the delta
descriptions are not.

| Record 010 claim | Actual state at `b87a7ea` |
|---|---|
| Item 2: `test_FSTOR_10` "now saves a full snapshot instead of three scalars" | Partly false. `before_nonce_registry = set(...)` and the audit copies were added, but `before_tuple = fresh.atomic_tuple` stayed a bare reference, and `operation_registry` / `inventory_revision` / `lifecycle` were not captured at all. |
| Item 3: "…and a missing credential is rejected" | False. `_validate_atomic_commit()` used `if authorization.receipt is not None`, so an absent credential skipped the consistency block entirely and validated. |
| Item 4: "`test_FSTOR_17` swaps the registry entry" | False. No `def test_FSTOR_17...` existed in the `b87a7ea` test blob; the only mention was a docstring reference inside `test_FSTOR_18`. |

## Correction

- Claims 1 and 3 were closed in code: F-D-NEW-04 at `5bdcd32`
  (`execution-record-012.md`), F-D-NEW-05 likewise (FSTOR_17 restored).
- Claim 3 was closed at `95347a5`: the guard is now unconditional and
  `test_FSTOR_19_missing_credential_is_rejected` proves it
  (`execution-record-013.md`).
- The identity-correct record for the current tip is
  `execution-record-013.md` (commit `95347a5`, model blob `771c1fdc…`,
  test blob `98d322a5…`, 92 tests).
- Do not cite record 010 for the snapshot-completeness, missing-credential, or
  FSTOR_17 assertions. Its `76 contract + 14 forget = 90 tests OK` line
  remains valid.

## Cause

The record was written from the author's intended delta rather than from the
committed blob, and shipped in the same push as the code. No test run was
fabricated — the 90-test `OK` output is real for `b87a7ea`. The defect is that
three prose claims were not verified against the code they describe, which is
exactly the failure mode NR-001 (author ≠ reviewer) exists to catch: the
reviewer found them, not the author.
