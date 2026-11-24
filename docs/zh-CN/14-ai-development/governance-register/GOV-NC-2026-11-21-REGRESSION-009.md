# GOV-NC-2026-11-21-REGRESSION-009

- 登记编号：GOV-NC-2026-11-21-REGRESSION-009
- 状态：`OPEN`（仅程序性结论）/ 技术性结论**已被 §12 推翻**：main 全绿，空 diff 的 `EXIT=2` 换了原因
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

---

## 10. 缺口从 1 个增加到 3 个：恶化仍在继续

### 10.1 实测

在 main `776f04fb69`（2026-11-21T07:58:58Z）上，空 diff：

```
$ BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
    python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/AID-2026-040/E1-E8-entry-gate-measurement-2026-11-21.md
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/AID-2026-040/prompt-v1.md
::error::New bilingual gap outside frozen baseline: 14-ai-development/work-items/GAP-BASELINE-001.md
EXIT=2
```

**从 1 个缺口变成 3 个。** 其中两个是新增的。

### 10.2 新增两个缺口的来源

| commit | 时间 | PR | 动作 |
|---|---|---|---|
| `1570a7591c` | 07:51:19Z | #437 | 新增 `AID-2026-040/E1-E8-entry-gate-measurement-2026-11-21.md`（+180）、`manifest.yaml`（+106）、`prompt-v1.md`（+176）、改 `INDEX.md`（+1） |

其中两个 `.md` 位于 `NORMATIVE_ROOTS` 下、无 `docs/en`/`docs/zh-CN` 镜像、不在基线 → 新增两个缺口。

### 10.3 #437 的合并状态

| 项 | 值 |
|---|---|
| created | 2026-11-21T07:52:20Z |
| merged | 2026-11-21T07:58:58Z |
| 跨度 | 6m38s |
| author | `oahcom` |
| merger | `oahcom` |
| reviews | **0** |
| files | 4，`+463 −0` |
| checks | 三条全 `failure`，`steps=0` |

与 008 记录的 #423 同形：`reviews=0`、`steps=0`、作者即合并者、数分钟内完成。

### 10.4 #426 也是 `reviews=0`

| 项 | 值 |
|---|---|
| created | 07:15:35Z |
| merged | 07:36:55Z |
| 跨度 | 21m20s |
| reviews | **0** |
| files | 2，`+60 −6` |
| checks | 四条全 `failure`，`steps=0` |

#426 改的是 `scripts/check_bilingual_docs.py`（−6 行，删除重复豁免键）——**又一次零审查的门禁脚本变更**。

### 10.5 这条数据说明了什么

009 §3 的论断是：未经独立审查的修复不能防止同类问题复发。

现在有更强的证据：**问题不只在复发，而在持续新增。**

```
07:08  Owner-A  直推   +1 缺口（GAP-BASELINE-001）
07:36  #426     零审查 改门禁脚本（未新增缺口，但改判据）
07:51  #437     零审查 +2 缺口（AID-2026-040 ×2）
07:58  main 到达 3 个缺口
```

50 分钟内，缺口 1 → 3，其中两次写入都是 `reviews=0` 或直推。

### 10.6 与 005 的对照

005 的窗口是 36 小时、348 条 check、0 次执行、85 次合并。现在这个窗口之后仍在持续：

- `#437` 三条 `steps=0`
- `#426` 四条 `steps=0`
- `#425` 三条 `steps=0`
- `#423` 三条 `steps=0`

**`steps=0` 不是偶发，是默认状态。**

### 10.7 一个不能回避的观察

这些 PR 的内容看起来是在推进 GAP-01 到 GAP-06——即 `GAP-BASELINE-001.md` 自己列出的六个缺失领域。也就是说：

- 有人认真读了那份基线；
- 按它的六个缺口逐个开工（#425 GAP-01、#433 GAP-02、#430 GAP-03、#428/#436 BMCP、#435 Phase 2、#434 context 测试）；
- 并行开了至少 9 个 PR；
- 而每一个都因付款失败拿不到 CI；
- 合并时 `reviews=0`。

