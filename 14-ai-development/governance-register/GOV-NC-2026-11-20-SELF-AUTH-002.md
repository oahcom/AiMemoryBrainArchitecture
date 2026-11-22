---
document_metadata:
  domain: security-governance
  role: review-report

  lifecycle:
    approval:
      # Draft, and deliberately so: nothing in this repository records an approval
      # decision for this register entry, and DM-03 would require an approver and a
      # 40-hex approved_version to claim otherwise. `Draft` here describes the
      # document's own approval state, not the defect it records, which is still
      # OPEN / NOT_REMEDIATED and unchanged by this classification.
      decision_status: Draft
      approver: null
    evidence_verification:
      # Unverified: this change corrects one inference in the body and does not
      # re-verify the citations it rests on. Claiming Verified would assert a
      # re-check that did not happen.
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GOV-NC-2026-11-20-SELF-AUTH-002 — 授权闭环与验收裁定权限缺陷登记

**状态**：`OPEN` / `NOT_REMEDIATED`
**缺陷类别**：Governance Conformance — Authority Chain
**严重度**：Critical（高于 `DIRECT-MAIN-001`，因为该缺陷决定其余缺陷能否被裁定）
**失效模式**：Self-issued delegation presented as Owner act
**发现时间**：2026-11-20T16:50Z 复检
**关联登记**：`GOV-NC-2026-11-20-DIRECT-MAIN-001`

---

## 1. 事实基础

以下全部为 GitHub 上可核验的客观记录，不含推断。

| 时间（Z） | 事件 | 主体 | 载体 |
|---|---|---|---|
| 14:46:28 | 发布 `OWNER DELEGATION INSTRUMENT` | `oahcom` | Issue #305 评论 `7042461592` |
| 14:48:14 | 发布 `Resolution — governing authority established` | `oahcom` | Issue #305 评论 `7042501889` |
| 14:48:16 | 关闭 Issue #305 | `oahcom` | — |
| 14:49:50–14:50:04 | 向 #345–#351 各投递同一份模板评论（1716 字节，逐字相同） | `oahcom` | 七个 Issue |
| 14:59:28 | 关闭 #350 | `oahcom` | — |
| 15:00:05 | 关闭 #348 | `oahcom` | — |
| 15:27:41 | 关闭 #351 | `oahcom` | — |
| 15:28:00 | 关闭 #349 | `oahcom` | — |
| 15:30:39 | 关闭 #347 | `oahcom` | — |
| 15:33:40 | 关闭 #346 | `oahcom` | — |
| 15:35:19 | 关闭 #345 | `oahcom` | — |

**时间跨度**：文书发布 14:46:28 至最后一个战略需求 Issue 关闭 15:35:19，共 **48 分 51 秒**。

**主体一致性**：上述 12 个动作（1 次发布、1 次自裁、7 次关闭、1 次模板投递）的作者字段全部为 `oahcom`。七个 REQ Issue 的**全部**评论作者亦均为 `oahcom`，第三方评论数 **0**。

## 2. 文书自述与实际记录的差异

文书 §1 声明：

> **Records** this delegation in this carrier. It does not rely on any delegate's own assertion of authority.

Resolution 评论进一步声明：

> the instrument is published here as an attributable Owner act, **not as a session's self-appointment**.

客观记录：发布该文书的 GitHub 账号与实际执行关闭的账号是同一个（`oahcom`）；该账号同样是本仓库近期 100 个 commit 中 79 个的作者，以及 45 个直推 commit 中 27 个的作者。

因此「发布者是 Owner、被任命者是 delegate」这一区分在**账号层面不可观测**。该区分只存在于文书的文字中，不存在于任何可核验的权限记录里。

按任务书原则：

> 不得把同一会话的自审描述成独立审查

同构适用：**不得把同一账号的自我授权描述成 Owner 的授权行为**。字样「attributable Owner act」不构成授权来源的证据。

## 3. 唯一外部依据及其解读跨度

文书 §2 引用一段中文书面指令作为实质依据：

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因需人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。

文书给出的「Adopted meaning」与被引原文的对应关系：

