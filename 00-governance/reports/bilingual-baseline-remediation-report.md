---
document_metadata:
  domain: security-governance
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: NOT_RECORDED
      decision_date: NOT_RECORDED
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
      last_verification_note: "No formal approval record exists; the report's own Status line reads DRAFT."
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
---

# GOV-DOC-001 v1.2 Bilingual Baseline Remediation Report
# GOV-DOC-001 v1.2 双语基线修复交付报告

- Work Item ID: GOV-DOC-001-V1.2-REMEDIATION
- Policy ID: GOV-DOC-001
- Proposed Version: 1.2
- Status: DRAFT — NEEDS REVISION — PENDING FORMAL GOVERNANCE APPROVAL
- Repository: oahcom/AiMemoryBrainArchitecture
- Target Branch: remediation/gov-doc-001-v1.2-bilingual-baseline
- Pull Request: #271
- Report Version: v2.10 / 文档版本：v2.10
- Revision Date: 2026-11-25 / 修订日期：2026-11-25

## 0. Record boundary and snapshot policy / 记录边界与快照口径

### EN

This report is a point-in-time governance record, not a live dashboard. Two classes of statement are separated and must not be conflated.

- **Bound assets (dated snapshots).** Repository HEADs, tree and blob SHAs, PR state (`OPEN` / `merged`), ahead/behind counts, workflow run identifiers, and file manifests are bound to the moment they were read. Each such line carries its own as-of boundary. A later commit does not falsify a bound snapshot, and a bound snapshot must not be read as a current assertion.
- **Live assertions (maintained state).** Only finding states (`CLOSED` / `PARTIAL` / `NOT_VERIFIED`), normative statements, and outstanding-blocker entries are maintained. When one changes, it is changed in a new revision with a revision note.
- **Limitation assertions.** A third class exists and must not be forced into the first two: statements that are true, permanent, and not actionable — for example "historical migration cannot be inferred from the inventory". These are recorded as `LIMITATION` rather than left `OPEN`. An `OPEN` finding is a work item; a `LIMITATION` is a boundary. Mixing them produces either a work item that can never be closed or a boundary that is quietly treated as closed. A `LIMITATION` is admissible only when all three conditions hold: (i) the statement is factually true as written; (ii) no work item would remove it — it is not merely hard or deferred; (iii) no reasonable executable path exists, including collecting further evidence, changing code, or re-running an investigation. If any one condition later fails, the entry returns to `OPEN` in a new revision with a revision note, exactly as any other falsified assertion. Without that escape the category would become a place to park inconvenient work, which is the failure mode it is meant to prevent. Each `LIMITATION` entry must additionally list the executable paths that were examined and why each was excluded, together with the review that confirmed the exclusion. "No executable path exists" is a conclusion that has to be shown, not asserted; an entry that asserts it without the enumeration fails c8.

Maintenance rule: do not rewrite a bound snapshot in order to chase a moving HEAD; append a new dated snapshot instead. Only live assertions may be edited in place, and every such edit must be recorded in the revision note. This rule exists because the opposite practice is unsatisfiable: any commit changes `main`, so a report that maintains HEAD values as current assertions is stale the moment it is merged.

**Re-open trigger.** A closure recorded in this report is not permanent and is not self-validating. If a maintained assertion is later shown to be false — a snapshot marked superseded is cited as current, a corrections section drifts from the objects it describes, or a newly introduced line repeats the same defect class — the affected finding is set back to `OPEN` in a new revision, and the revision note names the assertion that failed. The applicable test for this mechanism is therefore not whether an old bound snapshot is still accurate, but whether a newly introduced stale live assertion is re-opened rather than defended by the snapshot distinction. A rule that only ever permits closure would be self-exemption.

**Closure evidence standard.** A finding may be closed only on evidence that a third party with read access can re-derive: the repository object (path and ref, or endpoint and parameter), the expected value, and the check that compares them. Author narrative alone is not closure evidence. Where a closure also rests on a semantic judgement — for example that corrected prose no longer asserts a stale value — that judgement is labelled as judgement and attributed to the review that made it, not presented as a measured fact.

**Reproduction prerequisites.** Every request cited as closure evidence in this report is a plain `GET` carrying `Authorization: token <t>` and `Accept: application/vnd.github+json`, where `<t>` is a token with read access to this private repository. No write scope is needed. Response handling is fixed: a non-200 response — including `403` from a secondary rate limit or `404` from a wrong `ref` — is recorded as `INCONCLUSIVE`, never as a mismatch and never as a pass; only a `200` whose field equals the expected value counts as evidence. Where a `403` or `404` appears, the cause is diagnosed and stated rather than inferred from the status code.

### 中文

本报告是有时点的治理记录，不是实时看板。两类陈述必须分开，不得混为一谈。

- **绑定资产（带时点的快照）**：仓库 HEAD、tree 与 blob SHA、PR 状态（`OPEN` / `merged`）、ahead/behind 计数、workflow 运行标识、文件清单，均绑定于其被读取的时刻。每条此类陈述自带 as-of 边界。后续提交不使既有快照失效，既有快照也不得被读作当前断言。
- **活动断言（受维护的状态）**：仅限 finding 状态（`CLOSED` / `PARTIAL` / `NOT_VERIFIED`）、规范性陈述、未解决阻塞条目。它们发生变化时，在新修订中更新并附修订说明。
- **限制性断言**：存在第三类，且不得被强行归入前两类——它们成立、永久、且不可行动（例如「历史迁移无法从清单推得」）。此类记为 `LIMITATION`，而不是任其保持 `OPEN`。`OPEN` 是工作项，`LIMITATION` 是边界。两者混用的后果：要么得到一个永远无法关闭的工作项，要么得到一条被默认当作已关闭的边界。 `LIMITATION` 仅在三个条件同时成立时可用：（i）该陈述如其所写为事实；（ii）没有任何工作项能消除它——不只是「难」或「延后」；（iii）不存在合理可执行路径（包括补证据、改代码、重做调查）。任一条件日后不再成立，该条目在新修订中回到 `OPEN` 并附修订说明，与其他被证伪断言同样处理。若无此出口，该类别就会变成安放麻烦工作的地方，而这正是它要防止的失败模式。 每个 `LIMITATION` 条目还必须列出已排查的可执行路径、逐条排除理由，以及确认该排除的审查。「不存在可执行路径」是结论，必须被展示而非声明；未列举而直接声称者，在 c8 上不通过。

维护规则：不得为追逐移动的 HEAD 而改写历史快照，应追加新的带时点快照。只有活动断言可以就地变更，且每次变更都必须记入修订说明。该规则的存在理由：相反做法在逻辑上不可满足——任何提交都会改变 `main`，把 HEAD 值当作当前断言来维护的报告，在合并那一刻就已陈旧。

**重新开启触发器**：本报告记录的关闭不具永久性，也不自证。若某项受维护的断言事后被证为不真——例如已标注「被取代」的快照被引为当前、更正段落与其所描述对象脱节、新增行重复同一类缺陷——则在新修订中将相应 finding 置回 `OPEN`，并在修订说明中点名失败的断言。因此本机制的检验标准不是「旧快照是否仍准确」，而是「新引入的陈旧活动断言是否被重新开启」。只允许关闭、不允许重开的规则，本质上就是自我豁免。

**关闭证据标准**：finding 只能基于第三方可复现推导的证据关闭：必须给出对象（路径与 ref，或端点与参数）、期望值、以及比对方式。仅凭作者叙述不构成关闭证据。若关闭同时依赖语义判断（如「更正后的文字不再陈述旧值」），该判断应标注为判断并归属于作出该判断的审查，不得作为实测事实呈现。

**复现前提**：本报告中作为关闭证据引用的每个请求均为 `GET`，携带 `Authorization: token <t>` 与 `Accept: application/vnd.github+json`，其中 `<t>` 为对本私有仓库具有读权限的 token，无需写权限。响应处理规则固定：非 200 响应（包括次级限速的 `403`，或 `ref` 错误的 `404`）一律记为 `INCONCLUSIVE`，不得计为不符合，也不得计为通过；只有 `200` 且字段等于期望值才构成证据。出现 `403`/`404` 时，应诊断并写明原因，不得凭状态码推断。

## 1. Objective / 目标

### EN

Extend the existing GOV-DOC-001 bilingual architecture documentation policy to cover project governance work products, without creating a duplicate Policy ID or rewriting historical records.

The remediation includes bilingual Umbrella Requirements, GitHub Issues, Commit Messages, Pull Requests, future repository inheritance, and historical migration tracking.

This report records actual submission, read-back verification, historical inventory limitations, independent review findings, and outstanding CI failures.

### 中文

扩展现有 GOV-DOC-001 双语架构文档规范，使其覆盖项目治理工作产物，不创建重复 Policy ID，也不重写历史记录。

修复范围包括 Umbrella Requirement、GitHub Issue、Commit Message、Pull Request 双语化、未来仓库规范继承及历史迁移跟踪。

本报告记录实际提交、读回验证、历史清点限制、独立审查发现和未解决的 CI 失败。

## 2. Baseline and current repository evidence / 基线与当前仓库证据

### 2.1 Historical baseline / 历史基线

- Repository: oahcom/AiMemoryBrainArchitecture
- Historical baseline HEAD: c33a1bcd36f767c96f641d2a154f34d102ce2645
- Policy path: 00-governance/bilingual-documentation-policy.md
- Historical Policy Blob SHA: 0e170479e1a71e8f4c124c6f1dc170241652f42b
- Policy version read: 1.1
- Policy status read: NORMATIVE

The complete v1.1 policy was read before drafting v1.2.

已在编制 v1.2 前完整读取 v1.1 规范。

### 2.2 Current main and remediation branch / 当前 main 与修复分支

- T2 submission-time main HEAD: `c5a995d9a2808112b007a9108e085048cbed5cc9`
- Current main HEAD at R6 remediation baseline: `4f82e3a48a35e9fd73e7920f0c6a559b77aaf0dc`
- Current main HEAD source: direct GitHub branch comparison/read-back
- Current main D1 policy blob: `0e170479e1a71e8f4c124c6f1dc170241652f42b` (the unchanged GOV-DOC-001 v1.1 NORMATIVE baseline)
- Remediation branch: `remediation/gov-doc-001-v1.2-bilingual-baseline`
- PR #271 current head at R6 baseline: `47369925ace93821eab82e4cec8418f8d7505d64`
- PR #271 tree at R6 baseline: `a02020dcb2e6b23bd5456b61ddb772c74ca95a63`
- PR #271 state: OPEN; merged: false
- PR base / merge-base recorded: `c5a995d9a2808112b007a9108e085048cbed5cc9`
- Current main...PR head comparison at the R6 baseline: `diverged`; ahead 8 / behind 42; merge base `c5a995d9a2808112b007a9108e085048cbed5cc9`
- Post-v2.2 validation snapshot: PR head `bbfe046b9307c9bfffd7606c4a7caadcb1de32f8`; D7 blob read back as `36c50869fe2c42d5e1f12616012c84e0a1cc5d28`; main...head comparison `diverged`, ahead 10 / behind 42; merge base unchanged at `c5a995d9a2808112b007a9108e085048cbed5cc9`.
- v2.3 normative-boundary correction (`2026-11-19T17:06:00Z`): `00-governance/bilingual-documentation-policy.md` is restored to the GOV-DOC-001 v1.1 NORMATIVE text, blob `0e170479e1a71e8f4c124c6f1dc170241652f42b`, byte-identical to current main. The v1.2 proposal is relocated to `00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md`, blob `d91bd92b79177decc7baa038fdd24b3f8323b995`, and remains NON-NORMATIVE; the normative path is not replaced by a draft.
- **Post-merge snapshot (as-of `2026-11-19T17:39:16Z`, bound to this bullet set only):** PR #271 `state=closed`, `merged=true`, `merged_at=2026-11-19T17:16:13Z`; merge commit `f86fddc0fa0291ea8a5e080e741f083ce179a0a2`; merge parents `a22024112fce3851428343ca3e655712057e6dce` (main before merge) and `1eefa22e7fecfcd882aff795796ae178d1f7c4a5` (the head that R8 reviewed). The reviewed head is therefore contained in `main` history; the earlier `diverged / ahead N / behind M` comparisons describe the pre-merge branch and are superseded as current assertions. Post-merge `main` tip at the time of this reading: `8b7897f172cbf9b9dfbda5728836fd0a639e33bb`.
- **Annotation, not deletion:** the earlier bullet `PR #271 state: OPEN; merged: false` is a bound R6 snapshot. It is retained so the historical read-back stays auditable; it is not a current assertion.
- v2.3 measured comparison at the v2.3 authoring baseline (before the v2.3 commit): main `a22024112fce3851428343ca3e655712057e6dce`; PR head `f915e0234c3388def3bd97f2bfd2ce38dc1576d8`; `diverged`, ahead 11 / behind 70; merge base `c5a995d9a2808112b007a9108e085048cbed5cc9`.

**EN**

The current main baseline is newer than the PR's recorded base. The branch is divergent from current main. This comparison is evidence of divergence only; it is not a successful Exact-Head integration verification and does not authorize merge.

**中文**

当前 main 基线晚于 PR 记录的 base。修复分支与当前 main 已发生分叉。该比较仅证明分叉状态，不构成 Exact-Head 集成复核通过，也不构成合并授权。

## 3. Seven-file submission and read-back / 七文件提交与读回

### 3.1 Commit evidence / Commit 证据

**Historical initial seven-file submission / 历史首次七文件提交**

- Commit SHA: `a77219fa2834af0c4535e6692029adaec2e62638`
- Tree SHA: `b11d70b27ef63c5c6af64a5bbc537bec8ab70bd9`
- Parent SHA: `c5a995d9a2808112b007a9108e085048cbed5cc9`
- Commit timestamp: `2026-11-19T07:07:18Z`
- Scope: original seven-file submission; this is historical submission evidence, not the current PR head.

**Current PR head at the R6 review baseline / R6 复审基线的当前 PR head**

- Commit SHA: `47369925ace93821eab82e4cec8418f8d7505d64`
- Tree SHA: `a02020dcb2e6b23bd5456b61ddb772c74ca95a63`
- Commit timestamp: `2026-11-19T14:40:18Z`
- Commit subject: `docs(governance): restore acceptance and governance ledgers in remediation report`
- Changed path in this commit: `00-governance/reports/bilingual-baseline-remediation-report.md`
- PR: #271, OPEN, not merged.

**EN**

The initial seven-file submission and the later D7 report-restoration commit are distinct historical events. The original submission commit must not be presented as the current branch head. The R6 baseline head above is the pre-v2.2 remediation head. D7 v2.2 content was committed as `77084adfb782ed0579cda4c773b14784cd389e69`; the report-version metadata alignment commit is `bbfe046b9307c9bfffd7606c4a7caadcb1de32f8`. The post-commit D7 blob was read back as `36c50869fe2c42d5e1f12616012c84e0a1cc5d28`.

**中文**

首次七文件提交与后续 D7 报告恢复提交是两个不同的历史事件。不得将首次提交误写为当前分支 head。上列 R6 基线 head 是 v2.2 修正前的修复分支 head；v2.2 修正提交以随后 GitHub commit 和读回证据为准。

### 3.2 Exact file manifest / 精确文件清单

The following is the R6 independently read-back OBJ-07 seven-file manifest snapshot. The D7 entry is the pre-v2.2 D7 Version 2.1 report blob; it is retained as the historical manifest anchor and is not a self-referential hash for this v2.2 revision.

以下为 R6 独立读回的 OBJ-07 七文件 manifest 快照。D7 条目是 v2.2 修订前 D7 Version 2.1 报告的 blob；该值作为历史 manifest 锚点保留，不作为本 v2.2 修订的自引用哈希。

| ID | Repository path / 仓库路径 | Blob SHA |
|---|---|---|
| D1 | `00-governance/bilingual-documentation-policy.md` | `66517d39dfeae459fef5cedf9d5a79de08faf08d` |
| D2 | `00-governance/bilingual-governance-migration-register.md` | `b5d6d2b6c5049e71578d9323c770bc1b48b9e0cc` |
| D3 | `00-governance/templates/bilingual-issue-template.md` | `64d432395dc7bec9ba5c3b2ae534df4b01a2db3c` |
| D4 | `00-governance/templates/bilingual-umbrella-requirement-template.md` | `9265098d739369522000ebc54b8c0275ee7e5b6d` |
| D5 | `00-governance/templates/bilingual-commit-message.md` | `8ea68efd927c62ba48c3249cc39e62760ced9370` |
| D6 | `00-governance/templates/repository-policy-inheritance.md` | `122f86b1e223e852eb19add7c37c452151372fe8` |
| D7 | `00-governance/reports/bilingual-baseline-remediation-report.md` | `8fa00af52a6c61e36f850c90332006360b8a82df` |

D2 was not modified by commit `47369925ace93821eab82e4cec8418f8d7505d64`. This D7 v2.2 changeset is D7-only; it does not modify D2.

**v2.3 current manifest / v2.3 当前清单**

The v2.3 changeset relocates D1 and leaves D2-D6 byte-identical to the R6 read-back. D7 is the file carrying this text and therefore cannot contain its own blob; its post-commit blob is read back and recorded in a PR comment, not in this table.

本 v2.3 变更集迁移 D1，D2–D6 与 R6 读回结果逐字节一致。D7 即承载本表的文件，无法包含自身 blob；其提交后 blob 通过 PR 评论读回登记，不写入本表。

