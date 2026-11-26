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
        - "14-ai-development/work-items/AID-2026-098/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-098/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Prompt text is transcribed from the user request visible in this execution context; independent provenance and session identity are not verified."
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
    canonical_scope: "AID-2026-098 executed prompt snapshot"
    canonical_scope_id: "ai-development/aid-2026-098-prompt"
    canonical_scope_keywords:
      - storage-consistency
      - prompt-snapshot
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
﻿仓库：`oahcom/AiMemoryBrainArchitecture`。署名 `user-authorized operator (delegated by account owner)`，日期 2026-11-26；代理处置注明"代理登记，非自然人 Owner 签署"。直接读仓库动手。

## 任务：Storage/Consistency 物理合同候选规范
Gate A 的 F8 Storage Atomicity 在组合审查包（AID-2026-095，已合并）中标为 `BLOCKED_WITH_REASON`，缺"后端原子性、崩溃恢复、持久性证明"。把缺口写成可审查的候选合同：

1) 新建 `10-storage-consistency/` 下的候选规范（目录不存在则创建），覆盖：
   - 原子提交边界（哪些写入必须同事务、线性化点）
   - 崩溃恢复语义（WAL/检查点/重放顺序、部分写入判定）
   - 持久回执定义与最小字段
   - 可见性（提交后可读时点、隔离级别、读己之写）
   - 防回滚与 Fence 投影关系（引用 AID-2026-089 的 Forget Fence 单一权威，不得另立权威）
   - 与 D（canonical commit）、E（compiler 状态）、G（context 交付）的边界
2) 每条给 PASS/FAIL 检查点，并标 `DOCUMENTED_ONLY` / `EVIDENCE_REQUIRED`；
3) 三份文档 Canonical + EN + ZH-CN，结构一致，GOV-DOC-002 元数据齐全，状态 `Draft / Candidate / Informative`；
4) 新分支 + Draft PR；编号 **AID-2026-098**（`id_status: PROVISIONAL`；main 当前 096，097 已被 E/F 镜像预定）；
5) 在 #1212 与 #1180 各留一条评论说明落点与仍缺的实现证据。

回报：检查点条数、`EVIDENCE_REQUIRED` 计数、PR 链接、CI 结果、与 Forget Fence 权威一致性核对结论。
不改 runtime/validator，不合并、不关 Issue。