# GOV-NC-2026-11-21-SPLIT-DOMAIN-011 — 并排配对只实现在缺口扫描域，diff 判定域仍强制镜像：四个真实配对在主干上无法被编辑

## 0. 性质与结论

```
MEASUREMENT_ONLY / NO_IMPLEMENTATION / REQUIRES_INDEPENDENT_REVIEW
```

本文件记录一组**在真实克隆、真实 git 历史**上重复得到的实测结果。它不提出实现，不授权合并。

**结论一句话**：main `cb04524` 上，`current_bilingual_gaps()`（缺口扫描域）已承认并排配对，`check_normative_pairing()`（diff 判定域）**没有**。两个判定域对同一份改动给出相反结论。后果是：仓库里**四个真实存在的并排配对**，任何一个被编辑都会让门禁返回 `EXIT=1`，且**没有任何合法的绕过方式**。

## 0.1 本文包含一次自我更正

上一轮我曾判断「PR #470 把 `scripts/bilingual-baseline.txt` 写成了 GitHub API 的 JSON 响应体」。**该判断错误，已撤回。**

原因在我的测量装置：`GET /repos/{r}/git/blobs/{sha}` 返回的是 `{"sha":...,"content":"<base64>","encoding":"base64"}` 包装体，我的 `fetch_blob()` 直接把这个包装体写成了文件，于是每个"下载"的文件都是 JSON。用正确解码重测后，#470 的基线是合法的 80 条纯文本。

**这条更正的重要性**：它说明本系列的测量结论必须附带解码方式。所有 §2 起的结论都已用修正后的装置重跑。

## 1. 现状（main `cb04524`，实测）

### 1.1 两个判定域的代码位置

| 判定域 | 函数 | 是否承认并排配对 |
|---|---|---|
| 缺口扫描（全树） | `current_bilingual_gaps()` | **是**（#462 已合入） |
| diff 判定（本 PR 变更） | `check_normative_pairing()` | **否** |

`check_normative_pairing()` 第 730–732 行，对非 `14-ai-development` 的规范源**无条件**要求：

```python
en = f"docs/en/{source}"
zh = f"docs/zh-CN/{source}"
errors.extend(check_counterpart_requirement(source, [en, zh], changed, statuses, exception))
```

它不调用 `side_by_side_partner()`。而 `current_bilingual_gaps()` 已调用。

### 1.2 后果：四个真实配对全部无法编辑

在 main 上逐个编辑**两侧都已存在**的并排配对（改动同时落在 `.md` 与 `.zh-CN.md`），门禁返回：

| 配对 | 根 | `EXIT` | 错误类型 |
|---|---|---|---|
| `02-domain-model/phase-2-domain-extension` | `02-domain-model` | **1** | `PAIR` ×2 |
| `06-memory-context/context-implementation-coverage` | `06-memory-context` | **1** | `PAIR` ×2 |
| `07-agent-integration/adapter-capability-tiers` | `07-agent-integration` | **1** | `PAIR` ×2 |
| `08-bmcp-protocol/protocol-index` | `08-bmcp-protocol` | **1** | `PAIR` ×2 |
| `06-memory-context/phase-3.8.22-...-contract` | `06-memory-context` | **1** | `PAIR` ×2 |

典型报错原文：

```
::error::02-domain-model/phase-2-domain-extension.md requires all counterparts changed in this PR:
  02-domain-model/phase-2-domain-extension.md, docs/en/02-domain-model/phase-2-domain-extension.md,
  docs/zh-CN/02-domain-model/phase-2-domain-extension.md
```

**两侧都改了，仍然失败**——因为要求的是 `docs/` 下的两个镜像，而这对文件按政策**本来就不该有镜像**。

### 1.3 新增并排配对同样失败

| 用例 | `EXIT` |
|---|---|
| `02-domain-model/p.md` + `p.zh-CN.md`（新增） | **1** |
| `02-domain-model/q.en.md` + `q.zh-CN.md`（新增） | **1** |
| `13-engineering-decisions/p.md` + `p.zh-CN.md`（新增） | **1** |

对照组（说明这不是"新增文件一律失败"）：

| 对照组 | `EXIT` |
|---|---|
| `02-domain-model/m.md` + `docs/en/m.md` + `docs/zh-CN/m.md`（镜像三件套） | **0** |
| `14-ai-development/s.md` + `s.zh-CN.md`（**14 根**并排） | **0** |
| `02-domain-model/r.md` 单文件（无配对） | **2**（`GAP`，正确） |

**`14-ai-development` 通过、其余八根失败**——这是 `check_normative_pairing()` 里 `if source.startswith("14-ai-development/")` 分支的直接结果。

## 2. 死锁没有合法出口（逐条实测）

`check_counterpart_requirement()` 的 `exception` 参数是唯一出口，但它只在 PR body 携带**完整七字段**的 `BILINGUAL-EXCEPTION: APPROVED` 时为真：

