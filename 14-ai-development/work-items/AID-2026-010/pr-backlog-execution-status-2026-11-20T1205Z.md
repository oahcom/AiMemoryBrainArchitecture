# AID-2026-028 执行状态更新（L0，2026-11-20T12:05Z）

**关系：** 本文件是 `pr-backlog-convergence-plan.md`（AID-2026-028）的**执行状态附录**，不是该裁定的修订版。
**冲突处理：** 凡与 AID-2026-028 正文冲突处，以本文件记载的**实测值**为准（正文为落库时点快照，本文件为执行后测量）；裁定的授权边界、冻结纪律、处置原则本身**不变**。

## 一、正文已过期的三个字段

| AID-2026-028 正文 | 落库时值 | 实测当前（`2026-11-20T12:05Z`） |
|---|---|---|
| `Current observed open PR count` | 9 | **1** |
| `Observed main HEAD` | `5972a1d2…` | **`94cbb4db…`**（此后仍在推进） |
| PR 333 合并状态 | 「merged status not independently supplied」 | **merged，`2026-11-20T09:50:53Z`** |

正文的「The current open-PR count is 9」与「PR 333 has supplied successful local test evidence, with its merge record requiring confirmation」两句，已被实测取代。裁定原则不受影响。

## 二、17 条受跟踪 PR 的处置执行结果

| 处置 | PR | 执行结果 |
|---|---|---|
| `RETITLE-AND-DECLARE` | 320, 328, 331, 340 | 320/328/331 merged；340 由 #341 + #342 取代后关闭 |
| `REBASE-THEN-MERGE` | 321, 322, 326, 327, 334, 335 | **全部改为 `CONVERGED-EMPTY` 并合并**（见第三节） |
| `HOLD` | 323, 330, 337, 338 | 323/337/338 merged；**330 仍 open（draft，`dirty`）** |
| `CONVERGED-MERGED` | 332, 339 | 已确认 |
| `CONVERGED-VERIFIED` | 333 | 已确认合并 `09:50:53Z` |
| 计划外 | 353 | 新增并已 merged `11:15:51Z` |

## 三、`REBASE-THEN-MERGE` 列被实测推翻

该列的前提是「head 携带未落地改动」。对六条 PR 用 `GET /compare/<base>...<head>` 测量：

| PR | status | ahead | files | `merge_base == head` |
|---:|---|---:|---:|---|
| 321 | behind | 0 | 0 | 是 |
| 322 | behind | 0 | 0 | 是 |
| 326 | behind | 0 | 0 | 是 |
| 327 | behind | 0 | 0 | 是 |
| 334 | behind | 0 | 0 | 是 |
| 335 | behind | 0 | 0 | 是 |

`merge_base == head` 且 `ahead == 0` = PR diff 为空，内容已在各自 base 分支历史中。**不存在 rebase 的对象**。正确处置为 `CONVERGED-EMPTY`。

补充实测：对这三条 base 分支（`remediation/…` / `session-h-bmcp-protocol` / `session-g-memory-context`）做 `git merge --no-commit --no-ff` 试合并到 main，冲突文件数分别为 11 / 2 / 2，且全部为 `[2,3]` 阶段（双方各自新增、无共同祖先），main 侧文档版本普遍更新更大。**整支合并会以旧版覆盖 main 新版，不可采用。**

## 四、唯一剩余项 PR #330

| 项 | 值 |
|---|---|
| state | open, draft=true |
| `mergeable` / `mergeable_state` | **false / `dirty`** |
| vs main | diverged, ahead 35, behind 59 |
| changed_files | 8（+423 −10） |

`dirty` 成因已定位：仅 `INDEX.md` 一处冲突，`AID-2026-008` 行的 `accountable Owner` 字段——main 侧 `USER-PRINCIPAL-DELEGATED`，PR 分支侧 `NOT_ASSIGNED`（陈旧）；PR 分支另新增 `AID-2026-015` 行。属确定性可解冲突，非语义冲突。

**L0 未合并、未改写该分支**，理由：PR 自述 `NOT_GRANTED — Owner-directed adoption pending`，且改动含 `AI-EXEC-003` 与全局提示词，须独立审查。详见 PR #330 评论 `7038694481`。

## 五、AID-2026-028 的九项跟踪结果对照

| # | 正文跟踪项 | 状态 |
|---:|---|---|
| 1 | 320/328/331/340 body declarations | 320/328/331 merged；340 已由 #341+#342 取代 |
| 2 | 六个陈旧 head rebase 并本地验证 | **前提不成立**（六条皆空 PR，无需 rebase），已合并 |
| 3 | 323/330 冲突/历史决策记录 | 323 merged；330 已记录冲突定位，待其持有会话 rebase |
| 4 | 332/333/339 登记为已合并 | **完成** |
| 5 | 338 用实际本地执行证据验证 | merged |
| 6 | 337 补英文对应并审查 | merged |
| 7 | G6 语义等价独立审查 | 未开始（需独立合格审查） |
| 8 | 重测 open-PR 数；冻结待单独决定 | **已重测 = 1**；L0 不宣布解冻 |
| 9 | G8 与架构验收独立跟踪 | 已建仓库内载体 `g8-seven-conditions-evidence-map.md` |

## 六、授权边界不变

本文件**不**授予：直接写 `main`、新建 PR/Issue、合并授权、生产激活、架构验收、配额解冻。AID-2026-028 的 drain-under-freeze 纪律与「no merge authority」表述继续有效。

open PR = 1 已低于解冻阈值 6，但解冻须由协调器按 SOP 单独宣布，本文件只提供测量依据。

## 七、复现

```
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=open
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/330
GET /repos/oahcom/AiMemoryBrainArchitecture/compare/<base>...<head>
```

判空条件：`compare.merge_base_commit.sha == head.sha` 且 `ahead_by == 0`。

---

**记录边界：** 本文件为执行状态测量，不修改 AID-2026-028 的裁定原则与授权边界。