| ID | Repository path / 仓库路径 | Blob SHA | Note / 说明 |
|---|---|---|---|
| D1 | `00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md` | `d91bd92b79177decc7baa038fdd24b3f8323b995` | v1.2 draft, relocated from the normative path in v2.3 / v2.3 由规范路径迁移而来的 v1.2 草案 |
| D1-N | `00-governance/bilingual-documentation-policy.md` | `0e170479e1a71e8f4c124c6f1dc170241652f42b` | v1.1 NORMATIVE, restored and unmodified / v1.1 NORMATIVE，已恢复且未修改 |
| D2 | `00-governance/bilingual-governance-migration-register.md` | `b5d6d2b6c5049e71578d9323c770bc1b48b9e0cc` | unchanged / 未变更 |
| D3 | `00-governance/templates/bilingual-issue-template.md` | `64d432395dc7bec9ba5c3b2ae534df4b01a2db3c` | unchanged / 未变更 |
| D4 | `00-governance/templates/bilingual-umbrella-requirement-template.md` | `9265098d739369522000ebc54b8c0275ee7e5b6d` | unchanged / 未变更 |
| D5 | `00-governance/templates/bilingual-commit-message.md` | `8ea68efd927c62ba48c3249cc39e62760ced9370` | unchanged / 未变更 |
| D6 | `00-governance/templates/repository-policy-inheritance.md` | `122f86b1e223e852eb19add7c37c452151372fe8` | unchanged / 未变更 |
| D7 | `00-governance/reports/bilingual-baseline-remediation-report.md` | post-commit read-back / 提交后读回 | self-referential; recorded in PR comment / 自引用，登记于 PR 评论 |

提交 `47369925ace93821eab82e4cec8418f8d7505d64` 未修改 D2。本 D7 v2.2 变更集仅修改 D7，不修改 D2。

**Post-merge manifest read-back at `main` `8b7897f172cbf9b9dfbda5728836fd0a639e33bb` (as-of `2026-11-19T17:39:16Z`) / 合并后 manifest 读回（main `8b7897f1`，as-of `2026-11-19T17:39:16Z`）**

Read back through the contents API at the recorded `main` tip. This is a new dated snapshot; the R6 OBJ-07 snapshot above is unchanged and remains the historical anchor.

通过 contents API 在记录的 `main` tip 读回。本表为新的带时点快照；上方 R6 OBJ-07 快照未变，仍作为历史锚点。

| ID | Repository path / 仓库路径 | Blob SHA | Relation to the R6 snapshot / 与 R6 快照关系 |
|---|---|---|---|
| D1-N | `00-governance/bilingual-documentation-policy.md` | `0e170479e1a71e8f4c124c6f1dc170241652f42b` | byte-identical / 逐字节一致 |
| D1 | `00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md` | `d91bd92b79177decc7baa038fdd24b3f8323b995` | added by #271, NON-NORMATIVE / #271 新增，非规范 |
| D2 | `00-governance/bilingual-governance-migration-register.md` | `c805795625bfb367373826b6c6d33221af5853ba` | advanced by later register revisions / 随登记册后续修订前进 |
| D3 | `00-governance/templates/bilingual-issue-template.md` | `64d432395dc7bec9ba5c3b2ae534df4b01a2db3c` | unchanged / 未变更 |
| D4 | `00-governance/templates/bilingual-umbrella-requirement-template.md` | `9265098d739369522000ebc54b8c0275ee7e5b6d` | unchanged / 未变更 |
| D5 | `00-governance/templates/bilingual-commit-message.md` | `8ea68efd927c62ba48c3249cc39e62760ced9370` | unchanged / 未变更 |
| D6 | `00-governance/templates/repository-policy-inheritance.md` | `122f86b1e223e852eb19add7c37c452151372fe8` | unchanged / 未变更 |
| D8 | `00-governance/reports/f06-object-reconciliation.md` | `646800d4b426bd19cf9d58bf86433ece1a010bda` | added by #282 / #282 新增 |
| D7 | `00-governance/reports/bilingual-baseline-remediation-report.md` | self-referential / 自引用 | read back in a PR comment / 在 PR 评论中读回 |

`D2` differs from the R6 row on purpose: the register advanced after the R6 read-back. The R6 value is not wrong; it is bound to an earlier moment. No row above is a substitution into the R6 snapshot.

`D2` 与 R6 行不同是故意的：登记册在 R6 读回之后又有修订。R6 值并非错误，只是绑定于更早时点。上表任何行都不是对 R6 快照的替代。

### 3.3 Verification result / 验证结果

**Historical verification note / 历史验证说明**

The original verification in this section applied to the previously committed D7 Version 1.0. The subsequent Version 2.0 proposal was later committed, and the Version 2.1 report was committed at the R6 remediation head. The current verification target must be distinguished from those historical targets.

本节最初的验证针对此前已提交的 D7 Version 1.0。后续 Version 2.0 提案已经提交；Version 2.1 报告也已提交至 R6 修复分支 head。当前验证目标必须与上述历史目标区分。

**R6 OBJ-07 read-back / R6 OBJ-07 读回**

R6 independently read back all seven files against the OBJ-07 manifest snapshot: 7/7 matched. The D7 v2.1 blob in that snapshot is `8fa00af52a6c61e36f850c90332006360b8a82df`. The v2.2 revision changes D7 only; the new D7 blob is verified separately by post-commit read-back and must not be retroactively substituted into the pre-v2.2 OBJ-07 snapshot.

R6 已依据 OBJ-07 manifest 快照独立读回全部七个文件：7/7 匹配。该快照中的 D7 v2.1 blob 为 `8fa00af52a6c61e36f850c90332006360b8a82df`。v2.2 修订仅修改 D7；新的 D7 blob 通过提交后的独立读回单独验证，不得追溯替换 v2.2 之前的 OBJ-07 快照。

**Current verification boundary / 当前验证边界**

The R6 independent review of Version 2.1 returned `NEEDS-REVISION`. This Version 2.2 report records the corrective response to R6 findings; it is not itself an independent acceptance. The v2.2 report-version-alignment commit `bbfe046b9307c9bfffd7606c4a7caadcb1de32f8` was read back as D7 blob `36c50869fe2c42d5e1f12616012c84e0a1cc5d28`. Workflow run `44559550224` on that head completed SUCCESS (job `135684753485`; 2026-11-19 15:51:45Z–15:51:48Z). The post-v2.2 main...head comparison remained `diverged` (ahead 10 / behind 42; merge base `c5a995d9a2808112b007a9108e085048cbed5cc9`); successful Exact-Head integration verification has not been established. A fresh independent review must evaluate the final v2.2 commit.

R6 对 Version 2.1 的独立复审结论为 `NEEDS-REVISION`。本 Version 2.2 报告记录对 R6 findings 的修正响应；本报告本身不构成独立验收。v2.2 版本对齐提交 `bbfe046b9307c9bfffd7606c4a7caadcb1de32f8` 的 D7 blob 读回为 `36c50869fe2c42d5e1f12616012c84e0a1cc5d28`；该 head 上的 workflow 运行 `44559550224` 结论 SUCCESS（job `135684753485`；2026-11-19 15:51:45Z–15:51:48Z）。v2.2 后的 main...head 比较仍为 `diverged`（ahead 10 / behind 42；merge base `c5a995d9a2808112b007a9108e085048cbed5cc9`）；尚未建立 Exact-Head 集成复核通过证据。必须由新的独立复审针对最终 v2.3 精确提交进行评估。

## 4. Issue updates and verification / Issue 更新与验证

Issues #262–#266 were updated through the authorized coordination workflow.

T9 independently fetched their current GitHub API representations.

| Issue | Requirement ID | State | Body bytes/length | Labels | Updated At |
|---|---|---|---:|---|---|
| #262 | REQ-01 | open | 4611 | [] | 2026-11-19T07:08:27Z |
| #263 | REQ-02 | open | 4229 | [] | 2026-11-19T08:46:57Z |
| #264 | REQ-03 | open | 4963 | [] | 2026-11-19T08:42:39Z |
| #265 | REQ-04 | open | 5780 | [] | 2026-11-19T07:08:39Z |
| #266 | REQ-05 | open | 4138 | [] | 2026-11-19T08:29:28Z |

The five bilingual titles and bodies were read back.

No Issue was closed.

No label change was recorded.

The Requirement Status values remain RECORDED according to the original update evidence.

五个 Issue 的双语标题和正文已读回。

没有关闭任何 Issue。

没有记录标签变更。

根据原更新证据，五个 Requirement Status 均保持 RECORDED。

Bilingual completion does not mean Owner approval or requirement adoption.

完成双语化不代表 Owner 批准或需求采纳。

## 5. Historical inventory and migration register / 历史清点与迁移登记

### 5.1 Issue inventory / Issue 清点

**EN**

#### Historical Issue Language Inventory

The Issue language inventory contains **39 records**:

| Classification | Count | Treatment |
|---|---:|---|
| EN_ONLY | 28 | Subject to the applicable migration requirements |
| EN_ZH_MIXED | 10 | Subject to the applicable migration requirements |
| ZH_ORIGINAL_WITH_EN_TERMS | 1 | Issue #254; HOLD |
| **Total** | **39** | |

Issue #254 is included in the 39-record inventory. It is the record classified as `ZH_ORIGINAL_WITH_EN_TERMS` and remains on HOLD.

Each of the 39 records must be anchored to its corresponding `body_sha256`. The inventory count does not imply that the Issues have completed bilingual migration.

**中文**

#### 历史 Issue 双语语言状态清点

Issue 语言状态清单共包含 **39 条记录**：

| 分类 | 数量 | 处置 |
|---|---:|---|
| EN_ONLY | 28 | 按适用的迁移要求处理 |
| EN_ZH_MIXED | 10 | 按适用的迁移要求处理 |
| ZH_ORIGINAL_WITH_EN_TERMS | 1 | Issue #254；HOLD |
| **合计** | **39** | |

Issue #254 **属于这 39 条登记记录**，是分类为 `ZH_ORIGINAL_WITH_EN_TERMS` 的记录，当前继续保持 HOLD。

39 条记录均须以对应的 `body_sha256` 为锚点。清点数量一致不代表这些 Issue 已完成双语迁移。

---

### 5.2 Commit inventory / Commit 清点

**EN**

#### Historical Commit Message Language Inventory

The Commit inventory contains **313 records**:

| Classification | Count | Record |
|---|---:|---|
| EN_ONLY | 312 | English commit messages |
| MIXED | 1 | C168 |
| **Total** | **313** | |

Each record must include both its Git Commit `sha` and its corresponding `msg_sha256`.

Language classification is determined from the substantive content of the complete commit message, including its title and body. It must not be inferred from the language of changed files, paths, related Issues, or pull requests.

C168 is the only `MIXED` record in the 313-record inventory. The other 312 records are `EN_ONLY`.

The inventory records historical message states; it does not rewrite historical Git objects or establish that historical messages have been migrated.

**中文**

#### 历史 Commit 提交消息语言状态清点

Commit 登记清单共包含 **313 条记录**：

| 分类 | 数量 | 记录 |
|---|---:|---|
| EN_ONLY | 312 | 英文提交消息 |
| MIXED | 1 | C168 |
| **合计** | **313** | |

每条记录均须包含对应 Git Commit 的 `sha` 及其 `msg_sha256`。

语言分类依据完整提交消息的实质内容判定，包括标题和正文。不得根据被修改文件的语言、文件路径、关联 Issue 或 Pull Request 的语言推断。

C168 是 313 条记录中唯一的 `MIXED` 记录，其余 312 条均为 `EN_ONLY`。

本清单用于登记历史提交消息的语言状态，不改写历史 Git 对象，也不证明历史提交消息已经完成双语迁移。

---

### 5.3 Pull Request inventory / PR 清点

- Total PR count: 232.
- Identified single-language PR inventory: 230.
- Existing P-01 through P-06 group coverage: 216.
- Unassigned PRs: 14.

Unassigned PR identifiers:

#269, #207, #197, #194, #193, #192, #191, #190, #189, #154, #143, #141, #139, #136.

These 14 PRs have not been assigned to a migration group because sufficient grouping evidence is not included in the current evidence package.

不得在缺少归组依据时补造 P 组归属。

### 5.4 Migration classifications / 迁移分类

**EN**

#### Language Classification and Migration Boundary

Issue and Commit inventories are separate classification sets and must be counted independently.

