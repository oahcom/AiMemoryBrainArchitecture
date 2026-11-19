# GOV-DOC-001 v1.2 Bilingual Baseline Remediation Report
# GOV-DOC-001 v1.2 双语基线修复交付报告

- Work Item ID: GOV-DOC-001-V1.2-REMEDIATION
- Policy ID: GOV-DOC-001
- Proposed Version: 1.2
- Status: DRAFT — NEEDS REVISION — PENDING FORMAL GOVERNANCE APPROVAL
- Repository: oahcom/AiMemoryBrainArchitecture
- Target Branch: remediation/gov-doc-001-v1.2-bilingual-baseline
- Pull Request: #271
- Report Version: 2.0
- Report Evidence Date: 2026-11-19

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

- Total Issues excluding PRs: 39.
- Identified single-language Issue titles: 33.
- Coverage: all 39 Issue records.
- Body-language verification: incomplete.
- Original_Language_State for unverified bodies: UNKNOWN.
- Migration classification: MIGRATION_DEBT or INVENTORY_REQUIRED as applicable.

Issue 标题清点已覆盖 39 条记录，识别出 33 条单语标题。

正文语言尚未逐条核验，不能将标题语言直接当作正文语言。

### 5.2 Commit inventory / Commit 清点

- Examined sample: latest 100 Commits.
- Observed result: 100/100 single-language Commit Messages.
- Inventory coverage: sample only, not full history.
- Full historical inventory: INVENTORY_REQUIRED.
- Historical Commit rewriting: PROHIBITED.

最近 100 条 Commit 抽样均为单语，但不是完整历史清点。

不得将抽样结果描述为全量结论。

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

| Object category | Current classification |
|---|---|
| Known historical single-language records | MIGRATION_DEBT |
| Incomplete full-history inventory | INVENTORY_REQUIRED |
| Formally authorized exemptions | NONE_RECORDED |
| Authorized migration execution | NOT_CONFIRMED |
| Completed historical migration | NOT_CONFIRMED |

MIGRATION_DEBT is not EXEMPTION.

迁移技术债不等于正式豁免。

Inventory completion is not migration completion.

完成清点不等于完成迁移。

The T6/T7 D2 incremental appendix has been prepared as a separate artifact, but its incorporation into the committed D2 file is NOT_CONFIRMED.

T6/T7 的 D2 增量附录已经作为独立材料形成，但尚未确认已经合并进已提交的 D2 文件。

### 5.5 Historical Commit protection / 历史 Commit 保护

No historical Commit was rewritten.

No historical SHA was changed.

No force-push was performed.

未重写历史 Commit。

未修改历史 SHA。

未执行 force-push。

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

The inheritance mechanism must establish:

1. An explicit inheritance-validation authority.
2. A defined validation trigger.
3. Verification of Policy ID, approved version, source Commit, and Blob SHA.
4. Coverage of Issue, Commit, PR, and documentation workflows.
5. A deterministic failure result when inheritance requirements are unmet.
6. At least one reproducible PASS case and one reproducible FAIL case.

The current D1/D6 content establishes normative inheritance obligations but does not provide sufficient executable enforcement evidence.

现有 D1/D6 定义了继承义务，但没有提供充分的可执行门禁证据。

### 6.5 F-06 remediation requirements / F-06 修复条件

Required:

- Complete object-level inventory.
- Exact object identifiers.
- Verified original language states.
- Migration status and accountability.
- Exact source evidence.
- No historical Commit rewriting.
- No invented missing fields.
- No migration completion claims without evidence.

Required additional action: resolve the 14 ungrouped PRs.

### 6.6 F-07 correction / F-07 更正

Authoritative D1 Blob SHA:

66517d39dfeae459fef5cedf9d5a79de08faf08d

The 41-character malformed value was a transcription error in the review report's current-read field.

T9 directly fetched D1 and reconfirmed the authoritative 40-character SHA.

The historical erroneous transcription must remain visible as a corrected historical record, not silently overwritten.

历史转录错误必须保留为有更正说明的记录，不得静默覆盖。

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

Workflow run:

https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44477435608/job/135401280200

Check:

GOV-DOC-001 structural checks

Job ID:

135401280200

Conclusion:

FAILURE

Failure:

Normative source files changed but PR body lacks 'BILINGUAL-MANIFEST: COMPLETE' or a fully documented 'BILINGUAL-EXCEPTION: APPROVED'.

### 7.2 Actual gate behavior / 门禁实际行为

The current checker includes:

- NORMATIVE_ROOTS containing 00-governance.
- Markdown normative source detection.
- An EMBEDDED_BILINGUAL_SOURCES allowlist containing only D1.
- A mandatory PR manifest.
- A counterpart requirement for every normative source not in the allowlist.

