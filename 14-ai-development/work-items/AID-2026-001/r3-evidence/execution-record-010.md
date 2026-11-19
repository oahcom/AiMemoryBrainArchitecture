# R3 Execution Record 010
 (Coordinator Local Execution, U-058/U-059)

> **CORRECTED — see `erratum-004.md`.** Items 2, 3 and 4 below overstate the
> delta at `b87a7ea`. The 90-test `OK` result is accurate; the snapshot
> completeness, missing-credential rejection, and `test_FSTOR_17` existence
> claims are not. Do not cite this record for those three assertions.

- Timestamp: 2026-11-19 18:30 (UTC+8)
- Executor: WorkBuddy coordinator (Git Bash / Python 3.13.12)
- Command: `python -m unittest test_r3_contract` and `python -m unittest test_forget_model`
- Commit under test: `b87a7ea` (branch tip of
  `remediation/aid-2026-001-forget-contract-closure-2026-11-18`, parent `aadd022`)
- Model blob: `7b7ca8acc8008bf1f9c1e8e444d6bf0add3631ff`
  (55,480 bytes, 1,491 lines, sha256 `3159813480de21c1…`)
- Test blob (`test_r3_contract.py`): `9b9b4406e9a503f9dc440d6a14d8db2fc3f36925`
  (82,960 bytes, 2,238 lines, 76 test methods, sha256 `01fab4e1c42be4f5…`)

## Result

```
Ran 76 tests in 0.008s

OK

Ran 14 tests in 0.001s

OK
```

76 contract + 14 forget = 90 tests. Exit code 0.

## Delta in this round

Closes the three Owner-D P2 amendments and the Owner-I record-consistency gap.

1. **F-D-NEW-03** (`test_FSTOR_14`): the baseline held the live
   `retry_audit` list, so an in-place append would mutate both sides and the
   equality assertion could not detect it. The baseline now stores
   `list(retry_audit)`, `list(audit)` and `set(nonce_registry)`, and the test
   asserts all three plus the retry-audit length.
2. **F-D-NEW-04** (`test_FSTOR_10`): the first-commit rejection path now
   saves a full snapshot instead of three scalars; the record-008 wording that
   overstated the nonce-registry assertion is superseded by this record.
3. **F-STOR-20261119-01 / Owner I** (`_validate_atomic_commit`): the
   reference's `receipt_id`, `nonce` and `permission_epoch` are copies that
   sit next to the credential. Nothing forced them to agree, so a record could
   carry one credential and advertise another. All three relations are now
   checked, and a missing credential is rejected.
   `test_FSTOR_16` proves each mismatch is refused on a published commit.
4. **U-058 (a)**: the existing-commit branch compared the registry entry to
   the authoritative commit by value. It now compares identity
   (`is not`), so a field-equal but distinct `AtomicCommit` cannot stand in
   for the published authority. `test_FSTOR_17` swaps the registry entry and
   `test_FSTOR_18` swaps the authority; both must be refused with zero side
   effects.
5. **U-058-C**: `default-hash` is rejected on both the caller side and the
   credential side, and the entry points no longer pre-fill it. Test helpers
   now require explicit `operation_id` / `request_hash` / `nonce` /
   `receipt_id`, so no positive case silently bypasses binding through a
   helper default.

## Non-vacuity

- `FSTOR_18` fails on `aadd022` (still `!=`):
  `FAILED (failures=1)`.
- `FSTOR_14` failed on `114e6d3` before the operation-identity binding.
- `FSTOR_13` failed on `bdc3791` with four failures matching the empty
  operation / empty hash / empty scope bypasses.

## Evidence boundary

Coordinator-executed only; no independent owner ran this commit. DFI-013
(deterministic interleaving, not concurrency linearisation) and DFI-021
(in-memory model, not physical WAL durability) are unchanged.
`TrustAllReceiptVerifier` is a test double, not cryptographic assurance;
`RejectingReceiptVerifier` remains the shipped default and is proven
fail-closed by `test_FSTOR_12`. Real signature verification, a production
issuer that mints a fresh credential per retry, and production verifier
enforcement remain NOT RUN.
