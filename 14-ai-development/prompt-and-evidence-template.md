---
document_metadata:
  domain: ai-development
  role: reference
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
    canonical_conflict_status: None
---

# AI Work Item and Prompt Record Template
# AI 任务与提示词记录模板

**Document ID:** AI-TPL-001  
**Version:** 1.0  
**Status:** PROPOSED

Copy this template for each work item. Store the approved prompt as an immutable version before the AI run.

## 1. Work item manifest / 任务登记

```yaml
work_item_id: "AID-YYYY-NNN"
title: ""
class: "ARCH | IMPL | TEST | SEC | MIG | PERF | DOC | OPS"
risk: "R0 | R1 | R2 | R3"
status: "PROPOSED"
sponsor: ""
accountable_owner: "A | B | C | D | E | F | G | H | I | CROSS-CUTTING"
implementing_ai_session: ""
independent_reviewer: ""
integration_reviewer: ""
acceptance_authority: ""
repository: "oahcom/AiMemoryBrainArchitecture"
base_branch: ""
base_commit_sha: ""
dependency_refs: []
prompt_id: ""
prompt_version: "v1"
prompt_sha256: ""
# Exact payload sent to this session after composing baseline + task-specific instructions.
executed_prompt_snapshot_file: ""
executed_prompt_sha256: ""
executed_prompt_bytes: null
executed_prompt_provenance: "VERIFIED | NOT_VERIFIED | NOT_AVAILABLE"
session_reference_status: "RECORDED | NOT_AVAILABLE | NOT_RECORDED"
session_evidence_ref: ""
created_at: ""
updated_at: ""
implementation_branch: ""
implementation_commits: []
changed_paths: []
documentation:
  architecture_significant: true
  policy_id: "GOV-DOC-001"
  chinese_paths: []
  english_paths: []
  source_revision: ""
  parity_review: "NOT_STARTED"
  coverage_register_updated: false
verification:
  status: "NOT_RUN"
  commit_sha: ""
  commands: []
  evidence_refs: []
evidence_tiering:
  repository: ""
  change_class: "ARCHITECTURE | SECURITY | PERFORMANCE_CRITICAL | PUBLIC_API | DATA_MIGRATION | DOC_NORMATIVE | FEATURE | BUGFIX | DOC_EDITORIAL | OPS | UNKNOWN"
  review_level: "R0 | R1 | R2 | R3"
  evidence_level: "1 | 2 | 3"
  assessed_by: ""
  assessed_at: ""
  rationale: ""
  base_head: ""
  classification_basis: ""
  classification_confirmed_by: ""
  classification_record: ""
  downgrade_justification: ""
  downgrade_confirmed_by: ""
  downgrade_confirmation_record: ""
  escalation_target: ""
  checker_result: "NOT_RUN"
  declaration_path: "evidence-declaration.yaml"
review:
  status: "NOT_STARTED"
  report_ref: ""
  findings: []
acceptance:
  status: "PENDING"
  record_ref: ""
merge:
  target_branch: ""
  merge_commit_sha: ""
  status: "NOT_MERGED"
```

## 2. Prompt content / 提示词正文

# [Work Item ID] — [Task Title]

## Role
You are the [named Owner / specialist] for repository `oahcom/AiMemoryBrainArchitecture`.

## Objective
Describe the observable outcome. Do not describe an unapproved implementation as a requirement.

## Authoritative inputs
List exact file paths, branch names, commit SHAs, ADRs, decisions and relevant test fixtures. If a source is unavailable, stop and report it.

## Authority and ownership
- You own:
- You may modify:
- You must not modify:
- Required consultations/approvals:

## Scope
### In scope
- ...

### Out of scope
- ...

## Constraints and invariants
List normative requirements, trust boundaries, compatibility requirements, state-machine invariants and non-negotiable project rules.

## Required work
Provide ordered, bounded steps. Require inspection before modification. Identify design decisions that may be made by this Owner and decisions that must be escalated.

## Acceptance criteria
Each criterion MUST be objectively verifiable. Avoid “high quality”, “robust” or “complete” without a measurable condition.

1. [ ] ...
2. [ ] ...
3. [ ] ...

## Verification plan
List exact commands, tests, fixtures, expected results and required fault/security cases. Mark unavailable checks as NOT RUN with a reason.

## Mandatory bilingual requirement for every AI developer (GOV-DOC-001)

