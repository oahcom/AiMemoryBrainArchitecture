# Storage Phase 3.6.5 — Restore Control-High-Water Reference Model Evidence

- Branch HEAD: `19798634fb0d55cb0c901c8f4194506fab96b75b`
- Model: `reviews/storage-consistency/restore_reference/restore_highwater_model.py`, Blob `be0aef6232c8ee2ed6179df7b0a74473c3e25b3b`
- Tests: `reviews/storage-consistency/restore_reference/test_restore_highwater_model.py`, Blob `a9e1a96b449c6bf0e2b52c5fea394a8c32961a24`
- Workflow: `.github/workflows/storage-restore-highwater-reference.yml`, Blob `57ac98e333abfc325bfb9f3d3606fa0801adec4b`
- CI run: `43965501810`; job `133643756066`; commit `19798634fb0d55cb0c901c8f4194506fab96b75b`
- Result: **25/25 TESTS PASS**

## 1. Covered restore invariants

1. Restore starts quarantined and old primary must be fenced.
2. WAL/timeline continuity and exact target LSN are mandatory.
3. COC committed-prefix proof must match current epoch/index/voter configuration/digest/external anchor and be contiguous.
4. I proof set must cover every affected PolicyDomainRef; each PermissionEpoch, sequencer position, revocation high-water, ProducerDomainInventoryEpoch and registry digest must be current.
5. D proof set must cover every relevant ForgetOperation; fence generation, request cutoff, producer-registration high-water, lineage digest and barrier terminal state must match.
6. I TargetInventorySeal and D ForgetOperation binding must match exactly.
7. Storage participant ledger must enumerate every participant and match PreparedParticipantRef, PreparedTransactionGID, native XID, CanonicalAuthorityDBRef, system identifier, database OID, original prepare LSN/timeline and terminal resolution.
8. Pointer and PublicationReceipt transaction identity must match.
9. Signature, integrity, active key version and audience are mandatory.
10. COC/I/D high-water advance during restore forces a repeat reconciliation.
11. RestoreReconciliationReceipt is RECONCILED_BUT_FENCED; it does not enable service without a separate owner gate.
12. Restore receipt never proves Global Forget completion.

## 2. Exact CI outcome

Workflow run `43965501810` concluded SUCCESS; raw log reports 25 tests in 0.002 seconds and `OK`.

## 3. Limits

This is an in-memory logical reference model. It does not call real COC/I/D/Storage proof APIs, verify real signatures/keys, restore PostgreSQL from backup/WAL, reconcile real prepared GIDs, fence an old primary, validate production object-store ACLs or measure RTO. The restore contract remains architecture candidate; production restore remains fenced until real proofs and implementation exist.