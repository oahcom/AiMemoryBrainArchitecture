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
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "§1-§7 measured at main 2059c8105; §8 re-measured at main 84bbe9241. Every §8 row is one real invocation of scripts/check_bilingual_docs.py on a worktree reset to origin/main before the single commit under test, with the exit code recorded. Cases F and G exit 0, which is the evidence that no code reads docs/zh-CN content. Cases D, H, I exit non-zero, which refutes the inference that deleting a Chinese mirror goes unannounced. The baseline is 80 lines = 3 comments + 77 entries; none of the 7 content defects appears among those 77 entries. The pair count moved 123 -> 124 between the two measurement points because main gained files. §5 was corrected 2026-11-24 15:52 +0800 after #893 (e894865) and #896 (84bbe924) were found: the admission function returns True for work-item manifests at merge point 3026b31, and #896 used that channel to register AID-2026-055. Every §5 figure was re-run at that merge point; the suite figures and the two mutation results were re-run too and reproduced exactly."
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
    source: "14-ai-development/governance-register/GOV-REV-2026-11-24-FOUR-CORRECTIONS-033.md"
    en: "docs/en/14-ai-development/governance-register/GOV-REV-2026-11-24-FOUR-CORRECTIONS-033.md"
    zh-CN: null
---

# GOV-REV-2026-11-24-FOUR-CORRECTIONS-033

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION` / §8 added 2026-11-24
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 2059c8105` (§1–§4), `main = 84bbe9241` (§8), `main = 3026b31` (§5, re-measured 2026-11-24 15:52 +0800)
**Register author:** orchestrator session acting as owner-proxy. **Not** an independent reviewer, **not** the accountable owner.

---

## 1. 四条更正，三条打在我自己身上

本文件写在 `REGISTER-INDEX-031` 与 `DISPATCH-CHANNEL-CLOSED-032` 合并后一小时内。合并期间主干前进了三支，其中一支直接拆掉了我在 030 上引用的事实。

| # | 我此前写的 | 现在的实测 | 判定 |
|---|---|---|---|
| 1 | 030 §4/§6：52 个测试、24 个问题、无 workflow 运行 | `Ran 52 tests / OK`；`bilingual-docs.yml:27` 已运行 | **已被 `aaf6da966`（#892）修掉** |
| 2 | 「24 个问题」的存在意味着套件不能被杀 | 两个变异测试都杀掉了它 | **我的推断错**：它是能失败的 |
| 3 | 032 §6：把该工单保留待放行 | 工作已完成，工单内容作废 | **我保留的东西已无对象** |
| 4 | GAP-24：zh-CN 镜像是英文文件 | 123 对里 2 对逐字节相同，**方向相反** | **GAP-24 少算且只描述了一个方向** |

032 §1–§5（发派通道关闭）**不再成立**：§5 的更正显示准入通道自 `#893` 起已打开，`#896` 已用它登记了 `AID-2026-055`。032 §1/§3 由此失效，详见 §5.3。

---

## 2. 030 §4 与 §6 已被修掉，且修得对

`aaf6da966`（#892，2026-11-24 13:49:49 +0800）在我测量之后合入。同一台机器、同一条命令：

| 时点 | 输出 |
|---|---|
| `main` `ef7266db`（我测量时） | `Ran 52 tests in 72.708s` / **`FAILED (failures=3, errors=21)`** |
| `main` `2059c8105`（现在） | `Ran 52 tests in 35.976s` / **`OK`** |

它的提交信息把根因写对了，而且写得比我准：`REPO_ROOT` 在第 24 行定义，`ROOT = REPO_ROOT` 在第 170 行是一次**普通赋值而不是代理**，所以重绑一个名字另一个仍指向真实检出。两个名字已经漂成两种用途——文件存在性与配对逻辑读 `ROOT`，而**每一处** `subprocess.run(..., cwd=...)`、`BASELINE_PATH`、两个 import-time 检查读 `REPO_ROOT`。

§6 也一并修掉：`bilingual-docs.yml:27` 现在运行该套件，且放在真实闸门之前，理由写在提交信息里——「a fixture-only failure cannot be mistaken for a document problem」。这比我原本要派工单写的「加进 hygiene 的显式列表」更好：它挂在 `GOV-DOC-001 structural checks` 这个 required context 上，而不是挂在另一个 job 的时长里。

**所以 `AID-2026-055` 不需要登记了。** 032 §6 保留的那份内容（对象、依据、七条验收）现在指向一件已完成的工作。我不删除 032 的 §6——它记录了当时的判断，而判断当时是对的——但本文件声明它作废。

