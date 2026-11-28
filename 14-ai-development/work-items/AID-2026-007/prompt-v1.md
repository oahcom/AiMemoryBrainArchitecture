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
        - "14-ai-development/work-items/AID-2026-007/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "This file is the byte-exact registration prompt sent to the AI session; the measurements it quotes were produced by the coordinating operator and are recorded in evidence.md."
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
    canonical_scope: "Registration prompt for work item AID-2026-007 (session identity ratchet)."
    canonical_scope_id: "ai-development/aid-2026-007-prompt-v1"
    canonical_scope_keywords:
      - "AID-2026-007"
      - "prompt"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-007 registration prompt, v1

你负责产出工作项 AID-2026-007 的注册材料。下面是不可更改的事实包与输出契约。不要重新论证已完成的事实，不要新增未给出的数字。

## 0. 输出协议（强制）

- 每个文件以单独一行 `@@FILE@@ <repo-relative-path>` 开始，紧接着是该文件的完整内容；下一个 `@@FILE@@` 或结尾 `@@END@@` 终止上一个文件。`@@FILE@@` 与 `@@END@@` 只用于分界，不要出现在文件正文里。
- 只输出文件，不输出前言、解释、结语；不要用代码围栏把整份输出包起来。
- 输出五个块，顺序固定：`manifest.yaml`、`evidence.md`、`session-evidence.md`、`INDEX-ROW`、`PR-TITLE`、`PR-BODY`。
- `INDEX-ROW` 块只输出一行 Markdown 表格行；`PR-TITLE` 块只输出一行标题；`PR-BODY` 块输出 PR 正文全文。
- **`prompt-v1.md` 不由你输出**：它由协调方以本消息的字节原文落盘到 `14-ai-development/work-items/AID-2026-007/prompt-v1.md`。你只在 manifest 与 session-evidence 中引用该路径，并把 `executed_prompt_sha256` / `executed_prompt_bytes` 写成占位符，由协调方按实际落盘文件机械替换。

## 1. 事实包（已核实，直接引用）

- 仓库：`oahcom/AiMemoryBrainArchitecture`；目标分支 `main`；工作分支 `feat/2026-11-27-session-identity-ratchet`。
- 分支三提交（已 rebase 到 `origin/main`）：
  - `70c7c2f5` feat(gov): add a session-identity ratchet with a shrink-only baseline (AID-PENDING)
  - `ae6aa4c9` feat(gov): require an explicit git-verified bootstrap for the session-identity baseline (AID-PENDING)
  - `e8b60848` docs(gov): align the session-identity design with the git-verified bootstrap (AID-PENDING)
- `base_commit_sha`：`561e9f2471d09828cf7a91dc5b24bbfe82b2e213`（rebase 时的 `origin/main`，全 40 位）。
- 本分支改动文件：
  - `scripts/ci/check_session_identity.py`
  - `scripts/ci/test_check_session_identity.py`
  - `scripts/ci/baselines/session-identity.txt`（74 条基线）
  - `.github/workflows/session-identity-ratchet.yml`
  - `14-ai-development/design/session-identity-ratchet.md`
  - `14-ai-development/PR-GOVERNANCE-001.md`
- 本地门禁实测（逐字引用）：
  - `python scripts/ci/check_session_identity.py` → `SESSION IDENTITY: 74 violations, 74 baselined, 0 new`，exit 0
  - `python -m unittest scripts.ci.test_check_session_identity` → `Ran 27 tests` / `OK`
  - `python scripts/check_document_management.py --require-changed origin/main` → exit 0
  - `python scripts/ci/check_manifest_parse.py` → `Manifest parse: 136 manifests found, 136 parsed, 0 failed.`
- 执行会话（真实，单值）：`6b09360b-13cc-83ec-abfd-aa0e6362566c`（ChatGPT 会话 id，同时是本包 AI 执行会话标识；第三组 `83ec` 满足本仓 UUID 形状校验）。
- 投递记录（真实）：`SEND 6b09360b-13cc-83ec-abfd-aa0e6362566c -> 200`。
- 工作项编号：`AID-2026-007`（主分支 001–006 已占用、007 空号；19 个 open PR 的 title+body 均未声明 007）。
- 本 PR 不引用任何 Issue。
- 新增 GitHub 上下文：`Session identity ratchet` 作为 check 上下文存在，但**不设为 required**；required 仍为 16 条。

