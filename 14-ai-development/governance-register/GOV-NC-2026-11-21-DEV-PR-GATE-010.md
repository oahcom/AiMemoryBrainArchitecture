# GOV-NC-2026-11-21-DEV-PR-GATE-010 — 九个开发 PR 中五个无法通过门禁，原因相同

## 0. 摘要

按 Owner 裁定 D（开发继续、先走通一条合规路径）的要求，我逐个把 main 上九个开发 PR 的 exact head 叠加到当前 main（`c138654c94`），在**真实 git 历史**上跑双语门禁。

结果：

**4 个失败 / 5 个通过。四个失败全部是同一原因，而且都不是「PR 内容错」。**

更重要的是：通过的五个分属四种不同形态，失败的四个全是同一种形态。**门禁实际上在按「文件放在哪个目录」而不是「双语是否齐全」做判定。**

## 1. 这五个失败不是「PR 写错了」

### 1.1 通过的那五个说明了什么

#428、#430、#434、#444 通过，#429 也通过。它们的共同点：

| PR | 形态 |
|---|---|
| #428 | 新增 `08-bmcp-protocol/` 下 3 个文件 —— **但 §1.2 会说明为何它过了** |
| #429 | **只改已有的 `docs/en` + `docs/zh-CN` 文件**，无新增根文件 |
| #430 | 新增 `07-agent-integration/` 下 3 个文件 |
| #434 | 只改 `crates/` 下代码 |
| #444 | 只新增 `crates/` 下测试 |

#434、#444 通过是因为**代码和测试完全不受双语门禁约束**（门禁只扫 `*.md` 且只在 `NORMATIVE_ROOTS` 下）。这一点很重要：它意味着「测试能进、规范不能进」。

#429 通过是因为它改的是**已存在**的 `docs/en` 与 `docs/zh-CN` 配对文件，两侧同步修改，满足 `check_mirror_pairing`。

### 1.2 通过的那五个，形态各不相同——这本身就是答案

实测各 PR 的改动形态：

| PR | 形态 | 门禁 | 为什么 |
|---|---|---|---|
| #430 | 根 `07-agent-integration/X.md` + `docs/en/X.md` + `docs/zh-CN/X.md` | **PASS** | 三件套，`docs/` 两侧都存在 |
| #428 | `reviews/bmcp-architecture-followup/X.en.md` + `.zh-CN.md` | **PASS** | `reviews/` **不在 `NORMATIVE_ROOTS`**，完全不受约束 |
| #429 | 只改**已有**的 `docs/en` + `docs/zh-CN` 配对文件 | **PASS** | 两侧同步修改，`check_mirror_pairing` 满足 |
| #434 | 只改 `crates/` 下代码 | **PASS** | 门禁只扫 `NORMATIVE_ROOTS` 下的 `*.md` |
| #444 | 只新增 `crates/` 下测试 | **PASS** | 同上 |
| #425 | 根 `04-memory-compiler/X.md` + `X.zh-CN.md` | **FAIL** | 无 `docs/` 镜像 |
| #433 | 根 `06-memory-context/X.md` + `X.zh-CN.md` | **FAIL** | 同上 |
| #435 | 根 `02-domain-model/X.md` + `X.zh-CN.md` | **FAIL** | 同上 |
| #436 | 根 `08-bmcp-protocol/X.md` + `X.zh-CN.md` | **FAIL** | 同上 |

**这不是「有的 PR 写得好、有的写得差」。这是四种不同位置带来的四种不同约束：**

1. 写进 `crates/` → 不受约束（代码/测试）
2. 写进 `reviews/` → 不受约束（不在根清单里）
3. 写进已有 `docs/` 配对 → 受约束但满足
4. 写进 `NORMATIVE_ROOTS` 根目录并排双语 → **受约束且不满足**

四个失败全在第 4 类。

### 1.3 四个失败的共同形态

四个 `EXIT=2` 的 PR 有一个共同形态：

```
<NORMATIVE_ROOT>/X.md           (英文正文)
<NORMATIVE_ROOT>/X.zh-CN.md     (中文正文)
```

这是仓库**既有**的双语并排惯例——`08-bmcp-protocol/`、`13-engineering-decisions/`、`14-ai-development/` 下大量文件都是这个形态。

但 `current_bilingual_gaps()` 对 `NORMATIVE_ROOTS` 下每个 `*.md` 要求：

```python
english = REPO_ROOT / "docs" / "en" / source
chinese = REPO_ROOT / "docs" / "zh-CN" / source
if not english.is_file() or not chinese.is_file() or resolved_14 is None:
    gaps.add(source)
```

而 `resolved_14 = counterpart_14(source) if root_name == "14-ai-development" else True`。

**关键点：`counterpart_14` 只对 `14-ai-development` 生效。** 对 `00-governance`、`02-domain-model`、`04-memory-compiler`、`06-memory-context`、`08-bmcp-protocol`、`07-agent-integration`、`01-system-architecture`、`13-engineering-decisions` 这八个根，`resolved_14` 恒为 `True`，并排命名**完全不参与判定**——只认 `docs/en/` 与 `docs/zh-CN/` 两个目录。

于是：

| 形态 | 04/06/08 等八个根 | 14-ai-development |
|---|---|---|
| `X.md` + `X.zh-CN.md` 并排 | **缺口** | 需 `docs/` 镜像才算 |
| `X.md` + `X.en.md` 并排 | **缺口** | `resolved_14` 通过，但仍需 `docs/` 镜像 |
| 根 + `docs/en` + `docs/zh-CN` | 通过 | 通过 |
| 仅 `docs/en` + `docs/zh-CN`（无根） | 通过 | 通过 |

