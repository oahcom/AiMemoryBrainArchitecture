# R3 Runbook

## Scope and evidence level
This is a contract-level reference-model consistency suite only. It is not proof of production Transaction/WAL durability, replica/failover behavior, per-copy erasure, complete backup inventory, or production Restore safety. v2.2 remains PROPOSED. Passing tests does not imply implementation completion, Owner approval, or production activation.

## Execution baseline
- Executor: coordinator local environment (must be stated in the returned record)
- Repository: oahcom/AiMemoryBrainArchitecture
- Work directory: repository root
- Python: CPython 3.10+; standard library only
- Record exact checked-out commit SHA before execution; branch name is not a substitute.

## Exact command
From repository root:
```sh
python --version
python -m unittest discover -s 14-ai-development/work-items/AID-2026-001/reference-model -p 'test_*.py' -v
```
From reference-model directory:
```sh
python --version
python -m unittest discover -s . -p 'test_*.py' -v
```
Do not suppress stderr, filter failures, use `|| true`, or alter the exit code. Preserve complete stdout, stderr and exit code.

## Test inventory
- Existing baseline: 24 tests in test_forget_model.py (14 at original authoring; 10 added by later mainline).
- DFI-001…DFI-022: methods test_DFI_001…test_DFI_022 (22).
- I-U011-T01…T16: methods test_T01…test_T16; report full source IDs (16).
- STOR-01…07: methods test_STOR_01…test_STOR_07 (7).
- AUTH-01…AUTH-14: methods test_AUTH_01…test_AUTH_14 (14).
- FSTOR-01…FSTOR-20: methods test_FSTOR_01…test_FSTOR_20 (20).
- Expected discovered count: 103 (79 contract + 24 baseline). Any difference must be investigated and reported.
- Baseline reconciliation: 59 = original expectation (22+16+7+14 baseline-14); 93 = source dev-baseline run (79 contract + 14 baseline, record-014/015); 103 = current exact-Head run (79 contract + 24 baseline, record-017). Canonical current expectation = 103.

## Per-ID result table (expand to one row per ID)
| Test ID | Expected assertion | Actual result | PASS/FAIL/NOT IMPLEMENTED/NOT RUN | Output reference | Notes |
|---|---|---|---|---|---|
| DFI-001…022 | Matrix invariant | | | | |
| I-U011-T01…T16 | U-011 §8 invariant | | | | |
| STOR-01…07 | Fault schedule | | | | |
| AUTH-01…14 | Authorization matrix invariant | | | | |
| FSTOR-01…20 | Fault schedule / projection exactness | | | | |
| Existing baseline ×24 | Existing assertions unchanged | | | | |

Never mark unexecuted tests PASS. Preserve failures and tracebacks exactly. Production-only gaps must be separately marked NOT IMPLEMENTED / NOT RUN, not used to disguise the model test status.

## Required execution record
Executor and environment; exact commit SHA; Python implementation/version; OS; working directory; exact command; timestamp/timezone; full stdout/stderr; exit code; discovered/pass/fail/skip counts; per-ID table; fixtures and fault schedule; source contract paths and Blob SHAs; evidence level statement.

## Fault schedules represented
Atomic tuple abort before commit; stale replica promotion; old worker/lease rejection; duplicate/outbox replay; unknown external outcome requiring reconciliation before retry; Restore quarantine until current Fence and later Forget operations are reconciled; absent/unauthenticated/empty backup manifest => UNKNOWN. These are deterministic in-memory model schedules, not physical crash tests, multi-process concurrency tests, storage-provider tests, or durability proofs.

## Production-only evidence gaps
Unless supplied by a real implementation and independently evidenced, record Transaction/WAL receipts, durable replica high-water observations, per-replica erase/de-identification receipts, authenticated complete backup manifests, and Restore quarantine/reconciliation receipts as NOT IMPLEMENTED / NOT RUN.

Archive coordinator-supplied raw output verbatim in r3-evidence with the expanded per-ID table. Do not edit contract documents. Keep AID-2026-001 BLOCKED_PENDING_R3_EVIDENCE until evidence and independent review gates close.
