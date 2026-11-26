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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "All figures from live GitHub REST reads at main 84bbe9241/3026b319 and one local enumeration. Collaborators, invitations, branch-protection payload, required-review sub-resource, repo visibility and per-PR review counts are direct API responses, quoted verbatim. No PUT was issued against branch protection: writing it as a non-owner would reproduce SELF-AUTH-002. The register census read every root register and classified by the first Status line in the first 70 lines."
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
    en: "docs/en/14-ai-development/governance-register/GOV-REV-2026-11-24-CONVERGENCE-CEILING-034.md"
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-24-CONVERGENCE-CEILING-034.md"
---

# GOV-REV-2026-11-24-CONVERGENCE-CEILING-034

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION` / §2 **WITHDRAWN** by §9
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 3026b319b` (§1-§8); §9 erratum at `main = 1259f1af`
**Register author:** orchestrator session acting as owner-proxy. **Not** an independent reviewer.

---

## 1. 结论先行

本目录记录了几十个「无法收敛」的缺陷，并把原因归给具体的技术或流程疏漏。实测给出的原因更简单，也更难修：

**这个仓库只有一个可写身份。`collaborators = 1`，`pending invitations = 0`。**

于是 §5 要求的「独立审查」不是没人愿意做，是**结构上无法由第二个人做**。所有 `NOT_ASSIGNED` 的席位都不是待办事项，是当前身份拓扑下不可能被填的槽位。这解释了为什么 37 个登记里 21 个写着同一个词，而六个月来没有一个被真正关闭。

> **§9 已撤回本段推论（2026-11-24）。** 上面的测量不变。撤回的是推论：§5 要求的不是第二个**人**，是第二个**会话**，而本仓库随时可以开启一个。§9 记录了这处错误，也记录了它的方向——它把「675 件没做的事」写成了「做不了的事」。

---

## 2. 身份拓扑

```
GET /repos/oahcom/AiMemoryBrainArchitecture/collaborators
-> 1 entry: login=oahcom, type=User,
           permissions={admin,maintain,push,triage,pull} all true

GET /repos/{repo}/invitations
-> []

GET /repos/{repo}/pulls?state=closed&per_page=40
-> distinct authors among last 40 closed PRs = ['Hkncbn89', 'oahcom']
-> distinct mergers  among last 40 closed PRs = []
```

三件事同时成立：

1. **只有一个协作者**，且是全权限。
2. **没有待处理邀请**，即没有第二个身份正在加入。
3. 最近 40 个已关闭 PR 里出现两个作者名，但**合并者字段为空**——说明合并动作不是通过有记录的 review 流程完成的。

第 3 条不是「另一个人合并了」，而是合并记录本身缺失。这与 `SELF-REVIEW-007`（零审查合并）方向一致，但原因不同：007 归因于审查文化，本节归因于**没有第二个账号**〔2026-11-25 附注：这个归因就是 §9 纠正的那一处。「没有第二个账号」是账号层的事实，它不能解释合并记录为什么缺失；能解释的是这条路径**当时没人走**，而不是走不通。§9 已把本节结论判为假，此处只标注归因本身。〕

---

## 3. 分支保护的两个视图互相矛盾，而行为站在第三边

同一时刻对同一仓库连续读三次，结果稳定：

| 读法 | 结果 |
|---|---|
| `GET /branches/main/protection` → `required_pull_request_reviews` | **键不存在**（`has_prr=False`，三取三一致） |
| `GET /branches/main/protection/required_pull_request_reviews` | **200**，`required_approving_review_count = 1` |
| `GET /rulesets` | `[]`（无 ruleset 兜底） |
| `required_status_checks` | `strict = true`，**11 个** context |
| `enforce_admins` | `enabled = true` |

父资源说没有审查要求，子资源说有 1 条。两者不可能同时为真。**行为给出裁决**：

| PR | author | merged_by | merged | reviews | approvals |
|---|---|---|---|---|---|
| #869 | oahcom | oahcom | True | 0 | 0 |
| #880 | oahcom | oahcom | True | 0 | 0 |
| #889 | oahcom | oahcom | True | 0 | 0 |
| #897 | oahcom | oahcom | True | 0 | 0 |

