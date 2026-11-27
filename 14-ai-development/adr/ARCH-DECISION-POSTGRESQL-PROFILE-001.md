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
    canonical_scope: "W10 proxy disposition of PostgreSQL as a mature storage implementation"
    canonical_scope_id: "architecture-convergence/aid-2026-253"
    canonical_scope_keywords:
      - "postgresql"
      - "storage-profile"
      - "defer"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# ARCH-DECISION — PostgreSQL storage profile

- Decision ID: ARCH-DECISION-POSTGRESQL-PROFILE-001
- Decision date: 2026-11-27
- Decision authority: user-authorized operator (delegated by account owner)
- Capacity: delegated proxy adjudication; 代理裁决，非自然人 Owner 签署
- Related conflict: CF-014

## Decision

**DEFER** selection of PostgreSQL as the canonical server storage profile. This is not a rejection of PostgreSQL. Its maturity and server capabilities are relevant, but no measured workload or accepted end-to-end recovery evidence currently establishes that its operational and topology costs are required or that its physical transaction semantics have been mapped to D's logical commit contract.

## Rationale

CF-014 requires a workload, atomicity, HA, backup/restore and operational comparison. The current conflict record explicitly says L4 physical engine/deployment remains open. General product capability is not workload evidence, and choosing a server profile before establishing multi-process/multi-node requirements would be premature.

## Reopen trigger

Reopen when (1) representative workload measurements show a concrete need for server-side concurrency, multi-node availability or operational capabilities beyond the SQLite profile; or (2) an accepted deployment requirement mandates those capabilities. Require a reproducible comparison of transaction isolation/atomicity, failover, crash recovery, backup/restore, migration and operational burden, with exact versions and owner acceptance.

## Authority boundary

This decision does not reject PostgreSQL, approve production deployment, or select a physical engine. D retains logical commit authority; Storage retains physical implementation authority.
