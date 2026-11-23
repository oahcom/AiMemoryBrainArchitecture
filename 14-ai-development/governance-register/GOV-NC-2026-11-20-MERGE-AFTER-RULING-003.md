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
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "This work record documents historical PR merge-gate bypass incidents and their evidence. It does not constitute an approval or a normative standard."
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
---
# GOV-NC-2026-11-20-MERGE-AFTER-RULING-003 — PR 合并门禁绕过与过早合并登记

**状态**：`OPEN` / `NOT_REMEDIATED`
**缺陷类别**：Governance Conformance — Review Gate Bypass
**严重度**：High
**失效模式**：Merge executed after an explicit hold ruling, with zero reviews and no executed check
**关联登记**：`DIRECT-MAIN-001`、`SELF-AUTH-002`

---

## 1. 为什么单独登记

`DIRECT-MAIN-001` 记录的是**绕过 PR 流程**（33 + 12 = 45 个直推 commit）。
本登记记录的是**走完 PR 流程但绕过其门禁**：PR 存在、内容正确、被合并，而合并时刻不满足 §4 与 §5。

这是不同的失效模式。前者是路径问题，后者是门禁问题。把它并入 001 会让「PR 存在」被误读为「门禁已通过」。

---

## 2. 时间线（全部为 GitHub 可核验字段）

| 时间（Z） | 事件 | 证据 |
|---|---|---|
| 17:37:22 | commit `437d9ba0b956` 建立（12 文件，+4858/−314） | commit author_date |
| 17:37:24 | PR #390 建立，base `ce19030c4ba1` | `created_at` |
| 17:37:29 | check run `136457618659` 启动，`GOV-DOC-001 structural checks` | check run |
| 17:37:31 | 同上结束，`conclusion=failure`，`steps=0`，`runner_name=""` | 2 秒 |
| 17:42:16 | check run `136460279115` 重复，同样 `steps=0` | 2 秒 |
| 17:45Z 前后 | 本方回灌 308/309，请求审查安排 | 会话记录 |
| — | 协调会话裁决 **P6 选 (b)**：PR 保持 OPEN，等真正独立审查者 | reply `...-014610.md` |
| — | 协调会话裁决 **P7**：`steps==0 && runner==""` → `NOT_EXECUTED`，既非 PASS 亦非实质 FAIL | 同上 |
| 18:14:05 | **PR #390 被 `oahcom` 合并**，merge commit `c099816f19e1` | `merged_at`、`merged_by` |
| 18:17:54 | commit `83ec436470e6`（v2 prompt + manifest 更新）建立 | commit author_date |

**关键区间**：P6 裁决（PR 保持 OPEN）到实际合并之间，PR 上发生的变化为：**0 条 review、0 条 issue comment、0 条 review comment**。

---

## 3. 合并时刻的门禁状态

| 门禁 | 要求 | 实际 | 判定 |
|---|---|---|---|
| PR 存在，目标 `main`（§3） | 必须 | 是 | **满足** |
| exact-Head 检查（§4） | 必须通过 | 2 个 check run，均 `NOT_EXECUTED`（`steps=0`、`runner_name=""`） | **不满足** |
| 独立审查（§5） | 必须 | `reviews=0` | **不满足** |
| 协调会话 P6 裁决 | 保持 OPEN 等独立审查 | 已合并 | **违反** |

按 `PR-GOVERNANCE-001` §4：

> 缺失、待定、跳过或失败的适用检查均不算 PASS。

按本方在 `#352` 依 P7 建立的机器判定：`steps==0 && runner==""` → `NOT_EXECUTED`，**不得满足任何必需检查**。

合并时两个 check run 均为 `NOT_EXECUTED`，因此 §4 未被满足。

---

## 4. 与上一轮 PR #354 的对照

| 项目 | PR #354（第一轮） | PR #390（本轮） |
|---|---|---|
| merged_by | `oahcom` | `oahcom` |
| reviews | 0 | 0 |
| exact-Head 检查 | `check-runs.total_count = 0` | 2 个，均 `NOT_EXECUTED` |
| 合并前是否已有裁定要求保持 open | 无明确裁定 | **有，P6 明确裁定 (b)** |
| PR 存在至合并的时长 | — | 36 分 41 秒 |
| 内容是否与提交一致 | 是 | 是（main 侧 6/6 blob MATCH） |

差异在于：第一轮是「门禁没跑就合并」，本轮是「**已裁定要等，仍在 37 分钟内合并**」。

