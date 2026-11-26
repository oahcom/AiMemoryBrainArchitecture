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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-193/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "本记录中的数字由第 2 节的命令在已提交的树上运行得出：84 条缺失路径、300 次固定字符串出现、12 份文件中 21 行已加注、15 行延后并附两段门禁输出。不主张任何 CI 结果、合并 SHA 或 Owner 决定。"
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
    canonical_scope: "AID-2026-193 annotation of the live citations of the 84 09-security-governance paths that are absent from main"
    canonical_scope_id: "ai-development/aid-2026-193-dangling-09-security-governance-citations"
    canonical_scope_keywords:
      - "security-governance"
      - "dangling-reference"
      - "aid-2026-107"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-193/evidence.md"
    en: "docs/en/14-ai-development/work-items/AID-2026-193/evidence.md"
    zh-CN: null
---


# AID-2026-193 —— 84 个在 main 上不存在的 `09-security-governance/` 路径：标注活跃引用，不恢复任何文件

**状态：DRAFT —— 仅标注。** 本工作项改动 12 份文档、共 21 行，另有 15 行连同两段门禁输出一并
延后。它不在 `09-security-governance/` 下新建任何文件，不改动任何规范正文，不删除任何引用，也不把
任何引用改成可点击链接。每一行改动都原样保留原路径文本，只追加一句括注：
`(not restored on main; see AID-2026-107 §10)`。

## 1. 为什么要留这份记录

派单契约称"85 个指向不存在的 `09-security-governance/` 文档的引用"。在 `5df2ee0020a0eaf2092d38f5866ebe37dab0a0d0`
上重新实测：被引用的不同路径字符串共 91 条，其中 84 条在整棵树里都没有对应文件。
派单所说的第 85 条来自只在根目录判存在：`09-security-governance/security-governance-guide.md`
在根目录下不存在，但 `docs/en/` 与 `docs/zh-CN/` 下都有，且没有任何引用以根相对形式指向它，
因此它并不悬空。91 = 84 条缺失 + 7 条存在。

路径指向空，本身并不构成缺陷。300 次出现中有 252 次是 AID-2026-107 第 10.4 节裁决登记表的行，
该表的全部意义正是把这些路径登记为**不在 main 上**的候选，并逐条给出 Owner 分支 blob 与处置。
另有 12 次是 AID-2026-170 证据里逐字引用的"改前/改后"行。其余 36 次分布在 23 份文档中，属于
活跃引用：读者无法分辨它是 Owner 分支上的历史钉点，还是一份在 main 上能打开的文件。这 36 次中，
本工作项对 21 次加注；另 15 次按第 5.3、5.4 节延后，各自附上拒绝该改动的门禁输出。

这条注只是指针，不是处置结论。它说明文件不在 main 上，并把读者指到已经裁决过它的登记表；
它不主张该文档多余、已被取代或已获准恢复；其中 49 行 `UNDECIDED` 仍归相应 Owner 决定。

## 2. 实测

所有命令都在本 worktree 以 `PYTHONUTF8=1` 执行，基线为 `origin/main` = `5df2ee0020a0eaf2092d38f5866ebe37dab0a0d0`。

```
refs   = git grep -oh "09-security-governance/[A-Za-z0-9._-]*\.md" origin/main -- "*.md" | sort -u
tree   = git ls-tree -r --name-only origin/main
absent = refs 中在 tree 里既无同名条目、也无以 "/" + 该路径结尾条目的那些
occ    = git grep -n -F <path> -- "*.md"      # 对每个缺失路径执行
after  = git grep -F "not restored on main; see AID-2026-107" -- "*.md"
```

| 量 | 改前 | 改后 |
|---|---:|---:|
| 被引用的不同 `09-security-governance/*.md` 字符串 | 91 | 91 |
| 其中在整棵树中缺失的 | 84 | 84 |
| 84 条缺失路径的出现次数（固定字符串，`*.md`） | 300 | 300 |
| 带注的出现次数 | 0 | 21 |
| AID-2026-107 第 10.4 节登记表行（三个版本） | 252 | 252 |
| AID-2026-170 逐字 diff 引文（三个版本 × 4 行） | 12 | 12 |
| 延后的活跃引用：双语配对 / 元数据缺失（第 5.3 / 5.4 节） | 6 + 9 | 6 + 9 |
| 改动文件数 | 0 | 12 |
| 84 条中的可点击 markdown 链接数 | 0 | 0 |
| 在 `09-security-governance/` 下新建的文件数 | 0 | 0 |

