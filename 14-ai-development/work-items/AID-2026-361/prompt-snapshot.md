---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
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
        - "14-ai-development/work-items/AID-2026-361/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records task excerpts only; it is not a byte-for-byte export of the complete chat input."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope: "Recorded task excerpt for AID-2026-361 manifest blob-pin ledger squash-merge verification"
    canonical_scope_id: "ai-development/aid-2026-361-prompt-snapshot"
    canonical_scope_keywords:
      - "prompt"
      - "manifest"
      - "blob-pin"
      - "ledger"
      - "squash-merge"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# Executed prompt snapshot — AID-2026-361

This document records excerpts of the implementation task input. It is not a byte-for-byte export of the complete chat input; provenance is therefore recorded as NOT_VERIFIED.

> 你是实现会话。修复 `oahcom/AiMemoryBrainArchitecture` 中 manifest blob-pin ledger 在 squash merge 后错误报告 `repin_commit` 非 target ancestor 的问题。

> `repin_commit` 必须继续指向原始 repin commit。不能把 ledger 中的原始证据 SHA 改写成 squash SHA。

> 原始 repin commit 必须独立验证：能够解析；first-parent pin 等于 `previous_pin`；repin tree pin 等于 `new_pin`。

> 如果原始 repin commit 不是 target ancestor，只能接受 target first-parent history 中唯一的等价 squash transition。该 transition 的 first-parent pin 必须等于 `previous_pin`，tree pin 必须等于 `new_pin`，并且 squash tree 中 manifest 的 Git blob SHA 必须与原始 repin commit tree 中的 manifest Git blob SHA 完全相同。

> 将解析出的实际转换位置用于 `verify_unledgered_history`。不得放宽 forged `new_pin` 负例；伪造值必须因与原始 repin commit tree 中的真实值不一致而被拒绝。

> 只修改 `scripts/ci/check_manifest_blob_pins.py` 和 `tests/test_manifest_pin_ledger.py`。不改 CLI，不改 workflow，不改 baseline，不改无关文件。

> 保留原有 checker 和 negative-gate 语义，并为 squash 等价通过、manifest blob 不一致拒绝、伪造 `new_pin` 拒绝增加回归测试。

The implementation session identifier recorded for this work is:

`6b0a1b3c-4eb8-83ec-b8db-3edd54c94988`
