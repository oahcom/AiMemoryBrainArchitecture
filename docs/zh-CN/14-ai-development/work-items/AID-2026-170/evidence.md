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
        - "14-ai-development/work-items/AID-2026-170/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "两个被钉住的白名单 blob 均从本地对象库直接读取并逐行 diff；唯一改动的表格单元与其余 5c0e2049 钉点均按 origin/main 重新读取。未验证：哪一版 H schema 在规范上为当前版本，以及任何 Owner 签署。"
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
    canonical_scope: "SYS-RISK-001 的 I P0 白名单指针由 phase-3.8.9（5c0e2049）对齐到 Owner 指定的当前 phase-3.8.10（44986f5f）的证据"
    canonical_scope_id: "ai-development/aid-2026-170-sys-risk-001-p0-pin"
    canonical_scope_keywords:
      - sys-risk-001
      - p0-allowlist
      - pin-reconciliation
      - phase-3.8.10
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-170/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-170/evidence.md"
    zh-CN: null
---
# AID-2026-170 — SYS-RISK-001 的 I P0 白名单指针对齐

- 工作项：AID-2026-170；`id_status: PROVISIONAL`；`status: DISPATCHED`。
- 授权来源：user-authorized operator（由账户 owner 委托）；日期：2026-11-26。
- 建分支时的 main 基线：`8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`。
- 范围：两个 review 版本各改一个表格单元。不动白名单正文，不动任何其它钉点，不恢复 `phase-3.8.9`。

## 1. 所适用的裁定

派工说明记录了 Owner 的终裁：**current** 的 I P0 白名单是 `phase-3.8.10`（`44986f5f…`），`phase-3.8.9`（`5c0e2049…`）判为 `SUPERSEDED_BY`。本工作项把该裁定落到 `SYS-RISK-001` 中仍指旧钉点的两处。它登记的是一个受托裁定，不创造裁定，也不声称任何 Owner 签署。

## 2. 唯一改动的指针

`reviews/architecture/SYS-RISK-001.en.md` 第 297 行，改前：

```
| I | 28df608b075e619563c6367a8a1c171185c1faaf | 09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md | 5c0e2049513d391dfc118f4f629a5ec95de456d6 | I-owned P0 projection candidate; production profile, trust roots, key custody, anti-rollback and complete P0 vectors remain open |
```

改后：

```
| I | 28df608b075e619563c6367a8a1c171185c1faaf | 09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md | 44986f5f864bcdc1a79d34978273644d381a68c0 | I-owned P0 projection candidate; production profile, trust roots, key custody, anti-rollback and complete P0 vectors remain open; phase-3.8.9 Blob 5c0e2049513d391dfc118f4f629a5ec95de456d6 (SUPERSEDED_BY); reconciled_by: AID-2026-170 |
```

`reviews/architecture/SYS-RISK-001.zh-CN.md` 第 296 行，改前：

```
| I | 28df608b075e619563c6367a8a1c171185c1faaf | 09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md | 5c0e2049513d391dfc118f4f629a5ec95de456d6 | I-owned P0 projection candidate；生产 Profile、Trust Roots、Key Custody、anti-rollback 和完整 P0 vectors 仍未完成 |
```

改后：

```
| I | 28df608b075e619563c6367a8a1c171185c1faaf | 09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md | 44986f5f864bcdc1a79d34978273644d381a68c0 | I-owned P0 projection candidate；生产 Profile、Trust Roots、Key Custody、anti-rollback 和完整 P0 vectors 仍未完成；phase-3.8.9 Blob 5c0e2049513d391dfc118f4f629a5ec95de456d6（SUPERSEDED_BY）；reconciled_by: AID-2026-170 |
```

关于改动形状的两点说明：

- 该行的**路径**随 blob 一起改。若把 `phase-3.8.9-…-1.2.13….md` 留在路径列、把 `phase-3.8.10` 的 blob 放进 blob 列，就等于在一份只为精确性而存在的文档里制造路径/blob 不匹配。路径与 blob 是同一个指针，同格一并改动。
- 单元其余内容——owner HEAD `28df608b…`、"I-owned P0 projection candidate" 及其后每一条未完成项——逐字保留。旧钉点没有被抹掉：它在同一格里以显式 `SUPERSEDED_BY` 记录保留。

## 3. blob 身份与两个钉点之间的差异

| 钉点 | 完整 blob SHA | 对象大小 | 本次改动后的状态 |
|---|---|---|---|
| `phase-3.8.9` I P0 白名单 | `5c0e2049513d391dfc118f4f629a5ec95de456d6` | 20 906 字节 | `SUPERSEDED_BY` |
| `phase-3.8.10` I P0 白名单 | `44986f5f864bcdc1a79d34978273644d381a68c0` | 21 917 字节 | current |

直接从两个对象读出的差异：

```
git diff --text --stat 5c0e2049513d391dfc118f4f629a5ec95de456d6 44986f5f864bcdc1a79d34978273644d381a68c0
 1 file changed, 18 insertions(+), 11 deletions(-)
```

