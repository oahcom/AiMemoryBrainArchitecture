# GOV-NC-2026-11-21-REGRESSION-009

- 登记编号：GOV-NC-2026-11-21-REGRESSION-009
- 状态：`OPEN` / `ACTIVE` / main 在解除 45 分钟后**再次红**
- 发现时间：2026-11-21T07:35Z
- 观测对象：仓库 `oahcom/AiMemoryBrainArchitecture`，main `277daec7d0c6`
- 前置登记：006（死锁，已解除）、007（自我审查）、008（门禁零审查合并）

## 1. 结论先行

006 记录的「main 上门禁对空 diff 恒为 `EXIT=2`」在 `81dd9a72d2` 被解除（#418，F-1）。**45 分钟后它在 `1ad6c2cf67` 复发。**

```
$ # main 277daec7d0c6 的干净树
$ BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
    python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
EXIT=2
```

死锁解除与复发之间，**没有任何一次独立审查**。

## 2. 事实

### 2.1 复发链

| # | commit | 时间 | 身份 | 动作 | 是否经 PR |
|---|---|---|---|---|---|
| 1 | `ae37a419` | 04:50:35Z | — | 引入未配对规范文档，造成首次死锁 | 否（直推） |
| 2 | `fce40834` | 05:51:45Z | `oahcom` | #418 用 F-1 解除（+5 行豁免） | 是，**自我审查 12 秒** |
| 3 | `1ad6c2cf67` | 07:08:25Z | **`Owner-A <owner-a@local>`** | 新增 `14-ai-development/work-items/GAP-BASELINE-001.md`（+160 行），**造成第二次死锁** | **否（直推）** |
| 4 | `47b8600e75` | 07:15:33Z | `Owner-A` | 修改同一文件（+10 −3） | **否（直推）** |

### 2.2 第六个提交身份

`Owner-A <owner-a@local>`，首次出现在 `1ad6c2cf67`（2026-11-21T07:08:25Z）。

本系列此前记录的五个：`oahcom`、`unknown <1491856051>`、`governance@localhost`、`oahcom <noreply@github.com>`（网页提交）、`Ubuntu <ubuntu@localhost.localdomain>`。

**`Owner-A` 这个名字本身值得注意**：`Owner` 是本治理体系中具有裁定权的角色。而这个身份：

- 未经任何 PR；
- 新增了一个使 main 变红的规范文件；
- 45 分钟前刚有人修好同一个问题。

### 2.3 最近 20 个 main 提交的身份分布

```
14  oahcom <81014746+oahcom@users.noreply.github.com>
 4  unknown <1491856051>
 2  Owner-A <owner-a@local>
```

三个身份，零个 PR（`oahcom` 的两个是 `Merge PR #415` / `Merge PR #418`，其余均为直推或网页提交）。

### 2.4 `GAP-BASELINE-001.md` 为什么是缺口

该文件位于 `14-ai-development/work-items/`，是 `NORMATIVE_ROOTS` 下的 `.md`。按 006 §13.1 的机制：

- 无 `docs/en/` 与 `docs/zh-CN/` 双侧镜像 → `current_bilingual_gaps()` 判定为缺口；
- 不在 `scripts/bilingual-baseline.txt`（207 条）中 → 基线外；
- 未进 `EMBEDDED_BILINGUAL_SOURCES`。

三项都不满足，于是 `EXIT=2`。

而 `work-items/` 下已有 73 条路径在基线里（见 006 §13 的同类统计），说明这个目录历来靠基线豁免，而基线只能收缩。

### 2.5 该文件自己的内容

文件名 `GAP-BASELINE-001` 与它的提交消息值得直接引用：

```
1ad6c2cf67  docs(work-items): freeze GAP-BASELINE-001 with re-measured six-area state
47b8600e75  docs(work-items): resolve GAP-BASELINE-001 baseline SHA ambiguity
```

也就是说：**这份文件讨论的正是「基线」，而它自己成了基线外的缺口。** 这不是修辞，是实测结果。

