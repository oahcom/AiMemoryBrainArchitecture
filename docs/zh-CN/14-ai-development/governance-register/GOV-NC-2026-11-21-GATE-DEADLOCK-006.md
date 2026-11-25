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
      last_verified_date: "2026-11-21"
      last_verification_note: "All figures come from the GitHub REST API and from local gate runs on 2026-11-21; the 2026-11-25 annotations added in §12.3, §14.1 and §14.2 record no new measurement and change no number."
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
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md"
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md"
    zh-CN: null
---

# GOV-NC-2026-11-21-GATE-DEADLOCK-006 — 门禁在 main 上自我死锁：任何 PR 都无法通过

- 登记编号：GOV-NC-2026-11-21-GATE-DEADLOCK-006
- 状态：`RESOLVED_ON_MAIN` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY`（Owner 2026-11-21 裁定，见 §14）/ 解除方式为自我审查合并，见 §12
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
| F-2 | 为该模板补 `docs/en` + `docs/zh-CN` 镜像 | 2 个新文件 | 低；镜像**不是**新正文，是同一源文件的副本（见下） | §2.1 A 组：`NEW=0`，且**不需要任何规范变更** |
| F-3 | 把该模板加进 `bilingual-baseline.txt` | 1 行 | **最高**：直接违反「基线只许收缩、永不新增」的规则，会把棘轮变成可被随意扩写的清单 | §2.1 C 组：`NEW=0`，但会破坏棘轮语义 |

**F-2 的含义必须写清，否则容易被误读为「把一个模板拆成三份」：**

镜像指的是**同一源文件的逐字副本**，不是三份可以各自演化的正文。`00-governance/templates/document-metadata-template.md` 继续作为唯一权威来源，留在原位；`docs/en/...` 与 `docs/zh-CN/...` 只是它的存在性满足物。任何对模板内容的修改，仍然只改源文件，镜像跟随。

这一点不是本登记的推断，而是 Owner 在 2026-11-21 裁定中明确的边界：

> **关于 `document-metadata-template.md`：不批准拆成三份。**
> 模板应继续保留在 `00-governance/templates/` 的既有位置，作为单一模板来源。若该文件属于门禁要求镜像的范围，则按同一源文件补齐两侧镜像；不能为了迎合扫描结果而复制出三份各自演化的模板正文。

因此 F-2 的正确执行是「一源 + 两副本」，不是「三份正文」。

推荐 **F-2**（Owner 已批准，F-1 不列为本轮首选，F-3 不批准）。F-2 不需要改动任何规范或脚本，纯文档操作；F-1 同样有效（B 组 `NEW=0`），但它是一次规范变更，需判断「单文件双语模板是否属于豁免类」，按 §5 需独立审查，作者不能自审。Owner 同时限定：**不得把 `EMBEDDED_BILINGUAL_SOURCES` 当作新增登记的默认通道**。

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

**登记状态**：`ACCEPTED` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY` / main 上空 diff 恒为 `EXIT=2`（`81dd9a72d2` 起解除，见 §12）/ 判定分界是「是否补双侧镜像」而非「改了哪个文件」（§2.1）/ 引入方式为直推无 PR / 推荐修法 F-2 已获 Owner 批准但未执行，实际执行 F-1（§14）

Owner 裁定（2026-11-21）摘要：

- 采纳 §2.1 的边界更正，撤销初稿「任何 PR 都得到 `EXIT=2`」的过宽表述。
- **批准 F-2**（补齐双侧镜像）；F-1 不列为本轮首选；F-3 不批准。
- F-2 的执行约束：镜像须对应正确源路径，不得用无关文件或占位文件满足存在性检查；不改 `NORMATIVE_ROOTS`、门禁脚本、豁免白名单或基线；不得把 `EMBEDDED_BILINGUAL_SOURCES` 当作新增登记的默认通道。
- **不批准把 `document-metadata-template.md` 拆成三份**：模板留在 `00-governance/templates/` 作为单一来源，镜像只是同一源文件的副本。
- F-2 的镜像补齐可作为机械文档操作，不要求逐字另行授权；但若 PR 同时含治理判断、规范内容变化、模板语义变化或豁免授权，仍按相应审查要求处理。

---

## 12. 死锁已在 main 上解除 —— 用 F-1，且通过自我审查合并

### 12.1 事实

