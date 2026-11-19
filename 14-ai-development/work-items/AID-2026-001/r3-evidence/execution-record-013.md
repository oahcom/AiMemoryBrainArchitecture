# R3 Execution Record 013 (absent-credential closure)

- Timestamp: 2026-11-19 19:58 (UTC+8)
- Executor: WorkBuddy coordinator
- Commit under test: `95347a5` (parent `99c19f6`, code parent `5bdcd32`)
- Model blob: `771c1fdc6f8a248a7121d165a0b035cebcc9880c`
  (57,020 bytes, 1,494 lines, sha256 `35efab9361f313bb556159818ef2fbb1a6380cbf48d12f8aead273c3c438a946`)
- Test blob: `98d322a554875c223080b2e5393f58148cd8ed34`
  (87,994 bytes, 2,359 lines, sha256 `41952086671e40fc5b01b12bac24e86d232f423924b9c4ad1a1bd45b334578e1`)

## Result

```
Ran 78 tests — OK  (test_r3_contract)
Ran 14 tests — OK  (test_forget_model)
92 passed, 38 subtests passed  (python -m pytest -q)
```

78 contract + 14 forget = 92 tests. Exit code 0.

## Delta

**F-STOR-20261119-01 residual** (raised by Owner D,
`OD-D-FORGET-DELTA-20261119-007`, cross-domain note):

`_validate_atomic_commit()` guarded the projection/credential consistency
block with `if authorization.receipt is not None`. A reference that carried a
`receipt_id` and `nonce` but embedded **no** credential therefore skipped the
entire block and validated — contradicting the record-010 claim that a missing
credential is rejected.

Fix:

```python
        cred = authorization.receipt
        if cred is None:
            raise ContractViolation(
                "authorization reference is missing its credential"
            )
        if cred.receipt_id != authorization.receipt_id: ...
```

Guard is now unconditional; the three agreement checks run on every commit.
The production construction path (`commit_suppression`, L792–797) always sets
`receipt=auth.receipt`, so no legitimate commit relies on the bypass.

Test: `test_FSTOR_19_missing_credential_is_rejected`. Builds a healthy commit,
replaces only `authorization_reference.receipt` with `None` while keeping
`receipt_id` / `nonce` populated, then asserts refusal on both the
`published=True` and `published=False` paths, and asserts the error names the
missing credential.

## Non-vacuity

With the guard restored to its old conditional form
(`git stash push r3_contract_model.py`), `test_FSTOR_19` fails:
`AssertionError` at the `assertRaises(ContractViolation)` for the published
path — the commit validated. Restored model → 92 pass. The test detects the
exact bypass it claims to detect.

## Records corrected

- `execution-record-010.md` item 3 stated "a missing credential is rejected".
  At `b87a7ea` the code did not implement that. See `erratum-004.md`.

## Evidence boundary

Coordinator-executed only; no independent owner ran this commit yet.
DFI-013 (deterministic interleaving, not concurrency linearisation) and
DFI-021 (in-memory model, not physical WAL durability) unchanged.
`TrustAllReceiptVerifier` is a test double; `RejectingReceiptVerifier` is the
shipped default and stays fail-closed (`test_FSTOR_12`). Real signature
verification, production issuance of a fresh credential per retry, and
production verifier enforcement remain **NOT RUN**.
