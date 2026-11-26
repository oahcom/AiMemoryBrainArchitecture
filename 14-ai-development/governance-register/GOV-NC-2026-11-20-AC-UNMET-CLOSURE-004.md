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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-21"
      last_verification_note: "All figures come from the GitHub REST API and from local reads on 2026-11-21; the 2026-11-25 annotation in section 7 records no new measurement and changes no number."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004 — 验收条件未满足即关闭 Issue 登记

**状态**：`OPEN` / `NOT_REMEDIATED`
**缺陷类别**：Governance Conformance — Acceptance Closure Integrity
**严重度**：High
**失效模式**：Closure asserted against acceptance criteria that were never executed
**发现时间**：2026-11-21 复检
**关联登记**：`DIRECT-MAIN-001`、`SELF-AUTH-002`、`MERGE-AFTER-RULING-003`

---

## 1. 为什么单独登记

前三份登记记录的是**代码如何进入 main**（直推、门禁绕过、无审查合并）。

本登记记录的是**Issue 如何被关闭**：关闭评论声称修复完成，而该 Issue 自己定义的验收条件中，多数从未被执行，且经过实测确认不满足。

这与「实现有 bug」不是同一件事。实现有 bug 是工程问题；把未执行的验收条件声称为已满足，是记录完整性问题。后者会让后续所有依赖该 Issue 关闭状态的判断失真。

---

## 2. 事实基础

| 项目 | 值 |
|---|---|
| Issue | #384 `[GOV-DOC] Bilingual documentation gate whitelist does not match the repository tree` |
| 关闭者 | `oahcom` |
| 关闭时间 | 2026-11-20T18:25:06Z |
| 关联 PR | #394，`merged_at` 18:25:04Z |
| **关闭距合并** | **2 秒** |
| PR #394 改动 | 1 个文件，`scripts/check_bilingual_docs.py`，`+15/−5` |
| PR #394 reviews | 0 |
| PR #394 check run | `GOV-DOC-001 structural checks` → `failure` |
| PR #394 从建立到合并 | 14 秒 |

Issue #384 由本方（同一 GitHub 账号 `oahcom`）撰写并提交，其中定义了 AC-1 至 AC-10 十条验收条件。关闭评论未逐条对应，只提供了三个证据：修正前后名单对照、`NORMATIVE_ROOTS` 的 diff、fail-closed 自检演示。

**关闭距合并 2 秒**意味着关闭者没有时间运行 AC-5、AC-6、AC-7、AC-9 这类需要构造变更集才能验证的负向测试。

---

## 3. AC 逐条实测

以下全部为本方在 `main @ e2644784c010` 的浅克隆上实际执行的结果，不是阅读代码后的推断。

测试方法：构造 `BASE_SHA` / `HEAD_SHA` / `PR_BODY` 三个环境变量，直接运行仓库内的 `scripts/check_bilingual_docs.py`，记录退出码。

### AC-1 — 从目录树推导，而非手写名单

> The gate derives its normative root set from the repository tree at run time. No hand-maintained list of directory names decides whether a path is normative.

**实测**：新建 `09-storage-and-index/spec.md`（未配对），提交后运行门禁：

```
$ BASE_SHA=<B> HEAD_SHA=<H> PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python3 scripts/check_bilingual_docs.py
Bilingual documentation and prompt-library gate: PASS (1 changed paths inspected).
STDERR: NOTE: 1 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked
EXIT=0
```

**判定：`NOT_SATISFIED`**。`NORMATIVE_ROOTS` 仍是模块级硬编码集合（第 16–20 行，9 个字面量）。新增数字前缀目录不会被识别为规范域，只产生一条 stderr 提示，退出码为 0。AC-1 要求的行为与实际行为相反。

### AC-2 — 名单指向不存在目录时失败

**实测**：向集合注入 `"99-nonexistent"`：

```
STDERR: NORMATIVE_ROOTS references non-existent directories: 99-nonexistent
EXIT=2
```

**判定：`SATISFIED`**。这是本次修复唯一真正实现的机制性改动。

### AC-3 — 每个数字前缀目录要么被覆盖，要么带理由豁免

**实测**：`08-bmcp-protocol` 已加入集合，被覆盖。但 `09-storage-and-index` 这一 AC-1 测试中新建的目录，既未被覆盖，也没有任何显式豁免记录，且不产生失败。