---

## 3. 我对「24 个问题」的推断是错的：套件能被杀

030 §4 说 24 个失败「不会在任何地方变红」。我据此推断这套测试对被它守护的控制是钝的，并在 032 §6 写了两个变异测试要求。**推断错了**：24 个问题来自 helper 读错仓库，而不是来自断言恒真。

在 `main 2059c8105` 上，对 `scripts/check_bilingual_docs.py` 做两次变异，各跑一次 52 个测试，再还原：

| 变异 | 结果 | 判定 |
|---|---|---|
| 基线（未变异） | `Ran 52 tests in 25.117s` / **`OK`** | — |
| 甲：删掉 `and not partial_side_by_side` | `Ran 52 tests in 21.868s` / **`FAILED (failures=1)`** | **KILLED** |
| 乙：把每处 `cwd=ROOT` 换回真实检出（重造半覆盖 bug） | `Ran 52 tests in 97.701s` / **`FAILED (failures=8, errors=11)`** | **KILLED** |
| 还原后 | `Ran 52 tests in 16.828s` / **`OK`** | — |

两条都有明确的数字，不是「跑了一下没问题」。

**这对 `AID-2026-054` 有直接后果。** `ERRATUM-01` 的判据 11 要求「删掉 `and not partial_side_by_side` 后至少一个测试失败，并贴出失败输出」。该判据在写的时候是**不可满足**的——`PARTIAL_SIDE_BY_SIDE_PAIRS` 当时没有能生效的测试。现在可满足，且安全边际是 1 个失败：`ERRATUM-01` 的 C 项（加判据 11）由此从「提出要求」变成「要求可被执行」，但 1 个失败也是**薄**的——任何进一步削弱该断言的改动仍可能把它抹掉。判据 11 应改为要求「至少 1 个失败且该失败断言的是 `PARTIAL_SIDE_BY_SIDE_PAIRS` 语义」，而不只是「有测试变红」。

---

## 4. GAP-24 少算了一对，而且只描述了一个方向

以 `git ls-tree` 枚举主干上所有 `docs/en/<P>` 与 `docs/zh-CN/<P>` 同时存在的 `<P>`，逐对比对 blob：

| 类别 | 判据 | 数量 |
|---|---|---|
| **IDENTICAL** | `en` 与 `zh-CN` 逐字节相同 | **2** |
| **ZH_EMPTY** | 不同，且 `zh-CN` 零个 CJK 字符 | **2** |
| **ZH_THIN** | 不同，`zh-CN` 有 1–99 个 CJK | **3** |
| **REAL** | 不同，`zh-CN` ≥100 个 CJK | **116** |
| 合计 | — | **123** |

只有 2 对逐字节相同，也就是 123 分之 2。这个比例说明问题不是普遍的，GAP-24 的框架应该按「个别文件」而不是「一类文件」来读。

**但这两对的方向相反，而 GAP-24 只写了其中一个方向：**

| 文件 | 字节 | CJK | 根文件是 | 镜像问题 |
|---|---|---|---|---|
| `GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023.md` | 12181 | **0** | 英文 | `docs/zh-CN/` 是英文副本 —— **GAP-24 描述的就是这一种** |
| `GOV-REV-2026-11-21-PR425-001.md` | 7390 | **1057** | **中文** | `docs/en/` 是**中文**副本 —— **反方向，GAP-24 没有这一种** |

`GOV-REV-...-PR425-001.md` 的三个位置（根、`docs/en`、`docs/zh-CN`）md5 完全相同，内容是一份中文技术审查记录。它的 `docs/zh-CN/` 是**真中文**；错的是 `docs/en/`——一个打开 `docs/en/` 期待英文的读者会拿到 1057 个 CJK 字符的中文。

后果是 GAP-24 §3 提的检查 (a)（`md5(zh-CN) == md5(source)` 即报错）**当检测器仍然对**——它会抓到 2 个文件——**但它的描述会把 425 这一对归错**：那一对的 `zh-CN` 没有问题，问题在 `docs/en/`。检查必须写成方向无关（「任一侧是另一侧的逐字节副本」），并且两对的补救不同：

- `023`：补一份真的中文，或把它从 `docs/zh-CN/` 撤下并登记豁免。
- `PR425-001`：根文件是中文，`docs/zh-CN/` 合法，`docs/en/` 才是缺英文的那一侧。

**GAP-24 的计数因此要更正为 2，不是 1；而「zh-CN 镜像是英文文件」这句话只对其中 1 对成立。**

