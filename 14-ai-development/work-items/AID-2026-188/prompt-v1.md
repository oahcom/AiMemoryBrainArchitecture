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
        - "14-ai-development/work-items/AID-2026-188/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
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

# AID-2026-188 — dispatched prompt snapshot (v1)

Snapshot of the worker contract received by the executing session on 2026-11-26. The dispatch names the target work item as `AID-2026-<NNN>`; the number was allocated by the executing session under the rule recorded in `manifest.yaml` (`identifier_allocation`). Nothing below was rewritten; the premise statements are reproduced as dispatched so that the divergence recorded in `evidence.md` section 2 is checkable against the order that produced it.

---

You are a subagent spawned by another session.

你是修复 worker。⚠️ 本单元前两次派发均因 `9router` 免费上游 429 失败，现降级到 opencode-go 上游。请在回报 NOTES 首行写：`MODEL_FALLBACK: 9router/deepseek-v4.1-flash + 9router/9router_hermes 均 429，本次使用 opencode-go/deepseek-v4.1-flash`。

## 工作目录（固定，不要新建 worktree，不要碰其它目录）
`D:\code\wt-norm03`，分支 `docs/2026-11-26-normative-root-03`。

```powershell
cd D:\code\wt-norm03
git fetch origin main
git status --short
```
若非空：报告内容再决定，**不要删除别人的文件**。

## 事实（已实测）
- `scripts/check_bilingual_docs.py` 的 `NORMATIVE_ROOTS` 现 13 项，不含 `03-memory-brain`。
- main 上 `03-memory-brain/` 已有 3 份 canonical（`canonical-memory-store.md`、`commit-cursor-semantics.md`、`forget-fence-operation-and-publication-gate.md`），`docs/en|zh-CN/03-memory-brain/` 各有 13 个镜像，这 3 份镜像都存在。
- 进程内 monkeypatch 实测：加入 `03-memory-brain` 后 `current_bilingual_gaps()` **77 → 77，new=0, gone=0**。

## 要做
1. `NORMATIVE_ROOTS` 加 `"03-memory-brain"`（照现有格式与排序）。
2. 检查是否有第二处根清单（`check_bilingual_docs_full.py` 等）；有则同步，没有就在 evidence 写"仅一处定义"。
3. **不改两份 baseline 内容、不重新生成**。改完跑：
```powershell
$env:PYTHONUTF8="1"
python scripts/check_bilingual_docs.py
```
确认退出码 0、仍是 77 条。（本机 GBK 会让 `git show` 解码崩，`PYTHONUTF8=1` 是必需，属已知 locale 工件。）
4. 跑 `python -m unittest discover -s tests -p "test_check_bilingual*"`。注意 AID-172 刚给该脚本加了 15 个用例（含 `check_baseline_copies_agree()` 与写入拒绝），你的改动不能让它红。
5. `00-governance/document-scope-registry.yaml` 把这 3 份登记为受治理文档（照既有格式；`documents:` 若为精确等值需 +3）。
6. 新建 `14-ai-development/work-items/AID-2026-<NNN>/` 三份 + `INDEX.md` 一行。
   - 取号：`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=all&per_page=100`，标题/分支出现过的号不能用。**已合并 170/172/173，175–182 可能被占**。
   - manifest 必填：`work_item_id` `title` `class` `risk` `status: DISPATCHED` `sponsor: USER-PRINCIPAL-DELEGATED` `accountable_owner: USER-PRINCIPAL-DELEGATED` `repository` `base_branch: main` `base_commit_sha` `prompt_status: NOT_RECORDED` `id_status: PROVISIONAL`
7. 元数据**块式 YAML**（`check_document_management.py:309` 对 `{` 开头一律 ParseError）：
```yaml
      approval_scope:
        type: Full-document
      evidence_reference:
        - "AID-2026-<NNN>/evidence.md"
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
    canonical_scope_keywords:
      - "bilingual"
      - "normative-root"
      - "memory-brain"
```
三份都要 `read_metadata()` 返回 `True`。

## PR 与合并
- 凭证：`$env:USERPROFILE\.git-credentials` 里 `gho_` 40 位 token，`Authorization: Bearer`。不打印 token。
- PR 正文必须含 `Related issue(s): #1212`、`AI-assisted work: YES`、`Session evidence reference(s): AID-2026-<NNN>/evidence.md`。
- 初始 `mergeable_state=dirty` 时 GitHub 不产生任何 pull_request 运行（0 check runs）——先 `git merge --no-ff origin/main` 再推，别干等。
- 16 项全绿才合并；behind 必须 0；刷新到合并 1–2 分钟内；`merge` 方式；合并后核 blob。

## 禁止
不改 baseline 内容、不改 checker 判定语义（只加一个根条目）、不恢复其余 10 份 canonical、不删镜像、不关 Issue、不 force push。

## 回报
```
WORK_ITEM / BRANCH / PR / BASE_SHA / HEAD_SHA / CHECKS(16/16) / MERGE / BLOB_VERIFY / FILES / NOTES
```
附：改前改后 `NORMATIVE_ROOTS` 条目数、`check_bilingual_docs.py` 退出码与输出摘要、unittest 通过数、registry 计数变化。
