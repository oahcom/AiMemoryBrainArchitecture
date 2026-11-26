---
id: AID-2026-100
id_status: PROVISIONAL
title: "#1037 证据采集——完整克隆只读结果"
date: 2026-11-26
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
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "数据来自完整克隆上的本地只读执行，由用户提供；不是 CI。交接材料未提供 census 脚本精确调用命令和原始输出附件。"
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-100/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-100/evidence.md"
    zh-CN: null
---

# AID-2026-100 — #1037 证据记录（简体中文）

**署名：** user-authorized operator (delegated by account owner)  
**日期：** 2026-11-26  
**目的：** 关闭 Issue #1037 的两项证据类 BLOCKED；#1037 Issue 本身仍保持 OPEN。


## 证据来源与执行环境

以下测量值由用户提供，来源为**完整克隆**上的本地只读执行，**不是 CI**。此前 partial clone 上创建 worktree 失败，只描述先前 VM 的采集尝试；本次完整克隆采集结果取代其作为这两项证据的来源。

- 平台：Windows
- Python：3.12.3
- 环境变量：`PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`
- 克隆：完整历史；对 `c6b7d987`、`cb4b36d0`、`dc826e4e` 执行 `git cat-file -t` 均返回 `commit`
- Worktree：分别 detached 于 `c6b7d987b959c42af5072932963dae9ed55721e4` 和 `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706`
- 两个快照完全相同的 checker 命令：`python scripts/check_document_management.py`
- 扫描模式：全树扫描，不带 `--require-changed`

独立只读 census 脚本的精确调用命令未包含在所提供的采集记录中，因此下文将其标为 `NOT_PROVIDED`，不自行还原或猜测。

## 证据 A —— 全树 checker 采集

两个快照执行的命令：`python scripts/check_document_management.py`

| 项目 | Baseline `c6b7d987` | Fix `dc826e4e` |
|---|---:|---:|
| 退出码 | `2` | `2` |
| stdout 字节数 | 5443 | 5943 |
| stdout SHA-256 | `FCDDF7DE725A3676CD9AFAAA37EC897E8C6F4EBACBB49FF79814F591AC75CA8B` | `347292A4A6BD768A43DDE42FBD6DA8FAE01E1974DB3355C269B5922A1031F8DA` |
| stderr 字节数 | 230 | 230 |
| stderr SHA-256 | `EE34929E76B0FC03EE3842D206A7E9EC7695AB51CF87E34035287DC0A43CA92A` | `D4161D94B7EF4939374EAA80157553531176292BCE37BE528B9593CC77DCD926` |
| stdout 行数 | 50 | 55 |

**stdout 并非字节级相同**：5443 与 5943 字节，SHA-256 不同。两边退出码均为 `2`。

所提供结果中的 stderr 语义行如下（两边唯一差别是数字）：

- Baseline：`INCOMPLETE: no rule violations in 278 classified documents, but 484 governed documents are still unclassified`
- Fix：`INCOMPLETE: no rule violations in 293 classified documents, but 469 governed documents are still unclassified`

解释：两个快照都报告**没有规则违反**。退出码 `2` 表示 `INCOMPLETE`（全树分类尚未完成），不是执行失败，也不是 PASS。

上表字节数与摘要来自对完整原始 stdout/stderr 字节流的测量；但交接材料没有附上可单独下载的原始输出文件。因此本文记录所提供的哈希测量值，不声称附件中包含原始字节流。

## 证据 B —— stdout 逐行差异归因

所提供的 `Compare-Object` 摘要：**base 独有 8 行，fix 独有 13 行**。

Base 独有行：

```text
GOV-DOC-002: 762 governed documents, 278 classified, 484 unclassified
::notice::advisory (non-blocking): 121 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)
::notice::advisory (non-blocking):   139 distinct prose status value(s), 144 occurrence(s):
::notice::advisory (non-blocking):   (+129 more distinct value(s) not shown)
  01-system-architecture: 0/7 classified
  02-domain-model: 0/12 classified
  docs: 81/283 classified
  adoption backlog: ... ... (+479)
```

Fix 独有行：

```text
GOV-DOC-002: 762 governed documents, 293 classified, 469 unclassified
::notice::advisory (non-blocking): 117 governed document(s) carry a body '- Status:' line and no front-matter equivalent; DM-02 cannot see them (issue #481)
::notice::advisory (non-blocking):   135 distinct prose status value(s), 140 occurrence(s):
::notice::advisory (non-blocking):   (+125 more distinct value(s) not shown)
  01-system-architecture: 4/7 classified
  02-domain-model: 1/12 classified
  docs: 91/283 classified
  adoption backlog: ... ... (+464)
  authority: architecture/logical-system-component-map -> 01-system-architecture/component-map.md
  authority: architecture/subsystem-responsibility-matrix -> 01-system-architecture/responsibility-matrix.md
  authority: architecture/system-boundaries -> 01-system-architecture/system-boundaries.md
  authority: architecture/system-overview-guide -> 01-system-architecture/system-overview.md
  authority: domain-model/phase-1-domain-model-freeze -> 02-domain-model/phase-1-domain-model-freeze.md
```

所提供结果中的归因如下：