300 = 252 + 12 + 21 + 15。该划分是稳定的，因为注一律追加在路径文本之后：300 条路径字符串
仍全部可用固定字符串 grep 到，这正是将来恢复时还能从引用处找回它的原因。

引用形式：36 处活跃引用全部是反引号内联代码、未加反引号的表格单元格，或列表裸行。没有一处是
markdown 链接；全树中唯一两处以链接形式出现 `09-security-governance/` 路径的地方，是
`docs/{en,zh-CN}/09-security-governance/` 里指向 `security-governance-guide.md` 的对偶行，
而该文件存在。因此契约中"把可点击链接降为纯文本"的分支没有适用实例，改动全部走第一分支
（保留路径文本，追加说明）。

## 3. 完整清单：84 条缺失路径及其全部引用位置

每一行都由上述固定字符串 grep 产出，因此同一份文档内引用两次的路径会在位置列出现两次。
`已加注` = 该处已追加说明；`已延后` = 因第 5.3 或 5.4 节原因暂不加注；`登记表行` =
AID-2026-107 第 10.4 节中已记录该缺失的行；`逐字引文` = AID-2026-170 中被逐字引用的 diff 行。

| # | 缺失路径 | 引用数 | 引用位置 | 处置 |
|---|---|---:|---|---|
| 1 | `09-security-governance/audit-and-exception-governance.md` | 6 | `14-ai-development/work-items/AID-2026-107/evidence.md:432`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:429`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:429`, `prompts/I/phase-3-remediation.md:49`, `reviews/integration/phase-3-cross-module-remediation-task-pack.md:352`, `reviews/integration/phase-3-session-kickoff-prompts.md:404` | 已加注 + 登记表行 |
| 2 | `09-security-governance/governance-decision-register.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:435`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:432`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:432` | 登记表行 |
| 3 | `09-security-governance/phase-3-global-forget-remediation-report.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:436`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:433`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:433` | 登记表行 |
| 4 | `09-security-governance/phase-3.5-global-identity-forget-governance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:437`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:434`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:434` | 登记表行 |
| 5 | `09-security-governance/phase-3.6-bih-joint-architecture-acceptance-addendum.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:438`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:435`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:435` | 登记表行 |
| 6 | `09-security-governance/phase-3.6-cgh-applied-1.0-i-authority-confirmation.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:439`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:436`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:436` | 登记表行 |
| 7 | `09-security-governance/phase-3.6-cgh-applied-1.0-i-owner-authoritative-confirmation.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:440`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:437`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:437` | 登记表行 |
| 8 | `09-security-governance/phase-3.6-governance-acceptance-execution-addendum.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:441`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:438`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:438` | 登记表行 |
| 9 | `09-security-governance/phase-3.6-governance-approval-and-consumer-acceptance-register.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:442`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:439`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:439` | 登记表行 |
| 10 | `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:443`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:440`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:440` | 登记表行 |
| 11 | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | 10 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md:10`, `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md:29`, `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:79`, `14-ai-development/work-items/AID-2026-107/evidence.md:444`, `docs/en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md:22`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:441`, `docs/governance/owner-branch-translation-inventory.md:111`, `docs/zh-CN/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md:22`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:441`, `reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md:19` | 已加注 + 已延后 + 登记表行 |
| 12 | `09-security-governance/phase-3.6-permission-epoch-and-authorization-formal-confirmation.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:445`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:442`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:442` | 登记表行 |
| 13 | `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` | 5 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md:30`, `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:80`, `14-ai-development/work-items/AID-2026-107/evidence.md:446`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:443`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:443` | 已延后 + 登记表行 |
| 14 | `09-security-governance/phase-3.6-r1-r2-i-owner-gate-linearization-decision-candidate.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:447`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:444`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:444` | 登记表行 |
| 15 | `09-security-governance/phase-3.6-six-dimension-self-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:448`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:445`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:445` | 登记表行 |
| 16 | `09-security-governance/phase-3.6.10-i-exact-version-recovery-cutoff-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:449`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:446`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:446` | 登记表行 |
| 17 | `09-security-governance/phase-3.6.14-i-exact-review-storage-v3.2.4-successor-manifest.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:450`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:447`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:447` | 登记表行 |
| 18 | `09-security-governance/phase-3.6.2-i-coc-jf10-composition-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:451`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:448`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:448` | 登记表行 |
| 19 | `09-security-governance/phase-3.6.2-jf10-commit-authorization-recovery-acceptance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:452`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:449`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:449` | 登记表行 |
| 20 | `09-security-governance/phase-3.6.2-jf10-owner-gate-ordering-correction.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:453`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:450`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:450` | 登记表行 |
| 21 | `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md` | 5 | `14-ai-development/work-items/AID-2026-107/evidence.md:454`, `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:124`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:451`, `docs/zh-CN/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:124`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:451` | 已延后 + 登记表行 |
| 22 | `09-security-governance/phase-3.6.3-i-coc-durable-protocol-authority-acceptance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:455`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:452`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:452` | 登记表行 |
| 23 | `09-security-governance/phase-3.6.4-global-forget-evidence-reconciliation.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:456`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:453`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:453` | 登记表行 |
| 24 | `09-security-governance/phase-3.6.4-global-forget-reference-model-evidence.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:457`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:454`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:454` | 登记表行 |
| 25 | `09-security-governance/phase-3.6.4-i-prepared-participant-gid-authorization-acceptance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:458`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:455`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:455` | 登记表行 |
| 26 | `09-security-governance/phase-3.6.5-i-restore-control-highwater-acceptance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:459`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:456`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:456` | 登记表行 |
| 27 | `09-security-governance/phase-3.6.5-i36-governance-decision-proposal.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:460`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:457`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:457` | 登记表行 |
| 28 | `09-security-governance/phase-3.6.6-i-global-inventory-authority-addendum.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:461`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:458`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:458` | 登记表行 |
| 29 | `09-security-governance/phase-3.6.7-i-exact-version-owner-decision.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:462`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:459`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:459` | 登记表行 |
| 30 | `09-security-governance/phase-3.6.7-i-owner-local-gate-admission-release-amendment.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:463`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:460`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:460` | 登记表行 |
| 31 | `09-security-governance/phase-3.6.8-i-exact-version-owner-rereview-decision.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:464`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:461`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:461` | 登记表行 |
| 32 | `09-security-governance/phase-3.6.8-i-exact-version-r1-r4-rereview-decision.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:465`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:462`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:462` | 登记表行 |
| 33 | `09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:466`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:463`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:463` | 登记表行 |
| 34 | `09-security-governance/phase-3.6.9-i-r1-r2-exact-version-delegated-disposition.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:467`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:464`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:464` | 登记表行 |
| 35 | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | 8 | `14-ai-development/work-items/AID-2026-107/evidence.md:468`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:465`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:465`, `reviews/architecture/SYS-RISK-001.en.md:427`, `reviews/architecture/SYS-RISK-001.zh-CN.md:426`, `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md:9`, `reviews/integration/phase-3.8.2-callable-interface-convergence.en.md:24`, `reviews/integration/phase-3.8.2-callable-interface-convergence.zh-CN.md:24` | 已加注 + 登记表行 |
| 36 | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | 7 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md:43`, `14-ai-development/work-items/AID-2026-107/evidence.md:469`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:466`, `docs/research/product-first/PRODUCT-FIRST-001-SESSION-01-MEMORY-PRODUCTS.md:93`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:466`, `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md:11`, `reviews/technology-reality/TECH-REALITY-001-A-independent-review-follow-up.md:58` | 已加注 + 已延后 + 登记表行 |
| 37 | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | 12 | `14-ai-development/work-items/AID-2026-107/evidence.md:470`, `14-ai-development/work-items/AID-2026-170/evidence.md:70`, `14-ai-development/work-items/AID-2026-170/evidence.md:82`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:467`, `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md:70`, `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md:82`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:467`, `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md:70`, `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md:82`, `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md:67`, `reviews/architecture/SYS-RISK-001.en.md:297`, `reviews/architecture/SYS-RISK-001.zh-CN.md:296` | 已加注 + 登记表行 + 逐字引文 |
| 38 | `09-security-governance/phase-3.8.10-i-scope-clarification-c-profile-identifier.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:471`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:468`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:468` | 登记表行 |
| 39 | `09-security-governance/phase-3.8.11-i-exact-review-unified-1.2.13-recoveryjoin-1.0.2-p0.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:472`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:469`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:469` | 登记表行 |
| 40 | `09-security-governance/phase-3.8.11-i-review-storage-serialization-anchor.md` | 4 | `14-ai-development/work-items/AID-2026-107/evidence.md:473`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:470`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:470`, `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md:68` | 已加注 + 登记表行 |
| 41 | `09-security-governance/phase-3.8.12-i-exact-compatibility-h-unified-1.2.14-recoveryjoin-1.0.2.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:474`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:471`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:471` | 登记表行 |
| 42 | `09-security-governance/phase-3.8.12-i-exact-review-h-unified-1.2.14-current-schema-p0.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:475`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:472`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:472` | 登记表行 |
| 43 | `09-security-governance/phase-3.8.13-i-exact-review-h-authority-join-mapping-1.2.14.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:476`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:473`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:473` | 登记表行 |
| 44 | `09-security-governance/phase-3.8.13-i-review-h-1.2.14-authority-callback-contract.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:477`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:474`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:474` | 登记表行 |
| 45 | `09-security-governance/phase-3.8.13-i-review-h-terminal-authority-verifier-seam.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:478`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:475`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:475` | 登记表行 |
| 46 | `09-security-governance/phase-3.8.14-i-final-compatibility-h-1.2.14-callback-and-recoveryjoin.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:479`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:476`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:476` | 登记表行 |
| 47 | `09-security-governance/phase-3.8.14-i-review-h-full-path-terminal-callback-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:480`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:477`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:477` | 登记表行 |
| 48 | `09-security-governance/phase-3.8.15-i-exact-review-h-expanded-full-path-commit-won-callback.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:481`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:478`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:478` | 登记表行 |
| 49 | `09-security-governance/phase-3.8.15-i-review-h-expanded-full-path-terminal-and-envelope-auth-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:482`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:479`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:479` | 登记表行 |
| 50 | `09-security-governance/phase-3.8.16-i-exact-rereview-h-c-p0-projection-test-39-method-ci.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:483`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:480`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:480` | 登记表行 |
| 51 | `09-security-governance/phase-3.8.16-i-exact-review-h-42-test-commit-won-and-absence-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:484`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:481`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:481` | 登记表行 |
| 52 | `09-security-governance/phase-3.8.16-i-review-h-c-p0-nullable-coc-and-envelope-auth-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:485`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:482`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:482` | 登记表行 |
| 53 | `09-security-governance/phase-3.8.17-i-review-h-outer-envelope-authenticated-ingress-gate.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:486`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:483`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:483` | 登记表行 |
| 54 | `09-security-governance/phase-3.8.17-i-review-h-outer-envelope-authentication-trust-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:487`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:484`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:484` | 登记表行 |
| 55 | `09-security-governance/phase-3.8.18-i-exact-review-h-authenticated-ingress-envelope-trust-boundary.md` | 4 | `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:81`, `14-ai-development/work-items/AID-2026-107/evidence.md:488`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:485`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:485` | 已延后 + 登记表行 |
| 56 | `09-security-governance/phase-3.8.18-i-review-c-outer-envelope-signer-p0-trust-registration.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:489`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:486`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:486` | 登记表行 |
| 57 | `09-security-governance/phase-3.8.18-i-review-h-explicit-outer-signature-profile-requirement.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:490`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:487`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:487` | 登记表行 |
| 58 | `09-security-governance/phase-3.8.19-i-exact-review-c-outer-envelope-p0-correction.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:491`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:488`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:488` | 登记表行 |
| 59 | `09-security-governance/phase-3.8.19-i-review-c-separate-h-gateway-attestation-trust-model.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:492`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:489`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:489` | 登记表行 |
| 60 | `09-security-governance/phase-3.8.2-i-recovery-join-trust-currentness-exact-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:493`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:490`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:490` | 登记表行 |
| 61 | `09-security-governance/phase-3.8.20-i-exact-review-h-gateway-attestation-p0-candidate.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:494`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:491`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:491` | 登记表行 |
| 62 | `09-security-governance/phase-3.8.21-i-exact-rereview-h-gateway-attestation-p0-digest-encoding.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:495`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:492`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:492` | 登记表行 |
| 63 | `09-security-governance/phase-3.8.22-i-exact-review-h-unified-1.2.15-gateway-attestation-schema.md` | 5 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md:315`, `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md:344`, `14-ai-development/work-items/AID-2026-107/evidence.md:496`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:493`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:493` | 已延后 + 登记表行 |
| 64 | `09-security-governance/phase-3.8.23-i-rereview-h-gateway-attestation-replay-acceptance-order.md` | 4 | `14-ai-development/work-items/AID-2026-107/evidence.md:497`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:494`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:494`, `reviews/architecture-breakthrough/integration/evidence-source-ledger.md:126` | 已加注 + 登记表行 |
| 65 | `09-security-governance/phase-3.8.24-i-exact-review-h-applied-delivery-evidence-replay-authorization.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:498`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:495`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:495` | 登记表行 |
| 66 | `09-security-governance/phase-3.8.3-i-cryptographic-trust-profile-proposal.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:499`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:496`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:496` | 登记表行 |
| 67 | `09-security-governance/phase-3.8.3-i-exact-review-h-crypto-wire-mapping-r3.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:500`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:497`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:497` | 登记表行 |
| 68 | `09-security-governance/phase-3.8.3-i-exact-review-h-crypto-wire-mapping.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:501`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:498`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:498` | 登记表行 |
| 69 | `09-security-governance/phase-3.8.3-i-re-review-h-crypto-wire-mapping-r2.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:502`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:499`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:499` | 登记表行 |
| 70 | `09-security-governance/phase-3.8.4-i-c-provider-outcome-trust-boundary-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:503`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:500`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:500` | 登记表行 |
| 71 | `09-security-governance/phase-3.8.4-i-crypto-profile-artifact-revision-amendment.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:504`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:501`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:501` | 登记表行 |
| 72 | `09-security-governance/phase-3.8.4-i-exact-review-h-membership-proof-bundle.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:505`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:502`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:502` | 登记表行 |
| 73 | `09-security-governance/phase-3.8.4-i-exact-review-h-unified-manifest-1.2.11.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:506`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:503`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:503` | 登记表行 |
| 74 | `09-security-governance/phase-3.8.4-i-owner-snapshot-membership-proof-contract.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:507`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:504`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:504` | 登记表行 |
| 75 | `09-security-governance/phase-3.8.5-i-exact-review-h-unified-1.2.13-owner-proof-compatibility.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:508`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:505`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:505` | 登记表行 |
| 76 | `09-security-governance/phase-3.8.5-i-recoveryjoin-1.0.2-unified-1.2.12-wire-adoption-amendment.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:509`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:506`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:506` | 登记表行 |
| 77 | `09-security-governance/phase-3.8.5-i-storage-logical-serialization-topology-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:510`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:507`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:507` | 登记表行 |
| 78 | `09-security-governance/phase-3.8.6-i-c-outcome-crypto-profile-trust-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:511`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:508`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:508` | 登记表行 |
| 79 | `09-security-governance/phase-3.8.7-i-exact-signed-object-p0-allowlists.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:512`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:509`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:509` | 登记表行 |
| 80 | `09-security-governance/phase-3.8.7-i-h-owner-snapshot-attestation-schema-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:513`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:510`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:510` | 登记表行 |
| 81 | `09-security-governance/phase-3.8.8-i-crypto-profile-architecture-decision.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:514`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:511`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:511` | 登记表行 |
| 82 | `09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md` | 11 | `14-ai-development/work-items/AID-2026-107/evidence.md:515`, `14-ai-development/work-items/AID-2026-170/evidence.md:64`, `14-ai-development/work-items/AID-2026-170/evidence.md:76`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:512`, `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md:64`, `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md:76`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:512`, `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md:64`, `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md:76`, `reviews/architecture/SYS-RISK-001.en.md:77`, `reviews/architecture/SYS-RISK-001.zh-CN.md:77` | 已加注 + 登记表行 + 逐字引文 |
| 83 | `09-security-governance/phase-3.9-i-d-forget-lifecycle-terminalization-authorization-proposal.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:516`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:513`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:513` | 登记表行 |
| 84 | `09-security-governance/threat-model-and-adversarial-test-plan.md` | 6 | `14-ai-development/work-items/AID-2026-107/evidence.md:522`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:519`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:519`, `prompts/I/phase-3-remediation.md:48`, `reviews/integration/phase-3-cross-module-remediation-task-pack.md:351`, `reviews/integration/phase-3-session-kickoff-prompts.md:403` | 已加注 + 登记表行 |

