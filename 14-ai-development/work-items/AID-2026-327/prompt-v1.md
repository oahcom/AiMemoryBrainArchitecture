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
        - "14-ai-development/work-items/AID-2026-327/evidence.md"
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
    canonical_scope: "Preserves the bounded task prompt snapshot for AID-2026-327; it does not establish repository-wide requirements."
    canonical_scope_id: "ai-development/aid-2026-326-prompt"
    canonical_scope_keywords:
      - "AID-2026-327"
      - "d10-cursor-authority"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-327 Prompt v1

Record the final Owner D-10 decision from Issue #1210 (comment 7174534633) in the canonical `01-system-architecture/system-boundaries.md` and its EN/ZH-CN mirrors. The decision is final; do not reopen or reinterpret it.

Record these exact semantics:
- One deployment has one logical Brain authority. Tenant and shard are partition boundaries within that authority, not separate authorities.
- `CanonicalCommitCursor` is partitioned per tenant/shard. There is no total order across tenants or shards. A globally ordered cursor across tenants is rejected because it would require a global serialization point or distributed consensus not specified by this architecture.
- Cursor entries are ordered only within their own tenant/shard partition.
- Authority identity and epoch/incarnation are explicit parts of cursor identity. Rollover is an epoch change. Cursors from different authorities or epochs are not comparable; comparison across them is an error, never a numeric ordering.
- A cross-shard transaction produces one cursor entry per participating shard, ordered within each shard. The transaction is atomic all-or-none; atomicity does not imply a cross-shard total order, and no API may imply one.
- Aggregate revisions and lifecycle cursors remain separate domains.
- `ForgetFence`, `ProducerRegistrationHighWater`, and similar fences are per-authority and must carry authority identity and applicable target/partition scope so a fence from one shard cannot be read as covering another.
- Required negative cases: `cursor_comparison_across_authority_rejected` and `cross_shard_commit_exposes_no_total_order`.

In scope: add a clearly marked decision section to the canonical System Boundaries source, update its English and Chinese mirrors and source-revision pins, create this Work Item's evidence/session records, register one INDEX row, and maintain PR #1484's required bilingual, related-issue, session-evidence and exact-head validation declarations.

Out of scope: code, runtime, API/schema/DDL, tests, workflows, branch protection, Issue #1210 body edits, unrelated PR-body edits, and changes to the detailed D/F/G consumer documents. Do not claim that the System Boundaries document is formally approved or that downstream consumers are aligned. Preserve the document's Draft approval and Unverified evidence-verification metadata. Explicitly record the unresolved multi-shard transaction representation and F/G consistent-snapshot/cut protocol as follow-up work, not as newly decided wire semantics. No code or runtime implementation is authorized.
