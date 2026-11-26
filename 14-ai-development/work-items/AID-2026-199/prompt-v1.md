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
        - "14-ai-development/work-items/AID-2026-199/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "逐字收录收到的两个派发任务文件。它并非由执行会话撰写，也不声称任何 prompt 摘要被冻结。"
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
# UNIT gates-b · 空集合即通过 + 注释吃掉 workflow

worktree：`D:\code\wt-gates-b`，分支 `fix/2026-11-27-gates-b`。

## 缺陷
1. `check_repository_hygiene.py:496-505` `check_index_membership`：无目录 / 无 INDEX 都返回 `[]`（空集合即通过）；而同仓库其它检查对"0 输入"是 exit 2，口径相反。
2. `check_declared_check_contexts.py` / `check_test_reachability.py`：`jobs:  # comment` 让该 workflow 的 context 集合变空；两处都只 glob `*.yml`（漏 `.yaml`）；`check_test_reachability` 的 Rule B 把 workflow 里**注释中提到**的测试名算作"被执行"（同文件 gate 分支反而剥注释）。

## 要做
1. `check_index_membership`：目录或 INDEX 缺失时 fail-closed（exit 2 + 明确信息），不返回 `[]`。
2. 两处 glob 改 `*.yml` + `*.yaml`；YAML 解析前剥注释（复用现有 helper，若没有就加一个最小实现）。
3. 补测试：`jobs: # comment` 夹具 → 不得判通过；`.yaml` 文件会被读到；注释里的测试名不计入 Reachable。
4. 跑 `check_repository_hygiene.py` 与 `check_declared_check_contexts.py`，记录前后输出（应为 16 declared / 16 produced 不变）。

## 禁止
不新增 required context、不改 job 名、不放宽任何判定。
