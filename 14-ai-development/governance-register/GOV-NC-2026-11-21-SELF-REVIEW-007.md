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
      last_verified_date: "2026-11-25"
      last_verification_note: "正文与全部计数均未改动。2026-11-25 增补的附注只撤回 §5 的一处推论与 §7 的一格代价，不新增测量，不改动任何数字。"
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
    source: null
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.md"
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-SELF-REVIEW-007.md"
---

# GOV-NC-2026-11-21-SELF-REVIEW-007 — 零审查合并的「修复」是同一账号自我审查

- 登记编号：GOV-NC-2026-11-21-SELF-REVIEW-007
- 状态：`ACCEPTED` / `SELF_REVIEW_IDENTIFIED` / S-2 `APPROVED_IN_PRINCIPLE / IDENTITY_NOT_ASSIGNED`
- 缺陷类别：Governance Conformance — Independence of Review
- 严重度：High
- 发现时间：2026-11-21T05:50Z
- 前置登记：GOV-NC-2026-11-20-MERGE-AFTER-RULING-003（零审查合并，计数冻结 4）
- 关联：PR-GOVERNANCE-001 §5（独立审查）、#403 评论中的 Owner 附带裁定、GOV-NC-2026-11-20-CI-NOT-EXECUTED-005

---

## 1. 结论先行

`MERGE-AFTER-RULING-003` 记录的四例「零审查合并」有一个共同特征：`reviews = 0`。这个特征**已经消失**。取而代之的是一个更差的形态：

**作者本人以 `COMMENTED` 状态提交审查，然后在 13–74 秒内合并自己。**

| PR | author | sole reviewer | merger | review → merge |
|---|---|---|---|---|
| #403 | `oahcom` | `oahcom` | `oahcom` | **15 s** |
| #404 | `oahcom` | `oahcom` | `oahcom` | **40 s** |
| #408 | `oahcom` | `oahcom` | `oahcom` | **74 s** |
| #409 | `oahcom` | `oahcom` | `oahcom` | **13 s** |
| #413 | `oahcom` | `oahcom` | `oahcom` | **24 s** |
| #414 | `oahcom` | `oahcom` | `oahcom` | **20 s**（第 2 条审查 → 合并） |

六例全部满足 `author == sole reviewer == merger`。

这不是「审查不足」，是**审查被填表化**。`reviews >= 1` 这个计数指标现在可以被单账号在十几秒内满足，而 §5 要求的独立性一分未增。

---

## 2. 为什么这不是 MERGE-AFTER-RULING-003 的重复

两个登记的失效模式不同，且新形态在旧口径下**不可见**：

| | MERGE-AFTER-RULING-003 | 本登记 |
|---|---|---|
| 可观测特征 | `reviews == 0` | `reviews == 1`，但 reviewer == author |
| 在 `reviews >= 1` 指标下 | 违规（可见） | **合规（不可见）** |
| 防线位置 | 平台 required review（M-3） | 平台 required review **无法拦截**——它只数人，不数身份是否相同 |

关键点：`MERGE-AFTER-RULING-003` §11.1 已证明 M-3 在当前计划下不可实施（分支保护 API 返回 403）。**但即使 M-3 明天实施，本登记记录的六例仍然会通过**——GitHub 的分支保护不会阻止作者批准自己的 PR（它允许，只是不计入 required approvals 的场景取决于配置；而此处 `COMMENTED` 状态本身就不构成 approval，所以根本不在 M-3 的管辖范围内）。

也就是说：修好 M-3 不修复本登记。

---

## 3. 因果链：这是 Owner 自己那条裁定的机械后果

`MERGE-AFTER-RULING-003` 的实例计数被冻结在 4，依据是 #403 上那条 Owner 审查中的附带裁定（review id `6002557767`，2026-11-21T03:26:13Z）：

> ### 附带裁定：登记不得自我增殖
> 1. 「零审合并」实例计数**冻结在 4**，不再新增第 5 条。
> 2. 今后 Owner 执行合并时，在**被合并的那个 PR 本体**上留标准证据评论（命令、exit code、核对结论），**不再为记录这件事单独开 PR**。

这条裁定本身是合理的（它消除了「记录零审合并需要一次零审合并」的递归）。但它指定了一个**载体**——「在被合并的那个 PR 本体上留证据评论」——而没有指定该评论的身份必须与被合并者不同。

