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
        - "AID-2026-109 bounded I root and scope correction"
        - "main correction base 7629b9de5e5832fe486ee72d101c4bc5121015e6"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Informative root only; no I Owner policy acceptance or production conformance asserted."
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
    canonical_scope: "Language mirror of the informative I security-governance root and bounded source disposition"
    canonical_scope_id: "security-governance/root-index"
    canonical_scope_keywords:
      - security-governance
      - root-index
      - authorization
      - forget
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "09-security-governance/README.md"
    en: "docs/en/09-security-governance/README.md"
    zh-CN: null
---
# 安全、身份与治理

## 规范根范围

本目录是 I（Security, Identity & Governance，安全、身份与治理）域的规范性**信息根**。它确立领域边界并指向架构指南；它不发布或批准下列详细策略契约。

**策略语义接受权威：** I 是负责接受 I 域策略语义的领域 Owner。此处声明的是负责接受的权威归属，**不**表示 I 已接受任何策略。本规范根没有记录自然人 I Owner acceptance。

## 仍然有效的权威边界

- **AID-2026-089：** D 是规范 ForgetOperation identity、ForgetFence generation/cursor 和 D 域完成谓词的唯一逻辑权威。I 的策略职责不得签发/推进 D Fence，也不得重定义 D completion。
- **AID-2026-099 HIR-18：** replay disclosure 前，必须独立重查当前 I authorization / PermissionEpoch / issuer validity，以及当前 D Fence / lineage。拒绝或未知时 fail closed。本规范根不声称 HIR-18 已实现或符合要求。
- Storage 本地 Fence 数据（如存在）只能是 D 派生、可重建的 projection，不是第二权威。

## 架构指南

- [安全、身份与治理架构指南](security-governance-guide.md) — **RECONSTRUCTED_FROM_MIRROR**。历史源分支在该路径下没有 Canonical 指南。Canonical 正文逐字节取自现有 EN 镜像；现有 EN/ZH-CN 镜像正文保持不变。

## 四份详细策略契约 — NOT_RESTORED_BY_DECISION

以下每份文件均正式处置为 `NOT_RESTORED_BY_DECISION`：

- `forget-retention-backup-and-erasure-policy.md`
- `global-forget-target-inventory-and-completion-evidence.md`
- `principal-actor-and-authorization-contract.md`
- `scope-and-revocation-policy.md`

F4/F6/F7 审查段落指出 I 规范根缺失及其职责，并未将这四份详细策略文件逐一列为规范根必需内容。若恢复四份文件，需要额外八份 EN/ZH-CN 镜像。本次受限规范根决策未授权这项翻译工作量。该处置不表示详细策略内容已存在于 main 或已获 I 接受。

## 其他历史 I 文档 — NOT_RESTORED_BY_DECISION

- `audit-and-exception-governance.md` — F4/F6/F7 未将其列为必需规范根；超出受限范围。
- `governance-decision-register.md` — 历史决策登记册；导入可能使过时决策重新呈现为当前权威。
- `threat-model-and-adversarial-test-plan.md` — 历史威胁模型/测试材料，不是审查点名的规范根。
- `security-and-identity-overview.md` — 不恢复；使用现有架构指南作为唯一根级导览文档。此前的临时导入已由范围纠正 PR 删除。

## 历史 Phase 记录

源分支在 `09-security-governance/` 下共有 81 份 Phase 记录。它们按文件名前缀分类，统计见 AID-2026-109 证据报告，本次均不恢复。没有任何历史 Phase 记录被提升为当前规范性权威。

## Gate A 与剩余证据

Gate A 第 5 项中 I 的子项从**规范根缺失**变为**规范根已撰写、指南已根据镜像重建、四份详细策略契约已正式处置**。这不等于“I policy semantics accepted”。Gate A 仍为 PARTIAL / OPEN；Gate B 仍为 NOT VERIFIED。

**COC/GID 加密封存证据未触及，仍需补齐**（#1211）。本规范根不提供封存证据、签名者/密钥托管、quorum、anti-rollback、durable-log/recovery 或生产拓扑证明。

## 证据

源分支：`session-i-security-governance-2026-11-16` @ `8abddf814467b271344a9814613a6b7ca6a446c6`。

源 Blob、此前 main 临时导入 Blob、81 份 Phase 记录前缀统计及范围纠正历史，见 [AID-2026-109 范围纠正证据](../14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md)。
