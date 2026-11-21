# GOV-NC-2026-11-21-GATE-CLOSURE-020

**登记编号**：GOV-NC-2026-11-21-GATE-CLOSURE-020
**性质**：MEASUREMENT_ONLY / NO_IMPLEMENTATION / REQUIRES_INDEPENDENT_REVIEW
**测量点**：`main = 1a5342421a`（`grep -vc '^#' scripts/bilingual-baseline.txt` = 77）
**登记时间**：2026-11-21
**作者**：协调会话（非独立审查者）

---

## 0. 本登记要解决的问题

登记 011 至 019 在 `0cce40a` → `d647e7d` 期间记录了八处门禁缺陷。main 已推进到 `1a53424`，期间合入多个门禁修复 PR。本登记逐条核对：**哪些已被关闭、用什么方式关闭、哪些仍开着**。

这不是「缺陷已修复」的宣告。关闭与否由实测决定，且我作为记录者不是独立审查者。

---

## 0.1 本登记推翻的我自己的一条结论

登记 017 声称 `.json` schema 被要求双语镜像，机制是 `PAIR_ENFORCED_SUFFIXES` 只在 14 分支内生效。**缺陷真实存在，但根因我写错了一半。**

实际修复来自 #527（`717dfbf`），它改的不是 `PAIR_ENFORCED_SUFFIXES`，而是 `main()` 里构造 `normative_changes` 的过滤条件：

```python
# before (line 996 in d647e7d)
if Path(path).suffix.lower() in {".md", ".yaml", ".yml", ".json", ".toml", ".proto"}:
    normative_changes.append(path)

# after (line 1064 in 1a53424)
if Path(path).suffix.lower() == ".md":
    normative_changes.append(path)
```

也就是说：`.json` 现在**根本不进入配对检查**，而不是「进入后被后缀过滤器放过」。第 937 行的 `PAIR_ENFORCED_SUFFIXES` 仍在 14 分支内，但它已经不是 `.json` 逃生的地方。

两者的区别有实际后果：我的建议（把后缀过滤移到分支外）会让 `.json` 进入配对检查再被放过，仍然保留「哪些后缀算文档」的两处定义；实际采用的修复只有一处定义，更难写错。**实际修复比我的建议好。**

---

## 1. 逐条核对表

| 登记 | 缺陷 | `1a53424` 状态 | 关闭方式 |
|---|---|---|---|
| 011 | 非 14 根的并排配对在 diff 判定域被拒 | **CLOSED** | #485 `5f10930` 在 `check_normative_pairing()` 中加入 `side_by_side_partner(source)` 分支 |
| 013 | 同上（残量测量） | **CLOSED** | 同 011 |
| 014 | `ROOT = Path.cwd()` 与 `REPO_ROOT` 分裂 | **OPEN** | 未修。见 §2.1 |
| 015 | `13-engineering-decisions` 58 条冻结缺口 | **OPEN** | 未修。基线仍 77，58 条仍在 |
| 016 | M5/M6 变异体存活 | **OPEN** | 见 §3 |
| 017 | `.json` 被要求双语镜像 | **CLOSED** | #527 `717dfbf` 把 `normative_changes` 收窄为仅 `.md` |
| 019 | `PARTIAL_SIDE_BY_SIDE_PAIRS` 不进 diff 域 | **OPEN** | 未修。见 §2.2 |
| 020 | 零字节 / 三文件 / 单 CJK 三条漏洞 | **OPEN** | 见 §2.3 |

**2 关闭 / 6 未关闭。** 关闭的两条都是门禁形态问题；未关闭的六条中，三条是政策问题（014/015/019），三条是判据强度问题（020）。

---

## 2. 未关闭项的精确状态

### 2.1 014 — `ROOT` / `REPO_ROOT` 分裂仍然存在

```python
REPO_ROOT = Path(__file__).resolve().parents[1]   # line 23
ROOT      = Path.cwd()                            # line 157
```

在 `1a53424` 上实测：`str(REPO_ROOT) == str(ROOT)` 在仓库根运行时为 `True`，从外部目录运行时为 `False`。`--write-baseline` 从外部目录运行仍会把 77 条写成 117 条。

CI 不受影响（workflow 的 cwd 是 checkout 根）。这是本地测量与基线再生成的隐患，不是 CI 运行时缺陷。

### 2.2 019 — `PARTIAL_SIDE_BY_SIDE_PAIRS` 仍是空集且仍不进 diff 域

