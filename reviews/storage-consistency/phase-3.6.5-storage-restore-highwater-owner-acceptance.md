# Storage Owner — Exact Restore Control-High-Water and Quarantine Contract Acceptance

- Exact Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- Exact COC protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- Decision: **ACCEPT WITH STORAGE-OWNED RESTORE-RECONCILIATION CONDITIONS — ARCHITECTURE ONLY**
- Mode: Storage Owner technical acceptance; not independent validation or production approval.

Storage accepts the typed COCCommittedPrefixProof, IControlHighWaterProof, DForgetControlHighWaterProof and StorageParticipantLedgerProof model, plus a Storage-issued RestoreReconciliationReceipt that records successful local reconciliation without granting any owner authority or serving permission.

Storage confirms:

1. Restore begins quarantined; no public listener, authoritative reads/writes, cache/index rebuild, Adapter reconnect or content serving.
2. PostgreSQL base backup/WAL/timeline must reach the exact target LSN with a continuous integrity-verified chain; prepared GID/locks are preserved and resolved only by same GID.
3. COC committed prefix/checkpoint and external anchor must be current, gap-free and configuration-bound.
4. IControlHighWaterProof must cover each affected PolicyDomainRef, current PermissionEpoch/revocation high-water, ProducerDomainInventoryEpoch/registry digest and relevant active Forget inventory seals.
5. DForgetControlHighWaterProof must cover every relevant ForgetOperation, fence generation, request cutoff, producer-registration high-water, lineage snapshot and barrier terminal state.
6. StorageParticipantLedgerProof must account for every prepared participant/GID/native-XID tuple and terminal state in the restored snapshot.
7. Storage re-reads COC/I/D high-waters immediately before issuing RestoreReconciliationReceipt; any change repeats reconciliation.
8. RestoreReconciliationReceipt is `RECONCILED_BUT_FENCED`; D/F/G/H/C continue their own current I/D checks. The receipt is not authorization, Forget completion or physical-erasure proof.

Storage accepts the proposed initial RPO boundary only under the specified synchronous durability/fault models; numeric RTO remains TBD until measured restore/control-reconciliation runs. Production archive custody, external checkpoint custody, cloud fencing, operator identity, KMS and runbook remain engineering/deployment work.

**Disposition:** Storage accepts the exact restore control-high-water architecture contract. I/D/A exact acceptance is required before Gate A design can close. Implementation, signatures, API clients and production restore drill are NOT RUN; production activation NOT AUTHORIZED.