# GOV-NC-2026-11-21-GATE-DEADLOCK-006 — 门禁在 main 上自我死锁：任何 PR 都无法通过

- 登记编号：GOV-NC-2026-11-21-GATE-DEADLOCK-006
- 状态：`OPEN` / `ACTIVE` / 阻断全部 PR
- 发现时间：2026-11-21T05:05Z（last verified 2026-11-21T05:40Z @ `7d2233a5be`）
- 引入提交：`ae37a41900f1`（2026-11-21T04:50:35Z，**直推 main，无 PR**）
- 前置登记：GOV-NC-2026-11-20-CI-NOT-EXECUTED-005（门禁连续 36 小时零执行）
- 关联：#401（棘轮/基线，PR #408）、#407（存量清单口径）、#414（配对移动误判修正）

## 1. 结论先行

`main` 上，双语门禁 `scripts/check_bilingual_docs.py` **对任何输入都退出 2**，包括空 diff。自 `ae37a41900f1` 起，跨 7 个后续提交、至最新 `7d2233a5be`，判定不变。

```
$ git reset --hard ae37a41900f1     # 干净 main
$ BASE_SHA=$HEAD_SHA=$(git rev-parse HEAD) PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
    python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 00-governance/templates/document-metadata-template.md
EXIT=2
```

这不是「某个 PR 写得不对」，是**门禁本身在主干上处于不可满足状态**。空 diff 都过不了，所以任何未补双侧镜像的 PR 同样过不了——判定的分界是「有没有补 `docs/en` + `docs/zh-CN` 镜像」，不是「改了哪个文件」，见 §2.1 的六组隔离。

**复验（2026-11-21T05:40Z）**：`main` 已从 `ae37a41900f1` 前进 7 个提交到 `7d2233a5be`。在**最新头顶**的干净树上重跑同一命令，仍是 `EXIT=2`：

```
$ SHA=<7d2233a5be 干净树>
$ BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
::error::New bilingual gap outside frozen baseline: 00-governance/templates/document-metadata-template.md
EXIT=2
$ # 同一棵树，只删该模板
$ bilingual baseline: 207 frozen, 0 new gaps / exemptions: 20
$ Bilingual documentation and prompt-library gate: PASS (0 changed paths inspected).
EXIT=0
```

即死锁**未自我修复，且跨 7 个后续提交持续存在**。

一处更正：本登记初稿曾写「`9b6f73385e` 使基线 207 → 208」。实测该提交只改了三个文件（`architecture-document-management-policy.md`、`scripts/check_document_management.py`、`scripts/test_check_document_management.py`），**未触及 `scripts/bilingual-baseline.txt`**。基线自 `180d9ba0ebfc` 引入起一直是 **207** 条非注释行，全程未变。因此死锁的成因不随基线增长而缓解或加重，它只由那一个未配对文件决定。

由于 CI 自 2026-11-19T16:12:11Z 起零执行（见 005），这个死锁目前**没有任何自动通道能暴露它**——它只在有人手工在 exact Head 上跑脚本时才可见。

## 2. 三行定位

| 事实 | 值 |
|---|---|
| 新文件 | `00-governance/templates/document-metadata-template.md`（101 行，由 `ae37a419` 新增） |
| 基线 | `scripts/bilingual-baseline.txt`，207 条冻结项（由 `180d9ba0ebfc` 于 2026-11-21T03:55:54Z 引入） |
| 规则 | 基线只许收缩；出现基线外新缺口 → `::error::` + `EXIT=2` |

新文件落在 `00-governance/`（`NORMATIVE_ROOTS` 之内），是 `.md`，既不在 `EMBEDDED_BILINGUAL_SOURCES`，也不在 `PAIR_EXEMPT_PREFIXES`，且没有 `docs/en` / `docs/zh-CN` 镜像 → 它是一个**基线外的新缺口** → 门禁按设计拒绝。

**两件事各自都对，合起来死锁。** 基线机制（#401/#408）与「新增规范文档必须配对」各自都是合理规则；`ae37a419` 在同一棵树里既引入基线、又新增了一个未配对的规范文档，于是它自己的产物无法通过它自己的检查。

### 2.1 边界更正：不是「任何 PR 都无法通过」

本登记初稿写「任何基于当前 `main` 的 PR 都会得到同一个 `EXIT=2`」。实测这句话**过宽**，须收窄。