| 尝试 | `EXIT` | 说明 |
|---|---|---|
| 只写 `BILINGUAL-EXCEPTION: APPROVED` + 自造理由 | **1** | 七字段不全 |
| 补齐七字段（`Exception Owner` / `Authoritative language/version` / `Missing counterpart path` / `Exact source revision` / `Due date` / `Tracking Issue/PR` / `Approval evidence`） | **0** | **唯一可行路径** |

**这意味着**：任何对并排配对的编辑，都必须伪造一条"缺镜像"的例外声明才能通过。而按政策，并排配对**不缺任何东西**——要求它为不存在的缺失开例外，是把正确做法登记成缺陷。

同时门禁自己打印：

```
Approved bilingual exception declaration detected; human governance approval remains mandatory.
```

即 `EXIT=0` 只表示**语法完整**，不表示例外被批准。

## 3. 这不是我这份规格的预测——是规格被绕过的结果

`SPEC-2026-11-21-PAIRING-001.md` §4.1 明确要求**两处判据同时改**，并在 §4.5.2c 给出实测证据：只改缺口扫描时 #433/#435/#436 仍 `EXIT=1`。

合入 main 的 #462 **只改了缺口扫描**。它自己 PR body 的 N3/N4 用例写着「ACCEPT, rc=0」，但那是 **no-op 形态**（`BASE_SHA == HEAD_SHA`）下的结果。用真实 PR-diff 形态（`BASE_SHA = HEAD~1`）重跑同一用例：

```
PR462 head 7de3111    no-op rc=0 | diff rc=1
main after 462        no-op rc=0 | diff rc=1
origin/main           no-op rc=0 | diff rc=1
```

**N3/N4 的 ACCEPT 结论只在空 diff 下成立。** 这不是说 #462 的作者造假——no-op 是仓库既有的标准验证形态（`NOOP_RC`），只是它无法覆盖 diff 判定域。

## 4. 顺带发现：镜像形态出现回归

`current_bilingual_gaps()` 的新判定式：

```python
paired = mirrored or side_by_side_partner(source) is not None or (english.is_file() and _carries_chinese(source))
```

第三个分支 `english.is_file() and _carries_chinese(source)` **不再要求 `chinese.is_file()`**。原来只对 `14-ai-development` 生效（Shape 3），现在对九个根全部生效。

实测后果：

| 用例 | `0ca4d93`（118 基线） | main `cb04524`（80 基线） |
|---|---|---|
| `02-domain-model/hm.md`（中文）+ `docs/en/hm.md`（英文），**无 `docs/zh-CN`** | **GAP**（正确） | **accepted**（回归） |

即：**中文源 + 英文镜像、缺中文镜像**，现在被判定为已配对。这是 `docs/zh-CN/` 侧可以整体缺席。

## 5. 基线 118 → 80 的逐条归因（38 条全部闭合）

| 机制 | 条数 | 说明 |
|---|---|---|
| 并排配对（`14-ai-development`） | **29** | 与规格 §4.5.2b-2 对账结果一致 |
| 并排配对（非 14 根） | **1** | `07-agent-integration/adapter-capability-tiers.md` |
| Shape 3 从 14 根扩到全根 | **3** | `AI-EXEC-001.md`、`AI-EXEC-002.md`、`AI-EXEC-ROLLOUT-001.md` |
| 镜像实际补齐（#470 等） | **5** | `06-memory-context/README.md` + 4 个 `phase-3.6.x` |
| 未解释 | **0** | — |
| **合计** | **38** | |

每一步的基线都是自洽的（`baseline == gaps`，`new=0`，`resolved=0`）：

| 提交 | baseline | gaps | new | resolved |
|---|---|---|---|---|
| `0ca4d93` | 118 | 118 | 0 | 0 |
| `e6db42f` | 86 | 86 | 0 | 0 |
| `7de3111` | 85 | 85 | 0 | 0 |
| `704a712` | 80 | 80 | 0 | 0 |
| `cb04524` | 80 | 80 | 0 | 0 |

**注意**：`29 + 1 + 3 + 5 = 38`，而规格预测的是 29。差额 9 = 1（非14并排）+ 3（Shape3 扩根）+ 5（镜像补齐）。**规格只预测了并排那 29 条，另外 9 条来自规格未建议的两处改动。**

## 6. 唯一性规则未被采纳（规格 §4.5.2 的反例）

main 的 `side_by_side_partner()` 是**先匹配即返回**，无唯一性检查：

```python
elif source.endswith(".md"):
    stem = source[: -len(".md")]
    for cand in (stem + ".en.md", stem + ".zh-CN.md"):
        if cand != source and (ROOT / cand).is_file():
            return cand
```

实测三文件并存（`X.md` + `X.en.md` + `X.zh-CN.md`）：

```
p(u1.md)       = u1.en.md
p(u1.en.md)    = u1.zh-CN.md
p(u1.zh-CN.md) = u1.en.md
```