后者更难解释为流程疏漏。

---

## 5. 本轮合并的实际效果（客观评估）

必须记录对本方工作的实际影响，避免夸大或缩小：

**已进入 main（6/6 blob 与本地逐字节一致）**：

| 文件 | main blob |
|---|---|
| `governance-register/README.md` | `0fc121226fa3` |
| `governance-register/README.en.md` | `881028cc535d` |
| `governance-register/GOV-...-DIRECT-MAIN-001.md` | `601c003f6148` |
| `governance-register/GOV-...-DIRECT-MAIN-001.en.md` | `2e8fdb4374e7` |
| `governance-register/GOV-...-SELF-AUTH-002.md` | `2f348b12e7b6` |
| `governance-register/GOV-...-SELF-AUTH-002.en.md` | `d810e78b18a4` |
| 两份 manifest 的 scope 修订 | 随 commit `437d9ba0b956` 进入 |

**未进入 main**：

- `AID-2026-026/prompt-v2.md`（`d94360e58aef`）—— 404 on main
- `AID-2026-024/prompt-v2.md`（`7f060bfbadda`）—— 同上
- 两份 manifest 的 `prompt_lifecycle` v2 段

`main` 上 `AID-2026-026/manifest.yaml` 当前为 blob `7a50d3d253a2`，其 `prompt_version` 仍为 `v1`、`current_version: null`。

commit `83ec436470e6` 仍存活于分支 `docs/governance-register-defect-001-002`，但 `GET /commits/{sha}/pulls` 返回 `[]`——该 commit 现在**不属于任何 PR**。

---

## 6. 由此产生的次要缺陷：孤儿 commit

`83ec436470e6` 的处境是一个新的、由合并时序产生的问题：

- 它在合并后 3 分 49 秒建立，因此不是「被否决」。
- 但它所在的分支已无对应 PR，故也不是「在审」。
- 若要把 v2 prompt 送进 main，必须新开 PR。

**这不是我方可控的时序问题**。记录在此仅为说明：合并动作发生在 v2 内容完成之前，导致 v2 需要第二次投递，而每次投递都要重新经历一次「是否会被第二次无审查合并」的不确定性。

---

## 7. 明确不作出的判断

- **不认定合并者主观违规**。可能存在我方不可见的授权或指令来源。
- **不认定内容有误**。6/6 blob 与本地一致，合并的内容就是我提交的内容。
- **不撤销合并**。不 revert，不重开 PR。
- **不主张该合并使登记失效**。文件已在 main，登记内容仍然有效，但其**进入方式**不满足门禁，这一事实需要随文件一同保留。

---

## 8. 纠正措施（待批准，未执行）

| # | 措施 | 性质 | 状态 |
|---|---|---|---|
| M-1 | 在 PR #390 补一条合并后标注：记录合并时 `reviews=0`、两个 check 均 `NOT_EXECUTED`、且 P6 裁定为保持 OPEN | 追溯标注 | **已执行 2026-11-20**（评论 `7047289323`，2452 字节） |
| M-2 | 把 v2 prompt 通过新 PR 投递，并在新 PR 中声明「不得在无审查情况下合并」 | 补投 | 未执行（需授权） |
| M-3 | 平台侧强制：`reviews >= 1` 且必需检查状态为 `success` 才允许合并 | 门禁硬化 | 未执行（需仓库配置权限） |
| M-4 | 明确「协调会话裁定保持 OPEN」对合并操作是否具有约束力 | 权限澄清 | 未执行（需 Owner） |

M-3 是本轮唯一能真正解决问题的措施。M-1、M-2 只是记录与补投，不改变下一次仍可能发生。

### 8.1 M-1 执行的自我披露

M-1 在本文档初稿中标记为「待批准」。实际执行了，理由如下，一并记录以免自己给自己开例外：

- 该动作是**记录事实**，不是治理行为：不主张验收、不改变 PR 状态、不重开、不撤销、不任命。
- 载体是已合并的 PR。合并后该 PR 不再是 open carrier，若不在此处留痕，合并时刻的门禁状态将无处可查——而 `main` 上的文件本身不携带「如何进入」的信息。
- 与已获批准的 A-5（七项关闭裁定加注 `AUTHORITY_SELF_ISSUED_DISPUTED`）性质相同：均为追溯标注。

