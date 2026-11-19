# R3 Execution Record 015 (Storage P2 amendments)

- Timestamp: 2026-11-19 21:35 (UTC+8)
- Executor: WorkBuddy coordinator
- Base commit: `745c768` (code target `95347a5`)
- Model blob: `771c1fdc6f8a248a7121d165a0b035cebcc9880c` — unchanged
  (57,020 bytes, 1,494 lines, sha256 `35efab9361f313bb556159818ef2fbb1a6380cbf48d12f8aead273c3c438a946`)
- Test blob: `22b8d81e7738fe66074f9973932a2dbe79fb52ae`
  (94,380 bytes, 2,450 lines, sha256 `f326cafd70c97a7cc0133ad2139d7508d83f493c710d80f534e01c25d68734ce`)

## Result

```
Ran 93 tests in 0.006s — OK  (python -m unittest discover)
= 79 contract + 14 forget_model
```

Exit code 0. Model code is byte-identical to `95347a5`; only tests changed.

## Delta

Storage reviewer `DEC-AID-2026-001-STOR-20261119-06` accepted the code at
`95347a5` with two P2 test/evidence amendments. Both are addressed here.

### F-STOR-20261119-03 — staged rollback integration path

`test_FSTOR_20_staged_rejects_missing_credential_and_restores_projection`
uses a test-only `R3Model` subclass that strips the embedded credential from
the commit passed to PHASE 1 staged validation. The rejection therefore
travels through the real `commit_suppression()` staged projection writes,
exception handler and `_restore_commit_snapshot()`.

Assertions:

- `ContractViolation` text contains `missing its credential`;
- 11 business projections restored (`atomic_commit` by identity, everything
  else by value);
- `ATOMIC_TUPLE_ABORTED` is the *only* audit delta — an expected diagnostic
  event, so "zero side effect" is explicitly bounded to business state.

### F-STOR-20261119-04 — registry swap not silently repaired

`test_FSTOR_17_registry_must_hold_the_authoritative_object` now asserts:

```python
self.assertIs(m.operation_registry[idempotency_key]["commit"], swapped)
```

after the rejected retry, proving the deliberately corrupted registry
projection survives the rejection path unchanged.

## Vacuity check

- Removing the new FSTOR_17 assertion while replacing the registry entry
  back with `first` makes the test fail (`AssertionError: ... is not ...`);
  restoring the file returns 93/93 OK.
- The staged test reaches the intended branch: without `Phase.AUTHORIZED`
  it fails earlier with `authorization workflow phase required`; with it,
  the rejection text is `missing its credential`.

## Boundary

In-memory reference model only. No WAL, fsync, torn-write, power-loss,
physical crash-recovery or production verifier claim. DFI-013 / DFI-021
limits retained.
