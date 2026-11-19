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

: 00-governance/bilingual-governance-migration-register.md :: APPEND SECTION 8 -->

## 8. T6/T7 Historical Inventory and Migration Classification / 历史清点与迁移分类

### 8.1 Inventory revision / 清点修订

- Work Item: GOV-DOC-001-V1.2-REMEDIATION
- Policy: GOV-DOC-001 v1.2 (proposed)
- Inventory Revision: T6-T7-2026-11-18
- Inventory Evidence Source: Coordinator-provided T6-INVENTORY-DATA.json
- Branch: remediation/gov-doc-001-v1.2-bilingual-baseline
- Baseline Commit: a77219fa2834af0c4535e6692029adaec2e62638
- Register Status: DRAFT — PENDING GOVERNANCE APPROVAL

EN:

This revision records the results of the T6 historical inventory and T7 migration classification.

It does not authorize historical rewriting, Issue or PR state changes, Owner decisions, or exceptions.

CN:

本修订记录 T6 历史清点和 T7 迁移分类结果。

本修订不授权历史对象重写、Issue 或 PR 状态变更、Owner 决策或豁免。

### 8.2 Historical Issues / 历史 Issue

EN:

The supplied inventory covers all 39 Issues in the repository.

Thirty-three Issues have English-only titles, verified by the supplied title inventory.

The title-language result does not establish that the complete Issue body is English-only.

Therefore:

- Object_Type: Issue
- Original_Language_State: UNKNOWN
- Migration_Status: MIGRATION_DEBT
- Historical_Reason: English-only title verified; full body language not independently inspected.
- Authorized_Exception: NOT_RECORDED
- Accountable_Owner: NOT_ASSIGNED
- Tracking_Work_Item: GOV-DOC-001-V1.2-REMEDIATION
- Completion_Evidence: Coordinator-provided T6-INVENTORY-DATA.json, including exact Issue number, title, state and creation timestamp.

CN:

本次提供的清单覆盖仓库全部 39 个 Issue。

其中 33 个 Issue 的英文单语标题已经通过所提供的标题清单确认。

标题语言的核验不能证明完整 Issue 正文也是英文单语。

因此：

- Object_Type：Issue
- Original_Language_State：UNKNOWN
- Migration_Status：MIGRATION_DEBT
- Historical_Reason：已确认英文单语标题；完整正文语言尚未独立核验。
- Authorized_Exception：NOT_RECORDED
- Accountable_Owner：NOT_ASSIGNED
- Tracking_Work_Item：GOV-DOC-001-V1.2-REMEDIATION
- Completion_Evidence：协调方提供的 T6-INVENTORY-DATA.json，包含准确 Issue 编号、标题、状态和创建时间。

#### 8.2.1 Individual Issue records / Issue 逐项登记

All records below inherit the common fields in §8.2.

以下各记录使用 §8.2 所列的共同字段。