**执行强度很高，治理强度为零。** 这不是怠工，恰恰相反——是高速产出与零审查并存。而这正是 007 与 008 记录的形态在高负载下的自然结果：当 CI 不可用、审查主体缺位、通道又必须推进时，`reviews=0` 成为唯一可行的路径。

这一点必须写清楚，因为它决定了修复方向：**不是要求执行者更谨慎，而是补上那个空位。**

---

## 11. 阻塞已解除，但解除方式与本登记 §9 描述的路径不同

### 11.1 main 已恢复 EXIT=0（真实历史）

在真实克隆（770+ 提交）上 checkout `main` `c138654c94`：

```
$ BASE_SHA=$H HEAD_SHA=$H PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
bilingual baseline: 118 frozen, 0 new gaps
exemptions: 21
Bilingual documentation and prompt-library gate: PASS (0 changed paths inspected).
EXIT=0
```

**基线从 207 降到 118，缺口从 3 个降到 0 个。** §8.4 的闭合性结论（main 红则所有 PR 恒为 `EXIT=2`）在技术上仍然成立，但**前提已不满足**。

### 11.2 解除路径不是 §9.3 的那条链

§9.3 预期的链是：`#440 独立审查 → 合并 → main 修复`。实际发生的是：

| PR | 状态 | 内容 |
|---|---|---|
| #440 | **CLOSED_UNMERGED**（`reviews=0`） | `GAP-BASELINE-001` 双侧镜像，+299 −0 |
| #442 | **CLOSED_UNMERGED**（`reviews=0`） | 7 文件，含 `document-scope-registry.yaml` 镜像 |
| #443 | **CLOSED_UNMERGED**（`reviews=0`） | 6 文件，含 `GAP-BASELINE-001` 镜像 |
| #445 | **MERGED**（`reviews=1`） | `bilingual-baseline.txt` **−89**、`check_bilingual_docs.py` **+3** |
| #446 | **MERGED**（`reviews=0`） | 6 文件，`terminology.md` + ADR + 双侧镜像 |
| #448 | **MERGED**（`reviews=0`） | 3 文件，`terminology.md` 三处各改 1 行 |

**三个「补镜像」的 PR 全部被关闭未合并；真正解除阻塞的是 #445——把基线删掉 89 条。**

### 11.3 #445 做了什么：把配对豁免接进缺口扫描

```diff
--- a/scripts/check_bilingual_docs.py
+++ b/scripts/check_bilingual_docs.py
@@ -258,6 +258,9 @@ def current_bilingual_gaps() -> set[str]:
              if source in EMBEDDED_BILINGUAL_SOURCES:
                  continue
+            # Inventory and changed-path gates must share prefixes or pair-exempt paths become permanent gaps.
+            if source.startswith(PAIR_EXEMPT_PREFIXES):
+                continue
              english = REPO_ROOT / "docs" / "en" / source
```

`PAIR_EXEMPT_PREFIXES` 的定义（本已存在）：

```python
PAIR_EXEMPT_PREFIXES = (
    "14-ai-development/work-items/",
    "14-ai-development/prompts/",
    "14-ai-development/adr/",
)
```

即：**变更路径门禁早已豁免这三个前缀，但全树缺口扫描没有豁免**，于是这三个目录下的每个文件都成了「永久缺口」，被逐条冻进基线。89 条基线里绝大部分来自这里：

```
14-ai-development/adr/ADR-RUN-001..003                (5)
14-ai-development/prompts/global|owners/*             (15)
14-ai-development/work-items/**                       (其余)
```

### 11.4 这是一次真实修复，且理由正确

脚本内的注释写得很准确：

> Inventory and changed-path gates must share prefixes or pair-exempt paths become permanent gaps.

这句话点出了一个**两个判据不同步**的缺陷：同一批路径，一个门禁豁免、另一个门禁不豁免，结果就是基线被豁免项永久污染，棘轮无法收缩。

