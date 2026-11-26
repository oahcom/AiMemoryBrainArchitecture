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
        - "14-ai-development/work-items/AID-2026-191/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Scope snapshot, not a verbatim raw capture: records the two dispatched brief files that selected this unit's scope, its threshold and its prohibitions; the session identifier and the model input stream were not captured."
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
      - "bilingual"
      - "side-by-side"
      - "cjk-predicate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Prompt snapshot — AID-2026-191

**Scope snapshot, not a verbatim raw capture.** The dispatching session supplied two files plus a
subagent message. The unit brief is reproduced whole; the subagent message is reproduced whole; the
common brief is summarised because it is shared by every unit in the batch and its operative clauses
are quoted where they bind this unit.

## Task brief as received (verbatim, `unit-cjk.md`)

```
# UNIT cjk · "1 个汉字 = 已翻译"的判定

仓库：`D:\code\AiMemoryBrainArchitecture`。worktree：`D:\code\wt-cjk`，分支 `fix/2026-11-27-side-by-side-cjk`。

## 缺陷
`check_bilingual_docs.py:312-331`：`_has_any_chinese(source) or _has_any_chinese(partner)` —— **OR 包含源文件**。英文源里出现 2 个汉字、`.zh-CN.md` 是纯英文复制件，配对仍成立。测试 `test_issue_469` 固化了该行为。

## 要做（**先测量，再决定是否改判定**）
1. 先测量：把判定改成"**partner 必须含中文**"（去掉 source 的 OR），跑 `current_bilingual_gaps()`，记录 `77 → ?`，逐条列出新增缺口。
2. 若新增缺口 **≤ 3**：实施改动 + 更新基线（说明新增原因）+ 改 `test_issue_469` 为新语义（测试名改为描述新规则）。
3. 若新增缺口 **> 3**：**不改判定**，只产出一份报告：哪些文件是靠"源文件里有汉字"蒙过的、逐条列 `cjk/latin/ratio`，并在 evidence 标 `DEFERRED_TO_OWNER`（说明代价）。
4. 两种情况都要跑 `python -m unittest discover -s scripts -p "test_check_bilingual*"` 记录结果。

## 禁止
不删任何镜像、不新写译文、不改 `_carries_chinese()` 的 100 字阈值。
```

## Dispatching message as received (verbatim)

```
你是子代理。读这两个文件并端到端执行，不要提问：
1. `D:\code\.superpowers\sdd\2026-11-26-chatgpt-session-ops-skill\fix-brief-common.md`
2. `D:\code\.superpowers\sdd\2026-11-26-chatgpt-session-ops-skill\unit-cjk.md`

你的 worktree：`D:\code\wt-cjk`（分支 `fix/2026-11-27-side-by-side-cjk`）。**只在它里面干活**。

注意：这是**先测量、后决定**的单元。缺口 ≤3 才实施改动；>3 只出报告并标 `DEFERRED_TO_OWNER`。无论哪种都要给实测数字。
```

## Common brief (`fix-brief-common.md`) — operative clauses

- Model: both `9router` models returned 429, so the batch runs on `opencode-go/deepseek-v4.1-flash`;
  the NOTES file must open with that substitution.
- Work only inside the assigned worktree; merge `origin/main` before pushing so the PR is not dirty.
- Credentials: the `gho_` token from `%USERPROFILE%\.git-credentials`, used as a bearer token; never
  printed.
- Work-item structure: `14-ai-development/work-items/AID-2026-<NNN>/` with `manifest.yaml`,
  `evidence.md`, `prompt-v1.md`, `session-evidence.md`; one `evidence.md` under `docs/en/` and one
  under `docs/zh-CN/`; one row appended to `INDEX.md`.
- Manifest fields: `status: DISPATCHED`, `sponsor`/`accountable_owner: USER-PRINCIPAL-DELEGATED`,
  `repository`, `base_branch: main`, `base_commit_sha` (full SHA at branch creation),
  `prompt_status`, `id_status: PROVISIONAL`.
- Metadata must be block-style YAML; a leading `{` is a parse error in
  `check_document_management.py:309`.
- Numbers already merged: 170/172/173/188/189; the INDEX lags and is not authoritative. If an
  existing PR is doing the same job, stop and report instead of opening a second one.
- Merge discipline: sixteen required contexts completed/success on the exact head with no pending,
  behind zero, `merge_method: "merge"`, local and remote blobs compared after merge.
- Hard prohibitions: no branch-protection change, no Issue close, no required-context deletion, no
  unrelated file, no fabricated SHA, test output or gate result.

## What the brief did not say, and how it was resolved

The instruction "the partner must contain Chinese" is direction-blind, because
`side_by_side_partner()` is symmetric. Applied literally it flags twelve pairs whose Chinese
document is the named member and whose partner is the English file. The cost of the *intended*
rule — only the file designated to hold the Chinese text may certify the pair — is zero new gaps,
which is inside the ≤ 3 threshold. The measurement, the twelve false positives with their
`cjk`/`latin`/`ratio`, and the zero-cost rule are in `AID-2026-191/evidence.md` §2–§3.