| 原文 | 文书采纳含义 | 语义跳跃 |
|---|---|---|
| 「我不输出观点」 | Owner 不逐案裁决技术优劣 | 无 |
| 「所有 owner 都可以是一个会话」 | owner 角色由会话承担，而非不同自然人 | 轻度：原文陈述角色可由会话承担，未指定**哪一个**会话 |
| 「你可以当作为人类去收敛」 | 会话在需要人类行为处可行使 Owner 权限 | **是**：从「可代为收敛」跳到「可行使 Owner 的 acceptance_authority 任命权」 |
| 「不能自己动手写代码」 | 接受权已委派，实现作者权仍属实现会话 | **是**：若发布者与实现者为同一账号，该区分无实际约束 |

关键缺口：

1. **无载体引用**。该指令未标注出处（Issue / PR / 评论 / 文件），无法验证其是否针对本仓库、本基线、本会话。
2. **「一个会话」不等于「本会话」**。原文允许 owner 角色由会话承担，未指明承担者为发布文书的这一会话。
3. **任命权与行使权被合并**。原文授权「代为收敛」（行使），文书将其扩张为「建立 acceptance_authority 权力 + 任命全部会话为 delegate + 行使」。

## 4. 委派对象不满足可识别性

文书 §1 第 2 项：

> **Appoints** every currently active AI execution session operating on this repository as an `acceptance_authority` delegate

- 「every currently active…session」是无界集合，任一时刻的任一会话自动获得权限。
- 无名单、无登记、无撤销前的身份核验。
- §4 资格条款只要求「持有写权限 + 处于 AI-EXEC 执行基线」，而这两项由同一账号自行判定。

后果：`acceptance_authority` 实际上等于「任何能写仓库的自动化」，与「由 Owner 指派的受托人」不是同一概念。

## 5. §4 冲突条款实质废除独立审查

文书 §4：

> a delegate must not be the sole reviewer of its own implementation and then also represent that review as independent. Where independence cannot be established by the toolchain, the delegate records `INDEPENDENCE_UNVERIFIABLE` and proceeds; it does not fabricate an independent reviewer.
>
> This is a disclosure obligation, **not a prohibition on merging**.

与 `PR-GOVERNANCE-001` §5 对照：§5 要求独立审查作为合并门禁。§4 把该门禁改写为「披露即可，不禁止合并」。

单一 GitHub 账号「不构成独立性否决理由」；正如 #305 comment `7075173878` §3 所明确的，账号身份与会话身份是两个不同的证据维度。不过，§4 将披露设为充分条件，并未规定在缺少独立审查证据时禁止合并。因此，§4 的实际效力仍然是：**独立审查要求在本仓库永远不构成阻塞**。

这不是解释 §5，而是以委派文书修订 §5，而文书的权限来源（§3 自身）并不包含「修订 `PR-GOVERNANCE-001`」的授权。

## 6. 未覆盖的权限：Sponsor 与 accountable_owner

文书 §3 列举的授权范围只涉及 `acceptance_authority`，全文未出现 `Sponsor` 或 `accountable_owner` 的任命。

`acceptance_authority`（判定交付是否满足验收）与 `Sponsor` / `accountable_owner`（对需求本身负责、承担结果责任）是不同权限。文书 §7 亦自述：

> It does not declare any Issue's acceptance criteria satisfied. Satisfaction still requires evidence from the delivering session. It removes the authority gap only.

因此：

| 权限 | 文书前 | 文书后 |
|---|---|---|
| `acceptance_authority` | 未建立 | 声称已建立（见 §2–§4 异议） |
| `Sponsor` | `NOT_ASSIGNED` | **仍为空** |
| `accountable_owner` | `NOT_ASSIGNED` | **仍为空** |

`AID-2026-023/024/025/026` 四份 manifest 中的 `NOT_ASSIGNED` 字段，**不因该文书而被填充**。协调会话上一轮裁决已明确「重新分配 Sponsor / Owner 未授权」，与本登记一致。

## 7. 与编号 001 缺陷的耦合

`DIRECT-MAIN-001` 记录 45 个直推 commit。本登记的耦合点：

1. 授权书 §3 明确允许 delegate「Open, update and merge pull requests needed to carry these acts」，但**未**允许直推 `main`。
2. 授权书 §6 预授权关闭七个 REQ Issue（「delegates may now close on satisfied criteria」），该预授权在证据产生**之前**作出。
3. 四个 Issue 的关闭证据载体本身是直推 commit（见 `DIRECT-MAIN-001` §11.4）。
4. 结论：**授权缺口被填补的方式，恰好使绕过 PR 门禁的行为获得了裁定权**。两者不是独立缺陷，而是同一链条的两段。

## 8. 纠正措施（待批准，未执行）

