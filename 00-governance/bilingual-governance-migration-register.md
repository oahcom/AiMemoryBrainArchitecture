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

The original supplied inventory snapshot recorded 232 Pull Requests. The object-level reconciliation baseline at main commit `f86fddc0fa0291ea8a5e080e741f083ce179a0a2` contains 242 PRs; the 12 later PR objects are confirmed and registered in §8.4.2. This is a dated baseline, not a live repository total.

The supplied single-language PR inventory is classified by integration unit.

Each PR remains an independent historical object, even when grouped with other PRs.

| Group | Integration Unit | PR numbers | Migration_Status | Accountable_Owner |
|---|---|---|---|---|
| P-01 | AI governance / AI execution / policy adoption | #281, #280, #278, #277, #273, #272, #270, #269, #267, #261, #260, #256, #250, #248, #237, #230, #201, #199, #196, #195 | MIGRATION_DEBT | NOT_ASSIGNED |
| P-02 | AI execution traceability / bilingual governance / recovery records | #279, #271, #158, #157, #156, #155, #150, #149, #148, #147, #146, #145, #144, #142, #140, #138, #137, #136, #135, #133, #132 | MIGRATION_DEBT | NOT_ASSIGNED |
| P-03 | Phase 1 Rust / Storage / SQLite / Event Store | #249, #247, #246, #245, #244, #243, #242, #241, #240, #239, #238, #236, #235, #234, #233, #232, #231, #229, #228, #227, #226, #225, #224, #223, #222, #221, #220, #219, #217, #216, #215, #214, #213, #212, #211, #210, #209, #208, #206, #205, #204, #203, #202, #198, **#191** | MIGRATION_DEBT | NOT_ASSIGNED |
| P-04 | Publication / Forget / authorization / recovery | #276, #274, #187–#174, #173–#160, #159, #153, #152, #151, **#207, #141** | MIGRATION_DEBT | NOT_ASSIGNED |
| P-05 | Architecture / domain / integration / research | #275, #257, #255, #253, #252, #251, #197, #194, #193, #192, #190, #189, #188, #154, #143, #139, #131, #129–#121, #120–#114, #113–#99, #98–#89, #88–#80, #79–#71, #70–#60, #59–#52, #51, #50, #49, #48, #47, #46, #45, #44, #42, #40, #38, #36, #35, #34, #33, #32, #31, #28, #27, #23, #22, #12, #1 | MIGRATION_DEBT | NOT_ASSIGNED |
| P-06 | Event Store payload / Global Forget inventory hardening | #259, #258 | MIGRATION_DEBT | NOT_ASSIGNED |

CN:

原始提供的清点快照记载 232 个 Pull Request。对象级对账基线 main commit `f86fddc0fa0291ea8a5e080e741f083ce179a0a2` 共包含 242 个 PR；新增 12 个 PR 对象已在 §8.4.2 核验并登记。本数字为带时点基线，不是实时仓库总数。

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

#### 8.4.2 A Integration confirmation of the 12 later PR groupings / A 集成确认后续 12 个 PR 归组

**Decision scope:** A Integration confirms group classification only, exercising the coordination responsibility recorded in the F-06 object reconciliation report §4. This is not Project Owner approval, target-group Owner approval, accountable-owner appointment, language-state classification, or migration completion.

**Method:** each PR was fetched by exact PR number; title, body, state, merged flag and exact head SHA were read from GitHub. Group choice follows the PR's substantive integration unit and body, not number proximity, author identity, or title language alone.

| PR | Exact PR Head | State at readback | Confirmed group | Evidence basis |
|---|---|---|---|---|
| #48 | `cfcc8f20e2bd6323798864875735db4c57038479` | CLOSED / not merged | P-05 | Bilingual principal system-wide architecture risk assessment; research/architecture review record |
| #271 | `1eefa22e7fecfcd882aff795796ae178d1f7c4a5` | MERGED | P-02 | GOV-DOC-001 bilingual governance baseline and migration register |
| #272 | `e698999f1e8c80afb0fc9239971ae00ac509cf34` | MERGED | P-01 | Governance lifecycle gate consolidation (12-state to 6-phase) |
| #273 | `5e0a919a9253b8747c59062b87d0a580cd204e54` | MERGED | P-01 | AI execution governance structure and RULING-01 anchor correction |
| #274 | `9be9a09fb13fc7442f5a88e70280ffdfdfd989b9` | MERGED | P-04 | Typed watermark and ForgetFence binding contract |
| #275 | `373aaf5def95d64554d8ad020a1a53a0934f6819` | MERGED | P-05 | Project positioning, architecture and roadmap |
| #276 | `a7c15572d851f7764c7565c95b80c24a94548cde` | MERGED | P-04 | D owner-snapshot namespace and ForgetFence currentness contract |
| #277 | `6a6088afc4994e274974917e3fceb5e08c083bfe` | MERGED | P-01 | AID-2026-001 R3 development-baseline governance integration |
| #278 | `5f049265fc24a76fdac3647ff0b56eeee2521dbe` | MERGED | P-01 | PR-GOVERNANCE-001 acceptance-comment checklist |
| #279 | `33302f40e76065becf8e8e7e312a03a9c2438bc0` | MERGED | P-02 | Bilingual documentation tiering policy, inventory and checks |
| #280 | `ffda3ed9fcb6a697ae5ffa00a0ef007ce4a97d2e` | MERGED | P-01 | AID-2026-009 direct-push ratification record |
| #281 | `2f7397208fb5e76b69b43444cd0fbb3b3d0ce647` | MERGED | P-01 | Governance enforcement v1.2 platform-check unavailability handling |

**Result:** the 12 previously proposed assignments are now confirmed in the group table above. Together with the existing 230 group entries, the six groups cover 242/242 PR objects at reconciliation baseline `f86fddc0fa0291ea8a5e080e741f083ce179a0a2`. The earlier “14 unassigned PRs” statement remains retracted; those 14 were already present in the pre-existing group tables.

**Authority and limits:**
- `Accountable_Owner` remains `NOT_ASSIGNED` for every group; no individual or domain Owner is appointed.
- `Migration_Status` remains `MIGRATION_DEBT` for P-01 through P-06. Group registration is not bilingual migration.
- PR #48 remains CLOSED / not merged; its group membership does not alter that state.
- This 242-object baseline is historical and does not claim to inventory PRs created after the reconciliation baseline.

**中文**

**决策范围：**A Integration 依据 F-06 对象级对账报告 §4 所登记的协调责任，仅确认集成单元归组。这不是 Project Owner 或目标组 Owner 批准，不是责任人任命，不是语言状态分类，也不代表迁移完成。

**方法：**逐一按精确 PR 编号读取 GitHub 的标题、正文、状态、合并标志和 Head SHA；根据 PR 正文中的实质集成单元归组，不按编号邻近、作者身份或标题语言推断。

**结果：**此前 12 个归组提案现已确认并写入上表。与既有 230 条分组记录合计，在对账基线 `f86fddc0fa0291ea8a5e080e741f083ce179a0a2` 覆盖 242/242 个 PR 对象。此前“14 个未归组 PR”的说法仍明确撤回；该 14 个编号原本已存在于旧分组表。

**权责与限制：**
- 各组 `Accountable_Owner` 继续为 `NOT_ASSIGNED`；不任命任何个人或领域 Owner。
- P-01 至 P-06 的 `Migration_Status` 继续为 `MIGRATION_DEBT`。归组登记不等于双语迁移。
- PR #48 仍为 CLOSED / not merged；归组不改变其状态。
- 242 个对象是历史对账基线，不声称覆盖该基线之后创建的 PR。

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

### 8.11 Issue Language-State Audit — 39-Item Scope

本节登记仓库全部 **39 条非 PR Issue** 的语言状态，范围包含 Issue #254。语言状态依据各 Issue **body 的实质内容**判定，而非仅依据标题、标签、评论或技术术语的语言。各条目的 `body_sha256` 为对应 Issue body 的内容锚点，可对原始 body 重新计算 SHA-256 进行复核。

语言状态分类汇总如下：

| Language State | Count |
|---|---:|
| EN_ONLY | 28 |
| EN_ZH_MIXED | 10 |
| ZH_ORIGINAL_WITH_EN_TERMS | 1 |
| **Total** | **39** |

以下登记表逐项记录 Issue 编号、语言状态及对应 body SHA-256：

| Issue | Language State | body_sha256 (OBJ-A 锚点) |
|---:|---|---|
| #2 | EN_ONLY | `1a4bd2cbcbb2dc81c2868981553b96886f2a437755fea017a49f839854697a2d` |
| #3 | EN_ONLY | `19188103a04021af276fa3b82af32c8c4a0afe051674bd7c4d7c50af79d56c4b` |
| #4 | EN_ONLY | `5a30580e411d2aecc600cf3026a7ee8b2ceab37da02cf4f5212dfb218a51a588` |
| #5 | EN_ONLY | `e93edb64b4a30e425cd9176eba6fd126d7fe17bbb1ed3563ddf4175151a43fb2` |
| #6 | EN_ONLY | `45d23446569fcc893685575cd116b81ea0585f00e14b02ac3b6b75ce094e8977` |
| #7 | EN_ONLY | `9c54da9ce461f84c3d0bb5aff8ba94e56aaad97854617bd0f510adaaf70e060c` |
| #8 | EN_ONLY | `a4a2dcbcefcc31c95a63db4ae69db5a0bf7e3872d891b671db7cccea7c36b677` |
| #9 | EN_ONLY | `029cf67f2c15186c26701275940a2806eec1337c73184959b915d2f46c4dc4ca` |
| #10 | EN_ONLY | `0147a6c6f0c0506f7daa72687cbe6df69915776a5bde341fb633bd1e5a8efb45` |
| #11 | EN_ONLY | `0ffbc91be11af283c3f9c87dc837ddca8f67743f3ec14ab40a0e33ad0cef2329` |
| #13 | EN_ONLY | `a07fd8757fb7a045835193ea3f98cc8f57234d58a1179b1975dede05b55e95c8` |
| #14 | EN_ONLY | `f902bbd9c3224dc0f483b6d0149c581f441160894ccf1e71f2bf1d080a323ed9` |
| #15 | EN_ONLY | `718ed5d5017943780e63565bba782000ef8dd09318eadba973fe2bae380a1a0d` |
| #16 | EN_ONLY | `607e42171f6875477646a4a82c578232fef74db676e32fdd0a46978df1e17b19` |
| #17 | EN_ONLY | `d9e828c97662b8120fd9336f1a6a9ce8a404dbd4e1eac9e7b42e512be86c3ecb` |
| #18 | EN_ONLY | `8766750274a58b0ee584a6a5f2fc89a5a57c21f158b56a6aae29af149f9078d3` |
| #19 | EN_ONLY | `0b46b5f326d7fccc46023ecaa548f1709c72ab93e7f3d5ef1a7b78446b7f7bc3` |
| #20 | EN_ONLY | `8f1704fef55b0968fec0baee8843a3d92b429bd71d3a3de8617977dec6b1b043` |
| #21 | EN_ONLY | `c74c2ca31dabc95c988752f40cba51ad276040b608228782d3dc783a21303ac9` |
| #24 | EN_ONLY | `9d2d498404ef4a8aa00666d9aad1451cbb68dd2560c6c7216d04e96a0fde62e1` |
| #25 | EN_ONLY | `52fa354aa863ea983203fa669956c7275629e89a246e3538b2497b51ba594d14` |
| #26 | EN_ZH_MIXED | `eee6973bf825191fc97ffa0ae134500696377403f71a4fd94c532957abd220aa` |
| #29 | EN_ZH_MIXED | `5deb78f2cb9f1094b32fb024f5681d1717d485f49369031bf3383bded02e0a59` |
| #30 | EN_ONLY | `f693004486b8ad26c82b99122680e720828de3660ff1be2afac818edbac146d5` |
| #37 | EN_ONLY | `7d41f1f1cbd82a53c392fe03d9e1a6471b9b737b7ae59fcff0dda8bd97ad17bb` |
| #39 | EN_ONLY | `e1e7f413617c297d7bfd49f83204b7dea3d2607e944bd80a3648776a67e79317` |
| #41 | EN_ONLY | `155a7cf73ab71e9ac402d842b01bab9c6a96dbefb247ce74a2e56a983c2e2823` |
| #43 | EN_ZH_MIXED | `48f39d59bde15070c9fa9cfef6a5c8a49890064d6dffbf23a83b0ff2e4900d38` |
| #130 | EN_ZH_MIXED | `00714e5bbe0859b653c05cfc5a7ee69406e7abaa817626b4ed21c43994f69414` |
| #134 | EN_ONLY | `e2d5a8e3d20c25d2d427d68a6c8d17d809f4366b319446e875448b634189b13f` |
| #200 | EN_ONLY | `b56af133a378c0d4bebb723bd4d1f58999dfc60f602b76ab79964a20d1d7a669` |
| #218 | EN_ZH_MIXED | `772e5780cfd1c5d086826610866b3f6998fa6fb7e34f17a95a148fbeee56ec36` |
| #254 | ZH_ORIGINAL_WITH_EN_TERMS | `7c707cd5444bd0fedf2593a3200efd7e0fb90894455272fa817dc97587f324ff` |
| #262 | EN_ZH_MIXED | `eca818dec85b37532d1a586a96e3edde705d72cf2fd56f2a317e04328fc0f64b` |
| #263 | EN_ZH_MIXED | `2dd07b99c798521d399c01341267b460e7f1722c16ebb29c473d956bcce5086f` |
| #264 | EN_ZH_MIXED | `6df7dca0116231577397f71df84afd281ea70ba80f5466e3e66ab6a4797c4ee6` |
| #265 | EN_ZH_MIXED | `a2e727c5b977a4216c5e72b514eafa718a92e64b8f6a1f6bc263bde6477570e7` |
| #266 | EN_ZH_MIXED | `d984146097e7ce9a031f7046f4267ce7e2b40cd0380ccd6c37f98d17e93fadef` |
| #268 | EN_ONLY | `d3f387949e9f71b1e95c2dcbde4dcbad2dfaa521bd52682ca5a1d8e1d1901f16` |

