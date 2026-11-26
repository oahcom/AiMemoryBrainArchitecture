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
        - "AID-2026-109 scope correction; main base 7629b9de5e5832fe486ee72d101c4bc5121015e6"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Records the correction to the merged AID-2026-109 scope; does not assert I Owner acceptance or production conformance."
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
    canonical_scope: "Language mirror of AID-2026-109 I root scope correction and restoration evidence"
    canonical_scope_id: "ai-development/aid-2026-109-i-root-restoration"
    canonical_scope_keywords:
      - security-governance
      - source-restoration
      - not-restored-by-decision
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-109/i-security-governance-root-restoration.md"
    zh-CN: null
---
# AID-2026-109 — I 规范根范围纠正与受限恢复证据

**署名：** `user-authorized operator (delegated by account owner)`  
**代理说明：** 代理登记，非自然人 Owner 签署  
**日期：** 2026-11-26  
**工作项：** AID-2026-109（`id_status: PROVISIONAL`）  
**纠正基线：** `7629b9de5e5832fe486ee72d101c4bc5121015e6`

## 1. 本次纠正的原因

PR #1300 将 AID-2026-109 合并为 merge commit `e3a134de856bbb58581fd688462c9c0282631270`。该临时版本恢复了五份历史 I 文档（四份详细策略契约和一份安全/身份概览）。之后用户进一步收窄范围：根据现有镜像恢复 Guide、在三个路径写 README，并对上述八份历史文档正式作出不恢复处置，而不是导入详细策略。

本 follow-up 删除五份临时导入的 Canonical 文档及其十份 EN/ZH-CN 镜像。保留已经合入的 I 根登记：`00-governance/document-scope-registry.yaml` 与 `scripts/check_bilingual_docs.py::NORMATIVE_ROOTS`。不修改 checker 逻辑或双语配对豁免规则。

PR #1301 是基于较旧基线创建的另一份 Draft 尝试；GitHub 当前记录其状态为 CLOSED 且 `merged=false`。本代理没有合并该 PR。本次纠正以 AID-110 合并后的当前 main 为基线。

## 2. 审查推导 — F4/F6/F7

2026-11-26 A–I + Storage 组合审查在 F4、F6、F7 中指出 I 规范根缺失。精确缺失路径清单点名 `09-security-governance/README.md`；F4/F6/F7 的原因段落描述了 I 的职责，但没有逐一列出下方八个历史文件名。审查允许采取“restore or formally disposition”。

- **F4：** I global policy root 缺失；授权、保留和残余例外政策职责仍待落实。
- **F6：** I normative root 缺失；Scope/Permission policy 与 cache/revocation 保证仍未明确。
- **F7：** D 将全局完成与物理擦除政策留给 I；inventory、backup/external-copy 和 exception policy 尚未接受。
- **排除 F8：** F8 是 Storage/Consistency 的物理原子性、耐久性、崩溃与恢复证据缺口，不是 I 规范根缺失。

## 3. Guide 来源

**分类：`RECONSTRUCTED_FROM_MIRROR`（根据镜像重建）。**

源分支 `session-i-security-governance-2026-11-16`（`8abddf814467b271344a9814613a6b7ca6a446c6`）中不存在 `09-security-governance/README.md`，也不存在 `09-security-governance/security-governance-guide.md`。

main 原有以下 Guide 镜像：
- EN 原完整文件 Blob：`061c5847b3df879eeaf3c71e5eae0bfa162b276a`
- ZH-CN 原完整文件 Blob：`372d27c79dc79d09bcdb0f142c979efdba1c2b6e`

新建 Canonical Guide 正文与 EN 镜像逐字节一致。现有 EN 与 ZH-CN Guide 正文也逐字节保持原样；只为两份镜像增加 GOV-DOC-002 frontmatter。

| Guide 路径 | 原始/源 Blob | 纠正 PR Blob |
|---|---|---|
| `09-security-governance/security-governance-guide.md` | 源分支：NOT_FOUND | `0c88125480f46b2bd264dd6fd8c1f92423edd531` |
| `docs/en/09-security-governance/security-governance-guide.md` | `061c5847b3df879eeaf3c71e5eae0bfa162b276a` | `70ba84ce1ccaf1bbd316e93728a6765de553e11a` |
| `docs/zh-CN/09-security-governance/security-governance-guide.md` | `372d27c79dc79d09bcdb0f142c979efdba1c2b6e` | `54cb0ae5cfe8278a2f22b9ebaeed2e591651cf37` |

Canonical Guide 与两份镜像均保持 Draft / Informative，且 `approved_version: null`。

## 4. NOT_RESTORED_BY_DECISION 登记

下表记录源分支 Blob；若此前 AID-109 临时合并曾导入该文件，也记录纠正前 main 的 Canonical 和镜像 Blob。纠正 PR 删除这些临时导入，使最终 main 状态真正符合“不恢复”。