在 `14-ai-development/governance-register/` 上做的六组隔离（同一棵干净 `main` 树）：

| 组 | 做法 | gaps | baseline | NEW | EXIT |
|---|---|---|---|---|---|
| A | 三个登记对，各给真 `docs/en` + `docs/zh-CN` 镜像 | 207 | 207 | **0** | **0** |
| B | 三个登记对，写入 `EMBEDDED_BILINGUAL_SOURCES` | 207 | 207 | **0** | **0** |
| C | 三个登记对，追加进基线 | 213 | 213 | **0** | **0** |
| D | 三个登记对全部删除 | 207 | 207 | **0** | **0** |
| E | 全新的并列 `.md` + `.en.md` 对，无镜像 | 215 | 207 | **8** | **2** |
| F | 全新文件放在别处，**带**真镜像 | 213 | 207 | 6（全是 005/006/007 的） | **2** |

A、B、C、D 全为 `EXIT=0`。因此**目录没有被封死**，被封死的是「不带镜像地往里加文件」。

更精确的机制：`current_bilingual_gaps()` 对 `NORMATIVE_ROOTS` 下每个 `.md` 要求 `docs/en/<path>` 与 `docs/zh-CN/<path>` **同时存在**；`14-ai-development/` 走 `counterpart_14()`，但那只影响 `resolved_14` 的判定，**不影响 `english.is_file()` / `chinese.is_file()` 两项**。所以并列式 `.en.md` 配对本身不能让文件脱离缺口集合——这正是 `governance-register/` 现有 18 个文件（含 `README.md`）全部在基线里的原因，两侧都在。

在真实 PR 上复核（`main` → 三个登记对 + 全部镜像）：`207 frozen, 0 new gaps`，正文补 `BILINGUAL-MANIFEST: COMPLETE` 后 `PASS (18 changed paths inspected)`，`EXIT=0`。

**所以正确的结论是**：`main` 上那个未配对模板使**空 diff**恒为 `EXIT=2`；任何 PR 只要**新增规范文档而不补双侧镜像**也恒为 `EXIT=2`；而补了镜像的 PR 可以通过。初稿把「不补镜像的 PR」写成了「任何 PR」，是过度概括，此处更正。

## 3. 逐步隔离（可复算）

对同一棵 `ae37a419` 树，只做一件事，看退出码：

| # | 操作 | EXIT | 输出 |
|---|---|---|---|
| A | 原样，空 diff | **2** | `New bilingual gap outside frozen baseline: 00-governance/templates/document-metadata-template.md` |
| B | 仅删除该模板文件 | **0** | `bilingual baseline: 207 frozen, 0 new gaps` / `PASS (0 changed paths inspected)` |
| C | 恢复该文件 + 追加一个无关文件 | **2** | 同 A |

B 与 C 互为逆操作，只差那一个文件。**根因被隔离到单个路径，不是推断。**

## 4. 引入点前后对照

| 修订 | 模板存在 | 基线存在 | 空 diff 下 EXIT |
|---|---|---|---|
| `9eca5eda84ce`（`ae37a419` 的父提交） | 否 | 是 | **0**（`207 frozen, 0 new gaps`） |
| `ae37a41900f1`（当前 main） | 是 | 是 | **2** |

两次都在干净 tarball 上、用各自树内的脚本、空 diff、带 `BILINGUAL-MANIFEST: COMPLETE` 执行。**唯一变量是那个新文件。**

## 5. 这次是怎么进来的：直推，无 PR，无审查

`ae37a41900f1` 的提交元数据：

```
author:    unknown <1491856051>     2026-11-21T04:50:35Z
committer: unknown <1491856051>     2026-11-21T04:50:49Z
GitHub 关联账号: null
parents:   9eca5eda84ce
```

- 该 commit **没有关联任何 PR**（`GET /commits/ae37a41900f1/pulls` → `[]`）。
- 作者身份 `unknown <1491856051>` 无法映射到任何账号，是 300 个 main 提交里 7 种身份之一（见 §7）。
- 提交信息自称 `Self-check: 114/114 passed. Incremental gate: PASS.`——`test_check_document_management.py` 的 114 项通过，`check_document_management.py` 的增量门禁通过。**但那个「incremental gate」不是双语门禁**，双语门禁没有被跑过，所以它没发现自己在主干上制造了死锁。