**判定：`PARTIALLY_SATISFIED`**。对**当前存在**的目录成立；对**将来新增**的目录不成立，因为没有机制强制新目录必须被纳入或豁免——这正是 AC-1 与 AC-9 要解决的问题。

### AC-4 — 打印归类数与跳过数，两者皆零时报错

**实测**（真实配对变更集，3 个文件）：

```
STDOUT: Bilingual documentation and prompt-library gate: PASS (3 changed paths inspected).
STDERR: NOTE: 2 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked
EXIT=0
```

**判定：`NOT_SATISFIED`**。只输出 skipped 计数，没有输出「被归类为 normative 的路径数」。且「两者皆为零时报错」这一条完全未实现——代码中不存在该分支。

### AC-5 — 负向测试：直推旁路

> given a change set where a normative Chinese document already exists on `main` without a counterpart, and a PR adds only the English counterpart, the gate must **not** report complete bilingual compliance.

**实测（更正后，见 §11）**：AC-5 原文只描述一种形态——PR **只**补英文侧。按字面复现：

```
BASE:   08-bmcp-protocol/bypass9.md            (中文规范文件已在 main，无配对)
HEAD:   docs/en/08-bmcp-protocol/bypass9.md    (只加英文侧)

$ BASE_SHA=<B> HEAD_SHA=<H> PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python3 scripts/check_bilingual_docs.py
::error::docs/en/08-bmcp-protocol/bypass9.md changed without paired change docs/zh-CN/...
::error::Chinese counterpart does not exist: docs/zh-CN/08-bmcp-protocol/bypass9.md
Bilingual documentation gate: FAIL
EXIT=1
```

**判定：`SATISFIED`**。

> **更正**：本节上一版判定为 `NOT_SATISFIED`，依据的探针在 HEAD 侧**同时加了** `docs/en/` 与 `docs/zh-CN/`（见上方旧记录），被测门禁 `PASS EXIT=0`。该探针与 AC-5 原文不符——AC-5 说的是「**只**加英文」。而且那个 `PASS` 不是缺陷：源文件在 BASE 未配对，PR 补齐双侧后源文件即已配对，报 PASS 正确。
>
> 上一版把「门禁只检查 diff、不检查整棵树」这个性质错误地挂到 AC-5 名下。该性质真实存在，但载体是存量 83 条未配对路径（§11.3），不是 AC-5。
>
> 更正依据：`main @ eca6f5706e`、`@ 8dc92c3debde` 各复现一次，均 `EXIT=1`；`#351` 的**真实**提交对 `568b847ce39f → af1e93d49d` 在同一门禁上同样 `EXIT=1`。

### AC-6 — 未配对规范 md 失败

**实测**：`02-domain-model/unpaired-*.md` 单独变更：

```
::error::02-domain-model/unpaired-...md requires both counterparts changed in this PR: docs/en/..., docs/zh-CN/...
::error::Both counterpart files must exist for 02-domain-model/unpaired-...md
Bilingual documentation gate: FAIL
EXIT=1
```

**判定：`SATISFIED`**。

### AC-7 — 例外声明无审批记录时失败

**实测**：`PR_BODY="BILINGUAL-EXCEPTION: APPROVED"`（无审批记录字段）：

```
::error::Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED'.
Bilingual documentation gate: FAIL
EXIT=1
```

**判定：`SATISFIED`**。

### AC-8 — 正向对照：真实配对通过

**实测**：源 + `docs/en/` + `docs/zh-CN/` 三文件同变更集：

```
Bilingual documentation and prompt-library gate: PASS (3 changed paths inspected).
EXIT=0
```

**判定：`SATISFIED`**。

### AC-9 — 测试断言磁盘目录集等于门禁认知集

**实测**：在 `scripts/` 与 `tests/` 全量搜索 `NORMATIVE_ROOTS`：

- `scripts/governance/evidence/test_gate_normative_roots.py` 中 4 处引用，全部是 `assertIn("14-ai-development", ...)` 或 `src.split("/")[0] in ...` 形式。
- 无任何断言遍历磁盘上的 `^\d\d-` 目录并与 `NORMATIVE_ROOTS` 做集合相等比较。
- PR #394 未新增或修改任何测试文件（`files = 1`，仅 `check_bilingual_docs.py`）。

**判定：`NOT_SATISFIED`**。该测试不存在。

### AC-10 — 在仓库测试套件中执行，可离线运行，记录命令与退出码

**实测**：运行现存测试套件：

