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
        - "14-ai-development/work-items/AID-2026-173/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Records the dispatched task scope, not a full raw transcript; the session identifier and the verbatim model input stream were not captured."
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

# Prompt snapshot — AID-2026-173

**Scope snapshot, not a verbatim raw capture.** This file records the task as it was
dispatched to the implementing session. The dispatching session supplied a worker
contract and a task brief; the brief is reproduced below because it is the whole of
the instruction that selected the scope, the number band and the prohibition.

## Task brief as received (verbatim)

```
先读 worker-contract.md，严格照它作业（号段/Work Item/开 PR/等 16 项/原子合并/blob 核验）。

## 任务：AID-2026-173 · 隐形门槛清单（只记录，不改门禁）

### 事实
仓库里有多处"写死的数字"会在改文档时突然触发，但不显眼。已确认的例子：
- 某检查要求文件含 ≥100 个 CJK 字符
- 31 个 prompt 文件，每个 ≥250 字
- document-scope-registry.yaml 里 documents: 27 是精确等值
- 16 条 required check context 的名单固定
- 某 compare 有 300 文件上限
- 2026-12-01 生效的 session-evidence 时间闸

### 要做
1. 在 scripts/*.py、.github/workflows/*.yml、00-governance/*.yaml 里系统搜索硬编码阈值：
   >= \d+、<= \d+、MAX_、LIMIT、THRESHOLD、len(...) >、len(...) <、精确等值比较。
2. 产出一张表：阈值 / 定义位置（文件:行）/ 触发方式（改什么会碰到它）/ 违反时原文案。
3. 每条标注它属于：BLOCKING（红门禁）/ ADVISORY（只提示）/ SILENT（悄悄算错不报错）。
4. 特别查：有没有"改了文档才触发"的，例如"某目录必须有 README"、"某文件必须列在 registry"、
   "某类文件必须配对"。
5. 三份文档 + INDEX 一行，开 PR，等 16 项，原子合并，核 blob。

### 禁止
不改任何检查器的判定逻辑与阈值。本任务只记录。
```

## What this snapshot does not contain

- The model's own hidden reasoning or the raw message stream.
- Any tool transcript: the search commands, the gate runs and their full output are
  summarised in `evidence.md` section 2 and section 6, which state the method and the
  reproduction commands rather than replaying every line.
- A platform session identifier: none was exposed to the session, so the manifest
  records `implementing_ai_session: NOT_RECORDED` and `session_reference_status:
  NOT_RECORDED` rather than inventing one.