改动面（5 文件 +307/−194）：

| 文件 | 变更 |
|---|---|
| `00-governance/architecture-document-management-policy.md` | +7 −4 |
| `00-governance/architecture-document-metadata.schema.yaml` | +225 −133 |
| `00-governance/templates/document-metadata-template.md` | **+101 −0（新增）** |
| `scripts/check_document_management.py` | +41 −7 |
| `scripts/test_check_document_management.py` | +123 −50 |

## 6. 为什么 005 的 36 小时零执行让这件事更严重

如果 CI 正常，`ae37a419` 若是 PR 就会被自己的门禁拦下；即使直推，`push` 触发的 `bilingual-docs.yml` 也会立刻变红并在几秒内暴露。

实际情况：

| 层 | 状态 |
|---|---|
| PR 门禁 | 零执行（005） |
| `push` 触发的门禁 | 零执行（005 §4：边界后 348 个 failure 中 345 个 `steps=[]`） |
| 直推路径 | 本身不要求 PR（DIRECT-MAIN-001） |
| 结果 | 死锁在主干上存在了 **> 10 分钟且至今无人察觉**，只能靠手工复现发现 |

**三个失效叠加**：直推绕过 PR 审查 → 门禁零执行绕过自动检查 → 基线棘轮把「绕过」固化成不可满足状态。单看任何一层都不致命，叠起来就是「主干不可用」。

**但叠加不等于封死。** §2.1 的六组隔离证明：补双侧镜像的 PR 可以通过（`EXIT=0`）。所以准确的说法是——**主干处于「不补镜像就恒拒绝」的状态**，而不是「无论怎么做都拒绝」。这个区别决定了修法是「补镜像」还是「改规则」：前者不需要任何规范变更。

## 7. main 上的提交身份（300 个提交，2026-11-19T18:06 → 2026-11-21T04:50）

| 次数 | 身份 |
|---|---|
| 231 | `oahcom <81014746+oahcom@users.noreply.github.com>` |
| 26 | `oahcom <oahcom@users.noreply.github.com>` |
| 20 | `Ubuntu <ubuntu@localhost.localdomain>` |
| 10 | `unknown <1491856051>` |
| 7 | `L0-manager <l0@local>` |
| 4 | `oahcom <1491856051>` |
| 2 | `arch-governance <governance@localhost>` |

23 个提交（4 种身份字符串）**无法映射到任何 GitHub 账号**。`unknown <1491856051>` 与 `oahcom <1491856051>` 共用同一个邮箱串，但一个有名一个没名、一个无账号一个有账号——同一台机器上的两次不同配置，不能据此认定是同一人。

## 8. 修法（三条，均未执行）

本登记**不改代码**。以下为可选路径，代价递增：

| # | 做法 | 代价 | 风险 | 实测 |
|---|---|---|---|---|
| F-1 | 把该模板加入 `EMBEDDED_BILINGUAL_SOURCES`（它确实是单文件双语模板，符合该清单的语义） | 1 行 + 1 条 reason 注释 | 最低；与 `#404` 给其他条目补 reason 的做法一致 | §2.1 B 组：`NEW=0` |
| F-2 | 为该模板补 `docs/en` + `docs/zh-CN` 镜像 | 2 个新文件 | 中；一个「模板」被拆成三份，后续三处要同步 | §2.1 A 组：`NEW=0`，且**不需要任何规范变更** |
| F-3 | 把该模板加进 `bilingual-baseline.txt` | 1 行 | **最高**：直接违反「基线只许收缩、永不新增」的规则，会把棘轮变成可被随意扩写的清单 | §2.1 C 组：`NEW=0`，但会破坏棘轮语义 |

推荐 **F-2**（而非初稿推荐的 F-1）：F-2 不需要改动任何规范或脚本，纯文档操作，因此**不触发 §5 的独立审查要求**——它是唯一一条可以被无争议执行的路径。F-1 同样有效，但它是一次规范变更，需要判断「单文件双语模板是否属于豁免类」，按 §5 需独立审查，作者不能自审。

F-3 在技术上有效（C 组 `NEW=0`），但**不得采用**：它把「只许收缩」的棘轮改成可追加清单，等于取消这个机制本身。

