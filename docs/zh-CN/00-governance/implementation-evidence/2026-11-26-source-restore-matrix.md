---
document_metadata:
  domain: security-governance
  role: work-record
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
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "Bilingual evidence companion"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Draft evidence companion; CI and Owner review pending."
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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md"
    en: "docs/en/00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md"
    zh-CN: "docs/zh-CN/00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md"
---

- 源文件版本：a09ede9b70457b1dd0a42272b6e421557996ee8e
- 源规范：[规范证据记录](../../../../00-governance/implementation-evidence/2026-11-26-source-restore-matrix.md)（源 Blob `a09ede9b70457b1dd0a42272b6e421557996ee8e`）。

# AID-2026-11-26-SOURCE-RESTORE-02 — 规范源恢复证据矩阵

**main 基线：** `6314a65bd8be48c1a4bb0768e9960c4c808110ab`  
**D 源提交：** `b525e1f8fee2471a131e4a38efda99804045e424`

## D 逐文件证据

| 文件 | 原始源 Blob | 候选最终 Blob | 资格 |
|---|---|---|---|
| `03-memory-brain/memory-brain-overview.md` | `b4ed712ac0626ab127cccfd205c50a9013df01fb` | `3965c1e6c0810ac1850b75a6c08fb966610828e0` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/canonical-memory-store.md` | `6b37c91033fda21f072e2a3bde6f274663b1e76e` | `4d7d4db0585bb2e543881758bf27a8cbb0e323fa` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/memory-lifecycle-manager.md` | `8b972035b449e1eab546aedc9cc5b30581600c65` | `a644e6cb31d5674614f5edab9464cc03c2d7a077` | BLOCKED_OWNER_REVIEW |
| `03-memory-brain/forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | `d3ddfff9500d9138d643989e8496d99b8d9ed79e` | BLOCKED_OWNER_REVIEW |

四份源文件正文保持逐字节不变，仅在前面增加 GOV-DOC-002 元数据。原始源 Blob SHA 保留在元数据中。EN/ZH-CN 伴随文档正文保持不变，只更新元数据和源版本指针。Forget Fence 源继续保留四部分双语阅读材料。

## 治理变更

本 PR 将 `03-memory-brain` 加入双语门禁 normative roots 和 GOV-DOC-002 governed-root 登记，新增 D 规范源索引，并记录精确来源和镜像 Blob。源文件仍为 Candidate / Draft / Informative。本 PR 不声称 Owner 接受、Governance 批准或规范生效。

## 其他 Owner

F 仍需 F Owner 解决候选问题、接受精确版本并提供连续 watermark 覆盖证明。I 仍受治理批准阻塞。H 仍需精确核心规范清单、H Owner 接受和跨 Owner 依赖审查。本 PR 不恢复 F/I/H 文件。

## 校验

当前没有本地 Shell/工作区。本地 git 与 Python 门禁命令均为 NOT RUN；PR CI 和独立双语语义审查仍待完成。PR 为 Draft，未合并。
