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
        - "14-ai-development/work-items/AID-2026-013/session-evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "投递提示词正文按原始字节拼接；最终文件摘要与字节数待协调方实测回填。"
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
    canonical_scope: "AID-2026-013 original implementation task prompt"
    canonical_scope_id: "ai-development/aid-2026-013-prompt"
    canonical_scope_keywords:
      - "AID-2026-013"
      - "implementation prompt"
      - "GOV-DOC-002"
      - "concurrency"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "AI-assisted implementation; human-directed"
---

# 任务：修掉 GOV-DOC-002 会静默吞掉 required context 的并发组缺陷（AID-2026-013）

你是本工作项的实现与登记材料作者。仓库 `oahcom/AiMemoryBrainArchitecture`，基线 `origin/main` = `3d9b32bef6775974117ea0ab925179acf43c6ecb`（2026-11-28）。工作项 ID `AID-2026-013`（`14-ai-development/work-items/AID-2026-013/` 不存在，三方均为空，不要再去枚举）。

你只需要产出文本：一个精确 EDIT、四个文件的内容、一行 INDEX 行、PR 标题与正文。落盘、提交、push、开 PR 由协调方机械执行。

## 一、缺陷（已完整取证，直接采用，不要再查证）

`.github/workflows/document-management.yml` 第 1–9 行现状（逐字节，LF 换行）：

```
# Work-item uniqueness is a shared target-branch invariant, not a
# per-candidate invariant. PRs targeting the same branch must not run this
# gate in independent concurrency groups. Do not cancel a running decision
# when another candidate arrives.
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.base.ref || github.ref_name }}
  cancel-in-progress: false
```

事实：

- 所有目标 `main` 的 PR 共用同一个 group 字符串；`cancel-in-progress: false` 只保护「正在跑的」，**排队位只有一个，后来的 run 会顶掉排队中的 run**。
- 实测：全仓 `status=cancelled` 共 281 条，其中本 workflow 9 条。PR #1443 在 head `938e160f` 上 `GOV-DOC-002 metadata checks` **完全没有 check run**（run `45963399555` 被 cancelled，同秒同 group 的 PR #1448 的 run 成功）。平台侧该 required context 永久 absent → PR 卡死且没有任何失败信息。
- 全仓 19 个 open PR、1155 个远端分支里没有任何一个在改这三行；旧形态分支要么是 `head.sha` 分组 + `cancel-in-progress: true`（方向相反），要么是常量共享组（同一缺陷换写法）。

## 二、必须满足的 5 条

1. `group` 改为按事件与 PR 区分：`${{ github.workflow }}-${{ github.event_name }}-${{ github.event.pull_request.number || github.ref_name }}`（PR 事件用 PR 号，push/其它用 ref）。
2. `cancel-in-progress: false` **保留**（同一 PR 内不取消正在跑的决策）。
3. 第 1–5 行注释改写为真实取舍：为什么可以放弃「全 PR 串行」，以及被放弃的到底是什么。
4. **只改这三行 + 注释**，不得动任何 job / step / name。特别确认 `jobs.document-management.name` 仍是 `GOV-DOC-002 metadata checks`（它是 16 条 required context 之一，改名等于让 required context 永久消失）。
5. 不引入任何新触发器，不改 `on:`。

## 三、注释可以使用的唯一事实集（不得编造，尤其不得声称 `strict: true`）

- 该 job 只读：`permissions: contents: read`，无写操作、无共享可变状态，两次运行之间不存在需要互斥的资源。
- 决策在执行时重新取目标分支：step `Enforce work-item uniqueness against the current target base` 会 `git fetch origin "+refs/heads/${BASE_REF}:..."` 并对生成的 merge candidate 求值，不用 PR 事件里的陈旧 base SHA。
- 陈旧通过会被 required context `Branch freshness vs base` 拦住：head 不含 base 即失败 → 必须追平 → `synchronize` 事件 → 本 workflow 连同 16 条 required 一起重跑。**注意：branch protection 的 `strict` 实测为 `false`（2026-11-28 API 实测），注释里不得写 `strict: true`，追平机制要用上面这个 required context 表述。**
- 被放弃的是什么：跨 PR 的「全局串行决策」。它从未真正成立——排队位只有 1 个，后到的 run 顶掉排队中的 run；281 条 cancelled（本 workflow 9 条）与 PR #1443 永久缺失 `GOV-DOC-002` 就是它的代价。
- 保留的是什么：同一 PR 内新提交不取消正在跑的决策；每个 PR 的并发组互相独立，后来的 PR 不会再顶掉别人的排队 run。

