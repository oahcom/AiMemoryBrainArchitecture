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
      last_verification_note: "Every SHA, parent count, timestamp and API response body in this record was read from the GitHub REST API or from git in this session. No figure is carried over from another register. The record states one limit explicitly: the evidence cannot establish why the merged commit's shape differs from the requested merge_method."
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
    en: null
    zh-CN: null
---
# GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031 — PR #875 以 squash 形态落地，而请求的是 merge commit

**状态**：`OPEN` / `RECORDED`
**缺陷类别**：Governance Conformance — 合并结果验证不足
**严重度**：Low（内容无偏差；提交图形状与请求不一致）
**测量时点**：`main = a8c367d`
**关联**：`GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.4（本次偏差记录的正文对象不是 §13.4 的历史更正，该更正保持原样不动）

---

## 0. 一句话

PR #875 的内容按批准落地，但落地形态与我请求的合并方式不一致，而我在发出合并请求之前没有确认实际提交形态。**这是操作侧的验证缺陷，不是内容缺陷。** 本记录不撤销内容，只把形态偏差留成可审计事实。

---

## 1. 偏差陈述（Owner 指定措辞，逐字）

> 请求指定 `merge_method=merge`，但最终观察到的合并提交为单父 squash 形态。该提交在合并 API 请求前已经存在于 main；API 请求随后返回相同 SHA。请求与最终提交形态不一致，且请求与提交产生之间的因果关系无法由现有证据确立。操作者未在请求前确认实际提交形态，属于合并结果验证不足。

本条措辞的三项边界，均不得被后续引用时放宽：

1. **不声称 GitHub 忽略了 `merge_method`。** 仓库三种合并方式全部开启（`allow_merge_commit: true`、`allow_squash_merge: true`、`allow_rebase_merge: true`），API 没有任何理由推翻请求，但也没有证据表明它推翻了请求。
2. **不声称该 PUT 创建了该提交。** 请求返回的 SHA 在请求发出前已是 `main` 的 tip。
3. **不猜测另一个触发合并的主体。** 所有相关事件在 API 中都记为 `oahcom`，无法区分人工点击与自动化动作。无法区分就记为无法区分。

---

## 2. 实测证据

### 2.1 请求参数

```
PUT /repos/oahcom/AiMemoryBrainArchitecture/pulls/875/merge
{"merge_method":"merge","sha":"c10ebdc4663bca289d64826883f4723664180d52"}
```

### 2.2 API 返回值

```
第一次： 422  "11 of 11 required status checks are expected."
第二次： 422  "Head branch was modified. Review and try the merge again."
第三次： 200  {"merged": true, "sha": "a8c367def34e5a3082ab777a7afedf7e82f38aa0",
                "message": "Pull Request successfully merged"}
```

### 2.3 落地提交的形态

```
git rev-list --parents -n 1 a8c367d
a8c367def34e5a3082ab777a7afedf7e82f38aa0 8dada462b53ba6fd24e5775dcc761fc3528288c2
                                       ^ 单父 —— squash，不是双父 merge commit

subject: docs(register): record the #707 review-source correction in §13.4
```

### 2.4 关键时序（`issues/875/timeline` 与 `pulls/875` 原始返回）

| 时间（UTC） | 事件 | 主体 | 对象 |
|---|---|---|---|
| 2026-11-24T04:36:28Z | `head_ref_force_pushed` | oahcom | 我的 rebase，`cfe0e7d → 340167c` |
| 2026-11-24T04:43:58Z | `head_ref_force_pushed` | oahcom | 我的 rebase，`c1d5381 → 340167c` 线 |
| — | `committed` | — | `340167c` |
| — | `committed` | — | `4b64dcb`（GitHub Update branch，非我创建） |
| — | `committed` | — | `c10ebdc`（GitHub Update branch，非我创建） |
| 2026-11-24T04:54:07Z | `merged` | oahcom | `a8c367d` |
| 2026-11-24T04:54:07Z | `closed` | oahcom | — |

`a8c367d` 在我发出第三次 PUT 之前已经是 `main` 的 tip，这是我判定「因果关系无法确立」的直接依据。

### 2.5 内容未受影响

| 检查项 | 结果 |
|---|---|
| `GOV-NC-…-003.md` sha256 at `main` | `2cd88b58b29c9080be52c41f49db99aa7544fa76bcb0cafff25adca188a9a1d1` |
| `GOV-NC-…-003.en.md` sha256 at `main` | `ca43112043a3944bb9e3f39b1323ddd39c9a2c823c756a8636222053854b77c7` |
| `diff 8dada46..a8c367d` | `53 0` / `53 0`，无删除 |
| 批准时的同一对 sha256（`c1d5381`、`340167c`、`4b64dcb`、`c10ebdc`） | 逐一相同 |

结论：内容与被批准的内容逐字节相同；偏差只存在于提交图形状与请求形态之间。

---

## 3. 零正式 Review 实例的后续记录

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/875/reviews` → `[]`。

