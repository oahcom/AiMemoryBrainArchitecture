---
document_metadata:
  domain: memory-brain
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-11-26-SOURCE-RESTORE-02"
        - "Issue #1177"
        - "source commit: b525e1f8fee2471a131e4a38efda99804045e424"
        - "original source blob: 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Existing translated companion body preserved; source pin refreshed; semantic parity review pending."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "03-memory-brain/forget-fence-operation-and-publication-gate.md"
    en: "docs/en/03-memory-brain/forget-fence-operation-and-publication-gate.md"
    zh-CN: "docs/zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md"
---

# Forget Fence Operation and Publication Gate

- Document ID: D-FORGET-GATE-001
- Version: 1.0 (split bilingual companion)
- Source branch: session-d-memory-brain-2026-11-16
- Source revision: d3ddfff9500d9138d643989e8496d99b8d9ed79e
- Source: [canonical D source](../../../03-memory-brain/forget-fence-operation-and-publication-gate.md) (source commit `b525e1f8fee2471a131e4a38efda99804045e424`; original source blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`).
- Chinese counterpart: [Forget Fence Operation and Publication Gate](../../zh-CN/03-memory-brain/forget-fence-operation-and-publication-gate.md)
- Status: D semantic contract DECIDED; E/Storage enforcement, I authorization freshness and cross-module conformance OPEN

The source contract is long and is split into four parallel bilingual reading parts. The source file remains the normative source artifact; the split documents preserve its section coverage.

1. [Part 1 — Normative invariants, typed evidence and operation contracts](forget-fence-operation-and-publication-gate-part1.md)
2. [Part 2 — Visibility boundary, evidence, fault matrix and owner decisions](forget-fence-operation-and-publication-gate-part2.md)
3. [Part 3 — Phase 3.6 linearization, state machine and proof matrix](forget-fence-operation-and-publication-gate-part3.md)
4. [Part 4 — Phase 3.6.2 JF-10 / COC exact-version Owner decisions](forget-fence-operation-and-publication-gate-part4.md)

**Important:** DECIDED describes D-owned domain semantics only. It does not assert that Storage atomicity is implemented, that E/F/G/H/I enforcement is complete, that JF-10 is production-ready, or that Forget is globally/physically complete.