---

## 5. 032 §1–§5 的前提被 `#893` 拆掉：准入通道已打开，不是关着

本节原标题是「032 §1–§5 不受影响，已重新验证」。**这个结论是错的**，错在两处：漏了一次提交，以及把我测量时刻为真当成了合并点仍为真。

### 5.1 我漏掉的第三次提交

我写「最近两次改动仍是 `cfcafc98a`（#844）与 `e798b1a72`」时测的是 `main 2059c8105`。在那个树上这句话**是准确的**，重跑确认：

```
$ git log --oneline 2059c8105 -- scripts/ci/check_repository_hygiene.py
cfcafc9 ci(hygiene): admit new files through an explicit whitelist (#844)
e798b1a ci(hygiene): gate prohibited generated artifacts in the committed tree (#778)
```

但 2059c8105 之后主干又动了一次，而这次正好落在本节断言的对象上：

```
$ git log --oneline 3026b31 -- scripts/ci/check_repository_hygiene.py
e894865 fix(hygiene): admit work-item manifests by anchored path shape, not by suffix   <- 我漏掉的第三次
cfcafc9 ci(hygiene): admit new files through an explicit whitelist (#844)
e798b1a ci(hygiene): gate prohibited generated artifacts in the committed tree (#778)
```

`e894865`（#893，2026-11-24 14:13:58 +0800）在 `is_allowed_new_path()` 里加了第六类规则。正则原文（**合并点上的形态**）：

```python
WORK_ITEM_MANIFEST_RE = re.compile(
    r"14-ai-development/work-items/AID-[A-Za-z0-9][A-Za-z0-9._-]*/manifest\.yaml"
)
```

在合并点 `main 3026b31` 上直接调用该函数：

```
is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')  -> True
is_allowed_new_path('14-ai-development/work-items/AID-anything/manifest.yaml')   -> True
is_allowed_new_path('14-ai-development/governance-register/X.md')                -> True
```

原文写的 `-> False` 在 `2059c8105` 上确实为真（重跑同样得到 False：那个树的模块里没有 `WORK_ITEM_MANIFEST_RE`），但**它不是合并点的事实**。

### 5.2 通道不只是开着，它已经被用过一次

`#896`（合并 `84bbe924`，2026-11-24 14:51:51 +0800）就是走这条通道登记的：

| 文件 | 改动 |
|---|---|
| `14-ai-development/work-items/AID-2026-055/manifest.yaml` | +188 |
| `14-ai-development/work-items/AID-2026-055/prompt-v1.md` | +145 |
| `14-ai-development/work-items/INDEX.md` | +2 / -1 |

PR head `5585d95` 的 11 项检查全部 success。用含 `#893` 的闸门直接复核这次登记：

```
$ python scripts/ci/check_repository_hygiene.py \
    --base e8948654f941c8192579cf8861f54cef0b4993e1 \
    --head 84bbe9241aef748b406a969da321e7d3fcda2dc1
Repository new-file admission version=2026-11-24.1 ...
Repository new-file admission passed: 2 new path(s) checked.
-> rc=0
```

所以原文两句都已被推翻：**通道关着**——假，`#893` 起开着；**现在没有工作单想被登记**——假，`AID-2026-055` 已经登记进去了，就在写那句话的同一小时内。

### 5.3 032 的哪一部分因此失效

- **032 §1 失效。** 它的结论是「自 `cfcafc98a` 起，任何新的 AID 工作单都无法登记」。这句在 `cfcafc98a`..`e894865` 之间为真，自 `e894865` 起为假。今天登记一个新工作单是可行的，`#896` 就是证据。
- **032 §3 的规则表失效。** 它列「五类之外一律拒绝」，现在有第六类 `WORK_ITEM_MANIFEST_RE`。
- **032 §4 的推理不受影响，但它的对象消失了。**「由需要者自行放宽，正是缺的那道检查」这个论证仍然成立——它只是不再有一个需要它的人：`#893` 由另一个会话按「锚定路径形态」实施，不是由 032 的作者破例。
- **032 §6 已在 §2 声明作废**，与本更正一致。

**因此「032 §1–§5 不受影响」这句话本身作废。** 不是「部分受影响」，是它的核心结论（通道关着）已经不成立。032 文件我不改——它记录了当时的判断，而判断在当时是对的；本文件声明它失效。

### 5.4 引用这个正则时要带上时间点