执行结果是：此后每一次合并，Owner 都在被合并的 PR 上留一条内容详实的证据评论，**通过 review API 提交**（而不是 issue comment），于是 `reviews` 从 0 变成 1，`reviews == 0` 这个违规特征随之消失。

`#414` 上两种载体并存，可直接对照：

- 5 条 issue comments（`05:13:40`、`05:14:51`、`05:24:48`、`05:35:09`、`05:48:50`）
- 3 条 reviews（`04:56:22`、`05:27:21`、`05:41:38`）

同一账号，两种通道，内容都是「Owner 运行报告」。**选择 review 通道的那几次，恰好使 `reviews >= 1`。**

本登记不判定这是有意规避。证据只说明：裁定改变了载体，载体改变了计数，计数改变了违规的可见性。

---

## 4. 审查内容的质量与独立性是两个问题

必须公平记录：这六条审查**不是空壳**。内容层面它们比多数真实审查更扎实。

| PR | 审查实际内容 | 是否发现实质问题 |
|---|---|---|
| #403 | 核对四项事实、冻结计数、给出附带裁定 | 是（裁定本身） |
| #404 | 独立 checkout 实跑，`roots 9 / exempt 20 / uniq 20 / missing []` | 是 |
| #408 | 四项行为实测，含「新增未配对规范源 → EXIT=2」的旁路验证 | 是 |
| #409 | 复现 AC-5 更正，**并公开更正自己上一轮的误判** | 是（自我更正） |
| #413 | 五项行为实测，含注入 `pull_request + self-hosted` 的违规检测 | 是 |
| #414 | **8 项中 2 项与作者期望相反，判「不能合并」**；作者改后复跑 9 项全过 | 是（否决并促成修改） |

`#414` 尤其值得单独指出：第一次审查（`04:56:22`）明确写出「8 项中 2 项与你自己写的期望相反，不能合并」，PR 随后新增 commit `ddd4150b`，第二次审查（`05:27:21`）确认九项全过并**更正了自己第一次审查中的 P2 误判**。这个流程在功能上确实拦住了缺陷。

所以本登记的结论必须精确：**问题不在审查质量，在审查主体**。同一个会话既产出被审对象、又产出审查结论、又执行合并，无论结论多扎实，都不满足 §5 的独立性要求——因为没有任何机制能保证「下一次它不会给自己盖章」。`#414` 证明它会自我否决，但那是一次自愿行为，不是结构性约束。

---

## 5. 与既有结论的关系

- **MERGE-AFTER-RULING-003**：计数按 Owner 裁定仍冻结为 4，本登记**不改动该计数**。本登记指出的是该计数所依据的可观测特征已经失效，因此「4」不再是一个能覆盖当前状态的数字。
- **CI-NOT-EXECUTED-005**：这六次合并发生时 check 全部为 `failure`/`NOT_EXECUTED`。审查正文里对此有诚实声明（#403：「这不是 CI PASS」）。但审查者与被审者同一，使这条声明失去了外部效力。
- **GATE-DEADLOCK-006**：`#408` 引入的基线正是死锁的一半成因；`#414` 修正了门禁的配对移动判定。两次都是自我审查后合并，而门禁在此后对**任何** PR 恒为 `EXIT=2`。三条叠在一起：审查不独立、门禁不执行、门禁恒拒绝。

---

## 6. 客观事实与推断分界

事实：
- §1 表中六行的 `author` / reviewer / `merged_by` / 时间差，全部来自 `/pulls/{n}`、`/pulls/{n}/reviews`、`/pulls/{n}/comments`。
- §3 引用的裁定原文来自 review `6002557767` 正文。
- §4 的审查内容摘要来自各 review 正文。
- `#414` 的 5 条 issue comments 与 3 条 reviews 并存，时间戳如上。

推断（**不作出**）：
- 不判定 Owner 选择 review 通道是为了让 `reviews` 变成 1。裁定原文只指定了「在被合并的 PR 本体上留评论」，未指定通道。
- 不判定这六次合并的**内容**有缺陷。#414 的实例反而证明审查有效。
- 不主张把计数从 4 改成 10。计数口径本身已经失去意义，换数字不解决问题。

---

## 7. 可能的处置方向（均未执行）

