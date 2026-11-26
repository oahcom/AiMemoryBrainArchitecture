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
        - "14-ai-development/work-items/AID-2026-172/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Verbatim capture of the dispatched task text; the manifest pins its byte count and SHA-256."
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
# AID-2026-172-PROMPT v1

Attribution: user-authorized operator (delegated by account owner)
Date: 2026-11-26
Work item ID: AID-2026-172 (PROVISIONAL; assigned number range only)

先读 `D:\code\.superpowers\sdd\2026-11-26-chatgpt-session-ops-skill\worker-contract.md`，严格照它作业。

## 任务：AID-2026-172 · 两份"只许缩小"的 77 条基线缺乏一致性检查

### 事实
仓库里存在**两份内容当前逐条相同的 77 条冻结缺口清单**：
- `scripts/bilingual-baseline.txt`
- `scripts/ci/baselines/bilingual-docs.txt`

**没有任何检查器比较它们。** 任意一份被单独重新生成，另一份就会静默漂移，而门禁只读其中一份。

另有一条相关机制：`write_baseline()` 只校验工作树干净，**不校验新集合是否为旧集合子集**；`check_bilingual_docs.py:410` 的 "This baseline may only shrink; entries must never be added." 只是注释字符串，不是断言。所以重新生成能一次性抬高基线而不被拦。

### 要做
1. 在现有检查器体系里加一个**最小**检查（不要发明新框架）：
   - 比较两份基线的条目集合，不一致就 `::error::` 并打印双向差集，exit 非零。
   - 放在哪个脚本里由你判断（例如挂进 `check_repository_hygiene.py` 或独立小脚本 + 接到已有 workflow），但必须**复用现有 CI 接入方式**，不新增 required context。
   - 同时加一条断言：若 `write_baseline()` 的产物不是旧集合的子集，拒绝写入并打印新增条目。即把那句注释变成真断言。
2. 加对应单元测试（照现有 `test_check_*.py` 风格）。
3. evidence 里写清：为什么这是"防止静默漂移"而不是"新增门槛"；以及它不改变任何现有门禁的通过条件。
4. 三份文档 + INDEX 一行，开 PR，等 16 项，原子合并，核 blob。

### 禁止
不改两份基线的**内容**、不重新生成基线、不改 `current_bilingual_gaps()` 的语义。

回报按 worker-contract §7 格式。
