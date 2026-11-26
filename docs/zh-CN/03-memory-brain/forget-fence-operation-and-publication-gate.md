---
document_metadata:
  domain: memory-brain
  role: reference
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
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "仅作机械路径/来源配对更新；ORPHAN_MIRROR_PENDING_DECISION 仍然有效。"
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
    canonical_scope_keywords:
      - 
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
# Forget Fence Operation 与 Publication Gate（遗忘栅栏操作与发布门）

- 文档 ID：D-FORGET-GATE-001
- 版本：1.0（拆分式双语伴随文档）
- 源分支：session-d-memory-brain-2026-11-16
- 源文件版本：AID-2026-150 已恢复规范源 `03-memory-brain/forget-fence-operation-and-publication-gate.md`；镜像状态仍为 `ORPHAN_MIRROR_PENDING_DECISION`，正式采纳或退役待 D Owner 明确裁决。
- 英文对应：[Forget Fence Operation and Publication Gate](../../en/03-memory-brain/forget-fence-operation-and-publication-gate.md)
- 源规范：[`03-memory-brain/forget-fence-operation-and-publication-gate.md`](../../../03-memory-brain/forget-fence-operation-and-publication-gate.md) 已恢复；本 ZH-CN 文档仍非权威，孤儿镜像的正式处置待 D Owner 裁决。
- 状态：D 语义契约为 DECIDED；E/Storage 执行、I 授权新鲜度和跨模块 Conformance 仍为 OPEN

源规范较长，拆分为四个中英并行阅读部分。源文件仍是规范性来源；拆分文档完整覆盖其章节。

1. [第 1 部分 — 规范性不变量、类型化证据与操作契约](forget-fence-operation-and-publication-gate-part1.md)
2. [第 2 部分 — 可见性边界、Evidence、故障矩阵与 Owner 决议](forget-fence-operation-and-publication-gate-part2.md)
3. [第 3 部分 — Phase 3.6 线性化、状态机与证明矩阵](forget-fence-operation-and-publication-gate-part3.md)
4. [第 4 部分 — Phase 3.6.2 JF-10 / COC 精确版本 Owner 决议](forget-fence-operation-and-publication-gate-part4.md)

**重要说明：** DECIDED 仅指 D 拥有的领域语义。它不表示 Storage 原子性已实现、E/F/G/H/I 执行已完成、JF-10 已可用于生产，或 Forget 已在全局/物理层面完成。
