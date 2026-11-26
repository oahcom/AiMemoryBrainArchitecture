---
document_metadata:
  domain: memory-context
  role: review-report
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-193/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "为原本无 front-matter 的镜像补 GOV-DOC-002 分类：仅记录 domain、role、状态与规范源路径（依据正文自述：G consumer acceptance record; restore is not Full Applied）；不主张规范权威，也不证明与源语义对等。补元数据前正文 blob：699ff1d3e396bfce7d6a81bd802e245818ee3c9b。"
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: "06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md"
    en: "docs/en/06-memory-context/phase-3.6.5-g-restore-reconciliation-consumer-acceptance.md"
    zh-CN: null
---
# G Owner — 精确 Restore Reconciliation / Context Delivery Consumer 验收

- Storage restore contract Blob：`4f656163aeba532a441eaed1d293a48e2363cb4a`
- I proof acceptance Blob：`85d62b8858fc86addacd3b83f49476e42f49b785`
- D proof acceptance Blob：`211e54acfb4573b1c51d96f07af297671dfc4c4b`
- A restore integration acceptance Blob：`fa5e066a208a64401c96a6b8790d8b53dc7f1585`
- 决策：**ACCEPT WITH G CONTEXT / APPLIED / DELIVERY RESTORE GATES**

G 接受：restore reconciliation 不等于 Full Applied、current-use authorization 或 delivery permission。在 materialization 或 delivery 之前，恢复的 Context snapshots、deltas、membership、materializations 和 delivery intents 必须与当前 COC prefix、I PermissionEpoch/revocation/registry high-water、D Forget/lineage barrier 以及 Storage pointer/receipt/participant ledger 完成 reconciliation。

Full Applied 仍要求精确的同一 PreparedParticipantRef/PreparedTransactionGID、Storage same-GID resolution、atomic VisibilityPointer/PublicationReceipt proof、C outcome、H authenticated evidence、I terminal receipt 和 D barrier。RestoreReconciliationReceipt 不能作为替代。历史 Applied 与 current-use 仍然不同；过期的 ContextVersion、DeliveryCursor、cache、ACK 或 session 不能绕过当前 I/D checks。

限制：尚未实现/验证生产环境的 G restore/replay/adapter delivery integration。
