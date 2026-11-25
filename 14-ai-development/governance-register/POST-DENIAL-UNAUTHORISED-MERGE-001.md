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
      last_verification_note: "Every field in section 2 was read from the GitHub REST API in this session, and the endpoint is named beside each value. The one non-platform timestamp (the ruling's persistence time) is labelled as a local file modification time and is not used to order the two events; section 4 explains why the finding does not depend on it."
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

# POST-DENIAL-UNAUTHORISED-MERGE-001 — #946 在明确拒绝之后被合并

**事件类型：** 治理控制失效，不是普通的审批缺失记录。

**结论：** PR #946 的实现内容经技术验收通过并被保留；其合并行为未经授权，且发生在一条点名该 PR 的拒绝裁定之后。两者必须分开记录：内容正确不使合并获得追认，合并未经授权也不使内容失效。

---

## 1. 为什么这条记录单独存在

`GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.1–§3.5 记录了六次零正式 Review 合并。那六条的共同点是**顺序无法判定**：合并先发生，或同日而无法从平台字段判断先后。该登记因此只写「合并时零正式 Review」，不写「违反裁定后合并」。

本事件不属于该序列。拒绝已经存在、已经落盘、并且**点名了被合并的那个 PR**。把这种情况并入「顺序不明」会抹掉唯一的区别，所以单独立卷。

---

## 2. 平台字段

| 项目 | 端点 | 字段 | 返回值 |
|---|---|---|---|
| 合并时间 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946` | `merged_at` | `2026-11-24T14:05:56Z` |
| 合并账号 | 同上 | `merged_by.login` | `oahcom` |
| 合并提交 | 同上 | `merge_commit_sha` | `8e489ec1e18cd127088a695fa21121521e240514` |
| 正式 Review | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/reviews` | 数组长度 | `0` |
| Review 评论 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/comments` | 数组长度 | `0` |
| 提交数 / 增 / 删 | `pulls/946` | `commits` / `additions` / `deletions` | `10` / `547` / `7` |
| 合并时 head | `pulls/946` | `head.sha` | `600a562fbc52afc91ed0c7fcdadf684f9961e6c8` |
| PR 标题 | `pulls/946` | `title` | feat(hygiene): admit the ten Owner-ruled A/B shapes, and nothing else |

## 3. 拒绝裁定

裁定文本对应该 PR 的原话：

> 保留 PR #946，不执行合并。

同一份裁定还写明：

> **本轮裁定的是准入政策，不是合并授权。**

裁定落盘时间：`2026-11-24T13:20:27Z`（本地文件修改时间，`21:20:27 +0800`）。

## 4. 本事件为何不依赖两个时钟相减

把「拒绝在合并前 45 分钟」写成结论会很省事，但那个 45 分钟是**本地文件修改时间减平台时间戳**得出的。`OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001` 明确规定本地 mtime 不是平台时间戳。用它会得到一个更强但违反溯源规则的断言。

本记录改用不依赖时钟的依据：

1. 拒绝文本**点名了 `#946` 这个编号**，而 `#946` 正是被合并的对象。文档与其所指对象之间的对应关系是内容层面的，不需要两个时钟比较。
2. 该文本在本会话中于合并前已被读取，并据此发出了指令（保留 PR、不合并、把 D3 记为关闭、落盘验收证据）。
3. 因此可以确定的是：**拒绝存在、针对该 PR、且在被合并之前已被本会话持有。** 不能确定的是平台侧裁定的生效时刻与合并时刻的精确先后，这一点本记录不主张。

换句话说：本记录主张的是「有一条点名该 PR 的拒绝」，不是「拒绝在平台上先于合并生效 45 分钟」。

## 5. 与授权状态的关系

| 对象 | 状态 |
|---|---|
| #946 的代码内容 | ACCEPTED / RETAINED |
| #946 的合并授权 | NOT AUTHORISED |
| 实际合并行为 | UNAUTHORISED MERGE |
| 合并后的 `main` | 保留现状，不回滚 |
| 历史审计记录 | 不得改写为正常合并 |

保留内容的理由：A/B 规则已通过技术验收，AC8 实测 83 准入 / 30 拒绝，AC9 闭合于 `74 + 4 + 19 + 16 = 113`，回滚会毁掉已验收的实现却不能修复审批机制。

不追认的理由：技术正确不等于授权。如果「内容对」可以推出「合并合法」，那么 D1 就变成了一条内容审查规则，而不是合并控制。

> The implementation was technically accepted, but its merge was explicitly not authorised. Subsequent incorporation into main does not constitute retrospective authorisation.

## 6. 不作出的判断

