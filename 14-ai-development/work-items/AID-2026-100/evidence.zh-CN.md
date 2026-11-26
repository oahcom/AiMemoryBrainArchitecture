---
id: AID-2026-100
id_status: PROVISIONAL
title: "#1037 证据采集——受阻"
status: DRAFT
date: 2026-11-26
authority:
  canonical_status: Non-Canonical
  normative_status: Informative
---

# AID-2026-100 — #1037 证据采集记录（简体中文）

**署名：** user-authorized operator (delegated by account owner)  
**日期：** 2026-11-26  
**状态：** `NOT_CAPTURED`；本记录不构成 #1037 的解决证据。

## 固定提交

- Baseline：`c6b7d987b959c42af5072932963dae9ed55721e4`
- Fix（#1221 merge）：`dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706`

已核实 fix commit 的第一父提交为指定 baseline。

## 采集失败

尝试执行：

```sh
git -C /home/ubuntu/ai-projects/AiMemoryBrainArchitecture worktree add <TMP>/ev1037 c6b7d987b959c42af5072932963dae9ed55721e4
```

实际输出（原文）：

```
Preparing worktree (detached HEAD c6b7d987)
fatal: unable to access 'https://github.com/oahcom/AiMemoryBrainArchitecture.git/': GnuTLS, handshake failed: The TLS connection was non-properly terminated.
fatal: could not fetch b5aab97ed03c822b08a98d59d0c3dca6697f447b from promisor remote
```

退出码：`128`。worktree 在从 partial-clone promisor remote 获取缺失对象时失败。这不是 checker 执行。原有源工作树存在 11 项预先存在的变更，本次未修改它们。

## 原始证据登记

| 证据 | 命令 | 退出码 | 原始输出路径 | SHA-256 | 状态 |
|---|---|---:|---|---|---|
| Baseline checker stdout | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Baseline checker stderr | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix checker stdout | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix checker stderr | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Baseline 命令元数据 | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix 命令元数据 | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |
| Fix frontmatter 原始清单 | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | NOT_CAPTURED | BLOCKED |

由于没有生成 checker 原始输出或 census 清单，因此不声称存在相应 SHA-256，也不能判断字节级等价。

## Frontmatter census

尚未在 fix commit 上执行完整 census。文档总数、frontmatter 字段出现次数、字段缺失数、受治理文档分类分布以及 Normative/Informative 数量全部为 `NOT_CAPTURED`。不以其他提交或历史报告的数据代替。

| 统计项 | 结果 |
|---|---:|
| 完整文档原始清单 | NOT_CAPTURED |
| 字段出现次数 | NOT_CAPTURED |
| 字段缺失统计 | NOT_CAPTURED |
| 受治理 / 已分类 / 未分类 | NOT_CAPTURED |
| Normative / Informative | NOT_CAPTURED |
| 原始清单 SHA-256 | NOT_CAPTURED |

## 处置结论

**#1037 仍为 BLOCKED，不得标记 RESOLVED。** 解决前必须取得 baseline 与 fix 两次 checker 的完整原始记录（命令原文、退出码、完整 stdout、完整 stderr、各输出 SHA-256），并取得 fix commit 的完整 frontmatter census 原始清单及其 SHA-256。

未修改 runtime/validator 语义，也未修改既有 workflow 语义；未合并、未关闭 Issue。
