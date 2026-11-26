---
document_metadata:
  domain: ai-development
  role: work-item-evidence
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
      last_verification_note: "Source branch, mirrors and dispositions recorded; no I policy acceptance inferred."
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
    canonical_scope: "AID-2026-109 bounded I security-governance root recovery evidence"
    canonical_scope_id: "ai-development/aid-2026-109-i-root-recovery"
    canonical_scope_keywords:
      - security-governance
      - source-restoration
      - not-restored-by-decision
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
---
# AID-2026-109 — I 安全、身份与治理规范根受限恢复

**署名：** `user-authorized operator (delegated by account owner)`  
**日期：** 2026-11-26 · **编号：** `PROVISIONAL` · **main：** `a7e7c64bfd6c6d709a0a7b55358f94b8535815c1`

## 1. 审查推导

F4（审查第 176–193 行）、F6（214–231）和 F7（233–250）指出 I 规范根缺失及其职责。精确缺失路径清单（第 96–100 行）点名 `09-security-governance/README.md`；三个 Reason 段落没有列出具体策略文件名。审查允许 IMPL2/I 对规范根“恢复或正式处置”。

源分支在 `09-security-governance/` 下有 91 个文件，其中 81 份 Phase 记录。本次不导入整棵树。

## 2. Guide 来源判定

**`RECONSTRUCTED_FROM_MIRROR`，不是 restored。** 已检查源分支 Git tree，其中不存在 `09-security-governance/security-governance-guide.md`。main 已有 EN 镜像 Blob `061c5847b3df879eeaf3c71e5eae0bfa162b276a` 和 ZH-CN 镜像 Blob `372d27c79dc79d09bcdb0f142c979efdba1c2b6e`。新建 Canonical 正文与 EN 镜像逐字节一致，只增加 GOV-DOC-002 frontmatter；现有镜像不修改。

## 3. NOT_RESTORED_BY_DECISION

| 文档 | 源分支 Blob | 处置 | 理由 |
|---|---|---|---|
| `forget-retention-backup-and-erasure-policy.md` | `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` | `NOT_RESTORED_BY_DECISION` | Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file. |
| `global-forget-target-inventory-and-completion-evidence.md` | `9100061fa986fb6676656169de3fcf9fc1c72664` | `NOT_RESTORED_BY_DECISION` | Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file. |
| `principal-actor-and-authorization-contract.md` | `03765efac4bb1153f303ce0030f9e277d602e81d` | `NOT_RESTORED_BY_DECISION` | Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file. |
| `scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` | `NOT_RESTORED_BY_DECISION` | Four detailed policy docs require eight EN/ZH-CN mirrors in total; this translation work was not authorized and the review did not enumerate this detailed policy as a required root file. |
| `audit-and-exception-governance.md` | `0b5237f490066c7f95ebf4f5a5aa81edd8480bd4` | `NOT_RESTORED_BY_DECISION` | Not enumerated as required root content; outside bounded scope. |
| `governance-decision-register.md` | `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` | `NOT_RESTORED_BY_DECISION` | Historical decision register could revive dated decisions as current authority; outside bounded scope. |
| `threat-model-and-adversarial-test-plan.md` | `4227ac0e26228ca3504589efdee022b5d0802e12` | `NOT_RESTORED_BY_DECISION` | Not named as the missing normative root; outside bounded scope. |
| `security-and-identity-overview.md` | `26a990e44709d8604ae515a2a63b510400fd8471` | `NOT_RESTORED_BY_DECISION` | Guide reconstructed from existing mirror; restoring this additional historical overview would duplicate content and require more mirror work. |

前四份详细策略契约若全部恢复，需要额外八份 EN/ZH-CN 镜像。本次未获该翻译工作量授权，审查也未将这些详细策略逐一列为规范根必需文件。正式处置不表示其内容已存在于 main 或已获 I 接受。

## 4. Phase 记录前缀分类

81 份 Phase 记录全部排除。前缀统计：**phase-3: 1; phase-3.5: 1; phase-3.6: 30; phase-3.7: 1; phase-3.8: 47; phase-3.9: 1 (total 81)**。没有任何 Phase 记录被提升为当前规范性权威。

## 5. 权威与接受边界

- I 是策略语义接受权威；没有记录 I Owner acceptance。
- AID-2026-089：D 独占规范 ForgetOperation identity、ForgetFence generation/cursor 和 D 域完成谓词。I 不得签发/推进 D Fence，也不得重定义 D completion。
- AID-2026-099 HIR-18：replay disclosure 前独立重查当前 I authorization/PermissionEpoch/issuer validity 与当前 D Fence/lineage；拒绝/未知时 fail closed。
- README 与 Guide 均保持 Draft / Informative；`approved_version: null`。不声称规范性接受或生产符合性。

## 6. Gate A 与变更边界

Gate A 第 5 项中 I 子项从**规范根缺失**变为**规范根已撰写、指南已根据镜像重建、四份详细策略契约已正式处置**。这不等于“I policy semantics accepted”。Gate A 仍 PARTIAL / OPEN；Gate B NOT VERIFIED。

未修改 03/04/05、Runtime、validator semantics、tests、scripts、workflows、schemas、APIs、DDL、部署或生产配置。不关闭任何 Issue。
