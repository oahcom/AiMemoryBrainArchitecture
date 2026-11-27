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
        - "14-ai-development/work-items/AID-2026-140/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Execution prompt snapshot for AID-2026-140; not an approved architecture specification."
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
      - "aid-2026-140"
      - "memory-runtime"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---
# AID-2026-140 — Execution prompt snapshot

Use the account-fixed identifier range **AID-2026-140 through AID-2026-149**. This task uses AID-2026-140 if unoccupied; otherwise use the next free number within this range. Do not read INDEX max+1 and do not use a number outside this range.

Restore exactly these five F Canonical files from source branch `session-f-memory-runtime`:
- `activation-policy-engine.md`
- `retrieval-engine.md`
- `runtime-overview.md`
- `runtime-scheduling.md`
- `working-set-and-cache.md`

The existing EN and ZH-CN mirrors require no translation. Add GOV-DOC-002 metadata only to the five Canonical-backed mirror pairs; preserve all mirror bodies byte-for-byte. The `memory-runtime-guide.md` pair remains `ORPHAN_MIRROR_PENDING_DECISION` and is untouched. The source branch's ten historical records are not restored; the live tree count is nine `phase-*` files plus `module-baseline-and-redlines.md`, all ten recorded as `HISTORICAL_PHASE_RECORD`.

The F source root is `05-memory-runtime/runtime-overview.md`; do not create README in any language. Its frontmatter must contain:
- `designated_root: true`
- `source_hierarchy_decision: OWNER_REPLACEMENT`
- `replaces: 05-memory-runtime/README.md`
- `authority: user-authorized operator (delegated by account owner), 2026-11-26`

Do not restore `04-memory-compiler/compiler-stage-contract.md`; PR-C is cancelled.

The original five-root restoration was concurrently merged as PR #1314 under AID-2026-113. This follow-up re-registers the same work under the fixed-range identifier AID-2026-140, corrects the exact overview authority field and reconciles all source/mirror blob evidence. Do not duplicate or rewrite source/mirror bodies.

Merge only when all 16 required contexts are SUCCESS on the exact PR head and refreshed compare reports `behind_by = 0`; merge immediately after that readback. Record PR, merge SHA and the #1212 comment.