合并点的 `AID-[A-Za-z0-9][A-Za-z0-9._-]*` 很宽：`AID-anything` 也通过。更晚的主干把它收紧为 `AID-\d{4}-\d{3}`（`5822e52`），`AID-anything` 在最新 main 上不再通过。本节贴的是**合并点**上的形态，因为要证明的是合并点的事实；引用时请连同时间点一起引。

---

## 6. 本文件不主张什么

- 不主张 #892 需要回退。它修得比我要求的更好。
- 不主张 030 应当关闭。它的 §4/§6 已被修掉，§1–§3、§5、§7 的状态我不重测，`register_closure` 也不在本次授权内。
- 不主张 GAP-24 的白名单不需要管。我只更正它的计数与方向；它的 `docs/zh-CN/` 方向对 `023` 完全成立。
- 不主张 2 个逐字节相同就是全部。我只测了 `docs/en` 与 `docs/zh-CN` 同时存在的 123 对；并排配对（`X.en.md` / `X.zh-CN.md`）与只有单侧镜像的文件不在本次枚举内。
- 不指派独立审查。席位 `NOT_ASSIGNED`，本文件不能填。

**阻断链：** 独立审查 `NOT_ASSIGNED`，实施授权 `NOT_AUTHORISED`，sponsor / accountable owner `NOT_ASSIGNED`。

---

## 7. 复现

```
repo:  oahcom/AiMemoryBrainArchitecture
main:  2059c8105

# 1. 套件现在全绿
git worktree add --detach <tmp> origin/main
cd <tmp> && python -m unittest scripts.governance.evidence.test_gate_normative_roots
-> Ran 52 tests / OK

# 2. 它能被打红
#    把 `and not partial_side_by_side` 从 current_bilingual_gaps() 删掉，重跑
-> FAILED (failures=1)
#    把每处 `cwd=ROOT` 换成 pathlib.Path(__file__).resolve().parents[1]，重跑
-> FAILED (failures=8, errors=11)

# 3. 它现在被 CI 运行
grep -n 'test_gate_normative_roots' .github/workflows/bilingual-docs.yml
-> 27:        run: python3 -m unittest scripts.governance.evidence.test_gate_normative_roots

# 4. 镜像审计
#    枚举 docs/en/P 且 docs/zh-CN/P 同时存在的 P，比对 git show 的 blob
-> 123 pairs; IDENTICAL 2, ZH_EMPTY 2, ZH_THIN 3, REAL 116
#    两对逐字节相同的 CJK 计数分别是 0 与 1057

# 5. 准入已放行工作单（2026-11-24 15:52 +0800 于 main 3026b31 重测，见 §5）
python -c "import sys; sys.path.insert(0,'scripts/ci'); import check_repository_hygiene as h\
; print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml'))"
-> True
#    同一命令在 main 2059c8105 上为 False —— 差异来自 #893 的 WORK_ITEM_MANIFEST_RE
python scripts/ci/check_repository_hygiene.py --base e8948654f941c8192579cf8861f54cef0b4993e1 \
    --head 84bbe9241aef748b406a969da321e7d3fcda2dc1
-> Repository new-file admission passed: 2 new path(s) checked.  rc=0
```

---

## 8. 闸门不读内容——这次是跑出来的，不是读出来的

§4 对「只查存在性」的判断是**读源码**得出的。本节把它跑起来。方法：在 `origin/main` 的独立 worktree 上，每个用例 `git reset --hard origin/main` 后只提交一次，用真实的 `BASE_SHA` / `HEAD_SHA` 调用 `scripts/check_bilingual_docs.py`，记录退出码与全部 `::error::` 行。

### 8.1 八个用例

| # | 变异 | 改动文件数 | 退出码 | 拦截者 |
|---|---|---|---|---|
| 对照 | 不做任何改动 | 0 | **2** | `NOT_APPLICABLE`（零改动路径） |
| A | 删除某个 REAL 配对的 `docs/zh-CN/` | 1 | **1** | `changed without paired change` |
| B | 把 `docs/zh-CN/` 覆盖为英文原文 | 1 | **1** | `changed without paired change` |
| C | 删除 `023` 的 `docs/zh-CN/`（根 CJK 0） | 1 | **2** | `New bilingual gap outside frozen baseline` |
| D | 删除 `PR425-001` 的 `docs/zh-CN/`（根 CJK 1057） | 1 | **1** | `changed without paired change` |
| **F** | 改根 + `docs/en/` + `docs/zh-CN/`，且 `zh-CN` 变成英文逐字节副本 | 3 | **0** | **无** |
| **G** | 同上，但把 `zh-CN` 里每一个 CJK 字符替换成 `X` | 3 | **0** | **无** |
| H | 改根**并且**删除 `PR425-001` 的 `docs/zh-CN/` | 2 | **1** | `requires all counterparts changed` |
| I | 改根**并且**删除 `023` 的 `docs/zh-CN/` | 2 | **2** | `New bilingual gap outside frozen baseline` |

