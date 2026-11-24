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
      last_verification_note: "§1-§4 and §6-§7 measured at main 2059c8105; §8 re-measured at main 84bbe9241; §5 re-measured at main 1259f1a on 2026-11-24 18:32:42. Every §8 row is one real invocation of scripts/check_bilingual_docs.py on a worktree reset to origin/main before the single commit under test, with the exit code recorded. Cases F and G exit 0, which is the evidence that no code reads docs/zh-CN content. Cases D, H, I exit non-zero, which refutes the inference that deleting a Chinese mirror goes unannounced. The baseline is 80 lines = 3 comments + 77 entries; none of the 7 content defects appears among those 77 entries. The pair count moved 123 -> 124 between the two measurement points because main gained files. §5 was re-measured because its original two assertions were taken at 2059c8105, ten minutes before #893 added WORK_ITEM_MANIFEST_RE; AID-2026-055 (#896, 84bbe9241) and AID-2026-056 (#908, 5d83b3c) have since been registered through that rule."
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
    source: null
    en: "docs/en/14-ai-development/governance-register/GOV-REV-2026-11-24-FOUR-CORRECTIONS-033.md"
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-24-FOUR-CORRECTIONS-033.md"
---

# GOV-REV-2026-11-24-FOUR-CORRECTIONS-033

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION` / §8 added 2026-11-24
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 2059c8105` (§4), `main = 84bbe9241` (§8), `main = 1259f1a` (§5, re-measured 2026-11-24 18:32:42 after #893 opened the admission channel)
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

032 §1–§5（发派通道关闭）**不受影响这句话不再成立**：`#893` 在 2026-11-24 14:13:58 打开了通道，`AID-2026-055` 至 `AID-2026-058` 已经用上了。逐节重判见 §5.3。

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

## 5. 032 §1–§5 的前提已失效：准入通道由 #893 打开，且已被两件工作单使用

**本节原文在它自己合并的当天就已过期。** 不是事后追认，是时间线：

| 事件 | 提交 | 时刻（+0800） |
|---|---|---|
| 本节两条断言被测量 | `main = 2059c8105` | 2026-11-24 14:03:58 |
| `#893` 给准入加第六条规则 | `e8948654f` | 2026-11-24 14:13:58 |
| `AID-2026-055` 经该通道登记并合入（`#896`） | `84bbe9241` | 2026-11-24 14:51:52 |
| 本文件合并（`#897`） | `3026b319b` | 2026-11-24 15:12:35 |

测量与失效相隔十分钟，失效与合并相隔一小时。**本节写作时是对的**——在 `2059c8105` 上重跑，两条断言逐字复现（见 5.1 左列）。错的是它把一个绝对测量值当成了当前事实，而主干在测量与合并之间又前进了一支。这正是本文件 §8.5 自己写下的教训（「绝对计数有时效……复核时重跑，不要引用本文件的行号」），只是这次犯在正文里，不在附录里。

### 5.1 三处断言，逐条重测

`scripts/ci/check_repository_hygiene.py:79-81` 现在是：

```python
WORK_ITEM_MANIFEST_RE = re.compile(
    r"14-ai-development/work-items/AID-\d{4}-\d{3}/manifest\.yaml"
)
```

`:197` 的 `if WORK_ITEM_MANIFEST_RE.fullmatch(path): return True` 由 `#893` 加入，位置在 `.github/actions/` 规则之后、末尾 `return False` 之前。`#915`（`a7c5cd2`）随后把 ID 段从 `[A-Za-z0-9][A-Za-z0-9._-]*` 收紧为 `\d{4}-\d{3}`，理由是 `AID-<anything>` 会放行登记表无法分配的拼写。

**改前与改后，同一条命令，两个测量点：**

| # | 位置 | 改前：`main = 2059c8105`（2026-11-24 14:03:58） | 改后：`main = 1259f1a`（2026-11-24 18:32:42） |
|---|---|---|---|
| 1 | 本节代码块第 1 行 | `is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')` → **`False`** | → **`True`** |
| 2 | 本节代码块第 2 行 | `is_allowed_new_path('14-ai-development/governance-register/X.md')` → **`True`** | → **`True`**（值未变，含义变了：不再是「只有 `.md` 能过」，而是 `.md` 与 work-item manifest 都能过） |
| 3 | 本节结论句 | 「新的工作单无法登记」仍然成立；「现在没有工作单想被登记」 | **两句都不成立**：`AID-2026-055` 至 `AID-2026-058` 都已登记 |

复现命令（两次都是导入真实脚本、调用真实函数，不是读代码）：

```
# 改前：把 2059c8105 的脚本取出，单独导入
$ git show 2059c8105:scripts/ci/check_repository_hygiene.py > /tmp/hyg2059t/check_repository_hygiene.py
$ cd /tmp/hyg2059t && python3 -c "import check_repository_hygiene as h; \
    print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')); \
    print(h.is_allowed_new_path('14-ai-development/governance-register/X.md'))"
False
True

# 改后：在 1259f1a 的检出上直接导入
$ python3 -c "import sys; sys.path.insert(0,'scripts/ci'); import check_repository_hygiene as h; \
    print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml')); \
    print(h.is_allowed_new_path('14-ai-development/governance-register/X.md'))"
True
True

# 正则本身
$ python3 -c "import re; R=re.compile(r'14-ai-development/work-items/AID-\d{4}-\d{3}/manifest\.yaml'); \
    print(bool(R.fullmatch('14-ai-development/work-items/AID-2026-099/manifest.yaml')))"
True
```

### 5.2 通道不只是开着，已经被用过四次

| 工作项 | 登记提交 | 时刻（+0800） | 证据 |
|---|---|---|---|
| `AID-2026-055` | `#896`，merge `84bbe9241`（head `5585d95`） | 2026-11-24 14:51:52 | 新增 `14-ai-development/work-items/AID-2026-055/manifest.yaml` + `prompt-v1.md`，并改 `INDEX.md` |
| `AID-2026-056` | `5d83b3c`（`#908`） | 2026-11-24 17:03:50 | 新增 `14-ai-development/work-items/AID-2026-056/manifest.yaml` |
| `AID-2026-057` | `b3a65e5` | 2026-11-24 18:38:00 | 新增 `AID-2026-057/manifest.yaml` + `prompt-v1.md` |
| `AID-2026-058` | `01a3014` | 2026-11-24 19:39:28 | 新增 `AID-2026-058/manifest.yaml` + `prompt-v1.md` |

**前两行是 `main = 1259f1a` 上的快照，后两行是 `main = 01a3014` 上的。** `057` 与 `058` 在本节写完之后才合入——本节第一稿测到两件，再读时已是四件。这不是抓到了新缺陷，而是本节所论证的那件事在论证过程中又发生了一次：所以这里给的是四个带时刻的行，不是「共四件」这样一个会立刻过期的数。

`AID-2026-055` 的 `manifest.yaml` 首行是 `work_item_id: AID-2026-055`，`AID-2026-056` 是 `work_item_id: AID-2026-056`；两者都带完整的 `class` / `risk` / `risk_rationale` / `status: DISPATCHED` / `base_commit_sha`，不是占位目录：

```
$ git ls-tree --name-only origin/main 14-ai-development/work-items/ | grep -E 'AID-2026-05[5-8]'
14-ai-development/work-items/AID-2026-055
14-ai-development/work-items/AID-2026-056
14-ai-development/work-items/AID-2026-057
14-ai-development/work-items/AID-2026-058
$ git show origin/main:14-ai-development/work-items/AID-2026-055/manifest.yaml | head -1
work_item_id: AID-2026-055
$ git show origin/main:14-ai-development/work-items/AID-2026-056/manifest.yaml | head -1
work_item_id: AID-2026-056
```

**一个连带事实：** 本文件 §8 的测量点是 `main = 84bbe9241`——那正是 `AID-2026-055` 的登记合并提交。也就是说 §8 是在一棵**已经含有经该通道登记的工作单**的树上测的，而同一份文件的 §5 断言该通道拒绝工作单。两份结论同处一文，一份测于 `2059c8105`，一份测于 `84bbe9241`，中间隔了 48 分钟和一支提交。

### 5.3 032 §1–§5 因此逐节重判

032 讲的是**发派通道**，本文件讲的是四条更正；两者只有 §5 这一处相交，所以重判按节给，不给一个笼统的「不受影响」：

| 032 节 | 它说什么 | 现在 |
|---|---|---|
| §1 | 「自 `cfcafc98a` 起，任何新的 AID 工作单都无法登记」 | **不成立。** `#893` 加了 `WORK_ITEM_MANIFEST_RE` 这一条规则；`AID-2026-055`（#896）、`AID-2026-056`（#908）、`AID-2026-057`、`AID-2026-058` 已实际登记。 |
| §2 | 时间线：054 manifest `a3c6280aa`（11-23）/ 白名单 `cfcafc98a`（11-24）/ 尝试登记 055 | **事实成立**，三个日期与提交都没变。但它的作用是为 §1 做证，而 §1 的结论已反，所以这张表现在证明的是「白名单比 054 晚一天」这一件事，不再证明「通道关闭」。 |
| §3 | 白名单「五类」，「`manifest.yaml` 不在任何一类」 | **表格不再完整**：现在有第六条规则。前五类的描述仍逐条准确，`ALLOWED_DOCUMENT_SUFFIXES` / `ALLOWED_SOURCE_SUFFIXES` / `ALLOWED_CONFIG_PATHS` 都没被 `#893` 改动（`#893` 的 PR 说明明确写「No global `.yaml` suffix」）。 |
| §4 | 为什么本会话不自行放宽那一行 | **作为决策记录成立**：当时确实拒绝以需要者身份改闸门源码，理由（唯一想要门开的主体正是唯一有动机开得过宽的主体）与结论无关地仍然有效。其中「需要的改动是一行」现在由 `#893` 完成，`#915` 再收紧；「等放宽落地后一分钟内即可登记」的等待已结束。 |
| §5 | 「交叉处没人测过：白名单引入时没有同时测『现有工作单形态能否再次被创建』」 | **陈述成立**——`#844` 引入白名单时确实没有测这件事，`AID-2026-055` 在 `#887` 被 CI 拒绝就是漏测的证据。**但「这是当前存在的缺陷」不成立**，`#893` 已修。 |

**所以本文件撤回 §1 末尾那句「032 §1–§5 不受影响」**：§1 的结论已被事实推翻，§3 的枚举已不完整，§2/§4/§5 的部分陈述仍成立但已不支撑原结论。

本文件不修改 032 的正文，也不给它填 `register_closure`——那不在本次授权内（与 §6 一致）。032 需要它自己的一条勘误，本文件只负责把它的前提失效记录在案，并指向 `#893`、`#896`、`#908` 三个可复核的提交。

**这不是 hindsight 指责。** 本节写作时两条断言在 `2059c8105` 上都是真的，`#892` 确实没碰白名单。问题是它把「此刻为真」写成了「仍然成立」，而没有把测量点写进句子本身——`Measured at: main = 2059c8105` 挂在页首，读者要自己把它和「仍然」对齐。一份每条结论都带实测的文档，最该防的就是这种「实测正确、时态错误」。

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

# 5. 准入现在放行工作单（本节改于 2026-11-24，原写于 main = 2059c8105 时为 False）
python -c "import sys; sys.path.insert(0,'scripts/ci'); import check_repository_hygiene as h; \
  print(h.is_allowed_new_path('14-ai-development/work-items/AID-2026-099/manifest.yaml'))"
-> True
# 同一条命令在 2059c8105 上 -> False（#893 于 14:13:58 加入第六条规则）
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

