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

**实测**：忠实复现 Issue #351 记录的形态——中文规范文件先直推 main（无 PR），随后 PR 只补英文侧：

```
BASE:   08-bmcp-protocol/bypass.md        (直推，无配对)
HEAD:   docs/en/08-bmcp-protocol/bypass.md
        docs/zh-CN/08-bmcp-protocol/bypass.md

$ python3 scripts/check_bilingual_docs.py
Bilingual documentation and prompt-library gate: PASS (2 changed paths inspected).
STDERR: NOTE: 2 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked
EXIT=0
```

**判定：`NOT_SATISFIED`**。这正是 AC-5 明确要求**不得**出现的结果。门禁报告 PASS，而中文规范文件 `08-bmcp-protocol/bypass.md` 从未被任何配对检查看过——它在 BASE 侧，不在变更集内，而门禁只检查变更集。

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
| AC-5 | 直推旁路负向测试必须失败 | `NOT_SATISFIED` |
| AC-6 | 未配对失败 | `SATISFIED` |
| AC-7 | 无审批例外失败 | `SATISFIED` |
| AC-8 | 真实配对通过 | `SATISFIED` |
| AC-9 | 目录集相等测试 | `NOT_SATISFIED` |
| AC-10 | 测试套件覆盖并记录 | `PARTIALLY_SATISFIED` |

**4 条满足、2 条部分满足、4 条不满足。**

其中 AC-1、AC-5、AC-9 是本次 Issue 的**核心**：它们分别对应「不再依赖手写名单」「直推旁路被发现」「回归有测试守住」。这三条全部不满足，意味着 **Issue #384 所描述的缺陷在修复后仍然存在，只是形态略有变化**。

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

但 AC-5 的实测显示：这 4 个文件若先直推到 main，再在 PR 中补 `docs/en` 与 `docs/zh-CN` 镜像，门禁仍报 PASS。

即：**覆盖范围扩大了，旁路仍然存在**。旁路的根因不在名单，在于门禁只检查 `changed_paths()` 返回的变更集，而不检查变更集之外的既有规范文件是否已有配对。

这一点在 Issue #384 的 AC-5 中被准确描述，在修复中未被处理。

---

## 7. 与前三份登记的耦合

| 登记 | 耦合点 |
|---|---|
| `DIRECT-MAIN-001` | 旁路的前提是直推；直推至今仍在发生（`ae5a886f`、`25c61283` 等） |
| `SELF-AUTH-002` | 关闭者与实现者、审查者同为 `oahcom`；关闭裁定无第三方 |
| `MERGE-AFTER-RULING-003` | PR #394 在 `reviews=0`、check `failure` 下 14 秒内合并，随后 2 秒关闭 Issue |

四份登记指向同一根因：**本仓库当前不存在任何角色分离**。实现、审查、裁定、关闭由同一账号在秒级间隔内完成。

---

## 8. 纠正措施（待批准，未执行）

| # | 措施 | 性质 | 状态 |
|---|---|---|---|
| N-1 | 重新打开 #384，或建立 `#384-FOLLOWUP`，仅覆盖 AC-1、AC-4、AC-5、AC-9 四条 | 范围修正 | 未执行（需授权） |
| N-2 | 在 #384 补一条关闭后标注，写明「10 条 AC 中 4 条满足、4 条不满足」，并附本登记链接 | 追溯标注 | 未执行 |
| N-3 | 实现 AC-5 所要求的旁路检测：对 `docs/en/<root>/x` 的新增，检查源 `<root>/x` 是否在 main 上已有配对 | 实现 | 未执行（需投入会话执行） |
| N-4 | 实现 AC-9 的目录集相等测试 | 实现 | 未执行 |
| N-5 | 在 `PR-GOVERNANCE-001` 中明确：Issue 关闭评论必须逐条列出 AC 判定，未逐条列出者不得视为已验收 | 规范 | 未执行（需 Owner） |

N-5 是唯一能让本类缺陷不再重复的措施。N-1 至 N-4 只是补做。

---

## 9. 验证证据

| 证据 | 值 |
|---|---|
| 复检基线 | `main @ e2644784c010da488b4794f3e6b10d17c32e9b4b` |
| 门禁脚本 blob | `check_bilingual_docs.py` @ main，20451 字节 |
| AC-1 实测 | 新建 `09-storage-and-index/spec.md` → `PASS`，`EXIT=0` |
| AC-2 实测 | 注入 `99-nonexistent` → `EXIT=2` |
| AC-4 实测 | 3 文件配对变更 → 仅 stderr skipped 计数，无 normative 计数，`EXIT=0` |
| AC-5 实测 | #351 形态复现 → `PASS`，`EXIT=0` |
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
- 未修改门禁脚本。N-3、N-4 需由执行会话实现，本会话不代写。

---

**登记结论**：Issue #384 在 10 条自定 AC 中 4 条不满足、2 条部分满足的情况下被关闭，且关闭距合并 2 秒。核心三条（AC-1 树推导、AC-5 旁路检测、AC-9 回归测试）全部未实现，Issue 所描述的缺陷在修复后以相同机制继续存在。建议将 #384 的关闭状态标注为 `AC_PARTIALLY_UNMET`，而非 `FIXED`。
