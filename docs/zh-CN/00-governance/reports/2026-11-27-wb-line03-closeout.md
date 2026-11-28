---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null

    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null

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
---

# WB LINE 03 Closeout（WB LINE 03 收尾）— Validator（验证器）/ Repository Governance（仓库治理）/ MCP（模型上下文协议）/ Local Environment（本地环境）

**记录类型：** 开发基线审计记录。非规范性、信息性。本记录不更改任何验证器、门禁、工作流、运行时、API、schema、wire 语义、工作项、INDEX 行、manifest 或 ledger 条目。
**状态：** `PARTIAL` — 每一行都包含可复现的命令和原始输出；无法确定的项目已在 §6 列出，不会被掩盖。
**本记录的基线：** `5670357db7a836d4f26838dbaf99494af41e2b65` (`Merge pull request #1423 from oahcom/governance/2026-11-27-merge-authorization-1325`)。分支 `docs/wb-line03-closeout-final`，从该 SHA 切出。
**编写时间：** 2026-11-27T15:05 (+08)，修订于 2026-11-27T15:20。下文各行的时间戳均为该行命令实际执行的时刻。
**主机：** Windows 上的 opencode 2.4.2，PowerShell；`git` CLI；GitHub GraphQL。经过身份验证的 REST core 配额为 `0/5000`，因此除未认证探测配额外，没有使用 REST 读取作为证据。

> **证据等级。** `VERIFIED` = 命令及其原始输出均记录在本记录中，且输出足以确定该主张。`UNVERIFIED` = 已测量，但该测量不足以确定该主张。`NOT_REPRODUCED` = 已测试该主张，但未能复现。`NOT_RECORDED` = 任何载体中都不存在相关记录。`NOT_VERIFIED` = 本轮未测试。
>
> **行号有效性。** 每个行号和 blob SHA **仅在** `5670357d` 上有效。审计期间 `main` 至少前进了四次（§1.2）。应运行该行命令重新推导，绝不能直接信任行号。

---

## 1. 基线、漂移与范围

### 1.1 审计开始时，指令指定的基线就已经过时

| # | 主张 | 来源 | Commit SHA | Blob SHA | 行 | 命令 | 原始输出 | 时间戳 (+08) | 等级 | 处置 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.1.1 | 指令将 `788fbc01…` 固定为 `main` | 指令文本 | `788fbc011877a14976fc0a974ffe2e013dd9991b` | — | — | — | `788fbc01…` | — | — | 基线已被取代；本记录的任何测量均未使用该基线。 |
| 1.1.2 | 阶段 1 期间 `main` 前进至 `987d2602…` | `origin/main` | `987d26021affbb5ba6d651e0fb5985d6bd4026a5` | — | — | `git merge-base --is-ancestor 987d2602 5670357d` | `exit=0` | 2026-11-27T14:56:26 | VERIFIED | 是本记录基线的祖先。 |
| 1.1.3 | 随后 `main` 到达 `6306a858…` | `origin/main` | `6306a858afc378f27448f8796c6b6604dfa240bb` | — | — | `git merge-base --is-ancestor 6306a858 5670357d` | `exit=0` | 2026-11-27T14:56:26 | VERIFIED | 是本记录基线的祖先。 |
| 1.1.4 | **本记录的基线** | 切出分支时的 `origin/main` | `5670357db7a836d4f26838dbaf99494af41e2b65` | — | — | `git log -1 --format=%s 5670357d` | `Merge pull request #1423 from oahcom/governance/2026-11-27-merge-authorization-1325` | 2026-11-27T14:56:26 | VERIFIED | 本记录中的所有 blob SHA 和行号均固定于此。 |
| 1.1.5 | 与指令基线的距离 | `788fbc01..5670357d` | — | — | — | `git rev-list --count 788fbc01..5670357d` | `520` | 2026-11-27T14:56:26 | VERIFIED | 指令提供的 SHA 落后 520 个提交。未经重新推导，不会重用指令提供的任何行号。 |
| 1.1.6 | 切出本分支**之后** `main` 再次移动 | GraphQL `repository.defaultBranchRef` | `7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19` | — | — | GraphQL `{repository{defaultBranchRef{target{...on Commit{oid}}}}}` | `main_oid 7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19` | 2026-11-27T14:58:25 | VERIFIED | 记录为漂移，并未对此作修正。本记录有意**不**追随 `main`。 |
| 1.1.7 | 仓库可见性 | GraphQL | — | — | — | GraphQL `{repository{isPrivate visibility}}` | `isPrivate=false`, `visibility=PUBLIC` | 2026-11-27T14:38 | VERIFIED | 自 2026-11-25 起为公开仓库。这解释了为何无需 token 即可读取某些历史 CI 事实；**不会**据此推断任何审查情况。 |
| 1.1.8 | 经过身份验证的 REST core 配额 | `GET /rate_limit` | — | — | — | （审计开始时读取） | `core 0/5000`; `graphql 4983/5000` | 2026-11-27T11:47 | VERIFIED | 后果：以下所有 GitHub 读取均通过 GraphQL 或未认证方式完成。本记录任何位置均未作出基于 REST 身份验证的主张。 |

### 1.2 本记录允许作出的主张

编写本记录期间，`main` 移动了四次。因此：

- 所有形式为“X 位于 `main`”的陈述，均指“X 位于 `5670357d` 的树中”。
- 每个 PR 状态均为该行所示时间戳返回的值。审计期间，`#1321` 和 `#1309` 均改变过状态；两种状态及其时间戳都已记录。
- 不对 `2026-11-27T14:58:25` (+08) 之后的 `main` 作出任何主张。

---

## 2. 发现登记表

每项发现均由一项主张及用于确定该主张的确切命令组成。各行按标识符排序，而非按重要性排序。

### F-01 — PR #1329 已合并；其实际合并 head 为 `11fde79a`，且 `2afe24cd` 是其祖先