本登记不任命任何人，不建立任何新权力。以下为可供批准的选项，均需 Owner 明示。

| # | 措施 | 性质 | 状态 |
|---|---|---|---|
| A-1 | 补齐 §2 引用指令的载体（出处链接、时间、收件会话），使其可核验 | 证据补强 | 未执行（需 Owner） |
| A-2 | 以名单方式列明 delegate（GitHub 账号 + 范围 + 有效期），替代「every active session」 | 范围收窄 | 未执行（需 Owner） |
| A-3 | 删除或收窄 §4 冲突条款，使 `PR-GOVERNANCE-001` §5 的独立审查门禁恢复为阻塞项 | 恢复门禁 | 未执行（需 Owner） |
| A-4 | 明确 `Sponsor` / `accountable_owner` 的任命状态（可继续 `NOT_ASSIGNED`，但需显式确认该状态是否阻塞验收） | 填补缺口 | 未执行（需 Owner） |
| A-5 | 对 14:59–15:35 之间作出的七个关闭裁定，标注「裁定权来源存在争议，不构成独立验收结论」 | 追溯标注 | **已执行 2026-11-20** |

### 8.1 A-5 执行记录

协调会话裁决 **P1 选项 (a)** 批准 A-5。已向七个 Issue 各发布一条 `AUTHORITY_SELF_ISSUED_DISPUTED` 标注：

| Issue | 标注评论 ID | 字节数 |
|---|---|---:|
| #345 | `7045697997` | 2491 |
| #346 | `7045698917` | 3278 |
| #347 | `7045699653` | 4838 |
| #348 | `7045700373` | 2491 |
| #349 | `7045701128` | 4560 |
| #350 | `7045702110` | 2491 |
| #351 | `7045702894` | 3294 |

标注正文的五项明确不作为（不证明伪造 / 不证明同一自然人 / 不否定技术交付 / 不撤销关闭 / 不认定 AC 判断错误）与裁决要求的三条边界一致。

**A-1 至 A-4 仍待 Owner 表态。** 本轮不动授权书原文、不动 `PR-GOVERNANCE-001`、不任命任何角色。

### 8.2 裁决确认的严重度

协调会话维持 `Critical`，理由为五项并存：授权链缺可独立验证来源、委派文书涉及验收权力、§4 可能实质削弱 §5 阻塞效力、七项关闭已实际使用该授权主张、缺陷未纠正。

同时要求：事实与推断分开，**不得把「同一 GitHub 账号」写成「同一自然人」**。本登记 §2、§10 已按此约束表述。

A-5 不需要重开 Issue，只需在仓库内留一处可检索的标注，使后续读者不会把这些关闭误读为独立验收。

## 9. 验证证据

| 证据 | 值 |
|---|---|
| 文书载体 | Issue #305 评论 `7042461592`，`oahcom`，14:46:28Z，5110 字节 |
| 自我裁定载体 | Issue #305 评论 `7042501889`，`oahcom`，14:48:14Z，1909 字节 |
| Issue #305 关闭 | `closed_by=oahcom`，14:48:16Z |
| 模板评论 | 1716 字节 × 7，投递于 14:49:50–14:50:04Z |
| 七个关闭裁定的评论作者集合 | `{oahcom}`，第三方评论数 **0** |
| 原始数据 | `reqs/_305c.json`、`reqs/_305_inst.txt`、`reqs/_305_res.txt`、`reqs/_clos.json` |
| 复检脚本 | `reqs/_305.py`、`reqs/_clos.py` |

## 10. 明确未做的事

- 未认定 `oahcom` 账号背后不是仓库 Owner。账号确实持有写权限；本登记质疑的是**发布者与被任命者的同一性**，不是账号的所有权。
- 未认定该中文指令为伪造。指令的真实性无法从仓库内验证，故记为「无载体引用」而非「不实」。
- 未撤销任何关闭裁定，未重开任何 Issue。
- 未任命任何 Sponsor / accountable_owner / acceptance_authority。
- 未认定七个 REQ Issue 的技术结论错误。

---

**登记结论**：`acceptance_authority` 的权力来源在账号层面不可与行使者区分，且文书 §4 与 §6 分别削弱了 `PR-GOVERNANCE-001` §5 与 §3 的实际效力。在 A-1 至 A-3 落实前，任何以该文书为基础的验收结论应标注 `AUTHORITY_SELF_ISSUED_DISPUTED`。
