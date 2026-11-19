# Bilingual Governance Migration Register / 双语治理迁移登记表

- Register ID: GOV-DOC-001-MIGRATION
- Policy ID: GOV-DOC-001
- Register Version: 1.0
- Status: DRAFT — PENDING GOVERNANCE APPROVAL
- Baseline Policy: GOV-DOC-001 v1.1
- Proposed Policy: GOV-DOC-001 v1.2
- Accountable Governance Owner: NOT_ASSIGNED
- Last Inventory Revision: NOT_RECORDED

## 1. Purpose / 目的

EN:

This register tracks historical bilingual-governance debt and its remediation. It does not authorize historical rewriting, state changes, or exceptions.

CN:

本登记表用于跟踪历史双语治理技术债及其修复。它不授权历史重写、状态变更或豁免。

## 2. Migration classifications / 迁移分类

| Classification | Meaning | 中文说明 |
|---|---|---|
| MIGRATION_DEBT | Historical item requires bilingual migration | 历史项目需要双语迁移 |
| INVENTORY_REQUIRED | Inventory has not been completed | 尚未完成清点 |
| NOT_STARTED | Migration has not begun | 尚未开始迁移 |
| IN_PROGRESS | Authorized migration is underway | 已授权迁移正在进行 |
| PENDING_REVIEW | Migration awaits independent review | 等待独立审查 |
| COMPLETED | Migration evidence and parity review exist | 迁移证据和一致性审查均已完成 |
| EXEMPTION | Formally authorized, time-bounded exception | 正式授权且有期限的例外 |
| STALE | Counterpart is known to be outdated | 对应版本已知过期 |

MIGRATION_DEBT is not EXEMPTION.

迁移技术债不等于正式豁免。

## 3. Required record fields / 必需字段

Every record MUST contain:

| Field | Description |
|---|---|
| Object_Type | Issue / Umbrella Requirement / Commit / PR / Document |
| Object_ID | Stable object identifier |
| Original_Language_State | EN_ONLY / ZH_ONLY / BILINGUAL / UNKNOWN |
| Migration_Status | Canonical migration classification |
| Historical_Reason | Verified reason or NOT_RECORDED |
| Authorized_Exception | Authorization reference or NOT_RECORDED |
| Accountable_Owner | Named Owner or NOT_ASSIGNED |
| Tracking_Work_Item | Work Item ID or NOT_RECORDED |
| Completion_Evidence | Exact evidence or NOT_RECORDED |

每项记录 MUST 使用以上字段。未知信息不得推断。

## 4. Known historical Issue inventory / 已知历史 Issue 清单

### 4.1 Umbrella Requirements / 大需求

| Object_Type | Object_ID | Original_Language_State | Migration_Status | Accountable_Owner | Tracking_Work_Item |
|---|---|---|---|---|---|
| Umbrella Requirement | #262 / REQ-01 | ZH_ORIGINAL_WITH_EN_REGISTRATION | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |
| Umbrella Requirement | #263 / REQ-02 | ZH_ORIGINAL_WITH_EN_REGISTRATION | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |
| Umbrella Requirement | #264 / REQ-03 | ZH_ORIGINAL_WITH_EN_REGISTRATION | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |
| Umbrella Requirement | #265 / REQ-04 | ZH_ORIGINAL_WITH_EN_REGISTRATION | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |
| Umbrella Requirement | #266 / REQ-05 | ZH_ORIGINAL_WITH_EN_REGISTRATION | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |

Historical reason: These Issues were registered before the proposed expansion of GOV-DOC-001 to all Umbrella Requirements.

历史原因：这些 Issue 在 GOV-DOC-001 扩展至所有 Umbrella Requirement 之前完成登记。

Important:

- All five Issues remain OPEN.
- All five Requirement Status values remain RECORDED.
- The bilingual bodies are proposed migration deliverables.
- No Owner decision is implied.
- Original quotations and identifiers must remain unchanged.
- Historical source conversation gaps remain NOT_RECORDED.

重要说明：