本登记写完之后约 12 分钟，死锁被解除。解除过程如下：

| 项 | 值 |
|---|---|
| Issue | #416 `[P0] main is red: ae37a419 added a normative source with no bilingual mirror and...`，创建 2026-11-21T05:13:04Z，关闭 05:52:03Z |
| PR | #418 `fix(bilingual): register metadata template exemption (#416)` |
| 改动 | 仅 `scripts/check_bilingual_docs.py`，**+5 −0** |
| 实质 | 把 `00-governance/templates/document-metadata-template.md` 加入 `EMBEDDED_BILINGUAL_SOURCES`，附一段 reason |
| author | `oahcom` |
| 唯一 reviewer | `oahcom`，`COMMENTED`，05:51:33Z |
| merger | `oahcom`，05:51:45Z |
| review → merge | **12 秒** |
| merge commit | `fce408340c3f` |

加入的条目原文：

```python
"00-governance/templates/document-metadata-template.md": (
    "Provides one copy-paste metadata block whose field names, closed enums, "
    "and REQUIRED markers are consumed verbatim by check_document_management.py; "
    "split mirrors would let the two languages document different enum values."
),
```

### 12.2 复验：main 上空 diff 已为 EXIT=0

在 `main` `81dd9a72d2` 的干净树上：

```
$ BASE_SHA=$SHA HEAD_SHA=$SHA PR_BODY="BILINGUAL-MANIFEST: COMPLETE" python scripts/check_bilingual_docs.py
bilingual baseline: 207 frozen, 0 new gaps
exemptions: 21
Bilingual documentation and prompt-library gate: PASS (0 changed paths inspected).
EXIT=0
```

且：

```
exemptions 21
template exempt: True
gaps 207  baseline 207  NEW 0
```

**本登记 §1 的核心断言（空 diff 恒为 `EXIT=2`）在 `main` 上已不再成立。** 这不是推断，是实测。

### 12.3 三点必须同时记录，不得互相抵销

**第一，修法用的是 F-1，不是 Owner 批准的 F-2。**

Owner 裁定「批准 F-2；F-1 不列为本轮首选；F-3 不批准」，并明确「不得把 `EMBEDDED_BILINGUAL_SOURCES` 当作新增登记的默认通道」。而实际执行的是 F-1。

这不必然是违规：F-1 在本登记 §2.1 的 B 组实测中同样 `NEW=0`，且 §8 承认它技术有效。但**它是一次规范变更，按 §5 需独立审查**，而 §12.1 显示审查者是作者本人。

> **〔2026-11-25 附注〕** 本句把「§12.1 表中 `author` 与唯一 `reviewer` 同为 `oahcom`」这一账号层事实，当作「这次规范变更未取得独立审查」的理由。§5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）：同一 GitHub 身份下的另一会话即可构成独立审查。`/pulls/{n}/reviews` 只返回 `user.login`，不返回会话，故「同一身份 ⇒ 同一会话」这一步在该载荷里无法核实；§12.1 的表也不含会话标识，会话层无从查证。此处应读作「账号层不独立、会话层未核实」。
> **仍然成立的部分**：§12.1 记录该 PR 只有一次审查，状态为 `COMMENTED`。§5 明写 `COMMENT` 是技术评论、不是 `APPROVE`，这一点与判据版本无关；因此「未取得独立审批」的结论保留，依据从账号比较换成「唯一一次审查不是 `APPROVE`」。被撤销的只是账号比较那一步。

**第二，解除死锁的那次合并，本身就是 007 记录的失效模式。**

`author == sole reviewer == merger`，间隔 12 秒，`COMMENTED` 状态。这与 007 §1 表中六例完全同形。

> **〔2026-11-25 附注〕** 本句把「`author == sole reviewer == merger`」这个账号三元组，当作「与 007 §1 六例同形、即同属自我审查」的理由。§5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）：同一 GitHub 身份下的另一会话即可构成独立审查。`/pulls/{n}/reviews` 只返回 `user.login`，不返回会话，「同一身份 ⇒ 同一会话」在该载荷里无法核实。此处应读作「账号层不独立、会话层未核实」。
> **仍然成立的部分**：12 秒间隔与 `COMMENTED` 状态是 §12.1 表中可核的字段，不依赖身份如何定义；且 `COMMENT` 在任何版本的 §5 下都不是 `APPROVE`，故「这次合并没有 `APPROVE`」成立。不成立的是「同形 ⇒ 同属自我审查」这一步：账号相同推不出会话相同。

