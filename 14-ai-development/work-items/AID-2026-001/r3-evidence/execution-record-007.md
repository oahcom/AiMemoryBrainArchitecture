# R3 Execution Record 007 (Coordinator Local Execution, U-056e)

- Timestamp: 2026-11-19 17:05 (UTC+8)
- Executor: WorkBuddy coordinator (Git Bash / Python 3.13.12)
- Command: `python -m unittest discover -s . -p 'test_*.py'` from `reference-model/`
- Commit under test: `114e6d30593cc043e267d0666d86136c174fa460`
  (branch tip of `remediation/aid-2026-001-forget-contract-closure-2026-11-18`, parent `8ebe49c`)
- Model blob: `2f8993871c117ade24e5229276f8651886e53748` (unchanged from `316b70e`)
- Test blob (`test_r3_contract.py`): `cd37e38a43b7392c4ac0b573187075c3866ceda4` (67,769 bytes, 1,893 lines, 72 test methods)
- Test blob (`test_forget_model.py`): `5d09c6717a81428a23235fb0c87ccf3ade1671d9` (unchanged)

## Result

```
Ran 86 tests in 0.008s

OK
```

86 = 72 contract + 14 forget. Exit code 0.

## Delta in this commit (U-056e)

Operation-mismatch (non-empty wrong operation) rejection cases added on both paths,
closing minimal-fix item 5 of `AID-2026-001-R1-U056B-001`:
- `test_FSTOR_13` first-commit path: `authorized_attempt("other-operation", ...)` rejected
  with no commit / no fence advance / no retry audit / no nonce consumption.
- `test_FSTOR_11` idempotent-retry path: `auth(operation_id="other-operation", ...)`
  rejected with full no-side-effect assertions via `assert_no_retry_side_effect`.

## Relationship to record 006

Record 006 documents the run at `c44576a`. This record supersedes it as the execution
evidence for `114e6d3`; record 006 remains valid for `c44576a` itself.

## Evidence boundary

Coordinator-executed only. DFI-013 / DFI-021 limitations unchanged.
Production R3 human-expert review OUT-OF-SCOPE(dev-baseline).