```
$ python3 -m pytest scripts/governance/evidence/test_gate_normative_roots.py -q
.................                                                        [100%]
17 passed in 0.36s
```

**判定：`PARTIALLY_SATISFIED`**。套件可离线运行且通过，但它是 F-07 的测试，覆盖的是 `14-ai-development` 的配对惯例，**不覆盖 AC-1、AC-4、AC-5、AC-9**。关闭评论未记录任何测试命令与退出码。

---

## 4. 汇总

| AC | 要求 | 判定 |
|---|---|---|
| AC-1 | 运行时从目录树推导 | `NOT_SATISFIED` |
| AC-2 | 名单含不存在目录时失败 | `SATISFIED` |
| AC-3 | 每个数字目录被覆盖或带理由豁免 | `PARTIALLY_SATISFIED` |
| AC-4 | 打印归类数与跳过数，两者皆零报错 | `NOT_SATISFIED` |
| AC-5 | 直推旁路负向测试必须失败 | `SATISFIED`（更正） |
| AC-6 | 未配对失败 | `SATISFIED` |
| AC-7 | 无审批例外失败 | `SATISFIED` |
| AC-8 | 真实配对通过 | `SATISFIED` |
| AC-9 | 目录集相等测试 | `NOT_SATISFIED` |
| AC-10 | 测试套件覆盖并记录 | `PARTIALLY_SATISFIED` |

**5 条满足、2 条部分满足、3 条不满足。**

> 本节原为「4 满足 / 2 部分 / 4 不满足」，AC-5 记 `NOT_SATISFIED`。该判定已更正为 `SATISFIED`，理由见 §11.1。

其中 AC-1、AC-9 是本次 Issue 的**核心机制项**：前者对应「不再依赖手写名单」，后者对应「回归有测试守住」。两条均不满足。AC-4 是观测能力项，不满足。

---

## 5. 修复实际改变了什么

必须公允记录：PR #394 不是空操作。

| 变化 | 效果 |
|---|---|
| 删除 7 个不存在的目录名 | 名单不再自相矛盾 |
| `08-protocols` → `08-bmcp-protocol` | **4 个规范 md 恢复了配对检查覆盖**，这是实质改进 |
| 新增模块级 `_missing_roots` 检查 | 名单漂移的一个方向被堵住（指向不存在目录） |
| 新增 skipped 计数 stderr 提示 | 静默跳过变成有提示的跳过 |

但它修复的是**名单与树的当前不一致**，没有修复**名单与树会再次不一致**这个机制问题。后者才是 Issue #384 §"Required fix" 的第二段所要求的：

> If a hand-maintained list is kept for exclusion purposes, add a self-check that fails when a whitelisted directory does not exist, **and fails when a numbered directory exists but is neither whitelisted nor explicitly exempted with a reason**.

后半句未实现。实测：`09-storage-and-index` 存在、未列入、未豁免、不失败。

---

## 6. 一个需要指出的结构性事实

`08-bmcp-protocol` 的 4 个 md 在修复前不受检查、修复后受检查，因此**在修复之后**，任何针对这 4 个文件的未配对变更会失败。

本轮更正后的实测显示：AC-5 的旁路形态**确实被堵住**——源文件在 BASE、PR 只补英文侧 → `EXIT=1`。这一条 PR #394 的修复是有效的。

但**另一种形态仍然通过**：若 PR 在补英文的同时也补中文镜像（即同变更集内凑齐双侧），门禁报 `PASS`，而 BASE 侧那份未配对的源文件从未被看过。这一形态的 `PASS` 是**正确行为**（源文件此时已配对），它暴露的是另一个问题：门禁的判定域是 diff 而非树。

该问题不属于 #384 的 AC 范围，属于存量债务，见 §11.3。

---

## 7. 与前三份登记的耦合

| 登记 | 耦合点 |
|---|---|
| `DIRECT-MAIN-001` | 旁路的前提是直推；直推至今仍在发生（`ae5a886f`、`25c61283` 等） |
| `SELF-AUTH-002` | 关闭者与实现者、审查者同为 `oahcom`；关闭裁定无第三方 |
| `MERGE-AFTER-RULING-003` | PR #394 在 `reviews=0`、check `failure` 下 14 秒内合并，随后 2 秒关闭 Issue |

四份登记指向同一根因：**本仓库当前不存在任何角色分离**。实现、审查、裁定、关闭由同一账号在秒级间隔内完成。