| Object_ID | Original title | State | Created (UTC) | Migration_Status |
|---|---|---|---|---|
| #268 | FIX-2026-P1-T1 — Simplify prompt engineering from 15 to 7 core elements | CLOSED | 2026-11-19T05:01:40Z | MIGRATION_DEBT |
| #218 | AI-EXEC-001/002 adoption & rollout: AI development execution rules (AID-2026-002) | CLOSED | 2026-11-18T06:57:27Z | MIGRATION_DEBT |
| #200 | Phase 1 domain implementation drift: align Rust types with frozen DOMAIN-MODEL-001 | CLOSED | 2026-11-18T06:51:16Z | MIGRATION_DEBT |
| #134 | P0 — Enforce main merge gates; remediate PR #129 failed-check merge | OPEN | 2026-11-17T21:53:19Z | MIGRATION_DEBT |
| #130 | PR-GOVERNANCE-001 — Mandatory AI Session Delivery Traceability to PRs and Issues | OPEN | 2026-11-17T21:43:23Z | MIGRATION_DEBT |
| #43 | ARCH-CONSOL-001: System-wide Architecture Consolidation & Feasibility Review | OPEN | 2026-11-17T09:52:18Z | MIGRATION_DEBT |
| #41 | AID-2026-001: Define the ChatGPT-native AI development execution model | OPEN | 2026-11-17T09:27:45Z | MIGRATION_DEBT |
| #39 | POC: Verify ChatGPT-authenticated Codex CLI on the Ubuntu self-hosted runner | CLOSED | 2026-11-17T09:14:58Z | MIGRATION_DEBT |
| #37 | AI-IMPL-001: Implement the first executable GitHub-driven Owner Worker | OPEN | 2026-11-17T08:58:19Z | MIGRATION_DEBT |
| #30 | AI-RUN-003: Design and pilot the event-driven Owner Worker Runtime | OPEN | 2026-11-17T08:01:28Z | MIGRATION_DEBT |
| #29 | Phase 3.8.2 — HRC executable validation, bidirectional RecoveryJoin & topology proof | OPEN | 2026-11-17T07:30:07Z | MIGRATION_DEBT |
| #26 | [AI-RUN-002] Deploy persistent Ubuntu self-hosted worker runtime | OPEN | 2026-11-17T06:51:56Z | MIGRATION_DEBT |
| #25 | Phase 3.8 — D/E/I/Storage atomic producer admission and derivative visibility gate | OPEN | 2026-11-17T06:28:21Z | MIGRATION_DEBT |
| #24 | AID-2026-001 extension: GitHub-mediated Owner workflow and scheduled automation | OPEN | 2026-11-17T06:18:07Z | MIGRATION_DEBT |
| #21 | Phase 3.7 — F/E/G local lifecycle contracts and cross-owner reconciliation | OPEN | 2026-11-17T05:43:58Z | MIGRATION_DEBT |
| #20 | Archive Producer Classification × Forget Fence × Inventory × Restore Atomicity — exact Owner review | OPEN | 2026-11-17T05:33:34Z | MIGRATION_DEBT |
| #19 | Phase 3.6 — Storage COC protocol v3.1 fresh exact-version cross-owner review | CLOSED | 2026-11-17T05:33:05Z | MIGRATION_DEBT |
| #18 | Phase 3.6 — Fresh exact-version Owner review of Storage COC protocol v3 | CLOSED | 2026-11-16T21:49:41Z | MIGRATION_DEBT |
| #17 | Phase 3.6.3 — A/I/H exact review: Prepared GID, JF-10 bridge & signed wire envelope | CLOSED | 2026-11-16T21:40:33Z | MIGRATION_DEBT |
| #16 | Phase 3.6 — Storage COC protocol v2 fresh exact-version review (A/I/D/C/H) | CLOSED | 2026-11-16T21:38:42Z | MIGRATION_DEBT |
| #15 | Phase 3.6.3 — priority exact-Blob review: PreparedTransactionGID, PreparedParticipantReceipt & signature boundary | CLOSED | 2026-11-16T21:34:31Z | MIGRATION_DEBT |
| #14 | Phase 3.6 exact-version review: COC persistence, Recovery Cutoff Batch, Owner-local Gate & JF-10 same-XID bridge | OPEN | 2026-11-16T21:25:23Z | MIGRATION_DEBT |
| #13 | Phase 3.6: exact-version cross-owner review — COC durable log, Recovery Cutoff Batch, Owner-local Gates & JF-10 same-XID bridge | CLOSED | 2026-11-16T21:22:48Z | MIGRATION_DEBT |
| #11 | A–I Owner submissions: Module Baseline & Redlines rollout | OPEN | 2026-11-16T16:16:12Z | MIGRATION_DEBT |
| #10 | JF-10 P0: prove database prepared-XID capability, persistent COC and fault recovery | OPEN | 2026-11-16T16:12:28Z | MIGRATION_DEBT |
| #9 | JF-10 ↔ COC: D and Storage exact acceptance of complete pinned decision bundle | CLOSED | 2026-11-16T16:11:46Z | MIGRATION_DEBT |
| #8 | Phase 3.6 joint Owner decision: C / D / Storage acceptance of I-approved JF-10 ↔ COC bridge | CLOSED | 2026-11-16T15:32:05Z | MIGRATION_DEBT |
| #7 | [Engineering-phase handoff] Designate canonical runtime repository, engineering owners and implementation entry plan | OPEN | 2026-11-16T14:35:29Z | MIGRATION_DEBT |
| #6 | [BIH Consumers] Obtain explicit C/F/G acceptance of BIH36-JD-01..17 | CLOSED | 2026-11-16T14:14:52Z | MIGRATION_DEBT |
| #5 | [BIH / I Owner] Obtain formal Phase 3.6 identity-trust governance approvals I36-GOV-01..10 | OPEN | 2026-11-16T14:14:49Z | MIGRATION_DEBT |
| #4 | [I Owner] Phase 3.6 DE-S external dependency decisions: inventory, authorization and Global Forget completion | OPEN | 2026-11-16T13:17:34Z | MIGRATION_DEBT |
| #3 | Phase 3.6: C/G/H Applied Evidence & BMCP Wire Contract — explicit owner freeze decision | OPEN | 2026-11-16T13:09:05Z | MIGRATION_DEBT |
| #2 | Phase 3.6 joint decision required: D/E/Storage fence-enforced compiler publication | OPEN | 2026-11-16T12:29:39Z | MIGRATION_DEBT |