`partner(partner(x)) != x` —— 规格 §4.5.1 记录的这个循环**在 main 上依然存在**，且三个文件**全部被判为已配对**（`gaps=0`）。

同时**英文冒充中文**也被接受：

| 用例 | 结果 |
|---|---|
| `fake.md`（英文）+ `fake.zh-CN.md`（英文） | 两者都**不在** gaps |

即 `.zh-CN.md` 后缀 + 英文内容 = 通过。这是 #468 试图修的问题，**尚未合入**。

## 7. #468 不解决本文的主缺陷（实测）

`#468`（`fix(bilingual): reject side-by-side pairs without Chinese content`）只改缺口扫描域的内容校验。在 main + #468 overlay 上重跑：

| 用例 | main | main + #468 |
|---|---|---|
| 编辑 `02-domain-model/phase-2-domain-extension` 两侧 | `EXIT=1` `PAIR`×2 | **`EXIT=1` `PAIR`×2** |
| 编辑 `08-bmcp-protocol/protocol-index` 两侧 | `EXIT=1` `PAIR`×2 | **`EXIT=1` `PAIR`×2** |
| 新增 `02-domain-model/newpair.md` + `.zh-CN.md` | `EXIT=1` `PAIR`×2 | **`EXIT=1` `PAIR`×2** |

**#468 合入后死锁依旧。** 它修的是"假中文"，不是"两个判定域不一致"。

## 8. 影响面

| 项 | 状态 |
|---|---|
| 可编辑的并排配对（非 14 根） | **0 个**（四个全部 `EXIT=1`） |
| 新增并排配对（非 14 根） | **不可能**（`EXIT=1`） |
| 合法绕过 | 仅"七字段例外声明"（把正确做法登记为缺陷） |
| `docs/zh-CN` 侧缺失 | 被静默接受（§4 回归） |
| 三文件歧义 | 被静默接受（§6） |
| 英文冒充 `.zh-CN.md` | 被静默接受（§6） |

## 9. 本文不主张的事

- 不主张 #462 的作者有欺骗意图。no-op 是仓库既有验证形态。
- 不主张 main 当前是"红的"。`baseline == gaps` 在每一步都成立，**空 diff 恒 `EXIT=0`**。缺陷只在**有并排配对改动时**显形。
- 不主张本文提出的任何修复。本文只登记测量结果。
- 不主张 §4 的回归是 #462 引入的唯一原因；它也可能是 Shape-3 扩根的有意副作用。**这需要 Owner 裁定政策意图**。

## 10. 需要裁定的事项

| 编号 | 事项 | 需要谁 |
|---|---|---|
| Q-1 | 并排配对政策是否适用于**非 14 根**（政策已定"是"，代码只实现了一半） | Owner 确认代码须补齐 |
| Q-2 | `docs/zh-CN` 缺失被接受（§4）是**有意放宽**还是**副作用** | Owner |
| Q-3 | 三文件歧义与英文冒充中文（§6）是否在 #468 合入后解决 | 独立审查者 |
| Q-4 | 七字段例外是否是并排配对的**预期**通过路径 | Owner（若否，则当前无合法路径） |

## 11. 复现

环境：真实克隆 `origin/main` = `cb04524`，Python 3.13，无 CI。

```bash
git clone https://github.com/oahcom/AiMemoryBrainArchitecture.git
cd AiMemoryBrainArchitecture
git checkout cb04524

# 编辑一个真实并排配对的两侧
printf '\n<!-- t -->\n' >> 02-domain-model/phase-2-domain-extension.md
printf '\n<!-- t -->\n' >> 02-domain-model/phase-2-domain-extension.zh-CN.md
git commit -qam probe

BASE_SHA=HEAD~1 HEAD_SHA=$(git rev-parse HEAD) \
  PR_BODY='BILINGUAL-MANIFEST: COMPLETE' \
  python3 scripts/check_bilingual_docs.py
# -> EXIT=1, 2 x "requires all counterparts changed in this PR"

# 对照组：空 diff
BASE_SHA=$(git rev-parse HEAD) HEAD_SHA=$(git rev-parse HEAD) \
  PR_BODY='BILINGUAL-MANIFEST: COMPLETE' \
  python3 scripts/check_bilingual_docs.py
# -> EXIT=0
```

**复现的关键是 `BASE_SHA` 必须是真实父提交。** 用 `BASE_SHA == HEAD_SHA` 会得到 `EXIT=0`，从而看不到本缺陷——这正是 §3 记录的 #462 验证形态问题。

## 12. 状态

```
SPLIT_DOMAIN_CONFIRMED / DEADLOCK_NO_LEGAL_EXIT / MIRROR_REGRESSION_OBSERVED
INDEPENDENT_REVIEW: NOT_ASSIGNED
IMPLEMENTATION_AUTHORISATION: NOT_AUTHORISED
```
