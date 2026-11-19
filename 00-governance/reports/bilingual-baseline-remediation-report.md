# GOV-DOC-001 v1.2 Bilingual Baseline Remediation Report
# GOV-DOC-001 v1.2 双语基线修复交付报告

- Work Item ID: GOV-DOC-001-V1.2-REMEDIATION
- Policy ID: GOV-DOC-001
- Proposed Version: 1.2
- Status: DRAFT — NEEDS REVISION — PENDING FORMAL GOVERNANCE APPROVAL
- Repository: oahcom/AiMemoryBrainArchitecture
- Target Branch: remediation/gov-doc-001-v1.2-bilingual-baseline
- Pull Request: #271
- Report Version: v2.1 / 文档版本：v2.1
- Revision Date: 2026-11-19 / 修订日期：2026-11-19

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
- Current main...PR head comparison: `diverged`; ahead 8 / behind 42; merge base `c5a995d9a2808112b007a9108e085048cbed5cc9`

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

The initial seven-file submission and the later D7 report-restoration commit are distinct historical events. The original submission commit must not be presented as the current branch head. The R6 baseline head above is the pre-v2.2 remediation head; the v2.2 corrective commit is recorded in the subsequent GitHub commit/read-back evidence.

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

提交 `47369925ace93821eab82e4cec8418f8d7505d64` 未修改 D2。本 D7 v2.2 变更集仅修改 D7，不修改 D2。

### 3.3 Verification result / 验证结果

**Historical verification note / 历史验证说明**

The original verification in this section applied to the previously committed D7 Version 1.0. The subsequent Version 2.0 proposal was later committed, and the Version 2.1 report was committed at the R6 remediation head. The current verification target must be distinguished from those historical targets.

本节最初的验证针对此前已提交的 D7 Version 1.0。后续 Version 2.0 提案已经提交；Version 2.1 报告也已提交至 R6 修复分支 head。当前验证目标必须与上述历史目标区分。

**R6 OBJ-07 read-back / R6 OBJ-07 读回**

R6 independently read back all seven files against the OBJ-07 manifest snapshot: 7/7 matched. The D7 v2.1 blob in that snapshot is `8fa00af52a6c61e36f850c90332006360b8a82df`. The v2.2 revision changes D7 only; the new D7 blob is verified separately by post-commit read-back and must not be retroactively substituted into the pre-v2.2 OBJ-07 snapshot.

R6 已依据 OBJ-07 manifest 快照独立读回全部七个文件：7/7 匹配。该快照中的 D7 v2.1 blob 为 `8fa00af52a6c61e36f850c90332006360b8a82df`。v2.2 修订仅修改 D7；新的 D7 blob 通过提交后的独立读回单独验证，不得追溯替换 v2.2 之前的 OBJ-07 快照。

**Current verification boundary / 当前验证边界**

The R6 independent review of Version 2.1 returned `NEEDS-REVISION`. This Version 2.2 report records the corrective response to R6 findings; it is not itself an independent acceptance. A fresh independent review must evaluate the exact v2.2 commit. Current main...PR comparison remains `diverged` (ahead 8 / behind 42); successful Exact-Head integration verification has not been established.

R6 对 Version 2.1 的独立复审结论为 `NEEDS-REVISION`。本 Version 2.2 报告记录对 R6 findings 的修正响应；本报告本身不构成独立验收。必须由新的独立复审针对 v2.2 精确提交进行评估。当前 main 与 PR 比较仍为 `diverged`（ahead 8 / behind 42）；尚未建立 Exact-Head 集成复核通过证据。

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

1. **Requirement 1 — validator integrated and invoked by CI: COMPLETE / VERIFIED.**
   - Workflow: `.github/workflows/bilingual-docs.yml`, blob `fbb01f4cf6c1046fb4f3f6f962d1caed921577b2`.
   - Validator: `scripts/check_bilingual_docs.py`, blob `cfae34de1d07d4366850d439cb7c1e643d43cfae`.
   - The workflow step `Check paired documentation and PR manifest` runs `python3 scripts/check_bilingual_docs.py`.
   - The validator's `main()` calls `check_policy_inheritance(body, changed)`.

