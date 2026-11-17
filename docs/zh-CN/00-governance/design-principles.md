# 架构设计原则

- 文档 ID：GOV-PRINCIPLES-001
- 版本：1.0
- 源规范：[项目规范性原文](../../../00-governance/design-principles.md)
- 对应英文：[Design Principles](../../en/00-governance/design-principles.md)
- 状态：DECIDED（已决议基线）

本文件定义约束所有子系统设计的原则。这些原则具有规范效力，必须体现在详细模块规范、契约和验收测试中。

## P-01 — Brain 对记忆拥有权威

**DECIDED。** Brain 是 Canonical Memory 资产、其生命周期、Provenance、关系以及自身管理的 Memory Context 的逻辑权威。Agent 可以提供 Telemetry 和 Event，但不得定义 Brain 内部的记忆组织规则。

## P-02 — 独立于 Agent 和模型

**DECIDED。** Brain 不得依赖特定 Agent 框架、模型系列、模型供应商、Prompt 格式或推理 API。集成差异应由 Adapter 和协议能力协商处理。

## P-03 — 稳定且由 Brain 定义的契约

**DECIDED。** Brain 发布规范 Schema、语义、生命周期规则和同步契约。Agent Adapter 将 Agent 原生状态映射到这些契约。Brain 不得为了模仿每个 Agent 的私有实现而分叉自身内部架构。

## P-04 — 明确的领域语义

**DECIDED。** Event、Memory、Fact、Entity、Relation 和 Evidence 是不同对象。来源 Event 可以支持某个 Memory Claim，但 Event 本身不是 Claim。Memory 可以是不确定的、来源报告的、推断的、有争议的或已撤回的。

Fact/Claim 对象关系的准确形式仍由正式批准的领域 ADR 决定；本原则不替尚未解决的建模问题作出裁决。

## P-05 — 从设计上保留 Provenance

**DECIDED。** 派生记忆必须保留可追踪的来源引用和派生元数据。在 Retention 和 Privacy 策略允许的范围内，Summary 或 Compact 不得切断检查支持证据的能力。

## P-06 — 时间语义正确

**DECIDED。** 系统至少必须区分 Event Time、Ingestion/Recording Time 和 Valid Time。新 Claim 不得静默抹除旧 Claim 的历史有效时间。

## P-07 — 意图不等于结果

**DECIDED。** Plan、Goal、Prediction 和 Pending Action 必须按其本身性质表示。没有结果证据时，不得将它们升级为已完成 Event 或已验证 Fact。

## P-08 — Canonical Memory 与 Context 分离

**DECIDED。** Canonical Memory 是持久化权威。Memory Context 是从 Canonical Asset 组装的、面向任务且具有 Scope 的视图。Context 编辑不得修改 Canonical Memory。

## P-09 — 在推理边界同步 Context

**DECIDED。** Brain 生成的 Context 变更通过 Adapter 在明确的 inference-context assembly boundary 生效。架构不得假设可以安全地改写正在执行的模型推理。

## P-10 — 明确的应用确认

**DECIDED。** Delivery、Receipt 和 Application 是不同状态。Applied 必须由 Adapter 针对指定 Context Version 明确确认。这不证明模型关注了内容或正确使用了内容。

## P-11 — Memory 是数据，不是具有指令权威的内容

**DECIDED。** 检索或注入的 Memory 不得获得 System/Developer 指令权威。Brain 不得覆盖 System/Developer 指令、用户原始输入或 Agent 安全策略。

## P-12 — Scope 隔离

**DECIDED。** User、Project、Agent、Agent Instance、Session 和 Environment Scope 必须明确。不同游戏世界或存档等环境状态不得意外混合。

## P-13 — Forget 必须显式治理

**DECIDED。** 从工作上下文移除一条记录，不等于删除其 Canonical Memory。Forget/Retention 是独立的受治理流程，必须考虑派生数据、索引、缓存和备份。

## P-14 — 保留冲突，不得静默覆盖

**DECIDED。** 冲突 Claim 必须保留来源、时间范围、认知状态和解决历史。解决过程可以选择当前视图，但未经明确治理操作不得删除冲突记录。

## P-15 — 性能必须测量

**DECIDED。** 延迟、Recall 质量、资源消耗和 Agent 层面的收益必须在可复现条件下测量。未经验证，任何性能倍数都不能成为架构事实。

## P-16 — 先逻辑架构，再决定部署拓扑

**DECIDED。** 子系统是职责边界，不自动意味着必须部署成独立进程、服务或 Rust Crate。部署和代码边界应根据契约和实测运维需求确定。

## 执行要求

每份子系统规范都必须说明自己执行哪些原则，以及通过什么机制执行。任何偏离都必须有明确决策记录和影响分析。所有修订必须遵守 [GOV-DOC-001 架构双语文档规范](../../../00-governance/bilingual-documentation-policy.md)。