## 2. `14-ai-development/work-items/AID-2026-007/manifest.yaml`

必须是合法 YAML（无重复键），字段如下（键名照抄，值按事实包填）：

- `work_item_id: AID-2026-007`
- `title`：一句话说明新增会话身份棘轮（shrink-only 基线 + 显式 Git 校验 bootstrap）。
- `class: GATE/CI`；`risk: R2`；`risk_rationale`：说明新增 CI 检查器与工作流、基线只能收缩、bootstrap 需 Git 校验，不改生产运行时代码。
- `status: IMPLEMENTED`
- `id_status: PROVISIONAL`
- `sponsor` / `accountable_owner`: `USER-PRINCIPAL-DELEGATED`
- `acceptance_authority: NOT_ASSIGNED`
- `attribution: "user-authorized operator (delegated by account owner)"`
- `date: "2026-11-28"`
- `repository: oahcom/AiMemoryBrainArchitecture`
- `base_branch: main`
- `base_commit_sha: "561e9f2471d09828cf7a91dc5b24bbfe82b2e213"`
- `tracking_issue: NONE`
- `role: work-record`
- `steward: "user-authorized operator (delegated by account owner)"`
- `lifecycle`：映射，包含
  - `approval.decision_status: Draft`、`approval.approver: null`
  - `evidence_verification.verification_status: Verified`、`evidence_verification.last_verified_date: "2026-11-28"`、`evidence_verification.last_verification_note`（说明四条本地门禁由协调方实测，CI 结果以 PR 的 check-runs 为准）
  - `usage_status: Active`
  - `modification_status: Modified`
- `authority`：`canonical_status: Non-Canonical`、`canonical_conflict_status: None`、`normative_status: Informative`
- `scope`：`summary`、`in_scope`（六个改动面 + 四个新增工作项文档）、`out_of_scope`（不改既有 74 条基线条目、不改其它检查器、不改 `PR-GOVERNANCE-001.md` 之外的治理条款、不把 `Session identity ratchet` 设为 required）
- `evidence`：引用 `evidence.md`、`session-evidence.md`、`prompt-v1.md`、基线文件、工作流文件、设计文档、`base_commit_sha`
- `documentation`：三条，`relationship` 分别为 evidence / evidence / reference
- `acceptance`：`status: NOT_ASSIGNED`、`record_ref: ""`、`acceptance_authority: NOT_ASSIGNED`
- `acceptance_criteria`：AC1–AC6，分别对应四条本地门禁 + 基线只能收缩（新增违例必须修而不是入基线）+ 该上下文不设为 required
- `implementation`：`status: IMPLEMENTED`、`summary`、`pull_request: null`、`pull_request_url: null`、`merge_commit: ""`、`ci_status: NOT_CLAIMED`、`files_changed`（六个改动文件 + 四个新增文档 + `INDEX.md`）、`tests`（四条本地门禁命令原文 + `python scripts/ci/check_work_item_uniqueness.py --base origin/main --head HEAD` + `python scripts/check_traceability.py --index-only`）
- `session_evidence`：**一个条目**，字段为
  - `role: IMPLEMENTATION_SESSION`
  - `issue_refs: []`
  - `implementing_ai_session: 6b09360b-13cc-83ec-abfd-aa0e6362566c`（**单值字符串，不得写成列表、不得合并多值**）
  - `session_reference_status: RECORDED`
  - `session_evidence_ref: 14-ai-development/work-items/AID-2026-007/session-evidence.md`
  - `executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-007/prompt-v1.md`（仓库相对全路径，不是文件名）
  - `executed_prompt_sha256: "__PROMPT_SHA256__"`（占位符；协调方落盘后按实际文件机械替换为 64 位 hex）
  - `executed_prompt_bytes: __PROMPT_BYTES__`（占位符；协调方落盘后机械替换为整数）
  - `executed_prompt_provenance: NOT_VERIFIED`

## 3. `AID-2026-007/evidence.md`

- 必须带与本消息相同形状的 `document_metadata` 前 matter（`role: work-record`，`canonical_scope_id: "ai-development/aid-2026-007-execution-evidence"`，`evidence_reference` 指向本文件，`verification_status: Verified`，`last_verified_date: "2026-11-28"`）。
- 正文记录：分支三提交与 `base_commit_sha`；六个改动文件与各自作用；四条本地门禁的**逐字输出行与退出码**；基线 74 条的含义与「只能收缩」规则；bootstrap 的 Git 校验条件（非 shallow、REF 不含基线、基线由 REF 树生成、当前违例必须是 REF 子集）；新增上下文 `Session identity ratchet` 不设为 required 的声明；本 PR 不引用 Issue。
- 明确写出 `executed_prompt_sha256` 与 `executed_prompt_bytes` 由协调方在落盘后按 `prompt-v1.md` 实际字节机械替换（替换前为占位符）。

