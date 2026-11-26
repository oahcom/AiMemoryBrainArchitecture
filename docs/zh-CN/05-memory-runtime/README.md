---
# provenance: AUTHORED_INDEX
document_metadata:
  domain: "memory-runtime"
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
        - "directory inventory: 05-memory-runtime/"
        - "source branch: session-f-memory-runtime"
        - "source commit: 1908ce4d233b20f7cafd00cb679affd01bd15174"
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
    canonical_scope: "现有 Memory Runtime 候选文档的新建导航索引；不是恢复的源规范"
    canonical_scope_id: "memory-runtime/directory-index"
    canonical_scope_keywords: ["documentation-index", "source-provenance", "governance"]
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Memory Runtime — 目录索引

> **AUTHORED_INDEX — 非恢复的规范文件。** 不存在权威源；本文件为新建索引。它仅盘点 2026-11-26 检查时根目录中存在的文档，不建立规范权威，也不代表 Owner 已验收。

## 本目录现有文档

以下五份源文档均为 Draft / Candidate / Informative。其源 blob 固定于 F Owner 分支，且存在双语镜像。逐版本语义审查及 F Owner 验收仍待完成。

| 文档 | 状态与待审事项 | 源 blob |
|---|---|---|
| [Runtime Overview](runtime-overview.md) | Candidate；语义一致性审查及 F Owner 验收待完成 | `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` |
| [Activation Policy Engine](activation-policy-engine.md) | Candidate；F Owner 验收及 watermark 证明待完成 | `b7f5d85468f5262e472769a1991b812ac4a64f5b` |
| [Retrieval Engine](retrieval-engine.md) | Candidate；逐版本语义审查及 F Owner 验收待完成 | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` |
| [Runtime Scheduling](runtime-scheduling.md) | Candidate；逐版本语义审查及 F Owner 验收待完成 | `ca35d8cddd012c1ff067328ee22177f57c40ae36` |
| [Working Set and Cache](working-set-and-cache.md) | Candidate；逐版本语义审查及 F Owner 验收待完成 | `a934491950c876701e8ac592a0e6aaea983b44e3` |

## 治理说明

- 本索引仅用于导航，不修改架构决策或 runtime 合约。
- Candidate / Informative 不等于 Approved 或 Normative。
- 源分支 blob 固定只能证明来源，不能证明已验收或符合生产要求。
- 存在双语镜像不等于语义等价已经得到证明。
- 不得仅凭本索引实现尚未解决的 API、schema、预算或跨 Owner 决策。
- 晋级需要 F Owner 对精确版本进行审查，并取得适用的跨 Owner / Governance 验收。

## 缺失来源与剩余工作

- 未找到权威根目录 README 源 blob；本索引为新建文件。
- F 清单 15 项中仍有 10 项缺少现存 EN/ZH-CN 配对，继续阻塞。
- F watermark / scanned-through 证据及逐版本 Owner 验收仍未完成。
