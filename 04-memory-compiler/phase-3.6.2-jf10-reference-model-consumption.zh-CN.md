---
document_metadata:
  domain: memory-compiler
  role: design-specification
  steward: USER-PRINCIPAL-DELEGATED
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
    canonical_status: Non-Canonical
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6.2-jf10-reference-model-consumption.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-2-jf10-reference-model-consumption"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-2-jf10-reference-model-consumption
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# E Owner — JF-10 可执行参考模型使用说明

- 状态：**参考模型映射 / 需要 Owner 审查**
- 模型来源：Storage Owner 分支，`reviews/storage-consistency/reference_model/jf10_linearization_model.py`
- 范围：仅涉及逻辑稳定身份与重试语义；不代表 E 的生产实现。

## 模型所表示的 E 所有行为

参考模型的 `ProducerManifest` 将一个 WorkItemId 绑定到一个不可变的 PublicationOperationId 和清单摘要。重复执行尝试可以改变 AttemptId，但不得改变发布身份。若将同一 WorkItemId 重新绑定到另一个操作，或更改其冻结清单摘要，则会被拒绝。

这是 JF10-E-16 所覆盖的逻辑行为。Storage 参与者模型也会将不可变操作和清单摘要带入可见性发布过程。

## 必需的生产映射

E 实现必须明确持久化冻结输出/血缘清单、WorkItemId 与 PublicationOperationId 的生成方式、AttemptId/LeaseEpoch 重试栅栏、清单摘要规范化，以及与 Storage 的精确交接点。E 不得仅凭生产者执行完成或暂存对象存在就声称已 Published。

## 明确不作的声明

此模型并未实现 E 的持久化编译账本、制品存储、清单规范化、重试调度器、租约服务或 Storage 集成。它不能证明 E36 或 JF10-E-16 已通过。仍需 E Owner 审查及生产等效证据。