| 字段 | 值 |
|---|---|
| 来源 | GraphQL `repository.pullRequest(number:1329)` |
| `state` / `merged` | `MERGED` / `true` |
| `mergedAt` | `2026-11-26T18:48:41Z` |
| `mergeCommit.oid` | `76684cb28b132917b3f250e9bf6430713e61c362` |
| `headRefOid` | `11fde79a8f07fac5176f67a2fdc633411570e87e` |
| `baseRefOid` | `de9f6e9646c5140fe9c9767b1fd2fe15cc38b022` |
| `headRefName` | `docs/aid-151-retroactive-gate-gap` |
| `author` / `mergedBy` | `oahcom` / `oahcom` |
| 合并父提交 | `git log -1 --format=%P 76684cb2` → `de9f6e9646c5140fe9c9767b1fd2fe15cc38b022 11fde79a8f07fac5176f67a2fdc633411570e87e` |
| `2afe24cd` 的关系 | `git merge-base --is-ancestor 2afe24cd 11fde79a` → `exit=0`; `git rev-parse 2afe24cd` → `2afe24cdb4d52ebed6f085f49b25ccec6ebda247` ≠ `11fde79a…`。**是祖先，不是 head。** |
| `f8236828` 的关系 | `git merge-base --is-ancestor f8236828 11fde79a` → `exit=1`。151 时期的提交**不在**已合并的 head 中。 |
| 合并提交可从基线到达 | `git merge-base --is-ancestor 76684cb2 5670357d` → `exit=0` |

时间戳 2026-11-27T14:56:27 / 14:38 (+08)。**等级：** VERIFIED。**处置：** 将指令中的“head `2afe24cd`”更正为 `11fde79a`；记录 `2afe24cd` 是该分支合并过程中经过的祖先。合并状态仅作为集成事实记录——不据此推断审批。

### F-02 — #1329 以 `AID-2026-174` 落地，且 `AID-2026-151` 从未存在于 `main`

| 观察项 | 值 | 命令 | 时间戳 (+08) | 等级 |
|---|---|---|---|---|
| `5670357d` 树中任何位置的 `AID-2026-151` | 不存在 | `git grep -n -I AID-2026-151 5670357d` → `exit=1`（无匹配） | 2026-11-27T14:56:28 | VERIFIED |
| `AID-2026-151/` 目录 | 不存在 | `git ls-tree 5670357d -- 14-ai-development/work-items/AID-2026-151/` → 空 | 2026-11-27T14:56:28 | VERIFIED |
| `AID-2026-151` INDEX 行 | 不存在 | 对 `c14118f8` 执行 `git cat-file blob` 并筛选 `AID-2026-151` → `0` 次命中 | 2026-11-27T14:56:29 | VERIFIED |
| `AID-2026-174/manifest.yaml` | `3f3831e592f82b678ae4fdf5149213eed6e430a4` | `git ls-tree 5670357d -- …/AID-2026-174/` | 2026-11-27T14:56:28 | VERIFIED |
| `AID-2026-174/prompt-v1.md` | `f11541445f5d36d46163fe30c5a07f8257f38693` | 同上 | 2026-11-27T14:56:28 | VERIFIED |
| `AID-2026-174/session-evidence.md` | `a716146d9869580aeb7308d886d237796173117c` | 同上 | 2026-11-27T14:56:28 | VERIFIED |
| `INDEX.md` | blob `c14118f854addbc59d9c12692b6b3f4ee9c8fe04`，323 行 | `git ls-tree`; `cat-file blob … \| wc -l` | 2026-11-27T14:56:29 | VERIFIED |
| `AID-2026-174` INDEX 行 | **L58** | 扫描 `AID-2026-174` 所在行 | 2026-11-27T14:56:29 | VERIFIED |

**等级：** VERIFIED。**处置：** “151”是仅存在于分支中的中间标识符；规范落地标识符为 **174**。未重新编号，未重命名任何内容。

### F-03 — `AID-2026-112` 已由 PR #1316（合并提交 `8722a37b`）占用，而已关闭的 PR #1309 仍声称拥有它

| 字段 | 值 |
|---|---|
| `main` 上的 `AID-2026-112/` | `evidence.md` `ab6d63a79f73c22d773cf5ac864cb4b796ca3a51`; `manifest.yaml` `f246832b6da0db0b3a051c59050efbb114379265`; `prompt-v1.md` `f9cebc35f81ecf47f2530c65aff26bedc553bb5c`; `session-evidence.md` `275a1ef457ddc8eb75af112faa563a691baf8074` |
| INDEX 行 | **L293**（blob `c14118f8`） |
| 占用该编号的 PR | GraphQL `pullRequest(1316)`：`MERGED`，`mergedAt 2026-11-26T13:48:07Z`，`mergeCommit 8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`，head `f9e399fc27c8914f6229c9fad50f938216cf0682` |
| 合并提交可从基线到达 | `git merge-base --is-ancestor 8722a37b 5670357d` → `exit=0` |
| 第二个认领方 | GraphQL `pullRequest(1309)`：`CLOSED`，`merged=false`，`closedAt 2026-11-27T04:31:22Z`，head `df192ede5384227ab516ec19a49b2a9094cf224e`，ref `docs/2026-11-26-aid-112-e-canonical-restore-batch-1` |
| 已关闭 PR 的 head 仍包含该目录 | `git ls-tree df192ede -- 14-ai-development/work-items/` → `040000 tree 86bdcae69ea16dd406a8f41d6449a9de9018e4ad 14-ai-development/work-items/AID-2026-112` |

时间戳 2026-11-27T14:38（GraphQL）/ 14:56:28 (+08)。**等级：** VERIFIED。**处置：** `main` 上的 `112` 属于 #1316。#1309 已**关闭且未合并**——它不再对 `main` 声称拥有 112，但其 head tree 仍包含一个 `AID-2026-112/`；如果它以后被重新打开并 rebase，就会产生 add/add 冲突。已记录；未采取行动。

### F-04 — `AID-2026-116` 现已通过 #1321 合并至 `main`；INDEX 行和 ledger 却仍称其为“open”

| 字段 | 值 |
|---|---|
| `main` 上的 `AID-2026-116/` | `evidence.md` `7804abe9b09c3bdd28b53eff4dc008fa87d89f39`; `manifest.yaml` `46ce54e62388a3306c3048c9738feddf23c495f2`; `prompt-v1.md` `c926c6ca9859f5c7fc8e548362af517f6cad2162`; `session-evidence.md` `75aa1261670279d4349a1ef807affda8807f999e` |
| INDEX 行 | **L72**，其状态单元格仍显示 `PR_OPEN` |
| PR | GraphQL `pullRequest(1321)`：`MERGED`，head `e61e714a978cd9f298d9216e990b1d8466e4bf93`，ref `gov/aid-116-pin-and-attribution` |
| Ledger | `origin/aid-ledger` head `5592658f12f02ada111ccd338600ad2e17d7d2f4`，blob `9020f0a27945fcc3657d7fd35ab9cb699ee41855`，L150-153：`state: OCCUPIED_BY_OTHER`，`carrier: "PR #1321 (gov/aid-116-pin-and-attribution)"` |

