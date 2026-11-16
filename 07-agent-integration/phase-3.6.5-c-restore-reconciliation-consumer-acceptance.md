# C Owner — Exact Restore Reconciliation / Provider-Side-Effect Consumer Acceptance

- Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- I proof acceptance Blob: `85d62b8858fc86addacd3b83f49476e42f49b785`
- D proof acceptance Blob: `211e54acfb4573b1c51d96f07af297671dfc4c4b`
- A restore integration acceptance Blob: `fa5e066a208a64401c96a6b8790d8b53dc7f1585`
- Decision: **ACCEPT WITH C PROVIDER RESTORE GATE CONDITIONS**

C accepts that restore reconciliation is not provider authorization or provider outcome. After restore, C must not submit/retry a protected provider side effect until the exact Storage RestoreReconciliationReceipt is verified, the COC committed prefix is current, I authorization/PermissionEpoch is freshly checked, D Forget/lineage barrier is clear for the exact operation and the same C ProviderIdempotencyKey/request digest is resolved. The Storage receipt does not prove CSubmitOutcome or provider success.

C's ProviderIdempotencyKey remains distinct from PreparedParticipantRef/PreparedTransactionGID/native XID. Restore or process restart never creates a new key for an uncertain provider request. Missing proof, stale permission, D barrier, ambiguous provider result or audience/signature failure remains UNKNOWN/IN_DOUBT. No provider submit occurs while RESTORE_FENCED or solely because Storage is RECONCILED_BUT_FENCED.

Limit: C provider runtime/restore integration and real provider idempotency lookup remain NOT IMPLEMENTED / NOT RUN.