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

- T2 submission-time main HEAD: c5a995d9a2808112b007a9108e085048cbed5cc9
- Current main HEAD: 2ca77db4c66529394304f0e1e51ba4696544cfb6
- Current main HEAD verification: Direct GitHub branch-ref read
- Remediation branch: remediation/gov-doc-001-v1.2-bilingual-baseline
- Remediation branch HEAD: a77219fa2834af0c4535e6692029adaec2e62638
- PR: #271
- PR state: OPEN
- PR merged: false
- PR base SHA reported by GitHub: c5a995d9a2808112b007a9108e085048cbed5cc9

The current main HEAD was directly retrieved from the GitHub refs API during T9.

当前 main HEAD 已在 T9 期间通过 GitHub refs API 直接读取。

The PR base SHA differs from the current main HEAD. A fresh Exact-Head comparison is required before any integration decision.

PR base SHA 与当前 main HEAD 不同。任何集成决策前必须重新进行 Exact-Head 比较。

## 3. Seven-file submission and read-back / 七文件提交与读回

### 3.1 Commit evidence / Commit 证据

- Commit SHA: a77219fa2834af0c4535e6692029adaec2e62638
- Tree SHA: b11d70b27ef63c5c6af64a5bbc537bec8ab70bd9
- Parent SHA: c5a995d9a2808112b007a9108e085048cbed5cc9
- Author: oahcom
- Committer: oahcom
- Commit timestamp: 2026-11-19T07:07:18Z
- Changed files: 7
- Additions: 1597
- Deletions: 50
- Signature verification: unsigned
- PR: #271

Commit Subject:

docs(governance): expand bilingual governance baseline / 扩展双语治理基线

### 3.2 Exact file manifest / 精确文件清单

| ID | Repository path | Blob SHA | Bytes |
|---|---|---|---:|
| D1 | 00-governance/bilingual-documentation-policy.md | 66517d39dfeae459fef5cedf9d5a79de08faf08d | 33611 |
| D2 | 00-governance/bilingual-governance-migration-register.md | 9282ebf35415319b1be64d463b221ed0b54685bc | 7936 |
| D3 | 00-governance/templates/bilingual-issue-template.md | 64d432395dc7bec9ba5c3b2ae534df4b01a2db3c | 2730 |
| D4 | 00-governance/templates/bilingual-umbrella-requirement-template.md | 9265098d739369522000ebc54b8c0275ee7e5b6d | 2900 |
| D5 | 00-governance/templates/bilingual-commit-message.md | 8ea68efd927c62ba48c3249cc39e62760ced9370 | 2340 |
| D6 | 00-governance/templates/repository-policy-inheritance.md | 07683720cbd43cb60b53edb9ab9bb6de3e6f5a71 | 3382 |
| D7 | 00-governance/reports/bilingual-baseline-remediation-report.md | c9eff04b498ed0ceb7b9c581205c2426d6a245f5 | 5506 |

### 3.3 Verification result / 验证结果

All seven files were fetched from the remediation branch during T9.

All seven returned Blob SHAs match the T2/T3 manifest.

T9 重新从修复分支读取全部七个文件。

七个文件返回的 Blob SHA 均与 T2/T3 manifest 一致。

Result: 7/7 read-back verified.

Important: This verification applies to the committed D7 Version 1.0 content. This Version 2.0 report is a proposed replacement and has not yet been committed.

重要：以上验证针对已经提交的 D7 Version 1.0。本 Version 2.0 报告属于拟议替换内容，尚未提交。

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

The independent validator, its declaration, and the associated tests have been committed as `d568325b`.

The tests were subsequently corrected in accordance with the existing review ruling. The correction commit is `e6ff2746`, and the corresponding test-file blob is `4ca1f8a2`. The corrected test suite reports **6/6 PASS**.

**Current status: PARTIAL.**

The following requirements remain outstanding:

1. Integrate the independent validator into the CI workflow.
2. Provide evidence that the required check is configured and enforced.

Until both requirements have been implemented and verified, F-02 must not be marked COMPLETE. A local test pass does not establish that a CI required check is active or enforced.

**中文**