时间戳 2026-11-27T14:38 / 14:56:28 / 14:50 (+08)。**等级：** VERIFIED。**处置：** 三个载体与 `main` 的情况不一致——目录已合并，INDEX 行显示 `PR_OPEN`，ledger 则称该编号被另一工作项占用。更正文本见 §5，尚未应用。

### F-05 — `AID-2026-188` 已通过 #1337 合并，而分支 `renumber/1329-188` 仍试图创建同一目录

| 字段 | 值 |
|---|---|
| `main` 上的 `AID-2026-188/` | `evidence.md` `bd8bee389c78307407ef6292c5d3d18669359a50`; `manifest.yaml` `038a2e2935123e5a0f035d6a781c73a5d2e6cde6`; `prompt-v1.md` `c03204b6bf272c058a077985e606aac6a0020231`; `session-evidence.md` `035c5f2026c0af714653ba937655273e5eead87c` |
| INDEX 行 | **L299**，状态单元格为 `MERGED — PR #1337; merge f6ef2545913754da7859abfaad5559fdc68074ce` |
| PR | GraphQL `pullRequest(1337)`：`MERGED`，`mergedAt 2026-11-26T15:34:46Z`，`mergeCommit f6ef2545913754da7859abfaad5559fdc68074ce`，head `c1a485cb23161fa38cd5fd71f4cea937ce1e6fee` |
| 合并提交可从基线到达 | `git merge-base --is-ancestor f6ef2545 5670357d` → `exit=0` |
| 竞争分支 | `origin/renumber/1329-188` head `452285b9366cd26dd5fd23a86d77b061b0c94d95` (`fix(index): drop stale AID-2026-115 row duplicated by the main merge`) |
| 分歧 | `git rev-list --left-right --count 5670357d...origin/renumber/1329-188` → `868  5` |
| 该分支自己的 `AID-2026-188/manifest.yaml` | `99cc3460489215a35e7b8c16c5f136139c93ce18` — **≠** `main` 的 `038a2e29…` |
| Ledger | blob `9020f0a2` L181-183：`state: IN_FLIGHT`，`carrier: "PR #1337 (external)"` |

时间戳 2026-11-27T14:38 / 14:56:28 (+08)。**等级：** VERIFIED。**处置：** #1337 已合并；ledger 中的 `IN_FLIGHT` 已过时。若 rebase 并推送，renumber 分支会在 `AID-2026-188/manifest.yaml` 上产生 **add/add 冲突**。仅作记录；未重命名任何内容，未触及任何分支。

### F-06 — F-02 报告：`v2.11` 在 `main` 上取代了 `v2.10`；唯一残留的有效矛盾是 AC-15

| 观察项 | 值 | 命令 | 时间戳 (+08) | 等级 |
|---|---|---|---|---|
| 报告 blob | `8dd23ea35d1bce478073b7a122969f65c3e27e29` | `git ls-tree 5670357d -- 00-governance/reports/bilingual-baseline-remediation-report.md` | 2026-11-27T14:56:29 | VERIFIED |
| 行数 | `1472` | `git cat-file blob 8dd23ea3 \| split('\n')` | 2026-11-27T14:56:29 | VERIFIED |
| 声明版本 | **L50** 的 `v2.11` | 逐字节精确行扫描 | 2026-11-27T14:56:29 | VERIFIED |
| 作为声明版本的 `v2.10` | `Report Version: v2.10` 出现 `0` 次 | 同一扫描 | 2026-11-27T14:56:29 | VERIFIED |
| `v2.11` 修订说明 | **L1455-L1459**：“其存在的唯一原因，是 v2.10 留下的一个半修正状态……另有十处仍以现在时断言 F-02 Requirement 2 为 `NOT_VERIFIED`，或断言 F-02 整体为 `PARTIAL`” | 同一扫描 | 2026-11-27T14:56:29 | VERIFIED |
| 整个文件中的 `FAIL / BLOCKED` 出现次数 | **1** | `d.count(b"FAIL / BLOCKED")` | 2026-11-27T14:56:29 | VERIFIED |
| 该处出现位置 | **L869** `\| AC-15 \| Reproducible independent acceptance \| Review package and exact file SHAs recorded \| FAIL / BLOCKED — CI failure and outstanding findings \|` | 逐字节精确行扫描 | 2026-11-27T14:56:29 | VERIFIED |
| 对应的其他断言 | L505 `F-02 overall status: COMPLETE / VERIFIED`; L640 `F-02 overall COMPLETE / VERIFIED`; L968 `F-02 overall: COMPLETE / VERIFIED`; L1023 `No F-02 blocker remains`; L1164 `Required-check enforcement is COMPLETE / VERIFIED as of 2026-11-25`; L1180 过去时叙述；L1437-L1452 的 v2.11 注释本身 | 逐字节精确行扫描 | 2026-11-27T14:56:29 | VERIFIED |

**准确表述残留问题。** 在 `5670357d` 上，该报告 L869 是文档中**唯一**仍对 F-02 相关标准声称 `FAIL / BLOCKED` 的行，而另外六处均声称相反。L860 的 AC-06 也显示 `FAIL`，但该行依据的是“未采用 v1.2”这一已承认且不矛盾的事实——它并非自相矛盾。因此，AC-15 是 v2.11 未转换的唯一有效内部矛盾。

**等级：** VERIFIED（blob、行号、文本、计数）。**处置：** **已记录，未编辑。** 修正 L869 必须遵循报告自身的 §0 重新开启程序，并由其所有者执行；在此处编辑属于规范性编辑，本记录无权执行。更正提案见 §5 的 C-06。

### F-07 — `192.168.1.108:20127` 是 Web 控制台，而非 MCP 端点；`502 ETIMEDOUT` 分类已被证伪

| # | 探测 | 原始输出 | 时间戳 (+08) | 等级 |
|---|---|---|---|---|
| F-07.1 | TCP 可达性 | `Test-NetConnection 192.168.1.108 -Port 20127 -InformationLevel Quiet` → `True` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.2 | `GET /` | `http=307`，`redirect=http://192.168.1.108:20127/dashboard`，`t=0.274196s` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.3 | `GET /` 并跟随重定向 | `http=200`，`final=http://192.168.1.108:20127/login`，`t=0.025890s` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.4 | `GET /login` | `http=200`，`t=0.009948s` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.5 | `GET /mcp` | `http=404`，`t=0.016370s` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.6 | 受治理树中该端口的出现次数 | `git grep -n -I 20127 5670357d` → 恰好 2 次命中，且均为**叙述性文本**：`14-ai-development/work-items/AID-2026-078/session-evidence-1126.md:78` 和 `14-ai-development/work-items/AID-2026-241/evidence.md:73`，每处均位于关于 `ECONNREFUSED / ETIMEDOUT` 的句子中。`scripts/`、`.github/`、`crates/` 或任何可执行路径中均为零次命中。 | 2026-11-27T14:56:29 | VERIFIED |

