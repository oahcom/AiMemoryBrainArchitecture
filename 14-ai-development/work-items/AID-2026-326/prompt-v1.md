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
        - "14-ai-development/work-items/AID-2026-326/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "This prompt is a scope snapshot, not a verbatim platform payload; provenance remains unverified."
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
    canonical_scope: "Preserves the bounded task prompt snapshot for AID-2026-326; it does not establish repository-wide requirements."
    canonical_scope_id: "ai-development/aid-2026-326-prompt"
    canonical_scope_keywords:
      - "AID-2026-326"
      - "d10-cursor-authority"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-326 Prompt v1

Record the final Owner D-10 decision from Issue #1210 (comment 7174534633) in the canonical `01-system-architecture/system-boundaries.md` and its EN/ZH-CN mirrors. The decision is final; do not reopen or reinterpret it.

Record these exact semantics:
- One deployment has one logical Brain authority; tenant and shard are partition boundaries within that authority.
- `CanonicalCommitCursor` is partitioned per tenant/shard; there is no total order across shards.
- A cross-shard transaction produces one cursor entry per participating shard and is atomic all-or-none.
- Authority identity and epoch/incarnation are explicit; cursors from different authorities are not comparable.
- Aggregate revisions and lifecycle cursors are separate.
- `ForgetFence`, `ProducerRegistrationHighWater`, and similar fences are per-authority and must carry authority identity so a fence from one shard cannot be read as covering another.

In scope: add a clearly marked decision section to the canonical system-boundaries source, update its English and Chinese mirrors and source-revision pins, create this Work Item's evidence/session records, and register one INDEX row.

Out of scope: code, runtime, API/schema/DDL, tests, workflows, branch protection, Issue/PR body edits, and changes to the detailed D/F/G consumer documents. Do not claim that the system-boundaries document is formally approved or that downstream consumers are aligned. Preserve the document's Draft approval and Unverified evidence-verification metadata. Explicitly record the unresolved multi-shard transaction representation and F/G consistent-snapshot protocol as follow-up work, not as newly decided wire semantics.