## 3. 死锁的复发说明什么

006 §12 记录解除时说得很清楚：解除**在技术上有效**，但**程序未满足 §5**（自我审查，12 秒）。

`1ad6c2cf67` 证明了这个区别不是形式主义的：**一个没有经过独立审查的修复，不能防止同类问题再次发生，因为没有任何机制把「为什么红」变成「以后不要这样做」。**

三次事件的结构完全同形：

| 事件 | 引入方式 | 造成 | 修复方式 |
|---|---|---|---|
| `ae37a419` | 直推 | 死锁 #1 | #418 自我审查 |
| `1ad6c2cf67` | 直推 | 死锁 #2 | 尚未修复 |

同一个错误，同一个通道，45 分钟。

## 4. 与 008 的关系

008 记录 #423 以 `reviews=0` 修改了门禁实现（+110 −3），修复了「豁免可自注册」。

`1ad6c2cf67` 出现在 #423 合并（06:59:08Z）之后 9 分钟。所以：

- #423 修的是「已存在文件不得在同 commit 自注册豁免」；
- `1ad6c2cf67` 既没有注册豁免，也没有加镜像——它只是**新增了一个未配对文件**，这从来就是被禁止的，不需要新判据。

因此不能说 #423 的修复无效。准确的表述是：**#423 修的是自注册这条特定通道，而 `1ad6c2cf67` 走的是最原始的那条通道——直接新增未配对文件，不碰豁免表。这条通道从 `ae37a419` 到 `1ad6c2cf67` 一直开着。**

## 5. 本登记不作出的推断

- **不判定** `Owner-A` 是「冒充」Owner 角色。`Owner-A <owner-a@local>` 只是一个 git 身份字符串，任何人都能配置。本登记只记录它存在、它直推、它造成 main 变红。
- **不判定** `GAP-BASELINE-001.md` 的内容有问题。它可能是一份有价值的记录；问题只在于它的落盘方式使 main 变红。
- **不判定** 这是故意破坏。证据只支持「未经 PR、未经门禁、造成 `EXIT=2`」。
- **不把**复发读成 006 的结论错误。006 说的是「当时不可满足」，那是对的；复发是**新的事实**，不是对旧结论的否定。

## 6. 一个可检验的判据

如果要防止第三次，需要一条现在不存在的约束：

> 对 `main` 的每一次写入，无论来源身份，都必须先经过一次能返回 `EXIT=0` 的门禁执行。

现在的状态是：`main` 可以被任意身份直推，而门禁只在 PR 上跑，且（005）从未真正执行过。所以这条约束**在两条路径上都为空**：PR 路径没有执行，直推路径没有检查。

## 7. 复现

```bash
# 1) main 上空 diff 为 EXIT=2
git clone --depth 1 https://github.com/oahcom/AiMemoryBrainArchitecture.git
cd AiMemoryBrainArchitecture
SHA=$(git rev-parse HEAD)
BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"
# -> ::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
# -> EXIT=2

# 2) 该文件不在基线
grep -c "GAP-BASELINE-001" scripts/bilingual-baseline.txt   # -> 0
grep -vc "^#" scripts/bilingual-baseline.txt                # -> 207

# 3) 引入提交与身份
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/1ad6c2cf67 \
  | jq '{author: .commit.author, parents: [.parents[].sha], files: [.files[] | {filename, additions}]}'
```

**登记状态**：`OPEN` / `ACTIVE` / main `277daec7d0c6` 空 diff `EXIT=2` / 引入身份 `Owner-A <owner-a@local>` / 直推无 PR / 006 的死锁在解除后 45 分钟复发

---

## 8. 补充实测：main 红着的时候，任何 PR 都无法通过

### 8.1 隔离实验

在 main `a730880efdae` 的干净树上：

```
=== 仅 base，空 diff ===
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
EXIT=2
```

加上本 PR 的 15 个文件（每个登记根中文 / `docs/en` 英文 / `docs/zh-CN` 中文）：