Every AI developer/session MUST read GOV-DOC-001 before starting. This applies to architecture, implementation, testing, security, storage, protocol, performance, migration, operations, and review work. Inspect both language counterparts for affected contracts. If the task creates or changes architecture meaning, constraints, interfaces, behavior, tests, acceptance criteria, technology decisions or implementation guidance, update/create both Chinese and English versions in this same change set. If code/tests reveal a contract change, update the owning specification rather than treating the task as implementation-only. Preserve normative force, decision status and stable identifiers. Update the coverage register. A missing counterpart is NOT DONE unless a formally approved, time-bounded STALE exception records owner, source revision, due date and tracking issue.

## 所有 AI 开发者的强制双语要求（GOV-DOC-001）

每位 AI 开发者/会话在开始前 MUST 阅读 GOV-DOC-001。本要求覆盖架构、实现、测试、安全、存储、协议、性能、迁移、运维和审查工作。检查受影响契约的中英文版本。如果任务新增或改变架构含义、约束、接口、行为、测试、验收条件、技术决策或实现指导，必须在同一个变更集中创建/更新中英文版本。如果代码/测试揭示契约发生变化，必须更新所属规范，不能将任务视为纯实现工作。保持规范效力、决策状态和稳定标识一致，并更新覆盖登记表。缺少对应版本时属于 NOT DONE，除非正式批准有期限的 STALE 例外，并记录责任人、源版本、截止日期和跟踪 Issue。

## Required deliverables
- Chinese documentation paths:
- English documentation paths:
- Bilingual parity checklist/evidence:
- Coverage register update:
- Modified/new files:
- Decision/change log:
- Tests:
- Review evidence:
- Final report:

## Stop conditions
Stop and report if:
- a required source or dependency SHA is unavailable;
- authoritative contracts conflict;
- the task requires another Owner's decision;
- a security/data-integrity invariant cannot be maintained;
- acceptance criteria cannot be verified;
- unexpected files or migrations fall outside scope.

## Git and evidence requirements
- Work only on the assigned branch.
- Do not merge other branches.
- Commit with a meaningful message.
- Report full branch HEAD SHA and commit SHA.
- Read back changed files after writing.
- Report changed paths and test evidence.
- Do not claim success for unrun checks.

## Final report format
1. Work Item ID / Prompt ID and version.
2. Actual branch and base/head SHAs.
3. Sources read with exact SHAs.
4. Changes and rationale.
5. Acceptance criteria: PASS / FAIL / NOT RUN, with evidence.
6. Tests: command, environment, expected/actual, result.
7. Independent-review handoff notes.
8. Open questions, risks and dependencies.
9. Commit SHA and read-back verification.
10. Bilingual parity status and Chinese/English paths (or approved STALE exception).
11. Honest final status: IMPLEMENTED / VERIFIED / BLOCKED / PARTIAL.

## 3. Prompt versioning rules / 提示词版本规则

- Use immutable prompt versions: `prompt-v1.md`, `prompt-v2.md`, etc.
- Compute SHA-256 for each approved prompt file and store it in the manifest.
- Any material change to scope, acceptance criteria, authority, dependencies or procedure requires a new version.
- A correction to spelling that cannot change interpretation may be recorded as a non-semantic edit, but the stored artifact and hash must still be updated before execution.
- Record which version was actually used by each AI run.
- Never overwrite a prompt version that has already been executed.
- If a run used an unrecorded conversational clarification, append it as a dated run addendum and assess whether a new prompt version is required.

## 3.1 Executed prompt capture / 实际执行提示词留存

The reusable global/Owner prompt is a baseline, not necessarily the complete payload sent to a ChatGPT session. Before execution, preserve the exact task-specific payload actually supplied to the session as `executed_prompt_snapshot_file`. This snapshot MUST include the effective instructions after applicable baseline prompts and task-specific additions/clarifications have been composed. Do not reconstruct it from a summary or infer missing text.

Record its exact-byte SHA-256 and byte count in the manifest. Bind it to `implementing_ai_session` (or the relevant reviewer/session role) and `session_evidence_ref`. If the platform does not expose a stable session reference, use `session_reference_status: NOT_AVAILABLE` and explain the limitation in the evidence record; do not invent an identifier. If the original payload bytes cannot be recovered, use `executed_prompt_provenance: NOT_VERIFIED` or `NOT_AVAILABLE` and do not claim the prompt was captured.

