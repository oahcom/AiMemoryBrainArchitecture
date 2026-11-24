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

### 3.1 后续实例（二）：PR #890

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/890/reviews` → `[]`。

> Post-freeze observed instances: PR #890 — 2026-11-24 — 0 formal reviews.

核查证据（新增本条目时逐项读取，未沿用任何其他登记簿的数字）：

| 项目 | 端点 | 字段 | 返回值 |
|---|---|---|---|
| 正式 Review 记录 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/890/reviews` | 数组长度 | `0` 条 |
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
| 合并时间 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/927` | `merged_at` | `2026-11-24T10:38:00Z` |
| 合并账号 | 同上 | `merged_by.login` | `oahcom` |
| 合并提交 | 同上 | `merge_commit_sha` | `b3a65e54b0b0380430cc4cf8b187d3e0c9edb7a3` |
| 提交数 / 增 / 删 | 同上 | `commits` / `additions` / `deletions` | `2` / `462` / `0` |
| 合并时的 head | 同上 | `head.sha` | `5e0a93d6301a7b04b1ee5e1a3031ece1068c1dfa` |

适用与 §3.2 相同的边界：D1 在本次合并之前已生效，因此合并时的正式 Review 要求存在而未被满足；本记录不据此推断具体操作者，也不把「本会话未签发合并授权」写成「有人违反了授权」。本会话对该 PR 的处理是：提交内容审查请求，未调用合并接口。

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
