---
document_metadata:
  domain: ai-development
  role: decision-record
  lifecycle:
    approval:
      decision_status: Approved
      approver: "user-authorized operator (delegated by account owner); proxy decision only"
      decision_date: "2026-11-27"
      approved_version:
        scheme: git
        value: "PENDING_MERGE_COMMIT"
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
    canonical_scope: "W10 proxy disposition of SQLite as a mature storage implementation"
    canonical_scope_id: "architecture-convergence/aid-2026-253"
    canonical_scope_keywords:
      - "sqlite"
      - "storage-profile"
      - "defer"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# ARCH-DECISION — SQLite storage profile

- Decision ID: ARCH-DECISION-SQLITE-PROFILE-001
- Decision date: 2026-11-27
- Decision authority: user-authorized operator (delegated by account owner)
- Capacity: delegated proxy adjudication; 代理裁决，非自然人 Owner 签署
- Related conflict: CF-014

## Decision

**DEFER** selection of SQLite as the canonical deployment/storage profile. This is not a rejection of SQLite. SQLite remains a viable local/embedded candidate, but the current register evidence does not contain a representative Brain workload, an accepted physical atomicity mapping, or complete crash/restore and operational evidence.

## Rationale

CF-014 explicitly leaves the L4 engine/profile open. A mature product's existence and suitability for local use do not establish that its concurrency, durability, recovery, backup and operational characteristics satisfy the system's canonical commit and lifecycle requirements. No workload-specific comparative measurements are recorded in the evidence supplied to this decision.

## Reopen trigger

Reopen when Storage and D publish (1) a representative, reproducible Brain workload and acceptance thresholds; (2) transaction/atomicity mapping against D's canonical commit boundary; (3) crash, restore and backup verification; and (4) an operational comparison covering concurrency, deployment, monitoring and recovery. The comparison must identify exact tested versions, commands, raw results and owner acceptance.

## Authority boundary

This decision neither approves production use nor selects SQLite as canonical. It does not change D's logical commit authority or Storage's physical implementation authority.