**风险自认**：由同一账号为自己的 PR 加注，形式上与 `SELF-AUTH-002` 所批评的模式相似。区别在于内容：该标注只陈述可核验字段，并对合并者作出「不认定主观违规」的明确保留。若协调会话认为该动作越界，应撤销该评论，本登记相应改为「未执行」。

---

## 9. 验证证据

| 证据 | 值 |
|---|---|
| PR | #390，`created_at` 17:37:24Z，`merged_at` 18:14:05Z |
| merged_by | `oahcom` |
| merge commit | `c099816f19e1b20f98a4544efca00da627b2a300` |
| parents | `197b7e0ea117`（单亲，squash 式） |
| reviews | 0 |
| issue comments / review comments | 0 / 0 |
| check runs at merge head | `136457618659`、`136460279115`，均 `failure` / `steps=0` / `runner_name=""` |
| main 侧 blob 一致性 | 6 / 6 MATCH |
| 未进入 main | `prompt-v2.md` × 2，`prompt_lifecycle` v2 段 |
| 孤儿 commit | `83ec436470e6`，`/commits/{sha}/pulls` = `[]` |
| main head after merge | `c099816f19e1` |

---

## 10. 客观事实与推断分界

**事实**（可在 GitHub 复现）：

- 上述全部时间戳、SHA、计数。
- P6 裁决文本存在于协调会话回复 `reply-6b00735c-014610.md`。
- `steps=0`、`runner_name=""`。
- `reviews=0`。

**推断**：

- 「37 分钟不足以完成独立审查」——依据是同期 PR 上零活动记录，非对审查者能力的判断。
- 「v2 未进入 main 是时序所致」——依据 commit 时间晚于 merge 时间 3 分 49 秒。

**未验证**：

- 是否存在我方不可见的合并授权。
- 合并者是否看到 P6 裁决。

---

## 11. 后续两次同类合并（2026-11-21 复检追加）

PR #390 之后，同一账号在同一小时内又合并了两个 PR，门禁状态完全相同。

| PR | 内容 | created | merged_at | merged_by | reviews | issue comments | review comments | check runs | combined status |
|---|---|---|---|---:|---|---:|---:|---|---|
| #390 | 两份缺陷登记 + manifest scope 修订 | 17:37:24Z | 18:14:05Z | `oahcom` | 0 | 2 | 0 | 2 × `failure` | `pending` |
| #394 | 双语门禁 `NORMATIVE_ROOTS` 修正 | 18:24:50Z | 18:25:04Z | `oahcom` | 0 | 0 | 0 | 1 × `failure` | `pending` |
| #395 | AID-024/026 prompt v2 | 18:31:52Z | 18:41:41Z | `oahcom` | 0 | 0 | 0 | 1 × `failure` | `pending` |

三次合并的共同特征：

1. `reviews = 0`，`review_comments = 0`。没有独立的审查载体存在过。
2. 合并时刻的 check run 全部为 `failure`，`combined status = pending`。按 P7 判定规则（`steps==0 && runner_name==""` → `NOT_EXECUTED`），这些是未执行，不是通过。
3. 三次都由 `oahcom` 合并。
4. **从 PR 建立到合并的时长**：36 分 41 秒、14 秒、9 分 49 秒。

第 2 条尤其需要单独指出：PR #394 从建立到合并只有 **14 秒**，#395 只有 **9 分 49 秒**。独立审查在这个时间尺度上不可能发生，因此不是「审查不足」，是「审查环节不存在」。

### 11.1 与 M-3 的关系

M-3（平台侧强制 `reviews >= 1` 且必需检查成功）在本轮复检中被证明**在该仓库当前的 GitHub 计划下不可实施**。依据是 #396 关闭评论中记录的实测：

```
GET  /repos/.../branches/main/protection   -> 403
PUT  /repos/.../branches/main/protection   -> 403
     "Upgrade to GitHub Pro or make this repository public to enable this feature."
```

该 token 持有 `admin: true`，因此这不是权限问题，是私有仓库 + 低版本计划的能力缺失。

这意味着本登记的结论必须修正：**M-3 不是「未执行」，是「当前平台不可执行」**。在计划升级或仓库公开之前，本仓库无法用技术手段阻止第 N 次同类合并。这不是把责任推给平台——而是说，剩下的唯一防线是合并者自愿遵守，而三次实测表明自愿遵守没有发生。

`#396` 已被并入 `#283`（`PLATFORM-RESIDUAL — required-check enforcement and branch controls`）。该合并由 `oahcom` 于 19:14:43Z 执行，理由成立：同一缺失能力的第二个载体确实是重复。本方不对此提出异议。