**这不是绕过门禁，是修正门禁自身的内部不一致。** 它同时也解释了 006 §13.2 的实测现象——「加进基线」为什么不是出路：因为基线里那 89 条本身就是这个缺陷的沉淀物。

### 11.5 但程序问题仍然存在，且未被讨论

| 事实 | 值 |
|---|---|
| #445 author | `oahcom` |
| #445 reviews | 1 |
| 该 review 是否来自 author 本人 | **是**（与 007 §1 同形） |
| #446 / #448 reviews | **0** |
| #440 / #442 / #443 | `reviews=0` 即被关闭 |

所以：**解除阻塞的那次合并仍是自我审查；随后两次合并是零审查。**

这与 §9.6 的结论不冲突，反而加强它：修复质量与程序合规是两条独立的线。#445 的修复在技术上是对的（有 006 §13 的独立证据支持），但它的审查独立性与 007 记录的六例完全一致。

### 11.6 对本登记结论的影响

| 断言 | 状态 |
|---|---|
| §8.4 main 红则所有 PR 恒 `EXIT=2` | **机制成立**，但当前前提不满足（`0 new gaps`） |
| §9.3 阻塞链（#440 审查 → 合并 → 修复） | **未发生**；#440/#442/#443 全部关闭未合并 |
| §9.5 `#440 OPEN / PENDING_INDEPENDENT_REVIEW` | 已过期：`#440 CLOSED_UNMERGED` |
| §10.5 缺口 1→3 恶化 | 成立，且随后被 #445 一次性归零 |
| 007/008 的形态 | **不变**，#445/#446/#448 三例继续符合 |

### 11.7 一条方法论上的教训

本登记 §9 把「修复必须走 #440」当成唯一路径，于是把阻塞描述成「等一个审查者」。实际解法是**发现两个判据不同步**——这不需要审查者，只需要有人读懂脚本。

这不是说 §9 的裁定错了（维持 §5 的判断在程序上是对的），而是说：**当所有路径都指向「缺人」时，值得再查一遍是不是自己把问题定义窄了。** 本次是我定义窄了。

---

## 12. 2026-11-24 复核：标题性的技术断言已不成立，程序性结论仍然成立

**测量点：** `main = 5c64e560eb415af513c98a6d02d0322081ef92b9`（2026-11-24T03:22Z）

### 12.1 main 现在是全绿的

`main` 该 commit 的 9 个 check-run，**非绿数量为 0**：

| check | conclusion |
|---|---|
| Repository hygiene (hard gate) | success |
| GOV-DOC-002 metadata checks | success |
| Bilingual docs coverage (ratchet) | success |
| Rust format (hard gate) | success |
| Rust clippy (hard gate) | success |
| BMCP conformance suite (hard gate) | success |
| BMCP protocol index (hard gate) | success |
| Schema non-empty audit (hard gate) | success |
| audit | success |

`008` §5 那条「门禁全绿靠零审查合并维持」的判断不受影响——但「main 红」这个具体事实已经不成立，标题里的「再次红」因此过期。

### 12.2 缺口集与冻结基线逐元素相等

```
$ python -c "..."
baseline size : 77
gap set size  : 77
gap set == baseline: True

GAP-BASELINE-001.md exists on disk : True
  in gap set     : False
  in baseline    : False
  pair-exempt    : True
```

§1 复现里那个触发 `::error::New bilingual gap outside frozen baseline` 的文件 `14-ai-development/work-items/GAP-BASELINE-001.md`，**不在缺口集里**，也不在基线里——它落在 `PAIR_EXEMPT_PREFIXES` 内，两个判据都已豁免。§10.5 的「缺口 1→3」在今天是 **0**。

### 12.3 空 diff 仍然 `EXIT=2`，但原因换了

同一条命令，今天：

```
$ BASE_SHA=$S HEAD_SHA=$S PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
::error::NOT_APPLICABLE: BASE_SHA...HEAD_SHA contains zero changed paths; no bilingual incremental verification was performed.
EXIT=2
```