本节登记用于固定 39 条 Issue 的语言状态及其内容锚点。**登记本身不代表 Issue 已完成语言迁移、正文改写、状态迁移或关闭**；这些后续动作仍须依各自授权、审查及治理流程执行。若 Issue body 后续发生变更，应重新计算并更新对应 SHA-256 锚点，不得继续将旧锚点视为当前正文的校验值。

注：本表锚点为清点快照时的历史值。清点后被编辑的对象以 §8.15「锚点刷新登记」为准；截至本次修订，仅 #266 存在刷新条目。

Note: the anchors in this table are the inventory-snapshot values. For objects edited after that snapshot, §8.15 "Anchor refresh register" governs the current value; as of this revision only #266 has a refresh entry, and that is a statement about this revision, not a permanent limit.

### 8.12 Out-of-Scope/Disposition — Issue #254

Issue #254 属于本次 39 条非 PR Issue 审计集合，为集合内第 39 条。其语言状态登记为 `ZH_ORIGINAL_WITH_EN_TERMS`，即中文原始正文中包含英文技术术语。对应 `body_sha256` 为：

`7c707cd5444bd0fedf2593a3200efd7e0fb90894455272fa817dc97587f324ff`

**处置状态：HOLD。**

Issue #254 保留为独立外部审查证据载体。在 HOLD 期间：

1. 不得将其转移至其他 Issue。
2. 不得将其与其他 Issue 归并。
3. 不得关闭该 Issue。

HOLD 的退出条件为以下任一项完成：

- 全部审查问题均已转化为具名 finding，并建立可核验的回链；
- 治理 Owner 明确登记其处置状态为 `ARCHIVED_EVIDENCE`。

只有上述任一退出条件完成后，才允许进入关闭流程。协调器无权自行认定退出条件已满足，也无权自行执行或授权完成 Issue 的状态变更。

最新处置记录为 Issue #254 评论 **7005618269**。该记录作为本节处置依据的追踪锚点；在退出条件得到满足并由有权主体完成相应登记前，Issue #254 持续保持 **HOLD**。

### 8.13 Commit Message Language-State Audit — 313-Commit Scope (Part 1: C001–C160)

本节以 **完整 commit message 的实质内容**作为语言状态审计单元，包括 subject 与 message body；不以提交所修改文件的语言作为分类依据。

审计范围为 C001–C313，编号沿用 E9 原始编号，并按提交时间排序。全量分类汇总为：

| Language State | Count |
|---|---:|
| EN_ONLY | 312 |
| EN_ZH_MIXED | 1（C168） |
| **Total** | **313** |

本节前半登记 C001–C160，共 **160 条**，均登记为 `EN_ONLY`。每条记录包含原始提交 SHA、语言状态、完整 commit message 的 `msg_sha256` 锚点，以及 commit message 第一行 subject。`msg_sha256` 用于对完整 commit message 进行复算核验。

本节登记仅固定历史提交对象及其语言状态审计结果，不改写历史 commit message，不改变提交 SHA，不代表相关内容已完成双语迁移，也不得将登记结果升级解释为迁移完成。后半部分 C161–C313 另行登记；C168 为唯一 `EN_ZH_MIXED` 条目。

