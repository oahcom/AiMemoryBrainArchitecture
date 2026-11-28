---
title: "frontmatter_blob_sha is a fragment digest, not a repository blob pin"
status: "OPEN"
classification: "contract-definition-gap"
discovered_at_commit: "daa935f7a7ecc808f1775be8cf153cf715961b08"
evidence:
  - "14-ai-development/work-items/AID-2026-109/manifest.yaml @ 9a2063ae1fa5d905b3817cd4eddba065a06daa73 (five frontmatter_blob_sha declarations)"
  - "09-security-governance/global-forget-target-inventory-and-completion-evidence.md @ 9a2063ae (frontmatter bytes, 45 lines between fences)"
  - "09-security-governance/forget-retention-backup-and-erasure-policy.md @ 9a2063ae"
  - "09-security-governance/principal-actor-and-authorization-contract.md @ 9a2063ae"
  - "09-security-governance/scope-and-revocation-policy.md @ 9a2063ae"
  - "09-security-governance/security-and-identity-overview.md @ 9a2063ae"
  - "scripts/ci/check_manifest_blob_pins.py @ 9a2063ae (emits UNCLASSIFIED for the five fields)"
  - "scripts/ci/check_manifest_blob_pins.py @ daa935f7a (no occurrence of frontmatter_blob_sha)"
related_baseline_ids:
  - "#20"
  - "#21"
  - "#22"
  - "#23"
  - "#24"
scope: "diagnostic"
---

# DEFECT-1 — `frontmatter_blob_sha` is a fragment digest, not a repository blob pin

> 本记录只陈述调查结果。**尚未裁定修复方案，不构成 checker 变更授权，也不构成 baseline 处置授权。**

## 1. 声明与对象

样本 commit：`9a2063ae1fa5d905b3817cd4eddba065a06daa73`
目标 commit（现状复核）：`daa935f7a7ecc808f1775be8cf153cf715961b08`

| 字段路径（AID-2026-109） | 声明值 | 是否为仓库独立对象 |
|---|---|---|
| `source.selected_source_files[0].frontmatter_blob_sha` | `a0740d117603891c0a9633d093bd01cb9a92f8cf` | 否 |
| `source.selected_source_files[1].frontmatter_blob_sha` | `60b666d7b6ea38a9f2d70aa47744f3d076876e02` | 否 |
| `source.selected_source_files[2].frontmatter_blob_sha` | `d1b950f16ce89b8c23549c99bb885b0014a78dbf` | 否 |
| `source.selected_source_files[3].frontmatter_blob_sha` | `9252258fa0a5f64e3cea75513da4e5e48d6c7847` | 否 |
| `source.selected_source_files[4].frontmatter_blob_sha` | `fd42af80595cf8c4ef92795f64f5beacba38e7db` | 否 |

## 2. 重算证据（5/5 命中，唯一字节定义）

```
algorithm = git blob sha1   (sha1("blob <len>\0" + bytes))
bytes     = 从文件首行 "---" 起，到闭合 "---" 行（含）为止的原始字节
            （含首尾 fence，含行尾换行，按文件原始换行符）
source    = 同级 restored_blob_sha 所指文件内容
```

对每条声明各测 21 种候选字节定义（7 种字节切片 × 3 种哈希：`git-blob-sha1` / `sha1(raw)` / `sha256`），只有上述一种命中。
7 种切片：frontmatter body（去 fence）、body + 尾换行、含双 fence、含双 fence + 尾换行、`strip()` 后的 body、LF 规范化后的 body、LF 规范化 + 尾换行。

**口径限定**：这是本轮调查的实测结果，**不等于契约已经定义**该字段的摘要对象、算法或作用域。

## 3. 语义结论（限定于已测事实）

- 声明值是有效的 Git-blob-sha1 摘要；
- 摘要对象是**文件 frontmatter 片段的原始字节**，该片段从不作为独立 Git 对象存在；
- 同 manifest 的 `source_blob_sha` / `restored_blob_sha` 指向完整文件，且为真实存在的 Git 对象。

## 4. checker 行为

- `9a2063ae`：`#1426` checker 报 `UNCLASSIFIED … source declaration has no blob_pins registration`（293 条中的 5 条）
- `daa935f7a`：tip checker 全文不含 `frontmatter_blob_sha`（字符串计数 0），不再报告
- **checker 停止扫描 ≠ 问题解决**

## 5. 契约缺口

- 全树（`9a2063ae`，md/yaml/yml/json/py）只有 `AID-2026-109/manifest.yaml` 出现该字段字样
- 没有任何文档定义该字段的摘要对象、算法或作用域

## 6. 未决问题（本记录不裁定）

1. 该字段是否应纳入 blob-pin 契约？
2. 若纳入，pin 的 locator 如何表达「文件内的片段」？
3. 若不纳入，是否需要显式标注「非仓库对象摘要」，以免再次被键名启发式命中？

## 7. 复现

```
git cat-file -e a0740d117603891c0a9633d093bd01cb9a92f8cf     # rc=1，对象不存在
git cat-file -e daa935f7a:14-ai-development/work-items/AID-2026-109/manifest.yaml
```