- Issue inventory: 39 records — 28 `EN_ONLY`, 10 `EN_ZH_MIXED`, and 1 `ZH_ORIGINAL_WITH_EN_TERMS` (#254, HOLD).
- Commit inventory: 313 records — 312 `EN_ONLY` and 1 `MIXED` (C168).
- Issue records are anchored by `body_sha256`.
- Commit records are anchored by `sha` and `msg_sha256`.
- Commit language classification is based on the substantive content of the complete commit message.

Registration means that the historical object's language state has been identified and recorded. It does not mean that the object's content has been translated, rewritten, or migrated.

**中文**

#### 语言分类与迁移边界

Issue 与 Commit 清单是两个独立的分类集合，必须分别统计。

- Issue 清单：39 条——28 条 `EN_ONLY`、10 条 `EN_ZH_MIXED`、1 条 `ZH_ORIGINAL_WITH_EN_TERMS`（#254，HOLD）。
- Commit 清单：313 条——312 条 `EN_ONLY`、1 条 `MIXED`（C168）。
- Issue 记录以 `body_sha256` 为锚点。
- Commit 记录以 `sha` 和 `msg_sha256` 为锚点。
- Commit 语言分类依据完整提交消息的实质内容判定。

完成登记仅表示历史对象的语言状态已被识别并记录，不表示对象内容已经翻译、重写或完成双语迁移。

---

### 5.5 Historical Commit protection / 历史 Commit 保护

**EN**

#### Historical Commit Integrity and Registration Protection

Historical Git Commit objects must remain unchanged by the inventory and registration process.

The `sha` identifies the historical Commit object, while `msg_sha256` anchors the complete commit message content used for language classification.

Any correction to an inventory classification must be recorded as a separate registration correction, with the affected Commit, previous classification, review basis, and corrected classification identified. It must not be implemented by rewriting the historical Commit message.

Completing the inventory is not evidence of bilingual migration or authorization to rewrite historical Git objects.

**中文**

#### 历史 Commit 完整性与登记保护

历史 Git Commit 对象不得因清点或登记过程而被修改。

`sha` 用于标识历史 Commit 对象；`msg_sha256` 用于锚定语言分类所依据的完整提交消息内容。

如需更正登记分类，必须以独立登记更正记录的方式处理，明确列出受影响的 Commit、原分类、复核依据及更正后的分类。不得通过重写历史 Commit 消息实施更正。

完成清单登记不构成双语迁移完成的证据，也不构成改写历史 Git 对象的授权。

---

## 6. Independent review / 独立审查

### 6.1 Review record / 审查记录

- Review session: 6afeab2e-f7b8-83ec-b2fe-195ff144c330
- Review package: 125649 bytes
- Full harvested review: T8-INDEPENDENT-REVIEW-FULL.md
- Full review text length: 11444 characters
- Review mode: Independent, read-only
- Final disposition: FAIL — NEEDS REVISION

### 6.2 Review statistics / 审查统计

| Disposition | Count |
|---|---:|
| PASS | 8 |
| PASS WITH FINDINGS | 3 |
| PARTIAL | 1 |
| FAIL | 2 |
| NOT TESTABLE | 1 |

### 6.3 Findings / 发现

This table is the R6 review output, retained as a bound snapshot per §0. Its `Status` column records the state as found by R6 and is not maintained; current finding states live in §9 and §10.

本表为 R6 审查输出，按 §0 作为绑定快照保留。其 `Status` 列记录的是 R6 当时的发现状态，不受维护；当前 finding 状态以 §9 与 §10 为准。

| Finding | Severity | Status | Summary |
|---|---|---|---|
| F-01 | — | CLOSED | Accepted closure |
| F-02 | P1 | OPEN | Future repository inheritance lacks executable enforcement |
| F-03 | — | PARTIAL | Partial remediation does not establish complete closure |
| F-04 | — | PARTIAL | Partial remediation does not establish complete closure |
| F-05 | — | NOT_CONFIRMED | Historical migration cannot be inferred |
| F-06 | P2 | OPEN | Historical inventory incomplete |
| F-07 | P2 | OPEN | Blob SHA evidence transcription inconsistency |

### 6.4 F-02 remediation requirements / F-02 修复条件

**EN**

#### F-02 — Independent Validator and CI Integration Status

F-02 has two distinct requirements:

1. **Requirement 1 — validator integrated and invoked by CI: COMPLETE / VERIFIED, ADVISORY (non-blocking).**
   - Workflow: `.github/workflows/bilingual-docs.yml`, blob `fbb01f4cf6c1046fb4f3f6f962d1caed921577b2`.
   - Validator: `scripts/check_bilingual_docs.py`, blob `cfae34de1d07d4366850d439cb7c1e643d43cfae`.
   - The workflow step `Check paired documentation and PR manifest` runs `python3 scripts/check_bilingual_docs.py`.
   - The validator's `main()` calls `check_policy_inheritance(body, changed)` and emits its results as non-blocking notices; those results are not added to the gate's error set.
- Rationale for advisory scope: the declaration requirement originates from the unadopted GOV-DOC-001 v1.2 draft, so a blocking check would impose an unapproved normative obligation through tooling. Enforcement is deferred until the requirement is formally adopted.

2. **Requirement 2 — corresponding required check configured and enforced: COMPLETE / VERIFIED.**
   - Historical state, dated: at the 2026-11-20 readback both `GET /branches/main/protection` and `GET /rulesets` returned HTTP 403 — `{"message":"Upgrade to GitHub Pro or make this repository public to enable this feature."}` — because the repository was private under a plan without those settings. That reading is superseded on 2026-11-25 and is retained only as the record of the earlier blocker.
   - Current readings (2026-11-25): the repository is public (`private: false`, `visibility: public`); `GET /branches/main/protection` returns HTTP 200 with `required_status_checks.strict: true`, `enforce_admins.enabled: true`, and 16 contexts, one of which is `GOV-DOC-001 structural checks`; `GET /rulesets` returns HTTP 200 with `[]`, so the enforcement is classic branch protection rather than a ruleset. `required_pull_request_reviews` is absent.
   - Enforcement evidence, not inference: `PUT /pulls/1038/merge` on PR #1038 at head `b5cf4f25` was refused with HTTP 405 and the raw message `Required status check "rust-workspace-test" is failing.`, although `mergeable: true` had been reported immediately before. The platform therefore does block a merge on a failing required check. See §7.2.2.
   - Scope: what is verified is that the workflow job `GOV-DOC-001 structural checks` is a required check and that the platform enforces required checks. The declaration step inside that job (`check_policy_inheritance`) remains advisory — the job is blocking; one of its steps remains advisory.

**F-02 overall status: COMPLETE / VERIFIED** on both requirements. CI integration is verified, and required-check enforcement is measured rather than inferred. The advisory caveat is kept separate because collapsing it into the closure would be a new false claim: the declaration step `check_policy_inheritance` inside `scripts/check_bilingual_docs.py` is still non-blocking — the job is blocking; one of its steps remains advisory. A successful workflow run is still not proof of platform enforcement by itself; the proof here is the 2026-11-25 protection readback plus the PR #1038 merge rejection.

**中文**

#### F-02 — 独立校验器与 CI 接入状态

F-02 包含两个相互独立的要求：

1. **要求 1——校验器已接入并由 CI 调用：COMPLETE / VERIFIED（完成/已验证），ADVISORY（非阻断）。**
   - Workflow：`.github/workflows/bilingual-docs.yml`，blob `fbb01f4cf6c1046fb4f3f6f962d1caed921577b2`。
   - 校验器：`scripts/check_bilingual_docs.py`，blob `cfae34de1d07d4366850d439cb7c1e643d43cfae`。
   - Workflow 步骤 `Check paired documentation and PR manifest` 实际运行 `python3 scripts/check_bilingual_docs.py`。
   - 校验器的 `main()` 调用了 `check_policy_inheritance(body, changed)`，其结果以非阻断提示输出，不并入门禁错误集。
- 非阻断的理由：声明要求源自尚未采纳的 GOV-DOC-001 v1.2 草案，若设为阻断即在工具层施加未获批准的规范义务；正式采纳前不予强制。

2. **要求 2——对应 required check 已配置并强制执行：COMPLETE / VERIFIED（完成/已验证）。**
   - 历史状态（带时点）：2026-11-20 读取时 `GET /branches/main/protection` 与 `GET /rulesets` 均返回 HTTP 403——`{"message":"Upgrade to GitHub Pro or make this repository public to enable this feature."}`——原因是当时仓库为私有且所处计划不支持该设置。该读数已于 2026-11-25 被取代，仅作为当时阻塞的记录保留。
   - 当前读数（2026-11-25）：仓库已公开（`private: false`、`visibility: public`）；`GET /branches/main/protection` 返回 HTTP 200，`required_status_checks.strict: true`、`enforce_admins.enabled: true`、共 16 个 contexts，其中包含 `GOV-DOC-001 structural checks`；`GET /rulesets` 返回 HTTP 200，内容为 `[]`，故强制来自经典 branch protection 而非 ruleset。`required_pull_request_reviews` 缺失。
   - 强制执行证据（实测而非推断）：PR #1038 在 head `b5cf4f25` 上的 `PUT /pulls/1038/merge` 被拒绝，HTTP 405，原始消息 `Required status check "rust-workspace-test" is failing.`；而此前一刻平台仍报告 `mergeable: true`。因此平台确实会以失败的 required check 阻断合并。见 §7.2.2。
   - 适用范围：已验证的是 workflow job `GOV-DOC-001 structural checks` 属于 required check，且平台对 required check 强制执行。该 job 内的声明步骤（`check_policy_inheritance`）仍为非阻断——job 为阻断，其内部仍有一步为非阻断。

**F-02 总体状态：COMPLETE / VERIFIED（完成/已验证）**，两项要求均已满足。CI 接入已验证，required check 强制执行已实测而非推断。advisory 的限定仍单列，因为把它并入关闭结论会构成新的错误陈述：`scripts/check_bilingual_docs.py` 内的声明步骤 `check_policy_inheritance` 仍为非阻断——job 为阻断；其内部仍有一步为非阻断。单次 workflow 成功运行本身仍不构成平台强制的证明；此处的证明是 2026-11-25 的 protection 读回与 PR #1038 的合并拒绝。

### 6.5 F-06 remediation requirements / F-06 修复条件

**EN**

#### F-06 — Inventory Integrity and Migration Status

The historical language inventories are finalized with the following counts:

- **39 Issues:** 28 `EN_ONLY`, 10 `EN_ZH_MIXED`, and 1 `ZH_ORIGINAL_WITH_EN_TERMS` (#254, HOLD).
- **313 Commits:** 312 `EN_ONLY` and 1 `MIXED` (C168).

The Issue inventory uses `body_sha256` anchors. The Commit inventory uses `sha` and `msg_sha256` anchors. Commit classifications are based on the substantive content of the complete commit message.

Closure requires reconciliation of record counts, classification totals, object uniqueness, identity matching, anchor completeness, and missing or duplicate records. Issue #254 must remain included in the 39-record set, with HOLD and its explicit exit conditions preserved.

Finalizing the inventories does not establish completion of historical bilingual migration.

**中文**

#### F-06 — 清单完整性与迁移状态

历史语言状态清单已定稿，数量如下：

- **39 条 Issue：**28 条 `EN_ONLY`、10 条 `EN_ZH_MIXED`、1 条 `ZH_ORIGINAL_WITH_EN_TERMS`（#254，HOLD）。
- **313 条 Commit：**312 条 `EN_ONLY`、1 条 `MIXED`（C168）。

Issue 清单使用 `body_sha256` 锚点；Commit 清单使用 `sha` 和 `msg_sha256` 锚点。Commit 分类依据完整提交消息的实质内容判定。

关闭前必须对记录数量、分类总数、对象唯一性、对象身份匹配、锚点完整性及缺漏或重复情况完成对账。Issue #254 必须继续包含在 39 条集合内，并保留 HOLD 及其明确退出条件。

清单定稿不代表历史内容双语迁移已经完成。

---

### 6.6 F-07 correction / F-07 更正

**EN**

#### F-07 — Authoritative Baseline and Correction Record

The F-07 correction record has been registered in PR comment `7006445553`.

The authoritative D1 baseline blob is:

```text
66517d39
```

Subsequent verification, citation, and status decisions must use this authoritative D1 baseline.

The PR comment provides traceability for the correction record. It does not replace the authoritative D1 baseline and does not independently change any other normative status, migration status, or authorization boundary.

**中文**

#### F-07 — 权威基线与更正记录

F-07 更正记录已登记于 PR 评论 `7006445553`。

D1 权威基线 blob 为：

```text
66517d39
```

后续核验、引用及状态判断必须以该 D1 权威基线为准。

PR 评论用于追踪更正记录，不替代 D1 权威基线，也不会单独改变其他规范状态、迁移状态或授权边界。

---

### 6.7 Review limitations / 审查限制

The following remain unverified by the independent review evidence:

- Full historical Commit inventory.
- Complete historical object-level PR classification.
- Executable repository inheritance enforcement.
- A successful complete CI Exact-Head verification.
- Current-main direct branch-ref SHA at the time of the original review.

T9 directly verified current main HEAD after the independent review.

本轮直接读取 main HEAD 的证据晚于原独立审查，不能追溯性地改写独立审查当时的取证范围。

## 7. CI verification and remediation / CI 验证与修复

### 7.1 Actual CI result / 实际 CI 结果

**EN**

#### F-02 CI Verification Result

The workflow and validator are integrated:

- Workflow blob: `fbb01f4cf6c1046fb4f3f6f962d1caed921577b2`.
- Validator script blob: `cfae34de1d07d4366850d439cb7c1e643d43cfae`.
- Workflow job: `GOV-DOC-001 structural checks`.
- Executed step: `Check paired documentation and PR manifest`.
- The step runs `python3 scripts/check_bilingual_docs.py`; the script's `main()` invokes `check_policy_inheritance()` in ADVISORY mode (results printed as notices, never blocking).

Three successful workflow executions are independently evidenced:

| Run ID | Tested PR head | Job ID | Job / step result | UTC execution window |
|---|---|---|---|---|
| `44542512889` | `70219731485040e2974d537080f994108ee1d989` | `135624335886` | Job SUCCESS; validator step SUCCESS | `14:19:42Z–14:19:45Z`, 2026-11-19 |
| `44546301573` | `47369925ace93821eab82e4cec8418f8d7505d64` | `135637661718` | Job SUCCESS; validator step SUCCESS | `14:40:30Z–14:40:33Z`, 2026-11-19 |
| `44559550224` | `bbfe046b9307c9bfffd7606c4a7caadcb1de32f8` | `135684753485` | Job SUCCESS; validator step SUCCESS | `15:51:45Z–15:51:48Z`, 2026-11-19 |

All three executions reported `Bilingual documentation and prompt-library gate: PASS (11 changed paths inspected).` These runs verify workflow invocation and successful execution on their respective heads. They do not verify platform required-check enforcement.

The earlier structural CI failure run `44477435608` remains historical evidence and is not overwritten by these later successful runs.

**Status:** Requirement 1 COMPLETE / VERIFIED (advisory, non-blocking); Requirement 2 COMPLETE / VERIFIED (2026-11-25, §7.2.2); F-02 overall COMPLETE / VERIFIED.

**中文**

#### F-02 CI 验证结果

Workflow 与校验器已完成接入：

- Workflow blob：`fbb01f4cf6c1046fb4f3f6f962d1caed921577b2`。
- 校验器脚本 blob：`cfae34de1d07d4366850d439cb7c1e643d43cfae`。
- Workflow job：`GOV-DOC-001 structural checks`。
- 实际执行步骤：`Check paired documentation and PR manifest`。
- 该步骤运行 `python3 scripts/check_bilingual_docs.py`；脚本的 `main()` 以 ADVISORY 模式调用 `check_policy_inheritance()`（结果仅作提示，不阻断）。

已有三次成功的 workflow 执行证据：

| Run ID | 被测 PR head | Job ID | Job / 步骤结果 | UTC 执行时间 |
|---|---|---|---|---|
| `44542512889` | `70219731485040e2974d537080f994108ee1d989` | `135624335886` | Job SUCCESS；校验步骤 SUCCESS | 2026-11-19 `14:19:42Z–14:19:45Z` |
| `44546301573` | `47369925ace93821eab82e4cec8418f8d7505d64` | `135637661718` | Job SUCCESS；校验步骤 SUCCESS | 2026-11-19 `14:40:30Z–14:40:33Z` |
| `44559550224` | `bbfe046b9307c9bfffd7606c4a7caadcb1de32f8` | `135684753485` | Job SUCCESS；校验步骤 SUCCESS | 2026-11-19 `15:51:45Z–15:51:48Z` |

三次执行均报告 `Bilingual documentation and prompt-library gate: PASS (11 changed paths inspected).` 这些运行证明 workflow 在各自 head 上实际调用并成功执行校验器，但不证明平台 required check 已强制生效。

较早的结构 CI 失败运行 `44477435608` 保留为历史证据，不被后续成功运行覆盖。

**状态：**要求 1 COMPLETE / VERIFIED（advisory，非阻断）；要求 2 COMPLETE / VERIFIED（2026-11-25，§7.2.2）；F-02 总体 COMPLETE / VERIFIED。

### 7.2 Actual gate behavior / 门禁实际行为

**EN**

#### F-02 Gate Behavior — Verified Execution vs Platform Enforcement

The three successful workflow runs (including run `44559550224` on the v2.2 report-version-alignment head) establish that the PR workflow invokes the validator and that the validator step completed successfully on the recorded heads.

They do **not** establish:

- The check is configured as a required check in repository branch protection or a ruleset.
- A failing validator result is enforced by the platform as a merge blocker.
- The required-check configuration can be administered under the repository's current private-repository plan.

The branch-protection and ruleset API requests returned HTTP 403 with the GitHub plan-limit message recorded in §6.4 **at the 2026-11-20 readback**. That reading is historical: on 2026-11-25 both endpoints returned HTTP 200 — protection with `strict: true`, `enforce_admins.enabled: true` and 16 contexts including `GOV-DOC-001 structural checks`, and `/rulesets` with `[]` — and `PUT /pulls/1038/merge` was refused with 405 on a failing required check. Platform enforcement is therefore no longer `NOT_VERIFIED` and no longer a platform-limited blocker; see §7.2.2. The bullet list above still holds: workflow runs alone establish none of the three items.

**中文**

#### F-02 门禁行为——已验证执行与平台强制的区别

两次成功的 workflow 运行证明 PR workflow 实际调用了校验器，且校验器步骤在所记录的 head 上成功完成。

但这些证据**不能**证明：

- 该 check 已在仓库 branch protection 或 ruleset 中配置为 required check；
- 校验器失败时，平台会将其强制作为合并阻断条件；
- 当前私有仓库计划允许管理员配置 required-check 强制规则。

分支保护及 ruleset API 请求在 **2026-11-20 读取时**返回 §6.4 所记录的 GitHub 计划限制 HTTP 403。该读数为历史读数：2026-11-25 两个端点均返回 HTTP 200——protection 为 `strict: true`、`enforce_admins.enabled: true`、16 个 contexts 且含 `GOV-DOC-001 structural checks`，`/rulesets` 为 `[]`——且 `PUT /pulls/1038/merge` 因失败的 required check 被以 405 拒绝。因此平台强制状态不再是 `NOT_VERIFIED`，也不再构成平台限制阻塞；见 §7.2.2。上述三条「不能证明」仍成立：仅凭 workflow 运行无法建立其中任何一项。

### 7.2.1 Live platform recheck / 平台实时复核 (2026-11-20)

**EN**

The current-main branch object was read at `main@9546f78d364b5a1dd1fa2206b34255be9c7fb1a7`:

- `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main` returned `protected=false`; embedded `protection.enabled=false`; `required_status_checks.enforcement_level=off`; `contexts=[]`; `checks=[]`.
- `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` returned HTTP 403 with the raw message: `Resource not accessible by integration`.
- `GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets?per_page=100` returned HTTP 403 with the raw message: `Upgrade to GitHub Pro or make this repository public to enable this feature.`

The branch object is direct evidence that branch-protection required checks are not enabled on this readback. The rulesets endpoint is unavailable, so ruleset-based enforcement cannot be ruled in or out. **F-02 Requirement 2 therefore remains NOT_VERIFIED; F-02 overall remains PARTIAL.** No deliberately failing required-check experiment or platform merge-rejection evidence was run. Do not treat successful workflow runs as proof of platform enforcement.

**External dependency and verification path:** a repository administrator / plan owner must make branch-protection and ruleset state inspectable (integration permission for the branch-protection endpoint and an eligible GitHub plan/visibility for rulesets). Verify by successfully reading both endpoints, confirming the exact required check context is configured, then running a deliberately failing check and observing GitHub reject the merge. This paragraph records a limitation; it does not claim enforcement is enabled.

**Superseded status (pointer):** the readings in this subsection are the state at the 2026-11-20 readback and are superseded by §7.2.2 (2026-11-25). The measurements above are not rewritten and remain bound to their readback.

**中文**

当前 main 分支对象读取基线为 `main@9546f78d364b5a1dd1fa2206b34255be9c7fb1a7`：

- `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main` 返回 `protected=false`；嵌入的 `protection.enabled=false`；`required_status_checks.enforcement_level=off`；`contexts=[]`；`checks=[]`。
- `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` 返回 HTTP 403，原始消息：`Resource not accessible by integration`。
- `GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets?per_page=100` 返回 HTTP 403，原始消息：`Upgrade to GitHub Pro or make this repository public to enable this feature.`。

分支对象直接证明本次读取时 branch-protection required checks 未启用。rulesets 端点不可读取，因此无法排除或确认 ruleset 强制规则。**F-02 要求 2 仍为 NOT_VERIFIED；F-02 总体仍为 PARTIAL。**本次未运行故意失败的 required-check 实验，也没有平台拒绝合并证据。不得把 workflow 成功运行当作平台强制的证明。

**外部依赖与验证路径：**仓库管理员 / 计划负责人需使 branch-protection 与 rulesets 状态可读取（branch-protection 端点需具备集成读取权限，rulesets 需符合 GitHub 计划/可见性要求）。验证时先成功读取两个端点、确认精确 required-check context 已配置，再运行故意失败的 check 并观察 GitHub 拒绝合并。本段仅记录限制，不声称强制规则已经启用。

**取代状态（指针）：**本小节的读数为 2026-11-20 读取时点的状态，已由 §7.2.2（2026-11-25）取代。上述测量不作改写，仍绑定于其读取时刻。

### 7.2.2 Live platform recheck / 平台实时复核 (2026-11-25)

**EN**

The platform state was re-read on 2026-11-25 with the same `GET` requests recorded in §7.2.1:

- `GET /repos/oahcom/AiMemoryBrainArchitecture` returned `private: false`, `visibility: public`.
- `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` returned HTTP 200: `required_status_checks.strict: true`; `required_status_checks.contexts` length **16**, containing `GOV-DOC-001 structural checks`; `enforce_admins.enabled: true`; the key `required_pull_request_reviews` absent.
- `GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets` returned HTTP 200 with body `[]`. Enforcement is therefore classic branch protection, not a ruleset.
- The 16 contexts: `GOV-DOC-001 structural checks`, `Branch freshness vs base`, `audit`, `GOV-DOC-002 metadata checks`, `BMCP protocol index (hard gate)`, `BMCP conformance suite (hard gate)`, `Schema non-empty audit (hard gate)`, `Bilingual docs coverage (ratchet)`, `Rust clippy (hard gate)`, `Repository hygiene (hard gate)`, `Rust format (hard gate)`, `Rust doctests (hard gate)`, `Session Evidence`, `Session Evidence self-test (base)`, `Session Evidence self-test (head)`, `rust-workspace-test`.

**Failure-blocking behaviour, measured rather than inferred.** PR #1038 at head `b5cf4f25` was reported `mergeable: true` and then refused by `PUT /pulls/1038/merge` with HTTP 405 and the raw message `Required status check "rust-workspace-test" is failing.`; the PR was closed unmerged. `14-ai-development/PR-GOVERNANCE-001.md:288` on main already records the same experiment as passed on 2026-11-25, including the 405 text and the `mergeable: true` observation immediately before the rejection. This is the deliberately failing experiment that §7.2.1 recorded as not having been run.

**What this establishes, and what it does not.** The control exercises `rust-workspace-test`, so it demonstrates platform enforcement of required checks in general; that `GOV-DOC-001 structural checks` lies in the same required set is read from the contexts list, not from that single rejection. It does not establish review enforcement: `required_pull_request_reviews` is absent, so a merge needs the checks but not an approving review. Nor does it make the declaration step blocking — `check_policy_inheritance` inside `scripts/check_bilingual_docs.py` still emits notices only.

**中文**

2026-11-25 以 §7.2.1 所记录的同一组 `GET` 请求重新读取平台状态：

- `GET /repos/oahcom/AiMemoryBrainArchitecture` 返回 `private: false`、`visibility: public`。
- `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` 返回 HTTP 200：`required_status_checks.strict: true`；`required_status_checks.contexts` 长度为 **16**，含 `GOV-DOC-001 structural checks`；`enforce_admins.enabled: true`；`required_pull_request_reviews` 键缺失。
- `GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets` 返回 HTTP 200，内容为 `[]`。故强制来自经典 branch protection，而非 ruleset。
- 16 个 contexts 为：`GOV-DOC-001 structural checks`、`Branch freshness vs base`、`audit`、`GOV-DOC-002 metadata checks`、`BMCP protocol index (hard gate)`、`BMCP conformance suite (hard gate)`、`Schema non-empty audit (hard gate)`、`Bilingual docs coverage (ratchet)`、`Rust clippy (hard gate)`、`Repository hygiene (hard gate)`、`Rust format (hard gate)`、`Rust doctests (hard gate)`、`Session Evidence`、`Session Evidence self-test (base)`、`Session Evidence self-test (head)`、`rust-workspace-test`。

**失败阻断行为：实测而非推断。**PR #1038 在 head `b5cf4f25` 上先被报告 `mergeable: true`，随后 `PUT /pulls/1038/merge` 被拒绝，HTTP 405，原始消息 `Required status check "rust-workspace-test" is failing.`；该 PR 以未合并状态关闭。main 上的 `14-ai-development/PR-GOVERNANCE-001.md:288` 已把同一实验记录为 2026-11-25 通过，含 405 原文以及拒绝前一刻的 `mergeable: true` 观测。这正是 §7.2.1 记为「尚未运行」的那次故意失败实验。

**本小节建立了什么、没有建立什么。**该对照使用的是 `rust-workspace-test`，故它证明的是平台对 required check 的一般性强制执行；`GOV-DOC-001 structural checks` 与之处于同一 required 集合，这一点读自 contexts 列表，而非读自那一次拒绝。本小节不建立审查强制：`required_pull_request_reviews` 缺失，合并需要检查通过，但不需要批准审查。它也不使声明步骤变为阻断——`scripts/check_bilingual_docs.py` 内的 `check_policy_inheritance` 仍只输出提示。

### 7.3 Recommended remediation / 建议修复

**EN**

#### F-02 Required Follow-up

1. Integrate the independent validator into the intended CI workflow.
2. Execute the workflow and retain evidence of the validator's actual invocation and result.
3. Configure the corresponding check as required where required by the repository's governance rules.
4. Verify that the required check is enforced, including its failure behavior.
5. Update F-02 from PARTIAL only after the above evidence has been reviewed and accepted.

The existing local result of 6/6 PASS must remain distinguishable from CI execution and branch-protection enforcement.

**中文**

#### F-02 后续必需工作

1. 将独立校验器接入指定 CI workflow。
2. 实际运行 workflow，并保留校验器被调用及其运行结果的证据。
3. 按仓库治理规则要求，将对应 check 配置为 required check。
4. 验证 required check 确实生效，包括校验失败时的阻断行为。
5. 只有在上述证据均已审查并接受后，才可将 F-02 从 PARTIAL 更新为完成状态。

现有本地 6/6 PASS 结果必须与 CI 实际执行及分支保护强制检查证据明确区分。

---

### 7.4 Required PR body declaration / PR 正文声明

After the allowlist change is committed, the PR body must include:

```text
BILINGUAL-MANIFEST: COMPLETE
```

The declaration means all changed normative files have either:

- Both English and Chinese counterpart files changed and present; or
- An exact self-contained bilingual source explicitly listed in EMBEDDED_BILINGUAL_SOURCES.

It does not mean independent semantic review has passed.

It does not authorize merge or policy adoption.

### 7.5 Exception decision / 豁免处置

**EN**

#### Exception and Normative Status Protection

The following status boundaries remain unchanged:

1. **v1.1: NORMATIVE.** It remains the current normative version.
2. **v1.2: DRAFT.** It remains a draft and must not be represented as formally adopted.
3. **MIGRATION_DEBT != EXEMPTION.** Outstanding migration debt does not constitute an exemption.
4. No Owner approval may be inferred for any matter without explicit approval evidence.
5. No normative adoption, PR merge authorization, or historical content migration completion may be inferred.
6. Inventory registration, test success, comment records, or document revisions do not independently establish any of the approvals, adoptions, authorizations, or migration completions above.

Any exception must have explicit, traceable authorization. Silence, implementation progress, or the existence of a tracking record must not be treated as approval.

**中文**

#### 豁免与规范效力保护

以下状态边界保持不变：

1. **v1.1：NORMATIVE。**继续作为现行规范性版本。
2. **v1.2：DRAFT。**仍为草案，不得表述为已正式采纳。
3. **MIGRATION_DEBT != EXEMPTION。**未完成的迁移债务不构成豁免。
4. 对于没有明确批准证据的事项，不得推定 Owner 已批准。
5. 不得推定规范已被采纳、PR 已获合并授权或历史内容迁移已经完成。
6. 清单登记、测试通过、评论留痕或文档修订，均不能单独证明上述批准、采纳、授权或迁移完成。

任何豁免都必须具有明确且可追踪的授权。不得将沉默、实施进展或存在跟踪记录视为批准。

---

### 7.6 CI rerun / CI 重跑

After the script change and PR body update:

1. Re-read the exact PR head SHA.
2. Re-read the current main SHA.
3. Verify all seven embedded source paths.
4. Verify the complete manifest.
5. Run the structural check.
6. Record the new workflow run and job identifiers.
7. Require successful Exact-Head verification.

Until then, CI status remains FAILURE.

## 8. Acceptance matrix / 验收矩阵

AC-07 was blank in the original task definition. Its missing criterion must not be invented.

| AC | Criterion | Execution evidence | Independent review / final result |
|---|---|---|---|
| AC-01 | Full v1.1 inheritance | v1.1 read; D1/D6 committed | PARTIAL — inheritance is to v1.1 only, since v1.2 is not adopted. F-03/F-04 are `CLOSED (method-bound)` in §9 and are no longer cited here; the earlier wording treated them as an open blocker, which drifted from the registry |
| AC-02 | Issue bilingual requirements | Five templates/updates read back | Execution PASS; independent criterion mapping NOT_RECORDED |
| AC-03 | Umbrella Requirement bilingual requirements | D1/D4 and five Issue updates | Execution PASS; independent criterion mapping NOT_RECORDED |
| AC-04 | Commit Message bilingual requirements | D5 and actual bilingual Commit | Execution PASS; historical inventory incomplete |
| AC-05 | PR bilingual title/body | PR title and body bilingual | PARTIAL — the historical CI failure run 44477435608 is retained; the gate passes on the current exact head, but platform required-check enforcement is unverified (F-02 R2) |
| AC-06 | Future repository inheritance | D1/D6 drafted and committed | FAIL — F-02 Requirement 2 NOT_VERIFIED (platform-limited); v1.2 not adopted |
| AC-07 | Original criterion unspecified | No criterion supplied | NOT TESTABLE |
| AC-08 | Stable identifier preservation | Exact identifiers and SHA manifest checked | Execution PASS; independent mapping NOT_RECORDED |
| AC-09 | Status preservation | Five Issues remain OPEN; Requirement Status RECORDED | Execution PASS |
| AC-10 | No fabricated evidence | Unknown fields and source gaps preserved | Execution PASS within available evidence |
| AC-11 | Historical Commit immutability | No rewrite or force-push | Execution PASS |
| AC-12 | Historical migration registration | Issue/Commit/PR aggregate inventory prepared | PARTIAL — F-06 object reconciliation CLOSED (2026-11-20); migration itself not performed |
| AC-13 | Bilingual normative clauses | D1–D7 are embedded bilingual documents | Independent semantic parity not fully accepted |
| AC-14 | Complete file/change manifest | Seven files and five Issue updates verified | PARTIAL — inventory complete (F-06 CLOSED); historical migration not performed |
| AC-15 | Reproducible independent acceptance | Review package and exact file SHAs recorded | FAIL / BLOCKED — CI failure and outstanding findings |

Execution PASS does not imply independent review PASS.

执行自检 PASS 不等于独立审查 PASS。

独立的当前状态补充表

**EN**

| Item | Current status | Acceptance boundary |
|---|---|---|
| F-02 | PARTIAL | Validator and tests committed; corrected local tests 6/6 PASS. Declaration check is ADVISORY (non-blocking); CI workflow integration verified; required-check enforcement evidence remains outstanding. |
| F-06 Issue inventory | Inventory finalized | 39 records: 28 EN_ONLY, 10 EN_ZH_MIXED, 1 ZH_ORIGINAL_WITH_EN_TERMS (#254, HOLD). Each record requires a matching body_sha256. |
| F-06 Commit inventory | Inventory finalized | 313 records: 312 EN_ONLY, 1 MIXED (C168). Each record requires matching sha and msg_sha256; classification is based on the complete commit message. |
| F-07 | Correction recorded | PR comment `7006445553`; authoritative D1 blob `66517d39`. |
| Normative status | Unchanged | v1.1 NORMATIVE; v1.2 DRAFT. |
| Migration and exemption | Not interchangeable | MIGRATION_DEBT != EXEMPTION. Registration does not establish migration completion. |

**中文**

| 项目 | 当前状态 | 验收边界 |
|---|---|---|
| F-02 | PARTIAL | 校验器及测试已提交；修复后的本地测试 6/6 PASS。声明校验为 ADVISORY（非阻断）；CI workflow 接入已验证；required check 强制执行证据仍为未完成。 |
| F-06 Issue 清单 | 登记定稿 | 39 条：28 条 EN_ONLY、10 条 EN_ZH_MIXED、1 条 ZH_ORIGINAL_WITH_EN_TERMS（#254，HOLD）。每条记录均须具有匹配的 body_sha256。 |
| F-06 Commit 清单 | 登记定稿 | 313 条：312 条 EN_ONLY、1 条 MIXED（C168）。每条记录均须具有匹配的 sha 和 msg_sha256；分类依据完整提交消息判定。 |
| F-07 | 更正已登记 | PR 评论 `7006445553`；D1 权威 blob `66517d39`。 |
| 规范状态 | 不变 | v1.1 为 NORMATIVE；v1.2 为 DRAFT。 |
| 迁移与豁免 | 不可互相替代 | MIGRATION_DEBT != EXEMPTION。登记完成不构成迁移完成证明。 |

---

## 9. Outstanding blockers and next actions / 未解决阻塞与后续行动

### Finding registry / finding 登记表

Every finding raised against this deliverable appears here with a state and a basis. A finding that is absent from this table is not thereby closed; the registry exists so that no finding can be dropped silently between revisions, which is what had happened to F-01, F-03, F-04 and F-05 — they were listed only in the bound R6 snapshot (§6.3) and had no maintained state anywhere in §9 or §10.

本交付物引发的每一项 finding 均在此列出状态与依据。不在本表中出现并不意味着已关闭；本登记表存在的目的，就是防止 finding 在修订之间被静默遗落——F-01、F-03、F-04、F-05 正是如此：它们只出现在绑定快照 §6.3 中，在 §9 与 §10 里没有任何受维护的状态。

| # | Severity | State | Basis and where it is maintained |
|---|---|---|---|
| F-01 | — | `CLOSED` | Accepted closure recorded by the R6 review (§6.3). No counter-evidence recorded since. / R6 审查记录的已接受关闭（§6.3）。 |
| F-02 | P1 | `COMPLETE / VERIFIED` (2026-11-25) | Requirement 1 `COMPLETE / VERIFIED` (workflow integration, §7.1). Requirement 2, re-derivable: object `GET /branches/main/protection`, expected HTTP `200` with `required_status_checks.contexts` containing `GOV-DOC-001 structural checks`, actual `200` with 16 contexts containing it (§7.2.2); negative control `PUT /pulls/1038/merge`, expected `405`, actual `405` with `Required status check "rust-workspace-test" is failing.` Scope, stated so the closure is not over-read: the declaration step inside the job is still advisory, and `required_pull_request_reviews` is absent, so this is required-check enforcement only. Maintained in §9 P1, §7.2.2 and §10. / 要求 1 与要求 2 均可复现验证：`/protection` 200 且 16 个 contexts 含 `GOV-DOC-001 structural checks`；反向对照 `PUT /pulls/1038/merge` 预期 405、实际 405。job 内声明步骤仍为非阻断，且无审查强制。 |
| F-03 | — | `CLOSED (method-bound)` | The finding stated that partial remediation does not establish complete closure. That is a rule about method, not a defect with a patch. §0 and §9 now implement the distinction: remediation is recorded separately from state, and closure requires re-derivable evidence. **Basis proposed in this revision; requires this PR’s review to confirm.** Reopens if any revision records a `CLOSED` state whose basis is only a remediation artifact — check c9 below is the detector. / 该 finding 是方法性规则而非可补丁缺陷；依据本修订提出，待本 PR 审查确认；若任一修订将「仅以修复产物为依据」的状态记为 `CLOSED`，即重新开启（核对 c9 为检测器）。 |
| F-04 | — | `CLOSED (method-bound)` | Same basis and same reopen condition as F-03, recorded separately because R6 listed it as a separate row. / 与 F-03 同依据、同重开条件；R6 列为独立行，故分列。 |
| F-05 | — | `LIMITATION` | "Historical migration cannot be inferred" meets all three §0 conditions and the exclusion is enumerated rather than asserted. Paths examined: (1) infer migration from the 313-commit inventory — excluded, the inventory records message language, not whether content was migrated; (2) infer it from the 39-issue inventory — excluded, same reason; (3) re-run the historical sessions that produced the content — excluded, no such record carrier is available in this repository. No fourth path was identified. Confirming review: this PR. Recorded per §0 so it is neither closed silently nor left `OPEN` forever; re-evaluates if any condition fails or a fourth path is found. / 满足 §0 三条件，且排除是穷举而非声称：已排查①由 313 条 Commit 清单推得迁移（排除：清单只记录消息语种）、②由 39 条 Issue 清单推得（同因排除）、③重跑历史会话记录（排除：本仓库无此载体），未发现第四条路径；确认审查：本 PR。 |
| F-06 | P2 | `CLOSED` (2026-11-20) | Object reconciliation in `00-governance/reports/f06-object-reconciliation.md`; the 12 later PR groupings were confirmed by A Integration and registered in migration register §8.4.2 (commit `d344f43ce0d4b8eb9bab19da8ca30e4a518f1117`, Blob `46cabb97f63597eb3e8623c60305ed58980355f7`). The earlier "14 unassigned PRs" conclusion remains retracted. Historical migration debt is unchanged. / 对象级对账已完成；A Integration 已确认后续 12 个 PR 归组并登记于迁移登记册 §8.4.2；此前「14 个未归组 PR」结论仍为撤回。历史迁移欠账不变。 |
| F-07 | P2 | `CLOSED` | Correction recorded in PR comment `7006445553`; authoritative D1 blob `66517d39`. / 更正已登记。 |
| F-08 | P1 | `CLOSED` (2026-11-20) | §0 record boundary, §2.2 post-merge snapshot, §3.2 post-merge manifest; closure basis in §9 P1. / 关闭依据见 §9。 |
| F-09 | P1 | `CLOSED` (2026-11-20) | §6.4/§7.1/§7.2/§9/§10 separation of integration from enforcement; re-opened and re-closed on 2026-11-20 after the §11 contradiction. / 因 §11 矛盾曾重开，同日重新关闭。 |
| F-10 | P2 | `CLOSED` | PR #271 body declaration `BILINGUAL-MANIFEST: COMPLETE` recorded as execution evidence; implies no approval, adoption or merge authorisation. / 仅为执行证据。 |

Where a state here differs from the R6 snapshot in §6.3, this registry governs, because §6.3 is a bound snapshot.

若本表状态与 §6.3 的 R6 快照不一致，以本登记表为准，因为 §6.3 属于绑定快照。

### Status cross-check / 状态交叉核对

The following cross-check is run on every revision that touches a status sentence. It exists because the §11 contradiction was found only after merge, and because three acceptance-matrix rows had drifted from the finding states.

每次修订只要涉及状态句，就跑下面的交叉核对。设立理由：§11 的矛盾是合并后才发现的，且已有三行验收矩阵与 finding 状态脱节。

c1. Every sentence asserting a capability "has not been established" / 「尚未建立」 — check it names one requirement, not two.
c2. §10 rows against the finding registry — where a finding appears in both, the value must be identical. The registry is the single index; §10 is a stage ledger, so a finding absent from §10 is not a defect provided the registry entry names where its state is maintained. This wording replaces an earlier version that required §10 to carry every finding, which was unsatisfiable and therefore not a check.
c3. §11 status sentences against §7.1, §7.2, §9 and §10.
c4. §8 acceptance-matrix rows for any row that cites a finding state or a CI outcome.
c5. This registry against §6.3 — any divergence must be explained by §6.3 being a bound snapshot.
c6. Basis validity — for every state, is the cited basis still true, and is it the kind of basis that can support that state (see c9)?
c7. Maintenance location reachable — every §, comment id and file path cited as a maintenance location exists and actually carries the state.
c8. Closure conditions satisfied — where a finding states conditions for closure, each one is met; where it states a reopen condition, none has triggered.
c9. Closure/evidence consistency — the detector for the F-03/F-04 class. For each `CLOSED` row, the basis must name either (i) a re-derivable verification — object, expected value, comparison — or (ii) a rule change that makes the finding non-actionable, attributed to a review. A basis that names only a rewritten paragraph, a diff, or a partial fix is insufficient and the row must be `PARTIAL`. This check is falsifiable and the negative test is stated so it can be re-run: if F-03 were registered as `CLOSED` with the basis "v2.2 corrected §2.2 and §3.1–§3.3", c9 returns FAIL, because that names only a rewritten paragraph. The accepted basis survives c9 because it names a rule change plus review attribution, not a patch.

**c9 execution record / c9 执行记录.** c9 is a document-state check, not a script: the input is a registry row as written, the rule is the paragraph above, and the verdict is read off directly. Two tests are recorded so the check can be re-run by anyone:

| Test | Input row (as written into the registry) | Expected | Actual (2026-11-20) | Verdict |
|---|---|---|---|---|
| T1 | F-03, basis = "rule change (§0/§9 implement the distinction) + review attribution" | PASS — basis is type (ii) | PASS | check returns PASS |
| T2 | F-03, basis = "v2.2 corrected §2.2 and §3.1–§3.3" (hypothetical substituted row) | FAIL — basis is only a rewritten paragraph | FAIL | check returns FAIL |

T2 is the negative control: it substitutes the row that would have been written if the closure rested on the patch alone. It fails, so c9 is not a rule that passes everything. No automation exists for this check and none is claimed; what is claimed is that the two inputs and their expected verdicts are written down, so a later revision can be tested the same way.

**c9 执行记录**：c9 是文档状态核对而非脚本——输入是已写定的登记行，规则即上段，结论直接读出。T1：F-03 以「规则变更 + 审查归属」为依据 → 预期 PASS，实际 PASS；T2：将同一行换为「v2.2 已更正 §2.2 与 §3.1–§3.3」→ 预期 FAIL，实际 FAIL。T2 为反向对照：若关闭仅靠补丁，写出来的就是这一行，而它会失败——因此 c9 不是「什么都放过」的规则。本核对无自动化实现，也不声称有；声称的只是两个输入及其期望结果已写定，后续修订可用同法测试。

Result for this revision / 本修订核对结果：c1 clear (the only such sentence, in §11, was corrected in v2.6); c2 clear; c3 clear after v2.6; c4 **two rows drifted and were fixed here** — AC-14 still said "historical inventory incomplete" and AC-05 still said "CI FAILURE" without distinguishing the historical run from current enforcement; c5 **four findings were absent from §9/§10** and are now registered above.

本修订：c1 清（唯一此类句在 §11，v2.6 已更正）；c2 清；c3 经 v2.6 后清；c4 **两行脱节，已在本次修正**；c5 **四项 finding 未在 §9/§10 出现，已在上表登记**。

c6–c9 were run for the first time in this revision. c6 clear — all ten bases re-read and still true. c7 clear — the cited §, comment ids (`7006445553`, `7017127588`) and file path all exist and carry the stated values. c8 clear once the reopen conditions above were written; before that, the registry stated states without stating what would undo them, which is why c8 was added. c9: eight `CLOSED` rows pass; F-03 and F-04 pass only because their basis is a rule change with review attribution, and the negative test above records exactly how they would fail if that were not so.

c6–c9 首次执行。c6 清——十项依据逐一重读仍成立；c7 清——所引 §、评论 id（`7006445553`、`7017127588`）与文件路径均存在且载有所述值；c8 在补写上述重开条件后清——在此之前，登记表只写状态而不写什么会推翻该状态，这正是新增 c8 的原因；c9：八个 `CLOSED` 行通过；F-03 与 F-04 之所以通过，是因为其依据是规则变更加审查归属，而上述反例测试已记录了它们在不成立时会如何失败。

### P1

**F-02 — platform required-check enforcement**

- Requirement 1 (validator integrated and invoked by CI): COMPLETE / VERIFIED, ADVISORY (non-blocking).
- Enforcement scope (v2.4, R7 finding): the declaration check reports notices only. A blocking check would impose the unadopted v1.2 inheritance requirement through tooling; enforcement is deferred to adoption.
- Requirement 2 (required check configured and enforced): COMPLETE / VERIFIED (2026-11-25, §7.2.2) — `GET /branches/main/protection` returns 200 with 16 contexts including `GOV-DOC-001 structural checks`, and `PUT /pulls/1038/merge` was refused with 405 on a failing required check.
- F-02 overall: COMPLETE / VERIFIED on both requirements. The job is blocking; one of its steps (`check_policy_inheritance`) remains advisory, and `required_pull_request_reviews` is absent, so this does not claim review enforcement. A successful workflow run alone is still not platform enforcement; the evidence is the protection readback plus the merge rejection.

**F-08 — stale baseline and manifest**

- Status: `CLOSED` (2026-11-20), on a recorded basis. This closure is not retroactive.
- Status at the moment of the external correction: `corrected, not independently confirmed`. Comment `7017127588` withdraws the earlier `CLOSED` claim; it does not assert re-confirmation. The `CLOSED` state above is established only by the PR #285 review chain recorded on that PR, and reading the withdrawal as a re-confirmation would be an error.
- Correction trail: §2.2 and §3.1–§3.3 were rewritten in v2.2 to separate current main, current PR head/tree, the historical submission commit, and the R6 pre-v2.2 OBJ-07 snapshot; v2.3 added the v2.3 comparison and the normative-boundary correction; v2.5 adds the record-boundary rule (§0), a post-merge snapshot (§2.2) and a post-merge manifest read-back (§3.2).
- Root cause, stated so it is not repeated: the finding was structural, not clerical. A report that treats HEAD values as current assertions is stale the moment it is merged. §0 now separates bound snapshots from live assertions, which is what makes the class of defect closable rather than perpetually re-openable.
- Sequencing correction: this report previously required `Do not mark CLOSED before exact-Head re-review`, and the PR #271 acceptance record nevertheless listed F-08 as `CLOSED` before any review had examined it — R7 and R8 reviewed other findings. The closure above is supported by the v2.5 revision and its review; it does not validate that earlier line.
- Objective evidence — re-derivable by any reader with read access, not author narrative. Requests, expected values and the assertion each one supports are mapped one-to-one below; `GET`, token and failure handling follow the reproduction prerequisites in §0.

| # | Request (method + path) | Expected field = value | Assertion supported |
|---|---|---|---|
| E1 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/271` | `merged` = `true`; `merged_at` = `2026-11-19T17:16:13Z` | §2.2 states PR #271 is merged, at that time |
| E2 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/271` | `merge_commit_sha` = `f86fddc0fa0291ea8a5e080e741f083ce179a0a2` | the merge commit identity asserted in §2.2 |
| E3 | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/271` | `head.sha` = `1eefa22e7fecfcd882aff795796ae178d1f7c4a5`; `base.sha` = `c5a995d9a2808112b007a9108e085048cbed5cc9` | the reviewed head and the recorded base in §2.2 |
| E4 | `GET /repos/oahcom/AiMemoryBrainArchitecture/commits/f86fddc0fa0291ea8a5e080e741f083ce179a0a2` | `parents[0].sha` = `a22024112fce3851428343ca3e655712057e6dce`; `parents[1].sha` = `1eefa22e7fecfcd882aff795796ae178d1f7c4a5` | main before the merge, and the merged parent |
| E5 | E3 and E4 compared | E4 `parents[1].sha` = E3 `head.sha` | the merged head is the reviewed head, not a re-created one |
| E6 | `GET /repos/oahcom/AiMemoryBrainArchitecture/contents/<path>?ref=main`, once per row of §3.2 | `sha` = the `Blob SHA` in that row | the post-merge manifest recorded in §3.2 |

If any request returns non-200, the affected row is `INCONCLUSIVE` and F-08 may not be closed on it.
- Judgement, separated from the objective part: that the corrected prose in §2.2 and §3.2 no longer asserts stale values is a review judgement, recorded as such and attributed to the R1 review of PR #285, not presented as a measurement.
- External correction record: because the PR #271 acceptance comment is an independent historical decision record, it is corrected by comment `7017127588` on PR #271 itself, not by this report alone.

**F-09 — stale CI integration status**

- Status: `CLOSED` (2026-11-20), by the PR #285 review chain. At the moment of the external correction the status was `corrected, not independently confirmed`. §6.4, §7.1, §7.2, §9 and §10 distinguish verified workflow integration from unverified platform required-check enforcement, and §7.1 records three runs in both language columns.
- Boundary retained: closing F-09 does not close F-02. F-02 Requirement 2 stays `NOT_VERIFIED` because the platform setting is unavailable, not because the text is stale.
- Sequencing correction: same as F-08 — the earlier acceptance line cited closure ahead of the re-review this report required.
- **Re-open event (2026-11-20) — the first application of the §0 trigger to this report after closure.** §11 asserted that "CI workflow integration and required-check enforcement have not yet been established". That assertion is false for integration: §7.1 records three successful runs and §10 marks Requirement 1 `COMPLETE / VERIFIED`. The finding was therefore set back to `OPEN` in this revision, the failed assertion is named here, and `CLOSED` is re-established only by this revision and its review. This is what the §0 trigger is for; a mechanism that survived its first real contradiction by reinterpreting it would have been self-exemption after all.
- Objective evidence (re-derivable): §7.1 lists three workflow runs with their conclusions in both language columns; §6.4, §7.2 and §10 each state separately that workflow integration is verified and required-check enforcement is `NOT_VERIFIED`. The check is textual and located: read those four sections and confirm no line asserts platform enforcement.
- Judgement: that the four sections are now internally consistent and mutually non-contradictory is a review judgement, attributed to the R1 review of PR #285.

### P2

**F-06 — object-level reconciliation COMPLETE (2026-11-20); migration debt unchanged**

Object-level reconciliation is recorded in `00-governance/reports/f06-object-reconciliation.md`, executed against baseline `f86fddc0`. **This section's previous conclusion is retracted:** the statement that fourteen PRs remained unassigned was incorrect when written — all fourteen were already in the §8.4 group tables. Result: 313/313 commit anchors recomputed and matched (313 unique `sha`; 25 rows share 7 message digests, so `sha` remains the identity key and `msg_sha256` does not); 38/39 issue anchors matched, with #266 recorded as an explained anchor drift after a post-inventory body edit; PR grouping reconciled — all fourteen PR numbers previously listed here as unassigned are in fact present in the §8.4 group tables, and the twelve genuinely unassigned PRs (`#48`, `#271`–`#281`) carry **PROPOSED** assignments with per-item evidence, pending accountable-owner confirmation; formal coverage remains 230/242 until then.

Issue #254 remains within the 39-record set, on HOLD with its explicit exit conditions. Assignment is not migration: every group keeps `MIGRATION_DEBT` and `Accountable_Owner: NOT_ASSIGNED`. Closing F-06 does not establish historical bilingual migration completion.

**F-07 — authoritative baseline correction**

Use D1 authoritative baseline blob `66517d39` and retain PR comment `7006445553` as the correction traceability record.

**F-10 — completed PR manifest declaration**

The PR #271 body declaration `BILINGUAL-MANIFEST: COMPLETE` has already been updated. Record it as completed execution evidence; remove it from the outstanding CI blocker list. This declaration does not imply semantic review PASS, Owner approval, policy adoption, or merge authorization.

### CI blocker

The only remaining F-02 blocker is platform required-check configuration/enforcement. The branch-protection and ruleset endpoints returned HTTP 403 because the repository is private under a plan that does not support these settings. Retain `NOT_VERIFIED`; do not claim the required check is enforced. The workflow integration and successful runs are recorded in §7.1.

### Other required actions

1. Preserve the D2 incremental appendix and its reconciliation work as outstanding; **this changeset does not modify D2**.
2. `DONE (2026-11-20)` — the object-level reconciliation is recorded in `00-governance/reports/f06-object-reconciliation.md`; no migration group was inferred.
3. `DONE` — the D7 exact commit and its read-back evidence were independently reviewed at every revision (R6 → R8 on PR #271; R1 → R3 on #282; R1 → R3 on #284).
4. `SUPERSEDED` — the pre-merge `diverged` comparison is a bound snapshot, not a live check. After merge, `main` contains the reviewed head (merge `f86fddc0`), so Exact-Head integration is established by containment rather than by re-running a divergence comparison.
5. `DONE (2026-11-20)` — F-06 reconciliation complete; Issue #254 stays on HOLD with its exit conditions untouched.
6. `OUT-OF-SCOPE(dev-baseline)` — explicit authorized governance approval requires an accountable human authority. A single shared identity cannot supply it, so it is recorded as unreachable rather than simulated. No automatic approval or adoption is permitted or implied.

Platform residual tracking: the required-check blocker and the branch-protection 403 are tracked in Issue #283 with re-verification triggers, so they do not leave this report in a permanent open state.

---

### 后续行动与阻塞（中文）

### P1

**F-02——平台 required-check 强制执行**

- 要求 1（校验器已接入并由 CI 调用）：COMPLETE / VERIFIED，ADVISORY（非阻断）。
- 强制范围（v2.4，R7 发现）：声明校验仅输出提示。若设为阻断，即以工具施加尚未采纳的 v1.2 继承要求；强制执行推迟至规范采纳之后。
- 要求 2（required check 已配置并强制执行）：COMPLETE / VERIFIED（2026-11-25，§7.2.2）——`GET /branches/main/protection` 返回 200，16 个 contexts 含 `GOV-DOC-001 structural checks`；`PUT /pulls/1038/merge` 因失败的 required check 被以 405 拒绝。
- F-02 总体：两项要求均 COMPLETE / VERIFIED。job 为阻断；其内部的 `check_policy_inheritance` 步骤仍为非阻断，且 `required_pull_request_reviews` 缺失，故不构成对审查强制的声称。单次 workflow 成功运行仍不等于平台强制；证据是 protection 读回与合并拒绝。

**F-08——基线与 manifest 陈旧**

- 状态：`CLOSED`（2026-11-20），基于已登记依据。本次关闭不具溯及力。
- 更正轨迹：v2.2 重写§2.2 与 §3.1–§3.3，区分当前 main、当前 PR head/tree、历史首次提交与 R6 的 v2.2 前 OBJ-07 快照；v2.3 新增 v2.3 对比与规范边界更正；v2.5 新增记录边界规则（§0）、合并后快照（§2.2）与合并后 manifest 读回（§3.2）。
- 根因（写明以免重犯）：该 finding 是结构性的，不是文字疏漏。把 HEAD 值当作当前断言的报告，在合并那一刻就陈旧。§0 现已将绑定快照与活动断言分开，这才使这类缺陷可以真正关闭，而不是永远重开。
- 时序更正：本报告此前要求「Exact-Head 复审通过前不得标记 CLOSED」，而 PR #271 验收记录却在任何审查看过该项之前就列为 `CLOSED`——R7 与 R8 审的是其他 finding。上述关闭由 v2.5 修订及其审查支撑，不构成对那一行旧验收的追认。
- 客观证据（任何有读权限的人可重新推导，非作者叙述）：请求、期望值与其支持的断言已上表 E1–E6 逐项一一映射；方法、令牌与失败处理按 §0 的复现前提执行。任一请求返回非 200，对应行即为 `INCONCLUSIVE`，不得据此关闭 F-08。
- 外部更正时点的状态：`corrected, not independently confirmed`。评论 `7017127588` 撤回先前 `CLOSED` 表述，但并不声称重新确认；上方 `CLOSED` 仅由记录于 PR #285 的审查链成立，将「撤回」读作「重新确认」属误读。
- 判断与客观部分分离：「更正后的 §2.2 与 §3.2 不再陈述旧值」属审查判断，已如实标注并归属于 PR #285 的 R1 审查，不作为实测事实。
- 外部更正记录：PR #271 验收评论属独立历史决策记录，因此由 PR #271 上的评论 `7017127588` 修正，而非仅由本报告覆盖。

**F-09——CI 接入状态陈旧**

- 状态：`CLOSED`（2026-11-20），由 PR #285 的审查链成立。外部更正时点的状态为 `corrected, not independently confirmed`。§6.4、§7.1、§7.2、§9 与 §10 已区分已验证的 workflow 接入与未验证的平台 required-check 强制状态，且 §7.1 中英两列均列出三次运行。
- 保留边界：关闭 F-09 不等于关闭 F-02。F-02 要求 2 维持 `NOT_VERIFIED`，原因是平台设置不可用，而不是文字陈旧。
- 时序更正：与 F-08 同——此前验收行在本报告要求的复审之前就引用了关闭。
- **重新开启事件（2026-11-20）——§0 触发器在本报告关闭后的首次实际应用**：§11 声称「CI workflow 接入及 required check 强制生效尚未得到证实」。就接入而言该声称不成立：§7.1 记录三次成功运行，§10 将要求 1 记为 `COMPLETE / VERIFIED`。因此在本修订中将该 finding 置回 `OPEN`，在此点名失败的断言，`CLOSED` 仅由本修订及其审查重新成立。这正是 §0 触发器的用途；若一个机制在首次真实矛盾面前靠重新诠释而存活，那它就仍然是自我豁免。
- 客观证据（可重新推导）：§7.1 在中英两列均列出三次 workflow 运行及结论；§6.4、§7.2 与 §10 各自分别说明「workflow 接入已验证」与「required-check 强制为 `NOT_VERIFIED`」。检验方式为文本定位：阅读这四节并确认无任何行声称平台已强制执行。
- 判断：「四节内部一致且不矛盾」属审查判断，归属于 PR #285 的 R1 审查。

### P2

**F-06——对象级对账已完成（2026-11-20）；迁移欠账不变**

对象级对账记录于 `00-governance/reports/f06-object-reconciliation.md`，基线 `f86fddc0`。**本段原结论撤回：**此前「14 个 PR 未归组」的说法在写下时即为错误——该 14 个当时已在 §8.4 分组表中。结果：313/313 条 Commit 锚点复算命中（`sha` 313 条唯一；25 行分属 7 组同文消息，故身份键仍为 `sha`，`msg_sha256` 不可作身份键）；39 条 Issue 锚点命中 38 条，#266 因清点后正文被编辑而漂移，已连同编辑时间一并登记；PR 归组完成对账——本处原列的 14 个「未归组」PR 实际均已在 §8.4 分组表中，真正未归组的 12 个（`#48`、`#271`–`#281`）已按集成单元证据给出**PROPOSED 归组提案**，逐项附证据，待责任方确认；确认前正式覆盖率仍为 230/242。

Issue #254 继续包含在 39 条集合内，保持 HOLD 并保留退出条件。归组不等于迁移：各分组继续维持 `MIGRATION_DEBT` 与 `Accountable_Owner: NOT_ASSIGNED`。关闭 F-06 不代表历史双语迁移完成。

**F-07——权威基线更正**

后续使用 D1 权威基线 blob `66517d39`，并保留 PR 评论 `7006445553` 作为更正追踪记录。

**F-10——已完成的 PR manifest 声明**

PR #271 正文中的 `BILINGUAL-MANIFEST: COMPLETE` 声明已经更新。应将其记录为已完成执行证据，并从未解决 CI 阻塞项中移除。该声明不代表语义审查 PASS、Owner 批准、规范采纳或合并授权。

### CI 阻塞

F-02 唯一剩余阻塞是平台 required-check 配置/强制执行。由于当前私有仓库所处计划不支持相关设置，branch-protection 和 ruleset API 返回 HTTP 403。继续标记为 `NOT_VERIFIED`，不得声称 required check 已强制执行。Workflow 接入和成功运行已记录于 §7.1。

### 其他必需行动

1. 保留 D2 增量附录及其对账工作为未完成事项；**本变更集不修改 D2**。
2. `DONE（2026-11-20）`——对象级对账记录于 `00-governance/reports/f06-object-reconciliation.md`；未推断任何迁移组。
3. `DONE`——D7 各修订的精确提交与读回证据均已独立审查（#271 上 R6 → R8；#282 上 R1 → R3；#284 上 R1 → R3）。
4. `SUPERSEDED`——合并前的 `diverged` 比较是绑定快照，不是实时校验。合并后 `main` 已包含被审 head（merge `f86fddc0`），故 Exact-Head 集成由包含关系成立，无需重跑分叉比较。
5. `DONE（2026-11-20）`——F-06 对账完成；Issue #254 保持 HOLD，其退出条件未被改动。
6. `OUT-OF-SCOPE(dev-baseline)`——明确且有权的治理批准需要可归属的人类权威。单一共享身份无法提供，因此如实记为不可达，而不伪造。不得以任何方式推定自动批准或采纳。

平台残留跟踪：required-check 阻塞与 branch-protection 403 已在 Issue #283 中带复验触发器跟踪，不使本报告长期处于未决状态。

### Re-open check record / 重新开启核对记录

The §0 re-open trigger is only operative if it is actually applied to each revision. This record applies the three trigger conditions to this revision and states the result, including the one that fired.

§0 的重新开启触发器只有在逐次修订中真被执行时才有效。本记录将三个触发条件应用于本修订并说明结果，包括实际触发的那一项。

| Trigger condition | Check performed | Result | Evidence |
|---|---|---|---|
| A snapshot marked superseded is cited as current | searched §2.2 and §10 for the pre-merge `diverged` counts and for `OPEN; merged: false` | CLEAR — both retain an explicit bound/superseded label and neither is used as a current assertion | §2.2 annotation bullet; §10 F-06/F-08 rows |
| A corrections section has drifted from the objects it describes | read comment `7017127588` against §9 F-08 and F-09 | CLEAR — the comment withdraws the earlier `CLOSED` claim and §9 records the same withdrawal, with the dissolved state named `corrected, not independently confirmed` | comment `7017127588`; §9 |
| A new line repeats the same defect class | reviewed this revision's diff for unlabelled HEAD/PR-state assertions and for bilingual-parity gaps | **FIRED, fixed in this revision** — §8's Chinese F-02 row omitted the advisory-declaration and workflow-integration sentences present in the English row, which is the F-09 defect class | §8 F-02 rows |

A trigger that never fires is not evidence of health; it is more often evidence that the check was not performed. This revision's third row fired and was repaired before merge, and is recorded here rather than only in the diff.

**Cross-check run against merged `main` `07450a44` (v2.8, first full c1–c9 run).** The §0 rule is that the check runs on every revision that touches a status sentence; this run applies it to the merged report itself rather than to a pending diff.

| Check | Result | Note |
|---|---|---|
| c1 | CLEAR | no sentence asserts an unestablished capability; the only such sentence was corrected in v2.6 |
| c2 | **UNSATISFIABLE AS WRITTEN — wording fixed here** | it required §10 to carry every finding, but §10 is a stage ledger and legitimately carries six of ten. The check was rewritten to the single-index rule above |
| c3 | CLEAR | §11 distinguishes verified integration from unverified enforcement, consistent with §7.1/§7.2/§9/§10 |
| c4 | **FIRED — AC-01 corrected** | AC-01 still said "F-03/F-04 require further closure" while the registry marks both `CLOSED (method-bound)` |
| c5 | CLEAR | the only registry/§6.3 divergences are the four findings absent from §6.3 by construction |
| c6 | CLEAR | all ten bases re-read; none has been superseded |
| c7 | CLEAR | every cited §, comment id (`7006445553`, `7017127588`) and path exists and carries the stated value |
| c8 | CLEAR | no stated reopen condition has triggered; every `CLOSED` row still meets its closure condition |
| c9 | CLEAR | eight `CLOSED` rows pass T1; no row rests on a remediation artifact alone |

Two of nine checks fired, and one of them was the check itself being wrong rather than the report being wrong. That distinction is worth keeping: a check that cannot pass is a defect in the check, and fixing it by weakening the report would have been the wrong repair.

本轮后补：c2 原文要求 §10 携带每一项 finding，但 §10 是阶段台账、合理地只携带十项中的六项，该核对因此不可满足，已改为「单一索引」规则；c4 实际触发：AC-01 仍引用 F-03/F-04 作为未关闭阻塞，而登记表已将二者记为 `CLOSED (method-bound)`，已在本次修正。九项中两项触发，其中一项是「核对本身错了」而非「报告错了」——这个区分值得保留：一项永远无法通过的核对是核对自身的缺陷，靠削弱报告去让它通过是错误的修复。

**v2.6 — the first application after closure.** The same three conditions were applied again to the merged report as it stood at `main` `c0ea54ed`, before this revision. The third condition fired a second time, and this time against already-merged text rather than against a pending diff: §11 stated that "CI workflow integration and required-check enforcement have not yet been established", contradicting §7.1 and §10. It also turned out that every revision note from v2.1 onward contained the same class of line (v2.2's note still says F-06 "remains OPEN"), which is why those notes are now explicitly labelled as bound snapshots rather than maintained state. F-09 was set back to `OPEN` for this revision and re-closed only on its review.

**v2.6 — 关闭后的首次应用。** 同三个条件在本修订之前对「已合并的报告」（`main` `c0ea54ed`）再次应用。第三条件**第二次触发**，且这次面对的是已合并文本而非待合并 diff：§11 声称「CI workflow 接入及 required check 强制生效尚未得到证实」，与 §7.1 与 §10 相矛盾。同时发现：自 v2.1 起的每份修订说明都存在同类句子（v2.2 说明仍写「F-06 remains OPEN」），因此现已将这些说明明确标为绑定快照、非受维护状态。F-09 在本修订中置回 `OPEN`，仅在其审查通过后重新关闭。

触发器从不触发并不证明健康，更常说明核对未被执行。本修订第三行实际触发并在合并前修复，已在此登记，而不仅体现于 diff。

## 10. Governance stage ledger / 治理阶段登记

The original 15-row governance stage ledger is retained. Only affected evidence/status entries are updated; unrelated historical rows remain present.

原 15 行治理阶段登记表予以保留。仅更新受影响的证据/状态项；无关历史登记继续保留。

| Stage / 阶段 | Status / 状态 | Evidence and limitation / 证据与限制 |
|---|---|---|
| v1.1 Read / v1.1 读取 | READ | Historical GOV-DOC-001 v1.1 baseline; current main D1 remains v1.1 NORMATIVE. / 历史 GOV-DOC-001 v1.1 基线；当前 main D1 仍为 v1.1 NORMATIVE。 |
| v1.2 Drafted / v1.2 起草 | DRAFTED | D1–D7 proposal; v1.2 remains DRAFT. / D1–D7 提案；v1.2 仍为 DRAFT。 |
| Seven files submitted / 七文件提交 | SUBMITTED | Historical initial submission commit `a77219fa2834af0c4535e6692029adaec2e62638`; current PR #271 head at R6 baseline `47369925ace93821eab82e4cec8418f8d7505d64`. / 历史首次提交为上述 commit；R6 基线的 PR #271 head 为上述 SHA。 |
| Seven files read back / 七文件读回 | VERIFIED | R6 OBJ-07 pre-v2.2 manifest read-back: 7/7; D7 manifest entry is the v2.1 blob snapshot. / R6 对 v2.2 前 OBJ-07 manifest 读回 7/7；D7 条目为 v2.1 blob 快照。 |
| Five Issues updated / 五个 Issue 更新 | SUBMITTED | Issues #262–#266; all remain OPEN and Requirement Status RECORDED. / Issues #262–#266；均保持 OPEN，Requirement Status 为 RECORDED。 |
| Five Issues read back / 五个 Issue 读回 | VERIFIED | Five GitHub API read-backs; no Issue closure or label change inferred. / 五个 GitHub API 读回；不推定 Issue 已关闭或标签已变更。 |
| Historical inventory / 历史清单 | PARTIAL | 39 Issues and 313 Commits registered/reconciled; 242/242 PR objects at the `f86fddc0` reconciliation baseline are grouped after A Integration confirmed the 12 later mappings in register §8.4.2; F-06 object-level reconciliation CLOSED. Historical bilingual migration debt remains unchanged; #254 remains HOLD. / 已登记并对账 39 条 Issue、313 条 Commit；A Integration 确认登记册 §8.4.2 中后续 12 个归组后，对账基线 `f86fddc0` 的 242/242 个 PR 对象均已归组；F-06 对象级对账已 CLOSED。历史双语迁移欠账不变；#254 仍为 HOLD。 |
| Independent review / 独立复审 | REVIEW CHAIN RECORDED | R6 `NEEDS-REVISION` on D7 v2.1 (`6aff0b47-3988-83ec-b666-976e39dfe840`) → R7 `NEEDS-REVISION` on head `04d35f90` → R8 `PASS` on head `1eefa22e`; v2.5 closes the F-08/F-09 re-review that the earlier chain did not cover. Identity axis remains P-independent-unreachable. / R6 对 D7 v2.1 给 NEEDS-REVISION → R7 对 head `04d35f90` 给 NEEDS-REVISION → R8 对 head `1eefa22e` 给 PASS；v2.5 补齐前序链未覆盖的 F-08/F-09 复审。身份轴仍为 P-独立不可达。 |
| F-02 | PARTIAL | Requirement 1 CI integration COMPLETE/VERIFIED; Requirement 2 required-check enforcement NOT_VERIFIED due GitHub plan-limit HTTP 403. / 要求 1 CI 接入 COMPLETE/VERIFIED；要求 2 因 GitHub 计划限制 HTTP 403 而 NOT_VERIFIED。 |
| F-06 | CLOSED (2026-11-20) | Object-level reconciliation recorded in `00-governance/reports/f06-object-reconciliation.md`: 313/313 commit anchors matched, 38/39 issue anchors with #266 drift registered; the earlier "14 unassigned PRs" conclusion is retracted. #254 remains HOLD; migration debt unchanged. / 对象级对账已记录于上述报告：313/313 Commit 锚点命中，39 条 Issue 锚点命中 38 条并登记 #266 漂移；此前「14 个未归组 PR」结论已撤回。#254 保持 HOLD；迁移欠账不变。 |
| F-07 | CORRECTION RECORDED | PR comment `7006445553`; authoritative D1 baseline blob `66517d39`. / PR 评论 `7006445553`；D1 权威基线 blob `66517d39`。 |
| F-08 | CLOSED (2026-11-20) | Record-boundary rule §0 + post-merge snapshot §2.2 + post-merge manifest §3.2; closure basis and the acceptance-sequencing correction are recorded in §9. / §0 记录边界 + §2.2 合并后快照 + §3.2 合并后 manifest；关闭依据与验收时序更正记于 §9。 |
| F-09 | CLOSED (2026-11-20) | §6.4/§7.1/§7.2/§9/§10 separate verified workflow integration from unverified required-check enforcement; closing F-09 does not close F-02. / §6.4/§7.1/§7.2/§9/§10 已区分已验证 workflow 接入与未验证 required-check 强制；关闭 F-09 不等于关闭 F-02。 |
| F-10 | CLOSED | PR #271 body declaration `BILINGUAL-MANIFEST: COMPLETE` recorded as execution evidence; it implies no review PASS, approval, adoption or merge authorisation. / PR #271 正文声明已作为执行证据登记；不构成审查 PASS、批准、采纳或合并授权。 |
| Structural CI / 结构 CI | MIXED HISTORICAL RECORD | Failure run `44477435608` retained as historical; runs `44542512889`, `44546301573`, and post-v2.2 run `44559550224` SUCCESS. Required-check enforcement remains NOT_VERIFIED. / 失败运行 `44477435608` 保留为历史记录；运行 `44542512889`、`44546301573` 及 v2.2 后运行 `44559550224` 均 SUCCESS。required-check 强制执行仍为 NOT_VERIFIED。 |
| Owner approval / Owner 批准 | NOT_RECORDED | No explicit Owner approval evidence. / 无明确 Owner 批准证据。 |
| Policy adoption / 规范采纳 | NOT_ADOPTED | GOV-DOC-001 v1.2 remains DRAFT; no adoption evidence. / GOV-DOC-001 v1.2 仍为 DRAFT；无采纳证据。 |
| Effective status / 生效状态 | NOT_EFFECTIVE | v1.1 remains NORMATIVE; v1.2 is not effective. / v1.1 仍为 NORMATIVE；v1.2 尚未生效。 |

`Approval: NOT_RECORDED`  
`Adoption: NOT_ADOPTED`  
`MIGRATION_DEBT != EXEMPTION`

## 11. Honest declaration / 诚实声明

### EN


This report records delivery facts from 2026-11-19 and the finding statuses maintained through 2026-11-20.

The independent validator, declaration, and tests have been committed. The corrected local test suite reports 6/6 PASS. CI **workflow integration** is verified (§7.1 records the runs; §10 marks Requirement 1 COMPLETE / VERIFIED). **Required-check enforcement** is not verified, because the platform setting is unavailable on this repository — not because the integration is missing. F-02 therefore remains PARTIAL on Requirement 2 alone.

Correction of a contradiction: earlier text in this section stated that "CI workflow integration and required-check enforcement have not yet been established". That conflated the two requirements and contradicted §7.1 and §10. It is corrected here rather than left to be read as agreement that integration is unverified.

The historical language inventories have been finalized with 39 Issue records and 313 Commit records. Issue #254 is included in the 39-record Issue inventory, classified as `ZH_ORIGINAL_WITH_EN_TERMS`, and remains on HOLD. Commit language classification is based on the substantive content of the complete commit message. Inventory registration does not establish bilingual migration completion.

The F-07 correction record is registered in PR comment `7006445553`. The authoritative D1 baseline blob is `66517d39`.

Normative status remains unchanged: v1.1 is NORMATIVE and v1.2 is DRAFT. Migration debt is not an exemption. This report does not imply Owner approval, normative adoption, PR merge authorization, or completion of historical content migration.

Any item for which complete supporting evidence has not been established must remain explicitly identified as incomplete or unverified. This report must not be interpreted as a claim that all audits, CI gates, migration work, or governance approvals are complete.

### 中文


本报告记录 2026-11-19 的交付事实，以及维护至 2026-11-20 的 finding 状态。

独立校验器、配套声明及测试已提交入库。修复后的本地测试套件结果为 6/6 PASS。CI **workflow 接入已验证**（§7.1 列出运行记录，§10 将要求 1 记为 COMPLETE / VERIFIED）；**required check 强制执行未验证**，原因是本仓库不得使用该平台设置，而不是接入缺失。因此 F-02 仅因要求 2 而维持 PARTIAL。

矛盾更正：本节此前写有「CI workflow 接入及 required check 强制生效尚未得到证实」，该表述将两项要求混为一谈，与 §7.1 与 §10 相矛盾。此处予以更正，而非任由其被读作「接入尚未验证」的认可表述。

历史语言状态清单已定稿，包含 39 条 Issue 记录和 313 条 Commit 记录。Issue #254 包含在 39 条 Issue 清单内，分类为 `ZH_ORIGINAL_WITH_EN_TERMS`，当前保持 HOLD。Commit 语言分类依据完整提交消息的实质内容判定。清单登记完成不代表双语迁移完成。

F-07 更正记录已登记于 PR 评论 `7006445553`。D1 权威基线 blob 为 `66517d39`。

规范效力状态保持不变：v1.1 为 NORMATIVE，v1.2 为 DRAFT。迁移债务不构成豁免。本报告不表示 Owner 已批准、规范已被采纳、PR 已获得合并授权，或历史内容迁移已经完成。

凡尚未取得完整支持证据的事项，必须明确标记为未完成或未验证。本报告不得被解释为所有审计、CI 门禁、迁移工作或治理批准均已完成的声明。

---

**EN**

Every revision note from v2.1 onward is a bound snapshot of the revision that wrote it: it binds the original record at its own revision timepoint. It records what that revision changed and the state at that time, and it is not maintained. This labelling does not assert that the historical state was permanently correct, and it does not make a historical error harmless — it only removes the ambiguity of reading an old note as a current statement. Where a note says a finding "remains OPEN", that describes the state when the note was written. Current finding states live in §9 and §10 only.

自 v2.1 起的每份修订说明均为其所属修订的绑定快照：它绑定的是「原始记录在其自身修订时点」的状态，记录该修订做了什么以及当时状态，不受维护。该标注并不声称历史状态永久正确，也不使历史错误本身变得无害——它只消除「把旧说明当作当前陈述」的歧义。若某份说明写「某 finding 仍为 OPEN」，那指的是写下该说明时的状态。当前 finding 状态仅以 §9 与 §10 为准。

## D7 v2.1 Revision Note

This revision records the verified delivery facts and status boundaries as of 2026-11-19.

- **F-02:** The independent validator, declaration, and tests were committed as `d568325b`. Test corrections were committed as `e6ff2746`, with test-file blob `4ca1f8a2`; the corrected local test result is 6/6 PASS. CI workflow integration and required-check enforcement evidence remain outstanding. F-02 remains PARTIAL.
- **F-06:** The Issue inventory is finalized at 39 records: 28 EN_ONLY, 10 EN_ZH_MIXED, and 1 ZH_ORIGINAL_WITH_EN_TERMS (#254, HOLD). The Commit inventory is finalized at 313 records: 312 EN_ONLY and 1 MIXED (C168). Issue records use body_sha256 anchors; Commit records use sha and msg_sha256 anchors. Commit language classification is based on the substantive content of the complete commit message. Registration does not establish migration completion.
- **F-07:** The correction record is registered in PR comment `7006445553`. The authoritative D1 baseline blob is `66517d39`.
- **Normative and authorization boundaries:** v1.1 remains NORMATIVE; v1.2 remains DRAFT. MIGRATION_DEBT != EXEMPTION. No Owner approval, normative adoption, PR merge authorization, or historical migration completion is inferred.

This revision updates verified facts and delivery status only. It does not expand existing authorization, alter normative status, or waive any outstanding acceptance requirement.

**中文**

## D7 v2.1 修订说明

本次修订记录截至 2026-11-19 已核实的交付事实及状态边界。

- **F-02：**独立校验器、配套声明及测试已提交，提交为 `d568325b`。测试修复提交为 `e6ff2746`，测试文件 blob 为 `4ca1f8a2`；修复后的本地测试结果为 6/6 PASS。CI workflow 接入及 required check 强制生效证据仍未完成。F-02 维持 PARTIAL。
- **F-06：**Issue 清单已定稿，共 39 条：28 条 EN_ONLY、10 条 EN_ZH_MIXED、1 条 ZH_ORIGINAL_WITH_EN_TERMS（#254，HOLD）。Commit 清单已定稿，共 313 条：312 条 EN_ONLY、1 条 MIXED（C168）。Issue 记录使用 body_sha256 锚点；Commit 记录使用 sha 和 msg_sha256 锚点。Commit 语言分类依据完整提交消息的实质内容判定。登记完成不代表迁移完成。
- **F-07：**更正记录已登记于 PR 评论 `7006445553`。D1 权威基线 blob 为 `66517d39`。
- **规范效力与授权边界：**v1.1 继续为 NORMATIVE；v1.2 继续为 DRAFT。MIGRATION_DEBT != EXEMPTION。不得推定 Owner 已批准、规范已被采纳、PR 已获合并授权或历史迁移已经完成。

本次修订仅更新已核实事实及交付状态，不扩大既有授权范围，不改变规范效力，也不豁免任何尚未满足的验收要求。


**EN**

## D7 v2.2 Revision Note

This revision responds to the R6 independent review (session `6aff0b47-3988-83ec-b666-976e39dfe840`, final disposition `NEEDS-REVISION`).

- **F-08:** Corrects the stale main/PR baseline and separates the historical initial submission from the R6 current-head evidence. The OBJ-07 manifest is explicitly identified as the pre-v2.2 snapshot.
- **F-09 / F-02:** Records validator CI integration as COMPLETE / VERIFIED, records required-check configuration/enforcement as NOT_VERIFIED due the GitHub plan-limit HTTP 403, and retains F-02 overall as PARTIAL.
- **F-10:** Records the already completed `BILINGUAL-MANIFEST: COMPLETE` PR-body declaration as historical execution evidence and removes it from outstanding blockers.
- **F-06:** Remains OPEN; the 14 unassigned PRs and object-level reconciliation requirements remain outstanding.
- Post-v2.2 validation at head `bbfe046b9307c9bfffd7606c4a7caadcb1de32f8` read back D7 blob `36c50869fe2c42d5e1f12616012c84e0a1cc5d28`; workflow run `44559550224` passed. The main comparison remained `diverged` (ahead 10 / behind 42), so Exact-Head integration verification has not passed.
- D2 is not modified. v1.1 remains NORMATIVE; v1.2 remains DRAFT. `MIGRATION_DEBT != EXEMPTION`.
- `Approval: NOT_RECORDED`; `Adoption: NOT_ADOPTED`. This report does not authorize PR merge or imply Owner approval, policy adoption, or historical migration completion.
- This v2.2 correction is pending a fresh independent review; it is not self-approved.

**中文**

## D7 v2.2 修订说明

本次修订响应 R6 独立复审（会话 `6aff0b47-3988-83ec-b666-976e39dfe840`，最终结论 `NEEDS-REVISION`）。

- **F-08：**更正陈旧的 main/PR 基线，并区分历史首次提交与 R6 当前 head 证据。明确将 OBJ-07 manifest 标记为 v2.2 之前的快照。
- **F-09 / F-02：**将校验器 CI 接入登记为 COMPLETE / VERIFIED；将 required-check 配置/强制执行登记为因 GitHub 计划限制 HTTP 403 而 NOT_VERIFIED；F-02 总体继续保持 PARTIAL。
- **F-10：**将已经完成的 `BILINGUAL-MANIFEST: COMPLETE` PR 正文声明记录为历史执行证据，并从未解决阻塞项中移除。
- **F-06：**继续保持 OPEN；14 个未归组 PR 及对象级对账要求仍未完成。
- v2.2 之后的 current-main 比较结果为 `diverged`（ahead 10 / behind 42）。本次提交后仍须重新进行 Exact-Head 复核。
- 不修改 D2。v1.1 继续为 NORMATIVE；v1.2 继续为 DRAFT。 `MIGRATION_DEBT != EXEMPTION`。
- `Approval: NOT_RECORDED`；`Adoption: NOT_ADOPTED`。本报告不授权 PR 合并，也不表示 Owner 已批准、规范已采纳或历史迁移已完成。
- 本 v2.2 更正等待新一轮独立复审，不得自我批准。

**EN**

## D7 v2.3 Revision Note

This revision responds to a coordinator-side normative-boundary finding raised while preparing the fresh independent review required by R6. It is not an independent acceptance and does not alter any approval state.

- **Normative boundary (P1, new):** the v1.2 text previously replaced the NORMATIVE v1.1 document at `00-governance/bilingual-documentation-policy.md`. A draft occupying the normative path removes the only normative text from its canonical location without approval, and contradicts the PR statement that v1.2 does not become normative by being merged. Remedy: the normative path is restored to the v1.1 text (blob `0e170479e1a71e8f4c124c6f1dc170241652f42b`, byte-identical to current main `a22024112fce3851428343ca3e655712057e6dce`); the v1.2 proposal is relocated to `00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md` (blob `d91bd92b79177decc7baa038fdd24b3f8323b995`) with an explicit non-normative banner.
- **v2.2 defect corrections:** two literal backslash-n escape sequences that broke a §2.2 bullet and a §7.1 table row are replaced with real line breaks; the §7.1 Chinese table is aligned to the English table (three runs); §3.3 and the v2.2 note are corrected from `ahead 8` to `ahead 10` for the post-v2.2 snapshot, matching the English text; a stray trailing marker at end of file is removed.
- **Manifest:** §3.2 retains the R6 OBJ-07 snapshot as history and adds the v2.3 current manifest with D1 relocated and D1-N recording the restored normative blob. D2-D6 are byte-identical to the R6 read-back.
- **Gate wiring unchanged:** `scripts/check_bilingual_docs.py` still validates the `POLICY-INHERITANCE-DECLARATION` block for `00-governance/` changes, as accepted by R6. Because the inheritance requirement originates from the unadopted v1.2 draft, this wiring is recorded as tooling-level declaration checking, not as policy adoption; adoption remains `NOT_ADOPTED`.
- **Status boundaries unchanged:** GOV-DOC-001 v1.1 NORMATIVE; v1.2 DRAFT / NOT_ADOPTED / NOT_EFFECTIVE; `MIGRATION_DEBT != EXEMPTION`; `Approval: NOT_RECORDED`; F-02 overall PARTIAL; F-06 OPEN.
- **Self-reference:** D7 cannot contain its own post-commit blob; the post-commit read-back is recorded in a PR comment. This is the same disclosure pattern used for earlier non-self-referential records.

**中文**

## D7 v2.3 修订说明

本次修订响应协调方在准备 R6 所要求的独立复审过程中提出的规范性边界问题。本修订不构成独立验收，也不改变任何批准状态。

- **规范性边界（P1，新增）：**此前 v1.2 正文替换了规范路径 `00-governance/bilingual-documentation-policy.md` 上的 NORMATIVE v1.1 文件。草案占据规范路径，等于在未经批准的情况下把唯一的规范性文本从其权威位置移除，也与本 PR 关于「v1.2 不因合并而生效」的声明相矛盾。处置：规范路径恢复为 v1.1 原文（blob `0e170479e1a71e8f4c124c6f1dc170241652f42b`，与当前 main `a22024112fce3851428343ca3e655712057e6dce` 逐字节一致）；v1.2 拟议文本迁移至 `00-governance/drafts/GOV-DOC-001-v1.2-DRAFT.md`（blob `d91bd92b79177decc7baa038fdd24b3f8323b995`），并附明确非规范性横幅。
- **v2.2 缺陷更正：**两处字面反斜杠转义曾破坏 §2.2 的项目符号与 §7.1 的表格行，现改为真实换行；§7.1 中文表格与英文表格对齐（三次运行）；§3.3 与 v2.2 修订说明中针对 v2.2 后快照的 `ahead 8` 更正为 `ahead 10`，与英文文本一致；删除文件末尾的杂散标记。
- **清单：**§3.2 保留 R6 的 OBJ-07 快照作为历史，并新增 v2.3 当前清单：D1 已迁移，D1-N 记录恢复后的规范 blob。D2–D6 与 R6 读回结果逐字节一致。
- **门禁接线不变：**`scripts/check_bilingual_docs.py` 仍对触及 `00-governance/` 的变更校验 `POLICY-INHERITANCE-DECLARATION` 块，此点已经 R6 接受。由于继承要求源自尚未采纳的 v1.2 草案，该接线登记为工具层的声明校验，不构成政策采纳；采纳状态仍为 `NOT_ADOPTED`。
- **效力边界不变：**GOV-DOC-001 v1.1 NORMATIVE；v1.2 DRAFT / NOT_ADOPTED / NOT_EFFECTIVE；`MIGRATION_DEBT != EXEMPTION`；`Approval: NOT_RECORDED`；F-02 总体 PARTIAL；F-06 OPEN。
- **自引用：**D7 无法包含自身提交后的 blob；提交后读回登记于 PR 评论。此披露方式与既往非自引用记录一致。

**EN**

## D7 v2.4 Revision Note

This revision responds to the R7 independent review (final disposition `NEEDS-REVISION`, two P1 findings). It changes tooling behaviour only; no policy text, status, or approval state changes.

- **P1 (adoption-by-tooling) — remedied:** the `POLICY-INHERITANCE-DECLARATION` check is downgraded from a blocking gate error to an advisory notice. Because the inheritance requirement originates from the unadopted v1.2 draft, a blocking check would have imposed an unapproved normative obligation through tooling. The validator and its tests are retained; enforcement is deferred until formal adoption.
- **P1 (exception record) — remedied by external registration:** the RULING-06 five-field exception for the platform-unavailability compensation is registered in a PR comment rather than in this report, so that the authorising record is attributable and not self-issued by the report under review.
- **P2 (merge is not approval) — stated explicitly:** merging this PR does not constitute approval, adoption, or normative activation of GOV-DOC-001 v1.2. v1.1 remains the only NORMATIVE text at the normative path.
- **P2 (required-check re-verification) — deferred with an owner and a trigger:** the required-check configuration is re-verified when the GitHub Actions billing block is lifted; until then Requirement 2 stays `NOT_VERIFIED`.
- Gate re-execution at the v2.4 head remains local (platform compensation path); the exact-Head evidence and blob read-backs are recorded in the PR comment for this revision.

**中文**

## D7 v2.4 修订说明

本次修订响应 R7 独立复审（最终结论 `NEEDS-REVISION`，两项 P1）。仅改变工具行为，不改变任何政策正文、状态或批准状态。

- **P1（以工具实现事实采纳）——已修复：**`POLICY-INHERITANCE-DECLARATION` 校验由阻断性门禁错误降级为非阻断提示。由于继承要求源自尚未采纳的 v1.2 草案，阻断性校验等于以工具施加未获批准的规范义务。校验器及其测试保留，强制执行推迟至正式采纳之后。
- **P1（例外记录）——以外部登记方式修复：**平台不可用补偿所依据的 RULING-06 五字段例外登记于 PR 评论，而非本报告内，以使授权记录可归属、不由被审报告自我签发。
- **P2（合并不等于批准）——已显式声明：**合并本 PR 不构成对 GOV-DOC-001 v1.2 的批准、采纳或规范性生效。规范路径上唯一的 NORMATIVE 文本仍为 v1.1。
- **P2（required-check 复验）——带责任与触发器推迟：**待 GitHub Actions 计费阻塞解除后复验 required-check 配置；在此之前要求 2 维持 `NOT_VERIFIED`。
- v2.4 head 上的门禁复跑仍为本地执行（平台补偿路径）；该精确 head 的证据与 blob 读回登记于本次修订的 PR 评论。

## D7 v2.5 Revision Note

This revision closes the two findings left in an indeterminate state and removes the structural cause that kept them re-openable. It changes no policy text, no normative status, and no approval state.

- **New §0 record boundary.** Bound assets (HEADs, blob SHAs, PR state, run ids, manifests) are dated snapshots; live assertions (finding states, normative statements, blockers) are maintained. Maintenance must append a new dated snapshot rather than rewrite an old one. Without this rule F-08 was unsatisfiable: any commit changes `main`, so a report asserting current HEADs is stale on merge.
- **Post-merge snapshot §2.2 and post-merge manifest §3.2.** PR #271 is recorded as `merged=true` at `2026-11-19T17:16:13Z`, merge `f86fddc0`, parents `a2202411` + `1eefa22e`; the reviewed head is therefore contained in `main`. The post-merge manifest is read back at `main` `8b7897f1`. The pre-merge `diverged` comparisons are retained as bound snapshots and explicitly marked superseded as current assertions.
- **F-08 and F-09 set to `CLOSED` with a stated basis.** Both were previously annotated `corrected; independent re-review pending`, which is not a maintainable state: a finding that can never be closed by its own rule blocks the report permanently.
- **Sequencing correction recorded, not hidden.** The PR #271 acceptance record listed F-08 and F-09 as closed before any review examined them; R7 and R8 reviewed other findings. The closure recorded here rests on this revision and its review, and does not retroactively validate that line. The correction is written into §9 in both languages rather than silently repaired.
- **Required actions refreshed.** Items 2, 3 and 5 are `DONE`; item 4 is `SUPERSEDED` by merge containment; item 6 is `OUT-OF-SCOPE(dev-baseline)` because it needs accountable human authority, which a single shared identity cannot supply. Platform residuals are tracked in Issue #283 with re-verification triggers.
- **R1 review remediation.** The R1 review of this revision returned `NEEDS-REVISION` with one P1 and two P2. P1: a correction to the PR #271 acceptance record must be made on PR #271 itself, because that record is an independent historical decision and cannot be corrected from inside another report; the correction comment is posted there as `7017127588` and cited from this revision. P2: closure evidence must be re-derivable by a third party, so F-08 and F-09 now name the endpoint, parameter, expected value and comparison for each closure, and separate that objective part from the reviewer judgement. P2: a closure that can never be re-opened is self-exemption, so §0 now carries a re-open trigger and the report states the test that falsifies it.
- **R2 review remediation.** The R2 review returned `NEEDS-REVISION` with two P2 and one P3. P2: the re-open trigger needs a per-revision check record, now added as a section in §9 that applies the three conditions and reports that the third one fired and was repaired before merge. P2: closure evidence lacked HTTP method, authentication preconditions, failure handling and a one-to-one request-to-assertion mapping, all now in §0 and in the E1–E6 table. P3: the post-correction status of F-08 and F-09 must read `corrected, not independently confirmed`, so that withdrawing a `CLOSED` claim is not misread as re-confirming it.

## D7 v2.5 修订说明

本修订关闭两项处于未决状态的 finding，并移除使它们反复重开的结构性成因。不改变任何政策文本、不改变规范状态、不改变批准状态。

- **新增 §0 记录边界**：绑定资产（HEAD、blob SHA、PR 状态、run id、manifest）属于带时点快照；活动断言（finding 状态、规范陈述、阻塞项）受维护。维护应追加新快照，不得改写旧快照。无此规则时 F-08 在逻辑上不可满足：任何提交都会改变 `main`，把 HEAD 当当前断言的报告在合并时即陈旧。
- **合并后快照 §2.2 与合并后 manifest §3.2**：PR #271 记为 `merged=true`（`2026-11-19T17:16:13Z`，merge `f86fddc0`，parents `a2202411` + `1eefa22e`），被审 head 因此已包含于 `main`。合并后 manifest 在 `main` `8b7897f1` 读回。合并前的 `diverged` 比较作为绑定快照保留，并明确标注为已被取代的当前断言。
- **F-08 与 F-09 置为 `CLOSED` 并附依据**：此前标注为「已更正，待独立复审」，而这不是可维护状态——一项永远无法按自身规则关闭的 finding，会使报告永久阻塞。
- **时序更正入库而非静默修补**：PR #271 验收记录在任何审查看过 F-08/F-09 之前就将其列为已关闭；R7 与 R8 审的是其他 finding。本处记录的关闭依据本修订及其审查，不构成对那一行的溯及追认。中英两份 §9 均已写入该更正。
- **必需行动刷新**：第 2、3、5 项为 `DONE`；第 4 项因合并包含关系而 `SUPERSEDED`；第 6 项为 `OUT-OF-SCOPE(dev-baseline)`，因其需要可归属人类权威，单一共享身份无法提供。平台残留已在 Issue #283 中带复验触发器跟踪。
- **R1 审查整改**：本修订的 R1 审查结论为 `NEEDS-REVISION`（1×P1 + 2×P2）。P1：对 PR #271 验收记录的更正必须发在 PR #271 本身，因为该记录是独立的历史决策，不能由另一份报告从内部修正；更正评论已在该处发布并由本修订引用。P2：关闭证据必须可由第三方重新推导，故 F-08 与 F-09 现已逐项给出端点、参数、期望值与比对方式，并与审查判断分离。P2：永不可重开的关闭等于自我豁免，故 §0 现携带重新开启触发器，并写明可反驳它的检验。
- **R2 审查整改**：R2 结论为 `NEEDS-REVISION`（2×P2 + 1×P3）。P2：重新开启触发器需逐次修订的核对记录，已在 §9 新增小节，逐项应用三个条件，并记录第三项实际触发、已在合并前修复。P2：关闭证据缺 HTTP 方法、认证前提、失败响应处理与请求—断言一一映射，已分别补入 §0 与 E1–E6 表。P3：F-08/F-09 在外部更正时点的状态必须读作 `corrected, not independently confirmed`，以免将「撤回 CLOSED」误读为「重新确认关闭」。

## D7 v2.6 Revision Note

This revision is the first application of the §0 re-open trigger to already-merged text. It fixes a contradiction and, more importantly, records what the contradiction did to a finding's status.

- **The contradiction.** §11 stated that "CI workflow integration and required-check enforcement have not yet been established". §7.1 records three successful runs and §10 marks Requirement 1 `COMPLETE / VERIFIED`. The two statements cannot both hold; the earlier one conflated workflow integration with platform required-check enforcement, which is precisely the F-09 defect class.
- **The consequence for F-09.** Under §0, a falsified maintained assertion sets the affected finding back to `OPEN`. F-09 was therefore re-opened in this revision, the failed assertion is named in §9, and `CLOSED` is re-established only by this revision and its review. This is the mechanism's first real test, and it was recorded rather than quietly reinterpreted.
- **A second, wider instance of the same class.** Every revision note from v2.1 onward carried status lines that were true when written and are not true now — v2.2's note still says F-06 "remains OPEN". Those notes are now explicitly labelled as bound snapshots of their own revision, not maintained state, and current statuses are located in §9 and §10 only.
- **Section 11 corrected in both languages**, with the correction stated as a correction rather than silently replaced.
- No policy text, normative status, approval state or adoption state changes. v1.1 remains the only NORMATIVE text. F-02 stays PARTIAL on Requirement 2 only.

## D7 v2.6 修订说明

本修订是 §0 重新开启触发器首次应用于**已合并文本**。它修正一处矛盾，更重要的是记录该矛盾对 finding 状态造成了什么。

- **矛盾所在**：§11 声称「CI workflow 接入及 required check 强制生效尚未得到证实」；而 §7.1 记录三次成功运行，§10 将要求 1 记为 `COMPLETE / VERIFIED`。两者不可能同时成立；前者将「workflow 接入」与「平台 required-check 强制」混为一谈，而这正是 F-09 的缺陷类型。
- **对 F-09 的后果**：按 §0，被证伪的受维护断言应将相应 finding 置回 `OPEN`。因此本修订将 F-09 重新开启，在 §9 点名失败断言，并仅在本修订及其审查通过后重新关闭。这是该机制的首次真实检验，已如实登记，而非静默重新诠释。
- **同类缺陷的第二处、范围更广**：自 v2.1 起的每份修订说明都带有写下时成立、如今不成立的状态行（v2.2 说明仍写 F-06 「remains OPEN」）。这些说明现已明确标为属于其所属修订的绑定快照、非受维护状态；当前状态仅以 §9 与 §10 为准。
- **§11 中英两份均已更正**，且以「更正」形式写明，而非静默替换。
- 不改变任何政策文本、规范状态、批准状态、采纳状态；v1.1 仍为唯一 NORMATIVE；F-02 仅因要求 2 而为 PARTIAL。

## D7 v2.7 Revision Note

This revision closes a hole in the previous one: the registry of findings. It also discharges the two tracking items left open by the R1 review of PR #286.

- **Finding registry added.** F-01, F-03, F-04 and F-05 existed only inside the bound R6 snapshot (§6.3) and had no maintained state anywhere. A finding with no maintained state is indistinguishable from a dropped finding. All ten are now registered with a state and a basis, and where the registry differs from §6.3 the registry governs.
- **A third state category.** `LIMITATION` is introduced in §0 for statements that are true, permanent and not actionable — F-05 is the first. Without it, a boundary is either kept `OPEN` forever or quietly treated as closed; both are dishonest.
- **F-03 and F-04 closed as method-bound, with the basis attributed.** Their text is a rule about method (partial remediation does not establish complete closure), not a defect with a patch, and the report now enforces that distinction. The basis is proposed here and marked as requiring this PR’s review; it is not presented as an R6 finding.
- **Status cross-check list added (§9).** Five checks, run every time a status sentence is touched, together with this revision’s result. Two acceptance-matrix rows had drifted (AC-14, AC-05) and were corrected here.
- **R1 tracking items from PR #286 discharged.** The bound-snapshot declaration now says it binds the original record at its revision timepoint and explicitly does not assert the historical state was permanently correct; the cross-check list is the second item.
- **R1 review remediation.** The R1 review of this revision returned `NEEDS-REVISION` with two P2 and one P3, all three about the new mechanisms having no failure mode. P2: F-03/F-04 closure had no falsifiable test, so check c9 was added — a `CLOSED` basis must be either a re-derivable verification or a rule change with review attribution, and the exact basis that would make F-03 fail is written down so the test can be re-run. P2: `LIMITATION` had no re-evaluation trigger, so §0 now states three mandatory conditions (factually true, no work item removes it, no executable path) and returns the entry to `OPEN` if any fails. P3: the cross-check verified that states exist but not that their bases survive, so c6 (basis validity), c7 (maintenance location reachable) and c8 (closure conditions met) were added, with this revision’s results recorded.
- **R2 review remediation.** The R2 review returned `NEEDS-REVISION` with two P2, both about claims that were written but not evidenced. P2: the c9 negative test was described but not recorded as an executable test, so an execution record now gives two concrete input rows with expected and actual verdicts (T1 the accepted basis, T2 the remediation-only basis), including the statement that no automation exists and none is claimed. P2: `LIMITATION` excluded paths by assertion, so §0 now requires the enumerated paths, the exclusion reason for each, and the confirming review; F-05 lists three paths and why each fails.
- No policy text, normative status, approval state or adoption state changes. v1.1 remains the only NORMATIVE text. F-02 stays PARTIAL on Requirement 2 only.

## D7 v2.7 修订说明

本修订堵上上一版的一个缺口：finding 登记表。同时消账 PR #286 的 R1 审查留下的两项跟踪项。

- **新增 finding 登记表**：F-01、F-03、F-04、F-05 此前只存在于绑定快照 §6.3 中，在任何地方都没有受维护的状态。一项没有受维护状态的 finding，与被遗忘的 finding 无法区分。现十项全部登记状态与依据；与 §6.3 不一致时以本表为准。
- **第三类状态**：§0 新增 `LIMITATION`，用于「成立、永久、不可行动」的陈述（F-05 为首例）。若无此类，边界要么永远保持 `OPEN`，要么被默认当作已关闭，两者都不诚实。
- **F-03 与 F-04 以「方法性」为由关闭，且依据归属明确**：其文字是关于方法的规则（部分修复不等于完全关闭），非可补丁缺陷，而本报告现已强制该区分。该依据由本修订提出并标注待本 PR 审查确认，不冒充 R6 的 finding。
- **新增状态交叉核对清单（§9）**：五项核对，每次涉及状态句即执行，并附本修订结果。已发现两行验收矩阵脱节（AC-14、AC-05）并在本次修正。
- **PR #286 的 R1 跟踪项已消账**：绑定快照声明已改为「绑定原始记录在其修订时点」并明确不声称历史状态永久正确；交叉核对清单即第二项。
- **R1 审查整改**：R1 结论为 `NEEDS-REVISION`（2×P2 + 1×P3），三项均指向同一问题：新机制没有失败模式。P2：F-03/F-04 的关闭缺可反驳检验，故新增 c9——`CLOSED` 依据必须是可重推验证或规则变更加审查归属，并写明「使 F-03 失败的那个依据」以便重跑。P2：`LIMITATION` 缺重新评估触发器，故 §0 现写明三项必备条件（事实成立、无工作项可消除、无可执行路径），任一失效即回到 `OPEN`。P3：交叉核对只查状态存在、不查依据是否存续，故新增 c6（依据有效性）、c7（维护位置可达）、c8（关闭条件满足），并记录本修订执行结果。
- **R2 审查整改**：R2 结论为 `NEEDS-REVISION`（2×P2），两项均指向「写了声明但未留证据」。P2：c9 的反例测试只被描述、未作为可执行测试记录，故新增执行记录：两个具体输入行与预期/实际结果（T1 采用的依据、T2 仅靠补丁的依据），并写明无自动化实现、也不声称有。P2：`LIMITATION` 的路径排除只是声称，故 §0 现要求列出已排查路径、逐条排除理由与确认审查；F-05 已列三条路径及各自失败原因。
- 不改变任何政策文本、规范状态、批准状态、采纳状态；v1.1 仍为唯一 NORMATIVE；F-02 仅因要求 2 而为 PARTIAL。

## D7 v2.8 Revision Note

This revision is the first full run of the c1–c9 cross-check against the merged report, and it reports what that run found rather than asserting that the check exists.

- **c2 was wrong, not the report.** It required §10 to carry every finding; §10 is a stage ledger and carries six of ten by design. An unsatisfiable check is a defect in the check, so c2 was rewritten to the single-index rule: the registry is the index, §10 must agree where it speaks, and absence from §10 is acceptable when the registry names where the state lives.
- **c4 fired on AC-01.** It still read "PARTIAL — F-03/F-04 require further closure" while the registry marks both `CLOSED (method-bound)`. Corrected, and the earlier wording is named in the row rather than silently replaced.
- **Seven checks clear**, each with a stated basis rather than a bare "clear".
- No policy text, normative status, approval state or adoption state changes. v1.1 remains the only NORMATIVE text. F-02 stays PARTIAL on Requirement 2 only.

## D7 v2.8 修订说明

本修订是 c1–c9 交叉核对首次对「已合并报告」完整执行，并如实报告执行结果，而不是声称核对存在。

- **错的是 c2 而不是报告**：它要求 §10 携带每一项 finding，而 §10 是阶段台账，设计上只携带十项中的六项。不可满足的核对是核对自身的缺陷，故将 c2 改为「单一索引」规则：登记表为唯一索引，§10 一旦发言必须一致，未出现于 §10 可接受（需登记表写明维护位置）。
- **c4 实际触发于 AC-01**：它仍写「F-03/F-04 require further closure」，而登记表已将二者记为 `CLOSED (method-bound)`。已修正，且在行内点名原表述，而非静默替换。
- **七项清**，且每项附依据而非空写「清」。
- 不改变任何政策文本、规范状态、批准状态、采纳状态；v1.1 仍为唯一 NORMATIVE；F-02 仅因要求 2 而为 PARTIAL。


## D7 v2.9 Revision Note

This revision records A Integration's confirmation of the twelve later PR groupings identified by the F-06 object-level reconciliation. It changes the maintained inventory/group-registration assertion only; it does not complete historical bilingual migration or change any policy/adoption status.

- **The twelve proposals are now registered.** PRs #48 and #271–#281 were individually read back by exact PR number, including title, body, state, merged flag and exact Head. A Integration confirmed their existing proposed groups (P-01/P-02/P-04/P-05) and registered each object in `00-governance/bilingual-governance-migration-register.md` §8.4.2.
- **Coverage at the dated reconciliation baseline is 242/242.** The original 232-object inventory snapshot is preserved as historical; the 242-object count is bound to reconciliation baseline `f86fddc0fa0291ea8a5e080e741f083ce179a0a2`. This is not a live count of PRs created after that baseline.
- **Authority is bounded.** A Integration confirms group classification only. All group `Accountable_Owner` values remain `NOT_ASSIGNED`; no target-group Owner or Project Owner approval is inferred.
- **Migration debt is unchanged.** P-01..P-06 remain `MIGRATION_DEBT`; no historical PR body is translated or reclassified by this grouping update. PR #48 remains CLOSED / not merged. Issue #254 remains HOLD.
- **F-06 remains CLOSED at object-reconciliation scope.** This does not mean historical bilingual migration is complete, and it does not create an exemption.

Register evidence: commit `d344f43ce0d4b8eb9bab19da8ca30e4a518f1117`, Blob `46cabb97f63597eb3e8623c60305ed58980355f7`.

## D7 v2.9 修订说明

本修订记录 A Integration 对 F-06 对象级对账中识别的后续 12 个 PR 归组提案作出确认。只更新受维护的清点/归组登记断言；不代表历史双语迁移完成，也不改变任何政策或采纳状态。

- **12 个提案现已登记。**逐一按 PR 编号读取 #48、#271–#281 的标题、正文、状态、合并标志及精确 Head；A Integration 按既有提案确认其 P-01/P-02/P-04/P-05 归组，并登记于迁移登记册 §8.4.2。
- **带时点对账基线覆盖 242/242。**原始 232 个对象清点快照作为历史保留；242 个对象的数字绑定于对账基线 `f86fddc0fa0291ea8a5e080e741f083ce179a0a2`，不代表该基线之后创建的 PR 实时总数。
- **权责边界不变。**A Integration 只确认集成单元归组；各组 `Accountable_Owner` 仍为 `NOT_ASSIGNED`，不推定目标组 Owner 或 Project Owner 批准。
- **迁移欠账不变。**P-01 至 P-06 继续为 `MIGRATION_DEBT`；本次归组不翻译或重新分类任何历史 PR 正文。PR #48 仍为 CLOSED / not merged；Issue #254 仍为 HOLD。
- **F-06 在对象级对账范围内保持 CLOSED。**不代表历史双语迁移已完成，也不产生豁免。

登记册证据：commit `d344f43ce0d4b8eb9bab19da8ca30e4a518f1117`，Blob `46cabb97f63597eb3e8623c60305ed58980355f7`。

## D7 v2.10 Revision Note

This revision changes one maintained state — F-02 Requirement 2, and with it F-02 overall. It changes no policy text, no normative status, no approval state and no adoption state.

- **`NOT_VERIFIED / PLATFORM-LIMITED BLOCKER` → `COMPLETE / VERIFIED`; F-02 overall `PARTIAL` → `COMPLETE / VERIFIED`.** Live assertions edited, by section: §6.4 Requirement 2 heading and body and the closing F-02 line (EN and ZH); §7.1 status lines (EN and ZH); the §7.2 paragraph that told the reader not to mark F-02 COMPLETE (EN and ZH); the §9 finding registry row; the §9 P1 block (EN and ZH); a new §7.2.2; a superseded pointer appended to §7.2.1's EN and ZH paragraphs without altering its readings.
- **The measurement (2026-11-25).** Repository `private: false`, `visibility: public`. `GET /branches/main/protection` → 200, `required_status_checks.strict: true`, `enforce_admins.enabled: true`, 16 contexts, `required_pull_request_reviews` absent. `GET /rulesets` → 200 `[]`, so this is classic branch protection rather than a ruleset. `GOV-DOC-001 structural checks` is one of the 16.
- **The falsifiable control.** PR #1038 at head `b5cf4f25` was reported `mergeable: true` and then refused by `PUT /pulls/1038/merge` with 405 and the raw message `Required status check "rust-workspace-test" is failing.`; the PR was closed unmerged. This is the deliberately failing experiment that §7.2.1 recorded as not having been run.
- **What did NOT change, stated so this revision cannot be over-read.** (i) The declaration step `check_policy_inheritance` inside `scripts/check_bilingual_docs.py` is still advisory: the job is blocking, one of its steps is not. (ii) `required_pull_request_reviews` is still absent, so this revision establishes required-check enforcement only, not review enforcement. (iii) The three workflow runs in §7.1 and the 2026-11-20 403 readings in §7.2.1 remain bound snapshots at their own timepoints; §7.2.1 carries a status pointer to §7.2.2 instead of being rewritten. (iv) No policy adoption and no Owner approval is implied — a merge rejection is platform behaviour, not a governance decision.
- **Bound-snapshot status of this note.** Per §0, every revision note is a bound snapshot of its own revision; current finding states live in §9.

## D7 v2.10 修订说明

本修订只改变一项受维护状态——F-02 要求 2，以及随之而来的 F-02 总体。不改变任何政策文本、规范状态、批准状态与采纳状态。

- **`NOT_VERIFIED / PLATFORM-LIMITED BLOCKER` → `COMPLETE / VERIFIED`；F-02 总体 `PARTIAL` → `COMPLETE / VERIFIED`。**按节列出被编辑的活动断言：§6.4 要求 2 的标题与正文、以及收尾的 F-02 行（中英）；§7.1 状态行（中英）；§7.2 中原本要求「不得将 F-02 标记为 COMPLETE」的段落（中英）；§9 finding 登记行；§9 P1 区块（中英）；新增 §7.2.2；在 §7.2.1 中英两段末尾各追加一行取代指针，其读数未被改写。
- **测量（2026-11-25）。**仓库 `private: false`、`visibility: public`。`GET /branches/main/protection` → 200，`required_status_checks.strict: true`、`enforce_admins.enabled: true`、16 个 contexts、`required_pull_request_reviews` 缺失。`GET /rulesets` → 200、内容 `[]`，故为经典 branch protection 而非 ruleset。`GOV-DOC-001 structural checks` 是这 16 个之一。
- **可证伪的反向对照。**PR #1038 在 head `b5cf4f25` 上先被报告 `mergeable: true`，随后 `PUT /pulls/1038/merge` 被以 405 拒绝，原始消息 `Required status check "rust-workspace-test" is failing.`；该 PR 以未合并状态关闭。这正是 §7.2.1 记为尚未运行的那次故意失败实验。
- **未改变的部分（写明以免本修订被过度解读）：**（i）`scripts/check_bilingual_docs.py` 内的声明步骤 `check_policy_inheritance` 仍为非阻断：job 为阻断，其内部仍有一步不是。（ii）`required_pull_request_reviews` 仍缺失，故本修订只建立 required-check 强制，不建立审查强制。（iii）§7.1 的三次 workflow 运行与 §7.2.1 的 2026-11-20 403 读数仍为各自时点的绑定快照；§7.2.1 追加的是状态指针而非改写。（iv）不推定任何规范采纳或 Owner 批准——合并拒绝是平台行为，不是治理决定。
- **本说明的快照地位。**按 §0，每份修订说明都是其所属修订的绑定快照；当前 finding 状态以 §9 为准。
