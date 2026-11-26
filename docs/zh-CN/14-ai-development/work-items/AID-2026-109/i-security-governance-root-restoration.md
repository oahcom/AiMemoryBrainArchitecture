---
document_metadata:
  domain: security-governance
  role: review-report
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
        - "AID-2026-109 — bounded I source-root restoration audit"
        - "Source branch session-i-security-governance-2026-11-16 @ 8abddf814467b271344a9814613a6b7ca6a446c6"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Audit report and source blob readback; does not assert I Owner acceptance or production conformance."
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
    canonical_scope: "AID-2026-109 I security-governance source-root restoration audit"
    canonical_scope_id: "security-governance/aid-2026-109-i-root-restoration"
    canonical_scope_keywords:
      - security-governance
      - source-restoration
      - phase-freeze
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
---
# I 安全、身份与治理规范根受限恢复 — AID-2026-109

**署名：** `user-authorized operator (delegated by account owner)`  
**日期：** 2026-11-26  
**编号状态：** `PROVISIONAL`  
**提交前 fetch 的最新 main：** `a7e7c64bfd6c6d709a0a7b55358f94b8535815c1`  
**INDEX 编号核验：** 最大编号为 `AID-2026-108`；`AID-2026-109` 尚不存在，按规则分配下一号。  
**历史来源：** `session-i-security-governance-2026-11-16` @ `8abddf814467b271344a9814613a6b7ca6a446c6`

## 1. 从 F1–F8 推导恢复范围

当前 main 上的组合审查明确将 I 规范根缺失列为三个 Flow 的阻塞理由：

- **F4，第 180–181 行：** “I global policy root absent”；I 需要提供授权、保留与残余例外政策。
- **F6，第 218–219 行：** “I normative root absent”；Scope/Permission 模型尚未定义 policy 与 cache/revocation 保证；I 需提供 issuer、签名决策/attestor、PermissionEpoch、撤销与缓存新鲜度及 verifier。
- **F7，第 237–238 行：** “I root absent”；D 明确将全局完成与物理擦除留给 I；inventory、backup/external-copy 与 exception policy 尚未接受。

F1–F3、F5 没有把 I 规范根缺失列为其主要阻塞原因。F8 是 Storage/Consistency 的物理原子性、耐久性、崩溃与恢复缺口，不属于 I 规范根缺失。

**文件名证据边界：** 审查文档明确将 `09-security-governance/README.md` 列为 `NOT_FOUND_ON_MAIN`；但 F4/F6/F7 的原因段落只写“I root”，并未逐一列出五个政策文件名。以下五份文件是本任务给定的候选文件，按 F4/F6/F7 的职责映射选取；不声称它们是 F4/F6/F7 引文逐字点名的路径。

## 2. 受限选择

源分支在 `09-security-governance/` 下共有 91 个文件。本次只恢复选定的五份源文档，并新增一个 README 导航根；不复制审计登记册、Phase 3.x 决策记录、自审记录、测试、参考模型或历史分支的其余文件。

## 3. 源 Blob / 恢复 Blob 对照

五份规范文件的原始正文完整逐字节保留。唯一新增前缀是 GOV-DOC-002 frontmatter；没有改写源正文。第三个 SHA 是新增 frontmatter 自身的 Git blob SHA。

| 恢复后的 Canonical 路径 | 源 Blob SHA | 新完整文件 Blob SHA | Frontmatter-only Blob SHA | 判定 |
|---|---|---|---|---|
| `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` | `9100061fa986fb6676656169de3fcf9fc1c72664` | `c0ba8b2dacc115e29233268e62d5ababfc26a025` | `a0740d117603891c0a9633d093bd01cb9a92f8cf` | CURRENT — Candidate / Informative |
| `09-security-governance/forget-retention-backup-and-erasure-policy.md` | `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` | `ab2b28829100ca1f2a17d203396b910fe3979bff` | `60b666d7b6ea38a9f2d70aa47744f3d076876e02` | CURRENT — Candidate / Informative |
| `09-security-governance/principal-actor-and-authorization-contract.md` | `03765efac4bb1153f303ce0030f9e277d602e81d` | `b8073340cb2efba990c038e0b628ee6e9d0f24da` | `d1b950f16ce89b8c23549c99bb885b0014a78dbf` | CURRENT — Candidate / Informative |
| `09-security-governance/scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` | `b4c66e90afdb57c5b60d37ad86554ccae6292e9a` | `9252258fa0a5f64e3cea75513da4e5e48d6c7847` | CURRENT — Candidate / Informative |
| `09-security-governance/security-and-identity-overview.md` | `26a990e44709d8604ae515a2a63b510400fd8471` | `e9c71b15e19e9289bffa4d98bdfe254cc66a0b83` | `fd42af80595cf8c4ef92795f64f5beacba38e7db` | CURRENT — Candidate / Informative |

