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
        - "14-ai-development/work-items/AID-2026-256/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured task capture; it is not a byte-for-byte platform transcript."
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
      - "prompt-snapshot"
      - "registration-reconciliation"
      - "work-item-status"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-256 — executed prompt snapshot

This file records, verbatim, the instruction this work item executes. It is not a design document.

## Origin

Owner ruling, 2026-11-27 (prompt 49 → reply `reply-6b07c97e-114742.md`; prompt 50 → reply `reply-6b07c97e-115902.md`).

## Executed instruction (verbatim, condensed to the operative sentences)

> **修复第 1、2 类；第 3 类只处理与已合并 PR 能一一对应的记录，不做全量状态推断。**
> 具体边界：仅将有 GitHub 合并事实支撑的 19 个 AID（含 112）登记为 `MERGED`；不批量改写其余 manifest，不为缺少顶层 `status` 的 13 个 manifest 新增字段。
> **通用规则：** 对应 PR 已合并且 AID 映射明确时，将 INDEX 状态单元整体替换为 `MERGED`；该 AID manifest 已有顶层 `status` 时，将整个 `status` 字段替换为 `status: MERGED`。其他字段不动。
> 开新 PR，不只改本地。Work Item ID：`AID-2026-256`；分支：`work-item/aid-2026-256-governance-registration-reconciliation`；PR：Draft，**是**。
> `NOT_RECORDED` 是如实占位，不是有效证据引用。取得并提交真实 session evidence reference 前，不得把 PR 标为 ready，也不得宣称门禁通过。

Follow-up ruling on cell shape (prompt 50):

> **B**。成立：保留分隔符 `—` 与后续备注，即 `DRAFT PR — X` → `MERGED — X`。

## Operational constraints carried into execution

- Status cell prefix only; trailing provenance note preserved.
- Stale carrier phrases inside those cells (`PR PENDING`, `PR #NNN open`) replaced with the real merge PR number.
- No manifest status field invented where none existed.
- PR stays draft; `Session evidence reference(s): NOT_RECORDED`.