| 文档 | 源分支 Blob | 纠正前 main Canonical Blob | 纠正前 EN 镜像 | 纠正前 ZH-CN 镜像 | 最终处置 |
|---|---|---|---|---|---|
| `forget-retention-backup-and-erasure-policy.md` | `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` | `ab2b28829100ca1f2a17d203396b910fe3979bff` | `e3bd438c76fb4ba7b2af8342dbbb1ef5c4dc6e86` | `8117fc33573ef743c23a5ab0e8d9f9ea65f78fd9` | `NOT_RESTORED_BY_DECISION` |
| `global-forget-target-inventory-and-completion-evidence.md` | `9100061fa986fb6676656169de3fcf9fc1c72664` | `c0ba8b2dacc115e29233268e62d5ababfc26a025` | `c453b8703a3dd93d5b1d0c5d3dc008d1afa53ebb` | `14d6b7c377ca9ce39c3c31372c55803d4ce0f69c` | `NOT_RESTORED_BY_DECISION` |
| `principal-actor-and-authorization-contract.md` | `03765efac4bb1153f303ce0030f9e277d602e81d` | `b8073340cb2efba990c038e0b628ee6e9d0f24da` | `eee995574ffda289e3ad29aa1919c09806f19057` | `fc127f028bca96c3bee21d8da8e51a0b508d1fe2` | `NOT_RESTORED_BY_DECISION` |
| `scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` | `b4c66e90afdb57c5b60d37ad86554ccae6292e9a` | `8eef867241bdb25c01d2f9b7332f7e485def101f` | `887949ca54745e6c30cf8e402da5229bab861032` | `NOT_RESTORED_BY_DECISION` |
| `audit-and-exception-governance.md` | `0b5237f490066c7f95ebf4f5a5aa81edd8480bd4` | NOT_PRESENT | NOT_PRESENT | NOT_PRESENT | `NOT_RESTORED_BY_DECISION` |
| `governance-decision-register.md` | `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` | NOT_PRESENT | NOT_PRESENT | NOT_PRESENT | `NOT_RESTORED_BY_DECISION` |
| `threat-model-and-adversarial-test-plan.md` | `4227ac0e26228ca3504589efdee022b5d0802e12` | NOT_PRESENT | NOT_PRESENT | NOT_PRESENT | `NOT_RESTORED_BY_DECISION` |
| `security-and-identity-overview.md` | `26a990e44709d8604ae515a2a63b510400fd8471` | `e9c71b15e19e9289bffa4d98bdfe254cc66a0b83` | `7764d0692d432979b02849fe865404ee4eed8768` | `1ba7a813a76b9b2c62e4431fe6419aaa9988a2a7` | `NOT_RESTORED_BY_DECISION` |

### 四份详细策略不恢复的理由

前四行是详细策略契约。若恢复四份文件，需要额外八份 EN/ZH-CN 镜像。该翻译工作量未获授权，F4/F6/F7 也没有将这些详细策略文件名逐一列为规范根必需内容。正式处置不表示其策略内容存在于最终 main 或已获 I 接受。

另外四份历史文件也正式处置为不恢复。概览文档因已有架构指南作为唯一根级导览而删除；审计登记、决策登记和威胁模型/测试计划均属于非必需历史材料。

## 5. Phase 记录前缀分类

源分支在 `09-security-governance/` 下有 91 个文件，其中 81 个符合 Phase 记录文件名模式。本次均不恢复。

| 文件名前缀 | 数量 |
|---|---:|
| `phase-3` | 1 |
| `phase-3.5` | 1 |
| `phase-3.6` | 30 |
| `phase-3.7` | 1 |
| `phase-3.8` | 47 |
| `phase-3.9` | 1 |
| **总计** | **81** |

## 6. 权威与接受边界

- I 是 I policy semantics 的指定接受权威；本次纠正不声称 I 已接受任何策略。
- **AID-2026-089：** D 仍是 ForgetOperation identity、ForgetFence generation/cursor 和 D 域完成谓词的唯一逻辑权威。I 不得签发/推进 D Fence，也不得重定义 D completion。
- **AID-2026-099 HIR-18：** replay disclosure 必须独立重查当前 I authorization/PermissionEpoch/issuer validity 和当前 D Fence/lineage；拒绝或未知时 fail closed。
- README 与 Guide 均为 Draft / Informative，`approved_version: null`。不声称存在 Owner acceptance、生产符合性或 HIR-18 实现。

## 7. Gate A 第 5 项与 #1211

Gate A 第 5 项中 I 的子项从**规范根缺失**变为**规范根已撰写、Guide 已根据镜像重建、四份详细策略契约已正式处置**。这是审查允许的“恢复或正式处置”路径，不等于“I policy semantics accepted”。Gate A 仍为 PARTIAL / OPEN；Gate B 仍 NOT VERIFIED。

**COC/GID 加密封存证据未触及，仍需补齐。** 本次纠正没有恢复或验证 COC/GID 加密封存证据、签名者/密钥托管、quorum、anti-rollback、durable-log/recovery、backup/restore 或生产拓扑。#1211 仍 OPEN。

## 8. 变更边界

本次纠正删除五份临时导入的 I Canonical 文档及其十份镜像，新增 Canonical Guide 与 README 三语版本，并更新 AID-2026-109 证据。未修改 03/04/05、Runtime、产品 validator semantics、tests、workflows、schemas、APIs、DDL、部署或生产配置。不关闭 #1211 或 #1212。
