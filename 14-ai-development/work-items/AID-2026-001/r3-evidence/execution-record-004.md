# R3 Execution Record 004 (Coordinator Local Execution, U-055)

- Timestamp: 2026-11-19 15:20 (UTC+8)
- Executor: WorkBuddy coordinator (Git Bash / Python 3.13)
- Command: `python -m unittest discover -v` (cwd: `reference-model/`)
- Commit under test: `3948024` (full: `39480248` branch tip of `remediation/aid-2026-001-forget-contract-closure-2026-11-18`, parent `d763a92`)
- Model blob: `ee3df6f58d87defac4ec0dfa20caf567326fb6f0` (46,679 bytes, sha256 `99ea70ba7d4beeb5…`, 1,284 lines)
- Test blob (`test_r3_contract.py`): `5521b519f23cbd63a044d2c8f09cd008b2d26a38` (48,833 bytes, sha256 `a65c593e35c44f3d…`, 1,439 lines)
- Test blob (`test_forget_model.py`): `5d09c6717a81428a23235fb0c87ccf3ade1671d9` (7,415 bytes, sha256 `5d9bd9327f542b7f…`, 150 lines)

## Result

```
Ran 82 tests in 0.006s

OK
```

Exit code: 0. Breakdown: 68 `test_r3_contract` + 14 `test_forget_model`.

`test_r3_contract` composition: DFI 22, OwnerIU011 T01–T16 16, StorageFaults STOR-01..07 7,
AuthorizationCommitEntry 14, AtomicPublicationFaultInjection FSTOR-01..09 9 → 68 total.

## What this record supersedes

`execution-record-003.md` was committed as `427f76c` and cites a commit `77f6a3b…` and a model
blob `6ad55a4c…`. **Both objects are unresolvable in this repository** (`git cat-file -t` returns
`could not get object info`), and `427f76c`'s parent is `d763a92`, not the `e36a23a` stated there.
Record 003's identifiers are therefore not evidence-bound; treat record 003 as SUPERSEDED for
identity purposes. Its narrative (three deltas, 66 tests) is reproduced correctly in
`execution-record-003.md`'s prose but must not be cited as provenance for a specific SHA.

Record 004 is the identity-correct record for the current tip.

## Two defect rounds closed here

1. **F-OI-03 (P1, Owner D)**: `live_state=False` had gated both the `lifecycle == FORGOTTEN`
   terminal assertion and the `phase == SUPPRESSION_COMMITTED` assertion. A committed record with
   lifecycle rolled back to `ACTIVE` + phase reset to `AUTHORIZED` could be "reused" by an
   idempotent retry. Fix: the lifecycle assertion is now unconditional; only `phase` remains
   `live_state`-gated. Regression: `test_FSTOR_08`.
2. **F-OI-04 (P2, Owner I)**: retry audit wrote a model-generated `retry-receipt-N` while
   `Authorization` had no issuer-supplied receipt field. Fix: `Authorization.receipt_id` is now an
   authorization input; the commit boundary rejects a missing or already-used receipt; the first
   commit binds `auth.receipt_id` into `AuthorizationReference`; the retry audit records
   `auth.receipt_id`. Used receipts derive from the authoritative commit plus committed retry audit
   entries, mirroring the Nonce projection. Regression: `test_FSTOR_09`.

## Non-vacuity check

The 68-test suite was also run against the previous model (`d763a92`, blob
`427ef85772d1223a3e4da3a0b7574bd53ed4f758`): `FAILED (failures=1, errors=79)`. The two new tests
therefore constrain the new behaviour rather than passing trivially.

## Provenance

- A–E deltas proposed by the coordinator as a manager view; the author session
  `6afe842b-1430-83ee-9f30-3547ca54ba1b` returned `ACK` on all five, plus the two test methods
  (`test_FSTOR_08`, `test_FSTOR_09`) and the `auth()` helper change, at 15:06 with an explicit
  `NOT RUN` declaration.
- Landing, execution and commit by the coordinator. No fabricated output.

## Evidence level (honest)

Contract-level in-memory reference-model consistency evidence. This is **not** production runtime
persistence proof. DFI-013 remains a deterministic sequential interleaving, not a concurrency
proof. DFI-021 remains an in-memory boundary, not physical durability or crash-recovery evidence.
Production-level gaps (real WAL receipts, real replica inventories, real backup restores) remain
NOT IMPLEMENTED / NOT RUN.

## stderr (raw)

```
Ran 82 tests in 0.006s

OK
```
