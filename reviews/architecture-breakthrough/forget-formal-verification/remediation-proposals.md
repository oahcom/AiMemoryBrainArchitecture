# Remediation Proposals — Owner-Assigned, Non-Authoritative

These are closure proposals only; they do not amend Owner contracts.

| Priority | Owner | Required work | Exit evidence |
|---|---|---|---|
| P0 | D + Storage | Specify/prove one atomic ordering domain for ProducerWork registration, Fence high-water capture, final lineage/Fence validation and VisibilityPointer + PublicationReceipt commit | Exact accepted contract; database transaction tests; lost-ACK and crash/failover evidence |
| P0 | I | Approve producer/recipient inventory source, inventory epoch/seal, join/leave/change invalidation and Global Forget completion/exception policy | Signed current inventory seal and governance decision; no unknown producer domain |
| P0 | E | Promote derived registration/publication from Candidate to Owner-approved exact contract; prove complete dependency set is durable before visibility | Independent D/E/Storage acceptance; executable retry/DLQ/replay race tests |
| P0 | Storage | Close JF-10 cross-authority crash-atomic coupling between I sequencer decision and Storage visibility participant | Real database/HA crash campaign; immutable terminal outcome; same-GID recovery |
| P1 | F | Prove retrieval/index/cache/Working Set paths consult latest Fence at candidate and final disclosure boundaries | Integration tests for in-flight query, cache refill, stale segment swap and unknown authority |
| P1 | G | Freeze Applied persistence/reconciliation exact version with C/H/COC/Storage; late ACK cannot revive current-use state | Cross-owner accepted contract; crash/restore/duplicate receipt tests |
| P1 | H | Promote Adapter ACK/reconnect to accepted contract; prove stale offline snapshot and queued delivery cannot re-enter managed region | Adapter fault tests with per-target evidence and reconnect fencing |
| P1 | Storage + I + D | Restore quarantine/reconciliation/release: current COC prefix, I/D high-waters, participant ledger and stable final recheck | Physical PITR/backup/pg_rewind tests; service gate closed on mismatch |
| P2 | A / independent reviewer | Maintain exact branch/commit/blob evidence ledger and rerun model after Owner contract changes | Reproducible model and bilingual parity report |

## Implementation blockers

1. Confirm exactly one physical transaction domain per Canonical Memory Authority and select DB/isolation/HA profile.
2. Establish authoritative I inventory for all producers, recipients, backups and external copies.
3. Define exact final publication commit record and atomic consumption of single-use I authorization outcome.
4. Prove restore high-waters cannot themselves be rolled back with the restored backup.
5. Decide which F/G/H boundaries synchronously check Fence and what target-specific evidence closes each obligation.