## 4. 已加注的 21 处活跃引用

| # | 引用位置 | 被引路径 | 形式 | 处置 |
|---|---|---|---|---|
| 1 | `prompts/I/phase-3-remediation.md:49` | `09-security-governance/audit-and-exception-governance.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 2 | `reviews/integration/phase-3-cross-module-remediation-task-pack.md:352` | `09-security-governance/audit-and-exception-governance.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 3 | `reviews/integration/phase-3-session-kickoff-prompts.md:404` | `09-security-governance/audit-and-exception-governance.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 4 | `reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md:19` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 5 | `reviews/architecture/SYS-RISK-001.en.md:427` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 6 | `reviews/architecture/SYS-RISK-001.zh-CN.md:426` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 7 | `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md:9` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 8 | `reviews/integration/phase-3.8.2-callable-interface-convergence.en.md:24` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 9 | `reviews/integration/phase-3.8.2-callable-interface-convergence.zh-CN.md:24` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 10 | `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md:11` | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 11 | `reviews/technology-reality/TECH-REALITY-001-A-independent-review-follow-up.md:58` | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 12 | `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md:67` | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 13 | `reviews/architecture/SYS-RISK-001.en.md:297` | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 14 | `reviews/architecture/SYS-RISK-001.zh-CN.md:296` | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 15 | `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md:68` | `09-security-governance/phase-3.8.11-i-review-storage-serialization-anchor.md` | 表格单元格 | 在路径文本之后附加说明；路径文本保持原样 |
| 16 | `reviews/architecture-breakthrough/integration/evidence-source-ledger.md:126` | `09-security-governance/phase-3.8.23-i-rereview-h-gateway-attestation-replay-acceptance-order.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 17 | `reviews/architecture/SYS-RISK-001.en.md:77` | `09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 18 | `reviews/architecture/SYS-RISK-001.zh-CN.md:77` | `09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 19 | `prompts/I/phase-3-remediation.md:48` | `09-security-governance/threat-model-and-adversarial-test-plan.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 20 | `reviews/integration/phase-3-cross-module-remediation-task-pack.md:351` | `09-security-governance/threat-model-and-adversarial-test-plan.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |
| 21 | `reviews/integration/phase-3-session-kickoff-prompts.md:403` | `09-security-governance/threat-model-and-adversarial-test-plan.md` | 正文/列表 | 在路径文本之后附加说明；路径文本保持原样 |