可复用的全局/Owner 提示词是基线，不一定等于实际发送给 ChatGPT 会话的完整提示词。在执行前，必须将实际提供给会话的任务专属完整 payload 保存为 `executed_prompt_snapshot_file`。该快照必须包含适用基线提示词与任务专属补充/澄清组合后的有效指令。不得从摘要重建，也不得推测缺失文本。

在 manifest 中记录其原始字节 SHA-256 和字节数，并将其绑定到 `implementing_ai_session`（或相应审查者/会话角色）及 `session_evidence_ref`。如果平台不提供稳定会话引用，使用 `session_reference_status: NOT_AVAILABLE`，并在证据记录中说明限制；不得编造标识。如果无法恢复原始 payload 字节，使用 `executed_prompt_provenance: NOT_VERIFIED` 或 `NOT_AVAILABLE`，不得声称提示词已留存。

## 3.2 Canonical multi-session evidence container / 规范多会话证据容器

`session_evidence` is the canonical representation, and it is a repeatable list: one entry per session, including when there is only one session. Each entry carries `role`, `issue_refs` and all seven fields listed in section 1, is validated on its own, and must not share its `session_evidence_ref` with another entry.

Inside an entry the seven fields stay single-valued. A field must not join several values with a comma, semicolon, plus sign or whitespace; several sessions are expressed as several entries, never as one joined string. (`executed_prompt_bytes` is a nonnegative integer, not a string.)

A manifest with no `session_evidence` block is read as at most one legacy entry built from the seven top-level fields, and all seven must be present. Historical manifests are not rewritten to satisfy the policy: an unchanged file keeps that read path, and only a manifest that a pull request changes must use the canonical entries.

The two representations are mutually exclusive and fail-closed: a manifest that carries both top-level legacy fields and a `session_evidence` block is an error, never a merge, so the two can never become independently mutable sources of truth.

```yaml
session_evidence:
  - role: IMPLEMENTER
    issue_refs:
      - "#799"
    implementing_ai_session: session-799-orchestrator
    executed_prompt_snapshot_file: 14-ai-development/work-items/AID-YYYY-NNN/prompt-v1.md
    executed_prompt_sha256: "<64 hex>"
    executed_prompt_bytes: 3866
    executed_prompt_provenance: VERIFIED
    session_reference_status: RECORDED
    session_evidence_ref: 14-ai-development/work-items/AID-YYYY-NNN/session-evidence-799.md
```

`issue_refs` accepts `#number` or a canonical `https://github.com/<owner>/<repo>/issues/<number>` URL for this repository, and every Issue named there must also appear in the pull request's Related Issues. An entry may name an Issue whose row in the pull request's per-Issue table is `YES` or `LEGACY_UNDECLARED`; it may not name a `NO` row, because evidence cannot be attributed to an Issue that declares no AI involvement. `LEGACY_UNDECLARED` means no declaration exists because the Issue predates the policy, not that no AI was used, which is why attribution to it is allowed. A row mapped `YES` must still be represented by at least one entry. An entry may also carry an empty `issue_refs` when its evidence is attributed at pull-request scope only (recorded decision OD-A3), for a session whose work does not belong to any single linked Issue.

Enforcement lives in `scripts/governance/session_evidence/validate.py`: the validator, not this document, is the source of truth, and this section describes what it enforces.

`session_evidence` 是规范表示，且是可重复列表：一个会话一个条目，即使只有一个会话也是如此。每个条目包含 `role`、`issue_refs` 以及第 1 节列出的全部七个字段，逐条独立校验，且不得与另一个条目共用同一个 `session_evidence_ref`。

在单个条目内，七个字段保持单值。字段中不得用逗号、分号、加号或空白拼接多个值；多个会话应表达为多个条目，绝不能写成一个拼接字符串。（`executed_prompt_bytes` 是非负整数，不是字符串。）

没有 `session_evidence` 块的 manifest 按至多一条旧式（legacy）条目读取，由七个顶层字段构成，且七个字段必须齐全。历史 manifest 不为满足本策略而重写：未变更的文件沿用该读取路径，只有被 pull request 修改的 manifest 才必须使用规范条目。

两种表示互斥且失败关闭（fail-closed）：同时带有顶层旧式字段与 `session_evidence` 块的 manifest 属于错误，不做合并，二者因此不可能成为两个可独立变更的事实来源。

