---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-348/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prompt snapshot is an authoring reference. Exact transmission provenance has not been independently verified."
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
    canonical_scope: "Repair instructions for AID-2026-348: section 11 register-status line in all three copies."
    canonical_scope_id: "ai-development/aid-2026-348-prompt-v2"
    canonical_scope_keywords:
      - "AID-2026-348"
      - "prompt"
      - "governance-register"
      - "section-11"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

接着上一条（A1/A2/A3）。A1 的单行替换已落地。现在发现同一个文件里还有**第二处自相矛盾**，而且它在三份文件里同时存在，正好满足双语门禁"两侧必须同改"的硬约束。

# 事实

同一个 register 文档内部两处状态互相矛盾：

- 头部状态行（三份文件都已正确）：`RESOLVED_ON_MAIN`。
- §11 末尾的 **Register status / 登记状态** 段（三份文件都还写着旧状态）：

```
EN   L279: **Register status**: `ACCEPTED` / `F-2_APPROVED` / empty diff on main is permanently `EXIT=2` / the dividing line is "did the PR supply two-sided mirrors", not "which file did it touch" (§2.1) / introduced by direct push with no PR / recommended fix F-2 approved by the Owner, not executed
CANONICAL L281: （中文，逐字见下方上下文）
ZH   L281: （与 CANONICAL 逐字相同）
```

而同文档 §12 标题就是 "The deadlock is resolved on main — via F-1, and via a self-reviewed merge"，§12 正文与 §1 表格都记 `81dd9a72d2` 起 `EXIT=0`。也就是说 §11 末这句 "empty diff on main is permanently `EXIT=2`" 已被本文档自己证伪。

# 逐字上下文（从工作树直接导出，UTF-8）

### CANONICAL  path=14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md
L45: 
L46: - 登记编号：GOV-NC-2026-11-21-GATE-DEADLOCK-006
L47: - 状态：`RESOLVED_ON_MAIN` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY`（Owner 2026-11-21 裁定，见 §14）/ 解除方式为自我审查合并，见 §12
L48: - 发现时间：2026-11-21T05:05Z（last verified 2026-11-21T05:40Z @ `7d2233a5be`）
L49: - 引入提交：`ae37a41900f1`（2026-11-21T04:50:35Z，**直推 main，无 PR**）
...
L279: ```
L280: 
L281: **登记状态**：`ACCEPTED` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY` / main 上空 diff 恒为 `EXIT=2`（`81dd9a72d2` 起解除，见 §12）/ 判定分界是「是否补双侧镜像」而非「改了哪个文件」（§2.1）/ 引入方式为直推无 PR / 推荐修法 F-2 已获 Owner 批准但未执行，实际执行 F-1（§14）
L282: 
L283: Owner 裁定（2026-11-21）摘要：

### EN  path=docs/en/14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md
L45: 
L46: - Register ID: GOV-NC-2026-11-21-GATE-DEADLOCK-006
L47: - Status: `ACCEPTED` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY` (Owner ruling 2026-11-21, section 14) / the empty diff returned `EXIT=2` from `ae37a419` until `81dd9a72d2` (section 12)
L48: - Found at: 2026-11-21T05:05Z (last verified 2026-11-21T05:40Z @ `7d2233a5be`)
L49: - Introducing commit: `ae37a41900f1` (2026-11-21T04:50:35Z, **pushed straight to main, no PR**)
...
L279: **Register status**: `ACCEPTED` / `F-2_APPROVED` / empty diff on main is permanently `EXIT=2` / the dividing line is "did the PR supply two-sided mirrors", not "which file did it touch" (§2.1) / introduced by direct push with no PR / recommended fix F-2 approved by the Owner, not executed
L280: 
L281: Owner ruling (2026-11-21), summarised:
L282: 
L283: - Section 2.1's boundary correction is adopted; the first draft's "any PR gets `EXIT=2`" is withdrawn as too broad.

### ZH  path=docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-GATE-DEADLOCK-006.md
L45: 
L46: - 登记编号：GOV-NC-2026-11-21-GATE-DEADLOCK-006
L47: - 状态：`RESOLVED_ON_MAIN` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY`（Owner 2026-11-21 裁定，见 §14）/ 解除方式为自我审查合并，见 §12
L48: - 发现时间：2026-11-21T05:05Z（last verified 2026-11-21T05:40Z @ `7d2233a5be`）
L49: - 引入提交：`ae37a41900f1`（2026-11-21T04:50:35Z，**直推 main，无 PR**）
...
L279: ```
L280: 
L281: **登记状态**：`ACCEPTED` / `F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY` / main 上空 diff 恒为 `EXIT=2`（`81dd9a72d2` 起解除，见 §12）/ 判定分界是「是否补双侧镜像」而非「改了哪个文件」（§2.1）/ 引入方式为直推无 PR / 推荐修法 F-2 已获 Owner 批准但未执行，实际执行 F-1（§14）
L282: 
L283: Owner 裁定（2026-11-21）摘要：


# 要求

1. 给出**三个** `REPLACE` 块，分别改 `CANONICAL`、`EN`、`ZH` 三个路径的该段。三份必须同改（否则双语门禁 `check_mirror_pairing` 直接 FAIL）。
2. 改法约束：
   - 状态值统一为 `RESOLVED_ON_MAIN`；
   - 删掉/改写已被 §12 证伪的 "empty diff on main is permanently `EXIT=2`"（en）与"main 上空 diff 恒为 `EXIT=2`"（zh）；
   - **保留** 仍然成立的判定分界句（"是否补双侧镜像"）、引入方式句（直推无 PR）、以及 F-2 已批准未执行/实际执行 F-1 的说明；
   - 不要新增未在本文档出现过的结论或数字；不要改动其它段落。
3. 中文两份（CANONICAL 与 ZH）改后必须逐字一致；英文那份保持与中文同义的英文表达。
4. `OLD` 必须是单行逐字匹配（该段是单行 Markdown 段落），不要跨行。
5. 若你认为保留 "F-2_APPROVED; F-1_EQUIVALENT_FOR_TEMPLATE_ONLY" 这一段会与 `RESOLVED_ON_MAIN` 冲突，先给一句判断，再给块。

# 输出契约

```
===FILE: <路径>|REPLACE===
---OLD---
<逐字单行>
---NEW---
<逐字单行>
===END===
```

只输出判定句（若有）+ 三个块，不要计划。