**并排双语只对 `14-ai-development` 有效，对其他八个根完全无效。**

## 2. 因此这五个 PR 面临的是同一个选择

要么：

**(a) 补 `docs/en` + `docs/zh-CN` 镜像** — 但这意味着同一份正文存三份（根 / `docs/en` / `docs/zh-CN`），正是 Owner 在 #318 裁定边界中禁止的「为迎合扫描结果复制正文」；

要么：

**(b) 删掉根目录正文，只留 `docs/en` + `docs/zh-CN`** — 但这违反仓库既有惯例，且会让 `04-memory-compiler/` 下出现「没有根文件」的目录结构，与 `08-bmcp-protocol/` 等其他根不一致；

要么：

**(c) 进 `EMBEDDED_BILINGUAL_SOURCES` 豁免清单** — 但这需要逐条治理批准，Owner 已明确「不得作为新增登记的默认通道」。

**三条路都有代价，没有一条是「改一下 PR 就能过」。**

## 3. #429 是另一种失败

#429 `EXIT=1`、`err=1`、`gap=0`。唯一错误不是缺口，是 §2 之外的规则。这条需要单独看，但它同样不是「PR 内容错」。

## 4. 这条数据改变了什么

Owner 裁定 D 说「开发继续，六项工作量推进」。这九个数说明：

> **六项工作量里，凡是要在 `NORMATIVE_ROOTS` 根目录新增规范文档的部分，当前都无法通过门禁——不是因为写得不对，而是因为门禁只承认一种目录形态，而这种形态与仓库既有惯例冲突。**

具体到六项：

| 工作量 | 相关 PR | 门禁 | 含义 |
|---|---|---|---|
| Memory Compiler 核心 | #425 失败、#429 通过 | 1/2 | 新增契约文档被拒；改已有文档可行 |
| Memory Context 引擎 | #433 失败、#434/#444 通过 | 2/3 | **测试能进，规范不能进** |
| Agent Integration | #430 通过 | 1/1 | 用三件套，通过 |
| BMCP 协议栈 | #428 通过（在 `reviews/`）、#436 失败 | 1/2 | 换个目录就能过 |
| Phase 2/3 领域模型 | #435 失败 | 0/1 | **无法启动** |
| 端到端测试 | #444 通过（本地无法复现，见 §5） | 1/1 | — |

**两个结构性偏差：**

**第一，代码和测试完全不受双语门禁约束。** 门禁只扫 `NORMATIVE_ROOTS` 下的 `*.md`。于是持续推进的结果会是：实现越写越多，而解释实现的规范停在门外。#433 vs #434/#444 就是这个偏差的直接样本。

**第二，绕过门禁的方法比满足门禁更容易。** #428 把文档放进 `reviews/` 就通过了；#430 补三件套也通过了。两者都是「换个地方写」或「多写两份」，没有一个是「把并排双语变成合法形态」。这解释了为什么九个人各写了九种形态——**门禁没有告诉任何人正确形态是什么，只告诉了他们错误形态是什么。**

## 5. 附：#444 本地无法复现（环境限制，非 PR 缺陷）

#444 是唯一真正属于「端到端测试」的 PR（Rust 集成测试，`crates/memory-context/tests/e2e_store_to_context.rs`，178 行）。

本地尝试：

```
$ cargo test --offline -p memory-context --test e2e_store_to_context
error occurred in cc-rs: gcc.exe: fatal error: cannot execute 'cc1'
```

`libsqlite3-sys` 需要 C 编译器编译 sqlite3 源码，本机 gcc 缺 `cc1`（MinGW 安装不完整）。**这是环境缺陷，不是 PR 缺陷。** 记录在此以免被误读为「#444 测试失败」。

`cargo build -p memory-context` 在 main 上通过（11.33s），说明 crate 本身可编译，只是 sqlite 的 C 依赖无法构建。

## 6. 复现方式

```bash
# 真实克隆，main c138654c94
for PR in 425 428 429 430 433 434 435 436 444; do
  git reset --hard origin/main && git clean -qfd
  # 取该 PR 的 changed files，按 blob SHA-1 校验后落盘
  git add -A && git commit -m "sim $PR"
  BASE_SHA=$(git rev-parse origin/main) HEAD_SHA=$(git rev-parse HEAD) \
    PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
done
```

## 7. 本登记不主张的事

- 不主张这五个 PR 应被关闭。它们是**内容正确、形态不被门禁接受**。
- 不主张应放宽门禁。§1 的规则本身有道理（规范必须双语可寻），问题在于它对八个根只承认一种形态。
- 不主张我已解决这个问题。我只测出了它。
- 不把 #444 的本地失败算作 PR 缺陷（§5）。

## 8. 需要裁定的一件事

九个 PR 里五个卡在同一个形态问题上。这不是九次独立判断，是**一次判断**：

> 对 `NORMATIVE_ROOTS` 下非 `14-ai-development` 的八个根，并排 `.zh-CN.md` 是否应被承认为合法配对？

- 若**应承认**：改 `resolved_14` 的适用范围，一行改动，五个 PR 全部解除。但这是一次规范变更，需独立审查。
- 若**不应承认**：那仓库里既有的并排文件全部是历史遗留，新文件一律必须走 `docs/` 镜像，等于把「根目录正文」这个惯例逐步淘汰。这需要明确说明，否则每个新 PR 都会撞一次。

**这两个选项都需要 Owner 裁定，我不替它选。**