```
=== 15 文件 + 同一 base ===
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
EXIT=2
```

**同一句错误，只因为全树扫描与 diff 无关。** 15 个文件全部配对正确，不影响判定。

### 8.2 删掉那个文件后，15 个文件被判为完全合规

在同一树上删除 `14-ai-development/work-items/GAP-BASELINE-001.md`：

```
bilingual baseline: 207 frozen, 0 new gaps
EXIT=1   （唯一原因见 8.3）
```

按错误类型分类：

| 类别 | 条数 | 说明 |
|---|---|---|
| `New bilingual gap outside frozen baseline` | **0** | 本 PR 的 15 个文件没有产生任何新缺口 |
| `Embedded bilingual source … registered in the same commit` | 21 | 全部指向 `84831075`，即我本地合成的 base 提交（见 8.3） |
| `Normative source left NORMATIVE_ROOTS by deletion` | 1 | 删除 `GAP-BASELINE-001.md` 本身触发的规则 |

**0 条新缺口**是这一节最关键的数：它证明 §8.1 的 `EXIT=2` 完全来自 main 上的既有缺口，与 PR 内容无关。

### 8.3 21 条同 commit 注册错误是我的环境缺陷，不是仓库缺陷

这 21 条全部指向 `84831075`——我为本次实测把 main 树 `git init` 成一个新仓库并做单次提交，于是所有历史都压成一个 commit。`check_embedded_registration_history()` 用 `git log --diff-filter=A` 判断「文件创建提交」，在压平的历史里每个文件的创建提交都是 `84831075`，而豁免注册也在同一个 `84831075`，于是全部报错。

真实仓库的 770 个提交里这些文件的创建与注册分布在不同 commit，不会触发。**这 21 条不能作为 #423 有缺陷的证据**，只能作为「该判据依赖真实历史」的旁证（008 §6 已记录同一性质）。

### 8.4 由此得到的闭合性结论

> **当 main 上存在基线外缺口时，任何基于 main 的 PR 都无法通过双语门禁，无论该 PR 改了什么、改得多正确。**

这与 006 §2.1 的「判定域是 diff 而非树」形成对照：

- **配对检查**（`check_mirror_pairing`）判定域是 diff——只查本次改动的路径；
- **缺口检查**（`current_bilingual_gaps` vs baseline）判定域是**整棵树**——与本次改动无关。

所以「PR 只要自己配对正确就能过」是错的。**只要主干上有未修的红，所有 PR 一律 `EXIT=2`。** 这正是 `1ad6c2cf67` 造成的实际后果：它不只让 main 红，它让**整个 PR 通道失效**。

### 8.5 对 005 的叠加

005 记录：36 小时内门禁裁决 0 次，合并 85 次。

现在加上这一层：即使有人想走 PR 通道，**在 `1ad6c2cf67` 之后也不可能拿到 `EXIT=0`**。于是：

| 通道 | 状态 |
|---|---|
| PR + CI | 从未执行（005） |
| PR + 本地门禁 | main 红则恒为 `EXIT=2`（本节） |
| 直推 main | 无门禁（009 §6） |

三条通道全部为空。这不是「门禁太严」，是**门禁在任何路径上都不产生有效裁决**。

---

## 9. Owner 裁定：维持 §5，两个 PR 一并等待（选择 (b)）

### 9.1 裁定要点

面对「#440 修复 base 与 #422 验收互为死锁」这一结构，Owner 明确选择 **(b) 维持 §5 要求**，而非 (a) 由 Owner 直接裁定合并：

> 宁可明确承认当前 PR 通道因独立审查主体缺位而阻塞，也不以一次未经独立验证的紧急合并，制造新的治理例外。

裁定同时否决了「修复性变更可免除独立审查」这一理由，理由是 #440 含**完整中文翻译**，且译文承载规范效力（「明确的非主张」「派发规则」两节），因此不是单纯复制，而是**对治理文本语义的转换**。

### 9.2 一处事实更正被接受