#### 8.2.2 Preservation requirements / 状态保持

- Original Issue titles and bodies MUST NOT be overwritten merely to erase historical evidence.
- Existing OPEN/CLOSED states MUST remain unchanged.
- Historical creation timestamps MUST remain unchanged.
- Original quotations and stable identifiers MUST remain unchanged.
- Missing source conversations MUST remain NOT_RECORDED.

中文：

- 不得仅为消除历史证据而覆盖原始 Issue 标题或正文。
- 原有 OPEN/CLOSED 状态 MUST 保持。
- 历史创建时间 MUST 保持。
- 原始引文和稳定标识 MUST 保持。
- 缺失的来源对话 MUST 继续登记为 NOT_RECORDED。

### 8.3 Historical Commits / 历史 Commit

EN:

The latest 100 commits were sampled. All 100 sampled commit messages were reported as single-language.

This is a sample, not a complete historical commit inventory.

The available SHA evidence is partial. Therefore, this register uses topic-based groups rather than inventing missing SHA values.

Groups:

| C-01 | Governance / AI execution / bilingual policy | `c33a1bcd36f7`, `5ab18f57f350`, `1957faa63496`, `ef00db086d9c`, `7524a3dbba46`, `38ee99bc210c`, `a7d64175bb9f`, `1f97c3fae658`, `f0f5149dccbc`, `0f05c41b2fd6`, `3cc5419b339c`, `612c4b2d4d7e`, `778b4d3b4b6c` | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |
| C-02 | i18n / AI-EXEC bilingual counterpart rollout | `21e84c5fdfcf`, `8d9ee71c5e6c`, `e2fa44b1437a`, `6059067d1aed`, `9eb59ceacf75`, `3fbabe744a27`, `26fa557c5598`, `685622181144`, `6275265e0826`, `e683ea275dfa`, `08b07d228dbe`, `e0e20ed30b4a`, `0d2857a0fd02` | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |
| C-03 | Phase 1 Rust / SQLite / Storage / Event Store | `9b67fb1b0550`, `b663c8fde45d`, `6b5db2918cff`, `fcdecf0a4e63`, `fb9b25cec077`, `4a3e06fd263e`, `aa7112897853`, `715878ef3f5c`, `6691bfba44cb`, `bcfa0f4cb307`, `99a79fce7276` | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |
| C-04 | Architecture / integration / acceptance | `cd6efa2ba2ea`, `c3bf7e47b512`, `cd3f5d719100`, `2df5517a5813`, `3e8577acc3c6`, `5c751f1febe7`, `ed842fa7ce9d`, `5ce8657d402b`, `dfd4fdce0be0`, `b2960d375911` | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |
| C-05 | Exact-head remediation / terminal review | `2ca77db4c665`, `c5a995d9a280` | MIGRATION_DEBT | NOT_ASSIGNED | GOV-DOC-001-V1.2-REMEDIATION |

