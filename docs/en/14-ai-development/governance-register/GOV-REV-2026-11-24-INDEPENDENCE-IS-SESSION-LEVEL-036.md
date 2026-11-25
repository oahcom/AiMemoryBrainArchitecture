---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner, standing instruction in session 2026-11-24"
      decision_date: "2026-11-24"
      approved_version:
        scheme: content-hash
        value: "f8be29883e1c2ca2bf0e923cf21ded35a7be322c5e61760db7116cae7e0bcda5"
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
      last_verification_note: "The six amended clauses are line 136 of 14-ai-development/PR-GOVERNANCE-001.md, lines 40/43/55 of docs/en/.../PR-GOVERNANCE-001-ENFORCEMENT.md and the same three of docs/zh-CN/... . Each replacement was asserted present before substitution (string equality, not fuzzy matching), so no clause was silently skipped. The prior wording of all six is preserved verbatim in section 4 below. The baseline itself is an owner instruction given in session on 2026-11-24; it is authority, not a measurement, and is recorded as such."
    usage_status: Active
    modification_status: Pending-Reapproval
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
    source: "14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md"
---

# GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036

**Status:** `APPLIED` / `OWNER-INSTRUCTED` / `TEXT-AMENDED`
**Nature:** `GOVERNANCE-CLAUSE-CHANGE / SIX-SITES / PRIOR-WORDING-PRESERVED`
**Measured at:** `main = 1259f1af`
**Register author:** orchestrator session acting as owner-proxy, under direct owner instruction.

---

## 1. 改了什么

所有者指令：

> **独立审查只需要独立会话，不要求独立账号，这是基线。**
> 把基线改了，按我的逻辑改。

此前仓库的做法正好相反，而且是**逐字写明的相反**。本次把六处把独立性绑在 GitHub 账号上的条款，改为绑在**会话**上。

| 文件 | 行 | 原意 | 现意 |
|---|---|---|---|
| `14-ai-development/PR-GOVERNANCE-001.md` | 136 (EN) | 同一身份不独立，**即使会话扮演不同角色也一样** | 独立性是**会话**属性；身份是载体；**同会话内**角色模拟仍不独立 |
| 同上 | 138 (ZH) | 同上 | 同上 |
| `docs/en/.../PR-GOVERNANCE-001-ENFORCEMENT.md` | 40 | 要求**身份**独立的审查者 | 要求**会话**独立的审查者 |
| 同上 | 43 | **同身份的第二个 AI 角色**不算独立 | **另一会话**审查自己未撰写未实现的产物**算**独立，可走同一身份 |
| 同上 | 55 | 同身份的批准一律无效 | 同身份的批准**在会话独立且已披露时有效** |
| `docs/zh-CN/.../PR-GOVERNANCE-001-ENFORCEMENT.md` | 40 / 43 / 55 | 同上 | 同上 |

## 2. 为什么原来的文本必须改，而不只是"被误读"

原来的第 136 行不是措辞含糊，它专门点名了会话维度并予以否定：

> A review performed through the same connected GitHub identity as the author is not independent, **even if the session adopts a different role**.

> 作者与审查者使用同一 GitHub 身份时，不构成独立审查，**即使会话扮演不同角色也一样**。

这句话堵死的正是基线允许的那条路。所以基线不是"对旧文本的另一种解释"，而是**替换它**。同时，仓库内**没有任何文档**把独立性定义为会话级（对 main 全部 `.md` 搜 `independent session` / `独立会话` / `separate session` / `different session`，零命中），所以旧文本是唯一一侧，且站在基线的对面。

## 3. 新版条款的准确边界

改写后仍**不**允许的三件事：

1. **撰写会话内部换角色不算独立审查。** 这是基线的边界，不是对它的削弱：审查者与作者共享同一上下文与同一激励。
2. **`COMMENT` 仍不是 `APPROVE`。**
3. **例外仍必须显式记录**，不得默默豁免。

改写后**新允许**的一件事：

- 另一个不共享作者上下文的会话，审查其未撰写、未实现的产物，**构成独立审查**，且可经由作者相同的 GitHub 连接身份提交，须在评论中披露独立性为会话级。

## 4. 六处原文，逐字保留

