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
        value: "898b0d7f4a45667a22632b778dba0a29d40df1be9ecaa6ccf5cd223d054667c4"
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
    en: "docs/en/14-ai-development/governance-register/GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036.md"
    zh-CN: null
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

这句话堵死的正是基线允许的那条路。所以基线不是"对旧文本的另一种解释"，而是**替换它**。

**本节第一版在这里写错了一件事，2026-11-24 修正。** 第一版称「仓库内没有任何文档把独立性定义为会话级（搜 `independent session` / `独立会话` / `separate session` / `different session`，零命中）」。该搜索结论是错的：在改动前的基线 `1259f1af` 上，这四个词分别命中 8 / 10 / 11 / 6 个文件，例如 `AI-EXEC-001.md` §15 的「NR-001 独立会话」、`chatgpt-native-execution-model.zh-CN.md` §170 的「满足独立会话要求」、`AI-EXEC-ROLLOUT-001.md` 的「NR-001 独立会话审查」。

正确的表述是：会话级独立性**早已在多处被使用**，但没有任何一份治理条款把它**定义为 §5 的判据**——它一直是 NR-001 审查流程里的一个环节，而不是 §5 独立性本身。因此本次改动的性质是**把已在使用的口径提升为条款判据**，而不是「引入一个仓库里从未有过的概念」。这个区别影响可追溯性：前者有六个月的实践先例可引用，后者没有。

复现命令（本节第一版又漏了它，2026-11-25 补上）：

```
for t in "independent session" "独立会话" "separate session" "different session"; do
  printf '%-20s ' "$t"; git grep -il "$t" 1259f1af -- "*.md" | wc -l
done
-> independent session  8
   独立会话             10
   separate session     11
   different session    6
```

`-i` 不是可选的。去掉它得到的是 6 / 10 / 10 / 5，因为 `Independent Session`、`Separate sessions` 这类大小写变体被跳过。两个结果都不假，但只有带 `-i` 的才对得上本节写下的四个数字——也就是说，一个读者照本节原来的措辞去核对，会得到"数额不符"的结论，并合理地怀疑这份勘误本身又是编的。这正是 §2 要修的那类错误，所以命令必须写出来。

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

# 2. 六处已无身份级措辞。注意：下面两条命令在"包含本文件"的树上必然命中
#    本文件 §4 的存档引用（3 处）与本节自身（1 处），这是预期的。
#    判定标准是"本文件之外零命中"，不是"零输出"。
git grep -n "even if the session adopts a different role" -- "*.md"
-> 仅命中本文件（§2 引文、§4 存档、§8 自身）；其他文件零命中
git grep -n "even if the session adopts a different role" -- "*.md" ':!*INDEPENDENCE-IS-SESSION-LEVEL-036*'
-> (无输出)   # 排除本文件后的真实结果
git grep -n "作者相同 GitHub 连接身份、仅切换角色的第二个 AI 会话不构成独立审查者" -- "*.md"
-> (无输出)

# 3. 原文保存在本文件 §4
```