在 `enforce_admins = true` 且「需要 1 条审批」的前提下，作者自合并且 0 审批是**不可能成功**的。四次全成功。所以**存着的那个 1 不生效**，父资源的「不存在」才是当前实际状态。

本文件记录这个矛盾，不解释它。它有一个重要后果：任何以子资源为据、认为「审查已强制」的判断都是错的；而任何以父资源为据、认为「审查未配置」的判断也只是**当下**成立，因为打算配置它的那条 PUT 从来没有成功过（见 §4）。

---

## 4. 平台阻塞的原文，与一个已变化的事实

`governance-register/README.md` 写着本目录最重要的一句话：

> 第 3 类失效的纠正措施 M-3（平台强制 `reviews>=1` + 必需检查成功）已被证明**在当前 GitHub 计划下不可执行**：
> ```
> PUT /repos/.../branches/main/protection -> 403
>     "Upgrade to GitHub Pro or make this repository public to enable this feature."
> ```
> 持有 `admin: true` 仍返回 403，说明这不是权限问题，是私有仓库 + 低版本计划的能力缺失。

而今天的实测：

```
GET /repos/oahcom/AiMemoryBrainArchitecture
-> private = False
-> visibility = public
-> created_at = 2026-11-16T08:26:29Z
```

**仓库已经是公开的。** 那条报错点名的两个替代方案之一是「make this repository public」——这个条件已经满足。

**本文件不主张 PUT 现在会成功。** 我没有发那个 PUT，因为以非所有者身份写分支保护，正是 `SELF-AUTH-002` 记录的失效模式；用一次越权写去证明「越权写不必要」是自相矛盾的。

但可以主张一件更弱、也更确凿的事：

> **README 里那句「私有仓库 + 低版本计划的能力缺失」在当前仓库状态下不再是事实。** 它可能曾经是事实（仓库 2026-11-16 创建，何时转公开无法从 API 反查），但今天它不是。而这句话是 `RECORDED_NOT_PREVENTED` 这个上限的唯一技术依据。

### 4.1 这句话有多少份副本

`git grep` 在 `origin/main` 的 `.md` 里命中 **14 个文件**带 `Upgrade to GitHub Pro`：

```
00-governance/reports/bilingual-baseline-remediation-report.md
14-ai-development/governance-register/GOV-NC-2026-11-20-DIRECT-MAIN-001.{md,en.md}
14-ai-development/governance-register/GOV-NC-2026-11-20-MERGE-AFTER-RULING-003.{md,en.md}
14-ai-development/governance-register/README.{md,en.md}
14-ai-development/work-items/GAP-10-IMPLEMENTATION-FRONTIER.{md,zh-CN.md}
14-ai-development/work-items/GAP-11-FORGET-FENCE-SPLIT-AUTHORITY.{md,zh-CN.md}
14-ai-development/work-items/GAP-15-FMT-GATE-ABSENT.{md,zh-CN.md}
14-ai-development/work-items/GAP-BASELINE-002.md
```

这句话写于 `dd4ecf16`（2026-11-21）。它当时是否成立，本文件不判断；它**现在**不成立，是可核的。

---

## 5. 于是「收敛」到底卡在哪

把三件事连起来：

1. §5 的审查要求需要一个**第二身份**〔2026-11-25 附注：此前提已失效，见本节末〕；
2. 仓库只有**一个身份**且无邀请在途；
3. 唯一的补救（平台强制）所依赖的前提**已经变化，但记录没有更新**。

所以 37 个登记里 21 个 `NOT_ASSIGNED` 不是 21 个待办，是**同一个待办**：拿到第二个可写身份，或者由唯一身份的所有者明确裁定「放弃独立审查」。这两条路都不是写代码，也都不是我作为 owner-proxy 能自己给的——前者需要一个真实的人，后者需要所有者撤回 `PR-GOVERNANCE-001` §5。