2. **Requirement 2 — corresponding required check configured and enforced: NOT_VERIFIED / PLATFORM-LIMITED BLOCKER.**
   - `GET /branches/main/protection` returned HTTP 403:
     `{"message":"Upgrade to GitHub Pro or make this repository public to enable this feature."}`
   - `GET /rulesets` returned the same HTTP 403 plan-limit response.
   - These responses establish a GitHub plan/visibility limitation for this private repository, not a token-permission failure. Required-check configuration/enforcement and failure-blocking behavior therefore remain unverified.

**F-02 overall status: PARTIAL.** CI integration is verified; required-check enforcement is not verified. Successful workflow execution must not be treated as proof that the platform enforces the check.

**中文**

#### F-02 — 独立校验器与 CI 接入状态

F-02 包含两个相互独立的要求：

1. **要求 1——校验器已接入并由 CI 调用：COMPLETE / VERIFIED（完成/已验证）。**
   - Workflow：`.github/workflows/bilingual-docs.yml`，blob `fbb01f4cf6c1046fb4f3f6f962d1caed921577b2`。
   - 校验器：`scripts/check_bilingual_docs.py`，blob `cfae34de1d07d4366850d439cb7c1e643d43cfae`。
   - Workflow 步骤 `Check paired documentation and PR manifest` 实际运行 `python3 scripts/check_bilingual_docs.py`。
   - 校验器的 `main()` 调用了 `check_policy_inheritance(body, changed)`。

2. **要求 2——对应 required check 已配置并强制执行：NOT_VERIFIED / PLATFORM-LIMITED BLOCKER（未验证/平台限制阻塞）。**
   - `GET /branches/main/protection` 返回 HTTP 403：
     `{"message":"Upgrade to GitHub Pro or make this repository public to enable this feature."}`
   - `GET /rulesets` 返回相同的 HTTP 403 计划限制响应。
   - 该响应证明当前私有仓库受到 GitHub 计划/可见性限制，并非 token 权限不足。因此 required check 的配置、强制执行及失败阻断行为仍未验证。

**F-02 总体状态：PARTIAL（部分完成）。**CI 接入已验证；required check 强制执行尚未验证。Workflow 成功运行不得被当作平台已经强制执行该 check 的证明。

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
- The step runs `python3 scripts/check_bilingual_docs.py`; the script's `main()` invokes `check_policy_inheritance()`.

Two successful workflow executions are independently evidenced:

| Run ID | Tested PR head | Job ID | Job / step result | UTC execution window |
|---|---|---|---|---|
| `44542512889` | `70219731485040e2974d537080f994108ee1d989` | `135624335886` | Job SUCCESS; validator step SUCCESS | `14:19:42Z–14:19:45Z`, 2026-11-19 |
| `44546301573` | `47369925ace93821eab82e4cec8418f8d7505d64` | `135637661718` | Job SUCCESS; validator step SUCCESS | `14:40:30Z–14:40:33Z`, 2026-11-19 |

Both executions reported `Bilingual documentation and prompt-library gate: PASS (11 changed paths inspected).` These runs verify workflow invocation and successful execution on their respective heads. They do not verify platform required-check enforcement.

The earlier structural CI failure run `44477435608` remains historical evidence and is not overwritten by these later successful runs.

**Status:** Requirement 1 COMPLETE / VERIFIED; Requirement 2 NOT_VERIFIED; F-02 overall PARTIAL.

**中文**

#### F-02 CI 验证结果

Workflow 与校验器已完成接入：