因此出现一个必须直说的循环：

> 006 记录的是「门禁在主干上不可满足」。
> 007 记录的是「合并靠自我审查」。
> 而 006 的解除，是通过 007 描述的方式完成的。

**第三，解除本身在技术上是有效的，且理由站得住。**

`document-metadata-template.md` 的 reason 写得很具体：它的字段名、闭合枚举与 `REQUIRED` 标记被 `check_document_management.py` **逐字消费**，如果拆成双语镜像，两侧可能记录不同的枚举值。这个理由与 F-1 的语义（单文件双语源）吻合，也与 Owner「不批准拆成三份」的裁定方向一致。

所以准确的记录是：**结果正确，程序未满足 §5。** 两者都要写，不能只写一个。

> **〔2026-11-25 附注〕** 本句后半「程序未满足 §5」原先建立在「`author == sole reviewer == merger`」这个账号等式上。§5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）：同一 GitHub 身份下的另一会话即可构成独立审查；`/pulls/{n}/reviews` 只返回 `user.login`，不返回会话，故「同一身份 ⇒ 同一会话」无法核实。账号比较这一步应读作「账号层不独立、会话层未核实」。
> **仍然成立的部分**：「结果正确」不动。后半的结论也保留，但依据换了——§12.1 表记录该 PR 只有一次审查，`COMMENTED`，`oahcom`，合并前 12 秒。§5 明写 `COMMENT` 是技术评论、不是 `APPROVE`，这一点与判据版本无关；「唯一一次审查不是 `APPROVE`」在任何版本的 §5 下都成立，故「程序未满足 §5」仍成立。不成立的是「同一账号 ⇒ 同一会话」。

### 12.4 对本登记结论的影响

| 断言 | 状态 |
|---|---|
| §1 空 diff 在 `main` 上恒为 `EXIT=2` | **已失效**（`81dd9a72d2` 起 `EXIT=0`） |
| §1 死锁跨 7 个提交持续存在 | 成立（`ae37a419` → `7d2233a5`） |
| §2.1 判定分界是「是否补双侧镜像」 | **仍成立**，且被 #418 从反面确认：不补镜像时，唯一出路是进豁免清单 |
| §8 F-2 为首选修法 | Owner 批准，但未被执行；实际执行 F-1 |
| §7 三失效叠加 | 仍成立；#418 未触及 005 的零执行 |

### 12.5 一个更精确的机制结论

把 §2.1 的六组与 §12.1 合起来看，`NORMATIVE_ROOTS` 下新增文件的通过条件实际有**三条**，不是两条：

1. 补 `docs/en` + `docs/zh-CN` 双侧镜像（A 组）；
2. 进入 `EMBEDDED_BILINGUAL_SOURCES` 豁免清单（B 组，即 #418 走的路）；
3. 追加进 frozen baseline（C 组，会破坏棘轮语义，不应使用）。

第 1 条不需要规范变更；第 2 条需要一次规范变更并经独立审查；第 3 条不可用。

本登记初稿把「不补镜像就恒拒绝」当成唯一分界，遗漏了第 2 条。这是第二处过度概括，此处一并更正。

---

## 13. 本登记自己的 PR 必须长成什么样 —— 结构门禁与语义正确性之间没有联系

### 13.1 门禁对 `14-ai-development/` 根目录文件的真实要求

`current_bilingual_gaps()` 对 `NORMATIVE_ROOTS` 下每一个 `*.md` 做的是**硬性两侧检查**：

```python
english = REPO_ROOT / "docs" / "en" / source
chinese = REPO_ROOT / "docs" / "zh-CN" / source
if not english.is_file() or not chinese.is_file() or resolved_14 is None:
    gaps.add(source)
```

`resolved_14` 调用的 `counterpart_14()` 认并排命名（`X.md` ↔ `X.en.md`），但上面两个 `is_file()` **不认**。也就是说：并排命名能让 `resolved_14` 非空，却不能让 `docs/en/` 与 `docs/zh-CN/` 存在。

实测（本登记三份文件，`main` `ad4d7221f9`）：

