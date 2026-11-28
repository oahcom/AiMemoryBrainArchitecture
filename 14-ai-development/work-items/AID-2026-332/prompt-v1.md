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
        - "14-ai-development/work-items/AID-2026-332/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "Prompt snapshot integrity pins are measured from the committed file."
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
    canonical_scope: "Executed user instruction snapshot for AID-2026-332: split the GOV-DOC-001 owner-namespace and governance-operation checker workflow steps."
    canonical_scope_id: "ai-development/aid-2026-332-gov-doc-001-step-split-prompt"
    canonical_scope_keywords:
      - "AID-2026-332"
      - "GOV-DOC-001"
      - "workflow step split"
      - "prompt traceability"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# 新工作项 AID-2026-332：#1237 AC3 —— 拆分 GOV-DOC-001 的两个 checker step

## 已定事实
- ID：`AID-2026-332`（已确认 main 与所有远端 ref 上未被占用）。
- 分支：`fix/2026-11-28-govdoc001-split-checkers`，基于 `origin/main`。
- 唯一代码改动：`.github/workflows/bilingual-docs.yml` 中把合并 step 拆成两个独立命名 step（你上一轮已给出 YAML 片段）。
- 基线 main SHA：`4a6cdd0e7c5dc0db53be37a2f945e02c59d5abf9`（若我 push 前 main 又前进，我会用 merge 而不是 rebase，pins 不受影响）。
- 本机：Windows PowerShell，禁 WSL；Python 3.12；无法本地跑 workflow。

## 门禁硬约束（实测，必须满足）
1. **GOV-DOC-002**：新增 markdown 必须有 `document_metadata` front matter，`role`、`steward` 等键齐全（`AID-2026-329` 的四份文件已通过，可作为结构参照：`role: work-record`、`steward: "user-authorized operator (delegated by account owner)"`）。
2. **Session Evidence**：`session-evidence.md` 必须有精确标题 `Session role / use case`（或以 `Session role` 开头）、`Actual AI input`、`AI-visible output`，段落非空且不是 Summary；manifest 的 `executed_prompt_provenance` ∈ {VERIFIED, NOT_VERIFIED, NOT_AVAILABLE}，`session_reference_status` ∈ {RECORDED, NOT_AVAILABLE, NOT_RECORDED}。
3. **Prompt-to-commit trace**：manifest 需 `prompt_sha256` / `prompt_file` / `prompt_file_blob_sha` / `prompt_file_commit_sha` + `implementation.implementation_commit_sha`；缺失只会让该工作项落在 NO_TRACE（不阻塞必需检查），但你要给全字段。
4. **Work item manifest schema v2**：`documentation[].relationship` 只能是 `code|design|evidence|implementation|normative|reference|schema`；`status`、`id_status`、`risk`、`class`、`sponsor`、`accountable_owner`、`acceptance_authority`、`attribution`、`date`、`repository`、`base_branch`、`base_commit_sha` 必填。
5. **Repository hygiene**：work-item 目录必须在 `14-ai-development/work-items/INDEX.md` 有一行；INDEX 行格式参照现有行（ID 链接 / 标题 / sponsor / class+risk / status / prompt / implementation / review / acceptance 共 9 列）。

## 需要你产出（可直接落盘的完整文件）
A. `14-ai-development/work-items/AID-2026-332/manifest.yaml` 全文。
B. `AID-2026-332/evidence.md` 全文（含 front matter；记录：基线 SHA、要拆的两条命令、拆分前后 CI 可观测性差异、本机不可跑 workflow 的限制、未声称 CI 已通过的边界）。
C. `AID-2026-332/session-evidence.md` 全文（含 front matter 与三个必需标题；输入=用户要求拆 #1237 AC3；输出=YAML 片段与记录）。
D. `AID-2026-332/prompt-v1.md` 的 front matter 块（正文我会用本轮提示词原文）。
E. `INDEX.md` 需要新增的那一行（9 列，与现有格式一致；不确定的列写 `PENDING`/`NOT_ASSIGNED`，不要编造）。
F. PR body 全文（元数据块 + Summary + Changes + Verification boundary + `- Related issue(s): #1237`），标题给一个。

## 约束
LF、无 BOM、YAML 2 空格；不要编造 CI 结果；不要声称 #1196/#1208 已可关闭。