> **2026-11-25 附注（引文时效）。** 下表写于 2026-11-21，当时 §5 把独立性定义为 GitHub 身份的属性。2026-11-24 修订后，独立性是会话的属性，因此：
>
> - S-2 的代价不再是「需第二个身份」。一个独立会话即可；第二个身份是可选载体，不是前提。§7.1 的五条要求因此约束的是**载体**——谁把结论写在 PR 上——而不是独立性判据本身。
> - S-2 也不再是「唯一在 M-3 不可用时的结构性方案」：按现行 §5，这项要求本身已能由会话满足，不需要引入任何新账号。
> - S-1 与 S-3 的取舍不变。
>
> 表格原文保留，以便针对它写下的裁定仍然可读。

| # | 做法 | 代价 | 说明 |
|---|---|---|---|
| S-1 | 在 PR-GOVERNANCE-001 §5 中明确：`reviewer == author` 的审查**不计入** §5 要求 | 1 段文字 | 最低成本，但仍是自律条款，无平台强制 |
| S-2 | 引入第二个可提交审查的账号（人或独立会话），要求 §5 审查必须来自非作者身份 | 需第二个身份 | **Owner 已原则批准**；唯一在 M-3 不可用时的结构性方案 |
| S-3 | 把 §5 的判定从「是否存在 review」改为「是否存在 author 之外的 review 且其 commit_id == head」 | 1 条脚本 | 可自动化，可写入门禁 |

三条都不由本登记执行。S-1/S-3 是规范与脚本改动，按 §5 自身要求需独立审查；S-2 是 Owner 层决定。

### 7.1 S-2 的裁定状态

Owner 在 2026-11-21 裁定中原则批准 S-2，并给出五条最低要求：

1. PR 作者与独立审查者是不同身份；
2. 审查者不是该 PR 的唯一作者身份；
3. 合并者不得以自己的 review 替代独立审查；
4. 审查者须留下可追溯的实质审查结论；
5. `COMMENTED`、`APPROVED` 等状态不能单独证明审查独立性，必须同时核对身份关系。

**但本轮不任命第二身份。** 当前 Sponsor / accountable_owner 仍为 `NOT_ASSIGNED`；不能凭空指定一个 GitHub 账号，也不能把另一个账号的存在推定为具备授权、责任和持续履职能力。

因此 S-2 的实际状态是：

```
APPROVED_IN_PRINCIPLE / IDENTITY_NOT_ASSIGNED / NOT_YET_OPERATIONAL
```

在第二身份正式指定并建立责任边界之前，**不得宣称结构性独立审查已经建立**。S-1/S-3 自律条款继续有效，但不得被描述为平台强制防线。

---

## 8. 复算方式

```bash
TOK=...; R=oahcom/AiMemoryBrainArchitecture
for n in 403 404 408 409 413 414; do
  curl -s -H "Authorization: Bearer $TOK" https://api.github.com/repos/$R/pulls/$n \
    | jq -r '"\(.number) author=\(.user.login) merger=\(.merged_by.login) merged=\(.merged_at)"'
  curl -s -H "Authorization: Bearer $TOK" https://api.github.com/repos/$R/pulls/$n/reviews \
    | jq -r '.[] | "  review by \(.user.login) state=\(.state) at \(.submitted_at) commit=\(.commit_id[0:8])"'
done
```

判定：若 `author == merger` 且 reviews 中唯一 `user.login` 也是 `author`，则 §5 的独立性未成立。

---

**登记结论**：`MERGE-AFTER-RULING-003` 记录的失效模式（零审查）已被一种在计数上合规、在独立性上等价的形态取代。六例实测均为 `author == sole reviewer == merger`，间隔 13–74 秒。审查内容质量高，`#414` 甚至自我否决——但这恰恰说明防线依赖自愿，而非结构。本登记不改变既有计数，只记录该计数所依赖的特征已失效。

**Owner 裁定（2026-11-21）**：接受本登记为新失效模式，与 003 并列保留，不重写 003 的历史定义。明确三条禁令——不得将 `reviews >= 1` 视为独立审查的充分条件；不得把 `COMMENTED` 视为 approval；M-3 不构成该问题的修复方案。S-2 原则批准，状态 `IDENTITY_NOT_ASSIGNED`。

Owner 同时要求保留两个判断，不得互相抵销：**审查内容质量：高**；**审查主体独立性：未成立**。
