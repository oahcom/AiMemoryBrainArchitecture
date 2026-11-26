---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-109/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-109/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Verbatim user prompt body preserved below frontmatter; snapshot hash and byte count are recorded in the manifest."
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
    canonical_scope: "AID-2026-109 initiating user prompt snapshot"
    canonical_scope_id: "ai-development/aid-2026-109-prompt"
    canonical_scope_keywords:
      - prompt-snapshot
      - user-instruction
      - source-recovery
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

﻿#599 新任务：D（03-memory-brain）规范根的**受限恢复**

⚠️ 不要照搬整棵树。`session-d-memory-brain-2026-11-16`（head `b525e1f8`）上有 **60** 个文件，main 上 **0** 个。整棵搬进来会把 2026-11-16 的旧结论（很多已被 AID-2026-089 等后续裁决取代）重新变成现行规范——这正是项目最怕的"双权威"。

## 第一步：自己推导清单，不要用我猜的

读 `00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md`，找出 8 条流程（F1–F8）里所有把「D 规范根缺失」列为阻塞理由的段落，提取**它们具体点名的是哪几份 D 文档**。

我读到的线索（需你核实，不要照抄）：
- F2 说「D canonical store 规范根缺失」
- F3 说「D canonical feed 根也缺失，无任何源定义连续 watermark 证明」
- F4 说「D Fence 源为 Draft/Unverified/Informative 且不是 wire schema」
- F1 说「E Event Store 只是 candidate seam，accepted-receipt 与 producer-admission 两个规范根在 main 上缺失」

## 第二步：恢复

1) 只恢复被点名的 D 文档，从 `session-d-memory-brain-2026-11-16` **逐字节**取 blob，贴源 blob SHA vs 新 blob SHA 对照。
2) **每份都要做取代性判定**，在 evidence 里逐份写：`CURRENT` / `SUPERSEDED_BY AID-2026-089` / `CONFLICTS_WITH <具体裁决>`。凡判定为 `SUPERSEDED` 或 `CONFLICTS` 的，**恢复文件但不提升为现行权威**，在 frontmatter 里明确写 `canonical_status: Superseded` 或 `normative_status: Informative` 并在正文顶部加不可移除的取代声明。
3) 缺 frontmatter 的补 GOV-DOC-002 元数据，但记录「源 blob / 新 blob / 新增 frontmatter」三个 SHA，证明正文零改动。
4) 特别是 Forget Fence 相关：AID-2026-089 已确立「D 是唯一逻辑 Fence 权威」。恢复任何 Fence 文档时必须与该结论对齐，**不得恢复与之冲突的旧表述而不加取代声明**。

## 第三步：收口

5) 本机已确认 main 上 `03-memory-brain/` 目录**完全不存在**，所以这是纯新增，不会覆盖任何东西。
6) 编号：**推送时分配**。commit 前 `git fetch origin main`，读 INDEX，取 `^\|\s*\[AID-2026-(\d{3})\]` 的最大号 + 1。目前 107 与 108 已被别的会话预定，105/106 已合并。不要用 097/104。
7) 三份文档（Canonical + `docs/en/` + `docs/zh-CN/`，结构一致）。
8) 16 项全绿后自己合并，合并后核 blob。
9) 在 #1212 留评论：说明 D 规范根已恢复哪几份、哪些被标为 Superseded、Gate A 第 5 项（缺失的 D/E/F/I 规范根）中 D 的部分从 OPEN 变成什么。

回报：推导出的恢复清单（含"为什么这一份被点名"的引文）、取代性判定表、blob 对照、新编号、PR 链接、16 项、merge commit SHA、#1212 评论链接。
不伪造、不改正文、不动 04/05（归 #1220 与 E 会话）、不关 Issue。