> **〔2026-11-25 附注〕** 本句把「四份登记的四名角色登录名都是 `oahcom`」——一个**账号层**事实——当作「本仓库不存在任何角色分离」这一结论的依据。§5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）：同一 GitHub 身份下的另一会话即可构成独立审查。`/pulls/{n}/reviews` 只返回 `user.login`，不返回会话，故「同一身份 ⇒ 同一会话」这一步在该载荷里无法核实。此处应读作「账号层不独立、会话层未核实」。
> **仍然成立的部分**：上文四行表格里可核的字段都不依赖身份如何定义——`SELF-AUTH-002` 的关闭者是唯一账号、PR #394 的 `reviews=0` 且 check 为 `failure`、间隔 14 秒、「秒级间隔」本身。这些足以支撑「这四次动作没有第三方参与」；它们不足以支撑「角色分离在结构上不存在」。两者的区别是「未发生」与「不可能」，而本节原文把前者写成了后者。

---

## 8. 纠正措施（待批准，未执行）

| # | 措施 | 性质 | 状态 |
|---|---|---|---|
| N-1 | 重新打开 #384，或建立 `#384-FOLLOWUP`，仅覆盖 AC-1、AC-4、AC-5、AC-9 四条 | 范围修正 | 未执行（需授权） |
| N-2 | 在 #384 补一条关闭后标注，写明「10 条 AC 中 4 条满足、4 条不满足」，并附本登记链接 | 追溯标注 | 未执行 |
| N-3 | 实现 AC-5 所要求的旁路检测 | 实现 | **已撤回** —— AC-5 实测已满足，见 §11.1 |
| N-4 | 实现 AC-9 的目录集相等测试 | 实现 | 未执行 |
| N-5 | 在 `PR-GOVERNANCE-001` 中明确：Issue 关闭评论必须逐条列出 AC 判定，未逐条列出者不得视为已验收 | 规范 | 未执行（需 Owner） |
| N-6 | 存量 83 条未配对路径的独立清查 | 存量债务 | **已立 #407**，见 §11.3 |

N-5 是唯一能让本类缺陷不再重复的措施。N-1、N-2、N-4 只是补做。

---

## 9. 验证证据

| 证据 | 值 |
|---|---|
| 复检基线 | `main @ e2644784c010da488b4794f3e6b10d17c32e9b4b` |
| 门禁脚本 blob | `check_bilingual_docs.py` @ main，20451 字节 |
| AC-1 实测 | 新建 `09-storage-and-index/spec.md` → `PASS`，`EXIT=0` |
| AC-2 实测 | 注入 `99-nonexistent` → `EXIT=2` |
| AC-4 实测 | 3 文件配对变更 → 仅 stderr skipped 计数，无 normative 计数，`EXIT=0` |
| AC-5 实测 | 字面形态（只加英文）`EXIT=1`；更正见 §11.1 |
| AC-6 实测 | 未配对 md → `EXIT=1` |
| AC-7 实测 | 无审批例外 → `EXIT=1` |
| AC-8 实测 | 三文件配对 → `EXIT=0` |
| AC-9 实测 | `NORMATIVE_ROOTS` 全库搜索 4 处，均为成员断言，无集合相等断言 |
| AC-10 实测 | `pytest ... test_gate_normative_roots.py` → `17 passed in 0.36s` |
| 关闭时间差 | merge 18:25:04Z → close 18:25:06Z，2 秒 |
| PR #394 | `files=1`、`reviews=0`、check `failure`、建立到合并 14 秒 |

复检在 `main` 的浅克隆上执行，测试变更集为本地临时提交，**未推送、未修改远端任何内容**。

---

## 10. 明确未做的事

- 未重新打开 #384。是否重开属 Owner 决定，本登记不代为执行。
- 未认定修复者的技术判断错误。PR #394 的四项改动均正确，问题在于范围不足。
- 未主张应回滚 #394。`08-bmcp-protocol` 恢复覆盖是净改进，回滚会使情况更差。
- 未认定关闭者明知 AC 未满足。2 秒的间隔只证明未执行验证，不证明主观故意。
- 未修改门禁脚本。N-4 需由执行会话实现，本会话不代写。

---

## 11. 第五轮复检：对本文档自身的三处更正（2026-11-21 03:30Z 后）

### 11.1 AC-5 判定更正：`NOT_SATISFIED` → `SATISFIED`