Common fields:

- Object_Type: Commit
- Original_Language_State: UNKNOWN for individual Subject/Body language until individually verified; sample-level result is EN-only.
- Historical_Reason: Single-language commit messages reported in the latest-100 sample.
- Authorized_Exception: NOT_RECORDED
- Accountable_Owner: NOT_ASSIGNED
- Tracking_Work_Item: GOV-DOC-001-V1.2-REMEDIATION
- Completion_Evidence: Coordinator-provided sample statement and available SHA references.

CN:

最近 100 条 Commit 已完成抽样，抽样中的 100 条 Commit Message 均被报告为单语。

这属于抽样结果，不代表全部历史 Commit 已完成清点。

当前可用 SHA 证据不完整，因此采用主题归组登记，不补造缺失 SHA。

各组必须保留原始 Commit 对象，不得 rebase、amend、重写或 force-push。

#### 8.3.1 Commit migration strategy / Commit 迁移策略

1. Preserve original Commit SHA and metadata.
2. Do not rewrite historical Commit objects.
3. Group records by integration topic.
4. Associate future bilingual documentation with the relevant original SHA.
5. Record exact SHA, author date, Subject language and Body language when available.
6. Mark unavailable evidence NOT_RECORDED.
7. Do not claim COMPLETED without migration and parity evidence.

中文：

1. 保留原始 Commit SHA 和元数据。
2. 不重写历史 Commit 对象。
3. 按集成主题归组登记。
4. 将未来双语文档关联到对应原始 SHA。
5. 获得证据后记录准确 SHA、作者日期、Subject 语言和 Body 语言。
6. 无法取得的信息登记为 NOT_RECORDED。
7. 没有迁移及一致性证据时不得标记 COMPLETED。

### 8.4 Historical Pull Requests / 历史 PR

EN:

The repository has 232 Pull Requests.

The supplied single-language PR inventory is classified by integration unit.

Each PR remains an independent historical object, even when grouped with other PRs.

| Group | Integration Unit | PR numbers | Migration_Status | Accountable_Owner |
|---|---|---|---|---|
| P-01 | AI governance / AI execution / policy adoption | #270, #269, #267, #261, #260, #256, #250, #248, #237, #230, #201, #199, #196, #195 | MIGRATION_DEBT | NOT_ASSIGNED |
| P-02 | AI execution traceability / bilingual governance / recovery records | #158, #157, #156, #155, #150, #149, #148, #147, #146, #145, #144, #142, #140, #138, #137, #136, #135, #133, #132 | MIGRATION_DEBT | NOT_ASSIGNED |
| P-03 | Phase 1 Rust / Storage / SQLite / Event Store | #249, #247, #246, #245, #244, #243, #242, #241, #240, #239, #238, #236, #235, #234, #233, #232, #231, #229, #228, #227, #226, #225, #224, #223, #222, #221, #220, #219, #217, #216, #215, #214, #213, #212, #211, #210, #209, #208, #206, #205, #204, #203, #202, #198, **#191** | MIGRATION_DEBT | NOT_ASSIGNED |
| P-04 | Publication / Forget / authorization / recovery | #187–#174, #173–#160, #159, #153, #152, #151, **#207, #141** | MIGRATION_DEBT | NOT_ASSIGNED |
| P-05 | Architecture / domain / integration / research | #257, #255, #253, #252, #251, #197, #194, #193, #192, #190, #189, #188, #154, #143, #139, #131, #129–#121, #120–#114, #113–#99, #98–#89, #88–#80, #79–#71, #70–#60, #59–#52, #51, #50, #49, #47, #46, #45, #44, #42, #40, #38, #36, #35, #34, #33, #32, #31, #28, #27, #23, #22, #12, #1 | MIGRATION_DEBT | NOT_ASSIGNED |
| P-06 | Event Store payload / Global Forget inventory hardening | #259, #258 | MIGRATION_DEBT | NOT_ASSIGNED |