`issue_refs` 接受 `#number` 或本仓库的规范 URL `https://github.com/<owner>/<repo>/issues/<number>`，其中列出的每个 Issue 都必须同时出现在 pull request 的 Related Issues 中。条目可以为一个 Issue 归属证据，前提是它在 pull request 的逐 Issue 表中映射为 `YES` 或 `LEGACY_UNDECLARED`；条目不得指向 `NO` 行，因为证据不得归属于声明未使用 AI 的 Issue。`LEGACY_UNDECLARED` 表示该 Issue 早于策略生效时间因而没有声明，并不表示未使用 AI，这正是允许向其归属证据的原因。映射为 `YES` 的行仍必须至少由一个条目表示。当证据仅在 pull request 范围归属时，也可以携带空的 `issue_refs`（记录为决策 OD-A3），适用于其工作不属于任何单个关联 Issue 的会话。

执行位于 `scripts/governance/session_evidence/validate.py`：事实来源是校验器而不是本文档，本节描述的是它所强制的内容。

## 3.3 Pull-request body contract — scope and effective date / 正文契约的适用范围与生效时间

The pull-request body contract applies to a pull request that carries an AI-authored change: it declares `AI-assisted work`, the per-Issue table, and the evidence behind the declaration. A pull request with no AI involvement is not exempt from declaring — it MUST say `AI-assisted work: NO` and put `N/A` in `Session evidence reference(s)`, because silence is indistinguishable from an undeclared AI contribution, and no gate can read an unexplained blank as a claim that none exists. The body contract is not gated on `AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC = 2026-12-01T00:00:00Z`, which sets when the evidence *data* requirement begins. `scripts/governance/session_evidence/validate.py` does apply one bounded exemption: a pull request created before `2026-12-01T00:00:00Z` that links only Issues which themselves predate that cutoff and carry no declaration of their own, and whose body carries neither `AI-assisted work` nor `Session evidence reference(s)`, validates as `NOT_APPLICABLE` and is never checked against this contract. The exemption does not extend to a pull request created at or after `2026-12-01T00:00:00Z`: such a pull request must declare, even when every Issue it links is historical.

PR 正文契约适用于承载 AI 编写改动的 pull request：它声明 `AI-assisted work`、逐 Issue 表格，以及声明背后的证据。没有任何 AI 参与的 pull request 并不因此免于声明——必须写 `AI-assisted work: NO`，并在 `Session evidence reference(s)` 中写 `N/A`，因为沉默与「未声明的 AI 参与」不可区分，也没有门禁能把一处无解释的空白读成「没有 AI 参与」的声明。正文契约不以 `AI_SESSION_EVIDENCE_EFFECTIVE_AT_UTC = 2026-12-01T00:00:00Z` 为门槛——该常量设定的是证据**数据**要求的起点。`scripts/governance/session_evidence/validate.py` 确实设有一处有界的豁免：创建于 `2026-12-01T00:00:00Z` 之前、只关联那些本身早于该截止时间且没有自身声明的 Issue、并且正文中既无 `AI-assisted work` 也无 `Session evidence reference(s)` 的 pull request，会校验为 `NOT_APPLICABLE`，完全不按本契约检查。该豁免不延伸到 `2026-12-01T00:00:00Z` 当时或之后创建的 pull request：这样的 pull request 必须声明，即使它关联的每个 Issue 都是历史 Issue。

## 4. Required evidence bundle / 必需证据包

Each completed implementation task should contain, as applicable:

- `manifest.yaml` — task identity and status;
- `prompt-vN.md` — exact executed instruction;
- `prompt.sha256` — prompt integrity digest;
- `implementation-report.md` — author report;
- `test-report.md` — reproducible checks;
- `review-report.md` — independent review;
- `decision-records/` — approved material decisions;
- `integration-report.md` — cross-owner acceptance;
- links to PR, commits and CI runs.

## 4.1 Evidence depth declaration / 证据深度声明

Every work item MUST declare its evidence depth before delivering, using the manifest `evidence_tiering` block and a machine-checkable declaration file (`evidence-declaration.yaml` in the work-item bundle):

