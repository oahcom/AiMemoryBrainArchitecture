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
        - "14-ai-development/work-items/AID-2026-190/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Verbatim snapshot of the two dispatched task files as they were received. It was not authored by the executing session, and no prompt digest is claimed as frozen."
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

<!-- verbatim capture of the dispatched contract as received on 2026-11-27: two files, in the order given. -->

# FIX BRIEF · COMMON（每个单元必读）

## 0. 模型
9router 免费池已 429，本批全部使用 `opencode-go/deepseek-v4.1-flash`。回报 NOTES 首行写：
`MODEL_FALLBACK: 9router 两模型 429，本次 opencode-go/deepseek-v4.1-flash`

## 1. 工作目录
**只在你被分配的 worktree 里干活**，绝不碰 `D:\code\AiMemoryBrainArchitecture`（多 worker 共享克隆）。

```powershell
cd <YOUR_WORKTREE>
git fetch origin main
git merge --no-ff origin/main    # 先并入，避免 PR dirty 时 0 check runs
git status --short
```
`git status` 非空 = 你自己未提交的成果，保留；不确定就报告。

## 2. 凭证
`$env:USERPROFILE\.git-credentials` 里 `gho_` 开头 40 位 token（`https://oahcom:<token>@github.com`），用 `Authorization: Bearer <token>` 调 API。**不打印 token。**

## 3. 取号（必须先查占用）
```powershell
$H=@{ "Authorization"="Bearer $tok"; "User-Agent"="worker"; "Accept"="application/vnd.github+json" }
$open = Invoke-RestMethod -Uri "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls?state=all&per_page=100" -Headers $H
$open | Where-Object { $_.title -match "AID-2026-<NNN>" } | Select-Object number,title,state
```
标题/分支出现过的号不能用。**已合并：170/172/173/188/189**；INDEX 滞后，不可信。若发现已有 PR 在做同一件事，**停手报告，不要重复开 PR**。

## 4. Work item 结构
`14-ai-development/work-items/AID-2026-<NNN>/` 下 `manifest.yaml` + `evidence.md` + `prompt-v1.md` + `session-evidence.md`；`docs/en/` 与 `docs/zh-CN/` 各一份 `evidence.md`；`INDEX.md` 追加一行。

manifest 必填：`work_item_id` `title` `class` `risk` `status: DISPATCHED` `sponsor: USER-PRINCIPAL-DELEGATED` `accountable_owner: USER-PRINCIPAL-DELEGATED` `repository: oahcom/AiMemoryBrainArchitecture` `base_branch: main` `base_commit_sha: <建分支时的 origin/main 全量 SHA>` `prompt_status: NOT_RECORDED` `id_status: PROVISIONAL`

## 5. 元数据（**块式 YAML，内联 `{}` 必红**）
`check_document_management.py:309` 的 `_scalar()` 对 `{` 开头一律 `ParseError`。

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
        - "AID-2026-<NNN>/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "<一句话：记录了什么、不声称什么>"
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
    canonical_status: Canonical
    canonical_scope: "<范围>"
    canonical_scope_id: "ai-development/aid-2026-<NNN>-<slug>"
    canonical_scope_keywords:
      - "k1"
      - "k2"
      - "k3"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-<NNN>/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-<NNN>/evidence.md"
---
```

每份都过自检（本机需 `$env:PYTHONUTF8="1"`）：
```powershell
python -c "import sys;sys.path.insert(0,'scripts');from check_document_management import read_metadata;p=r'<path>';print(read_metadata(open(p,encoding='utf-8').read()) is not None)"
```
必须打印 `True`。

## 6. PR 正文（缺了 `Session Evidence` 必红）
```markdown
Related issue(s): #1212

AI-assisted work: YES

Session evidence reference(s): 14-ai-development/work-items/AID-2026-<NNN>/session-evidence.md
```
**必须是能在 head 树解析的完整路径**，短形式 `AID-2026-<NNN>/evidence.md` 会被判"路径不存在"。
`session-evidence.md` 必须含三节：`Session role / use case`、`Actual AI input`、`AI-visible output`。

## 7. 合并纪律
- 轮询 `GET /repos/oahcom/AiMemoryBrainArchitecture/commits/<head_sha>/check-runs?per_page=100`，**16 个 required context 全部 completed/success 且无 pending**。
- `strict: true` + `enforce_admins: true`：behind 必须 0；**刷新到合并 1–2 分钟内**完成，中间不插其它 API 调用。
- `merge_method: "merge"`（不 squash、不 rebase、不 force push）。
- 合并后 `git fetch origin main`，逐文件比对 `git rev-parse origin/main:<path>` 与分支 blob，必须一致。

## 8. 硬禁止
不改分支保护、不关 Issue、不删 required context、不改与本单元无关的文件、不伪造任何 SHA/测试输出/门禁结果。
门禁红且原因不在你的改动范围 → **停下报告失败 check 名与日志原文**，不要绕过。

## 9. 回报格式
```
MODEL_FALLBACK: ...
WORK_ITEM / BRANCH / PR / BASE_SHA / HEAD_SHA / CHECKS(16/16) / MERGE / BLOB_VERIFY / FILES / NOTES
```
NOTES 里必须写：改前改后实测数字、以及你**没做**什么（禁止项）。

<!-- ---- second file ---- -->

# UNIT refs · 治理登记里的假绿与死引用

仓库：`D:\code\AiMemoryBrainArchitecture`。worktree：`D:\code\wt-refs`，分支 `fix/2026-11-27-refs-fake-evidence`。

## 缺陷
1. `GOV-REV-2026-11-21-PR425-001.md:88-99` 粘贴的 **10 个 `ok` 用例在任何代码里都不存在**，其 `-s 04-memory-compiler/reference-model` 目录也不存在 → 治理登记里的假绿。
2. `AID-2026-113/restore-evidence.md`（+EN/ZH，共 39 处）标 `Verified`，但 **13 个 New blob SHA 全不可解析**且 != main 实际 blob（例 `activation-policy-engine.md` 实际 `ce15bec1`，表里 `028bc3b6`）。

## 要做
1. 对 PR425-001 的 10 个用例：**不改历史登记**，在其后追加一节 `## Correction (2026-11-27)`，逐条列出"该用例名在 head 树不存在"、给出你实际执行过的 `git grep` 证据，并把该节的结论标为 `NOT_VERIFIABLE_FROM_REPOSITORY`。
2. 对 AID-113：同样**不改原表**，追加 `## Correction`，逐条给出 13 个路径在 `origin/main` 的**真实 blob**（`git rev-parse origin/main:<path>`），并说明原表 13 个 SHA 全部不可解析（给 `git cat-file -t` 的失败输出）。
3. 在三份（canonical + en + zh）都追加，结构一致。
4. 不改 `verification_status` 字段（那是原作者的声明），但追加的 Correction 必须明写"该声明不成立"。

## 禁止
不改任何历史表格、不改任何 blob、不删内容、不重新声明为 Verified。
