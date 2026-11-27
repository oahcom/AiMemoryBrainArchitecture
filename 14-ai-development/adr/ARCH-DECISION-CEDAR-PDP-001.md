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
    canonical_scope: "W10 proxy disposition of Cedar PDP as a mature authorization implementation"
    canonical_scope_id: "architecture-convergence/aid-2026-253"
    canonical_scope_keywords:
      - "cedar"
      - "pdp"
      - "authorization"
      - "defer"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# ARCH-DECISION — Cedar policy decision point

- Decision ID: ARCH-DECISION-CEDAR-PDP-001
- Decision date: 2026-11-27
- Decision authority: user-authorized operator (delegated by account owner)
- Capacity: delegated proxy adjudication; 代理裁决，非自然人 Owner 签署
- Related conflict: CF-013

## Decision

**DEFER** production adoption of Cedar PDP. Cedar remains a bounded candidate, not rejected. The existing product-first evaluation is not production approval and does not transfer authorization authority from I to an external evaluator.

## Rationale

CF-013 requires wrapper vectors, revocation tests and Owner approval. Until those exist, the integration boundary is unproven: evaluator errors must fail closed, policy inputs must be bound to current identity/scope/permission epochs, and revocation must take effect consistently. A mature PDP cannot itself establish the repository's authority allocation.

## Reopen trigger

Reopen when I publishes and accepts a version-pinned wrapper contract and executable vectors covering allow, deny, malformed input, evaluator timeout/error, missing attributes, stale PermissionEpoch, revocation, policy update and replay; all error/unknown paths must deny. Require deterministic tests and explicit I Owner approval of the wrapper and policy-authority boundary.

## Authority boundary

Cedar may only evaluate policy through an I-owned adapter. It does not mint authorization decisions independently, override I revocation, or become the source of truth for PermissionEpoch.
