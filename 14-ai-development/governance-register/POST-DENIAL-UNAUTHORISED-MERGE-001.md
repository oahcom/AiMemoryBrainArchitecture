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
| `required_status_checks.strict` | 同上 | `true`，12 个 context（2026-11-24 实读；2026-11-25T02:52Z 复读为 16 项，多出四项：`Session Evidence`、其两个 self-test 上下文与 `rust-workspace-test`） |
| Rulesets | `GET /rulesets` | `[]` |
| Collaborators | `GET /collaborators` | 仅 `oahcom`（`push: true`） |
| `oahcom0831-design` 权限 | `GET /collaborators/oahcom0831-design/permission` | `read` |

三点后果，按实测而非推断：

1. **没有审批要求**，所以零 Review 合并不会被平台阻止，只会被事后记录。
2. **`read` 权限的账号无法提交正式 Approved Review**，所以即便打开 `required_pull_request_reviews`，也没有第二个身份能满足它。
3. **`enforce_admins: true`** 意味着任何新加的限制同样约束唯一的写权限账号；在第二名写权限身份存在之前打开审批要求，会把 `main` 冻结在一个无法自行解除的状态。

这三条合起来解释了为什么「文件写着禁止」没有变成「系统能够禁止」。

### 7.1 全历史普查：556 次合并里连一个 review 对象都没有

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

**这确立了什么。** 不是「七次合并跳过审查」，也不是「执行最近失效」。真正的发现是两个数字：在 662 个合并 PR 中，**556 个连一个 review 对象都没有**——不是「没有批准」，而是审查提交这条路径一次也没有被走过；另有 106 个有过 review 对象，共 170 条，全部是 `COMMENTED`。审查在形式上存在过 106 次，在 556 次合并里连形式都没有。

**`APPROVED = 0` 不是与上面同层级的发现，本文把它从头条位置撤下。** `GET /collaborators` 返回 `["oahcom"]`，只有一名 collaborator；`GET /pulls?state=closed` 逐页取全得到的 795 个已关闭 PR，`user.login` 全部是 `oahcom`（795 / 795）。GitHub 不允许一个账号批准自己撰写的 PR，因此 `APPROVED` 的数量不是「目前为零」，而是**在这个账号拓扑下必然为零，对每一个 PR、永远如此，与任何人的行为无关**。把它当作治理测量的头条，等于报告一枚只有一面的硬币落地为正面：数字是真的，信息量是零。

由此 D1 的定性改变：不是 `ENFORCEMENT FAILURE`（那是行为缺陷，暗示改行为），而是 **`REQUIRED BUT UNSATISFIABLE BY CONSTRUCTION`**（这是规格缺陷，暗示改规则）。原来的措辞完整保留在 `AID-2026-055` 的 `status_history` 里，使这次更正可审计而不是被覆盖。可被表达的独立性见 §7.2。

> **这一条此后又被拆开（2026-11-25，`AID-2026-055`）。** `REQUIRED BUT UNSATISFIABLE BY CONSTRUCTION` 作为**单一状态**把要求与它取代的口径焊在了一起，照字面接受会得出「独立性本身在这里不可能」的结论。实际不可能的是账号级形式；会话级形式一直可用，只是从未被记录。现行做法是把两半分开记录在 `current_status_parts`（`D1-a` = 可满足、未满足；`D1-b` = 必然为零、且已不是要求），而 `current_status` 本身保持原样并由 #1059 的附注限定在账号层——因为一份改写自己断言的记录就不再是记录。上面这段保留原样，因为它是当时那次更正的记录，不是对现状的陈述。

**这不确立什么。** 它不表明没有人看过代码，也不指认任何人的意图。`COMMENTED` 状态的 review 对象是真实的审查活动；它不是 D1 所要求的那个记录。这一发现是关于记录的，以及关于一个从未被配置成能产出该记录的控制面（`required_pull_request_reviews` 不存在，见 §7）。

**为什么本文不使用「七次」这个计数。** 本记录的早期草稿统计的是冻结之后的一个子集。子集计数容易引导出「问题有限且近期」的读法。普查既不有限也不近期，因此以普查为准。

### 7.2 第三个端点：会话线程，以及「零 Review」这个说法本身不准确

§7.1 测的是 `pulls/{n}/reviews`。那只是三个端点中的一个，而且是本仓库里唯一一个「批准」在构造上必然为零的那个——它并不为空：它有 170 个 `COMMENTED` 对象，恒为零的是 `APPROVED`（自我批准被平台禁止）。三者度量的东西不同，混用会得到一个看起来像证据的常量：