## 5. 未加注的 279 处

### 5.1 登记表行（252 处）

`14-ai-development/work-items/AID-2026-107/evidence.md` 第 10.4 节及其 `docs/en`、
`docs/zh-CN` 两个版本，逐条列出全部 84 条路径（84 × 3 = 252 行）。每行已带 Owner 分支
blob SHA、分类（`NORMATIVE_ROOT`、`HISTORICAL_PHASE_RECORD`、`UNDECIDED`）与依据代码，
且第 10.1 节已把范围写明为 main 上缺失的路径。在一份本来就只为说明"不在 main 上"而存在的
登记表正文里再追加"not restored on main"，不增加信息、降低可读性，还会让本工作项的指针指向
自己的加注副本。

### 5.2 逐字引文（12 处）

`14-ai-development/work-items/AID-2026-170/evidence.md` 把四行表格各引用两次（改前、改后），
共三个版本。这些引文是"某一格变了、其余没变"的证据。改动被引文本会让引文与被引文档
（`reviews/architecture/SYS-RISK-001.{en,zh-CN}.md`）不一致，因此引文逐字保留，注加在被引的
原文上。

### 5.3 因双语配对而延后（4 份文档中的 6 行）

- `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md`
- `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md`
- `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md`
- `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md`

其中位于 `13-engineering-decisions/` 的四份文档属于 `NORMATIVE_ROOTS` 之一。
`scripts/check_bilingual_docs.py` 要求改动这类文档时，必须在同一个 PR 内同时改动其全部双语
对偶文档。而这些对偶文档并不存在——它们正是仓库已记录为缺失的 77 组语言对之一——所以要满足该
要求只能新建它们，那属于本单元之外的建文档决定。先实测加注这四份文件，门禁给出的正是拒绝：