注释用英文写（与文件现有风格一致），4–6 行，须点明：只读、执行时重新取目标分支求值、追平由 `Branch freshness vs base` 强制重跑、放弃的是从未成立的全局串行。

## 四、产出格式（严格按分隔符，不要额外解释）

### 1) EDIT

```
===EDIT===
FIND:
<逐字节原文：上面第 1–9 行，含注释与 concurrency 两行>
REPLACE:
<新文本：新注释 + concurrency 两行>
===END EDIT===
```

FIND 必须在文件中唯一匹配（文件里 `concurrency:` 只出现一次，但注释首句可能被其它文件引用——以本文件内唯一为准）。只包含这 9 行，不要带 `name:` 行。

### 2) 四个文件

```
===FILE 14-ai-development/work-items/AID-2026-013/manifest.yaml===
<内容>
===FILE 14-ai-development/work-items/AID-2026-013/evidence.md===
<内容>
===FILE 14-ai-development/work-items/AID-2026-013/session-evidence.md===
<内容>
===INDEX ROW===
<单行 Markdown 表格行>
```

`prompt-v1.md` 不需要你写内容：协调方会把本次投递的提示词原文逐字节复制成该文件（`executed_prompt_snapshot_file`），你只需在 manifest / session-evidence 里如实声明这一点。

### 3) PR

```
===PR===
TITLE: fix(ci): give every pull request its own document-management concurrency group (AID-2026-013)
BODY:
<完整 Markdown 正文>
===END PR===
```

TITLE 用上面这一行原文。BODY 必须含：

- `## Work Item ID` 段：`AID-2026-013`
- `AI-assisted work: YES`
- `## Session evidence` 段：指向 `14-ai-development/work-items/AID-2026-013/session-evidence.md`，写 `implementing_ai_session: {{CONV_ID}}`
- Per-Issue 段写 `None.`（**不得引用 #1145**，也不得引用任何其它 Issue）
- 明确声明：本次改动只影响 concurrency group，job 名与所有 step 未变，16 条 required context 的产出不受影响
- 实测证据：改前全仓 281 条 `cancelled`、本 workflow 9 条；PR #1443（head `938e160f`）的 `GOV-DOC-002` 曾完全无 run（run `45963399555` 被 cancelled，同秒同 group 的 PR #1448 run 成功）
- 说明 `cancel-in-progress: false` 保留，以及被放弃的是「从未成立的全局串行」

## 五、manifest.yaml 硬性要求

- `work_item_id: AID-2026-013`
- `class` 与 `risk` / `risk_rationale` 自定（建议 `GATE/CI` + R1 或 R2，理由写清：只改并发组，不改 job/step/触发器）
- `status: DISPATCHED`，`id_status: PROVISIONAL`
- `sponsor` / `accountable_owner` / `acceptance_authority` / `attribution` / `date: "2026-11-28"` / `repository: oahcom/AiMemoryBrainArchitecture` / `base_branch: main`
- `base_commit_sha: "3d9b32bef6775974117ea0ab925179acf43c6ecb"`
- `tracking_issue: NONE`
- `scope`（summary / in_scope / files_out_of_scope / change_boundary）、`evidence`、`documentation`、`acceptance_criteria`（可执行、可测量）、`review`、`acceptance`、`implementation` 齐全
- `session_evidence` 为**单元素**列表：
  - `role: IMPLEMENTATION_SESSION`
  - `issue_refs: []`
  - `implementing_ai_session: {{CONV_ID}}`（**单值**，不是列表）
  - `executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-013/prompt-v1.md`
  - `executed_prompt_sha256: {{PROMPT_SHA256}}`（64 hex，占位符由协调方机械替换）
  - `executed_prompt_bytes: {{PROMPT_BYTES}}`（整数，占位符同上）
  - `executed_prompt_provenance: NOT_VERIFIED`
  - `session_reference_status: RECORDED`
  - `session_evidence_ref: 14-ai-development/work-items/AID-2026-013/session-evidence.md`
- `implementation.status: IMPLEMENTED`；`files_changed` 列 6 项：`.github/workflows/document-management.yml`、`14-ai-development/work-items/AID-2026-013/{manifest.yaml,evidence.md,session-evidence.md,prompt-v1.md}`、`14-ai-development/work-items/INDEX.md`；`tests` 列本次实际执行的 6 条门禁命令（见下）；`pull_request: 0`（开 PR 后回填，占位用 `0` 并在 summary 说明待回填）、`ci_status: NOT_CLAIMED`、`merge_commit: ""`
- 顶层必需键（schema v2）：`work_item_id, title, class, risk, risk_rationale, status, id_status, sponsor, accountable_owner, acceptance_authority, attribution, date, repository, base_branch, base_commit_sha, scope, evidence, documentation, session_evidence, implementation`