按 Owner 裁定：

> Post-freeze observed instances: PR #875 — 2026-11-24 — 0 formal reviews.

**不得回写或扩大 `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.7 已冻结的历史计数。** 冻结计数代表其原本定义的历史观察范围；把后续实例追加入原数字会改变统计口径与历史基线。本记录只在其后另列一句，不动原数字。

### 3.0 三个端点，三种不同的东西

本节每一张表都在问同一个问题：这次合并有没有被审查过。用错端点会得到一个看起来像证据的常量，所以先把三个端点各自度量什么写清楚：

| 端点 | 度量的是 | 不含什么 |
|---|---|---|
| `GET /pulls/{n}/reviews` | **正式提交的 Review**——`APPROVE` / `REQUEST_CHANGES` / `COMMENT` 三种动作，占用 "Files changed" 审查面板 | 会话线程中的任何发言 |
| `GET /pulls/{n}/comments` | **行内 diff 评论**——挂在补丁某一行上的评论 | 会话线程、正式 Review 状态 |
| `GET /issues/{n}/comments` | **会话线程**——PR 讨论区按时间排列的发言 | 正式 Review 状态、行内评论 |

两个 `0` 并排出现会读起来像互相印证，实际可能只是同一种缺席被数了两次——`#966` 证明这两条在本仓库里恰好就是这种情况。因此下文六个实例三个端点都测，并把「正式 Review」与「会话线程中的审查」分开记，不再合并成一个 `0`。

### 3.1 后续实例（二）：PR #890

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/890/reviews` → `[]`。

> Post-freeze observed instances: PR #890 — 2026-11-24 — 0 formal reviews.

核查证据（新增本条目时逐项读取，未沿用任何其他登记簿的数字）：

| 项目 | 端点 | 字段 | 返回值 |
|---|---|---|---|
| 正式 Review 记录 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/890/reviews` | 数组长度 | `0` 条 |
| 会话评论数 | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/890/comments` | 数组长度 | `0` 条 |
| 合并时间 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/890` | `merged_at` | `2026-11-24T05:39:10Z` |
| 合并账号 | 同上 | `merged_by.login` | `oahcom` |
| 合并提交 | 同上 | `merge_commit_sha` | `0f32d46c34cb086e52de38fa49b33ca8a3bf5cd3` |
| 行内 review 评论数 | 同上 | `review_comments` | `0` |
| 提交数 / 增 / 删 | 同上 | `commits` / `additions` / `deletions` | `1` / `306` / `0` |
| 标题 | 同上 | `title` | `docs(register): record the #875 merge-form deviation` |

时间关系按来源分别标注，不混用：

| 事件 | 时间 | 时间来源 |
|---|---|---|
| 本会话作出「不签发合并授权」的裁定 | 不晚于 `2026-11-24T05:36:33Z`（`13:36:33 +0800`） | 裁定文本落盘文件的本地修改时间。**这不是**平台签发的时间戳，只用于说明本会话内部的先后顺序，不用于证明合并行为本身。 |
| #890 合并 | `2026-11-24T05:39:10Z` | GitHub REST API `merged_at` |

两者相隔不超过 2 分 37 秒。此处只用时间说明先后，不用一个事件的时间去证明另一个事件的发生或不发生。

