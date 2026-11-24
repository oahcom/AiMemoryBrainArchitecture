---
document_metadata:
  domain: architecture
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Approved
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
      approved_version:
        scheme: git
        value: "a7d12fe9835d8f53403946ab08c1cae8c3f12fbf"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/design-principles.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "通常用于描述约束子系统设计的原则"
    usage_status: Active
    modification_status: Pending-Reapproval
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    # Translation of the authoritative source. It does not independently
    # claim canonical authority; see bilingual_counterpart below.
    canonical_status: Non-Canonical
    canonical_scope: "Architecture: design principles"
    canonical_scope_id: null
    canonical_scope_keywords:
      - principle
      - design-rule
      - boundary
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "00-governance/design-principles.md"
    en: "docs/en/00-governance/design-principles.md"
---

# 架构设计原则

- 文档 ID：GOV-PRINCIPLES-001
- 版本：1.0
- 源规范：[规范性原文](../../../00-governance/design-principles.md)
- 源版本：9792e189d63fbbc3694ab891fc4aeba5143b3b1c
- 对应英文：[Design Principles](../../en/00-governance/design-principles.md)
- 状态：DECIDED（已决议基线）

本文定义约束所有子系统设计的原则。

## P-01 — Brain 对记忆拥有权威

**DECIDED。** Brain 是 Canonical Memory 资产、其生命周期、来源链、关系以及自身管理的 Memory Context 的逻辑权威。Agent 可以提供遥测和事件，但不能定义 Brain 内部的记忆组织规则。

## P-02 — 独立于 Agent 和模型

**DECIDED。** Brain 不得依赖特定 Agent 框架、模型家族、模型供应商、Prompt 格式或推理 API。集成差异应由 Adapter 和协议能力协商处理。

## P-03 — 稳定且由 Brain 定义的契约

**DECIDED。** Brain 发布规范 Schema、语义、生命周期规则和同步契约。Agent Adapter 将 Agent 原生状态映射到这些契约。Brain 不会为了模仿每个 Agent 的私有实现而分叉自身架构。

## P-04 — 明确的领域语义

**DECIDED。** Event、Memory、Fact、Entity、Relation 和 Evidence 是不同对象。源事件可以支持一条记忆命题，但事件本身不是该命题。记忆可能处于不确定、被报告、推断、争议或撤回状态。

## P-05 — 从构造阶段保留来源链

**DECIDED。** 派生记忆必须保留可追踪的来源引用和派生元数据。在保留与隐私策略允许的范围内，摘要或压缩不得切断检查支持证据的能力。

## P-06 — 时间语义正确

**DECIDED。** 系统至少区分事件发生时间、接收/记录时间和有效时间。新命题不得静默抹去旧命题在历史上的有效性。

## P-07 — 意图不等于结果

**DECIDED。** 计划、目标、预测和待执行动作必须按其真实性质表示。没有结果证据，不得将它们提升为已完成事件或已验证事实。

## P-08 — 权威记忆与上下文分离

**DECIDED。** Canonical Memory 是持久化权威。Memory Context 是从权威资产构建的、针对特定任务和 Scope 的视图。上下文编辑不得修改权威记忆。

## P-09 — 在推理边界同步上下文

**DECIDED。** Brain 生成的上下文变更通过 Adapter 在明确的推理上下文组装边界生效。架构不得假设可以安全地改写正在执行的模型推理。

## P-10 — 明确的应用确认

**DECIDED。** Delivery、Receipt 和 Applied 是不同状态。Applied 必须有 Adapter 对指定 Context Version 的明确确认。这不能证明模型关注或正确使用了内容。

## P-11 — 记忆是数据，不是具有权威性的指令

**DECIDED。** 被检索或注入的记忆不能获得 System/Developer 指令权威。Brain 不得覆盖 System/Developer 指令、用户原始输入或 Agent 安全策略。

## P-12 — Scope 隔离

**DECIDED。** User、Project、Agent、Agent Instance、Session 和 Environment Scope 必须明确。不同游戏世界、存档等环境状态不得意外混用。

## P-13 — 遗忘必须受明确治理

**DECIDED。** 从工作上下文移除一个条目，不代表删除其 Canonical Memory。Forget/Retention 是独立的受治理流程，必须考虑派生数据、索引、缓存和备份。

## P-14 — 保留冲突，不得静默覆盖

**DECIDED。** 冲突命题必须保留其来源、时间范围、认知状态和解决历史。解决过程可以选择当前视图，但未经明确治理操作不得删除冲突记录。

## P-15 — 性能必须实测

**DECIDED。** 延迟、检索质量、资源消耗和 Agent 层面的收益必须在可复现条件下测量。在验证之前，任何性能倍数都不能作为架构事实。

## P-16 — 先定义逻辑架构，再确定部署拓扑

**DECIDED。** 子系统代表职责边界，不自动意味着独立进程、服务或 Rust Crate。部署和代码边界由契约及可测量的运维需求决定。