- 五个 Issue 均保持 OPEN。
- 五个 Requirement Status 均保持 RECORDED。
- 双语正文属于拟议迁移交付物。
- 不代表任何 Owner 已作出决议。
- 原始引文和标识必须保持不变。
- 历史来源对话缺失部分继续保持 NOT_RECORDED。

### 4.2 Historical single-language Issues / 历史单语 Issue

EN:

The complete historical Issue inventory has not yet been performed.

All historical Issues created before formal adoption of the expanded policy MUST be inventoried by exact Issue number, original title/body language, creation date, state, and source evidence.

Do not infer that all Issues are single-language or bilingual from a partial sample.

CN:

历史 Issue 的完整清点尚未完成。

扩展规范正式采纳前创建的全部历史 Issue MUST 按准确 Issue 编号、原始标题/正文语言、创建日期、状态和来源证据进行清点。

不得根据部分样本推断全部 Issue 均为单语或双语。

Current status: INVENTORY_REQUIRED.

### 4.3 Historical single-language Commits / 历史单语 Commit

EN:

Historical Commit Message inventory is NOT COMPLETE.

All historical commits MUST be examined without rewriting their objects.

The inventory MUST identify:

- Commit SHA.
- Original Subject language.
- Original Body language.
- Commit author date.
- Whether a migration annotation is required.
- Tracking Work Item.
- Completion evidence.

CN:

历史 Commit Message 清点尚未完成。

所有历史 Commit MUST 在不重写其对象的前提下接受检查。

清点必须识别：

- Commit SHA。
- 原始 Subject 语言。
- 原始 Body 语言。
- Commit 作者日期。
- 是否需要迁移说明。
- 跟踪 Work Item。
- 完成证据。

Current status: INVENTORY_REQUIRED.

No historical Commit is rewritten or force-pushed.

不重写任何历史 Commit，不执行 force-push。

### 4.4 Historical Pull Requests / 历史 PR

EN:

Historical PR title/body inventory remains INVENTORY_REQUIRED.

Existing PR state, review history, merge decisions, and exact-head evidence MUST be preserved.

CN:

历史 PR 标题和正文清点仍为 INVENTORY_REQUIRED。

现有 PR 状态、审查历史、合并决议和 Exact-Head 证据 MUST 保持不变。

## 5. Exemption register / 豁免登记

No formally authorized exemption is established by this register.

本登记表没有建立任何正式授权的豁免。

| Object_ID | Exception Authority | Decision Date | Expiry | Evidence |
|---|---|---|---|---|
| NONE_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED |

An unassigned Owner, incomplete inventory, or missing source is not an exemption.

Owner 未分配、清点不完整或来源缺失都不构成豁免。

## 6. Migration workflow / 迁移流程

1. Inventory the historical object.
2. Preserve original source and stable identifiers.
3. Determine original language state.
4. Create a bilingual counterpart without changing the original.
5. Translate original quotations accurately.
6. Preserve status, authority, and evidence.
7. Record missing information as NOT_RECORDED.
8. Perform identifier and semantic parity checks.
9. Obtain independent review.
10. Record completion evidence.

中文：

1. 清点历史对象。
2. 保留原始来源和稳定标识。
3. 确定原始语言状态。
4. 创建双语对应版本，不修改原件。
5. 准确翻译原始引文。
6. 保留状态、权限和证据。
7. 将缺失信息登记为 NOT_RECORDED。
8. 执行标识和语义一致性检查。
9. 取得独立审查。
10. 登记完成证据。

## 7. Current disposition / 当前处置

- Five Umbrella Requirements: migration drafts prepared; independent review pending.
- Historical single-language Issues: INVENTORY_REQUIRED.
- Historical single-language Commits: INVENTORY_REQUIRED.
- Historical PRs: INVENTORY_REQUIRED.
- Formal EXEMPTION: NONE_RECORDED.
- Migration completion: NOT_CONFIRMED.

五个大需求：已形成迁移草案，独立审查待完成。

历史单语 Issue：INVENTORY_REQUIRED。

历史单语 Commit：INVENTORY_REQUIRED。

历史 PR：INVENTORY_REQUIRED。

正式 EXEMPTION：NONE_RECORDED。

迁移完成：NOT_CONFIRMED.