CN:

仓库共有 232 个 Pull Request。

本次提供的单语 PR 清单按集成单元进行分类。

即使多个 PR 被归入同一组，每个 PR 仍然是独立的历史对象。

#### 8.4.1 PR migration strategy / PR 迁移策略

- Preserve original PR number.
- Preserve original title and body as historical evidence.
- Preserve OPEN/CLOSED and merged status.
- Preserve review history and merge decisions.
- Preserve exact-head evidence.
- Create bilingual companion records without replacing historical review records.
- Do not infer body-language parity from title-language inspection.

中文：

- 保留原始 PR 编号。
- 保留原始标题和正文作为历史证据。
- 保留 OPEN/CLOSED 和合并状态。
- 保留审查历史和合并决议。
- 保留 Exact-Head 证据。
- 创建双语对应记录，不替换历史审查记录。
- 不得根据标题语言核验推断正文语言一致性。

### 8.5 Migration classification / 迁移分类

EN:

The following classifications apply to the current evidence:

| Object | Current Classification | Reason |
|---|---|---|
| Umbrella Requirements #262–#266 | MIGRATION_DEBT | Existing D2 registration establishes the migration requirement |
| 33 single-language Issue titles | MIGRATION_DEBT | English-only titles verified |
| Commit groups C-01–C-05 | MIGRATION_DEBT | Latest-100 sample reports single-language messages |
| PR groups P-01–P-06 | MIGRATION_DEBT | Supplied single-language PR inventory |
| Formal exemptions | NONE_RECORDED | No independent authorization evidence |

CN:

当前证据对应的分类如下：

| 对象 | 当前分类 | 原因 |
|---|---|---|
| Umbrella Requirement #262–#266 | MIGRATION_DEBT | D2 已建立迁移义务 |
| 33 个单语标题 Issue | MIGRATION_DEBT | 已确认英文单语标题 |
| Commit 分组 C-01–C-05 | MIGRATION_DEBT | 最近 100 条抽样报告为单语 |
| PR 分组 P-01–P-06 | MIGRATION_DEBT | 提供的单语 PR 清单 |
| 正式豁免 | NONE_RECORDED | 没有独立授权证据 |

IN_PROGRESS, PENDING_REVIEW and COMPLETED are not asserted merely because this inventory has been produced.

本次完成清点并不代表迁移已经开始、正在等待独立审查或已经完成。因此不得仅凭本次清点将项目标记为 IN_PROGRESS、PENDING_REVIEW 或 COMPLETED。

### 8.6 Record ownership and evidence / 责任与证据

All newly inventoried historical records:

- Accountable_Owner: NOT_ASSIGNED
- Tracking_Work_Item: GOV-DOC-001-V1.2-REMEDIATION
- Authorized_Exception: NOT_RECORDED
- Completion_Evidence: NOT_RECORDED until actual migration and independent parity review are completed.

所有新增历史登记记录：

- Accountable_Owner：NOT_ASSIGNED
- Tracking_Work_Item：GOV-DOC-001-V1.2-REMEDIATION
- Authorized_Exception：NOT_RECORDED
- Completion_Evidence：在实际迁移和独立一致性审查完成前保持 NOT_RECORDED。

The inventory source is evidence of classification input, not evidence of migration completion.

清点来源只证明分类输入，不证明迁移已经完成。

### 8.7 Exemption ruling / 豁免裁定

No new EXEMPTION is created.

No formal exception authority, decision date, expiry date or supporting evidence was supplied.