**等级：** `502`/`ETIMEDOUT` 故障模式为 NOT_REPRODUCED；观察到的行为为 VERIFIED。**处置：** 该端点是可访问的 HTTP 控制台，不提供 MCP 路由。此前的分类予以撤回。本记录**不**对 MCP 契约本身作出超出 §2.7 所示内容的主张：仓库内的 memory-adapter 边界是本地 JSONL 子进程，因此，LAN 地址上的 HTTP 控制台不在该调用路径上。

### F-08 — opencode-purge：`continue_loop_on_deny` 是 2.4.2 中被接受的 `experimental` 键；`subagent_depth=4` 在 2.4.2 中处于有效状态，默认值为 1

| 层 | 证据 | 时间戳 (+08) | 等级 |
|---|---|---|---|
| 实际配置 | `%USERPROFILE%\.config\opencode\opencode.json` **L163-L164**：`"experimental": {` / `"subagent_depth": 4`。该文件中 `continue_loop_on_deny` 出现 **0** 次。 | 2026-11-27T14:20 | VERIFIED |
| 已安装二进制文件 | 2 个副本，**两者**均为 278,504,840 B，mtime 2026-11-26 14:08，`sha256 420c04c36407134e01ade0cec681c91407e119a0a5f37da69f097f61cbc7beee` **完全相同**：`…\ai.opencode.desktop\resources\opencode-cli.exe` 和 `…\Roaming\ai.opencode.desktop\cli\2.4.2-x64\opencode-cli.exe` | 2026-11-27T14:22 | VERIFIED |
| 二进制文件中的键存在情况 | `subagent_depth` ×6，`continue_loop_on_deny` ×2（两个二进制文件的原始字节计数） | 2026-11-27T14:22 | VERIFIED |
| 二进制文件中的 experimental 允许列表 | `KL=["logLevel","server","subagent_depth","layout"]`; `GI=["disable_paste_summary","batch_tool","openTelemetry","primary_tools","continue_loop_on_deny"]` | 2026-11-27T14:22 | VERIFIED |
| 二进制文件中的字段语义 | `Maximum subagent nesting depth. Defaults to 1.` ×2（UTF-16 字段说明，紧邻 `subagent_depth`） | 2026-11-27T14:44 | VERIFIED |
| 已发布 schema | `https://opencode.ai/config.json` → `http=200`，`75055` 字节；`experimental.additionalProperties = false`；`experimental.properties` 同时包含 `subagent_depth` 和 `continue_loop_on_deny`；`subagent_depth = {type: integer, minimum: 0, maximum: 9007199254740991}`；`continue_loop_on_deny = {type: boolean, description: "Continue the agent loop when a tool call is denied", deprecated: true}` | 2026-11-27T14:20 | VERIFIED |
| purge 自身的主张 | `D:\code\opencode-purge\lib\catalog.js` **L314-L317**，原文：`// Only subagent_depth is a live 2.4 field. \`continue_loop_on_deny\` used to be / // written here, but 2.4 lists it in GI and drops it as an unsupported legacy / // setting, so writing it only added noise to the config.` | 2026-11-27T14:18 | VERIFIED（按原文记录） |
| DP-01 补丁状态，两个二进制文件 | `DEEP_ANCHORS` = **9** 个条目。在**两个**二进制文件中，按偏移验证有 **8/9** 个已打补丁：原始 `find` 字符串不存在，替换后的 `repl` 字符串存在。偏移示例：`DEEP-IDENTITY-HI @261477553`、`DEEP-REFUSAL-LINE @261478528`、`DEEP-LENGTH-CAP @261485022`、`DEEP-24-IDENTITY @233918530`。 | 2026-11-27T14:24 | VERIFIED |
| 第 9 个锚点 | `DEEP-IDENTITY-COMMON` → `orig_off=-1`，`repl_off=-1`（`ABSENT_BOTH`）。其 `find` 文本是 `DEEP-IDENTITY-HI` 的严格子字符串，因此它被该锚点消耗，而不是在自身偏移处打补丁。 | 2026-11-27T14:24 | UNVERIFIED（未独立打补丁） |
| `subagent_depth` 的运行时加载 | `~/.local/share/opencode/log/opencode.log`：`subagent_depth` 0，`continue_loop_on_deny` 0，`Unrecognized` 0 → 没有拒绝警告，但也没有加载行 | 2026-11-27T13:00 | NOT_VERIFIED |
| 深度为 4 时的实际嵌套行为 | 本轮未执行嵌套 spawn 探测 | — | NOT_VERIFIED |

**等级：** 配置/schema/二进制/DP-01 偏移为 VERIFIED；运行时行为为 NOT_VERIFIED。
**处置：** “旧键已删除”的主张已被**证伪**——`continue_loop_on_deny` 位于 2.4.2 experimental 允许列表 `GI` 中，**并且**是已发布 schema 中 `experimental` 的有效属性（`additionalProperties:false`）。把允许列表当作删除的证据，颠倒了允许列表的含义。`subagent_depth` 是有效字段，文档注明其默认值为 `1`，当前配置为 `4`。两个键的**行为**均未经过测试。

### F-09 — 任何文件中都不存在“200 个验收框”

待测试的主张：`AID-2026-093` 的 INDEX 行声称“……仍有 200 个验收框未勾选”。

| `5670357d` 上的目标 | Blob | `- [ ]` | `- [x]` |
|---|---|---|---|
| `00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md` | `4810c6f8d3b5676a44288dea5782681e0745af6f` | **10** | 0 |
| `docs/en/…/2026-11-26-20-decision-acceptance-register.md` | `dcae8a7cb5c6e03bf220d1d681744cc68361e87d` | 10 | 0 |
| `docs/zh-CN/…/2026-11-26-20-decision-acceptance-register.md` | `49b3aff58991b77545ab143d12782b65e71a5a69` | 10 | 0 |
| `13-engineering-decisions/technology-architecture-blueprint.md` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | 10 | 0 |
| `00-governance/templates/bilingual-umbrella-requirement-template.md` | `9265098d739369522000ebc54b8c0275ee7e5b6d` | 4 | 0 |
| `14-ai-development/PR-GOVERNANCE-001.md` | `579ef2def33696c76eb636a46d6737eaee04edd5` | 0 | 0 |
| **整个树** | — | **28 个文件中共 333 个** | **32** |