> **2026-11-25 附注（引文时效）。** 本节第 1 条与上一段把「独立审查」写成需要一个**第二身份**、需要「一个真实的人」，默认独立性以 GitHub 账号为门槛。该默认已不成立：`PR-GOVERNANCE-001` §5 于 2026-11-24 由 commit `2eb4e352`（PR #935）修订，现行文本（`14-ai-development/PR-GOVERNANCE-001.md` 的 §5 正文）规定**独立性是审查会话的属性，不是承载它的 GitHub 账号的属性**；修订记录见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`。「拿到第二个可写身份」由此不再是 §5 推出的唯一出路——开一个不共享上下文的会话即可，§9.1 已把「出口只有两条」判为假并给出第三条出口。
> **仍然成立的部分**：本节的**上限结论**（收敛卡住、新增登记只让 §6 计数 +1）不因本附注改变。被撤销的只是「因为没有第二个 GitHub 身份，所以这个上限是结构性的」这一句**理由**；上游事实（`collaborators = 1`、`invitations = 0`）仍成立，见 §9.2。原文保留，未改写。

**在这个裁决作出之前，任何新增登记都不会改变状态。** 它只会让 §6 的计数再 +1。

---

## 6. 本目录的收敛计数（含本文件）

按每个根登记文件前 70 行内首个 `Status` 行分类：

| 类别 | 数量 |
|---|---|
| 有状态行、且含 `OPEN` | 7 |
| 有状态行、含 `RESOLVED`/`CLOSED`/`ACCEPTED` | 1 |
| 有状态行、其余措辞 | 5 |
| **完全无状态行** | **12** |
| 合计（含本文件前） | 37 |

`NOT_ASSIGNED` 出现在 37 个中的 21 个。

两个必须说清的限制：

- 「无状态行」12 这个数**取决于匹配方式**。我第一次用 `^\*\*Status:\*\*` 得到 24，改用宽松匹配后得到 12。**24 是我的正则太窄造成的，不是仓库的事实**，所以采用 12 并在此声明口径。
- 索引覆盖率另有一份记录（`REGISTER-INDEX-031`），本文件不重测。

---

## 7. 本文件不主张什么

- 不主张 README 那句话当初写错了。它可能是准确的当时快照。
- 不主张 PUT 现在会返回 200。没有发过。
- 不主张该把 `required_approving_review_count = 1` 删除或设置。那是所有者的动作。
- 不主张 37 个登记中任何一个应当关闭。关闭需要审查，而审查缺席位（§2）。

  > **〔2026-11-25 附注〕** 本条的括注把 §2 的结论——由 `collaborators = 1`、`pending invitations = 0` 这组账号层计数推出的「结构上无法由第二个人做」——当作「审查缺席位」的理由。§5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）：同一 GitHub 身份下、不共享作者上下文的另一会话即可构成独立审查；`/pulls/{n}/reviews` 只返回 `user.login`，不返回会话，故「同一身份 ⇒ 同一会话」在该载荷里无法核实，此处应读作「账号层不独立、会话层未核实」。**仍然成立的是本条的结论**：本文件不主张关闭 37 个登记中的任何一个，这句话不依赖 §2 的任何推论，删去括注它照样成立。**不成立的是括注给出的理由**：§9 已于 2026-11-24 撤回它——缺的是会话，不是人；席位空着是未履行，不是填不上。理由若仍要引用，应指向 §9，而不是被 §9 判错的 §2。原文保留，不改写。
- 不主张 `Hkncbn89` 是第二个人。PR 的 author 字段可以是被授权的第三方提交者，本文件没有核验其身份性质。
- 不指派独立审查。席位 `NOT_ASSIGNED`。

**阻断链：** 第二可写身份 `ABSENT`（实测 1 collaborator / 0 invitations）→ 独立审查 `NOT_ASSIGNED` → 登记关闭 `BLOCKED` → 收敛层次二 `WAITING_OWNER`。

