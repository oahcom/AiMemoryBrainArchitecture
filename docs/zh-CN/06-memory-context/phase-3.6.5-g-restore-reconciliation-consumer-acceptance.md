# G Owner — 精确 Restore Reconciliation / Context Delivery Consumer 验收

- Storage restore contract Blob：`4f656163aeba532a441eaed1d293a48e2363cb4a`
- I proof acceptance Blob：`85d62b8858fc86addacd3b83f49476e42f49b785`
- D proof acceptance Blob：`211e54acfb4573b1c51d96f07af297671dfc4c4b`
- A restore integration acceptance Blob：`fa5e066a208a64401c96a6b8790d8b53dc7f1585`
- 决策：**ACCEPT WITH G CONTEXT / APPLIED / DELIVERY RESTORE GATES**

G 接受：restore reconciliation 不等于 Full Applied、current-use authorization 或 delivery permission。在 materialization 或 delivery 之前，恢复的 Context snapshots、deltas、membership、materializations 和 delivery intents 必须与当前 COC prefix、I PermissionEpoch/revocation/registry high-water、D Forget/lineage barrier 以及 Storage pointer/receipt/participant ledger 完成 reconciliation。

Full Applied 仍要求精确的同一 PreparedParticipantRef/PreparedTransactionGID、Storage same-GID resolution、atomic VisibilityPointer/PublicationReceipt proof、C outcome、H authenticated evidence、I terminal receipt 和 D barrier。RestoreReconciliationReceipt 不能作为替代。历史 Applied 与 current-use 仍然不同；过期的 ContextVersion、DeliveryCursor、cache、ACK 或 session 不能绕过当前 I/D checks。

限制：尚未实现/验证生产环境的 G restore/replay/adapter delivery integration。
