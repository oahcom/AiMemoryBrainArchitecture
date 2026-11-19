# R3 Execution Record 008 (Coordinator Local Execution, U-057 fix)

- Timestamp: 2026-11-19 17:36 (UTC+8)
- Executor: WorkBuddy coordinator (Git Bash / Python 3.13.12)
- Command: `python -m unittest test_r3_contract` and `python -m unittest test_forget_model`
  from `reference-model/`
- Commit under test: `0655d696e6a97d7df74e40f9b88ade0e48567c3c`
  (branch tip of `remediation/aid-2026-001-forget-contract-closure-2026-11-18`,
  parent `114e6d3`)
- Model blob: `0b3e618f1366cf98264a06b291feefe0a895e420`
  (54,036 bytes, 1,427 lines, sha256 `ff4eb7425275c6a3…`)
- Test blob (`test_r3_contract.py`): `b5ad65ebedffb14bb6c337f2183a7534a1618a81`
  (74,534 bytes, 2,063 lines, 74 test methods, sha256 `7d3f9a4be971f009…`)
- Test blob (`test_forget_model.py`): `5d09c6717a81428a23235fb0c87ccf3ade1671d9` (unchanged)

## Result

```
Ran 74 tests in 0.005s

OK

Ran 14 tests in 0.000s

OK
```

74 contract + 14 forget = 88 tests. Exit code 0 for both runs.

## Delta in this commit

Closes `F-D-NEW-02` (Owner D, `OD-D-FORGET-DELTA-20261119-005`, P1):

`commit_suppression()`'s existing-commit branch compared only
`request_hash` against the registry entry, then verified the registered
commit was authoritative. It never compared the caller's `operation_id`
with `original.idempotency_identity.operation_id`. A caller could reuse an
idempotency key under a different operation, present a credential correctly
bound to that different operation — passing `_validate_authorization()` —
and receive the original operation's commit, while `retry_audit` recorded
the original operation identity.

The existing branch now requires:

```python
original.idempotency_identity.operation_id    == operation_id
original.idempotency_identity.idempotency_key == key
original.idempotency_identity.request_hash    == request_hash
```

All three checks run before `_append_retry_audit()`, so a mismatch consumes
no nonce/receipt and moves no projection.

## Tests added / amended

- `test_FSTOR_14_retry_cannot_cross_operation_identity` (new): same key and
  hash under a different operation, with a credential correctly bound to
  that different operation, is rejected; asserts Fence, commit counter,
  outbox, retry audit, `atomic_commit` and lifecycle are unchanged, the
  nonce and receipt registries do not contain the rejected credential, and
  the legitimate retry for the original operation still succeeds afterwards.
- `test_FSTOR_15_retry_reaches_completed_phase` (new): closes Owner D's
  observation that only `CLEANUP` was covered — `COMPLETED` retry reuses the
  commit without projection change, and a first commit in `COMPLETED` is
  still refused with no side effects.
- `test_FSTOR_10` (amended): first-commit rejection in `CLEANUP` now asserts
  `outbox`, `audit`, `retry_audit`, `atomic_tuple` and `nonce_registry` are
  all untouched, not just `atomic_commit` and Fence.
- `test_FSTOR_07` (amended): explicit assertions that
  `authorization_reference.receipt_id` equals
  `authorization_reference.receipt.receipt_id` and likewise for `nonce`,
  per Owner D's request to not rely on the constructor for that relation.

## Non-vacuity

The new test file was run against the parent model
(`114e6d3` blob `2f8993871c117ade24e5229276f8651886e53748`) in an isolated
directory:

```
FAIL: test_FSTOR_14_retry_cannot_cross_operation_identity
Ran 74 tests

FAILED (failures=1)
```

So `FSTOR_14` has real binding force on the fix rather than passing
vacuously.

## Evidence boundary

Coordinator-executed only; no independent owner ran this commit.
DFI-013 (deterministic interleaving, not concurrency linearisation) and
DFI-021 (in-memory boundary, not physical WAL durability) limitations are
unchanged. Production R3 human-expert review OUT-OF-SCOPE (dev-baseline).
`TrustAllReceiptVerifier` is a test double, not cryptographic assurance;
`RejectingReceiptVerifier` remains the shipped default and is proven
fail-closed by `test_FSTOR_12`.