## 4. `AID-2026-007/session-evidence.md`

- 同样的 `document_metadata` 形状，`canonical_scope_id: "ai-development/aid-2026-007-session-provenance"`。
- 含 YAML 块：`role: IMPLEMENTATION_SESSION`、`implementing_ai_session: 6b09360b-13cc-83ec-abfd-aa0e6362566c`、`session_reference_status: RECORDED`、`executed_prompt_snapshot_file: 14-ai-development/work-items/AID-2026-007/prompt-v1.md`、`executed_prompt_sha256: "__PROMPT_SHA256__"`、`executed_prompt_bytes: __PROMPT_BYTES__`、`executed_prompt_provenance: NOT_VERIFIED`、`session_evidence_ref` 指向本文件。
- 必须有 `## Actual AI input` 段，逐字写入：`SEND 6b09360b-13cc-83ec-abfd-aa0e6362566c -> 200`，并注明会话 id、投递轮次、本次产出的文件清单。
- 必须写明未声称的部分：没有独立第三方对会话身份的核验，`executed_prompt_provenance` 为 `NOT_VERIFIED`。

## 5. `INDEX-ROW`

`14-ai-development/work-items/INDEX.md` 的新增行，**9 列**，格式照抄现有行（`| ... |`），第一列为 `[AID-2026-007](AID-2026-007/manifest.yaml)`，后续依次为：标题、`USER-PRINCIPAL-DELEGATED`、`GATE/CI / R2`、状态摘要、Prompt 列（`[prompt-v1](AID-2026-007/prompt-v1.md)` 与 provenance 说明）、Implementation 列（三提交与改动面摘要）、Review 列（`NOT_ASSIGNED`）、Acceptance 列（`NOT_ASSIGNED`）。整行放在表格末尾。

## 6. `PR-TITLE`

形如 `feat(gov): register the session-identity ratchet as a work item (AID-2026-007)`。

## 7. `PR-BODY`

必须含以下段落，顺序自定但缺一不可：

1. `## Work Item ID` — `AID-2026-007`，附 `manifest.yaml` 路径。
2. `AI-assisted work: YES`
3. `## Session evidence` — 会话 id `6b09360b-13cc-83ec-abfd-aa0e6362566c`、`session_reference_status: RECORDED`、`SEND 6b09360b-13cc-83ec-abfd-aa0e6362566c -> 200`、指向 `AID-2026-007/session-evidence.md`。
4. `## Per-Issue` — 表格；**本 PR 不引用任何 Issue，写 `None.`**；不得出现 `#1145` 或任何其它 Issue 编号。
5. 变更摘要 — 六个改动文件、三个提交、新增四个工作项文档 + INDEX 行。
6. 门禁证据 — 四条本地结果逐字（74 baselined/0 new、Ran 27 tests OK、check_document_management exit 0、136/136 parsed）。
7. 声明段：这是**新增** GitHub 上下文 `Session identity ratchet`，**不设为 required**；required 仍为 16 条。

## 8. 语义自检

在输出最后追加一个 `@@FILE@@ SELF-CHECK` 块（纯文本短列表），逐条确认：

- `implementing_ai_session` 在 `session_evidence` 中只有一个条目、单值字符串、等于给定 UUID。
- `session_reference_status` 为 `RECORDED`。
- `executed_prompt_snapshot_file` 是仓库相对全路径 `14-ai-development/work-items/AID-2026-007/prompt-v1.md`。
- `executed_prompt_bytes` 与 `executed_prompt_sha256` 为占位符（协调方机械替换），替换后分别为整数与 64 位 hex。
- `base_commit_sha` 为 40 位全 SHA 且等于事实包值。
- INDEX 行为 9 列且第一列是指向 `AID-2026-007/manifest.yaml` 的链接。
- PR 正文含 `## Work Item ID`、`AI-assisted work: YES`、`## Session evidence`、`## Per-Issue` 且写 `None.`，全文无 `#1145`。
