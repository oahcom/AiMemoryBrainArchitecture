---
document_metadata:
  domain: memory-brain
  role: index
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
        - "03-memory-brain/README.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Bilingual mirror of a candidate root restored by AID-2026-100; content acceptance and semantic parity review remain pending."
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
    canonical_scope: "Bilingual mirror of 03-memory-brain/README.md"
    canonical_scope_id: "mirror/03-memory-brain/README"
    canonical_scope_keywords:
      - mirror
      - candidate
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "03-memory-brain/README.md"
    en: "docs/en/03-memory-brain/README.md"
    zh-CN: null
---

# Memory Brain — 阅读指南

- 文档 ID：D-READING-GUIDE-001
- 版本：1.0
- 英文对应：[Memory Brain Reading Guide](../../en/03-memory-brain/README.md)

## 推荐阅读顺序

1. [Memory Brain 总览](memory-brain-overview.md) — 权威边界、范围和 A–I 职责。
2. [Canonical Memory Store](canonical-memory-store.md) — 不可变版本、Commit 和 Outbox。
3. [Memory Lifecycle Manager](memory-lifecycle-manager.md) — Lifecycle 与 Epistemic Status 的区别，以及 Forget Operation。
4. [Entity 与 Relationship Manager](entity-and-relationship-manager.md) — 身份、类型化关系和 Merge/Split 历史。
5. [Memory Versioning](memory-versioning.md) — Revision、时间查询和并发。
6. [Canonical Commit 与 Cursor 语义](commit-cursor-semantics.md) — 不同 Cursor Namespace 的区别。
7. [Forget Fence 与完成契约](forget-fence-and-completion-contract.md) — D 拥有的抑制和证明边界。
8. [Forget Fence Operation 与 Publication Gate](forget-fence-operation-and-publication-gate.md) — 操作级线性化、竞争以及 JF-10/COC 决议。

## 权威与状态

D 拥有 Canonical Memory Identity/Version、Lifecycle 语义、Canonical Cursor 语义、Canonical Forget Operation/Fence，以及依赖/Barrier Evidence。D 不拥有全局授权、PermissionEpoch、Global Forget Completion、外部副本策略、物理擦除、BMCP Wire、ContextVersion 或 Agent 执行。

本指南中的 DECIDED 仅限 D 的领域权威。除非存在明确证据，跨模块实现、Storage 原子性、I Policy 和 Runtime Conformance 仍为 OPEN。

## 源版本纪律

每份文档都记录准确 Owner 分支和源 Blob SHA。将这些伴随文档作为实现基线前，必须重新查询 D 分支。翻译文档不等于合并或批准源分支。
