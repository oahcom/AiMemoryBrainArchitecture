# R3 Execution Record 012 (F-D-NEW-04/05 Closure)

- Timestamp: 2026-11-19 19:25 (UTC+8)
- Executor: WorkBuddy coordinator
- Commit under test: `5bdcd32` (parent `85293c2`)
- Model blob: `7b7ca8acc8008bf1f9c1e8e444d6bf0add3631ff`
  (55,480 bytes, 1,491 lines, sha256 `3159813480de21c15490d5db09f010ee77c813529a1ae229c6d61f9148bf451b`)
- Test blob: `629867fa644d44d28a32fe13e1c314d3270cd601`
  (86,063 bytes, 2,312 lines, sha256 `262c0764769726f1240cd93f22ab6f7f6c692dc4edac06bd9bd6b32d0f65bbc5`)

## Result

```
Ran 77 tests in 0.005s — OK  (test_r3_contract)
Ran 14 tests in 0.000s — OK  (test_forget_model)
```

77 contract + 14 forget = 91 tests. Exit code 0.

## Delta

1. **F-D-NEW-04** (Owner D `OD-D-FORGET-DELTA-20261119-007`): `test_FSTOR_10` snapshot completeness.
   - `before_tuple = dict(fresh.atomic_tuple)` (was bare reference).
   - Added `before_op_registry = dict(fresh.operation_registry)`, `before_inventory = fresh.inventory_revision`, `before_lifecycle = fresh.lifecycle`.
   - Post-rejection: `assertEqual` on all three.

2. **F-D-NEW-05** (same): `test_FSTOR_17_registry_must_hold_the_authoritative_object` restored.
   - Was lost during concurrent edits (record-010 claimed it existed; it did not).
   - Registry-side swap: `m.operation_registry[idempotency_key]["commit"] = swapped` (field-equal but distinct `AtomicCommit` via `dataclasses.replace`).
   - Retry must fail with full zero-side-effect assertion (commit/fence/counter/outbox/retry_audit/audit/nonce_registry).