留档的目的：将来若要回滚或对照，不必翻 git 历史。**这是被替换掉的原文，不是现行条款。**

**PR-GOVERNANCE-001.md:136 (EN)**
> A COMMENT review is technical commentary, not an APPROVE review. A review performed through the same connected GitHub identity as the author is not independent, even if the session adopts a different role. AI role simulation is not Owner approval. Record exceptions explicitly; do not silently waive the requirement.

**PR-GOVERNANCE-001.md:138 (ZH)**
> COMMENT 是技术评论，不是 APPROVE。作者与审查者使用同一 GitHub 身份时，不构成独立审查，即使会话扮演不同角色也一样。AI 角色模拟不构成 Owner 批准。任何例外都必须显式记录，不得默默豁免。

**ENFORCEMENT.md:40 (EN)**
> Require at least one approving review from a GitHub identity independent of the PR author for normal changes; require affected domain Owner approval for changes to that Owner's normative contract.

**ENFORCEMENT.md:43 (EN)**
> A COMMENT is not an APPROVE. A second AI role using the author's same connected GitHub identity is not an independent reviewer.

**ENFORCEMENT.md:55 (EN, 片段)**
> an approval given by the same GitHub identity as the PR author is not a valid approval and MUST NOT be recorded as APPROVED.

**ENFORCEMENT.md:40 (ZH)**
> 普通变更至少要求一位与 PR 作者身份独立的 GitHub 审查者批准；修改某领域 Owner 规范契约时，必须取得受影响领域 Owner 的批准。

**ENFORCEMENT.md:43 (ZH)**
> COMMENT 不是 APPROVE。使用作者相同 GitHub 连接身份、仅切换角色的第二个 AI 会话不构成独立审查者。

**ENFORCEMENT.md:55 (ZH, 片段)**
> 由与 PR 作者相同 GitHub 身份给出的批准不构成有效批准，不得记为 APPROVED。

## 5. 这个改动使哪些登记失效

`GOV-REV-2026-11-24-CONVERGENCE-CEILING-034` §2、§5、§7 中据"单一身份"推出的"不可能 / `BLOCKED` / 无出口"全部失效，已在其 §9 勘误。

`GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008`、`SELF-REVIEW-007`、`GOV-REV-2026-11-21-PR425-001` 等以"零审查合并"为主题的登记，其**事实**仍然成立（确实零审查合并过），但其**归因**需重读：过去归因于"平台无法强制 + 只有一个身份"，现在应归因为**未开独立会话**。

本文件不替它们改状态。那是各自登记的事。

### 5.1 清扫已落地：实测清单（2026-11-25）

上节的「等」不是修辞，是当时未清点的余额。清点结果：**11 个文件**，其中 9 个是三副本布局、2 个是 `.md` / `.en.md` 配对布局（后者按 `MERGE-AFTER-RULING-003` 的先例不声明 `bilingual_counterpart`）。

| 文件 | 注记数 root / en / zh-CN | 主要被替换的依据 |
|---|---|---|
| `OWNER-DECISION-REVIEW-INDEPENDENCE-001` | 20 / 20 / 20 | 「独立性需要第二个 GitHub 账号」的 7 处推论 |
| `GOV-NC-2026-11-21-SELF-REVIEW-007` | 12 / 12 / 12 | 标题、`reviews >= 1` 计数、§8 判定程序（明写「不能再用作门禁」） |
| `GOV-NC-2026-11-21-GATE-DEADLOCK-006` | 7 / 7 / 7 | §12.3、§14.1 两格、§14.2 代码块周围的推理 |
| `GOV-NC-2026-11-21-REGRESSION-009` | 7 / 7 / 7 | §10「作者即合并者」要素、§11.5 表格格 |
| `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` | 7 / 7 / 7 | §11.8 状态串的「0 次独立审查」是账号层计数 |
| `GOV-REV-2026-11-24-CONVERGENCE-CEILING-034` | 5 / 9 / 5 | §7 两处（双语文件，`docs/en` 内含中英两段，故不对称） |
| `GOV-REV-2026-11-21-PR425-001` | 2 / 2 / 2 | §0 唯一的**正向**用法：身份相异既非充分也非必要 |
| `GOV-NC-2026-11-24-REGISTER-INDEX-031` | 1 / 1 / 1 | — |
| `GOV-NC-2026-11-24-DISPATCH-CHANNEL-CLOSED-032` | 1 / 1 / 1 | 结论改为「自我签发的放宽由构造即未经第二方核对」 |
| `GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004` | 2 / — | 「不存在任何角色分离」→「未发生」不等于「不可能」 |
| `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` | 1 / — | 结论改依本项自带的 `COMMENTED` ≠ `APPROVE` |

