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

AID-2026-109 仅恢复由 F4、F6、F7 缺口映射出的五份政策/契约文档，并新增本导航页。未整体迁入 2026-11-16 历史分支的其余文件。五份文档均在各自 frontmatter 中声明 `canonical_status: Canonical`；该字段以各自 frontmatter 为唯一权威，本 README 仅为导读，不是规范来源。它们的 `normative_status: Informative`、`decision_status: Draft` 保持原样；文档存在不代表 Phase 3.x 决策已获批准、生产政策已获批准或实现符合性已得到证明。

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

Each of the five documents declares `canonical_status: Canonical` in its own frontmatter. That field is authoritative; this README is a guide, not a normative source. Their `normative_status: Informative` and `decision_status: Draft` remain as recorded. Their presence does not ratify Phase 3.x decisions, approve a production policy, or establish implementation/conformance evidence.

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

## 中文侧内容状态：重要说明

以下五份文档虽然具有 `canonical_status: Canonical` 元数据，但当前 zh-CN 镜像尚未形成中文规范文本。其正文主要为英文内容，仅包含少量中文标题或说明，不构成完整中文翻译，也不应被视为已经提供中文规范文本。

涉及文档：

- `forget-retention-backup-and-erasure-policy.md`
- `global-forget-target-inventory-and-completion-evidence.md`
- `principal-actor-and-authorization-contract.md`
- `scope-and-revocation-policy.md`
- `security-and-identity-overview.md`

阅读和引用规范内容时，应以对应的 Canonical 原文为准。此说明不改变 Canonical 身份、文档效力或现有镜像关系。