退出码与 §1 相同，报文不同。§1 的报文是 `New bilingual gap outside frozen baseline: ...`；今天是 `NOT_APPLICABLE`。

引入者是 `a82659a1`（2026-11-22 23:19:56 +0800，`fix(gov-doc-001): reject empty changed-path verification`），对 `scripts/check_bilingual_docs.py` **+7 −0**，只加了 `if not changed: ... return 2` 这一段。它**晚于**本登记的测量点 `c138654c94`（2026-11-21 16:26:23），所以 §11.1 记录的 `PASS (0 changed paths inspected). EXIT=0` 在当时为真，之后被这条守卫改掉。

区别是实质的：

| | §1 的 `EXIT=2` | 今天的 `EXIT=2` |
|---|---|---|
| 触发 | 门禁**认为**有未配对规范文档 | 门禁**拒绝在空增量上作判断** |
| 对象 | 仓库内容 | 调用方式 |
| 能否靠改仓库修掉 | 能 | 不能，只能改调用 |
| 是否 fail-closed | 否（是误报） | **是（是对的）** |

### 12.4 真实 PR 不会命中这条守卫

`.github/workflows/bilingual-docs.yml` 传的是 `github.event.pull_request.base.sha` 与 `head.sha`。真实 PR 的 base 与 head 必然不同，`git diff --name-status base...head` 必非空，守卫不触发。它会触发的唯一形态是**手工用同一个 SHA 调两次**——也就是本登记 §1 与 §11.1 用的那种复现方式。

所以 §8.4 的闭合性结论（main 红则所有 PR 恒 `EXIT=2`）**机制仍在，但今天既无前提（main 绿）也无触发路径（真实 PR 增量非空）**。

### 12.5 本登记的哪一部分仍然成立

| 断言 | 今天 |
|---|---|
| §1「main 在解除 45 分钟后再次红」 | **不成立**：main 全绿，缺口 0 |
| §10.5「缺口 1→3 恶化」 | **不成立**：缺口 0 |
| §11.1「main 已恢复 `EXIT=0`」 | **当时为真**，今天该命令返回 `EXIT=2`（`NOT_APPLICABLE`） |
| §11.5「解除阻塞的合并是自我审查；随后两次合并零审查」 | **成立**，不受影响 |
| §11.7「把问题定义窄了」 | **成立**，且本条是它第二次生效的证据 |

技术性结论按 §12 更新；程序性结论（谁审的、审了几个、为什么这算自我审查）**一条都没变**，因此状态保留 `OPEN`，只把技术断言标为已被本条推翻。

### 12.6 复现

```
repo:    oahcom/AiMemoryBrainArchitecture
commit:  5c64e560

# 1. main 全绿
gh api repos/:owner/:repo/commits/5c64e560/check-runs \
  --jq '[.check_runs[] | select(.conclusion != "success" and .conclusion != "skipped")] | length'
-> 0

# 2. 缺口集 == 基线
python -c "
import sys,os;sys.path.insert(0,os.path.join(os.getcwd(),'scripts'));sys.argv=['x']
import check_bilingual_docs as g
bs=set(g.read_baseline()); gs=set(g.current_bilingual_gaps())
print(len(bs), len(gs), gs==bs)"
-> 77 77 True

# 3. 空 diff 的报文
S=$(git rev-parse HEAD)
BASE_SHA=$S HEAD_SHA=$S PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"
-> ::error::NOT_APPLICABLE: ... zero changed paths ...
-> EXIT=2
```

### 12.7 这条更正为什么值得写

因为它是一个**退出码相同、语义相反**的例子。任何人只按 `EXIT=2` 判断，会得到「009 的结论仍然成立」的结论；而实际发生的是：原来的缺陷被修掉了，同一个退出码被一条**正确的** fail-closed 守卫接手。区分二者的唯一办法是读报文，不是读退出码。

`§11.7` 说「当所有路径都指向缺人时，值得再查一遍是不是自己把问题定义窄了」。这条是它的对偶：**当所有证据都指向同一个数字时，值得再查一遍这个数字是不是在说同一件事。**