| 组 | 形态 | 文件数 | 结果 |
|---|---|---|---|
| S1 | 仅根目录 `X.md` + `X.en.md`（并排） | 6 | `::error::New bilingual gap outside frozen baseline` × 6，`EXIT=2` |
| S2 | S1 + `docs/en`、`docs/zh-CN` 各放 `X.md` 与 `X.en.md` | 12 | 仍 `EXIT=2`（`.en.md` 两侧镜像缺失，报 3 条） |
| S3 | 根 `X.md`(中) + `docs/en/X.md`(英) + `docs/zh-CN/X.md`(中) | 9 | **`EXIT=0`**，`207 frozen, 0 new gaps` |
| T-a | 无根文件，仅 `docs/en`(英) + `docs/zh-CN`(中) | 6 | **`EXIT=0`** |

结论：新登记在 `14-ai-development/` 下**不能只靠并排 `.en.md` 通过**；必须给 `docs/en/` 与 `docs/zh-CN/` 两侧真镜像。

### 13.2 「加进基线」不是出路

C 组（§2.1）只测到 `current_bilingual_gaps()` 这一关。把文件写进 `scripts/bilingual-baseline.txt` 之后，**第二个检查会拒绝**：

```
$ # 加一个 14-ai-development/probe-single.md 并写进 baseline
bilingual baseline: 208 frozen, 0 new gaps
::error::14-ai-development/probe-single.md has no resolvable bilingual counterpart
         (side-by-side .en.md/.zh-CN.md or docs/en mirror); pair it, register it in
         EMBEDDED_BILINGUAL_SOURCES, or use a documented BILINGUAL-EXCEPTION
Bilingual documentation gate: FAIL
EXIT=1
```

所以 §2.1 的「C 组 `NEW=0`」只在第一关成立。基线扩写既违反棘轮语义，**在技术上也走不通**——两道检查串联，扩写基线只是把 `EXIT=2` 换成 `EXIT=1`。

### 13.3 一个必须直说的缺陷：门禁无法识别「镜像内容是另一语言的复制」

本登记 PR #419 的初版是 18 个文件，形态为：

```
14-ai-development/governance-register/X.md          (中文)
14-ai-development/governance-register/X.en.md       (英文)
docs/en/14-ai-development/governance-register/X.md  (中文 ← 与根目录同 blob)
docs/zh-CN/14-ai-development/governance-register/X.md (中文 ← 同 blob)
```

`docs/en/` 里装的是**中文正文**。实测哈希：

```
97c43724309d 14895  14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.md
a2ab8d078533 16635  14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.en.md
97c43724309d 14895  docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.md
97c43724309d 14895  docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.md
```

`docs/en` 与根目录**同一个 blob**，即英文目录里放的是中文。而这个形态**门禁判定为 `EXIT=0`**。

这不是门禁的 bug，是它的设计边界——脚本自己在通过时打印：

```
This is a structural gate only; semantic parity requires independent review.
```

但它有一个直接后果必须记录：**「补齐双侧镜像」这个动作可以被机械地满足，而语义完全不对。** 如果执行者只盯 `EXIT=0`，他会交出一份英文目录装中文的文件，并且门禁会替他背书。本登记初版就是这样，是我自己写出来的，不是别人。

### 13.4 处置

本 PR 重塑为 S3 形态（9 文件）：根目录留中文正文，`docs/en/` 放**真正的英文**（原 `X.en.md` 的内容），`docs/zh-CN/` 放中文。删掉并排 `.en.md`，删掉 `docs/en` 里的中文副本。

理由有两条，且互相独立：

1. **门禁要求**：S3 是 `EXIT=0` 的最小且符合仓库既有惯例的形态。仓库既有规范文档（如 `00-governance/design-principles.md`）正是「根 + `docs/en` + `docs/zh-CN`」三件套。
2. **Owner 裁定**：不得为迎合扫描结果复制正文。初版 18 文件里 `docs/en` 装中文，正是这种复制。

### 13.5 对本登记结论的影响

| 断言 | 状态 |
|---|---|
| §2.1 判定分界是「是否补双侧镜像」 | **成立，但需精确化**：补的是 `docs/en` 与 `docs/zh-CN` 两个**目录下的真文件**，不是并排 `.en.md` |
| §2.1 C 组「加基线 `NEW=0`」 | **收窄**：只过第一关，第二关 `EXIT=1`（§13.2） |
| §12.5 三条通过路径 | **收窄为两条半**：镜像（需两目录）、豁免清单、基线（技术不可行且违反棘轮） |
| 门禁能保证语义正确 | **不能**，且已有反例（§13.3） |

