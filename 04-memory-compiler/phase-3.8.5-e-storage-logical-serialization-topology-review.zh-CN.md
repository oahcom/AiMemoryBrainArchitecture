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
      last_verification_note: "从 Owner 源分支恢复；Owner 接受仍待定。"
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
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.8.5-e-storage-logical-serialization-topology-review.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-8-5-e-storage-logical-serialization-topology-review"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-8-5-e-storage-logical-serialization-topology-review
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.8.5 — E 对 Storage 逻辑序列化拓扑的精确审查

- 审查方：E — Memory Compiler
- 分支：`session-e-memory-compiler-2026-11-16`
- 审查的精确 Storage ADR：`reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`
- ADR Blob：`1ef47d4e5711c7db73a24d249adf1992be1f6aa4`
- E Phase 3.8 发布契约：Blob `475fee41e5eea527af4edefbfe88c58c86967d0a`
- 决策：**在列明 E 所有条件下接受 — L1/L2 组合**
- 英文与中文为同等规范文本。

## 1. E 决议

E 接受 Option A 作为派生发布的规范逻辑序列化拓扑。它与 E 生命周期一致：D 注册先于队列/租约/源解引用/执行；不可变 Compiler Input 和 DerivationRun；私有暂存；完整依赖注册；Storage 隐藏式 prepare；D participant 准入；I 单次授权；Storage 最终可见性事务；D/I 在同一权威 Storage outcome 之后完成 closeout。

## 2. E 绑定条件

1. E 的 AcceptedReceipt 仅是本地入口证据，绝不能替代 D RegistrationReceipt。
2. 在 D RegistrationReceipt 持久化，且通过稳定 WorkItemId + 请求摘要完成解析之前，E 不得入队、取得租约、解引用受保护源或执行可派生工作。
3. 每个编译器输出都必须保持不可变和私有，直至完整依赖集合及精确的 D/I/Storage 门禁成功。
4. E 重试时保留 WorkItemId 和请求摘要；AttemptId/LeaseId/LeaseEpoch 按需变化。重新编译创建新的 DerivationRunId，但不能逃离原根屏障。
5. 共享的可串行化事务域不是 E 队列/工作器事务，也不会使队列 ACK 或本地 Published 状态成为权威。
6. Storage UNKNOWN、D fence UNKNOWN、I authorization UNKNOWN 或任何未解决参与者都会使制品保持私有、D 屏障保持打开。
7. 在未来实现选择并证明具体引擎之前，E 不得声称 DB 事务在物理上可用。这属于 L4，并非拒绝逻辑拓扑的理由。

## 3. L1/L2 组合

只要保持以下顺序，拓扑就不存在循环依赖：

Storage PREPARED_HIDDEN → D PublicationParticipantRef → I 已消费的 CommitAuthorizationReceipt / COMMIT_WON → Storage 最终可见性提交 → I 结果后终态证明与 D 终态回执。

I 的结果后终态证明不是 Storage commit 的前置条件。E 本地状态更新跟随 Owner 权威结果，不属于可见性线性化点。

## 4. E 最终处置

**在列明 E 所有条件下接受 — L1/L2 组合。**

E 接受 ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` 作为抽象架构。实际 DB 事务行为、队列/工作器实现、故障注入和部署均属于 L4。E 对当前所有 D/I/Storage Phase 3.8 工件的独立精确批准，仍是单独的 Owner 审查要求。
