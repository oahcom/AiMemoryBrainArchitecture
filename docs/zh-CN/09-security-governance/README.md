---
document_metadata:
  domain: security-governance
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
        - "AID-2026-109 bounded I source-root recovery"
        - "Source branch session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Chinese navigation summary only; English source text is preserved verbatim below; full semantic translation parity is NOT_VERIFIED."
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
    canonical_scope: "Bounded I security-governance source-root navigation"
    canonical_scope_id: "security-governance/root-index"
    canonical_scope_keywords:
      - security-governance
      - source-root
      - navigation
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "09-security-governance/README.md"
---
# 安全、身份与治理

## 中文镜像状态

本页是 I 域安全治理文档的受限导航根。此中文镜像提供导航摘要；下方英文正文为原文逐字保留，完整中文逐段译文及语义一致性尚未完成独立审核。因此本镜像仅为 Informative，不构成中文规范性政策。

## 本次恢复范围

AID-2026-109 仅恢复由 F4、F6、F7 缺口映射出的五份政策/契约文档，并新增本导航页。未整体迁入 2026-11-16 历史分支的其余文件。五份文档各自的 frontmatter 均声明 `canonical_status: Canonical`。每份文档自身的 frontmatter 是其 `canonical_status` 的唯一权威来源；本 README 仅用于导读，不构成规范性来源。上述文档的存在不代表 Owner 已批准，也不代表生产实现已符合。

## 权威边界

- D 是 ForgetOperation identity 与 ForgetFence generation/cursor 的唯一逻辑权威；I 负责授权、保留、全局 inventory/completion 与物理擦除政策，不签发或推进 D Fence（AID-2026-089）。
- H replay disclosure 必须独立重查当前 I authorization 与当前 D Fence/lineage；任一拒绝或未知均 fail-closed（AID-2026-099 HIR-18）。
- Storage 本地 Fence 只能是 D 派生、可重建的 projection。
- 精确版本 Owner acceptance、实现证据与中文镜像语义审核仍未完成。

## 文档目录

- [全局 Forget 目标清单与完成证据契约](global-forget-target-inventory-and-completion-evidence.md)
- [Forget、保留、备份与擦除政策](forget-retention-backup-and-erasure-policy.md)
- [Principal、ActorRef 与授权契约](principal-actor-and-authorization-contract.md)
- [Scope 与撤销政策](scope-and-revocation-policy.md)
- [安全与身份概览](security-and-identity-overview.md)

---

## 英文源正文（逐字保留）


# Security, Identity & Governance

This is the bounded canonical entry point for the restored I-domain source set.

## Scope of this recovery

AID-2026-109 restores only five policy/contract documents selected against the I-root blockers in F4, F6 and F7 of the 2026-11-26 A–I + Storage composition review. It does **not** import the historical `session-i-security-governance-2026-11-16` tree wholesale. That branch contains 91 files under this domain; the other files are not restored by this work item.

这五份文档各自的 frontmatter 均声明 `canonical_status: Canonical`。每份文档自身的 frontmatter 是其 `canonical_status` 的唯一权威来源；本 README 仅用于导读，不构成规范性来源。这些文档在 main 上的存在不代表批准 Phase 3.x 决策，不代表批准生产策略，也不构成实现或符合性证据。

## Canonical I documents

- [Global Forget Target Inventory and Completion Evidence Contract](global-forget-target-inventory-and-completion-evidence.md)
- [Forget, Retention, Backup and Physical Erasure Policy](forget-retention-backup-and-erasure-policy.md)
- [Principal, ActorRef and Authorization Contract](principal-actor-and-authorization-contract.md)
- [Scope and Revocation Policy](scope-and-revocation-policy.md)
- [Security, Identity & Governance Overview](security-and-identity-overview.md)

## Authority boundaries that remain controlling

- **D is the sole logical authority** for ForgetOperation identity and ForgetFence generation/cursor. I owns authorization, retention, global inventory/completion policy and physical-erasure requirements; it does not issue or advance D's Fence. See AID-2026-089.
- **H replay disclosure independently rechecks current I authorization and current D Fence/lineage**, fail-closed. A historical receipt/signature is not current authorization. See AID-2026-099 HIR-18.
- Storage-local Fence data, if present, is a D-derived rebuildable projection, not a second authority.
- All five restored documents are `normative_status: Informative`, `decision_status: Draft`, and have no `approved_version`. Exact Owner acceptance and implementation evidence remain outstanding.

## Evidence

Original source branch: `session-i-security-governance-2026-11-16` @ `8abddf814467b271344a9814613a6b7ca6a446c6`.

Restoration and source/new blob comparisons are recorded in [AID-2026-109](../14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md).
