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
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/terminology.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "通常用于定义仓库内具有规范效力的术语"
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
    # Translation of the authoritative source. It does not independently
    # claim canonical authority; see bilingual_counterpart below.
    canonical_status: Non-Canonical
    canonical_scope: "Architecture: canonical terminology"
    canonical_scope_id: null
    canonical_scope_keywords:
      - terminology
      - glossary
      - definition
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
  bilingual_counterpart:
    en: "docs/en/00-governance/terminology.md"
---

# 规范术语表

- 文档 ID：GOV-TERM-001
- 版本：1.0
- 源规范：[项目规范性原文](../../../00-governance/terminology.md)
- 对应英文：[Canonical Terminology](../../en/00-governance/terminology.md)
- 状态：DECIDED（已决议基线）

本文件中的术语在本仓库内具有规范效力。子系统规范可以细化术语，但不得在没有明确决议的情况下重新定义术语。

| 规范术语 | 中文解释 | 不应混淆为 |
|---|---|---|
| Brain | 独立于模型和 Agent 的记忆权威及其服务 | Agent 规划器或编排框架 |
| Agent | 负责推理、规划、选择行动并调用工具或控制环境的系统 | Memory Brain |
| Adapter | 将 Agent 遥测映射为规范信号，并在推理边界应用 Brain 上下文变更的集成组件 | Brain 内部策略的所有者 |
| Event | 系统捕获的、有时间范围的发生、观察、报告或状态变化 | 持久记忆或已验证事实 |
| Memory | 从 Event、文档、用户输入等来源形成并保留、可寻址的知识资产 | 原始事件或必然为真的事实 |
| Fact / Claim | 关于实体、事件或状态，带有认知和时间限定的命题 | 来源证据本身 |
| Entity | 具有身份的对象，记忆和命题可以围绕其组织 | 一次文本提及或字符串出现 |
| Relation | 实体、记忆、事件或命题之间带类型、可能具有时间属性的关联 | 未经限定的文本共现 |
| Evidence | 支持、反驳或限定某个命题的来源材料或观察 | Confidence 分数 |
| Provenance | 记忆或命题可追踪的来源及派生历史 | 相似度分数 |
| Canonical Memory | 权威持久化记忆资产及其版本/历史 | 特定 Context 中的呈现形式 |
| Memory Context | 对选定记忆资产形成的、有范围和版本的任务化视图 | 整个记忆数据库或完整 Prompt |
| Context Entry | 某个 Memory Context 内对一条记忆的引用和呈现 | Canonical Memory 记录 |
| Applied Context | Adapter 确认已在约定推理边界应用的 Context 版本 | 模型已关注该内容的证明 |
| Working Set | 为低延迟使用而维护的、运行时本地且有容量上限的活跃记忆引用/数据集合 | 权威持久化存储 |
| Telemetry | 用于评估记忆需求和结果的结构化 Agent、任务和环境信号 | 完整隐藏思维链 |
| BMCP | Brain Memory Context Protocol：由 Brain 定义的遥测、上下文交付、确认和治理契约 | Agent 私有 API |
| Scope | 记忆或操作所属的命名空间/归属范围 | Permission |
| Permission | 对特定 Scope 资源执行操作的授权 | Scope 身份 |
| Epistemic Status | 命题被认知或获得支持的方式，例如 observed、reported、inferred、verified、disputed、retracted | Lifecycle State |
| Lifecycle State | 记忆资产的管理阶段，例如 candidate、consolidated、active、superseded、archived | 真实性状态 |
| Confidence | 按声明的方法估算或校准的支持程度 | Relevance |
| Relevance | 某条记忆在特定时间对特定任务/上下文的预期有用程度 | 真实性或置信度 |
| Event Time | 被描述事件实际发生的时间 | Ingestion Time |
| Recorded At | 系统记录或接收该内容的时间 | Event Time |
| Valid Time | 某项 Claim 被主张成立的时间区间 | 存储保留期限 |
| Forget | 针对 Canonical Memory 及适用派生物的受治理移除/去标识流程 | Context Remove |
| Consolidation | 在保留 Provenance 的前提下评估、合并、细化或关联候选记忆的过程 | 盲目去重 |

## 必须区分的概念

- **Epistemic Status（认知状态）**回答：“我们依据什么知道这件事？”
- **Lifecycle State（生命周期状态）**回答：“该资产处于哪个管理阶段？”
- **Confidence（置信度）**回答：“按声明的方法，这个命题获得多强的支持？”
- **Relevance（相关性）**回答：“这条记忆现在对当前任务有多大用处？”
- **Scope（作用域）**回答：“该资产属于哪个范围？”
- **Permission（权限）**回答：“谁可以对它执行什么操作？”