### 8.2 F 与 G 是结论

F 和 G 把一份真中文镜像改成完全不含中文（G 连一个 CJK 字符都不剩），**闸门以 0 退出**。这不是「漏检一个边界情况」，而是：**没有任何一行代码读 `docs/zh-CN/` 的内容**。§4 说的「存在性即合格」在这里有了可执行的证据，而不是源码推断。

注意 F/G 与 B 的区别。B 被抓到，不是因为内容变了，而是因为**只有一侧变了**。把 B 改成 F（两侧都改），同样的内容破坏就不再被拦。所以拦住 B 的是配对规则，不是内容判断。这个区分很重要：它意味着「镜像被换成英文」这件事，只要同一次提交里也碰一下根文件，就完全隐形。

### 8.3 「删掉中文镜像反而无告警」是错的

§4 之后的并行测量给出过一个推论：`023`（根 CJK 0）删掉 `zh-CN` 会报 gap，而 `PR425-001`（根 CJK 1057）删掉 `zh-CN` 不报——「删中文镜像反而无告警」。**实测否定它**：D 和 H 都以非零退出码失败。

那个推论只评估了 **gap 谓词**，而闸门有**两套**独立机制：gap 谓词，和「改动路径必须有配对改动」。`PR425-001` 的删除被后者拦住。把两套机制中的一个当作全部，就会得出「无告警」这种结论——这类错误在本会话里已经出现过两次（`EXIT` 取错管道、`PARTIAL_SIDE_BY_SIDE_PAIRS` 只按谓词推断可达性）。所以本节的做法是：**每个结论对应一次真实调用，退出码写在表里。**

### 8.4 两个互不相交的总体

`scripts/bilingual-baseline.txt` 共 80 行：3 行注释 + **77 条**冻结条目，与闸门打印的 `77 frozen` 一致，也解释了 033 §4 里 77 与 80 两个数字的关系。

关键点：**77 条基线里没有一条是那 7 个内容缺陷。**

| 总体 | 判据 | 数量 | 与对方的重叠 |
|---|---|---|---|
| 基线（冻结） | 某一侧**不存在** | 77 | — |
| 内容缺陷 | 两侧**都存在**，但 `zh-CN` 不是翻译 | 7 | **0** |

两者在定义上不可能相交：基线登记的是「缺一侧」，缺陷是「两侧都在、内容不对」。因此 `AID-2026-054` 把基线从 77 压到 11 的努力，**对那 7 个文件不起任何作用**——它清理的是另一个总体。这不是 054 的错误，054 的目标本来就不是内容；但它说明「基线清空」不等于「双语合格」，而目前的任何指标都不会同时看这两件事。

### 8.5 绝对计数有时效，本次是 124 不是 123

033 §4 写的是 123 对。本节重测为 **124 对**，因为两次测量之间主干合入了新的双语文件（本文件自己就是一对）。在 124 对里：`en` 侧 `>=100` CJK 的仍是 **1** 个（`PR425-001`），`en` 侧 `1..99` CJK 的 **56** 个，**两侧都零 CJK** 的 **3** 个（`018`、`023`、`019`）。

那 56 个不是缺陷：英文文档里出现少量中文术语/引用是正常的。列出来是为了说明「`en` 侧有中文」这个信号本身不能当判据，只有 `>=100` 才有意义——与 `_carries_chinese()` 的阈值一致。

**所以本文件不主张任何一对一的绝对数字是长期有效的。** 每个数字都对应 `main` 上的一次枚举，枚举命令在 §7；复核时重跑，不要引用本文件的行号。

### 8.6 本节的结论

1. 闸门从不读 `docs/zh-CN/` 内容。F、G 证明。
2. 删除镜像**会**被拦，靠的是配对规则，不是内容规则。D、H、I 证明。
3. 内容破坏只要与根文件改动同时发生，就**不被拦**。F、G 证明。
4. 77 条基线与 7 个内容缺陷是两个不相交总体，压基线不能修内容。
5. 因此 GAP-24 §3 提的检查 (a) 若实施，补的正是第 3 条这个洞；它不替代基线，也不被基线替代。