本记录陈述的事实：**#890 是在本会话已明确不签发合并授权之后被合并的，且合并时零正式 Review。** 这是已记录在案的治理控制失效，不只是尚未强制执行的策略。

本记录不陈述的事实：不把 `merged_by: oahcom` 归属到某个具体自然人。该字段标识的是一个 GitHub 账号，不必然是操作该账号的人。

### 3.2 后续实例（三）：PR #896

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/896/reviews` → `[]`。

> Post-freeze observed instances: PR #896 — 2026-11-24 — 0 formal reviews.

| 项目 | 端点 | 字段 | 返回值 |
|---|---|---|---|
| 正式 Review 记录 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/896/reviews` | 数组长度 | `0` 条 |
| 会话评论数 | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/896/comments` | 数组长度 | `0` 条 |
| 合并时间 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/896` | `merged_at` | `2026-11-24T06:51:52Z` |
| 合并账号 | 同上 | `merged_by.login` | `oahcom` |
| 合并提交 | 同上 | `merge_commit_sha` | `84bbe9241aef748b406a969da321e7d3fcda2dc1` |
| 提交数 / 增 / 删 | 同上 | `commits` / `additions` / `deletions` | `1` / `335` / `1` |
| 合并时的 head | 同上 | `head.sha` | `5585d95ffd5705fe7a636f475b295162737585e9` |

**本条只记录一项可测量的状态，不记录因果或归责：**

- 可确证：合并时该 PR 的正式 Review 记录为 `0` 条。`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/896/reviews` 返回 `[]`。

**一个必须分开的两件事：事件时间与规范生效时间。** 早先草稿在此处写「D1 所要求的内容在该时刻并不存在」，这是错的，已更正。正确的陈述是：

> PR #896 在 `2026-11-24T06:51:52Z` 合并，正式 Review API 返回 `[]`。该合并早于 Round 22 针对 #896 的拒绝授权文本持久化，因此不能认定为违反该项 Round 22 拒绝授权。但 D1 的正式 Review 要求已在 Round 20 作出；本次零 Review 合并仍与该既有要求不一致。现有证据不支持对具体操作者作进一步归因。

即：**D1 在合并之前就已经生效，所以合并时的要求存在，只是未被满足。** 不能说「要求在当时不存在」。也不能因此把该合并倒推成违反 Round 22 的那项拒绝授权——那项文本当时尚未落盘。两个时间边界都要保留。

- 不可确证：该合并与任何一次裁定的先后关系。本会话记录 #896 裁定的文本落盘时间为 `2026-11-24T06:53:07Z`（`14:53:07 +0800`，同为本地文件修改时间，非平台时间戳），晚于合并时间 `2026-11-24T06:51:52Z` 约 75 秒。

因此本条**不写**「违反裁定后合并」之类的表述。把先后顺序未知的事件写成违序，会与 `OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001` 直接冲突。此处只登记一个事实：**在 D1 已被确立之后，又发生了一次合并时零正式 Review 的合并。** 本次合并是否构成对某一次具体裁定的违反，需要平台侧事件序列才能回答，本记录不作判断。

### 3.3 后续实例（四）：PR #927

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/927/reviews` → `[]`。

> Post-freeze observed instances: PR #927 — 2026-11-24 — 0 formal reviews.

| 项目 | 端点 | 字段 | 返回值 |
|---|---|---|---|
| 正式 Review 记录 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/927/reviews` | 数组长度 | `0` 条 |
| 会话评论数 | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/927/comments` | 数组长度 | `1` 条 |
| 合并时间 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/927` | `merged_at` | `2026-11-24T10:38:00Z` |
| 合并账号 | 同上 | `merged_by.login` | `oahcom` |
| 合并提交 | 同上 | `merge_commit_sha` | `b3a65e54b0b0380430cc4cf8b187d3e0c9edb7a3` |
| 提交数 / 增 / 删 | 同上 | `commits` / `additions` / `deletions` | `2` / `462` / `0` |
| 合并时的 head | 同上 | `head.sha` | `5e0a93d6301a7b04b1ee5e1a3031ece1068c1dfa` |

