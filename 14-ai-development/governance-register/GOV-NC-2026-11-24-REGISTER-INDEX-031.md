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
      last_verification_note: "Every count in this register came from a script run in this session against main aae8b25b8: the 33-register list came from git ls-tree; the status tokens from a regex sweep of each root file; the README coverage from substring matching each register id against README.md; the three behavioural measurements ran scripts/check_bilingual_docs.py in a throwaway worktree on real commits; the PR #869 review count came from the GitHub REST API. No figure is carried over from another register."
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
    en: "docs/en/14-ai-development/governance-register/GOV-NC-2026-11-24-REGISTER-INDEX-031.md"
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-24-REGISTER-INDEX-031.md"
---

# GOV-NC-2026-11-24-REGISTER-INDEX-031

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = aae8b25b8`
**Register author:** orchestrator session acting as owner-proxy. **Not** an independent reviewer, **not** the accountable owner.

---

## 1. 结论先行

登记中心有 33 份登记。README 的「登记清单」列出其中 **11** 份，其余 **22** 份在唯一的索引里不存在。状态字段是自由文本，33 份里 **10 份没有状态行**，有状态行的用了 **14 种互不相同的状态词**，另有一份登记把编号写进了状态字段。

后果是可测量的，不是推测的：**三份登记连续两天写着错误的状态，而没有任何机制能发现**，因为

1. 它们不在索引里（`011`、`021`、`007` 三份全部不在那 11 份之中）；
2. 即使被看见，状态列是散文，没有可比对的取值集合；
3. 没有任何闸门读取登记状态——`check_bilingual_docs.py` 与 `check_document_management.py` 都不碰它。

本文件补充两件事：一份**覆盖全部 33 份**的表，以及三份登记的实测更正。它不提出实现，不授权合并。

---

## 2. 覆盖缺口（实测）

| 量 | 值 | 来源 |
|---|---|---|
| `governance-register/` 根目录登记数 | **33** | `git ls-tree` @ `aae8b25b8` |
| README「登记清单」点名数 | **11** | 逐 id 子串匹配 `README.md` |
| **不在索引中** | **22** | 差集 |
| README 表格行数 | 12 | `^\| \`ID\`` 匹配 |
| README 有行、无对应文件 | **1** | `OWNER-DECISION-REVIEW-INDEPENDENCE-001` |

不在索引中的 22 份包括本系列最核心的几份：

```
GOV-NC-2026-11-21-REGRESSION-009      GOV-NC-2026-11-21-SPLIT-DOMAIN-011
GOV-NC-2026-11-21-SELF-REVIEW-007     GOV-NC-2026-11-22-ENUM-BOUNDARY-021
GOV-NC-2026-11-21-GATE-DEADLOCK-006   GOV-REV-2026-11-21-PARTIAL-SCOPE-019
GOV-NC-2026-11-21-PAIRING-RESIDUAL-013 GOV-NC-2026-11-21-EMBEDDED-ROOT-015
GOV-NC-2026-11-21-SUFFIX-SCOPE-017    GOV-NC-2026-11-21-CWD-SPLIT-014
GOV-REV-2026-11-21-GATE-MUTANTS-016   GOV-NC-2026-11-20-CI-NOT-EXECUTED-005
   … 共 22 份，完整清单见 §5
```

索引不是「粗略」，是**三分之一**。

---

## 3. 状态字段被三种语义共用

把 33 份的状态行逐字取出，得到 14 个状态词。它们不属于同一个轴：

**轴 A — 生命周期状态（可迁移）**

| 词 | 次数 | 含义 |
|---|---|---|
| `OPEN` | 13 | 未处置 |
| `RULED` | 1 | 已裁定，实施待办 |
| `DISPATCHED` | 1 | 已发派工单 |
| `FIXED-UNGUARDED` | 1 | 已修，无回归测试 |
| `FIXED-CLOSED-BY-OTHER` | 1 | 被他路修复 |
| `RESOLVED_ON_MAIN` | 1 | 主干实测已解除 |
| `ACCEPTED` | 2 | 已承认，未修 |