- Workflow blob：`fbb01f4cf6c1046fb4f3f6f962d1caed921577b2`。
- 校验器脚本 blob：`cfae34de1d07d4366850d439cb7c1e643d43cfae`。
- Workflow job：`GOV-DOC-001 structural checks`。
- 实际执行步骤：`Check paired documentation and PR manifest`。
- 该步骤运行 `python3 scripts/check_bilingual_docs.py`；脚本的 `main()` 调用 `check_policy_inheritance()`。

已有两次成功的 workflow 执行证据：

| Run ID | 被测 PR head | Job ID | Job / 步骤结果 | UTC 执行时间 |
|---|---|---|---|---|
| `44542512889` | `70219731485040e2974d537080f994108ee1d989` | `135624335886` | Job SUCCESS；校验步骤 SUCCESS | 2026-11-19 `14:19:42Z–14:19:45Z` |
| `44546301573` | `47369925ace93821eab82e4cec8418f8d7505d64` | `135637661718` | Job SUCCESS；校验步骤 SUCCESS | 2026-11-19 `14:40:30Z–14:40:33Z` |

两次执行均报告 `Bilingual documentation and prompt-library gate: PASS (11 changed paths inspected).` 这些运行证明 workflow 在各自 head 上实际调用并成功执行校验器，但不证明平台 required check 已强制生效。

较早的结构 CI 失败运行 `44477435608` 保留为历史证据，不被后续成功运行覆盖。

**状态：**要求 1 COMPLETE / VERIFIED；要求 2 NOT_VERIFIED；F-02 总体 PARTIAL。

### 7.2 Actual gate behavior / 门禁实际行为

**EN**

#### F-02 Gate Behavior — Verified Execution vs Platform Enforcement

The two successful workflow runs establish that the PR workflow invokes the validator and that the validator step completed successfully on the recorded heads.

They do **not** establish:

- The check is configured as a required check in repository branch protection or a ruleset.
- A failing validator result is enforced by the platform as a merge blocker.
- The required-check configuration can be administered under the repository's current private-repository plan.

The branch-protection and ruleset API requests returned HTTP 403 with the GitHub plan-limit message recorded in §6.4. Accordingly, platform enforcement remains `NOT_VERIFIED` and is a platform-limited blocker. Do not mark F-02 COMPLETE.

**中文**

#### F-02 门禁行为——已验证执行与平台强制的区别

两次成功的 workflow 运行证明 PR workflow 实际调用了校验器，且校验器步骤在所记录的 head 上成功完成。

但这些证据**不能**证明：

- 该 check 已在仓库 branch protection 或 ruleset 中配置为 required check；
- 校验器失败时，平台会将其强制作为合并阻断条件；
- 当前私有仓库计划允许管理员配置 required-check 强制规则。

分支保护及 ruleset API 请求返回 §6.4 所记录的 GitHub 计划限制 HTTP 403。因此平台强制状态仍为 `NOT_VERIFIED`，并构成平台限制阻塞。不得将 F-02 标记为 COMPLETE。

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
| AC-01 | Full v1.1 inheritance | v1.1 read; v1.2 committed | PARTIAL — F-03/F-04 require further closure |
| AC-02 | Issue bilingual requirements | Five templates/updates read back | Execution PASS; independent criterion mapping NOT_RECORDED |
| AC-03 | Umbrella Requirement bilingual requirements | D1/D4 and five Issue updates | Execution PASS; independent criterion mapping NOT_RECORDED |
| AC-04 | Commit Message bilingual requirements | D5 and actual bilingual Commit | Execution PASS; historical inventory incomplete |
| AC-05 | PR bilingual title/body | PR title and body bilingual | PARTIAL — CI FAILURE |
| AC-06 | Future repository inheritance | D1/D6 drafted and committed | FAIL — F-02 OPEN |
| AC-07 | Original criterion unspecified | No criterion supplied | NOT TESTABLE |
| AC-08 | Stable identifier preservation | Exact identifiers and SHA manifest checked | Execution PASS; independent mapping NOT_RECORDED |
| AC-09 | Status preservation | Five Issues remain OPEN; Requirement Status RECORDED | Execution PASS |
| AC-10 | No fabricated evidence | Unknown fields and source gaps preserved | Execution PASS within available evidence |
| AC-11 | Historical Commit immutability | No rewrite or force-push | Execution PASS |
| AC-12 | Historical migration registration | Issue/Commit/PR aggregate inventory prepared | PARTIAL — F-06 OPEN |
| AC-13 | Bilingual normative clauses | D1–D7 are embedded bilingual documents | Independent semantic parity not fully accepted |
| AC-14 | Complete file/change manifest | Seven files and five Issue updates verified | PARTIAL — historical inventory incomplete |
| AC-15 | Reproducible independent acceptance | Review package and exact file SHAs recorded | FAIL / BLOCKED — CI failure and outstanding findings |