```yaml
work_item: "AID-YYYY-NNN"
repository: "oahcom/AiMemoryBrainArchitecture"
change_class: "FEATURE"
review_level: "R2"
evidence_level: 2
subject_head: "<40-hex commit>"
base_head: "<40-hex ancestor commit>"
change_summary: "one-line description of the change"
classification_basis: "why this risk class applies"
assessed_by: "owner-x"
assessed_at: "2026-11-20T00:00:00+08:00"
rationale: "why this evidence depth is sufficient"
classification_confirmed_by: "reviewer-y"      # required for FEATURE/BUGFIX/DOC_EDITORIAL/OPS
classification_record: "14-ai-development/work-items/AID-YYYY-NNN/classification.md"     # must exist in the subject tree
downgrade_justification: ""                    # only for R2 -> Level 3
downgrade_confirmed_by: ""
downgrade_confirmation_record: ""
source_authenticity: "NOT_VERIFIED"
evidence:
  design_doc: "14-ai-development/work-items/AID-YYYY-NNN/design.md"
  impact_analysis: "14-ai-development/work-items/AID-YYYY-NNN/impact.md"
  test_log: "14-ai-development/work-items/AID-YYYY-NNN/test-report.md"
  review_record: "14-ai-development/work-items/AID-YYYY-NNN/review-report.md"
  rollback_plan: "14-ai-development/work-items/AID-YYYY-NNN/rollback.md"
  review_note: "14-ai-development/work-items/AID-YYYY-NNN/review-ack.md"   # path to the acknowledgement record, not free text
binding:
  protocol: "v3"
  sidecar_path: "evidence.sha256"              # Level 1 only
  sidecar_anchor: "sha256:<64 hex>"            # Level 1 only
authenticity:
  acknowledged: "true"
  verification_record: "..."
```

Rules:
- `evidence_level` is an evidence depth selector, independent of `review_level`, the twelve states and the six phases (AI-STD-001 §4.2.1).
- Level 1 is mandatory for ARCHITECTURE, SECURITY, PERFORMANCE_CRITICAL, PUBLIC_API, DATA_MIGRATION, DOC_NORMATIVE and every R3 change.
- `UNKNOWN` is BLOCKED; it MUST NOT receive a level.
- Every level keeps a full 40-hex `subject_head` and `change_summary`, and v3 binding is verified against real Git objects at every level (protocol, subject-tree containment, blob equality); Level 1 additionally anchors a sidecar digest.
- `assessed_by`, `assessed_at`, `rationale`, `base_head` and `classification_basis` are machine-checked; a missing field is BLOCKED.
- The manifest `evidence_tiering` block and `evidence-declaration.yaml` MUST stay in sync on all of: `change_class`, `review_level`, `evidence_level`, `subject_head`, `base_head`, `classification_confirmed_by`, `classification_record`, `downgrade_justification`, `downgrade_confirmed_by`, `downgrade_confirmation_record`. A mismatch is a declaration defect and BLOCKED by review.
- `classification_record` and `downgrade_confirmation_record` are verified as Git objects (present in the subject tree, worktree bytes equal to the subject blob); a non-existent path is BLOCKED.
- `repository` MUST match the clone's `origin` remote; an unverifiable or mismatched identity is BLOCKED.
- Validate with `python scripts/governance/evidence/check-evidence-tiering.py <declaration>`, and record the per-scenario `VERDICT` / `REASON` output as evidence. An exit code alone is not acceptance evidence.
- Evidence paths are interpreted against the repository root of `subject_head`, not against the directory holding the declaration; `evidence.review_note` is a path to an acknowledgement record, never free text.

每个工作项在交付前 MUST 声明证据深度，使用 manifest 的 `evidence_tiering` 块与可机器校验的 `evidence-declaration.yaml`。`evidence_level` 是证据深度选择器，独立于 `review_level`、十二状态与六阶段（AI-STD-001 §4.2.1）。ARCHITECTURE、SECURITY、PERFORMANCE_CRITICAL、PUBLIC_API、DATA_MIGRATION、DOC_NORMATIVE 及所有 R3 变更强制 Level 1；`UNKNOWN` 为 BLOCKED，不得赋级；所有等级保留 40 位 `subject_head` 与 `change_summary`，v3 绑定在所有等级均对真实 Git 对象校验（protocol、subject tree 包含、blob 一致），Level 1 另加 sidecar 摘要锚定。`assessed_by`、`assessed_at`、`rationale`、`base_head`、`classification_basis` 均经机器校验，缺失即 BLOCKED。manifest 的 `evidence_tiering` 块与 `evidence-declaration.yaml` MUST 在 `change_class`、`review_level`、`evidence_level`、`subject_head`、`base_head`、`classification_confirmed_by`、`classification_record` 及三个 `downgrade_*` 字段上保持一致，不一致即声明缺陷并在审查中 BLOCKED。`classification_record` 与 `downgrade_confirmation_record` 按 Git 对象校验（须在 subject tree 且工作树/blob 一致），填写不存在的路径即 BLOCKED；`repository` 须与克隆的 `origin` 远程一致，无法核验或不符即 BLOCKED。使用检查器校验并记录逐项 `VERDICT`/`REASON` 输出，仅退出码不足以作为验收证据。证据路径按 subject 提交的仓库根解析（不相对声明文件所在目录）；`evidence.review_note` 须为指向确认记录的路径，不得填写自由文本。