| Object_ID | Exception Authority | Decision Date | Expiry | Evidence |
|---|---|---|---|---|
| NONE_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED |

An unassigned Owner, missing source, incomplete inventory or closed Issue/PR is not an exemption.

Owner 未分配、来源缺失、清点不完整或 Issue/PR 已关闭均不构成豁免。

### 8.8 Updated disposition / 更新后的处置状态

EN:

- Umbrella Requirements #262–#266: MIGRATION_DEBT; independent review remains pending.
- Historical Issues: all 39 covered; 33 English-only titles individually registered; body-language verification remains outstanding.
- Historical Commits: latest 100 sampled; all reported single-language; complete historical inventory remains outstanding.
- Historical PRs: repository total 232; supplied single-language inventory classified by integration unit.
- Formal EXEMPTION: NONE_RECORDED.
- Accountable Governance Owner: NOT_ASSIGNED.
- Migration completion: NOT_CONFIRMED.

CN:

- Umbrella Requirement #262–#266：MIGRATION_DEBT；独立审查仍待完成。
- 历史 Issue：覆盖全部 39 个；33 个英文单语标题已逐项登记；正文语言核验仍待完成。
- 历史 Commit：最近 100 条已抽样，均报告为单语；全部历史 Commit 清点仍未完成。
- 历史 PR：仓库共 232 个；提供的单语 PR 清单已按集成单元分类。
- 正式 EXEMPTION：NONE_RECORDED。
- 责任治理 Owner：NOT_ASSIGNED。
- 迁移完成状态：NOT_CONFIRMED。

### 8.9 Supersession and preservation / 覆盖关系与历史保留

This section supersedes the previous statements in §§4.2–4.4 and §7 that the Issue and PR inventories had not yet been performed, but only within the explicit evidence boundaries stated in §§8.2–8.4.

The previous statements remain part of the historical record.

No other existing registration, status, decision, or exception is changed.

本章仅在 §8.2–§8.4 明确的证据范围内，更新原 §4.2–§4.4 及 §7 中关于 Issue 和 PR 尚未清点的表述。

此前表述保留为历史记录。

不改变其他现有登记、状态、决策或豁免。

<!--


### 8.10 Registration completeness correction / 登记完整性修正（2026-11-19）

EN: The original section-8 group registration contained 216 PRs. Coordinator mechanical reconciliation against the 230-PR single-language inventory identified 14 PRs omitted from all six groups (#269, #207, #197, #194, #193, #192, #191, #190, #189, #154, #143, #141, #139, #136). The omission was a registration coverage gap in the original grouping list. All 14 were assigned to existing P-01–P-06 groups (no new group created): #269→P-01; #136→P-02; #191→P-03; #207, #141→P-04; #197, #194, #193, #192, #190, #189, #154, #143, #139→P-05. Registration baseline corrected to 230. No historical PR state changed; no SHA/Owner/date/approval evidence created; no EXEMPTION used. This correction does not constitute migration completion, exemption approval, or reconstruction of missing historical evidence.

CN: 原第 8 章分组登记含 216 条 PR。协调方与 230 条单语清单机械差异核对发现 14 条 PR 未进入任何分组（#269、#207、#197、#194、#193、#192、#191、#190、#189、#154、#143、#141、#139、#136）。该遗漏属原分组清单的覆盖疏漏。14 条已全部归入现有 P-01–P-06 分组（未新建分组）：#269→P-01；#136→P-02；#191→P-03；#207、#141→P-04；#197、#194、#193、#192、#190、#189、#154、#143、#139→P-05。登记基准修正为 230。未改变历史 PR 状态；未补造 SHA/Owner/日期/审批证据；未使用 EXEMPTION。本修正不构成迁移完成、豁免批准或缺失历史证据的重建。

Coverage check / 覆盖核对: 216 + 14 = 230 = coordinator inventory; 0 missing; 0 out-of-scope; 0 duplicates.
