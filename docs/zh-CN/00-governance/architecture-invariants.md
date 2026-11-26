---
document_metadata:
  domain: architecture
  role: normative-standard
  lifecycle:
    approval:
      decision_status: Under-Review
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
        - "00-governance/architecture-invariants.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "通常用于描述所有子系统规范必须遵守的约束"
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
    canonical_scope: "Architecture: system invariants"
    canonical_scope_id: "architecture/system-invariants"
    canonical_scope_keywords:
      - invariant
      - constraint
      - subsystem
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    source: "00-governance/architecture-invariants.md"
    en: "docs/en/00-governance/architecture-invariants.md"
---

# 架构不变量

- 文档 ID：GOV-INV-001
- 版本：1.1
- 源规范：[项目规范性原文](../../../00-governance/architecture-invariants.md)
- 对应英文：[Architecture Invariants](../../en/00-governance/architecture-invariants.md)
- 状态：CANDIDATE / Pending-Reapproval（当前版本未获批准）；I-01 至 I-24 尚无新的正式批准。

以下不变量是拟议的子系统规范和未来实现约束，仍须经过单独的正式批准。

| ID | 架构不变量 |
|---|---|
| I-01 | Brain 是 Canonical Memory 资产及其所管理 Memory Context 的逻辑权威。 |
| I-02 | Agent 不得定义或覆盖 Brain 内部的记忆组织规则。 |
| I-03 | Brain 独立于任何特定 Agent 框架、LLM 或推理供应商。 |
| I-04 | Event、Memory、Fact、Entity、Relation 和 Evidence 是不同的领域概念。 |
| I-05 | 每条派生记忆都必须保留到源 Evidence 的 Provenance；若无法提供，必须明确记录原因。 |
| I-06 | Intent、Plan、Prediction 和 Pending Action 不得自动视为已完成结果或已验证事实。 |
| I-07 | 编辑 Memory Context 不得直接修改 Canonical Memory。 |
| I-08 | 移除 Context Entry 不等于遗忘或删除其 Canonical Memory。 |
| I-09 | Context 变更必须版本化，并关联 base version，或明确执行 full-snapshot 转换。 |
| I-10 | 只有在 Adapter 明确 ACK 后，Context Delivery 才能标记为 Applied。 |
| I-11 | Context 变更必须在定义明确的 inference-context assembly boundary 生效。 |
| I-12 | Memory 内容是不可信数据，不得获得 system/developer instruction authority。 |
| I-13 | Scope 和 Permission 必须显式、独立执行；必须保持 Agent、task、session 和 environment 隔离。 |
| I-14 | 冲突 Claim 不得被静默覆盖；Provenance 和解决历史必须可审计。 |
| I-15 | Event time、recording time 和 validity time 不得混为一谈。 |
| I-16 | 状态变更协议操作的重试，必须在其定义的幂等范围内满足幂等性。 |
| I-17 | 每个 Context Version 必须具有唯一权威序列；并发变更必须串行化，或通过明确的并发控制解决。 |
| I-18 | Adapter ACK 证明协议层面的应用，不证明模型已经理解或遵循记忆。 |
| I-19 | Context Compact 必须保留来源引用；只要保留数据允许，还必须能够展开查看细节。 |
| I-20 | Forget 和 Retention 治理必须按声明的策略覆盖派生记录及二级表示。 |
| I-21 | 子系统边界不意味着必须部署为独立进程、服务或 Crate。 |
| I-22 | 性能声明必须基于明确声明的硬件、数据和负载进行可复现测量。 |
| I-23 | 每一项架构设计或改变架构语义的修改，都必须在同一个变更集中提供中文和英文文档；只有符合 GOV-DOC-001 的受治理临时例外才可暂缓。 |
| I-24 | 架构文档验收必须检查双语语义一致性、稳定标识一致性、决策状态一致性以及源版本可追溯性。 |

## 镜像补充章节——AID-2026-014 Claim/Fact 语义不变量

本节作为既有补充内容保留在此语言镜像中。当前规范原文 `00-governance/architecture-invariants.md` 没有对应章节，因此这些内容不会仅因出现在镜像中就成为规范不变量集的一部分；本节不修改或替代规范原文。是否将这些陈述纳入规范原文，须由相关内容 Owner 决定。

- Claim 与 Fact 是独立的规范对象。
- 保持命题身份的 Revision 之间必须保持稳定 Claim 身份。
- ClaimRevision 不可变，必须通过精确 ClaimRevisionRef 寻址。
- FactRevision 必须绑定准确 ClaimRevisionRef、Evidence、Provenance、Scope、Attestor 和 Method/Version。
- FactRevision 必须保留精确 I 授权决定引用。
- F 和 G 不得以当前 Head 或语义相似度解析替代精确历史 Revision 引用。
- Forget 检查必须覆盖共享 Fact 依赖及所有声明的替代读取路径。
- 以上是语义不变量，不构成 Schema、DDL、公开 API 或实现验收批准。

## 执行要求

每份子系统规范都必须说明自己负责执行哪些不变量、依赖哪些不变量，以及如何发现和处理违反不变量的情况。实现审查不得隐式豁免任何不变量；如需变更，必须提供明确的 ADR 和影响分析。

## 双语文档执行要求

所有架构 Owner 必须遵守 [GOV-DOC-001 架构双语文档规范](../../../00-governance/bilingual-documentation-policy.md)。任何临时 STALE 例外都必须明确登记、设置期限并持续跟踪。