```
::error::13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md requires all counterparts changed in this PR: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md, docs/en/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md, docs/zh-CN/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md
::error::13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md requires all counterparts changed in this PR: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md, docs/en/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md, docs/zh-CN/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md
::error::13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md requires all counterparts changed in this PR: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md, docs/en/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md, docs/zh-CN/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md
::error::13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md requires all counterparts changed in this PR: 13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md, docs/en/13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md, docs/zh-CN/13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md
Bilingual documentation gate: FAIL
```

### 5.4 因缺少文档元数据而延后（7 份文档中的 9 行）

延后清单中另外七份文档没有 `document_metadata` 块。在该基线上，元数据门禁会让任何被改动却缺少
该块的文档直接失败，于是仅加一句注就能把一项绿灯检查变成红灯：

```
FAIL: 7 error(s)
  DM-01 missing document_metadata block: 14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md
  DM-01 missing document_metadata block: docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md
  DM-01 missing document_metadata block: docs/en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md
  DM-01 missing document_metadata block: docs/zh-CN/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md
  DM-01 missing document_metadata block: docs/zh-CN/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md
  DM-01 missing document_metadata block: docs/governance/owner-branch-translation-inventory.md
  DM-01 missing document_metadata block: docs/research/product-first/PRODUCT-FIRST-001-SESSION-01-MEMORY-PRODUCTS.md
GOV-DOC-002: 955 governed documents, 509 classified, 446 unclassified
```

