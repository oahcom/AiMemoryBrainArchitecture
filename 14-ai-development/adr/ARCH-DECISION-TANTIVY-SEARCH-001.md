---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "Issue #265 — AC3 / AC4 evidence and acceptance text"
        - "AID-2026-253/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Proxy decision record; implementation selection remains deferred pending the stated measurable trigger evidence."
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
    canonical_scope: "W10 proxy disposition of Tantivy as a mature full-text search implementation"
    canonical_scope_id: "architecture-convergence/aid-2026-253"
    canonical_scope_keywords:
      - "tantivy"
      - "full-text-search"
      - "defer"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# ARCH-DECISION — Tantivy full-text search

- Decision ID: ARCH-DECISION-TANTIVY-SEARCH-001
- Decision date: 2026-11-27
- Decision authority: user-authorized operator (delegated by account owner)
- Capacity: delegated proxy adjudication; 代理裁决，非自然人 Owner 签署
- Related conflict: AC4; Issue #265

## Decision

**DEFER — NOT REJECTED** adoption of Tantivy. Tantivy remains an eligible mature search candidate; the existing DEFERRED — NOT REJECTED disposition is retained and made conditional rather than indefinite.

## Rationale

The cited req02-fts5-vs-like-decision.md records deferral, not rejection. The current evidence supplied for #265 does not include a reproducible Brain-specific workload showing that LIKE or SQLite FTS5 fails an accepted relevance, latency, indexing, consistency or operational threshold. Adopting a separate search engine without that evidence would add index lifecycle, synchronization and recovery obligations before demonstrating need.

## Reopen trigger

Reopen when a reproducible representative corpus/query benchmark shows that the selected LIKE/FTS5 baseline misses an explicit acceptance threshold, or when a product requirement needs search capabilities those options cannot provide. The evaluation must compare query quality, latency, indexing/update consistency, incremental rebuild, crash recovery, memory/disk footprint and operational complexity, pin versions and publish raw commands/results. Reopen also if the search contract requires capabilities unavailable in the current baseline.

## Authority boundary

This is not a rejection of Tantivy and does not authorize production adoption. D remains authoritative for canonical data; any search index is derived and rebuildable, with explicit consistency and recovery semantics.