```python
# line 44
PARTIAL_SIDE_BY_SIDE_PAIRS: set[frozenset[str]] = set()

# line 350 — inside current_bilingual_gaps()
and frozenset((source, side_by_side)) in PARTIAL_SIDE_BY_SIDE_PAIRS
```

`check_normative_pairing()`（line 919-963）内引用数：**0**。

而且 77 条基线中 **0 条**与另一条构成并排配对，所以该寄存器对既有缺口也无效。它的实际作用范围是「新配对的缺口扫描」，比名字暗示的窄得多。

### 2.3 020 — 三条判据强度漏洞，全部通过真实 CLI 可达

三条都用真实 CI 入口验证：文件写入 → `git add` → `git commit` → `BASE_SHA=HEAD~1 HEAD_SHA=HEAD PR_BODY='BILINGUAL-MANIFEST: COMPLETE' python scripts/check_bilingual_docs.py`。前置条件 `REPO_ROOT == ROOT` 已断言为 `True`。

| 漏洞 | 构造 | CLI 结果 | 应当 |
|---|---|---|---|
| **H1 零字节** | `zb.md`（中文）+ `zb.zh-CN.md`（**0 字节**） | **`EXIT=0`** | 拒绝 |
| **H2 三文件** | `am.md`（中）+ `am.en.md`（英）+ `am.zh-CN.md`（中） | **`EXIT=0`** | 拒绝（歧义） |
| **H3 单 CJK** | 两侧均英文，各含一个 `一` | **`EXIT=0`** | 拒绝 |

**H1 细节**：`zb.zh-CN.md` 的 `_has_any_chinese` 为 `False`，但 `_side_by_side_bilingual` 返回 `True` —— 因为判据是「源或配对**任一侧**含 CJK」，源侧含中文就够了。0 字节配对文件从不被读取。

**H2 细节**：配对链**不对称**，这是比「三文件被接受」更严重的事实：

```
am.md        -> am.en.md      -> am.zh-CN.md     ASYMMETRIC
am.en.md     -> am.zh-CN.md   -> am.en.md        SYMMETRIC
am.zh-CN.md  -> am.en.md      -> am.en.md        SYMMETRIC
```

`am.md` 指向 `am.en.md`，但 `am.en.md` 指回 `am.zh-CN.md`。`partner(partner(am.md)) != am.md`。因此 `am.md` 的中文正文**永远不会被任何一方要求同步** —— 它看起来被配对，实际上被排除在配对之外。这是「先匹配即返回」的直接后果。

**H3 细节**：`_has_any_chinese` 的判据是「任意一个 CJK 字符」。一个 `一` 字即可。两个英文文件各加一个 `一` 就构成「双语配对」。

### 2.4 存量利用情况：可利用但未被利用

```
0-byte .zh-CN.md files : 0
total .zh-CN.md files  : 72
```

**72 个 `.zh-CN.md` 全部非空。** 三条漏洞都是**潜在**的，不是**已发生**的。这个区分必须保留：说「门禁有漏洞」和说「仓库里有假翻译」是两件不同的事，后者不成立。

---

## 3. 变异体状态：M5 与 M6 仍存活

在 `1a53424` 上重跑四个变异体（测试文件当前 47 个测试）：

| 变异 | 结果 |
|---|---|
| **M4** 移除 `and not partial_side_by_side` | **KILLED**（1 失败） |
| **M5** 移除 Shape 3 的 `root_name == "14-ai-development"` 守卫 | **SURVIVED**（47 全过） |
| **M6** `ROOT = Path.cwd()` → `ROOT = REPO_ROOT` | **SURVIVED**（47 全过） |
| **M7** `_has_any_chinese` → `return True` | **KILLED**（1 失败） |

**M5 存活意味着**：产生 77 条基线中 58 条（登记 015）的那个根名守卫，没有任何测试覆盖。任何人都可以把它删掉，测试全绿。

**M6 存活意味着**：登记 014 的缺陷和它的修复对测试套件**都不可见**，因为每个测试都在仓库根运行。这也解释了为什么 014 能长期存在。

---

## 4. 当前 PR 矩阵

`main = 1a5342421a`，10 个开放 PR，每个 PR 以其精确 head overlay 到 main 后跑门禁：

