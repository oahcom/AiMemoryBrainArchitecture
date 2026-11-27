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
        - "14-ai-development/work-items/AID-2026-291/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Session Evidence structure is aligned to the repository validator; exact-head validation is pending."
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
    canonical_scope: "Implementation-session identity, actual input/output provenance, and validation record for AID-2026-291."
    canonical_scope_id: "ai-development/aid-2026-291-session-evidence"
    canonical_scope_keywords:
      - "AID-2026-291"
      - "prompt-to-commit trace"
      - "AC6 evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session Evidence — AID-2026-291

## Session role / use case

Implementation and validation session for Issue #265 AC6. The work adds a read-only prompt-to-implementation trace checker, deterministic regression assertions, an Actions-generated baseline and a ratchet gate. Repository changes are applied through the GitHub API connector; no local git or local Actions execution is claimed.

## Actual AI input

The user issued the following binding R5 instructions:

> # 裁决 R5 · 编号改为 AID-2026-291，立即执行，不要再问
>
> main（`5670357d`）上 290 已被 `#1268` 占用，我核过 290–299 只有 290 被占。**本任务改用 `AID-2026-291`。**
>
> - 把 `14-ai-development/work-items/AID-2026-290/` 整体改名为 `AID-2026-291/`，manifest 里 `work_item_id` 同步改。
> - 分支不用重建，PR #1427 不用关，直接把改动推上去即可（同一个 head 更新）。
> - 如果 `INDEX.md` 里已写 290 的行，改成 291；不要动 290 那一行（那是别人的）。
> - 再核一次：`git ls-tree -d --name-only origin/main 14-ai-development/work-items/ | grep AID-2026-29` 里 291 必须仍为空；若已被占，顺延 292 并回报。
>
> ## 其余按 R4 执行
> - 047 = `DIGEST_UNPINNED` / `HEAD_MATCH` + `REACHABLE`；`TRACEABLE` 期望 0；不加特例。
> - 追平 `origin/main`（`5670357d`）再推；`Schema non-empty audit` 会随 workflow 修复变绿，不要改那个 job。
> - baseline 用 Actions 快照 → 作为 `AID-2026-291/` 下的证据文件提交 → 门禁读它；baseline 里必须有 `commit` pin（写明测在哪个 main SHA）。
> - Session Evidence 按模板逐字对齐。
>
> ## 交付
> - 五状态计数和 3×4 矩阵必须来自 Actions 实跑输出。
> - 给出 11 份断言 manifest 的判定、baseline 内容、run URL、16/16 required check-runs 名字集合、merge SHA、逐文件 blob 核对，以及 #265 评论链接。
> - Issue #265 评论的 AC 勾选框保持未勾，并明确写「机制已可判；存量 TRACEABLE=0」。

Earlier R3/R4 rulings remain binding: nested `implementation.implementation_commit_sha` and legacy top-level field are both supported; prefer `implementation.merge_commit_sha` for ancestry, otherwise use the comparison base; either immutable prompt blob pin or prompt commit/path pin is sufficient, and both are checked when both exist; primary precedence is `NO_TRACE`, `DIGEST_UNPINNED`, `DIGEST_MISMATCH`, `COMMIT_UNREACHABLE`, `TRACEABLE`. AID-2026-047 is unpinned and must not receive an exception or a fabricated pin.

## AI-visible output

The synchronized PR tree is based on the current main commit `056209b71c2e559efa3526a31870187a8e6e47f2` and retains the previous branch head `417c2e4b573eaee51ee9383f9498ccfc25c53c6b` as a second parent. The main-tree occupancy check found AID-2026-291 vacant and AID-2026-290 occupied by the unrelated Issue #1268 item. The task records and index row are placed only under AID-2026-291; the existing AID-2026-290 files are inherited unchanged from main.

The checker regression suite previously passed on PR #1427. Final Actions evidence, generated baseline bytes, required check-run set, merge SHA and post-merge blob verification are to be appended after those operations actually complete.
