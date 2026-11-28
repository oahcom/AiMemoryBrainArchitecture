---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-348/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prompt snapshot is an authoring reference. Exact transmission provenance has not been independently verified."
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
    canonical_scope: "Repair instructions for AID-2026-348: GOV-NC-2026-11-21-GATE-DEADLOCK-006 mirror and section 11 status alignment."
    canonical_scope_id: "ai-development/aid-2026-348-prompt-v1"
    canonical_scope_keywords:
      - "AID-2026-348"
      - "prompt"
      - "governance-register"
      - "mirror"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# 角色

你是 `oahcom/AiMemoryBrainArchitecture` 的修复作者。无仓库读写权限，只输出逐字编辑块。

# 任务：三个独立的小修（同一 PR）

## A1. corpus-10：英文镜像仍称 `ACCEPTED`，Canonical 已记 `RESOLVED_ON_MAIN`

`14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md:47`（Canonical，中文）：

```
- 状态：`RESOLVED_ON_MAIN` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY`（Owner 2026-11-21 裁定，见 §14）/ 解除方式为自我审查合并，见 §12
```

`docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md:47`（英文镜像）：

```
- Status: `ACCEPTED` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY` (Owner ruling 2026-11-21, section 14) / the empty diff returned `EXIT=2` from `ae37a419` until `81dd9a72d2` (section 12)
```

`docs/zh-CN/...` 同路径那份已经是 `RESOLVED_ON_MAIN`，正确。

请给出英文镜像该行的替换块。要求：**保留** `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY` 与 section 14 的括注，把状态值改为与 Canonical 一致的 `RESOLVED_ON_MAIN`，并把后半句改成与 Canonical §12 同义的"解除方式为自我审查合并"（英文表达，不要丢 §12 引用）。不要新增别的行。

## A2. corpus-08 残留：三份 zh-CN 镜像缺 `Source revision`

实测（`origin/main`）：三份英文镜像的 `Source revision` 已与当前 Canonical blob 一致（OK）；**三份 zh-CN 镜像没有 `Source revision` 行**。

| Canonical | 当前 blob | en 镜像 | zh-CN 镜像 |
|---|---|---|---|
| `01-system-architecture/responsibility-matrix.md` | `7fc26ca93f4db3b5074156e76bee3555ac744e3a` | OK | 无该行 |
| `01-system-architecture/system-boundaries.md` | `8934b92bdaa89cf9697c7c4b14d15ca6dfca7328` | OK | 无该行 |
| `00-governance/design-principles.md` | `9fb729a4bd6ebcfa9576e5318804a65e2a95abe2` | OK | 无该行 |

英文镜像的头块长这样（`docs/en/01-system-architecture/system-boundaries.md` 附近）：

```
- Document ID: SYS-BOUNDARIES-001
- Version: 1.0
- Source: [Normative source specification](../../../01-system-architecture/system-boundaries.md)
- Source revision: 8934b92bdaa89cf9697c7c4b14d15ca6dfca7328
- Chinese counterpart: [系统边界](../../zh-CN/01-system-architecture/system-boundaries.md)
- Status: DECIDED where explicitly identified; CANDIDATE/OPEN items remain non-normative
```

**你需要先判断**：给 zh-CN 镜像加 `Source revision` 是不是正确的修法？如果 zh-CN 镜像正文与 Canonical 不是逐段对应（已知这五份 09 域镜像正文是英文原文；这三份 01/00 域的情况未知），那么加指针就是假证据。

因此：**先给出判定**（用一两行说明理由），再按判定输出块。若判定"不能加"，就输出 `===FILE: <path>|SKIP===` 并写清缺什么前置条件。

## A3. corpus-11：zh-CN README 比 Canonical 多 6 个章节

`09-security-governance/README.md` 的章节：

```
## Scope of this recovery
## Canonical I documents
## Authority boundaries that remain controlling
## Evidence
```

`docs/zh-CN/09-security-governance/README.md` 的章节：

```
## 中文镜像状态
## 本次恢复范围
## 权威边界
## 文档目录
## 英文源正文（逐字保留）
## Scope of this recovery
## Canonical I documents
## Authority boundaries that remain controlling
## Evidence
## 中文侧内容状态：重要说明
```

即 zh 侧有 6 个 Canonical 没有的章节（前五个 + 最后一个），且 Canonical 的 4 个英文章节被原样重复了一遍。

已知背景：这五份 09 域 Canonical 的中文镜像正文**实际是英文**（汉字占比 1.8%–4.5%），此前的处理是"披露而非翻译"，EN/ZH README 各追加过 14 行说明。所以这些额外章节可能是**有意的披露**，不是擅自扩张。

**你需要先判断**：这 6 个章节属于（a）合法披露、（b）越权新增规范、（c）两者混杂。给出判定依据（哪几段在陈述事实、哪几段在给出规范要求）。然后：
- 若 (a)：输出 `===FILE: ...|SKIP===` 并说明为何不改；
- 若 (b)/(c)：输出删除/改写的逐字块，保留必要的事实披露，去掉任何构成新规范要求的句子。

# 输出契约

```
===FILE: <仓库根相对路径>|REPLACE===
---OLD---
<逐字原文>
---NEW---
<逐字新文>
===END===
```

规则：`OLD` 必须逐字可匹配（含行尾）；一个文件多处改就给多个块；新增文件用 `|CREATE`；判定不改用 `|SKIP===` + 一行理由。先给 A2/A3 的判定，再给块，不要写计划。