#### F-02 — 独立校验器与 CI 接入状态

独立校验器、配套声明及相关测试已提交入库，提交为 `d568325b`。

测试随后依据既有审查裁决完成修复。修复提交为 `e6ff2746`，对应测试文件 blob 为 `4ca1f8a2`。修复后的测试结果为 **6/6 PASS**。

**当前状态：PARTIAL（部分完成）。**

以下要求仍未完成：

1. 将独立校验器接入 CI workflow。
2. 提供 required check 已配置并实际强制生效的证据。

在上述两项要求均完成并经过验证前，不得将 F-02 标记为 COMPLETE。本地测试通过不能证明 CI required check 已启用或已实际执行强制检查。

---

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

The independent validator and its tests are present in the repository. The corrected local test result is **6/6 PASS**, based on test-file blob `4ca1f8a2`, introduced by correction commit `e6ff2746`.

This result is local test evidence only. The independent validator has not yet been verified as integrated into the CI workflow, and no evidence has been established here that a corresponding required check is configured and enforced.

**Status: PARTIAL.** Do not report F-02 CI integration or required-check enforcement as complete.

**中文**

#### F-02 CI 验证结果

独立校验器及其测试已进入仓库。依据修复提交 `e6ff2746` 引入的测试文件 blob `4ca1f8a2`，修复后的本地测试结果为 **6/6 PASS**。

该结果仅属于本地测试证据。目前尚未验证独立校验器已接入 CI workflow，也没有证据证明对应的 required check 已完成配置并实际强制生效。

**状态：PARTIAL（部分完成）。**不得将 F-02 的 CI 接入或 required check 强制执行表述为已完成。

---

### 7.2 Actual gate behavior / 门禁实际行为

**EN**

#### F-02 Gate Behavior — Verification Boundary

The 6/6 PASS result establishes only that the corrected local test suite passed.

It does not establish any of the following:

- The validator is invoked by the CI workflow.
- The validator's result is exposed as a CI check.
- The check is configured as a required check.
- The check blocks a pull request when validation fails.

These behaviors remain unverified until supported by actual workflow and repository branch-protection evidence.

**中文**

#### F-02 门禁行为——验证边界

6/6 PASS 仅证明修复后的本地测试套件通过。

该结果不能证明以下事项：

- CI workflow 已调用该校验器；
- 校验结果已作为 CI check 提供；
- 该 check 已配置为 required check；
- 校验失败时该 check 会阻止 Pull Request 合并。

在取得实际 workflow 及仓库分支保护配置证据之前，上述门禁行为均应标记为未验证。

---

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

仅替换本节中涉及 F-02、F-06、F-07、规范效力、Owner 批准、豁免及迁移完成状态的对应矩阵行；保留其他验收项目及其原有内容。

**EN — Replacement rows**

