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
        - "14-ai-development/work-items/AID-2026-291/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Snapshot bytes are pinned in the adjacent manifest; provenance is recorded as NOT_VERIFIED."
    usage_status: Active
    modification_status: Active-Modified
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
# 裁决 R5 · 编号改为 AID-2026-291，立即执行，不要再问

## 1. 编号

main（`5670357d`）上 290 已被 `#1268` 占用，我核过 290–299 只有 290 被占。**本任务改用 `AID-2026-291`。**

- 把 `14-ai-development/work-items/AID-2026-290/` 整体改名为 `AID-2026-291/`，manifest 里 `work_item_id` 同步改。
- 分支不用重建，PR #1427 不用关，直接把改动推上去即可（同一个 head 更新）。
- 如果 `INDEX.md` 里已写 290 的行，改成 291；不要动 290 那一行（那是别人的）。
- 再核一次：`git ls-tree -d --name-only origin/main 14-ai-development/work-items/ | grep AID-2026-29` 里 291 必须仍为空；若已被占，顺延 292 并回报。

## 2. 其余按 R4 执行

- 047 = `DIGEST_UNPINNED` / `HEAD_MATCH` + `REACHABLE`；`TRACEABLE` 期望 0；不加特例。
- 追平 `origin/main`（`5670357d`）再推；`Schema non-empty audit` 会随 workflow 修复变绿，不要改那个 job。
- baseline 用 Actions 快照 → 作为 `AID-2026-291/` 下的证据文件提交 → 门禁读它；baseline 里必须有 `commit` pin（写明测在哪个 main SHA）。
- Session Evidence 按模板逐字对齐。

## 3. 交付（本轮必须给出，不许再停）

- 5 状态计数 + 3×4 矩阵（Actions 实跑原文）。
- 11 份断言 manifest 的判定。
- baseline 文件路径与内容。
- run URL、16/16（用 check-runs 名字集合核）、merge SHA、逐文件 blob 核对。
- #265 评论链接（`[ ]` 保持未勾，写明「机制已可判；存量 TRACEABLE=0」）。

若中途再遇外部阻断（不是你的代码问题），**先推分支、把阻断的 check 名与日志原文报回来**，不要停在没有 PR 的状态。
