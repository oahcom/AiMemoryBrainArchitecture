---
document_metadata:
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Approved
      approver: "delegated operator (coordinating session) under explicit human-owner authorization; not a natural-person signature"
      decision_date: "2026-11-27"
      approved_version:
        scheme: content-hash
        value: "1c15a4c972b0aff4ddbb97894f863ca6a8e2cecf21d00d6b1306eb7df0928885"
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "OA-MERGE-2026-11-27-1325"
        - "14-ai-development/PR-GOVERNANCE-001.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "本记录的条件在合并决策点逐条核对；本条目不主张任一条件曾经成立。"
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
    # 权威原文的译本，不独立主张规范权威；见下方 bilingual_counterpart。
    canonical_status: Non-Canonical
    canonical_scope: "Delegated merge authorization for PR #1325"
    canonical_scope_id: "ai-development/decisions/oa-merge-2026-11-27-1325"
    canonical_scope_keywords:
      - merge-authorization
      - delegated-operator
      - pr-1325
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "00-governance/decisions/2026-11-27-merge-authorization-pr-1325.md"
    en: "docs/en/00-governance/decisions/2026-11-27-merge-authorization-pr-1325.md"
  steward: "Architecture Governance (delegated operator for this record)"
---

# 合并授权记录 —— PR #1325（代理发布）

- Decision ID: `OA-MERGE-2026-11-27-1325`
- 授权对象：拉取请求 #1325，最多一次合并
- 发布日期：2026-11-27
- 发布身份：GitHub 账号 `oahcom`
- 记录状态：已发布的授权，有界且可撤回；它本身不授权任何动作

## 1. 授权主体与代理发布声明

本记录由协调层（delegated operator，代理操作者）依据人类所有者的明确授权发布；该授权允许协调层在本决策上代行人类角色。`oahcom` 仅为发布身份，不表示 Owner A 本人签署，也不得被读作 Owner A 亲自签署的文书。本记录不存在任何自然人签署，也不主张存在。

协调层是非人类代理：它不是自然人，不持有所有者角色，本记录除第 3 节所述范围外不向它授予任何权力。

## 2. 授权来源与边界

- 授权来源：人类所有者于 2026-11-27 在裁决会话中明确授权协调层就 PR #1325 的合并决策代行人类角色。该授权**没有**以独立的委托文件形式存档；本记录是它的第一份仓库内物件，缺少在先文件这一点如实写明，不作掩饰。
- 边界：授权仅覆盖「允许 PR #1325 合并一次」这一决策。它不转移所有权，不授权任何其他拉取请求，也不授权修改本仓库的分支保护、必需上下文或审查规则。

## 3. 授权范围

1. 仅 PR #1325。
2. 仅一次合并。第二次合并、回滚后重新合并、或任何其他 PR 的合并，都需要一份新记录与新的 Decision ID。
3. 第 4 节任一条件不得被豁免、重排、重新解释，也不得以论证代替证据来满足。条件无法举证，即不合并。

## 4. 生效条件 —— 五条须在合并决策点同时成立

下列技术状态由独立取证（W1）在 head `a3c236823138bd138e747f71098c4019bd67c560` 上测得，记录为**测量值，不是常驻许可**：分支刷新后 head 会变化，每一条都必须在新 head 上重新成立。

1. **新 head。** 分支刷新到当时的 `main` 之上并取得新的 head SHA。本记录中的 SHA 只是历史证据，不授权任何动作。
2. **该 head 上全部必需上下文通过。** 16 个必需状态上下文全部为 `SUCCESS`；无 `pending`、无 `failure`、无缺失。这 16 个名称已与 `GET /repos/{owner}/{repo}/branches/main/protection` 逐字比对并一致。
3. **`mergeable_state=clean`。** 测量时为 `behind`（落后 `main` 7 个提交），不是 clean，因此在刷新前不满足本授权下的可合并条件。
4. **SHA 稳定。** 校验时观察到的 head SHA 与合并时的 head SHA 相同。两者之间发生 push 即使校验失效。
5. **独立于作者会话的审查证据。** 必须存在可引用的证据，证明该变更由作者会话之外的第三方检视过。获取方式按优先次序：(a) 来自非作者会话发布身份的 GitHub 账号的 review 或评论；(b) 记录在案的第二个会话审查，含会话标识与其读取的材料；(c) 由未撰写该变更的一方从仓库重新推导被改动的结论，并保留命令与输出。CI 绿灯不能替代上述任何一种。

测量时的保护配置：`strict=true`、`enforce_admins=true`、无必需审查。`enforce_admins=true` 表示合并路径无法绕过必需上下文；而「无必需审查」意味着条件 5 **不能**由分支保护满足，必须由分支保护之外产生的证据满足。

## 5. 失效条件

出现下列任一情形，本授权即失效，无需另行通知：

1. 第 4 节任一条件不成立或无法举证。
2. 校验之后 head SHA 发生变化。
3. PR #1325 的范围变化：新增改变变更实质的提交、diff 扩大、标题或用途被改写。
4. 分支保护配置变化，使条件 2 的 16 上下文比对不再成立。
5. 人类所有者撤回授权。

## 6. 合并后最小回读清单

合并后须记录并留存：

1. 合并后的 `main` SHA。
2. merge commit SHA。
3. `main` 上 `AID-2026-241/` 目录的文件清单。
4. `14-ai-development/work-items/INDEX.md` 中对应的一行。
5. `main` 的 `git log -1` 输出。

无法产出的条目记为 `NOT_RECORDED`，不得推断。

## 7. 已知风险

- **自指风险。** PR #1325 修改的正是「独立审查由会话还是由账号判定」这条规则本身。因此作者会话对该变更的自评构成自指：它在评价那条将要验证自己工作的规则。此处如实记录为风险，本记录不予消解。
- **CI 不是审查。** 16 个上下文全绿只能证明声明的检查在某个提交上通过，不能证明独立第三方检视过该变更，也不得用来满足条件 5。**不得以 CI 绿灯替代独立审查。**
- **测量过期。** 第 4 节所有技术值均在分支刷新前测得。刷新后仍把它们当作现状，正是本节要防的错误。
- **测量通道不可用。** 发布时本工作区的 GitHub API 配额已耗尽（HTTP 403），因此第 4 节的数值无法在此重新测量。它们按「先前测量」记录，不按「刚刚核实」记录。

## 8. 审计字段

| 字段 | 值 |
|---|---|
| `decision_id` | `OA-MERGE-2026-11-27-1325` |
| `authorization_channel` | 人类所有者在裁决会话中于 2026-11-27 向协调层作出的明确授权；由代理操作者发布进仓库 |
| `published_by` | GitHub 账号 `oahcom`，以代理操作者身份发布（仅为发布身份） |
| `delegation_source` | 人类所有者「就本决策代行人类角色」的授权；作为独立委托文件为 `NOT_RECORDED` |
| `authorized_scope` | PR #1325，一次合并 |
| `measured_head` | `a3c236823138bd138e747f71098c4019bd67c560`（历史值；不授权任何动作） |
| `NOT_RECORDED` | `NO_NATURAL_PERSON_SIGNATURE; DELEGATED_OPERATOR_DECISION` |
| `review_independence` | 本记录未确立；见条件 5 |

本记录不主张 Owner A 曾亲自审查、批准、签署或合并任何内容。它唯一的声明是：一位经人类所有者授权的代理操作者，发布了一份有界、可撤回、条件可核验的合并授权。