**轴 B — 登记性质（不迁移）**

`MEASUREMENT_ONLY`（2）、`NO_IMPLEMENTATION`（1）、`SELF_REVIEW_IDENTIFIED`（1）

**轴 C — 残留条件（依附于 A）**

`NOT_REMEDIATED`（4）、`NOT_ASSIGNED`（4）、`CI_NOT_EXECUTED`（1）、`ACTIVE`（2）

**还有第三类：编号被写进了状态字段。**

`AID-2026-054`（2）、`OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025`（1）、`GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER`（1）

**这就是全部机制问题的根源**：一个字段承载三个轴，所以任意两份登记的状态字符串都不可比。`OPEN / NOT_REMEDIATED` 与单独的 `OPEN` 表达同一件事，却看起来不同；`MEASUREMENT_ONLY` 根本不是状态，却占着状态的位置。任何闸门都无法在没有取值集合的前提下校验它，于是没有闸门校验它，于是它出错时无人知晓。

`ENUM-BOUNDARY-021` 这份登记的名字里就有 enum——它记录的是双语闸门的枚举边界。登记中心自己没有枚举。这条对照不需要加工。

---

## 4. 三份登记的实测更正

三份都写入于错误尚不存在或尚未被发现的时刻；它们不是造假的产物，是**没有复检触发点**的产物。

### 4.1 `SPLIT-DOMAIN-011` — 写入时正确，1 小时 42 分后失效

| 项 | 值 |
|---|---|
| 登记测量点 | `main = cb04524`，2026-11-21 **18:48:20** +0800 |
| 该点 `check_normative_pairing()` 函数体 | **30 行**，不含 `side_by_side_partner` |
| 修复提交 | `5f109308d`，2026-11-21 **20:30:42** +0800 |
| 该提交后函数体 | **51 行**，含 `side_by_side_partner` |

所以 §1「14-ai-development 通过、其余八根失败」在 `cb04524` 上**为真**。现在的实测：

| 用例（真实 PR-diff 形态，`BASE_SHA = HEAD~1`） | `EXIT` |
|---|---|
| `02-domain-model/….zh-CN.md` 只改一侧 | **1** |
| `02-domain-model/….zh-CN.md` + `….md` 两侧都改 | **0** |
| `14-ai-development/AI-EXEC-INDEPENDENCE-RULING-001.en.md` 只改一侧 | **1** |
| 同上一对，两侧都改 | **0** |

**两侧行为一致。** §1 的不对称已不存在。§2「死锁没有合法出口」同时失效——出口是「两侧都改」，不需要伪造七字段例外。

§4 的镜像回归也已不在：构造「中文源 + `docs/en` 镜像、无 `docs/zh-CN`」，

| 根 | `EXIT` | 判定 |
|---|---|---|
| `02-domain-model/hm.md` | **2** | `New bilingual gap outside frozen baseline` —— 正确判为缺口 |
| `14-ai-development/hm.md` | **0** | Shape 3 合法形态 —— 正确接受 |

Shape 3 分支已重新限定在 `14-ai-development/`。

**本文件不推断 `5f109308d` 的作者是否知道 011 存在。**只记录时间关系：登记写于 18:48，修复合入于 20:30，登记此后未再被触碰。

### 4.2 `ENUM-BOUNDARY-021` — 登记与修复是同一个 commit

| 项 | 值 |
|---|---|
| 状态行 | `OPEN — Awaiting implementation and independent verification` |
| 该登记文件的引入提交 | `8ab40fb4f`，2026-11-22 10:37:32 +0800 |
| 同一提交同时改了 | `scripts/check_bilingual_docs.py`（+186/−46） |

登记和它要求的实现**一起合入**。状态行从未更新。

两项缺陷的实测（`main = aae8b25b8`，临时 worktree）：