命令：遍历 `git ls-tree -r --name-only 5670357d` 返回的每个路径，读取 `git cat-file blob <sha>`，并统计字节序列 `- [ ]` / `- [x]`。时间戳 2026-11-27T14:44 (+08)。**等级：** VERIFIED。

**处置：** 三种语言版本合计有 **30** 个框（10 + 10 + 10）；登记表本身有 **10** 个；整个树有 **333** 个。`200 = 20 × 10` 是将十项模板投射到二十条 DEC 行上的算术推算，却在 INDEX 单元格中被表述为观察结果。**此处不予更正**（INDEX 不在允许修改范围内）；更正文本见 §5 C-07。

### F-10 — single-writer（单写入者）：40/40 个已合并 PR 的 author == mergedBy；审查独立性在结构上不可实现

| # | 事实 | 证据 | 时间戳 (+08) | 等级 |
|---|---|---|---|---|
| F-10.1 | 最近更新的 40 个已合并 PR 中，`author == mergedBy` | GraphQL `pullRequests(states:MERGED, first:40, orderBy:UPDATED_AT DESC)` → `author_ne_mergedBy = 0`；`authors = ['oahcom']`；`mergedBy = ['oahcom']`；仓库 `totalCount = 865` 个已合并 PR | 2026-11-27T14:58:25 | VERIFIED |
| F-10.2 | 所有 open PR 均由同一账户创建 | GraphQL `pullRequests(states:OPEN)` → `open_total = 16`，`open_authors = ['oahcom']` | 2026-11-27T14:58:25 | VERIFIED |
| F-10.3 | 仓库为公开状态 | GraphQL `isPrivate=false`，`visibility=PUBLIC` | 2026-11-27T14:38 | VERIFIED |
| F-10.4 | 分支保护中不存在 `required_pull_request_reviews` | 报告 v2.11 L735（EN）/ L748（ZH）：“`GET /repos/…/branches/main/protection` 返回 HTTP 200：`required_status_checks.strict: true`；……**不存在 `required_pull_request_reviews`**。”L741：“这不能证明审查强制执行：`required_pull_request_reviews` 不存在，因此合并需要通过检查，但不需要获批审查。”文件中有 13 处独立记录与此一致。 | 2026-11-27T14:56:29 | VERIFIED（文档记录） |
| F-10.5 | 实时重新读取 `/protection` | 未执行——经过身份验证的 REST core 配额为 `0/5000` | — | NOT_VERIFIED |

**等级：** F-10.1–F-10.4 为 VERIFIED；F-10.5 为 NOT_VERIFIED。
**处置：** `OUT-OF-SCOPE(dev-baseline)`。平台层面的独立审查在**结构上不可实现**：只有一个账户，且没有强制审查，因此第二个会话或第二个浏览器都无法凭空产生独立审批者。此处记录的是能力边界，本记录中**没有**任何模拟行为——不声称存在独立审查者。

### F-11 — MCP 集成面：仓库内契约是本地子进程，而非 HTTP

| 载体 | 事实 |
|---|---|
| `chatgpt-session-ops/src/session_ops/memory_adapter_client.py` | 模块 docstring 声明采用 JSON Lines 协议、契约 v0.1，并注明“无 shell、无重试、无网络、无 MCP、无第三方依赖”；`import subprocess` |
| `chatgpt-session-ops/references/memory-adapter-contract-v0.1.md` | “首选传输方式：通过 stdin/stdout 传输 JSON Lines”；MCP 绝不能成为 SO 的强制依赖 |
| 本仓库在 `5670357d` 上的情况 | `git grep -n -I 20127` → 2 次命中，均为工作项证据中的叙述性文本（F-07.6）。没有代码路径。 |

**等级：** 对端口/代码主张（F-07.6）为 VERIFIED。**处置：** `192.168.1.108:20127` 上的 HTTP 控制台不属于本仓库的任何 MCP 代码路径。本轮未启动、连接或测试任何 MCP 服务器；运行时主张为 **NOT_VERIFIED**（§6，N-04）。

### F-12 — 此工作线此前的收尾尝试已被取代，其 CI 结果反映了本交付物的形态问题

草稿 PR **#1414**（`docs/wb-line03-closeout`，head `28b48f00654e03b872f2c1104ddc2c488858eaa6`，base `b12bfe8c`）由本工作线较早的一次尝试创建。该 PR 仍处于 open 状态。其自身的检查汇总于 2026-11-27T14:40 (+08) 读取，结果如下：

```
rollup FAILURE
  GOV-DOC-002 metadata checks  SUCCESS
  Repository hygiene (hard gate)  SUCCESS
  GOV-DOC-001 structural checks  FAILURE
  Bilingual docs coverage (ratchet)  FAILURE
  Branch freshness vs base  FAILURE
  Session Evidence  FAILURE
  (rust/clippy/fmt/doctest/BMCP/schema: SUCCESS)
```

**等级：** VERIFIED（通过 GraphQL `statusCheckRollup` 读取汇总结果）。**处置：** `Branch freshness` 失败，是因为该 PR 存续期间其 base 发生移动——这正是本记录通过固定基线并拒绝追随 `main`（§1.2）来缓解的结构性风险。三个实质性失败将在 §3 中结合本地门禁脚本分析；对于此单文件交付物无法满足的项目，将如实说明，而非加以隐藏。

---

## 3. 针对本提交运行的门禁

每个门禁均为仓库自身脚本，从分支工作树运行，使用其工作流采用的相同参数。“工作流名称”是该作业发布的必需检查上下文。

| # | 门禁（工作流上下文） | 判定 |
|---|---|---|
| 3.1 | GOV-DOC-002 metadata checks (`document-management.yml`) | PASS |
| 3.2 | GOV-DOC-001 structural checks — traceability leg (`bilingual-docs.yml`) | PASS |
| 3.3 | Bilingual documentation gate (`bilingual-docs.yml` / `Bilingual docs coverage (ratchet)`) | **FAIL** — 结构性失败，详见说明 |
| 3.4 | Repository hygiene (`repository-hygiene.yml`) | PASS |

**原始输出，按实际执行记录。** 以下四条命令从分支工作树运行，目标提交为 `5417d49c`——即引入此文件的提交。`5417d49c` 与你正在阅读的文件之间唯一的差异是本节文本，而任何门禁都不会读取该文本；在 PR head 上重新运行相同的四条命令，会得到相同的四个退出码（§3.5）。