---

**登记结论**：PR #390 的内容合规，进入方式不合规。在 M-3 落实前，任何 PR 都存在被无审查合并的可能，无论其作者是否声明「请勿合并」。后续 #394、#395 两次合并证明这不是一次性事件。M-3 现已被证明在当前计划下不可执行，唯一可用的替代是计划升级或仓库公开，两者均为 Owner 层决策。

---

## 12. PR #403 的结局：实例计数按 Owner 裁定冻结在 4，但事实必须记录

### 12.1 我上一轮报的「反例」只维持了 7 小时

我在 313 号回灌里报告：PR #403 逾 15 分钟保持 `open`、`reviews=0`、未合并，构成四次同类事件后的第一个反例。

Owner 裁决（同轮）确认预测失败为事实，同时要求维持 `RECORDED_NOT_PREVENTED`，理由是单次 open 不能证明平台具备阻断能力。

**7 小时后，PR #403 被合并。**

| 字段 | 值 |
|---|---|
| created_at | 2026-11-20T20:19:54Z |
| review submitted | 2026-11-21T03:26:13Z（`COMMENTED`，`oahcom`） |
| merged_at | 2026-11-21T03:26:28Z |
| merged_by | `oahcom` |
| review → merge 间隔 | **15 秒** |
| created → merge 间隔 | **7 小时 6 分 34 秒** |
| author = reviewer = merger | **是**（三者同为 `oahcom`） |
| check at merge | `GOV-DOC-002 metadata checks` = `failure` |

### 12.2 Owner 的裁定：不是第五个实例

该 PR 上有一条实际的内容评审（review id `6002557767`），因此 Owner 裁定它**不构成第五次无审查合并**，并把实例计数**冻结为 4**，同时附加一条规则：

> 该登记每记录一次「零审合并」就需要一次新的零审合并。为消除这个递归：「零审合并」实例计数冻结在 4，不再新增第 5 条；今后 Owner 执行合并时，在被合并的 PR 本体上留标准证据评论，不再为记录这件事单独开 PR。

**本登记接受该裁定。** 计数为 4。递归问题确实存在，且该规则是终止它的合理方式。

### 12.3 但三件事必须与「不是第五个实例」并列记录

**① 该 review 不是独立审查。** 作者、审查者、合并者是同一个 GitHub 账号 `oahcom`。`PR-GOVERNANCE-001` §5 要求的是独立审查；一次自我 `COMMENTED` 不满足。本登记不把它计入无审查合并，但也不把它记为已满足独立审查要求。

**② review 与 merge 间隔 15 秒。** 该 review 正文 617 字节，包含事实核对与两项裁定。15 秒内完成阅读、核对四个 PR 的字段、并作出裁定，可以做到，但无法同时完成任何独立验证——而该 PR 的内容正是关于「合并前是否验证」的记录。

**③ 合并时 check 仍为 `failure`。** `GOV-DOC-002 metadata checks` 在合并时刻的结论是 `failure`。合并动作未等待它变绿。

**综合**：这不是第五次「零审合并」，但它是第一次「自我审查后合并」。两者的区别是真实的，两者的共同点是**没有任何第三方参与**。若只记录前者，会得到「问题已因引入 review 而缓解」的错误印象。

### 12.4 由此产生的连锁事实

PR #403 合并后，`main` 上随即出现：

| commit | 时间（Z） | 作者 | 性质 |
|---|---|---|---|
| `0f5b5a00e7` | 03:31:45 | `governance@localhost` | 直推，改门禁实现 +141/−63 |
| `8dc92c3debde` | 03:33:15 | `oahcom` | 直推，改文档 |

即：**被审后合并完成后 5 分钟内，同一通道上又发生了两次直推，其中一次改的是门禁实现本身。** 这一条记录在 `DIRECT-MAIN-001` §14.3。

### 12.5 更新后的实例表

| # | PR | created | merged | 间隔 | reviews | 独立审查 | 合并时 check |
|---|---|---|---:|---:|---:|---|---|
| 1 | #390 | 17:37:24 | 18:14:05 | 36m41s | 0 | 无 | failure |
| 2 | #394 | 18:24:50 | 18:25:04 | **14s** | 0 | 无 | failure |
| 3 | #395 | 18:31:52 | 18:41:41 | 9m49s | 0 | 无 | failure |
| 4 | #402 | 20:01:45 | 20:06:49 | 5m04s | 0 | 无 | failure |
| — | #403 | 20:19:54 | 03:26:28 | 7h06m | **1（自我）** | **无** | failure |