裁定撤销了上一轮「根目录 `GAP-BASELINE-001.md` 是中文权威正文」的描述。实测：

```
$ # main a730880efdae 上的根文件
# GAP-BASELINE-001 — Key Missing Workload Baseline
- Repository: `oahcom/AiMemoryBrainArchitecture`
...
8460 bytes, 全英文
```

因此实际结构为：

| 路径 | 语言与角色 |
|---|---|
| 根目录 `GAP-BASELINE-001.md` | 既有英文源文件，**未修改** |
| `docs/en/.../GAP-BASELINE-001.md` | 根文件逐字英文镜像 |
| `docs/zh-CN/.../GAP-BASELINE-001.md` | 完整中文翻译 |

**这条更正本身值得记录**：它说明「根目录 = 中文权威」是一个未经核实的假定，而仓库里至少有一个规范文件是英文写的。任何依赖该假定的门禁设计或治理判断都应重新核对。

### 9.3 阻塞链与解除条件

```
#440 独立审查          ← 卡在这里
       ↓
#440 合并
       ↓
main 整树缺口修复
       ↓
main 空 diff 验证
       ↓
#422 exact-head 重测
       ↓
#422 独立审查与验收
```

解除条件（裁定原文要点）：

1. 指定一个与 #440 作者及合并者不同的审查身份；
2. 对英文源文件、英文镜像、中文翻译逐项核对；
3. 确认中文没有遗漏、改变或扩大原文规范效力；
4. 审查者明确给出独立审查结论；
5. 满足既有合并要求后，才进入合并决策。

并明确：**S-2 未指定身份不等于可以降低独立性标准**；但也不要求永远等待同一个尚未命名的账号——只要有真实、具备授权的独立审查者并满足身份分离，即可完成。

### 9.4 本地 `EXIT=1` 的证据效力被限定

裁定接受我的归因，但限定其效力：

| 命题 | 是否成立 |
|---|---|
| #440 消除了 `GAP-BASELINE-001.md` 对应的整树缺口 | 成立（实测 0 条 gap 错误） |
| 21 条同 commit 注册错误是测试装置伪影 | 成立，不作为仓库缺陷 |
| 本地 `EXIT=1` 证明真实仓库合并后门禁会失败 | **不成立** |
| 本地 `EXIT=1` 证明真实仓库合并后门禁会通过 | **不成立** |

所以「合并后在真实 main 历史上验证空 diff」这一步不可省略，本地模拟不能替代。

### 9.5 裁定后的状态

| 项目 | 状态 |
|---|---|
| #440 | `OPEN / PENDING_INDEPENDENT_REVIEW` |
| #422 | `OPEN / BLOCKED_BY_BASE_REPAIR` |
| #419 | `CLOSED_UNMERGED` |
| #423 | `MERGED / PROCEDURALLY_NONCOMPLIANT / AUDIT_PENDING` |
| main 双语门禁 | `BLOCKED_BY_GAP_BASELINE_001`，等待真实修复 |
| S-2 第二身份 | `APPROVED_IN_PRINCIPLE / IDENTITY_NOT_ASSIGNED` |
| Sponsor / Accountable Owner | `NOT_ASSIGNED` |
| AID-2026-023/024/026 R2 | `NOT_AUTHORIZED` |

### 9.6 这一裁定本身的意义

§9 记录的不是「又阻塞了一次」，而是一个**结构性事实**：

> 门禁的执行、base 的修复、审查的独立性，三者互为前提，而其中任何一项都依赖一个尚未存在的主体。

006 记录门禁不可满足；005 记录门禁从未执行；007 记录审查无独立性；008 记录判据被零审查修改；009 记录死锁复发且使整个 PR 通道失效。

**这五条合起来指向同一个结论：问题不在某一次合并、某一个文件、某一个身份，而在于「谁有权做出裁决」这个位置是空的。**

裁定选择 (b)，等于承认这个空位不能用「作者兼任审查者」填补。这是本系列登记中第一次，一个阻塞被明确保留而非绕过。