### 3.1 GOV-DOC-002 metadata checks — PASS

```
$ python scripts/check_document_management.py --require-changed 5670357db7a836d4f26838dbaf99494af41e2b65
…
manual controls (not machine-verified, policy 9.2): M-01 … M-10
PASS (incremental): no GOV-DOC-002 violations; 752 classified, 370 unclassified
  Incremental verdict only: files outside the changed set were not required to be classified.
exit=0
```

### 3.2 GOV-DOC-001 structural checks，traceability 部分 — PASS

```
$ python scripts/check_governance_operation_traceability.py --check
GOVERNANCE OPERATION TRACEABILITY: PASS (7 operations x 3 mirrors)
exit=0
```

同一工作流上下文还会运行 `check_owner_namespace_references.py --check` 和 `check_bilingual_docs.py`；后者对应 3.3。

### 3.3 Bilingual documentation gate — **FAIL (exit 2)**

```
$ BASE_SHA=5670357d HEAD_SHA=5417d49c PR_BODY=<the body of this PR> python scripts/check_bilingual_docs.py
::notice::reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md: 'HISTORICAL — not a gate input'; …
::notice::reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md: 'HISTORICAL — not a gate input'; …
::error::New bilingual gap outside frozen baseline: 00-governance/reports/2026-11-27-wb-line03-closeout.md
exit=2
```

**说明失败原因，不绕过它。** `00-governance` 是 `NORMATIVE_ROOTS` 条目（`scripts/check_bilingual_docs.py`），因此其中新增的 `.md` 在配备 `docs/en/…` + `docs/zh-CN/…` 镜像、登记到 `EMBEDDED_BILINGUAL_SOURCES`，或在 PR body 中包含经 Owner 批准的 `BILINGUAL-EXCEPTION` 块之前，都会构成双语缺口。本记录按指令要求**只有一个文件**，而登记属于对验证器的代码编辑——两者均超出范围。PR body 中没有声称存在上述任何声明，因为这些声明都不属实：没有中文对应文件，也不存在 Owner 批准。

**处置：** `OUT-OF-SCOPE(order)` —— 这是交付形态与仓库政策之间的真实冲突，并非本记录可以掩盖的缺陷。补救方式：后续 PR 添加两个镜像文件，或取得 Owner 批准的限时例外。这也是草稿 #1414 的 `Bilingual docs coverage (ratchet)` 检查显示红色的原因（§2 F-12）。

### 3.4 Repository hygiene — PASS

```
$ python scripts/ci/check_repository_hygiene.py --base 5670357d --head 5417d49c
Work-item manifest consistency unrecognized shape: 14-ai-development/work-items/AID-2026-096/manifest.yaml
… (10 such lines, all pre-existing at the base commit)
Work-item index membership version=2026-11-27.2 directories=138 linked=138
Work-item manifest consistency version=2026-11-27.2 manifests=127 in_scope=112 excluded_by_record_type=5 unrecognized=10 violations=0
Repository new-file admission version=2026-11-27.2 base=5670357db7a836d4f26838dbaf99494af41e2b65 head=5417d49cdac7a303b5d388b5e55710e9a3c7fe20 merge_base=5670357db7a836d4f26838dbaf99494af41e2b65
Repository new-file admission passed: 1 new path(s) checked.
exit=0
```

`violations=0`，且新文件准入检查恰好针对一个新增路径通过。十条 `unrecognized shape` 行属于基线提交自身的积压问题（`unrecognized=10`），并非本次引入。

### 3.5 门禁汇总

| 门禁 | 上下文 | Exit | 判定 |
|---|---|---|---|
| Document management | GOV-DOC-002 metadata checks | 0 | PASS |
| Traceability | GOV-DOC-001 structural checks | 0 | PASS |
| Repository hygiene | Repository hygiene (hard gate) | 0 | PASS |
| Bilingual | Bilingual docs coverage / GOV-DOC-001 structural checks | 2 | **FAIL — 冻结基线之外出现新的缺口，见 3.3** |

四项中三项通过。第四项因指令创建的结构性原因失败；本记录如实报告失败，而不是通过声称一个并不真实的声明，将其转换成通过结果。

---

## 4. 本记录未执行的操作

- 未编辑 `INDEX.md`、任何 `manifest.yaml`、`aid-ledger.yaml`、`scripts/`、`.github/` 或任何规范性文档——包括 §2 F-06 中记录了 L869 缺陷的 F-02 报告。
- 未合并、未 force-push、未删除分支、未打开/关闭/编辑 Issue、未重新编号、未创建新工作项、未写入 ledger。
- 未在 `D:\code\chatgpt-session-ops` 下的任何位置写入内容。
- 新增一个文件：本记录。见 §7。

---

## 5. Ledger 中需要进行的更正

以下各行的 ledger 基线均为：`origin/aid-ledger` head `5592658f12f02ada111ccd338600ad2e17d7d2f4`，`aid-ledger.yaml` blob `9020f0a27945fcc3657d7fd35ab9cb699ee41855`（251 行）。**这些更正均未应用**——ledger 不在本记录的写入边界内。最后一列是所有者需要采用的确切文本。

