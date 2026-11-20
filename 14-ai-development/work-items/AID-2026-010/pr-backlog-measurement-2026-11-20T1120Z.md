# PR 积压收敛实测记录（L0，2026-11-20T11:20Z）

本文件由 L0 协调层测量填写。它只记录测量事实与复现方法，**不构成**对任何 PR 处置、配额状态或验收结论的裁定。是否据此改变冻结线、解冻阈值或 F-43-01/F-43-02 状态，由 A 与相应 Owner 裁定。

## 一、收敛结果

测量时点：`2026-11-20T11:20Z`。

| 指标 | 收敛前（`pr-backlog-convergence-plan.md` 落库时） | 实测当前 |
|---|---|---|
| open PR 数 | 17 → 9 | **1** |
| 已合并（本轮） | — | 8 |
| `main` HEAD | `5972a1d2…` → `3bc51c61…` | **`94cbb4db…`** |

## 二、17 条受跟踪 PR 的终态

| PR | 终态 | 合并时间（UTC） | 备注 |
|---:|---|---|---|
| 320 | merged | 2026-11-20T08:13:21Z | |
| 321 | merged | 2026-11-20T11:07:05Z | 空 PR（见第三节） |
| 322 | merged | 2026-11-20T11:09:09Z | 空 PR |
| 323 | merged | 2026-11-20T11:15:03Z | 空 PR |
| 326 | merged | 2026-11-20T11:07:39Z | 空 PR |
| 327 | merged | 2026-11-20T11:07:31Z | 空 PR |
| 328 | merged | 2026-11-20T08:14:47Z | |
| 330 | **open（draft）** | — | 唯一未收敛项，见第四节 |
| 331 | merged | 2026-11-20T08:13:28Z | |
| 332 | merged | 2026-11-20T08:43:53Z | |
| 333 | merged | 2026-11-20T09:50:53Z | |
| 334 | merged | 2026-11-20T11:09:31Z | 空 PR |
| 335 | merged | 2026-11-20T11:09:39Z | 空 PR |
| 337 | merged | 2026-11-20T08:48:38Z | |
| 338 | merged | （早于本轮） | |
| 339 | merged | 2026-11-20T08:38:15Z | |
| 340 | closed / 未合并 | — | 由 #341 + #342 取代 |
| 353 | merged | 2026-11-20T11:15:51Z | 计划外新增，已收敛 |

## 三、关键实测：7 个 PR 是空 PR

收敛计划将 321/322/323/326/327/334/335 判为 `REBASE-THEN-MERGE`，前提是它们携带未落地的改动。**该前提经实测不成立。**

对每条 PR 用 `GET /compare/<base>...<head>` 测量：

| PR | base | status | ahead | behind | files | `merge_base == head` |
|---:|---|---|---:|---:|---:|---|
| 321 | `remediation/…-2026-11-18` | behind | 0 | 144 | 0 | **是** |
| 322 | `session-h-bmcp-protocol` | behind | 0 | 4 | 0 | **是** |
| 323 | `remediation/…-2026-11-18` | behind | 0 | 33 | 0 | **是** |
| 326 | `session-g-memory-context` | behind | 0 | 3 | 0 | **是** |
| 327 | `remediation/…-2026-11-18` | behind | 0 | 131 | 0 | **是** |
| 334 | `session-h-bmcp-protocol` | behind | 0 | 8 | 0 | **是** |
| 335 | `session-g-memory-context` | behind | 0 | 3 | 0 | **是** |

`merge_base == head` 且 `ahead == 0` 意味着 head 的全部提交都已在 base 分支历史中，PR 的 diff 为空。**这 7 条 PR 无任何未落地内容，不存在 rebase 的对象。**

因此这 7 条的正确处置是 **`CONVERGED-EMPTY`**，而非 `REBASE-THEN-MERGE`。计划的处置列在这一点上被实测推翻。

## 四、唯一剩余项 PR 330

| 项 | 值 |
|---|---|
| title | `docs(ai-exec-003): add execution-first AI development baseline` |
| base / head | `main` / `ai/AID-2026-011/IO-execution-first-baseline` |
| draft | true |
| changed_files | 8（+423 −10） |
| `mergeable` | **false** |
| `mergeable_state` | **`dirty`** |
| vs main | diverged, ahead 35, behind 59 |

`dirty` 表示存在冲突，需要先解决冲突或 rebase 才能合并。它是 draft，且改动集中在 `14-ai-development/AI-EXEC-003.md`、`prompts/global-project-developer*.md` 等基线文件，属治理基线变更，**不是 L0 可以自行合并的对象**。

## 五、对冻结线的影响（仅陈述，不裁定）

- 冻结线：open PR ≤ 10。
- 解冻阈值：open PR ≤ 6。
- 实测 open PR = 1，**已低于解冻阈值**。

L0 不宣布解冻。解冻由协调器按 SOP 宣布；本记录只提供触发解冻所需的测量依据。

## 六、复现方法

```
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=open&per_page=100
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/<n>
GET /repos/oahcom/AiMemoryBrainArchitecture/compare/<base>...<head>
GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main
```

判空条件：`compare.merge_base_commit.sha == head.sha` 且 `compare.ahead_by == 0`。

## 七、记录边界

本记录只提交测量事实与复现步骤。据以改变冻结线、宣布解冻、合并 PR 330、或调整 F-43-01/F-43-02 状态，均超出 L0 职责，须由 A 与相应 Owner 裁定。