## 5. Canonical prompt library and evidence layout / 规范提示词库与证据目录

Reusable prompts MUST first be stored in the repository-root `prompts/` library:
- Global prompts: directly under `prompts/`.
- Owner prompts: `prompts/A/` through `prompts/I/`.
- Every task prompt MUST reference the global prompts and applicable Owner prompt IDs.
- Before execution, copy the exact prompt text into the work-item evidence bundle, compute SHA-256, and never overwrite an executed version.

See [Prompt Library](../prompts/README.md).

可复用提示词必须先存入仓库根目录的 `prompts/`：全局提示词直接放在根目录，Owner 专属提示词放入各自目录。每项任务提示词必须引用全局提示词和适用的 Owner 提示词 ID。执行前将准确提示词复制到 Work Item 证据包并计算 SHA-256；已执行版本不得覆盖。

## 6. Suggested repository layout / 建议目录

```text
14-ai-development/
  README.md
  ai-development-standard.md
  iteration-lifecycle.md
  prompt-and-evidence-template.md
  prompts/
    global/
      chatgpt-session-contract-v1.md
    owners/
      A/owner-session-v1.md
      B/owner-session-v2.md
      C/owner-session-v1.md
      D/owner-session-v2.md
      E/owner-session-v1.md
      F/owner-session-v1.md
      G/owner-session-v1.md
      H/owner-session-v1.md
      I/owner-session-v2.md
  work-items/
    INDEX.md
    AID-YYYY-NNN/
      manifest.yaml
      prompt-v1.md
      prompt.sha256
      implementation-report.md
      test-report.md
      review-report.md
      decision-records/
```

For a multi-owner parent task, use one parent folder with child work items or explicit Owner-specific child IDs. Keep each prompt and evidence bundle immutable and linkable. Do not store secrets, credentials, private user data or raw sensitive production data in prompts or reports.


## 7. GitHub delivery carrier and closeout / GitHub 交付载体与结项记录

Before execution, fill in the owning Issue/PR URL and Work Item ID. Prefer an existing carrier; do not open a duplicate PR for the same integration unit. During work, update the carrier with material progress, decisions, changed commits/paths, verification evidence and blockers.

Required closeout fields:
- Session ID / Prompt ID / version / SHA-256:
- Work Item ID:
- Owning Issue URL:
- Related PR URL(s):
- Accountable Owner / Implementing session / Independent Reviewer:
- Repository / branch / base SHA / final Head SHA:
- Changed paths and commit SHAs:
- Work performed:
- Decisions and authority (PROPOSED / ACCEPTED / REJECTED / UNRESOLVED):
- Verification commands, environment, exact tested SHA, result and evidence links:
- Required checks NOT RUN and reasons:
- Review/integration disposition and reviewer-independence disclosure:
- Dependencies, blockers, follow-up Owner and closure condition:
- Merge status / target branch / merge commit SHA / post-merge checks:
- Work Item index row updated: YES / NO.

A blocked or no-change assigned session still records its outcome against the carrier. Never fabricate a prompt hash, test result, review, Owner approval or merge record.

执行前填写归属 Issue/PR URL 和 Work Item ID。优先复用现有载体；同一集成单元不得重复开 PR。工作期间及时更新重要进展、决策、变更 Commit/路径、验证证据和阻塞。

结项必须填写以上全部字段。受阻或无变更的已分配会话仍须在载体中记录结果。禁止伪造提示词哈希、测试结果、审查、Owner 批准或合并记录。
