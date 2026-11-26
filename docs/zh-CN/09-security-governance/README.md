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
        - "AID-2026-109 bounded I root recovery"
        - "main base a7e7c64bfd6c6d709a0a7b55358f94b8535815c1"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Informative root only; no I Owner acceptance or production conformance asserted."
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
    canonical_status: Canonical
    canonical_scope: "Informative I security-governance root, acceptance authority and bounded recovery scope"
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
    en: "docs/en/09-security-governance/README.md"
    zh-CN: "docs/zh-CN/09-security-governance/README.md"
---
# 安全、身份与治理

## 规范根范围

本文件是 I（Security, Identity & Governance，安全、身份与治理）域的规范性**信息根**，用于说明身份、授权策略、撤销、保留、审计治理、跨系统 Forget 政策和证据接受职责。它不是详细策略契约或生产安全认证。

**接受权威：** I 是负责接受策略语义的领域 Owner。此处仅声明应由谁接受，**不**表示 I 已接受任何策略。本文未记录自然人 I Owner acceptance。

- **AID-2026-089：** D 仍是规范 ForgetOperation identity、ForgetFence generation/cursor 和 D 域完成谓词的唯一逻辑权威。I policy 不得签发/推进 D Fence，也不得重定义 D completion。
- **AID-2026-099 HIR-18：** replay disclosure 前，必须独立重查当前 I authorization/PermissionEpoch/issuer validity 和当前 D Fence/lineage；拒绝或未知时 fail closed。本规范根不声称 HIR-18 已实现或符合要求。

## 架构指南

- [安全、身份与治理架构指南](security-governance-guide.md) — `RECONSTRUCTED_FROM_MIRROR`；源分支在该路径下没有指南 Blob；Canonical 正文逐字节取自现有 EN 镜像。

## 四份未恢复的详细策略契约

每项均正式处置为 `NOT_RESTORED_BY_DECISION`。F4/F6/F7 指出 I 规范根缺失及其职责，并未将以下四份详细策略文件逐一列为规范根必需文件。若恢复四份文件，需要额外八份 EN/ZH-CN 镜像；本次未获该翻译工作量授权，且恢复会错误暗示详细策略文本已存在并获接受。

- `forget-retention-backup-and-erasure-policy.md` — `NOT_RESTORED_BY_DECISION`；源 Blob `f14cb2149ca3f817229533005ab89dbdc7f0b3a8`。Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file.
- `global-forget-target-inventory-and-completion-evidence.md` — `NOT_RESTORED_BY_DECISION`；源 Blob `9100061fa986fb6676656169de3fcf9fc1c72664`。Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file.
- `principal-actor-and-authorization-contract.md` — `NOT_RESTORED_BY_DECISION`；源 Blob `03765efac4bb1153f303ce0030f9e277d602e81d`。Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file.
- `scope-and-revocation-policy.md` — `NOT_RESTORED_BY_DECISION`；源 Blob `71df6aaf21bb1767cd9fe5c947581b871325e023`。Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file.

## 其他未恢复的历史 I 文档

- `audit-and-exception-governance.md` — `NOT_RESTORED_BY_DECISION`；源 Blob `0b5237f490066c7f95ebf4f5a5aa81edd8480bd4`。Not enumerated as required root content; outside bounded scope.
- `governance-decision-register.md` — `NOT_RESTORED_BY_DECISION`；源 Blob `f5fd2558c657f4ef49396a7a00cdbcd0f226f853`。Historical decision register could revive dated decisions as current authority; outside bounded scope.
- `threat-model-and-adversarial-test-plan.md` — `NOT_RESTORED_BY_DECISION`；源 Blob `4227ac0e26228ca3504589efdee022b5d0802e12`。Not named as the missing normative root; outside bounded scope.
- `security-and-identity-overview.md` — `NOT_RESTORED_BY_DECISION`；源 Blob `26a990e44709d8604ae515a2a63b510400fd8471`。Guide reconstructed from existing mirror; restoring this additional historical overview would duplicate content and require more mirror work.

## 历史 Phase 记录

源分支在此目录下共有 81 份 Phase 记录，按文件名前缀的统计见 AID-2026-109 报告，本次均不恢复。没有任何历史 Phase 记录因本次工作被提升为当前规范性权威。

## Gate A 状态

Gate A 第 5 项中 I 的子项从**规范根缺失**变为**规范根已撰写、指南已根据镜像重建、四份详细策略契约已正式处置**。这不等于“I policy semantics accepted”。Gate A 仍为 PARTIAL / OPEN；Gate B 仍为 NOT VERIFIED。