| Commit ID | sha | language_state | msg_sha256 | subject (first line) |
|---|---|---|---|---|
| [C001] | 2ca77db4c66529394304f0e1e51ba4696544cfb6 | EN_ONLY | `0b99f18f843a3aad1d1422fa2696ebbd3c6d3cb14c9a4bb86e7795e1eec0020c` | chore(FIX-2026-P1-T1): record terminal R1 PASS |
| [C002] | c5a995d9a2808112b007a9108e085048cbed5cc9 | EN_ONLY | `7226dfdb30bbacd65be5171b84af403fb1437518598d1483844ee70d8283d077` | docs(work-items): close exact-head pending evidence states |
| [C003] | cd6efa2ba2ea098660ed66ba3e9c7d23df739e3e | EN_ONLY | `00ff0332c5df8235263e11c2cbd19af691093a0358dc4c33367b1309a7440115` | docs(work-items): reconcile FIX-2026-P1-T1 final review evidence |
| [C004] | c3bf7e47b5121c89277d3df55b12a7a95dcc9706 | EN_ONLY | `0ce9f1c9a19210b1bdd2c1d2bea3de4ec2293b8d00eccd2e16bbb2b7b23dc8f1` | docs(governance): remediate FIX-2026-P1-T1 review findings (#270) |
| [C005] | 9b67fb1b0550aa49abce97e653f0df931f3cbeea | EN_ONLY | `545b0ac075023372c4edd41915ccde34c6104c0ba13f2bee04d5566a646e46bd` | feat(event-store): persist and verify event payload bytes (#258) |
| [C006] | cd3f5d7191000f6414134ef235cac94f33ca87e8 | EN_ONLY | `de91ecbf17635a5ff894f4eda30fc350153d2b76590e845d6e84199594c1b7d1` | docs(prompts): simplify prompt template from 15 to 7 core sections (#269) |
| [C007] | 2df5517a58132153a554f96c22f420782e7d513c | EN_ONLY | `35813474493f1e99e9348c2adeabd73716ebbff80629c28e6fd9b16ffa2f1db6` | docs(architecture): correct acceptance and idempotency ownership in #43 (#255) |
| [C008] | 3e8577acc3c65a28464406d99fa1bf06a36e01fc | EN_ONLY | `78f2a9b0e734006c6e439a00defee37b55ab810935722ff252ed92a25c952393` | ACCEPTANCE-LOGIC-PHYSICAL-001: bilingual acceptance matrix for #25/#43 (#253) |
| [C009] | 5c751f1febe7e03de4b9b6c0f968bab1c7093be2 | EN_ONLY | `0627f339d95d2712bd7ebb1ff1c17cdcd48570df50c374df0310e1cc558b0cec` | docs(integration): converge candidate D/E/I/Storage callable interfaces (#252) |
| [C010] | ed842fa7ce9dd9df7b808495abd5cd1071850547 | EN_ONLY | `1ef290bd8ec6bb8d9c5504661435c8424c8b24e3c97455e0509483a5a0cee987` | RFC-IDE-001: Idempotency identity tuple contract (bilingual) (#251) |
| [C011] | b663c8fde45dd5db3b02c434c47def34a6d1fefe | EN_ONLY | `25b44485debc6263dcc83e354844f8b92604bdf18de2f13f6b9a630b59a619b2` | fix(storage): enforce Phase 1 invariants and deepen SQLite acceptance (#249) |
| [C012] | c33a1bcd36f767c96f641d2a154f34d102ce2645 | EN_ONLY | `aa4825a1cad096f757779f6d8e579682830ed441f0d7330273248afe3131a2ab` | docs(governance): register AID-2026-006 REQ-HIERARCHY session-management baselin |
| [C013] | 5ab18f57f3505cc26f1df457033fd9a5b8cf4aaa | EN_ONLY | `f3bb4f07b598991a33ee211e3443f58e43f5966b2ddb28f2b7811e02112ddf87` | docs(governance): register AID-2026-005 in work index |
| [C014] | 1957faa6349613280576bfa5f2a3a7107f6cb719 | EN_ONLY | `731734f966b57bbb93c7b8d69dfa4a5ff931ebe9806d8c385bf3cb68e087be8d` | docs(governance): add independence ruling proposal |
| [C015] | ef00db086d9c53894f50ce7a845a9bf7210c4408 | EN_ONLY | `de010b46c04ca5dee5607c7c0886549032280050227cfd421ba0715ac10a20b7` | docs(governance): register AID-2026-005 independence ruling |
| [C016] | 7524a3dbba469298b7277c0478c1e65b56dd184b | EN_ONLY | `babdb27e47631e855fc0fb5a89c80f38e4699908e2fa8161e03e26229d162c02` | docs(governance): add PR enforcement and evidence standard (#248) |
| [C017] | 5ce8657d402b911c72ccf1f2bd14c235d49aca86 | EN_ONLY | `57247a5777fd88cd1a2fce11a8b0eaa799c928b0d22fbbeee86a5e9a604b3e01` | docs(integration): Phase 1 A/B/C architecture integration review (#257) |
| [C018] | dfd4fdce0be0a03aa7d06a9feca7af1acfeb409b | EN_ONLY | `1e8ee885e7909a27fda79012dc2112a3bb83a9d8e549a5277b314e418c3ad57d` | docs(ai-dev-os): clarify Session 4 connector evidence (#261) |
| [C019] | 38ee99bc210c24d134217cabd6fbad3e10610125 | EN_ONLY | `bc6344310fba7ed16b5ac1f2f1c720f3a3ed7d4617ae91c5c42a32b5304672a5` | docs(governance): add bilingual PR merge evidence summary (#250) |
| [C020] | b2960d37591104a0fd27c81a4b98b30d386ea75f | EN_ONLY | `ba46ccb71bdc0aae1063faaf0da66098d4ed2681bd89eda46b84a9634a452ddd` | docs(work-items): reconcile Issue #130 session coverage (#260) |
| [C021] | 21e84c5fdfcf0eff81a327e3b224fb4f228919c1 | EN_ONLY | `7d7145940bf6b5c1b78bc9a772580c87e202a31bb49a027c0bd8e2482c855a82` | docs(i18n): link AID-2026-004 Issue closeout |
| [C022] | 8d9ee71c5e6ca92849e57e38cb88ca1656f6fb14 | EN_ONLY | `ec4ffed13afd8f955112896e5f24aca2ea1c3755f9eab83177a51d4bea5e322b` | docs(i18n): register AID-2026-004 in work item index |
| [C023] | e2fa44b1437a9cee22247fffd40c245a13fa4f90 | EN_ONLY | `865d12caf77233b2e63b613806281e257c4e97b6fb43fccf598cca3b6f1da36a` | docs(i18n): clear stale header for AI-EXEC-ROLLOUT-001.md |
| [C024] | 6059067d1aed1ca9e3785a8f12362423c1262e20 | EN_ONLY | `0f93b0390c09192d569111a2721107a2a2777cfab2c6c359154c1ed4c1ed0497` | docs(i18n): clear stale header for AI-EXEC-002.md |
| [C025] | 9eb59ceacf755d2c0ba54f3150e2fa91f1568beb | EN_ONLY | `fe38fc7af33c76f4f7478b25e4749ab5b51587300ac92e6c3c0aefd2913fd60d` | docs(i18n): clear stale header for AI-EXEC-001.md |
| [C026] | 3fbabe744a27dc4b44b414fd05009315ba4410ec | EN_ONLY | `fc8a5d1886645bd650939c1a885c0ec7404a4a331882aa914a1f568fcb7e40db` | docs(i18n): mark AI execution documents bilingual complete |
| [C027] | 26fa557c5598c8e91d8d648eb39824b7aada8a89 | EN_ONLY | `63abb48355209f724d8ce50f776e96c1ccec8d19e4ca0ca971bdfa5a1e612129` | docs(i18n): close AID-2026-002 bilingual exception |
| [C028] | 685622181144359f19b7aeb50deb00c451455cd2 | EN_ONLY | `e9de573902aa99b3e1e8565939a5f37cbef5992a93fbd33df2e05f7f6db5995e` | docs(i18n): close AID-2026-003 bilingual exception |
| [C029] | 6275265e08267d9e6a007b51ade5a1a1f8fce4ce | EN_ONLY | `4208dd58a34caf815d89308382713f05e251abaaa684078493c862ae55a1b961` | docs(i18n): register AID-2026-004 bilingual closeout |
| [C030] | e683ea275dfaf85fff0f9d18bb706d3bdb5d60a1 | EN_ONLY | `d52bda395d53c8cdd35afd41afc53ceda3cc9970247d4835f904400b9bfa0b88` | docs(i18n): add source-aligned English AI-EXEC-ROLLOUT-001 |
| [C031] | 08b07d228dbe78a209a5af68c4988b292e65e9c8 | EN_ONLY | `82f8d3e1aed58f2b5a16305cdfe25160f3e6c9b41f47968862d54124498162a0` | docs(i18n): add source-aligned English AI-EXEC-002 |
| [C032] | e0e20ed30b4a21c2e26d0a4c0903a63c0293a46f | EN_ONLY | `56203763e5a78f998d82551f3650db517398d024fafd497613637b92a4752367` | docs(i18n): align AI-EXEC-001 bilingual heading structure |
| [C033] | 0d2857a0fd026e49048031a7fd8b5d0d137ebf87 | EN_ONLY | `1cb530a85f0c9ab2462cc3bc266faf88b898890ca475242b3b68022291159dda` | docs(i18n): add source-aligned English AI-EXEC-001 v1.1 |
| [C034] | a7d64175bb9f2dc1fd1933563f1759e2edd20b9d | EN_ONLY | `48b4a2a110f8d762352d1a5098a06cb6339c270f41ea12c8657b9d3cfa8e7ba1` | docs(ai-exec): register policy ruling in AID manifest and INDEX |
| [C035] | 1f97c3fae65828266a0c3cb1d1e8d4e6cb330856 | EN_ONLY | `70239c8674b6c1c6c0485c73ba6c6d793d1414db0e4ba7059a9a5f4e2eceac96` | docs(ai-exec): rule three inter-standard conflicts and adopt v1.1 |
| [C036] | f0f5149dccbcb78fb23728205522e87f703218f5 | EN_ONLY | `309a41c87f91204acd3602433c01ce10caac4f795ed062a928af1050fb132389` | docs(index): close REG-01 residual adoption status cell |
| [C037] | 0f05c41b2fd6713a550ee737d573e913bafcaf91 | EN_ONLY | `d1032197b6718035f81f5afec86235bba44932e6a3b78fd441bc734ac243d678` | docs(aid-2026-003): record v1.1 adoption via PR #256 |
| [C038] | 3cc5419b339c00e054d5ac6ac7305d64cdd41bf7 | EN_ONLY | `d1032197b6718035f81f5afec86235bba44932e6a3b78fd441bc734ac243d678` | docs(aid-2026-003): record v1.1 adoption via PR #256 |
| [C039] | 48a556491506d25e78be47957276bf3821797a0a | EN_ONLY | `59338ff575fd3e0e7f568cb253957501444c4004181706c77d5c1c22eb0d9aa5` | docs(ai): AI-EXEC-001/002 v1.1 — close six rule-completeness gaps (AID-2026-003) |
| [C040] | 6b5db2918cffc2281deb22fd9858a37dbaeec726 | EN_ONLY | `49af2536eb5d2b6ed1351792b33111f055443822b3400a8a1f97d97d2978cc42` | docs(sqlite): decide bounded persistence and CAS guarantees |
| [C041] | fcdecf0a4e638c8b3c9ac0e4623f97c98ed21291 | EN_ONLY | `b6c31f335bbcde3d13691589d391263e86a624a765b417873a7a38b1b7871977` | feat(event-store): persist compile intent transactionally (#246) |
| [C042] | fb9b25cec0778eb6819eb2df0484e88445b5b837 | EN_ONLY | `6b376474e99b6ac3dcbf4c7a04d6516a618b3c66e9a916ee6a52619fac625cc5` | feat(event-store): add SQLite durable acceptance adapter (#245) |
| [C043] | 612c4b2d4d7e998818bee79fd0ce98b66ce78203 | EN_ONLY | `c7b05299c98ec53edd8ce9a3dcccfddec7b1ea9fe9fc866ef1b06a603ff158bd` | docs(work-items): record prompt-file commit SHA in AID-2026-002 registration |
| [C044] | 4a3e06fd263e9dbd1056179dceb3cb21b17e330f | EN_ONLY | `ca0da5d28908a5a8c80764f6dd92b399419b266b048667de3fa53e7a6fbcea09` | test(sqlite): verify independent-connection races |
| [C045] | aa711289785395d2efa202e34def64c393ee0ac7 | EN_ONLY | `82821fbc6f5f53c5f48d657b723a1c33689a5c59cfbf32b686619f86eb837586` | test(sqlite): verify durable reopen and abrupt process-exit rollback |
| [C046] | 715878ef3f5ce1331bc9caf771dd20481da1145e | EN_ONLY | `d4c959e50ec3e0dbbd1a12b7ced2ca3be5fb8de31152785dfa33d78def854cc9` | fix(rust): restore Phase 1 workspace serialization gate |
| [C047] | 6691bfba44cbebce6c4d3556e1c1cf9bbb3b16c8 | EN_ONLY | `7cb0263c5048d3010082ea68dcf6a13563bb5181241ec265d7daa301c42ff379` | fix(sqlite): paginate change records after scope filtering |
| [C048] | bcfa0f4cb307b3e8a1a2910e43b6a7ea63ea29e8 | EN_ONLY | `38eb4f44e9a8f0e10bb72eabb1da6a5da230b83207bf8a002ecf7be248838add` | ci: consolidate Rust workspace checks into one required gate |
| [C049] | 99a79fce7276853461a4ff28d89bfeb5df72d0c3 | EN_ONLY | `5379a28156af3dddf084996f50abf9ea57090f5a0143a562bd3889d4fbac0e45` | test(store): enforce scope and idempotency in facade fake |
| [C050] | 778b4d3b4b6c846faa6a02247d31d14a33d8b626 | EN_ONLY | `0bc83e464ae0a7b5896fdc682b800919b4f770fe6f79a9baed562a6a275fedd2` | docs(ai): close out and adopt AID-2026-002 |
| [C051] | e68a5d66f11383c5252a00bc9547073ff9f911d7 | EN_ONLY | `3977ff1358c920ad004129531bb66d9d9c3046d171ee92c17e1b44d328d0f710` | fix(sqlite): bind idempotency replay to memory identity |
| [C052] | ec4beee51b897d05f8253318c18b47a2ef25b368 | EN_ONLY | `86c2da195a49db0e4ad66be4a3778e0ef5c81eaf4afa6cdc0088d9f9ce95ad84` | ci: add Rust Phase 1 workspace test gate (#233) |
| [C053] | 53aae842c390eac6d54f937af6cd2744dbe8d09d | EN_ONLY | `777d970e61294244daeeebf3439f0381dd1b6790c1e987cdd8f5222b5b7ee46a` | docs(ai): add AI development execution rules and ecosystem rollout |
| [C054] | 396c569d234417aea84c1bbd9e3f2bf0a5d76bc3 | EN_ONLY | `776f59272858a456ff3b1db02cbfecf0802fdb2c31523fb9380d8071fcc2fc37` | test(store): prove minimal SQLite-backed Memory Store path |
| [C055] | 2d7675d590f3144ff56a0ecf55c6c8a31cfd1b47 | EN_ONLY | `c234b5bd853e53d7617032f5df96d89deec7d47c55c23d2f374721f25973dac0` | feat(store): add Phase 1 minimum Memory Store facade |
| [C056] | 7b8eef64390ed31cb92bdf7b29c98623d79a31fe | EN_ONLY | `d4eb68d96e552f0ce4c4918fb966ac4af50a7503e0026e3c9796d248611f9326` | fix(ci): complete Rust workspace integration |
| [C057] | 5447db7d0316e1725e0288cfad081cd7db74fe6c | EN_ONLY | `3e58951241123b0452e005303cd926625cf54bda5fcb852dd989cb3e35ecdbff` | fix(ci): complete Rust workspace test gate and SQLite serde dependency |
| [C058] | 02d13d19ba9b499de2670d7e565627a2fe200bfb | EN_ONLY | `c7a5a50080ff7d82bd4316fc678bf8b8b7fb3b18979cffbc7c180b776aa1cfd7` | fix(storage): enforce scope before creation and idempotency replay |
| [C059] | 0b35ee865bdd77229d411df4047cb6a9df13705f | EN_ONLY | `31f75fa766709e7e306e1cc1ee734fa2056155ea31f1582afadcda99a438fcbd` | fix(storage): enforce scope before creation and idempotency replay (#212) |
| [C060] | f8e6bb7fd3cfc71a0fc438b80029e0ef58063b4d | EN_ONLY | `44d9a2abc053d3890b2a19603b963f76b1651dcf4eaaf878da44867216dd7891` | fix(domain): align Phase 1 Rust implementation with frozen contract |
| [C061] | 7fa89148ef42e72a9ec15ef21db23cfd28aeb05b | EN_ONLY | `b83bd0c24edfc37493ad229355be1bd7205e4d36ba7dbdf0f1e74d8aa63ef808` | test(publication): enforce authoritative I currentness at protected boundaries ( |
| [C062] | 32788ba871ad4c503306401b642511716f719a91 | EN_ONLY | `1b9bb42b24a5a8b0671e7be9a2f292bc57a765a5d4df8953dd750e037a1935aa` | feat(event-store): define Phase 1 durable Event Store contract |
| [C063] | 23f81fb788cb52ade4543a4f3b3e34c923cbaf02 | EN_ONLY | `7592a2f3dbdcd4d2a54156c74e0eb239e983a09f016b1d359f2c0e92f396a1bb` | feat(sqlite): implement Phase 1 SQLite storage adapter |
| [C064] | 839b9e3acf5385ba6a11df3f51a92a86b332cd9a | EN_ONLY | `f345716046d2f3f60d8266076356b738cfd53306680f4431ae3bea7f6d0dc175` | fix(storage): add bilingual trait counterpart |
| [C065] | 474d0f2229eed2fe24898bd208a24b7d9423773c | EN_ONLY | `49f545ff9a0a0cde2d6236e8183e7d71de9a313503eac7a92d3f648af6f0b9f6` | docs(governance): reconcile PR-GOVERNANCE adoption status (#201) |
| [C066] | 162b1286d3ae69f19c8cc17ebd3d0aa2619596da | EN_ONLY | `69a88cfa4fe1fbe51d1568a8ad0b2b67c644e349de5a6caa91d24d843f09f46c` | docs(domain): add Phase 1 bilingual freeze counterparts |
| [C067] | add9a41d189f2088d426abe77fd6ad827a2d5f6c | EN_ONLY | `f4d88eabe45306a3466f1165b0c5fdd1a085bd6303b9f4e3290ce941d004368f` | docs(domain): add Phase 1 bilingual domain-freeze counterparts |
| [C068] | 10e9ded53c3b2b6cd7b875fc5e965c62c4a060b5 | EN_ONLY | `3a2bce97dd81e05ad32a8191291a03795b762a046cc908904113ffae97a1ef39` | feat(storage): define Phase 1 backend-neutral Storage Trait |
| [C069] | a9f6d9431ef1f4918b025a23a69463008e92b3c2 | EN_ONLY | `060f46070f30c51ff66e51107547e01b8a34caf28c3f8c0f200da5226c0877cc` | fix(domain): preserve open Claim identity decision |
| [C070] | 87a2199a0b6f89c14858f475e10e86cb7d6a452f | EN_ONLY | `ca30ccae148ed43dde115e8e7595a1efe7e3040742497405829e233d4fe527db` | fix(domain): preserve Claim identity as OPEN |
| [C071] | 2bedbcf8c0cdf4a4ff434049c973389c526a75ad | EN_ONLY | `c5d5afbd5e82b17fc816e8696b5b6c5c3dc52fc130b5ca0e49c55f0a74b64654` | feat(domain): add pure Rust Phase 1 workspace and validation |
| [C072] | f9f4e7975de58c60b724d5fcb9a72ae76f81e52b | EN_ONLY | `fa527906fc78172837f8614d38217b0edfa1fb352785525885cfab0548def790` | docs(domain): freeze Phase 1 implementation contract |
| [C073] | 9f2dc27d767fbd335906fe0e276cd123329974f8 | EN_ONLY | `d9cbdaa11c81f67be2c8f2a47746a2c6b65cafb0f96fec609f76291224e5dc4f` | docs(recovery): refresh terminal-path dependency digest evidence |
| [C074] | 282a82e58d8d9d1aa876621481df3184fbe5d284 | EN_ONLY | `f40aeee853f47fd47a97efc0907e7ffa8997fb713a285b17df5565d7bc537209` | test(publication): cover dependency digest at commit and unknown reconciliation |
| [C075] | ee76e054ccf71bfc3b5d50af6113c699c455852a | EN_ONLY | `b07416c8412f91ce9d7b8d3f4a4367a06d305f434295d0409c3761e256219c18` | docs(recovery): refresh inventory and I currentness regression closure |
| [C076] | 39fcb173965ec78b997e803b26c9902463fb25fb | EN_ONLY | `8bc149a5f59d8edc59a70d9021d33f39ad48d2c33049930a39e52a352134047e` | fix(publication): restore dependency digest binding after PermissionEpoch integr |
| [C077] | f55a591f1ad506c48de763984b12a9a667fde9a0 | EN_ONLY | `15c9d7cc09c42b4c47ac2daf310005e4883d076d7e7c17a07e8d2b79a0b3023c` | test(publication): model fail-closed PermissionEpoch currentness |
| [C078] | 8d717b0dd18b8deec150de38d09a4f48ea23c7e3 | EN_ONLY | `0b90e4249749209ce570c7da7504ba07162a5f331c01f29df0756a2894fb9c9d` | docs(recovery): refresh PR inventory and Phase 3.8 integration overlay |
| [C079] | 78ab36929ceebf50318edeec2720cee0967e98a8 | EN_ONLY | `0ed5a8a2ed84996f1c8d2e3acb254f3b9f028cbd79c0cb5610b3cf4f885244cb` | fix(publication): bind I context and operation identity |
| [C080] | 12e1ab92820c7fac113eb266e36c9ee2eec73c6b | EN_ONLY | `e8d1f06e5277aec4b72dc989fbc79b0d70c06062883c9eb9c0de2a1bb02e2132` | test(publication): model PermissionEpoch currentness and revocation ordering |
| [C081] | e5c0a60925fdb7ee00b3cea1bda86a0d9d5f902d | EN_ONLY | `ab53c79004938f3e529fa22e5ceffdc61e6ce6e74178e095f66cf0131980a1eb` | fix(publication): bind I scope lifecycle and workload authorization context (#17 |
| [C082] | 71b91d4512bbe87ac53ab04b7e9d3e088a942eb6 | EN_ONLY | `41e4fd3375c4c3eee6e04be09d4ade54ad14baecabb92c15f9242cf65c6d5cc0` | fix(publication): bind full I authorization context in reference model (#175) |
| [C083] | 67ab237f532d2e1436a351ae02464f0926205c52 | EN_ONLY | `fb440783a8b9b7589b579eea27bb70a86bda663fd2f5963e3a8b5a7dc5818d79` | docs(recovery): append 142-PR live inventory and publication winner hardening |
| [C084] | 60b6c2a0f987db4bc150aa7b90664c4c26f96b04 | EN_ONLY | `516ede846244ad89c6ca0833e71d5d45ae5e088d87d78ac6b7b1696b8b502eb9` | fix(publication): enforce one I COMMIT_WON winner per participant |
| [C085] | 9caded49a934194376a044a909cb96fcdbccdd44 | EN_ONLY | `3cdf7c643e671bc848e6610b7eb1a3f4d0b510272dfbf4b4e295afa4fbb5a858` | fix(publication): bind final visibility gate identity separately |
| [C086] | 401fe2e6ffb8432b00d651b262ca48b808d90c15 | EN_ONLY | `1ecdf22ce4a61c7b08b24cb9aacd1d4f8fe52b628d63b51581b6a47928664276` | fix(model): bind I COMMIT_WON to digest and owner boundary |
| [C087] | bde4e5481070b87a00e25c5b1b85a37706cdb578 | EN_ONLY | `bdba171308b2f5fbe4c79621776e811f5c241b59f7c6a1703b854bf1161a6a99` | docs(recovery): refresh 138-PR inventory and I Storage model correction |
| [C088] | 2fabe07640e2f3cee69b213275c9f5a7b17edd5d | EN_ONLY | `4b2566907651dd8bcbdac17e154c74ae80ac6bad9521b27950ba16b97e7b81ae` | fix(publication): separate I COMMIT_WON from Storage commit |
| [C089] | c52034a6e1cb5b8243bc7046e28663470b6f7016 | EN_ONLY | `8260d10d39b974503f4dce3327cc6ed67d5a38330f2ba6fc16e0c48dd9540977` | docs(recovery): append 135-PR live inventory and NO_PUBLICATION hardening |
| [C090] | ab74033142bc5bbc2983aa4cd1aefc166a93bea7 | EN_ONLY | `8598ee3cc2fd9dcfc965d82a62224c32021080ae4423ff6514082d7b85f45842` | test(publication): validate fenced NO_PUBLICATION reconciliation |
| [C091] | 70928d6832162c89f24a52dbb62220dae8e508c2 | EN_ONLY | `d745586c7b2402595853a0b7f343f54e1f0820a16a8655dc2c6bb65bd418f4c3` | docs(recovery): append 133-PR live inventory and latest follow-ups |
| [C092] | f262cd17c4a8ee039f99a79d4fb2b25b54128e67 | EN_ONLY | `7afd2b7f043d2d3eb1f899d52e350d04cd2a70503878a8357d2aef40681b7539` | test(publication): model positive NO_PUBLICATION reconciliation |
| [C093] | 9c4da591fc70b95ad769b33471825ccb96cdc4c7 | EN_ONLY | `8b60781149200ec203ef0e084faa8ac5229e865c8934d89c5af81937aa33fc01` | docs(worker): correct diagnostics evidence classification |
| [C094] | b9952f7fcf47db054e5699fecbb607b4cddf073f | EN_ONLY | `86d458031aa450c018959d2659c30e430bd1b64a502b0b7539ade0680a1c18a9` | docs(governance): record integration continuation session |
| [C095] | eb95fbf0ca563c950c3308a15c3e3b76eb2a0060 | EN_ONLY | `41f4c584498ac888afe049f4685b5d811ac1ebab4aa2b23e5e4be7390f8bec17` | docs(recovery): append 129-PR live inventory and publication follow-up |
| [C096] | 05fe0f9551ef3149d1c54b6f3a5e2f0ba6672551 | EN_ONLY | `b1e13fcc6a5f00cf96ddbf3d95e65c18dee71c1bd55f40c6136955fcab5bbd4b` | fix(publication): block recommit while operation outcome unknown |
| [C097] | 4f6d863bf245895b577c16ddf55aa9bf28f66d24 | EN_ONLY | `63061add2798d3e6660e77d949d86c8a95a7654e106f743ae538b14c5e51efc3` | docs(ai-dev): restore AID-2026-001 session traceability rows |
| [C098] | 962df750b07fe5e88f6f904abde9fd1a4c6ddfc3 | EN_ONLY | `da584cc2c087e43dae27968b5b151752c5e4dadf3004a17895b622b2aa52188d` | docs(recovery): append 125-PR live inventory and AID-2026-001 follow-up |
| [C099] | 9bddaf72e71b1826b22e013523bc19be4315f097 | EN_ONLY | `a5320d49314e6e921e9f3a748b5b8734e7181e34b0ed0528348daecf2fb8aa87` | docs(aid-2026-001): record strict manifest validation |
| [C100] | be90d5c5d04dab65123f53a153cadd562242daa1 | EN_ONLY | `5abee883ec85ae92b4f3a71f24681a58d6cc73f0b7be114e5a4a3e4637e6bdaf` | fix(publication): bind idempotent replay to immutable operation tuple |
| [C101] | bc6ab890aea68ea33f4de42e442d7ac22fcbf26b | EN_ONLY | `880769dd9170d33c9a5c3986d970f2ebae61c326ca7148bf5dcddfa4d398bb66` | fix(ci): reject duplicate YAML keys in AID manifest |
| [C102] | d38c8379392e56fa095ad7577e96c46b8ff202f3 | EN_ONLY | `98aafbf55a0b96187b973ff597d6f6df49a2c848a257f8598d91303653847c3a` | fix(publication): enforce fence-first admission ordering |
| [C103] | 56336bd16b4dcab1b600eb7ab12e171fda0553a1 | EN_ONLY | `13dad02496c5954e553b870ea5d46f1b36c5a6a7d1426a2b16264ae699779298` | docs(AID-2026-001): record PR #141 evidence and current R3 blockers |
| [C104] | 31a48f53b85929482ec1ef39a9ad2b254c64af00 | EN_ONLY | `03a09a3605048879245183eceadf7696d42d7fe585269807e60519d6278a644e` | ci(publication): run publication protocol reference model |
| [C105] | 4aae0a10aa16ca19de001153eb4dbe630f4d2054 | EN_ONLY | `90021207b21c0d9079ed99ffda262122dd655b1d51f730655021b4d7b5d14ad3` | fix(publication): enforce fence-first admission and preserve in-flight barrier |
| [C106] | d3dbc5321ccf97429b3003b19a28d8100330fda9 | EN_ONLY | `e22d83f916188f0ba37ec8c1928018cd4dd325348585c1ce54fbb0c8174534e6` | docs(aid-2026-001): record engineering-phase implementation deferral |
| [C107] | edb38a6fcd0ed46aa99641cc574d4860a86f644d | EN_ONLY | `28cb53dacc125dd988878fa33a2f8017ef823804d743e3e6cbcbd4350e649dff` | docs(aid-2026-001): pin model blobs and clarify engineering deferral |
| [C108] | c808abd2b63da9cc69ad4ead3a7a03e1fb7bf6b2 | EN_ONLY | `09a3a51fef2ab33b4ed33b6635b6e53fa213a86063ff33be31416f010f83509c` | docs(aid-2026-001): place continuation record in session table |
| [C109] | 8c05c858567171c6e1ff14be8359e1d11a50ec09 | EN_ONLY | `7b43fd871907bd49451097bf753ba65b8e7956e75445b4605930c17e81bec475` | docs(aid-2026-001): place session traceability row inside index table |
| [C110] | 797d0e278528b8b5e390573a93e7892edfe30329 | EN_ONLY | `9975e6063e6cdff7648bca5e87604a40fb1b1e3504330f2dc1d96e0f8d7042b8` | docs(recovery): append live PR inventory and disposition overlay |
| [C111] | 35631c376396dfb2647bf0b09e8476c5c8c7f726 | EN_ONLY | `97c844c14a1c7e74832fe98626d3dbf6618353dee24760c219c3d9d550812c1f` | docs(recovery): correct bilingual snapshot labels and PR138 head |
| [C112] | 1da0b89d306ee0fc7d76226f3990839aaf710731 | EN_ONLY | `325feb214dc3b2629acaed1ef62861468a1ac4cccb677a4a244928de7c83c687` | ci(aid-2026-001): validate full manifest YAML and required paths |
| [C113] | 599166546aa36cda46c19444cada45503e21e570 | EN_ONLY | `1b0d82736607d55da86f262fa1c43d4e314edc77fe9ebd94182c97b9d5986567` | docs(aid-2026-001): retarget specialist review handoffs to immutable current hea |
| [C114] | 926df420bdd8ee82a7caf0631400541912639c84 | EN_ONLY | `1b0d82736607d55da86f262fa1c43d4e314edc77fe9ebd94182c97b9d5986567` | docs(aid-2026-001): retarget specialist review handoffs to immutable current hea |
| [C115] | 37fc2c252d9e6751310cc7284041bf107e4dded7 | EN_ONLY | `1b0d82736607d55da86f262fa1c43d4e314edc77fe9ebd94182c97b9d5986567` | docs(aid-2026-001): retarget specialist review handoffs to immutable current hea |
| [C116] | f4245271963f26ee42875b46f50ac2dd321e3fc7 | EN_ONLY | `a1fdf729d9e4ec2b2230d8f107b322e6e34e409ed9b9e41eb51744c14a6f17d4` | docs(aid-2026-001): trace continuation session and PR141 merge |
| [C117] | e6c574a4bcd795906ad84620a97fa2a353d462b6 | EN_ONLY | `517581d0089844252086f434d78f8085ff93ab8d54ca2747a3606189b88a0c77` | docs(aid-2026-001): append PR141 execution and preliminary review record |
| [C118] | 169e2f3799bb6a0a3c5dbfd79eee00dcd077125e | EN_ONLY | `30eb636763508579647e6baadaaf0ef9fa7c8f4d82f2e4451748548f7538d699` | docs(aid-2026-001): record PR141 model test evidence and gates |
| [C119] | 7bd425de62fa2dc66c2d2df03fac58e02bb68ad5 | EN_ONLY | `6d030a19809def62401a6d491e5d51e5c00a385a1b3e1a8a5ccaa347f19b39ec` | docs(recovery): correct PR-RECOVERY-002 verdict factual parity |
| [C120] | 41367e8230cd906ce0548df37bbb77027b26124d | EN_ONLY | `0046ed50ae6553bfba7317a2035c5a0a6b95dc77bddafad0f9bd433350baf98d` | docs(governance): mark PR-GOVERNANCE-001 adopted |
| [C121] | 69c43ae126353616d64b66d7abc8f159219c1742 | EN_ONLY | `b09db3c502a732af2802a4198f4e420f52fac4f1d772adc779124e88551e1ba4` | docs(g): record Applied reference-model evidence and limits |
| [C122] | 9edc746c001f1f82950edad7ce130342db53ff67 | EN_ONLY | `6c441e64cb2d62606dfde8859c743ef4f5c59c7c5d22d4dd905ab7562e3804ed` | test(AID-2026-001): expand Forget reference model coverage and add CI |
| [C123] | 48db716c8053643ac328da212cb89a28ecac6bcf | EN_ONLY | `9be2258fb9c94d28f60846a98925798a717de7ee87bbd74b3cfe921d119a7141` | docs(g): add Chinese mirror for Chinese G contract |
| [C124] | 3d2aaeb87f0cdd30fac3558abc6fb9e1e6540238 | EN_ONLY | `018aedb06f2b043c87608c73d980cd5b87a2f05f662e79436bb87cbcf770e669` | docs(g): add English mirror for Chinese G contract |
| [C125] | d42abe86adfafd1ba17c5eca76eb2341cceb45b8 | EN_ONLY | `9a78531721e5cb8538e6da259a89383ed0ff78c432ef64e4a39f08ac1e089ba8` | docs(g): finalize paired reader summary traceability |
| [C126] | 664b4296412cd35ea9248a9ee7a8f4213c01ba22 | EN_ONLY | `9a78531721e5cb8538e6da259a89383ed0ff78c432ef64e4a39f08ac1e089ba8` | docs(g): finalize paired reader summary traceability |
| [C127] | 8e1ecbb25861f0fc17705d9b41d8ec3670c070bd | EN_ONLY | `9ae6746189dfe152b21c7626e8d91de30d4b41c390931a937a58cbbbfaad616c` | docs(g): add Chinese reader summary for Applied contract |
| [C128] | 557ff34bfcdc79784762e5008071a8293b7b207e | EN_ONLY | `cac61dc41216ad150388d8bab99f9e1b26fb6b948865ff04dc3d01119a95b907` | docs(g): add English reader summary for Applied contract |
| [C129] | 3754d049db840b049728afd814faac968bf10749 | EN_ONLY | `c42050da171156b1e44f03ae505074a39eb775729370acd4476d3a8686df2823` | docs(governance): add PR-GOVERNANCE-001 merge evidence standard |
| [C130] | 266d622be088c0707dbfde989a21f05d759b393d | EN_ONLY | `9a951f111ffaac6148180addfdedb0de2bf1824e071fcdc40aec258b3fcf60a3` | docs(recovery): correct PR-RECOVERY-002 final dispositions |
| [C131] | 23134a3365092bdcc00adc2080f4e00b940935e5 | EN_ONLY | `f79945f7f2abbb6c24068fc8f0b213f3b251047783ad7c6c77ba3ed5e7b1620d` | docs(g): add Chinese Applied reference-model evidence |
| [C132] | bf80d641665e5490aaf7e25458efb7c86eda393a | EN_ONLY | `5f92235d1fb426adbde1a8b09ead6d7b9c1155c86f9830debb24bed71827acf1` | docs(g): record bounded Applied reference-model evidence |
| [C133] | af3b0380e35a5834f8b5cdca92dfa0f8fcd8e1bf | EN_ONLY | `1ad27aaea692a68bfaa12dde060d4e92fefb31e4254daf61356e04c08edc7e66` | prototype(g): add executable durable Applied ledger reference model |
| [C134] | 7d63b9fed5c9905bf092875b8654c3f0987eac07 | EN_ONLY | `97e4d0c897eb1e830ccb5248e4d65ffdcad30aef80ed1e9dab6f4e26a32a5281` | ci(g): run Applied durable ledger reference tests |
| [C135] | f5ae7635f4de38d807bbc19e2a8e5ffe2c81b277 | EN_ONLY | `b56eaade92561578922c47ed7f37c79e5445308821a767e521323dd98032e0ed` | test(g): cover Applied idempotency and restart semantics |
| [C136] | 8e1794e16abb3fecf78651c80053e7abfec2ad1e | EN_ONLY | `0803469516fb22cb2d1f46c9e35bcf0b9310ba0d4d4ec90e547ca22998cc011b` | prototype(g): add durable Applied ledger reference model |
| [C137] | 8b9d896d714e6037a7856a77a9d2d3ec0179f117 | EN_ONLY | `cc68085c1bd222ff6046352a86a8f542d116d07661651072da0a3690496df600` | docs(recovery): publish PR-RECOVERY-002 full inventory and closeout |
| [C138] | 5ad451d1d2164c3e72d56c9bb5eeeeb388f8ecbc | EN_ONLY | `ae06a7df6793e7de0e765d63b7987103f2de3d81e52781b55766169ccc410ad2` | docs(AID-2026-001): close out PR 135 integration session |
| [C139] | fb9269661225a26416d11528e9a94d845345b2af | EN_ONLY | `5dd599fb3ed7b65f1de7e416bd4cd33cfc08e89c1adfa3fed64701e173b9c6de` | docs(AID-2026-001): refresh current mainline reconciliation |
| [C140] | 43203675389b7cb351587e465ab3acbb6e165efd | EN_ONLY | `beda43b5bef9e6936c1994b8e6a72e6a8f394fb7a5d498e09a7bcb2a2fc44ece` | docs(AID-2026-001): reconcile merged PRs and current R3 gate status |
| [C141] | 5bdb88f234eacae98aaa57f987cc7f71e3391768 | EN_ONLY | `1e3667f38e74f3583fe2e8e0f431293e71d812462e58b6676bfbe55ca98f2222` | docs(evidence): correct H Applied 29-test CI status |
| [C142] | 1cdd5a5b23fe942e35b890657546c429de8826be | EN_ONLY | `16162c4a8fd58f60e3e427a44d635588df6b0ebc8c904f54ee59add917d54c70` | fix(protocol): bind H Applied evidence to resolved C outcome reference |
| [C143] | 7f77cc3e03a0185af75e04268ae34d3f586d4586 | EN_ONLY | `f095168fb280cbc3c770406a5e25af258a928b09e42cdecdcd338bbba4c30ff3` | docs(governance): finalize PR 132 session evidence |
| [C144] | fcdc252f01bf96f9bd8fa215991275ddce64c65f | EN_ONLY | `a227fe20bc12721445b12e86e8c0e9adc8b334728e55cbf552fbe6057f2e8ecc` | docs(governance): close out merged PR 132 traceability record |
| [C145] | 6b7c864e65453f8e8c9f5edc02c6fd937f13813f | EN_ONLY | `c03d321f85b12997cd905bb2f830d8933887ca8047a4087b297c8b7722aea2b3` | docs(governance): enforce session-to-GitHub delivery traceability |
| [C146] | ac4558ce7a78fc8fb27a18d0c06033e3a48f6fff | EN_ONLY | `e2450d5eba09d1f1093802a0302cf12a60cbb26d0a39b3ac854640a288f1ff8d` | feat(protocol): publish current H Applied Evidence candidate |
| [C147] | 8d443f26d659e9767000494de535ceb8b9ad6d84 | EN_ONLY | `a5cb796faea8a07af31971d903e5251b6f1e139bff1cedddd586841f7ec09859` | docs(domain): publish refreshed cross-owner source reconciliation |
| [C148] | 35b041b6344664b3118cbd8fbdf5be15a90ab3b6 | EN_ONLY | `681f1863b98e5be040346d6df55580ff0d6e5eeb00f81ab39a7a2e0dab95519f` | docs(architecture): correct H Applied exact-head CI evidence |
| [C149] | c56fbeb78d6603a84f358429a59945a51c3b00b9 | EN_ONLY | `fe957d470ac4623b6af87f9256eac4b9c022e280b306656798f84b976e040658` | docs(architecture): align H hardening disposition with passing CI |
| [C150] | fb03fb3234fd8067366424315a9d948b9de184d4 | EN_ONLY | `87199c921277af9e400b717b52509bfe2c8ac3a091ba3f1fc5633798bf4936c3` | docs(architecture): correct H Applied exact-head CI evidence |
| [C151] | 960e27d9a4e2847eb39ae9ef2f2a9c9d56f2d2f1 | EN_ONLY | `048ab4b0eddb2c9b8bb4899423caca9d809a63662795f6aa4b7cf9effd3c2ca2` | docs(architecture): refresh convergence currentness |
| [C152] | e8d5e5e374627ac0c472d2bb179e8e940cc6a6de | EN_ONLY | `fee96d0192bf33a3ffd4afc0c417027b7b850d15003db99646276d2d491b9597` | docs(architecture): publish ARCH convergence currentness addendum |
| [C153] | ab1fa87d74ca4a632155aa19569533ea560109d5 | EN_ONLY | `f79d84c8a641eca4657d562e9bef63bf253153ae91e63945a317bbabdd933b15` | feat(protocol): publish H Applied Delivery Evidence hardening candidate |
| [C154] | 6c325804027b88de1014ab3364cdda7e0c023ba6 | EN_ONLY | `65f04a7fb4e3b16fb45602e8d4d491b18c32f40137b14348847851d5dc5896ee` | docs(domain): reconcile PR 55 post-merge research gates |
| [C155] | 431468a9066f6fe68d9c514f3603ab1a603146ff | EN_ONLY | `066efbabc468662337f8f6ac4025a0e527a8c3e4f32a054f2ad9e9dbe015d094` | docs(tech-reality): publish C/G/H Applied consumer audit |
| [C156] | a2b8babb1cacfcfbcd590b147bdf34ce162944c2 | EN_ONLY | `83bbad28c19045f204f507995c5c6aea4322fb272cc40bd836a196bc5ef76483` | docs(recovery): audit closed-unmerged PR content disposition (#118) |
| [C157] | ffd756b8465a74bf8cc910d70c16edf47eecf5c8 | EN_ONLY | `07b2eee4e016235cd18abacd5b7e1bb76916f005a13d7a53cd9f0a486a6cd32d` | docs(architecture): publish G Context package metadata |
| [C158] | 6faa3b038c02bce27b3b4443d6f1be95cf5c5beb | EN_ONLY | `8ddd3ec4a5d95bab68cddfee370761a797e3aa7a76c5f039c02608d70664c742` | docs(ai-dev): publish conflict-free AID-2026-001 governance artifacts (#116) |
| [C159] | c53da8bcaeca25c99dab722d29b3eea4814d34c2 | EN_ONLY | `2e2c80d6d20588c59c3f9f03d26efad1e1fa8010bfa8819cc3b70f913f385af5` | docs(context): publish conflict-free Session G architecture artifacts (#115) |
| [C160] | dfb37ab4cb263f399939da7fd99f8e98b5557979 | EN_ONLY | `49171ebdb16809d3b4ae4384d6f14a00a809dfbdc1f151c122eb791f96c39162` | docs(tech-reality): publish Owner A multi-owner remediation evidence (#114) |

| 编号 | sha | language_state | msg_sha256 | subject（first line） |
|---|---|---|---|---|
| [C161] | a6300b91e160a900620fdd2f32950e74bacfb98b | EN_ONLY | `826f1a7fb2b5e92bde96cdea327ed9983e3779b8966ad9e72b7f274d7b27eb5f` | A: H 1.2.15 validator, CI and trust exact review (#67) |
| [C162] | 974da77cfeca556a0b6df3c63f392e8ba528d6ee | EN_ONLY | `36537625079d51e5c71c43a6a80596064966d00c8d5b00843a1b50eb80a67699` | docs(A): record H/C owner branch tree integrity blocker and B-02 reconciliation |
| [C163] | ec44e8a962274b5ef07704cf9f72272db029d8d1 | EN_ONLY | `917939158a79d9e2d0c88f0bff15e2a387da290b228d8158707e97b96f8c8447` | feat(ai-dev): add bounded Codex Owner worker pilot (#36) |
| [C164] | 43b76350a7d654b3d0a3602c51ae7ddce7c81af1 | EN_ONLY | `14a09d13c0b7efb2d35e932f318cae3606c472ee3a4b2cd2c7bccbfa56162ccd` | docs(ai-dev): restart on ChatGPT-native execution model (#42) |
| [C165] | e72d03d90166c89273288aa664a934640699ab0e | EN_ONLY | `db19ee09ab202bba25d7b9aa3fafa6e8ac0868b526ece187eb0edbe38b7ccf5d` | docs(review): publish H Applied Delivery Evidence exact review |
| [C166] | f77f8884963bdc0e7bd1f15c8e9d4200b77d755f | EN_ONLY | `67976c8c0baf0c679ff962764e0e7723b74ce3bf1b4b71dc8e594a6aa6a2550a` | docs(ai-dev): design event-driven Owner Worker runtime pilot (#31) |
| [C167] | 18e05b4cd27a5d8096ab626673a8e555495f1e35 | EN_ONLY | `7e778f9c4a6256e0b8ff5c323a1bdada705d89c156346eb94d98b63d39bf000e` | docs(review): publish B-02 multi-role remediation review |
| [C168] | 32a35f422ba6442d1f700cfb327f348c0740a7f2 | EN_ZH_MIXED | `71bd2eb239fda47899d641cf9ee6002bbe483c48305d71b3e8a9ce1004aef7ea` | docs: expand bilingual architecture specifications across system, domain and cor |
| [C169] | b8b0f3d4eeea940047e1354d2777f213ea57ab5e | EN_ONLY | `c8644513aea05e618c257288e627403e163c43f947f7367c358d734b28f3ba52` | docs(engineering): add Session 3 root-first engineering planning assessment (#46 |
| [C170] | f3f85497f3d9c3dfadd175e62ba2a99663388b27 | EN_ONLY | `e689a5ba196b4c9a20f66d7e18afac2d286efb70755c8803a5551bf230d56d5f` | A review: B→A protocol convergence and Storage topology (#52) |
| [C171] | 2c1a25e81c7cf2c3e091f7c57fe89640388c7c7c | EN_ONLY | `c78e3dc9e0d71d740d2ec0bb8ac9a9b5447e5f996f33b7ddb52177679eb0b085` | docs(review): add B-to-A currentness reconciliation (#59) |
| [C172] | 022cdee78e4c9833aadc41be5957fc5aedc82248 | EN_ONLY | `f86a71678b8e4a7ec3415d6e5f5bd3e5b464fa42d2d0f01f5f3eb57a1c845979` | docs(review): record B-02 C/H 1.2.15 successor delta (#61) |
| [C173] | 59942f4a0ff1d5581260655f9e34838ba9ac880f | EN_ONLY | `d96e23151365999e6b6a4cb506b7b7af18dfe394c96b1eed9fb8bb37153cf395` | review: refresh R/X/F/D/P assessments against current main (#62) |
| [C174] | 47e6de8167d9ff76b23f4d062891ec40ef613c1d | EN_ONLY | `bc07e0679218062860c0296375a2dbc46bd07fe471b7b644febccf8da8b6202e` | A: G1 current-source and evidence-freshness audit v1.0.0 (#63) |
| [C175] | d4a71fa7d2145722fc73dbb7c355d555f0a29ea0 | EN_ONLY | `188166e1557b3ea65d22038bbeed30e77e8880a06ee3f4a2a95d3dc307b574b0` | docs(review): reconcile B-02 H/C 1.2.15 gateway join delta (#64) |
| [C176] | 2bfe1fd453653eb2c57329ab6c886650e6153f03 | EN_ONLY | `c173b385c3135ce6c55c12fe7899d50e1fc10e57844af5cdb8c28f945e9447a3` | A: R/X/F/D/P current-source refresh v0.3 (#65) |
| [C177] | da08d3e6b04ac6e8714a988bc7549bd4574a0fe4 | EN_ONLY | `38fbbb193b591d17150f7f83a2b5ebe761034c0dff4a2bad06c3178107cfaef4` | A: Final architecture engineering assessment — current-main conditional governan |
| [C178] | 19ae5ed2b7a0ab613f188a4dc8e75e4f5bc81320 | EN_ONLY | `9ab7317b056b867144b9ea395a471d10ee83309d973d15534b7e856fc8440370` | docs(ai-dev): register persistent Ubuntu worker endpoint (#27) |
| [C179] | 07ee5702cab0d12d6136fe3c024bde9a7af44a97 | EN_ONLY | `9d19c69c17bee93e5c47e298eab6b96ef91d765dcaf4fbaa3293910b7e453900` | [DRAFT] docs(domain): DOMAIN-REALITY-001-B canonical domain research (#55) |
| [C180] | 22e64ef2df60b4c2b022885aa3a50f12490b8f36 | EN_ONLY | `ea53143623109975814b3c5601566cd1e1218cb2a7577d1a9ab7e41c00d28ed6` | A: H branch baseline integrity incident and recovery conditions (#90) |
| [C181] | 6939a10b8de0f637d2c49e7c2cafa56b7f583eb6 | EN_ONLY | `97f1c50f4531a8eba6ff10e48b950d33102da85d71653dee0ef3423c9554e3fe` | A: minimum engineering slice entry contract and readiness decision (#95) |
| [C182] | e6adb447911403bd319ee8a9f7bc9014180e1d81 | EN_ONLY | `f5cd01f0223cfb3a038c5ad8c704cc2bbef338d5dc0840908b1b43021edf5e3f` | [DRAFT] ARCH-CONVERGENCE-001 — cross-workstream integration synthesis and advers |
| [C183] | e571a0f69b22ff5f565286981de839cd8eab515a | EN_ONLY | `99650f881090a37028356b0889988719ea942ff82db6af3cccd8a4208f73657e` | [DRAFT] ARCH-CONVERGENCE-001 E — minimum runnable architecture and roadmap (#106 |
| [C184] | b0acc289663d99797c7b12ae60ce97b80266ea41 | EN_ONLY | `6fe616dbd9f18b01a6d5afd55a5fac46aa53b09bee740d4f78473f44f27c9e6a` | docs(arch-convergence): define Context Applied runtime contract (#104) |
| [C185] | 2118741fcad6bcde2c9bcdfd4dbecc42403df252 | EN_ONLY | `1c5a6ac041b9ab68f5425af30f5218e8595fca6afb1452ab379c049ebf3b1722` | docs(arch-convergence): define Forget authorization and recovery safety contract |
| [C186] | 4e3cd1556b7ce18118148a87409d0e9c0343acd0 | EN_ONLY | `815e976759397c18fe1986f5e561c1f077a635bed17e9e2adb46c0cd1c2bc61a` | docs(arch-convergence): define conditional canonical transaction contract (#101) |
| [C187] | 9ebcfaf0a76a9152662a18d8a20b9e299a348cdd | EN_ONLY | `46cd6ae7411d61c79e86f216ec89c75319b8a1dbdc7868d932badf5de58fec8e` | [DRAFT] ARCH-CONVERGENCE-001 A — source-of-truth inventory (#99) |
| [C188] | 7fdccb9b3d9bf3f6337b3ffdcba29185dbfd56ea | EN_ONLY | `1d9932309de8a6edc8f720a7e3b06a8ca79280f572088e78ef2f60f7e2fc99cf` | A: exact Owner source refresh and Gate disposition (2026-11-18) (#102) |
| [C189] | e974b10f0ac761e9f85513059db81d249fa9876a | EN_ONLY | `4d50a5682e7dcfa976768af37a299577656861a0bf750997803665bb12912aa9` | A: source audit of architecture breakthrough integration PR #93 (#100) |
| [C190] | e153bbb1986d44b782d0c0e702e9699490f903ca | EN_ONLY | `cca7e27ae49f3b631d826426b50f2de8749f97b5b396328ae4c841e41431f30c` | research: integrate architecture breakthrough findings and cross-review (#93) |
| [C191] | e08391c68bfd0dee521596c295b753027d3059f1 | EN_ONLY | `04224327c4afa195cf13918a1080dfc5d64d8f0ba81b26689a002cb755bd7f6a` | research: TECH-REALITY-001-C agent integration and inference boundary (#69) |
| [C192] | 3218806e5e18d1ec00aa6f1140f02148eaf34354 | EN_ONLY | `344b2dd26341075743524550217cbd8e38611a352863bcdac73b4258b72cfec0` | review: independent TECH-REALITY-001-A technology architecture findings (#56) |
| [C193] | ce50865d6e578f88e5bfa6a4310415b6569786b7 | EN_ONLY | `a785467e4343a72d06e11f967c2a67201c20019dd9b092f3634b02c1be169c89` | research: TECH-REALITY-001-A technology feasibility and reality review (#45) |
| [C194] | 59769e109212eda813c75ae538bf8a22b9c4a222 | EN_ONLY | `2f100fde73c663ffb922bed18167379a02d9a0e7ec9e54b1f5f9c096011b4f35` | docs(research): add PRODUCT-FIRST-001 unified integration review (#89) |
| [C195] | cbabaa05e613f0e2d0b364c7b8280cb052f2e7d4 | EN_ONLY | `c2a432da4f9572b97105fa91b772c9153aecdb1b185878db852ba13a37622a88` | reviews: add Forget protocol bounded formal verification (#88) |
| [C196] | 707afd2164872df93a2e0fc917514ea1608420fe | EN_ONLY | `57d43784c9ed7e404572ccd9c7a9c98fc70748709432d175f93920f2043b9749` | docs(a): specify B-02 issuer state machine and correct owner evidence (#87) |
| [C197] | bcfedcbc008a4ee1c5b48f9c9472b1264a9ef9c3 | EN_ONLY | `8bac6b4e374f59675d8f96b294ce24c8a8e0f46fc28318786bb31f23b01718dc` | research: Memory Operating System architecture assessment (#86) |
| [C198] | 0d8f57c4beb9934037a8e4f3932b89bc3bd14d0b | EN_ONLY | `bab8ed33f5fa2514b0ad89b716acda45d5359a6e4cf67217c1b82c0afe8d9b06` | [DRAFT] Research: Memory IR and Compiler Architecture (MB-IR-001) (#85) |
| [C199] | e56ec6931939834dec2599e155926c95ca87cf81 | EN_ONLY | `4836e7d5b3d0720df1b00f53cbc3a7902b626a1cd7dbceeaf743bcc380af6c6e` | research: architecture breakthrough study — Forget model, Runtime resources, Mem |
| [C200] | a0ca511de4e548ae293314e73f3e2b49392b866a | EN_ONLY | `745612fbefe01f96ced57a21d11e727efd7822d0601d025d306f3ba797abab66` | [DRAFT] research: Architecture Breakthrough coordination (#83) |
| [C201] | 84dd459b6fc0f01c21f72f91bbb11ee5d798cf3f | EN_ONLY | `059b5192d39f398a210ae2e95d3f8da60be47bf5559825f23d9d0d7eed807ba5` | research: add PRODUCT-FIRST-001 Session 06 simplification review (#79) |
| [C202] | 507aa874b1aadae3d10a211604857b9cf92286d8 | EN_ONLY | `ed2cc74a1fc38676eabe1e5267a22f5cd866558549a93da2c597af28a8bbeeba` | [DRAFT] research: PRODUCT-FIRST-001 session 03 storage and search adoption (#78) |
| [C203] | 3e5ef62b2ebb3743709b7cd9d3f9e375fd465989 | EN_ONLY | `fee91c36c58500f076fd62f65929f3d1d7e679778795d6c5f3de5f847ef40929` | docs(research): add PRODUCT-FIRST-001 Session 05 agent runtime adoption study (# |
| [C204] | 151e332e292433c76b0728cea09bdfcf9a9a2fad | EN_ONLY | `79b1e6afb0d2b765a34085e08d038462aa729c2e15c9dd83955155bd128f9035` | docs(research): add PRODUCT-FIRST-001 session 04 security governance study (#76) |
| [C205] | a8c6a03d61e325b46582bef53a4d135a5195f93a | EN_ONLY | `1946c10151d468af453617bec19bac261844e88c4651db2fcb00d0a3f4e28c29` | research: assess durable execution product adoption (#75) |
| [C206] | 5f6f789f7f79d4619d80e06e40b71ecb10ca2033 | EN_ONLY | `d211db4562c37c8bd8aad68f2082601a1c94743ec40a96f12eb8164bd8017099` | research: PRODUCT-FIRST-001 Session 01 memory product adoption study (#74) |
| [C207] | 8d8ef80daacff90947f9a354a693b13c844cddc0 | EN_ONLY | `3a4b0fca01231dbba8b1be96685b142708949971647f20396294962a0d354651` | R: Principal System-wide Architecture Risk Assessment (SYS-RISK-001) (#50) |
| [C208] | 631081aaf13b7fc0f67f3b52f87a605f01e4d749 | EN_ONLY | `3dcc82d30fde922a21d0c866dc4b5e2130af5467c51e1c7b1693792d64d009ca` | docs(complexity): add independent bilingual architecture complexity assessment ( |
| [C209] | 0462b4a3a4a5249d1e379aeaa24cbd84de505144 | EN_ONLY | `f2b33421aed7f2b7bb3e39f63fd606ce19dbcef4b1b3377028f8ea9f46e916a6` | ARCH-CONSOL-001 Phase 2: System-wide architecture consolidation (#44) |
| [C210] | 7ea8b8517b395db45727cd24cf545c72dc436435 | EN_ONLY | `8dd5a879580deb3a772114d63897ad419923ea675cd72c7518e150a92cb85767` | docs(recovery): PR-RECOVERY-002 baseline, inventory and first triage (#105) |
| [C211] | fc03ce60ff9cd5c23f62dcbbe2cea5756f610f88 | EN_ONLY | `4ed2586312e6833b5db23a94ad0c950ace9378277814b7e8537e24350dc0ad7d` | rebase(Session 3): refresh research report onto current main (#111) |
| [C212] | 4a0acc1608f0909bafb64ac90f0a724b8223d546 | EN_ONLY | `99309ac75afed7629ba36d0665262ca829827ca679ed7a82b3f5bfe005d680cd` | Merge pull request #110 from oahcom/research/ai-dev-os-001-session-4 |
| [C213] | 5f42acb1391a06703f9aa1a7b615f4dd62d5cbea | EN_ONLY | `db39e41c3a94962db0cc25f6c06300cd124083e66c29ea23a832c408e326a49d` | Merge current main into Session 4 research branch |
| [C214] | b450c53956a7e11250aa0fea51676074f0ee5c1b | EN_ONLY | `a211281a8405926607fe2083bae2e9f4fa3e9ea235e5d7e1d71558adc8327617` | Refresh Session 4 baseline and remove account-specific plan assumptions |
| [C215] | e10cc49e9b7cfc46e30e85d67ca20a8cdc4ca60b | EN_ONLY | `317c888ddcd03aefe771024d221a220cbd5dbc23f910d9d7b35b35291c9f2fef` | Remove stale account-plan assumptions from adoption report |
| [C216] | 878baf8a6ce675d41cfab34282e4ed9b5984370e | EN_ONLY | `9d961d91a6a9355552a7ef193cc8f4f20f5762a53b070616587604aa4f1fc757` | Address Session 0 findings: enforce Issue 41 execution boundary and distinguish |
| [C217] | 4bee3e886cc0dec4a8d03817acd180ba979f8ceb | EN_ONLY | `845131d38441159a2106938b910f82cbcc9192a2d8142e12292cf4e875a337e2` | Merge PR #109: Session 1 GitHub Workflow Research |
| [C218] | 98fe7235fac8013b00ffa8a129d0f8fed830acf6 | EN_ONLY | `d7907a623a8a45e0e9890d4025b3133c43e6bc22ecca28e638b151055c5ac1ef` | Merge PR #108: Session 2 Prompt and Run Provenance Research |
| [C219] | ab6b5c204faa9f5ec686ea016413db73fc45a7b8 | EN_ONLY | `089963c99e66a400816d3ff4ef5ef67f4ff552723c647d6531002e0567f43227` | docs(ai-dev-os): publish phase 0 session 4 research report |
| [C220] | e9dda0d8d3e62d7d370892e032cb18a77872e233 | EN_ONLY | `d292f69f34830f52380a7ea99d84c26c5a3df23913058074e80a79d1f2dca24b` | docs(ai-dev-os): publish phase 0 session 1 research report |
| [C221] | 2d219492c0eb53ec4c7bde800f617b177da6f6b8 | EN_ONLY | `60c457997c5a16508526e3a1f7a9a4818e34e984efb5358c9e47a8f9bcfa4479` | docs(ai-dev-os): publish phase 0 session 2 research report |
| [C222] | e52594f181d2edb77448adcfed64a0fbdffaf3aa | EN_ONLY | `24e995d6e6f23ef88d611a6a9e25080464e46c9dfe9dcb036eedaa0ba11db5ac` | revert accidental A review document on main; restore protected branch tree |
| [C223] | 28fb37e21fa4ba2b871f7816fe669128618c063e | EN_ONLY | `38990d800c3a3cd7843f25fb90a6fa4c55851f39f78bdf9b13f0baf85edcaa6a` | docs(a): specify B-02 issuer state machine and correct owner evidence |
| [C224] | b3c666e67982cb3d3374e759cfb6552c7765aacb | EN_ONLY | `c2051fa0bf0b4d13ccdf9c9acf43284081f28d6be437e3ecd812494dfa3bdf5f` | revert(review): remove accidentally added R-X-F-D-P note from main |
| [C225] | 82f64137e0fef472db55088bc65eb0b82f9b6d27 | EN_ONLY | `5ff3598f33647c54adb4dd4861a4019534a04cbe2c12996061abcedb7172de3e` | revert(review): remove accidentally added A review note from main |
| [C226] | 0772736aab8e3f9ed58c3f5eaa64c7d8f1858823 | EN_ONLY | `b2605eba216c0d4fe46020b3c3599e4aaea15ffef2173b78f7ca2f63e4b37216` | docs(review): add Chinese current-main correction |
| [C227] | d754337ac70846688377c2a3e1e520ffadcac340 | EN_ONLY | `18550a283af6fa0505d708f274c730d48e637cf94ec3f6a7d5aa1d9a770f6ce0` | docs(a): add Chinese current-main baseline correction |
| [C228] | 901e38ba7b45ed1822eaefddc2da8d765cf8985c | EN_ONLY | `81ceaa5058a8f0f6c8711f6bbdac01fe6d0b4aeaaeab8a00893d9378775dddc5` | revert(domain): remove research-only bilingual audit from main |
| [C229] | ca69d50d1fc6c19a930128de700b0f2328bf32fb | EN_ONLY | `d5361d125e126ed468770d4ea164b8382ae0a8c38d0df9bdb2d4afa38198795d` | docs(domain): pin full complexity assessment bilingual remediation |
| [C230] | 8c0c5b11abf56a6f580fcf2a99c8043d3057da4f | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C231] | 67f1122e2ecad3bacd013871dde9a165f0730292 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C232] | e723222d38eceb9e7d0c7fe0827372cf2de6c966 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C233] | 56e4135c0b6de1f49c5165a68302e31609b357af | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C234] | d5c3795b40675c20034a59faa9654250e0cd11f3 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C235] | 145dd0620558a7f9bae3aab33fba3d98c21f4b79 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C236] | 99f4b12b7ef21954098cfea4b68af0285018de05 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C237] | 096422acb0270e5210d9c908d75755f42c55c902 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C238] | 1358aed9973a7c3a8bde3fe79106116c32510841 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C239] | fc2d5d4a6a25b3df85f7f707eebd6ad20b7a83c1 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C240] | 8a11e08264fc556b41e9f9b4ad61ff501804c8c8 | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C241] | bed1927e7ac1a711f1205cdbfd5e25f9dd5465ea | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C242] | 9e5123e36177615f6975d318f7e3747e86de1dfd | EN_ONLY | `60ab49c140b5bc3cff53bd66db530eeb52a2bec14acdf5a60ae78dd35c9bcd9f` | revert(domain): remove research artifact mistakenly written to main |
| [C243] | 052715487bd5e95aab8b9bb386c162cf2d6bf6d3 | EN_ONLY | `95a65043cf23ac92f40ce88cb563cbddc7ed9632a8e2196d21a1144ce28d80b9` | docs(domain): record canonical domain decisions and rejected alternatives |
| [C244] | aa6773fd44aed5301b0b357594954f1907cb919c | EN_ONLY | `4b1a8580400cdf1789f4b18e9635cf32bc4bccbe1acf2ff2e2ac9ffa9953125f` | docs(domain): publish recommended canonical domain model candidate |
| [C245] | 7c7a2bc74a0ad29c54cb92edb3f2d98eed0da8e8 | EN_ONLY | `5b6f552971651540834e50902cdc24ef58d86beab8fc3bf2f28f742cf1cf9a7b` | docs(domain): add bilingual canonical domain glossary |
| [C246] | ffe262b59aeb8f16d4d7c4e62ab2f4f5e7ef07a0 | EN_ONLY | `9cc97569d80ae9ec38d343371803740e8f297ec20bf1dc540ffeca231ee33789` | docs(domain): define candidate canonical domain invariants and tests |
| [C247] | 2b0dc111b13c5da19eb91de267b41145fb221e77 | EN_ONLY | `dba96a7bc63b9e8fe827f2d344507f57851eff318f2b6d0204e33be78c284bfd` | docs(domain): assess domain model complexity and minimization |
| [C248] | cb72bb4fd3a0ba4ff24de8687daf6e66c0684732 | EN_ONLY | `63eecfbec4cf1cce18e912bb8a09d38aa8287562c2ef9f17afc80bed600dd934` | docs(domain): define canonical domain relationship matrix |
| [C249] | f122fb2c1fddbc4e316a6fef609de7af2110a196 | EN_ONLY | `c995c5e494b30b7238c8de9f4818a18fece2b94a1df3a0edefd451283fe012a9` | docs(domain): register cross-owner semantic conflicts and gates |
| [C250] | 192d9412604d208f18a9227817664113ab007b3a | EN_ONLY | `17f2de943b49115b2618d2e2ac4123b66b2c7d4c6d5efa30e04e379e0d020c18` | docs(domain): add cross-owner canonical semantics matrix |
| [C251] | a67ef0a6361dc2a4771dcaf2e81d89a9c995c830 | EN_ONLY | `6c1f5b4fd9e29cee546f80e061a3d41534d6ff72f68aba78aa8abd32428c4c5a` | docs(domain): add mature domain model and project reference research |
| [C252] | 350df3f0bdcb05a1b26b72111a907af46b587244 | EN_ONLY | `e2fb07d31b120fa889c5928cf5ae006671efcf043987d5c41328b3b05a83d8a8` | docs(domain): define temporal evidence and provenance semantics |
| [C253] | 0aa8ec21db8055ef537ef40d7d6d3242fa99daa8 | EN_ONLY | `c42ed16dbb15133ed63416c61d2e3a5fd4667f23d45c85786aa238d8c67981e6` | docs(domain): define canonical state vocabulary and authority boundaries |
| [C254] | 6470f25ca23b8d35c06f60be2326867066418d18 | EN_ONLY | `73d61d020c19529b70528ced539e63ab8d941ffa07d1972676bab47c5bf01bde` | docs(domain): define candidate canonical identity semantics |
| [C255] | 141a44be4e01c0318e49c0875529aca621d2839a | EN_ONLY | `82c1cb5033d1237866dc6967872aef903e5bd83cf33115b170adc8a61a9f4be1` | docs(domain): add canonical domain entity inventory candidate |
| [C256] | b372b62c640a2b656e54b6db62a4ee67d7d8c001 | EN_ONLY | `14a865dcf857e23b18bed7152aec5f00775ad99ff6a57fb26ff3476dfc135046` | docs: remove superseded runner operations tracking row |
| [C257] | 568f632c1402be11e7bc13b4325c21a0de78ec41 | EN_ONLY | `89365048add3b92acff1276c534ddc8ce7f371459edb87881e33f4150ae384f3` | docs: remove superseded runner operations portal entry |
| [C258] | 81f2f050160a0d396b38ae46b2ae801b46e7caeb | EN_ONLY | `1eb06e590078a1c8fe3795172153b0196c2777f9a67489b81909cfa1b1e93e80` | chore: remove superseded runner automation artifacts |
| [C259] | 3148931ebd4d27438b0706d01ea88b7a1da4876a | EN_ONLY | `1eb06e590078a1c8fe3795172153b0196c2777f9a67489b81909cfa1b1e93e80` | chore: remove superseded runner automation artifacts |
| [C260] | c7a36832e0ec545b7167cd44900dc8d7b833bffb | EN_ONLY | `1eb06e590078a1c8fe3795172153b0196c2777f9a67489b81909cfa1b1e93e80` | chore: remove superseded runner automation artifacts |
| [C261] | eea6e603f4ca266e973ca886179f9cac5e71a62f | EN_ONLY | `1eb06e590078a1c8fe3795172153b0196c2777f9a67489b81909cfa1b1e93e80` | chore: remove superseded runner automation artifacts |
| [C262] | cc032eb76fded90e289ac74875a346f70d750570 | EN_ONLY | `1eb06e590078a1c8fe3795172153b0196c2777f9a67489b81909cfa1b1e93e80` | chore: remove superseded runner automation artifacts |
| [C263] | b0ec721d1663f78cd0dbc864a094f72ad1fa3ab7 | EN_ONLY | `a3e21a4552f7bd544cbc774e8aedd1c0beb21febd9a66a65ab69ab73442e9278` | docs(ai-dev): accept the deployed runner identity and enforce admission (DOC-OPS |
| [C264] | d0814623f79b4dc42c1833077101a3d84f9c407d | EN_ONLY | `00fa61190ed1fdb7279a681c24564c0e7aab61c32073d82707a8bfc435cbdf76` | ci(ai-dev): align self-test with ref-based admission and add temporary cron |
| [C265] | 9aaa3571a610381ec730f4b55b074b8e61e036be | EN_ONLY | `ab734d90403743a9b8da7d77dc6a8d1e30c1546cd864d5cf809ac22f833d5de2` | ci(ai-dev): add self-hosted admission audit and runner guard self-test |
| [C266] | a86e9c7ef0b3bef6154615e6149f75cedb6ff899 | EN_ONLY | `7489cbd4af85cbf2f21f27d5c79c0f35407461e06c1d16cd633c7f8bd08d3324` | docs(ai-dev): add bilingual CI runner operations design (DOC-OPS-001) |
| [C267] | 217b9fc18b0d618830ab5890f7292d25f1e7e5db | EN_ONLY | `0c1f288f5390a0bfaf2ea03097a90b6644d49507a2ed5f8e3a391c3ce33fc820` | Remove accidental non-owner-branch artifact |
| [C268] | fed4898f587b5ce283808ecf18aac73883930bc0 | EN_ONLY | `0c1f288f5390a0bfaf2ea03097a90b6644d49507a2ed5f8e3a391c3ce33fc820` | Remove accidental non-owner-branch artifact |
| [C269] | 7679799bee1f6c6406387de6ea295bf2016c329c | EN_ONLY | `0c1f288f5390a0bfaf2ea03097a90b6644d49507a2ed5f8e3a391c3ce33fc820` | Remove accidental non-owner-branch artifact |
| [C270] | 4bd0b3368b67af3ef31ecf2940fe11f7d0b50fcc | EN_ONLY | `28a097a95907028473ff5b3319539d9b8875fccd2a77955f1ca80bcd57b48614` | Record H exact-version review of unified manifest 1.2.11 |
| [C271] | b6aa3d5182d47bdb8c6dbac43b68a8d20dfc30a8 | EN_ONLY | `f3bfe870af6813c4d625026abf810cc218dfcad38b27e13d3826b247e75a2798` | Add schema and semantic vectors for unified manifest 1.2.9 |
| [C272] | b09ee5b2e02f83a9360af36d8c7da2f43911bf5a | EN_ONLY | `df74710aedb5a7639d455b9c506e052c18a7722ac0cc31b22221128bb9c83d46` | Add test-profile semantic validator for unified union manifest |
| [C273] | cd1ab0fb346c770d779b1d8d24297f6811a1a74f | EN_ONLY | `7d9f813d3640a4f200ed15654b8f6e9aadeadff9d659b67507ac8282eb9d1e00` | docs: adopt mandatory bilingual architecture policy |
| [C274] | 55d44b9276456f88bd2193de8b06aff146c228a4 | EN_ONLY | `112b78453763e1bfebed7c76104e5c6ad0aff61363d5919a2f7d2ba8f0e0446c` | docs(governance): establish AI development operating model |
| [C275] | 3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f | EN_ONLY | `44d6a53aa0981cad7e289143ca4fa4c5b1a25acebe97d6eee05c0808238da60c` | docs(review): add A-I technology architecture review tasks |
| [C276] | a20afe28998363b6185e054f7d4c1aa68cac9f3b | EN_ONLY | `63197afd48a4acddb1513502d0b6e219b1795d15bdd952223e1dafc54670234d` | docs(review): add A-I technology architecture review task pack |
| [C277] | e88ed03f8b5113ef25df1b91cde9145848f42eec | EN_ONLY | `b1e769d9b7f052c8b958bc9337563c7cddb8d32fc275e81c2ef2eb7c7cd7eec5` | docs(roadmap): link technology architecture blueprint |
| [C278] | 17581af398cfbb9c982f07718b0fd38af577d2fa | EN_ONLY | `c66c4e873731d4751257cc19d6bc4b87c3b4a92fd725445cf377a62932716be7` | docs(architecture): add system technology architecture blueprint |
| [C279] | 8a6414158c9c056c1638222534e1993d1bbc99d2 | EN_ONLY | `1e397589a1c18745b77902c2d8ba7d85a838078bd5674c48c1144f8bda515869` | docs(integration): review D E H I phase 3 contracts |
| [C280] | 8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2 | EN_ONLY | `1df9edb0570f6e2e2ff520a04b2f7c5e52116a0c665f8449fe21597535d19680` | Add nine copy-ready Phase 3 session kickoff prompts |
| [C281] | 3cae375aadfc2a8b2facce5cb006ff1e55c2dfe1 | EN_ONLY | `a16bc7473e04bdba8d81cc4da3e3e8e2cfb0b2a4e14c4d3374da1c27513dbbbe` | Add Phase 3 cross-module remediation task pack |
| [C282] | 2624c6d19bc4ca7c369fdd416e9d307755a83671 | EN_ONLY | `531bfb893e9285ffb4b8ec5563d5e6f0cec443eb2dc6bf829db99be4c4440e07` | Add Phase 2 D/E/F/G cross-session review reconciliation |
| [C283] | 396d5804bc1ca67e7d2a63299918d20c1d09808b | EN_ONLY | `2812fde68864e80096c1c35da7ff7a5ca7c6ff904bfcf4f7c4a5db3616486f52` | Add branch-aware Session D review scope correction and reassessment |
| [C284] | 51d3cd014ae887712eb4f46855b38df86b666cf9 | EN_ONLY | `792cef6e367550c4801ca71739ef1db8e03d1ace37a1059119d1122cdced33ae` | Add Session G three-party six-dimension architecture review |
| [C285] | eddfee02cb34c33918e50e9266cafee5011c2fc3 | EN_ONLY | `d2e209735c2613551d693246031b4957ec514b26f7171aed13d22fc368cccf12` | Add Session E three-party six-dimension architecture review |
| [C286] | e2cc35d382d971061f65294959d3c0e742552cc3 | EN_ONLY | `8b8aea4ae6b2b92aca2ce88e0d3e21b341411b965c9891bbb82f687faccf6016` | Add Session D three-party six-dimension architecture review |
| [C287] | 8fe2e171ded8d2031aa853cc516936d10b44a010 | EN_ONLY | `282317dc3192ac0f481cc23f23af7b1e7a73a8eb0fb4477da3547012d434837e` | docs(review): add Session F Memory Runtime architecture review |
| [C288] | e443b23f8a179ad12c163722ad93bc646fd3a80a | EN_ONLY | `1123bfd90382361ac721342d619c6b3d2e285e6e380f3291b9f5d00d295aefae` | Add Phase 1 A/B/C integration review |
| [C289] | 60adf3c0433158a497adf14c3de40fffb520deeb | EN_ONLY | `ebad32451307c39ba77461c2061ba6ad9fbd69607c7f82079951264fadb2a78c` | Add three-party six-dimension review for Session C |
| [C290] | e2c98d4d49dc7f159ef45533560f084fe3b30f3d | EN_ONLY | `3dd7d14a5676bf9ede296f8f6b2f2e58ef262feaf0236d525045a5d899126c98` | docs(review): add three-party six-dimension review for domain model |
| [C291] | 6efed32df68960fe2f78ae659852eacbd59b4a62 | EN_ONLY | `186581ade91616dac8d52603dc5931985fd81638bb4adf3fbf2f92592eb0ab64` | docs(review): add three-party six-dimension architecture review |
| [C292] | 3a578d0b42fe00e90fd8765a208c6f15801842dd | EN_ONLY | `24d03b9185c5c9d5f0d2a6c32f6472e911a842730dc39fba827fa9c3913ec8b1` | docs(domain): define scope and permission model |
| [C293] | d23c5fca6fc3e9cafb6ab7f504e0671652cd33e8 | EN_ONLY | `16d1c4aa2997f90a85878102a389de40aabe4d60b691ff52c8befc3c8810dfa3` | docs(domain): specify memory lifecycle model |
| [C294] | 07f2b3598b9a27877bd35dcfc126778c66c066ef | EN_ONLY | `9105ec0ba018b65f2edfce693fa32902273711518726ed901b478dfa808bf767` | docs(domain): define relationships and provenance model |
| [C295] | 96810b8a1b10635bfd18d17a0fea410593754d3d | EN_ONLY | `da26647f47382cee4ca0acd34d881ed3229be9a77ad1a0e58ca7b54ab5d3534f` | docs(domain): specify epistemic and temporal semantics |
| [C296] | 42f4f3fa08b4a45893fda279daafe477ee2ebf62 | EN_ONLY | `03c7ec3ae71378ec9fa491bc3960c8cb4e1afc834b22d41c3a064a1200d58e13` | docs(domain): define canonical core entities |
| [C297] | ae53bdf53eb4e579b99d6aa6bba97ea1eb53d223 | EN_ONLY | `fa667865075196f04e1c9526dd9330ca496210d087a4a9c7a1c2b456a29ddcb9` | docs(domain): add canonical domain model overview |
| [C298] | 60254332fa6cfad0d14a6f16c5d8aa22f422d641 | EN_ONLY | `9347aa72b58f130de44937dc3da96f095fcf55b26150f581656440edc7cd2099` | docs(agent-integration): define inference boundary and application semantics |
| [C299] | 038ad2893a245baa58bd7659bf31f8dec91de6a7 | EN_ONLY | `867958571d2a2c429db3eb1c9f7d16eb9c8d2fab618ea0d0cf72f4cc86e7176d` | docs(agent-integration): define adapter capability tiers |
| [C300] | 631b61b9544ab730018858b2c800b0c689f5a29c | EN_ONLY | `4562dcc6f40b75faf7127ab6664cf996e4e736ef2dd7ba73eb669bf00a740145` | docs(agent-integration): specify canonical telemetry model |
| [C301] | 62854e5adf348ebf824e1e2a4f69d79e242f51aa | EN_ONLY | `ba9e5e84901e6354224f6b1a96773e952c866f2a8a35d1aa82bc281900d6fff0` | docs(agent-integration): define integration boundaries |
| [C302] | c08d903255d23b2e069f6c23ff39aa3e5f96d36c | EN_ONLY | `fa4926acc6808cd370c319d9c510af2b3d8488e69f537c0a1bb3793c68deeb0b` | docs(architecture): add system architecture specification |
| [C303] | c467b13b83186dd24b29c4ee2468b2698ac6908b | EN_ONLY | `fa4926acc6808cd370c319d9c510af2b3d8488e69f537c0a1bb3793c68deeb0b` | docs(architecture): add system architecture specification |
| [C304] | 4fe0435ec07b2ef7cc6b354c1aad31162299370a | EN_ONLY | `fa4926acc6808cd370c319d9c510af2b3d8488e69f537c0a1bb3793c68deeb0b` | docs(architecture): add system architecture specification |
| [C305] | 5461dc2ae2e7bf88a16ca2314ed372fc74ee4e96 | EN_ONLY | `fa4926acc6808cd370c319d9c510af2b3d8488e69f537c0a1bb3793c68deeb0b` | docs(architecture): add system architecture specification |
| [C306] | 2f4bcd0c879d3a0d3fa797d70e0d7a695375231f | EN_ONLY | `c76f2bfcd7573efcdb2cc28fec871b5f48a2fca3905b2c9036ede1786d8f56ae` | docs: add subsystem responsibility matrix |
| [C307] | 69e920c4f3094dfe59477963c52a2a2ca78994f4 | EN_ONLY | `ed04e831a713f1334da2bae1e0af9224312a7ebb438368dcae961e5e89a9e541` | docs: add logical system component map |
| [C308] | fe6e55dc7cc5196f8cb8388df47b7628df251822 | EN_ONLY | `b372badec3d7d79d99379a74f71d52f48eb6ee789d24e67a5939b749c0117661` | docs: add system architecture overview |
| [C309] | c7f5499019c3b8e0365345a183a14bd6c2dcce69 | EN_ONLY | `9edee97d93a0abfaec99aef89e6c37cadfb7b3bbd0d5a13d6a41c315d922152f` | docs: establish canonical architecture terminology |
| [C310] | 13f9f0eafbaabe1f07f82a2fc5b291d20d89a0e8 | EN_ONLY | `7d3a5adbf77e9d13d687c534c0c37e8377b36ae310a9bdad18c0c174208a4fb1` | docs: establish system architecture invariants |
| [C311] | 424ca894a9d76281f1d7247ae4bc1684554b79c5 | EN_ONLY | `5bde113b09e02f8c6306b9aff493ac822d5684bb4493684e497c447dd7aca2da` | docs: define architecture design principles |
| [C312] | fef7ba5f3367c4734bcb838bc4565db1e44e34d3 | EN_ONLY | `ca6d4bd55840462e2f5c2d2f2c75ae19701df73eb2f700a38ec9783453665624` | docs: add architecture roadmap and design workflow |
| [C313] | 9ed0e7c79d7a16a122a797b15375658da62b367b | EN_ONLY | `086a7101c59d33e7f6e6b8e4c829a8b90249e624fa415b19f238c77cfe58b514` | docs: initialize AI Memory Brain architecture repository |

### §8.13 收尾：统计口径与自洽性声明

本节登记范围为 C001–C313，共 313 条 commit-message 记录。语言状态以**完整 commit message 的实质内容**为判定对象，而非仅依据变更文件的语言、路径或文件名；编号沿用 E9 原始编号及提交时间顺序。逐条登记结果为 **312 条 EN_ONLY、1 条 EN_ZH_MIXED（C168）**，合计 **312 + 1 = 313**，与登记总数一致。

C001–C160 与 C161–C313 为同一清单的前后两段；C168 是本批唯一标记为 EN_ZH_MIXED 的记录，其余本批记录均为 EN_ONLY。表中 `msg_sha256` 用于标识对应完整 commit message 的内容摘要，subject 列仅展示首行，不替代完整消息作为语言判定依据。

本清单属于历史 commit-message 语言状态登记，不改变任何历史 Git 对象，不改写既有 commit message，也不因完成登记而推定相关文档已完成双语迁移。登记状态、迁移状态与迁移验收状态应分别判定，不得相互替代。

## 任务 1：D2 §8.14 最终定稿

### 8.14 历史 Issue 与 Commit 语言登记的完整性及关闭条件

本节规定历史 Issue 与 Commit 语言状态登记的完整性要求、判定边界及关闭条件。登记集合分别以 §8.11 的 Issue 清单和 §8.12／§8.13 的 Commit 清单为准；不得将两类对象合并计数，也不得以登记完成替代双语迁移完成。

**1. Issue 登记集合及状态**

Issue 登记集合共 **39 条**，分类数量必须保持如下关系：

| 语言状态 | 数量 | 处置 |
|---|---:|---|
| EN_ONLY | 28 | 按既定迁移要求处理 |
| EN_ZH_MIXED | 10 | 按既定迁移要求处理 |
| ZH_ORIGINAL_WITH_EN_TERMS | 1 | Issue #254；保持 HOLD |
| **合计** | **39** | |

Issue #254 **属于这 39 条登记集合**，是第 39 条记录，分类为 `ZH_ORIGINAL_WITH_EN_TERMS`，当前处置为 `HOLD`。不得将其描述为集合外对象、从 39 条总数中排除，或将其计为已完成迁移。

**2. Issue 内容锚点**

39 条 Issue 记录必须逐条具有对应的 `body_sha256`。该锚点用于标识登记时实际检查的 Issue 正文版本。缺少锚点、锚点格式无效、同一记录锚点与其登记对象不匹配，均属于未关闭缺陷。

Issue #254 的 HOLD 必须有明确、可审计的退出条件和后续处置记录。只有在退出条件得到核验、处置决定被明确记录，并且相应内容及锚点完成复核后，方可更新其 HOLD 状态。不得仅因其已登记或总数对账通过而解除 HOLD。

**3. Commit 登记集合及状态**

Commit 登记集合共 **313 条**，分类数量必须保持如下关系：

| 语言状态 | 数量 | 说明 |
|---|---:|---|
| EN_ONLY | 312 | 英文提交消息 |
| MIXED | 1 | C168 |
| **合计** | **313** | |

313 条记录必须逐条具有 `msg_sha256` 和对应的 `sha`。`msg_sha256` 锚定登记时检查的完整提交消息内容；`sha` 标识对应 Git Commit 对象。不得缺失、错配或以其他字段替代这两个锚点。

**4. Commit 语言判定规则**

Commit 语言分类必须依据**完整提交消息的实质内容**判定，包括标题及正文；不得根据被修改文件的语言、路径、Issue 语言、PR 语言或其他间接信息推断。

C168 是 313 条记录中唯一的 `MIXED` 记录；其余 312 条均为 `EN_ONLY`。若后续复核发现提交消息内容与登记分类不符，必须记录具体对象、原分类、复核依据及更正结果，并重新执行数量对账。

**5. 计数、唯一性及缺漏对账**

关闭前必须完成并留存可复核的机器或人工对账结果，至少覆盖：

- Issue 登记恰为 39 条，分类数量为 28 + 10 + 1 = 39；
- Commit 登记恰为 313 条，分类数量为 312 + 1 = 313；
- 每个集合内部对象唯一，不得重复登记；
- 登记对象与对应 Issue／Commit 身份准确匹配；
- 39 条 Issue 均具有有效且匹配的 `body_sha256`；
- 313 条 Commit 均具有有效且匹配的 `sha` 与 `msg_sha256`；
- 不存在未解释的缺漏、重复、错配或分类数量差异；
- Issue #254 仍在 39 条集合内，并保留 HOLD 及其明确退出条件。

任一项未通过，相关登记工作不得判定为完整关闭。

**6. 登记完成与迁移完成的边界**

语言状态登记完成只表示历史对象已按规定识别、分类并建立内容锚点，不表示历史 Issue 或 Commit 消息已经完成双语迁移、修订或重写。历史 Git 对象不得因本登记而被改写。

不得将登记完成、计数一致、锚点齐全或测试通过单独表述为历史内容迁移完成，也不得将 Issue #254 的 HOLD 解释为豁免。

**7. 审计声明限制**

只有在上述对象范围、锚点、分类、唯一性、缺漏及 HOLD 处置证据均完整且通过复核后，才可声明本节规定的登记完整性检查已完成。

若证据仅覆盖部分对象、部分锚点或部分对账项目，必须明确标注审查范围及未验证事项；不得表述为已完成全部审计、已完成全部迁移或已满足全部关闭条件。

## 8.15 Anchor refresh register / 锚点刷新登记

**Purpose.** §8.11 and §8.13 record anchors taken at the inventory snapshot. When a registered object is edited after that snapshot, the historical anchor is *not* overwritten: it stays as recorded, and the refresh is registered here with both values, the observation time, and the source of the recomputation. A superseded anchor must never be presented as the current value.

**用途。** §8.11 与 §8.13 记录的是清点快照时的锚点。登记对象在快照后被编辑时，**不覆盖**历史锚点：原值保留在原表，刷新登记在本节，同时给出旧值、新值、观测时间与复算来源。已被取代的锚点不得作为现行值呈现。

| Object / 对象 | Recorded anchor (historical) / 原锚点 | Recomputed anchor (current) / 复算锚点 | Observation / 观测 | Classification re-check / 分类复核 | Source / 来源 |
|---|---|---|---|---|---|
| Issue #266 | `d984146097e7ce9a031f7046f4267ce7e2b40cd0380ccd6c37f98d17e93fadef` | `aaa599ccbfa45a20f4083ac2c9958739013dd4f816b9bda391964bd6b84ce3a9` | issue `updated_at` = `2026-11-19T16:34:35Z`; recomputed `2026-11-19T17:22Z` against the live API body | `EN_ZH_MIXED` — unchanged; the body still carries paired EN/ZH headings and parallel sections | `00-governance/reports/f06-object-reconciliation.md` §3 |

**Rules / 规则**

1. The original anchor in §8.11/§8.13 is never edited in place; this section is the single place where a refreshed value becomes authoritative for current use.
2. Every entry must carry: object identifier, both anchors, the observation time of each, the reason for the change (edit event with its timestamp), the classification re-check result **as evidence that the classification is unchanged**, and the source record that holds the recomputation.
3. **A refresh entry may only carry a re-check whose outcome is "unchanged".** If the re-check finds that a classification change is required, the refresh stops at that point: the entry records the stop and the referral, and the change is handled exclusively by the separate classification process defined in rule 5. The refresh entry must never carry the changed classification itself.
   A refresh entry therefore cannot change the object's language classification; it can only certify that the classification is unchanged, or record that the case was referred out.
4. Absence of an entry means the §8.11/§8.13 anchor was current as of the reconciliation baseline `f86fddc0` (recomputed 313/313 commits and 38/39 issues against that baseline).
5. **Isolation from classification changes.** A refresh entry must not modify an object's classification field, classification basis, or classification decision record. Any classification change requires its own re-inspection and its own registration/approval path; folding a classification change into an anchor refresh is prohibited.
6. A refresh entry does not migrate, rewrite, or exonerate any historical object; `MIGRATION_DEBT != EXEMPTION` remains in force.

**中文规则**

1. §8.11/§8.13 中的原锚点一律不就地改写；本节是刷新值取得现行效力的唯一位置。
2. 每条记录必须包含：对象标识、新旧两个锚点、各自的观测时间、变更原因（编辑事件及其时间戳）、**作为「分类未变」证据的**分类复核结果，以及保存复算过程的来源记录。
3. **刷新条目只承载结论为「未变」的复核。**若复核发现需要变更分类，刷新流程必须在此时停止：条目只记录「已停止并转交」，变更一律交由第 5 条规定的独立分类程序处理。刷新条目不得承载变更后的分类本身。
   因此刷新条目不能改变对象的语言分类，只能证明分类未变，或记录已转交。
4. 无条目意味着该对象的 §8.11/§8.13 锚点在对账基线 `f86fddc0` 上仍然有效（该基线复算：Commit 313/313、Issue 38/39）。
5. **与分类变更严格隔离。** 刷新条目不得修改对象的分类字段、分类依据或分类判定记录。任何分类变更都必须另行重新核查并走独立的登记/审批路径；禁止把分类变更夹带进锚点刷新。
6. 刷新条目不迁移、不改写、不豁免任何历史对象；`MIGRATION_DEBT != EXEMPTION` 继续有效。