Execution PASS does not imply independent review PASS.

执行自检 PASS 不等于独立审查 PASS。

独立的当前状态补充表

**EN**

| Item | Current status | Acceptance boundary |
|---|---|---|
| F-02 | PARTIAL | Validator and tests committed; corrected local tests 6/6 PASS. CI workflow integration and required-check enforcement evidence remain outstanding. |
| F-06 Issue inventory | Inventory finalized | 39 records: 28 EN_ONLY, 10 EN_ZH_MIXED, 1 ZH_ORIGINAL_WITH_EN_TERMS (#254, HOLD). Each record requires a matching body_sha256. |
| F-06 Commit inventory | Inventory finalized | 313 records: 312 EN_ONLY, 1 MIXED (C168). Each record requires matching sha and msg_sha256; classification is based on the complete commit message. |
| F-07 | Correction recorded | PR comment `7006445553`; authoritative D1 blob `66517d39`. |
| Normative status | Unchanged | v1.1 NORMATIVE; v1.2 DRAFT. |
| Migration and exemption | Not interchangeable | MIGRATION_DEBT != EXEMPTION. Registration does not establish migration completion. |

**中文**

| 项目 | 当前状态 | 验收边界 |
|---|---|---|
| F-02 | PARTIAL | 校验器及测试已提交；修复后的本地测试 6/6 PASS。CI workflow 接入及 required check 强制生效证据仍未完成。 |
| F-06 Issue 清单 | 登记定稿 | 39 条：28 条 EN_ONLY、10 条 EN_ZH_MIXED、1 条 ZH_ORIGINAL_WITH_EN_TERMS（#254，HOLD）。每条记录均须具有匹配的 body_sha256。 |
| F-06 Commit 清单 | 登记定稿 | 313 条：312 条 EN_ONLY、1 条 MIXED（C168）。每条记录均须具有匹配的 sha 和 msg_sha256；分类依据完整提交消息判定。 |
| F-07 | 更正已登记 | PR 评论 `7006445553`；D1 权威 blob `66517d39`。 |
| 规范状态 | 不变 | v1.1 为 NORMATIVE；v1.2 为 DRAFT。 |
| 迁移与豁免 | 不可互相替代 | MIGRATION_DEBT != EXEMPTION。登记完成不构成迁移完成证明。 |

---

## 9. Outstanding blockers and next actions / 未解决阻塞与后续行动

### P1

**F-02 — platform required-check enforcement**

- Requirement 1 (validator integrated and invoked by CI): COMPLETE / VERIFIED.
- Requirement 2 (required check configured and enforced): NOT_VERIFIED — PLATFORM-LIMITED BLOCKER.
- F-02 overall remains PARTIAL. Do not represent successful workflow runs as platform enforcement.

**F-08 — stale baseline and manifest**

- D7 §2.2 and §3.1–§3.3 have been corrected in this v2.2 revision to distinguish current main, current PR head/tree, historical submission commit, and the R6 OBJ-07 pre-v2.2 manifest snapshot.
- Remediation state: corrected in D7 v2.2; independent re-review pending. Do not mark CLOSED before exact-Head re-review.

**F-09 — stale CI integration status**

- D7 §6.4, §7.1, §7.2, §9 and §10 now distinguish verified workflow integration from unverified platform required-check enforcement.
- Remediation state: corrected in D7 v2.2; independent re-review pending. F-02 overall remains PARTIAL.

### P2

**F-06 — historical object-level reconciliation remains OPEN**

Preserve the 39-Issue and 313-Commit inventory boundaries and complete object-level reconciliation of counts, classification totals, object uniqueness, identity matching, required anchors, and missing/duplicate records. Issue #254 remains within the 39-record set, on HOLD, with its explicit exit conditions.

Fourteen PRs remain unassigned to migration groups because sufficient grouping evidence has not been established:

`#269, #207, #197, #194, #193, #192, #191, #190, #189, #154, #143, #141, #139, #136`.

Do not invent group assignments. F-06 remains OPEN until the object-level evidence and PR grouping/reconciliation are complete. Inventory registration does not establish historical bilingual migration completion.

**F-07 — authoritative baseline correction**

Use D1 authoritative baseline blob `66517d39` and retain PR comment `7006445553` as the correction traceability record.

**F-10 — completed PR manifest declaration**

The PR #271 body declaration `BILINGUAL-MANIFEST: COMPLETE` has already been updated. Record it as completed execution evidence; remove it from the outstanding CI blocker list. This declaration does not imply semantic review PASS, Owner approval, policy adoption, or merge authorization.

### CI blocker

The only remaining F-02 blocker is platform required-check configuration/enforcement. The branch-protection and ruleset endpoints returned HTTP 403 because the repository is private under a plan that does not support these settings. Retain `NOT_VERIFIED`; do not claim the required check is enforced. The workflow integration and successful runs are recorded in §7.1.

### Other required actions

1. Preserve the D2 incremental appendix and its reconciliation work as outstanding; **D2 is not modified by this D7 v2.2 changeset**.
2. Reconcile the 14 unassigned PRs listed above with object-level evidence; do not infer migration groups.
3. Obtain a fresh independent review of the D7 v2.2 exact commit and its read-back evidence.
4. Revalidate Exact-Head against the current main after the v2.2 commit; the pre-v2.2 comparison was `diverged` (ahead 8 / behind 42).
5. Complete F-06 object-level reconciliation and preserve Issue #254 HOLD/exit conditions.
6. Obtain explicit authorized governance approval. Only after approval may policy adoption and effective date be evaluated.

No automatic approval or adoption is permitted.

---

### 后续行动与阻塞（中文）

### P1

**F-02——平台 required-check 强制执行**

- 要求 1（校验器已接入并由 CI 调用）：COMPLETE / VERIFIED。
- 要求 2（required check 已配置并强制执行）：NOT_VERIFIED——PLATFORM-LIMITED BLOCKER。
- F-02 总体维持 PARTIAL。不得将 workflow 成功运行表述为平台强制执行。

**F-08——基线与 manifest 陈旧**

- 本 v2.2 修订已更正 D7 §2.2、§3.1–§3.3，明确区分当前 main、当前 PR head/tree、历史首次提交及 R6 的 v2.2 前 OBJ-07 manifest 快照。
- 修复状态：已在 D7 v2.2 中更正；等待独立复审。Exact-Head 复审通过前不得标记 CLOSED。

**F-09——CI 接入状态陈旧**

- D7 §6.4、§7.1、§7.2、§9 和 §10 已更新，明确区分已验证的 workflow 接入与未验证的平台 required-check 强制状态。
- 修复状态：已在 D7 v2.2 中更正；等待独立复审。F-02 总体仍为 PARTIAL。

### P2

**F-06——历史对象级对账仍为 OPEN**

保留 39 条 Issue 和 313 条 Commit 的清单边界，并完成对象级对账：记录数量、分类总数、对象唯一性、身份匹配、必需锚点及缺漏/重复记录。Issue #254 必须继续包含在 39 条集合内，保持 HOLD，并保留明确退出条件。

以下 14 个 PR 仍未归入迁移组，因为尚无充分归组证据：

`#269, #207, #197, #194, #193, #192, #191, #190, #189, #154, #143, #141, #139, #136`。

不得补造分组。对象级证据及 PR 归组/对账完成前，F-06 保持 OPEN。清单登记不代表历史双语迁移完成。

**F-07——权威基线更正**

后续使用 D1 权威基线 blob `66517d39`，并保留 PR 评论 `7006445553` 作为更正追踪记录。

**F-10——已完成的 PR manifest 声明**

PR #271 正文中的 `BILINGUAL-MANIFEST: COMPLETE` 声明已经更新。应将其记录为已完成执行证据，并从未解决 CI 阻塞项中移除。该声明不代表语义审查 PASS、Owner 批准、规范采纳或合并授权。

### CI 阻塞

F-02 唯一剩余阻塞是平台 required-check 配置/强制执行。由于当前私有仓库所处计划不支持相关设置，branch-protection 和 ruleset API 返回 HTTP 403。继续标记为 `NOT_VERIFIED`，不得声称 required check 已强制执行。Workflow 接入和成功运行已记录于 §7.1。

### 其他必需行动

1. 保留 D2 增量附录及其对账工作为未完成事项；**本 D7 v2.2 变更集不修改 D2**。
2. 使用对象级证据对上述 14 个未归组 PR 完成对账；不得推断迁移组。
3. 针对 D7 v2.2 精确提交及其读回证据开展新一轮独立复审。
4. 在 v2.2 提交后，针对当前 main 重新执行 Exact-Head 复核；v2.2 前比较结果为 `diverged`（ahead 8 / behind 42）。
5. 完成 F-06 对象级对账，并保留 Issue #254 的 HOLD/退出条件。
6. 取得明确且有权的治理批准。只有在批准后，才可评估规范采纳及生效日期。

不得自动推定批准或采纳。

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
| Historical inventory / 历史清单 | PARTIAL | 39 Issues and 313 Commits registered; F-06 object-level reconciliation and 14 unassigned PRs remain OPEN. / 已登记 39 条 Issue、313 条 Commit；F-06 对象级对账及 14 个未归组 PR 仍为 OPEN。 |
| Independent review / 独立复审 | NEEDS-REVISION | R6 review session `6aff0b47-3988-83ec-b666-976e39dfe840` returned NEEDS-REVISION; F-08/F-09/F-10 text corrections are in v2.2 and await fresh independent review. / R6 复审结论 NEEDS-REVISION；F-08/F-09/F-10 已在 v2.2 中更正，等待新一轮独立复审。 |
| F-02 | PARTIAL | Requirement 1 CI integration COMPLETE/VERIFIED; Requirement 2 required-check enforcement NOT_VERIFIED due GitHub plan-limit HTTP 403. / 要求 1 CI 接入 COMPLETE/VERIFIED；要求 2 因 GitHub 计划限制 HTTP 403 而 NOT_VERIFIED。 |
| F-06 | OPEN | 39-Issue / 313-Commit anchors and classification require object-level reconciliation; #254 remains HOLD; 14 PRs remain unassigned. / 39 条 Issue、313 条 Commit 的锚点和分类仍需对象级对账；#254 保持 HOLD；14 个 PR 未归组。 |
| F-07 | CORRECTION RECORDED | PR comment `7006445553`; authoritative D1 baseline blob `66517d39`. / PR 评论 `7006445553`；D1 权威基线 blob `66517d39`。 |
| Structural CI / 结构 CI | MIXED HISTORICAL RECORD | Failure run `44477435608` retained as historical; later runs `44542512889` and `44546301573` SUCCESS. Required-check enforcement remains NOT_VERIFIED. / 失败运行 `44477435608` 保留为历史记录；后续运行 `44542512889`、`44546301573` SUCCESS。required-check 强制执行仍为 NOT_VERIFIED。 |
| Owner approval / Owner 批准 | NOT_RECORDED | No explicit Owner approval evidence. / 无明确 Owner 批准证据。 |
| Policy adoption / 规范采纳 | NOT_ADOPTED | GOV-DOC-001 v1.2 remains DRAFT; no adoption evidence. / GOV-DOC-001 v1.2 仍为 DRAFT；无采纳证据。 |
| Effective status / 生效状态 | NOT_EFFECTIVE | v1.1 remains NORMATIVE; v1.2 is not effective. / v1.1 仍为 NORMATIVE；v1.2 尚未生效。 |

`Approval: NOT_RECORDED`  
`Adoption: NOT_ADOPTED`  
`MIGRATION_DEBT != EXEMPTION`

## 11. Honest declaration / 诚实声明

### EN


This report records the verified delivery and review status as of 2026-11-19.

The independent validator, declaration, and tests have been committed. The corrected local test suite reports 6/6 PASS. CI workflow integration and required-check enforcement have not yet been established; F-02 therefore remains PARTIAL.

The historical language inventories have been finalized with 39 Issue records and 313 Commit records. Issue #254 is included in the 39-record Issue inventory, classified as `ZH_ORIGINAL_WITH_EN_TERMS`, and remains on HOLD. Commit language classification is based on the substantive content of the complete commit message. Inventory registration does not establish bilingual migration completion.

The F-07 correction record is registered in PR comment `7006445553`. The authoritative D1 baseline blob is `66517d39`.

Normative status remains unchanged: v1.1 is NORMATIVE and v1.2 is DRAFT. Migration debt is not an exemption. This report does not imply Owner approval, normative adoption, PR merge authorization, or completion of historical content migration.

Any item for which complete supporting evidence has not been established must remain explicitly identified as incomplete or unverified. This report must not be interpreted as a claim that all audits, CI gates, migration work, or governance approvals are complete.

### 中文


本报告记录截至 2026-11-19 已核实的交付与审查状态。

独立校验器、配套声明及测试已提交入库。修复后的本地测试套件结果为 6/6 PASS。CI workflow 接入及 required check 强制生效尚未得到证实，因此 F-02 继续保持 PARTIAL。

历史语言状态清单已定稿，包含 39 条 Issue 记录和 313 条 Commit 记录。Issue #254 包含在 39 条 Issue 清单内，分类为 `ZH_ORIGINAL_WITH_EN_TERMS`，当前保持 HOLD。Commit 语言分类依据完整提交消息的实质内容判定。清单登记完成不代表双语迁移完成。

F-07 更正记录已登记于 PR 评论 `7006445553`。D1 权威基线 blob 为 `66517d39`。

规范效力状态保持不变：v1.1 为 NORMATIVE，v1.2 为 DRAFT。迁移债务不构成豁免。本报告不表示 Owner 已批准、规范已被采纳、PR 已获得合并授权，或历史内容迁移已经完成。

凡尚未取得完整支持证据的事项，必须明确标记为未完成或未验证。本报告不得被解释为所有审计、CI 门禁、迁移工作或治理批准均已完成的声明。

---

**EN**

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
- The pre-v2.2 current-main comparison was `diverged` (ahead 8 / behind 42). A fresh Exact-Head review is required after this commit.
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
- v2.2 之前的 current-main 比较结果为 `diverged`（ahead 8 / behind 42）。本次提交后仍须重新进行 Exact-Head 复核。
- 不修改 D2。v1.1 继续为 NORMATIVE；v1.2 继续为 DRAFT。 `MIGRATION_DEBT != EXEMPTION`。
- `Approval: NOT_RECORDED`；`Adoption: NOT_ADOPTED`。本报告不授权 PR 合并，也不表示 Owner 已批准、规范已采纳或历史迁移已完成。
- 本 v2.2 更正等待新一轮独立复审，不得自我批准。

R5D2-OK