- Fix 输出新增 5 条 authority 绑定。
- 已分类文档：278 → 293（**+15**）：`01-system-architecture` +4、`02-domain-model` +1、`docs` +10。
- 未分类文档：484 → 469（**−15**）。
- Advisory 数量同步变化：正文含 body-status 的文档 121 → 117；不同 prose status 值 139 → 135；出现次数 144 → 140。

因此两个输出**不等价**；所报告的差异归因于上述分类变化和 authority 绑定变化。adoption backlog 行按交接材料原样保留（包含省略号）；本文不会补写被省略的条目。

## 证据 C —— fix commit frontmatter census

快照：fix commit `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706`。

执行方式：只读脚本遍历所有 `*.md` 文件并解析 YAML frontmatter。所提供采集记录未包含精确脚本调用命令：`NOT_PROVIDED`。退出码：`0`。

报告 JSON 的 SHA-256：`DD6A4CC1440A331EE984518C6D6306A7C233B0A4324DDBE9035EF95D309F15CC`。

| 指标 | 数量 |
|---|---:|
| `total_md` | 1020 |
| `with_frontmatter` | 294 |
| `no_frontmatter` | 726 |
| `malformed_frontmatter` | 0 |

`document_metadata.lifecycle.modification_status` 分布：

| 值 | 数量 |
|---|---:|
| `Unchanged` | 159 |
| `Modified` | 117 |
| `Pending-Reapproval` | 15 |
| `Active-Modified` | 2 |
| `None` | 1 |

`document_metadata.authority.normative_status` 分布：

| 值 | 数量 |
|---|---:|
| `Informative` | 241 |
| `Normative` | 52 |
| `None` | 1 |

**Pending-Reapproval = 15**，其中 **Normative 12**、**Informative 3**。逐项清单：

```text
Normative   00-governance/architecture-invariants.md
Normative   00-governance/design-principles.md
Normative   14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md
Normative   14-ai-development/adr/OWNER-RULING-ATTESTOR-ISSUER-SEPARATION-031.md
Informative 14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md
Normative   14-ai-development/PR-GOVERNANCE-001.md
Normative   14-ai-development/work-items/I-OWNER-DECISION-AUTHORIZATION-DECISION-001.md
Normative   docs/en/00-governance/architecture-invariants.md
Normative   docs/en/00-governance/design-principles.md
Normative   docs/en/14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md
Informative docs/en/14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md
Normative   docs/zh-CN/00-governance/architecture-invariants.md
Normative   docs/zh-CN/00-governance/design-principles.md
Normative   docs/zh-CN/14-ai-development/adr/OWNER-DECISION-FACT-CLAIM-001.md
Informative docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md
```

归并关系：5 份文档各有 3 个镜像（`architecture-invariants`、`design-principles`、`OWNER-DECISION-FACT-CLAIM-001`、`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）加上 2 份仅存在于 root 的文档（`PR-GOVERNANCE-001`、`I-OWNER-DECISION-AUTHORIZATION-DECISION-001`），合计 15。3 条 `Informative` 记录是同一条 governance-register 记录的 root/EN/ZH-CN 镜像，与 Issue 先前评论一致。

上面记录了报告摘要的 digest。完整 JSON 原始清单未包含在交接材料中，因此本文不声称已附加该文件，也不虚构文件路径。

## 证据 D —— 增量模式对照（补充材料，不构成等价证明）

命令：`python scripts/check_document_management.py --require-changed c6b7d987b959c42af5072932963dae9ed55721e4`。

| 快照 | 退出码 | stdout | stderr |
|---|---:|---|---|
| `c6b7d987` | `3` | 0 字节；SHA-256 `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` | `NOT_APPLICABLE: --require-changed resolved to zero changed or untracked paths; no incremental verification was performed` |
| `dc826e4e` | `0` | 7986 字节；SHA-256 `130A0B10EDBD11D0EFBA5D98955F399E3AFB93F3BE9A57C86770BE893B97FAAE` | 5261 字节；SHA-256 `4E7C397CD0900538EAC8E286D0FBFA75CCC8948A36997A20A1AFD9F258F28253` |

在 baseline 上，`--require-changed <baseline 自身>` 必然解析出零个变更路径。因此增量模式不能用作 baseline/fix 等价对照；证据 A 的全树扫描才是有效对照。Baseline stderr 的 SHA-256 对应 122 字节原始内容；fix stderr 为 5261 字节，并包含 Windows GBK 解码噪声，两者不可比较。证据 D 仅作补充。

## 解决状态与范围

- `byte-for-byte output equivalence`：作为一项证据问题，状态为 **RESOLVED**。证据并未证明字节相等；它证明 stdout 不同、两个退出码均为 2、两边均无规则违反，并由所提供的逐行差异报告归因已报告的变化。本文不声称“输出等价”。
- `fresh metadata recount`：由证据 C 的 fix-commit census 解决，状态为 **RESOLVED**。
- 来源：完整克隆上的本地只读执行，**不是 CI**。
- **#1037 的这两项证据已闭合。**
- **#1037 整体仍保持 OPEN**。Owner acceptance 及其他尚未完成的验收事项并未由本证据采集完成。
- 未修改 runtime、validator 或 workflow 语义。本 PR 保持 Draft，本任务不执行合并。