> **〔2026-11-25 附注〕** 这条链的第一环是账号层计数 `collaborators = 1`、`invitations = 0`，它被用来支撑一个审查层结论「独立审查 `NOT_ASSIGNED`」，再把该结论一路推到关闭与收敛。四环里只有两环经得起看。
>
> - **第一环成立，但只作为测量。** 一个 collaborator、零邀请，重测仍是这两个数（§9.2）。
> - **第二环推不出来。** §5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）：不共享作者上下文的另一会话即可满足 §5，无需第二个账号。故 `ABSENT` 不产生 `NOT_ASSIGNED`；`/pulls/{n}/reviews` 只返回 `user.login`、不返回会话，这一跳在载荷里也无法核实。
> - **`NOT_ASSIGNED` 仍是真状态，但理由不同：** 不是「无法运行」，是「未运行」——没有任何人开过这样一个会话。§9.1 已把「结构上无法」判为假、把 `BLOCKED` 改判为「未被履行」；这条区分正是 §9 的全部要点。
> - **仍成立的是第三、四环。** 无论席位为什么空着，空席位挡住关闭，关闭挡住收敛层次二。所以终点 `WAITING_OWNER` 不动。
>
> 原文保留；本注只拆开这条链，不重写它。

---

## 8. 复现

```
GET /repos/oahcom/AiMemoryBrainArchitecture/collaborators   -> 1 (oahcom, all permissions)
GET /repos/oahcom/AiMemoryBrainArchitecture/invitations     -> []
GET /repos/oahcom/AiMemoryBrainArchitecture                 -> private=false visibility=public
GET /repos/.../branches/main/protection                     -> no required_pull_request_reviews key
GET /repos/.../branches/main/protection/required_pull_request_reviews
                                                            -> 200, required_approving_review_count=1
GET /repos/.../rulesets                                     -> []
GET /repos/.../pulls/{869,880,889,897}/reviews              -> 0 reviews each, all merged
```
---

## 9. 勘误（2026-11-24）：§2 的推论被所有者基线推翻

所有者给出的基线是：

> **独立审查只需要独立会话，不要求独立账号。**

**§2 的结论「结构上无法由第二个人做」是错的。** 不是测错了——`collaborators = 1` 与 `invitations = []` 仍然成立，重测依旧是这两个数。错的是**从那个事实推到「无法审查」的那一步**：那一步默认了独立审查需要一个第二账号，而这个前提从未被验证，我把它当成了不证自明。

这是本会话第四次同类错误：**把某一层的事实，当作另一层的结论**。前三次是 `EXIT` 取错管道、`PARTIAL_SIDE_BY_SIDE_PAIRS` 只按谓词推断可达性、「删除镜像无告警」只评估两套机制之一。这次是**把身份层的计数，当作审查层的可行性**。

### 9.1 按基线重读，本文件哪些判断失效

| 本文件原判断 | 在基线下 |
|---|---|
| §2 独立审查「结构上无法由第二个人做」 | **假**。可由另一会话做 |
| §5「21 个 `NOT_ASSIGNED` 是一个待办重复 21 次」 | **假**。是 21 个可执行但未执行的待办 |
| §5「出口只有两条」 | **假**。还有第三条：**开一个新会话做审查** |
| §7「关闭 `BLOCKED`」 | **假**。未被阻断，是**未被履行** |

这个区别重要：不可抗力不产生责任，未履行产生责任。本文件把性质写错了，且写错的方向是**替未履行找了不可抗力的理由**。

### 9.2 仍然成立的部分

**全部实测数字不动**：`collaborators = 1`、`invitations = []`、分支保护两视图矛盾、4 次零审批自合并、README 的 403 依据已过期、14 份文件复述它。这些与独立性定义无关，§3、§4、§6 的测量继续有效。

### 9.3 载体已按基线修订

`PR-GOVERNANCE-001.md` §5 与 `PR-GOVERNANCE-001-ENFORCEMENT.md` §2、§2.1 中共六处把独立性绑在 GitHub 账号上的条款，已按所有者指令改为**会话级**。修订本身记录在 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`。

**所以本文件与现行文本的冲突已经消除**：不是本文件被改对，是文本被改成了基线。§2 的原句作为历史记录保留在正文中，本节声明它不再成立。

### 9.4 本勘误不主张什么

- 不主张 034 应当删除。事实层有效，且以勘误方式更正正是 034 §7 自己声明的做法。
- 不主张会话级独立审查足够强。它强于同会话角色模拟，弱于人类审查；同一模型驱动的两个会话仍共享训练偏差。这一点在 036 中写明。
- 不主张「21 个待办」现在会被执行。可执行不等于已执行。