README 是新编写的导航索引（源分支不存在 README blob），不是恢复的历史政策正文。

## 4. 取代性与权威判定

五份恢复文档均判定为 **CURRENT（当前可用的候选信息性材料）**，不代表当前规范性权威：

| 文档 | 对应缺口 | 判定 |
|---|---|---|
| global-forget-target-inventory-and-completion-evidence.md | F4 / F7 | CURRENT — Informative；I 全局 inventory、目标证据与完成政策 |
| forget-retention-backup-and-erasure-policy.md | F4 / F7 | CURRENT — Informative；I 保留、备份、外部副本与物理擦除政策 |
| principal-actor-and-authorization-contract.md | F6 | CURRENT — Informative；I 授权语义，B 仍拥有 ActorRef/ScopeRef 类型语义 |
| scope-and-revocation-policy.md | F6 | CURRENT — Informative；I policy、PermissionEpoch、撤销与缓存新鲜度 |
| security-and-identity-overview.md | F4 / F6 / F7 | CURRENT — Informative 概览；其中历史基线引用仅作为来源信息，不构成新的 main 版本 pin |

没有将任何候选文档标记为 `SUPERSEDED_BY`：检查未发现必须由 AID-2026-089 或 AID-2026-099 取代的权威主张。这不等于源文档已获批准。所有文件均保持 `decision_status: Draft`、`approved_version: null`、`normative_status: Informative`。本次恢复不产生任何 Owner acceptance。

## 5. 与 AID-2026-089 及 AID-2026-099 HIR-18 对齐

- **AID-2026-089：** D 是 ForgetOperation identity 与 ForgetFence generation/cursor 的唯一逻辑签发权威。恢复的 I 文档保留 I 的授权、全局完成与保留政策职责，不把 Fence 签发、lineage 权威或 canonical suppression 转交给 I 或 Storage。
- **AID-2026-099 HIR-18：** replay disclosure 必须独立重查当前 I authorization/PermissionEpoch/issuer status，以及当前 D Fence/lineage；任一拒绝或未知均阻止披露。I 文档仅提供候选政策语义。本次恢复不声称 HIR-18 已实现、已获跨 Owner 接受、cryptographic verifier 已就绪或 runtime 已符合。
- Storage 本地 Fence 记录仍只能是 D 派生、可重建的 projection；没有引入第二权威。

## 6. Gate A 与 Issue 状态影响

此前 I source-presence 子项因 `09-security-governance/README.md` 与 I 政策根缺失而为 OPEN。本次恢复后，该子项变为：

**RESTORED_CANDIDATE_SOURCE_PRESENT / INFORMATIVE — I Owner 精确版本验证与 acceptance 仍为 OPEN。**

这不关闭 Gate A。Gate A 仍为 PARTIAL / OPEN；Gate B 仍为 NOT VERIFIED。不声称存在自然人 Owner 签署、政策 ratification、实现 acceptance 或生产符合性。

## 7. #1211 COC / GID 加密封存证据边界

**未触及，仍需补齐。** 本次只恢复 I 治理源文档；没有恢复或验证 Storage/Consistency 的 COC/GID 源文档、加密封存证据、签名者/密钥托管、quorum、anti-rollback、durable-log/recovery、backup/restore 或生产拓扑。#1211 仍保持 OPEN。

## 8. 变更边界

不修改 03/04/05 域；不修改 Runtime/product code、Validator code 或 validator semantics、tests、scripts、workflows、schemas、APIs、DDL、部署或生产配置。不关闭任何 Issue。
