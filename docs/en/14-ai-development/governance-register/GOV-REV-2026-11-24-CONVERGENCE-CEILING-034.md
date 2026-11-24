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
      last_verification_note: "All figures from live GitHub REST reads at main 84bbe9241/3026b319 and one local enumeration. Collaborators, invitations, branch-protection payload, required-review sub-resource, repo visibility and per-PR review counts are direct API responses, quoted verbatim. No PUT was issued against branch protection: writing it as a non-owner would reproduce SELF-AUTH-002. The register census read every root register and classified by the first Status line in the first 70 lines."
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
    source: "14-ai-development/governance-register/GOV-REV-2026-11-24-CONVERGENCE-CEILING-034.md"
    en: null
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

第 3 条不是「另一个人合并了」，而是合并记录本身缺失。这与 `SELF-REVIEW-007`（零审查合并）方向一致，但原因不同：007 归因于审查文化，本节归因于**没有第二个账号**。

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

1. §5 的审查要求需要一个**第二身份**；
2. 仓库只有**一个身份**且无邀请在途；
3. 唯一的补救（平台强制）所依赖的前提**已经变化，但记录没有更新**。

所以 37 个登记里 21 个 `NOT_ASSIGNED` 不是 21 个待办，是**同一个待办**：拿到第二个可写身份，或者由唯一身份的所有者明确裁定「放弃独立审查」。这两条路都不是写代码，也都不是我作为 owner-proxy 能自己给的——前者需要一个真实的人，后者需要所有者撤回 `PR-GOVERNANCE-001` §5。

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
- 不主张 `Hkncbn89` 是第二个人。PR 的 author 字段可以是被授权的第三方提交者，本文件没有核验其身份性质。
- 不指派独立审查。席位 `NOT_ASSIGNED`。

**阻断链：** 第二可写身份 `ABSENT`（实测 1 collaborator / 0 invitations）→ 独立审查 `NOT_ASSIGNED` → 登记关闭 `BLOCKED` → 收敛层次二 `WAITING_OWNER`。

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

## 1. The finding first

This directory records dozens of defects that "cannot converge", attributing each to a specific technical or procedural lapse. Measurement gives a simpler cause, and a harder one to fix:

**This repository has exactly one write identity. `collaborators = 1`, `pending invitations = 0`.**

So the independent review §5 requires is not unwanted — it is **structurally impossible for a second person to perform**. Every `NOT_ASSIGNED` seat is not a to-do item; it is a slot that the current identity topology cannot fill. That explains why 21 of 37 registers carry the same word and none has been genuinely closed in six months.

> **Withdrawn by §9 (2026-11-24).** The measurement above stands unchanged. The inference does not: §5 does not require a second *person*, it requires a second *session*, and this repository can always open one. §9 records the error and, more usefully, its direction — it turned “675 things not done” into “things that cannot be done”.

## 2. Identity topology

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

Three things hold at once: only one collaborator, with full permissions; no pending invitation, so no second identity is joining; and the merger field is empty across the last 40 closed PRs, meaning the merge action was not completed through a recorded review flow. The third is not "another person merged" — it is that the merger record is missing. That matches the direction of `SELF-REVIEW-007` (zero-review merges) but not its cause: 007 attributes it to review culture; this section attributes it to there being no second account.

## 3. Two branch-protection views contradict each other; behaviour sides with neither

Read three times in a row at the same moment, stable:

| Read | Result |
|---|---|
| `GET /branches/main/protection` → `required_pull_request_reviews` | **key absent** (`has_prr=False`, 3 of 3) |
| `GET .../protection/required_pull_request_reviews` | **200**, `required_approving_review_count = 1` |
| `GET /rulesets` | `[]` (no ruleset fallback) |
| `required_status_checks` | `strict = true`, **11** contexts |
| `enforce_admins` | `enabled = true` |

The parent says no review requirement; the child says one approval. Both cannot be true. **Behaviour adjudicates**: #869, #880, #889, #897 each had 0 reviews, 0 approvals, and all merged, all self-merged by the author. With `enforce_admins = true` and a one-approval rule, that is impossible. So the stored `1` is not in force, and the parent's absence is the operative state.

