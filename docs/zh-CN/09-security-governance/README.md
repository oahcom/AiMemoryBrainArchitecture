---
# provenance: AUTHORED_INDEX
document_metadata:
  domain: "security-governance"
  role: "guide"
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: {scheme: git, value: null}
      approval_scope: {type: Full-document, included_sections: [], included_assets: []}
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "provenance: AUTHORED_INDEX"
        - "directory inventory: 09-security-governance/"
        - "source branch: session-i-security-governance-2026-11-16"
        - "source commit: 8abddf814467b271344a9814613a6b7ca6a446c6"
        - "authoring date: 2026-11-26"
        - "executing operator: user-authorized operator (delegated by account owner)"
        - "no authoritative source; this file is a newly authored index"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "AUTHORED_INDEX; no authoritative source exists; this file is a newly authored navigation index. Owner review pending."
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
    canonical_status: Candidate
    canonical_scope: "现有安全与治理资料的新建导航索引；不是恢复的根规范"
    canonical_scope_id: "security-governance/directory-index"
    canonical_scope_keywords: ["documentation-index", "source-provenance", "governance"]
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Security, Identity & Governance — 目录索引

> **AUTHORED_INDEX — 非恢复的规范文件。** 不存在权威源；本文件为新建索引。在创建前检查中，根目录下没有现存源文档。

## 根目录清单

在本次变更前，`09-security-governance/` 下没有任何既有根级文档。本次新增的 README 是该目录唯一新增的根级文档。

## 现有双语资料

| 文档 | EN 镜像 | ZH-CN 镜像 | 状态 |
|---|---|---|---|
| Security, Identity & Governance Architecture Guide (DOC-SEC-001) | [英文指南](../../en/09-security-governance/security-governance-guide.md)，blob `061c5847b3df879eeaf3c71e5eae0bfa162b276a` | [中文指南](security-governance-guide.md)，blob `372d27c79dc79d09bcdb0f142c979efdba1c2b6e` | Candidate / Informative；I Owner 精确版本验收待完成；不构成生产安全认证 |

以上文件是现存镜像，仅作为导航目标列出。不得将其称为权威根源 blob。

## 治理边界

- I 负责全局身份/授权策略、委派与撤销、保留策略、审计治理、备份/外部副本策略、跨系统 Forget 治理评估策略、证据验收标准及物理擦除要求。
- D 继续拥有 canonical Forget 生命周期语义及其域完成谓词。本索引不重新定义该边界。
- D/E/F/G/H/C 保留各自本地执行机制及边界证据的所有权。
- 本索引不批准政策、不认证生产安全、不建立 canonical source，也不授予实施权限。
- 不得从 EN/ZH-CN 镜像的存在推断其具有权威源地位。

## 缺失权威来源与阻塞

- 未找到权威根 README 或根规范 blob；本文件为新建索引。
- 未取得精确源正文/frontmatter 和双语审查前，不在此恢复其他 I Owner 文档。
- I36-GOV-01..10 仍为 GOVERNANCE-BLOCKED，等待 approver、精确 policy hash/version、authority、scope 和 effective-time 证据。
- I Owner 精确版本审查及 Governance 验收仍待完成。
