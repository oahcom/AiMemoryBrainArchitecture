---
document_metadata:
  domain: security-governance
  role: decision-record
  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner delegate under Issue #305 comment 7042461592"
      decision_date: "2026-11-21"
      approved_version:
        scheme: git
        value: "e02848d7aa09aea8fce1fdd5bdf0e306f5a21d0b"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "GOV-DOC-002 DM-14 local verification on PR #438 pre-correction"
        - "00-governance/document-scope-registry.yaml"
        - "Issue #305 comment 7042461592"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "The local GOV-DOC-002 run counted 27 docs backlog files and reported the registry's 26 count as DM-14 failure."
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
    canonical_scope: "Governance decision: docs backlog count correction"
    canonical_scope_id: "security-governance/docs-backlog-count-correction"
    canonical_scope_keywords:
      - document-scope
      - backlog
      - dm-14
      - inventory
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Normative
---

# OWNER DECISION — DOCUMENT BACKLOG COUNT CORRECTION

- Decision ID: OWNER-DECISION-DOC-BACKLOG-COUNT-001
- Date: 2026-11-21 UTC
- Authority: Project Owner delegate under Issue #305 comment 7042461592
- Independence: INDEPENDENCE_UNVERIFIABLE; no independent human signature is claimed.

## Decision

The live repository count for the architecture-document backlog under docs/ (excluding docs/en, docs/zh-CN, and docs/governance/documentation-gaps.md) is **27**, not 26.

The registry count and the corresponding GOV-DOC-002 explanatory text are corrected to 27. This is a factual inventory correction only. It does not change the declared scope, the governed roots, the excluded directories, DM-14, or any classification rule.

The count was observed directly by the local GOV-DOC-002 checker on the PR #438 worktree. The checker reported 27 documents on disk and rejected the registry's declared count of 26.

## Mirror treatment

The machine-authoritative registry remains 00-governance/document-scope-registry.yaml. The docs/en and docs/zh-CN YAML copies are non-authoritative documentation mirrors only; repository tooling must continue to read the root registry. They are included solely to satisfy the repository's bilingual change-pairing contract.

## Acceptance and limits

- The root registry declares 27 docs backlog documents.
- The policy's English and Chinese count statements are corrected to 27.
- GOV-DOC-002 remains active and normative after this factual correction.
- No source code, CI workflow, test code, or Runtime implementation is changed.
- The local verification is a structural document-management check, not a claim that GitHub Actions ran or passed.

## 中文决策

# Owner 决策 — 文档积压数量更正

- 决策 ID：OWNER-DECISION-DOC-BACKLOG-COUNT-001
- 日期：2026-11-21 UTC
- 权威：Issue #305 评论 7042461592 授权的 Project Owner delegate
- 独立性：INDEPENDENCE_UNVERIFIABLE；不声称存在独立人工签名。

### 决策内容

当前仓库 docs/ 下的架构文档积压数量（排除 docs/en、docs/zh-CN 和 docs/governance/documentation-gaps.md）为 **27**，不是 26。

将范围登记表及 GOV-DOC-002 中对应的说明数量更正为 27。本次仅为事实性库存数量更正，不改变声明范围、受治理根目录、排除目录、DM-14 或任何分类规则。

该数量来自 PR #438 工作树上的本地 GOV-DOC-002 检查器实测。检查器报告磁盘上有 27 份积压文档，并因登记表仍声明 26 而触发 DM-14。

### 镜像处理

机器权威登记表仍为 00-governance/document-scope-registry.yaml。docs/en 和 docs/zh-CN 下的 YAML 副本仅为非权威文档镜像；仓库工具必须继续读取根目录登记表。创建镜像仅为满足仓库双语变更配对契约。

### 验收与限制

- 根目录登记表声明 docs 积压文档数量为 27。
- GOV-DOC-002 中英文数量说明均更正为 27。
- 本次事实更正后，GOV-DOC-002 继续有效且保持规范性。
- 不修改源代码、CI 工作流、测试代码或 Runtime 实现。
- 本地检查仅证明文档管理结构检查结果，不声称 GitHub Actions 已运行或通过。