## 9. 与本轮其它结论的关系

- **005（零执行）**：本登记是 005 的第一个具体后果。005 说「没有裁决」，本登记说「即使有裁决，当前也是 2」。
- **#409**：该 PR 在 04:20:40Z 被合并（head `ccd19ecd`，base `423fb4b7`）。合并时基线尚未包含 005 的两个文件，因此它与本死锁无关；但它合并后 main 又前进了 26 个提交才到 `ae37a419`。**005 的两个文件至今不在 main 上**（`GET /contents/...CI-NOT-EXECUTED-005.md` → 404）。
- **#414**：`ddd4150bf4` 修正了「配对文件移动被误判为删除」的缺陷（`scripts/check_bilingual_docs.py` +36/−8）。这是门禁实现的一次**真实改进**，但它不触及本死锁——本死锁不是误判，是设计上的正确拒绝。
- **#407**：Owner 在 #407 评论中指出全量扫描器口径 83 vs 门禁口径 88。本登记与它是同一机制的两个面：`current_bilingual_gaps()` 要求 `docs/en` 与 `docs/zh-CN` 双侧存在，因此**并列式 `.en.md` 配对不算配对**——`governance-register/` 现有 18 个文件（含 `README.md`）全部落在基线里，就是这一条的直接后果。
- **DIRECT-MAIN-001**：本登记的引入提交是第 63 次直推，且属于该登记已记录的性质升级（门禁实现被直推改写）的延续——这次连**被门禁管辖的内容**也被直推写入了。

## 10. 客观事实与推断分界

事实：
- §1、§2.1、§3、§4 的全部命令、输入、输出、退出码。
- §5 的提交元数据、PR 关联查询结果、改动行数。
- §7 的 300 提交身份统计。

推断（**不作出**）：
- 不判定 `ae37a419` 的作者「故意」绕过门禁。证据只能说明它没有经过 PR、没有跑双语门禁。
- 不判定 F-1/F-3 是否应被采纳。§8 给的是代价、风险与实测退出码，不是裁定。
- 不把本死锁读成「#401/#408 的棘轮设计有缺陷」。棘轮按设计工作；缺陷在于**新增未配对规范文档与新增基线发生在同一次直推里，且没有任何通道跑过一次门禁**。
- 不把 §2.1 的 A/B/C/D 四组 `EXIT=0` 读成「死锁不存在」。它读成：**分界线是镜像，不是文件内容**。空 diff 仍然 `EXIT=2`，这一点未变。

## 11. 复算方式

```bash
# 1) 取干净树（不要用工作副本，避免本地改动干扰）
curl -L -H "Authorization: Bearer $TOK" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/tarball/ae37a41900f1 | tar xz

# 2) 空 diff 下跑门禁
cd oahcom-AiMemoryBrainArchitecture-ae37a41900f1
git init -q . && git add -A && git commit -qm x
SHA=$(git rev-parse HEAD)
BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"     # -> 2

# 3) 只删该模板再跑
rm 00-governance/templates/document-metadata-template.md
git add -A && git commit -qm y
SHA=$(git rev-parse HEAD)
BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" \
  python scripts/check_bilingual_docs.py; echo "EXIT=$?"     # -> 0

# 4) 对父提交做同样的事
#    （重复 1-2，把 ae37a41900f1 换成 9eca5eda84ce）        # -> 0

# 5) §2.1 的边界：给一组新文件补真镜像，看是否脱离缺口集合
#    直接调用门禁自己的函数，避免被 diff 口径干扰：
python - <<'PY'
import importlib.util, os, sys
os.chdir(".")
spec = importlib.util.spec_from_file_location("g", "scripts/check_bilingual_docs.py")
g = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(g)
gaps, base = g.current_bilingual_gaps(), g.read_baseline()
print("gaps", len(gaps), "baseline", len(base), "NEW", len(sorted(gaps - base)))
PY
# 补 docs/en/<path> + docs/zh-CN/<path> 后重跑，NEW 归零
```

**登记状态**：`OPEN` / `ACTIVE` / main 上空 diff 恒为 `EXIT=2` / 判定分界是「是否补双侧镜像」而非「改了哪个文件」（§2.1）/ 引入方式为直推无 PR / 推荐修法 F-2 为纯文档操作，未执行
