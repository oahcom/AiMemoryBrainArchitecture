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
    en: "docs/en/14-ai-development/governance-register/GOV-REV-2026-11-24-CONVERGENCE-CEILING-034.md"
    zh-CN: null
---

# GOV-REV-2026-11-24-CONVERGENCE-CEILING-034

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = 3026b319b`, GitHub REST as of 2026-11-24T08:5xZ
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
