# Phase 3.8.26 — G Restore-Fenced Write Admission Hardening
# Phase 3.8.26 — G Restore-Fenced Write Admission 加固

- Date: 2026-11-18
- Exact code commit: `470d4c1934999263bfb8a4822b13c2ff854c3dfd`
- Test Blob: `e77d2375506e423bf53d8341fe9aecf2719d0609`
- Workflow: [G Applied Persistence Reference Model #44188852578](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44188852578)
- Job: `g-applied-reference-model` — SUCCESS
- Log: `Ran 17 tests ... OK`

## 1. Defect found

The reference model correctly disabled protected current use after a stale/mismatched restore, but `commit_full_applied` did not consult the global `serving_enabled` restore-fence state. A caller could therefore create a *new* Full Applied ledger/outbox record while restore reconciliation was still fenced.

This contradicted the G contract's requirement to block new Full Applied and protected current use until authoritative reconciliation completes.

## 2. Fix

Before allocating a new ledger sequence or inserting a new Applied row, `commit_full_applied` now reads `g_meta.serving_enabled` inside the same SQLite write transaction and rejects a new Full Applied commit while the restore fence is active.

An idempotent lookup of an already committed identical identity/revision/digest still returns its original receipt; it does not create a new row. Current-use remains denied while the global restore fence is active.

New negative test:
- `test_17_restore_fence_blocks_new_full_applied_commit`

The test first commits an existing Applied row, introduces a stale restore that sets FENCED, then attempts a different new Applied identity. The attempt is rejected and ledger/outbox counts remain unchanged.

## 3. Verification

Exact commit `470d4c1934999263bfb8a4822b13c2ff854c3dfd` passed **17/17** in run #44188852578. The preceding restore-anchor tests 15 and 16 remain in the same suite and passed in this run as well.

## 4. Limits

This is still a bounded SQLite reference model. It does not prove production G database transactions, authenticated external anchors, live owner-ledger proof resolution, multi-process/multi-replica recovery, PostgreSQL/Storage integration or production Full Applied. Production G remains NOT IMPLEMENTED / NOT VERIFIED.