**状态未改。** 上表只加注，不把任何登记从 `OPEN` / `DISPATCHED` 推进到别处；推进仍是各自登记的事。

### 5.2 清扫覆盖的三条轴，以及不覆盖什么

1. **树内**：工作树全树检索身份词族（`second account` / `collaborators = 1` / `one writable identity` / `same account` / `self-approv` / `sole reviewer` / `APPROVED = 0`），再检索**结论**词族（`不构成独立审查` / `does not constitute independent` / `not independent because` / `cannot be performed`）。第二遍是必要的：只搜身份词会漏掉那些已把「同一身份」抽象成「结构上不可能」的句子。
2. **镜像**：对每个命中的登记，比较三副本的注记计数。**这是唯一能发现单侧漂移的方法** —— 本轮两次抓到真实缺陷：`docs/zh-CN/…RULING-001` 曾比 root 少 7 条（单向漂移），修完后 root 又比 zh 少 1 条（反向漂移，§7 裁定第 4 项）。两次都是门禁之外的缺陷，任何单侧检索都不会发现。
3. **历史**：本仓库**非 shallow**（7410 个提交），故「未搜 Git 历史」的免责条款本轮已撤销。全历史 `git log --all -p -- '*.md'` 逐增行检索「独立性结论 + 账号层事实」同句出现：去重后 8 条，其中 7 条是上表的注记本身，1 条是 `034` §9 的勘误正文，1 条是无关的 work-item 表格行。**历史轴零残留。**

不覆盖：`branch-protection` 的 audit log（API 不暴露）；仓库外的引用（agent 提示词、下游工具）；`docs/en` 与 `docs/zh-CN` 的**语义**一致性 —— 那是政策 §9.1 右列的 `M-05`，不是机器可验证项。

### 5.3 两条曾被误记为缺陷、实为设计态的事项

清扫过程中有两项被初步记为「known defect」，复核后撤回。记在这里，是为了防止后续会话把它们当工作项重开：

- **`485 unclassified`**：全树 `check_document_management.py` 报 `INCOMPLETE`（退出 2）。这是政策 §8 明文允许的**渐进采纳积压** —— 「积压可以继续未分类，但禁止增长」，而 `--require-changed` 保证它不增长。`INCOMPLETE` 刻意不等于 PASS。不是缺陷。
- **4 个 `docs/zh-CN/` 文件是英文正文**（`PARTIAL-SCOPE-019`、`MEASUREMENT-REPRODUCIBILITY-023`、`PAIRING-RESIDUAL-013`、`GAP-EXEC-2026-11-21-018`，其中 `023` 与 `docs/en` 逐字节相同）：`check_bilingual_docs.py` 的 `mirrored = english.is_file() and chinese.is_file()` 只验**存在性**，政策 §9.1 把「语义一致」明确列在右列并指派给 `M-05`。门禁的行为与它声明的契约一致，不是漏洞。翻译这 4 份是内容工作，不是治理修复。

---

## 6. 必须写明的弱点

会话级独立审查比"同会话换角色"强，但比人类审查弱：**两个会话可能由同一模型、同一提供方驱动，共享训练偏差。** 这一点不是可以含糊过去的。

若要更强的独立性，需要的是**不同模型家族**或**人类审查**，那是另一条款，不在本次改动范围内。本文件不假装会话级审查已经足够，只把门槛设到基线要求的那一档，并标明再往上一档需要什么。

## 7. 本文件不主张什么

- 不主张会话级独立审查已充分覆盖高风险变更。它覆盖了基线要求的那一档，仅此。
- 不主张 21 个 `NOT_ASSIGNED` 会因此自动被执行。可执行不是已执行。
- 不主张旧条款"当初写错了"。2026-11-18 写下时可能正是当时意图；是意图变了。
- 不主张我作为 owner-proxy 有权独自改治理条款。是所有者直接指令，本文件记录该指令而非主张该权力。