适用与 §3.2 相同的边界：D1 在本次合并之前已生效，因此合并时的正式 Review 要求存在而未被满足；本记录不据此推断具体操作者，也不把「本会话未签发合并授权」写成「有人违反了授权」。本会话对该 PR 的处理是：提交内容审查请求，未调用合并接口。

**会话线程里有一条合并之后的审查。** `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/927/comments` → `1` 条，`created_at` 为 `2026-11-24T11:16:18Z`，比 `merged_at` `10:38:00Z` 晚 38 分钟，首行是 `## Ruling 86 — #927's classification reconciles exactly; the manifest is sound and should merge`。

因此本实例的准确表述不是「零审查」，而是 **`0` 条正式 Review，`1` 条合并后审查**。两个时间戳都出自同一个 API（`issues/{n}/comments.created_at` 与 `pulls/{n}.merged_at`），所以这个 `+38` 不需要任何本地时钟参与，`OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001` 所禁止的「本地 mtime 减平台时间戳」在这里不适用。这条审查写在合并之后，它没有、也不可能在合并之前拦住合并。

### 3.4 后续实例（五）：PR #933

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/933/reviews` → `[]`。

> Post-freeze observed instances: PR #933 — 2026-11-24 — 0 formal reviews.

| 项目 | 端点 | 字段 | 返回值 |
|---|---|---|---|
| 正式 Review 记录 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/933/reviews` | 数组长度 | `0` 条 |
| 会话评论数 | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/933/comments` | 数组长度 | `0` 条 |
| 合并时间 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/933` | `merged_at` | `2026-11-24T11:34:23Z` |
| 合并账号 | 同上 | `merged_by.login` | `oahcom` |
| 合并提交 | 同上 | `merge_commit_sha` | `3235db07f23cb272da7460147e2f80413e68e555` |
| 提交数 / 增 / 删 | 同上 | `commits` / `additions` / `deletions` | `2` / `143` / `1` |
| 合并时的 head | 同上 | `head.sha` | `4f4669fb7a81a09a15c6d91e590d9832e4d615bf` |

适用与 §3.2 相同的边界，不作操作者推断。

### 3.5 后续实例（六）：PR #946 — 合并时已存在明确的拒绝

前五个实例的共同点是**顺序不明**：合并先发生，或与裁定同日而无法从平台字段判定先后。本节不同，因此单独成节而不是并入上表。

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/reviews` → `[]`。

> Post-freeze observed instances: PR #946 — 2026-11-24 — 0 formal reviews.

| 项目 | 端点 | 字段 | 返回值 |
|---|---|---|---|
| 正式 Review 记录 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/reviews` | 数组长度 | `0` 条 |
| Review 评论数 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/comments` | 数组长度 | `0` 条 |
| 会话评论数 | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/946/comments` | 数组长度 | `1` 条 |
| 合并时间 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946` | `merged_at` | `2026-11-24T14:05:56Z` |
| 合并账号 | 同上 | `merged_by.login` | `oahcom` |
| 合并提交 | 同上 | `merge_commit_sha` | `8e489ec1e18cd127088a695fa21121521e240514` |
| 提交数 / 增 / 删 | 同上 | `commits` / `additions` / `deletions` | `10` / `547` / `7` |
| 合并时的 head | 同上 | `head.sha` | `600a562fbc52afc91ed0c7fcdadf684f9961e6c8` |

**为什么这一条与前五条不是同一类。** 拒绝合并授权的裁定文本，其落盘时间（本地文件修改时间，`2026-11-24T13:20:27Z`，即 `21:20:27 +0800`）早于合并时间 `14:05:56Z` 约 45 分钟。也就是说，这不是「合并先于裁定」，而是**裁定已经存在、已经落盘、且明确写着不合并，合并仍然发生**。

这里必须把两种时间分开，否则会写出一个更强的断言而非更准确的断言：

| 时间 | 来源 | 值 | 能证明什么 |
|---|---|---|---|
| 裁定落盘 | 本地文件修改时间 | `2026-11-24T13:20:27Z` | 本会话在其后仍持有该文本；不是平台时间戳 |
| 合并 | `pulls/946.merged_at` | `2026-11-24T14:05:56Z` | GitHub 记录的合并时刻 |

本地文件修改时间不是平台时间戳（见 `OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001`），所以上表不能单独证明「裁定在平台侧先于合并生效」。但本节所依据的不是两个时间戳的差值，而是**裁定内容本身引用被合并的那个 PR 编号**、且该文本在本会话中于合并前已被读取并据此发出过指令：`保留 PR #946，不执行合并。` 这是一个内容层面的对应关系，不依赖时钟。

