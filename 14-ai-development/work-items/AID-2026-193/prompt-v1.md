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
      last_verification_note: "Verbatim snapshot of the dispatched worker contract as it was received. It was not authored by the executing session and no prompt digest is claimed as frozen."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-193-PROMPT v1 — dispatched contract, as received

This file is a snapshot of the text the executing session was dispatched with, copied
without editing. It is not a transcript: no assistant turn, tool call or intermediate
reasoning is reproduced. Where the dispatch referenced a file on the operator's disk, the
file's content is reproduced under its own heading.

## 1. Dispatch message

```
You are a subagent spawned by another session.
读这两个文件并端到端执行，不要提问：
1. `D:\code\.superpowers\sdd\2026-11-26-chatgpt-session-ops-skill\fix-brief-common.md`
2. `D:\code\.superpowers\sdd\2026-11-26-chatgpt-session-ops-skill\unit-auth02.md`

你的 worktree：`D:\code\wt-auth02`（分支 `fix/2026-11-27-dangling-09-refs`）。**只在它里面干活**。

纪律：**不新建任何被引用文件**，只在引用处加说明并保留原路径文本。
```

## 2. `fix-brief-common.md`, as received

```
# FIX BRIEF · COMMON（每个单元必读）

## 0. 模型
9router 免费池已 429，本批全部使用 `opencode-go/deepseek-v4.1-flash`。回报 NOTES 首行写：
`MODEL_FALLBACK: 9router 两模型 429，本次 opencode-go/deepseek-v4.1-flash`

## 1. 工作目录
**只在你被分配的 worktree 里干活**，绝不碰 `D:\code\AiMemoryBrainArchitecture`（多 worker 共享克隆）。

    cd <YOUR_WORKTREE>
    git fetch origin main
    git merge --no-ff origin/main    # 先并入，避免 PR dirty 时 0 check runs
    git status --short

`git status` 非空 = 你自己未提交的成果，保留；不确定就报告。

## 2. 凭证
`$env:USERPROFILE\.git-credentials` 里 `gho_` 开头 40 位 token，用 `Authorization: Bearer <token>` 调 API。**不打印 token。**

## 3. 取号（必须先查占用）
标题/分支出现过的号不能用。**已合并：170/172/173/188/189**；INDEX 滞后，不可信。
若发现已有 PR 在做同一件事，**停手报告，不要重复开 PR**。

## 4. Work item 结构
`14-ai-development/work-items/AID-2026-<NNN>/` 下 `manifest.yaml` + `evidence.md` + `prompt-v1.md`
+ `session-evidence.md`；`docs/en/` 与 `docs/zh-CN/` 各一份 `evidence.md`；`INDEX.md` 追加一行。

manifest 必填：`work_item_id` `title` `class` `risk` `status: DISPATCHED`
`sponsor: USER-PRINCIPAL-DELEGATED` `accountable_owner: USER-PRINCIPAL-DELEGATED`
`repository: oahcom/AiMemoryBrainArchitecture` `base_branch: main`
`base_commit_sha: <建分支时的 origin/main 全量 SHA>` `prompt_status: NOT_RECORDED`
`id_status: PROVISIONAL`

## 5. 元数据（**块式 YAML，内联 `{}` 必红**）
`check_document_management.py:309` 的 `_scalar()` 对 `{` 开头一律 `ParseError`。

每份都过自检：
    python -c "import sys;sys.path.insert(0,'scripts');from check_document_management import read_metadata;p=r'<path>';print(read_metadata(open(p,encoding='utf-8').read()) is not None)"

必须打印 `True`。

## 6. PR 正文（缺了 `Session Evidence` 必红）
    Related issue(s): #1212

    AI-assisted work: YES

    Session evidence reference(s): 14-ai-development/work-items/AID-2026-<NNN>/session-evidence.md

**必须是能在 head 树解析的完整路径**，短形式会被判"路径不存在"。
`session-evidence.md` 必须含三节：`Session role / use case`、`Actual AI input`、`AI-visible output`。

## 7. 合并纪律
- 轮询 `GET /repos/oahcom/AiMemoryBrainArchitecture/commits/<head_sha>/check-runs?per_page=100`，
  **16 个 required context 全部 completed/success 且无 pending**。
- `strict: true` + `enforce_admins: true`：behind 必须 0；刷新到合并 1–2 分钟内完成。
- `merge_method: "merge"`（不 squash、不 rebase、不 force push）。
- 合并后 `git fetch origin main`，逐文件比对 `git rev-parse origin/main:<path>` 与分支 blob，必须一致。

## 8. 硬禁止
不改分支保护、不关 Issue、不删 required context、不改与本单元无关的文件、不伪造任何 SHA/测试输出/门禁结果。
门禁红且原因不在你的改动范围 → **停下报告失败 check 名与日志原文**，不要绕过。

## 9. 回报格式
    MODEL_FALLBACK: ...
    WORK_ITEM / BRANCH / PR / BASE_SHA / HEAD_SHA / CHECKS(16/16) / MERGE / BLOB_VERIFY / FILES / NOTES

NOTES 里必须写：改前改后实测数字、以及你**没做**什么（禁止项）。
```

## 3. `unit-auth02.md`, as received

```
# UNIT auth02 · 85 个指向不存在的 09 文档

worktree：`D:\code\wt-auth02`，分支 `fix/2026-11-27-dangling-09-refs`。

## 缺陷（我实测）
`git grep -oh "09-security-governance/[A-Za-z0-9._-]*\.md" origin/main -- "*.md"` 去重 91 条，
与 `git ls-tree` 求差 → **85 个不存在**。

## 要做
1. 产出完整清单（路径 + 引用它的文件:行），写进 evidence。
2. 对每处引用做**最小**处置，二选一并在 evidence 逐条记录选了哪个：
   - 若该引用位于"maintained in / see also"位置：改为文字说明
     `(not restored on main; see AID-2026-107 §10)` **并保留原路径文本**（便于将来恢复时检索）；
   - 若该引用被写成可点击链接：降为纯文本 + 同一说明。
3. **不要**新建任何被引用文件、不要改任何规范正文。
4. 改完跑 `check_bilingual_docs.py` 与 `check_document_management.py`，确认不变红。

## 禁止
不新建文档、不删引用、不改 09 下任何文件的内容。
```

## 4. What the executing session measured against this contract

- The 85th path in the defect statement resolves only under the root-directory reading; the
  measured set at the base commit is 84 absent paths plus 7 present ones (evidence section
  2). The contract's own command reproduces 91 distinct strings, so the arithmetic, not the
  command, is what differs.
- The contract asks for two handling branches. Only the first has instances: no citation of
  the 84 absent paths is a clickable link.
- The contract's two gates were run and are green for this change; the second one
  (`check_document_management.py`) exits 2 on the repository's standing `INCOMPLETE`
  verdict, which is unchanged before and after.
