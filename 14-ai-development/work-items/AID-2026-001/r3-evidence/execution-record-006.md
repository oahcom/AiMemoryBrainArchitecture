# R3 Execution Record 006 (Coordinator Local Execution, U-056c)

- Timestamp: 2026-11-19 17:02 (UTC+8)
- Executor: WorkBuddy coordinator (Git Bash / Python 3.13.12)
- Command: `python -m unittest test_r3_contract` and `python -m unittest test_forget_model`
- Commit under test: `c44576a69304fad12ed66f5e7f498d4d4df1ac1f`
  (parent `316b70e`, branch tip of `remediation/aid-2026-001-forget-contract-closure-2026-11-18`)
- Model blob: `2f8993871c117ade24e5229276f8651886e53748` (52,885 B, sha256 `92deb655e1522250c7159348…`, 1,401 lines)
- Test blob (`test_r3_contract.py`): `3b71a8fe647bc9ce6751ced079fc101f63be5ae2` (67,286 B, sha256 `e275b5b661fb68d3c269a5c7…`, 1,879 lines)

## Result

```
Ran 72 tests in 0.005s

OK

Ran 14 tests in 0.001s

OK
```

Total 86 tests (72 contract + 14 forget).

## Delta closed here

Strict credential context binding (F-OI-04 gaps A/B/C from the independent U-056 review of `4e646d5`).

Replaced the permissive guards

```python
if request_hash and cred.request_hash and cred.request_hash != request_hash: ...
if operation_id and cred.operation and cred.operation != operation_id: ...
if cred.scope and "suppression:commit" not in cred.scope: ...
```

with unconditional binding:

```python
if not cred.operation:            raise ContractViolation("receipt operation missing")
if cred.operation != operation_id: raise ContractViolation("receipt operation mismatch")
if not cred.request_hash:          raise ContractViolation("receipt request hash missing")
if cred.request_hash != request_hash: raise ContractViolation("receipt request_hash mismatch")
if not REQUIRED_RECEIPT_SCOPE.issubset(cred.scope):
                                   raise ContractViolation("receipt scope insufficient")
```

`REQUIRED_RECEIPT_SCOPE = frozenset({"suppression:commit"})` is now a model constant.
`authorize_and_suppress()` also passes `operation_id` / `request_hash` into validation, so first
commit and retry run the same binding checks.

## Tests

- `test_FSTOR_13_credential_context_binding_is_mandatory`: baseline credential commits; then five
  rejected cases — empty operation, empty request hash, the `"default-hash"` placeholder used for a
  different request, scope missing `suppression:commit`, empty scope. Each asserts no commit, no
  fence advance, no retry audit and no nonce consumption.
- Test helper `auth()` now binds `operation_id` and `request_hash` (defaulting to
  `commit_suppression()`'s own defaults) and every call site that commits under another identity
  passes them explicitly. Nonce-replay tests (`T03`, `AUTH_09`, `FSTOR_06`) were re-pointed at the
  same identity so the rejection still comes from replay, not from a binding mismatch.

## Non-vacuity check

`test_FSTOR_13` and the amended `test_FSTOR_11` were run against the pre-strict model (`bdc3791`,
blob `33eb1c91…`): `FAILED (failures=4)` — the empty-operation, empty-request-hash and empty-scope
bypasses reproduce exactly, plus the operation-binding gap in FSTOR_11. `FSTOR_10`, `FSTOR_12` and
the F-D-NEW-01 gate split are unchanged by this round.

## Remaining NOT RUN

- Real cryptographic signature verification (wrong key, wrong algorithm, tampered signature,
  revoked key). `TrustAllReceiptVerifier` is a test double and proves nothing about signatures.
- That a production issuing service can mint a fresh credential per attempt.
- That a production deployment cannot substitute a permissive verifier. The model accepts an
  injected verifier by construction and defaults to fail-closed; deployment-level enforcement is
  outside this reference model.

## Provenance

- Independent reviewer (session `6afea00e-a570-83ee-943f-9767f2440765`) reviewed `4e646d5` and
  issued `AID-2026-001-R1-U056-001`, `ACCEPT_WITH_AMENDMENTS`, F-D-NEW-01 PASS, F-OI-04 OPEN, with
  the three binding gaps plus the production-verifier boundary as the only remaining items.
- This round implements those three binding items only. It does not reopen F-D-NEW-01, F-OI-03,
  F-OI-01 or F-OI-02.