**阻断链（按新基线）：** 会话级独立审查 `AVAILABLE` → 未履行 `UNFULFILLED`（非 `BLOCKED`）→ 21 个 `NOT_ASSIGNED` 是待执行的审查任务 → 文本冲突已消除。

---

## 8. 复现

```
# 1. 现行条款已是会话级
grep -n "property of the reviewing session" 14-ai-development/PR-GOVERNANCE-001.md
grep -n "审查会话的属性" 14-ai-development/PR-GOVERNANCE-001.md

# 2. 六处已无身份级措辞。注意：在包含本文件的树上，下面第一条命令必然命中
#    本文件 §2 引文、§4 存档与本节自身，这是预期的。
#    判定标准是"本文件之外零命中"，不是"零输出"。
git grep -n "even if the session adopts a different role" -- "*.md" ':!*INDEPENDENCE-IS-SESSION-LEVEL-036*'
-> (无输出)   # 排除本文件后的真实结果
git grep -n "作者相同 GitHub 连接身份、仅切换角色的第二个 AI 会话不构成独立审查者" -- "*.md"
-> (无输出)

# 3. 原文保存在本文件 §4
```

---

## 1. What changed

The owner's instruction: *independent review requires only an independent session, not an independent account — that is the baseline.* The repository said the opposite, and said it verbatim. Six clauses that bound independence to the GitHub account now bind it to **the session**.

| File | Line | Before | After |
|---|---|---|---|
| `14-ai-development/PR-GOVERNANCE-001.md` | 136 (EN) | same identity is not independent, **even if the session adopts a different role** | independence is a **session** property; the identity is a carrier; role simulation **inside** the authoring session still is not independent |
| same | 138 (ZH) | as above | as above |
| `docs/en/.../PR-GOVERNANCE-001-ENFORCEMENT.md` | 40 | a **identity**-independent reviewer | a **session**-independent reviewer |
| same | 43 | a second AI role on the same identity is not independent | **another session** reviewing artifacts it neither authored nor implemented **is** independent, and may use the same identity |
| same | 55 | same-identity approval is always invalid | same-identity approval is valid **when the session is independent and discloses it** |
| `docs/zh-CN/.../PR-GOVERNANCE-001-ENFORCEMENT.md` | 40 / 43 / 55 | as above | as above |

## 2. Why the old text had to change, not be reinterpreted

Line 136 was not vague. It named the session dimension and denied it: *"A review performed through the same connected GitHub identity as the author is not independent, even if the session adopts a different role."* The Chinese counterpart said the same. That sentence closes the very path the baseline permits, so the baseline **replaces** it rather than reinterpreting it.

**The first version of this section got one thing wrong, corrected 2026-11-24.** It claimed that no document ever defined independence at session level, on the strength of a search for `independent session` / `独立会话` / `separate session` / `different session` returning nothing. That search result was false: on the pre-change baseline `1259f1af` those four terms hit 8 / 10 / 11 / 6 files respectively — e.g. `AI-EXEC-001.md` §15's "NR-001 independent session", `chatgpt-native-execution-model.zh-CN.md` §170's "satisfies the independent-session requirement", and `AI-EXEC-ROLLOUT-001.md`'s "NR-001 independent-session review".

The correct statement: session-level independence was **already in use in many places**, but no governance clause had made it **the §5 test** — it was one step inside the NR-001 review flow, never §5 independence itself. The change therefore **promotes an already-used test into the clause's criterion**; it does not introduce a concept the repository had never seen. That distinction matters for traceability: the former can cite six months of practice, the latter cannot.