| PR | head | 文件 | 原始 body | + manifest | 判定 |
|---|---|---|---|---|---|
| #530 | `f1fd4219` | 1 | `EXIT=0` | `EXIT=0` | PASS |
| #529 | `85257d5d` | 3 | `EXIT=0` | `EXIT=0` | PASS |
| #523 | `6bb94365` | 3 | `EXIT=0` | `EXIT=0` | PASS |
| #518 | `2651e226` | 1 | `EXIT=0` | `EXIT=0` | PASS |
| #513 | `d7992210` | 2 | `EXIT=0` | `EXIT=0` | PASS |
| #512 | `e265f7d5` | 2 | `EXIT=0` | `EXIT=0` | PASS |
| #496 | `4d1ce5ab` | 9 | `EXIT=0` | `EXIT=0` | PASS |
| #494 | `c1beeb1d` | 30 | `EXIT=0` | `EXIT=0` | PASS |
| #471 | `d33ee2bb` | 8 | `EXIT=1` (1) | **`EXIT=0`** | MANIFEST-ONLY |
| #433 | `81558c89` | 3 | `EXIT=0` | `EXIT=0` | PASS |

**9 通过 / 1 仅缺 manifest。** 与登记 017 时的「5 通过 / 4 失败」相比，门禁形态问题已基本清空。剩下的失败里没有一个属于 011 或 017 的类别。

---

## 5. 本登记不主张什么

- **不主张门禁可信**。M5、M6 存活，47 个测试覆盖不到产生 75% 基线的那条规则。
- **不主张三条漏洞必须立即修**。修复需要判断：0 字节判据会不会误伤 77 条基线？`_has_any_chinese` 提高到阈值会不会让真实短文档变成新缺口？我没有测这两点，所以不提议改法。
- **不主张 011/017 的关闭经过独立审查**。#485 与 #527 的审查轨迹我未核对。关闭是实测事实，不是审查结论。
- **不主张 CI 执行过**。全部 348 个 check 的 `steps=[]`（登记 005）状态未变，本轮所有验证均为本地补偿证据。
- **不主张测试通过等于覆盖充分**。47 个测试全过与 M5/M6 存活同时成立，正是「通过 ≠ 有效」的实例。

---

## 6. 复现命令

```bash
git clone https://github.com/oahcom/AiMemoryBrainArchitecture.git && cd AiMemoryBrainArchitecture
git rev-parse --short HEAD                      # 1a53424
grep -vc '^#' scripts/bilingual-baseline.txt    # 77

# H1 zero-byte
printf '# 标题\n\n%s\n' "$(python3 -c "print('中文内容测试。'*30)")" > 02-domain-model/zb.md
: > 02-domain-model/zb.zh-CN.md
git add -A && git -c user.email=t@t -c user.name=t commit -qm p
BASE_SHA=$(git rev-parse HEAD~1) HEAD_SHA=$(git rev-parse HEAD) \
  PR_BODY='BILINGUAL-MANIFEST: COMPLETE' python3 scripts/check_bilingual_docs.py; echo "EXIT=$?"
# -> EXIT=0

# H2 asymmetry
python3 -c "
import sys,os; sys.path.insert(0,'scripts'); sys.argv=['x']
import check_bilingual_docs as g
for f in ('02-domain-model/am.md','02-domain-model/am.en.md','02-domain-model/am.zh-CN.md'):
    p=g.side_by_side_partner(f); q=g.side_by_side_partner(p) if p else None
    print(f,'->',p,'->',q,'SYMMETRIC' if q==f else 'ASYMMETRIC')"

# M5 / M6 survival
python3 -m unittest discover -s scripts/governance/evidence -p "test_gate*.py"   # 47 OK
# then edit the guard, rerun -> still 47 OK
```

---

## 7. 留给独立审查者的三个问题

1. **M5 为什么没有测试？** 产生 58/77 基线条目的 `root_name == "14-ai-development"` 守卫，是政策决定还是历史遗留？如果是政策，应当有测试固定它；如果是遗留，应当移除并重新生成基线。
2. **H1 的最小修复会不会误伤基线？** 「配对文件必须非空」这一条，对 77 条冻结缺口中的并排配对是否产生新的 `resolved`（棘轮另一方向会报错）？我没有测。
3. **H2 的歧义应当拒绝还是应当定义优先级？** 拒绝会让三文件形态不可用；定义优先级需要说明为什么 `.md` 优先于 `.en.md`。这是政策问题，不是实现问题。

---

**本文件是测量记录，不是审查结论，不授权任何实施。**
