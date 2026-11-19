# R3 Execution Record 009 (Coordinator Local Execution, F-STOR-01 consistency)

- Timestamp: 2026-11-19 17:48 (UTC+8)
- Executor: WorkBuddy coordinator (Git Bash / Python 3.13.12)
- Command: `python -m unittest discover -s . -p 'test_*.py'` from `reference-model/`
- Commit under test: `2c458c9` (parent `66e78af`, branch tip of
  `remediation/aid-2026-001-forget-contract-closure-2026-11-18`)
- Delta: `_validate_atomic_commit()` cross-checks AuthorizationReference
  scalar fields against the embedded ReceiptCredential; `test_FSTOR_16`
  adds three inconsistent-record rejection cases.

## Result

```
Ran 89 tests in 0.006s

OK
```

89 = 75 contract + 14 forget. Exit code 0.

## Findings addressed

- `F-STOR-20261119-01` (Storage, P2): receipt_id/nonce/permission_epoch
  projection fields now verified equal to the embedded credential.
- `F-OI-04` residual #3 (Owner I, P2): same consistency invariant.

## Remaining NOT RUN (declared boundaries, not defects)

- Real cryptographic signature verification (wrong key/algorithm, tampered
  signature, revoked key). `TrustAllReceiptVerifier` is a test double.
- Production issuing service minting fresh credentials per attempt.
- Production deployment enforcement that a permissive verifier cannot be
  substituted. The model defaults to fail-closed (`RejectingReceiptVerifier`).

These are OUT-OF-SCOPE(dev-baseline) for the in-process reference model.

## Evidence boundary

Coordinator-executed only. DFI-013 / DFI-021 limitations unchanged.