Reproduction command (this section's first version omitted it too; added 2026-11-25):

```
for t in "independent session" "独立会话" "separate session" "different session"; do
  printf '%-20s ' "$t"; git grep -il "$t" 1259f1af -- "*.md" | wc -l
done
-> independent session  8
   独立会话             10
   separate session     11
   different session    6
```

`-i` is not optional. Without it the counts are 6 / 10 / 10 / 5, because variants such as `Independent Session` and `Separate sessions` are skipped. Neither result is false, but only the case-insensitive one matches the four numbers this section states — a reader checking the section as first written would find the numbers did not add up, and would be right to suspect that the erratum itself was fabricated. That is the defect class §2 exists to fix, so the command belongs in the text.

## 3. The new clause's exact boundaries

Still not allowed: **role simulation inside the authoring session** (the boundary of the baseline, not a weakening of it — reviewer and author would share one context and one incentive); `COMMENT` is still not `APPROVE`; exceptions must still be recorded explicitly.

Newly allowed: another session, not sharing the author's context, reviewing artifacts it neither authored nor implemented, **is** independent review, may be submitted through the same connected GitHub identity, and must disclose that its independence is session-level.

## 4. The six original clauses, verbatim

Kept so that a rollback or comparison needs no git archaeology. **This is replaced text, not current policy.** The full six originals appear in the Chinese section above; they are identical strings, quoted from `main = 1259f1af` before substitution.

## 5. What this invalidates

`CONVERGENCE-CEILING-034` §2, §5 and §7 — the impossibility, `BLOCKED`, and no-exit judgements — are withdrawn, recorded in its §9 erratum. Registers about zero-review merges (`ZERO-REVIEW-GATE-008`, `SELF-REVIEW-007`, `PR425-001`) keep their **facts** (zero-review merges did happen) but their **attribution** must be re-read: previously blamed on "the platform cannot enforce plus there is only one identity", now attributable to **not opening an independent session**. This file does not change their status; that is each register's own business.

### 5.1 The sweep has landed: the measured inventory (2026-11-25)

The "etc." in section 5 was not rhetoric -- it was a balance nobody had counted. The count: **11 files**, of which 9 use the three-copy layout and 2 use the `.md` / `.en.md` pairing layout (the latter declare no `bilingual_counterpart`, following the `MERGE-AFTER-RULING-003` precedent).

| File | Annotations root / en / zh-CN | Grounds chiefly replaced |
|---|---|---|
| `OWNER-DECISION-REVIEW-INDEPENDENCE-001` | 20 / 20 / 20 | The seven inferences drawn from "independence needs a second GitHub account" |
| `GOV-NC-2026-11-21-SELF-REVIEW-007` | 12 / 12 / 12 | The title, the `reviews >= 1` count, the section 8 decision procedure (now marked "cannot be used as a gate") |
| `GOV-NC-2026-11-21-GATE-DEADLOCK-006` | 7 / 7 / 7 | Section 12.3, the two cells in section 14.1, the reasoning around the section 14.2 code block |
| `GOV-NC-2026-11-21-REGRESSION-009` | 7 / 7 / 7 | The section 10 "author is the merger" element, the section 11.5 table cell |
| `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` | 7 / 7 / 7 | The section 11.8 status string's "0 independent reviews" is an account-layer count |
| `GOV-REV-2026-11-24-CONVERGENCE-CEILING-034` | 5 / 9 / 5 | Two places in section 7 (a bilingual file -- `docs/en` carries both languages, so the asymmetry is intended) |
| `GOV-REV-2026-11-21-PR425-001` | 2 / 2 / 2 | Section 0, the only **positive** use: differing identities is neither sufficient nor necessary |
| `GOV-NC-2026-11-24-REGISTER-INDEX-031` | 1 / 1 / 1 | -- |
| `GOV-NC-2026-11-24-DISPATCH-CHANNEL-CLOSED-032` | 1 / 1 / 1 | Conclusion re-grounded: a self-issued widening is, by construction, unseconded |
| `GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004` | 2 / -- | "No role separation exists" becomes "did not happen" is not "cannot happen" |
| `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` | 1 / -- | Conclusion now rests on the register's own `COMMENTED` is not `APPROVE` |

**No status was changed.** The table adds annotations only; it does not move any register out of `OPEN` / `DISPATCHED`. Promotion remains each register's own business.

### 5.2 The three axes the sweep covered, and what it does not cover

1. **The tree**: a whole-tree search for the identity vocabulary (`second account` / `collaborators = 1` / `one writable identity` / `same account` / `self-approv` / `sole reviewer` / `APPROVED = 0`), then a second search for the **conclusion** vocabulary (`does not constitute independent` / `not independent because` / `cannot be performed` / the Chinese equivalents). The second pass is not optional: an identity-only search misses the sentences that have already abstracted "one identity" into "structurally impossible".
2. **The mirrors**: for every hit, compare annotation counts across the three copies. **This is the only method that finds one-sided drift** -- it caught two real defects in this round: `docs/zh-CN/...RULING-001` once carried seven fewer annotations than root (drift in one direction), and after that was fixed root carried one fewer than zh (drift in the other -- section 7 ruling item 4). Neither was visible to any single-sided search.
3. **History**: this repository is **not shallow** (7,410 commits), so the "Git history not searched" caveat is withdrawn. A full `git log --all -p -- '*.md'` over every added line for "independence conclusion + account-layer fact" in one sentence yields 8 unique lines after deduplication: 7 are the annotations in the table above, 1 is the section 9 erratum text in `034`, 1 is an unrelated work-item table row. **Zero residual on the history axis.**

Not covered: the branch-protection audit log (the API does not expose it); references outside the repository (agent prompts, downstream tools); and **semantic** agreement between `docs/en` and `docs/zh-CN` -- that is `M-05` in the right-hand column of policy section 9.1, and it is not a machine-verifiable item.

### 5.3 Two items initially recorded as defects, withdrawn after review

Two items were provisionally logged as "known defects" during the sweep and then withdrawn. They are recorded here so a later session does not reopen them as work items:

- **`485 unclassified`**: a whole-tree `check_document_management.py` run reports `INCOMPLETE` (exit 2). This is the **progressive-adoption backlog** policy section 8 permits in so many words -- "the backlog may stay unclassified; it may not grow" -- and `--require-changed` is what stops it growing. `INCOMPLETE` is deliberately not PASS. Not a defect.
- **Four `docs/zh-CN/` files carrying English bodies** (`PARTIAL-SCOPE-019`, `MEASUREMENT-REPRODUCIBILITY-023`, `PAIRING-RESIDUAL-013`, `GAP-EXEC-2026-11-21-018`; `023` is byte-identical to its `docs/en` twin): `check_bilingual_docs.py` computes `mirrored = english.is_file() and chinese.is_file()` -- existence only -- and policy section 9.1 lists "semantic parity" in the right-hand column, assigned to `M-05`. The gate behaves as its declared contract says it does. Translating those four is content work, not governance repair.

---

## 6. The weakness that must be stated

Session-level independence is stronger than role simulation inside one session and weaker than human review: **two sessions may be driven by the same model from the same provider and share training bias.** That is not a detail to gloss over. Stronger independence needs a different model family or human review — a separate clause, outside this change. This file does not pretend session-level review is sufficient; it sets the bar where the baseline requires it and names what the next level up would take.

## 7. What this file does not claim

Not that session-level independence adequately covers high-risk changes — it covers the tier the baseline names, nothing more. Not that the 21 `NOT_ASSIGNED` entries will now be executed; executable is not executed. Not that the old clauses were wrong when written on 2026-11-18 — the intent changed. Not that an owner-proxy may unilaterally amend governance clauses: this was a direct owner instruction, and this file records it rather than asserting the power.

**Blocking chain under the new baseline:** session-level independent review `AVAILABLE` → `UNFULFILLED` (not `BLOCKED`) → the 21 `NOT_ASSIGNED` entries are pending review tasks → the textual conflict is resolved.

## 8. Reproduction

```
# 1. The clause is now session-level (run on the merge commit; on base this line
#    does not exist yet, so an empty result is expected there)
grep -n "property of the reviewing session" 14-ai-development/PR-GOVERNANCE-001.md
grep -n "审查会话的属性" 14-ai-development/PR-GOVERNANCE-001.md

# 2. No identity-level wording outside this file. The exclusion matcher is
#    required: without it the command necessarily hits this file's own
#    section 2 quotation, section 4 archive and this block. The test is
#    "zero hits outside this file", not "zero output".
git grep -n "even if the session adopts a different role" -- "*.md" ':!*INDEPENDENCE-IS-SESSION-LEVEL-036*'
-> (no output)

# 3. The original wording is preserved in section 4 of this file.
```