| # | Ledger 行 | 当前内容 | `5670357d` 上的实际情况 | 证据 | 给 ledger 所有者的确切更正内容 |
|---|---|---|---|---|---|
| C-01 | `AID-2026-112`，L134-L137 | `state: OCCUPIED_BY_OTHER`；注释：“……追溯门禁覆盖工作项由外部工作线（**PR #1329**）重新分配为 **AID-2026-151**……” | 占用状态正确；但解释有两处错误。#1329 已**合并**（`76684cb2`，head `11fde79a`），并以 **AID-2026-174** 落地，而不是 151。`AID-2026-151` 从未进入 `main`。112 的占用方是 **#1316**（`8722a37b`）；#1309 是唯一另一个认领方，已**关闭且未合并**（`2026-11-27T04:31:22Z`）。 | §2 F-01、F-02、F-03 | 保留 `state: OCCUPIED_BY_OTHER`。将注释替换为：`note: "main carries a different AID-2026-112 from PR #1316 (merge 8722a37b). The retroactive gate-coverage record was renumbered 112 -> 151 -> 174 on the external branch and merged as AID-2026-174 in PR #1329 (merge 76684cb2, head 11fde79a). AID-2026-151 never entered main. PR #1309, the other claimant of 112, was closed unmerged (head df192ede)."` |
| C-02 | `AID-2026-116`，L150-L153 | `state: OCCUPIED_BY_OTHER`；`carrier: "PR #1321 (gov/aid-116-pin-and-attribution)"` | #1321 已**MERGED**（head `e61e714a`），且 `AID-2026-116/` **已位于 `main` 上**（四个 blob，§2 F-04）。`OCCUPIED_BY_OTHER` 描述的是被他人已落地工作占用的编号；此处工作已经落地，该编号已被消耗。L72 的 INDEX 行使问题进一步恶化，因为它仍显示 `PR_OPEN`。 | §2 F-04 | 改为：`state: MERGED` / `carrier: "PR #1321 (gov/aid-116-pin-and-attribution), merge commit not recorded; head e61e714a"`。另一个独立缺陷，交由另一个所有者处理：INDEX L72 的状态单元格应从 `PR_OPEN` 改为其他状态。 |
| C-03 | `AID-2026-117`，L240-L242 | `state: FREE`；注释：“不要信任此行……下一个合理的可用编号应 >= 189。” | `FREE` 状态成立——`117` 不存在于树中（`git grep` exit 1）。但注释中的下限已过时：`main` 已包含 AID-2026-241/253/260/261/279/280/290。一条指示读者不要相信自身的记录，不是可用的预留记录。 | §2 F-02 证据集；`git grep -n -I AID-2026-117 5670357d` → exit 1 | 保留 `state: FREE`。将注释替换为：`note: "re-verified absent on main@5670357d. Do not reuse the 189 floor: main already carries 241/253/260/261/279/280/290. Re-scan the main work-items tree immediately before any reservation push."` |
| C-04 | `AID-2026-151`，L158-L161 | `state: IN_FLIGHT`；`carrier: "PR #1329 (external, head f8236828)"` | **三个字段均已过时。** #1329 已为 `MERGED`（`2026-11-26T18:48:41Z`，合并提交 `76684cb2`）；其合并后的 head 为 `11fde79a`；它落地的工作项是 `AID-2026-174`。`f8236828` **不是**合并后 head 的祖先（`exit=1`）。`AID-2026-151` 仅存在于分支中，在 `main` 上不存在。 | §2 F-01、F-02 | 将该块替换为：`- id: AID-2026-151` / `state: SUPERSEDED` / `carrier: "renumbered to AID-2026-174 before merge; landed by PR #1329 (merge 76684cb2, head 11fde79a)"` / `note: "branch-only identifier (commits c84a8191, f8236828). Never present on main. Do not reuse."` |
| C-05 | `AID-2026-188`，L181-L183 | `state: IN_FLIGHT`；`carrier: "PR #1337 (external): records that the 03-memory-brain normative root is already registered"` | #1337 已**MERGED**（`2026-11-26T15:34:46Z`，合并提交 `f6ef2545`，head `c1a485cb`）；`AID-2026-188/` 已在 `main` 上，包含四个 blob；INDEX L299 显示 `MERGED`。分支 `renumber/1329-188`（`452285b9`，落后 868 / 超前 5）仍创建 `AID-2026-188/`，且其 `manifest.yaml` blob 与 `main` 上的版本不同（`99cc3460` 对比 `038a2e29`）→ rebase 时产生 add/add 冲突。 | §2 F-05 | 改为：`state: MERGED` / `carrier: "PR #1337, merge f6ef2545, 2026-11-26T15:34:46Z, head c1a485cb"` / 追加：`note: "branch renumber/1329-188 (452285b9) still carries a divergent AID-2026-188/manifest.yaml (99cc3460 vs main 038a2e29); it must be dropped or renumbered before it is rebased."` |
| C-06 | F-02 报告 **L869**（不是 ledger 行，但属于同类过时断言） | `\| AC-15 \| Reproducible independent acceptance \| … \| FAIL / BLOCKED — CI failure and outstanding findings \|` | 同一文档中 F-02 的所有其他断言均为 `COMPLETE / VERIFIED`（L505、L640、L968、L1023、L1164、L1180）。L869 是唯一残留项。 | §2 F-06 | 仅通过报告 §0 的重新开启程序处理：将 AC-15 重新分类，说明其两个历史原因中哪个仍然成立；或者将其标记为 `PARTIAL — historical CI failure run 44477435608 retained as a bound record`。**本记录不对此进行编辑。** |
| C-07 | `AID-2026-093` INDEX 行（INDEX blob `c14118f8`） | “……仍有 **200** 个验收框未勾选” | 没有任何文件或 issue 包含 200 个框。登记表有 **10** 个；三个语言版本副本有 **30** 个；整个树有 **333** 个，分布在 28 个文件中。 | §2 F-09 | 将数字替换为 `333 open \`- [ ]\` across 28 tracked files at 5670357d (the register itself: 10)`，并将其标明为全树计数，而非登记表自身的计数。**本记录不编辑 INDEX。** |

### 5.1 RESERVED 自身错误

Ledger 自身的预留行存在方法错误，使这些预留无法审计；这与编号是否可用无关。仅作记录；未更正。

| # | 行 | 自身错误 | 证据 | 更正所需内容 |
|---|---|---|---|---|
| R-01 | `AID-2026-262` L196-L199 | `carrier` 引用“本地工作树 wt-a262（commit 2b63b8ba）+ ref origin/work-item/aid-2026-262-merge-broker（commit 8908bb16）”，注释称该编号被一个未发布的本地实现占用，“AIDSCAN 判定其非权威占用”。若预留决定依赖本地、未发布工作树的内容，则其他任何参与方都无法复现该决定。 | Ledger blob `9020f0a2` L196-L199 | 要么发布该工作树 ref 和 commit，要么将 `carrier` 替换为已落地的载体，并从理由中删除本地工作树主张。 |
| R-02 | `AID-2026-263` L224-L227 | 注释以“AIDSCAN 五范围零命中（main 全历史 2829 提交 / 2349 ref 去重 1317 唯一树 / ledger 21 版本 / 280 worktree / PR refs 无降级）”为预留理由。这五项扫描均未提供命令、脚本路径或输出文件——无法根据本记录重新运行该主张。 | 同一 blob，L224-L227 | 追加 `verification: "AIDSCAN command: <path>; raw output: <path>; reproducible=yes"`，或重新运行扫描并引用结果。 |
| R-03 | `AID-2026-281` L200-L203 | 注释声称“main work-items tree 最多占用到 AID-2026-279；AID-2026-280 已被 PR #1384 消耗”。同一 ledger 的 R-04 注释却称 main 包含高于 279 的 **AID-2026-290**。同一文件中的两条预留注释对树的最高编号给出了不同说法。 | 同一 blob，L200-L203 对比 L243-L246 | 根据实际最高编号（`git ls-tree 5670357d -- 14-ai-development/work-items/`）重新陈述 281 的前提，而不是依赖记忆中的值。 |
| R-04 | `AID-2026-284` L243-L246 | 前提为“main work-items tree 在 279 以上仅包含 AID-2026-280 和 AID-2026-290”——可验证，且形态正确，但没有提供命令。 | 同一 blob，L243-L246 | 添加 `git ls-tree` 调用及其输出。 |
| R-05 | `AID-2026-285` L247-L250 | 注释称“285 已在 main tree 以及**所有 18 个 open PR head tree** 中扫描确认可用”。在 2026-11-27T14:58:25，仓库有 **16** 个 open PR；在本次审计较早阶段则有 **23** 个。open PR 的数量是不断变化的目标，因此“所有 N 个 open PR head tree”不是可复现的范围。 | GraphQL `pullRequests(states:OPEN)` → 14:58:25 时 `open_total` = 16，14:38 时为 23 | 重新表述为“已针对 `<timestamp>` 时的 open-PR head 集合进行扫描，N=……；集合会变化，使用前应重新扫描”。 |

