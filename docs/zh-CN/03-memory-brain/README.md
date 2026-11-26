---
document_metadata:
  domain: memory-brain
  role: index
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
        - "Issue #1177"
        - "D bilingual reading-guide companion"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Candidate source index; semantic mirror review pending."
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
    en: "docs/en/03-memory-brain/README.md"
    zh-CN: "docs/zh-CN/03-memory-brain/README.md"
---

# Memory Brain — 阅读指南

- 文档 ID：D-READING-GUIDE-001
- 版本：1.1
- 英文对应：[Memory Brain Reading Guide](../../en/03-memory-brain/README.md)

## 推荐阅读顺序

1. [Memory Brain 总览](memory-brain-overview.md) — 权威边界、范围和 A–I 职责。
2. [Canonical Memory Store](canonical-memory-store.md) — 不可变版本、Commit 和 Outbox。
3. [Memory Lifecycle Manager](memory-lifecycle-manager.md) — Lifecycle 与 Epistemic Status 的区别，以及 Forget Operation。
4. [Forget Fence Operation 与 Publication Gate](forget-fence-operation-and-publication-gate.md) — 操作级线性化、竞争以及 JF-10/COC 决议。

## 规范源文件集

规范源路径位于仓库根目录的 [03-memory-brain](../../../03-memory-brain/README.md)。四份源文件已作为候选材料放入本次 Draft 恢复 PR。D Owner 接受、必要的依赖 Owner 接受以及 Governance 批准尚未按最终 Blob 完成之前，它们保持 `canonical_status: Candidate` 和 `normative_status: Informative`。本目录中的英文和中文文件是阅读伴随材料，不是规范源。

## 权威与状态

D 拥有 Canonical Memory Identity/Version、Lifecycle 语义、Canonical Cursor 语义、Canonical Forget Operation/Fence，以及依赖/Barrier Evidence。D 不拥有全局授权、PermissionEpoch、Global Forget Completion、外部副本策略、物理擦除、BMCP Wire、ContextVersion 或 Agent 执行。

本指南中的 DECIDED 仅限 D 的领域权威。除非存在明确证据，跨模块实现、Storage 原子性、I Policy 和 Runtime Conformance 仍为 OPEN。

## 源版本纪律

每份伴随文档中的源指针都指向当前规范源 Blob。源正文绑定到 GOV-DOC-002 元数据中记录的 Owner 分支提交和原始 Blob。翻译或恢复本身不构成 Owner 接受。