| 主张 | 实测 | 结论 |
|---|---|---|
| `current_bilingual_gaps()` 用文件系统递归，会收进未跟踪文件 | 在 `00-governance/` 写入未跟踪 `PHANTOM-UNTRACKED-PROBE.md`，扫描结果 **不含**该路径，缺口集仍为 **77** | 已修：`git ls-files` 为唯一枚举权威 |
| `write_baseline()` 不校验工作树 | 存在未跟踪文件时返回 **2**，打印 `working tree is not clean; ?? 00-governance/DIRTY-PROBE.md` | 已修：dirty tree 拒绝写入 |

「实现已完成、独立验证未完成」是本登记的真实残留；「Awaiting implementation」不是。

### 4.3 `SELF-REVIEW-007` — 没有失效，由我本人再次证实

状态 `ACCEPTED / SELF_REVIEW_IDENTIFIED / S-2 APPROVED_IN_PRINCIPLE / IDENTITY_NOT_ASSIGNED` 是准确的。用它自己的量具量我自己的合并：

| 字段 | PR #869 |
|---|---|
| author | `oahcom` |
| merged_by | `oahcom` |
| reviews | **0** |
| APPROVED | **0** |
| 末 commit → merge | **115 秒** |

007 的表格测到的是 13 s / 40 s。115 秒更长，但没有任何一项结构性条件改变：**一个可写身份，作者即合并者，零批准**。

> **〔2026-11-25 附注〕** 本句把「一个可写身份」与「作者即合并者」——两项账号层事实——列为判定该次合并独立性的「结构性条件」，并以二者未变推出「没有任何一项结构性条件改变」。§5 已于 2026-11-24 由 `2eb4e352`（PR #935）修订为会话层判据（见 `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`）：同一 GitHub 身份下的另一会话即可构成独立审查。`/pulls/{n}/reviews` 只返回 `user.login`，不返回会话，故「同一身份 ⇒ 同一会话」这一步在该载荷里无法核实。此处应读作「账号层不独立、会话层未核实」。**仍然成立的是「零批准」**：它是 `APPROVED` 的计数，与 §5 的版本无关——没有任何一版 §5 会把 `COMMENTED` 审查变成批准，所以 #869 的 `APPROVED = 0` 独立成立，且它本身已足以说明该次合并没有取得批准。**同样成立的是** 115 秒这一间隔测量。**不成立的是**把「一个可写身份 / 作者即合并者」当作独立性判据的结构条件——身份相等不再蕴含会话相等，「条件未变」因此不能覆盖独立性一项。

因此 007 不是待更正的登记，是**待处置而被外部阻塞的登记**。README §「一个必须记录的边界」已实测 `PUT /branches/main/protection` 返回 403（私有仓库 + 计划不支持），所以「技术上阻止」这条路在该仓库当前状态下不存在。此点仍成立，本文件不重复测量。

---

## 5. 完整清单（33 份，逐份实测两个布尔量）

「状态行」= 文件是否含 `状态:` / `Status:` 字段。「在索引」= README 是否点名。