给这七份文件补 `document_metadata` 块，等于为仓库尚未分类的文档指定域、角色、生命周期、规范
范围与双语对偶——那是一项治理动作，还会改变 `GOV-DOC-002` 的 `classified` 计数，超出本单元
范围。因此这些注被回退。两组回退都用 `check_document_management.py --require-changed` 复核，
结果为 `PASS (incremental)`。

## 6. 门禁结果

本地运行，对象为标注提交 `@@C1@@`，`PYTHONUTF8=1`：

```
@@GATES@@
```

不带 `--require-changed` 时 `check_document_management.py` 以 `INCOMPLETE` 退出 2，原因是仍有
446 份受管文档未分类；这是仓库在该基线上的既有状态，在任何改动之前对未修改的树运行也得到同一
结论。以增量模式（PR 所采用的方式）运行时，它报 `PASS (incremental): no GOV-DOC-002 violations`。

`check_bilingual_docs.py` 需要通过环境变量提供 `PR_BODY` 才能看到 manifest 标记；它报
`77 frozen, 0 new gaps`，因为没有路径被新增、删除或改名。

## 7. 未做的事

- 未在 `09-security-governance/` 下（任何版本）新建文件。84 条路径仍然缺失；恢复其中任何一条
  都是独立的、逐条的 Owner 决定。
