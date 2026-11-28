---
document_metadata:
  domain: memory-brain
  role: design-specification
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
        - "14-ai-development/work-items/AID-2026-150/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Navigation stub now identifies the restored canonical source; body update is limited to source-status/path accuracy, not a semantic translation certification."
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
    canonical_scope: "D ForgetFence, producer admission, barrier and publication eligibility semantics"
    canonical_scope_id: "memory-brain/forget-fence-publication-gate"
    canonical_scope_keywords:
      - "memory-brain"
      - "forget-fence"
      - "producer-admission"
      - "publication-gate"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "03-memory-brain/forget-fence-operation-and-publication-gate.md"
    en: null
    zh-CN: "docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md"
  steward: "user-authorized operator (delegated by account owner)"
---
# Forget Fence Operation and Publication Gate

- Document ID: D-FORGET-GATE-001
- Version: 1.0 (split bilingual companion)
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: dd26e3cae2e60dbdc44a6e084004effcd2033efa
- Source: [restored root document](../../../03-memory-brain/forget-fence-operation-and-publication-gate.md) (source body blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`; restored file includes GOV-DOC-002 metadata). This page remains a non-canonical navigation stub; the split family is pending Owner disposition.
- Chinese counterpart: [Forget Fence Operation and Publication Gate](../../zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md)
- Status: D semantic contract DECIDED; E/Storage enforcement, I authorization freshness and cross-module conformance OPEN

The source contract is long and is split into four parallel bilingual reading parts. The source file remains the normative source artifact; the split documents preserve its section coverage.

1. [Part 1 — Normative invariants, typed evidence and operation contracts](forget-fence-operation-and-publication-gate-part1.md)
2. [Part 2 — Visibility boundary, evidence, fault matrix and owner decisions](forget-fence-operation-and-publication-gate-part2.md)
3. [Part 3 — Phase 3.6 linearization, state machine and proof matrix](forget-fence-operation-and-publication-gate-part3.md)
4. [Part 4 — Phase 3.6.2 JF-10 / COC exact-version Owner decisions](forget-fence-operation-and-publication-gate-part4.md)

**Important:** DECIDED describes D-owned domain semantics only. It does not assert that Storage atomicity is implemented, that E/F/G/H/I enforcement is complete, that JF-10 is production-ready, or that Forget is globally/physically complete.
