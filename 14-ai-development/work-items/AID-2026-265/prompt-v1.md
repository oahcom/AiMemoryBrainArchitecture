---
document_metadata:
  domain: ai-development
  role: reference
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
        - "14-ai-development/work-items/AID-2026-265/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured task capture; it is not a byte-for-byte platform transcript."
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
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords:
      - "prompt-snapshot"
      - "index-table-integrity"
      - "document-management"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-265 Prompt Snapshot

Source: the dispatched repair task in the coordination conversation that carried
FIX-1418 (second pass on PR #1418).
Capture status: structured task snapshot, not a raw platform transcript.
Date: 2026-11-27.

You are a subagent spawned by another session.

你是修复子 Agent FIX-1418。任务：让 PR #1418 达到可合并状态。工作目录
D:\code\AiMemoryBrainArchitecture（Windows PowerShell，用 `;` 分隔）。API 配额可用。

## 事实

- `#1418`（`fix/2026-11-27-index-split-repair`，AID-2026-265）head `6c511ad2`，5 files，
  **`mergeable_state=dirty`，0 个 check run**（即 `refs/pull/1418/merge` 生成失败或
  workflow 未触发）。
- 内容：修复 `INDEX.md` 第 304/305 行（`AID-2026-190` 拆行、`erification_status` 截断）
  + 新增 `AID-2026-265` 工作项与 INDEX 行。
- `origin/main` 已多次前进（实测为准，最近为 `5670357d` 之后）。
- **重要**：合并进 main 的 #1423 报告指出，line 309（`AID-2026-190`）在 main /
  merge-base / merge commit 五处 sha256 前缀完全一致（`405e69727dc92887`），即该缺陷
  **仍在 main 上**、未被别人修掉。

## 执行

1. `git fetch origin`；确认 main 当前 SHA；读
   `git show origin/main:14-ai-development/work-items/INDEX.md` 中该行现状（是否仍拆行/截断）。
2. `git worktree add -f D:\code\_aimb\wt-1418 -B fix/2026-11-27-index-split-repair-2 origin/main`，
   把 #1418 的**有效改动**搬过来（优先 `git cherry-pick 6c511ad2`；冲突则手工按「单行、
   表头 9 列、`verification_status` 完整、无控制字符、以 `|` 收尾」重做）。
3. 机器校验（全部必做）：`Select-String -Path INDEX.md -Pattern "[\x00-\x08\x0B\x0C\x0E-\x1F]"`
   零命中；`^erification` 零命中；`^\|` 行数守恒；表头列数 = 每行单元格数（对新增/修复行
   逐行核对）；同一 AID 仅一行；`python scripts/check_traceability.py --index-only`；
   `python scripts/ci/check_repository_hygiene.py --base <40位SHA> --head <40位SHA>`（必须 40 位）。
4. push（不 force）。**然后诊断 0 check run 的原因**：`GET /repos/.../commits/<head>/check-runs`、
   `GET /repos/.../commits/<head>/status`、`GET /repos/.../actions/runs?head_sha=<head>`；若确实
   无 run，检查该分支是否曾以某种方式绕过 PR 事件（如直接 push 到分支后未触发 `synchronize`），
   给出可执行的补救（例如推一个空提交触发 `synchronize`，或关-开 PR），并执行最小补救。
5. 轮询新 head 的 check-runs（60s × 30），记录最终结论。
6. 交付 `D:\code\_aimb\round\FIX1418.md`：main 上缺陷现状、迁移方式、校验输出、
   0-check-run 诊断与补救、新 head、最终 check 结论、未达标项。

硬约束：不 force、不合并、不改其他 PR、不动主工作树。若 265 已被占用，停止并报告。

Acceptance for this work item: the repaired row carries ten pipe separators, the
word `verification_status` is complete, the file contains no control characters,
the count of `^|` lines grows by exactly the number of rows added, and the row
pair is gone from `main` after merge.