| 端点 | 度量的是 | 不含什么 |
|---|---|---|
| `GET /pulls/{n}/reviews` | 正式提交的 Review（`APPROVE` / `REQUEST_CHANGES` / `COMMENT`） | 会话线程中的任何发言 |
| `GET /pulls/{n}/comments` | 行内 diff 评论 | 会话线程、正式 Review |
| `GET /issues/{n}/comments` | 会话线程（PR 讨论区按时间排列的发言） | 正式 Review 状态、行内评论 |

`#966` 证明这个区别不是术语洁癖。`GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.5 把 `pulls/946/reviews` 与 `pulls/946/comments` 的两个 `0` 并排列出，读起来像互相印证，实际是同一种缺席被数了两次。同一 PR 的 `issues/946/comments` 返回 `1` 条，`created_at` 为 `2026-11-24T15:36:10Z`，比合并时间 `14:05:56Z` 晚 90 分钟，首行是 `## Owner review — approved. The arithmetic reconciles, and the mutation is a genuine bound`。

**全历史第三端点测量。** 与 §7.1 同一枚举口径，读取时刻 `2026-11-25T00:36Z`：

| 量 | 值 |
|---|---|
| 枚举到的已关闭 PR | 795 |
| 已合并 PR（`merged_at` 非空） | 681 |
| 仓库全部会话评论（`GET /issues/comments` 逐页取全） | 4577 |
| 这些评论的作者分布 | `{oahcom: 4577}` |
| 至少有一条会话评论的合并 PR | 406 |
| 其中合并**之前**已有会话评论 | 317 |
| 其中合并**之后**仍有会话评论 | 232 |
| 正式 Review 对象（§7.1 口径，增补至 681 个合并 PR） | 170，全部 `COMMENTED`，全部由 `oahcom` 发出 |
| 状态为 `APPROVED` 的正式 Review 对象 | **0** |

**因此 §7.1 的措辞需要一处更正，而 D1 的结论不变。**（该定性本身已于 2026-11-25 拆为 D1-a / D1-b，见 §7.1 的注释；此处「不变」指 D1 仍然成立、未被豁免。）§7.1 只测正式 Review 端点，容易被读成「没有人看过代码」，而那是错的：406 个已合并 PR 有会话评论，317 个在合并之前就有。真正的状态更准确，也更难辩解：

> 审查活动是存在的，写下来的审查也是存在的：406 个已合并 PR 有会话评论，317 个在合并之前就有。但这 4577 条会话评论和 170 条 review 对象全部由同一个账号发出，而该账号同时是全部 795 个已关闭 PR 的作者，GitHub 也不允许它批准自己撰写的 PR。

所以问题不是「有没有人审查」，也不是「审查的人够不够格」，而是：**用「是否出现第二个 GitHub 账号」来定义独立性，是一个在本拓扑下无法被满足的规格缺陷。**

这不是把标准降低，而是把标准换成这个仓库能够表达的那一维。`#935` 已经给过答案：**独立性是审查会话的属性，不是 GitHub 账号的属性。** 因此 D1 必须改写成 GitHub 能表达的形式——一个由 check run 产出的 required status check，断言存在一个非作者的审查会话。状态检查不需要第二个账号，`#704` 把 doctest 变成门禁、`#965` 把会话证据变成门禁，用的都是同一条路径。

反过来必须写明：**`required_pull_request_reviews` 在这里永远无法被满足，不得添加。** 打开它不会让 `main` 更安全，只会让下一次合并尝试直接无法发生——它要求一个这个账号拓扑产生不出来的对象。本记录 §7 把它记为「不存在」是事实陈述，不是修复指令；把它读成修复指令的下一个会话会把仓库冻死。

**这不推翻 §3 的拒绝结论。** 合并后 90 分钟出现的追认性批准，是对已经发生的合并的追认，不是对它的许可；它既不减轻也不加重既有的拒绝事实。两者的并列关系见 `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.5。

**这不改变 §7.1 的冻结口径。** `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.7 的历史计数保持原值；本节扩大的是观察维度，不是统计基线。

---

## 8. 关联记录

- `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.5 — 同事件的合并形式记录。
- `OWNER-DECISION-REVIEW-INDEPENDENCE-001` — D1 的政策依据与 690 个 PR 的全量测量。
- `#966` — 对 `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3 的 Owner 裁定：三个端点语义不同，会话线程中的事后审查必须与正式 Review 分开记。§7.2 按该裁定增补。
- `EX-20261123-01` — 唯一一条已登记的例外记录。
- `AID-2026-057` — 被合并实现的工作项，含 AC8/AC9 验收证据。