## 六、Markdown 文件的 document_metadata frontmatter（每个 .md 必须有）

`evidence.md` 与 `session-evidence.md` 必须以如下 frontmatter 开头（字段齐全，值按本工作项如实填写；`domain: ai-development`；`role: work-record` / `evidence` 择一；`steward` 与 manifest 的 `attribution` 一致；`lifecycle.evidence_verification.verification_status: Unverified`，`last_verified_date: "2026-11-28"`）：

```yaml
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
        - "14-ai-development/work-items/AID-2026-013/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "<一句话：任务输入与产出已记录；会话身份、精确提示词字节与独立执行来源未验证>"
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
    canonical_scope: "<本文件范围>"
    canonical_scope_id: "ai-development/aid-2026-013-<slug>"
    canonical_scope_keywords:
      - "AID-2026-013"
      - "<keyword>"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "<与 manifest attribution 一致>"
---
```

## 七、session-evidence.md 硬性要求

- 含 `## Session identity` 段（YAML 块，字段与 manifest 的 `session_evidence` 完全一致，`implementing_ai_session: {{CONV_ID}}`、sha/bytes 用同一占位符）
- 含 `## Session role` 段：本会话是 AID-2026-013 的实现会话，只改 concurrency 组与注释，不改 job/step/name/触发器
- 含 `## Actual AI input` 段：**必须非空**，逐条列出本次投递的实际输入（缺陷事实、5 条要求、16 条 required context 清单、注释可用事实集），并包含真实送达行占位 `{{SEND_LINE}}`（协调方第二轮替换为真实 `SEND <prompt-file> -> 200` 行，你原样保留该占位符，不要自己编造送达行）
- 含 `## AI-visible output` 段：列出本会话产出的 5 项（manifest / evidence / session-evidence / INDEX 行 / PR 文案），并声明未声称已落盘、已过门禁、已合并
- 不得声称已获独立审查、Owner 验收或 CI 成功

## 八、evidence.md 内容要求

记录：缺陷取证数字（281 / 9 / PR #1443 head `938e160f` / run `45963399555` / 同秒 PR #1448 成功 / 19 open PR / 1155 分支无冲突改动）；改前三行原文与改后三行原文；为什么 per-PR 分组可接受（只读 + 执行时重新取目标分支 + `Branch freshness vs base` 强制追平重跑）；`strict` 实测 `false` 因此不援引它；job 名不变与 16 条 required context 清单（逐条列出：`GOV-DOC-001 structural checks`、`Branch freshness vs base`、`audit`、`GOV-DOC-002 metadata checks`、`BMCP protocol index (hard gate)`、`BMCP conformance suite (hard gate)`、`Schema non-empty audit (hard gate)`、`Bilingual docs coverage (ratchet)`、`Rust clippy (hard gate)`、`Repository hygiene (hard gate)`、`Rust format (hard gate)`、`Rust doctests (hard gate)`、`Session Evidence`、`Session Evidence self-test (base)`、`Session Evidence self-test (head)`、`rust-workspace-test`）；本次将执行的 6 条门禁命令。

## 九、INDEX 行

`14-ai-development/work-items/INDEX.md` 表头为 9 列：
`| Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance |`

只给一行，置于表末（表格最后一行之后），格式与现有行一致，链接写 `[AID-2026-013](AID-2026-013/manifest.yaml)`。Status 写 `DISPATCHED — id_status: PROVISIONAL; concurrency group 改为 per-PR; 等待 CI 与合并`；Review 写 `NOT_ASSIGNED — 未记录独立审查`；Acceptance 写 `PENDING — 未声称 Owner 验收或 CI 成功`。

## 十、本次将执行的本地门禁（写进 manifest.tests 与 evidence.md）

```
python -c "import yaml;d=yaml.safe_load(open('.github/workflows/document-management.yml',encoding='utf-8'));print(d['jobs']['document-management']['name']);print(d['concurrency'])"
python scripts/ci/check_manifest_parse.py
python scripts/check_traceability.py --index-only
python scripts/check_document_management.py --require-changed origin/main
python scripts/ci/check_work_item_uniqueness.py --base origin/main --head HEAD
python scripts/check_declared_check_contexts.py
```

## 十一、纪律

- 不写"如果…则…"的条件分支；直接给最终文本。
- 占位符只允许 `{{CONV_ID}}`、`{{PROMPT_SHA256}}`、`{{PROMPT_BYTES}}`、`{{SEND_LINE}}` 四个，全部原样保留。
- 不引用 #1145；不声称任何未验证的 CI/审查/验收状态。
