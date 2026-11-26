---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "AID-PENDING-MERGE"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Historical task-specific input capture. Its initial provisional AID-2026-080 allocation was superseded after the mainline collision was identified; this record is carried forward under AID-PENDING-MERGE without changing the embedded user instruction. The complete effective model payload remains NOT_VERIFIED."
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
    source: null
    en: null
    zh-CN: null
---

# Task-specific user instruction

﻿以人类 Owner 身份授权：为本次实施正式登记仓库标准 Work Item，解除 Session Evidence Gate 的阻塞。

要求：
1) 按仓库编号规则取下一个可用 AID（先查重，不得复用或伪造已有编号），为 `SOURCE-RESTORE-02` 与 `DECISION-ACCEPTANCE-03` 建立 Stage 0 注册与 manifest，并更新 INDEX；
2) 把外部工作流编号（`AID-2026-11-26-…`）保留为证据引用，不作为仓库标准 ID；
3) 提交到 PR #1220 同一分支，重新触发 Session Evidence Gate；
4) 回报：分配到的标准 Work Item ID、改动路径、CI 最新结果、剩余阻塞。
不合并、不部署、不关闭 Issue、不修改 validator 逻辑。


RENUMBERED_FROM: AID-2026-090; prior chain: AID-2026-080 (path reuse) → AID-2026-083 → AID-2026-090 → AID-PENDING-MERGE. Final AID assigned by merge queue at merge time.