**§5 全部内容的等级：** VERIFIED（引用文本和对照测量）。**处置：** 更正均为提案。§5 中没有任何内容写入 ledger、`INDEX.md` 或 F-02 报告。

---

## 6. NOT_VERIFIED / UNVERIFIED 登记表

| # | 项目 | 保持未决的原因 | 如何确定 |
|---|---|---|---|
| N-01 | `experimental.subagent_depth = 4` 的**运行时行为** | 配置中存在该键，二进制允许列表中也存在该键，但 `opencode.log` 不包含加载行或拒绝行，且未运行嵌套 spawn 探测。 | 在深度 1 处 spawn 一个本身会继续 spawn 的 subagent，观察第 5 层是否因 `Increase "experimental.subagent_depth" to allow nested subagents.` 而被拒绝。 |
| N-02 | `continue_loop_on_deny` 的**行为** | 实际配置中不存在该键，因此没有可供测试的对象。它在 2.4.2 和 schema 中的*存在性*已经验证；其效果尚未验证。 | 在临时 profile 中设置该键，拒绝一次工具调用，观察循环是否继续。 |
| N-03 | 实时重新读取 `branches/main/protection` | 经过身份验证的 REST core 配额为 `0/5000`；未认证请求返回 `401`，而非目标内容。因此 F-10.4 依据的是报告在 2026-11-25 的读取结果，而非新请求。 | 配额重置后，使用 token 执行 `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection`。 |
| N-04 | MCP 运行时：未启动服务器、未连接会话、未执行工具往返 | 明确不属于开发基线审计范围；memory-adapter 边界是本地子进程（F-11），且探测地址上不存在 MCP 端点（F-07）。 | 针对指定端点建立实时 MCP 会话，并记录握手及一次工具调用。 |
| N-05 | `AID-2026-263` 的“AIDSCAN 五范围零命中” | 无法根据本记录复现（R-02）。 | 发布扫描命令及其原始输出。 |
| N-06 | `#1256` 类审批者身份 | 不存在自然人载体；同一账户自我指定不能构成证据。 | 在本仓库之外提供一份独立记录，明确指出一名自然人。 |
| N-07 | `DEEP-IDENTITY-COMMON`（DP-01 锚点 9 个中的第 5 个）是否在自身偏移处打补丁 | 其 `find` 字符串是 `DEEP-IDENTITY-HI` 的严格子字符串，因此状态为 `ABSENT_BOTH`：被相邻锚点消耗，而不是在原位置替换。其**原始**文本已消失（这是好的），但没有独立证据证明其已单独处理（尚未证实）。 | 对未打补丁的 2.4.2 构建，在 `261477553` 周围进行字节差异比较，证明 common-string 的出现位置与 HI 字符串属于相同字节。 |
| N-08 | 每个 open PR 的 head tree 的行为 | 仅检查了 §2 中点名的特定 PR。`AID-2026-285` 关于“所有 N 个 open PR head tree”的主张（R-05）未在此重新运行。 | 对每个 open PR head 执行 `git ls-tree`，检查相关标识符。 |

---

## 7. 写入边界与自审计

| 项目 | 值 |
|---|---|
| 分支 | `docs/wb-line03-closeout-final` |
| 基线 | `5670357db7a836d4f26838dbaf99494af41e2b65` — 切出分支时最新的 `origin/main`（2026-11-27T14:5x +08） |
| 新增文件 | 1 个 — `00-governance/reports/2026-11-27-wb-line03-closeout.md` |
| 修改文件 | 0 个 |
| 删除文件 | 0 个 |
| Commit SHA / blob SHA | 记录在 commit 对象和 Draft PR body 中。文件无法包含自身的 blob SHA 而不改变该 SHA，因此将其记录在上述位置，而非此处。 |
| 取代对象 | 草稿 PR #1414（同一工作线，base `b12bfe8c`，head `28b48f00`），该 PR 基于一个此后已移动 520 个提交的 `main`。本记录不触碰 #1414。 |

验证与基线相比恰好只有一个路径不同：

```
git diff --stat 5670357d...HEAD
```

---

## 8. 方法说明（用于复现）

- **仓库读取**使用了针对明确固定 SHA 的 `git cat-file blob <sha>`、`git ls-tree <ref> -- <path>` 和 `git grep -n -I <pat> <ref>`。没有使用工作树读取作为证据，因为工作树无法固定。
- **行号**通过将 blob 的原始字节按 `\n` 拆分计算。PowerShell 的 `>` 重定向会重新编码并重新包装流，且会悄然改变行数（实测：一个 1472 行 blob 被转换为 1222/2514 行），因此本记录中的行号均不是从重定向文件得出的。
- **框数**是对从 `git ls-tree -r --name-only <ref>` 枚举出的每个 blob 执行 `bytes.count(b"- [ ]")` 得出的。
- **二进制检查**采用对 ASCII 和 UTF-16 常量进行原始字节搜索，并在记录的偏移处使用 `str.find`。未进行反汇编；未执行任何修改过的二进制文件。
- **GitHub 读取**使用 GraphQL，或对运行读取端点使用未认证 REST。token 从凭据文件读取，且从未打印。经过身份验证的 REST core 配额为 0，因此没有重新读取 `/protection`（N-03）。
- **网络探测**使用 `Test-NetConnection -InformationLevel Quiet` 和带有明确超时的 `curl.exe -m 5 -w`；每个结果均记录了其 `time_total`。