- 未改动 `09-security-governance/` 下的任何正文；未改变任何规范陈述、分类或处置。
- 未删除任何引用，未改写、缩写或别名化任何路径文本。注是追加性的，`git grep -F <path>`
  仍能找全 300 处。
- 未把任何路径改成 markdown 链接，也未新建链接。
- 未新建双语对偶文档、未主张 `BILINGUAL-EXCEPTION`，也未为未分类文档凭空补 `document_metadata`。
- 未主张任何 CI context 结果、合并 SHA 或合并后回读；第 6 节是在所标 SHA 上的本地运行。
- 未关闭任何 Issue，未主张任何验收决定，未改动分支保护、登记表、元数据 schema 或基线。
- AID-2026-107 第 10.4 节中 49 行 `UNDECIDED` 仍未决。

## 8. 改动路径

- `prompts/I/phase-3-remediation.md`
- `reviews/architecture-breakthrough/integration/evidence-source-ledger.md`
- `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md`
- `reviews/architecture/SYS-RISK-001.en.md`
- `reviews/architecture/SYS-RISK-001.zh-CN.md`
- `reviews/integration/phase-3-cross-module-remediation-task-pack.md`
- `reviews/integration/phase-3-session-kickoff-prompts.md`
- `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md`
- `reviews/integration/phase-3.8.2-callable-interface-convergence.en.md`
- `reviews/integration/phase-3.8.2-callable-interface-convergence.zh-CN.md`
- `reviews/technology-reality/TECH-REALITY-001-A-independent-review-follow-up.md`
- `reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md`

## 9. 归属

派单修复契约中的标注 worker；执行模型 `opencode-go/deepseek-v4.1-flash`。不主张独立审查、
Owner 验收或人工签发。
