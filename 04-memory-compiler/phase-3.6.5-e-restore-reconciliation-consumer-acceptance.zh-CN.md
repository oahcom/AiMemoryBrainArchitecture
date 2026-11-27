---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "从 Owner 源分支逐字节恢复；Owner 接受仍待定。"
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6.5-e-restore-reconciliation-consumer-acceptance.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-5-e-restore-reconciliation-consumer-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-5-e-restore-reconciliation-consumer-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# E Owner — 精确恢复对账 / 编译器发布消费者接受

- Storage 恢复契约 Blob：`4f656163aeba532a441eaed1d293a48e2363cb4a`
- I 证明接受 Blob：`85d62b8858fc86addacd3b83f49476e42f49b785`
- D 证明接受 Blob：`211e54acfb4573b1c51d96f07af297671dfc4c4b`
- A 恢复集成接受 Blob：`fa5e066a208a64401c96a6b8790d8b53dc7f1585`
- 决策：**在满足 E 生产者 / 发布恢复门禁的条件下接受**

E 接受以下要求：恢复后的暂存制品、队列、outbox 和清单必须保持私有，直至完成对 COC 已提交前缀、当前 I 策略/撤销/注册表证明、D Forget/血缘证明以及 Storage participant/可见性账本的对账。RestoreReconciliationReceipt 不等同于 PublicationReceipt、VisibilityPointer 提交、Owner 最终门禁或 Full Applied 证明。

E 必须在恢复和重试期间保留相同的 PublicationOperationId/RequestDigest/PreparedParticipantRef/PreparedTransactionGID。AttemptId/LeaseEpoch 可以改变，但不可变元组不得改变。如果 Storage pointer 与 PublicationReceipt 的事务身份不一致，或者 D/I/COC 高水位过期，E 不得发布或暴露制品。任何迟到的派生项或 fence 生效后的生产者都必须保持阻塞。

限制：尚未实现/验证生产级 E 队列/outbox/manifest 恢复或发布门禁集成。
