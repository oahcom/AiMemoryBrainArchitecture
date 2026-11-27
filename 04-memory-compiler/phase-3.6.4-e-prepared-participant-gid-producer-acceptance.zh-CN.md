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
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6.4-e-prepared-participant-gid-producer-acceptance.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-4-e-prepared-participant-gid-producer-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-4-e-prepared-participant-gid-producer-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# E Owner — 精确 JF-10 Prepared Participant 身份 / GID 生产者边界接受

- Storage 协议 §14 Blob：`86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A 集成映射 Blob：`a71251704851cacd15f67faa985a5bd50057e92a`
- B 类型化引用注册表 Blob：`b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- H BMCP schema 1.1.1 候选 Blob：`c0bbfc7611a8d88a39cee209831db32b62601fde`
- 决策：**在满足 E 所有的生产者生命周期条件下接受**
- 模式：依照用户指示进行委托式 E 边界审查；不构成独立的人类签署。

E 接受新的 prepared participant 身份映射：

1. `PreparedParticipantRef` 与 `PreparedTransactionGID` 将一个不可变的 `PublicationOperationId`、`RequestDigest`、参与者摘要、WorkItem/DerivationRun/manifest 血缘、精确 Owner 边界、`CausalOrderDomainRef`、单一 `PolicyDomainRef` 以及 `CanonicalAuthorityDBRef` 绑定在一起。
2. Storage 负责分配并持久化稳定的 participant/GID 对。E **不得**创建 GID、按尝试轮换 GID、从 AttemptId 推导 GID，或在超时/重启后替换它。
3. 重试时 AttemptId 和工作器 LeaseEpoch 可以改变；PreparedParticipantRef、PreparedTransactionGID、PublicationOperationId、RequestDigest、manifest 摘要和 participant 元组不得改变。
4. COC prepare-intent 提交必须先于 Storage PREPARE。E 不得仅凭预分配就触发 Storage PREPARE 或发布制品。
5. `EngineNativeTransactionXIDRef` 是 PREPARE 之后产生的引擎证据；它不是 WorkItemId、PublicationOperationId、制品 ID、授权或重试身份。
6. D 生产者注册和屏障准入仍必须先于解引用/执行/发布。如果 D cutoff 先于 COC intent 生效，E 的工作必须保持阻塞且不得发生 PREPARE；如果 COC intent 先发生，D 必须在其屏障中跟踪同一个 PreparedParticipantRef。
7. 在 Storage 权威的同一 GID 决议及 VisibilityPointer/PublicationReceipt 原子事务完成之前，暂存制品必须保持私有。PreparedParticipantReceipt 本身不等同于发布。

例外：尚未实现生产级 E 账本、持久化队列/Outbox、工作器租约、制品存储或 Storage 适配器；预分配取消及同一 GID 恢复**尚未运行**。这仅是设计接受；JF-10 运行时 P0 仍为 OPEN。
