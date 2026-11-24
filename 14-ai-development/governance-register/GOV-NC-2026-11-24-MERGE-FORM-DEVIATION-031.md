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