D2–D7 are self-contained bilingual Markdown documents but are not currently included in the embedded-source allowlist.

Adding only BILINGUAL-MANIFEST: COMPLETE would therefore cause six additional counterpart errors.

仅增加 manifest 标记会导致 D2–D7 六份文件继续触发对应文件缺失错误。

### 7.3 Recommended remediation / 建议修复

Decision: OPTION (a).

Extend EMBEDDED_BILINGUAL_SOURCES to include all seven self-contained bilingual governance files.

This is preferable to duplicating the same bilingual content into docs/en and docs/zh-CN solely to satisfy a structural checker.

The allowlist change must be explicit, reviewable, and restricted to the exact paths listed below.

Recommended exact replacement:

```python
EMBEDDED_BILINGUAL_SOURCES = {
    "00-governance/bilingual-documentation-policy.md",
    "00-governance/bilingual-governance-migration-register.md",
    "00-governance/templates/bilingual-issue-template.md",
    "00-governance/templates/bilingual-umbrella-requirement-template.md",
    "00-governance/templates/bilingual-commit-message.md",
    "00-governance/templates/repository-policy-inheritance.md",
    "00-governance/reports/bilingual-baseline-remediation-report.md",
}
```

The current gate is structural. Allowlisting does not establish semantic parity.

独立审查仍必须检查双语语义一致性。

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

Option (c), BILINGUAL-EXCEPTION: APPROVED, is NOT selected.

No formal exception authorization evidence exists.

No Owner, approval date, or exception authority may be invented.

Do not submit a fake approval declaration.

不选择正式豁免方案，不补造授权信息。

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

## 9. Outstanding blockers and next actions / 未解决阻塞与后续行动

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

| Stage | Status | Evidence |
|---|---|---|
| v1.1 Read | READ | Historical policy source |
| v1.2 Drafted | DRAFTED | D1–D7 |
| Seven files submitted | SUBMITTED | Commit a77219fa2834af0c4535e6692029adaec2e62638 |
| Seven files read back | VERIFIED | Seven exact Blob SHAs |
| Five Issues updated | SUBMITTED | GitHub Issue records |
| Five Issues read back | VERIFIED | Five API reads |
| Historical inventory | PARTIAL | Issue/PR aggregate; Commit sample |
| Independent review | NEEDS REVISION | T8 review |
| F-02 | OPEN | P1 |
| F-06 | OPEN | P2 |
| F-07 | OPEN | P2 |
| Structural CI | FAILURE | Run 44477435608 |
| Owner approval | NOT_RECORDED | No approval evidence |
| Policy adoption | NOT_ADOPTED | No adoption evidence |
| Effective status | NOT_EFFECTIVE | v1.2 remains DRAFT |

## 11. Honest declaration / 诚实声明

### EN

This report records verified repository and GitHub API evidence available during T9.

The seven original deliverable files were committed and independently read back by exact Blob SHA.

The five Issue updates were read back with OPEN states preserved.

The current main branch HEAD was directly retrieved.

Historical Issue and PR aggregate inventories were prepared, but the historical Commit inventory remains sample-based.

Fourteen PR records remain ungrouped.

An independent review returned FAIL — NEEDS REVISION.

The structural CI check returned FAILURE.

The T6/T7 D2 incremental appendix has not been confirmed as incorporated into the committed D2.

This Version 2.0 D7 report is a proposed replacement and has not been committed.

No formal Owner approval is recorded.

No policy adoption is recorded.

GOV-DOC-001 v1.2 remains DRAFT and is not effective.

GOV-DOC-001 v1.1 remains NORMATIVE.

PR #271 remains OPEN and has not been authorized for merge by this report.

### 中文

本报告记录 T9 阶段能够核实的仓库和 GitHub API 证据。

原七份交付文件已经提交，并通过精确 Blob SHA 完成独立读回核验。

五份 Issue 更新已经读回，OPEN 状态得到保留。

当前 main 分支 HEAD 已直接读取。

历史 Issue 和 PR 的统计清点已经形成，但历史 Commit 清点仍然只是抽样。

仍有 14 条 PR 尚未归组。

独立审查结论为 FAIL — NEEDS REVISION。

结构性 CI 检查结论为 FAILURE。

T6/T7 的 D2 增量附录尚未确认已经并入已提交的 D2。

本 Version 2.0 D7 报告属于拟议替换版本，尚未提交。

没有正式 Owner 批准记录。

没有规范采纳记录。

GOV-DOC-001 v1.2 继续保持 DRAFT，尚未生效。

GOV-DOC-001 v1.1 继续保持 NORMATIVE。

本报告不授权合并 PR #271，PR #271 继续保持 OPEN。

