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
        - "14-ai-development/work-items/AID-2026-342/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "The prompt body is retained verbatim as the session input snapshot. The manifest records the snapshot digest and byte count; those values must identify the committed file blob after this metadata block is added. No CI result or independent review is asserted."
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
  steward: "user-authorized operator (delegated by account owner)"
---
# AID-2026-293 Prompt Snapshot v1

Prepare one documentation-only carrier for Issue #262 in `oahcom/AiMemoryBrainArchitecture`, using exact baseline `31c1e5d83e7dad326dbd4b69d4a8e19534718ff1`.

Scope is limited to AC3, AC4, AC6 and AC8.

Requirements:
- Preserve existing risk and complexity document content except for precise append-only patches.
- AC3: each of ten risk evidence cells must ultimately contain either a parseable `path:line` with an adjacent verbatim quote, or `NO_EVIDENCE_FOUND` with an actually executed search command and exact search scope.
- AC4: add four named dimensions (change surface, coupling, irreversibility, concurrency/state), a 1–5 rubric, scores for every module and a per-row `path:line` or `EVIDENCE_GAP`. Retain the historical eight-number column.
- AC6: provide a directly runnable Python checker, data file and unittest suite. Include one inline negative fixture for each of seven rules. Exit codes: 0 pass, 1 rule violation, 2 invalid arguments/input.
- AC8: provide bilingual review templates with baseline blob SHAs, `PENDING_INDEPENDENT_REVIEW`, and `TO_BE_FILLED_BY_INDEPENDENT_REVIEWER`. Do not self-sign.
- Add work-item manifest, evidence, session evidence, prompt snapshot and one INDEX registration row.
- PR body must identify Issue #262, AI assistance, bilingual manifest, per-AC evidence/status and explicit non-claims.

No repository writes, Issue edits, PR creation or merge are authorized by this prompt snapshot. Unexecuted searches/tests and independent review must remain pending.