| # | 登记 | 状态行 | 在索引 |
|---|---|---|---|
| 1 | `GOV-NC-2026-11-20-DIRECT-MAIN-001` | 有 | 是 |
| 2 | `GOV-NC-2026-11-20-SELF-AUTH-002` | 有 | 是 |
| 3 | `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` | 有 | 是 |
| 4 | `GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004` | 有 | **否** |
| 5 | `GOV-NC-2026-11-20-CI-NOT-EXECUTED-005` | 有 | **否** |
| 6 | `GOV-NC-2026-11-21-GATE-DEADLOCK-006` | 有 | **否** |
| 7 | `GOV-NC-2026-11-21-SELF-REVIEW-007` | 有 | **否** |
| 8 | `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` | 有 | **否** |
| 9 | `GOV-NC-2026-11-21-REGRESSION-009` | 有 | **否** |
| 10 | `GOV-NC-2026-11-21-DEV-PR-GATE-010` | **无** | **否** |
| 11 | `GOV-NC-2026-11-21-SPLIT-DOMAIN-011` | **无** | **否** |
| 12 | `GAP-EXEC-2026-11-21-012` | **无** | **否** |
| 13 | `GOV-NC-2026-11-21-PAIRING-RESIDUAL-013` | 有 | **否** |
| 14 | `GOV-NC-2026-11-21-CWD-SPLIT-014` | 有 | **否** |
| 15 | `GOV-NC-2026-11-21-EMBEDDED-ROOT-015` | 有 | **否** |
| 16 | `GOV-REV-2026-11-21-GATE-MUTANTS-016` | 有 | **否** |
| 17 | `GOV-NC-2026-11-21-SUFFIX-SCOPE-017` | 有 | **否** |
| 18 | `GAP-EXEC-2026-11-21-018` | 有 | **否** |
| 19 | `GOV-REV-2026-11-21-PARTIAL-SCOPE-019` | 有 | **否** |
| 20 | `GOV-NC-2026-11-21-GATE-CLOSURE-020` | **无** | **否** |
| 21 | `GOV-NC-2026-11-22-ENUM-BOUNDARY-021` | 有 | **否** |
| 22 | `GAP-EXEC-2026-11-22-PHASE2-RESIDUAL-022` | **无** | **否** |
| 23 | `GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023` | 有 | **否** |
| 24 | `GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024` | 有 | **否** |
| 25 | `GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` | 有 | 是 |
| 26 | `GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027` | **无** | 是 |
| 27 | `GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028` | **无** | 是 |
| 28 | `GOV-NC-2026-11-23-EXECUTION-RESTORED-029` | 有 | 是 |
| 29 | `GOV-NC-2026-11-23-UNREACHABLE-GUARD-030` | 有 | 是 |
| 30 | `GOV-NC-CONVERGENCE-2026-11-20` | 有 | 是 |
| 31 | `GOV-REV-2026-11-21-PR425-001` | **无** | **否** |
| 32 | `TEST-DRAFT-2026-11-21-PR425-M3` | **无** | **否** |
| 33 | `EX-20261123-01` | **无** | 是 |

无状态行的 10 份：`DEV-PR-GATE-010`、`SPLIT-DOMAIN-011`、`GAP-EXEC-012`、`GATE-CLOSURE-020`、`GAP-EXEC-022`、`PROVENANCE-REFERENCE-REVALIDATION-027`、`PROVENANCE-GRAPH-ADD-SIGNATURE-028`、`PR425-001`、`PR425-M3`、`EX-20261123-01`。

---

## 6. 建议的最小取值集合（不授权，仅提议）

把 §3 的三轴拆成三个字段，各自取值有限：

```
lifecycle:  OPEN | RULED | DISPATCHED | FIXED | RESOLVED | CLOSED
nature:     DEFECT | MEASUREMENT | DECISION | EXCEPTION
residual:   NONE | NOT_REMEDIATED | NOT_ASSIGNED | UNGUARDED | UNVERIFIED
```

`MEASUREMENT_ONLY`、`NO_IMPLEMENTATION` 归入 `nature`；`NOT_REMEDIATED`、`NOT_ASSIGNED` 归入 `residual`；编号引用移出状态字段，进入 `dispatch:` 字段。

**本文件不自授权这份方案。**它需要 Owner 裁定，或另立工单；签发权限不在本会话。记录在此的唯一目的是让下一位读者不必再从 33 份散文里重建取值集合。

---

## 7. 本文件没有做的事

- 没有修改 `011`、`021`、`007` 的状态行。它们仍然写着本文 §4 判定为过期或已证实的字面值。改它们需要动 3 份文件 × 3 种语言副本，而本文件已经载明真相；先补状态行还是先立取值集合，是 Owner 的选择，不是我的。
- 没有为 22 份缺失登记补 README 行。补 22 行需要逐份判定严重度与规模，那是重写索引，不是补索引。
- 没有测未列入 §4 的 30 份登记的技术主张是否仍成立。它们的「状态行/在索引」是机械可测的，本文测了；它们的技术结论不是，本文没有测，也没有写成任何形态的判定。
- 没有声称任何闸门因本文件而改变行为。`check_bilingual_docs.py` 与 `check_document_management.py` 都不读取登记状态，本文件不改变这一点。