该 diff 的全部内容只有三类：

1. 版本串 `1.2.13` → `1.2.14`：出现在两行标题、§4、§12.1、§13（英文与中文）；
2. 头部 schema blob `8e7f6a6c9663388863db88548f9c37d0fdb1bd97` → `09fcd1fa29fe24255fbd87cae79dafb406594a59`（一处）；
3. 末尾新增 §14：记录 H 侧把 `forget_fence_generation_high_water` 加入 **D** 专属 high-water union，并明确 I 的五字段 high-water 对象与 I P0 不变。

§2–§12 的字段清单逐条相同。I P0 投影没有增删任何字段。

## 4. 为什么这不是语义变更，只是登记对齐

两个 blob 是同一份白名单、只差一个版本串：内容差异仅是允许列表所绑定的 H 版本、对应 schema blob，以及一条说明新增 D 字段不触及 I 命名空间与 I P0 的注记——因此把 `SYS-RISK-001` 重钉到 `44986f5f`，改变的是报告**指称哪一份工件**，不是报告**要求什么**；I 合同、字段集与未完成项清单都没有移动。

## 5. main 上其余仍钉 `5c0e2049` 的文件（列出，不改）

`git grep -n 5c0e2049 origin/main` 返回 4 个文件中的 5 行。§2 中的两行是 `SYS-RISK-001` 内仅有的两处；其余原样保留，待另一次裁定：

| 文件 | 行 | 该行是什么 |
|---|---|---|
| `14-ai-development/work-items/AID-2026-107/evidence.md` | 515 | phase-3.8.9 白名单的证据台账行，处置 `UNDECIDED`，理由 `U-OWNER-DECISION` |
| `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md` | 512 | 同一行的 EN 镜像 |
| `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md` | 512 | 同一行的 ZH-CN 镜像 |
| `reviews/architecture-feasibility/phase-2-contradiction-register.md` | 150 | "Resolution evidence" 句子（英文），引用 3.8.9 P0 blob |
| `reviews/architecture-feasibility/phase-2-contradiction-register.md` | 154 | 同一句的中文 |

两点观察仅记录、不处理：

- AID-2026-107 的行是带 `UNDECIDED` 处置的台账。在此翻转它等于改写另一个工作项的裁定状态，派工说明禁止。
- 矛盾登记册的句子描述的是**当时** ARC-02/03 证据如何被解决，是对一次过去 readback 的历史叙述，不是"当前 I P0"的指针，因此 Owner 裁定不机械适用于它们。

已钉 `44986f5f…` 的文件（`reviews/architecture-authority/2026-11-17/FINAL-A-002.{en,zh-CN}.md`、`SYS-RISK-002.{en,zh-CN}.md`、`reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md`）无需改动，也未改动。

## 6. 已执行的验证及其边界

已执行：

- `git grep -n 5c0e2049 origin/main` 与 `git grep -n 44986f5f origin/main`——上文的钉点清单。
- 对两个 blob 执行 `git diff --text --stat` 并通读完整 `git diff --text`——§3 的 18+/11- 与三分类是从对象读出，不是抄派工说明。
- 对两个改动文件执行 `git diff -U0`——每文件只改一行：2 files changed, 2 insertions(+), 2 deletions(-)。
- `git ls-tree -r --name-only origin/main`——main 上不存在任何 `i-p0-allowlists` 工件，也不存在根版本 `reviews/architecture/SYS-RISK-001.md`；EN 与 ZH-CN 两个版本即为全集，两者都已改动。

未执行、也不声称：

- 没有重新判定哪一版 H unified schema 在规范上为当前版本，没有 Owner 签署，没有 review。
- 两份白名单是分支工件，不是 main 路径。其路径按派工说明与 `FINAL-A-002` / AID-2026-107 台账所记引用；只按内容核验了它们的 blob 身份。
- 不声称关闭 SYS-RISK-001 的任何风险。R-01…R-10 以及 I 行中每一条"仍未完成"都未被触及。

## 7. 本次变更的文件

| 文件 | 动作 |
|---|---|
| `reviews/architecture/SYS-RISK-001.en.md` | 第 297 行：一个指针单元重钉，加入 `reconciled_by` |
| `reviews/architecture/SYS-RISK-001.zh-CN.md` | 第 296 行：同一改动，结构保持一致 |
| `14-ai-development/work-items/AID-2026-170/manifest.yaml` | 新增 |
| `14-ai-development/work-items/AID-2026-170/prompt-v1.md` | 新增——已执行提示词快照 |
| `14-ai-development/work-items/AID-2026-170/session-evidence.md` | 新增 |
| `14-ai-development/work-items/AID-2026-170/evidence.md` | 新增——本文件 |
| `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md` | 新增——EN 版本 |
| `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md` | 新增——ZH-CN 版本 |
| `14-ai-development/work-items/INDEX.md` | 追加一行 |