This file records the contradiction, it does not explain it. The consequence matters: any judgement that "review is now enforced", based on the sub-resource, is wrong; and any judgement that "review is not configured", based on the parent, is true only *now*, because the PUT that would configure it has never succeeded (§4).

## 4. The blocked-platform quotation, and one fact that has changed

`governance-register/README.md` carries the directory's most load-bearing sentence: corrective measure M-3 (platform-enforced `reviews>=1` plus required checks) "has been proven **inexecutable under the current GitHub plan**", quoting `PUT /repos/.../branches/main/protection -> 403 "Upgrade to GitHub Pro or make this repository public to enable this feature."`, and concluding that holding `admin: true` and still getting 403 means the limitation is *private repository on a low plan*.

Today:

```
GET /repos/oahcom/AiMemoryBrainArchitecture
-> private = False, visibility = public, created_at = 2026-11-16T08:26:29Z
```

**The repository is already public.** One of the two alternatives the error message names — "make this repository public" — is satisfied.

**This file does not claim the PUT would now succeed.** I did not issue it, because writing branch protection as a non-owner is precisely the failure mode `SELF-AUTH-002` records; using an unauthorised write to prove that an unauthorised write is unnecessary would be self-contradictory.

What can be claimed is weaker and certain: **the README's "private repository plus low plan" is no longer a fact of this repository.** It may have been a fact when written (the repo was created 2026-11-16; when it became public is not recoverable from the API), but it is not one today — and that sentence is the only technical basis for the `RECORDED_NOT_PREVENTED` ceiling.

### 4.1 How many copies that sentence has

`git grep` over `.md` on `origin/main` finds `Upgrade to GitHub Pro` in **14 files**: the bilingual remediation report; `DIRECT-MAIN-001` and `MERGE-AFTER-RULING-003` (both sides); `README` (both sides); `GAP-10`, `GAP-11`, `GAP-15` (both sides); and `GAP-BASELINE-002`. It was written in `dd4ecf16` (2026-11-21). Whether it held then, this file does not judge; that it does not hold now is verifiable.

## 5. So where does convergence actually stall

Join the three: §5's review requirement needs a **second identity**; the repository has **one** with no invitation in flight; and the only remedy (platform enforcement) rests on a premise that **has changed while the record did not**.

So 21 `NOT_ASSIGNED` entries are not 21 to-dos. They are **one** to-do: obtain a second write identity, or have the sole owner explicitly rule that independent review is waived. Neither is code, and neither is something I as owner-proxy can supply — the first needs a real person, the second needs the owner to withdraw `PR-GOVERNANCE-001` §5.

**Until that ruling exists, no new register changes the state.** It only increments §6 by one.

## 6. Convergence census (including this file)

Classified by the first `Status` line within the first 70 lines of each root register: 7 `OPEN`; 1 `RESOLVED`/`CLOSED`/`ACCEPTED`; 5 other wording; **12 with no status line**; 37 total before this file. `NOT_ASSIGNED` appears in 21 of 37.

Two limits that must be stated: the "12 with no status line" figure **depends on the matching method** — my first pass with `^\*\*Status:\*\*` gave 24, a looser match gave 12. **24 was my regex being too narrow, not a fact about the repository**, so 12 is used with the method declared. Index coverage is recorded separately in `REGISTER-INDEX-031` and is not re-measured here.

## 7. What this file does not claim

Not that the README sentence was wrong when written. Not that the PUT would now return 200 — it was never issued. Not that `required_approving_review_count = 1` should be deleted or set; that is the owner's action. Not that any of the 37 registers should close; closure needs review, and review lacks a seat (§2). Not that `Hkncbn89` is a second person — a PR author field can be an authorised third-party committer, and its nature was not verified. No independent review is assigned; the seat is `NOT_ASSIGNED`.

**Blocking chain:** second write identity `ABSENT` (measured 1 collaborator / 0 invitations) → independent review `NOT_ASSIGNED` → register closure `BLOCKED` → convergence layer 2 `WAITING_OWNER`.

## 8. Reproduction

Same six read-only requests as the Chinese section: collaborators, invitations, repo visibility, the parent protection payload, the required-review sub-resource, rulesets, and the review lists for four merged PRs.
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

