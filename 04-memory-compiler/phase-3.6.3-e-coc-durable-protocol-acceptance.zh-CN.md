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
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6.3-e-coc-durable-protocol-acceptance.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-3-e-coc-durable-protocol-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-3-e-coc-durable-protocol-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# E Owner — 精确 COC 持久化协议的生产者边界接受

- 精确 Storage 协议 Blob：`4ac63ac79491e79ec0c9114ef73941c73d7bbf25`
- A COC 架构 Blob：`a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- E JF-10 生产者接受 Blob：`4503628cf6f6ea46696ab14e7decd3e408ced19a`
- 决策：**在满足 E 所有的生产者生命周期条件下接受**
- 模式：依照用户指示进行委托式 E 边界审查；不构成独立的人类签署。

E 接受该协议作为生产者生命周期与恢复记账边界：

1. AcceptedReceipt 仅表示入口接收已持久化；它不等同于 D 生产者注册、执行许可或发布。
2. WorkItemId、PublicationOperationId、DerivationRunId、冻结清单摘要、源修订引用以及 Storage participant/XID 必须保持不可变绑定。
3. 重试可以改变 AttemptId/LeaseEpoch，但不得创建新的逻辑参与者、XID、操作 ID 或清单摘要。
4. D 生产者注册及完整依赖回执必须先于解引用、租约获取、执行和发布。
5. 在 Storage 权威的同一 XID PublicationReceipt 确认原子可见性事务之前，制品、嵌入向量、溯源信息和候选元数据必须保持私有。
6. COC 仅记录生产者/参与者生命周期观察结果。它不授权编译器执行、不裁定 D/I 结果，也不发布内容。
7. 未知/处于事务疑难状态的参与者，在重启、DLQ、租约过期和恢复后仍必须保持未结状态；不得通过 TTL 释放。

例外：目前尚未实现生产级 E 账本、队列/Outbox、工作器租约、制品存储或 Storage 适配器；COC/E/D/I 端到端测试**尚未运行**。这不表示编译器已实现、已部署到生产环境或已完成 Global Forget。