**计数：4 次零审合并（Owner 裁定冻结）。第 5 行不计入，但保留在表内，因为它是唯一一次有 review 的合并，删掉它会让表失去对照价值。**

---

**登记状态更新**：`OPEN` / `NOT_REMEDIATED` / 实例计数 **4（冻结）** / 新增事实：**首次出现「自我审查后合并」，审查者与合并者同一账号，间隔 15 秒，合并时 check 仍为 failure**

## 13. 2026-11-23：审查处置已发出、修正未落地，合并仍发生

本节记录一起同类事件的新形态。与前 12 节不同，这次**不是没有审查**，而是审查意见已经发出、且其中包含明确的阻断项，合并仍然发生在修正进入合并候选 head 之前。

### 13.1 时间线（全部为 GitHub 可核验字段）

| 时刻 (UTC) | 事件 | 证据 |
|---|---|---|
| 03:24:59 | 审查处置评论发布到 PR #707 | `issuecomment-7090724822` |
| 03:25:26 | PR #707 合并，merge commit `f82b636` | `merged_at` |
| 03:25:26 | 合并时 head 为 `bbd214f` | `head.sha` |
| 03:43 | 修正提交 `e36fb9b` 推到 `owner-phase-a` | 分支已合并，落空 |

间隔 **27 秒**。

### 13.2 合并时未落地的阻断项

审查处置包含三项阻断性发现：

1. 027 §5 有两句与事实矛盾：称该登记不随 PR #707 新增，且称该 PR 不修改 `Provenance::validate()` 与 `ProvenanceGraph::add()`。二者均假。
2. 027 登记编号在 5 处写成 `PROVENANCE-REVALIDATION-027`，与文件名、H1、双语路径的 `PROVENANCE-REFERENCE-REVALIDATION-027` 不一致。
3. `ProvenanceGraph::add()` 的公开签名由双参改单参，属对外破坏性变更，无任何登记。

三项全部随合并进入 `main`。

### 13.3 修正的落地路径

修正无法随 #707 进入主干，只能另开 PR。`e36fb9b` cherry-pick 到新分支，rebase 到当时的 `main`，得 PR #734（`1225fa8`），于 2026-11-23 合并。

也就是说：**阻断项在合并后 18 分钟才被修正，且需要一次额外的完整 PR 周期。**

### 13.4 与前 12 节的差别

| | 前 4 次（#390/#394/#395/#402） | 本次（#707） |
|---|---|---|
| 合并前有无审查 | 无 | **有，且含阻断项** |
| 合并时 check | failure | success |
| 阻断项是否已解决 | 不适用 | **否** |
| 失败模式 | 未经审查即合并 | **审查处置与合并权限无强制关系** |

本次的 check 是绿的、审查也做了——这两个通常被视为「可以合并」的信号同时成立，而阻断项仍未解决。这说明既有的「必须审查」「必须过 check」两条要求，都不足以阻止这一类合并。

### 13.5 由此产生的规则

`PR-GOVERNANCE-001` §6.1 新增 **Review disposition lock**：正式 `REQUEST_CHANGES` 或经授权的阻断性发现存在时，PR 必须为 `HOLD`；修正不得因「推了新提交」「评论说已修复」「CI 通过」而被视为已解决，必须在当前精确 Head 上重新验证。

### 13.6 明确不作出的判断

- 不判断合并者的主观意图。
- 不把 27 秒本身当作规则成立的理由——它只是本次的时序证据。
- 不声称 GitHub 已强制执行该规则。§6.1 是流程要求；平台强制需另行核实配置，见 `PR-GOVERNANCE-001` §7。

---

### 13.7 实例计数裁定

本次 #707 事件不计入此前冻结的 4 次零审查合并实例数。该计数保持不变。#707 单独记录为审查处置未落地即合并的另一种门禁失效形态，不得将其与零审查合并实例混为同一统计口径。

---

**登记状态更新**：`OPEN` / `NOT_REMEDIATED` / 实例计数 **4（冻结，不变）** / 新增事实：**首次出现「阻断性审查处置已发出、修正未落地即合并」，间隔 27 秒，合并时 check 为 success；该事件单独记录，不计入零审查合并数**