**错在哪里**：本文档 §3 AC-5 原先引用的探针，HEAD 侧同时加了 `docs/en/` 与 `docs/zh-CN/` 双侧镜像。但 AC-5 的原文是「a PR adds **only** the English counterpart」。探针与判据不同形，结论无效。

**为什么那个 PASS 不是缺陷**：源文件在 BASE 侧未配对，PR 补齐双侧镜像后该源文件已配对。门禁报 `PASS` 在语义上正确。

**更正后的实测**（两个基线各一次）：

| 基线 | 变更集 | 结果 |
|---|---|---|
| `eca6f5706e` | BASE 有 `08-bmcp-protocol/bypass9.md`，HEAD 只加 `docs/en/.../bypass9.md` | `EXIT=1`，`::error::Chinese counterpart does not exist` |
| `8dc92c3debde` | 同上 | `EXIT=1` |
| `568b847ce39f → af1e93d49d`（#351 真实提交对） | ZH 文件在 BASE，PR 只加 EN | `EXIT=1` |

**AC-5 = `SATISFIED`。** 账目由「4 满足 / 2 部分 / 4 不满足」改为「5 满足 / 2 部分 / 3 不满足」。

**这次更正不是措辞让步**：上一版把一个超出 AC 原文的性质记成 AC 失败，会让修复者去实现一个没人要求的检查，同时让真正满足的条款显得未做。两者都是失实。

### 11.2 「门禁判定域是 diff 而非树」的正确归属

该性质真实存在，但**不是 AC-5**。它的正确载体是存量：在 `main @ 8dc92c3debde` 上跑全库扫描，**409 个在范围内 Markdown、107 个豁免、83 条未配对违规，`EXIT=1`**。

```
$ python3 check_bilingual_docs_full.py --paths-file <main@8dc92c3d 全路径> \
    --source-revision 8dc92c3debde --report ...
GOV-DOC-001 full scan: 409 in-scope Markdown files; 107 exempt; 83 violations.
GOV-DOC-001 full scan: FAIL
```

83 这个数在 `ae5462f6ef` 与 `8dc92c3debde` 两次取树上都是 83，不随最近提交漂移。

**归属更正**：N-3（在 #401 名下实现旁路检测）撤回。83 条存量走独立载体 **#407**（见 §11.3），不并入 #401。#401 继续只做它标题写的事。

### 11.3 新增载体：#407 存量 83 条清查

按 `PR-GOVERNANCE-001` 的分离原则，门禁修复（#401）与存量清查（#407）验收对象不同：

- #401 答复「门禁能否发现 BASE 侧既有未配对文件」——用专门构造的 BASE/HEAD 负向测试验收。
- #407 答复「仓内既有 83 条是否已逐项处置」——用逐路径分类与理由验收。

两者互不代替。若并入，会出现两种错误归因：门禁实现被 83 条处置进度阻塞；83 条处置结果被当成门禁修复成功的证明。

### 11.4 与本文档关联的新事实

| 事实 | 值 | 影响 |
|---|---|---|
| PR #403 最终被合并 | 03:26:28Z，`merged_by=oahcom` | 我在 313 号回灌里报的「反例」**只维持了 7 小时**；十分之十分钟预测失败，但同类合并最终仍发生 |
| #403 合并前有一次 review | 03:26:13Z，`COMMENTED`，作者 = 审查者 = 合并者 = `oahcom` | 「有 review」与「有独立 review」是两件事；此处 review 与合并间隔 15 秒 |
| #403 合并时 check | `GOV-DOC-002 metadata checks` = `failure` | 合并仍在检查失败下完成 |
| #384 再次被关闭 | 20:06:51Z，距 #402 合并 2 秒 | 我 19:34Z 的重开在 32 分钟后被覆盖；第三次关闭 |
| 直推累计 | **53 → 62**（新增 9 个，含 `governance@localhost` 身份 2 个） | 见 `DIRECT-MAIN-001` §14 |
| `check_document_management.py` 被直推大改 | `1733c3bf4a` +721/−166，`0f5b5a00e7` +141/−63 | 门禁实现本身以直推方式变更，无 PR、无 review |

**登记结论**：Issue #384 在 10 条自定 AC 中 **3 条不满足、2 条部分满足、5 条满足**的情况下被关闭，且首次关闭距合并 2 秒。核心机制项（AC-1 树推导、AC-9 回归测试）未实现，AC-4 观测项未实现；AC-5 旁路检测**已实现**。建议将 #384 的关闭状态标注为 `AC_PARTIALLY_UNMET`，而非 `FIXED`。
