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
      last_verification_note: "Verbatim capture of the dispatched task text for AID-2026-190; the manifest pins its byte count and SHA-256."
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
# AID-2026-190-PROMPT v1

Attribution: user-authorized operator (delegated by account owner)
Date: 2026-11-27
Work item ID: AID-2026-190 (PROVISIONAL; assigned number range only)

The dispatched task text, as received by the executing session:

## UNIT locale · 修"解码失败变成内容断言失败"

仓库：`D:\code\AiMemoryBrainArchitecture`。worktree：`D:\code\wt-locale`，分支 `fix/2026-11-27-git-decode-locale`。

### 缺陷（两个独立主体撞到）
`check_document_management.py:1189-1206` 与 `:1290-1296` 用 `subprocess(text=True)` 未指定 encoding。解码失败时 `stdout` 变 `None`，于是 DM-10 断言"该文件在 approved_version 不存在"。实测：9 条 DM-10 错误对应的 9 个文件 `git cat-file -e` 全部存在；仅把解码改成 UTF-8，同一棵树 9 条全变 0 错。
AID-173 worker 也在 `check_bilingual_docs.py` 上撞到：GBK 解码 `git show` 抛 `UnicodeDecodeError` → `stdout=None` → 崩溃。

### 要做
1. 全仓 grep `text=True` / `subprocess.run` / `subprocess.check_output`，**所有读取 git 输出的地方**统一加 `encoding="utf-8", errors="replace"`（或等价）。
2. **解码失败必须 fail-closed 且报"解码失败"**，不得退化成"内容不存在"这类确定性断言。给出实现：`None`/空输出时打印明确错误并 exit 2。
3. 补测试：构造非 UTF-8 字节输出 → 断言错误信息含 `decode`，不含"不存在"。
4. 跑 `check_document_management.py` 与 `check_bilingual_docs.py`，确认本机（GBK 控制台）不设 `PYTHONUTF8` 也能通过；记录前后退出码。

### 禁止
不改任何门禁的通过条件（只改错误分类与编码）。

回报按 worker-contract §7 格式。