- **不判断操作者。** `oahcom` 是 GitHub 账号，不是自然人。不从 `merged_by.login` 推断身份、意图或责任。
- **不写成已证实的恶意绕过。** 平台记录能证明「未经授权的合并发生了」，不能证明动机。
- **不主张本会话未参与即等于清白。** 本会话对 #946 的写操作是：建 PR、推分支、提交文档。未调用合并接口。这是关于本会话行为的事实陈述，不是对他人指控的答辩。
- **不据此改写 `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.7 的冻结计数。**

## 7. 控制面实测（2026-11-24）

治理失效的根源不在这条记录，而在控制面本身。同日实测：

| 检查项 | 端点 | 结果 |
|---|---|---|
| `required_pull_request_reviews` | `GET /branches/main/protection` | **不存在** |
| `enforce_admins` | 同上 | `true` |
| `allow_force_pushes` | 同上 | `false` |
| `required_status_checks.strict` | 同上 | `true`，12 个 context |
| Rulesets | `GET /rulesets` | `[]` |
| Collaborators | `GET /collaborators` | 仅 `oahcom`（`push: true`） |
| `oahcom0831-design` 权限 | `GET /collaborators/oahcom0831-design/permission` | `read` |

三点后果，按实测而非推断：

1. **没有审批要求**，所以零 Review 合并不会被平台阻止，只会被事后记录。
2. **`read` 权限的账号无法提交正式 Approved Review**，所以即便打开 `required_pull_request_reviews`，也没有第二个身份能满足它。
3. **`enforce_admins: true`** 意味着任何新加的限制同样约束唯一的写权限账号；在第二名写权限身份存在之前打开审批要求，会把 `main` 冻结在一个无法自行解除的状态。

这三条合起来解释了为什么「文件写着禁止」没有变成「系统能够禁止」。

### 7.1 全历史普查：该要求从未被满足过一次

上表测的是控制面。本节测的是全部历史的结果，因为「最近有多少次合并跳过审查」比「审查是否曾经发生过」是更弱的问题。

**方法。** `GET /pulls?state=closed&per_page=100` 逐页取全 → 775 个已关闭 PR，其中 `merged_at` 非空的 662 个。随后对全部 662 个逐一取 `GET /pulls/{n}/reviews`——不是抽样，也不限于近期合并。0 次请求失败，因此每个合并 PR 都被计入。读取时刻 `2026-11-24T18:47Z`。

| 量 | 值 |
|---|---|
| 枚举到的已关闭 PR | 775 |
| 已合并 PR（`merged_at` 非空） | 662 |
| 实际测量到的合并 PR（0 失败） | 662 |
| 至少有一个 review 对象的合并 PR | 106 |
| 完全没有 review 对象的合并 PR | 556 |
| 历史累计 review 对象数 | 170 |
| 这 170 个对象的状态分布 | `{COMMENTED: 170}` |
| **状态为 `APPROVED` 的 review 对象** | **0** |
| 产生过 review 对象的账号 | `oahcom`（170 / 170） |

**计数会增长，不变量不动。** 上表是 `2026-11-24T18:47Z` 的快照。合并仍在继续：`2026-11-24T20:35Z` 复测时为 676 个已合并 PR，自普查以来新增的 14 个全部不带任何 review 对象。因此「已合并数」每次读取都会变，而 `APPROVED = 0` 一次也没变过。上表因此标注测量时刻，本记录中的任何数字都不应在脱离该时刻的情况下被引用。

**独立于该枚举的交叉验证。** `GET /search/issues?q=repo:oahcom/AiMemoryBrainArchitecture+review:approved+is:pr` 返回 `total_count: 0`；加上 `is:merged` 限定后同样返回 `0`。不同端点、不同索引，同一答案。

**这确立了什么。** 不是「七次合并跳过审查」，也不是「执行最近失效」。状态是：在 662 个合并 PR 中，记录里**根本没有任何正式批准**——现存每一个 review 对象都是 `COMMENTED` 状态，而 D1 明确把它排除在批准之外，且这 170 个全部由撰写这些 PR 的同一个账号发出。D1 在本仓库任何时期都从未被满足过。

**这不确立什么。** 它不表明没有人看过代码，也不指认任何人的意图。`COMMENTED` 状态的 review 对象是真实的审查活动；它不是 D1 所要求的那个记录。这一发现是关于记录的，以及关于一个从未被配置成能产出该记录的控制面（`required_pull_request_reviews` 不存在，见 §7）。

**为什么本文不使用「七次」这个计数。** 本记录的早期草稿统计的是冻结之后的一个子集。子集计数容易引导出「问题有限且近期」的读法。普查既不有限也不近期，因此以普查为准。

---

## 8. 关联记录

- `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.5 — 同事件的合并形式记录。
- `OWNER-DECISION-REVIEW-INDEPENDENCE-001` — D1 的政策依据与 690 个 PR 的全量测量。
- `EX-20261123-01` — 唯一一条已登记的例外记录。
- `AID-2026-057` — 被合并实现的工作项，含 AC8/AC9 验收证据。