---

## 14. Owner 裁定（2026-11-21）：F-1 对该模板的受限等效，与 #418 程序状态不追认

### 14.1 裁定原文要点

| 维度 | 裁定 |
|---|---|
| F-1 技术路径（对 `document-metadata-template.md`） | **接受** |
| 模板豁免的当前治理依据 | **本轮批准**（此前无依据） |
| #418 当时是否获得事前授权 | **否** |
| #418 是否满足独立审查要求 | **否**〔2026-11-25 附注：该「否」建立在 §12.1 的账号三元组上；§5 已于 2026-11-24 改为会话层判据，而账号层不独立、会话层未核实。该「否」本身仍成立，但依据是唯一一次审查为 `COMMENTED`、非 `APPROVE`，此点与判据版本无关。原文保留〕 |
| #418 的合并程序是否合规 | **不合规**〔2026-11-25 附注：该「不合规」建立在 §12.1 的账号三元组上；§5 已于 2026-11-24 改为会话层判据，而账号层不独立、会话层未核实。该「不合规」本身仍成立，但依据是唯一一次审查为 `COMMENTED`、非 `APPROVE`，此点与判据版本无关。原文保留〕 |
| F-1 是否成为新登记的通用通道 | **否**，仅限该模板 |

裁定给出的技术理由与本登记 §12.3 第三点一致：该模板的字段名与闭合枚举被 `check_document_management.py` 逐字消费，拆镜像会导致两侧记录不同枚举值。

但裁定同时划出五条边界，全部必须记录：

1. 仅适用于该模板，**不构成其他新登记文件采用 F-1 的一般授权**；
2. 机器消费的字段名、枚举值必须保持唯一、稳定的权威写法；
3. 面向使用者的说明可双语，但**不得翻译或改写机器消费的标识符**；
4. 豁免必须明确记录原因、范围与权威来源，**不得扩展为目录级豁免**；
5. **不得把 F-1 的通过解释为中英文语义等价已经得到验证**。

### 14.2 「事后批准 ≠ 事前授权」

裁定明确：「本轮批准不追溯改变 #418 合并时的程序状态。不得把事后批准写成事前授权，也不得因此关闭或弱化 `SELF-REVIEW-007`。」

这一条是本登记必须固化的判据。`#418` 的事实链不变：

```
author = oahcom
sole reviewer = oahcom   (COMMENTED, 05:51:33Z)
merger = oahcom          (05:51:45Z)
review → merge = 12 秒
```

F-1 技术结果被接受，与该次合并未满足 §5 是**两个独立事实**。§12.3 的三点并列结构因此保持不变，只是第一点的表述由「不是 Owner 批准的 F-2」升级为「F-2 曾获事前批准；实际执行 F-1；Owner 事后基于机器消费约束批准 F-1 作为该模板的受限等效路径」。

> **〔2026-11-25 附注〕** 上一段把「该次合并未满足 §5」建立在上面代码块的三行账号记录上——那是账号层事实，被当作审查层结论的理由。§5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）；`/pulls/{n}/reviews` 只返回 `user.login`，不返回会话，「同一身份 ⇒ 同一会话」无法核实。代码块本身是事实记录，保持原样；账号比较这一步应读作「账号层不独立、会话层未核实」。
> **仍然成立的部分**：块内「唯一一次审查是 `COMMENTED`」在任何版本的 §5 下都不是 `APPROVE`，故「未满足 §5」的结论保留，依据换成这一条，而不是账号相等。

### 14.3 对本登记结论的影响

| 断言 | 裁定后状态 |
|---|---|
| §8 推荐 F-2 | Owner 事前批准 F-2，但**未执行**；F-1 获事后受限批准 |
| §12.1 修法用 F-1 而非 F-2 | 事实不变；程序偏差**保留**，不被事后批准消除 |
| §12.5 三条通过路径 | 维持 §13.5 的收窄结论：镜像（两目录）/ 豁免清单（需逐案批准）/ 基线（技术不可行且违反棘轮） |
| §13.3 门禁不能区分镜像与复制 | 不变；且被裁定第 5 条边界间接确认（`EXIT=0` 不推定语义等价） |
| 本登记自身状态 | `ACCEPTED`，但 main 上的实际修复路径与本登记推荐路径不同，此差异永久记录 |