| Item | Current status | Acceptance boundary |
|---|---|---|
| F-02 | PARTIAL | Validator and tests committed; corrected local tests 6/6 PASS. CI workflow integration and required-check enforcement evidence remain outstanding. |
| F-06 Issue inventory | Inventory finalized | 39 records: 28 EN_ONLY, 10 EN_ZH_MIXED, 1 ZH_ORIGINAL_WITH_EN_TERMS (#254, HOLD). Each record requires a matching body_sha256. |
| F-06 Commit inventory | Inventory finalized | 313 records: 312 EN_ONLY, 1 MIXED (C168). Each record requires matching sha and msg_sha256; classification is based on the complete commit message. |
| F-07 | Correction recorded | PR comment `7006445553`; authoritative D1 blob `66517d39`. |
| Normative status | Unchanged | v1.1 NORMATIVE; v1.2 DRAFT. |
| Migration and exemption | Not interchangeable | MIGRATION_DEBT != EXEMPTION. Registration does not establish migration completion. |

**中文 — 替换行**

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

仅更新本节中与 F-02、F-06、F-07、规范效力及迁移状态有关的条目；其他阻塞事项保持原文。

**EN — Replacement entries**

- **F-02:** Complete CI workflow integration and provide evidence that the required check is configured and enforced. Until then, retain PARTIAL.
- **F-06:** Preserve the finalized 39-Issue and 313-Commit inventories. Verify record uniqueness, object identity, classification totals, and all required content anchors. Keep Issue #254 within the 39-record set and on HOLD until its explicit exit conditions are satisfied.
- **F-07:** Use D1 authoritative blob `66517d39`; retain PR comment `7006445553` as the correction traceability record.
- **Normative and migration protection:** Maintain v1.1 as NORMATIVE and v1.2 as DRAFT. Do not treat migration debt as an exemption or infer Owner approval, normative adoption, PR merge authorization, or migration completion.

**中文 — 替换条目**

- **F-02：**完成 CI workflow 接入，并提供 required check 已配置且实际强制生效的证据。在此之前维持 PARTIAL。
- **F-06：**保留已定稿的 39 条 Issue 和 313 条 Commit 清单。核验记录唯一性、对象身份、分类总数及全部必需内容锚点。Issue #254 必须继续包含在 39 条集合内，并在明确退出条件满足前保持 HOLD。
- **F-07：**使用 D1 权威 blob `66517d39`；保留 PR 评论 `7006445553` 作为更正追踪记录。
- **规范与迁移保护：**维持 v1.1 为 NORMATIVE、v1.2 为 DRAFT。不得将迁移债务视为豁免，也不得推定 Owner 批准、规范采纳、PR 合并授权或迁移完成。

---

### P1

F-02:

Implement and demonstrate executable repository inheritance enforcement.

### P2

F-06:

Complete the historical object inventory, resolve the 14 ungrouped PRs, and verify the full Commit history.

F-07:

Record the authoritative D1 Blob SHA correction with historical traceability.

### CI blocker

Update scripts/check_bilingual_docs.py using the exact allowlist replacement in Section 7.

Update PR #271 with BILINGUAL-MANIFEST: COMPLETE.

Rerun the workflow and retain the actual result.

### Other required actions

1. Incorporate the T6/T7 D2 incremental appendix.
2. Reconcile D2 with the 14 ungrouped PRs.
3. Obtain independent re-review of the corrected artifacts.
4. Revalidate Exact-Head against current main.
5. Obtain explicit authorized governance approval.
6. Only after approval, evaluate policy adoption and effective date.

No automatic approval or adoption is permitted.

## 10. Governance stage ledger / 治理阶段登记

仅替换本节中涉及 F-02、F-06、F-07、规范效力及迁移完成状态的登记项；保留其他阶段记录、历史时间线和无关状态。

**EN — Replacement entries**

| Governance item | Recorded state | Limitation |
|---|---|---|
| F-02 | PARTIAL | Local tests pass 6/6; CI integration and required-check enforcement remain unverified. |
| F-06 Issue inventory | Finalized | 39 records, including #254 on HOLD; registration does not establish migration completion. |
| F-06 Commit inventory | Finalized | 313 records with sha and msg_sha256 anchors; classification is based on substantive complete-message content. |
| F-07 | Correction recorded | PR comment `7006445553`; authoritative D1 blob `66517d39`. |
| Normative status | Unchanged | v1.1 NORMATIVE; v1.2 DRAFT. |
| Migration status | Not inferred | MIGRATION_DEBT != EXEMPTION; no migration completion is inferred from registration. |

**中文 — 替换条目**

| 治理事项 | 登记状态 | 限制 |
|---|---|---|
| F-02 | PARTIAL | 本地测试 6/6 PASS；CI 接入及 required check 强制生效仍未验证。 |
| F-06 Issue 清单 | 已定稿 | 39 条记录，包含处于 HOLD 的 #254；登记完成不代表迁移完成。 |
| F-06 Commit 清单 | 已定稿 | 313 条记录具有 sha 和 msg_sha256 锚点；分类依据完整提交消息的实质内容判定。 |
| F-07 | 更正已登记 | PR 评论 `7006445553`；D1 权威 blob `66517d39`。 |
| 规范状态 | 不变 | v1.1 为 NORMATIVE；v1.2 为 DRAFT。 |
| 迁移状态 | 不作推定 | MIGRATION_DEBT != EXEMPTION；不得根据登记完成推定迁移完成。 |

---

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

R5D2-OK