本会话对 #946 的处理：创建 PR、推送分支、提交文档，**未调用合并接口**。`oahcom` 只能记为 GitHub 账号，不据此认定具体操作人。与前五条一样，本记录不判断谁触发了合并。

**合并之后 90 分钟，同一 PR 的会话线程里出现了一条批准。** `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/946/comments` → `1` 条，`created_at` 为 `2026-11-24T15:36:10Z`，比合并时间 `14:05:56Z` 晚 90 分钟，首行是 `## Owner review — approved. The arithmetic reconciles, and the mutation is a genuine bound`。

这条批准不在 `pulls/946/reviews` 里：它不是正式 Review 提交，是会话线程里的一次发言。两个时间都是平台时间戳，因此 `+90` 分钟不需要本地时钟参与。

**它不撤回本节的拒绝结论，两者并列。** 一条在合并完成 90 分钟之后写下的「approved / Merge it」是对已经发生的合并的**追认**，不是对它的**许可**——它没有、也不可能在合并之前拦住合并。因此本节的事实是两条而不是一条：

1. 合并时已有明确拒绝（上文，内容层面可确证）。
2. 合并后 90 分钟出现追认性批准（本段，平台时间戳可确证）。

把第 2 条写成对第 1 条的缓解，就会把「合并发生在明确拒绝之后」悄悄换读成「后来有人批准了」。第 2 条既不减轻也不加重；它只是让「零 Review」这个说法不再准确。准确的说法是：**`0` 条正式 Review，`1` 条合并后追认。**

### 3.6 序列汇总（不改写 §13.7 冻结计数）

| 序 | PR | 合并时间（UTC） | 正式 Review | 会话线程 | 与前序的差别 |
|---|---|---|---:|---|---|
| 一 | #875 | `2026-11-24T04:54:07Z` | 0 | 0 | 形态偏差，内容已批准 |
| 二 | #890 | `2026-11-24T05:39:10Z` | 0 | 0 | 顺序不明 |
| 三 | #896 | `2026-11-24T06:51:52Z` | 0 | 0 | 顺序不明（裁定晚于合并 75 秒） |
| 四 | #927 | `2026-11-24T10:38:00Z` | 0 | 1（合并后 +38 分钟） | 顺序不明 |
| 五 | #933 | `2026-11-24T11:34:23Z` | 0 | 0 | 顺序不明 |
| 六 | #946 | `2026-11-24T14:05:56Z` | 0 | 1（合并后 +90 分钟） | **合并时已有明确拒绝** |

`GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.7 的冻结计数保持原值，不因本表追加而改变。本表只是一个后续观察清单，不是对原统计口径的修订。新增的「会话线程」列同样不改变它：那一列扩大的是**观察实例的维度**，不是历史统计的基数。

---

## 4. 明确不作出的判断

- 不判断合并动作由谁触发，或是否存在多个主体。
- 不判断 GitHub 是否本应执行 merge commit。
- 不把 squash 形态本身当作治理缺陷。单父提交降低了可回溯性，但内容与批准一致；把它写成内容缺陷会是另一类不实陈述。
- 不声称本记录构成对 #875 的重新审批，也不改变任何既有审批状态。
- 不为本偏差追溯性地请求豁免。

---

## 5. 可操作的教训（仅此一条）

在合并请求返回成功之后，应核对**落地提交的父提交数量与 subject**，而不仅是 HTTP 状态与 `merged: true`。本次未做该核对，因此「合并成功」被当成了「按请求方式合并成功」。两者不是同一个断言。此教训适用于任何以指定 `merge_method` 发起的合并。
