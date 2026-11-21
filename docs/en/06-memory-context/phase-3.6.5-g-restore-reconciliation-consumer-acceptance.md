# G Owner — Exact Restore Reconciliation / Context Delivery Consumer Acceptance

- Storage restore contract Blob: `4f656163aeba532a441eaed1d293a48e2363cb4a`
- I proof acceptance Blob: `85d62b8858fc86addacd3b83f49476e42f49b785`
- D proof acceptance Blob: `211e54acfb4573b1c51d96f07af297671dfc4c4b`
- A restore integration acceptance Blob: `fa5e066a208a64401c96a6b8790d8b53dc7f1585`
- Decision: **ACCEPT WITH G CONTEXT / APPLIED / DELIVERY RESTORE GATES**

G accepts that restore reconciliation is not Full Applied, current-use authorization or delivery permission. Restored Context snapshots, deltas, membership, materializations and delivery intents must be reconciled to the current COC prefix, I PermissionEpoch/revocation/registry high-water, D Forget/lineage barrier and Storage pointer/receipt/participant ledger before materialization or delivery.

Full Applied still requires the exact same PreparedParticipantRef/PreparedTransactionGID, Storage same-GID resolution, atomic VisibilityPointer/PublicationReceipt proof, C outcome, H authenticated evidence, I terminal receipt and D barrier. RestoreReconciliationReceipt is not a substitute. Historical Applied and current-use remain distinct; stale ContextVersion, DeliveryCursor, cache, ACK or session cannot bypass current I/D checks.

Limit: no production G restore/replay/adapter delivery integration is implemented/verified.